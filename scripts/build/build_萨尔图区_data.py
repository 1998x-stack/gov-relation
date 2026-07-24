#!/usr/bin/env python3
"""
萨尔图区（黑龙江省大庆市）领导班子工作关系网络 — 2026-07-24
Build script for Sartu District, Daqing City, Heilongjiang Province.

Data sources:
- 萨尔图区人民政府官网 http://www.saertu.gov.cn/ — official leadership pages and news
- 维基百科 https://zh.wikipedia.org/wiki/萨尔图区 — confirms 区委书记 牛玉全
- News articles on saertu.gov.cn (2026-07) confirm 区长候选人 杨建华

TASK: heilongjiang_萨尔图区

Note: 牛玉全 (区委书记) and 杨建华 (区委副书记、区长候选人) are the current
core leadership duo as of July 2026. The 区长 position was previously vacant
(acted by 区委常委、副区长 王营) until 杨建华's appointment as candidate.
Biographical details beyond official titles remain limited.
"""

import json
import os
import sqlite3  # noqa: used via gov_relation.runner
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

TODAY = "2026-07-24"
AS_OF = TODAY

# ── STAGING DIRECTORIES ──
STAGING = Path(__file__).resolve().parent
DB_PATH = STAGING / "萨尔图区_network.db"
GEXF_PATH = STAGING / "萨尔图区_network.gexf"
PERSONS_DIR = STAGING

# ── DATA ──

# Integer IDs mapped: 1=牛玉全, 2=杨建华, 3=王营, 4=于博天, 5=提常君,
# 6=梁云阁, 7=杨硕, 8=吴宝祥, 9=张万东, 10=杨子叶, 11=吕鹏,
# 12=耿志权, 13=金庆君, 14=文慧玲, 15=张景权
PERSON_ID_MAP = {
    "牛玉全": 1,
    "杨建华": 2,
    "王营": 3,
    "于博天": 4,
    "提常君": 5,
    "梁云阁": 6,
    "杨硕": 7,
    "吴宝祥": 8,
    "张万东": 9,
    "杨子叶": 10,
    "吕鹏": 11,
    "耿志权": 12,
    "金庆君": 13,
    "文慧玲": 14,
    "张景权": 15,
}

ORG_ID_MAP = {
    "中共萨尔图区委员会": 1,
    "萨尔图区人民政府": 2,
    "萨尔图区人大常委会": 3,
    "萨尔图区政协": 4,
    "萨尔图区纪委监委": 5,
    "萨尔图区委组织部": 6,
    "萨尔图区委宣传部": 7,
    "萨尔图区委统战部": 8,
    "萨尔图区人民武装部": 9,
}

persons = [
    {
        "id": 1,
        "name": "牛玉全",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萨尔图区委书记",
        "current_org": "中共萨尔图区委员会",
        "source": "萨尔图区人民政府官网领导信息 (2026-07-24)",
    },
    {
        "id": 2,
        "name": "杨建华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萨尔图区委副书记、区长候选人",
        "current_org": "萨尔图区人民政府",
        "source": "萨尔图区人民政府官网新闻 '区政府召开第二季度安全生产工作例会' (2026-07-22)",
    },
    {
        "id": 3,
        "name": "王营",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萨尔图区委常委、副区长",
        "current_org": "萨尔图区人民政府",
        "source": "萨尔图区人民政府官网领导信息 (2026-07-24)",
    },
    {
        "id": 4,
        "name": "于博天",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萨尔图区委副书记（挂职）",
        "current_org": "中共萨尔图区委员会",
        "source": "萨尔图区人民政府官网领导信息 (2026-07-24)",
    },
    {
        "id": 5,
        "name": "提常君",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萨尔图区委副书记",
        "current_org": "中共萨尔图区委员会",
        "source": "萨尔图区人民政府官网领导信息 (2026-07-24)",
    },
    {
        "id": 6,
        "name": "梁云阁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萨尔图区委常委、组织部部长",
        "current_org": "萨尔图区委组织部",
        "source": "萨尔图区人民政府官网领导信息 (2026-07-24)",
    },
    {
        "id": 7,
        "name": "杨硕",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萨尔图区委常委、纪委书记、监委主任",
        "current_org": "萨尔图区纪委监委",
        "source": "萨尔图区人民政府官网领导信息 (2026-07-24)",
    },
    {
        "id": 8,
        "name": "吴宝祥",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萨尔图区委常委、宣传部部长、统战部部长",
        "current_org": "萨尔图区委宣传部",
        "source": "萨尔图区人民政府官网领导信息 (2026-07-24)",
    },
    {
        "id": 9,
        "name": "张万东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萨尔图区委常委、人民武装部政治委员",
        "current_org": "萨尔图区人民武装部",
        "source": "萨尔图区人民政府官网领导信息 (2026-07-24)",
    },
    {
        "id": 10,
        "name": "杨子叶",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萨尔图区政府副区长",
        "current_org": "萨尔图区人民政府",
        "source": "萨尔图区人民政府官网领导信息 (2026-07-24)",
    },
    {
        "id": 11,
        "name": "吕鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萨尔图区政府副区长",
        "current_org": "萨尔图区人民政府",
        "source": "萨尔图区人民政府官网领导信息 (2026-07-24)",
    },
    {
        "id": 12,
        "name": "耿志权",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萨尔图区政府副区长",
        "current_org": "萨尔图区人民政府",
        "source": "萨尔图区人民政府官网领导信息 (2026-07-24)",
    },
    {
        "id": 13,
        "name": "金庆君",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萨尔图区政府副区长",
        "current_org": "萨尔图区人民政府",
        "source": "萨尔图区人民政府官网领导信息 (2026-07-24)",
    },
    {
        "id": 14,
        "name": "文慧玲",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萨尔图区人大常委会主任",
        "current_org": "萨尔图区人大常委会",
        "source": "萨尔图区人民政府官网领导信息 (2026-07-24)",
    },
    {
        "id": 15,
        "name": "张景权",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萨尔图区政协主席",
        "current_org": "萨尔图区政协",
        "source": "萨尔图区人民政府官网领导信息 (2026-07-24)",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共萨尔图区委员会",
        "type": "党委",
        "level": "县处级",
        "location": "黑龙江省大庆市萨尔图区",
    },
    {
        "id": 2,
        "name": "萨尔图区人民政府",
        "type": "政府",
        "level": "县处级",
        "location": "黑龙江省大庆市萨尔图区",
    },
    {
        "id": 3,
        "name": "萨尔图区人大常委会",
        "type": "人大",
        "level": "县处级",
        "location": "黑龙江省大庆市萨尔图区",
    },
    {
        "id": 4,
        "name": "萨尔图区政协",
        "type": "政协",
        "level": "县处级",
        "location": "黑龙江省大庆市萨尔图区",
    },
    {
        "id": 5,
        "name": "萨尔图区纪委监委",
        "type": "党委",
        "level": "县处级",
        "location": "黑龙江省大庆市萨尔图区",
    },
    {
        "id": 6,
        "name": "萨尔图区委组织部",
        "type": "党委",
        "level": "县处级",
        "location": "黑龙江省大庆市萨尔图区",
    },
    {
        "id": 7,
        "name": "萨尔图区委宣传部",
        "type": "党委",
        "level": "县处级",
        "location": "黑龙江省大庆市萨尔图区",
    },
    {
        "id": 8,
        "name": "萨尔图区委统战部",
        "type": "党委",
        "level": "县处级",
        "location": "黑龙江省大庆市萨尔图区",
    },
    {
        "id": 9,
        "name": "萨尔图区人民武装部",
        "type": "党委",
        "level": "县处级",
        "location": "黑龙江省大庆市萨尔图区",
    },
]

positions = [
    # ── 牛玉全 ──
    {
        "person_id": 1,
        "org_id": 1,
        "title": "萨尔图区委书记",
        "start": "待查",
        "end": "present",
        "rank": "县处级正职",
        "note": "2026年7月仍任现职，主持区委全面工作",
    },
    # ── 杨建华 ──
    {
        "person_id": 2,
        "org_id": 2,
        "title": "萨尔图区委副书记、区长候选人",
        "start": "2026-07",
        "end": "present",
        "rank": "县处级正职",
        "note": "2026年7月以区委副书记、区长候选人身份主持区政府全面工作",
    },
    {
        "person_id": 2,
        "org_id": 1,
        "title": "萨尔图区委副书记",
        "start": "2026-07",
        "end": "present",
        "rank": "县处级副职",
        "note": "兼任区政府党组书记",
    },
    # ── 王营 ──
    {
        "person_id": 3,
        "org_id": 2,
        "title": "萨尔图区委常委、副区长",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "区长空缺期间（2026年上半年）主持区政府常务工作",
    },
    {
        "person_id": 3,
        "org_id": 1,
        "title": "萨尔图区委常委",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "区委领导班子成员",
    },
    # ── 于博天 ──
    {
        "person_id": 4,
        "org_id": 1,
        "title": "萨尔图区委副书记（挂职）",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "挂职干部",
    },
    # ── 提常君 ──
    {
        "person_id": 5,
        "org_id": 1,
        "title": "萨尔图区委副书记",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "专职副书记",
    },
    # ── 梁云阁 ──
    {
        "person_id": 6,
        "org_id": 6,
        "title": "萨尔图区委常委、组织部部长",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "主持区委组织部工作",
    },
    {
        "person_id": 6,
        "org_id": 1,
        "title": "萨尔图区委常委",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
    },
    # ── 杨硕 ──
    {
        "person_id": 7,
        "org_id": 5,
        "title": "萨尔图区委常委、纪委书记、监委主任",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "主持区纪委监委全面工作",
    },
    {
        "person_id": 7,
        "org_id": 1,
        "title": "萨尔图区委常委",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
    },
    # ── 吴宝祥 ──
    {
        "person_id": 8,
        "org_id": 7,
        "title": "萨尔图区委常委、宣传部部长",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "兼任统战部部长",
    },
    {
        "person_id": 8,
        "org_id": 8,
        "title": "萨尔图区委统战部部长",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
    },
    {
        "person_id": 8,
        "org_id": 1,
        "title": "萨尔图区委常委",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
    },
    # ── 张万东 ──
    {
        "person_id": 9,
        "org_id": 9,
        "title": "萨尔图区委常委、人民武装部政治委员",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "区人武部政委",
    },
    {
        "person_id": 9,
        "org_id": 1,
        "title": "萨尔图区委常委",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
    },
    # ── 杨子叶 ──
    {
        "person_id": 10,
        "org_id": 2,
        "title": "萨尔图区政府副区长",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
    },
    # ── 吕鹏 ──
    {
        "person_id": 11,
        "org_id": 2,
        "title": "萨尔图区政府副区长",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
    },
    # ── 耿志权 ──
    {
        "person_id": 12,
        "org_id": 2,
        "title": "萨尔图区政府副区长",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
    },
    # ── 金庆君 ──
    {
        "person_id": 13,
        "org_id": 2,
        "title": "萨尔图区政府副区长",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
    },
    # ── 文慧玲 ──
    {
        "person_id": 14,
        "org_id": 3,
        "title": "萨尔图区人大常委会主任",
        "start": "待查",
        "end": "present",
        "rank": "县处级正职",
        "note": "主持区人大常委会全面工作",
    },
    # ── 张景权 ──
    {
        "person_id": 15,
        "org_id": 4,
        "title": "萨尔图区政协主席",
        "start": "待查",
        "end": "present",
        "rank": "县处级正职",
        "note": "主持区政协全面工作",
    },
]

relationships = [
    # 党政搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "党政搭档",
        "context": "区委书记与区长（候选人）党政正职搭档关系",
        "overlap_org": "中共萨尔图区委员会/萨尔图区人民政府",
        "overlap_period": "2026年7月至今",
    },
    # 区委书记与副书记
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "区委书记与专职副书记",
        "overlap_org": "中共萨尔图区委员会",
        "overlap_period": "2026年",
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "区委书记与挂职副书记",
        "overlap_org": "中共萨尔图区委员会",
        "overlap_period": "2026年",
    },
    # 区委书记与区委常委
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "区委书记与组织部部长",
        "overlap_org": "中共萨尔图区委员会",
        "overlap_period": "2026年",
    },
    {
        "person_a": 1,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "区委书记与纪委书记",
        "overlap_org": "中共萨尔图区委员会",
        "overlap_period": "2026年",
    },
    {
        "person_a": 1,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "区委书记与宣传部部长",
        "overlap_org": "中共萨尔图区委员会",
        "overlap_period": "2026年",
    },
    # 区长候选人与副区长
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "区长候选人与常务副区长",
        "overlap_org": "萨尔图区人民政府",
        "overlap_period": "2026年7月至今",
    },
    {
        "person_a": 2,
        "person_b": 10,
        "type": "superior_subordinate",
        "context": "区长候选人与副区长",
        "overlap_org": "萨尔图区人民政府",
        "overlap_period": "2026年7月至今",
    },
    {
        "person_a": 2,
        "person_b": 11,
        "type": "superior_subordinate",
        "context": "区长候选人与副区长",
        "overlap_org": "萨尔图区人民政府",
        "overlap_period": "2026年7月至今",
    },
    {
        "person_a": 2,
        "person_b": 12,
        "type": "superior_subordinate",
        "context": "区长候选人与副区长",
        "overlap_org": "萨尔图区人民政府",
        "overlap_period": "2026年7月至今",
    },
    {
        "person_a": 2,
        "person_b": 13,
        "type": "superior_subordinate",
        "context": "区长候选人与副区长",
        "overlap_org": "萨尔图区人民政府",
        "overlap_period": "2026年7月至今",
    },
    # 区委常委同僚
    {
        "person_a": 3,
        "person_b": 6,
        "type": "同僚",
        "context": "同为区委常委",
        "overlap_org": "中共萨尔图区委员会",
        "overlap_period": "2026年",
    },
    {
        "person_a": 3,
        "person_b": 7,
        "type": "同僚",
        "context": "同为区委常委",
        "overlap_org": "中共萨尔图区委员会",
        "overlap_period": "2026年",
    },
    {
        "person_a": 3,
        "person_b": 8,
        "type": "同僚",
        "context": "同为区委常委",
        "overlap_org": "中共萨尔图区委员会",
        "overlap_period": "2026年",
    },
    {
        "person_a": 6,
        "person_b": 7,
        "type": "同僚",
        "context": "区委常委同僚",
        "overlap_org": "中共萨尔图区委员会",
        "overlap_period": "2026年",
    },
    # 政府副职同僚
    {
        "person_a": 10,
        "person_b": 11,
        "type": "同僚",
        "context": "同为区政府副区长",
        "overlap_org": "萨尔图区人民政府",
        "overlap_period": "2026年",
    },
    {
        "person_a": 10,
        "person_b": 12,
        "type": "同僚",
        "context": "同为区政府副区长",
        "overlap_org": "萨尔图区人民政府",
        "overlap_period": "2026年",
    },
    {
        "person_a": 10,
        "person_b": 13,
        "type": "同僚",
        "context": "同为区政府副区长",
        "overlap_org": "萨尔图区人民政府",
        "overlap_period": "2026年",
    },
    {
        "person_a": 11,
        "person_b": 12,
        "type": "同僚",
        "context": "同为区政府副区长",
        "overlap_org": "萨尔图区人民政府",
        "overlap_period": "2026年",
    },
    {
        "person_a": 11,
        "person_b": 13,
        "type": "同僚",
        "context": "同为区政府副区长",
        "overlap_org": "萨尔图区人民政府",
        "overlap_period": "2026年",
    },
    {
        "person_a": 12,
        "person_b": 13,
        "type": "同僚",
        "context": "同为区政府副区长",
        "overlap_org": "萨尔图区人民政府",
        "overlap_period": "2026年",
    },
]


def main():
    # Build DB and GEXF
    run_build(
        slug="萨尔图区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Print summary
    print(f"\nBuild complete: {TODAY}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")
    print(f"  Persons:  {len(persons)}")
    print(f"  Orgs:     {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print("\nNote: Biographical details limited due to web access constraints.")
    print("See open questions in person JSON files and report for gaps.")


if __name__ == "__main__":
    main()
