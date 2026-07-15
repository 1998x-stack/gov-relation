#!/usr/bin/env python3
"""Repository wrapper for the china-gov-network data/tmp processor."""

from pathlib import Path
import runpy

SCRIPT = Path(__file__).resolve().parents[1] / ".agents" / "skills" / "china-gov-network" / "scripts" / "process_tmp.py"
runpy.run_path(str(SCRIPT), run_name="__main__")

