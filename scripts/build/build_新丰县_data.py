#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新丰县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 广东省
Parent City: 韶关市
Region: 新丰县
Targets: 县委书记 & 县长

Research Sources:
- 新丰县人民政府公众信息网 (www.xinfeng.gov.cn) — 政务要闻、常委会会议报道
- 维基百科 (zh.wikipedia.org) — 新丰县词条
- Web search degraded: Exa rate-limited, Baidu 403, Baidu Baike inaccessible via Jina
- See open_gaps for access constraints

Current status (as of 2026-07-22):
- 县委书记: 郑伟平（2026年6月/7月常委会会议确认在任）
- 县长: 侯新祥（2026年7月多篇报道确认在任，县委副书记、县长）
- Wikipedia 列出县长为区毅明（推测为前任，侯新祥为继任）

Research Date: 2026-07-22
Web Access Status: Degraded (Exa rate-limited, Baidu 403, gov site leadership page JS-rendered)
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../"))

from gov_relation.runner import run_build

SLUG = "新丰县"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

persons = [
    {
        "id": 1,
        "name": "郑伟平",
        "gender": "待查",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共新丰县委书记",
        "current_org": "中共新丰县委员会",
        "source": "新丰县政府网—常委会会议报道（2026年5月-7月多篇）"
    },
    {
        "id": 2,
        "name": "侯新祥",
        "gender": "男",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "新丰县委副书记、县长",
        "current_org": "新丰县人民政府",
        "source": "新丰县政府网—政务要闻（2026年7月多篇报道）"
    },
    {
        "id": 3,
        "name": "叶森林",
        "gender": "待查",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "新丰县委常委、组织部部长",
        "current_org": "中共新丰县委组织部",
        "source": "新丰县政府网—十四届十次全会报道"
    },
    {
        "id": 4,
        "name": "钟卫苏",
        "gender": "待查",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "新丰县委常委、宣传部部长",
        "current_org": "中共新丰县委宣传部",
        "source": "新丰县政府网—侯新祥调研报道"
    },
    {
        "id": 5,
        "name": "郑万龙",
        "gender": "待查",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "新丰县委常委、政法委书记",
        "current_org": "中共新丰县委政法委员会",
        "source": "新丰县政府网—县委理论学习中心组学习会报道"
    },
    {
        "id": 6,
        "name": "谢金宏",
        "gender": "待查",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "新丰县委常委、统战部部长",
        "current_org": "中共新丰县委统战部",
        "source": "新丰县政府网—县委理论学习中心组学习会报道"
    },
    {
        "id": 7,
        "name": "罗红誉",
        "gender": "待查",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "新丰县委常委、人武部政委",
        "current_org": "新丰县人民武装部",
        "source": "新丰县政府网—县委理论学习中心组学习会报道"
    },
    {
        "id": 8,
        "name": "区毅明",
        "gender": "待查",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（历任）新丰县县长",
        "current_org": "（历任）新丰县人民政府",
        "source": "维基百科—新丰县词条（县长字段）"
    },
]

organizations = [
    {"id": 1, "name": "中共新丰县委员会", "type": "党委", "level": "正处级", "parent": "中共韶关市委员会", "location": "韶关市新丰县"},
    {"id": 2, "name": "新丰县人民政府", "type": "政府", "level": "正处级", "parent": "韶关市人民政府", "location": "韶关市新丰县"},
    {"id": 3, "name": "中共新丰县委组织部", "type": "党委", "level": "正科级", "parent": "中共新丰县委员会", "location": "韶关市新丰县"},
    {"id": 4, "name": "中共新丰县委宣传部", "type": "党委", "level": "正科级", "parent": "中共新丰县委员会", "location": "韶关市新丰县"},
    {"id": 5, "name": "中共新丰县委政法委员会", "type": "党委", "level": "正科级", "parent": "中共新丰县委员会", "location": "韶关市新丰县"},
    {"id": 6, "name": "中共新丰县委统战部", "type": "党委", "level": "正科级", "parent": "中共新丰县委员会", "location": "韶关市新丰县"},
    {"id": 7, "name": "新丰县人民武装部", "type": "政府", "level": "正团级", "parent": "韶关军分区", "location": "韶关市新丰县"},
    {"id": 8, "name": "新丰县人大常委会", "type": "人大", "level": "正处级", "parent": "韶关市人大常委会", "location": "韶关市新丰县"},
    {"id": 9, "name": "新丰县政协", "type": "政协", "level": "正处级", "parent": "韶关市政协", "location": "韶关市新丰县"},
    {"id": 10, "name": "中共韶关市委员会", "type": "党委", "level": "地厅级", "parent": "中共广东省委", "location": "韶关市"},
    {"id": 11, "name": "韶关市人民政府", "type": "政府", "level": "地厅级", "parent": "广东省人民政府", "location": "韶关市"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "新丰县委书记", "start": "待查（至2026年在任）", "end": "present", "rank": "正处级", "note": "2026年多篇常委会会议报道确认"},
    {"person_id": 2, "org_id": 1, "title": "新丰县委副书记", "start": "待查（至2026年在任）", "end": "present", "rank": "正处级", "note": "2026年多篇报道确认"},
    {"person_id": 2, "org_id": 2, "title": "新丰县县长", "start": "待查（至2026年在任）", "end": "present", "rank": "正处级", "note": "县政府党组书记"},
    {"person_id": 3, "org_id": 1, "title": "新丰县委常委", "start": "待查（至2026年在任）", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 3, "title": "新丰县委组织部部长", "start": "待查（至2026年在任）", "end": "present", "rank": "正科级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "新丰县委常委", "start": "待查（至2026年在任）", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "新丰县委宣传部部长", "start": "待查（至2026年在任）", "end": "present", "rank": "正科级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "新丰县委常委", "start": "待查（至2026年在任）", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 5, "title": "新丰县委政法委书记", "start": "待查（至2026年在任）", "end": "present", "rank": "正科级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "新丰县委常委", "start": "待查（至2026年在任）", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 6, "title": "新丰县委统战部部长", "start": "待查（至2026年在任）", "end": "present", "rank": "正科级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "新丰县委常委", "start": "待查（至2026年在任）", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 7, "title": "新丰县人武部政委", "start": "待查（至2026年在任）", "end": "present", "rank": "正团级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "新丰县县长（历任）", "start": "待查", "end": "待查", "rank": "正处级", "note": "维基百科列为县长，侯新祥为其继任者"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "新丰县委书记与县长党政搭档", "overlap_org": "新丰县", "overlap_period": "郑伟平任县委书记、侯新祥任县长期间（2026年）"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与组织部部长", "overlap_org": "中共新丰县委员会", "overlap_period": "当前（2026年）"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与宣传部部长", "overlap_org": "中共新丰县委员会", "overlap_period": "当前（2026年）"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委书记与政法委书记", "overlap_org": "中共新丰县委员会", "overlap_period": "当前（2026年）"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县委书记与统战部部长", "overlap_org": "中共新丰县委员会", "overlap_period": "当前（2026年）"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "县委书记与人武部政委", "overlap_org": "中共新丰县委员会", "overlap_period": "当前（2026年）"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长与组织部部长（县委班子同僚）", "overlap_org": "中共新丰县委员会", "overlap_period": "当前（2026年）"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "县长与宣传部部长（县委班子同僚）", "overlap_org": "中共新丰县委员会", "overlap_period": "当前（2026年）"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "县长与政法委书记（县委班子同僚）", "overlap_org": "中共新丰县委员会", "overlap_period": "当前（2026年）"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "县长与统战部部长（县委班子同僚）", "overlap_org": "中共新丰县委员会", "overlap_period": "当前（2026年）"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "县长与人武部政委（县委班子同僚）", "overlap_org": "中共新丰县委员会", "overlap_period": "当前（2026年）"},
    {"person_a": 8, "person_b": 2, "type": "predecessor_successor", "context": "区毅明为前任县长，侯新祥为现任县长", "overlap_org": "新丰县人民政府", "overlap_period": "前后任关系（具体交接时间待查）"},
]

# ── Build ──
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"Build complete: {SLUG}")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
