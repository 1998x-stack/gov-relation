from __future__ import annotations

import json
from pathlib import Path

import pytest

from gov_relation.province import (
    build_slug_province_map,
    detect_province,
)


class TestDetectProvince:
    def test_known_slugs(self) -> None:
        """Slugs that are exact matches in the map."""
        cache = {
            "周口市": "河南省",
            "固原市": "宁夏回族自治区",
            "甘肃省": "甘肃省",
        }
        assert detect_province("周口市", map_cache=cache) == "河南省"
        assert detect_province("固原市", map_cache=cache) == "宁夏回族自治区"
        assert detect_province("甘肃省", map_cache=cache) == "甘肃省"

    def test_unknown_slug_raises(self) -> None:
        cache = {"周口市": "河南省"}
        with pytest.raises(ValueError):
            detect_province("金星", map_cache=cache)


class TestBuildMapFromTodo:
    def test_from_todo_json(self, tmp_path: Path) -> None:
        todo = {
            "provinces": [
                {
                    "province": "江西省",
                    "tasks": [
                        {"id": "jiangxi_province", "region": "江西省", "level": "province"},
                        {
                            "id": "jiangxi_南昌市",
                            "region": "南昌市",
                            "level": "prefecture",
                            "sub_tasks": [
                                {"id": "jiangxi_东湖区", "region": "东湖区", "level": "district"},
                                {"id": "jiangxi_西湖区", "region": "西湖区", "level": "district"},
                            ],
                        },
                    ],
                },
                {
                    "province": "安徽省",
                    "tasks": [
                        {"id": "anhui_province", "region": "安徽省", "level": "province"},
                    ],
                },
            ],
        }
        todo_path = tmp_path / "TODO.json"
        with open(todo_path, "w") as f:
            json.dump(todo, f)

        mapping = build_slug_province_map(todo_path)
        # Top-level tasks
        assert mapping["南昌市"] == "江西省"
        assert mapping["安徽省"] == "安徽省"
        assert mapping["江西省"] == "江西省"
        # Sub-tasks (county/district level)
        assert mapping["东湖区"] == "江西省"
        assert mapping["西湖区"] == "江西省"