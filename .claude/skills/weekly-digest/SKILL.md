---
name: weekly-digest
description: Sunday advisory. Give buy/add/hold/trim/sell calls on the 3 most promising holdings and curate new picks from the pre-built weekly inputs. Use for the scheduled Sunday run.
---

# Weekly digest (Sunday, HKT)

## 1. Orient
- `git pull -q origin main`, then `pip install -q pyyaml pandas` if they're missing.
- `WEEK=$(TZ=Asia/Hong_Kong date +%G-W%V)`. If `weekly/$WEEK/inputs.json` doesn't exist, the Actions build
  didn't run. Write `weekly/$WEEK/digest.md` with only a `## Data gap` section explaining that, then commit,
  push and stop.
- `echo $WEEK > state/.digest_in_progress`. This arms the Stop hook, which runs `cfa.check_digest`.

## 2. Read, and only these files
- `weekly/$WEEK/factsheets.md`, `weekly/$WEEK/news_rollup.md`, plus the daily digests it lists
- `journal/scorecard_summary.md` and the 2 newest files in `journal/reflections/`
- `portfolio/holdings.yaml`, `config/risk_rules.yaml`, `config/target.yaml`

If the fact sheet says `Data ready: **False**`, write a `## Data gap` digest naming what's missing. Make no
buy/add/trim/sell calls, then go to step 5.

## 3. Decide
- Rank every holding on trend (r_4w, r_12w, above_ma20/60), risk (max_dd_52w, vol), flows (shares_chg_5d_pct
  and premium for ETFs), and theme news. Pick the **3 most promising** held products.
- For each of the three, choose one call: `add`, `hold`, `trim` or `sell`. Hold is the default, and you need
  evidence to move off it. Flag any other holding with a serious red flag in one line.
- For new picks, choose 1–3 from `candidates.csv` or the theme ETFs. Use `buy` only with confidence ≥ the
  floor in the risk rules; otherwise use `watch`. Prefer picks that diversify the current themes. Treat
  `chase_warning` as a reason for caution.
- Read last week's reflection and scorecard. Don't repeat mistakes they name.
- Log every call:
  `PYTHONPATH=src python3 -m cfa.journal add --json '{"code":"510300","name":"...","action":"hold","confidence":0.6,"horizon_weeks":4,"target_weight_pct":20,"thesis":"...","falsifiers":"...","data_asof":"<asof>"}'`

## 4. Write `weekly/$WEEK/digest.md`
Use these sections, in this order:
- `## Summary`: 3–5 lines, plus a one-line portfolio vs target vs benchmark comparison taken from the scorecard.
- `## Holdings: top 3`: per product: code and name, the call, confidence, horizon, 2–3 evidence bullets
  using numbers from the fact sheet, and the falsifier.
- `## New picks`: per pick: code and name, buy or watch, why now, how it fits the portfolio, the falsifier.
- `## Risks and what would change my mind`
- `## Data notes`: the as-of date, stale or missing sources, anything that weakens the call.

Copy every percentage exactly from the inputs, and don't do arithmetic. End with the line: "Research signals
from public data, not financial advice."

## 5. Reflect, check, ship
- Write `journal/reflections/$WEEK.md` in 15 lines or fewer: what the scorecard says about past calls, what to
  do differently, and any proposed rule change written as a suggestion for the user. Never edit the rules.
- `cp weekly/$WEEK/digest.md reports/latest.md`
- `PYTHONPATH=src python3 -m cfa.check_digest --week $WEEK`, and fix everything it reports.
- `git add weekly reports journal state && git commit -m "weekly digest $WEEK" && git push origin HEAD:main`
