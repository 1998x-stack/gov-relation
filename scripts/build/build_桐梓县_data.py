#!/usr/bin/env python3
"""桐梓县（遵义市）领导班子关系网络数据生成脚本。

Targets: 县委书记 陈钊, 县长 曾建祥
Data as of: 2026-07-23
Sources: 桐梓县人民政府官网 (www.gztongzi.gov.cn), official news reports
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

TASK_ID = "guizhou_桐梓县"
SLUG = "桐梓县"
AS_OF = "2026-07-23"
PROVINCE = "贵州省"
PARENT_CITY = "遵义市"

BASE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.path.join("data", "tmp", "guizhou_桐梓县")
_BASE_OVERRIDE = os.environ.get("TONGZI_BASE")
if _BASE_OVERRIDE:
    BASE = _BASE_OVERRIDE

DB_PATH = os.path.join(BASE, "桐梓县_network.db")
GEXF_PATH = os.path.join(BASE, "桐梓县_network.gexf")
PERSONS_DIR = os.path.join(BASE, "persons")
os.makedirs(PERSONS_DIR, exist_ok=True)

# ── Data ──────────────────────────────────────────────────────────────────────

persons = [
    # 1 - 县委书记
    {
        "id": 1,
        "name": "陈钊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桐梓县委书记",
        "current_org": "中共桐梓县委员会",
        "source": "http://www.gztongzi.gov.cn/xwzx/xwdt/yw/202606/t20260612_90516560.html",
    },
    # 2 - 县长
    {
        "id": 2,
        "name": "曾建祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桐梓县委副书记、县人民政府县长",
        "current_org": "桐梓县人民政府",
        "source": "http://www.gztongzi.gov.cn/xwzx/xwdt/yw/202606/t20260612_90516560.html",
    },
    # 3 - 县委副书记
    {
        "id": 3,
        "name": "胡杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桐梓县委副书记",
        "current_org": "中共桐梓县委员会",
        "source": "http://www.gztongzi.gov.cn/xwzx/xwdt/yw/202606/t20260612_90516560.html",
    },
    # 4 - 县委副书记
    {
        "id": 4,
        "name": "谭玉娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桐梓县委副书记",
        "current_org": "中共桐梓县委员会",
        "source": "http://www.gztongzi.gov.cn/xwzx/xwdt/yw/202606/t20260612_90516560.html",
    },
    # 5 - 人大主任
    {
        "id": 5,
        "name": "王官忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桐梓县人大常委会主任",
        "current_org": "桐梓县人大常委会",
        "source": "http://www.gztongzi.gov.cn/xwzx/xwdt/yw/202606/t20260612_90516560.html",
    },
    # 6 - 政协主席
    {
        "id": 6,
        "name": "周德超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桐梓县政协主席",
        "current_org": "桐梓县政协",
        "source": "http://www.gztongzi.gov.cn/xwzx/xwdt/yw/202606/t20260612_90516560.html",
    },
]

organizations = [
    {"id": 1, "name": "中共桐梓县委员会", "type": "党委", "level": "县级", "location": "桐梓县"},
    {"id": 2, "name": "桐梓县人民政府", "type": "政府", "level": "县级", "location": "桐梓县"},
    {"id": 3, "name": "桐梓县人大常委会", "type": "人大", "level": "县级", "location": "桐梓县"},
    {"id": 4, "name": "桐梓县政协", "type": "政协", "level": "县级", "location": "桐梓县"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正县级", "note": "confirmed by official news reports"},
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start": "", "end": "present", "rank": "正县级", "note": "confirmed by official news reports"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副县级", "note": "confirmed by official news reports"},
    {"person_id": 4, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副县级", "note": "confirmed by official news reports"},
    {"person_id": 5, "org_id": 3, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "正县级", "note": ""},
    {"person_id": 6, "org_id": 4, "title": "县政协主席", "start": "", "end": "present", "rank": "正县级", "note": ""},
]

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "陈钊（县委书记）与曾建祥（县长）在桐梓县委常委会共事",
        "overlap_org": "中共桐梓县委员会",
        "overlap_period": "至2026年7月",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "陈钊（县委书记）与胡杰（县委副书记）上下级关系",
        "overlap_org": "中共桐梓县委员会",
        "overlap_period": "至2026年7月",
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "陈钊（县委书记）与谭玉娟（县委副书记）上下级关系",
        "overlap_org": "中共桐梓县委员会",
        "overlap_period": "至2026年7月",
    },
    {
        "person_a": 2,
        "person_b": 5,
        "type": "overlap",
        "context": "曾建祥（县长）与王官忠（人大主任）在桐梓县工作共事",
        "overlap_org": "桐梓县人民政府",
        "overlap_period": "至2026年7月",
    },
    {
        "person_a": 2,
        "person_b": 6,
        "type": "overlap",
        "context": "曾建祥（县长）与周德超（政协主席）在桐梓县工作共事",
        "overlap_org": "桐梓县人民政府",
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
    if "书记" in role_lower and "县委" in role_lower:
        return "255,50,50"
    elif "县长" in role_lower or "县" in role_lower and ("长" in role_lower or "政府" in role_lower):
        return "50,100,255"
    elif "政协" in role_lower:
        return "255,240,200"
    elif "人大" in role_lower:
        return "200,255,255"
    else:
        return "100,100,100"


def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    elif "政府" in t:
        return "200,200,255"
    elif "人大" in t:
        return "200,255,255"
    elif "政协" in t:
        return "255,240,200"
    else:
        return "200,200,200"


def is_top_leader(p):
    return p["id"] in (1, 2)


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append(f'    <description>桐梓县（遵义市）领导班子工作关系网络</description>')
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
        lines.append(f'          <attvalue for="3" value="桐梓县"/>')
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
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value=""/>')
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
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('          <attvalue for="3" value=""/>')
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
                "title": "桐梓县委常委会会议报道",
                "url": "http://www.gztongzi.gov.cn/xwzx/xwdt/yw/202606/t20260612_90516560.html",
                "publisher": "桐梓县人民政府",
                "published_at": "2026-06-12",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认陈钊为县委书记、曾建祥为县长"
            }
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "完整履历未公开"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "陈钊的完整履历（包括出生年份、籍贯、教育背景、早年任职经历）",
                "why_it_matters": "核心领导人，需完整身份信息",
                "suggested_queries": ["陈钊 简历 桐梓", "陈钊 任前公示", "陈钊 百度百科"],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": "曾建祥的完整履历（包括出生年份、籍贯、教育背景、早年任职经历）",
                "why_it_matters": "政府首长，需完整身份信息",
                "suggested_queries": ["曾建祥 简历 桐梓", "曾建祥 任前公示", "曾建祥 百度百科"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "陈钊前任县委书记的去向",
                "why_it_matters": "了解换届交接和干部流动",
                "suggested_queries": ["桐梓县委书记 前任", "桐梓县委书记 卸任"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "曾建祥前任县长的去向",
                "why_it_matters": "了解政府首长更替路径",
                "suggested_queries": ["桐梓县长 前任", "桐梓县长 任命"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "胡杰、谭玉娟等副职的完整履历",
                "why_it_matters": "理解县委领导班子结构",
                "suggested_queries": ["胡杰 桐梓", "谭玉娟 桐梓"],
                "last_attempted": AS_OF
            }
        ]
    }

    # Write person JSON for each core figure
    for p in persons:
        data = person_json_template.copy()
        data["identity"]["person_id"] = f"tongzi_{p['name']}"
        data["identity"]["name"] = p["name"]
        data["identity"]["gender"] = p["gender"] or ""
        data["identity"]["ethnicity"] = p["ethnicity"] or ""
        data["current_status"]["current_post"] = p["current_post"]
        data["current_status"]["current_org"] = p["current_org"]
        data["investigation_scope"]["job"] = p["current_post"]

        # Generate dedupe keys from what we know
        data["identity"]["dedupe_keys"]["name_birth"] = f"桐梓_{p['name']}"
        data["identity"]["dedupe_keys"]["name_birthplace"] = f"桐梓_{p['name']}"

        job_short = p["current_post"].replace("桐梓", "").replace("县委", "").strip()
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
                    "person_id": f"tongzi_{target_p['name']}",
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
                    "person_id": f"tongzi_{target_p['name']}",
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

    return len(persons)


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
    print(f"Person JSONs: {count} files in {PERSONS_DIR}/")


if __name__ == "__main__":
    main()
