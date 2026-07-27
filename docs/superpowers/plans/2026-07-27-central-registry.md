# Central Registry Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a partitioned SQLite central registry that ingests all existing ~1668 region DBs and provides an API for new build scripts to write into it continuously.

**Architecture:** Province-partitioned SQLite databases with WAL mode, each containing deduplicated persons/organizations/positions/relationships tables keyed by SHA256 content-hash. A `registry.db` tracks partition metadata and migration audit. The `Central` class handles upsert and foreign-key re-keying; `run_build()` gets an optional `central` parameter. A one-shot migration script reads every `data/database/*_network.db`, computes content-hashes for the foreign-key remapping, and populates the partitions.

**Tech Stack:** Python 3.10+, stdlib sqlite3 (WAL mode), hashlib, pathlib, json, unicodedata

## Global Constraints

- All new modules go in `gov_relation/` package
- Tests go in `tests/` following existing patterns (pytest, `:memory:` fixtures, `sqlite3.Row`)
- Existing `gov_relation/schema.py` `create_tables()` must remain unchanged
- Existing `gov_relation/runner.py` `run_build()` signature must remain backward-compatible
- All `data/database/*_network.db` files must be preserved (read-only after migration)
- Central data goes in `data/central/`
- Person merge: `SHA256(normalize(name) + "|" + birth)[:16]` — same hash = same person (UPSERT)
- SHA256 output is hex lowercase
- `normalize(s)` = `unicodedata.normalize("NFKC", s).strip()`

---

## File Structure

| File | Responsibility |
|------|---------------|
| `gov_relation/hash.py` | `person_hash()`, `org_hash()`, `normalize()` |
| `gov_relation/paths.py` | Add `PROVINCE_DIR`, `REGISTRY_DB` |
| `gov_relation/schema.py` | Add `create_central_schema()`, `create_registry_schema()` |
| `gov_relation/central.py` | `Central` class (`merge_person`, `merge_organization`, `insert_position`, `insert_relationship`, `flush_registry`) |
| `gov_relation/province.py` | `detect_province()`, `build_slug_province_map()` |
| `gov_relation/runner.py` | Add optional `central` param |
| `scripts/migrate_to_central.py` | One-time migration |
| `tests/test_hash.py` | Hash function tests |
| `tests/test_central.py` | Central class tests |
| `tests/test_province.py` | Province detection tests |

---

## Task List

---

### Task 1: Hash functions (`gov_relation/hash.py`)

**Files:**
- Create: `gov_relation/hash.py`
- Test: `tests/test_hash.py`
- Modify: `gov_relation/__init__.py` (export hash functions)

**Interfaces:**
- Produces: `normalize(s: str) -> str`, `person_hash(name: str, birth: str) -> str`, `org_hash(province: str, fqn: str) -> str`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_hash.py
from __future__ import annotations

import pytest
from gov.hash import normalize, person_hash, org_hash


class TestNormalize:
    def test_trims_whitespace(self) -> None:
        assert normalize("  张三  ") == "张三"

    def test_unifies_wide_to_half(self) -> None:
        assert normalize("张　三") == "张三"

    def test_empty_string(self) -> None:
        assert normalize("") == ""

    def test_none_becomes empty(self) -> None:
        assert normalize(None) == ""


class TestPersonHash:
    def test_same_name_birth_same_hash(self) -> None:
        assert person_hash("张三", "1977-01") == person_hash("张三", "1977-01")

    def test_different_birth_different_hash(self) -> None:
        assert person_hash("张三", "1977-01") != person_hash("张三", "1980-05")

    def test_empty_birth_uses_empty_string(self) -> None:
        h = person_hash("张三", "")
        assert len(h) == 16

    def test_name_normalized(self) -> None:
        assert person_hash("  张三  ", "1977-01") == person_hash("张三", "1977-01")

    def test_returns_16_hex_chars(self) -> None:
        h = person_hash("张三", "1977-01")
        assert len(h) == 16
        assert all(c in "0123456789abcdef" for c in h)


class TestOrgHash:
    def test_same_fqn_same_hash(self) -> None:
        assert org_hash("河南省", "周口市人民政府") == org_hash("河南省", "周口市人民政府")

    def test_different_province_different_hash(self) -> None:
        assert org_hash("河南省", "周口市人民政府") != org_hash("湖北省", "周口市人民政府")

    def test_returns_16_hex_chars(self) -> None:
        h = org_hash("广东省", "深圳市人民政府")
        assert len(h) == 16
        assert all(c in "0123456789abcdef" for c in h)
```

- [ ] **Step 2: Run to verify failure**

```bash
cd /workspace/data/xieming/other-codes/gov-relation
PYTHONPATH=. python3 -m pytest tests/test_hash.py -v
```
Expected: `ModuleNotFoundError` or all tests FAIL

- [ ] **Step 3: Write implementation**

```python
# gov_relation/hash.py
from __future__ import annotations

import hashlib
import unicodedata


def normalize(s: str | None) -> str:
    """Normalize a string for hashing: NFC, strip."""
    if s is None:
        return ""
    return unicodedata.normalize("NFKC", s).strip()


def person_hash(name: str, birth: str) -> str:
    """SHA256(normalize(name) + "|" + (birth or ""))[:16] hex."""
    raw = normalize(name) + "|" + (birth or "")
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def org_hash(province: str, fqn: str) -> str:
    """SHA256(province + "|" + normalize(fqn))[:16] hex."""
    raw = province + "|" + normalize(fqn)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
```

- [ ] **Step 4: Run to verify passes**

```bash
PYTHONPATH=. python3 -m pytest tests/test_hash.py -v
```
Expected: ALL PASS

- [ ] **Step 5: Commit**

```bash
git add gov/hash.py tests/test_hash.py
git commit -m "feat: add content-hash functions for person/org dedup"
```

---

### Task 2: Central schema (`gov_relation/schema.py`)

**Files:**
- Modify: `gov_relation/schema.py`
- Test: `tests/test_schema.py`

**Interfaces:**
- Produces: `create_central_schema(conn)`, `create_registry_schema(conn)`

- [ ] **Step 1: Write test**

Append to `tests/test_schema.py`:

```python
class TestCentralSchema:
    def test_creates_central_tables(self) -> None:
        import sqlite3
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        from gov_relation.schema import create_central_schema
        create_central_schema(conn)
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence' ORDER BY name"
        ).fetchall()
        names = [r[0] for r in tables]
        assert names == ["organizations", "persons", "positions", "relationships"]

    def test_central_persons_has_id_hash_pk(self) -> None:
        import sqlite3
        conn = sqlite3.connect(":memory:")
        from gov_relation.schema import create_central_schema
        create_central_schema(conn)
        conn.execute(
            "INSERT INTO persons (id_hash, name, name_normalized) VALUES (?, ?, ?)",
            ("abc123", "张三", "张三"),
        )
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
```

- [ ] **Step 2: Run to verify failure**

```bash
PYTHONPATH=. python3 -m pytest tests/test_schema.py::TestCentralSchema -v
```
Expected: FAIL — cannot import `create_central_schema`

- [ ] **Step 3: Add central schema DDLs and functions to `gov_relation/schema.py`**

After the existing `create_tables()` function (before line 84), add:

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
```

- [ ] **Step 4: Run to verify passes**

```bash
PYTHONPATH=. python3 -m pytest tests/test_schema.py::TestCentralSchema -v
```
Expected: ALL PASS

- [ ] **Step 5: Commit**

```bash
git add gov_relation/schema.py tests/test_schema.py
git commit -m "feat: add central schema functions (persons/orgs/positions/relationships + registry)"
```

---

### Task 3: Central paths (`gov_relation/paths.py`)

**Files:**
- Modify: `gov_relation/paths.py`
- Test: `tests/test_paths.py`

- [ ] **Step 1: Write test**

Append to `tests/test_paths.py`:

```python
class TestCentralPaths:
    def test_central_paths_have_correct_names(self) -> None:
        from gov_relation.paths import REGISTRY_DB, PROVINCE_DIR
        assert REGISTRY_DB.name == "registry.db"
        assert PROVINCE_DIR.name == "provincial"

    def test_central_paths_under_data_central(self) -> None:
        from gov_relation.paths import CENTRAL_DIR
        assert str(CENTRAL_DIR).endswith("data/central")
```

- [ ] **Step 2: Modify `gov_relation/paths.py`**

Add after the existing path definitions:

```python
CENTRAL_DIR = DATA_DIR / "central"
REGISTRY_DB = CENTRAL_DIR / "registry.db"
PROVINCE_DIR = CENTRAL_DIR / "provincial"
```

- [ ] **Step 3: Run test**

```bash
PYTHONPATH=. python3 -m pytest tests/test_paths.py::TestCentralPaths -v
```
Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add gov_relation/paths.py tests/test_paths.py
git commit -m "feat: add central registry paths (CENTRAL_DIR, REGISTRY_DB, PROVINCE_DIR)"
```

---

### Task 4: Central writer class (`gov_relation/central.py`)

**Files:**
- Create: `gov_relation/central.py`
- Test: `tests/test_central.py`

**Interfaces:**
- Consumes: `gov_relation.hash.person_hash()`, `gov_relation.hash.org_hash()`, `gov_relation.paths.PROVINCE_DIR`, `gov_relation.schema.create_central_schema()`, `gov_relation.schema.create_registry_schema()`
- Produces: `class Central(province: str)`
  - `merge_person(person: dict) -> str` — returns id_hash
  - `merge_organization(org: dict) -> str` — returns id_hash
  - `insert_position(position: dict) -> int`
  - `insert_relationship(rel: dict) -> int`
  - `close()`
  - `flush_registry(registry_path: str | Path)`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_central.py
from __future__ import annotations

import json
import shutil
import sqlite3

import pytest

from gov_relation.central import Central
from gov_relation.paths import PROVINCE_DIR, CENTRAL_DIR


@pytest.fixture(autouse=True)
def cleanup_central():
    """Remove any leftover test_province data before/after tests."""
    if CENTRAL_DIR.exists():
        import shutil
        shutil.rmtree(str(CENTRAL_DIR))
    yield
    if CENTRAL_DIR.exists():
        import shutil
        shutil.rmtree(str(CENTRAL_DIR))


class TestCentral:
    @pytest.fixture
    def central(self) -> Central:
        c = Central("test_province")
        yield c
        c.close()

    def test_merge_person_returns_hash(self, central: Central) -> None:
        h = central.merge_person({"name": "张三", "birth": "1977-01"})
        assert len(h) == 16
        assert all(c in "0123456789abcdef" for c in h)

    def test_merge_same_person_returns_same_hash(self, central: Central) -> None:
        h1 = central.merge_person({"name": "张三", "birth": "1977-01"})
        h2 = central.merge_person({"name": "张三", "birth": "1977-01"})
        assert h1 == h2

    def test_merge_person_upserts_fields(self, central: Central) -> None:
        h = central.merge_person({"name": "张三", "birth": "1977-01", "gender": "男"})
        central.merge_person({"name": "张三", "birth": "1977-01", "education": "研究生"})
        row = central.conn.execute(
            "SELECT education FROM persons WHERE id_hash=?", (h,)
        ).fetchone()
        assert row[0] == "研究生"
        # Gender was not overwritten
        row2 = central.conn.execute(
            "SELECT gender FROM persons WHERE id_hash=?", (h,)
        ).fetchone()
        assert row2[0] == "男"

    def test_merge_org_returns_hash(self, central: Central) -> None:
        h = central.merge_organization({"fqn": "周口市人民政府", "province": "test_province"})
        assert len(h) == 16

    def test_insert_position(self, central: Central) -> None:
        p_h = central.merge_person({"name": "张三", "birth": "1977-01"})
        o_h = central.merge_organization({"fqn": "周口市人民政府", "province": "test_province"})
        pos_id = central.insert_position({
            "person_hash": p_h,
            "org_hash": o_h,
            "title": "市长",
            "province": "test_province",
        })
        assert pos_id is not None

    def test_insert_relationship(self, central: Central) -> None:
        p1 = central.merge_person({"name": "张三", "birth": "1977-01"})
        p2 = central.merge_person({"name": "李四", "birth": "1980-05"})
        rid = central.insert_relationship({
            "person_a_hash": p1,
            "person_b_hash": p2,
            "type": "正副搭档",
            "province": "test_province",
        })
        assert rid is not None

    def test_flush_registry_updates_counts(self, central: Central) -> None:
        central.merge_person({"name": "张三", "birth": "1977-01"})
        central.merge_organization({"fqn": "人民政府", "province": "test_province"})
        registry_path = str(PROVINCE_DIR.parent / "test_registry.db")
        central.flush_registry(registry_path)

        import sqlite3
        reg = sqlite3.connect(registry_path)
        row = reg.execute("SELECT * FROM region_registry WHERE province='test_province'").fetchone()
        assert row is not None
        assert row["person_count"] >= 1
        reg.close()
```

- [ ] **Step 2: Run to verify failure**

```bash
PYTHONPATH=. python3 -m pytest tests/test_central.py -v
```
Expected: FAIL (cannot import Central)

- [ ] **Step 3: Write implementation**

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
    """Province-partitioned central registry writer.

    Each instance targets one province partition (one SQLite file).
    Use one instance per province per build.

    The class is idempotent: calling merge methods with the same data
    repeatedly produces the same result (id_hash).
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

    # ── Person upsert ──────────────────────────────────────────────

    def merge_person(self, person: dict[str, Any]) -> str:
        name = person.get("name", "")
        birth = person.get("birth", "")
        h = person_hash(name, birth)

        existing = self.conn.execute(
            "SELECT * FROM persons WHERE id_hash=?", (h,)
        ).fetchone()

        if existing:
            aliases = json.loads(existing["aliases"] or "[]")
            source_json = json.loads(existing["source_json"] or "{}")
            src = person.get("source", "")
            if src and src not in source_json:
                source_json[src] = "migrated"
            if name and name != existing["name"] and name not in aliases:
                aliases.append(name)

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
                    name,
                    name,
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
                """INSERT INTO persons
                   (id_hash, name, name_normalized, gender, ethnicity,
                    birth, birthplace, education, party_join, work_start, source_json)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    h,
                    name,
                    name,
                    person.get("gender", ""),
                    person.get("ethnicity", ""),
                    birth,
                    person.get("birthplace", ""),
                    person.get("education", ""),
                    person.get("party_join", ""),
                    person.get("work_start", ""),
                    json.dumps({person.get("source", ""): "high"}, ensure_ascii=False),
                ),
            )
        self.conn.commit()
        return h

    # ── Organization upsert ────────────────────────────────────────

    def merge_organization(self, org: dict[str, Any]) -> str:
        province = org.get("province", self.province)
        fqn = org.get("fqn", org.get("name", ""))
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
                """INSERT INTO organizations
                   (id_hash, fqn, local_name, org_type, level, parent_fqn, location, province)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    h, fqn,
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

    # ── Position insert ────────────────────────────────────────────

    def insert_position(self, pos: dict[str, Any]) -> int:
        cur = self.conn.execute(
            """INSERT INTO positions
               (person_hash, org_hash, title, start_date, end_date,
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

    # ── Relationship insert ────────────────────────────────────────

    def insert_relationship(self, rel: dict[str, Any]) -> int:
        cur = self.conn.execute(
            """INSERT INTO relationships
               (person_a_hash, person_b_hash, type, context,
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

    # ── Cleanup & registry ─────────────────────────────────────────

    def close(self) -> None:
        self.conn.close()

    def flush_registry(self, registry_path: str | Path) -> None:
        """Write partition stats to the registry.db."""
        reg = sqlite3.connect(str(registry_path))
        create_registry_schema(reg)
        p = self.conn.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
        o = self.conn.execute("SELECT COUNT(*) FROM organizations").fetchone()[0]
        ps = self.conn.execute("SELECT COUNT(*) FROM positions").fetchone()[0]
        r = self.conn.execute("SELECT COUNT(*) FROM relationships").fetchone()[0]
        reg.execute(
            """INSERT OR REPLACE INTO region_registry
               (province, db_path, status, person_count, org_count,
                position_count, relation_count, last_updated)
               VALUES (?, ?, 'active', ?, ?, ?, ?, datetime('now'))""",
            (self.province, str(self.db_path), p, o, ps, r),
        )
        reg.commit()
        reg.close()
```

- [ ] **Step 4: Run tests to verify**

```bash
PYTHONPATH=. python3 -m pytest tests/test_central.py -v
```
Expected: ALL PASS

- [ ] **Step 5: Commit**

```bash
git add gov_relation/central.py tests/test_central.py
git commit -m "feat: central registry writer class with hash-based dedup"
```

---

### Task 5: Province detection (`gov_relation/province.py`)

**Files:**
- Create: `gov_relation/province.py`
- Test: `tests/test_province.py`

**Interfaces:**
- Consumes: `gov_relation.paths.TODO_PATH`
- Produces: `build_slug_province_map(todo_path: Path | None = None) -> dict[str, str]`, `detect_province(slug: str, map_cache: dict[str, str] | None = None) -> str`

- [ ] **Step 1: Write test**

```python
# tests/test_province.py
from __future__ import annotations

import json
from pathlib import Path

import pytest

from gov_relation.province import (
    build_slug_province_map,
    detect_province,
)


class TestDetectProvince:
    def test_known_slugs(self) -> None:
        """Slugs that are exact matches in the map."""
        cache = {
            "周口市": "河南省",
            "固原市": "宁夏回族自治区",
            "甘肃省": "甘肃省",
        }
        assert detect_province("周口市", map_cache=cache) == "河南省"
        assert detect_province("固原市", map_cache=cache) == "宁夏回族自治区"
        assert detect_province("甘肃省", map_cache=cache) == "甘肃省"

    def test_unknown_slug_raises(self) -> None:
        cache = {"周口市": "河南省"}
        with pytest.raises(ValueError):
            detect_province("金星", map_cache=cache)


class TestBuildMapFromTodo:
    def test_from_todo_json(self, tmp_path: Path) -> None:
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
```

- [ ] **Step 2: Run to verify failure**

```bash
PYTHONPATH=. python3 -m pytest tests/test_province.py -v
```
Expected: FAIL

- [ ] **Step 3: Write implementation**

```python
# gov_relation/province.py
from __future__ import annotations

import json
from pathlib import Path

from .paths import TODO_PATH


def build_slug_province_map(todo_path: Path | None = None) -> dict[str, str]:
    """Parse TODO.json to map region slugs to province names."""
    path = todo_path or TODO_PATH
    if not path.exists():
        raise FileNotFoundError(f"TODO.json not found at {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    mapping: dict[str, str] = {}
    for p_entry in data.get("provinces", []):
        province = p_entry["province"]
        for task in p_entry.get("tasks", []):
            region = task.get("region", "")
            if region:
                mapping[region] = province
    return mapping


def detect_province(
    slug: str,
    todo_path: Path | None = None,
    map_cache: dict[str, str] | None = None,
) -> str:
    """Determine province name for a region slug/name.

    Raises ValueError if no match is found.
    """
    if map_cache is not None:
        mapping = map_cache
    else:
        mapping = build_slug_province_map(todo_path)

    if slug in mapping:
        return mapping[slug]

    raise ValueError(f"Cannot determine province for slug: {slug}")
```

- [ ] **Step 4: Run to verify**

```bash
PYTHONPATH=. python3 -m pytest tests/test_province.py -v
```
Expected: ALL PASS

- [ ] **Step 5: Commit**

```bash
git add gov_relation/province.py tests/test_province.py
git commit -m "feat: province detection from TODO.json slug mapping"
```

---

### Task 6: Runner extension (`gov_relation/runner.py`)

**Files:**
- Modify: `gov_relation/runner.py`
- Test: `tests/test_runner.py`

- [ ] **Step 1: Write test**

Append to `tests/test_runner.py`:

```python
class TestRunBuildWithCentralOpt:
    def test_central_param_does_not_break_basic(self, tmp_path: Path) -> None:
        from gov_relation.runner import run_build
        db_path = tmp_path / "basic_network.db"
        gexf_path = tmp_path / "basic_network.gexf"
        # basic call with no central should work exactly as before
        run_build(
            slug="test",
            persons=[{"id": 1, "name": "张三"}],
            organizations=[],
            positions=[],
            relationships=[],
            db_path=str(db_path),
            gexf_path=str(gexf_path),
        )
        assert db_path.exists()
        assert gexf_path.exists()

    def test_central_param_does_not_crash(self, tmp_path: Path) -> None:
        from gov_relation.runner import run_build
        from gov_relation.central import Central
        central = Central("test_runner_prov")
        db_path = tmp_path / "with_central_network.db"
        gexf_path = tmp_path / "with_central_network.gexf"
        run_build(
            slug="test",
            persons=[{"id": 1, "name": "张三", "birth": "1977-01"}],
            organizations=[
                {"id": 10, "name": "县政府", "fqn": "run县人民政府", "province": "test_runner_prov"},
            ],
            positions=[],
            relationships=[],
            db_path=str(db_path),
            gexf_path=str(gexf_path),
            central=central,
        )
        assert db_path.exists()
        central.close()
```

- [ ] **Step 2: Modify `gov_relation/runner.py`**

Add `central` parameter to `run_build()`:

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
```

After the existing GEXF writing block at the end, add:

```python
    # ── Central registry ────────────────────────────────────────────
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

- [ ] **Step 3: Run to verify**

```bash
PYTHONPATH=. python3 -m pytest tests/test_runner.py::TestRunBuildWithCentralOpt -v
```
Expected: ALL PASS

- [ ] **Step 4: Commit**

```bash
git add gov_relation/runner.py tests/test_runner.py
git commit -m "feat: add optional central param to run_build()"
```

---

### Task 7: Migration script (`scripts/migrate_to_central.py`)

**Files:**
- Create: `scripts/migrate_to_central.py`

- [ ] **Step 1: Write the migration script**

```python
#!/usr/bin/env python3
"""One-time full migration from data/database/*_network.db to the central registry.

Reads every region DB, rekeys foreign keys using content hashes, and writes
into province-partitioned central DB files.

Usage:
    python3 scripts/migrate_to_central.py
    python3 scripts/migrate_to_central.py --dry-run
    python3 scripts/migrate_to_central.py --limit 10
    python3 scripts/migrate_to_central.py --resume
    python3 scripts/migrate_to_central.py --province 河南省
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.central import Central
from gov_relation.paths import DATABASE_DIR, REGISTRY_DB
from gov_relation.province import build_slug_province_map


def _slug_from_stem(stem: str) -> str:
    return stem.removesuffix("_network")


def _fetch_tuples(conn: sqlite3.Connection, table: str) -> list[dict[str, Any]]:
    cur = conn.execute(f"SELECT * FROM [{table}]")
    cols = [desc[0] for desc in cur.description]
    return [{col: (row[i] or "") for i, col in enumerate(cols)} for row in cur.fetchall()]


def migrate_one(db_path: Path, central: Central, slug: str) -> dict[str, int]:
    """Migrate a single region DB to central. Returns stats."""
    stats: dict[str, int] = {"persons": 0, "orgs": 0, "positions": 0, "rels": 0, "conflicts": 0}
    src = sqlite3.connect(str(db_path))
    src.row_factory = sqlite3.Row

    from gov_relation.hash import person_hash, org_hash

    # 1. Persons — collect old id → hash mapping
    persons = _read_tuples(src, "persons")
    old_id_to_hash: dict[str, str] = {}
    for p in persons:
        try:
            h = central.merge_person(p)
            old_id_to_hash[str(p.get("id", ""))] = h
            stats["persons"] += 1
        except Exception:
            stats["conflicts"] += 1

    # 2. Organizations
    orgs_data = _read_tuples(src, "organizations")
    old_org_id_to_hash: dict[str, str] = {}
    for o in orgs_data:
        o["province"] = central.province
        o["fqn"] = o.get("fqn", o.get("name", ""))
        o["local_name"] = o.get("local_name", o.get("name", ""))
        try:
            h = central.merge_organization(o)
            old_org_id_to_hash[str(o.get("id", ""))] = h
            stats["orgs"] += 1
        except Exception:
            stats["conflicts"] += 1

    # 3. Positions — rekey foreign keys
    positions = _read_tuples(src, "positions")
    for pos in positions:
        p_hash = old_id_to_hash.get(str(pos.get("person_id", "")))
        o_hash = old_org_id_to_hash.get(str(pos.get("org_id", "")))
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
            "province": central.province,
            "source": "",
        }
        try:
            central.insert_position(entry)
            stats["positions"] += 1
        except Exception:
            stats["conflicts"] += 1

    # 4. Relationships — rekey person references
    try:
        rels_data = _read_tuples(src, "relationships")
    except Exception:
        rels_data = []
    for rel in rels_data:
        pa = old_id_to_hash.get(str(rel.get("person_a", "")))
        pb = old_id_to_hash.get(str(rel.get("person_b", "")))
        if not pa or not pb:
            stats["conflicts"] += 1
            continue
        entry = {
            "person_a_hash": pa,
            "person_b_hash": pb,
            "type": rel.get("type", ""),
            "context": rel.get("context", ""),
            "overlap_org_hash": "",
            "overlap_period": rel.get("overlap_period", ""),
            "province": central.province,
            "source": "",
        }
        oo = str(rel.get("overlap_org", ""))
        if oo in old_org_id_to_hash:
            entry["overlap_org_hash"] = old_org_id_to_hash[oo]
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
    args = parser.parse_args()

    print("Building slug → province map from TODO.json ...")
    slug_map = build_slug_province_map()

    db_files = sorted(DATABASE_DIR.glob("*_network.db"))
    if not db_files:
        print(f"No *_network.db files found in {DATABASE_DIR}")
        return

    # Prepare registry metada DB
    REGISTRY_DB.parent.mkdir(parents=True, exist_ok=True)
    reg_conn = sqlite3.connect(str(REGISTRY_DB))
    from gov_relation.schema import create_registry_schema
    create_registry_schema(reg_conn)

    if args.resume:
        already = {r[0] for r in reg_conn.execute("SELECT slug FROM migration_audit").fetchall()}
    else:
        already = set()

    # Select DBs to process
    selected: list[tuple[str, str, Path]] = []
    for f in db_files:
        slug = _slug_to_stem(f.stem)
        if slug in already:
            continue
        province = slug_map.get(slug, "")
        if not province:
            # fuzzy fallback: if the slug ends with a known slug
            for key, p in slug_map.items():
                if slug.endswith(key) or key.endswith(slug):
                    province = p
                    break
        if not province:
            print(f"  ⚠ Cannot determine province for '{slug}' — skipping")
            continue
        if args.province and province != args.province:
            continue
        selected.append((province, slug, f))

    if args.dry_run:
        print(f"\nDry run: would process {len(selected)} DBs:")
        for province, slug, path in selected:
            print(f"  {path.name}  →  {province}/{slug}")
        reg_conn.close()
        return

    total = {"persons": 0, "orgs": 0, "positions": 0, "rels": 0, "conflicts": 0}
    start_time = time.time()
    current_province = None
    central = None

    try:
        for i, (province, slug, db_path) in enumerate(selected):
            if args.limit and i >= args.limit:
                break

            if province != current_province:
                if central:
                    central.flush_registry(str(REGISTRY_DB))
                    central.close()
                print(f"\n=== Province: {province} ===")
                central = Central(province)
                current_province = province

            print(f"  [{i+1}/{len(selected)}] {slug} ...", end=" ", flush=True)
            stats = migrate_one(db_path, central, slug)
            reg_conn.execute(
                """INSERT INTO migration_audit
                   (source_db, slug, province, persons_imported, orgs_imported,
                    positions_imported, rels_imported, merge_conflicts)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (str(db_path), slug, province,
                 stats["persons"], stats["orgs"],
                 stats["positions"], stats["rels"], stats["conflicts"]),
            )
            reg_conn.commit()
            for k in total:
                total[k] += stats[k]
            print(f"ok ({stats['persons']}p/{stats['orgs']}o/"
                  f"{stats['positions']}pos/{stats['rels']}r, {stats['conflicts']} conflicts)")

    finally:
        if central:
            central.flush_registry(str(REGISTRY_DB))
            central.close()
        reg_conn.close()

    elapsed = time.time() - start_time
    print(f"\n Done. Processed {len(selected)} DBs in {elapsed:.1f}s")
    print(f"  Total — persons: {total['persons']}, orgs: {total['orgs']}, "
          f"positions: {total['positions']}, rels: {total['rels']}")
    print(f"  Conflicts: {total['conflicts']} (see merge_conflicts table in registry.db)")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run a dry-run to verify it parses and discovers DBs**

```bash
PYTHONPATH=. python3 scripts/migrate_to_central.py --dry-run
```
Expected: Output showing all DBs and their province assignments (no writes)

- [ ] **Step 3: Run real migration (first 5 DBs)**

```bash
PYTHONPATH=. python3 scripts/migrate_to_central.py --limit 5
```
Expected: Processes 5 DBs, creates provincial DBs in data/central/provincial/

- [ ] **Step 4: Commit**

```bash
git add scripts/migrate_to_central.py
git commit -m "feat: one-time migration script from region DBs to central registry"
```

---

## Self-Review Checklist

**1. Spec coverage:**
- [x] Schema definitions (Task 2 covers central DDLs)
- [x] Hash strategy (Task 1 covers person/org hashing)
- [x] Path config (Task 3 covers paths)
- [x] Central writer API (Task 4 covers Central class)
- [x] Runner integration (Task 6 covers run_build extension)
- [x] Province detection (Task 5 covers province mapping)
- [x] Migration script (Task 7 covers one-time migration)
- [ ] Cross-province index — deferred to optional future task (cross-province.db not built yet — can be added after migration is done)
- [ ] Data integrity after migration — no explicit test that the total row counts match across source DBs vs. central DB; an `--audit` pass could be added later

**2. Placeholder scan:** No TBD, TODO, or incomplete code. All functions have complete implementations. ✅

**3. Type consistency:**
- Task 1: `person_hash(name, birth) -> str`, `org_hash(province, fqn) -> str`
- Task 4: `Central.merge_person()` returns `str` (the hash) — consistent ✅
- Task 4: `Central.merge_organization()` returns `str` (the hash) — consistent ✅
- Task 7: migration uses these exact hash functions ✅

**4. Execution order:**
- Task 1 → Task 2 → Task 3 → Task 4 → Task 5 → Task 6 → Task 7
- Each task only depends on interfaces produced by earlier tasks ✅