#!/usr/bin/env python3
"""Concurrent TODO queue for multiple OpenCode workers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gov_relation.queue import canonical_artifacts_ready, claim_next, claim_specific, force_unlock, queue_status, reconcile_claims, set_claim_status


def print_claim(claim: dict) -> None:
    task = claim["task"]
    print(f"CLAIMED {task['task_id']}")
    print(f"  worker:      {claim['worker_id']}")
    print(f"  intent:      {claim.get('model_intent', claim.get('model', ''))}")
    print(f"  oc_agent:    {claim.get('opencode_agent', '')}")
    print(f"  oc_model:    {claim.get('opencode_model', '')}")
    print(f"  province:    {task['province']}")
    if task.get("parent_city"):
        print(f"  parent_city: {task['parent_city']}")
    print(f"  region:      {task['region']}")
    print(f"  level:       {task['level']}")
    print(f"  targets:     {' & '.join(task['target_roles'])}")
    print(f"  prompt:      {claim['prompt_path']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    claim = sub.add_parser("claim", help="claim the next available TODO item")
    claim.add_argument("--worker-id", required=True)
    claim.add_argument("--model-intent", "--model", dest="model_intent", default="iagent", choices=["standard", "iagent"])
    claim.add_argument("--opencode-agent", default="")
    claim.add_argument("--opencode-model", default="iagent/standard")
    claim.add_argument("--task-id", help="claim a specific task instead of next")
    claim.add_argument("--json", action="store_true")

    done = sub.add_parser("done", help="mark a claimed task done and update TODO.json")
    done.add_argument("--task-id", required=True)
    done.add_argument("--worker-id", required=True)
    done.add_argument("--skip-artifact-check", action="store_true", help="mark done even if canonical build/db/gexf files are missing")

    fail = sub.add_parser("fail", help="mark a claimed task failed")
    fail.add_argument("--task-id", required=True)
    fail.add_argument("--worker-id", required=True)
    fail.add_argument("--reason", default="")

    release = sub.add_parser("release", help="release a claim without marking done")
    release.add_argument("--task-id", required=True)
    release.add_argument("--worker-id", required=True)
    release.add_argument("--reason", default="")

    status = sub.add_parser("status", help="print queue status")
    status.add_argument("--json", action="store_true")

    unlock = sub.add_parser("unlock", help="remove a stale dispatch lock")
    unlock.add_argument("--force", action="store_true", required=True)

    reconcile = sub.add_parser("reconcile", help="repair queue state from artifacts and stale claims")
    reconcile.add_argument("--done-ready", action="store_true", help="mark claims done when canonical artifacts exist")
    reconcile.add_argument("--release-superseded-workers", action="store_true", help="release older active claims when one worker owns multiple")
    reconcile.add_argument("--release-active", action="store_true", help="release all remaining active claims; use after stopping workers")
    reconcile.add_argument("--reason", default="manual reconcile")
    reconcile.add_argument("--json", action="store_true")

    args = parser.parse_args()

    if args.cmd == "claim":
        claim_data = (
            claim_specific(args.task_id, args.worker_id, args.model_intent, opencode_agent=args.opencode_agent, opencode_model=args.opencode_model)
            if args.task_id
            else claim_next(args.worker_id, args.model_intent, opencode_agent=args.opencode_agent, opencode_model=args.opencode_model)
        )
        if claim_data is None:
            print("NO_TASKS_AVAILABLE")
            return 2
        if args.json:
            print(json.dumps(claim_data, ensure_ascii=False, indent=2))
        else:
            print_claim(claim_data)
        return 0

    if args.cmd == "done":
        status_data = queue_status()
        claim = next((item for item in status_data["active"] if item["task"]["task_id"] == args.task_id), None)
        if claim is None:
            print(f"Task is not actively claimed: {args.task_id}", file=sys.stderr)
            return 1
        ready, missing = canonical_artifacts_ready(claim["task"])
        if not ready and not args.skip_artifact_check:
            print("Refusing to mark done; missing canonical artifacts:", file=sys.stderr)
            for path in missing:
                print(f"  - {path}", file=sys.stderr)
            print("Use --skip-artifact-check only for intentional exceptions.", file=sys.stderr)
            return 1
        set_claim_status(args.task_id, args.worker_id, "done")
        print(f"DONE {args.task_id}")
        return 0

    if args.cmd == "fail":
        set_claim_status(args.task_id, args.worker_id, "failed", args.reason)
        print(f"FAILED {args.task_id}")
        return 0

    if args.cmd == "release":
        set_claim_status(args.task_id, args.worker_id, "released", args.reason)
        print(f"RELEASED {args.task_id}")
        return 0

    if args.cmd == "status":
        data = queue_status()
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(f"TODO: {data['done']}/{data['total']} done, {data['remaining']} remaining")
            print(f"Claims: {data['active_claims']} active, {data['done_claims']} done, {data['failed_claims']} failed")
            for claim in data["active"]:
                task = claim["task"]
                print(f"  ACTIVE {task['task_id']} worker={claim['worker_id']} prompt={claim['prompt_path']}")
        return 0

    if args.cmd == "unlock":
        removed = force_unlock()
        print("UNLOCKED" if removed else "NO_LOCK")
        return 0

    if args.cmd == "reconcile":
        actions = reconcile_claims(
            done_ready=args.done_ready,
            release_superseded_workers=args.release_superseded_workers,
            release_active=args.release_active,
            reason=args.reason,
        )
        if args.json:
            print(json.dumps(actions, ensure_ascii=False, indent=2))
        else:
            for action in actions:
                print(f"{action['action'].upper()} {action['task_id']}")
            if not actions:
                print("NO_CHANGES")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
