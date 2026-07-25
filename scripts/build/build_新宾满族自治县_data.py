#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 新宾满族自治县, 抚顺市, 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_新宾满族自治县
Level: 县（自治县）
Targets: 县委书记 & 县长

Research status: WEB ACCESS DEGRADED
  - Exa API rate-limited (free tier exhausted)
  - Baidu: 403 captcha block
  - Official 新宾满族自治县人民政府网站 (www.xinbin.gov.cn): accessible via HTTP with GBK encoding
  - Leadership data confirmed via official county site's 领导之窗 page + multiple news articles

Current officeholders:
  - 县委书记: 郑毅 (confirmed via official news articles, earliest reference 2026-01-14)
  - 县委副书记、县长: 杨吉国 (confirmed via official leadership page + news articles 2023-2026)

Note on web access:
  - 新宾满族自治县人民政府网站 was accessible via direct Python HTTP requests
    with GB2312/GBK encoding. HTTPS was unreachable but HTTP worked.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
for parent_count in [3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "新宾满族自治县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
DB_PATH = _CURRENT_DIR / f"{SLUG}_network.db"
GEXF_PATH = _CURRENT_DIR / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    # ── 县委书记 ──
    {
        "id": 1,
        "name": "郑毅",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中国共产党新宾满族自治县委员会",
        "source": "http://www.xinbin.gov.cn/ins.asp?s=11&i=17892",
    },
    # ── 县委副书记、县长 ──
    {
        "id": 2,
        "name": "杨吉国",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "新宾满族自治县人民政府",
        "source": "http://www.xinbin.gov.cn/ld.asp?s=54",
    },
    # ── 县委常委、分管日常工作的副县长 ──
    {
        "id": 3,
        "name": "江艳梅",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、分管日常工作的副县长",
        "current_org": "新宾满族自治县人民政府",
        "source": "http://www.xinbin.gov.cn/ld.asp?s=54",
    },
    # ── 县委常委、副县长（挂职） ──
    {
        "id": 4,
        "name": "高升",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长（挂职）",
        "current_org": "新宾满族自治县人民政府",
        "source": "http://www.xinbin.gov.cn/ld.asp?s=54",
    },
    # ── 副县长 ──
    {
        "id": 5,
        "name": "车少辉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "新宾满族自治县人民政府",
        "source": "http://www.xinbin.gov.cn/ld.asp?s=54",
    },
    # ── 副县长 ──
    {
        "id": 6,
        "name": "佟震",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "新宾满族自治县人民政府",
        "source": "http://www.xinbin.gov.cn/ld.asp?s=54",
    },
    # ── 副县长 ──
    {
        "id": 7,
        "name": "崔正勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "新宾满族自治县人民政府",
        "source": "http://www.xinbin.gov.cn/ld.asp?s=54",
    },
    # ── 县人大常委会主任 ──
    {
        "id": 8,
        "name": "谢大利",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "新宾满族自治县人大常委会",
        "source": "http://www.xinbin.gov.cn/ins.asp?s=11&i=17981",
    },
    # ── 县政协主席 ──
    {
        "id": 9,
        "name": "张报吉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协新宾满族自治县委员会",
        "source": "http://www.xinbin.gov.cn/ins.asp?s=11&i=17981",
    },
    # ── 前任县委书记（2023年以前）──
    {
        "id": 10,
        "name": "王景涛",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县委书记（已离任）",
        "current_org": "中国共产党新宾满族自治县委员会",
        "source": "http://www.xinbin.gov.cn/search.asp?sname=%CD%F5%BE%B0%CC%CE",
    },
    # ── 县领导（陪同接待，可能为县委办主任等）──
    {
        "id": 11,
        "name": "石磊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（待确认具体职务）",
        "current_org": "新宾满族自治县",
        "source": "http://www.xinbin.gov.cn/ins.asp?s=11&i=17892",
    },
    # ── 县领导 ──
    {
        "id": 12,
        "name": "孟宪宾",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（待确认具体职务）",
        "current_org": "新宾满族自治县",
        "source": "http://www.xinbin.gov.cn/ins.asp?s=11&i=17892",
    },
    # ── 县领导 ──
    {
        "id": 13,
        "name": "于国徽",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（待确认具体职务）",
        "current_org": "新宾满族自治县",
        "source": "http://www.xinbin.gov.cn/ins.asp?s=11&i=17892",
    },
    # ── 县领导 ──
    {
        "id": 14,
        "name": "高远",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（待确认具体职务）",
        "current_org": "新宾满族自治县",
        "source": "http://www.xinbin.gov.cn/ins.asp?s=8&i=18374",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中国共产党新宾满族自治县委员会", "type": "党委", "level": "县", "parent": "中国共产党抚顺市委员会", "location": "新宾满族自治县"},
    {"id": 2, "name": "新宾满族自治县人民政府", "type": "政府", "level": "县", "parent": "抚顺市人民政府", "location": "新宾满族自治县"},
    {"id": 3, "name": "新宾满族自治县人大常委会", "type": "人大", "level": "县", "parent": "抚顺市人大常委会", "location": "新宾满族自治县"},
    {"id": 4, "name": "政协新宾满族自治县委员会", "type": "政协", "level": "县", "parent": "政协抚顺市委员会", "location": "新宾满族自治县"},
    {"id": 5, "name": "中国共产党新宾满族自治县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共抚顺市纪律检查委员会", "location": "新宾满族自治县"},
    {"id": 6, "name": "新宾满族自治县公安局", "type": "政府", "level": "县", "parent": "新宾满族自治县人民政府", "location": "新宾满族自治县"},
    {"id": 7, "name": "新宾满族自治县发展和改革局", "type": "政府", "level": "县", "parent": "新宾满族自治县人民政府", "location": "新宾满族自治县"},
    {"id": 8, "name": "新宾满族自治县财政局", "type": "政府", "level": "县", "parent": "新宾满族自治县人民政府", "location": "新宾满族自治县"},
    {"id": 9, "name": "新宾满族自治县人力资源和社会保障局", "type": "政府", "level": "县", "parent": "新宾满族自治县人民政府", "location": "新宾满族自治县"},
    {"id": 10, "name": "新宾满族自治县农业农村局", "type": "政府", "level": "县", "parent": "新宾满族自治县人民政府", "location": "新宾满族自治县"},
    {"id": 11, "name": "新宾满族自治县教育局", "type": "政府", "level": "县", "parent": "新宾满族自治县人民政府", "location": "新宾满族自治县"},
    {"id": 12, "name": "新宾满族自治县卫生健康局", "type": "政府", "level": "县", "parent": "新宾满族自治县人民政府", "location": "新宾满族自治县"},
    {"id": 13, "name": "新宾满族自治县交通运输局", "type": "政府", "level": "县", "parent": "新宾满族自治县人民政府", "location": "新宾满族自治县"},
    {"id": 14, "name": "新宾满族自治县住房和城乡建设局", "type": "政府", "level": "县", "parent": "新宾满族自治县人民政府", "location": "新宾满族自治县"},
    {"id": 15, "name": "新宾满族自治县市场监督管理局", "type": "政府", "level": "县", "parent": "新宾满族自治县人民政府", "location": "新宾满族自治县"},
    {"id": 16, "name": "新宾满族自治县工业和信息化局", "type": "政府", "level": "县", "parent": "新宾满族自治县人民政府", "location": "新宾满族自治县"},
    {"id": 17, "name": "新宾满族自治县自然资源局", "type": "政府", "level": "县", "parent": "新宾满族自治县人民政府", "location": "新宾满族自治县"},
    {"id": 18, "name": "新宾满族自治县水务局", "type": "政府", "level": "县", "parent": "新宾满族自治县人民政府", "location": "新宾满族自治县"},
    {"id": 19, "name": "新宾满族自治县应急管理局", "type": "政府", "level": "县", "parent": "新宾满族自治县人民政府", "location": "新宾满族自治县"},
    {"id": 20, "name": "新宾满族自治县司法局", "type": "政府", "level": "县", "parent": "新宾满族自治县人民政府", "location": "新宾满族自治县"},
    {"id": 21, "name": "新宾满族自治县文化旅游和广播电视局", "type": "政府", "level": "县", "parent": "新宾满族自治县人民政府", "location": "新宾满族自治县"},
    {"id": 22, "name": "新宾满族自治县林业和草原局", "type": "政府", "level": "县", "parent": "新宾满族自治县人民政府", "location": "新宾满族自治县"},
    {"id": 23, "name": "新宾满族自治县统计局", "type": "政府", "level": "县", "parent": "新宾满族自治县人民政府", "location": "新宾满族自治县"},
    {"id": 24, "name": "新宾满族自治县融媒体中心", "type": "事业单位", "level": "县", "parent": "新宾满族自治县人民政府", "location": "新宾满族自治县"},
    {"id": 25, "name": "新宾满族自治县营商环境建设局", "type": "政府", "level": "县", "parent": "新宾满族自治县人民政府", "location": "新宾满族自治县"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 郑毅 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正处级", "note": "中共新宾满族自治县委书记，2026年1月起有公开活动记录"},
    # 杨吉国 - 县委副书记、县长
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "正处级", "note": "新宾满族自治县人民政府党组书记、县长"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 江艳梅 - 县委常委、常务副县长
    {"person_id": 3, "org_id": 2, "title": "常务副县长（分管日常工作）", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 高升 - 县委常委、副县长（挂职）
    {"person_id": 4, "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": "挂职"},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": "挂职"},
    # 车少辉 - 副县长
    {"person_id": 5, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "带队督导企业安全生产工作"},
    # 佟震 - 副县长
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "陪同县委书记接待群众"},
    # 崔正勇 - 副县长
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 谢大利 - 县人大常委会主任
    {"person_id": 8, "org_id": 3, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": "列席县委常委会议"},
    # 张报吉 - 县政协主席
    {"person_id": 9, "org_id": 4, "title": "县政协主席", "start": "", "end": "present", "rank": "正处级", "note": "列席县委常委会议"},
    # 王景涛 - 前任县委书记
    {"person_id": 10, "org_id": 1, "title": "县委书记（前任）", "start": "", "end": "", "rank": "正处级", "note": "2023年3月仍有公开活动，后由郑毅接任"},
    # 石磊 - 县领导
    {"person_id": 11, "org_id": 1, "title": "县领导（待确认）", "start": "", "end": "present", "rank": "", "note": "陪同县委书记接待群众"},
    # 孟宪宾 - 县领导
    {"person_id": 12, "org_id": 1, "title": "县领导（待确认）", "start": "", "end": "present", "rank": "", "note": "陪同县委书记接待群众"},
    # 于国徽 - 县领导
    {"person_id": 13, "org_id": 1, "title": "县领导（待确认）", "start": "", "end": "present", "rank": "", "note": "陪同县委书记接待群众"},
    # 高远 - 县领导
    {"person_id": 14, "org_id": 1, "title": "县领导（待确认）", "start": "", "end": "present", "rank": "", "note": "陪同县委书记调研"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 郑毅 <-> 杨吉国 - 党政主要负责人搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长搭档，多次共同出席会见、调研活动",
     "overlap_org": "新宾满族自治县", "overlap_period": "至2026年7月"},
    # 郑毅 <-> 江艳梅
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记与常务副县长",
     "overlap_org": "新宾满族自治县", "overlap_period": "至2026年7月"},
    # 郑毅 <-> 佟震 - 陪同接待群众
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "县委书记与副县长，共同接待来访群众",
     "overlap_org": "新宾满族自治县", "overlap_period": "2026年1月"},
    # 郑毅 <-> 石磊 - 陪同活动
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate",
     "context": "县委书记与县领导，共同接待来访群众",
     "overlap_org": "新宾满族自治县", "overlap_period": "2026年1月"},
    # 郑毅 <-> 孟宪宾
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate",
     "context": "县委书记与县领导，共同接待来访群众",
     "overlap_org": "新宾满族自治县", "overlap_period": "2026年1月"},
    # 郑毅 <-> 于国徽
    {"person_a": 1, "person_b": 13, "type": "superior_subordinate",
     "context": "县委书记与县领导，共同接待来访群众",
     "overlap_org": "新宾满族自治县", "overlap_period": "2026年1月"},
    # 郑毅 <-> 高远 - 陪同调研
    {"person_a": 1, "person_b": 14, "type": "superior_subordinate",
     "context": "县委书记与县领导，共同调研蓝莓产业",
     "overlap_org": "新宾满族自治县", "overlap_period": "2026年7月"},
    # 杨吉国 <-> 江艳梅 - 县长与常务副县长
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "县长与常务副县长",
     "overlap_org": "新宾满族自治县人民政府", "overlap_period": "至2026年7月"},
    # 杨吉国 <-> 车少辉 - 县长与副县长
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "县长与副县长",
     "overlap_org": "新宾满族自治县人民政府", "overlap_period": "至2026年7月"},
    # 杨吉国 <-> 佟震
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "县长与副县长",
     "overlap_org": "新宾满族自治县人民政府", "overlap_period": "至2026年7月"},
    # 杨吉国 <-> 崔正勇
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "县长与副县长",
     "overlap_org": "新宾满族自治县人民政府", "overlap_period": "至2026年7月"},
    # 郑毅 <-> 王景涛 - 前后任
    {"person_a": 1, "person_b": 10, "type": "predecessor_successor",
     "context": "郑毅接替王景涛担任新宾县委书记",
     "overlap_org": "中国共产党新宾满族自治县委员会", "overlap_period": "2023-2025年间交接"},
    # 谢大利 <-> 郑毅 - 人大主任与县委书记
    {"person_a": 8, "person_b": 1, "type": "superior_subordinate",
     "context": "县人大常委会主任列席县委常委会议",
     "overlap_org": "新宾满族自治县", "overlap_period": "至2026年7月"},
    # 张报吉 <-> 郑毅 - 政协主席与县委书记
    {"person_a": 9, "person_b": 1, "type": "superior_subordinate",
     "context": "县政协主席列席县委常委会议",
     "overlap_org": "新宾满族自治县", "overlap_period": "至2026年7月"},
    # 江艳梅 <-> 高升 - 同为县委常委
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "同为县委常委",
     "overlap_org": "中国共产党新宾满族自治县委员会", "overlap_period": "至2026年7月"},
]

# ── Build ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Building {SLUG} data...")

    # Ensure staging dir exists
    _CURRENT_DIR.mkdir(parents=True, exist_ok=True)

    # DB
    print(f"  DB: {DB_PATH}")
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
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
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            "end" TEXT,
            rank TEXT,
            note TEXT
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT
        );
    """)

    for p in persons:
        cur.execute(
            "INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]),
        )

    for o in organizations:
        cur.execute(
            "INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]),
        )

    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start, \"end\", rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]),
        )

    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]),
        )

    conn.commit()
    conn.close()
    print(f"  DB written: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # GEXF
    print(f"  GEXF: {GEXF_PATH}")

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    from datetime import datetime as dt

    # Person colors by role
    def person_color(p):
        if p["id"] == 1:   # 县委书记
            return "255,50,50"
        elif p["id"] == 2: # 县长
            return "50,100,255"
        elif p["id"] == 10: # 前任县委书记
            return "200,50,50"
        else:
            return "100,100,100"

    # Organization color by type
    def org_color(o):
        colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "人大": "200,255,255",
            "政协": "255,240,200",
            "群团": "255,220,255",
            "事业单位": "220,220,220",
        }
        return colors.get(o["type"], "200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{dt.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append(f'    <description>新宾满族自治县领导班子关系网络 - {SLUG} leadership network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="level" type="string"/>')
    lines.append('      <attribute id="3" title="location" type="string"/>')
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
        c = person_color(p)
        sz = "20.0" if p["id"] in (1, 2, 10) else "12.0"
        title = esc(p["current_post"])
        name = esc(p["name"])
        lines.append(f'      <node id="p{p["id"]}" label="{name}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{title}"/>')
        lines.append(f'          <attvalue for="2" value="县"/>')
        lines.append(f'          <attvalue for="3" value="新宾满族自治县"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        name = esc(o["name"])
        lines.append(f'      <node id="o{o["id"]}" label="{name}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(o["location"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edge: person <-> organization (worked at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("note", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{pos["start"] or "?"} - {pos["end"] or "?"}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edge: person <-> person (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
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
    print(f"  GEXF written: {eid} edges")

    print(f"Done: {SLUG}")
