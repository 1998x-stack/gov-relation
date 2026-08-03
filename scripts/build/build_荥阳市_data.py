#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Xingyang City (荥阳市) leadership network."""

import sqlite3
import os
from datetime import datetime

STAGING_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(STAGING_DIR, "荥阳市_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "荥阳市_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Party Secretary ──
    {"id": 1, "name": "石玉", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共荥阳市委书记", "current_org": "中共荥阳市委员会",
     "source": "https://www.xingyang.gov.cn/xyxw/10172256.jhtml"},

    # ── Current Mayor ──
    {"id": 2, "name": "李明刚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "荥阳市人民政府市长", "current_org": "荥阳市人民政府",
     "source": "https://www.xingyang.gov.cn/xyxw/10077448.jhtml"},

    # ── Other Standing Committee Members ──
    {"id": 3, "name": "刘成伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "荥阳市委常委", "current_org": "中共荥阳市委员会",
     "source": "https://www.xingyang.gov.cn/xyxw/10172256.jhtml"},

    {"id": 4, "name": "赵晨阳", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "荥阳市委常委", "current_org": "中共荥阳市委员会",
     "source": "https://www.xingyang.gov.cn/xyxw/10172256.jhtml"},

    {"id": 5, "name": "王珂", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "荥阳市委常委", "current_org": "中共荥阳市委员会",
     "source": "https://www.xingyang.gov.cn/xyxw/10172256.jhtml"},

    {"id": 6, "name": "刘小波", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "荥阳市委常委", "current_org": "中共荥阳市委员会",
     "source": "https://www.xingyang.gov.cn/xyxw/10172256.jhtml"},

    {"id": 7, "name": "杜磊磊", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "荥阳市委常委", "current_org": "中共荥阳市委员会",
     "source": "https://www.xingyang.gov.cn/xyxw/10172256.jhtml"},

    {"id": 8, "name": "王幸", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "荥阳市委常委", "current_org": "中共荥阳市委员会",
     "source": "https://www.xingyang.gov.cn/xyxw/10172256.jhtml"},

    {"id": 9, "name": "韩玮", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "荥阳市委常委", "current_org": "中共荥阳市委员会",
     "source": "https://www.xingyang.gov.cn/xyxw/10172256.jhtml"},

    {"id": 10, "name": "陈洁", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "荥阳市委常委", "current_org": "中共荥阳市委员会",
     "source": "https://www.xingyang.gov.cn/xyxw/10172256.jhtml"},

    {"id": 11, "name": "吴菲", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "荥阳市委常委", "current_org": "中共荥阳市委员会",
     "source": "https://www.xingyang.gov.cn/xyxw/10172256.jhtml"},

    {"id": 12, "name": "李政", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "荥阳市委常委", "current_org": "中共荥阳市委员会",
     "source": "https://www.xingyang.gov.cn/xyxw/10172256.jhtml"},

    {"id": 13, "name": "张荣耀", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "荥阳市领导", "current_org": "荥阳市人民政府",
     "source": "https://www.xingyang.gov.cn/xyxw/10182602.jhtml"},

    # ── People's Congress Leaders ──
    {"id": 14, "name": "景秀香", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "荥阳市人大常委会主任", "current_org": "荥阳市人民代表大会常务委员会",
     "source": "https://www.xingyang.gov.cn/xyxw/10077448.jhtml"},

    {"id": 15, "name": "曹可艳", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "荥阳市人大常委会副主任", "current_org": "荥阳市人民代表大会常务委员会",
     "source": "https://www.xingyang.gov.cn/xyxw/10077448.jhtml"},

    {"id": 16, "name": "李定清", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "荥阳市人大常委会副主任", "current_org": "荥阳市人民代表大会常务委员会",
     "source": "https://www.xingyang.gov.cn/xyxw/10077448.jhtml"},

    {"id": 17, "name": "周红武", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "荥阳市人大常委会副主任", "current_org": "荥阳市人民代表大会常务委员会",
     "source": "https://www.xingyang.gov.cn/xyxw/10077448.jhtml"},

    {"id": 18, "name": "靳西峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "荥阳市人大常委会副主任", "current_org": "荥阳市人民代表大会常务委员会",
     "source": "https://www.xingyang.gov.cn/xyxw/10077448.jhtml"},

    {"id": 19, "name": "陈秀珍", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "荥阳市人大常委会副主任", "current_org": "荥阳市人民代表大会常务委员会",
     "source": "https://www.xingyang.gov.cn/xyxw/10077448.jhtml"},

    {"id": 20, "name": "司红辉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "荥阳市人大常委会副主任", "current_org": "荥阳市人民代表大会常务委员会",
     "source": "https://www.xingyang.gov.cn/xyxw/10077448.jhtml"},
]

organizations = [
    {"id": 1, "name": "中共荥阳市委员会", "type": "党委", "level": "县处级", "parent": "中共郑州市委员会", "location": "河南郑州荥阳"},
    {"id": 2, "name": "荥阳市人民政府", "type": "政府", "level": "县处级", "parent": "郑州市人民政府", "location": "河南郑州荥阳"},
    {"id": 3, "name": "荥阳市人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "", "location": "河南郑州荥阳"},
]

positions = [
    # ── Shi Yu (石玉) ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共荥阳市委书记", "start": "", "end": "", "rank": "县处级正职", "note": "现任，截至2026年7月"},

    # ── Li Minggang (李明刚) ──
    {"id": 2, "person_id": 2, "org_id": 2, "title": "荥阳市人民政府市长", "start": "2026-05", "end": "", "rank": "县处级正职", "note": "2026年5月31日当选"},

    # ── Standing Committee ──
    {"id": 3, "person_id": 3, "org_id": 1, "title": "荥阳市委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 4, "person_id": 4, "org_id": 1, "title": "荥阳市委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 5, "person_id": 5, "org_id": 1, "title": "荥阳市委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 6, "person_id": 6, "org_id": 1, "title": "荥阳市委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 7, "person_id": 7, "org_id": 1, "title": "荥阳市委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 8, "person_id": 8, "org_id": 1, "title": "荥阳市委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 9, "person_id": 9, "org_id": 1, "title": "荥阳市委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 10, "person_id": 10, "org_id": 1, "title": "荥阳市委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 11, "person_id": 11, "org_id": 1, "title": "荥阳市委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 12, "person_id": 12, "org_id": 1, "title": "荥阳市委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Government Leaders ──
    {"id": 13, "person_id": 13, "org_id": 2, "title": "荥阳市领导（副市长/党组成员）", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── People's Congress ──
    {"id": 14, "person_id": 14, "org_id": 3, "title": "荥阳市人大常委会主任", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},
    {"id": 15, "person_id": 15, "org_id": 3, "title": "荥阳市人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 16, "person_id": 16, "org_id": 3, "title": "荥阳市人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 17, "person_id": 17, "org_id": 3, "title": "荥阳市人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 18, "person_id": 18, "org_id": 3, "title": "荥阳市人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 19, "person_id": 19, "org_id": 3, "title": "荥阳市人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 20, "person_id": 20, "org_id": 3, "title": "荥阳市人大常委会副主任", "start": "2026", "end": "", "rank": "县处级副职", "note": "2026年5月当选"},
]

relationships = [
    # ── Party Secretary ↔ Mayor ──
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档", "context": "石玉任市委书记，李明刚任市长", "overlap_org": "中共荥阳市委员会/荥阳市人民政府", "overlap_period": "2026-05至今"},

    # ── Party Secretary ↔ Congress Chair ──
    {"id": 2, "person_a_id": 1, "person_b_id": 14, "type": "同僚", "context": "石玉与景秀香为市委、人大搭档", "overlap_org": "荥阳市人大常委会", "overlap_period": ""},

    # ── Standing Committee Common Tie ──
    {"id": 3, "person_a_id": 3, "person_b_id": 4, "type": "同僚", "context": "刘成伟与赵晨阳均为荥阳市委常委", "overlap_org": "中共荥阳市委员会", "overlap_period": ""},
    {"id": 4, "person_a_id": 5, "person_b_id": 6, "type": "同僚", "context": "王珂与刘小波均为荥阳市委常委", "overlap_org": "中共荥阳市委员会", "overlap_period": ""},
    {"id": 5, "person_a_id": 7, "person_b_id": 8, "type": "同僚", "context": "杜磊磊与王幸均为荥阳市委常委", "overlap_org": "中共荥阳市委员会", "overlap_period": ""},
    {"id": 6, "person_a_id": 9, "person_b_id": 10, "type": "同僚", "context": "韩玮与陈洁均为荥阳市委常委", "overlap_org": "中共荥阳市委员会", "overlap_period": ""},
    {"id": 7, "person_a_id": 11, "person_b_id": 12, "type": "同僚", "context": "吴菲与李政均为荥阳市委常委", "overlap_org": "中共荥阳市委员会", "overlap_period": ""},

    # ── Congress Internal ──
    {"id": 8, "person_a_id": 14, "person_b_id": 15, "type": "同僚", "context": "景秀香与曹可艳均为人大常委会领导", "overlap_org": "荥阳市人民代表大会常务委员会", "overlap_period": ""},
    {"id": 9, "person_a_id": 16, "person_b_id": 17, "type": "同僚", "context": "李定清与周红武均为人大常委会副主任", "overlap_org": "荥阳市人民代表大会常务委员会", "overlap_period": ""},
    {"id": 10, "person_a_id": 18, "person_b_id": 19, "type": "同僚", "context": "靳西峰与陈秀珍均为人大常委会副主任", "overlap_org": "荥阳市人民代表大会常务委员会", "overlap_period": ""},
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
lines.append(f'    <description>荥阳市领导班子工作关系网络 - {today}</description>')
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
    if p["id"] == 1:
        color = '#E03C31'  # red: Party Secretary
        size = 20.0
    elif p["id"] == 2:
        color = '#2980B9'  # blue: government leader
        size = 18.0
    elif p["id"] == 14:
        color = '#C9A94E'  # gold: congress leader
        size = 16.0
    else:
        color = '#95A5A6'  # grey: others
        size = 12.0

    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
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