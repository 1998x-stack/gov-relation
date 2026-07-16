#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for 大田县 (Datian County), 三明市, 福建省.

Level: 县
Province: 福建省
Parent City: 三明市
Targets: 县委书记 & 县长

Key findings (as of July 2026):
- 县委书记: 吴茂生 (confirmed via Chinese Wikipedia 大田县 infobox)
- 县长: 待查 (not confirmed through available web research channels — web search tools
  were rate-limited and government website datian.gov.cn was unreachable)
- 大田县别称"岩城"，位于福建省中部，面积约2294平方公里
- 大田县下辖12镇、6乡、1农场，人口约29.95万（2020年七普）

Sources:
- Chinese Wikipedia: 大田县 entry — infobox lists 县委书记 = 吴茂生
- Government website: www.datian.gov.cn (unreachable during research)
- No other confirmed biographical details found for 吴茂生
- No confirmed information found for current 县长

Current as of: July 2026

Gaps:
- 吴茂生的出生年份、籍贯、教育背景和完整履历
- 现任县长姓名
- 历任前任县委书记和县长名单
- 县委常委领导班子完整名单
- 其他县领导详细信息
"""

import sqlite3, os, sys, json
from datetime import datetime

STAGING = os.path.dirname(os.path.abspath(__file__))
PROJECT_BASE = os.path.normpath(os.path.join(STAGING, "..", "..", ".."))
DB_PATH = os.path.join(STAGING, "大田县_network.db")
GEXF_PATH = os.path.join(STAGING, "大田县_network.gexf")
PERSONS_DIR = STAGING

AS_OF = "2026-07-16"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 吴茂生 — 大田县委书记 (confirmed via Wikipedia infobox)
    {"id": 1, "name": "吴茂生", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大田县委书记", "current_org": "中共大田县委员会",
     "source": "https://zh.wikipedia.org/wiki/%E5%A4%A7%E7%94%B0%E5%8E%BF",
     "notes": "县委书记，来自维基百科大田县信息框确认",
     "confidence": "confirmed"},

    # 县长 — 待查 (not found through available research)
    {"id": 2, "name": "（待查·县长）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大田县县长", "current_org": "大田县人民政府",
     "source": "",
     "notes": "县长姓名未能在公开资料中找到",
     "confidence": "unverified"},

    # ── Predecessors - 县委书记 ──
    # Note: No predecessor information found through available research channels

    # ── Predecessors - 县长 ──
    # Note: No predecessor information found through available research channels
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共大田县委员会", "type": "党委", "level": "县处级",
     "parent": "中共三明市委员会", "location": "福建省三明市大田县"},
    {"id": 2, "name": "大田县人民政府", "type": "政府", "level": "县处级",
     "parent": "三明市人民政府", "location": "福建省三明市大田县"},
    {"id": 3, "name": "大田县人大常委会", "type": "人大", "level": "县处级",
     "parent": "", "location": "福建省三明市大田县"},
    {"id": 4, "name": "政协大田县委员会", "type": "政协", "level": "县处级",
     "parent": "", "location": "福建省三明市大田县"},
    {"id": 5, "name": "大田县监察委员会", "type": "党委", "level": "县处级",
     "parent": "", "location": "福建省三明市大田县"},
    {"id": 6, "name": "中共三明市委员会", "type": "党委", "level": "地级",
     "parent": "中共福建省委员会", "location": "福建省三明市"},
    {"id": 7, "name": "三明市人民政府", "type": "政府", "level": "地级",
     "parent": "福建省人民政府", "location": "福建省三明市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 吴茂生 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "大田县委书记",
     "start": "", "end": "present", "rank": "县处级",
     "note": "具体任职起始时间待查"},

    # 县长(待查) — 县长
    {"person_id": 2, "org_id": 2, "title": "大田县县长",
     "start": "", "end": "present", "rank": "县处级",
     "note": "县长姓名及任职时间待查"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 县委书记 <-> 县长 (current cooperation, placeholder)
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "吴茂生（县委书记）与大田县县长在大田县共事",
     "overlap_org": "中共大田县委员会",
     "overlap_period": "当前", "strength": "strong",
     "direction": "undirected"},
]

# =========================================================================
# SQLITE BUILD
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
    lines.append('    <description>大田县领导关系网络 — Party Secretary (吴茂生), County Mayor (待查)</description>')
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
    # 吴茂生 — 县委书记
    write_person_json(1, {
        "filename": "20260716-福建省-三明市-县委书记-吴茂生.json",
        "content": {
            "schema_version": "1.0",
            "generated_at": "2026-07-16",
            "investigation_scope": {
                "province": "福建省",
                "city": "三明市",
                "region": "大田县",
                "job": "县委书记",
                "task_id": "fujian_大田县",
                "time_focus": "present"
            },
            "identity": {
                "person_id": "fujian_datian_wumaosheng",
                "name": "吴茂生",
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
                    "name_birth": "吴茂生",
                    "name_birthplace": "",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "大田县委书记",
                "current_org": "中共大田县委员会",
                "administrative_rank": "县处级",
                "as_of": "2026-07-16",
                "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {"start": "", "end": "present", "org": "中共大田县委员会",
                 "title": "大田县委书记", "level": "县处级",
                 "location": "福建省三明市大田县", "system": "party",
                 "rank": "", "is_key_promotion": True,
                 "notes": "任职起始时间待查",
                 "confidence": "confirmed", "source_ids": ["S001"]}
            ],
            "organizations": [
                {"org_id": 1, "name": "中共大田县委员会", "type": "党委",
                 "level": "县处级", "location": "福建省三明市大田县"}
            ],
            "relationships": [],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "履历不详",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "因公开信息有限，无法全面查证",
                 "date": "", "confidence": "unverified", "source_ids": []}
            ],
            "source_register": [
                {"id": "S001", "title": "大田县 - 维基百科",
                 "url": "https://zh.wikipedia.org/wiki/%E5%A4%A7%E7%94%B0%E5%8E%BF",
                 "publisher": "维基百科", "published_at": "",
                 "accessed_at": "2026-07-16",
                 "source_type": "encyclopedia", "reliability": "medium",
                 "notes": "维基百科大田县条目，信息框列出县委书记为吴茂生"}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": "吴茂生的出生年份、籍贯、教育背景和完整履历均未获取"
            },
            "open_questions": [
                {"priority": "critical", "question": "吴茂生的出生日期、籍贯、教育背景",
                 "why_it_matters": "便于身份确认和与其他官员的关联分析",
                 "suggested_queries": ["吴茂生 简历 大田县", "吴茂生 百度百科"],
                 "last_attempted": "2026-07-16"},
                {"priority": "critical", "question": "吴茂生任大田县委书记前的工作经历",
                 "why_it_matters": "理解其职业路径和培养模式",
                 "suggested_queries": ["吴茂生 任职经历", "吴茂生 此前 担任"],
                 "last_attempted": "2026-07-16"},
                {"priority": "high", "question": "吴茂生的前任县委书记及去向",
                 "why_it_matters": "建立县委书记的职务变迁链条",
                 "suggested_queries": ["大田县 前任县委书记", "大田县 历任县委书记"],
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
                "region": "大田县",
                "job": "县长",
                "task_id": "fujian_大田县",
                "time_focus": "present"
            },
            "identity": {
                "person_id": "fujian_datian_xianzhang_daicha",
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
                "current_post": "大田县县长",
                "current_org": "大田县人民政府",
                "administrative_rank": "县处级",
                "as_of": "2026-07-16",
                "is_current_confirmed": False,
                "source_ids": []
            },
            "career_timeline": [],
            "organizations": [
                {"org_id": 2, "name": "大田县人民政府", "type": "政府",
                 "level": "县处级", "location": "福建省三明市大田县"}
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
                {"priority": "critical", "question": "大田县现任县长姓名",
                 "why_it_matters": "完成二把手身份确认",
                 "suggested_queries": ["大田县 县长 现任 2025 2026", "大田县人民政府 县长"],
                 "last_attempted": "2026-07-16"},
                {"priority": "critical", "question": "大田县县长的工作经历",
                 "why_it_matters": "评估其工作经验和专业背景",
                 "suggested_queries": ["大田县长 简历"],
                 "last_attempted": "2026-07-16"},
                {"priority": "high", "question": "大田县县长的前任及去向",
                 "why_it_matters": "建立县长的职务变迁链条",
                 "suggested_queries": ["大田县 历任县长"],
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
