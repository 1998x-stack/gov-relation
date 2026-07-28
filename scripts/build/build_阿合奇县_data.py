#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 阿合奇县 (Aheqi County) leadership network."""

import sqlite3
import os
from datetime import datetime

STAGING = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(STAGING, "..", ".."))
DB_PATH = os.path.join(STAGING, "阿合奇县_network.db")
GEXF_PATH = os.path.join(STAGING, "阿合奇县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── County Government Leaders (confirmed from official site) ──
    {"id": 1, "name": "阿不都瓦力·阿山拜克", "gender": "男", "ethnicity": "柯尔克孜族",
     "birth": "1985-01", "birthplace": "新疆乌恰", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阿合奇县委副书记、代理县长", "current_org": "阿合奇县人民政府",
     "source": "https://www.xjahq.gov.cn/xjahq/c103565/202109/3f2b4bdd940d46678ed3f35e86cdcb7c.shtml"},
    {"id": 2, "name": "周明来", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-11", "birthplace": "河南南阳", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、常务副县长", "current_org": "阿合奇县人民政府",
     "source": "https://www.xjahq.gov.cn/xjahq/c103566/202503/7fc2f1731f22469eb7e1cb19039eb368.shtml"},
    {"id": 3, "name": "宁海平", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "阿合奇县人民政府",
     "source": "https://www.xjahq.gov.cn/xjahq/c103567/202203/7c7c5f98e226405b86fb0fb96e53fa66.shtml"},
    {"id": 4, "name": "阿里木汗·买买提肉孜", "gender": "女", "ethnicity": "柯尔克孜族",
     "birth": "1981-01", "birthplace": "新疆阿合奇", "education": "大学本科学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "阿合奇县人民政府",
     "source": "https://www.xjahq.gov.cn/xjahq/c103567/202501/93a8052921674d6caf409b9a8584cde5.shtml"},
    {"id": 5, "name": "陈龙", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-09", "birthplace": "", "education": "大学本科学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "阿合奇县人民政府",
     "source": "https://www.xjahq.gov.cn/xjahq/c103567/202403/feae1a1904c04517bff1ef751a944053.shtml"},
    {"id": 6, "name": "孟欣", "gender": "男", "ethnicity": "汉族",
     "birth": "1988-02", "birthplace": "甘肃武威", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副县长、县公安局党委书记、局长", "current_org": "阿合奇县人民政府",
     "source": "https://www.xjahq.gov.cn/xjahq/c103567/202109/0068324453dd4fcca28bed5cec654c02.shtml"},
    {"id": 7, "name": "王军见", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "阿合奇县人民政府",
     "source": "https://www.xjahq.gov.cn/xjahq/c103567/202510/a8f2f17837014d75a500b272703fd6b2.shtml"},
    {"id": 8, "name": "孙宇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "阿合奇县人民政府",
     "source": "https://www.xjahq.gov.cn/xjahq/c103567/202605/e1a22e9324e44d97b283ea1a545ed9d5.shtml"},
    {"id": 9, "name": "王进", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "阿合奇县人民政府",
     "source": "https://www.xjahq.gov.cn/xjahq/c103567/202605/e46b26568eef4f03a53e4f20f62dd505.shtml"},
    {"id": 10, "name": "巴合提牙尔·克热木", "gender": "男", "ethnicity": "柯尔克孜族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "阿合奇县人民政府",
     "source": "https://www.xjahq.gov.cn/xjahq/c103567/202605/dbaf45b2b1ef4c4eac37b42f5ff7dc69.shtml"},
]

organizations = [
    {"id": 1, "name": "中共阿合奇县委员会", "type": "党委", "level": "县处级", "parent": "中共克孜勒苏柯尔克孜自治州委员会", "location": "新疆克州阿合奇"},
    {"id": 2, "name": "阿合奇县人民政府", "type": "政府", "level": "县处级", "parent": "克孜勒苏柯尔克孜自治州人民政府", "location": "新疆克州阿合奇"},
    {"id": 3, "name": "阿合奇县公安局", "type": "政府", "level": "正科级", "parent": "阿合奇县人民政府", "location": "新疆克州阿合奇"},
    {"id": 4, "name": "克孜勒苏柯尔克孜自治州工业和信息化局", "type": "政府", "level": "县处级", "parent": "克州人民政府", "location": "新疆克州"},
    {"id": 5, "name": "中共阿克陶县委员会", "type": "党委", "level": "县处级", "parent": "中共克州委员会", "location": "新疆克州阿克陶"},
    {"id": 6, "name": "乌恰县工商局", "type": "政府", "level": "正科级", "parent": "乌恰县人民政府", "location": "新疆克州乌恰"},
    {"id": 7, "name": "乌恰县委政法委", "type": "党委部门", "level": "正科级", "parent": "中共乌恰县委员会", "location": "新疆克州乌恰"},
    {"id": 8, "name": "乌恰县团委", "type": "群团", "level": "正科级", "parent": "共青团乌恰县委员会", "location": "新疆克州乌恰"},
    {"id": 9, "name": "乌恰县委宣传部", "type": "党委部门", "level": "正科级", "parent": "中共乌恰县委员会", "location": "新疆克州乌恰"},
    {"id": 10, "name": "克州公安局", "type": "政府", "level": "县处级", "parent": "克州人民政府", "location": "新疆克州"},
    {"id": 11, "name": "克州交通建设投资有限责任公司", "type": "国有企业", "level": "县处级", "parent": "克州人民政府", "location": "新疆克州"},
    {"id": 12, "name": "阿图什市交通运输局", "type": "政府", "level": "正科级", "parent": "阿图什市人民政府", "location": "新疆克州阿图什"},
    {"id": 13, "name": "色帕巴依乡人民政府", "type": "政府", "level": "乡科级", "parent": "阿合奇县人民政府", "location": "新疆克州阿合奇"},
    {"id": 14, "name": "新疆北阿铁路有限责任公司", "type": "国有企业", "level": "", "parent": "", "location": "新疆"},
    {"id": 15, "name": "自治区文化和旅游厅", "type": "政府", "level": "厅级", "parent": "新疆维吾尔自治区人民政府", "location": "新疆乌鲁木齐"},
]

positions = [
    # 阿不都瓦力·阿山拜克 - County Mayor (acting)
    {"id": 1, "person_id": 1, "org_id": 2, "title": "县委副书记、代理县长", "start": "", "end": "", "rank": "县处级正职", "note": "现任（代理）"},
    {"id": 2, "person_id": 1, "org_id": 4, "title": "克州工信局党组副书记、局长", "start": "", "end": "", "rank": "县处级正职", "note": "此前职务"},
    {"id": 3, "person_id": 1, "org_id": 5, "title": "阿克陶县委常委", "start": "", "end": "", "rank": "县处级副职", "note": "此前职务"},
    {"id": 4, "person_id": 1, "org_id": 9, "title": "乌恰县委宣传部副部长", "start": "", "end": "", "rank": "正科级", "note": ""},
    {"id": 5, "person_id": 1, "org_id": 8, "title": "乌恰县团委书记", "start": "", "end": "", "rank": "正科级", "note": ""},
    {"id": 6, "person_id": 1, "org_id": 7, "title": "乌恰县委政法委副书记", "start": "", "end": "", "rank": "副科级", "note": ""},
    {"id": 7, "person_id": 1, "org_id": 6, "title": "乌恰县工商局党组成员、副局长", "start": "", "end": "", "rank": "副科级", "note": ""},

    # 周明来 - Executive Deputy Mayor
    {"id": 8, "person_id": 2, "org_id": 2, "title": "县委常委、常务副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 9, "person_id": 2, "org_id": 12, "title": "阿图什市交通运输局党组书记、副局长", "start": "", "end": "", "rank": "正科级", "note": ""},
    {"id": 10, "person_id": 2, "org_id": 11, "title": "克州交通建设投资有限责任公司总经理", "start": "", "end": "", "rank": "", "note": ""},
    {"id": 11, "person_id": 2, "org_id": 11, "title": "克州交通建设投资有限责任公司董事长", "start": "", "end": "", "rank": "", "note": ""},

    # 宁海平 — Deputy Mayor
    {"id": 12, "person_id": 3, "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # 阿里木汗·买买提肉孜 — Deputy Mayor
    {"id": 13, "person_id": 4, "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 14, "person_id": 4, "org_id": 13, "title": "色帕巴依乡党委副书记、乡长", "start": "", "end": "", "rank": "正科级", "note": ""},

    # 陈龙 — Deputy Mayor
    {"id": 15, "person_id": 5, "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 16, "person_id": 5, "org_id": 15, "title": "自治区文旅厅艺术处四级调研员", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"id": 17, "person_id": 5, "org_id": 15, "title": "自治区文旅厅艺术处一级主任科员", "start": "", "end": "", "rank": "正科级", "note": ""},
    {"id": 18, "person_id": 5, "org_id": 14, "title": "新疆北阿铁路公司安质部副部长", "start": "", "end": "", "rank": "", "note": ""},

    # 孟欣 — Deputy Mayor + Police
    {"id": 19, "person_id": 6, "org_id": 2, "title": "副县长、县公安局党委书记、局长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 20, "person_id": 6, "org_id": 10, "title": "克州公安局警令部副主任", "start": "", "end": "", "rank": "副科级", "note": ""},
    {"id": 21, "person_id": 6, "org_id": 10, "title": "克州公安局政治部综合科科长", "start": "", "end": "", "rank": "正科级", "note": ""},

    # 王军见 — Deputy Mayor
    {"id": 22, "person_id": 7, "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # 孙宇 — Deputy Mayor
    {"id": 23, "person_id": 8, "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # 王进 — Deputy Mayor
    {"id": 24, "person_id": 9, "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # 巴合提牙尔·克热木 — Deputy Mayor
    {"id": 25, "person_id": 10, "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
]

relationships = [
    # Coworker relationships
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档", "context": "周明来任常务副县长协助县长阿不都瓦力·阿山拜克工作", "overlap_org": "阿合奇县人民政府", "overlap_period": "现任"},
    {"id": 2, "person_a_id": 1, "person_b_id": 7, "type": "跨县前同事", "context": "阿不都瓦力·阿山拜克曾任乌恰县委宣传部副部长、团委书记、政法委副书记等，在乌恰县有早年履历", "overlap_org": "乌恰县", "overlap_period": ""},

    # Cross-county flow
    {"id": 3, "person_a_id": 1, "person_b_id": 5, "type": "跨县调动", "context": "阿不都瓦力·阿山拜克曾任克州工信局长、阿克陶县委常委，在克州范围内任职", "overlap_org": "克州", "overlap_period": ""},
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

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

today = datetime.now().strftime("%Y-%m-%d")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>China-gov-network skill</creator>')
lines.append(f'    <description>阿合奇县领导班子工作关系网络 - {today}</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="category" type="string"/>')
lines.append('      <attribute id="2" title="birth" type="string"/>')
lines.append('      <attribute id="3" title="birthplace" type="string"/>')
lines.append('      <attribute id="4" title="education" type="string"/>')
lines.append('      <attribute id="5" title="current_post" type="string"/>')
lines.append('      <attribute id="6" title="source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('      <attribute id="2" title="period" type="string"/>')
lines.append('    </attributes>')

# Nodes: Persons
lines.append('    <nodes>')
for p in persons:
    pid = p["id"]
    # Color by role
    if p["id"] == 1:
        # 代理县长 (acting mayor) - blue for government leader
        c = "50,100,255"
        sz = "20.0"
    else:
        c = "100,100,100"
        sz = "12.0"

    lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="人物"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p["birth"])}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(p["birthplace"])}"/>')
    lines.append(f'          <attvalue for="4" value="{esc(p["education"])}"/>')
    lines.append(f'          <attvalue for="5" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="6" value="{esc(p["source"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Nodes: Organizations
for o in organizations:
    oid = 1000 + o["id"]
    lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="org"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="200" g="200" b="200"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
eid = 1

# person→organization (worked_at)
for pos in positions:
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
    lines.append(f'          <attvalue for="2" value="{pos["start"] or "?"} → {pos["end"] or "今"}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
    eid += 1

# person↔person (relationships), weight="2.0"
for r in relationships:
    lines.append(f'      <edge id="{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
    lines.append(f'          <attvalue for="2" value="{r["overlap_period"]}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
    eid += 1

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