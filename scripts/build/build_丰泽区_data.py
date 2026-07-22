#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Fengze District (丰泽区) leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/tmp/fujian_丰泽区/丰泽区_network.db")
GEXF_PATH = os.path.join(BASE, "data/tmp/fujian_丰泽区/丰泽区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Party Secretary (区委书记) ──
    {"id": 1, "name": "张照绿", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-07", "birthplace": "福建南安", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共泉州市丰泽区委书记", "current_org": "中共泉州市丰泽区委员会",
     "source": "https://baike.baidu.com/item/%E5%BC%A0%E7%85%A7%E7%BB%BF/20188980"},

    # ── Current Acting District Mayor (代区长) ──
    {"id": 2, "name": "张健龙", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-11", "birthplace": "", "education": "中央党校大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共丰泽区委副书记、区政府党组书记、代区长", "current_org": "丰泽区人民政府",
     "source": "https://www.qzfz.gov.cn/zwgk/ldzc/qz/zjl/"},

    # ── Previous Party Secretary (前任区委书记) ──
    {"id": 3, "name": "高金全", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-02", "birthplace": "福建安溪", "education": "中央党校大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "曾任泉州市丰泽区委书记", "current_org": "",
     "source": "https://baike.baidu.com/item/%E9%AB%98%E9%87%91%E5%85%A8/19770782"},

    # ── Standing Committee / Executive Deputy Mayor (常务副区长) ──
    {"id": 4, "name": "郑燕然", "gender": "女", "ethnicity": "汉族",
     "birth": "1981-10", "birthplace": "", "education": "全日制研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共泉州市丰泽区委常委、常务副区长、区政府党组副书记", "current_org": "丰泽区人民政府",
     "source": "https://www.qzfz.gov.cn/zwgk/ldzc/cwfqz/zyr/"},

    # ── Deputy Mayors (副区长) ──
    {"id": 5, "name": "蔡宁波", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-04", "birthplace": "", "education": "研究生/理学博士",
     "party_join": "九三学社社员", "work_start": "",
     "current_post": "泉州市丰泽区人民政府副区长", "current_org": "丰泽区人民政府",
     "source": "https://www.qzfz.gov.cn/zwgk/ldzc/fqz/cnb/"},

    {"id": 6, "name": "林伟伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-07", "birthplace": "", "education": "党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泉州市丰泽区人民政府副区长、党组成员", "current_org": "丰泽区人民政府",
     "source": "https://www.qzfz.gov.cn/zwgk/ldzc/fqz/lww/"},

    {"id": 7, "name": "杨柳刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-11", "birthplace": "", "education": "本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泉州市丰泽区人民政府副区长、党组成员", "current_org": "丰泽区人民政府",
     "source": "https://www.qzfz.gov.cn/zwgk/ldzc/fqz/ylg/"},

    {"id": 8, "name": "丁增辉", "gender": "男", "ethnicity": "回族",
     "birth": "1984-07", "birthplace": "", "education": "研究生/管理学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泉州市丰泽区人民政府副区长、党组成员", "current_org": "丰泽区人民政府",
     "source": "https://www.qzfz.gov.cn/zwgk/ldzc/fqz/dzh/"},

    {"id": 9, "name": "李勇", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-01", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "丰泽区人民政府副区长、党组成员，泉州市公安局丰泽分局党委书记、局长", "current_org": "丰泽区人民政府",
     "source": "https://www.qzfz.gov.cn/zwgk/ldzc/fqz/ly/"},

    {"id": 10, "name": "戴隽翔", "gender": "男", "ethnicity": "汉族",
     "birth": "1986-09", "birthplace": "", "education": "党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泉州市丰泽区人民政府副区长、党组成员", "current_org": "丰泽区人民政府",
     "source": "https://www.qzfz.gov.cn/zwgk/ldzc/fqz/djx/"},

    # ── Other leaders from news mentions ──
    {"id": 11, "name": "陈逢生", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "丰泽区人大常委会主任", "current_org": "丰泽区人大常委会",
     "source": "https://www.qzfz.gov.cn/zwgk/xwzx/fzxw/202607/t20260716_3309655.htm"},

    {"id": 12, "name": "黄泽鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "丰泽区政协主席（推测）", "current_org": "丰泽区政协",
     "source": "https://www.qzfz.gov.cn/zwgk/xwzx/fzxw/202607/t20260716_3309655.htm"},

    {"id": 13, "name": "苏伟强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "丰泽区领导", "current_org": "丰泽区",
     "source": "https://www.qzfz.gov.cn/zcjd/hygq/202607/t20260716_3309612.htm"},
]

organizations = [
    {"id": 1, "name": "中共泉州市丰泽区委员会", "type": "党委", "level": "县处级", "parent": "中共泉州市委员会", "location": "福建省泉州市丰泽区"},
    {"id": 2, "name": "丰泽区人民政府", "type": "政府", "level": "县处级", "parent": "泉州市人民政府", "location": "福建省泉州市丰泽区"},
    {"id": 3, "name": "丰泽区人大常委会", "type": "人大", "level": "县处级", "parent": "泉州市人大常委会", "location": "福建省泉州市丰泽区"},
    {"id": 4, "name": "丰泽区政协", "type": "政协", "level": "县处级", "parent": "泉州市政协", "location": "福建省泉州市丰泽区"},
    {"id": 5, "name": "泉州市公安局丰泽分局", "type": "政府", "level": "县处级", "parent": "泉州市公安局", "location": "福建省泉州市丰泽区"},
]

positions = [
    # 张照绿 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "中共泉州市丰泽区委书记", "start": "", "end": "present", "rank": "县处级正职", "note": "2025/2026年任"},
    # 张健龙 - 代区长
    {"person_id": 2, "org_id": 2, "title": "代区长", "start": "", "end": "present", "rank": "县处级正职", "note": "中共丰泽区委副书记、区政府党组书记、代区长"},
    # 高金全 - 前任区委书记
    {"person_id": 3, "org_id": 1, "title": "中共泉州市丰泽区委书记（前任）", "start": "", "end": "", "rank": "县处级正职", "note": "曾任丰泽区委书记"},
    # 郑燕然 - 常务副区长
    {"person_id": 4, "org_id": 2, "title": "常务副区长", "start": "", "end": "present", "rank": "县处级副职", "note": "中共丰泽区委常委、常务副区长、区政府党组副书记"},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 蔡宁波 - 副区长
    {"person_id": 5, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "县处级副职", "note": "九三学社社员，负责生态环境、卫生健康、市场监管等"},
    # 林伟伟 - 副区长
    {"person_id": 6, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "县处级副职", "note": "负责民政、人社、农业农村、退役军人事务等"},
    # 杨柳刚 - 副区长
    {"person_id": 7, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "县处级副职", "note": "负责文旅、市场监管、知识产权、体育等"},
    # 丁增辉 - 副区长
    {"person_id": 8, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "县处级副职", "note": "负责工信、科技、商务、数字经济等"},
    # 李勇 - 副区长/公安局长
    {"person_id": 9, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "县处级副职", "note": "负责公安、司法、信访、综治等"},
    {"person_id": 9, "org_id": 5, "title": "党委书记、局长", "start": "", "end": "present", "rank": "县处级副职", "note": "泉州市公安局丰泽分局"},
    # 戴隽翔 - 副区长
    {"person_id": 10, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "县处级副职", "note": "负责自然资源、住建、城市管理、交通等"},
    # 陈逢生 - 人大主任
    {"person_id": 11, "org_id": 3, "title": "主任", "start": "", "end": "present", "rank": "县处级正职", "note": "丰泽区人大常委会主任"},
    # 黄泽鹏 - 政协主席（推测）
    {"person_id": 12, "org_id": 4, "title": "主席（推测）", "start": "", "end": "present", "rank": "县处级正职", "note": "丰泽区政协主席"},
]

relationships = [
    # 张照绿 ↔ 张健龙 (区委书记 ↔ 代区长, 党政正职搭档)
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "张照绿任丰泽区委书记，张健龙任代区长，为当前党政正职搭档", "overlap_org": "丰泽区", "overlap_period": "2025-2026"},
    # 张照绿 ↔ 高金全 (前后任区委书记)
    {"person_a": 1, "person_b": 3, "type": "前后任", "context": "高金全曾任丰泽区委书记，张照绿接任", "overlap_org": "中共丰泽区委员会", "overlap_period": "交接期"},
    # 张照绿 ↔ 郑燕然 (书记 ↔ 常委)
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "张照绿为区委书记，郑燕然为区委常委", "overlap_org": "中共丰泽区委员会", "overlap_period": "2025-2026"},
    # 张健龙 ↔ 郑燕然 (区长 ↔ 常务副区长)
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "张健龙为代区长，郑燕然为常务副区长（区政府党组副书记）", "overlap_org": "丰泽区人民政府", "overlap_period": "2025-2026"},
    # 张照绿 ↔ 陈逢生 (区委书记 ↔ 人大主任)
    {"person_a": 1, "person_b": 11, "type": "四套班子同事", "context": "区委书记与人大主任同为区四套班子主要领导，共同出席会议", "overlap_org": "丰泽区", "overlap_period": "2025-2026"},
    # 张照绿 ↔ 黄泽鹏 (区委书记 ↔ 政协主席)
    {"person_a": 1, "person_b": 12, "type": "四套班子同事", "context": "区委书记与政协主席同为区四套班子主要领导", "overlap_org": "丰泽区", "overlap_period": "2025-2026"},
    # 张健龙 ↔ 丁增辉 (区长 ↔ 副区长, 共同调研)
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "张健龙与丁增辉在多个调研、会议中有工作交集", "overlap_org": "丰泽区人民政府", "overlap_period": "2025-2026"},
    # 张健龙 ↔ 李勇 (区长 ↔ 公安局长)
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "李勇为副区长兼公安分局局长，属张健龙领导下的区政府班子", "overlap_org": "丰泽区人民政府", "overlap_period": "2025-2026"},
    # 郑燕然 ↔ 蔡宁波 (正副区长)
    {"person_a": 4, "person_b": 5, "type": "同事", "context": "同属丰泽区人民政府领导班子", "overlap_org": "丰泽区人民政府", "overlap_period": "2025-2026"},
    # 郑燕然 ↔ 林伟伟
    {"person_a": 4, "person_b": 6, "type": "同事", "context": "同属丰泽区人民政府领导班子", "overlap_org": "丰泽区人民政府", "overlap_period": "2025-2026"},
    # 郑燕然 ↔ 杨柳刚
    {"person_a": 4, "person_b": 7, "type": "同事", "context": "同属丰泽区人民政府领导班子", "overlap_org": "丰泽区人民政府", "overlap_period": "2025-2026"},
    # 丁增辉 ↔ 苏伟强 (共同参加信访接待)
    {"person_a": 8, "person_b": 13, "type": "工作交集", "context": "丁增辉与苏伟强共同参加区委主要领导信访接待活动", "overlap_org": "丰泽区", "overlap_period": "2026-07"},
    # 张照绿 ↔ 苏伟强
    {"person_a": 1, "person_b": 13, "type": "上下级", "context": "苏伟强参加张照绿主持的信访接待活动", "overlap_org": "丰泽区", "overlap_period": "2026-07"},
]

# ── HELPERS ──────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_role_color(person):
    """Return r,g,b string for person node based on role."""
    if "书记" in person.get("current_post", "") and "副书记" not in person.get("current_post", ""):
        return "255,50,50"   # Red for Party Secretary
    if "区长" in person.get("current_post", "") or "代区长" in person.get("current_post", ""):
        return "50,100,255"  # Blue for Government head
    if "纪委书记" in person.get("current_post", "") or "监委" in person.get("current_post", ""):
        return "255,165,0"   # Orange for Discipline
    return "100,100,100"    # Grey for others

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(org_type, "200,200,200")

def is_top_leader(person):
    return person["id"] in [1, 2, 3]  # 书记、区长、前任书记

# ── BUILD SQLite ─────────────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, education TEXT,
    party_join TEXT, work_start TEXT,
    current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER, org_id INTEGER,
    title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
    FOREIGN KEY(person_id) REFERENCES persons(id),
    FOREIGN KEY(org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER, person_b INTEGER,
    type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY(person_a) REFERENCES persons(id),
    FOREIGN KEY(person_b) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
                 p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()
conn.close()
print(f"[OK] SQLite database written: {DB_PATH}")

# ── BUILD GEXF ───────────────────────────────────────────────────────

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>China Gov Network Investigator</creator>')
lines.append('    <description>丰泽区领导班子工作关系网络 - 福建省泉州市丰泽区</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attribute declarations
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="org" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('    </attributes>')

# Nodes: persons
lines.append('    <nodes>')
for p in persons:
    c = person_role_color(p)
    sz = "20.0" if is_top_leader(p) else ("12.0" if p["id"] <= 13 else "8.0")
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
    lines.append('        </attvalues>')
    parts = c.split(",")
    lines.append(f'        <viz:color r="{parts[0]}" g="{parts[1]}" b="{parts[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Nodes: organizations
for o in organizations:
    c = org_color(o["type"])
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="org"/>')
    lines.append(f'          <attvalue for="2" value="{esc(o["name"])}"/>')
    lines.append('        </attvalues>')
    parts = c.split(",")
    lines.append(f'        <viz:color r="{parts[0]}" g="{parts[1]}" b="{parts[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
eid = 0

# person -> organization (worked_at)
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

# person <-> person (relationship)
for r in relationships:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"[OK] GEXF graph written: {GEXF_PATH}")

# ── SUMMARY ──────────────────────────────────────────────────────────

print(f"\nSummary:")
print(f"  Persons:         {len(persons)}")
print(f"  Organizations:   {len(organizations)}")
print(f"  Positions:       {len(positions)}")
print(f"  Relationships:   {len(relationships)}")
print(f"  Edges (total):   {eid}")
print(f"\n  DB:   {DB_PATH}")
print(f"  GEXF: {GEXF_PATH}")
