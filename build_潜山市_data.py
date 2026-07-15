#!/usr/bin/env python3
"""Build Qianshan City (潜山市) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Sources:
  - www.qss.gov.cn (official Qianshan city government website, news articles accessed 2026-07-15)
  - qss.gov.cn news: 王国林会见"全国先进基层党组织"代表朱太平 (2026-07-06)
  - qss.gov.cn news: 王国林到源潭镇、梅城镇调研 (2026-07-03)
  - qss.gov.cn news: 王国林在黄柏镇、槎水镇调研 (2026-07-02)
  - qss.gov.cn news: 张健深入各乡镇开展综合调研 (2026-07-06) - identifies 张健 as 市委副书记、代市长
  - qss.gov.cn news: 市委常委会召开会议 (2026-07-08) - identifies 张健、张吉全、涂高生、汪沛 as 市委常委会会议组成人员
  - qss.gov.cn news: 潘良能开展"双招双引"活动 (2025-12-14) - identifies 潘良能 as 市委副书记、市长
  - qss.gov.cn news: 简讯：潘良能赴北京开展"双招双引"活动 (2025-07-31)
  - qss.gov.cn news: 简讯：潘良能赴浙江开展"双招双引"活动 (2025-06-27)
  - qss.gov.cn news: 简讯：王国林赴上海、南京开展"双招双引"活动 (2025-10-31)
  - www.anqing.gov.cn (Anqing city government website)

Confidence: Current top leaders (王国林 as 市委书记, 张健 as 市委副书记/代市长) confirmed
  from official Qianshan government news articles dated July 2026.
  Biographical details for most figures are partial; career timelines mostly unknown.
"""

import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "潜山市_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "潜山市_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ── Top Leaders ──────────────────────────────────────────────────
    {
        "id": 1,
        "name": "王国林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共潜山市委",
        "source": "https://www.qss.gov.cn/zwzx/jrqs/2024673907.html (王国林会见代表, 2026-07-06); https://www.qss.gov.cn/zwzx/jrqs/2024673075.html (王国林调研, 2026-07-03)",
        "notes": "潜山市委书记。主持市委全面工作。2026年7月频繁出现在公开报道中。此前曾任潜山市长（约2021-2025/2026年担任市长），后升任市委书记。具体接任时间待查。",
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "张健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记、代市长",
        "current_org": "潜山市人民政府",
        "source": "https://www.qss.gov.cn/zwzx/jrqs/2024674336.html (张健深入各乡镇开展综合调研, 2026-07-06); https://www.qss.gov.cn/zwzx/jrqs/2024677466.html (市委常委会会议, 2026-07-08)",
        "notes": "潜山市委副书记、代市长。2026年7月以代市长身份深入16个乡镇开展综合调研。此前职务待查。接替潘良能任市长。参加市委常委会会议（市委常委会会议组成人员）。",
        "confidence": "confirmed"
    },
    # ── Standing Committee (市委常委) ─────────────────────────────────
    {
        "id": 3,
        "name": "潘良能",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原市委副书记、市长（前任）",
        "current_org": "潜山市人民政府（原）",
        "source": "https://www.qss.gov.cn/tzqs/zsdt/2024474390.html (潘良能开展双招双引, 2025-12-14); https://www.qss.gov.cn/tzqs/zsdt/2024447243.html (潘良能双招双引, 2025-12)",
        "notes": "前任潜山市市长。2025年12月仍以市委副书记、市长身份带队赴苏州、西安开展双招双引活动。2025年7月以市长身份赴北京。2026年7月已由张健接替任代市长，潘良能去向待查。",
        "confidence": "confirmed"
    },
    {
        "id": 4,
        "name": "张吉全",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委（市委常委会会议组成人员）",
        "current_org": "中共潜山市委",
        "source": "https://www.qss.gov.cn/zwzx/jrqs/2024677466.html (市委常委会会议, 2026-07-08)",
        "notes": "潜山市委常委。参加2026年7月8日市委常委会会议。会议报道排序在张健之后。具体职务待查。",
        "confidence": "confirmed"
    },
    {
        "id": 5,
        "name": "涂高生",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委（市委常委会会议组成人员）",
        "current_org": "中共潜山市委",
        "source": "https://www.qss.gov.cn/zwzx/jrqs/2024677466.html (市委常委会会议, 2026-07-08)",
        "notes": "潜山市委常委。参加2026年7月8日市委常委会会议。会议报道排序在张吉全之后。具体职务待查。",
        "confidence": "confirmed"
    },
    {
        "id": 6,
        "name": "汪沛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共潜山市委",
        "source": "https://www.qss.gov.cn/zwzx/jrqs/2024673907.html (王国林会见代表, 2026-07-06); https://www.qss.gov.cn/zwzx/jrqs/2024673075.html (王国林调研, 2026-07-03)",
        "notes": "潜山市委常委。陪同王国林参加会见活动和调研。2026年7月3日陪同王国林赴源潭镇、梅城镇调研。",
        "confidence": "confirmed"
    },
    {
        "id": 7,
        "name": "韩亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委（市领导）",
        "current_org": "中共潜山市委",
        "source": "https://www.qss.gov.cn/zwzx/jrqs/2024671782.html (王国林在黄柏镇、槎水镇调研, 2026-07-02); https://www.qss.gov.cn/zwzx/jrqs/2024673075.html (王国林到源潭镇、梅城镇调研, 2026-07-03)",
        "notes": "潜山市领导（市委常委或副市长）。陪同王国林调研黄柏镇、槎水镇和源潭镇、梅城镇。具体职务待查。",
        "confidence": "plausible"
    },
    {
        "id": 8,
        "name": "鲍瑜斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "潜山市",
        "source": "https://www.qss.gov.cn/zwzx/jrqs/2024673907.html (王国林会见代表, 2026-07-06); https://www.qss.gov.cn/zwzx/jrqs/2024671782.html (王国林在黄柏镇、槎水镇调研, 2026-07-02)",
        "notes": "潜山市领导。陪同王国林参加会见和调研活动。具体职务待查。",
        "confidence": "plausible"
    },
    {
        "id": 9,
        "name": "陈玮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "潜山市",
        "source": "https://www.qss.gov.cn/tzqs/zsdt/2024474390.html (潘良能开展双招双引, 2025-12-14)",
        "notes": "潜山市领导。2025年12月陪同原市长潘良能赴苏州、西安开展双招双引活动。具体职务待查。",
        "confidence": "plausible"
    },
]

# ── Organizations ───────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共潜山市委", "type": "党委", "level": "县级市", "parent": "中共安庆市委", "location": "安徽省安庆市潜山市"},
    {"id": 2, "name": "潜山市人民政府", "type": "政府", "level": "县级市", "parent": "安庆市人民政府", "location": "安徽省安庆市潜山市"},
    {"id": 3, "name": "中共潜山市纪律检查委员会", "type": "党委", "level": "县级市", "parent": "中共潜山市委", "location": "安徽省安庆市潜山市"},
    {"id": 4, "name": "潜山市监察委员会", "type": "政府", "level": "县级市", "parent": "潜山市人民政府", "location": "安徽省安庆市潜山市"},
    {"id": 5, "name": "潜山市委组织部", "type": "党委", "level": "县级市", "parent": "中共潜山市委", "location": "安徽省安庆市潜山市"},
    {"id": 6, "name": "潜山市委宣传部", "type": "党委", "level": "县级市", "parent": "中共潜山市委", "location": "安徽省安庆市潜山市"},
    {"id": 7, "name": "潜山市委统战部", "type": "党委", "level": "县级市", "parent": "中共潜山市委", "location": "安徽省安庆市潜山市"},
    {"id": 8, "name": "潜山市委政法委", "type": "党委", "level": "县级市", "parent": "中共潜山市委", "location": "安徽省安庆市潜山市"},
    {"id": 9, "name": "潜山市人民代表大会常务委员会", "type": "人大", "level": "县级市", "parent": "潜山市", "location": "安徽省安庆市潜山市"},
    {"id": 10, "name": "中国人民政治协商会议潜山市委员会", "type": "政协", "level": "县级市", "parent": "潜山市", "location": "安徽省安庆市潜山市"},
]

# ── Positions ──────────────────────────────────────────────────────────

positions = [
    # 王国林 - 市委书记
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "", "end": "present", "rank": "正处级", "note": "主持市委全面工作。此前曾任潜山市市长，后升任市委书记。"},
    # 张健 - 代市长
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "正处级", "note": "市政府党组书记"},
    {"person_id": 2, "org_id": 2, "title": "代市长", "start": "", "end": "present", "rank": "正处级", "note": "2026年7月任代市长，主持市政府全面工作"},
    # 潘良能 - 前任市长
    {"person_id": 3, "org_id": 1, "title": "市委副书记（原）", "start": "", "end": "", "rank": "正处级", "note": "原潜山市长，2025年12月仍在任，2026年7月已由张健接替"},
    {"person_id": 3, "org_id": 2, "title": "市长（原）", "start": "", "end": "", "rank": "正处级", "note": "原潜山市市长，多次带队外出招商"},
    # 张吉全
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": "市委常委会会议组成人员"},
    # 涂高生
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": "市委常委会会议组成人员"},
    # 汪沛
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": "陪同市委书记调研"},
    # 韩亮
    {"person_id": 7, "org_id": 1, "title": "市委常委/市领导", "start": "", "end": "present", "rank": "副处级", "note": "陪同调研，具体职务不详"},
    # 鲍瑜斌
    {"person_id": 8, "org_id": 1, "title": "市领导", "start": "", "end": "present", "rank": "副处级", "note": "陪同调研会见，具体职务不详"},
    # 陈玮
    {"person_id": 9, "org_id": 2, "title": "市领导", "start": "", "end": "", "rank": "副处级", "note": "陪同原市长外出招商，具体职务不详"},
]

# ── Relationships ──────────────────────────────────────────────────────

relationships = [
    # Core leadership team - same org overlap (市委常委会)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "市委书记和代市长，市委市政府双核心搭档", "overlap_org": "中共潜山市委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "王国林接替前任或与潘良能先后任市长；王国林升任书记后潘良能接任市长，后张健接替潘良能", "overlap_org": "潜山市人民政府", "overlap_period": "2021-2026", "strength": "strong", "confidence": "plausible"},
    {"person_a": 2, "person_b": 3, "type": "predecessor_successor", "context": "张健接替潘良能任潜山市代市长", "overlap_org": "潜山市人民政府", "overlap_period": "2026", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "市委书记和市委常委张吉全，市委常委会共事", "overlap_org": "中共潜山市委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "市委书记和市委常委涂高生，市委常委会共事", "overlap_org": "中共潜山市委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "市委书记和市委常委汪沛，汪沛多次陪同调研", "overlap_org": "中共潜山市委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "市委书记和市领导韩亮，韩亮多次陪同调研", "overlap_org": "中共潜山市委", "overlap_period": "2026-", "strength": "medium", "confidence": "plausible"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "市委书记和市领导鲍瑜斌，鲍瑜斌多次陪同调研会见", "overlap_org": "中共潜山市委", "overlap_period": "2026-", "strength": "medium", "confidence": "plausible"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "代市长和市委常委张吉全，市委常委会共事", "overlap_org": "中共潜山市委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "代市长和市委常委涂高生，市委常委会共事", "overlap_org": "中共潜山市委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "代市长和市委常委汪沛，市委常委会共事", "overlap_org": "中共潜山市委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 6, "type": "overlap", "context": "原市长潘良能和市委常委汪沛，曾在市委/市政府共事", "overlap_org": "中共潜山市委", "overlap_period": "-2025", "strength": "medium", "confidence": "plausible"},
    {"person_a": 3, "person_b": 9, "type": "overlap", "context": "原市长潘良能和市领导陈玮，陈玮2025年12月陪同潘良能外出招商", "overlap_org": "潜山市人民政府", "overlap_period": "2025", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "市委常委张吉全和涂高生，同为市委常委会会议组成人员", "overlap_org": "中共潜山市委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "市委常委张吉全和汪沛，同为市委常委会会议组成人员", "overlap_org": "中共潜山市委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "市委常委涂高生和汪沛，同为市委常委会会议组成人员", "overlap_org": "中共潜山市委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 7, "person_b": 8, "type": "overlap", "context": "韩亮和鲍瑜斌，多次陪同市委书记调研", "overlap_org": "潜山市", "overlap_period": "2026-", "strength": "medium", "confidence": "plausible"},
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
            source TEXT, confidence TEXT
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
                                 education, party_join, work_start, current_post, current_org, source, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p["birthplace"], p["native_place"], p["education"],
              p["party_join"], p["work_start"], p["current_post"],
              p["current_org"], p["source"], p["confidence"]))

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
    if "书记" in role and "市委" in role and "副" not in role and "原" not in role:
        return "255,50,50"  # Red for Party Secretary
    if "市长" in role and ("代" in role or "副" not in role) and "原" not in role:
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
    if "市委书记" in role and "副" not in role and "原" not in role:
        return "20.0"
    if "市长" in role and ("代" in role or "副" not in role) and "原" not in role:
        return "20.0"
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
    lines.append('    <description>潜山市领导班子工作关系网络</description>')
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
        org = esc(p.get("current_org", ""))
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{role}"/>')
        lines.append(f'          <attvalue for="2" value="{org}"/>')
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
    print("  潜山市领导班子网络数据生成")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    create_database()
    generate_gexf()
    print(f"\n[OK] All files generated in: {SCRIPT_DIR}")


if __name__ == "__main__":
    main()
