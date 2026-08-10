# Phase 2: Schema 升级 + govdb.py 切换

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 升级 platform schema 到 v3，govdb.py build 切换到使用 InsertFactory 写新 schema。

**Architecture:** `gov_relation/schema.py` 新增 v3 DDL 常量（保留 v1/v2 legacy），`scripts/migrate/upgrade_schema_v2_to_v3.py` 在现有 platform DB 上执行 ALTER/新表，`scripts/govdb.py` 的 build 命令引入 InsertFactory 写新 schema。

**Spec:** `docs/superpowers/specs/2026-08-10-v3-refactor-design.md`
**Prerequisite:** Phase 1 (Foundation) 完成

## Global Constraints
- Python 3.11 stdlib only
- 保留 v2 schema 常量向后兼容
- 迁移脚本只新增表，不删除旧表
- 测试用隔离 tmp_path

---

### Task 1: 升级 gov_relation/schema.py 添加 v3 DDL 常量

**Files:**
- Modify: `gov_relation/schema.py`

**Interfaces:**
- Produces: `V3_SCHEMA_DDLS: list[str]` — all CREATE TABLE IF NOT EXISTS statements for v3

- [ ] **Step 1: 在 schema.py 末尾追加 v3 DDL 常量**

在现有的 `create_registry_schema` 函数后面追加：

```python
# ═══════════════════════════════════════════════════════════════
# V3 unified schema (2026-08-10) — 20 tables + 6 gold views
# ═══════════════════════════════════════════════════════════════

V3_JURISDICTIONS = """
CREATE TABLE IF NOT EXISTS jurisdictions (
    jurisdiction_id   TEXT PRIMARY KEY,
    parent_id         TEXT REFERENCES jurisdictions(jurisdiction_id),
    name              TEXT NOT NULL,
    normalized_name   TEXT NOT NULL,
    administrative_code TEXT NOT NULL DEFAULT '',
    level             TEXT NOT NULL DEFAULT 'unknown'
                       CHECK (level IN ('province','prefecture','county','town','unknown')),
    province_name     TEXT NOT NULL DEFAULT '',
    prefecture_name   TEXT NOT NULL DEFAULT '',
    county_name       TEXT NOT NULL DEFAULT '',
    valid_from        TEXT,
    valid_to          TEXT,
    UNIQUE (parent_id, normalized_name, level)
)"""

V3_PERSONS = """
CREATE TABLE IF NOT EXISTS persons (
    person_id       TEXT PRIMARY KEY,
    canonical_name  TEXT NOT NULL,
    normalized_name TEXT NOT NULL,
    gender          TEXT NOT NULL DEFAULT '',
    ethnicity       TEXT NOT NULL DEFAULT '',
    birth_text      TEXT NOT NULL DEFAULT '',
    birth_precision TEXT NOT NULL DEFAULT 'unknown'
                     CHECK (birth_precision IN ('day','month','year','unknown')),
    birthplace      TEXT NOT NULL DEFAULT '',
    native_place    TEXT NOT NULL DEFAULT '',
    education       TEXT NOT NULL DEFAULT '',
    party_join_text TEXT NOT NULL DEFAULT '',
    work_start_text TEXT NOT NULL DEFAULT '',
    identity_status TEXT NOT NULL DEFAULT 'unresolved'
                     CHECK (identity_status IN ('verified','probable','unresolved','merged')),
    merged_into_id  TEXT REFERENCES persons(person_id),
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
)"""

V3_PERSON_ALIASES = """
CREATE TABLE IF NOT EXISTS person_aliases (
    person_id        TEXT NOT NULL REFERENCES persons(person_id),
    alias            TEXT NOT NULL,
    normalized_alias TEXT NOT NULL,
    alias_type       TEXT NOT NULL DEFAULT 'other',
    PRIMARY KEY (person_id, normalized_alias)
)"""

V3_ORGANIZATIONS = """
CREATE TABLE IF NOT EXISTS organizations (
    organization_id        TEXT PRIMARY KEY,
    jurisdiction_id        TEXT REFERENCES jurisdictions(jurisdiction_id),
    parent_organization_id TEXT REFERENCES organizations(organization_id),
    canonical_name         TEXT NOT NULL,
    normalized_name        TEXT NOT NULL,
    organization_type      TEXT NOT NULL DEFAULT '',
    administrative_level   TEXT NOT NULL DEFAULT '',
    location_text          TEXT NOT NULL DEFAULT '',
    valid_from             TEXT,
    valid_to               TEXT,
    created_at             TEXT NOT NULL DEFAULT (datetime('now'))
)"""

V3_POSITIONS = """
CREATE TABLE IF NOT EXISTS positions (
    position_id       TEXT PRIMARY KEY,
    person_id         TEXT NOT NULL REFERENCES persons(person_id),
    organization_id   TEXT REFERENCES organizations(organization_id),
    organization_text TEXT NOT NULL DEFAULT '',
    title             TEXT NOT NULL DEFAULT '',
    title_category    TEXT NOT NULL DEFAULT '',
    rank              TEXT NOT NULL DEFAULT '',
    start_text        TEXT NOT NULL DEFAULT '',
    end_text          TEXT NOT NULL DEFAULT '',
    start_date        TEXT,
    end_date          TEXT,
    date_precision    TEXT NOT NULL DEFAULT 'unknown'
                       CHECK (date_precision IN ('day','month','year','range','unknown')),
    is_current        INTEGER NOT NULL DEFAULT 0 CHECK (is_current IN (0,1)),
    sort_order        INTEGER NOT NULL DEFAULT 0,
    confidence        TEXT NOT NULL DEFAULT 'unverified'
                       CHECK (confidence IN ('confirmed','plausible','unverified')),
    notes             TEXT NOT NULL DEFAULT ''
)"""

V3_RELATIONSHIPS = """
CREATE TABLE IF NOT EXISTS relationships (
    relationship_id          TEXT PRIMARY KEY,
    person_from_id           TEXT NOT NULL REFERENCES persons(person_id),
    person_to_id             TEXT NOT NULL REFERENCES persons(person_id),
    relationship_type        TEXT NOT NULL DEFAULT 'other',
    direction                TEXT NOT NULL DEFAULT 'undirected'
                              CHECK (direction IN ('undirected','from_to','to_from')),
    strength                 TEXT NOT NULL DEFAULT 'unknown'
                              CHECK (strength IN ('strong','medium','weak','unknown')),
    confidence               TEXT NOT NULL DEFAULT 'unverified'
                              CHECK (confidence IN ('confirmed','plausible','unverified')),
    context                  TEXT NOT NULL DEFAULT '',
    evidence_summary         TEXT NOT NULL DEFAULT '',
    overlap_organization_id  TEXT REFERENCES organizations(organization_id),
    overlap_organization_text TEXT NOT NULL DEFAULT '',
    overlap_period_text      TEXT NOT NULL DEFAULT '',
    valid_from               TEXT,
    valid_to                 TEXT,
    CHECK (person_from_id <> person_to_id)
)"""

V3_PERSON_STATUSES = """
CREATE TABLE IF NOT EXISTS person_statuses (
    status_id            TEXT PRIMARY KEY,
    person_id            TEXT NOT NULL REFERENCES persons(person_id),
    post_text            TEXT NOT NULL DEFAULT '',
    organization_text    TEXT NOT NULL DEFAULT '',
    administrative_rank  TEXT NOT NULL DEFAULT '',
    observed_at          TEXT,
    is_current_confirmed INTEGER NOT NULL DEFAULT 0 CHECK (is_current_confirmed IN (0,1)),
    confidence           TEXT NOT NULL DEFAULT 'unverified'
                          CHECK (confidence IN ('confirmed','plausible','unverified'))
)"""

V3_ENTITY_DDLS = [
    V3_JURISDICTIONS, V3_PERSONS, V3_PERSON_ALIASES, V3_ORGANIZATIONS,
    V3_POSITIONS, V3_RELATIONSHIPS, V3_PERSON_STATUSES,
]
```

暂只添加实体域 7 表（Evidence/Rights 域在 Phase 3 govdb.py 切换后按需创建）。  
完整 DDL 版在 `gov_relation/factory/schema_factory.py` 中已有。

- [ ] **Step 2: 验证 import**

Run: `python3 -c "from gov_relation.schema import V3_ENTITY_DDLS; print(f'V3 entity tables: {len(V3_ENTITY_DDLS)}')"`
Expected: `V3 entity tables: 7`

- [ ] **Step 3: Commit**

```bash
git add gov_relation/schema.py
git commit -m "refactor(schema): add V3 entity DDL constants alongside legacy v1/v2"
```

---

### Task 2: govdb.py build 切换到 InsertFactory

**Files:**
- Modify: `scripts/govdb.py`

- [ ] **Step 1: 在 build_database 函数中使用 InsertFactory + SchemaFactory**

```python
# 在 scripts/govdb.py 顶部添加 import
from gov_relation.factory.schema_factory import SchemaFactory
from gov_relation.factory.insert_factory import InsertFactory

# build_database 函数内，原来调用 importer 的逻辑改为：
# ... (原有 import_legacy_database / import_person_profile 逻辑保留)
# 新增: 写入完成后对 platform DB 用 SchemaFactory 创建 missing tables + views
```

具体实现：在 build 的最后阶段，调用 `SchemaFactory().create_all(conn)` 确保所有 v3 表存在，然后对每个导入的 legacy database 调用 InsertFactory 进行二次写入（生成 v3 格式的 persons/organizations/positions/relationships 表）。此步骤对存量数据做 normalization 但不修改已有 bronze 层数据。

**注意：** 当前 govdb.py build 已通过 platform/importer.py 写 v2 schema。此任务只是**追加** v3 表的初始化 — 不替换原有逻辑，仅确保 build 完成后 v3 表也存在。

- [ ] **Step 2: 更新 govdb.py imports**

```python
from gov_relation.factory.schema_factory import SchemaFactory
from gov_relation.factory.insert_factory import InsertFactory
```

- [ ] **Step 3: 添加到 build_database 函数末尾**

在 `build_database()` 中 `conn.commit()` 之前添加：

```python
# Ensure v3 tables exist
schema_factory = SchemaFactory()
schema_factory.create_all(conn)

# Populate v3 persons from legacy persons (if not already migrated)
v3_person_count = conn.execute("SELECT COUNT(*) FROM persons WHERE person_id LIKE 'per_%'").fetchone()[0]
if v3_person_count == 0:
    insert_factory = InsertFactory()
    for row in conn.execute("SELECT * FROM raw_records WHERE source_table='persons'"):
        # This is optional — factory mode tables will be populated by Phase 4
        pass
```

- [ ] **Step 4: 验证**

Run: `python3 -m pytest tests/test_platform.py -v --tb=short`
Expected: 现有测试通过

- [ ] **Step 5: Commit**

```bash
git add scripts/govdb.py
git commit -m "feat(govdb): integrate SchemaFactory to ensure v3 tables exist after build"
```

---

### Task 3: 写迁移脚本 upgrade_schema_v2_to_v3.py

**Files:**
- Create: `scripts/migrate/upgrade_schema_v2_to_v3.py`

- [ ] **Step 1: 实现**

```python
#!/usr/bin/env python3
"""Upgrade existing platform DB from v2 to v3 schema.

Usage:
    python3 scripts/migrate/upgrade_schema_v2_to_v3.py --database data/platform/gov_relation.db

This script is additive — it creates new v3 tables alongside existing v2 tables.
No data is deleted or altered.  Existing v2 tables remain untouched.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.platform.schema import connect
from gov_relation.factory.schema_factory import SchemaFactory


def upgrade(database: Path) -> dict:
    conn = connect(database)
    try:
        factory = SchemaFactory()

        # Check current version
        current = conn.execute(
            "SELECT value FROM schema_meta WHERE key='schema_version'"
        ).fetchone()

        if current and current[0] == "3.0.0":
            conn.close()
            return {"status": "skipped", "reason": "already v3.0.0"}

        # Create new tables
        factory.create_entity_tables(conn)
        factory.create_evidence_tables(conn)
        factory.create_rights_tables(conn)
        factory.create_meta_tables(conn)
        factory.create_views(conn)
        factory.create_indexes(conn)

        # Update version
        conn.execute(
            "INSERT OR REPLACE INTO schema_meta(key, value) VALUES('schema_version', '3.0.0')"
        )
        conn.commit()

        # Count new tables
        tables = conn.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table'"
        ).fetchone()[0]

        conn.close()
        return {
            "status": "upgraded",
            "from_version": current[0] if current else "none",
            "to_version": "3.0.0",
            "total_tables": tables,
        }
    except Exception as exc:
        try:
            conn.close()
        except Exception:
            pass
        return {"status": "failed", "error": str(exc)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--database", type=Path,
        default=REPO_ROOT / "data" / "platform" / "gov_relation.db",
    )
    args = parser.parse_args()
    import json
    result = upgrade(args.database)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] != "failed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: 测试 dry-run**

Run: `python3 scripts/migrate/upgrade_schema_v2_to_v3.py --database /tmp/test_v3_upgrade.db`
Expected: `{"status": "upgraded", ...}`

- [ ] **Step 3: Commit**

```bash
mkdir -p scripts/migrate
git add scripts/migrate/upgrade_schema_v2_to_v3.py
git commit -m "feat(migrate): add upgrade_schema_v2_to_v3.py for additive v3 migration"
```

---

## Phase 2 Completion Checklist

- [ ] `gov_relation/schema.py` 新增 V3_ENTITY_DDLS 常量
- [ ] `scripts/govdb.py` 集成 SchemaFactory
- [ ] `scripts/migrate/upgrade_schema_v2_to_v3.py` 可运行
- [ ] 全量测试通过
