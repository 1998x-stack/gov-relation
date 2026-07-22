"""Tests for gov_relation/queue.py."""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any, Generator

import pytest

from gov_relation.queue import (
    LOCK_STALE_SECONDS,
    active_claim_ids,
    canonical_artifacts_ready,
    cleanup_worker_active_claims_unlocked,
    find_next_claimable,
    force_unlock,
    load_state,
    now_iso,
    queue_lock,
    reconcile_claims,
    set_claim_status,
)
from gov_relation.slugs import artifact_paths


@pytest.fixture
def mock_all(monkeypatch: Any, tmp_path: Path) -> Generator[Path, None, None]:
    """Fully mock gov_relation paths to point at a temp directory."""
    import gov_relation.paths as p
    import gov_relation.queue as q
    import gov_relation.slugs as sl
    import gov_relation.inventory as inv

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

    # Also patch queue and inventory since they cache references at import time
    monkeypatch.setattr(q, "DISPATCH_STATE_PATH", tmp_path / "data" / "dispatch_state.json")
    monkeypatch.setattr(q, "DISPATCH_LOCK_DIR", tmp_path / "data" / "dispatch_state.lock")
    monkeypatch.setattr(q, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(inv, "REPO_ROOT", tmp_path)

    # Patch todo module's cached TODO_PATH and its default param in load_todo
    import gov_relation.todo as td
    monkeypatch.setattr(td, "TODO_PATH", tmp_path / "data" / "TODO.json")
    monkeypatch.setattr(td.load_todo, "__defaults__", (tmp_path / "data" / "TODO.json",))
    monkeypatch.setattr(td.save_todo, "__defaults__", (tmp_path / "data" / "TODO.json",))

    # Create minimal directories and TODO
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
                        "id": "task_a",
                        "region": "A市",
                        "level": "prefecture",
                        "done": False,
                        "targets": [{"role": "市委书记"}],
                    },
                    {
                        "id": "task_b",
                        "region": "B市",
                        "level": "prefecture",
                        "done": False,
                        "targets": [{"role": "市委书记"}],
                    },
                ],
            },
        ],
    }
    (tmp_path / "data" / "TODO.json").write_text(json.dumps(todo, ensure_ascii=False))
    yield tmp_path


# ── Basic helpers ──


class TestNowIso:
    def test_returns_iso_format(self) -> None:
        val = now_iso()
        assert "T" in val


class TestActiveClaimIds:
    def test_returns_active_task_ids(self) -> None:
        state = {"claims": {"t1": {"status": "active"}, "t2": {"status": "done"}}}
        assert active_claim_ids(state) == {"t1"}

    def test_empty(self) -> None:
        assert active_claim_ids({}) == set()


class TestFindNextClaimable:
    def test_finds_first_undone(self, mock_all: Path) -> None:
        from gov_relation.todo import load_todo
        todo = load_todo()
        item = find_next_claimable(todo, {"claims": {}})
        assert item is not None
        assert item.item.get("id") == "task_a"

    def test_skips_active(self, mock_all: Path) -> None:
        from gov_relation.todo import load_todo
        todo = load_todo()
        item = find_next_claimable(todo, {"claims": {"task_a": {"status": "active"}}})
        assert item is not None
        assert item.item.get("id") == "task_b"

    def test_all_active_returns_none(self, mock_all: Path) -> None:
        from gov_relation.todo import load_todo
        todo = load_todo()
        state = {"claims": {"task_a": {"status": "active"}, "task_b": {"status": "active"}}}
        assert find_next_claimable(todo, state) is None


class TestLoadSaveState:
    def test_load_creates_default_on_missing(self, mock_all: Path) -> None:
        state = load_state()
        assert "version" in state
        assert state["version"] == 1


class TestSetClaimStatus:
    def test_mark_done(self, mock_all: Path) -> None:
        from gov_relation.queue import claim_next
        c = claim_next("w1", "iagent")
        set_claim_status(c["task"]["task_id"], "w1", "done")
        from gov_relation.todo import load_todo, find_item_by_id
        assert find_item_by_id(load_todo(), c["task"]["task_id"]).item.get("done") is True

    def test_mark_failed(self, mock_all: Path) -> None:
        from gov_relation.queue import claim_next
        c = claim_next("w1", "iagent")
        set_claim_status(c["task"]["task_id"], "w1", "failed", "timeout")
        state = load_state()
        assert state["claims"][c["task"]["task_id"]]["status"] == "failed"

    def test_wrong_worker_raises(self, mock_all: Path) -> None:
        from gov_relation.queue import claim_next
        c = claim_next("w1", "iagent")
        with pytest.raises(PermissionError):
            set_claim_status(c["task"]["task_id"], "w2", "done")


class TestClaimNext:
    def test_claims_next(self, mock_all: Path) -> None:
        from gov_relation.queue import claim_next
        c = claim_next("w1", "iagent")
        assert c is not None
        assert c["task"]["task_id"] == "task_a"
        assert c["worker_id"] == "w1"

    def test_prompt_file_created(self, mock_all: Path) -> None:
        from gov_relation.queue import claim_next
        c = claim_next("w1", "iagent")
        prompt = Path(c["prompt_path"])
        assert prompt.exists() or (mock_all / c["prompt_path"]).exists()

    def test_returns_none_when_all_done(self, mock_all: Path) -> None:
        from gov_relation.queue import claim_next
        from gov_relation.todo import load_todo, save_todo
        todo = load_todo()
        for t in todo["provinces"][0]["tasks"]:
            t["done"] = True
        save_todo(todo)
        assert claim_next("w1", "iagent") is None


class TestQueueLock:
    def test_acquire_release(self, mock_all: Path) -> None:
        from gov_relation.paths import DISPATCH_LOCK_DIR
        with queue_lock():
            assert DISPATCH_LOCK_DIR.exists()
        assert not DISPATCH_LOCK_DIR.exists()

    def test_contended_lock_timeout(self, mock_all: Path) -> None:
        from gov_relation.paths import DISPATCH_LOCK_DIR
        DISPATCH_LOCK_DIR.mkdir(parents=True, exist_ok=True)
        with pytest.raises(TimeoutError):
            with queue_lock(timeout=0.2, poll=0.05):
                pass


class TestForceUnlock:
    def test_removes_lock(self, mock_all: Path) -> None:
        from gov_relation.paths import DISPATCH_LOCK_DIR
        DISPATCH_LOCK_DIR.mkdir(parents=True, exist_ok=True)
        assert force_unlock() is True
        assert not DISPATCH_LOCK_DIR.exists()

    def test_no_lock_returns_false(self, mock_all: Path) -> None:
        assert force_unlock() is False


class TestCanonicalArtifactsReady:
    def test_missing_artifacts(self, mock_all: Path) -> None:
        task = {"region": "A市"}
        ready, missing = canonical_artifacts_ready(task)
        assert ready is False

    def test_all_artifacts_present(self, mock_all: Path) -> None:
        from gov_relation.paths import REPO_ROOT
        paths = artifact_paths("A市")
        script = REPO_ROOT / paths["build_script"]
        db = REPO_ROOT / paths["db_output"]
        gexf = REPO_ROOT / paths["gexf_output"]
        script.parent.mkdir(parents=True, exist_ok=True)
        db.parent.mkdir(parents=True, exist_ok=True)
        gexf.parent.mkdir(parents=True, exist_ok=True)
        script.write_text("#")
        db.write_text("")
        gexf.write_text("")
        ready, missing = canonical_artifacts_ready(task := {"region": "A市"})
        assert ready is True, f"missing: {missing}"


class TestReconcileClaims:
    def test_releases_all_active(self, mock_all: Path) -> None:
        from gov_relation.queue import claim_next
        claim_next("w1", "iagent")
        claim_next("w2", "iagent")
        actions = reconcile_claims(release_active=True, reason="test")
        released = [a for a in actions if a["action"] == "released"]
        assert len(released) == 2


class TestCleanupWorkerActiveClaimsUnlocked:
    def test_releases_previous_claims(self, mock_all: Path) -> None:
        from gov_relation.todo import load_todo
        todo = load_todo()
        state = {
            "claims": {
                "task_a": {
                    "status": "active",
                    "worker_id": "w1",
                    "task": {"region": "A市", "task_id": "task_a"},
                    "claimed_at": "2026-01-01T00:00:00+00:00",
                }
            }
        }
        actions = cleanup_worker_active_claims_unlocked(todo, state, "w1")
        assert len(actions) == 1
        assert actions[0]["action"] == "released"
