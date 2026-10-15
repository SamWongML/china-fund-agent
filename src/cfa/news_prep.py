"""Build the ranked, size-capped input for the daily news digest.

Writes news/daily/inputs/YYYY-MM-DD.md for one HKT day: top items by mechanical score grouped by region,
a theme hit table and the next two days' macro calendar. The Claude news-digest skill reads only this file.

    python -m cfa.news_prep                 # yesterday (HKT); no-op if the file exists
    python -m cfa.news_prep --date 2026-10-14 --force
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt

import pandas as pd

from .collect_news import load_day
from .common import NEWS, log, log_run, md_table, now_hkt, retry, today_hkt, update_status

MAX_ITEMS = {"CN": 70, "US": 30, "GLOBAL": 25}


def macro_calendar(days: list[dt.date]) -> pd.DataFrame:
    import akshare as ak
    frames = []
    for d in days:
        try:
            df = retry(lambda: ak.macro_info_ws(date=d.strftime("%Y%m%d")), attempts=2, name="macro_info_ws")
            frames.append(df)
        except Exception as e:
            log.warning("calendar %s: %s", d, e)
    if not frames:
        return pd.DataFrame()
    df = pd.concat(frames)
    df["_imp"] = pd.to_numeric(df["重要性"], errors="coerce").fillna(0)
    df = df[df["_imp"] >= 2]
    # Keep the most important events of each day so the second day isn't cut off.
    df["_day"] = df["时间"].astype(str).str[:10]
    df = df.sort_values(["_day", "_imp"], ascending=[True, False]).groupby("_day").head(20).sort_values("时间")
    return df[["时间", "地区", "事件", "重要性", "预期", "前值"]]


def build(d: dt.date) -> str:
    items = load_day(d)
    lines = [f"# News input for {d} (HKT)", "",
             f"{len(items)} unique items collected; showing the top-scored per region. "
             "Score = CLS level A/B (+3) + official source (+2) + macro keywords (≤3) + theme hit (+1) "
             "+ extra sources reporting it (≤3).", ""]
    theme_counts = collections.Counter(t for i in items for t in i.get("themes") or [])
    for region in ("CN", "US", "GLOBAL"):
        sel = sorted((i for i in items if i.get("region") == region), key=lambda i: (-i.get("score", 0), i["ts"]))
        sel = sel[:MAX_ITEMS[region]]
        lines += [f"## {region} ({len(sel)} shown)", ""]
        for i in sorted(sel, key=lambda i: i["ts"]):
            srcs = "+".join([i["source"]] + (i.get("also") or []))
            summary = i["summary"] if i["summary"] and i["summary"][:20] not in i["title"] else ""
            th = f" #{' #'.join(i['themes'])}" if i.get("themes") else ""
            lines.append(f"- [{i['ts'][11:16]}][s{i.get('score', 0)}][{srcs}] {i['title']}"
                         + (f" — {summary[:160]}" if summary else "") + th)
        lines.append("")
    if theme_counts:
        lines += ["## Theme mentions (all items)", "",
                  md_table(pd.DataFrame(theme_counts.most_common(), columns=["theme", "items"])), ""]
    cal = macro_calendar([d + dt.timedelta(days=1), d + dt.timedelta(days=2)])
    lines += ["## Macro calendar, next two days (importance ≥ 2)", "",
              md_table(cal) if not cal.empty else "_calendar unavailable_", ""]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", type=dt.date.fromisoformat)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    d = args.date or (today_hkt() - dt.timedelta(days=1))
    out = NEWS / "daily" / "inputs" / f"{d}.md"
    if out.exists() and not args.force:
        log.info("%s exists, skipping", out)
        return 0
    if not args.date and now_hkt().hour < 6:
        log.info("before 06:00 HKT, yesterday's US session not closed yet; skipping")
        return 0
    text = build(d)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    update_status("news_prep", {"last_date": str(d), "ok": True})
    log_run("news_prep", True, date=str(d), bytes=len(text.encode()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
