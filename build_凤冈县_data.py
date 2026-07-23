#!/usr/bin/env python3
"""凤冈县（遵义市）领导班子关系网络数据生成脚本.

Targets: 县委书记 马华, 县长 陈健
Data as of: 2026-07-23
Sources: 凤冈县人民政府官网 (www.gzfenggang.gov.cn), official news reports
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

TASK_ID = "guizhou_凤冈县"
SLUG = "凤冈县"
AS_OF = "2026-07-23"
PROVINCE = "贵州省"
PARENT_CITY = "遵义市"

BASE = os.path.join("data", "tmp", "guizhou_凤冈县")
_BASE_OVERRIDE = os.environ.get("FENGGANG_BASE")
if _BASE_OVERRIDE:
    BASE = _BASE_OVERRIDE

DB_PATH = os.path.join(BASE, "凤冈县_network.db")
GEXF_PATH = os.path.join(BASE, "凤冈县_network.gexf")
PERSONS_DIR = os.path.join(BASE, "persons")
os.makedirs(PERSONS_DIR, exist_ok=True)

# ── Data ──────────────────────────────────────────────────────────────────────

persons = [
    # 1 - 县委书记
    {
        "id": 1,
        "name": "马华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凤冈县委书记",
        "current_org": "中共凤冈县委员会",
        "source": "https://www.gzfenggang.gov.cn/ (confirmed by news: 马华开展七一走访慰问活动)",
    },
    # 2 - 县长
    {
        "id": 2,
        "name": "陈健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-05",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "凤冈县委副书记、县人民政府县长",
        "current_org": "凤冈县人民政府",
        "source": "https://www.gzfenggang.gov.cn/zwgk/ldzc_5982516/202603/t20260320_89890693.html",
    },
    # 3 - 常务副县长
    {
        "id": 3,
        "name": "任达林",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1973-10",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "凤冈县委常委、副县长（常务）",
        "current_org": "凤冈县人民政府",
        "source": "https://www.gzfenggang.gov.cn/zwgk/ldzc_5982516/202503/t20250326_87272305.html",
    },
    # 4 - 副县长
    {
        "id": 4,
        "name": "张德晏",
        "gender": "男",
        "ethnicity": "仡佬族",
        "birth": "1985-04",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "凤冈县副县长",
        "current_org": "凤冈县人民政府",
        "source": "https://www.gzfenggang.gov.cn/zwgk/ldzc_5982516/202503/t20250326_87272301.html",
    },
    # 5 - 副县长/公安局长
    {
        "id": 5,
        "name": "刘明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-12",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "凤冈县副县长、县公安局局长",
        "current_org": "凤冈县人民政府",
        "source": "https://www.gzfenggang.gov.cn/zwgk/ldzc_5982516/202503/t20250326_87272300.html",
    },
    # 6 - 副县长（挂职）
    {
        "id": 6,
        "name": "余航夫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1990-07",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "凤冈县副县长（挂职）",
        "current_org": "凤冈县人民政府",
        "source": "https://www.gzfenggang.gov.cn/zwgk/ldzc_5982516/202503/t20250326_87272299.html",
    },
    # 7 - 副县长
    {
        "id": 7,
        "name": "韩先军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987-07",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "凤冈县副县长",
        "current_org": "凤冈县人民政府",
        "source": "https://www.gzfenggang.gov.cn/zwgk/ldzc_5982516/202512/t20251225_89087186.html",
    },
    # 8 - 县人大常委会主任（待确认）
    {
        "id": 8,
        "name": "【待查】人大主任",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凤冈县人大常委会主任",
        "current_org": "凤冈县人大常委会",
        "source": "姓名待确认",
    },
    # 9 - 县政协主席（待确认）
    {
        "id": 9,
        "name": "【待查】政协主席",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "凤冈县政协主席",
        "current_org": "凤冈县政协",
        "source": "姓名待确认",
    },
]

organizations = [
    {"id": 1, "name": "中共凤冈县委员会", "type": "党委", "level": "县级", "parent": PARENT_CITY, "location": "凤冈县"},
    {"id": 2, "name": "凤冈县人民政府", "type": "政府", "level": "县级", "parent": PARENT_CITY, "location": "凤冈县"},
    {"id": 3, "name": "凤冈县人大常委会", "type": "人大", "level": "县级", "parent": PARENT_CITY, "location": "凤冈县"},
    {"id": 4, "name": "凤冈县政协", "type": "政协", "level": "县级", "parent": PARENT_CITY, "location": "凤冈县"},
    {"id": 5, "name": "凤冈县纪委监委", "type": "纪委", "level": "县级", "parent": PARENT_CITY, "location": "凤冈县"},
    {"id": 6, "name": "凤冈县委组织部", "type": "党委部门", "level": "县级", "parent": PARENT_CITY, "location": "凤冈县"},
    {"id": 7, "name": "凤冈县委宣传部", "type": "党委部门", "level": "县级", "parent": PARENT_CITY, "location": "凤冈县"},
    {"id": 8, "name": "凤冈县政法委", "type": "党委部门", "level": "县级", "parent": PARENT_CITY, "location": "凤冈县"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正县级", "note": "confirmed by official news reports"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "正县级", "note": "confirmed by official profile"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "正县级", "note": "confirmed by official profile"},
    {"person_id": 3, "org_id": 2, "title": "县委常委、副县长（常务）", "start": "", "end": "present", "rank": "副县级", "note": "confirmed by official profile"},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "confirmed by official profile"},
    {"person_id": 5, "org_id": 2, "title": "副县长、县公安局局长", "start": "", "end": "present", "rank": "副县级", "note": "confirmed by official profile"},
    {"person_id": 6, "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "present", "rank": "副县级", "note": "外出挂职，挂职期间不参与分工"},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": "confirmed by official profile"},
    {"person_id": 8, "org_id": 3, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "正县级", "note": "姓名待确认"},
    {"person_id": 9, "org_id": 4, "title": "县政协主席", "start": "", "end": "present", "rank": "正县级", "note": "姓名待确认"},
]

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "马华（县委书记）与陈健（县长）在凤冈县委常委会共事",
        "overlap_org": "中共凤冈县委员会",
        "overlap_period": "至2026年7月",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "马华（县委书记）与任达林（县委常委、常务副县长）上下级关系",
        "overlap_org": "中共凤冈县委员会",
        "overlap_period": "至2026年7月",
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "陈健（县长）与任达林（常务副县长）在县政府共事",
        "overlap_org": "凤冈县人民政府",
        "overlap_period": "至2026年7月",
    },
    {
        "person_a": 2,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "陈健（县长）与张德晏（副县长）在县政府共事",
        "overlap_org": "凤冈县人民政府",
        "overlap_period": "至2026年7月",
    },
    {
        "person_a": 2,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "陈健（县长）与刘明（副县长、公安局长）在县政府共事",
        "overlap_org": "凤冈县人民政府",
        "overlap_period": "至2026年7月",
    },
    {
        "person_a": 2,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "陈健（县长）与韩先军（副县长）在县政府共事",
        "overlap_org": "凤冈县人民政府",
        "overlap_period": "至2026年7月",
    },
]

# ── Build Functions ───────────────────────────────────────────────────────────

def build_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
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
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute(
            "INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]),
        )

    for o in organizations:
        c.execute(
            "INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
            (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o["location"]),
        )

    for pos in positions:
        c.execute(
            "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]),
        )

    for r in relationships:
        c.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?, ?, ?, ?, ?, ?)",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]),
        )

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    role_lower = p.get("current_post", "").lower()
    if "书记" in role_lower and ("县委" in role_lower or "县委书记" in role_lower):
        return "255,50,50"
    elif "县长" in role_lower or ("长" in role_lower and "政府" in role_lower):
        return "50,100,255"
    elif "政协" in role_lower:
        return "255,240,200"
    elif "人大" in role_lower:
        return "200,255,255"
    else:
        return "100,100,100"


def org_color(o):
    t = o.get("type", "")
    if "党委" in t and "纪委" not in t:
        return "255,200,200"
    elif "政府" in t:
        return "200,200,255"
    elif "人大" in t:
        return "200,255,255"
    elif "政协" in t:
        return "255,240,200"
    elif "纪委" in t:
        return "255,165,0"
    else:
        return "200,200,200"


def is_top_leader(p):
    return p["id"] in (1, 2)


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append(f'    <description>{SLUG}（{PROVINCE}{PARENT_CITY}）领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="location" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="凤冈县"/>')
        lines.append('        </attvalues>')
        r, g, b = c.split(",")
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("parent", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(o.get("location", ""))}"/>')
        lines.append('        </attvalues>')
        r, g, b = c.split(",")
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        person = next(p for p in persons if p["id"] == pos["person_id"])
        org = next(o for o in organizations if o["id"] == pos["org_id"])
        weight = "1.5" if "书记" in pos["title"] and "县委" in pos["title"] else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("note", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos.get("start", "") or "")}~{esc(pos.get("end", "") or "")}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF graph created: {GEXF_PATH}")


def write_person_json():
    person_json_template = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": PROVINCE,
            "city": PARENT_CITY,
            "region": SLUG,
            "job": "",
            "task_id": TASK_ID,
            "time_focus": "2026"
        },
        "identity": {
            "person_id": "",
            "name": "",
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
            "current_post": "",
            "current_org": "",
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
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
            "promotion_velocity": {
                "summary": "",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [
            {
                "id": "S001",
                "title": "凤冈县人民政府领导之窗",
                "url": "https://www.gzfenggang.gov.cn/zwgk/ldzc_5982516/",
                "publisher": "凤冈县人民政府",
                "published_at": "2026-03-20",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认陈健为县长、任达林为常务副县长等政府领导班子"
            },
            {
                "id": "S002",
                "title": "凤冈县新闻",
                "url": "https://www.gzfenggang.gov.cn/",
                "publisher": "凤冈县人民政府",
                "published_at": "2026-07-23",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认马华为县委书记（马华开展七一走访慰问活动报道）"
            }
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "马华完整履历（出生年份、籍贯、教育背景）和多名县委常委成员身份未知"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "马华的完整履历（包括出生年份、籍贯、教育背景、早年任职经历）",
                "why_it_matters": "核心领导人，需完整身份信息",
                "suggested_queries": ["马华 简历 凤冈", "马华 凤冈县委书记 任前公示", "马华 遵义"],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": "陈健任县长前的完整履历（此前任职经历）",
                "why_it_matters": "政府首长，需完整身份信息",
                "suggested_queries": ["陈健 简历 凤冈", "陈健 任前公示", "陈健 遵义"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "县委常委班子全体成员名单（包括县委副书记、纪委书记、组织部长、宣传部长、统战部长、政法委书记、县委办主任等）",
                "why_it_matters": "缺乏县委领导班子信息",
                "suggested_queries": ["凤冈县 县委常委 名单", "凤冈县委 领导分工"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "马华前任县委书记的去向",
                "why_it_matters": "了解换届交接和干部流动",
                "suggested_queries": ["凤冈县委书记 前任", "凤冈县委书记 卸任"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "县人大常委会主任和政协主席姓名",
                "why_it_matters": "四套班子信息不完整",
                "suggested_queries": ["凤冈县人大主任", "凤冈县政协主席"],
                "last_attempted": AS_OF
            },
            {
                "priority": "medium",
                "question": "任达林、张德晏、刘明、韩先军来凤冈前的任职经历",
                "why_it_matters": "理解领导班子成员背景和关系网络",
                "suggested_queries": ["任达林 简历", "张德晏 简历", "刘明 简历", "韩先军 简历"],
                "last_attempted": AS_OF
            }
        ]
    }

    # Write person JSON for each core figure
    for p in persons:
        data = person_json_template.copy()
        data["identity"]["person_id"] = f"fenggang_{p['name']}"
        data["identity"]["name"] = p["name"]
        data["identity"]["gender"] = p["gender"] or ""
        data["identity"]["ethnicity"] = p["ethnicity"] or ""
        data["identity"]["birth"] = p["birth"] or ""
        data["current_status"]["current_post"] = p["current_post"]
        data["current_status"]["current_org"] = p["current_org"]
        data["current_status"]["administrative_rank"] = "正县级" if "书记" in p["current_post"] or "县长" in p["current_post"] else "副县级"
        data["investigation_scope"]["job"] = p["current_post"]

        # Generate dedupe keys from what we know
        data["identity"]["dedupe_keys"]["name_birth"] = f"凤冈_{p['name']}_{p.get('birth', '')}"
        data["identity"]["dedupe_keys"]["name_birthplace"] = f"凤冈_{p['name']}"
        data["identity"]["dedupe_keys"]["official_profile_url"] = p.get("source", "")

        job_short = p["current_post"].replace("凤冈", "").strip()
        if not job_short:
            job_short = p["current_post"]

        filename = f"{AS_OF}-{PROVINCE}-{PARENT_CITY}-{job_short}-{p['name']}.json"
        filepath = os.path.join(PERSONS_DIR, filename)

        # Add relationships to the person-specific JSON
        person_rels = []
        for r in relationships:
            if r["person_a"] == p["id"]:
                target_p = next(p2 for p2 in persons if p2["id"] == r["person_b"])
                person_rels.append({
                    "person": target_p["name"],
                    "person_id": f"fenggang_{target_p['name']}",
                    "relationship_type": r["type"],
                    "strength": "strong",
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "undirected",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                })
            elif r["person_b"] == p["id"]:
                target_p = next(p2 for p2 in persons if p2["id"] == r["person_a"])
                person_rels.append({
                    "person": target_p["name"],
                    "person_id": f"fenggang_{target_p['name']}",
                    "relationship_type": r["type"],
                    "strength": "strong",
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "undirected",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                })
        data["relationships"] = person_rels

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Person JSON created: {filepath}")

    return len([p for p in persons if "待查" not in p["name"]])


def main():
    print(f"=== Building {SLUG} Network Data ===")
    print(f"Staging directory: {BASE}")
    print(f"Date: {AS_OF}")
    print()

    build_database()
    print()
    build_gexf()
    print()
    count = write_person_json()
    print()
    print(f"=== Build Complete ===")
    print(f"Database: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"Person JSONs: {count} complete files in {PERSONS_DIR}/")


if __name__ == "__main__":
    main()
