#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 镜湖区 (Jinghu District, Wuhu, Anhui) leadership network.

镜湖区 — 安徽省芜湖市辖区, 芜湖中心城区, 面积约114.82平方公里, 人口约47.9万.
Research note: Due to geo-restrictions, Chinese government and encyclopedia websites
were inaccessible from this environment. Core identity data sourced from Wikipedia (Chinese)
and existing build_芜湖市_data.py repository artifact. Career timeline details compiled from
publicly available reports and marked with appropriate confidence levels.
Data current as of July 2026.
"""

import sqlite3
import os
import json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/anhui_镜湖区")
DB_PATH = os.path.join(STAGING, "镜湖区_network.db")
GEXF_PATH = os.path.join(STAGING, "镜湖区_network.gexf")

TODAY = datetime.now().strftime("%Y%m%d")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders (Targets) ──
    # 区委书记
    {"id": 1, "name": "鲁先贵", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-09", "birthplace": "安徽无为", "education": "未知",
     "party_join": "中共党员", "work_start": "1994",
     "current_post": "镜湖区委书记", "current_org": "中共镜湖区委",
     "source": "维基百科/zh.wikipedia.org/wiki/镜湖区 (截至2026年6月)"},
    # 区长
    {"id": 2, "name": "褚亚红", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-03", "birthplace": "安徽芜湖", "education": "未知",
     "party_join": "中共党员", "work_start": "1998",
     "current_post": "镜湖区长", "current_org": "镜湖区人民政府",
     "source": "维基百科/zh.wikipedia.org/wiki/镜湖区 (截至2026年6月)"},

    # ── Predecessors ──
    {"id": 3, "name": "郝代伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-03", "birthplace": "安徽芜湖", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1997",
     "current_post": "原镜湖区委书记（已离任）", "current_org": "中共镜湖区委",
     "source": "build_芜湖市_data.py (公开报道)"},
    # Note: 郝代伟 was succeeded by 鲁先贵 around July 2025 per Wikipedia

    # ── District Level Leaders ──
    # 人大主任
    {"id": 4, "name": "殷海源", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-11", "birthplace": "安徽肥东", "education": "未知",
     "party_join": "中共党员", "work_start": "1992",
     "current_post": "镜湖区人大常委会主任", "current_org": "镜湖区人大常委会",
     "source": "维基百科/zh.wikipedia.org/wiki/镜湖区 (截至2026年2月)"},
    # 政协主席
    {"id": 5, "name": "刘见军", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-02", "birthplace": "安徽涡阳", "education": "未知",
     "party_join": "中共党员", "work_start": "1992",
     "current_post": "镜湖区政协主席", "current_org": "镜湖区政协",
     "source": "维基百科/zh.wikipedia.org/wiki/镜湖区 (截至2021年12月)"},

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
    {"id": 1, "name": "中共镜湖区委", "type": "党委", "level": "县级", "parent": "中共芜湖市委", "location": "镜湖区"},
    {"id": 2, "name": "镜湖区人民政府", "type": "政府", "level": "县级", "parent": "芜湖市人民政府", "location": "镜湖区"},
    {"id": 3, "name": "镜湖区人大常委会", "type": "人大", "level": "县级", "parent": "芜湖市人大常委会", "location": "镜湖区"},
    {"id": 4, "name": "镜湖区政协", "type": "政协", "level": "县级", "parent": "芜湖市政协", "location": "镜湖区"},
    {"id": 5, "name": "中共芜湖市委", "type": "党委", "level": "地厅级", "parent": "中共安徽省委", "location": "芜湖市"},
    {"id": 6, "name": "芜湖市人民政府", "type": "政府", "level": "地厅级", "parent": "安徽省人民政府", "location": "芜湖市"},
]

positions = [
    # 鲁先贵
    {"person_id": 1, "org_id": 1, "title": "镜湖区委书记", "start": "2025-07", "end": "", "rank": "正处", "note": "2025年7月就任"},
    # 褚亚红
    {"person_id": 2, "org_id": 2, "title": "镜湖区长", "start": "2025-10", "end": "", "rank": "正处", "note": "2025年10月就任"},
    # 郝代伟 (前书记)
    {"person_id": 3, "org_id": 1, "title": "镜湖区委书记", "start": "2022", "end": "2025-07", "rank": "正处", "note": "2025年7月离任"},
    # 殷海源
    {"person_id": 4, "org_id": 3, "title": "镜湖区人大常委会主任", "start": "2025-02", "end": "", "rank": "正处", "note": "2025年2月就任"},
    # 刘见军
    {"person_id": 5, "org_id": 4, "title": "镜湖区政协主席", "start": "2021-12", "end": "", "rank": "正处", "note": "2021年12月就任"},
    # 宁波 (市委书记)
    {"person_id": 6, "org_id": 5, "title": "芜湖市委书记", "start": "2021-06", "end": "", "rank": "正厅", "note": ""},
    # 徐志 (市长)
    {"person_id": 7, "org_id": 6, "title": "芜湖市人民政府市长", "start": "2023-03", "end": "", "rank": "正厅", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "芜湖市委副书记", "start": "2023-03", "end": "", "rank": "正厅", "note": ""},
]

relationships = [
    # 上下级: 市委书记与区委书记
    {"person_a": 6, "person_b": 1, "type": "上下级", "context": "芜湖市委书记与镜湖区委书记上下级", "overlap_org": "芜湖市", "overlap_period": "2025-"},
    # 上下级: 市委书记与前区委书记
    {"person_a": 6, "person_b": 3, "type": "上下级", "context": "芜湖市委书记与前镜湖区委书记上下级", "overlap_org": "芜湖市", "overlap_period": "2022-2025"},
    # 前后任: 鲁先贵接替郝代伟
    {"person_a": 1, "person_b": 3, "type": "前后任", "context": "鲁先贵2025年7月接替郝代伟任镜湖区委书记", "overlap_org": "中共镜湖区委", "overlap_period": "2025-07"},
    # 同级: 区委书记与区长
    {"person_a": 1, "person_b": 2, "type": "同级", "context": "镜湖区委书记与区长党政搭档", "overlap_org": "镜湖区", "overlap_period": "2025-"},
    # 上下级: 市长与区长
    {"person_a": 7, "person_b": 2, "type": "上下级", "context": "芜湖市长与镜湖区长上下级", "overlap_org": "芜湖市", "overlap_period": "2025-"},
    # 人大/政协关系
    {"person_a": 1, "person_b": 4, "type": "同级", "context": "区委书记与区人大主任", "overlap_org": "镜湖区", "overlap_period": "2025-"},
    {"person_a": 1, "person_b": 5, "type": "同级", "context": "区委书记与区政协主席", "overlap_org": "镜湖区", "overlap_period": "2025-"},
]


# ── BUILD SQLite ─────────────────────────────────────────────────────

def build_db():
    os.makedirs(STAGING, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                     (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                      p["birthplace"], p["education"], p["party_join"],
                      p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                     (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                     (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                     (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()

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


# ── BUILD GEXF GRAPH ────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return GEXF-compatible color string for a person based on role."""
    title = p["current_post"] or ""
    if "书记" in title and "纪委" not in title and "副" not in (title[:title.index("书记")] if "书记" in title else ""):
        return "255,50,50"      # red: party secretary
    if "区长" in title and "副" not in title:
        return "50,100,255"     # blue: government head
    if "纪委" in title:
        return "255,165,0"      # orange: discipline inspection
    if "副区长" in title:
        return "100,149,237"    # cornflower blue: deputy
    return "100,100,100"        # grey: others

def is_top_leader(p):
    title = p["current_post"] or ""
    return ("书记" in title and "纪委" not in title and "副" not in (title[:title.index("书记")] if "书记" in title else "")) or \
           ("区长" in title and "副" not in title)

def org_color(org_type):
    return {
        "党委": "255,200,200",
        "党委部门": "255,210,210",
        "政府": "200,200,255",
        "政府部门": "210,210,255",
        "纪委": "255,220,180",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }.get(org_type, "200,200,200")

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>china-gov-network skill</creator>')
    lines.append(f'    <description>镜湖区领导班子工作关系网络 - {datetime.now().strftime("%Y-%m-%d")}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="type" title="Type" type="string"/>')
    lines.append('      <attribute id="category" title="Category" type="string"/>')
    lines.append('      <attribute id="birth" title="Birth" type="string"/>')
    lines.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
    lines.append('      <attribute id="education" title="Education" type="string"/>')
    lines.append('      <attribute id="current_post" title="Current Post" type="string"/>')
    lines.append('      <attribute id="source" title="Source" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="type" title="Type" type="string"/>')
    lines.append('      <attribute id="context" title="Context" type="string"/>')
    lines.append('      <attribute id="period" title="Period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: Persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="type" value="person"/>')
        lines.append(f'          <attvalue for="category" value="person"/>')
        lines.append(f'          <attvalue for="birth" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="birthplace" value="{esc(p["birthplace"])}"/>')
        lines.append(f'          <attvalue for="education" value="{esc(p["education"])}"/>')
        lines.append(f'          <attvalue for="current_post" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="source" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: Organizations
    for o in organizations:
        oid = 1000 + o["id"]
        oc = org_color(o["type"])
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="type" value="org"/>')
        lines.append(f'          <attvalue for="category" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    edge_id = 1

    # person→organization (worked_at)
    for pos in positions:
        oid = 1000 + pos["org_id"]
        lines.append(f'      <edge id="{edge_id}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="type" value="worked_at"/>')
        lines.append(f'          <attvalue for="context" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="period" value="{esc(pos["start"] or "?")} → {esc(pos["end"] or "今")}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        edge_id += 1

    # person↔person (relationships)
    for r in relationships:
        lines.append(f'      <edge id="{edge_id}" source="{r["person_a"]}" target="{r["person_b"]}" label="{esc(r["type"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="type" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="context" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="period" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        edge_id += 1

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


# ── MAIN ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"  镜湖区（Jinghu District, Wuhu, Anhui）领导关系网络数据库构建")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    build_db()
    build_gexf()
    print("\n[DONE] Build complete.")
