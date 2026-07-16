#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for 宁化县 (Ninghua County), 三明市, 福建省.

Level: 县
Province: 福建省
Parent City: 三明市
Targets: 县委书记 & 县长

Key findings (as of July 2026):
- 县委书记: 未确认 (Not confirmed through available web research channels)
- 县长: 未确认 (Not confirmed through available web research channels)
- 宁化县是著名的客家祖地，中央苏区县，红军长征出发地之一
- 宁化县下辖11镇、4乡、1民族乡，人口约26.2万

Sources:
- Government website: www.fjnh.gov.cn (active, dynamic rendering — leadership pages not directly accessible)
- Chinese Wikipedia: 宁化县 entry — infobox does NOT list current leaders
- Personnel notices on fjnh.gov.cn show names like 张清山, 蒋加福, 郑占泊, 黄华珍, 陈宁河 (likely deputy-level officials)
- No confirmed source found for current 县委书记 or 县长 names through available web channels

Current as of: July 2026

Gaps:
- 县委书记姓名未找到
- 县长姓名未找到
- 两位领导的出生年份、籍贯、教育背景和完整履历
- 历任前任县委书记和县长名单
- 县委常委领导班子完整名单
"""

import sqlite3, os, sys, json
from datetime import datetime

STAGING = os.path.dirname(os.path.abspath(__file__))
PROJECT_BASE = os.path.normpath(os.path.join(STAGING, "..", "..", ".."))
DB_PATH = os.path.join(STAGING, "宁化县_network.db")
GEXF_PATH = os.path.join(STAGING, "宁化县_network.gexf")
PERSONS_DIR = STAGING

AS_OF = "2026-07-16"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 县委书记 — 待查 (not found through available research)
    {"id": 1, "name": "（待查·县委书记）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "宁化县委书记", "current_org": "中共宁化县委员会",
     "source": "",
     "notes": "县委书记姓名未能在公开资料中找到",
     "confidence": "unverified"},

    # 县长 — 待查 (not found through available research)
    {"id": 2, "name": "（待查·县长）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "宁化县县长", "current_org": "宁化县人民政府",
     "source": "",
     "notes": "县长姓名未能在公开资料中找到",
     "confidence": "unverified"},

    # ── Predecessors - 县委书记 ──
    # Note: No predecessor information found through available research channels

    # ── Predecessors - 县长 ──
    # Note: No predecessor information found through available research channels

    # ── Other county-level leaders (from gov website personnel notices) ──
    # These names appeared in 宁化县人民政府 personnel notices but exact roles not confirmed
    {"id": 3, "name": "张清山", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "宁化县（职务待确认）", "current_org": "宁化县人民政府",
     "source": "宁化县人民政府网站 - 职务任免通知 2026-06-24",
     "notes": "出现在2026年6月24日宁化县人民政府职务任免通知中",
     "confidence": "plausible"},

    {"id": 4, "name": "蒋加福", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "宁化县（职务待确认——已免职）", "current_org": "",
     "source": "宁化县人民政府网站 - 免职通知 2026-03-06",
     "notes": "出现在2026年3月6日宁化县人民政府免职通知中",
     "confidence": "plausible"},

    {"id": 5, "name": "郑占泊", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "宁化县（职务待确认）", "current_org": "宁化县人民政府",
     "source": "宁化县人民政府网站 - 职务任免通知 2026-02-10",
     "notes": "出现在2026年2月10日宁化县人民政府职务任免通知中",
     "confidence": "plausible"},

    {"id": 6, "name": "黄华珍", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "宁化县（职务待确认）", "current_org": "宁化县人民政府",
     "source": "宁化县人民政府网站 - 任职通知 2026-02-10",
     "notes": "出现在2026年2月10日宁化县人民政府任职通知中",
     "confidence": "plausible"},

    {"id": 7, "name": "陈宁河", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "宁化县（职务待确认）", "current_org": "宁化县人民政府",
     "source": "宁化县人民政府网站 - 职务任免通知 2026-02-10",
     "notes": "出现在2026年2月10日宁化县人民政府职务任免通知中",
     "confidence": "plausible"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共宁化县委员会", "type": "党委", "level": "县处级",
     "parent": "中共三明市委员会", "location": "福建省三明市宁化县"},
    {"id": 2, "name": "宁化县人民政府", "type": "政府", "level": "县处级",
     "parent": "三明市人民政府", "location": "福建省三明市宁化县"},
    {"id": 3, "name": "宁化县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "三明市人大常委会", "location": "福建省三明市宁化县"},
    {"id": 4, "name": "中国人民政治协商会议宁化县委员会", "type": "政协", "level": "县处级",
     "parent": "政协三明市委员会", "location": "福建省三明市宁化县"},
    {"id": 5, "name": "宁化县监察委员会", "type": "党委", "level": "县处级",
     "parent": "", "location": "福建省三明市宁化县"},

    # 宁化县下辖11镇
    {"id": 11, "name": "翠江镇人民政府", "type": "政府", "level": "乡科级",
     "parent": "宁化县人民政府", "location": "福建省三明市宁化县翠江镇"},
    {"id": 12, "name": "泉上镇人民政府", "type": "政府", "level": "乡科级",
     "parent": "宁化县人民政府", "location": "福建省三明市宁化县泉上镇"},
    {"id": 13, "name": "湖村镇人民政府", "type": "政府", "level": "乡科级",
     "parent": "宁化县人民政府", "location": "福建省三明市宁化县湖村镇"},
    {"id": 14, "name": "石壁镇人民政府", "type": "政府", "level": "乡科级",
     "parent": "宁化县人民政府", "location": "福建省三明市宁化县石壁镇"},
    {"id": 15, "name": "曹坊镇人民政府", "type": "政府", "level": "乡科级",
     "parent": "宁化县人民政府", "location": "福建省三明市宁化县曹坊镇"},
    {"id": 16, "name": "安远镇人民政府", "type": "政府", "level": "乡科级",
     "parent": "宁化县人民政府", "location": "福建省三明市宁化县安远镇"},
    {"id": 17, "name": "淮土镇人民政府", "type": "政府", "level": "乡科级",
     "parent": "宁化县人民政府", "location": "福建省三明市宁化县淮土镇"},
    {"id": 18, "name": "安乐镇人民政府", "type": "政府", "level": "乡科级",
     "parent": "宁化县人民政府", "location": "福建省三明市宁化县安乐镇"},
    {"id": 19, "name": "水茜镇人民政府", "type": "政府", "level": "乡科级",
     "parent": "宁化县人民政府", "location": "福建省三明市宁化县水茜镇"},
    {"id": 20, "name": "城郊镇人民政府", "type": "政府", "level": "乡科级",
     "parent": "宁化县人民政府", "location": "福建省三明市宁化县城郊镇"},
    {"id": 21, "name": "城南镇人民政府", "type": "政府", "level": "乡科级",
     "parent": "宁化县人民政府", "location": "福建省三明市宁化县城南镇"},

    # 宁化县下辖4乡
    {"id": 22, "name": "济村乡人民政府", "type": "政府", "level": "乡科级",
     "parent": "宁化县人民政府", "location": "福建省三明市宁化县济村乡"},
    {"id": 23, "name": "方田乡人民政府", "type": "政府", "level": "乡科级",
     "parent": "宁化县人民政府", "location": "福建省三明市宁化县方田乡"},
    {"id": 24, "name": "中沙乡人民政府", "type": "政府", "level": "乡科级",
     "parent": "宁化县人民政府", "location": "福建省三明市宁化县中沙乡"},
    {"id": 25, "name": "河龙乡人民政府", "type": "政府", "level": "乡科级",
     "parent": "宁化县人民政府", "location": "福建省三明市宁化县河龙乡"},

    # 宁化县下辖1民族乡
    {"id": 26, "name": "治平畲族乡人民政府", "type": "政府", "level": "乡科级",
     "parent": "宁化县人民政府", "location": "福建省三明市宁化县治平畲族乡"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # Current positions
    {"person_id": 1, "org_id": 1, "title": "宁化县委书记",
     "start": "", "end": "present", "rank": "正处级",
     "note": "主持县委全面工作（待确认姓名）"},
    {"person_id": 2, "org_id": 2, "title": "宁化县县长",
     "start": "", "end": "present", "rank": "正处级",
     "note": "主持县政府全面工作（待确认姓名）"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "县委书记与县长在宁化县共事", "overlap_org": "宁化县", "overlap_period": "至今"},
]

# =========================================================================
# DB BUILD
# =========================================================================
def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS persons(
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS organizations(
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS positions(
        id INTEGER PRIMARY KEY,
        person_id INTEGER, org_id INTEGER, title TEXT,
        start TEXT, "end" TEXT, rank TEXT, note TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS relationships(
        id INTEGER PRIMARY KEY,
        person_a INTEGER, person_b INTEGER, type TEXT,
        context TEXT, overlap_org TEXT, overlap_period TEXT
    )""")

    for p in persons:
        c.execute("INSERT OR REPLACE INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"],
                   p["work_start"], p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        c.execute("INSERT OR REPLACE INTO organizations VALUES(?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for i, pos in enumerate(positions, 1):
        c.execute("INSERT OR REPLACE INTO positions VALUES(?,?,?,?,?,?,?,?)",
                  (i, pos["person_id"], pos["org_id"], pos["title"],
                   pos["start"], pos["end"], pos["rank"], pos["note"]))
    for i, rel in enumerate(relationships, 1):
        c.execute("INSERT OR REPLACE INTO relationships VALUES(?,?,?,?,?,?,?)",
                  (i, rel["person_a"], rel["person_b"], rel["type"],
                   rel["context"], rel["overlap_org"], rel["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")

# =========================================================================
# GEXF BUILD
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    title = (p.get("current_post") or "")
    if "县委书记" in title or "区委书记" in title:
        return "255,50,50"
    if "县长" in title or "区长" in title:
        return "50,100,255"
    return "100,100,100"

def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    return "200,200,200"

def is_top_leader(p):
    title = (p.get("current_post") or "")
    return "县委书记" in title or "县长" in title

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append('    <description>宁化县领导关系网络 — Party Secretary, County Mayor</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="level" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        role = esc(p.get("current_post", ""))
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{role}"/>')
        lines.append('          <attvalue for="2" value="county"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        period = f"{pos['start']}–{pos['end']}"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{period}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for rel in relationships:
        eid += 1
        ctx = esc(rel.get("context", ""))
        lines.append(f'      <edge id="e{eid}" source="p{rel["person_a"]}" target="p{rel["person_b"]}" label="{ctx}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rel["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")

# =========================================================================
# PERSON JSONS
# =========================================================================
def write_person_json(person_id, data):
    os.makedirs(PERSONS_DIR, exist_ok=True)
    fname = data["filename"]
    path = os.path.join(PERSONS_DIR, fname)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data["content"], f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {path}")

def build_person_jsons():
    # 县委书记 — 待查
    write_person_json(1, {
        "filename": "20260716-福建省-三明市-县委书记-待查.json",
        "content": {
            "schema_version": "1.0",
            "generated_at": "2026-07-16",
            "investigation_scope": {
                "province": "福建省",
                "city": "三明市",
                "region": "宁化县",
                "job": "县委书记",
                "task_id": "fujian_宁化县",
                "time_focus": "present"
            },
            "identity": {
                "person_id": "fujian_nignhua_daicha",
                "name": "（待查·县委书记）",
                "aliases": [],
                "gender": "",
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "",
                    "name_birthplace": "",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "宁化县委书记",
                "current_org": "中共宁化县委员会",
                "administrative_rank": "县处级",
                "as_of": "2026-07-16",
                "is_current_confirmed": False,
                "source_ids": []
            },
            "career_timeline": [],
            "organizations": [
                {"org_id": 1, "name": "中共宁化县委员会", "type": "党委", "level": "县处级",
                 "location": "福建省三明市宁化县"}
            ],
            "relationships": [],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "履历不详", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "因县委书记姓名未知，无法查证",
                 "date": "", "confidence": "unverified", "source_ids": []}
            ],
            "source_register": [],
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "unverified",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": "县委书记姓名及全部履历信息均未获取"
            },
            "open_questions": [
                {"priority": "critical", "question": "宁化县现任县委书记姓名",
                 "why_it_matters": "完成一把手身份确认",
                 "suggested_queries": ["宁化县 县委书记 现任 2025 2026",
                                      "宁化县委书记 任免"],
                 "last_attempted": "2026-07-16"},
                {"priority": "critical", "question": "宁化县委书记的出生日期、籍贯、教育背景",
                 "why_it_matters": "便于身份确认和与其他官员的关联分析",
                 "suggested_queries": ["宁化县委书记 简历"],
                 "last_attempted": "2026-07-16"},
                {"priority": "high", "question": "宁化县委书记的前任及继任信息",
                 "why_it_matters": "建立县委书记的职务变迁链条",
                 "suggested_queries": ["宁化县 历任县委书记"],
                 "last_attempted": "2026-07-16"}
            ]
        }
    })

    # 县长 — 待查
    write_person_json(2, {
        "filename": "20260716-福建省-三明市-县长-待查.json",
        "content": {
            "schema_version": "1.0",
            "generated_at": "2026-07-16",
            "investigation_scope": {
                "province": "福建省",
                "city": "三明市",
                "region": "宁化县",
                "job": "县长",
                "task_id": "fujian_宁化县",
                "time_focus": "present"
            },
            "identity": {
                "person_id": "fujian_nignhua_xianzhang_daicha",
                "name": "（待查·县长）",
                "aliases": [],
                "gender": "",
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "",
                    "name_birthplace": "",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "宁化县县长",
                "current_org": "宁化县人民政府",
                "administrative_rank": "县处级",
                "as_of": "2026-07-16",
                "is_current_confirmed": False,
                "source_ids": []
            },
            "career_timeline": [],
            "organizations": [
                {"org_id": 2, "name": "宁化县人民政府", "type": "政府", "level": "县处级",
                 "location": "福建省三明市宁化县"}
            ],
            "relationships": [],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "履历不详", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "因县长姓名未知，无法查证",
                 "date": "", "confidence": "unverified", "source_ids": []}
            ],
            "source_register": [],
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "unverified",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": "县长姓名及全部履历信息均未获取"
            },
            "open_questions": [
                {"priority": "critical", "question": "宁化县现任县长姓名",
                 "why_it_matters": "完成二把手身份确认",
                 "suggested_queries": ["宁化县 县长 现任 2025 2026",
                                      "宁化县人民政府 县长"],
                 "last_attempted": "2026-07-16"},
                {"priority": "critical", "question": "宁化县县长的出生日期、籍贯、教育背景",
                 "why_it_matters": "便于身份确认和与其他官员的关联分析",
                 "suggested_queries": ["宁化县长 简历"],
                 "last_attempted": "2026-07-16"},
                {"priority": "high", "question": "宁化县县长前任及继任信息",
                 "why_it_matters": "建立县长的职务变迁链条",
                 "suggested_queries": ["宁化县 历任县长"],
                 "last_attempted": "2026-07-16"}
            ]
        }
    })

# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    build_db()
    build_gexf()
    build_person_jsons()
    print("Done.")
