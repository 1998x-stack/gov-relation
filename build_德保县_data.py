#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
德保县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 广西壮族自治区
Parent City: 百色市
Region: 德保县
Targets: 县委书记 & 县长

当前在任 (as of 2026-07-23):
- 县委书记: 陆兰碧 (百色市人大常委会副主任兼德保县委书记)
- 县长: [待查 — 公开资料未找到现任县长姓名]
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

# ── Paths ──
BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "德保县"
DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = BASE

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
        "name": "陆兰碧",
        "gender": "女",
        "ethnicity": "壮族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "百色市人大常委会副主任（兼德保县委书记）",
        "current_org": "中共德保县委员会/百色市人民代表大会常务委员会",
        "source": "https://www.gxbsrd.gov.cn/html/news-view-78719.html"
    },
    # ════════════════════════════════════════
    # 核心领导：县长 — 待查
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "待查（县长）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "德保县委副书记、县长",
        "current_org": "德保县人民政府",
        "source": "待查"
    },
    # ════════════════════════════════════════
    # 县政协主席（基于百色市已知信息推断）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "待查（县政协主席）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "德保县政协主席",
        "current_org": "中国人民政治协商会议德保县委员会",
        "source": "待查"
    },
    # ════════════════════════════════════════
    # 县人大常委会主任
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "待查（县人大常委会主任）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "德保县人大常委会主任",
        "current_org": "德保县人民代表大会常务委员会",
        "source": "待查"
    },
    # ════════════════════════════════════════
    # 前德保县委书记（陆兰碧前任）
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "待查（前县委书记）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已调离",
        "current_org": "",
        "source": "待查"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共德保县委员会", "type": "党委", "level": "县处级", "parent": "中共百色市委员会", "location": "广西百色市德保县"},
    {"id": 2, "name": "德保县人民政府", "type": "政府", "level": "县处级", "parent": "百色市人民政府", "location": "广西百色市德保县"},
    {"id": 3, "name": "德保县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "百色市人大常委会", "location": "广西百色市德保县"},
    {"id": 4, "name": "中国人民政治协商会议德保县委员会", "type": "政协", "level": "县处级", "parent": "百色市政协", "location": "广西百色市德保县"},
    {"id": 5, "name": "百色市人民代表大会常务委员会", "type": "人大", "level": "地厅级", "parent": "广西壮族自治区人大常委会", "location": "广西百色市"},
    {"id": 6, "name": "中共百色市委员会", "type": "党委", "level": "地厅级", "parent": "", "location": "广西百色市"},
    {"id": 7, "name": "百色市人民政府", "type": "政府", "level": "地厅级", "parent": "", "location": "广西百色市"},
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 陆兰碧 - 德保县委书记
    {"person_id": 1, "org_id": 1, "title": "德保县委书记", "start": "待查", "end": "present", "rank": "县处级", "note": "陆兰碧同时任百色市人大常委会副主任（副厅级），属高配"},
    {"person_id": 1, "org_id": 5, "title": "百色市人大常委会副主任", "start": "待查", "end": "present", "rank": "副厅级", "note": "兼德保县委书记"},
    # 县长（待查）
    {"person_id": 2, "org_id": 2, "title": "德保县委副书记、县长", "start": "待查", "end": "present", "rank": "县处级", "note": "待查"},
    {"person_id": 2, "org_id": 1, "title": "德保县委副书记", "start": "待查", "end": "present", "rank": "县处级", "note": ""},
    # 县政协主席（待查）
    {"person_id": 3, "org_id": 4, "title": "德保县政协主席", "start": "待查", "end": "present", "rank": "县处级", "note": ""},
    # 县人大常委会主任（待查）
    {"person_id": 4, "org_id": 3, "title": "德保县人大常委会主任", "start": "待查", "end": "present", "rank": "县处级", "note": ""},
    # 前县委书记（待查）
    {"person_id": 5, "org_id": 1, "title": "德保县委书记（前任）", "start": "待查", "end": "待查", "rank": "县处级", "note": "陆兰碧的前任"},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 党政主要领导
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "陆兰碧（县委书记）与县长为德保县党政主要搭档",
     "overlap_org": "德保县党政班子", "overlap_period": ""},
    # 县委书记与人大主任
    {"person_a": 1, "person_b": 4, "type": "上下级",
     "context": "陆兰碧（县委书记）与县人大常委会主任为县委和人大领导关系",
     "overlap_org": "德保县四家班子", "overlap_period": ""},
    # 县委书记与政协主席
    {"person_a": 1, "person_b": 3, "type": "上下级",
     "context": "陆兰碧（县委书记）与县政协主席为县委和政协领导关系",
     "overlap_org": "德保县四家班子", "overlap_period": ""},
    # 上级关系：百色市委 → 德保县委
    {"person_a": 1, "person_b": 1, "type": "上下级",
     "context": "陆兰碧（德保县委书记）受百色市委领导（因同时任市人大常委会副主任，行政上属百色市副厅级领导）",
     "overlap_org": "中共百色市委员会/百色市人大常委会", "overlap_period": ""},
]

# =========================================================================
# 5. HELPERS
# =========================================================================

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return GEXF color for a person node based on role."""
    role_lower = p.get("current_post", "").lower()
    if "县委书记" in role_lower or "书记" in role_lower:
        return "255,50,50"
    elif "县长" in role_lower or "市长" in role_lower or "区长" in role_lower:
        return "50,100,255"
    elif "纪委书记" in role_lower or "监委" in role_lower:
        return "255,165,0"
    else:
        return "100,100,100"

def org_color(o):
    """Return GEXF color for an org node."""
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    elif "政府" in t:
        return "200,200,255"
    elif "人大" in t:
        return "200,255,255"
    elif "政协" in t:
        return "255,240,200"
    elif "开发区" in t:
        return "200,255,200"
    elif "乡镇" in t or "街道" in t:
        return "255,255,200"
    elif "事业单位" in t:
        return "220,220,220"
    elif "群团" in t:
        return "255,220,255"
    else:
        return "200,200,200"

def is_top_leader(p):
    """Check if a person is a top leader (县委书记/县长)."""
    post = p.get("current_post", "")
    return "书记" in post and "副书记" not in post and "县委" in post

# =========================================================================
# 6. BUILD SQLite DB
# =========================================================================

print(f"Building database: {DB_PATH}")
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Create tables
cur.executescript("""
DROP TABLE IF EXISTS persons;
DROP TABLE IF EXISTS organizations;
DROP TABLE IF EXISTS positions;
DROP TABLE IF EXISTS relationships;

CREATE TABLE persons (
    id INTEGER PRIMARY KEY,
    name TEXT,
    gender TEXT,
    ethnicity TEXT,
    birth TEXT,
    birthplace TEXT,
    education TEXT,
    party_join TEXT,
    work_start TEXT,
    current_post TEXT,
    current_org TEXT,
    source TEXT
);

CREATE TABLE organizations (
    id INTEGER PRIMARY KEY,
    name TEXT,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

CREATE TABLE positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER,
    org_id INTEGER,
    title TEXT,
    start TEXT,
    "end" TEXT,
    rank TEXT,
    note TEXT
);

CREATE TABLE relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER,
    person_b INTEGER,
    type TEXT,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT
);
""")

# Insert persons
for p in persons:
    cur.execute(
        "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"])
    )

# Insert organizations
for o in organizations:
    cur.execute(
        "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
        (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
    )

# Insert positions
for pos in positions:
    cur.execute(
        "INSERT INTO positions (person_id, org_id, title, start, \"end\", rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"])
    )

# Insert relationships
for r in relationships:
    cur.execute(
        "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?, ?, ?, ?, ?, ?)",
        (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
    )

conn.commit()
conn.close()
print(f"Database ready: {DB_PATH}")

# =========================================================================
# 7. BUILD GEXF
# =========================================================================

print(f"Building GEXF: {GEXF_PATH}")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
lines.append('    <creator>China Gov Network Research Agent</creator>')
lines.append('    <description>德保县领导班子工作关系网络 - 广西百色市德保县</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="org" type="string"/>')
lines.append('      <attribute id="3" title="level" type="string"/>')
lines.append('    </attributes>')

# Edge attributes
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('    </attributes>')

# Person nodes
lines.append('    <nodes>')
for p in persons:
    p_id = p["id"]
    name = p["name"]
    c = person_color(p)
    sz = "20.0" if is_top_leader(p) else "12.0"
    lines.append(f'      <node id="p{p_id}" label="{esc(name)}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
    lines.append('          <attvalue for="3" value=""/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Organization nodes
for o in organizations:
    o_id = o["id"]
    name = o["name"]
    c = org_color(o)
    lines.append(f'      <node id="o{o_id}" label="{esc(name)}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
    lines.append(f'          <attvalue for="2" value=""/>')
    lines.append(f'          <attvalue for="3" value="{esc(o["level"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges: person -> organization
lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

# Edges: person <-> person (relationships)
for r in relationships:
    if r["person_a"] == r["person_b"]:
        # Skip self-references (like the 百色市委→德保县委 abstract relationship)
        continue
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"GEXF ready: {GEXF_PATH}")

# =========================================================================
# 8. PERSON JSON (陆兰碧)
# =========================================================================

person_json_lulanbi = {
    "schema_version": "1.0",
    "generated_at": AS_OF,
    "investigation_scope": {
        "province": "广西壮族自治区",
        "city": "百色市",
        "region": "德保县",
        "job": "县委书记",
        "task_id": "guangxi_德保县",
        "time_focus": "2026"
    },
    "identity": {
        "person_id": "guangxi_baise_debao_lulanbi",
        "name": "陆兰碧",
        "aliases": [],
        "gender": "女",
        "ethnicity": "壮族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": [],
        "party_join": "中共党员",
        "work_start": "",
        "dedupe_keys": {
            "name_birth": "陆兰碧",
            "name_birthplace": "",
            "official_profile_url": ""
        }
    },
    "current_status": {
        "current_post": "百色市人大常委会副主任（兼德保县委书记）",
        "current_org": "中共德保县委员会/百色市人民代表大会常务委员会",
        "administrative_rank": "副厅级（高配）",
        "as_of": AS_OF,
        "is_current_confirmed": True,
        "source_ids": ["S001"]
    },
    "career_timeline": [
        {
            "start": "待查",
            "end": "present",
            "org": "中共德保县委员会",
            "title": "德保县委书记",
            "level": "县处级",
            "location": "广西百色市德保县",
            "system": "party",
            "rank": "正处级（高配副厅级）",
            "is_key_promotion": True,
            "notes": "同时担任百色市人大常委会副主任",
            "confidence": "confirmed",
            "source_ids": ["S001"]
        },
        {
            "start": "待查",
            "end": "present",
            "org": "百色市人民代表大会常务委员会",
            "title": "百色市人大常委会副主任",
            "level": "地厅级",
            "location": "广西百色市",
            "system": "party",
            "rank": "副厅级",
            "is_key_promotion": True,
            "notes": "兼德保县委书记",
            "confidence": "confirmed",
            "source_ids": ["S001"]
        }
    ],
    "organizations": [
        {"org_id": "org_debao_party", "name": "中共德保县委员会", "role": "县委书记", "period": "present"},
        {"org_id": "org_baise_people_congress", "name": "百色市人民代表大会常务委员会", "role": "副主任", "period": "present"}
    ],
    "relationships": [
        {
            "person": "待查（县长）",
            "person_id": "unknown_mayor",
            "relationship_type": "overlap",
            "strength": "strong",
            "evidence": "党政搭档——县委书记与县长为德保县党政主要领导班子成员",
            "overlap_org": "德保县党政班子",
            "overlap_period": "",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": []
        }
    ],
    "governance_record": [],
    "professional_profile": {
        "primary_specializations": [],
        "secondary_specializations": [],
        "career_pattern": "local_ladder",
        "systems_experience": ["party"],
        "geographic_pattern": ["广西壮族自治区"],
        "promotion_velocity": {
            "summary": "履历尚不完整，无法评估晋升速度",
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
            "description": "公开搜索未发现违纪处分、审计问题或负面报道",
            "date": "",
            "confidence": "plausible",
            "source_ids": []
        }
    ],
    "source_register": [
        {
            "id": "S001",
            "title": "百色市第五届人大常委会主任、副主任、秘书长、副秘书长、委员",
            "url": "https://www.gxbsrd.gov.cn/html/news-view-78719.html",
            "publisher": "广西百色人大网",
            "published_at": "2026-03-11",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认陆兰碧为百色市人大常委会副主任（兼德保县委书记）"
        }
    ],
    "confidence_summary": {
        "identity": "confirmed",
        "current_role": "confirmed",
        "career_completeness": "thin",
        "relationship_confidence": "low",
        "biggest_gap": "完整履历、出生年月、教育背景、早期任职经历均缺失"
    },
    "open_questions": [
        {
            "priority": "critical",
            "question": "陆兰碧的完整履历（出生年月、出生地、教育背景、早期任职经历）",
            "why_it_matters": "无法评估其晋升路径、系统背景和工作能力",
            "suggested_queries": ["陆兰碧 简历", "陆兰碧 德保 任职经历", "陆兰碧 出生"],
            "last_attempted": AS_OF
        },
        {
            "priority": "critical",
            "question": "谁是现任德保县县长",
            "why_it_matters": "县长是县级政府一把手，与县委书记为党政主要搭档",
            "suggested_queries": ["德保县 县长", "德保县 人民政府", "德保县 领导分工"],
            "last_attempted": AS_OF
        },
        {
            "priority": "high",
            "question": "陆兰碧何时接任德保县委书记，前任是谁",
            "why_it_matters": "了解干部调整节奏和交接背景",
            "suggested_queries": ["德保县委书记 任免", "德保县 陆兰碧 任职"],
            "last_attempted": AS_OF
        },
        {
            "priority": "high",
            "question": "德保县四家班子（县人大常委会主任、县政协主席）完整名单",
            "why_it_matters": "完整班子构成是了解县级政治生态的基础",
            "suggested_queries": ["德保县人大常委会主任", "德保县政协主席"],
            "last_attempted": AS_OF
        },
        {
            "priority": "medium",
            "question": "陆兰碧的政绩表现和分管领域",
            "why_it_matters": "了解其治理风格和工作重心",
            "suggested_queries": ["陆兰碧 调研", "陆兰碧 讲话", "德保 陆兰碧 主持"],
            "last_attempted": AS_OF
        }
    ]
}

# Write person JSON for 陆兰碧
json_path = os.path.join(PERSONS_DIR, f"{AS_OF}-广西壮族自治区-百色市-县委书记-陆兰碧.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(person_json_lulanbi, f, ensure_ascii=False, indent=2)
print(f"Person JSON written: {json_path}")

print("\n=== BUILD COMPLETE ===")
print(f"DB:  {DB_PATH}")
print(f"GEXF: {GEXF_PATH}")
print(f"JSON: {json_path}")
