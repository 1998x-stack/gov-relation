#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 相山区 (Xiangshan District, Huaibei, Anhui) leadership network.
Generated: 2026-07-15
Task: anhui_相山区 - 区委书记 & 区长
Sources: baike.baidu.com (encyclopedia, accessed 2026-07-15)
Notes: Government website (hbxf.gov.cn) DNS unreachable during build; data compiled from Baidu Baike
       (updated 2026-06-27) and available knowledge. See confidence levels and open_questions for gaps.
"""

import sqlite3
import os
from datetime import datetime

_script_dir = os.path.dirname(os.path.abspath(__file__))
# Support both staging (data/tmp/anhui_相山区/) and repo-root execution
if os.path.basename(_script_dir) == "anhui_相山区":
    BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(_script_dir))))
else:
    BASE = _script_dir
STAGING = os.path.join(BASE, "data/tmp/anhui_相山区")
DB_PATH = os.path.join(BASE, "data/database", "相山区_network.db") if os.path.basename(_script_dir) != "anhui_相山区" else os.path.join(STAGING, "相山区_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph", "相山区_network.gexf") if os.path.basename(_script_dir) != "anhui_相山区" else os.path.join(STAGING, "相山区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {"id": 1, "name": "池圣洲", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-08", "birthplace": "安徽萧县", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1998-05",
     "current_post": "相山区委书记", "current_org": "中共相山区委员会",
     "source": "https://baike.baidu.com/item/%E6%B1%A0%E5%9C%A3%E6%B4%B2"},
    {"id": 2, "name": "蒋鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "相山区委副书记、区长", "current_org": "相山区人民政府",
     "source": "https://baike.baidu.com/item/%E7%9B%B8%E5%B1%B1%E5%8C%BA"},

    # ── 四大班子主要领导 ──
    {"id": 3, "name": "李清平", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "相山区人大常委会党组书记、主任", "current_org": "相山区人民代表大会常务委员会",
     "source": "https://baike.baidu.com/item/%E7%9B%B8%E5%B1%B1%E5%8C%BA"},
    {"id": 4, "name": "赵德华", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "相山区政协党组书记、主席", "current_org": "政协相山区委员会",
     "source": "https://baike.baidu.com/item/%E7%9B%B8%E5%B1%B1%E5%8C%BA"},

    # ── 前任领导 ──
    {"id": 5, "name": "朱龙", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前相山区委书记", "current_org": "中共相山区委员会",
     "source": "https://baike.baidu.com/item/%E7%9B%B8%E5%B1%B1%E5%8C%BA"},
    {"id": 6, "name": "张利", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前相山区区长", "current_org": "相山区人民政府",
     "source": "https://baike.baidu.com/item/%E7%9B%B8%E5%B1%B1%E5%8C%BA"},
]

organizations = [
    {"id": 1, "name": "中共相山区委员会", "type": "党委", "level": "县处级", "parent": "中共淮北市委", "location": "安徽省淮北市相山区"},
    {"id": 2, "name": "相山区人民政府", "type": "政府", "level": "县处级", "parent": "淮北市人民政府", "location": "安徽省淮北市相山区"},
    {"id": 3, "name": "相山区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "淮北市人民代表大会常务委员会", "location": "安徽省淮北市相山区"},
    {"id": 4, "name": "政协相山区委员会", "type": "政协", "level": "县处级", "parent": "政协淮北市委员会", "location": "安徽省淮北市相山区"},
]

positions = [
    # 池圣洲 - 相山区委书记
    {"id": 1, "person_id": 1, "org_id": 1, "title": "相山区委书记",
     "start": "2025-09", "end": "present", "rank": "正县级", "note": "2025年9月任相山区人武部党委第一书记；2026年6月当选十届区委书记"},

    # 蒋鹏 - 相山区委副书记、区长
    {"id": 2, "person_id": 2, "org_id": 1, "title": "相山区委副书记",
     "start": "", "end": "present", "rank": "正县级", "note": ""},
    {"id": 3, "person_id": 2, "org_id": 2, "title": "相山区区长",
     "start": "", "end": "present", "rank": "正县级", "note": "截至2026年6月任区长"},

    # 李清平 - 人大主任
    {"id": 4, "person_id": 3, "org_id": 3, "title": "相山区人大常委会党组书记、主任",
     "start": "", "end": "present", "rank": "正县级", "note": ""},

    # 赵德华 - 政协主席
    {"id": 5, "person_id": 4, "org_id": 4, "title": "相山区政协党组书记、主席",
     "start": "", "end": "present", "rank": "正县级", "note": ""},

    # 朱龙 - 前区委书记
    {"id": 6, "person_id": 5, "org_id": 1, "title": "前相山区委书记",
     "start": "", "end": "2025-08", "rank": "正县级", "note": "前任区委书记，池圣洲2025年接任"},

    # 张利 - 前区长
    {"id": 7, "person_id": 6, "org_id": 2, "title": "前相山区区长",
     "start": "2022-01", "end": "", "rank": "正县级", "note": "2022年1月当选相山区区长"},
]

relationships = [
    # 池圣洲与蒋鹏 - 党政主官
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "superior_subordinate",
     "context": "区委书记与区长党政主官关系", "overlap_org": "中共相山区委员会/相山区人民政府",
     "overlap_period": "2025年至今"},

    # 池圣洲与李清平 - 区委书记与人大主任
    {"id": 2, "person_a_id": 1, "person_b_id": 3, "type": "overlap",
     "context": "区委书记与人大常委会主任", "overlap_org": "相山区",
     "overlap_period": "2025年至今"},

    # 池圣洲与赵德华 - 区委书记与政协主席
    {"id": 3, "person_a_id": 1, "person_b_id": 4, "type": "overlap",
     "context": "区委书记与政协主席", "overlap_org": "相山区",
     "overlap_period": "2025年至今"},

    # 池圣洲与朱龙 - 前后任
    {"id": 4, "person_a_id": 1, "person_b_id": 5, "type": "predecessor_successor",
     "context": "池圣洲接替朱龙任相山区委书记", "overlap_org": "中共相山区委员会",
     "overlap_period": ""},

    # 蒋鹏与张利 - 前后任区长
    {"id": 5, "person_a_id": 2, "person_b_id": 6, "type": "predecessor_successor",
     "context": "蒋鹏接替张利任相山区区长（推测）", "overlap_org": "相山区人民政府",
     "overlap_period": ""},
]


# ── HELPERS ──────────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    post = p["current_post"]
    if "区委书记" in post:
        return "255,50,50"
    if "区长" in post:
        return "50,100,255"
    if "人大" in post:
        return "200,100,100"
    if "政协" in post:
        return "100,100,200"
    return "100,100,100"

def org_color(o):
    t = o["type"]
    if t == "党委":
        return "255,200,200"
    if t == "政府":
        return "200,200,255"
    if t == "人大":
        return "200,255,255"
    if t == "政协":
        return "255,240,200"
    if t == "乡镇/街道":
        return "255,255,200"
    if t == "事业单位":
        return "220,220,220"
    if t == "群团":
        return "255,220,255"
    return "200,200,200"

def is_top_leader(p):
    return p["id"] in (1, 2)


# ── BUILD DB ─────────────────────────────────────────────────────────

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
    print(f"  Persons: {cur.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}")
    print(f"  Organizations: {cur.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}")
    print(f"  Positions: {cur.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}")
    print(f"  Relationships: {cur.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")
    conn.close()


# ── BUILD GEXF ───────────────────────────────────────────────────────

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>相山区（安徽省淮北市）领导关系网络 - 2026年7月</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="gender" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="level" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes - Persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["gender"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="4" value="县处级"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes - Organizations
    for o in organizations:
        c = org_color(o)
        oid = o["id"] + 100
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> Organization (worked_at)
    for pos in positions:
        eid += 1
        oid = pos["org_id"] + 100
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person relationships
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" label="{esc(r["type"])}" weight="2.0">')
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
    print(f"  GEXF: {len(persons)} persons, {len(organizations)} orgs, {eid} edges")


# ── MAIN ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.makedirs(STAGING, exist_ok=True)
    print("Building 相山区 (Xiangshan District, Huaibei) network...")
    print(f"  DB path: {DB_PATH}")
    print(f"  GEXF path: {GEXF_PATH}")
    build_db()
    build_gexf()
    print("Done.")
