#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 闽侯县 leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/闽侯县_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/闽侯县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current and Recent Minhou County Party Secretaries ──
    {"id": 1, "name": "吴永忠", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共闽侯县委书记", "current_org": "中共闽侯县委员会",
     "source": "https://www.minhou.gov.cn/xjwz/zwgk/gzdt/zwdt/202607/t20260709_5344666.htm"},
    {"id": 2, "name": "赵学峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "福州市人民政府副市长", "current_org": "福州市人民政府",
     "source": "https://baike.baidu.com/item/%E8%B5%B5%E5%AD%A6%E5%B3%B0"},
    {"id": 3, "name": "叶仁佑", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共福州市台江区委书记", "current_org": "中共福州市台江区委员会",
     "source": "https://baike.baidu.com/item/%E5%8F%B6%E4%BB%81%E4%BD%91"},

    # ── Current Minhou County Government Leaders ──
    {"id": 4, "name": "陈志毅", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "闽侯县人民政府县长", "current_org": "闽侯县人民政府",
     "source": "https://www.minhou.gov.cn/xjwz/zwgk/gzdt/zwdt/202607/t20260709_5344666.htm"},
    {"id": 5, "name": "王建生", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "闽侯县人民政府原县长", "current_org": "闽侯县人民政府",
     "source": "https://baike.baidu.com/item/%E7%8E%8B%E5%BB%BA%E7%94%9F"},
    {"id": 6, "name": "林颖", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "闽侯县人民政府原县长", "current_org": "闽侯县人民政府",
     "source": "https://baike.baidu.com/item/%E6%9E%97%E9%A2%96"},

    # ── Other County Leaders from official news ──
    {"id": 7, "name": "谢浩", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "闽侯县委常委、副县长", "current_org": "闽侯县人民政府",
     "source": "https://www.minhou.gov.cn/xjwz/zwgk/gzdt/zwdt/202607/t20260709_5344666.htm"},
    {"id": 8, "name": "王海峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "闽侯县副县长", "current_org": "闽侯县人民政府",
     "source": "https://www.minhou.gov.cn/xjwz/zwgk/gzdt/zwdt/202607/t20260709_5344666.htm"},
    {"id": 9, "name": "吕立邦", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "福州地区大学新校区管委会领导", "current_org": "福州地区大学新校区管委会",
     "source": "https://www.minhou.gov.cn/xjwz/zwgk/gzdt/zwdt/202607/t20260709_5344666.htm"},
    {"id": 10, "name": "林祥飞", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "福州地区大学新校区管委会领导", "current_org": "福州地区大学新校区管委会",
     "source": "https://www.minhou.gov.cn/xjwz/zwgk/gzdt/zwdt/202607/t20260709_5344666.htm"},
]

organizations = [
    {"id": 1, "name": "中共闽侯县委员会", "type": "党委", "level": "县处级", "parent": "中共福州市委员会", "location": "福建福州闽侯"},
    {"id": 2, "name": "闽侯县人民政府", "type": "政府", "level": "县处级", "parent": "福州市人民政府", "location": "福建福州闽侯"},
    {"id": 3, "name": "福州市人民政府", "type": "政府", "level": "副省级", "parent": "福建省人民政府", "location": "福建福州"},
    {"id": 4, "name": "福州地区大学新校区管委会", "type": "事业单位", "level": "县处级", "parent": "福州市人民政府", "location": "福建福州闽侯"},
    {"id": 5, "name": "中共福州市台江区委员会", "type": "党委", "level": "县处级", "parent": "中共福州市委员会", "location": "福建福州台江"},
]

positions = [
    # ── Wu Yongzhong (吴永忠) career ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共闽侯县委书记", "start": "", "end": "", "rank": "县处级正职", "note": "现任(2026年7月在任)"},

    # ── Zhao Xuefeng (赵学峰) career ──
    {"id": 2, "person_id": 2, "org_id": 1, "title": "中共闽侯县委书记", "start": "2016", "end": "2020", "rank": "县处级正职", "note": ""},
    {"id": 3, "person_id": 2, "org_id": 3, "title": "福州市人民政府副市长", "start": "2020", "end": "", "rank": "副厅级", "note": ""},

    # ── Ye Renyou (叶仁佑) career ──
    {"id": 4, "person_id": 3, "org_id": 1, "title": "中共闽侯县委书记", "start": "2021", "end": "", "rank": "县处级正职", "note": ""},
    {"id": 5, "person_id": 3, "org_id": 5, "title": "中共福州市台江区委书记", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},

    # ── Chen Zhiyi (陈志毅) career ──
    {"id": 6, "person_id": 4, "org_id": 2, "title": "闽侯县人民政府县长", "start": "", "end": "", "rank": "县处级正职", "note": "现任(2026年7月在任)"},

    # ── Wang Jiansheng (王建生) career ──
    {"id": 7, "person_id": 5, "org_id": 2, "title": "闽侯县人民政府县长", "start": "2016", "end": "2020", "rank": "县处级正职", "note": ""},

    # ── Lin Ying (林颖) career ──
    {"id": 8, "person_id": 6, "org_id": 2, "title": "闽侯县人民政府县长", "start": "2013", "end": "2016", "rank": "县处级正职", "note": ""},

    # ── Xie Hao (谢浩) career ──
    {"id": 9, "person_id": 7, "org_id": 2, "title": "闽侯县委常委、副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Wang Haifeng (王海峰) career ──
    {"id": 10, "person_id": 8, "org_id": 2, "title": "闽侯县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Lv Libang (吕立邦) career ──
    {"id": 11, "person_id": 9, "org_id": 4, "title": "福州地区大学新校区管委会领导", "start": "", "end": "", "rank": "县处级", "note": ""},

    # ── Lin Xiangfei (林祥飞) career ──
    {"id": 12, "person_id": 10, "org_id": 4, "title": "福州地区大学新校区管委会领导", "start": "", "end": "", "rank": "县处级", "note": ""},
]

relationships = [
    # ── Predecessor-Successor (县委书记) ──
    {"id": 1, "person_a_id": 2, "person_b_id": 1, "type": "交接", "context": "赵学峰→吴永忠 闽侯县委书记交接", "overlap_org": "中共闽侯县委员会", "overlap_period": ""},
    {"id": 2, "person_a_id": 3, "person_b_id": 2, "type": "交接", "context": "叶仁佑→赵学峰 闽侯县委书记交接（或前后任）", "overlap_org": "中共闽侯县委员会", "overlap_period": ""},

    # ── Predecessor-Successor (县长) ──
    {"id": 3, "person_a_id": 5, "person_b_id": 4, "type": "交接", "context": "王建生→陈志毅 闽侯县长交接", "overlap_org": "闽侯县人民政府", "overlap_period": ""},
    {"id": 4, "person_a_id": 6, "person_b_id": 5, "type": "交接", "context": "林颖→王建生 闽侯县长交接", "overlap_org": "闽侯县人民政府", "overlap_period": ""},

    # ── Current Coworkers ──
    {"id": 5, "person_a_id": 1, "person_b_id": 4, "type": "党政搭档", "context": "吴永忠（县委书记）与陈志毅（县长）为当前党政搭档", "overlap_org": "中共闽侯县委员会", "overlap_period": "2026"},
    {"id": 6, "person_a_id": 1, "person_b_id": 7, "type": "同僚", "context": "吴永忠与谢浩同为闽侯县领导", "overlap_org": "中共闽侯县委员会", "overlap_period": "2026"},
    {"id": 7, "person_a_id": 4, "person_b_id": 7, "type": "同僚", "context": "陈志毅与谢浩分别在县政府和县委任职", "overlap_org": "闽侯县人民政府", "overlap_period": "2026"},
    {"id": 8, "person_a_id": 4, "person_b_id": 8, "type": "同僚", "context": "陈志毅与王海峰同为闽侯县政府领导", "overlap_org": "闽侯县人民政府", "overlap_period": "2026"},
    {"id": 9, "person_a_id": 1, "person_b_id": 9, "type": "同僚", "context": "吴永忠与吕立邦在闽侯工作存在交集（大学城事务）", "overlap_org": "福州地区大学新校区管委会", "overlap_period": "2026"},
    {"id": 10, "person_a_id": 1, "person_b_id": 10, "type": "同僚", "context": "吴永忠与林祥飞在闽侯工作存在交集（大学城事务）", "overlap_org": "福州地区大学新校区管委会", "overlap_period": "2026"},
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
lines.append(f'    <description>闽侯县领导班子工作关系网络 - {today}</description>')
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
    if p["id"] in [1, 2, 3]:
        color = '#E03C31'  # red: Party Secretary
        size = 20.0
    elif p["id"] in [4, 5, 6]:
        color = '#2980B9'  # blue: government leader (county mayor)
        size = 18.0
    else:
        color = '#95A5A6'  # grey: others
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
    lines.append(f'        <viz:color r="{int(color[1:3], 16)}" g="{int(color[3:5], 16)}" b="{int(color[5:7], 16)}"/>')
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

if __name__ == "__main__":
    print("Build script executed directly.")
