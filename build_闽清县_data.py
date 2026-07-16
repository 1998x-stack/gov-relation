#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 闽清县 leadership network.

Research sources:
- CCTV news (2025-12-26): 闽清县委书记赵春荣 on 闽江流域智算产业集群
  https://search.cctv.com/search.php?qtext=闽清县+县委书记
- Supreme People's Procuratorate (2024-03-25): former 闽清县委书记肖华 prosecuted for bribery
- Baidu Baike: 闽清县 overview (geography/history)

Gaps:
- Current county mayor (县长) name unknown — needs further research
- 赵春荣's full career timeline before becoming 闽清县委书记
- Deputy leadership roster
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/闽清县_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/闽清县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Minqing County Party Secretary ──
    {"id": 1, "name": "赵春荣", "gender": "", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共闽清县委书记", "current_org": "中共闽清县委员会",
     "source": "https://search.cctv.com/search.php?qtext=闽清县+县委书记（2025年12月报道）"},

    # ── Former Minqing County Party Secretary (prosecuted) ──
    {"id": 2, "name": "肖华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原闽清县委书记（被调查）", "current_org": "福建省人民检察院",
     "source": "https://www.spp.gov.cn（2024年3月25日通报）"},

    # ── Earlier Minqing County Party Secretaries (from public records) ──
    {"id": 3, "name": "陈斌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "永泰县委书记", "current_org": "中共永泰县委员会",
     "source": "https://baike.baidu.com/item/陈斌（2016年尼伯特台风期间在任）"},
]

organizations = [
    {"id": 1, "name": "中共闽清县委员会", "type": "党委", "level": "县处级", "parent": "中共福州市委员会", "location": "福建福州闽清"},
    {"id": 2, "name": "闽清县人民政府", "type": "政府", "level": "县处级", "parent": "福州市人民政府", "location": "福建福州闽清"},
    {"id": 3, "name": "中共福州市委员会", "type": "党委", "level": "副省级", "parent": "中共福建省委员会", "location": "福建福州"},
    {"id": 4, "name": "福州市人民政府", "type": "政府", "level": "副省级", "parent": "福建省人民政府", "location": "福建福州"},
    {"id": 5, "name": "中共永泰县委员会", "type": "党委", "level": "县处级", "parent": "中共福州市委员会", "location": "福建福州永泰"},
]

positions = [
    # ── 赵春荣 (Zhao Chunrong) career ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共闽清县委书记", "start": "", "end": "", "rank": "县处级正职",
     "note": "现任(2025年12月CCTV报道在任)"},

    # ── 肖华 (Xiao Hua) career ──
    {"id": 2, "person_id": 2, "org_id": 1, "title": "中共闽清县委书记", "start": "", "end": "2023", "rank": "县处级正职",
     "note": "2024年因受贿被提起公诉"},
    {"id": 3, "person_id": 2, "org_id": 3, "title": "福州市人大常委会副主任", "start": "", "end": "", "rank": "副厅级",
     "note": "曾任；2024年3月被提起公诉"},

    # ── 陈斌 (Chen Bin) career ──
    {"id": 4, "person_id": 3, "org_id": 1, "title": "中共闽清县委书记", "start": "2016", "end": "", "rank": "县处级正职",
     "note": "2016年尼伯特台风期间在任"},
    {"id": 5, "person_id": 3, "org_id": 5, "title": "中共永泰县委书记", "start": "", "end": "", "rank": "县处级正职",
     "note": "后任永泰县委书记"},
]

relationships = [
    # ── Predecessor-Successor ──
    {"id": 1, "person_a_id": 2, "person_b_id": 1, "type": "交接", "context": "肖华→赵春荣 闽清县委书记交接", "overlap_org": "中共闽清县委员会", "overlap_period": ""},
    {"id": 2, "person_a_id": 3, "person_b_id": 2, "type": "交接", "context": "陈斌→肖华 闽清县委书记交接", "overlap_org": "中共闽清县委员会", "overlap_period": ""},
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
                (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                 p["birthplace"], p["education"], p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

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
lines.append(f'    <description>闽清县领导班子工作关系网络 - {today}</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# ── Attributes ──
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

# ── Nodes: Persons ──
lines.append('    <nodes>')
for p in persons:
    if p["id"] in [1]:
        # Party Secretary: Red
        r, g, b = 255, 50, 50
        size = 20.0
    elif p["id"] in [2]:
        # Former leadership with disciplinary issue: Orange-red
        r, g, b = 200, 80, 50
        size = 16.0
    else:
        # Others: Grey
        r, g, b = 100, 100, 100
        size = 12.0

    lines.append(f'      <node id="{p["id"]}" label="{p["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{p["birth"]}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{p["birthplace"]}"/>')
    lines.append(f'          <attvalue for="education" value="{p["education"]}"/>')
    lines.append(f'          <attvalue for="current_post" value="{p["current_post"]}"/>')
    lines.append(f'          <attvalue for="source" value="{p["source"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'      </node>')

# ── Nodes: Organizations ──
for o in organizations:
    oid = 1000 + o["id"]
    lines.append(f'      <node id="{oid}" label="{o["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{o["type"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="44" g="62" b="80"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'      </node>')
lines.append('    </nodes>')

# ── Edges ──
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

if __name__ == "__main__":
    print("Build script executed directly.")
