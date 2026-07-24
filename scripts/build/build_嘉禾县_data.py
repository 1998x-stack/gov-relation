#!/usr/bin/env python3
"""嘉禾县领导班子工作关系网络 — 数据构建脚本

Task: hunan_嘉禾县
Province: 湖南省
Parent City: 郴州市
Region: 嘉禾县
Level: 县
Targets: 县委书记 & 县长
Data as of: 2025-12 (Baidu Baike)

Research Sources:
  - Baidu Baike: 嘉禾县条目 (主要领导表, 截至2025年12月)
  - Baidu Baike: 嘉禾县条目 (四大班子主要领导)
  - Sogou/360 search results for biographical details

Confidence Note: Web access was severely degraded. Core leadership confirmed
from Baidu Baike. Detailed career histories for 何勇 and 贺理 were not
retrievable from blocked sources. Open questions documented in person JSON.
"""

import os
import sqlite3

# ══════════════════════════════════════════════════════════════════════════
# Paths
# ══════════════════════════════════════════════════════════════════════════

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AS_OF = "2026-07-25"
DB_PATH = os.path.join(BASE_DIR, "嘉禾县_network.db")
GEXF_PATH = os.path.join(BASE_DIR, "嘉禾县_network.gexf")

# ══════════════════════════════════════════════════════════════════════════
# Data: Persons
# ══════════════════════════════════════════════════════════════════════════

persons = [
    {
        "id": "p1",
        "name": "何勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "湖南省永州市",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "嘉禾县委书记",
        "current_org": "中共嘉禾县委",
        "source": "Baidu Baike 嘉禾县条目、Sogou搜索结果（'这位永州人任郴州市嘉禾县委书记'）",
        "notes": "履历完全缺失——来源仅为新闻报道标题提及'31岁任副处级领导'和'永州人'"
    },
    {
        "id": "p2",
        "name": "贺理",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "嘉禾县委副书记、县人民政府县长、党组书记",
        "current_org": "嘉禾县人民政府",
        "source": "Baidu Baike 嘉禾县条目、Baidu Baike 多义词'贺理'",
        "notes": "履历完全缺失——Baidu Baike多义词页面标记有'湖南省嘉禾县委副书记、县人民政府县长、党组书记'义项，但详情页面跳转至其他同名人物"
    },
    {
        "id": "p3",
        "name": "李资兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "嘉禾县人大常委会主任",
        "current_org": "嘉禾县人大常委会",
        "source": "Baidu Baike 嘉禾县条目（主要领导表）",
        "notes": "仅知姓名和职务，其他信息缺失"
    },
    {
        "id": "p4",
        "name": "何翔凤",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "嘉禾县政协主席",
        "current_org": "嘉禾县政协",
        "source": "Baidu Baike 嘉禾县条目（主要领导表）",
        "notes": "仅知姓名和职务，其他信息缺失"
    },
]

# ══════════════════════════════════════════════════════════════════════════
# Data: Organizations
# ══════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共嘉禾县委", "type": "党委", "level": "县处级", "parent": "中共郴州市委", "location": "湖南省郴州市嘉禾县"},
    {"id": 2, "name": "嘉禾县人民政府", "type": "政府", "level": "县处级", "parent": "郴州市人民政府", "location": "湖南省郴州市嘉禾县"},
    {"id": 3, "name": "嘉禾县人大常委会", "type": "人大", "level": "县处级", "parent": "嘉禾县", "location": "湖南省郴州市嘉禾县"},
    {"id": 4, "name": "嘉禾县政协", "type": "政协", "level": "县处级", "parent": "嘉禾县", "location": "湖南省郴州市嘉禾县"},
]

# ══════════════════════════════════════════════════════════════════════════
# Data: Positions
# ══════════════════════════════════════════════════════════════════════════

positions = [
    # 何勇
    {"person_id": "p1", "org_id": 1, "title": "嘉禾县委书记", "start": "", "end": "present", "rank": "正处级", "note": "截至2025年12月在任"},
    # 贺理
    {"person_id": "p2", "org_id": 2, "title": "嘉禾县委副书记、县人民政府县长、党组书记", "start": "", "end": "present", "rank": "正处级", "note": "截至2025年12月在任"},
    # 李资兵
    {"person_id": "p3", "org_id": 3, "title": "嘉禾县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": "截至2025年12月在任"},
    # 何翔凤
    {"person_id": "p4", "org_id": 4, "title": "嘉禾县政协主席", "start": "", "end": "present", "rank": "正处级", "note": "截至2025年12月在任"},
]

# ══════════════════════════════════════════════════════════════════════════
# Data: Relationships
# ══════════════════════════════════════════════════════════════════════════

relationships = [
    {
        "person_a": "p1",
        "person_b": "p2",
        "type": "superior_subordinate",
        "context": "何勇（县委书记）与贺理（县长）为嘉禾县党政正职搭档关系",
        "overlap_org": "嘉禾县",
        "overlap_period": "截至2025年12月",
        "confidence": "confirmed"
    },
    {
        "person_a": "p1",
        "person_b": "p3",
        "type": "superior_subordinate",
        "context": "何勇（县委书记）与李资兵（人大常委会主任）为县领导班子成员",
        "overlap_org": "嘉禾县",
        "overlap_period": "截至2025年12月",
        "confidence": "confirmed"
    },
    {
        "person_a": "p1",
        "person_b": "p4",
        "type": "superior_subordinate",
        "context": "何勇（县委书记）与何翔凤（政协主席）为县领导班子成员",
        "overlap_org": "嘉禾县",
        "overlap_period": "截至2025年12月",
        "confidence": "confirmed"
    },
    {
        "person_a": "p2",
        "person_b": "p3",
        "type": "superior_subordinate",
        "context": "贺理（县长）与李资兵（人大常委会主任）为县领导班子成员",
        "overlap_org": "嘉禾县",
        "overlap_period": "截至2025年12月",
        "confidence": "confirmed"
    },
    {
        "person_a": "p2",
        "person_b": "p4",
        "type": "superior_subordinate",
        "context": "贺理（县长）与何翔凤（政协主席）为县领导班子成员",
        "overlap_org": "嘉禾县",
        "overlap_period": "截至2025年12月",
        "confidence": "confirmed"
    },
    {
        "person_a": "p3",
        "person_b": "p4",
        "type": "superior_subordinate",
        "context": "李资兵（人大常委会主任）与何翔凤（政协主席）为县领导班子成员",
        "overlap_org": "嘉禾县",
        "overlap_period": "截至2025年12月",
        "confidence": "confirmed"
    },
]

# ══════════════════════════════════════════════════════════════════════════
# SQLite DB Builder
# ══════════════════════════════════════════════════════════════════════════

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for t in ("relationships", "positions", "organizations", "persons"):
        cur.execute(f"DROP TABLE IF EXISTS {t}")

    cur.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT,
        notes TEXT
    )""")
    cur.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    cur.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER,
        title TEXT, start TEXT, end TEXT,
        rank TEXT, note TEXT
    )""")
    cur.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        confidence TEXT DEFAULT 'unverified'
    )""")

    def pid(s):
        return int(s[1:])

    for p in persons:
        cur.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (pid(p["id"]), p["name"], p.get("gender", ""), p.get("ethnicity", ""),
                     p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
                     p.get("party_join", ""), p.get("work_start", ""),
                     p["current_post"], p["current_org"], p.get("source", ""),
                     p.get("notes", "")))
    for o in organizations:
        cur.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                    (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        cur.execute("INSERT INTO positions (person_id,org_id,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?)",
                    (pid(pos["person_id"]), pos["org_id"], pos["title"],
                     pos.get("start", ""), pos.get("end", ""),
                     pos.get("rank", ""), pos.get("note", "")))
    for r in relationships:
        cur.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period,confidence) VALUES (?,?,?,?,?,?,?)",
                    (pid(r["person_a"]), pid(r["person_b"]), r["type"], r["context"],
                     r["overlap_org"], r["overlap_period"], r.get("confidence", "unverified")))

    conn.commit()
    conn.close()
    print(f"  DB: {DB_PATH} ({len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships)")

# ══════════════════════════════════════════════════════════════════════════
# GEXF Graph Builder
# ══════════════════════════════════════════════════════════════════════════

esc = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;") if s is not None else ""

def person_color(post):
    if "县委书记" in post and "副" not in post:
        return ("255,50,50", 20.0)
    elif "县长" in post and "副" not in post:
        return ("50,100,255", 20.0)
    elif "人大" in post:
        return ("200,255,255", 12.0)
    elif "政协" in post:
        return ("255,240,200", 12.0)
    else:
        return ("100,100,100", 12.0)

org_colors_map = {
    "党委": ("255,200,200", 8.0),
    "政府": ("200,200,255", 8.0),
    "人大": ("200,255,255", 8.0),
    "政协": ("255,240,200", 8.0),
}

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append(f'    <description>嘉禾县领导班子关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c, sz = person_color(p["current_post"])
        nid = f"p{int(p['id'][1:])}"
        lines.append(f'      <node id="{nid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # Organization nodes
    for o in organizations:
        c, sz = org_colors_map.get(o["type"], ("200,200,200", 8.0))
        nid = f"o{o['id']}"
        lines.append(f'      <node id="{nid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person -> Organization
    for pos in positions:
        eid += 1
        pid_val = f"p{int(pos['person_id'][1:])}"
        nid = f"o{pos['org_id']}"
        lines.append(f'      <edge id="{eid}" source="{pid_val}" target="{nid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    # Person <-> Person
    for r in relationships:
        eid += 1
        pid_a = f"p{int(r['person_a'][1:])}"
        pid_b = f"p{int(r['person_b'][1:])}"
        lines.append(f'      <edge id="{eid}" source="{pid_a}" target="{pid_b}" label="{esc(r["type"])}" weight="2.0">')
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
    print(f"  GEXF: {GEXF_PATH}")

# ══════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    build_db()
    build_gexf()
    print(f"\n{'='*60}")
    print(f"嘉禾县 Network Build Complete")
    print(f"{'='*60}")
    print(f"Persons:     {len(persons)}")
    print(f"Orgs:        {len(organizations)}")
    print(f"Positions:   {len(positions)}")
    print(f"Edges:       {len(positions) + len(relationships)}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")
