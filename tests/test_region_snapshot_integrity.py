"""Region snapshots must refresh facts without deleting independent records."""

from __future__ import annotations

import pytest

from gov_relation.canon.pillar_region import (
    region_records,
    snapshot_regions,
    write_region,
)
from gov_relation.canon.streams import iter_jsonl, write_jsonl


def _persons(root):
    return list(iter_jsonl(root / "persons.jsonl"))


def _region(name):
    return region_records(
        "甲区",
        persons=[{"id": 1, "name": name}],
        organizations=[],
        positions=[],
        relationships=[],
    )


def test_snapshot_updates_researched_person_and_removes_stale_partition(tmp_path):
    root = tmp_path / "records"
    write_region(root, "甲区", "甲省", _region("旧姓名"))
    assert snapshot_regions(root)["persons"] == 1
    assert _persons(root)[0]["canonical_name"] == "旧姓名"

    write_region(root, "甲区", "甲省", _region("更新姓名"))
    assert snapshot_regions(root)["persons"] == 0
    assert _persons(root)[0]["canonical_name"] == "更新姓名"

    empty = region_records("甲区", persons=[], organizations=[], positions=[], relationships=[])
    part = write_region(root, "甲区", "甲省", empty)
    assert not (part / "persons.jsonl").exists()
    assert snapshot_regions(root)["persons"] == 0
    assert _persons(root) == []
    assert snapshot_regions(root)["persons"] == 0


def test_unrelated_flat_records_survive_region_refresh(tmp_path):
    root = tmp_path / "records"
    write_region(root, "甲区", "甲省", _region("原始"))
    write_jsonl(root / "persons.jsonl", iter([{"person_id": "independent", "canonical_name": "手工记录"}]))
    assert snapshot_regions(root)["persons"] == 1
    write_region(root, "甲区", "甲省", _region("修订"))
    assert snapshot_regions(root)["persons"] == 0
    assert [(r["person_id"], r["canonical_name"]) for r in _persons(root)] == [
        ("independent", "手工记录"), ("甲区:person:1", "修订")
    ]


def test_duplicate_id_across_provinces_fails_before_writing_flat_stream(tmp_path):
    root = tmp_path / "records"
    write_region(root, "甲区", "甲省", _region("甲"))
    write_region(root, "甲区", "乙省", _region("乙"))
    with pytest.raises(ValueError, match="Duplicate persons ID"):
        snapshot_regions(root)
    assert not (root / "persons.jsonl").exists()
    assert not (root / ".region_snapshot_state.json").exists()


def test_unowned_conflicting_flat_record_is_not_overwritten(tmp_path):
    root = tmp_path / "records"
    write_region(root, "甲区", "甲省", _region("调查数据"))
    existing = [{"person_id": "甲区:person:1", "canonical_name": "独立数据"}]
    write_jsonl(root / "persons.jsonl", iter(existing))
    with pytest.raises(ValueError, match="Unowned flat persons record"):
        snapshot_regions(root)
    assert _persons(root) == existing


def test_duplicate_raw_person_ids_rejected_before_partition_write():
    with pytest.raises(ValueError, match="Duplicate person ID"):
        region_records(
            "甲区", persons=[{"id": 1}, {"id": 1}],
            organizations=[], positions=[], relationships=[],
        )
