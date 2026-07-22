#!/usr/bin/env python3
"""
Print build artifact metadata for a task in data/TODO.json.

Usage:
  python3 generate_build_template.py <task_id>
"""

from __future__ import annotations

import sys

from gov_relation.slugs import artifact_paths
from gov_relation.todo import find_task, load_todo


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print("Usage: generate_build_template.py <task_id>")
        return 1

    task_id = argv[0]
    todo = load_todo()
    prov, item = find_task(todo, task_id)

    if item is None or prov is None:
        print(f"Task '{task_id}' not found")
        return 1

    region = item["region"]
    targets = item["targets"]
    role_names = [target["role"] for target in targets]
    paths = artifact_paths(region)

    print(f"--- Investigation Plan for {region} ({prov['province']}) ---")
    print(f"task_id:       {task_id}")
    print(f"region:        {region}")
    print(f"level:         {item['level']}")
    if item.get("parent_city"):
        print(f"parent_city:   {item['parent_city']}")
    print(f"province:      {prov['province']}")
    print(f"targets:       {' & '.join(role_names)}")
    print(f"build_script:  {paths['build_script']}")
    print(f"db_output:     {paths['db_output']}")
    print(f"gexf_output:   {paths['gexf_output']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

