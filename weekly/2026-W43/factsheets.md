# Fact sheets 2026-W43 (data as of 2026-10-23, built 2026-10-25 08:24 HKT)

Data ready: **True** (last good fund snapshot 2026-10-23; missing history: none).

Returns in %: r_1w=5 trading days, r_4w=20, r_12w=60, r_26w=120, r_52w=250. Prices are adjusted for splits and dividends (ETF/LOF) or total-return NAV (open funds); basis says which. pnl_pct uses the raw latest price.

Signals: composite = 0-100 weighted percentile of the live signals (trend, reversal, lottery, crowding, low volatility) across ~60 sector and broad ETFs plus holdings and candidates; higher is better. crowded = reasons not to add now. cluster = the highest-ranked fund it moves with (60-day correlation of market-relative returns above the threshold); funds sharing a cluster are one bet. Details: journal/signal_health.md.

## Market regime: **risk-off**

| label | score | votes | sh000300_ma200_gap_pct | sh000300_r_12w_pct | sh000905_ma200_gap_pct | sh000905_r_12w_pct | breadth_above_ma200_pct | breadth_n |
|---|---|---|---|---|---|---|---|---|
| risk-off | 0.0 | 5 | -12.06 | -13.17 | -15.24 | -11.89 | 13.7 | 51 |

Signal weight multipliers from the backtest: {'trend_12w': 0.5, 'trend_26w': 0.5, 'ma200_gap': 0.5, 'rev_1w': 0.0, 'rev_4w': 0.0, 'max_20d': 0.5, 'turnover_surge': 0.5, 'low_vol': 0.5}. Backtest status: {'trend_12w': 'unproven', 'trend_26w': 'unproven', 'ma200_gap': 'unproven', 'rev_1w': 'rejected', 'rev_4w': 'rejected', 'max_20d': 'unproven', 'turnover_surge': 'unproven', 'low_vol': 'unproven', 'legacy_screen': 'unproven'}.

## Holdings

_none_

## Rules-only calls (the baseline your calls are graded against)

Target weights: core {'511010': 25.0, '510880': 16.2, '510300': 16.5, '518880': 12.2}, satellite {}, unallocated 30.1%. risk-off regime: satellite sleeve left unallocated (hold bonds or cash)

| code | action | current_weight_pct | target_weight_pct | reason | name | composite | crowded | cluster |
|---|---|---|---|---|---|---|---|---|
| 511010 | buy | 0.0 | 25.0 | core sleeve | 国债ETF国泰 | 80.7 | turnover surge | 020927 |
| 510880 | buy | 0.0 | 16.2 | core sleeve | 红利ETF华泰柏瑞 | 78.6 |  | 020927 |
| 510300 | buy | 0.0 | 16.5 | core sleeve | 沪深300ETF华泰柏瑞 | 35.7 |  | 020927 |
| 518880 | buy | 0.0 | 12.2 | core sleeve | 黄金ETF华安 | 52.4 |  | 008142 |

## Candidates (pre-screened, not held)

| code | kind | last_date | basis | r_1w | r_4w | r_12w | r_26w | r_52w | max_dd_52w | off_52w_high | vol_60d_ann | above_ma20 | above_ma60 | name | screen_score | chase_warning | composite | crowded | cluster | trend_12w_rank | trend_26w_rank | above_ma200 | vol60_pct | premium_pct | turnover_cny_m | shares_chg_5d_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 020927 | open | 2026-10-23 | tr_nav | -0.0 | 0.87 | 2.05 | 5.49 | 6.65 | -0.78 | -0.16 | 1.96 | True | True | 中信保诚稳鸿D | 89.1 | False | 97.6 |  | 020927 | 99.0 | 100.0 | True | 1.98 |  |  |  |
| 020351 | open | 2026-10-23 | tr_nav | -0.22 | 2.14 | 4.2 | 5.32 | 6.66 | -0.62 | -0.37 | 3.81 | True | True | 农银金瑞利率债债券 | 89.4 | False | 96.6 |  | 020927 | 100.0 | 98.0 | True | 3.84 |  |  |  |
| 021266 | open | 2026-10-23 | tr_nav | -0.25 | 1.55 | 2.75 | 5.2 | 11.54 | -2.73 | -0.37 | 3.12 | True | True | 中信保诚稳悦债券D | 89.3 | False | 96.6 |  | 020927 | 98.0 | 99.0 | True | 3.15 |  |  |  |
| 000753 | open | 2026-10-23 | tr_nav | -0.29 | 0.11 | 0.39 | 0.86 | 2.89 | -0.74 | -0.29 | 1.3 | True | True | 华宝量化对冲混合A | 76.2 | False | 91.6 |  | 020927 | 90.0 | 92.0 | True | 1.31 |  |  |  |
| 020466 | open | 2026-10-23 | tr_nav | -2.27 | 0.31 | 4.04 | 2.05 | 8.16 | -15.8 | -3.59 | 11.69 | False | True | 华泰柏瑞中证中央企业红利ETF发起式联接A | 84.3 | False | 89.4 |  | 020927 | 97.0 | 81.0 | True | 11.79 |  |  |  |
| 012761 | open | 2026-10-23 | tr_nav | -3.38 | -0.92 | 0.87 | 1.23 | 10.17 | -12.97 | -4.93 | 14.46 | False | False | 华泰柏瑞上证红利ETF联接A | 83.7 | False | 86.9 |  | 020927 | 89.0 | 85.0 | True | 14.58 |  |  |  |
| 561580 | etf | 2026-10-23 | adj_close | -2.58 | -0.17 | 3.71 | 1.58 | 7.99 | -17.62 | -4.61 | 12.61 | False | False | 央企红利ETF华泰柏瑞 | 84.5 | False | 79.5 |  | 020927 | 94.0 | 78.0 | True | 12.72 |  | 83.2 | 3.01 |
| 001998 | open | 2026-10-23 | tr_nav | -1.12 | -2.54 | 9.5 | 27.15 | 62.5 | -14.28 | -6.26 | 26.08 | False | True | 工银新焦点混合C | 87.5 | False | 78.3 |  | 001998 | 91.0 | 97.0 | True | 26.3 |  |  |  |
| 014259 | open | 2026-10-23 | tr_nav | -0.04 | 10.05 | 10.37 | 11.22 | 12.34 | -0.17 | -0.04 | 18.93 | True | True | 百嘉百兴纯债债券A | 88.8 | False | 77.9 | lottery-like daily jump | 020927 | 96.0 | 90.0 | True | 19.09 |  |  |  |
| 002495 | open | 2026-10-23 | tr_nav | -1.05 | -3.77 | 0.5 | 3.07 | 18.58 | -14.18 | -8.25 | 24.24 | False | False | 前海开源量化优选A | 82.0 | False | 71.2 |  | 002495 | 75.0 | 74.0 | True | 24.45 |  |  |  |
| 011373 | open | 2026-10-23 | tr_nav | -3.26 | -11.45 | 9.91 | 23.51 | 15.89 | -24.4 | -18.04 | 47.21 | False | False | 招商前沿医疗保健股票A | 91.8 | False | 65.3 |  | 011373 | 86.0 | 87.0 | True | 47.61 |  |  |  |
| 000960 | open | 2026-10-23 | tr_nav | -2.22 | -10.23 | 8.8 | 24.1 | 23.72 | -22.62 | -17.87 | 47.54 | False | False | 招商医药健康产业股票 | 91.7 | False | 64.2 |  | 011373 | 82.0 | 86.0 | True | 47.94 |  |  |  |
| 009360 | open | 2026-10-23 | tr_nav | -3.43 | -12.06 | 8.6 | 19.33 | 8.91 | -23.3 | -18.66 | 47.99 | False | False | 招商创新增长混合A | 90.4 | False | 63.4 |  | 011373 | 84.0 | 84.0 | True | 48.39 |  |  |  |
| 004818 | open | 2026-10-23 | tr_nav | 0.02 | -9.87 | 0.01 | 9.52 | 29.78 | -32.92 | -28.53 | 36.25 | False | False | 国寿安保目标策略混合发起A | 82.5 | False | 63.0 |  | 004818 | 69.0 | 76.0 | False | 36.55 |  |  |  |
| 012186 | open | 2026-10-23 | tr_nav | -3.35 | -11.92 | 9.01 | 20.0 | 9.4 | -23.66 | -19.13 | 49.25 | False | False | 招商品质成长混合A | 90.8 | False | 62.5 |  | 011373 | 83.0 | 82.0 | True | 49.67 |  |  |  |
| 022490 | open | 2026-10-23 | tr_nav | -0.96 | -9.62 | -1.77 | -4.3 | 11.3 | -15.81 | -13.14 | 29.07 | False | False | 华商恒鑫回报混合A | 84.9 | False | 61.0 |  | 004818 | 63.0 | 66.0 | False | 29.32 |  |  |  |
| 005805 | open | 2026-10-23 | tr_nav | -4.06 | -12.38 | 2.67 | 12.77 | 11.46 | -26.03 | -19.78 | 49.22 | False | False | 华泰柏瑞医疗健康A | 90.6 | False | 58.8 |  | 011373 | 78.0 | 80.0 | True | 49.63 |  |  |  |
| 008142 | open | 2026-10-23 | tr_nav | -4.11 | -7.58 | -3.68 | -16.43 | -6.88 | -30.12 | -30.12 | 19.11 | False | False | 工银黄金ETF联接A | 79.5 | False | 57.9 |  | 008142 | 73.0 | 22.0 | False | 19.27 |  |  |  |
| 001040 | open | 2026-10-23 | tr_nav | -5.39 | -22.3 | -1.33 | -3.95 | 48.25 | -41.6 | -32.62 | 57.86 | False | False | 新华策略精选股票A | 87.7 | False | 54.5 |  | 004818 | 76.0 | 70.0 | False | 58.35 |  |  |  |
| 518850 | etf | 2026-10-23 | adj_close | -4.13 | -7.36 | -4.11 | -16.38 | -7.03 | -30.86 | -30.86 | 20.61 | False | False | 黄金ETF华夏 | 83.3 | False | 51.7 |  | 008142 | 70.0 | 28.0 | False | 20.78 |  | 872.1 | -0.08 |

## Theme ETFs

| theme | code | name | r_1w | r_4w | r_12w | off_52w_high | premium_pct | shares_chg_5d_pct | composite | crowded | cluster |
|---|---|---|---|---|---|---|---|---|---|---|---|
| broad_large | 510300 | 沪深300ETF华泰柏瑞 | -1.37 | -7.81 | -12.72 | -17.93 |  | 23.43 | 35.7 |  | 020927 |
| broad_mid | 510500 | 中证500ETF南方 | 0.7 | -10.73 | -11.37 | -24.07 |  | 26.45 | 35.4 |  | 004818 |
| growth_chinext | 159915 | 创业板ETF易方达 | -3.12 | -18.59 | -24.88 | -38.52 |  |  | 17.6 |  | 004818 |
| star_tech | 588000 | 科创50ETF华夏 | -0.56 | -16.16 | -24.68 | -39.33 |  | 17.23 | 30.4 |  | 004818 |
| semis | 512480 | 半导体ETF国联安 | 0.24 | -16.48 | -24.41 | -44.36 |  | -0.24 | 38.3 |  | 004818 |
| semis | 159995 | 芯片ETF华夏 | -0.87 | -18.4 | -27.97 | -46.37 |  |  | 38.4 |  | 004818 |
| ai_compute | 159819 | 人工智能ETF易方达 | 3.46 | -12.66 | -22.4 | -32.93 |  |  | 33.6 |  | 004818 |
| ai_compute | 515880 | 通信ETF国泰 | -1.53 | -25.07 | -23.4 | -45.41 |  | -0.33 | 33.3 |  | 004818 |
| brokers | 512880 | 证券ETF国泰 | -1.65 | -2.78 | -10.2 | -21.59 |  | -0.62 | 50.7 |  | 512880 |
| banks | 512800 | 银行ETF华宝 | -1.74 | 1.43 | 5.73 | -3.19 |  | 0.47 | 79.3 |  | 020927 |
| dividend | 510880 | 红利ETF华泰柏瑞 | -3.5 | -1.11 | 0.91 | -5.4 |  | 0.69 | 78.6 |  | 020927 |
| gold | 518880 | 黄金ETF华安 | -4.15 | -7.42 | -4.22 | -31.12 |  | 0.01 | 52.4 |  | 008142 |
| gov_bonds | 511010 | 国债ETF国泰 | 0.13 | 0.38 | 0.65 | -0.01 |  | 4.58 | 80.7 | turnover surge | 020927 |
| new_energy_ev | 515030 | 新能源车ETF华夏 | -1.12 | -10.52 | -17.48 | -39.74 |  | -0.68 | 21.3 |  | 512580 |
| new_energy_ev | 516160 | 新能源ETF南方 | -3.0 | -12.73 | -19.47 | -40.82 |  | -3.64 | 24.5 |  | 515790 |
| solar | 515790 | 光伏ETF华泰柏瑞 | 0.0 | -9.58 | -14.54 | -39.39 |  | -2.43 | 29.1 |  | 515790 |
| healthcare | 512010 | 医药ETF易方达 | 2.45 | 1.08 | -0.27 | -11.32 |  | -1.31 | 62.5 |  | 512010 |
| healthcare | 512170 | 医疗ETF华宝 | 3.73 | -0.89 | 2.77 | -14.36 |  | -1.54 | 59.5 |  | 011373 |
| consumer | 159928 | 消费ETF汇添富 | -0.6 | 2.16 | -1.04 | -22.27 |  |  | 56.6 |  | 020927 |
| consumer | 512690 | 酒ETF鹏华 | -1.43 | 1.72 | -2.35 | -31.63 |  | -0.4 | 53.0 |  | 020927 |
| defense | 512660 | 军工ETF国泰 | 0.19 | -7.09 | -3.63 | -36.92 |  | 6.69 | 38.5 |  | 001998 |
| real_estate | 512200 | 房地产ETF南方 | -3.24 | -1.6 | 0.78 | -29.55 |  | 0.25 | 50.8 |  | 512200 |

## Base rates for p_up

How often a fund in each composite band beat the CSI 300 over the next 4 weeks in the backtest. Start each call's p_up here. Watchlist themes and their products: themes.md.

| composite_band | fund_weeks | beat_csi300_pct | avg_excess_4w_pct |
|---|---|---|---|
| all | 20017 | 49.6 | 0.31 |
| 0-20 | 433 | 50.1 | 0.54 |
| 20-40 | 5230 | 47.2 | 0.13 |
| 40-60 | 8048 | 49.7 | 0.46 |
| 60-80 | 5190 | 50.6 | 0.26 |
| 80-100 | 1116 | 54.8 | 0.15 |
