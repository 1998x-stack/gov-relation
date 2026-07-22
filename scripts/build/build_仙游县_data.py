#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 仙游县 (福建省莆田市) leadership network.

Level: 县
Province: 福建省
Parent city: 莆田市
Targets: 县委书记 & 县长

Research Notes (as of 2026-07-16):
- Current 县委书记: 吴海端 (confirmed from Chinese Wikipedia 仙游县 page)
- Current 县长: 姓名待确认 — government website xianyou.gov.cn blocked;
  Baidu Baike and other Chinese sources also inaccessible due to captcha/WAF blocks.
- 吴海端's full biographical details (birth year, birthplace, education, career timeline)
  could not be retrieved due to access restrictions on Chinese sources (Baidu Baike,
  xianyou.gov.cn, Google cache). Baidu Baike page for 吴海端 does not exist.
- Wikipedia (zh) infobox only confirms name and role — no biography data.
- 前任县委书记 and 前任县长 could not be determined from accessible sources.

Known sources:
- https://zh.wikipedia.org/wiki/仙游县 — confirms 县委书记 吴海端
- https://www.xianyou.gov.cn — official site, inaccessible from build environment
- Baidu Baike — blocked by captcha

Key gaps:
- 县长 name unknown
- 吴海端 full career timeline unknown
- 县委常委 roster unknown
- 前任/ successor paths unknown
- Birth dates, education, native place for all figures unknown

All person data marked with confidence accordingly.
"""

import sqlite3
import os
import sys
from datetime import datetime

# ── Paths ──
BASE = os.path.dirname(os.path.abspath(__file__))
if "data/tmp" in BASE:
    DB_PATH = os.path.join(BASE, "仙游县_network.db")
    GEXF_PATH = os.path.join(BASE, "仙游县_network.gexf")
else:
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(PROJECT_ROOT, "data/database/仙游县_network.db")
    GEXF_PATH = os.path.join(PROJECT_ROOT, "data/graph/仙游县_network.gexf")

KNOWN_DATE = "2026-07-16"

# ══════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════

# ── Persons ──

persons = [
    # ══ 县委书记 (Party Secretary) ══
    # 吴海端 — confirmed from Wikipedia infobox
    {
        "id": 1,
        "name": "吴海端",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共仙游县委书记",
        "current_org": "中共仙游县委员会",
        "source": "https://zh.wikipedia.org/wiki/仙游县"
    },

    # ══ 县长 (County Mayor) ══
    # ⚠️ NAME UNKNOWN — all Chinese government and encyclopedia sources blocked
    {
        "id": 2,
        "name": "（待确认）",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "仙游县人民政府县长",
        "current_org": "仙游县人民政府",
        "source": "待查 — xianyou.gov.cn blocked"
    },

    # ══ 县委副书记（大概率由县长兼任）(Deputy Secretary, likely concurrent by mayor) ══
    {
        "id": 3,
        "name": "（待确认）",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "仙游县委副书记",
        "current_org": "中共仙游县委员会",
        "source": "待查"
    },

    # ══ 常务副县长 (Executive Deputy Mayor) ══
    {
        "id": 4,
        "name": "（待确认）",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "仙游县委常委、常务副县长",
        "current_org": "仙游县人民政府",
        "source": "待查"
    },

    # ══ 纪委书记 (Discipline Secretary) ══
    {
        "id": 5,
        "name": "（待确认）",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "仙游县委常委、县纪委书记",
        "current_org": "中共仙游县纪律检查委员会",
        "source": "待查"
    },

    # ══ 组织部长 (Organization Department Head) ══
    {
        "id": 6,
        "name": "（待确认）",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "仙游县委常委、组织部部长",
        "current_org": "中共仙游县委组织部",
        "source": "待查"
    },

    # ══ 政法委书记 (Political-Legal Secretary) ══
    {
        "id": 7,
        "name": "（待确认）",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "仙游县委常委、政法委书记",
        "current_org": "中共仙游县委政法委员会",
        "source": "待查"
    },

    # ══ 宣传部长 (Propaganda Department Head) ══
    {
        "id": 8,
        "name": "（待确认）",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "仙游县委常委、宣传部部长",
        "current_org": "中共仙游县委宣传部",
        "source": "待查"
    },

    # ══ 县委办主任或统战部长 (United Front Work Dept Head or Party Office Director) ══
    {
        "id": 9,
        "name": "（待确认）",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "仙游县委常委",
        "current_org": "中共仙游县委员会",
        "source": "待查"
    },

    # ══ 县人武部长 (County Armed Forces Director) — typically a常委 ══
    {
        "id": 10,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "仙游县委常委、县人武部部长",
        "current_org": "仙游县人民武装部",
        "source": "待查"
    },
]

# ── Organizations ──

organizations = [
    {"id": 1, "name": "中共仙游县委员会", "type": "党委", "level": "县", "parent": "中共莆田市委员会", "location": "福建省莆田市仙游县"},
    {"id": 2, "name": "仙游县人民政府", "type": "政府", "level": "县", "parent": "莆田市人民政府", "location": "福建省莆田市仙游县"},
    {"id": 3, "name": "中共仙游县纪律检查委员会", "type": "纪委", "level": "县", "parent": "中共莆田市纪律检查委员会", "location": "福建省莆田市仙游县"},
    {"id": 4, "name": "仙游县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "莆田市人民代表大会常务委员会", "location": "福建省莆田市仙游县"},
    {"id": 5, "name": "中国人民政治协商会议仙游县委员会", "type": "政协", "level": "县", "parent": "政协莆田市委员会", "location": "福建省莆田市仙游县"},
    {"id": 6, "name": "中共仙游县委组织部", "type": "党委", "level": "县", "parent": "中共仙游县委员会", "location": "福建省莆田市仙游县"},
    {"id": 7, "name": "中共仙游县委宣传部", "type": "党委", "level": "县", "parent": "中共仙游县委员会", "location": "福建省莆田市仙游县"},
    {"id": 8, "name": "中共仙游县委政法委员会", "type": "党委", "level": "县", "parent": "中共仙游县委员会", "location": "福建省莆田市仙游县"},
    {"id": 9, "name": "仙游县人民武装部", "type": "事业单位", "level": "县", "parent": "莆田军分区", "location": "福建省莆田市仙游县"},
    {"id": 10, "name": "中共仙游县委统一战线工作部", "type": "党委", "level": "县", "parent": "中共仙游县委员会", "location": "福建省莆田市仙游县"},
]

# ── Positions ──

positions = [
    # id, person_id, org_id, title, start, end, rank, note
    # 吴海端 — current county party secretary
    (1, 1, 1, "中共仙游县委书记", KNOWN_DATE, "present", "正处级", "confirmed from Wikipedia; appointment date unknown"),

    # ⚠️ All other positions — unknown officeholders
]

# ── Relationships ──

relationships = [
    # (person_a_id, person_b_id, type, context, overlap_org_id, overlap_period, confidence)
]

# ══════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════

def create_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT, birthplace TEXT,
            education TEXT, party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org INTEGER, overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id),
            FOREIGN KEY (overlap_org) REFERENCES organizations(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT OR REPLACE INTO positions
            (id, person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?,?)""", pos)

    for rel in relationships:
        c.execute("""INSERT OR REPLACE INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)""", rel)

    conn.commit()
    conn.close()

    counts = {}
    conn = sqlite3.connect(DB_PATH)
    for table in ["persons", "organizations", "positions", "relationships"]:
        counts[table] = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    conn.close()
    return counts


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    role = p["current_post"]
    if "书记" in role and "纪委" not in role:
        return "255,50,50"      # Red — Party Secretary
    if "县长" in role or "区长" in role or "市长" in role:
        return "50,100,255"     # Blue — Government head
    if "纪委" in role:
        return "255,165,0"      # Orange — Discipline
    return "100,100,100"        # Grey — Others


def is_top_leader(p):
    return p["id"] in (1, 2)


def create_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{KNOWN_DATE}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>仙游县（福建省莆田市）领导班子工作关系网络 — 2026年7月</description>')
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
    lines.append('      <attribute id="1" title="title" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        type_colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "纪委": "255,200,200",
            "人大": "200,255,255",
            "政协": "255,240,200",
            "事业单位": "220,220,220",
        }
        c = type_colors.get(o["type"], "200,200,200")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
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
        pid, oid, title = pos[1], pos[2], pos[3]
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person → Person (relationships)
    for rel in relationships:
        eid += 1
        a, b, rtype, context = rel[0], rel[1], rel[2], rel[3]
        lines.append(f'      <edge id="e{eid}" source="p{a}" target="p{b}" label="{esc(rtype)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    print(f"仙游县 Leadership Network Builder")
    print(f"Date: {KNOWN_DATE}")
    print()

    counts = create_db()
    print(f"✅ SQLite database: {DB_PATH}")
    print(f"   Persons: {counts['persons']}")
    print(f"   Organizations: {counts['organizations']}")
    print(f"   Positions: {counts['positions']}")
    print(f"   Relationships: {counts['relationships']}")

    create_gexf()
    print(f"✅ GEXF graph: {GEXF_PATH}")

    # Summary of known vs unknown
    known = sum(1 for p in persons if p["name"] != "（待确认）")
    unknown = sum(1 for p in persons if p["name"] == "（待确认）")
    print(f"\n📊 Known officeholders: {known}/{len(persons)}")
    print(f"📊 Unknown officeholders: {unknown}/{len(persons)}")
    print(f"\n⚠️  Research limitations:")
    print(f"   - xianyou.gov.cn blocked (WAF)")
    print(f"   - Baidu Baike blocked (captcha)")
    print(f"   - Exa web search rate-limited")
    print(f"   - 县长 name, full biographies, and leadership roster need field research")


if __name__ == "__main__":
    main()
