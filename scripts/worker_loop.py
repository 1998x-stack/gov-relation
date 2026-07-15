#!/usr/bin/env python3
"""Claim TODO items in a loop for an OpenCode worker."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gov_relation.queue import canonical_artifacts_ready, claim_next, set_claim_status
from gov_relation.slugs import artifact_paths


def log(message: str) -> None:
    ts = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    print(f"[{ts}] {message}", flush=True)


def task_commit_paths(task: dict) -> list[str]:
    paths = artifact_paths(task["region"])
    result = [
        paths["build_script"],
        paths["db_output"],
        paths["gexf_output"],
        "data/TODO.json",
        "report/open_gaps.md",
    ]
    region = task["region"]
    parent_city = task.get("parent_city") or ""
    province = task.get("province") or ""
    for directory, patterns in {
        Path("report"): [f"*{region}*", f"*{parent_city}*"] if parent_city else [f"*{region}*"],
        Path("data/persons"): [f"*{region}*", f"*{parent_city}*", f"*{province}*"],
        Path("docs/assets/data"): ["*.json"],
    }.items():
        if not directory.exists():
            continue
        for pattern in patterns:
            result.extend(str(path) for path in directory.glob(pattern) if path.is_file())
    return sorted(set(path for path in result if Path(path).exists()))


def git_commit_task(task: dict) -> bool:
    task_id = task["task_id"]
    paths = task_commit_paths(task)
    if not paths:
        log(f"GIT no task paths exist to commit for {task_id}")
        return True

    add = subprocess.run(["git", "add", *paths], text=True, capture_output=True, check=False)
    if add.returncode != 0:
        log(f"GIT add failed: {add.stderr.strip()}")
        return False

    status = subprocess.run(["git", "diff", "--cached", "--quiet"], check=False)
    if status.returncode == 0:
        log(f"GIT no staged changes to commit for {task_id}")
        return True

    message = f"Complete gov relation task {task_id}"
    commit = subprocess.run(["git", "commit", "-m", message], text=True, capture_output=True, check=False)
    if commit.returncode != 0:
        log(f"GIT commit failed: {commit.stderr.strip() or commit.stdout.strip()}")
        return False
    log(f"GIT committed task={task_id}: {message}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker-id", required=True)
    parser.add_argument("--model-intent", default="standard", choices=["standard", "iagent"], help="queue label: standard or iagent")
    parser.add_argument("--max-tasks", type=int, default=0, help="0 means loop until no task remains")
    parser.add_argument("--execute", action="store_true", help="run opencode after each claim")
    parser.add_argument("--opencode-bin", default="opencode")
    parser.add_argument("--opencode-agent", default="build", help="OpenCode --agent value")
    parser.add_argument("--opencode-model", default="agent-loop/standard", help="OpenCode provider/model value")
    parser.add_argument("--auto-done", action="store_true", help="mark done if opencode exits 0; use only if the prompt performs validation")
    parser.add_argument("--git-commit", action="store_true", help="commit repository changes after a task is marked done")
    parser.add_argument("--sleep-seconds", type=int, default=30, help="sleep between tasks when looping")
    args = parser.parse_args()

    completed = 0
    while True:
        if args.max_tasks and completed >= args.max_tasks:
            return 0
        claim = claim_next(
            args.worker_id,
            args.model_intent,
            opencode_agent=args.opencode_agent,
            opencode_model=args.opencode_model,
        )
        if claim is None:
            log("NO_TASKS_AVAILABLE")
            return 0
        task_id = claim["task"]["task_id"]
        prompt_path = claim["prompt_path"]
        log(f"CLAIMED {task_id} prompt={prompt_path}")

        if not args.execute:
            log(f"Run: {args.opencode_bin} run --agent {args.opencode_agent} --model {args.opencode_model} '<prompt from {prompt_path}>'")
            return 0

        log(f"START opencode task={task_id}")
        prompt_text = Path(prompt_path).read_text(encoding="utf-8")
        command = [args.opencode_bin, "run", "--agent", args.opencode_agent, "--model", args.opencode_model]
        command.append(prompt_text)
        result = subprocess.run(command, check=False)
        log(f"END opencode task={task_id} exit={result.returncode}")
        if result.returncode == 0 and args.auto_done:
            ready, missing = canonical_artifacts_ready(claim["task"])
            if not ready:
                set_claim_status(task_id, args.worker_id, "failed", f"missing canonical artifacts: {', '.join(missing)}")
                log(f"FAILED {task_id} missing canonical artifacts: {', '.join(missing)}")
                return 1
            set_claim_status(task_id, args.worker_id, "done")
            log(f"DONE {task_id}")
            if args.git_commit and not git_commit_task(claim["task"]):
                return 1
            completed += 1
            if args.sleep_seconds > 0:
                time.sleep(args.sleep_seconds)
            continue
        if result.returncode == 0 and not args.auto_done:
            log(f"COMPLETED {task_id}; waiting for manual done/release because --auto-done is disabled")
            return 0
        if result.returncode != 0:
            set_claim_status(task_id, args.worker_id, "failed", f"opencode exit {result.returncode}")
            log(f"FAILED {task_id} opencode exit {result.returncode}")
            return result.returncode
        completed += 1
        if args.sleep_seconds > 0:
            time.sleep(args.sleep_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
