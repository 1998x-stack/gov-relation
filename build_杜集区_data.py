#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 杜集区 (Duji District, Huaibei, Anhui) leadership network.
Generated: 2026-07-15
Task: anhui_杜集区 - 区委书记 & 区长
Sources:
  - https://www.hbdj.gov.cn/ (杜集区人民政府官方网站, 领导活动和党代会报道, accessed 2026-07-15)
  - https://www.hbdj.gov.cn/xwzx/djyw/60923792.html (九届一次全会选举结果, 2026-06-27)
  - https://www.hbdj.gov.cn/xwzx/djyw/60923763.html (第九次党代会开幕, 魏辉主持, 2026-06-26)
  - https://www.hbdj.gov.cn/xwzx/djyw/60923275.html (区委书记郑晓军调研, 2026-06-12)
  - https://www.hbdj.gov.cn/xwzx/djyw/60923025.html (郑晓军任人武部党委第一书记, 2026-06-05)
  - https://www.hbdj.gov.cn/xwzx/djyw/60924123.html (两优一先表彰大会, 2026-07-02)
  - https://www.hbdj.gov.cn/xwzx/djyw/60924372.html (淮北师范大学调研座谈, 2026-07-14)
  - https://zh.wikipedia.org/wiki/杜集区 (行政区划信息, accessed 2026-07-15)

Confidence: Current roles confirmed from official government news and the 九届一次全会
report (2026-06-26). Biographical details are partial due to Baidu Baike being blocked.
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
# If running from staging temp dir (data/tmp/anhui_杜集区/), go up to repo root
if "data/tmp" in BASE:
    BASE = os.path.dirname(os.path.dirname(os.path.dirname(BASE)))
STAGING = os.path.join(BASE, "data/tmp/anhui_杜集区")
DB_PATH = os.path.join(STAGING, "杜集区_network.db")
GEXF_PATH = os.path.join(STAGING, "杜集区_network.gexf")

# ── DATA ──────────────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "郑晓军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杜集区委书记",
        "current_org": "中共杜集区委员会",
        "source": "https://www.hbdj.gov.cn/xwzx/djyw/60923792.html (九届一次全会选举); "
                 "https://www.hbdj.gov.cn/xwzx/djyw/60923025.html (任人武部第一书记)",
        "notes": "杜集区委书记。2026年6月26日当选中共杜集区第九届委员会书记。"
                 "2026年6月5日任杜集区人武部党委委员、党委第一书记。"
                 "此前任杜集区委副书记、区长(推断)。详细履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "魏辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杜集区委副书记、区长",
        "current_org": "杜集区人民政府",
        "source": "https://www.hbdj.gov.cn/xwzx/djyw/60923792.html (九届一次全会选举); "
                 "https://www.hbdj.gov.cn/xwzx/djyw/60923763.html (主持第九次党代会)",
        "notes": "杜集区委副书记、区长。2026年6月26日当选中共杜集区第九届委员会副书记。"
                 "主持杜集区第九次党代会开幕大会。详细履历待补充。",
        "confidence": "confirmed"
    },
    # ── 区委领导 ──
    {
        "id": 3,
        "name": "魏宾",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杜集区委副书记",
        "current_org": "中共杜集区委员会",
        "source": "https://www.hbdj.gov.cn/xwzx/djyw/60923792.html (九届一次全会选举); "
                 "https://www.hbdj.gov.cn/xwzx/djyw/60924372.html (主持座谈)",
        "notes": "杜集区委副书记。2026年6月26日当选中共杜集区第九届委员会副书记。"
                 "2026年7月13日主持淮北师范大学调研座谈。详细履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 4,
        "name": "陈涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杜集区委常委",
        "current_org": "中共杜集区委员会",
        "source": "https://www.hbdj.gov.cn/xwzx/djyw/60923792.html (九届一次全会选举)",
        "notes": "2026年6月26日当选中共杜集区第九届委员会常委。具体职务待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 5,
        "name": "陆松平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杜集区委常委",
        "current_org": "中共杜集区委员会",
        "source": "https://www.hbdj.gov.cn/xwzx/djyw/60923792.html (九届一次全会选举)",
        "notes": "2026年6月26日当选中共杜集区第九届委员会常委。具体职务待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 6,
        "name": "蒋影",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杜集区委常委",
        "current_org": "中共杜集区委员会",
        "source": "https://www.hbdj.gov.cn/xwzx/djyw/60923792.html (九届一次全会选举)",
        "notes": "2026年6月26日当选中共杜集区第九届委员会常委。具体职务待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 7,
        "name": "徐善鲲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杜集区委常委",
        "current_org": "中共杜集区委员会",
        "source": "https://www.hbdj.gov.cn/xwzx/djyw/60923792.html (九届一次全会选举); "
                 "https://www.hbdj.gov.cn/xwzx/djyw/60923275.html (陪同郑晓军调研)",
        "notes": "2026年6月26日当选中共杜集区第九届委员会常委。"
                 "2026年6月11日陪同区委书记郑晓军赴杜集经开区督导调研。具体职务待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 8,
        "name": "李涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杜集区委常委",
        "current_org": "中共杜集区委员会",
        "source": "https://www.hbdj.gov.cn/xwzx/djyw/60923792.html (九届一次全会选举)",
        "notes": "2026年6月26日当选中共杜集区第九届委员会常委。具体职务待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 9,
        "name": "文婷婷",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杜集区委常委",
        "current_org": "中共杜集区委员会",
        "source": "https://www.hbdj.gov.cn/xwzx/djyw/60923792.html (九届一次全会选举)",
        "notes": "2026年6月26日当选中共杜集区第九届委员会常委。具体职务待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 10,
        "name": "许家升",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杜集区委常委、区人武部上校政治委员",
        "current_org": "杜集区人民武装部",
        "source": "https://www.hbdj.gov.cn/xwzx/djyw/60923792.html (九届一次全会选举); "
                 "https://www.hbdj.gov.cn/xwzx/djyw/60923025.html (人武部任职大会)",
        "notes": "2026年6月26日当选中共杜集区第九届委员会常委。"
                 "任杜集区人武部上校政治委员。主持2026年6月5日人武部任职大会。",
        "confidence": "confirmed"
    },
    {
        "id": 11,
        "name": "郭守厚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "杜集区委常委",
        "current_org": "中共杜集区委员会",
        "source": "https://www.hbdj.gov.cn/xwzx/djyw/60923792.html (九届一次全会选举)",
        "notes": "2026年6月26日当选中共杜集区第九届委员会常委。具体职务待补充。",
        "confidence": "confirmed"
    },
    # ── 前主要领导 ──
    {
        "id": 12,
        "name": "郑晓军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前区长（现任区委书记）",
        "current_org": "杜集区人民政府",
        "source": "推断：郑晓军任区委书记前的职务",
        "notes": "郑晓军在2026年6月任区委书记前应为杜集区区长。"
                 "详细任职时间线待补充。",
        "confidence": "plausible"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中国共产党杜集区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中国共产党淮北市委员会",
        "location": "安徽省淮北市杜集区"
    },
    {
        "id": 2,
        "name": "杜集区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "淮北市人民政府",
        "location": "安徽省淮北市杜集区"
    },
    {
        "id": 3,
        "name": "杜集区人民武装部",
        "type": "政府",
        "level": "县处级",
        "parent": "淮北军分区",
        "location": "安徽省淮北市杜集区"
    },
    {
        "id": 4,
        "name": "杜集区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中国共产党杜集区委员会",
        "location": "安徽省淮北市杜集区"
    },
    {
        "id": 5,
        "name": "杜集区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "杜集区",
        "location": "安徽省淮北市杜集区"
    },
    {
        "id": 6,
        "name": "政协杜集区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "杜集区",
        "location": "安徽省淮北市杜集区"
    },
    {
        "id": 7,
        "name": "杜集区纪委监委",
        "type": "党委",
        "level": "县处级",
        "parent": "中国共产党杜集区委员会",
        "location": "安徽省淮北市杜集区"
    },
]

positions = [
    # 郑晓军 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记、区人武部党委第一书记", "start": "2026-06", "end": "present", "rank": "县处级正职", "note": "2026年6月26日当选九届区委书记"},
    {"person_id": 1, "org_id": 3, "title": "区人武部党委第一书记", "start": "2026-06", "end": "present", "rank": "县处级正职", "note": "2026年6月5日任职通知"},
    # 魏辉 — 区长
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "rank": "县处级正职", "note": "2026年6月26日当选九届区委副书记"},
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "present", "rank": "县处级正职", "note": "主持杜集区第九次党代会"},
    # 魏宾 — 区委副书记
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "rank": "县处级副职", "note": "2026年6月26日当选九届区委副书记"},
    # 陈涛 — 常委
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "县处级副职", "note": "2026年6月26日当选九届区委常委"},
    # 陆松平 — 常委
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "县处级副职", "note": "2026年6月26日当选九届区委常委"},
    # 蒋影 — 常委
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "县处级副职", "note": "2026年6月26日当选九届区委常委"},
    # 徐善鲲 — 常委
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "县处级副职", "note": "2026年6月26日当选九届区委常委"},
    # 李涛 — 常委
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "县处级副职", "note": "2026年6月26日当选九届区委常委"},
    # 文婷婷 — 常委
    {"person_id": 9, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "县处级副职", "note": "2026年6月26日当选九届区委常委"},
    # 许家升 — 人武部政委
    {"person_id": 10, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "县处级副职", "note": "2026年6月26日当选九届区委常委"},
    {"person_id": 10, "org_id": 3, "title": "区人武部上校政治委员", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 郭守厚 — 常委
    {"person_id": 11, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "县处级副职", "note": "2026年6月26日当选九届区委常委"},
]

relationships = [
    # 郑晓军 ↔ 魏辉
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记与区长，区委领导班子正副搭档",
        "overlap_org": "中共杜集区委员会",
        "overlap_period": "2026-06至今",
        "confidence": "confirmed"
    },
    # 郑晓军 ↔ 魏宾
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "区委书记与区委副书记，区委领导班子",
        "overlap_org": "中共杜集区委员会",
        "overlap_period": "2026-06至今",
        "confidence": "confirmed"
    },
    # 魏辉 ↔ 魏宾
    {
        "person_a": 2,
        "person_b": 3,
        "type": "overlap",
        "context": "两位区委副书记，区委领导班子中协作",
        "overlap_org": "中共杜集区委员会",
        "overlap_period": "2026-06至今",
        "confidence": "confirmed"
    },
    # 郑晓军 — 前任区长 → 现任书记
    {
        "person_a": 12,
        "person_b": 1,
        "type": "predecessor_successor",
        "context": "郑晓军本人：前任区长晋升为现任区委书记（同一个人）",
        "overlap_org": "杜集区人民政府",
        "overlap_period": "推断",
        "confidence": "plausible"
    },
    # 全体常委与书记的班子关系
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "区委书记与区委常委，区委领导班子",
        "overlap_org": "中共杜集区委员会",
        "overlap_period": "2026-06至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "区委书记与区委常委，区委领导班子",
        "overlap_org": "中共杜集区委员会",
        "overlap_period": "2026-06至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "区委书记与区委常委，区委领导班子",
        "overlap_org": "中共杜集区委员会",
        "overlap_period": "2026-06至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 1,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "区委书记与区委常委（徐善鲲多次陪同调研）",
        "overlap_org": "中共杜集区委员会",
        "overlap_period": "2026-06至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 1,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "区委书记与区委常委，区委领导班子",
        "overlap_org": "中共杜集区委员会",
        "overlap_period": "2026-06至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 1,
        "person_b": 9,
        "type": "superior_subordinate",
        "context": "区委书记与区委常委，区委领导班子",
        "overlap_org": "中共杜集区委员会",
        "overlap_period": "2026-06至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 1,
        "person_b": 10,
        "type": "superior_subordinate",
        "context": "区委书记与人武部政委，人武部党委第一书记与常委",
        "overlap_org": "中共杜集区委员会",
        "overlap_period": "2026-06至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 1,
        "person_b": 11,
        "type": "superior_subordinate",
        "context": "区委书记与区委常委，区委领导班子",
        "overlap_org": "中共杜集区委员会",
        "overlap_period": "2026-06至今",
        "confidence": "confirmed"
    },
]


# ── build functions ──────────────────────────────────────────────────────

def create_database(db_path):
    """Create SQLite database with persons, organizations, positions, relationships."""
    os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
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
            source TEXT,
            notes TEXT,
            confidence TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""
            INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace,
                native_place, education, party_join, work_start, current_post, current_org,
                source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
              p.get("birth", ""), p.get("birthplace", ""), p.get("native_place", ""),
              p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
              p.get("current_post", ""), p.get("current_org", ""),
              p.get("source", ""), p.get("notes", ""), p.get("confidence", "")))

    for o in organizations:
        c.execute("""
            INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
              o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos.get("title", ""),
              pos.get("start", ""), pos.get("end", ""), pos.get("rank", ""),
              pos.get("note", "")))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r.get("type", ""),
              r.get("context", ""), r.get("overlap_org", ""),
              r.get("overlap_period", ""), r.get("confidence", "")))

    conn.commit()
    conn.close()


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return 'r,g,b' for a person node."""
    post = p.get("current_post", "")
    name = p.get("name", "")
    if "书记" in post and "纪委" not in post:
        return "255,50,50"    # Red — party secretary
    elif "区长" in post or "市长" in post or "县长" in post:
        return "50,100,255"   # Blue — government leader
    elif "纪委" in post:
        return "255,165,0"    # Orange — discipline
    else:
        return "100,100,100"  # Grey — other


def is_top_leader(p):
    post = p.get("current_post", "")
    return "书记" in post or "区长" in post or "县长" in post


def org_color(o):
    t = o.get("type", "")
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")


def generate_gexf(gexf_path):
    """Generate GEXF 1.3 graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>杜集区领导班子工作关系网络 — District Party Secretary, Mayor, and leadership team</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: Persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        pid = f"p{p['id']}"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"] + "(" + p.get("current_post","") + ")")}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("confidence", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: Organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos.get("title", ""))}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r.get("context", ""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("confidence", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    os.makedirs(os.path.dirname(gexf_path) or ".", exist_ok=True)
    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ── main ─────────────────────────────────────────────────────────────────

def main():
    print(f"=== 杜集区 Leadership Network Data Builder ===")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"Staging: {STAGING}")
    print()

    # 1. Database
    print(f"Creating database: {DB_PATH}")
    create_database(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        count = c.fetchone()[0]
        print(f"  {table}: {count} rows")
    conn.close()

    # 2. GEXF
    print(f"\nCreating GEXF: {GEXF_PATH}")
    generate_gexf(GEXF_PATH)
    gexf_size = os.path.getsize(GEXF_PATH)
    print(f"  GEXF file size: {gexf_size} bytes")

    # 3. Summary
    print(f"\n=== Summary ===")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")

    for p in persons:
        conf = p.get("confidence", "")
        print(f"  - {p['name']}: {p.get('current_post', '')} ({conf})")

    print(f"\nDone. Files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    main()
