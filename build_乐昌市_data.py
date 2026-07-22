#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
乐昌市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县级市
Province: 广东省
Parent City: 韶关市
Region: 乐昌市
Targets: 市委书记 & 市长

Research Sources:
- 百度百科 — 颜雪锋词条
- 百度百科 — 刘华益词条
- 百度百科 — 沈河民词条
- 乐昌市政府公众信息网 (www.lechang.gov.cn)

Current status (as of 2026-07-22):
- 市委书记: 颜雪锋（2025年9月－）
- 市长: 刘华益（2021年11月－）

Research Date: 2026-07-22
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "乐昌市"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 市委领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "颜雪锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年1月",
        "birthplace": "广东台山",
        "native_place": "广东台山",
        "education": "大学学历",
        "party_join": "中共党员（1995年1月）",
        "work_start": "1999年7月",
        "current_post": "中共乐昌市委书记、市人武部党委第一书记",
        "current_org": "中共乐昌市委员会",
        "source": "百度百科:颜雪锋"
    },
    {
        "id": 2,
        "name": "刘华益",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年12月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历，理学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "乐昌市委副书记、市政府党组书记、市长",
        "current_org": "乐昌市人民政府",
        "source": "百度百科:刘华益"
    },
    # ════════════════════════════════════════
    # 前任主要领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "沈河民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年10月",
        "birthplace": "广东",
        "native_place": "广东",
        "education": "华南农业大学农业推广硕士",
        "party_join": "中共党员",
        "work_start": "1987年7月",
        "current_post": "韶关市人大常委会党组副书记、副主任",
        "current_org": "韶关市人民代表大会常务委员会",
        "source": "百度百科:沈河民"
    },
    # ════════════════════════════════════════
    # 佛山市应急管理局（颜雪锋前任岗位相关）
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "颜雪锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年1月",
        "birthplace": "广东台山",
        "native_place": "广东台山",
        "education": "大学学历",
        "party_join": "中共党员（1995年1月）",
        "work_start": "1999年7月",
        "current_post": "（前任）佛山市应急管理局党委书记、局长",
        "current_org": "佛山市应急管理局",
        "source": "百度百科:颜雪锋"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共乐昌市委员会",
        "type": "党委",
        "level": "县级市",
        "parent": "中共韶关市委员会",
        "location": "乐昌市"
    },
    {
        "id": 2,
        "name": "乐昌市人民政府",
        "type": "政府",
        "level": "县级市",
        "parent": "韶关市人民政府",
        "location": "乐昌市"
    },
    {
        "id": 3,
        "name": "乐昌市人民代表大会常务委员会",
        "type": "人大",
        "level": "县级市",
        "parent": "韶关市人民代表大会常务委员会",
        "location": "乐昌市"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议乐昌市委员会",
        "type": "政协",
        "level": "县级市",
        "parent": "中国人民政治协商会议韶关市委员会",
        "location": "乐昌市"
    },
    {
        "id": 5,
        "name": "乐昌市人民武装部",
        "type": "党委",
        "level": "县级",
        "parent": "韶关军分区",
        "location": "乐昌市"
    },
    {
        "id": 6,
        "name": "佛山市应急管理局",
        "type": "政府",
        "level": "地级市",
        "parent": "佛山市人民政府",
        "location": "佛山市"
    },
    {
        "id": 7,
        "name": "佛山市禅城区张槎街道党工委",
        "type": "党委",
        "level": "乡级",
        "parent": "中共佛山市禅城区委员会",
        "location": "佛山市禅城区"
    },
    {
        "id": 8,
        "name": "佛山市高明区人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "佛山市人民政府",
        "location": "佛山市高明区"
    },
    {
        "id": 9,
        "name": "中共韶关市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广东省委员会",
        "location": "韶关市"
    },
    {
        "id": 10,
        "name": "韶关市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广东省人民政府",
        "location": "韶关市"
    },
    {
        "id": 11,
        "name": "韶关市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级市",
        "parent": "广东省人民代表大会常务委员会",
        "location": "韶关市"
    },
]

# 3. Positions (person_id, org_id, title, start, end, rank, note)
positions = [
    # 颜雪锋（现任市委书记）
    {"person_id": 1, "org_id": 1, "title": "中共乐昌市委书记", "start": "2025-09", "end": "present", "rank": "正处级", "note": "2025年9月跨市调任"},
    {"person_id": 1, "org_id": 5, "title": "乐昌市人武部党委第一书记", "start": "2025-12", "end": "present", "rank": "", "note": "2025年12月兼任"},
    # 颜雪锋（前任职务）
    {"person_id": 4, "org_id": 6, "title": "佛山市应急管理局党委书记、局长", "start": "2022", "end": "2025-09", "rank": "正处级", "note": "调任乐昌市委书记前职务"},
    {"person_id": 4, "org_id": 8, "title": "佛山市高明区副区长", "start": "2021", "end": "2022", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 7, "title": "佛山市禅城区张槎街道党工委书记", "start": "2019-03", "end": "2020-10", "rank": "正科级", "note": "后任禅城区副区长"},
    {"person_id": 4, "org_id": 7, "title": "佛山市禅城区张槎街道党工委副书记、办事处主任", "start": "2015-04", "end": "2019-02", "rank": "正科级", "note": ""},
    # 刘华益（现任市长）
    {"person_id": 2, "org_id": 2, "title": "乐昌市市长", "start": "2021-11", "end": "present", "rank": "正处级", "note": "2021年11月26日当选"},
    {"person_id": 2, "org_id": 1, "title": "乐昌市委副书记", "start": "2021-11", "end": "present", "rank": "正处级", "note": "市委副书记兼市长"},
    # 沈河民（前任市委书记）
    {"person_id": 3, "org_id": 1, "title": "中共乐昌市委书记", "start": "2018-09", "end": "2021-09", "rank": "正处级", "note": "此前曾任乐昌市市长"},
    {"person_id": 3, "org_id": 2, "title": "乐昌市市长", "start": "2016-10", "end": "2018-09", "rank": "正处级", "note": "2016年10月任代理市长，后当选市长"},
    {"person_id": 3, "org_id": 11, "title": "韶关市人大常委会副主任", "start": "2022-01", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 10, "title": "韶关市人民政府秘书长", "start": "2021-09", "end": "2022-01", "rank": "正处级", "note": ""},
]

# 4. Relationships
relationships = [
    # 现任党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "市委书记与市长是乐昌市最重要的党政搭档", "overlap_org": "中共乐昌市委员会/乐昌市人民政府", "overlap_period": "2025-09至今"},
    # 前后任市委书记
    {"person_a": 3, "person_b": 1, "type": "前后任", "context": "沈河民（2018-09至2021-09）→颜雪锋（2025-09至今）", "overlap_org": "中共乐昌市委员会", "overlap_period": "2025-09交接"},
    # 沈河民曾任市长后升市委书记（党政角色转换）
    {"person_a": 3, "person_b": 3, "type": "同人", "context": "沈河民从乐昌市长升任乐昌市委书记", "overlap_org": "乐昌市政府/乐昌市委", "overlap_period": "2016-10至2021-09"},
    # 沈河民与刘华益（前任党政搭档）
    {"person_a": 3, "person_b": 2, "type": "党政正职搭档", "context": "沈河民任市委书记时刘华益尚未到任，但沈河民离任后刘华益接任市长", "overlap_org": "中共乐昌市委员会/乐昌市人民政府", "overlap_period": "2021-11交接"},
    # 颜雪锋从佛山跨市调任
    {"person_a": 1, "person_b": 4, "type": "同人", "context": "颜雪锋从佛山市应急管理局党委书记、局长跨市调任乐昌市委书记", "overlap_org": "佛山市→乐昌市", "overlap_period": "2025-09"},
]

# ── Build ──
if __name__ == "__main__":
    print(f"Building {SLUG} network...")
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
