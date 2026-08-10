# Phase 2: Schema 升级 + govdb.py 切换

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 升级 platform schema 到 v3，govdb.py build 切换到使用 InsertFactory 写新 schema。

**Architecture:** `gov_relation/schema.py` 新增 v3 DDL 常量（保留 v1/v2 legacy），`scripts/migrate/upgrade_schema_v2_to_v3.py` 在现有 platform DB 上执行 ALTER/新表，`scripts/govdb.py` 的 build 命令引入 InsertFactory 写新 schema。

**Spec:** `docs/superpowers/specs/2026-08-10-v3-refactor-design.md`
**Prerequisite:** Phase 1 (Foundation) 完成

## Global Constraints
- Python 3.11 stdlib only
- 保留 v2 schema 常量向后兼容
- **v2 与 v3 共享同名表（`persons`/`positions`/`organizations`/`relationships`/`jurisdictions`/`datasets`/`sources`/`evidence_links`/`entity_provenance`/`quality_issues`/`resolution_candidates`/`raw_records`/`person_aliases`/`person_statuses`/`schema_meta` 等 21 表全部同名）**。因此：
  - `CREATE TABLE IF NOT EXISTS` 在已构建的 v2 DB 上是**静默 no-op** —— 不能用来"追加 v3 表"（评审 C1）。
  - 真实升级方式 = **对已存在表执行 `ALTER TABLE ADD COLUMN`（v3 增量列），对不存在表 `CREATE`**（见 Task 3）。
  - 迁移脚本只新增列/新增表，**不删除、不改名旧列**（`category`、`commercial_use_allowed` 保留，新 v3 列并行存在）。
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
# V3 unified schema (2026-08-10) — 21 tables + 6 gold views
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

> **关于同名表（评审 C1）：** v2 平台 DDL（`gov_relation/platform/schema.py`）与 v3 的实体域**表名完全相同**，仅列级增量（`persons` 增 `education`/`merged_into_id`；`positions` 用 `category` → v3 用 `title_category` + `sort_order`；`datasets`/`sources` 用 `commercial_use_allowed` → v3 用 `commercial_use`）。因此：
> - 这些 `V3_*` 常量用于**全新 DB**（factory 创建省库 / 重灌 platform）时直接建出 v3 形状；
> - 对**已存在的 v2 platform DB**，不能靠 `CREATE TABLE IF NOT EXISTS` 升级（同名表 no-op），必须走 Task 3 的 ALTER 迁移。
> - Evidence/Rights 域 DDL 在 `gov_relation/factory/schema_factory.py`，`V3_*` 常量只覆盖实体域 7 表（与本文件生成脚本保持一致）。

- [ ] **Step 2: 验证 import**

Run: `python3 -c "from gov_relation.schema import V3_ENTITY_DDLS; print(f'V3 entity tables: {len(V3_ENTITY_DDLS)}')"`
Expected: `V3 entity tables: 7`

- [ ] **Step 3: Commit**

```bash
git add gov_relation/schema.py
git commit -m "refactor(schema): add V3 entity DDL constants alongside legacy v1/v2"
```

---

### Task 2: govdb.py build 接入 v3（不改逻辑）

**Files:**
- Modify: `scripts/govdb.py`

**架构修正（评审 C1/F2）：** 原设计让 `build_database` 调用 `SchemaFactory().create_all(conn)`，
这在已存在的 v2 平台库上是**错的**：
1. `CREATE TABLE IF NOT EXISTS` 对同名 v2 表静默 no-op，v3 形状不会落地；
2. `create_indexes` 的 `idx_positions_person_time ON positions(..., sort_order, ...)` 在 v2 库（无 `sort_order`）上直接 `OperationalError`，导致 `build` 崩溃；
3. `person_id LIKE 'per_%'` 计数判断 "是否已迁移" 无效 —— 现库中 47,727 个所有人已都是 `per_<hex>` 前缀。

**正确的做法：** platform 库的 v2→v3 升级**唯一入口是 Task 3 的迁移脚本**（先跑，ALTER 加列）。
`govdb.py build` 自身的职责保持不变（platform importer 写 bronze/silver），仅在 build 前调用
`gov_relation.platform.schema.create_schema(conn)` 做版本校验与幂等 DDL——由于 Step 0 已把
`SCHEMA_VERSION` 升到 `3.0.0` 且 `ADDITIVE_SCHEMA_UPGRADES` 含 `2.1.0`，未迁移旧库会被平滑处理、
已迁移库直接通过。**不要**在 build 里创建 v3 factory 表。

- [ ] **Step 1: 在 build_database 开头加 schema 版本门禁（非 create_all）**

```python
# scripts/govdb.py build_database 内，conn 建立后、写数据前：
from gov_relation.platform.schema import create_schema
create_schema(conn)          # 版本校验 + 幂等 DDL；比 create_all 更安全
```

> 若确需 factory 表（省库路径），走 `RegionResearchFactory.generate_gexf()`（见 Phase 1 Task 7），
> 它在新 **province DB** 上调用 `SchemaFactory().create_all()`，不存在与 v2 同名表冲突。

- [ ] **Step 2: 验证**

Run: `python3 -m pytest tests/test_platform.py -v --tb=short`
Expected: 现有测试通过（`create_schema` 幂等，无 `sort_order` 崩溃）

- [ ] **Step 3: Commit**

```bash
git add scripts/govdb.py
git commit -m "feat(govdb): run create_schema version gate before build; drop v3 create_all in build

v2/v3 share table names; SchemaFactory.create_all in build no-ops and
crashes on idx_positions_person_time (no sort_order in v2). Migration
is owned by scripts/migrate/upgrade_schema_v2_to_v3.py; build only gates
schema version via platform.create_schema."
```

---

### Task 3: 写迁移脚本 upgrade_schema_v2_to_v3.py

**Files:**
- Create: `scripts/migrate/upgrade_schema_v2_to_v3.py`

- [ ] **Step 0（前置）: 更新 platform/schema.py 版本容限**

在迁移脚本运行前先改 `gov_relation/platform/schema.py`（评审 F4）：
`SCHEMA_VERSION = "2.1.0"` → `SCHEMA_VERSION = "3.0.0"`，且
`ADDITIVE_SCHEMA_UPGRADES = {"2.0.0", "2.1.0"}`。

原因：迁移完成后 DB 里 `schema_version='3.0.0'`。若不更新这两个常量，后续任何
`create_schema()`（govdb resolve / rights-apply 等都会调）都会因
`Database schema 3.0.0 is incompatible with code schema 2.1.0` 抛 `RuntimeError`。
把 2.1.0 加入 ADDITIVE 集合允许未迁移的旧库也能被 create_schema 平滑处理。

```python
# gov_relation/platform/schema.py 顶部
SCHEMA_VERSION = "3.0.0"
ADDITIVE_SCHEMA_UPGRADES = {"2.0.0", "2.1.0"}
```

同时把 `gov_relation/platform/schema.py` 的 `DDL` 里那 4 处列级增量对齐为 v3：
`persons` 加 `education`、`merged_into_id`；`positions` 加 `title_category`、`sort_order`；
`datasets`/`sources` 加 `commercial_use INTEGER NOT NULL DEFAULT 0`（保留 `commercial_use_allowed`）。
（新装 DB 用 `create_schema` 直接建出 v3 形状；已有 DB 走本脚本 ALTER。）

- [ ] **Step 1: 实现**

```python
#!/usr/bin/env python3
"""Upgrade existing platform DB from v2 to v3 schema.

Usage:
    python3 scripts/migrate/upgrade_schema_v2_to_v3.py --database data/platform/gov_relation.db [--dry-run]

This migration is additive and column-aware:
- v2 and v3 share the SAME table names (21 tables). For tables that already
  exist, we ALTER TABLE ADD COLUMN the v3 delta columns — CREATE TABLE IF NOT
  EXISTS would silently no-op and never install the v3 shape (评审 C1).
- v2-only columns (category, commercial_use_allowed) are kept; v3 members
  used by the factory are added alongside and backfilled.
- No column is dropped or renamed. Existing v2 views are left untouched.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.platform.schema import connect

# 仅对"已存在的同名表"需要 ALTER 的 v3 增量列
ALTER_COLUMNS: dict[str, list[str]] = {
    "persons": [
        "education TEXT NOT NULL DEFAULT ''",
        "merged_into_id TEXT REFERENCES persons(person_id)",
    ],
    "positions": [
        "title_category TEXT NOT NULL DEFAULT ''",
        "sort_order INTEGER NOT NULL DEFAULT 0",
    ],
    "datasets": [
        "commercial_use INTEGER NOT NULL DEFAULT 0 CHECK(commercial_use IN (0, 1))",
    ],
    "sources": [
        "commercial_use INTEGER NOT NULL DEFAULT 0 CHECK(commercial_use IN (0, 1))",
    ],
}

# v3 列 → 可回填其值对应的 v2 旧列（保留旧列）
BACKFILL: dict[str, tuple[str, str]] = {
    # (table, v2_column) -> v3_column
    "positions": ("category", "title_category"),
    "datasets": ("commercial_use_allowed", "commercial_use"),
    "sources": ("commercial_use_allowed", "commercial_use"),
}

# v2 平台已存在全部 21 表；此集合保证极端情况（缺表）也补建
# 实体域缺表场景：schema_factory 的 create_entity_tables(conn) 按需补齐。
def _ensure_entity_tables(conn) -> None:
    from gov_relation.factory.schema_factory import SchemaFactory
    SchemaFactory().create_entity_tables(conn)


def _columns(conn, table: str) -> set[str]:
    return {row[1] for row in conn.execute(f"PRAGMA table_info('{table}')")}


def upgrade(database: Path, *, dry_run: bool = False) -> dict:
    conn = connect(database)
    results: dict[str, list[str]] = {"altered": [], "created": [], "backfilled": []}
    try:
        current = conn.execute(
            "SELECT value FROM schema_meta WHERE key='schema_version'"
        ).fetchone()
        current_ver = current[0] if current else None
        if current_ver == "3.0.0":
            return {"status": "skipped", "reason": "already v3.0.0"}

        # 1) 对已存在的表做列级 ALTER
        for table, alts in ALTER_COLUMNS.items():
            if table not in _tables(conn):
                continue
            existing = _columns(conn, table)
            for col_def in alts:
                col_name = col_def.split(" ", 2)[1]
                if col_name in existing:
                    continue
                if not dry_run:
                    conn.execute(f"ALTER TABLE {table} {col_def}")
                    results["altered"].append(f"{table}.{col_name}")
                else:
                    results["altered"].append(f"(dry) {table}.{col_name}")

        # 2) 回填：v3 列从 v2 旧列拷贝
        for table, (old_col, new_col) in BACKFILL.items():
            if table in _tables(conn) and old_col in _columns(conn, table) and new_col in _columns(conn, table):
                if not dry_run:
                    conn.execute(
                        f"UPDATE {table} SET {new_col} = {old_col} WHERE {new_col} = 0 AND {old_col} != 0"
                    )
                    results["backfilled"].append(f"{table}.{new_col} <- {table}.{old_col}")
                else:
                    results["backfilled"].append(f"(dry) {table}.{new_col} <- {table}.{old_col}")

        # 3) 用 factory 补齐缺失表/索引/视图（仅对确实缺失的表生效）
        if not dry_run:
            from gov_relation.factory.schema_factory import SchemaFactory
            present = set(_tables(conn))
            factory = SchemaFactory()
            prior = present
            _ensure_entity_tables(conn)          # 先建实体域（FK 依赖）
            factory.create_evidence_tables(conn)
            factory.create_rights_tables(conn)
            factory.create_meta_tables(conn)
            factory.create_views(conn)
            factory.create_indexes(conn)
            after = set(_tables(conn))
            for t in sorted(after - prior):
                results["created"].append(t)

        # 4) 版本戳
        if not dry_run:
            conn.execute(
                "INSERT OR REPLACE INTO schema_meta(key, value) VALUES('schema_version', '3.0.0')"
            )
            conn.commit()
            conn.close()

        return {
            "status": "dry-run" if dry_run else "upgraded",
            "from_version": current_ver or "none",
            "to_version": "3.0.0",
            **results,
        }
    except Exception as exc:
        try:
            conn.close()
        except Exception:
            pass
        return {"status": "failed", "error": str(exc)}


def _tables(conn) -> set[str]:
    return {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--database", type=Path,
        default=REPO_ROOT / "data" / "platform" / "gov_relation.db",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    import json
    result = upgrade(args.database, dry_run=args.dry_run)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] != "failed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

> **视图决策（评审 F7）：** v2 已占用 `gold_current_positions`（position 版定义）等视图名，且每次 `create_schema()` 会 DROP 重建。迁移**不动已有视图**（保持 v2 定义），`create_views()` 的 `IF NOT EXISTS` 对其 no-op。若日后要 v3 的 person_statuses 版视图，需额外显式 `DROP VIEW IF EXISTS gold_current_positions` 后再建——放到独立迁移任务，不并入本次增量升级。

> **必须先跑 `--dry-run`** 确认预期 ALTER 列表非空；真实执行后再次运行返回 `skipped`。

- [ ] **Step 2: 测试 dry-run（对真实 v2 库预览）**

Run: `python3 scripts/migrate/upgrade_schema_v2_to_v3.py --database data/platform/gov_relation.db --dry-run`
Expected: `{"status": "dry-run", "from_version": "2.1.0", "altered": ["persons.education", "persons.merged_into_id", "positions.title_category", "positions.sort_order", "datasets.commercial_use", "sources.commercial_use"], "backfilled": [...]}` —— 列出实际会 ALTER/回填的列，**不落库**。

> 验证点：`altered` 应包含 `persons.education`、`positions.sort_order`（评审 F2/F3 的崩点）—— 这正是 v2 缺、v3 必须补的列。

- [ ] **Step 2b: dry-run 后用测试库验证目标形状**

```bash
cp data/database/gov_relation.db /tmp/v3_upgrade_test.db 2>/dev/null \
  || cp /tmp/fixture_v2.db /tmp/v3_upgrade_test.db
python3 scripts/migrate/upgrade_schema_v2_to_v3.py --database /tmp/v3_upgrade_test.db
python3 - <<'EOF'
import sqlite3
c = sqlite3.connect('/tmp/v3_upgrade_test.db')
cols_ok = {r[1] for r in c.execute("PRAGMA table_info(persons)")}
assert 'education' in cols_ok and 'merged_into_id' in cols_ok, cols_ok
pos = {r[1] for r in c.execute("PRAGMA table_info(positions)")}
assert 'sort_order' in pos and 'title_category' in pos, pos
assert c.execute("SELECT value FROM schema_meta WHERE key='schema_version'").fetchone()[0] == '3.0.0'
print("migration verified on copy")
EOF
```

- [ ] **Step 3: 真实执行**

Run: `python3 scripts/migrate/upgrade_schema_v2_to_v3.py --database data/database/gov_relation.db`
Expected: `{"status": "upgraded", ...}`；再跑一次 → `{"status": "skipped", "reason": "already v3.0.0"}`

> **执行前务必先运行 Step 0（platform/schema.py 版本容限）**，否则升级后 `govdb.py resolve` / `rights-apply` 会因版本不兼容抛 `RuntimeError`。

- [ ] **Step 4: Commit**

```bash
mkdir -p scripts/migrate
git add scripts/migrate/upgrade_schema_v2_to_v3.py gov_relation/platform/schema.py
git commit -m "feat(migrate): add upgrade_schema_v2_to_v3.py (column-aware ALTER, not CREATE IF NOT EXISTS)

v2 与 v3 表名相同，CREATE TABLE IF NOT EXISTS 对已有 v2 表是静默 no-op。
迁移改为 PRAGMA table_info 驱动：ALTER ADD COLUMN v3 增量列 + 旧列回填 +
补齐缺失表/索引/视图；platform SCHEMA_VERSION 升 3.0.0 且 ADDITIVE 纳入 2.1.0。"
```

---

## Phase 2 Completion Checklist

- [ ] `gov_relation/schema.py` 新增 V3_ENTITY_DDLS 常量
- [ ] `scripts/govdb.py` 集成 SchemaFactory
- [ ] `scripts/migrate/upgrade_schema_v2_to_v3.py` 可运行
- [ ] 全量测试通过
