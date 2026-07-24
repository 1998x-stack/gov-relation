#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 孟州市 (Mengzhou City), 焦作市, 河南省.

Investigation date: 2026-07-24
Task ID: henan_孟州市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - https://www.mengzhou.gov.cn/ — official government website
    (homepage news confirms 岳益民 as 市委书记, active July 2026:
     - 岳益民督导检查生态环境保护工作 (2026-07-23)
     - 岳益民调研督导防汛工作 (2026-07-17)
     - 岳益民暗访检查生态环境保护工作 (2026-07-17)
     - 岳益民督导检查消防安全工作 (2026-07-16)
     - 岳益民主持召开市委党的建设工作领导小组会议 (2026-07-14)
     - 岳益民主持召开市委常委会会议 (2026-07-14))
  - https://baike.baidu.com/item/孟州市 — Baidu Baike
    (confirmed leadership table: 岳益民 市委书记, 任红星 市长,
     闫全心 市人大常委会主任, 吴长青 市政协主席, as of 2026-04)
  - 十四届孟州市委一次全会 expected circa 2026 (standing committee details unverified)
  - http://www.jiaozuo.gov.cn/ — 焦作市 parent city government (for cross-reference)
  - 焦作市委组织部 任前公示 (pre-appointment notices for 孟州 leaders)

Confidence notes:
  - 岳益民 (市委书记): confirmed via multiple official news articles on mengzhou.gov.cn
    spanning July 2026. Previous career and birth year unverified — marked as gaps.
  - 任红星 (市长): confirmed via Baidu Baike (2026-04). Full career timeline and
    details unverified.
  - 闫全心 (市人大常委会主任): confirmed via Baidu Baike. Details unverified.
  - 吴长青 (市政协主席): confirmed via Baidu Baike. Details unverified.
  - 市委常委 and 副市长 slots: known positions exist but specific names beyond
    the core leadership are not confirmed from accessible sources.
  - Predecessor info for 岳益民 is unverified — likely appointed in 2025 or early 2026.
  - This is a partial-evidence artifact: core identities are confirmed;
    individual career histories are mostly unconfirmed.
"""

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "孟州市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "岳益民",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共孟州市委员会",
        "source": "Confirmed via mengzhou.gov.cn homepage news articles (2026-07): inspection, flood control, fire safety, party committee meetings. e.g. 岳益民督导检查生态环境保护工作 (2026-07-23)"
    },
    {
        "id": 2,
        "name": "任红星",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "孟州市人民政府",
        "source": "Confirmed via Baidu Baike 孟州市 leadership table (2026-04)"
    },
    # ═══════人大/政协 Leadership ═══════
    {
        "id": 3,
        "name": "闫全心",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "孟州市人民代表大会常务委员会",
        "source": "Confirmed via Baidu Baike 孟州市 leadership table (2026-04)"
    },
    {
        "id": 4,
        "name": "吴长青",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议孟州市委员会",
        "source": "Confirmed via Baidu Baike 孟州市 leadership table (2026-04)"
    },
    # ═══════ Known 市委常委 / 副市长 candidates (partial) ═══════
    # Note: These positions exist in the org structure but specific names
    # are not publicly accessible from available sources.
    # Include placeholder entries to indicate expected slots.
    # ═══════ Other Mentioned Leaders ═══════
    # Additional leaders may be mentioned in news articles but not
    # systematically documented in accessible sources.
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共孟州市委员会", "type": "党委", "level": "县级市", "location": "孟州市"},
    {"id": 2, "name": "孟州市人民政府", "type": "政府", "level": "县级市", "location": "孟州市"},
    {"id": 3, "name": "孟州市人民代表大会常务委员会", "type": "人大", "level": "县级市", "location": "孟州市"},
    {"id": 4, "name": "中国人民政治协商会议孟州市委员会", "type": "政协", "level": "县级市", "location": "孟州市"},
    {"id": 5, "name": "中共孟州市纪律检查委员会", "type": "党委", "level": "县级市", "location": "孟州市"},
    {"id": 6, "name": "中共孟州市委政法委员会", "type": "党委", "level": "县级市", "location": "孟州市"},
    {"id": 7, "name": "中共孟州市委组织部", "type": "党委", "level": "县级市", "location": "孟州市"},
]

# ── Positions ───────────────────────────────────────────────────────────────
positions = [
    # 岳益民
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "", "end": "present", "rank": "正处级", "note": "Confirmed active in multiple July 2026 news articles"},
    # 任红星
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "", "end": "present", "rank": "正处级", "note": "主持市政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 闫全心
    {"person_id": 3, "org_id": 3, "title": "市人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 吴长青
    {"person_id": 4, "org_id": 4, "title": "市政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # Core leadership overlaps
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "市委书记—市长搭档", "overlap_org": "中共孟州市委员会/孟州市人民政府", "overlap_period": "至2026年7月", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "市委书记—人大主任", "overlap_org": "孟州市", "overlap_period": "至2026年", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "市委书记—政协主席", "overlap_org": "孟州市", "overlap_period": "至2026年", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "市长—人大主任", "overlap_org": "孟州市", "overlap_period": "至2026年", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "市长—政协主席", "overlap_org": "孟州市", "overlap_period": "至2026年", "confidence": "confirmed"},
]

# ── Helper functions ────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(post):
    """Return GEXF color string for a person by current post."""
    if "书记" in post and "市委" in post:
        return "255,50,50"
    if "市长" in post or "副市长" in post or "政府" in post:
        return "50,100,255"
    if "纪委" in post:
        return "255,165,0"
    if "人大" in post:
        return "200,255,255"  # cyan
    if "政协" in post:
        return "255,240,200"  # cream
    if "政法委" in post:
        return "200,200,255"
    return "100,100,100"


def org_color(org_type):
    """Return GEXF color string for an organization by type."""
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(org_type, "200,200,200")


def is_top_leader(person):
    return person["current_post"] in ("市委书记", "市长")


def gen_gexf(persons, organizations, positions, relationships, output_path):
    """Generate GEXF 1.3 graph file using string formatting to avoid namespace issues."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append(f'    <description>孟州市领导班子工作关系网络 — 调查日期 {TODAY}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="org_type" type="string"/>')
    lines.append('      <attribute id="4" title="level" type="string"/>')
    lines.append('      <attribute id="5" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('      <attribute id="4" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        pcolor = person_color(p["current_post"])
        psize = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append(f'          <attvalue for="4" value=""/>')
        lines.append(f'          <attvalue for="5" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{pcolor.split(",")[0]}" g="{pcolor.split(",")[1]}" b="{pcolor.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{psize}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        ocolor = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(o["level"])}"/>')
        lines.append(f'          <attvalue for="5" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization edges (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])} at {esc(pos["note"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos["start"])}—{esc(pos["end"])}"/>')
        lines.append(f'          <attvalue for="4" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person edges (relationships)
    for r in relationships:
        eid += 1
        weight = "2.0" if r["confidence"] == "confirmed" else "1.0"
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append(f'          <attvalue for="4" value="{r["confidence"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def gen_person_json(person, today_str, task_id):
    """Generate a person JSON file following the person_graph_json.md schema."""
    person_id = f"mengzhou_{person['name']}"

    career_timeline = []
    for pos in positions:
        if pos["person_id"] == person["id"]:
            org_name = ""
            for o in organizations:
                if o["id"] == pos["org_id"]:
                    org_name = o["name"]
                    break
            career_timeline.append({
                "start": pos["start"] or "unknown",
                "end": pos["end"] or "unknown",
                "org": org_name,
                "title": pos["title"],
                "rank": pos["rank"],
                "notes": pos["note"],
                "confidence": "confirmed",
                "source_ids": ["S001"],
            })

    person_relationships = []
    for r in relationships:
        if r["person_a"] == person["id"]:
            target_id = r["person_b"]
            target_name = ""
            for p in persons:
                if p["id"] == target_id:
                    target_name = p["name"]
                    break
            person_relationships.append({
                "person": target_name,
                "person_id": f"mengzhou_{target_name}",
                "relationship_type": r["type"],
                "strength": "strong" if r["confidence"] == "confirmed" else "medium",
                "evidence": r["context"],
                "overlap_org": r["overlap_org"],
                "overlap_period": r["overlap_period"],
                "direction": "undirected",
                "confidence": r["confidence"],
                "source_ids": ["S001"],
            })
        elif r["person_b"] == person["id"]:
            src_id = r["person_a"]
            src_name = ""
            for p in persons:
                if p["id"] == src_id:
                    src_name = p["name"]
                    break
            person_relationships.append({
                "person": src_name,
                "person_id": f"mengzhou_{src_name}",
                "relationship_type": r["type"],
                "strength": "strong" if r["confidence"] == "confirmed" else "medium",
                "evidence": r["context"],
                "overlap_org": r["overlap_org"],
                "overlap_period": r["overlap_period"],
                "direction": "undirected",
                "confidence": r["confidence"],
                "source_ids": ["S001"],
            })

    orgs_for_person = []
    for pos in positions:
        if pos["person_id"] == person["id"]:
            for o in organizations:
                if o["id"] == pos["org_id"]:
                    orgs_for_person.append({
                        "id": o["id"],
                        "name": o["name"],
                        "type": o["type"],
                        "level": o["level"],
                    })

    schema = {
        "schema_version": "1.0",
        "generated_at": today_str,
        "investigation_scope": {
            "province": "河南省",
            "city": "焦作市",
            "region": "孟州市",
            "job": person["current_post"],
            "task_id": task_id,
            "time_focus": "2024-2026",
        },
        "identity": {
            "person_id": person_id,
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"] or "",
            "ethnicity": person["ethnicity"] or "",
            "birth": person["birth"] or "",
            "birthplace": person["birthplace"] or "",
            "native_place": "",
            "education": [],
            "party_join": person["party_join"] or "",
            "work_start": person["work_start"] or "",
            "dedupe_keys": {
                "name_birth": f"{person['name']}_",
                "name_birthplace": f"{person['name']}_",
                "official_profile_url": "https://www.mengzhou.gov.cn/",
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if "书记" in person["current_post"] and ("市委" in person["current_post"] or "市" in person["current_post"]) else ("正处级" if "市长" in person["current_post"] or "人大主任" in person["current_post"] or "政协主席" in person["current_post"] else "副处级"),
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": orgs_for_person,
        "relationships": person_relationships,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "详细履历待查",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {
            "degree_centrality": 0,
            "betweenness_centrality": 0,
            "community_cluster": "",
        },
        "risk_and_integrity_signals": [],
        "source_register": [
            {
                "id": "S001",
                "title": "孟州市人民政府官方网站",
                "url": "https://www.mengzhou.gov.cn/",
                "publisher": "孟州市人民政府",
                "published_at": AS_OF,
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "Primary source for leadership roster. Homepage news confirms 岳益民 as 市委书记 actively working in July 2026.",
            },
            {
                "id": "S002",
                "title": "百度百科 - 孟州市",
                "url": "https://baike.baidu.com/item/孟州市",
                "publisher": "百度百科",
                "published_at": "2026-04",
                "accessed_at": AS_OF,
                "source_type": "encyclopedia",
                "reliability": "medium",
                "notes": "Leadership table listing 岳益民、任红星、闫全心、吴长青.",
            },
        ],
        "confidence_summary": {
            "identity": "partial" if not person["birth"] else "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "high",
            "biggest_gap": "详细履历（出生年份、教育背景、早期任职经历）缺失；市委常委和副市长名单未确认",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的出生年份、出生地、教育经历",
                "why_it_matters": "核心身份信息，影响人员去重和晋升速度分析",
                "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 出生", f"孟州市 {person['name']} 任前公示"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{person['name']}的完整工作履历",
                "why_it_matters": "缺少早期职业经历，无法分析晋升路径和与其他官员的交集",
                "suggested_queries": [f"{person['name']} 任职经历", f"{person['name']} 曾任", f"焦作 {person['name']}"],
                "last_attempted": AS_OF,
            },
        ],
    }
    return schema


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    # Build SQLite
    import sqlite3
    db_path = DB_PATH
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS persons (
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
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    cur.execute("""
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
        )
    """)
    cur.execute("""
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
        )
    """)

    # Insert persons
    for p in persons:
        cur.execute("""
            INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
              p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    # Insert organizations
    for o in organizations:
        cur.execute("""
            INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], "", o["location"]))

    # Insert positions
    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    # Insert relationships
    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"✅ SQLite database: {db_path}")

    # Build GEXF
    gen_gexf(persons, organizations, positions, relationships, GEXF_PATH)
    print(f"✅ GEXF graph: {GEXF_PATH}")

    # Generate person JSONs for core leaders
    core_leaders = [p for p in persons if p["id"] in (1, 2)]  # 岳益民, 任红星
    for leader in core_leaders:
        suffix = leader["current_post"].replace("、", "_").replace(" ", "_")
        safe_name = leader["name"]
        json_path = PERSONS_DIR / f"{TODAY}-河南省-焦作市-{suffix}-{safe_name}.json"
        data = gen_person_json(leader, TODAY, "henan_孟州市")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Person JSON: {json_path}")

    print(f"\n📊 Summary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")


if __name__ == "__main__":
    main()
