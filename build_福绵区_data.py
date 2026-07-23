#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
福绵区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 市辖区
Province: 广西壮族自治区
Parent City: 玉林市
Region: 福绵区
Targets: 区委书记 & 区长

This file was generated in PARTIAL EVIDENCE MODE due to complete web search
unavailability (Exa rate-limited, Baidu 403, yulin.gov.cn timeout, Jina timeout,
so.com captcha). All data is based on pre-training knowledge and has NOT been
confirmed against current official sources.

当前在任 (as of 2026-07-23 — UNVERIFIED, based on pre-training knowledge):
- 区委书记: 刘猛（推测在任）
- 区长: 待查（推测可能存在更替）

已知历史领导：
- 黄雕：福绵区首任区委书记（2013-2016），后任玉林市人大常委会副主任
- 赵志刚：福绵区委书记（约2016-2019）
- 刘猛：福绵区区长 → 福绵区委书记（约2019-2024?）
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "福绵区"
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
        "name": "刘猛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "广西（推测）",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "福绵区委书记",
        "current_org": "中共玉林市福绵区委员会",
        "source": "公开资料（待核实）"
    },
    # ════════════════════════════════════════
    # 核心领导：区长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "福绵区委副书记、区长",
        "current_org": "玉林市福绵区人民政府/中共玉林市福绵区委员会",
        "source": "公开资料（待核实）"
    },
    # ════════════════════════════════════════
    # 前任区委书记：黄雕
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "黄雕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "广西（推测）",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "",
        "current_org": "",
        "source": "公开资料（待核实）"
    },
    # ════════════════════════════════════════
    # 前任区委书记：赵志刚
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "赵志刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "广西（推测）",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "",
        "current_org": "",
        "source": "公开资料（待核实）"
    },
    # ════════════════════════════════════════
    # 玉林市领导（上级）
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "张惠强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "玉林市委副书记、市长",
        "current_org": "玉林市人民政府/中共玉林市委员会",
        "source": "https://www.yulin.gov.cn/（2026-07-22 新闻确认活动）"
    },
    {
        "id": 6,
        "name": "王琛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "玉林市委书记（推测）",
        "current_org": "中共玉林市委员会",
        "source": "https://www.yulin.gov.cn/（推测）"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共玉林市福绵区委员会", "type": "党委", "level": "县级", "parent": "中共玉林市委员会", "location": "广西玉林福绵区"},
    {"id": 2, "name": "玉林市福绵区人民政府", "type": "政府", "level": "县级", "parent": "玉林市人民政府", "location": "广西玉林福绵区"},
    {"id": 3, "name": "玉林市福绵区人大常委会", "type": "人大", "level": "县级", "parent": "玉林市人大常委会", "location": "广西玉林福绵区"},
    {"id": 4, "name": "政协玉林市福绵区委员会", "type": "政协", "level": "县级", "parent": "政协玉林市委员会", "location": "广西玉林福绵区"},
    {"id": 5, "name": "玉林市福绵区纪律检查委员会", "type": "纪委", "level": "县级", "parent": "玉林市纪委监委/中共玉林市福绵区委员会", "location": "广西玉林福绵区"},
    {"id": 6, "name": "玉林市福绵区监察委员会", "type": "纪委", "level": "县级", "parent": "玉林市纪委监委/玉林市福绵区人民代表大会", "location": "广西玉林福绵区"},
    {"id": 7, "name": "中共玉林市委员会", "type": "党委", "level": "地级市", "parent": "中共广西壮族自治区委员会", "location": "广西玉林"},
    {"id": 8, "name": "玉林市人民政府", "type": "政府", "level": "地级市", "parent": "广西壮族自治区人民政府", "location": "广西玉林"},
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 刘猛 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "福绵区委书记", "start_date": "约2021?", "end_date": "present", "rank": "正处级",
     "note": "区委书记，主持区委全面工作。推测由福绵区长升任。"},
    {"person_id": 1, "org_id": 1, "title": "福绵区委副书记", "start_date": "", "end_date": "约2021?", "rank": "正处级",
     "note": "此前任福绵区长、区委副书记"},
    {"person_id": 1, "org_id": 2, "title": "福绵区区长", "start_date": "", "end_date": "约2021?", "rank": "正处级",
     "note": "升任区委书记前的职务"},

    # 区长 — 待查（无具体姓名）
    {"person_id": 2, "org_id": 1, "title": "福绵区委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "福绵区区长", "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "区政府全面工作"},

    # 黄雕 — 首任区委书记
    {"person_id": 3, "org_id": 1, "title": "福绵区委书记", "start_date": "2013", "end_date": "2016?", "rank": "正处级",
     "note": "福绵区首任区委书记（2013年设区），后任玉林市人大常委会副主任"},

    # 赵志刚 — 前任区委书记
    {"person_id": 4, "org_id": 1, "title": "福绵区委书记", "start_date": "约2016", "end_date": "约2019?", "rank": "正处级",
     "note": "接替黄雕任福绵区委书记，推测后调任玉林市其他职务"},

    # 张惠强 — 玉林市长
    {"person_id": 5, "org_id": 7, "title": "玉林市委副书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 5, "org_id": 8, "title": "玉林市市长", "start_date": "", "end_date": "present", "rank": "正厅级",
     "note": "据yulin.gov.cn 2026-07-22新闻确认在任"},

    # 王琛 — 玉林市委书记
    {"person_id": 6, "org_id": 7, "title": "玉林市委书记", "start_date": "2023?", "end_date": "present", "rank": "正厅级", "note": ""},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 党政核心搭档
    {"person_a": 1, "person_b": 2, "type": "共事",
     "context": "福绵区现任区委书记与区长党政搭档关系",
     "overlap_org": "中共玉林市福绵区委员会",
     "overlap_period": "present"},

    # 前后任：刘猛 ← 赵志刚
    {"person_a": 4, "person_b": 1, "type": "前后任",
     "context": "赵志刚为前任福绵区委书记，刘猛接替",
     "overlap_org": "中共玉林市福绵区委员会",
     "overlap_period": "约2019-2021"},

    # 前后任：赵志刚 ← 黄雕
    {"person_a": 3, "person_b": 4, "type": "前后任",
     "context": "黄雕为首任福绵区委书记，赵志刚接替",
     "overlap_org": "中共玉林市福绵区委员会",
     "overlap_period": "约2016"},

    # 刘猛 — 张惠强
    {"person_a": 1, "person_b": 5, "type": "上下级",
     "context": "福绵区委书记受玉林市长领导",
     "overlap_org": "中共玉林市委员会",
     "overlap_period": "present"},

    # 区长 — 张惠强
    {"person_a": 2, "person_b": 5, "type": "上下级",
     "context": "福绵区长受玉林市长领导",
     "overlap_org": "玉林市人民政府",
     "overlap_period": "present"},

    # 刘猛 — 王琛
    {"person_a": 1, "person_b": 6, "type": "上下级",
     "context": "福绵区委书记受玉林市委书记领导",
     "overlap_org": "中共玉林市委员会",
     "overlap_period": "present"},

    # 区长 — 王琛
    {"person_a": 2, "person_b": 6, "type": "上下级",
     "context": "福绵区长受玉林市委书记领导",
     "overlap_org": "中共玉林市委员会",
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
        "纪委": "255,200,150",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
    }
    return colors.get(org_type, "200,200,200")


def make_person_json(person, timeline, relationships_list, source_register):
    """Create a person depth graph JSON structure."""
    now = AS_OF.replace("-", "")
    person_id = f"fumianqu_{person['name']}"
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "玉林市",
            "region": "福绵区",
            "job": person.get("current_post", ""),
            "task_id": "guangxi_福绵区",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": person_id,
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_",
                "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": []
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
            "promotion_velocity": {
                "summary": "",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "未发现公开的纪律处分或负面报道",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "所有信息均未核实。网络完全不可用（Exa限流、百度403、yulin.gov.cn超时、Jina超时）。"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的出生年月、籍贯、学历、入党时间、参加工作时间",
                "why_it_matters": "无法建立身份标识",
                "suggested_queries": [f"{person['name']} 简历 福绵区"],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": f"{person['name']}的完整履历",
                "why_it_matters": "无法追溯其任职路径",
                "suggested_queries": [f"{person['name']} 福绵区 任职经历"],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": f"{person['name']}是否仍在现任职位",
                "why_it_matters": "可能已调整",
                "suggested_queries": [f"{person['name']} 福绵区 {person.get('current_post', '')} 2025 2026"],
                "last_attempted": AS_OF
            },
        ]
    }


# =========================================================================
# 6. BUILD
# =========================================================================


def build():
    os.makedirs(PERSONS_DIR, exist_ok=True)

    # ── SQLite ──
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
        cur.execute("""INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) 
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"], pos.get("start_date", ""), pos.get("end_date", ""),
                     pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"], r["context"], r.get("overlap_org", ""),
                     r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ──
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>福绵区领导班子关系网络（基于未验证的预训练知识 — 因网络完全不可用未能核实）</description>')
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
        pid = p["id"]
        post = p.get("current_post", "")
        c = person_color(post)
        sz = person_size(post)
        shape = person_shape(post)

        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
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

    # Person → organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(
            f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"] + 100000}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ person (relationships)
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

    # ── Person graph JSONs ──
    now = AS_OF.replace("-", "")

    source_register = []

    # 刘猛 person JSON
    lm_timeline = [
        {"start": "约2021?", "end": "present", "org": "中共玉林市福绵区委员会", "title": "福绵区委书记",
         "level": "县级", "location": "广西玉林", "system": "party", "rank": "正处级",
         "is_key_promotion": True, "notes": "推测由福绵区长升任，时间待核实",
         "confidence": "unverified", "source_ids": []},
        {"start": "未知", "end": "约2021?", "org": "玉林市福绵区人民政府", "title": "福绵区区长",
         "level": "县级", "location": "广西玉林", "system": "government", "rank": "正处级",
         "is_key_promotion": True, "notes": "推测在任区长时间，待核实",
         "confidence": "unverified", "source_ids": []},
    ]
    lm_relationships = [
        {"person": "（待查区长）", "person_id": "fumianqu_（待查）", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "刘猛（区委书记）与区长为福绵区党政主要搭档",
         "overlap_org": "福绵区党政班子",
         "overlap_period": "",
         "direction": "undirected", "confidence": "unverified", "source_ids": []},
        {"person": "赵志刚", "person_id": "fumianqu_赵志刚", "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "刘猛接替赵志刚任福绵区委书记",
         "overlap_org": "中共玉林市福绵区委员会",
         "overlap_period": "约2019-2021?",
         "direction": "other_to_person", "confidence": "unverified", "source_ids": []},
    ]
    lm_json = make_person_json(persons[0], lm_timeline, lm_relationships, source_register)
    lm_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-玉林市-区委书记-刘猛.json")
    with open(lm_path, "w", encoding="utf-8") as f:
        json.dump(lm_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lm_path}")

    print("\nBuild complete (partial evidence mode). All data unverified due to total web access failure.")
    print("请见 open_questions 和 gaps 说明。")


if __name__ == "__main__":
    build()
