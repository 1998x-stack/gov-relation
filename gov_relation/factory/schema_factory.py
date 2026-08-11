"""Create the unified v3 SQLite schema for regional data packages."""

from __future__ import annotations

import re
import sqlite3

from gov_relation.platform.schema import DDL as PLATFORM_DDL

SCHEMA_VERSION = "3.0.0"

ENTITY_TABLES = (
    "jurisdictions",
    "persons",
    "person_aliases",
    "organizations",
    "positions",
    "relationships",
    "person_statuses",
)
EVIDENCE_TABLES = (
    "datasets",
    "raw_records",
    "profile_documents",
    "sources",
    "evidence_links",
    "claims",
    "entity_provenance",
    "quality_issues",
    "resolution_candidates",
)
RIGHTS_TABLES = (
    "rights_review_keys",
    "rights_manifests",
    "source_rights_decisions",
)
META_TABLES = ("schema_meta", "ingest_runs")

_V3_COLUMNS: dict[str, tuple[str, ...]] = {
    "persons": (
        "education TEXT NOT NULL DEFAULT ''",
        "merged_into_id TEXT REFERENCES persons(person_id)",
    ),
    "positions": (
        "title_category TEXT NOT NULL DEFAULT ''",
        "sort_order INTEGER NOT NULL DEFAULT 0",
    ),
    "datasets": (
        "commercial_use INTEGER NOT NULL DEFAULT 0 "
        "CHECK(commercial_use IN (0, 1))",
    ),
    "sources": (
        "commercial_use INTEGER NOT NULL DEFAULT 0 "
        "CHECK(commercial_use IN (0, 1))",
    ),
}

_VIEWS = (
    """CREATE VIEW IF NOT EXISTS gold_current_positions AS
       SELECT p.person_id, p.canonical_name, ps.title,
              o.canonical_name AS organization_name, ps.rank,
              ps.start_text, ps.end_text, ps.confidence
       FROM positions ps
       JOIN persons p ON p.person_id = ps.person_id
       LEFT JOIN organizations o ON o.organization_id = ps.organization_id
       WHERE ps.is_current = 1""",
    """CREATE VIEW IF NOT EXISTS gold_relationship_edges AS
       SELECT r.relationship_id, a.canonical_name AS person_from,
              b.canonical_name AS person_to, r.relationship_type,
              r.direction, r.strength, r.confidence, r.context,
              r.overlap_period_text
       FROM relationships r
       JOIN persons a ON a.person_id = r.person_from_id
       JOIN persons b ON b.person_id = r.person_to_id""",
    """CREATE VIEW IF NOT EXISTS gold_commercial_sources AS
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
               AND (d2.effective_to IS NULL
                    OR datetime(d2.effective_to) >= CURRENT_TIMESTAMP)
             ORDER BY datetime(d2.effective_from) DESC, d2.rowid DESC
             LIMIT 1
         )""",
    """CREATE VIEW IF NOT EXISTS gold_commercial_persons AS
       SELECT DISTINCT p.* FROM persons p
       JOIN evidence_links e
         ON e.subject_type = 'person' AND e.subject_id = p.person_id
       JOIN gold_commercial_sources s ON s.source_id = e.source_id""",
    """CREATE VIEW IF NOT EXISTS gold_commercial_positions AS
       SELECT DISTINCT p.* FROM positions p
       JOIN evidence_links e
         ON e.subject_type = 'position' AND e.subject_id = p.position_id
       JOIN gold_commercial_sources s ON s.source_id = e.source_id""",
    """CREATE VIEW IF NOT EXISTS gold_commercial_relationships AS
       SELECT DISTINCT r.* FROM relationships r
       JOIN evidence_links e
         ON e.subject_type = 'relationship' AND e.subject_id = r.relationship_id
       JOIN gold_commercial_sources s ON s.source_id = e.source_id""",
)

_VIEW_NAMES = (
    "gold_commercial_relationships",
    "gold_commercial_positions",
    "gold_commercial_persons",
    "gold_commercial_sources",
    "gold_relationship_edges",
    "gold_current_positions",
)

_INDEXES = (
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
)


def _table_statement(table: str) -> str:
    pattern = re.compile(
        rf"CREATE TABLE IF NOT EXISTS {re.escape(table)}\s*\(.*?\n\);",
        re.DOTALL,
    )
    match = pattern.search(PLATFORM_DDL)
    if match is None:
        raise RuntimeError(f"platform DDL is missing table {table}")
    return match.group(0).rstrip(";")


def _columns(conn: sqlite3.Connection, table: str) -> set[str]:
    return {row[1] for row in conn.execute(f"PRAGMA table_info('{table}')")}


class SchemaFactory:
    """Create the 21-table v3 schema, six gold views, and indexes."""

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
            "INSERT OR REPLACE INTO schema_meta(key, value) VALUES(?, ?)",
            ("schema_version", SCHEMA_VERSION),
        )
        conn.commit()

    def _create_tables(
        self, conn: sqlite3.Connection, tables: tuple[str, ...]
    ) -> None:
        for table in tables:
            conn.execute(_table_statement(table))
            existing = _columns(conn, table)
            for definition in _V3_COLUMNS.get(table, ()):
                column = definition.split(None, 1)[0]
                if column not in existing:
                    conn.execute(f"ALTER TABLE {table} ADD COLUMN {definition}")

    def create_entity_tables(self, conn: sqlite3.Connection) -> None:
        self._create_tables(conn, ENTITY_TABLES)

    def create_evidence_tables(self, conn: sqlite3.Connection) -> None:
        self._create_tables(conn, EVIDENCE_TABLES)

    def create_rights_tables(self, conn: sqlite3.Connection) -> None:
        self._create_tables(conn, RIGHTS_TABLES)

    def create_meta_tables(self, conn: sqlite3.Connection) -> None:
        self._create_tables(conn, META_TABLES)

    def create_views(self, conn: sqlite3.Connection) -> None:
        for name in _VIEW_NAMES:
            conn.execute(f"DROP VIEW IF EXISTS {name}")
        for ddl in _VIEWS:
            conn.execute(ddl)

    def create_indexes(self, conn: sqlite3.Connection) -> None:
        for ddl in _INDEXES:
            conn.execute(ddl)
