"""Tests for generated v3 builder scripts."""

import py_compile
import runpy
import sqlite3

from gov_relation.factory import BuildScriptFactory


def test_generated_script_compiles_and_executes_full_relationship_flow(tmp_path):
    province_dir = tmp_path / "data" / "provinces" / "sichuan"
    script = BuildScriptFactory().generate(
        slug="测试县",
        province_name="四川省",
        persons=[
            {"canonical_name": "甲", "birth_text": "1960"},
            {"canonical_name": "乙", "birth_text": "1965"},
        ],
        organizations=[{"canonical_name": "测试县委"}],
        positions=[
            {
                "person_name": "甲",
                "organization_name": "测试县委",
                "title": "县委书记",
                "is_current": 1,
            }
        ],
        relationships=[
            {
                "person_from_name": "甲",
                "person_to_name": "乙",
                "relationship_type": "coworker",
            }
        ],
    )
    path = tmp_path / "scripts" / "build" / "build_sichuan_测试县_data.py"
    path.parent.mkdir(parents=True)
    # F4 定位机制:生成脚本向上寻找含 gov_relation/ 的目录作为仓库根。
    (tmp_path / "gov_relation").mkdir()  # 模拟测试环境中的仓库根标记
    path.write_text(script, encoding="utf-8")
    py_compile.compile(str(path), doraise=True)
    runpy.run_path(str(path), run_name="__main__")
    database = province_dir / "database" / "测试县_network.db"
    assert database.exists()
    conn = sqlite3.connect(database)
    assert conn.execute("SELECT COUNT(*) FROM positions").fetchone()[0] == 1
    assert conn.execute("SELECT COUNT(*) FROM relationships").fetchone()[0] == 1
    assert list((province_dir / "persons").glob("*.json"))
    assert (province_dir / "reports" / "测试县_report.md").exists()


def test_generated_script_uses_runner_v3_backend(tmp_path):
    script = BuildScriptFactory().generate(
        slug="空县", province_name="四川省",
        persons=[], organizations=[], positions=[], relationships=[],
    )
    assert "from gov_relation.runner import run_build" in script
    assert 'backend="v3"' in script
    assert str(tmp_path) not in script
    # F4: 仓库根由 _repo_root() 沿父目录链定位,不再硬编码 parents[2]
    assert 'def _repo_root()' in script
    assert '(parent / "gov_relation").is_dir()' in script
    assert 'Path(__file__).resolve().parents[2]' not in script
