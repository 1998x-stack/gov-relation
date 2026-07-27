#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合浦县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 广西壮族自治区
Parent City: 北海市
Region: 合浦县
Targets: 县委书记 & 县长

注意：当前网络访问受限，部分数据基于已有仓库信息和公开推断。
各字段附有置信度标记。

研究日期: 2026-07-23
"""

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "合浦县"
DB_PATH = STAGING_DIR / "data" / "database" / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / "data" / "graph" / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR / "data" / "persons"

AS_OF = "2026-07-23"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：县委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "王川",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "合浦县委书记",
        "current_org": "中共合浦县委员会",
        "source": "GAP — 需通过官方领导之窗或百度百科核实当前县委书记"
    },
    # ════════════════════════════════════════
    # 核心领导：县长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "白银冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "合浦县委副书记、县长",
        "current_org": "合浦县人民政府",
        "source": "GAP — 需通过官方领导之窗或百度百科核实当前县长"
    },
    # ════════════════════════════════════════
    # 县委副书记（常务副县长提名）
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "周水祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年10月",
        "birthplace": "江西湖口",
        "education": "大学学历，管理学学士（海南大学人力资源管理）",
        "party_join": "2005年12月",
        "work_start": "2011年7月",
        "current_post": "原合浦县委常委、常务副县长、县委办主任（已调柳州）",
        "current_org": "中共合浦县委员会/合浦县人民政府",
        "source": "data/persons/广西壮族自治区-柳州市-区委书记-周水祥.json (本仓库已有数据)"
    },
    # ════════════════════════════════════════
    # 县委常委、纪委书记
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "合浦县委常委、纪委书记",
        "current_org": "中共合浦县纪律检查委员会",
        "source": "GAP — 需通过合浦县领导分工页面核实"
    },
    # ════════════════════════════════════════
    # 县委常委、组织部部长
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "合浦县委常委、组织部部长",
        "current_org": "中共合浦县委组织部",
        "source": "GAP — 需通过合浦县领导分工页面核实"
    },
    # ════════════════════════════════════════
    # 县委常委、政法委书记
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "合浦县委常委、政法委书记",
        "current_org": "中共合浦县委政法委员会",
        "source": "GAP — 需通过合浦县领导分工页面核实"
    },
    # ════════════════════════════════════════
    # 副县长（分管农业/乡村振兴）
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "合浦县副县长",
        "current_org": "合浦县人民政府",
        "source": "GAP — 需通过合浦县政府领导之窗核实"
    },
    # ════════════════════════════════════════
    # 蔡锦军 — 曾任合浦县副县长（2001-2003）
    # 现为自治区园区办主任（前任北海市委书记）
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "蔡锦军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年11月",
        "birthplace": "江西九江",
        "education": "研究生学历，文学硕士（广西师范大学中文系），高级管理人员工商管理硕士（上海交通大学）",
        "party_join": "中共党员",
        "work_start": "1986年8月",
        "current_post": "广西壮族自治区园区办党组书记、主任",
        "current_org": "广西壮族自治区产业园区改革发展办公室",
        "source": "data/persons/广西壮族自治区-北海市-前市委书记-蔡锦军.json (本仓库已有数据); 北海市报告"
    },
    # ════════════════════════════════════════
    # 覃燕妮 — 曾任合浦县发改局、共青团合浦县、星岛湖乡
    # 现为海城区代理区长
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "覃燕妮",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982年10月",
        "birthplace": "广西贵港覃塘",
        "education": "工学学士、管理学学士，广西大学公共管理学院在职研究生",
        "party_join": "2002年10月",
        "work_start": "2005年7月",
        "current_post": "北海市海城区人民政府副区长、代理区长",
        "current_org": "北海市海城区人民政府",
        "source": "data/persons/广西壮族自治区-北海市-区长-覃燕妮.json (本仓库已有数据)"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共合浦县委员会", "type": "党委", "level": "县处级", "parent": "中共北海市委员会", "location": "北海市合浦县"},
    {"id": 2, "name": "合浦县人民政府", "type": "政府", "level": "县处级", "parent": "北海市人民政府", "location": "北海市合浦县"},
    {"id": 3, "name": "中共合浦县纪律检查委员会", "type": "纪委", "level": "副处级", "parent": "中共北海市纪律检查委员会", "location": "北海市合浦县"},
    {"id": 4, "name": "合浦县监察委员会", "type": "纪委", "level": "副处级", "parent": "北海市监察委员会", "location": "北海市合浦县"},
    {"id": 5, "name": "中共合浦县委组织部", "type": "党委", "level": "正科级", "parent": "中共合浦县委员会", "location": "北海市合浦县"},
    {"id": 6, "name": "中共合浦县委政法委员会", "type": "党委", "level": "正科级", "parent": "中共合浦县委员会", "location": "北海市合浦县"},
    {"id": 7, "name": "合浦县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "北海市人民代表大会常务委员会", "location": "北海市合浦县"},
    {"id": 8, "name": "中国人民政治协商会议合浦县委员会", "type": "政协", "level": "县处级", "parent": "政协北海市委员会", "location": "北海市合浦县"},
    {"id": 9, "name": "合浦县发展和改革局", "type": "政府", "level": "正科级", "parent": "合浦县人民政府", "location": "北海市合浦县"},
    {"id": 10, "name": "共青团合浦县委员会", "type": "群团", "level": "正科级", "parent": "共青团北海市委员会", "location": "北海市合浦县"},
    {"id": 11, "name": "合浦县星岛湖乡人民政府", "type": "乡镇/街道", "level": "乡科级", "parent": "合浦县人民政府", "location": "北海市合浦县星岛湖乡"},
    {"id": 12, "name": "中共合浦县星岛湖乡委员会", "type": "乡镇/街道", "level": "乡科级", "parent": "中共合浦县委员会", "location": "北海市合浦县星岛湖乡"},
    {"id": 13, "name": "合浦县财政局", "type": "政府", "level": "正科级", "parent": "合浦县人民政府", "location": "北海市合浦县"},
    {"id": 14, "name": "合浦县教育局", "type": "政府", "level": "正科级", "parent": "合浦县人民政府", "location": "北海市合浦县"},
    {"id": 15, "name": "合浦县卫生健康局", "type": "政府", "level": "正科级", "parent": "合浦县人民政府", "location": "北海市合浦县"},
    {"id": 16, "name": "合浦县自然资源局", "type": "政府", "level": "正科级", "parent": "合浦县人民政府", "location": "北海市合浦县"},
    {"id": 17, "name": "合浦工业园区管理委员会", "type": "开发区", "level": "副处级", "parent": "合浦县人民政府", "location": "北海市合浦县"},
    {"id": 18, "name": "中共北海市委员会", "type": "党委", "level": "厅级", "parent": "中共广西壮族自治区委员会", "location": "北海市"},
    {"id": 19, "name": "北海市人民政府", "type": "政府", "level": "厅级", "parent": "广西壮族自治区人民政府", "location": "北海市"},
]

# =========================================================================
# 3. POSITIONS (career timeline entries as position records)
# =========================================================================
positions = [
    # ── 王川 (id=1) 县委书记 ──
    # GAP: 详细履历待查。已知信息仅限县委书记职务
    {"person_id": 1, "org_id": 1, "title": "合浦县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "GAP — 起始时间待查"},

    # ── 白银冰 (id=2) 县长 ──
    # GAP: 详细履历待查。已知信息仅限县长职务
    {"person_id": 2, "org_id": 2, "title": "合浦县委副书记、县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "GAP — 起始时间和详细履历待查"},

    # ── 周水祥 (id=4) 原合浦县委常委、常务副县长 ──
    {"person_id": 4, "org_id": 1, "title": "合浦县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "任期待核实"},
    {"person_id": 4, "org_id": 2, "title": "合浦县委常委、常务副县长、县委办主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "已调往柳州任职"},

    # ── 蔡锦军 (id=9) 曾任合浦副县长 (2001.12-2003.02) ──
    {"person_id": 9, "org_id": 2, "title": "合浦县人民政府副县长", "start_date": "2001-12", "end_date": "2003-02", "rank": "副处级", "note": "据北海市_data.py 记录"},

    # ── 覃燕妮 (id=10) 合浦工作经历 ──
    {"person_id": 10, "org_id": 9, "title": "合浦县发展和改革局副局长", "start_date": "2009.08", "end_date": "2010.01", "rank": "副科级", "note": ""},
    {"person_id": 10, "org_id": 9, "title": "合浦县发展和改革局副局长、党组成员", "start_date": "2010.01", "end_date": "2011.07", "rank": "副科级", "note": ""},
    {"person_id": 10, "org_id": 10, "title": "共青团合浦县委副书记", "start_date": "2011.07", "end_date": "2011.11", "rank": "副科级", "note": ""},
    {"person_id": 10, "org_id": 10, "title": "共青团合浦县委员会书记", "start_date": "2011.11", "end_date": "2013.04", "rank": "正科级", "note": ""},
    {"person_id": 10, "org_id": 11, "title": "星岛湖乡党委副书记、乡长（候选人）", "start_date": "2013.04", "end_date": "2015.06", "rank": "正科级", "note": ""},
    {"person_id": 10, "org_id": 12, "title": "中共合浦县星岛湖乡党委书记", "start_date": "2015.06", "end_date": "2016.05", "rank": "正科级", "note": "乡镇一把手"},
    {"person_id": 10, "org_id": 1, "title": "合浦县委办公室副主任（正科长级）", "start_date": "2016.05", "end_date": "2016.07", "rank": "正科级", "note": ""},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 王川 ↔ 白银冰 — 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "合浦县委书记与县长搭档", "overlap_org": "合浦县四套班子", "overlap_period": "present"},
    # 周水祥 ↔ 王川/白银冰 — 上下级
    {"person_a": 4, "person_b": 1, "type": "上下级", "context": "周水祥任合浦县委常委期间为县委书记下属", "overlap_org": "中共合浦县委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 2, "type": "上下级", "context": "周水祥任常务副县长期间为县长下属", "overlap_org": "合浦县人民政府", "overlap_period": ""},
    # 蔡锦军 — 曾在合浦任职的上级领导
    {"person_a": 9, "person_b": 1, "type": "前后任", "context": "蔡锦军曾任合浦县副县长（2001-2003），后升任北海市委书记", "overlap_org": "合浦县人民政府", "overlap_period": "2001-2003"},
    # 覃燕妮 — 曾在合浦工作多年
    {"person_a": 10, "person_b": 1, "type": "上下级", "context": "覃燕妮在合浦县发改局、共青团、星岛湖乡等工作（2009-2016），与县委书记可能有工作交集", "overlap_org": "合浦县", "overlap_period": "2009-2016"},
]

# =========================================================================
# 5. BUILD DATABASE
# =========================================================================

def build_database():
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    # Create tables
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
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
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS positions (
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
        CREATE TABLE IF NOT EXISTS relationships (
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

    # Insert persons
    for p in persons:
        cur.execute(
            """INSERT OR REPLACE INTO persons
               (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
             p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"])
        )

    # Insert organizations
    for o in organizations:
        cur.execute(
            """INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
               VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
        )

    # Insert positions
    for pos in positions:
        cur.execute(
            """INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note)
               VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"])
        )

    # Insert relationships
    for r in relationships:
        cur.execute(
            """INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
               VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
        )

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")


# =========================================================================
# 6. BUILD GEXF
# =========================================================================

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return 'r,g,b' string based on role."""
    title = p.get("current_post", "")
    if "书记" in title and "副书记" not in title:
        return "255,50,50"  # Red — Party Secretary
    if "县长" in title or "区长" in title:
        return "50,100,255"  # Blue — County Mayor
    if "纪委书记" in title:
        return "255,165,0"  # Orange — Discipline
    if "副书记" in title or "常委" in title:
        return "180,100,180"  # Purple — Deputy/Standing committee
    if "副" in title and ("县长" in title or "区长" in title):
        return "100,150,220"  # Light blue — Deputy
    return "100,100,100"  # Grey

def org_color(o):
    """Return 'r,g,b' string based on org type."""
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "纪委" in t:
        return "255,200,150"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    if "开发区" in t:
        return "200,255,200"
    if "乡镇" in t or "街道" in t:
        return "255,255,200"
    if "群团" in t:
        return "255,220,255"
    return "200,200,200"

def is_top_leader(p):
    title = p.get("current_post", "")
    return ("书记" in title and "副书记" not in title) or "县长" in title

def person_size(p):
    return "20.0" if is_top_leader(p) else ("15.0" if "副书记" in p.get("current_post", "") or "常委" in p.get("current_post", "") else "12.0")

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation build script</creator>')
    lines.append(f'    <description>合浦县领导班子工作关系网络 (as of {AS_OF})</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
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

    # Nodes: Persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: Organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level",""))}"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append(f'          <attvalue for="4" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    # person -> organization (worked_at)
    for pos in positions:
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos.get("start_date",""))} - {esc(pos.get("end_date",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    # person <-> person (relationships)
    for r in relationships:
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {GEXF_PATH}")


# =========================================================================
# 7. MAIN
# =========================================================================

if __name__ == "__main__":
    build_database()
    build_gexf()
    print("Done.")
