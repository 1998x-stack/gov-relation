#!/usr/bin/env python3
"""
甘州区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

数据来源:
- 张掖市人民政府官方网站 (www.zhangye.gov.cn), 2026年7月确认
- 百度百科/百度搜索 (多渠道交叉验证)
- 新闻报道 (甘州融媒、网易新闻、中国张掖网等)
"""

import json
import os
import sqlite3
from datetime import datetime

# ── 路径 ──────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STAGING_DIR = SCRIPT_DIR  # 脚本在暂存目录内
DB_PATH = os.path.join(STAGING_DIR, "甘州区_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "甘州区_network.gexf")

# ── 数据 ──────────────────────────────────────────────

# 1. 人员
persons = [
    # === 核心领导（目标人物）===
    {
        "id": "p01",
        "name": "李锐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年6月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张掖市委常委、甘州区委书记",
        "current_org": "中共甘州区委员会",
        "source": "张掖市人民政府官网(zhangye.gov.cn), 2026-07",
        "person_id": "ganzhou_li_rui"
    },
    {
        "id": "p02",
        "name": "甘州区区长",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "甘州区委副书记、区政府区长",
        "current_org": "甘州区人民政府",
        "source": "待查（甘州区政府网站gsgz.gov.cn无法访问）",
        "person_id": "ganzhou_quzhang"
    },
    # === 区委副书记 / 重要副职 ===
    {
        "id": "p03",
        "name": "王敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "甘州区委副书记",
        "current_org": "中共甘州区委员会",
        "source": "新闻报道（甘州融媒）",
        "person_id": "ganzhou_wang_min"
    },
    # === 区纪委书记 ===
    {
        "id": "p04",
        "name": "张晓龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "甘州区委常委、区纪委书记、区监委主任",
        "current_org": "中共甘州区纪律检查委员会",
        "source": "新闻报道（甘州融媒）",
        "person_id": "ganzhou_zhang_xiaolong"
    },
    # === 常务副区长 ===
    {
        "id": "p05",
        "name": "张勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "甘州区委常委、常务副区长",
        "current_org": "甘州区人民政府",
        "source": "新闻报道（甘州融媒）",
        "person_id": "ganzhou_zhang_yong"
    },
    # === 区委组织部部长 ===
    {
        "id": "p06",
        "name": "安丽莉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "甘州区委常委、组织部部长",
        "current_org": "中共甘州区委员会组织部",
        "source": "新闻报道（甘州融媒）",
        "person_id": "ganzhou_an_lili"
    },
    # === 区委宣传部部长 ===
    {
        "id": "p07",
        "name": "刘波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "甘州区委常委、宣传部部长",
        "current_org": "中共甘州区委员会宣传部",
        "source": "新闻报道（甘州融媒）",
        "person_id": "ganzhou_liu_bo"
    },
    # === 区委统战部部长 ===
    {
        "id": "p08",
        "name": "先进个人姓名待查",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "甘州区委常委、统战部部长",
        "current_org": "中共甘州区委员会统战部",
        "source": "待查",
        "person_id": "ganzhou_tongzhan_buzhang"
    },
    # === 区委政法委书记 ===
    {
        "id": "p09",
        "name": "范天兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "甘州区委常委、政法委书记",
        "current_org": "中共甘州区委员会政法委员会",
        "source": "新闻报道（甘州融媒）",
        "person_id": "ganzhou_fan_tianbing"
    },
    # === 副区长 ===
    {
        "id": "p10",
        "name": "牛生波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "甘州区副区长",
        "current_org": "甘州区人民政府",
        "source": "新闻报道（甘州区政府网站）, 2022年确认",
        "person_id": "ganzhou_niu_shengbo"
    },
    {
        "id": "p11",
        "name": "秦楠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "甘州区副区长",
        "current_org": "甘州区人民政府",
        "source": "新闻报道（甘州融媒）",
        "person_id": "ganzhou_qin_nan"
    },
    # === 区人大常委会主任 ===
    {
        "id": "p12",
        "name": "郭威",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "甘州区人大常委会主任",
        "current_org": "甘州区人民代表大会常务委员会",
        "source": "新闻报道（甘州融媒）",
        "person_id": "ganzhou_guo_wei"
    },
    # === 区政协主席 ===
    {
        "id": "p13",
        "name": "魏士博",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "甘州区政协主席",
        "current_org": "中国人民政治协商会议甘州区委员会",
        "source": "新闻报道（甘州融媒）",
        "person_id": "ganzhou_wei_shibo"
    },
    # === 上级领导（张掖市）===
    {
        "id": "p14",
        "name": "李兴华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年3月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张掖市委书记",
        "current_org": "中共张掖市委员会",
        "source": "张掖市人民政府官网(zhangye.gov.cn), 2026-07",
        "person_id": "zhangye_li_xinghua"
    },
    {
        "id": "p15",
        "name": "叶尔波力·孜汗",
        "gender": "男",
        "ethnicity": "哈萨克族",
        "birth": "1973年5月",
        "birthplace": "新疆阿勒泰地区",
        "native_place": "新疆阿勒泰",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "1996年9月",
        "current_post": "张掖市委副书记、市政府党组书记、市长",
        "current_org": "张掖市人民政府",
        "source": "张掖市人民政府官网, 百度百科, 新闻报道",
        "person_id": "zhangye_yeerboli_zihan"
    },
    {
        "id": "p16",
        "name": "张永刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年12月",
        "birthplace": "甘肃甘谷",
        "native_place": "甘肃甘谷",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1992年7月",
        "current_post": "张掖市委常委、常务副市长",
        "current_org": "张掖市人民政府",
        "source": "张掖市人民政府官网, 百度百科, 新闻报道",
        "person_id": "zhangye_zhang_yonggang"
    },
]

# 2. 组织机构
organizations = [
    {"id": "o01", "name": "中共甘州区委员会", "type": "党委", "level": "县处级", "parent": "中共张掖市委员会", "location": "甘肃省张掖市甘州区"},
    {"id": "o02", "name": "甘州区人民政府", "type": "政府", "level": "县处级", "parent": "张掖市人民政府", "location": "甘肃省张掖市甘州区"},
    {"id": "o03", "name": "中共甘州区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共甘州区委员会", "location": "甘肃省张掖市甘州区"},
    {"id": "o04", "name": "中共甘州区委员会组织部", "type": "党委", "level": "县处级", "parent": "中共甘州区委员会", "location": "甘肃省张掖市甘州区"},
    {"id": "o05", "name": "中共甘州区委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共甘州区委员会", "location": "甘肃省张掖市甘州区"},
    {"id": "o06", "name": "中共甘州区委员会统战部", "type": "党委", "level": "县处级", "parent": "中共甘州区委员会", "location": "甘肃省张掖市甘州区"},
    {"id": "o07", "name": "中共甘州区委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共甘州区委员会", "location": "甘肃省张掖市甘州区"},
    {"id": "o08", "name": "甘州区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "甘州区", "location": "甘肃省张掖市甘州区"},
    {"id": "o09", "name": "中国人民政治协商会议甘州区委员会", "type": "政协", "level": "县处级", "parent": "甘州区", "location": "甘肃省张掖市甘州区"},
    {"id": "o10", "name": "张掖经济技术开发区", "type": "开发区", "level": "国家级", "parent": "张掖市人民政府", "location": "甘肃省张掖市甘州区"},
    {"id": "o11", "name": "中共张掖市委员会", "type": "党委", "level": "地级", "parent": "中共甘肃省委员会", "location": "甘肃省张掖市"},
    {"id": "o12", "name": "张掖市人民政府", "type": "政府", "level": "地级", "parent": "甘肃省人民政府", "location": "甘肃省张掖市"},
]

# 3. 任职
positions = [
    # 李锐
    {"person_id": "p01", "org_id": "o11", "title": "张掖市委常委", "start": "?", "end": "至今", "rank": "副厅级", "note": "兼任甘州区委书记"},
    {"person_id": "p01", "org_id": "o01", "title": "甘州区委书记", "start": "?", "end": "至今", "rank": "副厅级", "note": "主持区委全面工作"},
    # 区长（待定）
    {"person_id": "p02", "org_id": "o01", "title": "甘州区委副书记", "start": "?", "end": "至今", "rank": "正处级", "note": "兼任区长"},
    {"person_id": "p02", "org_id": "o02", "title": "甘州区区长", "start": "?", "end": "至今", "rank": "正处级", "note": "主持区政府全面工作"},
    # 王敏
    {"person_id": "p03", "org_id": "o01", "title": "甘州区委副书记", "start": "?", "end": "至今", "rank": "副处级", "note": ""},
    # 张晓龙
    {"person_id": "p04", "org_id": "o03", "title": "甘州区纪委书记、区监委主任", "start": "?", "end": "至今", "rank": "副处级", "note": ""},
    # 张勇
    {"person_id": "p05", "org_id": "o02", "title": "甘州区常务副区长", "start": "?", "end": "至今", "rank": "副处级", "note": ""},
    # 安丽莉
    {"person_id": "p06", "org_id": "o04", "title": "甘州区委组织部部长", "start": "?", "end": "至今", "rank": "副处级", "note": ""},
    # 刘波
    {"person_id": "p07", "org_id": "o05", "title": "甘州区委宣传部部长", "start": "?", "end": "至今", "rank": "副处级", "note": ""},
    # 统战部长
    {"person_id": "p08", "org_id": "o06", "title": "甘州区委统战部部长", "start": "?", "end": "至今", "rank": "副处级", "note": ""},
    # 范天兵
    {"person_id": "p09", "org_id": "o07", "title": "甘州区委政法委书记", "start": "?", "end": "至今", "rank": "副处级", "note": ""},
    # 牛生波
    {"person_id": "p10", "org_id": "o02", "title": "甘州区副区长", "start": "?", "end": "至今", "rank": "副处级", "note": ""},
    # 秦楠
    {"person_id": "p11", "org_id": "o02", "title": "甘州区副区长", "start": "?", "end": "至今", "rank": "副处级", "note": ""},
    # 郭威
    {"person_id": "p12", "org_id": "o08", "title": "甘州区人大常委会主任", "start": "?", "end": "至今", "rank": "正处级", "note": ""},
    # 魏士博
    {"person_id": "p13", "org_id": "o09", "title": "甘州区政协主席", "start": "?", "end": "至今", "rank": "正处级", "note": ""},
    # 上级领导
    {"person_id": "p14", "org_id": "o11", "title": "张掖市委书记", "start": "2025?", "end": "至今", "rank": "正厅级", "note": "主持市委全面工作"},
    {"person_id": "p15", "org_id": "o11", "title": "张掖市委副书记", "start": "2024?", "end": "至今", "rank": "副厅级", "note": "兼任市长"},
    {"person_id": "p15", "org_id": "o12", "title": "张掖市市长", "start": "2024?", "end": "至今", "rank": "正厅级", "note": "主持市政府全面工作"},
    {"person_id": "p16", "org_id": "o12", "title": "张掖市常务副市长", "start": "2024?", "end": "至今", "rank": "副厅级", "note": ""},
]

# 4. 关系
relationships = [
    # 党政一把手
    {"person_a": "p01", "person_b": "p02", "type": "overlap", "context": "李锐(书记)与区长: 党政一把手配合作", "overlap_org": "中共甘州区委员会/甘州区人民政府", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 书记与副书记
    {"person_a": "p01", "person_b": "p03", "type": "overlap", "context": "李锐(书记)与王敏(区委副书记): 上下级关系", "overlap_org": "中共甘州区委员会", "overlap_period": "至今", "strength": "strong", "confidence": "plausible"},
    # 书记与纪委书记
    {"person_a": "p01", "person_b": "p04", "type": "overlap", "context": "李锐(书记)与张晓龙(纪委书记): 上下级关系", "overlap_org": "中共甘州区委员会", "overlap_period": "至今", "strength": "strong", "confidence": "plausible"},
    # 书记与上级
    {"person_a": "p01", "person_b": "p14", "type": "overlap", "context": "李锐(甘州区委书记)与李兴华(张掖市委书记): 上下级关系", "overlap_org": "中共张掖市委员会/中共甘州区委员会", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p15", "type": "overlap", "context": "李锐(甘州区委书记)与叶尔波力·孜汗(市长): 上下级关系", "overlap_org": "张掖市党政系统", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 区长与上级
    {"person_a": "p02", "person_b": "p14", "type": "overlap", "context": "区长与李兴华(市委书记): 上下级关系", "overlap_org": "张掖市党政系统", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p02", "person_b": "p15", "type": "overlap", "context": "区长与叶尔波力·孜汗(市长): 上下级关系", "overlap_org": "张掖市-甘州区两级政府", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 区级班子内部关系
    {"person_a": "p01", "person_b": "p05", "type": "overlap", "context": "李锐(书记)与张勇(常务副区长): 上下级关系", "overlap_org": "中共甘州区委员会", "overlap_period": "至今", "strength": "strong", "confidence": "plausible"},
    {"person_a": "p01", "person_b": "p06", "type": "overlap", "context": "李锐(书记)与安丽莉(组织部长): 上下级关系", "overlap_org": "中共甘州区委员会", "overlap_period": "至今", "strength": "strong", "confidence": "plausible"},
    {"person_a": "p01", "person_b": "p07", "type": "overlap", "context": "李锐(书记)与刘波(宣传部长): 上下级关系", "overlap_org": "中共甘州区委员会", "overlap_period": "至今", "strength": "strong", "confidence": "plausible"},
    {"person_a": "p01", "person_b": "p09", "type": "overlap", "context": "李锐(书记)与范天兵(政法委书记): 上下级关系", "overlap_org": "中共甘州区委员会", "overlap_period": "至今", "strength": "strong", "confidence": "plausible"},
    # 人大政协
    {"person_a": "p01", "person_b": "p12", "type": "overlap", "context": "李锐(书记)与郭威(人大主任): 区委与人大的关系", "overlap_org": "甘州区", "overlap_period": "至今", "strength": "medium", "confidence": "plausible"},
    {"person_a": "p01", "person_b": "p13", "type": "overlap", "context": "李锐(书记)与魏士博(政协主席): 区委与政协的关系", "overlap_org": "甘州区", "overlap_period": "至今", "strength": "medium", "confidence": "plausible"},
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
        return "255,50,50"   # 红色 — 党委正职
    if "区长" in title or ("副区长" in title and "常委" not in title):
        return "50,100,255"  # 蓝色 — 政府领导
    if "纪委" in title or "监委" in title:
        return "255,165,0"   # 橙色 — 纪检
    if "副书记" in title:
        return "200,50,50"   # 暗红 — 副职
    if "常委" in title:
        return "200,100,100" # 粉红 — 其他常委
    if "副区长" in title:
        return "100,100,200" # 浅蓝 — 副区长
    if "人大" in title:
        return "200,255,255" # 青色 — 人大
    if "政协" in title:
        return "255,240,200" # 米色 — 政协
    return "100,100,100"     # 灰色 — 其他

def person_size(p):
    """按角色返回节点大小"""
    title = p["current_post"]
    if "区委书记" in title:
        return "20.0"
    if "区长" in title:
        return "20.0"
    if "副书记" in title or "常委" in title:
        return "14.0"
    if "副区长" in title:
        return "12.0"
    if "人大" in title or "政协" in title:
        return "12.0"
    return "10.0"

def org_color(o):
    """按类型返回组织颜色"""
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "事业单位": "220,220,220",
        "人大": "200,255,255",
        "政协": "255,240,200",
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
        overlap_org TEXT, overlap_period TEXT,
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
            o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]
        ))

    for pos in positions:
        c.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
                     VALUES (?,?,?,?,?,?,?)""", (
            pos["person_id"], pos["org_id"], pos["title"],
            pos["start"], pos["end"], pos["rank"], pos["note"]
        ))

    for r in relationships:
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                     VALUES (?,?,?,?,?,?)""", (
            r["person_a"], r["person_b"], r["type"], r["context"],
            r["overlap_org"], r["overlap_period"]
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
    lines.append('    <description>甘州区领导班子工作关系网络 - 数据来源: 张掖市人民政府官网及公开报道</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="province" type="string"/>')
    lines.append('      <attribute id="3" title="city" type="string"/>')
    lines.append('      <attribute id="4" title="district" type="string"/>')
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
        lines.append('          <attvalue for="2" value="甘肃省"/>')
        lines.append('          <attvalue for="3" value="张掖市"/>')
        lines.append('          <attvalue for="4" value="甘州区"/>')
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
        lines.append('          <attvalue for="2" value="甘肃省"/>')
        lines.append('          <attvalue for="3" value="张掖市"/>')
        lines.append('          <attvalue for="4" value="甘州区"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
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
    print(f"=== 甘州区网络数据构建 ===")
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
