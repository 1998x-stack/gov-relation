#!/usr/bin/env python3
"""Build 奎屯市 (伊犁哈萨克自治州, 新疆维吾尔自治区) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou + 中国日报网/中国在线/手机搜狐.
Current: 市委书记杨小成(2024市委常委会主持), 市长阿勒泰·赛肯. 前任书记赵永龙(伊犁州党委常委).
"""
import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "奎屯市"
STAGING = data_path("tmp", "新疆维吾尔自治区_奎屯市")
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

def _verify_db():
    conn = sqlite3.connect(str(DB_PATH))
    for table in ("persons", "organizations", "positions", "relationships"):
        try:
            n = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"  {table}: {n} rows")
        except Exception as exc:
            print(f"  {table}: (none) {exc}")
    conn.close()

PERSONS = [
    {"id": 1, "name": "杨小成", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市委书记", "current_org": "中共奎屯市委",
     "source": "奎屯市八届市委2024年第4次常委会(扩大)会议(市委书记杨小成主持会议并讲话)"},
    {"id": 2, "name": "阿勒泰·赛肯", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市长/市委副书记", "current_org": "奎屯市人民政府",
     "source": "新华/手机搜狐(新疆奎屯市委副书记、市人民政府市长阿勒泰·赛肯)"},
    {"id": 3, "name": "赵永龙", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "(前任书记)", "current_org": "中共奎屯市委",
     "source": "中国日报网(伊犁州党委常委、奎屯市委书记赵永龙)"},
]
ORGANIZATIONS = [
    {"id": 101, "name": "中共奎屯市委", "type": "党委", "level": "县级市", "parent": "中共伊犁州委", "location": "伊犁州奎屯市"},
    {"id": 102, "name": "奎屯市人民政府", "type": "政府", "level": "县级市", "parent": "伊犁州人民政府", "location": "伊犁州奎屯市"},
]
POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "市委书记", "start": "", "end": "", "rank": "正处级", "note": "2024主持市委常委会"},
    {"person_id": 2, "org_id": 102, "title": "市长", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 101, "title": "市委副书记", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 3, "org_id": 101, "title": "市委书记(前任)", "start": "", "end": "", "rank": "正处级", "note": "曾任伊犁州党委常委"},
]
RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "市委书记-市长", "overlap_org": "中共奎屯市委/奎屯市人民政府", "overlap_period": "现职"},
    {"person_a": 1, "person_b": 3, "type": "继任关系", "context": "杨小成继任赵永龙任奎屯市委书记", "overlap_org": "中共奎屯市委", "overlap_period": "交接"},
]
if __name__ == "__main__":
    run_build(slug="奎屯市", persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
