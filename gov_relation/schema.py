"""SQLite schema and bulk-insert helpers for the gov-relation pipeline."""

from __future__ import annotations

import sqlite3
from typing import Any

CREATE_PERSONS = """
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    gender TEXT DEFAULT '',
    ethnicity TEXT DEFAULT '',
    birth TEXT DEFAULT '',
    birthplace TEXT DEFAULT '',
    education TEXT DEFAULT '',
    party_join TEXT DEFAULT '',
    work_start TEXT DEFAULT '',
    current_post TEXT DEFAULT '',
    current_org TEXT DEFAULT '',
    source TEXT DEFAULT ''
)
"""

CREATE_ORGANIZATIONS = """
CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT DEFAULT '',
    level TEXT DEFAULT '',
    parent TEXT DEFAULT '',
    location TEXT DEFAULT ''
)
"""

CREATE_POSITIONS = """
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL,
    org_id INTEGER NOT NULL,
    title TEXT DEFAULT '',
    start_date TEXT DEFAULT '',
    end_date TEXT DEFAULT '',
    rank TEXT DEFAULT '',
    note TEXT DEFAULT '',
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
)
"""

CREATE_RELATIONSHIPS = """
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER NOT NULL,
    person_b INTEGER NOT NULL,
    type TEXT DEFAULT '',
    context TEXT DEFAULT '',
    overlap_org TEXT DEFAULT '',
    overlap_period TEXT DEFAULT '',
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
)
"""


def create_tables(conn: sqlite3.Connection, overwrite: bool = False) -> None:
    """Create the four standard tables.

    Parameters
    ----------
    conn:
        Open SQLite connection.
    overwrite:
        If True, DROP existing tables before creating them.
    """
    if overwrite:
        for name in ("relationships", "positions", "organizations", "persons"):
            conn.execute(f"DROP TABLE IF EXISTS {name}")
    for ddl in (CREATE_PERSONS, CREATE_ORGANIZATIONS, CREATE_POSITIONS, CREATE_RELATIONSHIPS):
        conn.execute(ddl)
    conn.commit()


# ── Central registry schema (province-partitioned) ────────────────────

CREATE_CENTRAL_PERSONS = """
CREATE TABLE IF NOT EXISTS persons (
    id_hash TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    name_normalized TEXT NOT NULL,
    gender TEXT DEFAULT '',
    ethnicity TEXT DEFAULT '',
    birth TEXT DEFAULT '',
    birthplace TEXT DEFAULT '',
    education TEXT DEFAULT '',
    party_join TEXT DEFAULT '',
    work_start TEXT DEFAULT '',
    aliases TEXT DEFAULT '[]',
    source_json TEXT DEFAULT '{}',
    updated_at TEXT DEFAULT (datetime('now'))
)
"""

CREATE_CENTRAL_ORGANIZATIONS = """
CREATE TABLE IF NOT EXISTS organizations (
    id_hash TEXT PRIMARY KEY,
    fqn TEXT NOT NULL,
    local_name TEXT NOT NULL,
    org_type TEXT DEFAULT '',
    level TEXT DEFAULT '',
    parent_fqn TEXT DEFAULT '',
    location TEXT DEFAULT '',
    province TEXT NOT NULL
)
"""

CREATE_CENTRAL_POSITIONS = """
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_hash TEXT NOT NULL,
    org_hash TEXT NOT NULL,
    title TEXT DEFAULT '',
    start_date TEXT DEFAULT '',
    end_date TEXT DEFAULT '',
    rank TEXT DEFAULT '',
    category TEXT DEFAULT '',
    note TEXT DEFAULT '',
    province TEXT NOT NULL,
    source TEXT DEFAULT '',
    FOREIGN KEY (person_hash) REFERENCES persons(id_hash),
    FOREIGN KEY (org_hash) REFERENCES organizations(id_hash)
)
"""

CREATE_CENTRAL_RELATIONSHIPS = """
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a_hash TEXT NOT NULL,
    person_b_hash TEXT NOT NULL,
    type TEXT DEFAULT '',
    context TEXT DEFAULT '',
    overlap_org_hash TEXT DEFAULT '',
    overlap_period TEXT DEFAULT '',
    province TEXT NOT NULL,
    source TEXT DEFAULT '',
    FOREIGN KEY (person_a_hash) REFERENCES persons(id_hash),
    FOREIGN KEY (person_b_hash) REFERENCES persons(id_hash),
    FOREIGN KEY (overlap_org_hash) REFERENCES organizations(id_hash)
)
"""

CREATE_REGION_REGISTRY = """
CREATE TABLE IF NOT EXISTS region_registry (
    province TEXT PRIMARY KEY,
    db_path TEXT NOT NULL,
    status TEXT DEFAULT 'active',
    person_count INTEGER DEFAULT 0,
    org_count INTEGER DEFAULT 0,
    position_count INTEGER DEFAULT 0,
    relation_count INTEGER DEFAULT 0,
    migrated_at TEXT,
    last_updated TEXT
)
"""

CREATE_MIGRATION_AUDIT = """
CREATE TABLE IF NOT EXISTS migration_audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_db TEXT NOT NULL,
    slug TEXT NOT NULL,
    province TEXT NOT NULL,
    persons_imported INTEGER DEFAULT 0,
    orgs_imported INTEGER DEFAULT 0,
    positions_imported INTEGER DEFAULT 0,
    rels_imported INTEGER DEFAULT 0,
    merge_conflicts INTEGER DEFAULT 0,
    migrated_at TEXT DEFAULT (datetime('now'))
)
"""

CREATE_MERGE_CONFLICTS = """
CREATE TABLE IF NOT EXISTS merge_conflicts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conflict_type TEXT NOT NULL,
    left_data TEXT,
    right_data TEXT,
    resolution TEXT DEFAULT 'pending',
    resolved_by TEXT DEFAULT '',
    resolved_at TEXT
)
"""


def create_central_schema(conn: sqlite3.Connection) -> None:
    """Create the 4 central-registry tables with WAL mode and indexes."""
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    for ddl in (CREATE_CENTRAL_PERSONS, CREATE_CENTRAL_ORGANIZATIONS,
                CREATE_CENTRAL_POSITIONS, CREATE_CENTRAL_RELATIONSHIPS):
        conn.execute(ddl)
    for idx in (
        "CREATE INDEX IF NOT EXISTS idx_central_persons_name ON persons(name)",
        "CREATE INDEX IF NOT EXISTS idx_central_orgs_province ON organizations(province)",
        "CREATE INDEX IF NOT EXISTS idx_central_positions_person ON positions(person_hash)",
        "CREATE INDEX IF NOT EXISTS idx_central_positions_org ON positions(org_hash)",
        "CREATE INDEX IF NOT EXISTS idx_central_positions_province ON positions(province)",
    ):
        conn.execute(idx)
    conn.commit()


def create_registry_schema(conn: sqlite3.Connection) -> None:
    """Create registry metadata tables."""
    for ddl in (CREATE_REGION_REGISTRY, CREATE_MIGRATION_AUDIT, CREATE_MERGE_CONFLICTS):
        conn.execute(ddl)
    conn.commit()


_COLUMN_MAP: dict[str, list[str]] = {
    "persons": ["id", "name", "gender", "ethnicity", "birth", "birthplace",
                 "education", "party_join", "work_start", "current_post",
                 "current_org", "source"],
    "organizations": ["id", "name", "type", "level", "parent", "location"],
    "positions": ["person_id", "org_id", "title", "start_date", "end_date", "rank", "note"],
    "relationships": ["person_a", "person_b", "type", "context", "overlap_org", "overlap_period"],
}


def _columns(table: str) -> list[str]:
    return _COLUMN_MAP.get(table, [])


def _placeholders(count: int) -> str:
    return ",".join("?" for _ in range(count))


def insert_persons(conn: sqlite3.Connection, persons: list[dict[str, Any]]) -> dict[int, int]:
    """Insert persons and return a mapping from old id to new rowid.

    The returned mapping lets callers update foreign keys after insertion.
    """
    cols = _columns("persons")
    placeholders = _placeholders(len(cols))
    id_map: dict[int, int] = {}
    for entry in persons:
        values = [entry.get(c, "") for c in cols]
        cur = conn.execute(f"INSERT INTO persons ({','.join(cols)}) VALUES ({placeholders})", values)
        id_map[entry["id"]] = cur.lastrowid
    conn.commit()
    return id_map


def insert_organizations(conn: sqlite3.Connection, organizations: list[dict[str, Any]]) -> dict[int, int]:
    """Insert organizations and return a mapping from old id to new rowid."""
    cols = _columns("organizations")
    placeholders = _placeholders(len(cols))
    id_map: dict[int, int] = {}
    for entry in organizations:
        values = [entry.get(c, "") for c in cols]
        cur = conn.execute(f"INSERT INTO organizations ({','.join(cols)}) VALUES ({placeholders})", values)
        id_map[entry["id"]] = cur.lastrowid
    conn.commit()
    return id_map


def insert_positions(conn: sqlite3.Connection, positions: list[dict[str, Any]]) -> None:
    """Insert position records."""
    cols = _columns("positions")
    placeholders = _placeholders(len(cols))
    for entry in positions:
        values = [entry.get(c, "") for c in cols]
        conn.execute(f"INSERT INTO positions ({','.join(cols)}) VALUES ({placeholders})", values)
    conn.commit()


def insert_relationships(conn: sqlite3.Connection, relationships: list[dict[str, Any]]) -> None:
    """Insert relationship records."""
    cols = _columns("relationships")
    placeholders = _placeholders(len(cols))
    for entry in relationships:
        values = [entry.get(c, "") for c in cols]
        conn.execute(f"INSERT INTO relationships ({','.join(cols)}) VALUES ({placeholders})", values)
    conn.commit()
