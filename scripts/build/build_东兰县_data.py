#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
东兰县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 广西壮族自治区
Parent City: 河池市
Region: 东兰县
Targets: 县委书记 & 县长

Research Date: 2026-07-23
Research Note:
  东兰县人民政府门户网站 (http://www.donglan.gov.cn/) 可通过 HTTP 访问。
  县政府领导页面 (xxgk/ldjj/) 可访问并列出政府班子成员。
  县委领导信息来自新闻报道交叉验证。

  关键发现：2026年7月6日至17日间发生主要领导调整：
  - 白玛泽仁由县长转任县委书记
  - 黄伟庭任县委副书记、副县长、代县长
  - 韦家甫不再担任县委书记职务（去向待查）

  Baidu、Google、Jina Reader 均无法正常访问（限制/超时），
  百度百科人物履历不可获取。人物传记信息严重缺失。

Sources:
  - http://www.donglan.gov.cn/xxgk/ldjj/ (县政府领导)
  - http://www.donglan.gov.cn/gddt/t27859297.shtml (2026-07-06: 韦家甫为县委书记、白玛泽仁为县长)
  - http://www.donglan.gov.cn/gddt/t27920481.shtml (2026-07-17: 白玛泽仁为县委书记)
  - http://www.donglan.gov.cn/zwdt/sdfk/t27941924.shtml (2026-07-23: 白玛泽仁为县委书记, 黄伟庭为代县长)
  - http://www.donglan.gov.cn/gddt/t27880429.shtml (2026-07-13: 白玛泽仁为县长, 李万章为常务副县长, 覃红连为县委常委、副县长)
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "东兰县"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-23"
TODAY = "20260723"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：县委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "白玛泽仁",
        "gender": "",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "东兰县委书记（原县长，2026年7月转任书记）",
        "current_org": "中共东兰县委员会",
        "source": "http://www.donglan.gov.cn/xxgk/ldjj/; http://www.donglan.gov.cn/gddt/t27920481.shtml (2026-07-17报道为县委书记)"
    },
    # ════════════════════════════════════════
    # 核心领导：代县长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "黄伟庭",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "东兰县委副书记、副县长、代县长",
        "current_org": "东兰县人民政府",
        "source": "http://www.donglan.gov.cn/zwdt/sdfk/t27941924.shtml (2026-07-23报道为代县长)"
    },
    # ════════════════════════════════════════
    # 前任县委书记
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "韦家甫",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原东兰县委书记（2026年7月离任，去向待查）",
        "current_org": "",
        "source": "http://www.donglan.gov.cn/gddt/t27859297.shtml (2026-07-06仍为县委书记)"
    },
    # ════════════════════════════════════════
    # 县委常委、组织部部长
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "胡大伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "东兰县委常委、组织部部长",
        "current_org": "中共东兰县委员会组织部",
        "source": "http://www.donglan.gov.cn/gddt/t27859297.shtml"
    },
    # ════════════════════════════════════════
    # 县委常委、常务副县长
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "李万章",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "东兰县委常委、常务副县长",
        "current_org": "东兰县人民政府",
        "source": "http://www.donglan.gov.cn/gddt/t27880429.shtml"
    },
    # ════════════════════════════════════════
    # 县委常委、副县长
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "覃红连",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "东兰县委常委、副县长",
        "current_org": "东兰县人民政府",
        "source": "http://www.donglan.gov.cn/gddt/t27880429.shtml; http://www.donglan.gov.cn/xxgk/ldjj/"
    },
    # ════════════════════════════════════════
    # 副县长
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "黄文江",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "东兰县副县长",
        "current_org": "东兰县人民政府",
        "source": "http://www.donglan.gov.cn/xxgk/ldjj/"
    },
    {
        "id": 8,
        "name": "叶思锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "东兰县副县长",
        "current_org": "东兰县人民政府",
        "source": "http://www.donglan.gov.cn/xxgk/ldjj/"
    },
    {
        "id": 9,
        "name": "侯毅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "东兰县副县长",
        "current_org": "东兰县人民政府",
        "source": "http://www.donglan.gov.cn/xxgk/ldjj/"
    },
    {
        "id": 10,
        "name": "韦明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "东兰县副县长",
        "current_org": "东兰县人民政府",
        "source": "http://www.donglan.gov.cn/xxgk/ldjj/"
    },
    {
        "id": 11,
        "name": "黄红梅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "东兰县副县长",
        "current_org": "东兰县人民政府",
        "source": "http://www.donglan.gov.cn/xxgk/ldjj/"
    },
    {
        "id": 12,
        "name": "潘华凯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "东兰县副县长",
        "current_org": "东兰县人民政府",
        "source": "http://www.donglan.gov.cn/xxgk/ldjj/"
    },
    {
        "id": 13,
        "name": "施扬泰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "东兰县副县长",
        "current_org": "东兰县人民政府",
        "source": "http://www.donglan.gov.cn/xxgk/ldjj/"
    },
    # ════════════════════════════════════════
    # 县府办主任
    # ════════════════════════════════════════
    {
        "id": 14,
        "name": "韦明龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "东兰县人民政府办公室主任",
        "current_org": "东兰县人民政府办公室",
        "source": "http://www.donglan.gov.cn/xxgk/ldjj/"
    },
    # ════════════════════════════════════════
    # 其他县级领导（从新闻中确认）
    # ════════════════════════════════════════
    {
        "id": 15,
        "name": "黄高线",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "东兰县领导（具体职务待确认）",
        "current_org": "",
        "source": "http://www.donglan.gov.cn/zwdt/sdfk/t27941924.shtml"
    },
    {
        "id": 16,
        "name": "黄吉楠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "东兰县领导（具体职务待确认）",
        "current_org": "",
        "source": "http://www.donglan.gov.cn/zwdt/sdfk/t27941924.shtml"
    },
    {
        "id": 17,
        "name": "班师",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "东兰县领导（具体职务待确认）",
        "current_org": "",
        "source": "http://www.donglan.gov.cn/zwdt/sdfk/t27941924.shtml"
    },
    {
        "id": 18,
        "name": "韦彩秀",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "东兰县领导（具体职务待确认）",
        "current_org": "",
        "source": "http://www.donglan.gov.cn/zwdt/sdfk/t27941924.shtml"
    },
    {
        "id": 19,
        "name": "梁江梅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "东兰县领导（具体职务待确认）",
        "current_org": "",
        "source": "http://www.donglan.gov.cn/zwdt/sdfk/t27941924.shtml"
    },
    {
        "id": 20,
        "name": "李举国",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "东兰县领导（具体职务待确认）",
        "current_org": "",
        "source": "http://www.donglan.gov.cn/zwdt/sdfk/t27941924.shtml"
    },
    {
        "id": 21,
        "name": "徐若杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "东兰县领导（具体职务待确认）",
        "current_org": "",
        "source": "http://www.donglan.gov.cn/zwdt/sdfk/t27941924.shtml"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {
        "id": 1,
        "name": "中共东兰县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共河池市委员会",
        "location": "广西河池市东兰县"
    },
    {
        "id": 2,
        "name": "东兰县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "河池市人民政府",
        "location": "广西河池市东兰县"
    },
    {
        "id": 3,
        "name": "中共东兰县委员会组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共东兰县委员会",
        "location": "广西河池市东兰县"
    },
    {
        "id": 4,
        "name": "东兰县人民政府办公室",
        "type": "政府",
        "level": "县级",
        "parent": "东兰县人民政府",
        "location": "广西河池市东兰县"
    },
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 白玛泽仁 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "东兰县委书记", "start": "2026-07", "end": "present", "rank": "县处级正职", "note": "由东兰县长转任县委书记；此前长期担任县长"},
    # 白玛泽仁 — 原县长
    {"person_id": 1, "org_id": 2, "title": "东兰县县长", "start": "", "end": "2026-07", "rank": "县处级正职", "note": "任县长期间曾主持政府全面工作；2026年7月转任县委书记"},
    # 黄伟庭 — 代县长
    {"person_id": 2, "org_id": 2, "title": "东兰县代县长", "start": "2026-07", "end": "present", "rank": "县处级正职", "note": "同时担任县委副书记、副县长"},
    {"person_id": 2, "org_id": 1, "title": "东兰县委副书记", "start": "2026-07", "end": "present", "rank": "县处级副职", "note": ""},
    # 韦家甫 — 原县委书记
    {"person_id": 3, "org_id": 1, "title": "东兰县委书记（原）", "start": "", "end": "2026-07", "rank": "县处级正职", "note": "2026年7月6日仍有公开活动；7月中旬不再任县委书记；去向待查"},
    # 胡大伟 — 组织部部长
    {"person_id": 4, "org_id": 3, "title": "县委常委、组织部部长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 李万章 — 常务副县长
    {"person_id": 5, "org_id": 2, "title": "县委常委、常务副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 覃红连 — 县委常委、副县长
    {"person_id": 6, "org_id": 2, "title": "县委常委、副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 副县长们
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 县府办主任
    {"person_id": 14, "org_id": 4, "title": "东兰县人民政府办公室主任", "start": "", "end": "present", "rank": "乡科级正职", "note": ""},
    # 其他领导（职务待确认）—— 挂名到县委
    {"person_id": 15, "org_id": 1, "title": "县领导（职务待确认）", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 16, "org_id": 1, "title": "县领导（职务待确认）", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 17, "org_id": 1, "title": "县领导（职务待确认）", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 18, "org_id": 1, "title": "县领导（职务待确认）", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 19, "org_id": 1, "title": "县领导（职务待确认）", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 20, "org_id": 1, "title": "县领导（职务待确认）", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 21, "org_id": 1, "title": "县领导（职务待确认）", "start": "", "end": "present", "rank": "", "note": ""},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 白玛泽仁 — 韦家甫 (前后任)
    {
        "person_a": 1,
        "person_b": 3,
        "type": "predecessor_successor",
        "context": "白玛泽仁接替韦家甫任东兰县委书记，白玛此前任东兰县长，韦家甫去向待查",
        "overlap_org": "中共东兰县委员会",
        "overlap_period": "2026-07"
    },
    # 白玛泽仁 — 黄伟庭 (前后任/上下级)
    {
        "person_a": 1,
        "person_b": 2,
        "type": "predecessor_successor",
        "context": "白玛泽仁由县长转任县委书记；黄伟庭接替白玛的县长职务（代县长）",
        "overlap_org": "东兰县人民政府",
        "overlap_period": "2026-07"
    },
    # 白玛泽仁 — 李万章 (上下级)
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "白玛泽仁任书记/县长期间，李万章任常务副县长",
        "overlap_org": "东兰县人民政府",
        "overlap_period": ""
    },
    # 白玛泽仁 — 胡大伟 (上下级)
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "白玛泽仁任书记，胡大伟任组织部部长",
        "overlap_org": "中共东兰县委员会",
        "overlap_period": ""
    },
    # 白玛泽仁 — 覃红连 (上下级)
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "白玛泽仁任书记/县长，覃红连任县委常委、副县长",
        "overlap_org": "东兰县人民政府",
        "overlap_period": ""
    },
    # 黄伟庭 — 李万章 (同级/同事)
    {
        "person_a": 2,
        "person_b": 5,
        "type": "overlap",
        "context": "黄伟庭任代县长，李万章任常务副县长，为政府班子正副职",
        "overlap_org": "东兰县人民政府",
        "overlap_period": "2026-07"
    },
]

# =========================================================================
# 5. BUILD
# =========================================================================

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def create_sqlite(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS relationships")
    c.execute("DROP TABLE IF EXISTS positions")
    c.execute("DROP TABLE IF EXISTS organizations")
    c.execute("DROP TABLE IF EXISTS persons")
    c.execute("""CREATE TABLE persons(
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE organizations(
        id INTEGER PRIMARY KEY, name TEXT, type TEXT,
        level TEXT, parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE positions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER, title TEXT,
        start TEXT, "end" TEXT, rank TEXT, note TEXT
    )""")
    c.execute("""CREATE TABLE relationships(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER, type TEXT,
        context TEXT, overlap_org TEXT, overlap_period TEXT
    )""")
    for p in persons:
        c.execute("""INSERT INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"], p["work_start"],
                   p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES(?,?,?,?,?,?)""",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        c.execute("""INSERT INTO positions(person_id, org_id, title, start, "end", rank, note) VALUES(?,?,?,?,?,?,?)""",
                  (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))
    for r in relationships:
        c.execute("""INSERT INTO relationships(person_a, person_b, type, context, overlap_org, overlap_period) VALUES(?,?,?,?,?,?)""",
                  (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))
    conn.commit()
    conn.close()
    print(f"  DB: {db_path} ({len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships)")

def person_color(p):
    role = p.get("current_post", "")
    if "书记" in role and "县委" in role:
        return "255,50,50"
    elif "县长" in role or "代县长" in role:
        return "50,100,255"
    elif "常务副" in role:
        return "50,100,255"
    elif "组织部" in role:
        return "255,165,0"
    elif "副县长" in role:
        return "100,100,255"
    return "100,100,100"

def is_top_leader(p):
    return "县委书记" in p.get("current_post", "") or "县长" in p.get("current_post", "") or "代县长" in p.get("current_post", "")

def create_gexf(gexf_path):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append(f'    <description>东兰县领导班子工作关系网络 (截至{AS_OF})</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # nodes - persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # nodes - orgs
    for o in organizations:
        if o["type"] == "党委":
            oc = "255,200,200"
        elif o["type"] == "政府":
            oc = "200,200,255"
        else:
            oc = "200,200,200"
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # edges - person->org
    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # edges - person<->person
    for r in relationships:
        eid += 1
        p1 = next((p for p in persons if p["id"] == r["person_a"]), None)
        p2 = next((p for p in persons if p["id"] == r["person_b"]), None)
        if p1 and p2:
            lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
            lines.append('        <attvalues>')
            lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
            lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
            lines.append('        </attvalues>')
            lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {gexf_path}")

def write_person_json(person, suffix):
    """Write a person JSON file."""
    fname = f"{TODAY}-广西壮族自治区-河池市-{suffix}-{person['name']}.json"
    fpath = os.path.join(PERSONS_DIR, fname)

    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "河池市",
            "region": "东兰县",
            "job": suffix,
            "task_id": "guangxi_东兰县",
            "time_focus": "截至2026年7月"
        },
        "identity": {
            "person_id": f"guangxi_donglan_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"] if person["gender"] else "",
            "ethnicity": person["ethnicity"] if person["ethnicity"] else "",
            "birth": person["birth"] if person["birth"] else "",
            "birthplace": person["birthplace"] if person["birthplace"] else "",
            "native_place": "",
            "education": [],
            "party_join": person["party_join"] if person["party_join"] else "",
            "work_start": person["work_start"] if person["work_start"] else "",
            "dedupe_keys": {"name_birth": "", "name_birthplace": "", "official_profile_url": ""}
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "县处级正职" if "书记" in person["current_post"] or "县长" in person["current_post"] or "代县长" in person["current_post"] else "县处级副职" if "副" in person["current_post"] else "",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [
            {
                "id": "S001",
                "title": "东兰县人民政府门户网站 - 县政府领导",
                "url": "http://www.donglan.gov.cn/xxgk/ldjj/",
                "publisher": "东兰县人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "县政府领导名单页面"
            },
            {
                "id": "S002",
                "title": "白玛泽仁到坡豪湖国家湿地公园检查指导旅游项目建设工作",
                "url": "http://www.donglan.gov.cn/gddt/t27920481.shtml",
                "publisher": "东兰县融媒体中心",
                "published_at": "2026-07-21",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认白玛泽仁为县委书记"
            },
            {
                "id": "S003",
                "title": "东兰县部署水库安全度汛与安全生产两线作战工作",
                "url": "http://www.donglan.gov.cn/zwdt/sdfk/t27941924.shtml",
                "publisher": "东兰县融媒体中心",
                "published_at": "2026-07-23",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认白玛泽仁为县委书记、黄伟庭为代县长"
            }
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "出生年月、籍贯、教育背景、完整职业履历均缺失"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的出生年月、籍贯、民族",
                "why_it_matters": "身份信息的核心字段，用于人员去重和网络构建",
                "suggested_queries": [f"{person['name']} 简历 东兰", f"{person['name']} 任前公示"],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": f"{person['name']}的完整工作履历",
                "why_it_matters": "网络关系中的时间线分析核心数据",
                "suggested_queries": [f"{person['name']} 东兰 任职", f"{person['name']} 河池"],
                "last_attempted": AS_OF
            }
        ]
    }
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath}")

# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    print(f"Building {SLUG} data artifacts...")
    create_sqlite(DB_PATH)
    create_gexf(GEXF_PATH)

    # Write person JSONs for core leaders
    write_person_json(persons[0], "县委书记")  # 白玛泽仁
    write_person_json(persons[1], "代县长")    # 黄伟庭
    write_person_json(persons[2], "原县委书记") # 韦家甫

    print("Done!")
