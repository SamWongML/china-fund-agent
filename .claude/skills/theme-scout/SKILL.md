---
name: theme-scout
description: Monthly research on promising and emerging investment fields (AI, robotics, chips...). Updates watchlist/themes.yaml, which the weekly build turns into product lists the Sunday advisor curates. Use for the monthly theme run or when the user asks to add or review a theme.
---

# Theme scout (monthly, or on request)

Goal: keep `watchlist/themes.yaml` to the few fields where China's policy support is real and the trade is not
yet crowded. You pick fields and write why. Scripts find the products and compute every number.

Evidence to keep in mind (details: the research note in `research/themes/`):
- Thematic ETFs launched after hot runs and heavy media coverage did worst afterwards (Ben-David et al.). A wave
  of new ETFs on a theme is a late, crowded signal.
- In China, firms with explicit State Council industrial-policy support earned a risk premium, which vanished
  when support was withdrawn (Sinclair & Zhang). Policy that is still being renewed is the core of a thesis.

## 1. Orient
- `git pull -q origin main`; `pip install -q pyyaml pandas pyarrow` if missing.
- `PYTHONPATH=src python3 -m cfa.themes scan` writes `weekly/<this week>/theme_scan.md` from the snapshots in the
  repo. Read it, the newest `weekly/*/themes.md`, `watchlist/themes.yaml`, the newest note in `research/themes/`,
  and the "Watchlist themes" table in `journal/scorecard_summary.md` if present.

## 2. Research
- For each active and watch-only theme: is the policy support still being renewed (new State Council or ministry
  documents, Five-Year Plan follow-ups, local pilots)? Any milestone or setback (orders, approvals, production,
  export controls)? Use web search; cite every claim with a link.
- For new fields: start from the discovery tables (busy families not watched, launch waves) and the current
  Five-Year Plan priorities. A field needs a named policy anchor to be added.
- Do not copy prices, returns or flows from the web into the watchlist. Numbers come from the build.

## 3. Decide
For each theme, keep, change stage, move between `active` and `watch-only`, or `retired` (never delete an entry;
the scorecard grades themes by id). Rules:
- Add at most 2 new themes per run. Keep at most `watch_themes.max_active` (in `config/universe.yaml`) active,
  most important first.
- `active` needs at least 3 index families with enough turnover in themes.md or the scan; otherwise `watch-only`.
- Stage `crowded` when launches in 6 months, news mentions and crowded products are all high; demote to
  `watch-only` or retire when policy support is dropped or a falsifier is hit.
- Every entry keeps: thesis, policy anchors, match/exclude name keywords (check they match the right products in
  the scan and nothing else), news keywords, falsifiers, `review_by` within 3 months.

## 4. Write and ship
- Edit `watchlist/themes.yaml`. Run `PYTHONPATH=src python3 -m cfa.themes check` and fix what it reports.
- Write `research/themes/YYYY-MM.md` (60 lines or fewer): what changed and why, one paragraph per theme added,
  removed or re-staged, with source links; then one line per unchanged theme.
- `PYTHONPATH=src python3 -m cfa.brief themes --month YYYY-MM` renders `briefs/themes.html`. Don't open it.
- `git add watchlist research/themes briefs && git commit -m "theme scout YYYY-MM" && git push origin HEAD:main`
- Reply with what changed on the watchlist in a few lines. End with: "Research signals from public data, not
  financial advice."
