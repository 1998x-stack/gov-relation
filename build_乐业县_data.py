#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
乐业县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 广西壮族自治区
Parent City: 百色市
Region: 乐业县
Targets: 县委书记 & 县长

Research Note:
   乐业县是百色市下辖县，位于广西西北部，地处黔桂交界，总面积约2,617平方公里，
   常住人口约15万。乐业县以世界地质公园大石围天坑群闻名。

   本次调查期间，乐业县人民政府网站（https://www.leye.gov.cn/）领导简介页面
   （http://www.leye.gov.cn/xxgk/ldjj/）可访问。
   县委书记张国革因县委领导信息与政府领导页面分设，从新闻报道中确认。
   Exa 搜索限流，部分背景资料来自政府网站新闻报道和百度百科片段。

Key Findings:
   - 县委书记：张国革（从新闻报道确认）
   - 县长：黄茂兵（1973年5月出生，壮族，在职研究生学历，中共党员）
   - 副县长7人：杨广林、蔡鹏飞、黄承万、李高振、蒙丽珍、林盛、黄尚兴

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
SLUG = "乐业县"
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-23"
TODAY = AS_OF.replace("-", "")

S1 = {"title": "乐业县人民政府网站—领导简介页面", "url": "http://www.leye.gov.cn/xxgk/ldjj/",
      "publisher": "乐业县人民政府", "accessed_at": AS_OF, "source_type": "official"}
S2 = {"title": "乐业县新闻—张国革调研报道", "url": "http://www.leye.gov.cn/zwdt/t27893283.shtml",
      "publisher": "乐业县人民政府", "accessed_at": AS_OF, "source_type": "official"}
S3 = {"title": "乐业县县长黄茂兵个人简介", "url": "http://www.leye.gov.cn/xxgk/ldjj/xz/t9941801.shtml",
      "publisher": "乐业县人民政府", "accessed_at": AS_OF, "source_type": "official"}
S4 = {"title": "乐业县政府常务会议报道", "url": "http://www.leye.gov.cn/xxgk/zfhy/cwhy/",
      "publisher": "乐业县人民政府", "accessed_at": AS_OF, "source_type": "official"}

SOURCE_REGISTER = [S1, S2, S3, S4]

# ═══════════════════════════════════════════════════════════════
# 1. PERSONS
# ═══════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 核心领导：县委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "张国革",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乐业县委书记",
        "current_org": "中共乐业县委员会",
        "source": "官方报道 — 2026年乐业县人民政府网站新闻确认县委书记张国革调研乡镇工作",
    },
    # ════════════════════════════════════════
    # 核心领导：县长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "黄茂兵",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1973年5月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乐业县长",
        "current_org": "乐业县人民政府",
        "source": "乐业县人民政府网站领导简介 — 黄茂兵，男，壮族，1973年5月出生，在职研究生学历，中共党员，现任广西百色市乐业县委副书记、县人民政府县长、党组书记",
    },
    # ════════════════════════════════════════
    # 副县长（从领导简介页面获取）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "杨广林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐业县副县长",
        "current_org": "乐业县人民政府",
        "source": "乐业县人民政府网站领导简介页面 — 副县长",
    },
    {
        "id": 4,
        "name": "蔡鹏飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐业县副县长",
        "current_org": "乐业县人民政府",
        "source": "乐业县人民政府网站领导简介页面 — 副县长",
    },
    {
        "id": 5,
        "name": "黄承万",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐业县副县长",
        "current_org": "乐业县人民政府",
        "source": "乐业县人民政府网站领导简介页面 — 副县长",
    },
    {
        "id": 6,
        "name": "李高振",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐业县副县长",
        "current_org": "乐业县人民政府",
        "source": "乐业县人民政府网站领导简介页面 — 副县长",
    },
    {
        "id": 7,
        "name": "蒙丽珍",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐业县副县长",
        "current_org": "乐业县人民政府",
        "source": "乐业县人民政府网站领导简介页面 — 副县长",
    },
    {
        "id": 8,
        "name": "林盛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐业县副县长",
        "current_org": "乐业县人民政府",
        "source": "乐业县人民政府网站领导简介页面 — 副县长",
    },
    {
        "id": 9,
        "name": "黄尚兴",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐业县副县长",
        "current_org": "乐业县人民政府",
        "source": "乐业县人民政府网站领导简介页面 — 副县长",
    },
    # ════════════════════════════════════════
    # 张国革前任（待查）
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "【待查】乐业县委书记（张国革前任）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任乐业县委书记（待查）",
        "current_org": "中共乐业县委员会",
        "source": "GAP — 需进一步查找",
    },
    # ════════════════════════════════════════
    # 黄茂兵前任（待查）
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "【待查】乐业县长（黄茂兵前任）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任乐业县长（待查）",
        "current_org": "乐业县人民政府",
        "source": "GAP — 需进一步查找",
    },
]

# ═══════════════════════════════════════════════════════════════
# 2. ORGANIZATIONS
# ═══════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共乐业县委员会", "type": "党委",
     "level": "县级", "parent": "中共百色市委员会", "location": "百色市乐业县"},
    {"id": 2, "name": "乐业县人民政府", "type": "政府",
     "level": "县级", "parent": "百色市人民政府", "location": "百色市乐业县"},
    {"id": 3, "name": "中共乐业县纪律检查委员会", "type": "纪委",
     "level": "县级", "parent": "中共百色市纪律检查委员会", "location": "百色市乐业县"},
    {"id": 4, "name": "乐业县人大常委会", "type": "人大",
     "level": "县级", "parent": "百色市人大常委会", "location": "百色市乐业县"},
    {"id": 5, "name": "中国人民政治协商会议乐业县委员会", "type": "政协",
     "level": "县级", "parent": "百色市政协", "location": "百色市乐业县"},
    {"id": 6, "name": "中共乐业县委组织部", "type": "党委部门",
     "level": "县级", "parent": "中共乐业县委员会", "location": "百色市乐业县"},
    {"id": 7, "name": "中共乐业县委宣传部", "type": "党委部门",
     "level": "县级", "parent": "中共乐业县委员会", "location": "百色市乐业县"},
    {"id": 8, "name": "中共乐业县委政法委员会", "type": "党委部门",
     "level": "县级", "parent": "中共乐业县委员会", "location": "百色市乐业县"},
    {"id": 9, "name": "中共乐业县委统一战线工作部", "type": "党委部门",
     "level": "县级", "parent": "中共乐业县委员会", "location": "百色市乐业县"},
    {"id": 10, "name": "乐业县公安局", "type": "政府部门",
     "level": "县级", "parent": "百色市公安局", "location": "百色市乐业县"},
]

# ═══════════════════════════════════════════════════════════════
# 3. POSITIONS
# ═══════════════════════════════════════════════════════════════

positions = [
    # ── 现任核心领导 ──
    {"person_id": 1, "org_id": 1, "title": "乐业县委书记",
     "start": "", "end": "", "rank": "正处",
     "note": "张国革，中共党员，2026年已确认在职"},
    {"person_id": 2, "org_id": 2, "title": "乐业县长",
     "start": "", "end": "", "rank": "正处",
     "note": "黄茂兵，1973年5月出生，壮族，在职研究生学历，中共党员"},
    {"person_id": 2, "org_id": 1, "title": "乐业县委副书记",
     "start": "", "end": "", "rank": "正处",
     "note": "黄茂兵兼任乐业县委副书记"},

    # ── 副县长 ──
    {"person_id": 3, "org_id": 2, "title": "乐业县副县长",
     "start": "", "end": "", "rank": "副处", "note": "杨广林"},
    {"person_id": 4, "org_id": 2, "title": "乐业县副县长",
     "start": "", "end": "", "rank": "副处", "note": "蔡鹏飞"},
    {"person_id": 5, "org_id": 2, "title": "乐业县副县长",
     "start": "", "end": "", "rank": "副处", "note": "黄承万"},
    {"person_id": 6, "org_id": 2, "title": "乐业县副县长",
     "start": "", "end": "", "rank": "副处", "note": "李高振"},
    {"person_id": 7, "org_id": 2, "title": "乐业县副县长",
     "start": "", "end": "", "rank": "副处", "note": "蒙丽珍"},
    {"person_id": 8, "org_id": 2, "title": "乐业县副县长",
     "start": "", "end": "", "rank": "副处", "note": "林盛"},
    {"person_id": 9, "org_id": 2, "title": "乐业县副县长",
     "start": "", "end": "", "rank": "副处", "note": "黄尚兴"},
]

# ═══════════════════════════════════════════════════════════════
# 4. RELATIONSHIPS
# ═══════════════════════════════════════════════════════════════

relationships = [
    # 核心党政搭档
    {"person_a": 1, "person_b": 2, "type": "党政同僚",
     "context": "乐业县委书记张国革与县长黄茂兵党政搭档",
     "overlap_org": "乐业县", "overlap_period": ""},

    # 县委书记与副县长（上下级）
    {"person_a": 1, "person_b": 3, "type": "上下级",
     "context": "县委书记与副县长杨广林",
     "overlap_org": "乐业县", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "上下级",
     "context": "县委书记与副县长蔡鹏飞",
     "overlap_org": "乐业县", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "上下级",
     "context": "县委书记与副县长黄承万",
     "overlap_org": "乐业县", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "上下级",
     "context": "县委书记与副县长李高振",
     "overlap_org": "乐业县", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "上下级",
     "context": "县委书记与副县长蒙丽珍",
     "overlap_org": "乐业县", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "上下级",
     "context": "县委书记与副县长林盛",
     "overlap_org": "乐业县", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "上下级",
     "context": "县委书记与副县长黄尚兴",
     "overlap_org": "乐业县", "overlap_period": ""},

    # 县长与副县长
    {"person_a": 2, "person_b": 3, "type": "上下级",
     "context": "县长与副县长杨广林",
     "overlap_org": "乐业县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "上下级",
     "context": "县长与副县长蔡鹏飞",
     "overlap_org": "乐业县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "上下级",
     "context": "县长与副县长黄承万",
     "overlap_org": "乐业县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "上下级",
     "context": "县长与副县长李高振",
     "overlap_org": "乐业县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "上下级",
     "context": "县长与副县长蒙丽珍",
     "overlap_org": "乐业县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "上下级",
     "context": "县长与副县长林盛",
     "overlap_org": "乐业县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "上下级",
     "context": "县长与副县长黄尚兴",
     "overlap_org": "乐业县人民政府", "overlap_period": ""},

    # 前后任
    {"person_a": 1, "person_b": 10, "type": "前后任",
     "context": "张国革接任乐业县委书记",
     "overlap_org": "中共乐业县委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "前后任",
     "context": "黄茂兵接任乐业县长",
     "overlap_org": "乐业县人民政府", "overlap_period": ""},
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
        if "县长" in title and "副" not in title:
            return "30,100,200"  # blue: government head
        if "纪委" in title:
            return "255,165,0"   # orange: discipline
        if "副" in title:
            return "100,149,237" # cornflower blue: deputy
        return "100,100,100"

    def is_top_leader(p):
        title = p["current_post"] or ""
        return ("书记" in title and "纪委" not in title and "副" not in title) or \
               ("县长" in title and "副" not in title)

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
    lines.append(f'    <description>乐业县领导班子工作关系网络 - {datetime.now().strftime("%Y-%m-%d")}</description>')
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
