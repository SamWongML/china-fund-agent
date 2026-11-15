# Signal health (walk-forward backtest)

51 funds, weekly from 2016-01-08 to 2026-11-13. IC = rank correlation between a signal and the next 4 (or 12) weeks' returns across funds; t counts one independent observation per 4 weeks. Spread = top third minus average, next 4 weeks, after costs.

Accepted (full weight) = positive IC with t above the floor, same sign in 2 of 3 subperiods, positive spread. Unproven (half weight) = positive and consistent but not yet significant. Insufficient (full weight) = too little history, literature prior kept. Rejected (no weight) = negative or inconsistent IC.

| signal | status | weeks | ic_4w | t_4w | ic_12w | ic_2016_19 | ic_2020_22 | ic_2023_now | top_third_spread_4w_pct | spread_periods |
|---|---|---|---|---|---|---|---|---|---|---|
| trend_12w | unproven | 551 | 0.018 | 0.61 | 0.025 | 0.002 | 0.002 | 0.047 | 0.22 | 138 |
| trend_26w | unproven | 551 | 0.017 | 0.56 | 0.053 | 0.013 | 0.019 | 0.02 | 0.13 | 138 |
| ma200_gap | unproven | 551 | 0.027 | 0.84 | 0.058 | 0.017 | 0.016 | 0.047 | 0.16 | 138 |
| rev_1w | rejected | 551 | -0.03 | -0.95 | -0.009 | -0.028 | -0.043 | -0.022 | -0.19 | 138 |
| rev_4w | rejected | 551 | -0.012 | -0.38 | -0.016 | 0.008 | -0.006 | -0.038 | -0.33 | 138 |
| max_20d | unproven | 551 | 0.041 | 1.3 | 0.053 | 0.049 | 0.01 | 0.058 | -0.21 | 138 |
| turnover_surge | rejected | 551 | 0.012 | 0.59 | 0.014 | -0.005 | 0.049 | -0.0 | -0.02 | 138 |
| low_vol | unproven | 551 | 0.059 | 1.63 | 0.111 | 0.093 | -0.016 | 0.082 | 0.02 | 138 |
| legacy_screen | unproven | 551 | 0.031 | 0.97 | 0.053 | 0.02 | 0.023 | 0.048 | 0.25 | 138 |

Signal meanings: `trend_12w` 12-week return skipping the last week, per unit of 60-day volatility; `trend_26w` 26-week return skipping the last week, per unit of 60-day volatility; `ma200_gap` price vs its 200-day average; `rev_1w` minus last week's return (short-term reversal); `rev_4w` minus last 4 weeks' return (one-month reversal); `max_20d` minus the largest daily gain in 20 days (lottery effect); `turnover_surge` minus 5-day turnover vs its 120-day median (crowding); `low_vol` minus 60-day volatility; `legacy_screen` the old candidate score: raw 1/3/6/12-month returns, for comparison only

## Regime check (CSI 300, next 4 weeks)

| state | weeks | csi300_next_4w_pct |
|---|---|---|
| breadth_above_half | 305 | 0.74 |
| breadth_below_half | 239 | -0.11 |

## Base rates for p_up (next 4 weeks vs CSI 300, by composite band)

Start a call's p_up from its band's beat rate, then adjust for named reasons. Weights were fitted on the same history, so the gap between bands is a little optimistic.

| composite_band | fund_weeks | beat_csi300_pct | avg_excess_4w_pct |
|---|---|---|---|
| all | 20242 | 49.8 | 0.32 |
| 0-20 | 767 | 47.3 | 0.3 |
| 20-40 | 5586 | 47.7 | 0.17 |
| 40-60 | 7079 | 49.4 | 0.38 |
| 60-80 | 5220 | 51.0 | 0.39 |
| 80-100 | 1590 | 55.3 | 0.37 |
