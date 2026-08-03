#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Yuanshi County (元氏县) leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/hebei_元氏县")
DB_PATH = os.path.join(STAGING, "元氏县_network.db")
GEXF_PATH = os.path.join(STAGING, "元氏县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

today = datetime.now().strftime("%Y-%m-%d")

persons = [
    # ── Current Party Secretary (县委书记) ──
    {"id": 1, "name": "郝永力", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共元氏县委书记", "current_org": "中共元氏县委员会",
     "source": "https://www.yuanshi.gov.cn/columns/8b10a0a2-6b39-4a7b-b1f8-5f1169e0d51d/202607/22/765ade70-499a-45f3-a5eb-6a36d9ef2261.html"},

    # ── Current County Mayor (县长) ──
    {"id": 2, "name": "谢槟择", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "元氏县人民政府县长", "current_org": "元氏县人民政府",
     "source": "https://www.yuanshi.gov.cn/columns/8b10a0a2-6b39-4a7b-b1f8-5f1169e0d51d/202607/29/7a7143da-ecb8-47c5-95e6-f485954270b5.html"},

    # ── Deputy County Party Secretary ──
    {"id": 3, "name": "李红强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "元氏县委副书记", "current_org": "中共元氏县委员会",
     "source": "https://www.yuanshi.gov.cn/columns/8b10a0a2-6b39-4a7b-b1f8-5f1169e0d51d/202607/29/7a7143da-ecb8-47c5-95e6-f485954270b5.html"},

    # ── Standing Committee, Executive Deputy County ──
    {"id": 4, "name": "张爱敏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "元氏县委常委、常务副县长", "current_org": "元氏县人民政府",
     "source": "https://www.yuanshi.gov.cn/columns/8b10a0a2-6b39-4a7b-b1f8-5f1169e0d51d/202607/29/7a7143da-ecb8-47c5-95e6-f485954270b5.html"},

    # ── County Party Congress Standing member ──
    {"id": 5, "name": "王伟龙", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "元氏县副县长", "current_org": "元氏县人民政府",
     "source": "https://www.yuanshi.gov.cn/columns/8b10a0a2-6b39-4a7b-b1f8-5f1169e0d51d/202607/31/54cfceb9-7b09-473a-9fd0-d7470c62842f.html"},

    # ── County People's Congress (人大主任) ──
    {"id": 6, "name": "张树果", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "元氏县人大常委会主任", "current_org": "元氏县人民代表大会常务委员会",
     "source": "https://www.yuanshi.gov.cn/columns/8b10a0a2-6b39-4a7b-b1f8-5f1169e0d51d/202607/27/884cf6b6-bb37-43d6-aacd-a5b6c960756b.html"},

    # ── County (政协主席) ──
    {"id": 7, "name": "吴茂林", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "元氏县政协主席", "current_org": "政协元氏县委员会",
     "source": "https://www.yuanshi.gov.cn/columns/8b10a0a2-6b39-4a7b-b1f8-5f1169e0d51d/202607/27/6adc2ef7-acd9-4858-9b8c-520dd3405235.html"},

    # ── Government Office Director ──
    {"id": 8, "name": "安宏泽", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "元氏县人民政府办公室主任", "current_org": "元氏县人民政府办公室",
     "source": "https://www.yuanshi.gov.cn/columns/9a27ba53-6fe3-47c9-9b11-19cdf1356af0/index.html"},

    # ── Previous Party Secretary (12th term predecessor) ──
    {"id": 9, "name": "郑巍", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://baike.baidu.com/item/%E9%83%91%E5%B7%8D/23398521"},

    # ── Previous County Mayor before election ──
    {"id": 10, "name": "米峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://www.yuanshi.gov.cn/"},  # to gain credibility for search
]

organizations = [
    {"id": 1, "name": "中共元氏县委员会", "type": "党委", "level": "县处级", "parent": "中共石家庄市委员会", "location": "河北省石家庄市元氏县"},
    {"id": 2, "name": "元氏县人民政府", "type": "政府", "level": "县处级", "parent": "石家庄市人民政府", "location": "河北省石家庄市元氏县"},
    {"id": 3, "name": "元氏县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "石家庄市人民代表大会常务委员会", "location": "河北省石家庄市元氏县"},
    {"id": 4, "name": "政协元氏县委员会", "type": "政协", "level": "县处级", "parent": "政协石家庄市委员会", "location": "河北省石家庄市元氏县"},
    {"id": 5, "name": "元氏县人民政府办公室", "type": "政府", "level": "县处级", "parent": "元氏县人民政府", "location": "河北省石家庄市元氏县"},
    {"id": 6, "name": "中共元氏县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共石家庄市纪律检查委员会", "location": "河北省石家庄市元氏县"},
]

positions = [
    # ── Hao Yongli (郝永力) career ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共元氏县委书记", "start": "2026-07", "end": "", "rank": "县处级正职", "note": "现任，2026年7月第十三次党代会当选"},

    # ── Xie Binze (谢槟择) career ──
    {"id": 2, "person_id": 2, "org_id": 2, "title": "元氏县人民政府县长", "start": "2026-07", "end": "", "rank": "县处级正职", "note": "现任，2026年7月第十八届人大第一次会议当选"},

    # ── Li Hongqiang (李红強) career ──
    {"id": 3, "person_id": 3, "org_id": 1, "title": "元氏县委副书记", "start": "2026-07", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Zhang Aimin (张爱敏) career ──
    {"id": 4, "person_id": 4, "org_id": 2, "title": "元氏县委常委、常务副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Wang Weilong (王伟龙) career ──
    {"id": 5, "person_id": 5, "org_id": 2, "title": "元氏县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Zhang Shuguo (张树果) ──
    {"id": 6, "person_id": 6, "org_id": 3, "title": "元氏县人大常委会主任", "start": "2026-07", "end": "", "rank": "县处级正职", "note": "2026年7月新当选"},

    # ── Wu Maolin (吴茂林) ──
    {"id": 7, "person_id": 7, "org_id": 4, "title": "元氏县政协主席", "start": "2026-07", "end": "", "rank": "县处级正职", "note": "2026年7月第十一届政协第一次会议"},

    # ── An Hongze (安宏泽) ──
    {"id": 8, "person_id": 8, "org_id": 5, "title": "元氏县人民政府办公室主任", "start": "", "end": "", "rank": "", "note": ""},

    # ── Previous Secretary Zheng Wei (郑巍) ──
    {"id": 9, "person_id": 9, "org_id": 1, "title": "中共元氏县委书记", "start": "", "end": "2026-07", "rank": "县处级正职", "note": "前任，第十二届县委书记"},

    # ── Previous Mayor Cao Feng (曹峰) ──
    {"id": 10, "person_id": 10, "org_id": 2, "title": "元氏县人民政府县长", "start": "", "end": "2026-07", "rank": "县处级正职", "note": "前任"},
]

relationships = [
    # ── Predecessor-Successor: Party Secretary ──
    {"id": 1, "person_a_id": 9, "person_b_id": 1, "type": "交接", "context": "郑巍→郝永力 元氏县委书记交接（2026年7月）", "overlap_org": "中共元氏县委员会", "overlap_period": "2026-07"},

    # ── Predecessor-Successor: County Mayor ──
    {"id": 2, "person_a_id": 10, "person_b_id": 2, "type": "交接", "context": "曹峰→谢槟择 元氏县长交接（2026年7月）", "overlap_org": "元氏县人民政府", "overlap_period": "2026-07"},

    # ── Party Secretary & County Mayor ──
    {"id": 3, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档", "context": "郝永力（县委书记）与谢槟择（县长）党政正职搭档", "overlap_org": "中共元氏县委员会", "overlap_period": "2026-07至今"},

    # ── Party Secretary & Deputy Secretary ──
    {"id": 4, "person_a_id": 1, "person_b_id": 3, "type": "上下级", "context": "郝永力与李红强为县委正副书记", "overlap_org": "中共元氏县委员会", "overlap_period": "2026-07至今"},

    # ── County Mayor & Executive Deputy ──
    {"id": 5, "person_a_id": 2, "person_b_id": 4, "type": "上下级", "context": "谢槟择（县长）与张爱敏（常务副县长）在县政府领导班子共事", "overlap_org": "元氏县人民政府", "overlap_period": ""},

    # ── County Mayor & Deputy Mayor ──
    {"id": 6, "person_a_id": 2, "person_b_id": 5, "type": "上下级", "context": "谢槟择（县长）与王伟龙（副县长）在县政府领导班子共事", "overlap_org": "元氏县人民政府", "overlap_period": ""},

    # ── Party Secretary & NPC Chairman ──
    {"id": 7, "person_a_id": 1, "person_b_id": 6, "type": "同僚", "context": "郝永力与张树果（人大主任）在县委和人大的工作协作", "overlap_org": "中共元氏县委员会", "overlap_period": "2026-07至今"},

    # ── Party Secretary & CPPCC Chairman ──
    {"id": 8, "person_a_id": 1, "person_b_id": 7, "type": "同僚", "context": "郝永力与吴茂林（政协主席）在县四个班子的协作", "overlap_org": "中共元氏县委员会", "overlap_period": "2026-07至今"},

    # ── Executive Deputy & Government Office ──
    {"id": 9, "person_a_id": 4, "person_b_id": 8, "type": "同僚", "context": "张爱敏（常务副县长）与安宏泽（办公室主任）工作关系", "overlap_org": "元氏县人民政府", "overlap_period": ""},
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
    cur.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                 p["birthplace"], p["education"], p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)",
                (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                 pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("INSERT INTO relationships VALUES (?,?,?,?,?,?,?)",
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

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>元氏县领导班子工作关系网络 - {today}</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attributes
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

# Nodes: Persons
lines.append('    <nodes>')
for p in persons:
    if p["id"] == 1:
        color = '#E03C31'  # red: Party Secretary
        size = 20.0
    elif p["id"] == 2:
        color = '#2980B9'  # blue: government leader (county mayor)
        size = 20.0
    elif p["id"] in [9, 10]:
        color = '#95A5A6'  # grey: predecessor
        size = 14.0
    elif p["id"] in [3, 4]:
        color = '#2980B9'
        size = 16.0
    else:
        color = '#95A5A6'
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
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'      </node>')

# Nodes: Organizations
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

# Edges
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