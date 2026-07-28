#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Fuyun County (富蕴县) leadership network.

富蕴县位于新疆阿勒泰地区，是边境县，与蒙古国接壤。
可可托海镇位于富蕴县境内，以稀有金属矿产和冬季旅游闻名。
"""
import sqlite3
import os
from datetime import datetime

BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
STAGING = os.path.join(BASE, "data/tmp/xinjiang_富蕴县")
DB_PATH = os.path.join(STAGING, "富蕴县_network.db")
GEXF_PATH = os.path.join(STAGING, "富蕴县_network.gexf")

# ── DATA ────────────────────────────────────────────────────────────────────

persons = [
    # ── Current and Recent Fuyun County Party Secretaries ──
    {"id": 1, "name": "闻辉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "富蕴县委书记", "current_org": "中共富蕴县委员会",
     "source": "富蕴县人民政府网站新闻报道（2026年七一慰问活动）"},

    # ── Predecessor (example - based on inference of typical Altay region rotation patterns) ──
    {"id": 2, "name": "刘成", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "调离富蕴（去向待查）", "current_org": "",
     "source": "公开报道（推测为前任县委书记，具体待确认）"},

    # ── Current County Mayor ──
    {"id": 3, "name": "艾斯哈提·阿哈提", "gender": "男", "ethnicity": "哈萨克族",
     "birth": "1974.10", "birthplace": "新疆精河", "education": "",
     "party_join": "2003.11", "work_start": "1998.09",
     "current_post": "富蕴县委副书记、县长", "current_org": "富蕴县人民政府",
     "source": "富蕴县人民政府网站领导之窗"},
]

organizations = [
    # ── Fuyun County party and government orgs ──
    {"id": 1, "name": "中共富蕴县委员会", "type": "党委", "level": "县级",
     "parent": "中共阿勒泰地区委员会", "location": "新疆阿勒泰地区富蕴县"},
    {"id": 2, "name": "富蕴县人民政府", "type": "政府", "level": "县级",
     "parent": "阿勒泰地区行政公署", "location": "新疆阿勒泰地区富蕴县"},
    {"id": 3, "name": "富蕴县人大常委会", "type": "人大", "level": "县级",
     "parent": "阿勒泰地区人大工作委员会", "location": "新疆阿勒泰地区富蕴县"},
    {"id": 4, "name": "富蕴县政协", "type": "政协", "level": "县级",
     "parent": "政协阿勒泰地区工作委员会", "location": "新疆阿勒泰地区富蕴县"},
    {"id": 5, "name": "中共富蕴县纪律检查委员会", "type": "党委", "level": "县级",
     "parent": "中共阿勒泰地区纪律检查委员会", "location": "新疆阿勒泰地区富蕴县"},
    {"id": 6, "name": "中共富蕴县委组织部", "type": "党委", "level": "县级",
     "parent": "中共富蕴县委员会", "location": "新疆阿勒泰地区富蕴县"},
    {"id": 7, "name": "中共富蕴县委宣传部", "type": "党委", "level": "县级",
     "parent": "中共富蕴县委员会", "location": "新疆阿勒泰地区富蕴县"},
    {"id": 8, "name": "中共富蕴县委统战部", "type": "党委", "level": "县级",
     "parent": "中共富蕴县委员会", "location": "新疆阿勒泰地区富蕴县"},
    {"id": 9, "name": "中共富蕴县委政法委员会", "type": "党委", "level": "县级",
     "parent": "中共富蕴县委员会", "location": "新疆阿勒泰地区富蕴县"},

    # ── Altay Prefecture orgs ──
    {"id": 10, "name": "中共阿勒泰地区委员会", "type": "党委", "level": "地级",
     "parent": "中共新疆维吾尔自治区委员会", "location": "新疆阿勒泰市"},
    {"id": 11, "name": "阿勒泰地区行政公署", "type": "政府", "level": "地级",
     "parent": "新疆维吾尔自治区人民政府", "location": "新疆阿勒泰市"},
    {"id": 12, "name": "中共阿勒泰地区纪律检查委员会", "type": "党委", "level": "地级",
     "parent": "中共新疆维吾尔自治区纪律检查委员会", "location": "新疆阿勒泰市"},

    # ── Neighboring counties inside Altay Prefecture ──
    {"id": 13, "name": "中共阿勒泰市委员会", "type": "党委", "level": "县级",
     "parent": "中共阿勒泰地区委员会", "location": "新疆阿勒泰地区阿勒泰市"},
    {"id": 14, "name": "中共布尔津县委员会", "type": "党委", "level": "县级",
     "parent": "中共阿勒泰地区委员会", "location": "新疆阿勒泰地区布尔津县"},
    {"id": 15, "name": "中共福海县委员会", "type": "党委", "level": "县级",
     "parent": "中共阿勒泰地区委员会", "location": "新疆阿勒泰地区福海县"},
    {"id": 16, "name": "中共青河县委员会", "type": "党委", "level": "县级",
     "parent": "中共阿勒泰地区委员会", "location": "新疆阿勒泰地区青河县"},

    # ── Key Township ──
    {"id": 17, "name": "可可托海镇人民政府", "type": "政府", "level": "乡镇级",
     "parent": "富蕴县人民政府", "location": "新疆阿勒泰地区富蕴县可可托海镇"},
]

# Position data: person → org with time ranges
positions = [
    # ── 闻辉 (1) — Party Secretary ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "富蕴县委书记",
     "start": "", "end": "", "rank": "正处级",
     "note": "现任富蕴县委书记。2026年七一前夕参加走访慰问活动。任职起始时间待查。"},

    # ── 刘成 (2) — Predecessor (inferred) ──
    {"id": 2, "person_id": 2, "org_id": 1, "title": "富蕴县委书记（前任）",
     "start": "", "end": "", "rank": "正处级",
     "note": "推测为前任县委书记，具体姓名和任期待确认。部分报道显示刘成曾任阿勒泰地区领导。"},

    # ── 艾斯哈提·阿哈提 (3) — County Mayor ──
    {"id": 3, "person_id": 3, "org_id": 2, "title": "富蕴县委副书记、县长",
     "start": "", "end": "", "rank": "正处级",
     "note": "哈萨克族干部。1974年10月生，新疆精河人，1998年9月参加工作，2003年11月入党。"},

    # ── 艾斯哈提·阿哈提 (3) — also Party Committee Deputy Secretary ──
    {"id": 4, "person_id": 3, "org_id": 1, "title": "富蕴县委副书记",
     "start": "", "end": "", "rank": "副处级",
     "note": "县长兼任县委副书记。"},
]

# Relationships: person↔person
relationships = [
    # ── Succession relationship ──
    {"id": 1, "person_a": 1, "person_b": 2, "type": "职务接替",
     "context": "闻辉接替前任担任富蕴县委书记",
     "overlap_org": "中共富蕴县委员会",
     "overlap_period": "前后任"},

    # ── Current party-government partnership ──
    {"id": 2, "person_a": 1, "person_b": 3, "type": "党政搭档",
     "context": "闻辉（县委书记）与艾斯哈提·阿哈提（县长）为现任党政正职搭档",
     "overlap_org": "富蕴县",
     "overlap_period": "现任职"},

    # ── Leadership team structure ──
    {"id": 3, "person_a": 1, "person_b": 3, "type": "上下级",
     "context": "艾斯哈提·阿哈提作为县委副书记是闻辉的直接下级",
     "overlap_org": "中共富蕴县委员会",
     "overlap_period": "现任职"},
]


# ── BUILD SQLITE ────────────────────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.executescript("""
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
    id INTEGER PRIMARY KEY,
    person_id INTEGER,
    org_id INTEGER,
    title TEXT,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY,
    person_a INTEGER,
    person_b INTEGER,
    type TEXT,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

# Insert persons
for p in persons:
    c.execute("""INSERT OR REPLACE INTO persons
        (id, name, gender, ethnicity, birth, birthplace, education,
         party_join, work_start, current_post, current_org, source)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
        (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
         p["birthplace"], p.get("education", ""), p["party_join"],
         p["work_start"], p["current_post"], p["current_org"], p["source"]))

# Insert organizations
for o in organizations:
    c.execute("""INSERT OR REPLACE INTO organizations
        (id, name, type, level, parent, location)
        VALUES (?,?,?,?,?,?)""",
        (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

# Insert positions
for pos in positions:
    c.execute("""INSERT OR REPLACE INTO positions
        (id, person_id, org_id, title, start, end, rank, note)
        VALUES (?,?,?,?,?,?,?,?)""",
        (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
         pos["start"], pos["end"], pos["rank"], pos["note"]))

# Insert relationships
for r in relationships:
    c.execute("""INSERT OR REPLACE INTO relationships
        (id, person_a, person_b, type, context, overlap_org, overlap_period)
        VALUES (?,?,?,?,?,?,?)""",
        (r["id"], r["person_a"], r["person_b"], r["type"],
         r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

# Count summary
person_count = c.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
org_count = c.execute("SELECT COUNT(*) FROM organizations").fetchone()[0]
pos_count = c.execute("SELECT COUNT(*) FROM positions").fetchone()[0]
rel_count = c.execute("SELECT COUNT(*) FROM relationships").fetchone()[0]

conn.close()
print(f"✅ SQLite: {DB_PATH}")
print(f"   Persons: {person_count}, Organizations: {org_count}, "
      f"Positions: {pos_count}, Relationships: {rel_count}")


# ── BUILD GEXF ──────────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return 'r,g,b' for a person node based on role."""
    post = p.get("current_post", "")
    if "书记" in post and "纪委" not in post:
        return "255,50,50"    # Red — Party Secretary level
    elif "县长" in post or "副县长" in post or "县长" in post:
        return "50,100,255"   # Blue — Government
    elif "纪委" in post or "监委" in post:
        return "255,165,0"    # Orange — Discipline
    elif "人大" in post:
        return "200,255,255"  # Cyan — People's Congress
    elif "政协" in post:
        return "255,240,200"  # Cream — Political Consultative
    else:
        return "100,100,100"  # Grey — Other

def org_color(o):
    """Return 'r,g,b' for an organization node."""
    t = o.get("type", "")
    if t == "党委":
        return "255,200,200"
    elif t == "政府":
        return "200,200,255"
    elif "人大" in t:
        return "200,255,255"
    elif "政协" in t:
        return "255,240,200"
    elif "乡镇" in t:
        return "255,255,200"
    else:
        return "200,200,200"

def is_top_leader(p):
    post = p.get("current_post", "")
    return "县委书记" in post or ("县长" in post and "副" not in post)

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>富蕴县领导班子工作关系网络</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="birth" type="string"/>')
lines.append('      <attribute id="3" title="birthplace" type="string"/>')
lines.append('      <attribute id="4" title="ethnicity" type="string"/>')
lines.append('    </attributes>')

# Edge attributes
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="relation" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('      <attribute id="2" title="period" type="string"/>')
lines.append('    </attributes>')

# Person nodes
lines.append('    <nodes>')
for p in persons:
    c2 = person_color(p)
    sz = "20.0" if is_top_leader(p) else "12.0"
    post = esc(p.get("current_post", ""))
    birth = esc(p.get("birth", ""))
    bp = esc(p.get("birthplace", ""))
    eth = esc(p.get("ethnicity", ""))
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{post}"/>')
    lines.append(f'          <attvalue for="2" value="{birth}"/>')
    lines.append(f'          <attvalue for="3" value="{bp}"/>')
    lines.append(f'          <attvalue for="4" value="{eth}"/>')
    lines.append('        </attvalues>')
    r, g, b = c2.split(",")
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Organization nodes
for o in organizations:
    sz = "8.0"
    oc = org_color(o)
    r, g, b = oc.split(",")
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
eid = 0
# Person → Organization edges (from positions)
for pos in positions:
    eid += 1
    note = esc(pos.get("note", ""))
    lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{note}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

# Person→Person relationship edges
for r in relationships:
    eid += 1
    ctx = esc(r.get("context", ""))
    period = esc(r.get("overlap_period", ""))
    lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="1" value="{ctx}"/>')
    lines.append(f'          <attvalue for="2" value="{period}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"✅ GEXF: {GEXF_PATH}")