#!/usr/bin/env python3
"""
安远县领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Anyuan County (安远县, 赣州市, 江西省) leadership.

Research date: 2026-07-15
Research method: government website (ay.gov.cn), Baidu search, news reports.

Key findings as of July 2026:
- 杨有谷 (县委书记 since 2021.8) has been transferred to 大余县委书记 (July 2026)
- 钟小刚 (县长 since 2023.10) has been promoted to 安远县委书记 (July 2026)
- 李高华 (née 于都县委副书记) is appointed 安远县委副书记、县长候选人 (July 2026)

Sources:
  - http://www.ay.gov.cn (安远县人民政府)
  - https://www.ganzhou.gov.cn (赣州市人民政府)
  - Baidu Baike: 严水石, 杨有谷
  - News reports: 汲古新知, 上观新闻, 澎湃新闻, 网易订阅
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/安远县_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/安远县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ══ Current Party Secretary (县委书记) ══
    {"id": 1, "name": "钟小刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-12", "birthplace": "江西赣州", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安远县委书记", "current_org": "中共安远县委员会",
     "source": "ay.gov.cn; 上观新闻; 澎湃新闻"},

    # ══ Current County Magistrate (县长候选人) ══
    {"id": 2, "name": "李高华", "gender": "女", "ethnicity": "汉族",
     "birth": "1978-12", "birthplace": "江西上犹平富", "education": "省委党校研究生",
     "party_join": "2001-09", "work_start": "2000-09",
     "current_post": "安远县委副书记、县长候选人", "current_org": "安远县人民政府",
     "source": "ay.gov.cn; 百度百科; 汲古新知"},

    # ══ Previous Party Secretary (前任县委书记, 已调大余) ══
    {"id": 3, "name": "杨有谷", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-05", "birthplace": "江西上犹", "education": "中央党校研究生",
     "party_join": "1998-09", "work_start": "1993-08",
     "current_post": "大余县委书记", "current_org": "中共大余县委员会",
     "source": "百度百科; 安远党务公开网; 网易订阅"},

    # ══ Previous Party Secretaries (历任县委书记) ══
    {"id": 4, "name": "严水石", "gender": "男", "ethnicity": "汉族",
     "birth": "1963-05", "birthplace": "江西南康", "education": "中央党校",
     "party_join": "1985-06", "work_start": "1980-11",
     "current_post": "赣州市人大常委会原副主任", "current_org": "赣州市人大常委会",
     "source": "百度百科; 澎湃新闻"},
    {"id": 5, "name": "陈阳霞", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（原安远县委书记）", "current_org": "",
     "source": "公开报道"},
    # 方敏 is not a confirmed 安远县委书记; removing as unverified

    # ══ Previous County Magistrates (历任县长) ══
    {"id": 6, "name": "肖斐杰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（原安远县长）", "current_org": "",
     "source": "公开报道"},
    {"id": 7, "name": "罗招荣", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（原安远县长）", "current_org": "",
     "source": "公开报道"},
    {"id": 8, "name": "李秋平", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-07", "birthplace": "江西新干", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（原安远县长，被停职审查）", "current_org": "",
     "source": "澎湃新闻; 上观新闻"},

    # ══ Known 安远籍在外领导 (Anyuan-born leaders elsewhere) ══
    {"id": 9, "name": "刘志怀", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-10", "birthplace": "江西安远", "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "章贡区委副书记、区长", "current_org": "章贡区人民政府",
     "source": "https://www.zgq.gov.cn"},
    {"id": 10, "name": "谢卫东", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-09", "birthplace": "江西安远", "education": "大学学历",
     "party_join": "1994-06", "work_start": "1989-08",
     "current_post": "赣州市政府秘书长、党组成员", "current_org": "赣州市人民政府",
     "source": "https://www.ganzhou.gov.cn/gzszf/xwd/zw_sz.shtml"},
]

organizations = [
    {"id": 1, "name": "中共安远县委员会", "type": "党委", "level": "县处级", "parent": "中共赣州市委员会", "location": "江西赣州安远"},
    {"id": 2, "name": "安远县人民政府", "type": "政府", "level": "县处级", "parent": "赣州市人民政府", "location": "江西赣州安远"},
    {"id": 3, "name": "中共大余县委员会", "type": "党委", "level": "县处级", "parent": "中共赣州市委员会", "location": "江西赣州大余"},
    {"id": 4, "name": "赣州市人大常委会", "type": "人大", "level": "地厅级", "parent": "江西省人大常委会", "location": "江西赣州"},
    {"id": 5, "name": "赣州市人民政府", "type": "政府", "level": "地级", "parent": "江西省人民政府", "location": "江西赣州"},
    {"id": 6, "name": "章贡区人民政府", "type": "政府", "level": "县处级", "parent": "赣州市人民政府", "location": "江西赣州章贡"},
    {"id": 7, "name": "赣州市政府金融工作办公室", "type": "政府", "level": "县处级", "parent": "赣州市人民政府", "location": "江西赣州"},
    {"id": 8, "name": "中共于都县委员会", "type": "党委", "level": "县处级", "parent": "中共赣州市委员会", "location": "江西赣州于都"},
    {"id": 9, "name": "中共赣州市委组织部", "type": "党委部门", "level": "地厅级", "parent": "中共赣州市委员会", "location": "江西赣州"},
    {"id": 10, "name": "上犹县人民政府", "type": "政府", "level": "县处级", "parent": "赣州市人民政府", "location": "江西赣州上犹"},
]

positions = [
    # ── 钟小刚 career (current Party Secretary) ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "安远县委书记", "start": "2026-07", "end": "", "rank": "县处级正职", "note": "现任（新任）"},
    {"id": 2, "person_id": 1, "org_id": 2, "title": "安远县委副书记、县长", "start": "2023-10", "end": "2026-07", "rank": "县处级正职", "note": "前任职务"},
    {"id": 3, "person_id": 1, "org_id": 7, "title": "赣州市政府金融办党组书记、主任", "start": "2021", "end": "2023-10", "rank": "县处级正职", "note": ""},
    {"id": 4, "person_id": 1, "org_id": 5, "title": "赣州市政府金融办（不详前任职务）", "start": "", "end": "2021", "rank": "", "note": "履历缺口"},
    {"id": 5, "person_id": 1, "org_id": 1, "title": "寻乌县委常委（曾任）", "start": "", "end": "", "rank": "县处级副职", "note": "曾任寻乌县委常委等职"},  # 挂靠 org 1 as placeholder for 寻乌

    # ── 李高华 career (current County Magistrate candidate) ──
    {"id": 6, "person_id": 2, "org_id": 2, "title": "安远县委副书记、县长候选人", "start": "2026-07", "end": "", "rank": "县处级正职", "note": "现任"},
    {"id": 7, "person_id": 2, "org_id": 8, "title": "于都县委副书记", "start": "2021-08", "end": "2026-07", "rank": "县处级副职", "note": ""},
    {"id": 8, "person_id": 2, "org_id": 8, "title": "于都县委常委、组织部部长", "start": "", "end": "2021-08", "rank": "县处级副职", "note": ""},
    {"id": 9, "person_id": 2, "org_id": 10, "title": "上犹县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "更早职务"},

    # ── 杨有谷 career (previous Party Secretary, now 大余) ──
    {"id": 10, "person_id": 3, "org_id": 1, "title": "安远县委书记", "start": "2021-08", "end": "2026-07", "rank": "县处级正职", "note": ""},
    {"id": 11, "person_id": 3, "org_id": 3, "title": "大余县委书记", "start": "2026-07", "end": "", "rank": "县处级正职", "note": "现任"},
    {"id": 12, "person_id": 3, "org_id": 9, "title": "赣州市委组织部副部长、市委非公有制经济组织与社会组织工委书记", "start": "", "end": "2021-08", "rank": "县处级正职", "note": ""},
    {"id": 13, "person_id": 3, "org_id": 1, "title": "安远县委副书记", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 14, "person_id": 3, "org_id": 2, "title": "安远县委常委、常务副县长", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 15, "person_id": 3, "org_id": 5, "title": "赣州市委办公厅副主任", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 16, "person_id": 3, "org_id": 5, "title": "赣州市委办公厅副调研员", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 17, "person_id": 3, "org_id": 1, "title": "乡镇党委副书记、镇长（安远县辖）", "start": "", "end": "", "rank": "乡科级", "note": "早期职务"},
    {"id": 18, "person_id": 3, "org_id": 1, "title": "共青团安远县委书记", "start": "", "end": "", "rank": "乡科级", "note": "早期职务"},
    {"id": 19, "person_id": 3, "org_id": 1, "title": "安远县委办副主任", "start": "", "end": "", "rank": "乡科级", "note": "早期职务"},

    # ── 严水石 career ──
    {"id": 20, "person_id": 4, "org_id": 1, "title": "安远县委书记", "start": "2013", "end": "2021-08", "rank": "县处级正职", "note": "后兼任赣州市人大常委会副主任"},
    {"id": 21, "person_id": 4, "org_id": 4, "title": "赣州市人大常委会副主任（兼）", "start": "2019", "end": "2023", "rank": "副厅级", "note": "兼任安远县委书记至2021年"},
    {"id": 22, "person_id": 4, "org_id": 2, "title": "安远县委副书记、县长", "start": "2009", "end": "2013", "rank": "县处级正职", "note": ""},
    {"id": 23, "person_id": 4, "org_id": 5, "title": "赣州市林业局局长", "start": "", "end": "2009", "rank": "县处级正职", "note": ""},
    {"id": 24, "person_id": 4, "org_id": 5, "title": "瑞金市委副书记", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 25, "person_id": 4, "org_id": 5, "title": "瑞金市委常委、副市长", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 26, "person_id": 4, "org_id": 5, "title": "大余县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "早期职务"},

    # ── 肖斐杰 career ──
    {"id": 27, "person_id": 6, "org_id": 2, "title": "安远县长", "start": "2016", "end": "2023-02", "rank": "县处级正职", "note": ""},
    {"id": 28, "person_id": 6, "org_id": 1, "title": "安远县委副书记", "start": "", "end": "2016", "rank": "县处级副职", "note": ""},

    # ── 罗招荣 career ──
    {"id": 29, "person_id": 7, "org_id": 2, "title": "安远县长", "start": "", "end": "2016", "rank": "县处级正职", "note": ""},

    # ── 李秋平 career (scandal predecessor) ──
    {"id": 30, "person_id": 8, "org_id": 2, "title": "安远县长", "start": "", "end": "2023-02", "rank": "县处级正职", "note": "因涉嫌侵犯挂职女干部被停职审查"},

    # ── 刘志怀 career ──
    {"id": 31, "person_id": 9, "org_id": 6, "title": "章贡区委副书记、区长", "start": "", "end": "", "rank": "县处级正职", "note": "现任, 安远籍"},

    # ── 谢卫东 career ──
    {"id": 32, "person_id": 10, "org_id": 5, "title": "赣州市政府秘书长、党组成员", "start": "", "end": "", "rank": "正处级", "note": "现任, 安远籍"},
]

relationships = [
    # ── Predecessor-Successor: Party Secretary ──
    {"id": 1, "person_a_id": 3, "person_b_id": 1, "type": "交接", "context": "杨有谷→钟小刚 安远县委书记交接（2026年7月）", "overlap_org": "中共安远县委员会", "overlap_period": "2026-07"},
    {"id": 2, "person_a_id": 4, "person_b_id": 3, "type": "交接", "context": "严水石→杨有谷 安远县委书记交接（2021年8月）", "overlap_org": "中共安远县委员会", "overlap_period": "2021-08"},

    # ── Predecessor-Successor: County Magistrate ──
    {"id": 3, "person_a_id": 6, "person_b_id": 1, "type": "交接", "context": "肖斐杰→钟小刚 安远县长交接（2023年10月）", "overlap_org": "安远县人民政府", "overlap_period": "2023-10"},
    {"id": 4, "person_a_id": 8, "person_b_id": 6, "type": "交接", "context": "李秋平→肖斐杰 安远县长交接", "overlap_org": "安远县人民政府", "overlap_period": ""},

    # ── 党政搭档 (Party Secretary & Government Head) ──
    {"id": 5, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档", "context": "钟小刚与李高华为安远县党政一把手（2026年7月至今）", "overlap_org": "安远县人民政府", "overlap_period": "2026-07-"},
    {"id": 6, "person_a_id": 3, "person_b_id": 1, "type": "党政搭档", "context": "杨有谷（县委书记）与钟小刚（县长）党政搭档（2023-2026）", "overlap_org": "安远县人民政府", "overlap_period": "2023-2026"},

    # ── 安远籍在外领导 (Cross-county: Anyuan-born leaders elsewhere) ──
    {"id": 7, "person_a_id": 9, "person_b_id": 3, "type": "同籍贯", "context": "刘志怀（安远籍）曾任章贡区区长", "overlap_org": "", "overlap_period": ""},
    {"id": 8, "person_a_id": 10, "person_b_id": 3, "type": "同籍贯", "context": "谢卫东（安远籍）为赣州市政府秘书长", "overlap_org": "", "overlap_period": ""},
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
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return r,g,b string for person node color based on role."""
    if p["id"] == 1:
        return "255,50,50"    # red: current party secretary
    elif p["id"] == 2:
        return "50,100,255"   # blue: government head
    elif p["id"] == 3:
        return "200,50,50"    # dark red: former secretary (now at new post)
    elif p["id"] in [4, 5]:
        return "200,100,100"  # dark pink: former secretaries
    elif p["id"] in [6, 7, 8]:
        return "100,100,200"  # dark blue: former magistrates
    else:
        return "100,100,100"  # grey: others

def is_top_leader(p):
    return p["id"] in [1, 2]

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>安远县领导班子工作关系网络 - {today}</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attributes
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

# Nodes: Persons
lines.append('    <nodes>')
for p in persons:
    c = person_color(p)
    sz = "20.0" if is_top_leader(p) else ("15.0" if p["id"] in [3, 4, 6] else "12.0")
    r, g, b = c.split(",")
    lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="type" value="person"/>')
    lines.append('          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{esc(p["birth"])}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{esc(p["birthplace"])}"/>')
    lines.append(f'          <attvalue for="education" value="{esc(p["education"])}"/>')
    lines.append(f'          <attvalue for="current_post" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="source" value="{esc(p["source"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Nodes: Organizations
org_colors = {
    1: "255,200,200",   # Pink: 党委
    2: "200,200,255",   # Light blue: 政府
    3: "255,200,200",   # Pink: 党委
    4: "200,255,255",   # Cyan: 人大
    5: "200,200,255",   # Light blue: 政府
    6: "200,200,255",   # Light blue: 政府
    7: "200,200,255",   # Light blue: 政府
    8: "255,200,200",   # Pink: 党委
    9: "255,200,200",   # Pink: 党委部门
    10: "200,200,255",  # Light blue: 政府
}
for o in organizations:
    oid = 1000 + o["id"]
    oc = org_colors.get(o["id"], "200,200,200")
    r, g, b = oc.split(",")
    lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{esc(o["type"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
edge_id = 1

# person→organization (worked_at)
for pos in positions:
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="{edge_id}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{esc(pos["title"])}"/>')
    lines.append(f'          <attvalue for="period" value="{esc(pos["start"] or "?")} → {esc(pos["end"] or "今")}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
    edge_id += 1

# person↔person (relationships)
for r in relationships:
    lines.append(f'      <edge id="{edge_id}" source="{r["person_a_id"]}" target="{r["person_b_id"]}" label="{esc(r["type"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="context" value="{esc(r["context"])}"/>')
    lines.append(f'          <attvalue for="period" value="{esc(r["overlap_period"])}"/>')
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
