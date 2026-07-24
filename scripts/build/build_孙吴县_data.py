#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 孙吴县 (Sunwu County), 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_孙吴县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - Wikipedia (zh.wikipedia.org) — 孙吴县 infobox shows 代树奇 as 县委书记
  - www.heihe.gov.cn — 黑河市人民政府网站（间接参考）
  - 孙吴县人民政府网站 (www.sunwu.gov.cn) — 无法直接访问（连接超时）

Confidence notes:
  - 代树奇: confirmed as 县委书记 per Wikipedia (page last modified 2025-05-26), but infobox may lag
  - 县长信息: 未能在公开信息中确认当前县长人选。Wikipedia 孙吴县页面仅列出县委书记，未列出县长
  - Web search tools (Exa, Jina, Baidu) were rate-limited or timed out during this investigation
  - The sunwu.gov.cn official website was unreachable (connection timeout and transport errors)
  - 代树奇の工作履历（含教育背景、历任职务）未能获取详细资料
  - All artifacts are created with explicit uncertainty markers
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "孙吴县"
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

    # 1. 县委书记 — 代树奇
    # Source: Wikipedia 孙吴县 infobox（页面最后修订于2025年5月26日）
    {
        "id": 1,
        "name": "代树奇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共孙吴县委员会",
        "source": "https://zh.wikipedia.org/wiki/孙吴县"
    },
    # 2. 县长 — 待确认
    # 未能通过公开渠道确认当前县长人选
    {
        "id": 2,
        "name": "（县长待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县长（待确认）",
        "current_org": "孙吴县人民政府",
        "source": "公开信息暂缺——sunwu.gov.cn无法访问"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共孙吴县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共黑河市委员会",
        "location": "孙吴县"
    },
    {
        "id": 2,
        "name": "孙吴县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "黑河市人民政府",
        "location": "孙吴县"
    },
    {
        "id": 3,
        "name": "孙吴县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "黑河市人民代表大会常务委员会",
        "location": "孙吴县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议孙吴县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "中国人民政治协商会议黑河市委员会",
        "location": "孙吴县"
    },
    {
        "id": 5,
        "name": "中共黑河市委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中共黑龙江省委员会",
        "location": "黑河市"
    },
    {
        "id": 6,
        "name": "黑河市人民政府",
        "type": "政府",
        "level": "地级",
        "parent": "黑龙江省人民政府",
        "location": "黑河市"
    },
    {
        "id": 7,
        "name": "黑龙江省人民政府",
        "type": "政府",
        "level": "省级",
        "parent": "",
        "location": "哈尔滨市"
    },
    {
        "id": 8,
        "name": "中共黑龙江省委员会",
        "type": "党委",
        "level": "省级",
        "parent": "",
        "location": "哈尔滨市"
    },
]

# ── Positions ──────────────────────────────────────────────────────────────

positions = [
    # 代树奇
    {"person_id": 1, "org_id": 1, "title": "孙吴县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "Wikipedia 孙吴县 infobox（2025年5月版本）显示为县委书记。上任日期和此前履历待查。"},

    # 县长（待确认）
    {"person_id": 2, "org_id": 2, "title": "孙吴县县长（待确认）", "start_date": "", "end_date": "present", "rank": "正处级", "note": "当前县长人选未能在公开渠道确认。"},
]

# ── Relationships ──────────────────────────────────────────────────────────

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "代树奇作为县委书记，与县长党政主要领导搭档（县长人选待确认）",
        "overlap_org": "孙吴县",
        "overlap_period": "（待确认）"
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
    if name == "代树奇":
        return "255,50,50"
    # Government leader — Blue
    if name == "（县长待确认）":
        return "50,100,255"
    # Others — Grey
    return "100,100,100"


def person_size(name):
    if name in ("代树奇",):
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
    lines.append(f'    <description>孙吴县领导班子工作关系网络 - {SLUG}</description>')
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
            "region": "孙吴县",
            "job": p.get("current_post", ""),
            "task_id": "heilongjiang_孙吴县",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"sunwu_{p['name']}",
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
            "is_current_confirmed": True if p["name"] == "代树奇" else False,
            "source_ids": ["S001"]
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
            {"type": "none_found", "description": "在公开信息中未发现该人物负面信号（因信息获取受限，搜索结果可能不完整）", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed" if p["name"] == "代树奇" else "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": f"{p['name']}的完整履历信息（含出生信息、教育背景、历任职务）均需补充"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{p['name']}的完整职业生涯履历（含出生信息、教育背景、历任职务）",
                "why_it_matters": "核心人物履历空白，无法追溯任职路径",
                "suggested_queries": [f"{p['name']} 简历 孙吴", f"{p['name']} 黑河", f"{p['name']} 任前公示"],
                "last_attempted": AS_OF
            }
        ]
    }


def build_person_jsons():
    source_register = [
        {"id": "S001", "title": "维基百科—孙吴县", "url": "https://zh.wikipedia.org/wiki/孙吴县", "publisher": "维基百科", "published_at": "2025-05-26", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "孙吴县infobox显示县委书记为代树奇——未列出县长"},
        {"id": "S002", "title": "孙吴县人民政府网站", "url": "http://www.sunwu.gov.cn", "publisher": "孙吴县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "unknown", "notes": "连接超时，无法获取数据"},
    ]

    # === 1. 代树奇（县委书记） ===
    dai_timeline = [
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "代树奇——孙吴县委书记，但公开资料未找到其出生信息和完整履历。Wikipedia 孙吴县页面（2025年5月版）仅列出其县委书记职务。", "confidence": "unverified", "source_ids": []},
        {"start": "", "end": "present", "org": "中共孙吴县委员会", "title": "孙吴县委书记", "notes": "Wikipedia 孙吴县 infobox 显示为县委书记（页面最后修订于2025年5月26日）", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    dai_relationships = [
        {"person": "（县长待确认）", "person_id": "sunwu_（县长待确认）", "relationship_type": "superior_subordinate", "strength": "weak", "evidence": "县委书记与县长为党政主要领导搭档关系，但县长人选暂未确认", "overlap_org": "孙吴县", "overlap_period": "（待确认）", "direction": "undirected", "confidence": "unverified", "source_ids": []},
    ]
    dai_json = make_person_json(persons[0], dai_timeline, dai_relationships, source_register)
    dai_json["professional_profile"]["career_pattern"] = "unknown"
    dai_json["open_questions"] = [
        {"priority": "critical", "question": "代树奇的完整职业生涯履历（含出生年月、籍贯、教育背景、历任职务、上任时间）", "why_it_matters": "核心人物，但几乎全部信息缺失", "suggested_queries": ["代树奇 简历 孙吴", "代树奇 黑河 任职", "代树奇 任前公示"], "last_attempted": AS_OF},
        {"priority": "high", "question": "代树奇的任职起始时间——何时开始担任孙吴县委书记", "why_it_matters": "无法确定其任期长度和晋升路径", "suggested_queries": ["代树奇 任孙吴县委书记 时间", "孙吴县 代树奇 任命"], "last_attempted": AS_OF},
        {"priority": "medium", "question": "代树奇的前任是谁？前任的去向", "why_it_matters": "无法构建孙吴县委书记职位的人事变动链", "suggested_queries": ["孙吴县 前任县委书记", "孙吴县 县委书记 历任"], "last_attempted": AS_OF},
    ]

    dai_path = PERSONS_DIR / f"{TODAY}-黑龙江省-黑河市-县委书记-代树奇.json"
    with open(dai_path, "w", encoding="utf-8") as f:
        json.dump(dai_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {dai_path.name}")

    # === 2. 县长（待确认） ===
    mayor_timeline = [
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "孙吴县县长人选未能在公开渠道确认。sunwu.gov.cn 网站无法访问；百度百科被403拦截；Exa/Jina 搜索速率受限。", "confidence": "unverified", "source_ids": []},
    ]
    mayor_relationships = [
        {"person": "代树奇", "person_id": "sunwu_代树奇", "relationship_type": "subordinate_to_superior", "strength": "weak", "evidence": "县长受县委书记领导，但县长人选未确认", "overlap_org": "孙吴县", "overlap_period": "（待确认）", "direction": "undirected", "confidence": "unverified", "source_ids": []},
    ]
    mayor_json = make_person_json(persons[1], mayor_timeline, mayor_relationships, source_register)
    mayor_json["open_questions"] = [
        {"priority": "critical", "question": "孙吴县现任县长是谁？其姓名、出生年月、籍贯、教育背景、完整履历", "why_it_matters": "目标人物之一，但连最基本的身份信息都未找到", "suggested_queries": ["孙吴县 县长 2025 2026", "孙吴县人民政府 县长", "孙吴县 领导分工"], "last_attempted": AS_OF},
        {"priority": "high", "question": "孙吴县县长何时上任？前任县长是谁、去向何处？", "why_it_matters": "无法构建县长职位的人事变动链", "suggested_queries": ["孙吴县 县长 任前公示", "孙吴县 人大 任命 县长", "孙吴县 前任县长"], "last_attempted": AS_OF},
    ]

    mayor_path = PERSONS_DIR / f"{TODAY}-黑龙江省-黑河市-县长-待确认.json"
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
