import datetime as dt
import json

import numpy as np
import pandas as pd
import pytest
import yaml

from cfa import backtest, check_digest, common, journal, themes


def write_holdings(root, rows):
    (root / "portfolio" / "holdings.yaml").write_text(yaml.safe_dump({"holdings": rows}, allow_unicode=True))


THEME = {"id": "robotics", "name": "Robotics", "status": "active", "stage": "growth", "added": "2026-10-15",
         "review_by": "2027-01-15", "thesis": "t", "policy": ["p"], "match": ["机器人", "机床"], "exclude": [],
         "news": ["机器人"], "falsifiers": "f"}


def products():
    return pd.DataFrame({
        "code": ["562500", "159530", "159770", "159663", "513000", "159999"],
        "name": ["机器人ETF华夏", "机器人ETF易方达", "机器人ETF天弘", "机床ETF华夏", "港股机器人ETF", "机器人ETF小"],
        "turnover_cny": [4.5e8, 5.2e8, 1.0e8, 7.5e7, 9e8, 1e6], "kind": "etf",
        "inception": ["2022-01-01", "2026-06-01", "2021-01-01", "2023-01-01", "2026-09-01", "2026-09-01"],
    }).assign(family=lambda d: d["name"].map(themes.family))


def test_family_strips_issuer_and_share_class():
    assert themes.family("机器人ETF华夏") == "机器人ETF"
    assert themes.family("科创半导体设备ETF华泰柏瑞") == "科创半导体设备ETF"
    assert themes.family("易方达中证机器人指数A") == "易方达中证机器人指数"


def test_theme_products_one_per_family_and_excludes_cross_border():
    p = themes.theme_products(THEME, products())
    assert list(p["code"]) == ["159530", "159663"]           # most liquid robot issuer + machine tools
    assert int(p.loc[p["code"] == "159530", "issuers"].iloc[0]) == 4
    stats = themes.theme_stats(THEME, products(), dt.date(2026, 10, 15))
    assert stats["products_matched"] == 5 and stats["launched_6m"] == 2   # the HK product is excluded


def test_scan_tags_watched_families():
    t = themes.scan(products(), dt.date(2026, 10, 15), [THEME])
    assert set(t.loc[t["watched_as"] == "robotics", "family"]) == {"机器人ETF", "机床ETF"}
    assert "港股机器人ETF" not in set(t["family"])


def test_watchlist_validation():
    assert themes.validate([THEME]) == []
    bad = THEME | {"id": "Bad Id", "status": "maybe", "match": []}
    errs = themes.validate([bad, THEME, THEME])
    assert any("lower_snake_case" in e for e in errs) and any("status" in e for e in errs)
    assert any("match" in e for e in errs) and any("duplicate" in e for e in errs)


def test_journal_derives_confidence_from_p_up(root, monkeypatch):
    monkeypatch.setattr(journal, "PATH", root / "journal" / "decisions.jsonl")
    write_holdings(root, [{"code": "510300", "units": 100, "cost": 4, "type": "etf"}])
    base = {"code": "510300", "horizon_weeks": 4, "thesis": "t", "falsifiers": "f", "data_asof": "2026-10-16"}
    sell = journal.add(base | {"action": "sell", "p_up": 0.3})
    assert sell["confidence"] == 0.7 and sell["view"] == "sell"
    hold = journal.add(base | {"action": "hold", "p_up": 0.45})
    assert hold["confidence"] == 0.45 and hold["view"] == "sell"   # leans sell, below the floor
    watch = journal.add(base | {"code": "512480", "action": "watch", "p_up": 0.58})
    assert watch["view"] == "watch"
    with pytest.raises(ValueError, match="between"):
        journal.add(base | {"action": "hold", "p_up": 0.95})
    with pytest.raises(ValueError, match="below 0.5"):
        journal.add(base | {"action": "sell", "p_up": 0.6})
    with pytest.raises(ValueError, match="confidence must equal"):
        journal.add(base | {"action": "add", "p_up": 0.7, "confidence": 0.9})


def test_check_digest_requires_three_calls_per_theme(root, monkeypatch):
    write_holdings(root, [{"code": "510300", "units": 100, "cost": 4, "type": "etf"}])
    week = "2026-W43"
    wdir = root / "weekly" / week
    wdir.mkdir(parents=True, exist_ok=True)
    prods = [{"code": c, "family": f"f{i}"} for i, c in enumerate(["562500", "159663", "159206", "159227"])]
    inputs = {"ready": True, "holdings": [{"code": "510300", "kind": "etf"}], "candidates": [], "themes": [],
              "watch_themes": [{"id": "robotics", "curate": True, "products": prods}],
              "risk_rules": common.load_yaml(common.CONFIG / "risk_rules.yaml")}
    (wdir / "inputs.json").write_text(json.dumps(inputs))
    body = ("## Summary\nok\n## Holdings: top 3\n510300 Buy 60%\n## Theme watchlist\n562500 159663 159206\n"
            "## New picks\nnone\n## Risks and what would change my mind\nx\n## Data notes\ny\n")
    (wdir / "digest.md").write_text(body)
    monkeypatch.setattr(journal, "PATH", root / "journal" / "decisions-w43.jsonl")
    monkeypatch.setattr(journal, "iso_week_label", lambda d: week)
    rec = {"action": "watch", "p_up": 0.55, "horizon_weeks": 4, "thesis": "t", "falsifiers": "f",
           "data_asof": "2026-10-23"}
    journal.add(rec | {"code": "510300", "action": "hold"})
    journal.add(rec | {"code": "562500", "theme": "robotics"})
    journal.add(rec | {"code": "159663", "theme": "robotics"})
    errs = check_digest.check(week)
    assert any("theme robotics: 2" in e for e in errs)
    journal.add(rec | {"code": "159206", "theme": "robotics"})
    assert check_digest.check(week) == []
    (wdir / "digest.md").write_text(body.replace("## Theme watchlist\n", ""))
    assert any("Theme watchlist" in e for e in check_digest.check(week))
    (wdir / "digest.md").write_text(body)
    journal.add(rec | {"code": "512480", "theme": "robotics"})
    assert any("512480" in e and "product list" in e for e in check_digest.check(week))


def test_base_rates_by_composite_band(root):
    idx = root / "data" / "history" / "index"
    idx.mkdir(parents=True, exist_ok=True)
    d = pd.bdate_range("2020-01-01", periods=200)
    pd.DataFrame({"date": d.date.astype(str), "close": np.full(200, 4000.0)}).to_csv(idx / "sh000300.csv", index=False)
    codes = [f"c{i}" for i in range(10)]
    # Signal = fund number; fund i drifts up when i is high, so high-composite funds beat a flat benchmark.
    feat = pd.DataFrame(np.tile(np.arange(10.0), (200, 1)), index=d, columns=codes)
    fwd = pd.DataFrame(np.tile(np.linspace(-0.05, 0.05, 10), (200, 1)), index=d, columns=codes)
    rows = backtest.composite_base_rates({"trend_12w": feat}, fwd, d[:150:5], {}, 5)
    by = {r["composite_band"]: r for r in rows}
    assert by["all"]["fund_weeks"] == 300
    assert by["80-100"]["beat_csi300_pct"] == 100.0 and by["0-20"]["beat_csi300_pct"] == 0.0
