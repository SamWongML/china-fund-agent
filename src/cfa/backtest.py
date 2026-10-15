"""Walk-forward test of every signal in signals.py over the stored fund histories.

Each week (last trading day), funds are ranked on each signal using only data up to that day, and the rank
is compared with the next 4 and 12 weeks' returns. A signal is kept live only if the evidence holds:
positive mean information coefficient (IC) with t > t_min, the same sign in at least two of three
subperiods, and a positive top-third spread after costs. A positive but not yet significant signal keeps
half its weight; one with a negative IC (or inconsistent sign across subperiods) gets none. Signals without
enough history keep their literature prior. Results go to journal/signal_health.md and .json.

    python -m cfa.backtest
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import signals
from .common import JOURNAL, load_universe, log, md_table, write_json

# Configured weight is multiplied by this: proven signals count fully, a positive but not yet significant
# one counts half, a literature prior without enough local history counts fully, contrary evidence counts zero.
STATUS_WEIGHT = {"accepted": 1.0, "unproven": 0.5, "insufficient": 1.0, "rejected": 0.0}
PERIODS = [("2016-01-01", "2019-12-31"), ("2020-01-01", "2022-12-31"), ("2023-01-01", "2099-12-31")]


def universe_codes() -> list[str]:
    uni = load_universe()
    codes = [str(c).zfill(6) for c in uni.get("research_etfs") or []]
    for theme in (uni.get("themes") or {}).values():
        codes += [str(c).zfill(6) for c in theme.get("etfs") or []]
    codes += [str(c).zfill(6) for c in (uni.get("portfolio") or {}).get("core") or []]
    return list(dict.fromkeys(codes))


def week_ends(index: pd.DatetimeIndex) -> pd.DatetimeIndex:
    s = pd.Series(index, index=index)
    return pd.DatetimeIndex(s.groupby(index.to_period("W")).max().values)


def _ic_rows(feat: pd.DataFrame, fwd: pd.DataFrame, dates, min_n: int) -> pd.Series:
    out = {}
    for d in dates:
        a, b = feat.loc[d], fwd.loc[d]
        ok = a.notna() & b.notna()
        if ok.sum() >= min_n:
            out[d] = a[ok].rank().corr(b[ok].rank())
    return pd.Series(list(out.values()), index=pd.DatetimeIndex(list(out.keys())), dtype=float)


def _spread(feat: pd.DataFrame, fwd: pd.DataFrame, dates, min_n: int, cost: float) -> tuple[float | None, int]:
    """Mean 4-week return of the top third minus the equal-weight average, non-overlapping, after costs."""
    vals, prev = [], set()
    for d in dates:
        a, b = feat.loc[d], fwd.loc[d]
        ok = a.notna() & b.notna()
        if ok.sum() < min_n:
            continue
        top = set(a[ok].sort_values(ascending=False).index[: max(1, ok.sum() // 3)])
        churn = len(top - prev) / len(top) if prev else 1.0
        vals.append(b[ok][list(top)].mean() - b[ok].mean() - 2 * cost * churn)
        prev = top
    return (float(np.mean(vals)) if vals else None), len(vals)


def run(codes: list[str] | None = None) -> dict:
    cfg = signals.cfg().get("backtest") or {}
    min_n = int(cfg.get("min_funds", 8))
    min_weeks = int(cfg.get("min_weeks", 150))
    t_min = float(cfg.get("t_min", 2.0))
    cost = float(cfg.get("cost_per_trade_pct", 0.1)) / 100
    p, t = signals.panel(codes or universe_codes())
    if p.empty or p.shape[1] < min_n:
        return {"ok": False, "reason": f"only {p.shape[1]} funds with history", "live": None, "weight_mult": None,
                "signals": {}}
    p = p[p.index >= "2014-01-01"]
    t = t.reindex(p.index)
    f = signals.features(p, t)
    filled = p.ffill(limit=5)
    fwd4 = filled.shift(-20) / filled - 1
    fwd12 = filled.shift(-60) / filled - 1
    weeks = week_ends(p.index)
    weeks = weeks[weeks >= "2016-01-01"]
    rows, mult = {}, {}
    for name in signals.SIGNALS:
        feat = f[name]
        ic4 = _ic_rows(feat, fwd4, weeks[:-4], min_n)
        ic12 = _ic_rows(feat, fwd12, weeks[:-12], min_n)
        n = len(ic4)
        # Weekly ICs on 4-week returns overlap, so count one independent observation per 4 weeks.
        t4 = float(ic4.mean() / ic4.std() * np.sqrt(n / 4)) if n > 8 and ic4.std() > 0 else None
        subs = []
        for a, b in PERIODS:
            s = ic4[(ic4.index >= a) & (ic4.index <= b)]
            subs.append(round(float(s.mean()), 3) if len(s) >= 26 else None)
        spread, n_sp = _spread(feat, fwd4, weeks[:-4][::4], min_n, cost)
        same_sign = sum(1 for s in subs if s is not None and ic4.mean() and np.sign(s) == np.sign(ic4.mean()))
        if n < min_weeks:
            status = "insufficient"
        elif not ic4.mean() > 0 or same_sign < 2:
            status = "rejected"
        elif t4 is not None and t4 >= t_min and (spread or 0) > 0:
            status = "accepted"
        else:
            status = "unproven"
        if name != "legacy_screen":
            mult[name] = STATUS_WEIGHT[status]
        rows[name] = {"status": status, "weeks": n, "ic_4w": round(float(ic4.mean()), 3) if n else None,
                      "t_4w": round(t4, 2) if t4 is not None else None,
                      "ic_12w": round(float(ic12.mean()), 3) if len(ic12) else None,
                      "ic_2016_19": subs[0], "ic_2020_22": subs[1], "ic_2023_now": subs[2],
                      "top_third_spread_4w_pct": round(spread * 100, 2) if spread is not None else None,
                      "spread_periods": n_sp}
    # Does the regime idea hold? Mean next-4-week CSI 300 return by market breadth (share above 200-day MA).
    regime_check = {}
    idx = signals._index("sh000300")
    if idx is not None:
        breadth = (f["ma200_gap"] > 0).where(f["ma200_gap"].notna()).mean(axis=1)
        fwd_idx = (idx.shift(-20) / idx - 1).reindex(weeks[:-4])
        b = breadth.reindex(weeks[:-4])
        ok = fwd_idx.notna() & b.notna() & (f["ma200_gap"].notna().sum(axis=1).reindex(weeks[:-4]) >= min_n)
        for lab, m in (("breadth_above_half", b[ok] > 0.5), ("breadth_below_half", b[ok] <= 0.5)):
            regime_check[lab] = {"weeks": int(m.sum()),
                                 "csi300_next_4w_pct": round(float(fwd_idx[ok][m].mean() * 100), 2) if m.any() else None}
    result = {"ok": True, "funds": int(p.shape[1]), "first_week": str(weeks[0].date()) if len(weeks) else None,
              "last_week": str(weeks[-1].date()) if len(weeks) else None,
              "live": sorted(k for k, v in mult.items() if v > 0), "weight_mult": mult, "signals": rows,
              "regime_check": regime_check}
    write(result)
    return result


def write(res: dict) -> None:
    JOURNAL.mkdir(parents=True, exist_ok=True)
    write_json(JOURNAL / "signal_health.json", res)
    df = pd.DataFrame([{"signal": k, **v} for k, v in res["signals"].items()])
    lines = ["# Signal health (walk-forward backtest)", "",
             f"{res['funds']} funds, weekly from {res['first_week']} to {res['last_week']}. IC = rank correlation "
             "between a signal and the next 4 (or 12) weeks' returns across funds; t counts one independent "
             "observation per 4 weeks. Spread = top third minus average, next 4 weeks, after costs.", "",
             "Accepted (full weight) = positive IC with t above the floor, same sign in 2 of 3 subperiods, positive "
             "spread. Unproven (half weight) = positive and consistent but not yet significant. Insufficient (full "
             "weight) = too little history, literature prior kept. Rejected (no weight) = negative or inconsistent IC.",
             "",
             md_table(df), "",
             "Signal meanings: " + "; ".join(f"`{k}` {v}" for k, v in signals.SIGNALS.items()), ""]
    if res.get("regime_check"):
        lines += ["## Regime check (CSI 300, next 4 weeks)", "",
                  md_table(pd.DataFrame([{"state": k, **v} for k, v in res["regime_check"].items()])), ""]
    (JOURNAL / "signal_health.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    res = run()
    log.info("backtest: %s", {k: v["status"] for k, v in res.get("signals", {}).items()} or res.get("reason"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
