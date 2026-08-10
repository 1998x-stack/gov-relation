"""Lossless importers from legacy region databases and person profile JSON."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from .identity import (
    date_precision,
    normalize_text,
    organization_key,
    person_key,
    sha256_bytes,
    stable_id,
)

CORE_TABLES = ("persons", "organizations", "positions", "relationships")


@dataclass
class ImportStats:
    datasets: int = 0
    jurisdictions: int = 0
    raw_records: int = 0
    persons: int = 0
    organizations: int = 0
    positions: int = 0
    relationships: int = 0
    profiles: int = 0
    sources: int = 0
    claims: int = 0
    issues: int = 0
    skipped: int = 0
    errors: list[str] = field(default_factory=list)

    def add(self, other: "ImportStats") -> None:
        for name in (
            "datasets", "jurisdictions", "raw_records", "persons", "organizations", "positions",
            "relationships", "profiles", "sources", "claims", "issues", "skipped",
        ):
            setattr(self, name, getattr(self, name) + getattr(other, name))
        self.errors.extend(other.errors)

    def as_dict(self) -> dict[str, Any]:
        return {
            name: getattr(self, name)
            for name in (
                "datasets", "jurisdictions", "raw_records", "persons", "organizations", "positions",
                "relationships", "profiles", "sources", "claims", "issues", "skipped",
                "errors",
            )
        }


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _row_dicts(conn: sqlite3.Connection, table: str) -> Iterable[dict[str, Any]]:
    cursor = conn.execute(f"SELECT * FROM [{table}]")
    columns = [item[0] for item in cursor.description or ()]
    for row in cursor:
        yield {name: row[index] for index, name in enumerate(columns)}


def _first(row: dict[str, Any], *names: str, default: Any = "") -> Any:
    for name in names:
        if name in row and row[name] is not None:
            return row[name]
    return default


def _normalize_confidence(value: object) -> str:
    text = normalize_text(value).lower()
    mapping = {
        "confirmed": "confirmed", "high": "confirmed", "高": "confirmed", "已确认": "confirmed",
        "plausible": "plausible", "medium": "plausible", "中": "plausible", "较高": "plausible",
        "unverified": "unverified", "low": "unverified", "低": "unverified", "": "unverified",
    }
    return mapping.get(text, "unverified")


def _normalize_strength(value: object) -> str:
    text = normalize_text(value).lower()
    mapping = {
        "strong": "strong", "high": "strong", "强": "strong",
        "medium": "medium", "中": "medium",
        "weak": "weak", "low": "weak", "弱": "weak", "": "unknown",
    }
    return mapping.get(text, "unknown")


def _normalize_direction(value: object) -> str:
    text = normalize_text(value).lower()
    if text in {"from_to", "person_to_other", "directed", "a_to_b"}:
        return "from_to"
    if text in {"to_from", "other_to_person", "b_to_a"}:
        return "to_from"
    return "undirected"


def _register_dataset(
    target: sqlite3.Connection,
    *,
    dataset_key: str,
    name: str,
    kind: str,
    source_path: str,
    digest: str,
) -> tuple[str, bool]:
    dataset_id = stable_id("dset", dataset_key)
    existing = target.execute(
        "SELECT content_sha256 FROM datasets WHERE dataset_key=?", (dataset_key,)
    ).fetchone()
    if existing:
        if existing[0] != digest:
            raise ValueError(f"dataset changed; rebuild or version it: {source_path}")
        return dataset_id, False
    target.execute(
        """INSERT INTO datasets
           (dataset_id, dataset_key, name, kind, source_path, content_sha256)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (dataset_id, dataset_key, name, kind, source_path, digest),
    )
    return dataset_id, True


def _jurisdiction(
    target: sqlite3.Connection,
    *,
    name: str,
    level: str,
    parent_id: str | None = None,
    province_name: str = "",
    prefecture_name: str = "",
    county_name: str = "",
) -> tuple[str | None, bool]:
    name = name.strip()
    if not name:
        return None, False
    key = f"{parent_id or 'root'}|{level}|{normalize_text(name)}"
    jurisdiction_id = stable_id("jur", key)
    cursor = target.execute(
        """INSERT OR IGNORE INTO jurisdictions
           (jurisdiction_id, parent_id, name, normalized_name, level,
            province_name, prefecture_name, county_name)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            jurisdiction_id, parent_id, name, normalize_text(name), level,
            province_name, prefecture_name, county_name,
        ),
    )
    return jurisdiction_id, cursor.rowcount > 0


def _raw_record(
    target: sqlite3.Connection,
    dataset_id: str,
    table: str,
    source_pk: object,
    payload: Any,
) -> tuple[str, bool]:
    payload_json = _json(payload)
    key = f"{dataset_id}|{table}|{source_pk}"
    raw_id = stable_id("raw", key)
    cursor = target.execute(
        """INSERT OR IGNORE INTO raw_records
           (raw_record_id, dataset_id, source_table, source_pk, payload_json, payload_sha256)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (raw_id, dataset_id, table, str(source_pk), payload_json, sha256_bytes(payload_json.encode())),
    )
    return raw_id, cursor.rowcount > 0


def _provenance(
    target: sqlite3.Connection,
    dataset_id: str,
    raw_id: str,
    entity_type: str,
    entity_id: str,
    transformation: str,
) -> None:
    target.execute(
        """INSERT OR IGNORE INTO entity_provenance
           (provenance_id, dataset_id, raw_record_id, entity_type, entity_id, transformation)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (
            stable_id("prov", f"{raw_id}|{entity_type}|{entity_id}"),
            dataset_id, raw_id, entity_type, entity_id, transformation,
        ),
    )


def _issue(
    target: sqlite3.Connection,
    stats: ImportStats,
    *,
    dataset_id: str | None,
    raw_id: str | None,
    severity: str,
    code: str,
    message: str,
    entity_type: str = "",
    entity_id: str = "",
) -> None:
    key = f"{dataset_id}|{raw_id}|{code}|{entity_type}|{entity_id}|{message}"
    cursor = target.execute(
        """INSERT OR IGNORE INTO quality_issues
           (issue_id, dataset_id, raw_record_id, severity, issue_code,
            entity_type, entity_id, message)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (stable_id("issue", key), dataset_id, raw_id, severity, code, entity_type, entity_id, message),
    )
    stats.issues += int(cursor.rowcount > 0)


def import_legacy_database(
    target: sqlite3.Connection,
    path: str | Path,
    *,
    source_root: str | Path | None = None,
) -> ImportStats:
    """Losslessly import one legacy SQLite database into canonical tables."""
    stats = ImportStats()
    db_path = Path(path).resolve()
    relative = db_path.relative_to(Path(source_root).resolve()) if source_root else db_path
    source_path = relative.as_posix()
    dataset_key = f"legacy-sqlite:{source_path}"
    digest = sha256_bytes(db_path.read_bytes())
    dataset_id, created = _register_dataset(
        target,
        dataset_key=dataset_key,
        name=db_path.stem,
        kind="legacy_sqlite",
        source_path=source_path,
        digest=digest,
    )
    if not created:
        stats.skipped = 1
        return stats
    stats.datasets = 1

    region_name = db_path.stem.removesuffix("_network")
    jurisdiction_id, jurisdiction_created = _jurisdiction(
        target, name=region_name, level="unknown", county_name=region_name
    )
    stats.jurisdictions += int(jurisdiction_created)
    target.execute(
        "UPDATE datasets SET jurisdiction_id=? WHERE dataset_id=?",
        (jurisdiction_id, dataset_id),
    )

    source = sqlite3.connect(f"file:{db_path.resolve()}?mode=ro", uri=True)
    source.row_factory = sqlite3.Row
    try:
        tables = {
            row[0]
            for row in source.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )
        }
        if "persons" not in tables:
            _issue(
                target, stats, dataset_id=dataset_id, raw_id=None, severity="error",
                code="missing_persons_table", message="Legacy database has no persons table",
            )
            return stats

        person_map: dict[str, str] = {}
        org_map: dict[str, str] = {}

        for index, row in enumerate(_row_dicts(source, "persons"), start=1):
            source_pk = _first(row, "id", "pid", default=index)
            raw_id, inserted = _raw_record(target, dataset_id, "persons", source_pk, row)
            stats.raw_records += int(inserted)
            name = str(_first(row, "name")).strip()
            if not name:
                _issue(
                    target, stats, dataset_id=dataset_id, raw_id=raw_id, severity="error",
                    code="person_missing_name", message="Person row cannot be normalized without a name",
                )
                continue
            birth = _first(row, "birth")
            key, identity_status = person_key(
                name=name, birth=birth, dataset_key=dataset_key, source_pk=source_pk
            )
            person_id = stable_id("per", key)
            cursor = target.execute(
                """INSERT OR IGNORE INTO persons
                   (person_id, canonical_name, normalized_name, gender, ethnicity,
                    birth_text, birth_precision, birthplace, native_place, party_join_text,
                    work_start_text, identity_status)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    person_id, name, normalize_text(name), str(_first(row, "gender")),
                    str(_first(row, "ethnicity")), str(birth or ""), date_precision(birth),
                    str(_first(row, "birthplace")), str(_first(row, "native_place")),
                    str(_first(row, "party_join")), str(_first(row, "work_start", "work_year")),
                    identity_status,
                ),
            )
            stats.persons += int(cursor.rowcount > 0)
            person_map[str(source_pk)] = person_id
            _provenance(target, dataset_id, raw_id, "person", person_id, "legacy_person_v1")

            source_text = str(_first(row, "source")).strip()
            if source_text:
                is_url = source_text.startswith(("http://", "https://"))
                source_id = stable_id("src", source_text)
                source_cursor = target.execute(
                    """INSERT OR IGNORE INTO sources
                       (source_id, canonical_url, title, source_type, reliability)
                       VALUES (?, ?, ?, 'other', 'low')""",
                    (source_id, source_text if is_url else "", "" if is_url else source_text),
                )
                stats.sources += int(source_cursor.rowcount > 0)
                target.execute(
                    """INSERT OR IGNORE INTO evidence_links
                       (evidence_id, source_id, subject_type, subject_id, field_name, confidence)
                       VALUES (?, ?, 'person', ?, 'legacy_source', 'unverified')""",
                    (stable_id("ev", f"{source_id}|person|{person_id}|legacy_source"), source_id, person_id),
                )

            current_post = str(_first(row, "current_post"))
            current_org = str(_first(row, "current_org"))
            if current_post or current_org:
                status_id = stable_id("status", f"{raw_id}|current")
                target.execute(
                    """INSERT OR IGNORE INTO person_statuses
                       (status_id, person_id, post_text, organization_text, confidence)
                       VALUES (?, ?, ?, ?, 'unverified')""",
                    (status_id, person_id, current_post, current_org),
                )

        if "organizations" in tables:
            for index, row in enumerate(_row_dicts(source, "organizations"), start=1):
                source_pk = _first(row, "id", default=index)
                raw_id, inserted = _raw_record(target, dataset_id, "organizations", source_pk, row)
                stats.raw_records += int(inserted)
                name = str(_first(row, "name", "fqn")).strip()
                if not name:
                    _issue(
                        target, stats, dataset_id=dataset_id, raw_id=raw_id, severity="warning",
                        code="organization_missing_name", message="Organization row has no name",
                    )
                    continue
                org_id = stable_id(
                    "org", organization_key(name=name, jurisdiction_key=db_path.stem, dataset_key=dataset_key)
                )
                cursor = target.execute(
                    """INSERT OR IGNORE INTO organizations
                       (organization_id, jurisdiction_id, canonical_name, normalized_name, organization_type,
                        administrative_level, location_text)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (
                        org_id, jurisdiction_id, name, normalize_text(name), str(_first(row, "type", "org_type")),
                        str(_first(row, "level")), str(_first(row, "location")),
                    ),
                )
                stats.organizations += int(cursor.rowcount > 0)
                org_map[str(source_pk)] = org_id
                _provenance(target, dataset_id, raw_id, "organization", org_id, "legacy_organization_v1")

        if "positions" in tables:
            for index, row in enumerate(_row_dicts(source, "positions"), start=1):
                source_pk = _first(row, "id", default=index)
                raw_id, inserted = _raw_record(target, dataset_id, "positions", source_pk, row)
                stats.raw_records += int(inserted)
                legacy_person = str(_first(row, "person_id"))
                person_id = person_map.get(legacy_person)
                if not person_id:
                    _issue(
                        target, stats, dataset_id=dataset_id, raw_id=raw_id, severity="error",
                        code="position_missing_person", message=f"Unknown person foreign key: {legacy_person}",
                    )
                    continue
                legacy_org = str(_first(row, "org_id"))
                org_id = org_map.get(legacy_org)
                org_text = str(_first(row, "org_name"))
                if legacy_org and not org_id:
                    _issue(
                        target, stats, dataset_id=dataset_id, raw_id=raw_id, severity="warning",
                        code="position_missing_organization", message=f"Unknown organization foreign key: {legacy_org}",
                    )
                start = str(_first(row, "start_date", "start"))
                end = str(_first(row, "end_date", "end"))
                position_id = stable_id("pos", f"{dataset_key}|{source_pk}")
                cursor = target.execute(
                    """INSERT OR IGNORE INTO positions
                       (position_id, person_id, organization_id, organization_text, title, rank,
                        start_text, end_text, date_precision, is_current, confidence, notes)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        position_id, person_id, org_id, org_text, str(_first(row, "title")),
                        str(_first(row, "rank")), start, end, date_precision(start),
                        int(normalize_text(end).lower() in {"present", "至今", "现任"}),
                        _normalize_confidence(_first(row, "confidence")), str(_first(row, "note", "notes")),
                    ),
                )
                stats.positions += int(cursor.rowcount > 0)
                _provenance(target, dataset_id, raw_id, "position", position_id, "legacy_position_v1")

        if "relationships" in tables:
            for index, row in enumerate(_row_dicts(source, "relationships"), start=1):
                source_pk = _first(row, "id", default=index)
                raw_id, inserted = _raw_record(target, dataset_id, "relationships", source_pk, row)
                stats.raw_records += int(inserted)
                left_key = str(_first(row, "person_a", "person_a_id", "person1_id", "persona_a"))
                right_key = str(_first(row, "person_b", "person_b_id", "person2_id", "persona_b"))
                left = person_map.get(left_key)
                right = person_map.get(right_key)
                if not left or not right or left == right:
                    _issue(
                        target, stats, dataset_id=dataset_id, raw_id=raw_id, severity="error",
                        code="relationship_invalid_endpoints",
                        message=f"Invalid relationship endpoints: {left_key}, {right_key}",
                    )
                    continue
                legacy_org = str(_first(row, "overlap_org", "org"))
                relationship_id = stable_id("rel", f"{dataset_key}|{source_pk}")
                cursor = target.execute(
                    """INSERT OR IGNORE INTO relationships
                       (relationship_id, person_from_id, person_to_id, relationship_type,
                        direction, strength, confidence, context, evidence_summary,
                        overlap_organization_id, overlap_organization_text, overlap_period_text)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        relationship_id, left, right, str(_first(row, "type", default="other")),
                        _normalize_direction(_first(row, "direction")),
                        _normalize_strength(_first(row, "strength", "strongth")),
                        _normalize_confidence(_first(row, "confidence")),
                        str(_first(row, "context", "description")), str(_first(row, "evidence")),
                        org_map.get(legacy_org), "" if legacy_org in org_map else legacy_org,
                        str(_first(row, "overlap_period", "period")),
                    ),
                )
                stats.relationships += int(cursor.rowcount > 0)
                _provenance(target, dataset_id, raw_id, "relationship", relationship_id, "legacy_relationship_v1")
    finally:
        source.close()
    return stats


def import_person_profile(
    target: sqlite3.Connection,
    path: str | Path,
    *,
    source_root: str | Path | None = None,
) -> ImportStats:
    """Import one person profile JSON, preserving the entire source document."""
    stats = ImportStats()
    profile_path = Path(path).resolve()
    relative = profile_path.relative_to(Path(source_root).resolve()) if source_root else profile_path
    source_path = relative.as_posix()
    raw_bytes = profile_path.read_bytes()
    digest = sha256_bytes(raw_bytes)
    try:
        profile = json.loads(raw_bytes)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        stats.errors.append(f"{source_path}: {exc}")
        stats.issues = 1
        return stats
    if not isinstance(profile, dict):
        stats.errors.append(f"{source_path}: profile root must be an object")
        stats.issues = 1
        return stats

    dataset_key = f"person-profile:{source_path}"
    dataset_id, created = _register_dataset(
        target,
        dataset_key=dataset_key,
        name=profile_path.stem,
        kind="person_profile",
        source_path=source_path,
        digest=digest,
    )
    if not created:
        stats.skipped = 1
        return stats
    stats.datasets = 1
    raw_id, inserted = _raw_record(target, dataset_id, "person_profiles", source_path, profile)
    stats.raw_records += int(inserted)

    scope = profile.get("investigation_scope") if isinstance(profile.get("investigation_scope"), dict) else {}
    province = str(scope.get("province") or "").strip()
    city = str(scope.get("city") or "").strip()
    region = str(scope.get("region") or "").strip()
    jurisdiction_id = None
    if province:
        jurisdiction_id, created = _jurisdiction(
            target, name=province, level="province", province_name=province
        )
        stats.jurisdictions += int(created)
    if city and normalize_text(city) != normalize_text(province):
        jurisdiction_id, created = _jurisdiction(
            target, name=city, level="prefecture", parent_id=jurisdiction_id,
            province_name=province, prefecture_name=city,
        )
        stats.jurisdictions += int(created)
    if region and normalize_text(region) not in {normalize_text(province), normalize_text(city)}:
        jurisdiction_id, created = _jurisdiction(
            target, name=region, level="county", parent_id=jurisdiction_id,
            province_name=province, prefecture_name=city, county_name=region,
        )
        stats.jurisdictions += int(created)
    target.execute(
        "UPDATE datasets SET jurisdiction_id=? WHERE dataset_id=?",
        (jurisdiction_id, dataset_id),
    )

    identity = profile.get("identity") if isinstance(profile.get("identity"), dict) else {}
    name = str(identity.get("name") or "").strip()
    if not name:
        _issue(
            target, stats, dataset_id=dataset_id, raw_id=raw_id, severity="error",
            code="profile_missing_name", message="Profile identity.name is missing",
        )
        return stats
    birth = identity.get("birth", "")
    source_pk = identity.get("person_id") or source_path
    key, identity_status = person_key(
        name=name, birth=birth, dataset_key=dataset_key, source_pk=source_pk
    )
    person_id = stable_id("per", key)
    cursor = target.execute(
        """INSERT OR IGNORE INTO persons
           (person_id, canonical_name, normalized_name, gender, ethnicity, birth_text,
            birth_precision, birthplace, native_place, party_join_text, work_start_text,
            identity_status)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            person_id, name, normalize_text(name), str(identity.get("gender") or ""),
            str(identity.get("ethnicity") or ""), str(birth or ""), date_precision(birth),
            str(identity.get("birthplace") or ""), str(identity.get("native_place") or ""),
            str(identity.get("party_join") or ""), str(identity.get("work_start") or ""),
            identity_status,
        ),
    )
    stats.persons += int(cursor.rowcount > 0)
    _provenance(target, dataset_id, raw_id, "person", person_id, "person_profile_v1")

    for alias in identity.get("aliases") or []:
        if alias:
            target.execute(
                """INSERT OR IGNORE INTO person_aliases
                   (person_id, alias, normalized_alias) VALUES (?, ?, ?)""",
                (person_id, str(alias), normalize_text(alias)),
            )

    profile_id = stable_id("profile", source_path)
    target.execute(
        """INSERT OR IGNORE INTO profile_documents
           (profile_id, person_id, raw_record_id, schema_version, generated_at, profile_json)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (
            profile_id, person_id, raw_id, str(profile.get("schema_version") or ""),
            str(profile.get("generated_at") or profile.get("investigation_date") or ""), _json(profile),
        ),
    )
    stats.profiles = 1

    current = profile.get("current_status")
    if isinstance(current, dict):
        status_id = stable_id("status", f"{profile_id}|current")
        target.execute(
            """INSERT OR IGNORE INTO person_statuses
               (status_id, person_id, post_text, organization_text, administrative_rank,
                observed_at, is_current_confirmed, confidence)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                status_id, person_id, str(current.get("current_post") or ""),
                str(current.get("current_org") or ""), str(current.get("administrative_rank") or ""),
                str(current.get("as_of") or "") or None, int(bool(current.get("is_current_confirmed"))),
                "confirmed" if current.get("is_current_confirmed") else "unverified",
            ),
        )

    org_scope = jurisdiction_id or "|".join(
        str(scope.get(k) or "") for k in ("province", "city", "region")
    )
    source_map: dict[str, str] = {}
    source_register = profile.get("source_register") or profile.get("sources") or []
    if isinstance(source_register, list):
        for index, source in enumerate(source_register, start=1):
            if not isinstance(source, dict):
                continue
            local_id = str(source.get("id") or f"S{index:03d}")
            url = str(source.get("url") or "").strip()
            source_id = stable_id("src", url or f"{source_path}|{local_id}")
            cursor = target.execute(
                """INSERT OR IGNORE INTO sources
                   (source_id, canonical_url, title, publisher, published_at, accessed_at,
                    source_type, reliability)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    source_id, url, str(source.get("title") or source.get("description") or ""),
                    str(source.get("publisher") or ""),
                    str(source.get("published_at") or "") or None,
                    str(source.get("accessed_at") or source.get("access_date") or "") or None,
                    _source_type(source.get("source_type") or source.get("type")),
                    _reliability(source.get("reliability") or source.get("confidence")),
                ),
            )
            stats.sources += int(cursor.rowcount > 0)
            source_map[local_id] = source_id

    timeline = profile.get("career_timeline") or []
    if isinstance(timeline, list):
        for index, item in enumerate(timeline):
            if not isinstance(item, dict) or item.get("org") == "履历缺口":
                continue
            org_name = str(item.get("org") or item.get("organization") or "").strip()
            org_id = None
            if org_name:
                org_id = stable_id(
                    "org", organization_key(name=org_name, jurisdiction_key=org_scope, dataset_key=dataset_key)
                )
                cursor = target.execute(
                    """INSERT OR IGNORE INTO organizations
                       (organization_id, jurisdiction_id, canonical_name, normalized_name, administrative_level,
                        location_text)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (
                        org_id, jurisdiction_id, org_name, normalize_text(org_name), str(item.get("level") or ""),
                        str(item.get("location") or ""),
                    ),
                )
                stats.organizations += int(cursor.rowcount > 0)
            start = str(item.get("start") or item.get("period") or "")
            end = str(item.get("end") or "")
            position_id = stable_id("pos", f"{profile_id}|career|{index}")
            cursor = target.execute(
                """INSERT OR IGNORE INTO positions
                   (position_id, person_id, organization_id, organization_text, title, rank,
                    category, start_text, end_text, date_precision, is_current, confidence, notes)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    position_id, person_id, org_id, org_name, str(item.get("title") or ""),
                    str(item.get("rank") or ""), str(item.get("system") or ""), start, end,
                    date_precision(start), int(normalize_text(end).lower() in {"present", "至今", "现任"}),
                    _normalize_confidence(item.get("confidence")), str(item.get("notes") or ""),
                ),
            )
            stats.positions += int(cursor.rowcount > 0)
            for local_source_id in item.get("source_ids") or []:
                source_id = source_map.get(str(local_source_id))
                if source_id:
                    target.execute(
                        """INSERT OR IGNORE INTO evidence_links
                           (evidence_id, source_id, subject_type, subject_id, field_name, confidence)
                           VALUES (?, ?, 'position', ?, 'career_timeline', ?)""",
                        (
                            stable_id("ev", f"{source_id}|position|{position_id}|career_timeline"),
                            source_id, position_id, _normalize_confidence(item.get("confidence")),
                        ),
                    )

    relationships = profile.get("relationships") or profile.get("relationship_network") or []
    if isinstance(relationships, list):
        for index, item in enumerate(relationships):
            if not isinstance(item, dict):
                continue
            other_name = str(item.get("person") or item.get("name") or "").strip()
            other_local_id = str(item.get("person_id") or other_name).strip()
            if not other_name or normalize_text(other_name) == normalize_text(name):
                _issue(
                    target, stats, dataset_id=dataset_id, raw_id=raw_id, severity="warning",
                    code="profile_relationship_invalid_target",
                    message=f"Invalid related person at index {index}: {other_name!r}",
                    entity_type="person", entity_id=person_id,
                )
                continue
            other_key = f"scoped:{dataset_key}|relationship|{other_local_id}|{normalize_text(other_name)}"
            other_id = stable_id("per", other_key)
            cursor = target.execute(
                """INSERT OR IGNORE INTO persons
                   (person_id, canonical_name, normalized_name, identity_status)
                   VALUES (?, ?, ?, 'unresolved')""",
                (other_id, other_name, normalize_text(other_name)),
            )
            stats.persons += int(cursor.rowcount > 0)

            overlap_org = str(item.get("overlap_org") or "").strip()
            overlap_org_id = None
            if overlap_org:
                overlap_org_id = stable_id(
                    "org", organization_key(
                        name=overlap_org, jurisdiction_key=org_scope, dataset_key=dataset_key
                    )
                )
                cursor = target.execute(
                    """INSERT OR IGNORE INTO organizations
                       (organization_id, jurisdiction_id, canonical_name, normalized_name)
                       VALUES (?, ?, ?, ?)""",
                    (overlap_org_id, jurisdiction_id, overlap_org, normalize_text(overlap_org)),
                )
                stats.organizations += int(cursor.rowcount > 0)

            relationship_id = stable_id("rel", f"{profile_id}|relationship|{index}")
            cursor = target.execute(
                """INSERT OR IGNORE INTO relationships
                   (relationship_id, person_from_id, person_to_id, relationship_type,
                    direction, strength, confidence, context, evidence_summary,
                    overlap_organization_id, overlap_organization_text, overlap_period_text)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    relationship_id, person_id, other_id,
                    str(item.get("relationship_type") or item.get("type") or "other"),
                    _normalize_direction(item.get("direction")), _normalize_strength(item.get("strength")),
                    _normalize_confidence(item.get("confidence")), str(item.get("context") or ""),
                    str(item.get("evidence") or ""), overlap_org_id, overlap_org,
                    str(item.get("overlap_period") or ""),
                ),
            )
            stats.relationships += int(cursor.rowcount > 0)
            for local_source_id in item.get("source_ids") or []:
                source_id = source_map.get(str(local_source_id))
                if source_id:
                    target.execute(
                        """INSERT OR IGNORE INTO evidence_links
                           (evidence_id, source_id, subject_type, subject_id, field_name, confidence)
                           VALUES (?, ?, 'relationship', ?, 'relationship', ?)""",
                        (
                            stable_id("ev", f"{source_id}|relationship|{relationship_id}|relationship"),
                            source_id, relationship_id, _normalize_confidence(item.get("confidence")),
                        ),
                    )

    for predicate, values in (
        ("governance_record", profile.get("governance_record")),
        ("risk_and_integrity_signal", profile.get("risk_and_integrity_signals")),
        ("open_question", profile.get("open_questions")),
    ):
        if not isinstance(values, list):
            continue
        for index, value in enumerate(values):
            claim_id = stable_id("claim", f"{profile_id}|{predicate}|{index}")
            confidence = _normalize_confidence(value.get("confidence")) if isinstance(value, dict) else "unverified"
            cursor = target.execute(
                """INSERT OR IGNORE INTO claims
                   (claim_id, subject_type, subject_id, predicate, value_json, confidence)
                   VALUES (?, 'person', ?, ?, ?, ?)""",
                (claim_id, person_id, predicate, _json(value), confidence),
            )
            stats.claims += int(cursor.rowcount > 0)
    return stats


def _source_type(value: object) -> str:
    text = str(value or "").strip()
    allowed = {"official", "appointment_notice", "media", "encyclopedia", "database", "inferred", "other"}
    aliases = {
        "gov_announcement": "official", "government": "official", "official_web": "official",
        "news": "media", "baike": "encyclopedia",
    }
    text = aliases.get(text, text)
    return text if text in allowed else "other"


def _reliability(value: object) -> str:
    text = str(value or "").strip().lower()
    return text if text in {"high", "medium", "low"} else "low"
