#!/usr/bin/env python3
"""Clean up empty or stale data/tmp/ directories from failed investigations.

Usage:
    python3 scripts/cleanup_tmp.py           # dry-run: show what would be removed
    python3 scripts/cleanup_tmp.py --apply   # actually remove
    python3 scripts/cleanup_tmp.py --age 7   # only remove if older than 7 days (default: 1 day)
"""

from __future__ import annotations

import argparse
import shutil
import time
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="actually remove empty dirs")
    parser.add_argument("--age", type=int, default=1, help="minimum age in days (default: 1)")
    args = parser.parse_args()

    tmp_root = Path(__file__).resolve().parents[1] / "data" / "tmp"
    if not tmp_root.exists():
        print("data/tmp/ does not exist")
        return 0

    now = time.time()
    age_seconds = args.age * 86400
    removed = 0
    skipped = 0
    errors = 0

    for entry in sorted(tmp_root.iterdir()):
        if not entry.is_dir():
            continue
        # Only empty dirs
        files = list(entry.rglob("*"))
        # Check if only empty subdirs exist
        real_files = [f for f in files if f.is_file() or f.is_symlink()]
        if real_files:
            skipped += 1
            continue
        # Check age
        try:
            mtime = entry.stat().st_mtime
        except OSError:
            mtime = 0
        if now - mtime < age_seconds:
            skipped += 1
            continue
        # Report
        subdirs = set(f.parent for f in files if f.is_dir()) | {entry}
        total_dirs = len(subdirs)
        if args.apply:
            try:
                shutil.rmtree(entry)
                print(f"REMOVED  {entry.relative_to(tmp_root.parent)} ({total_dirs} empty dirs)")
                removed += 1
            except OSError as e:
                print(f"ERROR    {entry.name}: {e}")
                errors += 1
        else:
            print(f"WOULD_REMOVE  {entry.relative_to(tmp_root.parent)} ({total_dirs} empty dirs)")

    print(f"\nDry-run summary:" if not args.apply else f"\nSummary:")
    print(f"  Removed: {removed}")
    print(f"  Skipped (has files / too recent): {skipped}")
    print(f"  Errors: {errors}")
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())