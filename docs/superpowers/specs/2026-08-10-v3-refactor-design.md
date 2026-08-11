# Gov-Relation v3 全量重整设计

2026-08-10 · spec · 谢明

> **修订注记(2026-08-11,SubAgentReview 后同步):** §4.5 / §9.2 / §11 已就地标注与落地实现的差异,行为以实现与对应 Phase 计划为准(此 spec 保留原设计描述作为演进记录)。审查报告见 `docs/superpowers/reviews/2026-08-11-review-*.md`。

## 1. 目标与范围

将当前两阶段(区域简表 → 平台导入)的松散流水线收敛为**统一 schema + factory 生成 + 按省份分区**的生产级数据平台。

### 范围

- **Schema**:统一为 v3 规范(20 张实体表 + 6 个 Gold View),覆盖实体、溯源、质量、版权四域
- **代码**:引入 `gov_relation/factory/` 工厂层,统一生成 build 脚本、schema DDL、upsert 代码、GEXF、person JSON、report 模板
- **目录**:按省份分区 `data/provinces/<province>/`,每省自含 build/database/graph/persons/reports
- **存储**:单文件 SQLite 部署,本地嵌入式,无 PostgreSQL 依赖
- **迁移**:分 5 阶段渐进迁移,不破坏存量 2000+ DB 和 6000+ 人物档案

### 不在范围

- PostgreSQL 生产部署(schema 保留 PG 兼容性,但不实施)
- 前端 UI 重构
- OpenCode worker 调度逻辑改动
- GEXF 可视化风格变更

---

## 2. 业务需求

```
┌──────────────────────────────────────────────────────────┐
│                    政府人员关系调研系统                      │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  1. 任务管理域 (Task Domain)                              │
│     ─ 全国行政区划 → 调研任务 → 分派 → 完成                │
│                                                          │
│  2. 调研生产域 (Research Domain)                          │
│     ─ 人物调查 → 履历采集 → 关系发现 → 证据留存            │
│                                                          │
│  3. 实体存储域 (Entity Domain)  ← 核心                    │
│     ─ Person / Organization / Position / Relationship    │
│                                                          │
│  4. 溯源审计域 (Provenance Domain)                        │
│     ─ Source → Evidence → Claim → Quality                │
│                                                          │
│  5. 版权授权域 (Rights Domain)                            │
│     ─ Rights Manifest → Review Key → Source Decision     │
│                                                          │
│  6. 发布展示域 (Publish Domain)                           │
│     ─ GEXF 图 / Person JSON / Report / API               │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

六个域的关系:任务管理驱动调研生产 → 生产产出写入实体存储(附溯源)→ 版权授权决定哪些可发布 → 发布展示消费授权后的数据。

---

## 3. 领域实体 ER

```
                    ┌──────────────────────┐
                    │     Jurisdiction      │  行政区划
                    │  (省/市/区县 层级树)    │
                    └──────┬───────────────┘
                           │ belongs to
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
┌──────────────────┐  ┌─────────────┐  ┌──────────────┐
│   Organization   │  │   Person    │  │   Dataset    │
│   组织机构        │  │   人员       │  │  来源数据集    │
└────┬─────────────┘  └──────┬──────┘  └──────┬───────┘
     │ 1:N                   │ 1:N            │ 1:N
     ▼                       ▼                ▼
┌──────────────┐    ┌──────────────┐  ┌──────────────┐
│   Position   │    │   Profile    │  │  RawRecord   │
│   任职记录     │    │  人物深度档案  │  │  原始记录      │
└──────────────┘    └──────────────┘  └──────┬───────┘
                                             │ 1:N
                    ┌────────────────────────┼──────────────┐
                    ▼                        ▼              ▼
           ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
           │ EvidenceLink │   │    Claim     │   │ QualityIssue │
           │  证据关联      │   │   事实陈述    │   │  质量问题      │
           └──────┬───────┘   └──────────────┘   └──────────────┘
                  │ N:1
                  ▼
           ┌──────────────┐
           │    Source    │  ← 1:1 ── SourceRightsDecision
           │   信息来源     │
           └──────────────┘

    ┌──────────────┐     ┌─────────────────┐
    │ Relationship │     │ResolutionCandidate│
    │  人员关系  ◄──N:M──►  实体合并候选       │
    └──────────────┘     └─────────────────┘

    ┌──────────────────┐   ┌───────────────────┐
    │ RightsManifest   │──►│ RightsReviewKey   │
    │ 版权授权清单       │   │ 审核签名公钥        │
    └──────────────────┘   └───────────────────┘
```

| 关系 | 基数 | 说明 |
|------|------|------|
| Person → Position | 1:N | 一个人有多个任职记录 |
| Organization → Position | 1:N | 一个组织有多人在此任职 |
| Person → Relationship | N:M | 关系表两端都指向 Person |
| Dataset → RawRecord | 1:N | 来源数据集有多条原始记录 |
| Source → EvidenceLink | 1:N | 一个来源可佐证多个实体 |
| EvidenceLink → (Person/Position/Relationship) | N:M | 多来源佐证同一事实 |
| ResolutionCandidate | N:2 | 每行指向两个待合并 Person |
| Source → SourceRightsDecision | 1:N | 时间维度(有效区间) |

---

## 4. 完整 Schema(21 表 + 6 Gold Views)

### 4.1 实体域

```sql
-- 行政区划
CREATE TABLE jurisdictions (
    jurisdiction_id   TEXT PRIMARY KEY,
    parent_id         TEXT REFERENCES jurisdictions(jurisdiction_id),
    name              TEXT NOT NULL,
    normalized_name   TEXT NOT NULL,
    administrative_code TEXT NOT NULL DEFAULT '',
    level             TEXT NOT NULL DEFAULT 'unknown'
                       CHECK (level IN ('province','prefecture','county','town','unknown')),
    province_name     TEXT NOT NULL DEFAULT '',
    prefecture_name   TEXT NOT NULL DEFAULT '',
    county_name       TEXT NOT NULL DEFAULT '',
    valid_from        TEXT,
    valid_to          TEXT,
    UNIQUE (parent_id, normalized_name, level)
);

-- 人员
CREATE TABLE persons (
    person_id       TEXT PRIMARY KEY,
    canonical_name  TEXT NOT NULL,
    normalized_name TEXT NOT NULL,
    gender          TEXT NOT NULL DEFAULT '',
    ethnicity       TEXT NOT NULL DEFAULT '',
    birth_text      TEXT NOT NULL DEFAULT '',
    birth_precision TEXT NOT NULL DEFAULT 'unknown'
                     CHECK (birth_precision IN ('day','month','year','unknown')),
    birthplace      TEXT NOT NULL DEFAULT '',
    native_place    TEXT NOT NULL DEFAULT '',
    education       TEXT NOT NULL DEFAULT '',
    party_join_text TEXT NOT NULL DEFAULT '',
    work_start_text TEXT NOT NULL DEFAULT '',
    identity_status TEXT NOT NULL DEFAULT 'unresolved'
                     CHECK (identity_status IN ('verified','probable','unresolved','merged')),
    merged_into_id  TEXT REFERENCES persons(person_id),
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE person_aliases (
    person_id       TEXT NOT NULL REFERENCES persons(person_id),
    alias           TEXT NOT NULL,
    normalized_alias TEXT NOT NULL,
    alias_type      TEXT NOT NULL DEFAULT 'other',
    PRIMARY KEY (person_id, normalized_alias)
);

-- 组织机构
CREATE TABLE organizations (
    organization_id        TEXT PRIMARY KEY,
    jurisdiction_id        TEXT REFERENCES jurisdictions(jurisdiction_id),
    parent_organization_id TEXT REFERENCES organizations(organization_id),
    canonical_name         TEXT NOT NULL,
    normalized_name        TEXT NOT NULL,
    organization_type      TEXT NOT NULL DEFAULT '',
    administrative_level   TEXT NOT NULL DEFAULT '',
    location_text          TEXT NOT NULL DEFAULT '',
    valid_from             TEXT,
    valid_to               TEXT,
    created_at             TEXT NOT NULL DEFAULT (datetime('now'))
);

-- 任职
CREATE TABLE positions (
    position_id       TEXT PRIMARY KEY,
    person_id         TEXT NOT NULL REFERENCES persons(person_id),
    organization_id   TEXT REFERENCES organizations(organization_id),
    organization_text TEXT NOT NULL DEFAULT '',
    title             TEXT NOT NULL DEFAULT '',
    title_category    TEXT NOT NULL DEFAULT '',
    rank              TEXT NOT NULL DEFAULT '',
    start_text        TEXT NOT NULL DEFAULT '',
    end_text          TEXT NOT NULL DEFAULT '',
    start_date        TEXT,
    end_date          TEXT,
    date_precision    TEXT NOT NULL DEFAULT 'unknown'
                       CHECK (date_precision IN ('day','month','year','range','unknown')),
    is_current        INTEGER NOT NULL DEFAULT 0 CHECK (is_current IN (0,1)),
    sort_order        INTEGER NOT NULL DEFAULT 0,
    confidence        TEXT NOT NULL DEFAULT 'unverified'
                       CHECK (confidence IN ('confirmed','plausible','unverified')),
    notes             TEXT NOT NULL DEFAULT ''
);

-- 关系
CREATE TABLE relationships (
    relationship_id          TEXT PRIMARY KEY,
    person_from_id           TEXT NOT NULL REFERENCES persons(person_id),
    person_to_id             TEXT NOT NULL REFERENCES persons(person_id),
    relationship_type        TEXT NOT NULL DEFAULT 'other',
    direction                TEXT NOT NULL DEFAULT 'undirected'
                              CHECK (direction IN ('undirected','from_to','to_from')),
    strength                 TEXT NOT NULL DEFAULT 'unknown'
                              CHECK (strength IN ('strong','medium','weak','unknown')),
    confidence               TEXT NOT NULL DEFAULT 'unverified'
                              CHECK (confidence IN ('confirmed','plausible','unverified')),
    context                  TEXT NOT NULL DEFAULT '',
    evidence_summary         TEXT NOT NULL DEFAULT '',
    overlap_organization_id  TEXT REFERENCES organizations(organization_id),
    overlap_organization_text TEXT NOT NULL DEFAULT '',
    overlap_period_text      TEXT NOT NULL DEFAULT '',
    valid_from               TEXT,
    valid_to                 TEXT,
    CHECK (person_from_id <> person_to_id)
);

-- 现任状态
CREATE TABLE person_statuses (
    status_id            TEXT PRIMARY KEY,
    person_id            TEXT NOT NULL REFERENCES persons(person_id),
    post_text            TEXT NOT NULL DEFAULT '',
    organization_text    TEXT NOT NULL DEFAULT '',
    administrative_rank  TEXT NOT NULL DEFAULT '',
    observed_at          TEXT,
    is_current_confirmed INTEGER NOT NULL DEFAULT 0 CHECK (is_current_confirmed IN (0,1)),
    confidence           TEXT NOT NULL DEFAULT 'unverified'
                          CHECK (confidence IN ('confirmed','plausible','unverified'))
);
```

### 4.2 溯源审计域

```sql
CREATE TABLE datasets (
    dataset_id      TEXT PRIMARY KEY,
    dataset_key     TEXT NOT NULL UNIQUE,
    name            TEXT NOT NULL,
    kind            TEXT NOT NULL CHECK (kind IN ('legacy_sqlite','person_profile','research_package','manual')),
    source_path     TEXT NOT NULL,
    jurisdiction_id TEXT REFERENCES jurisdictions(jurisdiction_id),
    content_sha256  TEXT NOT NULL,
    rights_status   TEXT NOT NULL DEFAULT 'unknown' CHECK (rights_status IN ('unknown','cleared','restricted')),
    commercial_use  INTEGER NOT NULL DEFAULT 0 CHECK (commercial_use IN (0,1)),
    imported_at     TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE raw_records (
    raw_record_id  TEXT PRIMARY KEY,
    dataset_id     TEXT NOT NULL REFERENCES datasets(dataset_id),
    source_table   TEXT NOT NULL,
    source_pk      TEXT NOT NULL,
    payload_json   TEXT NOT NULL,
    payload_sha256 TEXT NOT NULL,
    imported_at    TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (dataset_id, source_table, source_pk)
);

CREATE TABLE profile_documents (
    profile_id     TEXT PRIMARY KEY,
    person_id      TEXT NOT NULL REFERENCES persons(person_id),
    raw_record_id  TEXT NOT NULL REFERENCES raw_records(raw_record_id),
    schema_version TEXT NOT NULL DEFAULT '',
    generated_at   TEXT NOT NULL DEFAULT '',
    profile_json   TEXT NOT NULL
);

CREATE TABLE sources (
    source_id      TEXT PRIMARY KEY,
    canonical_url  TEXT NOT NULL DEFAULT '',
    title          TEXT NOT NULL DEFAULT '',
    publisher      TEXT NOT NULL DEFAULT '',
    published_at   TEXT,
    accessed_at    TEXT,
    source_type    TEXT NOT NULL DEFAULT 'other'
                    CHECK (source_type IN ('official','appointment_notice','media','encyclopedia','database','inferred','other')),
    reliability    TEXT NOT NULL DEFAULT 'low' CHECK (reliability IN ('high','medium','low')),
    rights_status  TEXT NOT NULL DEFAULT 'unknown' CHECK (rights_status IN ('unknown','cleared','restricted')),
    commercial_use INTEGER NOT NULL DEFAULT 0 CHECK (commercial_use IN (0,1)),
    content_sha256 TEXT NOT NULL DEFAULT ''
);

CREATE TABLE evidence_links (
    evidence_id   TEXT PRIMARY KEY,
    source_id     TEXT NOT NULL REFERENCES sources(source_id),
    subject_type  TEXT NOT NULL,
    subject_id    TEXT NOT NULL,
    field_name    TEXT NOT NULL DEFAULT '',
    claim_text    TEXT NOT NULL DEFAULT '',
    locator       TEXT NOT NULL DEFAULT '',
    confidence    TEXT NOT NULL DEFAULT 'unverified' CHECK (confidence IN ('confirmed','plausible','unverified')),
    UNIQUE (source_id, subject_type, subject_id, field_name, locator)
);

CREATE TABLE claims (
    claim_id      TEXT PRIMARY KEY,
    subject_type  TEXT NOT NULL,
    subject_id    TEXT NOT NULL,
    predicate     TEXT NOT NULL,
    value_json    TEXT NOT NULL,
    valid_from    TEXT,
    valid_to      TEXT,
    observed_at   TEXT,
    confidence    TEXT NOT NULL DEFAULT 'unverified' CHECK (confidence IN ('confirmed','plausible','unverified')),
    review_status TEXT NOT NULL DEFAULT 'pending' CHECK (review_status IN ('pending','accepted','rejected','superseded'))
);

CREATE TABLE entity_provenance (
    provenance_id   TEXT PRIMARY KEY,
    dataset_id      TEXT NOT NULL REFERENCES datasets(dataset_id),
    raw_record_id   TEXT REFERENCES raw_records(raw_record_id),
    entity_type     TEXT NOT NULL,
    entity_id       TEXT NOT NULL,
    source_field    TEXT NOT NULL DEFAULT '',
    transformation  TEXT NOT NULL DEFAULT '',
    UNIQUE (dataset_id, raw_record_id, entity_type, entity_id, source_field)
);

CREATE TABLE quality_issues (
    issue_id      TEXT PRIMARY KEY,
    dataset_id    TEXT REFERENCES datasets(dataset_id),
    raw_record_id TEXT REFERENCES raw_records(raw_record_id),
    severity      TEXT NOT NULL CHECK (severity IN ('error','warning','info')),
    issue_code    TEXT NOT NULL,
    entity_type   TEXT NOT NULL DEFAULT '',
    entity_id     TEXT NOT NULL DEFAULT '',
    message       TEXT NOT NULL,
    status        TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open','resolved','ignored')),
    created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE resolution_candidates (
    candidate_id    TEXT PRIMARY KEY,
    left_entity_id  TEXT NOT NULL,
    right_entity_id TEXT NOT NULL,
    entity_type     TEXT NOT NULL,
    score           REAL NOT NULL CHECK (score >= 0 AND score <= 1),
    reasons_json    TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','merged','rejected')),
    UNIQUE (left_entity_id, right_entity_id, entity_type)
);
```

### 4.3 版权授权域

```sql
CREATE TABLE rights_review_keys (
    key_id            TEXT PRIMARY KEY,
    algorithm         TEXT NOT NULL CHECK (algorithm = 'ecdsa-p256-sha256'),
    public_key_pem    TEXT NOT NULL,
    reviewer_identity TEXT NOT NULL,
    review_authority  TEXT NOT NULL,
    status            TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active','revoked')),
    valid_from        TEXT NOT NULL,
    valid_to          TEXT,
    created_at        TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE rights_manifests (
    manifest_id         TEXT PRIMARY KEY,
    schema_version      TEXT NOT NULL,
    payload_sha256      TEXT NOT NULL,
    signature_algorithm TEXT NOT NULL,
    signature_key_id    TEXT NOT NULL,
    signature_base64    TEXT NOT NULL,
    created_at          TEXT NOT NULL,
    reviewed_by         TEXT NOT NULL,
    review_authority    TEXT NOT NULL,
    legal_memo_ref      TEXT NOT NULL DEFAULT '',
    effective_from      TEXT NOT NULL,
    effective_to        TEXT,
    applied_at          TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE source_rights_decisions (
    decision_row_id      TEXT PRIMARY KEY,
    decision_id          TEXT NOT NULL,
    manifest_id          TEXT NOT NULL REFERENCES rights_manifests(manifest_id),
    source_id            TEXT NOT NULL REFERENCES sources(source_id),
    decision             TEXT NOT NULL CHECK (decision IN ('unknown','cleared','restricted')),
    permitted_uses_json  TEXT NOT NULL,
    permitted_fields_json TEXT NOT NULL,
    restrictions_json    TEXT NOT NULL,
    rationale            TEXT NOT NULL,
    effective_from       TEXT NOT NULL,
    effective_to         TEXT,
    UNIQUE (manifest_id, decision_id, source_id)
);
```

### 4.4 元数据

```sql
CREATE TABLE schema_meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE ingest_runs (
    run_id         TEXT PRIMARY KEY,
    started_at     TEXT NOT NULL,
    finished_at    TEXT,
    mode           TEXT NOT NULL,
    status         TEXT NOT NULL CHECK (status IN ('running','succeeded','failed','partial')),
    input_count    INTEGER NOT NULL DEFAULT 0,
    imported_count INTEGER NOT NULL DEFAULT 0,
    rejected_count INTEGER NOT NULL DEFAULT 0,
    error          TEXT NOT NULL DEFAULT ''
);
```

### 4.5 Gold Views

```sql
CREATE VIEW gold_current_positions AS
SELECT p.person_id, p.canonical_name, ps.post_text AS title, ps.organization_text AS organization_name,
       ps.administrative_rank AS rank, ps.confidence
FROM person_statuses ps
JOIN persons p ON p.person_id = ps.person_id
WHERE ps.is_current_confirmed = 1;

> **2026-08-11 审查同步:** 已实现视图改为 `FROM positions ps … LEFT JOIN organizations … WHERE ps.is_current=1`(含 `start_text/end_text`,不含 administrative_rank)。`person_statuses` 在 v3 中保留为实体表,但不再是本视图的数据源(GEXFFactory 内仍作兜底引用)。下游如需与之对齐,以 `gov_relation/factory/schema_factory.py` 的 DDL 为准。

CREATE VIEW gold_relationship_edges AS
SELECT r.relationship_id, a.canonical_name AS person_from, b.canonical_name AS person_to,
       r.relationship_type, r.direction, r.strength, r.confidence,
       r.context, r.overlap_period_text
FROM relationships r
JOIN persons a ON a.person_id = r.person_from_id
JOIN persons b ON b.person_id = r.person_to_id;

CREATE VIEW gold_commercial_sources AS
SELECT s.* FROM sources s
JOIN source_rights_decisions d ON d.source_id = s.source_id
WHERE d.decision = 'cleared'
  AND instr(d.permitted_uses_json, '"commercial_distribution"') > 0
  AND datetime(d.effective_from) <= CURRENT_TIMESTAMP
  AND (d.effective_to IS NULL OR datetime(d.effective_to) >= CURRENT_TIMESTAMP)
  AND d.rowid = (
      SELECT d2.rowid FROM source_rights_decisions d2
      WHERE d2.source_id = s.source_id
        AND datetime(d2.effective_from) <= CURRENT_TIMESTAMP
        AND (d2.effective_to IS NULL OR datetime(d2.effective_to) >= CURRENT_TIMESTAMP)
      ORDER BY datetime(d2.effective_from) DESC, d2.rowid DESC LIMIT 1
  );

CREATE VIEW gold_commercial_persons AS
SELECT DISTINCT p.* FROM persons p
JOIN evidence_links e ON e.subject_type = 'person' AND e.subject_id = p.person_id
JOIN gold_commercial_sources s ON s.source_id = e.source_id;

CREATE VIEW gold_commercial_positions AS
SELECT DISTINCT p.* FROM positions p
JOIN evidence_links e ON e.subject_type = 'position' AND e.subject_id = p.position_id
JOIN gold_commercial_sources s ON s.source_id = e.source_id;

CREATE VIEW gold_commercial_relationships AS
SELECT DISTINCT r.* FROM relationships r
JOIN evidence_links e ON e.subject_type = 'relationship' AND e.subject_id = r.relationship_id
JOIN gold_commercial_sources s ON s.source_id = e.source_id;
```

---

## 5. 约束总览

| 表 | PK | FK | UNIQUE | CHECK |
|----|----|----|--------|-------|
| jurisdictions | jurisdiction_id | parent_id → jurisdictions | (parent_id, normalized_name, level) | level |
| persons | person_id | merged_into_id → persons | - | birth_precision, identity_status |
| person_aliases | (person_id, normalized_alias) | person_id → persons | - | - |
| organizations | organization_id | jurisdiction_id, parent_organization_id | - | - |
| positions | position_id | person_id → persons, organization_id → orgs | - | date_precision, is_current, confidence |
| relationships | relationship_id | person_from_id/to_id → persons, overlap_organization_id → orgs | - | person_from_id <> person_to_id, direction, strength, confidence |
| person_statuses | status_id | person_id → persons | - | is_current_confirmed, confidence |
| datasets | dataset_id | jurisdiction_id | dataset_key | kind, rights_status, commercial_use |
| raw_records | raw_record_id | dataset_id → datasets | (dataset_id, source_table, source_pk) | - |
| profile_documents | profile_id | person_id → persons, raw_record_id → raw_records | - | - |
| sources | source_id | - | - | source_type, reliability, rights_status, commercial_use |
| evidence_links | evidence_id | source_id → sources | (source_id, subject_type, subject_id, field_name, locator) | confidence |
| claims | claim_id | - | - | confidence, review_status |
| entity_provenance | provenance_id | dataset_id, raw_record_id | (dataset_id, raw_record_id, entity_type, entity_id, source_field) | - |
| quality_issues | issue_id | dataset_id, raw_record_id | - | severity, status |
| resolution_candidates | candidate_id | - | (left_entity_id, right_entity_id, entity_type) | score [0,1], status |
| rights_review_keys | key_id | - | - | algorithm, status |
| rights_manifests | manifest_id | - | - | - |
| source_rights_decisions | decision_row_id | manifest_id, source_id | (manifest_id, decision_id, source_id) | decision |
| schema_meta | key | - | - | - |
| ingest_runs | run_id | - | - | status |

---

## 6. 索引

```sql
-- 核心查询路径
CREATE INDEX idx_persons_normalized_name ON persons(normalized_name);
CREATE INDEX idx_positions_person_time ON positions(person_id, sort_order, start_date);
CREATE INDEX idx_positions_org ON positions(organization_id, is_current);
CREATE INDEX idx_positions_dates ON positions(start_date, end_date);
CREATE INDEX idx_relationships_from ON relationships(person_from_id);
CREATE INDEX idx_relationships_to ON relationships(person_to_id);
CREATE INDEX idx_relationships_overlap_org ON relationships(overlap_organization_id);
CREATE INDEX idx_statuses_person ON person_statuses(person_id);

-- Evidence / Provenance
CREATE INDEX idx_sources_url ON sources(canonical_url);
CREATE INDEX idx_evidence_subject ON evidence_links(subject_type, subject_id);
CREATE INDEX idx_evidence_source ON evidence_links(source_id);
CREATE INDEX idx_provenance_dataset ON entity_provenance(dataset_id);
CREATE INDEX idx_provenance_entity ON entity_provenance(entity_type, entity_id);

-- Quality / Audit
CREATE INDEX idx_quality_status ON quality_issues(status, severity, issue_code);
CREATE INDEX idx_quality_dataset ON quality_issues(dataset_id);

-- Rights
CREATE INDEX idx_rights_decisions_source_time
    ON source_rights_decisions(source_id, effective_from, effective_to);

-- Jurisdiction / Organization
CREATE INDEX idx_jurisdictions_parent ON jurisdictions(parent_id);
CREATE INDEX idx_jurisdictions_level ON jurisdictions(province_name, level);
CREATE INDEX idx_orgs_jurisdiction ON organizations(jurisdiction_id);
CREATE INDEX idx_orgs_normalized_name ON organizations(normalized_name);

-- Datasets
CREATE INDEX idx_datasets_jurisdiction ON datasets(jurisdiction_id);
```

---

## 7. 典型 SQL

### Q1: 单人物完整履历 + 来源
```sql
SELECT p.title, o.canonical_name AS org, p.start_text, p.end_text,
       s.title AS source_title, s.canonical_url
FROM positions p
LEFT JOIN organizations o ON o.organization_id = p.organization_id
LEFT JOIN evidence_links e ON e.subject_type='position' AND e.subject_id=p.position_id
LEFT JOIN sources s ON s.source_id = e.source_id
WHERE p.person_id = ?
ORDER BY p.sort_order;
```

### Q2: 两人之间所有关系路径
```sql
SELECT r.relationship_type, r.context, r.overlap_period_text,
       a.canonical_name AS person_a, b.canonical_name AS person_b
FROM relationships r
JOIN persons a ON a.person_id = r.person_from_id
JOIN persons b ON b.person_id = r.person_to_id
WHERE (r.person_from_id = ? AND r.person_to_id = ?)
   OR (r.person_from_id = ? AND r.person_to_id = ?);
```

### Q3: 某组织当前任职人员(Gold View)
```sql
SELECT canonical_name, title, rank, confidence
FROM gold_current_positions
WHERE organization_name LIKE ?
ORDER BY rank;
```

### Q4: 按省份 + 职务分类统计
```sql
SELECT j.province_name, COUNT(DISTINCT p.person_id)
FROM persons p
JOIN positions pos ON pos.person_id = p.person_id
JOIN organizations o ON o.organization_id = pos.organization_id
JOIN jurisdictions j ON j.jurisdiction_id = o.jurisdiction_id
WHERE pos.is_current = 1 AND pos.title_category = ?
GROUP BY j.province_name;
```

### Q5: 待合并同名候选
```sql
SELECT rc.score, rc.reasons_json,
       l.canonical_name, l.birth_text,
       r.canonical_name, r.birth_text
FROM resolution_candidates rc
JOIN persons l ON l.person_id = rc.left_entity_id
JOIN persons r ON r.person_id = rc.right_entity_id
WHERE rc.entity_type = 'person' AND rc.status = 'pending'
ORDER BY rc.score DESC;
```

---

## 8. 反范式化

SQLite 单机环境下的 2 处反范式化:

| 位置 | 问题 | 方案 |
|------|------|------|
| `positions.organization_text` | 每次查履历都 join orgs,组织名变化少但查询量大 | 冗余组织名到 position 行,避免 N+1 join。`organization_id` 仍保留用于精确关联和分组统计 |
| `gold_current_positions` | 查现任领导需 3 表 join | 已是 View,无需额外反范式化。View 字段足以直接用于 API 响应 |

---

## 9. Factory 模式架构

### 9.1 工厂层级

```
RegionResearchFactory                         ← 统一入口
    │
    ├── SchemaFactory                         ← 生成 DDL
    ├── InsertFactory                         ← 生成 upsert / insert
    │       ├── 引用 identity.py (stable_id, person_key, normalize_text)
    │       └── 引用 schema.py (DDL 常量)
    ├── BuildScriptFactory                    ← 组装 → 生成 build_<slug>_data.py
    ├── GEXFFactory                           ← 调用 GEXFBuilder
    ├── PersonJSONFactory                     ← 生成人物深度图谱
    └── ReportFactory                         ← 生成调查骨架报告
```

### 9.2 核心接口

```python
class SchemaFactory:
    """统一 schema DDL 生成"""
    def create_all(self, conn: Connection) -> None
    def create_entity_tables(self, conn: Connection) -> None
    def create_evidence_tables(self, conn: Connection) -> None
    def create_meta_tables(self, conn: Connection) -> None

class InsertFactory:
    """参数化 upsert 代码"""
    def upsert_person(self, conn: Connection, data: dict) -> str          # → person_id
    def upsert_organization(self, conn: Connection, data: dict) -> str   # → organization_id
    def upsert_jurisdiction(self, conn: Connection, data: dict) -> str   # → jurisdiction_id
    def insert_position(self, conn: Connection, data: dict) -> str
    def insert_relationship(self, conn: Connection, data: dict) -> str
    def insert_source(self, conn: Connection, data: dict) -> str
    def link_evidence(self, conn: Connection, source_id: str, subject_type: str,
                       subject_id: str, field_name: str) -> None

class BuildScriptFactory:
    """组装完整构建脚本"""
    def generate(
        self,
        slug: str,
        province_dir: Path,
        persons: list[dict],
        organizations: list[dict],
        positions: list[dict],
        relationships: list[dict],
        sources: list[dict],
        claims: list[dict] | None = None,
    ) -> str   # 返回完整 .py 脚本内容

> **2026-08-11 审查同步:** 已实现为 keyword-only `generate(*, slug: str, province_name: str, persons, organizations, positions, relationships, sources, claims)`;生成脚本经 `gov_relation.runner.run_build(..., backend="v3")` 执行;仓库根由生成模板内的 `_repo_root()` 沿父目录链向上搜索 `gov_relation/` 定位(2026-08-11 F4 修复,不再硬编码 `parents[2]`)。


class GEXFFactory:
    """从 DB 查询生成 GEXF"""
    def build(self, conn: Connection, title: str) -> str   # GEXF XML string

class PersonJSONFactory:
    """生成单个人物深度图谱 JSON"""
    def build(self, conn: Connection, person_id: str) -> dict

class ReportFactory:
    """生成调查报告 Markdown 骨架"""
    def build(self, slug: str, stats: dict) -> str

class RegionResearchFactory:
    """顶层入口 - 协调所有子工厂"""
    def __init__(self, province: str, region: str, level: str, targets: list[dict])
    def generate_build_script(self) -> Path
    def generate_gexf(self) -> Path
    def generate_person_profiles(self) -> list[Path]
    def generate_report(self) -> Path
```

### 9.3 使用方式

```python
from gov_relation.factory import RegionResearchFactory

factory = RegionResearchFactory(
    province="四川省",
    region="成都市锦江区",
    level="county",
    targets=[{"role": "区委书记"}, {"role": "区长"}, {"role": "区委副书记"}],
)

# 生成 build 脚本 → data/provinces/sichuan/build/build_锦江区_data.py
factory.generate_build_script()

# build 脚本内部使用 InsertFactory:
#   factory.insert.upsert_person(conn, {"canonical_name": "张三", ...})
#   → 写入 data/provinces/sichuan/database/锦江区_network.db

# 生成 GEXF → data/provinces/sichuan/graph/锦江区_network.gexf
factory.generate_gexf()

# 生成人物 JSON → data/provinces/sichuan/persons/20260810-四川省-成都市-锦江区-区委书记-张三.json
factory.generate_person_profiles()
```

---

## 10. 目录结构

```
gov-relation/
├── CLAUDE.md
├── README.md
├── .gitignore
│
├── gov_relation/                          # 公共 Python 包
│   ├── __init__.py
│   ├── factory/                           # 【新】工厂层
│   │   ├── __init__.py
│   │   ├── schema_factory.py
│   │   ├── insert_factory.py
│   │   ├── build_factory.py
│   │   ├── gexf_factory.py
│   │   ├── person_factory.py
│   │   ├── report_factory.py
│   │   └── region_factory.py
│   ├── schema.py                          # 保留并升级到 v3
│   ├── identity.py                        # 保留
│   ├── gexf.py                            # 保留
│   ├── colors.py                          # 保留
│   ├── paths.py                           # 保留,新增 province 路径函数
│   ├── runner.py                          # 保留,底层调用 factory
│   ├── todo.py                            # 保留
│   ├── queue.py                           # 保留
│   ├── dispatch.py                        # 保留
│   ├── inventory.py                       # 保留
│   ├── web.py                             # 保留
│   ├── province.py                        # 保留
│   ├── slugs.py                           # 保留
│   ├── hash.py                            # 保留
│   └── log.py                             # 保留
│
├── data/
│   ├── TODO.json
│   ├── dispatch_state.json
│   ├── platform/                          # 平台统一 DB
│   │   └── gov_relation.db
│   │
│   ├── provinces/                         # 【新】按省份分区
│   │   ├── sichuan/
│   │   │   ├── build/                     #   build_<slug>_data.py
│   │   │   ├── database/                  #   <slug>_network.db
│   │   │   ├── graph/                     #   <slug>_network.gexf
│   │   │   ├── persons/                   #   YYYYMMDD-省-市-职务-姓名.json
│   │   │   └── reports/                   #   YYYYMMDD-地区-主题.md
│   │   ├── henan/
│   │   ├── shandong/
│   │   └── ... (31 个省份目录)
│   │
│   ├── database/                          # 【legacy】逐步迁移,保留只读
│   ├── graph/                             # 【legacy】
│   ├── persons/                           # 【legacy】
│   └── tmp/                               # 暂存区
│
├── scripts/
│   ├── govdb.py
│   ├── todo_queue.py
│   ├── dispatch_todo.py
│   ├── serve_app.py
│   ├── build_static_site_data.py
│   ├── inventory.py
│   ├── process_tmp.py
│   ├── migrate/                           # 【新】迁移脚本
│   │   ├── migrate_legacy_to_provinces.py
│   │   └── upgrade_schema_v2_to_v3.py
│   ├── build/                             # 【legacy】旧 build 脚本
│   └── tools/
│
├── tests/
│   ├── test_schema.py
│   ├── test_runner.py
│   ├── test_factory/                      # 【新】factory 测试
│   │   ├── test_schema_factory.py
│   │   ├── test_insert_factory.py
│   │   ├── test_build_factory.py
│   │   ├── test_gexf_factory.py
│   │   └── test_region_factory.py
│   └── ...
│
├── docs/
│   ├── superpowers/
│   │   └── specs/
│   │       └── 2026-08-10-v3-refactor-design.md
│   ├── ARCHITECTURE_V2.md
│   └── design/
│
├── report/                                # 【legacy】
├── config/
└── infra/
```

### paths.py 新增

```python
PROVINCES_DIR = DATA_DIR / "provinces"

# 省份名 → 目录 slug 映射(需新增,不在当前 REGION_SLUGS 中)
PROVINCE_SLUGS: dict[str, str] = {
    "四川省": "sichuan", "河南省": "henan", "山东省": "shandong",
    "云南省": "yunnan", "陕西省": "shaanxi", "辽宁省": "liaoning",
    # ... 31 个省份
}

def province_dir(province: str) -> Path:
    """省份中文名 → 省份根目录"""
    slug = PROVINCE_SLUGS.get(province, province)
    return PROVINCES_DIR / slug

def province_build_dir(province: str) -> Path:
    return province_dir(province) / "build"

def province_database_dir(province: str) -> Path:
    return province_dir(province) / "database"

def province_graph_dir(province: str) -> Path:
    return province_dir(province) / "graph"

def province_persons_dir(province: str) -> Path:
    return province_dir(province) / "persons"

def province_reports_dir(province: str) -> Path:
    return province_dir(province) / "reports"
```

### 外部数据合并

当前存在 `/workspace/data/xieming/other-codes/data/` 外部目录(736K),含 4 个数据库、5 个 GEXF 图、8 个 tmp 暂存目录。需要在迁移阶段并入仓库对应位置:

| 外部路径 | 目标位置 |
|----------|----------|
| `data/database/休宁县_network.db` | `data/database/休宁县_network.db`(legacy) |
| `data/database/昌宁县_network.db` | `data/database/昌宁县_network.db` |
| `data/database/松北区_network.db` | `data/database/松北区_network.db` |
| `data/database/黄山市_network.db` | `data/database/黄山市_network.db` |
| `data/graph/*.gexf` (5 files) | `data/graph/*.gexf`(legacy) |
| `data/tmp/*/` (8 dirs) | `data/tmp/*/` |
| `data/graph/赤城县_network.gexf` | `data/graph/赤城县_network.gexf`(注:只有 gexf 无对应 db) |

---

## 11. 迁移策略(5 阶段)

### Phase 1: Foundation(不影响现有系统)
- `gov_relation/factory/` 全部工厂类实现 + 测试通过
- `paths.py` 新增 province 路径函数
- `data/provinces/` 创建 31 省目录骨架 + `.gitkeep`

### Phase 2: Schema 升级

> **2026-08-11 审查同步: 本节方案已废弃**,以 `docs/superpowers/plans/2026-08-10-v3-phase2-schema-upgrade.md` Task 1 废弃声明与落地实现为准:v3 DDL 由 `gov_relation/factory/schema_factory.py` 统一提供(从 `platform/schema.py` DDL 派生 + v3 增量列);`gov_relation/schema.py` 保持 v1/v2 兼容不升级;`ADDITIVE_SCHEMA_UPGRADES` 维持空集,不塞入 2.1.0;upgrade 脚本仍做列级 ALTER + 补齐表/视图。

- ~~`gov_relation/schema.py` 升级到 v3 DDL(保留 v2 legacy 常量)~~(废弃,见上)
- `scripts/migrate/upgrade_schema_v2_to_v3.py` — 在现有 platform DB 上执行 **列级 ALTER**(v2 与 v3 表名相同,"CREATE IF NOT EXISTS" 对已有表是静默 no-op,必须 ALTER ADD COLUMN v3 增量列)+ 补齐缺失表/视图
- ~~同步升 `platform/schema.py` 的 `SCHEMA_VERSION` 至 3.0.0、`ADDITIVE_SCHEMA_UPGRADES` 纳入 2.1.0~~(废弃,保持空集;版本由 factory 的 `schema_version=3.0.0` 门禁体现)
- `govdb.py build` 仅做 `create_schema()` 版本门禁(不建 v3 factory 表)
- 验证:迁移脚本 dry-run → 真实执行 → 重建 platform DB → audit 零错误

### Phase 3: Migration
- `scripts/migrate/migrate_legacy_to_provinces.py` - 按 TODO.json province 映射分组,移入对应省份目录
- 合并外部 `/workspace/data/xieming/other-codes/data/` 到仓库
- `serve_app.py` / `inventory.py` 更新 scanners 同时读新旧路径
- 验证:inventory 数量一致,serve_app 正常

### Phase 4: 新流程上线
- `dispatch_todo.py` → 指定 province 路径给 worker
- `RegionResearchFactory` 对接 dispatch → 全自动生成
- `process_tmp.py` → 直接归档到 `data/provinces/` 目录
- `root legacy build_*.py` 标记 deprecated,新脚本一律输出到 `data/provinces/<province>/build/`
- 验证:端到端跑通一个新地区

### Phase 5: Cleanup(可选,低优先级)
- 删除 `gov_relation/central.py`(已被 factory + platform 覆盖)
- 清理 root legacy `build_*.py`(确认迁移后)
- 删除 `data/database/` `data/graph/` `data/persons/` legacy 目录(确认迁移后)

---

## 12. 核心设计原则

1. **保守实体解析**:只有 name + birth 都精确匹配时才合并;同名不同生日的绝不合并。存疑实体进入 `resolution_candidates`,不自动合并。宁可假分离也不假合并。
2. **不可变原始记录**:`raw_records.payload_json + payload_sha256` 提供完整溯源;`datasets.content_sha256` 检测源数据变更。
3. **Precision-preserving**:日期保留原始文本,`date_precision` 独立标记精度;不发明缺失的月日。
4. **Fail-closed 版权**:所有 source 默认 `rights_status='unknown'`、`commercial_use=0`;Gold views 只暴露版权已清理的数据。
5. **原子发布**:`govdb.py build` 先写 `.building` 临时文件,完成后 `os.replace()` 原子替换。
6. **文件锁并发**:`data/dispatch_state.lock/` 目录作为互斥锁,10 分钟超时自动失效。
7. **混合模式(C)**:新地区直接写统一 platform DB(通过 factory + insert factory),旧 DB 保留在 provinces/ 下作为独立可查询的数据库,同时可通过 `govdb.py build` 批量导入 platform。
