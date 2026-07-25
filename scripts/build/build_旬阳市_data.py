#!/usr/bin/env python3
"""Build script for 旬阳市 (安康市, 陕西省) government network.

Xunyang City - county-level city under Ankang City, Shaanxi Province.
Formerly 旬阳县 (Xunyang County), upgraded to county-level city in 2021.

Research date: 2026-07-25
Official website: https://www.xyx.gov.cn/ (NOT www.xunyang.gov.cn which is Jiangxi 浔阳区)

Confirmed sources:
  - https://www.xyx.gov.cn/Content-1248479.html (陈红星 profile)
  - https://www.xyx.gov.cn/Content-2838811.html (郭国安 profile)
  - https://www.xyx.gov.cn/Content-2315113.html (常彬 profile)
  - https://www.xyx.gov.cn/ (领导之窗 page)
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

STAGING_DIR = Path(__file__).resolve().parent
REPO_ROOT = STAGING_DIR.parents[2]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.gexf import GEXFBuilder
from gov_relation.schema import create_tables, insert_organizations, insert_persons, insert_positions, insert_relationships

SLUG = "旬阳市"
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

PERSONS = [
    # ── Current leadership: 市委书记 & 市长 ──
    {"id": 1, "name": "陈红星", "gender": "男", "ethnicity": "汉族",
     "birth": "1970年10月", "birthplace": "陕西岚皋",
     "education": "研究生学历", "party_join": "1995年7月", "work_start": "1990年7月",
     "current_post": "旬阳市委书记", "current_org": "中共旬阳市委员会",
     "source": "https://www.xyx.gov.cn/Content-1248479.html"},

    {"id": 2, "name": "郭国安", "gender": "男", "ethnicity": "汉族",
     "birth": "1977年12月", "birthplace": "陕西岚皋",
     "education": "在职研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "旬阳市委副书记、市长", "current_org": "旬阳市人民政府",
     "source": "https://www.xyx.gov.cn/Content-2838811.html"},

    # ── 市委领导班子 ──
    {"id": 3, "name": "常彬", "gender": "男", "ethnicity": "汉族",
     "birth": "1976年1月", "birthplace": "",
     "education": "在职大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "旬阳市委副书记、市委党校校长", "current_org": "中共旬阳市委员会",
     "source": "https://www.xyx.gov.cn/Content-2315113.html"},

    # ── 市纪委监委 ──
    {"id": 4, "name": "待确认_纪委书记", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "旬阳市委常委、纪委书记、监委主任",
     "current_org": "中共旬阳市纪律检查委员会",
     "source": "待确认 — 需从旬阳市官方网站领导之窗页面核实"},

    # ── 市政府领导班子 ──
    {"id": 5, "name": "待确认_常务副市长", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "旬阳市委常委、常务副市长", "current_org": "旬阳市人民政府",
     "source": "待确认"},

    {"id": 6, "name": "待确认_组织部部长", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "旬阳市委常委、组织部部长", "current_org": "中共旬阳市委员会",
     "source": "待确认"},

    {"id": 7, "name": "待确认_宣传部部长", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "旬阳市委常委、宣传部部长", "current_org": "中共旬阳市委员会",
     "source": "待确认"},

    {"id": 8, "name": "待确认_政法委书记", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "旬阳市委常委、政法委书记", "current_org": "中共旬阳市委员会",
     "source": "待确认"},

    {"id": 9, "name": "待确认_统战部部长", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "旬阳市委常委、统战部部长", "current_org": "中共旬阳市委员会",
     "source": "待确认"},

    # ── 人大 ──
    {"id": 10, "name": "王武臣", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "旬阳市人大常委会主任", "current_org": "旬阳市人民代表大会常务委员会",
     "source": "https://www.xyx.gov.cn/ (领导之窗)"},

    # ── 政协 ──
    {"id": 11, "name": "曾炜", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "政协旬阳市委员会主席", "current_org": "政协旬阳市委员会",
     "source": "https://www.xyx.gov.cn/ (领导之窗)"},
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共旬阳市委员会", "type": "党委", "level": "县处级", "parent": "中共安康市委", "location": "陕西省安康市旬阳市"},
    {"id": 2, "name": "旬阳市人民政府", "type": "政府", "level": "县处级", "parent": "安康市人民政府", "location": "陕西省安康市旬阳市"},
    {"id": 3, "name": "中共旬阳市纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共安康市纪委", "location": "陕西省安康市旬阳市"},
    {"id": 4, "name": "旬阳市人民武装部", "type": "军队", "level": "县处级", "parent": "安康军分区", "location": "陕西省安康市旬阳市"},
    {"id": 5, "name": "旬阳市人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "安康市人大常委会", "location": "陕西省安康市旬阳市"},
    {"id": 6, "name": "政协旬阳市委员会", "type": "政协", "level": "县处级", "parent": "政协安康市委员会", "location": "陕西省安康市旬阳市"},
    {"id": 7, "name": "旬阳市公安局", "type": "政府", "level": "正科级", "parent": "旬阳市人民政府", "location": "陕西省安康市旬阳市"},
    {"id": 8, "name": "中共安康市委", "type": "党委", "level": "地厅级", "parent": "中共陕西省委", "location": "陕西省安康市"},
    {"id": 9, "name": "安康市人民政府", "type": "政府", "level": "地厅级", "parent": "陕西省人民政府", "location": "陕西省安康市"},
    {"id": 10, "name": "政协安康市委员会", "type": "政协", "level": "地厅级", "parent": "政协陕西省委员会", "location": "陕西省安康市"},
]

POSITIONS = [
    # 市委
    {"person_id": 1, "org_id": 1, "title": "旬阳市委书记", "start_date": "2021-08", "end_date": "present", "rank": "正处级", "note": "2021年撤县设市后任市委书记。此前2014年11月任旬阳县委副书记、代县长、县长"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持市政府全面工作"},
    {"person_id": 3, "org_id": 1, "title": "市委副书记、市委党校校长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "市纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "市委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "市委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "市委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 陈红星 更早职务
    {"person_id": 1, "org_id": 2, "title": "旬阳县委副书记、代县长、县长", "start_date": "2014-11", "end_date": "2021-08", "rank": "正处级", "note": "撤县设市前"},
    # 郭国安 来旬阳前部分履历
    {"person_id": 2, "org_id": 8, "title": "安康市委社会工作部部长、市委非公有制经济组织和社会组织工作委员会书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "调任旬阳前任"},
    {"person_id": 2, "org_id": 9, "title": "安康市政府副秘书长、市信访局党组书记、局长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 市政府
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持市政府全面工作，分管市财政局、市审计局"},
    {"person_id": 5, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 人大
    {"person_id": 10, "org_id": 5, "title": "市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 政协
    {"person_id": 11, "org_id": 6, "title": "市政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 陈红星 — 安康市政协副主席（兼任，确认来源见安康官网）
    {"person_id": 1, "org_id": 10, "title": "安康市政协副主席（兼任）", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "安康市政协官网领导名单"},
]

RELATIONSHIPS = [
    # 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "市委书记陈红星与市长郭国安党政主要领导搭档", "overlap_org": "中共旬阳市委员会/旬阳市人民政府", "overlap_period": ""},

    # 市委书记与专职副书记
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "市委书记陈红星与专职副书记常彬", "overlap_org": "中共旬阳市委员会", "overlap_period": ""},

    # 市委书记与各常委（均为待确认）
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "市委书记与纪委书记", "overlap_org": "中共旬阳市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "市委书记与常务副市长", "overlap_org": "中共旬阳市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "市委书记与组织部部长", "overlap_org": "中共旬阳市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "市委书记与宣传部部长", "overlap_org": "中共旬阳市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "市委书记与政法委书记", "overlap_org": "中共旬阳市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "市委书记与统战部部长", "overlap_org": "中共旬阳市委员会", "overlap_period": ""},

    # 市长与副市长
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "市长与常务副市长（政府领导班子）", "overlap_org": "旬阳市人民政府", "overlap_period": ""},

    # 市委书记与人大、政协
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "市委书记陈红星与人大常委会主任王武臣", "overlap_org": "旬阳市", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "市委书记陈红星与政协主席曾炜", "overlap_org": "旬阳市", "overlap_period": ""},

    # 共同背景：陈红星与郭国安均为陕西岚皋籍
    {"person_a": 1, "person_b": 2, "type": "same_native_place", "context": "陈红星（岚皋）与郭国安（岚皋）均为岚皋籍干部", "overlap_org": "安康市岚皋县", "overlap_period": "", "strength": "weak"},
]


def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    GEXF_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    try:
        create_tables(conn, overwrite=True)
        insert_persons(conn, PERSONS)
        insert_organizations(conn, ORGANIZATIONS)
        insert_positions(conn, POSITIONS)
        insert_relationships(conn, RELATIONSHIPS)
        print(f"DB ready: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(POSITIONS)} positions, {len(RELATIONSHIPS)} relationships")
    finally:
        conn.close()

    builder = GEXFBuilder(title=SLUG)
    for p in PERSONS:
        builder.add_person(
            id=p["id"], name=p.get("name", ""),
            current_post=p.get("current_post", ""),
            current_org=p.get("current_org", ""),
            gender=p.get("gender", ""),
            ethnicity=p.get("ethnicity", ""),
            birth=p.get("birth", ""),
            source=p.get("source", "")
        )
    for o in ORGANIZATIONS:
        builder.add_organization(
            id=o["id"] + 100000, name=o.get("name", ""),
            org_type=o.get("type", ""), level=o.get("level", ""),
            location=o.get("location", "")
        )
    for r in RELATIONSHIPS:
        builder.add_relationship(
            source=r["person_a"], target=r["person_b"],
            rel_type=r.get("type", ""), context=r.get("context", ""),
            overlap_org=r.get("overlap_org", ""),
            overlap_period=r.get("overlap_period", "")
        )
    builder.write(GEXF_PATH)
    print(f"GEXF ready: {GEXF_PATH}")
    print(f"Done: {DB_PATH}, {GEXF_PATH}")


if __name__ == "__main__":
    main()
