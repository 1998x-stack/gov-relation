#!/usr/bin/env python3
"""Build and audit the canonical government relationship database."""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.platform.identity import stable_id
from gov_relation.platform.importer import ImportStats, import_legacy_database, import_person_profile
from gov_relation.platform.quality import database_report
from gov_relation.platform.resolution import build_person_candidates
from gov_relation.platform.rights import (
    RightsManifestError,
    apply_manifest,
    load_manifest,
    register_review_key,
    sign_manifest,
    validate_manifest,
    verify_manifest_signature,
)
from gov_relation.platform.schema import connect, create_schema
from gov_relation.paths import CANONICAL_DB

DEFAULT_DATABASE = CANONICAL_DB
DEFAULT_LEGACY_DIR = REPO_ROOT / "data" / "database"
DEFAULT_PROFILE_DIR = REPO_ROOT / "data" / "persons"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _print(value: object) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def _record_file_errors(conn: sqlite3.Connection, errors: list[str]) -> None:
    for error in errors:
        conn.execute(
            """INSERT OR IGNORE INTO quality_issues
               (issue_id, severity, issue_code, message)
               VALUES (?, 'error', 'input_parse_error', ?)""",
            (stable_id("issue", f"input_parse_error|{error}"), error),
        )


def build_database(args: argparse.Namespace) -> int:
    destination = args.database.resolve()
    if destination.exists() and not args.replace:
        raise SystemExit(f"Refusing to overwrite existing database: {destination}; use --replace")
    destination.parent.mkdir(parents=True, exist_ok=True)
    building = destination.with_name(destination.name + ".building")
    if building.exists():
        building.unlink()

    conn = connect(building)
    create_schema(conn)
    run_id = stable_id("run", f"build|{_now()}|{destination}")
    started = _now()
    conn.execute(
        "INSERT INTO ingest_runs(run_id, started_at, mode, status) VALUES (?, ?, 'build', 'running')",
        (run_id, started),
    )
    conn.commit()

    total = ImportStats()
    legacy_files = sorted(args.legacy_dir.resolve().glob("*.db"))
    profile_files = sorted(args.profiles_dir.resolve().glob("*.json"))
    if args.limit:
        legacy_files = legacy_files[: args.limit]
        profile_files = profile_files[: args.limit]
    input_count = len(legacy_files) + len(profile_files)

    try:
        for index, path in enumerate(legacy_files, start=1):
            try:
                with conn:
                    total.add(
                        import_legacy_database(conn, path, source_root=REPO_ROOT)
                    )
            except Exception as exc:
                total.errors.append(f"{path.relative_to(REPO_ROOT)}: {exc}")
            if args.progress and (index % args.progress == 0 or index == len(legacy_files)):
                print(f"legacy {index}/{len(legacy_files)}", file=sys.stderr)

        for index, path in enumerate(profile_files, start=1):
            try:
                with conn:
                    total.add(import_person_profile(conn, path, source_root=REPO_ROOT))
            except Exception as exc:
                total.errors.append(f"{path.relative_to(REPO_ROOT)}: {exc}")
            if args.progress and (index % args.progress == 0 or index == len(profile_files)):
                print(f"profiles {index}/{len(profile_files)}", file=sys.stderr)

        _record_file_errors(conn, total.errors)
        candidate_count = build_person_candidates(conn)
        status = "partial" if total.errors else "succeeded"
        conn.execute(
            """UPDATE ingest_runs SET finished_at=?, status=?, input_count=?,
               imported_count=?, rejected_count=?, error=? WHERE run_id=?""",
            (
                _now(), status, input_count, total.datasets,
                len(total.errors), "\n".join(total.errors[:100]), run_id,
            ),
        )
        conn.commit()
        report = database_report(conn)
        report["import"] = total.as_dict()
        report["resolution_candidates_created"] = candidate_count
        conn.close()
        if destination.exists():
            destination.unlink()
        os.replace(building, destination)
        _print({"database": str(destination), **report})
        return 0 if not total.errors else 2
    except BaseException:
        conn.execute(
            "UPDATE ingest_runs SET finished_at=?, status='failed' WHERE run_id=?",
            (_now(), run_id),
        )
        conn.commit()
        conn.close()
        raise


def init_database(args: argparse.Namespace) -> int:
    conn = connect(args.database)
    create_schema(conn)
    conn.close()
    _print({"database": str(args.database.resolve()), "status": "initialized"})
    return 0


def audit_database(args: argparse.Namespace) -> int:
    conn = connect(args.database, read_only=True)
    report = database_report(conn)
    conn.close()
    _print({"database": str(args.database.resolve()), **report})
    return 0 if not report["foreign_key_errors"] else 2


def resolve_database(args: argparse.Namespace) -> int:
    conn = connect(args.database)
    create_schema(conn)
    with conn:
        created = build_person_candidates(
            conn,
            minimum_score=args.minimum_score,
            maximum_name_group=args.maximum_name_group,
        )
    total = conn.execute("SELECT COUNT(*) FROM resolution_candidates").fetchone()[0]
    conn.close()
    _print({"database": str(args.database.resolve()), "created": created, "total": total})
    return 0


def release_check(args: argparse.Namespace) -> int:
    conn = connect(args.database, read_only=True)
    report = database_report(conn)
    conn.close()
    _print(
        {
            "database": str(args.database.resolve()),
            "commercial_release_ready": report["commercial_release_ready"],
            "open_quality_issues": report["open_quality_issues"],
            "rights": report["rights"],
        }
    )
    return 0 if report["commercial_release_ready"] else 3


def rights_validate(args: argparse.Namespace) -> int:
    manifest = load_manifest(args.manifest)
    validate_manifest(manifest, require_signature=True)
    _print({"manifest_id": manifest["manifest_id"], "status": "valid"})
    return 0


def rights_sign(args: argparse.Namespace) -> int:
    if args.output.exists() and not args.force:
        raise RightsManifestError(f"Refusing to overwrite {args.output}; use --force")
    signed = sign_manifest(load_manifest(args.manifest), args.private_key)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(signed, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _print({"manifest_id": signed["manifest_id"], "output": str(args.output), "status": "signed"})
    return 0


def rights_verify(args: argparse.Namespace) -> int:
    manifest = load_manifest(args.manifest)
    verify_manifest_signature(manifest, args.public_key)
    _print({"manifest_id": manifest["manifest_id"], "status": "signature_verified"})
    return 0


def rights_apply(args: argparse.Namespace) -> int:
    conn = connect(args.database)
    try:
        create_schema(conn)
        result = apply_manifest(conn, load_manifest(args.manifest), args.public_key)
        conn.commit()
    finally:
        conn.close()
    _print({"database": str(args.database.resolve()), **result})
    return 0


def rights_key_register(args: argparse.Namespace) -> int:
    conn = connect(args.database)
    try:
        create_schema(conn)
        with conn:
            result = register_review_key(
                conn,
                args.public_key,
                reviewer_identity=args.reviewer,
                review_authority=args.authority,
                valid_from=args.valid_from,
                valid_to=args.valid_to,
            )
    finally:
        conn.close()
    _print({"database": str(args.database.resolve()), **result})
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    subparsers = root.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="initialize an empty canonical database")
    init.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    init.set_defaults(handler=init_database)

    build = subparsers.add_parser("build", help="build canonical DB from all legacy inputs")
    build.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    build.add_argument("--legacy-dir", type=Path, default=DEFAULT_LEGACY_DIR)
    build.add_argument("--profiles-dir", type=Path, default=DEFAULT_PROFILE_DIR)
    build.add_argument("--limit", type=int, default=0, help="limit each input family for testing")
    build.add_argument("--progress", type=int, default=250, help="progress interval; 0 disables")
    build.add_argument("--replace", action="store_true", help="replace the exact destination atomically")
    build.set_defaults(handler=build_database)

    audit = subparsers.add_parser("audit", help="report integrity, quality, evidence, and rights")
    audit.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    audit.set_defaults(handler=audit_database)

    resolve = subparsers.add_parser("resolve", help="create conservative person merge candidates")
    resolve.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    resolve.add_argument("--minimum-score", type=float, default=0.65)
    resolve.add_argument("--maximum-name-group", type=int, default=40)
    resolve.set_defaults(handler=resolve_database)

    release = subparsers.add_parser(
        "release-check", help="fail unless commercial evidence and quality gates pass"
    )
    release.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    release.set_defaults(handler=release_check)

    validate = subparsers.add_parser(
        "rights-validate", help="validate a signed source-rights manifest"
    )
    validate.add_argument("--manifest", type=Path, required=True)
    validate.set_defaults(handler=rights_validate)

    sign = subparsers.add_parser("rights-sign", help="sign a source-rights manifest")
    sign.add_argument("--manifest", type=Path, required=True)
    sign.add_argument("--private-key", type=Path, required=True)
    sign.add_argument("--output", type=Path, required=True)
    sign.add_argument("--force", action="store_true")
    sign.set_defaults(handler=rights_sign)

    verify = subparsers.add_parser("rights-verify", help="verify a manifest signature")
    verify.add_argument("--manifest", type=Path, required=True)
    verify.add_argument("--public-key", type=Path, required=True)
    verify.set_defaults(handler=rights_verify)

    key_register = subparsers.add_parser(
        "rights-key-register", help="trust a rights reviewer's public signing key"
    )
    key_register.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    key_register.add_argument("--public-key", type=Path, required=True)
    key_register.add_argument("--reviewer", required=True)
    key_register.add_argument("--authority", required=True)
    key_register.add_argument("--valid-from", required=True, help="RFC3339 timestamp")
    key_register.add_argument("--valid-to", help="optional RFC3339 timestamp")
    key_register.set_defaults(handler=rights_key_register)

    apply = subparsers.add_parser(
        "rights-apply", help="verify and transactionally apply source-rights decisions"
    )
    apply.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    apply.add_argument("--manifest", type=Path, required=True)
    apply.add_argument("--public-key", type=Path, required=True)
    apply.set_defaults(handler=rights_apply)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        return args.handler(args)
    except RightsManifestError as exc:
        print(f"rights error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
