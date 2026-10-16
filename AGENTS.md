# china-fund-agent

Personal research system for China onshore ETFs, LOFs and open-end public funds.
Scripts collect and compute; Claude only judges. Git history is the audit trail.

Goal: steady returns, measured against `config/target.yaml` (12%/yr target, 15% stretch, rolling 12 months).
The target is a yardstick, not an instruction: never concentrate or trade more to chase it.
Output is research signals from public data, not licensed financial advice.

## Who writes what

| Path | Written by | Agent may |
|---|---|---|
| `portfolio/holdings.yaml` | the user | read only (hook-enforced) |
| `config/risk_rules.yaml`, `config/target.yaml` | the user | read only (hook-enforced) |
| `config/universe.yaml`, `config/sources.yaml` | user or agent via PR | edit when asked |
| `data/**`, `state/**` | GitHub Actions scripts | read; never hand-edit |
| `news/daily/inputs/*.md` | `cfa.news_prep` (script) | read |
| `news/daily/YYYY-MM-DD.md` | news-digest skill (Claude) | write |
| `watchlist/themes.yaml` | theme-scout skill (Claude) or the user | write (validate with `cfa.themes check`) |
| `research/themes/YYYY-MM.md` | theme-scout skill | write |
| `weekly/YYYY-Www/{factsheets.md,news_rollup.md,themes.md,theme_scan.md,candidates.csv,inputs.json}` | `cfa.weekly_build` | read |
| `weekly/YYYY-Www/digest.md`, `reports/latest.md` | weekly-digest skill (Claude) | write |
| `journal/decisions.jsonl` | `python -m cfa.journal add` only | append via that command |
| `journal/reflections/*.md` | weekly-digest skill | write |
| `journal/scorecard*` | `cfa.scorecard` | read |
| `journal/signal_health.{md,json}` | `cfa.backtest` (in the weekly build) | read |
| `journal/rules_baseline.jsonl` | `cfa.portfolio` (in the weekly build) | read |

## Rules for agents

1. Never read raw data to make decisions. Don't `cat` parquet or the raw news JSONL. Read the agent-facing
   files above. If you must query raw data, use DuckDB, e.g.
   `python -c "import duckdb; print(duckdb.sql(\"select * from 'data/raw/funds/etf/**/*.parquet' where code='510300'\"))"`.
2. Every number you write must come from an input file. Copy it exactly. Don't do arithmetic in prose;
   if a figure isn't computed for you, describe it in words.
3. New picks come only from `weekly/<week>/candidates.csv`, the theme ETFs in `factsheets.md`, or the watchlist
   products in `themes.md`. Every call carries `p_up` (probability of beating the CSI 300 over its horizon),
   started from the base-rate table and kept within the caps in `config/universe.yaml`.
4. If `inputs.json` says `"ready": false`, write a `## Data gap` digest and give no buy/sell calls.
5. Default to hold. Respect `config/risk_rules.yaml`: max actions per week, confidence floor,
   short-holding redemption penalties on open-end funds. The weekly rules-only call is the default for each
   holding; departing from it needs a logged `override_reason`. Never add to or buy a fund flagged `crowded`.
6. Commit to `main` with a clear message and push. Never rewrite history.

## Jobs

| Job | Runner | HKT |
|---|---|---|
| News collect (`cfa.collect_news`) + daily input (`cfa.news_prep`) | Actions `news.yml` | hourly 06:13–23:13, plus 01:13, 04:13 |
| Fund EOD snapshot (`cfa.collect_funds`) | Actions `funds.yml` | 23:17 Mon–Fri, retry 07:47 Tue–Sat |
| Daily news digest | Claude scheduled task, skill `news-digest` | 07:07 daily |
| Weekly build (`cfa.weekly_build`) | Actions `weekly-build.yml` | Sun 06:17 |
| Weekly advisory | Claude scheduled task, skill `weekly-digest` | Sun 08:07 |
| Theme scout | Claude scheduled task, skill `theme-scout` | 1st Sat of the month 09:58 |
| Maintenance (`cfa.maintenance`) | Actions `maintenance.yml` | 1st of month 10:23 |
| Source smoke test (`cfa.smoke_test`) | Actions `smoke.yml` | on demand |

Claude sessions cannot reach Chinese data hosts. Anything that fetches data runs on Actions.

## Commands

`make install | smoke | funds | news | news-prep | weekly-build | scorecard | check-digest | test`
(all set `PYTHONPATH=src` and `TZ=Asia/Hong_Kong`).

## Layout

- `src/cfa/`: collectors, `adjust` (split/dividend price adjustment), `signals` (trend, reversal, crowding,
  regime), `backtest` (walk-forward signal test, p_up base rates), `themes` (watchlist products and discovery scan), `portfolio` (core/satellite targets, rules-only calls),
  `weekly_build`, `scorecard`, `journal`, `check_digest` (Stop-hook gate), `guard` (PreToolUse hook)
- `data/raw/funds/<dataset>/year=/month=/<date>.parquet`: write-once daily snapshots (etf, lof, open, open_rank, exchange_rank)
- `data/raw/news/YYYY/MM/<date>.jsonl`: deduped headlines and snippets with region, themes and score
- `data/history/nav/<code>.csv`: per-code history (date, raw, price, volume, basis) for held, watched and research
  funds; `price` is split- and dividend-adjusted (ETF/LOF) or total-return NAV (open funds)
- `data/history/index/<sym>.csv`, `data/history/macro/` (CSI 300 PE, 10-year CGB yield), `data/ref/fund_actions.csv`
  (fund splits and dividends)
- `data/latest/snapshot.md`, `data/manifest.json`, `state/status/<job>.json`, `state/runs/<job>.jsonl`, `state/smoke.md`

To run an Actions job on demand from an agent session (workflow_dispatch isn't available there), write the
current time into `.github/kick/<workflow-name>` and push to main.
