"""Monthly housekeeping: refresh the trading calendar, check its horizon, report repo size."""
from __future__ import annotations

import subprocess

from .common import ROOT, calendar_horizon_days, log, log_run, refresh_calendar, update_status


def main() -> int:
    n = refresh_calendar()
    horizon = calendar_horizon_days()
    size = subprocess.run(["git", "count-objects", "-vH"], cwd=ROOT, capture_output=True, text=True).stdout
    du = subprocess.run(["du", "-sh", "data"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    warn = horizon < 30
    update_status("maintenance", {"calendar_days": n, "calendar_horizon_days": horizon, "calendar_warning": warn,
                                  "data_size": du, "git_objects": size.strip().replace("\n", "; ")})
    log_run("maintenance", not warn, calendar_horizon_days=horizon, data_size=du)
    log.info("calendar %d days, horizon %d days, %s", n, horizon, du)
    return 1 if warn else 0


if __name__ == "__main__":
    raise SystemExit(main())
