"""Render one-page HTML briefs from what the scheduled tasks already write. No LLM tokens are spent on HTML.

The agent writes (or already wrote) a small Markdown file; this script turns it into a self-contained page with
inline CSS and inline SVG, and adds the tables and charts it can compute from repo data itself (price moves,
sparklines, p_up bars, theme stats). Each task has one fixed output path that is overwritten on every run;
git history keeps the old versions.

    python -m cfa.brief news    [--date 2026-10-14]   # news/daily/<D>.md          -> briefs/news.html
    python -m cfa.brief morning [--date 2026-10-16]   # briefs/morning.md          -> briefs/morning.html
    python -m cfa.brief weekly  [--week 2026-W42]     # weekly/<W>/digest.md       -> briefs/weekly.html
    python -m cfa.brief themes  [--month 2026-10]     # research/themes/<M>.md     -> briefs/themes.html
    python -m cfa.brief index                         # briefs/index.html (also refreshed by every render)

Prints one line. Agents: run it, don't open the HTML.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import html
import json
import re
from pathlib import Path

from .common import (CONFIG, HISTORY, JOURNAL, LATEST, NEWS, ROOT, WEEKLY, iso_week_label, load_holdings,
                     load_universe, load_yaml, now_hkt, read_json, today_hkt, write_json)

BRIEFS = ROOT / "briefs"
REPO_URL = "https://github.com/SamWongML/china-fund-agent"
DISCLAIMER = "Research signals from public data, not financial advice."
TITLES = {"news": "Daily news digest", "morning": "Morning brief", "weekly": "Sunday advice",
          "themes": "Theme scout"}
CALL = {"buy": "buy", "add": "buy", "sell": "sell", "trim": "sell", "watch": "watch", "hold": "hold"}

# ---------------------------------------------------------------- style (one shared sheet, ~4 KB per page)

CSS = """
:root{--bg:#f7f4ee;--card:#fffdf9;--ink:#1d1c1a;--muted:#6b665d;--rule:#e4ddd0;--accent:#0b4f6c;
--up:%(up)s;--down:%(down)s;--flat:#8a8478;--buy:#0f6b4f;--sell:#a8322d;--watch:#8a6d1d;--hold:#55606e;
--bar:#d9d2c3;--mark:#1d1c1a}
@media (prefers-color-scheme:dark){:root{--bg:#141414;--card:#1c1c1b;--ink:#ece8e1;--muted:#a19a8e;
--rule:#2f2d2a;--accent:#7fb8d4;--up:%(up_d)s;--down:%(down_d)s;--buy:#4fb98f;--sell:#e0716a;--watch:#d4b25a;
--hold:#9aa6b4;--bar:#3a3833;--mark:#ece8e1}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",
"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;-webkit-text-size-adjust:100%%}
main{max-width:920px;margin:0 auto;padding:28px 16px 48px}
header.top{border-bottom:3px double var(--rule);padding-bottom:14px;margin-bottom:18px}
.kicker{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);font-weight:600}
h1{font:600 30px/1.2 Georgia,"Noto Serif SC","Songti SC",serif;margin:6px 0 4px}
.meta{color:var(--muted);font-size:13px}
.lede{font:18px/1.5 Georgia,"Noto Serif SC","Songti SC",serif;margin:14px 0 0}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:0 0 18px}
.kpi{background:var(--card);border:1px solid var(--rule);border-radius:8px;padding:10px 12px}
.kpi b{display:block;font:600 22px/1.2 Georgia,serif;font-variant-numeric:tabular-nums}
.kpi>span{color:var(--muted);font-size:12px}
section{background:var(--card);border:1px solid var(--rule);border-radius:10px;padding:14px 18px;margin:0 0 14px}
h2{font:600 19px/1.3 Georgia,"Noto Serif SC","Songti SC",serif;margin:0 0 8px;padding-bottom:6px;
border-bottom:1px solid var(--rule)}
h3{font-size:15px;margin:14px 0 4px}
p{margin:6px 0}ul,ol{margin:6px 0;padding-left:22px}li{margin:3px 0}
a{color:var(--accent)}code{font:12.5px ui-monospace,SFMono-Regular,Menlo,monospace;background:var(--bg);
padding:1px 4px;border-radius:4px}
blockquote{margin:8px 0;padding:6px 12px;border-left:3px solid var(--accent);color:var(--muted)}
.tw{overflow-x:auto;margin:8px 0}
table{border-collapse:collapse;width:100%%;font-size:13.5px;font-variant-numeric:tabular-nums}
th{text-align:left;font-weight:600;color:var(--muted);font-size:12px;border-bottom:1px solid var(--ink);
padding:4px 8px;white-space:nowrap}
td{padding:5px 8px;border-bottom:1px solid var(--rule);vertical-align:top}
td.n,th.n,td.nw,td.nm{text-align:right;white-space:nowrap}td.nw,td.nm{text-align:left}th.w{white-space:normal}
.up{color:var(--up)}.down{color:var(--down)}.flat{color:var(--flat)}
.badge{display:inline-block;min-width:46px;text-align:center;font-size:12px;font-weight:600;border-radius:4px;
padding:1px 6px;color:#fff;white-space:nowrap}
.b-buy{background:var(--buy)}.b-sell{background:var(--sell)}.b-watch{background:var(--watch)}
.b-hold{background:var(--hold)}
.pbar{display:inline-block;position:relative;width:110px;height:8px;background:var(--bar);border-radius:4px;
vertical-align:middle;margin-left:6px}
.pbar i{position:absolute;top:-3px;width:3px;height:14px;background:var(--mark);border-radius:1px}
.pbar u{position:absolute;top:-2px;width:1px;height:12px;background:var(--muted);text-decoration:none}
.pbar s{position:absolute;top:-2px;width:1px;height:12px;border-left:1px dashed var(--buy);text-decoration:none}
.tone{display:inline-block;width:22px;text-align:center;font-weight:700;border-radius:4px;margin-right:6px}
.t-pos{background:var(--up);color:#fff}.t-neg{background:var(--down);color:#fff}.t-0{background:var(--bar)}
svg.spark{vertical-align:middle}
.legend{color:var(--muted);font-size:12px;margin:4px 0 0}
footer{color:var(--muted);font-size:12px;margin-top:22px;border-top:1px solid var(--rule);padding-top:10px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}
.cards a{display:block;text-decoration:none;color:inherit}
.cards section:hover{border-color:var(--accent)}
@media print{body{background:#fff}section,.kpi{break-inside:avoid;border-color:#ccc}}
@media (max-width:560px){h1{font-size:24px}section{padding:12px}.pbar{width:70px}}
"""


def colors() -> dict:
    """China mainland convention by default: red = up, green = down. Set briefs.up_color: green to flip."""
    cfg = load_universe().get("briefs") or {}
    red, green, red_d, green_d = "#c0392b", "#1e7b4f", "#ef6f62", "#4fb98f"
    if str(cfg.get("up_color", "red")).lower() == "green":
        return {"up": green, "down": red, "up_d": green_d, "down_d": red_d}
    return {"up": red, "down": green, "up_d": red_d, "down_d": green_d}


# ---------------------------------------------------------------- small helpers

def esc(s) -> str:
    return html.escape(str(s if s is not None else ""), quote=True)


def num_class(v) -> str:
    try:
        f = float(str(v).replace("−", "-").rstrip("%"))
    except ValueError:
        return ""
    return "up" if f > 0 else "down" if f < 0 else "flat"


def signed(v, suffix="%") -> str:
    """A move with its sign, an arrow and the up/down colour. Value is copied, never recomputed."""
    if v in (None, ""):
        return '<span class="flat">–</span>'
    c = num_class(v)
    arrow = {"up": "▲", "down": "▼"}.get(c, "")
    s = str(v)
    s = s if s.startswith(("-", "+")) or c != "up" else "+" + s
    return f'<span class="{c}">{arrow}{esc(s)}{suffix}</span>'


def pbar(p: float, floor: float | None = None) -> str:
    """Probability on a 0-100 track with the coin-flip line and, if given, the action floor."""
    p = max(0.0, min(1.0, p))
    fl = f'<s style="left:{floor * 100:.0f}%" title="action floor"></s>' if floor else ""
    return (f'<span class="pbar" role="img" aria-label="{p * 100:.0f}%"><u style="left:50%"></u>{fl}'
            f'<i style="left:calc({p * 100:.1f}% - 1px)"></i></span>')


def badge(label: str, pct: str | None = None) -> str:
    k = label.lower()
    text = label.capitalize() + (f" {pct}%" if pct else "")
    return f'<span class="badge b-{CALL.get(k, "hold")}">{esc(text)}</span>'


def sparkline(code: str, n: int = 60, w: int = 84, h: int = 22) -> str:
    """Inline SVG of the last n adjusted prices in data/history/nav/<code>.csv; empty if no history."""
    p = HISTORY / "nav" / f"{code}.csv"
    if not p.exists():
        return ""
    with p.open(encoding="utf-8") as f:
        vals = [float(r["price"]) for r in csv.DictReader(f) if r.get("price") not in (None, "")][-n:]
    if len(vals) < 5:
        return ""
    lo, hi = min(vals), max(vals)
    rng = (hi - lo) or 1.0
    pts = " ".join(f"{i * (w - 2) / (len(vals) - 1) + 1:.1f},{h - 2 - (v - lo) / rng * (h - 4):.1f}"
                   for i, v in enumerate(vals))
    c = "up" if vals[-1] > vals[0] else "down" if vals[-1] < vals[0] else "flat"
    return (f'<svg class="spark {c}" width="{w}" height="{h}" viewBox="0 0 {w} {h}" aria-hidden="true">'
            f'<polyline fill="none" stroke="currentColor" stroke-width="1.4" points="{pts}"/></svg>')


def names() -> dict[str, str]:
    """code -> display name, from holdings and the newest weekly inputs (no network)."""
    out: dict[str, str] = {}
    weeks = sorted(p for p in WEEKLY.glob("*/inputs.json"))
    if weeks:
        d = read_json(weeks[-1], {}) or {}
        rows = (d.get("candidates") or []) + (d.get("themes") or []) + (d.get("rule_calls") or [])
        rows += [p for t in d.get("watch_themes") or [] for p in t.get("products") or []]
        for r in rows:
            if r.get("code") and r.get("name"):
                out.setdefault(str(r["code"]), str(r["name"]))
    for h in load_holdings():
        if h.get("name"):
            out[h["code"]] = str(h["name"])
    return out


# ---------------------------------------------------------------- Markdown -> HTML (the subset the skills write)

INLINE_CODE = re.compile(r"`([^`]+)`")
LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+|[\w./#-]+)\)")
BOLD = re.compile(r"\*\*(.+?)\*\*")
ITAL = re.compile(r"(?<![\w*])[_*](?![\s_*])(.+?)(?<![\s_*])[_*](?![\w*])")
SIGNED_PCT = re.compile(r"(?<![\w.%])([+\-−]\d+(?:\.\d+)?)%")
CALL_PCT = re.compile(r"\b(Buy|Sell|Watch|Hold)\s+(\d{1,2})%")
TONE = re.compile(r"^`?([\w/ ]+?)`?:\s*\*\*\s*([+\-−–0])\s*\*\*\s*,?\s*(.*)$")


def inline(s: str) -> str:
    codes: list[str] = []

    def keep(m):
        codes.append(f"<code>{esc(m.group(1))}</code>")
        return f"\x00{len(codes) - 1}\x00"

    s = INLINE_CODE.sub(keep, s)
    s = esc(s)
    s = CALL_PCT.sub(lambda m: badge(m.group(1), m.group(2)), s)
    s = SIGNED_PCT.sub(lambda m: signed(m.group(1).replace("−", "-")), s)
    s = LINK.sub(lambda m: f'<a href="{link_href(m.group(2))}">{m.group(1)}</a>', s)
    s = BOLD.sub(r"<b>\1</b>", s)
    s = ITAL.sub(r"<i>\1</i>", s)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], s)


def link_href(href: str) -> str:
    if href.startswith(("http://", "https://", "#")):
        return href
    return f"{REPO_URL}/blob/main/{href.lstrip('./')}"   # repo paths open on GitHub


def list_item(text: str) -> str:
    m = TONE.match(text.strip())
    if m:
        t = {"+": "pos", "-": "neg", "−": "neg", "–": "neg"}.get(m.group(2), "0")
        sym = {"pos": "+", "neg": "−", "0": "0"}[t]
        return f'<span class="tone t-{t}">{sym}</span><b>{esc(m.group(1))}</b> {inline(m.group(3))}'
    return inline(text)


LIST_RE = re.compile(r"^(\s*)([-*•]|\d+[.)])\s+(.*)$")


def render_list(lines: list[str]) -> str:
    items: list[list] = []   # [indent, ordered, text]
    for ln in lines:
        m = LIST_RE.match(ln)
        if m:
            items.append([len(m.group(1).expandtabs(2)), m.group(2)[0].isdigit(), m.group(3)])
        elif items:
            items[-1][2] += " " + ln.strip()
    out: list[str] = []
    stack: list[tuple[int, str]] = []
    for indent, ordered, text in items:
        while stack and indent < stack[-1][0]:
            out.append(f"</li></{stack.pop()[1]}>")
        if not stack or indent > stack[-1][0]:
            tag = "ol" if ordered else "ul"
            stack.append((indent, tag))
            out.append(f"<{tag}><li>")
        else:
            out.append("</li><li>")
        out.append(list_item(text))
    while stack:
        out.append(f"</li></{stack.pop()[1]}>")
    return "".join(out)


def split_row(ln: str) -> list[str]:
    return [c.strip() for c in ln.strip().strip("|").split("|")]


def table_cell(raw: str, head: str) -> tuple[str, str]:
    """Returns (css class, html). Recognises call labels, probabilities and signed moves."""
    s = raw.strip().strip("*").strip()
    if re.fullmatch(r"(?i)buy|sell|watch|hold", s):
        return "", badge(s)
    if re.fullmatch(r"\d{1,2}%", s) and head.strip() in {"%", "p_up", "chance", "prob"}:
        return "n", f"{esc(s)}{pbar(int(s[:-1]) / 100)}"
    if re.fullmatch(r"[+\-−]?\d+(?:\.\d+)?%?", s) and s.lstrip("+-−")[:1].isdigit():
        if s[0] in "+-−":
            return "n", signed(s.rstrip("%").replace("−", "-"), "%" if s.endswith("%") else "")
        return "n", esc(s)
    return "", inline(raw)


def render_table(lines: list[str]) -> str:
    rows = [split_row(x) for x in lines if not re.fullmatch(r"\|?[\s:|-]+\|?", x.strip())]
    if not rows:
        return ""
    head, body = rows[0], rows[1:]
    out = ['<div class="tw"><table><thead><tr>']
    numeric = []
    for i, h in enumerate(head):
        col = [r[i] for r in body if i < len(r)]
        numeric.append(bool(col) and all(re.fullmatch(r"[+\-−]?\d+(?:\.\d+)?%?|–|-|", c.strip()) for c in col))
        out.append(f'<th class="{"n" if numeric[i] else ""}">{inline(h)}</th>')
    out.append("</tr></thead><tbody>")
    for r in body:
        out.append("<tr>")
        for i, c in enumerate(r):
            cls, cell = table_cell(c, head[i] if i < len(head) else "")
            if not cls and i < len(head) and head[i].strip().lower() in {"name", "fund", "product"}:
                cls = "nm"   # fund names: one line, the table scrolls instead
            out.append(f'<td class="{cls}">{cell}</td>')
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def md_to_html(text: str) -> tuple[str, str, str]:
    """Markdown -> (title, lede html, body html). Each ## section becomes a card."""
    lines = text.splitlines()
    title, lede, body = "", [], []
    in_section = False
    para: list[str] = []
    target = lede

    def flush():
        if para:
            target.append(f"<p>{inline(' '.join(x.strip() for x in para))}</p>")
            para.clear()

    i = 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            flush()
            i += 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", ln)
        if m:
            flush()
            level, txt = len(m.group(1)), m.group(2).strip()
            if level == 1 and not title:
                title = txt
            elif level <= 2:
                if in_section:
                    body.append("</section>")
                body.append(f"<section><h2>{inline(txt)}</h2>")
                in_section, target = True, body
            else:
                target.append(f"<h3>{inline(txt)}</h3>")
            i += 1
            continue
        if ln.lstrip().startswith("|"):
            flush()
            block = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                block.append(lines[i])
                i += 1
            target.append(render_table(block))
            continue
        if ln.startswith(">"):
            flush()
            block = []
            while i < len(lines) and lines[i].startswith(">"):
                block.append(lines[i].lstrip(">").strip())
                i += 1
            target.append(f"<blockquote>{inline(' '.join(block))}</blockquote>")
            continue
        if LIST_RE.match(ln):
            flush()
            block = []
            while i < len(lines) and lines[i].strip() and (LIST_RE.match(lines[i]) or lines[i].startswith((" ", "\t"))):
                block.append(lines[i])
                i += 1
            target.append(render_list(block))
            continue
        para.append(ln)
        i += 1
    flush()
    if in_section:
        body.append("</section>")
    return title, "".join(lede), "".join(body)


# ---------------------------------------------------------------- page shell

def kpis(items: list[tuple[str, str]]) -> str:
    if not items:
        return ""
    return '<div class="kpis">' + "".join(f'<div class="kpi"><b>{v}</b><span>{esc(k)}</span></div>'
                                          for k, v in items) + "</div>"


def page(task: str, title: str, subtitle: str, lede: str, body: str, source: str) -> str:
    gen = now_hkt().strftime("%Y-%m-%d %H:%M HKT")
    src = f'<a href="{REPO_URL}/blob/main/{esc(source)}">{esc(source)}</a>' if source else ""
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta name="color-scheme" content="light dark"><title>{esc(title)}</title>'
            f"<style>{CSS % colors()}</style></head><body><main>"
            f'<header class="top"><div class="kicker">{esc(TITLES.get(task, task))} · '
            f'<a href="index.html">all briefs</a></div><h1>{esc(title)}</h1>'
            f'<div class="meta">{esc(subtitle)}</div>{f"<div class=lede>{lede}</div>" if lede else ""}</header>'
            f"{body}<footer>{DISCLAIMER} Generated {gen} from {src}. Red/green follows "
            f"{'the mainland convention (red = up)' if colors()['up'].startswith('#c0') else 'green = up'}; "
            f"arrows show direction either way.</footer></main></body></html>\n")


def write(task: str, html_text: str, meta: dict) -> Path:
    BRIEFS.mkdir(parents=True, exist_ok=True)
    out = BRIEFS / f"{task}.html"
    out.write_text(html_text, encoding="utf-8")
    man = read_json(BRIEFS / "manifest.json", {}) or {}
    man[task] = {**meta, "generated": now_hkt().strftime("%Y-%m-%d %H:%M"), "bytes": len(html_text.encode())}
    write_json(BRIEFS / "manifest.json", man)
    render_index(man)
    return out


def render_index(man: dict | None = None) -> Path:
    man = man if man is not None else (read_json(BRIEFS / "manifest.json", {}) or {})
    cards = []
    for task in ("morning", "news", "weekly", "themes"):
        m = man.get(task)
        if not m:
            continue
        cards.append(f'<a href="{task}.html"><section><div class="kicker">{esc(TITLES[task])}</div>'
                     f'<h2>{esc(m.get("title", ""))}</h2><div class="meta">{esc(m.get("subtitle", ""))}<br>'
                     f'updated {esc(m.get("generated", ""))} HKT</div></section></a>')
    body = f'<div class="cards">{"".join(cards) or "<p>No briefs yet.</p>"}</div>'
    out = BRIEFS / "index.html"
    BRIEFS.mkdir(parents=True, exist_ok=True)
    out.write_text(page("index", "China fund briefs", "Latest output of each scheduled task", "", body, ""),
                   encoding="utf-8")
    return out


def from_markdown(task: str, md_path: Path, subtitle: str, pre: str = "", post: str = "") -> Path:
    text = md_path.read_text(encoding="utf-8")
    title, lede, body = md_to_html(text)
    title = title or TITLES[task]
    rel = str(md_path.relative_to(ROOT))
    return write(task, page(task, title, subtitle, lede, pre + body + post, rel),
                 {"title": title, "subtitle": subtitle, "source": rel})


# ---------------------------------------------------------------- tasks

def newest(pattern: str, base: Path) -> Path | None:
    files = sorted(p for p in base.glob(pattern) if re.fullmatch(r"\d{4}-\d{2}(-\d{2})?\.md", p.name))
    return files[-1] if files else None


def news(date: str | None) -> Path:
    p = NEWS / "daily" / f"{date}.md" if date else newest("*.md", NEWS / "daily")
    if not p or not p.exists():
        raise SystemExit(f"no news digest found ({p})")
    return from_markdown("news", p, f"News for {p.stem} · for the Sunday advisor")


def snapshot_rows() -> tuple[str, list[dict]]:
    """Rows of data/latest/snapshot.md (already computed by cfa.collect_funds)."""
    p = LATEST / "snapshot.md"
    if not p.exists():
        return "", []
    text = p.read_text(encoding="utf-8")
    asof = (re.search(r"target date (\d{4}-\d{2}-\d{2})", text) or [None, ""])[1]
    lines = [x for x in text.splitlines() if x.startswith("|")]
    if len(lines) < 3:
        return asof, []
    head = split_row(lines[0])
    return asof, [dict(zip(head, split_row(x))) for x in lines[2:]]


def moves_table(rows: list[dict], label: dict[str, str]) -> str:
    nm = names()
    out = ['<div class="tw"><table><thead><tr><th></th><th>code</th><th>name</th><th class="n">1 day</th>'
           '<th class="n">5 days</th><th class="n">20 days</th><th>60-day trend</th></tr></thead><tbody>']
    for r in rows:
        c = r["code"]
        out.append(f'<tr><td class="meta">{esc(label.get(c, ""))}</td><td>{esc(c)}</td><td class="nm">{esc(nm.get(c, ""))}</td>'
                   f'<td class="n">{signed(r.get("r_1d%"))}</td><td class="n">{signed(r.get("r_5d%"))}</td>'
                   f'<td class="n">{signed(r.get("r_20d%"))}</td><td>{sparkline(c)}</td></tr>')
    out.append("</tbody></table></div>")
    return "".join(out)


def morning(date: str | None) -> Path:
    p = BRIEFS / "morning.md"
    if not p.exists():
        raise SystemExit("write briefs/morning.md first")
    asof, rows = snapshot_rows()
    held = {h["code"] for h in load_holdings()}
    core = [str(c) for c in (load_universe().get("portfolio") or {}).get("core") or []]
    key = [c for c in ["510300", "510500", "159915", *core] if c not in held]
    by = {r["code"]: r for r in rows}

    def r1(r):
        try:
            return float(r.get("r_1d%") or 0)
        except ValueError:
            return 0.0

    rest = sorted((r for r in rows if r["code"] not in held and r["code"] not in key), key=r1)
    pick: list[dict] = []
    label: dict[str, str] = {}
    for c, tag in [(c, "held") for c in sorted(held)] + [(c, "core" if c in core else "index") for c in key]:
        if c in by and c not in label:
            pick.append(by[c])
            label[c] = tag
    for r in rest[-3:][::-1] + rest[:3]:
        if r["code"] not in label:
            pick.append(r)
            label[r["code"]] = "mover"
    pre = ""
    if pick:
        pre = (f'<section><h2>Moves on {esc(asof)}</h2>{moves_table(pick, label)}<p class="legend">Held funds '
               "first, then the core sleeve and broad indices, then the 3 biggest gainers and losers on the "
               "watchlist. Returns are split- and dividend-adjusted, from data/latest/snapshot.md.</p></section>")
    d = date or str(today_hkt())
    return from_markdown("morning", p, f"{d} · prices as of {asof or 'n/a'} close", pre=pre)


def call_rows(week: str) -> list[dict]:
    from . import journal
    held = {h["code"] for h in load_holdings()}
    nm = names()
    out = []
    for r in journal.read_all():
        if r.get("week") != week or r.get("p_up") is None:
            continue
        p = float(r["p_up"])
        v = journal.view(r["action"], p, r["code"] in held)
        shown = round((1 - p if v == "sell" else p) * 100)
        out.append({"code": r["code"], "name": r.get("name") or nm.get(r["code"], ""), "view": v, "pct": shown,
                    "p_up": p, "action": r["action"], "theme": r.get("theme") or "",
                    "group": "Holdings" if r["code"] in held else (r.get("theme") or "New picks"),
                    "override": bool(r.get("override"))})
    return out


def calls_section(rows: list[dict], floor: float) -> str:
    if not rows:
        return ""
    groups: dict[str, list[dict]] = {}
    for r in rows:
        groups.setdefault(r["group"], []).append(r)
    order = sorted(groups, key=lambda g: (g != "Holdings", g == "New picks", g))
    out = ['<section><h2>Every call at a glance</h2><div class="tw"><table><thead><tr><th>group</th><th>code</th>'
           '<th>name</th><th>call</th><th class="n w">chance it beats the CSI 300</th><th>logged</th>'
           '<th>60-day trend</th></tr></thead><tbody>']
    for g in order:
        for r in sorted(groups[g], key=lambda x: -x["p_up"]):
            act = esc(r["action"]) + (" · override" if r["override"] else "")
            out.append(f'<tr><td class="meta">{esc(g)}</td><td>{esc(r["code"])}</td><td class="nm">{esc(r["name"])}</td>'
                       f'<td>{badge(r["view"], str(r["pct"]))}</td>'
                       f'<td class="n">{r["p_up"] * 100:.0f}%{pbar(r["p_up"], floor)}</td><td class="meta">{act}</td>'
                       f'<td>{sparkline(r["code"])}</td></tr>')
    out.append(f'</tbody></table></div><p class="legend">Marker = p_up, solid line = 50%, dashed line = the '
               f"{floor * 100:.0f}% floor a Buy or Sell must clear. From journal/decisions.jsonl.</p></section>")
    return "".join(out)


def weekly(week: str | None) -> Path:
    week = week or iso_week_label(today_hkt())
    wdir = WEEKLY / week
    p = wdir / "digest.md"
    if not p.exists() and (wdir / "digest.preview.md").exists():
        p = wdir / "digest.preview.md"
    if not p.exists():
        raise SystemExit(f"no digest for {week}")
    inp = read_json(wdir / "inputs.json", {}) or {}
    reg = inp.get("regime") or {}
    floor = float((load_yaml(CONFIG / "risk_rules.yaml") or {}).get("min_confidence_to_act", 0.6))
    rows = call_rows(week)
    k = []
    if reg.get("label"):
        k.append(("market regime", esc(reg["label"])))
    if reg.get("sh000300_ma200_gap_pct") is not None:
        k.append(("CSI 300 vs its 200-day average", signed(reg["sh000300_ma200_gap_pct"])))
    if reg.get("sh000300_r_12w_pct") is not None:
        k.append(("CSI 300, last 12 weeks", signed(reg["sh000300_r_12w_pct"])))
    if reg.get("breadth_above_ma200_pct") is not None:
        k.append(("funds above their 200-day average", f'{esc(reg["breadth_above_ma200_pct"])}%'))
    if rows:
        k.append(("calls logged", str(len(rows))))
        k.append(("Buy calls", str(sum(r["view"] == "buy" for r in rows))))
    pre = kpis(k) + calls_section(rows, floor)
    sub = f"Week {week} · data as of {inp.get('asof', 'n/a')}" + (" · PREVIEW" if "preview" in p.name else "")
    return from_markdown("weekly", p, sub, pre=pre)


def themes_page(month: str | None) -> Path:
    base = ROOT / "research" / "themes"
    p = base / f"{month}.md" if month else newest("*.md", base)
    if not p or not p.exists():
        raise SystemExit(f"no theme note found ({p})")
    wl = (load_yaml(ROOT / "watchlist" / "themes.yaml") or {}).get("themes") or []
    weeks = sorted(WEEKLY.glob("*/inputs.json"))
    stats = {t["id"]: t for t in ((read_json(weeks[-1], {}) or {}).get("watch_themes") or [])} if weeks else {}
    status_n = {s: sum(t.get("status") == s for t in wl) for s in ("active", "watch-only", "retired")}
    pre = kpis([(f"{s} themes", str(n)) for s, n in status_n.items()])
    rows = ['<section><h2>Watchlist now</h2><div class="tw"><table><thead><tr><th>theme</th><th>status</th>'
            '<th>stage</th><th class="n w">news this week</th><th class="n w">index families</th>'
            '<th class="n w">launched in 6 months</th><th class="n w">crowded products</th><th>review by</th>'
            "</tr></thead><tbody>"]
    for t in wl:
        s = stats.get(t.get("id"), {})
        rows.append(f'<tr><td><b>{esc(t.get("name"))}</b><br><span class="meta">{esc(t.get("id"))}</span></td>'
                    f'<td>{esc(t.get("status"))}</td><td>{esc(t.get("stage"))}</td>'
                    + "".join(f'<td class="n">{esc(s.get(f, "–"))}</td>'
                              for f in ("news_this_week", "index_families", "launched_6m", "crowded_products"))
                    + f'<td class="nw">{esc(t.get("review_by"))}</td></tr>')
    rows.append('</tbody></table></div><p class="legend">From watchlist/themes.yaml and the newest weekly build. '
                "A launch wave or crowded products are late-cycle warnings.</p></section>")
    pre += "".join(rows)
    return from_markdown("themes", p, f"Theme scout {p.stem}", pre=pre)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("task", choices=["news", "morning", "weekly", "themes", "index"])
    ap.add_argument("--date")
    ap.add_argument("--week")
    ap.add_argument("--month")
    a = ap.parse_args()
    if a.task == "index":
        out = render_index()
    else:
        out = {"news": lambda: news(a.date), "morning": lambda: morning(a.date), "weekly": lambda: weekly(a.week),
               "themes": lambda: themes_page(a.month)}[a.task]()
    print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
