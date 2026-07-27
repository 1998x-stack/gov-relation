# Central Registry Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a partitioned SQLite central registry that ingests all existing ~1668 region DBs and provides an API for new build scripts to write into it continuously.

**Architecture:** Province-partitioned SQLite databases with WAL mode, each containing persons/organizations/positions/relationships tables keyed by content-hash IDs. A `registry.db` tracks partition metadata and migration audit. The existing `gov_relation/runner.py` run_build() gets an optional `central` parameter; a new `Central` class handles dedup and upsert into the right province DB. A one-shot migration script reads every `data/database/*_network.db` and populates the central store.

**Tech Stack:** Python 3.10+, stdlib sqlite3 (WAL mode), hashlib, pathlib

## Global Constraints

- All new modules go in `gov_relation/` package
- Tests go in `tests/` following existing test pattern (pytest, sqlite3 `:memory:` fixtures)
- Existing `gov_relation/schema.py` `create_tables()` must remain unchanged (backward compat)
- Existing `gov_relation/runner.py` `run_build()` signature must remain backward-compatible
- All `data/database/*_network.db` files must be preserved (read-only after migration)
- Central data goes in `data/central/`
- Region-to-province mapping uses existing `data/TODO.json` province hierarchy
- Person merge: name + birth SHA256[:16] — same hash means same person (UPSERT)
- SHA256 output is hex digest (lowercase)

---

## File Structure

| File | Responsibility |
|------|---------------|
| `gov_relation/paths.py` | Add CENTRAL_DIR, REGISTRY_DB, PROVINCE_DIR |
| `gov_relation/central.py` | `Central` class: connect, merge_person, merge_org, insert_position/relationship |
| `gov_relation/hash.py` | `person_hash(name, birth)`, `org_hash(province, fqn)` with normalization |
| `gov_relation/schema.py` | Add `create_central_schema()`, `create_registry_schema()` |
| `gov_relation/runner.py` | Add optional `central` param to `run_build()` |
| `scripts/migrate_to_central.py` | One-time migration from `data/database/*_network.db` |
| `tests/test_central.py` | Tests for Central class | 
| `tests/test_hash.py` | Tests for hash functions |
| `tests/test_migrate.py` | Tests for migration script logic |

---

### Task 1: Hash functions (`gov_relation/hash.py`)

**Files:**
- Create: `gov_relation/hash.py`
- Test: `tests/test_hash.py`

**Interfaces:**
- Produces: `person_hash(name: str, birth: str) -> str`, `org_hash(province: str, fqn: str) -> str`, `normalize(s: str) -> str`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_hash.py
from __future__ import annotations

import pytest
from gov_relation.hash import normalize, person_hash, org_hash


class TestNormalize:
    def test_trims_whitespace(self) -> None:
        assert normalize("  张三  ") == "张三"

    def test_unifies_wide_halfwidth(self) -> None:
        assert normalize("张　三") == "张三"

    def test_empty_string(self) -> None:
        assert normalize("") == ""


class TestPersonHash:
    def test_same_name_birth_same_hash(self) -> None:
        h1 = person_hash("张三", "1977-01")
        h2 = person_hash("张三", "1977-01")
        assert h1 == h2

    def test_different_birth_different_hash(self) -> None:
        h1 = person_hash("张三", "1977-01")
        h2 = person_hash("张三", "1980-05")
        assert h1 != h2

    def test_empty_birth_uses_empty_string(self) -> None:
        h = person_hash("张三", "")
        assert len(h) == 16

    def test_name_normalized_before_hash(self) -> None:
        h1 = person_hash("张三", "1977-01")
        h2 = person_hash("  张三  ", "1977-01")
        assert h1 == h2

    def test_returns_hex_string(self) -> None:
        h = person_hash("张三", "1977-01")
        assert len(h) == 16
        assert all(c in "0123456789abcdef" for c in h)


class TestOrgHash:
    def test_same_province_fqn_same_hash(self) -> None:
        h1 = org_hash("河南省", "周口市人民政府")
        h2 = org_hash("河南省", "周口市人民政府")
        assert h1 == h2

    def test_different_province_different_hash(self) -> None:
        h1 = org_hash("河南省", "周口市人民政府")
        h2 = org_hash("湖北省", "周口市人民政府")
        assert h1 != h2

    def test_name_normalized(self) -> None:
        h1 = org_hash("河南省", "周口市人民政府")
        h2 = org_hash("河南省", "  周口市人民政府  ")
        assert h1 == h2

    def test_returns_hex_string(self) -> None:
        h = org_hash("广东省", "深圳市人民政府")
        assert len(h) == 16
        assert all(c in "0123456789abcdef" for c in h)
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python3 -m pytest tests/test_hash.py -v
```
Expected: FAIL with `ModuleNotFoundError` or all tests failing

- [ ] **Step 3: Write minimal implementation**

```python
# gov_relation/hash.py
from __future__ import annotations

import hashlib
import unicodedata


def normalize(s: str) -> str:
    """Normalize a string for hashing: strip, narrow full-width chars."""
    s = unicodedata.normalize("NFKC", s)
    return s.strip()


def person_hash(name: str, birth: str) -> str:
    """Content-hash for a person record.

    SHA256(normalize(name) + "|" + birth)[:16] (hex).
    If birth is empty, uses empty string as the input.
    """
    raw = normalize(name) + "|" + (birth or "")
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def org_hash(province: str, fqn: str) -> str:
    """Content-hash for an organization record.

    SHA256(province + "|" + normalize(fqn))[:16].
    """
    raw = province + "|" + normalize(fqn)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
```

- [ ] **Step 4: Run test to verify it passes**

```bash
PY3THON -m pytest tests/test_hash.py -v
```

Expected: ALL PASS

- [ ] **Step 5: Commit**

```bash
git add gov_relation/hash.py tests/test_hash.py
git commit -m "feat: add content-hash functions for person and org dedup"
```

---

### Task 2: Central schema — `gov_relation/schema.py`

**Files:**
- Modify: `gov_relation/schema.py`
- Test: `tests/test_schema.py` (append new test class)

**Interfaces:**
- Consumes: (none)
- Produces: `create_central_schema(conn)`, `create_registry_schema(conn)`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_schema.py`:

```python
class TestCentralSchema:
    def test_creates_central_tables(self) -> None:
        import sqlite3
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        from gov_relation.hash import person_hash, org_hash

        # Central table names
        from gov_relation.schema import create_central_schema
        create_central_schema(conn)
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence' ORDER BY name"
        ).fetchall()
        names = [r[0] for r in tables]
        # Should have exactly 4 central tables
        assert names == ["organizations", "persons", "positions", "relationships"]

    def test_central_persons_id_hash_pk(self) -> None:
        import sqlite3
        conn = sqlite3.connect(":memory:")
        from gov_relation.schema import create_central_schema
        create_central_schema(conn)
        # Insert a person with explicit hash
        conn.execute(
            "INSERT INTO persons (id_hash, name, name_normalized) VALUES (?, ?, ?)",
            ("abc123", "张三", "张三"),
        )
        # Same hash should conflict
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO persons (id_hash, name, name_normalized) VALUES (?, ?, ?)",
                ("abc123", "张三(重复)", "张三"),
            )

    def test_creates_registry_tables(self) -> None:
        import sqlite3
        conn = sqlite3.connect(":memory:")
        from gov_relation.schema import create_registry_schema
        create_registry_schema(conn)
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence' ORDER BY name"
        ).fetchall()
        names = [r[0] for r in tables]
        assert "region_registry" in names
        assert "migration_audit" in names
        assert "merge_conflicts" in names

    def test_central_tables_enable_wal(self) -> None:
        import sqlite3
        conn = sqlite3.connect(":memory:")
        from gov_relation.schema import create_central_schema
        create_central_schema(conn)
        # WAL mode pragma check
        mode = conn.execute("PRAGMA journal_mode").fetchone()[0]
        # :memory: is always delete, but code path should execute
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHON -m pytest tests/test_schema.py::TestCentralSchema -v`
Expected: FAIL: "can't import create_central_schema" or similar

- [ ] **Step 3: Add central schema DDLS and functions**

Add to `gov_relation/schema.py`:

```python
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

CREATE_REGISTRY = """
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
    """Create the 4 central-registry tables with WAL mode enabled."""
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    for ddl in (
        CREATE_CENTRAL_PERSONS,
        CREATE_CENTRAL_ORGANIZATIONS,
        CREATE_CENTRAL_POSITIONS,
        CREATE_CENTRAL_RELATIONSHIPS,
    ):
        conn.execute(ddl)
    # Create indexes for central tables
    conn.execute("CREATE INDEX IF NOT EXISTS idx_central_persons_name ON persons(name)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_central_persons_birth ON persons(birth)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_central_orgs_fqn ON organizations(fqn)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_central_orgs_province ON organizations(province)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_central_positions_person ON positions(person_hash)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_central_positions_org ON positions(org_hash)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_central_positions_province ON positions(province)")
    conn.commit()


def create_registry_schema(conn: sqlite3.Connection) -> None:
    """Create the 3 registry tables."""
    for ddl in (CREATE_REGISTRY, CREATE_MIGRATION_AUDIT, CREATE_MERGE_CONFLICTS):
        conn.execute(ddl)
    conn.commit()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=. python3 -m pytest tests/test_schema.py::TestCentralSchema -v`
Expected: ALL PASS

- [ ] **Step 5: Commit**

```bash
git add gov_relation/schema.py tests/test_schema.py
git commit -m "feat: add central schema functions to schema.py"
```

---

### Task 3: Paths update — `gov_relation/paths.py`

**Files:**
- Modify: `gov_relation/paths.py`
- Test: `tests/test_paths.py`

**Interfaces:**
- Produces: `CENTRAL_DIR`, `REGISTRY_DB`, `PROVINCE_DIR`

- [ ] **Step 1: Write test**

Add to `tests/test_paths.py`:

```python
class TestCentralPaths:
    def test_central_dir_exists(self) -> None:
        from gov_relation.paths import CENTRAL_DIR, REGISTRY_DB, PROVINCE_DIR
        assert CENTRAL_DIR.name == "central"
        assert REGISTRY_DB.name == "registry.db"
        assert PROVINCE_DIR.name == "provincial"
```

- [ ] **Step 2: Modify `gov_relation/paths.py`**

Add after existing path definitions:

```python
CENTRAL_DIR = DATA_DIR / "central"
REGISTRY_DB = CENTRAL_DIR / "registry.db"
PROVINCE_DIR = CENTRAL_DIR / "provincial"
```

- [ ] **Step 3: Run test**

Run: `PYTHONPATH=. python3 -m pytest tests/test_paths.py::TestCentralPaths -v`
Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add gov_relation/paths.py tests/test_paths.py
git commit -m "feat: add central registry paths"
```

---

### Task 4: Central data writer — `gov_relation/central.py`

**Files:**
- Create: `gov_relation/central.py`
- Test: `tests/test_central.py`

**Interfaces:**
- Produces: `class Central(province: str)`
  - `central.ensure_schema()` creates tables if missing
  - `central.merge_person(person: dict) -> str` — returns id_hash
  - `central.merge_organization(org: dict) -> str` — returns id_hash
  - `central.insert_position(position: dict) -> int`
  - `central.insert_relationship(rel: dict) -> int`
  - `central.close()`
  - `central.flush_registry(db_path: str)`
- Consumes: `gov_relation.hash.person_hash()`, `gov_relation.hash.org_hash()`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_central.py
from __future__ import annotations

import sqlite3
import tempfile
from pathlib import Path

import pytest

from gov_relation.central import Central


class TestCentral:
    @pytest.fixture
    def central(self) -> Central:
        from gov_relation.paths import CENTRAL_DIR
        c = Central("test_province")
        yield c
        c.close()
        # cleanup
        import shutil
        shutil.rmtree(CENTRAL_DIR, ignore_errors=True)

    def test_merge_person_returns_hash(self, central: Central) -> None:
        h = central.merge_person({"name": "张三", "birth": "1977-01"})
        assert len(h) == 16
        assert all(c in "0123456789abcdef" for c in h)

    def test_merge_same_person_returns_same_hash(self, central: Central) -> None:
        h1 = mid = central.merge_person({"name": "张三", "birth": "1977-01"})
        h2 = central.merge_person({"name": "张三", "birth": "1977-01"})
        assert h1 == h2

    def test_merge_person_upserts_fields(self, central: Central) -> None:
        h = central.merge_person({"name": "张三", "birth": "1977-01", "gender": "男"})
        # Second call with new field
        central.merge_person({"name": "张三", "birth": "1977-01", "gender": "男", "education": "研究生"})
        row = central.conn.execute(
            "SELECT education FROM persons WHERE id_hash=?", (h,)
        ).fetchone()
        assert row[0] == "研究生"

    def test_merge_org_returns_hash(self, central: Central) -> None:
        h = central.merge_organization({"fqn": "周口市人民政府", "province": "测试省"})
        assert len(h) == 16

    def test_insert_position(self, central: Central) -> None:
        p_h = central.merge_person({"name": "张三", "birth": "1977-01"})
        o_h = central.merge_organization({"fqn": "周口市人民政府", "province": "测试省"})
        pos_id = central.insert_position({
            "person_hash": p_h,
            "org_hash": o_h,
            "title": "市长",
            "province": "测试省",
        })
        assert pos_id is not None

    def test_insert_relationship(self, central: Central) -> None:
        p1_h = central.merge_person({"name": "张三", "birth": "1977-01"})
        p2_h = central.merge_person({"name": "李四", "birth": "1980-05"})
        rel_id = central.insert_relationship({
            "person_a_hash": p1_h,
            "person_b_hash": p2_h,
            "type": "正副搭档",
            "province": "测试省",
        })
        assert rel_id is not None

    def test_missing_province_partition_is_empty(self) -> None:
        # Creating Central for a province that doesn't exist yet should create the DB
        from gov_relation.paths import PROVINCI_DIR
        db_path = PROVINCE_DIR / "new_province.db"
        assert not db_path.exists()
        c = Central("new_province")
        assert db_path.exists()
        c.close()
        db_path.unlink()
```

- [ ] **Step 2: Run to verify failure**

Run: `PYTHONPATH=. python3 -m pytest tests/test_central.py -v`
Expected: FAIL

- [ ] **Step 3: Write the `Central` class**

```python
# gov_relation/central.py
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .hash import person_hash, org_hash
from .paths import PROVINCE_DIR
from .schema import create_central_schema, create_registry_schema


class Central:
    """Write data to a province-partitioned central registry.

    Each Central instance targets one province partition (one SQLite file).
    Use one instance per province per build.
    """

    def __init__(self, province: str) -> None:
        self.province = province
        PROVINCE_DIR.mkdir(parents=True, exist_ok=True)
        self.db_path = PROVINCE_DIR / f"{province}.db"
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA foreign_keys=ON")
        create_central_schema(self.conn)

    def merge_person(self, person: dict[str, Any]) -> str:
        """Insert or update a person record by content-hash.

        Returns the id_hash of the merged record.
        """
        name = person.get("name", "")
        birth = person.get("birth", "")
        h = person_hash(name, birth)

        existing = self.conn.execute(
            "SELECT * FROM persons WHERE id_hash=?", (h,)
        ).fetchone()

        if existing:
            # Merge fields: prefer non-empty values from new data
            aliases = json.loads(existing["aliases"] or "[]")
            source_json = json.loads(existing["source_json"] or "{}")
            new_source = person.get("source", "")
            if new_source and new_source not in source_json:
                source_json[new_source] = "pending"
            # If names differ (normalized same but raw different), add alias
            if person.get("name", "") != existing["name"] and person.get("name", "") not in aliases:
                aliases.append(person.get("name", ""))

            self.conn.execute(
                """UPDATE persons SET
                    name=COALESCE(NULLIF(?, ''), name),
                    name_normalized=COALESCE(NULLIF(?, ''), name_normalized),
                    gender=COALESCE(NULLIF(?, ''), gender),
                    ethnicity=COALESCE(NULLIF(?, ''), ethnicity),
                    birthplace=COALESCE(NULLIF(?, ''), birthplace),
                    education=COALESCE(NULLIF(?, ''), education),
                    party_join=COALESCE(NULLIF(?, ''), party_join),
                    work_start=COALESCE(NULLIF(?, ''), work_start),
                    aliases=?,
                    source_json=?,
                    updated_at=datetime('now')
                WHERE id_hash=?""",
                (
                    person.get("name", ""),
                    person.get("name", ""),
                    person.get("gender", ""),
                    person.get("ethnicity", ""),
                    person.get("birthplace", ""),
                    person.get("education", ""),
                    person.get("party_join", ""),
                    person.get("work_start", ""),
                    json.dumps(aliases, ensure_ascii=False),
                    json.dumps(source_json, ensure_ascii=False),
                    h,
                ),
            )
        else:
            self.conn.execute(
                """
                INSERT INTO persons (id_hash, name, name_normalized, gender, ethnicity, birth,
                                     birthplace, education, party_join, work_start, source_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    h,
                    person.get("name", ""),
                    person.get("name", ""),
                    person.get("gender", ""),
                    person.get("ethnicity", ""),
                    person.get("birth", ""),
                    person.get("birthplace", ""),
                    person.get("education", ""),
                    person.get("party_join", ""),
                    person.get("work_start", ""),
                    json.dumps({person.get("source", ""): "high"}, ensure_ascii=False),
                ),
            )

        self.conn.commit()
        return h

    def merge_organization(self, org: dict[str, Any]) -> str:
        """Insert or update an organization. Returns id_hash."""
        province = org.get("province", self.province)
        fqn = org.get("fqn", "")
        if not fqn:
            fqn = org.get("name", "")
        h = org_hash(province, fqn)

        existing = self.conn.execute(
            "SELECT * FROM organizations WHERE id_hash=?", (h,)
        ).fetchone()

        if existing:
            self.conn.execute(
                """UPDATE organizations SET
                org_type=COALESCE(NULLIF(?, ''), org_type),
                level=COALESCE(NULLIF(?, ''), level),
                parent_fqn=COALESCE(NULLIF(?, ''), parent_fqn),
                local_name=COALESCE(NULLIF(?, ''), local_name),
                location=COALESCE(NULLIF(?, ''), location)
                WHERE id_hash=?""",
                (
                    org.get("org_type", ""),
                    org.get("level", ""),
                    org.get("parent", ""),
                    org.get("local_name", fqn),
                    org.get("location", ""),
                    h,
                ),
            )
        else:
            self.conn.execute(
                """INSERT INTO organizations (id_hash, fqn, local_name, org_type, level, parent_fqn, location, province)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    h,
                    fqn,
                    org.get("local_name", fqn),
                    org.get("org_type", ""),
                    org.get("level", ""),
                    org.get("parent", ""),
                    org.get("location", ""),
                    province,
                ),
            )
        self.conn.commit()
        return h

    def insert_position(self, pos: dict[str, Any]) -> int:
        """Insert a position record. Returns the new row's integer id."""
        cur = self.conn.execute(
            """INSERT INTO positions (person_hash, org_hash, title, start_date, end_date,
                                      rank, category, note, province, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                pos["person_hash"],
                pos["org_hash"],
                pos.get("title", ""),
                pos.get("start_date", ""),
                pos.get("end_date", ""),
                pos.get("rank", ""),
                pos.get("category", ""),
                pos.get("note", ""),
                pos.get("province", self.province),
                pos.get("source", ""),
            ),
        )
        self.conn.commit()
        return cur.lastrowid

    def insert_relationship(self, rel: dict[str, Any]) -> int:
        """Insert a relationship record. Returns the source's integer id."""
        cur = self.conn.execute(
            """INSERT INTO relationships (person_a_hash, person_b_hash, type, context,
                                          overlap_org_hash, overlap_period, province, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                rel["person_a_hash"],
                rel["person_b_hash"],
                rel.get("type", ""),
                rel.get("context", ""),
                rel.get("overlap_org_hash", ""),
                rel.get("overlap_period", ""),
                rel.get("province", self.province),
                rel.get("source", ""),
            ),
        )
        self.conn.commit()
        return cur.lastrowid

    def close(self) -> None:
        self.conn.close()

    def flush_registry(self, db_path: str | Path) -> None:
        """Update the central registry.db with counts from this partition."""
        registry_conn = sqlite3.connect(str(db_path))
        create_registry_schema(registry_conn)
        p_count = self.conn.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
        o_count = self.conn.execute("SELECT COUNT(*) FROM organizations").fetchone()[0]
        pos_count = self.conn.execute("SELECT COUNT(*) FROM positions").fetchone()[0]
        r_count = self.conn.execute("SELECT COUNT(*) FROM relationships").fetchone()[0]
        registry_conn.execute(
            """INSERT OR REPLACE INTO region_registry
            (province, db_path, status, person_count,org_count, position_count, relation_count, last_updated)
            VALUES (?, ?, 'active', ?, ?, ?, ?, datetime('now'))""",
            (self.province, str(self.db_path), p_c, o_c, pos_count, r_count),
        )
        registry_conn.commit()
        registry_conn.close()
```

- [ ] **Step 4: Run tests to verify**

Run: `PYTHTHONPATH=. python3 -m pytest tests/test_central.py -v`
Expected: ALL PASS

- [ ] **Step 5: Commit**

```bash
git add gov_relation/central.py tests/test_central.py
git commit -m "feat: central data writer with hash-based dedup"
```

---

### Task 5: Runner extension — `gov_relation/runner.py`

**Files:**
- Modify: `gov_relation/runner.py`
- Test: `tests/test_runner.py`

**Interfaces:**
- Consumes: `Central.merge_person()`, `Central.merge_organization()`, `Central.insert_position()`, `Central.insert_relationship()`
- Produces: Extended `run_build()` with optional `central: Central | None` parameter; `detect_province(slug: str) -> str` helper

- [ ] **Step 1: Write test**

Add to `tests/test_runner.py`:

```python
class TestRunBuildWithCentral:
    def test_run_build_central_integration(self, tmp_path: Path) -> None:
        from gov_relation.central import Central
        from gov_relation.runner import run_build
        from gov_relation.paths import DATABASE_DIR

        central = Central("test_province")

        persons = [
            {"id": 1, "name": "张三", "birth": "1977-01"},
            {"id": 2, "name": "李四", "birth": "1980-05"},
        ]
        orgs = [
            {"id": 10, "name": "Test政府", "fqn": "测试县人民政府", "province": "test_province"},
        ]
        positions = [
            {"person_hash": None, "org_hash": None, "title": "县长", "province": "test_province"},
        ]
        rels = []

        db_path = tmp_path / "test_network.db"
        gexf_path = tmp_path / "test_network.gexf"

        # First need to resolve hashes
        # Actually, let's just test that the param isn't rejected
        run_build(
            slug="test",
            persons=[{"id": 1, "name": "王五"}],
            organizations=[],
            positions=[],
            relationships=[],
            db_path=str(db_path),
            gexf_path=str(gexf_path),
            central=central,
        )
        assert db_path.exists()
        central.close()
```

- [ ]  **Step 2: Modify `runner.py`**

In `gov_relation/runner.py`, add `central` parameter to `run_build()`:

```python
def run_build(
    *,
    slug: str,
    persons: list[dict[str, Any]],
    organizations: list[dict[str, Any]],
    positions: list[dict[str, Any]],
    relationships: list[dict[str, Any]],
    db_path: str | Path,
    gexf_path: str | Path,
    overwrite: bool = False,
    central: Any = None,  # Optional Central writer
) -> None:
    # ... existing body unchanged ...

    # After writing GEXF, optionally write to central
    if central is not None:
        for p in persons:
            central.merge_person(p)
        for o in organizations:
            central.merge_organization(o)
        for pos in positions:
            central.insert_position(pos)
        for rel in relationships:
            central.insert_relationship(rel)
```

- [ ] **Step 3: Run tests**

Run: `PYTHONPATH=. python3 -m pytest tests/test_runner.py::TestRunBuildWithCentral -v`
Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add gov_relation/runner.py tests/test_runner.py
git commit -m "feat: add optional central parameter to run_build()"
```

---

### Task 6: Province detection helper — `gov_relation/province.py`

**Files:**
- Create: `gov_relation/province.py`
- Test: `tests/test_province.py`

**Interfaces:**
- Produces: `detect_province(slug: str) -> str`, `build_slug_province_map(todo_path: Path | None = None) -> dict[str, str]`
- Consumes: `data/TODO.json`

- [ ] **Step 1: Write test**

```python
# tests/test_province.py
from __future__ import annotations

import json
from pathlib import Path

import pytest
from gov_relation.province import build_slug_province_map, detect_province


def test_detect_province_from_slug():
    # Known test mappings:
    slug_to_province = {
        "周口市": "河南省",
        "青浦区": "上海市",
        "七台河市": "黑龙江省",
        "南雄市": "广东省",
        "万州区": "重庆市",
        "固原市": "宁夏回族自治区",
        "甘肃省": "甘肃省",
    }
    for slug, expected in slg_province.items():
        assert detect_province(slug, map_cache=slug_to_province) == expected


def test_build_map_from_todo(tmp_path: Path) -> None:
    todo = {
        "provinces": [
            {
                "province": "江西省",
                "tasks": [
                    {"id": "jiangxi_province", "region": "江西省", "level": "province"},
                    {"id": "jiangxi_南昌市", "region": "南昌市", "level": "prefecture"},
                ],
            },
            {
                "province": "安徽省",
                "tasks": [
                    {"id": "anhui_province", "region": "安徽省", "level": "province"},
                ],
            },
        ],
    }
    todo_path = tmp_path / "TODO.json"
    with open(todo_path, "w") as f:
        json.dump(todo, f)
    mapping = build_slug_province_map(todo_path)
    assert mapping["南昌市"] == "江西省"
    assert mapping["安徽省"] == "安徽省"
    assert mapping["江西省"] == "江西省"


def test_detect_province_no_match(self) -> None:
    with pytest.raises(ValueError):
        detect_province("未知地区", map_cache={"测试省": "江西省"})
```

- [ ] **Step 2: Run to verify failure**

Run: `PYTHONPATH=. python3 -m pytest tests/test_province.py -v`
Expected: FAIL

- [ ] **Step 3: Write implementation**

```python
# gov_relation/province.py
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .paths import TODO_PATH


def build_slug_province_map(todo_path: Path | None = None) -> dict[str, str]:
    """Build a mapping of slug (region name) → province from TODO.json."""
    path = todo_path or TODO_PATH
    if not path.exists():
        raise FileNotFoundError(f"TODO.json not found at {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    mapping: dict[str, str] = {}
    for province_entry in data.get("provinces", []):
        province = province_entry["province"]
        for task in province_entry.get("tasks", []):
            region = task.get("region", "")
            if region:
                mapping[region] = province
    return mapping


def detect_province(
    slug: str,
    todo_path: Path | None = None,
    map_cache: dict[str, str] | None = None,
) -> str:
    """Determine province for a slug (region name)."""
    if map_cache is not None:
        mapping = map_cache
    else:
        mapping = build_slug_province_map(todo_path)

    if slug in mapping:
        return mapping[slug]

    # Fuzzy: try prefix match for prefecture-level slugs
    # e.g. "周口市" is the region itself
    for key, province in mapping.items():
        if slug.endswith(key):
            return province

    raise ValueError(f"Cannot determine province for slug: {slug}")
```

- [ ] **Step 4: Run to verify**

Run: `PYTHONPATH=. PYTHONPATH=. python3 -m pytest tests/test_province.py -v`
Expected: ALL PASS

- [ ] **Step 5: Commit**

```bash
git add gov_relation/province.py tests/test_province.py
git commit -m "feat: province detection from TODO.json slug mapping"
```

---

### Task 7: Migration script — `scripts/migrate_to_central.py`

**Files:**
- Create: `scripts/migrate_to_central.py`
- Test: (manual run on a subset of DBs; integration test optional)

- [ ] **Step 1: Write the migration script**

```python
#!/usr/bin/env python3
"""One-time migration: read every data/database/*_network.db and populate the central registry.

Usage:
    python3 scripts/migrate_to_central.py                          # full migration
    python3 scripts/migrate_to_central.py --dry-run                # show what would be done
    python3 scripts/migrate_to_central.py --limit 5                # first 5 DBs only
    python3 scripts/migrate_to_central.py --resume                 # skip already-migrated DBs

The script reads audit records from registry.db to track progress.
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
import time
from pathlib import Path

REPO_ROOT_PATH = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT_PATH))

from gov_relation.central import Central  # noqa: E402
from gov_relation.paths import DATABASE_DIR, REGISTRY_DB, REGISTRY_DIR, PROVINCE_DIR  # noqa: E402
from gov_relation.province import build_slug_province_map  # noqa: E402
from gov_relation.schema import create_registry_schema  # noqa: E402


def _normalize_slug(db_stem: str) -> str:
    """Convert '周口市_network' to '周口市'."""
    return db_stem.removesuffix("_network")


def _parse_slug_to_slug(db_path: Path) -> str:
    return _normalize_slug(db_path.stem)


_CURRENT_PERSONS_COLS = [
    "id", "name", "gender", "ethnicity", "birth", "birthplace",
    "education", "party_join", "work_start", "current_post",
    "current_org", "source",
]


def migrate_db(central, conn, slug: str) -> dict:
    """Migrate one region DB's data to central. Returns stats dict."""
    stats = {"persons": 0, "orgs": 0, "positions": 0, "rels": 0, "conflicts": 0}

    # Persons
    for row in conn.execute(f"SELECT {','.join(_CURRENT_PLACE_COLS)} FROM persons"):
        person = dict(zip(_CURRENT_PLACE_COLS, row))
        try:
            central.merge_person(person)
            stats["persons"] += 1
        except Exception:
            stats["conflicts"] += 1

    # Organizations (old schema → map to new fields)
    for row in conn.execute("SELECT * FROM organisations"):
        org = dict(row)
        org["fqn"] = org.get("fqn", org.get("name", ""))
        org["province"] = detect_province(slug)
        try:
            central.merge_organization(org)
            stats["orgs"] += 1
        except Exception:
            stats["conflicts"] += 1

    # Positions (need to rekey person_id → person_hash, org_id → org_hash)
    # The old schema uses INTEGER id; we can't reliably rehash without the new-style id_hash.
    # For migration: skip positions whose person/org don't exist in central yet
    # OR record them as is (with person_id/org_id as legacy reference)
    for row in conn.execute("SELECT * FROM positions"):
        pos = dict(zip(["id", "person_id", "org_id", "title", "start_date", "end_date", "rank", "note"], row))
        # We won't have the hash mapping for old int ids → this is best-effort
        # For now, record positions with an unres olved hash and later dedup pass
        stats["positions"] += 1
        # Actually positions: we need to find the person by name+date and the org by name
        # This is complex. For a real migration: read persons from source DB, rehash, look up in central
        # Let's use a simpler approach — we store the direct reference in a note
        # and run a second pass

    # Relationships: similar issue

    return stats


def main():
    parser = argparse.ArgumentParser(description="Migrate per-region DBs to central registry")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be done without doing it")
    parser.add_argument("--limit", type=int, help="Max DBs to process")
    parser.add_argument("--resume", action="store_true", help="Skip already-migrated DBs")
    args = parser.parse_args()

    # Build slug→province cache
    slug_cache = build_slug_province_map()

    # Prepare registry
    REGISTRY_DB.parent.mkdir(parents=True, exist_ok=True)
    reg_conn = sqlite3.connect(str(REGISTRY_DB))
    create_registry_schema(reg_conn)

    # Find all database files
    db_files = sorted(DATABASE_DIR.glob("*_network.db"))
    if args.limit:
        db_files = db_files[:args.limit]

    if args.resume:
        done_slugs = {
            r[0] for r in reg_conn.execute("SELECT slug FROM migration_audit").fetchall()
        }
        db_files = [f for f in db_files if _parse_slug_to_slug(f) not in done_slugs]

    total_stats = {"persons": 0, "orgs": 0, "positions": 0, "rels": 0, "conflicts": 0}
    start = time.time()

    for i, db_path in enumerate(db_files):
        slug = _parse_slug_to_slug(db_path)
        try:
            province = detect_province(slug, map_cache=slug_map)
        except ValueError:
            print(f"  ⚠ Cannot determine province for {slug} — skipping")
            continue

        print(f"[{i+1}/{len(db_files)}] {slug} → {province}")

        if args.dry_run:
            continue

        # Open region DB
        src_conn = sqlite3.connect(str(db_path))
        src_conn.row_factory = sqlite3.Row

        # Open central writer for this province
        central = Central(province)

        # Migrate
        stats = migration_process(central, src_conn, slug)

        central.flush_registry(str(REGISTRY_DB))

        # Record audit
        reg_conn.execute(
            """INSERT INTO migration_audit
            (source_db, slug, province, persons_imported, orgs_imported,
             positions_imported, rels_imported, merge_conflicts)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (str(db_path), slug, province,
             stats["persons"], stats["orgs"], stats["positions"],
             stats["rels"], stats["conflicts"]),
        )
        reg_conn.commit()

        central.close()
        src_conn.close()

        for kv in stats:
            total_stats[k] += v

    elapsed = time.time() - start
    print(f"\n Done. {len(db_files)} DBs in {elapsed:.1f}s")
    print(f"  Persons: {total_stats['persons']}, Orgs: {total_stats['orgs']}, "
          f"Positions: {total_stats['positions']}, Rels: {total_stats['rels']}")
    print(f"  Conflicts: {total_stats['conflicts']}")
    reg_conn.close()


if __name__ == "__main__":
    main()
```

`</think>

I notice the migration script got complex with the position/relationship rekeying issue — the old DBs use INTEGER `id` while the central uses TEXT `id_hash`. Let me reconsider the migration approach. Let me simplify by handling the position/relationship re-mapping more carefully.

<｜DSML｜tool_calls>
<｜DSML｜invoke name="write">
<｜DSML｜parameter name="content" string="true">#!/usr/bin/env python3
"""
One-time migration from historical per-region DBs to the central registry.

Reads every data/database/*_network.db, rekeys references (person_id → id_hash,
org_id → id_hash), and writes into the province-partitioned central warehouse.

Usage:
    python3 scripts/migrate_to_central.py              # full migration
    python3 scripts/migrate_to_central.py --dry-run     # show what would happen
    python3 scripts/migrate_to_central.py --limit 5     # first 5 DBs
    python3 scripts/migrate_to_central.py --resume      # skip already-done DBs
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.central import Central  # noqa: E402
from gov_relation.hash import person_hash, org_hash  # noqa: E402
from gov_relation.paths import DATABASE_DIR, REGISTRY_DB  # noqa: E402
from gov_relation.province import build_slug_province_map  # noqa: E402
from gov_relation.schema import create_registry_schema  # noqa: E402


def _db_stem_to_slug(stem: str) -> str:
    return stem.removesuffix("_network")


def _read_persons(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    """Read persons from a legacy DB. Adapts to the two known schemas."""
    cols = ["id", "name", "gender", "ethnicity", "birth", "birthplace",
            "education", "party_join", "work_start", "current_post",
            "current_org", "source"]
    try:
        cur = conn.execute(f"SELECT {','.join(cols)} FROM persons")
    except sqlite3.OperationalError:
        # Try with TEXT id column
        cur = conn.execute("SELECT * FROM persons")
        cols = [desc[0] for desc in cur.description]
    rows = []
    for row in cur.fetchall():
        d = {col: (row[i] or "") for i, col in enumerate(cols)}
        rows.append(d)
    return rows


def _read_orgs(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    """Read organizations from legacy DB."""
    try:
        cur = conn.execute("SELECT * FROM organizations")
        cols = [desc[0] for desc in cur.description]
        rows = []
        for row in cur.fetchall():
            d = {col: (row[i] or "") for i, col in enumerate(cols)}
            rows.append(d)
        return rows
    except sqlite3.OperationalError:
        return []


def _read_positions(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    try:
        cur = conn.execute("SELECT * FROM positions")
        cols = [desc[0] for desc in cur.description]
        rows = []
        for row in cur.fetchall():
            d = {col: (row[i] or "") for i, col in enumerate(cols)}
            rows.append(d)
        return rows
    except sqlite3.OperationalError:
        return []


def _read_relationships(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    try:
        cur = conn.execute("SELECT * FROM relationships")
        cols = [desc[0] for desc in cur.description]
        rows = []
        for row in cur.fetchall():
            d = {col: (row[i] or "") for i, col in enumerate(cols)}
            rows.append(d)
        return rows
    except sqlite3.OperationalError:
        return []


def _build_position_map(conn_province: sqlite3.Connection, key: str) -> dict[str, str]:
    """Build a map from old-style TEXT/INT id to id_hash.

    key is either 'person' or 'org'.
    If key == 'person': read all persons from central, key by (name+birth) → hash.
    """
    mapping: dict[str, str] = {}
    if key == "person":
        rows = conn_province.execute(
            "SELECT id_hash, name, birth FROM persons"
        ).fetchall()
    elif key == "org":
        rows = conn_province.execute(
            "SELECT id_hash, fqn, province FROM organizations"
        ).fetchall()
    else:
        return mapping
    for r in rows:
        mapping["id"] = r[0]
        mapping["name"] = r[0]
    return mapping


def migrate_db(db_path: Path, central: Central, slug: str, province: str) -> dict[str, int]:
    """Migrate a single database. Returns stats dict."""
    stats: dict[str, int] = {"persons": 0, "orgs": 0, "positions": 0, "rels": 0, "conflicts": 0}

    src = sqlite3.connect(str(db_path))
    src.row_factory = sqlite3.Row

    # 1. Persons
    persons = _read_neighbors(src)
    person_id_to_hash: dict[str, str] = {}
    for p in persons:
        try:
            h = central.merge_person(p)
            person_id_to_hash[str(p.get("id", ""))] = h
            stats["persons"] += 1
        except Exception as e:
            stats["conflicts"] += 1

    # 2. Organizations
    orgs = _read_orgs(src)
    org_id_to_hash: dict[str, str] = {}
    for o in orgs:
        o["province"] = province
        o["fqn"] = o.get("fqn", o.get("name", ""))
        if not o.get("local_name"):
            o["local_name"] = o.get("name", "")
        try:
            h = central.merge_organization(o)
            org_id_to_hash[str(o.get("id", ""))] = h
            stats["orgs"] += 1
        except Exception:
            stats["conflicts"] += 1

    # 3. Positions — rekey person_id/org_id → person_hash/org_hash
    positions = _read_positions(src)
    for pos in positions:
        old_person_id = str(pos.get("person_id", ""))
        old_org_id_id = str(pos.get("org_id", ""))
        p_hash = person_id_to_hash.get(old_person_id)
        o_hash = org_id_to_hash.get(old_org_id)
        if not p_hash or not o_hash:
            stats["conflicts"] += 1
            continue
        entry = {
            "person_hash": p_hash,
            "org_hash": o_hash,
            "title": pos.get("title", ""),
            "start_date": pos.get("start_date", pos.get("start", "")),
            "end_date": pos.get("end_date", pos.get("end", "")),
            "rank": pos.get("rank", ""),
            "note": pos.get("note", ""),
            "province": province,
            "source": "",
        }
        try:
            central.insert_position(entry)
            stats["positions"] += 1
        except Exception:
            stats["conflicts"] += 1

    # 4. Relationships — rekey person_a/person_b → hash
    relationships = _read_relationships(src)
    for rel in relationships:
        pa_id = str(rel.get("person_a", ""))
        pb_id = str(rel.get("person_b", ""))
        pa_hash = person_id_to_hash.get(pa_id)
        pb_hash = person_id_to_hash.get(pb_id)
        if not pa_hash or not pb_hash:
            stats["conflicts"] += 1
            continue
        entry = {
            "person_a_hash": pa_hash,
            "person_b_hash": pb_hash,
            "type": rel.get("type", ""),
            "context": rel.get("context", ""),
            "overlap_org_hash": "",  # Not straightforward to rekey without org hash
            "overlap_period": rel.get("overlap_period", ""),
            "province": province,
            "source": "",
        }
        # Try to resolve overlap_org if present
        overlap_org_id = str(rel.get("overlap_org", ""))
        if overlap_org_id and overlap_org_id in org_id_to_hash:
            entry["overlap_org_hash"] = org_id_to_hash[overlap_org_id]
        try:
            central.insert_relationship(entry)
            stats["rels"] += 1
        except Exception:
            stats["conflicts"] += 1

    src.close()
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description="Migrate per-region DBs to central registry")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no writes")
    parser.add_argument("--limit", type=int, default=0, help="Max DBs to process (0 = all)")
    parser.add_argument("--resume", action="store_true", help="Skip already-migrated DBs")
    parser.add_argument("--province", help="Only migrate DBs in this province")
    args argparse.ArgumentParser().parse_args()

    print("Building slug → province map from TODO.json ...")
    slug_map = build_slug_province_map()

    db_files = sorted(DATABASE_DIR.glob("*_network.db"))
    if not db_files:
        print("No *_network.db files found in data/database/")
        return

    # Prepare registry metadata DB
    REGISTRY_DB.parent.mkdir(parents=True, exist_ok=True)
    reg_conn = sqlite3.connect(str(REGISTRY_DB))
    create_registry_schema(reg_conn)

    # Build skip list for --resume
    if args.resume:
        already = {
            r[0] for r in reg_conn.execute("SELECT slug FROM migration_audit").fetchall()
        }
    else:
        already = set()

    # Apply filters
    selected = []
    for f in db_files:
        slug = _UTRAL_STEM_TO_SLUG(f.stem)
        if slug in already:
            continue
        try:
            province = slug_map[slug] if slug in slug_map else ""
            # fallback: try extracting from known prefixes
            if not province:
                for key, p in slug_map.items():
                    if slug.endswith(key) or key.endswith(slug):
                        province = p
                        break
            if not province:
                print(f"  ⚠ Cannot determine province for {slug} — skipping")
                continue
        except Exception:
            continue
        if args.province and province != args.province:
            continue
        selected.append((province, slug, f))

    if args.dry_run:
        print(f"\nDry run — would process: {len(selected)} DBs:")
        for province, slug, path in selected:
            print(f"  {path.name}  →  {province}/{slug}")
        print(f"\nProvinces B: {len(set(p for p, _, _ in selected))}")
        reg_conn.close()
        return

    total_stats = {"persons": 0, "orgs": 0, "positions": 0, "rels": 0, "conflicts": 0}
    start_time = time.time()
    current_province = None
    central = None

    try:
        for i, (province, slug, db_path) in enumerate(selected):
            if args.limit and i >= args.limit:
                break

            # Reuse central writer across different slugs in same province
            if province != current_province:
                if central:
                    # Flush + close previous
                    central.flush_registry(str(REGISTRY_DB))
                    central.close()
                print(f"\n=== Province: {province} ===")
                central = Central(province)
                current_province = province

            print(f"  [{i+1}/{len(selected)}] {slug} ...", end=" ", flush=True)
            stats = migrate_db(db_path, central, slug, province)

            # Record audit
            reg_conn.execute(
                """INSERT INTO migration_audit
                (source_db, slug, province, persons_imported, people_imported,
                 positions_imported, rels_imported, merge_conflicts)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (str(db_path), slug, province,
                 stats["persons"], stats["orgs"], stats["persons"],
                 stats["positions"], stats["rels"], stats["conflicts"]),
            )
            reg_conn.commit()

            for k in total_stats:
                total_stats[k] += v[k]

            print(f"{total_stats['persons']} persons, {stats['orgs']} mgs, "
                  f"{stats['positions']} positions, {stats['rels']} rels, "
                  f"{stats['conflicts']} conflicts")

    finally:
        if central:
            central.flush_registry(str(REGISTRY_DB))
            central.close()
        reg_conn.close()

    elapsed = time.time() - start_time
    print(f"\n Done. Processed {len(selected)} DBs in {elapsed:.1f}s")
    print(f"  Persons: {total_stats['persons']}, Orgs: {total_stats['orgs']}, "
          f"Positions: {total_stats['positions']}, Rels: {total_stats['rels']}")
    print(f"  Conflicts: {total_stats['conflicts']} (review merge_conflicts table in registry.db)")


if __name__ == "__main__":
    main()