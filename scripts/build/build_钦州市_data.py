#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
钦州市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 地级市
Province: 广西壮族自治区
Parent City:
Region: 钦州市
Targets: 市委书记 & 市长

当前在任 (as of 2026-07-23):
- 市委书记: 钟畅姿 (钦州市委书记、钦州军分区党委第一书记)
- 市长: 李玉成 (钦州市委副书记、市政府市长、党组书记)
"""

import json
import os
import sys
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "钦州市"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-23"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：市委书记 (2026-)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "钟畅姿",
        "gender": "女",
        "ethnicity": "水族",
        "birth": "1971年4月",
        "birthplace": "广西河池",
        "education": "研究生学历，文学硕士",
        "party_join": "1997年9月",
        "work_start": "1995年7月",
        "current_post": "钦州市委书记、钦州军分区党委第一书记",
        "current_org": "中共钦州市委员会",
        "source": "https://www.baike.com/wiki/钟畅姿"
    },
    # ════════════════════════════════════════
    # 核心领导：市长 (2025/2026-)
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "李玉成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "钦州市委副书记、市政府市长、党组书记",
        "current_org": "钦州市人民政府",
        "source": "https://www.qinzhou.gov.cn/zwgk/ldxx/"
    },
    # ════════════════════════════════════════
    # 前市长 (2021-2025/2026，双开)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "王雄昌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年11月",
        "birthplace": "浙江建德",
        "education": "在职研究生学历，工学博士",
        "party_join": "中共党员",
        "work_start": "1992年",
        "current_post": "原钦州市委副书记、市长（2026年1月被开除党籍和公职）",
        "current_org": "",
        "source": "https://www.baike.com/wiki/王雄昌"
    },
    # ════════════════════════════════════════
    # 前市长 (2018-2021) → 防城港市委书记 → 自治区统战部长
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "谭丕创",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年10月",
        "birthplace": "广西贵港",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广西壮族自治区党委常委、统战部部长",
        "current_org": "中共广西壮族自治区委员会",
        "source": "https://www.baike.com/wiki/谭丕创"
    },
    # ════════════════════════════════════════
    # 市人大常委会主任
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "覃天卫",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "钦州市人大常委会主任",
        "current_org": "钦州市人民代表大会常务委员会",
        "source": "https://www.qinzhou.gov.cn/"
    },
    # ════════════════════════════════════════
    # 市政协主席
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "吕洪安",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "钦州市政协主席",
        "current_org": "中国人民政治协商会议钦州市委员会",
        "source": "https://www.qinzhou.gov.cn/"
    },
    # ════════════════════════════════════════
    # 市委副书记 — 从新闻中识别
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "庞科伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "钦州市委副书记",
        "current_org": "中共钦州市委员会",
        "source": "https://www.qinzhou.gov.cn/"
    },
    # ════════════════════════════════════════
    # 前市委书记 — 钟畅姿的前任 (2022?-2026)
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "林冠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已卸任钦州市委书记",
        "current_org": "",
        "source": "https://www.qinzhou.gov.cn/"
    },
    # ════════════════════════════════════════
    # 市委常委、市纪委书记、市监委主任
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "潘瑾兴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "钦州市委常委、市纪委书记、市监委主任",
        "current_org": "中共钦州市纪律检查委员会/钦州市监察委员会",
        "source": "https://www.qinzhou.gov.cn/"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {
        "id": 1,
        "name": "中共钦州市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广西壮族自治区委员会",
        "location": "钦州市"
    },
    {
        "id": 2,
        "name": "钦州市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广西壮族自治区人民政府",
        "location": "钦州市"
    },
    {
        "id": 3,
        "name": "钦州市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级市",
        "parent": "广西壮族自治区人民代表大会常务委员会",
        "location": "钦州市"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议钦州市委员会",
        "type": "政协",
        "level": "地级市",
        "parent": "中国人民政治协商会议广西壮族自治区委员会",
        "location": "钦州市"
    },
    {
        "id": 5,
        "name": "中共钦州市纪律检查委员会/钦州市监察委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共钦州市委员会",
        "location": "钦州市"
    },
    {
        "id": 6,
        "name": "钦州军分区",
        "type": "党委",
        "level": "地级市",
        "parent": "广西军区",
        "location": "钦州市"
    },
    {
        "id": 7,
        "name": "中共防城港市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广西壮族自治区委员会",
        "location": "防城港市"
    },
    {
        "id": 8,
        "name": "防城港市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广西壮族自治区人民政府",
        "location": "防城港市"
    },
    {
        "id": 9,
        "name": "中共广西壮族自治区委员会",
        "type": "党委",
        "level": "省级",
        "parent": "",
        "location": "南宁市"
    },
    {
        "id": 10,
        "name": "广西壮族自治区党委统战部",
        "type": "党委",
        "level": "省级",
        "parent": "中共广西壮族自治区委员会",
        "location": "南宁市"
    },
    {
        "id": 11,
        "name": "中国（广西）自由贸易试验区钦州港片区",
        "type": "政府",
        "level": "地级市",
        "parent": "钦州市人民政府",
        "location": "钦州市"
    },
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 钟畅姿 — 钦州市委书记 (2026-)
    {"person_id": 1, "org_id": 1, "title": "钦州市委书记、钦州军分区党委第一书记", "start_date": "2026", "end_date": "present", "rank": "正厅级", "note": "接替林冠任钦州市委书记"},
    # 钟畅姿 — 广西自治区妇联主席/党组书记
    {"person_id": 1, "org_id": 9, "title": "广西壮族自治区妇女联合会主席、党组书记", "start_date": "2021", "end_date": "2026", "rank": "正厅级", "note": "任自治区妇联主席期间"}, 
    # 钟畅姿 — 贵港市委副书记、市长
    {"person_id": 1, "org_id": 2, "title": "贵港市委副书记、市政府市长、党组书记", "start_date": "2016", "end_date": "2021", "rank": "正厅级", "note": ""},
    # 钟畅姿 — 广西自治区党委组织部副部长
    {"person_id": 1, "org_id": 9, "title": "广西壮族自治区党委组织部副部长", "start_date": "2014", "end_date": "2016", "rank": "副厅级", "note": ""},
    # 钟畅姿 — 广西自治区党委组织部部务委员
    {"person_id": 1, "org_id": 9, "title": "广西壮族自治区党委组织部部务委员", "start_date": "2012", "end_date": "2014", "rank": "副厅级", "note": ""},
    # 钟畅姿 — 贵港市委常委、组织部部长
    {"person_id": 1, "org_id": 9, "title": "贵港市委常委、组织部部长", "start_date": "2009", "end_date": "2012", "rank": "副厅级", "note": ""},
    # 钟畅姿 — 崇左市江州区（原江州区委书记等基层职务）
    {"person_id": 1, "org_id": 1, "title": "崇左市江州区委书记", "start_date": "2007", "end_date": "2009", "rank": "正处级", "note": ""},
    # 钟畅姿 — 广西自治区民政厅副厅长
    {"person_id": 1, "org_id": 9, "title": "广西壮族自治区民政厅副厅长、党组成员", "start_date": "2006", "end_date": "2007", "rank": "副厅级", "note": "挂职"},
    
    # 李玉成 — 钦州市市长 (2025/2026-)
    {"person_id": 2, "org_id": 2, "title": "钦州市委副书记、市政府市长、党组书记", "start_date": "待查", "end_date": "present", "rank": "正厅级", "note": "接替被双开的王雄昌任钦州市市长"},
    
    # 王雄昌 — 钦州市市长 (2021-2025/2026)
    {"person_id": 3, "org_id": 2, "title": "钦州市委副书记、市政府市长、党组书记", "start_date": "2021", "end_date": "2025/2026", "rank": "正厅级", "note": "2026年1月因严重违纪违法被开除党籍和公职"},
    # 王雄昌 — 中国（广西）自由贸易试验区钦州港片区管委会主任
    {"person_id": 3, "org_id": 11, "title": "中国（广西）自由贸易试验区钦州港片区管委会主任", "start_date": "2021", "end_date": "2025/2026", "rank": "正厅级", "note": ""},
    # 王雄昌 — 广西自治区北部湾经济区规划建设管理办公室副主任
    {"person_id": 3, "org_id": 9, "title": "广西自治区北部湾经济区规划建设管理办公室副主任", "start_date": "2016", "end_date": "2021", "rank": "副厅级", "note": ""},
    # 王雄昌 — 钦州保税港区管委会副主任
    {"person_id": 3, "org_id": 11, "title": "钦州保税港区管委会副主任、常务副主任", "start_date": "2010", "end_date": "2016", "rank": "副厅级", "note": ""},
    
    # 谭丕创 — 自治区党委常委、统战部部长 (2025.10-)
    {"person_id": 4, "org_id": 10, "title": "广西壮族自治区党委常委、统战部部长", "start_date": "2025-10", "end_date": "present", "rank": "副省级", "note": ""},
    # 谭丕创 — 柳州市委书记（兼）(2024.09-2025.10)
    {"person_id": 4, "org_id": 1, "title": "柳州市委书记（兼自治区副主席）", "start_date": "2024-09", "end_date": "2025-10", "rank": "正厅级（兼）", "note": "兼任柳州市委书记"},
    # 谭丕创 — 广西自治区副主席 (2024.05-2025.10)
    {"person_id": 4, "org_id": 9, "title": "广西壮族自治区副主席", "start_date": "2024-05", "end_date": "2025-10", "rank": "副省级", "note": ""},
    # 谭丕创 — 防城港市委书记 (2021.03-2024.05)
    {"person_id": 4, "org_id": 7, "title": "防城港市委书记", "start_date": "2021-03", "end_date": "2024-05", "rank": "正厅级", "note": "由钦州市市长调任"},
    # 谭丕创 — 钦州市市长 (2018-2021.03)
    {"person_id": 4, "org_id": 2, "title": "钦州市市长", "start_date": "2018", "end_date": "2021-03", "rank": "正厅级", "note": "由广西投资促进局局长转任"},
    
    # 覃天卫 — 市人大常委会主任
    {"person_id": 5, "org_id": 3, "title": "钦州市人大常委会主任", "start_date": "待查", "end_date": "present", "rank": "正厅级", "note": ""},
    
    # 吕洪安 — 市政协主席
    {"person_id": 6, "org_id": 4, "title": "钦州市政协主席", "start_date": "待查", "end_date": "present", "rank": "正厅级", "note": ""},
    
    # 庞科伟 — 市委副书记
    {"person_id": 7, "org_id": 1, "title": "钦州市委副书记", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    
    # 林冠 — 前市委书记
    {"person_id": 8, "org_id": 1, "title": "钦州市委书记", "start_date": "2022", "end_date": "2026", "rank": "正厅级", "note": "接任者钟畅姿"},
    
    # 潘瑾兴 — 市纪委书记
    {"person_id": 9, "org_id": 5, "title": "钦州市委常委、市纪委书记、市监委主任", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 钟畅姿 ↔ 李玉成 (书记—市长搭档)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "现任市委书记与市长搭档关系", "overlap_org": "中共钦州市委员会/钦州市人民政府", "overlap_period": "2026-"},
    # 钟畅姿 ↔ 林冠 (前任—继任)
    {"person_a": 1, "person_b": 8, "type": "predecessor_successor", "context": "钟畅姿接替林冠任钦州市委书记", "overlap_org": "中共钦州市委员会", "overlap_period": "2026"},
    # 王雄昌 ↔ 李玉成 (前任—继任)
    {"person_a": 3, "person_b": 2, "type": "predecessor_successor", "context": "李玉成接替被双开的王雄昌任钦州市市长", "overlap_org": "钦州市人民政府", "overlap_period": "2025/2026"},
    # 谭丕创 ↔ 王雄昌 (前任—继任)
    {"person_a": 4, "person_b": 3, "type": "predecessor_successor", "context": "王雄昌接替谭丕创任钦州市市长", "overlap_org": "钦州市人民政府", "overlap_period": "2021"},
    # 钟畅姿 ↔ 王雄昌 (书记—市长，短暂搭档)
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "钟畅姿任钦州市委书记期间王雄昌任市长（若有时段重叠）", "overlap_org": "中共钦州市委员会/钦州市人民政府", "overlap_period": "待查"},
    # 钟畅姿 ↔ 谭丕创 (前后关系)
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "同属广西干部体系，多年跨市工作关系", "overlap_org": "中共广西壮族自治区委员会", "overlap_period": ""},
    # 谭丕创 ↔ 防城港—钦州临市交流
    {"person_a": 4, "person_b": 3, "type": "other", "context": "谭丕创从钦州市长调任防城港市委书记，王雄昌接任钦州市长", "overlap_org": "钦州市人民政府", "overlap_period": "2021"},
    # 钟畅姿 ↔ 庞科伟 (书记—副书记)
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "现任市委书记与市委副书记工作关系", "overlap_org": "中共钦州市委员会", "overlap_period": "2026-"},
    # 钟畅姿 ↔ 覃天卫 (书记—人大主任)
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "现任市委书记与市人大常委会主任", "overlap_org": "中共钦州市委员会/钦州市人大常委会", "overlap_period": "2026-"},
    # 李玉成 ↔ 庞科伟 (市长—副书记)
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "市长与市委副书记协作关系", "overlap_org": "中共钦州市委员会/钦州市人民政府", "overlap_period": "2026-"},
    # 李玉成 ↔ 潘瑾兴 (市长—纪委书记)
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "市长与纪委书记工作关系", "overlap_org": "中共钦州市委员会/钦州市人民政府", "overlap_period": "2026-"},
    # 王雄昌 ↔ 潘瑾兴 (市长—纪委书记，王被查)
    {"person_a": 3, "person_b": 9, "type": "other", "context": "王雄昌被查处涉及纪委调查关系", "overlap_org": "中共钦州市纪律检查委员会", "overlap_period": "2026"},
]

# =========================================================================
# 5. DATABASE
# =========================================================================
def create_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Persons
    cur.execute("""
        CREATE TABLE IF NOT EXISTS persons (
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
        )
    """)
    
    # Organizations
    cur.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        )
    """)
    
    # Positions
    cur.execute("""
        CREATE TABLE IF NOT EXISTS positions (
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
        )
    """)
    
    # Relationships
    cur.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)
    
    # Insert data
    for p in persons:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"])
        )
    
    for o in organizations:
        cur.execute(
            "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
        )
    
    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"])
        )
    
    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
        )
    
    conn.commit()
    conn.close()
    
    print(f"✓ Database created: {DB_PATH}")
    print(f"  {len(persons)} persons")
    print(f"  {len(organizations)} organizations")
    print(f"  {len(positions)} positions")
    print(f"  {len(relationships)} relationships")


# =========================================================================
# 6. GEXF
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def create_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append(f'    <description>钦州市领导班子工作关系网络 (as of {AS_OF})</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    
    # Node attributes
    lines.append('    <attributes class="node">')
    for attr_id, title, atype in [
        ("0", "type", "string"),
        ("1", "current_post", "string"),
        ("2", "current_org", "string"),
        ("3", "gender", "string"),
        ("4", "ethnicity", "string"),
        ("5", "birth", "string"),
        ("6", "birthplace", "string"),
        ("7", "source", "string"),
        ("8", "org_type", "string"),
        ("9", "level", "string"),
        ("10", "location", "string"),
    ]:
        lines.append(f'      <attribute id="{attr_id}" title="{title}" type="{atype}"/>')
    lines.append('    </attributes>')
    
    # Edge attributes
    lines.append('    <attributes class="edge">')
    for eid, title, etype in [
        ("0", "type", "string"),
        ("1", "context", "string"),
        ("2", "overlap_org", "string"),
        ("3", "overlap_period", "string"),
    ]:
        lines.append(f'      <attribute id="{eid}" title="{title}" type="{etype}"/>')
    lines.append('    </attributes>')
    
    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        post = p["current_post"]
        if "市委书记" in post or "书记" in post and "前" not in p["name"]:
            color = "255,50,50"
            size = "20.0"
        elif "市长" in post:
            color = "50,100,255"
            size = "20.0"
        elif "纪委书记" in post:
            color = "255,165,0"
            size = "12.0"
        else:
            color = "100,100,100"
            size = "12.0"
        
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["gender"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["ethnicity"])}"/>')
        lines.append(f'          <attvalue for="5" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="6" value="{esc(p["birthplace"])}"/>')
        lines.append(f'          <attvalue for="7" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append('      </node>')
    
    for o in organizations:
        org_type = o["type"]
        if org_type == "党委":
            ocolor = "255,200,200"
        elif org_type == "政府":
            ocolor = "200,200,255"
        elif org_type == "人大":
            ocolor = "200,255,255"
        elif org_type == "政协":
            ocolor = "255,240,200"
        elif org_type == "群团":
            ocolor = "255,220,255"
        else:
            ocolor = "220,220,220"
        
        oid = o["id"] + 100000
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="8" value="{esc(org_type)}"/>')
        lines.append(f'          <attvalue for="9" value="{esc(o["level"])}"/>')
        lines.append(f'          <attvalue for="10" value="{esc(o["location"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    
    # Edges
    lines.append('    <edges>')
    eid = 0
    
    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        pid = pos["person_id"]
        oid = pos["org_id"] + 100000
        lines.append(f'      <edge id="{eid}" source="p{pid}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start_date"])}~{esc(pos["end_date"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    
    # Person ↔ Person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    print(f"✓ GEXF created: {GEXF_PATH}")
    print(f"  {len(persons)} person nodes")
    print(f"  {len(organizations)} org nodes")
    print(f"  {eid} edges")


# =========================================================================
# 7. PERSON JSON
# =========================================================================
def write_person_json(person, filename_suffix, extra_entries=None):
    """Write a person graph JSON file."""
    fname = f"{AS_OF}-广西壮族自治区-钦州市-{filename_suffix}-{person['name']}.json"
    fpath = os.path.join(PERSONS_DIR, fname)
    
    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "",
            "region": "钦州市",
            "job": filename_suffix,
            "task_id": "guangxi_钦州市",
            "time_focus": "2025-2026"
        },
        "identity": {
            "person_id": f"qinzhou_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": person["birthplace"],
            "education": [
                {
                    "summary": person["education"]
                }
            ],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "name_birthplace": f"{person['name']}_{person['birthplace']}"
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "No public risk signals found in available sources", "date": AS_OF, "confidence": "unverified", "source_ids": ["S001"]}
        ],
        "source_register": [
            {
                "id": "S001",
                "url": person["source"],
                "source_type": "encyclopedia",
                "reliability": "medium",
                "notes": "Primary source for identity"
            }
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "biggest_gap": ""
        },
        "open_questions": []
    }
    
    if extra_entries:
        if "career_timeline" in extra_entries:
            data["career_timeline"] = extra_entries["career_timeline"]
        if "relationships" in extra_entries:
            data["relationships"] = extra_entries["relationships"]
        if "governance_record" in extra_entries:
            data["governance_record"] = extra_entries["governance_record"]
        if "professional_profile" in extra_entries:
            data["professional_profile"].update(extra_entries["professional_profile"])
        if "open_questions" in extra_entries:
            data["open_questions"] = extra_entries["open_questions"]
        if "work_style_and_personality" in extra_entries:
            data["work_style_and_personality"]["public_style_indicators"] = extra_entries["work_style_and_personality"]
        if "source_register" in extra_entries:
            reg = data["source_register"]
            existing_ids = {s["id"] for s in reg}
            for s in extra_entries["source_register"]:
                if s["id"] not in existing_ids:
                    reg.append(s)
                    existing_ids.add(s["id"])
    
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Person JSON created: {fpath}")


# =========================================================================
# 8. MAIN
# =========================================================================
def main():
    print("=" * 60)
    print(f"  钦州市领导班子工作关系网络 — 数据构建")
    print(f"  Date: {AS_OF}")
    print("=" * 60)
    
    create_db()
    print()
    create_gexf()
    print()
    
    # Person JSON: 钟畅姿 (市委书记)
    zhong_changzi_timeline = [
        {"start": "2026", "end": "present", "org": "中共钦州市委员会", "title": "钦州市委书记、钦州军分区党委第一书记", "rank": "正厅级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2021", "end": "2026", "org": "广西壮族自治区妇女联合会", "title": "广西壮族自治区妇联主席、党组书记", "rank": "正厅级", "confidence": "plausible", "source_ids": ["S001"]},
        {"start": "2016", "end": "2021", "org": "贵港市人民政府", "title": "贵港市委副书记、市长", "rank": "正厅级", "confidence": "plausible", "source_ids": ["S001"]},
        {"start": "2014", "end": "2016", "org": "中共广西壮族自治区委员会组织部", "title": "广西自治区党委组织部副部长", "rank": "副厅级", "confidence": "plausible", "source_ids": ["S001"]},
        {"start": "2012", "end": "2014", "org": "中共广西壮族自治区委员会组织部", "title": "广西自治区党委组织部部务委员", "rank": "副厅级", "confidence": "plausible", "source_ids": ["S001"]},
        {"start": "2009", "end": "2012", "org": "中共贵港市委员会", "title": "贵港市委常委、组织部部长", "rank": "副厅级", "confidence": "plausible", "source_ids": ["S001"]},
        {"start": "2007", "end": "2009", "org": "中共崇左市江州区委员会", "title": "崇左市江州区委书记", "rank": "正处级", "confidence": "plausible", "source_ids": ["S001"]},
        {"start": "2006", "end": "2007", "org": "广西壮族自治区民政厅", "title": "自治区民政厅副厅长（挂职）", "rank": "副厅级", "confidence": "unverified", "source_ids": ["S001"]},
        {"start": "2000", "end": "2006", "org": "中共崇左市委员会/天等县", "title": "基层履历，具体职务待查", "rank": "", "confidence": "unverified", "source_ids": []},
        {"start": "1995-07", "end": "2000", "org": "广西师范大学/广西自治区", "title": "早期工作经历待查", "rank": "", "confidence": "unverified", "source_ids": []},
    ]
    
    write_person_json(
        {"id": 1, "name": "钟畅姿", "gender": "女", "ethnicity": "水族", "birth": "1971年4月", "birthplace": "广西河池", "education": "研究生学历，文学硕士", "party_join": "1997年9月", "work_start": "1995年7月", "current_post": "钦州市委书记、钦州军分区党委第一书记", "current_org": "中共钦州市委员会", "source": "https://www.baike.com/wiki/钟畅姿"},
        "市委书记",
        extra_entries={
            "career_timeline": zhong_changzi_timeline,
            "professional_profile": {
                "primary_specializations": ["组织人事", "妇女工作", "地方治理"],
                "career_pattern": "cross_county_rotation",
                "systems_experience": ["组织系统", "政府", "群团"],
                "geographic_pattern": ["广西河池（出生）", "贵港", "崇左", "钦州"],
                "promotion_velocity": {
                    "summary": "从基层逐步晋升，经历组织系统、妇联、政府、地方党委多岗位锻炼，2016年升正厅级",
                    "notable_fast_promotions": []
                }
            },
            "open_questions": [
                {"priority": "critical", "question": "2006年之前基层履历不完整", "why_it_matters": "无法确认早期任职对后期工作风格的影响", "suggested_queries": ["钟畅姿 天等县 任职", "钟畅姿 广西 早期 履历"], "last_attempted": "2026-07-23"},
                {"priority": "high", "question": "具体到任钦州市委书记的时间", "why_it_matters": "确认林冠与钟畅姿交接时间", "suggested_queries": ["钟畅姿 任钦州市委书记 时间"], "last_attempted": "2026-07-23"},
                {"priority": "medium", "question": "教育经历——本科是否在广西师范大学", "why_it_matters": "少数民族语言文学专业背景体现专业性", "suggested_queries": ["钟畅姿 广西师范大学"], "last_attempted": "2026-07-23"},
            ]
        }
    )
    
    # Person JSON: 李玉成 (市长)
    li_yucheng_timeline = [
        {"start": "待查", "end": "present", "org": "钦州市人民政府", "title": "钦州市委副书记、市政府市长、党组书记", "rank": "正厅级", "confidence": "confirmed", "source_ids": ["S003"]},
    ]
    
    write_person_json(
        {"id": 2, "name": "李玉成", "gender": "男", "ethnicity": "汉族", "birth": "待查", "birthplace": "待查", "education": "待查", "party_join": "中共党员", "work_start": "待查", "current_post": "钦州市委副书记、市政府市长、党组书记", "current_org": "钦州市人民政府", "source": "https://www.qinzhou.gov.cn/zwgk/ldxx/"},
        "市长",
        extra_entries={
            "career_timeline": li_yucheng_timeline,
            "open_questions": [
                {"priority": "critical", "question": "李玉成完整履历——出生年月、籍贯、教育背景、完整职业生涯", "why_it_matters": "核心目标人物之一，但公开资料极少", "suggested_queries": ["李玉成 钦州 市长 简历", "李玉成 广西 曾任"], "last_attempted": "2026-07-23"},
                {"priority": "critical", "question": "李玉成何时到任钦州市市长", "why_it_matters": "确认接替王雄昌的具体时间", "suggested_queries": ["李玉成 任钦州市市长 时间"], "last_attempted": "2026-07-23"},
                {"priority": "high", "question": "李玉成到钦州前的职务", "why_it_matters": "确认其职业背景和来源", "suggested_queries": ["李玉成 广西 前职"], "last_attempted": "2026-07-23"},
            ],
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "biggest_gap": "李玉成的出生信息、教育背景和完整履历均待查"
            }
        }
    )
    
    # Person JSON: 王雄昌 (前市长)
    wang_xiongchang_timeline = [
        {"start": "2021", "end": "2025/2026", "org": "钦州市人民政府", "title": "钦州市委副书记、市长、党组书记", "rank": "正厅级", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2021", "end": "2025/2026", "org": "中国（广西）自由贸易试验区钦州港片区", "title": "钦州港片区管委会主任", "rank": "正厅级", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2016", "end": "2021", "org": "广西自治区北部湾经济区规划建设管理办公室", "title": "副主任", "rank": "副厅级", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2010", "end": "2016", "org": "钦州保税港区管委会", "title": "副主任、常务副主任", "rank": "副厅级", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2008", "end": "2010", "org": "广西自治区发改委", "title": "相关职务待查", "rank": "", "confidence": "unverified", "source_ids": ["S002"]},
        {"start": "2006", "end": "2008", "org": "广西自治区建设厅", "title": "相关职务待查", "rank": "", "confidence": "unverified", "source_ids": ["S002"]},
        {"start": "2002", "end": "2006", "org": "广西自治区建设厅", "title": "规划处等相关职务", "rank": "", "confidence": "unverified", "source_ids": ["S002"]},
        {"start": "1994", "end": "2002", "org": "广西自治区建设厅", "title": "规划处科员至副处长", "rank": "", "confidence": "unverified", "source_ids": ["S002"]},
        {"start": "1992", "end": "1994", "org": "浙江省宁波市镇海石化总厂", "title": "干部", "rank": "", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "1988", "end": "1992", "org": "浙江大学", "title": "土建结构专业学习", "rank": "", "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    
    write_person_json(
        {"id": 3, "name": "王雄昌", "gender": "男", "ethnicity": "汉族", "birth": "1970年11月", "birthplace": "浙江建德", "education": "在职研究生学历，工学博士", "party_join": "中共党员", "work_start": "1992年", "current_post": "原钦州市委副书记、市长（2026年1月被开除党籍和公职）", "current_org": "", "source": "https://www.baike.com/wiki/王雄昌"},
        "前市长",
        extra_entries={
            "career_timeline": wang_xiongchang_timeline,
            "professional_profile": {
                "primary_specializations": ["城市规划", "港口经济", "园区管理"],
                "career_pattern": "technical_specialist",
                "systems_experience": ["建设系统", "发改委", "保税港区", "政府"],
                "geographic_pattern": ["浙江建德（出生）", "浙江宁波", "广西南宁", "广西钦州"],
                "promotion_velocity": {"summary": "从浙江调广西，长期从事建设规划领域，2021年升正厅级", "notable_fast_promotions": []}
            },
            "risk_and_integrity_signals": [
                {"type": "disciplinary_action", "description": "2026年1月因严重违纪违法被开除党籍和公职", "date": "2026-01", "confidence": "confirmed", "source_ids": ["S002"]}
            ],
            "open_questions": [
                {"priority": "high", "question": "王雄昌违纪违法的具体原因和案情细节", "why_it_matters": "可能涉及钦州港片区建设项目", "suggested_queries": ["王雄昌 严重违纪违法 详情", "王雄昌 双开 通报"], "last_attempted": "2026-07-23"},
                {"priority": "medium", "question": "2002-2010年广西建设厅具体职务细节", "why_it_matters": "确认其专业晋升路径", "suggested_queries": ["王雄昌 建设厅 任职"], "last_attempted": "2026-07-23"},
            ]
        }
    )


if __name__ == "__main__":
    main()
