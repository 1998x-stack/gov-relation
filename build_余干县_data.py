#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 余干县 (Yugan County) leadership network.

上饶市余干县 - county-level administrative division of Shangrao City, Jiangxi Province.

Targets: 县委书记 & 县长

Current leadership (as of 2026-07):
- 县委书记: （待核实）
- 县长: （待核实）

Note: Exa/Baidu/Google/Wikipedia all blocked in current network environment.
Data is based on historical references found in existing repository build scripts.

Sources:
- build_shangrao_data.py (上饶市领导数据)
- build_ruichang_data.py (吴松曾任余干副县长)
- build_jingdezhen_mayor_data.py (刘峰曾任余干县委常委、组织部长)
- build_广丰区_data.py references
- Historical knowledge from repository
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/jiangxi_余干县")
DB_PATH = os.path.join(TMP, "余干县_network.db")
GEXF_PATH = os.path.join(TMP, "余干县_network.gexf")

os.makedirs(TMP, exist_ok=True)

# ════════════════════════════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════════════════════════════

# ── Current top leaders (待核实 — network blocked) ──
# Based on historical patterns: 
# 胡伟 was 余干县委书记 until ~2021 (based on news patterns)
# After 胡伟, leadership changes not confirmed from accessible sources
# 
# Common pattern in 上饶: county party secretaries serve ~3-5 years
# Recent 上饶 county leadership known from other build scripts:
# - 广信区: 叶文华 (区委书记), 顾海敏 (区长)
# - 广丰区: 待核实
# - 横峰县: 待核实
# - 弋阳县: 待核实
# - 铅山县: 待核实

persons = [
    # ── Current top leaders (待核实) ──
    {"id": 1, "name": "（待核实）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共余干县委书记", "current_org": "中共余干县委员会",
     "source": "网络环境限制，待核实"},

    {"id": 2, "name": "（待核实）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "余干县委副书记、县人民政府县长", "current_org": "余干县人民政府",
     "source": "网络环境限制，待核实"},

    # ── Historical: 胡伟 (former 余干县委书记, ~2016-2021) ──
    # 胡伟 served as 余干县委书记 from approximately 2016 to 2021
    # Born 1972, served in Shangrao system
    {"id": 3, "name": "胡伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "历史数据：曾任余干县委书记"},

    # ── Historical: 江忠汉 (former 余干县长, ~2016-2021) ──
    {"id": 4, "name": "江忠汉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "历史数据：曾任余干县长"},

    # ── 吴松 (former 余干副县长, 2016-2020, now 瑞昌市委书记) ──
    # From build_ruichang_data.py: 吴松, 1981-02, 江西弋阳人
    # 余干县人民政府副县长 (2016.09-2020.06)
    {"id": 5, "name": "吴松", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-02", "birthplace": "江西弋阳", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瑞昌市委书记（现任）", "current_org": "中共瑞昌市委员会",
     "source": "build_ruichang_data.py; 曾任余干副县长 2016-2020"},

    # ── 刘峰 (former 余干县委常委、组织部部长, 1997-11) ──
    # From build_jingdezhen_mayor_data.py
    {"id": 6, "name": "刘峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "build_jingdezhen_mayor_data.py; 曾任余干县委常委、组织部部长(1997-11)"},

    # ── 李高兴 (现任上饶市人大常委会主任, 江西余干人) ──
    # From build_shangrao_data.py: 1968-10, 江西余干人
    {"id": 7, "name": "李高兴", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-10", "birthplace": "江西余干", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "上饶市人大常委会主任", "current_org": "上饶市人大常委会",
     "source": "build_shangrao_data.py; https://zh.wikipedia.org/wiki/上饶市"},

    # ── 万广明 (现任江西省副省长, 江西余干人) ──
    # From build_jiangxi_province_data.py: 1967-01, 江西余干人
    {"id": 8, "name": "万广明", "gender": "男", "ethnicity": "汉族",
     "birth": "1967-01", "birthplace": "江西余干", "education": "研究生，工学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江西省人民政府副省长", "current_org": "江西省人民政府",
     "source": "build_jiangxi_province_data.py"},

    # ── 谭赣明 (现任宜春市长, 江西余干人) ──
    # From build_yichun_data.py: 1972-02, 江西余干人
    {"id": 9, "name": "谭赣明", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-02", "birthplace": "江西余干", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "宜春市委副书记、市长", "current_org": "宜春市人民政府",
     "source": "build_yichun_data.py; https://district.ce.cn/newarea/sddy/202308/t20230812_3201106.shtml"},

    # ── 洪略 (现任南昌市青云谱区委副书记、代区长, 江西余干人) ──
    # From build_qingyunpu_data.py: 1991-01, 江西余干人
    {"id": 10, "name": "洪略", "gender": "男", "ethnicity": "汉族",
     "birth": "1991-01", "birthplace": "江西余干", "education": "法学博士",
     "party_join": "", "work_start": "2018-08",
     "current_post": "南昌市青云谱区委副书记、代区长", "current_org": "南昌市青云谱区人民政府",
     "source": "build_qingyunpu_data.py"},
]

organizations = [
    {"id": 1, "name": "中共余干县委员会", "type": "党委", "level": "县处级", "parent": "中共上饶市委员会", "location": "江西省上饶市余干县"},
    {"id": 2, "name": "余干县人民政府", "type": "政府", "level": "县处级", "parent": "上饶市人民政府", "location": "江西省上饶市余干县"},
    {"id": 3, "name": "中共上饶市委员会", "type": "党委", "level": "地级", "parent": "中共江西省委员会", "location": "江西省上饶市"},
    {"id": 4, "name": "上饶市人民政府", "type": "政府", "level": "地级", "parent": "江西省人民政府", "location": "江西省上饶市"},
    {"id": 5, "name": "上饶市人大常委会", "type": "人大", "level": "地级", "parent": "江西省人大常委会", "location": "江西省上饶市"},
    {"id": 6, "name": "江西省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "江西省南昌市"},
    {"id": 7, "name": "宜春市人民政府", "type": "政府", "level": "地级", "parent": "江西省人民政府", "location": "江西省宜春市"},
    {"id": 8, "name": "中共瑞昌市委员会", "type": "党委", "level": "县处级", "parent": "中共九江市委员会", "location": "江西省九江市瑞昌市"},
    {"id": 9, "name": "南昌市青云谱区人民政府", "type": "政府", "level": "县处级", "parent": "南昌市人民政府", "location": "江西省南昌市青云谱区"},
]

positions = [
    # ── Current Party Secretary (待核实) ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共余干县委书记", "start": "", "end": "", "rank": "县处级正职", "note": "现任，姓名待核实"},

    # ── Current County Mayor (待核实) ──
    {"id": 2, "person_id": 2, "org_id": 2, "title": "余干县委副书记、县人民政府县长", "start": "", "end": "", "rank": "县处级正职", "note": "现任，姓名待核实"},
    {"id": 3, "person_id": 2, "org_id": 1, "title": "余干县委副书记", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── 胡伟 (former 县委书记) ──
    {"id": 4, "person_id": 3, "org_id": 1, "title": "中共余干县委书记", "start": "~2016", "end": "~2021", "rank": "县处级正职", "note": "前任县委书记，具体任职起止时间待核实"},

    # ── 江忠汉 (former 县长) ──
    {"id": 5, "person_id": 4, "org_id": 2, "title": "余干县人民政府县长", "start": "~2016", "end": "~2021", "rank": "县处级正职", "note": "前任县长，具体任职起止时间待核实"},
    {"id": 6, "person_id": 4, "org_id": 1, "title": "余干县委副书记", "start": "~2016", "end": "~2021", "rank": "县处级副职", "note": ""},

    # ── 吴松 (former 余干副县长, 2016-2020) ──
    {"id": 7, "person_id": 5, "org_id": 2, "title": "余干县人民政府副县长", "start": "2016-09", "end": "2020-06", "rank": "副处级", "note": "来自build_ruichang_data.py"},
    {"id": 8, "person_id": 5, "org_id": 8, "title": "瑞昌市委书记", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},

    # ── 刘峰 (former 余干县委常委、组织部部长, ~1997) ──
    {"id": 9, "person_id": 6, "org_id": 1, "title": "余干县委常委、组织部部长", "start": "1997-11", "end": "", "rank": "县处级副职", "note": "来自build_jingdezhen_mayor_data.py"},

    # ── 李高兴 (上饶市人大常委会主任, 余干人) ──
    {"id": 10, "person_id": 7, "org_id": 5, "title": "上饶市人大常委会主任", "start": "", "end": "", "rank": "地厅级正职", "note": "现任"},

    # ── 万广明 (江西省副省长, 余干人) ──
    {"id": 11, "person_id": 8, "org_id": 6, "title": "江西省人民政府副省长", "start": "", "end": "", "rank": "省部级副职", "note": "现任"},

    # ── 谭赣明 (宜春市长, 余干人) ──
    {"id": 12, "person_id": 9, "org_id": 7, "title": "宜春市委副书记、市长", "start": "2023-08", "end": "", "rank": "地厅级正职", "note": "现任"},

    # ── 洪略 (青云谱代区长, 余干人) ──
    {"id": 13, "person_id": 10, "org_id": 9, "title": "南昌市青云谱区委副书记、代区长", "start": "~2026", "end": "", "rank": "副厅级", "note": "代区长"},
]

relationships = [
    # ── Predecessor-Successor (historical) ──
    {"id": 1, "person_a_id": 3, "person_b_id": 1, "type": "职务接替", "context": "胡伟→（现任）余干县委书记接替", "overlap_org": "中共余干县委员会", "overlap_period": "~2021"},
    {"id": 2, "person_a_id": 4, "person_b_id": 2, "type": "职务接替", "context": "江忠汉→（现任）余干县长接替", "overlap_org": "余干县人民政府", "overlap_period": "~2021"},
    {"id": 3, "person_a_id": 3, "person_b_id": 4, "type": "党政搭档", "context": "胡伟（县委书记）与江忠汉（县长）同为余干县党政主要领导", "overlap_org": "中共余干县委员会", "overlap_period": "~2016-2021"},
    {"id": 4, "person_a_id": 3, "person_b_id": 5, "type": "上下级", "context": "胡伟（县委书记）与吴松（副县长）在余干县共事", "overlap_org": "中共余干县委员会", "overlap_period": "2016-2020"},
    {"id": 5, "person_a_id": 4, "person_b_id": 5, "type": "上下级", "context": "江忠汉（县长）与吴松（副县长）在余干县政府共事", "overlap_org": "余干县人民政府", "overlap_period": "2016-2020"},

    # ── 余干籍贯横向联系 ──
    {"id": 6, "person_a_id": 7, "person_b_id": 8, "type": "同乡", "context": "李高兴（上饶市人大常委会主任）与万广明（江西省副省长）均为江西余干人", "overlap_org": "", "overlap_period": ""},
    {"id": 7, "person_a_id": 7, "person_b_id": 9, "type": "同乡", "context": "李高兴与谭赣明（宜春市长）均为江西余干人", "overlap_org": "", "overlap_period": ""},
    {"id": 8, "person_a_id": 8, "person_b_id": 9, "type": "同乡", "context": "万广明（江西省副省长）与谭赣明（宜春市长）均为江西余干人", "overlap_org": "", "overlap_period": ""},
    {"id": 9, "person_a_id": 7, "person_b_id": 10, "type": "同乡", "context": "李高兴与洪略（青云谱代区长）均为江西余干人", "overlap_org": "", "overlap_period": ""},
    {"id": 10, "person_a_id": 8, "person_b_id": 10, "type": "同乡", "context": "万广明与洪略均为江西余干人", "overlap_org": "", "overlap_period": ""},

    # ── 余干县与上级组织 ──
    {"id": 11, "person_a_id": 7, "person_b_id": 1, "type": "上下级", "context": "李高兴（上饶市人大常委会主任）与余干县委书记为市-县上下级关系", "overlap_org": "", "overlap_period": ""},
    {"id": 12, "person_a_id": 8, "person_b_id": 1, "type": "上下级", "context": "万广明（副省长）与余干县委书记为省-县上下级关系", "overlap_org": "", "overlap_period": ""},
]


# ════════════════════════════════════════════════════════════════════
# BUILD SQLite DATABASE
# ════════════════════════════════════════════════════════════════════

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


# ════════════════════════════════════════════════════════════════════
# BUILD GEXF GRAPH
# ════════════════════════════════════════════════════════════════════

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
lines.append(f'    <description>余干县领导班子工作关系网络 - {today}</description>')
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
    pid = p["id"]
    # Color by role
    if pid == 1:  # Party Secretary (current, placeholder)
        color_hex = '#E03C31'
        size = 20.0
    elif pid == 3:  # Party Secretary (former)
        color_hex = '#E03C31'
        size = 18.0
    elif pid == 2:  # County Mayor (placeholder)
        color_hex = '#2980B9'
        size = 20.0
    elif pid == 4:  # County Mayor (former)
        color_hex = '#2980B9'
        size = 18.0
    elif pid in [5, 6]:  # Former county deputies
        color_hex = '#2980B9'
        size = 14.0
    elif pid in [7, 8, 9, 10]:  # Notable 余干-connected figures
        color_hex = '#C9A94E'
        size = 14.0
    else:
        color_hex = '#95A5A6'
        size = 12.0

    r_val = int(color_hex[1:3], 16)
    g_val = int(color_hex[3:5], 16)
    b_val = int(color_hex[5:7], 16)

    lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{esc(p["birth"])}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{esc(p["birthplace"])}"/>')
    lines.append(f'          <attvalue for="education" value="{esc(p["education"])}"/>')
    lines.append(f'          <attvalue for="current_post" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="source" value="{esc(p["source"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{r_val}" g="{g_val}" b="{b_val}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'      </node>')

# ── Nodes: Organizations ──
for o in organizations:
    oid = 1000 + o["id"]
    # Color by org type
    if o["type"] == "党委":
        org_color = "200,255,200"  # Light green
    elif o["type"] == "政府":
        org_color = "200,200,255"  # Light blue
    elif o["type"] == "人大":
        org_color = "200,255,255"  # Cyan
    else:
        org_color = "200,200,200"  # Light grey

    lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{esc(o["type"])}"/>')
    lines.append(f'        </attvalues>')
    oc_r, oc_g, oc_b = org_color.split(",")
    lines.append(f'        <viz:color r="{oc_r}" g="{oc_g}" b="{oc_b}"/>')
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
    lines.append(f'          <attvalue for="context" value="{esc(pos["title"])}"/>')
    lines.append(f'          <attvalue for="period" value="{esc(pos["start"] or "?")} → {esc(pos["end"] or "今")}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

# person↔person (relationships)
for r in relationships:
    lines.append(f'      <edge id="{edge_id}" source="{r["person_a_id"]}" target="{r["person_b_id"]}" label="{esc(r["type"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="context" value="{esc(r["context"])}"/>')
    lines.append(f'          <attvalue for="period" value="{esc(r["overlap_period"])}"/>')
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

# ── Verify ──
if os.path.exists(DB_PATH):
    print(f"\n✓ SQLite DB exists: {DB_PATH}")
if os.path.exists(GEXF_PATH):
    print(f"✓ GEXF exists: {GEXF_PATH}")

print("\nDone!")
