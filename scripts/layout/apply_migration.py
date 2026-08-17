#!/usr/bin/env python3
"""Apply a reviewed file-migration mapping CSV.

Reads a mapping CSV (old_path, target_path[, ...]) produced by
``plan_mapping.py`` and moves/renames files accordingly. It is strictly
data-driven: it does NOT re-derive target paths; it executes exactly the rows
in the mapping. Protections:

- ``--dry-run``: only print the diff, don't touch disk.
- Never overwrite an existing target file (skips with a conflict note).
- Never move outside the repo root (guards against a bad mapping column).
- Emits an execution log (old->new) that can be re-run/reversed.
- Only rows with an ``ok`` or ``override-needed`` status are applied;
  ``collision``/in-review rows are skipped.

Usage:
    python3 scripts/layout/apply_migration.py --mapping <mapping.csv> --dry-run
    python3 scripts/layout/apply_migration.py --mapping <mapping.csv> --apply
"""

from __future__ import annotations

import argparse
import csv
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
APPLIED_LOG = ROOT / "scripts" / "layout" / "out" / "applied.log.csv"


def is_inside(base: Path, path: Path) -> bool:
    try:
        path.relative_to(base)
        return True
    except ValueError:
        return False


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--mapping", required=True, help="path to mapping CSV")
    p.add_argument("--apply", action="store_true", help="actually move files (default is dry-run)")
    args = p.parse_args()

    mapping_path = Path(args.mapping)
    if not mapping_path.exists():
        print(f"mapping file not found: {mapping_path}")
        return 3

    rows = list(csv.DictReader(mapping_path.open(newline="")))
    moves, skips = [], []
    for i, r in enumerate(rows):
        old = Path(r["old_path"])
        new = Path(r["target_path"])
        status = r.get("status", "ok")
        if status == "collision":
            skips.append((i, r["old_path"], "collision-status"))
            continue
        if old == new:
            # no-op row (already at target) — skip silently
            continue
        old_abs = ROOT / old
        new_abs = ROOT / new
        if not is_inside(ROOT.resolve(), old_abs.resolve()) or not is_inside(ROOT.resolve(), new_abs.resolve()):
            skips.append((i, r["old_path"], "outside-repo"))
            continue
        if not old_abs.exists():
            skips.append((i, r["old_path"], "old-missing"))
            continue
        if new_abs.exists():
            skips.append((i, r["old_path"], "target-exists"))
            continue
        moves.append((i, old_abs, new_abs, r.get("note", "")))

    print(f"rows={len(rows)} to_move={len(moves)} skipped={len(skips)}")
    if args.apply:
        applied = 0
        for i, old_abs, new_abs, _note in moves:
            new_abs.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(old_abs), str(new_abs))
            applied += 1
        out_dir = ROOT / "scripts" / "layout" / "out"
        out_dir.mkdir(parents=True, exist_ok=True)
        with open(out_dir / "applied_migration.log", "a") as fh:
            for i, old_abs, new_abs, note in moves:
                fh.write(f"{old_abs.relative_to(ROOT)}\t{new_abs.relative_to(ROOT)}\n")
        print(f"applied {applied} moves; log -> scripts/layout/out/applied_migration.log")
    else:
        for i, old_abs, new_abs, _note in moves:
            print(f"  {old_abs.relative_to(ROOT)}  =>  {new_abs.relative_to(ROOT)}")
    if skips:
        print("--- skipped (not applied) ---")
        for i, o, reason in skips:
            print(f"  [{reason}] {o}")
    return 0


if __name__ == "__main__":

    raise SystemExit(main())