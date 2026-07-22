#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Qinzhou District (秦州区), Tianshui, Gansu.

秦州区 — 天水市市辖区, 天水市委、市政府驻地, 全市政治经济文化中心.
Covers current District Party Secretary (康泰来), District Mayor (王志成),
their predecessors, key district leaders, and major organizations.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/gansu_秦州区")
os.makedirs(TMP, exist_ok=True)

DB_PATH = os.path.join(TMP, "秦州区_network.db")
GEXF_PATH = os.path.join(TMP, "秦州区_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================

persons = [
    # ── A. Current Top Leaders ──

    # 康泰来 — 天水市委常委、秦州区委书记 (as of 2026.07)
    {
        "id": 1, "name": "康泰来", "gender": "男", "ethnicity": "汉族",
        "birth": "1975-03", "birthplace": "甘肃武山",
        "education": "大学学历，教育硕士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "天水市委常委、秦州区委书记",
        "current_org": "中共天水市秦州区委员会",
        "source": "http://www.qinzhouqu.gov.cn/ldzc.htm"
    },

    # 王志成 — 秦州区委副书记、区长 (as of 2026.07)
    {
        "id": 2, "name": "王志成", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "秦州区委副书记、区长",
        "current_org": "秦州区人民政府",
        "source": "http://www.qinzhouqu.gov.cn/ldzc.htm"
    },

    # ── B. Four Major Leadership Team ──

    # 舒健 — 区人大常委会党组书记、主任
    {
        "id": 3, "name": "舒健", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "秦州区人大常委会党组书记、主任",
        "current_org": "秦州区人民代表大会常务委员会",
        "source": "http://www.qinzhouqu.gov.cn/info/8457/684286.htm"
    },

    # 毛更生 — 区政协党组书记、主席
    {
        "id": 4, "name": "毛更生", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "秦州区政协党组书记、主席",
        "current_org": "中国人民政治协商会议秦州区委员会",
        "source": "http://www.qinzhouqu.gov.cn/info/8457/684276.htm"
    },

    # ── C. District Leadership (from news articles) ──

    # 冯荣 — 区领导 (likely区委常委/副区长)
    {
        "id": 5, "name": "冯荣", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "秦州区领导（区委常委/副区长）",
        "current_org": "中共天水市秦州区委员会",
        "source": "http://www.qinzhouqu.gov.cn/info/8457/685476.htm"
    },

    # 李东海 — 区领导
    {
        "id": 6, "name": "李东海", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "秦州区领导",
        "current_org": "中共天水市秦州区委员会",
        "source": "http://www.qinzhouqu.gov.cn/info/8457/685476.htm"
    },

    # 李明善 — 区领导
    {
        "id": 7, "name": "李明善", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "秦州区领导",
        "current_org": "秦州区人民政府",
        "source": "http://www.qinzhouqu.gov.cn/info/8457/684296.htm"
    },

    # ── D. District People's Congress Leaders ──

    # 杨波涛 — 区人大常委会副主任
    {
        "id": 8, "name": "杨波涛", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "秦州区人大常委会副主任",
        "current_org": "秦州区人民代表大会常务委员会",
        "source": "http://www.qinzhouqu.gov.cn/info/8457/684286.htm"
    },

    # 张千红 — 区人大常委会副主任
    {
        "id": 9, "name": "张千红", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "秦州区人大常委会副主任",
        "current_org": "秦州区人民代表大会常务委员会",
        "source": "http://www.qinzhouqu.gov.cn/info/8457/684286.htm"
    },

    # 黄永辉 — 区人大常委会副主任
    {
        "id": 10, "name": "黄永辉", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "秦州区人大常委会副主任",
        "current_org": "秦州区人民代表大会常务委员会",
        "source": "http://www.qinzhouqu.gov.cn/info/8457/684286.htm"
    },

    # 张雪亮 — 区人大常委会副主任
    {
        "id": 11, "name": "张雪亮", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "秦州区人大常委会副主任",
        "current_org": "秦州区人民代表大会常务委员会",
        "source": "http://www.qinzhouqu.gov.cn/info/8457/684286.htm"
    },

    # 李春明 — 区人大常委会副主任
    {
        "id": 12, "name": "李春明", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "秦州区人大常委会副主任",
        "current_org": "秦州区人民代表大会常务委员会",
        "source": "http://www.qinzhouqu.gov.cn/info/8457/684286.htm"
    },

    # ── E. Predecessors ──

    # 孟晓龙 — 前任秦州区长（2021-2023），现任天水市副市长
    {
        "id": 13, "name": "孟晓龙", "gender": "男", "ethnicity": "汉族",
        "birth": "1970-09", "birthplace": "甘肃天水",
        "education": "省委党校大学学历",
        "party_join": "1999-02", "work_start": "1994-12",
        "current_post": "天水市副市长（原秦州区长）",
        "current_org": "天水市人民政府",
        "source": "http://www.tianshui.gov.cn/"
    },
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================

organizations = [
    {"id": 1, "name": "中共天水市秦州区委员会", "type": "党委", "level": "县处级",
     "parent": "中共天水市委员会", "location": "甘肃省天水市秦州区"},
    {"id": 2, "name": "秦州区人民政府", "type": "政府", "level": "县处级",
     "parent": "天水市人民政府", "location": "甘肃省天水市秦州区"},
    {"id": 3, "name": "秦州区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "天水市人大常委会", "location": "甘肃省天水市秦州区"},
    {"id": 4, "name": "中国人民政治协商会议秦州区委员会", "type": "政协", "level": "县处级",
     "parent": "天水市政协", "location": "甘肃省天水市秦州区"},
    {"id": 5, "name": "中共天水市委员会", "type": "党委", "level": "地厅级",
     "parent": "中共甘肃省委员会", "location": "甘肃省天水市"},
    {"id": 6, "name": "天水市人民政府", "type": "政府", "level": "地厅级",
     "parent": "甘肃省人民政府", "location": "甘肃省天水市"},
    {"id": 7, "name": "天水市人大常委会", "type": "人大", "level": "地厅级",
     "parent": "甘肃省人大常委会", "location": "甘肃省天水市"},
    {"id": 8, "name": "天水市政协", "type": "政协", "level": "地厅级",
     "parent": "甘肃省政协", "location": "甘肃省天水市"},
]

# =========================================================================
# POSITIONS (person → organization edges)
# =========================================================================

positions = [
    # District party committee
    {"person_id": 1, "org_id": 1, "title": "天水市委常委、秦州区委书记",
     "start": "2024-06", "end": "present", "rank": "副厅级"},
    {"person_id": 2, "org_id": 1, "title": "秦州区委副书记",
     "start": "2024-12", "end": "present", "rank": "县处级"},
    {"person_id": 5, "org_id": 1, "title": "秦州区领导（区委常委/副区长）",
     "start": "", "end": "present", "rank": "县处级"},
    {"person_id": 6, "org_id": 1, "title": "秦州区领导",
     "start": "", "end": "present", "rank": "县处级"},

    # District government
    {"person_id": 2, "org_id": 2, "title": "秦州区委副书记、区长",
     "start": "2024-12", "end": "present", "rank": "县处级正职"},
    {"person_id": 7, "org_id": 2, "title": "秦州区领导",
     "start": "", "end": "present", "rank": ""},

    # People's Congress
    {"person_id": 3, "org_id": 3, "title": "秦州区人大常委会党组书记、主任",
     "start": "", "end": "present", "rank": "县处级正职"},
    {"person_id": 8, "org_id": 3, "title": "秦州区人大常委会副主任",
     "start": "", "end": "present", "rank": "县处级副职"},
    {"person_id": 9, "org_id": 3, "title": "秦州区人大常委会副主任",
     "start": "", "end": "present", "rank": "县处级副职"},
    {"person_id": 10, "org_id": 3, "title": "秦州区人大常委会副主任",
     "start": "", "end": "present", "rank": "县处级副职"},
    {"person_id": 11, "org_id": 3, "title": "秦州区人大常委会副主任",
     "start": "", "end": "present", "rank": "县处级副职"},
    {"person_id": 12, "org_id": 3, "title": "秦州区人大常委会副主任",
     "start": "", "end": "present", "rank": "县处级副职"},

    # Political Consultative Conference
    {"person_id": 4, "org_id": 4, "title": "秦州区政协党组书记、主席",
     "start": "", "end": "present", "rank": "县处级正职"},

    # Predecessor
    {"person_id": 13, "org_id": 2, "title": "秦州区长",
     "start": "2021", "end": "2023", "rank": "县处级正职"},
    {"person_id": 13, "org_id": 6, "title": "天水市副市长",
     "start": "2023", "end": "present", "rank": "副厅级"},
]

# =========================================================================
# RELATIONSHIPS (person → person)
# =========================================================================

relationships = [
    # Current top leadership pair
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "区委书记↔区长：党委政府主要领导搭档",
     "overlap_org": "中共天水市秦州区委员会",
     "overlap_period": "2024-12至今",
     "strength": "strong"},

    # District party secretary ↔ predecessor (predecessor_successor)
    # 康泰来 succeeded 孟晓龙 as top leader of 秦州区 (康泰来 as 区委书记, 孟晓龙 had been 区长,
    # but 康泰来 came from outside - he was 副市长/麦积区委书记 before)
    {"person_a": 1, "person_b": 13, "type": "predecessor_successor",
     "context": "区领导交接：康泰来接替孟晓龙（孟曾任秦州区长，康任区委书记）",
     "overlap_org": "秦州区",
     "overlap_period": "2024",
     "strength": "medium"},

    # 王志成 ↔ 孟晓龙 (predecessor_successor for mayor role)
    {"person_a": 2, "person_b": 13, "type": "predecessor_successor",
     "context": "区长继任：王志成接替孟晓龙",
     "overlap_org": "秦州区人民政府",
     "overlap_period": "2024-12",
     "strength": "medium"},

    # 舒健 ↔ 毛更生 (四大班子同事)
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "区人大主任↔区政协主席：四大班子同事",
     "overlap_org": "秦州区",
     "overlap_period": "当前",
     "strength": "medium"},

    # 康泰来 ↔ 舒健
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "区委书记↔区人大主任",
     "overlap_org": "秦州区",
     "overlap_period": "当前",
     "strength": "medium"},

    # 王志成 ↔ 舒健
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "区长↔区人大主任",
     "overlap_org": "秦州区",
     "overlap_period": "当前",
     "strength": "medium"},

    # Key deputy relationships (under 康泰来)
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "区委书记↔区领导冯荣",
     "overlap_org": "中共天水市秦州区委员会",
     "overlap_period": "当前",
     "strength": "medium"},
]


# =========================================================================
# DATABASE BUILD
# =========================================================================

os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute("PRAGMA foreign_keys = ON;")

c.execute("""CREATE TABLE IF NOT EXISTS persons (
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
);""")

c.execute("""CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);""")

c.execute("""CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER,
    org_id INTEGER,
    title TEXT,
    start TEXT,
    end TEXT,
    rank TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);""")

c.execute("""CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER,
    person_b INTEGER,
    type TEXT,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    strength TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);""")

for p in persons:
    c.execute("""INSERT OR REPLACE INTO persons
        (id, name, gender, ethnicity, birth, birthplace, education,
         party_join, work_start, current_post, current_org, source)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
        (p["id"], p["name"], p.get("gender",""), p.get("ethnicity",""),
         p.get("birth",""), p.get("birthplace",""), p.get("education",""),
         p.get("party_join",""), p.get("work_start",""),
         p.get("current_post",""), p.get("current_org",""), p.get("source","")))

for o in organizations:
    c.execute("""INSERT OR REPLACE INTO organizations
        (id, name, type, level, parent, location)
        VALUES (?,?,?,?,?,?)""",
        (o["id"], o["name"], o.get("type",""), o.get("level",""),
         o.get("parent",""), o.get("location","")))

for pos in positions:
    c.execute("""INSERT INTO positions
        (person_id, org_id, title, start, end, rank)
        VALUES (?,?,?,?,?,?)""",
        (pos["person_id"], pos["org_id"], pos["title"],
         pos.get("start",""), pos.get("end",""), pos.get("rank","")))

for r in relationships:
    c.execute("""INSERT INTO relationships
        (person_a, person_b, type, context, overlap_org, overlap_period, strength)
        VALUES (?,?,?,?,?,?,?)""",
        (r["person_a"], r["person_b"], r["type"], r["context"],
         r.get("overlap_org",""), r.get("overlap_period",""), r.get("strength","")))

conn.commit()
conn.close()
print(f"✓ Database written: {DB_PATH}")


# =========================================================================
# GEXF BUILD
# =========================================================================

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Color by role."""
    post = p.get("current_post", "")
    if "区委书记" in post:
        return "255,50,50"
    elif "区长" in post:
        return "50,100,255"
    elif "副主任" in post or "主任" in post:
        return "200,255,255"
    elif "政协" in post or "主席" in post:
        return "255,240,200"
    else:
        return "100,100,100"

def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    elif "政府" in t:
        return "200,200,255"
    elif "人大" in t:
        return "200,255,255"
    elif "政协" in t:
        return "255,240,200"
    else:
        return "200,200,200"

def is_top_leader(p):
    post = p.get("current_post", "")
    return "书记" in post or "区长" in post

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Gov Relation Research Agent</creator>')
lines.append('    <description>秦州区（天水市）领导关系网络 — Party Secretary, District Mayor, leadership team</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="org" type="string"/>')
lines.append('    </attributes>')

lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('      <attribute id="2" title="strength" type="string"/>')
lines.append('    </attributes>')

# Person nodes
lines.append('    <nodes>')
for p in persons:
    c_ = person_color(p)
    sz = "20.0" if is_top_leader(p) else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c_.split(",")[0]}" g="{c_.split(",")[1]}" b="{c_.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Organization nodes
for o in organizations:
    c_ = org_color(o)
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value=""/>')
    lines.append(f'          <attvalue for="2" value="{esc(o.get("type",""))}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c_.split(",")[0]}" g="{c_.split(",")[1]}" b="{c_.split(",")[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
eid = 0

# Person → Organization (worked_at)
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
    lines.append('          <attvalue for="2" value="1.0"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

# Person ↔ Person (relationships)
for r in relationships:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(r.get("strength",""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"✓ GEXF written: {GEXF_PATH}")
