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
- `journal/scorecard_summary.md`, `journal/signal_health.md`, and the 2 newest files in `journal/reflections/`
- `portfolio/holdings.yaml`, `config/risk_rules.yaml`, `config/target.yaml`

If the fact sheet says `Data ready: **False**`, write a `## Data gap` digest naming what's missing. Make no
buy/add/trim/sell calls, then go to step 5.

## 3. Decide
Start from the script's view, then judge it. The fact sheet gives you, in this order: the **market regime**,
the **rules-only calls** (core/satellite target weights turned into add/hold/trim/sell/buy), and per fund a
**composite** signal (0-100, higher is better), a **crowded** flag and a **cluster**.

- Read the regime first. In `risk-off`, new buys need unusually strong evidence; prefer the core sleeve.
- Rank every holding on composite, trend (r_4w, r_12w, trend ranks, above_ma200), risk (max_dd_52w, vol),
  flows (shares_chg_5d_pct and premium for ETFs) and theme news. Pick the **3 most promising** held products.
- For each of the three, the rules-only call is the default. Agree with it, or override it only for a named
  reason the script can't see (a policy event, news, a data problem in the fact sheet). An override is logged
  with `"override": true, "override_reason": "..."`; the scorecard grades overrides separately, so only
  override when you would bet on it. Flag any other holding with a serious red flag in one line.
- Never rank on raw recent return. In China last week's spike tends to reverse, and lottery-like jumps and
  turnover surges come before weak returns: a `crowded` fund is a hold or trim, never an add or buy.
- For new picks, choose 1-3 from the rules-only buys, `candidates.csv` or the theme ETFs. Use `buy` only with
  confidence at or above the floor in the risk rules; otherwise `watch`. Never buy two funds from the same
  cluster: they are one bet. Prefer picks whose cluster the portfolio doesn't already hold.
- Read last week's reflection, the scorecard (including how the rules-only baseline and your overrides did)
  and signal health. Don't repeat mistakes they name.
- Log every call:
  `PYTHONPATH=src python3 -m cfa.journal add --json '{"code":"510300","name":"...","action":"hold","confidence":0.6,"horizon_weeks":4,"target_weight_pct":20,"thesis":"...","falsifiers":"...","data_asof":"<asof>"}'`
  Add `"override": true, "override_reason": "..."` when a holding's call differs from its rules-only call.

## 4. Write `weekly/$WEEK/digest.md`
Use these sections, in this order:
- `## Summary`: 3–5 lines, starting with the regime label, plus a one-line portfolio vs target vs benchmark
  comparison taken from the scorecard.
- `## Holdings: top 3`: per product: code and name, the call, the rules-only call and whether you overrode it
  (and why), confidence, horizon, 2–3 evidence bullets using numbers from the fact sheet, and the falsifier.
- `## New picks`: per pick: code and name, buy or watch, its cluster, why now, how it fits the portfolio, the
  falsifier.
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
