#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 江川区, Yuxi, Yunnan."""

import sys
import os
from datetime import datetime

# Add project to path
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

TMP = os.path.join(BASE, "data/tmp/yunnan_江川区")
DB_PATH = os.path.join(TMP, "江川区_network.db")
GEXF_PATH = os.path.join(TMP, "江川区_network.gexf")

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {
        "id": 1,
        "name": "王晋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "玉溪市江川区委书记",
        "current_org": "中共玉溪市江川区委员会",
        "source": "https://www.ynjc.gov.cn/jc/jcdt79/20260724/1672446.html",
    },
    {
        "id": 2,
        "name": "李金",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "玉溪市江川区委副书记、区长",
        "current_org": "玉溪市江川区人民政府",
        "source": "https://www.ynjc.gov.cn/jc/jcdt79/20260728/1673019.html",
    },
    # ── Other Key Leaders ──
    {
        "id": 3,
        "name": "杨雪彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "玉溪市江川区委副书记",
        "current_org": "中共玉溪市江川区委员会",
        "source": "https://www.ynjc.gov.cn/jc/jcdt79/20260724/1672449.html",
    },
    {
        "id": 4,
        "name": "汪涉源",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "玉溪市江川区委常委、区人武部部长",
        "current_org": "玉溪市江川区人民武装部",
        "source": "https://www.ynjc.gov.cn/jc/jcdt79/20260717/1671486.html",
    },
    {
        "id": 5,
        "name": "杨刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "玉溪市江川区委常委、组织部部长",
        "current_org": "中共玉溪市江川区委员会组织部",
        "source": "https://www.ynjc.gov.cn/jc/jcdt79/20260724/1672449.html",
    },
    {
        "id": 6,
        "name": "普超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "江川区领导（区委常委）",
        "current_org": "中共玉溪市江川区委员会",
        "source": "https://www.ynjc.gov.cn/jc/tpxw/20260625/1668529.html",
    },
    {
        "id": 7,
        "name": "莽嘉慧",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "江川区领导",
        "current_org": "玉溪市江川区",
        "source": "https://www.ynjc.gov.cn/jc/jcdt79/20260724/1672449.html",
    },
    {
        "id": 8,
        "name": "李德坤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "江川区领导",
        "current_org": "中共玉溪市江川区委员会",
        "source": "https://www.ynjc.gov.cn/jc/tpxw/20260625/1668529.html",
    },
    {
        "id": 9,
        "name": "耿兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "江川区领导",
        "current_org": "中共玉溪市江川区委员会",
        "source": "https://www.ynjc.gov.cn/jc/tpxw/20260625/1668529.html",
    },
    {
        "id": 10,
        "name": "吴芳芳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "江川区领导",
        "current_org": "中共玉溪市江川区委员会",
        "source": "https://www.ynjc.gov.cn/jc/tpxw/20260625/1668529.html",
    },
    {
        "id": 11,
        "name": "宋磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "江川区领导",
        "current_org": "中共玉溪市江川区委员会",
        "source": "https://www.ynjc.gov.cn/jc/tpxw/20260625/1668529.html",
    },
    {
        "id": 12,
        "name": "刘勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "江川区领导",
        "current_org": "中共玉溪市江川区委员会",
        "source": "https://www.ynjc.gov.cn/jc/tpxw/20260625/1668529.html",
    },
    {
        "id": 13,
        "name": "王云峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "江川区领导",
        "current_org": "中共玉溪市江川区委员会",
        "source": "https://www.ynjc.gov.cn/jc/tpxw/20260625/1668529.html",
    },
    {
        "id": 14,
        "name": "林家宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "江川区领导",
        "current_org": "中共玉溪市江川区委员会",
        "source": "https://www.ynjc.gov.cn/jc/tpxw/20260625/1668529.html",
    },
    {
        "id": 15,
        "name": "李光耀",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "江川区领导",
        "current_org": "中共玉溪市江川区委员会",
        "source": "https://www.ynjc.gov.cn/jc/tpxw/20260625/1668529.html",
    },
    {
        "id": 16,
        "name": "王亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "江川区领导",
        "current_org": "中共玉溪市江川区委员会",
        "source": "https://www.ynjc.gov.cn/jc/tpxw/20260625/1668529.html",
    },
    {
        "id": 17,
        "name": "鲁熊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "江川区领导",
        "current_org": "中共玉溪市江川区委员会",
        "source": "https://www.ynjc.gov.cn/jc/tpxw/20260625/1668529.html",
    },
    {
        "id": 18,
        "name": "杨辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "玉溪市江川区人大常委会主任",
        "current_org": "玉溪市江川区人民代表大会常务委员会",
        "source": "https://www.ynjc.gov.cn/jc/jcdt79/20260717/1671477.html",
    },
    {
        "id": 19,
        "name": "陈挺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "玉溪市江川区政协主席",
        "current_org": "中国人民政治协商会议玉溪市江川区委员会",
        "source": "https://www.ynjc.gov.cn/jc/jcdt79/20260717/1671477.html",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共玉溪市江川区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共玉溪市委员会",
        "location": "云南省玉溪市江川区",
    },
    {
        "id": 2,
        "name": "玉溪市江川区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "玉溪市人民政府",
        "location": "云南省玉溪市江川区",
    },
    {
        "id": 3,
        "name": "玉溪市江川区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "玉溪市人大常委会",
        "location": "云南省玉溪市江川区",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议玉溪市江川区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "玉溪市政协",
        "location": "云南省玉溪市江川区",
    },
    {
        "id": 5,
        "name": "中共玉溪市江川区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共玉溪市纪律检查委员会",
        "location": "云南省玉溪市江川区",
    },
    {
        "id": 6,
        "name": "玉溪市江川区人民武装部",
        "type": "党委",
        "level": "县处级",
        "parent": "玉溪军分区",
        "location": "云南省玉溪市江川区",
    },
    {
        "id": 7,
        "name": "中共玉溪市江川区委员会组织部",
        "type": "党委",
        "level": "正科级",
        "parent": "中共玉溪市江川区委员会",
        "location": "云南省玉溪市江川区",
    },
]

positions = [
    # 王晋 - Party Secretary
    {"person_id": 1, "org_id": 1, "title": "玉溪市江川区委书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "2026年6月当选为江川区第四次党代会区委书记"},
    # 李金 - District Mayor
    {"person_id": 2, "org_id": 1, "title": "玉溪市江川区委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 2, "org_id": 2, "title": "玉溪市江川区区长",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "区政府党组书记"},
    # 杨雪彬 - Deputy Party Secretary
    {"person_id": 3, "org_id": 1, "title": "玉溪市江川区委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    # 汪涉源 - Standing Committee, Armed Forces
    {"person_id": 4, "org_id": 1, "title": "江川区委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 4, "org_id": 6, "title": "玉溪市江川区人武部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "上校军衔"},
    # 杨刚 - Organization Department
    {"person_id": 5, "org_id": 1, "title": "江川区委常委、组织部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    # 普超 - Standing Committee
    {"person_id": 6, "org_id": 1, "title": "江川区委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "具体职务待确认"},
    # 莽嘉慧 - District leader
    {"person_id": 7, "org_id": 2, "title": "江川区领导",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "具体职务待确认"},
    # Other Standing Committee
    {"person_id": 8, "org_id": 1, "title": "江川区委领导",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "区第四次党代会主席团成员"},
    {"person_id": 9, "org_id": 1, "title": "江川区委领导",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "区第四次党代会主席团成员"},
    {"person_id": 10, "org_id": 1, "title": "江川区委领导",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "区第四次党代会主席团成员"},
    {"person_id": 11, "org_id": 1, "title": "江川区委领导",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "区第四次党代会主席团成员"},
    {"person_id": 12, "org_id": 1, "title": "江川区委领导",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "区第四次党代会主席团成员"},
    {"person_id": 13, "org_id": 1, "title": "江川区委领导",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "区第四次党代会主席团成员"},
    {"person_id": 14, "org_id": 1, "title": "江川区委领导",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "区第四次党代会主席团成员"},
    {"person_id": 15, "org_id": 1, "title": "江川区委领导",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "区第四次党代会主席团成员"},
    {"person_id": 16, "org_id": 1, "title": "江川区委领导",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "区第四次党代会主席团成员"},
    {"person_id": 17, "org_id": 1, "title": "江川区委领导",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "区第四次党代会主席团成员"},
    # 杨辉 - People's Congress
    {"person_id": 18, "org_id": 3, "title": "江川区人大常委会主任",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": ""},
    # 陈挺 - Political Consultative Conference
    {"person_id": 19, "org_id": 4, "title": "江川区政协主席",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": ""},
]

relationships = [
    # Top leadership pair: Party Secretary + Mayor
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "王晋（区委书记）与李金（区长）为江川区党政主要领导搭档",
     "overlap_org": "中共玉溪市江川区委员会/玉溪市江川区人民政府",
     "overlap_period": "2026-至今"},
    # Party Secretary + Deputy Secretary
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "杨雪彬任区委副书记，协助王晋工作",
     "overlap_org": "中共玉溪市江川区委员会",
     "overlap_period": "2026-至今"},
    # Party Secretary + Organization Department Head
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "杨刚任区委组织部部长，王晋为区委书记",
     "overlap_org": "中共玉溪市江川区委员会",
     "overlap_period": "2026-至今"},
    # Party Secretary + Armed Forces
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "王晋兼任区人武部党委第一书记，汪涉源为人武部部长",
     "overlap_org": "玉溪市江川区人民武装部",
     "overlap_period": "2026-至今"},
    # Mayor + Party Congress attendance
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "李金、杨雪彬均为区委副书记，共同出席区第四次党代会",
     "overlap_org": "中共玉溪市江川区委员会",
     "overlap_period": "2026"},
]

# ── BUILD ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print(f"Building 江川区 network data")
    print(f"Database: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print("=" * 60)

    run_build(
        slug="江川区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    # Verify
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    for table in ("persons", "organizations", "positions", "relationships"):
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {count} rows")
    conn.close()

    gexf_size = os.path.getsize(GEXF_PATH)
    print(f"  GEXF: {gexf_size} bytes")
    print("Done.")