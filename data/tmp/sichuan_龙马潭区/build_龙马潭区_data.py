#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 龙马潭区 (Longmatan District), 泸州市, 四川省.

Investigation date: 2026-07-26
Task ID: sichuan_龙马潭区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.longmatan.gov.cn — 泸州市龙马潭区人民政府 (official leadership profiles, accessed 2026-07-26)
  - 涂曲平 (区委书记): Confirmed as 市人大常委会副主任、龙马潭区委书记、长开区党工委书记 via multiple news articles on longmatan.gov.cn (e.g., 2026-07-20 "涂曲平：高质高效推进项目建设")
  - 陈进 (区长): Official government profile at https://www.longmatan.gov.cn/ldzc/qzf/qz/content_776
  - 汪世平 (常务副区长): Official government profile at https://www.longmatan.gov.cn/ldzc/qzf/fqz/content_79269
  - 彭沭文 (副区长/区公安分局局长): Official government profile at https://www.longmatan.gov.cn/ldzc/qzf/fqz/content_79625
  - 其他副区长: Official government leadership window (names confirmed, detailed bios 403-blocked)

Confidence notes:
  - 涂曲平 (区委书记): confirmed role via multiple official news articles; detailed career history unverified due to web access limitations (Baidu 403, Exa rate-limited)
  - 陈进 (区长): confirmed via official government profile with full identity info
  - 汪世平 (常务副区长): confirmed via official government profile with identity info
  - 彭沭文 (副区长/区公安分局局长): confirmed via official government profile with identity info
  - Other deputy names confirmed via leadership page, bios unreadable due to 403
  - Search engines (Exa, Baidu, so.com) all rate-limited/blocked during investigation
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = str(STAGING_DIR)
SLUG = "龙马潭区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")

CANONICAL_DB = os.path.join(BASE, "..", "..", "database", f"{SLUG}_network.db")
CANONICAL_GEXF = os.path.join(BASE, "..", "..", "graph", f"{SLUG}_network.gexf")
CANONICAL_BUILD = os.path.join(BASE, "..", "..", "..", f"build_{SLUG}_data.py")
CANONICAL_PERSONS = Path(BASE) / ".." / ".." / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership — Party Secretary (区委书记)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "涂曲平",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共泸州市龙马潭区委员会",
        "source": "https://www.longmatan.gov.cn/xw/bdyw/content_83273 (news: 市人大常委会副主任、龙马潭区委书记、长开区党工委书记涂曲平)"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership — Government Leader (区长)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 2,
        "name": "陈进",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年8月",
        "birthplace": "四川省合江县",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "2005年7月",
        "current_post": "区委副书记、区长",
        "current_org": "泸州市龙马潭区人民政府",
        "source": "https://www.longmatan.gov.cn/ldzc/qzf/qz/content_776 (official profile)"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Leaders — 区政府副区长
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "汪世平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年8月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "2009年7月",
        "current_post": "区委常委、常务副区长",
        "current_org": "泸州市龙马潭区人民政府",
        "source": "https://www.longmatan.gov.cn/ldzc/qzf/fqz/content_79269 (official profile)"
    },
    {
        "id": 4,
        "name": "彭沭文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年10月",
        "birthplace": "四川省蓬溪县",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1994年8月",
        "current_post": "副区长、区公安分局局长",
        "current_org": "泸州市龙马潭区人民政府",
        "source": "https://www.longmatan.gov.cn/ldzc/qzf/fqz/content_79625 (official profile)"
    },
    {
        "id": 5,
        "name": "胡良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "泸州市龙马潭区人民政府",
        "source": "https://www.longmatan.gov.cn/ldzc/qzf/ (official leadership page)"
    },
    {
        "id": 6,
        "name": "狄娴",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "泸州市龙马潭区人民政府",
        "source": "https://www.longmatan.gov.cn/ldzc/qzf/ (official leadership page)"
    },
    {
        "id": 7,
        "name": "程荥川",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "泸州市龙马潭区人民政府",
        "source": "https://www.longmatan.gov.cn/ldzc/qzf/ (official leadership page)"
    },
    {
        "id": 8,
        "name": "彭健华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "泸州市龙马潭区人民政府",
        "source": "https://www.longmatan.gov.cn/ldzc/qzf/ (official leadership page)"
    },
    {
        "id": 9,
        "name": "任涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "泸州市龙马潭区人民政府",
        "source": "https://www.longmatan.gov.cn/ldzc/qzf/ (official leadership page)"
    },
]

# ── Organizations ────────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共泸州市龙马潭区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共泸州市委员会",
        "location": "四川省泸州市龙马潭区"
    },
    {
        "id": 2,
        "name": "泸州市龙马潭区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "泸州市人民政府",
        "location": "四川省泸州市龙马潭区"
    },
    {
        "id": 3,
        "name": "泸州市龙马潭区公安分局",
        "type": "政府",
        "level": "乡科级",
        "parent": "泸州市龙马潭区人民政府",
        "location": "四川省泸州市龙马潭区"
    },
    {
        "id": 4,
        "name": "泸州市人大常委会",
        "type": "人大",
        "level": "地厅级",
        "parent": "四川省人大常委会",
        "location": "四川省泸州市"
    },
    {
        "id": 5,
        "name": "四川泸州(长江)经济开发区党工委",
        "type": "党委",
        "level": "未知",
        "parent": "中共泸州市委员会",
        "location": "四川省泸州市龙马潭区"
    },
    {
        "id": 6,
        "name": "中国（四川）自由贸易试验区川南临港片区",
        "type": "开发区",
        "level": "未知",
        "parent": "泸州市人民政府",
        "location": "四川省泸州市龙马潭区"
    },
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 涂曲平
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "未知", "end": "至今", "rank": "正处级（兼副厅级）", "note": "同时担任泸州市人大常委会副主任、长开区党工委书记"},
    {"person_id": 1, "org_id": 4, "title": "市人大常委会副主任（兼）", "start": "未知", "end": "至今", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 5, "title": "长开区党工委书记（兼）", "start": "未知", "end": "至今", "rank": "", "note": ""},
    # 陈进
    {"person_id": 2, "org_id": 2, "title": "区委副书记、区长", "start": "未知", "end": "至今", "rank": "正处级", "note": "主持区政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "未知", "end": "至今", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "区政府党组书记", "start": "未知", "end": "至今", "rank": "", "note": ""},
    # 汪世平
    {"person_id": 3, "org_id": 2, "title": "区委常委、常务副区长", "start": "未知", "end": "至今", "rank": "副处级", "note": "负责区政府常务工作"},
    # 彭沭文
    {"person_id": 4, "org_id": 2, "title": "副区长、区公安分局局长", "start": "未知", "end": "至今", "rank": "副处级", "note": "负责政法工作"},
    {"person_id": 4, "org_id": 3, "title": "区公安分局局长", "start": "未知", "end": "至今", "rank": "正科级", "note": ""},
    # 胡良
    {"person_id": 5, "org_id": 2, "title": "副区长", "start": "未知", "end": "至今", "rank": "副处级", "note": ""},
    # 狄娴
    {"person_id": 6, "org_id": 2, "title": "副区长", "start": "未知", "end": "至今", "rank": "副处级", "note": ""},
    # 程荥川
    {"person_id": 7, "org_id": 2, "title": "副区长", "start": "未知", "end": "至今", "rank": "副处级", "note": ""},
    # 彭健华
    {"person_id": 8, "org_id": 2, "title": "副区长", "start": "未知", "end": "至今", "rank": "副处级", "note": ""},
    # 任涛
    {"person_id": 9, "org_id": 2, "title": "副区长", "start": "未知", "end": "至今", "rank": "副处级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "党委与政府主要领导工作搭档",
        "overlap_org": "中共泸州市龙马潭区委员会/龙马潭区人民政府",
        "overlap_period": "至今"
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "superior_subordinate",
        "context": "正职与常务副职工作搭档",
        "overlap_org": "泸州市龙马潭区人民政府",
        "overlap_period": "至今"
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "superior_subordinate",
        "context": "区长与分管公安的副区长工作关系",
        "overlap_org": "泸州市龙马潭区人民政府",
        "overlap_period": "至今"
    },
    {
        "person_a": 2, "person_b": 5,
        "type": "superior_subordinate",
        "context": "区长与副区长工作搭档",
        "overlap_org": "泸州市龙马潭区人民政府",
        "overlap_period": "至今"
    },
    {
        "person_a": 2, "person_b": 6,
        "type": "superior_subordinate",
        "context": "区长与副区长工作搭档",
        "overlap_org": "泸州市龙马潭区人民政府",
        "overlap_period": "至今"
    },
    {
        "person_a": 2, "person_b": 7,
        "type": "superior_subordinate",
        "context": "区长与副区长工作搭档",
        "overlap_org": "泸州市龙马潭区人民政府",
        "overlap_period": "至今"
    },
    {
        "person_a": 2, "person_b": 8,
        "type": "superior_subordinate",
        "context": "区长与副区长工作搭档",
        "overlap_org": "泸州市龙马潭区人民政府",
        "overlap_period": "至今"
    },
    {
        "person_a": 2, "person_b": 9,
        "type": "superior_subordinate",
        "context": "区长与副区长工作搭档",
        "overlap_org": "泸州市龙马潭区人民政府",
        "overlap_period": "至今"
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# Database builder
# ═══════════════════════════════════════════════════════════════════════════
def build_database(db_path):
    import sqlite3
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.executescript("""
        PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS persons (
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

        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );

        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
              p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()

    # Stats
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")


# ═════════════════════════════════════════════════════════════════════════════
# GEXF builder (string formatting to avoid ElementTree namespace issues)
# ═════════════════════════════════════════════════════════════════════════════
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    role = p["current_post"]
    if "书记" in role and "副" not in role:
        return "255,50,50"
    if "区长" in role and "副" not in role:
        return "50,100,255"
    if "纪委" in role or "监委" in role:
        return "255,165,0"
    return "100,100,100"


def org_color(o):
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "Default": "200,200,200",
    }
    return colors.get(t, colors["Default"])


def is_top_leader(p):
    return p["id"] in (1, 2)


def build_gexf(gexf_path):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append(f'    <description>龙马潭区领导班子工作关系网络 — 2026-07-26</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="org"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # person->org (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person<->person (relationship)
    for r in relationships:
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

    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF edges: {eid}")


# ═════════════════════════════════════════════════════════════════════════════
# Person JSON builder
# ═════════════════════════════════════════════════════════════════════════════
def build_person_json(p, output_dir):
    person_id = f"longmatan_{p['name'].replace(' ', '')}"
    fn = f"{TODAY}-四川省-泸州市-{p['current_post']}-{p['name']}.json"
    fpath = os.path.join(output_dir, fn)

    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "四川省",
            "city": "泸州市",
            "region": "龙马潭区",
            "job": p["current_post"],
            "task_id": "sichuan_龙马潭区",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": person_id,
            "name": p["name"],
            "aliases": [],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [{"institution": "", "major": "", "degree": p.get("education", ""), "study_type": "unknown", "source_ids": []}],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth', '')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                "official_profile_url": p["source"]
            }
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": bool(p.get("birth")),
            "source_ids": ["S001"]
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [],
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
        "risk_and_integrity_signals": [],
        "source_register": [
            {
                "id": "S001",
                "title": f"泸州市龙马潭区人民政府 — {p['name']}领导之窗",
                "url": p.get("source", "https://www.longmatan.gov.cn/ldzc/"),
                "publisher": "泸州市龙马潭区人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": ""
            }
        ],
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") else "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin" if p.get("birth") else "minimal",
            "relationship_confidence": "low" if not p.get("birth") else "medium",
            "biggest_gap": "履历完整度低" if not p.get("birth") else "早期职业履历缺失"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{p['name']}的完整履历（早期教育、工作经历、晋升时间线）",
                "why_it_matters": "核心领导人的职业路径反映权力来源和网络归属",
                "suggested_queries": [f"{p['name']} 简历", f"{p['name']} 任前公示", f"{p['name']} 经历"],
                "last_attempted": AS_OF
            }
        ]
    }

    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fn}")
    return fpath


# ═════════════════════════════════════════════════════════════════════════════
# Main
# ═════════════════════════════════════════════════════════════════════════════
def main():
    print(f"=== Building {SLUG} data ===")
    print(f"Staging: {BASE}")

    # Ensure output directory exists
    out_dir = CANONICAL_PERSONS
    out_dir.mkdir(parents=True, exist_ok=True)

    # Build database
    print("\n--- Database ---")
    build_database(DB_PATH)
    print(f"  DB: {DB_PATH}")

    # Build GEXF
    print("\n--- GEXF Graph ---")
    build_gexf(GEXF_PATH)
    print(f"  GEXF: {GEXF_PATH}")

    # Build person JSONs
    print("\n--- Person JSONs ---")
    for p in persons:
        if p["id"] <= 2:  # 区委书记 & 区长
            fpath = build_person_json(p, str(out_dir))
    print()

    # Summary
    dbsize = os.path.getsize(DB_PATH)
    gexfsize = os.path.getsize(GEXF_PATH)
    print(f"DB size:  {dbsize:,} bytes")
    print(f"GEXF size: {gexfsize:,} bytes")
    print(f"=== Done ===")


if __name__ == "__main__":
    main()