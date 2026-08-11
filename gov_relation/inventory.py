"""Read-only inventory helpers for scripts and generated artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .log import get_logger
from .paths import DATABASE_DIR, DOCS_DIR, GRAPH_DIR, JSON_DIR, PERSONS_DIR, PROVINCES_DIR, REPORT_DIR, REPO_ROOT, TMP_DIR

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


def _partitioned_paths(
    legacy: Path,
    subdir: str,
    pattern: str,
    provinces_dir: Path | None = None,
) -> list[tuple[Path, str]]:
    province_root = PROVINCES_DIR if provinces_dir is None else provinces_dir
    candidates: list[tuple[Path, str]] = []
    if province_root.exists():
        candidates.extend(
            (path, province.name)
            for province in sorted(province_root.iterdir())
            if province.is_dir()
            for path in sorted((province / subdir).glob(pattern))
        )
    candidates.extend((path, "") for path in sorted(legacy.glob(pattern)))
    output: list[tuple[Path, str]] = []
    seen: set[tuple[int, int]] = set()
    for path, province in candidates:
        if not path.is_file() or path.name.startswith("."):
            continue
        stat = path.stat()
        inode = (stat.st_dev, stat.st_ino)
        if inode not in seen:
            seen.add(inode)
            output.append((path, province))
    return output


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

    provinces_dir = data_dir / "provinces"
    db_rows = _partitioned_paths(db_dir, "database", "*.db", provinces_dir)
    graph_rows = _partitioned_paths(graph_dir, "graph", "*.gexf", provinces_dir)
    person_rows = _partitioned_paths(persons_dir, "persons", "*.json", provinces_dir)
    report_rows = _partitioned_paths(report_dir, "reports", "*", provinces_dir)
    db_stems = {(province, _network_stem(path)) for path, province in db_rows}
    graph_stems = {(province, _network_stem(path)) for path, province in graph_rows}

    def display(keys: set[tuple[str, str]]) -> list[str]:
        return sorted(f"{province}:{stem}" if province else stem for province, stem in keys)

    return Inventory(
        build_scripts=len(scripts),
        databases=len(db_rows),
        graphs=len(graph_rows),
        json_files=_count_files(json_dir, "*.json"),
        person_profiles=len(person_rows),
        reports=len(report_rows),
        docs=_count_files(docs_dir),
        logs=_count_files(root / "logs"),
        tmp_files=_count_visible_files(tmp_dir),
        orphan_databases=display(db_stems - graph_stems),
        orphan_graphs=display(graph_stems - db_stems),
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
