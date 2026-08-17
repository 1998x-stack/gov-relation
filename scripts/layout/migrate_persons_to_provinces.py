#!/usr/bin/env python3
"""Migrate flat legacy persons into the canonical province-partitioned store.

Design (locked with maintainers):
- Source (git-tracked legacy help): ``data/persons/<file>.json``
- Destination (canonical, code-read): ``data/provinces/<slug>/persons/<file>.json``
  (this is ``gov_relation.paths.province_persons_dir()``; also where build-time
  ``process_tmp.py`` and ``dispatch.py`` direct new profiles)
- Timestamps unified to 8-digit ``YYYYMMDD`` everywhere (matches dispatch).
- Dedup: if the normalized target already exists in the canonical store with
  identical bytes, the legacy duplicate is dropped (not copied).

The script is strictly data-driven and reversible: it first emits a mapping CSV
(old->target), lets a human review it, then applies it.

Usage:
    # 1) build a reviewable mapping
    python3 scripts/layout/migrate_persons_to_provinces.py --mapping out/persons_map.csv
    # 2) apply it
    python3 scripts/layout/migrate_persons_to_provinces.py --mapping out/persons_map.csv --apply
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import shutil
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from gov_relation.paths import PROVINCES_DIR  # noqa: E402
from scripts.layout import plan_mapping as pm  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
LEGACY = ROOT / "data" / "persons"


def _md5(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def existing_canonical() -> dict[tuple[str, str], Path]:
    """Return {(slug, filename): path} for current canonical persons."""
    out: dict[tuple[str, str], Path] = {}
    for pdir in PROVINCES_DIR.glob("*/persons"):
        slug = pdir.parent.name
        for f in pdir.glob("*.json"):
            out[(slug, f.name)] = f
    return out


def build_plan() -> tuple[list[dict], list[dict], list[dict]]:
    """Return (moves, dedups, anomalies)."""
    canon = existing_canonical()
    moves: list[dict] = []
    dedups: list[dict] = []
    anomalies: list[dict] = []
    for f in sorted(LEGACY.glob("*.json")):
        stem = f.stem
        info, reason = pm.parse_person(stem)
        slug = info.get("slug")
        if slug is None:
            anomalies.append(
                {"old": str(f.relative_to(ROOT)), "reason": reason or "unresolved-province"}
            )
            continue
        ymd = info["date"].replace("-", "")  # YYYY-MM-DD -> YYYYMMDD
        new_name = f"{ymd}-{info['rest']}.json"
        target = Path("data") / "provinces" / slug / "persons" / new_name
        key = (slug, new_name)
        if key in canon:
            if _md5(f) == _md5(canon[key]):
                dedups.append(
                    {"old": str(f.relative_to(ROOT)), "target": str(target), "province_slug": slug}
                )
            else:
                anomalies.append(
                    {
                        "old": str(f.relative_to(ROOT)),
                        "reason": f"content-conflict-with-canonical:{target}",
                    }
                )
            continue
        moves.append(
            {"old": str(f.relative_to(ROOT)), "target": str(target), "province_slug": slug}
        )
    return moves, dedups, anomalies


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--mapping", type=Path, default=ROOT / "scripts/layout/out/persons_map.csv")
    p.add_argument("--apply", action="store_true", help="perform the moves (default: plan+report only)")
    p.add_argument(
        "--link",
        action="store_true",
        help="create HARDLINKS into canonical (preserving the tracked source at "
        "data/persons/) instead of moving files. Mutually exclusive with --apply.",
    )
    args = p.parse_args()
    if args.apply and args.link:
        p.error("--apply and --link are mutually exclusive")

    moves, dedups, anomalies = build_plan()
    print(
        f"moves={len(moves)} dedup_drop={len(dedups)} anomalies={len(anomalies)} "
        f"province_count={len(set(m['province_slug'] for m in moves))}"
    )

    # collision check within the move set
    seen: dict[str, str] = {}
    coll: list[dict] = []
    for m in moves:
        if m["target"] in seen:
            coll.append({"old": m["old"], "target": m["target"]})
        seen.setdefault(m["target"], m["old"])
    if coll:
        print(f"INTERNAL-COLLISION count={len(coll)}; refusing to proceed without review")
        for c in coll[:10]:
            print("  ", c)
        return 3

    write_csv(Path(args.mapping), moves, ["old", "target", "province_slug"])
    print(f"plan -> {args.mapping}")

    if anomalies:
        write_csv(Path(args.mapping).with_suffix(".anomalies.csv"), anomalies, ["old", "reason"])

    if not args.apply and not args.link:
        print("dry-run: not moving. Re-run with --apply (move) or --link (hardlink) to execute.")
        return 0

    if args.link:
        # Hardlink mirror: keep tracked source; add canonical hardlink view.
        linked = skipped = existing = 0
        for m in moves:
            src = ROOT / m["old"]
            dst = ROOT / m["target"]
            if not src.exists():
                print(f"  skip(missing) {m['old']}")
                skipped += 1
                continue
            if dst.exists():
                if os.stat(src).st_ino == os.stat(dst).st_ino:
                    existing += 1  # already a hardlink; no-op
                else:
                    print(f"  skip(different-content-target) {m['target']}")
                    skipped += 1
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            try:
                os.link(str(src), str(dst))
                linked += 1
            except FileExistsError:
                existing += 1
        print(f"linked {linked}, already-linked {existing}, skipped={skipped}")
        return 0

    # apply (move) branch
    skipped = 0
    for m in moves:
        src = ROOT / m["old"]
        dst = ROOT / m["target"]
        if not src.exists():
            print(f"  skip(missing) {m['old']}")
            skipped += 1
            continue
        if dst.exists():
            print(f"  skip(target-exists) {m['target']}")
            skipped += 1
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
    print(f"applied {len(moves) - skipped} moves, skipped={skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())