import json

from cfa import brief


def test_markdown_subset_renders_sections_lists_tables_and_calls():
    md = """# News digest 2026-10-14

_Thin coverage._

## Top 5
1. **CPI** rose 0.9%, chips fell -3.65% and bonds +0.2%.
2. See `news/daily` and [MERICS](https://merics.org/x).

## Theme read-through
- ai_compute: **−**, the AI selloff.
- gov_bonds: **+**, PBOC injection.
- banks: **0**, nothing.

## Calendar
- Oct 15:
  - TSMC call
  - EU council
- Oct 16

## Calls
| code | name | call | % | r_4w |
|---|---|---|---|---|
| 159819 | AI ETF | Watch | 42% | -15.99 |
Verdict: **Buy 64%** on 510300.
"""
    title, lede, body = brief.md_to_html(md)
    assert title == "News digest 2026-10-14"
    assert "<i>Thin coverage.</i>" in lede
    assert body.count("<section>") == body.count("</section>") == 4
    assert "<ol><li><b>CPI</b> rose 0.9%" in body                     # unsigned numbers stay plain
    assert 'class="down">▼-3.65%' in body and 'class="up">▲+0.2%' in body
    assert "<code>news/daily</code>" in body and 'href="https://merics.org/x"' in body
    assert 'tone t-neg' in body and 'tone t-pos' in body and 'tone t-0' in body
    assert "<ul><li>Oct 15:<ul><li>TSMC call</li><li>EU council</li></ul></li><li>Oct 16</li></ul>" in body
    assert 'b-watch">Watch<' in body and 'class="pbar"' in body
    assert 'b-buy">Buy 64%<' in body
    assert "<script" not in body


def test_html_is_escaped():
    _, lede, _ = brief.md_to_html("<script>alert(1)</script> & **x**")
    assert "&lt;script&gt;" in lede and "<b>x</b>" in lede


def test_color_convention_flips(root, monkeypatch):
    monkeypatch.setattr(brief, "load_universe", lambda: {"briefs": {"up_color": "green"}})
    assert brief.colors()["up"] == "#1e7b4f"
    monkeypatch.setattr(brief, "load_universe", lambda: {})
    assert brief.colors()["up"] == "#c0392b"


def test_tasks_write_fixed_paths_and_index(root):
    (root / "news" / "daily").mkdir(parents=True, exist_ok=True)
    (root / "news" / "daily" / "2026-10-13.md").write_text("# News digest 2026-10-13\n## A\n- x\n")
    (root / "news" / "daily" / "2026-10-14.md").write_text("# News digest 2026-10-14\n## A\n- y\n")
    (root / "data" / "latest").mkdir(parents=True, exist_ok=True)
    (root / "data" / "latest" / "snapshot.md").write_text(
        "# Latest snapshot (target date 2026-10-15, built x)\n\n| code | type | held | date | r_1d% | r_5d% | r_20d% |"
        "\n|---|---|---|---|---|---|---|\n| 510300 | etf | False | 2026-10-15 | -1.21 | -3.35 | -8.52 |\n"
        "| 512010 | etf | False | 2026-10-15 | 0.8 | -1.31 | 0.8 |\n")
    (root / "data" / "history" / "nav").mkdir(parents=True, exist_ok=True)
    (root / "data" / "history" / "nav" / "510300.csv").write_text(
        "date,raw,price,volume,basis\n" + "".join(f"2026-09-{d:02d},4,{4 + d / 100},1,adj_close\n"
                                                   for d in range(1, 21)))
    (root / "briefs").mkdir(exist_ok=True)
    (root / "briefs" / "morning.md").write_text("# Morning brief\n## News\n1. a\n")
    w = root / "weekly" / "2026-W42"
    w.mkdir(parents=True, exist_ok=True)
    (w / "digest.md").write_text("# Weekly digest\n## Summary\n- risk-off\n")
    (w / "inputs.json").write_text(json.dumps({"asof": "2026-10-16", "regime": {
        "label": "risk-off", "sh000300_ma200_gap_pct": -11.01, "breadth_above_ma200_pct": 15.7}}))
    (root / "research" / "themes").mkdir(parents=True, exist_ok=True)
    (root / "research" / "themes" / "2026-10.md").write_text("# Theme scout 2026-10\n## Active\n- ai\n")

    assert brief.news(None).name == "news.html"
    assert "2026-10-14" in (root / "briefs" / "news.html").read_text()   # newest digest by default
    m = brief.morning("2026-10-16").read_text()
    assert "沪深" not in m and "510300" in m and "<svg" in m and "Moves on 2026-10-15" in m
    wk = brief.weekly("2026-W42").read_text()
    assert "risk-off" in wk and "▼-11.01%" in wk and "15.7%" in wk
    assert brief.themes_page(None).name == "themes.html"
    brief.news("2026-10-13")                                              # same path, overwritten
    assert "2026-10-13" in (root / "briefs" / "news.html").read_text()
    idx = (root / "briefs" / "index.html").read_text()
    assert all(f'href="{t}.html"' in idx for t in ("news", "morning", "weekly", "themes"))
    man = json.loads((root / "briefs" / "manifest.json").read_text())
    assert set(man) == {"news", "morning", "weekly", "themes"}
