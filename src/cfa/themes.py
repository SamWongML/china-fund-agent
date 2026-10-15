"""Theme watchlist: find every onshore product for each watched field, plus a discovery scan of fields not watched.

The theme-scout skill (Claude) decides which fields go in watchlist/themes.yaml and why. This module does the
counting: it matches product names in the latest ETF/LOF snapshot against each theme's keywords, collapses
same-index copies from different issuers into one row per index family (keeping the most liquid issuer),
and computes stage statistics the scout and the Sunday advisor read: launches, turnover, news mentions.

    python -m cfa.themes check                 # validate watchlist/themes.yaml
    python -m cfa.themes scan [--date D]       # write weekly/<week>/theme_scan.md from the repo's snapshots
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys

import pandas as pd

from .common import RAW, ROOT, WEEKLY, iso_week_label, last_trading_day, load_universe, load_yaml, log, md_table, \
    today_hkt

WATCHLIST = ROOT / "watchlist" / "themes.yaml"
STATUSES = {"active", "watch-only", "retired"}
STAGES = {"emerging", "growth", "crowded", "fading"}
REQUIRED = {"id", "name", "status", "stage", "added", "review_by", "thesis", "policy", "match", "news", "falsifiers"}


def cfg() -> dict:
    return load_universe().get("watch_themes") or {}


def load_watchlist() -> list[dict]:
    rows = (load_yaml(WATCHLIST) or {}).get("themes") or []
    return [dict(r) for r in rows if r and r.get("id")]


def active(themes: list[dict] | None = None) -> list[dict]:
    """Active themes, capped at max_active in file order (the scout lists the most important first)."""
    themes = load_watchlist() if themes is None else themes
    return [t for t in themes if t.get("status") == "active"][: int(cfg().get("max_active", 8))]


def validate(themes: list[dict]) -> list[str]:
    errs, seen = [], set()
    for t in themes:
        tid = t.get("id", "?")
        errs += [f"{tid}: missing {k}" for k in sorted(REQUIRED - t.keys())]
        if not re.fullmatch(r"[a-z0-9_]+", str(tid)):
            errs.append(f"{tid}: id must be lower_snake_case")
        if tid in seen:
            errs.append(f"{tid}: duplicate id")
        seen.add(tid)
        if t.get("status") not in STATUSES:
            errs.append(f"{tid}: status must be one of {sorted(STATUSES)}")
        if t.get("stage") not in STAGES:
            errs.append(f"{tid}: stage must be one of {sorted(STAGES)}")
        for k in ("policy", "match", "news"):
            if k in t and (not isinstance(t[k], list) or not t[k]):
                errs.append(f"{tid}: {k} must be a non-empty list")
        for k in ("added", "review_by"):
            try:
                dt.date.fromisoformat(str(t.get(k)))
            except ValueError:
                errs.append(f"{tid}: {k} must be YYYY-MM-DD")
    n_active = sum(t.get("status") == "active" for t in themes)
    if n_active > int(cfg().get("max_active", 8)):
        errs.append(f"{n_active} active themes > watch_themes.max_active; only the first ones are used")
    return errs


# ---------- products ----------

def family(name: str) -> str:
    """Index family: the name without the issuer suffix and share class ("机器人ETF华夏" -> "机器人ETF")."""
    n = re.sub(r"[A-Z]$", "", str(name))
    return re.sub(r"(ETF|LOF).*$", r"\1", n)


def _latest(dataset: str, asof: dt.date) -> pd.DataFrame:
    files = sorted((RAW / "funds" / dataset).rglob("*.parquet"))
    files = [f for f in files if dt.date.fromisoformat(f.stem) <= asof]
    return pd.read_parquet(files[-1]) if files else pd.DataFrame()


def exchange_products(asof: dt.date) -> pd.DataFrame:
    """ETFs and LOFs in the latest snapshot on or before asof, with inception date and ranked returns."""
    frames = []
    for kind in ("etf", "lof"):
        df = _latest(kind, asof)
        if not df.empty:
            frames.append(df.reindex(columns=["code", "name", "turnover_cny"]).assign(kind=kind))
    if not frames:
        return pd.DataFrame(columns=["code", "name", "turnover_cny", "kind", "family"])
    df = pd.concat(frames, ignore_index=True).drop_duplicates("code")
    rank = _latest("exchange_rank", asof)
    if not rank.empty:
        df = df.merge(rank.reindex(columns=["code", "inception", "r_1m", "r_3m"]), on="code", how="left")
    df["turnover_cny"] = pd.to_numeric(df["turnover_cny"], errors="coerce").fillna(0)
    df["family"] = df["name"].map(family)
    return df


def _excluded(names: pd.Series, extra: list[str]) -> pd.Series:
    words = list(cfg().get("exclude_name_keywords") or []) + list(extra or [])
    return names.astype(str).apply(lambda n: any(w in n for w in words))


def matches(theme: dict, df: pd.DataFrame) -> pd.DataFrame:
    """All products whose name contains one of the theme's match keywords (no liquidity filter)."""
    if df.empty:
        return df
    words = [str(w) for w in theme.get("match") or []]
    hit = df["name"].astype(str).apply(lambda n: any(w in n for w in words))
    return df[hit & ~_excluded(df["name"], theme.get("exclude") or [])]


def families(df: pd.DataFrame, min_turnover: float) -> pd.DataFrame:
    """One row per index family: the most liquid issuer, with the family's issuer count and total turnover."""
    if df.empty:
        return df.assign(issuers=pd.Series(dtype=int), family_turnover_cny_m=pd.Series(dtype=float))
    g = df.groupby("family")
    out = df.sort_values("turnover_cny", ascending=False).drop_duplicates("family").set_index("family")
    out["issuers"] = g.size()
    out["family_turnover_cny_m"] = (g["turnover_cny"].sum() / 1e6).round(1)
    out = out[out["turnover_cny"] >= min_turnover]
    return out.reset_index().sort_values("turnover_cny", ascending=False)


def theme_products(theme: dict, df: pd.DataFrame) -> pd.DataFrame:
    c = cfg()
    fam = families(matches(theme, df), float(c.get("min_turnover_cny", 2e7)))
    return fam.head(int(c.get("max_products", 6))).reset_index(drop=True)


def launches(df: pd.DataFrame, asof: dt.date, days: int) -> int:
    if df.empty or "inception" not in df:
        return 0
    inc = pd.to_datetime(df["inception"], errors="coerce")
    return int((inc >= pd.Timestamp(asof - dt.timedelta(days=days))).sum())


def news_counts(theme: dict, sunday: dt.date, load_day) -> tuple[int, float]:
    """Items mentioning a news keyword this week, and the weekly average over the 4 weeks before."""
    words = [str(w) for w in theme.get("news") or []]

    def count(days):
        n = 0
        for d in days:
            for i in load_day(d):
                text = f"{i.get('title', '')} {i.get('summary', '')}"
                n += any(w in text for w in words)
        return n
    this = count([sunday - dt.timedelta(days=i) for i in range(7, 0, -1)])
    prev = count([sunday - dt.timedelta(days=i) for i in range(35, 7, -1)])
    return this, round(prev / 4, 1)


def theme_stats(theme: dict, df: pd.DataFrame, asof: dt.date) -> dict:
    m = matches(theme, df)
    return {"products_matched": int(len(m)), "index_families": int(m["family"].nunique()) if len(m) else 0,
            "launched_6m": launches(m, asof, 182), "launched_12m": launches(m, asof, 365),
            "turnover_cny_m": round(float(m["turnover_cny"].sum()) / 1e6, 1) if len(m) else 0.0}


# ---------- discovery scan ----------

def scan(df: pd.DataFrame, asof: dt.date, themes: list[dict] | None = None) -> pd.DataFrame:
    """Every index family in the snapshot with launches, turnover and median returns, tagged with the watched
    theme it falls under (if any). Cross-border and bond products are left out, as in the candidate screen."""
    if df.empty:
        return df
    themes = load_watchlist() if themes is None else themes
    df = df[~_excluded(df["name"], [])].copy()
    tags: dict = {i: [] for i in df.index}
    for t in themes:
        if t.get("status") != "retired":
            for i in matches(t, df).index:
                tags[i].append(t["id"])
    df["theme"] = pd.Series({i: ",".join(v) for i, v in tags.items()}, dtype=str)
    inc = pd.to_datetime(df.get("inception"), errors="coerce") if "inception" in df else pd.Series(pd.NaT, index=df.index)
    df["new_12m"] = inc >= pd.Timestamp(asof - dt.timedelta(days=365))
    g = df.groupby("family")
    out = pd.DataFrame({
        "issuers": g.size(),
        "launched_12m": g["new_12m"].sum().astype(int),
        "turnover_cny_m": (g["turnover_cny"].sum() / 1e6).round(1),
        "median_r_1m": g["r_1m"].median().round(2) if "r_1m" in df else None,
        "median_r_3m": g["r_3m"].median().round(2) if "r_3m" in df else None,
        "watched_as": g["theme"].agg(lambda s: ",".join(sorted({x for v in s for x in v.split(",") if x}))),
    })
    return out.reset_index().sort_values("turnover_cny_m", ascending=False)


def scan_markdown(table: pd.DataFrame, asof: dt.date, top: int = 40) -> str:
    lines = [f"# Theme discovery scan (snapshot {asof})", "",
             "One row per index family (issuer suffix removed). issuers = products tracking it; launched_12m = "
             "products listed in the last 12 months (a launch wave is a late, crowded signal: Ben-David et al.); "
             "turnover is the latest day's total; returns are medians across the family's products, in %. "
             "watched_as names the watchlist theme it falls under, blank if none.", ""]
    if table.empty:
        return "\n".join(lines + ["_no snapshot available_", ""])
    lines += ["## Busiest families not on the watchlist", "",
              md_table(table[table["watched_as"] == ""].head(top)), "",
              "## Most new launches in 12 months (all families)", "",
              md_table(table.sort_values(["launched_12m", "turnover_cny_m"], ascending=False).head(20)), "",
              "## Watched families", "", md_table(table[table["watched_as"] != ""]), ""]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    s = sub.add_parser("scan")
    s.add_argument("--date", type=dt.date.fromisoformat)
    args = ap.parse_args()
    if args.cmd == "check":
        errs = validate(load_watchlist())
        for e in errs:
            print(e, file=sys.stderr)
        print("watchlist ok" if not errs else f"{len(errs)} problem(s)")
        return 1 if errs else 0
    day = args.date or today_hkt()
    asof = last_trading_day(day)
    out = WEEKLY / iso_week_label(day) / "theme_scan.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(scan_markdown(scan(exchange_products(asof), asof), asof), encoding="utf-8")
    log.info("wrote %s", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
