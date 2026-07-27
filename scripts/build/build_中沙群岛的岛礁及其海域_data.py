#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中沙群岛的岛礁及其海域 领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区（名义）/ 西沙区代管
Province: 海南省
Parent city: 三沙市
Region: 中沙群岛的岛礁及其海域
Targets: 区委书记 & 区长
Task ID: hainan_中沙群岛的岛礁及其海域
Model: iagent

=== 核心发现 ===
中沙群岛的岛礁及其海域 **没有独立的区委/区政府领导班子**。

2020年4月18日，国务院批准三沙市设立西沙区、南沙区两个市辖区，
**未设立中沙区**。中沙群岛的岛礁及其海域在行政上由**西沙区代管**
（西沙区管辖西沙群岛并代管中沙群岛）。

中沙群岛由20多个暗礁、暗沙和暗滩组成，唯一露出水面的岛礁是黄岩岛
（由海警巡驻）。该区域无常住居民，不设独立行政管理机构。

因此，本脚本记录的是代管此区域的**三沙市/西沙区级领导**，以及
本区域的历史行政沿革信息。

官方来源（截至2026-07-23）:
- https://www.sansha.gov.cn/ — 三沙市人民政府门户网站
- https://zh.wikipedia.org/wiki/三沙市 — 维基百科
- https://zh.wikipedia.org/wiki/西沙区 — 西沙区维基百科
- https://zh.wikipedia.org/wiki/中沙群岛 — 中沙群岛维基百科
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "中沙群岛的岛礁及其海域"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-23"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 三沙市委书记（代管此区域的上级领导）
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "葛国科",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年8月",
        "birthplace": "广西浦北",
        "education": "浙江大学研究生学历，农学博士学位",
        "party_join": "中共党员（1998年6月加入）",
        "work_start": "2000年",
        "current_post": "中共三沙市委书记",
        "current_org": "中共三沙市委员会",
        "source": "https://zh.wikipedia.org/wiki/葛国科"
    },
    # ════════════════════════════════════════
    # 三沙市长（代管此区域的上级领导）
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "陈儒茂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年9月",
        "birthplace": "待查",
        "education": "大学学历，工学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三沙市人民政府市长",
        "current_org": "三沙市人民政府",
        "source": "https://www.sansha.gov.cn/sansha/sssrmldjs/202312/d6b3e6f4de034b2f8574517d324ac504.shtml"
    },
    # ════════════════════════════════════════
    # 三沙市委副书记
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "江南",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共三沙市委副书记",
        "current_org": "中共三沙市委员会",
        "source": "https://www.sansha.gov.cn/sansha/toutiao/202607/9f2e4cedfab34faab702d93b1790976a.shtml"
    },
    # ════════════════════════════════════════
    # 三沙市副市长
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "林道杰",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三沙市人民政府副市长",
        "current_org": "三沙市人民政府",
        "source": "https://www.sansha.gov.cn/sansha/sssrmldjs/lingdao.shtml"
    },
    {
        "id": 5,
        "name": "李华",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三沙市人民政府副市长",
        "current_org": "三沙市人民政府",
        "source": "https://www.sansha.gov.cn/sansha/sssrmldjs/lingdao.shtml"
    },
    {
        "id": 6,
        "name": "黄广南",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三沙市人民政府副市长",
        "current_org": "三沙市人民政府",
        "source": "https://www.sansha.gov.cn/sansha/sssrmldjs/lingdao.shtml"
    },
    {
        "id": 7,
        "name": "刘云球",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三沙市人民政府副市长",
        "current_org": "三沙市人民政府",
        "source": "https://www.sansha.gov.cn/sansha/sssrmldjs/lingdao.shtml"
    },
    # ════════════════════════════════════════
    # 三沙市人大常委会主任
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "王长仁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965年11月",
        "birthplace": "吉林农安",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三沙市人大常委会主任",
        "current_org": "三沙市人民代表大会常务委员会",
        "source": "https://zh.wikipedia.org/wiki/王长仁"
    },
    # ════════════════════════════════════════
    # 三沙市政府秘书长
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "杜军奎",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三沙市人民政府秘书长",
        "current_org": "三沙市人民政府",
        "source": "https://www.sansha.gov.cn/sansha/sssrmldjs/lingdao.shtml"
    },
    # ════════════════════════════════════════
    # 前任三沙市委书记（2012-2017首任书记）
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "肖杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1960年9月",
        "birthplace": "广东雷州",
        "education": "华南师范大学研究生，法学硕士",
        "party_join": "中共党员",
        "work_start": "1982年7月",
        "current_post": "已卸任（曾任海南省人大常委会副主任）",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/肖杰_(1960年)"
    },
    # ════════════════════════════════════════
    # 首任三沙市长
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "张军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965年1月",
        "birthplace": "广东梅州",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已卸任（曾任海南省人民代表大会常务委员会副秘书长）",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/张军_(1965年)"
    },
    # ════════════════════════════════════════
    # 三沙市政协
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "王有福",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三沙市政协主席",
        "current_org": "三沙市政协",
        "source": "https://www.sansha.gov.cn/"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {
        "id": 1,
        "name": "中共三沙市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共海南省委",
        "location": "西沙区永兴岛"
    },
    {
        "id": 2,
        "name": "三沙市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "海南省人民政府",
        "location": "西沙区永兴岛"
    },
    {
        "id": 3,
        "name": "三沙市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级市",
        "parent": "海南省人大常委会",
        "location": "西沙区永兴岛"
    },
    {
        "id": 4,
        "name": "三沙市政协",
        "type": "政协",
        "level": "地级市",
        "parent": "海南省政协",
        "location": "西沙区永兴岛"
    },
    {
        "id": 5,
        "name": "中共西沙区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共三沙市委",
        "location": "西沙区永兴岛"
    },
    {
        "id": 6,
        "name": "西沙区人民政府",
        "type": "政府",
        "level": "市辖区",
        "parent": "三沙市人民政府",
        "location": "西沙区永兴岛"
    },
    {
        "id": 7,
        "name": "中沙群岛的岛礁及其海域（西沙区代管）",
        "type": "政府",
        "level": "市辖区（名义）",
        "parent": "西沙区人民政府",
        "location": "南海中沙海域"
    },
    {
        "id": 8,
        "name": "三沙市永乐工作委员会",
        "type": "党委",
        "level": "派出机构",
        "parent": "中共三沙市委",
        "location": "永乐群岛"
    },
    {
        "id": 9,
        "name": "黄岩岛（中沙群岛）",
        "type": "乡镇/街道",
        "level": "村级",
        "parent": "西沙区",
        "location": "南海中沙海域"
    },
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 葛国科
    {"person_id": 1, "org_id": 1, "title": "中共三沙市委书记",
     "start_date": "2024年12月", "end_date": "至今", "rank": "正厅级", "note": "跨省履新，此前任广西百色市市长"},
    # 陈儒茂
    {"person_id": 2, "org_id": 2, "title": "三沙市人民政府市长",
     "start_date": "2026年1月（代市长）", "end_date": "至今", "rank": "正厅级", "note": "2026年1月被任命为代市长"},
    {"person_id": 2, "org_id": 2, "title": "三沙市副市长",
     "start_date": "2022年?", "end_date": "2026年1月", "rank": "副厅级", "note": ""},
    # 江南
    {"person_id": 3, "org_id": 1, "title": "中共三沙市委副书记",
     "start_date": "待查", "end_date": "至今", "rank": "副厅级", "note": ""},
    # 林道杰
    {"person_id": 4, "org_id": 2, "title": "三沙市人民政府副市长",
     "start_date": "待查", "end_date": "至今", "rank": "副厅级", "note": ""},
    # 李华
    {"person_id": 5, "org_id": 2, "title": "三沙市人民政府副市长",
     "start_date": "待查", "end_date": "至今", "rank": "副厅级", "note": ""},
    # 黄广南
    {"person_id": 6, "org_id": 2, "title": "三沙市人民政府副市长",
     "start_date": "待查", "end_date": "至今", "rank": "副厅级", "note": ""},
    # 刘云球
    {"person_id": 7, "org_id": 2, "title": "三沙市人民政府副市长",
     "start_date": "待查", "end_date": "至今", "rank": "副厅级", "note": ""},
    # 王长仁
    {"person_id": 8, "org_id": 3, "title": "三沙市人大常委会主任",
     "start_date": "2022年1月", "end_date": "至今", "rank": "正厅级", "note": ""},
    # 杜军奎
    {"person_id": 9, "org_id": 2, "title": "三沙市人民政府秘书长",
     "start_date": "待查", "end_date": "至今", "rank": "正处级", "note": ""},
    # 肖杰（首任书记）
    {"person_id": 10, "org_id": 1, "title": "中共三沙市委书记",
     "start_date": "2012年7月", "end_date": "2017年4月", "rank": "正厅级", "note": "三沙市首任市委书记"},
    # 张军（首任市长）
    {"person_id": 11, "org_id": 2, "title": "三沙市人民政府市长",
     "start_date": "2012年7月", "end_date": "2017年?", "rank": "正厅级", "note": "三沙市首任市长"},
    # 王有福
    {"person_id": 12, "org_id": 4, "title": "三沙市政协主席",
     "start_date": "待查", "end_date": "至今", "rank": "正厅级", "note": ""},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 书记 ↔ 市长（当前搭档）
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "葛国科任市委书记，陈儒茂任市长，共同搭档治理三沙市（代管中沙群岛）",
     "overlap_org": "三沙市",
     "overlap_period": "2026年1月至今"},
    # 书记 ↔ 副书记
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "葛国科与江南在三沙市委搭班子",
     "overlap_org": "中共三沙市委员会",
     "overlap_period": "至今"},
    # 市长 ↔ 副市长们
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "陈儒茂与林道杰同为三沙市政府领导",
     "overlap_org": "三沙市人民政府",
     "overlap_period": "至今"},
    {"person_a": 2, "person_b": 5, "type": "overlap",
     "context": "陈儒茂与李华同为三沙市政府领导",
     "overlap_org": "三沙市人民政府",
     "overlap_period": "至今"},
    {"person_a": 2, "person_b": 6, "type": "overlap",
     "context": "陈儒茂与黄广南同为三沙市政府领导",
     "overlap_org": "三沙市人民政府",
     "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "overlap",
     "context": "陈儒茂与刘云球同为三沙市政府领导",
     "overlap_org": "三沙市人民政府",
     "overlap_period": "至今"},
    # 人大主任 ↔ 书记
    {"person_a": 8, "person_b": 1, "type": "overlap",
     "context": "王长仁任人大常委会主任，葛国科任市委书记",
     "overlap_org": "三沙市",
     "overlap_period": "2024年12月至今"},
    # 书记前后任
    {"person_a": 10, "person_b": 1, "type": "predecessor_successor",
     "context": "肖杰为首任市委书记，葛国科为现任书记",
     "overlap_org": "中共三沙市委员会",
     "overlap_period": "2012-2024"},
    # 市长前后任
    {"person_a": 11, "person_b": 2, "type": "predecessor_successor",
     "context": "张军为首任市长，陈儒茂为现任市长",
     "overlap_org": "三沙市人民政府",
     "overlap_period": "2012-2026"},
]

# =========================================================================
# Helper: XML escape
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

# =========================================================================
# 5. SQLite Database
# =========================================================================
print(f"[DB] Creating {DB_PATH} ...")
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Create tables
cur.executescript("""
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

# Insert persons
for p in persons:
    cur.execute("""INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
         p["education"], p["party_join"], p["work_start"], p["current_post"],
         p["current_org"], p["source"]))

# Insert organizations
for o in organizations:
    cur.execute("""INSERT INTO organizations (id, name, type, level, parent, location)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

# Insert positions
for pos in positions:
    cur.execute("""INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"],
         pos["end_date"], pos["rank"], pos["note"]))

# Insert relationships
for r in relationships:
    cur.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (r["person_a"], r["person_b"], r["type"], r["context"],
         r["overlap_org"], r["overlap_period"]))

conn.commit()
conn.close()
print(f"[DB] Done. {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships.")

# =========================================================================
# 6. GEXF Graph
# =========================================================================
print(f"[GEXF] Creating {GEXF_PATH} ...")

def person_color(name, current_post):
    """Assign color based on role."""
    post = current_post or ""
    if "书记" in post and "纪委" not in post:
        return "255,50,50"   # Red - Party Secretary
    if "市长" in post or "副市长" in post:
        return "50,100,255"  # Blue - Government
    if "人大" in post:
        return "200,255,255" # Cyan - NPC
    if "政协" in post:
        return "255,240,200" # Cream - CPPCC
    return "100,100,100"     # Grey - Other

def person_size(name, current_post):
    """Assign size based on role importance."""
    post = current_post or ""
    if "书记" in post and "纪委" not in post:
        return "20.0"
    if "市长" in post:
        return "20.0"
    if "副市长" in post or "秘书长" in post:
        return "12.0"
    if "人大" in post or "政协" in post:
        return "12.0"
    return "12.0"

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
    }
    return colors.get(org_type, "200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
lines.append('    <creator>Gov-Relation Research Agent</creator>')
lines.append(f'    <description>{SLUG} - 西沙区代管区域，无独立领导班子</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="organization_type" type="string"/>')
lines.append('      <attribute id="2" title="role" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('      <attribute id="2" title="start" type="string"/>')
lines.append('      <attribute id="3" title="end" type="string"/>')
lines.append('    </attributes>')

# Nodes: Persons
lines.append('    <nodes>')
for p in persons:
    c = person_color(p["name"], p.get("current_post", ""))
    sz = person_size(p["name"], p.get("current_post", ""))
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value=""/>')
    lines.append(f'          <attvalue for="2" value="{esc(p.get("current_post", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Nodes: Organizations
for o in organizations:
    c = org_color(o.get("type", ""))
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
    lines.append(f'          <attvalue for="2" value=""/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges: person→organization (worked_at)
lines.append('    <edges>')
edge_id = 0
for pos in positions:
    edge_id += 1
    lines.append(f'      <edge id="e{edge_id}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(pos.get("start_date", ""))}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(pos.get("end_date", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

# Edges: person↔person (relationship)
for r in relationships:
    edge_id += 1
    lines.append(f'      <edge id="e{edge_id}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_period", ""))}"/>')
    lines.append(f'          <attvalue for="3" value=""/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"[GEXF] Done. {len(persons)+len(organizations)} nodes, {edge_id} edges.")
print(f"\n{'='*60}")
print(f"Build complete!")
print(f"  DB:    {DB_PATH}")
print(f"  GEXF:  {GEXF_PATH}")
print(f"{'='*60}")
