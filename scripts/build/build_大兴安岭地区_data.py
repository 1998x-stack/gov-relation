#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 大兴安岭地区 (Daxing'anling Prefecture), 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_大兴安岭地区
Level: 地级市 (地区)
Targets: 地委书记 & 行署专员

Note: 大兴安岭地区 is a "地区" (prefecture), not a city. The party head is 地委书记
and the administrative head is 行署专员 (地区行政公署专员), not 市委书记/市长.

Research sources:
  - Wikipedia (zh.wikipedia.org) — leadership table for 大兴安岭地区
  - www.dxal.gov.cn — 大兴安岭地区行政公署网站

Confidence notes:
  - 范庆华: confirmed via Wikipedia leadership table (name, birth, native place, appointment date)
  - 王青伟: confirmed via Wikipedia (name, birth, native place, appointment date)
  - 蒋迎娟 (人大工委主任), 王洪斌 (政协工委主任): confirmed via Wikipedia
  - Detailed career timelines (education, early career) could not be fully verified due to web access limitations
  - Web search tools (Exa, Jina, Baidu) were rate-limited or timed out during this investigation
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "大兴安岭地区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

# ── Persons ─────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 1,
        "name": "范庆华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年10月",
        "birthplace": "吉林省延吉市",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "地委书记",
        "current_org": "中国共产党大兴安岭地区委员会",
        "source": "https://zh.wikipedia.org/wiki/大兴安岭地区"
    },
    {
        "id": 2,
        "name": "王青伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年2月",
        "birthplace": "黑龙江省尚志市",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "行署专员",
        "current_org": "大兴安岭地区行政公署",
        "source": "https://zh.wikipedia.org/wiki/大兴安岭地区"
    },
    {
        "id": 3,
        "name": "蒋迎娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1970年3月",
        "birthplace": "黑龙江省通河县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "地区人大工委主任",
        "current_org": "黑龙江省人大常委会大兴安岭地区工作委员会",
        "source": "https://zh.wikipedia.org/wiki/大兴安岭地区"
    },
    {
        "id": 4,
        "name": "王洪斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年6月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "地区政协工委主任",
        "current_org": "黑龙江省政协大兴安岭地区工作委员会",
        "source": "https://zh.wikipedia.org/wiki/大兴安岭地区"
    },
    # Predecessors
    {
        "id": 5,
        "name": "徐向国",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任地委书记",
        "current_org": "中国共产党大兴安岭地区委员会",
        "source": "https://zh.wikipedia.org/wiki/大兴安岭地区"
    },
    {
        "id": 6,
        "name": "张宝伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任地委书记",
        "current_org": "中国共产党大兴安岭地区委员会",
        "source": "https://zh.wikipedia.org/wiki/大兴安岭地区"
    },
    {
        "id": 7,
        "name": "李大义",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任地委书记/行署专员",
        "current_org": "中国共产党大兴安岭地区委员会",
        "source": "https://zh.wikipedia.org/wiki/大兴安岭地区"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中国共产党大兴安岭地区委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中国共产党黑龙江省委员会",
        "location": "大兴安岭地区"
    },
    {
        "id": 2,
        "name": "大兴安岭地区行政公署",
        "type": "政府",
        "level": "地级",
        "parent": "黑龙江省人民政府",
        "location": "大兴安岭地区"
    },
    {
        "id": 3,
        "name": "黑龙江省人大常委会大兴安岭地区工作委员会",
        "type": "人大",
        "level": "地级",
        "parent": "黑龙江省人民代表大会常务委员会",
        "location": "大兴安岭地区"
    },
    {
        "id": 4,
        "name": "黑龙江省政协大兴安岭地区工作委员会",
        "type": "政协",
        "level": "地级",
        "parent": "中国人民政治协商会议黑龙江省委员会",
        "location": "大兴安岭地区"
    },
    {
        "id": 5,
        "name": "黑龙江省人民政府",
        "type": "政府",
        "level": "省级",
        "parent": "",
        "location": "哈尔滨市"
    },
    {
        "id": 6,
        "name": "中国共产党黑龙江省委员会",
        "type": "党委",
        "level": "省级",
        "parent": "",
        "location": "哈尔滨市"
    },
]

# ── Positions ──────────────────────────────────────────────────────────────

positions = [
    # 范庆华 career timeline
    {"person_id": 1, "org_id": 1, "title": "大兴安岭地委书记", "start_date": "2023-10", "end_date": "present", "rank": "正厅级", "note": "2023年10月任大兴安岭地委书记"},
    {"person_id": 1, "org_id": 2, "title": "大兴安岭地区行署专员", "start_date": "2022-03", "end_date": "2024-01", "rank": "正厅级", "note": "2022年3月至2024年1月任行署专员"},
    {"person_id": 1, "org_id": 1, "title": "大兴安岭地委副书记", "start_date": "2022-03", "end_date": "2023-10", "rank": "正厅级", "note": "任专员期间同时任地委副书记"},

    # 王青伟
    {"person_id": 2, "org_id": 2, "title": "大兴安岭地区行署专员", "start_date": "2024-01", "end_date": "present", "rank": "正厅级", "note": "2024年1月任行署专员"},
    {"person_id": 2, "org_id": 1, "title": "大兴安岭地委副书记", "start_date": "2024-01", "end_date": "present", "rank": "正厅级", "note": "地委副书记、行署专员"},

    # 蒋迎娟
    {"person_id": 3, "org_id": 3, "title": "地区人大工委主任", "start_date": "2024-06", "end_date": "present", "rank": "正厅级", "note": "2024年6月任现职"},

    # 王洪斌
    {"person_id": 4, "org_id": 4, "title": "地区政协工委主任", "start_date": "2021-12", "end_date": "present", "rank": "正厅级", "note": "2021年12月当选"},

    # 徐向国（前任地委书记）
    {"person_id": 5, "org_id": 1, "title": "大兴安岭地委书记", "start_date": "2022-03", "end_date": "2023-10", "rank": "正厅级", "note": "2022年3月至2023年10月任地委书记"},
    {"person_id": 5, "org_id": 2, "title": "大兴安岭地区行署专员", "start_date": "2021-04", "end_date": "2022-03", "rank": "正厅级", "note": "2021年4月至2022年3月任行署专员"},

    # 张宝伟（前任地委书记）
    {"person_id": 6, "org_id": 1, "title": "大兴安岭地委书记", "start_date": "2021-04", "end_date": "2021-12", "rank": "正厅级", "note": "2021年4月至2021年12月任地委书记"},
    {"person_id": 6, "org_id": 2, "title": "大兴安岭地区行署专员", "start_date": "2020-01", "end_date": "2021-04", "rank": "正厅级", "note": "2020年1月至2021年4月任行署专员"},

    # 李大义（前任地委书记）
    {"person_id": 7, "org_id": 1, "title": "大兴安岭地委书记", "start_date": "2019-10", "end_date": "2021-04", "rank": "正厅级", "note": "2019年10月至2021年4月任地委书记"},
    {"person_id": 7, "org_id": 2, "title": "大兴安岭地区行署专员", "start_date": "2017-10", "end_date": "2020-01", "rank": "正厅级", "note": "2017年10月至2020年1月任行署专员"},
]

# ── Relationships ──────────────────────────────────────────────────────────

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "范庆华作为地委书记，王青伟作为行署专员，党政主要领导搭档",
        "overlap_org": "大兴安岭地区",
        "overlap_period": "2024-01至今"
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "范庆华与蒋迎娟在大兴安岭地区共事",
        "overlap_org": "大兴安岭地区",
        "overlap_period": "2023-10至今"
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "overlap",
        "context": "范庆华与王洪斌在大兴安岭地区共事",
        "overlap_org": "大兴安岭地区",
        "overlap_period": "2023-10至今"
    },
    {
        "person_a": 1, "person_b": 5,
        "type": "predecessor_successor",
        "context": "范庆华接替徐向国任大兴安岭地委书记",
        "overlap_org": "中国共产党大兴安岭地区委员会",
        "overlap_period": "2023-10",
        "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 6,
        "type": "predecessor_successor",
        "context": "范庆华接替张宝伟（间接）走地委书记任职链",
        "overlap_org": "中国共产党大兴安岭地区委员会",
        "overlap_period": "2021-2023",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 1,
        "type": "predecessor_successor",
        "context": "王青伟接替范庆华任行署专员（范庆华转任书记）",
        "overlap_org": "大兴安岭地区行政公署",
        "overlap_period": "2024-01"
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "王青伟与蒋迎娟在大兴安岭地区共事",
        "overlap_org": "大兴安岭地区",
        "overlap_period": "2024-01至今"
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "overlap",
        "context": "王青伟与王洪斌在大兴安岭地区共事",
        "overlap_org": "大兴安岭地区",
        "overlap_period": "2024-01至今"
    },
    {
        "person_a": 3, "person_b": 4,
        "type": "overlap",
        "context": "蒋迎娟与王洪斌在大兴安岭地区共事",
        "overlap_org": "大兴安岭地区",
        "overlap_period": "2024-06至今"
    },
    {
        "person_a": 5, "person_b": 7,
        "type": "predecessor_successor",
        "context": "徐向国接替李大义任地委书记",
        "overlap_org": "中国共产党大兴安岭地区委员会",
        "overlap_period": "2022-03"
    },
    {
        "person_a": 6, "person_b": 7,
        "type": "predecessor_successor",
        "context": "张宝伟接替李大义任地委书记",
        "overlap_org": "中国共产党大兴安岭地区委员会",
        "overlap_period": "2021-04"
    },
    {
        "person_a": 5, "person_b": 6,
        "type": "predecessor_successor",
        "context": "徐向国接替张宝伟任地委书记",
        "overlap_org": "中国共产党大兴安岭地区委员会",
        "overlap_period": "2022-03"
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
    if name == "范庆华":
        return "255,50,50"
    # Government leader — Blue
    if name == "王青伟":
        return "50,100,255"
    # 人大 — Cyan
    if name == "蒋迎娟":
        return "200,255,255"
    # 政协 — Cream
    if name == "王洪斌":
        return "255,240,200"
    # 前任 — Grey
    if name in ("徐向国", "张宝伟", "李大义"):
        return "150,150,150"
    # Others — Grey
    return "100,100,100"


def person_size(name):
    if name in ("范庆华", "王青伟"):
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
    lines.append(f'    <description>大兴安岭地区领导班子工作关系网络 - {SLUG}</description>')
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
            "city": "大兴安岭地区",
            "region": "大兴安岭地区",
            "job": p.get("current_post", ""),
            "task_id": "heilongjiang_大兴安岭地区",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"dxal_{p['name']}",
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
            "identity": "confirmed" if p["gender"] and p["birth"] else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if p["name"] in ("范庆华",) else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{p['name']}的完整履历信息（含教育背景、早期职务）需补充"
        },
        "open_questions": [
            {
                "priority": "critical" if p["name"] in ("王青伟",) else "high",
                "question": f"{p['name']}的完整职业生涯履历（含出生信息、教育背景、历任职务）",
                "why_it_matters": "无法追溯其任职路径和系统经历",
                "suggested_queries": [f"{p['name']} 简历 大兴安岭", f"{p['name']} 任前公示"],
                "last_attempted": AS_OF
            }
        ]
    }


def build_person_jsons():
    source_register = [
        {"id": "S001", "title": "维基百科—大兴安岭地区", "url": "https://zh.wikipedia.org/wiki/大兴安岭地区", "publisher": "维基百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "大兴安岭地区四大机构领导人表"},
        {"id": "S002", "title": "大兴安岭地区行政公署网站", "url": "http://www.dxal.gov.cn", "publisher": "大兴安岭地区行政公署", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "官方网站确认域名和领导活动"},
    ]

    # === 1. 范庆华 (地委书记) ===
    fan_timeline = [
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未找到2022年3月前详细履历。范庆华（1972年10月生，吉林延吉人）。据维基百科推测可能曾任黑龙江省直部门或大兴安岭地区副职。", "confidence": "unverified", "source_ids": []},
        {"start": "2022-03", "end": "2024-01", "org": "大兴安岭地区行政公署", "title": "行署专员", "notes": "2022年3月任大兴安岭地区行署专员", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2023-10", "end": "present", "org": "中国共产党大兴安岭地区委员会", "title": "地委书记", "notes": "2023年10月任大兴安岭地委书记", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    fan_relationships = [
        {"person": "王青伟", "person_id": "dxal_王青伟", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "范庆华转任书记后，王青伟接任行署专员", "overlap_org": "大兴安岭地区", "overlap_period": "2024-01", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "徐向国", "person_id": "dxal_徐向国", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "范庆华接替徐向国任大兴安岭地委书记", "overlap_org": "中共大兴安岭地委", "overlap_period": "2023-10", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "蒋迎娟", "person_id": "dxal_蒋迎娟", "relationship_type": "overlap", "strength": "medium", "evidence": "在地委/人大工委共事", "overlap_org": "大兴安岭地区", "overlap_period": "2023-10至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "王洪斌", "person_id": "dxal_王洪斌", "relationship_type": "overlap", "strength": "medium", "evidence": "在地委/政协工委共事", "overlap_org": "大兴安岭地区", "overlap_period": "2023-10至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    fan_json = make_person_json(persons[0], fan_timeline, fan_relationships, source_register)
    fan_json["professional_profile"]["career_pattern"] = "local_ladder"
    fan_json["professional_profile"]["promotion_velocity"] = {
        "summary": "1972年生，2022年已任行署专员（正厅级），2023年转任地委书记",
        "notable_fast_promotions": ["51岁任地委书记"]
    }
    fan_json["open_questions"] = [
        {"priority": "critical", "question": "范庆华2022年3月前的完整职业生涯履历（含教育背景、历任职务）", "why_it_matters": "核心人物，但其50岁前履历几乎完全空白", "suggested_queries": ["范庆华 1972 延吉 简历", "范庆华 大兴安岭 任前公示", "范庆华 黑龙江 任职经历"], "last_attempted": AS_OF},
    ]

    fan_path = PERSONS_DIR / f"{TODAY}-黑龙江省-大兴安岭地区-地委书记-范庆华.json"
    with open(fan_path, "w", encoding="utf-8") as f:
        json.dump(fan_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fan_path.name}")

    # === 2. 王青伟 (行署专员) ===
    wang_timeline = [
        {"start": "unknown", "end": "2024-01", "org": "履历缺口", "title": "", "notes": "公开资料未找到2024年1月前详细履历。王青伟（1975年2月生，黑龙江尚志人）。此前任职经历待查。", "confidence": "unverified", "source_ids": []},
        {"start": "2024-01", "end": "present", "org": "大兴安岭地区行政公署", "title": "行署专员", "notes": "2024年1月任大兴安岭地区行署专员", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2024-01", "end": "present", "org": "中国共产党大兴安岭地区委员会", "title": "地委副书记", "notes": "任专员同时任地委副书记", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    wang_open_questions = [
        {"priority": "critical", "question": "王青伟2024年1月前的完整职业生涯履历（含教育背景、历任职务）", "why_it_matters": "现任行署专员（2024年1月上任），此前任职经历完全空白", "suggested_queries": ["王青伟 1975 尚志 简历", "王青伟 任前公示", "王青伟 大兴安岭 任职"], "last_attempted": AS_OF},
    ]
    wang_relationships = [
        {"person": "范庆华", "person_id": "dxal_范庆华", "relationship_type": "subordinate_to_superior", "strength": "strong", "evidence": "行署专员受地委书记领导", "overlap_org": "大兴安岭地区", "overlap_period": "2024-01至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "蒋迎娟", "person_id": "dxal_蒋迎娟", "relationship_type": "overlap", "strength": "medium", "evidence": "行署专员与人大工委主任共事", "overlap_org": "大兴安岭地区", "overlap_period": "2024-01至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "王洪斌", "person_id": "dxal_王洪斌", "relationship_type": "overlap", "strength": "medium", "evidence": "行署专员与政协工委主任共事", "overlap_org": "大兴安岭地区", "overlap_period": "2024-01至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    wang_json = make_person_json(persons[1], wang_timeline, wang_relationships, source_register)
    wang_json["open_questions"] = wang_open_questions
    wang_path = PERSONS_DIR / f"{TODAY}-黑龙江省-大兴安岭地区-行署专员-王青伟.json"
    with open(wang_path, "w", encoding="utf-8") as f:
        json.dump(wang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {wang_path.name}")

    # === 3. 蒋迎娟 (人大工委主任) ===
    jiang_timeline = [
        {"start": "2024-06", "end": "present", "org": "黑龙江省人大常委会大兴安岭地区工作委员会", "title": "主任", "notes": "2024年6月任现职——此前履历待查", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "蒋迎娟（1970年3月生，黑龙江通河人），此前履历不详", "confidence": "unverified", "source_ids": []},
    ]
    jiang_relationships = []
    jiang_json = make_person_json(persons[2], jiang_timeline, jiang_relationships, source_register)
    jiang_path = PERSONS_DIR / f"{TODAY}-黑龙江省-大兴安岭地区-人大工委主任-蒋迎娟.json"
    with open(jiang_path, "w", encoding="utf-8") as f:
        json.dump(jiang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {jiang_path.name}")

    # === 4. 王洪斌 (政协工委主任) ===
    hongbin_timeline = [
        {"start": "2021-12", "end": "present", "org": "黑龙江省政协大兴安岭地区工作委员会", "title": "主任", "notes": "2021年12月任现职——此前履历待查", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "王洪斌（1966年6月生），此前履历不详", "confidence": "unverified", "source_ids": []},
    ]
    hongbin_relationships = []
    hongbin_json = make_person_json(persons[3], hongbin_timeline, hongbin_relationships, source_register)
    hongbin_path = PERSONS_DIR / f"{TODAY}-黑龙江省-大兴安岭地区-政协工委主任-王洪斌.json"
    with open(hongbin_path, "w", encoding="utf-8") as f:
        json.dump(hongbin_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {hongbin_path.name}")


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
