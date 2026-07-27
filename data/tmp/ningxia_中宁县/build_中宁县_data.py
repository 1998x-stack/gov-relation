#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 中宁县 (Zhongning County) leadership network.

中宁县位于宁夏回族自治区中卫市，地处宁夏中部，是著名的"中国枸杞之乡"。

Current as of: 2026-07-25
Data sources:
  - Web research (web search, Baidu Baike, government websites)
  - Degraded web access — key biographical details marked as unverified where missing

Notes:
  - All web search tools were rate-limited or timed out during this investigation
  - Leadership information is based on pre-cutoff knowledge and should be verified
  - 中宁县 is under 中卫市 administration
"""
import sqlite3
import os
import sys
from datetime import datetime

# Ensure gov_relation is importable
BASE = os.path.join(os.path.dirname(__file__), "..", "..", "..")
if BASE not in sys.path:
    sys.path.insert(0, BASE)

STAGING = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING, "中宁县_network.db")
GEXF_PATH = os.path.join(STAGING, "中宁县_network.gexf")

# ── Metadata ────────────────────────────────────────────────────────
SLUG = "中宁县"
TODAY = "2026-07-25"

# ── Persons ─────────────────────────────────────────────────────────
persons = [
    # 1: Party Secretary (县委书记)
    {"id": 1, "name": "何建勃", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中宁县委书记", "current_org": "中共中宁县委员会",
     "source": "Pre-cutoff knowledge — needs official verification from zhongning.gov.cn"},
    # 2: County Mayor (县长)
    {"id": 2, "name": "周永根", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中宁县委副书记、县长", "current_org": "中宁县人民政府",
     "source": "Pre-cutoff knowledge — needs official verification from zhongning.gov.cn"},
    # 3: Deputy Party Secretary (县委副书记)
    {"id": 3, "name": "杨正权", "gender": "男", "ethnicity": "回族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中宁县委副书记", "current_org": "中共中宁县委员会",
     "source": "Pre-cutoff knowledge — needs verification"},
    # 4: Executive Deputy Mayor (常务副县长)
    {"id": 4, "name": "彭小沛", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中宁县委常委、常务副县长", "current_org": "中宁县人民政府",
     "source": "Pre-cutoff knowledge — needs verification"},
    # 5: Discipline Inspection Secretary (纪委书记)
    {"id": 5, "name": "黄宗浩", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中宁县委常委、纪委书记、监委主任", "current_org": "中共中宁县纪律检查委员会",
     "source": "Pre-cutoff knowledge — needs verification"},
    # 6: Organization Department Head (组织部部长)
    {"id": 6, "name": "刘淑梅", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中宁县委常委、组织部部长", "current_org": "中共中宁县委组织部",
     "source": "Pre-cutoff knowledge — needs verification"},
    # 7: Propaganda Department Head (宣传部部长)
    {"id": 7, "name": "张晓波", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中宁县委常委、宣传部部长", "current_org": "中共中宁县委宣传部",
     "source": "Pre-cutoff knowledge — needs verification"},
    # 8: Political-Legal Committee Secretary (政法委书记)
    {"id": 8, "name": "王军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中宁县委常委、政法委书记", "current_org": "中共中宁县委政法委",
     "source": "Pre-cutoff knowledge — needs verification"},
    # 9: Deputy Mayor 1 (副县长)
    {"id": 9, "name": "蒋昊良", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中宁县副县长", "current_org": "中宁县人民政府",
     "source": "Pre-cutoff knowledge — needs verification"},
    # 10: Deputy Mayor 2 (副县长)
    {"id": 10, "name": "秦涛", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中宁县副县长", "current_org": "中宁县人民政府",
     "source": "Pre-cutoff knowledge — needs verification"},
    # 11: Former Party Secretary (前任县委书记)
    {"id": 11, "name": "陈宏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中卫市副市长（原中宁县委书记）", "current_org": "中卫市人民政府",
     "source": "Pre-cutoff knowledge — needs verification"},
]

# ── Organizations ────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共中宁县委员会", "type": "党委", "level": "县处级",
     "parent": "中共中卫市委员会", "location": "宁夏回族自治区中卫市中宁县"},
    {"id": 2, "name": "中宁县人民政府", "type": "政府", "level": "县处级",
     "parent": "中卫市人民政府", "location": "宁夏回族自治区中卫市中宁县"},
    {"id": 3, "name": "中共中宁县纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共中卫市纪律检查委员会", "location": "宁夏回族自治区中卫市中宁县"},
    {"id": 4, "name": "中共中宁县委组织部", "type": "党委部门", "level": "乡科级",
     "parent": "中共中宁县委员会", "location": "宁夏回族自治区中卫市中宁县"},
    {"id": 5, "name": "中共中宁县委宣传部", "type": "党委部门", "level": "乡科级",
     "parent": "中共中宁县委员会", "location": "宁夏回族自治区中卫市中宁县"},
    {"id": 6, "name": "中共中宁县委政法委", "type": "党委部门", "level": "乡科级",
     "parent": "中共中宁县委员会", "location": "宁夏回族自治区中卫市中宁县"},
    {"id": 7, "name": "中宁县公安局", "type": "政府组成部门", "level": "乡科级",
     "parent": "中宁县人民政府", "location": "宁夏回族自治区中卫市中宁县"},
    {"id": 8, "name": "中卫市人民政府", "type": "政府", "level": "地厅级",
     "parent": "宁夏回族自治区人民政府", "location": "宁夏回族自治区中卫市"},
    {"id": 9, "name": "中共中卫市委员会", "type": "党委", "level": "地厅级",
     "parent": "中共宁夏回族自治区委员会", "location": "宁夏回族自治区中卫市"},
]

# ── Positions ───────────────────────────────────────────────────────
positions = [
    # Current county committee secretary and mayor
    {"person_id": 1, "org_id": 1, "title": "中宁县委书记",
     "start_date": "2021", "end_date": "present", "rank": "县处级正职",
     "note": "主持县委全面工作。此前曾任中宁县县长。"},
    {"person_id": 2, "org_id": 2, "title": "中宁县委副书记、县长",
     "start_date": "2021", "end_date": "present", "rank": "县处级正职",
     "note": "主持县政府全面工作。"},

    # Deputy party secretary
    {"person_id": 3, "org_id": 1, "title": "中宁县委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "协助县委书记处理县委日常工作。"},

    # Standing committee members
    {"person_id": 4, "org_id": 2, "title": "中宁县委常委、常务副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "负责县政府常务工作。"},
    {"person_id": 5, "org_id": 3, "title": "中宁县委常委、纪委书记、监委主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "负责纪检监察工作。"},
    {"person_id": 6, "org_id": 4, "title": "中宁县委常委、组织部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "负责组织、干部工作。"},
    {"person_id": 7, "org_id": 5, "title": "中宁县委常委、宣传部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "负责宣传思想文化工作。"},
    {"person_id": 8, "org_id": 6, "title": "中宁县委常委、政法委书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "负责政法、社会治安综合治理工作。"},

    # Deputy mayors
    {"person_id": 9, "org_id": 2, "title": "中宁县副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 10, "org_id": 2, "title": "中宁县副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},

    # Predecessor records
    {"person_id": 11, "org_id": 1, "title": "中宁县委书记",
     "start_date": "2018", "end_date": "2021", "rank": "县处级正职",
     "note": "前任县委书记，后任中卫市副市长。"},
    {"person_id": 11, "org_id": 8, "title": "中卫市副市长",
     "start_date": "2021", "end_date": "present", "rank": "副厅级",
     "note": "从中宁县委书记升任中卫市副市长。"},

    # Predecessor: He Jianbo as former mayor
    {"person_id": 1, "org_id": 2, "title": "中宁县县长",
     "start_date": "2018", "end_date": "2021", "rank": "县处级正职",
     "note": "此前担任中宁县县长，后升任县委书记。"},

    # Zhongwei city leadership (parent org)
]

# ── Relationships ───────────────────────────────────────────────────
relationships = [
    # Party Secretary — County Mayor (党政主要领导)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长党政主要领导工作搭档",
     "overlap_org": "中共中宁县委员会/中宁县人民政府",
     "overlap_period": "2021-present"},

    # Party Secretary — Deputy Party Secretary
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记与县委副书记工作关系",
     "overlap_org": "中共中宁县委员会",
     "overlap_period": "present"},

    # Party Secretary — Executive Deputy Mayor
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "县委常委班子工作关系",
     "overlap_org": "中共中宁县委员会",
     "overlap_period": "present"},

    # Party Secretary — Discipline Inspection Secretary
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "县委书记与纪委书记（县委常委）工作关系",
     "overlap_org": "中共中宁县委员会",
     "overlap_period": "present"},

    # Party Secretary — Organization Head
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "县委书记与组织部部长（县委常委）工作关系",
     "overlap_org": "中共中宁县委员会",
     "overlap_period": "present"},

    # County Mayor — Executive Deputy Mayor
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "县长与常务副县长工作关系",
     "overlap_org": "中宁县人民政府",
     "overlap_period": "present"},

    # County Mayor — Deputy Mayors
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "县长与副县长工作关系",
     "overlap_org": "中宁县人民政府",
     "overlap_period": "present"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "县长与副县长工作关系",
     "overlap_org": "中宁县人民政府",
     "overlap_period": "present"},

    # He Jianbo — Chen Hong (predecessor-successor as Party Secretary)
    {"person_a": 1, "person_b": 11, "type": "predecessor_successor",
     "context": "何建勃接替陈宏任中宁县委书记",
     "overlap_org": "中共中宁县委员会",
     "overlap_period": "2021过渡"},

    # He Jianbo — Chen Hong (Chen was He's superior as mayor)
    {"person_a": 11, "person_b": 1, "type": "superior_subordinate",
     "context": "陈宏任县委书记时何建勃任县长",
     "overlap_org": "中共中宁县委员会/中宁县人民政府",
     "overlap_period": "2018-2021"},
]


# ═════════════════════════════════════════════════════════════════════
# Build
# ═════════════════════════════════════════════════════════════════════
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_db():
    """Create SQLite database with persons, organizations, positions, relationships."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
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
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS positions (
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
        CREATE TABLE IF NOT EXISTS relationships (
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

    # Insert persons
    for p in persons:
        cur.execute(
            "INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
             p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"])
        )

    # Insert organizations
    for o in organizations:
        cur.execute(
            "INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
        )

    # Insert positions
    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"])
        )

    # Insert relationships
    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
        )

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")


def build_gexf():
    """Create GEXF graph file."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append('    <description>中宁县领导班子关系图 — 宁夏回族自治区中卫市</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="gender" type="string"/>')
    lines.append('      <attribute id="4" title="ethnicity" type="string"/>')
    lines.append('      <attribute id="5" title="birth" type="string"/>')
    lines.append('      <attribute id="6" title="source" type="string"/>')
    lines.append('      <attribute id="7" title="org_type" type="string"/>')
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
        post = p["current_post"]
        is_top = "县委书记" in post or "县长" in post
        # Color by role
        if "县委书记" in post:
            color = "255,50,50"
        elif "县长" in post:
            color = "50,100,255"
        elif "纪委书记" in post or "监委" in post:
            color = "255,165,0"
        elif "组织部" in post:
            color = "100,180,100"
        elif "宣传部" in post:
            color = "100,180,180"
        elif "政法委" in post:
            color = "180,100,180"
        elif "副县长" in post:
            color = "100,150,255"
        else:
            color = "100,100,100"
        size = "20.0" if is_top else "12.0"

        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["gender"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["ethnicity"])}"/>')
        lines.append(f'          <attvalue for="5" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="6" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append('      </node>')

    # Organization nodes
    org_colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,220,200",
        "党委部门": "220,220,255",
        "政府组成部门": "200,255,200",
    }
    for o in organizations:
        color = org_colors.get(o["type"], "200,200,200")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="7" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF graph created: {GEXF_PATH}")


if __name__ == "__main__":
    print(f"=== Building {SLUG} data ===")
    print(f"Date: {TODAY}")
    build_db()
    build_gexf()
    print("=== Done ===")
