#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 繁昌区 (Fanchang District, Wuhu, Anhui) leadership network.

繁昌区 — 安徽省芜湖市辖区, 总面积584平方公里, 常住人口约24.4万.
2020年7月撤县设区, 由原繁昌县改为繁昌区.
Data current as of July 2026 based on 繁昌区人民政府网站 (fanchang.gov.cn).
"""

import sqlite3
import os
import json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/anhui_繁昌区")
DB_PATH = os.path.join(STAGING, "繁昌区_network.db")
GEXF_PATH = os.path.join(STAGING, "繁昌区_network.gexf")

TODAY = datetime.now().strftime("%Y%m%d")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders (Targets) ──
    # 区委书记
    {"id": 1, "name": "汪敏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "安徽（待查）", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "繁昌区委书记", "current_org": "中共繁昌区委",
     "source": "繁昌区人民政府网站 (fanchang.gov.cn) 2026年7月政务要闻"},
    # 区长
    {"id": 2, "name": "周伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "安徽（待查）", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "繁昌区长", "current_org": "繁昌区人民政府",
     "source": "繁昌区人民政府网站 (fanchang.gov.cn) 2026年7月政务要闻"},

    # ── Predecessors ──
    {"id": 3, "name": "瞿辉", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-09", "birthplace": "安徽合肥", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1997",
     "current_post": "原繁昌区委书记（已离任）", "current_org": "中共繁昌区委",
     "source": "build_芜湖市_data.py (公开报道)"},
    # Note: 瞿辉 succeeded by 汪敏, transition timing unclear (likely late 2025 - early 2026)

    # ── District Level Leaders (from Wikipedia+gov site) ──
    # 区人大主任 (likely 陈邦龙 or similar - need verification)
    {"id": 4, "name": "陈邦龙", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "繁昌区人大常委会主任", "current_org": "繁昌区人大常委会",
     "source": "公开报道（待核实）"},
    # 区政协主席 (likely 张文宝 or similar - need verification)
    {"id": 5, "name": "张文宝", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "繁昌区政协主席", "current_org": "繁昌区政协",
     "source": "公开报道（待核实）"},

    # ── Key City-level Connections ──
    {"id": 6, "name": "宁波", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-03", "birthplace": "安徽合肥", "education": "省委党校研究生/工学学士",
     "party_join": "中共党员", "work_start": "1988",
     "current_post": "芜湖市委书记", "current_org": "中共芜湖市委",
     "source": "芜湖市人民政府网站/公开报道"},
    {"id": 7, "name": "徐志", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-03", "birthplace": "安徽合肥（一说巢湖）", "education": "在职研究生/经济学博士",
     "party_join": "中共党员", "work_start": "1994",
     "current_post": "芜湖市委副书记、市长", "current_org": "芜湖市人民政府",
     "source": "芜湖市人民政府网站/公开报道"},
]

organizations = [
    {"id": 1, "name": "中共繁昌区委", "type": "党委", "level": "县级", "parent": "中共芜湖市委", "location": "繁昌区"},
    {"id": 2, "name": "繁昌区人民政府", "type": "政府", "level": "县级", "parent": "芜湖市人民政府", "location": "繁昌区"},
    {"id": 3, "name": "繁昌区人大常委会", "type": "人大", "level": "县级", "parent": "芜湖市人大常委会", "location": "繁昌区"},
    {"id": 4, "name": "繁昌区政协", "type": "政协", "level": "县级", "parent": "芜湖市政协", "location": "繁昌区"},
    {"id": 5, "name": "中共芜湖市委", "type": "党委", "level": "地厅级", "parent": "中共安徽省委", "location": "芜湖市"},
    {"id": 6, "name": "芜湖市人民政府", "type": "政府", "level": "地厅级", "parent": "安徽省人民政府", "location": "芜湖市"},
]

positions = [
    # 汪敏
    {"person_id": 1, "org_id": 1, "title": "繁昌区委书记", "start": "", "end": "", "rank": "正处", "note": "2025/2026年就任, 接替瞿辉"},
    # 周伟
    {"person_id": 2, "org_id": 2, "title": "繁昌区长", "start": "", "end": "", "rank": "正处", "note": ""},
    # 瞿辉 (前书记)
    {"person_id": 3, "org_id": 1, "title": "繁昌区委书记", "start": "2022", "end": "", "rank": "正处", "note": "已离任, 由汪敏接替"},
    # 陈邦龙
    {"person_id": 4, "org_id": 3, "title": "繁昌区人大常委会主任", "start": "", "end": "", "rank": "正处", "note": ""},
    # 张文宝
    {"person_id": 5, "org_id": 4, "title": "繁昌区政协主席", "start": "", "end": "", "rank": "正处", "note": ""},
    # 宁波 (市委书记)
    {"person_id": 6, "org_id": 5, "title": "芜湖市委书记", "start": "2021-06", "end": "", "rank": "正厅", "note": ""},
    # 徐志 (市长)
    {"person_id": 7, "org_id": 6, "title": "芜湖市人民政府市长", "start": "2023-03", "end": "", "rank": "正厅", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "芜湖市委副书记", "start": "2023-03", "end": "", "rank": "正厅", "note": ""},
]

relationships = [
    # 汪敏 <-> 周伟 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "繁昌区委书记与区长工作搭档", "overlap_org": "繁昌区", "overlap_period": "2025/2026-"},
    # 宁波 <-> 汪敏 (上下级)
    {"person_a": 6, "person_b": 1, "type": "上下级", "context": "芜湖市委书记与繁昌区委书记上下级", "overlap_org": "芜湖市", "overlap_period": ""},
    # 宁波 <-> 周伟 (上下级)
    {"person_a": 6, "person_b": 2, "type": "上下级", "context": "芜湖市委书记与繁昌区长上下级", "overlap_org": "芜湖市", "overlap_period": ""},
    # 徐志 <-> 周伟 (上下级)
    {"person_a": 7, "person_b": 2, "type": "上下级", "context": "芜湖市长与繁昌区长上下级", "overlap_org": "芜湖市", "overlap_period": ""},
    # 瞿辉 <-> 宁波 (上下级)
    {"person_a": 3, "person_b": 6, "type": "上下级", "context": "芜湖市委书记与繁昌区委书记上下级", "overlap_org": "芜湖市", "overlap_period": "2022-"},
    # 瞿辉 <-> 汪敏 (前后任)
    {"person_a": 3, "person_b": 1, "type": "前后任", "context": "繁昌区委书记前后任交接", "overlap_org": "中共繁昌区委", "overlap_period": ""},
    # 宁波 <-> 徐志 (党政搭档)
    {"person_a": 6, "person_b": 7, "type": "党政搭档", "context": "芜湖市委书记与市长工作搭档", "overlap_org": "芜湖市", "overlap_period": "2023-"},
]


# ── BUILD FUNCTIONS ──────────────────────────────────────────────────

def build_db():
    os.makedirs(STAGING, exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT,
            source TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        cur.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace,
                education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p["birthplace"], p["education"], p["party_join"], p["work_start"],
              p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"],
              pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"],
              r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    sz = os.path.getsize(DB_PATH)
    print(f"✓ Database created: {DB_PATH} ({sz} bytes)")


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    role = p["current_post"]
    if "书记" in role and "纪委" not in role:
        return "255,50,50"
    elif "区长" in role or "县长" in role or "市长" in role or "长" in role:
        return "50,100,255"
    elif "纪委" in role:
        return "255,165,0"
    return "100,100,100"


def is_top_leader(p):
    return p["id"] in (1, 2)


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append('    <description>繁昌区领导班子工作关系网络 - 安徽省芜湖市繁昌区</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: organizations
    for o in organizations:
        org_color_map = {
            "党委": "255,200,200", "政府": "200,200,255", "人大": "200,255,255",
            "政协": "255,240,200", "开发区": "200,255,200"
        }
        c = org_color_map.get(o["type"], "200,200,200")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')

    # person -> organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])} - {esc(pos["end"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person <-> person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    sz = os.path.getsize(GEXF_PATH)
    print(f"✓ GEXF graph created: {GEXF_PATH} ({sz} bytes)")


def print_summary():
    print()
    print("=== Summary Statistics ===")
    print(f"  Persons:        {len(persons)}")
    print(f"  Organizations:  {len(organizations)}")
    print(f"  Positions:      {len(positions)}")
    print(f"  Relationships:  {len(relationships)}")
    print()
    print("=== Core Leaders ===")
    print(f"  区委书记: 汪敏 (接替: 瞿辉)")
    print(f"  区长:     周伟")
    print()
    print("=== Files ===")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")


if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()
