#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
连平县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 广东省
Parent City: 河源市
Region: 连平县
Targets: 县委书记 & 县长

Research Sources:
- 连平县人民政府门户网站 (www.lianping.gov.cn) — 领导之窗、时政新闻
- 连平发布

Current status (as of 2026-07-22):
- 县委书记: 邓小强（河源市人大常委会副主任兼连平县委书记）
- 县长: 黄罡星（县委副书记，县政府党组书记、县长）

Research Date: 2026-07-22
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../"))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths ──
SLUG = "连平县"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 县委领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "邓小强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "河源市人大常委会副主任、中共连平县委书记",
        "current_org": "中共连平县委员会",
        "source": "连平县人民政府门户网站:时政新闻(2025-12至2026-07)"
    },
    {
        "id": 2,
        "name": "黄罡星",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共连平县委副书记、连平县人民政府县长",
        "current_org": "连平县人民政府",
        "source": "连平县人民政府门户网站:领导之窗、时政新闻(2026-07)"
    },
    # ════════════════════════════════════════
    # 县人大常委会领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "陈伟雄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "连平县人大常委会党组书记、主任",
        "current_org": "连平县人民代表大会常务委员会",
        "source": "连平县人民政府门户网站:两会报道(2026-02)"
    },
    # ════════════════════════════════════════
    # 县政协领导
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "吴树民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "连县政协党组书记、主席",
        "current_org": "中国人民政治协商会议连平县委员会",
        "source": "连平县人民政府门户网站:两会报道(2026-02)"
    },
    # ════════════════════════════════════════
    # 县政府领导班子
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "张志雄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "连平县委常委、副县长",
        "current_org": "连平县人民政府",
        "source": "连平县人民政府门户网站:领导之窗"
    },
    {
        "id": 6,
        "name": "戴妮娜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "连平县人民政府副县长",
        "current_org": "连平县人民政府",
        "source": "连平县人民政府门户网站:领导之窗"
    },
    {
        "id": 7,
        "name": "李辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "连平县人民政府副县长",
        "current_org": "连平县人民政府",
        "source": "连平县人民政府门户网站:领导之窗"
    },
    {
        "id": 8,
        "name": "罗中正",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "连平县人民政府副县长",
        "current_org": "连平县人民政府",
        "source": "连平县人民政府门户网站:领导之窗"
    },
    {
        "id": 9,
        "name": "李鸿飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "连平县人民政府副县长",
        "current_org": "连平县人民政府",
        "source": "连平县人民政府门户网站:领导之窗"
    },
    {
        "id": 10,
        "name": "邱文波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "连平县人民政府副县长",
        "current_org": "连平县人民政府",
        "source": "连平县人民政府门户网站:领导之窗"
    },
    {
        "id": 11,
        "name": "王汉璐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "连平县人民政府副县长",
        "current_org": "连平县人民政府",
        "source": "连平县人民政府门户网站:领导之窗"
    },
    # ════════════════════════════════════════
    # 其他县领导（县委常委等）
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "张志勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "连平县委常委",
        "current_org": "中共连平县委员会",
        "source": "连平县人民政府门户网站:时政新闻"
    },
    {
        "id": 13,
        "name": "吴秋菊",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "连平县委常委",
        "current_org": "中共连平县委员会",
        "source": "连平县人民政府门户网站:时政新闻"
    },
    {
        "id": 14,
        "name": "邓先明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "连平县委常委",
        "current_org": "中共连平县委员会",
        "source": "连平县人民政府门户网站:时政新闻(2026-04)"
    },
    {
        "id": 15,
        "name": "阳曜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "连平县委常委",
        "current_org": "中共连平县委员会",
        "source": "连平县人民政府门户网站:两会报道(2026-02)"
    },
    {
        "id": 16,
        "name": "熊剑伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "连平县委常委",
        "current_org": "中共连平县委员会",
        "source": "连平县人民政府门户网站:时政新闻"
    },
    {
        "id": 17,
        "name": "曾晓敏",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "连平县委常委",
        "current_org": "中共连平县委员会",
        "source": "连平县人民政府门户网站:两会报道(2026-02)"
    },
    {
        "id": 18,
        "name": "谢房志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "连平县委常委",
        "current_org": "中共连平县委员会",
        "source": "连平县人民政府门户网站:时政新闻(2026-01)"
    },
    {
        "id": 19,
        "name": "欧阳珊",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "连平县委常委",
        "current_org": "中共连平县委员会",
        "source": "连平县人民政府门户网站:两会报道(2026-02)"
    },
    {
        "id": 20,
        "name": "曾建平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "连平县委常委",
        "current_org": "中共连平县委员会",
        "source": "连平县人民政府门户网站:两会报道(2026-02)"
    },
    {
        "id": 21,
        "name": "陈容玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "连平县领导",
        "current_org": "中共连平县委员会",
        "source": "连平县人民政府门户网站:两会报道(2026-02)"
    },
    {
        "id": 22,
        "name": "叶彦波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "连平县领导",
        "current_org": "连平县人民政府",
        "source": "连平县人民政府门户网站:两会报道(2026-02)"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共连平县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共河源市委员会",
        "location": "广东省河源市连平县"
    },
    {
        "id": 2,
        "name": "连平县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "河源市人民政府",
        "location": "广东省河源市连平县"
    },
    {
        "id": 3,
        "name": "连平县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "parent": "河源市人民代表大会常务委员会",
        "location": "广东省河源市连平县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议连平县委员会",
        "type": "政协",
        "level": "县",
        "parent": "政协河源市委员会",
        "location": "广东省河源市连平县"
    },
    {
        "id": 5,
        "name": "河源市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级市",
        "parent": "广东省人民代表大会常务委员会",
        "location": "广东省河源市"
    },
]

# 3. Positions
positions = [
    # 邓小强
    {"person_id": 1, "org_id": 5, "title": "河源市人大常委会副主任", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": "confirmed"},
    {"person_id": 1, "org_id": 1, "title": "中共连平县委书记", "start_date": "2025-12前", "end_date": "present", "rank": "县处级正职", "note": "confirmed: 2025年12月起以县委书记身份参加活动"},
    # 黄罡星
    {"person_id": 2, "org_id": 2, "title": "连平县人民政府县长", "start_date": "待查", "end_date": "present", "rank": "县处级正职", "note": "confirmed: 2026年2月政府工作报告"},
    {"person_id": 2, "org_id": 1, "title": "中共连平县委副书记", "start_date": "待查", "end_date": "present", "rank": "", "note": "confirmed"},
    # 陈伟雄
    {"person_id": 3, "org_id": 3, "title": "连平县人大常委会党组书记、主任", "start_date": "待查", "end_date": "present", "rank": "县处级正职", "note": "confirmed: 2026年2月两会"},
    # 吴树民
    {"person_id": 4, "org_id": 4, "title": "连平县政协党组书记、主席", "start_date": "待查", "end_date": "present", "rank": "县处级正职", "note": "confirmed: 2026年2月两会"},
    # 县政府领导班子
    {"person_id": 5, "org_id": 1, "title": "连平县委常委", "start_date": "待查", "end_date": "present", "rank": "", "note": "confirmed"},
    {"person_id": 5, "org_id": 2, "title": "连平县人民政府副县长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "confirmed"},
    {"person_id": 6, "org_id": 2, "title": "连平县人民政府副县长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "confirmed"},
    {"person_id": 7, "org_id": 2, "title": "连平县人民政府副县长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "confirmed"},
    {"person_id": 8, "org_id": 2, "title": "连平县人民政府副县长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "confirmed"},
    {"person_id": 9, "org_id": 2, "title": "连平县人民政府副县长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "confirmed"},
    {"person_id": 10, "org_id": 2, "title": "连平县人民政府副县长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "confirmed"},
    {"person_id": 11, "org_id": 2, "title": "连平县人民政府副县长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "confirmed"},
    # 县委常委
    {"person_id": 12, "org_id": 1, "title": "连平县委常委", "start_date": "待查", "end_date": "present", "rank": "", "note": "confirmed"},
    {"person_id": 13, "org_id": 1, "title": "连平县委常委", "start_date": "待查", "end_date": "present", "rank": "", "note": "confirmed"},
    {"person_id": 14, "org_id": 1, "title": "连平县委常委", "start_date": "待查", "end_date": "present", "rank": "", "note": "confirmed"},
    {"person_id": 15, "org_id": 1, "title": "连平县委常委", "start_date": "待查", "end_date": "present", "rank": "", "note": "confirmed"},
    {"person_id": 16, "org_id": 1, "title": "连平县委常委", "start_date": "待查", "end_date": "present", "rank": "", "note": "confirmed"},
    {"person_id": 17, "org_id": 1, "title": "连平县委常委", "start_date": "待查", "end_date": "present", "rank": "", "note": "confirmed"},
    {"person_id": 18, "org_id": 1, "title": "连平县委常委", "start_date": "待查", "end_date": "present", "rank": "", "note": "confirmed"},
    {"person_id": 19, "org_id": 1, "title": "连平县委常委", "start_date": "待查", "end_date": "present", "rank": "", "note": "confirmed"},
    {"person_id": 20, "org_id": 1, "title": "连平县委常委", "start_date": "待查", "end_date": "present", "rank": "", "note": "confirmed"},
    {"person_id": 21, "org_id": 1, "title": "县领导", "start_date": "待查", "end_date": "present", "rank": "", "note": "confirmed"},
    {"person_id": 22, "org_id": 2, "title": "县领导", "start_date": "待查", "end_date": "present", "rank": "", "note": "confirmed"},
]

# 4. Relationships
relationships = [
    # 邓小强 ←→ 黄罡星（党政正职搭档）
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "连平县党政正职搭档，邓小强为县委书记、黄罡星为县长", "overlap_org": "连平县", "overlap_period": "2025-12至今"},
    # 邓小强 ←→ 陈伟雄（县委-县人大）
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记与县人大常委会主任", "overlap_org": "连平县", "overlap_period": "2025-12至今"},
    # 黄罡星 ←→ 陈伟雄（县政府-县人大）
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长与县人大常委会主任", "overlap_org": "连平县", "overlap_period": "已知时期"},
    # 黄罡星 ←→ 县政府领导班子
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "连平县人民政府", "overlap_period": "已知时期"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "连平县人民政府", "overlap_period": "已知时期"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "连平县人民政府", "overlap_period": "已知时期"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "连平县人民政府", "overlap_period": "已知时期"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "连平县人民政府", "overlap_period": "已知时期"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "连平县人民政府", "overlap_period": "已知时期"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "连平县人民政府", "overlap_period": "已知时期"},
    # 副县长之间的同僚关系
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "同为副县长", "overlap_org": "连平县人民政府", "overlap_period": "已知时期"},
    {"person_a": 5, "person_b": 7, "type": "overlap", "context": "同为副县长", "overlap_org": "连平县人民政府", "overlap_period": "已知时期"},
    {"person_a": 5, "person_b": 8, "type": "overlap", "context": "同为副县长", "overlap_org": "连平县人民政府", "overlap_period": "已知时期"},
    {"person_a": 5, "person_b": 9, "type": "overlap", "context": "同为副县长", "overlap_org": "连平县人民政府", "overlap_period": "已知时期"},
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "同为副县长", "overlap_org": "连平县人民政府", "overlap_period": "已知时期"},
    {"person_a": 6, "person_b": 8, "type": "overlap", "context": "同为副县长", "overlap_org": "连平县人民政府", "overlap_period": "已知时期"},
    {"person_a": 7, "person_b": 8, "type": "overlap", "context": "同为副县长", "overlap_org": "连平县人民政府", "overlap_period": "已知时期"},
    # 县委常委之间的关系
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate", "context": "县委书记与县委常委", "overlap_org": "中共连平县委员会", "overlap_period": "已知时期"},
    {"person_a": 1, "person_b": 13, "type": "superior_subordinate", "context": "县委书记与县委常委", "overlap_org": "中共连平县委员会", "overlap_period": "已知时期"},
    {"person_a": 1, "person_b": 14, "type": "superior_subordinate", "context": "县委书记与县委常委", "overlap_org": "中共连平县委员会", "overlap_period": "已知时期"},
    {"person_a": 1, "person_b": 15, "type": "superior_subordinate", "context": "县委书记与县委常委", "overlap_org": "中共连平县委员会", "overlap_period": "已知时期"},
    {"person_a": 1, "person_b": 16, "type": "superior_subordinate", "context": "县委书记与县委常委", "overlap_org": "中共连平县委员会", "overlap_period": "已知时期"},
    {"person_a": 1, "person_b": 17, "type": "superior_subordinate", "context": "县委书记与县委常委", "overlap_org": "中共连平县委员会", "overlap_period": "已知时期"},
    {"person_a": 1, "person_b": 18, "type": "superior_subordinate", "context": "县委书记与县委常委", "overlap_org": "中共连平县委员会", "overlap_period": "已知时期"},
    {"person_a": 1, "person_b": 19, "type": "superior_subordinate", "context": "县委书记与县委常委", "overlap_org": "中共连平县委员会", "overlap_period": "已知时期"},
    {"person_a": 1, "person_b": 20, "type": "superior_subordinate", "context": "县委书记与县委常委", "overlap_org": "中共连平县委员会", "overlap_period": "已知时期"},
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
    print("✅ Build complete!")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
