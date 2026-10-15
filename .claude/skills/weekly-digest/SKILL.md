---
name: weekly-digest
description: Sunday advisory. Give Buy/Sell calls with a percentage on holdings, Buy/Watch calls on new picks and on at least 3 products per watchlist theme, from the pre-built weekly inputs. Use for the scheduled Sunday run.
---

# Weekly digest (Sunday, HKT)

## 1. Orient
- `git pull -q origin main`, then `pip install -q pyyaml pandas` if they're missing.
- `WEEK=$(TZ=Asia/Hong_Kong date +%G-W%V)`. If `weekly/$WEEK/inputs.json` doesn't exist, the Actions build
  didn't run. Write `weekly/$WEEK/digest.md` with only a `## Data gap` section explaining that, then commit,
  push and stop.
- `echo $WEEK > state/.digest_in_progress`. This arms the Stop hook, which runs `cfa.check_digest`.

## 2. Read, and only these files
- `weekly/$WEEK/factsheets.md` (includes the **base rates** table), `weekly/$WEEK/themes.md`,
  `weekly/$WEEK/news_rollup.md`, plus the daily digests it lists
- `watchlist/themes.yaml` (thesis and falsifiers per theme)
- `journal/scorecard_summary.md`, `journal/signal_health.md`, and the 2 newest files in `journal/reflections/`
- `portfolio/holdings.yaml`, `config/risk_rules.yaml`, `config/target.yaml`

If the fact sheet says `Data ready: **False**`, write a `## Data gap` digest naming what's missing. Make no
buy/add/trim/sell calls, then go to step 5.

## 3. Put a percentage on every call
Every call carries **p_up: the probability that the fund beats the CSI 300 over the horizon** (default 4 weeks).
The journal derives `confidence` from it; never pass `confidence` yourself.

1. **Start from the base rate**: the fact sheet's base-rate table gives how often funds in each composite band
   beat the CSI 300 over the next 4 weeks. Use the fund's band. Without a composite, start at 0.5.
2. **Adjust in small steps for named reasons** the base rate can't see: regime (risk-off: down), crowded flag
   (down), theme stage `crowded` or a launch wave in themes.md (down), news or policy events (either way),
   rules-only call disagreement. A few points per reason; write the base rate and each adjustment in the thesis,
   e.g. `"base 0.51 (band 60-80); +0.03 policy renewal; -0.04 crowded -> 0.50"`.
3. Stay within 0.15 to 0.85 (the journal rejects anything outside). Weekly fund outcomes are close to coin
   flips; a 0.70 is a strong view. Check the p_up calibration table in the scorecard: if past high-p calls beat
   less often than stated, shrink toward the base rate.

How p_up becomes the label the user reads:

| | Label shown | % shown | Log action |
|---|---|---|---|
| Not held, p_up ≥ the confidence floor, not crowded, rules allow | **Buy** | p_up | `buy` |
| Not held, otherwise | **Watch** | p_up | `watch` |
| Held, p_up > 0.5 | **Buy** (add) | p_up | `add` if p_up ≥ floor and it fits the targets, else `hold` |
| Held, p_up < 0.5 | **Sell** | the chance it trails (for trim/sell, the `confidence` the journal prints) | `trim` or `sell` if that chance ≥ floor, else `hold` |

The floor is `min_confidence_to_act` in the risk rules. Below it, say so plainly: "Sell 55%, below the 60% floor,
so hold." Write percentages as whole numbers (`64%`), never with decimals.

## 4. Decide
Start from the script's view, then judge it. The fact sheet gives, in this order: the **market regime**, the
**rules-only calls**, and per fund a **composite** signal (0-100), a **crowded** flag and a **cluster**.

- Read the regime first. In `risk-off`, new buys need unusually strong evidence; prefer the core sleeve.
- **Holdings**: give every holding a Buy or Sell with its percentage. Rank them on composite, trend, risk,
  flows and theme news, and write the **3 most promising** in detail. The rules-only call is the default action;
  log `"override": true, "override_reason": "..."` when your action differs, only for a reason the script can't
  see. A `crowded` fund is never an add or buy.
- **Watchlist themes**: for every theme with `curate = True` in themes.md, call at least 3 of its listed products
  (all of them if it lists fewer). Prefer different index families; a held product counts, using its holding
  call. Tag each call with `"theme": "<id>"`. Buy only within the action caps; the rest are Watch with a p_up.
  Note the theme's stage, news trend and launch count in one line.
- **New picks** outside the themes: 1-3 from the rules-only buys, `candidates.csv` or the theme ETFs.
- Never rank on raw recent return. Never buy two funds from the same cluster: they are one bet. Respect
  `max_actions_per_week` and `max_new_buys_per_week`; watch calls don't count.
- Read last week's reflection, the scorecard and signal health. Don't repeat mistakes they name.
- Log every call (one entry per fund per week):
  `PYTHONPATH=src python3 -m cfa.journal add --json '{"code":"510300","name":"...","action":"hold","p_up":0.55,"horizon_weeks":4,"target_weight_pct":20,"thesis":"base ...; ...","falsifiers":"...","data_asof":"<asof>"}'`
  Add `"theme": "<id>"` for watchlist products and `"override": true, "override_reason": "..."` when a holding's
  action differs from its rules-only call.

## 5. Write `weekly/$WEEK/digest.md`
Use these sections, in this order:
- `## Summary`: 3–5 lines, starting with the regime label, plus a one-line portfolio vs target vs benchmark
  comparison taken from the scorecard.
- `## Holdings: top 3`: per product: code and name, **Buy NN%** or **Sell NN%**, the logged action and the
  rules-only call (and why you overrode it), horizon, 2–3 evidence bullets using numbers from the fact sheet, the
  falsifier. Then a short table of the other holdings: code, name, Buy/Sell, %, one-line reason.
- `## Theme watchlist`: per curated theme: name, stage, one line on news and crowding, then a table of at least
  3 products: code, name, Buy/Watch (or Buy/Sell if held), %, one-line reason.
- `## New picks`: per pick: code and name, Buy or Watch with %, its cluster, why now, how it fits, the falsifier.
- `## Risks and what would change my mind`
- `## Data notes`: the as-of date, stale or missing sources, anything that weakens the call.

Copy every decimal figure exactly from the inputs, and don't do arithmetic. End with the line: "Research signals
from public data, not financial advice."

## 6. Reflect, check, ship
- Write `journal/reflections/$WEEK.md` in 15 lines or fewer: what the scorecard says about past calls (including
  p_up calibration and themes), what to do differently, and any proposed rule change written as a suggestion for
  the user. Never edit the rules.
- `cp weekly/$WEEK/digest.md reports/latest.md`
- `PYTHONPATH=src python3 -m cfa.check_digest --week $WEEK`, and fix everything it reports.
- `git add weekly reports journal state && git commit -m "weekly digest $WEEK" && git push origin HEAD:main`
