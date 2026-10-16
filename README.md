# china-fund-agent

A personal research loop for China onshore ETFs, LOFs and public funds.

- **Every trading day**, GitHub Actions snapshots the whole onshore fund universe (prices, NAVs,
  premium/discount, shares outstanding, trailing returns) into `data/`.
- **Every hour**, Actions collects market-moving headlines from China, the US and the rest of the world
  into `data/raw/news/`, removing duplicates.
- **Every morning** Claude writes a short digest of the previous day's news into `news/daily/`.
- **Every Sunday morning (HKT)** a script builds fact sheets. Claude then reads them and writes calls to
  `weekly/<week>/digest.md` (latest always at `reports/latest.md`): **Buy or Sell** for your holdings,
  **Buy or Watch** for funds you don't own, each with a percentage, the chance it beats the CSI 300 over the
  call's horizon. Percentages start from a historical base rate and are graded every week.
- **Theme watchlist**: `watchlist/themes.yaml` lists promising fields (AI, robotics, chips...), maintained by a
  monthly theme-scout run. The Sunday build finds every onshore ETF in each field, one per index family, and
  Claude covers at least 3 per active field.
- The Sunday build also scores every fund on signals that have held up in China's market (3-6 month trend,
  crowding and lottery-like spikes, volatility), tests those signals on ten years of history every week
  (`journal/signal_health.md`), labels the market regime, and proposes core/satellite target weights. Its
  mechanical "rules-only" calls are graded alongside Claude's, so you can see whether Claude's judgement adds
  anything.
- **HTML briefs**: after each scheduled run, `briefs/<task>.html` (morning, news, weekly, themes) is
  re-rendered from that run's Markdown by a script, overwriting the previous one. Open `briefs/index.html`,
  or https://samwongml.github.io/china-fund-agent/ once GitHub Pages is on (Settings > Pages > Source:
  GitHub Actions).
- Every call goes into an append-only journal and is graded later against what actually happened
  (`journal/scorecard_summary.md`). After a few months, that shows whether the advice beats simply
  holding the CSI 300.

Target: 12% a year (≈0.95%/month), with 15% as a stretch goal, judged on a rolling 12 months. These are
research signals from public data, not financial advice.

## What you maintain

1. **`portfolio/holdings.yaml`**: what you own. Replace `holdings: []` with your entries, using the
   format shown in the file. Update it whenever you buy or sell.
2. Optionally edit `config/risk_rules.yaml` (how bold the advisor may be), `config/target.yaml`, and
   `config/universe.yaml` (themes and the starting ETF watchlist).

Agents can read these files but are blocked from editing them.

## First run

1. Actions → **smoke** → Run workflow. It calls every data and news source once and writes
   `state/smoke.md`. Some Chinese sites block overseas cloud IPs. If many sources fail, the fix is a
   self-hosted runner on a Hong Kong machine.
2. Actions → **funds** → Run workflow to take the first snapshot. Price history is backfilled
   automatically for your holdings and the watchlist.

How the system works and the rules agents follow are in [AGENTS.md](AGENTS.md).
