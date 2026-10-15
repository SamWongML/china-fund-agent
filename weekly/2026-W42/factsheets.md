# Fact sheets 2026-W42 (data as of 2026-10-16, built 2026-10-16 00:58 HKT)

Data ready: **True** (last good fund snapshot 2026-10-15; missing history: none).

Returns in %: r_1w=5 trading days, r_4w=20, r_12w=60, r_26w=120, r_52w=250. Prices are adjusted for splits and dividends (ETF/LOF) or total-return NAV (open funds); basis says which. pnl_pct uses the raw latest price.

Signals: composite = 0-100 weighted percentile of the live signals (trend, reversal, lottery, crowding, low volatility) across ~60 sector and broad ETFs plus holdings and candidates; higher is better. crowded = reasons not to add now. cluster = the highest-ranked fund it moves with (60-day correlation of market-relative returns above the threshold); funds sharing a cluster are one bet. Details: journal/signal_health.md.

## Market regime: **risk-off**

| label | score | votes | sh000300_ma200_gap_pct | sh000300_r_12w_pct | sh000905_ma200_gap_pct | sh000905_r_12w_pct | breadth_above_ma200_pct | breadth_n |
|---|---|---|---|---|---|---|---|---|
| risk-off | 0.0 | 5 | -11.01 | -12.97 | -15.91 | -16.92 | 15.7 | 51 |

Signal weight multipliers from the backtest: {'trend_12w': 0.0, 'trend_26w': 0.5, 'ma200_gap': 0.5, 'rev_1w': 0.0, 'rev_4w': 0.0, 'max_20d': 0.5, 'turnover_surge': 0.5, 'low_vol': 0.5}. Backtest status: {'trend_12w': 'rejected', 'trend_26w': 'unproven', 'ma200_gap': 'unproven', 'rev_1w': 'rejected', 'rev_4w': 'rejected', 'max_20d': 'unproven', 'turnover_surge': 'unproven', 'low_vol': 'unproven', 'legacy_screen': 'unproven'}.

## Holdings

_none_

## Rules-only calls (the baseline your calls are graded against)

Target weights: core {'511010': 25.0, '510880': 16.3, '510300': 15.4, '518880': 13.3}, satellite {}, unallocated 30.0%. risk-off regime: satellite sleeve left unallocated (hold bonds or cash)

| code | action | current_weight_pct | target_weight_pct | reason | name | composite | crowded | cluster |
|---|---|---|---|---|---|---|---|---|
| 511010 | buy | 0.0 | 25.0 | core sleeve | 国债ETF国泰 | 75.8 | turnover surge | 012111 |
| 510880 | buy | 0.0 | 16.3 | core sleeve | 红利ETF华泰柏瑞 | 75.4 |  | 012111 |
| 510300 | buy | 0.0 | 15.4 | core sleeve | 沪深300ETF华泰柏瑞 | 55.1 |  | 012111 |
| 518880 | buy | 0.0 | 13.3 | core sleeve | 黄金ETF华安 | 47.1 |  | 518880 |

## Candidates (pre-screened, not held)

| code | kind | last_date | basis | r_1w | r_4w | r_12w | r_26w | r_52w | max_dd_52w | off_52w_high | vol_60d_ann | above_ma20 | above_ma60 | name | screen_score | chase_warning | composite | crowded | cluster | trend_12w_rank | trend_26w_rank | above_ma200 | vol60_pct | premium_pct | turnover_cny_m |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 012111 | open | 2026-10-15 | tr_nav | -0.79 | -1.14 | 1.07 | 6.41 | 7.58 | -3.65 | -1.81 | 6.13 | False | False | 鹏华安颐混合A | 85.3 | False | 94.8 |  | 012111 | 82.0 | 99.0 | True | 6.18 |  |  |
| 009763 | open | 2026-10-15 | tr_nav | -3.07 | -3.37 | 0.68 | 4.63 | 5.17 | -7.68 | -4.55 | 10.21 | False | False | 惠升和悦债券A | 92.2 | False | 91.9 |  | 012111 | 86.0 | 98.0 | True | 10.29 |  |  |
| 024962 | open | 2026-10-15 | tr_nav | -0.6 | -1.29 | 1.28 | 2.68 |  | -1.4 | -1.4 | 4.94 | False | False | 宏利集享债券A | 85.4 | False | 91.3 |  | 012111 | 87.0 | 90.0 | True | 4.98 |  |  |
| 010630 | open | 2026-10-15 | tr_nav | -1.13 | -1.34 | 1.91 | 1.66 | 4.22 | -3.39 | -2.11 | 5.8 | False | False | 惠升和睿兴利债券A | 84.8 | False | 86.2 |  | 012111 | 98.0 | 82.0 | True | 5.85 |  |  |
| 005957 | open | 2026-10-13 | tr_nav | -0.18 | -1.04 | 0.77 | 0.68 | 1.69 | -4.09 | -1.77 | 5.23 | False | True | 华夏聚丰混合(FOF)A | 73.6 | False | 82.3 |  | 012111 | 67.0 | 71.0 | True | 5.08 |  |  |
| 001715 | open | 2026-10-15 | tr_nav | -1.24 | -7.91 | 5.95 | 30.17 | 59.93 | -14.24 | -7.91 | 26.82 | False | True | 工银新焦点混合A | 85.0 | False | 73.3 |  | 001715 | 78.0 | 100.0 | True | 27.05 |  |  |
| 001849 | open | 2026-10-15 | tr_nav | -6.67 | -6.04 | 1.33 | 6.97 | 21.3 | -12.83 | -9.91 | 26.56 | False | False | 前海开源强势共识100强股票 | 79.7 | False | 71.6 |  | 001849 | 84.0 | 87.0 | True | 26.78 |  |  |
| 002495 | open | 2026-10-15 | tr_nav | -6.0 | -6.84 | 2.08 | 3.93 | 19.76 | -14.18 | -8.15 | 27.25 | False | False | 前海开源量化优选A | 81.5 | False | 69.1 |  | 001849 | 83.0 | 84.0 | True | 27.48 |  |  |
| 005437 | open | 2026-10-15 | tr_nav | -4.66 | -4.85 | 2.49 | 1.92 | 15.38 | -16.25 | -6.84 | 30.64 | False | False | 易方达易百智能量化策略A | 79.4 | False | 64.8 |  | 005437 | 76.0 | 74.0 | True | 30.89 |  |  |
| 161724 | open | 2026-10-15 | tr_nav | -4.35 | -8.43 | 5.5 | 6.36 | 20.94 | -24.54 | -13.27 | 30.73 | False | False | 招商中证煤炭等权指数(LOF)A | 83.5 | False | 64.7 |  | 161724 | 85.0 | 78.0 | True | 30.99 |  |  |
| 001420 | open | 2026-10-15 | tr_nav | -5.47 | -4.19 | 10.01 | -2.81 | 11.17 | -24.27 | -8.88 | 25.73 | False | True | 南方大数据300A | 80.6 | False | 63.2 |  | 001420 | 99.0 | 67.0 | True | 25.95 |  |  |
| 008602 | open | 2026-10-15 | tr_nav | -8.77 | -13.08 | 5.27 | 19.75 | 31.79 | -19.8 | -19.8 | 37.43 | False | False | 方正富邦新兴成长混合A | 92.1 | False | 62.3 |  | 008602 | 90.0 | 97.0 | True | 37.75 |  |  |
| 022490 | open | 2026-10-15 | tr_nav | -6.78 | -10.09 | -5.45 | -1.0 | 9.39 | -15.81 | -13.1 | 29.62 | False | False | 华商恒鑫回报混合A | 83.0 | False | 60.9 |  | 022490 | 66.0 | 73.0 | False | 29.87 |  |  |
| 159985 | etf | 2026-10-15 | adj_close | -1.59 | -6.68 | 0.13 | 5.83 | 13.92 | -14.69 | -8.85 | 27.27 | False | False | 豆粕ETF华夏 | 87.6 | False | 60.7 |  | 159985 | 71.0 | 75.0 | True | 27.5 |  | 269.5 |
| 011373 | open | 2026-10-15 | tr_nav | -9.41 | -0.9 | 11.99 | 24.77 | 18.08 | -24.63 | -12.22 | 49.02 | False | True | 招商前沿医疗保健股票A | 87.0 | False | 58.8 |  | 011373 | 96.0 | 95.0 | True | 49.43 |  |  |
| 000960 | open | 2026-10-15 | tr_nav | -8.59 | 0.39 | 10.53 | 26.66 | 25.93 | -22.62 | -12.47 | 49.29 | False | True | 招商医药健康产业股票 | 86.6 | False | 57.5 |  | 011373 | 91.0 | 93.0 | True | 49.7 |  |  |
| 009360 | open | 2026-10-15 | tr_nav | -9.62 | -1.9 | 10.56 | 21.06 | 13.4 | -25.51 | -12.93 | 50.21 | False | True | 招商创新增长混合A | 86.6 | False | 56.5 |  | 011373 | 95.0 | 92.0 | True | 50.64 |  |  |
| 012186 | open | 2026-10-15 | tr_nav | -9.54 | -1.61 | 10.92 | 21.48 | 13.78 | -25.73 | -13.48 | 51.45 | False | True | 招商品质成长混合A | 86.6 | False | 55.0 |  | 011373 | 93.0 | 91.0 | True | 51.88 |  |  |
| 515220 | etf | 2026-10-15 | adj_close | -2.27 | -6.79 | 5.4 | 4.34 | 19.41 | -25.38 | -12.59 | 31.87 | False | False | 煤炭ETF国泰 | 80.0 | False | 53.8 |  | 161724 | 77.0 | 68.0 | True | 32.13 |  | 1107.3 |
| 159981 | etf | 2026-10-15 | adj_close | -5.47 | 4.27 | 22.15 | 10.5 | 40.31 | -23.52 | -5.47 | 35.22 | True | True | 能源化工ETF建信 | 89.5 | False | 48.1 | lottery-like daily jump | 159981 | 100.0 | 80.0 | True | 35.51 |  | 596.6 |

## Theme ETFs

| theme | code | name | r_1w | r_4w | r_12w | off_52w_high | premium_pct | shares_chg_5d_pct | composite | crowded | cluster |
|---|---|---|---|---|---|---|---|---|---|---|---|
| broad_large | 510300 | 沪深300ETF华泰柏瑞 | -3.35 | -8.52 | -12.32 | -16.68 |  |  | 55.1 |  | 012111 |
| broad_mid | 510500 | 中证500ETF南方 | -6.55 | -12.63 | -16.55 | -24.68 |  |  | 43.3 |  | 159516 |
| growth_chinext | 159915 | 创业板ETF易方达 | -8.09 | -16.81 | -26.7 | -36.15 |  |  | 31.5 |  | 159819 |
| star_tech | 588000 | 科创50ETF华夏 | -6.44 | -13.94 | -29.09 | -38.65 |  |  | 34.7 |  | 159516 |
| semis | 512480 | 半导体ETF国联安 | -8.1 | -14.55 | -31.82 | -44.09 |  |  | 44.9 |  | 159516 |
| semis | 159995 | 芯片ETF华夏 | -8.16 | -16.09 | -33.93 | -45.55 |  |  | 45.5 |  | 159516 |
| ai_compute | 159819 | 人工智能ETF易方达 | -9.74 | -15.99 | -28.78 | -35.26 |  |  | 47.7 |  | 159819 |
| ai_compute | 515880 | 通信ETF国泰 | -12.29 | -23.04 | -31.36 | -44.66 |  |  | 31.7 |  | 159819 |
| brokers | 512880 | 证券ETF国泰 | 2.87 | -4.24 | -8.05 | -19.58 |  |  | 58.8 |  | 512000 |
| banks | 512800 | 银行ETF华宝 | 0.47 | 2.49 | 9.24 | -0.58 |  |  | 70.5 |  | 012111 |
| dividend | 510880 | 红利ETF华泰柏瑞 | -0.29 | -2.63 | 6.94 | -2.66 |  |  | 75.4 |  | 012111 |
| gold | 518880 | 黄金ETF华安 | -0.02 | -6.29 | 1.23 | -28.83 |  |  | 47.1 |  | 518880 |
| gov_bonds | 511010 | 国债ETF国泰 | 0.14 | 0.22 | 0.5 | 0.0 |  |  | 75.8 | turnover surge | 012111 |
| new_energy_ev | 515030 | 新能源车ETF华夏 | -6.91 | -12.58 | -16.84 | -38.78 |  |  | 34.8 |  | 512580 |
| new_energy_ev | 516160 | 新能源ETF南方 | -7.34 | -12.36 | -16.9 | -38.81 |  |  | 36.0 |  | 512580 |
| solar | 515790 | 光伏ETF华泰柏瑞 | -6.42 | -12.61 | -16.0 | -39.64 |  |  | 35.9 |  | 515790 |
| healthcare | 512010 | 医药ETF易方达 | -1.31 | 0.8 | -0.53 | -15.85 |  |  | 63.3 |  | 512010 |
| healthcare | 512170 | 医疗ETF华宝 | -2.95 | -2.37 | -0.9 | -16.5 |  |  | 52.8 |  | 512010 |
| consumer | 159928 | 消费ETF汇添富 | 1.07 | -2.8 | 0.61 | -22.63 |  |  | 46.8 |  | 012111 |
| consumer | 512690 | 酒ETF鹏华 | 0.0 | -2.11 | 0.24 | -31.3 |  |  | 49.9 |  | 512010 |
| defense | 512660 | 军工ETF国泰 | -5.84 | -12.63 | -9.8 | -38.7 |  |  | 36.2 |  | 001715 |
| real_estate | 512200 | 房地产ETF南方 | -8.61 | -4.77 | -1.42 | -28.82 |  |  | 35.5 |  | 512200 |

## Base rates for p_up

How often a fund in each composite band beat the CSI 300 over the next 4 weeks in the backtest. Start each call's p_up here. Watchlist themes and their products: themes.md.

| composite_band | fund_weeks | beat_csi300_pct | avg_excess_4w_pct |
|---|---|---|---|
| all | 19976 | 49.3 | 0.28 |
| 0-20 | 458 | 49.8 | 0.81 |
| 20-40 | 4555 | 47.6 | 0.18 |
| 40-60 | 9306 | 48.7 | 0.38 |
| 60-80 | 4577 | 51.1 | 0.17 |
| 80-100 | 1080 | 54.6 | 0.14 |
