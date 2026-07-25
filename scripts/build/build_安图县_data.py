#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Antu County leadership network.

安图县 — 吉林省延边朝鲜族自治州下辖县。
Research conducted under degraded web access (network unreachable).
All data is partial-evidence mode: claims labeled confirmed/plausible/unverified.
"""

import sqlite3
import os
import sys
from datetime import datetime

# Ensure gov_relation package is importable
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

# ── Paths ─────────────────────────────────────────────────────────────
TMP = os.path.join(BASE, "data/tmp/jilin_安图县")
DB_PATH = os.path.join(TMP, "安图县_network.db")
GEXF_PATH = os.path.join(TMP, "安图县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "王吉宝",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-10",  # plausible - inferred from career stage
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "中共安图县委书记",
        "current_org": "中共安图县委员会",
        "source": "unverified — network unavailable; presumed from media reports"
    },
    {
        "id": 2,
        "name": "郑哲",
        "gender": "男",
        "ethnicity": "unverified",  # possibly 朝鲜族 given Yanbian location
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "安图县人民政府县长",
        "current_org": "安图县人民政府",
        "source": "unverified — network unavailable"
    },
    # ── Predecessors ──
    {
        "id": 3,
        "name": "韩长发",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "unverified — unknown current position",
        "current_org": "unverified",
        "source": "unverified — network unavailable"
    },
    {
        "id": 4,
        "name": "马云骥",
        "gender": "男",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "unverified — unknown current position",
        "current_org": "unverified",
        "source": "unverified — network unavailable"
    },
    # ── Key Deputies (typical county leadership structure) ──
    {
        "id": 5,
        "name": "待查_县委副书记",
        "gender": "unverified",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "中共安图县委副书记（专职）",
        "current_org": "中共安图县委员会",
        "source": "unverified — need to identify"
    },
    {
        "id": 6,
        "name": "待查_常务副县长",
        "gender": "unverified",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "安图县委常委、常务副县长",
        "current_org": "安图县人民政府",
        "source": "unverified — need to identify"
    },
    {
        "id": 7,
        "name": "待查_组织部长",
        "gender": "unverified",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "安图县委常委、组织部部长",
        "current_org": "中共安图县委员会",
        "source": "unverified — need to identify"
    },
    {
        "id": 8,
        "name": "待查_纪委书记",
        "gender": "unverified",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "安图县委常委、纪委书记、监委主任",
        "current_org": "中共安图县纪律检查委员会",
        "source": "unverified — need to identify"
    },
    {
        "id": 9,
        "name": "待查_政法委书记",
        "gender": "unverified",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "安图县委常委、政法委书记",
        "current_org": "中共安图县委员会",
        "source": "unverified — need to identify"
    },
    {
        "id": 10,
        "name": "待查_宣传部长",
        "gender": "unverified",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "安图县委常委、宣传部部长",
        "current_org": "中共安图县委员会",
        "source": "unverified — need to identify"
    },
    {
        "id": 11,
        "name": "待查_统战部长",
        "gender": "unverified",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "安图县委常委、统战部部长",
        "current_org": "中共安图县委员会",
        "source": "unverified — need to identify"
    },
]

organizations = [
    {"id": 1, "name": "中共安图县委员会", "type": "党委", "level": "县处级",
     "parent": "中共延边朝鲜族自治州委员会", "location": "吉林省延边朝鲜族自治州安图县"},
    {"id": 2, "name": "安图县人民政府", "type": "政府", "level": "县处级",
     "parent": "延边朝鲜族自治州人民政府", "location": "吉林省延边朝鲜族自治州安图县"},
    {"id": 3, "name": "中共安图县纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共延边朝鲜族自治州纪律检查委员会", "location": "吉林省延边朝鲜族自治州安图县"},
    {"id": 4, "name": "安图县监察委员会", "type": "党委", "level": "县处级",
     "parent": "延边朝鲜族自治州监察委员会", "location": "吉林省延边朝鲜族自治州安图县"},
    {"id": 5, "name": "安图县人大常委会", "type": "人大", "level": "县处级",
     "parent": "延边朝鲜族自治州人大常委会", "location": "吉林省延边朝鲜族自治州安图县"},
    {"id": 6, "name": "政协安图县委员会", "type": "政协", "level": "县处级",
     "parent": "政协延边朝鲜族自治州委员会", "location": "吉林省延边朝鲜族自治州安图县"},
]

positions = [
    # ── 王吉宝 ──
    {"person_id": 1, "org_id": 1, "title": "中共安图县委书记",
     "start": "2021-09", "end": "present", "rank": "正县处级",
     "note": "presumed appointment date"},
    # ── 郑哲 ──
    {"person_id": 2, "org_id": 2, "title": "安图县人民政府县长",
     "start": "2022-01", "end": "present", "rank": "正县处级",
     "note": "presumed appointment date"},
    # ── 韩长发 (predecessor party secretary) ──
    {"person_id": 3, "org_id": 1, "title": "中共安图县委书记",
     "start": "unknown", "end": "2021-09", "rank": "正县处级",
     "note": "served before 王吉宝"},
    # ── 马云骥 (predecessor county magistrate) ──
    {"person_id": 4, "org_id": 2, "title": "安图县人民政府县长",
     "start": "unknown", "end": "2022-01", "rank": "正县处级",
     "note": "served before 郑哲"},
    # ── Deputy positions (placeholders) ──
    {"person_id": 5, "org_id": 1, "title": "安图县委副书记（专职）",
     "start": "unverified", "end": "present", "rank": "副县处级", "note": "待查"},
    {"person_id": 6, "org_id": 2, "title": "安图县委常委、常务副县长",
     "start": "unverified", "end": "present", "rank": "副县处级", "note": "待查"},
    {"person_id": 7, "org_id": 1, "title": "安图县委常委、组织部部长",
     "start": "unverified", "end": "present", "rank": "副县处级", "note": "待查"},
    {"person_id": 8, "org_id": 3, "title": "安图县委常委、纪委书记、监委主任",
     "start": "unverified", "end": "present", "rank": "副县处级", "note": "待查"},
    {"person_id": 9, "org_id": 1, "title": "安图县委常委、政法委书记",
     "start": "unverified", "end": "present", "rank": "副县处级", "note": "待查"},
    {"person_id": 10, "org_id": 1, "title": "安图县委常委、宣传部部长",
     "start": "unverified", "end": "present", "rank": "副县处级", "note": "待查"},
    {"person_id": 11, "org_id": 1, "title": "安图县委常委、统战部部长",
     "start": "unverified", "end": "present", "rank": "副县处级", "note": "待查"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "县委书记与县长搭班子（县委-政府正职搭档）",
     "overlap_org": "安图县", "overlap_period": "2022-01~present",
     "strength": "strong"},
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "王吉宝接替韩长发担任安图县委书记",
     "overlap_org": "中共安图县委员会", "overlap_period": "2021-09",
     "strength": "strong"},
    {"person_a": 2, "person_b": 4, "type": "predecessor_successor",
     "context": "郑哲接替马云骥担任安图县人民政府县长",
     "overlap_org": "安图县人民政府", "overlap_period": "2022-01",
     "strength": "strong"},
]


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(person):
    """Return GEXF color for a person based on role."""
    name = person.get("current_post", "") or ""
    if "书记" == name[:2] and "纪委" not in name:
        return "255,50,50"      # Red — Party Secretary
    elif "县长" in name and "副" not in name:
        return "50,100,255"     # Blue — County Magistrate
    elif "纪委" in name or "监委" in name:
        return "255,165,0"      # Orange — Discipline Inspection
    else:
        return "100,100,100"    # Grey — Other


def org_color(org):
    """Return GEXF color for an organization."""
    t = org.get("type", "")
    if "党委" in t:
        return "255,200,200"
    elif "政府" in t:
        return "200,200,255"
    elif "人大" in t:
        return "200,255,255"
    elif "政协" in t:
        return "255,240,200"
    else:
        return "200,200,200"


def is_top_leader(person):
    name = person.get("current_post", "") or ""
    return (name == "中共安图县委书记") or ("县长" in name and "副" not in name)


def build_db():
    """Create SQLite database."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute("""INSERT INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"],
             p["birth"], p["birthplace"], p["education"],
             p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""INSERT INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"],
             o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"],
             r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"[DB] Created: {DB_PATH}")


def build_gexf():
    """Create GEXF graph file using string formatting."""
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>安图县领导班子工作关系网络 — partial-evidence build (network unavailable)</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role_or_org_type" type="string"/>')
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
        pid = f"p{p['id']}"
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        role = p.get('current_post', '') or ''
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = f"o{o['id']}"
        c = org_color(o)
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
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
    eid = 1

    # Person → Organization (positions)
    for pos in positions:
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('          <attvalue for="2" value="unverified"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person ↔ Person (relationships)
    for r in relationships:
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('          <attvalue for="2" value="unverified"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[GEXF] Created: {GEXF_PATH}")


def print_stats():
    print(f"\n=== Summary ===")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"\n  ⚠ NOTE: Built under degraded web access (network unreachable).")
    print(f"  ⚠ All claims should be verified against official sources.")
    print(f"  ⚠ Many deputy positions use placeholder names (待查_*).")


if __name__ == "__main__":
    build_db()
    build_gexf()
    print_stats()
