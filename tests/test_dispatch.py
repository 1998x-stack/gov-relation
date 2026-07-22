"""Tests for gov_relation/dispatch.py."""

from __future__ import annotations

from gov_relation.dispatch import build_dispatch_plan, build_dispatch_prompt
from gov_relation.todo import TodoItem


class TestBuildDispatchPrompt:
    def test_includes_task_id(self) -> None:
        item = TodoItem(province_name="测试省", task={"id": "test_city", "region": "测试市", "level": "prefecture", "targets": [{"role": "市长"}]})
        prompt = build_dispatch_prompt(item)
        assert "test_city" in prompt

    def test_includes_region(self) -> None:
        item = TodoItem(province_name="测试省", task={"id": "x", "region": "南昌市", "level": "prefecture", "targets": [{"role": "市长"}]})
        prompt = build_dispatch_prompt(item)
        assert "南昌市" in prompt

    def test_includes_province(self) -> None:
        item = TodoItem(province_name="江西省", task={"id": "x", "region": "南昌市", "level": "prefecture", "targets": [{"role": "市长"}]})
        prompt = build_dispatch_prompt(item)
        assert "江西省" in prompt

    def test_includes_target_roles(self) -> None:
        item = TodoItem(province_name="测试省", task={"id": "x", "region": "测试市", "level": "prefecture", "targets": [{"role": "市委书记"}, {"role": "市长"}]})
        prompt = build_dispatch_prompt(item)
        assert "市委书记" in prompt
        assert "市长" in prompt

    def test_includes_artifact_paths(self) -> None:
        item = TodoItem(province_name="测试省", task={"id": "test_city", "region": "测试市", "level": "prefecture", "targets": [{"role": "市长"}]})
        prompt = build_dispatch_prompt(item)
        assert "build_测试市_data.py" in prompt
        assert "data/database/测试市_network.db" in prompt
        assert "data/graph/测试市_network.gexf" in prompt

    def test_includes_parent_city_from_subtask(self) -> None:
        item = TodoItem(
            province_name="江西省",
            task={"id": "jx_nc", "region": "南昌市", "level": "prefecture", "targets": [{"role": "市长"}]},
            subtask={"id": "jx_nc_qsh", "region": "青山湖区", "level": "district", "parent_city": "南昌市", "targets": [{"role": "区长"}]},
        )
        prompt = build_dispatch_prompt(item)
        assert "青山湖区" in prompt
        assert "南昌市" in prompt
        assert "jx_nc_qsh" in prompt

    def test_model_intent_in_prompt(self) -> None:
        item = TodoItem(province_name="测试省", task={"id": "x", "region": "测试市", "level": "prefecture", "targets": [{"role": "市长"}]})
        prompt = build_dispatch_prompt(item, model_intent="iagent")
        assert "iagent" in prompt


class TestBuildDispatchPlan:
    def test_returns_plan_with_task(self) -> None:
        item = TodoItem(province_name="测试省", task={"id": "test_city", "region": "测试市", "level": "prefecture", "targets": [{"role": "市长"}]})
        plan = build_dispatch_plan(item)
        assert plan.task["task_id"] == "test_city"
        assert plan.model_intent == "standard"

    def test_prompt_matches_dispatch_prompt(self) -> None:
        item = TodoItem(province_name="测试省", task={"id": "test_city", "region": "测试市", "level": "prefecture", "targets": [{"role": "市长"}]})
        plan = build_dispatch_plan(item)
        expected = build_dispatch_prompt(item)
        assert plan.prompt == expected

    def test_suggested_command_not_empty(self) -> None:
        item = TodoItem(province_name="测试省", task={"id": "test_city", "region": "测试市", "level": "prefecture", "targets": [{"role": "市长"}]})
        plan = build_dispatch_plan(item)
        assert plan.suggested_command
        assert "opencode" in plan.suggested_command
