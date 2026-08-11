"""Generate promotion-compatible person profile JSON documents."""

from __future__ import annotations

import json
import sqlite3
from datetime import date
from pathlib import Path


def _rows_as_dicts(cursor: sqlite3.Cursor) -> list[dict]:
    columns = [item[0] for item in cursor.description or ()]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


class PersonJSONFactory:
    """Build a profile from v3 entities and their linked sources."""

    def build(self, conn: sqlite3.Connection, person_id: str) -> dict:
        cursor = conn.execute("SELECT * FROM persons WHERE person_id=?", (person_id,))
        rows = _rows_as_dicts(cursor)
        if not rows:
            raise ValueError(f"Person not found: {person_id}")
        person = rows[0]
        positions = _rows_as_dicts(
            conn.execute(
                """SELECT * FROM positions WHERE person_id=?
                   ORDER BY sort_order, start_date, start_text""",
                (person_id,),
            )
        )
        relationships = _rows_as_dicts(
            conn.execute(
                """SELECT r.*,
                          CASE WHEN r.person_from_id=? THEN target.canonical_name
                               ELSE source.canonical_name END AS related_person_name
                   FROM relationships r
                   JOIN persons source ON source.person_id=r.person_from_id
                   JOIN persons target ON target.person_id=r.person_to_id
                   WHERE r.person_from_id=? OR r.person_to_id=?""",
                (person_id, person_id, person_id),
            )
        )
        subject_ids = [person_id]
        subject_ids.extend(item["position_id"] for item in positions)
        subject_ids.extend(item["relationship_id"] for item in relationships)
        placeholders = ",".join("?" for _ in subject_ids)
        sources = _rows_as_dicts(
            conn.execute(
                f"""SELECT DISTINCT s.source_id, s.canonical_url, s.title,
                           s.publisher, s.published_at, s.accessed_at,
                           s.source_type, s.reliability
                    FROM sources s
                    JOIN evidence_links e ON e.source_id=s.source_id
                    WHERE e.subject_id IN ({placeholders})
                    ORDER BY s.source_id""",
                subject_ids,
            )
        )
        current = next((item for item in positions if item["is_current"]), None)
        return {
            "schema_version": "3.0",
            "generated_at": date.today().isoformat(),
            "person_id": person_id,
            "investigation_scope": {
                "province": "",
                "city": "",
                "region": "",
                "job": current["title"] if current else "",
            },
            "identity": {
                "name": person["canonical_name"],
                "gender": person["gender"],
                "ethnicity": person["ethnicity"],
                "birth": person["birth_text"],
                "birthplace": person["birthplace"],
                "native_place": person["native_place"],
                "education": person["education"],
            },
            "current_status": {
                "current_post": current["title"] if current else "",
                "current_organization": (
                    current["organization_text"] if current else ""
                ),
            },
            "career_timeline": [
                {
                    "title": item["title"],
                    "org": item["organization_text"],
                    "start": item["start_text"],
                    "end": item["end_text"],
                    "rank": item["rank"],
                    "is_current": bool(item["is_current"]),
                }
                for item in positions
            ],
            "relationships": [
                {
                    "person": item["related_person_name"],
                    "type": item["relationship_type"],
                    "context": item["context"],
                    "overlap_period": item["overlap_period_text"],
                }
                for item in relationships
            ],
            "source_register": sources,
            "open_questions": [],
        }

    def write(
        self, conn: sqlite3.Connection, person_id: str, path: str | Path
    ) -> None:
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(self.build(conn, person_id), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
