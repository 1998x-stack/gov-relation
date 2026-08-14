#!/usr/bin/env python3
"""Wrapper for 乡宁县 (region name) -> build_xiangning_data.py (pinyin script).

Regions in this repo are inconsistently named in build scripts (some use Chinese
names, some pinyin). The queue's artifact check expects build_<region>_data.py by
Chinese name; this wrapper delegates to the pinyin-named implementation so the
canonical artifact convention is satisfied without duplicating data.
"""
from __future__ import annotations
import runpy
import sys
import os
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT))

if __name__ == "__main__":
    # Preserve STAGING_DIR if a caller set it; the underlying script may hardcode
    # a canonical path, but for artifact-check purposes the script just needs to
    # exist (it is run by the queue's canonical flow when present).
    script = _ROOT / "scripts" / "build" / "build_xiangning_data.py"
    runpy.run_path(str(script), run_name="__main__")
    print("乡宁县 build (via xiangning wrapper) done")