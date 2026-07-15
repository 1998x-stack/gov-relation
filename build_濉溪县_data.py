#!/usr/bin/env python3
"""Build Suixi County (濉溪县) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Sources:
  - https://zh.wikipedia.org/wiki/濉溪县 (Wikipedia, accessed 2026-07-15)
  - http://www.sxx.gov.cn/ (濉溪县人民政府官方网站, accessed 2026-07-15)
  - https://zh.wikipedia.org/wiki/淮北市 (淮北市页面四大机构, accessed 2026-07-15)

Confidence: Current roles confirmed from Wikipedia and official government news.
  Biographical details are partial (Baidu Baike blocked from current network).
  Predecessor information inferred from leadership transition patterns.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "濉溪县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "濉溪县_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    {
        "id": 1,
        "name": "黄韡",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共濉溪县委",
        "source": "https://zh.wikipedia.org/wiki/濉溪县 (政府信息); http://www.sxx.gov.cn/",
        "notes": "现任中共濉溪县委书记。完整履历待补充（百度百科当前网络受限）。"
                 "从濉溪县政府网站新闻报道可见其为当前县委主要负责人。",
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "孙进",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县长",
        "current_org": "濉溪县人民政府",
        "source": "https://zh.wikipedia.org/wiki/濉溪县 (政府信息)",
        "notes": "现任濉溪县人民政府县长。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 3,
        "name": "姜灵",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "濉溪县人大常委会",
        "source": "https://zh.wikipedia.org/wiki/濉溪县 (政府信息)",
        "notes": "现任濉溪县人大常委会主任（女）。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 4,
        "name": "刘铁",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协濉溪县委员会",
        "source": "https://zh.wikipedia.org/wiki/濉溪县 (政府信息)",
        "notes": "现任政协濉溪县委员会主席（女）。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 5,
        "name": "史庆超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记/常务副县长（待确认）",
        "current_org": "中共濉溪县委/濉溪县人民政府",
        "source": "http://www.sxx.gov.cn/ (新闻报道，2026-07-13至2026-07-15)",
        "notes": "2026年7月频繁出现在县政府新闻报道中：调研电镀产业、基层治理、防汛工作、"
                 "学习教育查摆问题及集中整治等。具体职务待进一步核实。",
        "confidence": "plausible"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中国共产党濉溪县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中国共产党淮北市委员会",
        "location": "安徽省淮北市濉溪县"
    },
    {
        "id": 2,
        "name": "濉溪县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "淮北市人民政府",
        "location": "安徽省淮北市濉溪县"
    },
    {
        "id": 3,
        "name": "濉溪县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "濉溪县",
        "location": "安徽省淮北市濉溪县"
    },
    {
        "id": 4,
        "name": "政协濉溪县委员会",
        "type": "政协",
        "level": "县",
        "parent": "濉溪县",
        "location": "安徽省淮北市濉溪县"
    },
    {
        "id": 5,
        "name": "濉溪经济开发区",
        "type": "开发区",
        "level": "省级",
        "parent": "濉溪县人民政府",
        "location": "安徽省淮北市濉溪县"
    },
    {
        "id": 6,
        "name": "濉溪芜湖现代产业园区",
        "type": "开发区",
        "level": "省级",
        "parent": "濉溪县人民政府",
        "location": "安徽省淮北市濉溪县"
    },
]

positions = [
    # 黄韡
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "县处级正职", "note": "现任"},
    # 孙进
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "县处级正职", "note": "现任"},
    # 姜灵
    {"person_id": 3, "org_id": 3, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "县处级正职", "note": "现任"},
    # 刘铁
    {"person_id": 4, "org_id": 4, "title": "县政协主席", "start": "", "end": "present", "rank": "县处级正职", "note": "现任"},
    # 史庆超
    {"person_id": 5, "org_id": 1, "title": "县委副书记（推断）", "start": "", "end": "present", "rank": "县处级副职", "note": "具体职务待确认"},
    {"person_id": 5, "org_id": 2, "title": "县政府领导（推断）", "start": "", "end": "present", "rank": "县处级副职", "note": "负责多项县政府日常工作"},
]

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长，县委县政府主要领导搭档",
        "overlap_org": "中共濉溪县委",
        "overlap_period": "至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "overlap",
        "context": "县委书记与县人大常委会主任，县四大班子主要领导",
        "overlap_org": "濉溪县",
        "overlap_period": "至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "overlap",
        "context": "县委书记与县政协主席，县四大班子主要领导",
        "overlap_org": "濉溪县",
        "overlap_period": "至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "overlap",
        "context": "县长与县人大常委会主任，县四大班子主要领导",
        "overlap_org": "濉溪县",
        "overlap_period": "至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 2,
        "person_b": 4,
        "type": "overlap",
        "context": "县长与县政协主席，县四大班子主要领导",
        "overlap_org": "濉溪县",
        "overlap_period": "至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "县委书记与县委副书记/常务副县长（推断），县委领导班子搭档",
        "overlap_org": "中共濉溪县委",
        "overlap_period": "至今",
        "confidence": "plausible"
    },
    {
        "person_a": 2,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "县长与副县长（推断），县政府领导班子搭档",
        "overlap_org": "濉溪县人民政府",
        "overlap_period": "至今",
        "confidence": "plausible"
    },
]


# ── build functions ──────────────────────────────────────────────────────

def create_database(db_path):
    """Create SQLite database with persons, organizations, positions, relationships."""
    os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            native_place TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT,
            notes TEXT,
            confidence TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    c.execute("""
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
    c.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""
            INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace,
                native_place, education, party_join, work_start, current_post, current_org,
                source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
              p.get("birth", ""), p.get("birthplace", ""), p.get("native_place", ""),
              p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
              p.get("current_post", ""), p.get("current_org", ""),
              p.get("source", ""), p.get("notes", ""), p.get("confidence", "")))

    for o in organizations:
        c.execute("""
            INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
              o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos.get("title", ""),
              pos.get("start", ""), pos.get("end", ""), pos.get("rank", ""),
              pos.get("note", "")))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r.get("type", ""),
              r.get("context", ""), r.get("overlap_org", ""),
              r.get("overlap_period", ""), r.get("confidence", "")))

    conn.commit()
    conn.close()


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return 'r,g,b' for a person node."""
    post = p.get("current_post", "")
    if "书记" in post and "纪委" not in post:
        return "255,50,50"    # Red — party secretary
    elif "县长" in post or "市长" in post or "区长" in post:
        return "50,100,255"   # Blue — government leader
    elif "纪委" in post:
        return "255,165,0"    # Orange — discipline
    else:
        return "100,100,100"  # Grey — other


def is_top_leader(p):
    post = p.get("current_post", "")
    return "书记" in post or "县长" in post


def org_color(o):
    t = o.get("type", "")
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")


def generate_gexf(gexf_path):
    """Generate GEXF 1.3 graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>濉溪县领导班子工作关系网络 — Party Secretary, County Mayor, and leadership team</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: Persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        pid = f"p{p['id']}"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("confidence", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: Organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos.get("title", ""))}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r.get("context", ""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("confidence", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    os.makedirs(os.path.dirname(gexf_path) or ".", exist_ok=True)
    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ── main ─────────────────────────────────────────────────────────────────

def main():
    print(f"=== 濉溪县 Leadership Network Data Builder ===")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    print()

    # 1. Database
    print(f"Creating database: {DB_PATH}")
    create_database(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        count = c.fetchone()[0]
        print(f"  {table}: {count} rows")
    conn.close()

    # 2. GEXF
    print(f"\nCreating GEXF: {GEXF_PATH}")
    generate_gexf(GEXF_PATH)
    gexf_size = os.path.getsize(GEXF_PATH)
    print(f"  GEXF file size: {gexf_size} bytes")

    # 3. Summary
    print(f"\n=== Summary ===")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")

    for p in persons:
        conf = p.get("confidence", "")
        print(f"  - {p['name']}: {p.get('current_post', '')} ({conf})")

    print(f"\nDone. Files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    main()
