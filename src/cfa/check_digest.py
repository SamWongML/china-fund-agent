"""Gate for the weekly digest. Run by the Stop hook while state/.digest_in_progress exists.

Rejects the digest when: a required section is missing; a decimal percentage in it is not found in
weekly/<week>/inputs.json; a pick is outside the candidate list or theme ETFs; this week's journal entries
break config/risk_rules.yaml; or old journal lines were changed.

    python -m cfa.check_digest [--week 2026-W42]     # prints problems, exit 1 on failure
    python -m cfa.check_digest --hook                 # Stop-hook mode: exit 2 so Claude keeps working
"""
from __future__ import annotations

import argparse
import json
import re
import sys

from . import journal
from .common import STATE, WEEKLY, iso_week_label, load_holdings, read_json, today_hkt

MARKER = STATE / ".digest_in_progress"
SECTIONS = ["## Summary", "## Holdings: top 3", "## New picks", "## Risks and what would change my mind",
            "## Data notes"]
ACT = {"buy", "add", "trim", "sell"}
PCT = re.compile(r"(?<![\w.])([+-]?\d+\.\d+)\s*%")


def numbers_in(obj, acc: set[float]) -> set[float]:
    if isinstance(obj, dict):
        for v in obj.values():
            numbers_in(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            numbers_in(v, acc)
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        acc.add(round(float(obj), 2))
    return acc


def check(week: str) -> list[str]:
    errs: list[str] = []
    wdir = WEEKLY / week
    digest_p, inputs_p = wdir / "digest.md", wdir / "inputs.json"
    if not inputs_p.exists():
        return [f"{inputs_p} missing: run `make weekly-build` first"]
    if not digest_p.exists():
        return [f"{digest_p} not written yet"]
    inputs = read_json(inputs_p)
    text = digest_p.read_text(encoding="utf-8")
    errs += journal.verify()

    if not inputs.get("ready"):
        if "## Data gap" not in text:
            errs.append("inputs.json says data is not ready: the digest must contain a '## Data gap' section "
                        "and no buy/sell advice")
        if any(r.get("week") == week and r.get("action") in ACT for r in journal.read_all()):
            errs.append("data not ready but this week's journal has buy/add/trim/sell entries")
        return errs

    for s in SECTIONS:
        if s not in text:
            errs.append(f"missing section '{s}'")

    known = numbers_in(inputs, set())
    for m in PCT.finditer(text):
        v = float(m.group(1))
        if not any(abs(abs(v) - abs(k)) <= 0.051 for k in known):
            errs.append(f"number {m.group(0)} is not in inputs.json; copy figures exactly or remove them")

    rules = inputs.get("risk_rules") or {}
    held = {h["code"]: h for h in load_holdings()}
    allowed_new = {c["code"] for c in inputs.get("candidates") or []} | {t["code"] for t in inputs.get("themes") or []}
    recs = [r for r in journal.read_all() if r.get("week") == week]
    if held and not any(r["code"] in held for r in recs):
        errs.append("no journal entries for holdings this week (log each top-3 holding call with `python -m cfa.journal add`)")
    acts = [r for r in recs if r["action"] in ACT]
    if len(acts) > rules.get("max_actions_per_week", 3):
        errs.append(f"{len(acts)} buy/add/trim/sell calls > max_actions_per_week")
    buys = [r for r in recs if r["action"] == "buy"]
    if len(buys) > rules.get("max_new_buys_per_week", 2):
        errs.append(f"{len(buys)} new buys > max_new_buys_per_week")
    for r in recs:
        tag = f"{r['code']} {r['action']}"
        if r["code"] not in held and r["action"] in {"buy", "watch"} and r["code"] not in allowed_new:
            errs.append(f"{tag}: new pick is not in candidates.csv or the theme ETFs")
        if r["action"] in ACT and float(r["confidence"]) < rules.get("min_confidence_to_act", 0.6):
            errs.append(f"{tag}: confidence {r['confidence']} below min_confidence_to_act; use hold/watch")
        if r["horizon_weeks"] < rules.get("min_horizon_weeks", 2):
            errs.append(f"{tag}: horizon below min_horizon_weeks")
        tw = r.get("target_weight_pct")
        if tw is not None and float(tw) > rules.get("max_single_fund_weight_pct", 25):
            errs.append(f"{tag}: target_weight_pct {tw} above max_single_fund_weight_pct")
        if r["action"] in {"sell", "trim"} and r["code"] in held:
            hrow = next((h for h in inputs.get("holdings") or [] if h["code"] == r["code"]), {})
            if hrow.get("kind") == "open" and hrow.get("days_held") is not None \
                    and hrow["days_held"] < rules.get("short_hold_days_block_sell", 7):
                errs.append(f"{tag}: held {hrow['days_held']} days; short-holding redemption penalty applies")
        if r["code"] not in text:
            errs.append(f"{tag}: logged in the journal but not mentioned in the digest")
    return errs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--week")
    ap.add_argument("--hook", action="store_true")
    args = ap.parse_args()
    attempts_p = STATE / ".digest_attempts"
    if args.hook:
        try:
            json.load(sys.stdin)
        except Exception:
            pass
        if not MARKER.exists():
            return 0
        week = MARKER.read_text(encoding="utf-8").strip() or iso_week_label(today_hkt())
    else:
        week = args.week or iso_week_label(today_hkt())
    errs = check(week)
    if errs:
        msg = "Weekly digest check failed. Fix these, then finish:\n- " + "\n- ".join(errs)
        if args.hook:
            n = int(attempts_p.read_text() or 0) + 1 if attempts_p.exists() else 1
            attempts_p.write_text(str(n))
            if n >= 4:  # don't trap the agent forever: record the failure and let it stop
                (WEEKLY / week / "CHECK_FAILED.md").write_text(msg + "\n", encoding="utf-8")
                MARKER.unlink(missing_ok=True)
                attempts_p.unlink(missing_ok=True)
                return 0
        print(msg, file=sys.stderr)
        return 2 if args.hook else 1
    attempts_p.unlink(missing_ok=True)
    if args.hook:
        MARKER.unlink(missing_ok=True)
    print(f"digest {week}: all checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
