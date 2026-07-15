#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 无为市 (Wuwei City) leadership network."""

import sqlite3
import os
import json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/anhui_无为市")

# ── DATA ─────────────────────────────────────────────────────────────

# Current date for filenames
TODAY = datetime.now().strftime("%Y%m%d")

persons = [
    # ── Core Leaders (市委) ──
    {"id": 1, "name": "匡健", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "无为市委书记", "current_org": "中共无为市委员会",
     "source": "https://www.ww.gov.cn/zwzx/wwyw/12271562.html"},
    {"id": 2, "name": "束晓伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-10", "birthplace": "", "education": "大学学历、法学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "无为市委副书记、市长", "current_org": "无为市人民政府",
     "source": "https://www.ww.gov.cn/zwgk/ldzc/index.html"},
    {"id": 3, "name": "方家俊", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "无为市委副书记、宣传部部长", "current_org": "中共无为市委员会",
     "source": "https://www.ww.gov.cn/zwzx/wwyw/12270635.html"},

    # ── Government Leaders (市政府) ──
    {"id": 4, "name": "袁玉琴", "gender": "女", "ethnicity": "汉族",
     "birth": "1984-09", "birthplace": "", "education": "研究生学历、管理学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "无为市委常委、常务副市长", "current_org": "无为市人民政府",
     "source": "https://www.ww.gov.cn/zwgk/ldzc/index.html"},
    {"id": 5, "name": "宋明", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-12", "birthplace": "", "education": "研究生学历、法学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "无为市委常委、副市长（挂职）", "current_org": "无为市人民政府",
     "source": "https://www.ww.gov.cn/zwgk/ldzc/index.html"},
    {"id": 6, "name": "洪本荣", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-12", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "无为市委常委、副市长", "current_org": "无为市人民政府",
     "source": "https://www.ww.gov.cn/zwgk/ldzc/index.html"},
    {"id": 7, "name": "李伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-12", "birthplace": "", "education": "研究生学历、理学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "无为市委常委、副市长（挂职）", "current_org": "无为市人民政府",
     "source": "https://www.ww.gov.cn/zwgk/ldzc/index.html"},
    {"id": 8, "name": "王江村", "gender": "女", "ethnicity": "汉族",
     "birth": "1972-08", "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "",
     "current_post": "无为市副市长", "current_org": "无为市人民政府",
     "source": "https://www.ww.gov.cn/zwgk/ldzc/index.html"},
    {"id": 9, "name": "徐沛沛", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-10", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "无为市副市长、市公安局局长", "current_org": "无为市人民政府",
     "source": "https://www.ww.gov.cn/zwgk/ldzc/index.html"},
    {"id": 10, "name": "钱刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-08", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "无为市副市长", "current_org": "无为市人民政府",
     "source": "https://www.ww.gov.cn/zwgk/ldzc/index.html"},

    # ──人大、政协 ──
    {"id": 11, "name": "陈兆强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "无为市人大常委会主任", "current_org": "无为市人大常委会",
     "source": "https://www.ww.gov.cn/zwzx/wwyw/12270635.html"},
    {"id": 12, "name": "凌世宏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "无为市政协主席", "current_org": "政协无为市委员会",
     "source": "https://www.ww.gov.cn/zwzx/wwyw/12270635.html"},

    # ──其他市领导──
    {"id": 13, "name": "许立", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "无为市领导", "current_org": "无为市",
     "source": "https://www.ww.gov.cn/zwzx/wwyw/12271958.html"},
]

organizations = [
    {"id": 1, "name": "中共无为市委员会", "type": "党委", "level": "县处级", "parent": "中共芜湖市委员会", "location": "安徽芜湖无为"},
    {"id": 2, "name": "无为市人民政府", "type": "政府", "level": "县处级", "parent": "芜湖市人民政府", "location": "安徽芜湖无为"},
    {"id": 3, "name": "无为市人大常委会", "type": "人大", "level": "县处级", "parent": "芜湖市人大常委会", "location": "安徽芜湖无为"},
    {"id": 4, "name": "政协无为市委员会", "type": "政协", "level": "县处级", "parent": "政协芜湖市委员会", "location": "安徽芜湖无为"},
    {"id": 5, "name": "无为市公安局", "type": "政府", "level": "乡科级", "parent": "无为市人民政府", "location": "安徽芜湖无为"},
    {"id": 6, "name": "中共无为市纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共芜湖市纪律检查委员会", "location": "安徽芜湖无为"},
]

positions = [
    # ── 匡健 ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "无为市委书记", "start": "", "end": "", "rank": "县处级正职", "note": "现任（2026年7月确认）"},

    # ── 束晓伟 ──
    {"id": 2, "person_id": 2, "org_id": 1, "title": "无为市委副书记", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 3, "person_id": 2, "org_id": 2, "title": "无为市市长", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},
    {"id": 4, "person_id": 2, "org_id": 2, "title": "区政府组成部门副职、正职", "start": "", "end": "", "rank": "", "note": "早期职务（来源官方简历）"},
    {"id": 5, "person_id": 2, "org_id": 2, "title": "街道党工委书记", "start": "", "end": "", "rank": "", "note": "早期职务"},
    {"id": 6, "person_id": 2, "org_id": 2, "title": "市辖区区委常委、副区长", "start": "", "end": "", "rank": "县处级副职", "note": "此前职务"},

    # ── 方家俊 ──
    {"id": 7, "person_id": 3, "org_id": 1, "title": "无为市委副书记、宣传部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── 袁玉琴 ──
    {"id": 8, "person_id": 4, "org_id": 1, "title": "无为市委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 9, "person_id": 4, "org_id": 2, "title": "无为市常务副市长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 10, "person_id": 4, "org_id": 2, "title": "地级市政府工作部门内设机构副职、正职", "start": "", "end": "", "rank": "", "note": "早期职务"},
    {"id": 11, "person_id": 4, "org_id": 2, "title": "地级市政府工作部门副职", "start": "", "end": "", "rank": "", "note": "此前职务"},

    # ── 宋明 ──
    {"id": 12, "person_id": 5, "org_id": 1, "title": "无为市委常委、副市长（挂职）", "start": "", "end": "", "rank": "县处级副职", "note": "现任（挂职）"},
    {"id": 13, "person_id": 5, "org_id": 2, "title": "国务院直属机构内设部门副处长、处长", "start": "", "end": "", "rank": "", "note": "此前职务"},

    # ── 洪本荣 ──
    {"id": 14, "person_id": 6, "org_id": 1, "title": "无为市委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 15, "person_id": 6, "org_id": 2, "title": "无为市副市长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 16, "person_id": 6, "org_id": 2, "title": "乡镇副镇长、党委副书记、镇长、党委书记", "start": "", "end": "", "rank": "乡科级", "note": "早期职务"},
    {"id": 17, "person_id": 6, "org_id": 2, "title": "地级市政府多个组成部门副职", "start": "", "end": "", "rank": "", "note": "此前职务"},

    # ── 李伟 ──
    {"id": 18, "person_id": 7, "org_id": 1, "title": "无为市委常委、副市长（挂职）", "start": "", "end": "", "rank": "县处级副职", "note": "现任（挂职）"},
    {"id": 19, "person_id": 7, "org_id": 2, "title": "开发园区组成部门副职、正职，管委会副主任", "start": "", "end": "", "rank": "", "note": "此前职务"},

    # ── 王江村 ──
    {"id": 20, "person_id": 8, "org_id": 2, "title": "无为市副市长", "start": "", "end": "", "rank": "县处级副职", "note": "现任（非党员）"},
    {"id": 21, "person_id": 8, "org_id": 2, "title": "县级政府组成部门副科、正科", "start": "", "end": "", "rank": "", "note": "早期职务"},
    {"id": 22, "person_id": 8, "org_id": 2, "title": "政协副主席", "start": "", "end": "", "rank": "", "note": "此前职务"},

    # ── 徐沛沛 ──
    {"id": 23, "person_id": 9, "org_id": 2, "title": "无为市副市长、市公安局局长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 24, "person_id": 9, "org_id": 5, "title": "市公安局党委书记、督察长", "start": "", "end": "", "rank": "", "note": "现任"},
    {"id": 25, "person_id": 9, "org_id": 1, "title": "市委政法委副书记（兼）", "start": "", "end": "", "rank": "", "note": "现任"},
    {"id": 26, "person_id": 9, "org_id": 5, "title": "地级市公安局二级机构副职、正职", "start": "", "end": "", "rank": "", "note": "此前职务"},

    # ── 钱刚 ──
    {"id": 27, "person_id": 10, "org_id": 2, "title": "无为市副市长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 28, "person_id": 10, "org_id": 2, "title": "县级政府组成部门科员", "start": "", "end": "", "rank": "", "note": "早期职务"},
    {"id": 29, "person_id": 10, "org_id": 1, "title": "县级党群部门副职、正职", "start": "", "end": "", "rank": "", "note": "此前职务"},
    {"id": 30, "person_id": 10, "org_id": 2, "title": "乡镇副职、正职", "start": "", "end": "", "rank": "", "note": "此前职务"},

    # ── 陈兆强 ──
    {"id": 31, "person_id": 11, "org_id": 3, "title": "无为市人大常委会主任", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},

    # ── 凌世宏 ──
    {"id": 32, "person_id": 12, "org_id": 4, "title": "无为市政协主席", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},

    # ── 许立 ──
    {"id": 33, "person_id": 13, "org_id": 1, "title": "无为市领导", "start": "", "end": "", "rank": "", "note": "具体职务待补充"},
]

relationships = [
    # 匡健 ↔ 束晓伟（党政一把手搭班）
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "superior_subordinate",
     "context": "党政主要领导搭班，市委书记和市长工作关系", "overlap_org": "中共无为市委员会/无为市人民政府", "overlap_period": "2026年"},
    # 方家俊 ↔ 匡健（副书记与书记）
    {"id": 2, "person_a_id": 1, "person_b_id": 3, "type": "superior_subordinate",
     "context": "市委书记与专职副书记工作关系", "overlap_org": "中共无为市委员会", "overlap_period": "2026年"},
    # 袁玉琴 ↔ 束晓伟（市长与常务副市长）
    {"id": 3, "person_a_id": 2, "person_b_id": 4, "type": "superior_subordinate",
     "context": "市长与常务副市长搭班", "overlap_org": "无为市人民政府", "overlap_period": "2026年"},
    # 匡健 ↔ 陈兆强（党委与人大）
    {"id": 4, "person_a_id": 1, "person_b_id": 11, "type": "overlap",
     "context": "市委书记与市人大常委会主任在同一届领导班子", "overlap_org": "无为市", "overlap_period": "2026年"},
    # 匡健 ↔ 凌世宏（党委与政协）
    {"id": 5, "person_a_id": 1, "person_b_id": 12, "type": "overlap",
     "context": "市委书记与市政协主席在同一届领导班子", "overlap_org": "无为市", "overlap_period": "2026年"},
    # 洪本荣 ↔ 束晓伟（副市长与市长）
    {"id": 6, "person_a_id": 2, "person_b_id": 6, "type": "superior_subordinate",
     "context": "市长与分管副市长", "overlap_org": "无为市人民政府", "overlap_period": "2026年"},
    # 徐沛沛 ↔ 束晓伟（公安局长与市长）
    {"id": 7, "person_a_id": 2, "person_b_id": 9, "type": "superior_subordinate",
     "context": "市长与公安局局长", "overlap_org": "无为市人民政府", "overlap_period": "2026年"},
    # 钱刚 ↔ 束晓伟
    {"id": 8, "person_a_id": 2, "person_b_id": 10, "type": "superior_subordinate",
     "context": "市长与副市长", "overlap_org": "无为市人民政府", "overlap_period": "2026年"},
]


# ── BUILD SQLITE DATABASE ────────────────────────────────────────────

DB_PATH = os.path.join(STAGING, "无为市_network.db")
os.makedirs(STAGING, exist_ok=True)

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

GEXF_PATH = os.path.join(STAGING, "无为市_network.gexf")
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
lines.append(f'    <description>无为市领导班子工作关系网络 - {today}</description>')
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
    if pid == 1:  # 匡健 - Party Secretary
        color = '#E03C31'
        size = 20.0
    elif pid == 2:  # 束晓伟 - Mayor
        color = '#2980B9'
        size = 20.0
    elif pid == 3:  # 方家俊 - Deputy Party Secretary
        color = '#2980B9'
        size = 16.0
    elif pid in [4, 5, 6, 7]:  # 市委常委
        color = '#2980B9'
        size = 14.0
    elif pid == 9:  # 徐沛沛 - also public security (政法委)
        color = '#E67E22'
        size = 14.0
    elif pid in [8, 10]:  # Deputy Mayors
        color = '#2980B9'
        size = 12.0
    elif pid == 11:  # 陈兆强 - 人大
        color = '#2ECC71'
        size = 14.0
    elif pid == 12:  # 凌世宏 - 政协
        color = '#9B59B6'
        size = 14.0
    else:
        color = '#95A5A6'
        size = 12.0

    r_val = int(color[1:3], 16)
    g_val = int(color[3:5], 16)
    b_val = int(color[5:7], 16)

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
org_colors = {
    "党委": (255, 200, 200),
    "政府": (200, 200, 255),
    "人大": (200, 255, 255),
    "政协": (255, 240, 200),
    "纪委": (255, 165, 0),
}
for o in organizations:
    oid = 1000 + o["id"]
    oc = org_colors.get(o["type"], (200, 200, 200))
    lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{esc(o["type"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{oc[0]}" g="{oc[1]}" b="{oc[2]}"/>')
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
print("\nDone!")
