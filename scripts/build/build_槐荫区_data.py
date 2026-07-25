#!/usr/bin/env python3
"""Build script for 济南市槐荫区 cadre exchange network investigation.

Data sourced from official 槐荫区政府 website (www.huaiyin.gov.cn),
news articles dated June-July 2026, and public biographical sources.

As-of date: 2026-07-25
"""

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Ensure gov_relation is importable
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

AS_OF = "2026-07-25"
AS_OF_SHORT = AS_OF.replace("-", "")

# Paths
TMP = Path(__file__).resolve().parent
DB_PATH = TMP / "槐荫区_network.db"
GEXF_PATH = TMP / "槐荫区_network.gexf"
PERSONS_DIR = TMP / "persons"

# =========================================================================
# DATA — persons, organizations, positions, relationships
# =========================================================================

# Confirmation sources (all from huaiyin.gov.cn official news):
# - "孙常建、曲京鹏会见中国银行济南分行客人" 2026-07-17
# - "孙常建、曲京鹏会见中交第二公路工程局有限公司客人" 2026-07-16
# - "全区社区警务团队建设运行动员部署会议召开" 2026-06-11 (曲京鹏 as 代区长)
# - "槐荫区优秀共产党员…表彰大会" 2026-07-01
# - "区委常委会召开会议" 2026-07-13
# - "全区数智槐荫建设推进大会" 2026-05-08

PERSONS_DATA = [
    # ── Top Leaders ──
    {
        "id": 1, "name": "孙常建", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "槐荫区委书记", "current_org": "中共济南市槐荫区委员会",
        "source": "http://www.huaiyin.gov.cn/col/col21117/art/2026/art_cf28fd57613942cb9d580385b5f8e99f.html"
    },
    {
        "id": 2, "name": "曲京鹏", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "槐荫区委副书记、区长", "current_org": "槐荫区人民政府",
        "source": "http://www.huaiyin.gov.cn/col/col21117/art/2026/art_cf28fd57613942cb9d580385b5f8e99f.html"
    },
    # ── Top 4 Leaders ──
    {
        "id": 3, "name": "熊高翔", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "槐荫区人大常委会主任", "current_org": "槐荫区人大常委会",
        "source": "http://www.huaiyin.gov.cn/col/col21117/art/2026/art_02e122e7986c45d8be3f38d4fa67fea0.html"
    },
    {
        "id": 4, "name": "韩军", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "槐荫区政协主席", "current_org": "槐荫区政协",
        "source": "http://www.huaiyin.gov.cn/col/col21117/art/2026/art_02e122e7986c45d8be3f38d4fa67fea0.html"
    },
    # ── Deputy Party Secretary ──
    {
        "id": 5, "name": "韩卫英", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "槐荫区委副书记、统战部部长",
        "current_org": "中共济南市槐荫区委员会",
        "source": "http://www.huaiyin.gov.cn/col/col21117/art/2026/art_52c00ecbc9f74b3cacd5b624d4e92a63.html"
    },
    # ── Economic Development Zone ──
    {
        "id": 6, "name": "王永华", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "济南槐荫经济开发区党工委副书记、管委会副主任",
        "current_org": "济南槐荫经济开发区管委会",
        "source": "http://www.huaiyin.gov.cn/col/col21117/art/2026/art_52c00ecbc9f74b3cacd5b624d4e92a63.html"
    },
    # ── Standing Committee Members / Key Deputies ──
    {
        "id": 7, "name": "何小刚", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "槐荫区委常委、副区长",
        "current_org": "槐荫区人民政府",
        "source": "http://www.huaiyin.gov.cn/col/col21118/art/2026/art_606169674a174f4fb1ef906a7346702f.html"
    },
    {
        "id": 8, "name": "陈鲁", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "槐荫区委常委、组织部部长",
        "current_org": "中共济南市槐荫区委员会组织部",
        "source": "http://www.huaiyin.gov.cn/col/col21117/art/2026/art_d92f4d136cde4c78b99394ae8d694d66.html"
    },
    {
        "id": 9, "name": "王振国", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "槐荫区领导（区委常委）",
        "current_org": "中共济南市槐荫区委员会",
        "source": "http://www.huaiyin.gov.cn/col/col21117/art/2026/art_5e4a00b82e404170988abd01cf0ec296.html"
    },
    {
        "id": 10, "name": "尹强", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "槐荫区领导（区委常委）",
        "current_org": "中共济南市槐荫区委员会",
        "source": "http://www.huaiyin.gov.cn/col/col21117/art/2026/art_04bc4115add24e5fa41393ffe48ee942.html"
    },
    {
        "id": 11, "name": "刘磊", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "槐荫区领导",
        "current_org": "中共济南市槐荫区委员会",
        "source": "http://www.huaiyin.gov.cn/col/col21117/art/2026/art_7add451149f84051b7d2213d07a0b51c.html"
    },
    # ── Deputy District Mayors ──
    {
        "id": 12, "name": "谷长军", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "槐荫区领导（副区长）",
        "current_org": "槐荫区人民政府",
        "source": "http://www.huaiyin.gov.cn/col/col21117/art/2026/art_5e4a00b82e404170988abd01cf0ec296.html"
    },
    {
        "id": 13, "name": "杨飞", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "槐荫区副区长",
        "current_org": "槐荫区人民政府",
        "source": "http://www.huaiyin.gov.cn/col/col21118/art/2026/art_d507bb50093944959e88d09f0bcbb218.html"
    },
    {
        "id": 14, "name": "李君", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "槐荫区副区长",
        "current_org": "槐荫区人民政府",
        "source": "http://www.huaiyin.gov.cn/col/col21118/art/2026/art_919c293e840d4c488ad2d5a1f278f831.html"
    },
    {
        "id": 15, "name": "葛方强", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "槐荫区副区长、槐荫公安分局局长",
        "current_org": "槐荫区人民政府 / 济南市公安局槐荫分局",
        "source": "http://www.huaiyin.gov.cn/col/col21118/art/2026/art_3b3edf9d99d54cd8b579e16d8979c198.html"
    },
    {
        "id": 16, "name": "李元宏", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "槐荫区领导",
        "current_org": "槐荫区人民政府",
        "source": "http://www.huaiyin.gov.cn/col/col21117/art/2026/art_7add451149f84051b7d2213d07a0b51c.html"
    },
]

ORGANIZATIONS_DATA = [
    {"id": 1, "name": "中共济南市槐荫区委员会", "type": "党委", "level": "县处级",
     "parent": "中共济南市委员会", "location": "济南市槐荫区"},
    {"id": 2, "name": "槐荫区人民政府", "type": "政府", "level": "县处级",
     "parent": "济南市人民政府", "location": "济南市槐荫区"},
    {"id": 3, "name": "槐荫区人大常委会", "type": "人大", "level": "县处级",
     "parent": "济南市人大常委会", "location": "济南市槐荫区"},
    {"id": 4, "name": "槐荫区政协", "type": "政协", "level": "县处级",
     "parent": "济南市政协", "location": "济南市槐荫区"},
    {"id": 5, "name": "中共济南市槐荫区委员会组织部", "type": "党委", "level": "乡科级",
     "parent": "中共济南市槐荫区委员会", "location": "济南市槐荫区"},
    {"id": 6, "name": "中共济南市槐荫区委员会统战部", "type": "党委", "level": "乡科级",
     "parent": "中共济南市槐荫区委员会", "location": "济南市槐荫区"},
    {"id": 7, "name": "济南槐荫经济开发区管委会", "type": "开发区", "level": "县处级",
     "parent": "济南市人民政府", "location": "济南市槐荫区"},
    {"id": 8, "name": "济南市公安局槐荫分局", "type": "政府", "level": "乡科级",
     "parent": "济南市公安局", "location": "济南市槐荫区"},
]

POSITIONS_DATA = [
    # 孙常建
    {"person_id": 1, "org_id": 1, "title": "槐荫区委书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "现任槐荫区委书记，confirmed as of 2026-07"},
    # 曲京鹏
    {"person_id": 2, "org_id": 1, "title": "槐荫区委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "2026年6月任槐荫区代区长，后任区长"},
    {"person_id": 2, "org_id": 2, "title": "槐荫区区长",
     "start_date": "2026-06", "end_date": "present", "rank": "县处级正职",
     "note": "2026年6月11日以代区长身份出席活动"},
    # 熊高翔
    {"person_id": 3, "org_id": 3, "title": "槐荫区人大常委会主任",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 韩军
    {"person_id": 4, "org_id": 4, "title": "槐荫区政协主席",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 韩卫英
    {"person_id": 5, "org_id": 1, "title": "槐荫区委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 6, "title": "槐荫区委统战部部长",
     "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": ""},
    # 王永华
    {"person_id": 6, "org_id": 7, "title": "济南槐荫经济开发区党工委副书记、管委会副主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 何小刚
    {"person_id": 7, "org_id": 1, "title": "槐荫区委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "槐荫区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 陈鲁
    {"person_id": 8, "org_id": 1, "title": "槐荫区委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 5, "title": "槐荫区委组织部部长",
     "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": ""},
    # 王振国
    {"person_id": 9, "org_id": 1, "title": "槐荫区委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认"},
    # 尹强
    {"person_id": 10, "org_id": 1, "title": "槐荫区委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认"},
    # 刘磊
    {"person_id": 11, "org_id": 1, "title": "槐荫区领导",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认"},
    # 谷长军
    {"person_id": 12, "org_id": 2, "title": "槐荫区领导（副区长）",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 杨飞
    {"person_id": 13, "org_id": 2, "title": "槐荫区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "分管乡村振兴、农业农村"},
    # 李君
    {"person_id": 14, "org_id": 2, "title": "槐荫区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "分管行政审批、营商环境"},
    # 葛方强
    {"person_id": 15, "org_id": 2, "title": "槐荫区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 8, "title": "槐荫公安分局局长",
     "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": ""},
    # 李元宏
    {"person_id": 16, "org_id": 2, "title": "槐荫区领导",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认"},
]

RELATIONSHIPS_DATA = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记与区长搭档关系",
        "overlap_org": "中共济南市槐荫区委员会/槐荫区人民政府",
        "overlap_period": "2026-至今",
        "strength": "strong",
        "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 5,
        "type": "superior_subordinate",
        "context": "区委书记与分管统战工作的副书记",
        "overlap_org": "中共济南市槐荫区委员会",
        "overlap_period": "2026-至今",
        "strength": "strong",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 5,
        "type": "overlap",
        "context": "两位区委副书记在区委常委会共事",
        "overlap_org": "中共济南市槐荫区委员会",
        "overlap_period": "2026-至今",
        "strength": "medium",
        "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 7,
        "type": "superior_subordinate",
        "context": "区委书记与区委常委、副区长",
        "overlap_org": "中共济南市槐荫区委员会",
        "overlap_period": "2026-至今",
        "strength": "medium",
        "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 8,
        "type": "superior_subordinate",
        "context": "区委书记与组织部部长",
        "overlap_org": "中共济南市槐荫区委员会",
        "overlap_period": "2026-至今",
        "strength": "medium",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 7,
        "type": "superior_subordinate",
        "context": "区长与常务副区长（分管）",
        "overlap_org": "槐荫区人民政府",
        "overlap_period": "2026-至今",
        "strength": "strong",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 13,
        "type": "superior_subordinate",
        "context": "区长与分管农业农村的副区长",
        "overlap_org": "槐荫区人民政府",
        "overlap_period": "2026-至今",
        "strength": "medium",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 14,
        "type": "superior_subordinate",
        "context": "区长与分管行政审批的副区长",
        "overlap_org": "槐荫区人民政府",
        "overlap_period": "2026-至今",
        "strength": "medium",
        "confidence": "confirmed"
    },
    {
        "person_a": 15, "person_b": 2,
        "type": "superior_subordinate",
        "context": "公安分局局长受区长领导",
        "overlap_org": "槐荫区人民政府",
        "overlap_period": "2026-至今",
        "strength": "medium",
        "confidence": "confirmed"
    },
    {
        "person_a": 7, "person_b": 13,
        "type": "overlap",
        "context": "同为副区长在区政府共事",
        "overlap_org": "槐荫区人民政府",
        "overlap_period": "2026-至今",
        "strength": "medium",
        "confidence": "confirmed"
    },
    {
        "person_a": 7, "person_b": 14,
        "type": "overlap",
        "context": "同为副区长在区政府共事",
        "overlap_org": "槐荫区人民政府",
        "overlap_period": "2026-至今",
        "strength": "medium",
        "confidence": "confirmed"
    },
    {
        "person_a": 7, "person_b": 15,
        "type": "overlap",
        "context": "同为副区长在区政府共事",
        "overlap_org": "槐荫区人民政府",
        "overlap_period": "2026-至今",
        "strength": "medium",
        "confidence": "confirmed"
    },
]


# =========================================================================
# BUILD FUNCTIONS
# =========================================================================

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return r,g,b based on role."""
    post = p.get("current_post", "")
    if "区委书记" in post or "县委书记" in post:
        return "255,50,50"
    if "区长" in post or "县长" in post or "市长" in post:
        return "50,100,255"
    if "纪委书记" in post:
        return "255,165,0"
    return "100,100,100"

def is_top_leader(p):
    post = p.get("current_post", "")
    return "区委书记" in post or ("区长" in post and "副" not in post)

def build_database():
    """Create SQLite database."""
    print(f"Building database: {DB_PATH}")
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")

    conn.executescript("""
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
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    # Insert persons
    for p in PERSONS_DATA:
        conn.execute(
            "INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"])
        )
    print(f"  Persons: {len(PERSONS_DATA)}")

    # Insert organizations
    for o in ORGANIZATIONS_DATA:
        conn.execute(
            "INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
        )
    print(f"  Organizations: {len(ORGANIZATIONS_DATA)}")

    # Insert positions
    for pos in POSITIONS_DATA:
        s = pos.get("start_date", pos.get("start", ""))
        e = pos.get("end_date", pos.get("end", ""))
        conn.execute(
            "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"], s,
             e, pos["rank"], pos["note"])
        )
    print(f"  Positions: {len(POSITIONS_DATA)}")

    # Insert relationships
    for r in RELATIONSHIPS_DATA:
        conn.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"], r["context"],
             r["overlap_org"], r["overlap_period"])
        )
    print(f"  Relationships: {len(RELATIONSHIPS_DATA)}")

    conn.commit()
    conn.close()
    print("  Database ready.")


def build_gexf():
    """Create GEXF graph file."""
    print(f"Building GEXF: {GEXF_PATH}")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append('    <description>济南市槐荫区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in PERSONS_DATA:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("source", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    org_colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    for o in ORGANIZATIONS_DATA:
        oc = org_colors.get(o["type"], "200,200,200")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> Organization (worked_at)
    for pos in POSITIONS_DATA:
        ps = pos.get("start_date", pos.get("start", ""))
        pe = pos.get("end_date", pos.get("end", ""))
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(f"{ps} - {pe}")}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person -> Person (relationship)
    for r in RELATIONSHIPS_DATA:
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF ready: {eid + 1} edges")


def write_person_json():
    """Write individual person JSON files."""
    PERSONS_DIR.mkdir(parents=True, exist_ok=True)
    PROV = "山东省"
    CITY = "济南市"

    person_files = [
        {
            "filename": f"{AS_OF_SHORT}-{PROV}-{CITY}-{i.get('current_post', 'unknown').replace('/', '_')}-{i['name']}.json",
            "scope_job": i.get("current_post", ""),
            "name": i["name"],
            "pid": i["id"],
        }
        for i in PERSONS_DATA
    ]

    # Build the JSON for the two core leaders with what we know
    persons_detail = {
        1: {
            "name": "孙常建",
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "party_join": "中共党员",
            "work_start": "",
            "current_post": "槐荫区委书记",
            "current_org": "中共济南市槐荫区委员会",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "career_entries": [],
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "biggest_gap": "出生年月、籍贯、教育背景、完整履历均缺失"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "孙常建出生年月、籍贯、教育背景？",
                    "why_it_matters": "核心领导人的基本身份信息",
                    "suggested_queries": ["孙常建 简历 百度百科", "孙常建 出生 籍贯"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "critical",
                    "question": "孙常建何时何地任槐荫区委书记？之前任何职？",
                    "why_it_matters": "需了解其晋升路径和前任关系",
                    "suggested_queries": ["孙常建 任槐荫区 书记 时间", "孙常建 历任 职务"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": "孙常建此前是否曾任槐荫区区长或其他职务？",
                    "why_it_matters": "确定其是否从本区晋升",
                    "suggested_queries": ["孙常建 槐荫区 区长"],
                    "last_attempted": AS_OF
                }
            ],
            "sources": [
                {
                    "id": "S001",
                    "title": "槐荫区政府门户网站 - 孙常建、曲京鹏会见中国银行济南分行客人",
                    "url": "http://www.huaiyin.gov.cn/col/col21117/art/2026/art_cf28fd57613942cb9d580385b5f8e99f.html",
                    "publisher": "济南市槐荫区人民政府",
                    "published_at": "2026-07-17",
                    "accessed_at": AS_OF,
                    "source_type": "official",
                    "reliability": "high"
                }
            ]
        },
        2: {
            "name": "曲京鹏",
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "party_join": "中共党员",
            "work_start": "",
            "current_post": "槐荫区委副书记、区长",
            "current_org": "槐荫区人民政府",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "career_entries": [
                {
                    "start": "2026-06",
                    "end": "present",
                    "org": "槐荫区人民政府",
                    "title": "槐荫区区长（代区长→区长）",
                    "rank": "县处级正职",
                    "confidence": "confirmed"
                },
                {
                    "start": "2026-06",
                    "end": "present",
                    "org": "中共济南市槐荫区委员会",
                    "title": "槐荫区委副书记",
                    "rank": "县处级副职",
                    "confidence": "confirmed"
                }
            ],
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "biggest_gap": "出生年月、籍贯、教育背景、2026年之前的完整履历均缺失"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "曲京鹏出生年月、籍贯、教育背景？",
                    "why_it_matters": "核心领导人的基本身份信息",
                    "suggested_queries": ["曲京鹏 简历 百度百科", "曲京鹏 出生 籍贯"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "critical",
                    "question": "曲京鹏2026年6月前任任何职？从何处调入槐荫区？",
                    "why_it_matters": "了解其晋升路径和来源",
                    "suggested_queries": ["曲京鹏 任前公示 济南 槐荫区"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": "曲京鹏此前是否在济南市其他区县或市直机关任职？",
                    "why_it_matters": "考察其跨区县轮岗经历",
                    "suggested_queries": ["曲京鹏 济南 任职"],
                    "last_attempted": AS_OF
                }
            ],
            "sources": [
                {
                    "id": "S001",
                    "title": "槐荫区政府门户网站 - 全区社区警务团队建设运行动员部署会议召开",
                    "url": "http://www.huaiyin.gov.cn/col/col21117/art/2026/art_7add451149f84051b7d2213d07a0b51c.html",
                    "publisher": "济南市槐荫区人民政府",
                    "published_at": "2026-06-11",
                    "accessed_at": AS_OF,
                    "source_type": "official",
                    "reliability": "high",
                    "notes": "曲京鹏以代区长身份首次公开出席活动"
                },
                {
                    "id": "S002",
                    "title": "槐荫区政府门户网站 - 曲京鹏带队赴青岛考察招商",
                    "url": "http://www.huaiyin.gov.cn/col/col21117/art/2026/art_8e8b0acc53f8466c92e99be9f1138c6c.html",
                    "publisher": "济南市槐荫区人民政府",
                    "published_at": "2026-07-10",
                    "accessed_at": AS_OF,
                    "source_type": "official",
                    "reliability": "high",
                    "notes": "曲京鹏以区长身份出席活动"
                }
            ]
        }
    }

    # Write core leader person JSON files
    for pid, detail in persons_detail.items():
        p_data = next(p for p in PERSONS_DATA if p["id"] == pid)
        filename = f"{AS_OF_SHORT}-{PROV}-{CITY}-{p_data['current_post'].replace('/', '_')}-{detail['name']}.json"
        filepath = PERSONS_DIR / filename

        job_slug = p_data["current_post"]
        if "书记" in job_slug:
            job_short = "区委书记"
        elif "区长" in job_slug:
            job_short = "区长"
        else:
            job_short = job_slug

        person_json = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": PROV,
                "city": CITY,
                "region": "槐荫区",
                "job": job_short,
                "task_id": "shandong_槐荫区",
                "time_focus": AS_OF
            },
            "identity": {
                "person_id": f"huaiyin_{detail['name']}",
                "name": detail["name"],
                "aliases": [],
                "gender": detail["gender"],
                "ethnicity": detail["ethnicity"],
                "birth": detail["birth"],
                "birthplace": detail["birthplace"],
                "native_place": detail["native_place"],
                "education": [],
                "party_join": detail["party_join"],
                "work_start": detail["work_start"],
                "dedupe_keys": {
                    "name_birth": f"{detail['name']}_",
                    "name_birthplace": f"{detail['name']}_",
                    "official_profile_url": detail["sources"][0]["url"] if detail["sources"] else ""
                }
            },
            "current_status": {
                "current_post": detail["current_post"],
                "current_org": detail["current_org"],
                "administrative_rank": "县处级正职",
                "as_of": detail["as_of"],
                "is_current_confirmed": detail["is_current_confirmed"],
                "source_ids": [s["id"] for s in detail["sources"]]
            },
            "career_timeline": detail["career_entries"],
            "organizations": [],
            "relationships": [],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "数据不足，无法评估晋升速度", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "公开数据不足，无法评估工作风格"
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "截至2026年7月，公开渠道未发现该人员的纪律处分、审计问题或负面报道",
                    "date": AS_OF,
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "source_register": detail["sources"],
            "confidence_summary": detail["confidence_summary"],
            "open_questions": detail["open_questions"]
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(person_json, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {filename}")


def main():
    print(f"\n{'='*60}")
    print(f"  槐荫区 领导班子工作关系网络 — 数据构建脚本")
    print(f"  As of: {AS_OF}")
    print(f"{'='*60}\n")

    build_database()
    build_gexf()
    write_person_json()

    print(f"\n{'='*60}")
    print(f"  构建完成！")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  JSON: {PERSONS_DIR}/")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
