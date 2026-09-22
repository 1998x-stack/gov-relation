"""Canonical JSONL contract: objects only, valid JSON numbers and atomic writes."""

from __future__ import annotations

import math

import pytest

from gov_relation.canon.streams import iter_jsonl, write_jsonl


@pytest.mark.parametrize(
    "bad_line",
    ["[]", "null", "42", '"text"', '{"x": NaN}', '{"x": Infinity}', '{"x": -Infinity}', '{oops'],
)
def test_jsonl_reader_reports_file_and_original_line_number(tmp_path, bad_line):
    path = tmp_path / "persons.jsonl"
    path.write_text('{"person_id":"ok"}\n\n' + bad_line + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match=r"persons\.jsonl:3:"):
        list(iter_jsonl(path))


def test_reader_preserves_unicode_and_valid_json_values(tmp_path):
    path = tmp_path / "persons.jsonl"
    path.write_text('{"person_id":"测试", "value": null}\n', encoding="utf-8")
    assert list(iter_jsonl(path)) == [{"person_id": "测试", "value": None}]


@pytest.mark.parametrize("invalid", [float("nan"), float("inf"), -float("inf")])
def test_writer_rejects_nonfinite_numbers_without_replacing_existing_stream(tmp_path, invalid):
    path = tmp_path / "persons.jsonl"
    write_jsonl(path, iter([{"person_id": "existing"}]))
    before = path.read_bytes()
    with pytest.raises(ValueError):
        write_jsonl(path, iter([{"person_id": "new"}, {"value": invalid}]))
    assert path.read_bytes() == before
    assert list(tmp_path.glob(".persons.jsonl.*.tmp")) == []


def test_writer_rejects_non_object_row_and_discards_staged_rows(tmp_path):
    path = tmp_path / "persons.jsonl"
    write_jsonl(path, iter([{"person_id": "existing"}]))
    before = path.read_bytes()
    with pytest.raises(TypeError, match="row 2 must be a JSON object"):
        write_jsonl(path, iter([{"person_id": "new"}, [1, 2]]))
    assert path.read_bytes() == before
    assert list(tmp_path.glob(".persons.jsonl.*.tmp")) == []


def test_valid_writer_remains_idempotent(tmp_path):
    path = tmp_path / "persons.jsonl"
    rows = [{"person_id": "张三", "valid": True}, {"person_id": "李四", "value": 1.5}]
    assert write_jsonl(path, iter(rows)) == 2
    first = path.read_bytes()
    assert write_jsonl(path, iter(rows)) == 2
    assert path.read_bytes() == first
    assert list(iter_jsonl(path)) == rows
