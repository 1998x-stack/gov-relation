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

from gov_relation.log import get_logger, init_logging
from gov_relation.queue import canonical_artifacts_ready, claim_next, set_claim_status
from gov_relation.slugs import artifact_paths

logger = get_logger(__name__)


def task_commit_paths(task: dict, claimed_at: str = "") -> list[str]:
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
    since = None
    if claimed_at:
        try:
            since = datetime.fromisoformat(claimed_at).timestamp()
        except ValueError:
            since = None
    for directory, patterns in {
        Path("report"): [f"*{region}*", f"*{parent_city}*"] if parent_city else [f"*{region}*"],
        Path("data/persons"): [f"*{region}*", f"*{parent_city}*"] if parent_city else [f"*{region}*", f"*{province}*"],
        Path("docs/assets/data"): ["*.json"],
    }.items():
        if not directory.exists():
            continue
        for pattern in patterns:
            for path in directory.glob(pattern):
                if not path.is_file():
                    continue
                if since is not None and path.stat().st_mtime + 1 < since:
                    continue
                result.append(str(path))
    return sorted(set(path for path in result if Path(path).exists()))


def git_commit_task(task: dict, claimed_at: str = "") -> bool:
    task_id = task["task_id"]
    paths = task_commit_paths(task, claimed_at=claimed_at)
    if not paths:
        logger.info("GIT no task paths exist to commit for %s", task_id)
        return True

    add = subprocess.run(["git", "add", *paths], text=True, capture_output=True, check=False)
    if add.returncode != 0:
        logger.info("GIT add failed: %s", add.stderr.strip())
        return False

    status = subprocess.run(["git", "diff", "--cached", "--quiet"], check=False)
    if status.returncode == 0:
        logger.info("GIT no staged changes to commit for %s", task_id)
        return True

    message = f"Complete gov relation task {task_id}"
    commit = subprocess.run(["git", "commit", "-m", message], text=True, capture_output=True, check=False)
    if commit.returncode != 0:
        logger.info("GIT commit failed: %s", commit.stderr.strip() or commit.stdout.strip())
        return False
    logger.info("GIT committed task=%s: %s", task_id, message)
    return True


def main() -> int:
    init_logging()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker-id", required=True)
    parser.add_argument("--model-intent", default="standard", choices=["standard", "iagent"], help="queue label: standard or iagent")
    parser.add_argument("--max-tasks", type=int, default=0, help="0 means loop until no task remains")
    parser.add_argument("--execute", action="store_true", help="run opencode after each claim")
    parser.add_argument("--opencode-bin", default="opencode")
    parser.add_argument("--opencode-agent", default="", help="OpenCode --agent value; omit to use OpenCode's default primary agent")
    parser.add_argument("--opencode-model", default="agent-loop/standard", help="OpenCode provider/model value")
    parser.add_argument("--opencode-auto", action="store_true", help="pass --auto to OpenCode")
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
            logger.info("NO_TASKS_AVAILABLE")
            return 0
        task_id = claim["task"]["task_id"]
        prompt_path = claim["prompt_path"]
        logger.info("CLAIMED %s prompt=%s", task_id, prompt_path)

        if not args.execute:
            agent_arg = f" --agent {args.opencode_agent}" if args.opencode_agent else ""
            logger.info("Run: %s run%s --model %s '<prompt from %s>'", args.opencode_bin, agent_arg, args.opencode_model, prompt_path)
            return 0

        logger.info("START opencode task=%s", task_id)
        prompt_text = Path(prompt_path).read_text(encoding="utf-8")
        command = [args.opencode_bin, "run", "--model", args.opencode_model]
        if args.opencode_agent:
            command.extend(["--agent", args.opencode_agent])
        if args.opencode_auto:
            command.append("--auto")
        command.append(prompt_text)
        result = subprocess.run(command, check=False)
        logger.info("END opencode task=%s exit=%s", task_id, result.returncode)
        if result.returncode == 0 and args.auto_done:
            ready, missing = canonical_artifacts_ready(claim["task"])
            if not ready:
                set_claim_status(task_id, args.worker_id, "failed", f"missing canonical artifacts: {', '.join(missing)}")
                logger.info("FAILED %s missing canonical artifacts: %s", task_id, ', '.join(missing))
                completed += 1
                if args.sleep_seconds > 0:
                    time.sleep(args.sleep_seconds)
                continue
            set_claim_status(task_id, args.worker_id, "done")
            logger.info("DONE %s", task_id)
            if args.git_commit and not git_commit_task(claim["task"], claimed_at=claim.get("claimed_at", "")):
                return 1
            completed += 1
            if args.sleep_seconds > 0:
                time.sleep(args.sleep_seconds)
            continue
        if result.returncode == 0 and not args.auto_done:
            logger.info("COMPLETED %s; waiting for manual done/release because --auto-done is disabled", task_id)
            return 0
        if result.returncode != 0:
            set_claim_status(task_id, args.worker_id, "failed", f"opencode exit {result.returncode}")
            logger.info("FAILED %s opencode exit %s", task_id, result.returncode)
            completed += 1
            if args.sleep_seconds > 0:
                time.sleep(args.sleep_seconds)
            continue
        completed += 1
        if args.sleep_seconds > 0:
            time.sleep(args.sleep_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
