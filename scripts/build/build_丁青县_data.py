#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 丁青县 (Dingqing County), 昌都市, 西藏自治区.

Current officeholders as of 2026-07:
  - Party Secretary (县委书记): [待查 — web search degraded, names unconfirmed]
  - County Mayor (县长): [待查 — web search degraded, names unconfirmed]
  - Notable native: 白玛赤林 (Padma Choling), former Tibet Autonomous Region Government Chairman
    and former Vice Chairman of the NPC Standing Committee (born 丁青县)

IMPORTANT: Due to complete web access degradation (Exa rate-limited, Baidu 403/captcha,
Google 429, Bing timeout, all Chinese gov sites and baike unreachable from this environment),
this build represents a **minimal structural artifact** with placeholder data for the current
leadership. All current officeholder names/genders/ethnicity/birth are labeled as "待查" or
explicitly marked "unverified". Only confirmed data from existing repo artifacts is included.

Source: Existing repo artifacts (changdu build scripts, province build), known pattern.
"""

import sqlite3, os, json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TASK_ID = "xizang_丁青县"
STAGING = os.path.join(BASE, "data/tmp", TASK_ID)
DB_PATH = os.path.join(STAGING, "丁青县_network.db")
GEXF_PATH = os.path.join(STAGING, "丁青县_network.gexf")
TODAY = datetime.now().strftime("%Y-%m-%d")

os.makedirs(STAGING, exist_ok=True)

# =========================================================================
# PERSONS
# Confidence: confirmed = official source verified; plausible = credible media;
#             unverified = web degraded, unable to check
# =========================================================================
persons = [
    # ── 县委书记 (待确认) ──
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
        "current_post": "丁青县委书记",
        "current_org": "中共丁青县委员会",
        "source": "Web search fully unavailable — name cannot be confirmed. Try changdu.gov.cn leadership pages."
    },
    # ── 县长 (待确认) ──
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
        "current_post": "丁青县委副书记、县长",
        "current_org": "丁青县人民政府",
        "source": "Web search fully unavailable — name cannot be confirmed. Try changdu.gov.cn leadership pages."
    },
    # ── 白玛赤林 (丁青籍著名领导人, confirmed from repo artifacts) ──
    {
        "id": 3,
        "name": "白玛赤林",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1951-10",
        "birthplace": "西藏丁青",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "1969-12",
        "current_post": "原全国人大常委会副委员长（已退休）",
        "current_org": "全国人大常委会",
        "source": "scripts/build/build_changdu_data.py (verified via Baidu Baike before access degraded)"
    },
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共丁青县委员会", "type": "党委", "level": "县级",
     "parent": "中共昌都市委员会", "location": "西藏自治区昌都市丁青县"},
    {"id": 2, "name": "丁青县人民政府", "type": "政府", "level": "县级",
     "parent": "昌都市人民政府", "location": "西藏自治区昌都市丁青县"},
    {"id": 3, "name": "丁青县人大常委会", "type": "人大", "level": "县级",
     "parent": "丁青县", "location": "西藏自治区昌都市丁青县"},
    {"id": 4, "name": "政协丁青县委员会", "type": "政协", "level": "县级",
     "parent": "丁青县", "location": "西藏自治区昌都市丁青县"},
    {"id": 5, "name": "中共丁青县纪律检查委员会", "type": "党委", "level": "县级",
     "parent": "中共丁青县委员会", "location": "西藏自治区昌都市丁青县"},
    {"id": 6, "name": "丁青县监察委员会", "type": "政府", "level": "县级",
     "parent": "丁青县", "location": "西藏自治区昌都市丁青县"},
    {"id": 7, "name": "丁青县人民法院", "type": "政府", "level": "县级",
     "parent": "丁青县", "location": "西藏自治区昌都市丁青县"},
    {"id": 8, "name": "丁青县人民检察院", "type": "政府", "level": "县级",
     "parent": "丁青县", "location": "西藏自治区昌都市丁青县"},
    {"id": 9, "name": "中共丁青县委组织部", "type": "党委", "level": "县级",
     "parent": "中共丁青县委员会", "location": "西藏自治区昌都市丁青县"},
    {"id": 10, "name": "全国人大常委会", "type": "人大", "level": "国家级",
     "parent": "", "location": "北京市"},
    {"id": 11, "name": "西藏自治区人民政府", "type": "政府", "level": "省级",
     "parent": "", "location": "西藏自治区拉萨市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 县委书记 (待确认)
    {"person_id": 1, "org_id": 1, "title": "丁青县委书记",
     "start_date": "unknown", "end_date": "present", "rank": "正处级",
     "note": "当前任职者待确认 — web search unavailable"},
    # 县长 (待确认)
    {"person_id": 2, "org_id": 2, "title": "丁青县县长",
     "start_date": "unknown", "end_date": "present", "rank": "正处级",
     "note": "当前任职者待确认 — web search unavailable"},
    # 白玛赤林 — 丁青籍全国人大常委会副委员长
    {"person_id": 3, "org_id": 10, "title": "全国人大常委会副委员长",
     "start_date": "2013-03", "end_date": "2023-03", "rank": "副国级",
     "note": "昌都丁青人，已退休"},
    {"person_id": 3, "org_id": 11, "title": "西藏自治区政府主席",
     "start_date": "2010-01", "end_date": "2013-01", "rank": "正部级",
     "note": ""},
    {"person_id": 3, "org_id": 11, "title": "西藏自治区政府常务副主席",
     "start_date": "2006", "end_date": "2010-01", "rank": "副部级",
     "note": ""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 书记—县长（当前搭档）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "丁青县委书记与县长为党政一把手搭档（具体姓名待确认）",
     "overlap_org": "中共丁青县委员会/丁青县人民政府",
     "overlap_period": "至今"},
]

# =========================================================================
# GENERATION FUNCTIONS
# =========================================================================
def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    title = p.get("current_post","")
    if "书记" in title and "纪委" not in title and "统战" not in title:
        return "255,50,50"
    if "县长" in title or "市长" in title:
        return "50,100,255"
    if "纪委书记" in title or "监察" in title:
        return "255,165,0"
    if "人大" in title:
        return "200,255,255"
    if "政协" in title:
        return "255,240,200"
    return "100,100,100"

def org_color(o):
    ot = o.get("type","")
    if "党委" == ot: return "255,200,200"
    if "政府" in ot: return "200,200,255"
    if "人大" in ot: return "200,255,255"
    if "政协" in ot: return "255,240,200"
    return "200,200,200"

def is_top_leader(p):
    title = p.get("current_post","")
    return ("书记" in title and "纪委" not in title and "统战" not in title) or "县长" in title

def build_db():
    conn = sqlite3.connect(str(DB_PATH))

    # DDL
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS persons(
            id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations(
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, "end" TEXT, rank TEXT, note TEXT
        );
        CREATE TABLE IF NOT EXISTS relationships(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT
        );
    """)

    # Insert persons
    for p in persons:
        conn.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p.get("gender",""), p.get("ethnicity",""),
             p.get("birth",""), p.get("birthplace",""), p.get("education",""),
             p.get("party_join",""), p.get("work_start",""),
             p.get("current_post",""), p.get("current_org",""), p.get("source","")))

    # Insert organizations
    for o in organizations:
        conn.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o.get("type",""), o.get("level",""),
             o.get("parent",""), o.get("location","")))

    # Insert positions
    for pos in positions:
        conn.execute("INSERT INTO positions (person_id, org_id, title, \"start\", \"end\", rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos.get("start_date",""), pos.get("end_date",""),
             pos.get("rank",""), pos.get("note","")))

    # Insert relationships
    for rel in relationships:
        conn.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (rel["person_a"], rel["person_b"], rel["type"],
             rel["context"], rel.get("overlap_org",""), rel.get("overlap_period","")))

    conn.commit()

    # Verify counts
    for table in ["persons", "organizations", "positions", "relationships"]:
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {count} rows")
    conn.close()
    print(f"DB written: {DB_PATH}")

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append(f'    <description>丁青县领导班子工作关系网络 — {len(persons)} persons, {len(organizations)} orgs, {len(positions)+len(relationships)} edges (PARTIAL — current leaders unconfirmed, web unavailable)</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="title" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <nodes>')
    for p in persons:
        sz = "20.0" if is_top_leader(p) else "12.0"
        c = person_color(p).split(",")
        pid = p["id"]
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_post",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c = org_color(o).split(",")
        oid = o["id"]
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos.get("title",""))}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("start_date",""))}-{esc(pos.get("end_date",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for rel in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{rel["person_a"]}" target="p{rel["person_b"]}" label="{esc(rel.get("type",""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rel.get("type",""))}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(rel.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")

if __name__ == "__main__":
    print(f"Building 丁青县 network data...")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  NOTE: Current leaders marked '待确认' — web search fully degraded")
    build_db()
    build_gexf()
    print(f"\nDone. DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")