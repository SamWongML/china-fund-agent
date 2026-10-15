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
| `weekly/YYYY-Www/{factsheets.md,news_rollup.md,candidates.csv,inputs.json}` | `cfa.weekly_build` | read |
| `weekly/YYYY-Www/digest.md`, `reports/latest.md` | weekly-digest skill (Claude) | write |
| `journal/decisions.jsonl` | `python -m cfa.journal add` only | append via that command |
| `journal/reflections/*.md` | weekly-digest skill | write |
| `journal/scorecard*` | `cfa.scorecard` | read |

## Rules for agents

1. Never read raw data to make decisions. Don't `cat` parquet or the raw news JSONL. Read the agent-facing
   files above. If you must query raw data, use DuckDB, e.g.
   `python -c "import duckdb; print(duckdb.sql(\"select * from 'data/raw/funds/etf/**/*.parquet' where code='510300'\"))"`.
2. Every number you write must come from an input file. Copy it exactly. Don't do arithmetic in prose;
   if a figure isn't computed for you, describe it in words.
3. New picks come only from `weekly/<week>/candidates.csv` or the theme ETFs in `factsheets.md`.
4. If `inputs.json` says `"ready": false`, write a `## Data gap` digest and give no buy/sell calls.
5. Default to hold. Respect `config/risk_rules.yaml`: max actions per week, confidence floor,
   short-holding redemption penalties on open-end funds.
6. Commit to `main` with a clear message and push. Never rewrite history.

## Jobs

| Job | Runner | HKT |
|---|---|---|
| News collect (`cfa.collect_news`) + daily input (`cfa.news_prep`) | Actions `news.yml` | hourly 06:13–23:13, plus 01:13, 04:13 |
| Fund EOD snapshot (`cfa.collect_funds`) | Actions `funds.yml` | 23:17 Mon–Fri, retry 07:47 Tue–Sat |
| Daily news digest | Claude scheduled task, skill `news-digest` | 07:07 daily |
| Weekly build (`cfa.weekly_build`) | Actions `weekly-build.yml` | Sun 06:17 |
| Weekly advisory | Claude scheduled task, skill `weekly-digest` | Sun 08:07 |
| Maintenance (`cfa.maintenance`) | Actions `maintenance.yml` | 1st of month 10:23 |
| Source smoke test (`cfa.smoke_test`) | Actions `smoke.yml` | on demand |

Claude sessions cannot reach Chinese data hosts. Anything that fetches data runs on Actions.

## Commands

`make install | smoke | funds | news | news-prep | weekly-build | scorecard | check-digest | test`
(all set `PYTHONPATH=src` and `TZ=Asia/Hong_Kong`).

## Layout

- `src/cfa/`: collectors, `weekly_build`, `scorecard`, `journal`, `check_digest` (Stop-hook gate), `guard` (PreToolUse hook)
- `data/raw/funds/<dataset>/year=/month=/<date>.parquet`: write-once daily snapshots (etf, lof, open, open_rank, exchange_rank)
- `data/raw/news/YYYY/MM/<date>.jsonl`: deduped headlines and snippets with region, themes and score
- `data/history/nav/<code>.csv`, `data/history/index/<sym>.csv`: per-code price history for held and watched funds
- `data/latest/snapshot.md`, `data/manifest.json`, `state/status/<job>.json`, `state/runs/<job>.jsonl`, `state/smoke.md`

To run an Actions job on demand from an agent session (workflow_dispatch isn't available there), write the
current time into `.github/kick/<workflow-name>` and push to main.
