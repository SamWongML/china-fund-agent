# Signal health (walk-forward backtest)

51 funds, weekly from 2016-01-08 to 2026-11-06. IC = rank correlation between a signal and the next 4 (or 12) weeks' returns across funds; t counts one independent observation per 4 weeks. Spread = top third minus average, next 4 weeks, after costs.

Accepted (full weight) = positive IC with t above the floor, same sign in 2 of 3 subperiods, positive spread. Unproven (half weight) = positive and consistent but not yet significant. Insufficient (full weight) = too little history, literature prior kept. Rejected (no weight) = negative or inconsistent IC.

| signal | status | weeks | ic_4w | t_4w | ic_12w | ic_2016_19 | ic_2020_22 | ic_2023_now | top_third_spread_4w_pct | spread_periods |
|---|---|---|---|---|---|---|---|---|---|---|
| trend_12w | unproven | 550 | 0.017 | 0.58 | 0.025 | 0.002 | 0.002 | 0.045 | 0.22 | 138 |
| trend_26w | unproven | 550 | 0.017 | 0.57 | 0.053 | 0.013 | 0.019 | 0.02 | 0.13 | 138 |
| ma200_gap | unproven | 550 | 0.027 | 0.81 | 0.059 | 0.017 | 0.016 | 0.045 | 0.16 | 138 |
| rev_1w | rejected | 550 | -0.029 | -0.92 | -0.01 | -0.028 | -0.043 | -0.019 | -0.19 | 138 |
| rev_4w | rejected | 550 | -0.011 | -0.35 | -0.015 | 0.008 | -0.006 | -0.035 | -0.33 | 138 |
| max_20d | unproven | 550 | 0.041 | 1.29 | 0.052 | 0.049 | 0.01 | 0.058 | -0.21 | 138 |
| turnover_surge | rejected | 550 | 0.012 | 0.6 | 0.014 | -0.005 | 0.049 | 0.0 | -0.02 | 138 |
| low_vol | unproven | 550 | 0.058 | 1.61 | 0.11 | 0.093 | -0.016 | 0.08 | 0.02 | 138 |
| legacy_screen | unproven | 550 | 0.03 | 0.95 | 0.053 | 0.02 | 0.023 | 0.046 | 0.25 | 138 |

Signal meanings: `trend_12w` 12-week return skipping the last week, per unit of 60-day volatility; `trend_26w` 26-week return skipping the last week, per unit of 60-day volatility; `ma200_gap` price vs its 200-day average; `rev_1w` minus last week's return (short-term reversal); `rev_4w` minus last 4 weeks' return (one-month reversal); `max_20d` minus the largest daily gain in 20 days (lottery effect); `turnover_surge` minus 5-day turnover vs its 120-day median (crowding); `low_vol` minus 60-day volatility; `legacy_screen` the old candidate score: raw 1/3/6/12-month returns, for comparison only

## Regime check (CSI 300, next 4 weeks)

| state | weeks | csi300_next_4w_pct |
|---|---|---|
| breadth_above_half | 305 | 0.74 |
| breadth_below_half | 239 | -0.06 |

## Base rates for p_up (next 4 weeks vs CSI 300, by composite band)

Start a call's p_up from its band's beat rate, then adjust for named reasons. Weights were fitted on the same history, so the gap between bands is a little optimistic.

| composite_band | fund_weeks | beat_csi300_pct | avg_excess_4w_pct |
|---|---|---|---|
| all | 20201 | 49.7 | 0.32 |
| 0-20 | 767 | 47.3 | 0.3 |
| 20-40 | 5572 | 47.7 | 0.18 |
| 40-60 | 7062 | 49.4 | 0.38 |
| 60-80 | 5214 | 50.9 | 0.39 |
| 80-100 | 1586 | 55.1 | 0.35 |
