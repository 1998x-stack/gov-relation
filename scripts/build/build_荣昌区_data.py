#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Rongchang District leadership network."""

import sqlite3
import os
import json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/chongqing_荣昌区")
DB_PATH = os.path.join(STAGING, "荣昌区_network.db")
GEXF_PATH = os.path.join(STAGING, "荣昌区_network.gexf")

os.makedirs(STAGING, exist_ok=True)

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── District Party Secretary (区委书记) ──
    {"id": 1, "name": "万容", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共重庆市荣昌区委书记", "current_org": "中共重庆市荣昌区委员会",
     "source": "https://www.rongchang.gov.cn/zwxx/rcdt/202607/t20260715_15822738.html"},

    # ── District Mayor (区长) ──
    {"id": 2, "name": "廖传锦", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-01", "birthplace": "", "education": "研究生学历，工学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "重庆市荣昌区委副书记、区长、区政府党组书记", "current_org": "重庆市荣昌区人民政府",
     "source": "https://www.rongchang.gov.cn/zwgk_264/ldxx/qzf/ghb/202003/t20200327_6323531.html"},

    # ── Deputy District Party Secretary / Organization Dept Head ──
    {"id": 3, "name": "李学义", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "荣昌区委副书记、组织部部长", "current_org": "中共重庆市荣昌区委员会",
     "source": "https://www.rongchang.gov.cn/zwxx/rcdt/202607/t20260701_15789294.html"},

    # ── District Standing Committee / Propaganda Head ──
    {"id": 4, "name": "谢勇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "荣昌区委常委、宣传部部长", "current_org": "中共重庆市荣昌区委员会",
     "source": "https://www.rongchang.gov.cn/zwxx/rcdt/202607/t20260710_15812965.html"},

    # ── District Standing Committee / Executive Vice Mayor (常务副区长) ──
    {"id": 5, "name": "程建林", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-12", "birthplace": "", "education": "研究生学历，管理学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "荣昌区委常委、副区长、区政府党组成员", "current_org": "重庆市荣昌区人民政府",
     "source": "https://www.rongchang.gov.cn/zwgk_264/ldxx/qzf/cjl/202007/t20200717_7692447.html"},

    # ── District Standing Committee / High-tech Zone Secretary ──
    {"id": 6, "name": "李皓", "gender": "男", "ethnicity": "蒙古族",
     "birth": "1971-09", "birthplace": "", "education": "大学学历，农学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "荣昌区委常委、区政府党组成员、荣昌高新区党工委书记", "current_org": "重庆市荣昌区人民政府",
     "source": "https://www.rongchang.gov.cn/zwgk_264/ldxx/qzf/lh/202602/t20260202_15371977.html"},

    # ── Vice Mayor / Public Security ──
    {"id": 7, "name": "张元斌", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-02", "birthplace": "", "education": "中央党校大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "荣昌区副区长、区政府党组成员、区公安局局长", "current_org": "重庆市荣昌区人民政府",
     "source": "https://www.rongchang.gov.cn/zwgk_264/ldxx/qzf/zf_zyb/202406/t20240613_13291899.html"},

    # ── Vice Mayor ──
    {"id": 8, "name": "李德伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-04", "birthplace": "", "education": "研究生（地方）",
     "party_join": "中共党员", "work_start": "",
     "current_post": "荣昌区副区长、区政府党组成员", "current_org": "重庆市荣昌区人民政府",
     "source": "https://www.rongchang.gov.cn/zwgk_264/ldxx/qzf/ldw/202201/t20220112_10297416.html"},

    # ── Vice Mayor ──
    {"id": 9, "name": "王媛媛", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "荣昌区副区长", "current_org": "重庆市荣昌区人民政府",
     "source": "https://www.rongchang.gov.cn/zwgk_264/ldxx/"},

    # ── Vice Mayor ──
    {"id": 10, "name": "周鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "荣昌区副区长", "current_org": "重庆市荣昌区人民政府",
     "source": "https://www.rongchang.gov.cn/zwgk_264/ldxx/"},

    # ── Vice Mayor ──
    {"id": 11, "name": "夏定文", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "荣昌区副区长", "current_org": "重庆市荣昌区人民政府",
     "source": "https://www.rongchang.gov.cn/zwgk_264/ldxx/"},
]

organizations = [
    {"id": 1, "name": "中共重庆市荣昌区委员会", "type": "党委", "level": "区级", "parent": "中共重庆市委", "location": "重庆市荣昌区"},
    {"id": 2, "name": "重庆市荣昌区人民政府", "type": "政府", "level": "区级", "parent": "重庆市人民政府", "location": "重庆市荣昌区"},
    {"id": 3, "name": "荣昌高新区党工委", "type": "开发区", "level": "区级", "parent": "荣昌高新区管委会", "location": "重庆市荣昌区"},
    {"id": 4, "name": "荣昌区公安局", "type": "政府", "level": "区级", "parent": "重庆市荣昌区人民政府", "location": "重庆市荣昌区"},
]

positions = [
    # 万容
    {"person_id": 1, "org_id": 1, "title": "中共重庆市荣昌区委书记", "start": "", "end": "present", "rank": "正厅级", "note": "区委一把手"},
    # 廖传锦
    {"person_id": 2, "org_id": 2, "title": "重庆市荣昌区人民政府区长", "start": "", "end": "present", "rank": "正厅级", "note": "区政府一把手"},
    {"person_id": 2, "org_id": 1, "title": "荣昌区委副书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 李学义
    {"person_id": 3, "org_id": 1, "title": "荣昌区委副书记、组织部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 谢勇
    {"person_id": 4, "org_id": 1, "title": "荣昌区委常委、宣传部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 程建林
    {"person_id": 5, "org_id": 2, "title": "荣昌区委常委、副区长", "start": "", "end": "present", "rank": "副厅级", "note": "常务副区长"},
    # 李皓
    {"person_id": 6, "org_id": 2, "title": "荣昌区委常委、区政府党组成员", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 3, "title": "荣昌高新区党工委书记", "start": "", "end": "present", "rank": "", "note": ""},
    # 张元斌
    {"person_id": 7, "org_id": 2, "title": "荣昌区副区长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 4, "title": "荣昌区公安局局长", "start": "", "end": "present", "rank": "", "note": ""},
    # 李德伟
    {"person_id": 8, "org_id": 2, "title": "荣昌区副区长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 王媛媛
    {"person_id": 9, "org_id": 2, "title": "荣昌区副区长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 周鹏
    {"person_id": 10, "org_id": 2, "title": "荣昌区副区长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 夏定文
    {"person_id": 11, "org_id": 2, "title": "荣昌区副区长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
]

relationships = [
    # 万容 ↔ 廖传锦 (district party secretary and mayor)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "荣昌区党政一把手搭档", "overlap_org": "荣昌区委/区政府", "overlap_period": "现任"},
    # 程建林 ↔ 廖传锦 (Vice mayor and mayor)
    {"person_a": 5, "person_b": 2, "type": "superior_subordinate", "context": "常务副区长协助区长工作", "overlap_org": "荣昌区人民政府", "overlap_period": "现任"},
    # 李学义 ↔ 万容 (Party deputy and secretary)
    {"person_a": 3, "person_b": 1, "type": "superior_subordinate", "context": "区委副书记协助区委书记工作", "overlap_org": "荣昌区委", "overlap_period": "现任"},
    # Various vice mayors working under mayor
    {"person_a": 7, "person_b": 2, "type": "superior_subordinate", "context": "副区长协助区长分管公安、司法", "overlap_org": "荣昌区人民政府", "overlap_period": "现任"},
    {"person_a": 8, "person_b": 2, "type": "superior_subordinate", "context": "副区长协助区长工作", "overlap_org": "荣昌区人民政府", "overlap_period": "现任"},
    {"person_a": 9, "person_b": 2, "type": "superior_subordinate", "context": "副区长协助区长工作", "overlap_org": "荣昌区人民政府", "overlap_period": "现任"},
    {"person_a": 10, "person_b": 2, "type": "superior_subordinate", "context": "副区长协助区长工作", "overlap_org": "荣昌区人民政府", "overlap_period": "现任"},
    {"person_a": 11, "person_b": 2, "type": "superior_subordinate", "context": "副区长协助区长工作", "overlap_org": "荣昌区人民政府", "overlap_period": "现任"},
]


# ── BUILD DATABASE ──────────────────────────────────────────────────

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    name TEXT, gender TEXT, ethnicity TEXT, birth TEXT, birthplace TEXT,
    education TEXT, party_join TEXT, work_start TEXT,
    current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER, org_id INTEGER, title TEXT, start TEXT, end TEXT,
    rank TEXT, note TEXT,
    FOREIGN KEY(person_id) REFERENCES persons(id),
    FOREIGN KEY(org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER, person_b INTEGER, type TEXT, context TEXT,
    overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY(person_a) REFERENCES persons(id),
    FOREIGN KEY(person_b) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("""INSERT OR REPLACE INTO persons
        (id, name, gender, ethnicity, birth, birthplace, education,
         party_join, work_start, current_post, current_org, source)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
        (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
         p["birthplace"], p["education"], p["party_join"], p["work_start"],
         p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""INSERT OR REPLACE INTO organizations
        (id, name, type, level, parent, location)
        VALUES (?,?,?,?,?,?)""",
        (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("""INSERT INTO positions
        (person_id, org_id, title, start, end, rank, note)
        VALUES (?,?,?,?,?,?,?)""",
        (pos["person_id"], pos["org_id"], pos["title"],
         pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("""INSERT INTO relationships
        (person_a, person_b, type, context, overlap_org, overlap_period)
        VALUES (?,?,?,?,?,?)""",
        (r["person_a"], r["person_b"], r["type"],
         r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()
conn.close()

print(f"✓ SQLite DB created: {DB_PATH}")
print(f"  - {len(persons)} persons")
print(f"  - {len(organizations)} organizations")
print(f"  - {len(positions)} positions")
print(f"  - {len(relationships)} relationships")


# ── BUILD GEXF ──────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Red for party secretary, blue for government, orange for discipline, grey for others."""
    if "书记" in p["current_post"] and "区委书记" in p["current_post"]:
        return "255,50,50"
    elif "区长" in p["current_post"] or "副区长" in p["current_post"]:
        return "50,100,255"
    else:
        return "100,100,100"

def org_color(o):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
    }
    return colors.get(o["type"], "200,200,200")

def is_top_leader(p):
    return p["id"] in (1, 2)

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>重庆市荣昌区领导班子工作关系网络</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('    </attributes>')

# Edge attributes
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('    </attributes>')

# Nodes
lines.append('    <nodes>')
for p in persons:
    c = person_color(p)
    sz = "20.0" if is_top_leader(p) else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

for o in organizations:
    c = org_color(o)
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

for r in relationships:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✓ GEXF graph created: {GEXF_PATH}")
print(f"  - {len(persons)} person nodes")
print(f"  - {len(organizations)} organization nodes")
print(f"  - {len(positions) + len(relationships)} edges")

print("\nDone. All artifacts generated.")
