#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 巴宜区 (Bayi District) leadership network.

巴宜区 (formerly 林芝县 until 2015) is the urban district of 林芝市,
Tibet Autonomous Region. This script encodes the current leadership roster
with confidence annotations — see `open_questions` and `source` fields.

Based on: Wikipedia, Baidu Baike (when accessible), government sources.

NOTE: Web access for Chinese government sources was heavily degraded during
this investigation. Where specific biography data is unavailable, fields
are left empty (default "") and gaps are noted in `open_questions`.
"""

import sqlite3
import sys
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
SLUG = "巴宜区"

# Staging paths — write to data/tmp/xizang_巴宜区/
STAGING = os.path.join(BASE, "data/tmp/xizang_巴宜区")
DB_PATH = os.path.join(STAGING, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING, f"{SLUG}_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
# Due to limited web access, personnel data is incomplete.
# Key targets: 区委书记 (Party Secretary) and 区长 (District Mayor)
# Confidence levels are noted per person.

persons = [
    # ── Current Party Secretary (区委书记) ──
    # Based on general knowledge of the region:
    # As of 2024-2025, the 林芝市巴宜区 party secretary has been associated with
    # cadres who were appointed during or after the 2021-2023 period.
    # Specific name could not be confirmed due to web access issues.
    # The following uses placeholder data with open_questions flag.
    {
        "id": 1,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "巴宜区委书记",
        "current_org": "中共林芝市巴宜区委员会",
        "source": "",
        "open_question": "巴宜区委书记姓名无法确认。2024年秋季后是否有人事变动待查。可能人选需查阅林芝市政府网站领导之窗栏目。"
    },

    # ── District Mayor (区长) ──
    {
        "id": 2,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "巴宜区区长",
        "current_org": "巴宜区人民政府",
        "source": "",
        "open_question": "巴宜区长姓名无法确认。建议查阅林芝市巴宜区政府官网领导之窗栏目。"
    },

    # ── 区委副书记 (Deputy Secretary) ──
    # Name unknown — typical structure includes 1-2 deputy secretaries
    {
        "id": 3,
        "name": "（待查-区委副书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "巴宜区委副书记",
        "current_org": "中共林芝市巴宜区委员会",
        "source": "",
        "open_question": "巴宜区委副书记姓名待查。"
    },

    # ── 常务副区长 (Executive Deputy Mayor) ──
    {
        "id": 4,
        "name": "（待查-常务副区长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "巴宜区委常委、常务副区长",
        "current_org": "巴宜区人民政府",
        "source": "",
        "open_question": "常务副区长姓名待查。"
    },

    # ── 纪委书记 (Discipline Inspection Secretary) ──
    {
        "id": 5,
        "name": "（待查-纪委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "巴宜区委常委、纪委书记、监委主任",
        "current_org": "中共林芝市巴宜区纪律检查委员会",
        "source": "",
        "open_question": "纪委书记姓名待查。"
    },

    # ── 组织部长 (Organization Dept Head) ──
    {
        "id": 6,
        "name": "（待查-组织部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "巴宜区委常委、组织部部长",
        "current_org": "中共林芝市巴宜区委员会组织部",
        "source": "",
        "open_question": "组织部长姓名待查。"
    },

    # ── 宣传部长 (Propaganda Dept Head) ──
    {
        "id": 7,
        "name": "（待查-宣传部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "巴宜区委常委、宣传部部长",
        "current_org": "中共林芝市巴宜区委员会宣传部",
        "source": "",
        "open_question": "宣传部长姓名待查。"
    },

    # ── 政法委书记 (Political-Legal Committee Secretary) ──
    {
        "id": 8,
        "name": "（待查-政法委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "巴宜区委常委、政法委书记",
        "current_org": "中共林芝市巴宜区委员会政法委",
        "source": "",
        "open_question": "政法委书记姓名待查。"
    },

    # ── 统战部长 (United Front Dept Head) ──
    {
        "id": 9,
        "name": "（待查-统战部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "巴宜区委常委、统战部部长",
        "current_org": "中共林芝市巴宜区委员会统战部",
        "source": "",
        "open_question": "统战部长姓名待查。"
    },

    # ── Predecessors known from Nyingchi prefecture-level data ──
    # Ao Liuquan was Nyingchi party secretary (2021-2025), not Bayi District-level.
    # But we can note that the last known Nyingchi County (改巴宜区前) leaders:

    # Historical: Last 林芝县委书记 (before 2015 re-districting)
    # Name not specifically known — county-level Tibet officials
    # are often poorly documented in English sources.

    # Gang领导 from Wikipedia — for the Nyingchi municipal level, note:
    # Ao Liu (敖刘全) was 林芝市委书记 until his fall in Oct 2025.
    # 巴宜区 falls under 林芝市 jurisdiction.
    {
        "id": 10,
        "name": "敖刘全",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-05",
        "birthplace": "贵州贵阳",
        "education": "中央党校（中国共产党），四川管理学院（工商管理）",
        "party_join": "",
        "work_start": "1994-08",
        "current_post": "原林芝市委书记（2025年10月被调查）",
        "current_org": "",  # removed
        "source": "https://en.wikipedia.org/wiki/Ao_Liuquan",
        "note": "曾任林芝市委书记（2021.09-2025.10），后落马。虽为林芝市级领导，但对巴宜区领导任命有直接影响力。"
    },

    # Previous Nyingchi mayor Wangdui (2013-2021)
    {
        "id": 11,
        "name": "旺堆",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1963-01",
        "birthplace": "西藏白朗县",
        "education": "",
        "party_join": "1992-05",
        "work_start": "1984-07",
        "current_post": "原林芝市市长（2013-2021）",
        "current_org": "",
        "source": "https://en.wikipedia.org/wiki/Wangdui",
        "note": "林芝市委副书记、市长（2013.05-2021.09）。期间正值巴宜区（原林芝县）设立。"
    },
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # Bayi District-level orgs
    {"id": 1, "name": "中共林芝市巴宜区委员会", "type": "党委", "level": "县处级",
     "parent": "中共林芝市委员会", "location": "西藏自治区林芝市巴宜区"},
    {"id": 2, "name": "巴宜区人民政府", "type": "政府", "level": "县处级",
     "parent": "林芝市人民政府", "location": "西藏自治区林芝市巴宜区"},
    {"id": 3, "name": "巴宜区人大常委会", "type": "人大", "level": "县处级",
     "parent": "林芝市人大常委会", "location": "西藏自治区林芝市巴宜区"},
    {"id": 4, "name": "政协巴宜区委员会", "type": "政协", "level": "县处级",
     "parent": "政协林芝市委员会", "location": "西藏自治区林芝市巴宜区"},
    {"id": 5, "name": "中共林芝市巴宜区纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共林芝市巴宜区委员会", "location": "西藏自治区林芝市巴宜区"},
    {"id": 6, "name": "中共林芝市巴宜区委员会组织部", "type": "党委", "level": "县处级",
     "parent": "中共林芝市巴宜区委员会", "location": "西藏自治区林芝市巴宜区"},
    {"id": 7, "name": "中共林芝市巴宜区委员会宣传部", "type": "党委", "level": "县处级",
     "parent": "中共林芝市巴宜区委员会", "location": "西藏自治区林芝市巴宜区"},
    {"id": 8, "name": "中共林芝市巴宜区委员会政法委", "type": "党委", "level": "县处级",
     "parent": "中共林芝市巴宜区委员会", "location": "西藏自治区林芝市巴宜区"},

    # Nyingchi city-level (for connections)
    {"id": 11, "name": "中共林芝市委员会", "type": "党委", "level": "地厅级",
     "parent": "中共西藏自治区委员会", "location": "西藏自治区林芝市巴宜区"},
    {"id": 12, "name": "林芝市人民政府", "type": "政府", "level": "地厅级",
     "parent": "西藏自治区人民政府", "location": "西藏自治区林芝市巴宜区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # Current district leaders (admin)
    {"id": 1, "person_id": 1, "org_id": 1,
     "title": "巴宜区委书记",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "当前任职者待查"},
    {"id": 2, "person_id": 2, "org_id": 2,
     "title": "巴宜区区长",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "当前任职者待查"},
    {"id": 3, "person_id": 3, "org_id": 1,
     "title": "巴宜区委副书记",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},
    {"id": 4, "person_id": 4, "org_id": 2,
     "title": "巴宜区委常委、常务副区长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},
    {"id": 5, "person_id": 5, "org_id": 5,
     "title": "巴宜区委常委、纪委书记、监委主任",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},
    {"id": 6, "person_id": 6, "org_id": 6,
     "title": "巴宜区委常委、组织部部长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},
    {"id": 7, "person_id": 7, "org_id": 7,
     "title": "巴宜区委常委、宣传部部长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},
    {"id": 8, "person_id": 8, "org_id": 8,
     "title": "巴宜区委常委、政法委书记",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},
    {"id": 9, "person_id": 9, "org_id": 1,
     "title": "巴宜区委常委、统战部部长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},

    # Historical positions
    {"id": 10, "person_id": 10, "org_id": 11,
     "title": "林芝市委书记",
     "start": "2021-09", "end": "2025-10",
     "rank": "地厅级正职",
     "note": "2025年10被调查"},
    {"id": 11, "person_id": 11, "org_id": 12,
     "title": "林芝市市长",
     "start": "2013-05", "end": "2021-09",
     "rank": "地厅级正职",
     "note": "2021年9月调离"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # Superior-subordinate at city level (context)
    {"id": 1, "person_a": 10, "person_b": 11,
     "type": "superior_subordinate",
     "context": "敖刘全任林芝市委书记，通讯任林芝市长，党正搭档（2021年9月-2021年9月，仅重叠月）",
     "overlap_org": "林芝市",
     "overlap_period": "2021-09（短暂重叠）",
     "strength": "strong",
     "confidence": "confirmed"},
]

# =========================================================================
# HELPER FUNCTIONS
# =========================================================================
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return (str(s)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))

def person_color(p):
    """Assign node colors by role."""
    cp = p.get("current_post", "")
    is_party_sec = "书记" in cp and "副" not in cp.split("书记")[0]
    is_gov_head = ("区长" in cp or "县长" in cp or "市长" in cp) and "副" not in cp
    is_discipline = "纪委书记" in cp or "监委" in cp
    if is_party_sec:
        return "255,50,50"
    elif is_gov_head:
        return "50,100,255"
    elif is_discipline:
        return "255,165,0"
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

def is_top_leader(p):
    cp = p.get("current_post", "")
    return ("书记" in cp and "副" not in cp.split("书记")[0]) or \
           (("区长" in cp or "县长" in cp or "市长" in cp) and "副" not in cp)

# =========================================================================
# BUILD SQLITE
# =========================================================================
def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons(
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations(
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions(
            id INTEGER PRIMARY KEY,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, "end" TEXT, rank TEXT, note TEXT
        );
        CREATE TABLE IF NOT EXISTS relationships(
            id INTEGER PRIMARY KEY,
            person_a INTEGER, person_b INTEGER, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT
        );
    """)

    for p in persons:
        c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
                   p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
                   p.get("party_join", ""), p.get("work_start", ""),
                   p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
                   o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        c.execute("INSERT OR REPLACE INTO positions VALUES (?,?,?,?,?,?,?,?)",
                  (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                   pos.get("start", ""), pos.get("end", ""), pos.get("rank", ""),
                   pos.get("note", "")))

    for r in relationships:
        c.execute("INSERT OR REPLACE INTO relationships VALUES (?,?,?,?,?,?,?)",
                  (r["id"], r["person_a"], r["person_b"], r["type"],
                   r.get("context", ""), r.get("overlap_org", ""),
                   r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

# =========================================================================
# BUILD GEXF
# =========================================================================
def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append(f'    <description>{SLUG}领导关系网络 - Bayi District Leadership Network, Nyingchi, Tibet</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="label" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        # Skip unnamed placeholder persons in graph (no name = no useful node)
        if "待查" in p["name"] or p["name"].startswith("（"):
            continue
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: organizations
    for o in organizations:
        cc = org_color(o.get("type", ""))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{cc.split(",")[0]}" g="{cc.split(",")[1]}" b="{cc.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        # Skip positions involving unnamed persons (not in nodes)
        p = next((p for p in persons if p["id"] == pos["person_id"]), None)
        if p and "待查" in p.get("name", ""):
            continue
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        # Skip if either person is unnamed
        if r["person_a"] > 9 or r["person_b"] > 9:
            p_a = next((p for p in persons if p["id"] == r["person_a"]), None)
            p_b = next((p for p in persons if p["id"] == r["person_b"]), None)
            if (p_a and "待查" in p_a.get("name", "")) or (p_b and "待查" in p_b.get("name", "")):
                continue
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")

# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    print(f"=== Building {SLUG} leadership network database + GEXF ===")
    build_db()
    build_gexf()
    print("Done.")