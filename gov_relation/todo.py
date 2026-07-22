"""Utilities for reading and updating data/TODO.json."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .log import get_logger
from .paths import TODO_PATH

logger = get_logger(__name__)

TodoData = dict[str, Any]
Task = dict[str, Any]
Province = dict[str, Any]


@dataclass(frozen=True)
class TodoItem:
    province_name: str
    task: Task
    subtask: Task | None = None

    @property
    def item(self) -> Task:
        return self.subtask or self.task

    @property
    def parent_city(self) -> str:
        if self.subtask:
            return self.task.get("region", "")
        return self.item.get("parent_city", "")


def load_todo(path: Path = TODO_PATH) -> TodoData:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def save_todo(todo: TodoData, path: Path = TODO_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(todo, f, ensure_ascii=False, indent=2)


def iter_items(todo: TodoData) -> list[TodoItem]:
    items: list[TodoItem] = []
    for prov in todo["provinces"]:
        province_name = prov["province"]
        for task in prov.get("tasks", []):
            items.append(TodoItem(province_name, task, None))
            for subtask in task.get("sub_tasks", []):
                items.append(TodoItem(province_name, task, subtask))
    return items


def find_next(todo: TodoData) -> TodoItem | None:
    """Find the next unfinished item, checking subtasks before parent tasks."""
    for prov in todo["provinces"]:
        province_name = prov["province"]
        for task in prov.get("tasks", []):
            for subtask in task.get("sub_tasks", []):
                if not subtask.get("done"):
                    return TodoItem(province_name, task, subtask)
            if not task.get("done"):
                return TodoItem(province_name, task, None)
    return None


def count_stats(todo: TodoData) -> tuple[int, int]:
    total = 0
    done = 0
    for item in iter_items(todo):
        total += 1
        if item.item.get("done"):
            done += 1
    return total, done


def province_stats(todo: TodoData) -> list[tuple[str, int, int]]:
    rows: list[tuple[str, int, int]] = []
    for prov in todo["provinces"]:
        p_total = 0
        p_done = 0
        for task in prov.get("tasks", []):
            p_total += 1
            if task.get("done"):
                p_done += 1
            for subtask in task.get("sub_tasks", []):
                p_total += 1
                if subtask.get("done"):
                    p_done += 1
        rows.append((prov["province"], p_total, p_done))
    return rows


def find_task(todo: TodoData, task_id: str) -> tuple[Province | None, Task | None]:
    for prov in todo["provinces"]:
        for task in prov.get("tasks", []):
            if task.get("id") == task_id:
                return prov, task
            for subtask in task.get("sub_tasks", []):
                if subtask.get("id") == task_id:
                    return prov, subtask
    return None, None


def mark_done(todo: TodoData, task_id: str) -> bool:
    _, task = find_task(todo, task_id)
    if task is None:
        return False
    task["done"] = True
    return True


def item_summary(item: TodoItem) -> dict[str, Any]:
    task = item.item
    return {
        "task_id": task.get("id", ""),
        "province": item.province_name,
        "parent_city": item.parent_city,
        "region": task.get("region", ""),
        "level": task.get("level", ""),
        "targets": task.get("targets", []),
        "target_roles": [target.get("role", "") for target in task.get("targets", [])],
    }


def find_item_by_id(todo: TodoData, task_id: str) -> TodoItem | None:
    for item in iter_items(todo):
        if item.item.get("id") == task_id:
            return item
    return None
