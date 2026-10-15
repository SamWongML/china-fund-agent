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
        ("history etf eastmoney (510300)", lambda: cf.fetch_history("510300", "etf", start="20260101")),
        ("history etf sina (510300)", lambda: ak.fund_etf_hist_sina(symbol="sh510300")),
        ("history open fund (110022)", lambda: cf.fetch_history("110022", "open")),
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
