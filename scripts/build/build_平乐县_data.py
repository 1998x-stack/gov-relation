#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
平乐县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 广西壮族自治区
Parent City: 桂林市
Region: 平乐县
Targets: 县委书记 & 县长

当前在任 (as of 2026-07-22):
- 县委书记: 周政英 (confirmed via 全州县时期的人物调查)
- 县长: 待查 (网络访问受限，无法确认)

数据来源:
- 周政英: previous person JSON from 全州县 task (media source, plausible)
- 县长及常委班子: 因政府网站 (www.pingle.gov.cn) 超时、Exa 限流、百度 403，
  无法获取当前官方领导名单。需后续恢复网络后补充。

注意:
- 本脚本数据基于有限公开资料搜集。由于网络访问完全受限，
  大部分数据标记为 unverified，需后续核实补充。
- 周政英的平乐县委书记信息来自之前全州县任务中的人物档案，
  但其到任时间和详细履历仍需确认。
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "平乐县"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-22"
TODAY = AS_OF

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：县委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "周政英",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "平乐县委书记",
        "current_org": "中共平乐县委员会",
        "source": "plausible — 来自全州时期人物档案(163.com/dy 网易号/探秘桂北 2025-01-17)",
    },
    # ════════════════════════════════════════
    # 核心领导：县长（待查）
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平乐县委副书记、县长",
        "current_org": "平乐县人民政府",
        "source": "unverified — 政府网站超时，无法获取当前县长信息",
    },
    # ════════════════════════════════════════
    # 县人大常委会主任（待查）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平乐县人大常委会主任",
        "current_org": "平乐县人大常委会",
        "source": "unverified — 需通过政府官网确认",
    },
    # ════════════════════════════════════════
    # 县政协主席（待查）
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平乐县政协主席",
        "current_org": "平乐县政协",
        "source": "unverified — 需通过政府官网确认",
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共平乐县委员会", "type": "党委", "level": "县", "location": "平乐县"},
    {"id": 2, "name": "平乐县人民政府", "type": "政府", "level": "县", "location": "平乐县"},
    {"id": 3, "name": "平乐县人大常委会", "type": "人大", "level": "县", "location": "平乐县"},
    {"id": 4, "name": "平乐县政协", "type": "政协", "level": "县", "location": "平乐县"},
    {"id": 5, "name": "中共平乐县纪律检查委员会", "type": "党委", "level": "县", "location": "平乐县"},
    {"id": 6, "name": "中共平乐县委员会组织部", "type": "党委", "level": "县", "location": "平乐县"},
    {"id": 7, "name": "中共平乐县委员会宣传部", "type": "党委", "level": "县", "location": "平乐县"},
    {"id": 8, "name": "中共平乐县委员会统战部", "type": "党委", "level": "县", "location": "平乐县"},
    {"id": 9, "name": "中共平乐县委员会政法委员会", "type": "党委", "level": "县", "location": "平乐县"},
    {"id": 10, "name": "中共平乐县委员会办公室", "type": "党委", "level": "县", "location": "平乐县"},
    {"id": 11, "name": "中共桂林市委员会", "type": "党委", "level": "地级市", "location": "桂林市"},
    {"id": 12, "name": "桂林市人民政府", "type": "政府", "level": "地级市", "location": "桂林市"},
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 核心领导
    {"person_id": 1, "org_id": 1, "title": "平乐县委书记", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "平乐县委副书记", "start": "待查", "end": "present", "rank": "正处级", "note": "姓名待查"},
    {"person_id": 2, "org_id": 2, "title": "平乐县县长", "start": "待查", "end": "present", "rank": "正处级", "note": "姓名待查"},
    # 人大政协
    {"person_id": 3, "org_id": 3, "title": "平乐县人大常委会主任", "start": "待查", "end": "present", "rank": "正处级", "note": "姓名待查"},
    {"person_id": 4, "org_id": 4, "title": "平乐县政协主席", "start": "待查", "end": "present", "rank": "正处级", "note": "姓名待查"},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 党政主要领导
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "周政英（县委书记）与待查县长为平乐县党政主要搭档", "overlap_org": "平乐县党政班子", "overlap_period": ""},
    # 人大与党委
    {"person_a": 1, "person_b": 3, "type": "党政/人大关系", "context": "周政英（县委书记）与待查人大主任为县四家班子主要领导", "overlap_org": "平乐县四家班子", "overlap_period": ""},
    # 政协与党委
    {"person_a": 1, "person_b": 4, "type": "党政/政协关系", "context": "周政英（县委书记）与待查政协主席为县四家班子主要领导", "overlap_org": "平乐县四家班子", "overlap_period": ""},
    # 政府与人大
    {"person_a": 2, "person_b": 3, "type": "监督与被监督", "context": "待查县长与待查人大主任为政府与人大关系", "overlap_org": "平乐县四家班子", "overlap_period": ""},
    # 政府与政协
    {"person_a": 2, "person_b": 4, "type": "协商关系", "context": "待查县长与待查政协主席为政府与政协关系", "overlap_org": "平乐县四家班子", "overlap_period": ""},
]

# =========================================================================
# 5. DATABASE
# =========================================================================
def create_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)
    # Insert persons
    for p in persons:
        cur.execute("""INSERT OR REPLACE INTO persons
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p.get("gender",""), p.get("ethnicity",""),
             p.get("birth",""), p.get("birthplace",""), p.get("education",""),
             p.get("party_join",""), p.get("work_start",""),
             p["current_post"], p["current_org"], p.get("source","")))
    # Insert organizations
    for o in organizations:
        cur.execute("""INSERT OR REPLACE INTO organizations
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"],
             o.get("parent",""), o.get("location","")))
    # Insert positions
    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos.get("start",""), pos.get("end",""),
             pos.get("rank",""), pos.get("note","")))
    # Insert relationships
    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"],
             r["context"], r.get("overlap_org",""), r.get("overlap_period","")))
    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

# =========================================================================
# 6. GEXF
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    """Return r,g,b string based on role."""
    post = p.get("current_post","")
    if "书记" in post and "纪委" not in post and "县委" in post:
        return "255,50,50"  # red for party secretary
    elif "县长" in post or "副县长" in post or "常务" in post:
        return "50,100,255"  # blue for government
    elif "纪委" in post or "监委" in post:
        return "255,165,0"  # orange for discipline
    else:
        return "100,100,100"  # grey for others

def org_color(o):
    t = o.get("type","")
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")

def is_top_leader(p):
    return p["id"] in (1, 2)

def create_gexf():
    now = datetime.now().strftime("%Y-%m-%d")
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{now}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>平乐县领导班子工作关系网络 — 广西壮族自治区桂林市平乐县</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    # Attributes: node
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="birth" type="string"/>')
    lines.append('      <attribute id="3" title="source" type="string"/>')
    lines.append('    </attributes>')
    # Attributes: edge
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')
    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # Nodes: organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person->Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}在{esc(pos.get("start",""))}-{esc(pos.get("end",""))}任职"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    # Person<->Person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF graph created: {GEXF_PATH}")

# =========================================================================
# 7. PERSON JSON FILES
# =========================================================================
def write_person_json(person, relationships_for_person):
    """Write a deep person graph JSON file."""
    person_id = f"pingle_{person['name']}"
    # Build filename from current_post
    post_short = person['current_post'].replace('平乐','')
    filename = f"{TODAY}-广西壮族自治区-桂林市-{post_short}-{person['name']}.json"
    filepath = os.path.join(PERSONS_DIR, filename)

    rels_out = []
    for r in relationships_for_person:
        other_id = r["person_b"] if r["person_a"] == person["id"] else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        rels_out.append({
            "person": other["name"] if other else "未知",
            "person_id": f"pingle_{other['name']}" if other else "unknown",
            "relationship_type": r["type"],
            "strength": "weak",
            "evidence": r["context"],
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "unverified",
            "source_ids": []
        })

    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "桂林市",
            "region": "平乐县",
            "job": person["current_post"],
            "task_id": "guangxi_平乐县",
            "time_focus": "当前任期"
        },
        "identity": {
            "person_id": person_id,
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", "待查"),
            "birthplace": person.get("birthplace", "待查"),
            "native_place": "",
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", "待查"),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_待查",
                "name_birthplace": f"{person['name']}_待查",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if person["id"] in (1,2,3,4) else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": []
        },
        "career_timeline": [
            {
                "start": "待查",
                "end": "present",
                "org": person["current_org"],
                "title": person["current_post"],
                "level": "正处级" if person["id"] in (1,2,3,4) else "副处级",
                "location": "平乐县",
                "system": "party" if "委" in person["current_org"] else "government",
                "rank": "",
                "is_key_promotion": False,
                "notes": "需通过网络搜索补充完整履历",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "organizations": [],
        "relationships": rels_out,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "待查",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "由于网络访问受限，未获取到公开风格信息。需后续补充。"
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "因网络访问受限，未搜索到负面信息。不代表无风险。",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "探秘桂北 — 梁德锋简历/吕佳军简历",
                "url": "https://www.163.com/dy/article/JM2IVMEO0523L7A8.html",
                "publisher": "网易号/探秘桂北",
                "published_at": "2025-01-17",
                "accessed_at": AS_OF,
                "source_type": "media",
                "reliability": "medium",
                "notes": "周政英的基本信息和曾任全州县长信息"
            }
        ],
        "confidence_summary": {
            "identity": "unverified" if person["name"] == "待查" else "plausible",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "所有履历信息均待补充" if person["name"] == "待查" else "完整履历待补充"
        },
        "open_questions": []
    }

    # Add specific open questions for known person
    if person["id"] == 1:
        data["open_questions"] = [
            {
                "priority": "critical",
                "question": "周政英的完整履历（出生年月、籍贯、教育背景、历任职务）",
                "why_it_matters": "核心领导的基础信息，是评估其政治晋升路径和关系网络的基础",
                "suggested_queries": [
                    "周政英 简历 平乐",
                    "周政英 任前公示 桂林",
                    "周政英 百度百科"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": "周政英调任平乐县委书记的具体时间",
                "why_it_matters": "了解领导过渡模式，有助于追溯前任书记去向",
                "suggested_queries": [
                    "平乐县委书记 任免",
                    "周政英 平乐县委书记 任职"
                ],
                "last_attempted": AS_OF
            }
        ]
    elif person["name"] == "待查":
        data["open_questions"] = [
            {
                "priority": "critical",
                "question": f"平乐县{post_short}的姓名和完整履历",
                "why_it_matters": "核心领导的姓名是构建关系网络的基础",
                "suggested_queries": [
                    "平乐县 人民政府 领导",
                    "平乐县 县长",
                    "平乐县 领导分工"
                ],
                "last_attempted": AS_OF
            }
        ]

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Person JSON created: {filepath}")
    return filepath

# =========================================================================
# 8. MAIN
# =========================================================================
def main():
    print("=" * 60)
    print(f"平乐县领导班子工作关系网络 — 数据构建")
    print(f"As of: {AS_OF}")
    print("=" * 60)
    print()

    # Create DB
    create_db()
    print()

    # Create GEXF
    create_gexf()
    print()

    # Create person JSON files for core leaders
    core_ids = [1, 2]  # 县委书记 & 县长
    written = []
    for pid in core_ids:
        person = next((p for p in persons if p["id"] == pid), None)
        if person:
            rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
            path = write_person_json(person, rels)
            written.append(path)

    print()
    print("=" * 60)
    print("构建完成！")
    print(f"数据库: {DB_PATH}")
    print(f"GEXF图: {GEXF_PATH}")
    print(f"人物JSON: {len(written)} files")
    for w in written:
        print(f"  - {w}")
    print("=" * 60)
    print()
    print("⚠ 注意：所有数据均为 unverified 级别。")
    print("  由于网络访问受限，需后续通过官方网站核实。")
    print("  建议访问:")
    print("  - https://www.pingle.gov.cn/ldzc/")
    print("  - https://www.pingle.gov.cn/zwgk/ldzc/")
    print()
    print("  已知信息:")
    print("  - 县委书记: 周政英（女，原全州县长，后调任平乐县委书记）")
    print("  - 县长: 待查")
    print("  - 县委常委会成员全部待查")

if __name__ == "__main__":
    main()
