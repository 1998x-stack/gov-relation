"""Tests for process_tmp.py CLI behavior (auto-cleanup on --move)."""

from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

PROCESS_TMP_SCRIPT = (
    Path(__file__).resolve().parents[1]
    / ".agents" / "skills" / "china-gov-network" / "scripts" / "process_tmp.py"
)


def _run_process_tmp(staging_dir: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(PROCESS_TMP_SCRIPT), str(staging_dir), *args],
        capture_output=True, text=True, timeout=15,
        cwd=staging_dir.parents[2],
    )


@pytest.fixture
def staging_dir(tmp_path: Path) -> Path:
    staging = tmp_path / "data" / "tmp" / "test_region"
    staging.mkdir(parents=True)

    (staging / "build_test_region_data.py").write_text('import sqlite3; DB_PATH = "x"; GEXF_PATH = "y"\n')

    db = staging / "test_region_network.db"
    conn = sqlite3.connect(str(db))
    conn.execute("CREATE TABLE persons (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("CREATE TABLE organizations (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("CREATE TABLE positions (id INTEGER PRIMARY KEY, person_id INTEGER, org_id INTEGER)")
    conn.execute("CREATE TABLE relationships (id INTEGER PRIMARY KEY, person_a INTEGER, person_b INTEGER)")
    conn.commit(); conn.close()

    (staging / "test_region_network.gexf").write_text(
        '<?xml version="1.0"?><gexf><graph><nodes></nodes><edges></edges></graph></gexf>'
    )
    person = staging / "20260723-test.json"
    person.write_text(json.dumps({
        "identity": {"name": "张三"}, "career_timeline": [], "source_register": {},
    }, ensure_ascii=False))

    (tmp_path / "data" / "database").mkdir(parents=True)
    (tmp_path / "data" / "graph").mkdir(parents=True)
    (tmp_path / "data" / "persons").mkdir(parents=True)
    (tmp_path / "report").mkdir()
    (tmp_path / "logs" / "dispatch").mkdir(parents=True)
    return staging


class TestProcessTmpCLI:
    def test_dry_run_keeps_staging(self, staging_dir: Path) -> None:
        r = _run_process_tmp(staging_dir, "--allow-external")
        assert r.returncode == 0
        assert staging_dir.exists()
        assert (staging_dir / "build_test_region_data.py").exists()

    def test_move_removes_files(self, staging_dir: Path) -> None:
        r = _run_process_tmp(staging_dir, "--move", "--overwrite", "--allow-partial", "--allow-external")
        assert r.returncode == 0, f"stderr: {r.stderr}"
        assert "Cleaned up promoted files" in r.stdout

    def test_move_leaves_unknown_files(self, staging_dir: Path) -> None:
        (staging_dir / "extra_notes.txt").write_text("keep me")
        r = _run_process_tmp(staging_dir, "--move", "--overwrite", "--allow-partial", "--allow-external")
        assert r.returncode == 0

    def test_invalid_staging_returns_error(self, tmp_path: Path) -> None:
        r = _run_process_tmp(tmp_path / "nonexistent", "--allow-external")
        assert r.returncode == 1
