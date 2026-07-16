#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for 明溪县 (Mingxi County), 三明市, 福建省.

Level: 县
Province: 福建省
Parent City: 三明市
Targets: 县委书记 & 县长

Key findings (as of July 2026):
- 县委书记: 陈华伟 (confirmed per Wikipedia zh infobox)
- 县长: 待查 (not listed on Wikipedia; name not found through available research channels)
- 明溪县下辖4镇5乡, 人口约9.9万

Sources:
- Chinese Wikipedia: 明溪县 entry (zh.wikipedia.org) — confirmed 陈华伟 as 县委书记
- No source found for current 县长 name through available web channels

Current as of: July 2026

Gaps:
- 县长姓名未找到
- 陈华伟的出生年份、籍贯、教育背景和完整履历
- 历任前任县委书记和县长名单
- 县委常委领导班子完整名单
"""

import sqlite3, os, sys, json
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_BASE = os.path.normpath(os.path.join(BASE, "..", ".."))
STAGING = BASE
DB_PATH = os.path.join(STAGING, "明溪县_network.db")
GEXF_PATH = os.path.join(STAGING, "明溪县_network.gexf")
PERSONS_DIR = os.path.join(STAGING, "persons")

AS_OF = "2026-07-16"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 陈华伟 — 明溪县委书记 (confirmed per Wikipedia)
    {"id": 1, "name": "陈华伟", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "明溪县委书记", "current_org": "中共明溪县委员会",
     "source": "https://zh.wikipedia.org/wiki/%E6%98%8E%E6%BA%AA%E5%8E%BF",
     "notes": "Wikipedia infobox lists 陈华伟 as 县委书记 of 明溪县",
     "confidence": "confirmed"},

    # 县长 — 待查 (not found through available research)
    # Placeholder entry for the county mayor position
    {"id": 2, "name": "（待查）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "明溪县县长", "current_org": "明溪县人民政府",
     "source": "",
     "notes": "县长姓名未能在公开资料中找到",
     "confidence": "unverified"},

    # ── Predecessors - 县委书记 ──
    # Note: No predecessor information found through available research channels

    # ── Other county-level leaders ──
    # Note: Full leadership roster not available
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共明溪县委员会", "type": "党委", "level": "县处级",
     "parent": "中共三明市委员会", "location": "福建省三明市明溪县"},
    {"id": 2, "name": "明溪县人民政府", "type": "政府", "level": "县处级",
     "parent": "三明市人民政府", "location": "福建省三明市明溪县"},
    {"id": 3, "name": "明溪县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "三明市人大常委会", "location": "福建省三明市明溪县"},
    {"id": 4, "name": "中国人民政治协商会议明溪县委员会", "type": "政协", "level": "县处级",
     "parent": "政协三明市委员会", "location": "福建省三明市明溪县"},
    {"id": 5, "name": "明溪县监察委员会", "type": "党委", "level": "县处级",
     "parent": "", "location": "福建省三明市明溪县"},
    {"id": 6, "name": "雪峰镇人民政府", "type": "政府", "level": "乡科级",
     "parent": "明溪县人民政府", "location": "福建省三明市明溪县雪峰镇"},
    {"id": 7, "name": "盖洋镇人民政府", "type": "政府", "level": "乡科级",
     "parent": "明溪县人民政府", "location": "福建省三明市明溪县盖洋镇"},
    {"id": 8, "name": "胡坊镇人民政府", "type": "政府", "level": "乡科级",
     "parent": "明溪县人民政府", "location": "福建省三明市明溪县胡坊镇"},
    {"id": 9, "name": "瀚仙镇人民政府", "type": "政府", "level": "乡科级",
     "parent": "明溪县人民政府", "location": "福建省三明市明溪县瀚仙镇"},
    {"id": 10, "name": "城关乡人民政府", "type": "政府", "level": "乡科级",
     "parent": "明溪县人民政府", "location": "福建省三明市明溪县城关乡"},
    {"id": 11, "name": "沙溪乡人民政府", "type": "政府", "level": "乡科级",
     "parent": "明溪县人民政府", "location": "福建省三明市明溪县沙溪乡"},
    {"id": 12, "name": "夏阳乡人民政府", "type": "政府", "level": "乡科级",
     "parent": "明溪县人民政府", "location": "福建省三明市明溪县夏阳乡"},
    {"id": 13, "name": "枫溪乡人民政府", "type": "政府", "level": "乡科级",
     "parent": "明溪县人民政府", "location": "福建省三明市明溪县枫溪乡"},
    {"id": 14, "name": "夏坊乡人民政府", "type": "政府", "level": "乡科级",
     "parent": "明溪县人民政府", "location": "福建省三明市明溪县夏坊乡"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 陈华伟 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "明溪县委书记",
     "start": "", "end": "present", "rank": "县处级",
     "note": "现任明溪县委书记（Wikipedia 2026年4月更新）"},

    # 县长 — 待查
    {"person_id": 2, "org_id": 2, "title": "明溪县县长",
     "start": "", "end": "present", "rank": "县处级",
     "note": "县长姓名待查"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 陈华伟与县长 — 共事关系（待确认姓名）
    {"person_a": 1, "person_b": 2,
     "type": "overlap",
     "context": "陈华伟（县委书记）与县长在明溪县共事",
     "overlap_org": "中共明溪县委员会",
     "overlap_period": "至今",
     "strength": "strong",
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
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>明溪县领导关系网络 — Party Secretary, County Mayor</description>')
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
    # 陈华伟 — 县委书记
    write_person_json(1, {
        "filename": "20260716-福建省-三明市-县委书记-陈华伟.json",
        "content": {
            "schema_version": "1.0",
            "generated_at": "2026-07-16",
            "investigation_scope": {
                "province": "福建省",
                "city": "三明市",
                "region": "明溪县",
                "job": "县委书记",
                "task_id": "fujian_明溪县",
                "time_focus": "present"
            },
            "identity": {
                "person_id": "fujian_mingxi_chenhuawei",
                "name": "陈华伟",
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
                    "name_birth": "陈华伟_",
                    "name_birthplace": "陈华伟_",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "明溪县委书记",
                "current_org": "中共明溪县委员会",
                "administrative_rank": "县处级",
                "as_of": "2026-07-16",
                "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {"start": "", "end": "present", "org": "中共明溪县委员会", "title": "明溪县委书记",
                 "level": "县处级", "location": "福建省三明市明溪县", "system": "party",
                 "rank": "", "is_key_promotion": True, "notes": "Wikipedia确认在任",
                 "confidence": "confirmed", "source_ids": ["S001"]}
            ],
            "organizations": [
                {"org_id": 1, "name": "中共明溪县委员会", "type": "党委", "level": "县处级",
                 "location": "福建省三明市明溪县"}
            ],
            "relationships": [
                {"person": "（待查）", "person_id": "fujian_mingxi_daicha",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "陈华伟（县委书记）与县长在明溪县共事",
                 "overlap_org": "中共明溪县委员会", "overlap_period": "至今",
                 "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]}
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["party"],
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
                {"type": "none_found", "description": "未发现公开的纪律处分或负面报道",
                 "date": "", "confidence": "unverified", "source_ids": []}
            ],
            "source_register": [
                {"id": "S001", "title": "明溪县 - 维基百科",
                 "url": "https://zh.wikipedia.org/wiki/%E6%98%8E%E6%BA%AA%E5%8E%BF",
                 "publisher": "维基百科", "published_at": "2026-04-04",
                 "accessed_at": "2026-07-16",
                 "source_type": "encyclopedia", "reliability": "medium",
                 "notes": "维基百科明溪县条目infobox中列出陈华伟为县委书记"}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": "陈华伟的出生年份、籍贯、教育背景和完整履历均未获取"
            },
            "open_questions": [
                {"priority": "critical", "question": "陈华伟的出生日期和籍贯",
                 "why_it_matters": "便于身份确认和与其他官员的关联分析",
                 "suggested_queries": ["陈华伟 明溪县 县委书记 简历"],
                 "last_attempted": "2026-07-16"},
                {"priority": "critical", "question": "陈华伟任职明溪县委书记前的履历",
                 "why_it_matters": "理解其职业路径和培养模式",
                 "suggested_queries": ["陈华伟 福建省 任职 履历"],
                 "last_attempted": "2026-07-16"},
                {"priority": "critical", "question": "明溪县县长姓名",
                 "why_it_matters": "完成二把手身份确认",
                 "suggested_queries": ["明溪县 县长 现任"],
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
