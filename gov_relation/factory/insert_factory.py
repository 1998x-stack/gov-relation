"""Parameterized v3 entity inserts with deterministic identifiers."""

from __future__ import annotations

import json
import sqlite3
from typing import Any

from gov_relation.identity import (
    date_precision,
    normalize_text,
    organization_key,
    person_key,
    stable_id,
)


class InsertFactory:
    """Write v3 records without unsafe name-only person merging."""

    def upsert_person(
        self,
        conn: sqlite3.Connection,
        data: dict[str, Any],
        *,
        dataset_key: str = "factory",
        source_pk: str | None = None,
    ) -> str:
        name = str(data.get("canonical_name", "")).strip()
        birth = data.get("birth_text", "")
        precision = date_precision(birth)
        source_key = source_pk or data.get("_source_pk")
        if not source_key and precision == "unknown":
            raise ValueError(
                "source_pk is required for a person without a precise birth value"
            )
        key, status = person_key(
            name=name,
            birth=birth,
            dataset_key=dataset_key,
            source_pk=str(source_key or ""),
        )
        person_id = stable_id("per", key)
        params = {
            "person_id": person_id,
            "canonical_name": name,
            "normalized_name": normalize_text(name),
            "gender": str(data.get("gender", "")),
            "ethnicity": str(data.get("ethnicity", "")),
            "birth_text": str(birth),
            "birth_precision": precision,
            "birthplace": str(data.get("birthplace", "")),
            "native_place": str(data.get("native_place", "")),
            "education": str(data.get("education", "")),
            "party_join_text": str(data.get("party_join_text", "")),
            "work_start_text": str(data.get("work_start_text", "")),
            "identity_status": status,
        }
        conn.execute(
            """INSERT INTO persons (
                   person_id, canonical_name, normalized_name, gender, ethnicity,
                   birth_text, birth_precision, birthplace, native_place,
                   education, party_join_text, work_start_text, identity_status
               ) VALUES (
                   :person_id, :canonical_name, :normalized_name, :gender, :ethnicity,
                   :birth_text, :birth_precision, :birthplace, :native_place,
                   :education, :party_join_text, :work_start_text, :identity_status
               ) ON CONFLICT(person_id) DO UPDATE SET
                   canonical_name=excluded.canonical_name,
                   normalized_name=excluded.normalized_name,
                   gender=CASE WHEN excluded.gender='' THEN persons.gender ELSE excluded.gender END,
                   ethnicity=CASE WHEN excluded.ethnicity='' THEN persons.ethnicity ELSE excluded.ethnicity END,
                   birth_text=CASE WHEN excluded.birth_text='' THEN persons.birth_text ELSE excluded.birth_text END,
                   birth_precision=CASE WHEN excluded.birth_text='' THEN persons.birth_precision ELSE excluded.birth_precision END,
                   birthplace=CASE WHEN excluded.birthplace='' THEN persons.birthplace ELSE excluded.birthplace END,
                   native_place=CASE WHEN excluded.native_place='' THEN persons.native_place ELSE excluded.native_place END,
                   education=CASE WHEN excluded.education='' THEN persons.education ELSE excluded.education END,
                   party_join_text=CASE WHEN excluded.party_join_text='' THEN persons.party_join_text ELSE excluded.party_join_text END,
                   work_start_text=CASE WHEN excluded.work_start_text='' THEN persons.work_start_text ELSE excluded.work_start_text END,
                   identity_status=excluded.identity_status,
                   updated_at=datetime('now')""",
            params,
        )
        return person_id

    def upsert_jurisdiction(
        self, conn: sqlite3.Connection, data: dict[str, Any]
    ) -> str:
        name = str(data.get("name", "")).strip()
        parent_id = data.get("parent_id") or None
        level = str(data.get("level", "unknown"))
        jurisdiction_id = stable_id(
            "jur", f"{parent_id or 'root'}|{level}|{normalize_text(name)}"
        )
        conn.execute(
            """INSERT OR IGNORE INTO jurisdictions (
                   jurisdiction_id, parent_id, name, normalized_name, level,
                   province_name, prefecture_name, county_name
               ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                jurisdiction_id, parent_id, name, normalize_text(name), level,
                str(data.get("province_name", "")),
                str(data.get("prefecture_name", "")),
                str(data.get("county_name", "")),
            ),
        )
        return jurisdiction_id

    def upsert_organization(
        self,
        conn: sqlite3.Connection,
        data: dict[str, Any],
        *,
        dataset_key: str = "factory",
    ) -> str:
        name = str(data.get("canonical_name", "")).strip()
        jurisdiction_id = str(data.get("jurisdiction_id", "") or "")
        key = organization_key(
            name=name,
            jurisdiction_key=jurisdiction_id,
            dataset_key=dataset_key,
        )
        organization_id = stable_id("org", key)
        conn.execute(
            """INSERT OR IGNORE INTO organizations (
                   organization_id, jurisdiction_id, canonical_name,
                   normalized_name, organization_type, administrative_level,
                   location_text
               ) VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                organization_id, jurisdiction_id or None, name,
                normalize_text(name), str(data.get("organization_type", "")),
                str(data.get("administrative_level", "")),
                str(data.get("location_text", "")),
            ),
        )
        return organization_id

    def insert_position(
        self, conn: sqlite3.Connection, data: dict[str, Any]
    ) -> str:
        source_pk = data.get("_source_pk")
        if source_pk:
            key = f"{data.get('_dataset_key', 'factory')}|{source_pk}"
        else:
            key = "|".join(
                (
                    str(data.get("_dataset_key", "factory")),
                    str(data.get("person_id", "")),
                    str(data.get("organization_id", "")),
                    normalize_text(data.get("organization_text", "")),
                    normalize_text(data.get("title", "")),
                    normalize_text(data.get("start_text", "")),
                    normalize_text(data.get("end_text", "")),
                    str(int(data.get("is_current", 0))),
                )
            )
        position_id = stable_id("pos", key)
        start = str(data.get("start_text", ""))
        conn.execute(
            """INSERT OR IGNORE INTO positions (
                   position_id, person_id, organization_id, organization_text,
                   title, title_category, rank, start_text, end_text,
                   start_date, end_date, date_precision, is_current,
                   sort_order, confidence, notes
               ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                position_id, str(data.get("person_id", "")),
                data.get("organization_id") or None,
                str(data.get("organization_text", "")),
                str(data.get("title", "")),
                str(data.get("title_category", "")), str(data.get("rank", "")),
                start, str(data.get("end_text", "")),
                data.get("start_date") or None, data.get("end_date") or None,
                date_precision(start), int(data.get("is_current", 0)),
                int(data.get("sort_order", 0)),
                str(data.get("confidence", "unverified")),
                str(data.get("notes", "")),
            ),
        )
        return position_id

    def insert_relationship(
        self, conn: sqlite3.Connection, data: dict[str, Any]
    ) -> str:
        source_pk = data.get("_source_pk")
        if source_pk:
            key = f"{data.get('_dataset_key', 'factory')}|{source_pk}"
        else:
            key = "|".join(
                (
                    str(data.get("_dataset_key", "factory")),
                    str(data.get("person_from_id", "")),
                    str(data.get("person_to_id", "")),
                    str(data.get("relationship_type", "other")),
                    str(data.get("overlap_organization_id", "")),
                    normalize_text(data.get("overlap_organization_text", "")),
                    normalize_text(data.get("overlap_period_text", "")),
                    normalize_text(data.get("context", "")),
                )
            )
        relationship_id = stable_id("rel", key)
        conn.execute(
            """INSERT INTO relationships (
                   relationship_id, person_from_id, person_to_id,
                   relationship_type, direction, strength, confidence,
                   context, evidence_summary, overlap_organization_id,
                   overlap_organization_text, overlap_period_text
               ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(relationship_id) DO NOTHING""",
            (
                relationship_id, str(data.get("person_from_id", "")),
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
        return relationship_id

    def insert_source(self, conn: sqlite3.Connection, data: dict[str, Any]) -> str:
        url = str(data.get("canonical_url", "")).strip()
        title = str(data.get("title", "")).strip()
        source_id = stable_id(
            "src", url or title or str(data.get("publisher", "unknown"))
        )
        conn.execute(
            """INSERT OR IGNORE INTO sources (
                   source_id, canonical_url, title, publisher, published_at,
                   accessed_at, source_type, reliability
               ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                source_id, url, title, str(data.get("publisher", "")),
                data.get("published_at") or None, data.get("accessed_at") or None,
                str(data.get("source_type", "other")),
                str(data.get("reliability", "low")),
            ),
        )
        return source_id

    def insert_claim(self, conn: sqlite3.Connection, data: dict[str, Any]) -> str:
        value = data.get("value", data.get("value_json", ""))
        value_json = (
            value
            if isinstance(value, str)
            else json.dumps(value, ensure_ascii=False, sort_keys=True)
        )
        key = "|".join(
            (
                str(data.get("subject_type", "")),
                str(data.get("subject_id", "")),
                str(data.get("predicate", "")),
                value_json,
            )
        )
        claim_id = stable_id("clm", key)
        conn.execute(
            """INSERT OR IGNORE INTO claims (
                   claim_id, subject_type, subject_id, predicate, value_json,
                   valid_from, valid_to, observed_at, confidence, review_status
               ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                claim_id, str(data.get("subject_type", "")),
                str(data.get("subject_id", "")),
                str(data.get("predicate", "")), value_json,
                data.get("valid_from") or None, data.get("valid_to") or None,
                data.get("observed_at") or None,
                str(data.get("confidence", "unverified")),
                str(data.get("review_status", "pending")),
            ),
        )
        return claim_id

    def link_evidence(
        self,
        conn: sqlite3.Connection,
        source_id: str,
        subject_type: str,
        subject_id: str,
        field_name: str,
        locator: str = "",
    ) -> str:
        key = f"{source_id}|{subject_type}|{subject_id}|{field_name}|{locator}"
        evidence_id = stable_id("ev", key)
        conn.execute(
            """INSERT OR IGNORE INTO evidence_links (
                   evidence_id, source_id, subject_type, subject_id,
                   field_name, locator
               ) VALUES (?, ?, ?, ?, ?, ?)""",
            (
                evidence_id, source_id, subject_type, subject_id,
                field_name, locator,
            ),
        )
        return evidence_id
