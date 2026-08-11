"""Build complete GEXF documents from v3 SQLite data."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from gov_relation.gexf import GEXFBuilder


def _node_id(kind: str, entity_id: str) -> str:
    """Return a collision-free, type-scoped node identifier."""
    return f"{kind}:{entity_id}"


class GEXFFactory:
    """Render persons, organizations, and relationships from a v3 database."""

    def build(self, conn: sqlite3.Connection, title: str) -> str:
        builder = GEXFBuilder(title=title)
        for row in conn.execute(
            "SELECT person_id, canonical_name, gender, birth_text FROM persons"
        ):
            status = conn.execute(
                """SELECT post_text FROM person_statuses
                   WHERE person_id=? AND is_current_confirmed=1
                   ORDER BY observed_at DESC LIMIT 1""",
                (row[0],),
            ).fetchone()
            if status is None:
                status = conn.execute(
                    """SELECT title FROM positions
                       WHERE person_id=? AND is_current=1
                       ORDER BY sort_order, start_date DESC LIMIT 1""",
                    (row[0],),
                ).fetchone()
            builder.add_person(
                id=_node_id("person", row[0]),
                name=row[1],
                current_post=status[0] if status else "",
                gender=row[2] or "",
                birth=row[3] or "",
            )
        for row in conn.execute(
            "SELECT organization_id, canonical_name, organization_type, "
            "administrative_level, location_text FROM organizations"
        ):
            builder.add_organization(
                id=_node_id("organization", row[0]),
                name=row[1],
                org_type=row[2] or "",
                level=row[3] or "",
                location=row[4] or "",
            )
        for row in conn.execute(
            """SELECT person_from_id, person_to_id, relationship_type,
                      context, overlap_organization_text, overlap_period_text
               FROM relationships"""
        ):
            builder.add_relationship(
                _node_id("person", row[0]),
                _node_id("person", row[1]),
                row[2],
                context=row[3] or "",
                overlap_org=row[4] or "",
                overlap_period=row[5] or "",
            )
        return builder.to_string()

    def write(
        self,
        conn: sqlite3.Connection,
        title: str,
        path: str | Path,
    ) -> None:
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(self.build(conn, title), encoding="utf-8")
