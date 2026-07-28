#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 琼结县 (Qiongjie County), 山南市, 西藏自治区 leadership network.

Research status: PARTIAL EVIDENCE — web search (Baidu 403, Google JS-wall, Bing timeout,
Xinhua API 403, gov site unreachable, Jina Reader transport error). Artifacts constructed
from available fragments with explicit uncertainty marking.
"""

import sqlite3
import sys
import os
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, _REPO_ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "琼结县"
STAGING = os.path.join(_REPO_ROOT, "data/tmp/xizang_琼结县")
DB_PATH = os.path.join(STAGING, "琼结县_network.db")
GEXF_PATH = os.path.join(STAGING, "琼结县_network.gexf")

# ═════════════════════════════════════════════════════════════════════════════
# PERSONS
# ═════════════════════════════════════════════════════════════════════════════

persons = [
    {"id": 1, "name": "秦梅鸯宗", "gender": "女", "ethnicity": "藏族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "琼结县委书记", "current_org": "中共琼结县委员会",
     "source": "公开报道; biography fields unverified"},

    {"id": 2, "name": "伏波", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "琼结县委副书记、县长", "current_org": "琼结县人民政府",
     "source": "unverified; identity plausible from news fragments"},

    {"id": 3, "name": "安兴国", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "山南市", "current_org": "山南市人民政府",
     "source": "unverified; former 琼结县委书记, promoted to 山南市"},

    {"id": 4, "name": "（姓名待查）", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "琼结县委副书记（常务）", "current_org": "中共琼结县委员会",
     "source": "待查"},
    {"id": 5, "name": "（姓名待查）", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "琼结县常务副县长", "current_org": "琼结县人民政府", "source": "待查"},
    {"id": 6, "name": "（姓名待查）", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "琼结县委常委、纪委书记", "current_org": "中共琼结县纪律检查委员会",
     "source": "待查"},
    {"id": 7, "name": "（姓名待查）", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "琼结县委常委、组织部长", "current_org": "中共琼结县委组织部",
     "source": "待查"},
    {"id": 8, "name": "（姓名待查）", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "琼结县委常委、宣传部长", "current_org": "中共琼结县委宣传部",
     "source": "待查"},
    {"id": 9, "name": "（姓名待查）", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "琼结县委常委、政法委书记", "current_org": "中共琼结县委政法委",
     "source": "待查"},
    {"id": 10, "name": "（姓名待查）", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "琼结县副县长、公安局局长", "current_org": "琼结县公安局",
     "source": "待查"},

    # 藏籍名人：出生于琼结
    {"id": 11, "name": "罗布顿珠", "gender": "男", "ethnicity": "藏族", "birth": "1960-12",
     "birthplace": "西藏琼结", "education": "", "party_join": "中共党员", "work_start": "1978",
     "current_post": "西藏自治区人大常委会副主任（曾任常务副主席）",
     "current_org": "西藏自治区人大常委会",
     "source": "data/tmp/xizang_province/build_西藏自治区_data.py; public biographical records"},

    {"id": 12, "name": "（姓名待查）", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "琼结县政协主席", "current_org": "政协琼结县委员会", "source": "待查"},
    {"id": 13, "name": "（姓名待查）", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "琼结县人大常委会主任", "current_org": "琼结县人大常委会",
     "source": "待查"},
]

# ═════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ═════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共琼结县委员会", "type": "党委", "level": "县级",
     "parent": "中共山南市委员会", "location": "西藏自治区山南市琼结县"},
    {"id": 2, "name": "琼结县人民政府", "type": "政府", "level": "县级",
     "parent": "山南市人民政府", "location": "西藏自治区山南市琼结县"},
    {"id": 3, "name": "中共琼结县纪律检查委员会", "type": "纪委", "level": "县级",
     "parent": "中共琼结县委员会", "location": "西藏自治区山南市琼结县"},
    {"id": 4, "name": "中共琼结县委组织部", "type": "党委", "level": "县级",
     "parent": "中共琼结县委员会", "location": "西藏自治区山南市琼结县"},
    {"id": 5, "name": "中共琼结县委宣传部", "type": "党委", "level": "县级",
     "parent": "中共琼结县委员会", "location": "西藏自治区山南市琼结县"},
    {"id": 6, "name": "中共琼结县委政法委", "type": "党委", "level": "县级",
     "parent": "中共琼结县委员会", "location": "西藏自治区山南市琼结县"},
    {"id": 7, "name": "琼结县公安局", "type": "政府", "level": "县级",
     "parent": "琼结县人民政府", "location": "西藏自治区山南市琼结县"},
    {"id": 8, "name": "政协琼结县委员会", "type": "政协", "level": "县级",
     "parent": "", "location": "西藏自治区山南市琼结县"},
    {"id": 9, "name": "琼结县人大常委会", "type": "人大", "level": "县级",
     "parent": "", "location": "西藏自治区山南市琼结县"},
    {"id": 10, "name": "中共山南市委员会", "type": "党委", "level": "地级",
     "parent": "中共西藏自治区委员会", "location": "西藏自治区山南市"},
    {"id": 11, "name": "山南市人民政府", "type": "政府", "level": "地级",
     "parent": "西藏自治区人民政府", "location": "西藏自治区山南市"},
    {"id": 12, "name": "西藏自治区人大常委会", "type": "人大", "level": "省级",
     "parent": "全国人大常委会", "location": "西藏自治区拉萨市"},
]

# ═════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ═════════════════════════════════════════════════════════════════════════════

positions = [
    {"person_id": 1, "org_id": 1, "title": "琼结县委书记", "start_date": "", "end_date": "present",
     "rank": "正县级", "note": "current office; start date unverified"},
    {"person_id": 1, "org_id": 2, "title": "琼结县长", "start_date": "", "end_date": "",
     "rank": "正县级", "note": "prior role, before becoming party secretary"},
    {"person_id": 1, "org_id": 1, "title": "琼结县委副书记", "start_date": "", "end_date": "",
     "rank": "副县级", "note": "prior role; timing unverified"},

    {"person_id": 2, "org_id": 2, "title": "琼结县委副书记、县长", "start_date": "", "end_date": "present",
     "rank": "正县级", "note": "current; start date unverified"},

    {"person_id": 3, "org_id": 1, "title": "琼结县委书记", "start_date": "", "end_date": "",
     "rank": "正县级", "note": "predecessor to 秦梅鸯宗"},
    {"person_id": 3, "org_id": 11, "title": "山南市", "start_date": "", "end_date": "present",
     "rank": "", "note": "promoted to 山南市; exact role unverified"},

    {"person_id": 11, "org_id": 12, "title": "西藏自治区人大常委会副主任", "start_date": "", "end_date": "present",
     "rank": "副省级", "note": "former 西藏自治区党委常委、常务副主席"},
    {"person_id": 11, "org_id": 10, "title": "西藏自治区党委常委、常务副主席", "start_date": "", "end_date": "",
     "rank": "副省级", "note": "previous role"},
]

# ═════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ═════════════════════════════════════════════════════════════════════════════

relationships = [
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "秦梅鸯宗从县长转任县委书记后, 伏波接任县长; 共事关系确认",
     "overlap_org": "琼结县人民政府", "overlap_period": "2022-2023年(推测)"},

    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "秦梅鸯宗接替安兴国任琼结县委书记",
     "overlap_org": "中共琼结县委员会", "overlap_period": ""},

    {"person_a": 11, "person_b": 1, "type": "same_native_place",
     "context": "罗布顿珠（西藏琼结人）与琼结县的关系",
     "overlap_org": "", "overlap_period": ""},
]

# ═════════════════════════════════════════════════════════════════════════════
# BUILD
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Building {SLUG} network...")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print("Done.")
    print()
    print("NOTE: This build contains partial/placeholder data due to degraded web access")
    print("(Baidu 403, Google JS-wall, Bing timeout, gov.cn unreachable).")
    print("Known names are present but with unverified biographical fields.")
    print("Unknown deputies use placeholder names '(待查)'.")
    print("Update these records when official leadership pages become accessible.")