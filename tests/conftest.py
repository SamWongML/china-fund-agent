"""Run every test against a throwaway repo root so nothing touches real data."""
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TMP = Path(tempfile.mkdtemp(prefix="cfa-test-"))
shutil.copytree(REPO / "config", TMP / "config")
(TMP / "portfolio").mkdir()
os.environ["CFA_ROOT"] = str(TMP)
subprocess.run(["git", "init", "-q", str(TMP)], check=True)

import pytest  # noqa: E402


@pytest.fixture
def root():
    return TMP
