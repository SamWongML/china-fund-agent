"""Daily end-of-day snapshot of the onshore ETF / LOF / open-end fund universe.

Run after 23:00 HKT on trading days (open-end NAVs are filled 16:00-23:00), and again the next
morning as a catch-up. Idempotent: datasets already saved for the target date are skipped.

    python -m cfa.collect_funds            # latest trading day <= today (HKT)
    python -m cfa.collect_funds --date 2026-10-15 --force
"""
from __future__ import annotations

import argparse
import datetime as dt

import pandas as pd

from .common import (HISTORY, LATEST, RAW, REF, first_ok, last_trading_day, load_holdings, log, log_run,
                     md_table, now_hkt, retry, today_hkt, update_status, watch_codes, write_json, sha256_file, DATA)

MIN_ROWS = {"etf": 600, "lof": 150, "open": 6000, "open_rank": 5000, "exchange_rank": 600}
INDEXES = {"sh000300": "CSI 300", "sh000905": "CSI 500", "sz399006": "ChiNext", "sh000922": "CSI Dividend"}


def _num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")


# ---------- normalisers: every dataset gets English columns + code as 6-char string ----------

def etf_em() -> pd.DataFrame:
    import akshare as ak
    df = ak.fund_etf_spot_em()
    out = pd.DataFrame({
        "code": df["代码"].astype(str).str.zfill(6), "name": df["名称"], "close": _num(df["最新价"]),
        "iopv": _num(df["IOPV实时估值"]), "premium_pct": _num(df["基金折价率"]), "chg_pct": _num(df["涨跌幅"]),
        "volume": _num(df["成交量"]), "turnover_cny": _num(df["成交额"]), "shares": _num(df["最新份额"]),
        "mkt_cap": _num(df["总市值"]), "main_net_inflow": _num(df["主力净流入-净额"]),
        "data_date": df["数据日期"].astype(str).str[:10],
    })
    return out


def etf_sina(kind: str = "ETF基金") -> pd.DataFrame:
    import akshare as ak
    df = ak.fund_etf_category_sina(symbol=kind)
    code = df["代码"].astype(str).str[-6:]
    out = pd.DataFrame({"code": code, "name": df["名称"], "close": _num(df["最新价"]),
                        "chg_pct": _num(df["涨跌幅"]), "volume": _num(df["成交量"]),
                        "turnover_cny": _num(df["成交额"])})
    return out


def etf_ths() -> pd.DataFrame:
    import akshare as ak
    df = ak.fund_etf_spot_ths()
    cols = {c: c for c in df.columns}
    code_col = next(c for c in cols if "代码" in c)
    name_col = next(c for c in cols if "名称" in c)
    nav_col = next((c for c in cols if "当前-单位净值" in c or c == "最新-单位净值"), None)
    out = pd.DataFrame({"code": df[code_col].astype(str).str.zfill(6), "name": df[name_col]})
    if nav_col:
        out["close"] = _num(df[nav_col])
    return out


def lof_em() -> pd.DataFrame:
    import akshare as ak
    df = ak.fund_lof_spot_em()
    return pd.DataFrame({"code": df["代码"].astype(str).str.zfill(6), "name": df["名称"], "close": _num(df["最新价"]),
                         "chg_pct": _num(df["涨跌幅"]), "volume": _num(df["成交量"]),
                         "turnover_cny": _num(df["成交额"])})


def open_em() -> pd.DataFrame:
    import akshare as ak
    df = ak.fund_open_fund_daily_em()
    nav_cols = [c for c in df.columns if c.endswith("-单位净值")]
    acc_cols = [c for c in df.columns if c.endswith("-累计净值")]
    nav_date = nav_cols[0].rsplit("-", 1)[0]
    return pd.DataFrame({
        "code": df["基金代码"].astype(str).str.zfill(6), "name": df["基金简称"],
        "nav": _num(df[nav_cols[0]]), "acc_nav": _num(df[acc_cols[0]]),
        "prev_nav": _num(df[nav_cols[1]]) if len(nav_cols) > 1 else None,
        "daily_ret_pct": _num(df["日增长率"]), "purchase": df["申购状态"], "redeem": df["赎回状态"],
        "fee": df["手续费"].astype(str), "nav_date": nav_date,
    })


RANK_COLS = {"近1周": "r_1w", "近1月": "r_1m", "近3月": "r_3m", "近6月": "r_6m", "近1年": "r_1y",
             "近2年": "r_2y", "近3年": "r_3y", "今年来": "r_ytd", "成立来": "r_since"}


def open_rank_em() -> pd.DataFrame:
    import akshare as ak
    df = ak.fund_open_fund_rank_em(symbol="全部")
    out = pd.DataFrame({"code": df["基金代码"].astype(str).str.zfill(6), "name": df["基金简称"],
                        "nav_date": df["日期"].astype(str).str[:10], "nav": _num(df["单位净值"]),
                        "acc_nav": _num(df["累计净值"]), "fee": df["手续费"].astype(str)})
    for zh, en in RANK_COLS.items():
        out[en] = _num(df[zh])
    return out


def exchange_rank_em() -> pd.DataFrame:
    import akshare as ak
    df = ak.fund_exchange_rank_em()
    out = pd.DataFrame({"code": df["基金代码"].astype(str).str.zfill(6), "name": df["基金简称"],
                        "type": df["类型"], "nav_date": df["日期"].astype(str).str[:10],
                        "nav": _num(df["单位净值"]), "acc_nav": _num(df["累计净值"]),
                        "inception": df["成立日期"].astype(str).str[:10]})
    for zh, en in RANK_COLS.items():
        out[en] = _num(df[zh])
    return out


DATASETS = {
    "etf": [("eastmoney", etf_em), ("sina", etf_sina), ("ths", etf_ths)],
    "lof": [("eastmoney", lof_em), ("sina", lambda: etf_sina("LOF基金"))],
    "open": [("eastmoney", open_em)],
    "open_rank": [("eastmoney", open_rank_em)],
    "exchange_rank": [("eastmoney", exchange_rank_em)],
}


def snapshot_path(dataset: str, d: dt.date):
    return RAW / "funds" / dataset / f"year={d.year}" / f"month={d.month:02d}" / f"{d.isoformat()}.parquet"


def validate(dataset: str, df: pd.DataFrame) -> list[str]:
    problems = []
    if len(df) < MIN_ROWS.get(dataset, 1):
        problems.append(f"only {len(df)} rows (< {MIN_ROWS[dataset]})")
    dup = df["code"].duplicated().sum()
    if dup:
        problems.append(f"{dup} duplicate codes")
    price_col = "close" if "close" in df else "nav"
    if price_col in df and df[price_col].notna().mean() < 0.5:
        problems.append(f"{price_col} mostly missing")
    return problems


def collect_snapshots(target: dt.date, force: bool) -> dict:
    results = {}
    fetched_at = now_hkt().isoformat(timespec="seconds")
    for dataset, chain in DATASETS.items():
        path = snapshot_path(dataset, target)
        if path.exists() and not force:
            results[dataset] = {"ok": True, "skipped": "exists"}
            continue
        try:
            source, df = first_ok(chain)
        except Exception as e:
            log.error("%s: %s", dataset, e)
            results[dataset] = {"ok": False, "error": str(e)[:500]}
            continue
        df = df.drop_duplicates("code")
        problems = validate(dataset, df)
        stale = None
        if "data_date" in df and df["data_date"].notna().any():
            dd = df["data_date"].mode().iloc[0]
            stale = dd != target.isoformat()
        if "nav_date" in df and dataset == "open":
            stale = df["nav_date"].iloc[0] != target.isoformat()
        if stale:
            problems.append("data not yet updated for target date")
        if problems and dataset in {"open", "etf"} and stale:
            # Don't write a stale snapshot under today's date; the morning retry will pick it up.
            results[dataset] = {"ok": False, "source": source, "problems": problems}
            continue
        df["source"] = source
        df["fetched_at"] = fetched_at
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(path, index=False, compression="zstd")
        results[dataset] = {"ok": not problems, "source": source, "rows": len(df), "problems": problems}
        log.info("%s: %d rows from %s %s", dataset, len(df), source, problems or "")
    return results


def refresh_reference(target: dt.date) -> dict:
    """Weekly (Mondays or when missing): fund names/types and purchase status."""
    import akshare as ak
    out = {}
    jobs = {"fund_names": ak.fund_name_em, "fund_purchase": ak.fund_purchase_em}
    for name, fn in jobs.items():
        path = REF / f"{name}.parquet"
        if path.exists() and target.weekday() != 0:
            continue
        try:
            df = retry(fn, name=name)
            df.columns = [str(c) for c in df.columns]
            if "基金代码" in df:
                df["基金代码"] = df["基金代码"].astype(str).str.zfill(6)
            df = df.loc[:, ~df.columns.duplicated()]
            df = df[[c for c in df.columns if c not in {"-", "序号", "拼音缩写", "拼音全称"}]]
            df.to_parquet(path, index=False, compression="zstd")
            out[name] = {"ok": True, "rows": len(df)}
        except Exception as e:
            out[name] = {"ok": False, "error": str(e)[:300]}
    return out


def refresh_indexes() -> dict:
    import akshare as ak
    out = {}
    for sym in INDEXES:
        try:
            df = retry(lambda: ak.stock_zh_index_daily(symbol=sym), name=sym)
            df = df[["date", "close"]].tail(2600)
            path = HISTORY / "index" / f"{sym}.csv"
            path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(path, index=False)
            out[sym] = {"ok": True, "last": str(df["date"].iloc[-1])}
        except Exception as e:
            out[sym] = {"ok": False, "error": str(e)[:300]}
    return out


# ---------- per-code history for holdings + watchlist (small, diffable CSVs) ----------

def fetch_history(code: str, kind: str, start: str = "20150101") -> pd.DataFrame:
    """Return date, price where price is back-adjusted close (ETF/LOF) or accumulated NAV (open fund)."""
    import akshare as ak
    if kind in {"etf", "lof"}:
        def em():
            df = ak.fund_etf_hist_em(symbol=code, period="daily", start_date=start, end_date="20500101", adjust="hfq")
            return pd.DataFrame({"date": pd.to_datetime(df["日期"]).dt.date.astype(str), "price": _num(df["收盘"]),
                                 "basis": "hfq_close"})

        def sina():
            prefix = "sh" if code[0] in "56" else "sz"
            df = ak.fund_etf_hist_sina(symbol=prefix + code)
            return pd.DataFrame({"date": df["date"].astype(str), "price": _num(df["close"]), "basis": "raw_close"})
        _, df = first_ok([("eastmoney", em), ("sina", sina)])
    else:
        def nav():
            df = ak.fund_open_fund_info_em(symbol=code, indicator="累计净值走势")
            return pd.DataFrame({"date": pd.to_datetime(df["净值日期"]).dt.date.astype(str),
                                 "price": _num(df["累计净值"]), "basis": "acc_nav"})
        _, df = first_ok([("eastmoney", nav)])
    return df.dropna(subset=["price"]).drop_duplicates("date").sort_values("date")


def update_history(codes: dict[str, str]) -> dict:
    out = {}
    for code, kind in codes.items():
        path = HISTORY / "nav" / f"{code}.csv"
        try:
            if path.exists():
                old = pd.read_csv(path, dtype={"date": str})
                start = (dt.date.fromisoformat(old["date"].iloc[-1]) - dt.timedelta(days=10)).strftime("%Y%m%d")
                new = fetch_history(code, kind, start=start)
                if not new.empty and new["basis"].iloc[0] != old["basis"].iloc[0]:
                    new = fetch_history(code, kind)  # basis changed (fallback source): rebuild
                    df = new
                else:
                    df = pd.concat([old, new]).drop_duplicates("date", keep="last").sort_values("date")
            else:
                df = fetch_history(code, kind)
            path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(path, index=False)
            out[code] = {"ok": True, "last": df["date"].iloc[-1] if len(df) else None}
        except Exception as e:
            out[code] = {"ok": False, "error": str(e)[:300]}
    return out


def write_latest(target: dt.date) -> None:
    """Small agent-facing snapshot of holdings + watchlist (< 200 lines)."""
    holdings = {h["code"]: h for h in load_holdings()}
    rows = []
    for code, kind in watch_codes().items():
        path = HISTORY / "nav" / f"{code}.csv"
        if not path.exists():
            continue
        h = pd.read_csv(path, dtype={"date": str})
        if len(h) < 2:
            continue
        p = h["price"].tolist()
        last = p[-1]

        def ret(n):
            return round((last / p[-1 - n] - 1) * 100, 2) if len(p) > n else None
        rows.append({"code": code, "type": kind, "held": code in holdings, "date": h["date"].iloc[-1],
                     "r_1d%": ret(1), "r_5d%": ret(5), "r_20d%": ret(20), "r_60d%": ret(60)})
    df = pd.DataFrame(rows)
    LATEST.mkdir(parents=True, exist_ok=True)
    body = md_table(df) if not df.empty else "_no history yet_"
    (LATEST / "snapshot.md").write_text(
        f"# Latest snapshot (target date {target}, built {now_hkt():%Y-%m-%d %H:%M} HKT)\n\n"
        "Returns use back-adjusted close (ETF/LOF) or accumulated NAV (open funds).\n\n" + body + "\n",
        encoding="utf-8")


def write_manifest() -> None:
    manifest = {}
    for ds_dir in sorted((RAW / "funds").glob("*")):
        files = sorted(ds_dir.rglob("*.parquet"))
        if files:
            manifest[f"funds/{ds_dir.name}"] = {"files": len(files), "first": files[0].stem, "last": files[-1].stem,
                                               "last_sha256": sha256_file(files[-1])}
    news = sorted((RAW / "news").rglob("*.jsonl")) if (RAW / "news").exists() else []
    if news:
        manifest["news"] = {"files": len(news), "first": news[0].stem, "last": news[-1].stem}
    write_json(DATA / "manifest.json", manifest)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", type=dt.date.fromisoformat)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    now = now_hkt()
    # Before 16:00 HKT today's session isn't settled: the morning catch-up targets the previous trading day.
    ref = now.date() if now.hour >= 16 else now.date() - dt.timedelta(days=1)
    target = args.date or last_trading_day(ref)
    log.info("target trading day %s", target)
    res = {"snapshots": collect_snapshots(target, args.force), "reference": refresh_reference(target),
           "indexes": refresh_indexes(), "history": update_history(watch_codes())}
    write_latest(target)
    write_manifest()
    core_ok = all(res["snapshots"].get(k, {}).get("ok") for k in ("etf", "open"))
    status = {"target_date": str(target), "ok": core_ok,
              "detail": {k: {kk: (str(vv)[:160] if kk == "error" else vv) for kk, vv in v.items()}
                         for k, v in res["snapshots"].items()}}
    if core_ok:
        status["last_ok_date"] = str(target)
    update_status("funds", status)
    log_run("collect_funds", core_ok, target=str(target), result=res)
    return 0 if core_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
