#!/usr/bin/env python3
"""
Build SQLite database and GEXF graph for 苏仙区 (Suxian District, Chenzhou, Hunan) leadership network.

苏仙区 — 湖南省郴州市市辖区, 位于湖南省南部, 郴州市中心城区之一.
Research date: 2026-07-24. Sources: suxiannews.cn news articles.
"""

import json
import os
import sqlite3
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/hunan_苏仙区")
DB_PATH = os.path.join(STAGING, "苏仙区_network.db")
GEXF_PATH = os.path.join(STAGING, "苏仙区_network.gexf")
PERSONS_DIR = os.path.join(STAGING, "persons")

AS_OF = "2026-07-24"
TODAY = AS_OF.replace("-", "")

# ═══════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════

# ── Persons ──
persons = [
    # ── Core Leaders (Targets) ──
    # 禹谦和 — 苏仙区委书记 (confirmed via suxiannews.cn 2026-07-23)
    {"id": 1, "name": "禹谦和", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "苏仙区委书记",
     "current_org": "中共苏仙区委",
     "source": "suxiannews.cn (2026-07-23 article about industrial park inspection)"},

    # 苏仙区区长 — (name currently unknown, marked as open gap)
    {"id": 2, "name": "苏仙区区长（姓名待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "苏仙区委副书记、区长",
     "current_org": "苏仙区人民政府",
     "source": "open_gap — see report/open_gaps.md"},

    # ──区委其他领导 (partially known from suxiannews) ──
    # 吕银俊 — known from news headline "吕银俊检查重点领域安全生产工作"
    {"id": 3, "name": "吕银俊", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "苏仙区委领导",
     "current_org": "中共苏仙区委",
     "source": "suxiannews.cn headline (2026-07)"},
]

# ── Organizations ──
organizations = [
    {"id": 1, "name": "中共苏仙区委", "type": "党委", "level": "市辖区", "parent": "中共郴州市委", "location": "郴州市苏仙区"},
    {"id": 2, "name": "苏仙区人民政府", "type": "政府", "level": "市辖区", "parent": "郴州市人民政府", "location": "郴州市苏仙区"},
    {"id": 3, "name": "苏仙高新技术产业发展中心", "type": "开发区", "level": "市辖区", "parent": "苏仙区人民政府", "location": "郴州市苏仙区"},
]

# ── Positions ──
positions = [
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "", "end": "", "note": "as of 2026-07"},
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "", "note": "姓名待确认"},
    {"person_id": 3, "org_id": 1, "title": "区委领导", "start": "", "end": "", "note": "身份待确认"},
]

# ── Relationships ──
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "苏仙区", "overlap_org": "苏仙区",
     "overlap_period": "2026", "confidence": "confirmed",
     "source": "苏仙区领导架构"},
]

# ═══════════════════════════════════════════════════════════════════════
# BUILD DATABASE
# ═══════════════════════════════════════════════════════════════════════

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.executescript("""
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, education TEXT,
    party_join TEXT, work_start TEXT,
    current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER, org_id INTEGER, title TEXT,
    start TEXT, "end" TEXT, note TEXT,
    FOREIGN KEY(person_id) REFERENCES persons(id),
    FOREIGN KEY(org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER, person_b INTEGER,
    type TEXT, context TEXT,
    overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY(person_a) REFERENCES persons(id),
    FOREIGN KEY(person_b) REFERENCES persons(id)
);
""")

for p in persons:
    c.execute("""INSERT OR IGNORE INTO persons
        (id, name, gender, ethnicity, birth, birthplace, education,
         party_join, work_start, current_post, current_org, source)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
        (p["id"], p["name"], p["gender"], p["ethnicity"],
         p["birth"], p["birthplace"], p["education"],
         p["party_join"], p["work_start"],
         p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    c.execute("""INSERT OR IGNORE INTO organizations
        (id, name, type, level, parent, location)
        VALUES (?,?,?,?,?,?)""",
        (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    c.execute("""INSERT INTO positions
        (person_id, org_id, title, start, "end", note)
        VALUES (?,?,?,?,?,?)""",
        (pos["person_id"], pos["org_id"], pos["title"],
         pos.get("start", ""), pos.get("end", ""), pos.get("note", "")))

for rel in relationships:
    c.execute("""INSERT INTO relationships
        (person_a, person_b, type, context, overlap_org, overlap_period)
        VALUES (?,?,?,?,?,?)""",
        (rel["person_a"], rel["person_b"], rel["type"],
         rel["context"], rel["overlap_org"], rel["overlap_period"]))

conn.commit()

# Stats
print(f"✅ 数据库写入完成: {DB_PATH}")
print(f"   - {c.execute('SELECT COUNT(*) FROM persons').fetchone()[0]} 人")
print(f"   - {c.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]} 组织")
print(f"   - {c.execute('SELECT COUNT(*) FROM positions').fetchone()[0]} 任职")
print(f"   - {c.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]} 关系")

conn.close()

# ═══════════════════════════════════════════════════════════════════════
# BUILD GEXF
# ═══════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>gov-relation research agent</creator>')
lines.append('    <description>苏仙区领导班子工作关系网络</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attribute declarations
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="label" type="string"/>')
lines.append('    </attributes>')

# Person nodes
lines.append('    <nodes>')
for p in persons:
    pid = p["id"]
    name = p["name"]
    role = p["current_post"]
    # Color by role
    if "书记" in role:
        color = "255,50,50"  # Red - Party Secretary
        size = 20.0
    elif "区长" in role:
        color = "50,100,255"  # Blue - District Mayor
        size = 20.0
    else:
        color = "100,100,100"  # Grey
        size = 12.0

    lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append('      </node>')

# Organization nodes
for o in organizations:
    oid = o["id"] + 1000
    oname = o["name"]
    otype = o["type"]
    # Color by org type
    if "党委" in otype:
        color = "255,200,200"  # Pink
    elif "政府" in otype:
        color = "200,200,255"  # Light blue
    elif "开发区" in otype:
        color = "200,255,200"  # Light green
    else:
        color = "200,200,200"

    lines.append(f'      <node id="o{oid}" label="{esc(oname)}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')

lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
eid = 0

# worked_at edges
for pos in positions:
    pid = pos["person_id"]
    oid = pos["org_id"] + 1000
    title = pos["title"]
    lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
    eid += 1

# relationship edges
for rel in relationships:
    pa = rel["person_a"]
    pb = rel["person_b"]
    rtype = rel["type"]
    lines.append(f'      <edge id="e{eid}" source="p{pa}" target="p{pb}" label="{esc(rtype)}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{esc(rtype)}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
    eid += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ GEXF写入完成: {GEXF_PATH}")
print(f"   - {len(persons) + len(organizations)} 节点")
print(f"   - {len(positions) + len(relationships)} 边")
print("✅ 全部完成！")
