import datetime as dt
import json

import numpy as np
import pandas as pd
import pytest

from cfa import check_digest, collect_news, guard, journal, scorecard, weekly_build
from cfa import common


def write_holdings(root, rows):
    import yaml
    (root / "portfolio" / "holdings.yaml").write_text(yaml.safe_dump({"holdings": rows}, allow_unicode=True))


def write_hist(root, code, start, prices):
    d = pd.bdate_range(start, periods=len(prices))
    p = root / "data" / "history" / "nav"
    p.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({"date": d.date.astype(str), "price": prices, "basis": "hfq_close"}).to_csv(p / f"{code}.csv", index=False)


def test_norm_text_strips_wire_prefix():
    assert collect_news.norm_text("【财联社10月15日电】央行宣布降准") == "央行宣布降准"
    assert collect_news.norm_text("财联社10月15日电，央行宣布降准") == "央行宣布降准"


def test_near_duplicates_merge(root, monkeypatch):
    now = common.now_hkt().replace(microsecond=0)
    items = [
        {"ts": now.isoformat(), "source": "eastmoney_7x24", "title": "央行宣布下调存款准备金率0.5个百分点", "summary": "", "url": "", "level": ""},
        {"ts": now.isoformat(), "source": "cls_key", "title": "央行：下调存款准备金率0.5个百分点", "summary": "", "url": "", "level": "AB"},
        {"ts": now.isoformat(), "source": "futu", "title": "美联储维持利率不变", "summary": "", "url": "", "level": ""},
    ]
    cfg = common.load_yaml(common.CONFIG / "sources.yaml")
    themes = common.load_universe()["themes"]
    for i in items:
        collect_news.tag(i, cfg, themes)
    stats = collect_news.merge(items)
    assert stats == {"added": 2, "merged": 1}
    day = collect_news.load_day(now.date())
    rrr = next(i for i in day if "准备金" in i["title"])
    assert rrr["also"] == ["cls_key"] and rrr["level"] == "AB" and rrr["region"] == "CN"
    assert next(i for i in day if "美联储" in i["title"])["region"] == "US"


def test_scorecard_uses_first_price_after_decision(root):
    write_hist(root, "510300", "2026-01-05", list(np.linspace(1.0, 2.0, 60)))
    idx = root / "data" / "history" / "index"
    idx.mkdir(parents=True, exist_ok=True)
    d = pd.bdate_range("2026-01-05", periods=60)
    pd.DataFrame({"date": d.date.astype(str), "close": np.full(60, 4000.0)}).to_csv(idx / "sh000300.csv", index=False)
    rec = {"id": "x", "ts": "2026-01-05T08:00:00+08:00", "code": "510300", "action": "buy", "confidence": 0.7,
           "horizon_weeks": 2, "held": False}
    g = scorecard.grade(rec, scorecard.load_index("sh000300"))
    assert g["status"] == "closed"
    assert str(g["entry_date"]) == "2026-01-06"      # strictly after the decision date
    assert g["excess_pct"] > 0 and g["hit"] is True
    sell = scorecard.grade(rec | {"action": "sell"}, scorecard.load_index("sh000300"))
    assert sell["hit"] is False


def test_journal_validation(root):
    write_holdings(root, [{"code": "510300", "units": 100, "cost": 4, "type": "etf"}])
    base = {"code": "510300", "action": "hold", "confidence": 0.6, "horizon_weeks": 4, "thesis": "t",
            "falsifiers": "f", "data_asof": "2026-10-16"}
    assert journal.validate(base) == []
    assert any("not in portfolio" in e for e in journal.validate(base | {"code": "512480"}))
    assert any("action" in e for e in journal.validate(base | {"action": "yolo"}))


def test_check_digest_rules_and_numbers(root, monkeypatch):
    write_holdings(root, [{"code": "510300", "units": 100, "cost": 4, "type": "etf"}])
    week = "2026-W42"
    wdir = root / "weekly" / week
    wdir.mkdir(parents=True, exist_ok=True)
    inputs = {"ready": True, "holdings": [{"code": "510300", "kind": "etf", "r_4w": 3.21}],
              "candidates": [{"code": "512480", "r_1m": 5.5}], "themes": [],
              "risk_rules": common.load_yaml(common.CONFIG / "risk_rules.yaml")}
    (wdir / "inputs.json").write_text(json.dumps(inputs))
    body = ("## Summary\nok\n## Holdings: top 3\n510300 hold, r_4w 3.21%\n## New picks\n512480 watch, 1m 5.50%\n"
            "## Risks and what would change my mind\nx\n## Data notes\ny\n")
    (wdir / "digest.md").write_text(body)
    monkeypatch.setattr(journal, "PATH", root / "journal" / "decisions.jsonl")
    monkeypatch.setattr(common, "iso_week_label", lambda d: week)
    monkeypatch.setattr(journal, "iso_week_label", lambda d: week)
    rec = {"action": "hold", "confidence": 0.6, "horizon_weeks": 4, "thesis": "t", "falsifiers": "f", "data_asof": "2026-10-16"}
    journal.add(rec | {"code": "510300"})
    journal.add(rec | {"code": "512480", "action": "watch"})
    assert check_digest.check(week) == []
    (wdir / "digest.md").write_text(body.replace("3.21%", "9.87%"))
    assert any("9.87%" in e for e in check_digest.check(week))
    (wdir / "digest.md").write_text(body)
    journal.add(rec | {"code": "159995", "action": "watch"})
    errs = check_digest.check(week)
    assert any("159995" in e and "candidates" in e for e in errs)


def test_guard_blocks_protected_writes(monkeypatch, capsys):
    import io
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps({"tool_name": "Edit", "tool_input": {"file_path": "/r/portfolio/holdings.yaml"}})))
    assert guard.main() == 2
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps({"tool_name": "Bash", "tool_input": {"command": "echo x >> journal/decisions.jsonl"}})))
    assert guard.main() == 2
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps({"tool_name": "Bash", "tool_input": {"command": "cat portfolio/holdings.yaml"}})))
    assert guard.main() == 0


def test_screen_and_facts(root):
    asof = dt.date(2026, 10, 16)
    rng = np.random.default_rng(0)
    n = 40
    codes = [f"{510000 + i:06d}" for i in range(n)]
    rank = pd.DataFrame({"code": codes, "name": [f"基金{i}" for i in range(n)], "type": "ETF-场内",
                         "nav_date": str(asof), "nav": 1.0, "acc_nav": 1.0, "inception": "2020-01-01",
                         **{c: rng.normal(0, 5, n) for c in ["r_1w", "r_1m", "r_3m", "r_6m", "r_1y", "r_2y", "r_3y", "r_ytd", "r_since"]}})
    etf = pd.DataFrame({"code": codes, "name": rank["name"], "close": 1.0, "turnover_cny": 1e8, "premium_pct": 0.1, "shares": 1e9})
    for ds, df in (("exchange_rank", rank), ("etf", etf)):
        p = weekly_build.RAW / "funds" / ds / "year=2026" / "month=10" / f"{asof}.parquet"
        p.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(p)
    cands = weekly_build.screen(asof, held={codes[0]})
    assert 0 < len(cands) <= 5 and codes[0] not in set(cands["code"])
    write_hist(root, codes[1], "2025-06-02", list(np.linspace(1, 1.5, 300)))
    f = weekly_build.facts(codes[1], "etf", weekly_build.latest_snapshot("etf", asof, 6))
    assert f["r_1w"] > 0 and f["above_ma20"] and f["premium_pct"] == 0.1
