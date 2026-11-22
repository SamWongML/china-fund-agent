# Scorecard

Target: 12%/yr (≈0.95%/month). Benchmark: sh000300. Entry = first price after the decision date; hit = beat the benchmark (or underperformed it for trim/sell). rules_* = the mechanical core/satellite calls (journal/rules_baseline.jsonl), graded the same way; the advisor should beat them. Brier: lower is better, 0.25 is a coin flip.

| decisions | closed | hit_rate_pct | avg_excess_pct | brier | brier_p_up | rules_closed | rules_hit_rate_pct | rules_avg_excess_pct | annual_target_pct | portfolio_1m_pct | benchmark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 48 | 17 | 52.9 | 0.4 | 0.228 | 0.228 | 4 | 75.0 | 1.31 | 12.0 |  | sh000300 |

## By action (closed)

| action | n | hit_rate | avg_excess |
|---|---|---|---|
| watch | 17 | 0.5294117647058824 | 0.4 |

## Overrides of the rules-only call (closed)

| override | n | hit_rate | avg_excess |
|---|---|---|---|
| False | 17 | 0.5294117647058824 | 0.4 |

## Confidence calibration (closed)

| conf_bucket | n | hit_rate |
|---|---|---|
| (0.0, 0.5] | 12 | 0.3333333333333333 |
| (0.5, 0.7] | 5 | 1.0 |

## p_up calibration (closed): stated chance of beating the benchmark vs how often it did

If beat_rate sits well below mean_p_up in the high buckets, shrink p_up toward the base rate.

| p_bucket | n | mean_p_up | beat_rate |
|---|---|---|---|
| (0.4, 0.5] | 12 | 0.45 | 0.3333333333333333 |
| (0.5, 0.6] | 5 | 0.52 | 1.0 |

## Watchlist themes (closed calls)

| theme | n | beat_rate | avg_excess |
|---|---|---|---|
| ai_compute | 2 | 0.5 | -1.68 |
| chips_equipment | 2 | 0.0 | -6.11 |
| grid_power | 2 | 1.0 | 3.7 |
| innovative_drugs | 3 | 1.0 | 4.98 |
| new_materials | 3 | 0.0 | -4.17 |
| robotics | 3 | 0.3333333333333333 | 1.38 |

## Latest decisions

| id | week | code | action | confidence | p_up | view | theme | horizon_weeks | held | override | status | entry_date | exit_date | ret_pct | bench_ret_pct | excess_pct | hit | beat |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| e7c074c69aab | 2026-W44 | 159516 | watch | 0.48 | 0.48 | watch | chips_equipment | 4 | False | False | open | 2026-10-28 | 2026-11-20 | 2.81 | -3.17 | 5.97 |  |  |
| 5dc1bfea4e09 | 2026-W44 | 588200 | watch | 0.47 | 0.47 | watch | chips_equipment | 4 | False | False | open | 2026-10-28 | 2026-11-20 | -6.54 | -3.17 | -3.37 |  |  |
| c9894939319e | 2026-W44 | 512480 | watch | 0.46 | 0.46 | watch | chips_equipment | 4 | False | False | open | 2026-10-28 | 2026-11-20 | -6.52 | -3.17 | -3.36 |  |  |
| d05562fe4e94 | 2026-W44 | 159227 | watch | 0.47 | 0.47 | watch | space_satellites | 4 | False | False | open | 2026-10-28 | 2026-11-06 | 0.84 | -0.72 | 1.57 |  |  |
| 37be0df05133 | 2026-W44 | 159267 | watch | 0.47 | 0.47 | watch | space_satellites | 4 | False | False | open | 2026-10-28 | 2026-11-06 | 0.75 | -0.72 | 1.47 |  |  |
| 177cfd094a6f | 2026-W44 | 159206 | watch | 0.45 | 0.45 | watch | space_satellites | 4 | False | False | open | 2026-10-28 | 2026-11-06 | -1.11 | -0.72 | -0.39 |  |  |
| b232771d01ca | 2026-W44 | 159883 | watch | 0.51 | 0.51 | watch | innovative_drugs | 4 | False | False | open | 2026-10-28 | 2026-11-20 | -5.91 | -3.17 | -2.74 |  |  |
| a3e4a38fbc28 | 2026-W44 | 159992 | watch | 0.51 | 0.51 | watch | innovative_drugs | 4 | False | False | open | 2026-10-28 | 2026-11-20 | -5.06 | -3.17 | -1.9 |  |  |
| e7a08420e1f1 | 2026-W44 | 159837 | watch | 0.5 | 0.5 | watch | innovative_drugs | 4 | False | False | open | 2026-10-28 | 2026-11-20 | -4.86 | -3.17 | -1.7 |  |  |
| d841f7aec167 | 2026-W44 | 159611 | watch | 0.48 | 0.48 | watch | grid_power | 4 | False | False | open | 2026-10-28 | 2026-11-20 | 2.05 | -3.17 | 5.22 |  |  |
| e2180bf23cd5 | 2026-W44 | 159625 | watch | 0.47 | 0.47 | watch | grid_power | 4 | False | False | open | 2026-10-28 | 2026-11-20 | 1.43 | -3.17 | 4.6 |  |  |
| 7a94ff522be1 | 2026-W44 | 159326 | watch | 0.45 | 0.45 | watch | grid_power | 4 | False | False | open | 2026-10-28 | 2026-11-06 | -0.07 | -0.72 | 0.65 |  |  |
| 6eed9d1c1ede | 2026-W44 | 516150 | watch | 0.47 | 0.47 | watch | new_materials | 4 | False | False | open | 2026-10-28 | 2026-11-20 | -14.04 | -3.17 | -10.87 |  |  |
| 67dd1116b824 | 2026-W44 | 562800 | watch | 0.46 | 0.46 | watch | new_materials | 4 | False | False | open | 2026-10-28 | 2026-11-20 | -13.67 | -3.17 | -10.51 |  |  |
| 701441f4c6df | 2026-W44 | 588160 | watch | 0.45 | 0.45 | watch | new_materials | 4 | False | False | open | 2026-10-28 | 2026-11-20 | -13.54 | -3.17 | -10.38 |  |  |
