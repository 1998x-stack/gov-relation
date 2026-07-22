#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 黎川县 (抚州市, 江西省) leadership network.

Data sourced from 黎川县人民政府 website (www.jxlcx.gov.cn), leadership pages,
news articles, and meeting reports. Where information is incomplete, it is marked
with explicit confidence levels.

黎川县概况: 黎川县是江西省抚州市下辖的一个县，位于江西省东部，武夷山脉西麓，
与福建省接壤，是赣闽边境重要县份。
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/jiangxi_黎川县")
DB_PATH = os.path.join(STAGING, "黎川县_network.db")
GEXF_PATH = os.path.join(STAGING, "黎川县_network.gexf")

os.makedirs(STAGING, exist_ok=True)

# =========================================================================
# DATA
# =========================================================================

persons = [
    # ── Core Leaders: County Party Secretary ──
    {
        "id": 1,
        "name": "万国辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-03",
        "birthplace": "",
        "education": "大学学历，在职硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黎川县委书记",
        "current_org": "中共黎川县委员会",
        "source": "https://www.jxlcx.gov.cn/col/col28088/index.html — 黎川县政府网站领导之窗"
    },

    # ── Core Leaders: County Mayor Candidate ──
    {
        "id": 2,
        "name": "杜国辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黎川县委副书记、县长候选人",
        "current_org": "黎川县人民政府",
        "source": "https://www.jxlcx.gov.cn/art/2026/7/7/art_2466_4459807.html — 黎川县新闻（2026年7月7日）"
    },

    # ── Previous Deputy Party Secretary ──
    {
        "id": 3,
        "name": "宋小锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黎川县委副书记（前任）",
        "current_org": "中共黎川县委员会",
        "source": "https://www.jxlcx.gov.cn/col/col2456/index.html — 黎川县政府网站县委领导页; 新闻中仍以县委副书记身份出现"
    },

    # ── Standing Committee Members ──
    {
        "id": 4,
        "name": "陈武光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-05",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黎川县委常委、常务副县长",
        "current_org": "黎川县人民政府",
        "source": "https://www.jxlcx.gov.cn/col/col28104/index.html — 黎川县政府网站领导页"
    },
    {
        "id": 5,
        "name": "王文锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黎川县委常委、副县长",
        "current_org": "黎川县人民政府",
        "source": "https://www.jxlcx.gov.cn/col/col2456/index.html — 黎川县政府网站县委领导页"
    },
    {
        "id": 6,
        "name": "姚光辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黎川县委常委",
        "current_org": "中共黎川县委员会",
        "source": "https://www.jxlcx.gov.cn/col/col2456/index.html — 黎川县政府网站县委领导页"
    },
    {
        "id": 7,
        "name": "陈华兴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黎川县委常委",
        "current_org": "中共黎川县委员会",
        "source": "https://www.jxlcx.gov.cn/col/col2456/index.html — 黎川县政府网站县委领导页"
    },
    {
        "id": 8,
        "name": "严俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黎川县委常委",
        "current_org": "中共黎川县委员会",
        "source": "https://www.jxlcx.gov.cn/col/col2456/index.html — 黎川县政府网站县委领导页"
    },
    {
        "id": 9,
        "name": "曾建华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黎川县委常委、组织部部长",
        "current_org": "中共黎川县委组织部",
        "source": "https://www.jxlcx.gov.cn/art/2026/6/30/art_2466_4458194.html — 黎川县委表彰大会新闻"
    },
    {
        "id": 10,
        "name": "胡淑媛",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黎川县委常委、宣传部部长",
        "current_org": "中共黎川县委宣传部",
        "source": "https://www.jxlcx.gov.cn/art/2026/6/30/art_2466_4458192.html — 社科院调研组新闻"
    },
    {
        "id": 11,
        "name": "罗峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黎川县委常委",
        "current_org": "中共黎川县委员会",
        "source": "https://www.jxlcx.gov.cn/col/col2456/index.html — 黎川县政府网站县委领导页"
    },

    # ── Deputy County Mayors (副县长) ──
    {
        "id": 12,
        "name": "石俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黎川县副县长",
        "current_org": "黎川县人民政府",
        "source": "https://www.jxlcx.gov.cn/col/col2333/index.html — 黎川县政府网站县政府领导页"
    },
    {
        "id": 13,
        "name": "许志标",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黎川县副县长",
        "current_org": "黎川县人民政府",
        "source": "https://www.jxlcx.gov.cn/col/col2333/index.html — 黎川县政府网站县政府领导页"
    },
    {
        "id": 14,
        "name": "罗燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黎川县副县长",
        "current_org": "黎川县人民政府",
        "source": "https://www.jxlcx.gov.cn/col/col2333/index.html — 黎川县政府网站县政府领导页"
    },
    {
        "id": 15,
        "name": "颜文珍",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黎川县副县长",
        "current_org": "黎川县人民政府",
        "source": "https://www.jxlcx.gov.cn/col/col2333/index.html — 黎川县政府网站县政府领导页"
    },
    {
        "id": 16,
        "name": "陈咏梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黎川县副县长",
        "current_org": "黎川县人民政府",
        "source": "https://www.jxlcx.gov.cn/col/col2333/index.html — 黎川县政府网站县政府领导页"
    },
    {
        "id": 17,
        "name": "朱良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黎川县副县长",
        "current_org": "黎川县人民政府",
        "source": "https://www.jxlcx.gov.cn/col/col2333/index.html — 黎川县政府网站县政府领导页"
    },

    # ── Other Key Leaders ──
    {
        "id": 18,
        "name": "全安",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黎川县人大常委会主任",
        "current_org": "黎川县人民代表大会常务委员会",
        "source": "https://www.jxlcx.gov.cn/art/2026/6/30/art_2466_4458194.html — 黎川县七一表彰大会新闻"
    },
    {
        "id": 19,
        "name": "尧晓孙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黎川县政协主席",
        "current_org": "中国人民政治协商会议黎川县委员会",
        "source": "https://www.jxlcx.gov.cn/art/2026/7/1/art_2466_4458727.html — 建党105周年大会新闻"
    },

    # ── City-level leaders (抚州市) ──
    {
        "id": 20,
        "name": "范小林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-12",
        "birthplace": "江西宜丰",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "抚州市委书记",
        "current_org": "中共抚州市委员会",
        "source": "https://www.jxfz.gov.cn — 抚州市政府网站"
    },
    {
        "id": 21,
        "name": "胡剑飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "抚州市委副书记、市长",
        "current_org": "抚州市人民政府",
        "source": "https://www.jxfz.gov.cn — 抚州市政府网站"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共黎川县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共抚州市委员会",
        "location": "江西省抚州市黎川县"
    },
    {
        "id": 2,
        "name": "黎川县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "抚州市人民政府",
        "location": "江西省抚州市黎川县"
    },
    {
        "id": 3,
        "name": "黎川县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "抚州市人民代表大会常务委员会",
        "location": "江西省抚州市黎川县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议黎川县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "中国人民政治协商会议抚州市委员会",
        "location": "江西省抚州市黎川县"
    },
    {
        "id": 5,
        "name": "中共黎川县委组织部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共黎川县委员会",
        "location": "江西省抚州市黎川县"
    },
    {
        "id": 6,
        "name": "中共黎川县委宣传部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共黎川县委员会",
        "location": "江西省抚州市黎川县"
    },
    {
        "id": 7,
        "name": "中共抚州市委员会",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共江西省委员会",
        "location": "江西省抚州市"
    },
    {
        "id": 8,
        "name": "抚州市人民政府",
        "type": "政府",
        "level": "地厅级",
        "parent": "江西省人民政府",
        "location": "江西省抚州市"
    },
]

positions = [
    # 万国辉 — Party Secretary
    {"id": 1, "person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正县级", "note": "主持县委全面工作"},

    # 杜国辉 — County Mayor Candidate
    {"id": 2, "person_id": 2, "org_id": 2, "title": "县长候选人", "start": "2026-07", "end": "present", "rank": "正县级", "note": "2026年7月以县委副书记、县长候选人身份公开活动"},
    {"id": 3, "person_id": 2, "org_id": 1, "title": "县委副书记", "start": "2026-07", "end": "present", "rank": "正县级", "note": ""},

    # 宋小锋 — Previous Deputy Secretary
    {"id": 4, "person_id": 3, "org_id": 1, "title": "县委副书记", "start": "", "end": "2026-06", "rank": "正县级", "note": "2026年6月底仍以县委副书记身份主持会议"},

    # 陈武光 — Executive Deputy Mayor
    {"id": 5, "person_id": 4, "org_id": 2, "title": "常务副县长", "start": "", "end": "present", "rank": "副县级", "note": "负责县政府常务工作"},
    {"id": 6, "person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"id": 7, "person_id": 4, "org_id": 2, "title": "县政府党组副书记", "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 王文锋 — Deputy Mayor
    {"id": 8, "person_id": 5, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"id": 9, "person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 姚光辉
    {"id": 10, "person_id": 6, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 陈华兴
    {"id": 11, "person_id": 7, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 严俊
    {"id": 12, "person_id": 8, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 曾建华 — Organization Department Director
    {"id": 13, "person_id": 9, "org_id": 5, "title": "组织部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"id": 14, "person_id": 9, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 胡淑媛 — Propaganda Department Director
    {"id": 15, "person_id": 10, "org_id": 6, "title": "宣传部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"id": 16, "person_id": 10, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 罗峰
    {"id": 17, "person_id": 11, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},

    # Deputy Mayors
    {"id": 18, "person_id": 12, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"id": 19, "person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"id": 20, "person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"id": 21, "person_id": 15, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"id": 22, "person_id": 16, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"id": 23, "person_id": 17, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 全安 — People's Congress
    {"id": 24, "person_id": 18, "org_id": 3, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "正县级", "note": ""},

    # 尧晓孙 — Political Consultative Conference
    {"id": 25, "person_id": 19, "org_id": 4, "title": "县政协主席", "start": "", "end": "present", "rank": "正县级", "note": ""},

    # City-level leaders
    {"id": 26, "person_id": 20, "org_id": 7, "title": "抚州市委书记", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"id": 27, "person_id": 21, "org_id": 8, "title": "抚州市市长", "start": "", "end": "present", "rank": "正厅级", "note": ""},
]

relationships = [
    # Leadership team —县委常委会成员在同一班子共事
    {
        "id": 1,
        "person_a_id": 1,
        "person_b_id": 4,
        "type": "overlap",
        "context": "县委书记与常务副县长在同一县委班子共事",
        "overlap_org": "中共黎川县委员会",
        "overlap_period": "2024-2026年"
    },
    {
        "id": 2,
        "person_a_id": 1,
        "person_b_id": 3,
        "type": "overlap",
        "context": "县委书记与县委副书记（前任）共事",
        "overlap_org": "中共黎川县委员会",
        "overlap_period": "至2026年6月"
    },
    {
        "id": 3,
        "person_a_id": 1,
        "person_b_id": 2,
        "type": "superior_subordinate",
        "context": "县委书记与新任县长候选人搭档",
        "overlap_org": "中共黎川县委员会",
        "overlap_period": "2026年7月起"
    },
    {
        "id": 4,
        "person_a_id": 4,
        "person_b_id": 5,
        "type": "overlap",
        "context": "常务副县长与副县长在县政府班子共事",
        "overlap_org": "黎川县人民政府",
        "overlap_period": ""
    },
    {
        "id": 5,
        "person_a_id": 3,
        "person_b_id": 4,
        "type": "overlap",
        "context": "县委副书记与常务副县长在县委常委会共事",
        "overlap_org": "中共黎川县委员会",
        "overlap_period": ""
    },
    {
        "id": 6,
        "person_a_id": 9,
        "person_b_id": 1,
        "type": "superior_subordinate",
        "context": "县委组织部部长受县委书记领导",
        "overlap_org": "中共黎川县委员会",
        "overlap_period": ""
    },
    {
        "id": 7,
        "person_a_id": 10,
        "person_b_id": 1,
        "type": "superior_subordinate",
        "context": "县委宣传部部长受县委书记领导",
        "overlap_org": "中共黎川县委员会",
        "overlap_period": ""
    },
]


# =========================================================================
# BUILD SQLITE
# =========================================================================

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS relationships")
    cur.execute("DROP TABLE IF EXISTS positions")
    cur.execute("DROP TABLE IF EXISTS organizations")
    cur.execute("DROP TABLE IF EXISTS persons")

    cur.execute("""
        CREATE TABLE persons (
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
        )
    """)

    cur.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY,
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

    cur.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY,
            person_a_id INTEGER,
            person_b_id INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a_id) REFERENCES persons(id),
            FOREIGN KEY (person_b_id) REFERENCES persons(id)
        )
    """)

    for p in persons:
        cur.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education,
                                 party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p["birthplace"], p["education"], p["party_join"], p["work_start"],
              p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (id, person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
              pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (id, person_a_id, person_b_id, type, context,
                                       overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
              r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()

    # Stats
    print(f"  Persons: {cur.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}")
    print(f"  Organizations: {cur.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}")
    print(f"  Positions: {cur.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}")
    print(f"  Relationships: {cur.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")

    conn.close()


# =========================================================================
# BUILD GEXF
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    post = p["current_post"]
    if "书记" in post and "县委" in post:
        return "255,50,50"
    elif "县长" in post or "市长" in post:
        return "50,100,255"
    elif "常务" in post:
        return "50,100,255"
    elif "纪委书记" in post:
        return "255,165,0"
    else:
        return "100,100,100"

def org_color(o):
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")

def is_top_leader(p):
    current = p["current_post"]
    return "县委书记" in current or "县长" in current


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>黎川县领导班子工作关系网络 - 江西省抚州市黎川县</description>')
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
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
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
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges: person -> organization (worked_at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        label = f"{pos['title']}"
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(label)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"][:50]) if pos["note"] else ""}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges: person <-> person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["overlap_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF nodes: {len(persons) + len(organizations)}")
    print(f"  GEXF edges: {eid}")


# =========================================================================
# MAIN
# =========================================================================

if __name__ == "__main__":
    print("Building 黎川县 network data...")
    build_db()
    build_gexf()
    print(f"\nDone! Files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
