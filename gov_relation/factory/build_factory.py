"""Generate standalone province-qualified v3 build scripts."""

from __future__ import annotations

from pathlib import Path
from pprint import pformat

from gov_relation.paths import PROVINCE_SLUGS, safe_path_component


class BuildScriptFactory:
    """Assemble a script that delegates database and graph work to run_build."""

    def generate(
        self,
        *,
        slug: str,
        province_name: str,
        persons: list[dict],
        organizations: list[dict],
        positions: list[dict],
        relationships: list[dict],
        sources: list[dict] | None = None,
        claims: list[dict] | None = None,
    ) -> str:
        province_slug = PROVINCE_SLUGS.get(province_name, province_name)
        artifact_slug = safe_path_component(slug)
        values = {
            "PERSONS": persons,
            "ORGANIZATIONS": organizations,
            "POSITIONS": positions,
            "RELATIONSHIPS": relationships,
            "SOURCES": sources or [],
            "CLAIMS": claims or [],
        }
        declarations = "\n\n".join(
            f"{name} = {pformat(value, width=100, sort_dicts=False)}"
            for name, value in values.items()
        )
        return f'''#!/usr/bin/env python3
"""Build the {slug} v3 government-personnel network."""

from datetime import date
from pathlib import Path

from gov_relation.factory import PersonJSONFactory, ReportFactory
from gov_relation.paths import safe_path_component
from gov_relation.runner import run_build


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "gov_relation").is_dir():
            return parent
    raise RuntimeError("Cannot locate repo root: gov_relation/ not found among parents")

REPO_ROOT = _repo_root()
PROVINCE_DIR = REPO_ROOT / "data" / "provinces" / {province_slug!r}
DB_PATH = PROVINCE_DIR / "database" / {f'{artifact_slug}_network.db'!r}
GEXF_PATH = PROVINCE_DIR / "graph" / {f'{artifact_slug}_network.gexf'!r}
PERSONS_DIR = PROVINCE_DIR / "persons"
REPORTS_DIR = PROVINCE_DIR / "reports"

{declarations}


def main() -> None:
    run_build(
        slug={slug!r}, persons=PERSONS, organizations=ORGANIZATIONS,
        positions=POSITIONS, relationships=RELATIONSHIPS,
        sources=SOURCES, claims=CLAIMS, db_path=DB_PATH,
        gexf_path=GEXF_PATH, backend="v3", overwrite=True,
    )
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    try:
        PERSONS_DIR.mkdir(parents=True, exist_ok=True)
        profiles = PersonJSONFactory()
        stamp = date.today().strftime("%Y%m%d")
        for person_id, name in conn.execute(
            "SELECT person_id, canonical_name FROM persons ORDER BY person_id"
        ):
            current = conn.execute(
                "SELECT title FROM positions WHERE person_id=? AND is_current=1 "
                "ORDER BY sort_order LIMIT 1", (person_id,),
            ).fetchone()
            job = current[0] if current else "其他"
            filename = "-".join(
                safe_path_component(part)
                for part in (stamp, {province_name!r}, {slug!r}, job, name)
            ) + ".json"
            profiles.write(conn, person_id, PERSONS_DIR / filename)
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        report = ReportFactory().build_from_conn(conn, {slug!r})
        (REPORTS_DIR / {f'{artifact_slug}_report.md'!r}).write_text(
            report, encoding="utf-8"
        )
    finally:
        conn.close()


if __name__ == "__main__":
    main()
'''
