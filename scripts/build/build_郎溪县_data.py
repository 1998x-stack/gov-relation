#!/usr/bin/env python3
"""Build 郎溪县 (Langxi County, Xuancheng, Anhui) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Task: anhui_郎溪县 - 县委书记 & 县长
Province: 安徽省
City: 宣城市
Region: 郎溪县
Level: 县

Data sources:
- 中安在线/网易安徽 2026-06-01: announcement of 许立勋 as 郎溪县委书记
- 汲古知新/网易 2026-05-31: resume of 许立勋, career history
- 金台资讯/人民网 2021-05-11: 嵇文 appointed 郎溪县委书记 in 2021

Confirmed:
- 许立勋: 郎溪县委书记 (appointed 2026-05-31), b.1974-12, male, Han, 省委党校研究生
- 嵇文: 前任县委书记 (2021-05 to 2026-05), now 宣城市副市长 (since 2025-06)
- 彭禧元: earlier 县委书记 (before 2021)

NOTE: Web search (Exa) rate-limited. Government website (langxi.gov.cn) inaccessible from
this environment. Current 郎溪县长 name not confirmed (许立勋 served as 泾县县长 before
becoming 郎溪县委书记; the county mayor role after his departure needs live verification).
"""
import json
import os
import sqlite3
from datetime import datetime

# ── paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if "data/tmp" in SCRIPT_DIR:
    STAGING = SCRIPT_DIR
    DB_PATH = os.path.join(STAGING, "郎溪县_network.db")
    GEXF_PATH = os.path.join(STAGING, "郎溪县_network.gexf")
else:
    REPO = SCRIPT_DIR
    DB_PATH = os.path.join(REPO, "data/database", "郎溪县_network.db")
    GEXF_PATH = os.path.join(REPO, "data/graph", "郎溪县_network.gexf")

# ── research data ──

persons = [
    # ═══ Current Top Leaders ═══

    # 县委书记 — 许立勋 (confirmed from 中安在线/汲古知新 2026-05-31)
    {
        "id": "langxi_xu_lixun",
        "name": "许立勋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-12",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郎溪县委书记",
        "current_org": "中共郎溪县委员会",
        "source": "汲古知新/网易 2026-05-31; 中安在线 2026-06-01",
        "notes": "confirmed: 2026-05-31 appointed 郎溪县委书记。1974年12月生，省委党校研究生学历。曾任宣城市总工会党组成员、副主席，宁国市副市长，宁国市委常委、政法委书记，宣城市委宣传部副部长，宣城市委宣传部副部长、市政府新闻办公室主任（兼），宣城市委宣传部常务副部长、市政府新闻办公室主任（兼）。2021年12月任泾县县委副书记、县政府党组书记，次月当选泾县县长。",
        "confidence": "confirmed"
    },

    # 县长 — 待确认 (许立勋之前任泾县县长，调任郎溪县委书记后县长空缺)
    {
        "id": "langxi_county_mayor",
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郎溪县委副书记、县长（待确认）",
        "current_org": "郎溪县人民政府/中共郎溪县委员会",
        "source": "需从 langxi.gov.cn 或宣城市委组织部任前公示确认",
        "notes": "许立勋原为泾县县长，2026-05调任郎溪县委书记后，县长职位需从宣城市委组织部确认新任者。",
        "confidence": "unverified"
    },

    # ═══ Previous Leaders ═══

    # 前任县委书记 — 嵇文 (now 宣城市副市长)
    {
        "id": "langxi_ji_wen",
        "name": "嵇文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宣城市副市长",
        "current_org": "宣城市人民政府",
        "source": "金台资讯/人民网 2021-05-11; 汲古知新 2026-05-31",
        "notes": "前任郎溪县委书记（2021-05-10至2026-05-31）。2025年6月升任宣城市副市长。",
        "confidence": "confirmed"
    },

    # 更早前任县委书记 — 彭禧元 (2021年卸任)
    {
        "id": "langxi_peng_xiyuan",
        "name": "彭禧元",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（2021年5月卸任郎溪县委书记）",
        "current_org": "",
        "source": "金台资讯/人民网 2021-05-11",
        "notes": "2021年5月10日不再担任郎溪县委书记。去向待查。",
        "confidence": "confirmed"
    },

    # ═══ Key Deputy Positions (placeholder — names need live verification) ═══

    {
        "id": "langxi_deputy_secretary",
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郎溪县委专职副书记（待确认）",
        "current_org": "中共郎溪县委员会",
        "source": "需从 langxi.gov.cn 确认",
        "notes": "县委专职副书记。",
        "confidence": "unverified"
    },
    {
        "id": "langxi_discipline_secretary",
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郎溪县委常委、纪委书记（待确认）",
        "current_org": "中共郎溪县纪律检查委员会",
        "source": "需从 langxi.gov.cn 确认",
        "notes": "县纪委书记。",
        "confidence": "unverified"
    },
    {
        "id": "langxi_executive_deputy",
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郎溪县委常委、常务副县长（待确认）",
        "current_org": "郎溪县人民政府",
        "source": "需从 langxi.gov.cn 确认",
        "notes": "县政府常务副县长。",
        "confidence": "unverified"
    },
    {
        "id": "langxi_organization_minister",
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郎溪县委常委、组织部部长（待确认）",
        "current_org": "中共郎溪县委组织部",
        "source": "需从 langxi.gov.cn 确认",
        "notes": "县委组织部部长。",
        "confidence": "unverified"
    },
    {
        "id": "langxi_propaganda_minister",
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郎溪县委常委、宣传部部长（待确认）",
        "current_org": "中共郎溪县委宣传部",
        "source": "需从 langxi.gov.cn 确认",
        "notes": "县委宣传部部长。",
        "confidence": "unverified"
    },
    {
        "id": "langxi_united_front_minister",
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郎溪县委常委、统战部部长（待确认）",
        "current_org": "中共郎溪县委统战部",
        "source": "需从 langxi.gov.cn 确认",
        "notes": "县委统战部部长。",
        "confidence": "unverified"
    },
    {
        "id": "langxi_political_legal",
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郎溪县委常委、政法委书记（待确认）",
        "current_org": "中共郎溪县委政法委员会",
        "source": "需从 langxi.gov.cn 确认",
        "notes": "县委政法委书记。",
        "confidence": "unverified"
    },
]

organizations = [
    {
        "id": "org_cpc_langxi",
        "name": "中共郎溪县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共宣城市委员会",
        "location": "安徽省宣城市郎溪县"
    },
    {
        "id": "org_langxi_gov",
        "name": "郎溪县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "宣城市人民政府",
        "location": "安徽省宣城市郎溪县"
    },
    {
        "id": "org_discipline",
        "name": "中共郎溪县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共郎溪县委员会/中共宣城市纪律检查委员会",
        "location": "安徽省宣城市郎溪县"
    },
    {
        "id": "org_organization",
        "name": "中共郎溪县委组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共郎溪县委员会",
        "location": "安徽省宣城市郎溪县"
    },
    {
        "id": "org_propaganda",
        "name": "中共郎溪县委宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共郎溪县委员会",
        "location": "安徽省宣城市郎溪县"
    },
    {
        "id": "org_united_front",
        "name": "中共郎溪县委统战部",
        "type": "党委",
        "level": "县级",
        "parent": "中共郎溪县委员会",
        "location": "安徽省宣城市郎溪县"
    },
    {
        "id": "org_political_legal",
        "name": "中共郎溪县委政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共郎溪县委员会",
        "location": "安徽省宣城市郎溪县"
    },
    {
        "id": "org_military",
        "name": "郎溪县人民武装部",
        "type": "政府",
        "level": "县级",
        "parent": "宣城军分区",
        "location": "安徽省宣城市郎溪县"
    },
    {
        "id": "org_npc",
        "name": "郎溪县人大常委会",
        "type": "人大",
        "level": "县级",
        "parent": "宣城市人大常委会",
        "location": "安徽省宣城市郎溪县"
    },
    {
        "id": "org_cppcc",
        "name": "中国人民政治协商会议郎溪县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "政协宣城市委员会",
        "location": "安徽省宣城市郎溪县"
    },
    # External orgs for predecessor/successor tracking
    {
        "id": "org_xuancheng_gov",
        "name": "宣城市人民政府",
        "type": "政府",
        "level": "地市级",
        "parent": "安徽省人民政府",
        "location": "安徽省宣城市"
    },
    {
        "id": "org_jingxian_gov",
        "name": "泾县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "宣城市人民政府",
        "location": "安徽省宣城市泾县"
    },
    {
        "id": "org_cpc_jingxian",
        "name": "中共泾县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共宣城市委员会",
        "location": "安徽省宣城市泾县"
    },
]

positions = [
    # 许立勋 — 郎溪县委书记
    {"person_id": "langxi_xu_lixun", "org_id": "org_cpc_langxi", "title": "郎溪县委书记",
     "start": "2026-05", "end": "present", "rank": "正县级", "note": "confirmed from appointment notice"},

    # 许立勋 — 曾任泾县县长
    {"person_id": "langxi_xu_lixun", "org_id": "org_jingxian_gov", "title": "泾县县委副书记、县长",
     "start": "2021-12", "end": "2026-05", "rank": "正县级", "note": "2021年12月任泾县县委副书记、县政府党组书记，次月当选县长"},
    {"person_id": "langxi_xu_lixun", "org_id": "org_cpc_jingxian", "title": "泾县县委副书记",
     "start": "2021-12", "end": "2026-05", "rank": "正县级", "note": ""},

    # 许立勋 — 宣城市委宣传部
    {"person_id": "langxi_xu_lixun", "org_id": "org_cpc_langxi", "title": "宣城市委宣传部常务副部长、市政府新闻办公室主任（兼）",
     "start": "", "end": "2021-12", "rank": "正县级", "note": "之前曾任宣传部副部长/市政府新闻办主任"},

    # 嵇文 — 前任县委书记
    {"person_id": "langxi_ji_wen", "org_id": "org_cpc_langxi", "title": "郎溪县委书记",
     "start": "2021-05", "end": "2026-05", "rank": "正县级", "note": "2021-05-10至2026-05-31"},
    {"person_id": "langxi_ji_wen", "org_id": "org_xuancheng_gov", "title": "宣城市副市长",
     "start": "2025-06", "end": "present", "rank": "副厅级", "note": "2025年6月起任宣城市副市长"},

    # 彭禧元 — 更早县委书记
    {"person_id": "langxi_peng_xiyuan", "org_id": "org_cpc_langxi", "title": "郎溪县委书记",
     "start": "", "end": "2021-05", "rank": "正县级", "note": "2021年5月10日不再担任"},
]

relationships = [
    # 许立勋 ↔ 嵇文 (predecessor/successor)
    {"person_a": "langxi_xu_lixun", "person_b": "langxi_ji_wen", "type": "predecessor_successor",
     "strength": "strong", "context": "许立勋接替嵇文任郎溪县委书记",
     "overlap_org": "中共郎溪县委员会",
     "overlap_period": "2026-05",
     "note": "confirmed from appointment notice; 嵇文升任宣城市副市长"},

    # 嵇文 ↔ 彭禧元 (predecessor/successor)
    {"person_a": "langxi_ji_wen", "person_b": "langxi_peng_xiyuan", "type": "predecessor_successor",
     "strength": "strong", "context": "嵇文接替彭禧元任郎溪县委书记",
     "overlap_org": "中共郎溪县委员会",
     "overlap_period": "2021-05",
     "note": "confirmed from 金台资讯 2021-05-11"},
]


# ── HELPERS ──

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    post = p["current_post"]
    if "书记" in post and "县委" in post and "纪委" not in post and "政法" not in post:
        return "255,50,50"
    if "县长" in post or "代县长" in post:
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
    return p["id"] in ("langxi_xu_lixun",)


# ── BUILD DB ──

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


# ── BUILD GEXF ──

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>郎溪县（安徽省宣城市）领导关系网络 - 2026年7月</description>')
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


# ── MAIN ──

if __name__ == "__main__":
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    print("Building 郎溪县 (Langxi County, Xuancheng, Anhui) network...")
    print(f"  DB path: {DB_PATH}")
    print(f"  GEXF path: {GEXF_PATH}")
    print("  NOTE: 许立勋 confirmed as 县委书记 from public sources.")
    print("  Current 县长 and full roster need live langxi.gov.cn verification.")
    build_db()
    build_gexf()
    print("Done.")
