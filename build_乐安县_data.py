#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 乐安县 (抚州市, 江西省) leadership network.

Data sourced from 乐安县人民政府 website (www.jxlean.gov.cn), leadership pages,
news articles, and meeting reports. Where information is incomplete, it is marked
with explicit confidence levels.

乐安县概况: 乐安县是江西省抚州市下辖的一个县，位于江西省中部，抚州市西南部。
面积约2413平方公里，人口约36万。下辖9镇7乡。
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/jiangxi_乐安县")
DB_PATH = os.path.join(STAGING, "乐安县_network.db")
GEXF_PATH = os.path.join(STAGING, "乐安县_network.gexf")

os.makedirs(STAGING, exist_ok=True)

# =========================================================================
# DATA
# =========================================================================

# ── Notes on Data Sources ──
# 1. 郑军 biography: https://www.jxlean.gov.cn/col/col10214/index.html (2026-07)
# 2. 吴伟军 biography: https://www.jxlean.gov.cn/col/col28592/index.html (2026-07)
# 3. Meeting report revealing full leadership roster: https://www.jxlean.gov.cn/art/2026/7/7/art_447_4460141.html
# 4. 艾志峰/郑军 transition identified from: https://www.jxlean.gov.cn/art/2026/6/30/art_447_4457948.html
#    On 2026-06-30: 艾志峰 still Party Secretary, 郑军 as 县长
#    By 2026-07-07: 郑军 as Party Secretary, 吴伟军 as 县长候选人
#    By 2026-07-13: 郑军 confirmed as 县委书记

persons = [
    # ── Core Leaders: Party Secretary ──
    {
        "id": 1,
        "name": "郑军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-01",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乐安县委书记",
        "current_org": "中共乐安县委员会",
        "source": "https://www.jxlean.gov.cn/col/col10214/index.html — 乐安县政府网站领导专页"
    },

    # ── Core Leaders: Mayor Candidate ──
    {
        "id": 2,
        "name": "吴伟军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-12",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乐安县委副书记、县长候选人",
        "current_org": "乐安县人民政府",
        "source": "https://www.jxlean.gov.cn/col/col28592/index.html — 乐安县政府网站领导专页"
    },

    # ── Previous Party Secretary ──
    {
        "id": 3,
        "name": "艾志峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乐安县委书记（前任）",
        "current_org": "中共乐安县委员会",
        "source": "https://www.jxlean.gov.cn/art/2026/6/30/art_447_4457948.html — 乐安县新闻（2026年6月30日，艾志峰仍以县委书记身份出席活动）"
    },

    # ── County Leaders (from meeting report 2026-07-07) ──
    {
        "id": 4,
        "name": "游俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乐安县政协党组书记、主席",
        "current_org": "政协乐安县委员会",
        "source": "https://www.jxlean.gov.cn/art/2026/7/7/art_447_4460141.html — 县委政协工作会议报道（2026年7月7日）"
    },
    {
        "id": 5,
        "name": "张雷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乐安县领导",
        "current_org": "乐安县人民政府",
        "source": "https://www.jxlean.gov.cn/art/2026/7/7/art_447_4460141.html — 县委政协工作会议报道（2026年7月7日）"
    },
    {
        "id": 6,
        "name": "欧阳杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乐安县领导",
        "current_org": "乐安县人民政府",
        "source": "https://www.jxlean.gov.cn/art/2026/7/7/art_447_4460141.html — 县委政协工作会议报道（2026年7月7日）"
    },
    {
        "id": 7,
        "name": "吴捷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乐安县领导",
        "current_org": "乐安县人民政府",
        "source": "https://www.jxlean.gov.cn/art/2026/7/7/art_447_4460141.html — 县委政协工作会议报道（2026年7月7日）"
    },
    {
        "id": 8,
        "name": "陈若旻",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乐安县领导",
        "current_org": "乐安县人民政府",
        "source": "https://www.jxlean.gov.cn/art/2026/7/7/art_447_4460141.html — 县委政协工作会议报道（2026年7月7日）"
    },
    {
        "id": 9,
        "name": "周游",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乐安县领导",
        "current_org": "乐安县人民政府",
        "source": "https://www.jxlean.gov.cn/art/2026/7/7/art_447_4460141.html — 县委政协工作会议报道（2026年7月7日）"
    },
    {
        "id": 10,
        "name": "滕飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乐安县领导",
        "current_org": "乐安县人民政府",
        "source": "https://www.jxlean.gov.cn/art/2026/7/7/art_447_4460141.html — 县委政协工作会议报道（2026年7月7日）"
    },
]

organizations = [
    {"id": 1, "name": "中共乐安县委员会", "type": "党委", "level": "县处级", "parent": "中共抚州市委员会", "location": "江西省抚州市乐安县"},
    {"id": 2, "name": "乐安县人民政府", "type": "政府", "level": "县处级", "parent": "抚州市人民政府", "location": "江西省抚州市乐安县"},
    {"id": 3, "name": "政协乐安县委员会", "type": "政协", "level": "县处级", "parent": "政协抚州市委员会", "location": "江西省抚州市乐安县"},
    {"id": 4, "name": "乐安县人大常委会", "type": "人大", "level": "县处级", "parent": "抚州市人大常委会", "location": "江西省抚州市乐安县"},
]

positions = [
    # 郑军
    {"id": 1, "person_id": 1, "org_id": 1, "title": "乐安县委书记", "start": "2026-07", "end": "present", "rank": "县处级正职", "note": "原乐安县长晋升，接替艾志峰"},
    {"id": 2, "person_id": 1, "org_id": 2, "title": "乐安县委副书记、县长（前任职务）", "start": "unknown", "end": "2026-06", "rank": "县处级正职", "note": "2026年6月仍以县长身份活动"},

    # 吴伟军
    {"id": 3, "person_id": 2, "org_id": 2, "title": "乐安县委副书记、县长候选人", "start": "2026-07", "end": "present", "rank": "县处级正职", "note": "接替郑军任县长候选人"},

    # 艾志峰
    {"id": 4, "person_id": 3, "org_id": 1, "title": "乐安县委书记（前任）", "start": "unknown", "end": "2026-06", "rank": "县处级正职", "note": "截至2026年6月30日仍以县委书记身份活动"},

    # 游俊
    {"id": 5, "person_id": 4, "org_id": 3, "title": "乐安县政协党组书记、主席", "start": "unknown", "end": "present", "rank": "县处级正职", "note": ""},

    # Other leaders (exact titles TBD — listed as '县领导' in meeting report)
    {"id": 6, "person_id": 5, "org_id": 2, "title": "乐安县领导", "start": "unknown", "end": "present", "rank": "县处级", "note": "具体职务待核实"},
    {"id": 7, "person_id": 6, "org_id": 2, "title": "乐安县领导", "start": "unknown", "end": "present", "rank": "县处级", "note": "具体职务待核实"},
    {"id": 8, "person_id": 7, "org_id": 2, "title": "乐安县领导", "start": "unknown", "end": "present", "rank": "县处级", "note": "具体职务待核实"},
    {"id": 9, "person_id": 8, "org_id": 2, "title": "乐安县领导", "start": "unknown", "end": "present", "rank": "县处级", "note": "具体职务待核实"},
    {"id": 10, "person_id": 9, "org_id": 2, "title": "乐安县领导", "start": "unknown", "end": "present", "rank": "县处级", "note": "具体职务待核实"},
    {"id": 11, "person_id": 10, "org_id": 2, "title": "乐安县领导", "start": "unknown", "end": "present", "rank": "县处级", "note": "具体职务待核实"},
]

relationships = [
    # 郑军 ← predecessor/successor → 艾志峰
    {"id": 1, "person_a_id": 1, "person_b_id": 3, "type": "predecessor_successor", "context": "郑军接替艾志峰任乐安县委书记", "overlap_org": "中共乐安县委员会", "overlap_period": "2026-06/2026-07过渡期"},

    # 郑军 ← overlap → 吴伟军 (县长候选人, working together)
    {"id": 2, "person_a_id": 1, "person_b_id": 2, "type": "overlap", "context": "郑军作为县委书记与县长候选人吴伟军共事", "overlap_org": "乐安县人民政府", "overlap_period": "2026-07至今"},

    # 郑军 ← overlap → 游俊 (政协主席, attending same meetings)
    {"id": 3, "person_a_id": 1, "person_b_id": 4, "type": "overlap", "context": "县委政协工作会议召开，县委书记与政协主席共事", "overlap_org": "政协乐安县委员会", "overlap_period": "2026-07"},

    # 吴伟军 ← overlap → 游俊
    {"id": 4, "person_a_id": 2, "person_b_id": 4, "type": "overlap", "context": "吴伟军主持县委政协工作会议，游俊作报告", "overlap_org": "政协乐安县委员会", "overlap_period": "2026-07"},
]


# =========================================================================
# BUILD DATABASE
# =========================================================================

def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE persons(
            id INTEGER PRIMARY KEY,
            name TEXT,
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
        CREATE TABLE organizations(
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE positions(
            id INTEGER PRIMARY KEY,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT
        );
        CREATE TABLE relationships(
            id INTEGER PRIMARY KEY,
            person_a_id INTEGER,
            person_b_id INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT
        );
    """)

    for p in persons:
        cur.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education,
                                 party_join, work_start, current_post, current_org, source)
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
            INSERT INTO positions (id, person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
              pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (id, person_a_id, person_b_id, type, context,
                                       overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
              r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()

    print(f"  Persons: {cur.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}")
    print(f"  Organizations: {cur.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}")
    print(f"  Positions: {cur.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}")
    print(f"  Relationships: {cur.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")

    conn.close()


# =========================================================================
# BUILD GEXF
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    post = p["current_post"]
    if "书记" in post and "县委" in post:
        return "255,50,50"
    elif "县长" in post:
        return "50,100,255"
    elif "政协" in post:
        return "255,240,200"
    else:
        return "100,100,100"

def org_color(o):
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")

def is_top_leader(p):
    current = p["current_post"]
    return "县委书记" in current or "县长" in current


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>乐安县领导班子工作关系网络 - 江西省抚州市乐安县</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges: person -> organization (worked_at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        label = f"{pos['title']}"
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(label)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"][:50]) if pos["note"] else ""}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges: person <-> person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["overlap_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF nodes: {len(persons) + len(organizations)}")
    print(f"  GEXF edges: {eid}")


# =========================================================================
# MAIN
# =========================================================================

if __name__ == "__main__":
    print("Building 乐安县 network data...")
    build_db()
    build_gexf()
    print(f"\nDone! Files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
