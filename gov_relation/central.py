"""Central registry writer — province-partitioned SQLite with hash-based dedup.

Each :class:`Central` instance targets one province partition (one SQLite file).
Use one instance per province per build.

The class is idempotent: calling merge methods with the same data
repeatedly produces the same result (id_hash).
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .hash import org_hash, person_hash
from .paths import PROVINCE_DIR
from .schema import create_central_schema, create_registry_schema


class Central:
    """Province-partitioned central registry writer."""

    def __init__(self, province: str) -> None:
        self.province = province
        PROVINCE_DIR.mkdir(parents=True, exist_ok=True)
        self.db_path = PROVINCE_DIR / f"{province}.db"
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA foreign_keys=ON")
        create_central_schema(self.conn)

    # ── Person upsert ──────────────────────────────────────────────

    def merge_person(self, person: dict[str, Any]) -> str:
        """Upsert a person record keyed by content hash.  Returns id_hash."""
        name = person.get("name", "")
        birth = person.get("birth", "")
        h = person_hash(name, birth)

        existing = self.conn.execute(
            "SELECT * FROM persons WHERE id_hash=?", (h,)
        ).fetchone()

        if existing:
            aliases = json.loads(existing["aliases"] or "[]")
            source_json = json.loads(existing["source_json"] or "{}")
            src = person.get("source", "")
            if src and src not in source_json:
                source_json[src] = "migrated"
            if name and name != existing["name"] and name not in aliases:
                aliases.append(name)

            self.conn.execute(
                """UPDATE persons SET
                    name=COALESCE(NULLIF(?, ''), name),
                    name_normalized=COALESCE(NULLIF(?, ''), name_normalized),
                    gender=COALESCE(NULLIF(?, ''), gender),
                    ethnicity=COALESCE(NULLIF(?, ''), ethnicity),
                    birthplace=COALESCE(NULLIF(?, ''), birthplace),
                    education=COALESCE(NULLIF(?, ''), education),
                    party_join=COALESCE(NULLIF(?, ''), party_join),
                    work_start=COALESCE(NULLIF(?, ''), work_start),
                    aliases=?,
                    source_json=?,
                    updated_at=datetime('now')
                WHERE id_hash=?""",
                (
                    name,
                    name,
                    person.get("gender", ""),
                    person.get("ethnicity", ""),
                    person.get("birthplace", ""),
                    person.get("education", ""),
                    person.get("party_join", ""),
                    person.get("work_start", ""),
                    json.dumps(aliases, ensure_ascii=False),
                    json.dumps(source_json, ensure_ascii=False),
                    h,
                ),
            )
        else:
            self.conn.execute(
                """INSERT INTO persons
                   (id_hash, name, name_normalized, gender, ethnicity,
                    birth, birthplace, education, party_join, work_start, source_json)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    h,
                    name,
                    name,
                    person.get("gender", ""),
                    person.get("ethnicity", ""),
                    birth,
                    person.get("birthplace", ""),
                    person.get("education", ""),
                    person.get("party_join", ""),
                    person.get("work_start", ""),
                    json.dumps({person.get("source", ""): "high"}, ensure_ascii=False),
                ),
            )
        self.conn.commit()
        return h

    # ── Organization upsert ────────────────────────────────────────

    def merge_organization(self, org: dict[str, Any]) -> str:
        """Upsert an organization keyed by content hash.  Returns id_hash."""
        province = org.get("province", self.province)
        fqn = org.get("fqn", org.get("name", ""))
        h = org_hash(province, fqn)

        existing = self.conn.execute(
            "SELECT * FROM organizations WHERE id_hash=?", (h,)
        ).fetchone()

        if existing:
            self.conn.execute(
                """UPDATE organizations SET
                    org_type=COALESCE(NULLIF(?, ''), org_type),
                    level=COALESCE(NULLIF(?, ''), level),
                    parent_fqn=COALESCE(NULLIF(?, ''), parent_fqn),
                    local_name=COALESCE(NULLIF(?, ''), local_name),
                    location=COALESCE(NULLIF(?, ''), location)
                WHERE id_hash=?""",
                (
                    org.get("org_type", ""),
                    org.get("level", ""),
                    org.get("parent", ""),
                    org.get("local_name", fqn),
                    org.get("location", ""),
                    h,
                ),
            )
        else:
            self.conn.execute(
                """INSERT INTO organizations
                   (id_hash, fqn, local_name, org_type, level, parent_fqn, location, province)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    h, fqn,
                    org.get("local_name", fqn),
                    org.get("org_type", ""),
                    org.get("level", ""),
                    org.get("parent", ""),
                    org.get("location", ""),
                    province,
                ),
            )
        self.conn.commit()
        return h

    # ── Position insert ────────────────────────────────────────────

    def insert_position(self, pos: dict[str, Any]) -> int:
        """Insert a position record.  Returns the new row id."""
        cur = self.conn.execute(
            """INSERT INTO positions
               (person_hash, org_hash, title, start_date, end_date,
                rank, category, note, province, source)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                pos["person_hash"],
                pos["org_hash"],
                pos.get("title", ""),
                pos.get("start_date", ""),
                pos.get("end_date", ""),
                pos.get("rank", ""),
                pos.get("category", ""),
                pos.get("note", ""),
                pos.get("province", self.province),
                pos.get("source", ""),
            ),
        )
        self.conn.commit()
        # lastrowid is never None for an AUTOINCREMENT insert
        return cur.lastrowid  # type: ignore[return-value]

    # ── Relationship insert ────────────────────────────────────────

    def insert_relationship(self, rel: dict[str, Any]) -> int:
        """Insert a relationship record.  Returns the new row id."""
        cur = self.conn.execute(
            """INSERT INTO relationships
               (person_a_hash, person_b_hash, type, context,
                overlap_org_hash, overlap_period, province, source)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                rel["person_a_hash"],
                rel["person_b_hash"],
                rel.get("type", ""),
                rel.get("context", ""),
                rel.get("overlap_org_hash") or None,
                rel.get("overlap_period", ""),
                rel.get("province", self.province),
                rel.get("source", ""),
            ),
        )
        self.conn.commit()
        return cur.lastrowid  # type: ignore[return-value]

    # ── Cleanup & registry ─────────────────────────────────────────

    def close(self) -> None:
        """Close the underlying SQLite connection."""
        self.conn.close()

    def flush_registry(self, registry_path: str | Path) -> None:
        """Write partition stats to a registry DB at *registry_path*."""
        reg = sqlite3.connect(str(registry_path))
        create_registry_schema(reg)
        p = self.conn.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
        o = self.conn.execute("SELECT COUNT(*) FROM organizations").fetchone()[0]
        ps = self.conn.execute("SELECT COUNT(*) FROM positions").fetchone()[0]
        r = self.conn.execute("SELECT COUNT(*) FROM relationships").fetchone()[0]
        reg.execute(
            """INSERT OR REPLACE INTO region_registry
               (province, db_path, status, person_count, org_count,
                position_count, relation_count, last_updated)
               VALUES (?, ?, 'active', ?, ?, ?, ?, datetime('now'))""",
            (self.province, str(self.db_path), p, o, ps, r),
        )
        reg.commit()
        reg.close()