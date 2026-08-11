#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 江源区, 吉林省.

This is a forwarding script. The canonical build script lives at:
    scripts/build/build_江源区_data.py
"""
import sys
from pathlib import Path

CANONICAL = Path(__file__).resolve().parent / "scripts" / "build" / "build_江源区_data.py"
if CANONICAL.exists():
    exec_globals = {"__file__": str(CANONICAL), "__name__": "__main__"}
    exec(CANONICAL.read_text(encoding="utf-8"), exec_globals)
else:
    print(f"ERROR: Canonical build script not found: {CANONICAL}", file=sys.stderr)
    sys.exit(1)
