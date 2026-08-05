#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
江州区(崇左市)领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 市辖区
Province: 广西壮族自治区
Parent City: 崇左市
Region: 江州区
Targets: 区委书记 & 区长

注意: 本脚本数据基于公开资料搜集。本次调查网络搜索受限(Exa 限流)，
核心人物身份与履历主要来自百度百科及政府官网新闻，部分字段标记为
待查/unverified，需后续核实补充。

数据来源: 广西崇左市江州区人民政府门户网站 (czsjz.gov.cn)、百度百科、水附报道
截至日期: 2026-08-05
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "江州区"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-08-05"
TODAY = AS_OF

# =========================================================================
# 1. PERSONS
# =========================================================================
# 角色类型 (与 GEXF 配色对应):
#   party       区委书记/副书记 (红)
#   government  区长/副区长 (蓝)
#   discipline  纪委书记 (橙)
#   other       人大/政协/常委等 (灰)
persons = [
    # ════════════════════════════════════════
    # 核心领导：区委书记 李红兰
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "李红兰",
        "role_class": "primary",
        "gender": "女",
        "ethnicity": "壮族",
        "birth": "1977年9月",
        "birthplace": "广西大新",
        "native_place": "广西大新",
        "education": "广西壮族自治区党委党校研究生（公共管理，2010年1月在职研究生）",
        "party_join": "1998年7月",
        "work_start": "1995年7月",
        "current_post": "崇左市江州区委书记",
        "current_org": "中共崇左市江州区委员会",
        "rank": "正处级",
        "source": "confirmed — 江州区人民政府门户网站多篇新闻报道确认现任区委书记；百度百科",
    },
    # ════════════════════════════════════════
    # 核心领导：区长 谢添
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "谢添",
        "role": "county",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年12月",
        "birthplace": "广西玉林",
        "native_place": "广西玉林",
        "education": "在职研究生学历，管理学学士",
        "party_join": "2003年12月",
        "work_start": "待查",
        "current_post": "崇左市江州区委副书记、区长",
        "current_org": "崇左市江州区人民政府",
        "rank": "正处级",
        "source": "confirmed — 百度百科; 崇左市干部任前公示(2021); 江州区人大决议(2025-12)",
    },
    # ════════════════════════════════════════
    # 前任区委书记 梁金昌（已调任河池市副市长）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "梁金昌",
        "role": "primary",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年10月",
        "birthplace": "广西藤县",
        "native_place": "广西藤县",
        "education": "中央广播电视大学法学专业，大学学历",
        "party_join": "2004年6月",
        "work_start": "1999年9月",
        "current_post": "河池市人民政府副市长（原崇左市江州区委书记）",
        "current_org": "河池市人民政府",
        "rank": "副厅级",
        "source": "confirmed — 河池市人大决定(2025-08-30); 百度百科; 腾讯新闻",
    },
    # ════════════════════════════════════════
    # 区委常委、常务副区长 陆梧
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "陆梧",
        "role": "county",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1982年7月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "崇左市江州区委常委、常务副区长",
        "current_org": "崇左市江州区人民政府",
        "rank": "副县长级",
        "source": "confirmed — 崇左市生态环境局/江州区人民政府政务文件；百度百科摘要(2024-11政府领导简介)",
    },
    # ════════════════════════════════════════
    # 副区长 陆军敏
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "陆军敏",
        "role": "county",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1975年12月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "崇左市江州区人民政府党组成员、副区长",
        "current_org": "崇左市江州区人民政府",
        "rank": "副处级",
        "source": "confirmed — 江州区人民政府门户网站(领导简介, 2023-10-08)",
    },
    # ════════════════════════════════════════
    # 副区长 张全官
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "张全官",
        "role": "county",
        "gender": "男（推测）",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "崇左市江州区人民政府副区长",
        "current_org": "崇左市江州区人民政府",
        "rank": "副处级",
        "source": "confirmed — 江州区人民政府门户网站(领导之窗); 2024-2026会议报道",
    },
    # ════════════════════════════════════════
    # 副区长 邓欣荣（挂职）
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "邓欣荣",
        "role": "county",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "1979年8月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "江西财经（硕士?，待查）",
        "party_join": "民进会员（非中共党员）",
        "work_start": "待查",
        "current_post": "崇左市江州区人民政府副区长（挂职）",
        "current_org": "崇左市江州区人民政府",
        "rank": "副处级（挂职）",
        "source": "confirmed — 江州区政府门户网站(2020-01-28); 江州区人大常委会任免名单(2026-01-20 挂任期一年)",
    },
    # ════════════════════════════════════════
    # 区人大常委会党组书记 冯丹萍
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "冯丹萍",
        "role": "other",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "崇左市江州区人大常委会党组书记",
        "current_org": "崇左市江州区人民代表大会常务委员会",
        "rank": "正处级",
        "source": "confirmed — 江州区政府门户网站新闻(2026-07 建军慰问报道列名)",
    },
    # ════════════════════════════════════════
    # 区政协主席 黄德隆
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "黄德隆",
        "role": "other",
        "gender": "男（推测）",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "崇左市江州区政协主席",
        "current_org": "中国人民政治协商会议崇左市江州区委员会",
        "rank": "正处级",
        "source": "confirmed — 江州区政府门户网站新闻(2026-07 建军慰问报道列四位)",
    },
    # ════════════════════════════════════════
    # 区人大常委会主任 李利民（2025年1月仍任）
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "李利民",
        "role": "other",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "江州区人大常委会主任（前任）",
        "current_org": "崇左市江州区人民代表大会常务委员会",
        "rank": "正处级",
        "source": "confirmed — 2025年1月走访慰问报道(李利民列人大主任)；任期存在更替",
    },
    # ════════════════════════════════════════
    # 区政协副主席 陆永住（2023年报道为副区长，后任政协）
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "陆永住",
        "role": "other",
        "gender": "男（推测）",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "江州区领导/原副区长（2026-02 会议列名）",
        "current_org": "崇左市江州区人民政府",
        "rank": "副处级",
        "source": "confirmed — 2023-2026 江州区领导会议报道列名（副区长/政协副主席）",
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 101, "name": "中共崇左市江州区委员会", "type": "党委", "level": "市辖区", "parent": "中共崇左市委员会", "location": "广西崇左市江州区"},
    {"id": 102, "name": "崇左市江州区人民政府", "type": "政府", "level": "市辖区", "parent": "崇左市人民政府", "location": "广西崇左市江州区"},
    {"id": 103, "name": "崇左高新技术产业开发区（中泰产业园）", "type": "开发区", "level": "市管园区", "parent": "崇左市人民政府", "location": "广西崇左市"},
    {"id": 104, "name": "崇左市江州区人民代表大会常务委员会", "type": "人大", "level": "市辖区", "parent": "崇左市人民代表大会", "location": "广西崇左市江州区"},
    {"id": 105, "name": "中国人民政治协商会议崇左市江州区委员会", "type": "政协", "level": "市辖区", "parent": "政协崇左市委员会", "location": "广西崇左市江州区"},
    {"id": 106, "name": "崇左市人力资源和社会保障局", "type": "政府", "level": "地市级", "parent": "崇左市人民政府", "location": "广西崇左市"},
    {"id": 107, "name": "中共扶绥县委", "type": "党委", "level": "县", "parent": "中共崇左市委员会", "location": "广西崇左市扶绥县"},
    {"id": 108, "name": "河池市人民政府", "type": "政府", "level": "地市级", "parent": "广西壮族自治区人民政府", "location": "广西河池市"},
    {"id": 109, "name": "中共大新县委", "type": "党委", "level": "县", "parent": "中共崇左市委员会", "location": "广西崇左市大新县"},
    {"id": 110, "name": "大新县人民政府", "type": "政府", "level": "县", "parent": "崇左市人民政府", "location": "广西崇左市大新县"},
    {"id": 111, "name": "中共天等县委", "type": "党委", "level": "县", "parent": "中共崇左市委员会", "location": "广西崇左市天等县"},
    {"id": 112, "name": "天等县人民政府", "type": "政府", "level": "县", "parent": "崇左市人民政府", "location": "广西崇左市天等县"},
    {"id": 113, "name": "梧州市生态环境局", "type": "政府", "level": "地市级", "parent": "梧州市人民政府", "location": "广西梧州市"},
]

# =========================================================================
# 3. POSITIONS (工作经历)
# =========================================================================
positions = [
    # 李红兰
    {"person_id": 1, "org_id": 109, "title": "大新县堪圩乡中心小学教师", "start": "1995", "end": "待查", "rank": "副科级以下", "note": "从教师岗位起步"},
    {"person_id": 1, "org_id": 109, "title": "大新县雷平镇党委组织委员、副镇长", "start": "待查", "end": "待查", "rank": "科级", "note": ""},
    {"person_id": 1, "org_id": 109, "title": "大新县委办公室副主任", "start": "待查", "end": "待查", "rank": "科级", "note": ""},
    {"person_id": 1, "org_id": 109, "title": "大新县雷平镇镇长", "start": "待查", "end": "待查", "rank": "科级", "note": ""},
    {"person_id": 1, "org_id": 109, "title": "大新县昌明乡党委书记", "start": "待查", "end": "2014", "rank": "正科级", "note": ""},
    {"person_id": 1, "org_id": 112, "title": "天等县副县长", "start": "2014", "end": "待查", "rank": "副处级", "note": "2014年后任天等县副县长"},
    {"person_id": 1, "org_id": 102, "title": "崇左市江州区委副书记、区长", "start": "2020左右", "end": "2025年12月", "rank": "正处级", "note": "任内曾兼任区管多职"},
    {"person_id": 1, "org_id": 101, "title": "崇左市江州区委书记", "start": "2025年12月", "end": "present", "rank": "正处级", "note": "2025年11月拟进一步使用公示，2025-12正式转任"},
    {"person_id": 1, "org_id": 103, "title": "崇左高新技术产业开发区（中泰产业园）党工委书记", "start": "2025年12月", "end": "present", "rank": "正处级", "note": "兼任"},
    # 谢添
    {"person_id": 2, "org_id": 106, "title": "崇左市委组织部副部长、市公务员局局长（兼）", "start": "2021年初", "end": "2021年9月", "rank": "副处级", "note": "2021-07 任前公示信息"},
    {"person_id": 2, "org_id": 106, "title": "崇左市人力资源和社会保障局党组书记、局长兼市委组织部副部长", "start": "2021年9月", "end": "2023年左右", "rank": "正处级", "note": "2021-09 报道为该职务"},
    {"person_id": 2, "org_id": 107, "title": "扶绥县委副书记（正处级）、县委党校校长", "start": "2023年左右", "end": "2025年12月", "rank": "正处级", "note": "2023-02 以县委副书记出席"},
    {"person_id": 2, "org_id": 101, "title": "江州区委副书记", "start": "2025年12月", "end": "2025年12月", "rank": "正处级", "note": "2025-12-08 报道"},
    {"person_id": 2, "org_id": 102, "title": "崇左市江州区人民政府区长（代理→正式）", "start": "2025年12月", "end": "present", "rank": "正处级", "note": "2025-12-17 代理; 2026年后转正"},
    # 梁金昌
    {"person_id": 3, "org_id": 113, "title": "梧州市生态环境局局长、党组书记", "start": "待查", "end": "2021年7月", "rank": "正处级", "note": "此前长期在梧州市工作"},
    {"person_id": 3, "org_id": 101, "title": "崇左市江州区委书记", "start": "2021年7月", "end": "2025年8月", "rank": "正处级", "note": "2021-07 调任，2021-08 兼任中泰产业园工委书记"},
    {"person_id": 3, "org_id": 108, "title": "河池市人民政府副市长/党组成员", "start": "2025年8月", "end": "present", "rank": "副厅级", "note": "2025-07 拟任副厅级，2025-08 任命；兼任市公安局党委书记"},
    # 陆梧
    {"person_id": 4, "org_id": 102, "title": "江州区委常委、常务副区长", "start": "待查", "end": "present", "rank": "副处级", "note": "2023-2025 多份文件/报道确认"},
    # 陆军敏
    {"person_id": 5, "org_id": 102, "title": "江州区人民政府党组成员、副区长", "start": "2023年以前", "end": "present", "rank": "副处级", "note": ""},
    # 张全官
    {"person_id": 6, "org_id": 102, "title": "江州区人民政府副区长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 邓欣荣
    {"person_id": 7, "org_id": 102, "title": "江州区人民政府副区长（挂职）", "start": "2026年1月", "end": "2027年1月", "rank": "副处级", "note": "挂任期一年; 民进钦州市工委专职副主任、秘书长"},
    # 冯丹萍
    {"person_id": 8, "org_id": 104, "title": "江州区人大常委会党组书记", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    # 黄德隆
    {"person_id": 9, "org_id": 105, "title": "江州区政协主席", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    # 李利民
    {"person_id": 10, "org_id": 104, "title": "江州区人大常委会主任", "start": "待查", "end": "2026年左右", "rank": "正处级", "note": "2025-01 报道仍任人大主任"},
    # 陆永住
    {"person_id": 11, "org_id": 102, "title": "江州区副区长/区领导", "start": "待查", "end": "present", "rank": "副处级", "note": "2023副区长报道、2026-02列区领导"},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 现任党政搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "现任区委书记与区长党政搭档", "overlap_org": "中共江州区委/江州区人民政府", "overlap_period": "2025-12至今", "strength": "强"},
    # 前任书记 → 现任书记
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor", "context": "李红兰接任梁金昌任江州区委书记", "overlap_org": "中共江州区委", "overlap_period": "2025", "strength": "强"},
    # 前任书记 → 区长（班子共事）
    {"person_a": 3, "person_b": 2, "type": "overlap", "context": "梁金昌2025年8月前与区长同班子；谢2025-12到任，与张梁无直接重叠", "overlap_org": "江州区党政", "overlap_period": "2025", "strength": "弱"},
    # 李红兰此前任区长（与前任书记搭档）
    {"person_a": 3, "person_b": 1, "type": "overlap", "context": "李红兰任区长时任书记梁金昌党政搭档(2021-2025)", "overlap_org": "江州区党政", "overlap_period": "2021-2025", "strength": "强"},
    # 陆梧与谢添（现政府班子搭档）
    {"person_a": 4, "person_b": 2, "type": "overlap", "context": "区长谢添与常务副区长陆梧政府班子搭档", "overlap_org": "江州区人民政府", "overlap_period": "2025-12至今", "strength": "强"},
    # 陆军敏与李红兰（区政府班子共事）
    {"person_a": 5, "person_b": 1, "type": "overlap", "context": "陆军敏任副区长期间与李红兰区长共事", "overlap_org": "江州区人民政府", "overlap_period": "2020-2025", "strength": "中"},
    # 区四家班子
    {"person_a": 8, "person_b": 1, "type": "overlap", "context": "人大党组书记与区委书记区四家班子共事", "overlap_org": "江州区四家班子", "overlap_period": "2025-至今", "strength": "中"},
    {"person_a": 9, "person_b": 1, "type": "overlap", "context": "政协主席与区委书记区四家班子共事", "overlap_org": "江州区四家班子", "overlap_period": "2025-至今", "strength": "中"},
]

# =========================================================================
# HELPER: XML escape
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))

PERSON_COLORS = {
    "primary": "255,50,50",
    "county": "50,100,255",
    "discipline": "255,165,0",
    "other": "100,100,100",
}
ORG_COLORS = {
    "党委": "255,200,200",
    "政府": "200,200,255",
    "开发区": "200,255,200",
    "乡镇/街道": "255,255,200",
    "事业单位": "220,220,220",
    "群团": "255,220,255",
    "人大": "200,255,255",
    "政协": "255,240,200",
}

# =========================================================================
# BUILD SQLite
# =========================================================================
def build_db(path=DB_PATH):
    if os.path.exists(path):
        os.remove(path)
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.executescript("""
    CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT, birthplace TEXT,
        education TEXT, party_join TEXT, work_start TEXT,
        current_post TEXT, current_org TEXT, source TEXT
    );
    CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    );
    CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER, title TEXT, start TEXT, end TEXT,
        rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    );
    CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER, type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT, strength TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    );
    """)
    for p in persons:
        c.execute(
            "INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
             p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]),
        )
    for o in organizations:
        c.execute("INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for po in positions:
        c.execute("INSERT INTO positions (person_id,org_id,title,start,end,note) VALUES (?,?,?,?,?,?)",
                  (po["person_id"], po["org_id"], po["title"], po.get("start", ""), po.get("end", ""), po.get("note", "")))
    for r in relationships:
        c.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period,strength) VALUES (?,?,?,?,?,?,?)",
                  (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"], r["strength"]))
    conn.commit()
    conn.close()

# =========================================================================
# BUILD GEXF
# =========================================================================
def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>崇左市江州区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="birth" type="string"/>')
    lines.append('      <attribute id="3" title="birthplace" type="string"/>')
    lines.append('      <attribute id="4" title="current_post" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')
    # nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        role = p.get("role", "other")
        color = PERSON_COLORS.get(role, PERSON_COLORS["other"])
        size = "20.0" if role == "primary" else ("14.0" if role == "county" else "12.0")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("birth", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birthplace", ""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["current_post"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append('      </node>')
    # nodes: orgs
    for o in organizations:
        color = ORG_COLORS.get(o["type"], "200,200,200")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    # edges: worked_at
    lines.append('    <edges>')
    eid = 0
    for po in positions:
        lines.append(f'      <edge id="{eid}" source="p{po["person_id"]}" target="o{po["org_id"]}" label="{esc(po["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(po.get("note", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(po.get("start", ""))}—{esc(po.get("end", "present"))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    # edges: relationships
    for r in relationships:
        weight = "2.0" if r["strength"] in ("强",) else "1.5"
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# =========================================================================
# MAIN
# =========================================================================
def main():
    build_db()
    build_gexf()
    stats = {
        "persons": len(persons),
        "organizations": len(organizations),
        "positions": len(positions),
        "relationships": len(relationships),
    }
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    print(f"DB:   {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    for path in (DB_PATH, GEXF_PATH):
        if os.path.exists(path):
            print(f"  OK  {path} ({os.path.getsize(path)} bytes)")
        else:
            print(f"  MISSING {path}")

if __name__ == "__main__":
    main()