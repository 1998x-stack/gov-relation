"""Tests for gov_relation/paths.py."""

from __future__ import annotations

from pathlib import Path

from gov_relation.paths import REPO_ROOT, DATA_DIR, data_path, repo_path


class TestPathConstants:
    def test_repo_root_is_absolute(self) -> None:
        assert REPO_ROOT.is_absolute()

    def test_repo_root_contains_package(self) -> None:
        # 特征目录检查(不依赖 checkout 目录名,支持任意克隆路径)
        assert (REPO_ROOT / "gov_relation").is_dir()
        assert REPO_ROOT.is_absolute()

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


class TestCentralPaths:
    def test_central_paths_have_correct_names(self) -> None:
        from gov_relation.paths import REGISTRY_DB, PROVINCE_DIR
        assert REGISTRY_DB.name == "registry.db"
        assert PROVINCE_DIR.name == "provincial"

    def test_central_paths_under_data_central(self) -> None:
        from gov_relation.paths import CENTRAL_DIR
        assert str(CENTRAL_DIR).endswith("data/central")


class TestProvincePaths:
    def test_chinese_province_maps_to_stable_slug(self) -> None:
        from gov_relation.paths import PROVINCES_DIR, province_dir

        assert province_dir("四川省") == PROVINCES_DIR / "sichuan"

    def test_slug_is_accepted_without_translation(self) -> None:
        from gov_relation.paths import PROVINCES_DIR, province_dir

        assert province_dir("sichuan") == PROVINCES_DIR / "sichuan"

    def test_builders_remain_under_scripts_build(self) -> None:
        from gov_relation.paths import REPO_ROOT, province_build_dir

        assert province_build_dir("四川省") == REPO_ROOT / "scripts" / "build"

    def test_province_artifact_subdirectories(self) -> None:
        from gov_relation.paths import (
            PROVINCES_DIR,
            province_database_dir,
            province_graph_dir,
            province_persons_dir,
            province_reports_dir,
        )

        base = PROVINCES_DIR / "sichuan"
        assert province_database_dir("四川省") == base / "database"
        assert province_graph_dir("四川省") == base / "graph"
        assert province_persons_dir("四川省") == base / "persons"
        assert province_reports_dir("四川省") == base / "reports"
