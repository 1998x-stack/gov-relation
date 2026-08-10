# Phase 3-5: Migration + 新流程 + Cleanup

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Phase 3: Legacy 数据迁移到按省份分区。Phase 4: 新调研流程上线。Phase 5: 清理过期代码。

**Spec:** `docs/superpowers/specs/2026-08-10-v3-refactor-design.md`
**Prerequisite:** Phase 1 + Phase 2 完成

## Global Constraints
- Python 3.11 stdlib only
- 不删除 legacy 数据，仅移动或标记 deprecated
- 迁移脚本支持 --dry-run
- 所有操作可逆（hardlink 或 copy，不 move）

---

## Phase 3: Legacy Migration

### Task 1: 实现 migrate_legacy_to_provinces.py

**Files:**
- Create: `scripts/migrate/migrate_legacy_to_provinces.py`

- [ ] **Step 1: 实现迁移脚本**

```python
#!/usr/bin/env python3
"""Migrate legacy flat artifacts into province-partitioned directory structure.

Usage:
    python3 scripts/migrate/migrate_legacy_to_provinces.py --dry-run   # preview
    python3 scripts/migrate/migrate_legacy_to_provinces.py             # execute

Strategy: Hardlink files from data/database/, data/graph/, data/persons/
into data/provinces/<province>/ based on TODO.json region→province mapping.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.paths import (
    DATABASE_DIR, GRAPH_DIR, PERSONS_DIR,
    PROVINCES_DIR, PROVINCE_SLUGS,
    province_database_dir, province_graph_dir, province_persons_dir,
)
from gov_relation.todo import load_todo


def build_province_map() -> dict[str, str]:
    """Build region_slug → province_slug mapping from TODO.json."""
    todo = load_todo()
    mapping: dict[str, str] = {}
    for prov in todo["provinces"]:
        pname = prov["province"]
        pslug = PROVINCE_SLUGS.get(pname, pname)
        for task in prov.get("tasks", []):
            region = task.get("region", "")
            if region:
                mapping[region] = pslug
            for st in task.get("sub_tasks", []):
                st_region = st.get("region", "")
                if st_region:
                    mapping[st_region] = pslug
    return mapping


def migrate(mapping: dict[str, str], dry_run: bool = False) -> dict:
    stats = {"databases": 0, "graphs": 0, "persons": 0, "unmatched": []}

    # Migrate databases
    for db_path in sorted(DATABASE_DIR.glob("*.db")):
        stem = db_path.stem.replace("_network", "")
        # Try exact match first, then try component parts
        pslug = mapping.get(stem)
        if not pslug:
            stats["unmatched"].append(str(db_path.relative_to(REPO_ROOT)))
            continue
        dest_dir = province_database_dir(pslug) if pslug in PROVINCE_SLUGS.values() else province_database_dir(pslug)
        # Resolve province name from slug
        for pname, ps in PROVINCE_SLUGS.items():
            if ps == pslug:
                dest_dir = province_database_dir(pname)
                break
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / db_path.name
        if not dry_run and not dest.exists():
            dest.hardlink_to(db_path)
        stats["databases"] += 1

    # Migrate graphs
    for gexf_path in sorted(GRAPH_DIR.glob("*.gexf")):
        stem = gexf_path.stem.replace("_network", "")
        pslug = mapping.get(stem)
        if not pslug:
            stats["unmatched"].append(str(gexf_path.relative_to(REPO_ROOT)))
            continue
        dest_dir = province_graph_dir(pslug)
        if not any(ps == pslug for ps in PROVINCE_SLUGS.values()):
            continue
        for pname, ps in PROVINCE_SLUGS.items():
            if ps == pslug:
                dest_dir = province_graph_dir(pname)
                break
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / gexf_path.name
        if not dry_run and not dest.exists():
            dest.hardlink_to(gexf_path)
        stats["graphs"] += 1

    # Migrate person JSONs
    for person_path in sorted(PERSONS_DIR.glob("*.json")):
        # Extract province from filename: YYYYMMDD-<province>-<city>-<job>-<name>.json
        parts = person_path.stem.split("-")
        if len(parts) < 3:
            stats["unmatched"].append(str(person_path.relative_to(REPO_ROOT)))
            continue
        province_name = parts[1]
        pslug = PROVINCE_SLUGS.get(province_name)
        if not pslug:
            stats["unmatched"].append(str(person_path.relative_to(REPO_ROOT)))
            continue
        dest_dir = province_persons_dir(province_name)
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / person_path.name
        if not dry_run and not dest.exists():
            dest.hardlink_to(person_path)
        stats["persons"] += 1

    return stats


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    mapping = build_province_map()
    print(f"Region→Province mappings: {len(mapping)}")
    stats = migrate(mapping, dry_run=args.dry_run)
    mode = "DRY-RUN" if args.dry_run else "EXECUTED"
    print(json.dumps({"mode": mode, **stats}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: 测试 dry-run**

Run: `python3 scripts/migrate/migrate_legacy_to_provinces.py --dry-run`
Expected: 输出迁移计划，不实际创建文件

- [ ] **Step 3: 执行迁移**

Run: `python3 scripts/migrate/migrate_legacy_to_provinces.py`
Expected: Hardlink 所有 legacy 文件到 provinces/ 目录

- [ ] **Step 4: Commit**

```bash
git add scripts/migrate/migrate_legacy_to_provinces.py
git commit -m "feat(migrate): add legacy-to-provinces migration with --dry-run"
```

---

### Task 2: 更新 serve_app.py 和 inventory.py 读新路径

**Files:**
- Modify: `gov_relation/web.py` (list_databases, list_graphs, list_person_profiles)
- Modify: `gov_relation/inventory.py` (collect_inventory)

- [ ] **Step 1: web.py — 扩展扫描路径**

在 `list_databases()` 函数中，追加 provinces 路径扫描：

```python
def list_databases() -> list[dict]:
    rows = []
    seen_stems = set()
    # Legacy paths
    for path in sorted(DATABASE_DIR.glob("*.db")):
        rows.append({"name": path.name, "stem": path.stem, "path": str(path.relative_to(REPO_ROOT)), "size": path.stat().st_size})
        seen_stems.add(path.stem)
    # Province paths (skip if already seen from legacy)
    for prov_dir in sorted(PROVINCES_DIR.iterdir()):
        if prov_dir.is_dir():
            for path in sorted((prov_dir / "database").glob("*.db")):
                if path.stem not in seen_stems:
                    rows.append({"name": path.name, "stem": path.stem, "path": str(path.relative_to(REPO_ROOT)), "size": path.stat().st_size})
    return rows
```

类似地更新 `list_graphs()` 和 `list_person_profiles()`。

- [ ] **Step 2: inventory.py — 扩展盘点路径**

```python
# 在 collect_inventory() 中添加 provinces/ 扫描
province_dbs = []
for prov_dir in sorted(PROVINCES_DIR.iterdir()):
    if prov_dir.is_dir():
        province_dbs.extend((prov_dir / "database").glob("*.db"))
# merge with existing dbs list
```

- [ ] **Step 3: 验证**

Run: `python3 -c "from gov_relation.web import list_databases; dbs = list_databases(); print(f'Total DBs found: {len(dbs)}')"`
Expected: 包含 legacy + provinces 路径的数据库总数

- [ ] **Step 4: Commit**

```bash
git add gov_relation/web.py gov_relation/inventory.py
git commit -m "refactor(web,inventory): scan both legacy and province paths"
```

---

## Phase 4: 新流程上线

### Task 1: process_tmp.py 支持 province 路径归档

**Files:**
- Modify: `scripts/process_tmp.py` (wrapper → 更新默认目标路径逻辑)

- [ ] **Step 1: 在 process_tmp.py 的归档逻辑中加入 province 路径生成**

当前 `process_tmp.py` 是 wrapper（调用 `.agents/skills/.../process_tmp.py`）。  
不修改 wrapper，而是在底层脚本中追加逻辑：

```python
# 归档到 provinces/ 目录的条件:
# 1. 识别 TODO.json 中 task_id 的 province 信息
# 2. 如果 province 可识别 → 归档到 data/provinces/<pslug>/database/ 等
# 3. 否则 → 归档到 legacy data/database/ 等
```

- [ ] **Step 2: 提交**

```bash
git add .agents/skills/china-gov-network/scripts/process_tmp.py
git commit -m "feat(process_tmp): auto-route to province paths when province is known"
```

### Task 2: dispatch_todo.py 生成 province-aware prompt

**Files:**
- Modify: `gov_relation/dispatch.py`

- [ ] **Step 1: 在 build_dispatch_prompt 中添加 province 路径信息**

```python
# 在现有 prompt 末尾添加 province 路径提示
from gov_relation.paths import province_build_dir, province_database_dir

province_name = task.get("province", "")
if province_name:
    build_dir = province_build_dir(province_name)
    db_dir = province_database_dir(province_name)
    prompt += f"\n\nProvince output paths:\n- build: {build_dir}\n- database: {db_dir}"
```

- [ ] **Step 2: Commit**

```bash
git add gov_relation/dispatch.py
git commit -m "feat(dispatch): include province output paths in prompt"
```

### Task 3: 端到端验证 — 用 RegionResearchFactory 跑一个新地区

- [ ] **Step 1: 选一个未完成的 TODO 项**

```bash
python3 scripts/tools/run_todo_loop.py  # 找到 next task
```

- [ ] **Step 2: 用 factory 生成 build 脚本**

```python
from gov_relation.factory import RegionResearchFactory

factory = RegionResearchFactory(
    province="四川省",
    region="某个新区",
    level="county",
    targets=[{"role": "区委书记"}],
)
factory.add_person({"canonical_name": "测试", "birth_text": "1970"})
factory.add_organization({"canonical_name": "测试组织"})
build_path = factory.generate_build_script()
print(f"Generated: {build_path}")
```

- [ ] **Step 3: 运行生成的脚本**

```bash
python3 data/provinces/sichuan/build/build_某个新区_data.py
```

- [ ] **Step 4: 验证产物存在**

```bash
ls -la data/provinces/sichuan/database/某个新区_network.db
ls -la data/provinces/sichuan/graph/某个新区_network.gexf
ls -la data/provinces/sichuan/persons/
```

- [ ] **Step 5: Commit**

```bash
git add data/provinces/
git commit -m "test: end-to-end factory pipeline validation"
```

---

## Phase 5: Cleanup (可选)

### Task 1: 移除 central.py

- [ ] **Step 1: 标记 deprecated**

```python
# gov_relation/central.py 顶部
import warnings
warnings.warn(
    "gov_relation.central is deprecated as of v3. "
    "Use gov_relation.factory.InsertFactory instead.",
    DeprecationWarning, stacklevel=2,
)
```

- [ ] **Step 2: 确认无引用**

Run: `rg "from gov_relation.central import" --include="*.py"`  
Expected: 无输出（除 central.py 自身）

- [ ] **Step 3: 提交**

```bash
git add gov_relation/central.py
git commit -m "deprecate(central): mark Central class as deprecated for v3 factory"
```

### Task 2: 清理 root legacy build_*.py

**注意：** 此步骤为可选清理。仅在确认所有 legacy DB 已迁移到 provinces/ 后执行。

- [ ] **Step 1: 备份统计**

```bash
echo "Legacy build scripts at root:" && ls build_*_data.py | wc -l
echo "Legacy DBs in data/database:" && ls data/database/*.db | wc -l
```

- [ ] **Step 2: 移动而非删除 — 归档到 scripts/build/legacy/**

```bash
mkdir -p scripts/build/legacy
# Move root-level legacy scripts
for f in build_*_data.py; do
    git mv "$f" "scripts/build/legacy/$f"
done
```

- [ ] **Step 3: 提交**

```bash
git add scripts/build/legacy/
git commit -m "chore: archive root legacy build scripts to scripts/build/legacy/"
```

---

## 全量最终验证

- [ ] Run: `python3 -m pytest tests/ -v` → all pass
- [ ] Run: `python3 scripts/inventory.py` → 数量一致
- [ ] Run: `python3 scripts/serve_app.py --port 8000` → API 正常
- [ ] Run: `python3 scripts/govdb.py audit` → 平台审计通过
