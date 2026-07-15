"""Repository path helpers."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
TMP_DIR = DATA_DIR / "tmp"
DISPATCH_STATE_PATH = DATA_DIR / "dispatch_state.json"
DISPATCH_LOCK_DIR = DATA_DIR / "dispatch_state.lock"
DATABASE_DIR = DATA_DIR / "database"
GRAPH_DIR = DATA_DIR / "graph"
JSON_DIR = DATA_DIR / "json"
PERSONS_DIR = DATA_DIR / "persons"
REPORT_DIR = REPO_ROOT / "report"
DOCS_DIR = REPO_ROOT / "docs"
TODO_PATH = DATA_DIR / "TODO.json"


def repo_path(*parts: str) -> Path:
    """Return a path rooted at the repository."""
    return REPO_ROOT.joinpath(*parts)


def data_path(*parts: str) -> Path:
    """Return a path rooted at data/."""
    return DATA_DIR.joinpath(*parts)
