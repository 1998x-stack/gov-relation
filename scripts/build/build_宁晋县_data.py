#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 宁晋县 (Ningjin County) leadership network.

河北省邢台市宁晋县 — 县委书记 & 县长 investigation.
"""

import json
import os
import subprocess
import sys
from datetime import datetime

# Paths
BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_BASE = os.path.abspath(os.path.join(BASE, "../../.."))
DB_PATH = os.path.join(BASE, "宁晋县_network.db")
GEXF_PATH = os.path.join(BASE, "宁晋县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Party Secretary of Ningjin County ──
    {
        "id": 1,
        "name": "王涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共宁晋县委书记",
        "current_org": "中共宁晋县委员会",
        "source": "https://baike.baidu.com/item/%E5%AE%81%E6%99%8B%E5%8E%BF",
    },
    # ── Current County Mayor of Ningjin County ──
    {
        "id": 2,
        "name": "孔军峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宁晋县人民政府县长",
        "current_org": "宁晋县人民政府",
        "source": "https://www.ningjin.gov.cn/channel/list/22.html",
    },
    # ── Executive Deputy County Mayor ──
    {
        "id": 3,
        "name": "申立强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-12",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宁晋县常务副县长",
        "current_org": "宁晋县人民政府",
        "source": "https://www.ningjin.gov.cn/channel/list/22.html",
    },
    # ── Deputy County Mayor ──
    {
        "id": 4,
        "name": "宁岩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宁晋县人民政府副县长",
        "current_org": "宁晋县人民政府",
        "source": "https://www.ningjin.gov.cn/single/11/81660.html",
    },
    # ── County CPPCC Vice Chair ──
    {
        "id": 5,
        "name": "陈荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宁晋县政协副主席",
        "current_org": "宁晋县政协",
        "source": "https://www.ningjin.gov.cn/single/11/83104.html",
    },
    # ── County Government Office Director ──
    {
        "id": 6,
        "name": "贾锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宁晋县人民政府办公室主任",
        "current_org": "宁晋县人民政府办公室",
        "source": "https://www.ningjin.gov.cn/single/21/53119.html",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共宁晋县委员会",
        "type": "党委",
        "level": "县处级",
        "location": "河北省邢台市宁晋县",
    },
    {
        "id": 2,
        "name": "宁晋县人民政府",
        "type": "政府",
        "level": "县处级",
        "location": "河北省邢台市宁晋县",
    },
    {
        "id": 3,
        "name": "宁晋县政协",
        "type": "政协",
        "level": "县处级",
        "location": "河北省邢台市宁晋县",
    },
    {
        "id": 4,
        "name": "宁晋县人民政府办公室",
        "type": "政府",
        "level": "乡科级",
        "location": "河北省邢台市宁晋县",
    },
]

positions = [
    # 王涛 - Party Secretary
    {"person_id": 1, "org_id": 1, "title": "中共宁晋县委书记",
     "start": "", "end": "present", "rank": "正处级", "note": "Current county party secretary"},
    # 孔军峰 - County Mayor
    {"person_id": 2, "org_id": 2, "title": "宁晋县人民政府县长",
     "start": "", "end": "present", "rank": "正处级", "note": "Current county mayor"},
    # 申立强 - Executive Deputy Mayor
    {"person_id": 3, "org_id": 2, "title": "宁晋县常务副县长",
     "start": "", "end": "present", "rank": "副处级", "note": "Executive deputy county mayor"},
    # 宁岩 - Deputy Mayor
    {"person_id": 4, "org_id": 2, "title": "宁晋县人民政府副县长",
     "start": "", "end": "present", "rank": "副处级", "note": "Deputy county mayor"},
    # 陈荣 - CPPCC Vice Chair
    {"person_id": 5, "org_id": 3, "title": "宁晋县政协副主席",
     "start": "", "end": "present", "rank": "副处级", "note": "CPPCC vice chair"},
    # 贾锋 - Government Office Director
    {"person_id": 6, "org_id": 4, "title": "宁晋县人民政府办公室主任",
     "start": "", "end": "present", "rank": "正科级", "note": "Government office director"},
]

relationships = [
    # 王涛 (Party Secretary) <-> 孔军峰 (County Mayor) - work overlap
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "县委书记与县长在宁晋县搭班子", "overlap_org": "宁晋县",
     "overlap_period": ""},
    # 孔军峰 (County Mayor) <-> 申立强 (Executive Deputy Mayor)
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "申立强协助孔军峰县长负责审计工作（县政府领导分工确认）",
     "overlap_org": "宁晋县人民政府", "overlap_period": ""},
    # 申立强 <-> 宁岩 - both deputy mayors
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "同在宁晋县政府领导班子", "overlap_org": "宁晋县人民政府",
     "overlap_period": ""},
]


# ── HELPERS ─────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(person):
    """Return 'r,g,b' string based on role."""
    role = person.get("current_post", "")
    if "书记" in role and "县委" in role or "县委书记" in role:
        return "255,50,50"
    elif "县长" in role:
        return "50,100,255"
    elif "常务副县长" in role:
        return "50,100,255"
    elif "副县长" in role:
        return "50,100,255"
    elif "政协" in role:
        return "255,165,0"
    else:
        return "100,100,100"


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "政协": "255,240,200",
    }
    return colors.get(org_type, "200,200,200")


def is_top_leader(person):
    return "县委书记" in person.get("current_post", "") or "县长" in person.get("current_post", "")


def node_size(person):
    return "20.0" if is_top_leader(person) else "12.0"


# ── BUILD FUNCTIONS ─────────────────────────────────────────────────

def build_db(db_path):
    """Create SQLite database."""
    import sqlite3
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()

    # Create tables
    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
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
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        c.execute(
            "INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]),
        )

    # Insert organizations
    for o in organizations:
        c.execute(
            "INSERT INTO organizations VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o["location"]),
        )

    # Insert positions
    for pos in positions:
        c.execute(
            "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos.get("start", ""), pos.get("end", ""),
             pos.get("rank", ""), pos.get("note", "")),
        )

    # Insert relationships
    for r in relationships:
        c.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"],
             r["context"], r.get("overlap_org", ""), r.get("overlap_period", "")),
        )

    conn.commit()
    conn.close()
    print(f"  DB created: {db_path}")
    print(f"    Persons: {len(persons)}")
    print(f"    Organizations: {len(organizations)}")
    print(f"    Positions: {len(positions)}")
    print(f"    Relationships: {len(relationships)}")


def build_gexf(gexf_path):
    """Create GEXF graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>宁晋县（河北省邢台市）领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = node_size(p)
        pid = f"p{p['id']}"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("source", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: organizations
    for o in organizations:
        c = org_color(o["type"])
        oid = f"o{o['id']}"
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges: person->organization (worked_at)
    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        eid += 1
        lines.append(
            f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" '
            f'label="{esc(pos["title"])}" weight="1.0">'
        )
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges: person<->person (relationship)
    for r in relationships:
        eid += 1
        weight = "2.0"
        lines.append(
            f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" '
            f'label="{esc(r["type"])}" weight="{weight}">'
        )
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF created: {gexf_path}")
    print(f"    Nodes: {len(persons) + len(organizations)}")
    print(f"    Edges: {len(positions) + len(relationships)}")


def main():
    print("=" * 60)
    print("宁晋县 (Ningjin County) Leadership Network Builder")
    print("河北省邢台市")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    print("=" * 60)

    print("\n[1/2] Building SQLite database...")
    build_db(DB_PATH)

    print("\n[2/2] Building GEXF graph...")
    build_gexf(GEXF_PATH)

    print("\n" + "=" * 60)
    print("Build complete!")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    main()
