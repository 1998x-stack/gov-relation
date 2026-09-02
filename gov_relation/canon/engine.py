"""Canonical engine: export SQLite -> JSONL, rebuild SQLite from JSONL, verify."""

from __future__ import annotations

import json
import os
import re
import sqlite3
import uuid
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import streams

SCHEMA_FILE = "schema.sql"
VIEWS_FILE = "views.sql"
MANIFEST_FILE = "manifest.json"
SCHEMA_VERSION_STR = "2.0.0"

# Engine metadata / non-content: kept out of canonical streams, re-stamped by
# the backup builder (never carries provenance data).
NON_CONTENT_TABLES = {"schema_meta"}


def content_tables_from_db(conn: sqlite3.Connection) -> list[str]:
    return [t for t in streams.all_content_tables(conn) if t not in NON_CONTENT_TABLES]


def content_tables_from_dir(records_dir: Path) -> list[str]:
    return sorted(
        p.stem
        for p in records_dir.glob("*.jsonl")
        if p.name not in {SCHEMA_FILE, VIEWS_FILE, MANIFEST_FILE}
        and p.stem not in NON_CONTENT_TABLES
    )


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def content_tables_from_dir(records_dir: Path) -> list[str]:
    return sorted(
        p.stem
        for p in records_dir.glob("*.jsonl")
        if p.name not in {SCHEMA_FILE, VIEWS_FILE, MANIFEST_FILE}
    )


def export_db_to_records(
    db_path: str | Path,
    records_dir: str | Path,
    *,
    source_label: str | None = None,
) -> dict[str, Any]:
    """Export every content table of ``db_path`` into ``records_dir/*.jsonl``.

    Views are exported to ``views.sql`` only (rebuilt on demand). The JSONL
    streams are the canonical output; this function never mutates the source.
    """
    db_path = Path(db_path)
    records_dir = Path(records_dir)
    records_dir.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    tables: list[str] = []
    try:
        tables = content_tables_from_db(conn)
        views = streams.all_views(conn)

        ddl_lines = []
        for table in tables:
            n = streams.write_jsonl(
                records_dir / f"{table}.jsonl",
                streams.iter_table_rows(conn, table),
            )
            ddl_lines.append(streams.table_ddl(conn, table))
        (records_dir / SCHEMA_FILE).write_text(
            "\n;\n".join(ddl_lines) + "\n;\n", encoding="utf-8"
        )

        if views:
            view_ddl = [
                v[0]
                for v in conn.execute(
                    "SELECT sql FROM sqlite_master WHERE type='view' ORDER BY name"
                )
                if v[0]
            ]
            (records_dir / VIEWS_FILE).write_text(
                "\n;\n".join(view_ddl) + "\n;\n", encoding="utf-8"
            )
        elif (records_dir / VIEWS_FILE).exists():
            (records_dir / VIEWS_FILE).unlink()
    finally:
        conn.close()

    manifest = write_manifest(records_dir, source=str(db_path), tables=tables)
    return manifest


def rebuild_db_from_records(
    records_dir: str | Path,
    db_path: str | Path,
    *,
    overwrite: bool = False,
) -> int:
    """Rebuild a SQLite backup entirely from the JSONL streams.

    Disposable: the caller may delete ``db_path`` and re-run this at any time
    (outputs identical to the canonical JSONL).
    """
    records_dir = Path(records_dir)
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    tables = content_tables = content_tables_from_dir(records_dir)
    if db_path.exists():
        if not overwrite:
            raise FileExistsError(
                f"backup exists ({db_path}); pass overwrite=True"
            )
        db_path.unlink()

    sql = records_dir / SCHEMA_FILE
    if not sql.exists():
        # No canonical DDL yet (standalone generation); nothing to rebuild into.
        return 0

    # The backup is a mirror of the JSONL. Every JSONL row may carry NULL, so
    # drop NOT NULL constraints (keep PK/types/indexes); a JSONL row without a
    # value must store NULL, never fail the load.
    raw_ddl = sql.read_text(encoding="utf-8")
    ddl = re.sub(r"\s+NOT\s+NULL", "", raw_ddl)

    # Build into a temporary file, then atomically swap in only on success so a
    # failed rebuild never leaves a half-rebuilt backup behind.
    tmp_db = db_path.with_name(f".{db_path.name}.{uuid.uuid4().hex[:8]}.building")
    conn = sqlite3.connect(str(tmp_db))
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.executescript(ddl)

        for table in tables:
            cols: list[str] | None = None
            values: list[tuple] = []
            for row in streams.iter_jsonl(records_dir / f"{table}.jsonl"):
                if cols is None:
                    cols = sorted(row.keys())
                values.append(tuple(row.get(c) for c in cols))
            if not cols:
                continue
            colsql = ", ".join(cols)
            ph = ", ".join("?" * len(cols))
            conn.executemany(
                f'INSERT INTO "{table}" ({colsql}) VALUES ({ph})', values
            )
            conn.commit()

        if (records_dir / VIEWS_FILE).exists():
            conn.executescript((records_dir / VIEWS_FILE).read_text(encoding="utf-8"))
        _stamp_schema_meta(conn)

        conn.commit()
        # Make the temp file self-contained (no -wal/-shm required on open).
        conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        conn.execute("PRAGMA journal_mode=DELETE")
    except BaseException:
        try:
            conn.close()
        finally:
            pass
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
    meta = _table_exists(conn, "schema_meta")
    if meta:
        try:
            conn.execute(
                "INSERT OR REPLACE INTO schema_meta (key, value) VALUES ('schema_version', ?)",
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
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)
        ).fetchone()
        is not None
    )


def verify_consistency(
    records_dir: str | Path,
    db_path: str | Path,
) -> dict[str, Any]:
    """Re-export the backup and compare with the canonical JSONL.

    Returns per-table {count, sha256, ok} plus a top-level ``consistent`` flag.
    """
    records_dir = Path(records_dir)
    db_path = Path(db_path)
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    tables = content_tables_from_dir(records_dir)
    results: dict[str, Any] = {}
    try:
        actual = streams.all_content_tables(conn)
        missing = [t for t in tables if t not in actual]
        extra = [t for t in actual if t not in tables]
        for table in tables:
            jsonl_path = records_dir / f"{table}.jsonl"
            canon_count = sum(1 for _ in streams.iter_jsonl(jsonl_path))
            canon_sha = streams.jsonl_sha256(jsonl_path)
            # re-export db rows to a temp jsonl in same canonical ordering
            fd, tmp = tempfile.mkstemp(suffix=".jsonl")
            import os
            os.close(fd)
            tmp_path = Path(tmp)
            db_count = streams.write_jsonl(
                tmp_path, streams.iter_table_rows(conn, table)
            )
            db_sha = streams.jsonl_sha256(tmp_path)
            tmp_path.unlink()
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
        if path.name in {SCHEMA_FILE, VIEWS_FILE, MANIFEST_FILE}:
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