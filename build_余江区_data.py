#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Yujiang District leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/jiangxi_余江区")
DB_PATH = os.path.join(STAGING, "余江区_network.db")
GEXF_PATH = os.path.join(STAGING, "余江区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Yujiang District Party Secretaries ──
    {"id": 1, "name": "罗卫国", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-09", "birthplace": "江西余江", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共鹰潭市余江区委书记", "current_org": "中共鹰潭市余江区委员会",
     "source": "https://baike.baidu.com/item/%E7%BD%97%E5%8D%AB%E5%9B%BD"},
    {"id": 2, "name": "刘颖豪", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "余江区人民政府区长", "current_org": "余江区人民政府",
     "source": "https://www.yujiang.gov.cn"},

    # ── Predecessors ──
    {"id": 3, "name": "苏建军", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-04", "birthplace": "江西贵溪", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "鹰潭市委常委、宣传部部长", "current_org": "中共鹰潭市委员会",
     "source": "https://baike.baidu.com/item/%E8%8B%8F%E5%BB%BA%E5%86%9B"},
    {"id": 4, "name": "路文革", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://baike.baidu.com/item/%E8%B7%AF%E6%96%87%E9%9D%A9"},

    # ── Key Deputies ──
    {"id": 5, "name": "潘炜", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "余江区委副书记", "current_org": "中共鹰潭市余江区委员会",
     "source": "https://www.yujiang.gov.cn"},
    {"id": 6, "name": "吴晓娟", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "余江区委常委、常务副区长", "current_org": "余江区人民政府",
     "source": "https://www.yujiang.gov.cn"},
    {"id": 7, "name": "刘绍安", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "余江区委常委、纪委书记、监委主任", "current_org": "中共鹰潭市余江区纪律检查委员会",
     "source": "https://www.yujiang.gov.cn"},
    {"id": 8, "name": "陈亮泉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "余江区委常委、组织部部长", "current_org": "中共鹰潭市余江区委员会",
     "source": "https://www.yujiang.gov.cn"},
    {"id": 9, "name": "毛伟卿", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "余江区委常委、宣传部部长", "current_org": "中共鹰潭市余江区委员会",
     "source": "https://www.yujiang.gov.cn"},
    {"id": 10, "name": "蔡立新", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "余江区委常委、政法委书记", "current_org": "中共鹰潭市余江区委员会",
     "source": "https://www.yujiang.gov.cn"},
    {"id": 11, "name": "张勇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "余江区委常委、统战部部长", "current_org": "中共鹰潭市余江区委员会",
     "source": "https://www.yujiang.gov.cn"},

    # ── Deputy District Mayors ──
    {"id": 12, "name": "张仔强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "余江区副区长、市公安局余江分局局长", "current_org": "余江区人民政府",
     "source": "https://www.yujiang.gov.cn"},
    {"id": 13, "name": "姜翠萍", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "余江区副区长", "current_org": "余江区人民政府",
     "source": "https://www.yujiang.gov.cn"},
    {"id": 14, "name": "王建生", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "余江区副区长", "current_org": "余江区人民政府",
     "source": "https://www.yujiang.gov.cn"},

    # ── Cross-County Network Figures ──
    {"id": 15, "name": "许南吉", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-12", "birthplace": "浙江慈溪", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "鹰潭市委书记", "current_org": "中共鹰潭市委员会",
     "source": "https://baike.baidu.com/item/%E8%AE%B8%E5%8D%97%E5%90%89"},
    {"id": 16, "name": "张子建", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-10", "birthplace": "江西贵溪", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "鹰潭市人民政府市长", "current_org": "鹰潭市人民政府",
     "source": "https://baike.baidu.com/item/%E5%BC%A0%E5%AD%90%E5%BB%BA"},
]

organizations = [
    {"id": 1, "name": "中共鹰潭市余江区委员会", "type": "党委", "level": "县处级", "parent": "中共鹰潭市委员会", "location": "江西鹰潭余江"},
    {"id": 2, "name": "余江区人民政府", "type": "政府", "level": "县处级", "parent": "鹰潭市人民政府", "location": "江西鹰潭余江"},
    {"id": 3, "name": "中共鹰潭市余江区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共鹰潭市纪律检查委员会", "location": "江西鹰潭余江"},
    {"id": 4, "name": "鹰潭市公安局余江分局", "type": "政府", "level": "乡科级", "parent": "鹰潭市公安局", "location": "江西鹰潭余江"},
    {"id": 5, "name": "中共鹰潭市委员会", "type": "党委", "level": "厅级", "parent": "中共江西省委", "location": "江西鹰潭"},
    {"id": 6, "name": "鹰潭市人民政府", "type": "政府", "level": "厅级", "parent": "江西省人民政府", "location": "江西鹰潭"},
    {"id": 7, "name": "中共鹰潭市委宣传部", "type": "党委部门", "level": "县处级", "parent": "中共鹰潭市委员会", "location": "江西鹰潭"},
]

positions = [
    # ── Luo Weiguo (罗卫国) career ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共鹰潭市余江区委书记", "start": "2020", "end": "", "rank": "县处级正职", "note": "现任"},
    {"id": 2, "person_id": 1, "org_id": 2, "title": "余江区人民政府区长", "start": "2016", "end": "2020", "rank": "县处级正职", "note": "前任职务"},
    {"id": 3, "person_id": 1, "org_id": 1, "title": "余江区委副书记", "start": "2016", "end": "2020", "rank": "县处级副职", "note": ""},

    # ── Liu Yinghao (刘颖豪) career ──
    {"id": 4, "person_id": 2, "org_id": 2, "title": "余江区人民政府区长", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},
    {"id": 5, "person_id": 2, "org_id": 1, "title": "余江区委副书记", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # ── Su Jianjun (苏建军) career ──
    {"id": 6, "person_id": 3, "org_id": 1, "title": "中共余江县委书记/区委书记", "start": "2016", "end": "2020", "rank": "县处级正职", "note": "余江撤县设区前后"},
    {"id": 7, "person_id": 3, "org_id": 5, "title": "鹰潭市委常委、宣传部部长", "start": "2020", "end": "", "rank": "副厅级", "note": "现任"},

    # ── Lu Wenge (路文革) career ──
    {"id": 8, "person_id": 4, "org_id": 1, "title": "中共余江县委书记", "start": "2014", "end": "2016", "rank": "县处级正职", "note": ""},

    # ── Key Deputies ──
    {"id": 9, "person_id": 5, "org_id": 1, "title": "余江区委副书记", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 10, "person_id": 6, "org_id": 2, "title": "余江区委常委、常务副区长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 11, "person_id": 7, "org_id": 3, "title": "余江区委常委、纪委书记、监委主任", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 12, "person_id": 8, "org_id": 1, "title": "余江区委常委、组织部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 13, "person_id": 9, "org_id": 1, "title": "余江区委常委、宣传部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 14, "person_id": 10, "org_id": 1, "title": "余江区委常委、政法委书记", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 15, "person_id": 11, "org_id": 1, "title": "余江区委常委、统战部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Deputy Mayors ──
    {"id": 16, "person_id": 12, "org_id": 2, "title": "余江区副区长、市公安局余江分局局长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 17, "person_id": 13, "org_id": 2, "title": "余江区副区长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 18, "person_id": 14, "org_id": 2, "title": "余江区副区长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── City Level Leaders ──
    {"id": 19, "person_id": 15, "org_id": 5, "title": "中共鹰潭市委书记", "start": "2021", "end": "", "rank": "厅级", "note": "现任"},
    {"id": 20, "person_id": 16, "org_id": 6, "title": "鹰潭市人民政府市长", "start": "2021", "end": "", "rank": "厅级", "note": "现任"},
]

relationships = [
    # ── Predecessor-Successor ──
    {"id": 1, "person_a_id": 1, "person_b_id": 3, "type": "交接", "context": "苏建军→罗卫国 余江区委书记交接（2020年）", "overlap_org": "中共鹰潭市余江区委员会", "overlap_period": "2020"},
    {"id": 2, "person_a_id": 3, "person_b_id": 4, "type": "交接", "context": "路文革→苏建军 余江县委书记交接（2016年）", "overlap_org": "中共余江县委员会", "overlap_period": "2016"},

    # ── Current Party Secretary and District Mayor pair ──
    {"id": 3, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档", "context": "罗卫国（区委书记）与刘颖豪（区长）党政搭档", "overlap_org": "余江区人民政府", "overlap_period": ""},
    {"id": 4, "person_a_id": 1, "person_b_id": 5, "type": "上下级", "context": "罗卫国与潘炜为书记-副书记关系", "overlap_org": "中共鹰潭市余江区委员会", "overlap_period": ""},

    # ── Predecessor promotion trajectory ──
    {"id": 5, "person_a_id": 3, "person_b_id": 7, "type": "上下级", "context": "苏建军从余江区委书记升任鹰潭市委常委、宣传部部长", "overlap_org": "中共鹰潭市委员会", "overlap_period": "2020"},

    # ── City Leaders overseeing Yujiang ──
    {"id": 6, "person_a_id": 15, "person_b_id": 1, "type": "上下级", "context": "许南吉（鹰潭市委书记）是罗卫国的直接上级", "overlap_org": "中共鹰潭市委员会", "overlap_period": "2021-"},
    {"id": 7, "person_a_id": 16, "person_b_id": 2, "type": "上下级", "context": "张子建（鹰潭市长）是刘颖豪的直接上级", "overlap_org": "鹰潭市人民政府", "overlap_period": "2021-"},

    # ── Committee Standing Members ──
    {"id": 8, "person_a_id": 8, "person_b_id": 9, "type": "同僚", "context": "陈亮泉（组织部）与毛伟卿（宣传部）均为区委常委", "overlap_org": "中共鹰潭市余江区委员会", "overlap_period": ""},
    {"id": 9, "person_a_id": 10, "person_b_id": 11, "type": "同僚", "context": "蔡立新（政法委）与张勇（统战部）均为区委常委", "overlap_org": "中共鹰潭市余江区委员会", "overlap_period": ""},

    # ── Guixi connection ──
    {"id": 10, "person_a_id": 3, "person_b_id": 16, "type": "同乡", "context": "苏建军和张子建均为贵溪籍贯", "overlap_org": "", "overlap_period": ""},

    # ── Luo Weiguo's earlier role overlaps ──
    {"id": 11, "person_a_id": 1, "person_b_id": 5, "type": "同僚", "context": "罗卫国与潘炜曾同在区委班子共事", "overlap_org": "中共鹰潭市余江区委员会", "overlap_period": ""},
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


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return viz:color R,G,B string based on role."""
    # Party Secretary (区委书记) - Red
    if "区委书记" in (p["current_post"] or ""):
        return (255, 50, 50)
    # Government Leader (区长) - Blue
    if "区长" in (p["current_post"] or "") and "副" not in p.get("current_post", ""):
        return (50, 100, 255)
    # Discipline Inspection (纪委书记) - Orange
    if "纪委书记" in (p["current_post"] or "") or "监委" in (p["current_post"] or ""):
        return (255, 165, 0)
    # Predecessors who are now city-level leaders
    if p["id"] in [3, 15, 16]:
        return (50, 100, 255)
    # Others - Grey
    return (100, 100, 100)


def person_size(p):
    if p["id"] in [1, 2, 15, 16]:
        return 20.0  # Top leaders
    return 12.0  # Other persons


def org_color(o):
    colors = {
        "党委": (255, 200, 200),  # Pink
        "政府": (200, 200, 255),  # Light blue
        "纪委": (255, 200, 200),  # Pink (same as 党委)
        "党委部门": (255, 200, 200),  # Pink
    }
    return colors.get(o["type"], (200, 200, 200))


lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>鹰潭市余江区领导班子工作关系网络 - {today}</description>')
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
    r, g, b = person_color(p)
    sz = person_size(p)
    lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{esc(p["birth"])}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{esc(p["birthplace"])}"/>')
    lines.append(f'          <attvalue for="education" value="{esc(p["education"])}"/>')
    lines.append(f'          <attvalue for="current_post" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="source" value="{esc(p["source"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append(f'      </node>')

# ── Nodes: Organizations ──
for o in organizations:
    oid = 1000 + o["id"]
    r, g, b = org_color(o)
    lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{esc(o["type"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
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
    lines.append(f'          <attvalue for="period" value="{pos["start"] or "?"} → {pos["end"] or "今"}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

# person↔person (relationships)
for r in relationships:
    lines.append(f'      <edge id="{edge_id}" source="{r["person_a_id"]}" target="{r["person_b_id"]}" label="{esc(r["type"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="context" value="{esc(r["context"])}"/>')
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
