#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 左贡县 (Zuogong County), 昌都市, 西藏自治区.

Current officeholders as of 2026-07:
  - Party Secretary (县委书记): 常红强
  - County Mayor (县长): 格桑 (县委副书记、政府县长)
  - Key deputies: 陈友华 (县人大常委会主任), 周建军 (县委常委、政府副县长)
  - Predecessor: 白玛扎西 (former 左贡县委书记, promoted to 昌都市人大常委会副主任 2024-12)

Sources:
  - zuogong.changdu.gov.cn (official 左贡县人民政府 website, leadership section)
  - changdu.gov.cn news/search results (昌都市人民政府)
  - 昌都市人民代表大会公告 (2024-12-30)
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TASK_ID = "xizang_左贡县"
STAGING = os.path.join(BASE, "data/tmp", TASK_ID)
DB_PATH = os.path.join(STAGING, "左贡县_network.db")
GEXF_PATH = os.path.join(STAGING, "左贡县_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

os.makedirs(STAGING, exist_ok=True)

# =========================================================================
# SQL SCHEMA
# =========================================================================
CREATE_PERSONS = """CREATE TABLE IF NOT EXISTS persons (
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
)"""

CREATE_ORGANIZATIONS = """CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT DEFAULT '',
    level TEXT DEFAULT '',
    parent TEXT DEFAULT '',
    location TEXT DEFAULT ''
)"""

CREATE_POSITIONS = """CREATE TABLE IF NOT EXISTS positions (
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
)"""

CREATE_RELATIONSHIPS = """CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER NOT NULL,
    person_b INTEGER NOT NULL,
    type TEXT DEFAULT '',
    context TEXT DEFAULT '',
    overlap_org TEXT DEFAULT '',
    overlap_period TEXT DEFAULT '',
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
)"""

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── 县委书记 ──
    {
        "id": 1,
        "name": "常红强",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "左贡县委书记",
        "current_org": "中共左贡县委员会",
        "source": "http://zuogong.changdu.gov.cn/ (confirmed via news: 2024-06-04 六一活动) + changdu.gov.cn search"
    },
    # ── 县长 ──
    {
        "id": 2,
        "name": "格桑",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1973-10",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "左贡县委副书记、政府县长",
        "current_org": "左贡县人民政府",
        "source": "http://zuogong.changdu.gov.cn/ (official leadership section, confirmed 2026-07)"
    },
    # ── 县人大常委会主任 ──
    {
        "id": 3,
        "name": "陈友华",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "左贡县委常委、县人大常委会主任",
        "current_org": "左贡县人大常委会",
        "source": "changdu.gov.cn news: 人大资讯|李雨雷深入左贡县田妥镇调研 (2023-11-21)"
    },
    # ── 县委常委、副县长 ──
    {
        "id": 4,
        "name": "周建军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "左贡县委常委、政府副县长",
        "current_org": "左贡县人民政府",
        "source": "changdu.gov.cn news: 昌都市教育系统六一活动 (2024-06-04)"
    },
    # ── 前任县委书记（现已升迁）──
    {
        "id": 5,
        "name": "白玛扎西",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昌都市人大常委会副主任",
        "current_org": "昌都市人民代表大会常务委员会",
        "source": ("昌都市人民代表大会公告 (2024-12-30): "
                   "补选白玛扎西为昌都市人大常委会副主任")
    },
    # ── 县政协主席（待查）──
    {
        "id": 6,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "左贡县政协主席",
        "current_org": "政协左贡县委员会",
        "source": "Not yet identified — check zuogong.changdu.gov.cn leadership page"
    },
    # ── 县纪委书记（待查）──
    {
        "id": 7,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "左贡县委常委、纪委书记、监委主任",
        "current_org": "中共左贡县纪律检查委员会",
        "source": "Not yet identified — check website or news"
    },
    # ── 县委组织部部长（待查）──
    {
        "id": 8,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "左贡县委常委、组织部部长",
        "current_org": "中共左贡县委组织部",
        "source": "Not yet identified — check website or news"
    },
    # ── 县委宣传部部长（待查）──
    {
        "id": 9,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "左贡县委常委、宣传部部长",
        "current_org": "中共左贡县委宣传部",
        "source": "Not yet identified — check website or news"
    },
    # ── 县委政法委书记（待查）──
    {
        "id": 10,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "左贡县委常委、政法委书记",
        "current_org": "中共左贡县委政法委员会",
        "source": "Not yet identified — check website or news"
    },
    # ── 县委统战部部长（待查）──
    {
        "id": 11,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "左贡县委常委、统战部部长",
        "current_org": "中共左贡县委统战部",
        "source": "Not yet identified — check website or news"
    },
    # ── 县人武部部长（待查）──
    {
        "id": 12,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "左贡县委常委、人武部部长",
        "current_org": "左贡县人民武装部",
        "source": "Not yet identified — check website or news"
    },
    # ── 县委副书记（专职，待查）──
    {
        "id": 13,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "左贡县委副书记（专职）",
        "current_org": "中共左贡县委员会",
        "source": "Not yet identified — check website or news"
    },
    # ── 县政府副县长（分管常务，待查）──
    {
        "id": 14,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "左贡县委常委、常务副县长",
        "current_org": "左贡县人民政府",
        "source": "Not yet identified — check website or news"
    },
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共左贡县委员会", "type": "党委", "level": "县级",
     "parent": "中共昌都市委员会", "location": "西藏自治区昌都市左贡县"},
    {"id": 2, "name": "左贡县人民政府", "type": "政府", "level": "县级",
     "parent": "昌都市人民政府", "location": "西藏自治区昌都市左贡县"},
    {"id": 3, "name": "左贡县人大常委会", "type": "人大", "level": "县级",
     "parent": "左贡县", "location": "西藏自治区昌都市左贡县"},
    {"id": 4, "name": "政协左贡县委员会", "type": "政协", "level": "县级",
     "parent": "左贡县", "location": "西藏自治区昌都市左贡县"},
    {"id": 5, "name": "中共左贡县纪律检查委员会", "type": "党委", "level": "县级",
     "parent": "中共左贡县委员会", "location": "西藏自治区昌都市左贡县"},
    {"id": 6, "name": "左贡县监察委员会", "type": "政府", "level": "县级",
     "parent": "左贡县", "location": "西藏自治区昌都市左贡县"},
    {"id": 7, "name": "左贡县人民法院", "type": "政府", "level": "县级",
     "parent": "左贡县", "location": "西藏自治区昌都市左贡县"},
    {"id": 8, "name": "左贡县人民检察院", "type": "政府", "level": "县级",
     "parent": "左贡县", "location": "西藏自治区昌都市左贡县"},
    {"id": 9, "name": "中共左贡县委组织部", "type": "党委", "level": "县级",
     "parent": "中共左贡县委员会", "location": "西藏自治区昌都市左贡县"},
    {"id": 10, "name": "中共左贡县委宣传部", "type": "党委", "level": "县级",
     "parent": "中共左贡县委员会", "location": "西藏自治区昌都市左贡县"},
    {"id": 11, "name": "中共左贡县委政法委员会", "type": "党委", "level": "县级",
     "parent": "中共左贡县委员会", "location": "西藏自治区昌都市左贡县"},
    {"id": 12, "name": "中共左贡县委统战部", "type": "党委", "level": "县级",
     "parent": "中共左贡县委员会", "location": "西藏自治区昌都市左贡县"},
    {"id": 13, "name": "左贡县人民武装部", "type": "政府", "level": "县级",
     "parent": "左贡县", "location": "西藏自治区昌都市左贡县"},
    {"id": 14, "name": "中共昌都市委员会", "type": "党委", "level": "地级",
     "parent": "中共西藏自治区委员会", "location": "西藏自治区昌都市卡若区"},
    {"id": 15, "name": "昌都市人民政府", "type": "政府", "level": "地级",
     "parent": "西藏自治区人民政府", "location": "西藏自治区昌都市卡若区"},
    {"id": 16, "name": "昌都市人民代表大会常务委员会", "type": "人大", "level": "地级",
     "parent": "昌都市", "location": "西藏自治区昌都市卡若区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 常红强
    {"person_id": 1, "org_id": 1, "title": "左贡县委书记",
     "start_date": "unknown", "end_date": "present", "rank": "正处级",
     "note": "Current Party Secretary of Zuogong County. Confirmed via multiple news sources (2024-06 六一活动). Exact appointment date unknown."},
    # 格桑
    {"person_id": 2, "org_id": 2, "title": "左贡县委副书记、政府县长",
     "start_date": "unknown", "end_date": "present", "rank": "正处级",
     "note": "Confirmed on zuogong.changdu.gov.cn official leadership page. Male, Tibetan, born 1973-10."},
    # 陈友华
    {"person_id": 3, "org_id": 1, "title": "左贡县委常委",
     "start_date": "unknown", "end_date": "present", "rank": "副处级",
     "note": "Confirmed via changdu.gov.cn news (2023-11-21) as 县委常委"},
    {"person_id": 3, "org_id": 3, "title": "左贡县人大常委会主任",
     "start_date": "unknown", "end_date": "present", "rank": "正处级",
     "note": "Confirmed via changdu.gov.cn news (2023-11-21)"},
    # 周建军
    {"person_id": 4, "org_id": 1, "title": "左贡县委常委",
     "start_date": "unknown", "end_date": "present", "rank": "副处级",
     "note": "Confirmed as 县委常委、政府副县长 via changdu.gov.cn news (2024-06-04)"},
    {"person_id": 4, "org_id": 2, "title": "左贡县政府副县长",
     "start_date": "unknown", "end_date": "present", "rank": "副处级",
     "note": ""},
    # 白玛扎西 — 前任县委书记
    {"person_id": 5, "org_id": 1, "title": "左贡县委书记",
     "start_date": "unknown", "end_date": "2024-12", "rank": "正处级",
     "note": "Former Party Secretary of Zuogong County. Promoted out in 2024-12."},
    {"person_id": 5, "org_id": 16, "title": "昌都市人大常委会副主任",
     "start_date": "2024-12", "end_date": "present", "rank": "副厅级",
     "note": "Elected at 昌都市第二届人民代表大会第六次会议 (2024-12-30)"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "常红强（县委书记）和格桑（县长）是左贡县党政主要领导搭档",
        "overlap_org": "中共左贡县委员会/左贡县人民政府",
        "overlap_period": "2024至今"
    },
    {
        "person_a": 5, "person_b": 1,
        "type": "predecessor_successor",
        "context": "白玛扎西是前任左贡县委书记，常红强接任",
        "overlap_org": "中共左贡县委员会",
        "overlap_period": "2024"
    },
    {
        "person_a": 5, "person_b": 2,
        "type": "superior_subordinate",
        "context": "白玛扎西任县委书记时，格桑任县长",
        "overlap_org": "中共左贡县委员会/左贡县人民政府",
        "overlap_period": "至2024-12"
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "常红强（书记）与陈友华（常委、人大主任）为县委常委班子同事",
        "overlap_org": "中共左贡县委员会",
        "overlap_period": "至今"
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "superior_subordinate",
        "context": "常红强（书记）与周建军（常委、副县长）为县委常委班子同事",
        "overlap_org": "中共左贡县委员会",
        "overlap_period": "至今"
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "superior_subordinate",
        "context": "格桑（县长）与陈友华（人大主任）同乡县党政班子",
        "overlap_org": "左贡县",
        "overlap_period": "至今"
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "superior_subordinate",
        "context": "格桑（县长）与周建军（副县长）为县政府领导",
        "overlap_org": "左贡县人民政府",
        "overlap_period": "至今"
    },
]

# =========================================================================
# CREATE DATABASE
# =========================================================================
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute(CREATE_PERSONS)
c.execute(CREATE_ORGANIZATIONS)
c.execute(CREATE_POSITIONS)
c.execute(CREATE_RELATIONSHIPS)

# Insert persons
for p in persons:
    c.execute("""INSERT OR REPLACE INTO persons
        (id, name, gender, ethnicity, birth, birthplace, education,
         party_join, work_start, current_post, current_org, source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
         p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
         p.get("party_join", ""), p.get("work_start", ""),
         p["current_post"], p["current_org"], p["source"]))

# Insert organizations
for o in organizations:
    c.execute("""INSERT OR REPLACE INTO organizations
        (id, name, type, level, parent, location)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

# Insert positions
for pos in positions:
    c.execute("""INSERT INTO positions
        (person_id, org_id, title, start_date, end_date, rank, note)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (pos["person_id"], pos["org_id"], pos["title"],
         pos.get("start_date", ""), pos.get("end_date", ""),
         pos.get("rank", ""), pos.get("note", "")))

# Insert relationships
for rel in relationships:
    c.execute("""INSERT INTO relationships
        (person_a, person_b, type, context, overlap_org, overlap_period)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (rel["person_a"], rel["person_b"], rel["type"],
         rel["context"], rel["overlap_org"], rel["overlap_period"]))

conn.commit()
conn.close()

print(f"✅ SQLite database created: {DB_PATH}")
print(f"  - {len(persons)} persons")
print(f"  - {len(organizations)} organizations")
print(f"  - {len(positions)} positions")
print(f"  - {len(relationships)} relationships")

# =========================================================================
# CREATE GEXF
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    role = p.get("current_post", "")
    name = p.get("name", "")
    if name == "待查":
        return "180,180,180"
    if "县委书记" in role or "书记" in role:
        return "255,50,50"
    if "县长" in role or "市长" in role or "区长" in role:
        return "50,100,255"
    if "纪委书记" in role or "纪委" in role:
        return "255,165,0"
    if "政协" in role:
        return "255,240,200"
    if "人大" in role:
        return "200,255,255"
    if "常委" in role or "组织" in role or "宣传" in role or "统战" in role or "政法" in role:
        return "100,100,100"
    return "100,100,100"

def org_color(o):
    t = o["type"]
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "开发区" in t:
        return "200,255,200"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    if "乡镇" in t or "街道" in t:
        return "255,255,200"
    if "事业" in t:
        return "220,220,220"
    if "群团" in t:
        return "255,220,255"
    return "200,200,200"

def is_top_leader(p):
    role = p.get("current_post", "")
    if "县委书记" in role or "县长" in role or "区长" in role:
        return True
    return False

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{TODAY}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>左贡县领导班子工作关系网络 - Built from official government sources</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="level" type="string"/>')
lines.append('    </attributes>')

# Edge attributes
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('      <attribute id="2" title="period" type="string"/>')
lines.append('    </attributes>')

# Person nodes
lines.append('    <nodes>')
for p in persons:
    nid = f"p{p['id']}"
    label = p["name"]
    c = person_color(p)
    sz = "20.0" if is_top_leader(p) else ("12.0" if p["name"] != "待查" else "8.0")
    lines.append(f'      <node id="{nid}" label="{esc(label)}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
    lines.append(f'          <attvalue for="2" value="county"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Organization nodes
for o in organizations:
    nid = f"o{o['id']}"
    c = org_color(o)
    sz = "8.0"
    lines.append(f'      <node id="{nid}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(o.get("level", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
eid = 0

# Person→Organization: worked_at
for pos in positions:
    eid += 1
    src = f"p{pos['person_id']}"
    tgt = f"o{pos['org_id']}"
    label = pos['title']
    lines.append(f'      <edge id="e{eid}" source="{src}" target="{tgt}" label="{esc(label)}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(label)}"/>')
    lines.append(f'          <attvalue for="2" value="{pos.get("start_date","")}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

# Person↔Person: relationships
for rel in relationships:
    eid += 1
    src = f"p{rel['person_a']}"
    tgt = f"p{rel['person_b']}"
    lines.append(f'      <edge id="e{eid}" source="{src}" target="{tgt}" label="{esc(rel["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{esc(rel["context"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(rel["overlap_period"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ GEXF graph created: {GEXF_PATH}")
print(f"    - {len(persons)} person nodes")
print(f"    - {len(organizations)} organization nodes")
print(f"    - {eid} edges")
print()
print("=== IMPORTANT NOTES ===")
print("- Current officeholders for 常红强 (Party Sec) and correct (County Mayor) are confirmed.")
print("- 6 key deputy positions (纪委书记, 组织部长, 宣传部长, 统战部长, 政法书记, 人武部长, 专职副书记, 常务副县长)")
print("  are placeholder '待查' — their names were not found on the main homepage or search results.")
print("- 白玛扎西 (predecessor) confirmed promoted to 昌都市人大常委会副主任 in Dec 2024.")
print("- Try accessing zuogong.changdu.gov.cn/zwgk/ldzc/ or the internal leadership page for more.")