#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Baiyin District (白银区), Baiyin, Gansu."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/gansu_白银区")
DB_PATH = os.path.join(TMP, "白银区_network.db")
GEXF_PATH = os.path.join(TMP, "白银区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {"id": 1, "name": "韩继国", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "白银市白银区委书记", "current_org": "中共白银市白银区委员会",
     "source": "https://www.baiyinqu.gov.cn/",
     "notes": "2026年7月仍任区委书记。Baidu Baike 2025年11月已记载为区委书记。",
     "confidence": "confirmed"},
    {"id": 2, "name": "潘虎", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "白银市白银区委副书记、区长", "current_org": "白银市白银区人民政府",
     "source": "https://www.baiyinqu.gov.cn/",
     "notes": "2026年7月任区政府党组书记、区长，主持区政府常务会议。",
     "confidence": "confirmed"},

    # ── Other Key Leaders ──
    {"id": 3, "name": "冯树川", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "白银区人大常委会主任", "current_org": "白银区人民代表大会常务委员会",
     "source": "https://baike.baidu.com/item/%E7%99%BD%E9%93%B6%E5%8C%BA",
     "notes": "Baidu Baike记载截至2025年11月在任。",
     "confidence": "confirmed"},
    {"id": 4, "name": "郝文军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "白银区政协主席", "current_org": "中国人民政治协商会议白银区委员会",
     "source": "https://baike.baidu.com/item/%E7%99%BD%E9%93%B6%E5%8C%BA",
     "notes": "Baidu Baike记载截至2025年11月在任。",
     "confidence": "confirmed"},
]

organizations = [
    {"id": 1, "name": "中共白银市白银区委员会", "type": "党委", "level": "县处级",
     "parent": "中共白银市委员会", "location": "甘肃省白银市白银区"},
    {"id": 2, "name": "白银市白银区人民政府", "type": "政府", "level": "县处级",
     "parent": "白银市人民政府", "location": "甘肃省白银市白银区"},
    {"id": 3, "name": "白银区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "白银市人大常委会", "location": "甘肃省白银市白银区"},
    {"id": 4, "name": "中国人民政治协商会议白银区委员会", "type": "政协", "level": "县处级",
     "parent": "白银市政协", "location": "甘肃省白银市白银区"},
    {"id": 5, "name": "白银区纪委监委", "type": "党委", "level": "县处级",
     "parent": "白银市纪委监委", "location": "甘肃省白银市白银区"},
    {"id": 6, "name": "白银区大数据中心", "type": "事业单位", "level": "乡科级",
     "parent": "白银区人民政府", "location": "甘肃省白银市白银区"},
]

positions = [
    # ── Han Jiguo (韩继国) ──
    {"person_id": 1, "org_id": 1, "title": "白银区委书记", "start": "", "end": "present",
     "rank": "副厅级", "note": "2025年11月前已任区委书记；2026年7月在任"},
    # ── Pan Hu (潘虎) ──
    {"person_id": 2, "org_id": 2, "title": "白银区委副书记、区长", "start": "", "end": "present",
     "rank": "正县级", "note": "2026年7月任区政府党组书记、区长"},
    {"person_id": 2, "org_id": 1, "title": "白银区委副书记", "start": "", "end": "present",
     "rank": "副厅级", "note": "兼任"},
    # ── Feng Shuchuan (冯树川) ──
    {"person_id": 3, "org_id": 3, "title": "白银区人大常委会主任", "start": "", "end": "present",
     "rank": "正县级", "note": "Baidu Baike 2025-11记载"},
    # ── Hao Wenjun (郝文军) ──
    {"person_id": 4, "org_id": 4, "title": "白银区政协主席", "start": "", "end": "present",
     "rank": "正县级", "note": "Baidu Baike 2025-11记载"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "strength": "strong",
     "context": "韩继国作为区委书记，潘虎作为区长，为党政正职搭档",
     "overlap_org": "中共白银市白银区委员会/白银市白银区人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "strength": "strong",
     "context": "韩继国与冯树川在区四套班子共事",
     "overlap_org": "中共白银市白银区委员会/白银区人大常委会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "strength": "strong",
     "context": "韩继国与郝文军在区四套班子共事",
     "overlap_org": "中共白银市白银区委员会/白银区政协",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "strength": "strong",
     "context": "潘虎与冯树川在区共事",
     "overlap_org": "白银市白银区人民政府/白银区人大常委会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "strength": "strong",
     "context": "潘虎与郝文军在区共事",
     "overlap_org": "白银市白银区人民政府/白银区政协",
     "overlap_period": "至今", "confidence": "confirmed"},
]

# ── HELPERS ─────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    role = p["current_post"]
    if "区委书记" in role and "副书记" not in role:
        return "255,50,50"
    elif "区长" in role and "副书记" in role:
        return "50,100,255"
    elif "区长" in role:
        return "50,100,255"
    elif "人大" in role:
        return "200,255,255"
    elif "政协" in role:
        return "255,240,200"
    elif "纪委书记" in role or "纪检" in role:
        return "255,165,0"
    else:
        return "100,100,100"

def org_color(o):
    t = o["type"]
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }.get(t, "200,200,200")

def is_top_leader(p):
    role = p["current_post"]
    return "区委书记" in role or ("区长" in role and "副书记" in role)

def person_size(p):
    return "20.0" if is_top_leader(p) else "12.0"

# ── BUILD DB ─────────────────────────────────────────────────

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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT, strength TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT, confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, strength, context, overlap_org, overlap_period, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["strength"],
             r["context"], r["overlap_org"], r["overlap_period"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")

# ── BUILD GEXF ────────────────────────────────────────────────

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append('    <description>白银区领导班子工作关系网络 - 甘肃省白银市白银区</description>')
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
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
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
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["parent"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])}~{esc(pos["end"])}"/>')
        lines.append(f'          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationships)
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append(f'          <attvalue for="3" value="{r["confidence"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {GEXF_PATH}")

# ── SUMMARY ──────────────────────────────────────────────────

def print_summary():
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()
