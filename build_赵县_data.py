#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
赵县领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Zhao County leadership network.

Level: 县
Province: 河北省
Parent City: 石家庄市
Region: 赵县
Targets: 县委书记 & 县长

Research Sources:
- zhaoxian.gov.cn — 赵县人民政府门户网站 (2026年7月)
  - 领导之窗·县政府: http://www.zhaoxian.gov.cn/columns/63daca4b-cf8f-47f4-9e2b-94a34eae8733/index.html
  - 杨云龙(县长)简历: http://www.zhaoxian.gov.cn/columns/63daca4b-cf8f-47f4-9e2b-94a34eae8733/202509/23/40452b15-ec7d-4a52-b2a2-d78fa7f25f4e.html
- zh.wikipedia.org/wiki/赵县 — 维基百科赵县条目 (县委书记 王建海)

Confirmed officeholders (as of 2026-07-23):
- 县委书记: 王建海 (from Wikipedia)
- 县委副书记、县长: 杨云龙 (1976年11月生，男，汉族，中共党员; from zhaoxian.gov.cn official)

Note: Most biographical details (birthplace, education institutions, early career, full
leadership roster) remain to be filled from external sources. Baidu/Exa search was
unavailable during this research pass.

Research Date: 2026-07-23
"""

import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths ──
SLUG = "赵县"
AS_OF = "2026-07-23"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ════════════════════════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════════════════════════

# 1. Persons
persons = [
    # ═══════════════════════════════
    # Current Top Leaders
    # ═══════════════════════════════
    {
        "id": 1,
        "name": "王建海",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共赵县委员会",
        "source": "https://zh.wikipedia.org/wiki/%E8%B5%B5%E5%8E%BF — 维基百科赵县条目, accessed 2026-07-23"
    },
    {
        "id": 2,
        "name": "杨云龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年11月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "赵县人民政府",
        "source": "http://www.zhaoxian.gov.cn/columns/63daca4b-cf8f-47f4-9e2b-94a34eae8733/202509/23/40452b15-ec7d-4a52-b2a2-d78fa7f25f4e.html — 赵县人民政府领导之窗, accessed 2026-07-23"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共赵县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共石家庄市委员会",
        "location": "河北省石家庄市赵县"
    },
    {
        "id": 2,
        "name": "赵县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "石家庄市人民政府",
        "location": "河北省石家庄市赵县"
    },
]

# 3. Positions
positions = [
    {
        "person_id": 1,
        "org_id": 1,
        "title": "县委书记",
        "start_date": "",
        "end_date": "present",
        "rank": "正处级",
        "note": "主持县委全面工作"
    },
    {
        "person_id": 2,
        "org_id": 2,
        "title": "县委副书记、县长",
        "start_date": "",
        "end_date": "present",
        "rank": "正处级",
        "note": "领导县政府全面工作。分管县审计局。"
    },
    {
        "person_id": 2,
        "org_id": 1,
        "title": "县委副书记",
        "start_date": "",
        "end_date": "present",
        "rank": "正处级",
        "note": "县委副书记兼任县长"
    },
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "赵县县委书记与县长党政搭档",
        "overlap_org": "中共赵县委员会/赵县人民政府",
        "overlap_period": "present"
    },
]


# ════════════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(current_post):
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp and "纪委" not in cp:
        return "255,50,50"
    if "县长" in cp and "副" not in cp:
        return "50,100,255"
    if "副书记" in cp:
        return "220,80,80"
    if "常委" in cp and "纪委" in cp:
        return "255,165,0"
    if "常委" in cp:
        return "180,100,180"
    if "副" in cp and ("县长" in cp or "区长" in cp):
        return "100,150,220"
    if "主任" in cp or "人大" in cp:
        return "60,180,60"
    if "主席" in cp or "政协" in cp:
        return "60,180,60"
    if "副县长" in cp:
        return "100,150,220"
    return "100,100,100"


def person_size(current_post):
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp and "纪委" not in cp:
        return "20.0"
    if "县长" in cp and "副" not in cp:
        return "18.0"
    if "副书记" in cp:
        return "15.0"
    if "常委" in cp:
        return "12.0"
    if "副主任" in cp or "副主席" in cp or "副县长" in cp:
        return "12.0"
    if "主任" in cp or "主席" in cp:
        return "14.0"
    return "10.0"


def person_shape(current_post):
    cp = current_post or ""
    if "书记" in cp:
        return "square"
    if "人大" in cp or "政协" in cp:
        return "diamond"
    if "副" in cp:
        return "triangle"
    return "circle"


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "开发区": "200,255,200",
        "纪委": "255,200,150",
        "群团": "255,220,255",
    }
    return colors.get(org_type, "200,200,200")


def build_person_json(person, timeline, rels, sources):
    p = person
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河北省",
            "city": "石家庄市",
            "region": "赵县",
            "job": p.get("current_post", "").split("、")[0].split("兼")[0].strip("、"),
            "task_id": "hebei_赵县",
            "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"zhaoxian_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [
                {
                    "period": "",
                    "institution": "",
                    "major": "",
                    "degree": "",
                    "study_type": "unknown",
                    "source_ids": []
                }
            ],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source", "")
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "正处级" if ("书记" in p.get("current_post","") or "县长" in p.get("current_post","")) else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": rels,
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
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "No risk signals found through available public sources",
            "date": "",
            "confidence": "unverified",
            "source_ids": []
        }],
        "source_register": sources,
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": f"Earlier career timeline before current role for {p['name']}"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"Complete career timeline before current role for {p['name']} - full position history",
                "why_it_matters": "Cannot assess career pattern, promotion velocity, or network building without full timeline",
                "suggested_queries": [f"{p['name']} 简历 赵县", f"{p['name']} 任职经历", f"{p['name']} 百度百科"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"Birthplace and native place for {p['name']}",
                "why_it_matters": "Essential for identity deduplication and native-place network analysis",
                "suggested_queries": [f"{p['name']} 籍贯"],
                "last_attempted": AS_OF
            },
            {
                "priority": "medium",
                "question": f"Education details (institution, major, degree type) for {p['name']}",
                "why_it_matters": "Alumni networks are important relationship channels",
                "suggested_queries": [f"{p['name']} 毕业"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "Full county leadership roster (deputy party secretary, standing committee members, deputy county heads, etc.)",
                "why_it_matters": "Cannot build comprehensive network without full leadership team",
                "suggested_queries": ["赵县 县委常委 名单", "赵县 领导分工"],
                "last_attempted": AS_OF
            }
        ]
    }


def build_person_jsons():
    """Build and write person JSON files for 王建海 and 杨云龙."""
    now = AS_OF.replace("-", "")

    sources = [
        {"id": "S001", "title": "赵县人民政府·领导之窗",
         "url": "http://www.zhaoxian.gov.cn/columns/63daca4b-cf8f-47f4-9e2b-94a34eae8733/index.html",
         "publisher": "赵县人民政府",
         "published_at": "",
         "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "Official leadership roster page"},
        {"id": "S002", "title": "杨云龙简历页",
         "url": "http://www.zhaoxian.gov.cn/columns/63daca4b-cf8f-47f4-9e2b-94a34eae8733/202509/23/40452b15-ec7d-4a52-b2a2-d78fa7f25f4e.html",
         "publisher": "赵县人民政府",
         "published_at": "2025-09-23",
         "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "县长杨云龙官方简历"},
        {"id": "S003", "title": "维基百科·赵县条目",
         "url": "https://zh.wikipedia.org/wiki/%E8%B5%B5%E5%8E%BF",
         "publisher": "维基百科",
         "published_at": "",
         "accessed_at": AS_OF,
         "source_type": "encyclopedia", "reliability": "medium",
         "notes": "赵县Wikipedia条目，列出县委书记为王建海"},
    ]

    # ── 王建海 person JSON ──
    wjh_timeline = [
        {"start": "", "end": "present",
         "org": "中共赵县委员会",
         "title": "县委书记",
         "level": "正处级",
         "location": "河北省石家庄市赵县",
         "system": "party",
         "rank": "正处级",
         "is_key_promotion": True,
         "notes": "主持县委全面工作；仅Wikipedia确认角色，无完整简历",
         "confidence": "confirmed",
         "source_ids": ["S003"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到王建海任赵县县委书记之前的完整履历",
         "confidence": "unverified",
         "source_ids": []},
    ]
    wjh_relationships = [
        {"person": "杨云龙", "person_id": "zhaoxian_杨云龙",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "目前赵县县委书记与县长党政搭档",
         "overlap_org": "中共赵县委员会/赵县人民政府",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001", "S003"]},
    ]
    wjh_json = build_person_json(persons[0], wjh_timeline, wjh_relationships, sources)
    wjh_json["investigation_scope"]["job"] = "县委书记"
    wjh_json["identity"]["ethnicity"] = ""  # unknown
    wjh_json["identity"]["gender"] = ""  # unknown
    wjh_path = os.path.join(PERSONS_DIR, f"{now}-河北省-石家庄市-县委书记-王建海.json")
    with open(wjh_path, "w", encoding="utf-8") as f:
        json.dump(wjh_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {wjh_path}")

    # ── 杨云龙 person JSON ──
    yyl_timeline = [
        {"start": "", "end": "present",
         "org": "赵县人民政府",
         "title": "县委副书记、县长",
         "level": "正处级",
         "location": "河北省石家庄市赵县",
         "system": "government",
         "rank": "正处级",
         "is_key_promotion": True,
         "notes": "领导县政府全面工作，分管县审计局；1976年11月生，男，汉族，中共党员",
         "confidence": "confirmed",
         "source_ids": ["S001", "S002"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到杨云龙任赵县县长之前的完整履历",
         "confidence": "unverified",
         "source_ids": []},
    ]
    yyl_relationships = [
        {"person": "王建海", "person_id": "zhaoxian_王建海",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "目前赵县县长与县委书记党政搭档",
         "overlap_org": "赵县人民政府/中共赵县委员会",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001", "S003"]},
    ]
    yyl_json = build_person_json(persons[1], yyl_timeline, yyl_relationships, sources)
    yyl_json["investigation_scope"]["job"] = "县长"
    yyl_path = os.path.join(PERSONS_DIR, f"{now}-河北省-石家庄市-县长-杨云龙.json")
    with open(yyl_path, "w", encoding="utf-8") as f:
        json.dump(yyl_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {yyl_path}")


# ════════════════════════════════════════════════════════════════
# BUILD FUNCTIONS
# ════════════════════════════════════════════════════════════════

def build_db():
    """Build SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '',
            party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '',
            source TEXT DEFAULT ''
        );

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );

        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute("""INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,
                       party_join,work_start,current_post,current_org,source)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
                     p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
                     p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""),
                     p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location)
                       VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"],
                     o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note)
                       VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"],
                     pos.get("start_date", ""), pos.get("end_date", ""),
                     pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period)
                       VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"], r["context"],
                     r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


def build_gexf():
    """Build GEXF graph file."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>{SLUG}领导班子关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes - persons
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        cp = p.get("current_post", "")
        color = person_color(cp)
        size = person_size(cp)
        shape = person_shape(cp)
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(cp)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o["type"])
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('        <viz:shape value="hexagon"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]+100000}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ person (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")


def build():
    os.makedirs(STAGING_DIR, exist_ok=True)
    print(f"=== Building {SLUG} data ===")
    print(f"Staging dir: {STAGING_DIR}")

    build_db()
    build_gexf()
    build_person_jsons()

    print(f"\n=== Build complete ===")


if __name__ == "__main__":
    build()
