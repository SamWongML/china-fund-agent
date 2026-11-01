# Fact sheets 2026-W44 (data as of 2026-10-30, built 2026-11-01 09:17 HKT)

Data ready: **True** (last good fund snapshot 2026-10-30; missing history: none).

Returns in %: r_1w=5 trading days, r_4w=20, r_12w=60, r_26w=120, r_52w=250. Prices are adjusted for splits and dividends (ETF/LOF) or total-return NAV (open funds); basis says which. pnl_pct uses the raw latest price.

Signals: composite = 0-100 weighted percentile of the live signals (trend, reversal, lottery, crowding, low volatility) across ~60 sector and broad ETFs plus holdings and candidates; higher is better. crowded = reasons not to add now. cluster = the highest-ranked fund it moves with (60-day correlation of market-relative returns above the threshold); funds sharing a cluster are one bet. Details: journal/signal_health.md.

## Market regime: **risk-off**

| label | score | votes | sh000300_ma200_gap_pct | sh000300_r_12w_pct | sh000905_ma200_gap_pct | sh000905_r_12w_pct | breadth_above_ma200_pct | breadth_n |
|---|---|---|---|---|---|---|---|---|
| risk-off | 0.0 | 5 | -14.36 | -12.4 | -21.85 | -14.27 | 17.6 | 51 |

Signal weight multipliers from the backtest: {'trend_12w': 0.5, 'trend_26w': 0.5, 'ma200_gap': 0.5, 'rev_1w': 0.0, 'rev_4w': 0.0, 'max_20d': 0.5, 'turnover_surge': 0.0, 'low_vol': 0.5}. Backtest status: {'trend_12w': 'unproven', 'trend_26w': 'unproven', 'ma200_gap': 'unproven', 'rev_1w': 'rejected', 'rev_4w': 'rejected', 'max_20d': 'unproven', 'turnover_surge': 'rejected', 'low_vol': 'unproven', 'legacy_screen': 'unproven'}.

## Holdings

_none_

## Rules-only calls (the baseline your calls are graded against)

Target weights: core {'511010': 25.0, '510880': 15.7, '510300': 17.2, '518880': 12.1}, satellite {}, unallocated 30.0%. risk-off regime: satellite sleeve left unallocated (hold bonds or cash)

| code | action | current_weight_pct | target_weight_pct | reason | name | composite | crowded | cluster |
|---|---|---|---|---|---|---|---|---|
| 511010 | buy | 0.0 | 25.0 | core sleeve | 国债ETF国泰 | 92.2 | turnover surge | 022994 |
| 510880 | buy | 0.0 | 15.7 | core sleeve | 红利ETF华泰柏瑞 | 77.4 |  | 022994 |
| 510300 | buy | 0.0 | 17.2 | core sleeve | 沪深300ETF华泰柏瑞 | 37.9 |  | 022994 |
| 518880 | buy | 0.0 | 12.1 | core sleeve | 黄金ETF华安 | 50.9 |  | 009504 |

## Candidates (pre-screened, not held)

| code | kind | last_date | basis | r_1w | r_4w | r_12w | r_26w | r_52w | max_dd_52w | off_52w_high | vol_60d_ann | above_ma20 | above_ma60 | name | screen_score | chase_warning | composite | crowded | cluster | trend_12w_rank | trend_26w_rank | above_ma200 | vol60_pct | premium_pct | turnover_cny_m | shares_chg_5d_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 022994 | open | 2026-10-30 | tr_nav | -0.2 | 0.31 | 2.51 | 3.49 | 6.05 | -1.18 | -0.33 | 1.43 | False | True | 中信保诚稳健债券D | 89.9 | False | 97.9 |  | 022994 | 100.0 | 100.0 | True | 1.44 |  |  |  |
| 004102 | open | 2026-10-30 | tr_nav | -0.38 | -0.02 | 1.94 | 5.32 | 9.87 | -2.75 | -0.9 | 3.62 | False | True | 中信保诚稳悦债券A | 90.6 | False | 96.9 |  | 022994 | 99.0 | 99.0 | True | 3.65 |  |  |  |
| 012111 | open | 2026-10-30 | tr_nav | -0.82 | -1.78 | 2.06 | 3.9 | 7.47 | -3.65 | -2.14 | 4.93 | False | False | 鹏华安颐混合A | 90.4 | False | 95.9 |  | 022994 | 98.0 | 98.0 | True | 4.97 |  |  |  |
| 019400 | open | 2026-10-30 | tr_nav | -0.12 | -0.01 | 0.73 | 1.5 | 2.54 | -0.46 | -0.34 | 1.11 | False | True | 国泰海通安睿纯债债券A | 92.3 | False | 94.2 |  | 022994 | 95.0 | 95.0 | True | 1.12 |  |  |  |
| 159980 | etf | 2026-10-30 | adj_close | -0.33 | -3.27 | -0.05 | -2.19 | 18.04 | -15.56 | -7.41 | 12.28 | False | False | 有色ETF大成 | 78.4 | False | 78.9 |  | 022994 | 73.0 | 71.0 | False | 12.38 |  | 472.6 |  |
| 160642 | open | 2026-10-30 | tr_nav | -6.27 | -11.63 | 1.19 | -0.37 | 20.46 | -24.07 | -22.63 | 28.02 | False | False | 鹏华增瑞混合(LOF)A | 87.6 | False | 77.9 |  | 160642 | 85.0 | 93.0 | False | 28.25 |  |  |  |
| 159985 | etf | 2026-10-30 | adj_close | -3.41 | -7.16 | 3.11 | -0.28 | 11.67 | -14.69 | -12.16 | 22.06 | False | False | 豆粕ETF华夏 | 89.8 | False | 77.6 |  | 159985 | 86.0 | 79.0 | True | 22.25 |  | 171.4 |  |
| 017154 | open | 2026-10-30 | tr_nav | -7.9 | -13.93 | 1.99 | -3.62 | 13.74 | -14.22 | -14.22 | 26.15 | False | False | 民生加银专精特新智选混合发起式A | 87.2 | False | 76.9 |  | 017154 | 94.0 | 83.0 | False | 26.37 |  |  |  |
| 001715 | open | 2026-10-30 | tr_nav | -7.61 | -9.62 | 1.02 | 13.49 | 58.54 | -14.24 | -13.36 | 27.61 | False | False | 工银新焦点混合A | 89.3 | False | 76.5 |  | 001715 | 90.0 | 96.0 | True | 27.85 |  |  |  |
| 008168 | open | 2026-10-28 | tr_nav | -0.73 | -4.81 | -2.15 | 2.45 | 15.57 | -10.5 | -9.42 | 10.52 | False | False | 汇添富聚焦成长三个月混合FOF | 80.8 | False | 76.1 |  | 022994 | 52.0 | 84.0 | True | 10.2 |  |  |  |
| 001420 | open | 2026-10-30 | tr_nav | -6.75 | -12.39 | 4.83 | -12.84 | 5.26 | -24.27 | -15.06 | 24.34 | False | False | 南方大数据300A | 80.2 | False | 73.2 |  | 017154 | 96.0 | 63.0 | False | 24.55 |  |  |  |
| 011373 | open | 2026-10-30 | tr_nav | -0.7 | -15.31 | 16.6 | 22.22 | 17.65 | -24.4 | -18.61 | 46.86 | False | False | 招商前沿医疗保健股票A | 88.3 | False | 68.1 |  | 011373 | 93.0 | 90.0 | True | 47.26 |  |  |  |
| 014564 | open | 2026-10-30 | tr_nav | -2.1 | -8.21 | 1.85 | 5.5 | -1.36 | -23.05 | -12.08 | 31.82 | False | False | 天弘创新药精选50ETF联接A | 82.9 | False | 67.6 |  | 512010 | 82.0 | 80.0 | True | 32.09 |  |  |  |
| 000960 | open | 2026-10-30 | tr_nav | 1.24 | -13.3 | 17.53 | 24.04 | 27.67 | -22.62 | -16.85 | 47.23 | False | False | 招商医药健康产业股票 | 86.9 | False | 66.9 |  | 011373 | 91.0 | 91.0 | True | 47.62 |  |  |  |
| 501026 | open | 2026-10-30 | tr_nav | -3.77 | -19.35 | 0.29 | -1.86 | 62.99 | -34.49 | -34.3 | 41.4 | False | False | 财通多策略福享混合(LOF)A | 85.8 | False | 66.8 |  | 160642 | 79.0 | 81.0 | False | 41.75 |  |  |  |
| 517380 | etf | 2026-10-30 | adj_close | -2.21 | -8.39 | 2.18 | 5.28 | -0.62 | -23.92 | -12.9 | 35.31 | False | False | 创新药ETF天弘 | 83.4 | False | 66.2 |  | 512010 | 83.0 | 78.0 | True | 35.61 |  | 65.9 | 0.0 |
| 012186 | open | 2026-10-30 | tr_nav | -0.7 | -16.17 | 15.48 | 17.74 | 11.75 | -23.66 | -19.7 | 48.86 | False | False | 招商品质成长混合A | 87.3 | False | 65.8 |  | 011373 | 89.0 | 89.0 | True | 49.27 |  |  |  |
| 009360 | open | 2026-10-30 | tr_nav | -0.69 | -15.95 | 14.85 | 17.08 | 11.2 | -23.3 | -19.22 | 47.53 | False | False | 招商创新增长混合A | 87.2 | False | 65.6 |  | 011373 | 87.0 | 88.0 | True | 47.93 |  |  |  |
| 009805 | open | 2026-10-30 | tr_nav | -2.22 | -13.48 | 2.45 | 0.44 | 7.94 | -19.93 | -17.29 | 41.11 | False | False | 国泰医药健康股票A | 84.8 | False | 60.0 |  | 512010 | 81.0 | 73.0 | False | 41.46 |  |  |  |
| 009504 | open | 2026-10-30 | tr_nav | -1.02 | -7.6 | -2.83 | -16.73 | -11.87 | -30.99 | -30.99 | 19.5 | False | False | 富国上海金ETF联接A | 82.2 | False | 51.9 |  | 009504 | 53.0 | 21.0 | False | 19.67 |  |  |  |

## Theme ETFs

| theme | code | name | r_1w | r_4w | r_12w | off_52w_high | premium_pct | shares_chg_5d_pct | composite | crowded | cluster |
|---|---|---|---|---|---|---|---|---|---|---|---|
| broad_large | 510300 | 沪深300ETF华泰柏瑞 | -2.7 | -9.97 | -11.73 | -20.15 |  | 10.28 | 37.9 |  | 022994 |
| broad_mid | 510500 | 中证500ETF南方 | -8.05 | -17.58 | -14.05 | -30.19 |  | -5.7 | 41.1 |  | 512100 |
| growth_chinext | 159915 | 创业板ETF易方达 | -9.88 | -26.48 | -25.54 | -44.6 |  |  | 19.1 |  | 512100 |
| star_tech | 588000 | 科创50ETF华夏 | -13.64 | -28.31 | -26.42 | -47.61 |  | 9.45 | 34.7 |  | 512100 |
| semis | 512480 | 半导体ETF国联安 | -13.88 | -29.62 | -24.84 | -52.08 |  | 1.85 | 36.0 |  | 160642 |
| semis | 159995 | 芯片ETF华夏 | -13.86 | -30.83 | -27.5 | -53.81 |  |  | 30.5 |  | 160642 |
| ai_compute | 159819 | 人工智能ETF易方达 | -10.96 | -24.35 | -20.18 | -40.28 |  |  | 35.3 |  | 512100 |
| ai_compute | 515880 | 通信ETF国泰 | -15.95 | -36.38 | -22.16 | -54.12 |  | -3.53 | 28.0 |  | 512100 |
| brokers | 512880 | 证券ETF国泰 | -5.03 | -8.03 | -13.02 | -25.54 |  | -1.34 | 45.7 |  | 512880 |
| banks | 512800 | 银行ETF华宝 | 5.18 | 6.44 | 6.31 | 0.0 |  | 29.91 | 80.6 |  | 022994 |
| dividend | 510880 | 红利ETF华泰柏瑞 | 4.53 | 3.07 | 4.47 | -1.11 |  | 8.09 | 77.4 |  | 022994 |
| gold | 518880 | 黄金ETF华安 | -1.02 | -7.66 | -2.93 | -31.83 |  | -1.01 | 50.9 |  | 009504 |
| gov_bonds | 511010 | 国债ETF国泰 | -0.02 | 0.29 | 0.63 | -0.11 |  | 4.52 | 92.2 | turnover surge | 022994 |
| new_energy_ev | 515030 | 新能源车ETF华夏 | -3.54 | -13.04 | -20.15 | -41.87 |  | -1.53 | 16.6 |  | 512580 |
| new_energy_ev | 516160 | 新能源ETF南方 | -4.85 | -15.89 | -21.12 | -43.69 |  | -1.56 | 19.3 |  | 512580 |
| solar | 515790 | 光伏ETF华泰柏瑞 | -6.69 | -15.53 | -16.79 | -43.45 |  | -0.62 | 29.5 |  | 515790 |
| healthcare | 512010 | 医药ETF易方达 | 0.27 | 0.53 | 0.27 | -10.87 |  | -0.66 | 68.3 |  | 512010 |
| healthcare | 512170 | 医疗ETF华宝 | 0.3 | -1.76 | 3.08 | -14.1 |  | -1.41 | 67.5 |  | 512010 |
| consumer | 159928 | 消费ETF汇添富 | 1.96 | 4.64 | -3.29 | -20.75 |  |  | 48.1 |  | 022994 |
| consumer | 512690 | 酒ETF鹏华 | 4.1 | 5.88 | -4.42 | -28.83 |  | -2.54 | 34.4 |  | 022994 |
| defense | 512660 | 军工ETF国泰 | -7.45 | -13.02 | -8.48 | -41.62 |  | 2.21 | 43.4 |  | 001715 |
| real_estate | 512200 | 房地产ETF南方 | -4.63 | -11.54 | -5.28 | -32.81 |  | -0.08 | 46.6 |  | 512200 |

## Base rates for p_up

How often a fund in each composite band beat the CSI 300 over the next 4 weeks in the backtest. Start each call's p_up here. Watchlist themes and their products: themes.md.

| composite_band | fund_weeks | beat_csi300_pct | avg_excess_4w_pct |
|---|---|---|---|
| all | 20109 | 49.6 | 0.32 |
| 0-20 | 766 | 47.4 | 0.3 |
| 20-40 | 5549 | 47.7 | 0.18 |
| 40-60 | 7018 | 49.4 | 0.38 |
| 60-80 | 5199 | 50.8 | 0.37 |
| 80-100 | 1577 | 54.7 | 0.29 |
