#!/usr/bin/env python3
"""
Build SQLite database + GEXF graph for 芜湖市弋江区 cadre network.

弋江区 — 安徽省芜湖市辖区，与芜湖高新技术产业开发区合署办公（"三区合一"）。
Data sourced from official government website (yjq.gov.cn), leadership page, and news.
Data current as of July 2026.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/anhui_弋江区")
DB_PATH = os.path.join(STAGING, "弋江区_network.db")
GEXF_PATH = os.path.join(STAGING, "弋江区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── A. Current Top Leadership ──
    # Party Secretary (区委书记)
    {"id": 1, "name": "李新宇", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-02", "birthplace": "安徽芜湖", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1997",
     "current_post": "芜湖高新区（三山经开区）党工委书记、管委会主任，弋江区委书记",
     "current_org": "中共弋江区委",
     "source": "https://www.yjq.gov.cn/zxxx/dzyw/18537595.html (2026-05-18选举报道); 原南陵县委书记"},
    # District Mayor (区长)
    {"id": 2, "name": "林松", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-11", "birthplace": "", "education": "本科/工学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芜湖高新区党工委副书记、管委会副主任，弋江区委副书记、区政府党组书记、区长",
     "current_org": "弋江区人民政府",
     "source": "https://www.yjq.gov.cn/xxgk/ldzc/index.html (领导之窗); https://www.yjq.gov.cn/zxxx/dzyw/18537595.html (2026-05-18)"},

    # ── B. Key Deputies (区委常委 / 副区长) ──
    # Executive Vice Mayor (常务副区长)
    {"id": 3, "name": "高翔", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "弋江区委常委、区政府常务副区长",
     "current_org": "弋江区人民政府",
     "source": "https://www.yjq.gov.cn/xxgk/ldzc/index.html"},
    # Vice Mayor (区委常委、副区长)
    {"id": 4, "name": "华中刚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "弋江区委常委、区政府副区长",
     "current_org": "弋江区人民政府",
     "source": "https://www.yjq.gov.cn/xxgk/ldzc/index.html"},
    # Vice Mayor
    {"id": 5, "name": "许伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "弋江区政府副区长",
     "current_org": "弋江区人民政府",
     "source": "https://www.yjq.gov.cn/xxgk/ldzc/index.html"},
    {"id": 6, "name": "尹兵", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "弋江区政府副区长",
     "current_org": "弋江区人民政府",
     "source": "https://www.yjq.gov.cn/xxgk/ldzc/index.html"},
    {"id": 7, "name": "孙辉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "弋江区政府副区长",
     "current_org": "弋江区人民政府",
     "source": "https://www.yjq.gov.cn/xxgk/ldzc/index.html"},
    {"id": 8, "name": "张振兴", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "弋江区政府副区长",
     "current_org": "弋江区人民政府",
     "source": "https://www.yjq.gov.cn/xxgk/ldzc/index.html"},

    # ── C. Predecessors ──
    {"id": 9, "name": "陈海俊", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-11", "birthplace": "安徽芜湖", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1996",
     "current_post": "[原弋江区委书记]（前任，已离任）",
     "current_org": "",
     "source": "build_芜湖市_data.py (原有数据); 已被李新宇接替"},
    {"id": 10, "name": "汪敏", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "[原弋江区区长]（推测为前任，2026年1月仍为区代表）",
     "current_org": "",
     "source": "https://www.yjq.gov.cn/zxxx/dzyw/18525424.html (2026-01, 以代表身份参加市人代会); 待确认是否确为前任区长"},

    # ── D. City-level leadership (芜湖市) ──
    {"id": 11, "name": "宁波", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-03", "birthplace": "安徽合肥", "education": "省委党校研究生/工学学士",
     "party_join": "中共党员", "work_start": "1988",
     "current_post": "芜湖市委书记",
     "current_org": "中共芜湖市委",
     "source": "芜湖市人民政府网站; build_芜湖市_data.py"},
    {"id": 12, "name": "徐志", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-03", "birthplace": "安徽合肥（一说巢湖）", "education": "在职研究生/经济学博士",
     "party_join": "中共党员", "work_start": "1994",
     "current_post": "芜湖市委副书记、市长",
     "current_org": "芜湖市人民政府",
     "source": "芜湖市人民政府网站; build_芜湖市_data.py"},
]

organizations = [
    {"id": 1, "name": "中共弋江区委", "type": "党委", "level": "县处级", "parent": "中共芜湖市委", "location": "芜湖市弋江区"},
    {"id": 2, "name": "弋江区人民政府", "type": "政府", "level": "县处级", "parent": "芜湖市人民政府", "location": "芜湖市弋江区"},
    {"id": 3, "name": "芜湖高新技术产业开发区管委会", "type": "开发区", "level": "县处级", "parent": "芜湖市人民政府", "location": "芜湖市弋江区"},
    {"id": 4, "name": "中共芜湖市委", "type": "党委", "level": "地厅级", "parent": "中共安徽省委", "location": "芜湖市"},
    {"id": 5, "name": "芜湖市人民政府", "type": "政府", "level": "地厅级", "parent": "安徽省人民政府", "location": "芜湖市"},
]

positions = [
    # ── Li Xinyu (李新宇) — 区委书记 ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "弋江区委书记", "start": "~2026-01", "end": "", "rank": "县处级正职", "note": "现任（接替陈海俊）"},
    {"id": 2, "person_id": 1, "org_id": 3, "title": "芜湖高新区（三山经开区）党工委书记、管委会主任", "start": "~2026-01", "end": "", "rank": "县处级正职", "note": "合署办公"},
    {"id": 3, "person_id": 1, "org_id": 4, "title": "南陵县委书记（前任职务）", "start": "2021", "end": "~2025", "rank": "县处级正职", "note": "参照 build_芜湖市_data.py"},

    # ── Lin Song (林松) — 区长 ──
    {"id": 4, "person_id": 2, "org_id": 2, "title": "弋江区人民政府区长", "start": "2026-05-17", "end": "", "rank": "县处级正职", "note": "2026年5月17日区人代会选举"},
    {"id": 5, "person_id": 2, "org_id": 1, "title": "弋江区委副书记", "start": "~2026-05", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 6, "person_id": 2, "org_id": 3, "title": "芜湖高新区党工委副书记、管委会副主任", "start": "~2026-05", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 7, "person_id": 2, "org_id": 1, "title": "市辖区区委常委、组织部部长（前任职务）", "start": "", "end": "", "rank": "县处级副职", "note": "[GAP]具体任职时间、地点待核实"},
    {"id": 8, "person_id": 2, "org_id": 3, "title": "省级经济开发区党工委书记、管委会主任（前任职务）", "start": "", "end": "", "rank": "县处级正职", "note": "[GAP]具体任职时间、地点待核实"},

    # ── Gao Xiang (高翔) — 常务副区长 ──
    {"id": 9, "person_id": 3, "org_id": 2, "title": "弋江区委常委、区政府常务副区长", "start": "", "end": "", "rank": "县处级副职", "note": "[GAP]具体上任时间待核实"},

    # ── Hua Zhonggang (华中刚) — 区委常委、副区长 ──
    {"id": 10, "person_id": 4, "org_id": 2, "title": "弋江区委常委、区政府副区长", "start": "", "end": "", "rank": "县处级副职", "note": "[GAP]具体上任时间待核实"},

    # ── Vice Mayors ──
    {"id": 11, "person_id": 5, "org_id": 2, "title": "弋江区政府副区长", "start": "", "end": "", "rank": "县处级副职", "note": "[GAP]具体分工待核实"},
    {"id": 12, "person_id": 6, "org_id": 2, "title": "弋江区政府副区长", "start": "", "end": "", "rank": "县处级副职", "note": "[GAP]具体分工待核实"},
    {"id": 13, "person_id": 7, "org_id": 2, "title": "弋江区政府副区长", "start": "", "end": "", "rank": "县处级副职", "note": "[GAP]具体分工待核实"},
    {"id": 14, "person_id": 8, "org_id": 2, "title": "弋江区政府副区长", "start": "", "end": "", "rank": "县处级副职", "note": "[GAP]具体分工待核实"},

    # ── Predecessors ──
    {"id": 15, "person_id": 9, "org_id": 1, "title": "弋江区委书记（前任）", "start": "~2021", "end": "~2025", "rank": "县处级正职", "note": "[GAP]李新宇的前任; 具体离任时间待核实"},
    {"id": 16, "person_id": 10, "org_id": 2, "title": "[推测]弋江区人民政府区长（前任）", "start": "", "end": "~2026-05", "rank": "县处级正职", "note": "[GAP]林松的前任; 待确认"},

    # ── City-level leadership ──
    {"id": 17, "person_id": 11, "org_id": 4, "title": "芜湖市委书记", "start": "2021-06", "end": "", "rank": "正厅", "note": ""},
    {"id": 18, "person_id": 12, "org_id": 5, "title": "芜湖市人民政府市长", "start": "2023-03", "end": "", "rank": "正厅", "note": ""},
]

relationships = [
    # ── Current top leadership pair ──
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档", "context": "李新宇（区委书记）与林松（区长）为当前党政搭档", "overlap_org": "中共弋江区委/弋江区政府", "overlap_period": "2026-05至"},  # noqa

    # ── Predecessor-Successor ──
    {"id": 2, "person_a_id": 9, "person_b_id": 1, "type": "前后任", "context": "陈海俊→李新宇 弋江区委书记交接（~2025/2026）", "overlap_org": "中共弋江区委", "overlap_period": "~2025/2026"},
    {"id": 3, "person_a_id": 10, "person_b_id": 2, "type": "前后任", "context": "汪敏→林松 弋江区区长交接（2026-05）", "overlap_org": "弋江区人民政府", "overlap_period": "2026-05"},

    # ── Superior-subordinate (区委领导-区政府班子成员) ──
    {"id": 4, "person_a_id": 1, "person_b_id": 3, "type": "上下级", "context": "区委书记与常务副区长", "overlap_org": "中共弋江区委", "overlap_period": ""},
    {"id": 5, "person_a_id": 1, "person_b_id": 4, "type": "上下级", "context": "区委书记与常委副区长", "overlap_org": "中共弋江区委", "overlap_period": ""},
    {"id": 6, "person_a_id": 2, "person_b_id": 3, "type": "上下级", "context": "区长与常务副区长搭档", "overlap_org": "弋江区人民政府", "overlap_period": "2026-05至"},
    {"id": 7, "person_a_id": 2, "person_b_id": 4, "type": "上下级", "context": "区长与副区长（常委）搭档", "overlap_org": "弋江区人民政府", "overlap_period": "2026-05至"},
    {"id": 8, "person_a_id": 2, "person_b_id": 5, "type": "上下级", "context": "区长与副区长搭档", "overlap_org": "弋江区人民政府", "overlap_period": "2026-05至"},
    {"id": 9, "person_a_id": 2, "person_b_id": 6, "type": "上下级", "context": "区长与副区长搭档", "overlap_org": "弋江区人民政府", "overlap_period": "2026-05至"},
    {"id": 10, "person_a_id": 2, "person_b_id": 7, "type": "上下级", "context": "区长与副区长搭档", "overlap_org": "弋江区人民政府", "overlap_period": "2026-05至"},
    {"id": 11, "person_a_id": 2, "person_b_id": 8, "type": "上下级", "context": "区长与副区长搭档", "overlap_org": "弋江区人民政府", "overlap_period": "2026-05至"},

    # ── City-level oversight ──
    {"id": 12, "person_a_id": 11, "person_b_id": 1, "type": "上下级", "context": "芜湖市委书记与弋江区委书记上下级", "overlap_org": "芜湖市", "overlap_period": ""},
    {"id": 13, "person_a_id": 12, "person_b_id": 2, "type": "上下级", "context": "芜湖市长与弋江区区长上下级", "overlap_org": "芜湖市", "overlap_period": "2026-05至"},

    # ── Li Xinyu's own history (former Nanling county → Yijiang) ──
    {"id": 14, "person_a_id": 1, "person_b_id": 9, "type": "前辈/后辈", "context": "陈海俊原是弋江区委书记，李新宇从南陵县委书记调任接替", "overlap_org": "芜湖市", "overlap_period": ""},
]

# ── BUILD DATABASE ──────────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

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

# Summary
cur.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]

conn.close()
print(f"✅ SQLite database: {DB_PATH}")
print(f"   Persons: {person_count} | Orgs: {org_count} | Positions: {pos_count} | Relationships: {rel_count}")

# ── BUILD GEXF ──────────────────────────────────────────────────────

today = datetime.now().strftime("%Y-%m-%d")


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    post = p["current_post"] or ""
    if "区委书记" in post:
        return (255, 50, 50)  # Red
    if "区长" in post and "副" not in post:
        return (50, 100, 255)  # Blue
    if "常务副" in post:
        return (50, 100, 255)  # Blue
    if "副书记" in post:
        return (200, 100, 50)  # Orange-red
    # Predecessors / former
    if p["id"] in [9, 10]:
        return (150, 150, 150)  # Grey
    # City-level
    if p["id"] in [11]:
        return (255, 50, 50)
    if p["id"] in [12]:
        return (50, 100, 255)
    return (100, 100, 100)  # Grey


def person_size(p):
    if p["id"] in [1, 2, 11, 12]:
        return 20.0  # Top leaders
    if p["id"] in [3, 4]:
        return 15.0  # Key deputies
    return 12.0


def org_color(o):
    colors = {
        "党委": (255, 200, 200),   # Pink
        "政府": (200, 200, 255),   # Light blue
        "开发区": (200, 255, 200),  # Light green
    }
    return colors.get(o["type"], (200, 200, 200))


lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>芜湖市弋江区领导班子工作关系网络 - {today}</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# ── Attributes ──
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="category" title="Category" type="string"/>')
lines.append('      <attribute id="birth" title="Birth" type="string"/>')
lines.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
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
print(f"✅ GEXF graph: {GEXF_PATH}")
print(f"   Nodes: {len(persons)} persons + {len(organizations)} orgs = {total_nodes}")
print(f"   Edges: {len(positions)} worked_at + {len(relationships)} relationships = {total_edges}")
print()
print("⚠️  Gaps:")
print("  1. 林松完整履历时间线待补充（曾任组织部部长、开发区书记，具体地点时间不详）")
print("  2. 林松出生地/籍贯未公开")
print("  3. 陈海俊离任后新职务待查")
print("  4. 前任区长汪敏完整信息待确认（含是否确为前任区长）")
print("  5. 高翔、华中刚等副区长完整简历待补充")
print("  6. 区委其他常委（组织、纪委、宣传、政法、统战部长）信息待查")
print()
print("🔗 Verified Sources:")
print("  - https://www.yjq.gov.cn/xxgk/ldzc/index.html (政府领导之窗)")
print("  - https://www.yjq.gov.cn/zxxx/dzyw/18537595.html (林松当选区长报道 2026-05-18)")
print("  - https://www.yjq.gov.cn/zxxx/dzyw/18542586.html (区第五次党代会 2026-06-26)")
print("  - https://www.yjq.gov.cn (弋江区政府官网)")
print("✅ Done!")
