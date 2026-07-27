"""Read-only inventory helpers for scripts and generated artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .log import get_logger
from .paths import DATABASE_DIR, DOCS_DIR, GRAPH_DIR, JSON_DIR, PERSONS_DIR, REPORT_DIR, REPO_ROOT, TMP_DIR

logger = get_logger(__name__)


@dataclass(frozen=True)
class Inventory:
    build_scripts: int
    databases: int
    graphs: int
    json_files: int
    person_profiles: int
    reports: int
    docs: int
    logs: int
    tmp_files: int
    orphan_databases: list[str]
    orphan_graphs: list[str]


def _count_files(directory: Path, pattern: str = "*") -> int:
    if not directory.exists():
        return 0
    return sum(1 for path in directory.glob(pattern) if path.is_file())


def _count_visible_files(directory: Path, pattern: str = "*") -> int:
    if not directory.exists():
        return 0
    return sum(1 for path in directory.glob(pattern) if path.is_file() and not path.name.startswith("."))


def _network_stem(path: Path) -> str:
    stem = path.stem
    return stem.removesuffix("_network")


def collect_inventory(root: Path = REPO_ROOT) -> Inventory:
    scripts = sorted(root.glob("build_*_data.py"))
    build_dir = root / "scripts" / "build"
    if build_dir.exists():
        scripts.extend(sorted(build_dir.glob("*_data.py")))

    data_dir = root / "data"
    db_dir = data_dir / "database"
    graph_dir = data_dir / "graph"
    json_dir = data_dir / "json"
    persons_dir = data_dir / "persons"
    tmp_dir = data_dir / "tmp"
    report_dir = root / "report"
    docs_dir = root / "docs"

    dbs = sorted(db_dir.glob("*.db"))
    graphs = sorted(graph_dir.glob("*.gexf"))
    db_stems = {_network_stem(path) for path in dbs}
    graph_stems = {_network_stem(path) for path in graphs}

    return Inventory(
        build_scripts=len(scripts),
        databases=len(dbs),
        graphs=len(graphs),
        json_files=_count_files(json_dir, "*.json"),
        person_profiles=_count_files(persons_dir, "*.json"),
        reports=_count_files(report_dir),
        docs=_count_files(docs_dir),
        logs=_count_files(root / "logs"),
        tmp_files=_count_visible_files(tmp_dir),
        orphan_databases=sorted(db_stems - graph_stems),
        orphan_graphs=sorted(graph_stems - db_stems),
    )


def format_inventory(inv: Inventory) -> str:
    lines = [
        "Repository inventory:",
        f"  Build scripts: {inv.build_scripts}",
        f"  Databases:     {inv.databases}",
        f"  GEXF graphs:   {inv.graphs}",
        f"  JSON files:    {inv.json_files}",
        f"  Person JSON:   {inv.person_profiles}",
        f"  Reports:       {inv.reports}",
        f"  Docs:          {inv.docs}",
        f"  Logs:          {inv.logs}",
        f"  Tmp files:     {inv.tmp_files}",
        "",
        f"Database without matching GEXF: {len(inv.orphan_databases)}",
    ]
    lines.extend(f"  - {name}" for name in inv.orphan_databases[:30])
    if len(inv.orphan_databases) > 30:
        lines.append(f"  ... {len(inv.orphan_databases) - 30} more")

    lines.append("")
    lines.append(f"GEXF without matching database: {len(inv.orphan_graphs)}")
    lines.extend(f"  - {name}" for name in inv.orphan_graphs[:30])
    if len(inv.orphan_graphs) > 30:
        lines.append(f"  ... {len(inv.orphan_graphs) - 30} more")
    return "\n".join(lines)
