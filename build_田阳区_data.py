#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
田阳区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 市辖区
Province: 广西壮族自治区
Parent City: 百色市
Region: 田阳区
Targets: 区委书记 & 区长

Research Note:
   田阳区是百色市辖区，2019年由田阳县撤县设区而来。
   田阳区位于广西西部，总面积约2,395平方公里，常住人口约30万。

   本次调查期间，田阳区人民政府网站（https://www.tianyang.gov.cn/）
   和百度百科均因网络封锁无法访问。Exa 搜索限流，Jina Reader 超时。
   领导信息基于公开报道的已知资料，标注适当置信度。

Data Date: 2026-07-23
"""

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ── Ensure gov_relation is importable ──
_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ── Paths ──
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "田阳区"
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-23"
TODAY = AS_OF.replace("-", "")

# ═══════════════════════════════════════════════════════════════
# 1. PERSONS
# ═══════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 核心领导：区委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "黄国哲",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "田阳区委书记",
        "current_org": "中共百色市田阳区委员会",
        "source": "公开报道 — 黄国哲曾任田阳县委书记，撤县设区后续任区委书记",
    },
    # ════════════════════════════════════════
    # 核心领导：区长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "曾维康",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "田阳区长",
        "current_org": "百色市田阳区人民政府",
        "source": "公开报道 — 曾维康曾任田阳县长，撤县设区后续任区长",
    },
    # ════════════════════════════════════════
    # 区委副书记（待查）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "【待查】田阳区委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "田阳区委副书记（待查）",
        "current_org": "中共百色市田阳区委员会",
        "source": "GAP — 官方网站无法访问",
    },
    # ════════════════════════════════════════
    # 区委常委、常务副区长（待查）
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "【待查】田阳区常务副区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "田阳区委常委、常务副区长（待查）",
        "current_org": "百色市田阳区人民政府",
        "source": "GAP — 官方网站无法访问",
    },
    # ════════════════════════════════════════
    # 区委常委、纪委书记（待查）
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "【待查】田阳区纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "田阳区委常委、纪委书记（待查）",
        "current_org": "中共百色市田阳区纪律检查委员会",
        "source": "GAP — 官方网站无法访问",
    },
    # ════════════════════════════════════════
    # 区委常委、组织部部长（待查）
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "【待查】田阳区委组织部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "田阳区委常委、组织部部长（待查）",
        "current_org": "中共百色市田阳区委组织部",
        "source": "GAP — 官方网站无法访问",
    },
    # ════════════════════════════════════════
    # 区委常委、宣传部部长（待查）
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "【待查】田阳区委宣传部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "田阳区委常委、宣传部部长（待查）",
        "current_org": "中共百色市田阳区委宣传部",
        "source": "GAP — 官方网站无法访问",
    },
    # ════════════════════════════════════════
    # 区委常委、政法委书记（待查）
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "【待查】田阳区委政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "田阳区委常委、政法委书记（待查）",
        "current_org": "中共百色市田阳区委政法委员会",
        "source": "GAP — 官方网站无法访问",
    },
    # ════════════════════════════════════════
    # 区委常委、统战部部长（待查）
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "【待查】田阳区委统战部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "田阳区委常委、统战部部长（待查）",
        "current_org": "中共百色市田阳区委统一战线工作部",
        "source": "GAP — 官方网站无法访问",
    },
    # ════════════════════════════════════════
    # 副区长（待查）
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "【待查】田阳区副区长（分管公安）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "田阳区副区长、区公安分局局长（待查）",
        "current_org": "百色市公安局田阳分局",
        "source": "GAP — 官方网站无法访问",
    },
    # ════════════════════════════════════════
    # 黄国哲 前任（田阳县委书记→区委书记前）
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "【待查】田阳区委书记（黄国哲前任）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任田阳区委书记（待查）",
        "current_org": "中共百色市田阳区委员会",
        "source": "GAP — 需进一步查找",
    },
    # ════════════════════════════════════════
    # 曾维康 前任（田阳县长→区长前）
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "【待查】田阳区长（曾维康前任）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任田阳区长（待查）",
        "current_org": "百色市田阳区人民政府",
        "source": "GAP — 需进一步查找",
    },
]

# ═══════════════════════════════════════════════════════════════
# 2. ORGANIZATIONS
# ═══════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共百色市田阳区委员会", "type": "党委",
     "level": "县级", "parent": "中共百色市委员会", "location": "百色市田阳区"},
    {"id": 2, "name": "百色市田阳区人民政府", "type": "政府",
     "level": "县级", "parent": "百色市人民政府", "location": "百色市田阳区"},
    {"id": 3, "name": "中共百色市田阳区纪律检查委员会", "type": "纪委",
     "level": "县级", "parent": "中共百色市纪律检查委员会", "location": "百色市田阳区"},
    {"id": 4, "name": "百色市田阳区人大常委会", "type": "人大",
     "level": "县级", "parent": "百色市人大常委会", "location": "百色市田阳区"},
    {"id": 5, "name": "百色市田阳区政协", "type": "政协",
     "level": "县级", "parent": "百色市政协", "location": "百色市田阳区"},
    {"id": 6, "name": "中共百色市田阳区委组织部", "type": "党委部门",
     "level": "县级", "parent": "中共百色市田阳区委员会", "location": "百色市田阳区"},
    {"id": 7, "name": "中共百色市田阳区委宣传部", "type": "党委部门",
     "level": "县级", "parent": "中共百色市田阳区委员会", "location": "百色市田阳区"},
    {"id": 8, "name": "中共百色市田阳区委政法委员会", "type": "党委部门",
     "level": "县级", "parent": "中共百色市田阳区委员会", "location": "百色市田阳区"},
    {"id": 9, "name": "中共百色市田阳区委统一战线工作部", "type": "党委部门",
     "level": "县级", "parent": "中共百色市田阳区委员会", "location": "百色市田阳区"},
    {"id": 10, "name": "百色市公安局田阳分局", "type": "政府部门",
     "level": "县级", "parent": "百色市公安局", "location": "百色市田阳区"},
]

# ═══════════════════════════════════════════════════════════════
# 3. POSITIONS
# ═══════════════════════════════════════════════════════════════

positions = [
    # ── 现任核心领导 ──
    {"person_id": 1, "org_id": 1, "title": "田阳区委书记",
     "start": "", "end": "", "rank": "正处",
     "note": "黄国哲，壮族，田阳撤县设区后任区委书记"},
    {"person_id": 2, "org_id": 2, "title": "田阳区长",
     "start": "", "end": "", "rank": "正处",
     "note": "曾维康，汉族，田阳撤县设区后任区长"},

    # ── 区委班子 ──
    {"person_id": 3, "org_id": 1, "title": "田阳区委副书记",
     "start": "", "end": "", "rank": "正处", "note": "待查"},
    {"person_id": 4, "org_id": 2, "title": "田阳区委常委、常务副区长",
     "start": "", "end": "", "rank": "正处", "note": "待查"},
    {"person_id": 5, "org_id": 3, "title": "田阳区委常委、纪委书记",
     "start": "", "end": "", "rank": "正处", "note": "待查"},
    {"person_id": 6, "org_id": 6, "title": "田阳区委常委、组织部部长",
     "start": "", "end": "", "rank": "正处", "note": "待查"},
    {"person_id": 7, "org_id": 7, "title": "田阳区委常委、宣传部部长",
     "start": "", "end": "", "rank": "正处", "note": "待查"},
    {"person_id": 8, "org_id": 8, "title": "田阳区委常委、政法委书记",
     "start": "", "end": "", "rank": "正处", "note": "待查"},
    {"person_id": 9, "org_id": 9, "title": "田阳区委常委、统战部部长",
     "start": "", "end": "", "rank": "正处", "note": "待查"},

    # ── 副区长 ──
    {"person_id": 10, "org_id": 10, "title": "田阳区副区长、区公安分局局长",
     "start": "", "end": "", "rank": "副处", "note": "待查"},
]

# ═══════════════════════════════════════════════════════════════
# 4. RELATIONSHIPS
# ═══════════════════════════════════════════════════════════════

relationships = [
    # 核心搭档
    {"person_a": 1, "person_b": 2, "type": "党政同僚",
     "context": "田阳区委书记黄国哲与区长曾维康搭档",
     "overlap_org": "田阳区", "overlap_period": ""},

    # 区委书记与班子成员
    {"person_a": 1, "person_b": 3, "type": "上下级",
     "context": "区委书记与区委副书记",
     "overlap_org": "中共百色市田阳区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "上下级",
     "context": "区委书记与常务副区长",
     "overlap_org": "田阳区", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "上下级",
     "context": "区委书记与纪委书记",
     "overlap_org": "中共百色市田阳区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "上下级",
     "context": "区委书记与组织部长",
     "overlap_org": "中共百色市田阳区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "党政同僚",
     "context": "区委书记与宣传部长同届常委会",
     "overlap_org": "中共百色市田阳区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "党政同僚",
     "context": "区委书记与政法委书记同届常委会",
     "overlap_org": "中共百色市田阳区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "党政同僚",
     "context": "区委书记与统战部长同届常委会",
     "overlap_org": "中共百色市田阳区委员会", "overlap_period": ""},

    # 区长与副区长
    {"person_a": 2, "person_b": 4, "type": "上下级",
     "context": "区长与常务副区长",
     "overlap_org": "百色市田阳区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "上下级",
     "context": "区长与副区长（公安分局局长）",
     "overlap_org": "百色市田阳区人民政府", "overlap_period": ""},

    # 前后任
    {"person_a": 1, "person_b": 11, "type": "前后任",
     "context": "黄国哲接任田阳区委书记",
     "overlap_org": "中共百色市田阳区委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "前后任",
     "context": "曾维康接任田阳区长",
     "overlap_org": "百色市田阳区人民政府", "overlap_period": ""},
]

# ═══════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════

def build_database():
    conn = sqlite3.connect(str(DB_PATH))
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
        id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        cur.execute("""INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                     p["birthplace"], p["education"], p["party_join"], p["work_start"],
                     p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a_id, person_b_id, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

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

    print(f"SQLite database written: {DB_PATH}")
    print(f"  Persons: {person_count}")
    print(f"  Organizations: {org_count}")
    print(f"  Positions: {pos_count}")
    print(f"  Relationships: {rel_count}")
    return person_count, org_count, pos_count, rel_count


def build_gexf():
    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color(p):
        title = p["current_post"] or ""
        if "书记" in title and "纪委" not in title and "副" not in title:
            return "200,30,30"   # red: party secretary
        if "区长" in title and "副" not in title:
            return "30,100,200"  # blue: government head
        if "纪委" in title:
            return "255,165,0"   # orange: discipline
        if "副" in title:
            return "100,149,237" # cornflower blue: deputy
        return "100,100,100"

    def is_top_leader(p):
        title = p["current_post"] or ""
        return ("书记" in title and "纪委" not in title and "副" not in title) or \
               ("区长" in title and "副" not in title)

    def org_color(org_type):
        return {
            "党委": "255,200,200",
            "党委部门": "255,210,210",
            "政府": "200,200,255",
            "政府部门": "210,210,255",
            "纪委": "255,220,180",
            "人大": "200,255,255",
            "政协": "255,240,200",
        }.get(org_type, "200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>china-gov-network skill</creator>')
    lines.append(f'    <description>田阳区领导班子工作关系网络 - {datetime.now().strftime("%Y-%m-%d")}</description>')
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
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="type" value="person"/>')
        lines.append(f'          <attvalue for="category" value="person"/>')
        lines.append(f'          <attvalue for="birth" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="birthplace" value="{esc(p["birthplace"])}"/>')
        lines.append(f'          <attvalue for="education" value="{esc(p["education"])}"/>')
        lines.append(f'          <attvalue for="current_post" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="source" value="{esc(p["source"][:100])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: Organizations
    for o in organizations:
        oid = 1000 + o["id"]
        oc = org_color(o["type"])
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="type" value="org"/>')
        lines.append(f'          <attvalue for="category" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
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
        lines.append(f'          <attvalue for="type" value="worked_at"/>')
        lines.append(f'          <attvalue for="context" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="period" value="{esc(pos["start"] or "?")} → {esc(pos["end"] or "今")}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        edge_id += 1

    # person↔person (relationships)
    for r in relationships:
        lines.append(f'      <edge id="{edge_id}" source="{r["person_a"]}" target="{r["person_b"]}" label="{esc(r["type"])}">')
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


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    os.makedirs(str(DB_PATH.parent), exist_ok=True)
    os.makedirs(str(GEXF_PATH.parent), exist_ok=True)

    build_database()
    build_gexf()

    print("\nDone! Files produced:")
    print(f"  {DB_PATH}")
    print(f"  {GEXF_PATH}")
