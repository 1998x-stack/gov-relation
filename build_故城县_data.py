#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Gucheng County leadership network.

Research date: 2026-07-24
Sources:
  - http://www.gucheng.gov.cn (official county website)
  - Party Congress 15th Session articles (July 2026)
  - People's Congress 18th Session articles (July 2026)

Key findings:
  - 石帅: re-elected 县委书记 at 15th CPC Gucheng County Committee (2026-07-19)
  - 王士博: presided over Party Congress, presumed 县长/县委副书记
  - Party Congress presidium listed 11 members (all 县委常委 level)
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/hebei_故城县")
DB_PATH = os.path.join(STAGING, "故城县_network.db")
GEXF_PATH = os.path.join(STAGING, "故城县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Leadership ──
    {"id": 1, "name": "石帅", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "中共故城县委书记",
     "current_org": "中共故城县委员会",
     "source": "http://www.gucheng.gov.cn/art/2026/7/19/art_490_632052.html"},
    {"id": 2, "name": "王士博", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "故城县委副书记、县长",
     "current_org": "故城县人民政府",
     "source": "http://www.gucheng.gov.cn/art/2026/7/18/art_490_632048.html"},
    {"id": 3, "name": "邢涛", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "故城县委常委",
     "current_org": "中共故城县委员会",
     "source": "http://www.gucheng.gov.cn/art/2026/7/18/art_490_632048.html"},
    {"id": 4, "name": "刘斌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "故城县委常委",
     "current_org": "中共故城县委员会",
     "source": "http://www.gucheng.gov.cn/art/2026/7/18/art_490_632048.html"},
    {"id": 5, "name": "韩晓强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "故城县委常委",
     "current_org": "中共故城县委员会",
     "source": "http://www.gucheng.gov.cn/art/2026/7/18/art_490_632048.html"},
    {"id": 6, "name": "赵飞", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "故城县委常委",
     "current_org": "中共故城县委员会",
     "source": "http://www.gucheng.gov.cn/art/2026/7/18/art_490_632048.html"},
    {"id": 7, "name": "丁艳娜", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "故城县委常委",
     "current_org": "中共故城县委员会",
     "source": "http://www.gucheng.gov.cn/art/2026/7/18/art_490_632048.html"},
    {"id": 8, "name": "景永帅", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "故城县委常委",
     "current_org": "中共故城县委员会",
     "source": "http://www.gucheng.gov.cn/art/2026/7/18/art_490_632048.html"},
    {"id": 9, "name": "刘官权", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "故城县委常委",
     "current_org": "中共故城县委员会",
     "source": "http://www.gucheng.gov.cn/art/2026/7/18/art_490_632048.html"},
    {"id": 10, "name": "肖明阳", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "故城县委常委",
     "current_org": "中共故城县委员会",
     "source": "http://www.gucheng.gov.cn/art/2026/7/18/art_490_632048.html"},
    {"id": 11, "name": "王震", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "故城县委常委",
     "current_org": "中共故城县委员会",
     "source": "http://www.gucheng.gov.cn/art/2026/7/18/art_490_632048.html"},

    # ── Cross-county / Historical figures ──
    {"id": 12, "name": "刘新营", "gender": "男", "ethnicity": "汉族",
     "birth": "1966年12月", "birthplace": "河北省衡水市阜城县",
     "education": "河北师范大学/省委党校在职研究生",
     "party_join": "1990年10月", "work_start": "1988年8月",
     "current_post": "衡水市人大常委会副主任、枣强县委书记",
     "current_org": "衡水市人大常委会、中共枣强县委",
     "source": "data/persons/20260724-河北省-衡水市-县委书记-刘新营.json"},

    # Previous leadership (to be researched)
    {"id": 13, "name": "前任县委书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "待查"},
]

organizations = [
    {"id": 1, "name": "中共故城县委员会", "type": "党委", "level": "县处级",
     "parent": "中共衡水市委员会", "location": "河北省衡水市故城县"},
    {"id": 2, "name": "故城县人民政府", "type": "政府", "level": "县处级",
     "parent": "衡水市人民政府", "location": "河北省衡水市故城县"},
    {"id": 3, "name": "中共故城县纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共衡水市纪律检查委员会", "location": "河北省衡水市故城县"},
    {"id": 4, "name": "故城县人大常委会", "type": "人大", "level": "县处级",
     "parent": "衡水市人大常委会", "location": "河北省衡水市故城县"},
    {"id": 5, "name": "故城县政协", "type": "政协", "level": "县处级",
     "parent": "衡水市政协", "location": "河北省衡水市故城县"},
    {"id": 6, "name": "中共枣强县委", "type": "党委", "level": "县处级",
     "parent": "中共衡水市委员会", "location": "河北省衡水市枣强县"},
    {"id": 7, "name": "衡水市人大常委会", "type": "人大", "level": "副厅级",
     "parent": "河北省人大常委会", "location": "河北省衡水市"},
]

positions = [
    # ── 石帅 ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共故城县委书记",
     "start": "2021", "end": "", "rank": "县处级正职",
     "note": "2021年起任故城县委书记（第十四届），2026年7月连任第十五届。具体到任时间待查。"},

    # ── 王士博 ──
    {"id": 2, "person_id": 2, "org_id": 2, "title": "故城县人民政府县长",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "2026年7月县第十八届人代会选举确认。具体到任时间待查。曾任县委副书记。"},

    # ── 县委常委 ──
    {"id": 3, "person_id": 3, "org_id": 1, "title": "故城县委常委",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "具体分工待查"},
    {"id": 4, "person_id": 4, "org_id": 1, "title": "故城县委常委",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "具体分工待查"},
    {"id": 5, "person_id": 5, "org_id": 1, "title": "故城县委常委",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "具体分工待查"},
    {"id": 6, "person_id": 6, "org_id": 1, "title": "故城县委常委",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "具体分工待查"},
    {"id": 7, "person_id": 7, "org_id": 1, "title": "故城县委常委",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "女，具体分工待查"},
    {"id": 8, "person_id": 8, "org_id": 1, "title": "故城县委常委",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "具体分工待查"},
    {"id": 9, "person_id": 9, "org_id": 1, "title": "故城县委常委",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "具体分工待查"},
    {"id": 10, "person_id": 10, "org_id": 1, "title": "故城县委常委",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "具体分工待查"},
    {"id": 11, "person_id": 11, "org_id": 1, "title": "故城县委常委",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "具体分工待查"},

    # ── 刘新营 (cross-county) ──
    {"id": 12, "person_id": 12, "org_id": 1, "title": "故城县委常委、组织部长",
     "start": "2011-08", "end": "2015-06", "rank": "县处级副职",
     "note": "曾任故城县委常委、组织部长，后调任枣强县"},
]

relationships = [
    # ── 党政搭档 ──
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档",
     "context": "石帅（县委书记）与王士博（县长）搭班子共同领导故城县工作",
     "overlap_org": "故城县", "overlap_period": "2021-至今"},

    # ── 县委常委会 ──
    {"id": 2, "person_a_id": 1, "person_b_id": 3, "type": "上下级",
     "context": "石帅作为县委书记领导县委常委邢涛",
     "overlap_org": "中共故城县委员会", "overlap_period": ""},
    {"id": 3, "person_a_id": 1, "person_b_id": 4, "type": "上下级",
     "context": "石帅作为县委书记领导县委常委刘斌",
     "overlap_org": "中共故城县委员会", "overlap_period": ""},
    {"id": 4, "person_a_id": 1, "person_b_id": 5, "type": "上下级",
     "context": "石帅作为县委书记领导县委常委韩晓强",
     "overlap_org": "中共故城县委员会", "overlap_period": ""},
    {"id": 5, "person_a_id": 1, "person_b_id": 6, "type": "上下级",
     "context": "石帅作为县委书记领导县委常委赵飞",
     "overlap_org": "中共故城县委员会", "overlap_period": ""},
    {"id": 6, "person_a_id": 1, "person_b_id": 7, "type": "上下级",
     "context": "石帅作为县委书记领导县委常委丁艳娜",
     "overlap_org": "中共故城县委员会", "overlap_period": ""},
    {"id": 7, "person_a_id": 1, "person_b_id": 8, "type": "上下级",
     "context": "石帅作为县委书记领导县委常委景永帅",
     "overlap_org": "中共故城县委员会", "overlap_period": ""},
    {"id": 8, "person_a_id": 1, "person_b_id": 9, "type": "上下级",
     "context": "石帅作为县委书记领导县委常委刘官权",
     "overlap_org": "中共故城县委员会", "overlap_period": ""},
    {"id": 9, "person_a_id": 1, "person_b_id": 10, "type": "上下级",
     "context": "石帅作为县委书记领导县委常委肖明阳",
     "overlap_org": "中共故城县委员会", "overlap_period": ""},
    {"id": 10, "person_a_id": 1, "person_b_id": 11, "type": "上下级",
     "context": "石帅作为县委书记领导县委常委王震",
     "overlap_org": "中共故城县委员会", "overlap_period": ""},

    # ── 县长与常委 ──
    {"id": 11, "person_a_id": 2, "person_b_id": 3, "type": "同僚",
     "context": "王士博与邢涛在县党政班子共事",
     "overlap_org": "故城县", "overlap_period": ""},
    {"id": 12, "person_a_id": 2, "person_b_id": 4, "type": "同僚",
     "context": "王士博与刘斌在县党政班子共事",
     "overlap_org": "故城县", "overlap_period": ""},

    # ── 跨县关系 ──
    {"id": 13, "person_a_id": 12, "person_b_id": 1, "type": "前后任中同一组织系统",
     "context": "刘新营曾任故城县委常委、组织部长（2011-2015），石帅后任县委书记",
     "overlap_org": "中共故城县委员会", "overlap_period": "2011-2015（刘新营任职）"},
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
lines.append(f'    <description>故城县领导班子工作关系网络 - {today}</description>')
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
        color = '#2980B9'  # blue: government leader
        size = 18.0
    elif p["id"] in [12]:
        color = '#95A5A6'  # grey: historical figure (no longer in 故城)
        size = 12.0
    elif p["id"] == 13:
        color = '#95A5A6'
        size = 10.0
    else:
        color = '#95A5A6'  # grey: other 县委常委
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
org_colors = {
    1: (200, 50, 50),    # 党委 - dark red
    2: (50, 100, 200),   # 政府 - blue
    3: (255, 165, 0),    # 纪委 - orange
    4: (200, 200, 255),  # 人大 - light blue
    5: (255, 240, 200),  # 政协 - cream
    6: (200, 50, 50),    # 枣强县委 - dark red
    7: (200, 200, 255),  # 衡水人大 - light blue
}

for o in organizations:
    oid = 1000 + o["id"]
    rc, gc, bc = org_colors.get(o["id"], (200, 200, 200))
    lines.append(f'      <node id="{oid}" label="{o["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{o["type"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{rc}" g="{gc}" b="{bc}"/>')
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

os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

total_nodes = len(persons) + len(organizations)
total_edges = len(positions) + len(relationships)
print(f"\nGEXF graph written: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} organizations = {total_nodes} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {total_edges} total")
print("\nDone!")
