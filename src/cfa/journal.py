"""Append-only decision journal (journal/decisions.jsonl).

    python -m cfa.journal add --json '{"code": "510300", "action": "hold", ...}'
    python -m cfa.journal verify          # existing lines unchanged vs git HEAD

The agent must only add decisions through `add`; Edit/Write on the file is blocked by a hook.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import uuid

from .common import JOURNAL, ROOT, iso_week_label, load_holdings, now_hkt

PATH = JOURNAL / "decisions.jsonl"
ACTIONS = {"buy", "add", "hold", "trim", "sell", "watch"}
REQUIRED = {"code", "action", "confidence", "horizon_weeks", "thesis", "falsifiers", "data_asof"}


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
    held = {h["code"] for h in load_holdings()}
    if rec.get("action") in {"hold", "trim", "sell", "add"} and code not in held:
        errs.append(f"{rec.get('action')} on {code}, which is not in portfolio/holdings.yaml")
    return errs


def read_all() -> list[dict]:
    if not PATH.exists():
        return []
    return [json.loads(x) for x in PATH.read_text(encoding="utf-8").splitlines() if x.strip()]


def add(rec: dict) -> dict:
    rec = dict(rec)
    rec["code"] = str(rec.get("code", "")).zfill(6)
    errs = validate(rec)
    if errs:
        raise ValueError("; ".join(errs))
    now = now_hkt()
    rec = {"id": uuid.uuid4().hex[:12], "ts": now.isoformat(timespec="seconds"), "week": iso_week_label(now.date()),
           "held": rec["code"] in {h["code"] for h in load_holdings()}, **rec}
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
