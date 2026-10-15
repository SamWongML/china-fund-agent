"""Call every data and news source once and write a health table to state/smoke.md.

Run this from the real runner (GitHub Actions) before trusting any pipeline: the sources are undocumented
web APIs and some block overseas cloud IPs.
"""
from __future__ import annotations

import datetime as dt
import time

import pandas as pd

from . import collect_funds as cf
from . import collect_news as cn
from .common import CONFIG, STATE, load_yaml, md_table, now_hkt, write_json


def probe(name: str, fn) -> dict:
    t0 = time.time()
    try:
        out = fn()
        n = len(out) if hasattr(out, "__len__") else None
        return {"source": name, "ok": True, "rows": n, "secs": round(time.time() - t0, 1), "error": ""}
    except Exception as e:
        return {"source": name, "ok": False, "rows": None, "secs": round(time.time() - t0, 1), "error": str(e)[:140]}


def main() -> int:
    import akshare as ak
    checks = [
        ("calendar tool_trade_date_hist_sina", ak.tool_trade_date_hist_sina),
        ("etf eastmoney fund_etf_spot_em", cf.etf_em),
        ("etf sina fund_etf_category_sina", cf.etf_sina),
        ("etf ths fund_etf_spot_ths", cf.etf_ths),
        ("lof eastmoney fund_lof_spot_em", cf.lof_em),
        ("open eastmoney fund_open_fund_daily_em", cf.open_em),
        ("open rank fund_open_fund_rank_em", cf.open_rank_em),
        ("exchange rank fund_exchange_rank_em", cf.exchange_rank_em),
        ("fund names fund_name_em", ak.fund_name_em),
        ("purchase status fund_purchase_em", ak.fund_purchase_em),
        ("index sina stock_zh_index_daily", lambda: ak.stock_zh_index_daily(symbol="sh000300")),
        ("history etf eastmoney hfq (510300)", lambda: ak.fund_etf_hist_em(symbol="510300", start_date="20260101",
                                                                          end_date="20500101", adjust="hfq")),
        ("history etf sina (510300)", lambda: ak.fund_etf_hist_sina(symbol="sh510300")),
        ("history etf adjusted (510880)", lambda: cf.fetch_history("510880", "etf")),
        ("history open fund (110022)", lambda: cf.fetch_history("110022", "open")),
        ("fund splits fund_cf_em", lambda: ak.fund_cf_em(year=str(dt.date.today().year))),
        ("fund dividends fund_fh_em", lambda: ak.fund_fh_em(year=str(dt.date.today().year))),
        ("index csindex (000922)", lambda: ak.stock_zh_index_hist_csindex(symbol="000922", start_date="20260101",
                                                                         end_date="20500101")),
        ("valuation stock_index_pe_lg (CSI 300)", lambda: ak.stock_index_pe_lg(symbol="沪深300")),
        ("bond yields bond_zh_us_rate", lambda: ak.bond_zh_us_rate(start_date="20260101")),
        ("etf shares sse fund_etf_scale_sse", lambda: ak.fund_etf_scale_sse(
            date=(dt.date.today() - dt.timedelta(days=1)).strftime("%Y%m%d"))),
        ("etf shares szse fund_etf_scale_szse", ak.fund_etf_scale_szse),
        ("calendar macro_info_ws", lambda: ak.macro_info_ws(date=(dt.date.today()).strftime("%Y%m%d"))),
    ]
    cfg = load_yaml(CONFIG / "sources.yaml")
    for feed in cfg.get("akshare_feeds") or []:
        checks.append((f"news {feed['name']}", lambda f=feed: cn.fetch_akshare(f)))
    for feed in cfg.get("rss") or []:
        checks.append((f"rss {feed['name']}", lambda f=feed: cn.fetch_rss(f)))
    rows = [probe(n, f) for n, f in checks]
    df = pd.DataFrame(rows)
    ok = int(df["ok"].sum())
    text = (f"# Source smoke test ({now_hkt():%Y-%m-%d %H:%M} HKT)\n\n{ok}/{len(df)} sources reachable.\n\n"
            + md_table(df) + "\n")
    STATE.mkdir(parents=True, exist_ok=True)
    (STATE / "smoke.md").write_text(text, encoding="utf-8")
    write_json(STATE / "smoke.json", rows)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
