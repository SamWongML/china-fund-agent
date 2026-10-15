# Signal health (walk-forward backtest)

51 funds, weekly from 2016-01-08 to 2026-10-15. IC = rank correlation between a signal and the next 4 (or 12) weeks' returns across funds; t counts one independent observation per 4 weeks. Spread = top third minus average, next 4 weeks, after costs.

Accepted (full weight) = positive IC with t above the floor, same sign in 2 of 3 subperiods, positive spread. Unproven (half weight) = positive and consistent but not yet significant. Insufficient (full weight) = too little history, literature prior kept. Rejected (no weight) = negative or inconsistent IC.

| signal | status | weeks | ic_4w | t_4w | ic_12w | ic_2016_19 | ic_2020_22 | ic_2023_now | top_third_spread_4w_pct | spread_periods |
|---|---|---|---|---|---|---|---|---|---|---|
| trend_12w | rejected | 545 | 0.006 | 0.22 | 0.02 | -0.005 | -0.003 | 0.027 | 0.15 | 137 |
| trend_26w | unproven | 545 | 0.014 | 0.45 | 0.052 | 0.001 | 0.017 | 0.025 | 0.16 | 137 |
| ma200_gap | unproven | 545 | 0.022 | 0.67 | 0.055 | 0.011 | 0.009 | 0.045 | 0.19 | 137 |
| rev_1w | rejected | 545 | -0.027 | -0.84 | -0.007 | -0.026 | -0.04 | -0.017 | -0.14 | 137 |
| rev_4w | rejected | 545 | -0.004 | -0.13 | -0.007 | 0.014 | -0.0 | -0.026 | -0.26 | 137 |
| max_20d | unproven | 545 | 0.036 | 1.12 | 0.046 | 0.045 | 0.007 | 0.05 | -0.24 | 137 |
| turnover_surge | unproven | 545 | 0.016 | 0.77 | 0.014 | 0.003 | 0.049 | 0.002 | -0.01 | 137 |
| low_vol | unproven | 545 | 0.047 | 1.31 | 0.103 | 0.081 | -0.019 | 0.065 | -0.06 | 137 |
| legacy_screen | unproven | 545 | 0.022 | 0.68 | 0.05 | 0.012 | 0.014 | 0.039 | 0.19 | 137 |

Signal meanings: `trend_12w` 12-week return skipping the last week, per unit of 60-day volatility; `trend_26w` 26-week return skipping the last week, per unit of 60-day volatility; `ma200_gap` price vs its 200-day average; `rev_1w` minus last week's return (short-term reversal); `rev_4w` minus last 4 weeks' return (one-month reversal); `max_20d` minus the largest daily gain in 20 days (lottery effect); `turnover_surge` minus 5-day turnover vs its 120-day median (crowding); `low_vol` minus 60-day volatility; `legacy_screen` the old candidate score: raw 1/3/6/12-month returns, for comparison only

## Regime check (CSI 300, next 4 weeks)

| state | weeks | csi300_next_4w_pct |
|---|---|---|
| breadth_above_half | 301 | 0.78 |
| breadth_below_half | 241 | 0.11 |

## Base rates for p_up (next 4 weeks vs CSI 300, by composite band)

Start a call's p_up from its band's beat rate, then adjust for named reasons. Weights were fitted on the same history, so the gap between bands is a little optimistic.

| composite_band | fund_weeks | beat_csi300_pct | avg_excess_4w_pct |
|---|---|---|---|
| all | 19976 | 49.3 | 0.28 |
| 0-20 | 458 | 49.8 | 0.81 |
| 20-40 | 4555 | 47.6 | 0.18 |
| 40-60 | 9306 | 48.7 | 0.38 |
| 60-80 | 4577 | 51.1 | 0.17 |
| 80-100 | 1080 | 54.6 | 0.14 |
