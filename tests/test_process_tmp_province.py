"""Tests for province-aware staged artifact destinations."""

import importlib.util
import sqlite3
import sys
from pathlib import Path

import pytest


def _module():
    path = Path(".agents/skills/china-gov-network/scripts/process_tmp.py").resolve()
    spec = importlib.util.spec_from_file_location("process_tmp_impl", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_known_task_routes_database_to_province(tmp_path, monkeypatch):
    module = _module()

    class Item:
        province_name = "四川省"

    import gov_relation.todo as todo
    monkeypatch.setattr(todo, "load_todo", lambda: {})
    monkeypatch.setattr(todo, "find_item_by_id", lambda data, task_id: Item())
    destinations, route = module.destinations_for(tmp_path / "sichuan_测试县")
    assert route == "四川省"
    assert str(destinations["database"]).endswith(
        "data/provinces/sichuan/database"
    )
    assert str(destinations["build_script"]).endswith("scripts/build")


def test_unknown_task_keeps_legacy_destinations(tmp_path, monkeypatch):
    module = _module()
    import gov_relation.todo as todo
    monkeypatch.setattr(todo, "load_todo", lambda: {})
    monkeypatch.setattr(todo, "find_item_by_id", lambda data, task_id: None)
    destinations, route = module.destinations_for(tmp_path / "unknown")
    assert route == "legacy-fallback"
    assert destinations["database"] == module.DESTINATIONS["database"]


def test_todo_loading_error_does_not_fall_back_to_legacy(tmp_path, monkeypatch):
    module = _module()
    import gov_relation.todo as todo

    def fail():
        raise ValueError("invalid TODO")

    monkeypatch.setattr(todo, "load_todo", fail)
    with pytest.raises(ValueError, match="invalid TODO"):
        module.destinations_for(tmp_path / "task")


def test_checkpoints_are_not_promoted_as_reports(tmp_path, monkeypatch):
    module = _module()
    import gov_relation.todo as todo

    monkeypatch.setattr(todo, "load_todo", lambda: {})
    monkeypatch.setattr(todo, "find_item_by_id", lambda data, task_id: None)
    staging = tmp_path / "task"
    staging.mkdir()
    (staging / "checkpoint_04_complete.md").write_text("CHECKPOINT:complete")
    (staging / "public_report.md").write_text("# Report")
    actions = module.collect_actions(staging)
    assert [action.source.name for action in actions] == ["public_report.md"]


def test_sqlite_validation_does_not_create_wal_sidecars(tmp_path):
    module = _module()
    database = tmp_path / "staged.db"
    conn = sqlite3.connect(database)
    conn.execute("PRAGMA journal_mode=WAL")
    for table in ("persons", "organizations", "positions", "relationships"):
        conn.execute(f"CREATE TABLE {table}(id INTEGER PRIMARY KEY)")
    conn.commit()
    conn.close()
    Path(f"{database}-wal").unlink(missing_ok=True)
    Path(f"{database}-shm").unlink(missing_ok=True)

    assert module.validate_sqlite(database) == (True, "ok")
    assert not Path(f"{database}-wal").exists()
    assert not Path(f"{database}-shm").exists()
