# Signal health (walk-forward backtest)

51 funds, weekly from 2016-01-08 to 2026-10-23. IC = rank correlation between a signal and the next 4 (or 12) weeks' returns across funds; t counts one independent observation per 4 weeks. Spread = top third minus average, next 4 weeks, after costs.

Accepted (full weight) = positive IC with t above the floor, same sign in 2 of 3 subperiods, positive spread. Unproven (half weight) = positive and consistent but not yet significant. Insufficient (full weight) = too little history, literature prior kept. Rejected (no weight) = negative or inconsistent IC.

| signal | status | weeks | ic_4w | t_4w | ic_12w | ic_2016_19 | ic_2020_22 | ic_2023_now | top_third_spread_4w_pct | spread_periods |
|---|---|---|---|---|---|---|---|---|---|---|
| trend_12w | unproven | 546 | 0.012 | 0.41 | 0.025 | 0.002 | 0.002 | 0.031 | 0.18 | 137 |
| trend_26w | unproven | 546 | 0.019 | 0.63 | 0.055 | 0.013 | 0.019 | 0.026 | 0.16 | 137 |
| ma200_gap | unproven | 546 | 0.027 | 0.81 | 0.059 | 0.017 | 0.016 | 0.046 | 0.19 | 137 |
| rev_1w | rejected | 546 | -0.028 | -0.87 | -0.01 | -0.028 | -0.043 | -0.015 | -0.14 | 137 |
| rev_4w | rejected | 546 | -0.008 | -0.27 | -0.012 | 0.008 | -0.006 | -0.028 | -0.3 | 137 |
| max_20d | unproven | 546 | 0.039 | 1.22 | 0.051 | 0.049 | 0.01 | 0.051 | -0.24 | 137 |
| turnover_surge | unproven | 546 | 0.012 | 0.61 | 0.014 | -0.005 | 0.049 | 0.001 | -0.03 | 137 |
| low_vol | unproven | 546 | 0.054 | 1.49 | 0.108 | 0.093 | -0.016 | 0.069 | -0.02 | 137 |
| legacy_screen | unproven | 546 | 0.028 | 0.89 | 0.053 | 0.02 | 0.023 | 0.041 | 0.23 | 137 |

Signal meanings: `trend_12w` 12-week return skipping the last week, per unit of 60-day volatility; `trend_26w` 26-week return skipping the last week, per unit of 60-day volatility; `ma200_gap` price vs its 200-day average; `rev_1w` minus last week's return (short-term reversal); `rev_4w` minus last 4 weeks' return (one-month reversal); `max_20d` minus the largest daily gain in 20 days (lottery effect); `turnover_surge` minus 5-day turnover vs its 120-day median (crowding); `low_vol` minus 60-day volatility; `legacy_screen` the old candidate score: raw 1/3/6/12-month returns, for comparison only

## Regime check (CSI 300, next 4 weeks)

| state | weeks | csi300_next_4w_pct |
|---|---|---|
| breadth_above_half | 305 | 0.74 |
| breadth_below_half | 237 | 0.09 |

## Base rates for p_up (next 4 weeks vs CSI 300, by composite band)

Start a call's p_up from its band's beat rate, then adjust for named reasons. Weights were fitted on the same history, so the gap between bands is a little optimistic.

| composite_band | fund_weeks | beat_csi300_pct | avg_excess_4w_pct |
|---|---|---|---|
| all | 20017 | 49.6 | 0.31 |
| 0-20 | 433 | 50.1 | 0.54 |
| 20-40 | 5230 | 47.2 | 0.13 |
| 40-60 | 8048 | 49.7 | 0.46 |
| 60-80 | 5190 | 50.6 | 0.26 |
| 80-100 | 1116 | 54.8 | 0.15 |
