#!/usr/bin/env python3
"""
Build SQLite database and GEXF graph for 池州市领导班子 (Chizhou City Leadership Network).
Investigation date: 2026-07-15
Current 池州市委书记: 朱浩东 (as of 2026-07, confirmed by official news)
Current 池州市市长: 贺东 (as of 2026-07, confirmed by official 市长之窗 page)
"""

import sqlite3
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = SCRIPT_DIR
GRAPH_DIR = SCRIPT_DIR
os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(GRAPH_DIR, exist_ok=True)

DB_PATH = os.path.join(DB_DIR, "池州市_network.db")
GEXF_PATH = os.path.join(GRAPH_DIR, "池州市_network.gexf")

# ═══════════════════════════════════════════════════════════
# RESEARCH DATA (hard-coded)
# ═══════════════════════════════════════════════════════════

persons = [
    # ── 朱浩东 - 池州市委书记 (Party Secretary) ──
    {"id": 1, "name": "朱浩东", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "池州市委书记", "current_org": "中共池州市委",
     "source": "https://www.chizhou.gov.cn/Content/show/782319.html"},

    # ── 贺东 - 池州市市长 (Mayor) ──
    {"id": 2, "name": "贺东", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-06", "birthplace": "",
     "education": "省委党校研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "池州市委副书记、市政府市长、党组书记", "current_org": "池州市人民政府",
     "source": "https://www.chizhou.gov.cn/Leader/showList/3/2026.html"},

    # ── 巩文生 - 常务副市长 ──
    {"id": 3, "name": "巩文生", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-12", "birthplace": "",
     "education": "省委党校研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "池州市委常委、市政府常务副市长、党组副书记、市行政学院院长",
     "current_org": "池州市人民政府",
     "source": "https://www.chizhou.gov.cn/Leader/showList/3/3090.html"},

    # ── 曹霞 - 副市长 ──
    {"id": 4, "name": "曹霞", "gender": "女", "ethnicity": "汉族",
     "birth": "1970-09", "birthplace": "",
     "education": "省委党校研究生学历",
     "party_join": "致公党党员", "work_start": "",
     "current_post": "池州市政府副市长、致公党池州市基层委员会主委",
     "current_org": "池州市人民政府",
     "source": "https://www.chizhou.gov.cn/Leader/showList/3/1579.html"},

    # ── 胡军保 - 副市长 ──
    {"id": 5, "name": "胡军保", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "池州市政府副市长", "current_org": "池州市人民政府",
     "source": "https://www.chizhou.gov.cn/Leader/showList/3/1580.html"},

    # ── 王珏 - 副市长 ──
    {"id": 6, "name": "王珏", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "池州市政府副市长", "current_org": "池州市人民政府",
     "source": "https://www.chizhou.gov.cn/Leader/showList/3/2927.html"},

    # ── 柯春平 - 副市长 ──
    {"id": 7, "name": "柯春平", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "池州市政府副市长", "current_org": "池州市人民政府",
     "source": "https://www.chizhou.gov.cn/Leader/showList/3/3002.html"},

    # ── 汪政 - 秘书长 ──
    {"id": 8, "name": "汪政", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "池州市政府秘书长", "current_org": "池州市人民政府",
     "source": "https://www.chizhou.gov.cn/Leader/showList/3/3024.html"},

    # ── 席峰 - 市政协主席 ──
    {"id": 9, "name": "席峰", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "池州市政协主席", "current_org": "池州市政协",
     "source": "https://www.chizhou.gov.cn/Content/show/782417.html"},
]

organizations = [
    {"id": 1, "name": "中共池州市委", "type": "党委", "level": "地级市", "parent": "中共安徽省委", "location": "池州市"},
    {"id": 2, "name": "池州市人民政府", "type": "政府", "level": "地级市", "parent": "安徽省人民政府", "location": "池州市"},
    {"id": 3, "name": "池州市政协", "type": "政协", "level": "地级市", "parent": "安徽省政协", "location": "池州市"},
]

positions = [
    # 朱浩东
    {"person_id": 1, "org_id": 1, "title": "池州市委书记", "start": "", "end": "present", "rank": "正厅级", "note": "现任，截至2026年7月"},

    # 贺东
    {"person_id": 2, "org_id": 1, "title": "池州市委副书记", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "池州市政府市长、党组书记", "start": "", "end": "present", "rank": "正厅级", "note": "现任，截至2026年7月"},

    # 巩文生
    {"person_id": 3, "org_id": 1, "title": "池州市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "池州市政府常务副市长、党组副书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},

    # 曹霞
    {"person_id": 4, "org_id": 2, "title": "池州市政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": "致公党党员"},

    # 胡军保
    {"person_id": 5, "org_id": 2, "title": "池州市政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},

    # 王珏
    {"person_id": 6, "org_id": 2, "title": "池州市政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},

    # 柯春平
    {"person_id": 7, "org_id": 2, "title": "池州市政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},

    # 汪政
    {"person_id": 8, "org_id": 2, "title": "池州市政府秘书长", "start": "", "end": "present", "rank": "正处级", "note": ""},

    # 席峰
    {"person_id": 9, "org_id": 3, "title": "池州市政协主席", "start": "", "end": "present", "rank": "正厅级", "note": ""},
]

relationships = [
    # 朱浩东 - 贺东: 书记与市长搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "市委书记与市长党政搭档", "overlap_org": "中共池州市委/池州市人民政府",
     "overlap_period": "2025-至今"},

    # 贺东 - 巩文生: 市长与常务副市长
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "市长与常务副市长", "overlap_org": "池州市人民政府",
     "overlap_period": "至今"},

    # 朱浩东 - 巩文生: 书记与常委
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "市委书记与市委常委", "overlap_org": "中共池州市委",
     "overlap_period": "至今"},
]

# ═══════════════════════════════════════════════════════════
# DATABASE BUILD
# ═══════════════════════════════════════════════════════════

def build_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
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

        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );

        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            "end" TEXT,
            rank TEXT,
            note TEXT
        );

        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
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
            (person_id, org_id, title, start, "end", rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"],
             r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")


# ═══════════════════════════════════════════════════════════
# GEXF BUILD
# ═══════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return color for person by role."""
    title = p.get("current_post", "")
    if "书记" in title and "纪委" not in title:
        # Party Secretary (red) - only top party secretaries
        if "市委" in title or "党委" in title:
            return "255,50,50"
    if "市长" in title or "副县长" in title or "区长" in title or "县长" in title:
        return "50,100,255"  # Blue for government heads
    if "纪委" in title:
        return "255,165,0"   # Orange for discipline
    return "100,100,100"     # Grey for others

def is_top_leader(p):
    title = p.get("current_post", "")
    return "书记" in title and "纪委" not in title and "市委" in title

def org_color(o):
    otype = o.get("type", "")
    if "党委" in otype:
        return "255,200,200"
    if "政府" in otype:
        return "200,200,255"
    if "政协" in otype:
        return "255,240,200"
    return "200,200,200"

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>池州市领导班子关系网络 - Chizhou City Leadership Network (2026-07-15)</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: Persons
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        role = esc(p.get("current_post", ""))
        org = esc(p.get("current_org", ""))
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{role}"/>')
        lines.append(f'          <attvalue for="2" value="{org}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: Organizations
    for o in organizations:
        oid = o["id"]
        oc = org_color(o)
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> Organization (worked_at)
    for pos in positions:
        eid += 1
        notes = esc(pos.get("note", ""))
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" '
                     f'label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{notes}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person (relationship)
    for r in relationships:
        eid += 1
        ctx = esc(r.get("context", ""))
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" '
                     f'label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{ctx}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {GEXF_PATH}")


# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    build_database()
    build_gexf()
    print("Done.")
