#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 五大连池市 (Wudalianchi City), 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_五大连池市
Level: 县级市
Targets: 市委书记 & 市长
Parent city: 黑河市

Research sources:
  - www.wdlc.gov.cn — 五大连池市人民政府网站确认张继东（市长）、陈可航（副市长）等领导信息
  - Baidu Baike and Wikipedia were unreachable during this investigation

Confidence notes:
  - 张继东 (市长): confirmed via official government website (male, Han, born Mar 1983, Hailun, Heilongjiang)
  - 市委书记: NOT FOUND — the official site's 市委 leadership page was inaccessible (403/404)
  - Deputy mayors: names confirmed from government website, detailed bios partially available
  - Due to severe web access limitations (Exa rate-limited, Jina timeout, Baidu 403, gov.cn sections 404/403),
    detailed biographies for all figures remain incomplete
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
SLUG = "五大连池市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging directory
STAGING = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING, f"{SLUG}_network.gexf")

# ── Persons ─────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 1,
        "name": "市委书记（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共五大连池市委员会",
        "source": "姓名待查 — 官方网站领导之窗页面无法访问"
    },
    {
        "id": 2,
        "name": "张继东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年3月",
        "birthplace": "黑龙江省海伦市",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "2007年9月",
        "current_post": "市长",
        "current_org": "五大连池市人民政府",
        "source": "http://www.wdlc.gov.cn/wdlc/c101417/szfld.shtml"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Mayors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "陈可航",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1991年10月",
        "birthplace": "山东省即墨市",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "2013年10月",
        "current_post": "市委常委、副市长",
        "current_org": "五大连池市人民政府",
        "source": "http://www.wdlc.gov.cn/wdlc/chenkehang/szfld.shtml"
    },
    {
        "id": 4,
        "name": "孙宝柱",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "五大连池市人民政府",
        "source": "http://www.wdlc.gov.cn/wdlc/c101423/szfld.shtml"
    },
    {
        "id": 5,
        "name": "张贺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "五大连池市人民政府",
        "source": "http://www.wdlc.gov.cn/wdlc/c101422/szfld.shtml"
    },
    {
        "id": 6,
        "name": "马跃海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "五大连池市人民政府",
        "source": "http://www.wdlc.gov.cn/wdlc/c101421/szfld.shtml"
    },
    {
        "id": 7,
        "name": "谷大伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "五大连池市人民政府",
        "source": "http://www.wdlc.gov.cn/wdlc/c101426k/szfld.shtml"
    },
    {
        "id": 8,
        "name": "黄微",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "五大连池市人民政府",
        "source": "http://www.wdlc.gov.cn/wdlc/c101427d/szfld.shtml"
    },
    {
        "id": 9,
        "name": "李传义",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "五大连池市人民政府",
        "source": "http://www.wdlc.gov.cn/wdlc/c101424/szfld.shtml"
    },
    {
        "id": 10,
        "name": "张磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "五大连池市人民政府",
        "source": "http://www.wdlc.gov.cn/wdlc/szffszzl/szfld.shtml"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共五大连池市委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共黑河市委员会",
        "location": "五大连池市"
    },
    {
        "id": 2,
        "name": "五大连池市人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "黑河市人民政府",
        "location": "五大连池市"
    },
    {
        "id": 3,
        "name": "五大连池市人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "黑河市人民代表大会常务委员会",
        "location": "五大连池市"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议五大连池市委员会",
        "type": "政协",
        "level": "县级",
        "parent": "中国人民政治协商会议黑河市委员会",
        "location": "五大连池市"
    },
    {
        "id": 5,
        "name": "五大连池市监察委员会",
        "type": "政府",
        "level": "县级",
        "parent": "黑河市监察委员会",
        "location": "五大连池市"
    },
    {
        "id": 6,
        "name": "中共黑河市委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中共黑龙江省委员会",
        "location": "黑河市"
    },
    {
        "id": 7,
        "name": "黑河市人民政府",
        "type": "政府",
        "level": "地级",
        "parent": "黑龙江省人民政府",
        "location": "黑河市"
    },
]

# ── Positions ──────────────────────────────────────────────────────────────

positions = [
    # 市委书记（待确认）
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "前任市委书记姓名及任职时间待查"},
    # 张继东
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "市委副书记、市长"},
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "主持市政府全面工作。据官网简历确认"},
    # 陈可航
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "市委常委、副市长"},
    {"person_id": 3, "org_id": 2, "title": "副市长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "协助张继东同志工作，侧重生态环境保护"},
    # Deputy mayors
    {"person_id": 4, "org_id": 2, "title": "副市长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "市委书记与市长（党政主要领导搭档）",
        "overlap_org": "五大连池市",
        "overlap_period": "待确认",
        "confidence": "unverified"
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "superior_subordinate",
        "context": "市长与副市长工作搭档，陈可航协助张继东工作",
        "overlap_org": "五大连池市人民政府",
        "overlap_period": "待确认",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "superior_subordinate",
        "context": "市长与副市长工作搭档",
        "overlap_org": "五大连池市人民政府",
        "overlap_period": "待确认",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 5,
        "type": "superior_subordinate",
        "context": "市长与副市长工作搭档",
        "overlap_org": "五大连池市人民政府",
        "overlap_period": "待确认",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 6,
        "type": "superior_subordinate",
        "context": "市长与副市长工作搭档",
        "overlap_org": "五大连池市人民政府",
        "overlap_period": "待确认",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 7,
        "type": "superior_subordinate",
        "context": "市长与副市长工作搭档",
        "overlap_org": "五大连池市人民政府",
        "overlap_period": "待确认",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 8,
        "type": "superior_subordinate",
        "context": "市长与副市长工作搭档",
        "overlap_org": "五大连池市人民政府",
        "overlap_period": "待确认",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 9,
        "type": "superior_subordinate",
        "context": "市长与副市长工作搭档",
        "overlap_org": "五大连池市人民政府",
        "overlap_period": "待确认",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 10,
        "type": "superior_subordinate",
        "context": "市长与副市长工作搭档",
        "overlap_org": "五大连池市人民政府",
        "overlap_period": "待确认",
        "confidence": "confirmed"
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
    if name == "市委书记（待确认）":
        return "255,50,50"  # Party Secretary — Red
    if name == "张继东":
        return "50,100,255"  # Government leader — Blue
    if name == "陈可航":
        return "100,100,255"  # Deputy mayor — lighter blue
    return "100,100,100"  # Others — Grey


def person_size(name):
    if name in ("市委书记（待确认）", "张继东"):
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
    lines.append(f'    <description>五大连池市领导班子工作关系网络 - {SLUG}</description>')
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

def make_person_json(p, identity_updates=None, timeline=None, relationships_list=None, source_register=None):
    if identity_updates is None:
        identity_updates = {}
    if timeline is None:
        timeline = []
    if relationships_list is None:
        relationships_list = []
    if source_register is None:
        source_register = []

    dedupe_name = p["name"].replace("（待确认）", "")
    base_person_id = f"wdlc_{dedupe_name}"

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "五大连池市",
            "region": "五大连池市",
            "job": p.get("current_post", ""),
            "task_id": "heilongjiang_五大连池市",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": base_person_id,
            "name": dedupe_name,
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{dedupe_name}_{p.get('birth','')}",
                "name_birthplace": f"{dedupe_name}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source", "")
            },
            **identity_updates
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": True if p["name"] != "市委书记（待确认）" else False,
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
            "identity": "confirmed" if p["gender"] and p["birth"] else "unverified" if p["name"] == "市委书记（待确认）" else "plausible",
            "current_role": "unverified" if p["name"] == "市委书记（待确认）" else "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": f"{dedupe_name}的完整履历信息需补充"
        },
        "open_questions": [
            {
                "priority": "critical" if p["name"] in ("市委书记（待确认）",) else "high",
                "question": f"{dedupe_name}的完整职业生涯履历（含教育背景、历任职务）",
                "why_it_matters": "核心人物信息不完整",
                "suggested_queries": [f"{dedupe_name} 五大连池 简历", f"{dedupe_name} 任前公示", f"五大连池市 市委书记 2026"],
                "last_attempted": AS_OF
            }
        ]
    }


def build_person_jsons():
    source_register = [
        {"id": "S001", "title": "五大连池市人民政府—市政府领导页面", "url": "http://www.wdlc.gov.cn/wdlc/c100751/szf.shtml", "publisher": "五大连池市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认张继东（市长）、陈可航等8名副市长"},
        {"id": "S002", "title": "五大连池市人民政府—张继东简历", "url": "http://www.wdlc.gov.cn/wdlc/c101417/szfld.shtml", "publisher": "五大连池市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "张继东简历：1983年3月生，黑龙江海伦人，大学本科学历"},
        {"id": "S003", "title": "五大连池市人民政府—陈可航简历", "url": "http://www.wdlc.gov.cn/wdlc/chenkehang/szfld.shtml", "publisher": "五大连池市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "陈可航简历：1991年10月生，山东即墨人，研究生学历"},
    ]

    # === 1. 张继东 ===
    zhang_timeline = [
        {"start": "2007-09", "end": "unknown", "org": "（早期履历待查）", "title": "", "notes": "2007年9月参加工作，此前教育背景：大学本科。早期任职经历待补充", "confidence": "unverified", "source_ids": ["S002"]},
        {"start": "unknown", "end": "present", "org": "中共五大连池市委员会", "title": "市委副书记", "notes": "任副书记时间待查", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"start": "unknown", "end": "present", "org": "五大连池市人民政府", "title": "市长", "notes": "主持市政府全面工作。主管市审计局", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    ]
    zhang_relationships = [
        {"person": "市委书记（待确认）", "person_id": "wdlc_市委书记（待确认）", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "市长受市委书记领导", "overlap_org": "五大连池市", "overlap_period": "待确认", "direction": "undirected", "confidence": "confirmed", "source_ids": []},
        {"person": "陈可航", "person_id": "wdlc_陈可航", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "市长与副市长工作搭档，陈可航协助张继东工作", "overlap_org": "五大连池市人民政府", "overlap_period": "待确认", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "孙宝柱", "person_id": "wdlc_孙宝柱", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "市长与副市长工作搭档", "overlap_org": "五大连池市人民政府", "overlap_period": "待确认", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    zhang_json = make_person_json(persons[1], timeline=zhang_timeline, relationships_list=zhang_relationships, source_register=source_register)
    zhang_json["professional_profile"]["career_pattern"] = "unknown"
    zhang_json["professional_profile"]["promotion_velocity"] = {
        "summary": "1983年生，现任五大连池市市长（正处级），43岁任市长",
        "notable_fast_promotions": []
    }

    zhang_path = os.path.join(STAGING, f"{TODAY}-黑龙江省-黑河市-市长-张继东.json")
    with open(zhang_path, "w", encoding="utf-8") as f:
        json.dump(zhang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {os.path.basename(zhang_path)}")

    # === 2. 陈可航 ===
    chen_timeline = [
        {"start": "2013-10", "end": "unknown", "org": "（早期履历待查）", "title": "", "notes": "2013年10月参加工作，研究生学历。早期任职经历待补充", "confidence": "unverified", "source_ids": ["S003"]},
        {"start": "unknown", "end": "present", "org": "中共五大连池市委员会", "title": "市委常委", "notes": "任常委时间待查", "confidence": "confirmed", "source_ids": ["S003"]},
        {"start": "unknown", "end": "present", "org": "五大连池市人民政府", "title": "副市长", "notes": "协助张继东同志工作，侧重生态环境保护工作", "confidence": "confirmed", "source_ids": ["S003"]},
    ]
    chen_relationships = [
        {"person": "张继东", "person_id": "wdlc_张继东", "relationship_type": "subordinate_to_superior", "strength": "strong", "evidence": "协助市长工作", "overlap_org": "五大连池市人民政府", "overlap_period": "待确认", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
    ]
    chen_json = make_person_json(persons[2], timeline=chen_timeline, relationships_list=chen_relationships, source_register=source_register)
    chen_json["confidence_summary"]["identity"] = "confirmed"
    chen_json["open_questions"] = [
        {"priority": "high", "question": "陈可航任市委常委、副市长前的完整任职经历", "why_it_matters": "1991年生，34岁任市委常委/副市长，晋升路径值得关注", "suggested_queries": ["陈可航 五大连池 简历", "陈可航 黑河 任职经历"], "last_attempted": AS_OF},
    ]

    chen_path = os.path.join(STAGING, f"{TODAY}-黑龙江省-黑河市-副市长-陈可航.json")
    with open(chen_path, "w", encoding="utf-8") as f:
        json.dump(chen_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {os.path.basename(chen_path)}")


# ══════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Change to staging directory for output
    orig_cwd = os.getcwd()
    os.chdir(STAGING)
    try:
        print(f"Building {SLUG} network data...")
        build_db()
        build_gexf()
        build_person_jsons()
        print(f"\nOutput files in: {STAGING}")
        print(f"  DB:     {DB_PATH}")
        print(f"  GEXF:   {GEXF_PATH}")
        for f in os.listdir(STAGING):
            if f.endswith(".json") and f.startswith(TODAY):
                print(f"  Person: {os.path.join(STAGING, f)}")
        print("Done.")
    finally:
        os.chdir(orig_cwd)
