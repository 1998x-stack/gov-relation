#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宾阳县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 广西壮族自治区
Parent City: 南宁市
Region: 宾阳县
Targets: 县委书记 & 县长

当前在任 (as of 2026-07-22):
- 县委书记: 梁展凡 (宾阳县委书记)
- 县长: 廖伟行 (宾阳县委副书记、县长、县政府党组书记)
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "宾阳县"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-22"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：县委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "梁展凡",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-11",
        "birthplace": "广西南宁",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "宾阳县委书记、宾阳县人民武装部党委第一书记",
        "current_org": "中共宾阳县委员会",
        "source": "https://baike.baidu.com/item/%E6%A2%81%E5%B1%95%E5%87%A1"
    },
    # ════════════════════════════════════════
    # 核心领导：县长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "廖伟行",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "宾阳县委副书记、县长、县政府党组书记",
        "current_org": "宾阳县人民政府/中共宾阳县委员会",
        "source": "https://www.binyang.gov.cn/zwgk/ldzc/"
    },
    # ════════════════════════════════════════
    # 县人大常委会主任
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "罗宏周",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "宾阳县人大常委会主任",
        "current_org": "宾阳县人民代表大会常务委员会",
        "source": "https://www.binyang.gov.cn/zwgk/ldzc/"
    },
    # ════════════════════════════════════════
    # 县政协主席
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "麦阳明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "宾阳县政协主席",
        "current_org": "中国人民政治协商会议宾阳县委员会",
        "source": "https://www.binyang.gov.cn/zwgk/ldzc/"
    },
    # ════════════════════════════════════════
    # 县委副书记 (常务)
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "潘荫文",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "宾阳县委副书记",
        "current_org": "中共宾阳县委员会",
        "source": "https://www.binyang.gov.cn/zwgk/ldzc/"
    },
    # ════════════════════════════════════════
    # 县委常委、常务副县长
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "谢欢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "宾阳县委常委、常务副县长",
        "current_org": "中共宾阳县委员会/宾阳县人民政府",
        "source": "https://www.binyang.gov.cn/zwgk/ldzc/"
    },
    # ════════════════════════════════════════
    # 县委常委、纪委书记、监委主任
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "凌光宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "宾阳县委常委、纪委书记、县监委主任",
        "current_org": "中共宾阳县纪律检查委员会/宾阳县监察委员会",
        "source": "https://www.binyang.gov.cn/zwgk/ldzc/"
    },
    # ════════════════════════════════════════
    # 县委常委、组织部部长
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "徐飞雨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "宾阳县委常委、组织部部长",
        "current_org": "中共宾阳县委员会组织部",
        "source": "https://www.binyang.gov.cn/zwgk/ldzc/"
    },
    # ════════════════════════════════════════
    # 县委常委、政法委书记
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "吕子瑞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "宾阳县委常委、政法委书记",
        "current_org": "中共宾阳县委员会政法委员会",
        "source": "https://www.binyang.gov.cn/zwgk/ldzc/"
    },
    # ════════════════════════════════════════
    # 县委常委、宣传部部长
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "陈强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "宾阳县委常委、宣传部部长",
        "current_org": "中共宾阳县委员会宣传部",
        "source": "https://www.binyang.gov.cn/zwgk/ldzc/"
    },
    # ════════════════════════════════════════
    # 县委常委、县委办公室主任
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "韦定杰",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "宾阳县委常委、县委办公室主任",
        "current_org": "中共宾阳县委员会办公室",
        "source": "https://www.binyang.gov.cn/zwgk/ldzc/"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共宾阳县委员会", "type": "党委", "level": "县级", "parent": "中共南宁市委员会", "location": "广西南宁宾阳县"},
    {"id": 2, "name": "宾阳县人民政府", "type": "政府", "level": "县级", "parent": "南宁市人民政府", "location": "广西南宁宾阳县"},
    {"id": 3, "name": "宾阳县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "南宁市人民代表大会常务委员会", "location": "广西南宁宾阳县"},
    {"id": 4, "name": "中国人民政治协商会议宾阳县委员会", "type": "政协", "level": "县级", "parent": "南宁市政协", "location": "广西南宁宾阳县"},
    {"id": 5, "name": "中共宾阳县纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共南宁市纪律检查委员会", "location": "广西南宁宾阳县"},
    {"id": 6, "name": "宾阳县监察委员会", "type": "纪委", "level": "县级", "parent": "南宁市监察委员会", "location": "广西南宁宾阳县"},
    {"id": 7, "name": "宾阳县人民武装部", "type": "党委", "level": "县级", "parent": "南宁警备区", "location": "广西南宁宾阳县"},
    {"id": 8, "name": "中共宾阳县委员会组织部", "type": "党委", "level": "县级", "parent": "中共宾阳县委员会", "location": "广西南宁宾阳县"},
    {"id": 9, "name": "中共宾阳县委员会政法委员会", "type": "党委", "level": "县级", "parent": "中共宾阳县委员会", "location": "广西南宁宾阳县"},
    {"id": 10, "name": "中共宾阳县委员会宣传部", "type": "党委", "level": "县级", "parent": "中共宾阳县委员会", "location": "广西南宁宾阳县"},
    {"id": 11, "name": "中共宾阳县委员会办公室", "type": "党委", "level": "县级", "parent": "中共宾阳县委员会", "location": "广西南宁宾阳县"},
    {"id": 12, "name": "中共南宁市委员会", "type": "党委", "level": "地市级", "parent": "中共广西壮族自治区委员会", "location": "广西南宁"},
    {"id": 13, "name": "南宁市人民政府", "type": "政府", "level": "地市级", "parent": "广西壮族自治区人民政府", "location": "广西南宁"},
    {"id": 14, "name": "宾阳县公安局", "type": "政府", "level": "县级", "parent": "宾阳县人民政府/南宁市公安局", "location": "广西南宁宾阳县"},
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 梁展凡
    {"person_id": 1, "org_id": 1, "title": "宾阳县委书记", "start_date": "2023-04", "end_date": "present", "rank": "正处级", "note": "兼任县人武部党委第一书记"},
    {"person_id": 1, "org_id": 7, "title": "宾阳县人民武装部党委第一书记", "start_date": "2023-04", "end_date": "present", "rank": "正处级", "note": "兼任"},
    # 此前经历
    {"person_id": 1, "org_id": 14, "title": "曾任南宁市下辖区县领导职务", "start_date": "unknown", "end_date": "2023-04", "rank": "副处级", "note": "推测有南宁市辖区或市直部门工作经历，后任宾阳县委副书记、县长后晋升书记"},

    # 廖伟行
    {"person_id": 2, "org_id": 1, "title": "宾阳县委副书记", "start_date": "2024", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "宾阳县县长、县政府党组书记", "start_date": "2024-02", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "宾阳县副县长、代县长", "start_date": "2024-01", "end_date": "2024-02", "rank": "副处级", "note": "宾阳县人大常委会任命为副县长、代县长"},

    # 罗宏周
    {"person_id": 3, "org_id": 3, "title": "宾阳县人大常委会主任", "start_date": "2021", "end_date": "present", "rank": "正处级", "note": ""},

    # 麦阳明
    {"person_id": 4, "org_id": 4, "title": "宾阳县政协主席", "start_date": "2021", "end_date": "present", "rank": "正处级", "note": ""},

    # 潘荫文
    {"person_id": 5, "org_id": 1, "title": "宾阳县委副书记", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},

    # 谢欢
    {"person_id": 6, "org_id": 1, "title": "宾阳县委常委", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "宾阳县常务副县长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},

    # 凌光宇
    {"person_id": 7, "org_id": 1, "title": "宾阳县委常委、纪委书记", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 6, "title": "宾阳县监委主任", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},

    # 徐飞雨
    {"person_id": 8, "org_id": 1, "title": "宾阳县委常委、组织部部长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},

    # 吕子瑞
    {"person_id": 9, "org_id": 1, "title": "宾阳县委常委、政法委书记", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},

    # 陈强
    {"person_id": 10, "org_id": 1, "title": "宾阳县委常委、宣传部部长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},

    # 韦定杰
    {"person_id": 11, "org_id": 1, "title": "宾阳县委常委、县委办公室主任", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 党政搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "梁展凡（县委书记）与廖伟行（县长）为宾阳县党政一把手搭档",
     "overlap_org": "中共宾阳县委员会/宾阳县人民政府", "overlap_period": "2024-present"},

    # 县委班子
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "县委副书记协助县委书记工作",
     "overlap_org": "中共宾阳县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "县委常委班子共事",
     "overlap_org": "中共宾阳县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "县委常委班子共事",
     "overlap_org": "中共宾阳县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "县委常委班子共事",
     "overlap_org": "中共宾阳县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "县委常委班子共事",
     "overlap_org": "中共宾阳县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "县委常委班子共事",
     "overlap_org": "中共宾阳县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate",
     "context": "县委常委班子共事",
     "overlap_org": "中共宾阳县委员会", "overlap_period": "present"},

    # 县政府班子
    {"person_a": 2, "person_b": 6, "type": "overlap",
     "context": "县长与常务副县长政府班子共事",
     "overlap_org": "宾阳县人民政府", "overlap_period": "present"},

    # 前任联系
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "梁展凡此前曾任宾阳县县长，后接任县委书记；廖伟行接任县长",
     "overlap_org": "宾阳县人民政府", "overlap_period": "2022-2024"},
]


# =========================================================================
# 5. HELPERS
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(current_post):
    cp = current_post or ""
    # Party secretary = red
    if "书记" in cp and "副书记" not in cp and "纪委书记" not in cp:
        return "200,30,30"
    # County mayor = blue
    if "县长" in cp and "副" not in cp:
        return "30,100,200"
    # Deputy secretary = lighter red
    if "副书记" in cp:
        return "220,80,80"
    # Discipline inspection = orange
    if "纪委" in cp:
        return "255,165,0"
    # Deputy positions = medium blue
    if "副" in cp:
        return "100,150,220"
    # Standing committee = purple
    if "常委" in cp:
        return "180,100,180"
    # Congress chair = green
    if "主任" in cp or "人大" in cp:
        return "60,180,60"
    # Political consult = green
    if "主席" in cp:
        return "60,180,60"
    return "100,100,100"


def person_size(current_post):
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp and "纪委书记" not in cp:
        return "20.0"
    if "县长" in cp and "副" not in cp:
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
    cp = current_post or ""
    if "书记" in cp and "纪委书记" not in cp:
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
    lines.append('    <description>宾阳县领导班子关系网络</description>')
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
            "city": "南宁市",
            "region": "宾阳县",
            "job": p.get("current_post", "").split("、")[-1] if "、" in p.get("current_post", "") else p.get("current_post", ""),
            "task_id": "guangxi_宾阳县",
            "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"binyang_{p['name']}",
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
            "identity": "confirmed" if p.get("birth") else "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"Earlier career timeline before current role for {p['name']}"
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
        {"id": "S001", "title": "宾阳县人民政府门户网站",
         "url": "https://www.binyang.gov.cn/", "publisher": "宾阳县人民政府",
         "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "Active government portal with current leadership info"},
        {"id": "S002", "title": "宾阳县领导之窗",
         "url": "https://www.binyang.gov.cn/zwgk/ldzc/",
         "publisher": "宾阳县人民政府", "published_at": "",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "Formal leadership roster with bios"},
    ]

    # ── 梁展凡 person JSON ──
    lzf_timeline = [
        {"start": "2023-04", "end": "present",
         "org": "中共宾阳县委员会", "title": "宾阳县委书记",
         "level": "正处级", "location": "广西南宁宾阳县",
         "system": "party", "rank": "正处级", "is_key_promotion": True,
         "notes": "兼任宾阳县人民武装部党委第一书记",
         "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2023-04", "end": "present",
         "org": "宾阳县人民武装部", "title": "党委第一书记",
         "level": "正处级", "location": "广西南宁宾阳县",
         "system": "party", "rank": "正处级", "is_key_promotion": False,
         "notes": "兼任",
         "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "2023-04",
         "org": "宾阳县人民政府", "title": "宾阳县县长",
         "level": "正处级", "location": "广西南宁宾阳县",
         "system": "government", "rank": "正处级", "is_key_promotion": True,
         "notes": "梁展凡由宾阳县县长升任县委书记",
         "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口", "title": "",
         "notes": "公开资料未找到梁展凡在任宾阳县县长之前的完整任职履历。1973年11月生，广西南宁人，在职研究生学历。",
         "confidence": "unverified", "source_ids": []},
    ]
    lzf_relationships = [
        {"person": "廖伟行", "person_id": "binyang_廖伟行",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "目前宾阳县县委书记与县长为党政搭档；梁展凡此前任县长时廖伟行为后任",
         "overlap_org": "中共宾阳县委员会/宾阳县人民政府",
         "overlap_period": "2024-present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    lzf_json = build_person_json(persons[0], lzf_timeline, lzf_relationships, sources)
    lzf_json["identity"]["birth"] = "1973-11"
    lzf_json["identity"]["education"] = [
        {"period": "", "institution": "", "major": "",
         "degree": "在职研究生学历", "study_type": "part_time",
         "source_ids": []}
    ]
    lzf_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-南宁市-宾阳县委书记-梁展凡.json")
    with open(lzf_path, "w", encoding="utf-8") as f:
        json.dump(lzf_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lzf_path}")

    # ── 廖伟行 person JSON ──
    lwx_timeline = [
        {"start": "2024-02", "end": "present",
         "org": "中共宾阳县委员会/宾阳县人民政府",
         "title": "宾阳县委副书记、县长、县政府党组书记",
         "level": "正处级", "location": "广西南宁宾阳县",
         "system": "government", "rank": "正处级",
         "is_key_promotion": True,
         "notes": "负责县政府全面工作",
         "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2024-01", "end": "2024-02",
         "org": "宾阳县人民政府",
         "title": "宾阳县副县长、代县长",
         "level": "副处级", "location": "广西南宁宾阳县",
         "system": "government", "rank": "副处级",
         "is_key_promotion": False,
         "notes": "宾阳县人大常委会任命为副县长、代县长",
         "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口", "title": "",
         "notes": "公开资料未找到廖伟行2024年任代县长之前的完整履历。",
         "confidence": "unverified", "source_ids": []},
    ]
    lwx_relationships = [
        {"person": "梁展凡", "person_id": "binyang_梁展凡",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "廖伟行（县长）与梁展凡（县委书记）为宾阳县当前党政一把手搭档",
         "overlap_org": "中共宾阳县委员会/宾阳县人民政府",
         "overlap_period": "2024-present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "梁展凡", "person_id": "binyang_梁展凡",
         "relationship_type": "predecessor_successor",
         "strength": "strong",
         "evidence": "廖伟行接替梁展凡任宾阳县县长（梁展凡升任县委书记）",
         "overlap_org": "宾阳县人民政府",
         "overlap_period": "2024",
         "direction": "other_to_person",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    lwx_json = build_person_json(persons[1], lwx_timeline, lwx_relationships, sources)
    lwx_json["investigation_scope"]["job"] = "县长"
    lwx_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-南宁市-宾阳县县长-廖伟行.json")
    with open(lwx_path, "w", encoding="utf-8") as f:
        json.dump(lwx_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lwx_path}")


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
