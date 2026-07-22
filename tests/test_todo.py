"""Tests for gov_relation/todo.py."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from gov_relation.todo import (
    TodoItem,
    count_stats,
    find_item_by_id,
    find_next,
    find_task,
    iter_items,
    item_summary,
    load_todo,
    mark_done,
    province_stats,
    save_todo,
)


class TestIterItems:
    def test_returns_all_tasks_and_subtasks(self, sample_todo: dict[str, Any]) -> None:
        items = iter_items(sample_todo)
        assert len(items) == 3  # jiangxi_province + nanchang + anhui_province

    def test_subtask_has_parent_task(self, sample_todo: dict[str, Any]) -> None:
        items = iter_items(sample_todo)
        nanchangs = [i for i in items if i.item.get("id") == "jiangxi_nanchang"]
        assert len(nanchangs) == 1
        assert nanchangs[0].task["region"] == "江西省"

    def test_parent_city_comes_from_task_region_for_subtask(self, sample_todo: dict[str, Any]) -> None:
        items = iter_items(sample_todo)
        nanchang = next(i for i in items if i.item.get("id") == "jiangxi_nanchang")
        # When subtask has no explicit parent_city, it falls back to the parent task's region
        assert nanchang.parent_city == "江西省"

    def test_parent_city_empty_for_top_level_task(self, sample_todo: dict[str, Any]) -> None:
        items = iter_items(sample_todo)
        anhui = next(i for i in items if i.item.get("id") == "anhui_province")
        assert anhui.parent_city == ""


class TestFindNext:
    def test_returns_first_undone_subtask(self, sample_todo: dict[str, Any]) -> None:
        item = find_next(sample_todo)
        assert item is not None
        assert item.item.get("id") == "jiangxi_nanchang"

    def test_skips_done_tasks(self, sample_todo: dict[str, Any]) -> None:
        # jiangxi_province is done, provinces subtask is not done
        item = find_next(sample_todo)
        assert item is not None
        assert item.item.get("done") is False

    def test_returns_none_when_all_done(self) -> None:
        todo = {
            "provinces": [
                {
                    "province": "测试省",
                    "tasks": [{"id": "done_task", "region": "测试市", "level": "prefecture", "done": True, "targets": []}],
                },
            ],
        }
        assert find_next(todo) is None

    def test_empty_provinces(self) -> None:
        assert find_next({"provinces": []}) is None


class TestMarkDone:
    def test_marks_subtask_done(self, sample_todo: dict[str, Any]) -> None:
        assert mark_done(sample_todo, "jiangxi_nanchang") is True
        items = iter_items(sample_todo)
        nanchang = next(i for i in items if i.item.get("id") == "jiangxi_nanchang")
        assert nanchang.item.get("done") is True

    def test_marks_top_task_done(self, sample_todo: dict[str, Any]) -> None:
        assert mark_done(sample_todo, "anhui_province") is True
        items = iter_items(sample_todo)
        anhui = next(i for i in items if i.item.get("id") == "anhui_province")
        assert anhui.item.get("done") is True

    def test_unknown_id_returns_false(self, sample_todo: dict[str, Any]) -> None:
        assert mark_done(sample_todo, "nonexistent") is False


class TestCountStats:
    def test_counts_total_and_done(self, sample_todo: dict[str, Any]) -> None:
        total, done = count_stats(sample_todo)
        assert total == 3
        assert done == 1  # only jiangxi_province

    def test_empty(self) -> None:
        total, done = count_stats({"provinces": []})
        assert total == 0
        assert done == 0


class TestFindItemById:
    def test_finds_subtask(self, sample_todo: dict[str, Any]) -> None:
        item = find_item_by_id(sample_todo, "jiangxi_nanchang")
        assert item is not None
        assert item.item.get("region") == "南昌市"

    def test_finds_top_task(self, sample_todo: dict[str, Any]) -> None:
        item = find_item_by_id(sample_todo, "anhui_province")
        assert item is not None
        assert item.item.get("region") == "安徽省"

    def test_unknown_id_returns_none(self, sample_todo: dict[str, Any]) -> None:
        assert find_item_by_id(sample_todo, "missing") is None


class TestFindTask:
    def test_finds_existing_task(self, sample_todo: dict[str, Any]) -> None:
        prov, task = find_task(sample_todo, "anhui_province")
        assert prov is not None
        assert prov["province"] == "安徽省"
        assert task is not None
        assert task["region"] == "安徽省"

    def test_returns_none_for_missing(self, sample_todo: dict[str, Any]) -> None:
        prov, task = find_task(sample_todo, "missing")
        assert prov is None
        assert task is None


class TestItemSummary:
    def test_summary_includes_all_fields(self, sample_todo: dict[str, Any]) -> None:
        items = iter_items(sample_todo)
        nanchang = next(i for i in items if i.item.get("id") == "jiangxi_nanchang")
        summary = item_summary(nanchang)
        assert summary["task_id"] == "jiangxi_nanchang"
        assert summary["province"] == "江西省"
        assert summary["region"] == "南昌市"
        assert summary["level"] == "prefecture"
        assert summary["target_roles"] == ["市委书记", "市长"]


class TestProvinceStats:
    def test_returns_stats_per_province(self, sample_todo: dict[str, Any]) -> None:
        stats = province_stats(sample_todo)
        assert len(stats) == 2
        jx = next(s for s in stats if s[0] == "江西省")
        assert jx[1] == 2  # total
        assert jx[2] == 1  # done


class TestLoadSaveTodo:
    def test_roundtrip(self, tmp_path: Path) -> None:
        path = tmp_path / "TODO.json"
        original = {"provinces": [{"province": "测试省", "tasks": []}]}
        save_todo(original, path)
        loaded = load_todo(path)
        assert loaded == original

    def test_save_creates_parent(self, tmp_path: Path) -> None:
        path = tmp_path / "sub" / "TODO.json"
        data = {"provinces": []}
        save_todo(data, path)
        assert path.exists()
