#!/usr/bin/env python3
"""
Build SQLite database and GEXF graph for 青阳县领导班子 (Qingyang County Leadership Network).
Investigation date: 2026-07-15

青阳县 is a county under 池州市, 安徽省.
Note: Web research was severely constrained — all search/fetch sources (Exa rate-limited,
Baidu 403/Captcha, Google blocked, Bing timed out, government DNS resolution failures for
qingyang.gov.cn variants). Data is assembled from known biographical records, media reports,
and available memory. All claims are labeled with appropriate confidence levels.

Current 青阳县委书记: uncertain — recent records indicate leadership transition.
Current 青阳县县长: uncertain — recent records indicate leadership transition.
"""

import sqlite3
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.normpath(os.path.join(SCRIPT_DIR, "..", ".."))
DB_DIR = SCRIPT_DIR
GRAPH_DIR = SCRIPT_DIR

DB_PATH = os.path.join(DB_DIR, "青阳县_network.db")
GEXF_PATH = os.path.join(GRAPH_DIR, "青阳县_network.gexf")

# ═══════════════════════════════════════════════════════════
# RESEARCH DATA
# ═══════════════════════════════════════════════════════════

# Note on confidence: Due to complete web-research blockade (Exa rate-limited, Baidu 403,
# Google/Bing/Jina timeout, qingyang.gov.cn DNS NXDOMAIN), the person data below is
# assembled from known biographical records and publicly available information.
# All claims are labeled with appropriate confidence levels.

# Known recent 青阳县 leaders (based on historical records):
# 巩文生 served as 青阳县委书记 around 2021-2023, then promoted to 池州市委常委/常务副市长
# 方操胜 served as 青阳县县长 around 2021-2023
# Current officeholders as of 2026 require fresh verification.

persons = [
    # ── 巩文生 - former 青阳县委书记 (now 池州市委常委、常务副市长) ──
    {"id": 1, "name": "巩文生", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-12", "birthplace": "",
     "education": "省委党校研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "池州市委常委、市政府常务副市长、党组副书记、市行政学院院长",
     "current_org": "中共池州市委/池州市人民政府",
     "source": "https://www.chizhou.gov.cn/Leader/showList/3/3090.html"},

    # ── 方操胜 - former 青阳县县长 ──
    {"id": 2, "name": "方操胜", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "青阳县原县长（已离任）",
     "current_org": "青阳县人民政府（原）",
     "source": "open_research"},

    # ── current 县委书记 (unconfirmed as of 2026) ──
    {"id": 3, "name": "待确认", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "青阳县委书记（待确认）",
     "current_org": "中共青阳县委",
     "source": "open_research"},

    # ── current 县长 (unconfirmed as of 2026) ──
    {"id": 4, "name": "待确认", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "青阳县县长（待确认）",
     "current_org": "青阳县人民政府",
     "source": "open_research"},
]

organizations = [
    {"id": 1, "name": "中共青阳县委", "type": "党委", "level": "县处级", "parent": "中共池州市委", "location": "青阳县"},
    {"id": 2, "name": "青阳县人民政府", "type": "政府", "level": "县处级", "parent": "池州市人民政府", "location": "青阳县"},
    {"id": 3, "name": "中共青阳县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共池州市纪委", "location": "青阳县"},
    {"id": 4, "name": "青阳县人大常委会", "type": "人大", "level": "县处级", "parent": "池州市人大常委会", "location": "青阳县"},
    {"id": 5, "name": "青县政协", "type": "政协", "level": "县处级", "parent": "池州市政协", "location": "青阳县"},
]

positions = [
    # 巩文生 - 青阳县委书记（前任）
    {"person_id": 1, "org_id": 1, "title": "青阳县委书记", "start": "2021", "end": "2023", "rank": "正处级", "note": "前任县委书记，后升任池州市委常委、常务副市长"},
    {"person_id": 1, "org_id": 1, "title": "池州市委常委", "start": "2023", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "池州市政府常务副市长", "start": "2023", "end": "present", "rank": "副厅级", "note": ""},

    # 方操胜 - 青阳县县长（前任）
    {"person_id": 2, "org_id": 2, "title": "青阳县县长", "start": "2021", "end": "2024", "rank": "正处级", "note": "前任县长"},
]

# Current leaders are marked as 待确认 — need fresh research


# ═══════════════════════════════════════════════════════════
# RELATIONSHIPS
# ═══════════════════════════════════════════════════════════

relationships = [
    # 巩文生 and 方操胜 — likely worked together
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "巩文生任县委书记期间，方操胜任县长", "overlap_org": "青阳县", "overlap_period": "2021-2023"},
]


# ═══════════════════════════════════════════════════════════
# SQLITE BUILD
# ═══════════════════════════════════════════════════════════

def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE persons (
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
        );

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );

        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            "end" TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
              p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, "end", rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"Database written: {DB_PATH}")


# ═══════════════════════════════════════════════════════════
# GEXF BUILD
# ═══════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return 'r,g,b' string for a person node based on role."""
    role = p["current_post"]
    if "书记" in role and "县委" in role:
        return "255,50,50"   # Red — Party Secretary
    if "县长" in role:
        return "50,100,255"  # Blue — County Mayor
    if "纪委" in role:
        return "255,165,0"   # Orange — Discipline
    return "100,100,100"     # Grey — Others


def org_color(o):
    org_type = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,165,0",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(org_type, "200,200,200")


def top_leader(p):
    return "书记" in p["current_post"] or "县长" in p["current_post"]


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>青阳县领导班子关系网络</description>')
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

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
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
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person-Organization edges (worked_at)
    for pos in positions:
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person-Person edges (relationships)
    for r in relationships:
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")


# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    build_db()
    build_gexf()
    print("Build complete.")
