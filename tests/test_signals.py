import datetime as dt
import json

import numpy as np
import pandas as pd

from cfa import backtest, check_digest, common, journal, portfolio, signals


def write_hist(root, code, prices, start="2016-01-04", volume=None):
    d = pd.bdate_range(start, periods=len(prices))
    p = root / "data" / "history" / "nav"
    p.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame({"date": d.date.astype(str), "raw": prices, "price": prices, "basis": "adj_close"})
    if volume is not None:
        df["volume"] = volume
    df.to_csv(p / f"{code}.csv", index=False)


def walk(rng, n, drift, vol=0.015, common_move=None):
    r = rng.normal(drift, vol, n) + (common_move if common_move is not None else 0)
    return 1.0 * np.exp(np.cumsum(r))


def test_features_use_only_past_data(root):
    rng = np.random.default_rng(1)
    write_hist(root, "600001", walk(rng, 400, 0.0005))
    p, t = signals.panel(["600001"])
    f1 = signals.features(p, t)
    p2 = p.copy()
    p2.iloc[-1] = p2.iloc[-1] * 3          # a change on the last day must not alter any earlier value
    f2 = signals.features(p2, t)
    for k in ("trend_12w", "ma200_gap", "max_20d", "low_vol"):
        a, b = f1[k].iloc[:-1], f2[k].iloc[:-1]
        assert a.equals(b), k


def test_backtest_accepts_a_real_signal_and_rejects_noise(root, monkeypatch):
    rng = np.random.default_rng(2)
    n_days, codes = 1500, [f"6100{i:02d}" for i in range(12)]
    mkt = rng.normal(0.0002, 0.01, n_days)
    for i, c in enumerate(codes):
        # persistent per-fund drift: past 26-week trend predicts the future
        write_hist(root, c, walk(rng, n_days, 0.0002 * (i - 6), 0.012, mkt))
    monkeypatch.setattr(signals, "weights", lambda: dict(signals.DEFAULT_WEIGHTS))
    res = backtest.run(codes)
    assert res["ok"] and res["funds"] == 12
    assert res["signals"]["trend_26w"]["status"] == "accepted"
    assert res["weight_mult"]["trend_26w"] == 1.0
    assert res["signals"]["rev_4w"]["status"] == "rejected"     # reversal is wrong in a persistent-trend world
    assert (common.JOURNAL / "signal_health.md").exists()


def test_snapshot_flags_crowding_and_clusters(root):
    rng = np.random.default_rng(3)
    n = 400
    base = rng.normal(0, 0.012, n)
    write_hist(root, "620001", walk(rng, n, 0.001, 0.004, base))
    write_hist(root, "620002", walk(rng, n, 0.001, 0.004, base))           # moves with 620001
    other = rng.normal(0, 0.012, n)
    spike = walk(rng, n, 0.0, 0.004, other)
    spike[-3:] *= np.array([1.09, 1.09 * 1.05, 1.09 * 1.05 * 1.02])         # lottery-like jump at the end
    write_hist(root, "620003", spike)
    write_hist(root, "620004", walk(rng, n, 0.0, 0.004, -base))
    p, t = signals.panel(["620001", "620002", "620003", "620004"])
    snap = signals.snapshot(p, t).set_index("code")
    assert "lottery" in snap.at["620003", "crowded"]
    assert snap.at["620001", "cluster"] == snap.at["620002", "cluster"]
    assert snap.at["620003", "cluster"] == "620003"
    assert snap["composite"].between(0, 100).all()


def test_targets_respect_caps_regime_and_clusters(monkeypatch):
    sig = pd.DataFrame({
        "composite": [80, 70, 90, 85, 84, 30], "above_ma200": [True, True, True, True, True, False],
        "crowded": ["", "", "", "", "", ""], "vol60_pct": [15, 2, 25, 25, 25, 30],
        "cluster": ["A", "B", "C", "C", "D", "E"], "trend_26w_rank": [50, 50, 90, 80, 70, 10],
    }, index=["510880", "511010", "700001", "700002", "700003", "700004"])
    monkeypatch.setattr(portfolio, "cfg", lambda: {"core": ["510880", "511010"], "core_pct": 70, "satellite_pct": 30,
                                                   "satellite_slots": 3, "satellite_min_composite": 60,
                                                   "drift_band_pct": 5})
    tg = portfolio.targets(sig, "neutral")
    assert all(v <= 25 for v in tg["core"].values())
    assert set(tg["satellite"]) == {"700001", "700003"}            # 700002 shares a cluster with 700001
    assert portfolio.targets(sig, "risk-off")["satellite"] == {}
    calls = {c["code"]: c for c in portfolio.rule_calls(tg, [{"code": "700004", "value_cny": 1000},
                                                             {"code": "510880", "value_cny": 1000}], sig)}
    assert calls["700004"]["action"] == "sell"                      # not a target, below MA200, weak trend
    assert calls["510880"]["action"] == "trim"                      # 50% held vs 25% target
    assert calls["700001"]["action"] == "buy"


def test_rules_baseline_is_replaced_per_week(root, monkeypatch):
    monkeypatch.setattr(portfolio, "BASELINE", root / "journal" / "rules_baseline.jsonl")
    calls = [{"code": "510300", "action": "hold", "target_weight_pct": 20}]
    portfolio.write_baseline(calls, "2026-W42", dt.date(2026, 10, 16))
    portfolio.write_baseline(calls, "2026-W42", dt.date(2026, 10, 16))
    portfolio.write_baseline(calls, "2026-W43", dt.date(2026, 10, 23))
    rows = portfolio.read_baseline()
    assert [r["week"] for r in rows] == ["2026-W42", "2026-W43"]


def test_journal_override_needs_reason(root):
    (root / "portfolio" / "holdings.yaml").write_text("holdings:\n- {code: '510300', units: 1, cost: 1}\n")
    base = {"code": "510300", "action": "hold", "confidence": 0.6, "horizon_weeks": 4, "thesis": "t",
            "falsifiers": "f", "data_asof": "2026-10-16"}
    assert any("override_reason" in e for e in journal.validate(base | {"override": True}))
    assert journal.validate(base | {"override": True, "override_reason": "policy meeting"}) == []


def test_check_digest_enforces_rules_calls_crowding_and_clusters(root, monkeypatch):
    (root / "portfolio" / "holdings.yaml").write_text("holdings:\n- {code: '510300', units: 100, cost: 4, type: etf}\n")
    week = "2026-W44"
    wdir = root / "weekly" / week
    wdir.mkdir(parents=True, exist_ok=True)
    inputs = {"ready": True, "holdings": [{"code": "510300", "kind": "etf", "crowded": ""}],
              "candidates": [{"code": "512480", "crowded": "1-week gain", "cluster": "512480"},
                             {"code": "159995", "crowded": "", "cluster": "512480"},
                             {"code": "588000", "crowded": "", "cluster": "512480"}],
              "themes": [], "rule_calls": [{"code": "510300", "action": "trim"}],
              "risk_rules": common.load_yaml(common.CONFIG / "risk_rules.yaml")}
    (wdir / "inputs.json").write_text(json.dumps(inputs))
    body = ("## Summary\nok\n## Holdings: top 3\n510300\n## New picks\n512480 159995 588000\n"
            "## Risks and what would change my mind\nx\n## Data notes\ny\n")
    (wdir / "digest.md").write_text(body)
    monkeypatch.setattr(journal, "PATH", root / "journal" / f"decisions-{week}.jsonl")
    monkeypatch.setattr(journal, "iso_week_label", lambda d: week)
    rec = {"confidence": 0.7, "horizon_weeks": 4, "thesis": "t", "falsifiers": "f", "data_asof": "2026-10-30"}
    journal.add(rec | {"code": "510300", "action": "hold"})
    journal.add(rec | {"code": "512480", "action": "buy"})
    journal.add(rec | {"code": "159995", "action": "buy"})
    errs = check_digest.check(week)
    assert any("rules-only call 'trim'" in e for e in errs)
    assert any("512480" in e and "crowded" in e for e in errs)
    assert any("159995" in e and "cluster" in e for e in errs)
