#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
那坡县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 广西壮族自治区
Parent City: 百色市
Region: 那坡县
Targets: 县委书记 & 县长

当前在任 (as of 2026-07-23):
- 县委书记: 黄台勇 (那坡县委书记)
- 县长: 罗智郎 (那坡县委副书记、县长、县政府党组书记)

数据来源: 那坡县人民政府官方网站 http://www.napo.gov.cn/
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "那坡县"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-23"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：县委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "黄台勇",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "那坡县委书记",
        "current_org": "中共那坡县委员会",
        "source": "http://www.napo.gov.cn/npyw/zwyw/t27904683.shtml"
    },
    # ════════════════════════════════════════
    # 核心领导：县长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "罗智郎",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "那坡县委副书记、县长、县政府党组书记",
        "current_org": "那坡县人民政府/中共那坡县委员会",
        "source": "http://www.napo.gov.cn/zfxxgkzl/zcwj/xianbenjiwenjian/nzf/t27261230.shtml"
    },
    # ════════════════════════════════════════
    # 县人大常委会主任
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "闭鸿飞",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "那坡县人大常委会主任",
        "current_org": "那坡县人民代表大会常务委员会",
        "source": "http://www.napo.gov.cn/npyw/zwyw/t27802528.shtml"
    },
    # ════════════════════════════════════════
    # 县政协主席
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "马方",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "那坡县政协主席",
        "current_org": "中国人民政治协商会议那坡县委员会",
        "source": "http://www.napo.gov.cn/npyw/zwyw/t27802528.shtml"
    },
    # ════════════════════════════════════════
    # 常务副县长
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "李常政",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "那坡县委常委、常务副县长",
        "current_org": "中共那坡县委员会/那坡县人民政府",
        "source": "http://www.napo.gov.cn/zfxxgkzl/zcwj/xianbenjiwenjian/nzf/t27261230.shtml"
    },
    # ════════════════════════════════════════
    # 副县长（深圳对口帮扶）
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "孔令斌",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "那坡县副县长",
        "current_org": "那坡县人民政府",
        "source": "http://www.napo.gov.cn/zfxxgkzl/zcwj/xianbenjiwenjian/nzf/t27261230.shtml"
    },
    # ════════════════════════════════════════
    # 副县长（驻村工作队）
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "崔屹",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "那坡县副县长",
        "current_org": "那坡县人民政府",
        "source": "http://www.napo.gov.cn/zfxxgkzl/zcwj/xianbenjiwenjian/nzf/t27261230.shtml"
    },
    # ════════════════════════════════════════
    # 副县长（中车集团定点帮扶）
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "易湘戈",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "那坡县副县长",
        "current_org": "那坡县人民政府",
        "source": "http://www.napo.gov.cn/zfxxgkzl/zcwj/xianbenjiwenjian/nzf/t27261230.shtml"
    },
    # ════════════════════════════════════════
    # 副县长（挂职）
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "刘涛",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "那坡县副县长（挂职）",
        "current_org": "那坡县人民政府",
        "source": "http://www.napo.gov.cn/zfxxgkzl/zcwj/xianbenjiwenjian/nzf/t27261230.shtml"
    },
    # ════════════════════════════════════════
    # 副县长（工业、交通等）
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "李文清",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "那坡县副县长",
        "current_org": "那坡县人民政府",
        "source": "http://www.napo.gov.cn/zfxxgkzl/zcwj/xianbenjiwenjian/nzf/t27261230.shtml"
    },
    # ════════════════════════════════════════
    # 副县长（农业农村等）
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "梁俊仕",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "那坡县副县长",
        "current_org": "那坡县人民政府",
        "source": "http://www.napo.gov.cn/zfxxgkzl/zcwj/xianbenjiwenjian/nzf/t27261230.shtml"
    },
    # ════════════════════════════════════════
    # 副县长（公安、司法）
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "岑启先",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "那坡县副县长、县公安局局长",
        "current_org": "那坡县人民政府/那坡县公安局",
        "source": "http://www.napo.gov.cn/zfxxgkzl/zcwj/xianbenjiwenjian/nzf/t27261230.shtml"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共那坡县委员会", "type": "党委", "level": "县", "parent": "中共百色市委员会", "location": "广西百色市那坡县"},
    {"id": 2, "name": "那坡县人民政府", "type": "政府", "level": "县", "parent": "百色市人民政府", "location": "广西百色市那坡县"},
    {"id": 3, "name": "那坡县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "", "location": "广西百色市那坡县"},
    {"id": 4, "name": "中国人民政治协商会议那坡县委员会", "type": "政协", "level": "县", "parent": "", "location": "广西百色市那坡县"},
    {"id": 5, "name": "那坡县公安局", "type": "政府", "level": "县", "parent": "那坡县人民政府", "location": "广西百色市那坡县"},
    {"id": 6, "name": "那坡县深百协作办公室", "type": "政府", "level": "县", "parent": "那坡县人民政府", "location": "广西百色市那坡县"},
    {"id": 7, "name": "那坡县驻村工作队管理办公室", "type": "政府", "level": "县", "parent": "那坡县人民政府", "location": "广西百色市那坡县"},
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 黄台勇 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "那坡县委书记", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
    # 罗智郎 - 县委副书记、县长
    {"person_id": 2, "org_id": 1, "title": "那坡县委副书记", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "那坡县长、县政府党组书记", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "县政府全面工作，主管财政、审计"},
    # 闭鸿飞 - 县人大常委会主任
    {"person_id": 3, "org_id": 3, "title": "那坡县人大常委会主任", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
    # 马方 - 县政协主席
    {"person_id": 4, "org_id": 4, "title": "那坡县政协主席", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
    # 李常政 - 县委常委、常务副县长
    {"person_id": 5, "org_id": 1, "title": "那坡县委常委", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "那坡县常务副县长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "分管发改、应急、人社、统计、金融、沿边开发开放等"},
    # 孔令斌 - 副县长（深圳对口帮扶）
    {"person_id": 6, "org_id": 2, "title": "那坡县副县长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "负责深圳对口帮扶协作，分管深百协作办公室"},
    # 崔屹 - 副县长（驻村工作队）
    {"person_id": 7, "org_id": 2, "title": "那坡县副县长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "负责驻村工作队，分管驻村工作队管理办公室"},
    # 易湘戈 - 副县长（中车集团定点帮扶）
    {"person_id": 8, "org_id": 2, "title": "那坡县副县长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "负责中车集团定点帮扶那坡方面工作"},
    # 刘涛 - 副县长（挂职）
    {"person_id": 9, "org_id": 2, "title": "那坡县副县长（挂职）", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "广东省深圳市龙岗区挂职"},
    # 李文清 - 副县长
    {"person_id": 10, "org_id": 2, "title": "那坡县副县长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "分管工业、交通、市场监管、商务、自然资源、住建等"},
    # 梁俊仕 - 副县长
    {"person_id": 11, "org_id": 2, "title": "那坡县副县长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "分管农业农村、林业、水利、文体广电旅游、教育、卫健等"},
    # 岑启先 - 副县长、县公安局局长
    {"person_id": 12, "org_id": 2, "title": "那坡县副县长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 5, "title": "那坡县公安局局长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "负责公安、司法、信访、维稳"},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 党政主要领导
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "黄台勇（县委书记）与罗智郎（县长）为那坡县党政主要搭档", "overlap_org": "那坡县党政班子", "overlap_period": ""},
    # 县委书记与县委常委
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "黄台勇（县委书记）与李常政（县委常委、常务副县长）为县委班子领导关系", "overlap_org": "中共那坡县委员会", "overlap_period": ""},
    # 县长与副县长
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "罗智郎（县长）与李常政（常务副县长）为县政府班子领导关系", "overlap_org": "那坡县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "罗智郎（县长）与孔令斌（副县长）为县政府班子领导关系", "overlap_org": "那坡县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "罗智郎（县长）与崔屹（副县长）为县政府班子领导关系", "overlap_org": "那坡县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "罗智郎（县长）与易湘戈（副县长）为县政府班子领导关系", "overlap_org": "那坡县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "罗智郎（县长）与刘涛（挂职副县长）为县政府班子领导关系", "overlap_org": "那坡县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "罗智郎（县长）与李文清（副县长）为县政府班子领导关系", "overlap_org": "那坡县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "罗智郎（县长）与梁俊仕（副县长）为县政府班子领导关系", "overlap_org": "那坡县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "罗智郎（县长）与岑启先（副县长、县公安局局长）为县政府班子领导关系", "overlap_org": "那坡县人民政府", "overlap_period": ""},
    # 人大主任与县长
    {"person_a": 2, "person_b": 3, "type": "党政关系", "context": "罗智郎（县长）与闭鸿飞（县人大主任）为县人大-政府工作关系", "overlap_org": "那坡县县四家班子", "overlap_period": ""},
    # 政协主席与县委书记
    {"person_a": 1, "person_b": 4, "type": "党政关系", "context": "黄台勇（县委书记）与马方（县政协主席）为县委-政协工作关系", "overlap_org": "那坡县县四家班子", "overlap_period": ""},
]


# =========================================================================
# 5. HELPERS
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(current_post):
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp and "纪委书记" not in cp:
        return "200,30,30"
    if "县长" in cp and "副" not in cp:
        return "30,100,200"
    if "副书记" in cp:
        return "220,80,80"
    if "纪委" in cp:
        return "255,165,0"
    if "副" in cp:
        return "100,150,220"
    if "常委" in cp:
        return "180,100,180"
    if "主任" in cp or "人大" in cp:
        return "60,180,60"
    if "主席" in cp or "政协" in cp:
        return "60,180,60"
    return "100,100,100"


def person_size(current_post):
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp and "纪委书记" not in cp:
        return "20.0"
    if "县长" in cp and "副" not in cp:
        return "18.0"
    if "副书记" in cp:
        return "15.0"
    if "副" in cp:
        return "12.0"
    if "常委" in cp:
        return "12.0"
    if "主任" in cp or "主席" in cp:
        return "12.0"
    return "10.0"


def person_shape(current_post):
    cp = current_post or ""
    if "书记" in cp and "纪委书记" not in cp:
        return "square"
    if "人大" in cp or "政协" in cp:
        return "diamond"
    if "副" in cp:
        return "triangle"
    return "circle"


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "开发区": "200,255,200",
        "纪委": "255,200,150",
    }
    return colors.get(org_type, "200,200,200")


def _infer_rank(post):
    if not post:
        return ""
    if "书记" in post and "副书记" not in post and "副" not in post.replace("副书记", ""):
        return "正处级"
    if "县长" in post and "副" not in post:
        return "正处级"
    if "主任" in post and "副" not in post:
        return "正处级"
    if "主席" in post and "副" not in post:
        return "正处级"
    if "副" in post:
        return "副处级"
    return ""


# =========================================================================
# 6. BUILD FUNCTIONS
# =========================================================================

def build_db():
    """Build SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
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
    """)

    for p in persons:
        cur.execute("""INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) 
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"], pos.get("start_date", ""), pos.get("end_date", ""),
                     pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"], r["context"], r.get("overlap_org", ""),
                     r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


def build_gexf():
    """Build GEXF graph file."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>那坡县领导班子关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes — persons
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        post = p.get("current_post", "")
        c = person_color(post)
        sz = person_size(post)
        sh = person_shape(post)

        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'        <viz:shape value="{sh}"/>')
        lines.append('      </node>')

    # Nodes — organizations
    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o.get("type", ""))
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append(f'        <viz:shape value="hexagon"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(
            f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"] + 100000}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ person (relationships)
    for r in relationships:
        eid += 1
        lines.append(
            f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")


def build_person_json(person, timeline, rels, sources):
    """Build a person graph JSON following the person_graph_json schema."""
    slug = f"napo_{person['name']}"

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "百色市",
            "region": "那坡县",
            "job": person.get("current_post", ""),
            "task_id": "guangxi_那坡县",
            "time_focus": "2026-07"
        },
        "identity": {
            "person_id": slug,
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth','')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace','')}",
                "official_profile_url": person.get("source", "")
            }
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": _infer_rank(person.get("current_post", "")),
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": rels,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "",
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
                "description": "No integrity risk signals found in initial search",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": sources,
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"个人基本信息（出生年月、籍贯、教育背景）不完整。{person['name']}的完整履历需进一步调查。"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的出生年月和籍贯是什么？",
                "why_it_matters": "个人基本信息是身份识别的核心字段",
                "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 百度百科"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"{person['name']}的教育背景是什么？",
                "why_it_matters": "学缘关系是构建关系网络的重要维度",
                "suggested_queries": [f"{person['name']} 学历"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"{person['name']}的完整任职履历是怎样的？此前任何职？",
                "why_it_matters": "前序任职是构建继任关系和跨地区调任证据的关键",
                "suggested_queries": [f"{person['name']} 曾任", f"{person['name']} 调任"],
                "last_attempted": AS_OF
            }
        ]
    }


def build_all_person_jsons():
    """Build and write individual person JSON files for the two core leaders."""

    # ── 黄台勇 (limited data from official website) ──
    timeline_huang = [
        {
            "start": "未知",
            "end": "未知",
            "org": "中共那坡县委员会",
            "title": "那坡县委书记",
            "level": "正处级",
            "location": "广西百色市那坡县",
            "system": "party",
            "rank": "正处级",
            "is_key_promotion": True,
            "notes": "2026年7月16日以县委书记身份主持县委常委会第103次会议",
            "confidence": "confirmed",
            "source_ids": ["S001"]
        }
    ]
    rels_huang = [
        {"person": "罗智郎", "person_id": "napo_luozhilang", "relationship_type": "superior_subordinate",
         "strength": "strong", "evidence": "那坡县党政主要领导搭档",
         "overlap_org": "那坡县党政班子", "overlap_period": "", "direction": "person_to_other",
         "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"person": "李常政", "person_id": "napo_lichangzheng", "relationship_type": "superior_subordinate",
         "strength": "medium", "evidence": "县委常委班子",
         "overlap_org": "中共那坡县委员会", "overlap_period": "", "direction": "person_to_other",
         "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    sources_huang = [
        {"id": "S001", "title": "中共那坡县委十五届常委会第103次会议召开", "url": "http://www.napo.gov.cn/npyw/zwyw/t27904683.shtml",
         "publisher": "那坡县融媒体中心", "published_at": "2026-07-17", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "确认县委书记黄台勇现任身份"},
        {"id": "S002", "title": "那坡县人民政府关于县人民政府领导同志工作分工调整的通知（那政发〔2026〕2号）",
         "url": "http://www.napo.gov.cn/zfxxgkzl/zcwj/xianbenjiwenjian/nzf/t27261230.shtml",
         "publisher": "那坡县人民政府", "published_at": "2026-02-11", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "确认县政府领导班子成员及分工"},
    ]

    person_huang = build_person_json(
        [p for p in persons if p["name"] == "黄台勇"][0],
        timeline_huang,
        rels_huang,
        sources_huang
    )

    # ── 罗智郎 (limited data) ──
    timeline_luo = [
        {
            "start": "未知",
            "end": "未知",
            "org": "那坡县人民政府/中共那坡县委员会",
            "title": "那坡县委副书记、县长、县政府党组书记",
            "level": "正处级",
            "location": "广西百色市那坡县",
            "system": "government",
            "rank": "正处级",
            "is_key_promotion": True,
            "notes": "2026年2月11日那政发〔2026〕2号确认县长身份；2026年6月17日以县委副书记、县长身份参加县委常委会",
            "confidence": "confirmed",
            "source_ids": ["S001", "S002"]
        }
    ]
    rels_luo = [
        {"person": "黄台勇", "person_id": "napo_huangtaiyong", "relationship_type": "superior_subordinate",
         "strength": "strong", "evidence": "那坡县党政主要领导搭档",
         "overlap_org": "那坡县党政班子", "overlap_period": "", "direction": "other_to_person",
         "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"person": "李常政", "person_id": "napo_lichangzheng", "relationship_type": "superior_subordinate",
         "strength": "medium", "evidence": "县政府班子",
         "overlap_org": "那坡县人民政府", "overlap_period": "", "direction": "person_to_other",
         "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    sources_luo = [
        {"id": "S001", "title": "中共那坡县委十五届常委会第九十九次会议召开", "url": "http://www.napo.gov.cn/npyw/zwyw/t27802528.shtml",
         "publisher": "那坡县融媒体中心", "published_at": "2026-06-18", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "确认罗智郎县委副书记、县长身份"},
        {"id": "S002", "title": "那坡县人民政府关于县人民政府领导同志工作分工调整的通知（那政发〔2026〕2号）",
         "url": "http://www.napo.gov.cn/zfxxgkzl/zcwj/xianbenjiwenjian/nzf/t27261230.shtml",
         "publisher": "那坡县人民政府", "published_at": "2026-02-11", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "确认罗智郎主持县政府全面工作，主管财政、审计"},
    ]

    person_luo = build_person_json(
        [p for p in persons if p["name"] == "罗智郎"][0],
        timeline_luo,
        rels_luo,
        sources_luo
    )

    # Write JSON files
    now_str = AS_OF.replace("-", "")
    for person_data, name, job_title in [
        (person_huang, "黄台勇", "那坡县委书记"),
        (person_luo, "罗智郎", "那坡县长"),
    ]:
        filename = f"{now_str}-广西壮族自治区-百色市-{job_title}-{name}.json"
        filepath = os.path.join(PERSONS_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(person_data, f, ensure_ascii=False, indent=2)
        print(f"Person JSON written: {filepath}")


# =========================================================================
# 7. MAIN
# =========================================================================
def main():
    print("=" * 60)
    print(f"构建那坡县领导班子关系网络")
    print(f"数据截止日期: {AS_OF}")
    print(f"暂存目录: {STAGING_DIR}")
    print("=" * 60)

    build_db()
    build_gexf()
    build_all_person_jsons()

    print()
    print("=== 构建完成 ===")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Person JSONs: {PERSONS_DIR}")


if __name__ == "__main__":
    main()
