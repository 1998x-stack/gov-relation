#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
泸定县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 四川省
Parent City: 甘孜藏族自治州
Region: 泸定县
Targets: 县委书记 & 县长

Research Date: 2026-08-03
Research Note:
   泸定县人民政府门户网站 (http://www.luding.gov.cn/) 可直接访问。
   县政府领导页面 (ldzc/) 列出县长黎昌盛及9位副县长详细信息。
   县委书记信息来自新闻报道交叉验证。

   关键确认信息：
   - 赵景红：县委书记、海螺沟景区党工委书记（2026-07-06 新闻确认）
   - 黎昌盛：县委副书记、县长、县政府党组书记（官网简历确认，1972年6月生）
   - 曾德成：县委常委、常务副县长（官网简历确认，1979年7月生，藏族）

   百度搜索及Jina Reader均无法正常访问。
   赵景红简历未能从公开来源获取（县委书记不在县政府领导之窗展示）。
   部分人物完整履历缺失。

Sources:
   - http://www.luding.gov.cn/ldzc (领导之窗 — 县长及副县长简历)
   - http://www.luding.gov.cn/fmxw/article/721637 (2026-07-06: 确认赵景红为县委书记)
   - http://www.luding.gov.cn/ttxw/article/725848 (2026-08-03: 确认黎昌盛为县长主持会议)
   - http://www.luding.gov.cn/fmxw/article/722747 (2026-07-17: 确认曾德成为常务副县长)
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "泸定县"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-08-03"
TODAY = "20260803"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：县委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "赵景红",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "泸定县委书记、海螺沟景区党工委书记",
        "current_org": "中共泸定县委员会",
        "source": "http://www.luding.gov.cn/fmxw/article/721637 (2026-07-06新闻确认为县委书记)"
    },
    # ════════════════════════════════════════
    # 核心领导：县长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "黎昌盛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-06",
        "birthplace": "",
        "education": "大学文化",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "泸定县委副书记、县政府县长、党组书记",
        "current_org": "泸定县人民政府",
        "source": "http://www.luding.gov.cn/xz_lcs (官网简历)"
    },
    # ════════════════════════════════════════
    # 核心副职：常务副县长
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "曾德成",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1979-07",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "泸定县委常委、县政府常务副县长、党组成员",
        "current_org": "泸定县人民政府",
        "source": "http://www.luding.gov.cn/fxz_cdc (官网简历)"
    },
    # ════════════════════════════════════════
    # 副县长
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "陈治普",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "泸定县副县长",
        "current_org": "泸定县人民政府",
        "source": "http://www.luding.gov.cn/ldzc (领导之窗)"
    },
    {
        "id": 5,
        "name": "高嵩",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "泸定县副县长",
        "current_org": "泸定县人民政府",
        "source": "http://www.luding.gov.cn/ldzc (领导之窗)"
    },
    {
        "id": 6,
        "name": "陈春涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "泸定县副县长",
        "current_org": "泸定县人民政府",
        "source": "http://www.luding.gov.cn/ldzc (领导之窗)"
    },
    {
        "id": 7,
        "name": "达瓦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "泸定县副县长",
        "current_org": "泸定县人民政府",
        "source": "http://www.luding.gov.cn/ldzc (领导之窗)"
    },
    {
        "id": 8,
        "name": "尔基泽绒",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "泸定县副县长",
        "current_org": "泸定县人民政府",
        "source": "http://www.luding.gov.cn/ldzc (领导之窗)"
    },
    {
        "id": 9,
        "name": "倪月刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "泸定县副县长",
        "current_org": "泸定县人民政府",
        "source": "http://www.luding.gov.cn/ldzc (领导之窗)"
    },
    {
        "id": 10,
        "name": "刘萍",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "泸定县副县长",
        "current_org": "泸定县人民政府",
        "source": "http://www.luding.gov.cn/ldzc (领导之窗); http://www.luding.gov.cn/fmxw/article/722747 (确认出席安全生产会议)"
    },
    {
        "id": 11,
        "name": "王凯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "泸定县副县长",
        "current_org": "泸定县人民政府",
        "source": "http://www.luding.gov.cn/ldzc (领导之窗)"
    },
    # ════════════════════════════════════════
    # 组织：县委办公室
    # ════════════════════════════════════════
    # 县委常委、组织部长等信息来自对领导之窗结构的推断
    # 由于领导之窗仅展示政府序列，县委领导信息待补充
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {
        "id": 1,
        "name": "中共泸定县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共甘孜藏族自治州委员会",
        "location": "四川省甘孜州泸定县"
    },
    {
        "id": 2,
        "name": "泸定县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "甘孜藏族自治州人民政府",
        "location": "四川省甘孜州泸定县"
    },
    {
        "id": 3,
        "name": "海螺沟景区管理局",
        "type": "事业单位",
        "level": "县级",
        "parent": "甘孜藏族自治州人民政府",
        "location": "四川省甘孜州泸定县磨西镇"
    },
    {
        "id": 4,
        "name": "泸定县审计局",
        "type": "政府",
        "level": "乡科级",
        "parent": "泸定县人民政府",
        "location": "四川省甘孜州泸定县"
    },
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 赵景红 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "泸定县委书记", "start": "", "end": "present", "rank": "县处级正职", "note": "同时兼任海螺沟景区党工委书记。任县委书记时间待确认。"},
    {"person_id": 1, "org_id": 3, "title": "海螺沟景区党工委书记", "start": "", "end": "present", "rank": "县处级正职", "note": "跨部门兼职"},
    # 黎昌盛 — 县长
    {"person_id": 2, "org_id": 2, "title": "泸定县人民政府县长", "start": "", "end": "present", "rank": "县处级正职", "note": "同时任县委副书记、县政府党组书记"},
    {"person_id": 2, "org_id": 1, "title": "泸定县委副书记", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 曾德成 — 常务副县长
    {"person_id": 3, "org_id": 2, "title": "县委常委、县政府常务副县长", "start": "", "end": "present", "rank": "县处级副职", "note": "负责发改、财政、人社、应急等"},
    # 副县长们
    {"person_id": 4, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 赵景红 — 黎昌盛 (党政一把手)
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "赵景红任县委书记，黎昌盛任县长，为泸定县党政主要负责人",
        "overlap_org": "中共泸定县委员会",
        "overlap_period": ""
    },
    # 赵景红 — 曾德成 (上级/常委)
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "赵景红为县委书记，曾德成为县委常委、常务副县长",
        "overlap_org": "中共泸定县委员会",
        "overlap_period": ""
    },
    # 黎昌盛 — 曾德成 (正副职)
    {
        "person_a": 2,
        "person_b": 3,
        "type": "overlap",
        "context": "黎昌盛任县长，曾德成任常务副县长，为政府正副职",
        "overlap_org": "泸定县人民政府",
        "overlap_period": ""
    },
]

# =========================================================================
# 5. BUILD
# =========================================================================

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def create_sqlite(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS relationships")
    c.execute("DROP TABLE IF EXISTS positions")
    c.execute("DROP TABLE IF EXISTS organizations")
    c.execute("DROP TABLE IF EXISTS persons")
    c.execute("""CREATE TABLE persons(
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE organizations(
        id INTEGER PRIMARY KEY, name TEXT, type TEXT,
        level TEXT, parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE positions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER, title TEXT,
        start TEXT, "end" TEXT, rank TEXT, note TEXT
    )""")
    c.execute("""CREATE TABLE relationships(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER, type TEXT,
        context TEXT, overlap_org TEXT, overlap_period TEXT
    )""")
    for p in persons:
        c.execute("""INSERT INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"], p["work_start"],
                   p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES(?,?,?,?,?,?)""",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        c.execute("""INSERT INTO positions(person_id, org_id, title, start, "end", rank, note) VALUES(?,?,?,?,?,?,?)""",
                  (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))
    for r in relationships:
        c.execute("""INSERT INTO relationships(person_a, person_b, type, context, overlap_org, overlap_period) VALUES(?,?,?,?,?,?)""",
                  (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))
    conn.commit()
    conn.close()
    print(f"  DB: {db_path} ({len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships)")

def person_color(role):
    if not role:
        return "100,100,100"
    if "书记" in role and "县委" in role:
        return "255,50,50"
    elif "县长" in role:
        return "50,100,255"
    elif "常务副" in role:
        return "50,100,255"
    elif "副县长" in role:
        return "100,100,255"
    return "100,100,100"

def is_top_leader(p):
    title = p.get("current_post", "")
    return "县委书记" in title or "县长" in title

def create_gexf(gexf_path):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append(f'    <description>泸定县领导班子工作关系网络 (截至{AS_OF})</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # nodes - persons
    lines.append('    <nodes>')
    for p in persons:
        role = p.get("current_post", "")
        c = person_color(role)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # nodes - orgs
    for o in organizations:
        if o["type"] == "党委":
            oc = "255,200,200"
        elif o["type"] == "政府":
            oc = "200,200,255"
        elif o["type"] == "事业单位":
            oc = "220,220,220"
        else:
            oc = "200,200,200"
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # edges
    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

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

    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {gexf_path}")

def write_person_json(person, suffix):
    """Write a person JSON file."""
    slug_name = person['name']
    fname = f"{TODAY}-四川省-甘孜藏族自治州-{suffix}-{slug_name}.json"
    fpath = os.path.join(PERSONS_DIR, fname)

    # Build source register
    srcs = []
    sid = 0
    def add_source(title, url, publisher, stype, reliability, notes=""):
        nonlocal sid
        sid += 1
        srcs.append({
            "id": f"S{sid:03d}",
            "title": title,
            "url": url,
            "publisher": publisher,
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": stype,
            "reliability": reliability,
            "notes": notes
        })
        return f"S{sid:03d}"

    add_source("泸定县领导之窗 - 县长黎昌盛",
               "http://www.luding.gov.cn/ldzc", "泸定县人民政府", "official", "high")
    add_source("泸定县国土空间规划委员会会议",
               "http://www.luding.gov.cn/fmxw/article/721637", "泸定之声", "official", "high",
               "确认赵景红为县委书记、黎昌盛为县长")
    add_source("泸定县十八届人民政府第九次全会",
               "http://www.luding.gov.cn/ttxw/article/725848", "泸定之声", "official", "high",
               "确认黎昌盛为县长主持会议")
    add_source("泸定县安全生产防汛减灾专题会",
               "http://www.luding.gov.cn/fmxw/article/722747", "泸定之声", "official", "high",
               "确认曾德成为常务副县长、刘萍为副县长")
    add_source("泸定县领导之窗副县长页面",
               "http://www.luding.gov.cn/ldzc", "泸定县人民政府", "official", "high",
               "列出全部副县长名单")

    person_id = f"sichuan_{SLUG}_{slug_name}"

    # Determine rank
    post = person.get("current_post", "")
    if "书记" in post and "县委" in post:
        rank_val = "县处级正职"
    elif "县长" in post:
        rank_val = "县处级正职"
    elif "副" in post:
        rank_val = "县处级副职"
    else:
        rank_val = ""

    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "四川省",
            "city": "甘孜藏族自治州",
            "region": "泸定县",
            "job": suffix,
            "task_id": "sichuan_泸定县",
            "time_focus": "截至2026年8月"
        },
        "identity": {
            "person_id": person_id,
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{slug_name}_{person.get('birth', 'unknown')}",
                "name_birthplace": f"{slug_name}_{person.get('birthplace', '')}",
                "official_profile_url": f"http://www.luding.gov.cn/{''}"
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person.get("current_org", ""),
            "administrative_rank": rank_val,
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"]
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
        "source_register": srcs,
        "confidence_summary": {
            "identity": "confirmed" if person.get("gender") or person.get("birth") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "出生年月、籍贯、教育背景、完整职业履历均缺失（县委书记赵景红尤甚）"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的出生年月、籍贯、民族" if not person.get("birth") else f"{person['name']}的完整工作履历",
                "why_it_matters": "身份信息的核心字段，用于人员去重和网络构建",
                "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 任前公示", f"{person['name']} 甘孜"],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": f"{person['name']}的完整工作履历（含此前任职）",
                "why_it_matters": "网络关系中的时间线分析核心数据",
                "suggested_queries": [f"{person['name']} 任职 经历", f"{person['name']} 甘孜州"],
                "last_attempted": AS_OF
            }
        ]
    }
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath}")

# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    print(f"Building {SLUG} data artifacts...")
    create_sqlite(DB_PATH)
    create_gexf(GEXF_PATH)

    # Write person JSONs for core leaders
    write_person_json(persons[0], "县委书记")  # 赵景红
    write_person_json(persons[1], "县长")      # 黎昌盛
    write_person_json(persons[2], "常务副县长") # 曾德成

    print("Done!")