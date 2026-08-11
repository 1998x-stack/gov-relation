"""Integration tests for the regional v3 orchestrator."""

import json
import sqlite3

import gov_relation.factory.region_factory as region_module
import gov_relation.paths as paths
from gov_relation.factory import RegionResearchFactory


def test_full_region_pipeline_with_positions_and_relationships(tmp_path, monkeypatch):
    province_root = tmp_path / "provinces"
    build_root = tmp_path / "build"
    monkeypatch.setattr(paths, "PROVINCES_DIR", province_root)
    monkeypatch.setattr(region_module, "province_build_dir", lambda _: build_root)
    factory = RegionResearchFactory(
        province="四川省", region="测试县", level="county", targets=[]
    )
    factory.add_person({"canonical_name": "甲", "birth_text": "1960"})
    factory.add_person({"canonical_name": "乙", "birth_text": "1965"})
    factory.add_organization({"canonical_name": "测试县委"})
    factory.add_position(
        {
            "person_name": "甲",
            "organization_name": "测试县委",
            "title": "县委书记",
            "is_current": 1,
        }
    )
    factory.add_relationship(
        {
            "person_from_name": "甲",
            "person_to_name": "乙",
            "relationship_type": "coworker",
        }
    )
    script = factory.generate_build_script()
    graph = factory.generate_gexf()
    profiles = factory.generate_person_profiles()
    report = factory.generate_report()
    assert script.name == "build_sichuan_测试县_data.py"
    assert graph.exists() and len(profiles) == 2 and report.exists()
    profile = json.loads(profiles[0].read_text(encoding="utf-8"))
    assert "source_register" in profile
    conn = sqlite3.connect(province_root / "sichuan/database/测试县_network.db")
    assert conn.execute("SELECT COUNT(*) FROM positions").fetchone()[0] == 1
    assert conn.execute("SELECT COUNT(*) FROM relationships").fetchone()[0] == 1
