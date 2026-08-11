# Phase 2: Schema 升级 + govdb.py 切换

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 安全升级 platform schema 到 v3；`govdb.py build` 保持 platform importer 逻辑，并拒绝在未迁移的旧 schema 上运行。

**Architecture（采用方案）:** v3 统一 DDL 由 `gov_relation/factory/schema_factory.py` 提供（基于 `gov_relation/platform/schema.py` 的 `DDL` 抽取建表/视图/索引），legacy `gov_relation/schema.py` 保持兼容不动；`scripts/migrate/upgrade_schema_v2_to_v3.py` 在现有 platform DB 上执行 ALTER/新表；`scripts/govdb.py` 继续使用 platform importer。版本号只是结果记录；是否完成迁移必须同时检查必需列（`gov_relation/platform/schema.py::REQUIRED_V3_COLUMNS` / `has_v3_shape()`，与迁移脚本的 `REQUIRED_V3_COLUMNS` 一致），不能仅凭 `schema_version` 判定。

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

### Task 1: ~~升级 gov_relation/schema.py 添加 v3 DDL 常量~~（已废弃，勿参照执行）

> **该任务已被采用方案取代，不再执行：**
> 当时计划在 legacy `gov_relation/schema.py` 末尾追加 `V3_JURISDICTIONS`/`V3_PERSONS`/…/`V3_ENTITY_DDLS` 常量。
> 评审后采用的设计是 **v3 DDL 统一托管在 `gov_relation/factory/schema_factory.py`**（`SchemaFactory` 基于
> `gov_relation/platform/schema.py::DDL` 抽取 21 表 + 6 gold 视图 + 索引），legacy `gov_relation/schema.py`
> **保持 v1/v2 兼容、不新增 v3 DDL 常量**。
>
> 因此以下内容均已失效，**不要照做**：
> - `V3_ENTITY_DDLS` / `V3_SCHEMA_DDLS` 常量**不存在**于 `gov_relation/schema.py`；
> - 验证命令 `python3 -c "from gov_relation.schema import V3_ENTITY_DDLS; ..."` **会直接 ImportError**（已死）；
> - 如需在全新 DB 上建 v3 形状，调用 `gov_relation.factory.schema_factory.SchemaFactory().create_all(conn)`
>   （省库路径见 Phase 1 Task 7）；platform 库的门禁/幂等建表走 `gov_relation/platform/schema.py::create_schema()`。

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
`gov_relation.platform.schema.create_schema(conn)` 做版本校验与幂等 DDL。Step 0 把
`SCHEMA_VERSION` 升到 `3.0.0`，但不会把 `2.1.0` 声明为自动 additive；因此未迁移旧库
会明确失败并提示先运行迁移，已迁移库直接通过。**不要**在 build 里创建 v3 factory 表。

**执行顺序门禁：** 必须先在数据库副本上验证 Task 3，再升级真实 canonical DB，最后才启用
本 Task 的 `govdb.py` 版本门禁。禁止在未迁移的 v2 库上运行新版 `create_schema()`。

- [x] **Step 1: 在 build_database 开头加 schema 版本门禁（非 create_all）**

```python
# scripts/govdb.py build_database 内，conn 建立后、写数据前：
from gov_relation.platform.schema import create_schema
create_schema(conn)          # 版本校验 + 幂等 DDL；比 create_all 更安全
```

> 若确需 factory 表（省库路径），走 `RegionResearchFactory.generate_gexf()`（见 Phase 1 Task 7），
> 它在新 **province DB** 上调用 `SchemaFactory().create_all()`，不存在与 v2 同名表冲突。

- [x] **Step 2: 验证**

Run: `python3 -m pytest tests/test_platform.py -v --tb=short`
Expected: 现有测试通过（`create_schema` 幂等，无 `sort_order` 崩溃）

**2026-08-11 完成记录（SubAgentReview 后补提交）:** 门禁实现含形状校验（无版本戳库先验 v3 列、`--replace` 也拒绝非 v3 目标），`tests/test_worker_gate.py`（5 例）+ `tests/test_schema_migration.py`（7 例）通过；全量 `pytest tests/ -q` = 243 passed。

- [x] **Step 3: Commit**

```bash
git add scripts/govdb.py
git commit -m "feat(govdb): run create_schema version gate before build; drop v3 create_all in build

v2/v3 share table names; SchemaFactory.create_all in build no-ops and
crashes on idx_positions_person_time (no sort_order in v2). Migration
is owned by scripts/migrate/upgrade_schema_v2_to_v3.py; build only gates
schema version via platform.create_schema."
```

---

> **门禁加固（Phase 2 评审后续）:** 版本戳 `schema_version` 本身不可信——旧版 `create_schema()` 可能
> 在未 ALTER 同名 v2 表的情况下直接盖章 3.0.0。加固后：
> - `create_schema()` 对**无版本戳**的库（无 `schema_meta` 或无 version 行）先校验 v3 形状
>   （`persons.education`/`persons.merged_into_id`、`positions.title_category`/`positions.sort_order`、
>   `datasets.commercial_use`、`sources.commercial_use`），形状缺失 → `RuntimeError` 提示先跑迁移脚本；
>   全新空库（无任何表）仍可直接初始化。stamped 3.0.0 / stamped 不兼容版本 / `ADDITIVE_SCHEMA_UPGRADES`
>   行为保持不变。
> - `build_database` 对已存在目标文件做**只读形状校验**：非 v3 形状（版本缺失/非 3.0.0 或缺 v3 列）
>   即使带 `--replace` 也拒绝，并提示先运行迁移脚本；v3 形状目标 + `--replace` 照常可用。
> - 回归测试：`tests/test_schema_migration.py`（create_schema 门禁 7 例）、`tests/test_worker_gate.py`
>   （govdb build 门禁 5 例）。

### Task 3: 写迁移脚本 upgrade_schema_v2_to_v3.py

**Files:**
- Create: `scripts/migrate/upgrade_schema_v2_to_v3.py`

- [x] **Step 0（前置）: 更新 platform/schema.py 版本容限**

在迁移脚本运行前先改 `gov_relation/platform/schema.py`（评审 F4）：
`SCHEMA_VERSION = "2.1.0"` → `SCHEMA_VERSION = "3.0.0"`，并把
`ADDITIVE_SCHEMA_UPGRADES` 设为空集合。v2→v3 必须由显式迁移脚本完成，
普通 `create_schema()` 不得把旧库自动盖章为 3.0.0。

原因：迁移完成后 DB 里 `schema_version='3.0.0'`。若不更新这两个常量，后续任何
`create_schema()`（govdb resolve / rights-apply 等都会调）都会因
`Database schema 3.0.0 is incompatible with code schema 2.1.0` 抛 `RuntimeError`。
若把 2.1.0 加入 ADDITIVE 集合，当前 `create_schema()` 会执行同名
`CREATE TABLE IF NOT EXISTS`（无法补列）后仍无条件写入 3.0.0，造成假升级。

```python
# gov_relation/platform/schema.py 顶部
SCHEMA_VERSION = "3.0.0"
ADDITIVE_SCHEMA_UPGRADES: set[str] = set()
```

同时把 `gov_relation/platform/schema.py` 的 `DDL` 里那 4 处列级增量对齐为 v3：
`persons` 加 `education`、`merged_into_id`；`positions` 加 `title_category`、`sort_order`；
`datasets`/`sources` 加 `commercial_use INTEGER NOT NULL DEFAULT 0`（保留 `commercial_use_allowed`）。
（新装 DB 用 `create_schema` 直接建出 v3 形状；已有 DB 走本脚本 ALTER。）

- [x] **Step 1: 实现**

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
BACKFILL_SQL: dict[str, str] = {
    "positions": (
        "UPDATE positions SET title_category = category "
        "WHERE title_category = '' AND category != ''"
    ),
    "datasets": (
        "UPDATE datasets SET commercial_use = commercial_use_allowed "
        "WHERE commercial_use = 0 AND commercial_use_allowed != 0"
    ),
    "sources": (
        "UPDATE sources SET commercial_use = commercial_use_allowed "
        "WHERE commercial_use = 0 AND commercial_use_allowed != 0"
    ),
}

REQUIRED_V3_COLUMNS = {
    "persons": {"education", "merged_into_id"},
    "positions": {"title_category", "sort_order"},
    "datasets": {"commercial_use"},
    "sources": {"commercial_use"},
}

# v2 平台已存在全部 21 表；此集合保证极端情况（缺表）也补建
# 实体域缺表场景：schema_factory 的 create_entity_tables(conn) 按需补齐。
def _ensure_entity_tables(conn) -> None:
    from gov_relation.factory.schema_factory import SchemaFactory
    SchemaFactory().create_entity_tables(conn)


def _columns(conn, table: str) -> set[str]:
    return {row[1] for row in conn.execute(f"PRAGMA table_info('{table}')")}


def _has_v3_shape(conn) -> bool:
    tables = _tables(conn)
    return all(
        table in tables and required <= _columns(conn, table)
        for table, required in REQUIRED_V3_COLUMNS.items()
    )


def upgrade(database: Path, *, dry_run: bool = False) -> dict:
    conn = connect(database)
    results: dict[str, list[str]] = {"altered": [], "created": [], "backfilled": []}
    try:
        current = conn.execute(
            "SELECT value FROM schema_meta WHERE key='schema_version'"
        ).fetchone()
        current_ver = current[0] if current else None
        # A version stamp alone is insufficient: an older create_schema()
        # implementation may have stamped 3.0.0 without ALTERing same-name tables.
        if current_ver == "3.0.0" and _has_v3_shape(conn):
            return {"status": "skipped", "reason": "already v3.0.0"}

        # 1) 对已存在的表做列级 ALTER
        for table, alts in ALTER_COLUMNS.items():
            if table not in _tables(conn):
                continue
            existing = _columns(conn, table)
            for col_def in alts:
                col_name = col_def.split(None, 1)[0]
                if col_name in existing:
                    continue
                if not dry_run:
                    conn.execute(f"ALTER TABLE {table} {col_def}")
                    results["altered"].append(f"{table}.{col_name}")
                else:
                    results["altered"].append(f"(dry) {table}.{col_name}")

        # 2) 回填：v3 列从 v2 旧列拷贝
        for table, sql in BACKFILL_SQL.items():
            if table not in _tables(conn):
                continue
            if not dry_run:
                conn.execute(sql)
                results["backfilled"].append(table)
            else:
                # Report planned backfills even though dry-run did not add the
                # destination columns to this connection.
                results["backfilled"].append(f"(dry) {table}")

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
        return {
            "status": "dry-run" if dry_run else "upgraded",
            "from_version": current_ver or "none",
            "to_version": "3.0.0",
            **results,
        }
    except Exception as exc:
        conn.rollback()
        return {"status": "failed", "error": str(exc)}
    finally:
        conn.close()


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

- [x] **Step 2: 测试 dry-run（对真实 v2 库预览）**

Run: `python3 scripts/migrate/upgrade_schema_v2_to_v3.py --database data/platform/gov_relation.db --dry-run`
Expected: `{"status": "dry-run", "from_version": "2.1.0", "altered": ["persons.education", "persons.merged_into_id", "positions.title_category", "positions.sort_order", "datasets.commercial_use", "sources.commercial_use"], "backfilled": [...]}` —— 列出实际会 ALTER/回填的列，**不落库**。

> 验证点：`altered` 应包含 `persons.education`、`positions.sort_order`（评审 F2/F3 的崩点）—— 这正是 v2 缺、v3 必须补的列。

- [x] **Step 2b: dry-run 后用测试库验证目标形状**

```bash
cp data/platform/gov_relation.db /tmp/v3_upgrade_test.db
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

- [x] **Step 3: 真实执行**

Run: `python3 scripts/migrate/upgrade_schema_v2_to_v3.py --database data/platform/gov_relation.db`
Expected: `{"status": "upgraded", ...}`；再跑一次 → `{"status": "skipped", "reason": "already v3.0.0"}`

> **执行前务必备份 canonical DB 并先在副本验证。** 迁移脚本只使用 `connect()`，不会调用
> `create_schema()`；迁移成功并具备 v3 必需列后，其他命令才可使用新版版本门禁。

**2026-08-11 完成记录（SubAgentReview 后补提交）:** 已在副本验证后真实迁移 `data/platform/gov_relation.db`；`schema_version=3.0.0`、audit 外键错误 0。⚠️ **备份注记（审查发现）:** 迁移前计划生成的 `.pre-v3.bak` 实际未落盘，库已迁移、历史 v2 快照无法补回——已在流程上要求后续 DB 迁移必须先行备份。
- [x] **Step 4: Commit**

**2026-08-11 完成记录:** commit `20ca249e9`（含 `upgrade_schema_v2_to_v3.py`、`platform/schema.py`、`scripts/govdb.py`、门禁测试 12 例）。

```bash
mkdir -p scripts/migrate
git add scripts/migrate/upgrade_schema_v2_to_v3.py gov_relation/platform/schema.py
git commit -m "feat(migrate): add upgrade_schema_v2_to_v3.py (column-aware ALTER, not CREATE IF NOT EXISTS)

v2 与 v3 表名相同，CREATE TABLE IF NOT EXISTS 对已有 v2 表是静默 no-op。
迁移改为 PRAGMA table_info 驱动：ALTER ADD COLUMN v3 增量列 + 旧列回填 +
补齐缺失表/索引/视图；platform SCHEMA_VERSION 升 3.0.0，旧版不自动盖章升级。"
```

---

## Phase 2 Completion Checklist

- [x] v3 DDL 由 `gov_relation/factory/schema_factory.py` 统一提供；legacy `gov_relation/schema.py` 保持兼容（Task 1 的 `V3_ENTITY_DDLS` 方案已废弃，见上方说明）
- [x] `scripts/govdb.py` 使用 platform `create_schema()` 做严格版本门禁（不集成 SchemaFactory）
- [x] 门禁只信形状不信戳：`create_schema()` 对无版本戳库校验必需 v3 列；`build_database` 对已存在目标做只读 v3 形状校验，非 v3 形状即使 `--replace` 也拒绝
- [x] `scripts/migrate/upgrade_schema_v2_to_v3.py` 可运行，并通隔离 v2 fixture 测试
- [x] 全量测试通过（241 passed，含新增门禁测试 12 例）
- [x] 真实 `data/platform/gov_relation.db` 已在副本验证后迁移；audit 外键错误为 0
