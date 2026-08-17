#!/usr/bin/env python3
"""Generate a conservative, human-reviewable file-migration mapping.

Reads the current layout of `data/persons` (and optionally other domains) and
emits a *mapping table* (old path -> target path) plus an anomalies report.

Design principle: this script does NOT infer new names from rules. It only
performs mechanically safe operations (group into province subdirs via an
explicit province field, normalize the LEADING date format) and keeps every
other semantic field verbatim. Anything uncertain is written to the anomalies
list with a reason instead of being guessed, so a human can review and override
in the mapping CSV.

Usage:
    python3 scripts/layout/plan_mapping.py --domain persons --dry-run
    python3 scripts/layout/plan_mapping.py --domain persons --emit mapping-<ts>.csv
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from scripts.layout import province_map  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
PERSONS_DIR = ROOT / "data" / "persons"
GRAPH_DIR = ROOT / "data" / "graph"

# Leading date forms: YYYYMMDD or YYYY-MM-DD.
DATE_LEAD = re.compile(r"^(\d{4})-?(\d{2})-?(\d{2})-(.*)$", re.S)


def normalize_date_prefix(m: re.Match) -> tuple[str, str]:
    """Convert a leading date to YYYY-MM-DD; return (date, remainder)."""
    y, mo, d, rest = m.group(1), m.group(2), m.group(3), m.group(4)
    # sanity: plausible calendar date, else leave rest untouched
    try:
        dt.datetime(int(y), int(mo), int(d))
    except ValueError:
        return "", m.group(0)  # not a real date -> treat whole stem as remainder
    return f"{y}-{mo}-{d}", rest


def parse_person(stem: str) -> tuple[dict, str | None]:
    """Parse a persons filename stem into fields; returns (info, anomaly).

    info: dict with normalized fields for target path building.
    anomaly: a short human reason string, or None if we are confident.
    """
    m = DATE_LEAD.match(stem)
    if not m:
        return {}, "no-leading-date"
    date, rest = normalize_date_prefix(m)
    if not date:
        return {}, "unparsable-date"
    parts = rest.split("-")
    if len(parts) < 2:
        return {}, "too-few-fields"

    # Province is the first field after the date for the dominant 5-field form
    # (省会市...). For the 7-field form (YYYY-MM-DD-省-市-角色-名) the 2nd
    # field is the province and the 3rd is the city. Prefer a direct province
    # match on the first remaining field; otherwise, if that first field looks
    # like a province-less value, try a fixed offset.
    first = parts[0]
    slug = province_map.resolve_any_province_slug(first)
    if slug is None and len(parts) >= 2:
        # 7-field form: province in second field
        slug = province_map.resolve_any_province_slug(parts[1])
        if slug is None and parts[0].endswith("市"):
            # e.g. "重庆市"
            slug = province_map.resolve_any_province_slug(first)
    if slug is None:
        slug = province_map.PERSON_REGION_OVERRIDE.get(first)
    if slug is None:
        return {"date": date, "rest": rest}, "unresolved-province"

    # Semantic remainder kept verbatim; we do NOT reparse role/name.
    return {"date": date, "slug": slug, "rest": rest}, None


def target_person_filename(date: str, rest: str) -> str:
    """Return target filename, preserving original semantic fields."""
    return f"{date}-{rest}.json"


def build_persons_mapping() -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    anomalies: list[dict] = []
    for f in sorted(PERSONS_DIR.iterdir()):
        if not f.is_file() or f.suffix != ".json":
            continue
        stem = f.stem
        info, reason = parse_person(stem)
        if info.get("slug") is None:
            anomalies.append(
                {"old": f.name, "category": "persons", "reason": reason or "unresolved-province"}
            )
            continue
        new_name = target_person_filename(info["date"], info["rest"])
        target = Path("data") / "persons" / info["slug"] / new_name
        rows.append(
            {
                "domain": "persons",
                "old_path": str(f.relative_to(ROOT)),
                "target_path": str(target),
                "province_slug": info["slug"],
                "status": "override-needed" if reason else "ok",
                "note": reason or "",
            }
        )
    # detect collisions within a target directory
    seen: dict[str, str] = {}
    for r in rows:
        if r["target_path"] in seen:
            r["status"] = "collision"
            seen[r["target_path"]].update({"status": "collision"})
        seen.setdefault(r["target_path"], r)
    return rows, anomalies


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--domain", choices=["persons", "graph"], default="persons")
    p.add_argument("--dry-run", action="store_true", help="report counts without writing mapping CSV")
    p.add_argument("--emit", metavar="CSV", help="write mapping CSV to this path")
    p.add_argument("--anomalies", metavar="CSV", help="write anomaly report to this path")
    args = p.parse_args()

    rows, anomalies = build_persons_mapping() if args.domain == "persons" else build_graph_mapping()

    ok = sum(1 for r in rows if r["status"] == "ok")
    need = sum(1 for r in rows if r["status"] == "override-needed")
    coll = sum(1 for r in rows if r["status"] == "collision")
    print(f"domain={args.domain} mapped={len(rows)} ok={ok} override_needed={need} collision={coll} anomalies={len(anomalies)}")

    if args.emit:
        with open(args.emit, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["domain", "old_path", "target_path", "province_slug", "status", "note"])
            w.writeheader()
            w.writerows(rows)
        print(f"wrote mapping -> {args.emit}")
    if args.anomalies:
        with open(args.anomalies, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["old", "category", "reason"])
            w.writeheader()
            w.writerows(anomalies)
        print(f"wrote anomalies -> {args.anomalies}")
    return 0 if not anomalies else 2


def build_graph_mapping() -> tuple[list[dict], list[dict]]:
    """Generate old->new mapping for data/graph files.

    Only makes the mechanically safe normalization: every graph file must end
    in ``_network.gexf`` (some legacy files omit the suffix). Semantic stems are
    kept verbatim.
    """
    rows: list[dict] = []
    anomalies: list[dict] = []
    for f in sorted(GRAPH_DIR.iterdir()):
        if not f.is_file():
            continue
        name = f.name
        target = None
        if name.endswith("_network.gexf"):
            target = name
        elif name.endswith(".gexf") and not name.endswith("_network.gexf"):
            stem = name[: -len(".gexf")]
            target = f"{stem}_network.gexf"
            anomalies.append({"old": name, "category": "graph", "reason": "missing-_network-suffix"})
        else:
            # non-gexf files in graph dir (e.g. a stray .db) — leave; note it
            anomalies.append({"old": name, "category": "graph", "reason": "non-gexf-file"})
            continue
        rows.append(
            {
                "domain": "graph",
                "old_path": str(f.relative_to(ROOT)),
                "target_path": str(Path("data") / "graph" / target),
                "province_slug": "",
                "status": "ok" if target == name else "override-needed",
                "note": "" if target == name else "add-_network-suffix",
            }
        )
    # collision check
    seen: dict[str, str] = {}
    for r in rows:
        if r["target_path"] in seen:
            r["status"] = "collision"
            seen[r["target_path"]].update({"status": "collision"})
        seen.setdefault(r["target_path"], r)
    return rows, anomalies


if __name__ == "__main__":
    raise SystemExit(main())