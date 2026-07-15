# 文件系统与代码系统总览

更新时间：2026-07-15

## 1. 系统定位

该仓库用于系统性整理政府人员履历、组织任职、共事关系、跨地区干部流动，并输出可查询数据库、可视化图谱和调查报告。

当前代码系统更接近“研究流水线”而不是传统应用：

1. 从 `data/TODO.json` 读取全国分省、分地区的待调研任务。
2. 按地区编写或生成 `build_*_data.py` 脚本。
3. 脚本内置人员、组织、任职、关系数据。
4. 运行脚本生成 `data/database/*.db` 与 `data/graph/*.gexf`。
5. 在 `report/` 或 `docs/` 中沉淀 Markdown/HTML 报告。

## 2. 顶层目录职责

| 路径 | 类型 | 职责 |
| --- | --- | --- |
| `gov_relation/` | 公共包 | 路径、任务队列、slug、资产盘点等共享逻辑。 |
| `scripts/` | 工具入口 | 新增辅助 CLI，当前包含只读资产盘点命令。 |
| `build_*_data.py` | 代码 | 单地区或省级网络构建脚本，当前约 98 个。 |
| `build_data.py` | 代码 | 早期/通用构建脚本样例，包含完整数据结构和写库逻辑。 |
| `generate_build_template.py` | 工具 | 根据 `data/TODO.json` 的 `task_id` 打印脚本名、数据库名和图文件名。 |
| `run_todo_loop.py` | 工具 | 查看任务进度、获取下一个任务、标记任务完成。 |
| `scripts/dispatch_todo.py` | 工具 | 根据 TODO 项生成 Opencode/iagent/standard 调查 prompt。 |
| `scripts/todo_queue.py` | 工具 | 并发安全领取/完成/失败/释放 TODO 任务。 |
| `scripts/worker_loop.py` | 工具 | 单 worker 循环领取任务；可选执行 OpenCode。 |
| `scripts/start_workers_nohup.sh` | 工具 | nohup 启动 4 个 OpenCode worker，并写入独立日志/PID。 |
| `scripts/worker_status.sh` | 工具 | 查看 worker 进程、队列和最新日志。 |
| `scripts/stop_workers.sh` | 工具 | 停止 nohup worker。 |
| `scripts/process_tmp.py` | 工具 | 校验并归档 `data/tmp/<task_id>/` 暂存产物。 |
| `scripts/build_static_site_data.py` | 工具 | 生成 `docs/assets/data/*.json` 静态前端数据。 |
| `scripts/serve_app.py` | 工具 | 启动本地只读 SQLite/GEXF API 和 `docs/` 静态服务。 |
| `todo_batch.sh` | 工具 | 批处理任务辅助脚本。 |
| `watchdog.sh` | 工具 | 运行监控辅助脚本。 |
| `data/` | 数据 | 任务队列、行政区划 JSON、SQLite 数据库、GEXF 图谱。 |
| `docs/` | 文档/页面 | 已整理的文档、页面和索引。 |
| `report/` | 报告 | 调查报告、开放问题、图谱 HTML。 |
| `research_output/` | 中间产物 | 调研过程中的临时或半结构化输出。 |
| `logs/` | 日志 | 批处理和自动化运行日志。 |
| `.agents/` / `.claude/` | Agent 配置 | 政府关系网络调研技能说明和参考材料。 |

## 3. 数据目录结构

| 路径 | 当前数量 | 说明 |
| --- | ---: | --- |
| `data/TODO.json` | 1 | 全国任务队列，按省份包含地区、级别、目标职位、完成状态。 |
| `data/json/*.json` | 32 | 省级行政区划清单。 |
| `data/database/*.db` | 107 | SQLite 网络数据库。 |
| `data/graph/*.gexf` | 93 | GEXF 关系图文件。 |
| `data/persons/*.json` | 0 | 单个人物深度图谱档案，按 `YYYYMMDD-{province}-{city}-{job}-{name}.json` 命名。 |
| `data/tmp/<task_id>/` | 临时 | 队列调查暂存区，默认不提交，校验后归档。 |

典型命名：

- 数据库：`data/database/<slug>_network.db`
- 图谱：`data/graph/<slug>_network.gexf`
- 脚本：`build_<slug>_data.py`
- 人物图谱：`data/persons/YYYYMMDD-{province}-{city}-{job}-{name}.json`

少数历史文件未完全遵循该规则，例如 `data/database/chenzhou.db`、`data/database/jingdezhen_mayor.db`。

## 4. 代码系统结构

### 4.1 任务队列工具

`run_todo_loop.py` 是兼容入口，底层复用 `gov_relation.todo`。它提供三个主要动作：

- `python3 run_todo_loop.py --status`：统计全国任务进度。
- `python3 run_todo_loop.py`：打印下一个未完成任务。
- `python3 run_todo_loop.py --mark-done <task_id>`：标记任务完成。

当前队列统计：

- 总任务：3116
- 已完成：237
- 未完成：2879
- 完成率：7.6%
- 已完成省份：江苏省 109/109
- 进展较高：湖南省 67/137，江西省 46/112

### 4.2 公共包

`gov_relation/` 已抽出第一批稳定公共模块：

| 模块 | 职责 |
| --- | --- |
| `paths.py` | 仓库根目录、`data/`、`database/`、`graph/`、`report/` 等路径常量。 |
| `slugs.py` | 中文地区名到文件 slug 的映射，以及标准产物路径生成。 |
| `todo.py` | `TODO.json` 的读取、保存、遍历、统计、查找、标记完成。 |
| `inventory.py` | 只读扫描脚本、数据库、GEXF、报告、文档，并列出缺失配对。 |

### 4.3 构建脚本

`build_*_data.py` 是当前最核心的代码单元。典型脚本包含：

- `BASE` / `BASE_DIR`：仓库根目录。
- `DB_PATH`：SQLite 输出路径。
- `GEXF_PATH`：GEXF 输出路径。
- `persons`：人员节点。
- `organizations`：组织节点。
- `positions`：任职经历。
- `relationships`：人员之间的共事、前后任、上下级、同乡、同系统等关系。
- SQLite 建表和插入逻辑。
- GEXF XML 输出逻辑。
- 简单颜色、大小、标签规则。

常见数据库表：

| 表 | 含义 | 关键字段 |
| --- | --- | --- |
| `persons` | 人员 | `id`, `name`, `gender`, `birth`, `current_post`, `current_org`, `source` |
| `organizations` | 组织 | `id`, `name`, `type`, `level`, `parent`, `location` |
| `positions` | 任职 | `person_id`, `org_id`, `title`, `start`, `end`, `rank`, `note` |
| `relationships` | 关系 | `person_a`, `person_b`, `type`, `context`, `overlap_org`, `overlap_period` |

### 4.4 批量生成脚本

`build_hebei_all_data.py` 是更接近“生成器”的脚本，包含：

- 行政区划加载。
- 地区 slug 映射。
- 构建脚本模板生成。
- 批量地区脚本生成。
- 数据库和 GEXF 的统一写出模板。

后续如果要降低重复代码，应优先从这类脚本抽象公共库。

### 4.5 资产盘点

新增只读命令：

```bash
python3 scripts/inventory.py
```

它会统计：

- 根目录 `build_*_data.py` 数量。
- `data/database/*.db` 数量。
- `data/graph/*.gexf` 数量。
- `data/json/*.json`、`report/*`、`docs/*`、`logs/*` 数量。
- `data/persons/*.json` 人物图谱数量。
- 有数据库但无同名 GEXF、或有 GEXF 但无同名数据库的产物。

### 4.6 队列分派

新增命令：

```bash
python3 scripts/dispatch_todo.py --next --model standard
python3 scripts/dispatch_todo.py --task-id jiangxi_余江区 --model iagent
```

该命令只生成 prompt 和建议命令，不会自动启动外部 agent。默认策略是一个 TODO 项一个 Opencode run。新产物应先写入 `data/tmp/<task_id>/`，验证并归档后再用 `run_todo_loop.py --mark-done <task_id>` 标记完成。

并发 worker 模式：

```bash
python3 scripts/todo_queue.py claim --worker-id worker-1 --model standard
python3 scripts/todo_queue.py claim --worker-id worker-2 --model standard
python3 scripts/todo_queue.py claim --worker-id worker-3 --model iagent
python3 scripts/todo_queue.py claim --worker-id worker-4 --model iagent
```

这里 `standard` / `iagent` 是队列调度标签。实际 OpenCode 调用分为：

- `--agent build`
- `--model agent-loop/standard` 或 `--model iagent/standard`

每次 claim 会：

- 加锁读取 `data/TODO.json` 和 `data/dispatch_state.json`
- 跳过已完成和已被 active claim 的任务
- 生成 `logs/dispatch/<task_id>.<worker>.prompt.txt`
- 在 `data/dispatch_state.json` 记录 worker、model intent、OpenCode agent/model、attempts、prompt path

任务完成后：

```bash
python3 scripts/todo_queue.py done --task-id <task_id> --worker-id <worker-id>
```

失败：

```bash
python3 scripts/todo_queue.py fail --task-id <task_id> --worker-id <worker-id> --reason "..."
```

释放不完成：

```bash
python3 scripts/todo_queue.py release --task-id <task_id> --worker-id <worker-id>
```

状态：

```bash
python3 scripts/todo_queue.py status
```

nohup 长跑：

```bash
chmod +x scripts/start_workers_nohup.sh scripts/stop_workers.sh scripts/worker_status.sh
nohup bash scripts/start_workers_nohup.sh > logs/workers/supervisor.log 2>&1 &
```

默认启动 4 个 worker：全部使用 `iagent/standard`，OpenCode agent 默认 `build`。每个 worker 的日志和 PID 写入 `logs/workers/`。可用环境变量调整：

- `WORKER_COUNT=4`
- `MAX_TASKS=0`，0 表示一直跑到无任务
- `SLEEP_SECONDS=30`
- `OPENCODE_BIN=opencode`
- `OPENCODE_AGENT=build`
- `MODEL_1=iagent/standard`
- `MODEL_2=iagent/standard`
- `MODEL_3=iagent/standard`
- `MODEL_4=iagent/standard`
- `AUTO_DONE=1`

状态和停止：

```bash
bash scripts/worker_status.sh
bash scripts/stop_workers.sh
```

### 4.6.1 暂存区归档

新调查产物先放：

```text
data/tmp/<task_id>/
```

支持的暂存文件：

- `build_<slug>_data.py`
- `<slug>_network.db`
- `<slug>_network.gexf`
- `YYYYMMDD-{province}-{city}-{job}-{name}.json`
- `YYYYMMDD-[地区]-[主题].md`
- `YYYYMMDD-[地区]-[主题].html`

先 dry-run：

```bash
python3 scripts/process_tmp.py data/tmp/<task_id>
```

确认无误后复制到标准目录：

```bash
python3 scripts/process_tmp.py data/tmp/<task_id> --apply
```

默认不会覆盖已有文件；需要替换时显式加 `--overwrite`。

### 4.7 本地后端与静态前端

本地后端：

```bash
python3 scripts/serve_app.py --port 8000
```

主要接口：

- `/api/inventory`
- `/api/databases`
- `/api/database/{name}`
- `/api/database/{name}/persons`
- `/api/database/{name}/relationships`
- `/api/graphs`
- `/api/reports`
- `/api/person-profiles`

静态前端：

- `docs/app.html`
- `docs/assets/data/*.json`

静态数据生成：

```bash
python3 scripts/build_static_site_data.py
```

GitHub Pages workflow 位于 `.github/workflows/pages.yml`，只发布已有产物，不运行联网调研。

## 5. 报告系统

| 路径 | 当前数量 | 说明 |
| --- | ---: | --- |
| `report/*` | 约 99 | 调查报告、开放问题、图谱页面。 |
| `docs/*` | 约 17 | 早期文档、索引页面、少量发布页。 |

建议约定：

- `report/`：研究报告主目录，保留日期、地区、主题命名。
- `docs/`：项目说明、索引、可发布页面。
- `research_output/`：尚未整理进正式报告的中间材料。

## 6. 推荐工作流

### 单个地区

1. `python3 run_todo_loop.py` 获取下一个任务。
2. `python3 generate_build_template.py <task_id>` 确认脚本和产物路径。
3. 新建或更新 `build_<slug>_data.py`。
4. 运行脚本，生成 `.db` 和 `.gexf`。
5. 写入 `report/YYYYMMDD-地区-主题.md`。
6. 用 `python3 run_todo_loop.py --mark-done <task_id>` 标记完成。

### 批量地区

1. 先确认行政区划 JSON 存在。
2. 使用省级批量脚本或生成器创建地区脚本。
3. 分批运行，避免一次性覆盖大量数据库和图文件。
4. 对失败地区记录到 `report/open_gaps*.md` 或日志。

## 7. 当前整理原则

由于当前 git 工作区有大量未跟踪文件和已修改产物，不建议立即进行大规模移动或删除。建议分三阶段整理：

### 阶段一：文档化和命名收敛

- 保留现有文件路径。
- 补充 README 和系统总览。
- 记录历史命名例外。
- 新增脚本时统一使用 `build_<slug>_data.py`、`<slug>_network.db`、`<slug>_network.gexf`。

### 阶段二：抽公共库

已新增 `gov_relation/` 包，并开始沉淀：

- `paths.py`：统一路径。
- `slugs.py`：中文地区名到 slug 的映射。
- `todo.py`：任务队列读写。
- `inventory.py`：资产盘点。

后续仍可继续补充：

- `schema.py`：SQLite 建表语句。
- `gexf.py`：GEXF 写出逻辑。
- `colors.py`：节点颜色和大小规则。

先让新脚本使用公共库，再迁移旧脚本。

### 阶段三：目录重排

待公共库稳定后，再考虑把脚本移动为：

```text
scripts/build/        # 地区构建脚本
scripts/tools/        # 队列、模板、批处理工具
gov_relation/         # 公共 Python 包
data/database/        # SQLite 产物
data/graph/           # GEXF 产物
report/               # 正式报告
docs/                 # 项目文档和发布页
```

迁移时应同时提供兼容入口或迁移说明，避免破坏已有批处理命令。

## 8. 风险点

- 根目录脚本数量多，重复逻辑多，后续维护成本会继续增加。
- 不同脚本的建表方式、是否删除旧数据库、GEXF 样式规则并不完全一致。
- 部分输出文件名存在历史例外，批处理时需要显式处理。
- `data/database`、`data/graph`、`report` 中同时存在已跟踪和未跟踪产物，整理前需要先决定哪些产物应纳入版本控制。
- 脚本里存在绝对路径 `BASE = "/workspace/data/xieming/other-codes/gov-relation"`，迁移到其他机器时需要改为相对路径或统一配置。

## 9. 下一步建议

优先做两个低风险改进：

1. 新增 `gov_relation/` 公共包，只让后续脚本使用，不回改所有历史脚本。
2. 写一个只读清单脚本，扫描 `build_*_data.py`、`.db`、`.gexf`、报告文件，输出地区覆盖率和缺失产物。

这样可以逐步把研究流水线从“文件堆叠”收敛为“可持续维护的生成系统”。
