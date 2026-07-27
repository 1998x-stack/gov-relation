#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从江县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 贵州省
Parent City: 黔东南苗族侗族自治州
Region: 从江县
Task: guizhou_从江县
Targets: 县委书记 & 县长

当前在任 (as of 2026-07-23):
- 县委书记: 侯美彪 (confirmed from congjiang.gov.cn news articles 2026年7月)
- 县委副书记、县长: 龙稳全 (1981年6月生，苗族，博士研究生)
- 县政府领导: 李小锋、刘芳、谢卫忠、曲为君、潘勇、乐小虎、周海林、崔伟
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
BASE = os.path.dirname(os.path.abspath(__file__))
TASK_ID = "guizhou_从江县"
SLUG = "从江县"
AS_OF = "2026-07-23"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = BASE

# =========================================================================
# 1. SOURCE REGISTER
# =========================================================================
source_register = [
    {"id": "S001", "title": "从江县人民政府门户网站——领导之窗",
     "url": "https://www.congjiang.gov.cn/zwgk/ldzc/",
     "publisher": "从江县人民政府", "published_at": "2026-07-23", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "列出县政府领导班子——龙稳全（县长）及8位副县长"},
    {"id": "S002", "title": "从江县人民政府门户网站——首页新闻（侯美彪调研报道）",
     "url": "https://www.congjiang.gov.cn/",
     "publisher": "从江县人民政府", "published_at": "2026-07-22", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "确认侯美彪为从江县委书记（侯美彪调研防洪堤建设、防溺水安全等工作）"},
    {"id": "S003", "title": "从江县人民政府门户网站——侯美彪主持召开专题会议研究部署生态环保领域问题",
     "url": "https://www.congjiang.gov.cn/",
     "publisher": "从江县人民政府", "published_at": "2026-07", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "确认侯美彪为从江县委书记"},
    {"id": "S004", "title": "从江县人民政府门户网站——龙稳全到贯洞镇调研督导工作",
     "url": "https://www.congjiang.gov.cn/",
     "publisher": "从江县人民政府", "published_at": "2026-07-16", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "确认龙稳全以县委副书记、县长身份开展工作"},
    {"id": "S005", "title": "从江县人民政府门户网站——县委常委会第215次会议",
     "url": "https://www.congjiang.gov.cn/",
     "publisher": "从江县人民政府", "published_at": "2026-07-22", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "确认县委常委会运作，侯美彪主持"},
    {"id": "S006", "title": "从江县人民政府门户网站——县委常委同志一周动态（2026年7月13日—7月17日）",
     "url": "https://www.congjiang.gov.cn/",
     "publisher": "从江县人民政府", "published_at": "2026-07-23", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "确认县委常委领导班子在任"},
    {"id": "S007", "title": "从江县人民政府门户网站——从江县第十八届人大常委会第四十六次会议",
     "url": "https://www.congjiang.gov.cn/",
     "publisher": "从江县人民政府", "published_at": "2026-07", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "确认县人大常委会运作"},
    {"id": "S008", "title": "从江县人民政府门户网站——县委理论学习中心组2026年第6次集中研讨会",
     "url": "https://www.congjiang.gov.cn/",
     "publisher": "从江县人民政府", "published_at": "2026-07", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "确认县委领导班子集体学习"},
    {"id": "S009", "title": "从江县人民政府门户网站——从江县国民经济和社会发展第十五个五年规划纲要",
     "url": "https://www.congjiang.gov.cn/",
     "publisher": "从江县人民政府", "published_at": "2026-05-07", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "县政府发布十五五规划纲要"},
]

# =========================================================================
# 2. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：县委书记
    # ════════════════════════════════════════
    {"id": 1, "name": "侯美彪", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共从江县委书记", "current_org": "中共从江县委员会",
     "source": "S002"},

    # ════════════════════════════════════════
    # 核心领导：县长
    # ════════════════════════════════════════
    {"id": 2, "name": "龙稳全", "gender": "男", "ethnicity": "苗族",
     "birth": "1981-06", "birthplace": "", "education": "博士研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "从江县委副书记、县长", "current_org": "从江县人民政府",
     "source": "S001"},

    # ════════════════════════════════════════
    # 县政府副县长（从领导之窗页面确认）
    # ════════════════════════════════════════
    {"id": 3, "name": "李小锋", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "从江县人民政府副县长", "current_org": "从江县人民政府",
     "source": "S001"},

    {"id": 4, "name": "刘芳", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "从江县人民政府副县长", "current_org": "从江县人民政府",
     "source": "S001"},

    {"id": 5, "name": "谢卫忠", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "从江县人民政府副县长", "current_org": "从江县人民政府",
     "source": "S001"},

    {"id": 6, "name": "曲为君", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "从江县人民政府副县长", "current_org": "从江县人民政府",
     "source": "S001"},

    {"id": 7, "name": "潘勇", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "从江县人民政府副县长", "current_org": "从江县人民政府",
     "source": "S001"},

    {"id": 8, "name": "乐小虎", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "从江县人民政府副县长", "current_org": "从江县人民政府",
     "source": "S001"},

    {"id": 9, "name": "周海林", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "从江县人民政府副县长", "current_org": "从江县人民政府",
     "source": "S001"},

    {"id": 10, "name": "崔伟", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "从江县人民政府副县长", "current_org": "从江县人民政府",
     "source": "S001"},
]

# =========================================================================
# 3. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共从江县委员会", "type": "党委", "level": "县处级",
     "parent": "中共黔东南苗族侗族自治州委员会", "location": "贵州省黔东南州从江县"},
    {"id": 2, "name": "从江县人民政府", "type": "政府", "level": "县处级",
     "parent": "黔东南苗族侗族自治州人民政府", "location": "贵州省黔东南州从江县"},
    {"id": 3, "name": "从江县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "黔东南苗族侗族自治州人民代表大会常务委员会", "location": "贵州省黔东南州从江县"},
    {"id": 4, "name": "中国人民政治协商会议从江县委员会", "type": "政协", "level": "县处级",
     "parent": "", "location": "贵州省黔东南州从江县"},
    {"id": 5, "name": "中共从江县纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共黔东南苗族侗族自治州纪律检查委员会", "location": "贵州省黔东南州从江县"},
]

# =========================================================================
# 4. POSITIONS
# =========================================================================
positions = [
    # ── 侯美彪 ──
    {"person_id": 1, "org_id": 1, "title": "中共从江县委书记",
     "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任，2026年7月确认"},

    # ── 龙稳全 ──
    {"person_id": 2, "org_id": 1, "title": "从江县委副书记",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 2, "org_id": 2, "title": "从江县人民政府县长",
     "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},

    # ── 李小锋 ──
    {"person_id": 3, "org_id": 2, "title": "从江县人民政府副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},

    # ── 刘芳 ──
    {"person_id": 4, "org_id": 2, "title": "从江县人民政府副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},

    # ── 谢卫忠 ──
    {"person_id": 5, "org_id": 2, "title": "从江县人民政府副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},

    # ── 曲为君 ──
    {"person_id": 6, "org_id": 2, "title": "从江县人民政府副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},

    # ── 潘勇 ──
    {"person_id": 7, "org_id": 2, "title": "从江县人民政府副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},

    # ── 乐小虎 ──
    {"person_id": 8, "org_id": 2, "title": "从江县人民政府副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},

    # ── 周海林 ──
    {"person_id": 9, "org_id": 2, "title": "从江县人民政府副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},

    # ── 崔伟 ──
    {"person_id": 10, "org_id": 2, "title": "从江县人民政府副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
]

# =========================================================================
# 5. RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 党政主要领导 ──
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "侯美彪（县委书记）与龙稳全（县委副书记、县长）构成书记-县长搭档",
     "overlap_org": "中共从江县委员会/从江县人民政府", "overlap_period": ""},

    # ── 县长与副县长班子 ──
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "龙稳全（县长）与李小锋（副县长）在县政府班子共事",
     "overlap_org": "从江县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "龙稳全（县长）与刘芳（副县长）在县政府班子共事",
     "overlap_org": "从江县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "overlap",
     "context": "龙稳全（县长）与谢卫忠（副县长）在县政府班子共事",
     "overlap_org": "从江县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "overlap",
     "context": "龙稳全（县长）与曲为君（副县长）在县政府班子共事",
     "overlap_org": "从江县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "overlap",
     "context": "龙稳全（县长）与潘勇（副县长）在县政府班子共事",
     "overlap_org": "从江县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "overlap",
     "context": "龙稳全（县长）与乐小虎（副县长）在县政府班子共事",
     "overlap_org": "从江县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "overlap",
     "context": "龙稳全（县长）与周海林（副县长）在县政府班子共事",
     "overlap_org": "从江县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "overlap",
     "context": "龙稳全（县长）与崔伟（副县长）在县政府班子共事",
     "overlap_org": "从江县人民政府", "overlap_period": ""},

    # ── 副县长之间 ──
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "李小锋与刘芳在县政府班子共事",
     "overlap_org": "从江县人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 5, "type": "overlap",
     "context": "李小锋与谢卫忠在县政府班子共事",
     "overlap_org": "从江县人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 5, "type": "overlap",
     "context": "刘芳与谢卫忠在县政府班子共事",
     "overlap_org": "从江县人民政府", "overlap_period": ""},
    {"person_a": 5, "person_b": 6, "type": "overlap",
     "context": "谢卫忠与曲为君在县政府班子共事",
     "overlap_org": "从江县人民政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 7, "type": "overlap",
     "context": "曲为君与潘勇在县政府班子共事",
     "overlap_org": "从江县人民政府", "overlap_period": ""},
    {"person_a": 7, "person_b": 8, "type": "overlap",
     "context": "潘勇与乐小虎在县政府班子共事",
     "overlap_org": "从江县人民政府", "overlap_period": ""},
    {"person_a": 8, "person_b": 9, "type": "overlap",
     "context": "乐小虎与周海林在县政府班子共事",
     "overlap_org": "从江县人民政府", "overlap_period": ""},
    {"person_a": 9, "person_b": 10, "type": "overlap",
     "context": "周海林与崔伟在县政府班子共事",
     "overlap_org": "从江县人民政府", "overlap_period": ""},
]

# =========================================================================
# BUILD FUNCTIONS
# =========================================================================


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build():
    os.makedirs(BASE, exist_ok=True)

    # ── SQLite ──
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pid TEXT UNIQUE NOT NULL,
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
            person_id TEXT NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(pid),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(pid),
            FOREIGN KEY (person_b) REFERENCES persons(pid)
        );
    """)

    person_map = {}
    for idx, p in enumerate(persons, 1):
        pid = f"congjiang_{p['name']}"
        person_map[p["id"]] = pid
        cur.execute("""INSERT INTO persons (id,pid,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) 
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (idx, pid, p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (person_map[pos["person_id"]], pos["org_id"], pos["title"], pos.get("start_date", ""),
                     pos.get("end_date", ""), pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (person_map[r["person_a"]], person_map[r["person_b"]], r["type"], r["context"],
                     r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ──
    def person_color(post):
        if "书记" in post and "副" not in post and "纪委" not in post:
            return "255,50,50"
        if "县长" in post and "副" not in post and "人大" not in post and "政协" not in post:
            return "50,100,255"
        if "纪委书记" in post:
            return "255,165,0"
        if "副" in post or "副书记" in post:
            return "100,150,220"
        if "主任" in post and "副" not in post:
            return "60,180,60"
        if "政协" in post:
            return "180,160,80"
        return "100,100,100"

    def is_top_leader(post):
        return ("书记" in post and "副" not in post and "纪委" not in post) or \
               ("县长" in post and "副" not in post and "人大" not in post and "政协" not in post)

    def person_shape(post):
        if "书记" in post and "副" not in post and "纪委" not in post:
            return "square"
        if "县长" in post and "副" not in post and "人大" not in post and "政协" not in post:
            return "circle"
        if "纪委书记" in post or "纪委" in post:
            return "diamond"
        return "triangle"

    def org_color(otype):
        colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "人大": "200,255,255",
            "政协": "255,240,200",
            "纪委": "255,200,150",
        }
        return colors.get(otype, "200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>从江县领导班子关系网络（基于从江县人民政府门户网站）</description>')
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

    # Nodes — persons
    lines.append('    <nodes>')
    for p in persons:
        pid_num = p["id"]
        post = p.get("current_post", "")
        c = person_color(post)
        sz = "20.0" if is_top_leader(post) else "12.0"
        shape = person_shape(post)

        lines.append(f'      <node id="p{pid_num}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    # Nodes — organizations
    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o["type"])

        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append(f'        <viz:shape value="hexagon"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization
    for pos in positions:
        if pos["org_id"] == 99:
            continue
        eid += 1
        pid_num = pos["person_id"]
        oid = pos["org_id"] + 100000
        lines.append(
            f'      <edge id="e{eid}" source="p{pid_num}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ person
    for r in relationships:
        eid += 1
        lines.append(
            f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")

    # ── Person Graph JSONs ──
    now = AS_OF.replace("-", "")

    def make_person_json(p, timeline, relationships_list, custom_identity=None):
        """Generate a person graph JSON following the person_graph_json.md schema."""
        result = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "贵州省",
                "city": "黔东南苗族侗族自治州",
                "region": "从江县",
                "job": p.get("current_post", ""),
                "task_id": TASK_ID,
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"congjiang_{p['name']}",
                "name": p["name"],
                "aliases": [],
                "gender": p.get("gender", ""),
                "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""),
                "birthplace": p.get("birthplace", ""),
                "native_place": "",
                "education": [
                    {
                        "period": "",
                        "institution": "",
                        "major": "",
                        "degree": p.get("education", ""),
                        "study_type": "unknown",
                        "source_ids": []
                    }
                ] if p.get("education") else [],
                "party_join": p.get("party_join", ""),
                "work_start": p.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{p['name']}_{p.get('birth', '')}",
                    "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": p.get("current_post", ""),
                "current_org": p.get("current_org", ""),
                "administrative_rank": "县处级正职" if ("书记" in p.get("current_post", "") and "副" not in p.get("current_post", "") and "纪委" not in p.get("current_post", "")) or ("县长" in p.get("current_post", "") and "副" not in p.get("current_post", "") and "人大" not in p.get("current_post", "") and "政协" not in p.get("current_post", "")) else "县处级副职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002"] if p["id"] <= 2 else ["S001"]
            },
            "career_timeline": timeline,
            "organizations": [],
            "relationships": relationships_list,
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
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "在公开信息中未发现该人物负面信号",
                 "date": "", "confidence": "confirmed", "source_ids": []}
            ],
            "source_register": source_register,
            "confidence_summary": {
                "identity": "unverified" if not p.get("birth") else "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": ""
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{p['name']}的完整职业生涯履历",
                 "why_it_matters": "无法追溯其任职路径和系统经历",
                 "suggested_queries": [f"{p['name']} 简历 从江"],
                 "last_attempted": AS_OF},
            ]
        }
        if custom_identity:
            result["identity"].update(custom_identity)
        return result

    # ── 侯美彪 Person JSON ──
    hmb_timeline = [
        {"start": "", "end": "", "org": "中共从江县委员会", "title": "中共从江县委书记",
         "notes": "现任，2026年7月从江县人民政府网站确认在任", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "侯美彪任职从江县委书记之前的履历未找到（出生年月、籍贯、教育背景、晋升路径等信息缺失）",
         "confidence": "unverified", "source_ids": []},
    ]
    hmb_relationships = [
        {"person": "龙稳全", "person_id": "congjiang_龙稳全", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "侯美彪（县委书记）与龙稳全（县委副书记、县长）构成书记-县长搭档",
         "overlap_org": "中共从江县委员会/从江县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    ]

    hmb_json = make_person_json(persons[0], hmb_timeline, hmb_relationships)
    hmb_path = os.path.join(PERSONS_DIR, f"{now}-贵州省-黔东南苗族侗族自治州-县委书记-侯美彪.json")
    with open(hmb_path, "w", encoding="utf-8") as f:
        json.dump(hmb_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {hmb_path}")

    # ── 龙稳全 Person JSON ──
    lwq_timeline = [
        {"start": "", "end": "", "org": "从江县人民政府", "title": "从江县委副书记、县长",
         "notes": "现任，博士研究生学历，苗族，1981年6月出生", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "龙稳全任从江县长前的完整履历未找到（博士研究生毕业院校、早期任职经历等信息缺失）",
         "confidence": "unverified", "source_ids": []},
    ]
    lwq_relationships = [
        {"person": "侯美彪", "person_id": "congjiang_侯美彪", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "龙稳全（县长）与侯美彪（县委书记）构成书记-县长搭档",
         "overlap_org": "中共从江县委员会/从江县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"person": "李小锋", "person_id": "congjiang_李小锋", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "龙稳全（县长）与李小锋（副县长）在县政府班子共事",
         "overlap_org": "从江县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "刘芳", "person_id": "congjiang_刘芳", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "龙稳全（县长）与刘芳（副县长）在县政府班子共事",
         "overlap_org": "从江县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "谢卫忠", "person_id": "congjiang_谢卫忠", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "龙稳全（县长）与谢卫忠（副县长）在县政府班子共事",
         "overlap_org": "从江县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]

    lwq_json = make_person_json(persons[1], lwq_timeline, lwq_relationships)
    lwq_path = os.path.join(PERSONS_DIR, f"{now}-贵州省-黔东南苗族侗族自治州-县长-龙稳全.json")
    with open(lwq_path, "w", encoding="utf-8") as f:
        json.dump(lwq_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lwq_path}")

    print("\nDone. All artifacts generated in staging directory.")


if __name__ == "__main__":
    build()
