#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
良庆区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 市辖区
Province: 广西壮族自治区
Parent City: 南宁市
Region: 良庆区
Targets: 区委书记 & 区长

官方来源（截至2026-07-22）:
- http://www.liangqing.gov.cn/ — 良庆区人民政府门户网站
- http://www.liangqing.gov.cn/xxgk/fdzdgk/jcxxgk/ldjj/ — 领导之窗
- http://www.liangqing.gov.cn/xxgk/fdzdgk/jcxxgk/ldjj/qz/ — 区长邢义波简历
- http://www.liangqing.gov.cn/xxgk/fdzdgk/jcxxgk/ldjj/qz/ldhd/t6679108.html — 区委书记陆广平报道

当前在任 (as of 2026-07-22):
- 区委书记: 陆广平（良庆区委书记、五象新区/自贸试验区南宁片区管委会副主任）
- 区长: 邢义波（良庆区委副书记、区长、区政府党组书记）
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "良庆区"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-22"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：区委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "陆广平",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "良庆区委书记、五象新区（自贸试验区南宁片区）管委会副主任",
        "current_org": "中共南宁市良庆区委员会/五象新区管委会",
        "source": "https://baike.baidu.com/item/%E9%99%86%E5%B9%BF%E5%B9%B3"
    },
    # ════════════════════════════════════════
    # 核心领导：区长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "邢义波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987-06",
        "birthplace": "待查",
        "education": "清华大学研究生学历，理学硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "良庆区委副书记、区长、区政府党组书记",
        "current_org": "南宁市良庆区人民政府/中共南宁市良庆区委员会",
        "source": "http://www.liangqing.gov.cn/xxgk/fdzdgk/jcxxgk/ldjj/qz/"
    },
    # ════════════════════════════════════════
    # 副区长
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "程健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-10",
        "birthplace": "广西宾阳县",
        "education": "广西区党校本科班法律专业（在职本科）",
        "party_join": "中共党员",
        "work_start": "1997-07",
        "current_post": "良庆区副区长、良庆公安分局局长",
        "current_org": "南宁市良庆区人民政府",
        "source": "http://www.liangqing.gov.cn/xxgk/fdzdgk/jcxxgk/ldjj/fqz/t5917656.html"
    },
    {
        "id": 4,
        "name": "李韬",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1981-11",
        "birthplace": "广西南宁",
        "education": "吉林省教育学院汉语言文学专业",
        "party_join": "中共党员",
        "work_start": "2004-10",
        "current_post": "良庆区副区长、区政府党组成员",
        "current_org": "南宁市良庆区人民政府",
        "source": "http://www.liangqing.gov.cn/xxgk/fdzdgk/jcxxgk/ldjj/fqz/t2240970.html"
    },
    {
        "id": 5,
        "name": "卢贵福",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1980-09",
        "birthplace": "广西南宁",
        "education": "广西师范学院土地资源管理专业，在职研究生，管理学硕士",
        "party_join": "中共党员",
        "work_start": "2004-07",
        "current_post": "良庆区副区长、区政府党组成员",
        "current_org": "南宁市良庆区人民政府",
        "source": "http://www.liangqing.gov.cn/xxgk/fdzdgk/jcxxgk/ldjj/fqz/t6280764.html"
    },
    # ════════════════════════════════════════
    # 前任区长 — 李冉（推测为邢义波前任）
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "李冉",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "",
        "current_org": "",
        "source": "http://www.liangqing.gov.cn/xxgk/fdzdgk/jcxxgk/ghjh/ndgzjh/t6285897.html"
    },
    # ════════════════════════════════════════
    # 南宁市委书记（上级）
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "许永锞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-11",
        "birthplace": "广东潮州",
        "education": "本科（北京大学地球物理学）",
        "party_join": "1986-12",
        "work_start": "1991-07",
        "current_post": "广西壮族自治区党委常委、南宁市委书记",
        "current_org": "中共南宁市委员会",
        "source": "https://www.nanning.gov.cn/"
    },
    # ════════════════════════════════════════
    # 南宁市市长（上级）
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "侯刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南宁市委副书记、市长",
        "current_org": "南宁市人民政府",
        "source": "https://www.nanning.gov.cn/"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共南宁市良庆区委员会", "type": "党委", "level": "县级", "parent": "中共南宁市委员会", "location": "广西南宁良庆区"},
    {"id": 2, "name": "南宁市良庆区人民政府", "type": "政府", "level": "县级", "parent": "南宁市人民政府", "location": "广西南宁良庆区"},
    {"id": 3, "name": "南宁市良庆区人大常委会", "type": "人大", "level": "县级", "parent": "南宁市人大常委会", "location": "广西南宁良庆区"},
    {"id": 4, "name": "政协南宁市良庆区委员会", "type": "政协", "level": "县级", "parent": "政协南宁市委员会", "location": "广西南宁良庆区"},
    {"id": 5, "name": "五象新区（自贸试验区南宁片区）管委会", "type": "开发区", "level": "副厅级", "parent": "南宁市人民政府", "location": "广西南宁良庆区（五象新区）"},
    {"id": 6, "name": "南宁市良庆公安分局", "type": "政府", "level": "县级", "parent": "南宁市公安局/南宁市良庆区人民政府", "location": "广西南宁良庆区"},
    {"id": 7, "name": "广西良庆经济开发区管理委员会", "type": "开发区", "level": "县级", "parent": "南宁市良庆区人民政府", "location": "广西南宁良庆区"},
    {"id": 8, "name": "中共南宁市委员会", "type": "党委", "level": "地级市", "parent": "中共广西壮族自治区委员会", "location": "广西南宁"},
    {"id": 9, "name": "南宁市人民政府", "type": "政府", "level": "地级市", "parent": "广西壮族自治区人民政府", "location": "广西南宁"},
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 陆广平 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "良庆区委书记", "start_date": "", "end_date": "present", "rank": "正处级（或副厅级）", "note": "区委书记，主持区委全面工作"},
    {"person_id": 1, "org_id": 5, "title": "五象新区（自贸试验区南宁片区）管委会副主任（兼）", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼任"},

    # 邢义波 — 区长
    {"person_id": 2, "org_id": 1, "title": "良庆区委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "良庆区区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "区政府党组书记"},
    {"person_id": 2, "org_id": 2, "title": "良庆区人民政府党组书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 7, "title": "广西良庆经济开发区管委会主任（兼）", "start_date": "", "end_date": "present", "rank": "正处级", "note": "负责开发区全面工作"},

    # 程健 — 副区长
    {"person_id": 3, "org_id": 2, "title": "良庆区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "公安、司法、信访"},
    {"person_id": 3, "org_id": 6, "title": "良庆公安分局局长（兼）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼任"},

    # 李韬 — 副区长
    {"person_id": 4, "org_id": 2, "title": "良庆区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区政府党组成员；交通、农业农村、乡村振兴、生态环境、水利、退役军人、市场监管"},
    {"person_id": 4, "org_id": 2, "title": "良庆区人民政府党组成员", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # 卢贵福 — 副区长
    {"person_id": 5, "org_id": 2, "title": "良庆区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区政府党组成员；自然资源、林业、住建、城市管理、征地拆迁"},
    {"person_id": 5, "org_id": 2, "title": "良庆区人民政府党组成员", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # 李冉 — 前任区长
    {"person_id": 6, "org_id": 2, "title": "良庆区区长", "start_date": "2022?或更早", "end_date": "2025?（邢义波接任前）", "rank": "正处级", "note": "前任区长，2025年2月仍以区长身份提交政府工作报告"},

    # 上级领导
    {"person_id": 7, "org_id": 8, "title": "南宁市委书记", "start_date": "2024?（自治区党委常委兼任）", "end_date": "present", "rank": "副省级", "note": "自治区党委常委"},
    {"person_id": 7, "org_id": 8, "title": "广西壮族自治区党委常委", "start_date": "2024?", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 8, "org_id": 9, "title": "南宁市委副书记、市长", "start_date": "2024?", "end_date": "present", "rank": "正厅级", "note": "南宁市人民政府全面工作"},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 党政核心搭档
    {"person_a": 1, "person_b": 2, "type": "共事",
     "context": "良庆区现任区委书记与区长党政搭档关系",
     "overlap_org": "中共南宁市良庆区委员会",
     "overlap_period": "present"},

    # 前后任：邢义波 — 李冉
    {"person_a": 2, "person_b": 6, "type": "前后任",
     "context": "邢义波接替李冉为良庆区区长",
     "overlap_org": "南宁市良庆区人民政府",
     "overlap_period": "2025?"},

    # 区长 — 副区长（程健）
    {"person_a": 2, "person_b": 3, "type": "共事",
     "context": "区长与副区长领导关系（公安）",
     "overlap_org": "南宁市良庆区人民政府",
     "overlap_period": "present"},

    # 区长 — 副区长（李韬）
    {"person_a": 2, "person_b": 4, "type": "共事",
     "context": "区长与副区长领导关系",
     "overlap_org": "南宁市良庆区人民政府",
     "overlap_period": "present"},

    # 区长 — 副区长（卢贵福）
    {"person_a": 2, "person_b": 5, "type": "共事",
     "context": "区长与副区长领导关系",
     "overlap_org": "南宁市良庆区人民政府",
     "overlap_period": "present"},

    # 区委书记 — 市委领导
    {"person_a": 1, "person_b": 7, "type": "上下级",
     "context": "良庆区委书记受南宁市委书记领导",
     "overlap_org": "中共南宁市委员会",
     "overlap_period": "present"},

    # 区长 — 市长
    {"person_a": 2, "person_b": 8, "type": "上下级",
     "context": "良庆区区长受南宁市市长领导",
     "overlap_org": "南宁市人民政府",
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
    lines.append('    <description>良庆区领导班子关系网络</description>')
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
            "region": "良庆区",
            "job": p.get("current_post", "").split("、")[-1] if "、" in p.get("current_post", "") else p.get("current_post", ""),
            "task_id": "guangxi_良庆区",
            "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"liangqing_{p['name']}",
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
        {"id": "S001", "title": "南宁市良庆区人民政府门户网站",
         "url": "http://www.liangqing.gov.cn/", "publisher": "良庆区人民政府",
         "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "Active government portal with current leadership info"},
        {"id": "S002", "title": "良庆区领导之窗",
         "url": "http://www.liangqing.gov.cn/xxgk/fdzdgk/jcxxgk/ldjj/",
         "publisher": "良庆区人民政府", "published_at": "",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "Formal leadership roster with bios"},
        {"id": "S003", "title": "良庆区党委专项巡察书记专题会新闻",
         "url": "http://www.liangqing.gov.cn/xxgk/fdzdgk/jcxxgk/ldjj/qz/ldhd/t6679108.html",
         "publisher": "良庆区人民政府", "published_at": "2026-06-25",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "Confirming 陆广平 as party secretary"},
    ]

    # ── 陆广平 person JSON ──
    lgp_timeline = [
        {"start": "", "end": "present",
         "org": "中共南宁市良庆区委员会",
         "title": "良庆区委书记", "level": "正处级（或副厅级）",
         "location": "广西南宁良庆区", "system": "party",
         "rank": "正处级（或副厅级）", "is_key_promotion": True,
         "notes": "五象新区（自贸试验区南宁片区）管委会副主任兼任",
         "confidence": "confirmed",
         "source_ids": ["S003"]},
        {"start": "", "end": "present",
         "org": "五象新区（自贸试验区南宁片区）管委会",
         "title": "管委会副主任", "level": "副厅级",
         "location": "广西南宁良庆区", "system": "development_zone",
         "rank": "副厅级", "is_key_promotion": True,
         "notes": "兼任",
         "confidence": "confirmed",
         "source_ids": ["S003"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到陆广平完整的任职履历。推测已有多年基层或市级工作经验后晋升至良庆区委书记。",
         "confidence": "unverified",
         "source_ids": []},
    ]
    lgp_relationships = [
        {"person": "邢义波", "person_id": "liangqing_邢义波",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "目前良庆区区委书记与区长党政搭档",
         "overlap_org": "中共南宁市良庆区委员会",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S003"]},
        {"person": "许永锞", "person_id": "nanning_许永锞",
         "relationship_type": "superior_subordinate",
         "strength": "strong",
         "evidence": "良庆区委书记受南宁市委书记领导",
         "overlap_org": "中共南宁市委员会",
         "overlap_period": "present",
         "direction": "other_to_person",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    lgp_json = build_person_json(persons[0], lgp_timeline, lgp_relationships, sources)
    lgp_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-南宁市-良庆区委书记-陆广平.json")
    with open(lgp_path, "w", encoding="utf-8") as f:
        json.dump(lgp_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lgp_path}")

    # ── 邢义波 person JSON ──
    xyb_timeline = [
        {"start": "", "end": "present",
         "org": "中共南宁市良庆区委员会/良庆区人民政府",
         "title": "良庆区委副书记、区长、区政府党组书记", "level": "正处级",
         "location": "广西南宁良庆区", "system": "government",
         "rank": "正处级", "is_key_promotion": True,
         "notes": "1987年6月生，清华大学研究生学历，理学硕士。负责城区政府全面工作。",
         "confidence": "confirmed",
         "source_ids": ["S001", "S002"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到邢义波2025年任区长之前的完整履历。1987年生，清华大学硕士，推测为选调生身份进入政坛。",
         "confidence": "unverified",
         "source_ids": []},
    ]
    xyb_relationships = [
        {"person": "陆广平", "person_id": "liangqing_陆广平",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "目前良庆区区长与区委书记党政搭档",
         "overlap_org": "中共南宁市良庆区委员会/南宁市良庆区人民政府",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S003"]},
        {"person": "李冉", "person_id": "liangqing_李冉",
         "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "邢义波接替李冉为良庆区区长",
         "overlap_org": "南宁市良庆区人民政府",
         "overlap_period": "2025?",
         "direction": "person_to_other",
         "confidence": "plausible",
         "source_ids": []},
    ]
    xyb_json = build_person_json(persons[1], xyb_timeline, xyb_relationships, sources)
    xyb_json["identity"]["education"] = [
        {"period": "", "institution": "清华大学", "major": "",
         "degree": "理学硕士", "study_type": "full_time",
         "source_ids": ["S002"]}
    ]
    xyb_json["investigation_scope"]["job"] = "区长"
    xyb_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-南宁市-良庆区区长-邢义波.json")
    with open(xyb_path, "w", encoding="utf-8") as f:
        json.dump(xyb_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {xyb_path}")

    # ── 程健 person JSON ──
    cj_json = build_person_json(persons[2], [
        {"start": "unknown", "end": "present",
         "org": "良庆区人民政府/良庆公安分局",
         "title": "良庆区副区长、良庆公安分局局长", "level": "副处级",
         "location": "广西南宁良庆区", "system": "government",
         "rank": "副处级", "is_key_promotion": True,
         "notes": "1976年10月生，广西宾阳人。1998年1月入党，1997年7月参加工作。广西区党校本科班法律专业毕业。",
         "confidence": "confirmed",
         "source_ids": ["S002"]},
    ], [], sources)
    cj_json["investigation_scope"]["job"] = "副区长"
    cj_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-南宁市-良庆区副区长-程健.json")
    with open(cj_path, "w", encoding="utf-8") as f:
        json.dump(cj_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {cj_path}")

    # ── 李韬 person JSON ──
    lt_json = build_person_json(persons[3], [
        {"start": "unknown", "end": "present",
         "org": "良庆区人民政府",
         "title": "良庆区副区长、区政府党组成员", "level": "副处级",
         "location": "广西南宁良庆区", "system": "government",
         "rank": "副处级", "is_key_promotion": True,
         "notes": "1981年11月生，广西南宁人，壮族。2003年6月入党，2004年10月参加工作。吉林省教育学院汉语言文学专业毕业。",
         "confidence": "confirmed",
         "source_ids": ["S002"]},
    ], [], sources)
    lt_json["investigation_scope"]["job"] = "副区长"
    lt_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-南宁市-良庆区副区长-李韬.json")
    with open(lt_path, "w", encoding="utf-8") as f:
        json.dump(lt_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lt_path}")

    # ── 卢贵福 person JSON ──
    lgf_json = build_person_json(persons[4], [
        {"start": "unknown", "end": "present",
         "org": "良庆区人民政府",
         "title": "良庆区副区长、区政府党组成员", "level": "副处级",
         "location": "广西南宁良庆区", "system": "government",
         "rank": "副处级", "is_key_promotion": True,
         "notes": "1980年9月生，广西南宁人，壮族。2003年4月入党，2004年7月参加工作。广西师范学院土地资源管理专业在职研究生，管理学硕士。",
         "confidence": "confirmed",
         "source_ids": ["S002"]},
    ], [], sources)
    lgf_json["investigation_scope"]["job"] = "副区长"
    lgf_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-南宁市-良庆区副区长-卢贵福.json")
    with open(lgf_path, "w", encoding="utf-8") as f:
        json.dump(lgf_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lgf_path}")


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
