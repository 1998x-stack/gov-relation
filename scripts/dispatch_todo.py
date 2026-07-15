#!/usr/bin/env python3
"""Generate an Opencode dispatch prompt for a TODO item."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gov_relation.dispatch import build_dispatch_plan
from gov_relation.todo import find_item_by_id, find_next, load_todo


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--next", action="store_true", help="dispatch the next unfinished TODO item")
    group.add_argument("--task-id", help="dispatch a specific TODO task id")
    parser.add_argument("--model", default="standard", choices=["standard", "iagent"], help="model intent for generated prompt")
    parser.add_argument("--prompt-out", help="write prompt to this file")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    todo = load_todo()
    item = find_next(todo) if args.next else find_item_by_id(todo, args.task_id)
    if item is None:
        print("No matching TODO item found", file=sys.stderr)
        return 1

    plan = build_dispatch_plan(item, model=args.model)
    if args.prompt_out:
        out = Path(args.prompt_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(plan.prompt, encoding="utf-8")
        print(f"Wrote prompt: {out}")
    else:
        print(plan.prompt)
    print("Suggested command:")
    print(f"  {plan.suggested_command}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

