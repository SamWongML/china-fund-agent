# Source smoke test (2026-10-16 00:12 HKT)

34/39 sources reachable.

| source | ok | rows | secs | error |
|---|---|---|---|---|
| calendar tool_trade_date_hist_sina | True | 8797.0 | 0.8 |  |
| etf eastmoney fund_etf_spot_em | False |  | 8.1 | 502 Server Error: Bad Gateway for url: https://push2delay.eastmoney.com/api/qt/clist/get?pn=1&pz=100&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7 |
| etf sina fund_etf_category_sina | True | 1702.0 | 3.7 |  |
| etf ths fund_etf_spot_ths | True | 1748.0 | 2.5 |  |
| lof eastmoney fund_lof_spot_em | False |  | 7.4 | ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response')) |
| open eastmoney fund_open_fund_daily_em | True | 24242.0 | 21.8 |  |
| open rank fund_open_fund_rank_em | True | 20581.0 | 5.8 |  |
| exchange rank fund_exchange_rank_em | True | 1685.0 | 3.0 |  |
| fund names fund_name_em | True | 28065.0 | 5.4 |  |
| purchase status fund_purchase_em | True | 27790.0 | 15.0 |  |
| index sina stock_zh_index_daily | True | 6009.0 | 0.9 |  |
| history etf eastmoney hfq (510300) | False |  | 0.8 | ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response')) |
| history etf sina (510300) | True | 3494.0 | 0.6 |  |
| history etf adjusted (510880) | True | 4795.0 | 0.8 |  |
| history open fund (110022) | True | 3903.0 | 0.1 |  |
| fund splits fund_cf_em | True | 83.0 | 0.7 |  |
| fund dividends fund_fh_em | True | 5223.0 | 42.8 |  |
| index csindex (000922) | True | 188.0 | 0.7 |  |
| valuation stock_index_pe_lg (CSI 300) | True | 259.0 | 1.5 |  |
| bond yields bond_zh_us_rate | True | 209.0 | 1.1 |  |
| etf shares sse fund_etf_scale_sse | False |  | 1.3 | Expecting value: line 1 column 1 (char 0) |
| etf shares szse fund_etf_scale_szse | False |  | 3.4 | ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer')) |
| calendar macro_info_ws | True | 40.0 | 0.5 |  |
| news eastmoney_7x24 | True | 200.0 | 2.4 |  |
| news cls_key | True | 2.0 | 0.7 |  |
| news cls_all | True | 20.0 | 0.6 |  |
| news futu | True | 50.0 | 0.7 |  |
| news sina_7x24 | True | 20.0 | 1.0 |  |
| rss fed_press | True | 20.0 | 0.1 |  |
| rss fed_speeches | True | 15.0 | 0.1 |  |
| rss ecb_press | True | 15.0 | 0.9 |  |
| rss boj_news | True | 54.0 | 0.3 |  |
| rss cnbc_markets | True | 30.0 | 0.1 |  |
| rss cnbc_economy | True | 30.0 | 0.1 |  |
| rss marketwatch_top | True | 10.0 | 0.0 |  |
| rss bloomberg_markets | True | 20.0 | 0.5 |  |
| rss gnews_reuters_business | True | 100.0 | 0.7 |  |
| rss gnews_china_economy | True | 76.0 | 0.5 |  |
| rss gnews_cn_regulators | True | 40.0 | 0.6 |  |
