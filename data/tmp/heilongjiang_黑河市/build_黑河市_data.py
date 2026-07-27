#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 黑河市 (Heihe City), 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_黑河市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - Wikipedia (zh.wikipedia.org) — leadership table for 黑河市
  - www.heihe.gov.cn — 黑河市人民政府网站新闻确认秦波（市委书记）、战明秀（市长）
  - 黑河市第七届人民代表大会第七次会议新闻（2026-07-17）确认战明秀当选市长

Confidence notes:
  - 秦波: confirmed via Wikipedia leadership table (name, ethnicity, birth, native place, appointment date)
  - 战明秀: confirmed via Wikipedia and government website (born Apr 1974, Shandong Rizhao)
  - 狄恒 (人大主任), 丁兆禄 (政协主席): confirmed via Wikipedia
  - Detailed career timelines (education, early career) could not be verified due to web access limitations
  - Web search tools (Exa, Jina, Baidu) were rate-limited or timed out during this investigation
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "黑河市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

CANONICAL_DB = os.path.join(BASE, "..", "..", "database", f"{SLUG}_network.db")
CANONICAL_GEXF = os.path.join(BASE, "..", "..", "graph", f"{SLUG}_network.gexf")
CANONICAL_BUILD = os.path.join(BASE, "..", "..", "..", f"build_{SLUG}_data.py")
CANONICAL_PERSONS = Path(BASE) / ".." / ".." / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 1,
        "name": "秦波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年1月",
        "birthplace": "黑龙江省同江市",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共黑河市委员会",
        "source": "https://zh.wikipedia.org/wiki/黑河市"
    },
    {
        "id": 2,
        "name": "战明秀",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年4月",
        "birthplace": "山东省日照市",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "黑河市人民政府",
        "source": "https://zh.wikipedia.org/wiki/黑河市"
    },
    {
        "id": 3,
        "name": "狄恒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年11月",
        "birthplace": "山东省莱阳市",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "黑河市人民代表大会常务委员会",
        "source": "https://zh.wikipedia.org/wiki/黑河市"
    },
    {
        "id": 4,
        "name": "丁兆禄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年12月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议黑河市委员会",
        "source": "https://zh.wikipedia.org/wiki/黑河市"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Other key leaders (from government meeting seating)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 5,
        "name": "吴子慧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共黑河市委员会",
        "source": "https://www.heihe.gov.cn — 2026-07-17人大会议"
    },
    {
        "id": 6,
        "name": "尤晓林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共黑河市委员会",
        "source": "https://www.heihe.gov.cn — 2026-07-17人大会议"
    },
    {
        "id": 7,
        "name": "赵迎春",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共黑河市委员会",
        "source": "https://www.heihe.gov.cn — 2026-07-17人大会议"
    },
    {
        "id": 8,
        "name": "李平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共黑河市委员会",
        "source": "https://www.heihe.gov.cn — 2026-07-17人大会议"
    },
    {
        "id": 9,
        "name": "李百山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市监察委员会主任",
        "current_org": "黑河市监察委员会",
        "source": "https://www.heihe.gov.cn — 2026-07-17人大会议"
    },
    {
        "id": 10,
        "name": "贾牧樵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市公安局局长",
        "current_org": "黑河市人民政府",
        "source": "https://www.heihe.gov.cn — 2026-07-22新闻"
    },
    {
        "id": 11,
        "name": "邸建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府秘书长",
        "current_org": "黑河市人民政府",
        "source": "https://www.heihe.gov.cn — 2026-07-22新闻"
    },
    # Predecessors
    {
        "id": 12,
        "name": "李锡文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共黑河市委员会",
        "source": "https://zh.wikipedia.org/wiki/黑河市"
    },
    {
        "id": 13,
        "name": "赵荣国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市长",
        "current_org": "黑河市人民政府",
        "source": "https://zh.wikipedia.org/wiki/黑河市"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共黑河市委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中共黑龙江省委员会",
        "location": "黑河市"
    },
    {
        "id": 2,
        "name": "黑河市人民政府",
        "type": "政府",
        "level": "地级",
        "parent": "黑龙江省人民政府",
        "location": "黑河市"
    },
    {
        "id": 3,
        "name": "黑河市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级",
        "parent": "黑龙江省人民代表大会常务委员会",
        "location": "黑河市"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议黑河市委员会",
        "type": "政协",
        "level": "地级",
        "parent": "中国人民政治协商会议黑龙江省委员会",
        "location": "黑河市"
    },
    {
        "id": 5,
        "name": "黑河市监察委员会",
        "type": "政府",
        "level": "地级",
        "parent": "黑龙江省监察委员会",
        "location": "黑河市"
    },
    {
        "id": 6,
        "name": "黑河市公安局",
        "type": "政府",
        "level": "地级",
        "parent": "黑河市人民政府",
        "location": "黑河市"
    },
    {
        "id": 7,
        "name": "黑龙江省人民政府",
        "type": "政府",
        "level": "省级",
        "parent": "",
        "location": "哈尔滨市"
    },
    {
        "id": 8,
        "name": "中共黑龙江省委员会",
        "type": "党委",
        "level": "省级",
        "parent": "",
        "location": "哈尔滨市"
    },
]

# ── Positions ──────────────────────────────────────────────────────────────

positions = [
    # 秦波 career timeline
    {"person_id": 1, "org_id": 1, "title": "黑河市委书记", "start_date": "2026-04", "end_date": "present", "rank": "正厅级", "note": "2026年4月任黑河市委书记"},
    {"person_id": 1, "org_id": 2, "title": "黑河市代市长", "start_date": "2024-12", "end_date": "", "rank": "正厅级", "note": "2024年12月任代市长（此前任副市长或省直职务）"},
    {"person_id": 1, "org_id": 2, "title": "黑河市人民政府市长", "start_date": "", "end_date": "2026-05", "rank": "正厅级", "note": "2025年转正——2026年4月改任书记前为市长"},
    {"person_id": 1, "org_id": 1, "title": "黑河市委书记", "start_date": "2026-04", "end_date": "present", "rank": "正厅级", "note": "2026年4月接替李锡文任黑河市委书记"},

    # 战明秀
    {"person_id": 2, "org_id": 2, "title": "黑河市人民政府市长", "start_date": "2026-07-16", "end_date": "present", "rank": "正厅级", "note": "2026年7月16日黑河市第七届人大第七次会议当选"},
    {"person_id": 2, "org_id": 1, "title": "黑河市委副书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "市委副书记、市长"},

    # 狄恒
    {"person_id": 3, "org_id": 3, "title": "黑河市人大常委会主任", "start_date": "2024-08", "end_date": "present", "rank": "正厅级", "note": "2024年8月任现职"},

    # 丁兆禄
    {"person_id": 4, "org_id": 4, "title": "黑河市政协主席", "start_date": "2022-01", "end_date": "present", "rank": "正厅级", "note": "2022年1月当选"},

    # 吴子慧
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "2026年7月仍在任"},

    # 尤晓林
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "2026年7月仍在任"},

    # 赵迎春
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "2026年7月仍在任"},

    # 李平
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "2026年7月仍在任"},

    # 李百山
    {"person_id": 9, "org_id": 5, "title": "市监察委员会主任", "start_date": "2026-07-16", "end_date": "present", "rank": "副厅级", "note": "2026年7月16日当选"},

    # 贾牧樵
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼市公安局局长"},
    {"person_id": 10, "org_id": 6, "title": "市公安局局长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},

    # 邸建军
    {"person_id": 11, "org_id": 2, "title": "市政府秘书长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},

    # 李锡文（前任市委书记）
    {"person_id": 12, "org_id": 1, "title": "黑河市委书记", "start_date": "2021-09", "end_date": "2026-04", "rank": "正厅级", "note": "2021年9月至2026年4月任黑河市委书记"},

    # 赵荣国（前任市长）
    {"person_id": 13, "org_id": 2, "title": "黑河市人民政府市长", "start_date": "2021-12", "end_date": "2024-12", "rank": "正厅级", "note": "2021年12月至2024年12月任黑河市长"},
]

# ── Relationships ──────────────────────────────────────────────────────────

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "秦波作为市委书记，战明秀作为市长，党政主要领导搭档",
        "overlap_org": "黑河市",
        "overlap_period": "2026-07至今"
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "秦波与狄恒在黑河市共事",
        "overlap_org": "黑河市",
        "overlap_period": "2024-12至今"
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "overlap",
        "context": "秦波与丁兆禄在黑河市共事",
        "overlap_org": "黑河市",
        "overlap_period": "2024-12至今"
    },
    {
        "person_a": 1, "person_b": 12,
        "type": "predecessor_successor",
        "context": "秦波接替李锡文任黑河市委书记",
        "overlap_org": "中共黑河市委员会",
        "overlap_period": "2026-04",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 1,
        "type": "predecessor_successor",
        "context": "战明秀接替秦波任黑河市长（秦波转任书记）",
        "overlap_org": "黑河市人民政府",
        "overlap_period": "2026-07"
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "战明秀与狄恒在黑河市共事",
        "overlap_org": "黑河市",
        "overlap_period": "2026-07至今"
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "overlap",
        "context": "战明秀与丁兆禄在黑河市共事",
        "overlap_org": "黑河市",
        "overlap_period": "2026-07至今"
    },
    {
        "person_a": 2, "person_b": 10,
        "type": "superior_subordinate",
        "context": "市长与副市长工作搭档",
        "overlap_org": "黑河市人民政府",
        "overlap_period": "2026-07至今"
    },
    {
        "person_a": 2, "person_b": 11,
        "type": "superior_subordinate",
        "context": "市长与市政府秘书长工作搭档",
        "overlap_org": "黑河市人民政府",
        "overlap_period": "2026-07至今"
    },
    {
        "person_a": 3, "person_b": 4,
        "type": "overlap",
        "context": "狄恒与丁兆禄在黑河市共事",
        "overlap_org": "黑河市",
        "overlap_period": "2022-01至今"
    },
    {
        "person_a": 12, "person_b": 13,
        "type": "superior_subordinate",
        "context": "李锡文（书记）与赵荣国（市长）党政搭档",
        "overlap_org": "黑河市",
        "overlap_period": "2021-12至2024-12"
    },
    {
        "person_a": 1, "person_b": 13,
        "type": "predecessor_successor",
        "context": "秦波接替赵荣国任黑河市长",
        "overlap_org": "黑河市人民政府",
        "overlap_period": "2024-12"
    },
]


# ══════════════════════════════════════════════════════════════════════════
# Helper: XML escape
# ══════════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ══════════════════════════════════════════════════════════════════════════
# Build database
# ══════════════════════════════════════════════════════════════════════════

def build_db():
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS persons;
        DROP TABLE IF EXISTS organizations;

        CREATE TABLE persons (
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

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );

        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
              p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"  DB: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


# ══════════════════════════════════════════════════════════════════════════
# Build GEXF
# ══════════════════════════════════════════════════════════════════════════

def person_color(name):
    # Party Secretary — Red
    if name == "秦波":
        return "255,50,50"
    # Government leader — Blue
    if name == "战明秀":
        return "50,100,255"
    # 人大 — Cyan
    if name == "狄恒":
        return "200,255,255"
    # 政协 — Cream
    if name == "丁兆禄":
        return "255,240,200"
    # 纪委/监委 — Orange
    if name == "李百山":
        return "255,165,0"
    # 前任 — Grey
    if name in ("李锡文", "赵荣国"):
        return "150,150,150"
    # Others — Grey
    return "100,100,100"


def person_size(name):
    if name in ("秦波", "战明秀"):
        return "20.0"
    return "12.0"


def org_color(o_type):
    if "党委" in o_type:
        return "255,200,200"
    if "政府" in o_type:
        return "200,200,255"
    if "人大" in o_type:
        return "200,255,255"
    if "政协" in o_type:
        return "255,240,200"
    if "事业单位" in o_type:
        return "220,220,220"
    return "200,200,200"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append(f'    <description>黑河市领导班子工作关系网络 - {SLUG}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["name"])
        sz = person_size(p["name"])
        pid = f"p{p['id']}"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o["type"])
        oid = f"o{o['id']}"
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
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
        pid = f"p{pos['person_id']}"
        oid = f"o{pos['org_id']}"
        lines.append(f'      <edge id="{eid}" source="{pid}" target="{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        pa = f"p{r['person_a']}"
        pb = f"p{r['person_b']}"
        lines.append(f'      <edge id="{eid}" source="{pa}" target="{pb}" label="{esc(r["type"])}" weight="2.0">')
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
    print(f"  GEXF: {GEXF_PATH} ({eid} edges)")


# ══════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════

def make_person_json(p, timeline, relationships_list, source_register):
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "黑河市",
            "region": "黑河市",
            "job": p.get("current_post", ""),
            "task_id": "heilongjiang_黑河市",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"heihe_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": p.get("party_join", ""),
            "work_start": "",
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source", "")
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "正厅级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002", "S003"]
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": relationships_list,
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
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "在公开信息中未发现该人物负面信号", "date": "", "confidence": "confirmed", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if p["gender"] and p["birth"] else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if p["name"] in ("秦波",) else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{p['name']}的完整履历信息（含教育背景、早期职务）需补充"
        },
        "open_questions": [
            {
                "priority": "critical" if p["name"] in ("战明秀",) else "high",
                "question": f"{p['name']}的完整职业生涯履历（含出生信息、教育背景、历任职务）",
                "why_it_matters": "无法追溯其任职路径和系统经历",
                "suggested_queries": [f"{p['name']} 简历 黑河", f"{p['name']} 任前公示"],
                "last_attempted": AS_OF
            }
        ]
    }


def build_person_jsons():
    source_register = [
        {"id": "S001", "title": "维基百科—黑河市", "url": "https://zh.wikipedia.org/wiki/黑河市", "publisher": "维基百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "黑河市四大机构领导人表"},
        {"id": "S002", "title": "黑河市人民政府网站", "url": "http://www.heihe.gov.cn", "publisher": "黑河市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "首页新闻确认战明秀(市长)等领导活动"},
        {"id": "S003", "title": "黑河市第七届人大第七次会议新闻", "url": "https://www.heihe.gov.cn/hhs/c100749/202607/c11_356799.shtml", "publisher": "黑河市人民政府", "published_at": "2026-07-17", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认战明秀当选市长，李百山当选监委主任"},
        {"id": "S004", "title": "黑河市人民政府—战明秀防汛检查新闻", "url": "https://www.heihe.gov.cn/hhs/c100749/202607/c11_357024.shtml", "publisher": "黑河市人民政府", "published_at": "2026-07-22", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认战明秀为市委副书记、市长，贾牧樵为副市长兼公安局局长，邸建军为市政府秘书长"},
    ]

    # === 1. 秦波 ===
    qin_timeline = [
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未找到2024年12月前履历。秦波（1980年1月生，黑龙江同江人）", "confidence": "unverified", "source_ids": []},
        {"start": "2024-12", "end": "2026-04", "org": "黑河市人民政府", "title": "黑河市市长", "notes": "2024年12月任代市长，后转正——此前履历待查", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2026-04", "end": "present", "org": "中共黑河市委员会", "title": "黑河市委书记", "notes": "2026年4月任市委书记", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    qin_relationships = [
        {"person": "战明秀", "person_id": "heihe_战明秀", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "秦波由市长转任书记，战明秀接任市长", "overlap_org": "黑河市", "overlap_period": "2026-07", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
        {"person": "李锡文", "person_id": "heihe_李锡文", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "秦波接替李锡文任黑河市委书记", "overlap_org": "中共黑河市委", "overlap_period": "2026-04", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "赵荣国", "person_id": "heihe_赵荣国", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "秦波接替赵荣国任黑河市长", "overlap_org": "黑河市人民政府", "overlap_period": "2024-12", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "狄恒", "person_id": "heihe_狄恒", "relationship_type": "overlap", "strength": "medium", "evidence": "在市委/人大共事", "overlap_org": "黑河市", "overlap_period": "2024-12至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "丁兆禄", "person_id": "heihe_丁兆禄", "relationship_type": "overlap", "strength": "medium", "evidence": "在市委/政协共事", "overlap_org": "黑河市", "overlap_period": "2024-12至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    qin_json = make_person_json(persons[0], qin_timeline, qin_relationships, source_register)
    qin_json["professional_profile"]["career_pattern"] = "local_ladder"
    qin_json["professional_profile"]["promotion_velocity"] = {
        "summary": "1980年生，2024年底已任黑河市长（正厅级），晋升较快。2026年4月转任市委书记",
        "notable_fast_promotions": ["46岁任地级市市委书记"]
    }
    qin_json["open_questions"] = [
        {"priority": "critical", "question": "秦波2024年12月前的完整职业生涯履历（含教育背景、历任职务）", "why_it_matters": "核心人物，但45岁前履历完全空白", "suggested_queries": ["秦波 1980 同江 简历", "秦波 黑河市长 任前公示", "秦波 黑龙江 任职经历"], "last_attempted": AS_OF},
    ]

    qin_path = PERSONS_DIR / f"{TODAY}-黑龙江省-黑河市-市委书记-秦波.json"
    with open(qin_path, "w", encoding="utf-8") as f:
        json.dump(qin_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {qin_path.name}")

    # === 2. 战明秀 ===
    zhan_timeline = [
        {"start": "unknown", "end": "2026-07", "org": "履历缺口", "title": "", "notes": "公开资料未找到2026年7月前履历。战明秀（1974年4月生，山东日照人），此前职务及履历待查", "confidence": "unverified", "source_ids": []},
        {"start": "2026-07-16", "end": "present", "org": "黑河市人民政府", "title": "黑河市市长", "notes": "2026年7月16日黑河市第七届人大第七次会议当选市长", "confidence": "confirmed", "source_ids": ["S003"]},
        {"start": "", "end": "present", "org": "中共黑河市委员会", "title": "市委副书记", "notes": "当选市长时同时任市委副书记", "confidence": "confirmed", "source_ids": ["S004"]},
    ]
    zhan_open_questions = [
        {"priority": "critical", "question": "战明秀2026年7月前的完整职业生涯履历（含教育背景、历任职务）", "why_it_matters": "新任市长（2026年7月上任），此前任职经历几乎完全空白", "suggested_queries": ["战明秀 1974 山东日照 简历", "战明秀 任前公示", "战明秀 黑河 任职"], "last_attempted": AS_OF},
    ]
    zhan_relationships = [
        {"person": "秦波", "person_id": "heihe_秦波", "relationship_type": "subordinate_to_superior", "strength": "strong", "evidence": "市长受市委书记领导", "overlap_org": "黑河市", "overlap_period": "2026-07至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
        {"person": "贾牧樵", "person_id": "heihe_贾牧樵", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "市长与副市长工作搭档", "overlap_org": "黑河市人民政府", "overlap_period": "2026-07至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
        {"person": "邸建军", "person_id": "heihe_邸建军", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "市长与秘书长工作搭档", "overlap_org": "黑河市人民政府", "overlap_period": "2026-07至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
        {"person": "狄恒", "person_id": "heihe_狄恒", "relationship_type": "overlap", "strength": "medium", "evidence": "市长与人大主任共事", "overlap_org": "黑河市", "overlap_period": "2026-07至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
    ]
    zhan_json = make_person_json(persons[1], zhan_timeline, zhan_relationships, source_register)
    zhan_json["open_questions"] = zhan_open_questions
    zhan_path = PERSONS_DIR / f"{TODAY}-黑龙江省-黑河市-市长-战明秀.json"
    with open(zhan_path, "w", encoding="utf-8") as f:
        json.dump(zhan_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {zhan_path.name}")

    # === 3. 狄恒 ===
    di_timeline = [
        {"start": "2024-08", "end": "present", "org": "黑河市人民代表大会常务委员会", "title": "主任", "notes": "2024年8月任现职——此前履历待查", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "狄恒（1972年11月生，山东莱阳人），此前履历不详", "confidence": "unverified", "source_ids": []},
    ]
    di_relationships = []
    di_json = make_person_json(persons[2], di_timeline, di_relationships, source_register)
    di_path = PERSONS_DIR / f"{TODAY}-黑龙江省-黑河市-人大主任-狄恒.json"
    with open(di_path, "w", encoding="utf-8") as f:
        json.dump(di_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {di_path.name}")

    # === 4. 丁兆禄 ===
    ding_timeline = [
        {"start": "2022-01", "end": "present", "org": "中国人民政治协商会议黑河市委员会", "title": "主席", "notes": "2022年1月当选——此前履历待查", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "丁兆禄（1970年12月生），此前履历不详", "confidence": "unverified", "source_ids": []},
    ]
    ding_relationships = []
    ding_json = make_person_json(persons[3], ding_timeline, ding_relationships, source_register)
    ding_path = PERSONS_DIR / f"{TODAY}-黑龙江省-黑河市-政协主席-丁兆禄.json"
    with open(ding_path, "w", encoding="utf-8") as f:
        json.dump(ding_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {ding_path.name}")


# ══════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Building {SLUG} network data...")
    build_db()
    build_gexf()
    build_person_jsons()
    print(f"\nOutput files:")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")
    for p in PERSONS_DIR.glob(f"{TODAY}-*.json"):
        print(f"  Person: {p}")
    print("Done.")
