# 方案 A · 第二步「破坏性替换」结果报告

日期：2026-09-02　模型：Canonical JSONL + SQLite 备份（SQLite 仅备份）

## 完成的工作

**1. 破坏性替换（legacy 事实源移出工作区 → 可恢复归档）**
- 归档到 `.trash_batch/legacy_20260902/`（193M，18,551 文件）：
  - `data/platform/gov_relation.db`（旧 190MB 统一源）
  - `data/database/*.db`（652 legacy 地区库）
  - `data/graph/*.gexf`（2286 图谱）
  - `data/persons/*.json`（6739 人物档案）
  - `data/provinces/*/{database,graph,persons,reports}`
  - `report/**`（1486 文件）、`research_output/**`、data 根残留 `*.db`
- **未删除、保留为新数据层**：`data/records/`（规范源）、`data/database/platform.db`（备份）、`data/graph/platform-{graph,index}*`（Pillar B）、`data/taxonomy/`（Pillar C）、`data/database/zigong_network.db`（有意保留的示例）。

> 说明：归档而非硬删，破坏性替换同时保留可恢复性；git 历史仍可回溯。

**2. 一致性守门通过**
```bash
python3 scripts/gov2.py verify data/records data/database/platform.db  # exit 0, consistent=True
```

**3. 测试回归**
- 全量 `pytest tests/` → **247 passed**；仅 2 个预先存在的 `Path.hardlink_to` 环境失败（Python 3.9，与本次无关），CI 3.11 不受影响。

## 新数据层结构
```
data/
  records/                # ★ 规范 JSONL（唯一事实源，20 条流 + manifest/schema.sql）
  database/platform.db    # ★ SQLite 备份（gov2 backup 重建，可删）
  graph/                  # Pillar B：platform-graph.gexf + platform-index.jsonl
  taxonomy/               # Pillar C：classification.jsonl
  persons/, provinces/, report/  # （已归档，不再作活动数据层）
```

## 后续（步骤 3 及 git 策略，待拍板）
- **步骤 3**：2342 个 `build_*_data.py` 由「写 legacy SQLite」改为「写 canonical JSONL」（通过 gov2/pillar A）。
- **git 策略**：`data/records`（~200M）+ 是否版本化 / 按省分区；`data/database/platform.db` 已由 `*.db` 忽略。