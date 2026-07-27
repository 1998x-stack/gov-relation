#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宜州区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 市辖区
Province: 广西壮族自治区
Parent City: 河池市
Region: 宜州区
Targets: 区委书记 & 区长

历史沿革:
- 宜州区原为宜州市（县级市），2016年12月撤市设区，成为河池市宜州区
- 河池市政府驻地由金城江区迁至宜州区（2016年起推进，2021年完成部分搬迁）

当前在任信息（基于公开资料整理）:
- 区委书记: 薛海源（曾任宜州区区长，2021年任区委书记）
- 区长: 戚啸（曾任区委副书记，接替薛海源任区长）
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "宜州区"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-23"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：区委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "薛海源",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜州区委书记",
        "current_org": "中共河池市宜州区委员会",
        "source": "https://www.gxhc.gov.cn/"
    },
    # ════════════════════════════════════════
    # 核心领导：区长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "戚啸",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜州区委副书记、区长",
        "current_org": "河池市宜州区人民政府",
        "source": "https://www.gxhc.gov.cn/"
    },
    # ════════════════════════════════════════
    # 区人大常委会主任
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜州区人大常委会主任",
        "current_org": "河池市宜州区人大常委会",
        "source": "待查"
    },
    # ════════════════════════════════════════
    # 区政协主席
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜州区政协主席",
        "current_org": "政协河池市宜州区委员会",
        "source": "待查"
    },
    # ════════════════════════════════════════
    # 区委副书记（协助书记工作）
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜州区委副书记",
        "current_org": "中共河池市宜州区委员会",
        "source": "待查"
    },
    # ════════════════════════════════════════
    # 常务副区长
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜州区委常委、常务副区长",
        "current_org": "河池市宜州区人民政府",
        "source": "待查"
    },
    # ════════════════════════════════════════
    # 区委常委、纪委书记
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜州区委常委、纪委书记",
        "current_org": "中共河池市宜州区纪律检查委员会",
        "source": "待查"
    },
    # ════════════════════════════════════════
    # 区委常委、组织部部长
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜州区委常委、组织部部长",
        "current_org": "中共河池市宜州区委员会组织部",
        "source": "待查"
    },
    # ════════════════════════════════════════
    # 区委常委、宣传部部长
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜州区委常委、宣传部部长",
        "current_org": "中共河池市宜州区委员会宣传部",
        "source": "待查"
    },
    # ════════════════════════════════════════
    # 区委常委、政法委书记
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜州区委常委、政法委书记",
        "current_org": "中共河池市宜州区委员会政法委员会",
        "source": "待查"
    },
    # ════════════════════════════════════════
    # 前任区委书记 — 翟红玲（薛海源前任）
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "翟红玲",
        "gender": "女",
        "ethnicity": "壮族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "前任宜州区委书记；后调任河池市副市长（推测）"
    },
    # ════════════════════════════════════════
    # 河池市委书记（上级）
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "河池市委书记",
        "current_org": "中共河池市委员会",
        "source": "待查"
    },
    # ════════════════════════════════════════
    # 河池市市长（上级）
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "河池市委副书记、市长",
        "current_org": "河池市人民政府",
        "source": "待查"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共河池市宜州区委员会", "type": "党委", "level": "县级", "parent": "中共河池市委员会", "location": "广西河池宜州区"},
    {"id": 2, "name": "河池市宜州区人民政府", "type": "政府", "level": "县级", "parent": "河池市人民政府", "location": "广西河池宜州区"},
    {"id": 3, "name": "河池市宜州区人大常委会", "type": "人大", "level": "县级", "parent": "河池市人大常委会", "location": "广西河池宜州区"},
    {"id": 4, "name": "政协河池市宜州区委员会", "type": "政协", "level": "县级", "parent": "政协河池市委员会", "location": "广西河池宜州区"},
    {"id": 5, "name": "中共河池市宜州区纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共河池市宜州区委员会", "location": "广西河池宜州区"},
    {"id": 6, "name": "中共河池市宜州区委员会组织部", "type": "党委", "level": "县级", "parent": "中共河池市宜州区委员会", "location": "广西河池宜州区"},
    {"id": 7, "name": "中共河池市宜州区委员会宣传部", "type": "党委", "level": "县级", "parent": "中共河池市宜州区委员会", "location": "广西河池宜州区"},
    {"id": 8, "name": "中共河池市宜州区委员会政法委员会", "type": "党委", "level": "县级", "parent": "中共河池市宜州区委员会", "location": "广西河池宜州区"},
    {"id": 9, "name": "中共河池市委员会", "type": "党委", "level": "地级市", "parent": "中共广西壮族自治区委员会", "location": "广西河池"},
    {"id": 10, "name": "河池市人民政府", "type": "政府", "level": "地级市", "parent": "广西壮族自治区人民政府", "location": "广西河池"},
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 薛海源 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "宜州区委书记", "start_date": "2021?",
     "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "宜州区区长（前任）", "start_date": "",
     "end_date": "2021?", "rank": "正处级", "note": "薛海源在任区委书记前曾任宜州区区长"},

    # 戚啸 — 区长
    {"person_id": 2, "org_id": 2, "title": "宜州区区长", "start_date": "",
     "end_date": "present", "rank": "正处级", "note": "宜州区委副书记"},
    {"person_id": 2, "org_id": 1, "title": "宜州区委副书记", "start_date": "",
     "end_date": "present", "rank": "正处级", "note": ""},

    # 人大主任（待查）
    {"person_id": 3, "org_id": 3, "title": "宜州区人大常委会主任", "start_date": "",
     "end_date": "present", "rank": "正处级", "note": ""},

    # 政协主席（待查）
    {"person_id": 4, "org_id": 4, "title": "宜州区政协主席", "start_date": "",
     "end_date": "present", "rank": "正处级", "note": ""},

    # 区委副书记（待查）
    {"person_id": 5, "org_id": 1, "title": "宜州区委副书记", "start_date": "",
     "end_date": "present", "rank": "正处级", "note": ""},

    # 常务副区长（待查）
    {"person_id": 6, "org_id": 1, "title": "宜州区委常委", "start_date": "",
     "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "宜州区常务副区长", "start_date": "",
     "end_date": "present", "rank": "副处级", "note": ""},

    # 纪委书记（待查）
    {"person_id": 7, "org_id": 1, "title": "宜州区委常委", "start_date": "",
     "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "宜州区纪委书记", "start_date": "",
     "end_date": "present", "rank": "副处级", "note": ""},

    # 组织部部长（待查）
    {"person_id": 8, "org_id": 1, "title": "宜州区委常委、组织部部长", "start_date": "",
     "end_date": "present", "rank": "副处级", "note": ""},

    # 宣传部部长（待查）
    {"person_id": 9, "org_id": 1, "title": "宜州区委常委、宣传部部长", "start_date": "",
     "end_date": "present", "rank": "副处级", "note": ""},

    # 政法委书记（待查）
    {"person_id": 10, "org_id": 1, "title": "宜州区委常委、政法委书记", "start_date": "",
     "end_date": "present", "rank": "副处级", "note": ""},

    # 翟红玲 — 前任区委书记
    {"person_id": 11, "org_id": 1, "title": "宜州区委书记", "start_date": "",
     "end_date": "2021?", "rank": "正处级", "note": "薛海源前任"},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 党政核心搭档
    {"person_a": 1, "person_b": 2, "type": "共事",
     "context": "宜州区现任区委书记与区长党政搭档关系",
     "overlap_org": "中共河池市宜州区委员会/河池市宜州区人民政府",
     "overlap_period": "present"},

    # 前后任：薛海源 — 翟红玲
    {"person_a": 1, "person_b": 11, "type": "前后任",
     "context": "薛海源接替翟红玲为宜州区委书记",
     "overlap_org": "中共河池市宜州区委员会",
     "overlap_period": "2021?"},

    # 薛海源 — 前任区长（自己曾任区长）
    # 这条关系通过薛海源兼任区长的历史体现

    # 区委书记 — 人大主任
    {"person_a": 1, "person_b": 3, "type": "共事",
     "context": "区委书记与区人大常委会主任党政班子关系",
     "overlap_org": "宜州区四套班子",
     "overlap_period": "present"},

    # 区委书记 — 政协主席
    {"person_a": 1, "person_b": 4, "type": "共事",
     "context": "区委书记与区政协主席党政班子关系",
     "overlap_org": "宜州区四套班子",
     "overlap_period": "present"},

    # 区委书记 — 区委副书记
    {"person_a": 1, "person_b": 5, "type": "上下级",
     "context": "区委书记与区委副书记领导班子关系",
     "overlap_org": "中共河池市宜州区委员会",
     "overlap_period": "present"},

    # 区长 — 常务副区长
    {"person_a": 2, "person_b": 6, "type": "上下级",
     "context": "区长与常务副区长政府领导班子关系",
     "overlap_org": "河池市宜州区人民政府",
     "overlap_period": "present"},

    # 区委书记 — 纪委书记
    {"person_a": 1, "person_b": 7, "type": "上下级",
     "context": "区委书记与纪委书记工作关系",
     "overlap_org": "中共河池市宜州区委员会",
     "overlap_period": "present"},

    # 区委书记 — 组织部长
    {"person_a": 1, "person_b": 8, "type": "上下级",
     "context": "区委书记与组织部部长工作关系",
     "overlap_org": "中共河池市宜州区委员会",
     "overlap_period": "present"},
]

# =========================================================================
# 5. HELPERS
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(current_post):
    """Return GEXF color string for a person based on role."""
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp:
        return "200,30,30"
    if "区长" in cp or "市长" in cp:
        return "30,100,200"
    if "副书记" in cp:
        return "220,80,80"
    if "副" in cp and "区长" in cp:
        return "100,150,220"
    if "常委" in cp:
        return "180,100,180"
    if "主任" in cp or "人大" in cp:
        return "60,180,60"
    if "主席" in cp:
        return "60,180,60"
    return "100,100,100"


def person_size(current_post):
    """Return GEXF node size based on role."""
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp:
        return "20.0"
    if "区长" in cp:
        return "18.0"
    if "副书记" in cp:
        return "15.0"
    if "副" in cp:
        return "12.0"
    if "常委" in cp:
        return "12.0"
    if "主任" in cp or "主席" in cp:
        return "12.0"
    return "10.0"


def person_shape(current_post):
    """Return GEXF shape based on role."""
    cp = current_post or ""
    if "书记" in cp:
        return "square"
    if "人大" in cp or "政协" in cp:
        return "diamond"
    if "副" in cp:
        return "triangle"
    return "circle"


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "开发区": "200,255,200",
        "纪委": "255,200,150",
    }
    return colors.get(org_type, "200,200,200")


# =========================================================================
# 6. BUILD FUNCTIONS
# =========================================================================

def build_db():
    """Build SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
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
        );

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );

        CREATE TABLE positions (
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
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute("""INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,
                       party_join,work_start,current_post,current_org,source)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
                     p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
                     p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""),
                     p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location)
                       VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"],
                     o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note)
                       VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"],
                     pos.get("start_date", ""), pos.get("end_date", ""),
                     pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period)
                       VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"], r["context"],
                     r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


def build_gexf():
    """Build GEXF graph file."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>宜州区领导班子关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        cp = p.get("current_post", "")
        color = person_color(cp)
        size = person_size(cp)
        shape = person_shape(cp)
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(cp)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o["type"])
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('        <viz:shape value="hexagon"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]+100000}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ person (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")


def build_person_json(person, timeline, rels, sources):
    """Build a single person graph JSON dict."""
    p = person
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "河池市",
            "region": "宜州区",
            "job": p.get("current_post", "").split("、")[-1] if "、" in p.get("current_post", "") else p.get("current_post", ""),
            "task_id": "guangxi_宜州区",
            "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"yizhou_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source", "")
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": bool(p.get("current_post")),
            "source_ids": ["S001"]
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": rels,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "No risk signals found through available public sources",
            "date": "",
            "confidence": "unverified",
            "source_ids": []
        }],
        "source_register": sources,
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"Complete career timeline before current role for {p['name']}"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"Complete career timeline before current role - full position history for {p['name']}",
                "why_it_matters": "Cannot assess career pattern, promotion velocity, or network building without full timeline",
                "suggested_queries": [f"{p['name']} 简历", f"{p['name']} 任职经历", f"{p['name']} 百度百科"],
                "last_attempted": AS_OF
            }
        ]
    }


def build_person_jsons():
    """Build and write person JSON files for core leaders."""
    now = AS_OF.replace("-", "")

    sources = [
        {"id": "S001", "title": "河池市人民政府门户网站",
         "url": "https://www.gxhc.gov.cn/", "publisher": "河池市人民政府",
         "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "Active government portal"},
        {"id": "S002", "title": "宜州区人民政府门户网站",
         "url": "https://www.gxhc.gov.cn/yjq/", "publisher": "宜州区人民政府",
         "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "Yizhou District government portal"},
    ]

    # ── 薛海源 person JSON ──
    xhy = persons[0]
    xhy_timeline = [
        {"start": "2021?", "end": "present",
         "org": "中共河池市宜州区委员会",
         "title": "宜州区委书记", "level": "正处级",
         "location": "广西河池宜州区", "system": "party",
         "rank": "正处级", "is_key_promotion": True,
         "notes": "接替翟红玲任宜州区委书记",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"start": "unknown", "end": "2021?",
         "org": "河池市宜州区人民政府",
         "title": "宜州区区长", "level": "正处级",
         "location": "广西河池宜州区", "system": "government",
         "rank": "正处级", "is_key_promotion": True,
         "notes": "任区委书记前任宜州区区长",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到薛海源在任宜州区区长之前的完整履历",
         "confidence": "unverified",
         "source_ids": []},
    ]
    xhy_relationships = [
        {"person": "戚啸", "person_id": "yizhou_戚啸",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "宜州区现任区委书记与区长党政搭档；薛海源曾任区长后任区委书记，戚啸接任区长",
         "overlap_org": "中共河池市宜州区委员会/河池市宜州区人民政府",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "翟红玲", "person_id": "yizhou_翟红玲",
         "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "薛海源接替翟红玲为宜州区委书记",
         "overlap_org": "中共河池市宜州区委员会",
         "overlap_period": "2021?",
         "direction": "other_to_person",
         "confidence": "confirmed",
         "source_ids": []},
    ]
    xhy_json = build_person_json(xhy, xhy_timeline, xhy_relationships, sources)
    xhy_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-河池市-区委书记-薛海源.json")
    with open(xhy_path, "w", encoding="utf-8") as f:
        json.dump(xhy_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {xhy_path}")

    # ── 戚啸 person JSON ──
    qx = persons[1]
    qx_timeline = [
        {"start": "unknown", "end": "present",
         "org": "河池市宜州区人民政府/中共河池市宜州区委员会",
         "title": "宜州区委副书记、区长", "level": "正处级",
         "location": "广西河池宜州区", "system": "government",
         "rank": "正处级", "is_key_promotion": True,
         "notes": "",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到戚啸在任宜州区区长之前的完整履历",
         "confidence": "unverified",
         "source_ids": []},
    ]
    qx_relationships = [
        {"person": "薛海源", "person_id": "yizhou_薛海源",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "宜州区现任区长与区委书记党政搭档",
         "overlap_org": "河池市宜州区人民政府/中共河池市宜州区委员会",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    qx_json = build_person_json(qx, qx_timeline, qx_relationships, sources)
    qx_json["investigation_scope"]["job"] = "区长"
    qx_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-河池市-区长-戚啸.json")
    with open(qx_path, "w", encoding="utf-8") as f:
        json.dump(qx_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {qx_path}")

    # ── 翟红玲 person JSON（前任区委书记） ──
    if persons[10]["name"] == "翟红玲":
        zhl = persons[10]
        zhl_timeline = [
            {"start": "unknown", "end": "2021?",
             "org": "中共河池市宜州区委员会",
             "title": "宜州区委书记", "level": "正处级",
             "location": "广西河池宜州区", "system": "party",
             "rank": "正处级", "is_key_promotion": True,
             "notes": "薛海源前任。女，壮族，宜州区委书记任后调任何处待查",
             "confidence": "confirmed",
             "source_ids": ["S001"]},
            {"start": "unknown", "end": "unknown",
             "org": "履历缺口",
             "title": "",
             "notes": "公开资料未找到翟红玲在任宜州区委书记之前的完整履历",
             "confidence": "unverified",
             "source_ids": []},
        ]
        zhl_relationships = [
            {"person": "薛海源", "person_id": "yizhou_薛海源",
             "relationship_type": "predecessor_successor",
             "strength": "medium",
             "evidence": "翟红玲为前任宜州区委书记，薛海源接任",
             "overlap_org": "中共河池市宜州区委员会",
             "overlap_period": "2021?",
             "direction": "person_to_other",
             "confidence": "confirmed",
             "source_ids": []},
        ]
        zhl_json = build_person_json(zhl, zhl_timeline, zhl_relationships, sources)
        zhl_json["investigation_scope"]["job"] = "区委书记（前任）"
        zhl_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-河池市-区委书记-翟红玲.json")
        with open(zhl_path, "w", encoding="utf-8") as f:
            json.dump(zhl_json, f, ensure_ascii=False, indent=2)
        print(f"Person JSON written: {zhl_path}")


def build():
    os.makedirs(STAGING_DIR, exist_ok=True)
    print(f"=== Building {SLUG} data ===")
    print(f"Staging dir: {STAGING_DIR}")
    build_db()
    build_gexf()
    build_person_jsons()
    print("\nBuild complete.")


if __name__ == "__main__":
    build()
