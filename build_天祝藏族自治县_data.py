#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 天祝藏族自治县 (Tianzhu Tibetan Autonomous County, Gansu) leadership network.

天祝藏族自治县 — 甘肃省武威市下辖自治县, 祁连山东端.
Covers current Party Secretary (崔振华), County Mayor (王海青), their predecessors,
key leadership, and relationship network.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/gansu_天祝藏族自治县")
os.makedirs(STAGING, exist_ok=True)

DB_PATH = os.path.join(STAGING, "天祝藏族自治县_network.db")
GEXF_PATH = os.path.join(STAGING, "天祝藏族自治县_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── A. County-level top leadership (current) ──

    # 崔振华 — 天祝县委书记 (as of 2026.07)
    {"id":1,"name":"崔振华","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"天祝藏族自治县委书记",
     "current_org":"中共天祝藏族自治县委员会",
     "source":"https://www.gstianzhu.gov.cn"},

    # 王海青 — 天祝县县长 (as of 2026.07)
    {"id":2,"name":"王海青","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"天祝藏族自治县人民政府县长",
     "current_org":"天祝藏族自治县人民政府",
     "source":"https://www.gstianzhu.gov.cn"},

    # ── B. Predecessors — 县委书记 ──

    # 李鹏 — 前任县委书记 (Wikipedia listing, likely 2021-2025/2026)
    {"id":3,"name":"李鹏","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"原天祝县委书记（去向待查）",
     "current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E5%A4%A9%E7%A5%9D%E8%97%8F%E6%97%8F%E8%87%AA%E6%B2%BB%E5%8E%BF"},

    # ── C. Predecessors — 县长 ──

    # 沈忠道 — 前任县长
    {"id":4,"name":"沈忠道","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"原天祝县长（去向待查）",
     "current_org":"",
     "source":"https://zh.wikipedia.org/wiki/%E5%A4%A9%E7%A5%9D%E8%97%8F%E6%97%8F%E8%87%AA%E6%B2%BB%E5%8E%BF"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # 天祝县级核心
    {"id":1,"name":"中共天祝藏族自治县委员会","type":"党委","level":"县级","parent":"中共武威市委员会","location":"甘肃省武威市天祝藏族自治县"},
    {"id":2,"name":"天祝藏族自治县人民政府","type":"政府","level":"县级","parent":"武威市人民政府","location":"甘肃省武威市天祝藏族自治县"},
    {"id":3,"name":"天祝藏族自治县人大常委会","type":"人大","level":"县级","parent":"武威市人大常委会","location":"甘肃省武威市天祝藏族自治县"},
    {"id":4,"name":"天祝藏族自治县政协","type":"政协","level":"县级","parent":"政协武威市委员会","location":"甘肃省武威市天祝藏族自治县"},
    {"id":5,"name":"中共天祝藏族自治县纪律检查委员会","type":"党委","level":"县级","parent":"中共天祝藏族自治县委员会","location":"甘肃省武威市天祝藏族自治县"},

    # 上级
    {"id":6,"name":"中共武威市委员会","type":"党委","level":"地级","parent":"中共甘肃省委员会","location":"甘肃省武威市凉州区"},
    {"id":7,"name":"武威市人民政府","type":"政府","level":"地级","parent":"甘肃省人民政府","location":"甘肃省武威市凉州区"},
]

# =========================================================================
# POSITIONS (career timeline edges)
# =========================================================================
positions = [
    # 崔振华 — 书记
    {"id":1,"person_id":1,"org_id":1,"title":"天祝藏族自治县委书记","start":"","end":"present","rank":"正县级","note":"据2026年7月7日报道任县委书记"},
    {"id":2,"person_id":1,"org_id":6,"title":"前任职务（待查）","start":"","end":"","rank":"","note":"崔振华任县委书记前的职务待查"},

    # 王海青 — 县长
    {"id":10,"person_id":2,"org_id":2,"title":"天祝藏族自治县人民政府县长","start":"","end":"present","rank":"正县级","note":"据2026年7月12日报道任县长"},
    {"id":11,"person_id":2,"org_id":6,"title":"前任职务（待查）","start":"","end":"","rank":"","note":"王海青任县长前的职务待查"},

    # 李鹏 — 前任书记
    {"id":20,"person_id":3,"org_id":1,"title":"天祝藏族自治县委书记","start":"","end":"","rank":"正县级","note":"维基百科记载，任期和结局待查"},

    # 沈忠道 — 前任县长
    {"id":30,"person_id":4,"org_id":2,"title":"天祝藏族自治县人民政府县长","start":"","end":"","rank":"正县级","note":"维基百科记载，任期和去向待查"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 崔振华 ← → 王海青: 党政一把手
    {"id":1,"person_a":1,"person_b":2,"type":"superior_subordinate",
     "context":"崔振华（书记）与王海青（县长）为党政一把手搭档",
     "overlap_org":"中共天祝藏族自治县委员会/天祝藏族自治县人民政府","overlap_period":"2026年至今（具体起始时间待确认）"},

    # 崔振华 ← → 李鹏: 书记交接
    {"id":2,"person_a":1,"person_b":3,"type":"predecessor_successor",
     "context":"李鹏→崔振华: 崔振华接任天祝县委书记，前任为李鹏",
     "overlap_org":"中共天祝藏族自治县委员会","overlap_period":"交接（具体时间待确认）"},

    # 王海青 ← → 沈忠道: 县长交接
    {"id":3,"person_a":2,"person_b":4,"type":"predecessor_successor",
     "context":"沈忠道→王海青: 王海青接任天祝县长，前任为沈忠道",
     "overlap_org":"天祝藏族自治县人民政府","overlap_period":"交接（具体时间待确认）"},
]

# =========================================================================
# HELPER FUNCTIONS
# =========================================================================
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    """Return color based on role."""
    role = p["current_post"]
    if "书记" in role and "纪委" not in role:
        return "255,50,50"    # Red — Party Secretary
    elif "县长" in role or "市长" in role or "区长" in role:
        return "50,100,255"   # Blue — Government leader
    elif "纪委书记" in role or "纪委" in role:
        return "255,165,0"    # Orange — Discipline
    elif "人大" in role:
        return "200,255,255"  # Cyan — People's Congress
    elif "政协" in role:
        return "255,240,200"  # Cream — CPPCC
    else:
        return "100,100,100"  # Grey — Others

def is_top_leader(p):
    """Top leaders get larger node size."""
    return p["id"] in [1, 2]  # 书记, 县长

def org_color(o):
    """Return color for organization nodes."""
    t = o["type"]
    if t == "党委":
        return "255,200,200"
    elif t == "政府":
        return "200,200,255"
    elif t == "人大":
        return "200,255,255"
    elif t == "政协":
        return "255,240,200"
    else:
        return "200,200,200"

# =========================================================================
# BUILD DATABASE
# =========================================================================
def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
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
            id INTEGER PRIMARY KEY,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                  (p["id"],p["name"],p["gender"],p["ethnicity"],
                   p["birth"],p["birthplace"],p["education"],
                   p["party_join"],p["work_start"],
                   p["current_post"],p["current_org"],p["source"]))

    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                  (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)""",
                  (pos["id"],pos["person_id"],pos["org_id"],
                   pos["title"],pos["start"],pos["end"],
                   pos["rank"],pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships VALUES (?,?,?,?,?,?,?)""",
                  (r["id"],r["person_a"],r["person_b"],
                   r["type"],r["context"],r["overlap_org"],r["overlap_period"]))

    conn.commit()
    conn.close()

# =========================================================================
# BUILD GEXF
# =========================================================================
def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent / github.com/gov-relation</creator>')
    lines.append('    <description>天祝藏族自治县（甘肃省武威市）领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="birth" type="string"/>')
    lines.append('      <attribute id="3" title="birthplace" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
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
        lines.append(f'          <attvalue for="2" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birthplace"])}"/>')
        lines.append('        </attvalues>')
        cr = c.split(",")
        lines.append(f'        <viz:color r="{cr[0]}" g="{cr[1]}" b="{cr[2]}"/>')
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
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        cr = c.split(",")
        lines.append(f'        <viz:color r="{cr[0]}" g="{cr[1]}" b="{cr[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person->Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])} - {esc(pos["end"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person<->Person (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    build_db()
    build_gexf()

    # Stats
    print(f"Database: {DB_PATH}")
    print(f"GEXF:     {GEXF_PATH}")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["persons","organizations","positions","relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        cnt = c.fetchone()[0]
        print(f"  {table}: {cnt}")
    conn.close()
    print("Done.")
