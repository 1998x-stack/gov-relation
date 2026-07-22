#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
南雄市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县级市
Province: 广东省
Parent City: 韶关市
Region: 南雄市
Targets: 市委书记 & 市长

Research Sources:
- 南雄市人民政府公众信息网 (www.gdnx.gov.cn) — 领导之窗页面, 2026年7月确认
- 南雄市人民政府公众信息网 — 新闻动态 (2026年6-7月)
- 南雄市人民政府公众信息网 — 2026年政府工作报告

Current status (as of 2026-07-22):
- 市委书记: 柯建忠（1977年2月生）
- 市长: 陈冰（1981年2月生）

Research Date: 2026-07-22
"""

import json
import os
import sqlite3
from datetime import datetime

# ── 路径 ──────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "南雄市_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "南雄市_network.gexf")

# ── 数据 ──────────────────────────────────────────────

# 1. 人员
persons = [
    # ════════════════════════════════════════
    # 市委领导
    # ════════════════════════════════════════
    {
        "id": "p01",
        "name": "柯建忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年2月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共南雄市委书记",
        "current_org": "中共南雄市委员会",
        "source": "南雄市人民政府公众信息网(gdnx.gov.cn)领导之窗, 2026-07",
    },
    {
        "id": "p02",
        "name": "陈冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年2月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生/理学硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共南雄市委副书记、市长",
        "current_org": "南雄市人民政府",
        "source": "南雄市人民政府公众信息网(gdnx.gov.cn)领导之窗, 2026-07",
    },
    {
        "id": "p03",
        "name": "林军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共南雄市委副书记",
        "current_org": "中共南雄市委员会",
        "source": "南雄市人民政府公众信息网(gdnx.gov.cn)领导之窗, 2026-07",
    },
    {
        "id": "p04",
        "name": "雷伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共南雄市委副书记（挂职）",
        "current_org": "中共南雄市委员会",
        "source": "南雄市人民政府公众信息网(gdnx.gov.cn)领导之窗, 2026-07",
    },
    {
        "id": "p05",
        "name": "叶志明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共南雄市委常委、纪委书记、市监委主任",
        "current_org": "中共南雄市纪律检查委员会",
        "source": "南雄市人民政府公众信息网(gdnx.gov.cn)领导之窗, 2026-07",
    },
    {
        "id": "p06",
        "name": "温春花",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共南雄市委常委、宣传部部长",
        "current_org": "中共南雄市委宣传部",
        "source": "南雄市人民政府公众信息网(gdnx.gov.cn)领导之窗, 2026-07",
    },
    {
        "id": "p07",
        "name": "杨耀轩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共南雄市委常委、统战部部长",
        "current_org": "中共南雄市委统战部",
        "source": "南雄市人民政府公众信息网(gdnx.gov.cn)领导之窗, 2026-07",
    },
    {
        "id": "p08",
        "name": "石为",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共南雄市委常委、市委办公室主任",
        "current_org": "中共南雄市委办公室",
        "source": "南雄市人民政府公众信息网(gdnx.gov.cn)领导之窗, 2026-07",
    },
    {
        "id": "p09",
        "name": "吴宏文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共南雄市委常委、组织部部长",
        "current_org": "中共南雄市委组织部",
        "source": "南雄市人民政府公众信息网(gdnx.gov.cn)领导之窗, 2026-07",
    },
    {
        "id": "p10",
        "name": "胡春陵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共南雄市委常委、政法委书记",
        "current_org": "中共南雄市委政法委员会",
        "source": "南雄市人民政府公众信息网(gdnx.gov.cn)领导之窗, 2026-07",
    },
    # ════════════════════════════════════════
    # 市政府领导
    # ════════════════════════════════════════
    {
        "id": "p11",
        "name": "赖永兴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "南雄市人民政府副市长",
        "current_org": "南雄市人民政府",
        "source": "南雄市人民政府公众信息网(gdnx.gov.cn)领导之窗, 2026-07",
    },
    {
        "id": "p12",
        "name": "朱慧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "南雄市人民政府副市长",
        "current_org": "南雄市人民政府",
        "source": "南雄市人民政府公众信息网(gdnx.gov.cn)领导之窗, 2026-07",
    },
    {
        "id": "p13",
        "name": "许洪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "南雄市人民政府副市长",
        "current_org": "南雄市人民政府",
        "source": "南雄市人民政府公众信息网(gdnx.gov.cn)领导之窗, 2026-07",
    },
    {
        "id": "p14",
        "name": "刘春伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "南雄市人民政府副市长",
        "current_org": "南雄市人民政府",
        "source": "南雄市人民政府公众信息网(gdnx.gov.cn)领导之窗, 2026-07",
    },
    {
        "id": "p15",
        "name": "翟普尧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "南雄市人民政府副市长",
        "current_org": "南雄市人民政府",
        "source": "南雄市人民政府公众信息网(gdnx.gov.cn)领导之窗, 2026-07",
    },
    {
        "id": "p16",
        "name": "于高产",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "南雄市人民政府副市长（可供参考）",
        "current_org": "南雄市人民政府",
        "source": "南雄市人民政府公众信息网(gdnx.gov.cn)政府常务会议新闻, 2026-07",
    },
    {
        "id": "p17",
        "name": "李指源",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "南雄市人民政府副市长（可供参考）",
        "current_org": "南雄市人民政府",
        "source": "南雄市人民政府公众信息网(gdnx.gov.cn)政府常务会议新闻, 2026-07",
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共南雄市委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共韶关市委员会",
        "location": "南雄市雄州街道",
    },
    {
        "id": 2,
        "name": "南雄市人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "韶关市人民政府",
        "location": "南雄市雄州街道",
    },
    {
        "id": 3,
        "name": "中共南雄市纪律检查委员会（南雄市监察委员会）",
        "type": "纪委",
        "level": "县级",
        "parent": "中共韶关市纪律检查委员会",
        "location": "南雄市雄州街道",
    },
    {
        "id": 4,
        "name": "中共南雄市委宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共南雄市委员会",
        "location": "南雄市雄州街道",
    },
    {
        "id": 5,
        "name": "中共南雄市委统战部",
        "type": "党委",
        "level": "县级",
        "parent": "中共南雄市委员会",
        "location": "南雄市雄州街道",
    },
    {
        "id": 6,
        "name": "中共南雄市委办公室",
        "type": "党委",
        "level": "县级",
        "parent": "中共南雄市委员会",
        "location": "南雄市雄州街道",
    },
    {
        "id": 7,
        "name": "中共南雄市委组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共南雄市委员会",
        "location": "南雄市雄州街道",
    },
    {
        "id": 8,
        "name": "中共南雄市委政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共南雄市委员会",
        "location": "南雄市雄州街道",
    },
]

# 3. Positions (person_id, org_id, title, start, end, rank, note)
positions = [
    # 柯建忠（市委书记）
    {"person_id": "p01", "org_id": 1, "title": "中共南雄市委书记", "start": "待查", "end": "present", "rank": "县处级正职", "note": ""},

    # 陈冰（市长）
    {"person_id": "p02", "org_id": 2, "title": "南雄市人民政府市长", "start": "待查", "end": "present", "rank": "县处级正职", "note": ""},
    {"person_id": "p02", "org_id": 1, "title": "中共南雄市委副书记", "start": "待查", "end": "present", "rank": "县处级正职", "note": "市长兼任市委副书记"},

    # 林军（副书记）
    {"person_id": "p03", "org_id": 1, "title": "中共南雄市委副书记", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},

    # 雷伟（挂职副书记）
    {"person_id": "p04", "org_id": 1, "title": "中共南雄市委副书记（挂职）", "start": "待查", "end": "present", "rank": "县处级副职", "note": "挂职"},

    # 叶志明（纪委书记）
    {"person_id": "p05", "org_id": 3, "title": "中共南雄市委常委、纪委书记、市监委主任", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": "p05", "org_id": 1, "title": "中共南雄市委常委", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},

    # 温春花（宣传部长）
    {"person_id": "p06", "org_id": 4, "title": "中共南雄市委常委、宣传部部长", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": "p06", "org_id": 1, "title": "中共南雄市委常委", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},

    # 杨耀轩（统战部长）
    {"person_id": "p07", "org_id": 5, "title": "中共南雄市委常委、统战部部长", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": "p07", "org_id": 1, "title": "中共南雄市委常委", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},

    # 石为（市委办公室主任）
    {"person_id": "p08", "org_id": 6, "title": "中共南雄市委常委、市委办公室主任", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": "p08", "org_id": 1, "title": "中共南雄市委常委", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},

    # 吴宏文（组织部长）
    {"person_id": "p09", "org_id": 7, "title": "中共南雄市委常委、组织部部长", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": "p09", "org_id": 1, "title": "中共南雄市委常委", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},

    # 胡春陵（政法委书记）
    {"person_id": "p10", "org_id": 8, "title": "中共南雄市委常委、政法委书记", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": "p10", "org_id": 1, "title": "中共南雄市委常委", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},

    # 副市长们
    {"person_id": "p11", "org_id": 2, "title": "南雄市人民政府副市长", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": "p12", "org_id": 2, "title": "南雄市人民政府副市长", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": "p13", "org_id": 2, "title": "南雄市人民政府副市长", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": "p14", "org_id": 2, "title": "南雄市人民政府副市长", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": "p15", "org_id": 2, "title": "南雄市人民政府副市长", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": "p16", "org_id": 2, "title": "南雄市人民政府副市长", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": "p17", "org_id": 2, "title": "南雄市人民政府副市长", "start": "待查", "end": "present", "rank": "县处级副职", "note": ""},
]

# 4. Relationships
relationships = [
    # 党政正职搭档
    {"person_a": "p01", "person_b": "p02", "type": "党政正职搭档", "context": "市委书记与市长是县级市最重要的党政搭档", "overlap_org": "中共南雄市委员会/南雄市人民政府", "overlap_period": "2026年在任", "strength": "strong", "confidence": "confirmed"},

    # 市委副书记+书记
    {"person_a": "p01", "person_b": "p03", "type": "上下级", "context": "市委书记与市委副书记的工作关系", "overlap_org": "中共南雄市委员会", "overlap_period": "2026年在任", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p04", "type": "上下级", "context": "市委书记与挂职副书记的工作关系", "overlap_org": "中共南雄市委员会", "overlap_period": "2026年在任", "strength": "medium", "confidence": "confirmed"},

    # 纪委书记+书记
    {"person_a": "p01", "person_b": "p05", "type": "上下级", "context": "市委书记与纪委书记的监督与被监督关系", "overlap_org": "中共南雄市委员会", "overlap_period": "2026年在任", "strength": "strong", "confidence": "confirmed"},

    # 常委间关系（同一届常委班子成员）
    {"person_a": "p06", "person_b": "p07", "type": "同系统", "context": "宣传部与统战部均为市委工作部门，两部长同为市委常委", "overlap_org": "中共南雄市委员会", "overlap_period": "2026年在任", "strength": "medium", "confidence": "confirmed"},
    {"person_a": "p06", "person_b": "p09", "type": "同系统", "context": "宣传部与组织部均为市委工作部门", "overlap_org": "中共南雄市委员会", "overlap_period": "2026年在任", "strength": "medium", "confidence": "confirmed"},
    {"person_a": "p09", "person_b": "p10", "type": "同系统", "context": "组织部与政法委均为市委工作部门", "overlap_org": "中共南雄市委员会", "overlap_period": "2026年在任", "strength": "medium", "confidence": "confirmed"},

    # 市长+副市长
    {"person_a": "p02", "person_b": "p11", "type": "上下级", "context": "市长与副市长的工作关系", "overlap_org": "南雄市人民政府", "overlap_period": "2026年在任", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p02", "person_b": "p12", "type": "上下级", "context": "市长与副市长的工作关系", "overlap_org": "南雄市人民政府", "overlap_period": "2026年在任", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p02", "person_b": "p13", "type": "上下级", "context": "市长与副市长的工作关系", "overlap_org": "南雄市人民政府", "overlap_period": "2026年在任", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p02", "person_b": "p14", "type": "上下级", "context": "市长与副市长的工作关系", "overlap_org": "南雄市人民政府", "overlap_period": "2026年在任", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p02", "person_b": "p15", "type": "上下级", "context": "市长与副市长的工作关系", "overlap_org": "南雄市人民政府", "overlap_period": "2026年在任", "strength": "strong", "confidence": "confirmed"},
]


# ── 辅助函数 ──────────────────────────────────────────

def esc(s):
    """XML转义"""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """按角色返回RGB颜色"""
    title = p["current_post"]
    if "书记" in title and "纪委" not in title and "统战" not in title:
        if "副书记" in title:
            return "200,50,50"   # 暗红 — 副职
        return "255,50,50"   # 红色 — 党委正职
    if "市长" in title and "副市长" not in title:
        return "50,100,255"  # 蓝色 — 政府正职
    if "纪委" in title or "监委" in title:
        return "255,165,0"   # 橙色 — 纪检
    if "常委" in title:
        return "200,100,100" # 粉红 — 其他常委
    if "副市长" in title:
        return "80,80,200"   # 蓝紫 — 副市长
    return "100,100,100"     # 灰色 — 其他


def person_size(p):
    """按角色返回节点大小"""
    title = p["current_post"]
    if "市委书记" in title or ("市长" in title and "副市长" not in title):
        return "20.0"
    if "副书记" in title or "常委" in title:
        return "14.0"
    if "副市长" in title:
        return "12.0"
    return "10.0"


def org_color(o):
    """按类型返回组织颜色"""
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "纪委": "255,165,0",
    }
    return colors.get(t, "200,200,200")


# ── 构建数据库 ────────────────────────────────────────

def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS persons (
        id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, native_place TEXT, education TEXT,
        party_join TEXT, work_start TEXT, current_post TEXT,
        current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT, org_id TEXT, title TEXT,
        start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT, person_b TEXT, type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT, strength TEXT, confidence TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    c.execute("DELETE FROM persons")
    c.execute("DELETE FROM organizations")
    c.execute("DELETE FROM positions")
    c.execute("DELETE FROM relationships")

    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            p["id"], p["name"], p["gender"], p["ethnicity"],
            p["birth"], p["birthplace"], p["native_place"], p["education"],
            p["party_join"], p["work_start"], p["current_post"],
            p["current_org"], p["source"]
        ))

    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""", (
            str(o["id"]), o["name"], o["type"], o["level"], o["parent"], o["location"]
        ))

    for pos in positions:
        c.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
                     VALUES (?,?,?,?,?,?,?)""", (
            pos["person_id"], str(pos["org_id"]), pos["title"],
            pos["start"], pos["end"], pos["rank"], pos["note"]
        ))

    for r in relationships:
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence)
                     VALUES (?,?,?,?,?,?,?,?)""", (
            r["person_a"], r["person_b"], r["type"], r["context"],
            r["overlap_org"], r["overlap_period"], r.get("strength", "medium"), r.get("confidence", "plausible")
        ))

    conn.commit()
    conn.close()


# ── 构建 GEXF ─────────────────────────────────────────

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>南雄市领导班子工作关系网络 - 数据来源: 南雄市人民政府公众信息网(gdnx.gov.cn)</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="province" type="string"/>')
    lines.append('      <attribute id="3" title="city" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('          <attvalue for="2" value="广东省"/>')
        lines.append('          <attvalue for="3" value="南雄市"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{str(o["id"])}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('          <attvalue for="2" value="广东省"/>')
        lines.append('          <attvalue for="3" value="南雄市"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person→Organization (worked_at)
    for pos in positions:
        eid += 1
        weight = "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person↔Person (relationship)
    for r in relationships:
        eid += 1
        weight = "2.0"
        conf = r.get("confidence", "plausible")
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{conf}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ── 主函数 ──────────────────────────────────────────

def main():
    print(f"=== 南雄市网络数据构建 ===")
    print(f"人员: {len(persons)} 人")
    print(f"组织机构: {len(organizations)} 个")
    print(f"任职记录: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")

    print(f"\n构建数据库...")
    build_db()
    db_size = os.path.getsize(DB_PATH)
    print(f"  ✓ {DB_PATH} ({db_size} bytes)")

    print(f"构建GEXF图文件...")
    build_gexf()
    gexf_size = os.path.getsize(GEXF_PATH)
    print(f"  ✓ {GEXF_PATH} ({gexf_size} bytes)")

    print(f"\n=== 完成 ===")


if __name__ == "__main__":
    main()
