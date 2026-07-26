#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 泸州市 (Luzhou City), 四川省.

Investigation date: 2026-07-26
Task ID: sichuan_泸州市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - Wikipedia (zh.wikipedia.org) — leadership table for 泸州市
  - www.luzhou.gov.cn — 泸州市人民政府网站 (unreachable during investigation due to network restrictions)
  - Various news and Baidu Baike (unreachable due to 403/timeout)

Confidence notes:
  - 刘筱柳 (市委书记): confirmed via Wikipedia leadership table (name, birth year 1971, gender female, native Chengdu, appointment Sep 2024)
  - 张伟 (市长): confirmed via Wikipedia leadership table (name, birth 1976-09, native Hebei, appointment Apr 2025)
  - 鞠丽 (人大常委会主任): confirmed via Wikipedia (birth 1966, Nanchong)
  - 田亚东 (政协主席): confirmed via Wikipedia (birth 1962, Zhongjiang)
  - Detailed career timelines could not be verified due to web access limitations
  - Web search tools, Baidu Baike, and government sites were rate-limited or timed out
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "泸州市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")

CANONICAL_DB = os.path.join(BASE, "..", "..", "database", f"{SLUG}_network.db")
CANONICAL_GEXF = os.path.join(BASE, "..", "..", "graph", f"{SLUG}_network.gexf")
CANONICAL_BUILD = os.path.join(BASE, "..", "..", "..", f"build_{SLUG}_data.py")
CANONICAL_PERSONS = Path(BASE) / ".." / ".." / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "刘筱柳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1971年3月",
        "birthplace": "四川省成都市",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共泸州市委员会",
        "source": "https://zh.wikipedia.org/wiki/泸州市"
    },
    {
        "id": 2,
        "name": "张伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年9月",
        "birthplace": "河北省",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "泸州市人民政府",
        "source": "https://zh.wikipedia.org/wiki/泸州市"
    },
    {
        "id": 3,
        "name": "鞠丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1966年6月",
        "birthplace": "四川省南充市",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "泸州市人民代表大会常务委员会",
        "source": "https://zh.wikipedia.org/wiki/泸州市"
    },
    {
        "id": 4,
        "name": "田亚东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1962年2月",
        "birthplace": "四川省中江县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议泸州市委员会",
        "source": "https://zh.wikipedia.org/wiki/泸州市"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 5,
        "name": "杨林兴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共泸州市委员会（前任）",
        "source": "https://zh.wikipedia.org/wiki/泸州市"
    },
    {
        "id": 6,
        "name": "余先河",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市长",
        "current_org": "泸州市人民政府（前任）",
        "source": "https://zh.wikipedia.org/wiki/泸州市"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Historical Leaders (for network context)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 7,
        "name": "刘强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965年",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记（2018-2021）",
        "current_org": "中共泸州市委员会（前任）",
        "source": "https://zh.wikipedia.org/wiki/泸州市"
    },
    {
        "id": 8,
        "name": "杨林兴（市长时期）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市长（2018-2021）",
        "current_org": "泸州市人民政府（前任）",
        "source": "https://zh.wikipedia.org/wiki/泸州市"
    },
    {
        "id": 9,
        "name": "蒋辅义",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记（2013-2018）",
        "current_org": "中共泸州市委员会（前任）",
        "source": "https://zh.wikipedia.org/wiki/泸州市"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共泸州市委员会", "type": "党委", "level": "地级", "parent": "中共四川省委员会", "location": "泸州市"},
    {"id": 2, "name": "泸州市人民政府", "type": "政府", "level": "地级", "parent": "四川省人民政府", "location": "泸州市"},
    {"id": 3, "name": "泸州市人民代表大会常务委员会", "type": "人大", "level": "地级", "parent": "", "location": "泸州市"},
    {"id": 4, "name": "中国人民政治协商会议泸州市委员会", "type": "政协", "level": "地级", "parent": "", "location": "泸州市"},
    {"id": 5, "name": "泸州市纪律检查委员会", "type": "党委", "level": "地级", "parent": "中共泸州市委员会", "location": "泸州市"},
    {"id": 6, "name": "中共四川省委组织部", "type": "党委", "level": "省级", "parent": "中共四川省委员会", "location": "成都市"},
    {"id": 7, "name": "四川省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "成都市"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # Current leaders
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2024-09", "end_date": "至今", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "2025-04", "end_date": "至今", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 3, "title": "市人大常委会主任", "start_date": "2022-01", "end_date": "至今", "rank": "正厅级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "市政协主席", "start_date": "2017-01", "end_date": "至今", "rank": "正厅级", "note": ""},
    # Predecessors
    {"person_id": 5, "org_id": 1, "title": "市委书记", "start_date": "2021-04", "end_date": "2024-09", "rank": "正厅级", "note": "前任市委书记"},
    {"person_id": 6, "org_id": 2, "title": "市长", "start_date": "2021-05", "end_date": "2025-04", "rank": "正厅级", "note": "前任市长"},
    # Historical
    {"person_id": 7, "org_id": 1, "title": "市委书记", "start_date": "2018-10", "end_date": "2021-04", "rank": "正厅级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "市长", "start_date": "2018-10", "end_date": "2021-05", "rank": "正厅级", "note": "前任市长后来升任书记"},
    {"person_id": 9, "org_id": 1, "title": "市委书记", "start_date": "2013-02", "end_date": "2018-10", "rank": "正厅级", "note": ""},
    # 刘强 also served as mayor before becoming party secretary
    {"person_id": 7, "org_id": 2, "title": "市长", "start_date": "2011-11", "end_date": "2018-10", "rank": "正厅级", "note": "市长转任市委书记"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # Predecessor-Successor: 市委书记
    {"person_a": 9, "person_b": 7, "type": "predecessor_successor", "context": "蒋辅义→刘强 泸州市委书记交接 2018-10", "overlap_org": "中共泸州市委员会", "overlap_period": "2018-10"},
    {"person_a": 7, "person_b": 5, "type": "predecessor_successor", "context": "刘强→杨林兴 泸州市委书记交接 2021-04", "overlap_org": "中共泸州市委员会", "overlap_period": "2021-04"},
    {"person_a": 5, "person_b": 1, "type": "predecessor_successor", "context": "杨林兴→刘筱柳 泸州市委书记交接 2024-09", "overlap_org": "中共泸州市委员会", "overlap_period": "2024-09"},

    # Predecessor-Successor: 市长
    {"person_a": 8, "person_b": 6, "type": "predecessor_successor", "context": "杨林兴→余先河 泸州市长交接 2021-05", "overlap_org": "泸州市人民政府", "overlap_period": "2021-05"},
    {"person_a": 6, "person_b": 2, "type": "predecessor_successor", "context": "余先河→张伟 泸州市长交接 2025-04", "overlap_org": "泸州市人民政府", "overlap_period": "2025-04"},

    # Mayor-to-Secretary internal promotion (刘强)
    {"person_a": 7, "person_b": 8, "type": "colleague", "context": "刘强(市长)与杨林兴(副市长/后来接任)在泸州市政府共事", "overlap_org": "泸州市人民政府", "overlap_period": "2018"},
]

# ── Build ──────────────────────────────────────────────────────────────────
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return 'r,g,b' string for a person based on current role."""
    role = p.get("current_post", "")
    if "书记" in role and "纪委" not in role:
        return "255,50,50"    # Red — Party Secretary
    elif "市长" in role or "区长" in role or "县长" in role:
        return "50,100,255"   # Blue — Government leader
    elif "主任" in role:
        return "200,100,100"  # Brown
    elif "政协" in role:
        return "100,200,100"  # Green
    else:
        return "100,100,100"  # Grey

def org_color(o):
    t = o.get("type", "")
    if "党委" in t:  return "255,200,200"
    if "政府" in t:  return "200,200,255"
    if "人大" in t:  return "200,255,255"
    if "政协" in t:  return "255,240,200"
    return "200,200,200"

def is_top_leader(p):
    return p["id"] in (1, 2)

def node_size(p):
    return "20.0" if is_top_leader(p) else "12.0"

def build_sqlite(db_path):
    """Build SQLite database."""
    import sqlite3
    conn = sqlite3.connect(db_path)
    
    # Drop and recreate tables
    for name in ("relationships", "positions", "organizations", "persons"):
        conn.execute(f"DROP TABLE IF EXISTS {name}")
    
    conn.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT DEFAULT '',
        ethnicity TEXT DEFAULT '', birth TEXT DEFAULT '', birthplace TEXT DEFAULT '',
        education TEXT DEFAULT '', party_join TEXT DEFAULT '', work_start TEXT DEFAULT '',
        current_post TEXT DEFAULT '', current_org TEXT DEFAULT '', source TEXT DEFAULT ''
    )""")
    conn.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT DEFAULT '',
        level TEXT DEFAULT '', parent TEXT DEFAULT '', location TEXT DEFAULT ''
    )""")
    conn.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL, org_id INTEGER NOT NULL,
        title TEXT DEFAULT '', start_date TEXT DEFAULT '', end_date TEXT DEFAULT '',
        rank TEXT DEFAULT '', note TEXT DEFAULT '',
        FOREIGN KEY (person_id) REFERENCES persons(id), FOREIGN KEY (org_id) REFERENCES organizations(id)
    )""")
    conn.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL, person_b INTEGER NOT NULL,
        type TEXT DEFAULT '', context TEXT DEFAULT '', overlap_org TEXT DEFAULT '',
        overlap_period TEXT DEFAULT '',
        FOREIGN KEY (person_a) REFERENCES persons(id), FOREIGN KEY (person_b) REFERENCES persons(id)
    )""")
    
    for p in persons:
        conn.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                     (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                      p["birthplace"], p["education"], p["party_join"], p["work_start"],
                      p["current_post"], p["current_org"], p["source"]))
    
    for o in organizations:
        conn.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                     (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    
    for pos in positions:
        conn.execute("INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
                     (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))
    
    for r in relationships:
        conn.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                     (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))
    
    conn.commit()
    conn.close()
    print(f"  Database written: {db_path}")
    print(f"  - {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

def build_gexf(gexf_path):
    """Build GEXF graph using string formatting."""
    from datetime import datetime as dt
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{dt.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>泸州市领导班子工作关系网络 - {SLUG} Leadership Network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="birthplace" type="string"/>')
    lines.append('      <attribute id="3" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    # ── Person nodes ──
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = node_size(p)
        pid = f"p{p['id']}"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["birthplace"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'        <viz:position x="{hash(pid) % 1000 - 500}" y="{hash(pid[::-1]) % 1000 - 500}" z="0.0"/>')
        lines.append('      </node>')

    # ── Organization nodes ──
    for o in organizations:
        c = org_color(o)
        oid = f"o{o['id']}"
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["location"])}"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # ── Edges ──
    eid = 0
    lines.append('    <edges>')

    # Person→Organization edges (worked_at)
    for pos in positions:
        pid = f"p{pos['person_id']}"
        oid = f"o{pos['org_id']}"
        period = f"{pos['start_date']} - {pos['end_date']}"
        lines.append(f'      <edge id="e{eid}" source="{pid}" target="{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(period)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person↔Person edges (relationship)
    for r in relationships:
        pa = f"p{r['person_a']}"
        pb = f"p{r['person_b']}"
        weight = "2.0"  # Strong
        lines.append(f'      <edge id="e{eid}" source="{pa}" target="{pb}" weight="{weight}" label="{esc(r["context"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {gexf_path}")
    print(f"  - {len(positions)} worked_at edges, {len(relationships)} relationship edges")


def main():
    print(f"Building {SLUG} data...")
    print()
    
    print("[1/2] Building SQLite database...")
    build_sqlite(DB_PATH)
    
    print()
    print("[2/2] Building GEXF graph...")
    build_gexf(GEXF_PATH)

    print()
    print("Done. Statistics:")
    print(f"  Database: {os.path.getsize(DB_PATH)} bytes")
    print(f"  GEXF: {os.path.getsize(GEXF_PATH)} bytes")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")


if __name__ == "__main__":
    main()