#!/usr/bin/env python3
"""Hardlink audited legacy artifacts into province-partitioned directories."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.paths import (
    DATABASE_DIR,
    GRAPH_DIR,
    PERSONS_DIR,
    PROVINCE_SLUGS,
    province_database_dir,
    province_graph_dir,
    province_persons_dir,
)
from gov_relation.todo import load_todo


def load_holdouts(path: Path | None) -> set[str]:
    """Return relative paths excluded from migration (unresolvable artifacts)."""
    if path is None or not path.exists():
        return set()
    data = json.loads(path.read_text(encoding="utf-8"))
    artifacts = data.get("artifacts", []) if isinstance(data, dict) else data
    return {str(item.get("path", "")) for item in artifacts if item.get("path")}


def build_province_map() -> dict[str, set[str]]:
    """Return every candidate province for each region label."""
    mapping: dict[str, set[str]] = {}
    for province in load_todo()["provinces"]:
        slug = PROVINCE_SLUGS.get(province["province"], province["province"])
        for task in province.get("tasks", []):
            for item in (task, *task.get("sub_tasks", [])):
                region = str(item.get("region", ""))
                if region:
                    mapping.setdefault(region, set()).add(slug)
    return mapping


def resolve_province(
    relative_path: str,
    stem: str,
    mapping: dict[str, set[str]],
    overrides: dict[str, str],
) -> tuple[str | None, str]:
    """Resolve only exact overrides or unique TODO labels."""
    if relative_path in overrides:
        slug = overrides[relative_path]
        if slug not in PROVINCE_SLUGS.values():
            return None, f"invalid-override:{slug}"
        return slug, "override"
    candidates = mapping.get(stem, set())
    if len(candidates) == 1:
        return next(iter(candidates)), "todo"
    if len(candidates) > 1:
        return None, "ambiguous:" + ",".join(sorted(candidates))
    return None, "unmatched"


def _province_name(slug: str) -> str:
    return next(name for name, value in PROVINCE_SLUGS.items() if value == slug)


def _link(source: Path, destination: Path, *, dry_run: bool) -> str:
    if destination.exists():
        if source.stat().st_dev == destination.stat().st_dev and (
            source.stat().st_ino == destination.stat().st_ino
        ):
            return "existing-hardlink"
        raise FileExistsError(f"refusing to replace: {destination}")
    if not dry_run:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.hardlink_to(source)
    return "planned" if dry_run else "linked"


def migrate(
    mapping: dict[str, set[str]],
    overrides: dict[str, str],
    *,
    dry_run: bool,
    holdout: set[str] | None = None,
) -> dict:
    holdout = holdout or set()
    stats: dict[str, object] = {
        "databases": 0,
        "graphs": 0,
        "persons": 0,
        "holdout": [],
        "unmatched": [],
        "ambiguous": [],
        "actions": [],
    }
    actions: list[dict] = stats["actions"]  # type: ignore[assignment]
    for source_dir, pattern, kind, destination_factory in (
        (DATABASE_DIR, "*.db", "databases", province_database_dir),
        (GRAPH_DIR, "*.gexf", "graphs", province_graph_dir),
    ):
        for source in sorted(source_dir.glob(pattern)):
            relative = str(source.relative_to(REPO_ROOT))
            if relative in holdout:
                held: list[dict] = stats["holdout"]  # type: ignore[assignment]
                held.append({"path": relative, "reason": "holdout"})
                continue
            stem = source.stem.removesuffix("_network")
            slug, reason = resolve_province(relative, stem, mapping, overrides)
            if slug is None:
                bucket = "ambiguous" if reason.startswith("ambiguous:") else "unmatched"
                unresolved: list[dict] = stats[bucket]  # type: ignore[assignment]
                unresolved.append({"path": relative, "reason": reason})
                continue
            destination = destination_factory(_province_name(slug)) / source.name
            actions.append(
                {
                    "source": relative,
                    "destination": str(destination.relative_to(REPO_ROOT)),
                    "status": _link(source, destination, dry_run=dry_run),
                }
            )
            stats[kind] = int(stats[kind]) + 1

    for source in sorted(PERSONS_DIR.glob("*.json")):
        relative = str(source.relative_to(REPO_ROOT))
        if relative in holdout:
            kept: list[dict] = stats["holdout"]  # type: ignore[assignment]
            kept.append({"path": relative, "reason": "holdout"})
            continue
        province: str | None = None
        if relative in overrides:
            slug = overrides[relative]
            if slug in PROVINCE_SLUGS.values():
                province = _province_name(slug)
            else:
                unresolved = stats["unmatched"]  # type: ignore[assignment]
                unresolved.append({"path": relative, "reason": f"invalid-override:{slug}"})
                continue
        if province is None:
            parts = source.stem.split("-")
            remainder = parts[1:] if parts and len(parts[0]) == 8 else parts[3:]
            province = next((item for item in remainder if item in PROVINCE_SLUGS), None)
        if province is None:
            unresolved = stats["unmatched"]  # type: ignore[assignment]
            unresolved.append({"path": relative, "reason": "filename"})
            continue
        destination = province_persons_dir(province) / source.name
        actions.append(
            {
                "source": str(source.relative_to(REPO_ROOT)),
                "destination": str(destination.relative_to(REPO_ROOT)),
                "status": _link(source, destination, dry_run=dry_run),
            }
        )
        stats["persons"] = int(stats["persons"]) + 1
    return stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--mapping-file",
        type=Path,
        default=REPO_ROOT / "data/migrations/province_artifact_map.json",
    )
    parser.add_argument(
        "--holdout-file",
        type=Path,
        default=REPO_ROOT / "data/migrations/unresolved_holdout.json",
    )
    parser.add_argument("--allow-partial", action="store_true")
    args = parser.parse_args()
    overrides = (
        json.loads(args.mapping_file.read_text(encoding="utf-8"))
        if args.mapping_file.exists()
        else {}
    )
    holdout = load_holdouts(args.holdout_file)
    result = migrate(build_province_map(), overrides, dry_run=args.dry_run, holdout=holdout)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    unresolved = result["unmatched"] or result["ambiguous"]
    return 0 if args.dry_run or args.allow_partial or not unresolved else 2


if __name__ == "__main__":
    raise SystemExit(main())
