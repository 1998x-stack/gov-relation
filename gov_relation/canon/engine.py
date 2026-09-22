"""Canonical engine: export SQLite -> JSONL, rebuild SQLite from JSONL, verify."""

from __future__ import annotations

import json
import os
import re
import sqlite3
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import streams

SCHEMA_FILE = "schema.sql"
VIEWS_FILE = "views.sql"
MANIFEST_FILE = "manifest.json"
SCHEMA_VERSION_STR = "2.0.0"

# Engine metadata is regenerated, not part of the canonical data streams.
NON_CONTENT_TABLES = {"schema_meta"}


def content_tables_from_db(conn: sqlite3.Connection) -> list[str]:
    return [t for t in streams.all_content_tables(conn) if t not in NON_CONTENT_TABLES]


def content_tables_from_dir(records_dir: Path) -> list[str]:
    return sorted(
        p.stem
        for p in records_dir.glob("*.jsonl")
        if p.stem not in NON_CONTENT_TABLES
    )


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def export_db_to_records(
    db_path: str | Path,
    records_dir: str | Path,
    *,
    source_label: str | None = None,
) -> dict[str, Any]:
    """Export content tables and views without mutating the source database."""
    db_path = Path(db_path)
    records_dir = Path(records_dir)
    records_dir.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        tables = content_tables_from_db(conn)
        views = streams.all_views(conn)
        ddl_lines = []
        for table in tables:
            streams.write_jsonl(
                records_dir / f"{table}.jsonl",
                streams.iter_table_rows(conn, table),
            )
            ddl_lines.append(streams.table_ddl(conn, table))
        (records_dir / SCHEMA_FILE).write_text(
            "\n;\n".join(ddl_lines) + "\n;\n", encoding="utf-8"
        )
        if views:
            view_ddl = [
                row[0]
                for row in conn.execute(
                    "SELECT sql FROM sqlite_master WHERE type='view' ORDER BY name"
                )
                if row[0]
            ]
            (records_dir / VIEWS_FILE).write_text(
                "\n;\n".join(view_ddl) + "\n;\n", encoding="utf-8"
            )
        elif (records_dir / VIEWS_FILE).exists():
            (records_dir / VIEWS_FILE).unlink()
    finally:
        conn.close()

    return write_manifest(
        records_dir, source=source_label or str(db_path), tables=tables
    )


def rebuild_db_from_records(
    records_dir: str | Path,
    db_path: str | Path,
    *,
    overwrite: bool = False,
) -> int:
    """Atomically rebuild a disposable SQLite backup from canonical streams."""
    records_dir = Path(records_dir)
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    tables = content_tables_from_dir(records_dir)
    if db_path.exists() and not overwrite:
        raise FileExistsError(f"backup exists ({db_path}); pass overwrite=True")

    sql = records_dir / SCHEMA_FILE
    if not sql.exists():
        return 0

    raw_ddl = sql.read_text(encoding="utf-8")
    # Preserve the existing mirror contract: missing JSONL values become NULL.
    ddl = re.sub(r"\s+NOT\s+NULL", "", raw_ddl)
    tmp_db = db_path.with_name(f".{db_path.name}.{uuid.uuid4().hex[:8]}.building")
    conn = sqlite3.connect(str(tmp_db))
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.executescript(ddl)

        for table in tables:
            cols: list[str] | None = None
            values: list[tuple[Any, ...]] = []
            for row in streams.iter_jsonl(records_dir / f"{table}.jsonl"):
                if not isinstance(row, dict):
                    raise ValueError(f"Expected JSON object in {table}.jsonl")
                if cols is None:
                    cols = sorted(row.keys())
                unexpected = set(row).difference(cols)
                if unexpected:
                    raise ValueError(
                        f"Unexpected columns in {table}.jsonl: {sorted(unexpected)!r}"
                    )
                values.append(tuple(row.get(c) for c in cols))
            if not cols:
                continue
            colsql = ", ".join(streams.quote_identifier(c) for c in cols)
            ph = ", ".join("?" for _ in cols)
            conn.executemany(
                f"INSERT INTO {streams.quote_identifier(table)} ({colsql}) "
                f"VALUES ({ph})",
                values,
            )
            conn.commit()

        if (records_dir / VIEWS_FILE).exists():
            conn.executescript((records_dir / VIEWS_FILE).read_text(encoding="utf-8"))
        _stamp_schema_meta(conn)
        conn.commit()
        conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        conn.execute("PRAGMA journal_mode=DELETE")
    except BaseException:
        conn.close()
        tmp_db.unlink(missing_ok=True)
        _remove_sidecars(tmp_db)
        raise
    finally:
        conn.close()

    _remove_sidecars(db_path)
    os.replace(tmp_db, db_path)
    _remove_sidecars(db_path)
    return len(tables)


def _stamp_schema_meta(conn: sqlite3.Connection) -> None:
    if _table_exists(conn, "schema_meta"):
        try:
            conn.execute(
                "INSERT OR REPLACE INTO schema_meta (key, value) "
                "VALUES ('schema_version', ?)",
                (SCHEMA_VERSION_STR,),
            )
        except sqlite3.OperationalError:
            pass


def _remove_sidecars(path: Path) -> None:
    for suffix in ("-wal", "-shm"):
        Path(f"{path}{suffix}").unlink(missing_ok=True)


def _table_exists(conn: sqlite3.Connection, table: str) -> bool:
    return (
        conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
            (table,),
        ).fetchone()
        is not None
    )


def verify_consistency(
    records_dir: str | Path,
    db_path: str | Path,
) -> dict[str, Any]:
    """Compare a SQLite backup with the canonical streams and report mismatches."""
    records_dir = Path(records_dir)
    db_path = Path(db_path)
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    tables = content_tables_from_dir(records_dir)
    results: dict[str, Any] = {}
    try:
        actual = content_tables_from_db(conn)
        missing = [t for t in tables if t not in actual]
        extra = [t for t in actual if t not in tables]
        for table in tables:
            jsonl_path = records_dir / f"{table}.jsonl"
            canon_count = sum(1 for _ in streams.iter_jsonl(jsonl_path))
            canon_sha = streams.jsonl_sha256(jsonl_path)
            if table in missing:
                results[table] = {
                    "canon_count": canon_count,
                    "db_count": None,
                    "canon_sha256": canon_sha,
                    "db_sha256": None,
                    "ok": False,
                }
                continue
            # write_jsonl creates its own temporary file; the directory is
            # temporary too, and is cleaned even if iteration or hashing fails.
            with tempfile.TemporaryDirectory() as tmp_dir:
                tmp_path = Path(tmp_dir) / "actual.jsonl"
                db_count = streams.write_jsonl(
                    tmp_path, streams.iter_table_rows(conn, table)
                )
                db_sha = streams.jsonl_sha256(tmp_path)
            results[table] = {
                "canon_count": canon_count,
                "db_count": db_count,
                "canon_sha256": canon_sha,
                "db_sha256": db_sha,
                "ok": canon_count == db_count and canon_sha == db_sha,
            }
        results["_missing_tables"] = missing
        results["_extra_tables"] = extra
    finally:
        conn.close()
    results["consistent"] = (
        not missing
        and not extra
        and all(r["ok"] for k, r in results.items() if not k.startswith("_"))
    )
    return results


def write_manifest(
    records_dir: str | Path,
    *,
    source: str | None = None,
    tables: list[str] | None = None,
) -> dict[str, Any]:
    """Write a catalogue of every canonical JSONL stream (count + sha256)."""
    from . import SCHEMA_VERSION

    records_dir = Path(records_dir)
    rec_streams: dict[str, Any] = {}
    for path in sorted(records_dir.glob("*.jsonl")):
        if path.stem in NON_CONTENT_TABLES:
            continue
        count = sum(1 for _ in streams.iter_jsonl(path))
        rec_streams[path.stem] = {
            "count": count,
            "sha256": streams.jsonl_sha256(path),
        }
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": _now(),
        "source": source,
        "record_streams": rec_streams,
    }
    (records_dir / MANIFEST_FILE).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return manifest
