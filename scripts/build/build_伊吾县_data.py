#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 伊吾县 (Yiwu County) leadership network.

伊吾县, 新疆维吾尔自治区哈密市辖县.
Current as of: 2026-07 (Baidu Baike, accessed 2026-07-28)
"""

import sqlite3
import os
import sys
from datetime import datetime

# Resolve paths relative to repo root
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
STAGING = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING, "伊吾县_network.db")
GEXF_PATH = os.path.join(STAGING, "伊吾县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders (confirmed from Baidu Baike, as of June 2026) ──
    {"id": 1, "name": "李光泽", "gender": "", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "伊吾县委书记", "current_org": "中共伊吾县委员会",
     "source": "https://baike.baidu.com/item/伊吾县"},
    {"id": 2, "name": "沙吾列别克·阿汉", "gender": "男", "ethnicity": "哈萨克族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "伊吾县委副书记、县长", "current_org": "伊吾县人民政府",
     "source": "https://baike.baidu.com/item/伊吾县"},

    # ── County Congress and CPPCC Leaders ──
    {"id": 3, "name": "伊力哈木·艾力", "gender": "", "ethnicity": "维吾尔族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "伊吾县人大常委会主任", "current_org": "伊吾县人民代表大会常务委员会",
     "source": "https://baike.baidu.com/item/伊吾县"},
    {"id": 4, "name": "依明尼亚孜·玉努斯", "gender": "", "ethnicity": "维吾尔族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "伊吾县政协主席", "current_org": "中国人民政治协商会议伊吾县委员会",
     "source": "https://baike.baidu.com/item/伊吾县"},

    # ── Standing Committee (常委班子, names unconfirmed from public sources) ──
    {"id": 5, "name": "待查-常务副县长", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "伊吾县委常委、常务副县长", "current_org": "伊吾县人民政府",
     "source": ""},
    {"id": 6, "name": "待查_纪委书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "伊吾县委常委、纪委书记、监委主任", "current_org": "中共伊吾县纪律检查委员会",
     "source": ""},
    {"id": 7, "name": "待查_组织部长", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "伊吾县委常委、组织部部长", "current_org": "中共伊吾县委员会",
     "source": ""},
    {"id": 8, "name": "待查_宣传部长", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "伊吾县委常委、宣传部部长", "current_org": "中共伊吾县委员会",
     "source": ""},
    {"id": 9, "name": "待查_统战部长", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "伊吾县委常委、统战部部长", "current_org": "中共伊吾县委员会",
     "source": ""},
    {"id": 10, "name": "待查_政法书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "伊吾县委常委、政法委书记", "current_org": "中共伊吾县委员会",
     "source": ""},

    # ── Historical Predecessors (from open-source records) ──
    {"id": 11, "name": "彭刚", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原伊吾县委书记", "current_org": "",
     "source": ""},
    {"id": 12, "name": "斯坎旦·克尤木", "gender": "男", "ethnicity": "维吾尔族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原伊吾县县长", "current_org": "",
     "source": ""},
]

organizations = [
    {"id": 1, "name": "中共伊吾县委员会", "type": "党委", "level": "县处级", "parent": "中共哈密市委员会",
     "location": "新疆哈密伊吾"},
    {"id": 2, "name": "伊吾县人民政府", "type": "政府", "level": "县处级", "parent": "哈密市人民政府",
     "location": "新疆哈密伊吾"},
    {"id": 3, "name": "中共伊吾县纪律检查委员会", "type": "纪检", "level": "县处级", "parent": "中共哈密市纪律检查委员会",
     "location": "新疆哈密伊吾"},
    {"id": 4, "name": "伊吾县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "哈密市人民代表大会常务委员会",
     "location": "新疆哈密伊吾"},
    {"id": 5, "name": "中国人民政治协商会议伊吾县委员会", "type": "政协", "level": "县处级", "parent": "政协哈密市委员会",
     "location": "新疆哈密伊吾"},
    {"id": 6, "name": "中共哈密市委员会", "type": "党委", "level": "地厅级", "parent": "中共新疆维吾尔自治区委员会",
     "location": "新疆哈密"},
    {"id": 7, "name": "哈密市人民政府", "type": "政府", "level": "地厅级", "parent": "新疆维吾尔自治区人民政府",
     "location": "新疆哈密"},
]

positions = [
    {"id": 1, "person_id": 1, "org_id": 1, "title": "伊吾县委书记",
     "start": "", "end": "present", "rank": "县处级正职",
     "note": "现任。公开信息显示2024-2025年间任职"},
    {"id": 2, "person_id": 1, "org_id": 1, "title": "伊吾县委副书记",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "兼任县委书记"},
    {"id": 3, "person_id": 2, "org_id": 2, "title": "伊吾县委副书记、县长",
     "start": "", "end": "present", "rank": "县处级正职",
     "note": "哈萨克族干部，现任"},
    {"id": 4, "person_id": 2, "org_id": 1, "title": "伊吾县委常委",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "兼任县长"},
    {"id": 5, "person_id": 3, "org_id": 4, "title": "伊吾县人大常委会主任",
     "start": "", "end": "present", "rank": "县处级正职",
     "note": ""},
    {"id": 6, "person_id": 4, "org_id": 5, "title": "伊吾县政协主席",
     "start": "", "end": "present", "rank": "县处级正职",
     "note": ""},
    {"id": 7, "person_id": 5, "org_id": 2, "title": "伊吾县委常委、常务副县长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "人员姓名待确认"},
    {"id": 8, "person_id": 6, "org_id": 3, "title": "伊吾县委常委、纪委书记、监委主任",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "人员姓名待确认"},
    {"id": 9, "person_id": 7, "org_id": 1, "title": "伊吾县委常委、组织部部长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "人员姓名待确认"},
    {"id": 10, "person_id": 8, "org_id": 1, "title": "伊吾县委常委、宣传部部长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "人员姓名待确认"},
    {"id": 11, "person_id": 9, "org_id": 1, "title": "伊吾县委常委、统战部部长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "人员姓名待确认"},
    {"id": 12, "person_id": 10, "org_id": 1, "title": "伊吾县委常委、政法委书记",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "人员姓名待确认"},
    {"id": 13, "person_id": 11, "org_id": 1, "title": "伊吾县委书记",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "前任县委书记"},
    {"id": 14, "person_id": 12, "org_id": 2, "title": "伊吾县县长",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "前任县长，维吾尔族"},
]

relationships = [
    {"id": 1, "person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "李光泽任伊吾县委书记，沙吾列别克·阿汉任县长",
     "overlap_org": "伊吾县人民政府", "overlap_period": ""},
    {"id": 2, "person_a": 3, "person_b": 1, "type": "同僚",
     "context": "伊吾县人大常委会主任与县委书记",
     "overlap_org": "中共伊吾县委员会", "overlap_period": ""},
    {"id": 3, "person_a": 4, "person_b": 1, "type": "同僚",
     "context": "伊吾县政协主席与县委书记",
     "overlap_org": "中共伊吾县委员会", "overlap_period": ""},
]


# ── BUILD SQLite DATABASE ────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.executescript("""
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
        source TEXT DEFAULT ''
    );

    CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT DEFAULT '',
        level TEXT DEFAULT '',
        parent TEXT DEFAULT '',
        location TEXT DEFAULT ''
    );

    CREATE TABLE positions (
        id INTEGER PRIMARY KEY,
        person_id INTEGER NOT NULL,
        org_id INTEGER NOT NULL,
        title TEXT DEFAULT '',
        start TEXT DEFAULT '',
        end TEXT DEFAULT '',
        rank TEXT DEFAULT '',
        note TEXT DEFAULT '',
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );

    CREATE TABLE relationships (
        id INTEGER PRIMARY KEY,
        person_a INTEGER NOT NULL,
        person_b INTEGER NOT NULL,
        type TEXT DEFAULT '',
        context TEXT DEFAULT '',
        overlap_org TEXT DEFAULT '',
        overlap_period TEXT DEFAULT '',
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    );
""")

for p in persons:
    c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
              (p["id"], p["name"], p.get("gender",""), p.get("ethnicity",""),
               p.get("birth",""), p.get("birthplace",""), p.get("education",""),
               p.get("party_join",""), p.get("work_start",""),
               p.get("current_post",""), p.get("current_org",""), p.get("source","")))

for o in organizations:
    c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
              (o["id"], o["name"], o.get("type",""), o.get("level",""),
               o.get("parent",""), o.get("location","")))

for pos in positions:
    c.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)""",
              (pos["id"], pos["person_id"], pos["org_id"], pos.get("title",""),
               pos.get("start",""), pos.get("end",""), pos.get("rank",""), pos.get("note","")))

for r in relationships:
    c.execute("""INSERT INTO relationships VALUES (?,?,?,?,?,?,?)""",
              (r["id"], r["person_a"], r["person_b"], r.get("type",""),
               r.get("context",""), r.get("overlap_org",""), r.get("overlap_period","")))

conn.commit()
conn.close()

print(f"  SQLite DB: {DB_PATH}")
print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


# ── BUILD GEXF GRAPH ─────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    title = p.get("current_post", "")
    if "县委书记" in title:
        return "255,50,50"
    if "县长" in title:
        return "50,100,255"
    if "纪委" in title:
        return "255,165,0"
    if "常务" in title:
        return "50,100,255"
    if "主任" in title:
        return "200,255,255"
    if "政协" in title:
        return "255,240,200"
    return "100,100,100"

def org_color(o):
    t = o.get("type", "")
    colors = {"党委": "255,200,200", "政府": "200,200,255", "纪检": "255,165,0",
              "人大": "200,255,255", "政协": "255,240,200"}
    return colors.get(t, "200,200,200")

def node_size(p):
    title = p.get("current_post", "")
    if any(k in title for k in ["县委书记", "县长", "主任", "政协主席"]):
        return "20.0"
    return "12.0"

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>gov-relation research agent</creator>')
lines.append('    <description>伊吾县领导班子工作关系网络</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="organization" type="string"/>')
lines.append('      <attribute id="3" title="ethnicity" type="string"/>')
lines.append('      <attribute id="4" title="source" type="string"/>')
lines.append('    </attributes>')

lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
lines.append('    </attributes>')

lines.append('    <nodes>')
for p in persons:
    c = person_color(p)
    sz = node_size(p)
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(p.get("ethnicity",""))}"/>')
    lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

for o in organizations:
    c = org_color(o)
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append('          <attvalue for="1" value="机构"/>')
    lines.append(f'          <attvalue for="2" value="{esc(o["name"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

lines.append('    <edges>')
eid = 0

for pos in positions:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

for r in relationships:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org",""))}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period",""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"  GEXF graph: {GEXF_PATH}")

print(f"\n=== 伊吾县 Leadership Network Summary ===")
print(f"  Persons: {len(persons)}")
print(f"  Organizations: {len(organizations)}")
print(f"  Positions: {len(positions)}")
print(f"  Relationships: {len(relationships)}")
print("Done.")