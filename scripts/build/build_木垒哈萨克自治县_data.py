#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 木垒哈萨克自治县 (Mori Kazakh Autonomous County), 昌吉回族自治州, 新疆维吾尔自治区."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/xinjiang_木垒哈萨克自治县")
DB_PATH = os.path.join(TMP, "木垒哈萨克自治县_network.db")
GEXF_PATH = os.path.join(TMP, "木垒哈萨克自治县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    # NOTE: 县委书记 (Party Secretary) - identity NOT confirmed from web search. Gap.
    # Based on county-government structure, the 县委书记 would be the top leader.
    # Confirmed government leader:

    {"id": 1, "name": "祖哈尔", "gender": "女", "ethnicity": "哈萨克族",
     "birth": "1983-01", "birthplace": "新疆", "education": "大学本科/工程硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "木垒哈萨克自治县委副书记、县人民政府党组书记、县长",
     "current_org": "木垒哈萨克自治县人民政府",
     "source": "https://www.mlx.gov.cn/p212/xc/20251112/381485.html"},

    # ── County Government Leadership Team ──
    {"id": 2, "name": "王军", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-04", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "木垒哈萨克自治县委常委、县人民政府党组副书记、常务副县长",
     "current_org": "木垒哈萨克自治县人民政府",
     "source": "https://www.mlx.gov.cn/p212/cwfxc/20250804/273388.html"},

    {"id": 3, "name": "朱虹戌", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-09", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "木垒哈萨克自治县人民政府党组成员、副县长、县公安局党委书记、局长",
     "current_org": "木垒哈萨克自治县人民政府",
     "source": "https://www.mlx.gov.cn/p212/fxc/20250804/273386.html"},

    {"id": 4, "name": "哈斯特尔", "gender": "男", "ethnicity": "哈萨克族",
     "birth": "1984-09", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "木垒哈萨克自治县人民政府党组成员、副县长",
     "current_org": "木垒哈萨克自治县人民政府",
     "source": "https://www.mlx.gov.cn/p212/fxc/20250804/273387.html"},

    {"id": 5, "name": "安磊", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-01", "birthplace": "", "education": "硕士研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "木垒哈萨克自治县人民政府党组成员、副县长",
     "current_org": "木垒哈萨克自治县人民政府",
     "source": "https://www.mlx.gov.cn/p212/fxc/20250804/317659.html"},

    {"id": 6, "name": "沙拉买提·买木提明", "gender": "女", "ethnicity": "维吾尔族",
     "birth": "1982-05", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "木垒哈萨克自治县人民政府党组成员、副县长",
     "current_org": "木垒哈萨克自治县人民政府",
     "source": "https://www.mlx.gov.cn/p212/fxc/20250804/317660.html"},
]

organizations = [
    {"id": 1, "name": "中共木垒哈萨克自治县委员会", "type": "党委", "level": "县处级",
     "parent": "中共昌吉回族自治州委员会", "location": "新疆昌吉州木垒哈萨克自治县"},
    {"id": 2, "name": "木垒哈萨克自治县人民政府", "type": "政府", "level": "县处级",
     "parent": "昌吉回族自治州人民政府", "location": "新疆昌吉州木垒哈萨克自治县"},
    {"id": 3, "name": "木垒哈萨克自治县公安局", "type": "政府", "level": "乡科级",
     "parent": "木垒哈萨克自治县人民政府", "location": "新疆昌吉州木垒哈萨克自治县"},
    {"id": 4, "name": "木垒哈萨克自治县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "昌吉回族自治州人大常委会", "location": "新疆昌吉州木垒哈萨克自治县"},
    {"id": 5, "name": "中国人民政治协商会议木垒哈萨克自治县委员会", "type": "政协", "level": "县处级",
     "parent": "昌吉回族自治州政协", "location": "新疆昌吉州木垒哈萨克自治县"},
]

positions = [
    # ── 祖哈尔 (County Magistrate) ──
    {"person_id": 1, "org_id": 1, "title": "木垒哈萨克自治县委副书记",
     "start": "unknown", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "县人民政府党组书记、县长",
     "start": "unknown", "end": "present", "rank": "正县级", "note": "主持县人民政府全面工作"},

    # ── 王军 (Executive Deputy County Magistrate) ──
    {"person_id": 2, "org_id": 1, "title": "县委常委",
     "start": "unknown", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县人民政府党组副书记、常务副县长",
     "start": "unknown", "end": "present", "rank": "副县级",
     "note": "负责县政府常务工作，分管发改、财政、统计、应急管理等"},

    # ── 朱虹戌 (Deputy County Magistrate & Public Security) ──
    {"person_id": 3, "org_id": 2, "title": "县人民政府党组成员、副县长",
     "start": "unknown", "end": "present", "rank": "副县级", "note": "负责公安、司法、信访等"},
    {"person_id": 3, "org_id": 3, "title": "县公安局党委书记、局长",
     "start": "unknown", "end": "present", "rank": "正科级", "note": "主持公安局工作"},

    # ── 哈斯特尔 (Deputy County Magistrate - Agriculture) ──
    {"person_id": 4, "org_id": 2, "title": "县人民政府党组成员、副县长",
     "start": "unknown", "end": "present", "rank": "副县级",
     "note": "负责第一产业（农业农村、林业草原水利等）。挂职期间由安磊代管"},

    # ── 安磊 (Deputy County Magistrate - Industry) ──
    {"person_id": 5, "org_id": 2, "title": "县人民政府党组成员、副县长",
     "start": "unknown", "end": "present", "rank": "副县级",
     "note": "负责第二产业（工业经济、园区、住建、交通等）"},

    # ── 沙拉买提·买木提明 (Deputy County Magistrate - Tertiary Industry) ──
    {"person_id": 6, "org_id": 2, "title": "县人民政府党组成员、副县长",
     "start": "unknown", "end": "present", "rank": "副县级",
     "note": "负责第三产业（市场监管、卫健委、教育、文旅等）"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "strength": "strong",
     "context": "祖哈尔(县长)与王军(常务副县长)是县政府党政正副搭档关系",
     "overlap_org": "木垒哈萨克自治县人民政府",
     "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "strength": "strong",
     "context": "祖哈尔(县长)与朱虹戌(副县长兼公安局长)在县政府共事",
     "overlap_org": "木垒哈萨克自治县人民政府",
     "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "strength": "strong",
     "context": "祖哈尔(县长)与哈斯特尔(副县长)在县政府共事",
     "overlap_org": "木垒哈萨克自治县人民政府",
     "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "strength": "strong",
     "context": "祖哈尔(县长)与安磊(副县长)在县政府共事，安磊代管哈斯特尔的第一产业工作",
     "overlap_org": "木垒哈萨克自治县人民政府",
     "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "strength": "strong",
     "context": "祖哈尔(县长)与沙拉买提(副县长)在县政府共事",
     "overlap_org": "木垒哈萨克自治县人民政府",
     "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "strength": "strong",
     "context": "王军(常务副县长)与朱虹戌(副县长兼公安局长)在县政府班子共事",
     "overlap_org": "木垒哈萨克自治县人民政府",
     "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "strength": "strong",
     "context": "王军(常务副县长)与安磊(副县长)在县政府共事，安磊协助王军分管应急管理、国资监管",
     "overlap_org": "木垒哈萨克自治县人民政府",
     "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 5, "type": "overlap", "strength": "medium",
     "context": "哈斯特尔(副县长)挂职期间由安磊(副县长)代管第一产业工作",
     "overlap_org": "木垒哈萨克自治县人民政府",
     "overlap_period": "present", "confidence": "confirmed"},
]

# ── HELPERS ─────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    role = p["current_post"]
    if "县委书记" in role and "副书记" not in role:
        return "255,50,50"
    elif "县长" in role:
        return "50,100,255"
    elif "人大" in role:
        return "200,255,255"
    elif "政协" in role:
        return "255,240,200"
    elif "纪委书记" in role or "纪检" in role:
        return "255,165,0"
    else:
        return "100,100,100"

def org_color(o):
    t = o["type"]
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }.get(t, "200,200,200")

def is_top_leader(p):
    role = p["current_post"]
    return ("县委书记" in role and "副书记" not in role) or ("县长" in role and "副书记" in role)

def person_size(p):
    return "20.0" if is_top_leader(p) else "12.0"

# ── BUILD DB ─────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT, strength TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT, confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, strength, context, overlap_org, overlap_period, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["strength"],
             r["context"], r["overlap_org"], r["overlap_period"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")

# ── BUILD GEXF ────────────────────────────────────────────────

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append('    <description>木垒哈萨克自治县领导班子工作关系网络 - 新疆昌吉回族自治州木垒县</description>')
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
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["parent"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])}~{esc(pos["end"])}"/>')
        lines.append(f'          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationships)
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append(f'          <attvalue for="3" value="{r["confidence"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {GEXF_PATH}")

# ── SUMMARY ──────────────────────────────────────────────────

def print_summary():
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()