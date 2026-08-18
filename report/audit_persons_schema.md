# data/persons/ 个人档案 JSON 模式与命名一致性审计报告

**审计方式**：全量只读扫描 /Users/x/Desktop/gov-relation/data/persons/（6633 个 JSON），逐一解析 + 关键字段全局 grep。仅本报告为唯一写入，数据文件未改动。

## 0. 执行摘要
- 目录实际共 **6633** 个合法 JSON（glob 与 ls 一致；任务中提到的 6850 inventory 与实际不符，以本 glob 为准）。
- **5865 / 6633（88.4%）** 严格符合 reference/person_graph_json.md 的 16 键规范 schema。
- 全目录存在 **110 种不同的顶层键组合**；768 个文件偏离规范，203 个文件含规范之外的新增键。
- 字段命名高度不一致（current_status/current_role/current_position/current_post；relationship_* 十余种写法等）。
- 文件名：303 个属段数/地区/占位异常，430 个文件名含占位符。

## 1. 抽样文件与顶层字段
### 变体 A —— 规范 v1.0（5865 文件，88.4%）
代表：`data/persons/20260807-河南省-周口市-扶沟县-县委书记-李祥生.json`、`20260715-安徽省-合肥市-市委书记-张红文.json`、`20240325-福建省-福州市-原县委书记-肖华.json`、`20260724-湖北省-宜昌市-市委常委-宣传部部长-市总工会主席-阮晓阳.json`。
16 键：`schema_version`(1.0), `generated_at`, `investigation_scope`(province/city/region/job/task_id/time_focus), `identity`(person_id/name/aliases/gender/ethnicity/birth/birthplace/native_place/education/party_join/work_start/dedupe_keys), `current_status`(current_post/current_org/administrative_rank/as_of/is_current_confirmed/source_ids), `career_timeline`, `organizations`, `relationships`, `governance_record`, `professional_profile`, `work_style_and_personality`, `network_metrics`, `risk_and_integrity_signals`, `source_register`, `confidence_summary`, `open_questions`。
### 变体 B —— 规范子集/精简
`20260715-安徽省-六安市-区委书记-董永来.json`(15 键,280 文件，缺 network_metrics)；`20260726-吉林省-延边朝鲜族自治州-副市长-吕智梁.json`(185 文件，缺 schema_version+investigation_scope)。
### 变体 C —— 关系/来源/置信度重命名
`20260724-河南省-新乡市-前任市委书记-刘军伟.json`：`career_timeline|confidence|governance_profile|identity|investigation_date|open_questions|relationship_network|source_register`(36 文件)。
### 变体 D —— 独立 schema（北京东城）
`data/persons/20260716-beijing-dongcheng-sunxinjun.json`（188 行,13 键）：`current_role`, `professional_title`, `career_gaps`, `governance_profile`, `risk_integrity_signals`(对象), `relationship_leads`, `sources`, `overall_confidence` —— 全部偏离规范键。
### 变体 E —— 极简 person/basic_info
`20260724-河北省张家口市赤城县-县委书记-邓艳杰.json`(40 行)：`task_id,date,person,career_timeline,key_events,sources(字符串数组),gaps`。`20260716-永泰-福州-代县长-林吓清.json`：`task_id,date,name,pinyin,current_post,basic_info,career_timeline,other_positions,sources,gaps`。`20260726-泸州-纳溪-区长-张毅.json`：`name,id,government_url,baike_url,basic_info,career(非career_timeline),sources,data_collected,gaps`。`20260726-阳曲县-县委书记-姬发军.json`：`person,career_timeline(period/position),relationships,analysis`。
### 变体 F —— 扁平原生字段
`20260726-四川省-珙县-副县长-谢建文.json`、`20260803-黑龙江省-齐齐哈尔市-区长-孙坤.json`：顶层直接 birth/birthplace/gender/... + `career`/`career_entries`/`positions`。

## 2. Schema 变体频率
| 形态 | 文件数 | 占比 |
|---|---|---|
| 精确 16 键（规范） | 5865 | 88.4% |
| 规范子集（仅缺键） | ~6430 | 97% |
| 含≥1 非规范新增键 | 203 | 3.1% |
| 非规范（非 exact） | 768 | 11.6% |
全目录不同的顶层键组合数=110。

## 3. 字段名不一致（同概念→异键）与计数
| 概念 | 规范键 | 变体键（出现文件数） |
|---|---|---|
| 当前职务 | current_status | current_role(1) / current_position(18) / current_post(28 顶层) |
| 履历 | career_timeline | career(3) / career_entries(2) / positions(11) / _relationship_raw 等 |
| 关系 | relationships | relationship_network(42) / relationship_leads(1) / relationships_list(2) / key_relationships(8) / key_connections(3) / known_connections(8) / relationship_evidence(4) / political_network(3) / relationship_clusters(3) / confirmed_connections(1) / _relationship_raw(4) |
| governance | governance_record | governance_profile(70) / government_record(6) / governance(1) / governance_notes(1) |
| 来源 | source_register | sources(69) / source_urls(2) / source(16) / source_url(2) / government_url(2) / baike_url(2) |
| 置信度 | confidence_summary | confidence(73) / overall_confidence(1) / confidence_assessment(8) / confidence_overall(3) |
| 风险 | risk_and_integrity_signals | risk_integrity_signals(1) / risk_and_liability_signals(1) |
| 身份 | identity | person(17 顶层) / basic_info(6) / basic(1) / 扁平展开 |
| 出生 | identity.birth | birth_date(2) / 顶层 birth |
| 缺口 | open_questions | gaps(8) / career_gaps(2) / open_gaps(3) / career_timeline_gaps(2) |

## 4. 文件名格式一致性
- 全部 6633 均以 8 位日期开头且为合法 JSON。
- 日期后段数：4=6330(规范)；3=23；5=242；6=32；7=5；8=1 → 偏离 **303**(4.6%)。
- 省位异常 8 类：`beijing`(1,小写), `永泰`(3), `河北省张家口市赤城县`(3,省+市+县), `泸州`(2), `阳曲县`(2), `洛阳市`(1), `四川省乐山市`(1), `浙江省台州市`(1)。
- 文件名含占位符的 **430** 个：如 `20260715-安徽省-淮北市-区长-待确认.json`、`20260724-河南省-周口市-unknown_县委书记.json`、`20260717-福建省-龙岩-武平县领导（待确认具体职务）-练良祥.json`、`20260725-宁夏-银川-区长-（待确认-区长姓名）.json`。

## 5. 缺失段 / 确认字段 / 来源
### 5.1 缺失必备段（跨变体合并键）
| 段 | 缺失文件数 |
|---|---|
| source_register/sources 空 | 377 |
| career 容器空 | 368 |
| organizations 空 | 1932 |
| relationships 空(合并关系键) | 1633 |
| governance_record/profile 空 | 4092 |
| identity.gender 空 | 1062 |
| identity.birth 空/unknown | 3601 |
### 5.2 确认/未验证/confidence
- 3981 文件含“确认”（多为 source_register/relationship 证据，如李祥生 L201 `"notes":"确认其此前为县长"`）。
- 27 文件含“未验证”。
- confidence 取值：`confirmed`(29458)/`unverified`(8254)/`plausible`(7207) 为主；**域泄漏** `medium/high/low/weak`(强度值误写)；自定义扩展 `_full_career_timeline/name_only/partial/推定/(名单)`；**拼错** `confiremed`(1)；自由文本 `低 — 职务确认，履历待查`。
- confidence_summary.identity 取值也不统一（confirmed/partial/unverified）。
### 5.3 来源模式
- 规范：`source_register:[{id:S001,url,publisher,published_at,accessed_at,source_type,reliability,notes}]` + `career_timeline[*].source_ids:[S001]` 回链。
- 变体：`sources` 为字符串 URL 数组（无 id/类型，无法回链）；或 `{type,url,confidence}`；或单值 `source_url`/`government_url`/`baike_url`。

## 6. Top-3 标准化修复建议
1. **键级校验 + 别名归一（影响 768 文件，11.6%）**：用 `gov_relation.platform` 对 6633 文件跑 16 键子集白名单；建别名映射表（relationship_network→relationships、governance_profile→governance_record、current_position/current_post→current_status、sources/source_urls→source_register、confidence/confidence_overall→confidence_summary...）逐一归并；把 110 种组合收敛为规范 16 键。
2. **文件名规范化（303 段数 + 8 区域 + 430 占位）**：强制 `YYYYMMDD-省-市-职-名` 5 段；把 8 类非规范区域前缀清洗为规范省（永泰→福建省福州市等）；430 处占位名（待查/待确认/unknown_）标记 UNRESOLVED 而非当作合法人名入库，避免污染去重/merge 键。
3. **补齐证据段 + confidence 值域约束**：confidence 收紧为 {confirmed,plausible,unverified}，拦截/映射 24 类非法值（confiremed/partial/medium/high/low/自由文本）；对缺失 governance_record(4092)、relationships(1633)、birth(3601)、gender(1062)、sources(377)、career(368) 的文件标记“待补证据”并入 open_gaps，勿以空数组充数。

## 附件
- 本报告：`report/audit_persons_schema.md`（唯一写入；临时分析脚本已全部删除；`data/persons/` 保持只读）。