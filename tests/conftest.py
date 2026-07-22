"""Shared fixtures and helpers for gov_relation tests."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Generator

import pytest


@pytest.fixture
def tmp_repo(tmp_path: Path) -> Path:
    """Create a temporary repo-like directory structure."""
    (tmp_path / "data" / "database").mkdir(parents=True)
    (tmp_path / "data" / "graph").mkdir(parents=True)
    (tmp_path / "data" / "json").mkdir(parents=True)
    (tmp_path / "data" / "persons").mkdir(parents=True)
    (tmp_path / "data" / "tmp").mkdir(parents=True)
    (tmp_path / "logs" / "dispatch").mkdir(parents=True)
    (tmp_path / "report").mkdir()
    (tmp_path / "docs").mkdir()
    (tmp_path / "scripts" / "build").mkdir(parents=True)
    return tmp_path


@pytest.fixture
def sample_todo() -> dict[str, Any]:
    """A minimal TODO.json structure."""
    return {
        "provinces": [
            {
                "province": "江西省",
                "tasks": [
                    {
                        "id": "jiangxi_province",
                        "region": "江西省",
                        "level": "province",
                        "done": True,
                        "targets": [{"role": "省委书记"}, {"role": "省长"}],
                        "sub_tasks": [
                            {
                                "id": "jiangxi_nanchang",
                                "region": "南昌市",
                                "level": "prefecture",
                                "done": False,
                                "targets": [{"role": "市委书记"}, {"role": "市长"}],
                            },
                        ],
                    },
                ],
            },
            {
                "province": "安徽省",
                "tasks": [
                    {
                        "id": "anhui_province",
                        "region": "安徽省",
                        "level": "province",
                        "done": False,
                        "targets": [{"role": "省委书记"}],
                    },
                ],
            },
        ],
    }


@pytest.fixture
def sample_todo_no_subtasks() -> dict[str, Any]:
    """TODO.json without subtasks."""
    return {
        "provinces": [
            {
                "province": "测试省",
                "tasks": [
                    {"id": "test_city", "region": "测试市", "level": "prefecture", "done": False, "targets": []},
                ],
            },
        ],
    }
