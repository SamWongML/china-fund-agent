# Fact sheets 2026-W45 (data as of 2026-11-06, built 2026-11-08 09:31 HKT)

Data ready: **True** (last good fund snapshot 2026-11-06; missing history: none).

Returns in %: r_1w=5 trading days, r_4w=20, r_12w=60, r_26w=120, r_52w=250. Prices are adjusted for splits and dividends (ETF/LOF) or total-return NAV (open funds); basis says which. pnl_pct uses the raw latest price.

Signals: composite = 0-100 weighted percentile of the live signals (trend, reversal, lottery, crowding, low volatility) across ~60 sector and broad ETFs plus holdings and candidates; higher is better. crowded = reasons not to add now. cluster = the highest-ranked fund it moves with (60-day correlation of market-relative returns above the threshold); funds sharing a cluster are one bet. Details: journal/signal_health.md.

## Market regime: **risk-off**

| label | score | votes | sh000300_ma200_gap_pct | sh000300_r_12w_pct | sh000905_ma200_gap_pct | sh000905_r_12w_pct | breadth_above_ma200_pct | breadth_n |
|---|---|---|---|---|---|---|---|---|
| risk-off | 0.0 | 5 | -12.57 | -12.84 | -17.44 | -15.74 | 21.6 | 51 |

Signal weight multipliers from the backtest: {'trend_12w': 0.5, 'trend_26w': 0.5, 'ma200_gap': 0.5, 'rev_1w': 0.0, 'rev_4w': 0.0, 'max_20d': 0.5, 'turnover_surge': 0.0, 'low_vol': 0.5}. Backtest status: {'trend_12w': 'unproven', 'trend_26w': 'unproven', 'ma200_gap': 'unproven', 'rev_1w': 'rejected', 'rev_4w': 'rejected', 'max_20d': 'unproven', 'turnover_surge': 'rejected', 'low_vol': 'unproven', 'legacy_screen': 'unproven'}.

## Holdings

_none_

## Rules-only calls (the baseline your calls are graded against)

Target weights: core {'511010': 25.0, '510880': 16.0, '510300': 17.3, '518880': 11.7}, satellite {}, unallocated 30.0%. risk-off regime: satellite sleeve left unallocated (hold bonds or cash)

| code | action | current_weight_pct | target_weight_pct | reason | name | composite | crowded | cluster |
|---|---|---|---|---|---|---|---|---|
| 511010 | buy | 0.0 | 25.0 | core sleeve |  | 89.3 |  | 004726 |
| 510880 | buy | 0.0 | 16.0 | core sleeve | 红利ETF华泰柏瑞 | 81.9 |  | 004726 |
| 510300 | buy | 0.0 | 17.3 | core sleeve | 沪深300ETF华泰柏瑞 | 34.1 | turnover surge | 004726 |
| 518880 | buy | 0.0 | 11.7 | core sleeve | 黄金ETF华安 | 49.9 |  | 009477 |

## Candidates (pre-screened, not held)

| code | kind | last_date | basis | r_1w | r_4w | r_12w | r_26w | r_52w | max_dd_52w | off_52w_high | vol_60d_ann | above_ma20 | above_ma60 | name | screen_score | chase_warning | composite | crowded | cluster | trend_12w_rank | trend_26w_rank | above_ma200 | vol60_pct | premium_pct | turnover_cny_m | shares_chg_5d_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 004726 | open | 2026-11-06 | tr_nav | -0.28 | 1.09 | 5.81 | 29.29 | 34.01 | -19.35 | -0.46 | 7.69 | True | True | 先锋聚优A | 88.8 | False | 97.3 |  | 004726 | 99.0 | 100.0 | True | 7.76 |  |  |  |
| 002849 | open | 2026-11-06 | tr_nav | 0.53 | 2.13 | 6.33 | 12.8 | 14.66 | -7.31 | 0.0 | 7.65 | True | True | 金信智能中国2025混合A | 85.8 | False | 95.0 |  | 004726 | 96.0 | 99.0 | True | 7.71 |  |  |  |
| 008420 | open | 2026-11-06 | tr_nav | 0.04 | 0.31 | 2.26 | 3.54 | 5.87 | -2.87 | -0.18 | 3.36 | True | True | 广发招泰A | 86.5 | False | 93.4 |  | 004726 | 93.0 | 98.0 | True | 3.39 |  |  |  |
| 008298 | open | 2026-11-06 | tr_nav | -1.54 | 3.29 | 9.14 | 12.98 | 6.67 | -12.78 | -1.54 | 13.69 | True | True | 华夏中证银行ETF联接A | 89.4 | False | 90.8 |  | 004726 | 98.0 | 96.0 | True | 13.81 |  |  |  |
| 320018 | open | 2026-11-06 | tr_nav | -1.53 | 3.53 | 8.64 | 6.67 | 8.42 | -16.15 | -1.53 | 10.86 | True | True | 诺安新动力灵活配置混合A | 85.6 | False | 90.8 |  | 004726 | 100.0 | 88.0 | True | 10.95 |  |  |  |
| 022233 | open | 2026-11-06 | tr_nav | 0.24 | 0.5 | 3.28 | 3.11 | 3.92 | -1.55 | -0.04 | 4.94 | True | True | 鹏华双债增利债券D | 86.9 | False | 90.3 |  | 004726 | 91.0 | 87.0 | True | 4.98 |  |  |  |
| 004597 | open | 2026-11-06 | tr_nav | -1.52 | 3.28 | 9.11 | 13.01 | 6.48 | -13.0 | -1.52 | 13.71 | True | True | 南方中证银行ETF发起联接A | 89.2 | False | 89.7 |  | 004726 | 97.0 | 95.0 | True | 13.82 |  |  |  |
| 515020 | etf | 2026-11-06 | adj_close | -1.77 | 3.01 | 9.22 | 13.15 | 6.86 | -13.05 | -1.77 | 14.89 | True | True | 银行ETF华夏 | 89.5 | False | 88.9 |  | 004726 | 95.0 | 94.0 | True | 15.01 | 0.13 | 186.0 | 3.49 |
| 005937 | open | 2026-11-06 | tr_nav | -0.83 | 1.55 | 6.65 | 9.05 | 15.64 | -8.08 | -0.86 | 12.66 | True | True | 工银精选金融地产混合A | 88.2 | False | 87.9 |  | 004726 | 90.0 | 91.0 | True | 12.77 |  |  |  |
| 011796 | open | 2026-11-06 | tr_nav | 0.07 | 0.13 | 1.96 | 2.39 | 3.19 | -0.78 | -0.44 | 6.05 | True | True | 新华中债0-3年政策性金融债指数A | 88.5 | False | 87.2 |  | 004726 | 85.0 | 83.0 | True | 6.1 |  |  |  |
| 014259 | open | 2026-11-06 | tr_nav | 0.03 | 9.96 | 10.34 | 11.03 | 12.39 | -0.17 | 0.0 | 18.93 | True | True | 百嘉百兴纯债债券A | 89.6 | False | 76.4 | lottery-like daily jump | 004726 | 88.0 | 89.0 | True | 19.09 |  |  |  |
| 009213 | open | 2026-11-05 | tr_nav | 0.09 | -0.15 | -0.26 | -0.16 | 3.57 | -2.24 | -1.8 | 1.92 | True | False | 易方达如意安泰(FOF)A | 81.3 | False | 75.3 |  | 004726 | 55.0 | 74.0 | True | 1.93 |  |  |  |
| 008168 | open | 2026-11-04 | tr_nav | -0.35 | -3.63 | -2.93 | -3.07 | 15.85 | -11.18 | -9.74 | 10.24 | False | False | 汇添富聚焦成长三个月混合FOF | 87.5 | False | 66.4 |  | 004726 | 39.0 | 71.0 | False | 9.88 |  |  |  |
| 000711 | open | 2026-11-06 | tr_nav | 4.51 | -4.22 | 9.01 | 24.15 | 15.49 | -22.54 | -9.28 | 43.43 | True | False | 嘉实医疗保健股票 | 86.2 | False | 64.5 | lottery-like daily jump | 000711 | 79.0 | 82.0 | True | 43.79 |  |  |  |
| 000960 | open | 2026-11-06 | tr_nav | 4.4 | -7.97 | 13.28 | 30.62 | 30.84 | -22.62 | -13.19 | 50.37 | True | False | 招商医药健康产业股票 | 89.0 | False | 64.0 | lottery-like daily jump | 000711 | 83.0 | 86.0 | True | 50.79 |  |  |  |
| 011373 | open | 2026-11-06 | tr_nav | 4.71 | -10.81 | 12.45 | 29.14 | 21.08 | -24.4 | -14.78 | 50.72 | True | False | 招商前沿医疗保健股票A | 89.2 | False | 61.4 | lottery-like daily jump | 000711 | 81.0 | 85.0 | True | 51.15 |  |  |  |
| 009360 | open | 2026-11-06 | tr_nav | 4.31 | -11.27 | 10.57 | 23.95 | 11.85 | -23.3 | -15.73 | 51.3 | True | False | 招商创新增长混合A | 88.2 | False | 59.8 | lottery-like daily jump | 000711 | 80.0 | 81.0 | True | 51.74 |  |  |  |
| 005805 | open | 2026-11-06 | tr_nav | 4.07 | -12.36 | 6.54 | 20.02 | 12.14 | -26.03 | -16.25 | 53.51 | True | False | 华泰柏瑞医疗健康A | 88.4 | False | 57.4 | lottery-like daily jump | 000711 | 77.0 | 80.0 | True | 53.96 |  |  |  |
| 009477 | open | 2026-11-06 | tr_nav | 1.58 | -3.92 | -5.74 | -15.02 | -7.05 | -31.68 | -29.18 | 19.9 | False | False | 中银上海金ETF联接A | 84.5 | False | 51.4 |  | 009477 | 54.0 | 33.0 | False | 20.06 |  |  |  |
| 009504 | open | 2026-11-06 | tr_nav | 1.61 | -4.13 | -5.98 | -15.65 | -6.74 | -32.46 | -29.88 | 20.52 | False | False | 富国上海金ETF联接A | 90.4 | False | 49.5 |  | 009477 | 52.0 | 31.0 | False | 20.7 |  |  |  |

## Theme ETFs

| theme | code | name | r_1w | r_4w | r_12w | off_52w_high | premium_pct | shares_chg_5d_pct | composite | crowded | cluster |
|---|---|---|---|---|---|---|---|---|---|---|---|
| broad_large | 510300 | 沪深300ETF华泰柏瑞 | 1.45 | -5.95 | -12.42 | -18.99 | 0.26 | 14.72 | 34.1 | turnover surge | 004726 |
| broad_mid | 510500 | 中证500ETF南方 | 5.14 | -8.97 | -15.36 | -26.6 | 0.17 | 27.85 | 31.3 |  | 512100 |
| growth_chinext | 159915 | 创业板ETF易方达 | 1.85 | -19.06 | -29.94 | -43.57 | 0.04 |  | 17.2 | turnover surge | 512100 |
| star_tech | 588000 | 科创50ETF华夏 | 7.98 | -13.95 | -26.09 | -43.43 | 0.12 | 16.32 | 23.1 | lottery-like daily jump | 512100 |
| semis | 512480 | 半导体ETF国联安 | 7.64 | -14.93 | -25.98 | -48.42 | -0.01 | -0.96 | 30.4 | lottery-like daily jump | 512100 |
| semis | 159995 | 芯片ETF华夏 | 6.26 | -16.72 | -29.31 | -50.91 | 0.01 |  | 24.1 | lottery-like daily jump | 512100 |
| ai_compute | 159819 | 人工智能ETF易方达 | 1.88 | -15.39 | -26.4 | -39.16 | 0.11 |  | 29.4 | lottery-like daily jump | 159530 |
| ai_compute | 515880 | 通信ETF国泰 | -6.25 | -31.59 | -37.88 | -56.98 | -0.07 | -1.4 | 27.4 | lottery-like daily jump | 512100 |
| brokers | 512880 | 证券ETF国泰 | 4.99 | -2.42 | -7.85 | -21.83 | 0.12 | -0.05 | 47.7 |  | 512880 |
| banks | 512800 | 银行ETF华宝 | -1.79 | 3.18 | 8.94 | -1.79 | 0.27 | -3.82 | 87.0 |  | 004726 |
| dividend | 510880 | 红利ETF华泰柏瑞 | -2.57 | -1.75 | 2.52 | -3.66 | 0.08 | 0.32 | 81.9 |  | 004726 |
| gold | 518880 | 黄金ETF华安 | 1.7 | -4.22 | -6.16 | -30.67 | -0.08 | -1.52 | 49.9 |  | 009477 |
| gov_bonds | 511010 |  | 0.23 | 0.51 | 0.75 | 0.0 |  |  | 89.3 |  | 004726 |
| new_energy_ev | 515030 | 新能源车ETF华夏 | 6.88 | -7.25 | -16.53 | -37.87 | 0.12 | 0.23 | 19.9 |  | 512580 |
| new_energy_ev | 516160 | 新能源ETF南方 | 9.82 | -6.98 | -16.49 | -38.16 | -0.04 | 0.49 | 18.3 | 1-week gain | 512580 |
| solar | 515790 | 光伏ETF华泰柏瑞 | 11.81 | -2.22 | -11.48 | -36.77 | -0.51 | -0.49 | 21.3 | 1-week gain | 515790 |
| healthcare | 512010 | 医药ETF易方达 | 4.24 | 3.42 | 3.69 | -6.43 | -0.23 | 0.59 | 71.3 |  | 512010 |
| healthcare | 512170 | 医疗ETF华宝 | 4.18 | 2.35 | 5.44 | -10.51 | 0.03 | 0.21 | 68.3 |  | 512010 |
| consumer | 159928 | 消费ETF汇添富 | 4.73 | 7.11 | 5.83 | -17.0 | -0.08 |  | 70.2 |  | 004726 |
| consumer | 512690 | 酒ETF鹏华 | 3.7 | 6.92 | 3.23 | -26.19 | 0.33 | 2.66 | 61.7 |  | 512690 |
| defense | 512660 | 军工ETF国泰 | 3.97 | -5.64 | -10.04 | -39.3 | -0.01 | -0.35 | 36.2 |  | 159267 |
| real_estate | 512200 | 房地产ETF南方 | 2.7 | -10.99 | -5.39 | -30.87 | -0.09 | -0.19 | 47.8 |  | 512200 |

## Base rates for p_up

How often a fund in each composite band beat the CSI 300 over the next 4 weeks in the backtest. Start each call's p_up here. Watchlist themes and their products: themes.md.

| composite_band | fund_weeks | beat_csi300_pct | avg_excess_4w_pct |
|---|---|---|---|
| all | 20201 | 49.7 | 0.32 |
| 0-20 | 767 | 47.3 | 0.3 |
| 20-40 | 5572 | 47.7 | 0.18 |
| 40-60 | 7062 | 49.4 | 0.38 |
| 60-80 | 5214 | 50.9 | 0.39 |
| 80-100 | 1586 | 55.1 | 0.35 |
