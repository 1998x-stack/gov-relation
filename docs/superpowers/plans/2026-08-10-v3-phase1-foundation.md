# Phase 1: Foundation — Factory Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现 `gov_relation/factory/` 全部 6 个工厂类 + 基础路径 + 测试，不影响现有系统。

**Architecture:** 6 个工厂类分层：底层 SchemaFactory（DDL 生成）和 InsertFactory（upsert 逻辑）被 BuildScriptFactory（脚本组装）、GEXFFactory、PersonJSONFactory、ReportFactory 调用；RegionResearchFactory 是统一入口。所有类通过 `gov_relation.identity` 模块获取 `stable_id`/`normalize_text`/`person_key`，通过 `gov_relation.paths` 获取省份路径。

**Spec:** `docs/superpowers/specs/2026-08-10-v3-refactor-design.md`
**Next Phase:** Phase 2 (Schema 升级 + govdb.py 切换)

## Global Constraints

- Python 3.11 stdlib only
- 所有实体 ID 通过 `stable_id(kind, key)` 生成（UUIDv5）
- 日期保留原始文本；`date_precision` 独立标记精度
- SQLite WAL + foreign_keys=ON + busy_timeout=5000
- 测试用 `tmp_path` fixture 隔离
- 提交：`feat(factory): ...` / `test(factory): ...`

---

### Task 1: 提升 identity.py 到 gov_relation 包

**Files:**
- Create: `gov_relation/identity.py`
- Modify: `gov_relation/platform/identity.py` (改为薄 re-export，保留原函数签名)
- Modify: `gov_relation/platform/importer.py:16-17`, `gov_relation/platform/resolution.py:10`, `scripts/govdb.py:17`, `tests/test_platform.py:9`

**Interfaces:**
- Produces: `normalize_text(value: object) -> str`, `stable_id(kind: str, key: str) -> str`, `sha256_bytes(value: bytes) -> str`, `date_precision(value: object) -> str`, `person_key(*, name, birth, dataset_key, source_pk) -> tuple[str, str]`, `organization_key(*, name, jurisdiction_key, dataset_key) -> str`

**Design（修复 C1F "move vs copy"）:** `gov_relation.identity` 是**唯一实现**；`gov_relation/platform/identity.py` 保留但改为**薄 re-export**（单行 `from gov_relation.identity import *`），避免两个实现漂移，也不破坏现有 4 处 import（`platform/importer.py`、`platform/resolution.py`、`scripts/govdb.py`、`tests/test_platform.py` 全部继续可解析）。后续新增代码统一走 `gov_relation.identity`。

- [ ] **Step 1: 复制核心函数到 gov_relation/identity.py（唯一实现源）**

```python
"""Conservative normalization and deterministic identifiers for gov-relation.

These functions are used by both the factory layer and the platform importer.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
import uuid

_NAMESPACE = uuid.UUID("99f1252f-a5e0-4d43-a4d5-087776ec44f8")
_DATE_YEAR = re.compile(r"^\d{4}年?$")
_DATE_MONTH = re.compile(r"^\d{4}(?:[-./]\d{1,2}|年\d{1,2}月)$")
_DATE_DAY = re.compile(r"^\d{4}(?:[-./]\d{1,2}[-./]\d{1,2}|年\d{1,2}月\d{1,2}日)$")


def normalize_text(value: object) -> str:
    """Return a stable NFKC value with all whitespace removed."""
    text = unicodedata.normalize("NFKC", str(value or "")).strip()
    return re.sub(r"\s+", "", text)


def stable_id(kind: str, key: str) -> str:
    """Return a readable deterministic UUIDv5 identifier."""
    return f"{kind}_{uuid.uuid5(_NAMESPACE, f'{kind}:{key}').hex}"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def date_precision(value: object) -> str:
    text = str(value or "").strip()
    if _DATE_DAY.fullmatch(text):
        return "day"
    if _DATE_MONTH.fullmatch(text):
        return "month"
    if _DATE_YEAR.fullmatch(text):
        return "year"
    return "unknown"


def person_key(
    *, name: object, birth: object, dataset_key: str, source_pk: object
) -> tuple[str, str]:
    """Build an identity key and status without unsafe name-only merging."""
    normalized_name = normalize_text(name)
    if normalized_name and date_precision(birth) != "unknown":
        return f"verified:{normalized_name}|{normalize_text(birth)}", "verified"
    return f"scoped:{dataset_key}|{source_pk}|{normalized_name}", "unresolved"


def organization_key(*, name: object, jurisdiction_key: str, dataset_key: str) -> str:
    """Scope organization identity to jurisdiction, falling back to dataset."""
    scope = jurisdiction_key or dataset_key
    return f"{scope}|{normalize_text(name)}"
```

- [ ] **Step 2: platform/identity.py 改为 thin re-export，并同步其余 import 位置**

`gov_relation/platform/identity.py` 全文替换为：

```python
"""Conservative normalization and deterministic identifiers for canonical data.

Re-export of gov_relation.identity (v3 canonical source).
"""

from gov_relation.identity import (  # noqa: F401
    date_precision,
    normalize_text,
    organization_key,
    person_key,
    sha256_bytes,
    stable_id,
)
```

现有 4 处 import 保持不变即可（继续解析到 platform.identity 层），但为了让新代码明确只走规范实现，建议同时把显式 import 改到 `gov_relation.identity`：

```python
# gov_relation/platform/resolution.py:10
from gov_relation.identity import normalize_text, stable_id

# gov_relation/platform/importer.py:11
from gov_relation.identity import (
    date_precision,
    normalize_text,
    organization_key,
    person_key,
    sha256_bytes,
    stable_id,
)

# scripts/govdb.py:17
from gov_relation.identity import stable_id

# tests/test_platform.py:9
from gov_relation.identity import person_key, stable_id
```

> 若同时保留 re-export，以上显式改 import 非必须（re-export 已保证行为一致），但建议改以建立可 grep 的唯一来源。

- [ ] **Step 3: 验证现有测试不受影响**

Run: `python3 -m pytest tests/test_platform.py -v --tb=short`
Expected: 所有测试通过

- [ ] **Step 4: 验证 import 正确**

Run: `python3 -c "from gov_relation.identity import normalize_text, stable_id, person_key; print(stable_id('test', 'hello'))"`
Expected: 输出 `test_<hex>` 格式

- [ ] **Step 5: Commit**

```bash
git add gov_relation/identity.py gov_relation/platform/identity.py gov_relation/platform/importer.py gov_relation/platform/resolution.py scripts/govdb.py tests/test_platform.py
git commit -m "refactor(identity): extract core identity functions to gov_relation.identity

Copied normalize_text, stable_id, sha256_bytes, date_precision,
person_key, organization_key into gov_relation.identity as the
canonical implementation; platform/identity.py now re-exports from it.
All import sites still resolve."
```

---

### Task 2: 扩展 paths.py 省份路径函数

**Files:**
- Modify: `gov_relation/paths.py`

**Interfaces:**
- Produces: `PROVINCES_DIR: Path`, `PROVINCE_SLUGS: dict[str, str]`, `province_dir(province: str) -> Path`, `province_build_dir(province: str) -> Path`, `province_database_dir(province: str) -> Path`, `province_graph_dir(province: str) -> Path`, `province_persons_dir(province: str) -> Path`, `province_reports_dir(province: str) -> Path`

- [ ] **Step 1: 在 paths.py 末尾追加新常量和函数**

```python
PROVINCES_DIR = DATA_DIR / "provinces"

PROVINCE_SLUGS: dict[str, str] = {
    "安徽省": "anhui", "北京市": "beijing", "重庆市": "chongqing",
    "福建省": "fujian", "甘肃省": "gansu", "广东省": "guangdong",
    "广西壮族自治区": "guangxi", "贵州省": "guizhou", "海南省": "hainan",
    "河北省": "hebei", "河南省": "henan", "黑龙江省": "heilongjiang",
    "湖北省": "hubei", "湖南省": "hunan", "吉林省": "jilin",
    "江苏省": "jiangsu", "江西省": "jiangxi", "辽宁省": "liaoning",
    "内蒙古自治区": "inner_mongolia", "宁夏回族自治区": "ningxia",
    "青海省": "qinghai", "山东省": "shandong", "山西省": "shanxi",
    "陕西省": "shaanxi", "上海市": "shanghai", "四川省": "sichuan",
    "天津市": "tianjin", "西藏自治区": "xizang",
    "新疆维吾尔自治区": "xinjiang", "云南省": "yunnan",
    "浙江省": "zhejiang",
}


def province_dir(province: str) -> Path:
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

- [ ] **Step 2: 验证**

Run: `python3 -c "from pathlib import Path; import gov_relation.paths as p; assert p.PROVINCES_DIR == p.DATA_DIR / 'provinces'; assert p.province_dir('四川省') == p.PROVINCES_DIR / 'sichuan'; print(p.province_dir('四川省')); print(p.province_build_dir('河南省'))"`
Expected:
```
<repo>/data/provinces/sichuan
<repo>/data/provinces/henan/build
```
> 注意：`PROVINCES_DIR` 是绝对路径（`REPO_ROOT/data/provinces`），不能用 `Path('data/provinces')` 直接相等比较。

- [ ] **Step 3: Commit**

```bash
git add gov_relation/paths.py
git commit -m "feat(paths): add PROVINCE_SLUGS and province directory helpers"
```

---

### Task 3: SchemaFactory — v3 DDL 生成

**Files:**
- Create: `gov_relation/factory/__init__.py`
- Create: `gov_relation/factory/schema_factory.py`
- Create: `tests/test_factory/__init__.py`
- Create: `tests/test_factory/test_schema_factory.py`

**Interfaces:**
- Consumes: (none — standalone)
- Produces: `SchemaFactory.create_all(conn)`, `SchemaFactory.create_entity_tables(conn)`, `SchemaFactory.create_evidence_tables(conn)`, `SchemaFactory.create_meta_tables(conn)`, `SchemaFactory.create_views(conn)`, `SchemaFactory.create_indexes(conn)`

- [ ] **Step 1: 写测试**

```python
# tests/test_factory/test_schema_factory.py
"""Tests for SchemaFactory."""

import sqlite3

from gov_relation.factory.schema_factory import SchemaFactory


def test_create_entity_tables_creates_all_seven(tmp_path):
    """create_entity_tables should create 7 entity tables."""
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_path))
    factory = SchemaFactory()
    factory.create_entity_tables(conn)
    conn.commit()

    expected = [
        "jurisdictions", "persons", "person_aliases", "organizations",
        "positions", "relationships", "person_statuses",
    ]
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )
    tables = [row[0] for row in cursor]
    for name in expected:
        assert name in tables, f"Missing table: {name}"
    conn.close()


def test_create_evidence_tables_creates_all_nine(tmp_path):
    """create_evidence_tables should create 9 evidence/provenance tables."""
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_path))
    factory = SchemaFactory()
    factory.create_evidence_tables(conn)
    conn.commit()

    expected = [
        "claims", "datasets", "entity_provenance", "evidence_links",
        "profile_documents", "quality_issues", "raw_records", "resolution_candidates",
        "sources",
    ]
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )
    tables = [row[0] for row in cursor]
    for name in expected:
        assert name in tables, f"Missing table: {name}"
    conn.close()


def test_create_all_generates_schema_version(tmp_path):
    """create_all should insert schema_meta version."""
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_path))
    factory = SchemaFactory()
    factory.create_all(conn)
    conn.commit()

    version = conn.execute(
        "SELECT value FROM schema_meta WHERE key='schema_version'"
    ).fetchone()
    assert version is not None
    assert version[0] == "3.0.0"
    conn.close()


def test_positions_table_has_foreign_keys_enforced(tmp_path):
    """Positions should reject insert with non-existent person_id."""
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_path))
    factory = SchemaFactory()
    factory.create_all(conn)
    conn.commit()

    import pytest
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO positions(position_id, person_id) VALUES(?, ?)",
            ("pos_test", "nonexistent_person"),
        )
    conn.close()
```

- [ ] **Step 2: 运行测试确认失败**

Run: `python3 -m pytest tests/test_factory/test_schema_factory.py -v`
Expected: FAIL — ModuleNotFoundError

- [ ] **Step 3: 实现 SchemaFactory**

```python
# gov_relation/factory/__init__.py
"""Factory layer for gov-relation v3 pipeline."""

from .schema_factory import SchemaFactory

__all__ = ["SchemaFactory"]
```

```python
# gov_relation/factory/schema_factory.py
"""Unified v3 schema DDL generator."""

from __future__ import annotations

import sqlite3

SCHEMA_VERSION = "3.0.0"

# ── DDL constants (full v3 DDL from spec) ──

_JURISDICTIONS = """
CREATE TABLE IF NOT EXISTS jurisdictions (
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
)"""

_PERSONS = """
CREATE TABLE IF NOT EXISTS persons (
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
)"""

_PERSON_ALIASES = """
CREATE TABLE IF NOT EXISTS person_aliases (
    person_id       TEXT NOT NULL REFERENCES persons(person_id),
    alias           TEXT NOT NULL,
    normalized_alias TEXT NOT NULL,
    alias_type      TEXT NOT NULL DEFAULT 'other',
    PRIMARY KEY (person_id, normalized_alias)
)"""

_ORGANIZATIONS = """
CREATE TABLE IF NOT EXISTS organizations (
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
)"""

_POSITIONS = """
CREATE TABLE IF NOT EXISTS positions (
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
)"""

_RELATIONSHIPS = """
CREATE TABLE IF NOT EXISTS relationships (
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
)"""

_PERSON_STATUSES = """
CREATE TABLE IF NOT EXISTS person_statuses (
    status_id            TEXT PRIMARY KEY,
    person_id            TEXT NOT NULL REFERENCES persons(person_id),
    post_text            TEXT NOT NULL DEFAULT '',
    organization_text    TEXT NOT NULL DEFAULT '',
    administrative_rank  TEXT NOT NULL DEFAULT '',
    observed_at          TEXT,
    is_current_confirmed INTEGER NOT NULL DEFAULT 0 CHECK (is_current_confirmed IN (0,1)),
    confidence           TEXT NOT NULL DEFAULT 'unverified'
                          CHECK (confidence IN ('confirmed','plausible','unverified'))
)"""

# Evidence / Provenance tables
_DATASETS = """
CREATE TABLE IF NOT EXISTS datasets (
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
)"""

_RAW_RECORDS = """
CREATE TABLE IF NOT EXISTS raw_records (
    raw_record_id  TEXT PRIMARY KEY,
    dataset_id     TEXT NOT NULL REFERENCES datasets(dataset_id),
    source_table   TEXT NOT NULL,
    source_pk      TEXT NOT NULL,
    payload_json   TEXT NOT NULL,
    payload_sha256 TEXT NOT NULL,
    imported_at    TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (dataset_id, source_table, source_pk)
)"""

_PROFILE_DOCUMENTS = """
CREATE TABLE IF NOT EXISTS profile_documents (
    profile_id     TEXT PRIMARY KEY,
    person_id      TEXT NOT NULL REFERENCES persons(person_id),
    raw_record_id  TEXT NOT NULL REFERENCES raw_records(raw_record_id),
    schema_version TEXT NOT NULL DEFAULT '',
    generated_at   TEXT NOT NULL DEFAULT '',
    profile_json   TEXT NOT NULL
)"""

_SOURCES = """
CREATE TABLE IF NOT EXISTS sources (
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
)"""

_EVIDENCE_LINKS = """
CREATE TABLE IF NOT EXISTS evidence_links (
    evidence_id   TEXT PRIMARY KEY,
    source_id     TEXT NOT NULL REFERENCES sources(source_id),
    subject_type  TEXT NOT NULL,
    subject_id    TEXT NOT NULL,
    field_name    TEXT NOT NULL DEFAULT '',
    claim_text    TEXT NOT NULL DEFAULT '',
    locator       TEXT NOT NULL DEFAULT '',
    confidence    TEXT NOT NULL DEFAULT 'unverified' CHECK (confidence IN ('confirmed','plausible','unverified')),
    UNIQUE (source_id, subject_type, subject_id, field_name, locator)
)"""

_CLAIMS = """
CREATE TABLE IF NOT EXISTS claims (
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
)"""

_ENTITY_PROVENANCE = """
CREATE TABLE IF NOT EXISTS entity_provenance (
    provenance_id   TEXT PRIMARY KEY,
    dataset_id      TEXT NOT NULL REFERENCES datasets(dataset_id),
    raw_record_id   TEXT REFERENCES raw_records(raw_record_id),
    entity_type     TEXT NOT NULL,
    entity_id       TEXT NOT NULL,
    source_field    TEXT NOT NULL DEFAULT '',
    transformation  TEXT NOT NULL DEFAULT '',
    UNIQUE (dataset_id, raw_record_id, entity_type, entity_id, source_field)
)"""

_QUALITY_ISSUES = """
CREATE TABLE IF NOT EXISTS quality_issues (
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
)"""

_RESOLUTION_CANDIDATES = """
CREATE TABLE IF NOT EXISTS resolution_candidates (
    candidate_id    TEXT PRIMARY KEY,
    left_entity_id  TEXT NOT NULL,
    right_entity_id TEXT NOT NULL,
    entity_type     TEXT NOT NULL,
    score           REAL NOT NULL CHECK (score >= 0 AND score <= 1),
    reasons_json    TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','merged','rejected')),
    UNIQUE (left_entity_id, right_entity_id, entity_type)
)"""

# Rights tables
_RIGHTS_REVIEW_KEYS = """
CREATE TABLE IF NOT EXISTS rights_review_keys (
    key_id            TEXT PRIMARY KEY,
    algorithm         TEXT NOT NULL CHECK (algorithm = 'ecdsa-p256-sha256'),
    public_key_pem    TEXT NOT NULL,
    reviewer_identity TEXT NOT NULL,
    review_authority  TEXT NOT NULL,
    status            TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active','revoked')),
    valid_from        TEXT NOT NULL,
    valid_to          TEXT,
    created_at        TEXT NOT NULL DEFAULT (datetime('now'))
)"""

_RIGHTS_MANIFESTS = """
CREATE TABLE IF NOT EXISTS rights_manifests (
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
)"""

_SOURCE_RIGHTS_DECISIONS = """
CREATE TABLE IF NOT EXISTS source_rights_decisions (
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
)"""

_SCHEMA_META = """
CREATE TABLE IF NOT EXISTS schema_meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
)"""

_INGEST_RUNS = """
CREATE TABLE IF NOT EXISTS ingest_runs (
    run_id         TEXT PRIMARY KEY,
    started_at     TEXT NOT NULL,
    finished_at    TEXT,
    mode           TEXT NOT NULL,
    status         TEXT NOT NULL CHECK (status IN ('running','succeeded','failed','partial')),
    input_count    INTEGER NOT NULL DEFAULT 0,
    imported_count INTEGER NOT NULL DEFAULT 0,
    rejected_count INTEGER NOT NULL DEFAULT 0,
    error          TEXT NOT NULL DEFAULT ''
)"""

# ── Gold Views ──

_GOLD_CURRENT_POSITIONS = """
CREATE VIEW IF NOT EXISTS gold_current_positions AS
SELECT p.person_id, p.canonical_name, ps.post_text AS title,
       ps.organization_text AS organization_name,
       ps.administrative_rank AS rank, ps.confidence
FROM person_statuses ps
JOIN persons p ON p.person_id = ps.person_id
WHERE ps.is_current_confirmed = 1"""

_GOLD_RELATIONSHIP_EDGES = """
CREATE VIEW IF NOT EXISTS gold_relationship_edges AS
SELECT r.relationship_id, a.canonical_name AS person_from,
       b.canonical_name AS person_to,
       r.relationship_type, r.direction, r.strength, r.confidence,
       r.context, r.overlap_period_text
FROM relationships r
JOIN persons a ON a.person_id = r.person_from_id
JOIN persons b ON b.person_id = r.person_to_id"""

_GOLD_COMMERCIAL_SOURCES = """
CREATE VIEW IF NOT EXISTS gold_commercial_sources AS
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
  )"""

_GOLD_COMMERCIAL_PERSONS = """
CREATE VIEW IF NOT EXISTS gold_commercial_persons AS
SELECT DISTINCT p.* FROM persons p
JOIN evidence_links e ON e.subject_type = 'person' AND e.subject_id = p.person_id
JOIN gold_commercial_sources s ON s.source_id = e.source_id"""

_GOLD_COMMERCIAL_POSITIONS = """
CREATE VIEW IF NOT EXISTS gold_commercial_positions AS
SELECT DISTINCT p.* FROM positions p
JOIN evidence_links e ON e.subject_type = 'position' AND e.subject_id = p.position_id
JOIN gold_commercial_sources s ON s.source_id = e.source_id"""

_GOLD_COMMERCIAL_RELATIONSHIPS = """
CREATE VIEW IF NOT EXISTS gold_commercial_relationships AS
SELECT DISTINCT r.* FROM relationships r
JOIN evidence_links e ON e.subject_type = 'relationship' AND e.subject_id = r.relationship_id
JOIN gold_commercial_sources s ON s.source_id = e.source_id"""

# ── Index DDL ──

_INDEXES: list[str] = [
    "CREATE INDEX IF NOT EXISTS idx_persons_normalized_name ON persons(normalized_name)",
    "CREATE INDEX IF NOT EXISTS idx_positions_person_time ON positions(person_id, sort_order, start_date)",
    "CREATE INDEX IF NOT EXISTS idx_positions_org ON positions(organization_id, is_current)",
    "CREATE INDEX IF NOT EXISTS idx_positions_dates ON positions(start_date, end_date)",
    "CREATE INDEX IF NOT EXISTS idx_relationships_from ON relationships(person_from_id)",
    "CREATE INDEX IF NOT EXISTS idx_relationships_to ON relationships(person_to_id)",
    "CREATE INDEX IF NOT EXISTS idx_relationships_overlap_org ON relationships(overlap_organization_id)",
    "CREATE INDEX IF NOT EXISTS idx_statuses_person ON person_statuses(person_id)",
    "CREATE INDEX IF NOT EXISTS idx_sources_url ON sources(canonical_url)",
    "CREATE INDEX IF NOT EXISTS idx_evidence_subject ON evidence_links(subject_type, subject_id)",
    "CREATE INDEX IF NOT EXISTS idx_evidence_source ON evidence_links(source_id)",
    "CREATE INDEX IF NOT EXISTS idx_provenance_dataset ON entity_provenance(dataset_id)",
    "CREATE INDEX IF NOT EXISTS idx_provenance_entity ON entity_provenance(entity_type, entity_id)",
    "CREATE INDEX IF NOT EXISTS idx_quality_status ON quality_issues(status, severity, issue_code)",
    "CREATE INDEX IF NOT EXISTS idx_quality_dataset ON quality_issues(dataset_id)",
    "CREATE INDEX IF NOT EXISTS idx_rights_decisions_source_time ON source_rights_decisions(source_id, effective_from, effective_to)",
    "CREATE INDEX IF NOT EXISTS idx_jurisdictions_parent ON jurisdictions(parent_id)",
    "CREATE INDEX IF NOT EXISTS idx_jurisdictions_level ON jurisdictions(province_name, level)",
    "CREATE INDEX IF NOT EXISTS idx_orgs_jurisdiction ON organizations(jurisdiction_id)",
    "CREATE INDEX IF NOT EXISTS idx_orgs_normalized_name ON organizations(normalized_name)",
    "CREATE INDEX IF NOT EXISTS idx_datasets_jurisdiction ON datasets(jurisdiction_id)",
]

_ENTITY_DDLS = [
    _JURISDICTIONS, _PERSONS, _PERSON_ALIASES, _ORGANIZATIONS,
    _POSITIONS, _RELATIONSHIPS, _PERSON_STATUSES,
]

_EVIDENCE_DDLS = [
    _DATASETS, _RAW_RECORDS, _PROFILE_DOCUMENTS, _SOURCES,
    _EVIDENCE_LINKS, _CLAIMS, _ENTITY_PROVENANCE, _QUALITY_ISSUES,
    _RESOLUTION_CANDIDATES,
]

_RIGHTS_DDLS = [_RIGHTS_REVIEW_KEYS, _RIGHTS_MANIFESTS, _SOURCE_RIGHTS_DECISIONS]

_META_DDLS = [_SCHEMA_META, _INGEST_RUNS]

_ALL_VIEWS = [
    _GOLD_CURRENT_POSITIONS, _GOLD_RELATIONSHIP_EDGES,
    _GOLD_COMMERCIAL_SOURCES, _GOLD_COMMERCIAL_PERSONS,
    _GOLD_COMMERCIAL_POSITIONS, _GOLD_COMMERCIAL_RELATIONSHIPS,
]


class SchemaFactory:
    """Generate the complete v3 database schema (21 tables + 6 views + indexes)."""

    def create_all(self, conn: sqlite3.Connection) -> None:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("PRAGMA busy_timeout=5000")
        self.create_entity_tables(conn)
        self.create_evidence_tables(conn)
        self.create_rights_tables(conn)
        self.create_meta_tables(conn)
        self.create_views(conn)
        self.create_indexes(conn)
        conn.execute(
            "INSERT OR REPLACE INTO schema_meta(key, value) VALUES('schema_version', ?)",
            (SCHEMA_VERSION,),
        )
        conn.commit()

    def create_entity_tables(self, conn: sqlite3.Connection) -> None:
        for ddl in _ENTITY_DDLS:
            conn.execute(ddl)

    def create_evidence_tables(self, conn: sqlite3.Connection) -> None:
        for ddl in _EVIDENCE_DDLS:
            conn.execute(ddl)

    def create_rights_tables(self, conn: sqlite3.Connection) -> None:
        for ddl in _RIGHTS_DDLS:
            conn.execute(ddl)

    def create_meta_tables(self, conn: sqlite3.Connection) -> None:
        for ddl in _META_DDLS:
            conn.execute(ddl)

    def create_views(self, conn: sqlite3.Connection) -> None:
        for ddl in _ALL_VIEWS:
            conn.execute(ddl)

    def create_indexes(self, conn: sqlite3.Connection) -> None:
        for ddl in _INDEXES:
            conn.execute(ddl)
```

- [ ] **Step 4: 运行测试确认通过**

Run: `python3 -m pytest tests/test_factory/test_schema_factory.py -v`
Expected: 4 PASS

- [ ] **Step 5: Commit**

```bash
git add gov_relation/factory/__init__.py gov_relation/factory/schema_factory.py tests/test_factory/__init__.py tests/test_factory/test_schema_factory.py
git commit -m "feat(factory): add SchemaFactory with full v3 DDL (21 tables + 6 views + 21 indexes)"
```

---

### Task 4: InsertFactory — 参数化 upsert

**Files:**
- Create: `gov_relation/factory/insert_factory.py`
- Create: `tests/test_factory/test_insert_factory.py`

**Interfaces:**
- Consumes: `gov_relation.identity.stable_id, normalize_text, person_key`, `gov_relation.factory.schema_factory.SchemaFactory`
- Produces: `InsertFactory.upsert_person(conn, data) -> str`, `InsertFactory.upsert_organization(conn, data) -> str`, `InsertFactory.upsert_jurisdiction(conn, data) -> str`, `InsertFactory.insert_position(conn, data) -> str`, `InsertFactory.insert_relationship(conn, data) -> str`, `InsertFactory.insert_source(conn, data) -> str`, `InsertFactory.link_evidence(conn, source_id, subject_type, subject_id, field_name) -> None`

- [ ] **Step 1: 写测试**

```python
# tests/test_factory/test_insert_factory.py
"""Tests for InsertFactory."""

import sqlite3
import pytest

from gov_relation.factory.schema_factory import SchemaFactory
from gov_relation.factory.insert_factory import InsertFactory


@pytest.fixture
def conn(tmp_path):
    db_path = tmp_path / "test.db"
    c = sqlite3.connect(str(db_path))
    SchemaFactory().create_all(c)
    return c


def test_upsert_person_creates_and_returns_person_id(conn):
    factory = InsertFactory()
    data = {"canonical_name": "张三", "birth_text": "1965-03", "gender": "男"}
    person_id = factory.upsert_person(conn, data)
    assert person_id.startswith("per_")
    row = conn.execute(
        "SELECT canonical_name, gender FROM persons WHERE person_id=?", (person_id,)
    ).fetchone()
    assert row[0] == "张三"
    assert row[1] == "男"


def test_upsert_person_idempotent_same_data(conn):
    factory = InsertFactory()
    data = {"canonical_name": "李四", "birth_text": "1970-05"}
    id1 = factory.upsert_person(conn, data)
    id2 = factory.upsert_person(conn, data)
    assert id1 == id2
    count = conn.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
    assert count == 1


def test_upsert_person_verified_when_name_and_birth_present(conn):
    factory = InsertFactory()
    pdata = {"canonical_name": "王五", "birth_text": "1975-12-03"}
    pid = factory.upsert_person(conn, pdata)
    status = conn.execute(
        "SELECT identity_status FROM persons WHERE person_id=?", (pid,)
    ).fetchone()[0]
    assert status == "verified"


def test_upsert_person_unresolved_when_no_birth(conn):
    factory = InsertFactory()
    pdata = {"canonical_name": "无名"}
    pid = factory.upsert_person(conn, pdata)
    status = conn.execute(
        "SELECT identity_status FROM persons WHERE person_id=?", (pid,)
    ).fetchone()[0]
    assert status == "unresolved"


def test_upsert_jurisdiction_creates_rows(conn):
    factory = InsertFactory()
    jid = factory.upsert_jurisdiction(
        conn, {"name": "四川省", "level": "province", "province_name": "四川省"}
    )
    assert jid.startswith("jur_")
    row = conn.execute(
        "SELECT name, level FROM jurisdictions WHERE jurisdiction_id=?", (jid,)
    ).fetchone()
    assert row[0] == "四川省"
    assert row[1] == "province"


def test_upsert_organization_returns_id(conn):
    factory = InsertFactory()
    org_data = {"canonical_name": "中共锦江区委", "organization_type": "party"}
    org_id = factory.upsert_organization(conn, org_data)
    assert org_id.startswith("org_")


def test_insert_position_links_person_and_org(conn):
    factory = InsertFactory()
    pid = factory.upsert_person(conn, {"canonical_name": "赵六", "birth_text": "1968"})
    oid = factory.upsert_organization(conn, {"canonical_name": "中共某区委"})
    pos_data = {
        "person_id": pid, "organization_id": oid, "title": "区委书记",
        "title_category": "党委正职", "start_text": "2020-01", "is_current": 1,
    }
    pos_id = factory.insert_position(conn, pos_data)
    assert pos_id.startswith("pos_")
    row = conn.execute(
        "SELECT title, person_id, organization_id FROM positions WHERE position_id=?",
        (pos_id,),
    ).fetchone()
    assert row[0] == "区委书记"


def test_insert_position_same_title_different_persons_distinct_ids(conn):
    """F5 regression: two people with the same title must get distinct position ids."""
    factory = InsertFactory()
    pid_a = factory.upsert_person(conn, {"canonical_name": "A", "birth_text": "1960"})
    pid_b = factory.upsert_person(conn, {"canonical_name": "B", "birth_text": "1965"})
    pos_a = factory.insert_position(conn, {
        "person_id": pid_a, "title": "县委书记", "start_text": "2016-01",
    })
    pos_b = factory.insert_position(conn, {
        "person_id": pid_b, "title": "县委书记", "start_text": "2018-01",
    })
    assert pos_a != pos_b
    assert conn.execute("SELECT COUNT(*) FROM positions").fetchone()[0] == 2


def test_insert_relationship_creates_edge(conn):
    factory = InsertFactory()
    a = factory.upsert_person(conn, {"canonical_name": "A", "birth_text": "1960"})
    b = factory.upsert_person(conn, {"canonical_name": "B", "birth_text": "1965"})
    rel_id = factory.insert_relationship(conn, {
        "person_from_id": a, "person_to_id": b,
        "relationship_type": "coworker", "context": "同期任职",
    })
    assert rel_id.startswith("rel_")
    row = conn.execute(
        "SELECT relationship_type, person_from_id, person_to_id FROM relationships WHERE relationship_id=?",
        (rel_id,),
    ).fetchone()
    assert row[0] == "coworker"
    assert row[1] == a
    assert row[2] == b


def test_insert_source_and_link_evidence(conn):
    factory = InsertFactory()
    pid = factory.upsert_person(conn, {"canonical_name": "C", "birth_text": "1970"})
    src_id = factory.insert_source(conn, {
        "canonical_url": "https://example.com/appointment",
        "title": "任命通知", "source_type": "appointment_notice",
    })
    assert src_id.startswith("src_")
    factory.link_evidence(conn, src_id, "person", pid, "canonical_name", "evidence")
    ev = conn.execute(
        "SELECT 1 FROM evidence_links WHERE source_id=? AND subject_id=?", (src_id, pid)
    ).fetchone()
    assert ev is not None
```

- [ ] **Step 2: 运行测试确认失败**

Run: `python3 -m pytest tests/test_factory/test_insert_factory.py -v`
Expected: FAIL — ModuleNotFoundError

- [ ] **Step 3: 实现 InsertFactory**

```python
# gov_relation/factory/insert_factory.py
"""Parameterized upsert/insert operations for v3 schema entities."""

from __future__ import annotations

import sqlite3
from typing import Any

from gov_relation.identity import (
    normalize_text,
    organization_key,
    person_key,
    stable_id,
)

_INSERT_PERSON = """
INSERT OR IGNORE INTO persons
    (person_id, canonical_name, normalized_name, gender, ethnicity,
     birth_text, birth_precision, birthplace, native_place,
     education, party_join_text, work_start_text, identity_status)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

_UPDATE_PERSON = """
UPDATE persons SET
    canonical_name = COALESCE(NULLIF(:canonical_name, ''), canonical_name),
    normalized_name = COALESCE(NULLIF(:normalized_name, ''), normalized_name),
    gender = COALESCE(NULLIF(:gender, ''), gender),
    ethnicity = COALESCE(NULLIF(:ethnicity, ''), ethnicity),
    birth_text = COALESCE(NULLIF(:birth_text, ''), birth_text),
    birth_precision = COALESCE(NULLIF(:birth_precision, ''), birth_precision),
    updated_at = datetime('now')
WHERE person_id = :person_id
"""


class InsertFactory:
    """Write v3 entities with upsert semantics."""

    # ── Person ──

    def upsert_person(
        self, conn: sqlite3.Connection, data: dict[str, Any],
        *, dataset_key: str = "factory", source_pk: str | None = None,
    ) -> str:
        name = str(data.get("canonical_name", "")).strip()
        birth = data.get("birth_text", "")
        pk = source_pk or name
        key, identity_status = person_key(
            name=name, birth=birth, dataset_key=dataset_key, source_pk=pk,
        )
        person_id = stable_id("per", key)
        from gov_relation.identity import date_precision

        params = {
            "person_id": person_id,
            "canonical_name": name,
            "normalized_name": normalize_text(name),
            "gender": str(data.get("gender", "")),
            "ethnicity": str(data.get("ethnicity", "")),
            "birth_text": str(birth),
            "birth_precision": date_precision(birth),
            "birthplace": str(data.get("birthplace", "")),
            "native_place": str(data.get("native_place", "")),
            "education": str(data.get("education", "")),
            "party_join_text": str(data.get("party_join_text", "")),
            "work_start_text": str(data.get("work_start_text", "")),
            "identity_status": identity_status,
        }
        conn.execute(
            """INSERT OR IGNORE INTO persons
               (person_id, canonical_name, normalized_name, gender, ethnicity,
                birth_text, birth_precision, birthplace, native_place,
                education, party_join_text, work_start_text, identity_status)
               VALUES (:person_id, :canonical_name, :normalized_name, :gender, :ethnicity,
                       :birth_text, :birth_precision, :birthplace, :native_place,
                       :education, :party_join_text, :work_start_text, :identity_status)""",
            params,
        )
        self._update_person(conn, params)
        conn.commit()
        return person_id

    def _update_person(self, conn: sqlite3.Connection, params: dict[str, Any]) -> None:
        conn.execute(
            """UPDATE persons SET
                canonical_name = COALESCE(NULLIF(:canonical_name, ''), canonical_name),
                normalized_name = COALESCE(NULLIF(:normalized_name, ''), normalized_name),
                gender = COALESCE(NULLIF(:gender, ''), gender),
                ethnicity = COALESCE(NULLIF(:ethnicity, ''), ethnicity),
                birth_text = COALESCE(NULLIF(:birth_text, ''), birth_text),
                birth_precision = COALESCE(NULLIF(:birth_precision, ''), birth_precision),
                updated_at = datetime('now')
            WHERE person_id = :person_id""",
            params,
        )

    # ── Jurisdiction ──

    def upsert_jurisdiction(self, conn: sqlite3.Connection, data: dict[str, Any]) -> str:
        name = str(data.get("name", "")).strip()
        parent_id = data.get("parent_id") or None
        level = str(data.get("level", "unknown"))
        key = f"{parent_id or 'root'}|{level}|{normalize_text(name)}"
        jurisdiction_id = stable_id("jur", key)
        conn.execute(
            """INSERT OR IGNORE INTO jurisdictions
               (jurisdiction_id, parent_id, name, normalized_name, level,
                province_name, prefecture_name, county_name)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                jurisdiction_id, parent_id, name, normalize_text(name), level,
                str(data.get("province_name", "")),
                str(data.get("prefecture_name", "")),
                str(data.get("county_name", "")),
            ),
        )
        conn.commit()
        return jurisdiction_id

    # ── Organization ──

    def upsert_organization(
        self, conn: sqlite3.Connection, data: dict[str, Any],
        *, dataset_key: str = "factory",
    ) -> str:
        name = str(data.get("canonical_name", "")).strip()
        jurisdiction_key = str(data.get("jurisdiction_id", "") or "")
        key = organization_key(name=name, jurisdiction_key=jurisdiction_key, dataset_key=dataset_key)
        org_id = stable_id("org", key)
        conn.execute(
            """INSERT OR IGNORE INTO organizations
               (organization_id, jurisdiction_id, canonical_name, normalized_name,
                organization_type, administrative_level, location_text)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                org_id,
                data.get("jurisdiction_id") or None,
                name,
                normalize_text(name),
                str(data.get("organization_type", "")),
                str(data.get("administrative_level", "")),
                str(data.get("location_text", "")),
            ),
        )
        conn.commit()
        return org_id

    # ── Position ──

    def insert_position(self, conn: sqlite3.Connection, data: dict[str, Any]) -> str:
        dataset_key = str(data.get("_dataset_key", "factory"))
        source_pk = str(data.get("_source_pk", "None"))
        from gov_relation.identity import date_precision
        # 修复（评审 F5）：key 必须包含 person_id + title + start_text，
        # 否则同一 dataset 内两人同名职务（如两个"县委书记"）会算出相同
        # position_id，INSERT OR IGNORE 静默丢第二行。
        start = str(data.get("start_text", ""))
        dedup_key = (
            f'{dataset_key}|{data.get("person_id", "")}|'
            f'{normalize_text(data.get("title", ""))}|{normalize_text(start)}'
        )
        if source_pk in (None, "", "None"):
            source_pk = dedup_key
        key = f"{dataset_key}|{source_pk}"
        position_id = stable_id("pos", key)
        end = str(data.get("end_text", ""))
        conn.execute(
            """INSERT OR IGNORE INTO positions
               (position_id, person_id, organization_id, organization_text,
                title, title_category, rank, start_text, end_text, start_date, end_date,
                date_precision, is_current, sort_order, confidence, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                position_id,
                str(data.get("person_id", "")),
                data.get("organization_id") or None,
                str(data.get("organization_text", "")),
                str(data.get("title", "")),
                str(data.get("title_category", "")),
                str(data.get("rank", "")),
                start,
                end,
                None,
                None,
                date_precision(start),
                int(data.get("is_current", 0)),
                int(data.get("sort_order", 0)),
                str(data.get("confidence", "unverified")),
                str(data.get("notes", "")),
            ),
        )
        conn.commit()
        return position_id

    # ── Relationship ──

    def insert_relationship(self, conn: sqlite3.Connection, data: dict[str, Any]) -> str:
        dataset_key = str(data.get("_dataset_key", "factory"))
        source_pk = str(data.get("_source_pk", "None"))
        # 修复（评审 F5）：key 必须包含 relationship_type，否则同一对人员的
        # 多条关系（如 同事 + 亲属）会算出相同 relationship_id 而静默去重。
        dedup_key = (
            f'{data.get("person_from_id", "")}|{data.get("person_to_id", "")}|'
            f'{data.get("relationship_type", "other")}'
        )
        if source_pk in (None, "", "None"):
            source_pk = dedup_key
        key = f"{dataset_key}|{source_pk}"
        relationship_id = stable_id("rel", key)
        conn.execute(
            """INSERT OR IGNORE INTO relationships
               (relationship_id, person_from_id, person_to_id, relationship_type,
                direction, strength, confidence, context, evidence_summary,
                overlap_organization_id, overlap_organization_text, overlap_period_text)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                relationship_id,
                str(data.get("person_from_id", "")),
                str(data.get("person_to_id", "")),
                str(data.get("relationship_type", "other")),
                str(data.get("direction", "undirected")),
                str(data.get("strength", "unknown")),
                str(data.get("confidence", "unverified")),
                str(data.get("context", "")),
                str(data.get("evidence_summary", "")),
                data.get("overlap_organization_id") or None,
                str(data.get("overlap_organization_text", "")),
                str(data.get("overlap_period_text", "")),
            ),
        )
        conn.commit()
        return relationship_id

    # ── Source + Evidence ──

    def insert_source(self, conn: sqlite3.Connection, data: dict[str, Any]) -> str:
        url = str(data.get("canonical_url", "")).strip()
        title = str(data.get("title", "")).strip()
        key = url or title
        if not key:
            key = str(data.get("publisher", "unknown"))
        source_id = stable_id("src", key)
        conn.execute(
            """INSERT OR IGNORE INTO sources
               (source_id, canonical_url, title, publisher, published_at, accessed_at,
                source_type, reliability)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                source_id,
                url,
                title,
                str(data.get("publisher", "")),
                data.get("published_at") or None,
                data.get("accessed_at") or None,
                str(data.get("source_type", "other")),
                str(data.get("reliability", "low")),
            ),
        )
        conn.commit()
        return source_id

    def link_evidence(
        self, conn: sqlite3.Connection, source_id: str, subject_type: str,
        subject_id: str, field_name: str, locator: str = "",
    ) -> None:
        key = f"{source_id}|{subject_type}|{subject_id}|{field_name}|{locator}"
        evidence_id = stable_id("ev", key)
        conn.execute(
            """INSERT OR IGNORE INTO evidence_links
               (evidence_id, source_id, subject_type, subject_id, field_name, locator)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (evidence_id, source_id, subject_type, subject_id, field_name, locator),
        )
```

- [ ] **Step 4: 运行测试确认通过**

Run: `python3 -m pytest tests/test_factory/test_insert_factory.py -v`
Expected: 10 PASS（10 个测试函数：upsert_person×4 / jurisdiction / organization / position / position-same-title-collision / relationship / source+evidence）
> 评审确认：原计划 "8 PASS" 有误；修复后 F5 碰撞回归测试使总数 = 10。

- [ ] **Step 5: Commit**

```bash
git add gov_relation/factory/insert_factory.py tests/test_factory/test_insert_factory.py
git commit -m "feat(factory): add InsertFactory with upsert semantics for all v3 entities"
```

---

### Task 5: GEXFFactory — 从 DB 生成 GEXF

**Files:**
- Modify: `gov_relation/gexf.py`（重构：`_build_tree()` 共享 `write()`/`to_string()`）
- Create: `gov_relation/factory/gexf_factory.py`
- Create: `tests/test_factory/test_gexf_factory.py`

**Interfaces:**
- Consumes: `gov_relation.gexf.GEXFBuilder`, `gov_relation.factory.schema_factory.SchemaFactory`, `gov_relation.factory.insert_factory.InsertFactory`
- Produces: `GEXFFactory.build(conn, title) -> str`

**设计与修复点（承接评审 F1/F2）:**
1. `GEXFBuilder.to_string()` 目前只输出裸 `node id/label` 与 `edge id/source/target`（缺 `<meta><title>`、缺 `attvalues` 的 `type/context/overlap_period`），与 `write()` 文件形式不一致 → 断言 `"空图"`/`"coworker"`/`"同期任职"` 全失败。重构为先构建 ElementTree 再序列化，`write()` 与 `to_string()` 共用。
2. `GEXFFactory` 不用内建 `hash()` 做节点 id（进程内 salt 随机 → 跨运行漂移、person/org 区间重叠），改用 `gov_relation.identity.sha256_bytes()` 派生出确定性 `int` id。

- [ ] **Step 0（前置依赖）: 修 gexf.py — 让 to_string() 与 write() 输出一致**

`GEXFBuilder.write()` 已含完整 XML（meta/title + attvalues）。把第 103-198 行的树构建提取为私有方法，`write()` 与 `to_string()` 共用：

```python
# gov_relation/gexf.py 内
def _build_tree(self) -> ET.ElementTree:
    """Build the full GEXF ElementTree (title, node/edge attvalues...)."""
    # 将现有 write() 中 root→tree 的构建逻辑整体移入（含 meta title、
    # node viz:size/shape/color、node/edge attvalues），返回 ET.ElementTree。
    ...

def write(self, path: Path | str) -> None:
    tree = self._build_tree()
    ...  # 原 path.parent.mkdir + tree.write 保留

def to_string(self) -> str:
    import io
    buf = io.BytesIO()
    self._build_tree().write(buf, encoding="utf-8", xml_declaration=True)
    return buf.getvalue().decode("utf-8")
```

> 现有 `test_gexf.py`（若存在）应不受影响：此重构不改变 `write()` 产出的 XML 结构。若仓库现有测试对 to_string 的裸输出有断言，需相应调整。

```python
# tests/test_factory/test_gexf_factory.py
"""Tests for GEXFFactory."""

import sqlite3
from xml.etree import ElementTree as ET

from gov_relation.factory.schema_factory import SchemaFactory
from gov_relation.factory.insert_factory import InsertFactory
from gov_relation.factory.gexf_factory import GEXFFactory


def test_build_produces_valid_gexf_xml(tmp_path):
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_path))
    SchemaFactory().create_all(conn)
    f = InsertFactory()
    pid = f.upsert_person(conn, {"canonical_name": "张三", "birth_text": "1965", "gender": "男"})
    oid = f.upsert_organization(conn, {"canonical_name": "中共某区委"})
    f.insert_position(conn, {
        "person_id": pid, "organization_id": oid, "title": "区委书记",
        "is_current": 1,
    })
    conn.commit()

    gexf_factory = GEXFFactory()
    xml_str = gexf_factory.build(conn, "测试图")
    root = ET.fromstring(xml_str)

    ns = {"g": "http://www.gexf.net/1.3"}
    assert root.tag == "{http://www.gexf.net/1.3}gexf"
    assert root.get("version") == "1.3"
    nodes = root.findall(".//g:node", ns)
    assert len(nodes) >= 1
    labels = [n.get("label") for n in nodes]
    assert "张三" in labels
    assert "中共某区委" in labels
    conn.close()


def test_empty_db_produces_valid_gexf(tmp_path):
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_path))
    SchemaFactory().create_all(conn)
    xml_str = GEXFFactory().build(conn, "空图")
    assert "<gexf" in xml_str
    assert "空图" in xml_str
    conn.close()


def test_relationship_becomes_edge(tmp_path):
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_path))
    SchemaFactory().create_all(conn)
    f = InsertFactory()
    a = f.upsert_person(conn, {"canonical_name": "A", "birth_text": "1960"})
    b = f.upsert_person(conn, {"canonical_name": "B", "birth_text": "1965"})
    f.insert_relationship(conn, {
        "person_from_id": a, "person_to_id": b,
        "relationship_type": "coworker", "context": "同期任职于某部门",
    })
    conn.commit()
    xml_str = GEXFFactory().build(conn, "关系图")
    assert "coworker" in xml_str
    assert "同期任职" in xml_str
    conn.close()
```

- [ ] **Step 1: 写测试**

```python
# gov_relation/factory/gexf_factory.py
"""Factory that builds GEXF graphs from a v3 SQLite database.

Node ids are deterministic (sha256-derived), NOT builtin hash(): hash() is
salted per-process, so ids would drift every run and clobber git history.
"""

from __future__ import annotations

import sqlite3

from gov_relation.gexf import GEXFBuilder
from gov_relation.identity import sha256_bytes

_PERSON_BASE = 0          # persons map to [0, 10**9)
_ORG_BASE = 10**9         # organizations map to [10**9, 2*10**9): no overlap


def _node_id(kind: str, entity_id: str, base: int) -> int:
    """Deterministic entity id -> int in [base, base + 10**9)."""
    digest = sha256_bytes(f"{kind}|{entity_id}".encode("utf-8"))
    return base + int(digest[:16], 16) % (10**9)


class GEXFFactory:
    """Build GEXF XML from a v3-schema SQLite database."""

    def build(self, conn: sqlite3.Connection, title: str) -> str:
        builder = GEXFBuilder(title=title)

        for row in conn.execute(
            "SELECT person_id, canonical_name, gender, birth_text FROM persons"
        ):
            post = ""
            status = conn.execute(
                "SELECT post_text FROM person_statuses WHERE person_id=? AND is_current_confirmed=1 LIMIT 1",
                (row[0],),
            ).fetchone()
            if not status:
                status = conn.execute(
                    "SELECT title FROM positions WHERE person_id=? AND is_current=1 ORDER BY sort_order LIMIT 1",
                    (row[0],),
                ).fetchone()
            if status:
                post = status[0]
            builder.add_person(
                id=_node_id("per", row[0], _PERSON_BASE),
                name=row[1],
                current_post=post,
                gender=row[2] or "",
                birth=row[3] or "",
            )

        for row in conn.execute(
            "SELECT organization_id, canonical_name FROM organizations"
        ):
            builder.add_organization(
                id=_node_id("org", row[0], _ORG_BASE),
                name=row[1],
            )

        for row in conn.execute(
            """SELECT relationship_id, person_from_id, person_to_id,
                      relationship_type, context, overlap_period_text
               FROM relationships"""
        ):
            a = _node_id("per", row[1], _PERSON_BASE)
            b = _node_id("per", row[2], _PERSON_BASE)
            builder.add_relationship(
                a, b, row[3],
                context=row[4] or "",
                overlap_period=row[5] or "",
            )

        return builder.to_string()

    def write(self, conn: sqlite3.Connection, title: str, path: str) -> None:
        from pathlib import Path
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        xml = self.build(conn, title)
        Path(path).write_text(xml, encoding="utf-8")
```

- [ ] **Step 2: 运行测试确认通过**

Run: `python3 -m pytest tests/test_factory/test_gexf_factory.py -v`
Expected: 3 PASS

- [ ] **Step 3: Commit**

```bash
git add gov_relation/gexf.py gov_relation/factory/gexf_factory.py tests/test_factory/test_gexf_factory.py
git commit -m "feat(factory): add GEXFFactory that builds GEXF graphs from v3 database

Also refactor GEXFBuilder to share _build_tree() between write() and
to_string() so string output carries meta title and node/edge attvalues.
GEXFFactory uses deterministic sha256-derived ids, not builtin hash()."
```

---

### Task 6: PersonJSONFactory + ReportFactory + BuildScriptFactory

**Files:**
- Create: `gov_relation/factory/person_factory.py`
- Create: `gov_relation/factory/report_factory.py`
- Create: `gov_relation/factory/build_factory.py`
- Create: `tests/test_factory/test_build_factory.py`

**Interfaces:**
- Consumes: `InsertFactory`, `SchemaFactory`, `GEXFFactory`, `gov_relation.paths`
- Produces: `PersonJSONFactory.build(conn, person_id) -> dict`, `ReportFactory.build(slug, stats) -> str`, `BuildScriptFactory.generate(slug, province_dir, persons, orgs, positions, relationships, sources, claims=None) -> str`

- [ ] **Step 1: 写 PersonJSONFactory**

```python
# gov_relation/factory/person_factory.py
"""Factory for generating person profile JSON documents."""

from __future__ import annotations

import json
import sqlite3
from datetime import date


class PersonJSONFactory:
    """Generate a person profile JSON from v3 database records."""

    def build(self, conn: sqlite3.Connection, person_id: str) -> dict:
        person = conn.execute(
            "SELECT * FROM persons WHERE person_id=?", (person_id,)
        ).fetchone()
        if not person:
            raise ValueError(f"Person not found: {person_id}")

        cols = [desc[0] for desc in conn.execute("SELECT * FROM persons LIMIT 0").description]
        person_dict = dict(zip(cols, person))

        positions = []
        for row in conn.execute(
            "SELECT * FROM positions WHERE person_id=? ORDER BY sort_order",
            (person_id,),
        ):
            pos_cols = [desc[0] for desc in conn.execute("SELECT * FROM positions LIMIT 0").description]
            positions.append(dict(zip(pos_cols, row)))

        relationships = []
        for row in conn.execute(
            """SELECT r.*, p.canonical_name AS other_name
               FROM relationships r
               JOIN persons p ON (p.person_id = r.person_from_id OR p.person_id = r.person_to_id)
               WHERE (r.person_from_id=? OR r.person_to_id=?) AND p.person_id <> ?""",
            (person_id, person_id, person_id),
        ):
            rel_cols = [desc[0] for desc in conn.execute("SELECT * FROM relationships LIMIT 0").description]
            rel = dict(zip(rel_cols, row[:-1]))
            rel["related_person_name"] = row[-1]
            relationships.append(rel)

        return {
            "schema_version": "3.0",
            "generated_at": date.today().isoformat(),
            "person_id": person_id,
            "identity": {
                "name": person_dict.get("canonical_name", ""),
                "gender": person_dict.get("gender", ""),
                "ethnicity": person_dict.get("ethnicity", ""),
                "birth": person_dict.get("birth_text", ""),
                "birthplace": person_dict.get("birthplace", ""),
                "native_place": person_dict.get("native_place", ""),
                "education": person_dict.get("education", ""),
            },
            "career_timeline": [
                {
                    "title": p.get("title", ""),
                    "org": p.get("organization_text", ""),
                    "start": p.get("start_text", ""),
                    "end": p.get("end_text", ""),
                    "rank": p.get("rank", ""),
                    "is_current": bool(p.get("is_current", 0)),
                }
                for p in positions
            ],
            "relationships": [
                {
                    "person": r.get("related_person_name", ""),
                    "type": r.get("relationship_type", ""),
                    "context": r.get("context", ""),
                    "overlap_period": r.get("overlap_period_text", ""),
                }
                for r in relationships
            ],
            "open_questions": [],
        }

    def write(self, conn: sqlite3.Connection, person_id: str, path: str) -> None:
        from pathlib import Path
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        profile = self.build(conn, person_id)
        Path(path).write_text(
            json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8"
        )
```

- [ ] **Step 2: 写 ReportFactory**

```python
# gov_relation/factory/report_factory.py
"""Factory for generating investigation report Markdown templates."""

from __future__ import annotations

from datetime import date


class ReportFactory:
    """Generate a structured investigation report in Markdown."""

    def build(self, slug: str, stats: dict) -> str:
        today = date.today().isoformat()
        return f"""# {slug} 领导班子调查

**生成日期:** {today}

## 数据概览

| 指标 | 数量 |
|------|------|
| 人员 | {stats.get('persons', 0)} |
| 组织 | {stats.get('organizations', 0)} |
| 任职记录 | {stats.get('positions', 0)} |
| 关系 | {stats.get('relationships', 0)} |
| 来源 | {stats.get('sources', 0)} |

## 现任领导

<!-- TODO: fill in from research -->

## 关系网络摘要

<!-- TODO: fill in key relationships -->

## 开放问题

<!-- TODO: document gaps and uncertainties -->
"""

    def build_from_conn(self, conn, slug: str) -> str:
        import sqlite3
        stats = {}
        for table in ("persons", "organizations", "positions", "relationships", "sources"):
            try:
                stats[table] = conn.execute(f"SELECT COUNT(*) FROM [{table}]").fetchone()[0]
            except sqlite3.Error:
                stats[table] = 0
        return self.build(slug, stats)
```

- [ ] **Step 3: 写 BuildScriptFactory**

BuildScriptFactory 是最关键的工厂 — 它生成完整的、可独立运行的 build 脚本。

```python
# gov_relation/factory/build_factory.py
"""Factory that generates a complete, standalone build_<slug>_data.py script."""

from __future__ import annotations

from pathlib import Path


class BuildScriptFactory:
    """Generate a standalone build script from structured data lists."""

    def generate(
        self,
        *,
        slug: str,
        province_dir: Path,
        persons: list[dict],
        organizations: list[dict],
        positions: list[dict],
        relationships: list[dict],
        sources: list[dict] | None = None,
        claims: list[dict] | None = None,
    ) -> str:
        sources = sources or []
        claims = claims or []

        persons_repr = self._format_list(persons, "PERSONS")
        orgs_repr = self._format_list(organizations, "ORGANIZATIONS")
        pos_repr = self._format_list(positions, "POSITIONS")
        rels_repr = self._format_list(relationships, "RELATIONSHIPS")
        src_repr = self._format_list(sources, "SOURCES")
        claims_repr = self._format_list(claims, "CLAIMS")

        db_rel = Path(province_dir.name) / "database" / f"{slug}_network.db"
        gexf_rel = Path(province_dir.name) / "graph" / f"{slug}_network.gexf"

        return f'''#!/usr/bin/env python3
"""{slug} government personnel network — auto-generated by BuildScriptFactory."""

import sqlite3
import sys
from pathlib import Path

# 修复（评审 F4）：不能用固定 parents[3]（脚本在 data/provinces/<slug>/build/
# 时 parents[3] 是 data/ 而非仓库根）。改为向上查找 gov_relation 包所在目录，
# 对脚本存放层级不敏感。运行时不依赖 cwd 或 PYTHONPATH。
REPO_ROOT = next(
    p for p in Path(__file__).resolve().parents
    if (p / "gov_relation").is_dir()
)
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.factory.schema_factory import SchemaFactory
from gov_relation.factory.insert_factory import InsertFactory
from gov_relation.factory.gexf_factory import GEXFFactory
from gov_relation.factory.person_factory import PersonJSONFactory
from gov_relation.factory.report_factory import ReportFactory
from gov_relation.paths import PROVINCES_DIR

PROVINCE_DIR = PROVINCES_DIR / "{province_dir.name}"
DB_PATH = PROVINCE_DIR / "database" / "{slug}_network.db"
GEXF_PATH = PROVINCE_DIR / "graph" / "{slug}_network.gexf"

{persons_repr}

{orgs_repr}

{pos_repr}

{rels_repr}

{src_repr}

{claims_repr}


def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    GEXF_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(DB_PATH))
    factory = InsertFactory()

    # Build
    SchemaFactory().create_all(conn)

    # 修复（F6）：POSITIONS/RELATIONSHIPS 数据在源列表里带的是人/机构名字
    # （或空 person_id）。先生成人员/机构 id → 名字映射，插入任职/关系时回填
    # 真实 FK，避免 FOREIGN KEY constraint failed。
    person_id_by_name = {{}}
    for p in PERSONS:
        pid = factory.upsert_person(conn, p)
        person_id_by_name[p.get("canonical_name", "")] = pid
    org_id_by_name = {{}}
    for o in ORGANIZATIONS:
        oid = factory.upsert_organization(conn, o)
        org_id_by_name[o.get("canonical_name", "")] = oid

    for pos in POSITIONS:
        pos = dict(pos)
        if not pos.get("person_id"):
            pos["person_id"] = person_id_by_name.get(pos.pop("person_name", ""), "")
        if not pos.get("organization_id"):
            pos["organization_id"] = org_id_by_name.get(pos.pop("organization_name", ""))
        factory.insert_position(conn, pos)

    for rel in RELATIONSHIPS:
        rel = dict(rel)
        if not rel.get("person_from_id"):
            rel["person_from_id"] = person_id_by_name.get(rel.pop("person_from_name", ""), "")
        if not rel.get("person_to_id"):
            rel["person_to_id"] = person_id_by_name.get(rel.pop("person_to_name", ""), "")
        factory.insert_relationship(conn, rel)

    for src in SOURCES:
        factory.insert_source(conn, src)

    # GEXF
    GEXFFactory().write(conn, "{slug}", str(GEXF_PATH))

    # Person profiles
    pf = PersonJSONFactory()
    persons_dir = PROVINCE_DIR / "persons"
    persons_dir.mkdir(parents=True, exist_ok=True)
    for p in PERSONS:
        pid = person_id_by_name.get(p.get("canonical_name", ""))
        if not pid:
            continue
        name = p.get("canonical_name", "unknown")
        pf.write(conn, pid, str(persons_dir / f"{{name}}.json"))

    # Report —— 修复（F10）：原模板丢弃了返回值；实际写入 reports/
    report_dir = PROVINCE_DIR / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    report = ReportFactory().build_from_conn(conn, "{slug}")
    (report_dir / f"{{slug}}_report.md").write_text(report, encoding="utf-8")

    conn.close()
    print(f"Built: {{DB_PATH}}")
    print(f"Graph: {{GEXF_PATH}}")


if __name__ == "__main__":
    main()
'''

    def _format_list(self, data: list[dict], name: str) -> str:
        import json
        lines = [f"{name} = ["]
        for i, item in enumerate(data):
            comma = "," if i < len(data) - 1 else ""
            serialized = json.dumps(item, ensure_ascii=False, indent=4)
            indented = "\n".join("    " + line for line in serialized.split("\n"))
            lines.append(f"{indented}{comma}")
        lines.append("]")
        return "\n".join(lines)
```

- [ ] **Step 4: 写 BuildScriptFactory 测试**

```python
# tests/test_factory/test_build_factory.py
"""Tests for BuildScriptFactory."""

import sqlite3
from pathlib import Path

from gov_relation.factory.build_factory import BuildScriptFactory


def test_generate_returns_valid_python_script(tmp_path):
    factory = BuildScriptFactory()
    province_dir = tmp_path / "sichuan"

    script = factory.generate(
        slug="锦江区",
        province_dir=province_dir,
        persons=[{"canonical_name": "张三", "birth_text": "1965", "gender": "男"}],
        organizations=[{"canonical_name": "中共锦江区委", "organization_type": "party"}],
        positions=[{
            "person_id": "", "organization_id": "",
            "title": "区委书记", "title_category": "党委正职",
            "start_text": "2022-01", "is_current": 1,
        }],
        relationships=[],
    )

    assert "#!/usr/bin/env python3" in script
    assert "锦江区" in script
    assert "PERSONS" in script
    assert "张三" in script
    assert "区委书记" in script

    # Verify it compiles
    script_path = tmp_path / "build_test_data.py"
    script_path.write_text(script, encoding="utf-8")
    import py_compile
    py_compile.compile(str(script_path), doraise=True)


def test_generated_script_includes_gexf_export(tmp_path):
    factory = BuildScriptFactory()
    script = factory.generate(
        slug="test",
        province_dir=tmp_path / "sichuan",
        persons=[{"canonical_name": "A", "birth_text": "1970"}],
        organizations=[{"canonical_name": "Org"}],
        positions=[],
        relationships=[],
    )
    assert "GEXFFactory" in script
    assert ".gexf" in script


def test_generated_script_includes_person_profiles(tmp_path):
    factory = BuildScriptFactory()
    script = factory.generate(
        slug="test",
        province_dir=tmp_path / "sichuan",
        persons=[{"canonical_name": "李四", "birth_text": "1975"}],
        organizations=[{"canonical_name": "Org"}],
        positions=[],
        relationships=[],
    )
    assert "PersonJSONFactory" in script
    assert "persons" in script
    assert "李四" in script
```

- [ ] **Step 5: 运行测试**

Run: `python3 -m pytest tests/test_factory/test_build_factory.py -v`
Expected: 3 PASS

- [ ] **Step 6: Commit**

```bash
git add gov_relation/factory/person_factory.py gov_relation/factory/report_factory.py gov_relation/factory/build_factory.py tests/test_factory/test_build_factory.py
git commit -m "feat(factory): add PersonJSONFactory, ReportFactory, BuildScriptFactory"
```

---

### Task 7: RegionResearchFactory — 统一入口

**Files:**
- Create: `gov_relation/factory/region_factory.py`
- Create: `tests/test_factory/test_region_factory.py`
- Modify: `gov_relation/factory/__init__.py`

**Interfaces:**
- Consumes: 所有 5 个子工厂
- Produces: `RegionResearchFactory(province, region, level, targets)` with `generate_build_script()`, `generate_gexf()`, `generate_person_profiles()`, `generate_report()`

- [ ] **Step 1: 写 RegionResearchFactory**

```python
# gov_relation/factory/region_factory.py
"""Top-level orchestrator: RegionResearchFactory."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from gov_relation.paths import (
    province_build_dir,
    province_database_dir,
    province_dir,
    province_graph_dir,
    province_persons_dir,
    province_reports_dir,
)

from .schema_factory import SchemaFactory
from .insert_factory import InsertFactory
from .build_factory import BuildScriptFactory
from .gexf_factory import GEXFFactory
from .person_factory import PersonJSONFactory
from .report_factory import ReportFactory


class RegionResearchFactory:
    """Unified factory for a single region's complete research package."""

    def __init__(
        self,
        *,
        province: str,
        region: str,
        level: str,
        targets: list[dict],
    ) -> None:
        self.province = province
        self.region = region
        self.level = level
        self.targets = targets
        self._persons: list[dict] = []
        self._organizations: list[dict] = []
        self._positions: list[dict] = []
        self._relationships: list[dict] = []
        self._sources: list[dict] = []

    def add_person(self, data: dict) -> None:
        self._persons.append(data)

    def add_organization(self, data: dict) -> None:
        self._organizations.append(data)

    def add_position(self, data: dict) -> None:
        self._positions.append(data)

    def add_relationship(self, data: dict) -> None:
        self._relationships.append(data)

    def add_source(self, data: dict) -> None:
        self._sources.append(data)

    def generate_build_script(self) -> Path:
        script_factory = BuildScriptFactory()
        # 修复（F9）：用 paths.province_dir()（绝对路径）替代"data/provinces"相对字面量，
        # 与 province_build_dir() 保持一致；province_dir.name 仍是 slug，供生成脚本定位。
        pd = province_dir(self.province)
        script = script_factory.generate(
            slug=self.region,
            province_dir=pd,
            persons=self._persons,
            organizations=self._organizations,
            positions=self._positions,
            relationships=self._relationships,
            sources=self._sources,
        )
        build_dir = province_build_dir(self.province)
        build_dir.mkdir(parents=True, exist_ok=True)
        path = build_dir / f"build_{self.region}_data.py"
        path.write_text(script, encoding="utf-8")
        return path

    def generate_gexf(self) -> Path:
        db_dir = province_database_dir(self.province)
        db_dir.mkdir(parents=True, exist_ok=True)
        db_path = db_dir / f"{self.region}_network.db"
        conn = sqlite3.connect(str(db_path))
        try:
            SchemaFactory().create_all(conn)
            f = InsertFactory()
            for p in self._persons:
                f.upsert_person(conn, p)
            for o in self._organizations:
                f.upsert_organization(conn, o)
            for pos in self._positions:
                f.insert_position(conn, pos)
            for rel in self._relationships:
                f.insert_relationship(conn, rel)
            for src in self._sources:
                f.insert_source(conn, src)
            conn.commit()

            graph_dir = province_graph_dir(self.province)
            graph_dir.mkdir(parents=True, exist_ok=True)
            gexf_path = graph_dir / f"{self.region}_network.gexf"
            GEXFFactory().write(conn, f"{self.region} 领导班子关系图", str(gexf_path))
            return gexf_path
        finally:
            conn.close()

    def generate_person_profiles(self) -> list[Path]:
        db_dir = province_database_dir(self.province)
        db_path = db_dir / f"{self.region}_network.db"
        if not db_path.exists():
            self.generate_gexf()

        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        try:
            pf = PersonJSONFactory()
            persons_dir = province_persons_dir(self.province)
            persons_dir.mkdir(parents=True, exist_ok=True)
            from datetime import date
            stamp = date.today().strftime("%Y%m%d")
            paths = []
            for row in conn.execute("SELECT person_id, canonical_name FROM persons"):
                pid, name = row[0], row[1]
                # 修复（F11）：文件名按 spec §10 格式 YYYYMMDD-省-市-职务-姓名.json
                job = conn.execute(
                    "SELECT title FROM positions WHERE person_id=? AND is_current=1 "
                    "ORDER BY sort_order LIMIT 1",
                    (pid,),
                ).fetchone()
                job_name = job[0] if job else "其他"
                path = persons_dir / f"{stamp}-{self.province}-{self.region}-{job_name}-{name}.json"
                pf.write(conn, pid, str(path))
                paths.append(path)
            return paths
        finally:
            conn.close()

    def generate_report(self) -> Path:
        db_dir = province_database_dir(self.province)
        db_path = db_dir / f"{self.region}_network.db"
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        try:
            report = ReportFactory().build_from_conn(conn, self.region)
            report_dir = province_reports_dir(self.province)
            report_dir.mkdir(parents=True, exist_ok=True)
            path = report_dir / f"{self.region}_report.md"
            path.write_text(report, encoding="utf-8")
            return path
        finally:
            conn.close()
```

- [ ] **Step 2: 写集成测试**

```python
# tests/test_factory/test_region_factory.py
"""Integration tests for RegionResearchFactory."""

import sqlite3
from pathlib import Path
from xml.etree import ElementTree as ET

from gov_relation.factory.region_factory import RegionResearchFactory


def test_full_pipeline_produces_db_gexf_profiles_report(tmp_path, monkeypatch):
    # Redirect output to tmp_path
    import gov_relation.paths
    monkeypatch.setattr(gov_relation.paths, "PROVINCES_DIR", tmp_path / "provinces")
    monkeypatch.setattr(
        gov_relation.paths, "PROVINCE_SLUGS",
        {"四川省": "sichuan"},
        raising=False,
    )

    factory = RegionResearchFactory(
        province="四川省",
        region="锦江区",
        level="county",
        targets=[{"role": "区委书记"}],
    )
    factory.add_person({"canonical_name": "张三", "birth_text": "1965-03", "gender": "男"})
    factory.add_person({"canonical_name": "李四", "birth_text": "1970-07", "gender": "女"})
    factory.add_organization({"canonical_name": "中共锦江区委", "organization_type": "party"})
    factory.add_organization({"canonical_name": "锦江区人民政府", "organization_type": "government"})

    # Generate build script
    build_path = factory.generate_build_script()
    assert build_path.exists()
    assert build_path.suffix == ".py"
    content = build_path.read_text()
    assert "张三" in content
    assert "锦江区" in content

    # Generate GEXF
    gexf_path = factory.generate_gexf()
    assert gexf_path.exists()
    assert gexf_path.suffix == ".gexf"
    xml = ET.parse(str(gexf_path))
    ns = {"g": "http://www.gexf.net/1.3"}
    nodes = xml.findall(".//g:node", ns)
    assert len(nodes) >= 2

    # Generate person profiles
    profiles = factory.generate_person_profiles()
    assert len(profiles) >= 2
    assert profiles[0].exists()

    # Generate report
    report_path = factory.generate_report()
    assert report_path.exists()
    report = report_path.read_text()
    assert "锦江区" in report


def test_empty_factory_still_produces_valid_outputs(tmp_path, monkeypatch):
    import gov_relation.paths
    monkeypatch.setattr(gov_relation.paths, "PROVINCES_DIR", tmp_path / "provinces")
    monkeypatch.setattr(gov_relation.paths, "PROVINCE_SLUGS", {"测试省": "test_prov"}, raising=False)

    factory = RegionResearchFactory(
        province="测试省", region="空白区", level="county", targets=[],
    )
    gexf_path = factory.generate_gexf()
    assert gexf_path.exists()
    report_path = factory.generate_report()
    assert report_path.exists()
```

- [ ] **Step 3: 运行集成测试**

Run: `python3 -m pytest tests/test_factory/test_region_factory.py -v`
Expected: 2 PASS

- [ ] **Step 4: 更新 __init__.py 导出**

```python
# gov_relation/factory/__init__.py (replace with full exports)
"""Factory layer for gov-relation v3 pipeline."""

from .schema_factory import SchemaFactory
from .insert_factory import InsertFactory
from .build_factory import BuildScriptFactory
from .gexf_factory import GEXFFactory
from .person_factory import PersonJSONFactory
from .report_factory import ReportFactory
from .region_factory import RegionResearchFactory

__all__ = [
    "SchemaFactory",
    "InsertFactory",
    "BuildScriptFactory",
    "GEXFFactory",
    "PersonJSONFactory",
    "ReportFactory",
    "RegionResearchFactory",
]
```

- [ ] **Step 5: 运行全部 factory 测试**

Run: `python3 -m pytest tests/test_factory/ -v`
Expected: 22 PASS（schema 4 + insert 10 + gexf 3 + build 3 + region 2）
> 评审确认：原计划 "约 20" 不准；插入 F5 碰撞回归测试后总数为 22。

- [ ] **Step 6: Commit**

```bash
git add gov_relation/factory/region_factory.py tests/test_factory/test_region_factory.py gov_relation/factory/__init__.py
git commit -m "feat(factory): add RegionResearchFactory as unified top-level entry point"
```

---

### Task 8: 创建省份目录骨架 + 合并外部数据

**Files:**
- (no code files)
- Create: `data/provinces/<31 provinces>/.gitkeep`
- Shell task: 合并 `/workspace/data/xieming/other-codes/data/` → repo

- [ ] **Step 1: 创建省份目录**

Run:
```bash
for prov in anhui beijing chongqing fujian gansu guangdong guangxi guizhou hainan hebei henan heilongjiang hubei hunan jilin jiangsu jiangxi liaoning inner_mongolia ningxia qinghai shandong shanxi shaanxi shanghai sichuan tianjin xizang xinjiang yunnan zhejiang; do
    for sub in build database graph persons reports; do
        mkdir -p "data/provinces/$prov/$sub"
        touch "data/provinces/$prov/$sub/.gitkeep"
    done
done
```

- [ ] **Step 2: 合并外部数据**

```bash
EXT_DIR="/workspace/data/xieming/other-codes/data"
REPO_ROOT="/workspace/data/xieming/other-codes/gov-relation"

# Copy databases
cp -n "$EXT_DIR/database/"*.db "$REPO_ROOT/data/database/" 2>/dev/null || true

# Copy graphs
cp -n "$EXT_DIR/graph/"*.gexf "$REPO_ROOT/data/graph/" 2>/dev/null || true

# Copy tmp staging dirs
cp -rn "$EXT_DIR/tmp/"* "$REPO_ROOT/data/tmp/" 2>/dev/null || true

echo "External data merged"
```

- [ ] **Step 3: 验证**

Run: `python3 -c "from gov_relation.paths import PROVINCES_DIR; print(f'Provinces dir: {PROVINCES_DIR}'); import os; print(f'Exists: {PROVINCES_DIR.exists()}'); dirs = [d.name for d in PROVINCES_DIR.iterdir() if d.is_dir()]; print(f'Count: {len(dirs)}')"`
Expected: 31 个省份目录

- [ ] **Step 4: Commit**

```bash
git add data/provinces/
git commit -m "feat(data): create province directory skeleton for 31 provinces"
```

---

### Task 9: 验证完整性 — 运行全量测试 + import 检查

- [ ] **Step 1: Run full test suite**

Run: `python3 -m pytest tests/ -v --tb=short`
Expected: All existing + new tests pass

- [ ] **Step 2: Verify all factory imports work**

Run:
```bash
python3 -c "
from gov_relation.factory import (
    SchemaFactory, InsertFactory, BuildScriptFactory,
    GEXFFactory, PersonJSONFactory, ReportFactory,
    RegionResearchFactory,
)
print('All factory imports OK')
print(f'SchemaFactory: {SchemaFactory}')
print(f'InsertFactory: {InsertFactory}')
print(f'RegionResearchFactory: {RegionResearchFactory}')
"
```

- [ ] **Step 3: 验证 inventory 不受影响**

Run: `python3 scripts/inventory.py`
Expected: 与重构前数据量一致

- [ ] **Step 4: Final commit**

```bash
# Nothing to commit if all tests pass — verification only
echo "Phase 1 complete"
```

---

## Phase 1 Completion Checklist

- [ ] `gov_relation/identity.py` — 核心函数从 platform/ 提升
- [ ] `gov_relation/paths.py` — PROVINCES_DIR + PROVINCE_SLUGS + 6 个 province_*() 函数
- [ ] `gov_relation/factory/schema_factory.py` — 21 表 + 6 view + 21 index 全部 DDL
- [ ] `gov_relation/factory/insert_factory.py` — 7 个 upsert/insert/link 方法
- [ ] `gov_relation/factory/gexf_factory.py` — DB → GEXF XML
- [ ] `gov_relation/factory/person_factory.py` — DB → Person JSON
- [ ] `gov_relation/factory/report_factory.py` — stats → Markdown
- [ ] `gov_relation/factory/build_factory.py` — 数据列表 → 完整可运行 .py 脚本
- [ ] `gov_relation/factory/region_factory.py` — 统一入口，协调所有子工厂
- [ ] `tests/test_factory/` — 全部 factory 单元测试 + 集成测试
- [ ] `data/provinces/` — 31 省目录骨架
- [ ] 外部数据合并
- [ ] 全量测试通过
