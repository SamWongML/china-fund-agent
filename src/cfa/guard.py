"""PreToolUse hook: block agent writes to human-owned files. Exit 2 blocks the tool call."""
from __future__ import annotations

import json
import re
import sys

PROTECTED = ("portfolio/", "config/risk_rules.yaml", "config/target.yaml", "journal/decisions.jsonl")
WRITE_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
BASH_WRITE = re.compile(r"(>|\btee\b|\bsed\s+-i|\brm\b|\bmv\b|\bcp\b|\btruncate\b|git\s+(checkout|restore)\b)")


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except Exception:
        return 0
    tool = event.get("tool_name", "")
    inp = event.get("tool_input") or {}
    if tool in WRITE_TOOLS:
        path = str(inp.get("file_path") or inp.get("notebook_path") or "")
        if any(p in path for p in PROTECTED):
            print(f"{path} is human-owned. Read it, never edit it. Journal entries go through "
                  "`python -m cfa.journal add --json ...`.", file=sys.stderr)
            return 2
    if tool == "Bash":
        cmd = str(inp.get("command") or "")
        if any(p in cmd for p in PROTECTED) and BASH_WRITE.search(cmd) and "cfa.journal add" not in cmd:
            print("This command would modify a human-owned file (portfolio/, risk rules, target, or the journal).",
                  file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
