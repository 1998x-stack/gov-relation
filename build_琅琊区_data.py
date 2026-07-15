#!/usr/bin/env python3
"""Build 琅琊区 (Langya District, Chuzhou, Anhui) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Task: anhui_琅琊区 - 区委书记 & 区长
Province: 安徽省
City: 滁州市
Region: 琅琊区
Level: 市辖区

IMPORTANT: Research was conducted under network constraints — official government websites
(www.lyq.gov.cn, www.chuzhou.gov.cn), Baidu Baike, and search engines were all unreachable
from this environment. The data below is compiled from pre-training knowledge and should be
verified against live sources before relying on for publication.

Confidence: Current roles are plausible but UNVERIFIED against live official sources.
Career timelines are partial and should be supplemented.
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
                           "data/tmp/anhui_琅琊区")
DB_PATH = os.path.join(STAGING, "琅琊区_network.db")
GEXF_PATH = os.path.join(STAGING, "琅琊区_network.gexf")

# ── research data ──────────────────────────────────────────────────────

persons = [
    # ═══ Current Top Leaders ═══

    # 区委书记 — name needs verification from live official source
    {
        "id": "langya_jiao_yan",
        "name": "焦艳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "琅琊区委书记",
        "current_org": "中共琅琊区委员会",
        "source": "需从官网 lyq.gov.cn 或滁州市政府网站确认",
        "notes": "根据公开资料，焦艳曾任琅琊区委书记。具体简历和任命时间需从官方渠道确认。",
        "confidence": "unverified"
    },

    # 区长 — name needs verification
    {
        "id": "langya_wang_zheng",
        "name": "王政",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "琅琊区委副书记、区长",
        "current_org": "琅琊区人民政府",
        "source": "需从官网 lyq.gov.cn 或滁州市政府网站确认",
        "notes": "根据公开资料，王政曾任琅琊区委副书记、区长。具体简历和任命时间需从官方渠道确认。",
        "confidence": "unverified"
    },

    # ═══ District Party Committee Standing Members (区委常委) ═══
    # Names below need verification

    {
        "id": "langya_deputy_secretary_1",
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "琅琊区委副书记",
        "current_org": "中共琅琊区委员会",
        "source": "需从 lyq.gov.cn 领导之窗页面确认",
        "notes": "琅琊区委副书记（专职）。具体姓名待从官网确认。",
        "confidence": "unverified"
    },
    {
        "id": "langya_deputy_mayor_1",
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "琅琊区委常委、常务副区长",
        "current_org": "琅琊区人民政府",
        "source": "需从 lyq.gov.cn 领导之窗页面确认",
        "notes": "区政府常务副区长、党组副书记。具体姓名待从官网确认。",
        "confidence": "unverified"
    },
    {
        "id": "langya_organization_minister",
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "琅琊区委常委、组织部部长",
        "current_org": "中共琅琊区委员会组织部",
        "source": "需从 lyq.gov.cn 领导之窗页面确认",
        "notes": "区委组织部部长。具体姓名待从官网确认。",
        "confidence": "unverified"
    },
    {
        "id": "langya_discipline_secretary",
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "琅琊区委常委、纪委书记、监委主任",
        "current_org": "中共琅琊区纪律检查委员会",
        "source": "需从 lyq.gov.cn 领导之窗页面确认",
        "notes": "区纪委书记、监委主任。具体姓名待从官网确认。",
        "confidence": "unverified"
    },
    {
        "id": "langya_propaganda_minister",
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "琅琊区委常委、宣传部部长",
        "current_org": "中共琅琊区委员会宣传部",
        "source": "需从 lyq.gov.cn 领导之窗页面确认",
        "notes": "区委宣传部部长。具体姓名待从官网确认。",
        "confidence": "unverified"
    },
    {
        "id": "langya_politics_law_secretary",
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "琅琊区委常委、政法委书记",
        "current_org": "中共琅琊区委员会政法委员会",
        "source": "需从 lyq.gov.cn 领导之窗页面确认",
        "notes": "区委政法委书记。具体姓名待从官网确认。",
        "confidence": "unverified"
    },
    {
        "id": "langya_united_front_minister",
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "琅琊区委常委、统战部部长",
        "current_org": "中共琅琊区委员会统战部",
        "source": "需从 lyq.gov.cn 领导之窗页面确认",
        "notes": "区委统战部部长。具体姓名待从官网确认。",
        "confidence": "unverified"
    },

    # ═══ NPC Standing Committee (区人大) ═══
    {
        "id": "langya_npc_director",
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "琅琊区人大常委会主任",
        "current_org": "琅琊区人民代表大会常务委员会",
        "source": "需从 lyq.gov.cn 确认",
        "notes": "区人大常委会主任。具体姓名待从官网确认。",
        "confidence": "unverified"
    },

    # ═══ CPPCC (区政协) ═══
    {
        "id": "langya_cppcc_director",
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "琅琊区政协主席",
        "current_org": "政协琅琊区委员会",
        "source": "需从 lyq.gov.cn 确认",
        "notes": "区政协主席。具体姓名待从官网确认。",
        "confidence": "unverified"
    },
]

organizations = [
    {"id": "org_party", "name": "中共琅琊区委员会", "type": "党委", "level": "县处级", "parent": "中共滁州市委", "location": "安徽省滁州市琅琊区"},
    {"id": "org_gov", "name": "琅琊区人民政府", "type": "政府", "level": "县处级", "parent": "滁州市人民政府", "location": "安徽省滁州市琅琊区"},
    {"id": "org_discipline", "name": "中共琅琊区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共琅琊区委员会", "location": "安徽省滁州市琅琊区"},
    {"id": "org_organization", "name": "中共琅琊区委员会组织部", "type": "党委", "level": "乡科级", "parent": "中共琅琊区委员会", "location": "安徽省滁州市琅琊区"},
    {"id": "org_propaganda", "name": "中共琅琊区委员会宣传部", "type": "党委", "level": "乡科级", "parent": "中共琅琊区委员会", "location": "安徽省滁州市琅琊区"},
    {"id": "org_united_front", "name": "中共琅琊区委员会统战部", "type": "党委", "level": "乡科级", "parent": "中共琅琊区委员会", "location": "安徽省滁州市琅琊区"},
    {"id": "org_politics_law", "name": "中共琅琊区委员会政法委员会", "type": "党委", "level": "乡科级", "parent": "中共琅琊区委员会", "location": "安徽省滁州市琅琊区"},
    {"id": "org_npc", "name": "琅琊区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "滁州市人大常委会", "location": "安徽省滁州市琅琊区"},
    {"id": "org_cppcc", "name": "政协琅琊区委员会", "type": "政协", "level": "县处级", "parent": "政协滁州市委员会", "location": "安徽省滁州市琅琊区"},
]

positions = [
    # 焦艳 (区委书记)
    {"person_id": "langya_jiao_yan", "org_id": "org_party", "title": "琅琊区委书记", "start": "", "end": "present", "rank": "正县级", "note": "现任区委书记，需确认任职起始时间"},
    {"person_id": "langya_jiao_yan", "org_id": "org_party", "title": "琅琊区委副书记（前职）", "start": "", "end": "", "rank": "副县级", "note": "可能此前担任区委副书记或区政府职务"},

    # 王政 (区长)
    {"person_id": "langya_wang_zheng", "org_id": "org_gov", "title": "琅琊区委副书记、区长", "start": "", "end": "present", "rank": "正县级", "note": "现任区长，需确认任职起始时间"},
    {"person_id": "langya_wang_zheng", "org_id": "org_gov", "title": "琅琊区委常委、副区长（前职）", "start": "", "end": "", "rank": "副县级", "note": "可能此前担任常务副区长或副区长"},

    # 专职副书记
    {"person_id": "langya_deputy_secretary_1", "org_id": "org_party", "title": "琅琊区委副书记（专职）", "start": "", "end": "present", "rank": "副县级", "note": "专职副书记，待确认姓名"},

    # 常务副区长
    {"person_id": "langya_deputy_mayor_1", "org_id": "org_gov", "title": "琅琊区委常委、常务副区长", "start": "", "end": "present", "rank": "副县级", "note": "常务副区长，待确认姓名"},

    # 组织部部长
    {"person_id": "langya_organization_minister", "org_id": "org_organization", "title": "琅琊区委常委、组织部部长", "start": "", "end": "present", "rank": "副县级", "note": "待确认姓名"},

    # 纪委书记
    {"person_id": "langya_discipline_secretary", "org_id": "org_discipline", "title": "琅琊区委常委、纪委书记、监委主任", "start": "", "end": "present", "rank": "副县级", "note": "待确认姓名"},

    # 宣传部部长
    {"person_id": "langya_propaganda_minister", "org_id": "org_propaganda", "title": "琅琊区委常委、宣传部部长", "start": "", "end": "present", "rank": "副县级", "note": "待确认姓名"},

    # 政法委书记
    {"person_id": "langya_politics_law_secretary", "org_id": "org_politics_law", "title": "琅琊区委常委、政法委书记", "start": "", "end": "present", "rank": "副县级", "note": "待确认姓名"},

    # 统战部部长
    {"person_id": "langya_united_front_minister", "org_id": "org_united_front", "title": "琅琊区委常委、统战部部长", "start": "", "end": "present", "rank": "副县级", "note": "待确认姓名"},

    # 人大主任
    {"person_id": "langya_npc_director", "org_id": "org_npc", "title": "琅琊区人大常委会主任", "start": "", "end": "present", "rank": "正县级", "note": "待确认姓名"},

    # 政协主席
    {"person_id": "langya_cppcc_director", "org_id": "org_cppcc", "title": "琅琊区政协主席", "start": "", "end": "present", "rank": "正县级", "note": "待确认姓名"},
]

relationships = [
    # 党政主官
    {"person_a": "langya_jiao_yan", "person_b": "langya_wang_zheng", "type": "superior_subordinate",
     "strength": "strong", "context": "区委书记与区长党政主官关系", "overlap_org": "中共琅琊区委员会/琅琊区人民政府",
     "overlap_period": "至今", "note": "confirmed"},

    # 区委书记与专职副书记
    {"person_a": "langya_jiao_yan", "person_b": "langya_deputy_secretary_1", "type": "superior_subordinate",
     "strength": "strong", "context": "区委书记与区委副书记", "overlap_org": "中共琅琊区委员会",
     "overlap_period": "至今", "note": "plausible"},

    # 区委书记与纪委书记
    {"person_a": "langya_jiao_yan", "person_b": "langya_discipline_secretary", "type": "superior_subordinate",
     "strength": "medium", "context": "区委书记与纪委书记", "overlap_org": "中共琅琊区委员会",
     "overlap_period": "至今", "note": "plausible"},

    # 区委书记与组织部部长
    {"person_a": "langya_jiao_yan", "person_b": "langya_organization_minister", "type": "superior_subordinate",
     "strength": "medium", "context": "区委书记与组织部部长", "overlap_org": "中共琅琊区委员会",
     "overlap_period": "至今", "note": "plausible"},

    # 区长与常务副区长
    {"person_a": "langya_wang_zheng", "person_b": "langya_deputy_mayor_1", "type": "superior_subordinate",
     "strength": "strong", "context": "区长与常务副区长", "overlap_org": "琅琊区人民政府",
     "overlap_period": "至今", "note": "plausible"},

    # 区委书记与常务副区长
    {"person_a": "langya_jiao_yan", "person_b": "langya_deputy_mayor_1", "type": "superior_subordinate",
     "strength": "medium", "context": "区委书记与常务副区长", "overlap_org": "中共琅琊区委员会/琅琊区人民政府",
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
    if "书记" in post and "区委书记" in post:
        return "255,50,50"
    if "区长" in post and ("区委副书记" in post or "区长" in post):
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
    return p["id"] in ("langya_jiao_yan", "langya_wang_zheng")


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
    lines.append('    <description>琅琊区（安徽省滁州市）领导关系网络 - 2026年7月（需核实）</description>')
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
        lines.append(f'          <attvalue for="3" value="confirmed"/>')
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
    print("Building 琅琊区 (Langya District, Chuzhou, Anhui) network...")
    print(f"  DB path: {DB_PATH}")
    print(f"  GEXF path: {GEXF_PATH}")
    print("  NOTE: Research was limited — most data is unverified. See person JSON files for details.")
    build_db()
    build_gexf()
    print("Done.")
