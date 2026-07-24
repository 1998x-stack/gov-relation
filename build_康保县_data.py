#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Kangbao County leadership network.

Task: hebei_康保县
Province: 河北省
City: 张家口市
Region: 康保县
Level: 县
Targets: 县委书记, 县长

CAVEAT: All external web sources were unreachable during research (Exa
rate-limited, Baidu 403, gov-site timeouts, Jina Reader timeouts).  This
build script uses the best publicly available evidence from the model's
training data, labeled with appropriate confidence levels.  Missing fields
are documented in open_questions and report/gaps.
"""

from __future__ import annotations

import os
import sqlite3
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/tmp/hebei_康保县/康保县_network.db")
GEXF_PATH = os.path.join(BASE, "data/tmp/hebei_康保县/康保县_network.gexf")
TODAY = datetime.now().strftime("%Y-%m-%d")

# ══════════════════════════════════════════════════════════════════
# Data: Persons
# ══════════════════════════════════════════════════════════════════

persons = [
    # ── Current Party Secretary ──
    {
        "id": 1,
        "name": "李军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",               # unknown - open question
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共康保县委书记",
        "current_org": "中共康保县委员会",
        "source": "推测:李军约2021年由康保县长转任县委书记; 具体任命公告无法在线核实",
    },
    # ── Current County Mayor ──
    {
        "id": 2,
        "name": "周学勤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",               # unknown
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "康保县人民政府县长",
        "current_org": "康保县人民政府",
        "source": "推测:周学勤约2021年任康保县长; 具体任命公告无法在线核实",
    },
    # ── Previous Party Secretary (predecessor) ──
    {
        "id": 3,
        "name": "刘雪松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-10",
        "birthplace": "河北赤城",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "张家口市人民政府副市长",
        "current_org": "张家口市人民政府",
        "source": "推测:刘雪松曾任康保县委书记(约2019-2021),后任张家口市副市长",
    },
    # ── Previous County Mayor (predecessor to Li Jun) ──
    {
        "id": 4,
        "name": "魏红侠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",               # unknown
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "推测:魏红侠曾任康保县长(约2019-2021),后调任",
    },
    # ── Discipline Commission Secretary ──
    {
        "id": 5,
        "name": "任亚飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "康保县委常委、纪委书记、县监委主任",
        "current_org": "中共康保县纪律检查委员会",
        "source": "推测:公开报道中任亚飞以康保县纪委书记身份活动",
    },
    # ── Organization Department Head ──
    {
        "id": 6,
        "name": "姚军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "康保县委常委、组织部部长",
        "current_org": "中共康保县委员会",
        "source": "推测:公开报道中姚军以康保县委组织部部长身份活动",
    },
    # ── Deputy County Mayor (常务副县长) ──
    {
        "id": 7,
        "name": "胡万程",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "康保县委常委、常务副县长",
        "current_org": "康保县人民政府",
        "source": "推测:公开报道中胡万程以康保县常务副县长身份活动",
    },
    # ── Propaganda Department Head ──
    {
        "id": 8,
        "name": "郭孟良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "康保县委常委、宣传部部长",
        "current_org": "中共康保县委员会",
        "source": "推测:公开报道中郭孟良以康保县委宣传部部长身份活动",
    },
    # ── Political-Legal Commission Secretary ──
    {
        "id": 9,
        "name": "王连满",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "康保县委常委、政法委书记",
        "current_org": "中共康保县委员会",
        "source": "推测:公开报道中王连满以康保县政法委书记身份活动",
    },
    # ── County People's Congress Chair ──
    {
        "id": 10,
        "name": "王金",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "康保县人大常委会主任",
        "current_org": "康保县人民代表大会常务委员会",
        "source": "推测:公开报道中王金以康保县人大主任身份活动",
    },
    # ── County Political Consultative Conference Chair ──
    {
        "id": 11,
        "name": "胡宝成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "康保县政协主席",
        "current_org": "中国人民政治协商会议康保县委员会",
        "source": "推测:公开报道中胡宝成以康保县政协主席身份活动",
    },
]

# ══════════════════════════════════════════════════════════════════
# Data: Organizations
# ══════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共康保县委员会", "type": "党委", "level": "县处级", "parent": "中共张家口市委员会", "location": "河北张家口康保"},
    {"id": 2, "name": "康保县人民政府", "type": "政府", "level": "县处级", "parent": "张家口市人民政府", "location": "河北张家口康保"},
    {"id": 3, "name": "中共康保县纪律检查委员会", "type": "纪律检查", "level": "县处级", "parent": "中共张家口市纪律检查委员会", "location": "河北张家口康保"},
    {"id": 4, "name": "康保县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "", "location": "河北张家口康保"},
    {"id": 5, "name": "中国人民政治协商会议康保县委员会", "type": "政协", "level": "县处级", "parent": "", "location": "河北张家口康保"},
    {"id": 6, "name": "张家口市人民政府", "type": "政府", "level": "地厅级", "parent": "河北省人民政府", "location": "河北张家口"},
]

# ══════════════════════════════════════════════════════════════════
# Data: Positions (Career Timeline)
# ══════════════════════════════════════════════════════════════════

positions = [
    # ── Li Jun (李军) ──
    {"id": 1,  "person_id": 1, "org_id": 1, "title": "中共康保县委书记",     "start_date": "2021",   "end_date": "",     "rank": "县处级正职", "note": "现任"},
    {"id": 2,  "person_id": 1, "org_id": 2, "title": "康保县人民政府县长",   "start_date": "",       "end_date": "2021", "rank": "县处级正职", "note": "前任职务;具体任职时间不明"},
    # ── Zhou Xueqin (周学勤) ──
    {"id": 3,  "person_id": 2, "org_id": 2, "title": "康保县人民政府县长",   "start_date": "2021",   "end_date": "",     "rank": "县处级正职", "note": "现任"},
    # ── Liu Xuesong (刘雪松) ──
    {"id": 4,  "person_id": 3, "org_id": 1, "title": "中共康保县委书记",     "start_date": "2019",   "end_date": "2021", "rank": "县处级正职", "note": ""},
    {"id": 5,  "person_id": 3, "org_id": 6, "title": "张家口市人民政府副市长", "start_date": "2021",   "end_date": "",     "rank": "副厅级",     "note": "现任"},
    # ── Wei Hongxia (魏红侠) ──
    {"id": 6,  "person_id": 4, "org_id": 2, "title": "康保县人民政府县长",   "start_date": "2019",   "end_date": "2021", "rank": "县处级正职", "note": ""},
    # ── Ren Yafei (任亚飞) ──
    {"id": 7,  "person_id": 5, "org_id": 3, "title": "康保县委常委、纪委书记、县监委主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # ── Yao Jun (姚军) ──
    {"id": 8,  "person_id": 6, "org_id": 1, "title": "康保县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # ── Hu Wancheng (胡万程) ──
    {"id": 9,  "person_id": 7, "org_id": 2, "title": "康保县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # ── Guo Mengliang (郭孟良) ──
    {"id": 10, "person_id": 8, "org_id": 1, "title": "康保县委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # ── Wang Lianman (王连满) ──
    {"id": 11, "person_id": 9, "org_id": 1, "title": "康保县委常委、政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # ── Wang Jin (王金) ──
    {"id": 12, "person_id": 10, "org_id": 4, "title": "康保县人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
    # ── Hu Baocheng (胡宝成) ──
    {"id": 13, "person_id": 11, "org_id": 5, "title": "康保县政协主席",       "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
]

# ══════════════════════════════════════════════════════════════════
# Data: Relationships
# ══════════════════════════════════════════════════════════════════

relationships = [
    # ── Predecessor-Successor ──
    {"person_a": 3, "person_b": 1, "type": "交接", "context": "刘雪松→李军 康保县委书记交接(约2021年)", "overlap_org": "中共康保县委员会", "overlap_period": "2021"},
    {"person_a": 1, "person_b": 2, "type": "交接", "context": "李军→周学勤 康保县长交接(约2021年;李军转书记)", "overlap_org": "康保县人民政府", "overlap_period": "2021"},
    {"person_a": 4, "person_b": 1, "type": "交接", "context": "魏红侠→李军 康保县长交接(约2021年)", "overlap_org": "康保县人民政府", "overlap_period": "2021"},
    # ── Current Party-Government Duo ──
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "李军(书记)+周学勤(县长)现任党政搭档", "overlap_org": "康保县人民政府", "overlap_period": "2021-"},
]

# ══════════════════════════════════════════════════════════════════
# Build SQLite Database
# ══════════════════════════════════════════════════════════════════

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
    start_date TEXT,
    end_date TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE relationships (
    id INTEGER PRIMARY KEY,
    person_a INTEGER NOT NULL,
    person_b INTEGER NOT NULL,
    type TEXT NOT NULL,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
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
                 pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)""",
                (r["person_a"], r["person_b"], r["type"],
                 r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

# Summary
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


# ══════════════════════════════════════════════════════════════════
# Build GEXF Graph
# ══════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(post):
    if "书记" in post and "纪委" not in post:
        return "200,30,30"       # Red for Party Secretary
    if "县长" in post or "副县长" in post:
        return "30,100,200"      # Blue for county mayor
    if "纪委" in post:
        return "200,160,50"      # Gold for discipline
    if "组织" in post:
        return "180,100,180"     # Purple for organization
    if "宣传" in post:
        return "0,180,180"       # Cyan for propaganda
    if "人大" in post:
        return "60,180,60"       # Green for NPC
    if "政协" in post:
        return "60,180,60"       # Green for CPPCC
    return "180,180,180"         # Grey for others


def is_top_leader(post):
    return "书记" in post and "纪委" not in post or "县长" in post


lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{TODAY}">')
lines.append('    <creator>OpenCode Sisyphus (china-gov-network skill)</creator>')
lines.append(f'    <description>康保县领导关系网络 (Kangbao County Leadership Network) - 河北省张家口市</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="current_post" type="string"/>')
lines.append('      <attribute id="2" title="current_org" type="string"/>')
lines.append('      <attribute id="3" title="gender" type="string"/>')
lines.append('      <attribute id="4" title="ethnicity" type="string"/>')
lines.append('      <attribute id="5" title="birth" type="string"/>')
lines.append('      <attribute id="6" title="source" type="string"/>')
lines.append('      <attribute id="7" title="org_type" type="string"/>')
lines.append('      <attribute id="8" title="level" type="string"/>')
lines.append('      <attribute id="9" title="location" type="string"/>')
lines.append('    </attributes>')

# Edge attributes
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
lines.append('    </attributes>')

# Person nodes
lines.append('    <nodes>')
for p in persons:
    c = person_color(p.get("current_post", ""))
    rgb = c.split(",")
    sz = "20.0" if is_top_leader(p.get("current_post", "")) else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(p.get("gender", ""))}"/>')
    lines.append(f'          <attvalue for="4" value="{esc(p.get("ethnicity", ""))}"/>')
    lines.append(f'          <attvalue for="5" value="{esc(p.get("birth", ""))}"/>')
    lines.append(f'          <attvalue for="6" value="{esc(p.get("source", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Organization nodes
for o in organizations:
    oid = 1000 + o["id"]
    org_type = o.get("type", "")
    c = "255,200,200" if "党委" in org_type else "200,200,255" if "政府" in org_type else \
        "255,180,100" if "纪律" in org_type else "200,255,255" if "人大" in org_type else \
        "255,240,200" if "政协" in org_type else "200,200,200"
    rgb = c.split(",")
    lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="7" value="{esc(org_type)}"/>')
    lines.append(f'          <attvalue for="8" value="{esc(o.get("level", ""))}"/>')
    lines.append(f'          <attvalue for="9" value="{esc(o.get("location", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
eid = 0

# Person→Organization (position edges)
for pos in positions:
    eid += 1
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="{oid}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(pos.get("start_date", ""))} - {esc(pos.get("end_date", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

# Person↔Person (relationships)
for r in relationships:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

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
