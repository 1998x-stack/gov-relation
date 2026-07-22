#!/usr/bin/env python3
"""
广德市 (Guangde City) — Leadership Network Data Builder
Province: 安徽省
Parent City: 宣城市
Level: 县级市
Generated: 2026-07-16
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

# ── Paths ────────────────────────────────────────────────────────────
STAGING = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING, "广德市_network.db")
GEXF_PATH = os.path.join(STAGING, "广德市_network.gexf")
TODAY = "2026-07-16"

# ── DATA: Persons ────────────────────────────────────────────────────
persons = [
    {
        "id": "jin_ning",
        "name": "金宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "广德市委书记",
        "current_org": "中国共产党广德市委员会",
        "source": "广德市人民政府网站",
        "notes": "2026年6月当选广德市委书记（市第二次党代会）",
        "confidence": "confirmed",
    },
    {
        "id": "qian_hui",
        "name": "钱会",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年5月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "广德市委副书记、市长",
        "current_org": "广德市人民政府",
        "source": "广德市人民政府网站",
        "notes": "历任广德县政府副县长，广德县委常委、县政府党组成员，共青团宣城市委党组书记、书记，泾县县委副书记、党校校长",
        "confidence": "confirmed",
    },
    {
        "id": "zhang_yongguo",
        "name": "张勇国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年6月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府党组副书记，广德经开区党工委书记、管委会主任",
        "current_org": "广德市人民政府",
        "source": "广德市人民政府网站",
        "notes": "历任广德市新杭镇党委书记，广德经开区党工委书记、管委会主任，广德市委常委、市政府副市长、党组副书记",
        "confidence": "confirmed",
    },
    {
        "id": "hu_xinghua",
        "name": "胡兴华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年3月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委，市政府党组副书记、常务副市长",
        "current_org": "广德市人民政府",
        "source": "广德市人民政府网站",
        "notes": "历任旌德县政府副县长、党组成员，旌德县委常委、政法委书记、群工部部长，旌德县政府常务副县长、党组副书记",
        "confidence": "confirmed",
    },
    {
        "id": "wang_zeyin",
        "name": "王泽银",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年9月",
        "birthplace": "",
        "native_place": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市政府党组成员、副市长，市公安局党委书记、局长、督察长",
        "current_org": "广德市人民政府",
        "source": "广德市人民政府网站",
        "notes": "历任宁国市公安局西津派出所所长，宁国市西津街道党工委书记，宁国市教育体育局党委书记、局长",
        "confidence": "confirmed",
    },
    {
        "id": "jiang_xiaohua",
        "name": "江晓华",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政府副市长",
        "current_org": "广德市人民政府",
        "source": "广德市人民政府网站",
        "notes": "",
        "confidence": "confirmed",
    },
    {
        "id": "kuai_haoning",
        "name": "蒯浩宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府党组成员、副市长",
        "current_org": "广德市人民政府",
        "source": "广德市人民政府网站",
        "notes": "",
        "confidence": "confirmed",
    },
    {
        "id": "sun_kai",
        "name": "孙凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府党组成员、副市长",
        "current_org": "广德市人民政府",
        "source": "广德市人民政府网站",
        "notes": "",
        "confidence": "confirmed",
    },
    {
        "id": "xiang_zexian",
        "name": "向泽显",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府党组成员、副市长",
        "current_org": "广德市人民政府",
        "source": "广德市人民政府网站",
        "notes": "",
        "confidence": "confirmed",
    },
    {
        "id": "zhou_gaichao",
        "name": "周改超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府党组成员、副市长（挂职）",
        "current_org": "广德市人民政府",
        "source": "广德市人民政府网站",
        "notes": "挂职",
        "confidence": "confirmed",
    },
    {
        "id": "li_jun",
        "name": "李军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "广德市人大常委会主任",
        "current_org": "广德市人大常委会",
        "source": "广德新闻网",
        "notes": "市四大班子领导成员",
        "confidence": "confirmed",
    },
    {
        "id": "liu_qun",
        "name": "刘群",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "广德市政协主席",
        "current_org": "广德市政协",
        "source": "广德新闻网",
        "notes": "市四大班子领导成员",
        "confidence": "confirmed",
    },
    {
        "id": "li_meng",
        "name": "李檬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "广德市委常委",
        "current_org": "中国共产党广德市委员会",
        "source": "广德新闻网",
        "notes": "市四大班子领导成员",
        "confidence": "confirmed",
    },
    {
        "id": "zhou_qihong",
        "name": "周其红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "公开报道",
        "notes": "前任广德市委书记，后调任宣城市",
        "confidence": "plausible",
    },
]

# ── DATA: Organizations ──────────────────────────────────────────────
organizations = [
    {
        "id": "guangde_cpc",
        "name": "中国共产党广德市委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中国共产党宣城市委员会",
        "location": "广德市",
    },
    {
        "id": "guangde_gov",
        "name": "广德市人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "宣城市人民政府",
        "location": "广德市",
    },
    {
        "id": "guangde_npc",
        "name": "广德市人大常委会",
        "type": "人大",
        "level": "县级",
        "parent": "",
        "location": "广德市",
    },
    {
        "id": "guangde_cppcc",
        "name": "广德市政协",
        "type": "政协",
        "level": "县级",
        "parent": "",
        "location": "广德市",
    },
    {
        "id": "guangde_psb",
        "name": "广德市公安局",
        "type": "政府",
        "level": "县级",
        "parent": "广德市人民政府",
        "location": "广德市",
    },
    {
        "id": "guangde_edz",
        "name": "广德经济技术开发区",
        "type": "开发区",
        "level": "县级",
        "parent": "广德市人民政府",
        "location": "广德市",
    },
    {
        "id": "xuancheng_cyl",
        "name": "共青团宣城市委员会",
        "type": "群团",
        "level": "地市级",
        "parent": "",
        "location": "宣城市",
    },
    {
        "id": "jingxian_cpc",
        "name": "中国共产党泾县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中国共产党宣城市委员会",
        "location": "泾县",
    },
    {
        "id": "jingde_cpc",
        "name": "中国共产党旌德县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中国共产党宣城市委员会",
        "location": "旌德县",
    },
    {
        "id": "jingde_gov",
        "name": "旌德县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "宣城市人民政府",
        "location": "旌德县",
    },
    {
        "id": "ningguo_psb",
        "name": "宁国市公安局",
        "type": "政府",
        "level": "县级",
        "parent": "宁国市人民政府",
        "location": "宁国市",
    },
    {
        "id": "ningguo_xijin",
        "name": "宁国市西津街道办事处",
        "type": "乡镇/街道",
        "level": "乡镇级",
        "parent": "宁国市人民政府",
        "location": "宁国市",
    },
    {
        "id": "ningguo_edu",
        "name": "宁国市教育体育局",
        "type": "政府",
        "level": "县级",
        "parent": "宁国市人民政府",
        "location": "宁国市",
    },
    {
        "id": "xinhang_town",
        "name": "广德市新杭镇",
        "type": "乡镇/街道",
        "level": "乡镇级",
        "parent": "广德市人民政府",
        "location": "广德市",
    },
]

# ── DATA: Positions ──────────────────────────────────────────────────
positions = [
    # 金宁
    {"person_id": "jin_ning", "org_id": "guangde_cpc", "title": "广德市委书记", "start": "2026年6月", "end": "present", "rank": "正县级", "note": "市第二次党代会当选"},
    # 钱会
    {"person_id": "qian_hui", "org_id": "guangde_gov", "title": "广德市市长", "start": "", "end": "present", "rank": "正县级", "note": "现任"},
    {"person_id": "qian_hui", "org_id": "guangde_cpc", "title": "广德市委副书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": "qian_hui", "org_id": "guangde_gov", "title": "广德县政府副县长", "start": "", "end": "", "rank": "副县级", "note": "早期任职"},
    {"person_id": "qian_hui", "org_id": "guangde_cpc", "title": "广德县委常委、县政府党组成员", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": "qian_hui", "org_id": "xuancheng_cyl", "title": "共青团宣城市委党组书记、书记", "start": "", "end": "", "rank": "正县级", "note": ""},
    {"person_id": "qian_hui", "org_id": "jingxian_cpc", "title": "泾县县委副书记、党校校长", "start": "", "end": "", "rank": "副县级", "note": ""},
    # 张勇国
    {"person_id": "zhang_yongguo", "org_id": "guangde_gov", "title": "市政府党组副书记，广德经开区党工委书记、管委会主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": "zhang_yongguo", "org_id": "xinhang_town", "title": "新杭镇党委书记", "start": "", "end": "", "rank": "正科级", "note": ""},
    {"person_id": "zhang_yongguo", "org_id": "guangde_edz", "title": "广德经开区党工委书记、管委会主任", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": "zhang_yongguo", "org_id": "guangde_cpc", "title": "广德市委常委、市政府副市长、党组副书记", "start": "", "end": "", "rank": "副县级", "note": ""},
    # 胡兴华
    {"person_id": "hu_xinghua", "org_id": "guangde_gov", "title": "市委常委、常务副市长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": "hu_xinghua", "org_id": "jingde_gov", "title": "旌德县政府副县长、党组成员", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": "hu_xinghua", "org_id": "jingde_cpc", "title": "旌德县委常委、政法委书记、群工部部长", "start": "", "end": "", "rank": "副县级", "note": ""},
    {"person_id": "hu_xinghua", "org_id": "jingde_gov", "title": "旌德县政府常务副县长、党组副书记", "start": "", "end": "", "rank": "副县级", "note": ""},
    # 王泽银
    {"person_id": "wang_zeyin", "org_id": "guangde_gov", "title": "市委常委、副市长，市公安局党委书记、局长、督察长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": "wang_zeyin", "org_id": "ningguo_psb", "title": "宁国市公安局西津派出所所长", "start": "", "end": "", "rank": "副科级", "note": ""},
    {"person_id": "wang_zeyin", "org_id": "ningguo_xijin", "title": "西津街道党工委书记", "start": "", "end": "", "rank": "正科级", "note": ""},
    {"person_id": "wang_zeyin", "org_id": "ningguo_edu", "title": "宁国市教育体育局党委书记、局长", "start": "", "end": "", "rank": "正科级", "note": ""},
    # 其他副市长
    {"person_id": "jiang_xiaohua", "org_id": "guangde_gov", "title": "市政府副市长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": "kuai_haoning", "org_id": "guangde_gov", "title": "市政府党组成员、副市长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": "sun_kai", "org_id": "guangde_gov", "title": "市政府党组成员、副市长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": "xiang_zexian", "org_id": "guangde_gov", "title": "市政府党组成员、副市长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": "zhou_gaichao", "org_id": "guangde_gov", "title": "市政府党组成员、副市长（挂职）", "start": "", "end": "present", "rank": "副县级", "note": "挂职"},
    # 人大、政协
    {"person_id": "li_jun", "org_id": "guangde_npc", "title": "市人大常委会主任", "start": "", "end": "present", "rank": "正县级", "note": ""},
    {"person_id": "liu_qun", "org_id": "guangde_cppcc", "title": "市政协主席", "start": "", "end": "present", "rank": "正县级", "note": ""},
    {"person_id": "li_meng", "org_id": "guangde_cpc", "title": "市委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
]

# ── DATA: Relationships ──────────────────────────────────────────────
relationships = [
    {
        "person_a": "jin_ning", "person_b": "qian_hui",
        "type": "superior_subordinate",
        "context": "市委书记与市长党政主要领导搭档",
        "overlap_org": "广德市",
        "overlap_period": "2026年6月至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": "jin_ning", "person_b": "li_jun",
        "type": "superior_subordinate",
        "context": "市委主要领导与市人大常委会主任",
        "overlap_org": "广德市",
        "overlap_period": "2026年6月至今",
        "strength": "medium",
        "confidence": "confirmed",
    },
    {
        "person_a": "jin_ning", "person_b": "liu_qun",
        "type": "superior_subordinate",
        "context": "市委主要领导与市政协主席",
        "overlap_org": "广德市",
        "overlap_period": "2026年6月至今",
        "strength": "medium",
        "confidence": "confirmed",
    },
    {
        "person_a": "jin_ning", "person_b": "li_meng",
        "type": "superior_subordinate",
        "context": "市委书记与市委常委",
        "overlap_org": "中国共产党广德市委员会",
        "overlap_period": "2026年6月至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": "qian_hui", "person_b": "hu_xinghua",
        "type": "superior_subordinate",
        "context": "市长与常务副市长",
        "overlap_org": "广德市人民政府",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": "qian_hui", "person_b": "zhang_yongguo",
        "type": "overlap",
        "context": "市长与市政府党组副书记，曾共事于广德市政府",
        "overlap_org": "广德市人民政府",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": "qian_hui", "person_b": "wang_zeyin",
        "type": "superior_subordinate",
        "context": "市长与分管公安的副市长",
        "overlap_org": "广德市人民政府",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": "hu_xinghua", "person_b": "wang_zeyin",
        "type": "overlap",
        "context": "常务副市长与副市长同在市府班子",
        "overlap_org": "广德市人民政府",
        "overlap_period": "至今",
        "strength": "medium",
        "confidence": "confirmed",
    },
    {
        "person_a": "zhang_yongguo", "person_b": "hu_xinghua",
        "type": "overlap",
        "context": "先后担任广德市常务副市长/经开区主任，同在市府班子",
        "overlap_org": "广德市人民政府",
        "overlap_period": "至今",
        "strength": "medium",
        "confidence": "confirmed",
    },
    {
        "person_a": "jin_ning", "person_b": "zhou_qihong",
        "type": "predecessor_successor",
        "context": "周其红为金宁前任广德市委书记",
        "overlap_org": "中国共产党广德市委员会",
        "overlap_period": "",
        "strength": "medium",
        "confidence": "plausible",
    },
]


# ── BUILD FUNCTIONS ──────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_db():
    """Create SQLite database."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE persons (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            native_place TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT,
            notes TEXT,
            confidence TEXT
        )
    """)

    c.execute("""
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)

    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            strength TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace,
                                 native_place, education, party_join, work_start,
                                 current_post, current_org, source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
            p.get("birth", ""), p.get("birthplace", ""), p.get("native_place", ""),
            p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
            p.get("current_post", ""), p.get("current_org", ""),
            p.get("source", ""), p.get("notes", ""), p.get("confidence", ""),
        ))

    for o in organizations:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            pos["person_id"], pos["org_id"], pos["title"],
            pos.get("start", ""), pos.get("end", ""),
            pos.get("rank", ""), pos.get("note", ""),
        ))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context,
                                       overlap_org, overlap_period, strength)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            r["person_a"], r["person_b"], r["type"], r.get("context", ""),
            r.get("overlap_org", ""), r.get("overlap_period", ""), r.get("strength", ""),
        ))

    conn.commit()
    conn.close()
    print(f"[DB] Created: {DB_PATH}")


def build_gexf():
    """Create GEXF graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>广德市 (Guangde, Xuancheng, Anhui) — Leadership Network Graph</description>')
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
    lines.append('      <attribute id="2" title="strength" type="string"/>')
    lines.append('    </attributes>')

    def person_color(p):
        post = p.get("current_post", "")
        if "市委书记" in post:
            return "255,50,50"   # red — party secretary
        if "市长" in post:
            return "50,100,255"  # blue — government leader
        if "常务副市长" in post:
            return "50,100,255"  # blue
        if "纪委书记" in post:
            return "255,165,0"   # orange — discipline
        if "人大" in post or "政协" in post:
            return "100,180,100" # green — congress/CPPCC
        if "市委常委" in post:
            return "200,100,100" # light red — party standing committee
        return "100,100,100"     # grey — others

    def is_top_leader(p):
        return "市委书记" in p.get("current_post", "") or "市长" in p.get("current_post", "")

    def org_color(o):
        t = o["type"]
        if "党委" in t:
            return "255,200,200"
        if "政府" in t:
            return "200,200,255"
        if "人大" in t:
            return "200,255,255"
        if "政协" in t:
            return "255,240,200"
        if "开发区" in t:
            return "200,255,200"
        if "乡镇/街道" in t:
            return "255,255,200"
        if "群团" in t:
            return "255,220,255"
        return "200,200,200"

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="{esc(p["id"])}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="{esc(o["id"])}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization edges
    for pos in positions:
        lines.append(f'      <edge id="e{eid}" source="{esc(pos["person_id"])}" target="{esc(pos["org_id"])}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person ↔ Person edges
    for r in relationships:
        weight = "2.0" if r.get("strength") == "strong" else "1.5" if r.get("strength") == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{esc(r["person_a"])}" target="{esc(r["person_b"])}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("strength", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[GEXF] Created: {GEXF_PATH}")
    print(f"[GEXF] Nodes: {len(persons)} persons + {len(organizations)} orgs")
    print(f"[GEXF] Edges: {len(positions)} worked_at + {len(relationships)} relationships")


def main():
    os.makedirs(STAGING, exist_ok=True)
    build_db()
    build_gexf()

    print(f"\n{'=' * 50}")
    print(f"广德市 Leadership Network — Build Complete")
    print(f"{'=' * 50}")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print(f"\nOutput files:")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
