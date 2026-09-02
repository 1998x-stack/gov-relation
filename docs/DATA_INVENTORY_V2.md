# 数据资产系统性盘点报告（Data Inventory）

> 生成时间：本会话（基于当前工作区快照）
> 范围：`gov-relation` 仓库全部数据产出，含统一平台库、历史遗留资产与暂存/研究区
> 说明：数字来自 `scripts/inventory.py`、对 `data/platform/gov_relation.db` 的 SQL 统计及目录扫描，时间为"当前快照"，非实时。

---

## 一、总览（Top-Level）

仓库按"研发 → 校验/归档 → 摄取(platform) → 解析/质检 → 发布"思路组织。数据分散在两类位置：

- **统一平台库**（v2 规范，唯一权威单文件库）：`data/platform/gov_relation.db`（约 146 MB）
- **历史/遗留资产**（legacy，地域生成器产出）：`data/database/`、`data/graph/`、`data/persons/`、`data/provinces/*/`、`report/`、`data/research/`、`data/findings/`、`data/tmp/`

### 规模汇总（核对自 inventory.py）

| 资产 | 数量 | 位置 |
| --- | --- | --- |
| 地区构建脚本 build_*_data.py | **2,276** | `scripts/build/`（2,280 个 .py，其中 build_<slug>_data.py 占 2,276）+ 根目录遗留 | 
| 独立 SQLite 数据库 | **39** | `data/database/`(2) + `data/provinces/*/database/`(37) |
| GEXF 关系图 | **2,322 → 2,285** | `data/graph/` 2285 + 省级 `provinces/*/graph` |
| 行政区划 JSON | 32 | `data/json/`（31 省 + 1 simple） |
| 人物档案 JSON（persons） | **6,851 → 6,634** | `data/persons/` + `provinces/*/persons/` |
| 调查报告 md/html | **1,420**（report 1,383） | `report/` 1,309 md + 73 html + 38 其他 |
| 文档 docs | 24 | `docs/` |
| 暂存区 data/tmp | **686** 个任务目录 | 未 promote 的出场产物 |
| 待办任务 TODO | ~3,100 | `data/TODO.json` |

> 注意：inventory.py 与目录扫描数字略有出入（带 .gitkeep、测试残留等），本表以上述扫描为准。

---

## 二、统一平台数据库 `data/platform/gov_relation.db`（v2 权威）

### 2.1 分层表与行数

| 数据层 | 表 | 行数 | 契约 |
| --- | --- | --- | --- |
| **Bronze（金砖）** | `datasets` | 6,635 | 源入库登记（2 legacy_sqlite + 6,633 person_profile） |
| | `raw_records` | 6,676 | 原始行/载荷，无字段损失 |
| | `profile_documents` | 6,586 | 人物 JSON 档案 |
| **Silver（银）** | `persons` | **19,609** | 规范人物实体 |
| | `organizations` | **12,322** | 机构实体 |
| | `positions` | **14,780** | 任职记录（当前 5,808 / 历史 8,972） |
| | `relationships` | **13,385** | 关系记录 |
| | `person_statuses` | 6,529 | 当前状态观测 |
| | `person_aliases` | 36 | 别名 |
| **Evidence** | `sources` | **10,001** | 来源登记 |
| | `claims` | **26,341** | 事实/风险/开放问题声明 |
| | `evidence_links` | **30,273** | 事实↔来源可追溯 |
| | `entity_provenance` | 6,629 | 实体生成溯源 |
| **Quality** | `quality_issues` | 425 | 质检隔离 |
| | `resolution_candidates` | **9,758** | 疑似重复实体 |
| | `ingest_runs` | 1 | 入库运行记录 |
| **Gold** | `rights_manifests` | 0 | 商业授权清单（未启用） |
| | `rights_review_keys` | 0 | |
| | `source_rights_decisions` | 0 | |
| **区域** | `jurisdictions` | 2,197 | 行政区划 |
| `schema_meta` | 1 | 库版本/元数据 |

### 2.2 关键清洗/质检缺口
- **机构类型：`organizations.organization_type` 12,311 行为空**（占 99.9%），仅 11 行有类型 → 机构类型尚未清洗，影响实体归并级联。
- **关系标签高度非规范化**：`relationships.relationship_type` 有 100+ 种离散值，包含大量未标准化的中文杂项（如"上下级""前后任""党政搭档""跨县交流杠杆""抗风险"等约 90 种中文标签与约 45 种英文标签共存），而非统一的 `overlap`/`superior_subordinate`/`predecessor_successor` 等，render 和 graphs 的一致性受限。
- **职位类别（`positions.category`）** 混中英文与重复（如 "government 5767 / party 4577 / 政府 5 / 党委 8 / 人大 3" 并用），有非规范化。
- **人物身份状态**：unresolved 16,796 / verified 2,813 → 大量人物仍待核实。
- **人物性别/生日覆盖不全**：有 birth 字段仅 3,354 人；性别 14,166 人为空或占位。
- **Quality issues**：378 条 `profile_relationship_invalid_target`（warning）+ 47 条 `profile_missing_name`（error）→ 存在错位关系目标与缺名实体，error 级会阻塞 release。
- **实体解析保守**：resolution_candidates 9,758 条疑似重复，"宁可分裂不可误并"（安全取向），表示大量跨库同名可再合并。

### 2.3 覆盖度
| 观测点 | 值 |
| --- | --- |
| 平台 persons | 19,609 |
| 平台 jz 有任职 | 5,998 人（有 position） |
| 人物 JSON（data/persons） | 6,634 文件 → 6,586 档案入库 |
| 差距 | 遗留 etc. `data/graph` 2283 个 GEXF 无对应 .db；provinces 内 37 个区域 DB 尚未批量导入 platform（platform 仅 2 个 legacy SQLite） |

---

## 三、人物档案（`data/persons/` + `data/provinces/*/persons/`）

### 3.1 省份分布（按档案文件名省/区前缀）
| 省/区 | 档案数（约） |
| --- | --- |
| 河南省 | 688 |
| 湖北省 | 503 |
| 黑龙江省 | 493 |
| 辽宁省 | 412 |
| 河北省 | 380 |
| 广西壮族自治区 | 363 |
| 陕西省 | 340 |
| 山东省 | 318 |
| 广东省 | 314 |
| 吉林省 | 286 |
| 安徽省 | 257 |
| 贵州省 | 247 |
| 福建省 | 243 |
| 甘肃省 | 228 |
| 内蒙古自治区 | 207 |
| 湖南省 | 193 |
| 山西省 | 189 |
| 四川省 | 172 |
| 江西省 | 157 |
| 青海省 | 106 |
| 重庆市 | 86 |
| 云南省/宁夏 | 79 / 78 |
| 西藏 | 68 |
| 新疆 | 57 |
| 海南 | 52 |
| 浙江 | 37 |
| 北京 | 33 |
| 上海 | 29 |
| 天津 | 4 |
> 另有少量文件命名不规范（如 永泰、阳曲县、泸州、beijing、test.json）约零散 <30，属历史遗留需重命名。

- 文件名格式（已规范化为主）：`YYYYMMDD-省份-市/县-职务-姓名.json`（schema_version 1.0）。
- 每档案字段：identity（name/aliases/gender/ethnicity/birth/birthplace/native_place/education/party_join/work_start）、current_status（rationally rank/as_of）、career_timeline（start/end/org/title 数组）、relations、achievements/sources/confidence、dedupe_keys（name_birth、name_birthplace）。

---

## 四、关系图（`data/graph/*.gexf` + `provinces/*/graph`）

- **GEXF 图：`data/graph/` 2,285 个 + 省级图若干**（inventory 汇总 2,322）。
- 命名：地区 slug （如 aksai、anyuan、baoding…，多为县/区级）。
- 可用 Gephi/ Cytoscape 导入；包含节点（人物/机构）与边（任职交集/前任继任/上下级等）。
- **缺口：data/graph 目录下 2,283 个 GEXF 无同名 `.db`**（database 目录只保留了 37 个地区库 + 2 个遗留库）。大部分历史图只留 gexf 展示，底层结构库已下沉或未入库。**仅 39 个地区库可追溯。**

---

## 五、数据库（`data/database/` + `provinces/*/database`）

| 位置 | 数量 | 示例 |
| --- | --- | --- |
| data/database/ | 2 | test_region_network.db、zigong_network.db（遗留测试/省级） |
| data/provinces/<省>/database/ | 37 | 通河县、集贤县、果洛、门源、鹿邑、商南、咸丰、西陵、城区、金州、盖州、铁岭县、沈北、阜新市、西丰、昌都、乡宁、襄垣、东安、益阳、沅江、娄星、南关、延吉、柳河、洮南、乌达、东河、兴安盟、九原、玉泉、满洲里、定州、文安、临安等 |
| data/.trash_batch/stage_*/ | ~31 个副本 | 清理历史备份 |

数据库 schema：persons / organizations / positions / relationships，供`govdb.py`无损导入。

---

## 六、报告（`report/` + docs 内报告副本）

- **report/**：1,383 个文件 = **1,309 md + 73 html + 1 文件夹（_unpublished_tools）**。
- **docs/**：另有 report md/html 副本（用于 GitHub Pages）。
- 内容：领导班子、市委书记/市长、县委书记/县长、关系网络图、履历深挖、跨县干部交流网络、前任/继任、纪委书记/组织部部长、风险纪律信号等。
- 覆盖：河北省12、广11、黑9、山东9、上海8、重庆7、辽7、豫7、晋(h/f)、吉7 …（抽样展示），全国省级均涉及。

---

## 七、研究/发现/暂存区

- **data/research/**：12 个内部研究产物（跨县交流网络、领导班子等）。
- **data/findings/**：5 个调查发现存档（如 宾阳县长、珙县前任继任、大同阳高技术交流等）。
- **data/tmp/**：**662 个任务暂存目录**（如 gongjingqu_20260726、heilongjiang_* 等）——*未通过 process_tmp 校验入正库的出场产物*，是"已收数据"中尚未归档/尚待 promote 的部分。inventory 显示仅 4 个 tmp 文件被计入。

---

## 八、行政区划与任务队列

- **data/json/**：31 省行政区划 JSON（anhui…zhejiang_administrative_divisions.json），用于解析、slug、scope。
- **data/TODO.json**：全国调研任务队列（包含 provinces、generated_at、note），~3100 任务（3 个省级框架：目前按调研队列逐步出）。
- **data/dispatch_state.json / queue_guangdong.json**：任务分发状态快照与广东队列。

---

## 九、数据来源与质量（`sources` + strong evidence）

### 9.1 来源构成（sources 表，10,001 条）
| source_type | 高可靠 | 中可靠 | 低可靠 | 合计 |
| --- | --- | --- | --- | --- |
| official（官方/任免通知） | 7,181 | 82 | 63 | ~7,326 |
| encyclopedia | 53 | 877 | 15 | ~945 |
| media | 457 | 478 | 133 | ~1,068 |
| database | 46 | 140 | 18 | ~204 |
| appointment_notice | 207 | 17 | 1 | ~225 |
| inferred | 0 | 27 | 76 | ~103 |
| other | 24 | 10 | 96 | ~130 |

- 整体以**官方来源（official）高可靠**为主（7,181），百度/媒体/词条次之。
- **rights/商业授权字段几乎为零**：所有 commercial_use_allowed、source_rights_decisions、rights_manifests、rights_review_keys 均为 0 或空 → 商业发布通道未启用（符合 ARK 设计"默认禁止"）。

### 9.2 证据
- evidence_links：30,273 条把 claims/facts 绑定到 source_id。
- claims：26,341 条（含风险与诚信信号、开放问题）。
- 大量 legacy_source 证据、低置信度约束（如"备注"字段），指向后续人工核实。

---

## 十、整体评价与缺口

### 已具备的强项
1. 人物档案 1.9 万（platform 层）/ 机构 1.2 万 / 关系 1.3 万，全国省级（31 分区）全覆盖。
2. 官方来源权重高，证据链路完备（claim→evidence→source 可追溯）。
3. 分层青铜/银/证据/质检四层架构清晰，保守实体解析安全。
4. 城区、省份两套 数据库 + gexf 图双产物，报告体系多形态（md/html + 图）。

### 主要缺口 / 待办
1. **统一库导入不完整**：平台库只入库 2 个 legacy SQLite + 6,633 person_profile；数据 provinces 里 37 个地区 DB 尚未批量导入（——`data/graph/` 2,283 个无名 GEXF 缺 DB）。
2. **机构类型 99.9% 为空**（12,311/12,322）；机构 registry 未建，影响解析。
3. **职位类别 / 关系类型 非标准化**（多种中英文标签混用），与 schema 名义契约不符。
4. **人物基础字段覆盖不全**：birth 只 3,354 人、性别 17,000 空/待定；resolution_candidates 含 9,758 条疑似重复；另有 persons 实体未全面核实。
5. **清洗/核实**：quality_issues 425 条（含 47 error：profile_missing_name 阻断 release）；resolution_candidates 9,758 需人工/自动复核。
6. **授权（Gold/Gold commercial）为空**：rights_manifests / source_rights_decisions / commercial_use 全 0 → 无法商用导出（除非逐来源清理授权）。
7. 历史脏文件名（永泰、阳曲等 <30 条）与 data/.trash_batch（约 31 个旧 stage 副本）待清理。

---

## 附：核查命令
```bash
python3 scripts/inventory.py
python3 scripts/govdb.py audit --database data/platform/gov_relation.db
python3 scripts/govdb.py release-check --database data/platform/gov_relation.db
python3 scripts/todo_queue.py status
python3 scripts/process_tmp.py data/tmp/<task_id>   # （dry-run 先）
```