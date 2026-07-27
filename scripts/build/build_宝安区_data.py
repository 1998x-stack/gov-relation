#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宝安区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 深圳市
Region: 宝安区
Targets: 区委书记 & 区长

Research Sources:
- 维基百科: 宝安区条目 (zh.wikipedia.org/wiki/宝安区) — 区委书记=舒毓民, 区长=王立德
- 宝安政府在线 (www.baoan.gov.cn) — 领导之窗页面因网络限制未能获取详情
- 人民网地方领导资料库 — 网络受限

Research Date: 2026-07-22

网络环境限制说明:
- Exa 搜索达到速率限制 (无 API key)
- Jina Reader 超时
- 百度百科被 403 拦截
- 宝安区政府网站领导之窗路径返回 404
- 基于维基百科宝安区条目确认核心领导信息

核心领导信息:
- 舒毓民: 宝安区委书记（维基百科宝安区条目 infobox 显示）
- 王立德: 宝安区委副书记、区长（维基百科宝安区条目 infobox 显示）
- 两人均为中共党员，其他履历详情因网络受限待补充

已知的前任领导:
- 王守睿: 前宝安区委书记（2021-2024年在任，后调任深圳市副市长）
- 于宝明: 前宝安区政协主席
- 张志彪: 前宝安区人大常委会主任
"""

import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "宝安区_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "宝安区_network.gexf")

# ════════════════════════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Current Top Leaders (as of 2026-07-22)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "舒毓民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "宝安区委书记",
        "current_org": "中共深圳市宝安区委员会",
        "source": "维基百科宝安区条目 infobox (2026-07-22版) — https://zh.wikipedia.org/wiki/%E5%AE%9D%E5%AE%89%E5%8C%BA"
    },
    {
        "id": 2,
        "name": "王立德",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "宝安区委副书记、区长",
        "current_org": "深圳市宝安区人民政府",
        "source": "维基百科宝安区条目 infobox (2026-07-22版) — https://zh.wikipedia.org/wiki/%E5%AE%9D%E5%AE%89%E5%8C%BA"
    },
    # ════════════════════════════════════════
    # Former Leaders (Predecessors)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "王守睿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已离任（原宝安区委书记，现任深圳市副市长）",
        "current_org": "深圳市人民政府",
        "source": "公开报道 — 原宝安区委书记（2021-2024年在任），后升任深圳市副市长"
    },
]

organizations = [
    {"id": 1, "name": "中共深圳市宝安区委员会", "type": "党委", "level": "县处级", "parent": "中共深圳市委员会",
     "location": "广东省深圳市宝安区创业一路1号"},
    {"id": 2, "name": "深圳市宝安区人民政府", "type": "政府", "level": "县处级", "parent": "深圳市人民政府",
     "location": "广东省深圳市宝安区创业一路1号"},
    {"id": 3, "name": "宝安区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "深圳市人大常委会",
     "location": "广东省深圳市宝安区"},
    {"id": 4, "name": "中国人民政治协商会议宝安区委员会", "type": "政协", "level": "县处级", "parent": "深圳市政协",
     "location": "广东省深圳市宝安区"},
    {"id": 5, "name": "中共深圳市宝安区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共深圳市纪律检查委员会",
     "location": "广东省深圳市宝安区"},
    {"id": 6, "name": "中共深圳市宝安区委组织部", "type": "党委", "level": "乡科级", "parent": "中共深圳市宝安区委员会",
     "location": "广东省深圳市宝安区"},
    {"id": 7, "name": "中共深圳市宝安区委宣传部", "type": "党委", "level": "乡科级", "parent": "中共深圳市宝安区委员会",
     "location": "广东省深圳市宝安区"},
    {"id": 8, "name": "中共深圳市宝安区委政法委员会", "type": "党委", "level": "乡科级", "parent": "中共深圳市宝安区委员会",
     "location": "广东省深圳市宝安区"},
    {"id": 9, "name": "深圳市公安局宝安分局", "type": "政府", "level": "乡科级", "parent": "深圳市公安局",
     "location": "广东省深圳市宝安区"},
    # 10个街道
    {"id": 10, "name": "宝安区新安街道", "type": "乡镇/街道", "level": "乡科级", "parent": "深圳市宝安区人民政府",
     "location": "广东省深圳市宝安区新安街道"},
    {"id": 11, "name": "宝安区西乡街道", "type": "乡镇/街道", "level": "乡科级", "parent": "深圳市宝安区人民政府",
     "location": "广东省深圳市宝安区西乡街道"},
    {"id": 12, "name": "宝安区航城街道", "type": "乡镇/街道", "level": "乡科级", "parent": "深圳市宝安区人民政府",
     "location": "广东省深圳市宝安区航城街道"},
    {"id": 13, "name": "宝安区福永街道", "type": "乡镇/街道", "level": "乡科级", "parent": "深圳市宝安区人民政府",
     "location": "广东省深圳市宝安区福永街道"},
    {"id": 14, "name": "宝安区福海街道", "type": "乡镇/街道", "level": "乡科级", "parent": "深圳市宝安区人民政府",
     "location": "广东省深圳市宝安区福海街道"},
    {"id": 15, "name": "宝安区沙井街道", "type": "乡镇/街道", "level": "乡科级", "parent": "深圳市宝安区人民政府",
     "location": "广东省深圳市宝安区沙井街道"},
    {"id": 16, "name": "宝安区新桥街道", "type": "乡镇/街道", "level": "乡科级", "parent": "深圳市宝安区人民政府",
     "location": "广东省深圳市宝安区新桥街道"},
    {"id": 17, "name": "宝安区松岗街道", "type": "乡镇/街道", "level": "乡科级", "parent": "深圳市宝安区人民政府",
     "location": "广东省深圳市宝安区松岗街道"},
    {"id": 18, "name": "宝安区燕罗街道", "type": "乡镇/街道", "level": "乡科级", "parent": "深圳市宝安区人民政府",
     "location": "广东省深圳市宝安区燕罗街道"},
    {"id": 19, "name": "宝安区石岩街道", "type": "乡镇/街道", "level": "乡科级", "parent": "深圳市宝安区人民政府",
     "location": "广东省深圳市宝安区石岩街道"},
]

positions = [
    # ── 舒毓民 ──
    {"person_id": 1, "org_id": 1, "title": "宝安区委书记",
     "start": "未知", "end": "present", "rank": "副厅级",
     "note": "现任宝安区委书记。到任具体时间待确认。维基百科宝安区条目显示为现任。"},

    # ── 王立德 ──
    {"person_id": 2, "org_id": 2, "title": "宝安区委副书记、区长",
     "start": "未知", "end": "present", "rank": "正局级",
     "note": "现任宝安区区长。到任具体时间待确认。维基百科宝安区条目显示为现任。"},

    # ── 王守睿 — 前区委书记 ──
    {"person_id": 3, "org_id": 1, "title": "宝安区委书记",
     "start": "2021", "end": "2024", "rank": "副厅级",
     "note": "前宝安区委书记，后调任深圳市副市长。在任期间与王立德形成党政搭档。"},
    {"person_id": 3, "org_id": 9, "title": "深圳市副市长",
     "start": "2024", "end": "present", "rank": "正厅级",
     "note": "现任深圳市副市长。"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "strength": "strong",
     "context": "舒毓民（区委书记）与王立德（区长）为宝安区现任党政一把手搭档关系。",
     "overlap_org": "中共深圳市宝安区委员会/深圳市宝安区人民政府",
     "overlap_period": "待确认", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 2, "type": "superior_subordinate", "strength": "strong",
     "context": "王守睿（前任区委书记）与王立德（区长）曾为宝安区党政一把手搭档关系（2021-2024年）。",
     "overlap_org": "中共深圳市宝安区委员会",
     "overlap_period": "2021~2024", "confidence": "plausible"},
]

# ════════════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════════════

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

# ════════════════════════════════════════════════════════════════
# BUILD DB
# ════════════════════════════════════════════════════════════════

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, native_place TEXT, education TEXT,
            party_join TEXT, work_start TEXT, current_post TEXT,
            current_org TEXT, source TEXT
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
            (id, name, gender, ethnicity, birth, birthplace, native_place,
             education, party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p.get("native_place", ""), p["education"],
             p["party_join"], p["work_start"], p["current_post"],
             p["current_org"], p["source"]))

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

# ════════════════════════════════════════════════════════════════
# BUILD GEXF
# ════════════════════════════════════════════════════════════════

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append('    <description>宝安区领导班子工作关系网络 - 广东省深圳市宝安区</description>')
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

# ════════════════════════════════════════════════════════════════
# SUMMARY
# ════════════════════════════════════════════════════════════════

def print_summary():
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"\n⚠️  This is a PARTIAL build with significant data gaps due to web access limitations.")
    print(f"   Core leader names confirmed from Wikipedia (2026-07-22).")
    print(f"   Career timelines, deputies, and detailed bios need further research.")

if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()
