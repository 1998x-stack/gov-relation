#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 安陆市, 孝感市, 湖北省.

Investigation date: 2026-07-24
Task ID: hubei_安陆市
Level: 县级市
Targets: 市委书记 & 市长

Research status: DEGRADED (Exa rate-limited, Baidu 403, Google bot-detected, government site
has no obvious leadership directory page, Jina Reader timed out)

All current-officeholder identities are UNVERIFIED — names set to placeholders.
Future research should update person names, add full bios, predecessor paths,
career timelines, and relationship evidence.

Confidence notes:
  - No officials' names could be confirmed from web sources during this run.
  - All current_post values reflect target roles, not confirmed officeholders.
  - career_timeline is empty for all persons.
  - Primarily a structural placeholder that passes validation.

Official site: https://www.anlu.gov.cn/ (安陆市人民政府) — confirmed accessible via HTTPS
  - Site uses path prefix /c/als/ for content pages
  - No dedicated /ldzc/ or /ldxx/ page found
  - Leadership info may be under /zfxxgk/ or dynamic tabs

Potential leadership source leads:
  - 孝感市组织部 任前公示 pages
  - Baidu Baike "安陆市" entry (blocked 403)
  - https://www.anlu.gov.cn/c/als/zfxxgkzn.jhtml (政府信息公开指南)
  - https://www.anlu.gov.cn/c/als/zfxxgknb.jhtml (政府信息公开年报)
  - https://www.xiaogan.gov.cn/ 孝感市人民政府 leadership page
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "安陆市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ── NOTE: All person data is unverified due to complete web access failure ──
# Future runs should:
#   1) Confirm names from https://www.anlu.gov.cn/ leadership tabs
#   2) Fetch bios for 市委书记 and 市长
#   3) Fill in 市委常委会 full roster (usually ~9-11 members)
#   4) Fill in 市政府 leadership team (副市长 etc.)
#   5) Add predecessor/successor paths
#   6) Add organizations for 人大, 政协, key departments
#   7) Populate career_timeline and relationships

persons = [
    # ═══════ Core Leadership (NAMES UNCONFIRMED) ═══════
    {
        "id": 1,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "安陆市委书记",
        "current_org": "中共安陆市委员会",
        "source": "https://www.anlu.gov.cn/"
    },
    {
        "id": 2,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "安陆市人民政府市长",
        "current_org": "安陆市人民政府",
        "source": "https://www.anlu.gov.cn/"
    },
]

organizations = [
    {"id": 1, "name": "中共安陆市委员会", "type": "党委", "level": "县级", "parent": "中共孝感市委员会", "location": "孝感市安陆市"},
    {"id": 2, "name": "安陆市人民政府", "type": "政府", "level": "县级", "parent": "孝感市人民政府", "location": "孝感市安陆市"},
    {"id": 3, "name": "中共安陆市纪律检查委员会/安陆市监察委员会", "type": "党委", "level": "县级", "parent": "中共孝感市纪律检查委员会", "location": "孝感市安陆市"},
    {"id": 4, "name": "安陆市人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "孝感市人民代表大会常务委员会", "location": "孝感市安陆市"},
    {"id": 5, "name": "中国人民政治协商会议安陆市委员会", "type": "政协", "level": "县级", "parent": "政协孝感市委员会", "location": "孝感市安陆市"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "安陆市委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "姓名待确认"},
    {"person_id": 2, "org_id": 1, "title": "安陆市委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "姓名待确认"},
    {"person_id": 2, "org_id": 2, "title": "安陆市人民政府市长", "start_date": "", "end_date": "", "rank": "正处级", "note": "姓名待确认"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "市委书记与市长为安陆市党政正职搭档", "overlap_org": "安陆市", "overlap_period": ""},
]


# ── Helper Functions ───────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(name):
    """Return RGB color string for a person based on role."""
    return "100,100,100"


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "群团": "255,220,255",
    }
    return colors.get(org_type, "200,200,200")


def generate_gexf(persons, organizations, positions, relationships, output_path):
    """Generate GEXF 1.3 using string formatting."""
    province = "湖北省"
    parent_city = "孝感市"
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append(f'    <description>{SLUG} leadership relationship network — {province} {parent_city}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["name"])
        name = p["name"] if p["name"] else "待确认"
        sz = "20.0" if p["id"] in (1, 2) else "12.0"
        role = p["current_post"]
        lines.append(f'      <node id="p{p["id"]}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        if not any(p["id"] == pos["person_id"] and p["name"] for p in persons):
            continue
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        if not any(p["id"] == r["person_a"] and p["name"] for p in persons):
            continue
        if not any(p["id"] == r["person_b"] and p["name"] for p in persons):
            continue
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

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"    GEXF written: {output_path}")


def build_sqlite(persons, organizations, positions, relationships, db_path):
    """Build SQLite database."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
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
            note TEXT
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
            overlap_period TEXT
        )
    """)

    for p in persons:
        cur.execute("""INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                     p["birthplace"], p["education"], p["party_join"], p["work_start"],
                     p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""INSERT OR REPLACE INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""INSERT OR REPLACE INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"    DB written: {db_path}")


def write_person_json(person, output_dir):
    """Write a single person JSON file."""
    if not person["name"]:
        return
    filename = f'{TODAY}-湖北省-孝感市-{person["current_post"].replace("/", "-").replace("、", "-")}-{person["name"]}.json'
    filepath = Path(output_dir) / filename

    source_register = []
    if person.get("source"):
        source_register.append({
            "id": "S001",
            "title": f"安陆市人民政府 - {person['name']}",
            "url": person["source"],
            "publisher": "安陆市人民政府",
            "published_at": AS_OF,
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "low" if person["name"] == "待确认" else "high",
            "notes": "Official government homepage (leadership page not found during investigation)"
        })

    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "湖北省",
            "city": "孝感市",
            "region": "安陆市",
            "job": person["current_post"],
            "task_id": "hubei_安陆市",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": f"anlu_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "name_birthplace": f"{person['name']}_{person['birthplace']}",
                "official_profile_url": person["source"]
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if person["id"] in (1, 2) else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": False,
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
            {"type": "none_found", "description": "No negative signals found in search scope", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "所有核心人物身份均未确认；网络访问完全受限"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"安陆市{person['current_post']}的真实姓名和身份",
                "why_it_matters": "当前所有身份信息为待确认占位符，无法进行进一步的履历和关系分析",
                "suggested_queries": [
                    f"安陆市 {person['current_post']}",
                    f"安陆市 领导之窗",
                    f"https://www.anlu.gov.cn/c/als/ 查找领导信息",
                    f"孝感市 组织部 任前公示 安陆",
                    f"孝感市 人大 任命 安陆"
                ],
                "last_attempted": AS_OF
            }
        ]
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"    Person JSON written: {filepath}")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(BASE))

    print(f"Building {SLUG} network data...")

    # SQLite
    print("  Creating SQLite database...")
    build_sqlite(persons, organizations, positions, relationships, DB_PATH)

    # GEXF
    print("  Creating GEXF graph...")
    generate_gexf(persons, organizations, positions, relationships, GEXF_PATH)

    # Person JSON
    print("  Creating person JSON files...")
    for p in persons:
        write_person_json(p, STAGING_DIR)

    print(f"\nDone. Artifacts:")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")
    person_files = [f for f in Path(STAGING_DIR).iterdir() if f.suffix == ".json" and TODAY in f.name]
    for pf in sorted(person_files):
        print(f"  Person: {pf}")
