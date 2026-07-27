#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
汪清县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 吉林省
Parent City: 延边朝鲜族自治州
Region: 汪清县
Targets: 县委书记 & 县长

Current officeholders (as of 2026-07-25):
- 县委书记: 待查 (无法通过网络验证)
- 县长: 待查 (无法通过网络验证)

NOTE: Web access to government sites (wangqing.gov.cn, baidu, jina) was unavailable during
the investigation period. All current officeholder names are UNKNOWN and marked with
confidence="unverified". Person JSON files are created with open_questions documenting
the gaps. This build provides the structural scaffold for future investigation.
"""

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "汪清县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / "build_汪清县_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：县委书记 (UNKNOWN)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "待查（县委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汪清县委书记",
        "current_org": "中共汪清县委员会",
        "source": ""
    },
    # ════════════════════════════════════════
    # 核心领导：县长 (UNKNOWN)
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "待查（县长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汪清县委副书记、县长",
        "current_org": "汪清县人民政府",
        "source": ""
    },
    # ════════════════════════════════════════
    # 县人大常委会主任 (UNKNOWN)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "待查（人大主任）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汪清县人大常委会主任",
        "current_org": "汪清县人民代表大会常务委员会",
        "source": ""
    },
    # ════════════════════════════════════════
    # 县政协主席 (UNKNOWN)
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "待查（政协主席）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汪清县政协主席",
        "current_org": "中国人民政治协商会议汪清县委员会",
        "source": ""
    },
    # ════════════════════════════════════════
    # 县委副书记 (UNKNOWN)
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "待查（县委副书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汪清县委副书记",
        "current_org": "中共汪清县委员会",
        "source": ""
    },
    # ════════════════════════════════════════
    # 县委常委、常务副县长 (UNKNOWN)
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "待查（常务副县长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汪清县委常委、常务副县长",
        "current_org": "汪清县人民政府",
        "source": ""
    },
    # ════════════════════════════════════════
    # 县委常委、组织部部长 (UNKNOWN)
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "待查（组织部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汪清县委常委、组织部部长",
        "current_org": "中共汪清县委组织部",
        "source": ""
    },
    # ════════════════════════════════════════
    # 县委常委、纪委书记（监委主任）(UNKNOWN)
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "待查（纪委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汪清县委常委、纪委书记、监委主任",
        "current_org": "中共汪清县纪律检查委员会",
        "source": ""
    },
    # ════════════════════════════════════════
    # 县委常委、政法委书记 (UNKNOWN)
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "待查（政法委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汪清县委常委、政法委书记",
        "current_org": "中共汪清县委政法委员会",
        "source": ""
    },
    # ════════════════════════════════════════
    # 县委常委、宣传部部长 (UNKNOWN)
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "待查（宣传部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汪清县委常委、宣传部部长",
        "current_org": "中共汪清县委宣传部",
        "source": ""
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
orgs = [
    {"id": 1, "name": "中共汪清县委员会", "type": "党委"},
    {"id": 2, "name": "汪清县人民政府", "type": "政府"},
    {"id": 3, "name": "汪清县人民代表大会常务委员会", "type": "人大"},
    {"id": 4, "name": "中国人民政治协商会议汪清县委员会", "type": "政协"},
    {"id": 5, "name": "中共汪清县委组织部", "type": "党委"},
    {"id": 6, "name": "中共汪清县纪律检查委员会", "type": "纪委"},
    {"id": 7, "name": "中共汪清县委政法委员会", "type": "党委"},
    {"id": 8, "name": "中共汪清县委宣传部", "type": "党委"},
]

# =========================================================================
# 3. POSITIONS (任职关系)
# =========================================================================
positions = [
    # 县委书记 -> 县委
    {"person_id": 1, "org_id": 1, "title": "汪清县委书记", "start": "", "end": "present", "source": "", "confidence": "unverified"},
    # 县长 -> 县政府 (兼县委副书记)
    {"person_id": 2, "org_id": 2, "title": "汪清县长", "start": "", "end": "present", "source": "", "confidence": "unverified"},
    {"person_id": 2, "org_id": 1, "title": "汪清县委副书记", "start": "", "end": "present", "source": "", "confidence": "unverified"},
    # 人大主任 -> 人大
    {"person_id": 3, "org_id": 3, "title": "汪清县人大常委会主任", "start": "", "end": "present", "source": "", "confidence": "unverified"},
    # 政协主席 -> 政协
    {"person_id": 4, "org_id": 4, "title": "汪清县政协主席", "start": "", "end": "present", "source": "", "confidence": "unverified"},
    # 县委副书记 -> 县委
    {"person_id": 5, "org_id": 1, "title": "汪清县委副书记", "start": "", "end": "present", "source": "", "confidence": "unverified"},
    # 常务副县长 -> 县政府
    {"person_id": 6, "org_id": 2, "title": "汪清县委常委、常务副县长", "start": "", "end": "present", "source": "", "confidence": "unverified"},
    # 组织部长 -> 组织部
    {"person_id": 7, "org_id": 5, "title": "汪清县委常委、组织部部长", "start": "", "end": "present", "source": "", "confidence": "unverified"},
    # 纪委书记 -> 纪委
    {"person_id": 8, "org_id": 6, "title": "汪清县委常委、纪委书记、监委主任", "start": "", "end": "present", "source": "", "confidence": "unverified"},
    # 政法委书记 -> 政法委
    {"person_id": 9, "org_id": 7, "title": "汪清县委常委、政法委书记", "start": "", "end": "present", "source": "", "confidence": "unverified"},
    # 宣传部长 -> 宣传部
    {"person_id": 10, "org_id": 8, "title": "汪清县委常委、宣传部部长", "start": "", "end": "present", "source": "", "confidence": "unverified"},
]

# =========================================================================
# 4. RELATIONSHIPS (人物关系)
# =========================================================================
relationships = [
    # 县委书记 <-> 县长 (共事关系)
    {
        "person1_id": 1, "person2_id": 2, "type": "共事",
        "strength": "strong", "org": "汪清县四套班子",
        "period": "待查", "source": "", "confidence": "unverified"
    },
    # 县委书记 <-> 县委副书记 (上下级)
    {
        "person1_id": 1, "person2_id": 5, "type": "上下级",
        "strength": "strong", "org": "中共汪清县委员会",
        "period": "待查", "source": "", "confidence": "unverified"
    },
    # 县长 <-> 常务副县长 (上下级)
    {
        "person1_id": 2, "person2_id": 6, "type": "上下级",
        "strength": "strong", "org": "汪清县人民政府",
        "period": "待查", "source": "", "confidence": "unverified"
    },
    # 县委书记 <-> 组织部长 (干部管理)
    {
        "person1_id": 1, "person2_id": 7, "type": "上下级",
        "strength": "medium", "org": "中共汪清县委员会",
        "period": "待查", "source": "", "confidence": "unverified"
    },
    # 县委书记 <-> 纪委书记 (监督关系)
    {
        "person1_id": 1, "person2_id": 8, "type": "上下级",
        "strength": "medium", "org": "中共汪清县委员会",
        "period": "待查", "source": "", "confidence": "unverified"
    },
    # 县委书记 <-> 政法委书记
    {
        "person1_id": 1, "person2_id": 9, "type": "上下级",
        "strength": "medium", "org": "中共汪清县委员会",
        "period": "待查", "source": "", "confidence": "unverified"
    },
    # 县长 <-> 宣传部长
    {
        "person1_id": 2, "person2_id": 10, "type": "共事",
        "strength": "medium", "org": "汪清县",
        "period": "待查", "source": "", "confidence": "unverified"
    },
]

# =========================================================================
# 5. GEXF 生成
# =========================================================================

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(post):
    """Color person node by role (gexf_pattern.md scheme)."""
    if "书记" in post and "纪委" not in post and "政法" not in post:
        return "255,50,50"       # Red — party secretary
    elif "县长" in post or "区长" in post or "副市长" in post or "副县" in post:
        return "50,100,255"      # Blue — government head
    elif "纪委" in post or "监委" in post:
        return "255,165,0"       # Orange — discipline
    else:
        return "100,100,100"     # Grey — others

def org_color(o):
    t = o.get("type", "")
    if t == "党委":
        return "255,200,200"     # Pink
    elif t == "政府":
        return "200,200,255"     # Light blue
    elif t == "人大":
        return "200,255,255"     # Cyan
    elif t == "政协":
        return "255,240,200"     # Cream
    elif t == "纪委":
        return "255,220,180"     # Light orange
    else:
        return "200,200,200"

def is_top_leader(p):
    return "县委书记" in p["current_post"] or "县长" in p["current_post"]

def build_gexf():
    from datetime import datetime
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append('    <description>汪清县领导班子工作关系网络 — 吉林省延边朝鲜族自治州汪清县</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('      <attribute id="5" title="org_type" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="confidence" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p.get("current_post", ""))
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth", ""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in orgs:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append(f'          <attvalue for="5" value="{esc(o.get("type", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person->Organization edges (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("confidence", "plausible"))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person->Person edges (relationships)
    for rel in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{rel["person1_id"]}" target="p{rel["person2_id"]}" label="{esc(rel["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rel["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel.get("confidence", "plausible"))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(rel.get("period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH}")


# =========================================================================
# 6. Build SQLite DB
# =========================================================================
def build_db():
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    c.execute("""
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
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT ''
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT DEFAULT '',
            end TEXT DEFAULT '',
            source TEXT DEFAULT '',
            confidence TEXT DEFAULT 'plausible',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            person1_id INTEGER,
            person2_id INTEGER,
            type TEXT,
            strength TEXT DEFAULT 'medium',
            org TEXT DEFAULT '',
            period TEXT DEFAULT '',
            source TEXT DEFAULT '',
            confidence TEXT DEFAULT 'plausible',
            FOREIGN KEY (person1_id) REFERENCES persons(id),
            FOREIGN KEY (person2_id) REFERENCES persons(id)
        )
    """)

    # Insert data
    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
             p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
             p.get("party_join", ""), p.get("work_start", ""),
             p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in orgs:
        c.execute("INSERT OR REPLACE INTO organizations (id, name, type) VALUES (?,?,?)",
                  (o["id"], o["name"], o.get("type", "")))

    for pos in positions:
        c.execute("""INSERT OR REPLACE INTO positions
            (person_id, org_id, title, start, end, source, confidence)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos.get("start", ""), pos.get("end", ""),
             pos.get("source", ""), pos.get("confidence", "plausible")))

    for rel in relationships:
        c.execute("""INSERT OR REPLACE INTO relationships
            (person1_id, person2_id, type, strength, org, period, source, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (rel["person1_id"], rel["person2_id"], rel["type"],
             rel.get("strength", "medium"), rel.get("org", ""),
             rel.get("period", ""), rel.get("source", ""),
             rel.get("confidence", "plausible")))

    conn.commit()
    conn.close()
    print(f"  DB: {DB_PATH}")


# =========================================================================
# 7. Person JSON 生成
# =========================================================================
def write_person_json(person, job_title):
    """Write a single person JSON file."""
    person_id_str = f"wangqing_{person['name']}"
    filename = f"{TODAY}-吉林省-延边朝鲜族自治州-{job_title}-{person['name']}.json"
    filepath = PERSONS_DIR / filename

    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "吉林省",
            "city": "延边朝鲜族自治州",
            "region": "汪清县",
            "job": job_title,
            "task_id": "jilin_汪清县",
            "time_focus": ""
        },
        "identity": {
            "person_id": person_id_str,
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
                "name_birth": f"{person['name']}_{person.get('birth','')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace','')}",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正县处级",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": []
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": person.get("current_org", ""),
                "title": person.get("current_post", ""),
                "level": "正县处级",
                "location": "吉林省延边朝鲜族自治州汪清县",
                "system": "party" if "书记" in job_title and "纪委" not in job_title else "government",
                "rank": "正县处级",
                "is_key_promotion": True,
                "notes": f"Current role as of {AS_OF}. Full career history not available — web research was blocked.",
                "confidence": "unverified",
                "source_ids": []
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": "公开资料无法获取 — 汪清县政府网站 (wangqing.gov.cn) 和百度百科均无法访问",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "organizations": [
            {
                "org_name": person.get("current_org", ""),
                "org_type": person.get("current_org", ""),
                "role": person.get("current_post", ""),
                "period": f"unknown~present"
            }
        ],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "无法评估 — 缺少简历信息",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment. No data available due to blocked web access."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "无法通过网络获取任何纪律或廉洁信息",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "所有身份信息和履历均无法通过网络验证"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"汪清县{job_title}的姓名是什么？出生年月？籍贯？",
                "why_it_matters": "核心领导的身份信息是关系网络分析的基础",
                "suggested_queries": [
                    f"汪清县 {person.get('current_post','')}",
                    f"汪清县 领导之窗",
                    "wangqing.gov.cn 领导分工",
                    f"延边 汪清县 {person.get('current_post','')} 简历"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"{person.get('current_post','')}的完整履历？",
                "why_it_matters": "履历信息用于追溯前任继任关系和共事交集",
                "suggested_queries": [
                    f"延边 汪清县 {person.get('current_post','')} 任前公示"
                ],
                "last_attempted": AS_OF
            }
        ]
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {filepath}")


def build_person_jsons():
    # Write person JSON for each core figure
    write_person_json(persons[0], "县委书记")  # 县委书记
    write_person_json(persons[1], "县长")      # 县长
    # Also write placeholder for 人大主任, 政协主席 etc if names were known
    # These are deferred until actual names are discovered


# =========================================================================
# Main
# =========================================================================
if __name__ == "__main__":
    print(f"Building {SLUG} network...")
    build_db()
    build_gexf()
    build_person_jsons()
    print("Done.")
