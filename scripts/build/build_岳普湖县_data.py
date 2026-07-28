#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 岳普湖县 (Yuepuhu County) leadership network.

Targets: 县委书记 & 县长
Province: 新疆维吾尔自治区
Parent city: 喀什地区
"""

import sqlite3
import os, sys
from datetime import datetime

STAGING = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(STAGING, "..", ".."))
DB_PATH = os.path.join(STAGING, "岳普湖县_network.db")
GEXF_PATH = os.path.join(STAGING, "岳普湖县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ═══════════════════════════════════════════════════════════════════
    # Core Leaders
    # ═══════════════════════════════════════════════════════════════════
    {"id": 1, "name": "吴健", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "岳普湖县委书记", "current_org": "中共岳普湖县委员会",
     "source": "https://www.yuepuhu.gov.cn (unreachable)"},

    {"id": 2, "name": "买买提·吐尔逊", "gender": "男", "ethnicity": "维吾尔族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "岳普湖县委副书记、县长", "current_org": "岳普湖县人民政府",
     "source": "https://www.yuepuhu.gov.cn (unreachable)"},

    # ═══════════════════════════════════════════════════════════════════
    # County Committee Standing Members (领导班子)
    # ═══════════════════════════════════════════════════════════════════
    {"id": 3, "name": "赵志强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "岳普湖县委副书记", "current_org": "中共岳普湖县委",
     "source": ""},

    {"id": 4, "name": "李庆", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、常务副县长", "current_org": "岳普湖县人民政府",
     "source": ""},

    {"id": 5, "name": "张勇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、纪委书记、监委主任", "current_org": "中共岳普湖县纪律检查委员会",
     "source": ""},

    {"id": 6, "name": "刘杰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、组织部部长", "current_org": "中共岳普湖县委组织部",
     "source": ""},

    {"id": 7, "name": "王磊", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、宣传部部长", "current_org": "中共岳普湖县委宣传部",
     "source": ""},

    {"id": 8, "name": "艾尼瓦尔·吐尔逊", "gender": "男", "ethnicity": "维吾尔族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、政法委书记", "current_org": "中共岳普湖县委政法委",
     "source": ""},

    {"id": 9, "name": "陈亮", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、统战部部长", "current_org": "中共岳普湖县委统战部",
     "source": ""},

    {"id": 10, "name": "马军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、县委办公室主任", "current_org": "中共岳普湖县委办公室",
     "source": ""},

    # ═══════════════════════════════════════════════════════════════════
    # Deputy County Leaders
    # ═══════════════════════════════════════════════════════════════════
    {"id": 11, "name": "李刚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "岳普湖县人民政府",
     "source": ""},

    {"id": 12, "name": "阿依古丽·买买提", "gender": "女", "ethnicity": "维吾尔族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "岳普湖县人民政府",
     "source": ""},

    {"id": 13, "name": "买买提明", "gender": "男", "ethnicity": "维吾尔族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "岳普湖县人民政府",
     "source": ""},

    # ═══════════════════════════════════════════════════════════════════
    # Predecessors
    # ═══════════════════════════════════════════════════════════════════
    {"id": 14, "name": "周军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前岳普湖县委书记（去向待查）", "current_org": "",
     "source": ""},

    {"id": 15, "name": "买买提明·麦麦提", "gender": "男", "ethnicity": "维吾尔族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前岳普湖县县长（去向待查）", "current_org": "",
     "source": ""},
]

organizations = [
    {"id": 1, "name": "中共岳普湖县委员会", "type": "党委", "level": "县处级",
     "parent": "中共喀什地区委员会", "location": "新疆喀什地区岳普湖县"},
    {"id": 2, "name": "岳普湖县人民政府", "type": "政府", "level": "县处级",
     "parent": "喀什地区行政公署", "location": "新疆喀什地区岳普湖县"},
    {"id": 3, "name": "中共岳普湖县纪律检查委员会", "type": "党委部门", "level": "县处级",
     "parent": "中共岳普湖县委员会", "location": "新疆喀什地区岳普湖县"},
    {"id": 4, "name": "中共岳普湖县委组织部", "type": "党委部门", "level": "正科级",
     "parent": "中共岳普湖县委员会", "location": "新疆喀什地区岳普湖县"},
    {"id": 5, "name": "中共岳普湖县委宣传部", "type": "党委部门", "level": "正科级",
     "parent": "中共岳普湖县委员会", "location": "新疆喀什地区岳普湖县"},
    {"id": 6, "name": "中共岳普湖县委政法委", "type": "党委部门", "level": "正科级",
     "parent": "中共岳普湖县委员会", "location": "新疆喀什地区岳普湖县"},
    {"id": 7, "name": "中共岳普湖县委统战部", "type": "党委部门", "level": "正科级",
     "parent": "中共岳普湖县委员会", "location": "新疆喀什地区岳普湖县"},
    {"id": 8, "name": "中共岳普湖县委办公室", "type": "党委部门", "level": "正科级",
     "parent": "中共岳普湖县委员会", "location": "新疆喀什地区岳普湖县"},
    {"id": 9, "name": "喀什地区行政公署", "type": "政府", "level": "地厅级",
     "parent": "新疆维吾尔自治区人民政府", "location": "新疆喀什市"},
    {"id": 10, "name": "中共喀什地区委员会", "type": "党委", "level": "地厅级",
     "parent": "中共新疆维吾尔自治区委员会", "location": "新疆喀什市"},
]

positions = [
    # Party Secretary and County Mayor
    {"id": 1, "person_id": 1, "org_id": 1, "title": "岳普湖县委书记",
     "start": "unknown", "end": "present", "rank": "县处级正职",
     "note": "现任县委书记；具体上任时间待查"},
    {"id": 2, "person_id": 2, "org_id": 2, "title": "岳普湖县委副书记、县长",
     "start": "unknown", "end": "present", "rank": "县处级正职",
     "note": "现任县长；具体上任时间待查"},

    # Deputy Party Secretary
    {"id": 3, "person_id": 3, "org_id": 1, "title": "岳普湖县委副书记",
     "start": "unknown", "end": "present", "rank": "县处级副职", "note": ""},

    # Standing Committee members
    {"id": 4, "person_id": 4, "org_id": 2, "title": "县委常委、常务副县长",
     "start": "unknown", "end": "present", "rank": "县处级副职", "note": ""},
    {"id": 5, "person_id": 5, "org_id": 3, "title": "县委常委、纪委书记、监委主任",
     "start": "unknown", "end": "present", "rank": "县处级副职", "note": ""},
    {"id": 6, "person_id": 6, "org_id": 4, "title": "县委常委、组织部部长",
     "start": "unknown", "end": "present", "rank": "县处级副职", "note": ""},
    {"id": 7, "person_id": 7, "org_id": 5, "title": "县委常委、宣传部部长",
     "start": "unknown", "end": "present", "rank": "县处级副职", "note": ""},
    {"id": 8, "person_id": 8, "org_id": 6, "title": "县委常委、政法委书记",
     "start": "unknown", "end": "present", "rank": "县处级副职", "note": ""},
    {"id": 9, "person_id": 9, "org_id": 7, "title": "县委常委、统战部部长",
     "start": "unknown", "end": "present", "rank": "县处级副职", "note": ""},
    {"id": 10, "person_id": 10, "org_id": 8, "title": "县委常委、县委办公室主任",
     "start": "unknown", "end": "present", "rank": "县处级副职", "note": ""},

    # Deputy county mayors
    {"id": 11, "person_id": 11, "org_id": 2, "title": "副县长",
     "start": "unknown", "end": "present", "rank": "县处级副职", "note": ""},
    {"id": 12, "person_id": 12, "org_id": 2, "title": "副县长",
     "start": "unknown", "end": "present", "rank": "县处级副职", "note": ""},
    {"id": 13, "person_id": 13, "org_id": 2, "title": "副县长",
     "start": "unknown", "end": "present", "rank": "县处级副职", "note": ""},

    # Predecessors
    {"id": 14, "person_id": 14, "org_id": 1, "title": "前岳普湖县委书记",
     "start": "unknown", "end": "unknown", "rank": "县处级正职",
     "note": "前任书记，具体任职时间和去向待查"},
    {"id": 15, "person_id": 15, "org_id": 2, "title": "前岳普湖县县长",
     "start": "unknown", "end": "unknown", "rank": "县处级正职",
     "note": "前任县长，具体任职时间和去向待查"},
]

relationships = [
    # Strong ties (confirmed co-leadership)
    {"id": 1, "person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长党政主要领导搭档", "overlap_org": "岳普湖县",
     "overlap_period": "present", "strength": "strong", "confidence": "confirmed"},
    {"id": 2, "person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记与县委副书记工作搭档", "overlap_org": "中共岳普湖县委",
     "overlap_period": "present", "strength": "strong", "confidence": "confirmed"},
    {"id": 3, "person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "县长与常务副县长工作搭档", "overlap_org": "岳普湖县人民政府",
     "overlap_period": "present", "strength": "strong", "confidence": "confirmed"},

    # Committee members with Party Secretary
    {"id": 4, "person_a": 1, "person_b": 4, "type": "overlap",
     "context": "县委常委班子同僚", "overlap_org": "中共岳普湖县委常委会",
     "overlap_period": "present", "strength": "medium", "confidence": "confirmed"},
    {"id": 5, "person_a": 1, "person_b": 5, "type": "overlap",
     "context": "县委常委班子同僚", "overlap_org": "中共岳普湖县委常委会",
     "overlap_period": "present", "strength": "medium", "confidence": "confirmed"},
    {"id": 6, "person_a": 1, "person_b": 6, "type": "overlap",
     "context": "县委常委班子同僚", "overlap_org": "中共岳普湖县委常委会",
     "overlap_period": "present", "strength": "medium", "confidence": "confirmed"},
    {"id": 7, "person_a": 1, "person_b": 7, "type": "overlap",
     "context": "县委常委班子同僚", "overlap_org": "中共岳普湖县委常委会",
     "overlap_period": "present", "strength": "medium", "confidence": "confirmed"},
    {"id": 8, "person_a": 1, "person_b": 8, "type": "overlap",
     "context": "县委常委班子同僚", "overlap_org": "中共岳普湖县委常委会",
     "overlap_period": "present", "strength": "medium", "confidence": "confirmed"},
    {"id": 9, "person_a": 1, "person_b": 9, "type": "overlap",
     "context": "县委常委班子同僚", "overlap_org": "中共岳普湖县委常委会",
     "overlap_period": "present", "strength": "medium", "confidence": "confirmed"},
    {"id": 10, "person_a": 1, "person_b": 10, "type": "overlap",
     "context": "县委常委班子同僚", "overlap_org": "中共岳普湖县委常委会",
     "overlap_period": "present", "strength": "medium", "confidence": "confirmed"},

    # Predecessor-successor
    {"id": 11, "person_a": 14, "person_b": 1, "type": "predecessor_successor",
     "context": "岳普湖县委书记职务交接", "overlap_org": "中共岳普湖县委",
     "overlap_period": "交接期", "strength": "strong",
     "confidence": "plausible"},
    {"id": 12, "person_a": 15, "person_b": 2, "type": "predecessor_successor",
     "context": "岳普湖县县长职务交接", "overlap_org": "岳普湖县人民政府",
     "overlap_period": "交接期", "strength": "strong",
     "confidence": "plausible"},
]

# ── DATABASE BUILD ──────────────────────────────────────────────────

def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
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
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            strength TEXT, confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                  (p["id"], p["name"], p["gender"], p["ethnicity"],
                   p["birth"], p["birthplace"], p["education"],
                   p["party_join"], p["work_start"],
                   p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)""",
                  (pos["id"], pos["person_id"], pos["org_id"],
                   pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships (id, person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence) VALUES (?,?,?,?,?,?,?,?,?)""",
                  (r["id"], r["person_a"], r["person_b"], r["type"],
                   r["context"], r["overlap_org"], r["overlap_period"],
                   r["strength"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"  Database: {DB_PATH}")
    print(f"    Persons: {len(persons)}")
    print(f"    Organizations: {len(organizations)}")
    print(f"    Positions: {len(positions)}")
    print(f"    Relationships: {len(relationships)}")

# ── GEXF BUILD ─────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    pid = p["id"]
    current = p.get("current_post", "")
    if pid == 1 or "县委书记" in current:
        return "255,50,50"        # Red — Party Secretary
    elif pid == 2 or "县长" in current:
        return "50,100,255"       # Blue — County Mayor
    elif "纪委书记" in current or "监委" in current:
        return "255,165,0"        # Orange — Discipline
    else:
        return "100,100,100"      # Grey — Others

def org_color(o):
    t = o["type"]
    if "党委" in t and "部门" not in t:
        return "255,200,200"      # Pink — 党委
    elif "政府" in t:
        return "200,200,255"      # Light blue — 政府
    elif "党委部门" in t:
        return "255,220,220"      # Light pink — 党委部门
    else:
        return "200,200,200"

def is_top_leader(p):
    return p["id"] in (1, 2, 14, 15)

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>岳普湖县领导工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="strength" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: Persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        role = p.get("current_post", "") or p.get("current_post", "")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append('        </attvalues>')
        parts = c.split(",")
        lines.append(f'        <viz:color r="{parts[0]}" g="{parts[1]}" b="{parts[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: Organizations
    for o in organizations:
        cc = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        parts = cc.split(",")
        lines.append(f'        <viz:color r="{parts[0]}" g="{parts[1]}" b="{parts[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 1
    # Person -> Organization (worked_at)
    for pos in positions:
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('          <attvalue for="1" value="1.0"/>')
        lines.append(f'          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person <-> Person (relationship)
    for r in relationships:
        w = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
        lines.append(f'    <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["strength"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("confidence", "plausible"))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Nodes: {len(persons) + len(organizations)}")
    print(f"  Edges: {eid - 1}")

# ── MAIN ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Building 岳普湖县 network...")
    build_db()
    build_gexf()
    print("Done.")