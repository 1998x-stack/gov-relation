"""Top-level orchestration for one regional v3 research package."""

from __future__ import annotations

import sqlite3
from datetime import date
from pathlib import Path

from gov_relation.paths import (
    PROVINCE_SLUGS,
    canonical_province_name,
    province_build_dir,
    province_database_dir,
    province_dir,
    province_graph_dir,
    province_persons_dir,
    province_reports_dir,
    safe_path_component,
)
from gov_relation.runner import run_build

from .build_factory import BuildScriptFactory
from .person_factory import PersonJSONFactory
from .report_factory import ReportFactory


class RegionResearchFactory:
    """Collect structured research and generate its complete package."""

    def __init__(
        self,
        *,
        province: str,
        region: str,
        level: str,
        targets: list[dict],
    ) -> None:
        if province not in PROVINCE_SLUGS and province not in PROVINCE_SLUGS.values():
            raise ValueError(f"unknown province: {province}")
        self.province = province
        self.province_name = canonical_province_name(province)
        self.region = region
        self.level = level
        self.targets = targets
        self._persons: list[dict] = []
        self._organizations: list[dict] = []
        self._positions: list[dict] = []
        self._relationships: list[dict] = []
        self._sources: list[dict] = []
        self._claims: list[dict] = []

    def add_person(self, data: dict) -> None:
        self._persons.append(data)

    def add_organization(self, data: dict) -> None:
        self._organizations.append(data)

    def add_position(self, data: dict) -> None:
        self._positions.append(data)

    def add_relationship(self, data: dict) -> None:
        self._relationships.append(data)

    def add_source(self, data: dict) -> None:
        self._sources.append(data)

    def add_claim(self, data: dict) -> None:
        self._claims.append(data)

    def generate_build_script(self) -> Path:
        province_path = province_dir(self.province)
        script = BuildScriptFactory().generate(
            slug=self.region,
            province_name=self.province_name,
            persons=self._persons,
            organizations=self._organizations,
            positions=self._positions,
            relationships=self._relationships,
            sources=self._sources,
            claims=self._claims,
        )
        output_dir = province_build_dir(self.province)
        output_dir.mkdir(parents=True, exist_ok=True)
        province_slug = province_path.name
        output = output_dir / (
            f"build_{province_slug}_{safe_path_component(self.region)}_data.py"
        )
        output.write_text(script, encoding="utf-8")
        return output

    def generate_gexf(self) -> Path:
        artifact = safe_path_component(self.region)
        database = province_database_dir(self.province) / f"{artifact}_network.db"
        graph = province_graph_dir(self.province) / f"{artifact}_network.gexf"
        run_build(
            slug=self.region,
            persons=self._persons,
            organizations=self._organizations,
            positions=self._positions,
            relationships=self._relationships,
            sources=self._sources,
            claims=self._claims,
            db_path=database,
            gexf_path=graph,
            backend="v3",
            overwrite=True,
        )
        return graph

    def _database_path(self) -> Path:
        path = province_database_dir(self.province) / (
            f"{safe_path_component(self.region)}_network.db"
        )
        if not path.exists():
            self.generate_gexf()
        return path

    def generate_person_profiles(self) -> list[Path]:
        conn = sqlite3.connect(f"file:{self._database_path()}?mode=ro", uri=True)
        try:
            output_dir = province_persons_dir(self.province)
            output_dir.mkdir(parents=True, exist_ok=True)
            profiles = PersonJSONFactory()
            stamp = date.today().strftime("%Y%m%d")
            outputs = []
            for person_id, name in conn.execute(
                "SELECT person_id, canonical_name FROM persons ORDER BY person_id"
            ):
                current = conn.execute(
                    """SELECT title FROM positions
                       WHERE person_id=? AND is_current=1
                       ORDER BY sort_order LIMIT 1""",
                    (person_id,),
                ).fetchone()
                job = current[0] if current else "其他"
                filename = "-".join(
                    safe_path_component(part)
                    for part in (
                        stamp, self.province_name, self.region, job, name,
                    )
                ) + ".json"
                output = output_dir / filename
                profiles.write(conn, person_id, output)
                outputs.append(output)
            return outputs
        finally:
            conn.close()

    def generate_report(self) -> Path:
        conn = sqlite3.connect(f"file:{self._database_path()}?mode=ro", uri=True)
        try:
            output_dir = province_reports_dir(self.province)
            output_dir.mkdir(parents=True, exist_ok=True)
            output = output_dir / (
                f"{safe_path_component(self.region)}_report.md"
            )
            output.write_text(
                ReportFactory().build_from_conn(conn, self.region),
                encoding="utf-8",
            )
            return output
        finally:
            conn.close()
