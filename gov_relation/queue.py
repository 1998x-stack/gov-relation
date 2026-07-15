"""Concurrent TODO queue state for multiple OpenCode workers."""

from __future__ import annotations

import json
import os
import shutil
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .dispatch import build_dispatch_plan
from .paths import DISPATCH_LOCK_DIR, DISPATCH_STATE_PATH, REPO_ROOT
from .slugs import artifact_paths
from .todo import TodoItem, find_item_by_id, iter_items, item_summary, load_todo, mark_done, save_todo


LOCK_STALE_SECONDS = 10 * 60


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def safe_name(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in value)


@contextmanager
def queue_lock(timeout: float = 30.0, poll: float = 0.1, stale_after: float = LOCK_STALE_SECONDS):
    start = time.time()
    while True:
        try:
            os.mkdir(DISPATCH_LOCK_DIR)
            (DISPATCH_LOCK_DIR / "owner.json").write_text(
                json.dumps({"pid": os.getpid(), "created_at": now_iso()}, ensure_ascii=False),
                encoding="utf-8",
            )
            break
        except FileExistsError:
            try:
                age = time.time() - DISPATCH_LOCK_DIR.stat().st_mtime
            except FileNotFoundError:
                continue
            if age > stale_after:
                shutil.rmtree(DISPATCH_LOCK_DIR, ignore_errors=True)
                continue
            if time.time() - start > timeout:
                raise TimeoutError(f"timed out waiting for queue lock: {DISPATCH_LOCK_DIR}")
            time.sleep(poll)
    try:
        yield
    finally:
        try:
            shutil.rmtree(DISPATCH_LOCK_DIR)
        except FileNotFoundError:
            pass


def load_state() -> dict[str, Any]:
    if not DISPATCH_STATE_PATH.exists():
        return {"version": 1, "updated_at": now_iso(), "claims": {}}
    with DISPATCH_STATE_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def save_state(state: dict[str, Any]) -> None:
    state["updated_at"] = now_iso()
    DISPATCH_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = DISPATCH_STATE_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(DISPATCH_STATE_PATH)


def active_claim_ids(state: dict[str, Any]) -> set[str]:
    return {task_id for task_id, claim in state.get("claims", {}).items() if claim.get("status") == "active"}


def parse_iso(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return datetime.min.replace(tzinfo=timezone.utc)


def claim_sort_key(claim: dict[str, Any]) -> datetime:
    return parse_iso(claim.get("claimed_at") or claim.get("updated_at") or "")


def _canonical_artifacts_ready_unlocked(task: dict[str, Any]) -> tuple[bool, list[str]]:
    paths = artifact_paths(task["region"])
    required = [
        REPO_ROOT / paths["build_script"],
        REPO_ROOT / paths["db_output"],
        REPO_ROOT / paths["gexf_output"],
    ]
    missing = [str(path.relative_to(REPO_ROOT)) for path in required if not path.exists()]
    return not missing, missing


def _mark_claim_done_unlocked(todo: dict, claim: dict[str, Any], reason: str = "") -> None:
    task_id = claim["task"]["task_id"]
    claim["status"] = "done"
    claim["updated_at"] = now_iso()
    if reason:
        claim["reason"] = reason
    if not mark_done(todo, task_id):
        raise KeyError(f"task not found in TODO.json: {task_id}")


def cleanup_worker_active_claims_unlocked(todo: dict, state: dict[str, Any], worker_id: str) -> list[dict[str, str]]:
    """Clear impossible leftover active claims before a worker takes new work."""
    actions: list[dict[str, str]] = []
    for task_id, claim in state.get("claims", {}).items():
        if claim.get("status") != "active" or claim.get("worker_id") != worker_id:
            continue
        ready, missing = _canonical_artifacts_ready_unlocked(claim["task"])
        if ready:
            _mark_claim_done_unlocked(todo, claim, "auto-reconciled before worker reclaimed")
            actions.append({"task_id": task_id, "action": "done"})
        else:
            claim["status"] = "released"
            claim["updated_at"] = now_iso()
            claim["reason"] = f"released before worker reclaimed; missing: {', '.join(missing)}"
            actions.append({"task_id": task_id, "action": "released"})
    return actions


def find_next_claimable(todo: dict, state: dict[str, Any]) -> TodoItem | None:
    active = active_claim_ids(state)
    for item in iter_items(todo):
        task_id = item.item.get("id")
        if not task_id or item.item.get("done") or task_id in active:
            continue
        return item
    return None


def write_prompt(plan, worker_id: str, prompt_dir: Path) -> Path:
    prompt_dir.mkdir(parents=True, exist_ok=True)
    task_id = plan.task["task_id"]
    path = prompt_dir / f"{safe_name(task_id)}.{safe_name(worker_id)}.prompt.txt"
    path.write_text(plan.prompt, encoding="utf-8")
    return path


def claim_next(
    worker_id: str,
    model_intent: str = "iagent",
    prompt_dir: Path | None = None,
    opencode_agent: str = "",
    opencode_model: str = "iagent/standard",
) -> dict[str, Any] | None:
    prompt_dir = prompt_dir or (REPO_ROOT / "logs" / "dispatch")
    with queue_lock():
        todo = load_todo()
        state = load_state()
        cleanup_worker_active_claims_unlocked(todo, state, worker_id)
        item = find_next_claimable(todo, state)
        if item is None:
            save_todo(todo)
            save_state(state)
            return None
        plan = build_dispatch_plan(item, model_intent=model_intent)
        prompt_path = write_prompt(plan, worker_id, prompt_dir)
        task_id = plan.task["task_id"]
        previous = state.setdefault("claims", {}).get(task_id, {})
        claim = {
            "status": "active",
            "worker_id": worker_id,
            "model_intent": model_intent,
            "opencode_agent": opencode_agent,
            "opencode_model": opencode_model,
            "claimed_at": now_iso(),
            "updated_at": now_iso(),
            "attempts": int(previous.get("attempts", 0)) + 1,
            "prompt_path": str(prompt_path.relative_to(REPO_ROOT)),
            "task": plan.task,
        }
        state["claims"][task_id] = claim
        save_todo(todo)
        save_state(state)
        return claim


def set_claim_status(task_id: str, worker_id: str, status: str, reason: str = "") -> dict[str, Any]:
    if status not in {"active", "done", "failed", "released"}:
        raise ValueError(f"invalid claim status: {status}")
    with queue_lock():
        state = load_state()
        claim = state.setdefault("claims", {}).get(task_id)
        if claim is None:
            raise KeyError(f"task is not claimed: {task_id}")
        if worker_id and claim.get("worker_id") != worker_id:
            raise PermissionError(f"task {task_id} is claimed by {claim.get('worker_id')}, not {worker_id}")
        if claim.get("status") != "active" and status in {"done", "failed", "released"}:
            raise ValueError(f"task {task_id} is not active; current status is {claim.get('status')}")
        claim["status"] = status
        claim["updated_at"] = now_iso()
        if reason:
            claim["reason"] = reason
        state["claims"][task_id] = claim
        if status == "done":
            todo = load_todo()
            if not mark_done(todo, task_id):
                raise KeyError(f"task not found in TODO.json: {task_id}")
            save_todo(todo)
        save_state(state)
        return claim


def canonical_artifacts_ready(task: dict[str, Any]) -> tuple[bool, list[str]]:
    return _canonical_artifacts_ready_unlocked(task)


def claim_specific(
    task_id: str,
    worker_id: str,
    model_intent: str = "iagent",
    prompt_dir: Path | None = None,
    opencode_agent: str = "",
    opencode_model: str = "iagent/standard",
) -> dict[str, Any]:
    prompt_dir = prompt_dir or (REPO_ROOT / "logs" / "dispatch")
    with queue_lock():
        todo = load_todo()
        state = load_state()
        item = find_item_by_id(todo, task_id)
        if item is None:
            raise KeyError(f"task not found: {task_id}")
        if item.item.get("done"):
            raise ValueError(f"task already done: {task_id}")
        active = active_claim_ids(state)
        if task_id in active:
            raise ValueError(f"task already actively claimed: {task_id}")
        plan = build_dispatch_plan(item, model_intent=model_intent)
        prompt_path = write_prompt(plan, worker_id, prompt_dir)
        previous = state.setdefault("claims", {}).get(task_id, {})
        claim = {
            "status": "active",
            "worker_id": worker_id,
            "model_intent": model_intent,
            "opencode_agent": opencode_agent,
            "opencode_model": opencode_model,
            "claimed_at": now_iso(),
            "updated_at": now_iso(),
            "attempts": int(previous.get("attempts", 0)) + 1,
            "prompt_path": str(prompt_path.relative_to(REPO_ROOT)),
            "task": item_summary(item),
        }
        state["claims"][task_id] = claim
        save_state(state)
        return claim


def queue_status() -> dict[str, Any]:
    todo = load_todo()
    state = load_state()
    claims = state.get("claims", {})
    active = [claim for claim in claims.values() if claim.get("status") == "active"]
    done_claims = [claim for claim in claims.values() if claim.get("status") == "done"]
    failed = [claim for claim in claims.values() if claim.get("status") == "failed"]
    total = 0
    done = 0
    for item in iter_items(todo):
        total += 1
        if item.item.get("done"):
            done += 1
    return {
        "total": total,
        "done": done,
        "remaining": total - done,
        "active_claims": len(active),
        "done_claims": len(done_claims),
        "failed_claims": len(failed),
        "active": active,
        "failed": failed,
        "state_path": str(DISPATCH_STATE_PATH.relative_to(REPO_ROOT)),
    }


def reconcile_claims(
    *,
    done_ready: bool = True,
    release_superseded_workers: bool = True,
    release_active: bool = False,
    reason: str = "manual reconcile",
) -> list[dict[str, str]]:
    actions: list[dict[str, str]] = []
    with queue_lock():
        todo = load_todo()
        state = load_state()
        claims = state.setdefault("claims", {})

        if done_ready:
            for task_id, claim in claims.items():
                if claim.get("status") not in {"active", "failed", "released"}:
                    continue
                ready, _missing = _canonical_artifacts_ready_unlocked(claim["task"])
                if ready:
                    _mark_claim_done_unlocked(todo, claim, "auto-reconciled canonical artifacts")
                    actions.append({"task_id": task_id, "action": "done"})

        if release_superseded_workers:
            by_worker: dict[str, list[tuple[str, dict[str, Any]]]] = {}
            for task_id, claim in claims.items():
                if claim.get("status") == "active":
                    by_worker.setdefault(claim.get("worker_id", ""), []).append((task_id, claim))
            for worker_id, worker_claims in by_worker.items():
                if len(worker_claims) <= 1:
                    continue
                worker_claims.sort(key=lambda item: claim_sort_key(item[1]), reverse=True)
                for task_id, claim in worker_claims[1:]:
                    claim["status"] = "released"
                    claim["updated_at"] = now_iso()
                    claim["reason"] = f"released superseded active claim for {worker_id}"
                    actions.append({"task_id": task_id, "action": "released"})

        if release_active:
            for task_id, claim in claims.items():
                if claim.get("status") != "active":
                    continue
                claim["status"] = "released"
                claim["updated_at"] = now_iso()
                claim["reason"] = reason
                actions.append({"task_id": task_id, "action": "released"})

        save_todo(todo)
        save_state(state)
    return actions


def force_unlock() -> bool:
    if DISPATCH_LOCK_DIR.exists():
        shutil.rmtree(DISPATCH_LOCK_DIR, ignore_errors=True)
        return True
    return False
