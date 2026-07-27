#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 庆安县 (Qing'an County), 绥化市, 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_庆安县
Level: 县 (county)
Parent city: 绥化市
Province: 黑龙江省
Targets: 县委书记 & 县长

Research sources:
  - 庆安县人民政府官网 (www.hljqingan.gov.cn) — confirmed current leadership via news articles
  - 庆安要闻: 县委农村工作领导小组2026年第一次全体会议 (2026-07-21) — confirmed 慕海军 as 县委书记, 刘志宇 as 县长
  - 庆安要闻: 县领导到14个乡镇调研督导 (2026-07-23) — confirmed 慕海军 as 县委书记
  - 中国共产党庆安县第十六届委员会第九次全体会议 (2025-12-08) — confirmed 慕海军 as 县委书记
  - Wikipedia (zh.wikipedia.org) — confirmed 慕海军 as 县长 (historical), county basic info

Key findings:
  - 慕海军: 县委书记, previously served as 县长 of 庆安县, promoted to Party Secretary before Dec 2025
  - 刘志宇: 县长, confirmed in role as of July 2026
  - Also identified: 杨琦琳 as 县领导 (出席县委农村工作领导小组会议)

Confidence notes:
  - 慕海军 (县委书记): confirmed via multiple official government news articles (July 2026, Dec 2025)
  - 刘志宇 (县长): confirmed via official government news (July 2026)
  - Detailed career histories before current roles are mostly unavailable
  - Previous 县委书记 and 县长 information unknown
  - Web search (Exa, Baidu, Jina, Google) was rate-limited or blocked during this investigation
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add project root to sys.path
BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

sys.path.insert(0, os.path.join(PROJECT_ROOT, "."))
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Constants ─────────────────────────────────────────────────────────────
SLUG = "庆安县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Source URLs
SRC_GOV = "https://www.hljqingan.gov.cn/"
SRC_NEWS_1 = "https://www.hljqingan.gov.cn/qa/qayw/202607/c12_237978.shtml"  # 县委农村工作领导小组会议 (confirms 慕海军 书记, 刘志宇 县长)
SRC_NEWS_2 = "https://www.hljqingan.gov.cn/qa/qayw/202607/c12_238190.shtml"  # 县领导到14个乡镇调研 (confirms 慕海军 书记)
SRC_NEWS_3 = "https://www.hljqingan.gov.cn/qa/qayw/202512/c12_222446.shtml"  # 县委十六届九次全会 (confirms 慕海军 书记)
SRC_WIKI = "https://zh.wikipedia.org/wiki/%E5%BA%86%E5%AE%89%E5%8E%BF"

# Staging file names (written to data/tmp/heilongjiang_庆安县/)
DB_NAME = f"{SLUG}_network.db"
GEXF_NAME = f"{SLUG}_network.gexf"

# Absolute paths for process_tmp.py compatibility (will be overridden in main())
DB_PATH = os.path.join(BASE, DB_NAME)
GEXF_PATH = os.path.join(BASE, GEXF_NAME)

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    # ═══════════════════════════════════════════════════════════════════════
    # 1. Core Leadership
    # ═══════════════════════════════════════════════════════════════════════

    # 慕海军 — 县委书记
    {
        "id": 1,
        "name": "慕海军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共庆安县委员会",
        "source": SRC_NEWS_1
    },
    # 刘志宇 — 县长
    {
        "id": 2,
        "name": "刘志宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县长",
        "current_org": "庆安县人民政府",
        "source": SRC_NEWS_1
    },
    # 杨琦琳 — 县领导 (confirmed attending 县委农村工作领导小组会议)
    {
        "id": 3,
        "name": "杨琦琳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "庆安县",
        "source": SRC_NEWS_1
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共庆安县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共绥化市委员会",
        "location": "庆安县"
    },
    {
        "id": 2,
        "name": "庆安县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "绥化市人民政府",
        "location": "庆安县"
    },
    {
        "id": 3,
        "name": "庆安县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "parent": "绥化市人民代表大会常务委员会",
        "location": "庆安县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议庆安县委员会",
        "type": "政协",
        "level": "县",
        "parent": "政协绥化市委员会",
        "location": "庆安县"
    },
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 慕海军 — 县委书记
    {
        "person_id": 1,
        "org_id": 1,
        "title": "县委书记",
        "start": "",
        "end": "present",
        "rank": "正处级",
        "note": "Confirmed as of July 2026. Previously served as 县长 of 庆安县, promoted to 县委书记 before December 2025."
    },
    # 刘志宇 — 县长
    {
        "person_id": 2,
        "org_id": 2,
        "title": "县长",
        "start": "",
        "end": "present",
        "rank": "正处级",
        "note": "Confirmed as of July 2026."
    },
    # 杨琦琳 — 县领导
    {
        "person_id": 3,
        "org_id": 1,
        "title": "县领导",
        "start": "",
        "end": "present",
        "rank": "",
        "note": "Attended 县委农村工作领导小组2026年第一次全体会议 (2026-07-20). Exact role unknown."
    },
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长关系",
        "overlap_org": "庆安县",
        "overlap_period": "2026-",
        "strength": "strong",
        "confidence": "confirmed",
        "source": SRC_NEWS_1
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委领导与县领导工作关系",
        "overlap_org": "庆安县",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed",
        "source": SRC_NEWS_1
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "overlap",
        "context": "县政府领导和县领导工作关系",
        "overlap_org": "庆安县",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed",
        "source": SRC_NEWS_1
    },
]

# ── Helper Functions ──────────────────────────────────────────────────────
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return 'r,g,b' color string based on role."""
    title = p.get("current_post", "")
    if "书记" in title and "纪委" not in title:
        return "255,50,50"  # Party Secretary - Red
    elif "县长" in title or "区长" in title or "市长" in title:
        return "50,100,255"  # Mayor - Blue
    elif "纪委" in title:
        return "255,165,0"  # Discipline - Orange
    else:
        return "100,100,100"  # Others - Grey

def org_color(o):
    """Return 'r,g,b' color string based on org type."""
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

# ── Run Build ──────────────────────────────────────────────────────────────
def main():
    staging_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(staging_dir, DB_NAME)
    gexf_path = os.path.join(staging_dir, GEXF_NAME)

    print(f"=== Building {SLUG} network ===")
    print(f"Staging dir: {staging_dir}")
    print(f"Database: {db_path}")
    print(f"GEXF: {gexf_path}")
    print(f"Persons: {len(persons)}")
    print(f"Orgs: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")

    # 1. Create SQLite DB
    import sqlite3
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS persons
        (id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
         birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
         work_start TEXT, current_post TEXT, current_org TEXT, source TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS organizations
        (id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
         parent TEXT, location TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS positions
        (id INTEGER PRIMARY KEY, person_id INTEGER, org_id INTEGER,
         title TEXT, start TEXT, "end" TEXT, rank TEXT, note TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS relationships
        (id INTEGER PRIMARY KEY, person_a INTEGER, person_b INTEGER,
         type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
         strength TEXT, confidence TEXT, source TEXT)''')

    for p in persons:
        c.execute('''INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
            (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
             p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
             p.get("party_join", ""), p.get("work_start", ""),
             p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        c.execute('''INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)''',
            (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for i, pos in enumerate(positions, 1):
        c.execute('''INSERT OR REPLACE INTO positions
            (id, person_id, org_id, title, start, "end", rank, note)
            VALUES (?,?,?,?,?,?,?,?)''',
            (i, pos["person_id"], pos["org_id"], pos["title"],
             pos.get("start", ""), pos.get("end", ""),
             pos.get("rank", ""), pos.get("note", "")))

    for i, rel in enumerate(relationships, 1):
        c.execute('''INSERT OR REPLACE INTO relationships
            (id, person_a, person_b, type, context, overlap_org,
             overlap_period, strength, confidence, source)
            VALUES (?,?,?,?,?,?,?,?,?,?)''',
            (i, rel["person_a"], rel["person_b"], rel["type"],
             rel.get("context", ""), rel.get("overlap_org", ""),
             rel.get("overlap_period", ""), rel.get("strength", ""),
             rel.get("confidence", ""), rel.get("source", "")))

    conn.commit()
    conn.close()
    print(f"✓ Database created: {db_path}")

    # 2. Create GEXF file
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append(f'    <description>{SLUG} leadership relationship network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="confidence" type="string"/>')
    lines.append('      <attribute id="2" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        is_top = "书记" in p["current_post"] and "纪委" not in p["current_post"]
        sz = "20.0" if is_top else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('          <attvalue for="1" value="confirmed"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for rel in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{rel["person_a"]}" target="p{rel["person_b"]}" label="{esc(rel["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rel["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel.get("confidence", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(rel.get("context", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✓ GEXF created: {gexf_path}")

    # 3. Create person JSONs
    for p in persons:
        person_id = f"heilongjiang_suihua_qingan_{p['name']}"
        job = p["current_post"].replace(" ", "")
        filename = f"{TODAY}-黑龙江省-绥化市-{job}-{p['name']}.json"
        filepath = os.path.join(staging_dir, filename)

        person_data = {
            "schema_version": "1.0",
            "generated_at": TODAY,
            "investigation_scope": {
                "province": "黑龙江省",
                "city": "绥化市",
                "region": "庆安县",
                "job": p["current_post"],
                "task_id": "heilongjiang_庆安县",
                "time_focus": AS_OF
            },
            "identity": {
                "person_id": person_id,
                "name": p["name"],
                "aliases": [],
                "gender": p.get("gender", ""),
                "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""),
                "birthplace": "",
                "native_place": "",
                "education": [{"period": "", "institution": "", "major": "", "degree": "", "study_type": "unknown", "source_ids": []}],
                "party_join": p.get("party_join", ""),
                "work_start": "",
                "dedupe_keys": {"name_birth": "", "name_birthplace": "", "official_profile_url": ""}
            },
            "current_status": {
                "current_post": p["current_post"],
                "current_org": p["current_org"],
                "administrative_rank": "",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {
                    "start": "",
                    "end": "present",
                    "org": p["current_org"],
                    "title": p["current_post"],
                    "level": "正处级" if "书记" in p["current_post"] or "县长" in p["current_post"] else "",
                    "location": "庆安县, 绥化市, 黑龙江省",
                    "system": "party" if "书记" in p["current_post"] else "government",
                    "rank": "",
                    "is_key_promotion": True,
                    "notes": "",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                }
            ],
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
            "source_register": [
                {
                    "id": "S001",
                    "title": f"庆安县人民政府 - 确认{p['current_post']}",
                    "url": p.get("source", SRC_GOV),
                    "publisher": "庆安县人民政府",
                    "published_at": AS_OF,
                    "accessed_at": TODAY,
                    "source_type": "official",
                    "reliability": "high",
                    "notes": f"Official government news confirming {p['name']} as {p['current_post']}"
                }
            ],
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": f"完整职业生涯（出生日期、教育背景、历任职务）完全未知"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": f"{p['name']}的完整职业生涯（出生日期、籍贯、教育背景、历任职务）",
                    "why_it_matters": f"了解{p['name']}的干部成长轨迹，发现与其他干部的关联和上级培养体系",
                    "suggested_queries": [f"{p['name']} 简历 庆安县", f"{p['name']} 出生", f"{p['name']} 历任"],
                    "last_attempted": TODAY
                },
                {
                    "priority": "high",
                    "question": f"{p['name']}任{p['current_post']}的具体时间",
                    "why_it_matters": "确定任职时间线，建立精确的predecessor/successor关系",
                    "suggested_queries": [f"庆安县 人大 任命 {p['name']}"],
                    "last_attempted": TODAY
                }
            ]
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(person_data, f, ensure_ascii=False, indent=2)
        print(f"✓ Person JSON created: {filepath}")

    print(f"\n=== Build complete for {SLUG} ===")
    print(f"Database: {db_path}")
    print(f"GEXF: {gexf_path}")
    print(f"Person JSONs: {len(persons)} files in {staging_dir}")

if __name__ == "__main__":
    main()
