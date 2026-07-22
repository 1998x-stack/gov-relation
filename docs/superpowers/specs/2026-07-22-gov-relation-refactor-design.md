# gov-relation 系统性重构设计

> 日期：2026-07-22
> 范围：代码框架 · 数据框架 · 日志框架

---

## 1. 当前状态诊断

### 1.1 代码框架

- **484 个 `build_*_data.py`**，合计 ~250,000 行，散落在仓库根目录。
- 每个脚本 400-550 行，~80% 是完全重复的模板代码（SQLite 建表、INSERT、GEXF XML 拼接、颜色字典）。
- 不同脚本的字段名、建表 DDL、颜色规则不完全一致。
- 部分脚本硬编码绝对路径 `BASE = "/workspace/data/xieming/other-codes/gov-relation"`。
- `gov_relation/` 公共包已存在（6 个模块），但构建脚本尚未使用。
- 双入口：`run_todo_loop.py`（旧）和 `scripts/todo_queue.py`（新）。

### 1.2 数据框架

- `data/` 结构合理（database/ graph/ persons/ json/ tmp/）。
- 383 个 `data/tmp/` 暂存目录残留，大部分已完成任务但未清理。
- 文件名命名 95% 一致，少数历史例外（`chenzhou.db`、`jingdezhen_mayor.db`）。
- 队列状态 `data/dispatch_state.json` 在 `.gitignore` 中（合理）。

### 1.3 日志框架

- 无统一日志入口，各模块使用 `print()` 或自制 `log()` 函数。
- 日志散落在 `logs/` 根目录、`logs/dispatch/`、`logs/workers/`。
- 无结构化格式、无级别区分、无轮转机制。
- worker 日志与模块日志脱节。

---

## 2. 设计原则

1. **旧脚本不动** — 486 个历史脚本不改一行，零风险兼容。
2. **新脚本用新库** — 调研 agent 生成的新脚本使用公共库，从 400 行降到 ~50 行。
3. **分批迁移** — 旧脚本逐步移入 `scripts/build/`，不一次性破坏。
4. **三圈同步** — 代码/数据/日志三个圈子同步推进，但不是一次性发布，而是设计上统一、实施上分步。

---

## 3. 代码框架（gov_relation/ 公共库）

### 3.1 新增模块

#### `gov_relation/schema.py` — SQLite 层

```python
def create_tables(conn: sqlite3.Connection, overwrite: bool = False) -> None
def insert_persons(conn, persons: list[dict]) -> dict[int, int]
def insert_organizations(conn, organizations: list[dict]) -> dict[int, int]
def insert_positions(conn, positions: list[dict]) -> None
def insert_relationships(conn, relationships: list[dict]) -> None
```

- 统一 DDL：persons / organizations / positions / relationships 四张标准表。
- 统一字段名（消除 `party_join` vs `party_date` 等差异）。
- `overwrite=True` 时 DROP TABLE 后重建（当前各脚本行为不一致）。

#### `gov_relation/gexf.py` — GEXF 生成器

```python
class GEXFBuilder:
    def __init__(self, title: str = "")
    def add_person(self, id: int, name: str, current_post: str = "", ...)
    def add_organization(self, id: int, name: str, type: str = "", ...)
    def add_relationship(self, source: int, target: int, type: str, context: str = "")
    def write(self, path: Path) -> None
```

- 取代当前每个脚本的 XML 字符串拼接。
- 统一节点属性集、边属性集、XML 命名空间。

#### `gov_relation/colors.py` — 节点样式

```python
def node_color(role: str, level: str = "") -> dict
def node_size(role: str, level: str = "") -> float
def node_shape(title: str) -> str
```

- 统一的职务→颜色映射表。
- 一级党委 > 政府一把手 > 副职 > 部门负责人的大小梯度。
- 支持自定义 override（通过 dict merge）。

#### `gov_relation/runner.py` — 顶层编排

```python
def run_build(
    *,
    slug: str,
    persons: list[dict],
    organizations: list[dict],
    positions: list[dict],
    relationships: list[dict],
    db_path: Path,
    gexf_path: Path,
    overwrite: bool = False,
) -> None
```

- 一个函数完成全部：建表 → 插数据 → 写 GEXF。
- 新脚本只需要调用这一个函数。

#### `gov_relation/log.py` — 统一日志

```python
def get_logger(name: str) -> logging.Logger
def init_logging(log_dir: Path = ..., level: int = logging.INFO)
```

- 统一格式：`[2026-07-22 10:00:00] [INFO] [module] message`。
- 文件 handler（`logs/gov_relation.log`，10MB 轮转，5 备份）+ stdout handler。
- 所有 `gov_relation/` 模块和 `scripts/` 入口通过 `get_logger(__name__)` 获得 logger。

### 3.2 旧脚本生命周期

| 阶段 | 旧 486 个脚本 | 新脚本 |
|---|---|---|
| 1. 新模块发布 | 不变 | 调研 agent 开始使用 `runner.run_build()` |
| 2. 稳定后 | 可选迁入 `scripts/build/` | 全部使用新库 |
| 3. 长期 | 逐渐淘汰/删除 | 全部使用新库 |

### 3.3 `gov_relation/` 完整目录

```
gov_relation/
├── __init__.py     # 已有
├── paths.py        # 已有
├── slugs.py        # 已有
├── todo.py         # 已有
├── inventory.py    # 已有（需更新 scan paths）
├── dispatch.py     # 已有
├── queue.py        # 已有
├── web.py          # 已有
├── schema.py       # 🆕
├── gexf.py         # 🆕
├── colors.py       # 🆕
├── runner.py       # 🆕
└── log.py          # 🆕
```

---

## 4. 数据框架

### 4.1 目标目录布局

```
.
├── README.md                       ← 唯一根级文件
├── scripts/
│   ├── build/                      ← 构建脚本（新 + 迁移来）
│   │   ├── 七里河区_data.py
│   │   └── ...
│   ├── tools/                      ← 队列/模板/批处理
│   │   ├── todo_queue.py
│   │   ├── worker_loop.py
│   │   ├── process_tmp.py
│   │   ├── generate_build_template.py
│   │   ├── dispatch_todo.py
│   │   └── run_todo_loop.py        # 从根目录迁入
│   ├── data/                       ← 数据生成工具
│   │   ├── build_static_site_data.py
│   │   └── serve_app.py
│   └── inventory.py
├── gov_relation/                   ← 公共包
├── data/
│   ├── TODO.json
│   ├── dispatch_state.json
│   ├── database/ / graph/ / persons/ / json/
│   └── tmp/                        ← 仅保留活跃暂存
├── logs/
├── docs/ / report/
└── .gitignore / opencode.jsonc
```

### 4.2 tmp 清理

| 条件 | 动作 |
|---|---|
| 任务已完成 + 产物已归档 | 删除整个 `data/tmp/<task_id>/` |
| 任务已完成 + 产物未归档 | `process_tmp.py --apply` 归档，归档失败则记录到日志后删除 |
| 任务未完成 | 保留 |
| 超过 90 天无修改 | 打包到 `data/tmp_archive/` |

### 4.3 命名收敛

| 当前 | 目标 | 数量 |
|---|---|---|
| `chenzhou.db` | `chenzhou_network.db` | 1 |
| `jingdezhen_mayor.db` | `jingdezhen_mayor_network.db` | 1 |

根目录 `build_*_data.py` → `scripts/build/`：分批迁移，每批 ~20 个，持续 commit。

### 4.4 根目录瘦身

迁走 `run_todo_loop.py`、`generate_build_template.py`、以及所有 `build_*_data.py` 后，根目录仅保留：

- `README.md`
- `data/`（数据目录）
- `scripts/`（工具和构建脚本）
- `gov_relation/`（公共包）
- `docs/` / `report/` / `logs/`（产物和文档）
- `.gitignore` / `opencode.jsonc`（配置）

---

## 5. 日志框架

### 5.1 统一日志配置

- 所有 `gov_relation/` 模块使用 `get_logger(__name__)`。
- `scripts/` 入口使用 `get_logger(__name__)`。
- 格式：`[2026-07-22 10:00:00] [INFO] [gov_relation.gexf] Wrote GEXF: xxx`
- 文件 handler：`logs/gov_relation.log`，10MB 轮转，保留 5 个备份。
- stdout handler：仅 WARNING+（生产模式）或 INFO+（开发模式）。

### 5.2 日志目录重排

| 当前 | 目标 |
|---|---|
| `logs/batch_20260714_*.log` | `logs/batch/20260714_*.log` |
| `logs/jiangxi_上栗县.log` | `logs/tasks/上栗县.log` |
| `logs/dispatch/*.prompt.txt` | 不变 |
| `logs/workers/*.log` | 不变（worker stdout 重定向） |
| — | `logs/gov_relation.log`（新增统一应用日志） |

### 5.3 worker_loop.py 日志升级

- 自制 `log()` 函数替换为 `get_logger("worker_loop")`。
- 日志同时写入 stdout 和 `logs/gov_relation.log`。
- 每个 task 的生命周期事件（CLAIMED / START / END / DONE / FAILED）记录到日志。

### 5.4 旧脚本兼容

- 旧脚本的 `print()` 调用保持不动——它们不 import 新日志模块。
- 旧脚本未来迁移到公共库后自动获得统一日志。

---

## 6. 实施建议

### 阶段一（安全基础）
1. 创建 5 个新模块（`schema.py`, `gexf.py`, `colors.py`, `runner.py`, `log.py`）。
2. 更新 `gov_relation/__init__.py` 暴露新模块。
3. 用新模块构建 1-2 个测试脚本验证流程。
4. 更新 `scripts/inventory.py` 适配新目录结构。

### 阶段二（数据框架）
1. 将 `run_todo_loop.py`、`generate_build_template.py` 移入 `scripts/tools/`。
2. 更新所有引用旧路径的脚本（`scripts/todo_queue.py` 的 `sys.path` 等）。
3. 清理已完成的 `data/tmp/` 目录。
4. 修复命名例外（`chenzhou.db` → `chenzhou_network.db`）。

### 阶段三（批量迁移）
1. 分批将旧 `build_*_data.py` 移入 `scripts/build/`，每批 ~20 个，每个批次 commit。
2. 更新 `scripts/inventory.py` 扫描范围。
3. 更新 `.gitignore`。

### 阶段四（日志上线）
1. 发布 `gov_relation/log.py`。
2. 更新所有 `gov_relation/` 模块使用 `get_logger(__name__)`。
3. 更新 `worker_loop.py` 使用统一日志。
4. 重排日志目录（`batch/`、`tasks/`）。

---

## 7. 风险与缓解

| 风险 | 缓解 |
|---|---|
| 迁移中 worker 引用旧路径 | 迁移前停 worker，迁移后更新路径，再启动 |
| 旧脚本硬编码绝对路径 | 迁移时批量替换为 `project_root()` 函数 |
| 调研 agent 生成的脚本使用旧模板 | 更新 `.agents/skills/china-gov-network/` 中的 prompt 模板 |
| 484 个文件移动导致 git 历史混乱 | 分批移动 + `git mv` 保留 rename detection |
| tmp 清理误删未归档产物 | 先 `process_tmp.py --apply`，失败则不删 |

---

## 8. 验收标准

- [ ] `gov_relation/schema.py`、`gexf.py`、`colors.py`、`runner.py`、`log.py` 创建并测试通过。
- [ ] 新调研脚本能使用 `runner.run_build()` 完成构建（从 400 行降到 ~50 行）。
- [ ] 旧 486 个脚本不改一行仍然可运行。
- [ ] `run_todo_loop.py` 从根目录迁入 `scripts/tools/` 后，`scripts/todo_queue.py` 正常工作。
- [ ] 已归档的 `data/tmp/` 目录清理完毕。
- [ ] 日志统一写入 `logs/gov_relation.log` 且格式一致。
- [ ] `logs/` 根目录下不再有散落的 `*.log`。
