# Source smoke test (2026-10-15 22:14 HKT)

29/31 sources reachable.

| source | ok | rows | secs | error |
|---|---|---|---|---|
| calendar tool_trade_date_hist_sina | True | 8797.0 | 0.6 |  |
| etf eastmoney fund_etf_spot_em | False |  | 8.0 | 502 Server Error: Bad Gateway for url: https://push2delay.eastmoney.com/api/qt/clist/get?pn=1&pz=100&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7 |
| etf sina fund_etf_category_sina | True | 1702.0 | 4.5 |  |
| etf ths fund_etf_spot_ths | True | 1748.0 | 2.3 |  |
| lof eastmoney fund_lof_spot_em | False |  | 12.1 | ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response')) |
| open eastmoney fund_open_fund_daily_em | True | 24241.0 | 80.1 |  |
| open rank fund_open_fund_rank_em | True | 20582.0 | 4.4 |  |
| exchange rank fund_exchange_rank_em | True | 1685.0 | 3.0 |  |
| fund names fund_name_em | True | 28065.0 | 3.8 |  |
| purchase status fund_purchase_em | True | 27790.0 | 102.2 |  |
| index sina stock_zh_index_daily | True | 6009.0 | 1.0 |  |
| history etf eastmoney (510300) | True | 3494.0 | 10.8 |  |
| history etf sina (510300) | True | 3494.0 | 0.2 |  |
| history open fund (110022) | True | 3903.0 | 0.6 |  |
| calendar macro_info_ws | True | 77.0 | 1.0 |  |
| news eastmoney_7x24 | True | 200.0 | 1.6 |  |
| news cls_key | True | 3.0 | 1.1 |  |
| news cls_all | True | 20.0 | 0.7 |  |
| news futu | True | 50.0 | 0.8 |  |
| news sina_7x24 | True | 20.0 | 1.3 |  |
| rss fed_press | True | 20.0 | 0.1 |  |
| rss fed_speeches | True | 15.0 | 0.1 |  |
| rss ecb_press | True | 15.0 | 0.8 |  |
| rss boj_news | True | 54.0 | 0.4 |  |
| rss cnbc_markets | True | 30.0 | 0.2 |  |
| rss cnbc_economy | True | 30.0 | 0.2 |  |
| rss marketwatch_top | True | 10.0 | 0.1 |  |
| rss bloomberg_markets | True | 20.0 | 0.4 |  |
| rss gnews_reuters_business | True | 100.0 | 0.6 |  |
| rss gnews_china_economy | True | 74.0 | 0.5 |  |
| rss gnews_cn_regulators | True | 40.0 | 0.5 |  |
