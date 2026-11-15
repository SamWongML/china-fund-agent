# Fact sheets 2026-W46 (data as of 2026-11-13, built 2026-11-15 10:05 HKT)

Data ready: **True** (last good fund snapshot 2026-11-13; missing history: none).

Returns in %: r_1w=5 trading days, r_4w=20, r_12w=60, r_26w=120, r_52w=250. Prices are adjusted for splits and dividends (ETF/LOF) or total-return NAV (open funds); basis says which. pnl_pct uses the raw latest price.

Signals: composite = 0-100 weighted percentile of the live signals (trend, reversal, lottery, crowding, low volatility) across ~60 sector and broad ETFs plus holdings and candidates; higher is better. crowded = reasons not to add now. cluster = the highest-ranked fund it moves with (60-day correlation of market-relative returns above the threshold); funds sharing a cluster are one bet. Details: journal/signal_health.md.

## Market regime: **risk-off**

| label | score | votes | sh000300_ma200_gap_pct | sh000300_r_12w_pct | sh000905_ma200_gap_pct | sh000905_r_12w_pct | breadth_above_ma200_pct | breadth_n |
|---|---|---|---|---|---|---|---|---|
| risk-off | 0.0 | 5 | -13.06 | -13.89 | -18.7 | -18.86 | 17.6 | 51 |

Signal weight multipliers from the backtest: {'trend_12w': 0.5, 'trend_26w': 0.5, 'ma200_gap': 0.5, 'rev_1w': 0.0, 'rev_4w': 0.0, 'max_20d': 0.5, 'turnover_surge': 0.0, 'low_vol': 0.5}. Backtest status: {'trend_12w': 'unproven', 'trend_26w': 'unproven', 'ma200_gap': 'unproven', 'rev_1w': 'rejected', 'rev_4w': 'rejected', 'max_20d': 'unproven', 'turnover_surge': 'rejected', 'low_vol': 'unproven', 'legacy_screen': 'unproven'}.

## Holdings

_none_

## Rules-only calls (the baseline your calls are graded against)

Target weights: core {'511010': 25.0, '510880': 16.1, '510300': 17.5, '518880': 11.4}, satellite {}, unallocated 30.0%. risk-off regime: satellite sleeve left unallocated (hold bonds or cash)

| code | action | current_weight_pct | target_weight_pct | reason | name | composite | crowded | cluster |
|---|---|---|---|---|---|---|---|---|
| 511010 | buy | 0.0 | 25.0 | core sleeve | 国债ETF国泰 | 90.7 | turnover surge | 020992 |
| 510880 | buy | 0.0 | 16.1 | core sleeve | 红利ETF华泰柏瑞 | 81.0 |  | 020992 |
| 510300 | buy | 0.0 | 17.5 | core sleeve | 沪深300ETF华泰柏瑞 | 32.2 |  | 020992 |
| 518880 | buy | 0.0 | 11.4 | core sleeve | 黄金ETF华安 | 46.9 |  | 518880 |

## Candidates (pre-screened, not held)

| code | kind | last_date | basis | r_1w | r_4w | r_12w | r_26w | r_52w | max_dd_52w | off_52w_high | vol_60d_ann | above_ma20 | above_ma60 | name | screen_score | chase_warning | composite | crowded | cluster | trend_12w_rank | trend_26w_rank | above_ma200 | vol60_pct | premium_pct | turnover_cny_m |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 020992 | open | 2026-11-13 | tr_nav | -0.87 | -0.21 | 0.86 | 1.98 | 3.85 | -0.89 | -0.87 | 1.97 | False | True | 华安中债7-10年国开债E | 94.1 | False | 96.1 |  | 020992 | 99.0 | 98.0 | True | 1.99 |  |  |
| 006848 | open | 2026-11-13 | tr_nav | -0.95 | -0.26 | 0.77 | 1.92 | 4.2 | -0.95 | -0.95 | 1.83 | False | True | 博时中债5-10农发行A | 93.7 | False | 95.9 |  | 020992 | 98.0 | 100.0 | True | 1.84 |  |  |
| 006961 | open | 2026-11-13 | tr_nav | -0.94 | -0.23 | 0.94 | 2.01 | 3.89 | -0.94 | -0.94 | 2.14 | False | True | 南方中债7-10年国开行债券指数A | 95.8 | False | 95.5 |  | 020992 | 100.0 | 97.0 | True | 2.16 |  |  |
| 004102 | open | 2026-11-13 | tr_nav | -0.9 | -0.32 | 1.33 | 4.6 | 8.0 | -2.75 | -0.93 | 3.84 | False | True | 中信保诚稳悦债券A | 93.2 | False | 94.4 |  | 020992 | 92.0 | 99.0 | True | 3.88 |  |  |
| 002334 | open | 2026-11-13 | tr_nav | -1.37 | 2.66 | 5.43 | 9.83 | 11.12 | -9.37 | -1.45 | 9.2 | True | True | 汇丰晋信大盘波动股票A | 82.1 | False | 94.0 |  | 020992 | 97.0 | 94.0 | True | 9.28 |  |  |
| 019259 | open | 2026-11-13 | tr_nav | -1.97 | -1.1 | 4.69 | 0.99 | 3.3 | -19.51 | -6.08 | 11.19 | False | True | 国泰富时国企红利ETF联接A | 82.5 | False | 86.0 |  | 020992 | 93.0 | 80.0 | True | 11.29 |  |  |
| 019311 | open | 2026-11-13 | tr_nav | -2.35 | -1.55 | 4.39 | 0.18 | 2.04 | -19.57 | -6.7 | 12.0 | False | True | 南方富时中国国企开放共赢ETF发起联接A | 82.4 | False | 84.0 |  | 020992 | 91.0 | 79.0 | True | 12.1 |  |  |
| 519655 | open | 2026-11-13 | tr_nav | -1.29 | 5.18 | 2.31 | 9.55 | 12.48 | -13.37 | -1.67 | 14.19 | True | True | 银河服务混合A | 82.7 | False | 82.7 |  | 020992 | 84.0 | 88.0 | True | 14.31 |  |  |
| 015718 | open | 2026-11-13 | tr_nav | -3.79 | 2.61 | 3.42 | 5.23 | 6.55 | -18.84 | -5.35 | 15.29 | False | True | 财通资管均衡臻选混合A | 85.5 | False | 82.4 |  | 015718 | 89.0 | 84.0 | True | 15.42 |  |  |
| 008277 | open | 2026-11-13 | tr_nav | -3.52 | 2.53 | 3.25 | 4.41 | 4.28 | -18.62 | -6.14 | 14.69 | False | True | 财通资管行业精选混合 | 84.4 | False | 82.0 |  | 020992 | 88.0 | 81.0 | True | 14.81 |  |  |
| 005618 | open | 2026-11-13 | tr_nav | -2.22 | 3.22 | 2.43 | -1.58 | 10.08 | -21.34 | -9.89 | 16.02 | True | True | 融通红利机会主题精选混合A | 81.7 | False | 75.8 |  | 020992 | 85.0 | 75.0 | True | 16.16 |  |  |
| 021308 | open | 2026-11-13 | tr_nav | -3.77 | 3.02 | -1.16 | 19.34 | 18.52 | -14.24 | -5.39 | 24.97 | False | True | 鹏华创新医药混合A | 86.3 | False | 75.4 |  | 021308 | 79.0 | 92.0 | True | 25.18 |  |  |
| 620001 | open | 2026-11-13 | tr_nav | -0.58 | 1.16 | -0.32 | -2.5 | 5.19 | -9.01 | -7.05 | 5.43 | True | True | 金元顺安宝石动力混合 | 81.5 | False | 72.6 |  | 020992 | 75.0 | 45.0 | False | 5.48 |  |  |
| 001715 | open | 2026-11-13 | tr_nav | -3.05 | -4.1 | 1.24 | 10.43 | 57.47 | -14.24 | -9.05 | 28.72 | False | False | 工银新焦点混合A | 91.1 | False | 71.6 |  | 001715 | 81.0 | 85.0 | True | 28.96 |  |  |
| 159980 | etf | 2026-11-13 | adj_close | -0.54 | -3.84 | -5.23 | -5.41 | 11.54 | -15.56 | -10.54 | 13.0 | False | False | 有色ETF大成 | 80.0 | False | 61.9 |  | 020992 | 46.0 | 51.0 | False | 13.11 |  | 859.1 |
| 000960 | open | 2026-11-13 | tr_nav | -3.31 | -0.07 | -7.84 | 28.4 | 26.58 | -22.62 | -16.06 | 45.88 | False | False | 招商医药健康产业股票 | 85.2 | False | 59.4 | lottery-like daily jump | 000960 | 67.0 | 90.0 | True | 46.26 |  |  |
| 023144 | open | 2026-11-13 | tr_nav | -2.71 | -7.61 | -5.85 | -13.99 | 12.64 | -27.74 | -25.54 | 24.82 | False | False | 汇添富中证油气资源ETF发起式联接A | 81.0 | False | 58.1 |  | 023144 | 64.0 | 55.0 | False | 25.03 |  |  |
| 011373 | open | 2026-11-13 | tr_nav | -2.46 | -1.89 | -8.32 | 28.26 | 18.73 | -24.4 | -16.88 | 45.87 | False | False | 招商前沿医疗保健股票A | 83.8 | False | 56.8 | lottery-like daily jump | 000960 | 63.0 | 89.0 | True | 46.26 |  |  |
| 160326 | open | 2026-11-13 | tr_nav | -1.17 | -1.01 | -8.02 | -8.83 | 2.45 | -14.14 | -12.72 | 13.73 | False | False | 华夏优选配置股票(FOF-LOF)A | 83.9 | False | 53.8 |  | 020992 | 34.0 | 38.0 | False | 13.85 |  |  |
| 014092 | open | 2026-11-13 | tr_nav | -1.18 | -1.04 | -8.15 | -9.06 | 2.02 | -14.29 | -12.89 | 13.74 | False | False | 华夏优选配置股票(FOF)C | 79.8 | False | 51.7 |  | 020992 | 30.0 | 37.0 | False | 13.85 |  |  |

## Theme ETFs

| theme | code | name | r_1w | r_4w | r_12w | off_52w_high | premium_pct | shares_chg_5d_pct | composite | crowded | cluster |
|---|---|---|---|---|---|---|---|---|---|---|---|
| broad_large | 510300 | 沪深300ETF华泰柏瑞 | -0.99 | -3.61 | -13.66 | -19.8 |  | 2.32 | 32.2 |  | 020992 |
| broad_mid | 510500 | 中证500ETF南方 | -2.02 | -4.61 | -18.61 | -28.08 |  | 1.55 | 27.1 |  | 159530 |
| growth_chinext | 159915 | 创业板ETF易方达 | -1.53 | -12.44 | -32.24 | -44.44 |  |  | 11.9 |  | 159516 |
| star_tech | 588000 | 科创50ETF华夏 | 2.11 | -5.31 | -25.28 | -42.24 |  | -1.32 | 23.0 | lottery-like daily jump | 159516 |
| semis | 512480 | 半导体ETF国联安 | 2.32 | -4.92 | -25.75 | -47.22 |  | -2.89 | 28.3 | lottery-like daily jump | 159516 |
| semis | 159995 | 芯片ETF华夏 | 3.73 | -5.89 | -27.6 | -49.09 |  |  | 20.8 | lottery-like daily jump | 159516 |
| ai_compute | 159819 | 人工智能ETF易方达 | 3.02 | -3.32 | -23.47 | -37.32 |  |  | 24.4 | lottery-like daily jump | 159530 |
| ai_compute | 515880 | 通信ETF国泰 | 3.21 | -19.92 | -37.24 | -55.6 |  | -0.64 | 13.7 | lottery-like daily jump | 515880 |
| brokers | 512880 | 证券ETF国泰 | -2.87 | -4.76 | -10.9 | -23.72 |  | -2.63 | 50.3 |  | 512880 |
| banks | 512800 | 银行ETF华宝 | 2.28 | 3.82 | 11.71 | 0.0 |  | 5.14 | 89.0 |  | 020992 |
| dividend | 510880 | 红利ETF华泰柏瑞 | 0.09 | -1.63 | 3.09 | -3.57 |  | -6.58 | 81.0 |  | 020992 |
| gold | 518880 | 黄金ETF华安 | -3.62 | -7.01 | -12.03 | -33.18 |  | -0.53 | 46.9 |  | 518880 |
| gov_bonds | 511010 | 国债ETF国泰 | -0.08 | 0.26 | 0.59 | -0.08 |  |  | 90.7 | turnover surge | 020992 |
| new_energy_ev | 515030 | 新能源车ETF华夏 | -5.41 | -3.58 | -22.05 | -41.24 |  | -3.02 | 18.0 |  | 512580 |
| new_energy_ev | 516160 | 新能源ETF南方 | -6.12 | -4.84 | -23.46 | -41.95 |  | 9.18 | 17.6 |  | 515790 |
| solar | 515790 | 光伏ETF华泰柏瑞 | -6.68 | -2.65 | -19.12 | -41.0 |  | 16.61 | 26.1 |  | 515790 |
| healthcare | 512010 | 医药ETF易方达 | -3.05 | 3.81 | -4.99 | -7.3 |  | -2.45 | 72.0 |  | 021308 |
| healthcare | 512170 | 医疗ETF华宝 | -2.87 | 5.28 | -4.51 | -13.08 |  | -1.91 | 65.9 |  | 021308 |
| consumer | 159928 | 消费ETF汇添富 | -0.85 | 5.25 | 2.63 | -17.7 |  |  | 74.2 |  | 020992 |
| consumer | 512690 | 酒ETF鹏华 | -1.79 | 4.51 | -2.0 | -27.51 |  | -3.16 | 61.1 |  | 015718 |
| defense | 512660 | 军工ETF国泰 | -1.96 | -5.48 | -12.8 | -40.49 |  | 3.25 | 33.1 |  | 001715 |
| real_estate | 512200 | 房地产ETF南方 | -2.98 | -8.05 | -10.65 | -32.93 |  | -8.15 | 42.6 |  | 512200 |

## Base rates for p_up

How often a fund in each composite band beat the CSI 300 over the next 4 weeks in the backtest. Start each call's p_up here. Watchlist themes and their products: themes.md.

| composite_band | fund_weeks | beat_csi300_pct | avg_excess_4w_pct |
|---|---|---|---|
| all | 20242 | 49.8 | 0.32 |
| 0-20 | 767 | 47.3 | 0.3 |
| 20-40 | 5586 | 47.7 | 0.17 |
| 40-60 | 7079 | 49.4 | 0.38 |
| 60-80 | 5220 | 51.0 | 0.39 |
| 80-100 | 1590 | 55.3 | 0.37 |
