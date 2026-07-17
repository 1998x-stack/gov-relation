#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 屏南县 leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/fujian_屏南县")
DB_PATH = os.path.join(TMP, "屏南县_network.db")
GEXF_PATH = os.path.join(TMP, "屏南县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Party Secretary ──
    {"id": 1, "name": "周春海", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共屏南县委书记", "current_org": "中共屏南县委员会",
     "source": "https://www.pingnan.gov.cn"},

    # ── Current County Mayor ──
    {"id": 2, "name": "霍立昀", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "屏南县人民政府县长", "current_org": "屏南县人民政府",
     "source": "https://www.pingnan.gov.cn"},

    # ── County People's Congress Director ──
    {"id": 3, "name": "陆泽干", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "屏南县人大常委会主任", "current_org": "屏南县人大常委会",
     "source": "https://www.pingnan.gov.cn"},

    # ── County CPPCC Chairman ──
    {"id": 4, "name": "张德力", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "屏南县政协主席", "current_org": "屏南县政协",
     "source": "https://www.pingnan.gov.cn"},

    # ── Key Deputies ──
    {"id": 5, "name": "魏宏峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "屏南县委常委、常务副县长", "current_org": "屏南县人民政府",
     "source": "https://www.pingnan.gov.cn"},

    {"id": 6, "name": "兰艺欣", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "屏南县委常委、组织部部长", "current_org": "中共屏南县委员会",
     "source": "https://www.pingnan.gov.cn"},

    {"id": 7, "name": "陈剑峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "屏南县委常委、纪委书记、县监委主任", "current_org": "中共屏南县纪律检查委员会",
     "source": "https://www.pingnan.gov.cn"},

    {"id": 8, "name": "陆东炫", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "屏南县委常委、政法委书记", "current_org": "中共屏南县委员会",
     "source": "https://www.pingnan.gov.cn"},

    {"id": 9, "name": "韦孝珠", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "屏南县委常委、宣传部部长", "current_org": "中共屏南县委员会",
     "source": "https://www.pingnan.gov.cn"},

    {"id": 10, "name": "陈传旺", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "屏南县委常委、统战部部长", "current_org": "中共屏南县委员会",
     "source": "https://www.pingnan.gov.cn"},

    {"id": 11, "name": "张著文", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "屏南县人民政府副县长", "current_org": "屏南县人民政府",
     "source": "https://www.pingnan.gov.cn"},

    {"id": 12, "name": "陈思文", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "屏南县人民政府副县长", "current_org": "屏南县人民政府",
     "source": "https://www.pingnan.gov.cn"},

    {"id": 13, "name": "李章通", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "屏南县人民政府副县长、公安局局长", "current_org": "屏南县公安局",
     "source": "https://www.pingnan.gov.cn"},

    {"id": 14, "name": "何雷鸣", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "屏南县人民政府副县长", "current_org": "屏南县人民政府",
     "source": "https://www.pingnan.gov.cn"},

    {"id": 15, "name": "苏健", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "屏南县人民政府科技副县长", "current_org": "屏南县人民政府",
     "source": "https://www.pingnan.gov.cn"},

    # ── Predecessors ──
    {"id": 16, "name": "党帅", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-07", "birthplace": "山东济南", "education": "博士研究生（清华大学）",
     "party_join": "中共党员", "work_start": "2010-07",
     "current_post": "屏南县委书记（原任）", "current_org": "中共屏南县委员会",
     "source": "https://zh.wikipedia.org/wiki/%E5%8F%A4%E7%94%B0%E5%8E%BF"},

    {"id": 17, "name": "柳岳", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "屏南县人民政府县长（原任）", "current_org": "屏南县人民政府",
     "source": "http://www.pingnan.gov.cn"},

    {"id": 18, "name": "蔡晶晶", "gender": "女", "ethnicity": "汉族",
     "birth": "1982-11", "birthplace": "", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "霞浦县人民政府代县长", "current_org": "霞浦县人民政府",
     "source": "https://report/open_gaps.md"},
]

organizations = [
    {"id": 1, "name": "中共屏南县委员会", "type": "党委"},
    {"id": 2, "name": "屏南县人民政府", "type": "政府"},
    {"id": 3, "name": "屏南县人大常委会", "type": "人大"},
    {"id": 4, "name": "屏南县政协", "type": "政协"},
    {"id": 5, "name": "中共屏南县纪律检查委员会", "type": "纪委"},
    {"id": 6, "name": "屏南县委组织部", "type": "党委"},
    {"id": 7, "name": "屏南县委宣传部", "type": "党委"},
    {"id": 8, "name": "屏南县委政法委", "type": "党委"},
    {"id": 9, "name": "屏南县委统战部", "type": "党委"},
    {"id": 10, "name": "屏南县公安局", "type": "政府"},
    {"id": 11, "name": "古田县人民政府", "type": "政府"},
    {"id": 12, "name": "霞浦县人民政府", "type": "政府"},
    {"id": 13, "name": "中共霞浦县委员会", "type": "党委"},
    {"id": 14, "name": "宁德市人民政府", "type": "政府"},
    {"id": 15, "name": "宁德市人民检察院", "type": "其他"},
]

positions = [
    # 周春海 - Party Secretary
    {"person_id": 1, "org_id": 1, "title": "中共屏南县委书记", "start": "", "end": "至今"},

    # 霍立昀 - County Mayor
    {"person_id": 2, "org_id": 2, "title": "屏南县人民政府县长", "start": "", "end": "至今"},
    {"person_id": 2, "org_id": 1, "title": "中共屏南县委副书记", "start": "", "end": "至今"},

    # 陆泽干 - Congress Director
    {"person_id": 3, "org_id": 3, "title": "屏南县人大常委会主任", "start": "", "end": "至今"},

    # 张德力 - CPPCC Chairman
    {"person_id": 4, "org_id": 4, "title": "屏南县政协主席", "start": "", "end": "至今"},

    # 魏宏峰 - Executive Deputy Mayor
    {"person_id": 5, "org_id": 2, "title": "屏南县委常委、常务副县长", "start": "", "end": "至今"},
    {"person_id": 5, "org_id": 1, "title": "屏南县委常委", "start": "", "end": "至今"},

    # 兰艺欣 - Organization Dept
    {"person_id": 6, "org_id": 6, "title": "屏南县委常委、组织部部长", "start": "", "end": "至今"},
    {"person_id": 6, "org_id": 1, "title": "屏南县委常委", "start": "", "end": "至今"},

    # 陈剑峰 - Discipline Inspection
    {"person_id": 7, "org_id": 5, "title": "屏南县委常委、纪委书记、县监委主任", "start": "", "end": "至今"},
    {"person_id": 7, "org_id": 1, "title": "屏南县委常委", "start": "", "end": "至今"},

    # 陆东炫 - Political/Legal
    {"person_id": 8, "org_id": 8, "title": "屏南县委常委、政法委书记", "start": "", "end": "至今"},
    {"person_id": 8, "org_id": 1, "title": "屏南县委常委", "start": "", "end": "至今"},

    # 韦孝珠 - Propaganda
    {"person_id": 9, "org_id": 7, "title": "屏南县委常委、宣传部部长", "start": "", "end": "至今"},
    {"person_id": 9, "org_id": 1, "title": "屏南县委常委", "start": "", "end": "至今"},

    # 陈传旺 - United Front
    {"person_id": 10, "org_id": 9, "title": "屏南县委常委、统战部部长", "start": "", "end": "至今"},
    {"person_id": 10, "org_id": 1, "title": "屏南县委常委", "start": "", "end": "至今"},

    # 张著文 - Deputy Mayor
    {"person_id": 11, "org_id": 2, "title": "屏南县人民政府副县长", "start": "", "end": "至今"},

    # 陈思文 - Deputy Mayor
    {"person_id": 12, "org_id": 2, "title": "屏南县人民政府副县长", "start": "", "end": "至今"},

    # 李章通 - Deputy Mayor + Public Security
    {"person_id": 13, "org_id": 2, "title": "屏南县人民政府副县长、公安局局长", "start": "", "end": "至今"},
    {"person_id": 13, "org_id": 10, "title": "屏南县公安局局长", "start": "", "end": "至今"},

    # 何雷鸣 - Deputy Mayor
    {"person_id": 14, "org_id": 2, "title": "屏南县人民政府副县长", "start": "", "end": "至今"},

    # 苏健 - Science/Tech Deputy Mayor
    {"person_id": 15, "org_id": 2, "title": "屏南县人民政府科技副县长", "start": "", "end": "至今"},

    # Predecessors
    {"person_id": 16, "org_id": 1, "title": "中共屏南县委书记（原任）", "start": "", "end": ""},

    {"person_id": 17, "org_id": 2, "title": "屏南县人民政府县长（原任）", "start": "", "end": ""},

    {"person_id": 18, "org_id": 1, "title": "中共屏南县委副书记（原任）", "start": "", "end": ""},
    {"person_id": 18, "org_id": 12, "title": "霞浦县人民政府代县长", "start": "", "end": "至今"},
]

relationships = [
    # 周春海 ↔ 霍立昀 (Party-Government 搭档)
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "superior_subordinate",
     "context": "周春海作为县委书记领导县长霍立昀", "overlap_org": "中共屏南县委员会", "overlap_period": "至今"},

    # 魏宏峰 ↔ 周春海 (Standing Committee overlap)
    {"id": 2, "person_a_id": 5, "person_b_id": 1, "type": "overlap",
     "context": "县委常委班子共事", "overlap_org": "中共屏南县委员会", "overlap_period": ""},

    # 兰艺欣 ↔ 周春海
    {"id": 3, "person_a_id": 6, "person_b_id": 1, "type": "overlap",
     "context": "县委常委班子共事", "overlap_org": "中共屏南县委员会", "overlap_period": ""},

    # 陈剑峰 ↔ 周春海
    {"id": 4, "person_a_id": 7, "person_b_id": 1, "type": "overlap",
     "context": "县委常委班子共事", "overlap_org": "中共屏南县委员会", "overlap_period": ""},

    # 陆东炫 ↔ 周春海
    {"id": 5, "person_a_id": 8, "person_b_id": 1, "type": "overlap",
     "context": "县委常委班子共事", "overlap_org": "中共屏南县委员会", "overlap_period": ""},

    # 韦孝珠 ↔ 周春海
    {"id": 6, "person_a_id": 9, "person_b_id": 1, "type": "overlap",
     "context": "县委常委班子共事", "overlap_org": "中共屏南县委员会", "overlap_period": ""},

    # 陈传旺 ↔ 周春海
    {"id": 7, "person_a_id": 10, "person_b_id": 1, "type": "overlap",
     "context": "县委常委班子共事", "overlap_org": "中共屏南县委员会", "overlap_period": ""},

    # 魏宏峰 ↔ 霍立昀 (Government team)
    {"id": 8, "person_a_id": 5, "person_b_id": 2, "type": "overlap",
     "context": "县政府班子成员", "overlap_org": "屏南县人民政府", "overlap_period": ""},

    # 张著文 ↔ 霍立昀
    {"id": 9, "person_a_id": 11, "person_b_id": 2, "type": "overlap",
     "context": "县政府班子成员", "overlap_org": "屏南县人民政府", "overlap_period": ""},

    # 陈思文 ↔ 霍立昀
    {"id": 10, "person_a_id": 12, "person_b_id": 2, "type": "overlap",
     "context": "县政府班子成员", "overlap_org": "屏南县人民政府", "overlap_period": ""},

    # 李章通 ↔ 霍立昀
    {"id": 11, "person_a_id": 13, "person_b_id": 2, "type": "overlap",
     "context": "县政府班子成员", "overlap_org": "屏南县人民政府", "overlap_period": ""},

    # 何雷鸣 ↔ 霍立昀
    {"id": 12, "person_a_id": 14, "person_b_id": 2, "type": "overlap",
     "context": "县政府班子成员", "overlap_org": "屏南县人民政府", "overlap_period": ""},

    # 周春海 ↔ 党帅 (Predecessor-Successor)
    {"id": 13, "person_a_id": 1, "person_b_id": 16, "type": "predecessor_successor",
     "context": "周春海接替党帅任屏南县委书记", "overlap_org": "中共屏南县委员会", "overlap_period": ""},

    # 霍立昀 ↔ 柳岳 (Predecessor-Successor)
    {"id": 14, "person_a_id": 2, "person_b_id": 17, "type": "predecessor_successor",
     "context": "霍立昀接替柳岳任屏南县长", "overlap_org": "屏南县人民政府", "overlap_period": ""},

    # 陆泽干 ↔ 周春海 (Four-bank leadership)
    {"id": 15, "person_a_id": 3, "person_b_id": 1, "type": "overlap",
     "context": "县四套班子领导", "overlap_org": "屏南县", "overlap_period": "至今"},

    # 张德力 ↔ 周春海
    {"id": 16, "person_a_id": 4, "person_b_id": 1, "type": "overlap",
     "context": "县四套班子领导", "overlap_org": "屏南县", "overlap_period": "至今"},

    # 蔡晶晶 ↔ 周春海 (曾为屏南县委副书记)
    {"id": 17, "person_a_id": 18, "person_b_id": 1, "type": "overlap",
     "context": "曾共事于屏南县委", "overlap_org": "中共屏南县委员会", "overlap_period": ""},
]


# ── BUILD SQLITE DATABASE ─────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
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
    type TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    person_id INTEGER,
    org_id INTEGER,
    title TEXT,
    start TEXT,
    end TEXT,
    FOREIGN KEY(person_id) REFERENCES persons(id),
    FOREIGN KEY(org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY,
    person_a_id INTEGER,
    person_b_id INTEGER,
    type TEXT,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY(person_a_id) REFERENCES persons(id),
    FOREIGN KEY(person_b_id) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (p["id"], p["name"], p["gender"], p["ethnicity"],
                 p["birth"], p["birthplace"], p["education"],
                 p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""INSERT INTO organizations VALUES (?,?,?)""",
                (o["id"], o["name"], o["type"]))

for pos in positions:
    cur.execute("""INSERT INTO positions VALUES (?,?,?,?,?)""",
                (pos["person_id"], pos["org_id"], pos["title"],
                 pos["start"], pos["end"]))

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

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return color string based on role."""
    if p["id"] == 1:
        return "255,50,50"    # red: party secretary
    elif p["id"] == 2:
        return "50,100,255"   # blue: government leader
    elif p["id"] == 7:
        return "255,165,0"    # orange: discipline
    elif p["id"] in [3, 4]:
        return "100,100,100"  # grey: congress/cppcc
    else:
        return "100,100,100"  # grey: others

def person_size(p):
    if p["id"] in [1, 2]:
        return "20.0"
    elif p["id"] in [3, 4]:
        return "16.0"
    elif p["id"] in [5, 6, 7, 8, 9, 10]:
        return "14.0"
    else:
        return "12.0"

def org_color(o):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "纪委": "255,165,0",
    }
    return colors.get(o["type"], "200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>屏南县领导班子工作关系网络 - {today}</description>')
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
    c = person_color(p)
    sz = person_size(p)
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{esc(p["birth"])}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{esc(p["birthplace"])}"/>')
    lines.append(f'          <attvalue for="education" value="{esc(p["education"])}"/>')
    lines.append(f'          <attvalue for="current_post" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="source" value="{esc(p["source"])}"/>')
    lines.append(f'        </attvalues>')
    rgb = c.split(",")
    lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append(f'      </node>')

# ── Nodes: Organizations ──
for o in organizations:
    oid = 1000 + o["id"]
    c = org_color(o)
    lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{esc(o["type"])}"/>')
    lines.append(f'        </attvalues>')
    rgb = c.split(",")
    lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'      </node>')
lines.append('    </nodes>')

# ── Edges ──
lines.append('    <edges>')
edge_id = 1

# person→organization (worked_at)
for pos in positions:
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="e{edge_id}" source="p{pos["person_id"]}" target="o{oid}" label="worked_at">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{esc(pos["title"])}"/>')
    lines.append(f'          <attvalue for="period" value="{pos["start"] or "?"} → {pos["end"] or "今"}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

# person↔person (relationships)
for r in relationships:
    lines.append(f'      <edge id="e{edge_id}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" label="{esc(r["type"])}">')
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

print("\nDone!")
