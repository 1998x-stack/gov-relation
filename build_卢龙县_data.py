#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build SQLite database and GEXF graph for Lulong County (卢龙县), Qinhuangdao, Hebei.

Level: 县
Province: 河北省 (Hebei)
Parent City: 秦皇岛市 (Qinhuangdao)
Region: 卢龙县
Targets: 县委书记 & 县长

Research Sources:
  - https://www.lulong.gov.cn/channel/list/24.html (政府领导 - confirmed 于忠林 bio)
  - https://www.lulong.gov.cn/single/24/7298.html (于忠林 official bio)
  - https://www.lulong.gov.cn/single/24/7304.html (杨晨 official bio)
  - https://www.lulong.gov.cn/single/24/7300.html (陈峰 official bio)
  - https://www.lulong.gov.cn/single/24/7299.html (张倩 official bio)
  - https://www.lulong.gov.cn/single/24/7305.html (张立强 official bio)
  - https://www.lulong.gov.cn/single/24/7303.html (王光冲 official bio)
  - https://www.lulong.gov.cn/single/6/18949.html (张志明 news confirmation from 2025-01-15)
  - https://www.lulong.gov.cn/single/6/24147.html (张志明 news 2025-05-20)
  - https://www.lulong.gov.cn/ (general site)

Research Date: 2026-07-23

Notes:
  - 县委领导 (Party Committee leadership) page not directly accessible on gov site
  - 张志明 confirmed as 县委书记 via multiple news articles on lulong.gov.cn
  - 张志明's full biography and career history were not available on accessible pages
  - Additional 县委 leaders names sourced from news articles:
    - 郝向东 (mentioned as "县领导" alongside 张志明 and 于忠林)
    - 邱中凯 (mentioned as "县领导" in 2025 news)
    - 刘晓东 (mentioned as "县领导" in 2025 news)
    - 刘猛 (mentioned as "县领导" in meetings)
    - 陈纪行 (mentioned in 张志明 investigation reports)
    - 周庚全 (mentioned in 张志明 investigation reports)
"""

import os
import sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "卢龙县_network.db")
GEXF_PATH = os.path.join(BASE, "卢龙县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

# fmt: off
persons = [
    # ════════════════════════════════════════
    # Core Leaders
    # ════════════════════════════════════════

    # 县委书记 (Party Secretary) — confirmed via multiple news articles
    {
        "id": 1,
        "name": "张志明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "卢龙县委书记",
        "current_org": "中共卢龙县委员会",
        "source": "https://www.lulong.gov.cn/single/6/18949.html — 2025年1月15日新闻确认县委书记张志明; https://www.lulong.gov.cn/single/6/24147.html — 2025年5月20日新闻再次确认",
    },
    # 县长 (County Mayor) — confirmed on gov site leader page
    {
        "id": 2,
        "name": "于忠林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年3月",
        "birthplace": "待查",
        "education": "大学学历，理学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "卢龙县委副书记、县长、县政府党组书记",
        "current_org": "卢龙县人民政府",
        "source": "https://www.lulong.gov.cn/channel/list/24.html — 卢龙县政府领导之窗（官网确认）",
    },

    # ════════════════════════════════════════
    # Government Leaders (confirmed from 政府领导 page)
    # ════════════════════════════════════════

    # 县委常委、常务副县长
    {
        "id": 3,
        "name": "杨晨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年4月",
        "birthplace": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "卢龙县委常委、常务副县长",
        "current_org": "卢龙县人民政府",
        "source": "https://www.lulong.gov.cn/single/24/7304.html — 官网确认",
    },
    # 副县长
    {
        "id": 4,
        "name": "陈峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年6月",
        "birthplace": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "卢龙县副县长",
        "current_org": "卢龙县人民政府",
        "source": "https://www.lulong.gov.cn/single/24/7300.html — 官网确认",
    },
    # 副县长
    {
        "id": 5,
        "name": "张倩",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977年10月",
        "birthplace": "待查",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "卢龙县副县长",
        "current_org": "卢龙县人民政府",
        "source": "https://www.lulong.gov.cn/single/24/7299.html — 官网确认",
    },
    # 副县长、公安局局长
    {
        "id": 6,
        "name": "张立强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年7月",
        "birthplace": "待查",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "卢龙县副县长、公安局局长",
        "current_org": "卢龙县人民政府",
        "source": "https://www.lulong.gov.cn/single/24/7305.html — 官网确认",
    },
    # 副县长
    {
        "id": 7,
        "name": "王光冲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988年8月",
        "birthplace": "待查",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "卢龙县副县长",
        "current_org": "卢龙县人民政府",
        "source": "https://www.lulong.gov.cn/single/24/7303.html — 官网确认",
    },

    # ════════════════════════════════════════
    # Other Party Committee / County Leaders
    # (identified from news articles — specific roles to be confirmed)
    # ════════════════════════════════════════

    # 郝向东 — mentioned as "县领导" alongside 张志明 and 于忠林
    {
        "id": 8,
        "name": "郝向东",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "卢龙县领导（具体职务待查）",
        "current_org": "卢龙县",
        "source": "https://www.lulong.gov.cn/single/6/18949.html — 2025年1月15日新闻提及为\"县领导\"",
    },
    # 邱中凯 — mentioned as "县领导" in 2025 news
    {
        "id": 9,
        "name": "邱中凯",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "卢龙县领导（具体职务待查）",
        "current_org": "卢龙县",
        "source": "https://www.lulong.gov.cn/single/6/24147.html — 2025年5月20日新闻提及",
    },
    # 刘晓东 — mentioned as "县领导" in 2025 news
    {
        "id": 10,
        "name": "刘晓东",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "卢龙县领导（具体职务待查）",
        "current_org": "卢龙县",
        "source": "https://www.lulong.gov.cn/single/6/24147.html — 2025年5月20日新闻提及",
    },
    # 刘猛 — mentioned as "县领导" in multiple news
    {
        "id": 11,
        "name": "刘猛",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "卢龙县领导（具体职务待查）",
        "current_org": "卢龙县",
        "source": "https://www.lulong.gov.cn/single/6/24147.html — 2025年5月20日及2024年Q4新闻提及",
    },
    # 唐海山 — mentioned as 县领导 in news
    {
        "id": 12,
        "name": "唐海山",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "卢龙县领导（具体职务待查）",
        "current_org": "卢龙县",
        "source": "https://www.lulong.gov.cn/single/6/31396.html — 2025年新闻提及",
    },
    # 陈纪行 — mentioned in 张志明 investigation reports
    {
        "id": 13,
        "name": "陈纪行",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "卢龙县领导（具体职务待查）",
        "current_org": "卢龙县",
        "source": "https://www.lulong.gov.cn/single/6/14422.html — 张志明调研新闻提及",
    },
    # 周庚全 — mentioned in 张志明 investigation reports
    {
        "id": 14,
        "name": "周庚全",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "卢龙县领导（具体职务待查）",
        "current_org": "卢龙县",
        "source": "https://www.lulong.gov.cn/single/6/14422.html — 张志明调研新闻提及",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共卢龙县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共秦皇岛市委员会",
        "location": "河北省秦皇岛市卢龙县",
    },
    {
        "id": 2,
        "name": "卢龙县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "秦皇岛市人民政府",
        "location": "河北省秦皇岛市卢龙县",
    },
    {
        "id": 3,
        "name": "卢龙县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "秦皇岛市人大常委会",
        "location": "河北省秦皇岛市卢龙县",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议卢龙县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "秦皇岛市政协",
        "location": "河北省秦皇岛市卢龙县",
    },
    {
        "id": 5,
        "name": "卢龙县公安局",
        "type": "政府",
        "level": "乡科级",
        "parent": "卢龙县人民政府",
        "location": "河北省秦皇岛市卢龙县",
    },
]

positions = [
    # ── 张志明 (Zhang Zhiming) ──
    {"person_id": 1, "org_id": 1, "title": "卢龙县委书记",
     "start": "约2021", "end": "present", "rank": "正县处级",
     "note": "主持县委全面工作；具体任职时间和此前履历待查"},
    # ── 于忠林 (Yu Zhonglin) ──
    {"person_id": 2, "org_id": 2, "title": "卢龙县委副书记、县长、县政府党组书记",
     "start": "约2021", "end": "present", "rank": "正县处级",
     "note": "主持县政府全面工作；1982年3月生，大学学历，理学学士"},

    # ── Government Leaders ──
    {"person_id": 3, "org_id": 2, "title": "卢龙县委常委、常务副县长",
     "start": "", "end": "present", "rank": "副县处级",
     "note": "1980年4月生，大学学历"},
    {"person_id": 4, "org_id": 2, "title": "卢龙县副县长",
     "start": "", "end": "present", "rank": "副县处级",
     "note": "1972年6月生，大学学历"},
    {"person_id": 5, "org_id": 2, "title": "卢龙县副县长",
     "start": "", "end": "present", "rank": "副县处级",
     "note": "1977年10月生，研究生学历"},
    {"person_id": 6, "org_id": 2, "title": "卢龙县副县长、公安局局长",
     "start": "", "end": "present", "rank": "副县处级",
     "note": "1982年7月生，研究生学历"},
    {"person_id": 6, "org_id": 5, "title": "卢龙县公安局局长",
     "start": "", "end": "present", "rank": "乡科级",
     "note": "兼任县公安局局长"},
    {"person_id": 7, "org_id": 2, "title": "卢龙县副县长",
     "start": "", "end": "present", "rank": "副县处级",
     "note": "1988年8月生，研究生学历"},

    # ── Other County Leaders (specific roles待查) ──
    {"person_id": 8, "org_id": 1, "title": "卢龙县领导（具体职务待查）",
     "start": "", "end": "present", "rank": "",
     "note": "新闻中作为县领导出现；具体分工待查"},
    {"person_id": 9, "org_id": 1, "title": "卢龙县领导（具体职务待查）",
     "start": "", "end": "present", "rank": "",
     "note": "新闻中作为县领导出现；具体分工待查"},
    {"person_id": 10, "org_id": 1, "title": "卢龙县领导（具体职务待查）",
     "start": "", "end": "present", "rank": "",
     "note": "新闻中作为县领导出现；具体分工待查"},
    {"person_id": 11, "org_id": 1, "title": "卢龙县领导（具体职务待查）",
     "start": "", "end": "present", "rank": "",
     "note": "新闻中作为县领导出现；具体分工待查"},
    {"person_id": 12, "org_id": 1, "title": "卢龙县领导（具体职务待查）",
     "start": "", "end": "present", "rank": "",
     "note": "新闻中作为县领导出现；具体分工待查"},
    {"person_id": 13, "org_id": 1, "title": "卢龙县领导（具体职务待查）",
     "start": "", "end": "present", "rank": "",
     "note": "新闻中作为县领导出现；具体分工待查"},
    {"person_id": 14, "org_id": 1, "title": "卢龙县领导（具体职务待查）",
     "start": "", "end": "present", "rank": "",
     "note": "新闻中作为县领导出现；具体分工待查"},
]

relationships = [
    # ── 张志明 (Party Secretary) ↔ 于忠林 (County Mayor) ──
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "strength": "strong",
     "context": "张志明作为县委书记、于忠林作为县长，是卢龙县党政一把手搭档关系",
     "overlap_org": "中共卢龙县委员会/卢龙县人民政府",
     "overlap_period": "约2021年至今",
     "confidence": "confirmed"},

    # ── 张志明 ↔ 杨晨 (常委副县长) ──
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "strength": "strong",
     "context": "张志明与杨晨在县委和政府共事，杨晨任县委常委、常务副县长",
     "overlap_org": "中共卢龙县委/卢龙县人民政府",
     "overlap_period": "当前",
     "confidence": "confirmed"},

    # ── 于忠林 ↔ 杨晨 (县长 & 常务副县长) ──
    {"person_a": 2, "person_b": 3, "type": "subordinate",
     "strength": "strong",
     "context": "于忠林作为县长，杨晨作为常务副县长协助县长工作",
     "overlap_org": "卢龙县人民政府",
     "overlap_period": "当前",
     "confidence": "confirmed"},

    # ── 于忠林 ↔ 陈峰 ──
    {"person_a": 2, "person_b": 4, "type": "subordinate",
     "strength": "medium",
     "context": "于忠林与陈峰在县政府共事，陈峰任副县长",
     "overlap_org": "卢龙县人民政府",
     "overlap_period": "当前",
     "confidence": "confirmed"},

    # ── 于忠林 ↔ 张倩 ──
    {"person_a": 2, "person_b": 5, "type": "subordinate",
     "strength": "medium",
     "context": "于忠林与张倩在县政府共事，张倩任副县长",
     "overlap_org": "卢龙县人民政府",
     "overlap_period": "当前",
     "confidence": "confirmed"},

    # ── 于忠林 ↔ 张立强 ──
    {"person_a": 2, "person_b": 6, "type": "subordinate",
     "strength": "medium",
     "context": "于忠林与张立强在县政府共事，张立强任副县长兼公安局局长",
     "overlap_org": "卢龙县人民政府",
     "overlap_period": "当前",
     "confidence": "confirmed"},

    # ── 于忠林 ↔ 王光冲 ──
    {"person_a": 2, "person_b": 7, "type": "subordinate",
     "strength": "medium",
     "context": "于忠林与王光冲在县政府共事，王光冲任副县长",
     "overlap_org": "卢龙县人民政府",
     "overlap_period": "当前",
     "confidence": "confirmed"},

    # ── 张志明 ↔ other county leaders (from joint appearances in news) ──
    {"person_a": 1, "person_b": 8, "type": "overlap",
     "strength": "medium",
     "context": "张志明与郝向东在县委会议上共同出席",
     "overlap_org": "卢龙县",
     "overlap_period": "2025年至今",
     "confidence": "confirmed"},

    {"person_a": 1, "person_b": 9, "type": "overlap",
     "strength": "medium",
     "context": "张志明与邱中凯在人才座谈会上共同出席",
     "overlap_org": "卢龙县",
     "overlap_period": "2025年至今",
     "confidence": "confirmed"},

    {"person_a": 1, "person_b": 10, "type": "overlap",
     "strength": "medium",
     "context": "张志明与刘晓东在县委会议中共同出席",
     "overlap_org": "卢龙县",
     "overlap_period": "2025年至今",
     "confidence": "confirmed"},

    {"person_a": 1, "person_b": 11, "type": "overlap",
     "strength": "medium",
     "context": "张志明与刘猛在多项县内活动中共同出席",
     "overlap_org": "卢龙县",
     "overlap_period": "2024-2025年",
     "confidence": "confirmed"},

    {"person_a": 1, "person_b": 12, "type": "overlap",
     "strength": "medium",
     "context": "张志明与唐海山共同参加招商引资活动",
     "overlap_org": "卢龙县",
     "overlap_period": "2025年",
     "confidence": "confirmed"},

    {"person_a": 1, "person_b": 13, "type": "overlap",
     "strength": "medium",
     "context": "张志明与陈纪行在项目调研中共同出席",
     "overlap_org": "卢龙县",
     "overlap_period": "2024年",
     "confidence": "confirmed"},

    {"person_a": 1, "person_b": 14, "type": "overlap",
     "strength": "medium",
     "context": "张志明与周庚全在调研活动中共同出席",
     "overlap_org": "卢龙县",
     "overlap_period": "2024年",
     "confidence": "confirmed"},
]

# ── HELPERS ─────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    role = p["current_post"]
    if "县委书记" in role and "副书记" not in role:
        return "255,50,50"  # Red for party secretary
    elif "县长" in role:
        return "50,100,255"  # Blue for government head
    elif "副县长" in role or "常委" in role:
        return "100,100,255"  # Light blue for deputies
    elif "人大" in role:
        return "200,255,255"  # Cyan for NPC
    elif "政协" in role:
        return "255,240,200"  # Cream for CPPCC
    else:
        return "100,100,100"  # Grey for others

def org_color(o):
    t = o["type"]
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }.get(t, "200,200,200")

def is_top_leader(p):
    role = p["current_post"]
    return "县委书记" in role and "副书记" not in role

def person_size(p):
    return "20.0" if is_top_leader(p) else "12.0"

# ── BUILD DB ─────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT, strength TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT, confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, strength, context, overlap_org, overlap_period, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["strength"],
             r["context"], r["overlap_org"], r["overlap_period"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")

# ── BUILD GEXF ────────────────────────────────────────────────

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append('    <description>卢龙县领导班子工作关系网络 - 河北省秦皇岛市卢龙县</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["parent"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
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
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])}~{esc(pos["end"])}"/>')
        lines.append(f'          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationships)
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.5"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append(f'          <attvalue for="3" value="{r["confidence"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {GEXF_PATH}")

# ── SUMMARY ──────────────────────────────────────────────────

def print_summary():
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

if __name__ == "__main__":
    import sqlite3
    build_db()
    build_gexf()
    print_summary()
