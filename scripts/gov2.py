#!/usr/bin/env python3
"""gov2 — canonical JSONL + SQLite backup engine (destructive refactor).

The canonical data lives as JSONL streams under ``data/records/``. The SQLite
database is a *derived backup* rebuilt from those streams; ``verify`` proves the
two are identical.

Commands
--------
  export   <src.db> [records]   Export a SQLite DB into canonical JSONL streams
  backup   [records] [dst.db]   Rebuild the SQLite backup from JSONL (--overwrite)
  verify   [records] [db]       Assert JSONL and SQLite are byte-for-byte equal
  build    ...                  Pillar A: data generation (writes JSONL)
  viz      ...                  Pillar B: visualization (JSONL -> graph/dashboard)
  classify ...                  Pillar C: classification / induction (JSONL -> taxonomy)

Default paths: records=data/records, db=data/database/platform.db
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.canon import (
    export_db_to_records,
    rebuild_db_from_records,
    verify_consistency,
)

RECORDS_DEFAULT = REPO_ROOT / "data" / "records"
DB_DEFAULT = REPO_ROOT / "data" / "database" / "platform.db"


def _print_obj(obj):
    import json
    print(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True))


def main() -> int:
    ap = argparse.ArgumentParser(prog="gov2", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("export")
    p.add_argument("src_db", nargs="?")
    p.add_argument("records", nargs="?", default=str(RECORDS_DEFAULT))

    p = sub.add_parser("backup")
    p.add_argument("records", nargs="?", default=str(RECORDS_DEFAULT))
    p.add_argument("dst", nargs="?", default=str(DB_DEFAULT))
    p.add_argument("--overwrite", action="store_true")

    p = sub.add_parser("verify")
    p.add_argument("records", nargs="?", default=str(RECORDS_DEFAULT))
    p.add_argument("db", nargs="?", default=str(DB_DEFAULT))

    p = sub.add_parser("build")
    p.add_argument("--records", default=str(RECORDS_DEFAULT))
    p.add_argument("--profiles", action="append")
    for name in ("viz", "classify", "profiles"):
        p = sub.add_parser(name)
        p.add_argument("--records", default=str(RECORDS_DEFAULT))
    p = sub.add_parser("region")
    p.add_argument("--spec", required=True, help="region spec JSON (persons/orgs/positions/relationships)")
    p.add_argument("--slug", required=True)
    p.add_argument("--province", required=True)
    p.add_argument("--records", default=str(RECORDS_DEFAULT))
    sub.add_parser("snapshot").add_argument("--records", default=str(RECORDS_DEFAULT))

    args = ap.parse_args()

    if args.cmd == "export":
        src = args.src_db or (REPO_ROOT / "data" / "platform" / "gov_relation.db")
        m = export_db_to_records(
            src, args.records, source_label=str(src)
        )
        _print_obj(m)
        return 0
    if args.cmd == "backup":
        n = rebuild_db_from_records(
            args.records, args.dst, overwrite=args.overwrite
        )
        print(f"rebuilt {args.dst} from {n} streams over {args.records}")
        return 0
    if args.cmd == "verify":
        r = verify_consistency(args.records, args.db)
        _print_obj(r)
        return 0 if r.get("consistent") else 1
    if args.cmd == "build":
        from gov_relation.canon.pillar_build import pillar_build
        return pillar_build(args)
    if args.cmd == "viz":
        from gov_relation.canon.pillar_viz import pillar_viz
        return pillar_viz(args)
    if args.cmd == "classify":
        from gov_relation.canon.pillar_classify import pillar_classify
        return pillar_classify(args)
    if args.cmd == "profiles":
        from gov_relation.canon.pillar_profiles import pillar_import_profiles
        return pillar_import_profiles(args)
    if args.cmd == "region":
        from gov_relation.canon.pillar_region import pillar_build_region
        return pillar_build_region(args)
    if args.cmd == "snapshot":
        from gov_relation.canon.pillar_region import snapshot_regions
        import json as _json
        from gov_relation.canon import write_manifest
        print("aggregated:", _json.dumps(snapshot_regions(args.records), ensure_ascii=False))
        write_manifest(Path(args.records), source="<regions-agg>", tables=[])
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())