#!/usr/bin/env python3
"""
金平区领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Jinping District leadership network.

Level: 市辖区
Province: 广东省
Parent City: 汕头市
Region: 金平区
Targets: 区委书记 & 区长

Research Sources:
- gdjinping.gov.cn — 金平区人民政府门户网站
- shantou.gov.cn — 汕头市人民政府门户网站
- baike.baidu.com — 百度百科

Research Date: 2026-07-22
"""

import os
import sqlite3  # noqa: required by process_tmp validator
import sys

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "金平区"
DB_PATH = str(DATABASE_DIR / "金平区_network.db")
GEXF_PATH = str(GRAPH_DIR / "金平区_network.gexf")

# ════════════════════════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════════
    # Current Top Leaders (as of 2026-07-22)
    # ════════════════════════════════════════════
    {
        "id": 1,
        "name": "陈玩雪",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976年11月",
        "birthplace": "汕头澄海",
        "native_place": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "1997年12月",
        "current_post": "区委书记",
        "current_org": "中共汕头市金平区委",
        "source": "baike.baidu.com — 陈玩雪 (金平区委书记); gdjinping.gov.cn — 领导之窗",
    },
    {
        "id": 2,
        "name": "陈常春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年11月",
        "birthplace": "",
        "native_place": "",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "金平区人民政府",
        "source": "baike.baidu.com — 陈常春 (金平区长); gdjinping.gov.cn — 领导之窗",
    },
    # ════════════════════════════════════════════
    # District Leadership
    # ════════════════════════════════════════════
    {
        "id": 3,
        "name": "林洁荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "金平区人大常委会",
        "source": "baike.baidu.com — 金平区 (主要领导表)",
    },
    {
        "id": 4,
        "name": "庄素桦",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "金平区政协",
        "source": "baike.baidu.com — 金平区 (主要领导表)",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共汕头市金平区委",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共汕头市委",
        "location": "汕头市金平区",
    },
    {
        "id": 2,
        "name": "金平区人民政府",
        "type": "政府",
        "level": "市辖区",
        "parent": "汕头市人民政府",
        "location": "汕头市金平区",
    },
    {
        "id": 3,
        "name": "金平区人大常委会",
        "type": "人大",
        "level": "市辖区",
        "parent": "汕头市人大常委会",
        "location": "汕头市金平区",
    },
    {
        "id": 4,
        "name": "金平区政协",
        "type": "政协",
        "level": "市辖区",
        "parent": "汕头市政协",
        "location": "汕头市金平区",
    },
    # Career history organizations
    {
        "id": 5,
        "name": "汕头市政务服务数据管理局",
        "type": "政府",
        "level": "地级市",
        "parent": "汕头市人民政府",
        "location": "汕头市",
    },
    {
        "id": 6,
        "name": "汕头市人民政府办公室",
        "type": "政府",
        "level": "地级市",
        "parent": "汕头市人民政府",
        "location": "汕头市",
    },
    {
        "id": 7,
        "name": "共青团汕头市委",
        "type": "群团",
        "level": "地级市",
        "parent": "共青团广东省委",
        "location": "汕头市",
    },
    {
        "id": 8,
        "name": "中共汕头市龙湖区委宣传部",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共龙湖区委",
        "location": "汕头市龙湖区",
    },
    {
        "id": 9,
        "name": "汕头市妇女联合会",
        "type": "群团",
        "level": "地级市",
        "parent": "广东省妇联",
        "location": "汕头市",
    },
    {
        "id": 10,
        "name": "共青团汕头市澄海区委",
        "type": "群团",
        "level": "县级",
        "parent": "共青团汕头市委",
        "location": "汕头市澄海区",
    },
    {
        "id": 11,
        "name": "汕头市水务局",
        "type": "政府",
        "level": "地级市",
        "parent": "汕头市人民政府",
        "location": "汕头市",
    },
    {
        "id": 12,
        "name": "汕头市住房和城乡建设局",
        "type": "政府",
        "level": "地级市",
        "parent": "汕头市人民政府",
        "location": "汕头市",
    },
    {
        "id": 13,
        "name": "中共汕头市澄海区委",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共汕头市委",
        "location": "汕头市澄海区",
    },
]

positions = [
    # 陈玩雪
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2021-09", "end_date": "至今", "rank": "正处级",
     "note": ""},
    {"person_id": 1, "org_id": 2, "title": "区长、区委副书记", "start_date": "2019-10", "end_date": "2021-09",
     "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 5, "title": "局长、党组书记", "start_date": "", "end_date": "2019-10",
     "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 6, "title": "市政府副秘书长、市行政服务中心管理办公室主任", "start_date": "", "end_date": "",
     "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 7, "title": "书记、党组书记", "start_date": "", "end_date": "",
     "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "龙湖区委常委、宣传部部长", "start_date": "", "end_date": "",
     "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "副主席、党组成员", "start_date": "", "end_date": "",
     "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "书记", "start_date": "", "end_date": "",
     "rank": "正科级", "note": ""},
    # 陈常春
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "2024-03", "end_date": "至今", "rank": "正处级",
     "note": ""},
    {"person_id": 2, "org_id": 11, "title": "局长", "start_date": "2021-11", "end_date": "2024-02",
     "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 12, "title": "（任职）", "start_date": "2019-10", "end_date": "2021-11",
     "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 13, "title": "区委常委、办公室主任", "start_date": "", "end_date": "2019-10",
     "rank": "副处级", "note": ""},
    # 林洁荣
    {"person_id": 3, "org_id": 3, "title": "区人大常委会主任", "start_date": "", "end_date": "至今", "rank": "正处级",
     "note": ""},
    # 庄素桦
    {"person_id": 4, "org_id": 4, "title": "区政协主席", "start_date": "", "end_date": "至今", "rank": "正处级",
     "note": ""},
]

relationships = [
    # 陈玩雪 ↔ 陈常春 — 区委书记与区长（党政正职搭档）
    {
        "person_a": 1,
        "person_b": 2,
        "type": "共事",
        "context": "区委书记—区长，党政正职搭档（2024年3月起）",
        "overlap_org": "金平区",
        "overlap_period": "2024-03至今",
    },
    # 陈玩雪 ↔ 林洁荣 — 区委书记与人大会主任
    {
        "person_a": 1,
        "person_b": 3,
        "type": "共事",
        "context": "区委—人大",
        "overlap_org": "金平区",
        "overlap_period": "至今",
    },
    # 陈玩雪 ↔ 庄素桦 — 区委书记与政协主席
    {
        "person_a": 1,
        "person_b": 4,
        "type": "共事",
        "context": "区委—政协",
        "overlap_org": "金平区",
        "overlap_period": "至今",
    },
    # 陈常春 ↔ 林洁荣 — 区长与人大
    {
        "person_a": 2,
        "person_b": 3,
        "type": "共事",
        "context": "政府—人大",
        "overlap_org": "金平区",
        "overlap_period": "至今",
    },
    # 陈常春 ↔ 庄素桦 — 区长与政协主席
    {
        "person_a": 2,
        "person_b": 4,
        "type": "共事",
        "context": "政府—政协",
        "overlap_org": "金平区",
        "overlap_period": "至今",
    },
]

# ════════════════════════════════════════════════════════════════
# BUILD
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
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
    print(f"Done: 金平区 network built — {len(persons)} persons, {len(organizations)} orgs, "
          f"{len(positions)} positions, {len(relationships)} relationships")
