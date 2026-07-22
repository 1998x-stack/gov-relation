#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
博罗县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 广东省
Parent City: 惠州市
Region: 博罗县
Targets: 县委书记 & 县长

Research Sources:
- 博罗县人民政府门户网站 (www.boluo.gov.cn) — 政务要闻、政府会议等官方新闻
- 惠州市人民政府门户网站 (www.huizhou.gov.cn) — 领导之窗
- 数据采集日期: 2026-07-22
- 官方来源确认，所有现任职务均有据可查

Current status (as of 2026-07-22):
- 县委书记: 周耿斌
- 县委副书记、县长: 邱志彪
- 县人大常委会主任: 田裕东
- 县政协主席: 徐颂
- 县委常委、常务副县长: 孙宇强
- 县委常委、组织部部长: 周厚虎
- 县委常委、县纪委书记、县监委主任: 邱敏强
- 县委常委、统战部部长: 陈沛亮
- 副县长: 李智

Research Date: 2026-07-22
Evidence Note: Leadership names confirmed from official government news articles.
Biographical details for most figures are still to be collected from external sources;
incomplete fields are marked accordingly.
"""

import os
import sys
from datetime import datetime

# Allow import from repo root
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "博罗县"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════════
    # 县委领导
    # ════════════════════════════════════════════
    {
        "id": 1,
        "name": "周耿斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共博罗县委书记",
        "current_org": "中共博罗县委员会",
        "source": "博罗县政府官网政务要闻 (confirmed) — 县委书记"
    },
    {
        "id": 2,
        "name": "邱志彪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "博罗县委副书记、县长",
        "current_org": "博罗县人民政府",
        "source": "博罗县政府官网政务要闻 (confirmed) — 县委副书记、县长"
    },
    {
        "id": 3,
        "name": "田裕东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "博罗县人大常委会主任",
        "current_org": "博罗县人民代表大会常务委员会",
        "source": "博罗县政府官网政府会议 (confirmed) — 县人大常委会主任"
    },
    {
        "id": 4,
        "name": "徐颂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "博罗县政协主席",
        "current_org": "中国人民政治协商会议博罗县委员会",
        "source": "博罗县政府官网政府会议 (confirmed) — 县政协主席"
    },
    {
        "id": 5,
        "name": "孙宇强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "博罗县委常委、常务副县长",
        "current_org": "博罗县人民政府",
        "source": "博罗县政府官网 (confirmed) — 县委常委、常务副县长"
    },
    {
        "id": 6,
        "name": "周厚虎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "博罗县委常委、组织部部长",
        "current_org": "中共博罗县委员会",
        "source": "博罗县政府官网政府会议 (confirmed) — 县委常委、组织部部长"
    },
    {
        "id": 7,
        "name": "邱敏强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "博罗县委常委、县纪委书记、县监委主任",
        "current_org": "中共博罗县纪律检查委员会",
        "source": "博罗县政府官网 (confirmed) — 县委常委、县纪委书记"
    },
    {
        "id": 8,
        "name": "陈沛亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "博罗县委常委、统战部部长",
        "current_org": "中共博罗县委员会",
        "source": "博罗县政府官网 (confirmed) — 县委常委、统战部部长"
    },
    {
        "id": 9,
        "name": "李智",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "博罗县副县长",
        "current_org": "博罗县人民政府",
        "source": "博罗县政府官网 (confirmed) — 副县长"
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共博罗县委员会", "type": "党委", "level": "县处级", "parent": "中共惠州市委员会", "location": "广东省惠州市博罗县"},
    {"id": 2, "name": "博罗县人民政府", "type": "政府", "level": "县处级", "parent": "惠州市人民政府", "location": "广东省惠州市博罗县"},
    {"id": 3, "name": "博罗县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "惠州市人民代表大会常务委员会", "location": "广东省惠州市博罗县"},
    {"id": 4, "name": "中国人民政治协商会议博罗县委员会", "type": "政协", "level": "县处级", "parent": "中国人民政治协商会议惠州市委员会", "location": "广东省惠州市博罗县"},
    {"id": 5, "name": "中共博罗县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共惠州市纪律检查委员会", "location": "广东省惠州市博罗县"},
    {"id": 6, "name": "中国共产党博罗县委员会组织部", "type": "党委", "level": "正科级", "parent": "中共博罗县委员会", "location": "广东省惠州市博罗县"},
    {"id": 7, "name": "中国共产党博罗县委员会统战部", "type": "党委", "level": "正科级", "parent": "中共博罗县委员会", "location": "广东省惠州市博罗县"},
]

# 3. Positions
positions = [
    # 周耿斌 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "中共博罗县委书记", "start_date": "待查", "end_date": "present", "rank": "县处级正职", "note": "博罗县委一把手"},
    # 邱志彪 — 副书记、县长
    {"person_id": 2, "org_id": 1, "title": "博罗县委副书记", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "县委副书记"},
    {"person_id": 2, "org_id": 2, "title": "博罗县县长", "start_date": "待查", "end_date": "present", "rank": "县处级正职", "note": "县政府一把手"},
    # 田裕东 — 人大主任
    {"person_id": 3, "org_id": 3, "title": "博罗县人大常委会主任", "start_date": "待查", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 徐颂 — 政协主席
    {"person_id": 4, "org_id": 4, "title": "博罗县政协主席", "start_date": "待查", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 孙宇强 — 常委、常务副县长
    {"person_id": 5, "org_id": 1, "title": "博罗县委常委", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "博罗县常务副县长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "负责县政府常务工作"},
    # 周厚虎 — 常委、组织部部长
    {"person_id": 6, "org_id": 1, "title": "博罗县委常委", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 6, "title": "博罗县委组织部部长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "县委组织部部长"},
    # 邱敏强 — 常委、纪委书记
    {"person_id": 7, "org_id": 1, "title": "博罗县委常委", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "博罗县纪委书记、县监委主任", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "县纪委监委负责人"},
    # 陈沛亮 — 常委、统战部部长
    {"person_id": 8, "org_id": 1, "title": "博罗县委常委", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 7, "title": "博罗县委统战部部长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 李智 — 副县长
    {"person_id": 9, "org_id": 2, "title": "博罗县副县长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "副县长"},
]

# 4. Relationships
relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长——党政一把手搭档", "overlap_org": "中共博罗县委员会/博罗县人民政府", "overlap_period": "现任（2026-07-22）"},
    # 县委书记与各常委
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委书记与常委、常务副县长", "overlap_org": "中共博罗县委员会", "overlap_period": "现任（2026-07-22）"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县委书记与常委、组织部部长", "overlap_org": "中共博罗县委员会", "overlap_period": "现任（2026-07-22）"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "县委书记与纪委书记——党委与纪委监督关系", "overlap_org": "中共博罗县委员会", "overlap_period": "现任（2026-07-22）"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "县委书记与统战部部长", "overlap_org": "中共博罗县委员会", "overlap_period": "现任（2026-07-22）"},
    # 县长与副县长
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "县长与常务副县长——县政府工作搭档", "overlap_org": "博罗县人民政府", "overlap_period": "现任（2026-07-22）"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "博罗县人民政府", "overlap_period": "现任（2026-07-22）"},
    # 人大与县委
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与县人大常委会主任", "overlap_org": "博罗县四套班子", "overlap_period": "现任（2026-07-22）"},
    # 政协与县委
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与县政协主席", "overlap_org": "博罗县四套班子", "overlap_period": "现任（2026-07-22）"},
]

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
    print("Done.")
