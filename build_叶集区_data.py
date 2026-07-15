#!/usr/bin/env python3
"""Build Yeji District (叶集区) leadership network database and GEXF graph.

Targets: 区委书记郑武军, 区长秦富好
Research date: 2026-07-15
Sources:
  - www.ahyeji.gov.cn (official district government website)
  - 领导之窗: https://www.ahyeji.gov.cn/xxgk/ldzchuang/index.html
  - 郑武军 profile: https://www.ahyeji.gov.cn/content/column/6790691?liId=481
  - 秦富好 profile: https://www.ahyeji.gov.cn/content/column/6790691?liId=650 / liId=678
  - 7月全区重点工作推进会 (2026-07-08)
  - 三届区委第2次常委会会议 (2026-07-08)
  - 全区"两优一先"表彰大会暨党课报告会 (2026-07-02)
  - 三届区委第1次常委会会议 (2026-06-28)
  - 中国共产党六安市叶集区第三次代表大会 (2026-06-26)

Confidence: Current roles confirmed from official government website and leadership pages.
  Biographical details sourced from official profiles. Career timelines beyond current
  role are partial for most figures.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "叶集区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "叶集区_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # === 1. Party Secretary (区委书记) ===
    {
        "id": 1,
        "name": "郑武军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-04",
        "birthplace": "安徽金寨",
        "native_place": "安徽金寨",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共六安市叶集区委员会",
        "source": "https://www.ahyeji.gov.cn/content/column/6790691?liId=481 (领导之窗-区委书记); https://www.ahyeji.gov.cn (2026-07-08, 主持7月全区重点工作推进会)",
        "notes": "郑武军，男，汉族，金寨人，1974年4月出生，中共党员，大学学历。现任中共六安市叶集区委书记。主持区委全面工作。",
        "confidence": "confirmed"
    },
    # === 2. District Mayor (区长) ===
    {
        "id": 2,
        "name": "秦富好",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-10",
        "birthplace": "安徽霍邱",
        "native_place": "安徽霍邱县",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2004-07",
        "current_post": "区委副书记、区长",
        "current_org": "叶集区人民政府",
        "source": "https://www.ahyeji.gov.cn/content/column/6790691?liId=650 (领导之窗-区委副书记); https://www.ahyeji.gov.cn/content/column/6790691?liId=678 (领导之窗-区长); https://www.ahyeji.gov.cn/public/6596441/26545698.html (2026-05-15, 主持区政府第78次常务会议)",
        "notes": "秦富好，男，汉族，安徽霍邱县人，1980年10月出生，2003年2月加入中国共产党，2004年7月参加工作，大学学历。现任叶集区委副书记、区长。领导区政府全面工作，负责审计工作，分管区审计局。",
        "confidence": "confirmed"
    },
    # === 3. Deputy Party Secretary (区委副书记) ===
    {
        "id": 3,
        "name": "鲍园兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记、安徽叶集经济开发区党工委书记、管委会主任",
        "current_org": "安徽叶集经济开发区",
        "source": "https://www.ahyeji.gov.cn/content/column/6790691?liId=762 (领导之窗-区委副书记); https://www.ahyeji.gov.cn (2026-07-08, 出席7月全区重点工作推进会)",
        "notes": "鲍园兵，现任叶集区委副书记，兼任安徽叶集经济开发区党工委书记、管委会主任。",
        "confidence": "confirmed"
    },
    # === 4. Standing Committee Members (区委常委) ===
    {
        "id": 4,
        "name": "崔玲",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "叶集区人民政府",
        "source": "https://www.ahyeji.gov.cn/content/column/6790691?liId=621 (领导之窗-区委常委); https://www.ahyeji.gov.cn/content/column/6790691?liId=719 (领导之窗-副区长)",
        "notes": "崔玲，现任叶集区委常委、常务副区长。",
        "confidence": "confirmed"
    },
    {
        "id": 5,
        "name": "张勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、统战部部长",
        "current_org": "中共六安市叶集区委统战部",
        "source": "https://www.ahyeji.gov.cn/content/column/6790691?liId=639 (领导之窗-区委常委)",
        "notes": "张勇，现任叶集区委常委、统战部部长。",
        "confidence": "confirmed"
    },
    {
        "id": 6,
        "name": "郑德跃",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、纪委书记，区监察委员会主任",
        "current_org": "中共六安市叶集区纪律检查委员会",
        "source": "https://www.ahyeji.gov.cn/content/column/6790691?liId=640 (领导之窗-区委常委)",
        "notes": "郑德跃，现任叶集区委常委、纪委书记，区监察委员会主任。",
        "confidence": "confirmed"
    },
    {
        "id": 7,
        "name": "于永军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、人武部政委",
        "current_org": "叶集区人民武装部",
        "source": "https://www.ahyeji.gov.cn/content/column/6790691?liId=771 (领导之窗-区委常委)",
        "notes": "于永军，现任叶集区委常委、人武部政委。",
        "confidence": "confirmed"
    },
    {
        "id": 8,
        "name": "余珊珊",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共六安市叶集区委组织部",
        "source": "https://www.ahyeji.gov.cn/content/column/6790691?liId=781 (领导之窗-区委常委)",
        "notes": "余珊珊，现任叶集区委常委、组织部部长。",
        "confidence": "confirmed"
    },
    {
        "id": 9,
        "name": "邵宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "叶集区人民政府",
        "source": "https://www.ahyeji.gov.cn/content/column/6790691?liId=795 (领导之窗-区委常委); https://www.ahyeji.gov.cn/content/column/6790691?liId=774 (领导之窗-副区长)",
        "notes": "邵宇，现任叶集区委常委、副区长。",
        "confidence": "confirmed"
    },
    {
        "id": 10,
        "name": "赵以友",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、政法委书记",
        "current_org": "中共六安市叶集区委政法委员会",
        "source": "https://www.ahyeji.gov.cn/content/column/6790691?liId=796 (领导之窗-区委常委)",
        "notes": "赵以友，现任叶集区委常委、政法委书记。",
        "confidence": "confirmed"
    },
    {
        "id": 11,
        "name": "周晓娟",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共六安市叶集区委宣传部",
        "source": "https://www.ahyeji.gov.cn/content/column/6790691?liId=800 (领导之窗-区委常委)",
        "notes": "周晓娟，现任叶集区委常委、宣传部部长。",
        "confidence": "confirmed"
    },
    # === 12-16. Deputy District Mayors ===
    {
        "id": 12,
        "name": "刘美胜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "叶集区人民政府",
        "source": "https://www.ahyeji.gov.cn/content/column/6790691?liId=692 (领导之窗-副区长)",
        "notes": "刘美胜，现任叶集区副区长。",
        "confidence": "confirmed"
    },
    {
        "id": 13,
        "name": "李永新",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "叶集区人民政府",
        "source": "https://www.ahyeji.gov.cn/content/column/6790691?liId=735 (领导之窗-副区长)",
        "notes": "李永新，现任叶集区副区长。",
        "confidence": "confirmed"
    },
    {
        "id": 14,
        "name": "杨志红",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "叶集区人民政府",
        "source": "https://www.ahyeji.gov.cn/content/column/6790691?liId=767 (领导之窗-副区长)",
        "notes": "杨志红，现任叶集区副区长。",
        "confidence": "confirmed"
    },
    {
        "id": 15,
        "name": "崔巍",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "叶集区人民政府",
        "source": "https://www.ahyeji.gov.cn/content/column/6790691?liId=793 (领导之窗-副区长)",
        "notes": "崔巍，现任叶集区副区长。",
        "confidence": "confirmed"
    },
    {
        "id": 16,
        "name": "黄巍",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "叶集区人民政府",
        "source": "https://www.ahyeji.gov.cn/content/column/6790691?liId=798 (领导之窗-副区长)",
        "notes": "黄巍，现任叶集区副区长。",
        "confidence": "confirmed"
    },
    {
        "id": 17,
        "name": "王昊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "提名副区长（挂职）",
        "current_org": "叶集区人民政府",
        "source": "https://www.ahyeji.gov.cn/content/column/6790691?liId=803 (领导之窗-副区长)",
        "notes": "王昊，提名叶集区副区长（挂职）。",
        "confidence": "confirmed"
    },
    # === 18. Predecessor (前任区委书记) ===
    {
        "id": 18,
        "name": "胡四军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任区委书记（现任区领导）",
        "current_org": "中共六安市叶集区委员会",
        "source": "https://www.ahyeji.gov.cn (2026-07-08, 出席7月全区重点工作推进会以'区领导'身份出席); 推断为前任区委书记转任",
        "notes": "胡四军，此前报道中曾以叶集区委书记身份活动。2026年6月26日第三次党代会后，郑武军接任区委书记。胡四军目前以'区领导'身份出席活动，具体转任岗位待查。",
        "confidence": "plausible"
    },
]

# ── Organizations ──────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共六安市叶集区委员会", "type": "党委", "level": "县处级", "parent": "中共六安市委员会", "location": "六安市叶集区"},
    {"id": 2, "name": "叶集区人民政府", "type": "政府", "level": "县处级", "parent": "六安市人民政府", "location": "六安市叶集区"},
    {"id": 3, "name": "中共六安市叶集区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共六安市叶集区委员会", "location": "六安市叶集区"},
    {"id": 4, "name": "叶集区监察委员会", "type": "政府", "level": "县处级", "parent": "叶集区人民政府", "location": "六安市叶集区"},
    {"id": 5, "name": "中共六安市叶集区委组织部", "type": "党委", "level": "乡科级", "parent": "中共六安市叶集区委员会", "location": "六安市叶集区"},
    {"id": 6, "name": "中共六安市叶集区委宣传部", "type": "党委", "level": "乡科级", "parent": "中共六安市叶集区委员会", "location": "六安市叶集区"},
    {"id": 7, "name": "中共六安市叶集区委统战部", "type": "党委", "level": "乡科级", "parent": "中共六安市叶集区委员会", "location": "六安市叶集区"},
    {"id": 8, "name": "中共六安市叶集区委政法委员会", "type": "党委", "level": "乡科级", "parent": "中共六安市叶集区委员会", "location": "六安市叶集区"},
    {"id": 9, "name": "叶集区人民武装部", "type": "党委", "level": "县处级", "parent": "六安军分区", "location": "六安市叶集区"},
    {"id": 10, "name": "安徽叶集经济开发区", "type": "开发区", "level": "县处级", "parent": "叶集区人民政府", "location": "六安市叶集区"},
    {"id": 11, "name": "叶集区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "六安市人民代表大会常务委员会", "location": "六安市叶集区"},
    {"id": 12, "name": "叶集区政协", "type": "政协", "level": "县处级", "parent": "政协六安市委员会", "location": "六安市叶集区"},
]

# ── Positions ──────────────────────────────────────────────────────────

positions = [
    # 郑武军 - 区委书记
    (1, 1, "区委书记", "2026-06", "present", "正处级", "2026年6月26日第三次党代会后任区委书记"),
    # 秦富好 - 区长
    (2, 1, "区委副书记", "", "present", "正处级", ""),
    (2, 2, "区长", "", "present", "正处级", "领导区政府全面工作"),
    # 鲍园兵 - 区委副书记
    (3, 1, "区委副书记", "", "present", "正处级", ""),
    (3, 10, "安徽叶集经济开发区党工委书记、管委会主任", "", "present", "正处级", ""),
    # 崔玲
    (4, 1, "区委常委", "", "present", "副处级", ""),
    (4, 2, "常务副区长", "", "present", "副处级", ""),
    # 张勇
    (5, 1, "区委常委", "", "present", "副处级", ""),
    (5, 7, "统战部部长", "", "present", "副处级", ""),
    # 郑德跃
    (6, 1, "区委常委", "", "present", "副处级", ""),
    (6, 3, "纪委书记", "", "present", "副处级", ""),
    (6, 4, "区监察委员会主任", "", "present", "副处级", ""),
    # 于永军
    (7, 1, "区委常委", "", "present", "副处级", ""),
    (7, 9, "人武部政委", "", "present", "副处级", ""),
    # 余珊珊
    (8, 1, "区委常委", "", "present", "副处级", ""),
    (8, 5, "组织部部长", "", "present", "副处级", ""),
    # 邵宇
    (9, 1, "区委常委", "", "present", "副处级", ""),
    (9, 2, "副区长", "", "present", "副处级", ""),
    # 赵以友
    (10, 1, "区委常委", "", "present", "副处级", ""),
    (10, 8, "政法委书记", "", "present", "副处级", ""),
    # 周晓娟
    (11, 1, "区委常委", "", "present", "副处级", ""),
    (11, 6, "宣传部部长", "", "present", "副处级", ""),
    # Deputy Mayors
    (12, 2, "副区长", "", "present", "副处级", ""),
    (13, 2, "副区长", "", "present", "副处级", ""),
    (14, 2, "副区长", "", "present", "副处级", ""),
    (15, 2, "副区长", "", "present", "副处级", ""),
    (16, 2, "副区长", "", "present", "副处级", ""),
    (17, 2, "提名副区长（挂职）", "", "present", "副处级", ""),
    # Predecessor
    (18, 1, "区委书记（前任）", "", "2026-06", "正处级", "前任区委书记，第三次党代会后离任"),
]

# ── Relationships ──────────────────────────────────────────────────────

relationships = [
    # 书记 - 区长
    (1, 2, "overlap", "书记与区长搭档，共同主持区委区政府工作", "中共六安市叶集区委员会", "2026-", "strong"),
    # 书记 - 副书记
    (1, 3, "overlap", "书记与副书记在区委常委会共事", "中共六安市叶集区委员会", "2026-", "strong"),
    # 书记 - 各常委（区委常委会共事）
    (1, 4, "overlap", "区委常委会共事", "中共六安市叶集区委员会", "2026-", "medium"),
    (1, 5, "overlap", "区委常委会共事", "中共六安市叶集区委员会", "2026-", "medium"),
    (1, 6, "overlap", "区委常委会共事；书记与纪委书记", "中共六安市叶集区委员会", "2026-", "medium"),
    (1, 7, "overlap", "区委常委会共事", "中共六安市叶集区委员会", "2026-", "medium"),
    (1, 8, "overlap", "区委常委会共事；书记与组织部部长", "中共六安市叶集区委员会", "2026-", "medium"),
    (1, 9, "overlap", "区委常委会共事", "中共六安市叶集区委员会", "2026-", "medium"),
    (1, 10, "overlap", "区委常委会共事", "中共六安市叶集区委员会", "2026-", "medium"),
    (1, 11, "overlap", "区委常委会共事", "中共六安市叶集区委员会", "2026-", "medium"),
    # 区长 - 常务副区长
    (2, 4, "overlap", "区长与常务副区长工作搭档", "叶集区人民政府", "2026-", "strong"),
    # 区长 - 各副区长
    (2, 9, "overlap", "区政府班子", "叶集区人民政府", "2026-", "medium"),
    (2, 12, "overlap", "区政府班子", "叶集区人民政府", "2026-", "medium"),
    (2, 13, "overlap", "区政府班子", "叶集区人民政府", "2026-", "medium"),
    (2, 14, "overlap", "区政府班子", "叶集区人民政府", "2026-", "medium"),
    (2, 15, "overlap", "区政府班子", "叶集区人民政府", "2026-", "medium"),
    (2, 16, "overlap", "区政府班子", "叶集区人民政府", "2026-", "medium"),
    (2, 17, "overlap", "区政府班子", "叶集区人民政府", "2026-", "medium"),
    # Predecessor chain
    (1, 18, "predecessor_successor", "郑武军接替胡四军任叶集区委书记", "中共六安市叶集区委员会", "2026-06", "strong"),
    # 副书记 - 开发区
    (3, 4, "overlap", "同为区委常委", "中共六安市叶集区委员会", "2026-", "medium"),
    (3, 10, "overlap", "同为区委常委", "中共六安市叶集区委员会", "2026-", "medium"),
    # 常委副区长之间
    (4, 9, "overlap", "同为区委常委、副区长", "叶集区人民政府", "2026-", "medium"),
    # 组织部 - 书记
    (8, 1, "overlap", "组织部部长与书记在干部工作中密切配合", "中共六安市叶集区委员会", "2026-", "strong"),
]


# ══════════════════════════════════════════════════════════════════════════
# Database + GEXF generation
# ══════════════════════════════════════════════════════════════════════════

def create_database():
    """Create SQLite database with persons, organizations, positions, relationships."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = ON;")

    c.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, native_place TEXT,
            education TEXT, party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT,
            source TEXT, notes TEXT, confidence TEXT
        )
    """)
    c.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        )
    """)
    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            strength TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, native_place,
                                 education, party_join, work_start, current_post, current_org,
                                 source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p["birthplace"], p["native_place"], p["education"],
              p["party_join"], p["work_start"],
              p["current_post"], p["current_org"],
              p["source"], p["notes"], p["confidence"]))

    for o in organizations:
        c.execute("INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        pid, oid, title, start, end, rank, note = pos
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (pid, oid, title, start, end, rank, note))

    for r in relationships:
        pa, pb, rtype, ctx, oorg, operiod, strength = r
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (pa, pb, rtype, ctx, oorg, operiod, strength))

    conn.commit()
    conn.close()
    print(f"[OK] Database created: {DB_PATH}")
    print(f"      Persons: {len(persons)}")
    print(f"      Organizations: {len(organizations)}")
    print(f"      Positions: {len(positions)}")
    print(f"      Relationships: {len(relationships)}")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(person):
    """Return 'r,g,b' string based on role."""
    role = person.get("current_post", "")
    if "书记" in role and "副书记" not in role:
        return "255,50,50"  # Red for Party Secretary
    if "区长" in role and "副" not in role:
        return "50,100,255"  # Blue for Mayor
    if "纪委书记" in role or "监委" in role:
        return "255,165,0"  # Orange for Discipline
    if "常委" in role and "副区长" in role:
        return "50,100,255"  # Blue for Standing/Deputy
    if "副区长" in role:
        return "50,100,255"  # Blue for Deputy Mayor
    if "部长" in role:
        return "100,150,255"  # Blue for Department head
    if "副书记" in role:
        return "255,100,100"  # Light Red for Deputy Secretary
    if "统战" in role:
        return "100,150,255"
    if "政法" in role:
        return "100,150,255"
    if "人武" in role:
        return "100,150,255"
    return "100,100,100"  # Grey for others


def person_size(person):
    """Return node size based on rank."""
    role = person.get("current_post", "")
    if "区委书记" in role and "副" not in role:
        return "20.0"
    if "区长" in role and "副" not in role:
        return "20.0"
    return "12.0"


def org_color(org):
    """Return 'r,g,b' string for organization type."""
    t = org.get("type", "")
    type_colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return type_colors.get(t, "200,200,200")


def generate_gexf():
    """Generate GEXF graph using string formatting to avoid XML namespace issues."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append('    <description>叶集区领导班子工作关系网络 - 六安市叶集区</description>')
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
    lines.append('    </attributes>')

    # Nodes: Persons
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

    # Nodes: Organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["name"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization edges (worked_at)
    for pos in positions:
        pid, oid, title, start, end, rank, note = pos
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(start)}-{esc(end)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person ↔ Person edges (relationship)
    for r in relationships:
        pa, pb, rtype, ctx, oorg, operiod, strength = r
        weight = "2.0" if strength == "strong" else "1.5" if strength == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{pa}" target="p{pb}" label="{esc(rtype)}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(ctx)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(operiod)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[OK] GEXF graph created: {GEXF_PATH}")
    print(f"      Person nodes: {len(persons)}")
    print(f"      Organization nodes: {len(organizations)}")
    print(f"      Person→Org edges: {len(positions)}")
    print(f"      Person↔Person edges: {len(relationships)}")
    print(f"      Total edges: {len(positions) + len(relationships)}")


def main():
    print("=" * 60)
    print("  叶集区领导班子网络数据生成")
    print(f"  Generated: {TODAY}")
    print("=" * 60)
    create_database()
    generate_gexf()
    print(f"\nSummary:")
    print(f"  Top leaders: 郑武军（区委书记）, 秦富好（区长）")
    print(f"  Standing Committee: 11 members (including secretary and deputy)")
    print(f"  Government team: 1区长 + 1常务副区长 + 6副区长 + 1挂职副区长")
    print(f"  Predecessor tracked: 胡四军（前任区委书记）")
    print(f"  Research as of: {TODAY}")
    print(f"\n[OK] All files generated in: {SCRIPT_DIR}")


if __name__ == "__main__":
    main()
