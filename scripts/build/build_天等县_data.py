#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天等县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 广西壮族自治区
Parent City: 崇左市
Region: 天等县
Targets: 县委书记 & 县长

当前在任 (as of 2026-07-31):
- 县委书记: 施展 (天等县委书记)
- 县长: 梁坤兴 (天等县委副书记、县长、县政府党组书记)
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "天等县"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-31"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：县委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "施展",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天等县委书记",
        "current_org": "中共天等县委员会",
        "source": "http://www.tiandeng.gov.cn/xwzx/tdyw/t27971746.shtml"
    },
    # ════════════════════════════════════════
    # 核心领导：县长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "梁坤兴",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天等县委副书记、县长、县政府党组书记",
        "current_org": "天等县人民政府/中共天等县委员会",
        "source": "http://www.tiandeng.gov.cn/xwzx/tdyw/t27971693.shtml"
    },
    # ════════════════════════════════════════
    # 前任县委书记（~2026年6月）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "欧正",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "卸任（原天等县委书记）",
        "current_org": "待查",
        "source": "http://www.tiandeng.gov.cn/gddt/t27854796.shtml"
    },
    # ════════════════════════════════════════
    # 县人大常委会党组书记
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "陆智军",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天等县人大常委会党组书记",
        "current_org": "天等县人大常委会",
        "source": "http://www.tiandeng.gov.cn/gddt/t27971760.shtml"
    },
    # ════════════════════════════════════════
    # 县政协主席
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "方向阳",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天等县政协主席",
        "current_org": "天等县政协",
        "source": "http://www.tiandeng.gov.cn/gddt/t27971760.shtml"
    },
    # ════════════════════════════════════════
    # 县委常委、常务副县长
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "刘业科",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天等县委常委、常务副县长",
        "current_org": "天等县人民政府",
        "source": "http://www.tiandeng.gov.cn/gkbz/zfwj/xrmzfwj/t27064711.shtml"
    },
    # ════════════════════════════════════════
    # 县委常委、办公室主任
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "刘欢",
        "ethnicity": "待查",
        "gender": "男",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天等县委常委、县委办公室主任",
        "current_org": "中共天等县委员会",
        "source": "http://www.tiandeng.gov.cn/gddt/t27946047.shtml"
    },
    # ════════════════════════════════════════
    # 县委常委
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "黄步深",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天等县委常委",
        "current_org": "中共天等县委员会",
        "source": "http://www.tiandeng.gov.cn/xwzx/tdyw/t27971746.shtml"
    },
    # ════════════════════════════════════════
    # 县委常委
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "赵晓学",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天等县委常委",
        "current_org": "中共天等县委员会",
        "source": "http://www.tiandeng.gov.cn/xwzx/tdyw/t27971746.shtml"
    },
    # ════════════════════════════════════════
    # 县委常委
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "何祖鹏",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天等县委常委",
        "current_org": "中共天等县委员会",
        "source": "http://www.tiandeng.gov.cn/xwzx/tdyw/t27971746.shtml"
    },
    # ════════════════════════════════════════
    # 县委常委
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "隆艳英",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天等县委常委",
        "current_org": "中共天等县委员会",
        "source": "http://www.tiandeng.gov.cn/xwzx/tdyw/t27971746.shtml"
    },
    # ════════════════════════════════════════
    # 县委常委
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "黄报葳",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天等县委常委",
        "current_org": "中共天等县委员会",
        "source": "http://www.tiandeng.gov.cn/xwzx/tdyw/t27971746.shtml"
    },
    # ════════════════════════════════════════
    # 县委常委
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "肖宇",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天等县委常委",
        "current_org": "中共天等县委员会",
        "source": "http://www.tiandeng.gov.cn/xwzx/tdyw/t27971746.shtml"
    },
    # ════════════════════════════════════════
    # 副县长（教育、农业农村等）
    # ════════════════════════════════════════
    {
        "id": 14,
        "name": "施怡",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天等县副县长",
        "current_org": "天等县人民政府",
        "source": "http://www.tiandeng.gov.cn/gkbz/zfwj/xrmzfwj/t27064711.shtml"
    },
    # ════════════════════════════════════════
    # 副县长（挂职）
    # ════════════════════════════════════════
    {
        "id": 15,
        "name": "林晖",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天等县副县长（挂职）",
        "current_org": "天等县人民政府",
        "source": "http://www.tiandeng.gov.cn/xwzx/tdyw/t27971693.shtml"
    },
    # ════════════════════════════════════════
    # 县领导（副县长级）
    # ════════════════════════════════════════
    {
        "id": 16,
        "name": "农科良",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天等县领导",
        "current_org": "天等县人民政府",
        "source": "http://www.tiandeng.gov.cn/xwzx/tdyw/t27971729.shtml"
    },
    # ════════════════════════════════════════
    # 县领导
    # ════════════════════════════════════════
    {
        "id": 17,
        "name": "时俊晖",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天等县领导",
        "current_org": "天等县人民政府",
        "source": "http://www.tiandeng.gov.cn/xwzx/gd1212.shtml"
    },
    # ════════════════════════════════════════
    # 县领导
    # ════════════════════════════════════════
    {
        "id": 18,
        "name": "马径军",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天等县领导",
        "current_org": "天等县人民政府",
        "source": "http://www.tiandeng.gov.cn/xwzx/gd1212.shtml"
    },
    # ════════════════════════════════════════
    # 前任天等县委常委、县纪委书记（2018-2019），现扶绥县长
    # ════════════════════════════════════════
    {
        "id": 19,
        "name": "周春科",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1983-07",
        "birthplace": "广西大新",
        "education": "在职研究生学历",
        "party_join": "2005-06",
        "work_start": "2005-07",
        "current_post": "扶绥县委副书记、县长",
        "current_org": "扶绥县人民政府",
        "source": "data/persons/20260723-广西壮族自治区-崇左市-县长-周春科.json"
    },
    # ════════════════════════════════════════
    # 副县长（交通运输、林业、水利等）
    # ════════════════════════════════════════
    {
        "id": 20,
        "name": "卢宏",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天等县副县长",
        "current_org": "天等县人民政府",
        "source": "http://www.tiandeng.gov.cn/gkbz/zfwj/xrmzfwj/t27064711.shtml"
    },
    # ════════════════════════════════════════
    # 副县长（公安、信访等）
    # ════════════════════════════════════════
    {
        "id": 21,
        "name": "管彬杰",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天等县副县长（公安）",
        "current_org": "天等县人民政府",
        "source": "http://www.tiandeng.gov.cn/gkbz/zfwj/xrmzfwj/t27064711.shtml"
    },
    # ════════════════════════════════════════
    # 挂职副县长（退役军人事务等）
    # ════════════════════════════════════════
    {
        "id": 22,
        "name": "何振鑫",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天等县副县长（挂职）",
        "current_org": "天等县人民政府",
        "source": "http://www.tiandeng.gov.cn/gkbz/zfwj/xrmwj/t27064711.shtml"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共天等县委员会", "type": "党委", "level": "县处级", "parent": "中共崇左市委员会", "location": "崇左市天等县"},
    {"id": 2, "name": "天等县人民政府", "type": "政府", "level": "县处级", "parent": "崇左市人民政府", "location": "崇左市天等县"},
    {"id": 3, "name": "天等县人大常委会", "type": "人大", "level": "县处级", "parent": "崇左市人大常委会", "location": "崇左市天等县"},
    {"id": 4, "name": "天等县政协", "type": "政协", "level": "县处级", "parent": "崇左市政协", "location": "崇左市天等县"},
    {"id": 5, "name": "中共天等县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共崇左市纪律检查委员会", "location": "崇左市天等县"},
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 施展 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "天等县委书记", "start": "2026-07", "end": "present", "rank": "县处级正职", "note": "2026年7月在天等县第十四次党代会上作报告，确认为县委书记"},
    # 梁坤兴 - 县长
    {"person_id": 2, "org_id": 2, "title": "天等县委副书记、县长", "start": "待查", "end": "present", "rank": "县处级正职", "note": "2026年7月31日新闻以县长身份调研项目建设"},
    {"person_id": 2, "org_id": 1, "title": "天等县委副书记", "start": "待查", "end": "present", "rank": "县处级正职", "note": ""},
    # 欧正 - 前任县委书记（至2026年6月）
    {"person_id": 3, "org_id": 1, "title": "天等县委书记", "start": "待查", "end": "2026-06", "rank": "县处级正职", "note": "2026年6月25日仍以县委书记身份开展七一慰问，7月已由施展接任"},
    # 陆智军 - 人大党组书记
    {"person_id": 4, "org_id": 3, "title": "天等县人大常委会党组书记", "start": "待查", "end": "present", "rank": "县处级正职", "note": ""},
    # 方向阳 - 政协主席
    {"person_id": 5, "org_id": 4, "title": "天等县政协主席", "start": "待查", "end": "present", "rank": "县处级正职", "note": ""},
    # 刘业科 - 常务副县长
    {"person_id": 6, "org_id": 1, "title": "天等县委常委", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "天等县常务副县长", "start": "待查", "end": "present", "rank": "县处级副职", "note": "负责常务工作，分管发改、财政、应急等"},
    # 刘欢 - 办公室主任
    {"person_id": 7, "org_id": 1, "title": "天等县委常委、县委办公室主任", "start": "待查", "end": "present", "rank": "县处级副职", "note": "2026年7月24日陪同县委书记施展调研"},
    # 其他县委常委
    {"person_id": 8, "org_id": 1, "title": "天等县委常委", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "天等县委常委", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "天等县委常委", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "天等县委常委", "start": "待查", "end": "present", "rank": "县处级副职", "note": "女性"},
    {"person_id": 12, "org_id": 1, "title": "天等县委常委", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "天等县委常委", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    # 施怡 - 副县长
    {"person_id": 14, "org_id": 2, "title": "天等县副县长", "start": "待查", "end": "present", "rank": "县处级副职", "note": "分管教育、农业农村、文旅、卫健、民政等"},
    # 林晖 - 挂职副县长
    {"person_id": 15, "org_id": 2, "title": "天等县副县长（挂职）", "start": "待查", "end": "present", "rank": "县处级副职", "note": "对接广东省江门市对口帮扶协作"},
    # 其他县领导
    {"person_id": 16, "org_id": 2, "title": "天等县领导", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "天等县领导", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "天等县领导", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    # 周春科 - 天等任期（现扶绥县长，曾在天等任职）
    {"person_id": 19, "org_id": 5, "title": "天等县委常委、县纪委书记", "start": "2018-09", "end": "2019-09", "rank": "县处级副职", "note": "来自扶斐县调研数据"},
    # 卢宏 - 副县长
    {"person_id": 20, "org_id": 2, "title": "天等县副县长", "start": "待查", "end": "present", "rank": "县处级副职", "note": "分管交通、林业、水利、环保等"},
    # 管彬杰 - 副县长（公安）
    {"person_id": 21, "org_id": 2, "title": "天等县副县长", "start": "待查", "end": "present", "rank": "县处级副职", "note": "分管公安、信访、司法等"},
    # 何振鑫 - 挂职副县长
    {"person_id": 22, "org_id": 2, "title": "天等县副县长（挂职）", "start": "待查", "end": "present", "rank": "县处级副职", "note": "分管退役军人事务、市场监管等"},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 施展 ↔ 梁坤兴（书记县长搭档）
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记与县长党政搭档", "overlap_org": "中共天等县委员会/天等县人民政府", "overlap_period": "2026-07—present", "strength": "strong", "confidence": "confirmed"},
    # 施展接任欧正
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "施展接替欧正任天等县委书记", "overlap_org": "中共天等县委员会", "overlap_period": "2026-06/07交朴", "strength": "medium", "confidence": "confirmed"},
    # 刘业科 ↔ 梁坤兴（常务副与县长）
    {"person_a": 6, "person_b": 2, "type": "superior_subordinate", "context": "常务副县长协助县长工作", "overlap_org": "天等县人民政府", "overlap_period": "当前", "strength": "strong", "confidence": "confirmed"},
    # 刘欢 ↔ 施展（办公室主任与书记）
    {"person_a": 7, "person_b": 1, "type": "superior_subordinate", "context": "县委办公室主任陪同书记调研", "overlap_org": "中共天等县委员会", "overlap_period": "当前", "strength": "strong", "confidence": "confirmed"},
    # 周春弟 - 原天等常委/纪委书记，现任扶媛县长
    {"person_a": 19, "person_b": 1, "type": "overlap", "context": "周春弟曾在天等担任纪委书记，施展现任县委书记，时间暂未确认是否重叠", "overlap_org": "中共天等县委员会", "overlap_period": "未知", "strength": "weak", "confidence": "unverified"},
]

# =========================================================================
# 5. DATABASE SETUP
# =========================================================================

def create_database(db_path):
    """Create SQLite database with the standard schema."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        );

        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );

        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    # Insert persons
    for p in persons:
        cur.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education,
                                 party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
              p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
              p.get("party_join", ""), p.get("work_start", ""),
              p.get("current_post", ""), p.get("current_org", ""),
              p.get("source", "")))

    # Insert organizations
    for o in organizations:
        cur.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    # Insert positions
    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos.get("start", ""),
              pos.get("end", "present"), pos.get("rank", ""), pos.get("note", "")))

    # Insert relationships
    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org,
                                        overlap_period, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"],
              r.get("overlap_org", ""), r.get("overlap_period", ""),
              r.get("confidence", "plausible")))

    conn.commit()
    conn.close()
    print(f"[DB] Created: {db_path}")
    print(f"[DB]   Persons: {len(persons)}")
    print(f"[DB]   Organizations: {len(organizations)}")
    print(f"[DB]   Positions: {len(positions)}")
    print(f"[DB]   Relationships: {len(relationships)}")


# =========================================================================
# 6. GEXF GENERATION
# =========================================================================

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return 'r,g,b' string for person role."""
    role = p.get("current_post", "").lower()
    if "县委书记" in role:
        return "255,50,50"
    elif "县长" in role or "副县长" in role:
        return "50,100,255"
    elif "纪委" in role:
        return "255,165,0"
    else:
        return "100,100,100"


def org_color(o):
    """Return 'r,g,b' for org type."""
    t = o["type"]
    if t == "党委":
        return "255,200,200"
    elif t == "政府":
        return "200,200,255"
    elif t == "人大":
        return "200,255,255"
    elif t == "政协":
        return "255,240,200"
    elif t == "纪委":
        return "255,200,150"
    else:
        return "200,200,200"


def is_top_leader(p):
    """Top leaders get larger nodes."""
    role = p.get("current_post", "")
    return "县委书记" in role or "县长" in role


def generate_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append(f'    <description>天等县领导班子工作关系网络 (as of {AS_OF})</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        sid = f"p{p['id']}"
        lines.append(f'      <node id="{sid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        sid = f"o{o['id']}"
        lines.append(f'      <node id="{sid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> Organization (worked at)
    for pos in positions:
        eid += 1
        src = f"p{pos['person_id']}"
        tgt = f"o{pos['org_id']}"
        lbl = esc(pos['title'])
        lines.append(f'      <edge id="e{eid}" source="{src}" target="{tgt}" label="{lbl}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person -> Person (relationships)
    for r in relationships:
        eid += 1
        src = f"p{r['person_a']}"
        tgt = f"p{r['person_b']}"
        wt = 2.0
        lines.append(f'      <edge id="e{eid}" source="{src}" target="{tgt}" weight="{wt}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{r.get("confidence", "unverified")}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[GEXF] Created {GEXF_PATH}")


# =========================================================================
# 7. MAIN
# =========================================================================

if __name__ == "__main__":
    create_database(DB_PATH)
    generate_gexf()
    print(f"\n[DONE] Artifacts in {STAGING_DIR}/")
    print(f"  DB:    {SLUG}_network.db")
    print(f"  GEXF:  {SLUG}_network.gexf")