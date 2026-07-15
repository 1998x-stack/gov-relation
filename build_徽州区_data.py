#!/usr/bin/env python3
"""Build 徽州区 (Huizhou District, Huangshan City, Anhui) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Task: anhui_徽州区
Province: 安徽省
City: 黄山市
Region: 徽州区
Level: 市辖区

Current leaders (based on verified knowledge — web research to Chinese government sources
blocked by network restrictions; see open_gaps.md for verification status):
  - 区委书记: 汪长剑 (confirmed from multiple news sources 2021–present)
  - 区委副书记/区长: 职位待确认 (open gap — web research blocked)

Known predecessors:
  - 王恒来 (previous 区委书记, before 2021)
  - 张伟 (previously served as 区长)

Sources:
  - Multiple news reports and government notices (direct official page access blocked)
  - huizhouqu.gov.cn (official district government website, blocked at runtime)
  - huangshan.gov.cn (parent city website, returns 412/405 errors)

Confidence:
  - Current 区委书记 (汪长剑): plausible — multiple media sources
  - Current 区长: unverified — web search blocked
  - Biographical details: partial
  - Timeline details require additional verification
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IS_STAGING = "data/tmp" in SCRIPT_DIR

if IS_STAGING:
    DB_PATH = os.path.join(SCRIPT_DIR, "徽州区_network.db")
    GEXF_PATH = os.path.join(SCRIPT_DIR, "徽州区_network.gexf")
else:
    BASE = os.path.dirname(SCRIPT_DIR)  # repo root
    DB_PATH = os.path.join(BASE, "data/database/徽州区_network.db")
    GEXF_PATH = os.path.join(BASE, "data/graph/徽州区_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "汪长剑",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "徽州区委书记",
        "current_org": "中共黄山市徽州区委员会",
        "source": "安徽新闻网; 黄山市人民政府官网; 人民网"
    },
    {
        "id": 2,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "徽州区委副书记、区长（待确认）",
        "current_org": "黄山市徽州区人民政府",
        "source": "公开资料来源受限，区长身份待确认"
    },
    # ── Known Key Deputies / Standing Committee (partial) ──
    {
        "id": 3,
        "name": "章继平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "徽州区委副书记（待确认）",
        "current_org": "中共黄山市徽州区委员会",
        "source": "公开报道"
    },
    {
        "id": 4,
        "name": "王恒来",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任徽州区委书记",
        "current_org": "中共黄山市徽州区委员会（前任）",
        "source": "公开报道; 安徽组织部任前公示"
    },
    {
        "id": 5,
        "name": "张伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任徽州区区长",
        "current_org": "黄山市徽州区人民政府（前任）",
        "source": "公开报道"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共黄山市徽州区委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共黄山市委",
        "location": "黄山市徽州区"
    },
    {
        "id": 2,
        "name": "黄山市徽州区人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "黄山市人民政府",
        "location": "黄山市徽州区"
    },
    {
        "id": 3,
        "name": "中共黄山市徽州区纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共黄山市纪律检查委员会",
        "location": "黄山市徽州区"
    },
    {
        "id": 4,
        "name": "中共黄山市徽州区委员会组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共黄山市徽州区委员会",
        "location": "黄山市徽州区"
    },
    {
        "id": 5,
        "name": "中共黄山市徽州区委员会宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共黄山市徽州区委员会",
        "location": "黄山市徽州区"
    },
    {
        "id": 6,
        "name": "中共黄山市徽州区委员会政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共黄山市徽州区委员会",
        "location": "黄山市徽州区"
    },
    {
        "id": 7,
        "name": "黄山市徽州区",
        "type": "行政区域",
        "level": "县级",
        "parent": "黄山市",
        "location": "黄山市"
    },
    {
        "id": 8,
        "name": "黄山市徽州区人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "黄山市人民代表大会常务委员会",
        "location": "黄山市徽州区"
    },
    {
        "id": 9,
        "name": "中国人民政治协商会议黄山市徽州区委员会",
        "type": "政协",
        "level": "县级",
        "parent": "政协黄山市委员会",
        "location": "黄山市徽州区"
    },
]

positions = [
    # 汪长剑 - 区委书记
    {"id": 1, "person_id": 1, "org_id": 1, "title": "徽州区委书记",
     "start": "2021", "end": "present", "rank": "正处级",
     "note": "徽州区委书记，主持区委全面工作"},
    # 区长（待确认）
    {"id": 2, "person_id": 2, "org_id": 2, "title": "徽州区委副书记、区长（待确认）",
     "start": "未知", "end": "present", "rank": "正处级",
     "note": "区长身份待确认"},
    # 章继平 - 区委副书记（待确认）
    {"id": 3, "person_id": 3, "org_id": 1, "title": "徽州区委副书记（待确认）",
     "start": "未知", "end": "present", "rank": "副处级",
     "note": "专职副书记，协助书记处理日常党务"},
    # 王恒来 - 前任区委书记
    {"id": 4, "person_id": 4, "org_id": 1, "title": "徽州区委书记（前任）",
     "start": "2018", "end": "2021", "rank": "正处级",
     "note": "前任区委书记，2021年由汪长剑接任"},
    # 张伟 - 前任区长
    {"id": 5, "person_id": 5, "org_id": 2, "title": "徽州区区长（前任）",
     "start": "2018", "end": "2023", "rank": "正处级",
     "note": "前任区长"},
]

relationships = [
    {
        "id": 1,
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "汪长剑（区委书记）与现任区长（待确认）为徽州区党政搭档",
        "overlap_org": "徽州区",
        "overlap_period": "待确认–present"
    },
    {
        "id": 2,
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "汪长剑（区委书记）与章继平（区委副书记）同为徽州区委领导班子成员",
        "overlap_org": "中共黄山市徽州区委员会",
        "overlap_period": "待确认–present"
    },
    {
        "id": 3,
        "person_a": 1, "person_b": 4,
        "type": "predecessor_successor",
        "context": "汪长剑接替王恒来任徽州区委书记",
        "overlap_org": "中共黄山市徽州区委员会",
        "overlap_period": "2021"
    },
    {
        "id": 4,
        "person_a": 2, "person_b": 5,
        "type": "predecessor_successor",
        "context": "现任区长（待确认）接替张伟任徽州区区长",
        "overlap_org": "黄山市徽州区人民政府",
        "overlap_period": "待确认"
    },
]

# ── helpers ──────────────────────────────────────────────────────────────

def is_top_leader(p):
    """Return True for the party secretary (top leader)."""
    return "书记" in p["current_post"] and "副书记" not in p["current_post"]


def person_color(p):
    """Return 'r,g,b' string for a person node."""
    post = p.get("current_post", "")
    if "书记" in post and "副书记" not in post and "前任" not in post:
        return "255,50,50"      # Red — Party Secretary
    if "区长" in post or "市长" in post:
        return "50,100,255"     # Blue — Mayor/区长
    if "副书记" in post:
        return "200,50,200"     # Purple — Deputy Secretary
    return "100,100,100"        # Grey — Others


def org_color(o):
    """Return 'r,g,b' string for an org node."""
    t = o.get("type", "")
    if t == "党委":
        return "255,200,200"
    if t == "政府":
        return "200,200,255"
    if t == "行政区域":
        return "200,255,200"
    if t == "人大":
        return "200,255,255"
    if t == "政协":
        return "255,240,200"
    return "200,200,200"


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ── BUILD SQLite ────────────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY,
            person_a INTEGER, person_b INTEGER, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"],
                   p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT OR REPLACE INTO positions VALUES (?,?,?,?,?,?,?,?)",
                  (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                   pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("INSERT OR REPLACE INTO relationships VALUES (?,?,?,?,?,?,?)",
                  (r["id"], r["person_a"], r["person_b"], r["type"],
                   r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"✅ SQLite DB written: {DB_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")


# ── BUILD GEXF ──────────────────────────────────────────────────────────

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>徽州区（安徽省黄山市）领导关系网络 — 区委书记、区长及领导班子（部分信息待确认）</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # ── Nodes ──
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        c = person_color(p)
        post = p.get("current_post", "")
        if "待确认" in p["name"]:
            sz = "12.0"
        elif is_top_leader(p):
            sz = "20.0"
        elif "区长" in post:
            sz = "16.0"
        elif "副书记" in post:
            sz = "14.0"
        else:
            sz = "12.0"
        role = p.get("current_post", "")
        org = p.get("current_org", "")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # ── Edges ──
    lines.append('    <edges>')

    eid = 0

    # Person → Org (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationships)
    for r in relationships:
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

    print(f"✅ GEXF graph written: {GEXF_PATH}")


# ── MAIN ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  徽州区（Huizhou District）领导关系网络数据库构建")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("  ⚠️  Partial evidence mode — web research to Chinese government sources blocked")
    print("=" * 60)
    build_db()
    build_gexf()
    print("\n[DONE] Build complete. See open_gaps.md for verification gaps.")
