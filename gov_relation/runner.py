"""Top-level orchestration for a single region network build.

Usage::

    from gov_relation.runner import run_build
    from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

    run_build(
        slug="七里河区",
        persons=[...],
        organizations=[...],
        positions=[...],
        relationships=[...],
        db_path=DATABASE_DIR / "七里河区_network.db",
        gexf_path=GRAPH_DIR / "七里河区_network.gexf",
    )
"""

from __future__ import annotations

import os
import shutil
import sqlite3
import tempfile
import uuid
from pathlib import Path
from typing import Any

from .gexf import GEXFBuilder
from .log import get_logger
from .schema import (
    create_tables,
    insert_organizations,
    insert_persons,
    insert_positions,
    insert_relationships,
)

logger = get_logger(__name__)


def run_build(
    *,
    slug: str,
    persons: list[dict[str, Any]],
    organizations: list[dict[str, Any]],
    positions: list[dict[str, Any]],
    relationships: list[dict[str, Any]],
    db_path: str | Path,
    gexf_path: str | Path,
    overwrite: bool = False,
    central: Any = None,  # Optional Central writer
    backend: str = "legacy",
    sources: list[dict[str, Any]] | None = None,
    claims: list[dict[str, Any]] | None = None,
) -> None:
    if backend == "v3":
        _run_v3_build(
            slug=slug,
            persons=persons,
            organizations=organizations,
            positions=positions,
            relationships=relationships,
            sources=sources or [],
            claims=claims or [],
            db_path=db_path,
            gexf_path=gexf_path,
            overwrite=overwrite,
        )
        return
    if backend != "legacy":
        raise ValueError(f"unsupported build backend: {backend}")
    db_path = Path(db_path)
    gexf_path = Path(gexf_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    gexf_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info("Building database: %s", db_path)
    conn = sqlite3.connect(str(db_path))
    try:
        create_tables(conn, overwrite=overwrite)
        insert_persons(conn, persons)
        insert_organizations(conn, organizations)
        insert_positions(conn, positions)
        insert_relationships(conn, relationships)
        logger.info(
            "DB ready: %d persons, %d orgs, %d positions, %d relationships",
            len(persons),
            len(organizations),
            len(positions),
            len(relationships),
        )
    finally:
        conn.close()

    logger.info("Building GEXF: %s", gexf_path)
    builder = GEXFBuilder(title=slug)
    for p in persons:
        builder.add_person(
            id=p["id"],
            name=p.get("name", ""),
            current_post=p.get("current_post", ""),
            current_org=p.get("current_org", ""),
            gender=p.get("gender", ""),
            ethnicity=p.get("ethnicity", ""),
            birth=p.get("birth", ""),
            source=p.get("source", ""),
        )
    for o in organizations:
        builder.add_organization(
            id=o["id"] + 100000,
            name=o.get("name", ""),
            org_type=o.get("type", ""),
            level=o.get("level", ""),
            location=o.get("location", ""),
        )
    for r in relationships:
        builder.add_relationship(
            source=r["person_a"],
            target=r["person_b"],
            rel_type=r.get("type", ""),
            context=r.get("context", ""),
            overlap_org=r.get("overlap_org", ""),
            overlap_period=r.get("overlap_period", ""),
        )
    builder.write(gexf_path)
    logger.info("GEXF ready: %s", gexf_path)

    # ── Central registry ────────────────────────────────────────────
    if central is not None:
        # Build id → hash maps so positions/relationships can reference correctly
        person_id_to_hash: dict[str, str] = {}
        org_id_to_hash: dict[str, str] = {}
        for p in persons:
            h = central.merge_person(p)
            person_id_to_hash[str(p.get("id", ""))] = h
        for o in organizations:
            h = central.merge_organization(o)
            org_id_to_hash[str(o.get("id", ""))] = h
        for pos in positions:
            p_hash = person_id_to_hash.get(str(pos.get("person_id", "")))
            o_hash = org_id_to_hash.get(str(pos.get("org_id", "")))
            if p_hash and o_hash:
                central.insert_position({
                    "person_hash": p_hash,
                    "org_hash": o_hash,
                    "title": pos.get("title", ""),
                    "start_date": pos.get("start_date", ""),
                    "end_date": pos.get("end_date", ""),
                    "rank": pos.get("rank", ""),
                    "note": pos.get("note", ""),
                    "province": central.province,
                    "source": "",
                })
        for rel in relationships:
            pa_hash = person_id_to_hash.get(str(rel.get("person_a", "")))
            pb_hash = person_id_to_hash.get(str(rel.get("person_b", "")))
            if pa_hash and pb_hash:
                central.insert_relationship({
                    "person_a_hash": pa_hash,
                    "person_b_hash": pb_hash,
                    "type": rel.get("type", ""),
                    "context": rel.get("context", ""),
                    "overlap_org_hash": "",
                    "overlap_period": rel.get("overlap_period", ""),
                    "province": central.province,
                    "source": "",
                })


def _run_v3_build(
    *,
    slug: str,
    persons: list[dict[str, Any]],
    organizations: list[dict[str, Any]],
    positions: list[dict[str, Any]],
    relationships: list[dict[str, Any]],
    sources: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    db_path: str | Path,
    gexf_path: str | Path,
    overwrite: bool,
) -> None:
    """Build and publish a regional v3 package without exposing partial output."""
    from .factory import GEXFFactory, InsertFactory, SchemaFactory

    database = Path(db_path)
    graph = Path(gexf_path)
    database.parent.mkdir(parents=True, exist_ok=True)
    graph.parent.mkdir(parents=True, exist_ok=True)
    if not overwrite and (database.exists() or graph.exists()):
        raise FileExistsError("v3 build output exists; pass overwrite=True")

    temp_database = _temporary_output(database)
    temp_graph = _temporary_output(graph)
    conn = sqlite3.connect(temp_database)
    build_complete = False
    try:
        SchemaFactory().create_all(conn)
        inserts = InsertFactory()
        person_ids: dict[str, str | None] = {}
        person_refs: dict[str, str] = {}
        for person in persons:
            item = dict(person)
            source_pk = item.get("_source_pk")
            person_id = inserts.upsert_person(
                conn,
                item,
                source_pk=str(source_pk) if source_pk is not None else None,
            )
            _register_name(person_ids, str(item.get("canonical_name", "")), person_id)
            if source_pk is not None:
                _register_ref(person_refs, str(source_pk), person_id, "person")
        organization_ids: dict[str, str | None] = {}
        organization_refs: dict[str, str] = {}
        for organization in organizations:
            item = dict(organization)
            organization_id = inserts.upsert_organization(conn, item)
            _register_name(
                organization_ids,
                str(item.get("canonical_name", "")),
                organization_id,
            )
            if item.get("_source_pk") is not None:
                _register_ref(
                    organization_refs,
                    str(item["_source_pk"]),
                    organization_id,
                    "organization",
                )

        for position in positions:
            item = dict(position)
            if not item.get("person_id"):
                item["person_id"] = _resolve_reference(
                    item,
                    ref_field="person_ref",
                    name_field="person_name",
                    refs=person_refs,
                    names=person_ids,
                    kind="person",
                )
            if not item["person_id"]:
                raise ValueError(f"position has unresolved person: {position!r}")
            if not item.get("organization_id") and (
                item.get("organization_name") or item.get("organization_ref")
            ):
                item["organization_id"] = _resolve_reference(
                    item,
                    ref_field="organization_ref",
                    name_field="organization_name",
                    refs=organization_refs,
                    names=organization_ids,
                    kind="organization",
                )
                if not item["organization_id"]:
                    raise ValueError(
                        f"position has unresolved organization: {position!r}"
                    )
            inserts.insert_position(conn, item)

        for relationship in relationships:
            item = dict(relationship)
            if not item.get("person_from_id"):
                item["person_from_id"] = _resolve_reference(
                    item,
                    ref_field="person_from_ref",
                    name_field="person_from_name",
                    refs=person_refs,
                    names=person_ids,
                    kind="person",
                )
            if not item.get("person_to_id"):
                item["person_to_id"] = _resolve_reference(
                    item,
                    ref_field="person_to_ref",
                    name_field="person_to_name",
                    refs=person_refs,
                    names=person_ids,
                    kind="person",
                )
            if not item["person_from_id"] or not item["person_to_id"]:
                raise ValueError(
                    f"relationship has unresolved person: {relationship!r}"
                )
            inserts.insert_relationship(conn, item)
        for source in sources:
            inserts.insert_source(conn, source)
        for claim in claims:
            inserts.insert_claim(conn, claim)
        conn.commit()
        if conn.execute("PRAGMA foreign_key_check").fetchone() is not None:
            raise sqlite3.IntegrityError("v3 build contains foreign-key violations")
        GEXFFactory().write(conn, slug, temp_graph)
        build_complete = True
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
        if not build_complete:
            _remove_sqlite_output(temp_database)
            temp_graph.unlink(missing_ok=True)
    try:
        _publish_outputs(((temp_database, database), (temp_graph, graph)))
    finally:
        _remove_sqlite_output(temp_database)
        temp_graph.unlink(missing_ok=True)


def _temporary_output(target: Path) -> Path:
    handle, value = tempfile.mkstemp(
        prefix=f".{target.name}.", suffix=".building", dir=target.parent
    )
    os.close(handle)
    return Path(value)


def _register_name(mapping: dict[str, str | None], name: str, entity_id: str) -> None:
    """Register a unique natural-name lookup while retaining ambiguity."""
    if not name:
        return
    if name in mapping and mapping[name] != entity_id:
        mapping[name] = None
    else:
        mapping[name] = entity_id


def _register_ref(
    mapping: dict[str, str], reference: str, entity_id: str, kind: str
) -> None:
    if not reference:
        raise ValueError(f"{kind} reference must not be empty")
    if reference in mapping and mapping[reference] != entity_id:
        raise ValueError(f"duplicate {kind} reference: {reference!r}")
    mapping[reference] = entity_id


def _resolve_reference(
    item: dict[str, Any],
    *,
    ref_field: str,
    name_field: str,
    refs: dict[str, str],
    names: dict[str, str | None],
    kind: str,
) -> str:
    reference = str(item.pop(ref_field, ""))
    if reference:
        return refs.get(reference, "")
    name = str(item.pop(name_field, ""))
    if name in names and names[name] is None:
        raise ValueError(
            f"ambiguous {kind} name {name!r}; use an explicit {ref_field}"
        )
    return names.get(name) or ""


def _publish_outputs(outputs: tuple[tuple[Path, Path], ...]) -> None:
    """Replace a set of outputs and restore all originals on ordinary failure."""
    token = uuid.uuid4().hex
    backups: dict[Path, Path] = {}
    published: set[Path] = set()
    try:
        for _, target in outputs:
            if target.exists():
                backup = target.with_name(f".{target.name}.{token}.backup")
                shutil.copy2(target, backup)
                backups[target] = backup
        for staged, target in outputs:
            os.replace(staged, target)
            published.add(target)
    except BaseException:
        for target in published:
            target.unlink(missing_ok=True)
        for target, backup in backups.items():
            os.replace(backup, target)
        raise
    finally:
        for backup in backups.values():
            backup.unlink(missing_ok=True)


def _remove_sqlite_output(path: Path) -> None:
    path.unlink(missing_ok=True)
    Path(f"{path}-wal").unlink(missing_ok=True)
    Path(f"{path}-shm").unlink(missing_ok=True)
