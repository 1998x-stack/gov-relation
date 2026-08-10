"""Quality and commercialization gates for the canonical database."""

from __future__ import annotations

import sqlite3
from typing import Any


def database_report(conn: sqlite3.Connection) -> dict[str, Any]:
    """Return deterministic health, coverage, and rights metrics."""
    tables = (
        "datasets", "raw_records", "persons", "organizations", "person_statuses",
        "positions", "relationships", "sources", "claims", "evidence_links",
        "profile_documents", "resolution_candidates", "quality_issues", "jurisdictions",
    )
    counts = {
        table: conn.execute(f"SELECT COUNT(*) FROM [{table}]").fetchone()[0]
        for table in tables
    }
    foreign_key_errors = [dict(row) for row in conn.execute("PRAGMA foreign_key_check")]
    open_issues = {
        row[0]: row[1]
        for row in conn.execute(
            "SELECT severity, COUNT(*) FROM quality_issues WHERE status='open' GROUP BY severity"
        )
    }
    issue_codes = {
        row[0]: row[1]
        for row in conn.execute(
            """SELECT issue_code, COUNT(*) FROM quality_issues
               WHERE status='open' GROUP BY issue_code ORDER BY COUNT(*) DESC"""
        )
    }
    rights = {
        row[0]: row[1]
        for row in conn.execute("SELECT rights_status, COUNT(*) FROM sources GROUP BY rights_status")
    }
    evidence = conn.execute(
        """SELECT
               SUM(CASE WHEN EXISTS (
                   SELECT 1 FROM evidence_links e
                   WHERE e.subject_type='position' AND e.subject_id=p.position_id
               ) THEN 1 ELSE 0 END),
               COUNT(*)
           FROM positions p"""
    ).fetchone()
    relationships = conn.execute(
        """SELECT
               SUM(CASE WHEN confidence='confirmed' THEN 1 ELSE 0 END),
               COUNT(*)
           FROM relationships"""
    ).fetchone()
    unresolved = conn.execute(
        "SELECT COUNT(*) FROM persons WHERE identity_status='unresolved'"
    ).fetchone()[0]
    commercial_counts = {
        entity: conn.execute(f"SELECT COUNT(*) FROM gold_commercial_{entity}").fetchone()[0]
        for entity in ("persons", "positions", "relationships", "claims")
    }
    return {
        "schema_version": conn.execute(
            "SELECT value FROM schema_meta WHERE key='schema_version'"
        ).fetchone()[0],
        "counts": counts,
        "foreign_key_errors": foreign_key_errors,
        "open_quality_issues": open_issues,
        "open_quality_issue_codes": issue_codes,
        "identity": {
            "unresolved_persons": unresolved,
            "unresolved_ratio": round(unresolved / counts["persons"], 6) if counts["persons"] else 0,
        },
        "evidence": {
            "positions_with_evidence": evidence[0] or 0,
            "positions_total": evidence[1],
            "confirmed_relationships": relationships[0] or 0,
            "relationships_total": relationships[1],
        },
        "rights": {
            "source_counts": rights,
            "commercially_cleared_sources": conn.execute(
                "SELECT COUNT(*) FROM gold_commercial_sources"
            ).fetchone()[0],
            "commercially_exportable": commercial_counts,
        },
        "commercial_release_ready": (
            not foreign_key_errors
            and not open_issues.get("error", 0)
            and sum(commercial_counts.values()) > 0
        ),
    }
