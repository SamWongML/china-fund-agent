from pathlib import Path

import numpy as np
import pandas as pd

from cfa import adjust

REPO = Path(__file__).resolve().parents[1]


def test_listed_split_and_dividend():
    dates = [str(d.date()) for d in pd.bdate_range("2026-01-05", periods=6)]
    # 1% a day, a 1:2 split before day 3, a 0.05 cash dividend going ex on day 5
    raw = [1.00, 1.01, 1.01 ** 2 / 2, 1.01 ** 3 / 2]
    raw += [raw[-1] * 1.01 - 0.05]
    raw = np.array(raw + [raw[-1] * 1.01])
    acts = pd.DataFrame({"date": [dates[2], dates[4]], "kind": ["split", "div"], "value": [2.0, 0.05]})
    price, events = adjust.adjust(dates, raw, acts)
    rets = price[1:] / price[:-1] - 1
    assert price[-1] == raw[-1]
    assert [e["kind"] for e in events] == ["split", "div"] and events[0]["source"] == "listed"
    assert np.all(np.abs(rets - 0.01) < 0.002)          # no fake crash, no dividend drop


def test_unlisted_split_is_detected_and_snapped():
    dates = [str(d.date()) for d in pd.bdate_range("2026-01-05", periods=4)]
    raw = np.array([4.0, 4.04, 2.03, 2.05])             # 1:2 split plus a small market move
    price, events = adjust.adjust(dates, raw)
    assert events == [{"date": dates[2], "kind": "split", "factor": 0.5, "source": "detected"}]
    assert abs(price[2] / price[1] - 1 - (2.03 / 2.02 - 1)) < 1e-9


def test_limit_moves_are_not_splits():
    dates = [str(d.date()) for d in pd.bdate_range("2024-09-24", periods=4)]
    raw = np.array([1.0, 1.2, 1.44, 1.2])               # ChiNext ETF +20%, +20%, -16.7%
    price, events = adjust.adjust(dates, raw)
    assert events == [] and np.allclose(price, raw)


def test_total_return_nav_chains_growth():
    nav = np.array([1.0, 1.01, 0.51, 0.52])             # split on day 3; growth rate says +1%
    tr = adjust.total_return_nav(nav, np.array([np.nan, 1.0, 1.0, np.nan]))
    assert abs(tr[2] / tr[1] - 1.01) < 1e-9 and tr[-1] == nav[-1]


def test_repo_histories_have_no_impossible_moves_after_adjustment():
    for f in sorted((REPO / "data" / "history" / "nav").glob("*.csv")):
        h = pd.read_csv(f, dtype={"date": str})
        raw = (h["raw"] if "raw" in h and h["raw"].notna().all() else h["price"]).to_numpy(float)
        price, _ = adjust.adjust(h["date"].tolist(), raw)
        r = price[1:] / price[:-1]
        assert ((r >= adjust.JUMP_LO) & (r <= adjust.JUMP_HI)).all(), f.name
