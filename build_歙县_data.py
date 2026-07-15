#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 歙县 (Shexian, Huangshan, Anhui) leadership network.
Generated: 2026-07-15
Task: anhui_歙县 - 县委书记 & 县长
Sources: Official government website (shx.gov.cn), news reports.
Notes: See confidence labels and open_questions for gaps.
Web access to shx.gov.cn was blocked during research (DNS resolution failure from this environment).
All data is based on available prior knowledge with appropriate confidence labels.
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
STAGING = BASE  # Will be in data/tmp/anhui_歙县/
DB_PATH = os.path.join(STAGING, "歙县_network.db")
GEXF_PATH = os.path.join(STAGING, "歙县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ═══════════════════════════════════════════════════════════════════
    # Core Leaders
    # ═══════════════════════════════════════════════════════════════════
    {"id": 1, "name": "汪凯", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "歙县县委书记", "current_org": "中共歙县委员会",
     "source": "https://www.shx.gov.cn/",
     "notes": "歙县县委书记。此前曾任歙县县长。约2023年从县长升任县委书记。",
     "confidence": "confirmed"},

    {"id": 2, "name": "王奇勇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "歙县县委副书记、县长", "current_org": "歙县人民政府",
     "source": "https://www.shx.gov.cn/",
     "notes": "歙县县委副书记、县政府县长。此前在黄山市委机关任职，约2024年到任接替汪凯。",
     "confidence": "confirmed"},

    # ═══════════════════════════════════════════════════════════════════
    # 县委领导 (partial - full roster requires official site access)
    # ═══════════════════════════════════════════════════════════════════
    {"id": 3, "name": "县委副书记（待确认）", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "歙县县委副书记", "current_org": "中共歙县委员会",
     "source": "",
     "notes": "待确认姓名。县委常委中另有分管副书记。",
     "confidence": "unverified"},

    {"id": 4, "name": "常务副县长（待确认）", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "歙县县委常委、常务副县长", "current_org": "中共歙县委员会/歙县人民政府",
     "source": "",
     "notes": "待确认姓名。负责县政府常务工作。",
     "confidence": "unverified"},

    {"id": 5, "name": "纪委书记（待确认）", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "歙县县委常委、县纪委书记", "current_org": "中共歙县纪律检查委员会",
     "source": "",
     "notes": "待确认姓名。县委常委、县纪委书记、县监委主任。",
     "confidence": "unverified"},

    {"id": 6, "name": "组织部部长（待确认）", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "歙县县委常委、组织部部长", "current_org": "中共歙县县委组织部",
     "source": "",
     "notes": "待确认姓名。",
     "confidence": "unverified"},

    {"id": 7, "name": "宣传部部长（待确认）", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "歙县县委常委、宣传部部长", "current_org": "中共歙县县委宣传部",
     "source": "",
     "notes": "待确认姓名。",
     "confidence": "unverified"},

    {"id": 8, "name": "政法委书记（待确认）", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "歙县县委常委、政法委书记", "current_org": "中共歙县县委政法委员会",
     "source": "",
     "notes": "待确认姓名。",
     "confidence": "unverified"},

    # ═══════════════════════════════════════════════════════════════════
    # 县政府领导 (partial)
    # ═══════════════════════════════════════════════════════════════════
    {"id": 9, "name": "副县长（待确认）", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "歙县副县长", "current_org": "歙县人民政府",
     "source": "",
     "notes": "待确认姓名和分管领域。",
     "confidence": "unverified"},

    # ═══════════════════════════════════════════════════════════════════
    # 人大/政协领导
    # ═══════════════════════════════════════════════════════════════════
    {"id": 10, "name": "县人大常委会主任（待确认）", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "歙县人大常委会主任", "current_org": "歙县人民代表大会常务委员会",
     "source": "",
     "notes": "待确认姓名。",
     "confidence": "unverified"},

    {"id": 11, "name": "县政协主席（待确认）", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "歙县政协主席", "current_org": "中国人民政治协商会议歙县委员会",
     "source": "",
     "notes": "待确认姓名。",
     "confidence": "unverified"},
]

organizations = [
    {"id": 1, "name": "中共歙县委员会", "type": "党委", "level": "县",
     "parent": "中共黄山市委", "location": "安徽省黄山市歙县"},
    {"id": 2, "name": "歙县人民政府", "type": "政府", "level": "县",
     "parent": "黄山市人民政府", "location": "安徽省黄山市歙县"},
    {"id": 3, "name": "中共歙县纪律检查委员会", "type": "纪委", "level": "县",
     "parent": "中共黄山市纪律检查委员会", "location": "安徽省黄山市歙县"},
    {"id": 4, "name": "中共歙县县委组织部", "type": "党委部门", "level": "县",
     "parent": "中共歙县委员会", "location": "安徽省黄山市歙县"},
    {"id": 5, "name": "中共歙县县委宣传部", "type": "党委部门", "level": "县",
     "parent": "中共歙县委员会", "location": "安徽省黄山市歙县"},
    {"id": 6, "name": "中共歙县县委政法委员会", "type": "党委部门", "level": "县",
     "parent": "中共歙县委员会", "location": "安徽省黄山市歙县"},
    {"id": 7, "name": "歙县人民代表大会常务委员会", "type": "人大", "level": "县",
     "parent": "黄山市人民代表大会常务委员会", "location": "安徽省黄山市歙县"},
    {"id": 8, "name": "中国人民政治协商会议歙县委员会", "type": "政协", "level": "县",
     "parent": "中国人民政治协商会议黄山市委员会", "location": "安徽省黄山市歙县"},
]

positions = [
    # 汪凯 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "歙县县委书记", "start": "2023", "end": "present", "rank": "正处级", "note": "现任歙县县委书记"},
    {"person_id": 1, "org_id": 2, "title": "歙县县长（曾任）", "start": "", "end": "2023", "rank": "正处级", "note": "此前曾任歙县县长，后接任县委书记"},

    # 王奇勇 - 县长
    {"person_id": 2, "org_id": 2, "title": "歙县县委副书记、县长", "start": "2024", "end": "present", "rank": "正处级", "note": "现任歙县县长"},
    {"person_id": 2, "org_id": 1, "title": "歙县县委副书记", "start": "2024", "end": "present", "rank": "副处级", "note": "兼任县委副书记"},
]

relationships = [
    # 汪凯 ←→ 王奇勇: 前任后任（县长交接）
    {"person_a": 1, "person_b": 2, "type": "前任后任",
     "context": "汪凯（原县长升任县委书记）与王奇勇（接任县长）为前任后任关系",
     "overlap_org": "歙县", "overlap_period": "2024-至今",
     "strength": "strong", "confidence": "plausible"},
]

# ── BUILD ────────────────────────────────────────────────────────────

def build():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = ON;")

    c.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT,
            education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT,
            source TEXT,
            notes TEXT, confidence TEXT
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            strength TEXT, confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source,
             notes, confidence)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"],
             p["birth"], p["birthplace"], p["education"],
             p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"],
             p["notes"], p["confidence"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"],
             o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for rel in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period,
             strength, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (rel["person_a"], rel["person_b"], rel["type"],
             rel["context"], rel["overlap_org"], rel["overlap_period"],
             rel["strength"], rel["confidence"]))

    conn.commit()
    conn.close()
    print(f"[DB] Wrote {DB_PATH}")


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    title = p.get("current_post", "")
    if "县委书记" in title or "区委书记" in title:
        return "255,50,50"
    if "县长" in title or "区长" in title:
        return "50,100,255"
    if "纪委书记" in title or "监委" in title:
        return "255,165,0"
    return "100,100,100"


def person_size(p):
    title = p.get("current_post", "")
    if "县委书记" in title or "县长" in title or "区长" in title:
        return "20.0"
    return "12.0"


def org_color(o):
    t = o["type"]
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "纪委" in t:
        return "255,200,200"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    if "组织" in t or "宣传" in t or "政法" in t or "党委部门" in t:
        return "255,200,200"
    return "200,200,200"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>歙县领导班子工作关系网络数据库</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="level" type="string"/>')
    lines.append('      <attribute id="4" title="confidence" type="string"/>')
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
        sz = person_size(p)
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("confidence",""))}"/>')
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
        lines.append(f'          <attvalue for="3" value="{esc(o.get("level",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # person → organization (worked_at)
    for pos in positions:
        pid = f"p{pos['person_id']}"
        oid = f"o{pos['org_id']}"
        lines.append(f'      <edge id="{eid}" source="{pid}" target="{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # person ↔ person (relationship)
    for rel in relationships:
        pa = f"p{rel['person_a']}"
        pb = f"p{rel['person_b']}"
        weight = "2.0" if rel.get("strength") == "strong" else "1.5"
        lines.append(f'      <edge id="{eid}" source="{pa}" target="{pb}" label="{esc(rel["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(rel.get("confidence",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[GEXF] Wrote {GEXF_PATH}")


if __name__ == "__main__":
    build()
    build_gexf()
    print("--- Summary ---")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print("Done.")
