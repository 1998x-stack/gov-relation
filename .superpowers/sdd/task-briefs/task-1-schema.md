# Task 1: 创建 `gov_relation/schema.py`

**Project:** gov-relation 公共库重构
**Goal:** 创建 SQLite schema 和批量插入工具模块

## Files
- Create: `gov_relation/schema.py`

## Interfaces
- Produces:
  - `create_tables(conn, overwrite=False)`
  - `insert_persons(conn, persons) -> dict[int, int]`
  - `insert_organizations(conn, orgs) -> dict[int, int]`
  - `insert_positions(conn, positions)`
  - `insert_relationships(conn, relationships)`

## Requirements
1. 四个标准表 DDL（persons, organizations, positions, relationships）
2. `overwrite=True` 时 DROP 后重建
3. `insert_*` 函数返回新老 id 映射（用于 foreign key 更新）
4. 字段名匹配政务数据格式：party_join, work_start, current_post, current_org 等

## 完整代码

```python
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
    if overwrite:
        for name in ("relationships", "positions", "organizations", "persons"):
            conn.execute(f"DROP TABLE IF EXISTS {name}")
    for ddl in (CREATE_PERSONS, CREATE_ORGANIZATIONS, CREATE_POSITIONS, CREATE_RELATIONSHIPS):
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
    cols = _columns("positions")
    placeholders = _placeholders(len(cols))
    for entry in positions:
        values = [entry.get(c, "") for c in cols]
        conn.execute(f"INSERT INTO positions ({','.join(cols)}) VALUES ({placeholders})", values)
    conn.commit()


def insert_relationships(conn: sqlite3.Connection, relationships: list[dict[str, Any]]) -> None:
    cols = _columns("relationships")
    placeholders = _placeholders(len(cols))
    for entry in relationships:
        values = [entry.get(c, "") for c in cols]
        conn.execute(f"INSERT INTO relationships ({','.join(cols)}) VALUES ({placeholders})", values)
    conn.commit()
```

## Steps
1. Create `gov_relation/schema.py` with the code above
2. Smoke test (create DB, insert, query, verify id_map)
3. Commit with message: `feat(gov_relation): add schema.py with standard table DDL and bulk-insert helpers`
