#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 汾西县 leadership network.

汾西县位于山西省中南部，临汾市北部，吕梁山南麓。
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DB_PATH = os.path.join(BASE, "data/tmp/shanxi_汾西县/汾西县_network.db")
GEXF_PATH = os.path.join(BASE, "data/tmp/shanxi_汾西县/汾西县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Party Secretary (县委书记) ──
    {"id": 1, "name": "安海清", "gender": "男", "ethnicity": "汉族",
     "birth": "1971", "birthplace": "山西省高平市", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "中共汾西县委书记", "current_org": "中共汾西县委员会",
     "source": "https://www.sohu.com/a/1031789298_121430044"},

    # ── County Mayor (县长) ──
    {"id": 2, "name": "霍俊波", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-05", "birthplace": "山西省", "education": "研究生",
     "party_join": "", "work_start": "",
     "current_post": "汾西县委副书记、县长", "current_org": "汾西县人民政府",
     "source": "http://www.fenxi.gov.cn/contents/9166/995.html"},

    # ── Executive Deputy Mayor (常务副县长) ──
    {"id": 3, "name": "卢燕飞", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-03", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "汾西县委常委、常务副县长", "current_org": "汾西县人民政府",
     "source": "http://www.fenxi.gov.cn/contents/9167/1001.html"},

    # ── Organization Department Head (组织部部长) ──
    {"id": 4, "name": "景星", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "山西省", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "汾西县委常委、组织部部长", "current_org": "中共汾西县委组织部",
     "source": "http://www.fenxi.gov.cn/"},

    # ── Deputy Mayor & Public Security Chief ──
    {"id": 5, "name": "刘勇辉", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-09", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "汾西县副县长、公安局局长", "current_org": "汾西县人民政府",
     "source": "http://www.fenxi.gov.cn/"},

    # ── Deputy Mayor (副县长) ──
    {"id": 6, "name": "周锁龙", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-02", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "汾西县副县长", "current_org": "汾西县人民政府",
     "source": "http://www.fenxi.gov.cn/"},

    # ── Predecessor 1: 王林波 ──
    {"id": 7, "name": "王林波", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "山西省", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "襄汾县委书记", "current_org": "中共襄汾县委员会",
     "source": "https://www.sohu.com/a/1031789298_121430044"},

    # ── Predecessor 2: 张安文 ──
    {"id": 8, "name": "张安文", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "山西省", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "（原汾西县委书记，已调离）", "current_org": "",
     "source": ""},

    # ── Predecessor 3: 任天顺 ──
    {"id": 9, "name": "任天顺", "gender": "男", "ethnicity": "汉族",
     "birth": "1963-01", "birthplace": "山西省", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "临汾市人大常委会副主任", "current_org": "临汾市人大常委会",
     "source": ""},

    # ── Predecessor 4: 张德英 (disgraced) ──
    {"id": 10, "name": "张德英", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "山西省", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "（已被查处）", "current_org": "",
     "source": ""},

    # ── 陈宇芳 (县委领导) ──
    {"id": 11, "name": "陈宇芳", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "山西省", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "汾西县领导", "current_org": "汾西县人民政府",
     "source": "http://www.fenxi.gov.cn/"},

    # ── 王瑞 (前副书记，已调离) ──
    {"id": 12, "name": "王瑞", "gender": "女", "ethnicity": "汉族",
     "birth": "1980-11", "birthplace": "山西省", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "原汾西县委副书记（调任市直正处级）", "current_org": "",
     "source": ""},

    # ── Predecessor officials for reference ──
    {"id": 13, "name": "郑相如", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "山西省", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "原汾西县副县长、公安局局长（已调离）", "current_org": "",
     "source": "http://www.fenxi.gov.cn/"},

    {"id": 14, "name": "郭凯", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "山西省", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "原汾西县副县长（已调离）", "current_org": "",
     "source": "http://www.fenxi.gov.cn/"},
]

organizations = [
    {"id": 1, "name": "中共汾西县委员会", "type": "党委", "level": "县处级", "parent": "中共临汾市委员会", "location": "山西省临汾市汾西县"},
    {"id": 2, "name": "汾西县人民政府", "type": "政府", "level": "县处级", "parent": "临汾市人民政府", "location": "山西省临汾市汾西县"},
    {"id": 3, "name": "中共汾西县委组织部", "type": "党委部门", "level": "正科级", "parent": "中共汾西县委员会", "location": "山西省临汾市汾西县"},
    {"id": 4, "name": "中共临汾市委员会", "type": "党委", "level": "地厅级", "parent": "中共山西省委", "location": "山西省临汾市"},
    {"id": 5, "name": "临汾市人民政府", "type": "政府", "level": "地厅级", "parent": "山西省人民政府", "location": "山西省临汾市"},
    {"id": 6, "name": "临汾市人大常委会", "type": "人大", "level": "地厅级", "parent": "", "location": "山西省临汾市"},
    {"id": 7, "name": "中共襄汾县委员会", "type": "党委", "level": "县处级", "parent": "中共临汾市委员会", "location": "山西省临汾市襄汾县"},
    {"id": 8, "name": "中共古县委员会", "type": "党委", "level": "县处级", "parent": "中共临汾市委员会", "location": "山西省临汾市古县"},
    {"id": 9, "name": "中共安泽县委员会", "type": "党委", "level": "县处级", "parent": "中共临汾市委员会", "location": "山西省临汾市安泽县"},
    {"id": 10, "name": "中共临汾市纪律检查委员会", "type": "纪委", "level": "地厅级", "parent": "中共临汾市委员会", "location": "山西省临汾市"},
]

positions = [
    # Current roles
    {"person_id": 1, "org_id": 1, "title": "汾西县委书记", "start_date": "2026-06", "end_date": "present", "rank": "正处级", "note": "2026年6月2日上任，接替王林波"},
    {"person_id": 2, "org_id": 2, "title": "汾西县委副书记、县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "至少从2021年起任县长"},
    {"person_id": 3, "org_id": 2, "title": "汾西县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "汾西县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "汾西县副县长、公安局局长", "start_date": "2025-10", "end_date": "present", "rank": "副处级", "note": "接替郑相如"},
    {"person_id": 6, "org_id": 2, "title": "汾西县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼财政局局长"},
    {"person_id": 11, "org_id": 2, "title": "汾西县领导", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # 安海清 past roles
    {"person_id": 1, "org_id": 8, "title": "古县县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "安泽县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "临汾市纪委常委", "start_date": "", "end_date": "2021-01", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 4, "title": "临汾市委副秘书长、办公室主任", "start_date": "2021-01", "end_date": "2026-06", "rank": "正处级", "note": "主持日常工作"},

    # Predecessors
    {"person_id": 7, "org_id": 1, "title": "汾西县委书记", "start_date": "", "end_date": "2026-06", "rank": "正处级", "note": "前任县委书记"},
    {"person_id": 7, "org_id": 7, "title": "襄汾县委书记", "start_date": "2026-06", "end_date": "present", "rank": "正处级", "note": "现任"},
    {"person_id": 8, "org_id": 1, "title": "汾西县委书记", "start_date": "2021-03", "end_date": "", "rank": "正处级", "note": "前任（从县长升任）"},
    {"person_id": 8, "org_id": 2, "title": "汾西县县长", "start_date": "", "end_date": "2021-03", "rank": "正处级", "note": "升任书记"},
    {"person_id": 9, "org_id": 1, "title": "汾西县委书记", "start_date": "", "end_date": "2021-03", "rank": "正处级", "note": "前任"},
    {"person_id": 9, "org_id": 6, "title": "临汾市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "现任"},
    {"person_id": 10, "org_id": 1, "title": "汾西县委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "前任，后被翼城县委书记，被查处"},

    # 王瑞
    {"person_id": 12, "org_id": 1, "title": "汾西县委副书记", "start_date": "", "end_date": "2026-01", "rank": "副处级", "note": "调任市直正处级"},

    # Former deputies
    {"person_id": 13, "org_id": 2, "title": "汾西县副县长、公安局局长", "start_date": "", "end_date": "2025-10", "rank": "副处级", "note": "被刘勇辉接替"},
    {"person_id": 14, "org_id": 2, "title": "汾西县副县长", "start_date": "", "end_date": "2023-12", "rank": "副处级", "note": "调离"},
]

relationships = [
    # Current top leaders
    {"person_a": 1, "person_b": 2, "type": "党政一把手共事", "context": "县委书记与县长搭班子", "overlap_org": "汾西县", "overlap_period": "2026-06至今"},
    {"person_a": 1, "person_b": 7, "type": "前后任", "context": "安海清接替王林波任县委书记", "overlap_org": "中共汾西县委员会", "overlap_period": "2026-06"},
    {"person_a": 7, "person_b": 8, "type": "前后任", "context": "王林波接替张安文", "overlap_org": "中共汾西县委员会", "overlap_period": ""},
    {"person_a": 8, "person_b": 9, "type": "前后任", "context": "张安文接替任天顺", "overlap_org": "中共汾西县委员会", "overlap_period": "2021-03"},
    {"person_a": 9, "person_b": 10, "type": "前后任", "context": "任天顺接替张德英", "overlap_org": "中共汾西县委员会", "overlap_period": ""},

    # County government teamwork
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记与常务副县长", "overlap_org": "汾西县", "overlap_period": "2026-06至今"},
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "县长与常务副县长", "overlap_org": "汾西县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "县长与公安局长", "overlap_org": "汾西县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "县长与副县长", "overlap_org": "汾西县人民政府", "overlap_period": ""},

    # Cross-county
    {"person_a": 1, "person_b": 8, "type": "同系统", "context": "安海清曾在古县任组织部长，张安文曾任汾西县长", "overlap_org": "临汾市", "overlap_period": ""},
    {"person_a": 13, "person_b": 5, "type": "前后任", "context": "郑相如被刘勇辉接替公安局长职位", "overlap_org": "汾西县人民政府", "overlap_period": "2025-10"},

    # 安海清和旧同事
    {"person_a": 1, "person_b": 9, "type": "上下级系统", "context": "安海清曾任临汾市纪委常委，任天顺曾任汾西县委书记", "overlap_org": "临汾市", "overlap_period": ""},

    # 王瑞调离
    {"person_a": 12, "person_b": 1, "type": "上下级", "context": "王瑞曾任汾西县委副书记，安海清上任后调离", "overlap_org": "中共汾西县委员会", "overlap_period": "2026-01"},
]

# ── BUILD ────────────────────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

# Database
conn = sqlite3.connect(DB_PATH)
conn.executescript("""
    DROP TABLE IF EXISTS relationships;
    DROP TABLE IF EXISTS positions;
    DROP TABLE IF EXISTS organizations;
    DROP TABLE IF EXISTS persons;

    CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        gender TEXT DEFAULT '',
        ethnicity TEXT DEFAULT '',
        birth TEXT DEFAULT '',
        birthplace TEXT DEFAULT '',
        education TEXT DEFAULT '',
        party_join TEXT DEFAULT '',
        work_start TEXT DEFAULT '',
        current_post TEXT DEFAULT '',
        current_org TEXT DEFAULT '',
        source TEXT DEFAULT ''
    );

    CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT DEFAULT '',
        level TEXT DEFAULT '',
        parent TEXT DEFAULT '',
        location TEXT DEFAULT ''
    );

    CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER NOT NULL,
        org_id INTEGER NOT NULL,
        title TEXT DEFAULT '',
        start_date TEXT DEFAULT '',
        end_date TEXT DEFAULT '',
        rank TEXT DEFAULT '',
        note TEXT DEFAULT '',
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );

    CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER NOT NULL,
        person_b INTEGER NOT NULL,
        type TEXT DEFAULT '',
        context TEXT DEFAULT '',
        overlap_org TEXT DEFAULT '',
        overlap_period TEXT DEFAULT '',
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    );
""")

for p in persons:
    conn.execute(
        "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, "
        "party_join, work_start, current_post, current_org, source) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
         p["education"], p["party_join"], p["work_start"], p["current_post"],
         p["current_org"], p["source"])
    )

for o in organizations:
    conn.execute(
        "INSERT INTO organizations (id, name, type, level, parent, location) "
        "VALUES (?,?,?,?,?,?)",
        (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
    )

for pos in positions:
    conn.execute(
        "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) "
        "VALUES (?,?,?,?,?,?,?)",
        (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"],
         pos["end_date"], pos["rank"], pos["note"])
    )

for r in relationships:
    conn.execute(
        "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) "
        "VALUES (?,?,?,?,?,?)",
        (r["person_a"], r["person_b"], r["type"], r["context"],
         r["overlap_org"], r["overlap_period"])
    )

conn.commit()
conn.close()

print(f"Database written: {DB_PATH}")
print(f"  Persons: {len(persons)}")
print(f"  Organizations: {len(organizations)}")
print(f"  Positions: {len(positions)}")
print(f"  Relationships: {len(relationships)}")

# ── GEXF ─────────────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(current_post):
    if "书记" in current_post and "纪委" not in current_post:
        return (255, 50, 50)
    elif "县长" in current_post or "副县长" in current_post:
        return (50, 100, 255)
    elif "人大" in current_post:
        return (200, 255, 255)
    else:
        return (100, 100, 100)

def person_size(current_post):
    if "县委书记" in current_post:
        return 20.0
    elif "县长" in current_post:
        return 18.0
    elif "原" in current_post or "已" in current_post:
        return 10.0
    else:
        return 12.0

def org_color(org_type):
    colors = {
        "党委": (255, 200, 200),
        "政府": (200, 200, 255),
        "纪委": (255, 165, 0),
        "人大": (200, 255, 255),
        "党委部门": (255, 220, 220),
    }
    return colors.get(org_type, (200, 200, 200))

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>汾西县领导班子工作关系网络图</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="current_post" type="string"/>')
lines.append('      <attribute id="2" title="current_org" type="string"/>')
lines.append('      <attribute id="3" title="birth" type="string"/>')
lines.append('      <attribute id="4" title="birthplace" type="string"/>')
lines.append('      <attribute id="5" title="education" type="string"/>')
lines.append('      <attribute id="6" title="source" type="string"/>')
lines.append('      <attribute id="7" title="org_type" type="string"/>')
lines.append('      <attribute id="8" title="level" type="string"/>')
lines.append('      <attribute id="9" title="location" type="string"/>')
lines.append('    </attributes>')

lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('      <attribute id="2" title="period" type="string"/>')
lines.append('    </attributes>')

# Nodes: Persons
lines.append('    <nodes>')
for p in persons:
    c = person_color(p["current_post"])
    sz = person_size(p["current_post"])
    lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
    lines.append(f'          <attvalue for="4" value="{esc(p["birthplace"])}"/>')
    lines.append(f'          <attvalue for="5" value="{esc(p["education"])}"/>')
    lines.append(f'          <attvalue for="6" value="{esc(p["source"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Nodes: Organizations
for o in organizations:
    oid = 1000 + o["id"]
    c = org_color(o["type"])
    lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="org"/>')
    lines.append(f'          <attvalue for="7" value="{esc(o["type"])}"/>')
    lines.append(f'          <attvalue for="8" value="{esc(o["level"])}"/>')
    lines.append(f'          <attvalue for="9" value="{esc(o["location"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')

lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
edge_id = 1
for pos in positions:
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="{edge_id}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
    lines.append(f'          <attvalue for="2" value="{pos["start_date"] or "?"} → {pos["end_date"] or "今"}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
    edge_id += 1

for r in relationships:
    lines.append(f'      <edge id="{edge_id}" source="{r["person_a"]}" target="{r["person_b"]}" label="{esc(r["type"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
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