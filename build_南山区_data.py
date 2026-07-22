#!/usr/bin/env python3
"""
深圳市南山区领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Nanshan District leadership network.

Level: 市辖区
Province: 广东省
Parent City: 深圳市
Region: 南山区
Targets: 区委书记 & 区长

Research Sources:
- 深圳市南山区人民政府官网 (szns.gov.cn) — 区政府领导成员
- Wikipedia (zh.wikipedia.org) — 南山区, 曾湃, 姜建军, 余新国, 梁道行
- 百度百科 — 黄湘岳
- 南方杂志 — 李小宁任命报道

Research Date: 2026-07-22
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "南山区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "南山区_network.gexf")

# ── DATA ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders (as of 2026-07-22)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "黄湘岳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年3月",
        "birthplace": "湖南湘潭",
        "education": "大学(浙江大学化工系有机化工)/在职研究生(武汉大学金融学硕士)/在职博士(北京师范大学自然灾害学博士)",
        "party_join": "1990年6月",
        "work_start": "1991年7月",
        "current_post": "南山区委书记",
        "current_org": "中共深圳市南山区委员会",
        "source": "百度百科-黄湘岳; 深圳市南山区人民政府官网"
    },
    {
        "id": 2,
        "name": "李小宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年9月",
        "birthplace": "待查",
        "education": "大学学历、法律硕士",
        "party_join": "中共党员",
        "work_start": "未知",
        "current_post": "南山区区长",
        "current_org": "深圳市南山区人民政府",
        "source": "深圳市南山区人民政府官网(szns.gov.cn/xxgk/); 南方杂志(李小宁代理区长报道)"
    },
    # ════════════════════════════════════════
    # Key Deputies (区政府领导班子)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "夏雷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年4月",
        "birthplace": "待查",
        "education": "大学学历、工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南山区委常委、副区长",
        "current_org": "深圳市南山区人民政府",
        "source": "深圳市南山区人民政府官网"
    },
    {
        "id": 4,
        "name": "周睿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年9月",
        "birthplace": "待查",
        "education": "研究生学历、理学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南山区委常委、区委(区政府)办公室主任、招商街道党工委书记",
        "current_org": "中共深圳市南山区委员会",
        "source": "深圳市南山区人民政府官网"
    },
    {
        "id": 5,
        "name": "叶春",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1974年1月",
        "birthplace": "待查",
        "education": "大学学历",
        "party_join": "致公党",
        "work_start": "",
        "current_post": "南山区副区长",
        "current_org": "深圳市南山区人民政府",
        "source": "深圳市南山区人民政府官网"
    },
    {
        "id": 6,
        "name": "于红军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年4月",
        "birthplace": "待查",
        "education": "大学学历、工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南山区副区长、市公安局南山分局局长",
        "current_org": "深圳市南山区人民政府",
        "source": "深圳市南山区人民政府官网"
    },
    {
        "id": 7,
        "name": "蔡淡宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年2月",
        "birthplace": "待查",
        "education": "在职研究生学历、法学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南山区副区长",
        "current_org": "深圳市南山区人民政府",
        "source": "深圳市南山区人民政府官网"
    },
    {
        "id": 8,
        "name": "郭晓宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年11月",
        "birthplace": "待查",
        "education": "大学学历、工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南山区副区长",
        "current_org": "深圳市南山区人民政府",
        "source": "深圳市南山区人民政府官网"
    },
    {
        "id": 9,
        "name": "李志娜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1979年6月",
        "birthplace": "待查",
        "education": "研究生学历、法学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南山区副区长",
        "current_org": "深圳市南山区人民政府",
        "source": "深圳市南山区人民政府官网"
    },
    # ════════════════════════════════════════
    # Predecessors (for relationship network)
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "曾湃",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前海管理局局长(曾任)",
        "current_org": "深圳市前海管理局",
        "source": "Wikipedia-曾湃"
    },
    {
        "id": 11,
        "name": "王强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965年",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "深圳市委常委、宣传部部长",
        "current_org": "中共深圳市委宣传部",
        "source": "Wikipedia"
    },
    {
        "id": 12,
        "name": "姜建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1964年",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "湛江市市长(曾任)/深圳市政协副主席(现任)",
        "current_org": "深圳市政协",
        "source": "Wikipedia-姜建军"
    },
    {
        "id": 13,
        "name": "余新国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1964年",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "深圳市委副书记(曾任)/深圳市委常委、政法委书记(曾任)",
        "current_org": "中共深圳市委",
        "source": "Wikipedia-余新国"
    },
    {
        "id": 14,
        "name": "梁道行",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1949年",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "深圳市副市长(曾任)",
        "current_org": "深圳市人民政府",
        "source": "Wikipedia-梁道行"
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共深圳市南山区委员会", "type": "党委", "level": "市辖区", "parent": "中共深圳市委", "location": "深圳市南山区"},
    {"id": 2, "name": "深圳市南山区人民政府", "type": "政府", "level": "市辖区", "parent": "深圳市人民政府", "location": "深圳市南山区"},
    {"id": 3, "name": "中共深圳市委宣传部", "type": "党委", "level": "副省级", "parent": "中共深圳市委", "location": "深圳市"},
    {"id": 4, "name": "中共深圳市委政法委员会", "type": "党委", "level": "副省级", "parent": "中共深圳市委", "location": "深圳市"},
    {"id": 5, "name": "深圳市人民政府", "type": "政府", "level": "副省级", "parent": "广东省人民政府", "location": "深圳市"},
    {"id": 6, "name": "深圳市政协", "type": "政协", "level": "副省级", "parent": "广东省政协", "location": "深圳市"},
    {"id": 7, "name": "深圳市前海深港现代服务业合作区管理局", "type": "开发区", "level": "副省级", "parent": "深圳市政府", "location": "深圳市南山区"},
    {"id": 8, "name": "龙华新区党工委/龙华区委", "type": "党委", "level": "市辖区", "parent": "中共深圳市委", "location": "深圳市龙华区"},
    {"id": 9, "name": "深圳市公安局南山分局", "type": "政府", "level": "区级", "parent": "深圳市公安局", "location": "深圳市南山区"},
    {"id": 10, "name": "南头街道党工委", "type": "党委", "level": "街道", "parent": "南山区委", "location": "深圳市南山区"},
]

# 3. Positions
positions = [
    # 黄湘岳
    {"person_id": 1, "org_id": 1, "title": "南山区委书记", "start_date": "2023年6月", "end_date": "至今", "rank": "副厅级", "note": "2023.06-2024.01兼任区长"},
    {"person_id": 1, "org_id": 2, "title": "南山区区长", "start_date": "2019年9月", "end_date": "2024年1月", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "南山区委副书记", "start_date": "2018年1月", "end_date": "2023年6月", "rank": "副厅级", "note": "2018.01-2019.08兼任政法委书记"},
    {"person_id": 1, "org_id": 4, "title": "深圳市委政法委专职委员", "start_date": "2016年9月", "end_date": "2019年8月", "rank": "正处级", "note": "期间2018年起任南山区委副书记"},
    {"person_id": 1, "org_id": 4, "title": "深圳市委政法委维稳办专职副主任", "start_date": "2013年7月", "end_date": "2016年9月", "rank": "正处级", "note": ""},
    # 李小宁
    {"person_id": 2, "org_id": 2, "title": "南山区区长(代理)", "start_date": "2024年1月", "end_date": "至今", "rank": "副厅级", "note": "代理区长"},
    # 夏雷
    {"person_id": 3, "org_id": 2, "title": "南山区委常委、副区长", "start_date": "未知", "end_date": "至今", "rank": "副厅级", "note": "负责教育、科技、民政等"},
    # 周睿
    {"person_id": 4, "org_id": 1, "title": "南山区委常委、区委(区政府)办公室主任、招商街道党工委书记", "start_date": "未知", "end_date": "至今", "rank": "副厅级", "note": ""},
    # 叶春
    {"person_id": 5, "org_id": 2, "title": "南山区副区长", "start_date": "未知", "end_date": "至今", "rank": "副厅级", "note": "致公党"},
    # 于红军
    {"person_id": 6, "org_id": 2, "title": "南山区副区长", "start_date": "未知", "end_date": "至今", "rank": "副厅级", "note": "兼公安分局局长"},
    {"person_id": 6, "org_id": 9, "title": "南山公安分局局长", "start_date": "未知", "end_date": "至今", "rank": "正处级", "note": ""},
    # 蔡淡宏
    {"person_id": 7, "org_id": 2, "title": "南山区副区长", "start_date": "未知", "end_date": "至今", "rank": "副厅级", "note": "负责城市更新、金融等"},
    # 郭晓宁
    {"person_id": 8, "org_id": 2, "title": "南山区副区长", "start_date": "未知", "end_date": "至今", "rank": "副厅级", "note": "负责住建、城管等"},
    # 李志娜
    {"person_id": 9, "org_id": 2, "title": "南山区副区长", "start_date": "未知", "end_date": "至今", "rank": "副厅级", "note": "负责工业、商务等"},
    # 曾湃
    {"person_id": 10, "org_id": 1, "title": "南山区委书记", "start_date": "2020年9月", "end_date": "2023年6月", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "南山区区长", "start_date": "2017年10月", "end_date": "2019年6月", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 7, "title": "前海管理局局长", "start_date": "2021年11月", "end_date": "2023年", "rank": "正厅级", "note": "深圳市委常委兼任"},
    # 王强
    {"person_id": 11, "org_id": 1, "title": "南山区委书记", "start_date": "2017年", "end_date": "2020年9月", "rank": "副厅级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "南山区区长", "start_date": "2015年", "end_date": "2017年", "rank": "副厅级", "note": ""},
    {"person_id": 11, "org_id": 3, "title": "深圳市委常委、宣传部部长", "start_date": "2021年", "end_date": "至今", "rank": "副省级", "note": ""},
    # 姜建军
    {"person_id": 12, "org_id": 1, "title": "南山区委书记", "start_date": "2015年7月", "end_date": "2017年4月", "rank": "副厅级", "note": ""},
    {"person_id": 12, "org_id": 8, "title": "龙华新区党工委书记", "start_date": "2013年", "end_date": "2015年7月", "rank": "副厅级", "note": "后龙华升格为行政区"},
    {"person_id": 12, "org_id": 6, "title": "深圳市政协副主席", "start_date": "2020年", "end_date": "至今", "rank": "正厅级", "note": ""},
    # 余新国
    {"person_id": 13, "org_id": 2, "title": "南山区区长", "start_date": "2011年11月", "end_date": "2015年8月", "rank": "副厅级", "note": ""},
    {"person_id": 13, "org_id": 8, "title": "龙华新区党工委书记/龙华区委书记", "start_date": "2015年8月", "end_date": "2018年6月", "rank": "副厅级", "note": ""},
    {"person_id": 13, "org_id": 4, "title": "深圳市委常委、政法委书记", "start_date": "2018年6月", "end_date": "2022年9月", "rank": "副省级", "note": ""},
    # 梁道行
    {"person_id": 14, "org_id": 1, "title": "南山区委书记", "start_date": "1997年12月", "end_date": "2002年2月", "rank": "副厅级", "note": ""},
    {"person_id": 14, "org_id": 5, "title": "深圳市副市长", "start_date": "2002年2月", "end_date": "2012年", "rank": "副省级", "note": "2012年落马"},
]

# 4. Relationships
relationships = [
    # 当前班子成员间的工作关系
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—区长党政搭档", "overlap_org": "南山区", "overlap_period": "2024.01-至今"},
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "区委书记—区委常委/副区长", "overlap_org": "南山区委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "区委书记—区委常委/办公室主任", "overlap_org": "南山区委", "overlap_period": "至今"},
    # 党政搭档关系
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "区长—副区长", "overlap_org": "南山区政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "区长—副区长", "overlap_org": "南山区政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "区长—副区长", "overlap_org": "南山区政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "区长—副区长", "overlap_org": "南山区政府", "overlap_period": "至今"},
    # 区委书记—前任关系 (继任链)
    {"person_a": 1, "person_b": 10, "type": "继任", "context": "黄湘岳接替曾湃任南山区委书记", "overlap_org": "南山区委", "overlap_period": "2023.06"},
    {"person_a": 1, "person_b": 11, "type": "继任", "context": "黄湘岳接替王强任南山区长", "overlap_org": "南山区政府", "overlap_period": "2019.09"},
    {"person_a": 10, "person_b": 11, "type": "继任", "context": "曾湃接替王强任南山区委书记", "overlap_org": "南山区委", "overlap_period": "2020.09"},
    # 跨区交流关系
    {"person_a": 13, "person_b": 12, "type": "跨区", "context": "余新国(南山区长)→龙华; 姜建军(龙华书记)→南山; 双向交换", "overlap_org": "南山区-龙华区", "overlap_period": "2015"},
    {"person_a": 10, "person_b": 1, "type": "共事", "context": "曾湃任南山区长时黄湘岳任区委副书记", "overlap_org": "南山区", "overlap_period": "2018-2019"},
    # 南山区—龙华区干部交流
    {"person_a": 13, "person_b": 12, "type": "跨区", "context": "南山-龙华双向干部交流", "overlap_org": "南山-龙华", "overlap_period": "2015"},
    {"person_a": 12, "person_b": 13, "type": "跨区", "context": "姜建军(龙华→南山) 余新国(南山→龙华)", "overlap_org": "南山-龙华", "overlap_period": "2015"},
    # 南山区内的上下级关系
    {"person_a": 3, "person_b": 4, "type": "共事", "context": "同为南山区委常委", "overlap_org": "南山区委", "overlap_period": "至今"},
    {"person_a": 3, "person_b": 7, "type": "共事", "context": "南山区政府副区长", "overlap_org": "南山区政府", "overlap_period": "至今"},
    {"person_a": 5, "person_b": 8, "type": "共事", "context": "南山区政府副区长", "overlap_org": "南山区政府", "overlap_period": "至今"},
]


# ── DB & GEXF Generation ──

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(post):
    if "书记" in post:
        return "255,50,50"
    elif "区长" in post and "书记" not in post:
        return "50,100,255"
    elif "副区长" in post:
        return "50,100,255"
    elif "局长" in post:
        return "255,165,0"
    elif "维稳" in post:
        return "255,165,0"
    else:
        return "100,100,100"

def is_top_leader(name, post):
    top_names = ["黄湘岳", "李小宁"]
    return name in top_names

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Drop existing tables
    cur.execute("DROP TABLE IF EXISTS relationships")
    cur.execute("DROP TABLE IF EXISTS positions")
    cur.execute("DROP TABLE IF EXISTS organizations")
    cur.execute("DROP TABLE IF EXISTS persons")
    
    # Create tables
    cur.execute("""CREATE TABLE persons (
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
    )""")
    cur.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT DEFAULT '',
        level TEXT DEFAULT '',
        parent TEXT DEFAULT '',
        location TEXT DEFAULT ''
    )""")
    cur.execute("""CREATE TABLE positions (
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
    )""")
    cur.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER NOT NULL,
        person_b INTEGER NOT NULL,
        type TEXT DEFAULT '',
        context TEXT DEFAULT '',
        overlap_org TEXT DEFAULT '',
        overlap_period TEXT DEFAULT '',
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    )""")
    
    # Insert persons
    for p in persons:
        cur.execute("""INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
             p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))
    
    # Insert organizations
    for o in organizations:
        cur.execute("""INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    
    # Insert positions
    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))
    
    # Insert relationships
    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))
    
    conn.commit()
    conn.close()
    
    print(f"✅ DB ready: {DB_PATH}")
    print(f"   Persons: {len(persons)}")
    print(f"   Organizations: {len(organizations)}")
    print(f"   Positions: {len(positions)}")
    print(f"   Relationships: {len(relationships)}")

def build_gexf():
    from datetime import datetime
    
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>深圳市南山区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    
    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="gender" type="string"/>')
    lines.append('      <attribute id="4" title="ethnicity" type="string"/>')
    lines.append('      <attribute id="5" title="birth" type="string"/>')
    lines.append('      <attribute id="6" title="source" type="string"/>')
    lines.append('      <attribute id="7" title="org_type" type="string"/>')
    lines.append('    </attributes>')
    
    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')
    
    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["current_post"])
        sz = "20.0" if is_top_leader(p["name"], p["current_post"]) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["gender"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["ethnicity"])}"/>')
        lines.append(f'          <attvalue for="5" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="6" value="{esc(p["source"][:50])}"/>')
        lines.append('        </attvalues>')
        r, g, b = c.split(",")
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    
    # Organization nodes
    for o in organizations:
        o_color = {"党委": "255,200,200", "政府": "200,200,255", "开发区": "200,255,200",
                     "政协": "255,240,200"}.get(o["type"], "200,200,200")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="7" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        r2, g2, b2 = o_color.split(",")
        lines.append(f'        <viz:color r="{r2}" g="{g2}" b="{b2}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    
    lines.append('    </nodes>')
    
    # Edges
    lines.append('    <edges>')
    eid = 0
    
    # Person→Organization edges (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("note",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos["start_date"])}-{esc(pos["end_date"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    
    # Person↔Person edges (relationships)
    for r in relationships:
        eid += 1
        weight = "2.0"
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{weight}">')
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
    
    print(f"✅ GEXF ready: {GEXF_PATH}")
    print(f"   Nodes: {len(persons) + len(organizations)}")
    print(f"   Edges: {eid}")


# ── Main ──
if __name__ == "__main__":
    build_db()
    build_gexf()
    print("\n🎉 南山区数据构建完成!")
