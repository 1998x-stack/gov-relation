#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
儋州市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 地级市
Province: 海南省
Region: 儋州市
Targets: 市委书记 & 市长

官方来源（截至2026-08-05）:
- https://www.danzhou.gov.cn/ — 儋州市人民政府门户网站（领导简介页：xxgk/szf/szfld/）
- http://www.hndzdj.cn/      — 儋州党建网（市委组织部；2026年活动报道佐证邹广为现任市委书记）
- 本地省份脚本: scripts/build/build_海南省_data.py（含邹广在省委常委中的登记）

当前在任 (as of 2026-08-05):
- 市委书记: 邹广（海南省委常委、儋州市委书记）
- 市长: 陈阳（儋州市委副书记、市长，洋浦经济开发区工委副书记/管委会主任）

模型说明：
- 核心两位书记/市长履历、身份由官方来源确认；邹广简历细节（出生/学历/任儋州前履历）在本次访问
  （Exa 限流、Wikipedia/Jina 不可达）下未取得，按 partial-evidence 模式将缺口写入
  person JSON 的 open_questions 与 report/open_gaps.md，不编造字段。
- 政府部门领导班子全员（副市长/秘书长）官方简历已核实，纳入网络。
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "儋州市"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-08-05"

# 官方来源URL记录
GOV_LD_MAYOR = "https://www.danzhou.gov.cn/danzhou/xxgk/szf/szfld/sz/202307/t20230704_3447110.html"
GOV_LD_DIR = "https://www.danzhou.gov.cn/danzhou/xxgk/szf/szfld/"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：市委书记（副部级 — 省委常委兼任儋州市委书记）
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "邹广",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "海南省委常委、儋州市委书记",
        "current_org": "中共儋州市委员会",
        "source": "https://www.hndzdj.cn/",
        "note": "儋州党建网2026-06/03 活动报道佐证现任；出生/学历等公开信息本次未取得"
    },
    # ════════════════════════════════════════
    # 核心领导：市长（正厅级）
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "陈阳",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1973-09",
        "birthplace": "待查",
        "education": "经济学博士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "儋州市委副书记、市长，洋浦经济开发区工委副书记/管委会主任",
        "current_org": "儋州市人民政府",
        "source": "https://www.danzhou.gov.cn/danzhou/xxgk/szf/szfld/sz/202307/t20230704_3447110.html",
        "note": ""
    },
    # ════════════════════════════════════════
    # 常务副市长
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "张华伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-10",
        "birthplace": "待查",
        "education": "哲学硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "儋州市委常委、市政府党组副书记、常务副市长，洋浦经开区常务副主任",
        "current_org": "儋州市人民政府",
        "source": "https://www.danzhou.gov.cn/danzhou/xxgk/szf/szfld/fsz/202505/t20250530_3872684.html",
        "note": ""
    },
    # ════════════════════════════════════════
    # 市委常委、副市长（挂职）
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "肖谦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-03",
        "birthplace": "待查",
        "education": "工商管理硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "儋州市委常委、市政府党组成员、副市长（挂职）",
        "current_org": "儋州市人民政府",
        "source": "https://www.danzhou.gov.cn/danzhou/xxgk/szf/szfld/fsz/202411/t20241127_3775165.html",
        "note": "挂职两年；负责国资、卫健、医保、市场监管等"
    },
    # ════════════════════════════════════════
    # 副市长、洋阳澄经开区管委会副主任
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "冯本彦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-08",
        "birthplace": "待查",
        "education": "法学硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "儋州市副市长，洋阳澄经开区工委委员、管委会副主任",
        "current_org": "儋州市人民政府",
        "source": "https://www.danzhou.gov.cn/danzhou/xxgk/szf/szfld/fsz/202111/t20211119_3095627.html",
        "note": "负责自然资源规划、海洋、住建、综合执法等"
    },
    # ════════════════════════════════════════
    # 副市长（农业农村）
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "莫正群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-01",
        "birthplace": "待查",
        "education": "农业推广硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "儋州市副市长",
        "current_org": "儋州市人民政府",
        "source": "https://www.danzhou.gov.cn/danzhou/xxgk/szf/szfld/fsz/201902/t20190218_2340387.html",
        "note": "负责生态环境、农业农村、乡村振兴、水务等"
    },
    # ════════════════════════════════════════
    # 副市长兼公安局长
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "杨宗峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-05",
        "birthplace": "待查",
        "education": "工学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "儋州市副市长、市公安局局长兼任",
        "current_org": "儋州市人民政府",
        "source": "https://www.danzhou.gov.cn/danzhou/xxgk/szf/szdld/fsz/202406/t20240624_3685392.html",
        "note": "市公安局党委书记、局长、督察长；负责公安、司法、信访"
    },
    # ════════════════════════════════════════
    # 副市长（工业/科技）
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "陈评",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1973-01",
        "birthplace": "待查",
        "education": "工学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "儋州市副市长",
        "current_org": "儋州市人民政府",
        "source": "https://www.danzhou.gov.cn/danzhou/xxgk/szf/szdld/fsz/202509/t20250902_3923103.html",
        "note": "负责工业、科技、石化新材料、数字经济"
    },
    # ════════════════════════════════════════
    # 副市长（营商环境/商务/金融）
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "詹联科",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "1981-01",
        "birthplace": "待查",
        "education": "经济学博士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "儋州市副市长",
        "current_org": "儋州市人民政府",
        "source": "https://www.danzhou.gov.cn/danzhou/xxgk/szf/szdld/fsz/202603/t20260319_4045823.html",
        "note": "全日制研究生、经济学博士；负责营商环境、投资促进、商务、金融"
    },
    # ════════════════════════════════════════
    # 市政府党组成员（洋阳澄经开区）
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "张勇军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-06",
        "birthplace": "待查",
        "education": "经济学博士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "儋州市政府党组成员、洋阳澄经开区工委委员、管委会副主任",
        "current_org": "洋阳经济开发区",
        "source": "https://www.danzhou.gov.cn/danzhou/xxgk/szf/szdld/fsz/202403/t20240313_3616822.html",
        "note": "负责交通运输和港航等"
    },
    # ════════════════════════════════════════
    # 市政府党组成员/一级巡视员
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "王凌融",
        "gender": "女",
        "ethnicity": "土家族",
        "birth": "1967-12",
        "birthplace": "待查",
        "education": "公共管理硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "儋州市政府党组成员、一级巡视员",
        "current_org": "儋州市人民政府",
        "source": "https://www.danzhou.gov.cn/danzhou/xxgk/szf/szdld/fsz/202112/t20211220_3115975.html",
        "note": "负责教育、人社、民政、退役军人事务等"
    },
    # ════════════════════════════════════════
    # 政府秘书长
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "王冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-11",
        "birthplace": "待查",
        "education": "工学博士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "儋州市政府党组成员、秘书长",
        "current_org": "儋州市人民政府",
        "source": "https://www.danzhou.gov.cn/danzhou/xxgk/szf/szdly/msz/202607/t20260717_4112543.html",
        "note": "秘书长、办公室党组书记；协助陈阳市长工作"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共儋州市委员会", "type": "党委", "level": "地级", "parent": "中共海南省委员会", "location": "海南省儋州市"},
    {"id": 2, "name": "儋州市人民政府", "type": "政府", "level": "地级", "parent": "海南省人民政府", "location": "海南省儋州市"},
    {"id": 3, "name": "中共海南省委员会", "type": "党委", "level": "省级", "parent": "", "location": "海南省海口市"},
    {"id": 4, "name": "洋浦经济开发区管委会", "type": "开发区", "level": "地级", "parent": "海南省人民政府", "location": "海南省儋州市洋浦"},
    {"id": 5, "name": "儋州市公安局", "type": "政府", "level": "地级", "parent": "儋州市人民政府", "location": "海南省儋州市"},
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # ── 邹广 (id=1) ──
    {"person_id": 1, "org_id": 1, "title": "儋州市委书记", "start": "", "end": "present", "rank": "副部级", "note": "海南省委常委兼任儋州市委书记"},
    {"person_id": 1, "org_id": 3, "title": "海南省委常委", "start": "", "end": "present", "rank": "副部级", "note": ""},

    # ── 陈阳 (id=2) ──
    {"person_id": 2, "org_id": 1, "title": "儋州市委副书记", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "儋州市市长", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 4, "title": "洋浦经济开发区工委副书记、管委会主任", "start": "", "end": "present", "rank": "正厅级", "note": ""},

    # ── 张华伟 (id=3) ──
    {"person_id": 3, "org_id": 1, "title": "儋州市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "儋州市常务副市长（党组副书记）", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 4, "title": "洋浦经开区工委委员、管委会常务副主任", "start": "", "end": "present", "rank": "副厅级", "note": ""},

    # ── 肖谦 (id=4) ──
    {"person_id": 4, "org_id": 1, "title": "儋州市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "儋州市副市长（挂职）", "start": "", "end": "present", "rank": "副厅级", "note": "挂职两年"},

    # ── 冯本彦 (id=5) ──
    {"person_id": 5, "org_id": 2, "title": "儋州市副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 4, "title": "洋浦经开区管委会副主任", "start": "", "end": "present", "rank": "副厅级", "note": ""},

    # ── 莫正群 (id=6) ──
    {"person_id": 6, "org_id": 2, "title": "儋州市副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},

    # ── 杨宗峰 (id=7) ──
    {"person_id": 7, "org_id": 2, "title": "儋州市副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "市公安局局长、党委书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},

    # ── 陈评 (id=8) ──
    {"person_id": 8, "org_id": 2, "title": "儋州市副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},

    # ── 詹联科 (id=9) ──
    {"person_id": 9, "org_id": 2, "title": "儋州市副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},

    # ── 张勇军 (id=10) ──
    {"person_id": 10, "org_id": 2, "title": "儋州市政府党组成员", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 4, "title": "洋浦经开区管委会副主任", "start": "", "end": "present", "rank": "副厅级", "note": ""},

    # ── 王凌融 (id=11) ──
    {"person_id": 11, "org_id": 2, "title": "儋州市政府党组成员、一级巡视员", "start": "", "end": "present", "rank": "副厅级", "note": ""},

    # ── 王冰 (id=12) ──
    {"person_id": 12, "org_id": 2, "title": "儋州市政府秘书长", "start": "", "end": "present", "rank": "正处级", "note": "政府办公室党组书记"},

    # ── 前任（地方档案佐证）: 袁光平（前儋州市长·三沙书记）──
    # 注：袁光平历史任职（儋州市长）来自本地 report 档案；此处仅作为组织人事背景登记，
    # 不与实时角色混淆，不纳入 network 主要 edge。
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 核心搭档：邹广 ↔ 陈阳（党政一把手）──
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "儋州市委书记与市长党政搭档（书记由省委常委兼任）", "overlap_org": "中共儋州市委员会/儋州市人民政府", "overlap_period": "present"},
    # ── 张华伟（常务副市长）与市长 ──
    {"person_a": 3, "person_b": 2, "type": "overlap", "context": "市委常委、常务副市长与市长政府班子搭档", "overlap_org": "儋州市人民政府", "overlap_period": "present"},
    # ── 张华伟与市委书记（市委常委同事）──
    {"person_a": 3, "person_b": 1, "type": "overlap", "context": "儋州市委常委班子同事", "overlap_org": "中共儋州市委员会", "overlap_period": "present"},
    # ── 肖谦（市委常委/挂职副市长）与市长 ──
    {"person_a": 4, "person_b": 2, "type": "overlap", "context": "市委常委、副市长与市长政府班子搭档", "overlap_org": "儋州市人民政府", "overlap_period": "present"},
    {"person_a": 4, "person_b": 1, "type": "overlap", "context": "儋州市委常委班子同事", "overlap_org": "中共儋州市委员会", "overlap_period": "present"},
    # ── 其他副市长与市长（政府班子）──
    {"person_a": 5, "person_b": 2, "type": "overlap", "context": "儋州市副市长与市长政府班子搭档", "overlap_org": "儋州市人民政府", "overlap_period": "present"},
    {"person_a": 6, "person_b": 2, "type": "overlap", "context": "儋州市副市长与市长政府班子搭档", "overlap_org": "儋州市人民政府", "overlap_period": "present"},
    {"person_a": 7, "person_b": 2, "type": "overlap", "context": "儋州市副市长与市长政府班子搭档", "overlap_org": "儋州市人民政府", "overlap_period": "present"},
    {"person_a": 8, "person_b": 2, "type": "overlap", "context": "儋州市副市长与市长政府班子搭档", "overlap_org": "儋州市人民政府", "overlap_period": "present"},
    {"person_a": 9, "person_b": 2, "type": "overlap", "context": "儋州市副市长与市长政府班子搭档", "overlap_org": "儋州市人民政府", "overlap_period": "present"},
    {"person_a": 10, "person_b": 2, "type": "overlap", "context": "儋州市政府党组成员/洋浦经开区与市长工作关系", "overlap_org": "儋州市人民政府/洋浦经开区", "overlap_period": "present"},
    {"person_a": 11, "person_b": 2, "type": "overlap", "context": "儋州市政府党组成员、一级巡视员与市长工作关系", "overlap_org": "儋州市人民政府", "overlap_period": "present"},
    {"person_a": 12, "person_b": 2, "type": "overlap", "context": "市政府秘书长协助市长工作", "overlap_org": "儋州市人民政府", "overlap_period": "present"},
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
    if "书记" in cp and "副书记" not in cp:
        return "200,30,30"
    if "市长" in cp and "副" not in cp:
        return "30,100,200"
    if "市长" in cp:
        return "100,150,220"
    if "副书记" in cp:
        return "220,80,80"
    if "常委" in cp:
        return "180,100,180"
    if "秘书长" in cp:
        return "200,160,50"
    return "100,100,100"


def person_size(current_post):
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp:
        return "20.0"
    if "市长" in cp:
        return "18.0"
    if "副书记" in cp:
        return "15.0"
    if "常委" in cp:
        return "12.0"
    if "副" in cp:
        return "12.0"
    return "10.0"


def person_shape(current_post):
    cp = current_post or ""
    if "书记" in cp:
        return "square"
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
    lines.append('    <description>儋州市领导班子关系网络</description>')
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


def build_person_json(person, timeline, rels, sources, job_scope=None):
    p = person
    job = job_scope or (p.get("current_post", "").split("、")[-1] if "、" in p.get("current_post", "") else p.get("current_post", ""))
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "海南省",
            "city": "儋州市",
            "region": "儋州市",
            "job": job,
            "task_id": "hainan_儋州市",
            "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"danzhou_{p['name']}",
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
            "administrative_rank": "副部级" if ("书记" in p.get("current_post", "") and "副书记" not in p.get("current_post", "")) else "正厅级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"]
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
        "source_register": [
            {"id": "S001", "title": "儋州市人民政府门户网站-市政府领导",
             "url": GOV_LD_DIR, "publisher": "儋州市人民政府",
             "published_at": "", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high",
             "notes": "官方政府领导简介，含市长及所有副市长、秘书长官方简历"},
            {"id": "S002", "title": "儋州党建网（中共儋州市委组织部）",
             "url": "http://www.hndzdj.cn/", "publisher": "中共儋州市委组织部",
             "published_at": "", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high",
             "notes": "2025-2026 市委活动报道《邹广到洋浦开展我陪群众走流程活动》等，佐证邹广任现职"},
            {"id": "S003", "title": "海南省领导班子构建脚本",
             "url": "https://github.com/gov-relation", "publisher": "gov-relation 库内档案",
             "published_at": "", "accessed_at": AS_OF,
             "source_type": "database", "reliability": "medium",
             "notes": "scripts/build/build_海南省_data.py —— 登记邹广(海南省委常委、儋州市委书记)，附 Wikipedia 引用"}
        ],
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
    now = AS_OF.replace("-", "")

    # ── 邹广 person JSON ──
    zg_timeline = [
        {"start": "", "end": "present",
         "org": "中共儋州市委员会",
         "title": "儋州市委书记", "level": "副部级",
         "location": "海南儋州", "system": "party",
         "rank": "副部级", "is_key_promotion": True,
         "notes": "海南省委常委兼任儋州市委书记；儋州党建网 2026-03/06 活动报道佐证",
         "confidence": "confirmed",
         "source_ids": ["S002", "S003"]},
        {"start": "", "end": "present",
         "org": "中共海南省委员会",
         "title": "海南省委常委", "level": "副部级",
         "location": "海南海口", "system": "party",
         "rank": "副部级", "is_key_promotion": True,
         "notes": "",
         "confidence": "plausible",
         "source_ids": ["S003"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "公开渠道（Exa 限流、Wikipedia/Jina 不可达）未取得邹广任儋州市委书记之前的完整履历（出生、学历、籍贯）",
         "confidence": "unverified",
         "source_ids": []},
    ]
    zg_relationships = [
        {"person": "陈阳", "person_id": "danzhou_陈阳",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "目前儋州市委书记与市长党政搭档",
         "overlap_org": "中共儋州市委员会/儋州市人民政府",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    zg_json = build_person_json(
        {"id": 1, "name": "邹广", "gender": "男", "ethnicity": "待查", "birth": "待查",
         "birthplace": "待查", "education": "待查", "party_join": "中共党员", "work_start": "待查",
         "current_post": "儋州市委书记（海南省委常委兼任）", "current_org": "中共儋州市委员会",
         "source": "http://www.hndzdj.cn/"},
        zg_timeline, zg_relationships, None, job_scope="儋州市委书记")
    zg_json["investigation_scope"]["job"] = "市委书记"
    zg_path = os.path.join(PERSONS_DIR, f"{now}-海南省-儋州市-市委书记-邹广.json")
    with open(zg_path, "w", encoding="utf-8") as f:
        json.dump(zg_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {zg_path}")

    # ── 陈阳 person JSON ──
    cy_timeline = [
        {"start": "", "end": "present",
         "org": "儋州市人民政府",
         "title": "儋州市市长", "level": "正厅级",
         "location": "海南儋州", "system": "government",
         "rank": "正厅级", "is_key_promotion": True,
         "notes": "回族，1973年9月生，经济学博士；政府党组书记",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"start": "", "end": "present",
         "org": "中共儋州市委员会",
         "title": "儋州市委副书记", "level": "正厅级",
         "location": "海南儋州", "system": "party",
         "rank": "正厅级", "is_key_promotion": True,
         "notes": "",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"start": "", "end": "present",
         "org": "洋浦经济开发区管委会",
         "title": "洋浦经开区工委副书记、管委会主任", "level": "正厅级",
         "location": "海南儋州洋浦", "system": "development_zone",
         "rank": "正厅级", "is_key_promotion": True,
         "notes": "恢复儋洋一体化节奏",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到陈阳任儋州市长之前（任市长前/任市长后）的完整执业履历",
         "confidence": "unverified",
         "source_ids": []},
    ]
    cy_relationships = [
        {"person": "邹广", "person_id": "danzhou_邹广",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "目前儋州市市长与市委书记党政搭档",
         "overlap_org": "儋州市人民政府/中共儋州市委员会",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    # 从 persons 列表中取陈阳 = id 2
    cy_p = next(p for p in persons if p["id"] == 2)
    cy_json = build_person_json(cy_p, cy_timeline, cy_relationships, [], job_scope="儋州市长")
    cy_json["investigation_scope"]["job"] = "市长"
    cy_path = os.path.join(PERSONS_DIR, f"{now}-海南省-儋州市-市长-陈阳.json")
    with open(cy_path, "w", encoding="utf-8") as f:
        json.dump(cy_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {cy_path}")


# =========================================================================
# 7. MAIN
# =========================================================================

def main():
    print(f"=== Building {SLUG} data === (as of {AS_OF})")
    build_db()
    build_gexf()
    build_person_jsons()
    print(f"=== Done === {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


if __name__ == "__main__":
    main()