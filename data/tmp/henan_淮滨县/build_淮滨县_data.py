#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Huaibin County leadership network."""

import sqlite3
import os
from datetime import datetime

# Script lives at data/tmp/henan_淮滨县/build_淮滨县_data.py
# Need to go up 4 levels to reach repo root (/workspace/data/xieming/other-codes/gov-relation)
TMPDIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DB_PATH = os.path.join(TMPDIR, "淮滨县_network.db")
GEXF_PATH = os.path.join(TMPDIR, "淮滨县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Huaibin County Leadership ──
    {"id": 1, "name": "朱志勇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "中共淮滨县委书记", "current_org": "中共淮滨县委员会",
     "source": "https://www.huaibin.gov.cn/2026/07-23/795843.html"},
    {"id": 2, "name": "王璠", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-11", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "淮滨县委副书记、县政府党组书记、县长", "current_org": "淮滨县人民政府",
     "source": "https://www.huaibin.gov.cn/2026/01-09/747450.html"},
    {"id": 3, "name": "陈严", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-11", "birthplace": "", "education": "硕士研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "淮滨县委常委、常务副县长", "current_org": "淮滨县人民政府",
     "source": "https://www.huaibin.gov.cn/2026/01-09/747459.html"},
    {"id": 4, "name": "陈洋", "gender": "男", "ethnicity": "汉族",
     "birth": "1988-09", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "淮滨县委常委、宣传部部长、副县长", "current_org": "淮滨县委宣传部",
     "source": "https://www.huaibin.gov.cn/2026/06-25/791780.html"},
    {"id": 5, "name": "程涛", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-05", "birthplace": "", "education": "硕士研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "淮滨县委常委、统战部长", "current_org": "淮滨县委统战部",
     "source": "https://www.huaibin.gov.cn/2026/01-05/747480.html"},
    {"id": 6, "name": "何海雁", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-04", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "淮滨县副县长、县公安局局长", "current_org": "淮滨县人民政府",
     "source": "https://www.huaibin.gov.cn/2026/01-05/747494.html"},
    {"id": 7, "name": "何雨楠", "gender": "男", "ethnicity": "汉族",
     "birth": "1985-10", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "淮滨县副县长", "current_org": "淮滨县人民政府",
     "source": "https://www.huaibin.gov.cn/2026/01-05/747483.html"},
    {"id": 8, "name": "张成友", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-08", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "淮滨县副县长", "current_org": "淮滨县人民政府",
     "source": "https://www.huaibin.gov.cn/2026/06-24/791618.html"},
]

organizations = [
    {"id": 1, "name": "中共淮滨县委员会", "type": "党委", "level": "县处级", "parent": "中共信阳市委员会", "location": "河南信阳淮滨"},
    {"id": 2, "name": "淮滨县人民政府", "type": "政府", "level": "县处级", "parent": "信阳市人民政府", "location": "河南信阳淮滨"},
    {"id": 3, "name": "中共淮滨县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共信阳市纪律检查委员会", "location": "河南信阳淮滨"},
    {"id": 4, "name": "淮滨县委宣传部", "type": "党委部门", "level": "县处级", "parent": "中共淮滨县委员会", "location": "河南信阳淮滨"},
    {"id": 5, "name": "淮滨县委统战部", "type": "党委部门", "level": "县处级", "parent": "中共淮滨县委员会", "location": "河南信阳淮滨"},
    {"id": 6, "name": "淮滨县公安局", "type": "政府", "level": "县处级", "parent": "淮滨县人民政府", "location": "河南信阳淮滨"},
]

positions = [
    # ── Zhu Zhiyong (朱志勇) ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共淮滨县委书记", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},

    # ── Wang Fan (王璠) ──
    {"id": 2, "person_id": 2, "org_id": 2, "title": "淮滨县人民政府县长", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},
    {"id": 3, "person_id": 2, "org_id": 1, "title": "淮滨县委副书记", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Chen Yan (陈严) ──
    {"id": 4, "person_id": 3, "org_id": 2, "title": "淮滨县委常委、常务副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Chen Yang (陈洋) ──
    {"id": 5, "person_id": 4, "org_id": 4, "title": "淮滨县委常委、宣传部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 6, "person_id": 4, "org_id": 2, "title": "淮滨县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Cheng Tao (程涛) ──
    {"id": 7, "person_id": 5, "org_id": 5, "title": "淮滨县委常委、统战部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── He Haiyan (何海雁) ──
    {"id": 8, "person_id": 6, "org_id": 2, "title": "淮滨县副县长、县公安局局长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 9, "person_id": 6, "org_id": 6, "title": "淮滨县公安局局长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── He Yunan (何雨楠) ──
    {"id": 10, "person_id": 7, "org_id": 2, "title": "淮滨县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Zhang Chengyou (张成友) ──
    {"id": 11, "person_id": 8, "org_id": 2, "title": "淮滨县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
]

relationships = [
    # ── Party Secretary ↔ County Mayor ──
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档", "context": "朱志勇任淮滨县委书记，王璠任淮滨县委副书记、县长", "overlap_org": "中共淮滨县委员会", "overlap_period": ""},

    # ── Colleagues within the Standing Committee ──
    {"id": 2, "person_a_id": 3, "person_b_id": 4, "type": "同僚", "context": "陈严与陈洋均为淮滨县委常委", "overlap_org": "中共淮滨县委员会", "overlap_period": ""},
    {"id": 3, "person_a_id": 5, "person_b_id": 3, "type": "同僚", "context": "程涛与陈严均为淮滨县委常委", "overlap_org": "中共淮滨县委员会", "overlap_period": ""},

    # ── County Government colleagues ──
    {"id": 4, "person_a_id": 6, "person_b_id": 8, "type": "同僚", "context": "何海雁与张成友均为淮滨县政府班子成员", "overlap_org": "淮滨县人民政府", "overlap_period": ""},

    # ── Superior-subordinate ──
    {"id": 5, "person_a_id": 2, "person_b_id": 3, "type": "上下级", "context": "王璠任县长，陈严任常务副县长", "overlap_org": "淮滨县人民政府", "overlap_period": ""},
    {"id": 6, "person_a_id": 2, "person_b_id": 6, "type": "上下级", "context": "王璠任县长，何海雁任副县长兼公安局长", "overlap_org": "淮滨县人民政府", "overlap_period": ""},
]


# ── BUILD SQLite DATABASE ────────────────────────────────────────────

os.makedirs(TMPDIR, exist_ok=True)
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
lines.append(f'    <description>淮滨县领导班子工作关系网络 - {today}</description>')
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
    if p["id"] == 1:
        color = '#E03C31'  # red: Party Secretary
        size = 20.0
    elif p["id"] == 2:
        color = '#2980B9'  # blue: government leader (county mayor)
        size = 18.0
    else:
        color = '#95A5A6'  # grey: others
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
    lines.append(f'        <viz:color r="{int(color[1:3], 16)}" g="{int(color[3:5], 16)}" b="{int(color[5:7], 16)}"/>')
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
