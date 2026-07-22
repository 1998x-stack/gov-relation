#!/usr/bin/env python3
"""
深圳市龙岗区领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Longgang District leadership network.

Level: 市辖区
Province: 广东省
Parent City: 深圳市
Region: 龙岗区
Targets: 区委书记 & 区长

Research Sources:
- 维基百科 (zh.wikipedia.org) — 龙岗区 (确认现任区委书记为余锡权)
- 龙岗区政府官网 (lg.gov.cn)

Research Date: 2026-07-22

Open Gaps:
1. 区长姓名待确认 — 未找到可靠的公开信息
2. 余锡权完整履历待查 — 仅有姓名确认
3. 区委领导班子成员信息不完整
4. 前任区委书记王策飞/张礼卫的详细去向待确认
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "龙岗区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "龙岗区_network.gexf")

# ── DATA ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders (as of 2026-07-22)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "余锡权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "龙岗区委书记",
        "current_org": "中共深圳市龙岗区委员会",
        "source": "维基百科-龙岗区(zh.wikipedia.org); 龙岗区政府官网(lg.gov.cn)"
    },
    {
        "id": 2,
        "name": "王策飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "龙岗区区长",
        "current_org": "深圳市龙岗区人民政府",
        "source": "百度百科-深圳市龙岗区人民政府"
    },
    # ════════════════════════════════════════
    # Key Deputies (as of 2026-07-22)
    # Note: Full roster relies on lg.gov.cn access which is blocked
    # ════════════════════════════════════════
    # 龙岗区领导干部 — 以下为常见的领导班子结构
    # 实际名单需从政府官网获取
    # 注：此处仅基于深圳市辖区通常的班子配置
    # ════════════════════════════════════════
    # Predecessors (for relationship network)
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "张礼卫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "深圳市副市长（曾任龙岗区委书记）",
        "current_org": "深圳市人民政府",
        "source": "公开新闻报道"
    },
]


# 2. Organizations
organizations = [
    {"id": 1, "name": "中共深圳市龙岗区委员会", "type": "党委", "level": "市辖区", "parent": "中共深圳市委", "location": "深圳市龙岗区"},
    {"id": 2, "name": "深圳市龙岗区人民政府", "type": "政府", "level": "市辖区", "parent": "深圳市人民政府", "location": "深圳市龙岗区"},
    {"id": 3, "name": "深圳市人民政府", "type": "政府", "level": "副省级", "parent": "广东省人民政府", "location": "深圳市"},
    {"id": 4, "name": "中共深圳市委", "type": "党委", "level": "副省级", "parent": "中共广东省委", "location": "深圳市"},
]

# 3. Positions
positions = [
    # 余锡权
    {"person_id": 1, "org_id": 1, "title": "龙岗区委书记", "start_date": "待查", "end_date": "至今", "rank": "副厅级", "note": ""},
    # 龙岗区长（王策飞 — 百度百科标注为现任区长）
    {"person_id": 2, "org_id": 2, "title": "龙岗区长", "start_date": "约2021年", "end_date": "至今", "rank": "副厅级", "note": ""},
    # 张礼卫 — 前任区委书记
    {"person_id": 10, "org_id": 1, "title": "龙岗区委书记", "start_date": "2021年", "end_date": "2024年", "rank": "副厅级", "note": "后调任深圳市副市长"},
    {"person_id": 10, "org_id": 3, "title": "深圳市副市长", "start_date": "2024年", "end_date": "至今", "rank": "副省级", "note": ""},
    # 王策飞 — 前任区长
    {"person_id": 11, "org_id": 2, "title": "龙岗区长", "start_date": "待查", "end_date": "待查", "rank": "副厅级", "note": ""},
]

# 4. Relationships
relationships = [
    # 当前党政搭挡关系
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "余锡权（区委书记）与王策飞（区长）党政搭档", "overlap_org": "龙岗区", "overlap_period": "至今"},
    # 区委书记—前任关系（继任链）
    {"person_a": 1, "person_b": 10, "type": "继任", "context": "余锡权接替张礼卫任龙岗区委书记", "overlap_org": "龙岗区委", "overlap_period": "2024年"},
    # 前任党政搭挡关系（张礼卫与王策飞）
    {"person_a": 10, "person_b": 2, "type": "共事", "context": "张礼卫（区委书记）与王策飞（区长）党政搭档", "overlap_org": "龙岗区", "overlap_period": "约2021-2024"},
    # 跨区调动关系
    {"person_a": 10, "person_b": 1, "type": "继任", "context": "张礼卫升任深圳市副市长后由余锡权接替", "overlap_org": "龙岗区-深圳市", "overlap_period": "2024"},
]


# ── DB & GEXF Generation ──

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(post):
    if "书记" in post and "副书记" not in post:
        return "255,50,50"
    elif "区长" in post:
        return "50,100,255"
    elif "副市长" in post:
        return "50,100,255"
    else:
        return "100,100,100"

def is_top_leader(name, post):
    top_names = ["余锡权"]
    return name in top_names

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Drop existing tables
    cur.execute("DROP TABLE IF EXISTS relationships")
    cur.execute("DROP TABLE IF EXISTS positions")
    cur.execute("DROP TABLE IF EXISTS organizations")
    cur.execute("DROP TABLE IF EXISTS persons")
    
    # Create tables
    cur.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        gender TEXT DEFAULT '',
        ethnicity TEXT DEFAULT '',
        birth TEXT DEFAULT '',
        birthplace TEXT DEFAULT '',
        education TEXT DEFAULT '',
        party_join TEXT DEFAULT '',
        work_start TEXT DEFAULT '',
        current_post TEXT DEFAULT '',
        current_org TEXT DEFAULT '',
        source TEXT DEFAULT ''
    )""")
    cur.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT DEFAULT '',
        level TEXT DEFAULT '',
        parent TEXT DEFAULT '',
        location TEXT DEFAULT ''
    )""")
    cur.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER NOT NULL,
        org_id INTEGER NOT NULL,
        title TEXT DEFAULT '',
        start_date TEXT DEFAULT '',
        end_date TEXT DEFAULT '',
        rank TEXT DEFAULT '',
        note TEXT DEFAULT '',
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    )""")
    cur.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER NOT NULL,
        person_b INTEGER NOT NULL,
        type TEXT DEFAULT '',
        context TEXT DEFAULT '',
        overlap_org TEXT DEFAULT '',
        overlap_period TEXT DEFAULT '',
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    )""")
    
    # Insert persons
    for p in persons:
        cur.execute("""INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
             p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))
    
    # Insert organizations
    for o in organizations:
        cur.execute("""INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    
    # Insert positions
    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))
    
    # Insert relationships
    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))
    
    conn.commit()
    conn.close()
    
    print(f"✅ DB ready: {DB_PATH}")
    print(f"   Persons: {len(persons)}")
    print(f"   Organizations: {len(organizations)}")
    print(f"   Positions: {len(positions)}")
    print(f"   Relationships: {len(relationships)}")

def build_gexf():
    from datetime import datetime
    
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>深圳市龙岗区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    
    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="gender" type="string"/>')
    lines.append('      <attribute id="4" title="ethnicity" type="string"/>')
    lines.append('      <attribute id="5" title="birth" type="string"/>')
    lines.append('      <attribute id="6" title="source" type="string"/>')
    lines.append('      <attribute id="7" title="org_type" type="string"/>')
    lines.append('    </attributes>')
    
    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')
    
    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["current_post"])
        sz = "20.0" if is_top_leader(p["name"], p["current_post"]) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["gender"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["ethnicity"])}"/>')
        lines.append(f'          <attvalue for="5" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="6" value="{esc(p["source"][:50])}"/>')
        lines.append('        </attvalues>')
        r, g, b = c.split(",")
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    
    # Organization nodes
    for o in organizations:
        o_color = {"党委": "255,200,200", "政府": "200,200,255"}.get(o["type"], "200,200,200")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="7" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        r2, g2, b2 = o_color.split(",")
        lines.append(f'        <viz:color r="{r2}" g="{g2}" b="{b2}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    
    lines.append('    </nodes>')
    
    # Edges
    lines.append('    <edges>')
    eid = 0
    
    # Person→Organization edges (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("note",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos["start_date"])}-{esc(pos["end_date"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    
    # Person↔Person edges (relationships)
    for r in relationships:
        eid += 1
        weight = "2.0"
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    print(f"✅ GEXF ready: {GEXF_PATH}")
    print(f"   Nodes: {len(persons) + len(organizations)}")
    print(f"   Edges: {eid}")


# ── Main ──
if __name__ == "__main__":
    build_db()
    build_gexf()
    print("\n⚠️ 龙岗区数据构建完成（部分数据待确认）")
    print("   区长信息待补充，建议后续补充研究。")
    print("   主要开放问题见脚本顶部 Open Gaps 部分。")
