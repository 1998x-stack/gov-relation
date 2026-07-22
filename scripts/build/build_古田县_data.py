#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 古田县 leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/fujian_古田县")
DB_PATH = os.path.join(TMP, "古田县_network.db")
GEXF_PATH = os.path.join(TMP, "古田县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Party Secretary ──
    {"id": 1, "name": "许锋", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-05", "birthplace": "福建霞浦", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1995-08",
     "current_post": "中共古田县委书记", "current_org": "中共古田县委员会",
     "source": "https://zh.wikipedia.org/wiki/%E5%8F%A4%E7%94%B0%E5%8E%BF"},

    # ── Current County Mayor ──
    {"id": 2, "name": "吴新情", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-11", "birthplace": "福建寿宁", "education": "在职大学",
     "party_join": "中共党员", "work_start": "1998-08",
     "current_post": "古田县人民政府县长", "current_org": "古田县人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E5%8F%A4%E7%94%B0%E5%8E%BF"},

    # ── County People's Congress Director ──
    {"id": 3, "name": "郑国淑", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古田县人大常委会主任", "current_org": "古田县人大常委会",
     "source": "https://zh.wikipedia.org/wiki/%E5%8F%A4%E7%94%B0%E5%8E%BF"},

    # ── County CPPCC Chairman ──
    {"id": 4, "name": "林纪建", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古田县政协主席", "current_org": "古田县政协",
     "source": "https://zh.wikipedia.org/wiki/%E5%8F%A4%E7%94%B0%E5%8E%BF"},

    # ── Key Deputies ──
    {"id": 5, "name": "俞仰林", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古田县委常委、常务副县长", "current_org": "古田县人民政府",
     "source": "https://www.gutian.gov.cn"},

    {"id": 6, "name": "叶斯颖", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古田县委常委、组织部部长", "current_org": "中共古田县委员会",
     "source": "https://www.gutian.gov.cn"},

    {"id": 7, "name": "林晓晞", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古田县委常委、纪委书记、县监委主任", "current_org": "中共古田县纪律检查委员会",
     "source": "https://www.gutian.gov.cn"},

    {"id": 8, "name": "黄建", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古田县委常委、政法委书记", "current_org": "中共古田县委员会",
     "source": "https://www.gutian.gov.cn"},

    {"id": 9, "name": "张明生", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古田县委常委、宣传部部长", "current_org": "中共古田县委员会",
     "source": "https://www.gutian.gov.cn"},

    {"id": 10, "name": "李黄灼", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古田县委常委、统战部部长", "current_org": "中共古田县委员会",
     "source": "https://www.gutian.gov.cn"},

    {"id": 11, "name": "刘荣", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古田县委常委、县人武部政委", "current_org": "古田县人民武装部",
     "source": "https://www.gutian.gov.cn"},

    {"id": 12, "name": "张沂", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古田县人民政府副县长", "current_org": "古田县人民政府",
     "source": "https://www.gutian.gov.cn"},

    {"id": 13, "name": "黄忠钦", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古田县人民政府副县长、公安局局长", "current_org": "古田县人民政府",
     "source": "https://www.gutian.gov.cn"},

    {"id": 14, "name": "雷毅", "gender": "男", "ethnicity": "畲族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古田县人民政府副县长", "current_org": "古田县人民政府",
     "source": "https://www.gutian.gov.cn"},

    {"id": 15, "name": "陈锐杰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古田县人民政府副县长", "current_org": "古田县人民政府",
     "source": "https://www.gutian.gov.cn"},

    {"id": 16, "name": "李晓霞", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "古田县人民政府科技副县长", "current_org": "古田县人民政府",
     "source": "https://www.gutian.gov.cn"},

    # ── Predecessors ──
    {"id": 17, "name": "张成慧", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-04", "birthplace": "福建福安", "education": "在职大学",
     "party_join": "中共党员", "work_start": "1991-08",
     "current_post": "宁德市人民政府副市长", "current_org": "宁德市人民政府",
     "source": "https://baike.baidu.com/item/%E5%BC%A0%E6%88%90%E6%85%A7"},

    {"id": 18, "name": "党帅", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-07", "birthplace": "山东济南", "education": "博士研究生（清华大学）",
     "party_join": "中共党员", "work_start": "2010-07",
     "current_post": "屏南县委书记", "current_org": "中共屏南县委员会",
     "source": "https://baike.baidu.com/item/%E5%85%9A%E5%B8%85"},
]

organizations = [
    {"id": 1, "name": "中共古田县委员会", "type": "党委"},
    {"id": 2, "name": "古田县人民政府", "type": "政府"},
    {"id": 3, "name": "古田县人大常委会", "type": "人大"},
    {"id": 4, "name": "古田县政协", "type": "政协"},
    {"id": 5, "name": "中共古田县纪律检查委员会", "type": "纪委"},
    {"id": 6, "name": "古田县委组织部", "type": "党委"},
    {"id": 7, "name": "古田县委宣传部", "type": "党委"},
    {"id": 8, "name": "古田县委政法委", "type": "党委"},
    {"id": 9, "name": "古田县委统战部", "type": "党委"},
    {"id": 10, "name": "古田县人民武装部", "type": "其他"},
    {"id": 11, "name": "古田县公安局", "type": "政府"},
    {"id": 12, "name": "古田县人民检察院", "type": "其他"},
    {"id": 13, "name": "古田县人民法院", "type": "其他"},
    {"id": 14, "name": "宁德市人民政府", "type": "政府"},
    {"id": 15, "name": "中共屏南县委员会", "type": "党委"},
]

positions = [
    # 许锋 - Party Secretary
    {"person_id": 1, "org_id": 1, "title": "中共古田县委书记", "start": "2025-04", "end": "至今"},
    {"person_id": 1, "org_id": 2, "title": "古田县人民政府县长（原任）", "start": "", "end": "2025-04"},

    # 吴新情 - County Mayor
    {"person_id": 2, "org_id": 2, "title": "古田县人民政府县长", "start": "2025-04", "end": "至今"},

    # 郑国淑 - Congress Director
    {"person_id": 3, "org_id": 3, "title": "古田县人大常委会主任", "start": "2021-12", "end": "至今"},

    # 林纪建 - CPPCC Chairman
    {"person_id": 4, "org_id": 4, "title": "古田县政协主席", "start": "2021-12", "end": "至今"},

    # 俞仰林 - Executive Deputy Mayor
    {"person_id": 5, "org_id": 2, "title": "古田县委常委、常务副县长", "start": "", "end": "至今"},
    {"person_id": 5, "org_id": 1, "title": "古田县委常委", "start": "", "end": "至今"},

    # 叶斯颖 - Organization Dept
    {"person_id": 6, "org_id": 6, "title": "古田县委常委、组织部部长", "start": "", "end": "至今"},
    {"person_id": 6, "org_id": 1, "title": "古田县委常委", "start": "", "end": "至今"},

    # 林晓晞 - Discipline Inspection
    {"person_id": 7, "org_id": 5, "title": "古田县委常委、纪委书记、县监委主任", "start": "", "end": "至今"},
    {"person_id": 7, "org_id": 1, "title": "古田县委常委", "start": "", "end": "至今"},

    # 黄建 - Political/Legal
    {"person_id": 8, "org_id": 8, "title": "古田县委常委、政法委书记", "start": "", "end": "至今"},
    {"person_id": 8, "org_id": 1, "title": "古田县委常委", "start": "", "end": "至今"},

    # 张明生 - Propaganda
    {"person_id": 9, "org_id": 7, "title": "古田县委常委、宣传部部长", "start": "", "end": "至今"},
    {"person_id": 9, "org_id": 1, "title": "古田县委常委", "start": "", "end": "至今"},

    # 李黄灼 - United Front
    {"person_id": 10, "org_id": 9, "title": "古田县委常委、统战部部长", "start": "", "end": "至今"},
    {"person_id": 10, "org_id": 1, "title": "古田县委常委", "start": "", "end": "至今"},

    # 刘荣 - Military
    {"person_id": 11, "org_id": 10, "title": "古田县委常委、县人武部政委", "start": "", "end": "至今"},
    {"person_id": 11, "org_id": 1, "title": "古田县委常委", "start": "", "end": "至今"},

    # 张沂 - Deputy Mayor
    {"person_id": 12, "org_id": 2, "title": "古田县人民政府副县长", "start": "", "end": "至今"},

    # 黄忠钦 - Deputy Mayor + Public Security
    {"person_id": 13, "org_id": 2, "title": "古田县人民政府副县长、公安局局长", "start": "", "end": "至今"},
    {"person_id": 13, "org_id": 11, "title": "古田县公安局局长", "start": "", "end": "至今"},

    # 雷毅 - Deputy Mayor
    {"person_id": 14, "org_id": 2, "title": "古田县人民政府副县长", "start": "", "end": "至今"},

    # 陈锐杰 - Deputy Mayor
    {"person_id": 15, "org_id": 2, "title": "古田县人民政府副县长", "start": "", "end": "至今"},

    # 李晓霞 - Science/Tech Deputy Mayor
    {"person_id": 16, "org_id": 2, "title": "古田县人民政府科技副县长", "start": "", "end": "至今"},

    # Predecessors
    {"person_id": 17, "org_id": 1, "title": "中共古田县委书记（原任）", "start": "2021-06", "end": "2025-04"},
    {"person_id": 17, "org_id": 14, "title": "宁德市人民政府副市长", "start": "2025-04", "end": "至今"},

    {"person_id": 18, "org_id": 1, "title": "中共古田县委书记（原任）", "start": "2020-12", "end": "2021-06"},
    {"person_id": 18, "org_id": 15, "title": "屏南县委书记", "start": "2021-06", "end": "至今"},
]

relationships = [
    # 许锋 ↔ 张成慧 (Predecessor-Successor at 古田县委书记)
    {"id": 1, "person_a_id": 1, "person_b_id": 17, "type": "predecessor_successor",
     "context": "许锋接替张成慧任古田县委书记", "overlap_org": "中共古田县委员会", "overlap_period": "2025-04"},

    # 张成慧 ↔ 党帅 (Predecessor-Successor at 古田县委书记)
    {"id": 2, "person_a_id": 17, "person_b_id": 18, "type": "predecessor_successor",
     "context": "张成慧接替党帅任古田县委书记", "overlap_org": "中共古田县委员会", "overlap_period": "2021-06"},

    # 许锋 ↔ 吴新情 (Party-Government 搭档)
    {"id": 3, "person_a_id": 1, "person_b_id": 2, "type": "superior_subordinate",
     "context": "许锋作为县委书记领导县长吴新情", "overlap_org": "中共古田县委员会", "overlap_period": "2025-04至今"},

    # 俞仰林 ↔ 许锋 (Standing Committee overlap)
    {"id": 4, "person_a_id": 5, "person_b_id": 1, "type": "overlap",
     "context": "县委常委班子共事", "overlap_org": "中共古田县委员会", "overlap_period": ""},

    # 叶斯颖 ↔ 许锋
    {"id": 5, "person_a_id": 6, "person_b_id": 1, "type": "overlap",
     "context": "县委常委班子共事", "overlap_org": "中共古田县委员会", "overlap_period": ""},

    # 林晓晞 ↔ 许锋
    {"id": 6, "person_a_id": 7, "person_b_id": 1, "type": "overlap",
     "context": "县委常委班子共事", "overlap_org": "中共古田县委员会", "overlap_period": ""},

    # 黄建 ↔ 许锋
    {"id": 7, "person_a_id": 8, "person_b_id": 1, "type": "overlap",
     "context": "县委常委班子共事", "overlap_org": "中共古田县委员会", "overlap_period": ""},

    # 张明生 ↔ 许锋
    {"id": 8, "person_a_id": 9, "person_b_id": 1, "type": "overlap",
     "context": "县委常委班子共事", "overlap_org": "中共古田县委员会", "overlap_period": ""},

    # 李黄灼 ↔ 许锋
    {"id": 9, "person_a_id": 10, "person_b_id": 1, "type": "overlap",
     "context": "县委常委班子共事", "overlap_org": "中共古田县委员会", "overlap_period": ""},

    # 刘荣 ↔ 许锋
    {"id": 10, "person_a_id": 11, "person_b_id": 1, "type": "overlap",
     "context": "县委常委班子共事", "overlap_org": "中共古田县委员会", "overlap_period": ""},

    # 俞仰林 ↔ 吴新情 (Government team)
    {"id": 11, "person_a_id": 5, "person_b_id": 2, "type": "overlap",
     "context": "县政府班子成员", "overlap_org": "古田县人民政府", "overlap_period": ""},

    # 张沂 ↔ 吴新情
    {"id": 12, "person_a_id": 12, "person_b_id": 2, "type": "overlap",
     "context": "县政府班子成员", "overlap_org": "古田县人民政府", "overlap_period": ""},

    # 黄忠钦 ↔ 吴新情
    {"id": 13, "person_a_id": 13, "person_b_id": 2, "type": "overlap",
     "context": "县政府班子成员", "overlap_org": "古田县人民政府", "overlap_period": ""},

    # 雷毅 ↔ 吴新情
    {"id": 14, "person_a_id": 14, "person_b_id": 2, "type": "overlap",
     "context": "县政府班子成员", "overlap_org": "古田县人民政府", "overlap_period": ""},

    # 陈锐杰 ↔ 吴新情
    {"id": 15, "person_a_id": 15, "person_b_id": 2, "type": "overlap",
     "context": "县政府班子成员", "overlap_org": "古田县人民政府", "overlap_period": ""},

    # 郑国淑 ↔ 许锋 (Four-bank leadership overlap)
    {"id": 16, "person_a_id": 3, "person_b_id": 1, "type": "overlap",
     "context": "县四套班子领导", "overlap_org": "古田县", "overlap_period": "2025-04至今"},

    # 林纪建 ↔ 许锋
    {"id": 17, "person_a_id": 4, "person_b_id": 1, "type": "overlap",
     "context": "县四套班子领导", "overlap_org": "古田县", "overlap_period": "2025-04至今"},
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
    elif p["id"] in [5, 6, 7, 8, 9, 10, 11]:
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
lines.append(f'    <description>古田县领导班子工作关系网络 - {today}</description>')
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
