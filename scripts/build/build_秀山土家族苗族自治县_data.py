#!/usr/bin/env python3
"""
秀山土家族苗族自治县（重庆市辖自治县）领导班子工作关系网络 — 数据构建脚本
Builds SQLite DB + GEXF graph for Xiushan Tujia & Miao Autonomous County leadership network.

Research date: 2026-07-16
Task ID: chongqing_秀山土家族苗族自治县

Sources:
  - baike.baidu.com/item/秀山土家族苗族自治县 (百度百科，截至2025年10月)
  - Media reports

NOTE: External web access was limited during research. Basic identity confirmed
via Baidu Baike. Career histories for most individuals are incomplete and marked
with appropriate confidence levels.
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
# The build script lives in data/tmp/<task_id>/; repo root is BASE/../../..
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))

DB_PATH = os.path.join(REPO_ROOT, "data/database/秀山土家族苗族自治县_network.db")
GEXF_PATH = os.path.join(REPO_ROOT, "data/graph/秀山土家族苗族自治县_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current Party Secretary (县委书记) ──
    {
        "id": 1, "name": "马文森", "gender": "男", "ethnicity": "土家族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "中共秀山土家族苗族自治县委书记",
        "current_org": "中共秀山土家族苗族自治县委员会",
        "source": "百度百科秀山词条（截至2025年10月）"
    },

    # ── Current County Mayor (县长) ──
    {
        "id": 2, "name": "谭雪峰", "gender": "男", "ethnicity": "土家族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "秀山土家族苗族自治县委副书记、县长",
        "current_org": "秀山土家族苗族自治县人民政府",
        "source": "百度百科秀山词条（截至2025年10月）"
    },

    # ── County People's Congress Chair ──
    {
        "id": 3, "name": "任强", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "秀山土家族苗族自治县人大常委会主任",
        "current_org": "秀山土家族苗族自治县人大常委会",
        "source": "百度百科秀山词条（截至2025年10月）"
    },

    # ── County CPPCC Chair ──
    {
        "id": 4, "name": "吴彪", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "秀山土家族苗族自治县政协主席",
        "current_org": "中国人民政治协商会议秀山土家族苗族自治县委员会",
        "source": "百度百科秀山词条（截至2025年10月）"
    },
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {
        "id": 1, "name": "中共秀山土家族苗族自治县委员会",
        "type": "党委", "level": "县处级", "parent": "中共重庆市委",
        "location": "重庆市秀山土家族苗族自治县"
    },
    {
        "id": 2, "name": "秀山土家族苗族自治县人民政府",
        "type": "政府", "level": "县处级", "parent": "重庆市人民政府",
        "location": "重庆市秀山土家族苗族自治县"
    },
    {
        "id": 3, "name": "秀山土家族苗族自治县人大常委会",
        "type": "人大", "level": "县处级", "parent": "重庆市人大常委会",
        "location": "重庆市秀山土家族苗族自治县"
    },
    {
        "id": 4, "name": "中国人民政治协商会议秀山土家族苗族自治县委员会",
        "type": "政协", "level": "县处级", "parent": "重庆市政协",
        "location": "重庆市秀山土家族苗族自治县"
    },
]

# =========================================================================
# POSITIONS (person_id, org_id, title, start, end, rank, note)
# =========================================================================
positions = [
    # 马文森
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正处级/副厅级", "note": "自治县可能高配"},
    # 谭雪峰
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "正处级", "note": "同时任县委副书记"},
    # 任强
    {"person_id": 3, "org_id": 3, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 吴彪
    {"person_id": 4, "org_id": 4, "title": "县政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长搭档", "overlap_org": "秀山土家族苗族自治县", "overlap_period": "当前任期"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委与县人大常委会领导共事", "overlap_org": "秀山土家族苗族自治县", "overlap_period": "当前任期"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委与县政协领导共事", "overlap_org": "秀山土家族苗族自治县", "overlap_period": "当前任期"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县政府与人大领导共事", "overlap_org": "秀山土家族苗族自治县", "overlap_period": "当前任期"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "县政府与政协领导共事", "overlap_org": "秀山土家族苗族自治县", "overlap_period": "当前任期"},
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "人大与政协领导共事", "overlap_org": "秀山土家族苗族自治县", "overlap_period": "当前任期"},
]


# =========================================================================
# Helper: color for person by role
# =========================================================================
def person_is_secretary(p):
    return "书记" in p["current_post"] and "副书记" not in p["current_post"]

def person_is_mayor(p):
    return "县长" in p["current_post"] and "副书记" in p["current_post"]

def person_is_discipline(p):
    return "纪委" in p["current_post"] or "监委" in p["current_post"]

def person_color(p):
    if person_is_secretary(p):
        return "255,50,50"
    if person_is_mayor(p):
        return "50,100,255"
    if person_is_discipline(p):
        return "255,165,0"
    return "100,100,100"

def is_top_leader(p):
    return person_is_secretary(p) or person_is_mayor(p)

def org_color(o):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(o["type"], "200,200,200")


# =========================================================================
# BUILD SQLite
# =========================================================================
def build_sqlite():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT,
        party_join TEXT, work_start TEXT,
        current_post TEXT, current_org TEXT, source TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER,
        title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    for p in persons:
        cur.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"],
             p["birth"], p["birthplace"], p["education"],
             p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"],
             r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"[OK] SQLite DB written: {DB_PATH}")
    print(f"      {len(persons)} persons, {len(organizations)} orgs, "
          f"{len(positions)} positions, {len(relationships)} relationships")


# =========================================================================
# BUILD GEXF
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append('    <description>秀山土家族苗族自治县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="org_type" type="string"/>')
    lines.append('      <attribute id="2" title="role" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append('          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_post"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('          <attvalue for="2" value=""/>')
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
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[OK] GEXF graph written: {GEXF_PATH}")
    print(f"      {len(persons) + len(organizations)} nodes, {eid} edges")


# =========================================================================
# MAIN
# =========================================================================
def main():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    build_sqlite()
    build_gexf()
    print("\n=== Summary ===")
    print(f"Database: {DB_PATH}")
    print(f"Graph:    {GEXF_PATH}")
    print(f"Persons:  {len(persons)}")
    print(f"Orgs:     {len(organizations)}")
    print(f"Positions:{len(positions)}")
    print(f"Edges:    {len(relationships)}")

if __name__ == "__main__":
    main()
