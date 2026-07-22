"""Tests for gov_relation/inventory.py."""

from __future__ import annotations

from pathlib import Path

from gov_relation.inventory import _count_files, _count_visible_files, _network_stem, collect_inventory


class TestCountFiles:
    def test_returns_zero_for_nonexistent(self, tmp_path: Path) -> None:
        assert _count_files(tmp_path / "nonexistent") == 0

    def test_counts_files_in_directory(self, tmp_path: Path) -> None:
        (tmp_path / "a.txt").write_text("a")
        (tmp_path / "b.txt").write_text("b")
        assert _count_files(tmp_path) == 2

    def test_ignores_subdirectories(self, tmp_path: Path) -> None:
        (tmp_path / "a.txt").write_text("a")
        (tmp_path / "sub").mkdir()
        assert _count_files(tmp_path) == 1


class TestCountVisibleFiles:
    def test_excludes_dotfiles(self, tmp_path: Path) -> None:
        (tmp_path / "visible.txt").write_text("x")
        (tmp_path / ".hidden.txt").write_text("x")
        assert _count_visible_files(tmp_path) == 1


class TestNetworkStem:
    def test_removes_network_suffix(self) -> None:
        assert _network_stem(Path("anyi_network.db")) == "anyi"

    def test_no_suffix(self) -> None:
        assert _network_stem(Path("anyi.db")) == "anyi"

    def test_empty_stem(self) -> None:
        assert _network_stem(Path("_network.db")) == ""


class TestCollectInventory:
    def test_empty_directory(self, tmp_path: Path) -> None:
        inv = collect_inventory(tmp_path)
        assert inv.databases == 0
        assert inv.graphs == 0
        assert inv.build_scripts == 0

    def test_counts_databases(self, tmp_path: Path) -> None:
        (tmp_path / "data" / "database").mkdir(parents=True)
        (tmp_path / "data" / "database" / "anyi_network.db").write_text("x")
        inv = collect_inventory(tmp_path)
        assert inv.databases == 1

    def detects_orphan_databases(self, tmp_path: Path) -> None:
        (tmp_path / "data" / "database").mkdir(parents=True)
        (tmp_path / "data" / "graph").mkdir(parents=True)
        (tmp_path / "data" / "database" / "orphan_network.db").write_text("x")
        inv = collect_inventory(tmp_path)
        assert "orphan" in inv.orphan_databases

    def detects_orphan_graphs(self, tmp_path: Path) -> None:
        (tmp_path / "data" / "database").mkdir(parents=True)
        (tmp_path / "data" / "graph").mkdir(parents=True)
        (tmp_path / "data" / "graph" / "orphan_network.gexf").write_text("x")
        inv = collect_inventory(tmp_path)
        assert "orphan" in inv.orphan_graphs

    def test_balanced_db_and_graph_no_orphans(self, tmp_path: Path) -> None:
        (tmp_path / "data" / "database").mkdir(parents=True)
        (tmp_path / "data" / "graph").mkdir(parents=True)
        (tmp_path / "data" / "database" / "test_network.db").write_text("x")
        (tmp_path / "data" / "graph" / "test_network.gexf").write_text("x")
        inv = collect_inventory(tmp_path)
        assert inv.databases == 1
        assert inv.graphs == 1
        assert inv.orphan_databases == []
        assert inv.orphan_graphs == []
