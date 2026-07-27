#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 东昌区 (Dongchang District), 通化市, 吉林省.

Investigation date: 2026-07-25
Task ID: jilin_东昌区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - dongchang.gov.cn — 东昌区人民政府官方网站（无法访问：HTTPS/HTTP均超时）
  - tonghua.gov.cn — 通化市人民政府官方网站（无法访问：HTTPS超时）
  - Baidu Baike — 返回403
  - Exa search — rate limited
  - Jina Reader — request timeout on Chinese government sites
  - Bing/Google — timeout

Confidence notes:
  - 本任务在web完全不可用的情况下完成（dongchang.gov.cn超时、搜索引擎全部不可达）
  - 由于web访问全面退化，无法确认当前区委书记和区长的姓名
  - 所有核心人物信息标记为"unverified"，放在open_questions中
  - 这是partial-evidence artifact mode产物，标记了明确的 uncertainty
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "东昌区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

# ── Persons ─────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership — NAMES UNKNOWN (web access completely degraded)
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 1,
        "name": "待查_东昌区委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共东昌区委员会",
        "source": "web不可用 - 预计dongchang.gov.cn/ldzc/可查"
    },
    {
        "id": 2,
        "name": "待查_东昌区区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "东昌区人民政府",
        "source": "web不可用 - 预计dongchang.gov.cn/ldzc/可查"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共东昌区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共通化市委员会",
        "location": "通化市东昌区"
    },
    {
        "id": 2,
        "name": "东昌区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "通化市人民政府",
        "location": "通化市东昌区"
    },
    {
        "id": 3,
        "name": "东昌区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "通化市人民代表大会常务委员会",
        "location": "通化市东昌区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议东昌区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "中国人民政治协商会议通化市委员会",
        "location": "通化市东昌区"
    },
    {
        "id": 5,
        "name": "中共东昌区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共通化市纪律检查委员会",
        "location": "通化市东昌区"
    },
]

# ── Positions ──────────────────────────────────────────────────────────────

positions = [
    # 区委书记 — 姓名未知
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": "当前在任——姓名和具体任职时间待查"},

    # 区长 — 姓名未知
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": "当前在任——姓名和具体任职时间待查"},
]

# ── Relationships ──────────────────────────────────────────────────────────

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "区委书记与区长作为党政主要领导搭档，共同主持东昌区全面工作",
        "overlap_org": "东昌区",
        "overlap_period": "截至2026年7月"
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
    if "区委书记" in name or "书记" in name:
        return "255,50,50"
    # Government leader — Blue
    if "区长" in name:
        return "50,100,255"
    return "100,100,100"


def person_size(name):
    if "书记" in name or "区长" in name:
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
    return "200,200,200"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append(f'    <description>东昌区领导班子工作关系网络 - {SLUG} (partial-evidence mode - web degraded)</description>')
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
            "province": "吉林省",
            "city": "通化市",
            "region": "东昌区",
            "job": p.get("current_post", ""),
            "task_id": "jilin_东昌区",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"dongchang_{p['name']}",
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
            "administrative_rank": "正处级",
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
            {"type": "none_found", "description": "公开信息未发现该人物负面信号（但所有web搜索均受阻）", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": f"{p['name']}: 包括姓名在内的所有基本信息完全未知（web全面不可用）"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{p['name']}的真实姓名、出生年月、籍贯、教育背景、完整履历",
                "why_it_matters": "核心目标人物之一，但所有信息完全空白",
                "suggested_queries": [
                    f"东昌区 {p['current_post']} 姓名",
                    f"东昌区 领导 简历",
                    f"东昌区 领导班子"
                ],
                "last_attempted": AS_OF
            }
        ]
    }


def build_person_jsons():
    source_register = [
        {"id": "S001", "title": "东昌区人民政府官方网站", "url": "https://www.dongchang.gov.cn/",
         "publisher": "东昌区人民政府", "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "low",
         "notes": "网站完全无法访问（HTTPS/HTTP均超时）——预计ldzc/路径可查领导信息"},
        {"id": "S002", "title": "通化市人民政府官方网站", "url": "https://www.tonghua.gov.cn/",
         "publisher": "通化市人民政府", "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "low",
         "notes": "网站完全无法访问（HTTPS超时）"},
    ]

    # === 1. 待查_东昌区委书记 ===
    sec_timeline = [
        {"start": "unknown", "end": "unknown", "org": "中共东昌区委员会", "title": "区委书记",
         "notes": "当前在任——姓名和具体任职时间因web不可用而未知", "confidence": "unverified", "source_ids": []},
    ]
    sec_relationships = [
        {"person": "待查_东昌区区长", "person_id": "dongchang_待查_东昌区区长",
         "relationship_type": "overlap", "strength": "strong",
         "evidence": "区委书记与区长作为党政主要领导搭档",
         "overlap_org": "东昌区", "overlap_period": "截至2026年7月",
         "direction": "undirected", "confidence": "unverified", "source_ids": []},
    ]
    sec_json = make_person_json(persons[0], sec_timeline, sec_relationships, source_register)
    sec_json["confidence_summary"]["identity"] = "unverified"
    sec_json["confidence_summary"]["current_role"] = "unverified"

    sec_path = PERSONS_DIR / f"{TODAY}-吉林省-通化市-区委书记-待查.json"
    with open(sec_path, "w", encoding="utf-8") as f:
        json.dump(sec_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {sec_path.name}")

    # === 2. 待查_东昌区区长 ===
    mayor_timeline = [
        {"start": "unknown", "end": "unknown", "org": "东昌区人民政府", "title": "区长",
         "notes": "当前在任——姓名和具体任职时间因web不可用而未知", "confidence": "unverified", "source_ids": []},
    ]
    mayor_relationships = [
        {"person": "待查_东昌区委书记", "person_id": "dongchang_待查_东昌区委书记",
         "relationship_type": "subordinate_to_superior", "strength": "strong",
         "evidence": "区长受区委书记领导",
         "overlap_org": "东昌区", "overlap_period": "截至2026年7月",
         "direction": "undirected", "confidence": "unverified", "source_ids": []},
    ]
    mayor_json = make_person_json(persons[1], mayor_timeline, mayor_relationships, source_register)
    mayor_json["confidence_summary"]["identity"] = "unverified"
    mayor_json["confidence_summary"]["current_role"] = "unverified"

    mayor_path = PERSONS_DIR / f"{TODAY}-吉林省-通化市-区长-待查.json"
    with open(mayor_path, "w", encoding="utf-8") as f:
        json.dump(mayor_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {mayor_path.name}")


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
