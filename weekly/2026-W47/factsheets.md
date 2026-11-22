# Fact sheets 2026-W47 (data as of 2026-11-20, built 2026-11-22 10:19 HKT)

Data ready: **True** (last good fund snapshot 2026-11-20; missing history: none).

Returns in %: r_1w=5 trading days, r_4w=20, r_12w=60, r_26w=120, r_52w=250. Prices are adjusted for splits and dividends (ETF/LOF) or total-return NAV (open funds); basis says which. pnl_pct uses the raw latest price.

Signals: composite = 0-100 weighted percentile of the live signals (trend, reversal, lottery, crowding, low volatility) across ~60 sector and broad ETFs plus holdings and candidates; higher is better. crowded = reasons not to add now. cluster = the highest-ranked fund it moves with (60-day correlation of market-relative returns above the threshold); funds sharing a cluster are one bet. Details: journal/signal_health.md.

## Market regime: **risk-off**

| label | score | votes | sh000300_ma200_gap_pct | sh000300_r_12w_pct | sh000905_ma200_gap_pct | sh000905_r_12w_pct | breadth_above_ma200_pct | breadth_n |
|---|---|---|---|---|---|---|---|---|
| risk-off | 0.0 | 5 | -14.04 | -13.9 | -23.99 | -23.49 | 15.7 | 51 |

Signal weight multipliers from the backtest: {'trend_12w': 0.5, 'trend_26w': 0.5, 'ma200_gap': 0.5, 'rev_1w': 0.0, 'rev_4w': 0.0, 'max_20d': 0.5, 'turnover_surge': 0.0, 'low_vol': 0.5}. Backtest status: {'trend_12w': 'unproven', 'trend_26w': 'unproven', 'ma200_gap': 'unproven', 'rev_1w': 'rejected', 'rev_4w': 'rejected', 'max_20d': 'unproven', 'turnover_surge': 'rejected', 'low_vol': 'unproven', 'legacy_screen': 'unproven'}.

## Holdings

_none_

## Rules-only calls (the baseline your calls are graded against)

Target weights: core {'511010': 25.0, '510880': 15.6, '510300': 18.8, '518880': 10.6}, satellite {}, unallocated 30.0%. risk-off regime: satellite sleeve left unallocated (hold bonds or cash)

| code | action | current_weight_pct | target_weight_pct | reason | name | composite | crowded | cluster |
|---|---|---|---|---|---|---|---|---|
| 511010 | buy | 0.0 | 25.0 | core sleeve | 国债ETF国泰 | 86.9 |  | 004726 |
| 510880 | buy | 0.0 | 15.6 | core sleeve | 红利ETF华泰柏瑞 | 75.3 |  | 004726 |
| 510300 | buy | 0.0 | 18.8 | core sleeve | 沪深300ETF华泰柏瑞 | 32.9 |  | 004726 |
| 518880 | buy | 0.0 | 10.6 | core sleeve | 黄金ETF华安 | 38.9 |  | 009477 |

## Candidates (pre-screened, not held)

| code | kind | last_date | basis | r_1w | r_4w | r_12w | r_26w | r_52w | max_dd_52w | off_52w_high | vol_60d_ann | above_ma20 | above_ma60 | name | screen_score | chase_warning | composite | crowded | cluster | trend_12w_rank | trend_26w_rank | above_ma200 | vol60_pct | premium_pct | turnover_cny_m | shares_chg_5d_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 004726 | open | 2026-11-20 | tr_nav | -0.34 | 1.13 | 2.65 | 30.22 | 34.42 | -19.35 | -0.34 | 2.86 | True | True | 先锋聚优A | 81.2 | False | 98.3 |  | 004726 | 100.0 | 100.0 | True | 2.88 |  |  |  |
| 003226 | open | 2026-11-20 | tr_nav | -0.02 | -0.23 | 1.5 | 3.08 | 5.28 | -1.16 | -0.46 | 1.52 | False | True | 中信保诚稳健债券A | 92.0 | False | 96.2 |  | 004726 | 99.0 | 98.0 | True | 1.53 |  |  |  |
| 002849 | open | 2026-11-20 | tr_nav | 1.3 | 5.25 | 6.31 | 13.85 | 16.97 | -7.31 | 0.0 | 7.74 | True | True | 金信智能中国2025混合A | 78.8 | False | 94.7 |  | 004726 | 94.0 | 99.0 | True | 7.81 |  |  |  |
| 004597 | open | 2026-11-20 | tr_nav | 2.99 | 8.42 | 12.69 | 20.77 | 10.82 | -13.0 | 0.0 | 14.04 | True | True | 南方中证银行ETF发起联接A | 79.5 | False | 91.2 |  | 004726 | 98.0 | 97.0 | True | 14.15 |  |  |  |
| 008298 | open | 2026-11-20 | tr_nav | 3.01 | 8.45 | 12.64 | 20.68 | 11.03 | -12.78 | 0.0 | 14.04 | True | True | 华夏中证银行ETF联接A | 79.4 | False | 90.4 |  | 004726 | 97.0 | 96.0 | True | 14.16 |  |  |  |
| 002334 | open | 2026-11-20 | tr_nav | -0.52 | 2.55 | 3.36 | 10.69 | 8.34 | -9.37 | -1.96 | 9.14 | False | True | 汇丰晋信大盘波动股票A | 78.9 | False | 90.4 |  | 004726 | 90.0 | 92.0 | True | 9.22 |  |  |  |
| 022220 | open | 2026-11-20 | tr_nav | -0.0 | -0.09 | 0.63 | 1.26 | 2.63 | -0.38 | -0.23 | 0.85 | False | True | 鹏华丰盈债券D | 89.3 | False | 89.0 |  | 004726 | 83.0 | 89.0 | True | 0.86 |  |  |  |
| 515020 | etf | 2026-11-20 | adj_close | 3.01 | 9.18 | 13.16 | 21.32 | 11.64 | -13.05 | 0.0 | 15.11 | True | True | 银行ETF华夏 | 79.6 | False | 88.7 |  | 004726 | 96.0 | 94.0 | True | 15.24 |  | 170.4 | 3.9 |
| 011796 | open | 2026-11-20 | tr_nav | 0.02 | 0.13 | 2.1 | 2.25 | 3.15 | -0.78 | -0.4 | 6.03 | True | True | 新华中债0-3年政策性金融债指数A | 88.9 | False | 86.9 |  | 004726 | 85.0 | 78.0 | True | 6.09 |  |  |  |
| 005937 | open | 2026-11-20 | tr_nav | 0.45 | 5.11 | 5.52 | 13.63 | 17.7 | -8.08 | -1.06 | 12.81 | True | True | 工银精选金融地产混合A | 79.6 | False | 86.1 |  | 004726 | 87.0 | 90.0 | True | 12.92 |  |  |  |
| 021322 | open | 2026-11-20 | tr_nav | 0.11 | 0.19 | 10.33 | 10.1 | 10.25 | -1.95 | 0.0 | 18.93 | True | True | 百嘉百兴纯债债券C | 92.3 | False | 84.8 |  | 004726 | 91.0 | 82.0 | True | 19.09 |  |  |  |
| 288001 | open | 2026-11-20 | tr_nav | -1.6 | -0.17 | 2.4 | 4.28 | 9.97 | -21.7 | -10.79 | 10.32 | False | False | 华夏经典混合 | 79.7 | False | 84.0 |  | 004726 | 88.0 | 81.0 | True | 10.41 |  |  |  |
| 519655 | open | 2026-11-20 | tr_nav | -0.01 | 4.06 | 2.88 | 10.46 | 11.05 | -13.37 | -1.87 | 14.61 | True | True | 银河服务混合A | 78.8 | False | 79.8 |  | 004726 | 80.0 | 88.0 | True | 14.73 |  |  |  |
| 011911 | open | 2026-11-20 | tr_nav | -6.38 | -1.39 | -0.13 | 4.77 | -2.79 | -19.27 | -6.75 | 20.41 | False | False | 华夏消费优选混合A | 79.9 | False | 74.2 |  | 011911 | 84.0 | 80.0 | True | 20.58 |  |  |  |
| 159980 | etf | 2026-11-20 | adj_close | -7.1 | -10.54 | -11.5 | -12.33 | 4.09 | -16.89 | -16.89 | 14.36 | False | False | 有色ETF大成 | 80.0 | False | 62.2 |  | 004726 | 49.0 | 56.0 | False | 14.48 |  | 899.7 |  |
| 000960 | open | 2026-11-20 | tr_nav | -10.82 | -8.86 | -18.64 | 18.06 | 13.92 | -25.14 | -25.14 | 45.62 | False | False | 招商医药健康产业股票 | 80.6 | False | 54.9 | lottery-like daily jump | 000960 | 62.0 | 87.0 | True | 46.0 |  |  |  |
| 160326 | open | 2026-11-20 | tr_nav | -5.72 | -5.65 | -13.0 | -14.95 | -3.42 | -17.71 | -17.71 | 14.41 | False | False | 华夏优选配置股票(FOF-LOF)A | 81.4 | False | 52.7 |  | 160326 | 29.0 | 47.0 | False | 14.53 |  |  |  |
| 014092 | open | 2026-11-20 | tr_nav | -5.72 | -5.67 | -13.11 | -15.17 | -3.82 | -17.87 | -17.87 | 14.4 | False | False | 华夏优选配置股票(FOF)C | 77.9 | False | 51.3 |  | 160326 | 26.0 | 45.0 | False | 14.52 |  |  |  |
| 011373 | open | 2026-11-20 | tr_nav | -11.77 | -10.52 | -20.86 | 15.43 | 7.79 | -26.66 | -26.66 | 45.75 | False | False | 招商前沿医疗保健股票A | 79.1 | False | 50.9 | lottery-like daily jump | 000960 | 57.0 | 85.0 | False | 46.14 |  |  |  |
| 009477 | open | 2026-11-20 | tr_nav | -8.18 | -10.7 | -20.15 | -21.04 | -17.6 | -37.15 | -37.15 | 21.59 | False | False | 中银上海金ETF联接A | 78.2 | False | 40.6 |  | 009477 | 21.0 | 44.0 | False | 21.77 |  |  |  |

## Theme ETFs

| theme | code | name | r_1w | r_4w | r_12w | off_52w_high | premium_pct | shares_chg_5d_pct | composite | crowded | cluster |
|---|---|---|---|---|---|---|---|---|---|---|---|
| broad_large | 510300 | 沪深300ETF华泰柏瑞 | -1.59 | -3.83 | -13.65 | -21.08 |  | 20.96 | 32.9 |  | 004726 |
| broad_mid | 510500 | 中证500ETF南方 | -6.81 | -11.73 | -23.02 | -32.98 |  | 35.71 | 25.8 |  | 159516 |
| growth_chinext | 159915 | 创业板ETF易方达 | -8.68 | -17.47 | -36.5 | -49.26 |  |  | 12.8 |  | 515050 |
| star_tech | 588000 | 科创50ETF华夏 | -3.99 | -8.58 | -25.46 | -44.54 |  | 0.23 | 28.1 | lottery-like daily jump | 159516 |
| semis | 512480 | 半导体ETF国联安 | -6.05 | -10.89 | -28.3 | -50.42 |  | 2.04 | 29.5 | lottery-like daily jump | 159516 |
| semis | 159995 | 芯片ETF华夏 | -5.68 | -10.45 | -29.28 | -51.98 |  |  | 24.0 | lottery-like daily jump | 159516 |
| ai_compute | 159819 | 人工智能ETF易方达 | -11.29 | -17.1 | -28.27 | -44.4 |  |  | 28.9 | lottery-like daily jump | 515400 |
| ai_compute | 515880 | 通信ETF国泰 | -13.4 | -29.57 | -45.48 | -61.55 |  | 1.21 | 15.1 | lottery-like daily jump | 515050 |
| brokers | 512880 | 证券ETF国泰 | 0.0 | -3.16 | -7.71 | -23.72 |  | -1.98 | 51.3 |  | 512070 |
| banks | 512800 | 银行ETF华宝 | 3.23 | 9.07 | 13.2 | 0.0 |  | -6.67 | 87.1 |  | 004726 |
| dividend | 510880 | 红利ETF华泰柏瑞 | 1.63 | 3.6 | 1.39 | -2.0 |  | -0.24 | 75.3 |  | 004726 |
| gold | 518880 | 黄金ETF华安 | -8.45 | -11.18 | -21.14 | -38.83 |  | -1.72 | 38.9 |  | 009477 |
| gov_bonds | 511010 | 国债ETF国泰 | 0.05 | 0.18 | 0.57 | -0.03 |  | 11.67 | 86.9 |  | 004726 |
| new_energy_ev | 515030 | 新能源车ETF华夏 | -6.41 | -8.74 | -25.2 | -45.0 |  | -1.28 | 19.2 |  | 512580 |
| new_energy_ev | 516160 | 新能源ETF南方 | -7.08 | -8.84 | -26.91 | -46.05 |  | -2.76 | 16.6 |  | 512580 |
| solar | 515790 | 光伏ETF华泰柏瑞 | -9.03 | -11.44 | -25.21 | -46.32 |  | -2.85 | 19.2 |  | 515790 |
| healthcare | 512010 | 医药ETF易方达 | -1.84 | -0.53 | -6.5 | -9.0 |  | -1.04 | 66.2 |  | 512010 |
| healthcare | 512170 | 医疗ETF华宝 | -5.01 | -3.59 | -10.31 | -17.44 |  | 0.88 | 60.1 |  | 512010 |
| consumer | 159928 | 消费ETF汇添富 | 0.28 | 6.18 | 5.23 | -17.47 |  |  | 73.7 |  | 004726 |
| consumer | 512690 | 酒ETF鹏华 | -2.05 | 3.86 | 1.17 | -29.0 |  | -2.98 | 62.2 |  | 011911 |
| defense | 512660 | 军工ETF国泰 | -10.49 | -15.55 | -18.32 | -46.73 |  | -3.86 | 35.1 |  | 159638 |
| real_estate | 512200 | 房地产ETF南方 | -8.75 | -13.29 | -17.06 | -38.8 |  | -12.28 | 43.6 |  | 512200 |

## Base rates for p_up

How often a fund in each composite band beat the CSI 300 over the next 4 weeks in the backtest. Start each call's p_up here. Watchlist themes and their products: themes.md.

| composite_band | fund_weeks | beat_csi300_pct | avg_excess_4w_pct |
|---|---|---|---|
| all | 20283 | 49.7 | 0.32 |
| 0-20 | 770 | 47.1 | 0.27 |
| 20-40 | 5597 | 47.6 | 0.15 |
| 40-60 | 7095 | 49.4 | 0.37 |
| 60-80 | 5227 | 51.0 | 0.4 |
| 80-100 | 1594 | 55.6 | 0.41 |
