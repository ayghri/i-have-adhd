"""ADR 0004: shared-core sections must not drift across family skills."""

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check_shared_core.py"


def test_shared_core_in_sync():
    result = subprocess.run(
        [sys.executable, str(SCRIPT)], capture_output=True, text=True
    )
    assert result.returncode == 0, (
        f"shared-core drift detected:\n{result.stdout}\n{result.stderr}"
    )
