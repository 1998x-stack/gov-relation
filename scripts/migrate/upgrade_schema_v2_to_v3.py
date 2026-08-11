#!/usr/bin/env python3
"""Explicitly upgrade a canonical v2 SQLite database to schema v3."""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.factory import SchemaFactory
from gov_relation.platform.schema import connect

ALTER_COLUMNS: dict[str, tuple[str, ...]] = {
    "persons": (
        "education TEXT NOT NULL DEFAULT ''",
        "merged_into_id TEXT REFERENCES persons(person_id)",
    ),
    "positions": (
        "title_category TEXT NOT NULL DEFAULT ''",
        "sort_order INTEGER NOT NULL DEFAULT 0",
    ),
    "datasets": (
        "commercial_use INTEGER NOT NULL DEFAULT 0 CHECK(commercial_use IN (0, 1))",
    ),
    "sources": (
        "commercial_use INTEGER NOT NULL DEFAULT 0 CHECK(commercial_use IN (0, 1))",
    ),
}
REQUIRED_V3_COLUMNS = {
    table: {definition.split(None, 1)[0] for definition in definitions}
    for table, definitions in ALTER_COLUMNS.items()
}
BACKFILLS = (
    (
        "positions", "category", "title_category",
        "UPDATE positions SET title_category=category "
        "WHERE title_category='' AND category!=''",
    ),
    (
        "datasets", "commercial_use_allowed", "commercial_use",
        "UPDATE datasets SET commercial_use=commercial_use_allowed "
        "WHERE commercial_use=0 AND commercial_use_allowed!=0",
    ),
    (
        "sources", "commercial_use_allowed", "commercial_use",
        "UPDATE sources SET commercial_use=commercial_use_allowed "
        "WHERE commercial_use=0 AND commercial_use_allowed!=0",
    ),
)


def _tables(conn: sqlite3.Connection) -> set[str]:
    return {
        row[0]
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
    }


def _columns(conn: sqlite3.Connection, table: str) -> set[str]:
    return {row[1] for row in conn.execute(f"PRAGMA table_info('{table}')")}


def has_v3_shape(conn: sqlite3.Connection) -> bool:
    tables = _tables(conn)
    return all(
        table in tables and required <= _columns(conn, table)
        for table, required in REQUIRED_V3_COLUMNS.items()
    )


def upgrade(database: Path, *, dry_run: bool = False) -> dict:
    """Upgrade one database transactionally; dry-run performs no writes."""
    conn = connect(database, read_only=True)
    result: dict[str, object] = {
        "altered": [], "created": [], "backfilled": []
    }
    try:
        tables = _tables(conn)
        if "schema_meta" not in tables:
            raise RuntimeError("schema_meta is missing; database is not canonical")
        row = conn.execute(
            "SELECT value FROM schema_meta WHERE key='schema_version'"
        ).fetchone()
        current = row[0] if row else None
        if current == "3.0.0" and has_v3_shape(conn):
            return {"status": "skipped", "reason": "already v3.0.0"}

        if not dry_run:
            backup = database.with_suffix(f"{database.suffix}.pre-v3.bak")
            if not backup.exists():
                backup_conn = sqlite3.connect(backup)
                try:
                    conn.backup(backup_conn)
                finally:
                    backup_conn.close()
            result["backup"] = str(backup)
            writable_conn = connect(database)
            conn.close()
            conn = writable_conn

        altered: list[str] = result["altered"]  # type: ignore[assignment]
        for table, definitions in ALTER_COLUMNS.items():
            if table not in tables:
                continue
            existing = _columns(conn, table)
            for definition in definitions:
                column = definition.split(None, 1)[0]
                if column in existing:
                    continue
                altered.append(f"{table}.{column}")
                if not dry_run:
                    conn.execute(f"ALTER TABLE {table} ADD COLUMN {definition}")

        backfilled: list[str] = result["backfilled"]  # type: ignore[assignment]
        for table, old_column, new_column, sql in BACKFILLS:
            columns = _columns(conn, table) if table in tables else set()
            destination_will_exist = (
                new_column in columns
                or new_column in REQUIRED_V3_COLUMNS.get(table, set())
            )
            if old_column not in columns or not destination_will_exist:
                continue
            backfilled.append(f"{table}.{new_column}<-{old_column}")
            if not dry_run:
                conn.execute(sql)

        if dry_run:
            conn.rollback()
            return {
                "status": "dry-run", "from_version": current,
                "to_version": "3.0.0", **result,
            }

        before = _tables(conn)
        factory = SchemaFactory()
        factory.create_entity_tables(conn)
        factory.create_evidence_tables(conn)
        factory.create_rights_tables(conn)
        factory.create_meta_tables(conn)
        factory.create_views(conn)
        factory.create_indexes(conn)
        created: list[str] = result["created"]  # type: ignore[assignment]
        created.extend(sorted(_tables(conn) - before))
        if not has_v3_shape(conn):
            raise RuntimeError("migration did not produce the required v3 columns")
        conn.execute(
            "INSERT OR REPLACE INTO schema_meta(key, value) VALUES(?, ?)",
            ("schema_version", "3.0.0"),
        )
        conn.commit()
        return {
            "status": "upgraded", "from_version": current,
            "to_version": "3.0.0", **result,
        }
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--database", type=Path,
        default=REPO_ROOT / "data" / "platform" / "gov_relation.db",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    print(json.dumps(upgrade(args.database, dry_run=args.dry_run), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
