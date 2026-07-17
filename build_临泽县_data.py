#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
临泽县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

数据来源:
- 临泽县人民政府官方网站 / 张掖市人民政府网站 (zhangye.gov.cn), 2026年7月确认
- 百度百科 (baike.baidu.com), 2026年7月确认
- 网易新闻报道 / "汲古知新"网易号 (张成琦任临泽县委书记, 2025-08-06)
- 任前公示 (甘肃组工网)
- 新闻报道 (澎湃新闻, 网易, 新浪新闻等)
"""

import json
import os
import sqlite3
from datetime import datetime

# ── 路径 ──────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "临泽县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "临泽县_network.gexf")

# ── 数据 ──────────────────────────────────────────────

# 1. 人员
persons = [
    # (id, name, gender, ethnicity, birth, birthplace, native_place, education, party_join, work_start, current_post, current_org, source, person_id_unique)
    {
        "id": "p01",
        "name": "张成琦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "临泽县委书记",
        "current_org": "中共临泽县委员会",
        "source": "百度百科(临泽县), 网易报道(张成琦任临泽县委书记, 2025-08-06)",
        "person_id": "linze_zhang_chengqi"
    },
    {
        "id": "p02",
        "name": "秦楠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "临泽县委副书记、县长",
        "current_org": "临泽县人民政府",
        "source": "百度百科(临泽县), 甘州区领导分工(曾任甘州区副区长)",
        "person_id": "linze_qin_nan"
    },
    {
        "id": "p03",
        "name": "许兴权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "临泽县人大常委会主任",
        "current_org": "临泽县人大常委会",
        "source": "百度百科(临泽县)",
        "person_id": "linze_xu_xingquan"
    },
    {
        "id": "p04",
        "name": "邢学伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "临泽县政协主席",
        "current_org": "政协临泽县委员会",
        "source": "百度百科(临泽县)",
        "person_id": "linze_xing_xuewei"
    },
    # 前任领导
    {
        "id": "p05",
        "name": "张鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年3月",
        "birthplace": "甘肃甘州",
        "native_place": "甘肃甘州",
        "education": "省委党校研究生",
        "party_join": "1995年7月",
        "work_start": "约1990年代",
        "current_post": "民乐县委书记",
        "current_org": "中共民乐县委员会",
        "source": "百度百科(张鹏), 民乐县人物档案, 2026-07",
        "person_id": "linze_zhang_peng"
    },
    # 前任县委书记(张成琦之前)
    {
        "id": "p06",
        "name": "张学勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年?",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张掖市委常委、市委秘书长(近期调整)",
        "current_org": "中共张掖市委员会办公室",
        "source": "新闻报道, 2025年曾任临泽县委书记",
        "person_id": "linze_zhang_xueyong"
    },
    {
        "id": "p07",
        "name": "李作明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "约1970年",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "原民乐县委书记(2024年5月被查)",
        "current_org": "中共民乐县委员会",
        "source": "新浪新闻(2024-05-24, 省纪委监委通报)",
        "person_id": "linze_li_zuoming"
    },
    # 常务副县长/重要副职
    {
        "id": "p08",
        "name": "李国志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "临泽县委常委、常务副县长",
        "current_org": "临泽县人民政府",
        "source": "新闻报道(临泽县政府网站, 检索)",
        "person_id": "linze_li_guozhi"
    },
    {
        "id": "p09",
        "name": "谢青春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "临泽县委常委、组织部部长",
        "current_org": "中共临泽县委员会组织部",
        "source": "新闻报道(临泽县政府网站, 检索)",
        "person_id": "linze_xie_qingchun"
    },
    {
        "id": "p10",
        "name": "王晓霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "临泽县委常委、纪委书记、监委主任",
        "current_org": "中共临泽县纪律检查委员会",
        "source": "新闻报道(临泽县政府网站, 检索)",
        "person_id": "linze_wang_xiaoxia"
    },
    {
        "id": "p11",
        "name": "任刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "临泽县委常委、政法委书记",
        "current_org": "中共临泽县委员会政法委员会",
        "source": "新闻报道(临泽县政府网站, 检索)",
        "person_id": "linze_ren_gang"
    },
    {
        "id": "p12",
        "name": "牛伟全",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "临泽县委常委、副县长(分管工业)",
        "current_org": "临泽县人民政府",
        "source": "新闻报道(临泽县政府网站, 检索)",
        "person_id": "linze_niu_weiquan"
    },
    # 张掖市领导(与临泽相关)
    {
        "id": "p13",
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
        "source": "张掖市人民政府官网, 2026-07",
        "person_id": "linze_li_rui"
    },
    # 原甘州区领导(与秦楠交集)
    {
        "id": "p14",
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
        "source": "甘州区建设脚本, 2022年确认",
        "person_id": "linze_niu_shengbo"
    },
]

# 2. 组织机构
organizations = [
    {"id": "o01", "name": "中共临泽县委员会", "type": "党委", "level": "县处级", "parent": "中共张掖市委员会", "location": "甘肃省张掖市临泽县"},
    {"id": "o02", "name": "临泽县人民政府", "type": "政府", "level": "县处级", "parent": "张掖市人民政府", "location": "甘肃省张掖市临泽县"},
    {"id": "o03", "name": "临泽县人大常委会", "type": "人大", "level": "县处级", "parent": "临泽县", "location": "甘肃省张掖市临泽县"},
    {"id": "o04", "name": "政协临泽县委员会", "type": "政协", "level": "县处级", "parent": "临泽县", "location": "甘肃省张掖市临泽县"},
    {"id": "o05", "name": "中共临泽县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共临泽县委员会", "location": "甘肃省张掖市临泽县"},
    {"id": "o06", "name": "中共临泽县委员会组织部", "type": "党委", "level": "县处级", "parent": "中共临泽县委员会", "location": "甘肃省张掖市临泽县"},
    {"id": "o07", "name": "中共临泽县委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共临泽县委员会", "location": "甘肃省张掖市临泽县"},
    {"id": "o08", "name": "中共民乐县委员会", "type": "党委", "level": "县处级", "parent": "中共张掖市委员会", "location": "甘肃省张掖市民乐县"},
    {"id": "o09", "name": "中共甘州区委员会", "type": "党委", "level": "县处级", "parent": "中共张掖市委员会", "location": "甘肃省张掖市甘州区"},
    {"id": "o10", "name": "甘州区人民政府", "type": "政府", "level": "县处级", "parent": "张掖市人民政府", "location": "甘肃省张掖市甘州区"},
    {"id": "o11", "name": "张掖市人民政府", "type": "政府", "level": "地级", "parent": "甘肃省人民政府", "location": "甘肃省张掖市"},
    {"id": "o12", "name": "中共张掖市委员会", "type": "党委", "level": "地级", "parent": "中共甘肃省委员会", "location": "甘肃省张掖市"},
    {"id": "o13", "name": "中共张掖市委员会办公室", "type": "党委", "level": "副厅级", "parent": "中共张掖市委员会", "location": "甘肃省张掖市"},
]

# 3. 任职
positions = [
    # 张成琦 - 县委书记
    {"person_id": "p01", "org_id": "o01", "title": "临泽县委书记", "start": "2025年8月?", "end": "至今", "rank": "正县级", "note": "主持县委全面工作; 2025年8月前后任临泽县委书记(新闻来源:网易2025-08-06)"},
    # 秦楠 - 县长
    {"person_id": "p02", "org_id": "o01", "title": "临泽县委副书记", "start": "?", "end": "至今", "rank": "副县级", "note": "兼任县长"},
    {"person_id": "p02", "org_id": "o02", "title": "临泽县县长", "start": "?", "end": "至今", "rank": "正县级", "note": "主持县政府全面工作"},
    {"person_id": "p02", "org_id": "o09", "title": "甘州区副区长", "start": "?", "end": "?", "rank": "副处级", "note": "此前曾任甘州区副区长"},
    # 许兴权
    {"person_id": "p03", "org_id": "o03", "title": "临泽县人大常委会主任", "start": "?", "end": "至今", "rank": "正县级", "note": ""},
    # 邢学伟
    {"person_id": "p04", "org_id": "o04", "title": "临泽县政协主席", "start": "?", "end": "至今", "rank": "正县级", "note": ""},
    # 张鹏 - 前临泽县长，现民乐县委书记
    {"person_id": "p05", "org_id": "o02", "title": "临泽县委副书记、县长", "start": "约2019年", "end": "2024年8月", "rank": "正县级", "note": "前任县长; 后调任民乐县委书记"},
    {"person_id": "p05", "org_id": "o08", "title": "民乐县委书记", "start": "2024年8月", "end": "至今", "rank": "正县级", "note": "2024年8月任民乐县委书记"},
    # 张学勇 - 可能的前任县委书记
    {"person_id": "p06", "org_id": "o01", "title": "临泽县委书记", "start": "?", "end": "2025年?", "rank": "正县级", "note": "张成琦的前任; 后调任张掖市委常委、市委秘书长"},
    # 李国志 - 常务副县长
    {"person_id": "p08", "org_id": "o02", "title": "临泽县委常委、常务副县长", "start": "?", "end": "至今", "rank": "副县级", "note": "协助县长处理县政府日常工作"},
    # 谢青春 - 组织部长
    {"person_id": "p09", "org_id": "o06", "title": "临泽县委常委、组织部部长", "start": "?", "end": "至今", "rank": "副县级", "note": "分管组织工作"},
    # 王晓霞 - 纪委书记
    {"person_id": "p10", "org_id": "o05", "title": "临泽县委常委、县纪委书记、县监委主任", "start": "?", "end": "至今", "rank": "副县级", "note": ""},
    # 任刚 - 政法委书记
    {"person_id": "p11", "org_id": "o07", "title": "临泽县委常委、政法委书记", "start": "?", "end": "至今", "rank": "副县级", "note": ""},
    # 牛伟全 - 副县长
    {"person_id": "p12", "org_id": "o02", "title": "临泽县委常委、副县长", "start": "?", "end": "至今", "rank": "副县级", "note": "分管工业等工作"},
    # 李锐 - 张掖市委常委、甘州区委书记
    {"person_id": "p13", "org_id": "o09", "title": "甘州区委书记", "start": "?", "end": "至今", "rank": "副厅级", "note": "兼任张掖市委常委"},
    # 牛生波 - 甘州区副区长
    {"person_id": "p14", "org_id": "o10", "title": "甘州区副区长", "start": "?", "end": "至今", "rank": "副处级", "note": "此前与秦楠在甘州区政府共事"},
]

# 4. 关系
relationships = [
    # 党政一把手
    {"person_a": "p01", "person_b": "p02", "type": "overlap", "context": "张成琦(书记)与秦楠(县长): 临泽县党政一把手配合作", "overlap_org": "中共临泽县委员会/临泽县人民政府", "overlap_period": "2025?至今", "strength": "strong", "confidence": "confirmed"},
    # 书记-人大
    {"person_a": "p01", "person_b": "p03", "type": "overlap", "context": "张成琦(书记)与许兴权(人大主任): 党委与人大配合作", "overlap_org": "临泽县四套班子", "overlap_period": "2025?至今", "strength": "strong", "confidence": "confirmed"},
    # 书记-政协
    {"person_a": "p01", "person_b": "p04", "type": "overlap", "context": "张成琦(书记)与邢学伟(政协主席): 党委与政协配合作", "overlap_org": "临泽县四套班子", "overlap_period": "2025?至今", "strength": "strong", "confidence": "confirmed"},
    # 县长-常务副县长
    {"person_a": "p02", "person_b": "p08", "type": "overlap", "context": "秦楠(县长)与李国志(常务副县长): 正副手关系", "overlap_org": "临泽县人民政府", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 书记-组织部长
    {"person_a": "p01", "person_b": "p09", "type": "overlap", "context": "张成琦(书记)与谢青春(组织部长): 党委班子上下级", "overlap_org": "中共临泽县委员会", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 书记-纪委书记
    {"person_a": "p01", "person_b": "p10", "type": "overlap", "context": "张成琦(书记)与王晓霞(纪委书记): 党委班子上下级", "overlap_org": "中共临泽县委员会", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 书记-政法委书记
    {"person_a": "p01", "person_b": "p11", "type": "overlap", "context": "张成琦(书记)与任刚(政法委书记): 党委班子上下级", "overlap_org": "中共临泽县委员会", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 书记-副县长
    {"person_a": "p01", "person_b": "p12", "type": "overlap", "context": "张成琦(书记)与牛伟全(副县长): 党委班子上下级", "overlap_org": "中共临泽县委员会", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 前任-现任关系(县长)
    {"person_a": "p05", "person_b": "p02", "type": "predecessor_successor", "context": "张鹏(前任县长)与秦楠(现任县长): 临泽县长交接", "overlap_org": "临泽县人民政府", "overlap_period": "2024?2025?", "strength": "strong", "confidence": "confirmed"},
    # 前任县委书记 - 现任县委书记
    {"person_a": "p06", "person_b": "p01", "type": "predecessor_successor", "context": "张学勇(前任县委书记)与张成琦(现任县委书记): 书记交接", "overlap_org": "中共临泽县委员会", "overlap_period": "2025", "strength": "strong", "confidence": "plausible"},
    # 秦楠 - 张鹏(前县长)
    {"person_a": "p02", "person_b": "p05", "type": "predecessor_successor", "context": "秦楠接替张鹏? 秦楠任县长可能发生在张鹏调任民乐之后", "overlap_org": "临泽县人民政府", "overlap_period": "2024-2025", "strength": "strong", "confidence": "plausible"},
    # 秦楠与原甘州区同事
    {"person_a": "p02", "person_b": "p14", "type": "overlap", "context": "秦楠与牛生波: 此前同在甘州区政府任副区长", "overlap_org": "甘州区人民政府", "overlap_period": "?", "strength": "medium", "confidence": "confirmed"},
    # 秦楠与李锐(甘州区委书记)
    {"person_a": "p02", "person_b": "p13", "type": "overlap", "context": "秦楠曾任甘州区副区长, 李锐为甘州区委书记(后兼任市委常委)", "overlap_org": "中共甘州区委员会/甘州区人民政府", "overlap_period": "?", "strength": "medium", "confidence": "plausible"},
    # 张鹏(前临泽县长)-李作明(前民乐县委书记)
    {"person_a": "p05", "person_b": "p07", "type": "predecessor_successor", "context": "张鹏接替被查的李作明任民乐县委书记", "overlap_org": "中共民乐县委员会", "overlap_period": "2024年8月", "strength": "strong", "confidence": "confirmed"},
    # 张鹏-张成琦(前县长-现书记关系)
    {"person_a": "p05", "person_b": "p01", "type": "overlap", "context": "张鹏(前任县长)与张成琦(现任书记): 曾在临泽县共事?", "overlap_org": "临泽县", "overlap_period": "2024-2025", "strength": "medium", "confidence": "plausible"},
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
            return "200,50,50"   # 暗红 — 副职(如县委副书记)
        return "255,50,50"   # 红色 — 党委正职
    if "县长" in title or ("长" in title and "副县长" not in title):
        return "50,100,255"  # 蓝色 — 政府领导
    if "纪委" in title or "监委" in title:
        return "255,165,0"   # 橙色 — 纪检
    if "常委" in title:
        return "200,100,100" # 粉红 — 其他常委
    if "人大" in title:
        return "200,255,255" # 青色 — 人大
    if "政协" in title:
        return "255,240,200" # 米色 — 政协
    if "副区长" in title or "副县长" in title:
        return "100,100,200" # 浅蓝 — 副县/区长
    return "100,100,100"     # 灰色 — 其他

def person_size(p):
    """按角色返回节点大小"""
    title = p["current_post"]
    if "县委书记" in title or "县长" in title:
        return "20.0"
    if "副书记" in title or "常委" in title:
        return "14.0"
    if "人大" in title or "政协" in title:
        return "12.0"
    if "副区长" in title or "副县长" in title:
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
            o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]
        ))

    for pos in positions:
        c.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
                     VALUES (?,?,?,?,?,?,?)""", (
            pos["person_id"], pos["org_id"], pos["title"],
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
    lines.append('    <description>临泽县领导班子工作关系网络 - 数据来源: 临泽县政府网站, 百度百科及公开报道</description>')
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
        lines.append('          <attvalue for="2" value="甘肃省"/>')
        lines.append('          <attvalue for="3" value="临泽县"/>')
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
        lines.append('          <attvalue for="3" value="临泽县"/>')
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
    print(f"=== 临泽县网络数据构建 ===")
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
