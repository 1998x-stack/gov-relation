"""Tests for fail-safe mechanism in queue.py and worker_loop.py."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Generator

import pytest

from gov_relation.queue import (
    claim_next,
    find_next_claimable,
    load_state,
    reconcile_claims,
    set_claim_status,
)


@pytest.fixture
def mock_all(monkeypatch: Any, tmp_path: Path) -> Generator[Path, None, None]:
    """Fully mock gov_relation paths to point at a temp directory."""
    import gov_relation.paths as p
    import gov_relation.queue as q
    import gov_relation.inventory as inv
    import gov_relation.todo as td

    monkeypatch.setattr(p, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(p, "DATA_DIR", tmp_path / "data")
    monkeypatch.setattr(p, "DATABASE_DIR", tmp_path / "data" / "database")
    monkeypatch.setattr(p, "GRAPH_DIR", tmp_path / "data" / "graph")
    monkeypatch.setattr(p, "PERSONS_DIR", tmp_path / "data" / "persons")
    monkeypatch.setattr(p, "JSON_DIR", tmp_path / "data" / "json")
    monkeypatch.setattr(p, "REPORT_DIR", tmp_path / "report")
    monkeypatch.setattr(p, "DOCS_DIR", tmp_path / "docs")
    monkeypatch.setattr(p, "TMP_DIR", tmp_path / "data" / "tmp")
    monkeypatch.setattr(p, "DISPATCH_STATE_PATH", tmp_path / "data" / "dispatch_state.json")
    monkeypatch.setattr(p, "DISPATCH_LOCK_DIR", tmp_path / "data" / "dispatch_state.lock")
    monkeypatch.setattr(p, "TODO_PATH", tmp_path / "data" / "TODO.json")

    monkeypatch.setattr(q, "DISPATCH_STATE_PATH", tmp_path / "data" / "dispatch_state.json")
    monkeypatch.setattr(q, "DISPATCH_LOCK_DIR", tmp_path / "data" / "dispatch_state.lock")
    monkeypatch.setattr(q, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(inv, "REPO_ROOT", tmp_path)

    monkeypatch.setattr(td, "TODO_PATH", tmp_path / "data" / "TODO.json")
    monkeypatch.setattr(td.load_todo, "__defaults__", (tmp_path / "data" / "TODO.json",))
    monkeypatch.setattr(td.save_todo, "__defaults__", (tmp_path / "data" / "TODO.json",))

    (tmp_path / "data").mkdir(parents=True)
    (tmp_path / "logs" / "dispatch").mkdir(parents=True)
    (tmp_path / "data" / "database").mkdir(parents=True)
    (tmp_path / "data" / "graph").mkdir(parents=True)

    todo = {
        "provinces": [
            {
                "province": "测试省",
                "tasks": [
                    {
                        "id": "task_normal",
                        "region": "A市",
                        "level": "prefecture",
                        "done": False,
                        "targets": [{"role": "市委书记"}],
                    },
                    {
                        "id": "task_blocked",
                        "region": "B市",
                        "level": "prefecture",
                        "done": False,
                        "blocked": True,
                        "blocked_reason": "exceeded max retries",
                        "targets": [{"role": "市委书记"}],
                    },
                ],
            },
        ],
    }
    (tmp_path / "data" / "TODO.json").write_text(json.dumps(todo, ensure_ascii=False))
    yield tmp_path


class TestFindNextClaimableSkipBlocked:
    def test_skips_blocked_tasks(self, mock_all: Path) -> None:
        from gov_relation.todo import load_todo
        todo = load_todo()
        item = find_next_claimable(todo, {"claims": {}})
        assert item is not None
        assert item.item.get("id") == "task_normal"

    def test_returns_none_when_all_done_or_blocked(self, mock_all: Path) -> None:
        from gov_relation.todo import load_todo, mark_done, save_todo
        todo = load_todo()
        mark_done(todo, "task_normal")
        save_todo(todo)
        item = find_next_claimable(todo, {"claims": {}})
        # task_blocked is blocked -> should be skipped -> no more items
        assert item is None

    def test_blocked_task_not_skipped_when_flag_absent(self, mock_all: Path) -> None:
        from gov_relation.todo import load_todo
        todo = load_todo()
        # Remove blocked flag from task_blocked — it should become claimable
        for prov in todo["provinces"]:
            for task in prov["tasks"]:
                if task["id"] == "task_blocked":
                    del task["blocked"]
                    break
        items_before = sum(1 for _ in range(100))  # dummy
        item = find_next_claimable(todo, {"claims": {"task_normal": {"status": "active"}}})
        assert item is not None
        assert item.item.get("id") == "task_blocked"


class TestClaimNextSkipsBlocked:
    def test_claims_normal_instead_of_blocked(self, mock_all: Path) -> None:
        c = claim_next("w1", "iagent")
        assert c is not None
        assert c["task"]["task_id"] == "task_normal"

    def test_returns_none_when_only_blocked_remain(self, mock_all: Path) -> None:
        from gov_relation.todo import load_todo, mark_done, save_todo
        todo = load_todo()
        mark_done(todo, "task_normal")
        save_todo(todo)
        c = claim_next("w1", "iagent")
        assert c is None


class TestBlockedInStatus:
    def test_blocked_tasks_counted_in_status(self, mock_all: Path) -> None:
        from gov_relation.queue import queue_status
        status = queue_status()
        # total 2, done 0, but only 1 claimable
        assert status["total"] == 2
        assert status["remaining"] == 2  # blocked tasks are not "done"
