#!/usr/bin/env python3
"""
临武县领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for 临武县 leadership network.
Investigation date: 2026-07-24

IMPORTANT: All external web search (Exa, Jina, Baidu, gov sites) was unavailable during
this investigation. This build script records the gap explicitly. All leader names
and biographies remain unverified pending successful web research.

Current leadership (as of 2026-07-24): UNKNOWN
    县委书记: 待查 (web search unavailable)
    县长: 待查 (web search unavailable)
"""

import sqlite3
import os
import sys
from datetime import datetime

# ── Paths (relative to repo root) ──
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

# Staging-aware paths
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
STAGING_CANDIDATE = os.path.join(REPO_ROOT, "data", "tmp", "hunan_临武县")
if os.path.basename(THIS_DIR) == "hunan_临武县":
    STAGING_DIR = THIS_DIR
elif os.path.isdir(STAGING_CANDIDATE):
    STAGING_DIR = STAGING_CANDIDATE
else:
    STAGING_DIR = THIS_DIR

DB_PATH = os.path.join(STAGING_DIR, "临武县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "临武县_network.gexf")

# ═══════════════════════════════════════════════════════════
# RESEARCH DATA
# ═══════════════════════════════════════════════════════════
# ALL DATA BELOW IS UNVERIFIED — Web research was entirely blocked.
# See open gaps in report for details.

PERSONS = [
    # ── 1. 县委书记 (UNKNOWN) ──
    {
        "id": 1,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共临武县委书记",
        "current_org": "中共临武县委员会",
        "source": "研究时无法访问外部网络；见 open_gaps",
        "notes": "姓名未知。郴州市下辖临武县，2026年7月24日时县委书记待确认。县委是全县的领导核心。",
    },
    # ── 2. 县长 (UNKNOWN) ──
    {
        "id": 2,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "临武县人民政府县长",
        "current_org": "临武县人民政府",
        "source": "研究时无法访问外部网络；见 open_gaps",
        "notes": "姓名未知。郴州市下辖临武县，2026年7月24日时县长待确认。县政府是全县的行政领导机关。",
    },
    # ── 3. 临武县人大常委会主任 (UNKNOWN) ──
    {
        "id": 3,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "临武县人大常委会主任",
        "current_org": "临武县人民代表大会常务委员会",
        "source": "研究时无法访问外部网络；见 open_gaps",
        "notes": "姓名未知。",
    },
    # ── 4. 临武县政协主席 (UNKNOWN) ──
    {
        "id": 4,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "临武县政协主席",
        "current_org": "中国人民政治协商会议临武县委员会",
        "source": "研究时无法访问外部网络；见 open_gaps",
        "notes": "姓名未知。",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共临武县委员会", "type": "党委", "level": "县处级", "parent": "中共郴州市委", "location": "湖南省郴州市临武县"},
    {"id": 2, "name": "临武县人民政府", "type": "政府", "level": "县处级", "parent": "郴州市人民政府", "location": "湖南省郴州市临武县"},
    {"id": 3, "name": "临武县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "郴州市人大常委会", "location": "湖南省郴州市临武县"},
    {"id": 4, "name": "中国人民政治协商会议临武县委员会", "type": "政协", "level": "县处级", "parent": "政协郴州市委员会", "location": "湖南省郴州市临武县"},
    {"id": 5, "name": "中共郴州市委", "type": "党委", "level": "地市级", "parent": "中共湖南省委", "location": "湖南省郴州市"},
    {"id": 6, "name": "郴州市人民政府", "type": "政府", "level": "地市级", "parent": "湖南省人民政府", "location": "湖南省郴州市"},
    {"id": 7, "name": "临武县纪委监委", "type": "党委", "level": "县处级", "parent": "中共临武县委员会", "location": "湖南省郴州市临武县"},
]

POSITIONS = [
    # ── 县委书记 ──
    {"person_id": 1, "org_id": 1, "title": "中共临武县委书记", "start": "", "end": "", "rank": "正处级", "note": "现任；具体任职起始时间待查"},
    # ── 县长 ──
    {"person_id": 2, "org_id": 2, "title": "临武县人民政府县长", "start": "", "end": "", "rank": "正处级", "note": "现任；具体任职起始时间待查"},
    # ── 人大主任 ──
    {"person_id": 3, "org_id": 3, "title": "临武县人大常委会主任", "start": "", "end": "", "rank": "正处级", "note": "现任"},
    # ── 政协主席 ──
    {"person_id": 4, "org_id": 4, "title": "政协临武县委员会主席", "start": "", "end": "", "rank": "正处级", "note": "现任"},
]

RELATIONSHIPS = [
    # All relationships are unverified — names unknown
    {"person_a": 1, "person_b": 2, "type": "搭档", "context": "县委书记与县长为临武县党政正职搭档关系，具体搭档时间待查", "overlap_org": "临武县", "overlap_period": ""},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记与人大常委会主任同属临武县四套班子", "overlap_org": "临武县", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记与政协主席同属临武县四套班子", "overlap_org": "临武县", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长与人大常委会主任同属临武县四套班子", "overlap_org": "临武县", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "县长与政协主席同属临武县四套班子", "overlap_org": "临武县", "overlap_period": ""},
]

# ═══════════════════════════════════════════════════════════
# DATABASE BUILD
# ═══════════════════════════════════════════════════════════

def create_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)

    for t in ["relationships", "positions", "organizations", "persons"]:
        conn.execute(f"DROP TABLE IF EXISTS {t}")

    conn.execute("""
        CREATE TABLE persons (
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
        )
    """)
    conn.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        )
    """)
    conn.execute("""
        CREATE TABLE positions (
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
        )
    """)
    conn.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    cols_p = ["id", "name", "gender", "ethnicity", "birth", "birthplace",
              "education", "party_join", "work_start", "current_post", "current_org", "source"]
    for p in PERSONS:
        vals = [p.get(c, "") for c in cols_p]
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?']*len(cols_p))})", vals)

    cols_o = ["id", "name", "type", "level", "parent", "location"]
    for o in ORGANIZATIONS:
        vals = [o.get(c, "") for c in cols_o]
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?']*len(cols_o))})", vals)

    cols_pos = ["person_id", "org_id", "title", "start_date", "end_date", "rank", "note"]
    for pos in POSITIONS:
        vals = [pos.get(c, "") for c in cols_pos]
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?']*len(cols_pos))})", vals)

    cols_r = ["person_a", "person_b", "type", "context", "overlap_org", "overlap_period"]
    for r in RELATIONSHIPS:
        vals = [r.get(c, "") for c in cols_r]
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?']*len(cols_r))})", vals)

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")


# ═══════════════════════════════════════════════════════════
# GEXF BUILD
# ═══════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(title):
    t = title
    if "书记" in t and "副" not in t and "政协" not in t and "人大" not in t:
        return "200,30,30"
    if "县长" in t and "副" not in t:
        return "30,100,200"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    if "副" in t:
        return "100,150,220"
    return "180,180,180"

def is_top_leader(name):
    return name in ["（待查）"]

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(org_type, "200,200,200")

def generate_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>临武县领导班子工作关系网络 — 注意：所有领导人姓名在外网不可用期间待查</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in PERSONS:
        c = person_color(p["current_post"])
        sz = "60.0" if is_top_leader(p["name"]) else "35.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        cr, cg, cb = c.split(",")
        lines.append(f'        <viz:color r="{cr}" g="{cg}" b="{cb}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in ORGANIZATIONS:
        c = org_color(o["type"])
        cr, cg, cb = c.split(",")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{cr}" g="{cg}" b="{cb}" a="0.8"/>')
        lines.append('        <viz:size value="20.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    added_edges = set()
    for pos in POSITIONS:
        pid = pos["person_id"]
        oid = pos["org_id"]
        eid += 1
        edge_key = f"p{pid}-o{oid}-{pos['title']}"
        if edge_key in added_edges:
            continue
        added_edges.add(edge_key)
        lines.append(f'      <edge id="{eid}" source="p{pid}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos["start"])}—{esc(pos["end"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in RELATIONSHIPS:
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

    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF graph created: {GEXF_PATH}")


def print_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        cnt = c.fetchone()[0]
        print(f"  {table}: {cnt}")
    conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print("  临武县领导班子工作关系网络 — 数据构建")
    print("  调查日期: 2026-07-24")
    print("  ⚠️ 注意: 所有外网搜索不可用，领导人姓名待查")
    print("=" * 60)
    create_db()
    generate_gexf()
    print("\n📊 Summary:")
    print_stats()
    print("\n⚠️  此构建为占位符。所有个人姓名都是'待查'。")
    print("   当网络搜索恢复时，需要重新研究。")
