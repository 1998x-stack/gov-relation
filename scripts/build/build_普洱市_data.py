#!/usr/bin/env python3
"""Build script for 普洱市 (Pu'er City) — prefecture-level city in 云南省.

Current leaders (as of 2026-08):
- 市委书记: 李庆元 (Li Qingyuan, b. 1970-08, 玉溪江川)
- 市长: 王刚 (Wang Gang, b. 1977-11, Yi ethnic, 昭通大关)
- 人大主任: 王鸿彬 (Wang Hongbin, b. 1968-03, 普洱景东)
- 政协主席: 张光彦 (Zhang Guangyan, b. 1970-08, 曲靖宣威, elected 2026-02)

Sources:
- Wikipedia (zh): https://zh.wikipedia.org/wiki/普洱市
- People's Daily leadership database (referenced but not directly accessible)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Persons ────────────────────────────────────────────────────────

persons = [
    {
        "id": 1,
        "name": "李庆元",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年8月",
        "birthplace": "云南省玉溪市江川区",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "普洱市委书记",
        "current_org": "中国共产党普洱市委员会",
        "source": "https://zh.wikipedia.org/wiki/普洱市",
    },
    {
        "id": 2,
        "name": "王刚",
        "gender": "男",
        "ethnicity": "彝族",
        "birth": "1977年11月",
        "birthplace": "云南省昭通市大关县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "普洱市市长",
        "current_org": "普洱市人民政府",
        "source": "https://zh.wikipedia.org/wiki/普洱市",
    },
    {
        "id": 3,
        "name": "王鸿彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年3月",
        "birthplace": "云南省普洱市景东彝族自治县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "普洱市人大常委会主任",
        "current_org": "普洱市人民代表大会常务委员会",
        "source": "https://zh.wikipedia.org/wiki/普洱市",
    },
    {
        "id": 4,
        "name": "张光彦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年8月",
        "birthplace": "云南省曲靖市宣威市",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "普洱市政协主席",
        "current_org": "中国人民政治协商会议普洱市委员会",
        "source": "https://zh.wikipedia.org/wiki/普洱市",
    },
    # Predecessors
    {
        "id": 5,
        "name": "卫星",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/普洱市",
    },
    {
        "id": 6,
        "name": "刘勇",
        "gender": "男",
        "ethnicity": "纳西族",
        "birth": "1967年",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "云南省副省长",
        "current_org": "云南省人民政府",
        "source": "https://zh.wikipedia.org/wiki/普洱市",
    },
    {
        "id": 7,
        "name": "沈培平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1962年",
        "birthplace": "云南省保山市施甸县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/普洱市",
    },
    {
        "id": 8,
        "name": "杨照辉",
        "gender": "男",
        "ethnicity": "",
        "birth": "1963年",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/普洱市",
    },
    {
        "id": 9,
        "name": "钱德伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/普洱市",
    },
    {
        "id": 10,
        "name": "李小平",
        "gender": "男",
        "ethnicity": "",
        "birth": "1965年",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/普洱市",
    },
    {
        "id": 11,
        "name": "卯稳国",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/普洱市",
    },
    {
        "id": 12,
        "name": "高旭升",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/普洱市",
    },
    {
        "id": 13,
        "name": "李元书",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/普洱市",
    },
]

# ── Organizations ──────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中国共产党普洱市委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中国共产党云南省委员会",
        "location": "云南省普洱市思茅区",
    },
    {
        "id": 2,
        "name": "普洱市人民政府",
        "type": "政府",
        "level": "地级",
        "parent": "云南省人民政府",
        "location": "云南省普洱市思茅区",
    },
    {
        "id": 3,
        "name": "普洱市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级",
        "parent": "",
        "location": "云南省普洱市思茅区",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议普洱市委员会",
        "type": "政协",
        "level": "地级",
        "parent": "",
        "location": "云南省普洱市思茅区",
    },
    {
        "id": 5,
        "name": "云南省人民政府",
        "type": "政府",
        "level": "省级",
        "parent": "",
        "location": "云南省昆明市",
    },
]

# ── Positions ──────────────────────────────────────────────────────

positions = [
    # Current leadership
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2021年6月", "end_date": "", "rank": "正厅级", "note": "现任"},
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "2022年2月", "end_date": "", "rank": "正厅级", "note": "现任"},
    {"person_id": 3, "org_id": 3, "title": "市人大常委会主任", "start_date": "2022年2月", "end_date": "", "rank": "正厅级", "note": "现任"},
    {"person_id": 4, "org_id": 4, "title": "市政协主席", "start_date": "2026年2月", "end_date": "", "rank": "正厅级", "note": "现任"},

    # Predecessor positions — Party Secretaries
    {"person_id": 5, "org_id": 1, "title": "市委书记", "start_date": "2013年2月", "end_date": "2021年6月", "rank": "正厅级", "note": "前任"},
    {"person_id": 7, "org_id": 1, "title": "市委书记", "start_date": "2009年12月", "end_date": "2013年2月", "rank": "正厅级", "note": "前任"},
    {"person_id": 12, "org_id": 1, "title": "市委书记", "start_date": "2005年8月", "end_date": "2009年12月", "rank": "正厅级", "note": "前任"},
    {"person_id": 13, "org_id": 1, "title": "市委书记", "start_date": "2004年3月", "end_date": "2005年8月", "rank": "正厅级", "note": "首任"},

    # Predecessor Mayors
    {"person_id": 6, "org_id": 2, "title": "市长", "start_date": "2018年6月", "end_date": "2022年2月", "rank": "正厅级", "note": "前任"},
    {"person_id": 8, "org_id": 2, "title": "市长", "start_date": "2015年6月", "end_date": "2018年6月", "rank": "正厅级", "note": "前任"},
    {"person_id": 9, "org_id": 2, "title": "市长", "start_date": "2013年2月", "end_date": "2015年6月", "rank": "正厅级", "note": "前任"},
    {"person_id": 10, "org_id": 2, "title": "市长", "start_date": "2010年1月", "end_date": "2013年2月", "rank": "正厅级", "note": "前任"},
    {"person_id": 7, "org_id": 2, "title": "市长", "start_date": "2005年1月", "end_date": "2009年12月", "rank": "正厅级", "note": "前任 → 升任市委书记"},
    {"person_id": 11, "org_id": 2, "title": "市长", "start_date": "2004年3月", "end_date": "2004年12月", "rank": "正厅级", "note": "首任市长"},

    # Other current roles
    {"person_id": 6, "org_id": 5, "title": "副省长", "start_date": "2024年", "end_date": "", "rank": "副省级", "note": "现任"},
]

# ── Relationships ──────────────────────────────────────────────────

relationships = [
    # Succession relationships
    {
        "person_a": 5, "person_b": 1,
        "type": "predecessor_successor",
        "context": "卫星→李庆元：普洱市委书记接任",
        "overlap_org": "中国共产党普洱市委员会",
        "overlap_period": "2021年6月",
    },
    {
        "person_a": 6, "person_b": 2,
        "type": "predecessor_successor",
        "context": "刘勇→王刚：普洱市市长接任",
        "overlap_org": "普洱市人民政府",
        "overlap_period": "2022年2月",
    },
    {
        "person_a": 7, "person_b": 5,
        "type": "predecessor_successor",
        "context": "沈培平→卫星：普洱市委书记接任",
        "overlap_org": "中国共产党普洱市委员会",
        "overlap_period": "2013年2月",
    },
    {
        "person_a": 8, "person_b": 6,
        "type": "predecessor_successor",
        "context": "杨照辉→刘勇：普洱市市长接任",
        "overlap_org": "普洱市人民政府",
        "overlap_period": "2018年6月",
    },
    {
        "person_a": 9, "person_b": 8,
        "type": "predecessor_successor",
        "context": "钱德伟→杨照辉：普洱市市长接任",
        "overlap_org": "普洱市人民政府",
        "overlap_period": "2015年6月",
    },
    # Internal promotion: 沈培平 市长→书记
    {
        "person_a": 7, "person_b": 7,
        "type": "promotion_chain",
        "context": "沈培平由普洱市长升任市委书记（内部提拔）",
        "overlap_org": "中国共产党普洱市委员会/普洱市人民政府",
        "overlap_period": "2009-2013",
    },
    # Colleague relationships (current leadership team)
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "李庆元（书记）与王刚（市长）为现任党政一把手",
        "overlap_org": "中国共产党普洱市委员会",
        "overlap_period": "2022年2月至今",
    },
    # Cross-city flows
    {
        "person_a": 1, "person_b": 2,
        "type": "same_region_rotation",
        "context": "李庆元（玉溪→普洱）与王刚（昭通→普洱）均为外市调入",
        "overlap_org": "普洱市",
        "overlap_period": "2021-2022",
    },
]

# ── Paths ──────────────────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "普洱市_network.db")
GEXF_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "普洱市_network.gexf")

# ── Run ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sqlite3
    db_path = DB_PATH
    gexf_path = GEXF_PATH

    run_build(
        slug="普洱市",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
    )

    print("=" * 50)
    print(f"Database: {db_path}")
    print(f"GEXF:     {gexf_path}")
    print(f"Persons:  {len(persons)}")
    print(f"Orgs:     {len(organizations)}")
    print(f"Positions:{len(positions)}")
    print(f"Rels:     {len(relationships)}")
    print("=" * 50)