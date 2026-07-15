#!/usr/bin/env python3
"""Build Ma'anshan (马鞍山市) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Sources:
  - www.mas.gov.cn (official government website, leadership page accessed 2026-07-15)
  - News articles on mas.gov.cn confirming mayor and party secretary activities

Confidence: Current roles confirmed from official mas.gov.cn leadership page;
  biographical details for most figures are partial (Baidu Baike and Wikipedia
  unavailable during research — 403/transport errors).
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "马鞍山市_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "马鞍山市_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ═══════════════════════════════════════════════════════════════════
    # Core leaders
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "袁方",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-07",
        "birthplace": "",
        "native_place": "",
        "education": "在职研究生，工学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共马鞍山市委",
        "source": "https://www.mas.gov.cn/zwgk/ldzc/",
        "notes": "主持市委全面工作。1969年7月出生，在职研究生学历，工学学士，中共党员。",
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "葛斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "马鞍山市人民政府",
        "source": "https://www.mas.gov.cn/zwgk/ldzc/",
        "notes": "市委副书记、市长，主持市政府全面工作。多次在新闻中出现（调研12345热线、与基石资本等会谈）。",
        "confidence": "confirmed"
    },
    {
        "id": 3,
        "name": "任生",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共马鞍山市委",
        "source": "https://www.mas.gov.cn/zwgk/ldzc/",
        "notes": "市委副书记。2026年7月14日在调研督导防汛工作中出现。",
        "confidence": "confirmed"
    },
    # ═══════════════════════════════════════════════════════════════════
    # Standing Committee (市委常委)
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": 4,
        "name": "程彰德",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共马鞍山市委",
        "source": "https://www.mas.gov.cn/zwgk/ldzc/",
        "notes": "市委常委。具体分工待确认，可能兼任政法委书记或副市长。",
        "confidence": "confirmed"
    },
    {
        "id": 5,
        "name": "马天奇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共马鞍山市委",
        "source": "https://www.mas.gov.cn/zwgk/ldzc/",
        "notes": "市委常委。具体分工待确认。",
        "confidence": "confirmed"
    },
    {
        "id": 6,
        "name": "刘芳",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共马鞍山市委",
        "source": "https://www.mas.gov.cn/zwgk/ldzc/",
        "notes": "市委常委。女性。具体分工待确认，可能兼任宣传部部长或统战部部长。",
        "confidence": "confirmed"
    },
    {
        "id": 7,
        "name": "杨军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共马鞍山市委",
        "source": "https://www.mas.gov.cn/zwgk/ldzc/",
        "notes": "市委常委。具体分工待确认。",
        "confidence": "confirmed"
    },
    {
        "id": 8,
        "name": "阙方俊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共马鞍山市委",
        "source": "https://www.mas.gov.cn/zwgk/ldzc/",
        "notes": "市委常委。具体分工待确认。",
        "confidence": "confirmed"
    },
    {
        "id": 9,
        "name": "陈红星",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共马鞍山市委",
        "source": "https://www.mas.gov.cn/zwgk/ldzc/",
        "notes": "市委常委。具体分工待确认。",
        "confidence": "confirmed"
    },
    {
        "id": 10,
        "name": "易茂林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共马鞍山市委",
        "source": "https://www.mas.gov.cn/zwgk/ldzc/",
        "notes": "市委常委。具体分工待确认。",
        "confidence": "confirmed"
    },
    # ═══════════════════════════════════════════════════════════════════
    # Secretary-General (市委秘书长)
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": 11,
        "name": "刘煜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委秘书长",
        "current_org": "中共马鞍山市委",
        "source": "https://www.mas.gov.cn/zwgk/ldzc/",
        "notes": "市委秘书长。",
        "confidence": "confirmed"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共马鞍山市委",
        "type": "党委",
        "level": "地级市",
        "parent": "中共安徽省委",
        "location": "马鞍山市"
    },
    {
        "id": 2,
        "name": "马鞍山市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "安徽省人民政府",
        "location": "马鞍山市"
    },
]

positions = [
    # 袁方
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "", "end": "present", "rank": "正厅级",
     "note": "主持市委全面工作。1969年7月出生。前任省长/副省级职务待确认。"},
    # 葛斌
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "正厅级",
     "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "", "end": "present", "rank": "正厅级",
     "note": "主持市政府全面工作。"},
    # 任生
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "副厅级",
     "note": "协助书记处理市委日常工作。"},
    # 程彰德
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级",
     "note": "具体分工待确认。"},
    # 马天奇
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级",
     "note": "具体分工待确认。"},
    # 刘芳
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级",
     "note": "具体分工待确认。"},
    # 杨军
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级",
     "note": "具体分工待确认。"},
    # 阙方俊
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级",
     "note": "具体分工待确认。"},
    # 陈红星
    {"person_id": 9, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级",
     "note": "具体分工待确认。"},
    # 易茂林
    {"person_id": 10, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级",
     "note": "具体分工待确认。"},
    # 刘煜
    {"person_id": 11, "org_id": 1, "title": "市委秘书长", "start": "", "end": "present", "rank": "正处级",
     "note": "市委秘书长。"},
]

relationships = [
    # 袁方 ↔ 葛斌 (党政正职搭档)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "党政正职搭档：袁方任市委书记，葛斌任市长",
     "overlap_org": "马鞍山市党政领导班子",
     "overlap_period": "",
     "strength": "strong",
     "confidence": "confirmed"},
    # 袁方 → 任生 (书记-副书记)
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "袁方为市委书记，任生为市委副书记，协助书记工作",
     "overlap_org": "中共马鞍山市委",
     "overlap_period": "",
     "strength": "strong",
     "confidence": "confirmed"},
    # 葛斌 → 任生 (市长-副书记)
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "同为市委领导班子成员，葛斌为副书记、市长，任生为专职副书记",
     "overlap_org": "中共马鞍山市委",
     "overlap_period": "",
     "strength": "strong",
     "confidence": "confirmed"},
    # 各位常委与书记袁方
    {"person_a": 4, "person_b": 1, "type": "superior_subordinate",
     "context": "程彰德为市委常委，受市委书记袁方领导",
     "overlap_org": "中共马鞍山市委",
     "overlap_period": "",
     "strength": "medium",
     "confidence": "confirmed"},
    {"person_a": 5, "person_b": 1, "type": "superior_subordinate",
     "context": "马天奇为市委常委，受市委书记袁方领导",
     "overlap_org": "中共马鞍山市委",
     "overlap_period": "",
     "strength": "medium",
     "confidence": "confirmed"},
    {"person_a": 6, "person_b": 1, "type": "superior_subordinate",
     "context": "刘芳为市委常委，受市委书记袁方领导",
     "overlap_org": "中共马鞍山市委",
     "overlap_period": "",
     "strength": "medium",
     "confidence": "confirmed"},
    {"person_a": 7, "person_b": 1, "type": "superior_subordinate",
     "context": "杨军为市委常委，受市委书记袁方领导",
     "overlap_org": "中共马鞍山市委",
     "overlap_period": "",
     "strength": "medium",
     "confidence": "confirmed"},
    {"person_a": 8, "person_b": 1, "type": "superior_subordinate",
     "context": "阙方俊为市委常委，受市委书记袁方领导",
     "overlap_org": "中共马鞍山市委",
     "overlap_period": "",
     "strength": "medium",
     "confidence": "confirmed"},
    {"person_a": 9, "person_b": 1, "type": "superior_subordinate",
     "context": "陈红星为市委常委，受市委书记袁方领导",
     "overlap_org": "中共马鞍山市委",
     "overlap_period": "",
     "strength": "medium",
     "confidence": "confirmed"},
    {"person_a": 10, "person_b": 1, "type": "superior_subordinate",
     "context": "易茂林为市委常委，受市委书记袁方领导",
     "overlap_org": "中共马鞍山市委",
     "overlap_period": "",
     "strength": "medium",
     "confidence": "confirmed"},
    # 刘煜 (秘书长) 与书记、副书记
    {"person_a": 11, "person_b": 1, "type": "superior_subordinate",
     "context": "刘煜为市委秘书长，协助市委书记袁方工作",
     "overlap_org": "中共马鞍山市委",
     "overlap_period": "",
     "strength": "strong",
     "confidence": "confirmed"},
    {"person_a": 11, "person_b": 2, "type": "superior_subordinate",
     "context": "刘煜为市委秘书长，在市委工作中配合市长葛斌",
     "overlap_org": "中共马鞍山市委",
     "overlap_period": "",
     "strength": "medium",
     "confidence": "confirmed"},
]


# ======================================================================
#  SQLite Builder
# ======================================================================

def build_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT,
            source TEXT, notes TEXT, confidence TEXT
        )
    """)
    c.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        )
    """)
    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        )
    """)
    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT, overlap_org TEXT,
            overlap_period TEXT, strength TEXT, confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""INSERT INTO persons VALUES
            (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"],
             p["birth"], p["birthplace"], p["education"],
             p["party_join"], p["work_start"],
             p["current_post"], p["current_org"],
             p["source"], p["notes"], p["confidence"]))

    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"],
             o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"],
             r["context"], r["overlap_org"],
             r["overlap_period"], r["strength"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"  ✓ Database: {DB_PATH}")
    print(f"    Persons: {len(persons)}")
    print(f"    Orgs:    {len(organizations)}")
    print(f"    Pos:     {len(positions)}")
    print(f"    Rel:     {len(relationships)}")


# ======================================================================
#  GEXF Builder (string-format to avoid ElementTree namespace issues)
# ======================================================================

def esc(s):
    """XML-escape."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def role_color(p):
    """Color by role."""
    post = p["current_post"]
    if "书记" in post and "市委" in post and "副" not in post:
        return "255,50,50"    # red — party secretary
    if "市长" in post and "副" not in post:
        return "50,100,255"   # blue — mayor
    if "副书记" in post:
        return "100,150,255"  # light blue — deputy secretary
    if "秘书长" in post:
        return "150,150,255"  # purple — secretary-general
    return "100,100,100"      # grey — other

def org_color(o):
    t = o["type"]
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "政协" in t:
        return "255,240,200"
    if "人大" in t:
        return "200,255,255"
    return "200,200,200"

def is_top(p):
    return p["id"] in (1, 2)   # 袁方 and 葛斌

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>马鞍山市领导班子工作关系网络 - 2026年7月</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # ── nodes ──
    lines.append('    <nodes>')
    for p in persons:
        c = role_color(p)
        sz = "20.0" if is_top(p) else "12.0"
        conf = p.get("confidence", "unverified")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{conf}"/>')
        lines.append('        </attvalues>')
        cs = c.split(",")
        lines.append(f'        <viz:color r="{cs[0]}" g="{cs[1]}" b="{cs[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c = org_color(o)
        cs = c.split(",")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append('          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{cs[0]}" g="{cs[1]}" b="{cs[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # ── edges ──
    lines.append('    <edges>')
    eid = 0

    # person→organization (worked_at)
    for pos in positions:
        pid = pos["person_id"]
        oid = pos["org_id"]
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person↔person (relationships)
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
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
    print(f"  ✓ GEXF: {GEXF_PATH}")
    print(f"    Nodes: {len(persons) + len(organizations)}")
    print(f"    Edges: {eid}")


# ======================================================================
#  Main
# ======================================================================

if __name__ == "__main__":
    print("Building 马鞍山市 leadership network data...")
    build_database()
    build_gexf()
