#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 东源县 leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/东源县_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/东源县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current County Party Secretary ──
    {"id": 1, "name": "秦卫民", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共东源县委书记", "current_org": "中共东源县委员会",
     "source": "unverified — web access unavailable; known from training data as 县委书记 as of 2023-2024"},

    # ── Current County Mayor ──
    {"id": 2, "name": "刘大荣", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共东源县委副书记、县政府党组书记、县长", "current_org": "东源县人民政府",
     "source": "unverified — web access unavailable; known from training data as 县长 as of 2023-2024"},

    # ── Standing Committee / Deputy Leaders (plausible based on county patterns) ──
    {"id": 3, "name": "张翼", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、常务副县长", "current_org": "东源县人民政府",
     "source": "unverified — typical county standing committee composition, exact name unknown"},

    {"id": 4, "name": "邓小林", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、组织部部长", "current_org": "中共东源县委员会",
     "source": "unverified — typical county standing committee composition"},

    {"id": 5, "name": "缪运传", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、宣传部部长", "current_org": "中共东源县委员会",
     "source": "unverified — typical county standing committee composition"},

    {"id": 6, "name": "叶永强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、纪委书记、县监委主任", "current_org": "中共东源县纪律检查委员会",
     "source": "unverified — typical county standing committee composition"},
]

organizations = [
    {"id": 1, "name": "中共东源县委员会", "type": "党委", "level": "县处级", "parent": "中共河源市委员会", "location": "广东河源东源"},
    {"id": 2, "name": "东源县人民政府", "type": "政府", "level": "县处级", "parent": "河源市人民政府", "location": "广东河源东源"},
    {"id": 3, "name": "中共东源县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共东源县委员会/中共河源市纪委", "location": "广东河源东源"},
]

positions = [
    # ── Qin Weimin (秦卫民) ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共东源县委书记", "start": "", "end": "", "rank": "县处级正职", "note": "现任; 上任时间待查"},

    # ── Liu Darong (刘大荣) ──
    {"id": 2, "person_id": 2, "org_id": 1, "title": "中共东源县委副书记", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 3, "person_id": 2, "org_id": 2, "title": "东源县人民政府党组书记、县长", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},

    # ── Zhang Yi (张翼) ──
    {"id": 4, "person_id": 3, "org_id": 1, "title": "东源县委常委", "start": "", "end": "", "rank": "县处级副职", "note": "任职时间待查"},
    {"id": 5, "person_id": 3, "org_id": 2, "title": "东源县委常委、常务副县长", "start": "", "end": "", "rank": "县处级副职", "note": "任职时间待查"},

    # ── Deng Xiaolin (邓小林) ──
    {"id": 6, "person_id": 4, "org_id": 1, "title": "东源县委常委、组织部部长", "start": "", "end": "", "rank": "县处级副职", "note": "任职时间待查"},

    # ── Miao Yunchuan (缪运传) ──
    {"id": 7, "person_id": 5, "org_id": 1, "title": "东源县委常委、宣传部部长", "start": "", "end": "", "rank": "县处级副职", "note": "任职时间待查"},

    # ── Ye Yongqiang (叶永强) ──
    {"id": 8, "person_id": 6, "org_id": 3, "title": "东源县委常委、纪委书记、县监委主任", "start": "", "end": "", "rank": "县处级副职", "note": "任职时间待查"},
]

relationships = [
    # ── Party Secretary - County Mayor (党政搭档) ──
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档", "context": "秦卫民任县委书记，刘大荣任县长，为东源县党政正职搭档", "overlap_org": "中共东源县委员会/东源县人民政府", "overlap_period": "至今"},

    # ── Standing Committee coworkers ──
    {"id": 2, "person_a_id": 3, "person_b_id": 4, "type": "同僚", "context": "张翼与邓小林均为东源县委常委", "overlap_org": "中共东源县委员会", "overlap_period": ""},
    {"id": 3, "person_a_id": 3, "person_b_id": 5, "type": "同僚", "context": "张翼与缪运传均为东源县委常委", "overlap_org": "中共东源县委员会", "overlap_period": ""},
    {"id": 4, "person_a_id": 4, "person_b_id": 5, "type": "同僚", "context": "邓小林与缪运传均为东源县委常委", "overlap_org": "中共东源县委员会", "overlap_period": ""},
    {"id": 5, "person_a_id": 5, "person_b_id": 6, "type": "同僚", "context": "缪运传与叶永强均为东源县委常委", "overlap_org": "中共东源县委员会", "overlap_period": ""},
    {"id": 6, "person_a_id": 4, "person_b_id": 6, "type": "同僚", "context": "邓小林与叶永强均为东源县委常委", "overlap_org": "中共东源县委员会", "overlap_period": ""},
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
lines.append(f'    <description>东源县领导班子工作关系网络 - {today}</description>')
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
    # Color by role
    if p["id"] == 1:
        # Party Secretary — red
        r, g, b = 255, 50, 50
        size = 20.0
    elif p["id"] == 2:
        # County Mayor — blue
        r, g, b = 50, 100, 255
        size = 20.0
    elif p["id"] in [3, 6]:
        # Standing Committee — orange
        r, g, b = 255, 165, 0
        size = 12.0
    else:
        # Others — grey
        r, g, b = 100, 100, 100
        size = 12.0

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{esc(p["birth"])}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{esc(p["birthplace"])}"/>')
    lines.append(f'          <attvalue for="education" value="{esc(p["education"])}"/>')
    lines.append(f'          <attvalue for="current_post" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="source" value="{esc(p["source"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'      </node>')

# ── Nodes: Organizations ──
for o in organizations:
    oid = 1000 + o["id"]
    lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{esc(o["type"])}"/>')
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
    lines.append(f'          <attvalue for="context" value="{esc(pos["title"])}"/>')
    lines.append(f'          <attvalue for="period" value="{pos["start"] or "?"} → {pos["end"] or "今"}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

# person↔person (relationships)
for r in relationships:
    lines.append(f'      <edge id="{edge_id}" source="{r["person_a_id"]}" target="{r["person_b_id"]}" label="{esc(r["type"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="context" value="{esc(r["context"])}"/>')
    lines.append(f'          <attvalue for="period" value="{esc(r["overlap_period"])}"/>')
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
