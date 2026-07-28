#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 阿坝县 (Aba County, Sichuan) leadership network."""

import sqlite3
import os
from datetime import datetime

STAGING = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(STAGING))
DB_PATH = os.path.join(STAGING, "阿坝县_network.db")
GEXF_PATH = os.path.join(STAGING, "阿坝县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Top Leaders: Party Secretary & County Mayor ──
    {"id": 1, "name": "王甲", "gender": "男", "ethnicity": "藏族",
     "birth": "1982-02", "birthplace": "四川阿坝", "education": "在职大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共阿坝县委书记", "current_org": "中共阿坝县委员会",
     "source": "https://www.abaxian.gov.cn/abxrmzf/c100050/202607/8423a63d38e34f4aa6a4ce44f848843c.shtml"},
    {"id": 2, "name": "王子亮", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阿坝县委副书记、县长", "current_org": "阿坝县人民政府",
     "source": "https://www.abaxian.gov.cn/abxrmzf/c100050/202607/8423a63d38e28b4aa6a4ce44f848843c.shtml"},

    # ── Deputy Party Secretaries ──
    {"id": 3, "name": "罗尔特", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阿坝县委副书记", "current_org": "中共阿坝县委员会",
     "source": "https://www.abaxian.gov.cn/abxrmzf/c100050/202607/8423a63d38e28b4aa6a4ce44f848843c.shtml"},
    {"id": 4, "name": "刘朝军", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阿坝县委副书记", "current_org": "中共阿坝县委员会",
     "source": "https://www.abaxian.gov.cn/abxrmzf/c100050/202607/8423a63d38e28b4aa6a4ce44f848843c.shtml"},

    # ── County Party Standing Committee / Leadership ──
    {"id": 5, "name": "曾付康", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阿坝县委常委、县人武部上校政治委员", "current_org": "阿坝县人民武装部",
     "source": "https://www.abaxian.gov.cn/abxrmzf/c100050/202607/94ac4a5890894189941002de134c35e8.shtml"},
    {"id": 6, "name": "倪长龙", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阿坝县人武部部长", "current_org": "阿坝县人民武装部",
     "source": "https://www.abaxian.gov.cn/abxrmzf/c100050/202607/94ac4a5890894189941002de134c35e8.shtml"},
    {"id": 7, "name": "刘利增", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阿坝县副县长", "current_org": "阿坝县人民政府",
     "source": "https://www.abaxian.gov.cn/abxrmzf/c100050/202607/94ac4a5890894189941002de134c35e8.shtml"},

    # ── Former Party Secretaries (Predecessors) ──
    {"id": 8, "name": "陈宝华", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阿坝州政府一级巡视员（原阿坝县委书记）", "current_org": "阿坝州人民政府",
     "source": "https://www.abazhou.gov.cn/"},
    {"id": 9, "name": "苏均", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阿坝州政协副主席（原阿坝县委书记）", "current_org": "阿坝州政协",
     "source": "https://baike.baidu.com/item/%E8%8B%8F%E5%9D%87"},

    # ── Former County Mayor (Predecessor) ──
    {"id": 10, "name": "龙真泽郎", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阿坝州（另有任用）", "current_org": "",
     "source": "https://www.abaxian.gov.cn/"},
]

organizations = [
    {"id": 1, "name": "中共阿坝县委员会", "type": "党委", "level": "县处级", "parent": "中共阿坝州委员会", "location": "四川阿坝州阿坝县"},
    {"id": 2, "name": "阿坝县人民政府", "type": "政府", "level": "县处级", "parent": "阿坝州人民政府", "location": "四川阿坝州阿坝县"},
    {"id": 3, "name": "阿坝县人民武装部", "type": "军事", "level": "县处级", "parent": "阿坝州军分区", "location": "四川阿坝州阿坝县"},
    {"id": 4, "name": "阿坝县人大常委会", "type": "人大", "level": "县处级", "parent": "阿坝州人大常委会", "location": "四川阿坝州阿坝县"},
    {"id": 5, "name": "阿坝县政协", "type": "政协", "level": "县处级", "parent": "阿坝州政协", "location": "四川阿坝州阿坝县"},
    {"id": 6, "name": "阿坝州人民政府", "type": "政府", "level": "地厅级", "parent": "四川省人民政府", "location": "四川马尔康"},
    {"id": 7, "name": "阿坝州政协", "type": "政协", "level": "地厅级", "parent": "四川省政协", "location": "四川马尔康"},
]

positions = [
    # ── Wang Jia (王甲) career ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共阿坝县委书记", "start": "", "end": "", "rank": "县处级正职", "note": "现任，藏族干部，1982年2月出生"},
    {"id": 2, "person_id": 1, "org_id": 1, "title": "阿坝县委副书记", "start": "", "end": "", "rank": "县处级副职", "note": "升任书记前曾任副书记"},

    # ── 王子亮 (Wang Ziliang) career ──
    {"id": 3, "person_id": 2, "org_id": 2, "title": "阿坝县委副书记、县长", "start": "", "end": "", "rank": "县处级正职", "note": "现任县长"},

    # ── Deputy Secretaries ──
    {"id": 4, "person_id": 3, "org_id": 1, "title": "阿坝县委副书记", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 5, "person_id": 4, "org_id": 1, "title": "阿坝县委副书记", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Zeng Fukang ──
    {"id": 6, "person_id": 5, "org_id": 3, "title": "阿坝县委常委、县人武部上校政治委员", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 7, "person_id": 5, "org_id": 1, "title": "阿坝县委常委", "start": "", "end": "", "rank": "县处级副职", "note": "县委常委会成员"},

    # ── Ni Changlong ──
    {"id": 8, "person_id": 6, "org_id": 3, "title": "阿坝县人武部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Liu Lizeng ──
    {"id": 9, "person_id": 7, "org_id": 2, "title": "阿坝县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Chen Baohua ── 原县委书记
    {"id": 10, "person_id": 8, "org_id": 1, "title": "中共阿坝县委书记", "start": "", "end": "", "rank": "县处级正职", "note": "前任县委书记"},
    {"id": 11, "person_id": 8, "org_id": 6, "title": "阿坝州委一级巡视员", "start": "", "end": "", "rank": "副厅级", "note": "现任"},

    # ── Su Jun (苏均) ──
    {"id": 12, "person_id": 9, "org_id": 1, "title": "中共阿坝县委书记", "start": "", "end": "", "rank": "县处级正职", "note": "更早前任县委书记"},
    {"id": 13, "person_id": 9, "org_id": 7, "title": "阿坝州政协副主席", "start": "", "end": "", "rank": "副厅级", "note": "现任"},

    # ── Long Wei Zelang (龙卫泽郎) ──
    {"id": 14, "person_id": 10, "org_id": 2, "title": "阿坝县委副书记、县长", "start": "", "end": "", "rank": "县处级正职", "note": "前任县长，已调离"},
]

relationships = [
    # ── Party Secretary ↔ County Mayor (current leadership duo) ──
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档", "context": "王甲（县委书记）与王子亮（县长）为现任党政主要领导搭档", "overlap_org": "中共阿坝县委员会/阿坝县人民政府", "overlap_period": "当前"},

    # ── Predecessor-Successor: Party Secretary ──
    {"id": 2, "person_a_id": 8, "person_b_id": 1, "type": "交接", "context": "陈宝华→王甲 阿坝县委书记交接", "overlap_org": "中共阿坝县委员会", "overlap_period": ""},
    {"id": 3, "person_a_id": 9, "person_b_id": 8, "type": "交接", "context": "苏均→陈宝华 阿坝县委书记交接", "overlap_org": "中共阿坝县委员会", "overlap_period": ""},

    # ── Predecessor-Successor: County Mayor ──
    {"id": 4, "person_a_id": 10, "person_b_id": 2, "type": "交接", "context": "龙卫泽郎→王子亮 阿坝县长交接（王子亮接任）", "overlap_org": "阿坝县人民政府", "overlap_period": ""},

    # ── Current Standing Committee ──
    {"id": 5, "person_a_id": 3, "person_b_id": 4, "type": "同僚", "context": "罗尔特与刘朝军同为阿坝县委副书记", "overlap_org": "中共阿坝县委员会", "overlap_period": ""},
    {"id": 6, "person_a_id": 5, "person_b_id": 6, "type": "同僚", "context": "曾付康（县委常委/人武部政委）与倪长龙（人武部部长）为人武部同事", "overlap_org": "阿坝县人民武装部", "overlap_period": ""},

    # ── Wang Jia seeing Liu Lize ──
    {"id": 7, "person_a_id": 1, "person_b_id": 7, "type": "上下级", "context": "王甲（县委书记）与刘利增（副县长）为上下级关系", "overlap_org": "中共阿坝县委员会/阿坝县人民政府", "overlap_period": ""},
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

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>阿坝县领导班子工作关系网络 - {today}</description>')
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
        color = (255, 50, 50)   # red: Party Secretary
        size = 20.0
    elif p["id"] == 2:
        color = (50, 100, 255)  # blue: government leader (mayor)
        size = 20.0
    elif p["id"] in [3, 4]:
        color = (100, 100, 100) # grey: deputy secretary
        size = 12.0
    elif p["id"] in [8, 9]:
        color = (100, 100, 100) # grey: predecessor officials
        size = 16.0
    elif p["id"] == 10:
        color = (50, 100, 255)  # blue: former mayor
        size = 16.0
    else:
        color = (100, 100, 100) # grey: others
        size = 12.0

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
    lines.append(f'        <viz:color r="{color[0]}" g="{color[1]}" b="{color[2]}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'      </node>')

# ── Nodes: Organizations ──
org_colors = {
    "党委": (255, 200, 200),
    "政府": (200, 200, 255),
    "军事": (220, 220, 220),
    "人大": (200, 255, 255),
    "政协": (255, 240, 200),
}
for o in organizations:
    oid = 1000 + o["id"]
    oc = org_colors.get(o["type"], (200, 200, 200))
    lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{esc(o["type"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{oc[0]}" g="{oc[1]}" b="{oc[2]}"/>')
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