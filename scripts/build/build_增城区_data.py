#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增城区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 广州市
Region: 增城区
Targets: 区委书记 & 区长

Research Sources:
- 广州市增城区人民政府门户网站 (www.zc.gov.cn) — 新闻中心: 领导活动报道
- 广州市人民政府门户网站 (www.gz.gov.cn) — 领导之窗
- zc.gov.cn 增城要闻文章 (2026年7月)

Research Date: 2026-07-22
"""

import os
import sqlite3
from datetime import datetime

# ── Paths ──
BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/guangdong_增城区")
DB_PATH = os.path.join(TMP, "增城区_network.db")
GEXF_PATH = os.path.join(TMP, "增城区_network.gexf")

# ════════════════════════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════════════════════════

persons = [
    # ── 1. Current Top Leaders ──
    {
        "id": 1,
        "name": "赵国生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广州市副市长、增城区委书记、增城经济技术开发区党工委书记",
        "current_org": "中共广州市增城区委员会",
        "source": "www.zc.gov.cn 增城要闻 — 增城区领导干部警示教育会 (2026-07-15)"
    },
    {
        "id": 2,
        "name": "林怡辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "增城区委副书记、区长",
        "current_org": "广州市增城区人民政府",
        "source": "www.zc.gov.cn 增城要闻 — 增城区领导干部警示教育会 (2026-07-15)"
    },
    # ── 2.人大政协领导 ──
    {
        "id": 3,
        "name": "祁森林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "增城区人大常委会主任",
        "current_org": "增城区人民代表大会常务委员会",
        "source": "www.zc.gov.cn 增城要闻 — 增城区领导干部警示教育会 (2026-07-15)"
    },
    {
        "id": 4,
        "name": "丘岳峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "增城区政协主席",
        "current_org": "中国人民政治协商会议广州市增城区委员会",
        "source": "www.zc.gov.cn 增城要闻 — 增城区领导干部警示教育会 (2026-07-15)"
    },
]

organizations = [
    {"id": 1, "name": "中共广州市增城区委员会", "type": "党委", "level": "县处级",
     "parent": "中共广州市委员会", "location": "广东省广州市增城区"},
    {"id": 2, "name": "广州市增城区人民政府", "type": "政府", "level": "县处级",
     "parent": "广州市人民政府", "location": "广东省广州市增城区"},
    {"id": 3, "name": "增城经济技术开发区党工委", "type": "党委", "level": "县处级",
     "parent": "中共广州市增城区委员会", "location": "广东省广州市增城区"},
    {"id": 4, "name": "增城区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "广州市人大常委会", "location": "广东省广州市增城区"},
    {"id": 5, "name": "中国人民政治协商会议广州市增城区委员会", "type": "政协", "level": "县处级",
     "parent": "广州市政协", "location": "广东省广州市增城区"},
]

positions = [
    # ── Zhao Guosheng (赵国生) ──
    {"person_id": 1, "org_id": 1, "title": "增城区委书记", "start": "", "end": "present",
     "rank": "副厅级", "note": "2026年7月以增城区委书记身份出席区领导干部警示教育会"},
    {"person_id": 1, "org_id": 3, "title": "增城经济技术开发区党工委书记", "start": "", "end": "present",
     "rank": "", "note": "兼任"},
    # ── Lin Yihui (林怡辉) ──
    {"person_id": 2, "org_id": 2, "title": "增城区委副书记、区长", "start": "", "end": "present",
     "rank": "正县级", "note": "2026年7月以区长身份主持区领导干部警示教育会"},
    # ── Qi Senlin (祁森林) ──
    {"person_id": 3, "org_id": 4, "title": "增城区人大常委会主任", "start": "", "end": "present",
     "rank": "正县级", "note": ""},
    # ── Qiu Yuefeng (丘岳峰) ──
    {"person_id": 4, "org_id": 5, "title": "增城区政协主席", "start": "", "end": "present",
     "rank": "正县级", "note": ""},
]

relationships = [
    # ── Top Leaders ──
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "strength": "strong",
     "context": "赵国生作为区委书记，林怡辉作为区长，是党政一把手搭档关系",
     "overlap_org": "中共广州市增城区委员会/广州市增城区人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    # ── Party Secretary → People's Congress ──
    {"person_a": 1, "person_b": 3, "type": "overlap", "strength": "medium",
     "context": "赵国生（区委书记）与祁森林（区人大常委会主任）在增城区委常委会同班共事",
     "overlap_org": "中共广州市增城区委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    # ── Party Secretary → Political Consultative ──
    {"person_a": 1, "person_b": 4, "type": "overlap", "strength": "medium",
     "context": "赵国生（区委书记）与丘岳峰（区政协主席）在增城区合作共事",
     "overlap_org": "中共广州市增城区委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    # ── Mayor → People's Congress ──
    {"person_a": 2, "person_b": 3, "type": "overlap", "strength": "medium",
     "context": "林怡辉（区长）与祁森林（区人大常委会主任）在增城区合作共事",
     "overlap_org": "广州市增城区人民政府/区人大",
     "overlap_period": "至今", "confidence": "confirmed"},
    # ── Mayor → Political Consultative ──
    {"person_a": 2, "person_b": 4, "type": "overlap", "strength": "medium",
     "context": "林怡辉（区长）与丘岳峰（区政协主席）在增城区合作共事",
     "overlap_org": "广州市增城区人民政府/区政协",
     "overlap_period": "至今", "confidence": "confirmed"},
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
    else:
        return "100,100,100"


def org_color(o):
    t = o["type"]
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
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
    lines.append('    <description>增城区领导班子工作关系网络 - 广东省广州市增城区</description>')
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


if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()
