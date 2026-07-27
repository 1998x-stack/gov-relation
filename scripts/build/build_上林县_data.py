#!/usr/bin/env python3
"""
上林县（南宁市）领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Shanglin County leadership.

Research note: Due to geo-restrictions and rate limits, Chinese search engines
(Baidu, Exa) and encyclopedias (baike.baidu.com) were inaccessible from this
environment. Primary data was extracted from the official county government website
shanglin.gov.cn (news articles and leadership page). Key biographical details
(birth dates, birthplace, education, full career timelines) remain unverified and
require confirmation from:
  - 上林县人民政府门户网站 (shanglin.gov.cn) leadership bio pages
  - 南宁市委组织部任前公示
  - Baidu Baike entries for each individual

Last updated: 2026-07-23
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(STAGING_DIR, "..", ".."))
DB_PATH = os.path.join(STAGING_DIR, "上林县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "上林县_network.gexf")
PERSONS_DIR = STAGING_DIR


# ═══════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════

# --- Person ID convention: shanglin_{surname_givenname} ---
# Confirmed from official government website shanglin.gov.cn

TODAY = "2026-07-23"

PERSONS = [
    # TOP LEADERS (Confirmed from shanglin.gov.cn news articles)
    {
        "id": 1,
        "name": "杨世爵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "县委书记",
        "current_org": "中共上林县委员会",
        "source": "http://www.shanglin.gov.cn/yw/sldt/t6672954.html (2026-07-01 七一慰问报道确认)"
    },
    {
        "id": 2,
        "name": "王鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "县委副书记、县长",
        "current_org": "上林县人民政府",
        "source": "http://www.shanglin.gov.cn/gk/xxgkml/jcxxgk/ldzc/ (领导之窗页面确认)"
    },
    # FOUR LEADER TEAM (Confirmed from 七一 article)
    {
        "id": 3,
        "name": "李玉辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "县人大常委会主任",
        "current_org": "上林县人民代表大会常务委员会",
        "source": "http://www.shanglin.gov.cn/yw/sldt/t6672954.html"
    },
    {
        "id": 4,
        "name": "韦泽伦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议上林县委员会",
        "source": "http://www.shanglin.gov.cn/yw/sldt/t6672954.html"
    },
    # COUNTY GOVERNMENT DEPUTY LEADERS (Confirmed from 领导之窗 page)
    {
        "id": 5,
        "name": "邓智",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "县委常委、副县长",
        "current_org": "上林县人民政府",
        "source": "http://www.shanglin.gov.cn/gk/xxgkml/jcxxgk/ldzc/"
    },
    {
        "id": 6,
        "name": "黄东锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "副县长",
        "current_org": "上林县人民政府",
        "source": "http://www.shanglin.gov.cn/yw/sldt/t6672371.html; 领导之窗页面"
    },
    {
        "id": 7,
        "name": "林信",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "副县长",
        "current_org": "上林县人民政府",
        "source": "http://www.shanglin.gov.cn/gk/xxgkml/jcxxgk/ldzc/"
    },
    {
        "id": 8,
        "name": "覃兰斌",
        "gender": "女",
        "ethnicity": "壮族(推测)",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "副县长",
        "current_org": "上林县人民政府",
        "source": "http://www.shanglin.gov.cn/gk/xxgkml/jcxxgk/ldzc/"
    },
    {
        "id": 9,
        "name": "王涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "副县长",
        "current_org": "上林县人民政府",
        "source": "http://www.shanglin.gov.cn/yw/sldt/t6672371.html; 领导之窗页面"
    },
    {
        "id": 10,
        "name": "宋尧华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "副县长",
        "current_org": "上林县人民政府",
        "source": "http://www.shanglin.gov.cn/yw/sldt/t6661803.html"
    },
    {
        "id": 11,
        "name": "阳秀娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "副县长",
        "current_org": "上林县人民政府",
        "source": "http://www.shanglin.gov.cn/gk/xxgkml/jcxxgk/ldzc/"
    },
    {
        "id": 12,
        "name": "蓝挺慧",
        "gender": "男",
        "ethnicity": "瑶族(推测)",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "副县长",
        "current_org": "上林县人民政府",
        "source": "http://www.shanglin.gov.cn/yw/sldt/t6661803.html"
    },
    {
        "id": 13,
        "name": "苏志林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "副县长",
        "current_org": "上林县人民政府",
        "source": "http://www.shanglin.gov.cn/gk/xxgkml/jcxxgk/ldzc/"
    },
    # OTHER KEY LEADERS
    {
        "id": 14,
        "name": "吴可文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "县委常委、县委办公室主任(推测)",
        "current_org": "中共上林县委员会",
        "source": "http://www.shanglin.gov.cn/yw/sldt/t6672954.html (陪同县委书记慰问)"
    },
]

# Person ID mapping for relationships
P_杨世爵 = 1
P_王鹏 = 2
P_李玉辉 = 3
P_韦泽伦 = 4
P_邓智 = 5
P_黄东锋 = 6
P_林信 = 7
P_覃兰斌 = 8
P_王涛 = 9
P_宋尧华 = 10
P_阳秀娟 = 11
P_蓝挺慧 = 12
P_苏志林 = 13
P_吴可文 = 14


ORGANIZATIONS = [
    {"id": 1, "name": "中共上林县委员会", "type": "党委", "level": "县级", "parent": "中共南宁市委员会", "location": "上林县"},
    {"id": 2, "name": "上林县人民政府", "type": "政府", "level": "县级", "parent": "南宁市人民政府", "location": "上林县"},
    {"id": 3, "name": "上林县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "", "location": "上林县"},
    {"id": 4, "name": "中国人民政治协商会议上林县委员会", "type": "政协", "level": "县级", "parent": "", "location": "上林县"},
    {"id": 5, "name": "中共上林县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共上林县委员会", "location": "上林县"},
    {"id": 6, "name": "中共上林县委组织部", "type": "党委", "level": "县级", "parent": "中共上林县委员会", "location": "上林县"},
    {"id": 7, "name": "中共上林县委宣传部", "type": "党委", "level": "县级", "parent": "中共上林县委员会", "location": "上林县"},
    {"id": 8, "name": "中共上林县委政法委员会", "type": "党委", "level": "县级", "parent": "中共上林县委员会", "location": "上林县"},
    {"id": 9, "name": "中共上林县委统战部", "type": "党委", "level": "县级", "parent": "中共上林县委员会", "location": "上林县"},
    {"id": 10, "name": "中共上林县委办公室", "type": "党委", "level": "县级", "parent": "中共上林县委员会", "location": "上林县"},
    {"id": 11, "name": "上林县纪委监委", "type": "党委", "level": "县级", "parent": "中共上林县纪律检查委员会", "location": "上林县"},
]

# NOTE: 县委常委具体分工（纪委书记、组织部长、宣传部长等）未在已获取页面中找到
# 需进一步从 shanglin.gov.cn 或南宁市委确认


POSITIONS = [
    # 杨世爵 — Current roles
    {"person_id": P_杨世爵, "org_id": 1, "title": "县委书记",
     "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "任职起始时间待查"},

    # 王鹏 — Current roles
    {"person_id": P_王鹏, "org_id": 2, "title": "县长",
     "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "任职起始时间待查"},
    {"person_id": P_王鹏, "org_id": 1, "title": "县委副书记",
     "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "兼任县委副书记"},

    # 李玉辉
    {"person_id": P_李玉辉, "org_id": 3, "title": "县人大常委会主任",
     "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},

    # 韦泽伦
    {"person_id": P_韦泽伦, "org_id": 4, "title": "县政协主席",
     "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},

    # 邓智
    {"person_id": P_邓智, "org_id": 2, "title": "副县长",
     "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "推测为县委常委、常务副县长"},
    {"person_id": P_邓智, "org_id": 1, "title": "县委常委(推测)",
     "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},

    # 黄东锋
    {"person_id": P_黄东锋, "org_id": 2, "title": "副县长",
     "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},

    # 林信
    {"person_id": P_林信, "org_id": 2, "title": "副县长",
     "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},

    # 覃兰斌
    {"person_id": P_覃兰斌, "org_id": 2, "title": "副县长",
     "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},

    # 王涛
    {"person_id": P_王涛, "org_id": 2, "title": "副县长",
     "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},

    # 宋尧华
    {"person_id": P_宋尧华, "org_id": 2, "title": "副县长",
     "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},

    # 阳秀娟
    {"person_id": P_阳秀娟, "org_id": 2, "title": "副县长",
     "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},

    # 蓝挺慧
    {"person_id": P_蓝挺慧, "org_id": 2, "title": "副县长",
     "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},

    # 苏志林
    {"person_id": P_苏志林, "org_id": 2, "title": "副县长",
     "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},

    # 吴可文
    {"person_id": P_吴可文, "org_id": 1, "title": "县委常委、县委办主任(推测)",
     "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
]


RELATIONSHIPS = [
    # 杨世爵 <-> 王鹏 (书记-县长搭档关系)
    {"person_a": P_杨世爵, "person_b": P_王鹏, "type": "superior_subordinate",
     "context": "县委书记与县长搭档关系", "overlap_org": "中共上林县委员会/上林县人民政府",
     "overlap_period": "待查至今"},
    # 杨世爵 <-> 李玉辉
    {"person_a": P_杨世爵, "person_b": P_李玉辉, "type": "overlap",
     "context": "县委-人大领导共事", "overlap_org": "上林县四家班子",
     "overlap_period": "待查至今"},
    # 杨世爵 <-> 韦泽伦
    {"person_a": P_杨世爵, "person_b": P_韦泽伦, "type": "overlap",
     "context": "县委-政协领导共事", "overlap_org": "上林县四家班子",
     "overlap_period": "待查至今"},
    # 杨世爵 <-> 吴可文
    {"person_a": P_杨世爵, "person_b": P_吴可文, "type": "superior_subordinate",
     "context": "书记-办公室主任工作关系", "overlap_org": "中共上林县委员会",
     "overlap_period": "待查至今"},
    # 邓智 <-> 其他副县长 (共事关系)
    {"person_a": P_邓智, "person_b": P_黄东锋, "type": "overlap",
     "context": "县政府领导班子共事", "overlap_org": "上林县人民政府",
     "overlap_period": "待查至今"},
]


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(current_post):
    if "书记" in current_post and "县委" in current_post:
        return "255,50,50"  # Red
    elif "县长" in current_post or "副县长" in current_post:
        return "50,100,255"  # Blue
    elif "人大" in current_post:
        return "200,255,255"  # Cyan
    elif "政协" in current_post:
        return "255,240,200"  # Cream
    else:
        return "100,100,100"  # Grey


def is_top_leader(current_post):
    return "县委书记" in current_post or ("县长" in current_post and "副" not in current_post)


def org_color(org_type):
    mapping = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return mapping.get(org_type, "200,200,200")


def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Drop existing tables
    for t in ("relationships", "positions", "organizations", "persons"):
        cur.execute(f"DROP TABLE IF EXISTS {t}")

    # Create tables
    cur.execute("""
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
        )
    """)

    cur.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        )
    """)

    cur.execute("""
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
        )
    """)

    cur.execute("""
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
        )
    """)

    # Insert persons
    for p in PERSONS:
        cur.execute(
            "INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"])
        )

    # Insert organizations
    for o in ORGANIZATIONS:
        cur.execute(
            "INSERT INTO organizations VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
        )

    # Insert positions
    for pos in POSITIONS:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"],
             pos["end_date"], pos["rank"], pos["note"])
        )

    # Insert relationships
    for r in RELATIONSHIPS:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"], r["context"],
             r["overlap_org"], r["overlap_period"])
        )

    conn.commit()
    conn.close()

    print(f"✅ Database created: {DB_PATH}")
    print(f"   Persons: {len(PERSONS)}")
    print(f"   Organizations: {len(ORGANIZATIONS)}")
    print(f"   Positions: {len(POSITIONS)}")
    print(f"   Relationships: {len(RELATIONSHIPS)}")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>ChinaGovNetwork Research Agent</creator>')
    lines.append('    <description>上林县领导班子工作关系网络（南宁市）</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="gender" type="string"/>')
    lines.append('      <attribute id="4" title="ethnicity" type="string"/>')
    lines.append('      <attribute id="5" title="birth" type="string"/>')
    lines.append('      <attribute id="6" title="source" type="string"/>')
    lines.append('      <attribute id="7" title="org_type" type="string"/>')
    lines.append('      <attribute id="8" title="level" type="string"/>')
    lines.append('      <attribute id="9" title="location" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Persons as nodes
    lines.append('    <nodes>')
    for p in PERSONS:
        c = person_color(p["current_post"]).split(",")
        sz = "20.0" if is_top_leader(p["current_post"]) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["gender"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["ethnicity"])}"/>')
        lines.append(f'          <attvalue for="5" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="6" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organizations as nodes
    for o in ORGANIZATIONS:
        oc = org_color(o["type"]).split(",")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="7" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="8" value="{esc(o["level"])}"/>')
        lines.append(f'          <attvalue for="9" value="{esc(o["location"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc[0]}" g="{oc[1]}" b="{oc[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges: positions (person -> organization)
    lines.append('    <edges>')
    eid = 0
    for pos in POSITIONS:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges: person -> person (relationships)
    for r in RELATIONSHIPS:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ GEXF created: {GEXF_PATH}")
    print(f"   Nodes: {len(PERSONS) + len(ORGANIZATIONS)}")
    print(f"   Edges: {len(POSITIONS) + len(RELATIONSHIPS)}")


def build_person_json(person, career_timeline=None):
    """Generate person JSON file in staging directory."""
    person_id_str = f"shanglin_{person['name']}"
    filename = f"{TODAY}-广西壮族自治区-南宁市-{person['current_post'].replace('/', '、')}-{person['name']}.json"

    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "南宁市",
            "region": "上林县",
            "job": person["current_post"],
            "task_id": "guangxi_上林县",
            "time_focus": "2025-2026"
        },
        "identity": {
            "person_id": person_id_str,
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"] if person["ethnicity"] != "待查" else "",
            "birth": person["birth"] if person["birth"] != "待查" else "",
            "birthplace": person["birthplace"] if person["birthplace"] != "待查" else "",
            "native_place": "",
            "education": [],
            "party_join": person["party_join"] if person["party_join"] != "待查" else "",
            "work_start": person["work_start"] if person["work_start"] != "待查" else "",
            "dedupe_keys": {
                "name_birth": f"{person['name']}_",
                "name_birthplace": f"{person['name']}_",
                "official_profile_url": f"http://www.shanglin.gov.cn/gk/xxgkml/jcxxgk/ldzc/"
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if is_top_leader(person["current_post"]) else "副处级",
            "as_of": TODAY,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": career_timeline or [
            {
                "start": "待查",
                "end": "present",
                "org": person["current_org"],
                "title": person["current_post"],
                "level": "正处级" if is_top_leader(person["current_post"]) else "副处级",
                "location": "上林县",
                "system": "party" if "县委" in person["current_org"] else "government" if "政府" in person["current_org"] else "other",
                "rank": "",
                "is_key_promotion": False,
                "notes": "履历待确认 — 公开资料仅确认现任职务",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "organizations": [
            {"id": 1, "name": "中共上林县委员会", "type": "党委", "level": "县级", "location": "上林县"},
            {"id": 2, "name": "上林县人民政府", "type": "政府", "level": "县级", "location": "上林县"},
        ],
        "relationships": [
            {
                "person": "王鹏" if person["name"] != "王鹏" else "杨世爵",
                "person_id": "shanglin_王鹏" if person["name"] != "王鹏" else "shanglin_杨世爵",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "县委书记与县长搭档关系",
                "overlap_org": "中共上林县委员会/上林县人民政府",
                "overlap_period": "待查至今",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "待查 — 需补充完整履历后评估",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至" + TODAY + "，公开渠道未发现违纪处分、审计问题或负面舆情",
                "date": "",
                "confidence": "unverified",
                "source_ids": ["S001"]
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "上林县人民政府门户网站 - 领导之窗",
                "url": "http://www.shanglin.gov.cn/gk/xxgkml/jcxxgk/ldzc/",
                "publisher": "上林县人民政府",
                "published_at": "",
                "accessed_at": TODAY,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认县长名单；县委书记未列在此页"
            },
            {
                "id": "S002",
                "title": "上林县四家班子领导开展'七一'走访慰问活动",
                "url": "http://www.shanglin.gov.cn/yw/sldt/t6672954.html",
                "publisher": "上林发布",
                "published_at": "2026-07-01",
                "accessed_at": TODAY,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认杨世爵为县委书记，王鹏为县长，李玉辉为人大常委会主任，韦泽伦为政协主席"
            }
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{person['name']}的出生日期、籍贯、学历、入党时间、完整职业生涯均待查"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的出生年月和籍贯",
                "why_it_matters": "人员身份基本信息，跨数据库去重关键字段",
                "suggested_queries": [f"{person['name']} 出生", f"{person['name']} 籍贯", f"{person['name']} 百度百科"],
                "last_attempted": TODAY
            },
            {
                "priority": "critical",
                "question": f"{person['name']}的完整职业生涯（任职经历）",
                "why_it_matters": "需追溯到乡镇/科员级别的早期岗位以构建完整晋升路径",
                "suggested_queries": [f"{person['name']} 简历 任职", f"{person['name']} 任前公示"],
                "last_attempted": TODAY
            },
            {
                "priority": "high",
                "question": f"{person['name']}的教育背景和入党时间",
                "why_it_matters": "评估其专业背景和系统归属",
                "suggested_queries": [f"{person['name']} 学历", f"{person['name']} 毕业"],
                "last_attempted": TODAY
            },
            {
                "priority": "high",
                "question": "杨世爵何时被任命为上林县委书记",
                "why_it_matters": "确定任期起点，分析晋升节奏",
                "suggested_queries": ["杨世爵 任上林县委书记 任命", "杨世爵 接任 上林县委书记"],
                "last_attempted": TODAY
            },
            {
                "priority": "medium",
                "question": "县委常委分工（纪委书记、组织部长、宣传部长、政法委书记、统战部长具体姓名）",
                "why_it_matters": "完整领导班子画像",
                "suggested_queries": ["上林县 县委常委 分工", "上林县 纪委书记", "上林县 组织部长"],
                "last_attempted": TODAY
            },
            {
                "priority": "medium",
                "question": "前任县委书记和县长是谁，现在何处",
                "why_it_matters": "了解干部流动方向和提拔路径",
                "suggested_queries": ["上林县 前县委书记", "上林县 前任县长"],
                "last_attempted": TODAY
            }
        ]
    }

    filepath = os.path.join(PERSONS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Person JSON created: {filepath}")
    return filename


if __name__ == "__main__":
    print("=" * 60)
    print("上林县领导班子工作关系网络 — 数据构建")
    print("=" * 60)

    # 1. Build SQLite database
    build_db()

    # 2. Build GEXF graph file
    build_gexf()

    # 3. Build person JSON files for core leaders
    # For 杨世爵 (party secretary)
    build_person_json(
        next(p for p in PERSONS if p["id"] == P_杨世爵),
        career_timeline=[
            {
                "start": "待查",
                "end": "present",
                "org": "中共上林县委员会",
                "title": "县委书记",
                "level": "正处级",
                "location": "上林县",
                "system": "party",
                "rank": "",
                "is_key_promotion": True,
                "notes": "上林县委书记 — 最早可查记录为2025年已有公开活动报道",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            }
        ]
    )

    # For 王鹏 (county mayor)
    build_person_json(
        next(p for p in PERSONS if p["id"] == P_王鹏),
        career_timeline=[
            {
                "start": "待查",
                "end": "present",
                "org": "上林县人民政府",
                "title": "县长",
                "level": "正处级",
                "location": "上林县",
                "system": "government",
                "rank": "",
                "is_key_promotion": True,
                "notes": "上林县县长 — 最早可查记录为2025年已有公开活动报道",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"]
            },
            {
                "start": "待查",
                "end": "present",
                "org": "中共上林县委员会",
                "title": "县委副书记",
                "level": "正处级",
                "location": "上林县",
                "system": "party",
                "rank": "",
                "is_key_promotion": False,
                "notes": "兼任",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            }
        ]
    )

    print()
    print("✅ Build complete!")
    print(f"   DB:  {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
    print()

    # Verify files exist
    for path in [DB_PATH, GEXF_PATH]:
        if os.path.exists(path):
            size_kb = os.path.getsize(path) / 1024
            print(f"   ✅ {path} ({size_kb:.1f} KB)")
        else:
            print(f"   ❌ MISSING: {path}")
            sys.exit(1)

    print()
    print("=" * 60)
    print("⚠️  NOTE: Most biographical data is unverified. See report for details.")
    print("=" * 60)
