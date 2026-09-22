"""JSONL stream and SQLite metadata helpers."""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import tempfile
from pathlib import Path
from typing import Any, Iterator


def quote_identifier(name: str) -> str:
    """Quote a SQLite table/column name, including embedded double quotes."""
    if not isinstance(name, str) or not name or "\x00" in name:
        raise ValueError("SQLite identifier must be a nonempty string without NUL")
    return '"' + name.replace('"', '""') + '"'


def table_columns(conn: sqlite3.Connection, table: str) -> list[str]:
    return [
        row[1]
        for row in conn.execute(f"PRAGMA table_info({quote_identifier(table)})")
    ]


def table_ddl(conn: sqlite3.Connection, table: str) -> str:
    row = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name=?",
        (table,),
    ).fetchone()
    if row is None:
        raise ValueError(f"SQLite table not found: {table!r}")
    return row[0]


def all_content_tables(conn: sqlite3.Connection) -> list[str]:
    return [
        row[0]
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )
    ]


def all_views(conn: sqlite3.Connection) -> list[str]:
    return [
        row[0]
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='view' ORDER BY name"
        )
    ]


def iter_table_rows(
    conn: sqlite3.Connection, table: str
) -> Iterator[dict[str, Any]]:
    cols = table_columns(conn, table)
    for row in conn.execute(
        f"SELECT * FROM {quote_identifier(table)} ORDER BY rowid"
    ):
        yield dict(zip(cols, row))


def _reject_non_finite(token: str) -> None:
    # Python's JSON decoder accepts NaN/Infinity by default, but JSONL is JSON.
    raise ValueError(f"non-finite JSON number: {token}")


def iter_jsonl(path: str | Path) -> Iterator[dict[str, Any]]:
    """Yield canonical JSON objects; identify malformed records by file and line."""
    path = Path(path)
    with path.open(encoding="utf-8") as fh:
        for line_number, raw in enumerate(fh, start=1):
            line = raw.strip()
            if not line:
                continue
            try:
                row = json.loads(line, parse_constant=_reject_non_finite)
            except ValueError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSONL: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(
                    f"{path}:{line_number}: JSONL record must be a JSON object, "
                    f"not {type(row).__name__}"
                )
            yield row


def write_jsonl(path: str | Path, rows: Iterator[dict[str, Any]]) -> int:
    """Atomically replace one JSONL stream with strictly valid JSON objects."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    fd, tmp = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            for row in rows:
                if not isinstance(row, dict):
                    raise TypeError(
                        f"{path}: row {count + 1} must be a JSON object, "
                        f"not {type(row).__name__}"
                    )
                fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True, allow_nan=False))
                fh.write("\n")
                count += 1
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        # fdopen owns the descriptor after opening; close only if still open.
        try:
            os.close(fd)
        except OSError:
            pass
        raise
    return count


def jsonl_sha256(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()
