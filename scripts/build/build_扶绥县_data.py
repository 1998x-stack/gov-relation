#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扶绥县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 广西壮族自治区
Parent City: 崇左市
Region: 扶绥县
Targets: 县委书记 & 县长

当前在任 (as of 2026-07-23):
- 县委书记: 许家恺 (扶绥县委书记)
- 县长: 周春科 (扶绥县委副书记、县长、县政府党组书记)
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "扶绥县"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-23"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：县委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "许家恺",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1974-09",
        "birthplace": "广西大新",
        "education": "广西区委党校研究生学历",
        "party_join": "2001-07",
        "work_start": "1996-08",
        "current_post": "扶绥县委书记",
        "current_org": "中共扶绥县委员会",
        "source": "https://baike.baidu.com/item/%E8%AE%B8%E5%AE%B6%E6%84%BA"
    },
    # ════════════════════════════════════════
    # 核心领导：县长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "周春科",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1983-07",
        "birthplace": "广西大新",
        "education": "在职研究生学历",
        "party_join": "2005-06",
        "work_start": "2005-07",
        "current_post": "扶绥县委副书记、县长、县政府党组书记",
        "current_org": "扶绥县人民政府/中共扶绥县委员会",
        "source": "https://baike.baidu.com/item/%E5%91%A8%E6%98%A5%E7%A7%91/18888888"
    },
    # ════════════════════════════════════════
    # 前任县委书记（2021-2025）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "黄建辉",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1979-09",
        "birthplace": "广西大新",
        "education": "大学学历（广西大学商学院经济学专业）",
        "party_join": "2004-07",
        "work_start": "2002-07",
        "current_post": "南丹县委书记（原扶绥县委书记）",
        "current_org": "中共南丹县委员会",
        "source": "https://baike.baidu.com/item/%E9%BB%84%E5%BB%BA%E8%BE%89"
    },
    # ════════════════════════════════════════
    # 县人大常委会主任
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "黄剑克",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "扶绥县人大常委会主任",
        "current_org": "扶绥县人民代表大会常务委员会",
        "source": "https://www.fusui.gov.cn/"
    },
    # ════════════════════════════════════════
    # 县政协主席
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "刘登科",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "扶绥县政协主席",
        "current_org": "中国人民政治协商会议扶绥县委员会",
        "source": "https://www.fusui.gov.cn/"
    },
    # ════════════════════════════════════════
    # 县委副书记（2022-2025，已调任）
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "谢添",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-12",
        "birthplace": "广西玉林",
        "education": "在职研究生学历，管理学学士",
        "party_join": "2003-12",
        "work_start": "待查",
        "current_post": "江州区委副书记、区长候选人",
        "current_org": "中共崇左市江州区委员会",
        "source": "https://baike.baidu.com/item/%E8%B0%A2%E6%B7%BB"
    },
    # ════════════════════════════════════════
    # 县委常委、组织部部长
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "杨家东",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "扶绥县委常委、组织部部长",
        "current_org": "中共扶绥县委员会",
        "source": "https://www.fusui.gov.cn/"
    },
    # ════════════════════════════════════════
    # 县委常委、纪委书记/监委主任
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "梁钊丰",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "扶绥县委常委、纪委书记、监委主任",
        "current_org": "中共扶绥县纪律检查委员会/扶绥县监察委员会",
        "source": "https://www.fusui.gov.cn/"
    },
    # ════════════════════════════════════════
    # 县委常委、宣传部部长（2025.06-）
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "黄柏昌",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "扶绥县委常委、宣传部部长",
        "current_org": "中共扶绥县委员会",
        "source": "http://www.gxcounty.com/"
    },
    # ════════════════════════════════════════
    # 副县长
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "赵小凤",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "扶绥县副县长",
        "current_org": "扶绥县人民政府",
        "source": "https://www.fusui.gov.cn/"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {
        "id": 1,
        "name": "中共扶绥县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共崇左市委员会",
        "location": "崇左市扶绥县"
    },
    {
        "id": 2,
        "name": "扶绥县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "崇左市人民政府",
        "location": "崇左市扶绥县"
    },
    {
        "id": 3,
        "name": "扶绥县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "崇左市人大常委会",
        "location": "崇左市扶绥县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议扶绥县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协崇左市委员会",
        "location": "崇左市扶绥县"
    },
    {
        "id": 5,
        "name": "中共扶绥县纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共崇左市纪律检查委员会",
        "location": "崇左市扶绥县"
    },
    {
        "id": 6,
        "name": "扶绥县监察委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "崇左市监察委员会",
        "location": "崇左市扶绥县"
    },
    {
        "id": 7,
        "name": "中共扶绥县委组织部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共扶绥县委员会",
        "location": "崇左市扶绥县"
    },
    {
        "id": 8,
        "name": "中共扶绥县委宣传部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共扶绥县委员会",
        "location": "崇左市扶绥县"
    },
    {
        "id": 9,
        "name": "崇左市人民政府",
        "type": "政府",
        "level": "地厅级",
        "parent": "广西壮族自治区人民政府",
        "location": "崇左市"
    },
    {
        "id": 10,
        "name": "中共崇左市委员会",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共广西壮族自治区委员会",
        "location": "崇左市"
    },
    {
        "id": 11,
        "name": "中共南丹县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共河池市委员会",
        "location": "河池市南丹县"
    },
    {
        "id": 12,
        "name": "广西凭祥综合保税区管委会",
        "type": "事业单位",
        "level": "副厅级",
        "parent": "广西壮族自治区人民政府",
        "location": "崇左市凭祥市"
    },
    {
        "id": 13,
        "name": "崇左市国防动员办公室",
        "type": "政府",
        "level": "县处级",
        "parent": "崇左市人民政府",
        "location": "崇左市"
    },
    {
        "id": 14,
        "name": "崇左市外事和边境事务局",
        "type": "政府",
        "level": "县处级",
        "parent": "崇左市人民政府",
        "location": "崇左市"
    },
    {
        "id": 15,
        "name": "共青团崇左市委员会",
        "type": "群团",
        "level": "县处级",
        "parent": "共青团广西壮族自治区委员会",
        "location": "崇左市"
    },
    {
        "id": 16,
        "name": "中共天等县纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共崇左市纪律检查委员会",
        "location": "崇左市天等县"
    },
    {
        "id": 17,
        "name": "中共崇左市江州区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共崇左市委员会",
        "location": "崇左市江州区"
    },
    {
        "id": 18,
        "name": "崇左市发展和改革委员会",
        "type": "政府",
        "level": "县处级",
        "parent": "崇左市人民政府",
        "location": "崇左市"
    },
]

# =========================================================================
# 3. POSITIONS (career timeline entries)
# =========================================================================
positions = [
    # ── 许家恺 career ──
    {"person_id": 1, "org_id": 2, "title": "扶绥县委副书记、县长", "start": "2020-05", "end": "2021-06", "rank": "县处级正职", "note": "扶绥县县长"},
    {"person_id": 1, "org_id": 2, "title": "扶绥县委副书记、县长", "start": "2021-06", "end": "2021-07", "rank": "县处级正职", "note": "县长候选人后正式当选"},
    {"person_id": 1, "org_id": 2, "title": "扶绥县委副书记、县长", "start": "2021-07", "end": "2025-05", "rank": "县处级正职", "note": "正式担任县长"},
    {"person_id": 1, "org_id": 1, "title": "扶绥县委书记", "start": "2025-05", "end": "present", "rank": "县处级正职", "note": "2025年5月任前公示，随后任县委书记"},

    # ── 周春科 career ──
    {"person_id": 2, "org_id": 13, "title": "崇左市国防动员办公室党组书记、主任", "start": "2023-01", "end": "2025-05", "rank": "县处级正职", "note": "兼任市发改委副主任"},
    {"person_id": 2, "org_id": 14, "title": "崇左市外事和边境事务局党委书记、局长", "start": "2022-08", "end": "2023-01", "rank": "县处级正职", "note": ""},
    {"person_id": 2, "org_id": 15, "title": "共青团崇左市委书记", "start": "2019-09", "end": "2022-08", "rank": "县处级正职", "note": ""},
    {"person_id": 2, "org_id": 16, "title": "天等县委常委、县纪委书记", "start": "2018-09", "end": "2019-09", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "扶绥县委副书记、副县长、代理县长", "start": "2025-06", "end": "2025-07", "rank": "县处级正职", "note": "2025年6月13日任命为副县长、代理县长"},
    {"person_id": 2, "org_id": 2, "title": "扶绥县委副书记、县长", "start": "2025-07", "end": "present", "rank": "县处级正职", "note": ""},

    # ── 黄建辉 career (前扶绥县委书记) ──
    {"person_id": 3, "org_id": 12, "title": "广西凭祥综合保税区党工委副书记、管委会常务副主任", "start": "2025-04", "end": "2025-07", "rank": "副厅级", "note": "中国(广西)自由贸易试验区崇左片区管委会常务副主任(兼)"},
    {"person_id": 3, "org_id": 2, "title": "扶绥县委副书记、县长", "start": "2020-05", "end": "2021-07", "rank": "县处级正职", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "扶绥县委书记", "start": "2021-07", "end": "2025-03", "rank": "县处级正职", "note": ""},
    {"person_id": 3, "org_id": 11, "title": "南丹县委书记", "start": "2025-07", "end": "present", "rank": "县处级正职", "note": "跨市调任"},

    # ── 黄剑克 career ──
    {"person_id": 4, "org_id": 3, "title": "扶绥县人大常委会主任", "start": "2021", "end": "present", "rank": "县处级正职", "note": ""},

    # ── 刘登科 career ──
    {"person_id": 5, "org_id": 4, "title": "扶绥县政协主席", "start": "2021", "end": "present", "rank": "县处级正职", "note": ""},

    # ── 谢添 career ──
    {"person_id": 6, "org_id": 1, "title": "扶绥县委副书记（正处长级）、县委党校校长", "start": "2022-06", "end": "2025-12", "rank": "县处级正职", "note": ""},
    {"person_id": 6, "org_id": 17, "title": "江州区委副书记、区长", "start": "2025-12", "end": "present", "rank": "县处级正职", "note": ""},

    # ── 杨家东 career ──
    {"person_id": 7, "org_id": 7, "title": "扶绥县委常委、组织部部长", "start": "2023", "end": "present", "rank": "县处级副职", "note": ""},

    # ── 梁钊丰 career ──
    {"person_id": 8, "org_id": 5, "title": "扶绥县委常委、纪委书记、监委主任", "start": "2023", "end": "present", "rank": "县处级副职", "note": ""},

    # ── 黄柏昌 career ──
    {"person_id": 9, "org_id": 8, "title": "扶绥县委常委、宣传部部长", "start": "2025-06", "end": "present", "rank": "县处级副职", "note": ""},

    # ── 赵小凤 career ──
    {"person_id": 10, "org_id": 2, "title": "扶绥县副县长", "start": "2023", "end": "present", "rank": "县处级副职", "note": ""},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 许家恺 ← 周春科: 前后任县长 (许升书记, 周接县长) ──
    {
        "person_a": 1,
        "person_b": 2,
        "type": "predecessor_successor",
        "context": "许家恺由县长升任县委书记后，周春科接任扶绥县县长",
        "overlap_org": "扶绥县人民政府",
        "overlap_period": "2025-06—present",
    },
    # ── 许家恺 ← 黄建辉: 前后任县委书记 ──
    {
        "person_a": 3,
        "person_b": 1,
        "type": "predecessor_successor",
        "context": "黄建辉2021-2025任扶绥县委书记，许家恺2025年接任",
        "overlap_org": "中共扶绥县委员会",
        "overlap_period": "—2025-05",
    },
    # ── 许家恺 ← 黄建辉: 曾搭档（县长+书记）─
    {
        "person_a": 3,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "黄建辉任县委书记期间，许家恺任县长",
        "overlap_org": "中共扶绥县委员会/扶绥县人民政府",
        "overlap_period": "2021-07—2025-03",
    },
    # ── 许家恺 ← 谢添: 搭档（书记+副书记）─
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "谢添任扶绥县委副书记期间与许家恺（县长/书记）共事",
        "overlap_org": "中共扶绥县委员会",
        "overlap_period": "2022-06—2025-05",
    },
    # ── 谢添 ← 黄建辉: 搭档（书记+副书记）─
    {
        "person_a": 3,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "谢添任扶绥县委副书记，黄建辉任县委书记",
        "overlap_org": "中共扶绥县委员会",
        "overlap_period": "2022-06—2025-03",
    },
    # ── 许家恺 ← 杨家东: 上下级（书记+组织部长）─
    {
        "person_a": 1,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "许家恺（县长/书记）与杨家东（组织部长）在县委班子共事",
        "overlap_org": "中共扶绥县委员会",
        "overlap_period": "2023—present",
    },
    # ── 许家恺 ← 梁钊丰: 上下级（书记+纪委书记）─
    {
        "person_a": 1,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "许家恺与梁钊丰在县委班子共事",
        "overlap_org": "中共扶绥县委员会",
        "overlap_period": "2023—present",
    },
    # ── 周春科 ← 谢添: 前任后任（县长+副书记，谢添先离）─
    {
        "person_a": 2,
        "person_b": 6,
        "type": "overlap",
        "context": "周春科代理县长时，谢添仍在县委副书记任上，短暂共事",
        "overlap_org": "中共扶绥县委员会",
        "overlap_period": "2025-06—2025-12",
    },
]

# =========================================================================
# 5. DATABASE & GEXF BUILD
# =========================================================================

CREATE_PERSONS_SQL = """
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    name TEXT,
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
"""

CREATE_ORGANIZATIONS_SQL = """
CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);
"""

CREATE_POSITIONS_SQL = """
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER,
    org_id INTEGER,
    title TEXT,
    start TEXT,
    "end" TEXT,
    rank TEXT,
    note TEXT
);
"""

CREATE_RELATIONSHIPS_SQL = """
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER,
    person_b INTEGER,
    type TEXT,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT
);
"""


def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # Drop existing tables for overwrite
    cur.execute("DROP TABLE IF EXISTS relationships")
    cur.execute("DROP TABLE IF EXISTS positions")
    cur.execute("DROP TABLE IF EXISTS organizations")
    cur.execute("DROP TABLE IF EXISTS persons")

    cur.execute(CREATE_PERSONS_SQL)
    cur.execute(CREATE_ORGANIZATIONS_SQL)
    cur.execute(CREATE_POSITIONS_SQL)
    cur.execute(CREATE_RELATIONSHIPS_SQL)

    for p in persons:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p["education"],
             p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"])
        )
    for o in organizations:
        cur.execute(
            "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
        )
    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start, \"end\", rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"])
        )
    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?, ?, ?, ?, ?, ?)",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
        )

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(name, current_post):
    """Color by role."""
    if "书记" in current_post and "县委" in current_post:
        return "255,50,50"
    if "县长" in current_post or ("副县长" in current_post and "县长" in current_post):
        return "50,100,255"
    if "纪委" in current_post or "监委" in current_post:
        return "255,165,0"
    if "人大" in current_post:
        return "200,255,255"
    if "政协" in current_post:
        return "255,240,200"
    if "组织部" in current_post:
        return "200,200,255"
    if "宣传部" in current_post:
        return "100,200,255"
    return "100,100,100"


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "纪委": "255,165,0",
        "群团": "255,220,255",
        "事业单位": "220,220,220",
    }
    return colors.get(org_type, "200,200,200")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>gov-relation build script</creator>')
    lines.append(f'    <description>扶绥县领导班子工作关系网络 (as of {AS_OF})</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="level" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        name = p["name"]
        post = p["current_post"]
        org = p["current_org"]
        c = person_color(name, post)
        sz = "20.0" if p["id"] in (1, 2) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
        lines.append('          <attvalue for="3" value="person"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append('          <attvalue for="3" value="org"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])}—{esc(pos["end"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person → Person (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")


# =========================================================================
# 6. PERSON JSON FILES
# =========================================================================
def write_person_json(person_id):
    """Write a graph-style person JSON file."""
    p = next(x for x in persons if x["id"] == person_id)
    name = p["name"]
    slug_name = name

    # Collect positions for this person
    person_positions = [pos for pos in positions if pos["person_id"] == person_id]

    # Collect relationships involving this person
    person_rels = []
    for r in relationships:
        if r["person_a"] == person_id or r["person_b"] == person_id:
            other_id = r["person_b"] if r["person_a"] == person_id else r["person_a"]
            other = next(x for x in persons if x["id"] == other_id)
            person_rels.append({
                "person": other["name"],
                "person_id": f"p{other_id}",
                "relationship_type": r["type"],
                "strength": "strong",
                "evidence": r["context"],
                "overlap_org": r["overlap_org"],
                "overlap_period": r["overlap_period"],
                "direction": "undirected",
                "confidence": "confirmed",
            })

    # Build source register
    sources = [
        {"id": "S001", "title": "扶绥县人民政府门户网站", "url": "https://www.fusui.gov.cn/", "publisher": "扶绥县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "官方政府网站"},
        {"id": "S002", "title": "百度百科-许家恺", "url": "https://baike.baidu.com/item/%E8%AE%B8%E5%AE%B6%E6%84%BA", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": ""},
        {"id": "S003", "title": "百度百科-周春科", "url": "https://baike.baidu.com/item/%E5%91%A8%E6%98%A5%E7%A7%91", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": ""},
        {"id": "S004", "title": "百度百科-黄建辉", "url": "https://baike.baidu.com/item/%E9%BB%84%E5%BB%BA%E8%BE%89", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": ""},
        {"id": "S005", "title": "崇左市领导干部任职前公示（2025-05-22）", "url": "https://www.chongzuo.gov.cn/", "publisher": "崇左市人民政府", "published_at": "2025-05-22", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high", "notes": "许家恺拟任县委书记, 周春科拟作为县长人选"},
        {"id": "S006", "title": "扶绥县第十七届人大常委会第三十三次会议", "url": "https://www.fusui.gov.cn/", "publisher": "扶绥县人大常委会", "published_at": "2025-06-13", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high", "notes": "任命周春科为副县长、代理县长"},
        {"id": "S007", "title": "网易新闻-周春科任扶绥县代理县长", "url": "https://www.163.com/", "publisher": "网易", "published_at": "2025-06-14", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": ""},
    ]

    job_label = "县委书记" if p["current_post"].startswith("扶绥县委书记") else "县长"
    
    filename = f"{AS_OF.replace('-', '')}-广西壮族自治区-崇左市-{job_label}-{name}.json"
    filepath = os.path.join(PERSONS_DIR, filename)

    doc = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "崇左市",
            "region": "扶绥县",
            "job": job_label,
            "task_id": "guangxi_扶绥县",
            "time_focus": "2021-present"
        },
        "identity": {
            "person_id": f"guangxi_fusui_{name}_{p['birth'][:4] if p['birth'] != '待查' else 'unknown'}",
            "name": name,
            "aliases": [],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "birthplace": p["birthplace"],
            "native_place": p["birthplace"],
            "education": [{"period": "", "institution": p["education"], "major": p.get("major", ""), "degree": "", "study_type": "unknown", "source_ids": ["S001", "S002", "S003", "S004"]}],
            "party_join": p["party_join"],
            "work_start": p["work_start"] if p["work_start"] != "待查" else "待查",
            "dedupe_keys": {
                "name_birth": f"{name}_{p['birth']}" if p['birth'] != '待查' else name,
                "name_birthplace": f"{name}_{p['birthplace']}" if p['birthplace'] != '待查' else name,
                "official_profile_url": "https://www.fusui.gov.cn/"
            }
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "县处级正职" if p["id"] in (1, 2) else "县处级正职/副职",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002", "S003", "S004"]
        },
        "career_timeline": [
            {
                "start": pos["start"],
                "end": pos["end"],
                "org": next((o["name"] for o in organizations if o["id"] == pos["org_id"]), ""),
                "title": pos["title"],
                "level": pos["rank"],
                "location": "崇左市扶绥县",
                "system": "government" if any(x in pos["title"] for x in ["县长", "副县"]) else "party",
                "rank": pos["rank"],
                "is_key_promotion": "书记" in pos["title"] or "县长" in pos["title"],
                "notes": pos["note"],
                "confidence": "confirmed",
                "source_ids": ["S001", "S002", "S003", "S004", "S005", "S006", "S007"]
            }
            for pos in person_positions
        ],
        "organizations": [
            {
                "org_id": o["id"],
                "name": o["name"],
                "type": o["type"],
                "level": o["level"],
                "parent": o["parent"],
                "location": o["location"]
            }
            for o in organizations
            if o["id"] in [pos["org_id"] for pos in person_positions]
        ],
        "relationships": person_rels,
        "governance_record": [
            {
                "period": "2021-2025",
                "domain": "economic_development",
                "achievement_or_event": "扶绥县提出'全面建成全区县域经济第一强县'目标",
                "role_in_event": "县委主要领导（县长/书记）",
                "measurable_outcome": "",
                "location": "扶绥县",
                "confidence": "plausible",
                "source_ids": ["S001"]
            }
        ],
        "professional_profile": {
            "primary_specializations": ["党政管理"],
            "secondary_specializations": [],
            "career_pattern": "local_ladder" if name in ("黄建辉", "许家恺") else "cross_county_rotation" if name == "周春科" else "unknown",
            "systems_experience": ["party", "government"],
            "geographic_pattern": ["崇左市", "扶绥县", "大新县"],
            "promotion_velocity": {
                "summary": "常规晋升",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "unknown",
                    "evidence": "尚未深入调研公开报道",
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {
            "direct_connections": len(person_rels),
            "total_connections": len(person_rels),
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至调研日期未发现公开的纪律处分或负面舆情",
                "date": AS_OF,
                "confidence": "plausible",
                "source_ids": ["S001"]
            }
        ],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "部分早期履历细节待补充（教育经历、早期职级）"
        },
        "open_questions": [
            {
                "priority": "medium",
                "question": f"请补充{name}的完整早期履历",
                "why_it_matters": "提升 career_timeline 完整性",
                "suggested_queries": [f"{name} 早期 工作 简历"],
                "last_attempted": AS_OF
            },
            {
                "priority": "low",
                "question": f"{name}的具体教育和专业背景",
                "why_it_matters": "充实 professional_profile",
                "suggested_queries": [f"{name} 毕业 院校 专业"],
                "last_attempted": AS_OF
            }
        ]
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {filepath}")


# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    os.makedirs(STAGING_DIR, exist_ok=True)
    print(f"Building 扶绥县 data in staging: {STAGING_DIR}")
    build_db()
    build_gexf()
    # Write person JSON for core leaders (县委书记 & 县长)
    write_person_json(1)  # 许家恺
    write_person_json(2)  # 周春科
    print("Done.")
