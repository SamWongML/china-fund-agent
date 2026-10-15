# Source smoke test (2026-10-15 22:06 HKT)

29/31 sources reachable.

| source | ok | rows | secs | error |
|---|---|---|---|---|
| calendar tool_trade_date_hist_sina | True | 8797.0 | 0.8 |  |
| etf eastmoney fund_etf_spot_em | False |  | 8.2 | 502 Server Error: Bad Gateway for url: https://push2delay.eastmoney.com/api/qt/clist/get?pn=1&pz=100&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7 |
| etf sina fund_etf_category_sina | True | 1702.0 | 4.7 |  |
| etf ths fund_etf_spot_ths | True | 1748.0 | 3.1 |  |
| lof eastmoney fund_lof_spot_em | False |  | 9.2 | ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response')) |
| open eastmoney fund_open_fund_daily_em | True | 24241.0 | 144.0 |  |
| open rank fund_open_fund_rank_em | True | 20582.0 | 5.6 |  |
| exchange rank fund_exchange_rank_em | True | 1685.0 | 4.0 |  |
| fund names fund_name_em | True | 28065.0 | 5.8 |  |
| purchase status fund_purchase_em | True | 27790.0 | 20.4 |  |
| index sina stock_zh_index_daily | True | 6009.0 | 0.8 |  |
| history etf eastmoney (510300) | True | 3494.0 | 12.5 |  |
| history etf sina (510300) | True | 3494.0 | 0.1 |  |
| history open fund (110022) | True | 3903.0 | 0.6 |  |
| calendar macro_info_ws | True | 77.0 | 3.5 |  |
| news eastmoney_7x24 | True | 200.0 | 4.0 |  |
| news cls_key | True | 3.0 | 1.2 |  |
| news cls_all | True | 20.0 | 0.8 |  |
| news futu | True | 50.0 | 1.1 |  |
| news sina_7x24 | True | 20.0 | 1.6 |  |
| rss fed_press | True | 20.0 | 0.1 |  |
| rss fed_speeches | True | 15.0 | 0.1 |  |
| rss ecb_press | True | 15.0 | 0.4 |  |
| rss boj_news | True | 54.0 | 0.2 |  |
| rss cnbc_markets | True | 30.0 | 0.1 |  |
| rss cnbc_economy | True | 30.0 | 0.1 |  |
| rss marketwatch_top | True | 10.0 | 0.0 |  |
| rss bloomberg_markets | True | 20.0 | 0.3 |  |
| rss gnews_reuters_business | True | 100.0 | 0.6 |  |
| rss gnews_china_economy | True | 72.0 | 0.4 |  |
| rss gnews_cn_regulators | True | 100.0 | 0.5 |  |
