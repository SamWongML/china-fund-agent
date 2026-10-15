"""Hourly news collector: AKShare flash feeds + RSS -> data/raw/news/YYYY/MM/YYYY-MM-DD.jsonl (HKT dates).

Exact and near-duplicate items are merged (the duplicate's source is added to `also`), every item is tagged
with region, themes and a mechanical importance score. The LLM never reads this raw file directly; it reads
the ranked daily input built by cfa.news_prep.
"""
from __future__ import annotations

import datetime as dt
import email.utils
import hashlib
import html
import json
import re
import xml.etree.ElementTree as ET

import pandas as pd
import requests

from .common import CONFIG, HKT, RAW, load_universe, load_yaml, log, log_run, now_hkt, retry, update_status

UA = {"User-Agent": "Mozilla/5.0 (china-fund-agent personal research; contact via GitHub)"}
NEWS_DIR = RAW / "news"
SNIPPET = 280


def norm_text(s: str) -> str:
    s = html.unescape(s or "")
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"^【[^】]{0,40}】", "", s.strip())          # 【财联社10月15日电】-style prefixes
    s = re.sub(r"^(财联社|新华社|央视新闻)?\d{1,2}月\d{1,2}日(电|讯)[，,]?", "", s)
    return re.sub(r"\s+", " ", s).strip()


def shingles(s: str, n: int = 3) -> set[str]:
    s = re.sub(r"[\W_]+", "", s.lower())
    return {s[i:i + n] for i in range(max(len(s) - n + 1, 1))}


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0


def to_hkt(value) -> dt.datetime | None:
    if value is None or (isinstance(value, float) and value != value):
        return None
    try:
        ts = pd.to_datetime(value)
    except Exception:
        try:
            ts = pd.Timestamp(email.utils.parsedate_to_datetime(str(value)))
        except Exception:
            return None
    if ts is pd.NaT:
        return None
    ts = ts.to_pydatetime()
    return ts.replace(tzinfo=HKT) if ts.tzinfo is None else ts.astimezone(HKT)


# ---------- fetchers ----------

def fetch_akshare(feed: dict) -> list[dict]:
    import akshare as ak
    df = retry(lambda: getattr(ak, feed["func"])(**(feed.get("args") or {})), attempts=2, name=feed["name"])
    items = []
    for r in df.to_dict("records"):
        title = norm_text(str(r.get("标题") or ""))
        body = norm_text(str(r.get("内容") or r.get("摘要") or ""))
        if "发布日期" in r and "发布时间" in r:
            when = to_hkt(f"{r['发布日期']} {r['发布时间']}")
        else:
            when = to_hkt(r.get("发布时间") or r.get("时间"))
        url = str(r.get("链接") or "")
        if url and not url.startswith("http") and feed["func"] == "stock_info_global_em":
            url = f"https://finance.eastmoney.com/a/{url}.html"
        if not (title or body) or when is None:
            continue
        items.append({"ts": when, "source": feed["name"], "title": title or body[:60], "summary": body[:SNIPPET],
                      "url": url, "level": feed.get("level", "")})
    return items


def fetch_rss(feed: dict) -> list[dict]:
    resp = retry(lambda: requests.get(feed["url"], headers=UA, timeout=20), attempts=2, name=feed["name"])
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    items = []
    for node in root.iter():
        tag = node.tag.split("}")[-1]
        if tag not in {"item", "entry"}:
            continue
        get = lambda name: next((c for c in node if c.tag.split("}")[-1] == name), None)  # noqa: E731
        title = norm_text((get("title").text if get("title") is not None else "") or "")
        link_node = get("link")
        link = (link_node.text or link_node.attrib.get("href", "")) if link_node is not None else ""
        desc_node = get("description") if get("description") is not None else get("summary")
        desc = norm_text(desc_node.text if desc_node is not None and desc_node.text else "")
        date_node = next((get(n) for n in ("pubDate", "published", "updated", "date") if get(n) is not None), None)
        when = to_hkt(date_node.text) if date_node is not None else None
        if title and when:
            items.append({"ts": when, "source": feed["name"], "title": title, "summary": desc[:SNIPPET],
                          "url": link.strip(), "level": "", "region": feed.get("region"),
                          "official": bool(feed.get("official"))})
    return items


# ---------- tagging ----------

def tag(item: dict, cfg: dict, themes: dict) -> dict:
    text = f"{item['title']} {item['summary']}"
    if not item.get("region"):
        item["region"] = "CN"
        for region in ("US", "GLOBAL"):
            if any(k in text for k in cfg["region_keywords"][region]):
                item["region"] = region
                break
    item["themes"] = sorted(t for t, spec in themes.items() if any(k in text for k in spec.get("keywords") or []))
    official = item.pop("official", False) or any(k in text[:60] for k in cfg.get("official_keywords") or [])
    macro_hits = sum(1 for k in cfg.get("macro_keywords") or [] if k in text)
    score = (3 if item.get("level") == "AB" else 0) + (2 if official else 0) + min(macro_hits, 3) \
        + (1 if item["themes"] else 0)
    item["official"] = bool(official)
    item["base_score"] = score
    return item


def item_id(item: dict) -> str:
    key = re.sub(r"[\W_]+", "", (item["title"] or item["summary"])[:80].lower())
    return hashlib.sha1(key.encode()).hexdigest()[:16]


# ---------- storage ----------

def day_path(d: dt.date):
    return NEWS_DIR / f"{d.year}" / f"{d.month:02d}" / f"{d.isoformat()}.jsonl"


def load_day(d: dt.date) -> list[dict]:
    p = day_path(d)
    if not p.exists():
        return []
    return [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]


def save_day(d: dt.date, items: list[dict]) -> None:
    p = day_path(d)
    p.parent.mkdir(parents=True, exist_ok=True)
    items.sort(key=lambda x: x["ts"])
    p.write_text("".join(json.dumps(i, ensure_ascii=False) + "\n" for i in items), encoding="utf-8")


def merge(new_items: list[dict], horizon_days: int = 2, near_dup: float = 0.6) -> dict[str, int]:
    today = now_hkt().date()
    days = {today - dt.timedelta(days=i): load_day(today - dt.timedelta(days=i)) for i in range(horizon_days)}
    by_id = {i["id"]: i for items in days.values() for i in items}
    index = [(i, shingles(i["title"] + i["summary"][:60])) for i in by_id.values()]
    added = merged = 0
    for it in new_items:
        it["id"] = item_id(it)
        d = dt.date.fromisoformat(it["ts"][:10])
        if d not in days:  # older than horizon or future-dated: keep only if recent
            if (today - d).days > 7 or d > today:
                continue
            days[d] = load_day(d)
            for i in days[d]:
                by_id.setdefault(i["id"], i)
        target = by_id.get(it["id"])
        if target is None:
            sh = shingles(it["title"] + it["summary"][:60])
            target = next((i for i, s in index if jaccard(sh, s) >= near_dup), None)
        if target is not None:
            if it["source"] != target["source"] and it["source"] not in target.setdefault("also", []):
                target["also"].append(it["source"])
                if it.get("level") == "AB":
                    target["level"] = "AB"
                merged += 1
            continue
        it["also"] = []
        by_id[it["id"]] = it
        index.append((it, shingles(it["title"] + it["summary"][:60])))
        days[d].append(it)
        added += 1
    for d, items in days.items():
        for i in items:
            i["score"] = i.get("base_score", 0) + min(len(i.get("also") or []), 3)
        if items:
            save_day(d, items)
    return {"added": added, "merged": merged}


def main() -> int:
    cfg = load_yaml(CONFIG / "sources.yaml")
    themes = load_universe().get("themes") or {}
    collected, health = [], {}
    for feed in cfg.get("akshare_feeds") or []:
        try:
            got = fetch_akshare(feed)
            health[feed["name"]] = {"ok": True, "n": len(got)}
            collected += got
        except Exception as e:
            health[feed["name"]] = {"ok": False, "error": str(e)[:160]}
    for feed in cfg.get("rss") or []:
        try:
            got = fetch_rss(feed)
            health[feed["name"]] = {"ok": True, "n": len(got)}
            collected += got
        except Exception as e:
            health[feed["name"]] = {"ok": False, "error": str(e)[:160]}
    for it in collected:
        it["ts"] = it["ts"].isoformat(timespec="seconds")
        tag(it, cfg, themes)
    # Prefer the "key" CLS feed first so its AB level survives the merge.
    collected.sort(key=lambda x: (x.get("level") != "AB",))
    stats = merge(collected)
    ok_sources = sum(1 for h in health.values() if h["ok"])
    ok = ok_sources >= 2
    update_status("news", {"last_run": now_hkt().isoformat(timespec="seconds"), "ok": ok, "sources": health, **stats})
    log_run("collect_news", ok, ok_sources=ok_sources, **stats)
    log.info("news: %s, %d/%d sources ok", stats, ok_sources, len(health))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
