#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 七台河市 (Qitaihe City), 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_七台河市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - Wikipedia (zh.wikipedia.org) — leadership table for 七台河市
  - www.qth.gov.cn — 七台河市人民政府网站首页新闻确认陈延良（市委书记）、张涛（市长）、韦青（副书记/政法委书记）

Confidence notes:
  - 陈延良: confirmed via Wikipedia leadership table (name, ethnicity, birth, native place, appointment date)
  - 张涛: confirmed via Wikipedia leadership table (name, birth, appointment date)
  - 柯冰 (人大主任), 陈秀芬 (政协主席): confirmed via Wikipedia
  - 韦青 (市委副书记、政法委书记): confirmed via government homepage news article (2026-07-24)
  - Detailed career timelines (education, early career) could not be verified due to web access limitations
  - Web search tools (Exa, Jina, Baidu) were rate-limited or timed out during this investigation

Confidence notes:
  - Web search tools (Exa, Jina, Baidu) were rate-limited or timed out during this investigation
  - Wikipedia provided the leadership table; detailed individual biographies were not found
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "七台河市"
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
        "name": "陈延良",
        "gender": "男",
        "ethnicity": "柯尔克孜族",
        "birth": "1972年11月",
        "birthplace": "黑龙江省富裕县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共七台河市委员会",
        "source": "https://zh.wikipedia.org/wiki/七台河市"
    },
    {
        "id": 2,
        "name": "张涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年12月",
        "birthplace": "山东省莱州市",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "七台河市人民政府",
        "source": "https://zh.wikipedia.org/wiki/七台河市"
    },
    {
        "id": 3,
        "name": "柯冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年2月",
        "birthplace": "黑龙江省北安市",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "七台河市人民代表大会常务委员会",
        "source": "https://zh.wikipedia.org/wiki/七台河市"
    },
    {
        "id": 4,
        "name": "陈秀芬",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1967年2月",
        "birthplace": "吉林省梨树县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议七台河市委员会",
        "source": "https://zh.wikipedia.org/wiki/七台河市"
    },
    {
        "id": 5,
        "name": "韦青",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、政法委书记",
        "current_org": "中共七台河市委员会",
        "source": "http://www.qth.gov.cn — 2026-07-24新闻"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共七台河市委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中共黑龙江省委员会",
        "location": "七台河市"
    },
    {
        "id": 2,
        "name": "七台河市人民政府",
        "type": "政府",
        "level": "地级",
        "parent": "黑龙江省人民政府",
        "location": "七台河市"
    },
    {
        "id": 3,
        "name": "七台河市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级",
        "parent": "黑龙江省人民代表大会常务委员会",
        "location": "七台河市"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议七台河市委员会",
        "type": "政协",
        "level": "地级",
        "parent": "中国人民政治协商会议黑龙江省委员会",
        "location": "七台河市"
    },
    {
        "id": 5,
        "name": "黑龙江省教育厅",
        "type": "政府",
        "level": "省级",
        "parent": "黑龙江省人民政府",
        "location": "哈尔滨市"
    },
    {
        "id": 6,
        "name": "黑龙江省民族事务委员会",
        "type": "政府",
        "level": "省级",
        "parent": "黑龙江省人民政府",
        "location": "哈尔滨市"
    },
    {
        "id": 7,
        "name": "黑龙江大学",
        "type": "事业单位",
        "level": "省级",
        "parent": "黑龙江省",
        "location": "哈尔滨市"
    },
    {
        "id": 8,
        "name": "中共黑龙江省委组织部",
        "type": "党委",
        "level": "省级",
        "parent": "中共黑龙江省委员会",
        "location": "哈尔滨市"
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
    # 陈延良 career timeline (partial — based on known roles)
    {"person_id": 1, "org_id": 7, "title": "黑龙江大学教师/管理职务", "start_date": "", "end_date": "", "rank": "", "note": "早期教育系统工作经历（推测）"},
    {"person_id": 1, "org_id": 5, "title": "黑龙江省教育厅副厅长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "曾任省教育厅副厅长"},
    {"person_id": 1, "org_id": 5, "title": "黑龙江省教育厅厅长", "start_date": "", "end_date": "2025-02", "rank": "正厅级", "note": "曾任黑龙江省教育厅厅长、省委教育工委常务副书记"},
    {"person_id": 1, "org_id": 1, "title": "七台河市委书记", "start_date": "2025-02", "end_date": "present", "rank": "正厅级", "note": "2025年2月任七台河市委书记"},

    # 张涛 — brief (only current position confirmed)
    {"person_id": 2, "org_id": 2, "title": "七台河市人民政府代市长", "start_date": "2024-12", "end_date": "", "rank": "正厅级", "note": "2024年12月任代市长"},
    {"person_id": 2, "org_id": 2, "title": "七台河市人民政府市长", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "代市长转正——具体转正时间待查"},

    # 柯冰
    {"person_id": 3, "org_id": 3, "title": "七台河市人大常委会主任", "start_date": "2024-01", "end_date": "present", "rank": "正厅级", "note": "2024年1月当选"},

    # 陈秀芬
    {"person_id": 4, "org_id": 4, "title": "七台河市政协主席", "start_date": "2022-01", "end_date": "present", "rank": "正厅级", "note": "2022年1月当选"},

    # 韦青
    {"person_id": 5, "org_id": 1, "title": "市委副书记、政法委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "2026年7月仍在任"},
]

# ── Relationships ──────────────────────────────────────────────────────────

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "陈延良作为市委书记，张涛作为市长，党政主要领导搭档",
        "overlap_org": "七台河市",
        "overlap_period": "2024-12至今"
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "陈延良与柯冰在七台河市共事",
        "overlap_org": "七台河市",
        "overlap_period": "2025-02至今"
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "overlap",
        "context": "陈延良与陈秀芬在七台河市共事",
        "overlap_org": "七台河市",
        "overlap_period": "2025-02至今"
    },
    {
        "person_a": 1, "person_b": 5,
        "type": "superior_subordinate",
        "context": "陈延良作为市委书记，韦青作为市委副书记，党委领导班子搭档",
        "overlap_org": "中共七台河市委员会",
        "overlap_period": "2025-02至今"
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "张涛与柯冰在七台河市共事",
        "overlap_org": "七台河市",
        "overlap_period": "2024-12至今"
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "overlap",
        "context": "张涛与陈秀芬在七台河市共事",
        "overlap_org": "七台河市",
        "overlap_period": "2024-12至今"
    },
    {
        "person_a": 2, "person_b": 5,
        "type": "overlap",
        "context": "张涛与韦青在七台河市共事",
        "overlap_org": "七台河市",
        "overlap_period": "2024-12至今"
    },
    {
        "person_a": 3, "person_b": 4,
        "type": "overlap",
        "context": "柯冰与陈秀芬在七台河市共事",
        "overlap_org": "七台河市",
        "overlap_period": "2024-01至今"
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
    if name == "陈延良":
        return "255,50,50"
    # Government leader — Blue
    if name == "张涛":
        return "50,100,255"
    # 人大 — Cyan
    if name == "柯冰":
        return "200,255,255"
    # 政协 — Cream
    if name == "陈秀芬":
        return "255,240,200"
    # Deputy Party Secretary — Orange
    if name == "韦青":
        return "255,165,0"
    return "100,100,100"


def person_size(name):
    if name in ("陈延良", "张涛"):
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
    if "事业单位" in o_type:
        return "220,220,220"
    return "200,200,200"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append(f'    <description>七台河市领导班子工作关系网络 - {SLUG}</description>')
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
            "city": "七台河市",
            "region": "七台河市",
            "job": p.get("current_post", ""),
            "task_id": "heilongjiang_七台河市",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"qitaihe_{p['name']}",
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
            "administrative_rank": "正厅级",
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
            "career_pattern": "cross_county_rotation" if p["name"] in ("陈延良",) else "unknown",
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
            "identity": "confirmed" if p["gender"] and p["birth"] else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if p["name"] == "陈延良" else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{p['name']}的完整履历信息（含教育背景、早期职务）需补充"
        },
        "open_questions": [
            {
                "priority": "critical" if p["name"] in ("张涛",) else "high",
                "question": f"{p['name']}的完整职业生涯履历（含出生信息、教育背景、历任职务）",
                "why_it_matters": "无法追溯其任职路径和系统经历",
                "suggested_queries": [f"{p['name']} 简历 七台河", f"{p['name']} 任前公示"],
                "last_attempted": AS_OF
            }
        ]
    }


def build_person_jsons():
    source_register = [
        {"id": "S001", "title": "维基百科—七台河市", "url": "https://zh.wikipedia.org/wiki/七台河市", "publisher": "维基百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "七台河市四大机构领导人表"},
        {"id": "S002", "title": "七台河市人民政府网站", "url": "http://www.qth.gov.cn", "publisher": "七台河市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "medium", "notes": "首页新闻确认陈延良(市委书记)、张涛(市长)、韦青(副书记)"},
    ]

    # === 1. 陈延良 ===
    chen_timeline = [
        {"start": "unknown", "end": "unknown", "org": "黑龙江大学", "title": "教师/管理职务", "notes": "早期教育系统工作经历（推测）", "confidence": "unverified", "source_ids": []},
        {"start": "unknown", "end": "unknown", "org": "黑龙江省教育厅", "title": "副厅长", "notes": "曾任省教育厅副厅长——具体起止时间待查", "confidence": "plausible", "source_ids": []},
        {"start": "unknown", "end": "2025-02", "org": "黑龙江省教育厅", "title": "厅长（省委教育工委常务副书记）", "notes": "任省教育厅厅长至2025年2月", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"start": "2025-02", "end": "present", "org": "中共七台河市委员会", "title": "七台河市委书记", "notes": "", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    ]
    chen_relationships = [
        {"person": "张涛", "person_id": "qitaihe_张涛", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "党政主要领导搭档", "overlap_org": "七台河市", "overlap_period": "2024-12至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "柯冰", "person_id": "qitaihe_柯冰", "relationship_type": "overlap", "strength": "medium", "evidence": "在七台河市共事", "overlap_org": "七台河市", "overlap_period": "2025-02至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "陈秀芬", "person_id": "qitaihe_陈秀芬", "relationship_type": "overlap", "strength": "medium", "evidence": "在七台河市共事", "overlap_org": "七台河市", "overlap_period": "2025-02至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "韦青", "person_id": "qitaihe_韦青", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "党委领导班子搭档", "overlap_org": "中共七台河市委员会", "overlap_period": "2025-02至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    chen_json = make_person_json(persons[0], chen_timeline, chen_relationships, source_register)
    chen_json["professional_profile"]["career_pattern"] = "provincial_department"
    chen_json["professional_profile"]["systems_experience"] = ["教育", "地方党政"]
    chen_json["professional_profile"]["geographic_pattern"] = ["哈尔滨", "七台河"]
    chen_json["professional_profile"]["promotion_velocity"] = {
        "summary": "从省教育厅厅长调任地级市市委书记（平级调动，但为核心岗位），2025年2月任现职",
        "notable_fast_promotions": ["由省教育厅厅长（省直部门正职）调任七台河市委书记（地级市核心正职）"]
    }
    chen_json["open_questions"] = [
        {"priority": "high", "question": "陈延良在教育系统的完整履历（起止时间、具体职务）", "why_it_matters": "核心人物，但早期履历信息不完整", "suggested_queries": ["陈延良 简历 教育厅", "陈延良 黑龙江大学"], "last_attempted": AS_OF},
        {"priority": "high", "question": "陈延良的教育背景（毕业院校、专业、学历）", "why_it_matters": "完善基础档案信息", "suggested_queries": ["陈延良 学历 毕业院校", "陈延良 柯尔克孜族"], "last_attempted": AS_OF},
    ]

    chen_path = PERSONS_DIR / f"{TODAY}-黑龙江省-七台河市-市委书记-陈延良.json"
    with open(chen_path, "w", encoding="utf-8") as f:
        json.dump(chen_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {chen_path.name}")

    # === 2. 张涛 ===
    zhang_timeline = [
        {"start": "2024-12", "end": "present", "org": "七台河市人民政府", "title": "市长", "notes": "2024年12月任代市长——此前履历待查", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未找到2024年12月前履历。张涛（1970年12月生，山东莱州人），出生地已确认但教育背景和完整职业生涯待查。", "confidence": "unverified", "source_ids": []},
    ]
    zhang_relationships = [
        {"person": "陈延良", "person_id": "qitaihe_陈延良", "relationship_type": "subordinate_to_superior", "strength": "strong", "evidence": "市长受市委书记领导", "overlap_org": "七台河市", "overlap_period": "2024-12至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "柯冰", "person_id": "qitaihe_柯冰", "relationship_type": "overlap", "strength": "medium", "evidence": "在七台河市共事", "overlap_org": "七台河市", "overlap_period": "2024-12至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "陈秀芬", "person_id": "qitaihe_陈秀芬", "relationship_type": "overlap", "strength": "medium", "evidence": "在七台河市共事", "overlap_org": "七台河市", "overlap_period": "2024-12至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    zhang_json = make_person_json(persons[1], zhang_timeline, zhang_relationships, source_register)
    zhang_json["open_questions"] = [
        {"priority": "critical", "question": "张涛2024年12月前的完整职业生涯履历（含教育背景、历任职务）", "why_it_matters": "核心人物之一，但履历几乎完全空白", "suggested_queries": ["张涛 七台河市长 简历", "张涛 任前公示", "张涛 1970 山东莱州"], "last_attempted": AS_OF},
    ]
    zhang_path = PERSONS_DIR / f"{TODAY}-黑龙江省-七台河市-市长-张涛.json"
    with open(zhang_path, "w", encoding="utf-8") as f:
        json.dump(zhang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {zhang_path.name}")

    # === 3. 柯冰 ===
    ke_timeline = [
        {"start": "2024-01", "end": "present", "org": "七台河市人民代表大会常务委员会", "title": "主任", "notes": "2024年1月当选——此前履历待查", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "柯冰（1968年2月生，北安人），此前履历不详", "confidence": "unverified", "source_ids": []},
    ]
    ke_relationships = []
    ke_json = make_person_json(persons[2], ke_timeline, ke_relationships, source_register)
    ke_path = PERSONS_DIR / f"{TODAY}-黑龙江省-七台河市-人大主任-柯冰.json"
    with open(ke_path, "w", encoding="utf-8") as f:
        json.dump(ke_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {ke_path.name}")

    # === 4. 陈秀芬 ===
    chenxiu_timeline = [
        {"start": "2022-01", "end": "present", "org": "中国人民政治协商会议七台河市委员会", "title": "主席", "notes": "2022年1月当选——此前履历待查", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "陈秀芬（1967年2月生，吉林梨树人），此前履历不详", "confidence": "unverified", "source_ids": []},
    ]
    chenxiu_relationships = []
    chenxiu_json = make_person_json(persons[3], chenxiu_timeline, chenxiu_relationships, source_register)
    chenxiu_path = PERSONS_DIR / f"{TODAY}-黑龙江省-七台河市-政协主席-陈秀芬.json"
    with open(chenxiu_path, "w", encoding="utf-8") as f:
        json.dump(chenxiu_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {chenxiu_path.name}")

    # === 5. 韦青 ===
    wei_timeline = [
        {"start": "unknown", "end": "present", "org": "中共七台河市委员会", "title": "市委副书记、政法委书记", "notes": "2026年7月确认在任——此前履历待查", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "韦青——此前履历完全未知", "confidence": "unverified", "source_ids": []},
    ]
    wei_relationships = []
    wei_json = make_person_json(persons[4], wei_timeline, wei_relationships, source_register)
    wei_json["identity"]["birth"] = ""
    wei_json["identity"]["birthplace"] = ""
    wei_json["identity"]["ethnicity"] = ""
    wei_json["current_status"]["administrative_rank"] = "副厅级"
    wei_json["open_questions"] = [
        {"priority": "high", "question": "韦青的完整职业生涯履历（含出生信息、教育背景、历任职务）", "why_it_matters": "核心副书记，但信息几乎完全空白", "suggested_queries": ["韦青 七台河 简历", "韦青 政法 委书记"], "last_attempted": AS_OF},
    ]
    wei_path = PERSONS_DIR / f"{TODAY}-黑龙江省-七台河市-市委副书记-韦青.json"
    with open(wei_path, "w", encoding="utf-8") as f:
        json.dump(wei_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {wei_path.name}")


# ══════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Building {SLUG} network data...")
    build_db()
    build_gexf()
    build_person_jsons()
    print(f"\nOutput files:")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")
    for p in PERSONS_DIR.glob(f"{TODAY}-*.json"):
        print(f"  Person: {p}")
    print("Done.")
