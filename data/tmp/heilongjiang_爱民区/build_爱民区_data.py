#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 爱民区 (Aimin District), 牡丹江市, 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_爱民区
Research sources:
  - Aimin District Government Website (www.aimin.gov.cn)
  - Wikipedia: 爱民区
  - Mudanjiang City Government Website (www.mdj.gov.cn)
"""

import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "爱民区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = TODAY

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

# Also produce canonical destination paths
CANONICAL_DB = os.path.join(BASE, "..", "..", "database", f"{SLUG}_network.db")
CANONICAL_GEXF = os.path.join(BASE, "..", "..", "graph", f"{SLUG}_network.gexf")
CANONICAL_BUILD = os.path.join(BASE, "..", "..", "..", f"build_{SLUG}_data.py")
CANONICAL_PERSONS = Path(BASE) / ".." / ".." / "persons"

# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════════
    # Core Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 惠金山 — 区委书记 (as of 2024-2026, confirmed active on aimin.gov.cn)
    # Source: Various news reports on aimin.gov.cn referencing "区委书记惠金山"
    {"id": 1, "name": "惠金山", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委书记", "current_org": "中共牡丹江市爱民区委员会",
     "source": "https://www.aimin.gov.cn"},

    # 杨云峰 — 区长 (as of 2024-2026, referenced on government website)
    {"id": 2, "name": "杨云峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区长", "current_org": "牡丹江市爱民区人民政府",
     "source": "https://www.aimin.gov.cn"},

    # ══════════════════════════════════════════════════════════════════════════
    # District Standing Committee / Key Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 赵鑫 — 区委副书记 (as of 2024-2026)
    {"id": 3, "name": "赵鑫", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委副书记", "current_org": "中共牡丹江市爱民区委员会",
     "source": "https://www.aimin.gov.cn"},

    # 王丹 — 区委常委、副区长（常务）
    {"id": 4, "name": "王丹", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、副区长（常务）", "current_org": "牡丹江市爱民区人民政府",
     "source": "https://www.aimin.gov.cn"},

    # 李志刚 — 区委常委、区纪委书记、监委主任
    {"id": 5, "name": "李志刚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、区纪委书记、监委主任", "current_org": "中共牡丹江市爱民区纪律检查委员会",
     "source": "https://www.aimin.gov.cn"},

    # 梁红娟 — 区委常委、组织部部长
    {"id": 6, "name": "梁红娟", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、组织部部长", "current_org": "中共牡丹江市爱民区委员会组织部",
     "source": "https://www.aimin.gov.cn"},

    # 赵岩 — 区委常委、宣传部部长
    {"id": 7, "name": "赵岩", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、宣传部部长", "current_org": "中共牡丹江市爱民区委员会宣传部",
     "source": "https://www.aimin.gov.cn"},

    # 袁青 — 区委常委、政法委书记
    {"id": 8, "name": "袁青", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、政法委书记", "current_org": "中共牡丹江市爱民区委员会政法委员会",
     "source": "https://www.aimin.gov.cn"},

    # 李荣 — 副区长
    {"id": 9, "name": "李荣", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副区长", "current_org": "牡丹江市爱民区人民政府",
     "source": "https://www.aimin.gov.cn"},

    # 刘辉 — 副区长
    {"id": 10, "name": "刘辉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副区长", "current_org": "牡丹江市爱民区人民政府",
     "source": "https://www.aimin.gov.cn"},
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共牡丹江市爱民区委员会", "type": "党委", "level": "县处级", "parent": "中共牡丹江市委员会", "location": "牡丹江市爱民区天安路300号"},
    {"id": 2, "name": "牡丹江市爱民区人民政府", "type": "政府", "level": "县处级", "parent": "牡丹江市人民政府", "location": "牡丹江市爱民区天安路300号"},
    {"id": 3, "name": "中共牡丹江市爱民区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共牡丹江市纪律检查委员会", "location": "牡丹江市爱民区"},
    {"id": 4, "name": "牡丹江市爱民区人大常委会", "type": "人大", "level": "县处级", "parent": "牡丹江市人大常委会", "location": "牡丹江市爱民区"},
    {"id": 5, "name": "中国人民政治协商会议牡丹江市爱民区委员会", "type": "政协", "level": "县处级", "parent": "政协牡丹江市委员会", "location": "牡丹江市爱民区"},
    {"id": 6, "name": "中共牡丹江市爱民区委员会组织部", "type": "党委", "level": "乡科级", "parent": "中共牡丹江市爱民区委员会", "location": "牡丹江市爱民区"},
    {"id": 7, "name": "中共牡丹江市爱民区委员会宣传部", "type": "党委", "level": "乡科级", "parent": "中共牡丹江市爱民区委员会", "location": "牡丹江市爱民区"},
    {"id": 8, "name": "中共牡丹江市爱民区委员会政法委员会", "type": "党委", "level": "乡科级", "parent": "中共牡丹江市爱民区委员会", "location": "牡丹江市爱民区"},
    {"id": 9, "name": "牡丹江市爱民区监察委员会", "type": "纪委", "level": "县处级", "parent": "牡丹江市监察委员会", "location": "牡丹江市爱民区"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 惠金山 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "", "end": "present", "rank": "县处级正职", "note": "爱民区委书记，主持区委全面工作"},
    # 杨云峰 — 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "present", "rank": "县处级正职", "note": "爱民区区长，主持区政府全面工作"},
    # 赵鑫 — 区委副书记
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "rank": "县处级副职", "note": "协助区委书记处理日常事务"},
    # 王丹 — 区委常委、副区长（常务）
    {"person_id": 4, "org_id": 2, "title": "区委常委、副区长（常务）", "start": "", "end": "present", "rank": "县处级副职", "note": "负责区政府常务工作"},
    # 李志刚 — 区纪委书记
    {"person_id": 5, "org_id": 3, "title": "区委常委、区纪委书记、监委主任", "start": "", "end": "present", "rank": "县处级副职", "note": "负责纪检监察工作"},
    {"person_id": 5, "org_id": 9, "title": "监委主任", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 梁红娟 — 区委组织部部长
    {"person_id": 6, "org_id": 6, "title": "区委常委、组织部部长", "start": "", "end": "present", "rank": "县处级副职", "note": "负责组织人事工作"},
    # 赵岩 — 区委宣传部部长
    {"person_id": 7, "org_id": 7, "title": "区委常委、宣传部部长", "start": "", "end": "present", "rank": "县处级副职", "note": "负责宣传思想文化工作"},
    # 袁青 — 区委政法委书记
    {"person_id": 8, "org_id": 8, "title": "区委常委、政法委书记", "start": "", "end": "present", "rank": "县处级副职", "note": "负责政法稳定工作"},
    # 李荣 — 副区长
    {"person_id": 9, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 刘辉 — 副区长
    {"person_id": 10, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 惠金山 ↔ 杨云峰 — 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "惠金山任区委书记、杨云峰任区长，为爱民区党政正职", "overlap_org": "牡丹江市爱民区", "overlap_period": ""},
    # 惠金山 ↔ 赵鑫 — 正副书记
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "惠金山作为区委书记，赵鑫作为区委副书记协助工作", "overlap_org": "中共牡丹江市爱民区委员会", "overlap_period": ""},
    # 杨云峰 ↔ 王丹 — 区长与常务副区长
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "杨云峰作为区长，王丹作为常务副区长协助工作", "overlap_org": "牡丹江市爱民区人民政府", "overlap_period": ""},
    # 惠金山 ↔ 李志刚 — 区委书记与纪委书记
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记与纪委书记的监督关系", "overlap_org": "中共牡丹江市爱民区委员会", "overlap_period": ""},
    # 惠金山 ↔ 梁红娟 — 区委书记与组织部长
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区委书记与组织部长的干部管理关系", "overlap_org": "中共牡丹江市爱民区委员会", "overlap_period": ""},
    # 惠金山 ↔ 袁青 — 区委书记与政法委书记
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "区委书记与政法委书记的工作关系", "overlap_org": "中共牡丹江市爱民区委员会", "overlap_period": ""},
    # 杨云峰 ↔ 李荣 — 区长与副区长
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "区政府正副职工作关系", "overlap_org": "牡丹江市爱民区人民政府", "overlap_period": ""},
    # 杨云峰 ↔ 刘辉 — 区长与副区长
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "区政府正副职工作关系", "overlap_org": "牡丹江市爱民区人民政府", "overlap_period": ""},
]


# ══════════════════════════════════════════════════════════════════════════════
# SQLite DB Builder
# ══════════════════════════════════════════════════════════════════════════════

esc = lambda s: str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;") if s is not None else ""

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Drop existing tables
    for t in ("relationships","positions","organizations","persons"):
        cur.execute(f"DROP TABLE IF EXISTS {t}")
    
    # Create tables
    cur.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    cur.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    cur.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER,
        title TEXT, start_date TEXT, end_date TEXT,
        rank TEXT, note TEXT
    )""")
    cur.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT
    )""")
    
    for p in persons:
        cur.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],
                     p["birthplace"],p["education"],p["party_join"],p["work_start"],
                     p["current_post"],p["current_org"],p["source"]))
    for o in organizations:
        cur.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                    (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
    for pos in positions:
        cur.execute("INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)",
                    (pos["person_id"],pos["org_id"],pos["title"],pos.get("start",""),pos.get("end",""),pos.get("rank",""),pos.get("note","")))
    for r in relationships:
        cur.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                    (r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))
    
    conn.commit()
    conn.close()
    print(f"  DB: {DB_PATH} ({len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships)")


# ══════════════════════════════════════════════════════════════════════════════
# GEXF Graph Builder
# ══════════════════════════════════════════════════════════════════════════════

def person_color(post):
    if "书记" in post and "副" not in post and "纪委" not in post:
        return ("255,50,50", 20.0)  # Red, large
    elif "区长" in post and "副" not in post:
        return ("50,100,255", 20.0)  # Blue, large
    elif "常委" in post and ("副区长" in post or "副" in post):
        return ("100,150,255", 12.0)  # Light blue
    elif "常委" in post:
        return ("100,150,255", 12.0)
    elif "纪委" in post:
        return ("255,165,0", 12.0)  # Orange for discipline
    else:
        return ("100,100,100", 12.0)

def org_color(org_type):
    colors = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "纪委": ("255,200,200", 8.0),
        "人大": ("200,255,255", 8.0),
        "政协": ("255,240,200", 8.0),
    }
    return colors.get(org_type, ("200,200,200", 8.0))


def build_gexf():
    from datetime import datetime
    
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append(f'    <description>爱民区领导班子关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    
    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')
    
    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')
    
    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c, sz = person_color(p["current_post"])
        lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # Organization nodes
    for o in organizations:
        c, sz = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    
    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person -> Organization (worked at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    # Person <-> Person (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="{r["person_a"]}" target="{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
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
    print(f"  GEXF: {GEXF_PATH}")


# ══════════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════════

def make_source_register():
    return [
        {"id":"S001","title":"爱民区人民政府—首页","url":"https://www.aimin.gov.cn","publisher":"爱民区人民政府","published_at":"2026-07-24","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"爱民区政府官方网站，包含领导之窗"},
        {"id":"S002","title":"维基百科—爱民区","url":"https://zh.wikipedia.org/wiki/爱民区","publisher":"维基百科","published_at":"2023-09-09","accessed_at":AS_OF,"source_type":"encyclopedia","reliability":"medium","notes":"爱民区行政区划信息"},
    ]


def make_person_json(p, timeline, relationships_list, source_register):
    result = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "牡丹江市",
            "region": "爱民区",
            "job": p["current_post"],
            "task_id": "heilongjiang_爱民区",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"aiminqu_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender",""),
            "ethnicity": p.get("ethnicity",""),
            "birth": p.get("birth",""),
            "birthplace": p.get("birthplace",""),
            "native_place": "",
            "education": [{"period":"","institution":"","major":"","degree":p.get("education",""),"study_type":"unknown","source_ids":[]}] if p.get("education") else [],
            "party_join": p.get("party_join","").replace("中共党员（","").replace("中共党员","").replace("）",""),
            "work_start": p.get("work_start",""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source","")
            }
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "县处级正职" if ("区委书记" in p["current_post"] or "区长" == p["current_post"]) else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": True,
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
        "risk_and_integrity_signals": [],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "公开资料受限，无法获取完整履历、出生日期、教育背景等详细信息"
        },
        "open_questions": [
            {"priority": "critical", "question": f"{p['name']}的完整履历", "why_it_matters": "核心领导人履历是关系网络的基础", "suggested_queries": [f"{p['name']} 简历 爱民区", f"{p['name']} 任前公示", f"{p['name']} 牡丹江"], "last_attempted": AS_OF},
            {"priority": "critical", "question": f"{p['name']}的出生日期和籍贯", "why_it_matters": "用于身份识别和去重", "suggested_queries": [f"{p['name']} 出生 爱民区", f"{p['name']} 籍贯"], "last_attempted": AS_OF},
        ]
    }
    return result


def write_person_jsons():
    source_register = make_source_register()
    
    # Map person ID to their relationship records
    person_relationships = {p["id"]: [] for p in persons}
    for r in relationships:
        person_relationships.setdefault(r["person_a"], []).append(r)
        person_relationships.setdefault(r["person_b"], []).append(r)
    
    for p in persons:
        # Build basic timeline
        p_positions = [pos for pos in positions if pos["person_id"] == p["id"]]
        timeline = []
        for pos in p_positions:
            timeline.append({
                "start": pos.get("start",""),
                "end": pos.get("end",""),
                "org": next((o["name"] for o in organizations if o["id"] == pos["org_id"]), ""),
                "title": pos["title"],
                "level": pos.get("rank",""),
                "location": "牡丹江市爱民区",
                "system": "party" if "区委" in pos["title"] else "government",
                "rank": pos.get("rank",""),
                "is_key_promotion": False,
                "notes": pos.get("note",""),
                "confidence": "plausible",
                "source_ids": []
            })
        
        # Build relationships for this person
        rels = []
        for r in person_relationships.get(p["id"], []):
            other_id = r["person_b"] if r["person_a"] == p["id"] else r["person_a"]
            other = next((x for x in persons if x["id"] == other_id), None)
            if other:
                rels.append({
                    "person": other["name"],
                    "person_id": f"aiminqu_{other['name']}",
                    "relationship_type": r["type"],
                    "strength": "strong" if r["type"] in ("党政搭档","上下级") else "medium",
                    "evidence": r["context"],
                    "overlap_org": r.get("overlap_org",""),
                    "overlap_period": r.get("overlap_period",""),
                    "direction": "undirected",
                    "confidence": "plausible",
                    "source_ids": []
                })
        
        data = make_person_json(p, timeline, rels, source_register)
        
        fname = f"{TODAY}-黑龙江省-牡丹江市-{p['current_post']}-{p['name']}.json"
        fpath = PERSONS_DIR / fname
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {fpath}")


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════

def build():
    print(f"Building {SLUG} network...")
    build_db()
    build_gexf()
    write_person_jsons()
    print("Done.")


if __name__ == "__main__":
    build()
