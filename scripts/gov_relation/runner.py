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

import sqlite3
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
) -> None:
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
