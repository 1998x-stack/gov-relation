#!/usr/bin/env python3
"""Build 利辛县 (Lixin County, Bozhou, Anhui) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Task: anhui_利辛县 (安徽亳州市利辛县 - 县)

Confirmed officeholders (from 亳州市 city-level DB):
  - 县委书记: 张吉业 (confirmed at county level)
  - 县长: 万中强 (confirmed at county level)

Sources:
  - 亳州市_network.db (existing repository database)
  - build_亳州市_data.py (existing repository build script)

Confidence: Core leader identities (县委书记 张吉业, 县长 万中强) confirmed.
  Career timelines and biographical details pending direct web access — most fields
  marked as "待查". Gaps explicitly encoded with confidence markers.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "利辛县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "利辛县_network.gexf")
TODAY = datetime.now().strftime("%Y-%m-%d")

# ── helper functions ─────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return 'r,g,b' for a person node based on current role."""
    post = p["current_post"]
    if "县委书记" in post:
        return "255,50,50"
    if "县长" in post or "代县长" in post or "县长候选人" in post:
        return "50,100,255"
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"
    if "人大" in post:
        return "200,100,100"
    if "政协" in post:
        return "100,150,100"
    return "100,100,100"

def org_color(o):
    """Return 'r,g,b' for an organization node."""
    t = o["type"]
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    if "纪委" in t or "监委" in t:
        return "255,200,100"
    if "开发区" in t:
        return "200,255,200"
    if "乡镇" in t or "街道" in t:
        return "255,255,200"
    if "群团" in t:
        return "255,220,255"
    if "事业" in t:
        return "220,220,220"
    return "200,200,200"

def is_top_leader(p):
    return "县委书记" in p.get("current_post", "") or "县长" in p.get("current_post", "")

def pid(slug):
    """Generate person ID consistent with the lixin_ prefix convention."""
    return f"lixin_{slug}"

def oid(slug):
    """Generate org ID."""
    return f"org_lixin_{slug}"

# ── DATA ─────────────────────────────────────────────────────────────────

persons = [
    # ═══ Current Top Leaders ═══

    # 县委书记 张吉业
    {
        "id": pid("zhang_jiye"),
        "name": "张吉业",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "利辛县委书记",
        "current_org": "中共利辛县委员会",
        "source": "亳州市_network.db",
        "notes": "利辛县委书记。兼职亳州市委常委（推断，依据亳州市委常委配置惯例）。具体出生年月、籍贯、学历和完整履历待进一步核实。",
        "confidence": "confirmed"
    },
    # 县长 万中强
    {
        "id": pid("wan_zhongqiang"),
        "name": "万中强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "利辛县委副书记、县长",
        "current_org": "利辛县人民政府",
        "source": "亳州市_network.db",
        "notes": "利辛县县长。具体出生年月、籍贯、学历和完整履历待进一步核实。",
        "confidence": "confirmed"
    },
    # ═══ 其他已知领导班子成员（推断、部分确认）═══
    # Note: Full leadership roster for 利辛县 requires direct web/官方页面 access.
    # The following entries represent the expected standard composition of a county
    # leadership team in Anhui. Names marked "待核实" are unverified placeholder entries.
    # ---
    # 县人大常委会主任
    {
        "id": pid("npc_chair"),
        "name": "待核实（人大常委会主任）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "利辛县人大常委会主任",
        "current_org": "利辛县人大常委会",
        "source": "待核实",
        "notes": "利辛县人大常委会主任。姓名待确认。",
        "confidence": "unverified"
    },
    # 县政协主席
    {
        "id": pid("cppcc_chair"),
        "name": "待核实（政协主席）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "利辛县政协主席",
        "current_org": "中国人民政治协商会议利辛县委员会",
        "source": "待核实",
        "notes": "利辛县政协主席。姓名待确认。",
        "confidence": "unverified"
    },
]

organizations = [
    {
        "id": oid("cpc"),
        "name": "中共利辛县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共亳州市委员会",
        "location": "安徽省亳州市利辛县"
    },
    {
        "id": oid("gov"),
        "name": "利辛县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "亳州市人民政府",
        "location": "安徽省亳州市利辛县"
    },
    {
        "id": oid("npc"),
        "name": "利辛县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "亳州市人大常委会",
        "location": "安徽省亳州市利辛县"
    },
    {
        "id": oid("cppcc"),
        "name": "中国人民政治协商会议利辛县委员会",
        "type": "政协",
        "level": "县",
        "parent": "亳州市政协",
        "location": "安徽省亳州市利辛县"
    },
    {
        "id": oid("discipline"),
        "name": "中共利辛县纪律检查委员会",
        "type": "纪委",
        "level": "县",
        "parent": "中共亳州市纪律检查委员会",
        "location": "安徽省亳州市利辛县"
    },
    {
        "id": oid("gov_general"),
        "name": "利辛县人民政府办公室",
        "type": "政府",
        "level": "县",
        "parent": "利辛县人民政府",
        "location": "安徽省亳州市利辛县"
    },
]

positions = [
    # 张吉业 → 利辛县委
    {"person_id": pid("zhang_jiye"), "org_id": oid("cpc"),
     "title": "利辛县委书记", "start": "", "end": "",
     "rank": "1", "note": "利辛县委书记"},
    # 万中强 → 利辛县政府
    {"person_id": pid("wan_zhongqiang"), "org_id": oid("gov"),
     "title": "利辛县委副书记、县长", "start": "", "end": "",
     "rank": "1", "note": "利辛县县长"},
    # 县人大常委会主任（待核实）
    {"person_id": pid("npc_chair"), "org_id": oid("npc"),
     "title": "利辛县人大常委会主任", "start": "", "end": "",
     "rank": "1", "note": "待核实"},
    # 县政协主席（待核实）
    {"person_id": pid("cppcc_chair"), "org_id": oid("cppcc"),
     "title": "利辛县政协主席", "start": "", "end": "",
     "rank": "1", "note": "待核实"},
]

relationships = [
    # 张吉业 ↔ 万中强：党政正职关系
    {"person_a": pid("zhang_jiye"), "person_b": pid("wan_zhongqiang"),
     "type": "colleague", "strength": "strong",
     "context": "县委书记与县长搭档（党政正职关系）",
     "overlap_org": oid("cpc"), "overlap_period": "",
     "confidence": "confirmed"},
    # 张吉业 → 市人大常委会（上级关系，通过亳州市委）
    {"person_a": pid("zhang_jiye"), "person_b": pid("npc_chair"),
     "type": "colleague", "strength": "medium",
     "context": "县委书记与人大常委会主任（县四套班子关系）",
     "overlap_org": oid("cpc"), "overlap_period": "",
     "confidence": "unverified"},
    # 万中强 → 县政协主席
    {"person_a": pid("wan_zhongqiang"), "person_b": pid("cppcc_chair"),
     "type": "colleague", "strength": "medium",
     "context": "县长与政协主席（县四套班子关系）",
     "overlap_org": oid("gov"), "overlap_period": "",
     "confidence": "unverified"},
]

# ═════════════════════════════════════════════════════════════════════════
# BUILD FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════

def build_db():
    """Create SQLite database."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = ON;")

    c.execute("""
        CREATE TABLE persons (
            id TEXT PRIMARY KEY,
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
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
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
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT,
            strength TEXT,
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
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace,
                                 native_place, education, party_join, work_start,
                                 current_post, current_org, source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
            p.get("birth", ""), p.get("birthplace", ""), p.get("native_place", ""),
            p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
            p.get("current_post", ""), p.get("current_org", ""),
            p.get("source", ""), p.get("notes", ""), p.get("confidence", ""),
        ))

    for o in organizations:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            pos["person_id"], pos["org_id"], pos["title"],
            pos.get("start", ""), pos.get("end", ""),
            pos.get("rank", ""), pos.get("note", ""),
        ))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, strength, context,
                                       overlap_org, overlap_period, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            r["person_a"], r["person_b"], r["type"], r.get("strength", ""),
            r.get("context", ""), r.get("overlap_org", ""),
            r.get("overlap_period", ""), r.get("confidence", ""),
        ))

    conn.commit()
    conn.close()
    print(f"[DB] Created: {DB_PATH}")


def build_gexf():
    """Create GEXF graph file using string formatting (avoids namespace issues)."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>利辛县 (Lixin County, Bozhou, Anhui) — Leadership Network Graph</description>')
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
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="{esc(p["id"])}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="{esc(o["id"])}" label="{esc(o["name"])}">')
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

    # Person → Organization edges (worked_at)
    for pos in positions:
        lines.append(f'      <edge id="e{eid}" source="{esc(pos["person_id"])}" target="{esc(pos["org_id"])}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person ↔ Person edges (relationship)
    for r in relationships:
        weight = "2.0" if r.get("strength") == "strong" else "1.5" if r.get("strength") == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{esc(r["person_a"])}" target="{esc(r["person_b"])}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("confidence", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[GEXF] Created: {GEXF_PATH}")
    print(f"[GEXF] Nodes: {len(persons)} persons + {len(organizations)} orgs")
    print(f"[GEXF] Edges: {len(positions)} worked_at + {len(relationships)} relationships")


def main():
    build_db()
    build_gexf()

    print(f"\n{'=' * 50}")
    print(f"利辛县 Leadership Network — Build Complete")
    print(f"{'=' * 50}")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print(f"\nOutput files:")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
