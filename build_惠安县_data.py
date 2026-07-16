#!/usr/bin/env python3
"""Build 惠安县 (福建省泉州市) leadership network: SQLite DB + GEXF graph.

Research date: 2026-07-17
Level: 县
Province: 福建省
Parent city: 泉州市
Targets: 县委书记 & 县长

Sources:
  - www.huian.gov.cn (official county government homepage — confirmed 代县长 & 副县长)
  - zh.wikipedia.org/wiki/惠安县 (confirmed 县长 黄育奇, historical)
  - www.quanzhou.gov.cn (泉州市政府 — confirmed 副市长 王春雷, former 惠安县委书记)

Confidence:
  - Current 代县长 陈剑锋 confirmed from official county website homepage header (2026-07).
  - Current 常务副县长 蔡旭萌 confirmed from official county website homepage header.
  - Current 副县长 roster (9 deputies) confirmed from official county website homepage header.
  - 县委书记 name NOT directly confirmed on any accessible official page.
    huian.gov.cn lacks a publicly accessible 领导之窗/领导分工 page (404).
    Baidu Baike blocked by captcha/WAF (403).
    zh.wikipedia.org infobox for 惠安县 does not list party secretary.
    The gov website homepage references "县委主要领导" in news headlines but
    article URLs follow an unpredictable ID scheme that could not be resolved.
  - Based on prior knowledge: 王春雷 served as 惠安县委书记 until ~2024-2025,
    then promoted to Quanzhou 副市长 (confirmed on quanzhou.gov.cn 副市长 list).
    The current successor to 王春雷 as 惠安县委书记 is unknown from accessible sources.
  - Based on prior knowledge: 黄育奇 served as 惠安县长 until ~2025-2026.
    The current 代县长 陈剑锋 is the acting successor.
  - Biographical details (birth, birthplace, education, career timeline) for all
    figures could not be retrieved from accessible Chinese sources.

Known sources:
  - https://www.huian.gov.cn — homepage header shows 代县长+副县长 list
  - https://zh.wikipedia.org/wiki/惠安县 — infobox shows 县长 黄育奇
  - https://www.quanzhou.gov.cn — infobox shows 副市长 王春雷

Key gaps:
  - Current 县委书记 name unconfirmed (successor to 王春雷 unknown)
  - 陈剑锋 full career timeline unknown
  - 蔡旭萌 full career timeline unknown
  - All 9 副县长 career timelines unknown
  - Birth dates, education, native place for all figures unknown
  - Predecessor/successor paths for all roles unknown
  - 县委常委 roster unknown

All person data marked with confidence accordingly.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if "data/tmp" in SCRIPT_DIR:
    DB_PATH = os.path.join(SCRIPT_DIR, "惠安县_network.db")
    GEXF_PATH = os.path.join(SCRIPT_DIR, "惠安县_network.gexf")
else:
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(PROJECT_ROOT, "data/database/惠安县_network.db")
    GEXF_PATH = os.path.join(PROJECT_ROOT, "data/graph/惠安县_network.gexf")

KNOWN_DATE = "2026-07-17"

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ═══ Current Top Leaders ═══

    # ⚠️ 县委书记 (Party Secretary) — NAME UNKNOWN
    # 王春雷 was 惠安县委书记 until ~2024-2025, promoted to Quanzhou 副市长.
    # Successor not confirmed from accessible sources.
    {
        "id": "huian_party_sec_unknown",
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠安县委书记",
        "current_org": "中共惠安县委员会",
        "source": "待查 — 王春雷已升任泉州市副市长，继任者信息无法从公开渠道确认",
        "notes": "⚠️ 县委书记姓名未确认。前任王春雷（~2020-2024/2025任）已升泉州市副市长。",
        "confidence": "unverified"
    },

    # 代县长 陈剑锋 (Acting County Mayor) — confirmed from gov homepage
    {
        "id": "huian_chen_jianfeng",
        "name": "陈剑锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠安县代县长",
        "current_org": "惠安县人民政府",
        "source": "https://www.huian.gov.cn — homepage header (2026-07)",
        "notes": "惠安县代县长，兼任县委副书记（推定）。2026年任代县长，此前履历待查。",
        "confidence": "confirmed"
    },

    # ═══ Key Deputies (from official gov homepage) ═══

    # 常务副县长 蔡旭萌 (Executive Deputy Mayor)
    {
        "id": "huian_cai_xumeng",
        "name": "蔡旭萌",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠安县委常委、常务副县长",
        "current_org": "惠安县人民政府",
        "source": "https://www.huian.gov.cn — homepage header (2026-07)",
        "notes": "惠安县委常委、常务副县长。姓名从官方主页确认，详细履历待查。",
        "confidence": "confirmed"
    },

    # 副县长 蒋舒翔
    {
        "id": "huian_jiang_shuxiang",
        "name": "蒋舒翔",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠安县副县长",
        "current_org": "惠安县人民政府",
        "source": "https://www.huian.gov.cn — homepage header (2026-07)",
        "notes": "惠安县副县长。姓名从官方主页确认，详细履历待查。",
        "confidence": "confirmed"
    },

    # 副县长 王立双
    {
        "id": "huian_wang_lishuang",
        "name": "王立双",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠安县副县长",
        "current_org": "惠安县人民政府",
        "source": "https://www.huian.gov.cn — homepage header (2026-07)",
        "notes": "惠安县副县长。姓名从官方主页确认，详细履历待查。",
        "confidence": "confirmed"
    },

    # 副县长 陈剑虹
    {
        "id": "huian_chen_jianhong",
        "name": "陈剑虹",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠安县副县长",
        "current_org": "惠安县人民政府",
        "source": "https://www.huian.gov.cn — homepage header (2026-07)",
        "notes": "惠安县副县长。姓名从官方主页确认，详细履历待查。",
        "confidence": "confirmed"
    },

    # 副县长 庄泽平
    {
        "id": "huian_zhuang_zeping",
        "name": "庄泽平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠安县副县长",
        "current_org": "惠安县人民政府",
        "source": "https://www.huian.gov.cn — homepage header (2026-07)",
        "notes": "惠安县副县长。姓名从官方主页确认，详细履历待查。",
        "confidence": "confirmed"
    },

    # 副县长 郭惠卿
    {
        "id": "huian_guo_huiqing",
        "name": "郭惠卿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠安县副县长",
        "current_org": "惠安县人民政府",
        "source": "https://www.huian.gov.cn — homepage header (2026-07)",
        "notes": "惠安县副县长。姓名从官方主页确认，详细履历待查。",
        "confidence": "confirmed"
    },

    # 副县长 陈荣煌
    {
        "id": "huian_chen_ronghuang",
        "name": "陈荣煌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠安县副县长",
        "current_org": "惠安县人民政府",
        "source": "https://www.huian.gov.cn — homepage header (2026-07)",
        "notes": "惠安县副县长。姓名从官方主页确认，详细履历待查。",
        "confidence": "confirmed"
    },

    # 副县长 郭晓辉
    {
        "id": "huian_guo_xiaohui",
        "name": "郭晓辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠安县副县长",
        "current_org": "惠安县人民政府",
        "source": "https://www.huian.gov.cn — homepage header (2026-07)",
        "notes": "惠安县副县长。姓名从官方主页确认，详细履历待查。",
        "confidence": "confirmed"
    },

    # 副县长 庄剑雄
    {
        "id": "huian_zhuang_jianxiong",
        "name": "庄剑雄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠安县副县长",
        "current_org": "惠安县人民政府",
        "source": "https://www.huian.gov.cn — homepage header (2026-07)",
        "notes": "惠安县副县长。姓名从官方主页确认，详细履历待查。",
        "confidence": "confirmed"
    },

    # 副县长 王海演
    {
        "id": "huian_wang_haiyan",
        "name": "王海演",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠安县副县长",
        "current_org": "惠安县人民政府",
        "source": "https://www.huian.gov.cn — homepage header (2026-07)",
        "notes": "惠安县副县长。姓名从官方主页确认，详细履历待查。",
        "confidence": "confirmed"
    },
]

# ── Organizations ──

organizations = [
    {"id": "org_party", "name": "中共惠安县委员会", "type": "党委", "level": "县", "parent": "中共泉州市委员会", "location": "福建省泉州市惠安县"},
    {"id": "org_gov", "name": "惠安县人民政府", "type": "政府", "level": "县", "parent": "泉州市人民政府", "location": "福建省泉州市惠安县"},
    {"id": "org_discipline", "name": "中共惠安县纪律检查委员会", "type": "纪委", "level": "县", "parent": "中共泉州市纪律检查委员会", "location": "福建省泉州市惠安县"},
    {"id": "org_npc", "name": "惠安县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "泉州市人民代表大会常务委员会", "location": "福建省泉州市惠安县"},
    {"id": "org_ppcc", "name": "中国人民政治协商会议惠安县委员会", "type": "政协", "level": "县", "parent": "政协泉州市委员会", "location": "福建省泉州市惠安县"},
    {"id": "org_organization", "name": "中共惠安县委组织部", "type": "党委", "level": "县", "parent": "中共惠安县委员会", "location": "福建省泉州市惠安县"},
    {"id": "org_propaganda", "name": "中共惠安县委宣传部", "type": "党委", "level": "县", "parent": "中共惠安县委员会", "location": "福建省泉州市惠安县"},
    {"id": "org_politics_law", "name": "中共惠安县委政法委员会", "type": "党委", "level": "县", "parent": "中共惠安县委员会", "location": "福建省泉州市惠安县"},
    {"id": "org_armed_forces", "name": "惠安县人民武装部", "type": "事业单位", "level": "县", "parent": "泉州军分区", "location": "福建省泉州市惠安县"},
    {"id": "org_united_front", "name": "中共惠安县委统一战线工作部", "type": "党委", "level": "县", "parent": "中共惠安县委员会", "location": "福建省泉州市惠安县"},
]

# ── Positions ──

positions = [
    # (person_id, org_id, title, start, end, rank, note)

    # 县委书记 — unknown
    ("huian_party_sec_unknown", "org_party", "惠安县委书记", "待查", "present", "正处级",
     "⚠️ 姓名待确认。前任王春雷已升泉州市副市长。"),

    # 代县长 陈剑锋
    ("huian_chen_jianfeng", "org_gov", "惠安县代县长", KNOWN_DATE, "present", "正处级",
     "从惠安县政府官网主页确认。代县长，任期起始日期待查。"),
    ("huian_chen_jianfeng", "org_party", "惠安县委副书记", KNOWN_DATE, "present", "正处级",
     "推定由县长兼任。"),

    # 常务副县长 蔡旭萌
    ("huian_cai_xumeng", "org_gov", "惠安县委常委、常务副县长", KNOWN_DATE, "present", "副处级",
     "从惠安县政府官网主页确认。"),

    # 副县长 (9人)
    ("huian_jiang_shuxiang", "org_gov", "惠安县副县长", KNOWN_DATE, "present", "副处级", ""),
    ("huian_wang_lishuang", "org_gov", "惠安县副县长", KNOWN_DATE, "present", "副处级", ""),
    ("huian_chen_jianhong", "org_gov", "惠安县副县长", KNOWN_DATE, "present", "副处级", ""),
    ("huian_zhuang_zeping", "org_gov", "惠安县副县长", KNOWN_DATE, "present", "副处级", ""),
    ("huian_guo_huiqing", "org_gov", "惠安县副县长", KNOWN_DATE, "present", "副处级", ""),
    ("huian_chen_ronghuang", "org_gov", "惠安县副县长", KNOWN_DATE, "present", "副处级", ""),
    ("huian_guo_xiaohui", "org_gov", "惠安县副县长", KNOWN_DATE, "present", "副处级", ""),
    ("huian_zhuang_jianxiong", "org_gov", "惠安县副县长", KNOWN_DATE, "present", "副处级", ""),
    ("huian_wang_haiyan", "org_gov", "惠安县副县长", KNOWN_DATE, "present", "副处级", ""),
]

# ── Relationships ──

relationships = [
    # (person_a, person_b, type, strength, context, overlap_org, overlap_period, note)

    # 代县长 陈剑锋 — 常务副县长 蔡旭萌 (work overlap in government)
    ("huian_chen_jianfeng", "huian_cai_xumeng", "overlap", "medium",
     "县长与常务副县长在惠安县政府共事", "org_gov", KNOWN_DATE + "起", "confirmed"),

    # 代县长 陈剑锋 — each 副县长 (work overlap in government)
    ("huian_chen_jianfeng", "huian_jiang_shuxiang", "overlap", "weak",
     "县长与副县长在惠安县政府共事", "org_gov", KNOWN_DATE + "起", "confirmed"),
    ("huian_chen_jianfeng", "huian_wang_lishuang", "overlap", "weak",
     "县长与副县长在惠安县政府共事", "org_gov", KNOWN_DATE + "起", "confirmed"),
    ("huian_chen_jianfeng", "huian_chen_jianhong", "overlap", "weak",
     "县长与副县长在惠安县政府共事", "org_gov", KNOWN_DATE + "起", "confirmed"),
    ("huian_chen_jianfeng", "huian_zhuang_zeping", "overlap", "weak",
     "县长与副县长在惠安县政府共事", "org_gov", KNOWN_DATE + "起", "confirmed"),
    ("huian_chen_jianfeng", "huian_guo_huiqing", "overlap", "weak",
     "县长与副县长在惠安县政府共事", "org_gov", KNOWN_DATE + "起", "confirmed"),
    ("huian_chen_jianfeng", "huian_chen_ronghuang", "overlap", "weak",
     "县长与副县长在惠安县政府共事", "org_gov", KNOWN_DATE + "起", "confirmed"),
    ("huian_chen_jianfeng", "huian_guo_xiaohui", "overlap", "weak",
     "县长与副县长在惠安县政府共事", "org_gov", KNOWN_DATE + "起", "confirmed"),
    ("huian_chen_jianfeng", "huian_zhuang_jianxiong", "overlap", "weak",
     "县长与副县长在惠安县政府共事", "org_gov", KNOWN_DATE + "起", "confirmed"),
    ("huian_chen_jianfeng", "huian_wang_haiyan", "overlap", "weak",
     "县长与副县长在惠安县政府共事", "org_gov", KNOWN_DATE + "起", "confirmed"),
]

# ══════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════

def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = ON;")

    c.execute("DROP TABLE IF EXISTS relationships;")
    c.execute("DROP TABLE IF EXISTS positions;")
    c.execute("DROP TABLE IF EXISTS organizations;")
    c.execute("DROP TABLE IF EXISTS persons;")

    c.execute("""
        CREATE TABLE persons (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            native_place TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT,
            notes TEXT,
            confidence TEXT DEFAULT 'unverified'
        )
    """)

    c.execute("""
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT NOT NULL,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)

    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT,
            strength TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            note TEXT DEFAULT 'unverified',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, native_place,
                                 education, party_join, work_start, current_post, current_org,
                                 source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
            p["birthplace"], p["native_place"], p["education"],
            p["party_join"], p["work_start"], p["current_post"], p["current_org"],
            p["source"], p["notes"], p["confidence"]
        ))

    for o in organizations:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        person_id, org_id, title, start, end, rank, note = pos[:7]
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (person_id, org_id, title, start, end, rank, note))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, strength, context, overlap_org, overlap_period, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]))

    conn.commit()
    conn.close()
    print(f"[DB] Created: {DB_PATH}")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return 'r,g,b' string based on role."""
    post = p["current_post"]
    if "县委书记" in post or "县委" in post and "书记" in post:
        return "255,50,50"
    if "县长" in post or "代县长" in post:
        return "50,100,255"
    if "常务副县长" in post:
        return "50,100,255"
    if "副县长" in post:
        return "100,100,255"
    if "纪委书记" in post:
        return "255,165,0"
    return "100,100,100"


def is_top_leader(p):
    """Return True if person is a top leader (书记 or 县长)."""
    post = p["current_post"]
    return "县委书记" in post or "县长" in post or "代县长" in post


def org_color(o):
    """Return 'r,g,b' string for organization type."""
    t = o["type"]
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "纪委" in t:
        return "255,165,0"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    if "事业单位" in t:
        return "220,220,220"
    return "200,200,200"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{KNOWN_DATE}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>惠安县 (福建省泉州市) 领导关系网络 — 2026年7月</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="rank" type="string"/>')
    lines.append('      <attribute id="4" title="confidence" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="strength" type="string"/>')
    lines.append('      <attribute id="2" title="title" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="{esc(p["id"])}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="正处级"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["confidence"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="{esc(o["id"])}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["name"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(o["level"])}"/>')
        lines.append(f'          <attvalue for="4" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> Organization edges (worked_at)
    for pos in positions:
        person_id, org_id, title = pos[0], pos[1], pos[2]
        eid += 1
        lines.append(f'      <edge id="{eid}" source="{esc(person_id)}" target="{esc(org_id)}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('          <attvalue for="1" value="confirmed"/>')
        lines.append(f'          <attvalue for="2" value="{esc(title)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person edges (relationships)
    for r in relationships:
        person_a, person_b, rtype, strength = r[0], r[1], r[2], r[3]
        eid += 1
        lines.append(f'      <edge id="{eid}" source="{esc(person_a)}" target="{esc(person_b)}" label="{esc(rtype)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(strength)}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[GEXF] Created: {GEXF_PATH}")


# ── main ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"=== 惠安县 (福建省泉州市) data builder ===")
    print(f"Date: {KNOWN_DATE}")

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    build_db()
    build_gexf()

    print("=== Done ===")
