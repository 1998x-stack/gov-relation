#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 广昌县 (抚州市, 江西省) leadership network.

Research status as of 2026-07-15:
- 县委书记: 吴自胜 (confirmed from 抚州市-level build script)
- 县长: [待核实] — name not found in available research materials

广昌县概况: 广昌县是江西省抚州市下辖的一个县，位于江西省东部，
武夷山西麓，是抚河的发源地之一，面积约1,612平方公里。

External web access (gov sites, Baidu Baike, search engines) was unavailable at build time.
All data beyond the confirmed county party secretary name is partial and explicitly marked
with confidence levels.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/jiangxi_广昌县")
DB_PATH = os.path.join(STAGING, "广昌县_network.db")
GEXF_PATH = os.path.join(STAGING, "广昌县_network.gexf")

os.makedirs(STAGING, exist_ok=True)

today = datetime.now().strftime("%Y-%m-%d")

# =========================================================================
# DATA
# =========================================================================

persons = [
    # ── Core Leaders: County Party Secretary ──
    {
        "id": 1,
        "name": "吴自胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "广昌县委书记",
        "current_org": "中共广昌县委员会",
        "source": "https://www.jxfz.gov.cn — 抚州市政府网站; build_fuzhou_data.py"
    },

    # ── Core Leaders: County Mayor ──
    {
        "id": 2,
        "name": "[待核实·广昌县长]",
        "gender": "[待核实]",
        "ethnicity": "汉族",
        "birth": "[待核实]",
        "birthplace": "[待核实]",
        "education": "[待核实]",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "广昌县长",
        "current_org": "广昌县人民政府",
        "source": "需查阅广昌县政府官网(www.jxgc.gov.cn)或江西省委组织部任前公示"
    },

    # ── City-level leaders (抚州市) for context ──
    {
        "id": 3,
        "name": "范小林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-12",
        "birthplace": "江西宜丰",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "抚州市委书记",
        "current_org": "中共抚州市委员会",
        "source": "https://www.jxfz.gov.cn — 抚州市政府网站; build_fuzhou_data.py"
    },
    {
        "id": 4,
        "name": "胡剑飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "抚州市委副书记、市长",
        "current_org": "抚州市人民政府",
        "source": "https://www.jxfz.gov.cn — 抚州市政府网站; build_黎川县_data.py"
    },

    # ── 广昌县人大常委会主任 (placeholder) ──
    {
        "id": 5,
        "name": "[待核实·广昌县人大常委会主任]",
        "gender": "[待核实]",
        "ethnicity": "汉族",
        "birth": "[待核实]",
        "birthplace": "[待核实]",
        "education": "[待核实]",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "广昌县人大常委会主任",
        "current_org": "广昌县人民代表大会常务委员会",
        "source": "需查阅广昌县政府网站领导之窗"
    },

    # ── 广昌县政协主席 (placeholder) ──
    {
        "id": 6,
        "name": "[待核实·广昌县政协主席]",
        "gender": "[待核实]",
        "ethnicity": "汉族",
        "birth": "[待核实]",
        "birthplace": "[待核实]",
        "education": "[待核实]",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "广昌县政协主席",
        "current_org": "中国人民政治协商会议广昌县委员会",
        "source": "需查阅广昌县政府网站领导之窗"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共广昌县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共抚州市委员会",
        "location": "江西省抚州市广昌县"
    },
    {
        "id": 2,
        "name": "广昌县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "抚州市人民政府",
        "location": "江西省抚州市广昌县"
    },
    {
        "id": 3,
        "name": "广昌县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "抚州市人民代表大会常务委员会",
        "location": "江西省抚州市广昌县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议广昌县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "中国人民政治协商会议抚州市委员会",
        "location": "江西省抚州市广昌县"
    },
    {
        "id": 5,
        "name": "中共抚州市委员会",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共江西省委员会",
        "location": "江西省抚州市"
    },
    {
        "id": 6,
        "name": "抚州市人民政府",
        "type": "政府",
        "level": "地厅级",
        "parent": "江西省人民政府",
        "location": "江西省抚州市"
    },
]

positions = [
    # 吴自胜 — Party Secretary
    {"id": 1, "person_id": 1, "org_id": 1, "title": "广昌县委书记", "start": "", "end": "present", "rank": "正县级", "note": "主持县委全面工作"},

    # [待核实·广昌县长] — County Mayor
    {"id": 2, "person_id": 2, "org_id": 2, "title": "广昌县长", "start": "", "end": "present", "rank": "正县级", "note": "主持县政府全面工作"},
    {"id": 3, "person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "正县级", "note": ""},

    # City-level leaders
    {"id": 4, "person_id": 3, "org_id": 5, "title": "抚州市委书记", "start": "2024-10", "end": "present", "rank": "正厅级", "note": ""},
    {"id": 5, "person_id": 4, "org_id": 6, "title": "抚州市委副书记、市长", "start": "", "end": "present", "rank": "正厅级", "note": ""},

    # 人大/政协
    {"id": 6, "person_id": 5, "org_id": 3, "title": "广昌县人大常委会主任", "start": "", "end": "present", "rank": "正县级", "note": ""},
    {"id": 7, "person_id": 6, "org_id": 4, "title": "广昌县政协主席", "start": "", "end": "present", "rank": "正县级", "note": ""},
]

relationships = [
    # County Party Secretary ↔ City-level leaders
    {
        "id": 1,
        "person_a_id": 1,
        "person_b_id": 3,
        "type": "superior_subordinate",
        "context": "范小林（抚州市委书记）领导广昌县委书记吴自胜",
        "overlap_org": "中共抚州市委员会 → 中共广昌县委员会",
        "overlap_period": "2024-10至今"
    },
    {
        "id": 2,
        "person_a_id": 1,
        "person_b_id": 4,
        "type": "superior_subordinate",
        "context": "胡剑飞（抚州市长）与广昌县为政府系统上下级关系",
        "overlap_org": "抚州市人民政府 → 广昌县人民政府",
        "overlap_period": ""
    },
    # County Party Secretary ↔ County Mayor (known pairing relationship)
    {
        "id": 3,
        "person_a_id": 1,
        "person_b_id": 2,
        "type": "superior_subordinate",
        "context": "广昌县委书记与县长为党政一把手搭档",
        "overlap_org": "中共广昌县委员会 / 广昌县人民政府",
        "overlap_period": ""
    },
]

# =========================================================================
# BUILD SQLITE
# =========================================================================

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS relationships")
    cur.execute("DROP TABLE IF EXISTS positions")
    cur.execute("DROP TABLE IF EXISTS organizations")
    cur.execute("DROP TABLE IF EXISTS persons")

    cur.execute("""
        CREATE TABLE persons (
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
        )
    """)

    cur.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE positions (
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
        )
    """)

    cur.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY,
            person_a_id INTEGER,
            person_b_id INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a_id) REFERENCES persons(id),
            FOREIGN KEY (person_b_id) REFERENCES persons(id)
        )
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

    # Stats
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
    elif "主任" in post and "人大" in post:
        return "200,255,255"
    elif "主席" in post and "政协" in post:
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
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>广昌县领导班子工作关系网络 - 江西省抚州市广昌县</description>')
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
    print("Building 广昌县 network data...")
    build_db()
    build_gexf()
    print(f"\nDone! Files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
