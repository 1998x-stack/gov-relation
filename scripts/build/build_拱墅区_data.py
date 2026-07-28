#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Gongshu District (拱墅区), Hangzhou, Zhejiang.

Researched 2026-07-28.
Confirmed data: 敖煜新 (Ao Yuxin) complete career from Baidu Baike.
Partial data: deputy positions from gov website snippets.
Gaps marked in comments.
"""

import sqlite3
import sys
import os
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "拱墅区"
TODAY = "20260728"

# ── PERSONS ────────────────────────────────────────────────────────────

persons = [
    # ═══ Current Top Leaders ═══
    {
        "id": 1,
        "name": "敖煜新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-09",
        "birthplace": "浙江长兴",
        "education": "浙江省委党校研究生",
        "party_join": "2000-10",
        "work_start": "1996-08",
        "current_post": "杭州市拱墅区委书记",
        "current_org": "中共杭州市拱墅区委员会",
        "source": "https://baike.baidu.com/item/%E6%95%96%E7%85%9C%E6%96%B0",
    },
    {
        "id": 2,
        "name": "待确认-拱墅区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "拱墅区委副书记、区长",
        "current_org": "杭州市拱墅区人民政府",
        "source": "待查",
    },
    {
        "id": 3,
        "name": "李志龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-00",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原拱墅区委书记（2024卸任）",
        "current_org": "",
        "source": "https://baike.baidu.com/item/%E6%9D%8E%E5%BF%97%E9%BE%99",
    },

    # ═══ Standing Committee Members ═══
    {
        "id": 4,
        "name": "许雷挺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-03",
        "birthplace": "",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "拱墅区委常委、区政府党组成员",
        "current_org": "中共杭州市拱墅区委员会",
        "source": "https://www.gongshu.gov.cn （搜狗搜索结果片段）",
    },
    {
        "id": 5,
        "name": "待确认-常务副区长",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-00",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "拱墅区委常委、常务副区长",
        "current_org": "杭州市拱墅区人民政府",
        "source": "https://www.gongshu.gov.cn （搜狗搜索结果片段）",
    },
    {
        "id": 6,
        "name": "待确认-组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "拱墅区委常委、组织部部长",
        "current_org": "中共杭州市拱墅区委员会",
        "source": "https://www.gongshu.gov.cn （搜狗搜索结果片段）",
    },
    {
        "id": 7,
        "name": "待确认-纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "拱墅区委常委、区纪委书记/监委主任",
        "current_org": "中共杭州市拱墅区纪律检查委员会",
        "source": "待查",
    },
    {
        "id": 8,
        "name": "待确认-宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "拱墅区委常委、宣传部部长",
        "current_org": "中共杭州市拱墅区委员会",
        "source": "待查",
    },
    {
        "id": 9,
        "name": "待确认-统战部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "拱墅区委常委、统战部部长",
        "current_org": "中共杭州市拱墅区委员会",
        "source": "待查",
    },

    # ═══ Key historical connections from Ao Yuxin's career ═══
    {
        "id": 10,
        "name": "鲍一飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "拱墅区第一届人大常委会主任",
        "current_org": "拱墅区人民代表大会常务委员会",
        "source": "https://baike.baidu.com/item/%E6%95%96%E7%85%9C%E6%96%B0 (reference [15])",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共杭州市拱墅区委员会", "type": "党委", "level": "县处级",
     "parent": "中共杭州市委员会", "location": "浙江省杭州市拱墅区"},
    {"id": 2, "name": "杭州市拱墅区人民政府", "type": "政府", "level": "县处级",
     "parent": "杭州市人民政府", "location": "浙江省杭州市拱墅区"},
    {"id": 3, "name": "拱墅区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "杭州市人大常委会", "location": "浙江省杭州市拱墅区"},
    {"id": 4, "name": "政协杭州市拱墅区委员会", "type": "政协", "level": "县处级",
     "parent": "杭州市政协", "location": "浙江省杭州市拱墅区"},
    {"id": 5, "name": "中共德清县委员会", "type": "党委", "level": "县处级",
     "parent": "中共湖州市委员会", "location": "浙江省湖州市德清县"},
    {"id": 6, "name": "德清县人民政府", "type": "政府", "level": "县处级",
     "parent": "湖州市人民政府", "location": "浙江省湖州市德清县"},
    {"id": 7, "name": "中共湖州市委员会", "type": "党委", "level": "地厅级",
     "parent": "", "location": "浙江省湖州市"},
    {"id": 8, "name": "湖州莫干山高新技术产业开发区管委会", "type": "开发区", "level": "县处级",
     "parent": "", "location": "浙江省湖州市德清县"},
    {"id": 9, "name": "中共杭州市拱墅区纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共杭州市纪律检查委员会", "location": "浙江省杭州市拱墅区"},
]

# ── POSITIONS ──────────────────────────────────────────────────────────

positions = [
    # 敖煜新 career timeline
    {"person_id": 1, "org_id": 5, "title": "德清县委书记", "start": "2021-02", "end": "2024-04", "rank": "正处级",
     "note": "同时继续担任县长至2021.02"},
    {"person_id": 1, "org_id": 6, "title": "德清县县长", "start": "2018-09", "end": "2021-02", "rank": "正处级",
     "note": "兼湖州莫干山高新区管委会主任"},
    {"person_id": 1, "org_id": 5, "title": "德清县委副书记", "start": "2016-12", "end": "2018-09", "rank": "副处级",
     "note": "兼任政法委书记"},
    {"person_id": 1, "org_id": 5, "title": "德清县委常委、组织部部长", "start": "2015-10", "end": "2016-11", "rank": "副处级",
     "note": "兼任县委党校校长2016.03-2016.11"},
    {"person_id": 1, "org_id": 5, "title": "德清县委常委、副县长（挂职）", "start": "2014-08", "end": "2015-10", "rank": "副处级",
     "note": "湖州市委副秘书长同时"},
    {"person_id": 1, "org_id": 7, "title": "湖州市委办公室副主任", "start": "2010-12", "end": "2014-06", "rank": "副处级",
     "note": "浙江省委党校在职研究生 2010-2013"},
    {"person_id": 1, "org_id": 7, "title": "湖州市委办公室调研处处长", "start": "2007-03", "end": "2010-12", "rank": "正科级",
     "note": ""},
    {"person_id": 1, "org_id": 7, "title": "湖州市委办公室综合一处副处长", "start": "2005-08", "end": "2007-03", "rank": "副科级",
     "note": ""},
    {"person_id": 1, "org_id": 7, "title": "湖州市委党史研究室党史编研处副处长", "start": "2005-01", "end": "2005-08", "rank": "副科级",
     "note": ""},
    {"person_id": 1, "org_id": 7, "title": "湖州市委宣传部宣传科科员", "start": "1997-08", "end": "2003-05", "rank": "科员",
     "note": "其间1998-2001在湖州市深化企业改革办公室工作"},
    # Ao Yuxin transition to Hangzhou
    {"person_id": 1, "org_id": 1, "title": "拱墅区委书记", "start": "2026-01", "end": "", "rank": "副厅级",
     "note": "杭州市拱墅区为副厅级架构"},
    {"person_id": 1, "org_id": 2, "title": "拱墅区委副书记、区长", "start": "2025-05", "end": "2026-01", "rank": "副厅级",
     "note": "2025.05.30当选区长"},
    {"person_id": 1, "org_id": 2, "title": "拱墅区委副书记、代区长", "start": "2024-04", "end": "2025-05", "rank": "副厅级",
     "note": "跨市从德清县调任杭州拱墅区"},

    # 李志龙 (predecessor)
    {"person_id": 3, "org_id": 1, "title": "拱墅区委书记", "start": "~2020", "end": "2024-04", "rank": "副厅级",
     "note": "前任拱墅区委书记，2024年4月卸任。具体去向待确认。"},

    # 许雷挺
    {"person_id": 4, "org_id": 1, "title": "拱墅区委常委", "start": "2025-11", "end": "", "rank": "副处级",
     "note": "区政府党组成员"},
    {"person_id": 4, "org_id": 2, "title": "拱墅区政府党组成员", "start": "2025-11", "end": "", "rank": "副处级",
     "note": ""},

    # 鲍一飞 (人大常委会主任)
    {"person_id": 10, "org_id": 3, "title": "拱墅区人大常委会主任", "start": "2025-05", "end": "", "rank": "正处级",
     "note": "2025.05.30与敖煜新同日由区人大选举产生"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────────

relationships = [
    # 敖煜新 ↔ 鲍一飞 (同时当选区长和人大主任)
    {"person_a": 1, "person_b": 10, "type": "colleague", "context": "2025年5月区人大会同时当选区长和人大主任",
     "overlap_org": "杭州市拱墅区", "overlap_period": "2025-05"},
    # 敖煜新 ↔ 李志龙 (前后任区委书记)
    {"person_a": 1, "person_b": 3, "type": "successor", "context": "接替李志龙任拱墅区委书记",
     "overlap_org": "中共杭州市拱墅区委员会", "overlap_period": ""},
]

# ── RUN BUILD ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DATABASE_DIR / f"{SLUG}_network.db",
        gexf_path=GRAPH_DIR / f"{SLUG}_network.gexf",
        overwrite=True,
    )
    print(f"Done. Built database and GEXF for {SLUG}.")
    print("GAPS: 区长姓名（敖煜新升书记后的继任者）、常务副区长姓名、组织部长姓名、")
    print("纪委书记姓名、宣传部长姓名、统战部长姓名、李志龙完整去向")
