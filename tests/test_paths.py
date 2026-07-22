"""Tests for gov_relation/paths.py."""

from __future__ import annotations

from pathlib import Path

from gov_relation.paths import REPO_ROOT, DATA_DIR, data_path, repo_path


class TestPathConstants:
    def test_repo_root_is_absolute(self) -> None:
        assert REPO_ROOT.is_absolute()

    def test_repo_root_ends_with_gov_relation(self) -> None:
        assert REPO_ROOT.name == "gov-relation"

    def test_data_dir_is_under_repo_root(self) -> None:
        assert str(DATA_DIR).startswith(str(REPO_ROOT))

    def test_data_dir_named_data(self) -> None:
        assert DATA_DIR.name == "data"


class TestRepoPath:
    def test_repo_path_joins_relative(self) -> None:
        result = repo_path("scripts", "build", "test.py")
        assert result == REPO_ROOT / "scripts" / "build" / "test.py"

    def test_repo_path_is_absolute(self) -> None:
        assert repo_path("foo").is_absolute()

    def test_repo_path_empty_returns_repo_root(self) -> None:
        assert repo_path() == REPO_ROOT


class TestDataPath:
    def test_data_path_joins_relative(self) -> None:
        result = data_path("database", "test.db")
        assert result == DATA_DIR / "database" / "test.db"

    def test_data_path_is_under_data(self) -> None:
        result = data_path("tmp", "foo.txt")
        assert str(result).startswith(str(DATA_DIR))

    def test_data_path_empty_returns_data_dir(self) -> None:
        assert data_path() == DATA_DIR
