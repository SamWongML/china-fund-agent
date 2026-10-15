"""Grade past decisions against what happened next, and track the portfolio against the return target.

Entry price is the first price dated strictly after the decision date (no same-day look-ahead).
Exit is the first price on or after entry + horizon. Unfinished decisions are marked to market as "open".
Writes journal/scorecard.csv and journal/scorecard_summary.md.
"""
from __future__ import annotations

import datetime as dt

import pandas as pd

from .common import CONFIG, HISTORY, JOURNAL, load_holdings, load_universe, load_yaml, log, md_table, write_json
from .journal import read_all
from .portfolio import read_baseline

UP_ACTIONS = {"buy", "add", "hold", "watch"}


def load_prices(code: str) -> pd.Series | None:
    p = HISTORY / "nav" / f"{code}.csv"
    if not p.exists():
        return None
    df = pd.read_csv(p, dtype={"date": str})
    return pd.Series(df["price"].values, index=pd.to_datetime(df["date"])).sort_index()


def load_index(sym: str) -> pd.Series | None:
    p = HISTORY / "index" / f"{sym}.csv"
    if not p.exists():
        return None
    df = pd.read_csv(p)
    return pd.Series(df["close"].values, index=pd.to_datetime(df["date"])).sort_index()


def first_after(s: pd.Series, when: pd.Timestamp, strict: bool) -> tuple[pd.Timestamp, float] | None:
    sel = s[s.index > when] if strict else s[s.index >= when]
    return (sel.index[0], float(sel.iloc[0])) if len(sel) else None


def grade(rec: dict, bench: pd.Series | None) -> dict:
    out = {k: rec.get(k) for k in ("id", "week", "code", "action", "confidence", "p_up", "view", "theme",
                                   "horizon_weeks", "held")}
    out["override"] = bool(rec.get("override"))
    prices = load_prices(rec["code"])
    decided = pd.Timestamp(rec["ts"][:10])
    if prices is None or (entry := first_after(prices, decided, strict=True)) is None:
        return out | {"status": "pending"}
    e_date, e_px = entry
    due = e_date + pd.Timedelta(weeks=int(rec["horizon_weeks"]))
    exit_ = first_after(prices, due, strict=False)
    status = "closed" if exit_ else "open"
    x_date, x_px = exit_ if exit_ else (prices.index[-1], float(prices.iloc[-1]))
    ret = (x_px / e_px - 1) * 100
    b_ret = None
    if bench is not None:
        b0, b1 = first_after(bench, e_date, False), first_after(bench, x_date, False)
        if b0 and b1:
            b_ret = (b1[1] / b0[1] - 1) * 100
    excess = ret - b_ret if b_ret is not None else None
    hit = None
    if status == "closed" and excess is not None:
        hit = excess > 0 if rec["action"] in UP_ACTIONS else excess < 0
    return out | {"status": status, "entry_date": e_date.date(), "exit_date": x_date.date(), "ret_pct": round(ret, 2),
                  "bench_ret_pct": round(b_ret, 2) if b_ret is not None else None,
                  "excess_pct": round(excess, 2) if excess is not None else None, "hit": hit,
                  "beat": (excess > 0) if status == "closed" and excess is not None else None}


def portfolio_month(bench: pd.Series | None, target_monthly: float) -> dict:
    """Value-weighted return of current holdings over the last ~21 trading days vs target and benchmark."""
    rows, total = [], 0.0
    for h in load_holdings():
        s = load_prices(h["code"])
        if s is None or len(s) < 22:
            continue
        value = float(h.get("units") or 0) * float(s.iloc[-1])
        rows.append((value, (s.iloc[-1] / s.iloc[-22] - 1) * 100))
        total += value
    if not rows or total <= 0:
        return {"portfolio_1m_pct": None}
    ret = sum(v * r for v, r in rows) / total
    b = (bench.iloc[-1] / bench.iloc[-22] - 1) * 100 if bench is not None and len(bench) > 22 else None
    return {"portfolio_1m_pct": round(ret, 2), "target_1m_pct": round(target_monthly, 2),
            "bench_1m_pct": round(b, 2) if b is not None else None, "gap_vs_target_pct": round(ret - target_monthly, 2)}


def main() -> dict:
    target = load_yaml(CONFIG / "target.yaml")
    annual = float(target.get("annual_target_pct", 12))
    target_monthly = ((1 + annual / 100) ** (1 / 12) - 1) * 100
    bench_sym = (load_universe().get("benchmarks") or {}).get("primary", "sh000300")
    bench = load_index(bench_sym)
    graded = [grade(r, bench) for r in read_all()]
    df = pd.DataFrame(graded)
    JOURNAL.mkdir(parents=True, exist_ok=True)
    if not df.empty:
        df.to_csv(JOURNAL / "scorecard.csv", index=False)
    closed = df[df["status"] == "closed"] if not df.empty else df
    base = pd.DataFrame([grade(r, bench) for r in read_baseline()])
    base_closed = base[base["status"] == "closed"] if not base.empty else base
    if not base.empty:
        base.to_csv(JOURNAL / "rules_baseline_scorecard.csv", index=False)
    pm = portfolio_month(bench, target_monthly)
    # Brier score: confidence read as the probability the call is right (lower is better; 0.25 = coin flip).
    brier = None
    if len(closed):
        ok = closed["hit"].notna()
        brier = round(float(((closed.loc[ok, "confidence"].astype(float) - closed.loc[ok, "hit"].astype(float)) ** 2).mean()), 3)
    # Same for p_up (probability of beating the benchmark), on every call that carries one.
    with_p = closed[closed["p_up"].notna() & closed["beat"].notna()] if len(closed) and "p_up" in closed else closed.iloc[0:0]
    brier_p = round(float(((with_p["p_up"].astype(float) - with_p["beat"].astype(float)) ** 2).mean()), 3) \
        if len(with_p) else None
    summary = {
        "decisions": int(len(df)), "closed": int(len(closed)),
        "hit_rate_pct": round(closed["hit"].mean() * 100, 1) if len(closed) else None,
        "avg_excess_pct": round(closed["excess_pct"].mean(), 2) if len(closed) else None,
        "brier": brier, "brier_p_up": brier_p,
        "rules_closed": int(len(base_closed)),
        "rules_hit_rate_pct": round(base_closed["hit"].mean() * 100, 1) if len(base_closed) else None,
        "rules_avg_excess_pct": round(base_closed["excess_pct"].mean(), 2) if len(base_closed) else None,
        "annual_target_pct": annual, **pm, "benchmark": bench_sym,
    }
    lines = ["# Scorecard", "",
             f"Target: {annual:g}%/yr (≈{target_monthly:.2f}%/month). Benchmark: {bench_sym}. "
             "Entry = first price after the decision date; hit = beat the benchmark (or underperformed it for trim/sell). "
             "rules_* = the mechanical core/satellite calls (journal/rules_baseline.jsonl), graded the same way; "
             "the advisor should beat them. Brier: lower is better, 0.25 is a coin flip.",
             "", md_table(pd.DataFrame([summary])), ""]
    if len(closed):
        by = closed.groupby("action").agg(n=("id", "count"), hit_rate=("hit", "mean"), avg_excess=("excess_pct", "mean"))
        by = by.round(2).reset_index()
        lines += ["## By action (closed)", "", md_table(by), ""]
        ov = closed.groupby("override").agg(n=("id", "count"), hit_rate=("hit", "mean"),
                                            avg_excess=("excess_pct", "mean")).round(2).reset_index()
        lines += ["## Overrides of the rules-only call (closed)", "", md_table(ov), ""]
        closed = closed.assign(conf_bucket=pd.cut(closed["confidence"].astype(float), [0, .5, .7, .85, 1.0]))
        cal = closed.groupby("conf_bucket", observed=True).agg(n=("id", "count"), hit_rate=("hit", "mean")).round(2)
        lines += ["## Confidence calibration (closed)", "", md_table(cal.reset_index().astype(str)), ""]
    if len(with_p):
        wp = with_p.assign(p_bucket=pd.cut(with_p["p_up"].astype(float), [0, .4, .5, .6, .7, 1.0]))
        pc = wp.groupby("p_bucket", observed=True).agg(n=("id", "count"), mean_p_up=("p_up", "mean"),
                                                       beat_rate=("beat", "mean")).round(2)
        lines += ["## p_up calibration (closed): stated chance of beating the benchmark vs how often it did", "",
                  "If beat_rate sits well below mean_p_up in the high buckets, shrink p_up toward the base rate.", "",
                  md_table(pc.reset_index().astype(str)), ""]
        th = with_p[with_p["theme"].notna()] if "theme" in with_p else with_p.iloc[0:0]
        if len(th):
            bt = th.groupby("theme").agg(n=("id", "count"), beat_rate=("beat", "mean"),
                                         avg_excess=("excess_pct", "mean")).round(2).reset_index()
            lines += ["## Watchlist themes (closed calls)", "", md_table(bt), ""]
    recent = df.tail(15) if not df.empty else df
    if len(recent):
        lines += ["## Latest decisions", "", md_table(recent), ""]
    (JOURNAL / "scorecard_summary.md").write_text("\n".join(lines), encoding="utf-8")
    write_json(JOURNAL / "scorecard_summary.json", summary)
    log.info("scorecard: %s", summary)
    return summary


if __name__ == "__main__":
    main()
