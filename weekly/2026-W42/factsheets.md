# Fact sheets 2026-W42 (data as of 2026-10-16, built 2026-10-18 08:08 HKT)

Data ready: **True** (last good fund snapshot 2026-10-16; missing history: none).

Returns in %: r_1w=5 trading days, r_4w=20, r_12w=60, r_26w=120, r_52w=250. Prices are adjusted for splits and dividends (ETF/LOF) or total-return NAV (open funds); basis says which. pnl_pct uses the raw latest price.

Signals: composite = 0-100 weighted percentile of the live signals (trend, reversal, lottery, crowding, low volatility) across ~60 sector and broad ETFs plus holdings and candidates; higher is better. crowded = reasons not to add now. cluster = the highest-ranked fund it moves with (60-day correlation of market-relative returns above the threshold); funds sharing a cluster are one bet. Details: journal/signal_health.md.

## Market regime: **risk-off**

| label | score | votes | sh000300_ma200_gap_pct | sh000300_r_12w_pct | sh000905_ma200_gap_pct | sh000905_r_12w_pct | breadth_above_ma200_pct | breadth_n |
|---|---|---|---|---|---|---|---|---|
| risk-off | 0.0 | 5 | -10.87 | -11.23 | -15.85 | -14.87 | 13.7 | 51 |

Signal weight multipliers from the backtest: {'trend_12w': 0.5, 'trend_26w': 0.5, 'ma200_gap': 0.5, 'rev_1w': 0.0, 'rev_4w': 0.0, 'max_20d': 0.5, 'turnover_surge': 0.5, 'low_vol': 0.5}. Backtest status: {'trend_12w': 'unproven', 'trend_26w': 'unproven', 'ma200_gap': 'unproven', 'rev_1w': 'rejected', 'rev_4w': 'rejected', 'max_20d': 'unproven', 'turnover_surge': 'unproven', 'low_vol': 'unproven', 'legacy_screen': 'unproven'}.

## Holdings

_none_

## Rules-only calls (the baseline your calls are graded against)

Target weights: core {'511010': 25.0, '510880': 16.3, '510300': 15.6, '518880': 13.1}, satellite {}, unallocated 30.0%. risk-off regime: satellite sleeve left unallocated (hold bonds or cash)

| code | action | current_weight_pct | target_weight_pct | reason | name | composite | crowded | cluster |
|---|---|---|---|---|---|---|---|---|
| 511010 | buy | 0.0 | 25.0 | core sleeve | 国债ETF国泰 | 75.6 | turnover surge | 012111 |
| 510880 | buy | 0.0 | 16.3 | core sleeve | 红利ETF华泰柏瑞 | 81.8 |  | 012111 |
| 510300 | buy | 0.0 | 15.6 | core sleeve | 沪深300ETF华泰柏瑞 | 38.4 |  | 012111 |
| 518880 | buy | 0.0 | 13.1 | core sleeve | 黄金ETF华安 | 54.6 |  | 518880 |

## Candidates (pre-screened, not held)

| code | kind | last_date | basis | r_1w | r_4w | r_12w | r_26w | r_52w | max_dd_52w | off_52w_high | vol_60d_ann | above_ma20 | above_ma60 | name | screen_score | chase_warning | composite | crowded | cluster | trend_12w_rank | trend_26w_rank | above_ma200 | vol60_pct | premium_pct | turnover_cny_m |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 012111 | open | 2026-10-16 | tr_nav | -0.74 | -0.86 | 1.55 | 6.54 | 8.07 | -3.65 | -1.66 | 6.09 | False | False | 鹏华安颐混合A | 85.8 | False | 91.0 |  | 012111 | 82.0 | 100.0 | True | 6.15 |  |  |
| 010630 | open | 2026-10-16 | tr_nav | -1.62 | -1.48 | 2.06 | 1.55 | 4.04 | -3.39 | -2.38 | 5.76 | False | False | 惠升和睿兴利债券A | 83.6 | False | 91.0 |  | 012111 | 98.0 | 85.0 | True | 5.8 |  |  |
| 009763 | open | 2026-10-16 | tr_nav | -3.43 | -3.41 | 0.71 | 3.54 | 5.09 | -7.68 | -4.87 | 10.2 | False | False | 惠升和悦债券A | 89.9 | False | 90.6 |  | 012111 | 86.0 | 99.0 | True | 10.29 |  |  |
| 161724 | open | 2026-10-16 | tr_nav | -4.6 | -6.94 | 8.68 | 8.79 | 21.76 | -24.54 | -12.65 | 30.37 | False | False | 招商中证煤炭等权指数(LOF)A | 83.4 | False | 75.3 |  | 161724 | 93.0 | 80.0 | True | 30.63 |  |  |
| 002495 | open | 2026-10-16 | tr_nav | -4.77 | -4.16 | 4.85 | 4.23 | 21.05 | -14.18 | -7.28 | 27.07 | False | False | 前海开源量化优选A | 82.1 | False | 73.2 |  | 002495 | 80.0 | 82.0 | True | 27.3 |  |  |
| 008279 | open | 2026-10-16 | tr_nav | -2.34 | -3.72 | 9.36 | 7.99 | 22.1 | -23.94 | -10.12 | 29.15 | False | True | 国泰中证煤炭ETF联接A | 80.4 | False | 72.4 |  | 161724 | 85.0 | 76.0 | True | 29.39 |  |  |
| 005437 | open | 2026-10-16 | tr_nav | -4.63 | -3.05 | 4.28 | 1.7 | 16.74 | -16.25 | -6.36 | 30.54 | False | True | 易方达易百智能量化策略A | 80.8 | False | 70.3 |  | 005437 | 79.0 | 75.0 | True | 30.8 |  |  |
| 011373 | open | 2026-10-16 | tr_nav | -11.33 | -2.18 | 10.03 | 24.24 | 16.27 | -24.63 | -15.28 | 49.44 | False | False | 招商前沿医疗保健股票A | 89.5 | False | 69.8 |  | 011373 | 95.0 | 95.0 | True | 49.86 |  |  |
| 008602 | open | 2026-10-16 | tr_nav | -7.83 | -12.82 | 5.55 | 17.96 | 31.42 | -20.13 | -20.13 | 37.41 | False | False | 方正富邦新兴成长混合A | 92.4 | False | 69.3 |  | 008602 | 84.0 | 96.0 | True | 37.73 |  |  |
| 159985 | etf | 2026-10-16 | adj_close | -3.95 | -3.99 | 2.98 | 5.64 | 13.55 | -14.69 | -9.75 | 26.21 | False | False | 豆粕ETF华夏 | 92.2 | False | 68.6 |  | 159985 | 78.0 | 79.0 | True | 26.43 |  | 255.7 |
| 013835 | open | 2026-10-16 | tr_nav | 0.15 | 222.46 | 222.97 | 223.52 | 226.61 | -0.31 | 0.0 | 236.35 | True | True | 中加优享纯债债券C | 88.9 | False | 68.3 | lottery-like daily jump | 013835 | 100.0 | 97.0 | True | 238.34 |  |  |
| 009360 | open | 2026-10-16 | tr_nav | -11.3 | -2.95 | 8.76 | 20.3 | 11.81 | -25.51 | -15.77 | 50.57 | False | False | 招商创新增长混合A | 88.8 | False | 67.0 |  | 011373 | 92.0 | 90.0 | True | 51.0 |  |  |
| 000960 | open | 2026-10-16 | tr_nav | -10.95 | -1.4 | 8.07 | 24.37 | 22.89 | -22.62 | -16.0 | 49.88 | False | False | 招商医药健康产业股票 | 90.5 | False | 66.7 |  | 011373 | 88.0 | 93.0 | True | 50.3 |  |  |
| 012186 | open | 2026-10-16 | tr_nav | -11.28 | -2.55 | 9.06 | 20.71 | 12.21 | -25.73 | -16.33 | 51.81 | False | False | 招商品质成长混合A | 88.9 | False | 65.7 |  | 011373 | 90.0 | 89.0 | True | 52.25 |  |  |
| 000598 | open | 2026-10-16 | tr_nav | -3.13 | -2.22 | 1.23 | 2.19 | 26.59 | -31.89 | -17.5 | 39.52 | False | True | 长盛生态环境混合A | 79.5 | False | 65.5 |  | 005437 | 71.0 | 68.0 | True | 39.85 |  |  |
| 515220 | etf | 2026-10-16 | adj_close | -2.54 | -4.09 | 9.15 | 7.29 | 21.4 | -25.38 | -11.54 | 31.56 | False | True | 煤炭ETF国泰 | 80.5 | False | 65.1 |  | 161724 | 83.0 | 73.0 | True | 31.82 |  | 414.7 |
| 159981 | etf | 2026-10-16 | adj_close | -4.77 | 3.79 | 23.47 | 10.6 | 41.34 | -23.52 | -5.21 | 35.14 | True | True | 能源化工ETF建信 | 89.8 | False | 64.2 | lottery-like daily jump | 159981 | 99.0 | 84.0 | True | 35.44 |  | 596.5 |
| 000711 | open | 2026-10-16 | tr_nav | -8.51 | -2.54 | -0.04 | 16.41 | 6.93 | -24.45 | -13.34 | 43.32 | False | False | 嘉实医疗保健股票 | 81.1 | False | 64.1 |  | 011373 | 75.0 | 86.0 | True | 43.69 |  |  |
| 160326 | open | 2026-10-16 | tr_nav | -2.11 | -6.53 | -6.33 | -3.08 | 3.92 | -12.09 | -11.82 | 14.75 | False | False | 华夏优选配置股票(FOF-LOF)A | 77.7 | False | 61.1 |  | 012111 | 25.0 | 72.0 | False | 14.88 |  |  |
| 014092 | open | 2026-10-16 | tr_nav | -2.13 | -6.59 | -6.47 | -3.31 | 3.5 | -12.23 | -11.97 | 14.75 | False | False | 华夏优选配置股票(FOF)C | 74.5 | False | 60.7 |  | 012111 | 24.0 | 71.0 | False | 14.87 |  |  |

## Theme ETFs

| theme | code | name | r_1w | r_4w | r_12w | off_52w_high | premium_pct | shares_chg_5d_pct | composite | crowded | cluster |
|---|---|---|---|---|---|---|---|---|---|---|---|
| broad_large | 510300 | 沪深300ETF华泰柏瑞 | -3.4 | -8.25 | -10.88 | -16.79 |  |  | 38.4 |  | 012111 |
| broad_mid | 510500 | 中证500ETF南方 | -6.5 | -12.05 | -14.42 | -24.61 |  |  | 40.5 |  | 159516 |
| growth_chinext | 159915 | 创业板ETF易方达 | -8.98 | -16.94 | -25.09 | -36.54 |  |  | 23.1 |  | 159363 |
| star_tech | 588000 | 科创50ETF华夏 | -7.2 | -13.8 | -26.48 | -38.99 |  |  | 27.5 |  | 159516 |
| semis | 512480 | 半导体ETF国联安 | -8.45 | -14.55 | -28.04 | -44.49 |  |  | 35.3 |  | 159516 |
| semis | 159995 | 芯片ETF华夏 | -8.21 | -16.26 | -30.37 | -45.9 |  |  | 34.0 |  | 159516 |
| ai_compute | 159819 | 人工智能ETF易方达 | -9.84 | -14.83 | -26.92 | -35.17 |  |  | 36.0 |  | 159363 |
| ai_compute | 515880 | 通信ETF国泰 | -11.82 | -22.21 | -28.69 | -44.56 |  |  | 30.3 |  | 159363 |
| brokers | 512880 | 证券ETF国泰 | -0.48 | -5.59 | -7.46 | -20.28 |  |  | 45.2 |  | 512880 |
| banks | 512800 | 银行ETF华宝 | 1.65 | 1.29 | 10.49 | -0.46 |  |  | 78.0 |  | 012111 |
| dividend | 510880 | 红利ETF华泰柏瑞 | -0.03 | -1.24 | 9.03 | -1.97 |  |  | 81.8 |  | 012111 |
| gold | 518880 | 黄金ETF华安 | -0.73 | -5.82 | 2.28 | -28.14 |  |  | 54.6 |  | 518880 |
| gov_bonds | 511010 | 国债ETF国泰 | 0.17 | 0.29 | 0.57 | 0.0 |  |  | 75.6 | turnover surge | 012111 |
| new_energy_ev | 515030 | 新能源车ETF华夏 | -9.02 | -11.71 | -16.18 | -39.06 |  |  | 32.2 |  | 512580 |
| new_energy_ev | 516160 | 新能源ETF南方 | -8.23 | -12.06 | -14.92 | -38.99 |  |  | 33.7 |  | 512580 |
| solar | 515790 | 光伏ETF华泰柏瑞 | -6.27 | -11.26 | -13.2 | -39.39 |  |  | 33.9 |  | 512580 |
| healthcare | 512010 | 医药ETF易方达 | -3.42 | -0.54 | -2.91 | -18.08 |  |  | 62.5 |  | 512010 |
| healthcare | 512170 | 医疗ETF华宝 | -5.57 | -3.3 | -3.3 | -18.27 |  |  | 57.3 |  | 011373 |
| consumer | 159928 | 消费ETF汇添富 | 0.91 | 0.0 | 0.3 | -21.81 |  |  | 51.2 |  | 012111 |
| consumer | 512690 | 酒ETF鹏华 | 0.48 | 0.72 | 0.24 | -30.64 |  |  | 52.1 |  | 512010 |
| defense | 512660 | 军工ETF国泰 | -2.13 | -10.25 | -5.45 | -37.04 |  |  | 37.7 |  | 159227 |
| real_estate | 512200 | 房地产ETF南方 | -6.08 | -1.47 | -0.41 | -27.19 |  |  | 47.9 |  | 512200 |

## Base rates for p_up

How often a fund in each composite band beat the CSI 300 over the next 4 weeks in the backtest. Start each call's p_up here. Watchlist themes and their products: themes.md.

| composite_band | fund_weeks | beat_csi300_pct | avg_excess_4w_pct |
|---|---|---|---|
| all | 19976 | 49.5 | 0.3 |
| 0-20 | 433 | 50.1 | 0.54 |
| 20-40 | 5219 | 47.2 | 0.14 |
| 40-60 | 8026 | 49.6 | 0.46 |
| 60-80 | 5184 | 50.5 | 0.25 |
| 80-100 | 1114 | 54.7 | 0.11 |
