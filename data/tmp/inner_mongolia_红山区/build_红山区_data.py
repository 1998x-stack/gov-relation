#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 红山区 (Hongshan District), 赤峰市, 内蒙古自治区.

Research date: 2026-07-25
Task ID: inner_mongolia_红山区
Level: 市辖区 (District)

NOTE: Web search was heavily degraded (Exa rate-limited, Baidu 403/captcha, Google blocked,
government site subpages timed out). Data is based on partial evidence from the district
government homepage (www.hongshanqu.gov.cn). Missing fields are marked accordingly.
"""

import sqlite3  # noqa: F401
import os
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TMP = os.path.join(BASE, "data/tmp/inner_mongolia_红山区")
DB_PATH = os.path.join(TMP, "红山区_network.db")
GEXF_PATH = os.path.join(TMP, "红山区_network.gexf")
AS_OF = "2026-07-25"

# ── PERSONS ──────────────────────────────────────────────────────────
# Confidence levels:
#   confirmed = official source (government homepage news / official page)
#   plausible = credible media with partial corroboration
#   unverified = lead without enough evidence

persons = [
    # ════ Current Top Leaders ════
    # 区委书记 — Name not found in captured homepage text
    # News article titles show "区委常委会（扩大）会议" but do not name the secretary
    # This is the biggest open gap.
    {
        "id": 1,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "红山区委书记",
        "current_org": "中共赤峰市红山区委员会",
        "source": "红山区政府网站首页: 区委常委会（扩大）会议 news item",
        "notes": "⚠️ 区委书记姓名未确认。须通过赤峰市委组织部任前公示或红山区政府网站领导之窗页面确认。",
    },
    # 赵兰广 — 区委副书记、区长 (confirmed from homepage news)
    {
        "id": 2,
        "name": "赵兰广",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "红山区委副书记、区长",
        "current_org": "赤峰市红山区人民政府",
        "source": "https://www.hongshanqu.gov.cn/ — news: '赵兰广主持召开红山区政府2026年第11次常务会议' (2026-07-22)",
        "notes": "区长身份通过政府常务会议新闻标题确认。",
    },

    # ════ 人大常委会主任 ════
    {
        "id": 3,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "红山区人大常委会主任",
        "current_org": "赤峰市红山区人民代表大会常务委员会",
        "source": "",
        "notes": "未找到相关信息",
    },
    # ════ 政协主席 ════
    {
        "id": 4,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "红山区政协主席",
        "current_org": "中国人民政治协商会议赤峰市红山区委员会",
        "source": "",
        "notes": "未找到相关信息",
    },
]

# ── ORGANIZATIONS ────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共赤峰市红山区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共赤峰市委员会",
        "location": "内蒙古自治区赤峰市红山区",
    },
    {
        "id": 2,
        "name": "赤峰市红山区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "赤峰市人民政府",
        "location": "内蒙古自治区赤峰市红山区",
    },
    {
        "id": 3,
        "name": "赤峰市红山区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "赤峰市人大常委会",
        "location": "内蒙古自治区赤峰市红山区",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议赤峰市红山区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "赤峰市政协",
        "location": "内蒙古自治区赤峰市红山区",
    },
]

# ── POSITIONS ────────────────────────────────────────────────────────

positions = [
    # 区委书记 (unknown)
    {"person_id": 1, "org_id": 1, "title": "红山区委书记",
     "start": "", "end": "present", "rank": "正处级",
     "note": "主持区委全面工作。姓名及履历待查。"},
    # 赵兰广 — 区委副书记、区长
    {"person_id": 2, "org_id": 1, "title": "红山区委副书记",
     "start": "", "end": "present", "rank": "副处级",
     "note": "区委副书记，协助区委书记工作。"},
    {"person_id": 2, "org_id": 2, "title": "红山区区长",
     "start": "", "end": "present", "rank": "正处级",
     "note": "主持区政府全面工作。2026年7月22日主持召开区政府2026年第11次常务会议。来源：红山区政府网站。"},
]

# ── RELATIONSHIPS ────────────────────────────────────────────────────

relationships = [
    # 区委书记 <-> 赵兰广 : 党政一把手
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "strength": "strong",
        "context": "区委书记（待确认）与赵兰广（区长）为红山区党政主要领导搭档",
        "overlap_org": "中共赤峰市红山区委员会",
        "overlap_period": "现任",
        "confidence": "plausible",
    },
]

# ── HELPERS ─────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    role = p["current_post"]
    if "区委书记" in role and "副书记" not in role:
        return "255,50,50"
    elif "区长" in role and "副书记" in role:
        return "50,100,255"
    elif "区长" in role:
        return "50,100,255"
    elif "人大" in role:
        return "200,255,255"
    elif "政协" in role:
        return "255,240,200"
    elif "纪委书记" in role or "纪检" in role:
        return "255,165,0"
    else:
        return "100,100,100"

def org_color(o):
    t = o["type"]
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }.get(t, "200,200,200")

def is_top_leader(p):
    role = p["current_post"]
    return "区委书记" in role or ("区长" in role and "副书记" in role)

def person_size(p):
    return "20.0" if is_top_leader(p) else "12.0"

# ── BUILD DB ─────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT,
            notes TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT, strength TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT, confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source, notes)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
             p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
             p.get("party_join", ""), p.get("work_start", ""),
             p["current_post"], p["current_org"], p.get("source", ""), p.get("notes", "")))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos.get("start", ""), pos.get("end", ""),
             pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, strength, context, overlap_org, overlap_period, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["strength"],
             r["context"], r["overlap_org"], r["overlap_period"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")

# ── BUILD GEXF ────────────────────────────────────────────────

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Sisyphus Gov-Relation Research Agent</creator>')
    lines.append('    <description>红山区领导班子工作关系网络 - 内蒙古赤峰市红山区</description>')
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
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("parent", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("start", ""))}~{esc(pos.get("end", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationships)
    for r in relationships:
        eid += 1
        w = "2.0" if r.get("strength") == "strong" else "1.5" if r.get("strength") == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{r.get("confidence", "unverified")}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {GEXF_PATH}")

# ── SUMMARY ──────────────────────────────────────────────────

def print_summary():
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"\n⚠️  NOTE: Web search was degraded. Key data gaps:")
    for p in persons:
        if p["name"] == "待查":
            print(f"  - {p['current_post']}: name not found")
    print(f"  - Full biographical data unavailable for all figures")

if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()
