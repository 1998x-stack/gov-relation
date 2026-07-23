#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
桂平市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县级市
Province: 广西壮族自治区
Parent City: 贵港市
Region: 桂平市
Targets: 市委书记 & 市长

当前在任 (as of 2026-07-23):
- 市委书记: 杨燕忠 (2026年7月上任，前任港北区委书记)
- 市长: 卜凡 (桂平市委副书记、市长、市政府党组书记)

前市委书记: 黄创优 (~2026年7月离任)
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "桂平市"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-23"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：市委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "杨燕忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桂平市委书记",
        "current_org": "中共桂平市委员会",
        "source": "https://www.guiping.gov.cn/"
    },
    # ════════════════════════════════════════
    # 核心领导：市长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "卜凡",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桂平市委副书记、市长、市政府党组书记",
        "current_org": "桂平市人民政府/中共桂平市委员会",
        "source": "https://www.guiping.gov.cn/"
    },
    # ════════════════════════════════════════
    # 前任市委书记
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "黄创优",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://www.guiping.gov.cn/"
    },
    # ════════════════════════════════════════
    # 市委副书记、常务副市长
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "蒙鑫淼",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桂平市委副书记、常务副市长",
        "current_org": "桂平市人民政府/中共桂平市委员会",
        "source": "https://www.guiping.gov.cn/"
    },
    # ════════════════════════════════════════
    # 市人大常委会主任
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "蒙爱杏",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桂平市人大常委会主任",
        "current_org": "桂平市人民代表大会常务委员会",
        "source": "https://www.guiping.gov.cn/"
    },
    # ════════════════════════════════════════
    # 市政协主席
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "梁东",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桂平市政协主席",
        "current_org": "中国人民政治协商会议桂平市委员会",
        "source": "https://www.guiping.gov.cn/"
    },
    # ════════════════════════════════════════
    # 副市长
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "陆建军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桂平市副市长",
        "current_org": "桂平市人民政府",
        "source": "https://www.guiping.gov.cn/"
    },
    {
        "id": 8,
        "name": "黄健文",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桂平市副市长",
        "current_org": "桂平市人民政府",
        "source": "https://www.guiping.gov.cn/"
    },
    {
        "id": 9,
        "name": "陈庆勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桂平市副市长",
        "current_org": "桂平市人民政府",
        "source": "https://www.guiping.gov.cn/"
    },
    # ════════════════════════════════════════
    # 市人大常委会副主任
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "郑具清",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桂平市人大常委会副主任",
        "current_org": "桂平市人民代表大会常务委员会",
        "source": "https://www.guiping.gov.cn/"
    },
    # ════════════════════════════════════════
    # 市政协副主席
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "陈雪峰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桂平市政协副主席",
        "current_org": "中国人民政治协商会议桂平市委员会",
        "source": "https://www.guiping.gov.cn/"
    },
    # ════════════════════════════════════════
    # 其他市领导（2026年两会列名）
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "陆献玲",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桂平市领导",
        "current_org": "桂平市",
        "source": "https://www.guiping.gov.cn/"
    },
    {
        "id": 13,
        "name": "陈家羡",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桂平市领导",
        "current_org": "桂平市",
        "source": "https://www.guiping.gov.cn/"
    },
    {
        "id": 14,
        "name": "覃桂深",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桂平市领导",
        "current_org": "桂平市",
        "source": "https://www.guiping.gov.cn/"
    },
    {
        "id": 15,
        "name": "黄平壮",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桂平市领导",
        "current_org": "桂平市",
        "source": "https://www.guiping.gov.cn/"
    },
    {
        "id": 16,
        "name": "潘振成",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桂平市领导",
        "current_org": "桂平市",
        "source": "https://www.guiping.gov.cn/"
    },
    {
        "id": 17,
        "name": "李凌明",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桂平市领导",
        "current_org": "桂平市",
        "source": "https://www.guiping.gov.cn/"
    },
    {
        "id": 18,
        "name": "陈丕钊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桂平市领导",
        "current_org": "桂平市",
        "source": "https://www.guiping.gov.cn/"
    },
    {
        "id": 19,
        "name": "廖恬",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桂平市领导",
        "current_org": "桂平市",
        "source": "https://www.guiping.gov.cn/"
    },
    {
        "id": 20,
        "name": "杨锋",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桂平市领导",
        "current_org": "桂平市",
        "source": "https://www.guiping.gov.cn/"
    },
    {
        "id": 21,
        "name": "冼济江",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桂平市领导",
        "current_org": "桂平市",
        "source": "https://www.guiping.gov.cn/"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共桂平市委员会", "type": "党委", "level": "县处级",
     "parent": "中共贵港市委员会", "location": "广西贵港桂平市"},
    {"id": 2, "name": "桂平市人民政府", "type": "政府", "level": "县处级",
     "parent": "贵港市人民政府", "location": "广西贵港桂平市"},
    {"id": 3, "name": "桂平市人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "贵港市人大常委会", "location": "广西贵港桂平市"},
    {"id": 4, "name": "中国人民政治协商会议桂平市委员会", "type": "政协", "level": "县处级",
     "parent": "贵港市政协", "location": "广西贵港桂平市"},
    {"id": 5, "name": "中共桂平市纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共桂平市委员会", "location": "广西贵港桂平市"},
    {"id": 6, "name": "中共桂平市委员会宣传部", "type": "党委", "level": "县处级",
     "parent": "中共桂平市委员会", "location": "广西贵港桂平市"},
    {"id": 7, "name": "中共桂平市委员会统战部", "type": "党委", "level": "县处级",
     "parent": "中共桂平市委员会", "location": "广西贵港桂平市"},
    {"id": 8, "name": "中共桂平市委员会政法委员会", "type": "党委", "level": "县处级",
     "parent": "中共桂平市委员会", "location": "广西贵港桂平市"},
    {"id": 9, "name": "桂平市人民武装部", "type": "政府", "level": "县处级",
     "parent": "桂平市人民政府", "location": "广西贵港桂平市"},
    {"id": 10, "name": "桂平市人民法院", "type": "政府", "level": "县处级",
     "parent": "桂平市人民政府", "location": "广西贵港桂平市"},
    {"id": 11, "name": "桂平市人民检察院", "type": "政府", "level": "县处级",
     "parent": "桂平市人民政府", "location": "广西贵港桂平市"},
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 杨燕忠 — 桂平市委书记 (2026-07~)
    {"person_id": 1, "org_id": 1, "title": "桂平市委书记",
     "start_date": "2026-07", "end_date": "present", "rank": "县处级",
     "note": "2026年7月15日首次以桂平市委书记身份主持召开市委常委会。此前任港北区委书记"},
    # 杨燕忠 — 港北区委书记 (前任职务)
    {"person_id": 1, "org_id": 1, "title": "港北区委书记（前任）",
     "start_date": "unknown", "end_date": "2026-06", "rank": "县处级",
     "note": "2026年6月5日仍以港北区委书记身份开展调研，6月26日检查中考备考工作"},

    # 卜凡 — 桂平市长
    {"person_id": 2, "org_id": 2, "title": "桂平市市长",
     "start_date": "unknown", "end_date": "present", "rank": "县处级",
     "note": "2025年10月24日以市长身份主持召开市政府第73次常务会议。2026年2月12日在市人大会议上作政府工作报告"},
    {"person_id": 2, "org_id": 1, "title": "桂平市委副书记",
     "start_date": "unknown", "end_date": "present", "rank": "县处级",
     "note": "担任桂平市委副书记，市政府党组书记"},

    # 黄创优 — 前任桂平市委书记
    {"person_id": 3, "org_id": 1, "title": "桂平市委书记（前任）",
     "start_date": "unknown", "end_date": "2026-07", "rank": "县处级",
     "note": "2026年2月12日主持市人大会议，2026年6月10日仍以市委书记身份主持化解历史矛盾推进会。此后由杨燕忠接任"},
    {"person_id": 3, "org_id": 2, "title": "桂平市领导",
     "start_date": "unknown", "end_date": "2026-07", "rank": "县处级",
     "note": "曾同时担任桂平市党政领导"},

    # 蒙鑫淼 — 市委副书记、常务副市长
    {"person_id": 4, "org_id": 1, "title": "桂平市委副书记",
     "start_date": "unknown", "end_date": "present", "rank": "县处级",
     "note": ""},
    {"person_id": 4, "org_id": 2, "title": "桂平市常务副市长",
     "start_date": "unknown", "end_date": "present", "rank": "县处级",
     "note": ""},

    # 蒙爱杏 — 人大主任
    {"person_id": 5, "org_id": 3, "title": "桂平市人大常委会主任",
     "start_date": "unknown", "end_date": "present", "rank": "县处级",
     "note": "2026年2月12日在市人大会议上作人大常委会工作报告"},

    # 梁东 — 政协主席
    {"person_id": 6, "org_id": 4, "title": "桂平市政协主席",
     "start_date": "unknown", "end_date": "present", "rank": "县处级",
     "note": ""},

    # 陆建军 — 副市长
    {"person_id": 7, "org_id": 2, "title": "桂平市副市长",
     "start_date": "unknown", "end_date": "present", "rank": "副县处级",
     "note": "2025年10月24日市政府常务会议列名副市长"},

    # 黄健文 — 副市长
    {"person_id": 8, "org_id": 2, "title": "桂平市副市长",
     "start_date": "unknown", "end_date": "present", "rank": "副县处级",
     "note": "2025年10月24日市政府常务会议列名副市长"},

    # 陈庆勇 — 副市长
    {"person_id": 9, "org_id": 2, "title": "桂平市副市长",
     "start_date": "unknown", "end_date": "present", "rank": "副县处级",
     "note": "2025-2026年多次市政府常务会议列名副市长"},

    # 郑具清 — 人大副主任
    {"person_id": 10, "org_id": 3, "title": "桂平市人大常委会副主任",
     "start_date": "unknown", "end_date": "present", "rank": "副县处级",
     "note": "2026年人大会议执行主席"},

    # 陈雪峰 — 政协副主席
    {"person_id": 11, "org_id": 4, "title": "桂平市政协副主席",
     "start_date": "unknown", "end_date": "present", "rank": "副县处级",
     "note": "2025年10月24日市政府常务会议列名"},  # 未确认是否仍为政协副主席
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 杨燕忠 ↔ 卜凡（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "杨燕忠（市委书记）与卜凡（市长）为桂平市当前党政一把手搭档",
     "overlap_org": "中共桂平市委员会/桂平市人民政府",
     "overlap_period": "2026-07-present"},

    # 杨燕忠 → 黄创优（前任接任）
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor",
     "context": "杨燕忠接替黄创优任桂平市委书记",
     "overlap_org": "中共桂平市委员会",
     "overlap_period": "2026-07"},

    # 黄创优 ↔ 卜凡（前任市委书记与市长搭档）
    {"person_a": 3, "person_b": 2, "type": "overlap",
     "context": "黄创优任桂平市委书记期间，卜凡任市长，党政搭档关系",
     "overlap_org": "中共桂平市委员会/桂平市人民政府",
     "overlap_period": "至2026-06"},

    # 蒙鑫淼 ↔ 卜凡（市长+常务副市长搭档）
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "卜凡（市长）与蒙鑫淼（常务副市长）在市政府班子中搭档",
     "overlap_org": "桂平市人民政府",
     "overlap_period": "present"},

    # 蒙爱杏 ↔ 黄创优（市委书记+人大主任）
    {"person_a": 3, "person_b": 5, "type": "overlap",
     "context": "黄创优任市委书记期间蒙爱杏任人大主任",
     "overlap_org": "桂平市四家班子",
     "overlap_period": "至2026-06"},

    # 梁东 ↔ 黄创优（市委书记+政协主席）
    {"person_a": 3, "person_b": 6, "type": "overlap",
     "context": "黄创优任市委书记期间梁东任政协主席",
     "overlap_org": "桂平市四家班子",
     "overlap_period": "to 2026-06"},
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
    if "市长" in cp and "副" not in cp and "市委" not in cp:
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
    if "主席" in cp:
        return "60,180,60"
    return "100,100,100"


def person_size(current_post):
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp and "纪委书记" not in cp:
        return "20.0"
    if "市长" in cp and "副" not in cp:
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
    lines.append('    <description>桂平市领导班子关系网络 — Sources: Official government website, news reports</description>')
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
        color = person_color(post)
        size = person_size(post)
        shape = person_shape(post)

        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    # Nodes — organizations
    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o["type"])

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
    """Build a single person graph JSON dict."""
    p = person
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "贵港市",
            "region": "桂平市",
            "job": p.get("current_post", "").split("、")[-1] if "、" in p.get("current_post", "") else p.get("current_post", ""),
            "task_id": "guangxi_桂平市",
            "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"guiping_{p['name']}",
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
            "administrative_rank": "",
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
            "identity": "confirmed" if p.get("birth") else "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"Earlier career timeline before current role for {p['name']}"
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
        {"id": "S001", "title": "桂平市人民政府门户网站",
         "url": "https://www.guiping.gov.cn/", "publisher": "桂平市人民政府",
         "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "Active government portal with current leadership info"},
        {"id": "S002", "title": "桂平市两会报道",
         "url": "https://mp.weixin.qq.com/s/D9mHs6OMtDSpWJ9mF0vZPQ",
         "publisher": "新桂平（桂平市融媒体中心）", "published_at": "2026-02-12",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "桂平市第十七届人民代表大会第六次会议，确认全部四家班子领导名单"},
        {"id": "S003", "title": "港北区政府门户网站",
         "url": "http://www.gbq.gov.cn/", "publisher": "港北区人民政府",
         "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "杨燕忠前任职务（港北区委书记）信息"},
    ]

    # ── 杨燕忠 person JSON ──
    yyz_timeline = [
        {"start": "2026-07", "end": "present",
         "org": "中共桂平市委员会", "title": "桂平市委书记",
         "level": "县处级", "location": "广西贵港桂平市",
         "system": "party", "rank": "县处级", "is_key_promotion": True,
         "notes": "2026年7月15日首次以桂平市委书记身份主持会议。从港北区调任桂平市，属于跨区交流提拔",
         "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "2026-06",
         "org": "中共贵港市港北区委员会", "title": "港北区委书记",
         "level": "县处级", "location": "广西贵港港北区",
         "system": "party", "rank": "县处级", "is_key_promotion": True,
         "notes": "2026年6月5日仍以港北区委书记身份开展企业纾困解难调研，6月26日检查中考备考工作。此后由刘理接任",
         "confidence": "confirmed", "source_ids": ["S003"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口", "title": "",
         "notes": "公开资料未找到杨燕忠就任港北区委书记前的完整履历。其此前在何处任职、何时担任港北区委书记均待查",
         "confidence": "unverified", "source_ids": []},
    ]
    yyz_relationships = [
        {"person": "卜凡", "person_id": "guiping_卜凡",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "杨燕忠（市委书记）与卜凡（市长）为桂平市当前党政一把手搭档",
         "overlap_org": "中共桂平市委员会/桂平市人民政府",
         "overlap_period": "2026-07-present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "黄创优", "person_id": "guiping_黄创优",
         "relationship_type": "predecessor_successor",
         "strength": "strong",
         "evidence": "杨燕忠接替黄创优任桂平市委书记",
         "overlap_org": "中共桂平市委员会",
         "overlap_period": "2026-07",
         "direction": "other_to_person",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    yyz_json = build_person_json(persons[0], yyz_timeline, yyz_relationships, sources)
    yyz_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-贵港市-市委书记-杨燕忠.json")
    with open(yyz_path, "w", encoding="utf-8") as f:
        json.dump(yyz_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {yyz_path}")

    # ── 卜凡 person JSON ──
    bf_timeline = [
        {"start": "unknown", "end": "present",
         "org": "桂平市人民政府/中共桂平市委员会",
         "title": "桂平市委副书记、市长、市政府党组书记",
         "level": "县处级", "location": "广西贵港桂平市",
         "system": "government", "rank": "县处级",
         "is_key_promotion": True,
         "notes": "负责市政府全面工作。2025年10月起以市长身份主持市政府常务会议（第73次起），2026年2月在市人大会议上作政府工作报告",
         "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口", "title": "",
         "notes": "公开资料未找到卜凡就任桂平市长前的完整履历。其此前在何处任职、何时担任桂平市长均待查",
         "confidence": "unverified", "source_ids": []},
    ]
    bf_relationships = [
        {"person": "杨燕忠", "person_id": "guiping_杨燕忠",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "卜凡（市长）与杨燕忠（市委书记）为桂平市当前党政一把手搭档",
         "overlap_org": "中共桂平市委员会/桂平市人民政府",
         "overlap_period": "2026-07-present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "黄创优", "person_id": "guiping_黄创优",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "卜凡任市长期间黄创优曾任市委书记，党政搭档关系",
         "overlap_org": "中共桂平市委员会/桂平市人民政府",
         "overlap_period": "至2026-06",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001", "S002"]},
        {"person": "蒙鑫淼", "person_id": "guiping_蒙鑫淼",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "卜凡（市长）与蒙鑫淼（常务副市长）在市政府班子中紧密搭档",
         "overlap_org": "桂平市人民政府",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    bf_json = build_person_json(persons[1], bf_timeline, bf_relationships, sources)
    bf_json["investigation_scope"]["job"] = "市长"
    bf_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-贵港市-市长-卜凡.json")
    with open(bf_path, "w", encoding="utf-8") as f:
        json.dump(bf_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {bf_path}")

    # ── 黄创优 person JSON（前任市委书记） ──
    hcy_timeline = [
        {"start": "unknown", "end": "2026-07",
         "org": "中共桂平市委员会", "title": "桂平市委书记",
         "level": "县处级", "location": "广西贵港桂平市",
         "system": "party", "rank": "县处级", "is_key_promotion": True,
         "notes": "2026年2月12日主持市人大会议，2026年6月10日主持全市化解历史矛盾推进会。此后由杨燕忠接任。去向待查",
         "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口", "title": "",
         "notes": "公开资料未找到黄创优就任桂平市委书记前的完整履历。黄创优在贵港市数据库中有记录，曾任贵港市领导",
         "confidence": "unverified", "source_ids": []},
    ]
    hcy_relationships = [
        {"person": "卜凡", "person_id": "guiping_卜凡",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "黄创优任市委书记期间卜凡任市长，党政搭档关系",
         "overlap_org": "中共桂平市委员会/桂平市人民政府",
         "overlap_period": "to 2026-06",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001", "S002"]},
        {"person": "杨燕忠", "person_id": "guiping_杨燕忠",
         "relationship_type": "predecessor_successor",
         "strength": "strong",
         "evidence": "杨燕忠接替黄创优任桂平市委书记",
         "overlap_org": "中共桂平市委员会",
         "overlap_period": "2026-07",
         "direction": "person_to_other",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "蒙爱杏", "person_id": "guiping_蒙爱杏",
         "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "黄创优任市委书记期间蒙爱杏任人大主任",
         "overlap_org": "桂平市四家班子",
         "overlap_period": "to 2026-06",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S002"]},
    ]
    hcy_json = build_person_json(persons[2], hcy_timeline, hcy_relationships, sources)
    hcy_json["investigation_scope"]["job"] = "市委书记（前任）"
    hcy_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-贵港市-市委书记（前任）-黄创优.json")
    with open(hcy_path, "w", encoding="utf-8") as f:
        json.dump(hcy_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {hcy_path}")


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
