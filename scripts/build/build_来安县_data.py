#!/usr/bin/env python3
"""Build 来安县 (Lai'an County, Chuzhou, Anhui) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Task: anhui_来安县 - 县委书记 & 县长
Province: 安徽省
City: 滁州市
Region: 来安县
Level: 县

Data sources:
- laian.gov.cn (official government website, 2026-07-15) — confirmed current leaders
- Pre-training knowledge for biographical details (marked confidence accordingly)

Confirmed from laian.gov.cn as of 2026-07-15:
- 张传宗: 县委书记 (presides over 县委理论学习中心组学习会, 县委常委会, field research)
- 王海峰: 县长 (leads 防汛防台风, rural development research, 信访接访)

NOTE: Web search (Exa), Baidu Baike, and general internet search were unavailable
from this research environment. Biographical details below are from pre-training
knowledge and should be verified against live sources.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ──────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Detect if running from staging
if "data/tmp" in SCRIPT_DIR:
    STAGING = SCRIPT_DIR
else:
    STAGING = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR))),
                           "data/tmp/anhui_来安县")
DB_PATH = os.path.join(STAGING, "来安县_network.db")
GEXF_PATH = os.path.join(STAGING, "来安县_network.gexf")

# ── research data ──────────────────────────────────────────────────────

persons = [
    # ═══ Current Top Leaders ═══

    # 县委书记 — 张传宗 (confirmed from laian.gov.cn news articles, 2026-07-15)
    {
        "id": "laian_zhang_chuanzong",
        "name": "张传宗",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "来安县委书记",
        "current_org": "中共来安县委员会",
        "source": "laian.gov.cn 政务要闻 (2026-07-15 张传宗主持召开县委理论学习中心组学习会)",
        "notes": "confirmed from laian.gov.cn: 主持县委常委会、县委理论学习中心组学习会，深入乡镇调研和美乡村建设和农业产业。",
        "confidence": "confirmed"
    },

    # 县长 — 王海峰 (confirmed from laian.gov.cn news articles, 2026-07-12/07-09)
    {
        "id": "laian_wang_haifeng",
        "name": "王海峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "来安县委副书记、县长",
        "current_org": "来安县人民政府",
        "source": "laian.gov.cn 政务要闻 (2026-07-12 王海峰调研防汛防台风, 2026-07-09 王海峰带队调研和美乡村)",
        "notes": "confirmed from laian.gov.cn: 调研防汛防台风和城市内涝治理，调研和美乡村建设，赴县信访局接访。",
        "confidence": "confirmed"
    },

    # ═══ County Party Committee Standing Members (县委常委会) ═══
    # Names pending verification from official leadership page

    {
        "id": "laian_deputy_secretary_1",
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "来安县委副书记（专职）",
        "current_org": "中共来安县委员会",
        "source": "需从 laian.gov.cn 领导之窗页面确认",
        "notes": "县委专职副书记。具体姓名待从官网确认。",
        "confidence": "unverified"
    },
    {
        "id": "laian_discipline_secretary",
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "来安县委常委、纪委书记",
        "current_org": "中共来安县纪律检查委员会",
        "source": "需从 laian.gov.cn 领导之窗页面确认",
        "notes": "县纪委书记。具体姓名待从官网确认。",
        "confidence": "unverified"
    },
    {
        "id": "laian_organization_minister",
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "来安县委常委、组织部部长",
        "current_org": "中共来安县委组织部",
        "source": "需从 laian.gov.cn 领导之窗页面确认",
        "notes": "县委组织部部长。具体姓名待从官网确认。",
        "confidence": "unverified"
    },
    {
        "id": "laian_propaganda_minister",
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "来安县委常委、宣传部部长",
        "current_org": "中共来安县委宣传部",
        "source": "需从 laian.gov.cn 领导之窗页面确认",
        "notes": "县委宣传部部长。具体姓名待从官网确认。",
        "confidence": "unverified"
    },
    {
        "id": "laian_united_front_minister",
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "来安县委常委、统战部部长",
        "current_org": "中共来安县委统战部",
        "source": "需从 laian.gov.cn 领导之窗页面确认",
        "notes": "县委统战部部长。具体姓名待从官网确认。",
        "confidence": "unverified"
    },
    {
        "id": "laian_political_legal_secretary",
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "来安县委常委、政法委书记",
        "current_org": "中共来安县委政法委员会",
        "source": "需从 laian.gov.cn 领导之窗页面确认",
        "notes": "县委政法委书记。具体姓名待从官网确认。",
        "confidence": "unverified"
    },
    {
        "id": "laian_deputy_mayor_1",
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "来安县委常委、常务副县长",
        "current_org": "来安县人民政府",
        "source": "需从 laian.gov.cn 领导之窗页面确认",
        "notes": "县政府常务副县长。具体姓名待从官网确认。",
        "confidence": "unverified"
    },
    {
        "id": "laian_military_committee",
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "来安县委常委、人武部政委/部长",
        "current_org": "来安县人民武装部",
        "source": "需从 laian.gov.cn 领导之窗页面确认",
        "notes": "县人武部主官。具体姓名待从官网确认。",
        "confidence": "unverified"
    },
]

organizations = [
    # Party and government core
    {
        "id": "org_cpc_laian",
        "name": "中共来安县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共滁州市委员会",
        "location": "安徽省滁州市来安县"
    },
    {
        "id": "org_laian_gov",
        "name": "来安县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "滁州市人民政府",
        "location": "安徽省滁州市来安县"
    },
    {
        "id": "org_discipline",
        "name": "中共来安县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共来安县委员会/中共滁州市纪律检查委员会",
        "location": "安徽省滁州市来安县"
    },
    {
        "id": "org_organization",
        "name": "中共来安县委组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共来安县委员会",
        "location": "安徽省滁州市来安县"
    },
    {
        "id": "org_propaganda",
        "name": "中共来安县委宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共来安县委员会",
        "location": "安徽省滁州市来安县"
    },
    {
        "id": "org_united_front",
        "name": "中共来安县委统战部",
        "type": "党委",
        "level": "县级",
        "parent": "中共来安县委员会",
        "location": "安徽省滁州市来安县"
    },
    {
        "id": "org_political_legal",
        "name": "中共来安县委政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共来安县委员会",
        "location": "安徽省滁州市来安县"
    },
    {
        "id": "org_military",
        "name": "来安县人民武装部",
        "type": "政府",
        "level": "县级",
        "parent": "滁州军分区",
        "location": "安徽省滁州市来安县"
    },
    {
        "id": "org_npc",
        "name": "来安县人大常委会",
        "type": "人大",
        "level": "县级",
        "parent": "滁州市人大常委会",
        "location": "安徽省滁州市来安县"
    },
    {
        "id": "org_cppcc",
        "name": "中国人民政治协商会议来安县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "政协滁州市委员会",
        "location": "安徽省滁州市来安县"
    },
]

positions = [
    # 县委书记 张传宗
    {"person_id": "laian_zhang_chuanzong", "org_id": "org_cpc_laian", "title": "来安县委书记",
     "start": "", "end": "present", "rank": "正县级", "note": "confirmed from laian.gov.cn"},

    # 县长 王海峰
    {"person_id": "laian_wang_haifeng", "org_id": "org_laian_gov", "title": "来安县委副书记、县长",
     "start": "", "end": "present", "rank": "正县级", "note": "confirmed from laian.gov.cn"},
    {"person_id": "laian_wang_haifeng", "org_id": "org_cpc_laian", "title": "来安县委副书记",
     "start": "", "end": "present", "rank": "正县级", "note": "confirmed from laian.gov.cn"},

    # 县委专职副书记
    {"person_id": "laian_deputy_secretary_1", "org_id": "org_cpc_laian", "title": "来安县委副书记（专职）",
     "start": "", "end": "present", "rank": "副县级", "note": "待确认姓名"},

    # 纪委书记
    {"person_id": "laian_discipline_secretary", "org_id": "org_discipline", "title": "来安县委常委、纪委书记",
     "start": "", "end": "present", "rank": "副县级", "note": "待确认姓名"},

    # 组织部部长
    {"person_id": "laian_organization_minister", "org_id": "org_organization", "title": "来安县委常委、组织部部长",
     "start": "", "end": "present", "rank": "副县级", "note": "待确认姓名"},

    # 宣传部部长
    {"person_id": "laian_propaganda_minister", "org_id": "org_propaganda", "title": "来安县委常委、宣传部部长",
     "start": "", "end": "present", "rank": "副县级", "note": "待确认姓名"},

    # 统战部部长
    {"person_id": "laian_united_front_minister", "org_id": "org_united_front", "title": "来安县委常委、统战部部长",
     "start": "", "end": "present", "rank": "副县级", "note": "待确认姓名"},

    # 政法委书记
    {"person_id": "laian_political_legal_secretary", "org_id": "org_political_legal", "title": "来安县委常委、政法委书记",
     "start": "", "end": "present", "rank": "副县级", "note": "待确认姓名"},

    # 常务副县长
    {"person_id": "laian_deputy_mayor_1", "org_id": "org_laian_gov", "title": "来安县委常委、常务副县长",
     "start": "", "end": "present", "rank": "副县级", "note": "待确认姓名"},

    # 人武部
    {"person_id": "laian_military_committee", "org_id": "org_military", "title": "来安县委常委、人武部主官",
     "start": "", "end": "present", "rank": "副县级", "note": "待确认姓名"},
]

relationships = [
    # 党政主官
    {"person_a": "laian_zhang_chuanzong", "person_b": "laian_wang_haifeng", "type": "superior_subordinate",
     "strength": "strong", "context": "县委书记与县长党政主官关系",
     "overlap_org": "中共来安县委员会/来安县人民政府",
     "overlap_period": "至今", "note": "confirmed"},

    # 县委书记与专职副书记
    {"person_a": "laian_zhang_chuanzong", "person_b": "laian_deputy_secretary_1", "type": "superior_subordinate",
     "strength": "strong", "context": "县委书记与县委副书记",
     "overlap_org": "中共来安县委员会",
     "overlap_period": "至今", "note": "plausible"},

    # 县委书记与纪委书记
    {"person_a": "laian_zhang_chuanzong", "person_b": "laian_discipline_secretary", "type": "superior_subordinate",
     "strength": "medium", "context": "县委书记与纪委书记",
     "overlap_org": "中共来安县委员会",
     "overlap_period": "至今", "note": "plausible"},

    # 县委书记与组织部部长
    {"person_a": "laian_zhang_chuanzong", "person_b": "laian_organization_minister", "type": "superior_subordinate",
     "strength": "medium", "context": "县委书记与组织部部长",
     "overlap_org": "中共来安县委员会",
     "overlap_period": "至今", "note": "plausible"},

    # 县委书记与宣传部部长
    {"person_a": "laian_zhang_chuanzong", "person_b": "laian_propaganda_minister", "type": "superior_subordinate",
     "strength": "medium", "context": "县委书记与宣传部部长",
     "overlap_org": "中共来安县委员会",
     "overlap_period": "至今", "note": "plausible"},

    # 县委书记与政法委书记
    {"person_a": "laian_zhang_chuanzong", "person_b": "laian_political_legal_secretary", "type": "superior_subordinate",
     "strength": "medium", "context": "县委书记与政法委书记",
     "overlap_org": "中共来安县委员会",
     "overlap_period": "至今", "note": "plausible"},

    # 县委书记与统战部部长
    {"person_a": "laian_zhang_chuanzong", "person_b": "laian_united_front_minister", "type": "superior_subordinate",
     "strength": "medium", "context": "县委书记与统战部部长",
     "overlap_org": "中共来安县委员会",
     "overlap_period": "至今", "note": "plausible"},

    # 县长与常务副县长
    {"person_a": "laian_wang_haifeng", "person_b": "laian_deputy_mayor_1", "type": "superior_subordinate",
     "strength": "strong", "context": "县长与常务副县长",
     "overlap_org": "来安县人民政府",
     "overlap_period": "至今", "note": "plausible"},

    # 县委书记与人武部主官
    {"person_a": "laian_zhang_chuanzong", "person_b": "laian_military_committee", "type": "superior_subordinate",
     "strength": "medium", "context": "县委书记与人武部主官",
     "overlap_org": "中共来安县委员会",
     "overlap_period": "至今", "note": "plausible"},
]


# ── HELPERS ────────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    post = p["current_post"]
    if "书记" in post and "县委书记" in post:
        return "255,50,50"
    if "县长" in post:
        return "50,100,255"
    if "纪委书记" in post:
        return "255,165,0"
    if "人大" in post:
        return "200,100,100"
    if "政协" in post:
        return "100,100,200"
    return "100,100,100"


def org_color(o):
    t = o["type"]
    if t == "党委":
        return "255,200,200"
    if t == "政府":
        return "200,200,255"
    if t == "人大":
        return "200,255,255"
    if t == "政协":
        return "255,240,200"
    return "200,200,200"


def is_top_leader(p):
    return p["id"] in ("laian_zhang_chuanzong", "laian_wang_haifeng")


# ── BUILD DB ───────────────────────────────────────────────────────────

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
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"],
              pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, strength, context, overlap_org, overlap_period, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["strength"],
              r["context"], r["overlap_org"], r["overlap_period"], r["note"]))

    conn.commit()
    print(f"  Persons: {c.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}")
    print(f"  Orgs: {c.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}")
    print(f"  Positions: {c.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}")
    print(f"  Relationships: {c.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")
    conn.close()


# ── BUILD GEXF ─────────────────────────────────────────────────────────

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>来安县（安徽省滁州市）领导关系网络 - 2026年7月</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="gender" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="strength" type="string"/>')
    lines.append('    </attributes>')

    # Nodes - Persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="{esc(p["id"])}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["gender"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["confidence"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes - Organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="{esc(o["id"])}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="{esc(pos["person_id"])}" target="{esc(pos["org_id"])}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person relationships
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.5"
        lines.append(f'      <edge id="e{eid}" source="{esc(r["person_a"])}" target="{esc(r["person_b"])}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["strength"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {len(persons)} persons, {len(organizations)} orgs, {eid} edges")


# ── MAIN ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    print("Building 来安县 (Lai'an County, Chuzhou, Anhui) network...")
    print(f"  DB path: {DB_PATH}")
    print(f"  GEXF path: {GEXF_PATH}")
    print("  NOTE: Core leaders confirmed from laian.gov.cn. Roster members need live verification.")
    build_db()
    build_gexf()
    print("Done.")
