"""Tests for gov_relation/runner.py."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from gov_relation.runner import run_build


class TestRunBuild:
    def test_creates_db_and_gexf(self, tmp_path: Path) -> None:
        db = tmp_path / "test_network.db"
        gexf = tmp_path / "test_network.gexf"
        run_build(
            slug="测试市",
            persons=[{"id": 1, "name": "张三"}, {"id": 2, "name": "李四"}],
            organizations=[{"id": 10, "name": "市政府"}],
            positions=[
                {"person_id": 1, "org_id": 10, "title": "市长"},
                {"person_id": 2, "org_id": 10, "title": "副市长"},
            ],
            relationships=[{"person_a": 1, "person_b": 2, "type": "共事"}],
            db_path=db,
            gexf_path=gexf,
            overwrite=True,
        )
        assert db.exists()
        assert gexf.exists()

    def test_db_has_correct_data(self, tmp_path: Path) -> None:
        db = tmp_path / "test_network.db"
        gexf = tmp_path / "test_network.gexf"
        run_build(
            slug="测试市",
            persons=[{"id": 1, "name": "张三"}],
            organizations=[{"id": 10, "name": "市政府"}],
            positions=[{"person_id": 1, "org_id": 10, "title": "市长"}],
            relationships=[],
            db_path=db,
            gexf_path=gexf,
            overwrite=True,
        )
        conn = sqlite3.connect(str(db))
        conn.row_factory = sqlite3.Row
        try:
            persons = conn.execute("SELECT name FROM persons").fetchall()
            assert [r[0] for r in persons] == ["张三"]
            orgs = conn.execute("SELECT name FROM organizations").fetchall()
            assert [r[0] for r in orgs] == ["市政府"]
        finally:
            conn.close()

    def test_overwrite_replaces_db(self, tmp_path: Path) -> None:
        db = tmp_path / "test_network.db"
        gexf = tmp_path / "test_network.gexf"
        run_build(
            slug="测试市",
            persons=[{"id": 1, "name": "张三"}],
            organizations=[{"id": 10, "name": "市政府"}],
            positions=[{"person_id": 1, "org_id": 10, "title": "市长"}],
            relationships=[],
            db_path=db,
            gexf_path=gexf,
            overwrite=True,
        )
        # Run again with overwrite
        run_build(
            slug="测试市",
            persons=[{"id": 2, "name": "李四"}],
            organizations=[{"id": 20, "name": "新机构"}],
            positions=[{"person_id": 2, "org_id": 20, "title": "主任"}],
            relationships=[],
            db_path=db,
            gexf_path=gexf,
            overwrite=True,
        )
        conn = sqlite3.connect(str(db))
        try:
            names = conn.execute("SELECT name FROM persons").fetchall()
            assert [r[0] for r in names] == ["李四"]  # overwritten, not appended
        finally:
            conn.close()

    def test_gexf_contains_nodes_and_edges(self, tmp_path: Path) -> None:
        db = tmp_path / "test_network.db"
        gexf = tmp_path / "test_network.gexf"
        run_build(
            slug="测试市",
            persons=[{"id": 1, "name": "张三"}, {"id": 2, "name": "李四"}],
            organizations=[{"id": 10, "name": "市政府"}],
            positions=[{"person_id": 1, "org_id": 10, "title": "市长"}],
            relationships=[{"person_a": 1, "person_b": 2, "type": "共事"}],
            db_path=db,
            gexf_path=gexf,
            overwrite=True,
        )
        content = gexf.read_text(encoding="utf-8")
        # GEXF should mention both persons and the relationship
        assert "张三" in content
        assert "李四" in content
        assert "市政府" in content
        assert "共事" in content
        # Should be valid XML
        import xml.etree.ElementTree as ET
        root = ET.fromstring(content)
        assert root.tag.endswith("gexf")
