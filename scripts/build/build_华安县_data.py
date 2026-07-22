#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Hua'an County leadership network."""

import sqlite3
import os
import json
import sys
from datetime import datetime

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
STAGING = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING, "华安县_network.db")
GEXF_PATH = os.path.join(STAGING, "华安县_network.gexf")
PERSONS_DIR = STAGING

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Hua'an County Party Secretary ──
    {
        "id": 1, "name": "廖海军", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "中共华安县委书记", "current_org": "中共华安县委员会",
        "source": "https://zh.wikipedia.org/wiki/华安县"
    },
    # ── Current Hua'an County Deputy Secretary & Acting County Mayor ──
    {
        "id": 2, "name": "（待查）代县长", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "华安县委副书记、代县长", "current_org": "华安县人民政府",
        "source": "https://www.huaan.gov.cn/"
    },
    # ── Previous Party Secretary (predecessor to 廖海军) ──
    {
        "id": 3, "name": "叶毓", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "（前任华安县委书记）", "current_org": "",
        "source": "https://www.huaan.gov.cn/"
    },
    # ── Previous County Mayor ──
    {
        "id": 4, "name": "陈敏杰", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "（前任华安县县长）", "current_org": "",
        "source": "https://www.huaan.gov.cn/cms/html/haxrmzf/rsxx/index.html"
    },
]

organizations = [
    {"id": 1, "name": "中共华安县委员会", "type": "党委", "level": "县处级", "parent": "中共漳州市委员会", "location": "福建省漳州市华安县"},
    {"id": 2, "name": "华安县人民政府", "type": "政府", "level": "县处级", "parent": "漳州市人民政府", "location": "福建省漳州市华安县"},
    {"id": 3, "name": "华安县人大常委会", "type": "人大", "level": "县处级", "parent": "漳州市人大常委会", "location": "福建省漳州市华安县"},
    {"id": 4, "name": "华安县政协", "type": "政协", "level": "县处级", "parent": "漳州市政协", "location": "福建省漳州市华安县"},
    {"id": 5, "name": "华安县纪委监委", "type": "党委", "level": "县处级", "parent": "中共华安县委员会", "location": "福建省漳州市华安县"},
    {"id": 6, "name": "华安县委组织部", "type": "党委", "level": "县处级", "parent": "中共华安县委员会", "location": "福建省漳州市华安县"},
    {"id": 7, "name": "华安县委宣传部", "type": "党委", "level": "县处级", "parent": "中共华安县委员会", "location": "福建省漳州市华安县"},
    {"id": 8, "name": "华安县委政法委", "type": "党委", "level": "县处级", "parent": "中共华安县委员会", "location": "福建省漳州市华安县"},
    {"id": 9, "name": "华安县人民政府办公室", "type": "政府", "level": "乡科级", "parent": "华安县人民政府", "location": "福建省漳州市华安县"},
    {"id": 10, "name": "华安县委统战部", "type": "党委", "level": "县处级", "parent": "中共华安县委员会", "location": "福建省漳州市华安县"},
]

positions = [
    # 廖海军
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共华安县委书记", "start": "未知", "end": "present", "rank": "县处级正职", "note": "2026年7月确认在任"},
    # 代县长（待查）
    {"id": 2, "person_id": 2, "org_id": 2, "title": "华安县委副书记、代县长", "start": "未知", "end": "present", "rank": "县处级正职", "note": "2026年7月确认在任"},
    {"id": 3, "person_id": 2, "org_id": 1, "title": "华安县委副书记", "start": "未知", "end": "present", "rank": "县处级副职", "note": ""},
    # 叶毓（前任县委书记）
    {"id": 4, "person_id": 3, "org_id": 1, "title": "华安县委书记（前任）", "start": "未知", "end": "未知", "rank": "县处级正职", "note": "廖海军的前任"},
    # 陈敏杰（前任县长）
    {"id": 5, "person_id": 4, "org_id": 2, "title": "华安县县长（前任）", "start": "未知", "end": "未知", "rank": "县处级正职", "note": "代县长的前任"},
]

relationships = [
    {"id": 1, "person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与代县长，党政主要领导搭档", "overlap_org": "华安县", "overlap_period": "2026-"},
    {"id": 2, "person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "廖海军接替叶毓的县委书记职务", "overlap_org": "中共华安县委员会", "overlap_period": ""},
    {"id": 3, "person_a": 2, "person_b": 4, "type": "predecessor_successor", "context": "代县长接替陈敏杰的县长职务", "overlap_org": "华安县人民政府", "overlap_period": ""},
]


# ── HELPERS ──────────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_role_color(p):
    name = p.get("current_post", "") or ""
    if "书记" in name and "县委" in name:
        return "255,50,50"
    if "代县长" in name or "县长" in name or "副县长" in name:
        return "50,100,255"
    if "纪委" in name or "监委" in name:
        return "255,165,0"
    return "100,100,100"


def is_top_leader(p):
    name = p.get("current_post", "") or ""
    return ("书记" in name and "县委" in name) or "县长" in name or "代县长" in name


def org_type_color(org):
    t = org.get("type", "")
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
    }
    return colors.get(t, "200,200,200")


# ── BUILD DATABASE ───────────────────────────────────────────────────

def build_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY,
            person_a INTEGER, person_b INTEGER, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id,name,type,level,parent,location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT OR REPLACE INTO positions
            (id,person_id,org_id,title,start,end,rank,note)
            VALUES (?,?,?,?,?,?,?,?)""",
            (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT OR REPLACE INTO relationships
            (id,person_a,person_b,type,context,overlap_org,overlap_period)
            VALUES (?,?,?,?,?,?,?)""",
            (r["id"], r["person_a"], r["person_b"], r["type"],
             r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"  ✓ Database written: {DB_PATH}")


# ── BUILD GEXF ───────────────────────────────────────────────────────

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    today = datetime.now().strftime("%Y-%m-%d")

    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append('    <description>华安县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        pid = f"p{p['id']}"
        color = person_role_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        role = esc(p.get("current_post", ""))
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{role}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = f"o{o['id']}"
        color = org_type_color(o)
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 1
    # person->organization (worked_at)
    for pos in positions:
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # person<->person (relationship)
    for r in relationships:
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  ✓ GEXF written: {GEXF_PATH}")


# ── STATS ────────────────────────────────────────────────────────────

def print_stats():
    print(f"\n  人物: {len(persons)}")
    print(f"  机构: {len(organizations)}")
    print(f"  任职: {len(positions)}")
    print(f"  关系: {len(relationships)}")


# ── MAIN ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("华安县领导班子关系网络 — 数据构建")
    print("=" * 50)
    print_stats()
    print()
    build_database()
    build_gexf()
    print("\n  ✓ 完成")
