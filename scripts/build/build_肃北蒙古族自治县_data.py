#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
肃北蒙古族自治县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

数据来源:
- 肃北县人民政府官方网站 (subei.gov.cn), 2026年7月确认
- 百度百科 (baike.baidu.com), 2026年7月确认
- 百度AI搜索摘要 (2026年7月)
- 搜狗搜索 (sogou.com), 2026年7月确认
- 肃北党建网 (subeidj.gov.cn)
- 新闻报道 (每日甘肃, 澎湃新闻, 网易, 新浪新闻等)
- 酒泉市领导班子公开信息，酒泉市人大常委会2025-12
"""

import json
import os
import sqlite3
from datetime import datetime

# ── 路径 ──────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "肃北蒙古族自治县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "肃北蒙古族自治县_network.gexf")

# ── 数据 ──────────────────────────────────────────────

# 1. 人员
persons = [
    # === 核心领导 ===
    {
        "id": "p01",
        "name": "马伟",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "肃北县委书记",
        "current_org": "中共肃北蒙古族自治县委员会",
        "source": "肃北县人民政府官网(subei.gov.cn)2026-07, 每日甘肃2026-07-13, 美篇(肃北县2026年春节团拜会)",
        "person_id": "subei_ma_wei"
    },
    {
        "id": "p02",
        "name": "巴成",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1972年10月",
        "birthplace": "甘肃肃北",
        "native_place": "甘肃肃北",
        "education": "大学本科(西北师范大学)",
        "party_join": "1998年6月",
        "work_start": "2000年7月",
        "current_post": "肃北县委副书记、县长",
        "current_org": "肃北蒙古族自治县人民政府",
        "source": "百度百科(巴成), 酒泉市人民政府(酒政任字〔2021〕12号), 2022肃北年鉴",
        "person_id": "subei_ba_cheng"
    },
    # === 前任县委书记 ===
    {
        "id": "p03",
        "name": "张跃峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "酒泉市人民政府副市长",
        "current_org": "酒泉市人民政府",
        "source": "中国甘肃网, 酒泉市人大常委会2025-12, 肃北县政府官网(2024-01全会报道, 2025-04文章)",
        "person_id": "subei_zhang_yuefeng"
    },
    # === 前任县委书记(更早) ===
    {
        "id": "p04",
        "name": "张立东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查",
        "current_org": "待查",
        "source": "搜狐网(2019-04, 省委副书记孙伟调研报道)",
        "person_id": "subei_zhang_lidong"
    },
    # === 县委常委/副职领导 ===
    {
        "id": "p05",
        "name": "王迎军",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "肃北县委常委、常务副县长",
        "current_org": "肃北蒙古族自治县人民政府",
        "source": "2022肃北年鉴(肃北县政府官网), 搜狗搜索",
        "person_id": "subei_wang_yingjun"
    },
    {
        "id": "p06",
        "name": "王东云",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "肃北县委常委、副县长",
        "current_org": "肃北蒙古族自治县人民政府",
        "source": "2022肃北年鉴(肃北县政府官网), 搜狗搜索",
        "person_id": "subei_wang_dongyun"
    },
    # === 原县长(前任) ===
    {
        "id": "p07",
        "name": "图门吉尔格勒",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查(原肃北县长)",
        "current_org": "肃北蒙古族自治县人民政府",
        "source": "肃北县人民政府公众信息网(历史领导名录, 2021-03-11)",
        "person_id": "subei_tumen_jiergele"
    },
    # 酒泉市领导(上级)
    {
        "id": "p08",
        "name": "王立奇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年12月",
        "birthplace": "辽宁北票",
        "native_place": "辽宁北票",
        "education": "研究生/工学硕士(清华大学管理科学与工程专业)",
        "party_join": "中共党员",
        "work_start": "2003年9月",
        "current_post": "酒泉市委书记",
        "current_org": "中共酒泉市委员会",
        "source": "酒泉市_network.db, 百度百科",
        "person_id": "subei_wang_liqi"
    },
    {
        "id": "p09",
        "name": "贾志升",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年7月",
        "birthplace": "甘肃镇原",
        "native_place": "甘肃镇原",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "1996年11月",
        "current_post": "酒泉市委副书记、市长",
        "current_org": "酒泉市人民政府",
        "source": "酒泉市_network.db, 百度百科",
        "person_id": "subei_jia_zhisheng"
    },
    # 牧仁 - 县委副书记(2020年报道中提到)
    {
        "id": "p10",
        "name": "牧仁",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "肃北县委副书记(2020年)",
        "current_org": "中共肃北蒙古族自治县委员会",
        "source": "搜狐网(政协常委会2020-09-15报道), 搜狗搜索",
        "person_id": "subei_mu_ren"
    },
]

# 2. 组织机构
organizations = [
    {"id": "o01", "name": "中共肃北蒙古族自治县委员会", "type": "党委", "level": "县处级", "parent": "中共酒泉市委员会", "location": "甘肃省酒泉市肃北蒙古族自治县"},
    {"id": "o02", "name": "肃北蒙古族自治县人民政府", "type": "政府", "level": "县处级", "parent": "酒泉市人民政府", "location": "甘肃省酒泉市肃北蒙古族自治县"},
    {"id": "o03", "name": "肃北蒙古族自治县人大常委会", "type": "人大", "level": "县处级", "parent": "肃北蒙古族自治县", "location": "甘肃省酒泉市肃北蒙古族自治县"},
    {"id": "o04", "name": "政协肃北蒙古族自治县委员会", "type": "政协", "level": "县处级", "parent": "肃北蒙古族自治县", "location": "甘肃省酒泉市肃北蒙古族自治县"},
    {"id": "o05", "name": "肃北蒙古族自治县纪委监委", "type": "党委", "level": "县处级", "parent": "中共肃北蒙古族自治县委员会", "location": "甘肃省酒泉市肃北蒙古族自治县"},
    {"id": "o06", "name": "中共肃北蒙古族自治县委员会组织部", "type": "党委", "level": "县处级", "parent": "中共肃北蒙古族自治县委员会", "location": "甘肃省酒泉市肃北蒙古族自治县"},
    {"id": "o07", "name": "中共肃北蒙古族自治县委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共肃北蒙古族自治县委员会", "location": "甘肃省酒泉市肃北蒙古族自治县"},
    {"id": "o08", "name": "中共肃北蒙古族自治县委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共肃北蒙古族自治县委员会", "location": "甘肃省酒泉市肃北蒙古族自治县"},
    {"id": "o09", "name": "中共酒泉市委员会", "type": "党委", "level": "地级", "parent": "中共甘肃省委员会", "location": "甘肃省酒泉市"},
    {"id": "o10", "name": "酒泉市人民政府", "type": "政府", "level": "地级", "parent": "甘肃省人民政府", "location": "甘肃省酒泉市"},
    {"id": "o11", "name": "酒泉市民族宗教事务委员会", "type": "政府", "level": "地级", "parent": "酒泉市人民政府", "location": "甘肃省酒泉市"},
]

# 3. 任职
positions = [
    # 马伟 - 县委书记
    {"person_id": "p01", "org_id": "o01", "title": "肃北县委书记", "start": "2025-2026年?", "end": "至今", "rank": "正县级", "note": "主持县委全面工作; 接替张跃峰任肃北县委书记; 2026年春节团拜会以县委书记身份发表新春致辞"},
    # 巴成 - 县长
    {"person_id": "p02", "org_id": "o01", "title": "肃北县委副书记", "start": "?", "end": "至今", "rank": "副县级", "note": "兼任县长"},
    {"person_id": "p02", "org_id": "o02", "title": "肃北蒙古族自治县县长", "start": "?", "end": "至今", "rank": "正县级", "note": "主持县政府全面工作"},
    {"person_id": "p02", "org_id": "o11", "title": "酒泉市民族宗教事务委员会副主任", "start": "?", "end": "2021年9月", "rank": "副处级", "note": "酒政任字〔2021〕12号, 2021年9月免职"},
    # 张跃峰 - 前任县委书记
    {"person_id": "p03", "org_id": "o01", "title": "肃北县委书记", "start": "约2021-2023年?", "end": "约2025-2026年", "rank": "正县级", "note": "至少任职至2025年4月(发表署名文章); 后调任酒泉市副市长"},
    {"person_id": "p03", "org_id": "o10", "title": "酒泉市人民政府副市长", "start": "2025年12月", "end": "至今", "rank": "副厅级", "note": "2025年12月酒泉市人大常委会任命"},
    # 张立东 - 更早的前任县委书记
    {"person_id": "p04", "org_id": "o01", "title": "肃北县委书记", "start": "约2019年及更早", "end": "约2021年?", "rank": "正县级", "note": "2019年4月报道中为县委书记; 张跃峰的前任"},
    # 王迎军 - 常务副县长
    {"person_id": "p05", "org_id": "o02", "title": "肃北县委常委、常务副县长", "start": "?", "end": "至今", "rank": "副县级", "note": "协助县长处理县政府日常工作(2022肃北年鉴)"},
    # 王东云 - 副县长
    {"person_id": "p06", "org_id": "o02", "title": "肃北县委常委、副县长", "start": "?", "end": "至今", "rank": "副县级", "note": "(2022肃北年鉴)"},
    # 图门吉尔格勒 - 前县长
    {"person_id": "p07", "org_id": "o02", "title": "肃北蒙古族自治县县长", "start": "?", "end": "约2021年?", "rank": "正县级", "note": "前任县长; 巴成的前任"},
    # 王立奇 - 酒泉市委书记
    {"person_id": "p08", "org_id": "o09", "title": "酒泉市委书记", "start": "2021年7月", "end": "至今", "rank": "正厅级", "note": "主持市委全面工作; 肃北县的直接上级领导"},
    # 贾志升 - 酒泉市长
    {"person_id": "p09", "org_id": "o09", "title": "酒泉市委副书记", "start": "2025年9月", "end": "至今", "rank": "副厅级", "note": "兼任市长"},
    {"person_id": "p09", "org_id": "o10", "title": "酒泉市人民政府市长", "start": "2025年10月", "end": "至今", "rank": "正厅级", "note": "肃北县的直接上级领导"},
    # 牧仁 - 县委副书记(曾任)
    {"person_id": "p10", "org_id": "o01", "title": "肃北县委副书记", "start": "?", "end": "?", "rank": "副县级", "note": "2020年9月报道中为县委副书记"},
]

# 4. 关系
relationships = [
    # 党政一把手
    {"person_a": "p01", "person_b": "p02", "type": "overlap", "context": "马伟(书记)与巴成(县长): 肃北县党政一把手配合", "overlap_org": "中共肃北蒙古族自治县委员会/肃北蒙古族自治县人民政府", "overlap_period": "至今(2025-2026?)", "strength": "strong", "confidence": "confirmed"},
    # 书记-前任书记
    {"person_a": "p01", "person_b": "p03", "type": "predecessor_successor", "context": "马伟接替张跃峰任肃北县委书记", "overlap_org": "中共肃北蒙古族自治县委员会", "overlap_period": "2025-2026", "strength": "strong", "confidence": "confirmed"},
    # 张跃峰-张立东
    {"person_a": "p03", "person_b": "p04", "type": "predecessor_successor", "context": "张跃峰接替张立东任肃北县委书记", "overlap_org": "中共肃北蒙古族自治县委员会", "overlap_period": "约2021年", "strength": "strong", "confidence": "plausible"},
    # 县长-前任县长(图门吉尔格勒)
    {"person_a": "p02", "person_b": "p07", "type": "predecessor_successor", "context": "巴成接替图门吉尔格勒任肃北县长", "overlap_org": "肃北蒙古族自治县人民政府", "overlap_period": "约2021年", "strength": "strong", "confidence": "plausible"},
    # 县长-常务副县长
    {"person_a": "p02", "person_b": "p05", "type": "overlap", "context": "巴成(县长)与王迎军(常务副县长): 正副手关系", "overlap_org": "肃北蒙古族自治县人民政府", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 县长-副县长
    {"person_a": "p02", "person_b": "p06", "type": "overlap", "context": "巴成(县长)与王东云(副县长): 正副手关系", "overlap_org": "肃北蒙古族自治县人民政府", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 书记-酒泉市委书记(上下级)
    {"person_a": "p01", "person_b": "p08", "type": "superior_subordinate", "context": "马伟(肃北县委书记)与王立奇(酒泉市委书记): 上下级领导关系", "overlap_org": "中共酒泉市委员会/中共肃北蒙古族自治县委员会", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    # 书记-酒泉市长(上下级)
    {"person_a": "p01", "person_b": "p09", "type": "superior_subordinate", "context": "马伟(肃北县委书记)与贾志升(酒泉市长): 上下级领导关系", "overlap_org": "酒泉市人民政府/中共肃北蒙古族自治县委员会", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    # 县长-酒泉市长(上下级)
    {"person_a": "p02", "person_b": "p09", "type": "superior_subordinate", "context": "巴成(肃北县长)与贾志升(酒泉市长): 上下级领导关系", "overlap_org": "酒泉市人民政府/肃北蒙古族自治县人民政府", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    # 巴成 - 牧仁(县委副书记班子)
    {"person_a": "p02", "person_b": "p10", "type": "overlap", "context": "巴成与牧仁(县委副书记): 县委班子共事", "overlap_org": "中共肃北蒙古族自治县委员会", "overlap_period": "?", "strength": "medium", "confidence": "plausible"},
    # 张跃峰(前书记) - 巴成(县长): 曾搭班子
    {"person_a": "p03", "person_b": "p02", "type": "overlap", "context": "张跃峰(前书记)与巴成(县长): 曾在肃北县搭班子", "overlap_org": "中共肃北蒙古族自治县委员会/肃北蒙古族自治县人民政府", "overlap_period": "约2021-2025/2026", "strength": "strong", "confidence": "confirmed"},
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
    if "县长" in title or ("长" in title and "副县长" not in title):
        if "常务" in title:
            return "100,100,255"  # 深蓝 — 常务副县长
        return "50,100,255"  # 蓝色 — 政府正职
    if "纪委" in title or "监委" in title:
        return "255,165,0"   # 橙色 — 纪检
    if "常委" in title:
        return "200,100,100" # 粉红 — 其他常委
    if "人大" in title:
        return "200,255,255" # 青色 — 人大
    if "政协" in title:
        return "255,240,200" # 米色 — 政协
    if "副市长" in title:
        return "80,80,200"   # 蓝紫 — 副市长
    if "副区长" in title or "副县长" in title:
        return "100,100,200" # 浅蓝 — 副县/区长
    return "100,100,100"     # 灰色 — 其他

def person_size(p):
    """按角色返回节点大小"""
    title = p["current_post"]
    if "县委书记" in title or ("县长" in title and "副县长" not in title and "常务" not in title):
        return "20.0"
    if "副书记" in title or "常委" in title:
        return "14.0"
    if "副市长" in title:
        return "14.0"
    if "人大" in title or "政协" in title:
        return "12.0"
    if "常务副" in title:
        return "14.0"
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
    lines.append('    <description>肃北蒙古族自治县领导班子工作关系网络 - 数据来源: 肃北县政府网站, 百度百科及公开报道</description>')
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
        lines.append('          <attvalue for="3" value="肃北蒙古族自治县"/>')
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
        lines.append('          <attvalue for="3" value="肃北蒙古族自治县"/>')
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
    print(f"=== 肃北蒙古族自治县网络数据构建 ===")
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
