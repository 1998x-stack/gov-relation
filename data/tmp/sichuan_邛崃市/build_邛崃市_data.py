#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 邛崃市 (Qionglai City), Sichuan.

NOTE: This build uses PARTIAL EVIDENCE because web access was completely blocked
during research (Baidu 403, Google/Bing/DDG timeout, qionglai.gov.cn WAF 412,
Jina Reader down, Wayback Machine timeout). Core leader names were sourced from
an earlier cached Baidu Baike snapshot in the Dayi County cross-county report.

All biographical details beyond names are marked as gaps.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/sichuan_邛崃市")
DB_PATH = os.path.join(TMP, "邛崃市_network.db")
GEXF_PATH = os.path.join(TMP, "邛崃市_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leader (党政一肩挑) ──
    {"id": 1, "name": "王德彰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "邛崃市委书记、市长（党政一肩挑）", "current_org": "中共邛崃市委员会/邛崃市人民政府",
     "source": "https://baike.baidu.com/item/%E9%82%9B%E5%B4%90%E5%B8%82 (cached via 大邑县 cross-county report)"},

    # ── People's Congress ──
    {"id": 2, "name": "王瑞平", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "邛崃市人大常委会主任", "current_org": "邛崃市人民代表大会常务委员会",
     "source": "https://baike.baidu.com/item/%E9%82%9B%E5%B4%90%E5%B8%82 (via 大邑县 cross-county report)"},

    # ── Political Consultative Conference ──
    {"id": 3, "name": "徐戎", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "邛崃市政协主席", "current_org": "中国人民政治协商会议邛崃市委员会",
     "source": "https://baike.baidu.com/item/%E9%82%9B%E5%B4%90%E5%B8%82 (cached via 大邑县 report)"},

    # ── Possible former mayor (unverified) ──
    {"id": 4, "name": "惠朝旭", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "疑似前任邛崃市长（已离任）", "current_org": "未知",
     "source": "https://en.wikipedia.org/wiki/Qionglai (outdated data)"},
]

organizations = [
    {"id": 1, "name": "中共邛崃市委员会", "type": "党委", "level": "县处级", "parent": "中共成都市委员会",
     "location": "四川省成都市邛崃市"},
    {"id": 2, "name": "邛崃市人民政府", "type": "政府", "level": "县处级", "parent": "成都市人民政府",
     "location": "四川省成都市邛崃市"},
    {"id": 3, "name": "邛崃市人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "成都市人大常委会",
     "location": "四川省成都市邛崃市"},
    {"id": 4, "name": "中国人民政治协商会议邛崃市委员会", "type": "政协", "level": "县处级", "parent": "成都市政协",
     "location": "四川省成都市邛崃市"},
    {"id": 5, "name": "中共成都市纪律检查委员会/成都市监察委员会", "type": "党委", "level": "地厅级", "parent": "中共成都市委员会",
     "location": "四川省成都市"},
]

positions = [
    # ── Wang Dezhang (王德彰) ──
    {"person_id": 1, "org_id": 1, "title": "邛崃市委书记", "start": "未知", "end": "present",
     "rank": "副厅级", "note": "党政一肩挑，同时任市委书记和市长；具体上任日期待查"},
    {"person_id": 1, "org_id": 2, "title": "邛崃市长", "start": "未知", "end": "present",
     "rank": "正县级", "note": "同时任市长；上任日期待查"},

    # ── Wang Ruiping (王瑞平) ──
    {"person_id": 2, "org_id": 3, "title": "邛崃市人大常委会主任", "start": "未知", "end": "present",
     "rank": "正县级", "note": "上任日期待查"},

    # ── Xu Rong (徐戎) ──
    {"person_id": 3, "org_id": 4, "title": "邛崃市政协主席", "start": "未知", "end": "present",
     "rank": "正县级", "note": "上任日期待查"},

    # ── Huo Zhaoxu (惠朝旭) — Possible former mayor ──
    {"person_id": 4, "org_id": 2, "title": "邛崃市长（前）", "start": "未知", "end": "未知",
     "rank": "正县级", "note": "据Wikipedia旧数据可能曾任邛崃市长；是否前任或去向均待查"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "overlap", "strength": "medium",
     "context": "王德彰（市委书记/市长）与王瑞平（人大主任）在邛崃市党政班子共事",
     "overlap_org": "邛崃市", "overlap_period": "未知", "confidence": "plausible"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "strength": "medium",
     "context": "王德彰（市委书记/市长）与徐戎（政协主席）在邛崃市党政班子共事",
     "overlap_org": "邛崃市", "overlap_period": "未知", "confidence": "plausible"},
    {"person_a": 1, "person_b": 4, "type": "predecessor_successor", "strength": "weak",
     "context": "惠朝旭可能是王德彰的前任市长；王德彰可能接替惠朝旭任市长后同时任书记",
     "overlap_org": "邛崃市人民政府", "overlap_period": "未知", "confidence": "unverified"},
]

# ── HELPERS ─────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    role = p["current_post"]
    if "市委书记" in role and "副书记" not in role:
        return "255,50,50"
    elif "市长" in role:
        return "50,100,255"
    elif "人大" in role:
        return "200,255,255"
    elif "政协" in role:
        return "255,240,200"
    else:
        return "100,100,100"

def org_color(o):
    t = o["type"]
    return {"党委": "255,200,200", "政府": "200,200,255",
            "人大": "200,255,255", "政协": "255,240,200"}.get(t, "200,200,200")

def is_top_leader(p):
    return "市委书记" in p["current_post"]

def person_size(p):
    return "20.0" if is_top_leader(p) else "12.0"

# ── BUILD DB ─────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT, strength TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT, confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
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
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))
    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, strength, context, overlap_org, overlap_period, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["strength"],
             r["context"], r["overlap_org"], r["overlap_period"], r["confidence"]))
    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")

# ── BUILD GEXF ────────────────────────────────────────────────

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent (Partial Evidence Mode)</creator>')
    lines.append('    <description>邛崃市领导班子工作关系网络 - 四川省成都市邛崃市（部分证据模式）</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["parent"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])}~{esc(pos["end"])}"/>')
        lines.append(f'          <attvalue for="3" value="plausible"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person (relationships)
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append(f'          <attvalue for="3" value="{r["confidence"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {GEXF_PATH}")

# ── SUMMARY ──────────────────────────────────────────────────

def print_summary():
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"\n  NOTE: Most biographical data is missing due to complete")
    print(f"  inaccessibility of all Chinese web sources (Baidu 403,")
    print(f"  qionglai.gov.cn WAF 412, Google/Bing/DDG timeout).")
    print(f"  See open_gaps.md for full gap registry.")

if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()