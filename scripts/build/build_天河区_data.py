#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天河区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 广州市
Region: 天河区
Targets: 区委书记 & 区长

Research Sources:
- 广州市天河区人民政府门户网站 (www.thnet.gov.cn) — 领导之窗: 区政府领导分工与简历
- 南方+ 新闻报道 — 确认区委书记谭明鹤 (2026年2月高质量发展大会报道)
- 天河区人民政府门户网站 — 区长陈建荣简历页 (2026年7月更新)
- 天河区人民政府门户网站 — 区政府领导分工

Research Date: 2026-07-22
"""

import os
import sqlite3
from datetime import datetime

# ── Paths ──
BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/guangdong_天河区")
DB_PATH = os.path.join(TMP, "天河区_network.db")
GEXF_PATH = os.path.join(TMP, "天河区_network.gexf")

# ════════════════════════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════════════════════════

persons = [
    # ── 1. Current Top Leaders ──
    {
        "id": 1,
        "name": "谭明鹤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天河区委书记",
        "current_org": "中共广州市天河区委员会",
        "source": "南方+ 报道 — 天河区委书记谭明鹤在2026年天河区高质量发展大会上讲话 (2026-02-27)"
    },
    {
        "id": 2,
        "name": "陈建荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年2月",
        "birthplace": "江苏江阴",
        "native_place": "江苏江阴",
        "education": "大学学历，经济学硕士",
        "party_join": "中共党员",
        "work_start": "1990年7月",
        "current_post": "天河区委副书记、区政府党组书记、区长",
        "current_org": "广州市天河区人民政府",
        "source": "www.thnet.gov.cn 领导之窗—区长简历 (2026年7月更新)"
    },
    # ── 2. Deputy Government Leaders (from thnet.gov.cn) ──
    {
        "id": 3,
        "name": "黄卓丰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天河区委常委、区政府党组副书记、常务副区长",
        "current_org": "广州市天河区人民政府",
        "source": "www.thnet.gov.cn 领导之窗—常务副区长"
    },
    {
        "id": 4,
        "name": "刘庆进",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天河区委常委、区政府党组成员、副区长",
        "current_org": "广州市天河区人民政府",
        "source": "www.thnet.gov.cn 领导之窗—副区长"
    },
    {
        "id": 5,
        "name": "黄新锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天河区政府党组成员、副区长",
        "current_org": "广州市天河区人民政府",
        "source": "www.thnet.gov.cn 领导之窗—副区长 (2026-07-08更新)"
    },
    {
        "id": 6,
        "name": "焦志伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天河区政府党组成员、副区长（公安分局局长）",
        "current_org": "广州市公安局天河区分局",
        "source": "www.thnet.gov.cn 领导之窗—副区长"
    },
    {
        "id": 7,
        "name": "陈志宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天河区政府党组成员、副区长",
        "current_org": "广州市天河区人民政府",
        "source": "www.thnet.gov.cn 领导之窗—副区长"
    },
    {
        "id": 8,
        "name": "袁笑一",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天河区政府党组成员、副区长",
        "current_org": "广州市天河区人民政府",
        "source": "www.thnet.gov.cn 领导之窗—副区长"
    },
    {
        "id": 9,
        "name": "邓萍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天河区副区长",
        "current_org": "广州市天河区人民政府",
        "source": "www.thnet.gov.cn 领导之窗—副区长"
    },
    # ── 3. Key Party Committee Leaders ──
    {
        "id": 10,
        "name": "杨海涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天河区委常委、组织部部长",
        "current_org": "中共广州市天河区委组织部",
        "source": "天河区十届区委第十四轮巡察动员部署会报道 (2026-06-26)"
    },
    {
        "id": 11,
        "name": "戴小松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天河区纪委副书记、监委副主任",
        "current_org": "中共广州市天河区纪律检查委员会",
        "source": "天河区十届区委第十四轮巡察动员部署会报道 (2026-06-26)"
    },
    {
        "id": 12,
        "name": "王异军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "天河区委组织部副部长",
        "current_org": "中共广州市天河区委组织部",
        "source": "天河区十届区委第十四轮巡察动员部署会报道 (2026-06-26)"
    },
]

organizations = [
    {"id": 1, "name": "中共广州市天河区委员会", "type": "党委", "level": "县处级",
     "parent": "中共广州市委员会", "location": "广东省广州市天河区"},
    {"id": 2, "name": "广州市天河区人民政府", "type": "政府", "level": "县处级",
     "parent": "广州市人民政府", "location": "广东省广州市天河区"},
    {"id": 3, "name": "广州市公安局天河区分局", "type": "政府", "level": "乡科级",
     "parent": "广州市公安局", "location": "广东省广州市天河区"},
    {"id": 4, "name": "中共广州市天河区委组织部", "type": "党委", "level": "乡科级",
     "parent": "中共广州市天河区委员会", "location": "广东省广州市天河区"},
    {"id": 5, "name": "中共广州市天河区纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共广州市天河区委员会", "location": "广东省广州市天河区"},
    {"id": 6, "name": "天河区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "广州市人大常委会", "location": "广东省广州市天河区"},
    {"id": 7, "name": "中国人民政治协商会议广州市天河区委员会", "type": "政协", "level": "县处级",
     "parent": "广州市政协", "location": "广东省广州市天河区"},
    {"id": 8, "name": "天河区审计局", "type": "政府", "level": "乡科级",
     "parent": "广州市天河区人民政府", "location": "广东省广州市天河区"},
    {"id": 9, "name": "天河科技园管理委员会", "type": "事业单位", "level": "县处级",
     "parent": "广州市天河区人民政府", "location": "广东省广州市天河区"},
]

positions = [
    # ── Tan Minghe (谭明鹤) ──
    {"person_id": 1, "org_id": 1, "title": "天河区委书记", "start": "", "end": "present",
     "rank": "副厅级", "note": "2026年2月以天河区委书记身份出席天河区高质量发展大会"},
    # ── Chen Jianrong (陈建荣) ──
    {"person_id": 2, "org_id": 2, "title": "天河区委副书记、区政府党组书记、区长", "start": "", "end": "present",
     "rank": "正县级", "note": "主持区政府全面工作，负责审计、天河科技园方面工作"},
    {"person_id": 2, "org_id": 8, "title": "分管区审计局", "start": "", "end": "present",
     "rank": "", "note": ""},
    {"person_id": 2, "org_id": 9, "title": "分管天河科技园管委会", "start": "", "end": "present",
     "rank": "", "note": ""},
    # ── Huang Zhuofeng (黄卓丰) ──
    {"person_id": 3, "org_id": 2, "title": "天河区委常委、区政府党组副书记、常务副区长", "start": "", "end": "present",
     "rank": "副县级", "note": "负责发展和改革、粮食、财政、税务、国有资产、应急管理、统计、消防、国防动员、街道方面工作"},
    {"person_id": 3, "org_id": 1, "title": "天河区委常委", "start": "", "end": "present",
     "rank": "副县级", "note": ""},
    # ── Liu Qingjin (刘庆进) ──
    {"person_id": 4, "org_id": 2, "title": "天河区委常委、区政府党组成员、副区长", "start": "", "end": "present",
     "rank": "副县级", "note": "负责水务、农业农村、扶贫开发、对口帮扶、对口支援、生态环境、经济协作、供销社方面工作"},
    {"person_id": 4, "org_id": 1, "title": "天河区委常委", "start": "", "end": "present",
     "rank": "副县级", "note": ""},
    # ── Huang Xinfeng (黄新锋) ──
    {"person_id": 5, "org_id": 2, "title": "天河区政府党组成员、副区长", "start": "", "end": "present",
     "rank": "副县级", "note": "负责民族、宗教、对台、民政、文化、文物、广播电视、旅游、体育、卫生健康、信访方面工作"},
    # ── Jiao Zhiwei (焦志伟) ──
    {"person_id": 6, "org_id": 2, "title": "天河区政府党组成员、副区长（公安分局局长）", "start": "", "end": "present",
     "rank": "副县级", "note": "负责公安、司法、武装方面工作"},
    {"person_id": 6, "org_id": 3, "title": "天河区公安分局局长", "start": "", "end": "present",
     "rank": "乡科级", "note": ""},
    # ── Chen Zhihong (陈志宏) ──
    {"person_id": 7, "org_id": 2, "title": "天河区政府党组成员、副区长", "start": "", "end": "present",
     "rank": "副县级", "note": "负责住房和建设、园林、交通运输、城市管理、综合执法、规划、自然资源、东站地区管理、建设工程项目代建方面工作"},
    # ── Yuan Xiaoyi (袁笑一) ──
    {"person_id": 8, "org_id": 2, "title": "天河区政府党组成员、副区长", "start": "", "end": "present",
     "rank": "副县级", "note": "负责天河中央商务区、科学技术、工业、信息、商贸、金融、机关事务管理方面工作"},
    # ── Deng Ping (邓萍) ──
    {"person_id": 9, "org_id": 2, "title": "天河区副区长", "start": "", "end": "present",
     "rank": "副县级", "note": "负责教育、人力资源和社会保障、退役军人事务、市场监督管理、知识产权、政务数据管理、政务公开、行政审批、保密、档案、妇女儿童、地方志方面工作"},
    # ── Yang Haitao (杨海涛) ──
    {"person_id": 10, "org_id": 1, "title": "天河区委常委、组织部部长", "start": "", "end": "present",
     "rank": "副县级", "note": "区委巡察工作领导小组副组长 (2026年6月报道)"},
    {"person_id": 10, "org_id": 4, "title": "天河区委组织部部长", "start": "", "end": "present",
     "rank": "副县级", "note": ""},
    # ── Dai Xiaosong (戴小松) ──
    {"person_id": 11, "org_id": 5, "title": "天河区纪委副书记、监委副主任", "start": "", "end": "present",
     "rank": "副县级", "note": "区委巡察工作领导小组成员 (2026年6月报道)"},
    # ── Wang Yijun (王异军) ──
    {"person_id": 12, "org_id": 4, "title": "天河区委组织部副部长", "start": "", "end": "present",
     "rank": "乡科级", "note": "区委巡察工作领导小组成员 (2026年6月报道)"},
]

relationships = [
    # ── Top Leaders ──
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "strength": "strong",
     "context": "谭明鹤作为区委书记，陈建荣作为区长，是党政一把手搭档关系",
     "overlap_org": "中共广州市天河区委员会/广州市天河区人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    # ── Mayor → Deputies ──
    {"person_a": 2, "person_b": 3, "type": "overlap", "strength": "strong",
     "context": "陈建荣与黄卓丰在区政府共事，黄卓丰为常务副区长协助区长工作",
     "overlap_org": "广州市天河区人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "strength": "strong",
     "context": "陈建荣与刘庆进在区政府共事，刘庆进为区委常委、副区长",
     "overlap_org": "广州市天河区人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "strength": "medium",
     "context": "陈建荣与黄新锋在区政府共事",
     "overlap_org": "广州市天河区人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "strength": "medium",
     "context": "陈建荣与焦志伟在区政府共事，焦志伟任副区长兼公安分局局长",
     "overlap_org": "广州市天河区人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "strength": "medium",
     "context": "陈建荣与陈志宏在区政府共事",
     "overlap_org": "广州市天河区人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "strength": "medium",
     "context": "陈建荣与袁笑一在区政府共事",
     "overlap_org": "广州市天河区人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "strength": "medium",
     "context": "陈建荣与邓萍在区政府共事",
     "overlap_org": "广州市天河区人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    # ── Party Secretary → Party Committee ──
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "strength": "medium",
     "context": "谭明鹤作为区委书记，杨海涛作为区委组织部部长，为上下级关系",
     "overlap_org": "中共广州市天河区委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 10, "person_b": 12, "type": "superior_subordinate", "strength": "medium",
     "context": "杨海涛与王异军在区委组织部为上下级关系",
     "overlap_org": "中共广州市天河区委组织部",
     "overlap_period": "至今", "confidence": "confirmed"},
    # ── Same Standing Committee (区委常委共事) ──
    {"person_a": 3, "person_b": 4, "type": "overlap", "strength": "medium",
     "context": "黄卓丰与刘庆进同任区委常委",
     "overlap_org": "中共广州市天河区委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 10, "type": "overlap", "strength": "medium",
     "context": "黄卓丰与杨海涛同任区委常委",
     "overlap_org": "中共广州市天河区委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 10, "type": "overlap", "strength": "medium",
     "context": "刘庆进与杨海涛同任区委常委",
     "overlap_org": "中共广州市天河区委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    # ── Discipline Inspection ──
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "strength": "medium",
     "context": "谭明鹤作为区委书记，戴小松作为纪委副书记，为领导与被领导关系",
     "overlap_org": "中共广州市天河区委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 10, "person_b": 11, "type": "overlap", "strength": "weak",
     "context": "杨海涛与戴小松同任区委巡察工作领导小组成员",
     "overlap_org": "中共广州市天河区委员会",
     "overlap_period": "2026年", "confidence": "confirmed"},
]


# ════════════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    role = p["current_post"]
    if "区委书记" in role and "副书记" not in role:
        return "255,50,50"
    elif "区长" in role and "副书记" in role:
        return "50,100,255"
    elif "区长" in role:
        return "50,100,255"
    elif "纪委书记" in role or "纪委" in role:
        return "255,165,0"
    elif "组织部" in role:
        return "255,165,0"
    else:
        return "100,100,100"


def org_color(o):
    t = o["type"]
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }.get(t, "200,200,200")


def is_top_leader(p):
    role = p["current_post"]
    return "区委书记" in role or ("区长" in role and "副书记" in role)


def person_size(p):
    return "20.0" if is_top_leader(p) else "12.0"


# ════════════════════════════════════════════════════════════════
# BUILD DB
# ════════════════════════════════════════════════════════════════

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


# ════════════════════════════════════════════════════════════════
# BUILD GEXF
# ════════════════════════════════════════════════════════════════

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append('    <description>天河区领导班子工作关系网络 - 广东省广州市天河区</description>')
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
        w = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
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


# ════════════════════════════════════════════════════════════════
# SUMMARY
# ════════════════════════════════════════════════════════════════

def print_summary():
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()
