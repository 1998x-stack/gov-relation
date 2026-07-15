# gov-relation

政府人员履历、任职交集与工作关系网络研究仓库。

本仓库的核心产出是按地区构建的关系网络数据：

- `build_*_data.py`：地区或省级网络生成脚本。
- `gov_relation/`：公共 Python 工具包，集中路径、任务队列、slug 和资产盘点逻辑。
- `scripts/`：只读盘点等辅助命令入口。
- `data/database/*.db`：SQLite 结构化关系数据库。
- `data/graph/*.gexf`：可导入 Gephi、Cytoscape 等工具的关系图。
- `data/persons/*.json`：单个人物的深度图谱档案，包含履历、关系、政绩、专业背景、公开性格/工作风格线索和来源置信度。
- `data/tmp/<task_id>/`：新调查产物暂存区；通过 `scripts/process_tmp.py` 校验后再归档。
- `report/*.md` / `report/*.html`：面向阅读的调查报告和图谱页面。
- `data/TODO.json`：全国行政区划调研任务队列。

更完整的文件系统与代码系统说明见 [docs/SYSTEM_OVERVIEW.md](docs/SYSTEM_OVERVIEW.md)。

## 常用命令

查看任务进度：

```bash
python3 run_todo_loop.py --status
```

查看下一个待处理任务：

```bash
python3 run_todo_loop.py
```

生成某个任务的脚本与产物路径提示：

```bash
python3 generate_build_template.py <task_id>
```

盘点当前脚本、数据库、图文件和缺失配对：

```bash
python3 scripts/inventory.py
```

生成下一个 TODO 项的 Opencode 调查 prompt：

```bash
python3 scripts/dispatch_todo.py --next --model standard
python3 scripts/dispatch_todo.py --next --model iagent --prompt-out logs/dispatch/next.prompt.txt
```

并发队列：4 个 OpenCode worker 各自领取不同任务：

```bash
python3 scripts/todo_queue.py claim --worker-id worker-1 --model standard
python3 scripts/todo_queue.py claim --worker-id worker-2 --model standard
python3 scripts/todo_queue.py claim --worker-id worker-3 --model iagent
python3 scripts/todo_queue.py claim --worker-id worker-4 --model iagent
```

注意：这里的 `standard`/`iagent` 是队列里的调查强度标签；nohup worker 默认全部使用 OpenCode `--agent build --model iagent/standard`。

查看队列状态：

```bash
python3 scripts/todo_queue.py status
```

完成并归档后标记任务完成：

```bash
python3 scripts/todo_queue.py done --task-id <task_id> --worker-id <worker-id>
```

用 nohup 启动 4 个长期 worker，并保存日志：

```bash
chmod +x scripts/start_workers_nohup.sh scripts/stop_workers.sh scripts/worker_status.sh
nohup bash scripts/start_workers_nohup.sh > logs/workers/supervisor.log 2>&1 &
```

默认 `AUTO_DONE=1` 且 `GIT_COMMIT=1`：每个任务验证通过、标记 done 后自动执行 `git add -A && git commit -m "Complete gov relation task <task_id>"`。

默认日志位置：

```text
logs/workers/worker-1.log
logs/workers/worker-2.log
logs/workers/worker-3.log
logs/workers/worker-4.log
logs/workers/*.pid
```

查看状态：

```bash
bash scripts/worker_status.sh
```

停止：

```bash
bash scripts/stop_workers.sh
```

安全试跑一个任务上限：

```bash
MAX_TASKS=1 bash scripts/start_workers_nohup.sh
```

可通过环境变量改 OpenCode agent/model：

```bash
OPENCODE_AGENT=build MODEL_1=iagent/standard MODEL_2=iagent/standard MODEL_3=iagent/standard MODEL_4=iagent/standard bash scripts/start_workers_nohup.sh
```

校验并归档暂存区产物：

```bash
python3 scripts/process_tmp.py data/tmp/<task_id>
python3 scripts/process_tmp.py data/tmp/<task_id> --apply
```

生成 GitHub Pages/静态前端使用的数据：

```bash
python3 scripts/build_static_site_data.py
```

启动本地只读后端和前端：

```bash
python3 scripts/serve_app.py --port 8000
```

然后打开 `http://127.0.0.1:8000/app.html`。

运行某个地区网络生成脚本：

```bash
python3 build_anyi_data.py
```

## 当前系统边界

代码主体仍是“一个地区一个生成脚本”的结构。每个脚本通常内置 `persons`、`organizations`、`positions`、`relationships` 四类数据，运行后写出 SQLite 数据库和 GEXF 图文件。

基础工具已开始收敛到 `gov_relation/`：`run_todo_loop.py`、`generate_build_template.py` 和 `scripts/inventory.py` 复用同一套路径、任务队列和命名逻辑。

调查队列可通过 `scripts/dispatch_todo.py` 逐项生成 Opencode prompt；新产物先写入 `data/tmp/<task_id>/`，再由 `scripts/process_tmp.py` dry-run 校验并归档。本地浏览通过 `scripts/serve_app.py` 提供只读 SQLite API；GitHub Pages 发布通过 `.github/workflows/pages.yml` 构建 `docs/assets/data/*.json` 并部署 `docs/`。

需要 4 个 worker 循环跑时，用 `scripts/todo_queue.py claim` 分配任务，队列状态写入 `data/dispatch_state.json`，并由锁目录 `data/dispatch_state.lock` 防止并发抢同一任务。

当前工作区包含大量未跟踪研究产物和生成脚本，说明项目处在持续采集阶段。整理仓库时应优先补文档、统一命名和抽公共库，避免直接移动或删除现有文件。
