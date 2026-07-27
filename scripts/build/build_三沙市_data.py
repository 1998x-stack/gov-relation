#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三沙市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 地级市
Province: 海南省
Region: 三沙市
Targets: 市委书记 & 市长
Task ID: hainan_三沙市
Model: iagent

官方来源 (as of 2026-07-23):
- https://www.sansha.gov.cn/ — 三沙市人民政府门户网站
- https://zh.wikipedia.org/wiki/三沙市 — 维基百科
- https://zh.wikipedia.org/wiki/葛国科 — 葛国科简历
- https://zh.wikipedia.org/wiki/文斌_(1972年) — 文斌简历

当前在任 (as of 2026-07-23):
- 市委书记: 葛国科（2024年12月履新，此前任广西百色市市长）
- 代市长: 陈儒茂（2026年1月起任三沙市代市长）
- 前任市长: 文斌（2023年12月-2026年1月）
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "三沙市"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-23"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：市委书记（正厅级/省管）
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "葛国科",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年8月",
        "birthplace": "广西浦北",
        "education": "浙江大学（博士？不详）",
        "party_join": "中共党员（1998年加入）",
        "work_start": "2000年左右",
        "current_post": "中共三沙市委书记",
        "current_org": "中共三沙市委员会",
        "source": "https://zh.wikipedia.org/wiki/葛国科"
    },
    # ════════════════════════════════════════
    # 核心领导：市长/代市长（正厅级）
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "陈儒茂",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三沙市代市长",
        "current_org": "三沙市人民政府",
        "source": "https://www.sansha.gov.cn/"
    },
    # ════════════════════════════════════════
    # 前任市长（数据参考）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "文斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年6月",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已卸任三沙市市长",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/文斌_(1972年)"
    },
    # ════════════════════════════════════════
    # 前任市委书记（数据参考）
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "袁光平",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已卸任三沙市委书记",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/袁光平"
    },
    # ════════════════════════════════════════
    # 人大常委会主任
    # ════════════════════════════════════════
    {
        "id": 5,
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
    # 副市长
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "徐志飞",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三沙市副市长",
        "current_org": "三沙市人民政府",
        "source": "https://zh.wikipedia.org/wiki/三沙市"
    },
    # ════════════════════════════════════════
    # 前任市长 邓忠
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "邓忠",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "1968年",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已卸任三沙市市长",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/邓忠_(1968年)"
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
        "name": "广西百色市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广西壮族自治区人民政府",
        "location": "广西百色"
    },
    {
        "id": 5,
        "name": "广西玉林市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广西壮族自治区党委",
        "location": "广西玉林"
    },
    {
        "id": 6,
        "name": "广西容县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共玉林市委",
        "location": "广西容县"
    },
    {
        "id": 7,
        "name": "广西容县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "玉林市人民政府",
        "location": "广西容县"
    },
    {
        "id": 8,
        "name": "广西北流市委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共玉林市委",
        "location": "广西北流"
    },
    {
        "id": 9,
        "name": "广西壮族自治区党委改革办",
        "type": "党委",
        "level": "省级",
        "parent": "中共广西壮族自治区党委",
        "location": "广西南宁"
    },
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 葛国科
    {"person_id": 1, "org_id": 1, "title": "中共三沙市委书记",
     "start_date": "2024年12月", "end_date": "至今", "rank": "正厅级", "note": "跨省履新"},
    {"person_id": 1, "org_id": 4, "title": "百色市人民政府市长",
     "start_date": "2021年4月", "end_date": "2024年12月", "rank": "正厅级", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "广西自治区党委改革办专职副主任",
     "start_date": "2019年4月", "end_date": "2021年4月", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 5, "title": "玉林市委常委、秘书长",
     "start_date": "2016年6月", "end_date": "2019年4月", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "北流市委书记（兼任）",
     "start_date": "2018年6月", "end_date": "2019年4月", "rank": "副厅级", "note": "兼任"},
    {"person_id": 1, "org_id": 6, "title": "中共容县县委书记",
     "start_date": "2014年1月", "end_date": "2016年5月", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 7, "title": "容县人民政府县长（代县长、县长）",
     "start_date": "2013年6月", "end_date": "2014年1月", "rank": "正处级", "note": "代县长后正式当选"},
    # 陈儒茂
    {"person_id": 2, "org_id": 2, "title": "三沙市代市长",
     "start_date": "2026年1月", "end_date": "至今", "rank": "正厅级", "note": "2026年1月被任命为代市长"},
    {"person_id": 2, "org_id": 2, "title": "三沙市副市长",
     "start_date": "2022年?", "end_date": "2026年1月", "rank": "副厅级", "note": ""},
    # 文斌
    {"person_id": 3, "org_id": 2, "title": "三沙市人民政府市长",
     "start_date": "2023年12月", "end_date": "2026年1月", "rank": "正厅级", "note": ""},
    # 袁光平
    {"person_id": 4, "org_id": 1, "title": "中共三沙市委书记",
     "start_date": "2021年12月", "end_date": "2024年12月", "rank": "正厅级", "note": ""},
    # 王长仁
    {"person_id": 5, "org_id": 3, "title": "三沙市人大常委会主任",
     "start_date": "2022年1月", "end_date": "至今", "rank": "正厅级", "note": ""},
    # 徐志飞
    {"person_id": 6, "org_id": 2, "title": "三沙市副市长",
     "start_date": "待查", "end_date": "至今", "rank": "副厅级", "note": ""},
    # 邓忠
    {"person_id": 7, "org_id": 2, "title": "三沙市人民政府市长",
     "start_date": "2019年12月", "end_date": "2023年12月", "rank": "正厅级", "note": ""},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 市委书记 ↔ 代市长（当前搭档）
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "葛国科任市委书记，陈儒茂任代市长，共同搭档",
     "overlap_org": "三沙市",
     "overlap_period": "2026年1月至今"},
    # 葛国科 ↔ 袁光平（前后任书记）
    {"person_a": 1, "person_b": 4, "type": "predecessor_successor",
     "context": "葛国科接替袁光平任三沙市委书记",
     "overlap_org": "中共三沙市委员会",
     "overlap_period": "2024年12月"},
    # 陈儒茂 ↔ 文斌（前后任市长）
    {"person_a": 2, "person_b": 3, "type": "predecessor_successor",
     "context": "陈儒茂接替文斌任三沙市代市长",
     "overlap_org": "三沙市人民政府",
     "overlap_period": "2026年1月"},
    # 文斌 ↔ 邓忠（前后任市长）
    {"person_a": 3, "person_b": 7, "type": "predecessor_successor",
     "context": "文斌接替邓忠任三沙市市长",
     "overlap_org": "三沙市人民政府",
     "overlap_period": "2023年12月"},
    # 王长仁 — 三沙人大主任
    {"person_a": 5, "person_b": 1, "type": "overlap",
     "context": "王长仁任人大常委会主任，葛国科任市委书记",
     "overlap_org": "三沙市",
     "overlap_period": "2024年12月至今"},
    {"person_a": 5, "person_b": 2, "type": "overlap",
     "context": "王长仁任人大常委会主任，陈儒茂任代市长",
     "overlap_org": "三沙市",
     "overlap_period": "2026年1月至今"},
    # 陈儒茂 ↔ 徐志飞（副市长同事）
    {"person_a": 2, "person_b": 6, "type": "overlap",
     "context": "陈儒茂与徐志飞先后任三沙市副市长",
     "overlap_org": "三沙市人民政府",
     "overlap_period": "2022年-2026年"},
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
    if "市长" in post or "代市长" in post or "副市长" in post:
        return "50,100,255"  # Blue - Government
    if "人大" in post:
        return "200,255,255" # Cyan - NPC
    return "100,100,100"     # Grey - Other

def person_size(name, current_post):
    """Assign size based on role importance."""
    post = current_post or ""
    if "书记" in post and "纪委" not in post:
        return "20.0"
    if "市长" in post or "代市长" in post:
        return "20.0"
    if "副市长" in post or "人大" in post:
        return "12.0"
    return "12.0"

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
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
lines.append('    <description>三沙市领导班子工作关系网络</description>')
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
