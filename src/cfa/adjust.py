"""Turn raw exchange closes into a total-return price series.

Raw Sina closes show fund share splits and consolidations (份额拆分/折算) as fake crashes or jumps, and they
drop cash dividends. `adjust` fixes both: the adjusted price equals the raw close times the product of every
later event's factor, so the latest adjusted price equals the market price and every daily return is a
total return.

Events come from data/ref/fund_actions.csv (Eastmoney split and dividend tables, refreshed by
collect_funds). A one-day move no fund can make (beyond any daily price limit) that no listed split explains
is treated as an unlisted split, snapped to a round ratio when one is close.
"""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd

from .common import REF, log, retry

ACTIONS_PATH = REF / "fund_actions.csv"
# Daily limits are ±10% (main board) and ±20% (ChiNext/STAR); nothing inside this band can be a split.
JUMP_LO, JUMP_HI = 0.75, 1.30
ROUND_RATIOS = sorted({float(k) for k in (2, 3, 4, 5, 10, 20)} | {1 / k for k in (2, 3, 4, 5, 10, 20)})
FIRST_YEAR = 2012
BACKFILL_YEARS_PER_RUN = 4


def load_actions(code: str | None = None) -> pd.DataFrame:
    if not ACTIONS_PATH.exists():
        return pd.DataFrame(columns=["code", "date", "kind", "value"])
    df = pd.read_csv(ACTIONS_PATH, dtype={"code": str, "date": str})
    return df[df["code"] == code] if code else df


def _snap(ratio: float, tol: float = 0.05) -> float | None:
    best = min(ROUND_RATIOS, key=lambda r: abs(np.log(ratio / r)))
    return best if abs(np.log(ratio / best)) <= np.log(1 + tol) else None


def adjust(dates: list[str], raw: np.ndarray, actions: pd.DataFrame | None = None) -> tuple[np.ndarray, list[dict]]:
    """Return (adjusted prices, applied events). `factor[i]` scales every price before index i."""
    raw = np.asarray(raw, dtype=float)
    n = len(raw)
    if n < 2:
        return raw.copy(), []
    d = pd.to_datetime(pd.Series(dates)).dt.date.to_numpy()
    factor = np.ones(n)
    handled = np.zeros(n, dtype=bool)
    ratio = np.r_[1.0, raw[1:] / raw[:-1]]
    events: list[dict] = []
    acts = actions if actions is not None else pd.DataFrame(columns=["date", "kind", "value"])

    for a in acts[acts["kind"] == "split"].itertuples():
        k = float(a.value)
        if not k > 0 or abs(np.log(k)) < 1e-6:
            continue
        when = dt.date.fromisoformat(str(a.date)[:10])
        win = [i for i in range(1, n) if when - dt.timedelta(days=5) <= d[i] <= when + dt.timedelta(days=10)
               and not handled[i]]
        # The table's ratio is units after per unit before; accept either direction, the price confirms it.
        best = None
        for i in win:
            for target in (1 / k, k):
                err = abs(np.log(ratio[i] / target))
                if err < np.log(1.15) and (best is None or err < best[0]):
                    best = (err, i, target)
        if best:
            _, i, target = best
            factor[i] *= target
            handled[i] = True
            events.append({"date": str(d[i]), "kind": "split", "factor": round(target, 6), "source": "listed"})

    for i in range(1, n):
        if handled[i] or JUMP_LO <= ratio[i] <= JUMP_HI:
            continue
        snapped = _snap(ratio[i])
        factor[i] *= snapped or ratio[i]
        handled[i] = True
        events.append({"date": str(d[i]), "kind": "split", "factor": round(float(snapped or ratio[i]), 6),
                       "source": "detected"})

    for a in acts[acts["kind"] == "div"].itertuples():
        cash = float(a.value)
        when = dt.date.fromisoformat(str(a.date)[:10])
        idx = np.searchsorted(d, when)
        if idx <= 0 or idx >= n or not 0 < cash < raw[idx - 1]:
            continue
        f = (raw[idx - 1] - cash) / raw[idx - 1]
        factor[idx] *= f
        events.append({"date": str(d[idx]), "kind": "div", "factor": round(f, 6), "cash": cash})

    # multiplier[j] = product of factor[i] for i > j
    mult = np.r_[np.cumprod(factor[::-1])[::-1][1:], 1.0]
    return raw * mult, sorted(events, key=lambda e: e["date"])


def total_return_nav(nav: np.ndarray, growth_pct: np.ndarray) -> np.ndarray:
    """Open-end funds: chain the published daily growth rate (日增长率, which includes dividends and splits)
    and scale so the last value equals the last unit NAV. Missing rates fall back to the NAV ratio."""
    nav = np.asarray(nav, dtype=float)
    g = np.asarray(growth_pct, dtype=float) / 100
    step = np.r_[1.0, nav[1:] / nav[:-1]]
    step = np.where(np.isnan(g), step, 1 + g)
    step[0] = 1.0
    tr = np.cumprod(step)
    return tr / tr[-1] * nav[-1]


# ---------- reference table ----------

def _fetch_year(year: int) -> pd.DataFrame:
    import akshare as ak
    frames = []
    try:
        cf = retry(lambda: ak.fund_cf_em(year=str(year)), attempts=2, name=f"fund_cf_em {year}")
        if len(cf):
            frames.append(pd.DataFrame({"code": cf["基金代码"].astype(str).str.zfill(6),
                                        "date": pd.to_datetime(cf["拆分折算日"]).dt.date.astype(str),
                                        "kind": "split", "value": pd.to_numeric(cf["拆分折算"], errors="coerce")}))
    except Exception as e:
        log.warning("split table %s unavailable: %s", year, e)
    try:
        fh = retry(lambda: ak.fund_fh_em(year=str(year)), attempts=2, name=f"fund_fh_em {year}")
        if len(fh):
            frames.append(pd.DataFrame({"code": fh["基金代码"].astype(str).str.zfill(6),
                                        "date": pd.to_datetime(fh["除息日期"]).dt.date.astype(str),
                                        "kind": "div", "value": pd.to_numeric(fh["分红"], errors="coerce")}))
    except Exception as e:
        log.warning("dividend table %s unavailable: %s", year, e)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def refresh_actions(today: dt.date) -> dict:
    """Backfill missing years (newest first, a few per run to keep the daily job short); afterwards refresh
    this year and last year on Mondays."""
    old = load_actions()
    have = set(pd.to_datetime(old["date"]).dt.year) if len(old) else set()
    years = sorted((y for y in range(FIRST_YEAR, today.year + 1) if y not in have), reverse=True)[:BACKFILL_YEARS_PER_RUN]
    if today.weekday() == 0 or not len(old):
        years += [today.year - 1, today.year]
    years = sorted(set(years))
    if not years:
        return {"ok": True, "rows": len(old), "years": []}
    new = [df for y in years if len(df := _fetch_year(y))]
    if not new:
        return {"ok": False, "rows": len(old), "years": years}
    new_df = pd.concat(new, ignore_index=True)
    fetched_years = set(pd.to_datetime(new_df["date"]).dt.year)
    keep = old[~pd.to_datetime(old["date"]).dt.year.isin(fetched_years)] if len(old) else old
    df = pd.concat([keep, new_df], ignore_index=True).dropna(subset=["value"])
    df = df.drop_duplicates().sort_values(["code", "date", "kind"])
    ACTIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(ACTIONS_PATH, index=False)
    return {"ok": True, "rows": len(df), "years": years}
