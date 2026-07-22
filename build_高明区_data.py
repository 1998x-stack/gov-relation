#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高明区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 佛山市
Region: 高明区
Targets: 区委书记 & 区长

Research Sources:
- zh.wikipedia.org/wiki/高明区 — 确认区委书记姜岳新 (2026-07-15更新)
- www.gaoming.gov.cn/zwgk/ldcy/ — 区政府领导名单 (2026-07访问)
- www.gaoming.gov.cn/zwgk/ldcy/qzf/qz/content/post_5873518.html — 唐磊晶简历
- www.gaoming.gov.cn/zwgk/ldcy/qzf/fqz/ — 副区长简历页面
- 金湾区构建脚本/报告 — 梁耀斌曾任高明区区长，后调任珠海金湾区委书记
- www.gaoming.gov.cn/zwgk/zwdt/ — 新闻确认姜岳新任区委书记 (2026-07-10活动报道)

Research Date: 2026-07-22

网络环境限制说明:
- Exa搜索达到速率限制
- Baidu/So.com搜索被验证码拦截
- Wikipedia/澎湃/搜狐等搜索超时或不可达
- Jina Reader超时
- gaoming.gov.cn区委领导名单通过JS动态渲染，静态HTML不可获取
- 基于政府网站公开页面确认区长和副区长简历，Wikipedia确认区委书记
"""

import os
import sys
from datetime import datetime

# ── Paths ──
BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "data/database/高明区_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/高明区_network.gexf")

import sqlite3

# ════════════════════════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════════════════════════

persons = [
    # ── 1. Current Top Leaders ──
    {
        "id": 1,
        "name": "姜岳新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "佛山市高明区委书记",
        "current_org": "中共佛山市高明区委员会",
        "source": "zh.wikipedia.org/wiki/高明区 — 区委书记姜岳新 (2026-07-15更新); www.gaoming.gov.cn — 新闻'姜岳新率队实地督导检查防汛工作'(2026-07-10)"
    },
    {
        "id": 2,
        "name": "唐磊晶",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1979-02",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学，法学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "佛山市高明区委副书记、区长",
        "current_org": "佛山市高明区人民政府",
        "source": "www.gaoming.gov.cn/zwgk/ldcy/qzf/qz/content/post_5873518.html — 唐磊晶官方简历"
    },
    # ── 2. District Government Leaders (副区长) ──
    {
        "id": 3,
        "name": "王志容",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-12",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学，农业推广硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "佛山市高明区委常委、副区长（常务）",
        "current_org": "佛山市高明区人民政府",
        "source": "www.gaoming.gov.cn/zwgk/ldcy/qzf/fqz/content/post_5950881.html — 王志容官方简历"
    },
    {
        "id": 4,
        "name": "朱立坚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-05",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学，文学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "佛山市高明区委常委、副区长",
        "current_org": "佛山市高明区人民政府",
        "source": "www.gaoming.gov.cn/zwgk/ldcy/qzf/fqz/content/post_5056857.html — 朱立坚官方简历"
    },
    {
        "id": 5,
        "name": "骆康",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-11",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "省委党校大专",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "高明区副区长、公安分局局长",
        "current_org": "佛山市公安局高明分局",
        "source": "www.gaoming.gov.cn/zwgk/ldcy/qzf/fqz/content/post_5350978.html — 骆康官方简历"
    },
    {
        "id": 6,
        "name": "黄友谊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-07",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "高明区副区长",
        "current_org": "佛山市高明区人民政府",
        "source": "www.gaoming.gov.cn/zwgk/ldcy/qzf/fqz/content/post_5056854.html — 黄友谊官方简历"
    },
    {
        "id": 7,
        "name": "陈妍妍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981-09",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学，经济学学士",
        "party_join": "民革党员",
        "work_start": "待查",
        "current_post": "高明区副区长",
        "current_org": "佛山市高明区人民政府",
        "source": "www.gaoming.gov.cn/zwgk/ldcy/qzf/fqz/content/post_5360457.html — 陈妍妍官方简历"
    },
    {
        "id": 8,
        "name": "谭桂清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-01",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "省委党校大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "高明区副区长",
        "current_org": "佛山市高明区人民政府",
        "source": "www.gaoming.gov.cn/zwgk/ldcy/qzf/fqz/content/post_5407171.html — 谭桂清官方简历"
    },
    {
        "id": 9,
        "name": "陈伟光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-09",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "省委党校大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "高明区副区长",
        "current_org": "佛山市高明区人民政府",
        "source": "www.gaoming.gov.cn/zwgk/ldcy/qzf/fqz/content/post_5974956.html — 陈伟光官方简历"
    },
    {
        "id": 10,
        "name": "于长灏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1990-09",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "省委党校研究生，工学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "高明区副区长（挂职）",
        "current_org": "佛山市高明区人民政府",
        "source": "www.gaoming.gov.cn/zwgk/ldcy/qzf/fqz/content/post_7117670.html — 于长灏官方简历"
    },
    # ── 3. Predecessors ──
    {
        "id": 11,
        "name": "梁耀斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "珠海市金湾区委书记",
        "current_org": "中共珠海市金湾区委员会",
        "source": "金湾区构建脚本 — 梁耀斌曾任高明区区长; 金湾区调查报告确认跨市调任"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共佛山市高明区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共佛山市委",
        "location": "佛山市高明区"
    },
    {
        "id": 2,
        "name": "佛山市高明区人民政府",
        "type": "政府",
        "level": "市辖区",
        "parent": "佛山市人民政府",
        "location": "佛山市高明区"
    },
    {
        "id": 3,
        "name": "佛山市公安局高明分局",
        "type": "政府",
        "level": "市辖区",
        "parent": "佛山市公安局",
        "location": "佛山市高明区"
    },
    {
        "id": 4,
        "name": "荷城街道办事处",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "高明区人民政府",
        "location": "佛山市高明区"
    },
    {
        "id": 5,
        "name": "杨和镇人民政府",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "高明区人民政府",
        "location": "佛山市高明区"
    },
    {
        "id": 6,
        "name": "明城镇人民政府",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "高明区人民政府",
        "location": "佛山市高明区"
    },
    {
        "id": 7,
        "name": "更合镇人民政府",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "高明区人民政府",
        "location": "佛山市高明区"
    },
]

positions = [
    # 姜岳新 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "佛山市高明区委书记", "start": "待查", "end": "至今", "rank": "正处级", "note": "当前区委书记"},
    # 唐磊晶 — 区长
    {"person_id": 2, "org_id": 2, "title": "佛山市高明区区长", "start": "待查", "end": "至今", "rank": "正处级", "note": "区委副书记、区长、党组书记"},
    {"person_id": 2, "org_id": 1, "title": "高明区委副书记", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 王志容 — 常务副区长
    {"person_id": 3, "org_id": 2, "title": "高明区委常委、常务副区长", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "高明区委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 朱立坚 — 副区长
    {"person_id": 4, "org_id": 2, "title": "高明区委常委、副区长", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "高明区委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 骆康 — 副区长、公安局长
    {"person_id": 5, "org_id": 2, "title": "高明区副区长", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "高明公安分局局长", "start": "待查", "end": "至今", "rank": "副处级", "note": "区委政法委第一副书记"},
    # 黄友谊 — 副区长
    {"person_id": 6, "org_id": 2, "title": "高明区副区长", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 陈妍妍 — 副区长
    {"person_id": 7, "org_id": 2, "title": "高明区副区长", "start": "待查", "end": "至今", "rank": "副处级", "note": "民革党员"},
    # 谭桂清 — 副区长
    {"person_id": 8, "org_id": 2, "title": "高明区副区长", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 陈伟光 — 副区长
    {"person_id": 9, "org_id": 2, "title": "高明区副区长", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 于长灏 — 挂职副区长
    {"person_id": 10, "org_id": 2, "title": "高明区副区长（挂职）", "start": "待查", "end": "至今", "rank": "副处级", "note": "挂职"},
    # 梁耀斌 — 前任高明区长
    {"person_id": 11, "org_id": 1, "title": "高明区委副书记", "start": "待查", "end": "待查", "rank": "副处级", "note": "曾任高明区区长，后调任珠海金湾"},
    {"person_id": 11, "org_id": 2, "title": "高明区区长", "start": "待查", "end": "待查", "rank": "正处级", "note": "前任区长，现为金湾区委书记"},
]

relationships = [
    # 区委书记 ↔ 区长 — 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "区委书记与区长，党政正职搭档关系",
     "overlap_org": "高明区", "overlap_period": "当前"},
    # 区委书记 ↔ 区委常委/常务副区长
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "区委书记与区委常委（常务副区长）",
     "overlap_org": "中共高明区委", "overlap_period": "当前"},
    # 区委书记 ↔ 区委常委/副区长
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "区委书记与区委常委（副区长）",
     "overlap_org": "中共高明区委", "overlap_period": "当前"},
    # 区长 ↔ 副区长们
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "区长与常务副区长",
     "overlap_org": "高明区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "区长与副区长",
     "overlap_org": "高明区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "区长与副区长兼公安分局局长",
     "overlap_org": "高明区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "区长与副区长",
     "overlap_org": "高明区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "区长与副区长",
     "overlap_org": "高明区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "区长与副区长",
     "overlap_org": "高明区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "区长与副区长",
     "overlap_org": "高明区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "区长与挂职副区长",
     "overlap_org": "高明区人民政府", "overlap_period": "当前"},
    # 梁耀斌 — 前任区长与现任区长的关系（继任者）
    {"person_a": 11, "person_b": 2, "type": "predecessor_successor",
     "context": "梁耀斌前任高明区长，唐磊晶现任高明区长",
     "overlap_org": "高明区人民政府", "overlap_period": "继任"},
    # 王志容（常委/常务副区长）↔ 朱立坚（常委/副区长）
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "同为高明区委常委",
     "overlap_org": "中共高明区委", "overlap_period": "当前（同为常委）"},
]


# ════════════════════════════════════════════════════════════════
# DATABASE
# ════════════════════════════════════════════════════════════════

def create_tables(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            native_place TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS positions (
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
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        )
    """)


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return 'r,g,b' string based on role."""
    post = p.get("current_post", "")
    name = p.get("name", "")
    if "书记" in post and "区委书记" in post:
        return "255,50,50"
    if "区长" in post:
        return "50,100,255"
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"
    return "100,100,100"


def is_top_leader(p):
    post = p.get("current_post", "")
    return "书记" in post or "区长" in post


def build_gexf(persons, orgs, positions, rels, output_path):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append('    <description>高明区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="gender" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')
    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')
    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        role = p.get("current_post", "")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("gender",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # Nodes: organizations
    for o in orgs:
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    # Person ↔ Person (relationships)
    for r in rels:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════

def main():
    # Build database
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)
    for p in persons:
        conn.execute(
            "INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,native_place,education,party_join,work_start,current_post,current_org,source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
             p["native_place"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"])
        )
    for o in organizations:
        conn.execute(
            "INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
        )
    for pos in positions:
        conn.execute(
            "INSERT INTO positions (person_id,org_id,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"])
        )
    for r in relationships:
        conn.execute(
            "INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
        )
    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")
    print(f"   - {len(persons)} persons")
    print(f"   - {len(organizations)} organizations")
    print(f"   - {len(positions)} positions")
    print(f"   - {len(relationships)} relationships")

    # Build GEXF
    build_gexf(persons, organizations, positions, relationships, GEXF_PATH)
    print(f"✅ GEXF created: {GEXF_PATH}")

    print("\nDone.")


if __name__ == "__main__":
    main()
