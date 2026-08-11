"""Tests for legacy/province asset discovery."""

from pathlib import Path

import gov_relation.inventory as inventory
import gov_relation.web as web


def test_inventory_deduplicates_hardlinks_but_keeps_cross_province_names(tmp_path, monkeypatch):
    data = tmp_path / "data"
    legacy = data / "database"
    legacy.mkdir(parents=True)
    source = legacy / "同名区_network.db"
    source.write_bytes(b"db")
    provinces = data / "provinces"
    first = provinces / "a/database/同名区_network.db"
    first.parent.mkdir(parents=True)
    first.hardlink_to(source)
    second = provinces / "b/database/同名区_network.db"
    second.parent.mkdir(parents=True)
    second.write_bytes(b"other")
    monkeypatch.setattr(inventory, "PROVINCES_DIR", provinces)
    rows = inventory._partitioned_paths(legacy, "database", "*.db")
    assert len(rows) == 2
    assert rows[0] == (first, "a")


def test_collect_inventory_uses_requested_root_and_ignores_gitkeep(tmp_path):
    reports = tmp_path / "data" / "provinces" / "sichuan" / "reports"
    reports.mkdir(parents=True)
    (reports / ".gitkeep").touch()
    (reports / "report.md").write_text("# Report")
    result = inventory.collect_inventory(tmp_path)
    assert result.reports == 1


def test_web_partitioned_files_reports_province_slug(tmp_path, monkeypatch):
    legacy = tmp_path / "legacy"
    legacy.mkdir()
    provinces = tmp_path / "provinces"
    target = provinces / "sichuan/graph/a.gexf"
    target.parent.mkdir(parents=True)
    target.write_text("<gexf/>")
    monkeypatch.setattr(web, "PROVINCES_DIR", provinces)
    assert web._partitioned_files(legacy, "graph", "*.gexf") == [(target, "sichuan")]


def test_web_prefers_province_path_for_legacy_hardlink(tmp_path, monkeypatch):
    legacy = tmp_path / "legacy"
    legacy.mkdir()
    old = legacy / "a.gexf"
    old.write_text("<gexf/>")
    provinces = tmp_path / "provinces"
    target = provinces / "sichuan" / "graph" / "a.gexf"
    target.parent.mkdir(parents=True)
    target.hardlink_to(old)
    monkeypatch.setattr(web, "PROVINCES_DIR", provinces)
    assert web._partitioned_files(legacy, "graph", "*.gexf") == [
        (target, "sichuan")
    ]
