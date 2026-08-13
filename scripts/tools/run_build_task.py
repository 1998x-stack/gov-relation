#!/usr/bin/env python3
"""Reusable: run a queue task's build script into a clean staging dir + validate.

Handles the 3 repo build-script path styles:
  1. STAGING env override (兴安盟) / STAGING_DIR var — run with STAGING_DIR set
  2. _STAGING_CANDIDATE that prefers existing dir (乌达区/满洲里) — pre-create it
  3. _CURRENT_DIR (writes to scripts/build) — run then move into staging

Usage:
  python3 scripts/tools/run_build_task.py --task inner_mongolia_西丰县 \
      --build scripts/build/build_西丰县_data.py --stage data/tmp/liaoning_西丰县
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True, help="task_id")
    ap.add_argument("--build", required=True, help="build script path (relative to repo)")
    ap.add_argument("--stage", required=True, help="staging dir (relative to repo)")
    a = ap.parse_args()

    build = (REPO_ROOT / a.build).resolve()
    stage = (REPO_ROOT / a.stage).resolve()
    stage.mkdir(parents=True, exist_ok=True)

    # Run with PYTHONPATH=repo (for scripts that probe parents[2]/[3]) and
    # STAGING_DIR=stage (for scripts honoring env). Pre-creating stage improves
    # _STAGING_CANDIDATE-style scripts.
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO_ROOT)
    env["STAGING_DIR"] = str(stage)
    print(f"[run] {a.build} -> {a.stage}")
    r = subprocess.run([sys.executable, str(build)], cwd=REPO_ROOT, env=env, capture_output=True, text=True)
    print(r.stdout[-1500:])
    if r.returncode != 0:
        print("STDERR:", r.stderr[-800:])
        return r.returncode

    # Move any db/gexf/json that the script freshly wrote into scripts/build.
    slug_base = Path(a.build).name.replace("build_", "").replace("_data.py", "")
    candidates = [
        REPO_ROOT / "scripts" / "build" / f"{slug_base}_network.db",
        REPO_ROOT / "scripts" / "build" / f"{slug_base}_network.gexf",
    ]
    moved = 0
    for c in candidates:
        if c.exists():
            shutil.move(str(c), str(stage / c.name)); moved += 1
    # Scripts that self-generate person JSON often write them to their _CURRENT_DIR
    # (scripts/build). Move any *.json created in the last 5 minutes there.
    import time
    cutoff = time.time() - 300
    for f in list((REPO_ROOT / "scripts" / "build").glob("*.json")) + list((REPO_ROOT / "scripts" / "build").glob("*.md")):
        try:
            if f.stat().st_mtime >= cutoff:
                shutil.move(str(f), str(stage / f.name)); moved += 1
        except OSError:
            pass
    print(f"[move] consolidated {moved} artifacts into staging.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())