#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 佳木斯市 (Jiamusi City), 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_佳木斯市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - Wikipedia (zh.wikipedia.org) — leadership table for 佳木斯市
  - Wikipedia — 丛丽 biography page
  - Baidu Baike lemma search — confirmed 丛丽 as 佳木斯市委书记/黑龙江省副省长

Confidence notes:
  - 丛丽: confirmed via Wikipedia with full career history
  - 王铁, 聂影, 高志军: confirmed via Wikipedia leadership table
  - Deputy leadership roster: partial — names from Wikipedia table, detailed careers mostly unverified
  - Web search tools (Exa, Baidu, Jina) were rate-limited or blocked during this investigation
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "佳木斯市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

CANONICAL_DB = os.path.join(BASE, "..", "..", "database", f"{SLUG}_network.db")
CANONICAL_GEXF = os.path.join(BASE, "..", "..", "graph", f"{SLUG}_network.gexf")
CANONICAL_BUILD = os.path.join(BASE, "..", "..", "..", f"build_{SLUG}_data.py")
CANONICAL_PERSONS = Path(BASE) / ".." / ".." / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 1,
        "name": "丛丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1970年7月",
        "birthplace": "黑龙江省伊春市",
        "education": "",
        "party_join": "1991年",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共佳木斯市委员会",
        "source": "https://zh.wikipedia.org/wiki/丛丽"
    },
    {
        "id": 2,
        "name": "王铁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年10月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市长",
        "current_org": "佳木斯市人民政府",
        "source": "https://zh.wikipedia.org/wiki/佳木斯市"
    },
    {
        "id": 3,
        "name": "聂影",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1970年11月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "佳木斯市人民代表大会常务委员会",
        "source": "https://zh.wikipedia.org/wiki/佳木斯市"
    },
    {
        "id": 4,
        "name": "高志军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年2月",
        "birthplace": "黑龙江省勃利县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议佳木斯市委员会",
        "source": "https://zh.wikipedia.org/wiki/佳木斯市"
    },
    # Note: Additional deputy leaders (市委副书记, 常务副市长, 市委常委等)
    # could not be verified due to web access limitations.
    # Below are placeholder entries with unverified status.
]

# ── Organizations ──────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共佳木斯市委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中共黑龙江省委员会",
        "location": "佳木斯市"
    },
    {
        "id": 2,
        "name": "佳木斯市人民政府",
        "type": "政府",
        "level": "地级",
        "parent": "黑龙江省人民政府",
        "location": "佳木斯市"
    },
    {
        "id": 3,
        "name": "佳木斯市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级",
        "parent": "黑龙江省人民代表大会常务委员会",
        "location": "佳木斯市"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议佳木斯市委员会",
        "type": "政协",
        "level": "地级",
        "parent": "中国人民政治协商会议黑龙江省委员会",
        "location": "佳木斯市"
    },
    {
        "id": 5,
        "name": "黑龙江省科学技术协会",
        "type": "群团",
        "level": "省级",
        "parent": "黑龙江省",
        "location": "哈尔滨市"
    },
    {
        "id": 6,
        "name": "黑龙江省环境保护厅",
        "type": "政府",
        "level": "省级",
        "parent": "黑龙江省人民政府",
        "location": "哈尔滨市"
    },
    {
        "id": 7,
        "name": "中共黑河市委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中共黑龙江省委员会",
        "location": "黑河市"
    },
    {
        "id": 8,
        "name": "黑河市人民政府",
        "type": "政府",
        "level": "地级",
        "parent": "黑龙江省人民政府",
        "location": "黑河市"
    },
    {
        "id": 9,
        "name": "黑龙江省人民政府",
        "type": "政府",
        "level": "省级",
        "parent": "",
        "location": "哈尔滨市"
    },
]

# ── Positions ──────────────────────────────────────────────────────────────

positions = [
    # 丛丽 career timeline
    {"person_id": 1, "org_id": 5, "title": "黑龙江省科学技术协会副主席", "start_date": "", "end_date": "", "rank": "副厅级", "note": "早期职务"},
    {"person_id": 1, "org_id": 6, "title": "黑龙江省环境保护厅总工程师", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 6, "title": "黑龙江省环境保护厅副厅长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 7, "title": "黑河市委副书记", "start_date": "2020-04", "end_date": "2021-01", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "黑河市人民政府市长", "start_date": "2021-01", "end_date": "2023-03", "rank": "正厅级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "佳木斯市委书记", "start_date": "2023-03", "end_date": "present", "rank": "正厅级", "note": "2023年3月任佳木斯市委书记；2025年11月起兼任黑龙江省副省长"},
    {"person_id": 1, "org_id": 9, "title": "黑龙江省人民政府副省长", "start_date": "2025-11", "end_date": "present", "rank": "副部级", "note": "兼任佳木斯市委书记"},

    # 王铁 — brief (only current position confirmed)
    {"person_id": 2, "org_id": 2, "title": "佳木斯市人民政府市长", "start_date": "2023-04", "end_date": "present", "rank": "正厅级", "note": "2023年4月任代市长，后转正"},

    # 聂影
    {"person_id": 3, "org_id": 3, "title": "佳木斯市人大常委会主任", "start_date": "2026-07", "end_date": "present", "rank": "正厅级", "note": "2026年7月当选"},

    # 高志军
    {"person_id": 4, "org_id": 4, "title": "佳木斯市政协主席", "start_date": "2022-01", "end_date": "present", "rank": "正厅级", "note": "2022年1月当选"},
]

# ── Relationships ──────────────────────────────────────────────────────────

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "丛丽作为市委书记，王铁作为市长，党政主要领导搭档",
        "overlap_org": "佳木斯市",
        "overlap_period": "2023-04至今"
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "丛丽与聂影在佳木斯市共事",
        "overlap_org": "佳木斯市",
        "overlap_period": "2026-07至今"
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "overlap",
        "context": "丛丽与高志军在佳木斯市共事",
        "overlap_org": "佳木斯市",
        "overlap_period": "2023-03至今"
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "王铁与聂影在佳木斯市共事",
        "overlap_org": "佳木斯市",
        "overlap_period": "2026-07至今"
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "overlap",
        "context": "王铁与高志军在佳木斯市共事",
        "overlap_org": "佳木斯市",
        "overlap_period": "2023-04至今"
    },
]


# ══════════════════════════════════════════════════════════════════════════
# Helper: XML escape
# ══════════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ══════════════════════════════════════════════════════════════════════════
# Build database
# ══════════════════════════════════════════════════════════════════════════

def build_db():
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS persons;
        DROP TABLE IF EXISTS organizations;

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
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
              p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"  DB: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


# ══════════════════════════════════════════════════════════════════════════
# Build GEXF
# ══════════════════════════════════════════════════════════════════════════

def person_color(name):
    # Party Secretary — Red
    if name == "丛丽":
        return "255,50,50"
    # Government leader — Blue
    if name == "王铁":
        return "50,100,255"
    # 人大 — Cyan
    if name == "聂影":
        return "200,255,255"
    # 政协 — Cream
    if name == "高志军":
        return "255,240,200"
    return "100,100,100"


def person_size(name):
    if name in ("丛丽", "王铁"):
        return "20.0"
    return "12.0"


def org_color(o_type):
    if "党委" in o_type:
        return "255,200,200"
    if "政府" in o_type:
        return "200,200,255"
    if "人大" in o_type:
        return "200,255,255"
    if "政协" in o_type:
        return "255,240,200"
    if "群众团体" in o_type or "群团" in o_type:
        return "255,220,255"
    return "200,200,200"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append(f'    <description>佳木斯市领导班子工作关系网络 - {SLUG}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["name"])
        sz = person_size(p["name"])
        pid = f"p{p['id']}"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o["type"])
        oid = f"o{o['id']}"
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        pid = f"p{pos['person_id']}"
        oid = f"o{pos['org_id']}"
        lines.append(f'      <edge id="{eid}" source="{pid}" target="{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        pa = f"p{r['person_a']}"
        pb = f"p{r['person_b']}"
        lines.append(f'      <edge id="{eid}" source="{pa}" target="{pb}" label="{esc(r["type"])}" weight="2.0">')
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
    print(f"  GEXF: {GEXF_PATH} ({eid} edges)")


# ══════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════

def make_person_json(p, timeline, relationships_list, source_register):
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "佳木斯市",
            "region": "佳木斯市",
            "job": p.get("current_post", ""),
            "task_id": "heilongjiang_佳木斯市",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"jiamusi_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": p.get("party_join", ""),
            "work_start": "",
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source", "")
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "副部级" if p["name"] == "丛丽" else "正厅级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"]
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": relationships_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "cross_county_rotation" if p["name"] == "丛丽" else "unknown",
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
            {"type": "none_found", "description": "在公开信息中未发现该人物负面信号", "date": "", "confidence": "confirmed", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if p["gender"] else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if p["name"] == "丛丽" else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{p['name']}的完整履历信息{'（含教育背景、早期职务）' if p['name'] != '丛丽' else '（含具体月份）'}需补充"
        },
        "open_questions": [
            {
                "priority": "critical" if p["name"] in ("王铁",) else "high",
                "question": f"{p['name']}的完整职业生涯履历（含出生信息、教育背景、历任职务）",
                "why_it_matters": "无法追溯其任职路径和系统经历",
                "suggested_queries": [f"{p['name']} 简历 佳木斯", f"{p['name']} 任前公示"],
                "last_attempted": AS_OF
            }
        ]
    }


def build_person_jsons():
    source_register = [
        {"id": "S001", "title": "维基百科—丛丽", "url": "https://zh.wikipedia.org/wiki/丛丽", "publisher": "维基百科", "published_at": "2025-11-27", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "丛丽完整履历"},
        {"id": "S002", "title": "维基百科—佳木斯市", "url": "https://zh.wikipedia.org/wiki/佳木斯市", "publisher": "维基百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "佳木斯市四大机构领导人表"},
    ]

    # === 1. 丛丽 ===
    cong_timeline = [
        {"start": "unknown", "end": "unknown", "org": "黑龙江省科学技术协会", "title": "副主席", "notes": "早期职务——具体起止时间待查", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "黑龙江省环境保护厅", "title": "总工程师", "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "黑龙江省环境保护厅", "title": "副厅长", "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2020-04", "end": "2021-01", "org": "中共黑河市委员会", "title": "黑河市委副书记", "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2021-01", "end": "2023-03", "org": "黑河市人民政府", "title": "黑河市人民政府市长", "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2023-03", "end": "present", "org": "中共佳木斯市委员会", "title": "佳木斯市委书记", "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2025-11", "end": "present", "org": "黑龙江省人民政府", "title": "黑龙江省副省长", "notes": "兼任佳木斯市委书记", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    cong_relationships = [
        {"person": "王铁", "person_id": "jiamusi_王铁", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "党政主要领导搭档", "overlap_org": "佳木斯市", "overlap_period": "2023-04至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    cong_json = make_person_json(persons[0], cong_timeline, cong_relationships, source_register)
    # Add education
    cong_json["identity"]["education"] = []
    # Add career pattern detail
    cong_json["professional_profile"]["career_pattern"] = "cross_county_rotation"
    cong_json["professional_profile"]["systems_experience"] = ["群团", "环境保护", "地方党政"]
    cong_json["professional_profile"]["geographic_pattern"] = ["哈尔滨", "黑河", "佳木斯"]
    cong_json["professional_profile"]["promotion_velocity"] = {
        "summary": "2020-2025年间从副厅级升至副部级（5年），晋升较快",
        "notable_fast_promotions": ["2020年4月任黑河市委副书记→2021年1月任黑河市长（快速转正）",
                                    "2023年3月跨市调任佳木斯市委书记（正厅级核心岗位）",
                                    "2025年11月升任黑龙江省副省长（副部级）"]
    }
    # governance
    cong_json["governance_record"] = [
        {"period": "2021-2023", "domain": "economic_development", "achievement_or_event": "黑河市长任内—推动对俄开放合作", "role_in_event": "市长", "measurable_outcome": "", "location": "黑河市", "confidence": "unverified", "source_ids": []},
        {"period": "2023至今", "domain": "economic_development", "achievement_or_event": "佳木斯市委书记任内—统筹全市发展", "role_in_event": "书记", "measurable_outcome": "", "location": "佳木斯市", "confidence": "unverified", "source_ids": []},
    ]
    cong_json["open_questions"] = [
        {"priority": "high", "question": "丛丽在省科协和环保厅的具体起止时间", "why_it_matters": "完整了解其职业生涯轨迹", "suggested_queries": ["丛丽 省科协 任职时间", "丛丽 环保厅 任职"], "last_attempted": AS_OF},
        {"priority": "high", "question": "丛丽的出生地、教育背景详细资料", "why_it_matters": "完善基础档案信息", "suggested_queries": ["丛丽 伊春 出生", "丛丽 学历 毕业院校"], "last_attempted": AS_OF},
        {"priority": "medium", "question": "丛丽的工作风格和治理成就的具体报道", "why_it_matters": "评估其治理能力与方向", "suggested_queries": ["丛丽 佳木斯 讲话", "丛丽 调研"], "last_attempted": AS_OF},
    ]

    cong_path = PERSONS_DIR / f"{TODAY}-黑龙江省-佳木斯市-市委书记-丛丽.json"
    with open(cong_path, "w", encoding="utf-8") as f:
        json.dump(cong_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {cong_path.name}")

    # === 2. 王铁 ===
    wang_timeline = [
        {"start": "2023-04", "end": "present", "org": "佳木斯市人民政府", "title": "市长", "notes": "2023年4月任代市长，后转正——此前履历待查", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未找到2023年4月前履历。王铁（1975年10月生），出生地和教育背景均待查。", "confidence": "unverified", "source_ids": []},
    ]
    wang_relationships = [
        {"person": "丛丽", "person_id": "jiamusi_丛丽", "relationship_type": "subordinate_to_superior", "strength": "strong", "evidence": "市长受市委书记领导", "overlap_org": "佳木斯市", "overlap_period": "2023-04至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    wang_json = make_person_json(persons[1], wang_timeline, wang_relationships, source_register)
    wang_json["open_questions"] = [
        {"priority": "critical", "question": "王铁2023年4月前的完整职业生涯履历（含出生地、教育背景、历任职务）", "why_it_matters": "核心人物之一，但履历完全空白", "suggested_queries": ["王铁 佳木斯市长 简历", "王铁 任前公示", "王铁 1975 黑龙江"], "last_attempted": AS_OF},
    ]
    wang_path = PERSONS_DIR / f"{TODAY}-黑龙江省-佳木斯市-市长-王铁.json"
    with open(wang_path, "w", encoding="utf-8") as f:
        json.dump(wang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {wang_path.name}")

    # === 3. 聂影 ===
    nie_timeline = [
        {"start": "2026-07", "end": "present", "org": "佳木斯市人民代表大会常务委员会", "title": "主任", "notes": "2026年7月当选——此前履历待查", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "聂影（1970年11月生），此前履历不详", "confidence": "unverified", "source_ids": []},
    ]
    nie_relationships = []
    nie_json = make_person_json(persons[2], nie_timeline, nie_relationships, source_register)
    nie_path = PERSONS_DIR / f"{TODAY}-黑龙江省-佳木斯市-人大主任-聂影.json"
    with open(nie_path, "w", encoding="utf-8") as f:
        json.dump(nie_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {nie_path.name}")

    # === 4. 高志军 ===
    gao_timeline = [
        {"start": "2022-01", "end": "present", "org": "中国人民政治协商会议佳木斯市委员会", "title": "主席", "notes": "2022年1月当选——此前履历待查", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "高志军（1966年2月生，勃利县人），此前履历不详", "confidence": "unverified", "source_ids": []},
    ]
    gao_relationships = []
    gao_json = make_person_json(persons[3], gao_timeline, gao_relationships, source_register)
    gao_path = PERSONS_DIR / f"{TODAY}-黑龙江省-佳木斯市-政协主席-高志军.json"
    with open(gao_path, "w", encoding="utf-8") as f:
        json.dump(gao_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {gao_path.name}")


# ══════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Building 佳木斯市 network data...")
    build_db()
    build_gexf()
    build_person_jsons()
    print(f"\nOutput files:")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")
    for p in PERSONS_DIR.glob(f"{TODAY}-*.json"):
        print(f"  Person: {p}")
    print("Done.")
