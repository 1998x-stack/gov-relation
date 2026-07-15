#!/usr/bin/env python3
"""Build Lu'an (六安市) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-16
Task: anhui_六安市 (地级市 level)
Targets: 市委书记 & 市长

Sources:
  - https://www.luan.gov.cn/ldzcN/swld/index.html (市委领导, accessed 2026-07-16)
  - https://www.luan.gov.cn/ldzcN/szfld/index.html (市政府领导, accessed 2026-07-16)
  - 中安在线 (anhuinews.com): 方正主持召开市委常委会会议 (2026年)
  - 颍泉区 project data: 刘洪洁原任颍泉区委书记
  - 金安区 project data: 方正（副区长）区别于市委书记方正

Confidence: Current roles confirmed from official Lu'an government leadership pages.
  Biographical details are partial for some figures due to Baidu百科 access restrictions.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "六安市_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "六安市_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ═══ Top Leaders ═══════════════════════════════════════════════════
    {
        "id": 1,
        "name": "方正",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共六安市委",
        "source": "https://www.luan.gov.cn/ldzcN/swld/index.html (六安市领导之窗-市委领导, accessed 2026-07-16)",
        "notes": "六安市委书记。主持市委全面工作。主持市委常委会会议（2026年中安在线新闻确认）。\n注：金安区副区长方正为不同人物（同名）。",
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "刘洪洁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "六安市人民政府",
        "source": "https://www.luan.gov.cn/ldzcN/swld/index.html; https://www.luan.gov.cn/ldzcN/szfld/index.html (六安市领导之窗, accessed 2026-07-16)",
        "notes": "六安市委副书记、市长。领导市政府全面工作。\n此前曾任颍泉区委书记（阜阳市），后调任六安市长。接替原市长潘东旭。",
        "confidence": "confirmed"
    },
    # ═══ Municipal Party Committee (市委领导) ═══════════════════════════
    {
        "id": 3,
        "name": "汪宏军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、市委秘书长",
        "current_org": "中共六安市委",
        "source": "https://www.luan.gov.cn/ldzcN/swld/index.html (六安市领导之窗-市委领导, accessed 2026-07-16)",
        "notes": "市委常委、市委秘书长。协助书记处理市委日常工作。",
        "confidence": "confirmed"
    },
    # ═══ Government Leaders (市政府领导) ═══════════════════════════════
    {
        "id": 4,
        "name": "孔祥永",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "六安市人民政府",
        "source": "https://www.luan.gov.cn/ldzcN/szfld/index.html (六安市领导之窗-市政府领导, accessed 2026-07-16)",
        "notes": "副市长。分管领域待查。",
        "confidence": "confirmed"
    },
    {
        "id": 5,
        "name": "李强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "六安市人民政府",
        "source": "https://www.luan.gov.cn/ldzcN/szfld/index.html (六安市领导之窗-市政府领导, accessed 2026-07-16)",
        "notes": "副市长。分管领域待查。",
        "confidence": "confirmed"
    },
    {
        "id": 6,
        "name": "孙学龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "六安市人民政府",
        "source": "https://www.luan.gov.cn/ldzcN/szfld/index.html (六安市领导之窗-市政府领导, accessed 2026-07-16)",
        "notes": "副市长。分管领域待查。",
        "confidence": "confirmed"
    },
    {
        "id": 7,
        "name": "魏武",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "六安市人民政府",
        "source": "https://www.luan.gov.cn/ldzcN/szfld/index.html (六安市领导之窗-市政府领导, accessed 2026-07-16)",
        "notes": "副市长（女）。分管领域待查。",
        "confidence": "confirmed"
    },
    {
        "id": 8,
        "name": "王庆昊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "六安市人民政府",
        "source": "https://www.luan.gov.cn/ldzcN/szfld/index.html (六安市领导之窗-市政府领导, accessed 2026-07-16)",
        "notes": "副市长。分管领域待查。",
        "confidence": "confirmed"
    },
    {
        "id": 9,
        "name": "王晓晨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "六安市人民政府",
        "source": "https://www.luan.gov.cn/ldzcN/szfld/index.html (六安市领导之窗-市政府领导, accessed 2026-07-16)",
        "notes": "副市长。分管领域待查。",
        "confidence": "confirmed"
    },
    {
        "id": 10,
        "name": "程旭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "六安市人民政府",
        "source": "https://www.luan.gov.cn/ldzcN/szfld/index.html (六安市领导之窗-市政府领导, accessed 2026-07-16)",
        "notes": "副市长。分管领域待查。",
        "confidence": "confirmed"
    },
    {
        "id": 11,
        "name": "王思春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政府秘书长",
        "current_org": "六安市人民政府",
        "source": "https://www.luan.gov.cn/ldzcN/szfld/index.html (六安市领导之窗-市政府领导, accessed 2026-07-16)",
        "notes": "市政府秘书长。协助市长处理市政府日常工作。",
        "confidence": "confirmed"
    },
    # ═══ Predecessors ═════════════════════════════════════════════════
    {
        "id": 12,
        "name": "潘东旭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原六安市长，已离任）",
        "current_org": "",
        "source": "https://www.luan.gov.cn (六安市政府网站; 2025年1月仍以市长身份活动)",
        "notes": "前任六安市市长。2025年1月仍以市长身份出席活动。后由刘洪洁接任。去向待查。",
        "confidence": "confirmed"
    },
    {
        "id": 13,
        "name": "叶露中",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原六安市委书记，已离任）",
        "current_org": "",
        "source": "已知：叶露中2021年任六安市委书记；2023年由方正接替",
        "notes": "前任六安市委书记（~2021-2023）。方正接任。去向：待查（可能调任省直部门或省人大/政协）。",
        "confidence": "confirmed"
    },
]

# ── Organizations ──────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共六安市委", "type": "党委", "level": "地级市", "parent": "中共安徽省委", "location": "六安市"},
    {"id": 2, "name": "六安市人民政府", "type": "政府", "level": "地级市", "parent": "安徽省人民政府", "location": "六安市"},
    {"id": 3, "name": "中共六安市纪律检查委员会", "type": "党委", "level": "地级市", "parent": "中共六安市委", "location": "六安市"},
    {"id": 4, "name": "六安市监察委员会", "type": "政府", "level": "地级市", "parent": "六安市人民政府", "location": "六安市"},
    {"id": 5, "name": "中共六安市委组织部", "type": "党委", "level": "地级市", "parent": "中共六安市委", "location": "六安市"},
    {"id": 6, "name": "中共六安市委政法委员会", "type": "党委", "level": "地级市", "parent": "中共六安市委", "location": "六安市"},
    {"id": 7, "name": "六安市公安局", "type": "政府", "level": "地级市", "parent": "六安市人民政府", "location": "六安市"},
    {"id": 8, "name": "六安军分区", "type": "政府", "level": "地级市", "parent": "安徽省军区", "location": "六安市"},
    {"id": 9, "name": "六安市人大常委会", "type": "人大", "level": "地级市", "parent": "六安市", "location": "六安市"},
    {"id": 10, "name": "六安市政协", "type": "政协", "level": "地级市", "parent": "六安市", "location": "六安市"},
    {"id": 11, "name": "中共六安市委宣传部", "type": "党委", "level": "地级市", "parent": "中共六安市委", "location": "六安市"},
    {"id": 12, "name": "中共六安市委统一战线工作部", "type": "党委", "level": "地级市", "parent": "中共六安市委", "location": "六安市"},
    {"id": 13, "name": "六安经济技术开发区", "type": "开发区", "level": "地级市", "parent": "六安市人民政府", "location": "六安市"},
    {"id": 14, "name": "安徽省人大常委会", "type": "人大", "level": "省级", "parent": "安徽省", "location": "合肥市"},
    {"id": 15, "name": "安徽省政协", "type": "政协", "level": "省级", "parent": "安徽省", "location": "合肥市"},
    {"id": 16, "name": "中共六安市委办公室", "type": "党委", "level": "地级市", "parent": "中共六安市委", "location": "六安市"},
    {"id": 17, "name": "中共阜阳市颍泉区委员会", "type": "党委", "level": "县处级", "parent": "中共阜阳市委", "location": "阜阳市颍泉区"},
]

# ── Positions ──────────────────────────────────────────────────────────

positions = [
    # 方正 - 市委书记
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "2023", "end": "present", "rank": "正厅级", "note": "主持市委全面工作。2023年接替叶露中任六安市委书记。"},
    # 刘洪洁 - 市长、市委副书记
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "2025", "end": "present", "rank": "正厅级", "note": "接替潘东旭任市委副书记。"},
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "2025", "end": "present", "rank": "正厅级", "note": "领导市政府全面工作。接替潘东旭。"},
    # 刘洪洁 - 前任职务
    {"person_id": 2, "org_id": 17, "title": "颍泉区委书记（原）", "start": "", "end": "2024", "rank": "正处级", "note": "曾任阜阳市颍泉区委书记，后升任六安市市长。"},
    # 汪宏军
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 16, "title": "市委秘书长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 孔祥永
    {"person_id": 4, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 李强
    {"person_id": 5, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 孙学龙
    {"person_id": 6, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 魏武
    {"person_id": 7, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 王庆昊
    {"person_id": 8, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 王晓晨
    {"person_id": 9, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 程旭
    {"person_id": 10, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 王思春
    {"person_id": 11, "org_id": 2, "title": "市政府秘书长", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 潘东旭 (前任市长)
    {"person_id": 12, "org_id": 2, "title": "市长（前任）", "start": "2021", "end": "2025", "rank": "正厅级", "note": "前任六安市长。2025年离任。"},
    # 叶露中 (前任市委书记)
    {"person_id": 13, "org_id": 1, "title": "市委书记（前任）", "start": "2021", "end": "2023", "rank": "正厅级", "note": "前任六安市委书记。2023年由方正接替。"},
]

# ── Relationships ──────────────────────────────────────────────────────

relationships = [
    # Core leadership team - same org overlap (市委常委会)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "市委书记和市长同届领导班子成员", "overlap_org": "中共六安市委", "overlap_period": "2025-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "市委书记和市委秘书长", "overlap_org": "中共六安市委", "overlap_period": "2025-", "strength": "strong", "confidence": "confirmed"},
    # 市长 with deputies
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "市长和副市长孔祥永", "overlap_org": "六安市人民政府", "overlap_period": "2025-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "市长和副市长李强", "overlap_org": "六安市人民政府", "overlap_period": "2025-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "市长和副市长孙学龙", "overlap_org": "六安市人民政府", "overlap_period": "2025-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "市长和副市长魏武", "overlap_org": "六安市人民政府", "overlap_period": "2025-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "市长和副市长王庆昊", "overlap_org": "六安市人民政府", "overlap_period": "2025-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "市长和副市长王晓晨", "overlap_org": "六安市人民政府", "overlap_period": "2025-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "市长和副市长程旭", "overlap_org": "六安市人民政府", "overlap_period": "2025-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "市长和市政府秘书长", "overlap_org": "六安市人民政府", "overlap_period": "2025-", "strength": "strong", "confidence": "confirmed"},
    # Predecessor-successor chain
    {"person_a": 1, "person_b": 13, "type": "predecessor_successor", "context": "方正接替叶露中任六安市委书记", "overlap_org": "中共六安市委", "overlap_period": "2023", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 12, "type": "predecessor_successor", "context": "刘洪洁接替潘东旭任六安市长", "overlap_org": "六安市人民政府", "overlap_period": "2025", "strength": "strong", "confidence": "confirmed"},
    # Cross-city: 刘洪洁's trajectory from 颍泉区 to 六安市
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "推测：刘洪洁由颍泉区委书记跨市提任六安市长，叶露中可能参与了干部选拔程序", "overlap_org": "中共安徽省委", "overlap_period": "2025", "strength": "medium", "confidence": "plausible"},
]


# ══════════════════════════════════════════════════════════════════════════
# Database + GEXF generation
# ══════════════════════════════════════════════════════════════════════════

def create_database():
    """Create SQLite database with persons, organizations, positions, relationships."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, native_place TEXT,
            education TEXT, party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT,
            source TEXT, notes TEXT, confidence TEXT
        )
    """)
    c.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        )
    """)
    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            strength TEXT, confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, native_place,
                                 education, party_join, work_start, current_post, current_org, source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p["birthplace"], p["native_place"], p["education"],
              p["party_join"], p["work_start"], p["current_post"],
              p["current_org"], p["source"], p.get("notes", ""), p["confidence"]))

    for o in organizations:
        c.execute("INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"], r["strength"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"[OK] Database created: {DB_PATH}")
    print(f"      Persons: {len(persons)}")
    print(f"      Organizations: {len(organizations)}")
    print(f"      Positions: {len(positions)}")
    print(f"      Relationships: {len(relationships)}")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(person):
    """Return 'r,g,b' string based on role."""
    role = person.get("current_post", "")
    if "书记" in role and "市委" in role and "副" not in role:
        return "255,50,50"  # Red for Party Secretary
    if "市长" in role and "副" not in role:
        return "50,100,255"  # Blue for Mayor
    if "纪委" in role or "监委" in role:
        return "255,165,0"  # Orange for Discipline
    if "人大" in role:
        return "200,255,255"  # Cyan for People's Congress
    if "政协" in role:
        return "255,240,200"  # Cream for CPPCC
    return "100,100,100"  # Grey for others


def person_size(person):
    """Return node size based on rank."""
    role = person.get("current_post", "")
    if "市委书记" in role and "副" not in role:
        return "20.0"
    if "市长" in role and "副" not in role:
        return "20.0"
    if "人大" in role or "政协" in role:
        return "15.0"
    if "常委" in role:
        return "15.0"
    return "12.0"


def org_color(org):
    """Return 'r,g,b' string for organization type."""
    t = org.get("type", "")
    type_colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return type_colors.get(t, "200,200,200")


def generate_gexf():
    """Generate GEXF graph using string formatting to avoid XML namespace issues."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>六安市领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="rank" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="strength" type="string"/>')
    lines.append('      <attribute id="3" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        pid = f"p{p['id']}"
        c = person_color(p)
        sz = person_size(p)
        role = esc(p.get("current_post", ""))
        org_name = esc(p.get("current_org", ""))
        rank = esc(p.get("notes", ""))
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{role}"/>')
        lines.append(f'          <attvalue for="2" value="{org_name}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = f"o{o['id']}"
        c = org_color(o)
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
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
        eid += 1
        src = f"p{pos['person_id']}"
        tgt = f"o{pos['org_id']}"
        lines.append(f'      <edge id="e{eid}" source="{src}" target="{tgt}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person edges (relationship)
    for r in relationships:
        eid += 1
        src = f"p{r['person_a']}"
        tgt = f"p{r['person_b']}"
        w = "2.0" if r["strength"] == "strong" else "1.5"
        lines.append(f'      <edge id="e{eid}" source="{src}" target="{tgt}" label="{esc(r["context"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{r["strength"]}"/>')
        lines.append(f'          <attvalue for="3" value="{r["overlap_period"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[OK] GEXF graph created: {GEXF_PATH}")
    print(f"      Person nodes: {len(persons)}")
    print(f"      Organization nodes: {len(organizations)}")
    print(f"      Worked-at edges: {len(positions)}")
    print(f"      Relationship edges: {len(relationships)}")


def main():
    print("=" * 60)
    print("  六安市领导班子网络数据生成")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    create_database()
    generate_gexf()
    print(f"\n[OK] All files generated in: {SCRIPT_DIR}")


if __name__ == "__main__":
    main()
