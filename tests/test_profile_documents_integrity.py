"""Regression coverage for provenance-safe profile document imports."""

from __future__ import annotations

import json
from argparse import Namespace
from pathlib import Path

import pytest

from gov_relation.canon.pillar_profiles import _profile_to_document, pillar_import_profiles
from gov_relation.canon.streams import iter_jsonl, write_jsonl


def _fixture(monkeypatch, tmp_path: Path):
    import gov_relation.paths as paths

    monkeypatch.setattr(paths, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(paths, "PERSONS_DIR", tmp_path / "data" / "persons")
    monkeypatch.setattr(paths, "PROVINCES_DIR", tmp_path / "data" / "provinces")
    paths.PROVINCES_DIR.mkdir(parents=True)
    records = tmp_path / "data" / "records"
    return Namespace(records=str(records)), records / "profile_documents.jsonl"


def _write_profile(tmp_path: Path, province: str, name: str, person_id: str):
    path = tmp_path / "data" / "provinces" / province / "persons" / "same.json"
    path.parent.mkdir(parents=True)
    data = {"identity": {"person_id": person_id, "name": name}}
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return path, data


def test_same_relative_filename_in_two_provinces_gets_distinct_stable_ids(monkeypatch, tmp_path):
    args, target = _fixture(monkeypatch, tmp_path)
    _write_profile(tmp_path, "a", "甲", "person-a")
    _write_profile(tmp_path, "b", "乙", "person-b")

    assert pillar_import_profiles(args) == 0
    rows = list(iter_jsonl(target))
    assert len(rows) == 2
    assert {r["person_id"] for r in rows} == {"person-a", "person-b"}
    assert len({r["profile_id"] for r in rows}) == 2
    before = target.read_bytes()
    assert pillar_import_profiles(args) == 0
    assert target.read_bytes() == before


def test_unambiguous_legacy_id_is_preserved_without_duplicate(monkeypatch, tmp_path):
    args, target = _fixture(monkeypatch, tmp_path)
    _, data = _write_profile(tmp_path, "a", "甲", "person-a")
    target.parent.mkdir(parents=True)
    old = _profile_to_document(data, "same.json")
    write_jsonl(target, iter([old]))
    before = target.read_bytes()

    assert pillar_import_profiles(args) == 0
    assert target.read_bytes() == before
    assert list(iter_jsonl(target)) == [old]


def test_ambiguous_legacy_id_requires_explicit_reconciliation(monkeypatch, tmp_path):
    args, target = _fixture(monkeypatch, tmp_path)
    _, data = _write_profile(tmp_path, "a", "甲", "person-a")
    _write_profile(tmp_path, "b", "乙", "person-b")
    target.parent.mkdir(parents=True)
    write_jsonl(target, iter([_profile_to_document(data, "same.json")]))
    before = target.read_bytes()

    with pytest.raises(ValueError, match="ambiguous legacy profile_id"):
        pillar_import_profiles(args)
    assert target.read_bytes() == before


def test_updated_profile_fails_without_silently_preserving_stale_data(monkeypatch, tmp_path):
    args, target = _fixture(monkeypatch, tmp_path)
    path, data = _write_profile(tmp_path, "a", "甲", "person-a")
    assert pillar_import_profiles(args) == 0
    before = target.read_bytes()
    data["identity"]["name"] = "甲（更新）"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    with pytest.raises(ValueError, match="profile changed or ID collided"):
        pillar_import_profiles(args)
    assert target.read_bytes() == before


def test_conflict_after_new_candidate_does_not_partially_append(monkeypatch, tmp_path):
    args, target = _fixture(monkeypatch, tmp_path)
    _write_profile(tmp_path, "z", "原记录", "person-z")
    assert pillar_import_profiles(args) == 0
    before = target.read_bytes()
    # Sorting by source key processes the new record before the stale one.
    _write_profile(tmp_path, "a", "新增", "person-a")
    _write_profile(tmp_path, "z", "已修改", "person-z")

    with pytest.raises(ValueError, match="profile changed or ID collided"):
        pillar_import_profiles(args)
    assert target.read_bytes() == before


def test_duplicate_existing_profile_id_is_rejected(monkeypatch, tmp_path):
    args, target = _fixture(monkeypatch, tmp_path)
    target.parent.mkdir(parents=True)
    row = _profile_to_document({"identity": {"person_id": "x"}}, "same.json")
    write_jsonl(target, iter([row, row]))
    before = target.read_bytes()

    with pytest.raises(ValueError, match="duplicate existing profile_id"):
        pillar_import_profiles(args)
    assert target.read_bytes() == before
