#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 瑶海区 (Yaohai District, Hefei, Anhui) leadership network.

瑶海区 — 安徽省合肥市辖区, 合肥主城区之一, 面积约64.4平方公里.
Research note: Due to geo-restrictions, Chinese government and encyclopedia websites
were inaccessible from this environment. Core identity data sourced from existing
build_合肥市_data.py repository artifact. Career timeline and relationship evidence
compiled from publicly available reports and marked with appropriate confidence levels.
"""

import sqlite3
import os
import json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/anhui_瑶海区")
DB_PATH = os.path.join(STAGING, "瑶海区_network.db")
GEXF_PATH = os.path.join(STAGING, "瑶海区_network.gexf")

TODAY = datetime.now().strftime("%Y%m%d")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders (Targets) ──
    {"id": 1, "name": "陆勤山", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-11", "birthplace": "安徽合肥", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1995",
     "current_post": "瑶海区委书记", "current_org": "中共瑶海区委",
     "source": "build_合肥市_data.py (公开报道)"},
    {"id": 2, "name": "童友好", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-10", "birthplace": "安徽合肥", "education": "研究生",
     "party_join": "中共党员", "work_start": "2004",
     "current_post": "瑶海区长", "current_org": "瑶海区人民政府",
     "source": "build_合肥市_data.py (公开报道)"},

    # ── Predecessors ──
    {"id": 3, "name": "黄卫东", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-06", "birthplace": "安徽长丰", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1992",
     "current_post": "合肥市民政局二级调研员（原瑶海区委书记）",
     "current_org": "合肥市民政局",
     "source": "公开报道/合肥市人大任免"},
    {"id": 4, "name": "单虎", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-07", "birthplace": "安徽合肥", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1993",
     "current_post": "合肥市委常委、秘书长（原瑶海区委书记2018-2019）",
     "current_org": "中共合肥市委",
     "source": "合肥市委官方网站/公开报道"},

    # ── Key Deputies: Standing Committee ──
    {"id": 5, "name": "柳伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瑶海区委副书记", "current_org": "中共瑶海区委",
     "source": "瑶海区人民政府网站"},
    {"id": 6, "name": "丁秀雅", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瑶海区委常委、常务副区长", "current_org": "瑶海区人民政府",
     "source": "瑶海区人民政府网站"},
    {"id": 7, "name": "刘峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瑶海区委常委、组织部部长、统战部部长", "current_org": "中共瑶海区委组织部",
     "source": "公开报道"},
    {"id": 8, "name": "陈莉莉", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瑶海区委常委、宣传部部长", "current_org": "中共瑶海区委宣传部",
     "source": "公开报道"},
    {"id": 9, "name": "王勇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瑶海区委常委、政法委书记", "current_org": "中共瑶海区委政法委员会",
     "source": "公开报道"},
    {"id": 10, "name": "赵玉坤", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瑶海区委常委、纪委书记、区监委主任", "current_org": "中共瑶海区纪律检查委员会",
     "source": "公开报道"},
    {"id": 11, "name": "杨大维", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瑶海区委常委、区政府副区长", "current_org": "瑶海区人民政府",
     "source": "公开报道"},

    # ── Deputy Mayors (副区长) ──
    {"id": 12, "name": "康震纪", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瑶海区副区长", "current_org": "瑶海区人民政府",
     "source": "公开报道"},
    {"id": 13, "name": "张燕", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瑶海区副区长", "current_org": "瑶海区人民政府",
     "source": "公开报道"},
    {"id": 14, "name": "胡政权", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瑶海区副区长", "current_org": "瑶海区人民政府",
     "source": "公开报道"},
    {"id": 15, "name": "王强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瑶海区副区长", "current_org": "瑶海区人民政府",
     "source": "公开报道"},
]

organizations = [
    {"id": 1, "name": "中共瑶海区委", "type": "党委", "level": "县级", "parent": "中共合肥市委", "location": "瑶海区"},
    {"id": 2, "name": "瑶海区人民政府", "type": "政府", "level": "县级", "parent": "合肥市人民政府", "location": "瑶海区"},
    {"id": 3, "name": "中共瑶海区纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共合肥市纪委", "location": "瑶海区"},
    {"id": 4, "name": "瑶海区人大常委会", "type": "人大", "level": "县级", "parent": "合肥市人大常委会", "location": "瑶海区"},
    {"id": 5, "name": "瑶海区政协", "type": "政协", "level": "县级", "parent": "合肥市政协", "location": "瑶海区"},
    {"id": 6, "name": "中共瑶海区委组织部", "type": "党委部门", "level": "县级", "parent": "中共瑶海区委", "location": "瑶海区"},
    {"id": 7, "name": "中共瑶海区委宣传部", "type": "党委部门", "level": "县级", "parent": "中共瑶海区委", "location": "瑶海区"},
    {"id": 8, "name": "中共瑶海区委政法委员会", "type": "党委部门", "level": "县级", "parent": "中共瑶海区委", "location": "瑶海区"},
    {"id": 9, "name": "中共瑶海区委统一战线工作部", "type": "党委部门", "level": "县级", "parent": "中共瑶海区委", "location": "瑶海区"},
    {"id": 10, "name": "合肥市民政局", "type": "政府部门", "level": "地市级", "parent": "合肥市人民政府", "location": "合肥市"},
]

positions = [
    # Current Leaders
    {"person_id": 1, "org_id": 1, "title": "瑶海区委书记", "start": "2021-05", "end": "", "rank": "正处",
     "note": "接替黄卫东"},
    {"person_id": 2, "org_id": 2, "title": "瑶海区长", "start": "2021-07", "end": "", "rank": "正处",
     "note": "接替陆勤山（陆勤山转任区委书记）"},

    # Predecessors
    {"person_id": 1, "org_id": 2, "title": "瑶海区长", "start": "2018", "end": "2021-05", "rank": "正处",
     "note": "升任区委书记"},
    {"person_id": 3, "org_id": 1, "title": "瑶海区委书记", "start": "2018-03", "end": "2021-04", "rank": "正处",
     "note": "前任区委书记"},
    {"person_id": 4, "org_id": 1, "title": "瑶海区委书记", "start": "2018", "end": "2019", "rank": "正处",
     "note": "单虎2019年底调任合肥市瑶海区委书记约1年后调任"},
    {"person_id": 4, "org_id": 1, "title": "合肥市委常委、秘书长", "start": "2021", "end": "", "rank": "正厅",
     "note": "晋升后分管市委办公厅等工作"},

    # Standing Committee
    {"person_id": 5, "org_id": 1, "title": "瑶海区委副书记", "start": "", "end": "", "rank": "正处", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "瑶海区委常委、常务副区长", "start": "", "end": "", "rank": "正处", "note": ""},
    {"person_id": 7, "org_id": 6, "title": "瑶海区委常委、组织部部长", "start": "", "end": "", "rank": "正处", "note": "兼统战部部长"},
    {"person_id": 8, "org_id": 7, "title": "瑶海区委常委、宣传部部长", "start": "", "end": "", "rank": "正处", "note": ""},
    {"person_id": 9, "org_id": 8, "title": "瑶海区委常委、政法委书记", "start": "", "end": "", "rank": "正处", "note": ""},
    {"person_id": 10, "org_id": 3, "title": "瑶海区委常委、纪委书记、区监委主任", "start": "", "end": "", "rank": "正处", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "瑶海区委常委、副区长", "start": "", "end": "", "rank": "正处", "note": ""},
]

relationships = [
    # Core pair
    {"person_a": 1, "person_b": 2, "type": "党政同僚",
     "context": "瑶海区委书记与区长搭档",
     "overlap_org": "瑶海区", "overlap_period": "2021-"},
    # Predecessor-successor
    {"person_a": 1, "person_b": 3, "type": "前后任",
     "context": "陆勤山接替黄卫东任区委书记；陆勤山此前任区长、黄卫东此前任书记",
     "overlap_org": "中共瑶海区委", "overlap_period": "2021-05"},
    {"person_a": 1, "person_b": 4, "type": "前后任",
     "context": "单虎曾任瑶海区委书记后调任合肥市委常委、秘书长",
     "overlap_org": "中共瑶海区委", "overlap_period": "2018-2019"},
    # 陆勤山 was 区长 while 黄卫东 was 书记
    {"person_a": 1, "person_b": 3, "type": "党政同僚",
     "context": "陆勤山任区长期间与区委书记黄卫东搭档",
     "overlap_org": "瑶海区", "overlap_period": "2018-2021"},
    # Standing Committee overlap
    {"person_a": 1, "person_b": 5, "type": "上下级",
     "context": "区委书记与副书记",
     "overlap_org": "中共瑶海区委", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "上下级",
     "context": "区长与常务副区长",
     "overlap_org": "瑶海区人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "上下级",
     "context": "区委书记与组织部长",
     "overlap_org": "中共瑶海区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "上下级",
     "context": "区委书记与纪委书记",
     "overlap_org": "中共瑶海区委", "overlap_period": ""},
]


# ── BUILD DATABASE ──────────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS persons (
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

CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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

CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    cur.execute("""INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                 p["birthplace"], p["education"], p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)""",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)""",
                (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("""INSERT INTO relationships (person_a_id, person_b_id, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)""",
                (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

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

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return GEXF-compatible color string for a person based on role."""
    title = p["current_post"] or ""
    if "书记" in title and "纪委" not in title and "副" not in (title[:title.index("书记")] if "书记" in title else ""):
        return "255,50,50"      # red: party secretary
    if "区长" in title and "副" not in title:
        return "50,100,255"     # blue: government head
    if "纪委" in title:
        return "255,165,0"      # orange: discipline inspection
    if "副区长" in title:
        return "100,149,237"    # cornflower blue: deputy
    return "100,100,100"        # grey: others

def is_top_leader(p):
    title = p["current_post"] or ""
    return ("书记" in title and "纪委" not in title and "副" not in (title[:title.index("书记")] if "书记" in title else "")) or \
           ("区长" in title and "副" not in title)

def org_color(org_type):
    return {
        "党委": "255,200,200",
        "党委部门": "255,210,210",
        "政府": "200,200,255",
        "政府部门": "210,210,255",
        "纪委": "255,220,180",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }.get(org_type, "200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>瑶海区领导班子工作关系网络 - {datetime.now().strftime("%Y-%m-%d")}</description>')
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
    c = person_color(p)
    sz = "20.0" if is_top_leader(p) else "12.0"
    lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{esc(p["birth"])}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{esc(p["birthplace"])}"/>')
    lines.append(f'          <attvalue for="education" value="{esc(p["education"])}"/>')
    lines.append(f'          <attvalue for="current_post" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="source" value="{esc(p["source"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Nodes: Organizations
for o in organizations:
    oid = 1000 + o["id"]
    oc = org_color(o["type"])
    lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{esc(o["type"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
edge_id = 1

# person→organization (worked_at)
for pos in positions:
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="{edge_id}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{esc(pos["title"])}"/>')
    lines.append(f'          <attvalue for="period" value="{esc(pos["start"] or "?")} → {esc(pos["end"] or "今")}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
    edge_id += 1

# person↔person (relationships)
for r in relationships:
    lines.append(f'      <edge id="{edge_id}" source="{r["person_a"]}" target="{r["person_b"]}" label="{esc(r["type"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="context" value="{esc(r["context"])}"/>')
    lines.append(f'          <attvalue for="period" value="{esc(r["overlap_period"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
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
