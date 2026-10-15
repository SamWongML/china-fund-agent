"""Sunday deterministic build: candidate screen, fact sheets, news rollup, scorecard, readiness flag.

Writes weekly/YYYY-Www/{factsheets.md, candidates.csv, news_rollup.md, inputs.json}. The weekly-digest skill
reads only these files plus journal/scorecard_summary.md and recent reflections.

    python -m cfa.weekly_build [--date 2026-10-18]
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import json

import numpy as np
import pandas as pd

from . import scorecard
from .collect_funds import snapshot_path, update_history
from .collect_news import load_day
from .common import (CONFIG, HISTORY, NEWS, RAW, REF, WEEKLY, guess_type, iso_week_label, last_trading_day,
                     load_holdings, load_universe, load_yaml, log, log_run, md_table, now_hkt, read_status, retry,
                     today_hkt, update_status, watch_codes, write_json, STATE)


def latest_snapshot(dataset: str, on_or_before: dt.date, n: int = 1) -> list[tuple[dt.date, pd.DataFrame]]:
    files = sorted((RAW / "funds" / dataset).rglob("*.parquet"))
    files = [f for f in files if dt.date.fromisoformat(f.stem) <= on_or_before][-n:]
    return [(dt.date.fromisoformat(f.stem), pd.read_parquet(f)) for f in files]


def zscore(s: pd.Series) -> pd.Series:
    sd = s.std()
    return (s - s.mean()) / sd if sd and sd == sd else s * 0


# ---------- candidate screen ----------

def screen(asof: dt.date, held: set[str]) -> pd.DataFrame:
    cfg = load_universe().get("screen") or {}
    frames = []
    open_rank = latest_snapshot("open_rank", asof)
    if open_rank:
        df = open_rank[0][1].copy()
        names_path = REF / "fund_names.parquet"
        if names_path.exists():
            names = pd.read_parquet(names_path)[["基金代码", "基金类型"]].rename(columns={"基金代码": "code", "基金类型": "type"})
            df = df.merge(names, on="code", how="left")
        else:
            df["type"] = "开放式"
        snap = latest_snapshot("open", asof)
        if snap:
            st = snap[0][1].reindex(columns=["code", "purchase"])
            df = df.merge(st, on="code", how="left")
            df = df[df["purchase"].fillna("").str.contains("开放")]
        df["kind"] = "open"
        frames.append(df)
    ex_rank = latest_snapshot("exchange_rank", asof)
    if ex_rank:
        df = ex_rank[0][1].copy()
        etf = latest_snapshot("etf", asof)
        if etf:
            e = etf[0][1].reindex(columns=["code", "turnover_cny", "premium_pct"])
            df = df.merge(e, on="code", how="left")
        lof = latest_snapshot("lof", asof)
        if lof:
            lt = lof[0][1].reindex(columns=["code", "turnover_cny"]).rename(columns={"turnover_cny": "lof_turnover"})
            df = df.merge(lt, on="code", how="left")
            df["turnover_cny"] = df.get("turnover_cny", pd.Series(index=df.index, dtype=float)).fillna(df["lof_turnover"])
        df = df[df["turnover_cny"].fillna(0) >= cfg.get("min_etf_turnover_cny", 5e7)]
        df["kind"] = df["code"].map(lambda c: "etf" if guess_type(c) == "etf" else "lof")
        frames.append(df)
    if not frames:
        return pd.DataFrame()
    df = pd.concat(frames, ignore_index=True)
    df["type"] = df["type"].fillna("").astype(str)
    excl = cfg.get("exclude_name_keywords") or []
    mask = ~df["name"].astype(str).apply(lambda n: any(k in n for k in excl)) & ~df["type"].str.contains("货币|理财|QDII|海外")
    df = df[mask & df["r_1y"].notna() & df["r_3m"].notna()]
    df = df[~df["code"].isin(held)]
    df["group"] = df["type"].str.split("-").str[:2].str.join("-").replace("", "other")
    # Drop data artifacts (one-off jumps from tiny funds or share events): weekly move far outside the group norm.
    med = df.groupby("group")["r_1w"].transform("median")
    mad = df.groupby("group")["r_1w"].transform(lambda s: (s - s.median()).abs().median())
    df = df[(df["r_1w"] - med).abs() <= 8 * mad.fillna(0) + 2]
    weights = cfg.get("weights") or {"r_1m": .2, "r_3m": .35, "r_6m": .25, "r_1y": .2}
    # Percentile ranks within the group are robust to outliers; scale 0-100.
    df["score"] = 0.0
    for col, w in weights.items():
        df["score"] += w * df.groupby("group")[col].rank(pct=True).fillna(0.5) * 100
    df["chase_warning"] = df["r_1w"].fillna(0) > cfg.get("chase_warning_1w_pct", 8)
    df["asset"] = np.where(df["group"].str.contains("债|固收"), "bond", "growth")
    # collapse share classes (A/C/E...) and keep the best scoring one
    # ...and ETFs tracking the same index from different issuers ("银行ETF富国" / "银行ETF华夏")
    df["base_name"] = df["name"].astype(str).str.replace(r"[A-Z]$", "", regex=True).str.replace(r"(ETF).*$", r"\1", regex=True)
    df = df.sort_values("score", ascending=False).drop_duplicates("base_name")
    df = df.groupby("group", group_keys=False).head(cfg.get("max_per_type", 3))
    df = df.sort_values("score", ascending=False)
    bonds = df[df["asset"] == "bond"].head(cfg.get("max_bond_candidates", 4))
    growth = df[df["asset"] != "bond"].head(cfg.get("max_candidates", 20) - len(bonds))
    df = pd.concat([growth, bonds]).sort_values("score", ascending=False)
    keep = ["code", "name", "kind", "group", "score", "r_1w", "r_1m", "r_3m", "r_6m", "r_1y", "chase_warning"]
    keep += [c for c in ("turnover_cny", "premium_pct") if c in df]
    out = df[keep].copy()
    out["score"] = out["score"].round(1)
    return out.reset_index(drop=True)


# ---------- fact sheets ----------

def facts(code: str, kind: str, etf_snaps: list[tuple[dt.date, pd.DataFrame]]) -> dict:
    p = HISTORY / "nav" / f"{code}.csv"
    f: dict = {"code": code, "kind": kind}
    if p.exists():
        h = pd.read_csv(p, dtype={"date": str})
        px = h["price"].astype(float).to_numpy()
        f["last_date"] = h["date"].iloc[-1]
        f["basis"] = h["basis"].iloc[-1] if "basis" in h else None

        def r(n):
            return round((px[-1] / px[-1 - n] - 1) * 100, 2) if len(px) > n else None
        f.update({"r_1w": r(5), "r_4w": r(20), "r_12w": r(60), "r_26w": r(120), "r_52w": r(250)})
        win = px[-250:]
        if len(win) > 20:
            peak = np.maximum.accumulate(win)
            f["max_dd_52w"] = round(float(((win / peak) - 1).min() * 100), 2)
            f["off_52w_high"] = round(float((win[-1] / win.max() - 1) * 100), 2)
            rets = np.diff(np.log(px[-61:]))
            f["vol_60d_ann"] = round(float(rets.std() * np.sqrt(250) * 100), 2)
            f["above_ma20"] = bool(px[-1] > px[-20:].mean())
            f["above_ma60"] = bool(len(px) >= 60 and px[-1] > px[-60:].mean())
    if kind == "etf" and etf_snaps:
        last = etf_snaps[-1][1].set_index("code")
        if code in last.index:
            row = last.loc[code]
            f["premium_pct"] = None if pd.isna(row.get("premium_pct")) else round(float(row["premium_pct"]), 2)
            f["turnover_cny_m"] = None if pd.isna(row.get("turnover_cny")) else round(float(row["turnover_cny"]) / 1e6, 1)
            f["name"] = row.get("name")
            first = etf_snaps[0][1].set_index("code")
            if code in first.index and "shares" in last and pd.notna(row.get("shares")) and first.loc[code].get("shares"):
                f["shares_chg_5d_pct"] = round((float(row["shares"]) / float(first.loc[code]["shares"]) - 1) * 100, 2)
    return f


def holding_facts(h: dict, f: dict, asof: dt.date) -> dict:
    p = HISTORY / "nav" / f"{h['code']}.csv"
    out = {"name": h.get("name", f.get("name", "")), "units": h.get("units"), "cost": h.get("cost"),
           "bought": str(h.get("bought", ""))}
    if p.exists() and h.get("units") and h.get("cost"):
        raw_last = None
        # Holding P&L must use the unadjusted price, which the user can compare with their broker.
        # History uses adjusted prices, so approximate with the latest raw snapshot price when available.
        for ds, col in (("etf", "close"), ("lof", "close"), ("open", "nav")):
            snaps = latest_snapshot(ds, asof)
            if snaps:
                s = snaps[0][1].set_index("code")
                if h["code"] in s.index and pd.notna(s.loc[h["code"]][col]):
                    raw_last = float(s.loc[h["code"]][col])
                    break
        if raw_last:
            out["last_price"] = raw_last
            out["value_cny"] = round(raw_last * float(h["units"]), 2)
            out["pnl_pct"] = round((raw_last / float(h["cost"]) - 1) * 100, 2)
    if h.get("bought"):
        try:
            out["days_held"] = (asof - dt.date.fromisoformat(str(h["bought"]))).days
        except ValueError:
            pass
    return out


def news_rollup(sunday: dt.date) -> tuple[str, dict]:
    days = [sunday - dt.timedelta(days=i) for i in range(7, 0, -1)]
    prev = [sunday - dt.timedelta(days=i) for i in range(14, 7, -1)]
    this_items = [i for d in days for i in load_day(d)]
    prev_items = [i for d in prev for i in load_day(d)]
    cnt = collections.Counter(t for i in this_items for t in i.get("themes") or [])
    pcnt = collections.Counter(t for i in prev_items for t in i.get("themes") or [])
    themes = sorted(set(cnt) | set(pcnt), key=lambda t: -cnt[t])
    theme_df = pd.DataFrame([{"theme": t, "this_week": cnt[t], "prev_week": pcnt[t]} for t in themes])
    top = sorted(this_items, key=lambda i: -i.get("score", 0))[:30]
    digests = [f"news/daily/{d}.md" for d in days if (NEWS / "daily" / f"{d}.md").exists()]
    lines = [f"# News rollup, week ending {sunday}", "",
             f"{len(this_items)} unique items this week, {len(prev_items)} last week.", "",
             "## Daily digests to read", ""] + [f"- {p}" for p in digests] + (["- _none written_"] if not digests else [])
    lines += ["", "## Theme mentions (mechanical keyword counts)", "",
              md_table(theme_df) if not theme_df.empty else "_none_", "", "## Top 30 items by score", ""]
    lines += [f"- {i['ts'][:16]} [{i['region']}][s{i.get('score', 0)}] {i['title']}" for i in top]
    try:
        import akshare as ak
        frames = []
        for k in range(1, 8):
            d = sunday + dt.timedelta(days=k)
            frames.append(retry(lambda: ak.macro_info_ws(date=d.strftime("%Y%m%d")), attempts=2, name="macro_info_ws"))
        cal = pd.concat(frames)
        cal = cal[pd.to_numeric(cal["重要性"], errors="coerce").fillna(0) >= 2][["时间", "地区", "事件", "重要性", "预期", "前值"]]
        lines += ["", "## Macro calendar, next 7 days (importance ≥ 2)", "", md_table(cal.head(60))]
    except Exception as e:
        lines += ["", f"_macro calendar unavailable: {str(e)[:120]}_"]
    return "\n".join(lines) + "\n", {"themes_this_week": dict(cnt), "digests": digests}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", type=dt.date.fromisoformat, help="the Sunday (HKT) this build is for")
    args = ap.parse_args()
    sunday = args.date or today_hkt()
    week = iso_week_label(sunday)
    out_dir = WEEKLY / week
    out_dir.mkdir(parents=True, exist_ok=True)
    asof = last_trading_day(sunday)
    holdings = load_holdings()
    held = {h["code"] for h in holdings}

    hist = update_history(watch_codes())
    cands = screen(asof, held)
    if not cands.empty:
        hist |= update_history({c: k for c, k in zip(cands["code"], cands["kind"])})
        cands.to_csv(out_dir / "candidates.csv", index=False)
    etf_snaps = latest_snapshot("etf", asof, n=6)

    hold_rows = []
    for h in holdings:
        kind = (h.get("type") or guess_type(h["code"])).lower()
        f = facts(h["code"], kind, etf_snaps)
        hold_rows.append(f | holding_facts(h, f, asof))
    cand_rows = [facts(c, k, etf_snaps) | {"name": n, "screen_score": s, "chase_warning": bool(w)}
                 for c, k, n, s, w in zip(cands.get("code", []), cands.get("kind", []), cands.get("name", []),
                                          cands.get("score", []), cands.get("chase_warning", []))]
    theme_rows = []
    for theme, spec in (load_universe().get("themes") or {}).items():
        for c in spec.get("etfs") or []:
            f = facts(str(c).zfill(6), "etf", etf_snaps)
            theme_rows.append({"theme": theme, **{k: f.get(k) for k in ("code", "name", "r_1w", "r_4w", "r_12w",
                                                                         "off_52w_high", "premium_pct", "shares_chg_5d_pct")}})

    rollup_md, rollup_meta = news_rollup(sunday)
    (out_dir / "news_rollup.md").write_text(rollup_md, encoding="utf-8")
    score = scorecard.main()

    funds_status = read_status("funds")
    last_ok = funds_status.get("last_ok_date")
    stale_days = (asof - dt.date.fromisoformat(last_ok)).days if last_ok else None
    ready = bool(last_ok) and stale_days is not None and stale_days <= 3
    missing_hist = [c for c in held if not (HISTORY / "nav" / f"{c}.csv").exists()]
    if missing_hist:
        ready = False

    def tbl(rows):
        return md_table(pd.DataFrame(rows)) if rows else "_none_"
    md = [f"# Fact sheets {week} (data as of {asof}, built {now_hkt():%Y-%m-%d %H:%M} HKT)", "",
          f"Data ready: **{ready}** (last good fund snapshot {last_ok}; missing history: {missing_hist or 'none'}).", "",
          "Returns in %: r_1w=5 trading days, r_4w=20, r_12w=60, r_26w=120, r_52w=250. "
          "Prices are adjusted for splits and dividends (ETF/LOF) or total-return NAV (open funds); basis says which. "
          "pnl_pct uses the raw latest price.", "",
          "## Holdings", "", tbl(hold_rows), "", "## Candidates (pre-screened, not held)", "", tbl(cand_rows), "",
          "## Theme ETFs", "", tbl(theme_rows), ""]
    (out_dir / "factsheets.md").write_text("\n".join(md), encoding="utf-8")
    inputs = {"week": week, "sunday": str(sunday), "asof": str(asof), "ready": ready, "holdings": hold_rows,
              "candidates": cand_rows, "themes": theme_rows, "scorecard": score, "news": rollup_meta,
              "risk_rules": load_yaml(CONFIG / "risk_rules.yaml"), "target": load_yaml(CONFIG / "target.yaml")}
    write_json(out_dir / "inputs.json", inputs)
    update_status("weekly_build", {"week": week, "asof": str(asof), "ready": ready, "candidates": len(cand_rows)})
    log_run("weekly_build", True, week=week, ready=ready, history_failures=[c for c, v in hist.items() if not v["ok"]])
    log.info("weekly build %s ready=%s candidates=%d", week, ready, len(cand_rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
