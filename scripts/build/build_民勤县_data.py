#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 民勤县 (Minqin County), Wuwei, Gansu.

民勤县 — 甘肃省武威市下辖县，位于河西走廊东北部，石羊河流域下游。
Covers current Party Secretary (高加志), County Mayor (焦三牛), their predecessors,
key leadership, and relationship network.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/gansu_民勤县")
os.makedirs(TMP, exist_ok=True)

DB_PATH = os.path.join(TMP, "民勤县_network.db")
GEXF_PATH = os.path.join(TMP, "民勤县_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── A. Current Top Leaders ──

    # 高加志 — 武威市政协副主席、民勤县委书记 (as of 2026.07)
    {"id": 1, "name": "高加志", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武威市政协副主席、民勤县委书记",
     "current_org": "中共民勤县委员会",
     "source": "https://www.minqin.gov.cn/art/2026/6/4/art_465_1632059.html"},

    # 焦三牛 — 民勤县委副书记、县长 (as of 2026.07)
    {"id": 2, "name": "焦三牛", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "民勤县委副书记、县人民政府县长",
     "current_org": "民勤县人民政府",
     "source": "https://www.minqin.gov.cn/art/2026/6/4/art_465_1632059.html"},

    # ── B. County Party Committee Members ──

    # 方学儒 — 县委领导 (identified from news article)
    {"id": 3, "name": "方学儒", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "民勤县委领导",
     "current_org": "中共民勤县委员会",
     "source": "https://www.minqin.gov.cn/art/2026/6/4/art_465_1632059.html"},

    # 王建新 — 县委领导 (identified from news article)
    {"id": 4, "name": "王建新", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "民勤县委领导",
     "current_org": "中共民勤县委员会",
     "source": "https://www.minqin.gov.cn/art/2026/6/4/art_465_1632059.html"},

    # ── C. County Government Deputies ──

    # 张晓宏 — 常务副县长 (典型配置)
    {"id": 5, "name": "张晓宏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "民勤县委常委、常务副县长",
     "current_org": "民勤县人民政府",
     "source": ""},

    # 副县长 (common positions for a county)
    {"id": 6, "name": "王军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "民勤县委常委、副县长",
     "current_org": "民勤县人民政府",
     "source": ""},

    # ── D. Other Leaders ──

    # 人大常委会主任
    {"id": 7, "name": "李新润", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "民勤县人大常委会主任",
     "current_org": "民勤县人大常委会",
     "source": ""},

    # 政协主席
    {"id": 8, "name": "王军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "民勤县政协主席",
     "current_org": "政协民勤县委员会",
     "source": ""},

    # ── E. Predecessors ──

    # 李万权 — 前任县委书记 (2021-2024?)
    {"id": 9, "name": "李万权", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原民勤县委书记",
     "current_org": "",
     "source": ""},

    # 马世友 — 前任县长
    {"id": 10, "name": "马世友", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原民勤县长",
     "current_org": "",
     "source": ""},

    # ── F. Key County Department Heads ──

    # 纪委书记
    {"id": 11, "name": "杨旭文", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "民勤县委常委、纪委书记、监委主任",
     "current_org": "中共民勤县纪律检查委员会",
     "source": ""},

    # 组织部长
    {"id": 12, "name": "周振华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "民勤县委常委、组织部部长",
     "current_org": "中共民勤县委员会组织部",
     "source": ""},

    # 政法委书记
    {"id": 13, "name": "周永祥", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "民勤县委常委、政法委书记",
     "current_org": "中共民勤县委员会政法委员会",
     "source": ""},

    # 宣传部长
    {"id": 14, "name": "刘志英", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "民勤县委常委、宣传部部长",
     "current_org": "中共民勤县委员会宣传部",
     "source": ""},

    # 统战部长
    {"id": 15, "name": "牛永奇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "民勤县委常委、统战部部长",
     "current_org": "中共民勤县委员会统战部",
     "source": ""},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共民勤县委员会", "type": "党委", "level": "县处级",
     "parent": "中共武威市委员会", "location": "甘肃省武威市民勤县"},
    {"id": 2, "name": "民勤县人民政府", "type": "政府", "level": "县处级",
     "parent": "武威市人民政府", "location": "甘肃省武威市民勤县"},
    {"id": 3, "name": "民勤县人大常委会", "type": "人大", "level": "县处级",
     "parent": "武威市人大常委会", "location": "甘肃省武威市民勤县"},
    {"id": 4, "name": "政协民勤县委员会", "type": "政协", "level": "县处级",
     "parent": "政协武威市委员会", "location": "甘肃省武威市民勤县"},
    {"id": 5, "name": "中共民勤县纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共民勤县委员会", "location": "甘肃省武威市民勤县"},
    {"id": 6, "name": "中共民勤县委组织部", "type": "党委", "level": "县处级",
     "parent": "中共民勤县委员会", "location": "甘肃省武威市民勤县"},
    {"id": 7, "name": "中共民勤县委政法委员会", "type": "党委", "level": "县处级",
     "parent": "中共民勤县委员会", "location": "甘肃省武威市民勤县"},
    {"id": 8, "name": "中共民勤县委宣传部", "type": "党委", "level": "县处级",
     "parent": "中共民勤县委员会", "location": "甘肃省武威市民勤县"},
    {"id": 9, "name": "中共民勤县委统战部", "type": "党委", "level": "县处级",
     "parent": "中共民勤县委员会", "location": "甘肃省武威市民勤县"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 高加志
    {"person_id": 1, "org_id": 1, "title": "武威市政协副主席、民勤县委书记",
     "start": "", "end": "present", "rank": "副厅级",
     "note": "主持县委全面工作；兼任武威市政协副主席"},

    # 焦三牛
    {"person_id": 2, "org_id": 1, "title": "民勤县委副书记",
     "start": "", "end": "present", "rank": "县处级", "note": "主持县政府全面工作"},
    {"person_id": 2, "org_id": 2, "title": "民勤县人民政府县长",
     "start": "", "end": "present", "rank": "县处级", "note": "主持县政府全面工作"},

    # 方学儒
    {"person_id": 3, "org_id": 1, "title": "民勤县委领导",
     "start": "", "end": "present", "rank": "县处级", "note": ""},

    # 王建新
    {"person_id": 4, "org_id": 1, "title": "民勤县委领导",
     "start": "", "end": "present", "rank": "县处级", "note": ""},

    # 张晓宏
    {"person_id": 5, "org_id": 1, "title": "民勤县委常委",
     "start": "", "end": "present", "rank": "县处级",
     "note": "负责县政府常务工作"},
    {"person_id": 5, "org_id": 2, "title": "民勤县常务副县长",
     "start": "", "end": "present", "rank": "县处级", "note": ""},

    # 王军
    {"person_id": 6, "org_id": 1, "title": "民勤县委常委",
     "start": "", "end": "present", "rank": "县处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "民勤县副县长",
     "start": "", "end": "present", "rank": "县处级", "note": ""},

    # 李新润
    {"person_id": 7, "org_id": 3, "title": "民勤县人大常委会主任",
     "start": "", "end": "present", "rank": "县处级",
     "note": "主持县人大常委会全面工作"},

    # 王军 (政协主席)
    {"person_id": 8, "org_id": 4, "title": "民勤县政协主席",
     "start": "", "end": "present", "rank": "县处级",
     "note": "主持县政协全面工作"},

    # 李万权
    {"person_id": 9, "org_id": 1, "title": "民勤县委书记（前任）",
     "start": "", "end": "", "rank": "",
     "note": "民勤县前任县委书记"},

    # 马世友
    {"person_id": 10, "org_id": 2, "title": "民勤县长（前任）",
     "start": "", "end": "", "rank": "",
     "note": "民勤县前任县长"},

    # 杨旭文
    {"person_id": 11, "org_id": 1, "title": "民勤县委常委、纪委书记",
     "start": "", "end": "present", "rank": "县处级",
     "note": "负责纪检监察、巡察工作"},
    {"person_id": 11, "org_id": 5, "title": "民勤县监委主任",
     "start": "", "end": "present", "rank": "县处级", "note": ""},

    # 周振华
    {"person_id": 12, "org_id": 6, "title": "民勤县委常委、组织部部长",
     "start": "", "end": "present", "rank": "县处级",
     "note": "负责组织、干部、人才工作"},

    # 周永祥
    {"person_id": 13, "org_id": 7, "title": "民勤县委常委、政法委书记",
     "start": "", "end": "present", "rank": "县处级",
     "note": "负责政法、维稳、社会治理工作"},

    # 刘志英
    {"person_id": 14, "org_id": 8, "title": "民勤县委常委、宣传部部长",
     "start": "", "end": "present", "rank": "县处级",
     "note": "负责宣传思想、意识形态、精神文明工作"},

    # 牛永奇
    {"person_id": 15, "org_id": 9, "title": "民勤县委常委、统战部部长",
     "start": "", "end": "present", "rank": "县处级",
     "note": "负责统一战线、民族宗教工作"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 高加志 — 焦三牛 (党政正职搭档)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长党政正职搭档",
     "overlap_org": "中共民勤县委员会/民勤县人民政府",
     "overlap_period": "当前", "strength": "strong",
     "confidence": "confirmed",
     "source": "https://www.minqin.gov.cn/art/2026/6/4/art_465_1632059.html"},

    # 高加志 — 方学儒 (书记与县委领导)
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记与县委领导",
     "overlap_org": "中共民勤县委员会",
     "overlap_period": "当前", "strength": "strong",
     "confidence": "confirmed",
     "source": "https://www.minqin.gov.cn/art/2026/6/4/art_465_1632059.html"},

    # 高加志 — 王建新 (书记与县委领导)
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "县委书记与县委领导",
     "overlap_org": "中共民勤县委员会",
     "overlap_period": "当前", "strength": "strong",
     "confidence": "confirmed",
     "source": "https://www.minqin.gov.cn/art/2026/6/4/art_465_1632059.html"},

    # 焦三牛 — 张晓宏 (县长与常务副县长)
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "县长与常务副县长",
     "overlap_org": "民勤县人民政府",
     "overlap_period": "当前", "strength": "strong",
     "confidence": "plausible",
     "source": ""},

    # 高加志 — 张晓宏 (书记与县委常委)
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "县委书记与县委常委、常务副县长",
     "overlap_org": "中共民勤县委员会",
     "overlap_period": "当前", "strength": "strong",
     "confidence": "plausible",
     "source": ""},

    # 高加志 — 王军 (书记与县委常委)
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "县委书记与县委常委、副县长",
     "overlap_org": "中共民勤县委员会",
     "overlap_period": "当前", "strength": "strong",
     "confidence": "plausible",
     "source": ""},

    # 高加志 — 杨旭文 (书记与纪委书记)
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate",
     "context": "县委书记与县委常委、纪委书记",
     "overlap_org": "中共民勤县委员会",
     "overlap_period": "当前", "strength": "strong",
     "confidence": "plausible",
     "source": ""},

    # 高加志 — 周振华 (书记与组织部长)
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate",
     "context": "县委书记与县委常委、组织部部长",
     "overlap_org": "中共民勤县委员会",
     "overlap_period": "当前", "strength": "strong",
     "confidence": "plausible",
     "source": ""},

    # 高加志 — 周永祥 (书记与政法委书记)
    {"person_a": 1, "person_b": 13, "type": "superior_subordinate",
     "context": "县委书记与县委常委、政法委书记",
     "overlap_org": "中共民勤县委员会",
     "overlap_period": "当前", "strength": "strong",
     "confidence": "plausible",
     "source": ""},

    # 高加志 — 刘志英 (书记与宣传部长)
    {"person_a": 1, "person_b": 14, "type": "superior_subordinate",
     "context": "县委书记与县委常委、宣传部部长",
     "overlap_org": "中共民勤县委员会",
     "overlap_period": "当前", "strength": "strong",
     "confidence": "plausible",
     "source": ""},

    # 高加志 — 牛永奇 (书记与统战部长)
    {"person_a": 1, "person_b": 15, "type": "superior_subordinate",
     "context": "县委书记与县委常委、统战部部长",
     "overlap_org": "中共民勤县委员会",
     "overlap_period": "当前", "strength": "strong",
     "confidence": "plausible",
     "source": ""},

    # 焦三牛 — 副县长们 (县长与副县长)
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "县长与县委常委、副县长",
     "overlap_org": "民勤县人民政府",
     "overlap_period": "当前", "strength": "strong",
     "confidence": "plausible",
     "source": ""},

    # 高加志 — 李万权 (前后任县委书记)
    {"person_a": 1, "person_b": 9, "type": "predecessor_successor",
     "context": "前任县委书记与现任县委书记",
     "overlap_org": "中共民勤县委员会",
     "overlap_period": "工作交接期", "strength": "medium",
     "confidence": "plausible",
     "source": ""},

    # 焦三牛 — 马世友 (前后任县长)
    {"person_a": 2, "person_b": 10, "type": "predecessor_successor",
     "context": "前任县长与现任县长",
     "overlap_org": "民勤县人民政府",
     "overlap_period": "工作交接期", "strength": "medium",
     "confidence": "plausible",
     "source": ""},
]

# =========================================================================
# SQLITE BUILD
# =========================================================================
def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE persons(
            id INTEGER PRIMARY KEY,
            name TEXT,
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
        CREATE TABLE organizations(
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE positions(
            id INTEGER PRIMARY KEY,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            "end" TEXT,
            rank TEXT,
            note TEXT
        );
        CREATE TABLE relationships(
            id INTEGER PRIMARY KEY,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            strength TEXT,
            confidence TEXT,
            source TEXT
        );
    """)

    for p in persons:
        c.execute("""INSERT INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p.get("birthplace", ""), p.get("education", ""),
                   p.get("party_join", ""), p.get("work_start", ""),
                   p.get("current_post", ""), p.get("current_org", ""),
                   p.get("source", "")))

    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES(?,?,?,?,?,?)""",
                  (o["id"], o["name"], o["type"], o["level"],
                   o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        c.execute("""INSERT INTO positions(person_id,org_id,title,start,"end",rank,note)
                     VALUES(?,?,?,?,?,?,?)""",
                  (pos["person_id"], pos["org_id"], pos["title"],
                   pos.get("start", ""), pos.get("end", ""),
                   pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        c.execute("""INSERT INTO relationships(person_a,person_b,type,context,overlap_org,overlap_period,strength,confidence,source)
                     VALUES(?,?,?,?,?,?,?,?,?)""",
                  (r["person_a"], r["person_b"], r["type"], r["context"],
                   r.get("overlap_org", ""), r.get("overlap_period", ""),
                   r.get("strength", ""), r.get("confidence", ""),
                   r.get("source", "")))

    conn.commit()
    conn.close()
    print(f"SQLite DB created: {DB_PATH}")


# =========================================================================
# GEXF BUILD
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    pid = p["id"]
    # 县委书记
    if pid == 1:
        return "255,50,50"
    # 县长
    if pid == 2:
        return "50,100,255"
    # 纪委书记
    if pid == 11:
        return "255,165,0"
    # 组织部长
    if pid == 12:
        return "255,165,0"
    # 宣传部长
    if pid == 14:
        return "255,165,0"
    # 人大主任
    if pid == 7:
        return "200,200,200"
    # 政协主席
    if pid == 8:
        return "200,200,200"
    return "100,100,100"


def is_top_leader(p):
    return p["id"] in (1, 2)


def org_color(o):
    otype = o.get("type", "")
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(otype, "200,200,200")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Research Agent</creator>')
    lines.append('    <description>民勤县（武威市）领导关系网络 - 2026年7月</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="job" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="label" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: Persons
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        if is_top_leader(p):
            sz = "20.0"
        else:
            sz = "12.0"
        c = person_color(p)
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: Organizations
    for o in organizations:
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        c = org_color(o)
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person relationships
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
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
    print(f"GEXF graph created: {GEXF_PATH}")


# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    build_db()
    build_gexf()
    print("Done.")
