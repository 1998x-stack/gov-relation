#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 景东彝族自治县 leadership network.

NOTE: Web research was unavailable during this build (Exa rate-limited,
Baidu/Google blocked, Jina/Bing timeout, government sites unreachable).
Data is structurally valid but content is marked tentative.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/景东彝族自治县_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/景东彝族自治县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

# All data below is unverified. Names, titles, and organization structure
# are placeholders reflecting known county-level government structure.
# Web research was unavailable. See report/open_gaps.md for details.

persons = [
    {
        "id": 1,
        "name": "（县委书记待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共景东彝族自治县委员会",
        "source": "待查 - 公开信息来源不可用",
    },
    {
        "id": 2,
        "name": "（县长待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "景东彝族自治县人民政府",
        "source": "待查 - 公开信息来源不可用",
    },
    {
        "id": 3,
        "name": "（副书记待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共景东彝族自治县委员会",
        "source": "待查 - 公开信息来源不可用",
    },
    {
        "id": 4,
        "name": "（常务副县长待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "景东彝族自治县人民政府",
        "source": "待查 - 公开信息来源不可用",
    },
    {
        "id": 5,
        "name": "（纪委书记待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共景东彝族自治县纪律检查委员会",
        "source": "待查 - 公开信息来源不可用",
    },
    {
        "id": 6,
        "name": "（组织部长待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共景东彝族自治县委组织部",
        "source": "待查 - 公开信息来源不可用",
    },
    {
        "id": 7,
        "name": "（宣传部长待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共景东彝族自治县委宣传部",
        "source": "待查 - 公开信息来源不可用",
    },
    {
        "id": 8,
        "name": "（政法委书记待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共景东彝族自治县委政法委员会",
        "source": "待查 - 公开信息来源不可用",
    },
    {
        "id": 9,
        "name": "（统战部长待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共景东彝族自治县委统战部",
        "source": "待查 - 公开信息来源不可用",
    },
]

organizations = [
    {"id": 1, "name": "中共景东彝族自治县委员会", "type": "党委", "level": "县级", "parent": "中共普洱市委员会", "location": "云南省普洱市景东彝族自治县"},
    {"id": 2, "name": "景东彝族自治县人民政府", "type": "政府", "level": "县级", "parent": "普洱市人民政府", "location": "云南省普洱市景东彝族自治县"},
    {"id": 3, "name": "景东彝族自治县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "景东彝族自治县", "location": "云南省普洱市景东彝族自治县"},
    {"id": 4, "name": "中国人民政治协商会议景东彝族自治县委员会", "type": "政协", "level": "县级", "parent": "景东彝族自治县", "location": "云南省普洱市景东彝族自治县"},
    {"id": 5, "name": "中共景东彝族自治县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共景东彝族自治县委员会", "location": "云南省普洱市景东彝族自治县"},
    {"id": 6, "name": "中共景东彝族自治县委组织部", "type": "党委", "level": "县级", "parent": "中共景东彝族自治县委员会", "location": "云南省普洱市景东彝族自治县"},
    {"id": 7, "name": "中共景东彝族自治县委宣传部", "type": "党委", "level": "县级", "parent": "中共景东彝族自治县委员会", "location": "云南省普洱市景东彝族自治县"},
    {"id": 8, "name": "中共景东彝族自治县委政法委员会", "type": "党委", "level": "县级", "parent": "中共景东彝族自治县委员会", "location": "云南省普洱市景东彝族自治县"},
    {"id": 9, "name": "中共景东彝族自治县委统战部", "type": "党委", "level": "县级", "parent": "中共景东彝族自治县委员会", "location": "云南省普洱市景东彝族自治县"},
    {"id": 10, "name": "景东彝族自治县监察委员会", "type": "党委", "level": "县级", "parent": "景东彝族自治县", "location": "云南省普洱市景东彝族自治县"},
]

positions = [
    {"id": 1, "person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "", "rank": "正处级", "note": "待查"},
    {"id": 2, "person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start": "", "end": "", "rank": "正处级", "note": "待查"},
    {"id": 3, "person_id": 3, "org_id": 1, "title": "县委副书记", "start": "", "end": "", "rank": "副处级", "note": "待查"},
    {"id": 4, "person_id": 4, "org_id": 2, "title": "县委常委、常务副县长", "start": "", "end": "", "rank": "副处级", "note": "待查"},
    {"id": 5, "person_id": 5, "org_id": 5, "title": "县委常委、县纪委书记、县监委主任", "start": "", "end": "", "rank": "副处级", "note": "待查"},
    {"id": 6, "person_id": 6, "org_id": 6, "title": "县委常委、组织部部长", "start": "", "end": "", "rank": "副处级", "note": "待查"},
    {"id": 7, "person_id": 7, "org_id": 7, "title": "县委常委、宣传部部长", "start": "", "end": "", "rank": "副处级", "note": "待查"},
    {"id": 8, "person_id": 8, "org_id": 8, "title": "县委常委、政法委书记", "start": "", "end": "", "rank": "副处级", "note": "待查"},
    {"id": 9, "person_id": 9, "org_id": 9, "title": "县委常委、统战部部长", "start": "", "end": "", "rank": "副处级", "note": "待查"},
]

relationships = []


# ── HELPERS ──────────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")


def person_color(person):
    role = person.get("current_post", "")
    if "县委书记" in role:
        return "255,50,50"
    if "县长" in role and "副" not in role:
        return "50,100,255"
    if "纪委" in role or "监委" in role:
        return "255,165,0"
    if "副" in role:
        return "50,100,255"
    return "100,100,100"


def is_top_leader(p):
    role = p.get("current_post", "")
    return "县委书记" in role or ("县长" in role and "副" not in role)


def org_color(org_type):
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }.get(org_type, "200,200,200")


# ── BUILD DB ─────────────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY, person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY, person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],
             p["education"],p["party_join"],p["work_start"],p["current_post"],p["current_org"],p["source"]))

    for o in organizations:
        c.execute("INSERT OR REPLACE INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)",
            (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))

    for pos in positions:
        c.execute("INSERT OR REPLACE INTO positions (id,person_id,org_id,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?,?)",
            (pos["id"],pos["person_id"],pos["org_id"],pos["title"],pos["start"],pos["end"],pos["rank"],pos["note"]))

    for r in relationships:
        c.execute("INSERT OR REPLACE INTO relationships (id,person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?,?)",
            (r["id"],r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"DB: {DB_PATH}")
    print(f"  persons: {len(persons)}, orgs: {len(organizations)}, positions: {len(positions)}, relationships: {len(relationships)}")


# ── BUILD GEXF ───────────────────────────────────────────────────────

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus AI Research Agent</creator>')
    lines.append('    <description>景东彝族自治县领导班子工作关系网络（数据待验证）</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="title" type="string"/>')
    lines.append('    </attributes>')
    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p).split(",")
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # Org nodes
    for o in organizations:
        c = org_color(o["type"]).split(",")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("parent",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF: {GEXF_PATH}")
    print(f"  nodes: {len(persons)+len(organizations)}, edges: {eid}")


if __name__ == "__main__":
    build_db()
    build_gexf()
    print("Done. NOTE: All data is unverified — web research unavailable during build.")