#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
北海市海城区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 市辖区
Province: 广西壮族自治区
Parent City: 北海市
Region: 海城区
Targets: 区委书记 & 区长

当前在任 (as of 2026-07-23):
- 区委书记: 陈文初 (2025.07-，原区长晋升)
- 区长/代理区长: 覃燕妮 (女，2025.07.17-，代理区长)
"""

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "海城区"
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-23"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：区委书记 (2025.07-)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "陈文初",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年6月",
        "birthplace": "广西北海",
        "education": "大学学历，法学学士（广西大学法学院）",
        "party_join": "1997年6月",
        "work_start": "1997年7月",
        "current_post": "北海市海城区委书记",
        "current_org": "中共北海市海城区委员会",
        "source": "https://www.thepaper.cn/newsDetail_forward_19565967"
    },
    # ════════════════════════════════════════
    # 核心领导：区长/代理区长 (2025.07.17-)
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "覃燕妮",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982年10月",
        "birthplace": "广西贵港覃塘",
        "education": "工学学士、管理学学士，广西大学公共管理学院在职研究生",
        "party_join": "2002年10月",
        "work_start": "2005年7月",
        "current_post": "北海市海城区人民政府副区长、代理区长",
        "current_org": "北海市海城区人民政府",
        "source": "http://www.gxcounty.com/e/DoPrint/?classid=30&id=183594"
    },
    # ════════════════════════════════════════
    # 前任区委书记 (～2025.07)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "祝小东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原海城区委书记（去向待查）",
        "current_org": "中共北海市海城区委员会",
        "source": "GAP — inferred from 陈文初晋升接任"
    },
    # ════════════════════════════════════════
    # 前任区长 (2020-2022, 被免职)
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "苏矿峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年4月",
        "birthplace": "广西合浦",
        "education": "在职研究生学历，理学硕士，经济师",
        "party_join": "1995年12月",
        "work_start": "1997年7月",
        "current_post": "原海城区区长（2022.07被免职）",
        "current_org": "北海市海城区人民政府",
        "source": "https://www.nbd.com.cn/articles/2022-07-17/2368168.html"
    },
    # ════════════════════════════════════════
    # 区委常委、常务副区长
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "张英毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年3月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海城区委常委、常务副区长",
        "current_org": "北海市海城区人民政府",
        "source": "海城区政府领导之窗"
    },
    # ════════════════════════════════════════
    # 副区长
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "郭立冬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海城区副区长",
        "current_org": "北海市海城区人民政府",
        "source": "海城区政府领导之窗"
    },
    {
        "id": 7,
        "name": "陈流芳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海城区副区长",
        "current_org": "北海市海城区人民政府",
        "source": "海城区政府领导之窗"
    },
    {
        "id": 8,
        "name": "黎建杨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海城区副区长",
        "current_org": "北海市海城区人民政府",
        "source": "海城区政府领导之窗"
    },
    {
        "id": 9,
        "name": "杨贞纯",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984年8月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海城区副区长",
        "current_org": "北海市海城区人民政府",
        "source": "海城区政府领导之窗"
    },
    {
        "id": 10,
        "name": "吴春雄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海城区副区长",
        "current_org": "北海市海城区人民政府",
        "source": "海城区政府领导之窗"
    },
    {
        "id": 11,
        "name": "马璐璐",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海城区副区长",
        "current_org": "北海市海城区人民政府",
        "source": "海城区政府领导之窗"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共北海市海城区委员会", "type": "党委", "level": "正处级", "parent": "中共北海市委员会", "location": "北海市海城区"},
    {"id": 2, "name": "北海市海城区人民政府", "type": "政府", "level": "正处级", "parent": "北海市人民政府", "location": "北海市海城区"},
    {"id": 3, "name": "中共北海市海城区纪律检查委员会", "type": "纪委", "level": "副处级", "parent": "中共北海市纪律检查委员会", "location": "北海市海城区"},
    {"id": 4, "name": "中共北海市海城区委组织部", "type": "党委", "level": "正科级", "parent": "中共北海市海城区委员会", "location": "北海市海城区"},
    {"id": 5, "name": "北海市科学技术局", "type": "政府", "level": "正处级", "parent": "北海市人民政府", "location": "北海市"},
    {"id": 6, "name": "共青团北海市委员会", "type": "群团", "level": "正处级", "parent": "共青团广西壮族自治区委员会", "location": "北海市"},
    {"id": 7, "name": "广西北海市铁山港区人民政府", "type": "政府", "level": "正处级", "parent": "北海市人民政府", "location": "北海市铁山港区"},
    {"id": 8, "name": "中共北海市铁山港区委员会", "type": "党委", "level": "正处级", "parent": "中共北海市委员会", "location": "北海市铁山港区"},
    {"id": 9, "name": "北海市交通运输局", "type": "政府", "level": "正处级", "parent": "北海市人民政府", "location": "北海市"},
]

# =========================================================================
# 3. POSITIONS (career timeline entries as position records)
# =========================================================================
positions = [
    # ── 陈文初 (id=1) ──
    {"person_id": 1, "org_id": 7, "title": "铁山港区司法局副局长、法制办副主任（兼）", "start_date": "2002.04", "end_date": "2003.03", "rank": "副科级", "note": ""},
    {"person_id": 1, "org_id": 7, "title": "铁山港区政府办副主任，法制办主任（正科级）", "start_date": "2003.03", "end_date": "2005.07", "rank": "正科级", "note": ""},
    {"person_id": 1, "org_id": 7, "title": "铁山港区司法局局长、调处办主任", "start_date": "2005.07", "end_date": "2011.07", "rank": "正科级", "note": ""},
    {"person_id": 1, "org_id": 7, "title": "铁山港区副区长", "start_date": "2011.07", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "铁山港区委常委、政法委书记", "start_date": "", "end_date": "2021.04", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "铁山港区委副书记", "start_date": "", "end_date": "2021.04", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "北海市交通运输局党组书记", "start_date": "2021.04", "end_date": "2021.06", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "北海市交通运输局局长、党组书记", "start_date": "2021.06", "end_date": "2022.07", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "海城区委副书记、代区长", "start_date": "2022.08", "end_date": "2022.10", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "海城区委副书记、区长", "start_date": "2022.10", "end_date": "2025.07", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "海城区委书记", "start_date": "2025.07", "end_date": "present", "rank": "正处级", "note": ""},

    # ── 覃燕妮 (id=2) ──
    {"person_id": 2, "org_id": 7, "title": "合浦县发展和改革局副局长", "start_date": "2009.08", "end_date": "2010.01", "rank": "副科级", "note": "企业人事关系挂靠人才市场（2005.07-2009.08）后进入公务员系统"},
    {"person_id": 2, "org_id": 7, "title": "合浦县发展和改革局副局长、党组成员", "start_date": "2010.01", "end_date": "2011.07", "rank": "副科级", "note": ""},
    {"person_id": 2, "org_id": 6, "title": "共青团合浦县委副书记", "start_date": "2011.07", "end_date": "2011.11", "rank": "副科级", "note": ""},
    {"person_id": 2, "org_id": 6, "title": "共青团合浦县委员会书记", "start_date": "2011.11", "end_date": "2013.04", "rank": "正科级", "note": ""},
    {"person_id": 2, "org_id": 7, "title": "星岛湖乡党委副书记、乡长（候选人）", "start_date": "2013.04", "end_date": "2015.06", "rank": "正科级", "note": ""},
    {"person_id": 2, "org_id": 8, "title": "中共合浦县星岛湖乡党委书记", "start_date": "2015.06", "end_date": "2016.05", "rank": "正科级", "note": "乡镇一把手"},
    {"person_id": 2, "org_id": 8, "title": "合浦县委办公室副主任（正科长级）", "start_date": "2016.05", "end_date": "2016.07", "rank": "正科级", "note": ""},
    {"person_id": 2, "org_id": 6, "title": "共青团北海市委员会副书记、党组成员", "start_date": "2016.07", "end_date": "2024.01", "rank": "副处级", "note": "约7.5年"},
    {"person_id": 2, "org_id": 5, "title": "北海市科学技术局局长", "start_date": "2024.01", "end_date": "2024.03", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 5, "title": "北海市科学技术局党组书记、局长", "start_date": "2024.03", "end_date": "2025.07", "rank": "正处级", "note": "党政一肩挑"},
    {"person_id": 2, "org_id": 2, "title": "海城区副区长、代理区长", "start_date": "2025.07.17", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "海城区委副书记", "start_date": "2025.07", "end_date": "present", "rank": "副处级", "note": ""},

    # ── 祝小东 (id=3) ──
    {"person_id": 3, "org_id": 1, "title": "海城区委书记", "start_date": "", "end_date": "2025.07", "rank": "正处级", "note": "GAP — 任期起止和详细履历待查"},

    # ── 苏矿峰 (id=4) ──
    {"person_id": 4, "org_id": 2, "title": "海城区区长", "start_date": "2020", "end_date": "2022.07", "rank": "正处级", "note": "2022.07因疫情防控不力被免职"},

    # ── 张英毅 (id=5) ──
    {"person_id": 5, "org_id": 2, "title": "海城区常务副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "海城区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # ── 郭立冬 (id=6) ──
    {"person_id": 6, "org_id": 2, "title": "海城区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # ── 陈流芳 (id=7) ──
    {"person_id": 7, "org_id": 2, "title": "海城区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # ── 黎建杨 (id=8) ──
    {"person_id": 8, "org_id": 2, "title": "海城区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # ── 杨贞纯 (id=9) ──
    {"person_id": 9, "org_id": 2, "title": "海城区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # ── 吴春雄 (id=10) ──
    {"person_id": 10, "org_id": 2, "title": "海城区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # ── 马璐璐 (id=11) ──
    {"person_id": 11, "org_id": 2, "title": "海城区副区长", "start_date": "2025.12", "end_date": "present", "rank": "副处级", "note": ""},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 陈文初 ↔ 覃燕妮 — 前后任区长/党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "前后任", "context": "陈文初晋升区委书记，覃燕妮接任代理区长", "overlap_org": "海城区四套班子", "overlap_period": "2025.07-"},
    # 陈文初 ↔ 祝小东 — 前后任区委书记
    {"person_a": 1, "person_b": 3, "type": "前后任", "context": "陈文初接替祝小东任区委书记", "overlap_org": "中共海城区委员会", "overlap_period": "2025.07"},
    # 陈文初 ↔ 苏矿峰 — 前后任区长
    {"person_a": 1, "person_b": 4, "type": "前后任", "context": "陈文初接替苏矿峰（被免职）任区长", "overlap_org": "海城区人民政府", "overlap_period": "2022.08"},
    # 陈文初 ↔ 张英毅 — 上下级
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "陈文初任区长/区委书记期间，张英毅为常务副区长/区委常委", "overlap_org": "海城区委常委会", "overlap_period": "2025.07-"},
    # 陈文初 ↔ 郭立冬 — 上下级
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "陈文初任区长/区委书记期间，郭立冬为副区长", "overlap_org": "海城区人民政府", "overlap_period": "2022.10-"},
    # 覃燕妮 ↔ 张英毅 — 上下级
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "覃燕妮为代理区长，张英毅为常务副区长", "overlap_org": "海城区人民政府", "overlap_period": "2025.07-"},
    # 覃燕妮 ↔ 郭立冬 — 上下级
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "覃燕妮代理区长期间，郭立冬为副区长", "overlap_org": "海城区人民政府", "overlap_period": "2025.07-"},
    # 陈文初 ↔ 陈流芳 — 上下级
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "陈流芳为副区长", "overlap_org": "海城区人民政府", "overlap_period": "2022.10-"},
    # 陈文初 ↔ 黎建杨 — 上下级
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "黎建杨为副区长", "overlap_org": "海城区人民政府", "overlap_period": "2022.10-"},
    # 陈文初 ↔ 杨贞纯 — 上下级
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "杨贞纯为副区长", "overlap_org": "海城区人民政府", "overlap_period": "2022.10-"},
    # 陈文初 ↔ 吴春雄 — 上下级
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "吴春雄为副区长", "overlap_org": "海城区人民政府", "overlap_period": "2022.10-"},
    # 陈文初 ↔ 马璐璐 — 上下级
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "马璐璐为副区长（2025.12任）", "overlap_org": "海城区人民政府", "overlap_period": "2025.12-"},
]

# =========================================================================
# 5. BUILD DATABASE
# =========================================================================

def build_database():
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    # Create tables
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '',
            party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '',
            source TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    # Insert persons
    for p in persons:
        cur.execute(
            """INSERT OR REPLACE INTO persons
               (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
             p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"])
        )

    # Insert organizations
    for o in organizations:
        cur.execute(
            """INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
               VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
        )

    # Insert positions
    for pos in positions:
        cur.execute(
            """INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note)
               VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"])
        )

    # Insert relationships
    for r in relationships:
        cur.execute(
            """INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
               VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
        )

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")


# =========================================================================
# 6. BUILD GEXF
# =========================================================================

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return 'r,g,b' string based on role."""
    title = p.get("current_post", "")
    if "书记" in title and "区委书记" in title:
        return "255,50,50"  # Red
    if "区长" in title or "代理区长" in title:
        return "50,100,255"  # Blue
    if "纪委书记" in title:
        return "255,165,0"  # Orange
    return "100,100,100"  # Grey

def org_color(o):
    """Return 'r,g,b' string based on org type."""
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "纪委" in t:
        return "255,200,200"
    if "群团" in t:
        return "255,220,255"
    return "200,200,200"

def is_top_leader(p):
    title = p.get("current_post", "")
    return "书记" in title or "区长" in title or "代理区长" in title

def person_size(p):
    return "20.0" if is_top_leader(p) else "12.0"

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation build script</creator>')
    lines.append(f'    <description>北海市海城区领导班子工作关系网络 (as of {AS_OF})</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: Persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: Organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level",""))}"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append(f'          <attvalue for="4" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    # person -> organization (worked_at)
    for pos in positions:
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos.get("start_date",""))} - {esc(pos.get("end_date",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    # person <-> person (relationships)
    for r in relationships:
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {GEXF_PATH}")


# =========================================================================
# 7. MAIN
# =========================================================================

if __name__ == "__main__":
    build_database()
    build_gexf()
    print("Done.")
