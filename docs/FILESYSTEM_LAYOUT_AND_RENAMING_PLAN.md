# 文件系统层级分类体系与重命名系统方案

> 目标：解决 `report/`(1380 个文件)、`data/persons/`(6600+)、`data/graph/`(2284) 等目录
> 文件过多、命名口径混乱、省份/日期格式不一、缺失成对文件的问题。
> 本文是**设计提案**，落地需逐步实施 + 迁移脚本，切勿一次改动破坏存量数据。

---

## 一、现状问题诊断

| 目录 | 数量 | 主要问题 |
|---|---|---|
| `report/` | ~1380 文件 | 全部扁平，交易日+地区混合命名；适用两类语义（研究报告、领导班子快照）没区分；html/md 双写冗余 |
| `data/persons/` | 6600+ | 全部扁平；日期两种格式混用（`20240325` vs `2026-07-17`）；无省份/角色分类；文件名内嵌的角色描述混乱（"原县委书记"、"已离任"等非结构化字段） |
| `data/graph/` | 2284 gexf | 按 slug，但存在 `xxx.gexf` 与 `xxx_network.gexf` 两种命名；成对 `.db` 几乎缺失（2284 gexf vs 1 db） |
| `data/database/` | 空 | 本该容纳各区域 `<slug>_network.db`，未填充 |
| `data/provinces/`、`data/json/` | 33 / 32 | 省份划分信息与行政划分 JSON，命名基本可用但建议纳入统一规则 |
| `data/findings/`、`data/research/` | 散落 | 调研草稿与证据，命名口径最乱（中英混用、日期不一致） |

**核心症结**：缺少统一的「文件分类体系 + 命名语法」，各地生成脚本各自命名，导致：
1. 日期格式不统一（`8位紧凑` vs `ISO横线`）
2. 层级不分组（几千个文件堆在一个目录）
3. 实体类型（人/关系图/报告）没有显式前缀或子目录
4. 无「主文件 + 伴生文件」的对偶关系（db/gexf、html/md/report）

---

## 二、设计原则

1. **按数据语义分层，不按生成批次扁平堆放** —— 第一层是领域（person/graph/report/org），第二层是地理（省市），第三层才是明细文件。
2. **单一事实命名语法** —— 全仓库统一一种文件名模板，脚本可解析、可排序、可校验。
3. **日期领先且唯一格式** —— 所有文件统一 `YYYYMMDD`（8 位），禁止 `2026-07-17`。
4. **目录兜底、文件去重** —— 通过子目录归档实体，文件命名只保留「身份信息 + 角色/类型的净化版本」，不做无意义流水。
5. **成对文件强制命名关联** —— graph 的 `.gexf`/`.db` 前缀同 slug；report 的同主题 `.md`/`.html` 同名同地。
6. **兼容既有 slug 体系**（`gov_relation/slugs.py`），不打断 `inventory.py`、`serve_app.py`、`govdb.py` 的读取。

---

## 三、目标层级分类体系（推荐）

```
data/
├── database/                      # 区域级结构化数据库（SQLite，gitignore）
│   └── <slug>_network.db
├── graph/                         # 关系图谱（GEXF）
│   └── <slug>_network.gexf
├── persons/                       # LEGACY 个人履历档案（git 跟踪来源）
│   └── YYYYMMDD-<province>-<city>-<role>-<name>.json
├── provinces/                     # 省级分层 CANONICAL（gitignore 生成视图）
│   └── <province-slug>/
│       ├── database/ <slug>_network.db
│       ├── graph/     <slug>_network.gexf
│       ├── persons/   YYYYMMDD-...json   # 硬链接镜像 data/persons/ + 新建产物
│       └── reports/   新建报告
├── json/              # 行政划分等基础数据
├── research/ / findings/ / tmp/   # 调研草稿 / 结论 / 暂存
└── platform/                      # 统一平台库（现有 gov_relation.db）

report/                            # 存量顶层报告（约 1380，保持平铺）
└── YYYYMMDD-<city>-<kind>-<主题>.md|.html
```

### 关键层级决策（与现行代码对齐，已执行）

- **persons 的规范读取位置是 `data/provinces/<slug>/persons/`**（`paths.province_persons_dir()`），
  由 `inventory.py`/`web.py` 扫描，`dispatch.py` 和技能 `process_tmp.py` 把新建档案直写到此。
- **git 跟踪的源保持在扁平 `data/persons/`**。规范位置是**硬链接镜像**（`migrate_legacy_to_provinces.py`
  或 `scripts/layout/migrate_persons_to_provinces.py --link`），保证源有 git 历史、规范可读，且 inventory 按 inode 去重。
- 新构建产物直接写规范子目录，`data/database/`、`data/graph/`、`data/provinces/` 均为 gitignore 生成区。
- report 存量保持平铺 `report/`；新建报告写 `data/provinces/<slug>/reports/`。

### 关键层级决策

- **persons** 规范视图按**省份 slug** 分一层（`data/provinces/<slug>/persons/`），git 跟踪源保持扁平 `data/persons/` 并复用 `slugs.py` 省份 slug。该位置由 `inventory.py`/`web.py` 读取，构建产物由 `dispatch.py`/技能 `process_tmp.py` 直写。
- **report** 存量保持顶层平铺；新建报告写 `data/provinces/<slug>/reports/`；同一主题的 `.md` 与 `.html` 必须同「stem」，仅扩展名不同，便于工具配对。

---

## 四、命名规范（RENAMING 系统）

### 4.1 统一时间戳
- **只允许** `YYYYMMDD`（8 位紧凑），如 `20260722`（对应 `dispatch.py` 既定约定）。
- 存量 `YYYY-MM-DD`（ISO）一律归一为 8 位：`2026-07-22` → `20260722`。已执行于
  `data/persons/`（280 文件）与 `data/provinces/<slug>/persons/`（24 文件）。
- 出于排序需求，统一为「日期在前」。

### 4.2 通配文件名（person）
```
YYYYMMDD-<province>-<city|county>-<role-normalized>-<name>.json
```
- 字段分隔符用 `-`；角色名净化：**去除「原/已离任/前任」类冗余前缀**，改为后缀或副字段 `(原)` 备注。
- 例：`20240325-福建省-福州市-原县委书记-肖华.json`
- 净化的名称（slug 化）来自 `paths.slugs`。

### 4.3 通配符命名（graph / database）
```
<slug>_network.gexf        # 图
<slug>_network.db          # 其结构化源库（同 slug 配）
```
> 修复现存的 `chenzhou.gexf`（无 `_network`）→ `chenzhou_network.gexf`，并补 `._network.db`。

### 4.4 report 命名
```
<YYYYMMDD>-<city|-县>-<kind>-<主题>.md|.html
kind ∈ {领导成员, 履历, 交流网络, 证据更新, ...}
```
- 同主题 `.md` 与 `.html` stem 相同。如 `20260722-南昌-领导班子-2026.md/.html`。

### 4.5 findings / research
```
<YYYYMMDD>-<city>-<主题>[-_更新].md
```
- 消除中英混排（如 `biyang-county-mayor.md` → `20260724-泌阳县-县长.md`）。
- 多版本用 `-v2`/`_修订` 后缀（保留，不覆盖原稿）。

---

## 五、命名解析（机器可用）

- 提供 `gov_relation/naming.py`：`parse_person_filename()`、`parse_report_filename()`、`parse_graph_slug()` 解析/校验任意前文命名。
- 所有目录文件应由同一种规约生成，禁止脚本各自拼字符串。

---

## 六、落地步骤（实际已执行部分用 ✅ 标注）

### 阶段 1：写入规范库 + 干扫描管线
1. ✅ coinsured **person 规范位置 = `data/provinces/<slug>/persons/`**（与代码读取一致），源保持 `data/persons/` git 跟踪。
2. ✅ 工具：`scripts/layout/`（`plan_mapping.py` 出清单、`province_map.py` 省份解析、`apply_migration.py` 旧映射执行、`migrate_persons_to_provinces.py` 迁移/硬链接）。

### 阶段 2：数据统一与镜像（✅ 已执行）
- ✅ persons 日期归一 `YYYYMMDD`：`data/persons/`（280 文件，commit `f9c6ce1e`）、`data/provinces/*/persons/`（24 文件）。
- ✅ graph 归一 `<slug>_network.gexf`（4 文件 + zigong db 归位 `data/database/`，commit `5f52014b`）。
- ✅ 规范 persons 视图：`scripts/layout/migrate_persons_to_provinces.py --link` 建立 6620 个硬链接镜像，inventory 按 inode 去重为 6850（容量与基线一致）。
- report 存量保持平铺 `report/`；新建报告写 `data/provinces/<slug>/reports/`（未改存量）。

### 阶段 3：回归校验（✅）
- `python3 scripts/inventory.py`：Person JSON=6850（与基线一致）、graph 域一致。
- `pytest` 全量：7 个失败均为**预存环境问题**（`Path.hardlink_to` 缺于 Py3.9、OpenSSL P-256 检测），与整理无关。

### 阶段 4：固化规范（待做）
- 更新 `AGENTS.md` / `CLAUDE.md` 目录约定、`scripts/build/build_*_data.py` 模板输出均指向规范目录；如需 CI lint 可后续加 `layout check`。

---

## 七、风险与说明（务必先读）

- **规范位置 `data/provinces/**` 整体 gitignore（仅放行目录与 `.gitkeep`）**：因此 person 档案的 git 跟踪**必须留在扁平 `data/persons/`**，规范位用**硬链接镜像**（不要物理 move，否则全部退出版本控制）。
- **日期一律 8 位 `YYYYMMDD`**：`dispatch.py` 是权威约定；勿再引入 ISO 横线（`-`）命名，否则 inventory/dispatch 扫描口径不一致。
- 跨多省身份：主档案放现归属省，其它省生成 `_cross.json` 指针，避免 inode 重复被算两次。
- `report/_unpublished_tools/` 这类特殊目录**移出迁移范围**，保持原样。
- `.trash_batch`、`.playwright-mcp`、`.checkpoints`、`.omo`、`.superpowers` 等内部工具目录不在迁移范围。

---

## 理想终态目录样例（对齐现行代码）

```
data/
  persons/20240325-福建省-福州市-原县委书记-肖华.json          # git 跟踪源（扁平）
  provinces/fujian/persons/20240325-福建省-福州市-原县委书记-肖华.json   # 硬链接镜像
  provinces/gansu/persons/20240722-甘肃省-金昌市-市长-王琳玺.json
  provinces/gansu/database/xhsx_network.db                    # 生成
  provinces/gansu/graph/xhsx_network.gexf                     # 生成
report/20260714-九江市浔阳区-领导班子.md                        # 存量平铺
  provinces/sichuan/reports/20260714-成都市-领导班子.html      # 新建报告
```