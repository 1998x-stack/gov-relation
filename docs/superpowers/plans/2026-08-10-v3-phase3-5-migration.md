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

- [x] **Step 1: 实现迁移脚本**

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


def build_province_map() -> dict[str, set[str]]:
    """Build region label → candidate province slugs without overwriting collisions."""
    todo = load_todo()
    mapping: dict[str, set[str]] = {}
    for prov in todo["provinces"]:
        pname = prov["province"]
        pslug = PROVINCE_SLUGS.get(pname, pname)
        for task in prov.get("tasks", []):
            region = task.get("region", "")
            if region:
                mapping.setdefault(region, set()).add(pslug)
            for st in task.get("sub_tasks", []):
                st_region = st.get("region", "")
                if st_region:
                    mapping.setdefault(st_region, set()).add(pslug)
    return mapping


def resolve_province(
    relative_path: str,
    stem: str,
    mapping: dict[str, set[str]],
    overrides: dict[str, str],
) -> tuple[str | None, str]:
    """Resolve only unambiguous mappings; exact path overrides win."""
    if relative_path in overrides:
        return overrides[relative_path], "override"
    candidates = mapping.get(stem, set())
    if len(candidates) == 1:
        return next(iter(candidates)), "todo"
    if len(candidates) > 1:
        return None, "ambiguous:" + ",".join(sorted(candidates))
    return None, "unmatched"


def migrate(
    mapping: dict[str, set[str]],
    overrides: dict[str, str],
    dry_run: bool = False,
) -> dict:
    stats = {
        "databases": 0, "graphs": 0, "persons": 0,
        "unmatched": [], "ambiguous": [],
    }

    # Migrate databases
    for db_path in sorted(DATABASE_DIR.glob("*.db")):
        stem = db_path.stem.replace("_network", "")
        relative = str(db_path.relative_to(REPO_ROOT))
        pslug, reason = resolve_province(relative, stem, mapping, overrides)
        if not pslug:
            stats["ambiguous" if reason.startswith("ambiguous:") else "unmatched"].append(
                {"path": relative, "reason": reason}
            )
            continue
        # 修复（评审 F3-#5）：province_database_dir() 实际接收**省份中文名**（内部再查 slug）。
        # 直接用 PROVINCE_SLUGS.get(pname, pname) 反查，删除死代码三元组（两侧相同）。
        pname = next((n for n, s in PROVINCE_SLUGS.items() if s == pslug), pslug)
        dest_dir = province_database_dir(pname)
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / db_path.name
        if not dry_run and not dest.exists():
            dest.hardlink_to(db_path)
        stats["databases"] += 1

    # Migrate graphs
    for gexf_path in sorted(GRAPH_DIR.glob("*.gexf")):
        stem = gexf_path.stem.replace("_network", "")
        relative = str(gexf_path.relative_to(REPO_ROOT))
        pslug, reason = resolve_province(relative, stem, mapping, overrides)
        if not pslug:
            stats["ambiguous" if reason.startswith("ambiguous:") else "unmatched"].append(
                {"path": relative, "reason": reason}
            )
            continue
        # 修复（评审 F3-#5）：与 db 分支一致，用省份中文名 + 反查 slug。
        pname = next((n for n, s in PROVINCE_SLUGS.items() if s == pslug), pslug)
        dest_dir = province_graph_dir(pname)
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / gexf_path.name
        if not dry_run and not dest.exists():
            dest.hardlink_to(gexf_path)
        stats["graphs"] += 1

    # Migrate person JSONs
    for person_path in sorted(PERSONS_DIR.glob("*.json")):
        # 修复（评审 F3-#4）：文件有两种日期前缀：
        #   YYYYMMDD-<province>-<city>-<job>-<name>.json   (20260724-...)
        #   YYYY-MM-DD-<province>-<city>-<job>-<name>.json (2026-07-24-...)  ← parts[1]=="07" 非省份
        # 因此不能用固定 parts[1]；改为把年份前缀剥掉后，在剩余段里找第一个能匹配
        # PROVINCE_SLUGS 的段（省份中文名；市中可能含 "-"，故逐段尝试）。
        stem = person_path.stem
        parts = stem.split("-")
        if (len(parts) >= 2 and len(parts[0]) == 8 and parts[0].isdigit()):
            remainder = parts[1:]
        elif (len(parts) >= 4 and len(parts[0]) == 4 and parts[0].isdigit()):
            remainder = parts[3:]
        else:
            remainder = parts
        province_name = next(
            (seg for seg in remainder if seg in PROVINCE_SLUGS),
            None,
        )
        if not province_name:
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
    parser.add_argument(
        "--mapping-file", type=Path,
        default=REPO_ROOT / "data" / "migrations" / "province_artifact_map.json",
        help="audited relative-path → province-slug overrides",
    )
    parser.add_argument("--allow-partial", action="store_true")
    args = parser.parse_args()

    mapping = build_province_map()
    print(f"Region→Province mappings: {len(mapping)}")
    overrides = json.loads(args.mapping_file.read_text()) if args.mapping_file.exists() else {}
    stats = migrate(mapping, overrides, dry_run=args.dry_run)
    mode = "DRY-RUN" if args.dry_run else "EXECUTED"
    print(json.dumps({"mode": mode, **stats}, ensure_ascii=False, indent=2))
    unresolved = stats["unmatched"] or stats["ambiguous"]
    return 0 if not unresolved or args.allow_partial or args.dry_run else 2


if __name__ == "__main__":
    raise SystemExit(main())
```

- [x] **Step 2: 测试 dry-run**

Run: `python3 scripts/migrate/migrate_legacy_to_provinces.py --dry-run`
Expected: 输出迁移计划，不实际创建文件；歧义项进入 `ambiguous`，未知命名进入
`unmatched`。当前数据基线约有 26 个跨省同名 region label、24 个歧义 DB/GEXF，
另有约 128 个 DB 与 118 个 GEXF 无 TODO 精确匹配；必须审计并写入 mapping-file。

**2026-08-11 增量执行记录（历史产物审计收尾）：** 本次审计将 261 个 unmatched + 48 个
ambiguous 全部按证据解析：DB/GEXF 依据库内 organizations.location / persons.birthplace /
GEXF 节点标签逐一判定归省，人为覆盖写入 `data/migrations/province_artifact_map.json`
（305 项精确路径→slug）；14 个文件名省份段失效的 person JSON 一并写入覆盖映射，并为
迁移脚本补充 person/holdout 覆盖机制。仅 4 个确无归省证据的产物（openping / test_region
DB+GEXF / 20260723-test.json）写入 `data/migrations/unresolved_holdout.json` 显式排除。
全量 dry-run 与真实 run：`databases=2290, graphs=2281, persons=6629, holdout=4,
unmatched=0, ambiguous=0`；新增 305 个 hardlink，全部 11,200 产物 hardlink 幂等。

- [x] **Step 3: 执行迁移**

Run: `python3 scripts/migrate/migrate_legacy_to_provinces.py`
Expected: 只有在 `ambiguous=[]` 且 `unmatched=[]` 后才成功；随后 hardlink 所有已审计
legacy 文件到 provinces/。禁止依赖 TODO 遍历顺序选择省份。

**2026-08-11 完成记录：** `scripts/migrate/migrate_legacy_to_provinces.py` 真实执行两次
exit 0：首次 305 项 `linked`，复跑全部 11,200 项 `existing-hardlink`；`unmatched=[]` 且
`ambiguous=[]`（4 个 holdout 由 `unresolved_holdout.json` 显式排除，不参与门禁统计）。
门禁已通过（见 Task 1 Step 3）。person 覆盖机制与 holdout 排除机制为本次审计所需的最小
脚本增强。

- [x] **Step 4: Commit**

```bash
git add scripts/migrate/migrate_legacy_to_provinces.py
git commit -m "feat(migrate): add legacy-to-provinces migration with --dry-run"
```

**2026-08-11 完成记录:** commit `622f46493`（含审计产物 `data/migrations/province_artifact_map.json` + `unresolved_holdout.json`）。

**2026-08-11 追加（holdout 人工判定）:** 4 个 holdout（openping_network.db / test_region_network.db / test_region_network.gexf / 20260723-test.json）经用户确认定性为「测试/占位文件，不进迁移」，判定结果已写入 `data/migrations/unresolved_holdout.json`（status=triaged, decision=test/placeholder）。

---

### Task 2: 更新 serve_app.py 和 inventory.py 读新路径

**Files:**
- Modify: `gov_relation/web.py` (list_databases, list_graphs, list_person_profiles)
- Modify: `gov_relation/inventory.py` (collect_inventory)

- [x] **Step 1: web.py — 扩展扫描路径**

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
    # 修复（评审 F3-#9）：seen_stems 只能用来去重「legacy 已收录」的文件；
    # 跨省份去重会误丢同省同名 region（如东湖区/西湖区存在于多省）。
    for prov_dir in sorted(PROVINCES_DIR.iterdir()):
        if prov_dir.is_dir():
            for path in sorted((prov_dir / "database").glob("*.db")):
                if path.stem in seen_stems:
                    continue                  # legacy 已收录，跳过
                rows.append({"name": path.name, "stem": path.stem, "path": str(path.relative_to(REPO_ROOT)), "size": path.stat().st_size})
                seen_stems.add(f"{prov_dir.name}:{path.stem}")   # 跨省同名也保留，仅在省内部去重
    return rows
```

类似地更新 `list_graphs()`、`list_person_profiles()` 和 `list_reports()`。API 返回项增加
`province_slug`；不能只按 stem 去重跨省同名地区。对迁移产生的新旧 hardlink，使用
`(st_dev, st_ino)` 去重；非 hardlink 副本使用解析后的绝对路径作为独立资产。

- [x] **Step 2: inventory.py — 扩展盘点路径**

```python
# 在 collect_inventory() 中添加 provinces/ 扫描
province_dbs = []
for prov_dir in sorted(PROVINCES_DIR.iterdir()):
    if prov_dir.is_dir():
        province_dbs.extend((prov_dir / "database").glob("*.db"))
# merge with existing dbs list, then de-duplicate hardlinks by
# (path.stat().st_dev, path.stat().st_ino).  Graph/person/report 同理。
```

`orphan_databases` / `orphan_graphs` 使用 `(province_slug, network_stem)` 比较，不能继续只用
stem；否则跨省同名地区会互相抵消。新增 tmp_path 测试覆盖 legacy hardlink 不双计数、跨省
同名各保留一条、province report 可见。

- [x] **Step 3: 验证**

Run: `python3 -c "from gov_relation.web import list_databases; dbs = list_databases(); print(f'Total DBs found: {len(dbs)}')"`
Expected: 包含 legacy + provinces 路径的数据库总数

- [x] **Step 4: Commit**

```bash
git add gov_relation/web.py gov_relation/inventory.py
git commit -m "refactor(web,inventory): scan both legacy and province paths"
```

**2026-08-11 完成记录：** commit bd3d9e6；`list_databases/graphs/person_profiles/reports` 均返回 legacy+provinces 合并资产，`collect_inventory()` 按 (st_dev, st_ino) 去重 hardlink。241 tests passed。

---

## Phase 4: 新流程上线

### Task 1: process_tmp.py 支持 province 路径归档

**Files:**
- Modify: `scripts/process_tmp.py` (wrapper → 更新默认目标路径逻辑)

- [x] **Step 1: 在 process_tmp.py 的归档逻辑中加入 province 路径生成**

当前 `process_tmp.py` 是 wrapper（调用 `.agents/skills/.../process_tmp.py`）。
不修改 wrapper，而是在底层脚本中实现一个显式的 destination resolver：

```python
from gov_relation.paths import (
    province_database_dir, province_graph_dir,
    province_persons_dir, province_reports_dir,
)
from gov_relation.todo import find_item_by_id, load_todo

# task_id = staging_dir.name；通过 find_item_by_id(load_todo(), task_id) 找省份。
# build_script 始终归档到 scripts/build/（遵守仓库 builder 约定）。
# database/graph/person_json/report 在识别到省份时分别进入 province_*_dir。
# 无法识别任务时保持 legacy destination，但在 plan 输出中标注 fallback。
# destination resolver 同时用于 dry-run 与 --apply，避免预览/执行路径漂移。
```

新增 `tests/test_process_tmp.py`：覆盖已知省份路由、未知 task fallback、dry-run 不写入、
PersonJSONFactory 输出可被 classify、同名目标拒绝覆盖五种行为。禁止只改常量字典而不测试。

- [x] **Step 2: 提交**

```bash
git add .agents/skills/china-gov-network/scripts/process_tmp.py
git commit -m "feat(process_tmp): auto-route to province paths when province is known"
```

**2026-08-11 完成记录:** commit `2e2385525`（含 `tests/test_process_tmp_province.py` 6 例）。

### Task 2: dispatch_todo.py 生成 province-aware prompt

**Files:**
- Modify: `gov_relation/dispatch.py`

- [x] **Step 1: 在 build_dispatch_prompt 中添加 province 路径信息**

```python
# build_dispatch_prompt 当前直接 return f-string；先赋值给 prompt，再统一 return。
from gov_relation.paths import province_build_dir, province_database_dir

province_name = task.get("province", "")
if province_name:
    build_dir = province_build_dir(province_name)
    db_dir = province_database_dir(province_name)
    prompt += f"\n\nProvince output paths:\n- build: {build_dir}\n- database: {db_dir}"

return prompt
```

同时替换原有 `Canonical destination after validation` 段，不能让同一 prompt 同时声明
legacy 与 province 两套 canonical destination。build script 仍指向 `scripts/build/`；数据库、
GEXF、Person JSON、report 指向对应省目录。新增 dispatch 单元测试断言旧路径不再出现。

- [x] **Step 2: Commit**

```bash
git add gov_relation/dispatch.py
git commit -m "feat(dispatch): include province output paths in prompt"
```

**2026-08-11 完成记录:** commit `38a93c8df`（含 `queue.py` 就绪检查、`tests/test_dispatch.py`/`test_queue.py`）。

### Task 3: 端到端验证 — 用 RegionResearchFactory 跑一个新地区

- [x] **Step 1: 选一个未完成的 TODO 项**

```bash
python3 scripts/tools/run_todo_loop.py  # 找到 next task
```

- [x] **Step 2: 用 factory 生成 build 脚本**

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

- [x] **Step 3: 运行生成的脚本**

```bash
python3 scripts/build/build_sichuan_某个新区_data.py
```

- [x] **Step 4: 验证产物存在**

```bash
ls -la data/provinces/sichuan/database/某个新区_network.db
ls -la data/provinces/sichuan/graph/某个新区_network.gexf
ls -la data/provinces/sichuan/persons/
```

**实际验证样本（2026-08-11）：** `guangxi_南丹县`。通过 staging dry-run 与 apply
生成并晋升 1 个 v3 DB、1 个 GEXF、2 个 Person JSON、1 个报告及
`scripts/build/build_guangxi_南丹县_data.py`。数据库包含 2 人、7 组织、7 任职、
1 关系、7 来源、33 evidence links，`PRAGMA foreign_key_check=[]`。

- [ ] **Step 5: Commit**

```bash
git add data/provinces/
git commit -m "test: end-to-end factory pipeline validation"
```

**2026-08-11 完成记录（策略变更）:** `data/provinces/` 已按 SubAgentReview 决策加入 `.gitignore`（运行时产物不入库，仅骨架 `.gitkeep` 入库），故本步改为**产物验证 + 生成器入库**：验证样本 `guangxi_南丹县` 的 DB/GEXF/2 Person JSON/报告均存在且 `PRAGMA foreign_key_check=[]`；生成器 `scripts/build/build_guangxi_南丹县_data.py` 与 `build_guangxi_大化瑶族自治县_data.py` 已随 Phase 1 提交 `276320464` 入库。Phase 4 全部完成，相关联收尾提交 `8086baaa4`（rights commercial_use / central deprecation / tool sys.path）。

---

## Phase 5: Cleanup (可选)

### Task 1: 移除 central.py

- [x] **Step 1: 标记 deprecated**

```python
# gov_relation/central.py 顶部
import warnings
warnings.warn(
    "gov_relation.central is deprecated as of v3. "
    "Use gov_relation.factory.InsertFactory instead.",
    DeprecationWarning, stacklevel=2,
)
```

- [x] **Step 2: 确认引用并处理**

Run: `rg "from gov_relation.central import" --include="*.py"`
**评审修正（F3-#6）：并非"无输出"——存在 4 处真实引用：**
`tests/test_central.py`, `tests/test_runner.py`, `tests/test_migrate.py`, `scripts/migrate_to_central.py`。
处置：
1. 保留 `gov_relation/central.py`（`migrate_to_central.py` 是仍可能使用的 legacy 迁移工具）；
2. 仅保留 `DeprecationWarning` 标记，**不删除文件、不改这 4 处 import**；
3. 对产物：deprecation 对测试无碍（warning 仅告警），接受测试仍 import central。

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

- [x] Run: `python3 -m pytest tests/ -v` → 220 passed
- [x] Run: `python3 scripts/inventory.py` → 扫描完成
- [x] Web API helpers → databases/graphs/persons/reports 均可读取
- [x] Run: `python3 scripts/govdb.py audit` → v3.0.0，foreign_key_errors=[]
