"""Core/satellite target weights and the rules-only calls the advisor is measured against.

Core: steady sleeves (dividend, broad index, government bonds, gold), weighted by inverse volatility so
each contributes similar risk. Satellite: the best-ranked sector ETFs by composite signal, one per
correlation cluster, not crowded, above their 200-day average, and only outside a risk-off regime.
Every weight is capped at max_single_fund_weight_pct from config/risk_rules.yaml.

Rules-only calls are written to journal/rules_baseline.jsonl (script-owned, one set per week) and graded by
the scorecard exactly like the advisor's own calls.
"""
from __future__ import annotations

import datetime as dt
import json

import numpy as np
import pandas as pd

from .common import CONFIG, JOURNAL, load_universe, load_yaml

BASELINE = JOURNAL / "rules_baseline.jsonl"


def cfg() -> dict:
    return load_universe().get("portfolio") or {}


def _cap_weights(raw: dict[str, float], total: float, cap: float) -> dict[str, float]:
    """Scale raw positive scores to sum to total, capping each at cap and redistributing the excess."""
    w = {k: v for k, v in raw.items() if v > 0}
    out: dict[str, float] = {}
    left = total
    while w and left > 1e-9:
        s = sum(w.values())
        trial = {k: left * v / s for k, v in w.items()}
        over = {k for k, v in trial.items() if v > cap}
        if not over:
            out.update(trial)
            left = 0
            break
        for k in over:
            out[k] = cap
            left -= cap
            w.pop(k)
    return {k: round(v, 1) for k, v in out.items()}


def targets(sig: pd.DataFrame, regime_label: str) -> dict:
    """sig: signals.snapshot rows (index = code). Returns {core, satellite, unallocated_pct, notes}."""
    c = cfg()
    rules = load_yaml(CONFIG / "risk_rules.yaml")
    cap = float(rules.get("max_single_fund_weight_pct", 25))
    core_codes = [str(x).zfill(6) for x in c.get("core") or []]
    core_pct = float(c.get("core_pct", 70))
    sat_pct = float(c.get("satellite_pct", 30))
    min_comp = float(c.get("satellite_min_composite", 60))
    slots = int(c.get("satellite_slots", 3))
    notes = []

    def vol(code):
        v = sig.at[code, "vol60_pct"] if code in sig.index else np.nan
        return max(float(v), 2.0) if pd.notna(v) else np.nan

    inv = {k: 1 / vol(k) for k in core_codes if pd.notna(vol(k))}
    missing = [k for k in core_codes if k not in inv]
    if missing:
        notes.append(f"core funds without history: {', '.join(missing)}")
    core = _cap_weights(inv, core_pct, cap)

    sat: dict[str, float] = {}
    picks: list[str] = []
    if regime_label == "risk-off":
        notes.append("risk-off regime: satellite sleeve left unallocated (hold bonds or cash)")
    else:
        pool = sig[~sig.index.isin(core_codes)].copy()
        pool = pool[(pool["composite"] >= min_comp) & pool["above_ma200"].fillna(False) & (pool["crowded"] == "")]
        seen = {sig.at[k, "cluster"] for k in core_codes if k in sig.index}   # don't double up on a core bet
        for code, row in pool.sort_values("composite", ascending=False).iterrows():
            if row["cluster"] in seen:
                continue
            seen.add(row["cluster"])
            picks.append(code)
            if len(picks) >= slots:
                break
        # Each slot is capped at its share of the sleeve, so one passing fund never takes the whole sleeve.
        slot_cap = min(cap, sat_pct / max(slots, 1) * 1.5)
        sat = _cap_weights({k: 1 / vol(k) for k in picks if pd.notna(vol(k))}, sat_pct, slot_cap)
        if len(picks) < slots:
            notes.append(f"only {len(picks)} satellite funds pass the filters")
    unalloc = round(100 - sum(core.values()) - sum(sat.values()), 1)
    return {"core": core, "satellite": sat, "unallocated_pct": unalloc, "notes": notes}


def rule_calls(tg: dict, holdings: list[dict], sig: pd.DataFrame, cash_cny: float = 0.0) -> list[dict]:
    """Mechanical call per holding plus a buy for each target fund not held. Hold is the default."""
    band = float(cfg().get("drift_band_pct", 5))
    weights = {**tg["core"], **tg["satellite"]}
    values = {h["code"]: float(h.get("value_cny") or 0) for h in holdings}
    total = sum(values.values()) + float(cash_cny or 0)
    calls = []
    for h in holdings:
        code = h["code"]
        cur = round(values[code] / total * 100, 1) if total > 0 else None
        tgt = weights.get(code, 0.0)
        row = sig.loc[code] if code in sig.index else None
        action, why = "hold", "within band"
        if cur is not None and code in weights:
            if cur < tgt - band:
                action, why = "add", f"below target weight by more than {band:g} points"
            elif cur > tgt + band:
                action, why = "trim", f"above target weight by more than {band:g} points"
        elif row is not None and code not in weights:
            if not row["above_ma200"] and (row.get("trend_26w_rank") or 100) <= 33:
                action, why = "sell", "not a target, below 200-day average, bottom-third 26-week trend"
            elif row["crowded"]:
                action, why = "trim", f"not a target and crowded ({row['crowded']})"
            else:
                why = "not a target, but no exit signal"
        calls.append({"code": code, "action": action, "current_weight_pct": cur, "target_weight_pct": tgt,
                      "reason": why})
    held = {h["code"] for h in holdings}
    for code, w in weights.items():
        if code not in held:
            calls.append({"code": code, "action": "buy", "current_weight_pct": 0.0, "target_weight_pct": w,
                          "reason": "core sleeve" if code in tg["core"] else "top satellite pick"})
    return calls


def write_baseline(calls: list[dict], week: str, asof: dt.date, horizon_weeks: int = 4) -> None:
    """Replace this week's rules-only calls (reruns of the build must not duplicate them)."""
    BASELINE.parent.mkdir(parents=True, exist_ok=True)
    old = [json.loads(x) for x in BASELINE.read_text(encoding="utf-8").splitlines() if x.strip()] \
        if BASELINE.exists() else []
    keep = [r for r in old if r.get("week") != week]
    ts = f"{asof.isoformat()}T16:00:00+08:00"
    new = [{"id": f"rules-{week}-{c['code']}", "ts": ts, "week": week, "source": "rules", "code": c["code"],
            "action": c["action"], "confidence": 0.6, "horizon_weeks": horizon_weeks,
            "target_weight_pct": c["target_weight_pct"], "held": c["action"] != "buy"} for c in calls]
    BASELINE.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in keep + new), encoding="utf-8")


def read_baseline() -> list[dict]:
    if not BASELINE.exists():
        return []
    return [json.loads(x) for x in BASELINE.read_text(encoding="utf-8").splitlines() if x.strip()]
