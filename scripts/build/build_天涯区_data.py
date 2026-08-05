#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天涯区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 市辖区
Province: 海南省
Parent city: 三亚市
Region: 天涯区
Targets: 区委书记 & 区长

官方来源（截至2026-08-05）:
- http://ty.sanya.gov.cn/ — 三亚市天涯区人民政府门户网站
- https://search.sanya.gov.cn/ — 天涯区站内搜索
- https://baike.baidu.com/item/朱志兴 — 百度百科（义项确认）

当前在任 (as of 2026-08-05):
- 区委书记: 朱志兴（天涯区委书记、区人武部党委第一书记）
- 区长: 陈潇（女，1979年12月生，研究生、法学硕士；区委副书记、区政府党组书记、区长）
- 常务副区长: 符启川
- 副区长: 吴中华（挂职）、陈翊逵、曾宇、许和裕、钟庆红、胡首要、刘阳柳
- 区委常委、统战部部长: 罗有豪

注：区委书记朱志兴及区长陈潇的任职时间来自天涯区政府门户网站领导简介页与天涯区站内新闻；
部分领导（朱志兴）出生年月/籍贯/任前履历在公开渠道未找到完整信息，已在人物 JSON 与
report/open_gaps.md 中标注。数据遵循 source_fallbacks 的 partial-evidence artifact mode。
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

# 使脚本可从任意目录运行
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "天涯区"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

AS_OF = "2026-08-05"

# =========================================================================
# 1. PERSONS
# =========================================================================
# id 约定: 1=区委书记, 2=区长, 3-10=副区长, 11=统战部长, 12=谢香慧(区领导),
# 13=三亚市委书记, 14=三亚市长
persons = [
    # 核心: 区委书记
    {
        "id": 1,
        "name": "朱志兴",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三亚市天涯区委书记、区人武部党委第一书记",
        "current_org": "中共三亚市天涯区委员会",
        "source": "https://baike.baidu.com/item/朱志兴 + ty.sanya.gov.cn",
    },
    # 核心: 区长
    {
        "id": 2,
        "name": "陈潇",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1979-12",
        "birthplace": "待查",
        "education": "研究生，法学硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三亚市天涯区委副书记、区政府党组书记、区长",
        "current_org": "三亚市天涯区人民政府",
        "source": "http://ty.sanya.gov.cn/tyqsite/qzfld/202512/b481fbb1ab9a4318a091824fa06a5165.shtml",
    },
    # 副区长
    {
        "id": 3,
        "name": "符启川",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-07",
        "birthplace": "待查",
        "education": "大学，工学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三亚市天涯区委常委、区政府党组副书记、副区长",
        "current_org": "三亚市天涯区人民政府",
        "source": "http://ty.sanya.gov.cn/tyqsite/qzfld/202512/a20f05f866744acea1506119d4b8d208.shtml",
    },
    {
        "id": 4,
        "name": "吴中华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-01",
        "birthplace": "待查",
        "education": "在职工商管理硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三亚市天涯区委常委、区政府党组成员、副区长（挂职）",
        "current_org": "三亚市天涯区人民政府",
        "source": "http://ty.sanya.gov.cn/tyqsite/qzfld/202412/dbce8181f06843ea9a56bac569db1f37.shtml",
    },
    {
        "id": 5,
        "name": "陈翊逵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-10",
        "birthplace": "待查",
        "education": "大学，法学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三亚市天涯区人民政府副区长",
        "current_org": "三亚市天涯区人民政府",
        "source": "http://ty.sanya.gov.cn/tyqsite/qzfld/202512/dccc011614fc4c02a791f2d2ed11b2db.shtml",
    },
    {
        "id": 6,
        "name": "曾宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-10",
        "birthplace": "待查",
        "education": "本科，理学学士",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "三亚市天涯区人民政府副区长",
        "current_org": "三亚市天涯区人民政府",
        "source": "http://ty.sanya.gov.cn/tyqsite/qzfld/202512/2545e5c207bc44419a5ccae34d910a42.shtml",
    },
    {
        "id": 7,
        "name": "许和裕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-04",
        "birthplace": "待查",
        "education": "大学，法学专业",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三亚市天涯区人民政府党组成员、副区长",
        "current_org": "三亚市天涯区人民政府",
        "source": "http://ty.sanya.gov.cn/tyqsite/qzfld/202512/7feed46b3ca34bf699391c667fbd70ac.shtml",
    },
    {
        "id": 8,
        "name": "钟庆红",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976-04",
        "birthplace": "待查",
        "education": "大学本科",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "三亚市天涯区人民政府党组成员、副区长",
        "current_org": "三亚市天涯区人民政府",
        "source": "http://ty.sanya.gov.cn/tyqsite/qzfld/202607/883f8540939a4c37804937f7e024bf25.shtml",
    },
    {
        "id": 9,
        "name": "胡首要",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-12",
        "birthplace": "待查",
        "education": "大学，农学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三亚市天涯区人民政府党组成员、副区长",
        "current_org": "三亚市天涯区人民政府",
        "source": "http://ty.sanya.gov.cn/tyqsite/qzfld/202403/51a1df3b8c3f46bfad3ff4fa5ad50bbd.shtml",
    },
    {
        "id": 10,
        "name": "刘阳柳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-01",
        "birthplace": "待查",
        "education": "大学，法学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三亚市天涯区人民政府党组成员、副区长",
        "current_org": "三亚市天涯区人民政府",
        "source": "http://ty.sanya.gov.cn/tyqsite/qzfld/202403/6a489961e79d4dbd41a9bac869df20.shtml",
    },
    # 区委常委、统战部长
    {
        "id": 11,
        "name": "罗有豪",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三亚市天涯区委常委、统战部部长",
        "current_org": "中共三亚市天涯区委员会",
        "source": "https://search.sanya.gov.cn（天涯区2025-03-04新闻：书记拜访省委统战部）",
    },
    # 区领导（会场上座）
    {
        "id": 12,
        "name": "谢香慧",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "天涯区领导（具体岗位待核）",
        "current_org": "三亚市天涯区（区级机关）",
        "source": "https://search.sanya.gov.cn（2025-09-30区委书记点评会）",
    },
    # 三亚市级（上级）
    {
        "id": 13,
        "name": "王祺扬",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "海南省委常委、三亚市委书记",
        "current_org": "中共三亚市委员会",
        "source": "scripts/build/build_三亚市_data.py",
    },
    {
        "id": 14,
        "name": "陈希",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "三亚市委副书记、市长",
        "current_org": "三亚市人民政府",
        "source": "scripts/build/build_三亚市_data.py",
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共三亚市天涯区委员会", "type": "党委", "level": "市辖区", "parent": "中国共产党三亚市委员会", "location": "海南省三亚市天涯区"},
    {"id": 2, "name": "三亚市天涯区人民政府", "type": "政府", "level": "市辖区", "parent": "三亚市人民政府", "location": "海南省三亚市天涯区"},
    {"id": 3, "name": "中共三亚市委员会", "type": "党委", "level": "地级市", "parent": "中国共产党海南省委员会", "location": "海南省三亚市"},
    {"id": 4, "name": "三亚市人民政府", "type": "政府", "level": "地级市", "parent": "海南省人民政府", "location": "海南省三亚市"},
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 朱志兴 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "天涯区委书记", "start_date": "2024", "end_date": "present", "rank": "县处级/副厅级", "note": "兼区人武部党委第一书记；2024年度即任，持续在任至2026"},
    # 陈潇 — 区长（自2022前）
    {"person_id": 2, "org_id": 2, "title": "天涯区区长／区政府党组书记", "start_date": "2022-02前", "end_date": "present", "rank": "正处级", "note": "区委副书记、政府党组书记、区长"},
    {"person_id": 2, "org_id": 1, "title": "天涯区委副书记", "start_date": "2022-02前", "end_date": "present", "rank": "副处级/正处级", "note": "区委副书记、区长"},
    # 副区长
    {"person_id": 3, "org_id": 2, "title": "常务副区长（区委常委、政府党组副书记）", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副区长（挂职）", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "区委常委，挂职"},
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 统战部长
    {"person_id": 11, "org_id": 1, "title": "区委常委、统战部部长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 谢香慧
    {"person_id": 12, "org_id": 1, "title": "区领导（岗位待核）", "start_date": "待查", "end_date": "present", "rank": "待查", "note": "可能为区政协/人大或常委"},
    # 上级
    {"person_id": 13, "org_id": 3, "title": "海南省委常委、三亚市委书记", "start_date": "待查", "end_date": "present", "rank": "副部级", "note": ""},
    {"person_id": 14, "org_id": 4, "title": "三亚市委副书记、市长", "start_date": "待查", "end_date": "present", "rank": "正厅级", "note": ""},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 党政搭档 (strong, confirmed)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "区委书记与区长党政一把手搭档关系", "overlap_org": "中共三亚市天涯区委员会/三亚市天涯区人民政府", "overlap_period": "2024-2026"},
    # 区委书记 ↔ 区政府班子 (superior_subordinate, confirmed 行政隶属)
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区委书记辖区政府常务副区长", "overlap_org": "中共三亚市天涯区委员会/三亚市天涯区人民政府", "overlap_period": "2024-2026"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "区长与常务副区长区政府班子搭档", "overlap_org": "三亚市天涯区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "区长与副区长（挂职）政府班子", "overlap_org": "三亚市天涯区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "区长与副区长政府班子", "overlap_org": "三亚市天涯区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "区长与副区长政府班子", "overlap_org": "三亚市天涯区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "区长与副区长政府班子", "overlap_org": "三亚市天涯区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "区长与副区长政府班子", "overlap_org": "三亚市天涯区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "区长与副区长政府班子", "overlap_org": "三亚市天涯区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "区长与副区长政府班子", "overlap_org": "三亚市天涯区人民政府", "overlap_period": "2026"},
    # 区委常委会 (medium, plausible)
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "区委书记与常委统战部长同属区委常委会班子", "overlap_org": "中共三亚市天涯区委员会", "overlap_period": "2024-2026"},
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "区领导在区委常委会（扩大）会议按程序出席", "overlap_org": "中共三亚市天涯区委员会", "overlap_period": "2025-2026"},
    # 上级-下级 (superior_subordinate, confirmed)
    {"person_a": 13, "person_b": 1, "type": "superior_subordinate", "context": "三亚市委书记辖天涯区委书记", "overlap_org": "中共三亚市委员会/中共三亚市天涯区委员会", "overlap_period": "2024-2026"},
    {"person_a": 14, "person_b": 2, "type": "superior_subordinate", "context": "三亚市长辖天涯区长", "overlap_org": "三亚市人民政府/三亚市天涯区人民政府", "overlap_period": "2022-2026"},
]

# =========================================================================
# 5. BUILD DATABASE
# =========================================================================
def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript(
        """
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
        """
    )
    for p in persons:
        cur.execute(
            """INSERT INTO persons
               (id,name,gender,ethnicity,birth,birthplace,education,party_join,
                work_start,current_post,current_org,source)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
             p["education"], p["party_join"], p["work_start"], p["current_post"],
             p["current_org"], p["source"]),
        )
    for o in organizations:
        cur.execute(
            "INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]),
        )
    for pos in positions:
        cur.execute(
            """INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note)
               VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"],
             pos["end_date"], pos["rank"], pos["note"]),
        )
    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]),
        )
    conn.commit()
    conn.close()


# =========================================================================
# 6. BUILD GEXF
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    # 书记=红, 政府领导(区长/副区长)=蓝, 其他=灰
    if "书记" in p["current_post"] or "书记" in p.get("name", ""):
        return "255,71,71"
    if "区长" in p["current_post"] or "副区长" in p["current_post"] or "市长" in p["current_post"]:
        return "50,100,255"
    if "纪委" in p["current_post"] or "监委" in p["current_post"]:
        return "255,165,0"
    return "120,120,120"


def org_color(o):
    t = o["type"]
    if t == "党委":
        return "255,200,200"
    if t == "政府":
        return "200,200,255"
    return "200,200,200"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>海南省三亚市天涯区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    # node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="name" type="string"/>')
    lines.append('      <attribute id="2" title="current_post" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')
    # edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        rg, g, b = c.split(",")
        is_leader = p["id"] in (1, 2)
        sz = "20.0" if is_leader else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["name"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{rg}" g="{g}" b="{b}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c = org_color(o)
        rg, g, b = c.split(",")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["name"])}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('          <attvalue for="4" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{rg}" g="{g}" b="{b}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    # person->org: worked_at
    for pos in positions:
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}"'
                     f' label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"] or "")}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos["start_date"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    # person<->person: relationship (weight 2.0)
    strong = {"overlap", "superior_subordinate"}
    for r in relationships:
        w = "2.0" if r["type"] in strong else "1.0"
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}"'
                     f' label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# =========================================================================
if __name__ == "__main__":
    build_db()
    build_gexf()
    print("OK: 天涯区 build complete")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")