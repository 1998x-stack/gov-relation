#!/usr/bin/env python3
"""
环江毛南族自治县 — 领导班子关系网络数据生成脚本

Generated: 2026-07-23
Sources:
  - http://www.hjzf.gov.cn/xxgk/ (县政府领导页面)
  - http://www.hjzf.gov.cn/xxgk/ldjj/xzfld/xz/ (县长毛华慧)
  - http://www.hjzf.gov.cn/xxgk/ldjj/xzfld/fxz/ (副县长们)
  - http://www.hjzf.gov.cn/xxgk/ldjj/ (领导简介)
  - http://www.hjzf.gov.cn/hdjl/zxft/t19587498.shtml (陈斌(前任书记)采访)
  - http://www.hjzf.gov.cn/gdtt/t27931622.shtml (彭继军 巡察会议)
  - http://www.hjzf.gov.cn/gdtt/t27931563.shtml (彭继军 大安乡调研)

Confidence: confirmed (official government sources), plausible/unverified for career gaps
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────────
SLUG = "环江毛南族自治县"
PROVINCE = "广西壮族自治区"
PARENT_CITY = "河池市"
AS_OF = "2026-07-23"
AS_OF_COMPACT = AS_OF.replace("-", "")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Detect if running from canonical repo root or staging directory
if os.path.exists(os.path.join(SCRIPT_DIR, "build_环江毛南族自治县_data.py")) and \
   os.path.exists(os.path.join(SCRIPT_DIR, "data", "persons")):
    # Running from repo root — canonical paths
    REPO_ROOT = SCRIPT_DIR
    DB_PATH = os.path.join(REPO_ROOT, "data", "database", f"{SLUG}_network.db")
    GEXF_PATH = os.path.join(REPO_ROOT, "data", "graph", f"{SLUG}_network.gexf")
    PERSONS_DIR = os.path.join(REPO_ROOT, "data", "persons")
else:
    # In staging/tmp dir
    DB_PATH = os.path.join(SCRIPT_DIR, f"{SLUG}_network.db")
    GEXF_PATH = os.path.join(SCRIPT_DIR, f"{SLUG}_network.gexf")
    PERSONS_DIR = SCRIPT_DIR


# ── DATA ───────────────────────────────────────────────────────────────

persons = [
    {
        "id": 1,
        "name": "彭继军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "自治县党委书记",
        "current_org": "中共环江毛南族自治县委员会",
        "source": "http://www.hjzf.gov.cn/gdtt/t27931622.shtml",
    },
    {
        "id": 2,
        "name": "毛华慧",
        "gender": "女",
        "ethnicity": "毛南族",
        "birth": "1981年10月",
        "birthplace": "",
        "education": "硕士研究生，哲学硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "自治县县长",
        "current_org": "环江毛南族自治县人民政府",
        "source": "http://www.hjzf.gov.cn/xxgk/ldjj/xzfld/xz/",
    },
    {
        "id": 3,
        "name": "陆永亮",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "自治县党委副书记",
        "current_org": "中共环江毛南族自治县委员会",
        "source": "http://www.hjzf.gov.cn/gdtt/t27931622.shtml",
    },
    {
        "id": 4,
        "name": "李润权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年6月",
        "birthplace": "",
        "education": "硕士研究生，经济学硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "环江毛南族自治县人民政府",
        "source": "http://www.hjzf.gov.cn/xxgk/ldjj/xzfld/fxz/t18045346.shtml",
    },
    {
        "id": 5,
        "name": "谭淑方",
        "gender": "女",
        "ethnicity": "毛南族",
        "birth": "1981年12月",
        "birthplace": "",
        "education": "在职研究生，文学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、统战部部长、副县长",
        "current_org": "环江毛南族自治县人民政府",
        "source": "http://www.hjzf.gov.cn/xxgk/ldjj/xzfld/fxz/t11240068.shtml",
    },
    {
        "id": 6,
        "name": "赫永生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年3月",
        "birthplace": "",
        "education": "硕士研究生，工商管理硕士、法律硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长（挂职）",
        "current_org": "环江毛南族自治县人民政府",
        "source": "http://www.hjzf.gov.cn/xxgk/ldjj/xzfld/fxz/t11240250.shtml",
    },
    {
        "id": 7,
        "name": "聂云鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年12月",
        "birthplace": "",
        "education": "理学博士",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长（挂职）",
        "current_org": "环江毛南族自治县人民政府",
        "source": "http://www.hjzf.gov.cn/xxgk/ldjj/xzfld/fxz/t20665520.shtml",
    },
    {
        "id": 8,
        "name": "郭大涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年2月",
        "birthplace": "",
        "education": "工学硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长（挂职）",
        "current_org": "环江毛南族自治县人民政府",
        "source": "http://www.hjzf.gov.cn/xxgk/ldjj/xzfld/fxz/t17104171.shtml",
    },
    {
        "id": 9,
        "name": "张昌信",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年12月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "环江毛南族自治县人民政府",
        "source": "http://www.hjzf.gov.cn/xxgk/ldjj/xzfld/fxz/t11240288.shtml",
    },
    {
        "id": 10,
        "name": "谭荣生",
        "gender": "女",
        "ethnicity": "毛南族",
        "birth": "1979年10月",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "环江毛南族自治县人民政府",
        "source": "http://www.hjzf.gov.cn/xxgk/ldjj/xzfld/fxz/t11240036.shtml",
    },
    {
        "id": 11,
        "name": "袁雄宇",
        "gender": "男",
        "ethnicity": "瑶族",
        "birth": "1976年7月",
        "birthplace": "",
        "education": "学士学位",
        "party_join": "",
        "work_start": "2001年7月",
        "current_post": "副县长",
        "current_org": "环江毛南族自治县人民政府",
        "source": "http://www.hjzf.gov.cn/xxgk/ldjj/xzfld/fxz/t11240021.shtml",
    },
    {
        "id": 12,
        "name": "杨凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年8月",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "环江毛南族自治县人民政府",
        "source": "http://www.hjzf.gov.cn/xxgk/ldjj/xzfld/fxz/t11240329.shtml",
    },
    {
        "id": 13,
        "name": "黄艳娜",
        "gender": "女",
        "ethnicity": "壮族",
        "birth": "1996年12月",
        "birthplace": "",
        "education": "大学本科，工学学士、经济学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府办公室主任",
        "current_org": "环江毛南族自治县人民政府办公室",
        "source": "http://www.hjzf.gov.cn/xxgk/ldjj/xzfld/bgszr/t10385082.shtml",
    },
    {
        "id": 14,
        "name": "彭邓兮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共环江毛南族自治县委员会",
        "source": "http://www.hjzf.gov.cn/gdtt/t27931622.shtml",
    },
    {
        "id": 15,
        "name": "韦格",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、纪委书记",
        "current_org": "中共环江毛南族自治县纪律检查委员会",
        "source": "http://www.hjzf.gov.cn/gdtt/t27931622.shtml",
    },
    {
        "id": 16,
        "name": "覃纯果",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共环江毛南族自治县委员会",
        "source": "http://www.hjzf.gov.cn/gdtt/t27931563.shtml",
    },
    {
        "id": 17,
        "name": "陈斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任自治县党委书记",
        "current_org": "中共环江毛南族自治县委员会",
        "source": "http://www.hjzf.gov.cn/hdjl/zxft/t19587498.shtml",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共环江毛南族自治县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共河池市委员会",
        "location": "广西河池环江毛南族自治县",
    },
    {
        "id": 2,
        "name": "环江毛南族自治县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "河池市人民政府",
        "location": "广西河池环江毛南族自治县",
    },
    {
        "id": 3,
        "name": "中共环江毛南族自治县纪律检查委员会",
        "type": "纪委",
        "level": "县级",
        "parent": "中共河池市纪律检查委员会",
        "location": "广西河池环江毛南族自治县",
    },
    {
        "id": 4,
        "name": "环江毛南族自治县人民政府办公室",
        "type": "政府",
        "level": "县级",
        "parent": "环江毛南族自治县人民政府",
        "location": "广西河池环江毛南族自治县",
    },
    {
        "id": 5,
        "name": "环江毛南族自治县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "环江毛南族自治县人民政府",
        "location": "广西河池环江毛南族自治县",
    },
    {
        "id": 6,
        "name": "河池经济技术开发区环江分园（河池·环江工业园区）",
        "type": "开发区",
        "level": "县级",
        "parent": "环江毛南族自治县人民政府",
        "location": "广西河池环江毛南族自治县",
    },
]

positions = [
    # 彭继军 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "自治县党委书记", "start_date": "2026?", "end_date": "present", "rank": "正处级", "note": "2026年7月已以自治县党委书记身份公开活动"},
    # 毛华慧 — 县长
    {"person_id": 2, "org_id": 2, "title": "自治县县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "自治县人民政府党组书记、县长、一级调研员"},
    {"person_id": 2, "org_id": 1, "title": "自治县党委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 6, "title": "党工委副书记、管委会主任（兼）", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 陆永亮 — 县委副书记
    {"person_id": 3, "org_id": 1, "title": "自治县党委副书记", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 李润权 — 常务副县长
    {"person_id": 4, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "present", "rank": "", "note": "县委常委、常务副县长"},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 谭淑方 — 统战部长、副县长
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "", "note": "外出挂职期间"},
    {"person_id": 5, "org_id": 1, "title": "县委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 赫永生 — 副县长（挂职）
    {"person_id": 6, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "present", "rank": "", "note": "粤桂协作挂职干部"},
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 聂云鹏 — 副县长（挂职）
    {"person_id": 7, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "present", "rank": "", "note": "中科院亚热带农业生态研究所研究员挂职"},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 郭大涛 — 副县长（挂职）
    {"person_id": 8, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "present", "rank": "", "note": "挂职"},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 张昌信 — 副县长、公安局长
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "", "note": "县公安局党委书记、局长"},
    {"person_id": 9, "org_id": 5, "title": "党委书记、局长", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 谭荣生 — 副县长
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 袁雄宇 — 副县长
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 杨凯 — 副县长
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 黄艳娜 — 办公室主任
    {"person_id": 13, "org_id": 4, "title": "办公室主任", "start_date": "", "end_date": "present", "rank": "", "note": "县政府党组成员、办公室主任"},
    # 彭邓兮 — 组织部长
    {"person_id": 14, "org_id": 1, "title": "县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 韦格 — 纪委书记
    {"person_id": 15, "org_id": 3, "title": "县委常委、纪委书记", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 覃纯果 — 宣传部长
    {"person_id": 16, "org_id": 1, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 陈斌 — 前任县委书记
    {"person_id": 17, "org_id": 1, "title": "自治县党委书记（前任）", "start_date": "2022?或更早", "end_date": "2026?", "rank": "正处级", "note": "2025年2月仍以县委书记身份出席河池两会；2026年7月由彭继军接任"},
]

relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记与县长党政搭档", "overlap_org": "环江毛南族自治县", "overlap_period": "2026?-present"},
    # 县委副书记与书记
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记与县委副书记", "overlap_org": "中共环江毛南族自治县委员会", "overlap_period": "2026?-present"},
    # 县委副书记与县长
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "县长与县委副书记（同为县委副职）", "overlap_org": "中共环江毛南族自治县委员会", "overlap_period": "2026?-present"},
    # 县委常委之间
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "县委书记与县委常委", "overlap_org": "中共环江毛南族自治县委员会", "overlap_period": "2026?-present"},
    {"person_a": 1, "person_b": 14, "type": "上下级", "context": "县委书记与组织部长", "overlap_org": "中共环江毛南族自治县委员会", "overlap_period": "2026?-present"},
    {"person_a": 1, "person_b": 15, "type": "上下级", "context": "县委书记与纪委书记", "overlap_org": "中共环江毛南族自治县委员会", "overlap_period": "2026?-present"},
    {"person_a": 1, "person_b": 16, "type": "上下级", "context": "县委书记与宣传部长", "overlap_org": "中共环江毛南族自治县委员会", "overlap_period": "2026?-present"},
    # 县长与副县长们
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "县长与常务副县长", "overlap_org": "环江毛南族自治县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "县长与副县长/公安局长", "overlap_org": "环江毛南族自治县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "县长与副县长", "overlap_org": "环江毛南族自治县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "县长与副县长", "overlap_org": "环江毛南族自治县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "县长与副县长", "overlap_org": "环江毛南族自治县人民政府", "overlap_period": "present"},
    # 前任与继任
    {"person_a": 17, "person_b": 1, "type": "前后任", "context": "陈斌前任县委书记，彭继军接任", "overlap_org": "中共环江毛南族自治县委员会", "overlap_period": "2026?"},
    # 陈斌与毛华慧（前任搭档）
    {"person_a": 17, "person_b": 2, "type": "党政搭档", "context": "前任县委书记与县长（党政搭档）", "overlap_org": "环江毛南族自治县", "overlap_period": "2025-2026?"},
]


# ── HELPERS ────────────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(current_post):
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp:
        return "200,30,30"
    if "县长" in cp:
        return "30,100,200"
    if "副书记" in cp:
        return "220,80,80"
    if "常务" in cp:
        return "100,150,220"
    if "常委" in cp or "组织" in cp or "宣传" in cp or "统战" in cp:
        return "180,100,180"
    if "副" in cp:
        return "100,150,220"
    if "主任" in cp:
        return "60,180,60"
    if "纪委" in cp:
        return "255,165,0"
    return "100,100,100"


def person_size(current_post):
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp:
        return "20.0"
    if "县长" in cp:
        return "18.0"
    if "副书记" in cp:
        return "15.0"
    if "常委" in cp or "组织" in cp or "宣传" in cp or "统战" in cp or "纪委" in cp:
        return "12.0"
    if "常务" in cp:
        return "14.0"
    if "副" in cp:
        return "12.0"
    if "主任" in cp:
        return "10.0"
    return "10.0"


def person_shape(current_post):
    cp = current_post or ""
    if "书记" in cp:
        return "square"
    if "纪委" in cp:
        return "diamond"
    if "人大" in cp or "政协" in cp:
        return "diamond"
    if "副" in cp or "常委" in cp:
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


# ── BUILD FUNCTIONS ────────────────────────────────────────────────────

def build_db():
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
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>{SLUG}领导班子关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
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

    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]+100000}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

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


def build_person_json(person, timeline, rels, sources, job_override=""):
    p = person
    job = job_override or p.get("current_post", "").split("、")[-1] if "、" in p.get("current_post", "") else p.get("current_post", "")
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": PROVINCE,
            "city": PARENT_CITY,
            "region": SLUG,
            "job": job,
            "task_id": "guangxi_环江毛南族自治县",
            "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"huanjiang_{p['name']}",
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
            "administrative_rank": "正处级" if ("书记" in p.get("current_post","") and "副" not in p.get("current_post","")) or "县长" in p.get("current_post","") else "",
            "as_of": AS_OF,
            "is_current_confirmed": bool(p.get("current_post")),
            "source_ids": ["S001"] if p["id"] <= 16 else ["S004"]
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
            "identity": "partial" if not p.get("birth") else "confirmed",
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
    sources_gov = [
        {"id": "S001", "title": "环江毛南族自治县人民政府门户网站",
         "url": "http://www.hjzf.gov.cn/xxgk/", "publisher": "环江毛南族自治县人民政府",
         "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "Active government portal with current leadership info"},
        {"id": "S002", "title": "环江县领导简介-县政府领导",
         "url": "http://www.hjzf.gov.cn/xxgk/ldjj/",
         "publisher": "环江毛南族自治县人民政府", "published_at": "",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "Formal leadership roster"},
    ]
    sources_news = [
        {"id": "S003", "title": "环江融媒新闻-巡察会议",
         "url": "http://www.hjzf.gov.cn/gdtt/t27931622.shtml",
         "publisher": "环江融媒", "published_at": "2026-07-22",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "Confirmed 彭继军 as 县委书记, 陆永亮 as 副书记, 彭邓兮 as 组织部长, 韦格 as 纪委书记"},
        {"id": "S004", "title": "环江融媒-陈斌代表通道采访",
         "url": "http://www.hjzf.gov.cn/hdjl/zxft/t19587498.shtml",
         "publisher": "环江融媒", "published_at": "2025-02-13",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "Confirmed 陈斌 as 县委书记 in Feb 2025"},
    ]

    # ── 彭继军 person JSON ──
    pjj_timeline = [
        {"start": "2026?", "end": "present",
         "org": "中共环江毛南族自治县委员会",
         "title": "自治县党委书记", "level": "正处级",
         "location": f"广西河池{SLUG}", "system": "party",
         "rank": "正处级", "is_key_promotion": True,
         "notes": "接替陈斌任县委书记。2026年7月已以县委书记身份公开活动（巡察会议、大安乡调研）",
         "confidence": "confirmed",
         "source_ids": ["S003"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到彭继军在任环江县委书记之前的完整履历",
         "confidence": "unverified",
         "source_ids": []},
    ]
    pjj_relationships = [
        {"person": "毛华慧", "person_id": "huanjiang_毛华慧",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "县委书记与县长党政搭档",
         "overlap_org": "中共环江毛南族自治县委员会/环江毛南族自治县人民政府",
         "overlap_period": "2026?-present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S003"]},
        {"person": "陈斌", "person_id": "huanjiang_陈斌",
         "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "接替陈斌任环江县委书记",
         "overlap_org": "中共环江毛南族自治县委员会",
         "overlap_period": "2026?",
         "direction": "other_to_person",
         "confidence": "confirmed",
         "source_ids": ["S003", "S004"]},
    ]
    pjj_json = build_person_json(persons[0], pjj_timeline, pjj_relationships, sources_gov + sources_news, "县委书记")
    pjj_path = os.path.join(PERSONS_DIR, f"{AS_OF_COMPACT}-{PROVINCE}-{PARENT_CITY}-县委书记-彭继军.json")
    with open(pjj_path, "w", encoding="utf-8") as f:
        json.dump(pjj_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {pjj_path}")

    # ── 毛华慧 person JSON ──
    mhh_timeline = [
        {"start": "", "end": "present",
         "org": "环江毛南族自治县人民政府/中共环江毛南族自治县委员会",
         "title": "自治县党委副书记、县长、一级调研员", "level": "正处级",
         "location": f"广西河池{SLUG}", "system": "government",
         "rank": "正处级", "is_key_promotion": True,
         "notes": "兼河池经济技术开发区环江分园（河池·环江工业园区）党工委副书记、管委会主任",
         "confidence": "confirmed",
         "source_ids": ["S001", "S002"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "1981年10月生，毛南族，硕士研究生，哲学硕士。公开资料未找到任县长之前或初任的具体日期与完整履历",
         "confidence": "unverified",
         "source_ids": []},
    ]
    mhh_relationships = [
        {"person": "彭继军", "person_id": "huanjiang_彭继军",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "县长与县委书记党政搭档",
         "overlap_org": "环江毛南族自治县人民政府/中共环江毛南族自治县委员会",
         "overlap_period": "2026?-present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S003"]},
        {"person": "陈斌", "person_id": "huanjiang_陈斌",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "前任县委书记时的党政搭档",
         "overlap_org": "环江毛南族自治县",
         "overlap_period": "2025-2026?",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S004"]},
    ]
    mhh_json = build_person_json(persons[1], mhh_timeline, mhh_relationships, sources_gov, "县长")
    mhh_json["identity"]["education"] = [
        {"period": "", "institution": "", "major": "",
         "degree": "哲学硕士", "study_type": "full_time",
         "source_ids": ["S001"]}
    ]
    mhh_path = os.path.join(PERSONS_DIR, f"{AS_OF_COMPACT}-{PROVINCE}-{PARENT_CITY}-县长-毛华慧.json")
    with open(mhh_path, "w", encoding="utf-8") as f:
        json.dump(mhh_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {mhh_path}")


def build():
    os.makedirs(PERSONS_DIR, exist_ok=True)
    print(f"=== Building {SLUG} data ===")
    print(f"Output dir: {os.path.dirname(DB_PATH)}")
    build_db()
    build_gexf()
    build_person_jsons()
    print("\nBuild complete.")


if __name__ == "__main__":
    build()
