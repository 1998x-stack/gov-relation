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


def _task_done_task_id(task: Task) -> str:
    """Return a unique-ish key for matching done/set_claim_status calls."""
    return task.get("id", "")


def _task_done_context(task: Task, province_name: str, parent_city: str) -> tuple[str, str, str]:
    """Return (task_id, province, parent_city) for disambiguation."""
    return (task.get("id", ""), province_name, parent_city)


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


def find_task(todo: TodoData, task_id: str, province: str = "", parent_city: str = "") -> tuple[Province | None, Task | None]:
    """Find a task by id, optionally disambiguating by province + parent_city.

    When multiple tasks share the same id (e.g. 石家庄市桥西区 vs 张家口市桥西区),
    pass province and parent_city to find the correct one. Without disambiguation,
    the *first* match is returned (backward-compatible).
    """
    for prov in todo["provinces"]:
        for task in prov.get("tasks", []):
            if task.get("id") == task_id:
                if province and prov["province"] != province:
                    continue
                if parent_city:
                    task_parent = task.get("parent_city", "")
                    if task_parent != parent_city:
                        continue
                return prov, task
            for subtask in task.get("sub_tasks", []):
                if subtask.get("id") == task_id:
                    if province and prov["province"] != province:
                        continue
                    if parent_city and task.get("region") != parent_city:
                        continue
                    return prov, subtask
    return None, None


def mark_done(todo: TodoData, task_id: str, province: str = "", parent_city: str = "") -> bool:
    _, task = find_task(todo, task_id, province=province, parent_city=parent_city)
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


def find_item_by_id(todo: TodoData, task_id: str, province: str = "", parent_city: str = "") -> TodoItem | None:
    for item in iter_items(todo):
        if item.item.get("id") == task_id:
            if province and item.province_name != province:
                continue
            if parent_city and item.parent_city != parent_city:
                continue
            return item
    return None
