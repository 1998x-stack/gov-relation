#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 隰县 leadership network.

Due to degraded web access (Baidu 403, Exa rate-limited, government sites
unreachable), some data is partial. See open_questions in person JSON files
and report/20260726-山西省-临汾市-隰县-领导班子工作关系网络调查报告.md.
"""

import sqlite3
import os
import json
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DB_PATH = os.path.join(BASE, "data/tmp/shanxi_隰县/隰县_network.db")
GEXF_PATH = os.path.join(BASE, "data/tmp/shanxi_隰县/隰县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Party Secretary (县委书记) ──
    # Current 县委书记 of 隰县 — name unconfirmed due to web access failure.
    # See open_gaps.md for current status.
    # Known predecessor patterns: often appointed from 临汾市委 or neighboring counties.
    {"id": 1, "name": "（现任县委书记）待查", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "山西省", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "中共隰县县委书记", "current_org": "中共隰县委员会",
     "source": ""},

    # ── County Mayor (县长) ──
    {"id": 2, "name": "（现任县长）待查", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "山西省", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "隰县人民政府县长", "current_org": "隰县人民政府",
     "source": ""},

    # ── Notable figure from 隰县 ──
    {"id": 3, "name": "郭灵计", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-07", "birthplace": "山西隰县", "education": "中央党校研究生，公共管理硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湖南省委组织部部长", "current_org": "中共湖南省委组织部",
     "source": "https://baike.baidu.com/item/%E9%83%AD%E7%81%B5%E8%AE%A1"},

    # ── Key Standing Committee roles (standard county-level positions) ──
    {"id": 4, "name": "（县委副书记）待查", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "隰县县委副书记", "current_org": "中共隰县委员会",
     "source": ""},

    {"id": 5, "name": "（常务副县长）待查", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "隰县县委常委、常务副县长", "current_org": "隰县人民政府",
     "source": ""},

    {"id": 6, "name": "（纪委书记）待查", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "隰县县委常委、县纪委书记、县监委主任", "current_org": "中共隰县纪律检查委员会",
     "source": ""},

    {"id": 7, "name": "（组织部部长）待查", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "隰县县委常委、组织部部长", "current_org": "中共隰县委员会组织部",
     "source": ""},

    {"id": 8, "name": "（宣传部部长）待查", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "隰县县委常委、宣传部部长", "current_org": "中共隰县委员会宣传部",
     "source": ""},

    {"id": 9, "name": "（政法委书记）待查", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "隰县县委常委、政法委书记", "current_org": "中共隰县委员会政法委员会",
     "source": ""},

    {"id": 10, "name": "（县委统战部部长）待查", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "隰县县委常委、统战部部长", "current_org": "中共隰县委员会统战部",
     "source": ""},

    {"id": 11, "name": "（县人武部政委/部长）待查", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "隰县县委常委、人武部领导", "current_org": "隰县人民武装部",
     "source": ""},
]

organizations = [
    {"id": 1, "name": "中共隰县委员会", "type": "党委", "level": "县处级", "parent": "中共临汾市委员会", "location": "山西省临汾市隰县"},
    {"id": 2, "name": "隰县人民政府", "type": "政府", "level": "县处级", "parent": "临汾市人民政府", "location": "山西省临汾市隰县"},
    {"id": 3, "name": "中共隰县纪律检查委员会", "type": "纪委", "level": "副县级", "parent": "中共隰县委员会", "location": "山西省临汾市隰县"},
    {"id": 4, "name": "中共隰县委员会组织部", "type": "党委部门", "level": "正科级", "parent": "中共隰县委员会", "location": "山西省临汾市隰县"},
    {"id": 5, "name": "中共隰县委员会宣传部", "type": "党委部门", "level": "正科级", "parent": "中共隰县委员会", "location": "山西省临汾市隰县"},
    {"id": 6, "name": "中共隰县委员会政法委员会", "type": "党委部门", "level": "正科级", "parent": "中共隰县委员会", "location": "山西省临汾市隰县"},
    {"id": 7, "name": "中共隰县委员会统战部", "type": "党委部门", "level": "正科级", "parent": "中共隰县委员会", "location": "山西省临汾市隰县"},
    {"id": 8, "name": "隰县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "隰县", "location": "山西省临汾市隰县"},
    {"id": 9, "name": "中国人民政治协商会议隰县委员会", "type": "政协", "level": "县处级", "parent": "隰县", "location": "山西省临汾市隰县"},
    {"id": 10, "name": "隰县人民武装部", "type": "武装", "level": "正团级", "parent": "", "location": "山西省临汾市隰县"},
    {"id": 11, "name": "中共湖南省委组织部", "type": "党委部门", "level": "省部级", "parent": "中共湖南省委", "location": "湖南省长沙市"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "隰县县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "现任，姓名待确认"},
    {"person_id": 2, "org_id": 2, "title": "隰县县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "现任，姓名待确认"},
    {"person_id": 3, "org_id": 11, "title": "湖南省委组织部部长", "start_date": "", "end_date": "present", "rank": "副部级", "note": "山西隰县人"},
    {"person_id": 4, "org_id": 1, "title": "隰县县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "姓名待确认"},
    {"person_id": 5, "org_id": 2, "title": "隰县县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "姓名待确认"},
    {"person_id": 6, "org_id": 3, "title": "隰县县委常委、县纪委书记、县监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "姓名待确认"},
    {"person_id": 7, "org_id": 4, "title": "隰县县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "姓名待确认"},
    {"person_id": 8, "org_id": 5, "title": "隰县县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "姓名待确认"},
    {"person_id": 9, "org_id": 6, "title": "隰县县委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "姓名待确认"},
    {"person_id": 10, "org_id": 7, "title": "隰县县委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "姓名待确认"},
    {"person_id": 11, "org_id": 10, "title": "隰县人武部领导", "start_date": "", "end_date": "present", "rank": "正团级/副处级", "note": "姓名待确认"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政一把手共事", "context": "县委书记与县长搭班子", "overlap_org": "隰县", "overlap_period": "目前"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "县委书记与县委副书记", "overlap_org": "中共隰县委员会", "overlap_period": "目前"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "县委书记与常务副县长", "overlap_org": "隰县", "overlap_period": "目前"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "县长与常务副县长", "overlap_org": "隰县人民政府", "overlap_period": "目前"},
]

# ── BUILD ────────────────────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

# Database
conn = sqlite3.connect(DB_PATH)
conn.executescript("""
    DROP TABLE IF EXISTS relationships;
    DROP TABLE IF EXISTS positions;
    DROP TABLE IF EXISTS organizations;
    DROP TABLE IF EXISTS persons;

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
    );

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
    );
""")

for p in persons:
    conn.execute(
        "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, "
        "party_join, work_start, current_post, current_org, source) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
         p["education"], p["party_join"], p["work_start"], p["current_post"],
         p["current_org"], p["source"])
    )

for o in organizations:
    conn.execute(
        "INSERT INTO organizations (id, name, type, level, parent, location) "
        "VALUES (?,?,?,?,?,?)",
        (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
    )

for pos in positions:
    conn.execute(
        "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) "
        "VALUES (?,?,?,?,?,?,?)",
        (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"],
         pos["end_date"], pos["rank"], pos["note"])
    )

for r in relationships:
    conn.execute(
        "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) "
        "VALUES (?,?,?,?,?,?)",
        (r["person_a"], r["person_b"], r["type"], r["context"],
         r["overlap_org"], r["overlap_period"])
    )

conn.commit()
conn.close()

print(f"Database written: {DB_PATH}")
print(f"  Persons: {len(persons)}")
print(f"  Organizations: {len(organizations)}")
print(f"  Positions: {len(positions)}")
print(f"  Relationships: {len(relationships)}")

# ── GEXF ─────────────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(current_post):
    if "书记" in current_post and "纪委" not in current_post:
        return (255, 50, 50)  # Red: Party Secretary
    elif "县长" in current_post or ("副县长" in current_post):
        return (50, 100, 255)  # Blue: government leader
    elif "纪委书记" in current_post or "纪委" in current_post:
        return (255, 165, 0)  # Orange: discipline
    elif "人大" in current_post:
        return (200, 255, 255)  # Cyan
    elif "政协" in current_post:
        return (255, 240, 200)  # Cream
    else:
        return (100, 100, 100)  # Grey: others

def person_size(current_post):
    if "县委书记" in current_post:
        return 20.0
    elif "县长" in current_post:
        return 18.0
    else:
        return 12.0

def org_color(org_type):
    colors = {
        "党委": (255, 200, 200),
        "政府": (200, 200, 255),
        "纪委": (255, 165, 0),
        "人大": (200, 255, 255),
        "政协": (255, 240, 200),
        "党委部门": (255, 220, 220),
    }
    return colors.get(org_type, (200, 200, 200))

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>隰县领导班子工作关系网络图（部分数据为待查状态）</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="current_post" type="string"/>')
lines.append('      <attribute id="2" title="current_org" type="string"/>')
lines.append('      <attribute id="3" title="birth" type="string"/>')
lines.append('      <attribute id="4" title="birthplace" type="string"/>')
lines.append('      <attribute id="5" title="education" type="string"/>')
lines.append('      <attribute id="6" title="source" type="string"/>')
lines.append('      <attribute id="7" title="org_type" type="string"/>')
lines.append('      <attribute id="8" title="level" type="string"/>')
lines.append('      <attribute id="9" title="location" type="string"/>')
lines.append('    </attributes>')

lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('      <attribute id="2" title="period" type="string"/>')
lines.append('    </attributes>')

# Nodes: Persons
lines.append('    <nodes>')
for p in persons:
    c = person_color(p["current_post"])
    sz = person_size(p["current_post"])
    lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
    lines.append(f'          <attvalue for="4" value="{esc(p["birthplace"])}"/>')
    lines.append(f'          <attvalue for="5" value="{esc(p["education"])}"/>')
    lines.append(f'          <attvalue for="6" value="{esc(p["source"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Nodes: Organizations
for o in organizations:
    oid = 1000 + o["id"]
    c = org_color(o["type"])
    lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="org"/>')
    lines.append(f'          <attvalue for="7" value="{esc(o["type"])}"/>')
    lines.append(f'          <attvalue for="8" value="{esc(o["level"])}"/>')
    lines.append(f'          <attvalue for="9" value="{esc(o["location"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')

lines.append('    </nodes>')

# Edges: person -> organization (worked_at)
lines.append('    <edges>')
edge_id = 1
for pos in positions:
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="{edge_id}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
    lines.append(f'          <attvalue for="2" value="{pos["start_date"] or "?"} → {pos["end_date"] or "今"}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
    edge_id += 1

# Edges: person -> person (relationships)
for r in relationships:
    lines.append(f'      <edge id="{edge_id}" source="{r["person_a"]}" target="{r["person_b"]}" label="{esc(r["type"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
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