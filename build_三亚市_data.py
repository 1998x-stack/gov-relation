#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三亚市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 地级市
Province: 海南省
Region: 三亚市
Targets: 市委书记 & 市长

官方来源（截至2026-07-23）:
- https://www.sanya.gov.cn/ — 三亚市人民政府门户网站
- 省构建脚本: build_海南省_data.py (含王祺扬在省委常委中的信息)

当前在任 (as of 2026-07-23):
- 市委书记: 王祺扬（海南省委常委、三亚市委书记）
- 市长: 陈希（三亚市委副书记、市长）
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "三亚市"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-23"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：市委书记（副部级 — 省委常委兼任）
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "王祺扬",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "海南省委常委、三亚市委书记",
        "current_org": "中共三亚市委员会",
        "source": "https://www.sanya.gov.cn/"
    },
    # ════════════════════════════════════════
    # 核心领导：市长（正厅级）
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "陈希",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三亚市委副书记、市长",
        "current_org": "三亚市人民政府",
        "source": "https://www.sanya.gov.cn/"
    },
    # ════════════════════════════════════════
    # 副市长们
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "陈景进",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三亚市委常委、常务副市长",
        "current_org": "三亚市人民政府",
        "source": "https://www.sanya.gov.cn/"
    },
    {
        "id": 4,
        "name": "向义海",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三亚市委常委、副市长",
        "current_org": "三亚市人民政府",
        "source": "https://www.sanya.gov.cn/"
    },
    {
        "id": 5,
        "name": "张长丰",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三亚市副市长",
        "current_org": "三亚市人民政府",
        "source": "https://www.sanya.gov.cn/"
    },
    {
        "id": 6,
        "name": "尹承玲",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三亚市副市长",
        "current_org": "三亚市人民政府",
        "source": "https://www.sanya.gov.cn/"
    },
    {
        "id": 7,
        "name": "范维正",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三亚市副市长",
        "current_org": "三亚市人民政府",
        "source": "https://www.sanya.gov.cn/"
    },
    {
        "id": 8,
        "name": "陈志伟",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三亚市副市长",
        "current_org": "三亚市人民政府",
        "source": "https://www.sanya.gov.cn/"
    },
    {
        "id": 9,
        "name": "陈克伯",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三亚市副市长",
        "current_org": "三亚市人民政府",
        "source": "https://www.sanya.gov.cn/"
    },
    {
        "id": 10,
        "name": "樊木",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三亚市副市长",
        "current_org": "三亚市人民政府",
        "source": "https://www.sanya.gov.cn/"
    },
    # ════════════════════════════════════════
    # 市政府秘书长
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "杨军建",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三亚市人民政府秘书长",
        "current_org": "三亚市人民政府",
        "source": "https://www.sanya.gov.cn/"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共三亚市委员会", "type": "党委", "level": "地级", "parent": "中共海南省委员会", "location": "海南省三亚市"},
    {"id": 2, "name": "三亚市人民政府", "type": "政府", "level": "地级", "parent": "海南省人民政府", "location": "海南省三亚市"},
    {"id": 3, "name": "三亚市人民代表大会常务委员会", "type": "人大", "level": "地级", "parent": "", "location": "海南省三亚市"},
    {"id": 4, "name": "政协三亚市委员会", "type": "政协", "level": "地级", "parent": "", "location": "海南省三亚市"},
    {"id": 5, "name": "中共海南省委员会", "type": "党委", "level": "省级", "parent": "", "location": "海南省海口市"},
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # ── 王祺扬 (id=1) ──
    {"person_id": 1, "org_id": 1, "title": "三亚市委书记", "start": "", "end": "present", "rank": "副部级", "note": "海南省委常委兼任三亚市委书记"},
    {"person_id": 1, "org_id": 5, "title": "海南省委常委", "start": "", "end": "present", "rank": "副部级", "note": ""},

    # ── 陈希 (id=2) ──
    {"person_id": 2, "org_id": 1, "title": "三亚市委副书记", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "三亚市市长", "start": "", "end": "present", "rank": "正厅级", "note": ""},

    # ── 陈景进 (id=3) ──
    {"person_id": 3, "org_id": 2, "title": "三亚市委常委、常务副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "三亚市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},

    # ── 向义海 (id=4) ──
    {"person_id": 4, "org_id": 2, "title": "三亚市委常委、副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "三亚市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},

    # ── 张长丰 (id=5) ──
    {"person_id": 5, "org_id": 2, "title": "三亚市副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},

    # ── 尹承玲 (id=6) ──
    {"person_id": 6, "org_id": 2, "title": "三亚市副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},

    # ── 范维正 (id=7) ──
    {"person_id": 7, "org_id": 2, "title": "三亚市副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},

    # ── 陈志伟 (id=8) ──
    {"person_id": 8, "org_id": 2, "title": "三亚市副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},

    # ── 陈克伯 (id=9) ──
    {"person_id": 9, "org_id": 2, "title": "三亚市副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},

    # ── 樊木 (id=10) ──
    {"person_id": 10, "org_id": 2, "title": "三亚市副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},

    # ── 杨军建 (id=11) ──
    {"person_id": 11, "org_id": 2, "title": "三亚市人民政府秘书长", "start": "", "end": "present", "rank": "正处级", "note": ""},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 核心搭档：王祺扬 ↔ 陈希（党政一把手）──
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "三亚市市委书记与市长党政搭档", "overlap_org": "中共三亚市委员会/三亚市人民政府", "overlap_period": "present"},
    # ── 陈景进 ↔ 陈希（政府班子副班长）──
    {"person_a": 3, "person_b": 2, "type": "overlap", "context": "三亚市委常委、常务副市长与市长政府班子搭档", "overlap_org": "三亚市人民政府", "overlap_period": "present"},
    # ── 向义海 ↔ 陈希（政府班子副班长）──
    {"person_a": 4, "person_b": 2, "type": "overlap", "context": "三亚市委常委、副市长与市长政府班子搭档", "overlap_org": "三亚市人民政府", "overlap_period": "present"},
    # ── 陈景进 ↔ 王祺扬（市委常委同事）──
    {"person_a": 3, "person_b": 1, "type": "overlap", "context": "三亚市委常委班子同事", "overlap_org": "中共三亚市委员会", "overlap_period": "present"},
    # ── 向义海 ↔ 王祺扬（市委常委同事）──
    {"person_a": 4, "person_b": 1, "type": "overlap", "context": "三亚市委常委班子同事", "overlap_org": "中共三亚市委员会", "overlap_period": "present"},
    # ── 副市长间的工作关系 ──
    {"person_a": 5, "person_b": 2, "type": "overlap", "context": "三亚市副市长与市长政府班子搭档", "overlap_org": "三亚市人民政府", "overlap_period": "present"},
    {"person_a": 6, "person_b": 2, "type": "overlap", "context": "三亚市副市长与市长政府班子搭档", "overlap_org": "三亚市人民政府", "overlap_period": "present"},
    {"person_a": 7, "person_b": 2, "type": "overlap", "context": "三亚市副市长与市长政府班子搭档", "overlap_org": "三亚市人民政府", "overlap_period": "present"},
    {"person_a": 8, "person_b": 2, "type": "overlap", "context": "三亚市副市长与市长政府班子搭档", "overlap_org": "三亚市人民政府", "overlap_period": "present"},
    {"person_a": 9, "person_b": 2, "type": "overlap", "context": "三亚市副市长与市长政府班子搭档", "overlap_org": "三亚市人民政府", "overlap_period": "present"},
    {"person_a": 10, "person_b": 2, "type": "overlap", "context": "三亚市副市长与市长政府班子搭档", "overlap_org": "三亚市人民政府", "overlap_period": "present"},
    {"person_a": 11, "person_b": 2, "type": "overlap", "context": "三亚市政府秘书长与市长政府班子搭档", "overlap_org": "三亚市人民政府", "overlap_period": "present"},
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
    if "市长" in cp:
        return "30,100,200"
    if "副书记" in cp:
        return "220,80,80"
    if "副" in cp and "市长" in cp:
        return "100,150,220"
    if "常委" in cp:
        return "180,100,180"
    if "秘书长" in cp:
        return "200,160,50"
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
    if "市长" in cp:
        return "18.0"
    if "副书记" in cp:
        return "15.0"
    if "副" in cp:
        return "12.0"
    if "常委" in cp:
        return "12.0"
    if "秘书长" in cp:
        return "10.0"
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
    lines.append('    <description>三亚市领导班子关系网络</description>')
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
            "province": "海南省",
            "city": "三亚市",
            "region": "三亚市",
            "job": p.get("current_post", "").split("、")[-1] if "、" in p.get("current_post", "") else p.get("current_post", ""),
            "task_id": "hainan_三亚市",
            "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"sanya_{p['name']}",
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
            "administrative_rank": "副部级" if "书记" in p.get("current_post", "") and "副书记" not in p.get("current_post", "") else "正厅级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
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
            "identity": "confirmed",
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
        {"id": "S001", "title": "三亚市人民政府门户网站",
         "url": "https://www.sanya.gov.cn/", "publisher": "三亚市人民政府",
         "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "Active government portal with current leadership info"},
    ]

    # ── 王祺扬 person JSON ──
    wqy_timeline = [
        {"start": "", "end": "present",
         "org": "中共三亚市委员会",
         "title": "三亚市委书记", "level": "副部级",
         "location": "海南三亚", "system": "party",
         "rank": "副部级", "is_key_promotion": True,
         "notes": "海南省委常委兼任三亚市委书记",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"start": "", "end": "present",
         "org": "中共海南省委员会",
         "title": "海南省委常委", "level": "副部级",
         "location": "海南海口", "system": "party",
         "rank": "副部级", "is_key_promotion": True,
         "notes": "海南省委常委会成员",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到王祺扬任三亚市委书记之前的完整履历",
         "confidence": "unverified",
         "source_ids": []},
    ]
    wqy_relationships = [
        {"person": "陈希", "person_id": "sanya_陈希",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "目前三亚市市委书记与市长党政搭档",
         "overlap_org": "中共三亚市委员会/三亚市人民政府",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    wqy_json = build_person_json(persons[0], wqy_timeline, wqy_relationships, sources)
    wqy_path = os.path.join(PERSONS_DIR, f"{now}-海南省-三亚市-市委书记-王祺扬.json")
    with open(wqy_path, "w", encoding="utf-8") as f:
        json.dump(wqy_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {wqy_path}")

    # ── 陈希 person JSON ──
    cx_timeline = [
        {"start": "", "end": "present",
         "org": "三亚市人民政府",
         "title": "三亚市市长", "level": "正厅级",
         "location": "海南三亚", "system": "government",
         "rank": "正厅级", "is_key_promotion": True,
         "notes": "",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"start": "", "end": "present",
         "org": "中共三亚市委员会",
         "title": "三亚市委副书记", "level": "正厅级",
         "location": "海南三亚", "system": "party",
         "rank": "正厅级", "is_key_promotion": True,
         "notes": "",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到陈希任三亚市市长之前的完整履历",
         "confidence": "unverified",
         "source_ids": []},
    ]
    cx_relationships = [
        {"person": "王祺扬", "person_id": "sanya_王祺扬",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "目前三亚市市长与市委书记党政搭档",
         "overlap_org": "三亚市人民政府/中共三亚市委员会",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    cx_json = build_person_json(persons[1], cx_timeline, cx_relationships, sources)
    cx_json["investigation_scope"]["job"] = "市长"
    cx_path = os.path.join(PERSONS_DIR, f"{now}-海南省-三亚市-市长-陈希.json")
    with open(cx_path, "w", encoding="utf-8") as f:
        json.dump(cx_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {cx_path}")


# =========================================================================
# 7. MAIN
# =========================================================================

def build():
    """Main build entry point."""
    print(f"=== Building {SLUG} data === (as of {AS_OF})")
    build_db()
    build_gexf()
    build_person_jsons()
    print(f"=== Done === {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


if __name__ == "__main__":
    build()
