#!/usr/bin/env bash
# Commit generated files and push to main, rebasing over concurrent bot commits.
set -euo pipefail
msg="${1:-data update}"
git config user.name "china-fund-agent bot"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
git add -A data state news weekly journal reports 2>/dev/null || true
if git diff --cached --quiet; then echo "nothing to commit"; exit 0; fi
git commit -q -m "$msg"
for i in 1 2 3 4 5; do
  if git pull -q --rebase origin main && git push -q origin HEAD:main; then echo "pushed"; exit 0; fi
  sleep $((i * 5))
done
echo "push failed" >&2; exit 1
