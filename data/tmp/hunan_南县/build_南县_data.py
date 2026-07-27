#!/usr/bin/env python3
"""
南县领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Nan County (南县) leadership network.
Investigation date: 2026-07-24

南县 is a county under 益阳市, 湖南省.

Current leadership (as of 2026-07-24):
  县委书记、县长: 钟剑波 (born 1976-11, 湖南桃江人; 县长 since 2021.10, 书记 since 2025.02)
  Predecessor 书记: 罗讯 (born 1974-09, 湖南益阳人; 曾任南县县委书记→去向待查)
  Predecessor 县长: 待查 (before 钟剑波)
"""

import sqlite3
import os
import sys
from datetime import datetime

# ── Paths ──
STAGING = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DB_PATH = os.path.join(STAGING, "南县_network.db")
GEXF_PATH = os.path.join(STAGING, "南县_network.gexf")

# ═══════════════════════════════════════════════════════════
# RESEARCH DATA
# ═══════════════════════════════════════════════════════════

PERSONS = [
    # ─── Core Leaders ───
    {
        "id": 1,
        "name": "钟剑波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-11",
        "birthplace": "湖南省桃江县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共南县委书记、县人民政府县长",
        "current_org": "中共南县委员会/南县人民政府",
        "source": "维基百科 · 南县; 中国经济网; 益阳日报; build_益阳市_data.py",
    },
    {
        "id": 2,
        "name": "罗讯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-09",
        "birthplace": "湖南益阳",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "1995-08",
        "current_post": "前任南县县委书记",
        "current_org": "中共南县委员会（前任）",
        "source": "资阳区政府网站; build_资阳区_data.py",
        "notes": "2016-2020任资阳区区长，后调任南县县委书记。约2025年2月前离任，去向待查。"
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共南县委员会", "type": "党委", "level": "县处级", "parent": "中共益阳市委", "location": "湖南省益阳市南县"},
    {"id": 2, "name": "南县人民政府", "type": "政府", "level": "县处级", "parent": "益阳市人民政府", "location": "湖南省益阳市南县"},
    {"id": 3, "name": "南县人大常委会", "type": "人大", "level": "县处级", "parent": "益阳市人大常委会", "location": "湖南省益阳市南县"},
    {"id": 4, "name": "政协南县委员会", "type": "政协", "level": "县处级", "parent": "政协益阳市委员会", "location": "湖南省益阳市南县"},
    {"id": 5, "name": "益阳市资阳区人民政府", "type": "政府", "level": "县处级", "parent": "益阳市人民政府", "location": "湖南省益阳市资阳区"},
]

POSITIONS = [
    # ─── 钟剑波 ───
    {"person_id": 1, "org_id": 2, "title": "南县人民政府县长", "start": "2021-10", "end": "", "rank": "正处级", "note": "现任; 2021.10任县长"},
    {"person_id": 1, "org_id": 1, "title": "中共南县委书记", "start": "2025-02", "end": "", "rank": "正处级", "note": "现任; 2025.02兼任县委书记"},
    # ─── 罗讯 ───
    {"person_id": 2, "org_id": 5, "title": "益阳市资阳区区长", "start": "2016", "end": "2020", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "中共南县县委书记", "start": "2020", "end": "2025-02", "rank": "正处级", "note": "前任南县县委书记; 钟剑波2025.02接任"},
]

RELATIONSHIPS = [
    # 钟剑波 ↔ 罗讯（前后任县委书记）
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "罗讯约2025年2月前离任南县县委书记后，钟剑波（时任县长）兼任县委书记",
     "overlap_org": "中共南县委员会", "overlap_period": "2025-02"},
]

# ═══════════════════════════════════════════════════════════
# DATABASE BUILD
# ═══════════════════════════════════════════════════════════

def create_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    # Remove existing DB
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE persons (
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
            source TEXT DEFAULT '',
            notes TEXT DEFAULT ''
        )
    """)
    c.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        )
    """)
    c.execute("""
        CREATE TABLE positions (
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
        )
    """)
    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in PERSONS:
        c.execute("INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source, notes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
                   p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
                   p.get("party_join", ""), p.get("work_start", ""),
                   p.get("current_post", ""), p.get("current_org", ""),
                   p.get("source", ""), p.get("notes", "")))

    for o in ORGANIZATIONS:
        c.execute("INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in POSITIONS:
        c.execute("INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
                  (pos["person_id"], pos["org_id"], pos["title"], pos.get("start", ""),
                   pos.get("end", ""), pos.get("rank", ""), pos.get("note", "")))

    for r in RELATIONSHIPS:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                  (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")


# ═══════════════════════════════════════════════════════════
# GEXF BUILD
# ═══════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(title):
    t = title
    if "书记" in t and "副" not in t:
        return "200,30,30"  # Red for party secretary
    if "县长" in t or "市长" in t or "区长" in t:
        if "副" in t:
            return "100,150,220"
        return "30,100,200"  # Blue for gov head
    if "副书记" in t:
        return "220,80,80"
    if "主任" in t or "主席" in t:
        return "60,180,60"
    if "前" in t:
        return "150,150,150"  # Grey for predecessor
    return "180,180,180"


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(org_type, "200,200,200")


def generate_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>南县领导班子工作关系网络 — 截至2026-07-24</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
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
    for p in PERSONS:
        c = person_color(p["current_post"])
        sz = "45.0" if p["id"] == 1 else "30.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        cr, cg, cb = c.split(",")
        lines.append(f'        <viz:color r="{cr}" g="{cg}" b="{cb}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in ORGANIZATIONS:
        c = org_color(o["type"])
        cr, cg, cb = c.split(",")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{cr}" g="{cg}" b="{cb}" a="0.8"/>')
        lines.append(f'        <viz:size value="18.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    added_edges = set()

    # Person → Organization (worked_at)
    for pos in POSITIONS:
        pid = pos["person_id"]
        oid = pos["org_id"]
        eid += 1
        edge_key = f"p{pid}-o{oid}-{pos['title']}"
        if edge_key in added_edges:
            continue
        added_edges.add(edge_key)
        lines.append(f'      <edge id="{eid}" source="p{pid}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos.get("start", ""))}—{esc(pos.get("end", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in RELATIONSHIPS:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF graph created: {GEXF_PATH}")


def print_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        cnt = c.fetchone()[0]
        print(f"  {table}: {cnt}")
    conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print("  南县领导班子工作关系网络 — 数据构建")
    print("  调查日期: 2026-07-24")
    print("=" * 60)
    create_db()
    generate_gexf()
    print("\n📊 Summary:")
    print_stats()
    print("Done.")
