#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 泉港区 (Quangang District) leadership network.

Level: 市辖区
Province: 福建省
Parent City: 泉州市
Targets: 区委书记 & 区长

Key findings (as of July 2026):
- 区委书记: 杨昌文 (confirmed per Wikipedia)
- 区委副书记、区长: 杨凤翔 (confirmed from qg.gov.cn homepage)
- 副区长: 陈其昌, 庄一鸣, 谢梓骞, 郭雅婷, 朱添洪, 庄向阳, 张剑平, 林坤清

Sources:
- Wikipedia (zh.wikipedia.org): 泉港区 entry, registers 杨昌文 as 区委书记
- Quangang District Government website (www.qg.gov.cn): lists 杨凤翔 as 区长
- Quangang District Government homepage leadership section

Current as of: July 2026

Gaps:
- Birth dates, education, and full career timelines for most officials
- Party Committee Standing Committee (区委常委) full roster beyond top leaders
- Previous Party Secretary and their current whereabouts
- Details on 杨昌文's earlier career history
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/tmp/fujian_泉港区/泉港区_network.db")
GEXF_PATH = os.path.join(BASE, "data/tmp/fujian_泉港区/泉港区_network.gexf")

# ── HELPER FUNCTIONS ────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_role_color(p):
    """Return viz color based on role."""
    post = p["current_post"]
    if "区委书记" in post and "副书记" not in post:
        return "255,50,50"   # Red — Party Secretary
    if "区长" in post:
        return "50,100,255"  # Blue — Government head
    if "副区长" in post or "区政府" in post:
        return "50,100,255"  # Blue — Government deputy
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"   # Orange — Discipline
    if "政法委" in post:
        return "180,130,50"  # Brown — Legal/political-legal
    if "组织部" in post:
        return "200,100,200" # Purple — Organization
    if "宣传部" in post:
        return "100,200,100" # Green — Propaganda
    if "副书记" in post:
        return "200,50,50"   # Dark red — Deputy Party Secretary
    return "100,100,100"    # Grey — Others

def is_top_leader(p):
    """Check if person is a top leader (区委书记 or 区长)."""
    return p["id"] <= 2

def org_color(org_type):
    """Return viz color for organization type."""
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(org_type, "200,200,200")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Party Secretary (区委书记) ──
    {"id": 1, "name": "杨昌文", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共泉州市泉港区委书记", "current_org": "中共泉州市泉港区委员会",
     "source": "https://zh.wikipedia.org/wiki/%E6%B3%89%E6%B8%AF%E5%8C%BA"},

    # ── Current District Mayor (区长) ──
    {"id": 2, "name": "杨凤翔", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泉港区人民政府区长", "current_org": "泉港区人民政府",
     "source": "https://www.qg.gov.cn/"},

    # ── Deputy District Mayors (副区长) ──
    {"id": 3, "name": "陈其昌", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "泉港区人民政府副区长", "current_org": "泉港区人民政府",
     "source": "https://www.qg.gov.cn/"},

    {"id": 4, "name": "庄一鸣", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "泉港区人民政府副区长", "current_org": "泉港区人民政府",
     "source": "https://www.qg.gov.cn/"},

    {"id": 5, "name": "谢梓骞", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "泉港区人民政府副区长", "current_org": "泉港区人民政府",
     "source": "https://www.qg.gov.cn/"},

    {"id": 6, "name": "郭雅婷", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "泉港区人民政府副区长", "current_org": "泉港区人民政府",
     "source": "https://www.qg.gov.cn/"},

    {"id": 7, "name": "朱添洪", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "泉港区人民政府副区长", "current_org": "泉港区人民政府",
     "source": "https://www.qg.gov.cn/"},

    {"id": 8, "name": "庄向阳", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "泉港区人民政府副区长", "current_org": "泉港区人民政府",
     "source": "https://www.qg.gov.cn/"},

    {"id": 9, "name": "张剑平", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "泉港区人民政府副区长", "current_org": "泉港区人民政府",
     "source": "https://www.qg.gov.cn/"},

    {"id": 10, "name": "林坤清", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "泉港区人民政府副区长", "current_org": "泉港区人民政府",
     "source": "https://www.qg.gov.cn/"},
]

organizations = [
    {"id": 1, "name": "中共泉州市泉港区委员会", "type": "党委", "level": "市辖区", "parent": "中共泉州市委员会", "location": "福建省泉州市泉港区"},
    {"id": 2, "name": "泉港区人民政府", "type": "政府", "level": "市辖区", "parent": "泉州市人民政府", "location": "福建省泉州市泉港区"},
    {"id": 3, "name": "中共泉港区纪律检查委员会", "type": "党委", "level": "市辖区", "parent": "中共泉州市泉港区委员会", "location": "福建省泉州市泉港区"},
    {"id": 4, "name": "泉港区人民代表大会常务委员会", "type": "人大", "level": "市辖区", "parent": "泉港区", "location": "福建省泉州市泉港区"},
    {"id": 5, "name": "中国人民政治协商会议泉港区委员会", "type": "政协", "level": "市辖区", "parent": "泉港区", "location": "福建省泉州市泉港区"},
]

positions = [
    # 杨昌文 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "中共泉州市泉港区委书记", "start": "", "end": "present", "rank": "正处级", "note": "区委书记"},

    # 杨凤翔 — 区长
    {"person_id": 2, "org_id": 2, "title": "泉港区人民政府区长", "start": "", "end": "present", "rank": "正处级", "note": "区长"},

    # 副区长们
    {"person_id": 3, "org_id": 2, "title": "泉港区人民政府副区长", "start": "", "end": "present", "rank": "副处级", "note": "副区长"},
    {"person_id": 4, "org_id": 2, "title": "泉港区人民政府副区长", "start": "", "end": "present", "rank": "副处级", "note": "副区长"},
    {"person_id": 5, "org_id": 2, "title": "泉港区人民政府副区长", "start": "", "end": "present", "rank": "副处级", "note": "副区长"},
    {"person_id": 6, "org_id": 2, "title": "泉港区人民政府副区长", "start": "", "end": "present", "rank": "副处级", "note": "副区长"},
    {"person_id": 7, "org_id": 2, "title": "泉港区人民政府副区长", "start": "", "end": "present", "rank": "副处级", "note": "副区长"},
    {"person_id": 8, "org_id": 2, "title": "泉港区人民政府副区长", "start": "", "end": "present", "rank": "副处级", "note": "副区长"},
    {"person_id": 9, "org_id": 2, "title": "泉港区人民政府副区长", "start": "", "end": "present", "rank": "副处级", "note": "副区长"},
    {"person_id": 10, "org_id": 2, "title": "泉港区人民政府副区长", "start": "", "end": "present", "rank": "副处级", "note": "副区长"},
]

relationships = [
    # 杨昌文 + 杨凤翔 — 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长党政正职搭档", "overlap_org": "泉港区", "overlap_period": "至今"},
]


# ── BUILD SQLITE DB ──────────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
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
    person_id INTEGER, org_id INTEGER,
    title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
    FOREIGN KEY(person_id) REFERENCES persons(id),
    FOREIGN KEY(org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER, person_b INTEGER,
    type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY(person_a) REFERENCES persons(id),
    FOREIGN KEY(person_b) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
                 p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()
conn.close()
print(f"[OK] SQLite database written: {DB_PATH}")

# ── BUILD GEXF ───────────────────────────────────────────────────────

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>China Gov Network Investigator</creator>')
lines.append('    <description>泉港区领导班子工作关系网络 - 福建省泉州市泉港区</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attribute declarations
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="org" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('    </attributes>')

# Nodes: persons
lines.append('    <nodes>')
for p in persons:
    c = person_role_color(p)
    sz = "20.0" if is_top_leader(p) else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
    lines.append('        </attvalues>')
    parts = c.split(",")
    lines.append(f'        <viz:color r="{parts[0]}" g="{parts[1]}" b="{parts[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Nodes: organizations
for o in organizations:
    c = org_color(o["type"])
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="org"/>')
    lines.append(f'          <attvalue for="2" value="{esc(o["name"])}"/>')
    lines.append('        </attvalues>')
    parts = c.split(",")
    lines.append(f'        <viz:color r="{parts[0]}" g="{parts[1]}" b="{parts[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
eid = 0

# person -> organization (worked_at)
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

# person <-> person (relationship)
for r in relationships:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"[OK] GEXF graph written: {GEXF_PATH}")

# ── SUMMARY ──────────────────────────────────────────────────────────

print(f"\nSummary:")
print(f"  Persons:         {len(persons)}")
print(f"  Organizations:   {len(organizations)}")
print(f"  Positions:       {len(positions)}")
print(f"  Relationships:   {len(relationships)}")
print(f"  Edges (total):   {eid}")
print(f"\n  DB:   {DB_PATH}")
print(f"  GEXF: {GEXF_PATH}")
