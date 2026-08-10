"""Versioned SQLite schema for the canonical government relationship database."""

from __future__ import annotations

import sqlite3
from pathlib import Path

SCHEMA_VERSION = "2.1.0"
ADDITIVE_SCHEMA_UPGRADES = {"2.0.0"}

DDL = """
CREATE TABLE IF NOT EXISTS schema_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS jurisdictions (
    jurisdiction_id TEXT PRIMARY KEY,
    parent_id TEXT REFERENCES jurisdictions(jurisdiction_id),
    name TEXT NOT NULL,
    normalized_name TEXT NOT NULL,
    administrative_code TEXT,
    level TEXT NOT NULL DEFAULT 'unknown',
    province_name TEXT NOT NULL DEFAULT '',
    prefecture_name TEXT NOT NULL DEFAULT '',
    county_name TEXT NOT NULL DEFAULT '',
    valid_from TEXT,
    valid_to TEXT,
    UNIQUE(parent_id, normalized_name, level)
);

CREATE TABLE IF NOT EXISTS datasets (
    dataset_id TEXT PRIMARY KEY,
    dataset_key TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    kind TEXT NOT NULL CHECK(kind IN ('legacy_sqlite', 'person_profile', 'research_package', 'manual')),
    source_path TEXT NOT NULL,
    content_sha256 TEXT NOT NULL,
    jurisdiction_id TEXT REFERENCES jurisdictions(jurisdiction_id),
    rights_status TEXT NOT NULL DEFAULT 'unknown'
        CHECK(rights_status IN ('unknown', 'cleared', 'restricted')),
    commercial_use_allowed INTEGER NOT NULL DEFAULT 0 CHECK(commercial_use_allowed IN (0, 1)),
    imported_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ingest_runs (
    run_id TEXT PRIMARY KEY,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    mode TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('running', 'succeeded', 'failed', 'partial')),
    input_count INTEGER NOT NULL DEFAULT 0,
    imported_count INTEGER NOT NULL DEFAULT 0,
    rejected_count INTEGER NOT NULL DEFAULT 0,
    error TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS raw_records (
    raw_record_id TEXT PRIMARY KEY,
    dataset_id TEXT NOT NULL REFERENCES datasets(dataset_id),
    source_table TEXT NOT NULL,
    source_pk TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    payload_sha256 TEXT NOT NULL,
    imported_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(dataset_id, source_table, source_pk)
);

CREATE TABLE IF NOT EXISTS persons (
    person_id TEXT PRIMARY KEY,
    canonical_name TEXT NOT NULL,
    normalized_name TEXT NOT NULL,
    gender TEXT NOT NULL DEFAULT '',
    ethnicity TEXT NOT NULL DEFAULT '',
    birth_text TEXT NOT NULL DEFAULT '',
    birth_precision TEXT NOT NULL DEFAULT 'unknown'
        CHECK(birth_precision IN ('day', 'month', 'year', 'unknown')),
    birthplace TEXT NOT NULL DEFAULT '',
    native_place TEXT NOT NULL DEFAULT '',
    party_join_text TEXT NOT NULL DEFAULT '',
    work_start_text TEXT NOT NULL DEFAULT '',
    identity_status TEXT NOT NULL DEFAULT 'unresolved'
        CHECK(identity_status IN ('verified', 'probable', 'unresolved', 'merged')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS person_aliases (
    person_id TEXT NOT NULL REFERENCES persons(person_id),
    alias TEXT NOT NULL,
    normalized_alias TEXT NOT NULL,
    alias_type TEXT NOT NULL DEFAULT 'other',
    PRIMARY KEY(person_id, normalized_alias)
);

CREATE TABLE IF NOT EXISTS organizations (
    organization_id TEXT PRIMARY KEY,
    jurisdiction_id TEXT REFERENCES jurisdictions(jurisdiction_id),
    parent_organization_id TEXT REFERENCES organizations(organization_id),
    canonical_name TEXT NOT NULL,
    normalized_name TEXT NOT NULL,
    organization_type TEXT NOT NULL DEFAULT '',
    administrative_level TEXT NOT NULL DEFAULT '',
    location_text TEXT NOT NULL DEFAULT '',
    valid_from TEXT,
    valid_to TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS person_statuses (
    status_id TEXT PRIMARY KEY,
    person_id TEXT NOT NULL REFERENCES persons(person_id),
    post_text TEXT NOT NULL DEFAULT '',
    organization_text TEXT NOT NULL DEFAULT '',
    administrative_rank TEXT NOT NULL DEFAULT '',
    observed_at TEXT,
    is_current_confirmed INTEGER NOT NULL DEFAULT 0 CHECK(is_current_confirmed IN (0, 1)),
    confidence TEXT NOT NULL DEFAULT 'unverified'
        CHECK(confidence IN ('confirmed', 'plausible', 'unverified'))
);

CREATE TABLE IF NOT EXISTS positions (
    position_id TEXT PRIMARY KEY,
    person_id TEXT NOT NULL REFERENCES persons(person_id),
    organization_id TEXT REFERENCES organizations(organization_id),
    organization_text TEXT NOT NULL DEFAULT '',
    title TEXT NOT NULL DEFAULT '',
    rank TEXT NOT NULL DEFAULT '',
    category TEXT NOT NULL DEFAULT '',
    start_text TEXT NOT NULL DEFAULT '',
    end_text TEXT NOT NULL DEFAULT '',
    start_date TEXT,
    end_date TEXT,
    date_precision TEXT NOT NULL DEFAULT 'unknown'
        CHECK(date_precision IN ('day', 'month', 'year', 'range', 'unknown')),
    is_current INTEGER NOT NULL DEFAULT 0 CHECK(is_current IN (0, 1)),
    confidence TEXT NOT NULL DEFAULT 'unverified'
        CHECK(confidence IN ('confirmed', 'plausible', 'unverified')),
    notes TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS relationships (
    relationship_id TEXT PRIMARY KEY,
    person_from_id TEXT NOT NULL REFERENCES persons(person_id),
    person_to_id TEXT NOT NULL REFERENCES persons(person_id),
    relationship_type TEXT NOT NULL,
    direction TEXT NOT NULL DEFAULT 'undirected'
        CHECK(direction IN ('undirected', 'from_to', 'to_from')),
    strength TEXT NOT NULL DEFAULT 'unknown'
        CHECK(strength IN ('strong', 'medium', 'weak', 'unknown')),
    confidence TEXT NOT NULL DEFAULT 'unverified'
        CHECK(confidence IN ('confirmed', 'plausible', 'unverified')),
    context TEXT NOT NULL DEFAULT '',
    evidence_summary TEXT NOT NULL DEFAULT '',
    overlap_organization_id TEXT REFERENCES organizations(organization_id),
    overlap_organization_text TEXT NOT NULL DEFAULT '',
    overlap_period_text TEXT NOT NULL DEFAULT '',
    valid_from TEXT,
    valid_to TEXT,
    CHECK(person_from_id <> person_to_id)
);

CREATE TABLE IF NOT EXISTS sources (
    source_id TEXT PRIMARY KEY,
    canonical_url TEXT NOT NULL DEFAULT '',
    title TEXT NOT NULL DEFAULT '',
    publisher TEXT NOT NULL DEFAULT '',
    published_at TEXT,
    accessed_at TEXT,
    source_type TEXT NOT NULL DEFAULT 'database'
        CHECK(source_type IN ('official', 'appointment_notice', 'media', 'encyclopedia', 'database', 'inferred', 'other')),
    reliability TEXT NOT NULL DEFAULT 'low' CHECK(reliability IN ('high', 'medium', 'low')),
    rights_status TEXT NOT NULL DEFAULT 'unknown'
        CHECK(rights_status IN ('unknown', 'cleared', 'restricted')),
    commercial_use_allowed INTEGER NOT NULL DEFAULT 0 CHECK(commercial_use_allowed IN (0, 1)),
    content_sha256 TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS claims (
    claim_id TEXT PRIMARY KEY,
    subject_type TEXT NOT NULL,
    subject_id TEXT NOT NULL,
    predicate TEXT NOT NULL,
    value_json TEXT NOT NULL,
    valid_from TEXT,
    valid_to TEXT,
    observed_at TEXT,
    confidence TEXT NOT NULL DEFAULT 'unverified'
        CHECK(confidence IN ('confirmed', 'plausible', 'unverified')),
    review_status TEXT NOT NULL DEFAULT 'pending'
        CHECK(review_status IN ('pending', 'accepted', 'rejected', 'superseded'))
);

CREATE TABLE IF NOT EXISTS evidence_links (
    evidence_id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL REFERENCES sources(source_id),
    subject_type TEXT NOT NULL,
    subject_id TEXT NOT NULL,
    field_name TEXT NOT NULL DEFAULT '',
    claim_text TEXT NOT NULL DEFAULT '',
    locator TEXT NOT NULL DEFAULT '',
    confidence TEXT NOT NULL DEFAULT 'unverified'
        CHECK(confidence IN ('confirmed', 'plausible', 'unverified')),
    UNIQUE(source_id, subject_type, subject_id, field_name, locator)
);

CREATE TABLE IF NOT EXISTS entity_provenance (
    provenance_id TEXT PRIMARY KEY,
    dataset_id TEXT NOT NULL REFERENCES datasets(dataset_id),
    raw_record_id TEXT REFERENCES raw_records(raw_record_id),
    entity_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    source_field TEXT NOT NULL DEFAULT '',
    transformation TEXT NOT NULL DEFAULT '',
    UNIQUE(dataset_id, raw_record_id, entity_type, entity_id, source_field)
);

CREATE TABLE IF NOT EXISTS profile_documents (
    profile_id TEXT PRIMARY KEY,
    person_id TEXT NOT NULL REFERENCES persons(person_id),
    raw_record_id TEXT NOT NULL REFERENCES raw_records(raw_record_id),
    schema_version TEXT NOT NULL DEFAULT '',
    generated_at TEXT NOT NULL DEFAULT '',
    profile_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS resolution_candidates (
    candidate_id TEXT PRIMARY KEY,
    left_entity_id TEXT NOT NULL,
    right_entity_id TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    score REAL NOT NULL CHECK(score >= 0 AND score <= 1),
    reasons_json TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK(status IN ('pending', 'merged', 'rejected')),
    UNIQUE(left_entity_id, right_entity_id, entity_type)
);

CREATE TABLE IF NOT EXISTS quality_issues (
    issue_id TEXT PRIMARY KEY,
    dataset_id TEXT REFERENCES datasets(dataset_id),
    raw_record_id TEXT REFERENCES raw_records(raw_record_id),
    severity TEXT NOT NULL CHECK(severity IN ('error', 'warning', 'info')),
    issue_code TEXT NOT NULL,
    entity_type TEXT NOT NULL DEFAULT '',
    entity_id TEXT NOT NULL DEFAULT '',
    message TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open', 'resolved', 'ignored')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rights_review_keys (
    key_id TEXT PRIMARY KEY,
    algorithm TEXT NOT NULL CHECK(algorithm = 'ecdsa-p256-sha256'),
    public_key_pem TEXT NOT NULL,
    reviewer_identity TEXT NOT NULL,
    review_authority TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'revoked')),
    valid_from TEXT NOT NULL,
    valid_to TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rights_manifests (
    manifest_id TEXT PRIMARY KEY,
    schema_version TEXT NOT NULL,
    payload_sha256 TEXT NOT NULL,
    signature_algorithm TEXT NOT NULL,
    signature_key_id TEXT NOT NULL,
    signature_base64 TEXT NOT NULL,
    created_at TEXT NOT NULL,
    reviewed_by TEXT NOT NULL,
    review_authority TEXT NOT NULL,
    legal_memo_ref TEXT NOT NULL DEFAULT '',
    effective_from TEXT NOT NULL,
    effective_to TEXT,
    applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS source_rights_decisions (
    decision_row_id TEXT PRIMARY KEY,
    decision_id TEXT NOT NULL,
    manifest_id TEXT NOT NULL REFERENCES rights_manifests(manifest_id),
    source_id TEXT NOT NULL REFERENCES sources(source_id),
    decision TEXT NOT NULL CHECK(decision IN ('unknown', 'cleared', 'restricted')),
    permitted_uses_json TEXT NOT NULL,
    permitted_fields_json TEXT NOT NULL,
    restrictions_json TEXT NOT NULL,
    rationale TEXT NOT NULL,
    effective_from TEXT NOT NULL,
    effective_to TEXT,
    UNIQUE(manifest_id, decision_id, source_id)
);

CREATE INDEX IF NOT EXISTS idx_persons_name ON persons(normalized_name);
CREATE INDEX IF NOT EXISTS idx_orgs_name ON organizations(normalized_name);
CREATE INDEX IF NOT EXISTS idx_positions_person ON positions(person_id, start_date, end_date);
CREATE INDEX IF NOT EXISTS idx_positions_org ON positions(organization_id);
CREATE INDEX IF NOT EXISTS idx_relationships_from ON relationships(person_from_id);
CREATE INDEX IF NOT EXISTS idx_relationships_to ON relationships(person_to_id);
CREATE INDEX IF NOT EXISTS idx_sources_url ON sources(canonical_url);
CREATE INDEX IF NOT EXISTS idx_evidence_subject ON evidence_links(subject_type, subject_id);
CREATE INDEX IF NOT EXISTS idx_provenance_entity ON entity_provenance(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_quality_status ON quality_issues(status, severity, issue_code);
CREATE INDEX IF NOT EXISTS idx_rights_decisions_source
    ON source_rights_decisions(source_id, effective_from, effective_to);

DROP VIEW IF EXISTS gold_commercial_claims;
DROP VIEW IF EXISTS gold_commercial_relationships;
DROP VIEW IF EXISTS gold_commercial_positions;
DROP VIEW IF EXISTS gold_commercial_persons;
DROP VIEW IF EXISTS gold_commercial_sources;
DROP VIEW IF EXISTS gold_relationship_edges;
DROP VIEW IF EXISTS gold_current_positions;

CREATE VIEW IF NOT EXISTS gold_current_positions AS
SELECT p.person_id, p.canonical_name, ps.title, o.canonical_name AS organization_name,
       ps.rank, ps.start_text, ps.end_text, ps.confidence
FROM positions ps
JOIN persons p ON p.person_id = ps.person_id
LEFT JOIN organizations o ON o.organization_id = ps.organization_id
WHERE ps.is_current = 1;

CREATE VIEW IF NOT EXISTS gold_relationship_edges AS
SELECT r.relationship_id, a.canonical_name AS person_from, b.canonical_name AS person_to,
       r.relationship_type, r.direction, r.strength, r.confidence,
       r.context, r.overlap_period_text
FROM relationships r
JOIN persons a ON a.person_id = r.person_from_id
JOIN persons b ON b.person_id = r.person_to_id;

CREATE VIEW IF NOT EXISTS gold_commercial_sources AS
SELECT s.* FROM sources s
JOIN source_rights_decisions d ON d.source_id=s.source_id
WHERE d.decision='cleared'
  AND instr(d.permitted_uses_json, '"commercial_distribution"') > 0
  AND datetime(d.effective_from) <= CURRENT_TIMESTAMP
  AND (d.effective_to IS NULL OR datetime(d.effective_to) >= CURRENT_TIMESTAMP)
  AND d.rowid = (
      SELECT d2.rowid FROM source_rights_decisions d2
      WHERE d2.source_id=s.source_id
        AND datetime(d2.effective_from) <= CURRENT_TIMESTAMP
        AND (d2.effective_to IS NULL OR datetime(d2.effective_to) >= CURRENT_TIMESTAMP)
      ORDER BY datetime(d2.effective_from) DESC, d2.rowid DESC
      LIMIT 1
  );

CREATE VIEW IF NOT EXISTS gold_commercial_persons AS
SELECT DISTINCT p.* FROM persons p
JOIN evidence_links e ON e.subject_type='person' AND e.subject_id=p.person_id
JOIN gold_commercial_sources s ON s.source_id=e.source_id;

CREATE VIEW IF NOT EXISTS gold_commercial_positions AS
SELECT DISTINCT p.* FROM positions p
JOIN evidence_links e ON e.subject_type='position' AND e.subject_id=p.position_id
JOIN gold_commercial_sources s ON s.source_id=e.source_id;

CREATE VIEW IF NOT EXISTS gold_commercial_relationships AS
SELECT DISTINCT r.* FROM relationships r
JOIN evidence_links e ON e.subject_type='relationship' AND e.subject_id=r.relationship_id
JOIN gold_commercial_sources s ON s.source_id=e.source_id;

CREATE VIEW IF NOT EXISTS gold_commercial_claims AS
SELECT DISTINCT c.* FROM claims c
JOIN evidence_links e ON e.subject_type='claim' AND e.subject_id=c.claim_id
JOIN gold_commercial_sources s ON s.source_id=e.source_id;
"""


def connect(path: str | Path, *, read_only: bool = False) -> sqlite3.Connection:
    """Open a configured canonical database connection."""
    db_path = Path(path).resolve()
    if read_only:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    else:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(db_path))
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


def create_schema(conn: sqlite3.Connection) -> None:
    """Create or verify the canonical schema."""
    has_meta = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='schema_meta'"
    ).fetchone()
    current = None
    if has_meta:
        row = conn.execute(
            "SELECT value FROM schema_meta WHERE key='schema_version'"
        ).fetchone()
        current = row[0] if row else None
    if current and current != SCHEMA_VERSION and current not in ADDITIVE_SCHEMA_UPGRADES:
        raise RuntimeError(
            f"Database schema {current} is incompatible with code schema {SCHEMA_VERSION}"
        )
    conn.executescript(DDL)
    conn.execute(
        "INSERT OR REPLACE INTO schema_meta(key, value) VALUES('schema_version', ?)",
        (SCHEMA_VERSION,),
    )
    conn.commit()
