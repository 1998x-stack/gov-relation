#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 东乡区 (抚州市, 江西省) leadership network.

Data sourced from existing repository artifacts (build_fuzhou_data.py), public Chinese
government websites, and news reports. Where information is incomplete, it is marked
with explicit confidence levels.

东乡区概况: 东乡区是江西省抚州市下辖的市辖区, 2016年由东乡县撤县设区。
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/jiangxi_东乡区")
DB_PATH = os.path.join(STAGING, "东乡区_network.db")
GEXF_PATH = os.path.join(STAGING, "东乡区_network.gexf")

os.makedirs(STAGING, exist_ok=True)

# =========================================================================
# DATA
# =========================================================================

persons = [
    # ── Current Party Secretary ──
    {
        "id": 1,
        "name": "彭敏群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",           # 待查
        "birthplace": "",      # 待查
        "education": "",       # 待查
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "东乡区委书记",
        "current_org": "中共抚州市东乡区委员会",
        "source": "https://www.jxfz.gov.cn — 抚州市政府网站 (via build_fuzhou_data.py)"
    },

    # ── Current District Mayor (区长) [NAME TO BE CONFIRMED] ──
    {
        "id": 2,
        "name": "【待查】",     # 2026年7月的东乡区区长姓名待核实
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "东乡区区长",
        "current_org": "东乡区人民政府",
        "source": "信息待查 — 需要从东乡区政府网站或抚州市任前公示核实"
    },

    # ── City-level leaders (抚州市) overseeing 东乡区 ──
    {
        "id": 3,
        "name": "范小林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-12",
        "birthplace": "江西宜丰",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "抚州市委书记",
        "current_org": "中共抚州市委员会",
        "source": "https://www.thepaper.cn/newsDetail_forward_29115114"
    },
    {
        "id": 4,
        "name": "胡剑飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",           # 待查
        "birthplace": "",      # 待查
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "抚州市委副书记、市长",
        "current_org": "抚州市人民政府",
        "source": "https://www.jxfz.gov.cn — 抚州市政府网站 (2026年7月确认)"
    },
    {
        "id": 5,
        "name": "彭银贵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "抚州市委常委、政法委书记",
        "current_org": "中共抚州市委政法委员会",
        "source": "https://www.jxfz.gov.cn"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共抚州市东乡区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共抚州市委员会",
        "location": "江西省抚州市东乡区"
    },
    {
        "id": 2,
        "name": "东乡区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "抚州市人民政府",
        "location": "江西省抚州市东乡区"
    },
    {
        "id": 3,
        "name": "中共抚州市委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中共江西省委",
        "location": "江西省抚州市"
    },
    {
        "id": 4,
        "name": "抚州市人民政府",
        "type": "政府",
        "level": "地级",
        "parent": "江西省人民政府",
        "location": "江西省抚州市"
    },
    {
        "id": 5,
        "name": "中共抚州市委政法委员会",
        "type": "党委部门",
        "level": "县处级",
        "parent": "中共抚州市委员会",
        "location": "江西省抚州市"
    },
]

positions = [
    # 彭敏群
    {"id": 1, "person_id": 1, "org_id": 1, "title": "东乡区委书记",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "现任 — 具体任职起始时间待查；根据 build_fuzhou_data.py 确认"},  # noqa: E501

    # 【待查】区长
    {"id": 2, "person_id": 2, "org_id": 2, "title": "东乡区区长",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "现任 — 姓名和具体信息待核实"},

    # 范小林 — 抚州市委书记
    {"id": 3, "person_id": 3, "org_id": 3, "title": "抚州市委书记",
     "start": "2024-10", "end": "", "rank": "正厅级",
     "note": "2024年10月省委任命"},

    # 胡剑飞 — 抚州市长
    {"id": 4, "person_id": 4, "org_id": 4, "title": "抚州市委副书记、市长",
     "start": "", "end": "", "rank": "正厅级",
     "note": "2026年7月确认在职"},

    # 彭银贵 — 政法委书记
    {"id": 5, "person_id": 5, "org_id": 5, "title": "抚州市委常委、政法委书记",
     "start": "", "end": "", "rank": "副厅级",
     "note": ""},
]

relationships = [
    # 区委书记 ↔ 区长 (党政搭档)
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档",
     "context": "彭敏群（区委书记）与东乡区区长（姓名待核实）为党政一把手关系",
     "overlap_org": "东乡区",
     "overlap_period": ""},

    # 范小林 ↔ 彭敏群 (上下级: 市委书记—区委书记)
    {"id": 2, "person_a_id": 3, "person_b_id": 1, "type": "上下级",
     "context": "范小林（抚州市委书记）直接领导东乡区委书记彭敏群",
     "overlap_org": "抚州市",
     "overlap_period": "2024-10至今"},

    # 胡剑飞 ↔ 东乡区区长 (上下级: 市长—区长)
    {"id": 3, "person_a_id": 4, "person_b_id": 2, "type": "上下级",
     "context": "胡剑飞（抚州市长）与东乡区区长（姓名待核实）为政府系统上下级关系",
     "overlap_org": "抚州市",
     "overlap_period": ""},
]

# =========================================================================
# BUILD SQLite DATABASE
# =========================================================================

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

# =========================================================================
# BUILD GEXF GRAPH
# =========================================================================

today = datetime.now().strftime("%Y-%m-%d")


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    post = p.get("current_post", "") or ""
    if "区委书记" in post:
        return (255, 50, 50)     # Red — Party Secretary
    if "区长" in post and "副" not in post:
        return (50, 100, 255)    # Blue — Gov Leader
    if "市委书记" in post:
        return (255, 50, 50)     # Red — Prefecture Party Secretary
    if "市长" in post and "副" not in post:
        return (50, 100, 255)    # Blue — Prefecture Mayor
    if "政法委" in post:
        return (150, 200, 230)
    return (100, 100, 100)


def person_size(p):
    """Top leaders larger."""
    if p["id"] in [1, 2, 3, 4]:
        return 20.0
    return 12.0


def org_color(o):
    colors = {
        "党委": (255, 200, 200),    # Pink
        "政府": (200, 200, 255),    # Light blue
        "党委部门": (255, 200, 200),  # Pink
    }
    return colors.get(o["type"], (200, 200, 200))


lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append('    <description>江西省抚州市东乡区领导班子工作关系网络 - 2026年7月15日生成</description>')
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
    r, g, b = person_color(p)
    sz = person_size(p)
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
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append(f'      </node>')

# ── Nodes: Organizations ──
for o in organizations:
    oid = 1000 + o["id"]
    r, g, b = org_color(o)
    lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{esc(o["type"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
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
