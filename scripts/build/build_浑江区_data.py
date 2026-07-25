#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Hunjiang District (浑江区), Baishan, Jilin."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/jilin_浑江区")
DB_PATH = os.path.join(TMP, "浑江区_network.db")
GEXF_PATH = os.path.join(TMP, "浑江区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {"id": 1, "name": "王明明", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "白山市浑江区委书记", "current_org": "中共白山市浑江区委员会",
     "source": "https://baike.baidu.com/item/%E6%B5%91%E6%B1%9F%E5%8C%BA"},
    {"id": 2, "name": "沈鹏飞", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "白山市浑江区委副书记、区长", "current_org": "白山市浑江区人民政府",
     "source": "https://baike.baidu.com/item/%E6%B5%91%E6%B1%9F%E5%8C%BA"},

    # ── Previous Leaders ──
    {"id": 3, "name": "张海", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原白山市浑江区委书记（已离任）", "current_org": "",
     "source": "https://baike.baidu.com/item/%E6%B5%91%E6%B1%9F%E5%8C%BA"},
]

organizations = [
    {"id": 1, "name": "中共白山市浑江区委员会", "type": "党委", "level": "县处级",
     "parent": "中共白山市委员会", "location": "吉林省白山市浑江区"},
    {"id": 2, "name": "白山市浑江区人民政府", "type": "政府", "level": "县处级",
     "parent": "白山市人民政府", "location": "吉林省白山市浑江区"},
    {"id": 3, "name": "浑江区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "白山市人大常委会", "location": "吉林省白山市浑江区"},
    {"id": 4, "name": "中国人民政治协商会议浑江区委员会", "type": "政协", "level": "县处级",
     "parent": "白山市政府", "location": "吉林省白山市浑江区"},
]

positions = [
    # Current leaders
    {"person_id": 1, "org_id": 1, "title": "白山市浑江区委书记",
     "start": "2025-12", "end": "present", "rank": "正县级",
     "note": "接替张海，2025年12月任免决定"},
    {"person_id": 2, "org_id": 2, "title": "白山市浑江区委副书记、区长",
     "start": "", "end": "present", "rank": "正县级",
     "note": "截至2026年7月现任"},

    # Previous leaders
    {"person_id": 3, "org_id": 1, "title": "白山市浑江区委书记",
     "start": "", "end": "2025-12", "rank": "正县级",
     "note": "据中国吉林网2025年12月26日任免决定离任"},
]

relationships = [
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "王明明接替张海任浑江区委书记",
     "overlap_org": "中共白山市浑江区委员会",
     "overlap_period": ""},
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "王明明作为区委书记与区长沈鹏飞搭班",
     "overlap_org": "浑江区",
     "overlap_period": ""},
]

# ── BUILD ────────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_role_color(name, post):
    """Return color by role for person nodes."""
    if "书记" in post and "纪委" not in post:
        return "255,50,50"
    if "区长" in post or "市长" in post or "县长" in post:
        return "50,100,255"
    if "纪委" in post or "监委" in post:
        return "255,165,0"
    return "100,100,100"

def person_role_size(name, post):
    """Return node size by role."""
    if "书记" in post and "纪委" not in post:
        return "20.0"
    if "区长" in post or "市长" in post or "县长" in post:
        return "20.0"
    return "12.0"

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
    }
    return colors.get(org_type, "200,200,200")


def build_db():
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
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, "end" TEXT, rank TEXT, note TEXT
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT
        );
    """)

    for p in persons:
        cur.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"],
             p["birth"], p["birthplace"], p["education"],
             p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""INSERT INTO positions
            (person_id, org_id, title, start, "end", rank, note)
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
    print(f"DB ready: {DB_PATH}")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append(f'    <description>Hunjiang District (浑江区) government personnel network - Baishan, Jilin</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="source" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_role_color(p["name"], p["current_post"])
        sz = person_role_size(p["name"], p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
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
    print(f"GEXF ready: {GEXF_PATH}")


if __name__ == "__main__":
    os.makedirs(TMP, exist_ok=True)
    build_db()
    build_gexf()
    print("Done.")
