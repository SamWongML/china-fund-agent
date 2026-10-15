"""Shared helpers: paths, time, config, retries, trading calendar, run log and status."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import logging
import os
import time
from pathlib import Path
from typing import Any, Callable

import yaml

ROOT = Path(os.environ.get("CFA_ROOT") or Path(__file__).resolve().parents[2])
CONFIG = ROOT / "config"
DATA = ROOT / "data"
RAW = DATA / "raw"
HISTORY = DATA / "history"
REF = DATA / "ref"
LATEST = DATA / "latest"
NEWS = ROOT / "news"
WEEKLY = ROOT / "weekly"
JOURNAL = ROOT / "journal"
STATE = ROOT / "state"
PORTFOLIO = ROOT / "portfolio"

HKT = dt.timezone(dt.timedelta(hours=8))  # HK and Beijing are both UTC+8, no DST

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"), format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("cfa")


def now_hkt() -> dt.datetime:
    return dt.datetime.now(HKT)


def today_hkt() -> dt.date:
    return now_hkt().date()


def iso_week_label(d: dt.date) -> str:
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


def load_yaml(path: Path) -> Any:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def retry(fn: Callable[[], Any], attempts: int = 3, backoff: float = 3.0, name: str = "") -> Any:
    last: Exception | None = None
    for i in range(attempts):
        try:
            return fn()
        except Exception as e:  # network libraries raise many types
            last = e
            log.warning("%s attempt %d/%d failed: %s", name or fn, i + 1, attempts, e)
            time.sleep(backoff * (2**i))
    raise RuntimeError(f"{name} failed after {attempts} attempts: {last}")


def first_ok(chain: list[tuple[str, Callable[[], Any]]], attempts: int = 2) -> tuple[str, Any]:
    """Try each (source_name, fetch) in order; return the first that succeeds."""
    errors = []
    for name, fn in chain:
        try:
            return name, retry(fn, attempts=attempts, name=name)
        except Exception as e:
            errors.append(f"{name}: {e}")
    raise RuntimeError("all sources failed -> " + " | ".join(errors))


# ---------- run log and status ----------

def log_run(job: str, ok: bool, **details: Any) -> None:
    """Append to state/runs/<job>.jsonl (one file per job so concurrent workflows never conflict)."""
    path = STATE / "runs" / f"{job}.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    rec = {"ts": now_hkt().isoformat(timespec="seconds"), "job": job, "ok": ok, **details}
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")


def read_status(section: str) -> dict:
    return read_json(STATE / "status" / f"{section}.json", {}) or {}


def update_status(section: str, payload: dict) -> None:
    """Merge payload into state/status/<section>.json."""
    status = read_status(section)
    status.update(payload)
    status["updated"] = now_hkt().isoformat(timespec="seconds")
    write_json(STATE / "status" / f"{section}.json", status)


# ---------- trading calendar ----------

CAL_PATH = REF / "trade_calendar.csv"


def refresh_calendar() -> int:
    import akshare as ak

    df = retry(ak.tool_trade_date_hist_sina, name="tool_trade_date_hist_sina")
    dates = sorted({str(d)[:10] for d in df["trade_date"]})
    CAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    CAL_PATH.write_text("trade_date\n" + "\n".join(dates) + "\n", encoding="utf-8")
    return len(dates)


def trading_days() -> list[dt.date]:
    if not CAL_PATH.exists():
        refresh_calendar()
    lines = CAL_PATH.read_text(encoding="utf-8").split()[1:]
    return [dt.date.fromisoformat(x) for x in lines]


def is_trading_day(d: dt.date) -> bool:
    return d in set(trading_days())


def last_trading_day(on_or_before: dt.date) -> dt.date:
    days = [d for d in trading_days() if d <= on_or_before]
    return days[-1]


def calendar_horizon_days() -> int:
    days = trading_days()
    return (days[-1] - today_hkt()).days if days else -1


# ---------- holdings / universe ----------

def load_holdings() -> list[dict]:
    data = load_yaml(PORTFOLIO / "holdings.yaml")
    rows = data.get("holdings") or []
    out = []
    for r in rows:
        if not r or not r.get("code"):
            continue
        r = dict(r)
        r["code"] = str(r["code"]).zfill(6)
        out.append(r)
    return out


def load_universe() -> dict:
    return load_yaml(CONFIG / "universe.yaml")


def watch_codes() -> dict[str, str]:
    """code -> type ('etf'|'lof'|'open') for holdings plus configured theme ETFs and benchmarks."""
    codes: dict[str, str] = {}
    uni = load_universe()
    for theme in (uni.get("themes") or {}).values():
        for c in theme.get("etfs") or []:
            codes[str(c).zfill(6)] = "etf"
    for h in load_holdings():
        codes[h["code"]] = (h.get("type") or guess_type(h["code"])).lower()
    return codes


def guess_type(code: str) -> str:
    code = str(code).zfill(6)
    if code[:2] in {"51", "52", "56", "58", "15"} and not code.startswith("16"):
        return "etf"
    if code.startswith("16") or code.startswith("50"):
        return "lof"
    return "open"


def md_table(df) -> str:
    """Render a DataFrame as a GitHub markdown table without extra dependencies."""
    cols = [str(c) for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for row in df.itertuples(index=False):
        cells = ["" if (v is None or (isinstance(v, float) and v != v)) else str(v) for v in row]
        lines.append("| " + " | ".join(c.replace("|", "/") for c in cells) + " |")
    return "\n".join(lines)
