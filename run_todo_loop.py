#!/usr/bin/env python3
"""
TODO Loop Runner - picks the next unfinished item from data/TODO.json.

Usage:
  python3 run_todo_loop.py [--mark-done TASK_ID]
  python3 run_todo_loop.py [--status]
  python3 run_todo_loop.py
"""

from __future__ import annotations

import sys

from gov_relation.todo import count_stats, find_next, load_todo, mark_done, province_stats, save_todo


def print_status(todo: dict) -> None:
    total, done = count_stats(todo)
    print("TODO.json status:")
    print(f"  Total items: {total}")
    print(f"  Finished:    {done}")
    print(f"  Remaining:   {total - done}")
    print(f"  Progress:    {done / max(total, 1) * 100:.1f}%")

    for province, p_total, p_done in province_stats(todo):
        if p_total > 0:
            print(f"  {province:20} {p_done:>4}/{p_total:<4} ({p_done / max(p_total, 1) * 100:.0f}%)")


def print_next(todo: dict) -> int:
    next_item = find_next(todo)
    if next_item is None:
        print("ALL DONE! No unfinished items remain.")
        return 0

    total, done = count_stats(todo)
    item = next_item.item
    targets = item["targets"]
    role_names = [target["role"] for target in targets]

    print(f"PROGRESS: {done}/{total} ({done / max(total, 1) * 100:.1f}%)")
    print("NEXT_ITEM_START")
    print(f"  task_id: {item['id']}")
    print(f"  province: {next_item.province_name}")
    if next_item.subtask:
        print(f"  parent_city: {next_item.parent_city}")
    print(f"  region: {item['region']}")
    print(f"  level: {item['level']}")
    print(f"  targets: {' & '.join(role_names)}")
    print(f"  description: 调研{item['region']}{item['level']}的{'和'.join(role_names)}履历及工作关系网络")
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    todo = load_todo()

    if argv:
        cmd = argv[0]
        if cmd == "--status":
            print_status(todo)
            return 0

        if cmd == "--mark-done" and len(argv) > 1:
            task_id = argv[1]
            if mark_done(todo, task_id):
                save_todo(todo)
                total, done = count_stats(todo)
                print(f"Marked '{task_id}' as done. Progress: {done}/{total} ({done / max(total, 1) * 100:.1f}%)")
                return 0
            print(f"Task '{task_id}' not found")
            return 1

    return print_next(todo)


if __name__ == "__main__":
    raise SystemExit(main())

