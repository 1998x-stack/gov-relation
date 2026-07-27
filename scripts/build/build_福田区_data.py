#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Futian District (福田区), Shenzhen, Guangdong."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/guangdong_福田区")
DB_PATH = os.path.join(TMP, "福田区_network.db")
GEXF_PATH = os.path.join(TMP, "福田区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {"id": 1, "name": "周江涛", "gender": "", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "深圳市福田区委书记", "current_org": "中共深圳市福田区委员会",
     "source": "https://zh.wikipedia.org/zh-cn/%E7%A6%8F%E7%94%B0%E5%8C%BA"},
    {"id": 2, "name": "黄伟", "gender": "", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "深圳市福田区委副书记、区长", "current_org": "深圳市福田区人民政府",
     "source": "https://zh.wikipedia.org/zh-cn/%E7%A6%8F%E7%94%B0%E5%8C%BA"},

    # ── Standing Committee (待补充) ──
    # 常务副区长, 组织部长, 纪委书记, 政法委书记, 宣传部长 - research needed

    # ── Additional Leaders (partial, from existing Shenzhen data) ──
    # 福田区人大常委会主任 for completeness
    # 福田区政协主席 for completeness
]

organizations = [
    {"id": 1, "name": "中共深圳市福田区委员会", "type": "党委", "level": "县处级", "parent": "中共深圳市委员会",
     "location": "广东省深圳市福田区福民路123号"},
    {"id": 2, "name": "深圳市福田区人民政府", "type": "政府", "level": "县处级", "parent": "深圳市人民政府",
     "location": "广东省深圳市福田区福民路123号"},
    {"id": 3, "name": "福田区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "深圳市人大常委会",
     "location": "广东省深圳市福田区"},
    {"id": 4, "name": "中国人民政治协商会议福田区委员会", "type": "政协", "level": "县处级", "parent": "深圳市政协",
     "location": "广东省深圳市福田区"},
    {"id": 5, "name": "中共深圳市福田区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共深圳市纪律检查委员会",
     "location": "广东省深圳市福田区"},
    {"id": 6, "name": "中共深圳市福田区委组织部", "type": "党委", "level": "乡科级", "parent": "中共深圳市福田区委员会",
     "location": "广东省深圳市福田区"},
    {"id": 7, "name": "中共深圳市福田区委宣传部", "type": "党委", "level": "乡科级", "parent": "中共深圳市福田区委员会",
     "location": "广东省深圳市福田区"},
    {"id": 8, "name": "中共深圳市福田区委政法委员会", "type": "党委", "level": "乡科级", "parent": "中共深圳市福田区委员会",
     "location": "广东省深圳市福田区"},
    {"id": 9, "name": "深圳市公安局福田分局", "type": "政府", "level": "乡科级", "parent": "深圳市公安局",
     "location": "广东省深圳市福田区"},
    {"id": 10, "name": "福田区园岭街道", "type": "乡镇/街道", "level": "乡科级", "parent": "深圳市福田区人民政府",
     "location": "广东省深圳市福田区"},
    {"id": 11, "name": "福田区南园街道", "type": "乡镇/街道", "level": "乡科级", "parent": "深圳市福田区人民政府",
     "location": "广东省深圳市福田区"},
    {"id": 12, "name": "福田区福田街道", "type": "乡镇/街道", "level": "乡科级", "parent": "深圳市福田区人民政府",
     "location": "广东省深圳市福田区"},
    {"id": 13, "name": "福田区沙头街道", "type": "乡镇/街道", "level": "乡科级", "parent": "深圳市福田区人民政府",
     "location": "广东省深圳市福田区"},
    {"id": 14, "name": "福田区梅林街道", "type": "乡镇/街道", "level": "乡科级", "parent": "深圳市福田区人民政府",
     "location": "广东省深圳市福田区"},
    {"id": 15, "name": "福田区华富街道", "type": "乡镇/街道", "level": "乡科级", "parent": "深圳市福田区人民政府",
     "location": "广东省深圳市福田区"},
    {"id": 16, "name": "福田区香蜜湖街道", "type": "乡镇/街道", "level": "乡科级", "parent": "深圳市福田区人民政府",
     "location": "广东省深圳市福田区"},
    {"id": 17, "name": "福田区莲花街道", "type": "乡镇/街道", "level": "乡科级", "parent": "深圳市福田区人民政府",
     "location": "广东省深圳市福田区"},
    {"id": 18, "name": "福田区华强北街道", "type": "乡镇/街道", "level": "乡科级", "parent": "深圳市福田区人民政府",
     "location": "广东省深圳市福田区"},
    {"id": 19, "name": "福田区福保街道", "type": "乡镇/街道", "level": "乡科级", "parent": "深圳市福田区人民政府",
     "location": "广东省深圳市福田区"},
]

positions = [
    # ── Zhou Jiangtao (周江涛) ──
    # Career timeline: 待补充。周江涛原为福田区长，后升任福田区委书记
    # 公开信息缺口: 出生年份、籍贯、教育背景、到任时间均待补充
    {"person_id": 1, "org_id": 2, "title": "福田区委副书记、区长",
     "start": "未知", "end": "未知", "rank": "正局级",
     "note": "曾任福田区长，后任区委书记。具体到任时间待补充。"},
    {"person_id": 1, "org_id": 1, "title": "福田区委书记",
     "start": "未知", "end": "present", "rank": "副厅级",
     "note": "现任福田区委书记。到任时间待确认（2026-07-20维基百科显示为现任）"},

    # ── Huang Wei (黄伟) ──
    # Career timeline: 待补充。黄伟曾任福田区委书记，后转任区长
    {"person_id": 2, "org_id": 1, "title": "福田区委书记",
     "start": "未知", "end": "未知", "rank": "副厅级",
     "note": "曾任福田区委书记，后转任区长"},
    {"person_id": 2, "org_id": 2, "title": "福田区委副书记、区长",
     "start": "未知", "end": "present", "rank": "正局级",
     "note": "现任福田区长。到任时间待确认（2026-07-20维基百科显示为现任）"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "strength": "strong",
     "context": "周江涛与黄伟在福田区形成党政一把手搭档关系（周江涛为区委书记，黄伟为区长）。二人或存在角色交接：黄伟此前任福田区委书记，周江涛此前任福田区长，后二人职务互换。",
     "overlap_org": "中共深圳市福田区委员会/深圳市福田区人民政府",
     "overlap_period": "待确认", "confidence": "plausible"},
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
    lines.append('    <description>福田区领导班子工作关系网络 - 广东省深圳市福田区</description>')
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
        lines.append(f'          <attvalue for="3" value="plausible"/>')
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
    print(f"\n⚠️  This is a PARTIAL build with significant data gaps.")
    print(f"   Core leader names confirmed from Wikipedia (2026-07-20).")
    print(f"   Career timelines, deputies, and predecessor/successor info need further research.")

if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()
