"""Price-based signals for funds, built from data/history/nav/<code>.csv.

Signals follow the China evidence in research/strategy_review: index and sector trend over 3-6 months
works, last week's and last month's spikes reverse, lottery-like jumps and turnover surges precede weak
returns, and calm beats exciting. Every signal is oriented so that higher = better, then ranked to a
0-100 percentile within the set being compared.

    signals.panel(codes)            -> (prices, turnover) wide frames, one column per code
    signals.features(prices, turn)  -> {signal: wide frame}
    signals.snapshot(...)           -> one row per code at the latest date with ranks, composite, flags
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .common import HISTORY, log, load_universe

SIGNALS = {
    "trend_12w": "12-week return skipping the last week, per unit of 60-day volatility",
    "trend_26w": "26-week return skipping the last week, per unit of 60-day volatility",
    "ma200_gap": "price vs its 200-day average",
    "rev_1w": "minus last week's return (short-term reversal)",
    "rev_4w": "minus last 4 weeks' return (one-month reversal)",
    "max_20d": "minus the largest daily gain in 20 days (lottery effect)",
    "turnover_surge": "minus 5-day turnover vs its 120-day median (crowding)",
    "low_vol": "minus 60-day volatility",
    "legacy_screen": "the old candidate score: raw 1/3/6/12-month returns, for comparison only",
}
DEFAULT_WEIGHTS = {"trend_12w": 0.25, "trend_26w": 0.2, "ma200_gap": 0.1, "rev_1w": 0.1, "max_20d": 0.1,
                   "turnover_surge": 0.1, "low_vol": 0.15}


def cfg() -> dict:
    return load_universe().get("signals") or {}


def weights() -> dict[str, float]:
    return {k: float(v) for k, v in (cfg().get("weights") or DEFAULT_WEIGHTS).items()}


def load_history(code: str) -> pd.DataFrame | None:
    p = HISTORY / "nav" / f"{code}.csv"
    if not p.exists():
        return None
    h = pd.read_csv(p, dtype={"date": str})
    h["date"] = pd.to_datetime(h["date"])
    return h.drop_duplicates("date").set_index("date").sort_index()


def panel(codes: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    prices, turn = {}, {}
    for c in dict.fromkeys(codes):
        h = load_history(c)
        if h is None or len(h) < 30:
            continue
        prices[c] = h["price"].astype(float)
        if "volume" in h and h["volume"].notna().mean() > 0.8:
            raw = h["raw"] if "raw" in h and h["raw"].notna().all() else h["price"]
            turn[c] = h["volume"].astype(float) * raw.astype(float)
    p = pd.DataFrame(prices).sort_index()
    t = pd.DataFrame(turn).reindex(p.index) if turn else pd.DataFrame(index=p.index)
    return p, t


def features(p: pd.DataFrame, t: pd.DataFrame | None = None) -> dict[str, pd.DataFrame]:
    """Each value is a dates x codes frame computed only from data up to that date."""
    filled = p.ffill(limit=5)
    daily = filled.pct_change(fill_method=None)
    vol60 = np.log(filled).diff().rolling(60, min_periods=40).std() * np.sqrt(250)
    vol = vol60.clip(lower=0.02)

    def ret(n, skip=0):
        return filled.shift(skip) / filled.shift(n) - 1

    f = {
        "trend_12w": ret(60, 5) / vol,
        "trend_26w": ret(125, 5) / vol,
        "ma200_gap": filled / filled.rolling(200, min_periods=150).mean() - 1,
        "rev_1w": -ret(5),
        "rev_4w": -ret(20),
        "max_20d": -daily.rolling(20, min_periods=15).max(),
        "low_vol": -vol60,
    }
    if t is not None and not t.empty:
        surge = t.rolling(5, min_periods=3).mean() / t.rolling(120, min_periods=60).median()
        f["turnover_surge"] = -surge.reindex(columns=p.columns)
    else:
        f["turnover_surge"] = pd.DataFrame(np.nan, index=p.index, columns=p.columns)
    legacy = sum(w * ret(n).rank(axis=1, pct=True) for n, w in ((20, .2), (60, .35), (120, .25), (250, .2)))
    f["legacy_screen"] = legacy
    f["_vol60"] = vol60
    f["_r5"], f["_r20"], f["_r60"], f["_r250"] = ret(5), ret(20), ret(60), ret(250)
    f["_max1d"] = daily.rolling(20, min_periods=15).max()
    f["_surge"] = -f["turnover_surge"]
    return f


def composite(ranks: pd.DataFrame, mult: dict[str, float] | None = None) -> pd.Series:
    """Weighted mean of 0-100 percentile ranks; mult (from the backtest) scales each configured weight.
    Signals a code lacks are skipped for that code."""
    w = {k: v * (1.0 if mult is None else mult.get(k, 1.0)) for k, v in weights().items() if k in ranks}
    w = {k: v for k, v in w.items() if v > 0}
    if not w:
        return pd.Series(np.nan, index=ranks.index)
    num = sum(ranks[k].fillna(0) * v for k, v in w.items())
    den = sum(ranks[k].notna() * v for k, v in w.items())
    return (num / den.replace(0, np.nan)).round(1)


def crowded(row: pd.Series) -> list[str]:
    c = cfg().get("crowding") or {}
    why = []
    if pd.notna(row.get("r_1w_pct")) and row["r_1w_pct"] > c.get("max_1w_pct", 8):
        why.append("1-week gain")
    if pd.notna(row.get("max_1d_pct")) and row["max_1d_pct"] > c.get("max_1d_pct", 7):
        why.append("lottery-like daily jump")
    if pd.notna(row.get("turnover_x")) and row["turnover_x"] > c.get("max_turnover_x", 2.5):
        why.append("turnover surge")
    return why


def clusters(p: pd.DataFrame, order: list[str], threshold: float | None = None) -> dict[str, str]:
    """Greedy grouping by 60-day correlation of market-relative daily returns: each code joins the first higher-ranked leader
    it correlates with above the threshold, otherwise it leads its own cluster."""
    thr = threshold if threshold is not None else float(cfg().get("cluster_corr", 0.6))
    codes = [c for c in order if c in p]
    r = p[codes].ffill(limit=5).pct_change(fill_method=None).tail(60)
    # Remove the common market move first; otherwise everything clusters together in a broad sell-off.
    r = r.sub(r.mean(axis=1), axis=0)
    corr = r.corr(min_periods=40)
    leaders: list[str] = []
    out = {}
    for c in codes:
        lead = next((l for l in leaders if pd.notna(corr.at[c, l]) and corr.at[c, l] >= thr), None)
        if lead is None:
            leaders.append(c)
            lead = c
        out[c] = lead
    return out


def snapshot(p: pd.DataFrame, t: pd.DataFrame, mult: dict[str, float] | None = None) -> pd.DataFrame:
    """Latest-date signal table for every code in the panel, ranked within the panel."""
    if p.empty:
        return pd.DataFrame()
    f = features(p, t)
    last = {k: v.iloc[-1] for k, v in f.items()}
    df = pd.DataFrame({k: v for k, v in last.items() if not k.startswith("_")})
    ranks = df[[k for k in SIGNALS if k in df]].rank(pct=True) * 100
    out = pd.DataFrame(index=df.index)
    out["composite"] = composite(ranks, mult)
    for k in ("trend_12w", "trend_26w", "rev_1w", "max_20d", "turnover_surge", "low_vol"):
        out[f"{k}_rank"] = ranks[k].round(0)
    out["above_ma200"] = df["ma200_gap"] > 0
    out["ma200_gap_pct"] = (df["ma200_gap"] * 100).round(2)
    out["vol60_pct"] = (last["_vol60"] * 100).round(2)
    out["r_1w_pct"] = (last["_r5"] * 100).round(2)
    out["r_12w_pct"] = (last["_r60"] * 100).round(2)
    out["max_1d_pct"] = (last["_max1d"] * 100).round(2)
    out["turnover_x"] = last["_surge"].round(2)
    out["crowded"] = out.apply(lambda r: "; ".join(crowded(r)), axis=1)
    order = out.sort_values("composite", ascending=False).index.tolist()
    cl = clusters(p, order)
    out["cluster"] = out.index.map(lambda c: cl.get(c, c))
    out.index.name = "code"
    return out.reset_index()


# ---------- market regime ----------

def _index(sym: str) -> pd.Series | None:
    path = HISTORY / "index" / f"{sym}.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path)
    return pd.Series(df["close"].values, index=pd.to_datetime(df["date"])).sort_index()


def regime(breadth_prices: pd.DataFrame, valuation: dict | None = None) -> dict:
    """Plain risk-on / neutral / risk-off label from index trend, breadth and (when available) valuation."""
    votes, detail = [], {}
    for sym in ("sh000300", "sh000905"):
        s = _index(sym)
        if s is None or len(s) < 200:
            continue
        gap = s.iloc[-1] / s.tail(200).mean() - 1
        r12 = s.iloc[-1] / s.iloc[-61] - 1
        detail[f"{sym}_ma200_gap_pct"] = round(gap * 100, 2)
        detail[f"{sym}_r_12w_pct"] = round(r12 * 100, 2)
        votes += [gap > 0, r12 > 0]
    if not breadth_prices.empty:
        gap = breadth_prices.ffill(limit=5).iloc[-1] / breadth_prices.ffill(limit=5).tail(200).mean() - 1
        gap = gap[breadth_prices.notna().tail(200).sum() >= 150]
        if len(gap) >= 10:
            share = float((gap > 0).mean())
            detail["breadth_above_ma200_pct"] = round(share * 100, 1)
            detail["breadth_n"] = int(len(gap))
            votes.append(share > 0.5)
    if valuation and valuation.get("erp_pctile_5y") is not None:
        detail.update(valuation)
        # Cheap equities vs bonds (top 30% of the 5-year range) count for risk-on, expensive against.
        if valuation["erp_pctile_5y"] >= 70:
            votes.append(True)
        elif valuation["erp_pctile_5y"] <= 30:
            votes.append(False)
    if not votes:
        return {"label": "unknown", "score": None, "votes": 0, **detail}
    score = sum(votes) / len(votes)
    label = "risk-on" if score >= 0.7 else "risk-off" if score <= 0.3 else "neutral"
    return {"label": label, "score": round(score, 2), "votes": len(votes), **detail}


def refresh_valuation() -> dict:
    """CSI 300 earnings yield minus the 10-year CGB yield (股债性价比), with its 5-year percentile.
    Fetched on Actions and cached in data/history/macro/; returns {} when the sources are unreachable."""
    import akshare as ak

    from .common import retry
    macro = HISTORY / "macro"
    macro.mkdir(parents=True, exist_ok=True)
    try:
        pe = retry(lambda: ak.stock_index_pe_lg(symbol="沪深300"), attempts=2, name="stock_index_pe_lg")
        pe = pd.DataFrame({"date": pd.to_datetime(pe["日期"]).dt.date.astype(str), "pe_ttm": pe["滚动市盈率"]})
        pe.to_csv(macro / "csi300_pe.csv", index=False)
    except Exception as e:
        log.warning("CSI 300 PE unavailable: %s", e)
    try:
        y = retry(lambda: ak.bond_zh_us_rate(start_date="20150101"), attempts=2, name="bond_zh_us_rate")
        y = pd.DataFrame({"date": pd.to_datetime(y["日期"]).dt.date.astype(str), "cn10y": y["中国国债收益率10年"]})
        y.dropna().to_csv(macro / "cn10y.csv", index=False)
    except Exception as e:
        log.warning("CGB yields unavailable: %s", e)
    return valuation_from_cache()


def valuation_from_cache() -> dict:
    macro = HISTORY / "macro"
    if not (macro / "csi300_pe.csv").exists() or not (macro / "cn10y.csv").exists():
        return {}
    pe = pd.read_csv(macro / "csi300_pe.csv").dropna()
    y = pd.read_csv(macro / "cn10y.csv").dropna()
    df = pe.merge(y, on="date").sort_values("date")
    df = df[df["pe_ttm"] > 0]
    if len(df) < 250:
        return {}
    df["erp"] = 100 / df["pe_ttm"] - df["cn10y"]
    last5 = df[pd.to_datetime(df["date"]) >= pd.to_datetime(df["date"].iloc[-1]) - pd.DateOffset(years=5)]
    pct = float((last5["erp"] <= df["erp"].iloc[-1]).mean() * 100)
    return {"valuation_date": df["date"].iloc[-1], "csi300_pe_ttm": round(float(df["pe_ttm"].iloc[-1]), 2),
            "cn10y_pct": round(float(df["cn10y"].iloc[-1]), 2), "erp_pct": round(float(df["erp"].iloc[-1]), 2),
            "erp_pctile_5y": round(pct, 1)}
