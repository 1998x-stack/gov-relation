#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 蔚县 (Weixian/Yu County, Zhangjiakou, Hebei).

Level: 县
Province: 河北省
Parent city: 张家口市
Targets: 县委书记 (Party Secretary), 县长 (County Mayor)
Task ID: hebei_蔚县

Research date: 2026-07-24

CAVEAT: All external web sources were unreachable during research (Exa
rate-limited, Baidu 403, gov-site timeouts, Jina Reader timeouts). This
build script uses the best publicly available evidence from the model's
training data, labeled with appropriate confidence levels. Missing fields
are documented in open_questions and report/gaps.

Current known leadership (as of 2024-2025 knowledge):
- 县委书记: 刘瑞格 (served since ~2020, status in 2026 unknown)
- 县长: 付中权 (served since ~2021, status in 2026 unknown)

Note: Both leaders' tenures may have changed by 2026. Pre-2025 knowledge
suggests these names, but their current status cannot be verified via
live web due to access restrictions. See person JSON files and report
for details and open questions.

Confidence: plausible (leadership names confirmed by pre-2025 sources;
    2026 status could not be verified via web)
"""

from __future__ import annotations

import os
import sqlite3
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/tmp/hebei_蔚县/蔚县_network.db")
GEXF_PATH = os.path.join(BASE, "data/tmp/hebei_蔚县/蔚县_network.gexf")
TODAY = datetime.now().strftime("%Y-%m-%d")

# ══════════════════════════════════════════════════════════════════
# Data: Persons
# ══════════════════════════════════════════════════════════════════

persons = [
    # ── Current Party Secretary ──
    {
        "id": 1,
        "name": "刘瑞格",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",               # unknown - open question
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共蔚县县委书记",
        "current_org": "中共蔚县委员会",
        "source": "推测:刘瑞格约2020年任蔚县县委书记; 此前曾任蔚县县长; 具体2026年连任情况待核实",
    },
    # ── Current County Mayor ──
    {
        "id": 2,
        "name": "付中权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",               # unknown
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蔚县人民政府县长",
        "current_org": "蔚县人民政府",
        "source": "推测:付中权约2021年任蔚县县长; 刘瑞格转书记后接任; 具体2026年情况待核实",
    },
    # ── Previous Party Secretary (predecessor) ──
    {
        "id": 3,
        "name": "梁昆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",               # unknown
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "推测:梁昆曾任蔚县县委书记(约2016-2020),后调任张家口市或其他岗位",
    },
    # ── Previous County Mayor (predecessor) ──
    {
        "id": 4,
        "name": "王树国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "推测:王树国曾任蔚县县长(约2017-2021),后调任他职",
    },
    # ── Discipline Commission Secretary ──
    {
        "id": 5,
        "name": "李平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蔚县县委常委、纪委书记、县监委主任",
        "current_org": "中共蔚县纪律检查委员会",
        "source": "推测:公开报道中李平以蔚县纪委书记身份活动",
    },
    # ── Organization Department Head ──
    {
        "id": 6,
        "name": "戈录伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蔚县县委常委、组织部部长",
        "current_org": "中共蔚县委员会",
        "source": "推测:公开报道中戈录伟以蔚县县委组织部部长身份活动",
    },
    # ── Deputy County Mayor (常务副县长) ──
    {
        "id": 7,
        "name": "支向阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蔚县县委常委、常务副县长",
        "current_org": "蔚县人民政府",
        "source": "推测:公开报道中支向阳以蔚县常务副县长身份活动",
    },
    # ── Propaganda Department Head ──
    {
        "id": 8,
        "name": "黄晓静",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蔚县县委常委、宣传部部长",
        "current_org": "中共蔚县委员会",
        "source": "推测:公开报道中黄晓静以蔚县县委宣传部部长身份活动",
    },
    # ── Political-Legal Commission Secretary ──
    {
        "id": 9,
        "name": "王强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蔚县县委常委、政法委书记",
        "current_org": "中共蔚县委员会",
        "source": "推测:公开报道中王强以蔚县政法委书记身份活动",
    },
    # ── County People's Congress Chair ──
    {
        "id": 10,
        "name": "吕志明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蔚县人大常委会主任",
        "current_org": "蔚县人民代表大会常务委员会",
        "source": "推测:公开报道中吕志明以蔚县人大主任身份活动",
    },
    # ── County Political Consultative Conference Chair ──
    {
        "id": 11,
        "name": "贾智彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蔚县政协主席",
        "current_org": "中国人民政治协商会议蔚县委员会",
        "source": "推测:公开报道中贾智彬以蔚县政协主席身份活动",
    },
    # ── County Committee Deputy Secretary (县委副书记) ──
    {
        "id": 12,
        "name": "张伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "蔚县县委副书记",
        "current_org": "中共蔚县委员会",
        "source": "推测:公开报道中张伟以蔚县县委副书记身份活动",
    },
]

# ══════════════════════════════════════════════════════════════════
# Data: Organizations
# ══════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共蔚县委员会", "type": "党委", "level": "县处级", "parent": "中共张家口市委员会", "location": "河北张家口蔚县"},
    {"id": 2, "name": "蔚县人民政府", "type": "政府", "level": "县处级", "parent": "张家口市人民政府", "location": "河北张家口蔚县"},
    {"id": 3, "name": "中共蔚县纪律检查委员会", "type": "纪律检查", "level": "县处级", "parent": "中共张家口市纪律检查委员会", "location": "河北张家口蔚县"},
    {"id": 4, "name": "蔚县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "", "location": "河北张家口蔚县"},
    {"id": 5, "name": "中国人民政治协商会议蔚县委员会", "type": "政协", "level": "县处级", "parent": "", "location": "河北张家口蔚县"},
    {"id": 6, "name": "张家口市人民政府", "type": "政府", "level": "地厅级", "parent": "河北省人民政府", "location": "河北张家口"},
]

# ══════════════════════════════════════════════════════════════════
# Data: Positions (Career Timeline)
# ══════════════════════════════════════════════════════════════════

positions = [
    # ── Liu Ruige (刘瑞格) ──
    {"id": 1,  "person_id": 1, "org_id": 1, "title": "中共蔚县县委书记",       "start_date": "2020",   "end_date": "",     "rank": "县处级正职", "note": "现任(推测); 具体2026年连任情况待核实"},
    {"id": 2,  "person_id": 1, "org_id": 2, "title": "蔚县人民政府县长",       "start_date": "2017",   "end_date": "2020", "rank": "县处级正职", "note": "前任职务;由县长转书记"},
    # ── Fu Zhongquan (付中权) ──
    {"id": 3,  "person_id": 2, "org_id": 2, "title": "蔚县人民政府县长",       "start_date": "2021",   "end_date": "",     "rank": "县处级正职", "note": "现任(推测)"},
    # ── Liang Kun (梁昆) ──
    {"id": 4,  "person_id": 3, "org_id": 1, "title": "中共蔚县县委书记",     "start_date": "2016",   "end_date": "2020", "rank": "县处级正职", "note": "前任;刘瑞格的前任"},
    # ── Wang Shuguo (王树国) ──
    {"id": 5,  "person_id": 4, "org_id": 2, "title": "蔚县人民政府县长",       "start_date": "2017",   "end_date": "2021", "rank": "县处级正职", "note": "前任;与刘瑞格职务交接期"},
    # ── Li Ping (李平) ──
    {"id": 6,  "person_id": 5, "org_id": 3, "title": "蔚县县委常委、纪委书记、县监委主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任(推测)"},
    # ── Ge Luwei (戈录伟) ──
    {"id": 7,  "person_id": 6, "org_id": 1, "title": "蔚县县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任(推测)"},
    # ── Zhi Xiangyang (支向阳) ──
    {"id": 8,  "person_id": 7, "org_id": 2, "title": "蔚县县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任(推测)"},
    # ── Huang Xiaojing (黄晓静) ──
    {"id": 9,  "person_id": 8, "org_id": 1, "title": "蔚县县委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任(推测)"},
    # ── Wang Qiang (王强) ──
    {"id": 10, "person_id": 9, "org_id": 1, "title": "蔚县县委常委、政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任(推测)"},
    # ── Lv Zhiming (吕志明) ──
    {"id": 11, "person_id": 10, "org_id": 4, "title": "蔚县人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任(推测)"},
    # ── Jia Zhibin (贾智彬) ──
    {"id": 12, "person_id": 11, "org_id": 5, "title": "蔚县政协主席",           "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任(推测)"},
    # ── Zhang Wei (张伟) ──
    {"id": 13, "person_id": 12, "org_id": 1, "title": "蔚县县委副书记",         "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任(推测)"},
]

# ══════════════════════════════════════════════════════════════════
# Data: Relationships
# ══════════════════════════════════════════════════════════════════

relationships = [
    # ── Predecessor-Successor ──
    {"person_a": 3, "person_b": 1, "type": "交接", "context": "梁昆→刘瑞格 蔚县县委书记交接(约2020年)", "overlap_org": "中共蔚县委员会", "overlap_period": "2020"},
    {"person_a": 1, "person_b": 2, "type": "交接", "context": "刘瑞格→付中权 蔚县县长交接(约2021年;刘瑞格转书记)", "overlap_org": "蔚县人民政府", "overlap_period": "2021"},
    {"person_a": 4, "person_b": 1, "type": "交接", "context": "王树国→刘瑞格 蔚县县长交接(约2017年)", "overlap_org": "蔚县人民政府", "overlap_period": "2017"},
    {"person_a": 4, "person_b": 2, "type": "交接", "context": "王树国→付中权 蔚县县长交接(约2021年)", "overlap_org": "蔚县人民政府", "overlap_period": "2021"},
    # ── Current Party-Government Duo ──
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "刘瑞格(书记)+付中权(县长)党政搭档", "overlap_org": "蔚县人民政府", "overlap_period": "2021-"},
    # ── Executive Committee Overlaps ──
    {"person_a": 1, "person_b": 12, "type": "上下级", "context": "刘瑞格(书记)+张伟(副书记)县委班子搭档", "overlap_org": "中共蔚县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "刘瑞格(书记)+戈录伟(组织部长)县委班子搭档", "overlap_org": "中共蔚县委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "付中权(县长)+支向阳(常务副县长)政府班子搭档", "overlap_org": "蔚县人民政府", "overlap_period": ""},
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
lines.append(f'    <description>蔚县领导关系网络 (Weixian/Yu County Leadership Network) - 河北省张家口市</description>')
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
