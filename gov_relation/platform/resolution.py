"""Conservative entity-resolution candidate generation without automatic merges."""

from __future__ import annotations

import json
import sqlite3
from collections import defaultdict
from itertools import combinations

from .identity import normalize_text, stable_id


def build_person_candidates(
    conn: sqlite3.Connection,
    *,
    minimum_score: float = 0.65,
    maximum_name_group: int = 40,
) -> int:
    """Create review candidates using corroborating attributes beyond a shared name."""
    persons = {
        row["person_id"]: dict(row)
        for row in conn.execute(
            """SELECT person_id, normalized_name, birth_text, birthplace, native_place,
                      identity_status FROM persons WHERE normalized_name <> ''"""
        )
    }
    name_groups: dict[str, list[str]] = defaultdict(list)
    for person_id, person in persons.items():
        name_groups[person["normalized_name"]].append(person_id)

    orgs: dict[str, set[str]] = defaultdict(set)
    for row in conn.execute(
        """SELECT p.person_id, COALESCE(o.normalized_name, p.organization_text) AS org_name
           FROM positions p LEFT JOIN organizations o ON o.organization_id=p.organization_id"""
    ):
        value = normalize_text(row["org_name"])
        if value:
            orgs[row["person_id"]].add(value)
    for row in conn.execute(
        "SELECT person_id, organization_text FROM person_statuses"
    ):
        value = normalize_text(row["organization_text"])
        if value:
            orgs[row["person_id"]].add(value)
    for row in conn.execute(
        """SELECT person_from_id, person_to_id,
                  COALESCE(o.normalized_name, r.overlap_organization_text) AS org_name
           FROM relationships r
           LEFT JOIN organizations o ON o.organization_id=r.overlap_organization_id"""
    ):
        value = normalize_text(row["org_name"])
        if value:
            orgs[row["person_from_id"]].add(value)
            orgs[row["person_to_id"]].add(value)

    inserted = 0
    for group in name_groups.values():
        if len(group) < 2 or len(group) > maximum_name_group:
            continue
        for left_id, right_id in combinations(sorted(group), 2):
            left = persons[left_id]
            right = persons[right_id]
            left_birth = normalize_text(left["birth_text"])
            right_birth = normalize_text(right["birth_text"])
            if left_birth and right_birth and left_birth != right_birth:
                continue

            score = 0.45
            reasons = ["normalized_name_exact"]
            left_places = {
                normalize_text(left["birthplace"]), normalize_text(left["native_place"])
            } - {""}
            right_places = {
                normalize_text(right["birthplace"]), normalize_text(right["native_place"])
            } - {""}
            shared_places = sorted(left_places & right_places)
            if shared_places:
                score += 0.25
                reasons.append(f"shared_place:{shared_places[0]}")
            shared_orgs = sorted(orgs[left_id] & orgs[right_id])
            if shared_orgs:
                score += 0.25
                reasons.append(f"shared_organization:{shared_orgs[0]}")
            if {left["identity_status"], right["identity_status"]} & {"verified", "probable"}:
                score += 0.05
                reasons.append("one_identity_resolved")
            if score < minimum_score:
                continue
            candidate_id = stable_id("candidate", f"person|{left_id}|{right_id}")
            cursor = conn.execute(
                """INSERT OR IGNORE INTO resolution_candidates
                   (candidate_id, left_entity_id, right_entity_id, entity_type,
                    score, reasons_json)
                   VALUES (?, ?, ?, 'person', ?, ?)""",
                (
                    candidate_id, left_id, right_id, min(score, 0.99),
                    json.dumps(reasons, ensure_ascii=False),
                ),
            )
            inserted += int(cursor.rowcount > 0)
    return inserted
