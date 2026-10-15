"""Append-only decision journal (journal/decisions.jsonl).

    python -m cfa.journal add --json '{"code": "510300", "action": "hold", "p_up": 0.55, ...}'
    python -m cfa.journal verify          # existing lines unchanged vs git HEAD

The agent must only add decisions through `add`; Edit/Write on the file is blocked by a hook.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import uuid

from .common import JOURNAL, ROOT, iso_week_label, load_holdings, load_universe, now_hkt

PATH = JOURNAL / "decisions.jsonl"
ACTIONS = {"buy", "add", "hold", "trim", "sell", "watch"}
REQUIRED = {"code", "action", "confidence", "horizon_weeks", "thesis", "falsifiers", "data_asof"}
DOWN = {"trim", "sell"}   # graded as right when the fund trails the benchmark


def advice_cfg() -> dict:
    return load_universe().get("advice") or {}


def view(action: str, p_up: float, held: bool) -> str:
    """What the user sees: Buy/Sell for holdings, Buy/Watch for everything else."""
    if not held:
        return "buy" if action == "buy" else "watch"
    if action in DOWN:
        return "sell"
    if action == "hold":
        return "buy" if p_up >= 0.5 else "sell"
    return "buy"


def normalize(rec: dict) -> dict:
    """p_up is the probability the fund beats the benchmark over the horizon. confidence (the probability the
    logged action turns out right, which the scorecard grades) is derived from it, never typed separately."""
    rec = dict(rec)
    if rec.get("p_up") is None:
        return rec
    try:
        p = round(float(rec["p_up"]), 3)
    except (TypeError, ValueError):
        return rec
    derived = round(1 - p, 3) if rec.get("action") in DOWN else p
    if "confidence" in rec and rec["confidence"] is not None:
        try:
            if abs(float(rec["confidence"]) - derived) > 0.011:
                rec["_conflict"] = derived
        except (TypeError, ValueError):
            pass
    rec["p_up"], rec["confidence"] = p, derived
    return rec


def validate(rec: dict) -> list[str]:
    errs = [f"missing {k}" for k in sorted(REQUIRED - rec.keys())]
    if rec.get("action") not in ACTIONS:
        errs.append(f"action must be one of {sorted(ACTIONS)}")
    try:
        c = float(rec.get("confidence", -1))
        if not 0 <= c <= 1:
            errs.append("confidence must be 0..1")
    except (TypeError, ValueError):
        errs.append("confidence must be a number")
    if not isinstance(rec.get("horizon_weeks"), int) or not 1 <= rec["horizon_weeks"] <= 52:
        errs.append("horizon_weeks must be an int 1..52")
    code = str(rec.get("code", ""))
    if len(code) != 6 or not code.isdigit():
        errs.append("code must be 6 digits")
    if "_conflict" in rec:
        errs.append(f"confidence must equal {rec['_conflict']} for p_up {rec.get('p_up')}; pass p_up only")
    if rec.get("p_up") is not None:
        a = advice_cfg()
        try:
            p = float(rec["p_up"])
        except (TypeError, ValueError):
            p = None
            errs.append("p_up must be a number")
        if p is not None:
            lo, hi = float(a.get("p_min", 0.15)), float(a.get("p_max", 0.85))
            if not lo <= p <= hi:
                errs.append(f"p_up must be between {lo} and {hi} (weekly fund outcomes are near coin flips)")
            if rec.get("action") in DOWN and p >= 0.5:
                errs.append(f"{rec['action']} needs p_up below 0.5 (you expect it to trail the benchmark)")
            if rec.get("action") in {"buy", "add"} and p <= 0.5:
                errs.append(f"{rec['action']} needs p_up above 0.5")
    if "theme" in rec and not str(rec.get("theme") or "").strip():
        errs.append("theme must be a watchlist theme id when given")
    if "override" in rec and not isinstance(rec["override"], bool):
        errs.append("override must be true or false")
    if rec.get("override") and not str(rec.get("override_reason") or "").strip():
        errs.append("override=true needs an override_reason (news, policy event, data issue...)")
    held = {h["code"] for h in load_holdings()}
    if rec.get("action") in {"hold", "trim", "sell", "add"} and code not in held:
        errs.append(f"{rec.get('action')} on {code}, which is not in portfolio/holdings.yaml")
    return errs


def read_all() -> list[dict]:
    if not PATH.exists():
        return []
    return [json.loads(x) for x in PATH.read_text(encoding="utf-8").splitlines() if x.strip()]


def add(rec: dict) -> dict:
    rec = normalize(rec)
    rec["code"] = str(rec.get("code", "")).zfill(6)
    errs = validate(rec)
    if errs:
        raise ValueError("; ".join(errs))
    now = now_hkt()
    held = rec["code"] in {h["code"] for h in load_holdings()}
    rec = {"id": uuid.uuid4().hex[:12], "ts": now.isoformat(timespec="seconds"), "week": iso_week_label(now.date()),
           "held": held, **rec}
    if rec.get("p_up") is not None:
        rec["view"] = view(rec["action"], rec["p_up"], held)
    PATH.parent.mkdir(parents=True, exist_ok=True)
    with PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def head_version() -> str:
    try:
        return subprocess.run(["git", "show", f"HEAD:{PATH.relative_to(ROOT)}"], cwd=ROOT, capture_output=True,
                              text=True, check=True).stdout
    except subprocess.CalledProcessError:
        return ""


def verify() -> list[str]:
    old = head_version()
    new = PATH.read_text(encoding="utf-8") if PATH.exists() else ""
    if old and not new.startswith(old):
        return ["journal/decisions.jsonl: existing lines were changed or removed (append-only)"]
    return []


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("--json", required=True)
    sub.add_parser("verify")
    args = ap.parse_args()
    if args.cmd == "add":
        try:
            print(json.dumps(add(json.loads(args.json)), ensure_ascii=False))
        except (ValueError, json.JSONDecodeError) as e:
            print(f"rejected: {e}", file=sys.stderr)
            return 2
        return 0
    errs = verify()
    for e in errs:
        print(e, file=sys.stderr)
    return 1 if errs else 0


if __name__ == "__main__":
    raise SystemExit(main())
