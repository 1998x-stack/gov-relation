# Canonical JSONL + SQLite Backup Architecture (破坏性重构)

> 状态：核心引擎 + 步骤1(非破坏汇入) + 步骤2(破坏性替换)已完成；步骤3(构建脚本改写)待做。详情见 CANONICAL_STEP1_COVERAGE.md 与 CANONICAL_STEP2_SWAP.md。

## 1. 设计契约（核心理念反转）

历史上 `SQLite` 是事实源。新模型反转：

- **`data/records/*.jsonl` 是唯一事实源（system of record）**。每个文件是一条记录流，一行一条 JSON 对象，`sort_keys` 保证确定性可 diff。
- **SQLite（`data/database/platform.db`）只是备份/索引副本**，由 `gov2 backup` 从 JSONL 重建，可随时删除重建，**绝不**作为事实源。
- **`verify` 保证两者逐字节一致**：对每条流重导出备份并比对 `count + sha256`，不一致即失败（exit 1）。
- 每个 records 目录自带 `schema.sql`（DDL）、`views.sql`（视图，按需重建）、`manifest.json`（schema 版本 + 每流 {count, sha256} + 来源），因此从裸检出即可重建 SQLite 备份。

## 2. 目录布局

```
data/
  records/                 # ★ 规范 JSONL（事实源）
    persons.jsonl  organizations.jsonl  positions.jsonl  relationships.jsonl
    sources.jsonl  claims.jsonl  jurisdiction_sources.jsonl  ...   (20 流)
    schema.sql  manifest.json  views.sql         # DDL + 目录 + 视图
  database/platform.db     # ★ SQLite 备份（gov2 backup 重建，可删）
  graph/                   # Pillar B 可视化产物（GEXF / index jsonl）
  taxonomy/                # Pillar C 分类归纳产物（classification.jsonl）
```

## 2. 数据流

```
Pillar A 生成:  (source → canonical JSONL)  gov2 build --records --profiles <dir>
                                  │ 幂等去重（按主键 id）
                                  ▼
                     data/records/*.jsonl   ←── 事实源
                                  │
        gov2 backup  ─────────────┘  (重建 SQLite, overwrite)
                                  ▼
                  data/database/platform.db  ←── 只读副本
        gov2 verify：逐流 count+sha256 全等
Pillar B 可视化:  gov2 viz（records → GEXF + index）
Pillar C 分类/归纳: gov2 classify（records → taxonomy）
```

## 3. 三支柱

- **Pillar A 数据生成** `gov2 build`：把人物档案（person profile JSON，含 career_timeline/relationships）无损扁平化为 canonical `persons/positions/relationships` 流；幂等（主键去重）。随后 rebuild SQLite 备份，使生成成果立即可查询。
- **Pillar B 数据可视化** `gov2 viz`：读取 canonical 流，输出 `data/graph/platform-graph.gexf`（节点=person，边=relationship）与 `platform-index.jsonl`（node/edge 索引），供 Gephi/dashboard 使用。
- **Pillar C 数据分类/归纳** `gov2 classify`：从 canonical 流归纳分类面（person× 省份/状态，position×system，relationship×type），写 `data/taxonomy/classification.jsonl` 并返回汇总。

## 4. 迁移与破坏性替换（安全执行）

全量验证已通过：现有 190MB 统一库 → `data/records`（20 流）→ 重建 `platform.db` → verify `consistent=True`（逐流 sha256 一致）。

破坏性替换**尚未执行**（保留旧布局以保安全），按以下顺序进行（每步先验证再推进）：

1. 保留 `data/records/`（新规范源，版本化）。
2. 备份旧数据库节点。
3. 逐一将 legacy `data/database/*.db`、person JSON、v3 库导入 canonical 流（用 `gov2 build` / 对 legacy 库复用 export）。
4. 用 `gov2 verify` 确保 JSONL ↔ SQLite 全一致后，再移除旧目录/旧 `data/platform/gov_relation.db`。
5. 迁移 `docs/` 前端与 `serve_app` 读取 canonical 流或 SQLite 备份。

> 警告：任何一步旧数据尚未全部落到 canonical JSONL 之前，禁止删除旧目录。verify 是破坏性替换的守门条件。

## 5. 命令速查

```bash
python3 scripts/gov2.py export <src.db> data/records     # SQLite → JSONL（导入）
python3 scripts/gov2.py backup data/records data/database/platform.db --overwrite
python3 scripts/gov2.py verify data/records data/database/platform.db
python3 scripts/gov2.py build --records data/records --profiles <person JSON 目录>
python3 scripts/gov2.py viz --records data/records
python3 scripts/gov2.py classify --records data/records
```

测试：`python3 -m pytest tests/test_canon.py -q`