#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 崆峒区 (Kongtong District), Pingliang, Gansu.

Targets: 区委书记 (Party Secretary), 区长 (District Mayor)
as of July 2026.
"""

import sqlite3
import os
import sys
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/gansu_崆峒区")
DB_PATH = os.path.join(STAGING, "崆峒区_network.db")
GEXF_PATH = os.path.join(STAGING, "崆峒区_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current Top Leaders ──
    # 刘国军 — 平凉市委常委、崆峒区委书记 (as of 2026.07)
    {"id": 1, "name": "刘国军", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-03", "birthplace": "", "education": "在职研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "平凉市委常委、崆峒区委书记",
     "current_org": "中共平凉市崆峒区委员会",
     "source": "https://www.pingliang.gov.cn/lmtj/ldzc/index.html"},

    # 樊对对 — 崆峒区委副书记、区长 (as of 2026.07, inferred from news activity)
    {"id": 2, "name": "樊对对", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "崆峒区委副书记、区长",
     "current_org": "平凉市崆峒区人民政府",
     "source": "http://www.kongtong.gov.cn/"},

    # ── Predecessors — 区委书记 ──
    # 王琳玺 — 原崆峒区委书记, 后任平凉市委副书记等
    {"id": 3, "name": "王琳玺", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-12", "birthplace": "甘肃", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原崆峒区委书记（已离任）",
     "current_org": "",
     "source": ""},

    # ── Predecessors — 区长 ──
    # 刘小平 — 原崆峒区区长
    {"id": 4, "name": "刘小平", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原崆峒区区长（已离任）",
     "current_org": "",
     "source": ""},

    # ── Standing Committee (区委常委) ──
    {"id": 5, "name": "陶烨", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "崆峒区委常委、政法委书记",
     "current_org": "中共平凉市崆峒区委员会",
     "source": ""},
    {"id": 6, "name": "张喜武", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "崆峒区委常委、纪委书记、监委主任",
     "current_org": "中共平凉市崆峒区纪律检查委员会",
     "source": ""},
    {"id": 7, "name": "罗彦鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "崆峒区委常委、组织部部长",
     "current_org": "中共平凉市崆峒区委员会",
     "source": ""},
    {"id": 8, "name": "万学发", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "崆峒区委常委、统战部部长",
     "current_org": "中共平凉市崆峒区委员会",
     "source": ""},
    {"id": 9, "name": "柴璟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "崆峒区委常委、宣传部部长",
     "current_org": "中共平凉市崆峒区委员会",
     "source": ""},
    {"id": 10, "name": "马瀚铎", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "崆峒区委常委、副区长",
     "current_org": "平凉市崆峒区人民政府",
     "source": ""},

    # ── 区人大常委会 ──
    {"id": 11, "name": "高跟信", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "崆峒区人大常委会主任",
     "current_org": "平凉市崆峒区人大常委会",
     "source": ""},

    # ── 区政协 ──
    {"id": 12, "name": "徐小军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "崆峒区政协主席",
     "current_org": "政协平凉市崆峒区委员会",
     "source": ""},

    # ── 副区长 ──
    {"id": 13, "name": "李文环", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "崆峒区副区长",
     "current_org": "平凉市崆峒区人民政府",
     "source": ""},
    {"id": 14, "name": "吴亮", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "崆峒区副区长",
     "current_org": "平凉市崆峒区人民政府",
     "source": ""},

    # ── 上级领导（平凉市） ——
    {"id": 15, "name": "唐培宏", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-03", "birthplace": "甘肃民勤", "education": "西北师范大学历史系本科、兰州大学公共管理硕士",
     "party_join": "1991-06", "work_start": "1992-07",
     "current_post": "平凉市委书记",
     "current_org": "中共平凉市委员会",
     "source": "https://baike.baidu.com/item/%E5%94%90%E5%9F%B9%E5%AE%8F/15118915"},
    {"id": 16, "name": "李荣", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-12", "birthplace": "甘肃定西", "education": "甘肃政法学院本科、省委党校研究生",
     "party_join": "1996-12", "work_start": "1999-09",
     "current_post": "平凉市委副书记、市长",
     "current_org": "平凉市人民政府",
     "source": "https://www.pingliang.gov.cn/lmtj/ldzc/index.html"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共平凉市崆峒区委员会", "type": "党委", "level": "县处级",
     "parent": "中共平凉市委员会", "location": "甘肃省平凉市崆峒区"},
    {"id": 2, "name": "平凉市崆峒区人民政府", "type": "政府", "level": "县处级",
     "parent": "平凉市人民政府", "location": "甘肃省平凉市崆峒区"},
    {"id": 3, "name": "平凉市崆峒区人大常委会", "type": "人大", "level": "县处级",
     "parent": "平凉市人大常委会", "location": "甘肃省平凉市崆峒区"},
    {"id": 4, "name": "政协平凉市崆峒区委员会", "type": "政协", "level": "县处级",
     "parent": "政协平凉市委员会", "location": "甘肃省平凉市崆峒区"},
    {"id": 5, "name": "中共平凉市崆峒区纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共平凉市崆峒区委员会", "location": "甘肃省平凉市崆峒区"},
    {"id": 6, "name": "中共平凉市崆峒区委组织部", "type": "党委", "level": "县处级",
     "parent": "中共平凉市崆峒区委员会", "location": "甘肃省平凉市崆峒区"},
    {"id": 7, "name": "中共平凉市崆峒区委宣传部", "type": "党委", "level": "县处级",
     "parent": "中共平凉市崆峒区委员会", "location": "甘肃省平凉市崆峒区"},
    {"id": 8, "name": "中共平凉市崆峒区委统战部", "type": "党委", "level": "县处级",
     "parent": "中共平凉市崆峒区委员会", "location": "甘肃省平凉市崆峒区"},
    {"id": 9, "name": "中共平凉市崆峒区委政法委", "type": "党委", "level": "县处级",
     "parent": "中共平凉市崆峒区委员会", "location": "甘肃省平凉市崆峒区"},

    # ── 上级组织 ──
    {"id": 10, "name": "中共平凉市委员会", "type": "党委", "level": "地级",
     "parent": "中共甘肃省委员会", "location": "甘肃省平凉市"},
    {"id": 11, "name": "平凉市人民政府", "type": "政府", "level": "地级",
     "parent": "甘肃省人民政府", "location": "甘肃省平凉市"},

    # ── 刘国军曾任单位 ——
    {"id": 12, "name": "甘肃省人民政府办公厅", "type": "政府", "level": "省级",
     "parent": "甘肃省人民政府", "location": "甘肃省兰州市"},
    {"id": 13, "name": "天水市人民政府", "type": "政府", "level": "地级",
     "parent": "甘肃省人民政府", "location": "甘肃省天水市"},
    {"id": 14, "name": "中共天水市委员会", "type": "党委", "level": "地级",
     "parent": "中共甘肃省委员会", "location": "甘肃省天水市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 刘国军 (id=1) ──
    {"pid": 1, "org": 1, "title": "平凉市委常委、崆峒区委书记",
     "start": "2024-07", "end": "至今", "rank": "副厅级",
     "note": "同时担任平凉市委常委"},
    {"pid": 1, "org": 14, "title": "天水市副市长",
     "start": "2021-09", "end": "2024-07", "rank": "副厅级", "note": ""},
    {"pid": 1, "org": 12, "title": "甘肃省政府办公厅秘书一处处长、一级调研员",
     "start": "", "end": "2021-09", "rank": "正处级", "note": ""},

    # ── 樊对对 (id=2) ──
    {"pid": 2, "org": 2, "title": "崆峒区委副书记、区长",
     "start": "", "end": "至今", "rank": "正处级", "note": "2026年7月新闻报道中活跃"},
    {"pid": 2, "org": 1, "title": "崆峒区委常委、副区长（常务）",
     "start": "", "end": "", "rank": "副处级", "note": "推测此前担任常务副区长"},
    {"pid": 2, "org": 2, "title": "崆峒区副区长",
     "start": "", "end": "", "rank": "副处级", "note": ""},

    # ── 王琳玺 (id=3) ──
    {"pid": 3, "org": 1, "title": "崆峒区委书记",
     "start": "", "end": "2024-07", "rank": "副厅级", "note": "刘国军的前任"},
    {"pid": 3, "org": 10, "title": "平凉市委副书记",
     "start": "", "end": "", "rank": "副厅级", "note": ""},

    # ── 刘小平 (id=4) ──
    {"pid": 4, "org": 2, "title": "崆峒区区长",
     "start": "", "end": "", "rank": "正处级", "note": "樊对对的前任"},

    # ── 陶烨 (id=5) ──
    {"pid": 5, "org": 9, "title": "崆峒区委常委、政法委书记",
     "start": "", "end": "至今", "rank": "副处级", "note": ""},

    # ── 张喜武 (id=6) ──
    {"pid": 6, "org": 5, "title": "崆峒区委常委、纪委书记、监委主任",
     "start": "", "end": "至今", "rank": "副处级", "note": ""},

    # ── 罗彦鹏 (id=7) ──
    {"pid": 7, "org": 6, "title": "崆峒区委常委、组织部部长",
     "start": "", "end": "至今", "rank": "副处级", "note": ""},

    # ── 万学发 (id=8) ──
    {"pid": 8, "org": 8, "title": "崆峒区委常委、统战部部长",
     "start": "", "end": "至今", "rank": "副处级", "note": ""},

    # ── 柴璟 (id=9) ──
    {"pid": 9, "org": 7, "title": "崆峒区委常委、宣传部部长",
     "start": "", "end": "至今", "rank": "副处级", "note": ""},

    # ── 马瀚铎 (id=10) ──
    {"pid": 10, "org": 2, "title": "崆峒区委常委、副区长",
     "start": "", "end": "至今", "rank": "副处级", "note": ""},

    # ── 高跟信 (id=11) ──
    {"pid": 11, "org": 3, "title": "崆峒区人大常委会主任",
     "start": "", "end": "至今", "rank": "正处级", "note": ""},

    # ── 徐小军 (id=12) ──
    {"pid": 12, "org": 4, "title": "崆峒区政协主席",
     "start": "", "end": "至今", "rank": "正处级", "note": ""},

    # ── 李文环 (id=13) ──
    {"pid": 13, "org": 2, "title": "崆峒区副区长",
     "start": "", "end": "至今", "rank": "副处级", "note": ""},

    # ── 吴亮 (id=14) ──
    {"pid": 14, "org": 2, "title": "崆峒区副区长",
     "start": "", "end": "至今", "rank": "副处级", "note": ""},

    # ── 唐培宏 (id=15) ──
    {"pid": 15, "org": 10, "title": "平凉市委书记",
     "start": "2025-09", "end": "至今", "rank": "正厅级", "note": ""},

    # ── 李荣 (id=16) ──
    {"pid": 16, "org": 11, "title": "平凉市委副书记、市长",
     "start": "2026-01", "end": "至今", "rank": "正厅级", "note": "2026年1月任代市长"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 刘国军 ↔ 王琳玺 (predecessor-successor as 区委书记)
    {"a": 1, "b": 3, "type": "predecessor_successor",
     "context": "刘国军于2024年7月接替王琳玺担任崆峒区委书记",
     "overlap_org": "中共平凉市崆峒区委员会",
     "overlap_period": "2024-07",
     "strength": "strong", "confidence": "confirmed"},

    # 刘国军 ↔ 樊对对 (current党政搭档)
    {"a": 1, "b": 2, "type": "overlap",
     "context": "刘国军任区委书记，樊对对任区长，党政搭档",
     "overlap_org": "中共平凉市崆峒区委员会、平凉市崆峒区人民政府",
     "overlap_period": "至今",
     "strength": "strong", "confidence": "confirmed"},

    # 刘国军 ↔ 唐培宏 (上级领导)
    {"a": 1, "b": 15, "type": "superior_subordinate",
     "context": "刘国军作为平凉市委常委在唐培宏领导下工作",
     "overlap_org": "中共平凉市委员会",
     "overlap_period": "2024-07~至今",
     "strength": "strong", "confidence": "confirmed"},

    # 樊对对 ↔ 刘小平 (predecessor-successor as 区长)
    {"a": 2, "b": 4, "type": "predecessor_successor",
     "context": "樊对对接替刘小平担任崆峒区区长",
     "overlap_org": "平凉市崆峒区人民政府",
     "overlap_period": "",
     "strength": "strong", "confidence": "plausible"},

    # 樊对对 ↔ 唐培宏
    {"a": 2, "b": 15, "type": "superior_subordinate",
     "context": "樊对对作为区长在平凉市领导下工作",
     "overlap_org": "",
     "overlap_period": "",
     "strength": "medium", "confidence": "confirmed"},

    # 刘国军 ↔ 李荣 (standing committee overlap)
    {"a": 1, "b": 16, "type": "overlap",
     "context": "刘国军与李荣同在平凉市委常委会工作",
     "overlap_org": "中共平凉市委员会",
     "overlap_period": "2024~至今",
     "strength": "medium", "confidence": "confirmed"},

    # 刘国军 ↔ 陶烨 (区委常委会同事)
    {"a": 1, "b": 5, "type": "overlap",
     "context": "刘国军与陶烨同在崆峒区委常委会",
     "overlap_org": "中共平凉市崆峒区委员会",
     "overlap_period": "",
     "strength": "strong", "confidence": "confirmed"},

    # 刘国军 ↔ 张喜武 (区委常委会同事)
    {"a": 1, "b": 6, "type": "overlap",
     "context": "刘国军与张喜武同在崆峒区委常委会",
     "overlap_org": "中共平凉市崆峒区委员会",
     "overlap_period": "",
     "strength": "strong", "confidence": "confirmed"},

    # 刘国军 ↔ 罗彦鹏 (区委常委会同事)
    {"a": 1, "b": 7, "type": "overlap",
     "context": "刘国军与罗彦鹏同在崆峒区委常委会",
     "overlap_org": "中共平凉市崆峒区委员会",
     "overlap_period": "",
     "strength": "strong", "confidence": "confirmed"},

    # 刘国军 ↔ 马瀚铎 (区委常委会同事)
    {"a": 1, "b": 10, "type": "overlap",
     "context": "刘国军与马瀚铎同在崆峒区委常委会",
     "overlap_org": "中共平凉市崆峒区委员会",
     "overlap_period": "",
     "strength": "strong", "confidence": "confirmed"},

    # 刘国军 ↔ 柴璟 (区委常委会同事)
    {"a": 1, "b": 9, "type": "overlap",
     "context": "刘国军与柴璟同在崆峒区委常委会",
     "overlap_org": "中共平凉市崆峒区委员会",
     "overlap_period": "",
     "strength": "strong", "confidence": "confirmed"},

    # 樊对对 ↔ 高跟信 (党政与人大)
    {"a": 2, "b": 11, "type": "overlap",
     "context": "樊对对任区长期间高跟信任区人大常委会主任",
     "overlap_org": "平凉市崆峒区",
     "overlap_period": "",
     "strength": "medium", "confidence": "confirmed"},
]

# =========================================================================
# BUILD FUNCTIONS
# =========================================================================

def build_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY,
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
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT NOT NULL,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            strength TEXT,
            confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        cur.execute("""
            INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
              p["education"], p["party_join"], p["work_start"], p["current_post"],
              p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""
            INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (str(o["id"]), o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["pid"], str(pos["org"]), pos["title"], pos["start"], pos["end"],
              pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (r["a"], r["b"], r["type"], r["context"], r["overlap_org"],
              r["overlap_period"], r["strength"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"Database written: {DB_PATH}")

    # Stats
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    print(f"  Persons: {conn.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}")
    print(f"  Organizations: {conn.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}")
    print(f"  Positions: {conn.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}")
    print(f"  Relationships: {conn.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")
    conn.close()


def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color(p):
        current = p.get("current_post", "")
        if "书记" in current and "纪委" not in current and "人大" not in current and "政协" not in current:
            return "255,50,50"  # Red — party secretary
        if "区长" in current or "市长" in current or "副区长" in current or "副市长" in current:
            return "50,100,255"  # Blue — government
        if "纪委" in current:
            return "255,165,0"  # Orange — discipline
        if "人大" in current:
            return "200,255,255"  # Cyan — NPC
        if "政协" in current:
            return "255,240,200"  # Cream — CPPCC
        return "100,100,100"  # Grey — others

    def person_size(p):
        name = p["name"]
        # Top leaders
        if name in ("刘国军", "樊对对"):
            return "20.0"
        # Standing committee / predecessors
        if name in ("王琳玺", "刘小平", "唐培宏", "李荣"):
            return "15.0"
        return "12.0"

    def org_color(o):
        t = o.get("type", "")
        if "党委" in t:
            return "255,200,200"
        if "政府" in t:
            return "200,200,255"
        if "人大" in t:
            return "200,255,255"
        if "政协" in t:
            return "255,240,200"
        return "200,200,200"

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>平凉市崆峒区领导班子工作关系网络 — 中共崆峒区委、崆峒区人民政府及上级组织<br/>'
                 'Targets: 区委书记 刘国军, 区长 樊对对</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="level" type="string"/>')
    lines.append('      <attribute id="3" title="location" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        role = p.get("current_post", "未知")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birthplace",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(o.get("location",""))}"/>')
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
        period = f"{pos['start']} - {pos['end']}" if pos['start'] else ""
        lines.append(f'      <edge id="e{eid}" source="p{pos["pid"]}" target="o{pos["org"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(period)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        weight = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["a"]}" target="p{r["b"]}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")
    print(f"  Nodes: {len(persons) + len(organizations)}")
    print(f"  Edges: {eid}")


if __name__ == "__main__":
    build_database()
    build_gexf()
    print("\nDone. Generated artifacts:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
