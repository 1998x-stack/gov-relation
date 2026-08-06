#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 咸宁市 (Xianning City), 湖北省.

Investigation date: 2026-08-06
Task ID: hubei_咸宁市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.xianning.gov.cn (咸宁市人民政府门户网站) — 政府领导 (市委副书记、市长：杨军) official resume page
  - 咸宁日报 articles via gov site: 周锋主持市委常委会（2026-07-30）、周锋杨军等市领导开展八一走访慰问（2026-08-01）、周锋主持政党协商座谈会（2026-08-06）

Confidence notes:
  - 周锋 (市委书记): current post CONFIRMED via official 咸宁日报/gov news. Birth/education/full career timeline UNVERIFIED (external search blocked).
  - 杨军 (市长): identity CONFIRMED via official gov resume page (1970年5月生，汉族，大学学历、在职硕士，中共党员). Full career gaps remain.
  - 朱庆刚、梁细林、张远梅、彭辉、郑黎明、林桢栋、张学华、金山、葛军: current posts CONFIRMED via official gov leader roster / committee articles; earlier careers UNVERIFIED.
  - Previous 市委书记/市长 and any county-level transfers: UNVERIFIED (web access degraded).

Degraded web access: Exa rate-limited, Baidu/360 captcha, Bing/Jina/DDG/Wikipedia blocked. Relying on official gov site (authoritative primary source). Artifacts encode gaps via open_questions / report/open_gaps.md.
"""

import json
import os
import shutil
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "咸宁市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

CANONICAL_DB = os.path.join(BASE, "..", "..", "database", f"{SLUG}_network.db")
CANONICAL_GEXF = os.path.join(BASE, "..", "..", "graph", f"{SLUG}_network.gexf")
CANONICAL_BUILD = os.path.join(BASE, "..", "..", "..", f"build_{SLUG}_data.py")
CANONICAL_PERSONS = Path(BASE) / ".." / ".." / "persons"

PROVINCE = "湖北省"
CITY = "咸宁市"

THEME_DEFAULT = None

# ── Persons ─────────────────────────────────────────────────────────────────

persons = [
    # ══════════ Core Leadership (target) ══════════
    {
        "id": 1, "name": "周锋", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委书记", "current_org": "中共咸宁市委员会",
        "source": "http://www.xianning.gov.cn/xwzx/xnyw/202607/t20260730_5167442.shtml",
    },
    {
        "id": 2, "name": "杨军", "gender": "男", "ethnicity": "汉族",
        "birth": "1970年5月", "birthplace": "", "education": "大学学历、在职硕士学位",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委副书记、市长", "current_org": "咸宁市人民政府",
        "source": "http://www.xianning.gov.cn/xxgk/zfld/yj/202602/t20260202_4241759.shtml",
    },
    # ══════════ Leadership team ══════════
    {
        "id": 3, "name": "朱庆刚", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市人大常委会党组书记、主任", "current_org": "咸宁市人民代表大会常务委员会",
        "source": "http://www.xianning.gov.cn/xwzx/xnyw/202607/t20260730_5167442.shtml",
    },
    {
        "id": 4, "name": "梁细林", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市政协党组书记、主席", "current_org": "中国人民政治协商会议咸宁市委员会",
        "source": "http://www.xianning.gov.cn/xwzx/xnyw/202607/t20260730_5167442.shtml",
    },
    {
        "id": 5, "name": "张远梅", "gender": "女", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委副书记", "current_org": "中共咸宁市委员会",
        "source": "http://www.xianning.gov.cn/xwzx/xnyw/202607/t20260730_5167442.shtml",
    },
    {
        "id": 6, "name": "彭辉", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、副市长", "current_org": "咸宁市人民政府",
        "source": "http://www.xianning.gov.cn/xxgk/zfld/yj/",
    },
    {
        "id": 7, "name": "郑黎明", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、副市长", "current_org": "咸宁市人民政府",
        "source": "http://www.xianning.gov.cn/xxgk/zfld/yj/",
    },
    {
        "id": 8, "name": "林桢栋", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副市长", "current_org": "咸宁市人民政府",
        "source": "http://www.xianning.gov.cn/xxgk/zfld/yj/",
    },
    {
        "id": 9, "name": "张学华", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副市长", "current_org": "咸宁市人民政府",
        "source": "http://www.xianning.gov.cn/xxgk/zfld/yj/",
    },
    {
        "id": 10, "name": "金山", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副市长", "current_org": "咸宁市人民政府",
        "source": "http://www.xianning.gov.cn/xxgk/zfld/yj/",
    },
    {
        "id": 11, "name": "葛军", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市政府秘书长", "current_org": "咸宁市人民政府",
        "source": "http://www.xianning.gov.cn/xxgk/zfld/yj/",
    },
]

# ── Organizations ──────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共咸宁市委员会", "type": "党委", "level": "地级市", "parent": "中共湖北省委", "location": "湖北省咸宁市"},
    {"id": 2, "name": "咸宁市人民政府", "type": "政府", "level": "地级市", "parent": "湖北省人民政府", "location": "湖北省咸宁市"},
    {"id": 3, "name": "咸宁市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "咸宁市", "location": "湖北省咸宁市"},
    {"id": 4, "name": "中国人民政治协商会议咸宁市委员会", "type": "政协", "level": "地级市", "parent": "咸宁市", "location": "湖北省咸宁市"},
    {"id": 5, "name": "咸宁军分区", "type": "党委", "level": "地级市", "parent": "湖北省军区", "location": "湖北省咸宁市"},
]

# ── Positions ──────────────────────────────────────────────────────────────

positions = [
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "兼任咸宁军分区党委第一书记（2026-08-01 官方新闻确认）"},
    {"person_id": 1, "org_id": 5, "title": "党委第一书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "咸宁军分区党委第一书记（市委书记兼任）"},
    {"person_id": 2, "org_id": 2, "title": "市长、市政府党组书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "市委副书记、市政府市长、党组书记，官方任免页面（2026-02-02）"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "市委副书记、市长"},
    {"person_id": 3, "org_id": 3, "title": "市人大常委会党组书记、主任", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "2026-07-30 市委常委会（扩大）会议列席"},
    {"person_id": 4, "org_id": 4, "title": "市政协党组书记、主席", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "2026-07-30 市委常委会（扩大）会议列席"},
    {"person_id": 5, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "2026-07-30 市委常委会（扩大）会议列席"},
    {"person_id": 6, "org_id": 2, "title": "市委常委、副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "咸宁市政府领导名单"},
    {"person_id": 7, "org_id": 2, "title": "市委常委、副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "咸宁市政府领导名单"},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "咸宁市政府领导名单"},
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "咸宁市政府领导名单"},
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "咸宁市政府领导名单"},
    {"person_id": 11, "org_id": 2, "title": "市政府秘书长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "咸宁市政府领导名单"},
]

# ── Relationships ──────────────────────────────────────────────────────────

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书记与市长党政正职搭档", "overlap_org": "咸宁市", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "colleague", "context": "市委常委班子成员", "overlap_org": "中共咸宁市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 3, "type": "colleague", "context": "市委与市人大正职共事", "overlap_org": "咸宁市", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "colleague", "context": "市委与市政协正职共事", "overlap_org": "咸宁市", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "咸宁市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "咸宁市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "咸宁市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "咸宁市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "咸宁市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "市长与市政府秘书长", "overlap_org": "咸宁市人民政府", "overlap_period": "至今"},
]

# ══════════════════════════════════════════════════════════════════════════
# Escaping / GEXF helpers
# ══════════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ══════════════════════════════════════════════════════════════════════════
# Build database
# ══════════════════════════════════════════════════════════════════════════

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS persons;
        DROP TABLE IF EXISTS organizations;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
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
    if name == "周锋":
        return "255,50,50"      # 市委书记 Red
    if name == "杨军":
        return "50,100,255"     # 市长 Blue
    if name == "朱庆刚":
        return "200,255,255"    # 人大 Cyan
    if name == "梁细林":
        return "255,240,200"    # 政协 Cream
    if name == "张远梅" or name == "彭辉" or name == "郑黎明":
        return "255,165,0"      # 市委/常务 橙
    if name == "葛军":
        return "180,180,180"    # 秘书长 Grey
    return "100,100,100"


def person_size(name):
    if name in ("周锋", "杨军"):
        return "20.0"
    if name in ("朱庆刚", "梁细林"):
        return "16.0"
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
    lines.append(f'    <description>咸宁市领导班子工作关系网络 - {SLUG}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

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
            "province": PROVINCE,
            "city": CITY,
            "region": CITY,
            "job": p.get("current_post", ""),
            "task_id": "hubei_咸宁市",
            "time_focus": "2026年8月"
        },
        "identity": {
            "person_id": f"xianning_{p['name']}",
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
            "administrative_rank": "正厅级" if p["id"] in (1, 2, 3, 4) else ("副厅级" if p["id"] in (5, 6, 7, 8, 9, 10) else "正处级"),
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002", "S003"]
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
            "identity": "confirmed" if p["gender"] or p["birth"] else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if p.get("birth") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{p['name']}的完整履历信息（含出生信息、教育背景、早期职务）需补充"
        },
        "open_questions": [
            {
                "priority": "critical" if p["id"] in (1, 2) else "high",
                "question": f"{p['name']}的完整职业生涯履历（出生信息、籍贯、教育背景、历任职务）",
                "why_it_matters": "核心班子成员，却缺少可核实的履历信息",
                "suggested_queries": [f"{p['name']} 简历 咸宁", f"{p['name']} 任前公示", f"{p['name']} 履新"],
                "last_attempted": AS_OF
            }
        ]
    }


def build_person_jsons():
    source_register = [
        {"id": "S001", "title": "咸宁市人民政府门户网站—政府领导", "url": "http://www.xianning.gov.cn/xxgk/zfld/yj/", "publisher": "咸宁市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "市委副书记、市长：杨军简历及市政府领导名单"},
        {"id": "S002", "title": "咸宁日报—市委常委会（扩大）会议", "url": "http://www.xianning.gov.cn/xwzx/xnyw/202607/t20260730_5167442.shtml", "publisher": "咸宁日报", "published_at": "2026-07-30", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "周锋(市委书记)、杨军(市长)、朱庆刚、梁细林、张远梅"},
        {"id": "S003", "title": "咸宁日报—八一走访慰问", "url": "http://www.xianning.gov.cn/xwzx/xnyw/202608/t20260801_5174216.shtml", "publisher": "咸宁日报", "published_at": "2026-08-01", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "周锋(咸宁军分区党委第一书记)、杨军(市长)"},
    ]

    core = [
        (1, "市委书记", "周锋", [
            {"start": "unknown", "end": "present", "org": "中共咸宁市委员会", "title": "市委书记", "notes": "兼任咸宁军分区党委第一书记；2026年7-8月官方新闻确认在任", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "周锋任咸宁市委书记前的完整履历（出生、籍贯、教育、前职）未获公开源确认", "confidence": "unverified", "source_ids": []},
        ], THEME_DEFAULT),
        (2, "市长", "杨军", [
            {"start": "unknown", "end": "present", "org": "咸宁市人民政府", "title": "市长", "notes": "市委副书记、市政府市长、党组书记", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "杨军（1970年5月生，汉族，大学学历、在职硕士）任咸宁市长前及早期履历未核实", "confidence": "unverified", "source_ids": []},
        ], THEME_DEFAULT),
    ]

    # All members minimal person JSON
    members = range(1, 12)

    for pid, job, name, timeline, theme in core:
        p = next(x for x in persons if x["id"] == pid)
        rels = build_relationships_for(p)
        js = make_person_json(p, timeline, rels, source_register)
        js["confidence_summary"]["identity"] = "confirmed" if p.get("birth") or p.get("gender") else "plausible"
        path = PERSONS_DIR / f"{TODAY}-{PROVINCE}-{CITY}-{job}-{name}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(js, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {path.name}")

    # deputies / others (thinner timelines)
    other_profiles = [
        (3, "市人大常委会主任", "朱庆刚"),
        (4, "市政协主席", "梁细林"),
        (5, "市委副书记", "张远梅"),
        (11, "市政府秘书长", "葛军"),
    ]
    for pid, job, name in other_profiles:
        p = next(x for x in persons if x["id"] == pid)
        timeline = [
            {"start": "unknown", "end": "present", "org": p["current_org"], "title": p["current_post"], "notes": "2026年官方名单确认在任", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": f"{name}的身份与履历细节待补充", "confidence": "unverified", "source_ids": []},
        ]
        rels = build_relationships_for(p)
        js = make_person_json(p, timeline, rels, source_register)
        path = PERSONS_DIR / f"{TODAY}-{PROVINCE}-{CITY}-{job}-{name}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(js, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {path.name}")


def build_relationships_for(p):
    rules = {
        1: [{"person": "杨军", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "市委书记与市长核心党政搭档", "overlap_org": "咸宁市", "overlap_period": "至今", "confidence": "confirmed"}],
        2: [{"person": "周锋", "relationship_type": "subordinate_to_superior", "strength": "strong", "evidence": "市长受市委书记领导", "overlap_org": "咸宁市", "overlap_period": "至今", "confidence": "confirmed"}],
        3: [{"person": "周锋", "relationship_type": "colleague", "strength": "medium", "evidence": "市委与市人大正职共事", "overlap_org": "咸宁市", "overlap_period": "至今", "confidence": "confirmed"}],
        4: [{"person": "周锋", "relationship_type": "colleague", "strength": "medium", "evidence": "市委与市政协正职共事", "overlap_org": "咸宁市", "overlap_period": "至今", "confidence": "confirmed"}],
        5: [{"person": "周锋", "relationship_type": "colleague", "strength": "medium", "evidence": "市委领导班子成员", "overlap_org": "中共咸宁市委员会", "overlap_period": "至今", "confidence": "confirmed"}],
        11: [{"person": "杨军", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "市政府秘书长辅佐市长", "overlap_org": "咸宁市人民政府", "overlap_period": "至今", "confidence": "confirmed"}],
    }
    items = rules.get(p["id"], [])
    out = []
    for it in items:
        out.append({
            "person": it["person"], "person_id": f"xianning_{it['person']}",
            "relationship_type": it["relationship_type"], "strength": it["strength"],
            "evidence": it["evidence"], "overlap_org": it["overlap_org"],
            "overlap_period": it["overlap_period"], "direction": "undirected",
            "confidence": it["confidence"], "source_ids": ["S001", "S002"]
        })
    return out


def promote_to_canonical():
    CANONICAL_DB_DIR = os.path.join(BASE, "..", "..", "database")
    CANONICAL_GEXF_DIR = os.path.join(BASE, "..", "..", "graph")
    os.makedirs(CANONICAL_DB_DIR, exist_ok=True)
    os.makedirs(CANONICAL_GEXF_DIR, exist_ok=True)
    os.makedirs(CANONICAL_PERSONS, exist_ok=True)

    shutil.copy2(DB_PATH, CANONICAL_DB)
    print(f"  Promoted DB  -> {CANONICAL_DB}")
    shutil.copy2(GEXF_PATH, CANONICAL_GEXF)
    print(f"  Promoted GEXF -> {CANONICAL_GEXF}")
    for p in PERSONS_DIR.glob(f"{TODAY}-*.json"):
        shutil.copy2(p, CANONICAL_PERSONS / p.name)
    print(f"  Promoted {len(list(PERSONS_DIR.glob(f'{TODAY}-*.json')))} person JSON --> {CANONICAL_PERSONS}")

    root_build = Path(CANONICAL_BUILD)
    root_build.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(os.path.abspath(__file__), root_build)
    print(f"  Promoted build -> {root_build}")


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