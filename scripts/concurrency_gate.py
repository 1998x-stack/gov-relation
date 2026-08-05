#!/usr/bin/env python3
"""File-based concurrency gate: limits active agent count across worker processes.

Each worker acquires a lease file before starting opencode, and releases it
when done. Workers that cannot acquire a lease spin-wait and poll.

Usage:
    from concurrency_gate import acquire
    with acquire(worker_id="worker-1", max_active=2):
        subprocess.run(["opencode", ...])
"""

from __future__ import annotations

import json
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

REPO_ROOT = Path(__file__).resolve().parents[1]
GATE_DIR = REPO_ROOT / "data" / ".concurrency_gate"
LEASE_TIMEOUT_SECONDS = 4 * 60 * 60  # 4h — lease expires if worker crashes or stalls too long
POLL_INTERVAL = 5.0


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _lease_path(worker_id: str) -> Path:
    return GATE_DIR / f"{worker_id}.lease.json"


def _active_leases(max_age: float = LEASE_TIMEOUT_SECONDS) -> list[dict[str, Any]]:
    """Return list of active (non-stale) lease records."""
    if not GATE_DIR.exists():
        return []
    leases: list[dict[str, Any]] = []
    now = time.time()
    for f in sorted(GATE_DIR.iterdir()):
        if not f.name.endswith(".lease.json"):
            continue
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            try:
                f.unlink()
            except OSError:
                pass
            continue
        age = now - data.get("acquired_at", 0)
        if age > max_age:
            try:
                f.unlink()
            except OSError:
                pass
            continue
        leases.append(data)
    return leases


def release_lease(worker_id: str) -> None:
    path = _lease_path(worker_id)
    try:
        path.unlink()
    except OSError:
        pass


@contextmanager
def acquire(worker_id: str, max_active: int = 2, timeout: float = 0.0) -> Iterator[bool]:
    """Context manager: wait until <= max_active leases, then acquire.

    Yields True once lease is acquired. Blocks indefinitely (timeout=0) so
    workers keep waiting for a slot rather than dying mid-pipeline; pass an
    explicit positive timeout only when bounded waits are intended.
    """
    start = time.time()
    GATE_DIR.mkdir(parents=True, exist_ok=True)
    our_path = _lease_path(worker_id)

    while True:
        active = _active_leases()
        other_count = sum(1 for l in active if l.get("worker_id") != worker_id)
        if other_count < max_active:
            break
        elapsed = time.time() - start
        if timeout > 0 and elapsed > timeout:
            raise TimeoutError(
                f"worker={worker_id} waited {elapsed:.0f}s for concurrency slot "
                f"(max_active={max_active}, active_others={other_count})"
            )
        time.sleep(POLL_INTERVAL)

    # Acquire: write lease
    now_ts = time.time()
    data: dict[str, Any] = {
        "worker_id": worker_id,
        "acquired_at": now_ts,
        "expires": now_ts + LEASE_TIMEOUT_SECONDS,
        "since": now_iso(),
    }
    our_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    try:
        yield True
    finally:
        release_lease(worker_id)


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2 and sys.argv[1] == "--status":
        leases = _active_leases()
        print(f"Concurrency gate: {len(leases)} active lease(s)")
        for l in leases:
            print(f"  {l['worker_id']} since {l['since']}")
    elif len(sys.argv) >= 2 and sys.argv[1] == "--release":
        release_lease(sys.argv[2])
        print(f"Released lease for {sys.argv[2]}")
    else:
        print(f"Usage: {sys.argv[0]} --status|--release <worker-id>")
