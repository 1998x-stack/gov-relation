#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Ninghai County leadership network.

Note: Biographical details (birth, birthplace, education) are marked as
'待查' (to be verified) where official sources could not be reached.
See report/open_gaps.md for full gap registry.
"""

import sqlite3
import os
import sys
from datetime import datetime

# Allow import from repo root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

BASE = os.path.dirname(os.path.abspath(__file__))
# Write to staging dir
DB_PATH = os.path.join(BASE, "宁海县_network.db")
GEXF_PATH = os.path.join(BASE, "宁海县_network.gexf")

# ── DATA ──

persons = [
    # ── Current Party Secretary ──
    {"id": 1, "name": "楼鼎鼎", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁海县委书记", "current_org": "中共宁海县委员会",
     "source": "https://www.ninghai.gov.cn/col/col1229092961/art/2026/art_e1977d75166f430aa418b5957cef12b4.html"},
    # ── Current County Mayor ──
    {"id": 2, "name": "王佳毅", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁海县委副书记、县长", "current_org": "宁海县人民政府",
     "source": "https://www.ninghai.gov.cn/col/col1229092961/art/2026/art_0277a396f8e14ccd8afba8ee03a97ba2.html"},
    # ── Party Standing Committee ──
    {"id": 3, "name": "黄崭", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁海县委常委、常务副县长", "current_org": "宁海县人民政府",
     "source": "https://www.ninghai.gov.cn/col/col1229092111/index.html"},
    {"id": 4, "name": "陈立蒙", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁海县委常委、组织部部长", "current_org": "中共宁海县委组织部",
     "source": "https://www.ninghai.gov.cn/col/col1229092961/art/2026/art_0277a396f8e14ccd8afba8ee03a97ba2.html"},
    {"id": 5, "name": "郭文魁", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁海县委常委、副县长", "current_org": "宁海县人民政府",
     "source": "https://www.ninghai.gov.cn/col/col1229092961/art/2026/art_9289d30aabf04579ac0ccdda5139199f.html"},
    # ── Deputy County Mayors ──
    {"id": 6, "name": "龚慧", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁海县副县长", "current_org": "宁海县人民政府",
     "source": "https://www.ninghai.gov.cn/col/col1229092111/index.html"},
    {"id": 7, "name": "黄建福", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁海县副县长", "current_org": "宁海县人民政府",
     "source": "https://www.ninghai.gov.cn/col/col1229092111/index.html"},
    {"id": 8, "name": "张吉峰", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁海县副县长、县公安局局长", "current_org": "宁海县人民政府",
     "source": "https://www.ninghai.gov.cn/col/col1229092111/index.html"},
    {"id": 9, "name": "杨周宏", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁海县副县长", "current_org": "宁海县人民政府",
     "source": "https://www.ninghai.gov.cn/col/col1229092111/index.html"},
    {"id": 10, "name": "谭志金", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁海县副县长（挂职）", "current_org": "宁海县人民政府",
     "source": "https://www.ninghai.gov.cn/col/col1229092111/index.html"},
    {"id": 11, "name": "陈剑", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁海县副县长", "current_org": "宁海县人民政府",
     "source": "https://www.ninghai.gov.cn/col/col1229092111/index.html"},
    # ── Other Key Leaders ──
    {"id": 12, "name": "王辅橡", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁海县人大常委会主任", "current_org": "宁海县人大常委会",
     "source": "https://www.ninghai.gov.cn/col/col1229092961/art/2026/art_e1977d75166f430aa418b5957cef12b4.html"},
    {"id": 13, "name": "叶秀高", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁海县政协主席", "current_org": "宁海县政协",
     "source": "https://www.ninghai.gov.cn/col/col1229092961/art/2026/art_e1977d75166f430aa418b5957cef12b4.html"},
    {"id": 14, "name": "叶亦金", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "宁海县人大常委会副主任", "current_org": "宁海县人大常委会",
     "source": "https://www.ninghai.gov.cn/col/col1229092961/art/2026/art_5b658c99a890481aaabfcf33d2a0098f.html"},
]

organizations = [
    {"id": 1, "name": "中共宁海县委员会", "type": "党委", "level": "县处级",
     "parent": "中共宁波市委员会", "location": "浙江宁波宁海"},
    {"id": 2, "name": "宁海县人民政府", "type": "政府", "level": "县处级",
     "parent": "宁波市人民政府", "location": "浙江宁波宁海"},
    {"id": 3, "name": "中共宁海县委组织部", "type": "党委部门", "level": "县处级",
     "parent": "中共宁海县委员会", "location": "浙江宁波宁海"},
    {"id": 4, "name": "宁海县人大常委会", "type": "人大", "level": "县处级",
     "parent": "", "location": "浙江宁波宁海"},
    {"id": 5, "name": "宁海县政协", "type": "政协", "level": "县处级",
     "parent": "", "location": "浙江宁波宁海"},
]

positions = [
    # ── Lou Dingding (楼鼎鼎) ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "宁海县委书记",
     "start": "", "end": "present", "rank": "县处级正职",
     "note": "现任，确认于2026年5月19日主持开游节"},
    # ── Wang Jiayi (王佳毅) ──
    {"id": 2, "person_id": 2, "org_id": 1, "title": "宁海县委副书记",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},
    {"id": 3, "person_id": 2, "org_id": 2, "title": "宁海县人民政府县长",
     "start": "", "end": "present", "rank": "县处级正职",
     "note": "确认于2026年7月24日以县长身份活动"},
    # ── Huang Zhan (黄崭) ──
    {"id": 4, "person_id": 3, "org_id": 1, "title": "宁海县委常委",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},
    {"id": 5, "person_id": 3, "org_id": 2, "title": "宁海县常务副县长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "分管发改、应急、统计、国资等"},
    # ── Chen Limeng (陈立蒙) ──
    {"id": 6, "person_id": 4, "org_id": 1, "title": "宁海县委常委、组织部部长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},
    {"id": 7, "person_id": 4, "org_id": 3, "title": "县委组织部部长（兼任）",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},
    # ── Guo Wenkui (郭文魁) ──
    {"id": 8, "person_id": 5, "org_id": 1, "title": "宁海县委常委",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},
    {"id": 9, "person_id": 5, "org_id": 2, "title": "宁海县副县长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "分管教育、民政、卫健、医保、金融等"},
    # ── Gong Hui (龚慧) ──
    {"id": 10, "person_id": 6, "org_id": 2, "title": "宁海县副县长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "分管经信、科技、招商等"},
    # ── Huang Jianfu (黄建福) ──
    {"id": 11, "person_id": 7, "org_id": 2, "title": "宁海县副县长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "分管自然资源、住建、交通等"},
    # ── Zhang Jifeng (张吉峰) ──
    {"id": 12, "person_id": 8, "org_id": 2, "title": "宁海县副县长、县公安局局长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "分管公安、交通安全等"},
    # ── Yang Zhouhong (杨周宏) ──
    {"id": 13, "person_id": 9, "org_id": 2, "title": "宁海县副县长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "分管水利、农业、退役军人事务等"},
    # ── Tan Zhijin (谭志金) ──
    {"id": 14, "person_id": 10, "org_id": 2, "title": "宁海县副县长（挂职）",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "分管法治政府、司法行政"},
    # ── Chen Jian (陈剑) ──
    {"id": 15, "person_id": 11, "org_id": 2, "title": "宁海县副县长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "分管商务、旅游、体育等"},
    # ── Wang Fuxiang (王辅橡) ──
    {"id": 16, "person_id": 12, "org_id": 4, "title": "宁海县人大常委会主任",
     "start": "", "end": "present", "rank": "县处级正职",
     "note": ""},
    # ── Ye Xiugao (叶秀高) ──
    {"id": 17, "person_id": 13, "org_id": 5, "title": "宁海县政协主席",
     "start": "", "end": "present", "rank": "县处级正职",
     "note": "推断为政协主席"},
    # ── Ye Yijin (叶亦金) ──
    {"id": 18, "person_id": 14, "org_id": 4, "title": "宁海县人大常委会副主任",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},
]

relationships = [
    # ── 楼鼎鼎 ↔ 王佳毅 (1-2) ──
    {"id": 1, "person_a_id": 1, "person_b_id": 2,
     "type": "superior_subordinate", "context": "县委书记与县长搭档关系",
     "overlap_org": "中共宁海县委员会", "overlap_period": "present"},
    # ── 楼鼎鼎 ↔ 黄崭 (1-3) ──
    {"id": 2, "person_a_id": 1, "person_b_id": 3,
     "type": "superior_subordinate",
     "context": "县委书记与常务副县长—县委常委班子",
     "overlap_org": "中共宁海县委员会", "overlap_period": "present"},
    # ── 楼鼎鼎 ↔ 陈立蒙 (1-4) ──
    {"id": 3, "person_a_id": 1, "person_b_id": 4,
     "type": "superior_subordinate",
     "context": "县委书记与组织部部长",
     "overlap_org": "中共宁海县委员会", "overlap_period": "present"},
    # ── 王佳毅 ↔ 黄崭 (2-3) ──
    {"id": 4, "person_a_id": 2, "person_b_id": 3,
     "type": "superior_subordinate",
     "context": "县长与常务副县长工作搭档",
     "overlap_org": "宁海县人民政府", "overlap_period": "present"},
    # ── 王佳毅 ↔ 郭文魁 (2-5) ──
    {"id": 5, "person_a_id": 2, "person_b_id": 5,
     "type": "superior_subordinate",
     "context": "县长与副县长",
     "overlap_org": "宁海县人民政府", "overlap_period": "present"},
    # ── 陈立蒙 ↔ 黄崭 (4-3) ──
    {"id": 6, "person_a_id": 4, "person_b_id": 3,
     "type": "overlap",
     "context": "同届县委常委",
     "overlap_org": "中共宁海县委员会", "overlap_period": "present"},
    # ── 王辅橡 ↔ 王佳毅 (12-2) ──
    {"id": 7, "person_a_id": 12, "person_b_id": 2,
     "type": "overlap",
     "context": "人大主任与县长在工作中的配合关系",
     "overlap_org": "宁海县", "overlap_period": "present"},
    # ── 郭文魁 ↔ 黄崭 (5-3) ──
    {"id": 8, "person_a_id": 5, "person_b_id": 3,
     "type": "overlap",
     "context": "县政府内搭档，一位分管常务，一位分管教育卫健",
     "overlap_org": "宁海县人民政府", "overlap_period": "present"},
]


# ── BUILD SQLITE DATABASE ──

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
CREATE TABLE persons (
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
)""")

cur.execute("""
CREATE TABLE organizations (
    id INTEGER PRIMARY KEY,
    name TEXT,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
)""")

cur.execute("""
CREATE TABLE positions (
    id INTEGER PRIMARY KEY,
    person_id INTEGER,
    org_id INTEGER,
    title TEXT,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
)""")

cur.execute("""
CREATE TABLE relationships (
    id INTEGER PRIMARY KEY,
    person_a_id INTEGER,
    person_b_id INTEGER,
    type TEXT,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a_id) REFERENCES persons(id),
    FOREIGN KEY (person_b_id) REFERENCES persons(id)
)""")

# Insert data
for p in persons:
    cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (p["id"], p["name"], p["gender"], p["ethnicity"],
                 p["birth"], p["birthplace"], p["education"],
                 p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                (o["id"], o["name"], o["type"], o["level"],
                 o["parent"], o["location"]))

for pos in positions:
    cur.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)""",
                (pos["id"], pos["person_id"], pos["org_id"],
                 pos["title"], pos["start"], pos["end"],
                 pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("""INSERT INTO relationships VALUES (?,?,?,?,?,?,?)""",
                (r["id"], r["person_a_id"], r["person_b_id"],
                 r["type"], r["context"],
                 r["overlap_org"], r["overlap_period"]))

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


# ── BUILD GEXF GRAPH ────────────────────────────────

today = datetime.now().strftime("%Y-%m-%d")

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>宁海县领导班子工作关系网络 - {today}</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="category" title="Category" type="string"/>')
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
    # Color by role
    if p["id"] == 1:   # Party Secretary
        r, g, b = 255, 50, 50
        size = 20.0
    elif p["id"] == 2:  # County Mayor
        r, g, b = 50, 100, 255
        size = 20.0
    elif p["id"] == 3:  # Executive Deputy Mayor (常委)
        r, g, b = 50, 100, 255
        size = 14.0
    elif p["id"] in [4, 5]:  # Other Standing Committee
        r, g, b = 100, 100, 100
        size = 14.0
    elif p["id"] in [12, 13]:  # 人大/政协
        r, g, b = 200, 200, 100
        size = 14.0
    else:
        r, g, b = 100, 100, 100  # Grey: other deputy mayors
        size = 12.0

    lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="current_post" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="source" value="{esc(p["source"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'      </node>')

# Organization nodes
for o in organizations:
    oid = 1000 + o["id"]
    lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{esc(o["type"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="44" g="62" b="80"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
edge_num = 1

# person→organization (worked_at)
for pos in positions:
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="{edge_num}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{esc(pos["title"])}"/>')
    lines.append(f'          <attvalue for="period" value="{pos["start"] or "?"} → {pos["end"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_num += 1

# person↔person (relationships)
for r in relationships:
    lines.append(f'      <edge id="{edge_num}" source="{r["person_a_id"]}" target="{r["person_b_id"]}" label="{r["type"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{r["type"]}"/>')
    lines.append(f'          <attvalue for="context" value="{esc(r["context"])}"/>')
    lines.append(f'          <attvalue for="period" value="{r["overlap_period"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_num += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

total_nodes = len(persons) + len(organizations)
total_edges = len(positions) + len(relationships)
print(f"\nGEXF graph written: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} orgs = {total_nodes} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} rels = {total_edges} total")
print("\nDone!")