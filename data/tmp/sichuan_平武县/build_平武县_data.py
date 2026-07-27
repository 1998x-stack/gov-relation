#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Pingwu County (平武县) leadership network.

平武县 — 四川省绵阳市下辖县
Sources: Official government website (pingwu.gov.cn), leadership page as of 2025-04.
"""

import json
import os
import sqlite3
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
# When promoted: these paths point to canonical locations
DB_PATH = os.path.join(BASE, "平武县_network.db")
GEXF_PATH = os.path.join(BASE, "平武县_network.gexf")
PERSON_DIR = BASE

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {
        "id": 1, "name": "姜坤", "gender": "男", "ethnicity": "羌族",
        "birth": "1978-08", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "中共平武县委书记",
        "current_org": "中共平武县委员会",
        "source": "https://www.pingwu.gov.cn/pingwu/c115811/202504/95b88edd439f417e8dda2561088c9d3a.shtml",
    },
    {
        "id": 2, "name": "赵琳", "gender": "女", "ethnicity": "汉族",
        "birth": "1981-10", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "平武县委副书记、县长",
        "current_org": "平武县人民政府",
        "source": "https://www.pingwu.gov.cn/pingwu/c115812/202604/6ce921fa873a4e0ba1efb05b6a12cf8a.shtml",
    },
    # ── County Party Committee (县委) Members ──
    {
        "id": 3, "name": "梁帮浩", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "平武县委副书记",
        "current_org": "中共平武县委员会",
        "source": "https://www.pingwu.gov.cn/pingwu/c115811/ldzc.shtml",
    },
    {
        "id": 4, "name": "巩宁", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "平武县委常委、统战部部长",
        "current_org": "中共平武县委员会",
        "source": "https://www.pingwu.gov.cn/pingwu/c115811/ldzc.shtml",
    },
    {
        "id": 5, "name": "田佳龄", "gender": "女", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "平武县委常委、纪委书记、县监委主任",
        "current_org": "中共平武县纪律检查委员会",
        "source": "https://www.pingwu.gov.cn/pingwu/c115811/ldzc.shtml",
    },
    {
        "id": 6, "name": "张仁斌", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "平武县委常委、政法委书记",
        "current_org": "中共平武县委员会",
        "source": "https://www.pingwu.gov.cn/pingwu/c115811/ldzc.shtml",
    },
    {
        "id": 7, "name": "王小江", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "平武县委常委、人武部政委",
        "current_org": "平武县人民武装部",
        "source": "https://www.pingwu.gov.cn/pingwu/c115811/ldzc.shtml",
    },
    {
        "id": 8, "name": "吴浩", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "平武县委常委、副县长（挂职）",
        "current_org": "平武县人民政府",
        "source": "https://www.pingwu.gov.cn/pingwu/c115811/ldzc.shtml",
    },
    {
        "id": 9, "name": "朱沛元", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "平武县委常委、常务副县长",
        "current_org": "平武县人民政府",
        "source": "https://www.pingwu.gov.cn/pingwu/c115811/ldzc.shtml",
    },
    {
        "id": 10, "name": "杨鹏", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "平武县委常委、组织部部长",
        "current_org": "中共平武县委员会",
        "source": "https://www.pingwu.gov.cn/pingwu/c115811/ldzc.shtml",
    },
    {
        "id": 11, "name": "杨蕊铱", "gender": "女", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "平武县委常委、宣传部部长",
        "current_org": "中共平武县委员会",
        "source": "https://www.pingwu.gov.cn/pingwu/c115811/ldzc.shtml",
    },
    # ── County Government Deputy Leaders ──
    {
        "id": 12, "name": "张绍菊", "gender": "女", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "平武县副县长",
        "current_org": "平武县人民政府",
        "source": "https://www.pingwu.gov.cn/pingwu/c115812/ldzc.shtml",
    },
    {
        "id": 13, "name": "盛天晓", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "平武县副县长",
        "current_org": "平武县人民政府",
        "source": "https://www.pingwu.gov.cn/pingwu/c115812/ldzc.shtml",
    },
    {
        "id": 14, "name": "刘鹏", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "平武县副县长",
        "current_org": "平武县人民政府",
        "source": "https://www.pingwu.gov.cn/pingwu/c115812/ldzc.shtml",
    },
    {
        "id": 15, "name": "薛成", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "平武县副县长",
        "current_org": "平武县人民政府",
        "source": "https://www.pingwu.gov.cn/pingwu/c115812/ldzc.shtml",
    },
    {
        "id": 16, "name": "王金柱", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "平武县副县长、县公安局局长",
        "current_org": "平武县人民政府",
        "source": "https://www.pingwu.gov.cn/pingwu/c115812/ldzc.shtml",
    },
]

organizations = [
    {"id": 1, "name": "中共平武县委员会", "type": "党委", "level": "县处级",
     "parent": "中共绵阳市委员会", "location": "四川绵阳平武"},
    {"id": 2, "name": "平武县人民政府", "type": "政府", "level": "县处级",
     "parent": "绵阳市人民政府", "location": "四川绵阳平武"},
    {"id": 3, "name": "中共平武县纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共绵阳市纪律检查委员会", "location": "四川绵阳平武"},
    {"id": 4, "name": "平武县人民武装部", "type": "军事", "level": "县处级",
     "parent": "", "location": "四川绵阳平武"},
    {"id": 5, "name": "平武县人大常委会", "type": "人大", "level": "县处级",
     "parent": "绵阳市人大常委会", "location": "四川绵阳平武"},
    {"id": 6, "name": "政协平武县委员会", "type": "政协", "level": "县处级",
     "parent": "政协绵阳市委员会", "location": "四川绵阳平武"},
    {"id": 7, "name": "河北—平武工业园区", "type": "开发区", "level": "县处级",
     "parent": "平武县人民政府", "location": "四川绵阳平武"},
    {"id": 8, "name": "平武县公安局", "type": "政府", "level": "县处级",
     "parent": "平武县人民政府", "location": "四川绵阳平武"},
]

positions = [
    # 姜坤 career (partial - limited public data)
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共平武县委书记",
     "start": "", "end": "", "rank": "县处级正职", "note": "现任，就任具体时间待查"},
    # 赵琳 career (partial - limited public data)
    {"id": 2, "person_id": 2, "org_id": 1, "title": "平武县委副书记",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 3, "person_id": 2, "org_id": 2, "title": "平武县人民政府县长",
     "start": "", "end": "", "rank": "县处级正职", "note": "现任，as of time待查"},
    # Party Committee members - current roles
    {"id": 4, "person_id": 3, "org_id": 1, "title": "平武县委副书记",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 5, "person_id": 4, "org_id": 1, "title": "平武县委常委、统战部部长",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 6, "person_id": 5, "org_id": 3, "title": "平武县委常委、纪委书记、县监委主任",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 7, "person_id": 6, "org_id": 1, "title": "平武县委常委、政法委书记",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 8, "person_id": 7, "org_id": 4, "title": "平武县委常委、人武部政委",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 9, "person_id": 8, "org_id": 2, "title": "平武县委常委、副县长（挂职）",
     "start": "", "end": "", "rank": "县处级副职", "note": "挂职"},
    {"id": 10, "person_id": 9, "org_id": 2, "title": "平武县委常委、常务副县长",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 11, "person_id": 10, "org_id": 1, "title": "平武县委常委、组织部部长",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 12, "person_id": 11, "org_id": 1, "title": "平武县委常委、宣传部部长",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    # Deputy county heads
    {"id": 13, "person_id": 12, "org_id": 2, "title": "平武县副县长",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 14, "person_id": 13, "org_id": 2, "title": "平武县副县长",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 15, "person_id": 14, "org_id": 2, "title": "平武县副县长",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 16, "person_id": 15, "org_id": 2, "title": "平武县副县长",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 17, "person_id": 16, "org_id": 2, "title": "平武县副县长、县公安局局长",
     "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
]

relationships = [
    # Predecessor-Successor (all unverified - need to confirm predecessors)
]

# ── BUILD SQLite DATABASE ────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE persons (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    gender TEXT,
    ethnicity TEXT,
    birth TEXT,
    birthplace TEXT,
    education TEXT,
    party_join TEXT,
    work_start TEXT,
    current_post TEXT,
    current_org TEXT,
    source TEXT
);

CREATE TABLE organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

CREATE TABLE positions (
    id INTEGER PRIMARY KEY,
    person_id INTEGER NOT NULL,
    org_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE relationships (
    id INTEGER PRIMARY KEY,
    person_a_id INTEGER NOT NULL,
    person_b_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a_id) REFERENCES persons(id),
    FOREIGN KEY (person_b_id) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
                 p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
                 p.get("party_join", ""), p.get("work_start", ""),
                 p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

for o in organizations:
    cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)""",
                (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                 pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("""INSERT INTO relationships VALUES (?,?,?,?,?,?,?)""",
                (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
                 r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

# Summary stats
cur.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]

conn.close()
print(f"SQLite database written: {DB_PATH}")
print(f"  Persons: {person_count}")
print(f"  Organizations: {org_count}")
print(f"  Positions: {pos_count}")
print(f"  Relationships: {rel_count}")


# ── BUILD GEXF GRAPH ────────────────────────────────────────────────

today = datetime.now().strftime("%Y-%m-%d")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>平武县领导班子工作关系网络 - {today}</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="category" title="Category" type="string"/>')
lines.append('      <attribute id="birth" title="Birth" type="string"/>')
lines.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
lines.append('      <attribute id="education" title="Education" type="string"/>')
lines.append('      <attribute id="current_post" title="Current Post" type="string"/>')
lines.append('      <attribute id="source" title="Source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="context" title="Context" type="string"/>')
lines.append('      <attribute id="period" title="Period" type="string"/>')
lines.append('    </attributes>')

# Nodes: Persons
lines.append('    <nodes>')
for p in persons:
    pid = p["id"]
    # Color by role
    if pid == 1:
        r, g, b = 255, 50, 50   # Red: Party Secretary
        sz = 20.0
    elif pid == 2:
        r, g, b = 50, 100, 255  # Blue: County Mayor
        sz = 20.0
    elif pid == 5:
        r, g, b = 255, 165, 0   # Orange: Discipline Inspection
        sz = 16.0
    else:
        r, g, b = 100, 100, 100 # Grey: others
        sz = 12.0

    lines.append(f'      <node id="{pid}" label="{p["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{p.get("birth", "")}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{p.get("birthplace", "")}"/>')
    lines.append(f'          <attvalue for="education" value="{p.get("education", "")}"/>')
    lines.append(f'          <attvalue for="current_post" value="{p.get("current_post", "")}"/>')
    lines.append(f'          <attvalue for="source" value="{p.get("source", "")}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append(f'      </node>')

# Nodes: Organizations
for o in organizations:
    oid = 1000 + o["id"]
    # Org type color
    type_colors = {
        "党委": (255, 200, 200),
        "政府": (200, 200, 255),
        "纪委": (255, 200, 200),
        "人大": (200, 255, 255),
        "政协": (255, 240, 200),
        "军事": (220, 220, 220),
        "开发区": (200, 255, 200),
    }
    cr, cg, cb = type_colors.get(o["type"], (200, 200, 200))
    lines.append(f'      <node id="{oid}" label="{o["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{o["type"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{cr}" g="{cg}" b="{cb}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
edge_id = 1

# person→organization (worked_at)
for pos in positions:
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="{edge_id}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{pos["title"]}"/>')
    lines.append(f'          <attvalue for="period" value="{pos["start"] or "?"} → {pos["end"] or "今"}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

# person↔person (relationships)
for r in relationships:
    lines.append(f'      <edge id="{edge_id}" source="{r["person_a_id"]}" target="{r["person_b_id"]}" label="{r["type"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{r["type"]}"/>')
    lines.append(f'          <attvalue for="context" value="{r["context"]}"/>')
    lines.append(f'          <attvalue for="period" value="{r["overlap_period"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

total_nodes = len(persons) + len(organizations)
total_edges = len(positions) + len(relationships)
print(f"\nGEXF graph written: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} organizations = {total_nodes} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {total_edges} total")
print("\nDone!")