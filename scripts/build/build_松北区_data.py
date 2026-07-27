#!/usr/bin/env python3
"""松北区（哈尔滨市）领导班子关系网络生成脚本

数据来源：
  - 哈尔滨市松北区人民政府官网 (www.songbei.gov.cn) 领导信息及新闻报道
  - 松北区第五届人民代表大会第五次会议报道 (2026-01-26)
  - 各区政府领导简历页面

数据截至：2026年7月

Target roles:
  - 区委书记/哈尔滨新区党工委书记: 肖彬
  - 区委副书记、区长/哈尔滨新区管委会主任: 贺业方
  - 区委常委、常务副区长: 董方
  - 区委常委、副区长: 陈方晔
  - 副区长: 夏厦（无党派）
  - 副区长: 苏志
  - 副区长、公安分局局长: 刘辉
  - 副区长: 葛红升
  - 副区长: 刘惟乔
  - 区人大常委会主任: 黄明瑾
"""

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──
REPO = Path(__file__).resolve().parent
DB_PATH = REPO / "data/database/松北区_network.db"
GEXF_PATH = REPO / "data/graph/松北区_network.gexf"
PERSONS_DIR = REPO / "data/persons"

TODAY = "2026-07-24"
AS_OF = TODAY

# ── Helper ──
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# =========================================================================
# DATA
# =========================================================================

persons = [
    {
        "id": 1,
        "name": "肖彬",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "哈尔滨新区党工委书记、松北区委书记",
        "current_org": "中共哈尔滨市松北区委员会 / 哈尔滨新区党工委",
        "source": "https://www.songbei.gov.cn/",
    },
    {
        "id": 2,
        "name": "贺业方",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-03",
        "birthplace": "山东烟台",
        "education": "研究生，工学硕士",
        "party_join": "2004-04",
        "work_start": "2010-07",
        "current_post": "哈尔滨新区党工委副书记、管委会主任，松北区委副书记、政府区长",
        "current_org": "哈尔滨市松北区人民政府 / 哈尔滨新区管委会",
        "source": "https://www.songbei.gov.cn/hebsbq/xiaobin/ldxx.shtml",
    },
    {
        "id": 3,
        "name": "董方",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1973-02",
        "birthplace": "",
        "education": "大学，工程硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "松北区委常委、政府副区长（常务）、党组副书记",
        "current_org": "哈尔滨市松北区人民政府",
        "source": "https://www.songbei.gov.cn/hebsbq/dongfang/ldxx.shtml",
    },
    {
        "id": 4,
        "name": "陈方晔",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-02",
        "birthplace": "",
        "education": "大学，经济学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "松北区委常委、政府副区长",
        "current_org": "哈尔滨市松北区人民政府",
        "source": "https://www.songbei.gov.cn/hebsbq/cfy/ldxx.shtml",
    },
    {
        "id": 5,
        "name": "夏厦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-06",
        "birthplace": "",
        "education": "大学，工程硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "松北区政府副区长（无党派）",
        "current_org": "哈尔滨市松北区人民政府",
        "source": "https://www.songbei.gov.cn/hebsbq/xsqz/ldxx.shtml",
    },
    {
        "id": 6,
        "name": "苏志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-08",
        "birthplace": "",
        "education": "大学，管理学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "松北区政府副区长",
        "current_org": "哈尔滨市松北区人民政府",
        "source": "https://www.songbei.gov.cn/hebsbq/suzhi/ldxx.shtml",
    },
    {
        "id": 7,
        "name": "刘辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-09",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "松北区政府副区长、党组成员，区公安分局局长",
        "current_org": "哈尔滨市松北区人民政府 / 哈尔滨市公安局松北分局",
        "source": "https://www.songbei.gov.cn/hebsbq/c112168/ldxx.shtml",
    },
    {
        "id": 8,
        "name": "葛红升",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-02",
        "birthplace": "",
        "education": "市委党校大学",
        "party_join": "",
        "work_start": "",
        "current_post": "松北区政府副区长",
        "current_org": "哈尔滨市松北区人民政府",
        "source": "https://www.songbei.gov.cn/hebsbq/c112502/ldxx.shtml",
    },
    {
        "id": 9,
        "name": "刘惟乔",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-05",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "松北区政府副区长、党组成员",
        "current_org": "哈尔滨市松北区人民政府",
        "source": "https://www.songbei.gov.cn/hebsbq/c112521/ldxx.shtml",
    },
    {
        "id": 10,
        "name": "黄明瑾",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "松北区人大常委会主任",
        "current_org": "哈尔滨市松北区人大常委会",
        "source": "https://www.songbei.gov.cn/",
    },
    {
        "id": 11,
        "name": "赵琪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "松北区人大常委会副主任（大会执行主席）",
        "current_org": "哈尔滨市松北区人大常委会",
        "source": "https://www.songbei.gov.cn/hebsbq/sbdt/202601/c01_1104833.shtml",
    },
    {
        "id": 12,
        "name": "张建国",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "松北区领导（区委办）",
        "current_org": "中共哈尔滨市松北区委员会",
        "source": "https://www.songbei.gov.cn/hebsbq/sbdt/202602/c01_1110317.shtml",
    },
]

organizations = [
    {"id": 1, "name": "中共哈尔滨市松北区委员会", "type": "党委", "level": "县处级", "parent": "中共哈尔滨市委", "location": "松北区"},
    {"id": 2, "name": "哈尔滨市松北区人民政府", "type": "政府", "level": "县处级", "parent": "哈尔滨市人民政府", "location": "松北区"},
    {"id": 3, "name": "哈尔滨新区党工委", "type": "党委", "level": "正厅级", "parent": "中共哈尔滨市委", "location": "松北区"},
    {"id": 4, "name": "哈尔滨新区管理委员会", "type": "政府", "level": "正厅级", "parent": "哈尔滨市人民政府", "location": "松北区"},
    {"id": 5, "name": "中国（黑龙江）自由贸易试验区哈尔滨片区党工委", "type": "党委", "level": "正厅级", "parent": "中共黑龙江省委", "location": "松北区"},
    {"id": 6, "name": "中国（黑龙江）自由贸易试验区哈尔滨片区管委会", "type": "政府", "level": "正厅级", "parent": "黑龙江省人民政府", "location": "松北区"},
    {"id": 7, "name": "哈尔滨市松北区人大常委会", "type": "人大", "level": "县处级", "parent": "哈尔滨市人大常委会", "location": "松北区"},
    {"id": 8, "name": "哈尔滨市公安局松北分局", "type": "政府", "level": "县处级", "parent": "哈尔滨市公安局", "location": "松北区"},
]

positions = [
    # 肖彬
    {"person_id": 1, "org_id": 1, "title": "松北区委书记", "start_date": "", "end_date": "present", "rank": "正处级（高配正厅级）", "note": "同时兼任哈尔滨新区党工委书记"},
    {"person_id": 1, "org_id": 3, "title": "哈尔滨新区党工委书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 贺业方
    {"person_id": 2, "org_id": 2, "title": "松北区委副书记、政府区长", "start_date": "2026-01", "end_date": "present", "rank": "正厅级", "note": "2026年1月起任代理区长，后任区长"},
    {"person_id": 2, "org_id": 1, "title": "松北区委副书记", "start_date": "2026-01", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 4, "title": "哈尔滨新区党工委副书记、管委会主任", "start_date": "2026-01", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 5, "title": "自贸试验区哈尔滨片区党工委副书记", "start_date": "2026-01", "end_date": "present", "rank": "正厅级", "note": ""},
    # 董方
    {"person_id": 3, "org_id": 2, "title": "松北区委常委、政府副区长（常务）", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "分管常务工作"},
    {"person_id": 3, "org_id": 4, "title": "哈尔滨新区党工委委员、管委会副主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 陈方晔
    {"person_id": 4, "org_id": 2, "title": "松北区委常委、政府副区长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "哈尔滨新区党工委委员、管委会成员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 夏厦
    {"person_id": 5, "org_id": 2, "title": "松北区政府副区长（无党派）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "无党派人士"},
    # 苏志
    {"person_id": 6, "org_id": 2, "title": "松北区政府副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 刘辉
    {"person_id": 7, "org_id": 2, "title": "松北区政府副区长、党组成员", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼任区公安分局局长"},
    {"person_id": 7, "org_id": 8, "title": "松北区公安分局局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 葛红升
    {"person_id": 8, "org_id": 2, "title": "松北区政府副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 刘惟乔
    {"person_id": 9, "org_id": 2, "title": "松北区政府副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 黄明瑾
    {"person_id": 10, "org_id": 7, "title": "松北区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 赵琪
    {"person_id": 11, "org_id": 7, "title": "松北区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "曾担任五届五次人代会执行主席"},
    # 张建国
    {"person_id": 12, "org_id": 1, "title": "区委办公室负责人", "start_date": "", "end_date": "present", "rank": "", "note": "在领导调研新闻中作为陪同人员出现"},
]

relationships = [
    # 肖彬—贺业方：党政正职
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "党政正职搭档：区委书记与区长", "overlap_org": "松北区委/区政府", "overlap_period": "2026-01至今"},
    # 肖彬—董方：区委书记—常委副区长
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "区委书记与常务副区长", "overlap_org": "中共哈尔滨市松北区委员会", "overlap_period": ""},
    # 肖彬—陈方晔：区委书记—常委副区长
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "区委书记与常委副区长", "overlap_org": "中共哈尔滨市松北区委员会", "overlap_period": ""},
    # 肖彬—黄明瑾：区委—人大
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "区委书记与人常委会主任", "overlap_org": "松北区党政领导班子", "overlap_period": ""},
    # 贺业方—董方：区长—常务副区长
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "区长与常务副区长", "overlap_org": "哈尔滨市松北区人民政府", "overlap_period": "2026-01至今"},
    # 贺业方—陈方晔：区长—副区长
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "区长与副区长", "overlap_org": "哈尔滨市松北区人民政府", "overlap_period": "2026-01至今"},
    # 贺业方—刘辉：区长—副区长兼公安局长
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "区长与副区长/公安局长", "overlap_org": "哈尔滨市松北区人民政府", "overlap_period": "2026-01至今"},
    # 董方—陈方晔：同为区政府班子成员
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "区政府领导（常务副区长与副区长）", "overlap_org": "哈尔滨市松北区人民政府", "overlap_period": ""},
    # 董方—夏厦：区政府班子成员
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "区政府正副职", "overlap_org": "哈尔滨市松北区人民政府", "overlap_period": ""},
    # 董方—苏志：区政府班子成员
    {"person_a": 3, "person_b": 6, "type": "overlap", "context": "区政府正副职", "overlap_org": "哈尔滨市松北区人民政府", "overlap_period": ""},
    # 董方—刘辉：区政府班子成员
    {"person_a": 3, "person_b": 7, "type": "overlap", "context": "区政府正副职", "overlap_org": "哈尔滨市松北区人民政府", "overlap_period": ""},
    # 董方—葛红升：区政府班子成员
    {"person_a": 3, "person_b": 8, "type": "overlap", "context": "区政府正副职", "overlap_org": "哈尔滨市松北区人民政府", "overlap_period": ""},
    # 董方—刘惟乔：区政府班子成员
    {"person_a": 3, "person_b": 9, "type": "overlap", "context": "区政府正副职", "overlap_org": "哈尔滨市松北区人民政府", "overlap_period": ""},
]


# =========================================================================
# HELPER FUNCTIONS
# =========================================================================

def node_color(current_post):
    """Return RGB for person node based on role."""
    post = current_post or ""
    if "区委书记" in post or "党工委书记" in post:
        return {"r": 255, "g": 50, "b": 50, "a": 1.0}  # Red
    if "区长" in post and "副" not in post:
        return {"r": 50, "g": 100, "b": 255, "a": 1.0}  # Blue
    if "副区长" in post or "副主任" in post or "副局长" in post:
        return {"r": 50, "g": 100, "b": 255, "a": 1.0}  # Blue (deputy)
    if "主任" in post:
        return {"r": 50, "g": 180, "b": 100, "a": 1.0}  # Green (congress)
    return {"r": 100, "g": 100, "b": 100, "a": 1.0}  # Grey


def node_size(current_post):
    """Return size for person node."""
    post = current_post or ""
    if "区委书记" in post or "党工委书记" in post:
        return 20.0
    if "区长" in post and "副" not in post:
        return 18.0
    return 12.0


def node_shape(current_post):
    return "circle"


ORG_COLORS = {
    "党委": {"r": 255, "g": 200, "b": 200},
    "政府": {"r": 200, "g": 200, "b": 255},
    "人大": {"r": 200, "g": 255, "b": 255},
}
ORG_DEFAULT = {"r": 220, "g": 220, "b": 220}


# =========================================================================
# BUILD SQLITE
# =========================================================================

def build_db():
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    # Create tables
    c.executescript("""
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
        c.execute(
            "INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]),
        )

    # Insert organizations
    for o in organizations:
        c.execute(
            "INSERT INTO organizations VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]),
        )

    # Insert positions
    for pos in positions:
        c.execute(
            "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"],
             pos["end_date"], pos["rank"], pos["note"]),
        )

    # Insert relationships
    for r in relationships:
        c.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"], r["context"],
             r["overlap_org"], r["overlap_period"]),
        )

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")


# =========================================================================
# BUILD GEXF
# =========================================================================

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>松北区（哈尔滨市）领导班子关系网络</description>')
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

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = node_color(p["current_post"])
        sz = node_size(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        if p.get("gender"):
            lines.append(f'          <attvalue for="3" value="{esc(p["gender"])}"/>')
        if p.get("ethnicity"):
            lines.append(f'          <attvalue for="4" value="{esc(p["ethnicity"])}"/>')
        if p.get("birth"):
            lines.append(f'          <attvalue for="5" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="6" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c["r"]}" g="{c["g"]}" b="{c["b"]}" a="{c["a"]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'        <viz:shape value="circle"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oc = ORG_COLORS.get(o["type"], ORG_DEFAULT)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="7" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="8" value="{esc(o["level"])}"/>')
        lines.append(f'          <attvalue for="9" value="{esc(o["location"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc["r"]}" g="{oc["g"]}" b="{oc["b"]}" a="1.0"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('        <viz:shape value="diamond"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges: person->organization (worked_at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{pos["start_date"] or ""}"/>')
        lines.append(f'          <attvalue for="3" value="{pos["end_date"] or ""}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges: person<->person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")
    print(f"  Person nodes: {len(persons)}")
    print(f"  Org nodes: {len(organizations)}")
    print(f"  Edges: {eid}")


# =========================================================================
# MAIN
# =========================================================================

if __name__ == "__main__":
    build_db()
    build_gexf()
    print("Done.")
