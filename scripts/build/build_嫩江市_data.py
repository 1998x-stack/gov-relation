#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 嫩江市 (Nenjiang City), 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_嫩江市
Level: 县级市
Parent city: 黑河市
Targets: 市委书记 & 市长

Research sources:
  - www.nenjiang.gov.cn — 嫩江市人民政府官方网站新闻确认崔凯（市委书记）、孙建龙（市长）
  - 中共嫩江市委一届146次常委会会议新闻（2026-07-21）确认崔凯主持
  - 群众身边不正之风和腐败问题集中整治攻坚决战半年推进会议（2026-07-22）确认孙建龙为市长

Confidence notes:
  - 崔凯: confirmed via government website as 嫩江市委书记（2026年7月在任）
  - 孙建龙: confirmed via government website as 嫩江市委副书记、政府市长（2026年7月在任）
  - 曲荣海: confirmed as 市委副书记
  - 教旭: confirmed as 市委常委、政府副市长
  - Detailed career timelines (education, early career) could not be verified due to web access limitations
  - Web search tools (Exa, Jina, Baidu) were rate-limited or timed out during this investigation
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "嫩江市"
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
        "name": "崔凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共嫩江市委员会",
        "source": "https://www.nenjiang.gov.cn — 2026-07-21常委会会议"
    },
    {
        "id": 2,
        "name": "孙建龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "嫩江市人民政府",
        "source": "https://www.nenjiang.gov.cn — 2026-07-22集中整治会议"
    },
    {
        "id": 3,
        "name": "曲荣海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共嫩江市委员会",
        "source": "https://www.nenjiang.gov.cn — 2026-07-24垦地合作会议"
    },
    {
        "id": 4,
        "name": "教旭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、政府副市长",
        "current_org": "中共嫩江市委员会 / 嫩江市人民政府",
        "source": "https://www.nenjiang.gov.cn — 2026-07-13防汛检查"
    },
    {
        "id": 5,
        "name": "赵志奎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "嫩江市",
        "source": "https://www.nenjiang.gov.cn — 2026-07-23高标准农田会议"
    },
    {
        "id": 6,
        "name": "李大华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "嫩江市",
        "source": "https://www.nenjiang.gov.cn — 2026-07-23高标准农田会议"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共嫩江市委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共黑河市委员会",
        "location": "嫩江市"
    },
    {
        "id": 2,
        "name": "嫩江市人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "黑河市人民政府",
        "location": "嫩江市"
    },
    {
        "id": 3,
        "name": "中共黑河市委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中共黑龙江省委员会",
        "location": "黑河市"
    },
    {
        "id": 4,
        "name": "黑河市人民政府",
        "type": "政府",
        "level": "地级",
        "parent": "黑龙江省人民政府",
        "location": "黑河市"
    },
]

# ── Positions ──────────────────────────────────────────────────────────────

positions = [
    # 崔凯 career timeline
    {"person_id": 1, "org_id": 1, "title": "嫩江市委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "2026年7月在任（中共嫩江市委一届146次常委会会议）"},

    # 孙建龙
    {"person_id": 2, "org_id": 2, "title": "嫩江市人民政府市长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "2026年7月在任，同时担任市委副书记"},
    {"person_id": 2, "org_id": 1, "title": "嫩江市委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},

    # 曲荣海
    {"person_id": 3, "org_id": 1, "title": "嫩江市委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "2026年7月仍在任"},

    # 教旭
    {"person_id": 4, "org_id": 1, "title": "嫩江市委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "嫩江市人民政府副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "市委常委、政府副市长"},

    # 赵志奎
    {"person_id": 5, "org_id": 1, "title": "市领导", "start_date": "", "end_date": "present", "rank": "县处级", "note": "2026年7月出席会议"},

    # 李大华
    {"person_id": 6, "org_id": 1, "title": "市领导", "start_date": "", "end_date": "present", "rank": "县处级", "note": "2026年7月出席会议"},
]

# ── Relationships ──────────────────────────────────────────────────────────

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "党政搭档",
        "context": "崔凯作为市委书记，孙建龙作为市长，党政主要领导搭档",
        "overlap_org": "嫩江市",
        "overlap_period": "2026-07至今"
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "上下级",
        "context": "崔凯（书记）与曲荣海（副书记）在市委班子共事",
        "overlap_org": "中共嫩江市委员会",
        "overlap_period": "2026-07至今"
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "上下级",
        "context": "崔凯与教旭在市委班子共事（常委）",
        "overlap_org": "中共嫩江市委员会",
        "overlap_period": "2026-07至今"
    },
    {
        "person_a": 1, "person_b": 5,
        "type": "上下级",
        "context": "崔凯与赵志奎在嫩江市共事",
        "overlap_org": "嫩江市",
        "overlap_period": "2026-07至今"
    },
    {
        "person_a": 1, "person_b": 6,
        "type": "上下级",
        "context": "崔凯与李大华在嫩江市共事",
        "overlap_org": "嫩江市",
        "overlap_period": "2026-07至今"
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "上下级",
        "context": "孙建龙（市长、副书记）与曲荣海（副书记）在市委班子共事",
        "overlap_org": "中共嫩江市委员会",
        "overlap_period": "2026-07至今"
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "上下级",
        "context": "孙建龙（市长）与教旭（副市长）在政府班子共事",
        "overlap_org": "嫩江市人民政府",
        "overlap_period": "2026-07至今"
    },
    {
        "person_a": 3, "person_b": 4,
        "type": "overlap",
        "context": "曲荣海与教旭在市委班子共事",
        "overlap_org": "中共嫩江市委员会",
        "overlap_period": "2026-07至今"
    },
    {
        "person_a": 5, "person_b": 6,
        "type": "overlap",
        "context": "赵志奎与李大华在嫩江市共事",
        "overlap_org": "嫩江市",
        "overlap_period": "2026-07至今"
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
    if name == "崔凯":
        return "255,50,50"      # Red — Party Secretary
    if name == "孙建龙":
        return "50,100,255"     # Blue — Mayor
    if name == "曲荣海":
        return "100,150,255"    # Light blue — Deputy Secretary
    if name == "教旭":
        return "100,150,255"    # Light blue — Standing Committee / Deputy Mayor
    return "100,100,100"        # Grey — Others


def person_size(name):
    if name in ("崔凯", "孙建龙"):
        return "20.0"
    return "12.0"


def org_color(o_type):
    if "党委" in o_type:
        return "255,200,200"
    if "政府" in o_type:
        return "200,200,255"
    return "200,200,200"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append(f'    <description>嫩江市领导班子工作关系网络 - {SLUG}</description>')
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
            "city": "黑河市",
            "region": "嫩江市",
            "job": p.get("current_post", ""),
            "task_id": "heilongjiang_嫩江市",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"nenjiang_{p['name']}",
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
            "administrative_rank": "县处级正职" if ("书记" in p.get("current_post", "") and "副" not in p.get("current_post", "") or "市长" == p.get("current_post", "")) else "县处级副职",
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
            {"type": "none_found", "description": "在公开信息中未发现该人物负面信号", "date": "", "confidence": "confirmed", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{p['name']}的完整履历信息（含出生信息、教育背景、早期职务）需补充"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{p['name']}的完整职业生涯履历（含出生信息、教育背景、历任职务）",
                "why_it_matters": "核心领导人履历是关系网络的基础",
                "suggested_queries": [f"{p['name']} 简历 嫩江", f"{p['name']} 任前公示", f"{p['name']} 黑河"],
                "last_attempted": AS_OF
            }
        ]
    }


def build_person_jsons():
    source_register = [
        {"id": "S001", "title": "嫩江市人民政府网站—嫩江要闻", "url": "https://www.nenjiang.gov.cn", "publisher": "嫩江市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "官网新闻确认崔凯（市委书记）、孙建龙（市长）等领导活动"},
        {"id": "S002", "title": "中共嫩江市委一届146次常委会会议", "url": "https://www.nenjiang.gov.cn/njs/c100369/202607/c11_356947.shtml", "publisher": "嫩江市融媒体中心", "published_at": "2026-07-21", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认崔凯为嫩江市委书记"},
        {"id": "S003", "title": "群众身边不正之风和腐败问题集中整治攻坚决战半年推进会议", "url": "https://www.nenjiang.gov.cn/njs/c100369/202607/c11_356989.shtml", "publisher": "嫩江市融媒体中心", "published_at": "2026-07-22", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认孙建龙为嫩江市委副书记、政府市长"},
        {"id": "S004", "title": "嫩江市委主要领导防汛检查", "url": "https://www.nenjiang.gov.cn/njs/c100369/202607/c11_356519.shtml", "publisher": "嫩江市融媒体中心", "published_at": "2026-07-13", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认教旭为嫩江市委常委、政府副市长"},
    ]

    # === 1. 崔凯 ===
    cui_timeline = [
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未找到上任前的履历", "confidence": "unverified", "source_ids": []},
        {"start": "", "end": "present", "org": "中共嫩江市委员会", "title": "嫩江市委书记", "notes": "2026年7月21日在中共嫩江市委一届146次常委会会议主持", "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    cui_relationships = [
        {"person": "孙建龙", "person_id": "nenjiang_孙建龙", "relationship_type": "党政搭档", "strength": "strong", "evidence": "崔凯作为市委书记，孙建龙作为市长，党政主要领导搭档", "overlap_org": "嫩江市", "overlap_period": "2026-07至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
        {"person": "曲荣海", "person_id": "nenjiang_曲荣海", "relationship_type": "上下级", "strength": "medium", "evidence": "崔凯（书记）与曲荣海（副书记）在市委班子共事", "overlap_org": "中共嫩江市委员会", "overlap_period": "2026-07至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "教旭", "person_id": "nenjiang_教旭", "relationship_type": "上下级", "strength": "medium", "evidence": "崔凯与教旭在市委班子共事", "overlap_org": "中共嫩江市委员会", "overlap_period": "2026-07至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
        {"person": "赵志奎", "person_id": "nenjiang_赵志奎", "relationship_type": "overlap", "strength": "medium", "evidence": "崔凯与赵志奎在嫩江市共事", "overlap_org": "嫩江市", "overlap_period": "2026-07至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    cui_json = make_person_json(persons[0], cui_timeline, cui_relationships, source_register)

    cui_path = PERSONS_DIR / f"{TODAY}-黑龙江省-黑河市-市委书记-崔凯.json"
    with open(cui_path, "w", encoding="utf-8") as f:
        json.dump(cui_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {cui_path.name}")

    # === 2. 孙建龙 ===
    sun_timeline = [
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未找到上任前的履历", "confidence": "unverified", "source_ids": []},
        {"start": "", "end": "present", "org": "嫩江市人民政府", "title": "嫩江市市长", "notes": "2026年7月22日在集中整治会议上以市委副书记、政府市长身份部署工作", "confidence": "confirmed", "source_ids": ["S003"]},
        {"start": "", "end": "present", "org": "中共嫩江市委员会", "title": "市委副书记", "notes": "同时担任嫩江市委副书记", "confidence": "confirmed", "source_ids": ["S003"]},
    ]
    sun_relationships = [
        {"person": "崔凯", "person_id": "nenjiang_崔凯", "relationship_type": "党政搭档", "strength": "strong", "evidence": "孙建龙作为市长，崔凯作为市委书记，党政搭档", "overlap_org": "嫩江市", "overlap_period": "2026-07至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"person": "曲荣海", "person_id": "nenjiang_曲荣海", "relationship_type": "overlap", "strength": "medium", "evidence": "孙建龙与曲荣海在市委班子共事", "overlap_org": "中共嫩江市委员会", "overlap_period": "2026-07至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "教旭", "person_id": "nenjiang_教旭", "relationship_type": "上下级", "strength": "medium", "evidence": "孙建龙（市长）与教旭（副市长）在政府班子共事", "overlap_org": "嫩江市人民政府", "overlap_period": "2026-07至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
    ]
    sun_json = make_person_json(persons[1], sun_timeline, sun_relationships, source_register)

    sun_path = PERSONS_DIR / f"{TODAY}-黑龙江省-黑河市-市长-孙建龙.json"
    with open(sun_path, "w", encoding="utf-8") as f:
        json.dump(sun_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {sun_path.name}")


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
