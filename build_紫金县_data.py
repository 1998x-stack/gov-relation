#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 紫金县 leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/紫金县_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/紫金县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current County Party Secretary ──
    {"id": 1, "name": "黄春彭", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共紫金县委书记", "current_org": "中共紫金县委员会",
     "source": "http://www.zijin.gov.cn/xw/zwdt/content/post_707458.html"},

    # ── Current County Mayor ──
    {"id": 2, "name": "林仕玮", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-10", "birthplace": "", "education": "大学/历史学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共紫金县委副书记、县政府党组书记、县长", "current_org": "紫金县人民政府",
     "source": "http://www.zijin.gov.cn/zw/ldzc/xzfld/content/post_614350.html"},

    # ── County Standing Committee / Deputy County Heads ──
    {"id": 3, "name": "肖奇聪", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-09", "birthplace": "", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、县政府党组成员、副县长", "current_org": "紫金县人民政府",
     "source": "http://www.zijin.gov.cn/zw/ldzc/xzfld/content/post_614348.html"},

    {"id": 4, "name": "黄少波", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-03", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、宣传部部长", "current_org": "中共紫金县委员会",
     "source": "http://www.zijin.gov.cn/zw/ldzc/xzfld/content/post_614349.html"},

    {"id": 5, "name": "徐敏", "gender": "女", "ethnicity": "汉族",
     "birth": "1982-01", "birthplace": "", "education": "在职研究生/农业推广硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、统战部部长，县政协党组副书记", "current_org": "中共紫金县委员会",
     "source": "http://www.zijin.gov.cn/zw/ldzc/xzfld/content/post_614347.html"},

    {"id": 6, "name": "陈燮军", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-08", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政府党组成员、副县长、县公安局局长", "current_org": "紫金县人民政府",
     "source": "http://www.zijin.gov.cn/zw/ldzc/xzfld/content/post_614346.html"},

    {"id": 7, "name": "谢运畅", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-12", "birthplace": "", "education": "在职研究生",
     "party_join": "中国民主促进会", "work_start": "",
     "current_post": "县政府副县长", "current_org": "紫金县人民政府",
     "source": "http://www.zijin.gov.cn/zw/ldzc/xzfld/content/post_614345.html"},

    {"id": 8, "name": "周丽娴", "gender": "女", "ethnicity": "汉族",
     "birth": "1983-12", "birthplace": "", "education": "大学/文学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政府党组成员、副县长", "current_org": "紫金县人民政府",
     "source": "http://www.zijin.gov.cn/zw/ldzc/xzfld/content/post_614343.html"},

    {"id": 9, "name": "吴荣辉", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-11", "birthplace": "", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政府党组成员、副县长", "current_org": "紫金县人民政府",
     "source": "http://www.zijin.gov.cn/zw/ldzc/xzfld/content/post_614342.html"},

    {"id": 10, "name": "戴志尚", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-09", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政府党组成员、副县长", "current_org": "紫金县人民政府",
     "source": "http://www.zijin.gov.cn/zw/ldzc/xzfld/content/post_614344.html"},
]

organizations = [
    {"id": 1, "name": "中共紫金县委员会", "type": "党委", "level": "县处级", "parent": "中共河源市委员会", "location": "广东河源紫金"},
    {"id": 2, "name": "紫金县人民政府", "type": "政府", "level": "县处级", "parent": "河源市人民政府", "location": "广东河源紫金"},
    {"id": 3, "name": "紫金县公安局", "type": "政府", "level": "县处级", "parent": "紫金县人民政府/河源市公安局", "location": "广东河源紫金"},
    {"id": 4, "name": "紫金县政协", "type": "政协", "level": "县处级", "parent": "政协河源市委员会", "location": "广东河源紫金"},
]

positions = [
    # ── Huang Chunpeng (黄春彭) career ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共紫金县委书记", "start": "", "end": "", "rank": "县处级正职", "note": "现任, 上任时间待查"},

    # ── Lin Shiwei (林仕玮) career ──
    {"id": 2, "person_id": 2, "org_id": 1, "title": "中共紫金县委副书记", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 3, "person_id": 2, "org_id": 2, "title": "紫金县人民政府党组书记、县长", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},

    # ── Xiao Qicong (肖奇聪) ──
    {"id": 4, "person_id": 3, "org_id": 1, "title": "紫金县委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 5, "person_id": 3, "org_id": 2, "title": "紫金县政府党组成员、副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Huang Shaobo (黄少波) ──
    {"id": 6, "person_id": 4, "org_id": 1, "title": "紫金县委常委、宣传部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Xu Min (徐敏) ──
    {"id": 7, "person_id": 5, "org_id": 1, "title": "紫金县委常委、统战部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 8, "person_id": 5, "org_id": 4, "title": "紫金县政协党组副书记", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Chen Xiejun (陈燮军) ──
    {"id": 9, "person_id": 6, "org_id": 2, "title": "县政府党组成员、副县长、县公安局局长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Xie Yunchang (谢运畅) ──
    {"id": 10, "person_id": 7, "org_id": 2, "title": "紫金县人民政府副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任，民进"},

    # ── Zhou Lixian (周丽娴) ──
    {"id": 11, "person_id": 8, "org_id": 2, "title": "紫金县政府党组成员、副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Wu Ronghui (吴荣辉) ──
    {"id": 12, "person_id": 9, "org_id": 2, "title": "紫金县政府党组成员、副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Dai Zhishang (戴志尚) ──
    {"id": 13, "person_id": 10, "org_id": 2, "title": "紫金县政府党组成员、副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
]

relationships = [
    # ── Party Secretary - County Mayor (党政搭档) ──
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档", "context": "黄春彭任县委书记，林仕玮任县长，为紫金县党政正职搭档", "overlap_org": "中共紫金县委员会/紫金县人民政府", "overlap_period": "至今"},

    # ── Standing Committee coworkers ──
    {"id": 2, "person_a_id": 3, "person_b_id": 4, "type": "同僚", "context": "肖奇聪与黄少波均为紫金县委常委", "overlap_org": "中共紫金县委员会", "overlap_period": ""},
    {"id": 3, "person_a_id": 3, "person_b_id": 5, "type": "同僚", "context": "肖奇聪与徐敏均为紫金县委常委", "overlap_org": "中共紫金县委员会", "overlap_period": ""},
    {"id": 4, "person_a_id": 4, "person_b_id": 5, "type": "同僚", "context": "黄少波与徐敏均为紫金县委常委", "overlap_org": "中共紫金县委员会", "overlap_period": ""},

    # ── Government colleagues ──
    {"id": 5, "person_a_id": 6, "person_b_id": 7, "type": "同僚", "context": "陈燮军与谢运畅均为紫金县政府领导", "overlap_org": "紫金县人民政府", "overlap_period": ""},
    {"id": 6, "person_a_id": 8, "person_b_id": 9, "type": "同僚", "context": "周丽娴与吴荣辉均为紫金县政府领导", "overlap_org": "紫金县人民政府", "overlap_period": ""},
    {"id": 7, "person_a_id": 8, "person_b_id": 10, "type": "同僚", "context": "周丽娴与戴志尚均为紫金县政府领导", "overlap_org": "紫金县人民政府", "overlap_period": ""},
    {"id": 8, "person_a_id": 9, "person_b_id": 10, "type": "同僚", "context": "吴荣辉与戴志尚均为紫金县政府领导", "overlap_org": "紫金县人民政府", "overlap_period": ""},
]


# ── BUILD SQLite DATABASE ────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE persons (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
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

CREATE TABLE organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

CREATE TABLE positions (
    id INTEGER PRIMARY KEY,
    person_id INTEGER NOT NULL,
    org_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE relationships (
    id INTEGER PRIMARY KEY,
    person_a_id INTEGER NOT NULL,
    person_b_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a_id) REFERENCES persons(id),
    FOREIGN KEY (person_b_id) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                 p["birthplace"], p["education"], p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)""",
                (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                 pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("""INSERT INTO relationships VALUES (?,?,?,?,?,?,?)""",
                (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
                 r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

# Summary stats
cur.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]

conn.close()
print(f"SQLite database written: {DB_PATH}")
print(f"  Persons: {person_count}")
print(f"  Organizations: {org_count}")
print(f"  Positions: {pos_count}")
print(f"  Relationships: {rel_count}")


# ── BUILD GEXF GRAPH ────────────────────────────────────────────────

today = datetime.now().strftime("%Y-%m-%d")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>紫金县领导班子工作关系网络 - {today}</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# ── Attributes ──
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="category" title="Category" type="string"/>')
lines.append('      <attribute id="birth" title="Birth" type="string"/>')
lines.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
lines.append('      <attribute id="education" title="Education" type="string"/>')
lines.append('      <attribute id="current_post" title="Current Post" type="string"/>')
lines.append('      <attribute id="source" title="Source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="context" title="Context" type="string"/>')
lines.append('      <attribute id="period" title="Period" type="string"/>')
lines.append('    </attributes>')

# ── Nodes: Persons ──
lines.append('    <nodes>')
for p in persons:
    # Color by role
    if p["id"] == 1:
        # Party Secretary — red
        r, g, b = 255, 50, 50
        size = 20.0
    elif p["id"] == 2:
        # County Mayor — blue
        r, g, b = 50, 100, 255
        size = 20.0
    elif p["id"] in [3, 4, 5]:
        # Standing Committee — orange
        r, g, b = 255, 165, 0
        size = 12.0
    else:
        # Others — grey
        r, g, b = 100, 100, 100
        size = 12.0

    lines.append(f'      <node id="{p["id"]}" label="{p["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{p["birth"]}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{p["birthplace"]}"/>')
    lines.append(f'          <attvalue for="education" value="{p["education"]}"/>')
    lines.append(f'          <attvalue for="current_post" value="{p["current_post"]}"/>')
    lines.append(f'          <attvalue for="source" value="{p["source"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'      </node>')

# ── Nodes: Organizations ──
for o in organizations:
    oid = 1000 + o["id"]
    lines.append(f'      <node id="{oid}" label="{o["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{o["type"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="44" g="62" b="80"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'      </node>')
lines.append('    </nodes>')

# ── Edges ──
lines.append('    <edges>')
edge_id = 1

# person→organization (worked_at)
for pos in positions:
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="{edge_id}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{pos["title"]}"/>')
    lines.append(f'          <attvalue for="period" value="{pos["start"] or "?"} → {pos["end"] or "今"}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

# person↔person (relationships)
for r in relationships:
    lines.append(f'      <edge id="{edge_id}" source="{r["person_a_id"]}" target="{r["person_b_id"]}" label="{r["type"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{r["type"]}"/>')
    lines.append(f'          <attvalue for="context" value="{r["context"]}"/>')
    lines.append(f'          <attvalue for="period" value="{r["overlap_period"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

total_nodes = len(persons) + len(organizations)
total_edges = len(positions) + len(relationships)
print(f"\nGEXF graph written: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} organizations = {total_nodes} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {total_edges} total")
print("\nDone!")
