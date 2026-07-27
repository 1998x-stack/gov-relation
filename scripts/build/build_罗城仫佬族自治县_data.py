#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
罗城仫佬族自治县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县（自治县）
Province: 广西壮族自治区
Parent City: 河池市
Region: 罗城仫佬族自治县
Targets: 县委书记 & 县长

当前在任信息（基于公开资料整理，as of 2026-07-23）:
- 县委书记: 吴贞儒
- 县长: 吴国军
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "罗城仫佬族自治县"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-23"

# =========================================================================
# 1. PERSONS (ordered by importance)
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：县委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "吴贞儒",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "罗城仫佬族自治县委书记",
        "current_org": "中共罗城仫佬族自治县委员会",
        "source": "https://baike.baidu.com/item/%E5%90%B4%E8%B4%9E%E5%84%92"
    },
    # ════════════════════════════════════════
    # 核心领导：县长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "吴国军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "罗城仫佬族自治县县长",
        "current_org": "罗城仫佬族自治县人民政府",
        "source": "http://www.luocheng.gov.cn/zfxxgk/zcwj20/zfbwj/t27563987.shtml"
    },
    # ════════════════════════════════════════
    # 常务副县长
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "陆金光",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "罗城仫佬族自治县常务副县长",
        "current_org": "罗城仫佬族自治县人民政府",
        "source": "http://www.luocheng.gov.cn/zfxxgk/zcwj20/zfbwj/t27563987.shtml"
    },
    # ════════════════════════════════════════
    # 副县长：杨妍（挂职深圳龙华）
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "杨妍",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "罗城仫佬族自治县副县长（挂职）",
        "current_org": "罗城仫佬族自治县人民政府",
        "source": "http://www.luocheng.gov.cn/zfxxgk/zcwj20/zfbwj/t27563987.shtml"
    },
    # ════════════════════════════════════════
    # 副县长（挂职）：闵志强（国家林草局）
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "闵志强",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "罗城仫佬族自治县副县长（挂职）",
        "current_org": "罗城仫佬族自治县人民政府",
        "source": "http://www.luocheng.gov.cn/zfxxgk/zcwj20/zfbwj/t27563987.shtml"
    },
    # ════════════════════════════════════════
    # 副县长（挂职）：赵成刚（粤桂协作）
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "赵成刚",
        "ethnicity": "",
        "gender": "男",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "罗城仫佬族自治县副县长（挂职）",
        "current_org": "罗城仫佬族自治县人民政府",
        "source": "http://www.luocheng.gov.cn/zfxxgk/zcwj20/zfbwj/t27563987.shtml"
    },
    # ════════════════════════════════════════
    # 副县长（挂职）：肖春明（驻村工作队）
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "肖春明",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "罗城仫佬族自治县副县长（挂职）",
        "current_org": "罗城仫佬族自治县人民政府",
        "source": "http://www.luocheng.gov.cn/zfxxgk/zcwj20/zfbwj/t27563987.shtml"
    },
    # ════════════════════════════════════════
    # 副县长：黄中建（公安）
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "黄中建",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "罗城仫佬族自治县副县长、公安局局长",
        "current_org": "罗城仫佬族自治县人民政府/公安局",
        "source": "http://www.luocheng.gov.cn/zfxxgk/zcwj20/zfbwj/t27563987.shtml"
    },
    # ════════════════════════════════════════
    # 副县长：范小龙
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "范小龙",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "罗城仫佬族自治县副县长",
        "current_org": "罗城仫佬族自治县人民政府",
        "source": "http://www.luocheng.gov.cn/zfxxgk/zcwj20/zfbwj/t27563987.shtml"
    },
    # ════════════════════════════════════════
    # 副县长：韦覃猛
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "韦覃猛",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "罗城仫佬族自治县副县长",
        "current_org": "罗城仫佬族自治县人民政府",
        "source": "http://www.luocheng.gov.cn/zfxxgk/zcwj20/zfbwj/t27563987.shtml"
    },
    # ════════════════════════════════════════
    # 副县长：谭奇兵
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "谭奇兵",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "罗城仫佬族自治县副县长",
        "current_org": "罗城仫佬族自治县人民政府",
        "source": "http://www.luocheng.gov.cn/zfxxgk/zcwj20/zfbwj/t27563987.shtml"
    },
    # ════════════════════════════════════════
    # 副县长级：邹明助（供销联社）
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "邹明助",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "罗城仫佬族自治县副县长级、供销联社主任",
        "current_org": "罗城仫佬族自治县人民政府/供销联社",
        "source": "http://www.luocheng.gov.cn/zfxxgk/zcwj20/zfbwj/t27563987.shtml"
    },
]


# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {
        "id": 1,
        "name": "中共罗城仫佬族自治县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共河池市委员会",
        "location": "广西河池罗城仫佬族自治县"
    },
    {
        "id": 2,
        "name": "罗城仫佬族自治县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "河池市人民政府",
        "location": "广西河池罗城仫佬族自治县"
    },
    {
        "id": 3,
        "name": "罗城仫佬族自治县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "罗城仫佬族自治县人民政府/河池市公安局",
        "location": "广西河池罗城仫佬族自治县"
    },
    {
        "id": 4,
        "name": "罗城仫佬族自治县供销联社",
        "type": "政府",
        "level": "县级",
        "parent": "罗城仫佬族自治县人民政府",
        "location": "广西河池罗城仫佬族自治县"
    },
    {
        "id": 5,
        "name": "中共罗城仫佬族自治县纪律检查委员会",
        "type": "纪委",
        "level": "县级",
        "parent": "中共河池市纪律检查委员会",
        "location": "广西河池罗城仫佬族自治县"
    },
    {
        "id": 6,
        "name": "罗城仫佬族自治县人大常委会",
        "type": "人大",
        "level": "县级",
        "parent": "河池市人大常委会",
        "location": "广西河池罗城仫佬族自治县"
    },
    {
        "id": 7,
        "name": "政协罗城仫佬族自治县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "政协河池市委员会",
        "location": "广西河池罗城仫佬族自治县"
    },
]


# =========================================================================
# 3. POSITIONS (career timeline for each person)
# =========================================================================
positions = [
    # 吴贞儒
    {"person_id": 1, "org_id": 1, "title": "罗城仫佬族自治县委书记",
     "start_date": "unknown", "end_date": "present", "rank": "正处级",
     "note": "公开资料未找到吴贞儒任县委书记之前的完整履历"},
    # 吴国军
    {"person_id": 2, "org_id": 2, "title": "罗城仫佬族自治县县长",
     "start_date": "2025?", "end_date": "present", "rank": "正处级",
     "note": "根据2026年1月政府领导分工通知确认现任县长"},
    {"person_id": 2, "org_id": 1, "title": "罗城仫佬族自治县委副书记",
     "start_date": "unknown", "end_date": "present", "rank": "正处级",
     "note": "县长兼任县委副书记"},
    # 陆金光（常务副县长）
    {"person_id": 3, "org_id": 2, "title": "罗城仫佬族自治县常务副县长",
     "start_date": "unknown", "end_date": "present", "rank": "副处级",
     "note": "负责县政府常务工作"},
    {"person_id": 3, "org_id": 1, "title": "罗城仫佬族自治县委常委",
     "start_date": "unknown", "end_date": "present", "rank": "副处级",
     "note": "常务副县长通常为县委常委"},
    # 杨妍
    {"person_id": 4, "org_id": 2, "title": "罗城仫佬族自治县副县长（挂职）",
     "start_date": "unknown", "end_date": "present", "rank": "副处级",
     "note": "在深圳市龙华区福城街道挂职"},
    # 闵志强（国家林草局挂职）
    {"person_id": 5, "org_id": 2, "title": "罗城仫佬族自治县副县长（挂职）",
     "start_date": "unknown", "end_date": "present", "rank": "副处级",
     "note": "国家林草局定点帮扶罗城"},
    # 赵成刚（粤桂协作挂职）
    {"person_id": 6, "org_id": 2, "title": "罗城仫佬族自治县副县长（挂职）",
     "start_date": "unknown", "end_date": "present", "rank": "副处级",
     "note": "粤桂东西部协作"},
    # 肖春明（驻村工作队挂职）
    {"person_id": 7, "org_id": 2, "title": "罗城仫佬族自治县副县长（挂职）",
     "start_date": "unknown", "end_date": "present", "rank": "副处级",
     "note": "广西罗城驻村工作队"},
    # 黄中建
    {"person_id": 8, "org_id": 2, "title": "罗城仫佬族自治县副县长",
     "start_date": "unknown", "end_date": "present", "rank": "副处级",
     "note": "分管公安、武装、司法、信访维稳"},
    {"person_id": 8, "org_id": 3, "title": "罗城仫佬族自治县公安局局长",
     "start_date": "unknown", "end_date": "present", "rank": "副处级",
     "note": "兼任县公安局局长"},
    # 范小龙
    {"person_id": 9, "org_id": 2, "title": "罗城仫佬族自治县副县长",
     "start_date": "unknown", "end_date": "present", "rank": "副处级",
     "note": "分管教育、文旅、交通、卫健、医保、民政、退役军人事务"},
    # 韦覃猛
    {"person_id": 10, "org_id": 2, "title": "罗城仫佬族自治县副县长",
     "start_date": "unknown", "end_date": "present", "rank": "副处级",
     "note": "分管乡村振兴、水利、农业农村、林业、糖业、妇女儿童"},
    # 谭奇兵
    {"person_id": 11, "org_id": 2, "title": "罗城仫佬族自治县副县长",
     "start_date": "unknown", "end_date": "present", "rank": "副处级",
     "note": "分管生态环境、工业科技、招商、人社、大数据、市场监管、民族宗教"},
    # 邹明助
    {"person_id": 12, "org_id": 2, "title": "罗城仫佬族自治县副县长级",
     "start_date": "unknown", "end_date": "present", "rank": "副处级",
     "note": "分管供销联社，协助交通、招商引资"},
    {"person_id": 12, "org_id": 4, "title": "罗城仫佬族自治县供销联社主任",
     "start_date": "unknown", "end_date": "present", "rank": "副处级",
     "note": "兼任供销联社主任"},
]


# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 党政一把手搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "罗城仫佬族自治县现任县委书记与县长党政搭档关系",
     "overlap_org": "中共罗城仫佬族自治县委员会/罗城仫佬族自治县人民政府",
     "overlap_period": "present"},
    # 县委书记与常务副县长
    {"person_a": 1, "person_b": 3, "type": "上下级",
     "context": "县委书记与常务副县长县委常委班子关系",
     "overlap_org": "中共罗城仫佬族自治县委员会",
     "overlap_period": "present"},
    # 县长与常务副县长
    {"person_a": 2, "person_b": 3, "type": "上下级",
     "context": "县长与常务副县长工作搭档关系",
     "overlap_org": "罗城仫佬族自治县人民政府",
     "overlap_period": "present"},
    # 县长与各副县长（共事关系）
    {"person_a": 2, "person_b": 4, "type": "上下级",
     "context": "县长与挂职副县长政府班子关系",
     "overlap_org": "罗城仫佬族自治县人民政府",
     "overlap_period": "present"},
    {"person_a": 2, "person_b": 5, "type": "上下级",
     "context": "县长与挂职副县长政府班子关系",
     "overlap_org": "罗城仫佬族自治县人民政府",
     "overlap_period": "present"},
    {"person_a": 2, "person_b": 6, "type": "上下级",
     "context": "县长与挂职副县长政府班子关系",
     "overlap_org": "罗城仫佬族自治县人民政府",
     "overlap_period": "present"},
    {"person_a": 2, "person_b": 7, "type": "上下级",
     "context": "县长与挂职副县长政府班子关系",
     "overlap_org": "罗城仫佬族自治县人民政府",
     "overlap_period": "present"},
    {"person_a": 2, "person_b": 8, "type": "上下级",
     "context": "县长与副县长政府班子关系",
     "overlap_org": "罗城仫佬族自治县人民政府",
     "overlap_period": "present"},
    {"person_a": 2, "person_b": 9, "type": "上下级",
     "context": "县长与副县长政府班子关系",
     "overlap_org": "罗城仫佬族自治县人民政府",
     "overlap_period": "present"},
    {"person_a": 2, "person_b": 10, "type": "上下级",
     "context": "县长与副县长政府班子关系",
     "overlap_org": "罗城仫佬族自治县人民政府",
     "overlap_period": "present"},
    {"person_a": 2, "person_b": 11, "type": "上下级",
     "context": "县长与副县长政府班子关系",
     "overlap_org": "罗城仫佬族自治县人民政府",
     "overlap_period": "present"},
    {"person_a": 2, "person_b": 12, "type": "上下级",
     "context": "县长与副县长级领导政府班子关系",
     "overlap_org": "罗城仫佬族自治县人民政府",
     "overlap_period": "present"},
]


# =========================================================================
# 5. HELPERS
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(current_post):
    """Return GEXF color string for a person based on role."""
    cp = current_post or ""
    if "县委书记" in cp or "县委书记" in cp:
        return "200,30,30"
    if "县长" in cp and "副" not in cp and "挂职" not in cp:
        return "30,100,200"
    if "副书记" in cp:
        return "220,80,80"
    if "常务副" in cp:
        return "100,150,220"
    if "副" in cp and "县长" in cp:
        return "100,150,220"
    if "常委" in cp:
        return "180,100,180"
    if "主任" in cp or "人大" in cp:
        return "60,180,60"
    if "主席" in cp:
        return "60,180,60"
    return "100,100,100"


def person_size(current_post):
    """Return GEXF node size based on role."""
    cp = current_post or ""
    if "县委书记" in cp or "县委书记" in cp:
        return "20.0"
    if "县长" in cp and "副" not in cp and "挂职" not in cp:
        return "18.0"
    if "副书记" in cp:
        return "15.0"
    if "常务副" in cp:
        return "15.0"
    if "副" in cp:
        return "12.0"
    if "常委" in cp:
        return "12.0"
    if "主任" in cp or "主席" in cp:
        return "12.0"
    return "10.0"


def person_shape(current_post):
    """Return GEXF shape based on role."""
    cp = current_post or ""
    if "书记" in cp:
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
        cur.execute("""INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,
                       party_join,work_start,current_post,current_org,source)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
                     p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
                     p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""),
                     p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location)
                       VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"],
                     o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note)
                       VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"],
                     pos.get("start_date", ""), pos.get("end_date", ""),
                     pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period)
                       VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"], r["context"],
                     r.get("overlap_org", ""), r.get("overlap_period", "")))

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
    lines.append(f'    <description>{SLUG}领导班子关系网络</description>')
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

    # Nodes - persons
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        cp = p.get("current_post", "")
        color = person_color(cp)
        size = person_size(cp)
        shape = person_shape(cp)
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(cp)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o["type"])
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('        <viz:shape value="hexagon"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]+100000}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ person (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")


def build_person_json(person, timeline, rels, sources):
    """Build a single person graph JSON dict."""
    p = person
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "河池市",
            "region": "罗城仫佬族自治县",
            "job": p.get("current_post", ""),
            "task_id": "guangxi_罗城仫佬族自治县",
            "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"luocheng_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source", "")
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "正处级" if p["id"] <= 2 else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": bool(p.get("current_post")),
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
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "No risk signals found through available public sources",
            "date": "",
            "confidence": "unverified",
            "source_ids": []
        }],
        "source_register": sources,
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"Complete career timeline before current role for {p['name']}"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"Complete career timeline before current role - full position history for {p['name']}",
                "why_it_matters": "Cannot assess career pattern, promotion velocity, or network building without full timeline",
                "suggested_queries": [f"{p['name']} 简历", f"{p['name']} 任职经历", f"{p['name']} 百度百科"],
                "last_attempted": AS_OF
            }
        ]
    }


def build_person_jsons():
    """Build and write person JSON files for core leaders."""
    now = AS_OF.replace("-", "")

    sources = [
        {"id": "S001", "title": "罗城仫佬族自治县人民政府门户网站",
         "url": "http://www.luocheng.gov.cn/", "publisher": "罗城仫佬族自治县人民政府",
         "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "Active government portal with current leadership info"},
        {"id": "S002", "title": "罗城仫佬族自治县人民政府关于政府领导工作分工调整的通知",
         "url": "http://www.luocheng.gov.cn/zfxxgk/zcwj20/zfbwj/t27563987.shtml",
         "publisher": "罗城仫佬族自治县人民政府办公室", "published_at": "2026-01-08",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "Official document detailing all government leaders and their work divisions"},
        {"id": "S003", "title": "罗城仫佬族自治县百度百科",
         "url": "https://baike.baidu.com/item/%E7%BD%97%E5%9F%8E%E4%BB%AB%E4%BD%AC%E6%97%8F%E8%87%AA%E6%B2%BB%E5%8E%BF",
         "publisher": "百度百科", "published_at": "",
         "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium",
         "notes": "Lists 吴贞儒 as 县委书记"},
    ]

    # ── 吴贞儒 person JSON ──
    wuzr_timeline = [
        {"start": "unknown", "end": "present",
         "org": "中共罗城仫佬族自治县委员会",
         "title": "罗城仫佬族自治县委书记", "level": "正处级",
         "location": "广西河池罗城仫佬族自治县", "system": "party",
         "rank": "正处级", "is_key_promotion": True,
         "notes": "公开资料未找到吴贞儒任县委书记之前的完整履历",
         "confidence": "confirmed",
         "source_ids": ["S003"]},
    ]
    wuzr_relationships = [
        {"person": "吴国军", "person_id": "luocheng_吴国军",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "罗城仫佬族自治县现任县委书记与县长党政搭档",
         "overlap_org": "中共罗城仫佬族自治县委员会/罗城仫佬族自治县人民政府",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001", "S002"]},
    ]
    wuzr_json = build_person_json(persons[0], wuzr_timeline, wuzr_relationships, sources)
    wuzr_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-河池市-县委书记-吴贞儒.json")
    with open(wuzr_path, "w", encoding="utf-8") as f:
        json.dump(wuzr_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {wuzr_path}")

    # ── 吴国军 person JSON ──
    wugj_timeline = [
        {"start": "2025?", "end": "present",
         "org": "罗城仫佬族自治县人民政府",
         "title": "罗城仫佬族自治县县长", "level": "正处级",
         "location": "广西河池罗城仫佬族自治县", "system": "government",
         "rank": "正处级", "is_key_promotion": True,
         "notes": "2026年1月政府领导分工通知确认其为县长，负责县政府全面工作",
         "confidence": "confirmed",
         "source_ids": ["S001", "S002"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到吴国军任县长之前的完整履历",
         "confidence": "unverified",
         "source_ids": []},
    ]
    wugj_relationships = [
        {"person": "吴贞儒", "person_id": "luocheng_吴贞儒",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "罗城仫佬族自治县现任县长与县委书记党政搭档",
         "overlap_org": "罗城仫佬族自治县人民政府/中共罗城仫佬族自治县委员会",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001", "S002"]},
    ]
    wugj_json = build_person_json(persons[1], wugj_timeline, wugj_relationships, sources)
    wugj_json["investigation_scope"]["job"] = "县长"
    wugj_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-河池市-县长-吴国军.json")
    with open(wugj_path, "w", encoding="utf-8") as f:
        json.dump(wugj_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {wugj_path}")


def build():
    os.makedirs(STAGING_DIR, exist_ok=True)
    print(f"=== Building {SLUG} data ===")
    print(f"Staging dir: {STAGING_DIR}")
    build_db()
    build_gexf()
    build_person_jsons()
    print("\nBuild complete.")


if __name__ == "__main__":
    build()
