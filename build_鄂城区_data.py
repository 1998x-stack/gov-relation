#!/usr/bin/env python3
"""Wrapper for the canonical 鄂城区 (Echeng, Ezhou) build script.

This is a thin launcher that runs the canonical script in scripts/build/,
which writes data/database/鄂城区_network.db and data/graph/鄂城区_network.gexf.

Canonical: scripts/build/build_鄂城区_data.py
Task ID:   hubei_鄂城区
"""
import runpy
import sys
from pathlib import Path

_here = Path(__file__).resolve().parent
_canonical = _here / "scripts" / "build" / "build_鄂城区_data.py"
if not _canonical.exists():
    sys.stderr.write(f"ERROR: canonical build script not found: {_canonical}\n")
    sys.exit(1)
runpy.run_path(str(_canonical), run_name="__main__")