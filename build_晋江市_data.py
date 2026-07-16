#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Jinjiang City leadership network.

晋江市——福建省泉州市下辖县级市，全国百强县前列，著名侨乡。
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/fujian_晋江市")
DB_PATH = os.path.join(STAGING, "晋江市_network.db")
GEXF_PATH = os.path.join(STAGING, "晋江市_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Jinjiang City Party Secretaries ──
    {"id": 1, "name": "王明元", "gender": "男", "ethnicity": "汉族",
     "birth": "1975年11月", "birthplace": "福建省泉州市鲤城区", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共晋江市委书记", "current_org": "中共晋江市委员会",
     "source": "https://www.jinjiang.gov.cn/"},

    # ── Current Jinjiang City Government Leaders ──
    {"id": 2, "name": "王小阳", "gender": "男", "ethnicity": "汉族",
     "birth": "1972年12月", "birthplace": "福建省晋江市", "education": "党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "晋江市市长", "current_org": "晋江市人民政府",
     "source": "https://www.jinjiang.gov.cn/"},

    # ── Deputy Mayors (from official website) ──
    {"id": 3, "name": "吴靖宇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "晋江市副市长", "current_org": "晋江市人民政府",
     "source": "https://www.jinjiang.gov.cn/"},

    {"id": 4, "name": "吴尊意", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "晋江市副市长", "current_org": "晋江市人民政府",
     "source": "https://www.jinjiang.gov.cn/"},

    {"id": 5, "name": "王也夫", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "晋江市副市长", "current_org": "晋江市人民政府",
     "source": "https://www.jinjiang.gov.cn/"},

    {"id": 6, "name": "陈丽蓉", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "晋江市副市长", "current_org": "晋江市人民政府",
     "source": "https://www.jinjiang.gov.cn/"},

    {"id": 7, "name": "陈进福", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "晋江市副市长", "current_org": "晋江市人民政府",
     "source": "https://www.jinjiang.gov.cn/"},

    {"id": 8, "name": "陈清平", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "晋江市副市长", "current_org": "晋江市人民政府",
     "source": "https://www.jinjiang.gov.cn/"},

    {"id": 9, "name": "陈英煌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "晋江市副市长", "current_org": "晋江市人民政府",
     "source": "https://www.jinjiang.gov.cn/"},

    # ── Other Key Leaders (from Wikipedia) ──
    {"id": 10, "name": "陈长义", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "福建省南安市", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "晋江市人大常委会主任", "current_org": "晋江市人民代表大会常务委员会",
     "source": "https://zh.wikipedia.org/wiki/%E6%99%8B%E6%B1%9F%E5%B8%82"},

    {"id": 11, "name": "黄天凯", "gender": "男", "ethnicity": "汉族",
     "birth": "1972年5月", "birthplace": "福建省永春县湖洋镇", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "晋江市政协主席", "current_org": "中国人民政治协商会议晋江市委员会",
     "source": "https://zh.wikipedia.org/wiki/%E6%99%8B%E6%B1%9F%E5%B8%82"},

    {"id": 12, "name": "郑永璘", "gender": "男", "ethnicity": "汉族",
     "birth": "1973年10月", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "晋江市监察委员会主任", "current_org": "晋江市监察委员会",
     "source": "https://zh.wikipedia.org/wiki/%E6%99%8B%E6%B1%9F%E5%B8%82"},

    # ── Predecessors ──
    {"id": 13, "name": "张文贤", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泉州市委常委（推测已调任）", "current_org": "中共泉州市委员会",
     "source": "https://zh.wikipedia.org/wiki/%E6%B3%89%E5%B7%9E%E5%B8%82"},
]

organizations = [
    {"id": 1, "name": "中共晋江市委员会", "type": "党委", "level": "县级",
     "parent": "中共泉州市委员会", "location": "福建省泉州市晋江市"},
    {"id": 2, "name": "晋江市人民政府", "type": "政府", "level": "县级",
     "parent": "泉州市人民政府", "location": "福建省泉州市晋江市"},
    {"id": 3, "name": "晋江市人民代表大会常务委员会", "type": "人大", "level": "县级",
     "parent": "泉州市人民代表大会常务委员会", "location": "福建省泉州市晋江市"},
    {"id": 4, "name": "中国人民政治协商会议晋江市委员会", "type": "政协", "level": "县级",
     "parent": "中国人民政治协商会议泉州市委员会", "location": "福建省泉州市晋江市"},
    {"id": 5, "name": "晋江市监察委员会", "type": "其他", "level": "县级",
     "parent": "泉州市监察委员会", "location": "福建省泉州市晋江市"},
    {"id": 6, "name": "中共泉州市委员会", "type": "党委", "level": "地厅级",
     "parent": "中共福建省委员会", "location": "福建省泉州市"},
]

positions = [
    # 王明元
    {"id": 1, "person_id": 1, "org_id": 1,
     "title": "中共晋江市委书记", "start": "2026-01", "end": "至今",
     "rank": "正处级", "note": "2026年1月就任"},

    # 王小阳
    {"id": 2, "person_id": 2, "org_id": 2,
     "title": "晋江市市长", "start": "2026-01", "end": "至今",
     "rank": "正处级", "note": "2026年1月就任"},

    # Deputy Mayors
    {"id": 3, "person_id": 3, "org_id": 2,
     "title": "晋江市副市长", "start": "", "end": "至今",
     "rank": "副处级", "note": ""},
    {"id": 4, "person_id": 4, "org_id": 2,
     "title": "晋江市副市长", "start": "", "end": "至今",
     "rank": "副处级", "note": ""},
    {"id": 5, "person_id": 5, "org_id": 2,
     "title": "晋江市副市长", "start": "", "end": "至今",
     "rank": "副处级", "note": ""},
    {"id": 6, "person_id": 6, "org_id": 2,
     "title": "晋江市副市长", "start": "", "end": "至今",
     "rank": "副处级", "note": ""},
    {"id": 7, "person_id": 7, "org_id": 2,
     "title": "晋江市副市长", "start": "", "end": "至今",
     "rank": "副处级", "note": ""},
    {"id": 8, "person_id": 8, "org_id": 2,
     "title": "晋江市副市长", "start": "", "end": "至今",
     "rank": "副处级", "note": ""},
    {"id": 9, "person_id": 9, "org_id": 2,
     "title": "晋江市副市长", "start": "", "end": "至今",
     "rank": "副处级", "note": ""},

    # 陈长义
    {"id": 10, "person_id": 10, "org_id": 3,
     "title": "晋江市人大常委会主任", "start": "2026-01", "end": "至今",
     "rank": "正处级", "note": "2026年1月就任"},

    # 黄天凯
    {"id": 11, "person_id": 11, "org_id": 4,
     "title": "晋江市政协主席", "start": "2024-12", "end": "至今",
     "rank": "正处级", "note": "2024年12月就任"},

    # 郑永璘
    {"id": 12, "person_id": 12, "org_id": 5,
     "title": "晋江市监察委员会主任", "start": "2026-01", "end": "至今",
     "rank": "正处级", "note": "2026年1月就任"},

    # 张文贤 — 前任市委书记
    {"id": 13, "person_id": 13, "org_id": 1,
     "title": "中共晋江市委书记（前任）", "start": "2021?", "end": "2025-12",
     "rank": "副厅级（兼任泉州市委常委）", "note": "约2021年-2025年12月任晋江市委书记，同时任泉州市委常委"},

    # 张文贤 — 泉州市委常委
    {"id": 14, "person_id": 13, "org_id": 6,
     "title": "泉州市委常委", "start": "2021?", "end": "至今",
     "rank": "副厅级", "note": "兼任晋江市委书记期间为泉州市委常委；卸任书记后是否仍任常委待确认"},
]

relationships = [
    # 王明元 ↔ 王小阳 — 党政一把手
    {"id": 1, "person_a_id": 1, "person_b_id": 2,
     "type": "党政搭档", "context": "王明元（市委书记）与王小阳（市长）为晋江市党政一把手搭档",
     "overlap_org": "晋江市", "overlap_period": "2026-01至今"},

    # 王小阳 ↔ 副市长 — 政府领导班子
    {"id": 2, "person_a_id": 2, "person_b_id": 3,
     "type": "上下级", "context": "市长与副市长（吴靖宇）",
     "overlap_org": "晋江市人民政府", "overlap_period": "至今"},
    {"id": 3, "person_a_id": 2, "person_b_id": 4,
     "type": "上下级", "context": "市长与副市长（吴尊意）",
     "overlap_org": "晋江市人民政府", "overlap_period": "至今"},
    {"id": 4, "person_a_id": 2, "person_b_id": 5,
     "type": "上下级", "context": "市长与副市长（王也夫）",
     "overlap_org": "晋江市人民政府", "overlap_period": "至今"},
    {"id": 5, "person_a_id": 2, "person_b_id": 6,
     "type": "上下级", "context": "市长与副市长（陈丽蓉）",
     "overlap_org": "晋江市人民政府", "overlap_period": "至今"},
    {"id": 6, "person_a_id": 2, "person_b_id": 7,
     "type": "上下级", "context": "市长与副市长（陈进福）",
     "overlap_org": "晋江市人民政府", "overlap_period": "至今"},
    {"id": 7, "person_a_id": 2, "person_b_id": 8,
     "type": "上下级", "context": "市长与副市长（陈清平）",
     "overlap_org": "晋江市人民政府", "overlap_period": "至今"},
    {"id": 8, "person_a_id": 2, "person_b_id": 9,
     "type": "上下级", "context": "市长与副市长（陈英煌）",
     "overlap_org": "晋江市人民政府", "overlap_period": "至今"},

    # 王明元 ↔ 张文贤 — 前任书记接任关系
    {"id": 9, "person_a_id": 13, "person_b_id": 1,
     "type": "前任继任", "context": "张文贤（前任书记，兼任泉州市委常委）→ 王明元（2026年1月接任书记）",
     "overlap_org": "中共晋江市委员会", "overlap_period": "2026-01（交接）"},

    # 王明元 ↔ 王小阳 — 前任市长接任关系
    {"id": 10, "person_a_id": 1, "person_b_id": 2,
     "type": "前任继任", "context": "王明元（推测前任市长，升任书记）→ 王小阳（接任市长）",
     "overlap_org": "晋江市人民政府", "overlap_period": "2026-01（交接）"},
]


# ── BUILD SQLITE DATABASE ────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS persons (
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

CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

CREATE TABLE IF NOT EXISTS positions (
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

CREATE TABLE IF NOT EXISTS relationships (
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
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>晋江市领导班子工作关系网络 - {today}</description>')
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
        color = '#2980B9'  # blue: government leader (mayor)
        size = 18.0
    elif p["id"] == 13:
        color = '#E03C31'  # red: former Party Secretary
        size = 16.0
    elif p["id"] == 10:
        color = '#2ECC71'  # green: People's Congress
        size = 14.0
    elif p["id"] == 11:
        color = '#F39C12'  # gold: PPCC
        size = 14.0
    elif p["id"] == 12:
        color = '#E67E22'  # orange: discipline
        size = 14.0
    else:
        color = '#95A5A6'  # grey: others
        size = 12.0

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
    lines.append(f'        <viz:color r="{int(color[1:3], 16)}" g="{int(color[3:5], 16)}" b="{int(color[5:7], 16)}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'      </node>')

# ── Nodes: Organizations ──
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

os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

total_nodes = len(persons) + len(organizations)
total_edges = len(positions) + len(relationships)
print(f"\nGEXF graph written: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} organizations = {total_nodes} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {total_edges} total")
print("\nDone!")
