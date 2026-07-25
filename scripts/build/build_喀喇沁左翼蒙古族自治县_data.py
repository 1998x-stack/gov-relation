#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 喀喇沁左翼蒙古族自治县 leadership network.

Research date: 2026-07-25
Research sources:
  - https://www.kazuo.gov.cn (official county government site)
  - https://www.kazuo.gov.cn/kzxzf/zwgk/zfld/glist.html (government leadership page)
  - 2026-07 news articles from kazuo.gov.cn (16th Party Congress coverage)
"""

import sqlite3
import os
import sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "喀喇沁左翼蒙古族自治县_network.db")
GEXF_PATH = os.path.join(BASE, "喀喇沁左翼蒙古族自治县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {
        "id": 1, "name": "杨春柏", "gender": "男", "ethnicity": "汉族",
        "birth": "unknown", "birthplace": "unknown", "education": "unknown",
        "party_join": "中共党员", "work_start": "unknown",
        "current_post": "中共喀喇沁左翼蒙古族自治县委书记",
        "current_org": "中共喀喇沁左翼蒙古族自治县委员会",
        "source": "https://www.kazuo.gov.cn/html/KZXZF/202607/0178398586976375.html"
    },
    {
        "id": 2, "name": "韩健", "gender": "男", "ethnicity": "蒙古族",
        "birth": "1978-04", "birthplace": "unknown", "education": "在职研究生/工学硕士",
        "party_join": "中共党员", "work_start": "unknown",
        "current_post": "中共喀左县委副书记、县长、朝阳喀左经济开发区党工委书记（兼）",
        "current_org": "喀喇沁左翼蒙古族自治县人民政府",
        "source": "https://www.kazuo.gov.cn/kzxzf/zwgk/zfld/glist.html"
    },
    # ── Government Leadership Team ──
    {
        "id": 3, "name": "徐广强", "gender": "男", "ethnicity": "汉族",
        "birth": "1968-11", "birthplace": "unknown", "education": "大专",
        "party_join": "中共党员", "work_start": "unknown",
        "current_post": "喀左县委常委、常务副县长",
        "current_org": "喀喇沁左翼蒙古族自治县人民政府",
        "source": "https://www.kazuo.gov.cn/kzxzf/zwgk/zfld/glist.html"
    },
    {
        "id": 4, "name": "于涛", "gender": "男", "ethnicity": "汉族",
        "birth": "1982-04", "birthplace": "unknown", "education": "研究生/历史学硕士",
        "party_join": "中共党员", "work_start": "unknown",
        "current_post": "朝阳喀左经济开发区管委会主任",
        "current_org": "朝阳喀左经济开发区",
        "source": "https://www.kazuo.gov.cn/kzxzf/zwgk/zfld/glist.html"
    },
    {
        "id": 5, "name": "房家阳", "gender": "男", "ethnicity": "蒙古族",
        "birth": "1984-12", "birthplace": "unknown", "education": "大学/工学学士",
        "party_join": "中共党员", "work_start": "unknown",
        "current_post": "喀左县委常委、副县长",
        "current_org": "喀喇沁左翼蒙古族自治县人民政府",
        "source": "https://www.kazuo.gov.cn/kzxzf/zwgk/zfld/glist.html"
    },
    {
        "id": 6, "name": "刘秀娟", "gender": "女", "ethnicity": "蒙古族",
        "birth": "1968-09", "birthplace": "unknown", "education": "大学",
        "party_join": "中共党员", "work_start": "unknown",
        "current_post": "喀左县人民政府副县长",
        "current_org": "喀喇沁左翼蒙古族自治县人民政府",
        "source": "https://www.kazuo.gov.cn/kzxzf/zwgk/zfld/glist.html"
    },
    {
        "id": 7, "name": "张晶", "gender": "女", "ethnicity": "汉族",
        "birth": "1986-01", "birthplace": "unknown", "education": "大学/在职公共管理硕士",
        "party_join": "中共党员", "work_start": "unknown",
        "current_post": "喀左县人民政府副县长",
        "current_org": "喀喇沁左翼蒙古族自治县人民政府",
        "source": "https://www.kazuo.gov.cn/kzxzf/zwgk/zfld/glist.html"
    },
    {
        "id": 8, "name": "王德文", "gender": "男", "ethnicity": "蒙古族",
        "birth": "1974-09", "birthplace": "unknown", "education": "大专",
        "party_join": "中共党员", "work_start": "unknown",
        "current_post": "喀左县人民政府副县长",
        "current_org": "喀喇沁左翼蒙古族自治县人民政府",
        "source": "https://www.kazuo.gov.cn/kzxzf/zwgk/zfld/glist.html"
    },
    {
        "id": 9, "name": "钱文涛", "gender": "男", "ethnicity": "汉族",
        "birth": "1985-11", "birthplace": "unknown", "education": "省委党校研究生/法学学士",
        "party_join": "中共党员", "work_start": "unknown",
        "current_post": "喀左县人民政府副县长、县公安局局长",
        "current_org": "喀喇沁左翼蒙古族自治县人民政府",
        "source": "https://www.kazuo.gov.cn/kzxzf/zwgk/zfld/glist.html"
    },
    {
        "id": 10, "name": "王崇东", "gender": "男", "ethnicity": "汉族",
        "birth": "1972-09", "birthplace": "unknown", "education": "大学",
        "party_join": "中共党员", "work_start": "unknown",
        "current_post": "喀左县人民政府党组成员（副处级）",
        "current_org": "喀喇沁左翼蒙古族自治县人民政府",
        "source": "https://www.kazuo.gov.cn/kzxzf/zwgk/zfld/glist.html"
    },
    {
        "id": 11, "name": "姜岱盛", "gender": "男", "ethnicity": "蒙古族",
        "birth": "1970-12", "birthplace": "unknown", "education": "大学",
        "party_join": "中共党员", "work_start": "unknown",
        "current_post": "喀左县人民政府四级调研员、副处级干部",
        "current_org": "喀喇沁左翼蒙古族自治县人民政府",
        "source": "https://www.kazuo.gov.cn/kzxzf/zwgk/zfld/glist.html"
    },
    # ── Party Leadership (from 16th Party Congress coverage) ──
    {
        "id": 12, "name": "杨朝辉", "gender": "男", "ethnicity": "unknown",
        "birth": "unknown", "birthplace": "unknown", "education": "unknown",
        "party_join": "中共党员", "work_start": "unknown",
        "current_post": "中共喀左县委领导",
        "current_org": "中共喀喇沁左翼蒙古族自治县委员会",
        "source": "https://www.kazuo.gov.cn/html/KZXZF/202607/0178476342932112.html"
    },
    {
        "id": 13, "name": "宋永波", "gender": "男", "ethnicity": "unknown",
        "birth": "unknown", "birthplace": "unknown", "education": "unknown",
        "party_join": "中共党员", "work_start": "unknown",
        "current_post": "中共喀左县委领导",
        "current_org": "中共喀喇沁左翼蒙古族自治县委员会",
        "source": "https://www.kazuo.gov.cn/html/KZXZF/202607/0178484756629882.html"
    },
    {
        "id": 14, "name": "李海源", "gender": "男", "ethnicity": "unknown",
        "birth": "unknown", "birthplace": "unknown", "education": "unknown",
        "party_join": "中共党员", "work_start": "unknown",
        "current_post": "中共喀左县委领导",
        "current_org": "中共喀喇沁左翼蒙古族自治县委员会",
        "source": "https://www.kazuo.gov.cn/html/KZXZF/202607/0178484756629882.html"
    },
    {
        "id": 15, "name": "刘东涛", "gender": "男", "ethnicity": "unknown",
        "birth": "unknown", "birthplace": "unknown", "education": "unknown",
        "party_join": "中共党员", "work_start": "unknown",
        "current_post": "中共喀左县委领导",
        "current_org": "中共喀喇沁左翼蒙古族自治县委员会",
        "source": "https://www.kazuo.gov.cn/html/KZXZF/202607/0178484756629882.html"
    },
    {
        "id": 16, "name": "陈天虹", "gender": "男", "ethnicity": "unknown",
        "birth": "unknown", "birthplace": "unknown", "education": "unknown",
        "party_join": "中共党员", "work_start": "unknown",
        "current_post": "中共喀左县委领导",
        "current_org": "中共喀喇沁左翼蒙古族自治县委员会",
        "source": "https://www.kazuo.gov.cn/html/KZXZF/202607/0178484756629882.html"
    },
    {
        "id": 17, "name": "谢育", "gender": "男", "ethnicity": "unknown",
        "birth": "unknown", "birthplace": "unknown", "education": "unknown",
        "party_join": "中共党员", "work_start": "unknown",
        "current_post": "中共喀左县委领导",
        "current_org": "中共喀喇沁左翼蒙古族自治县委员会",
        "source": "https://www.kazuo.gov.cn/html/KZXZF/202607/0178484756629882.html"
    },
    {
        "id": 18, "name": "遇长波", "gender": "男", "ethnicity": "unknown",
        "birth": "unknown", "birthplace": "unknown", "education": "unknown",
        "party_join": "中共党员", "work_start": "unknown",
        "current_post": "中共喀左县委领导",
        "current_org": "中共喀喇沁左翼蒙古族自治县委员会",
        "source": "https://www.kazuo.gov.cn/html/KZXZF/202607/0178484756629882.html"
    },
    {
        "id": 19, "name": "马贤军", "gender": "男", "ethnicity": "unknown",
        "birth": "unknown", "birthplace": "unknown", "education": "unknown",
        "party_join": "中共党员", "work_start": "unknown",
        "current_post": "喀左县人大常委会领导",
        "current_org": "喀喇沁左翼蒙古族自治县人大常委会",
        "source": "https://www.kazuo.gov.cn/html/KZXZF/202607/0178484756629882.html"
    },
    {
        "id": 20, "name": "赵升龙", "gender": "男", "ethnicity": "unknown",
        "birth": "unknown", "birthplace": "unknown", "education": "unknown",
        "party_join": "中共党员", "work_start": "unknown",
        "current_post": "喀左县政协领导",
        "current_org": "喀喇沁左翼蒙古族自治县政协",
        "source": "https://www.kazuo.gov.cn/html/KZXZF/202607/0178484756629882.html"
    },
    {
        "id": 21, "name": "许春宇", "gender": "男", "ethnicity": "unknown",
        "birth": "unknown", "birthplace": "unknown", "education": "unknown",
        "party_join": "中共党员", "work_start": "unknown",
        "current_post": "喀左县政协领导",
        "current_org": "喀喇沁左翼蒙古族自治县政协",
        "source": "https://www.kazuo.gov.cn/html/KZXZF/202607/0178484756629882.html"
    },
]

organizations = [
    {"id": 1, "name": "中共喀喇沁左翼蒙古族自治县委员会", "type": "党委", "level": "县级", "parent": "中共朝阳市委", "location": "辽宁省朝阳市喀左县"},
    {"id": 2, "name": "喀喇沁左翼蒙古族自治县人民政府", "type": "政府", "level": "县级", "parent": "朝阳市人民政府", "location": "辽宁省朝阳市喀左县"},
    {"id": 3, "name": "朝阳喀左经济开发区", "type": "开发区", "level": "省级", "parent": "喀喇沁左翼蒙古族自治县人民政府", "location": "辽宁省朝阳市喀左县"},
    {"id": 4, "name": "喀喇沁左翼蒙古族自治县人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "辽宁省朝阳市喀左县"},
    {"id": 5, "name": "喀喇沁左翼蒙古族自治县政协", "type": "政协", "level": "县级", "parent": "", "location": "辽宁省朝阳市喀左县"},
]

positions = [
    # 杨春柏
    {"person_id": 1, "org_id": 1, "title": "中共喀喇沁左翼蒙古族自治县委书记", "start": "unknown", "end": "present", "rank": "正处级", "note": "截至2026年7月在职"},
    # 韩健
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "unknown", "end": "present", "rank": "正处级", "note": "县委副书记、县政府党组书记"},
    {"person_id": 2, "org_id": 3, "title": "朝阳喀左经济开发区党工委书记（兼）", "start": "unknown", "end": "present", "rank": "正处级", "note": ""},
    # 徐广强
    {"person_id": 3, "org_id": 2, "title": "常务副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "县委常委、县政府党组副书记"},
    # 于涛
    {"person_id": 4, "org_id": 3, "title": "朝阳喀左经济开发区管委会主任", "start": "unknown", "end": "present", "rank": "副处级", "note": "经开区党工委副书记"},
    # 房家阳
    {"person_id": 5, "org_id": 2, "title": "县委常委、副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # 刘秀娟
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "三级调研员"},
    # 张晶
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # 王德文
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # 钱文涛
    {"person_id": 9, "org_id": 2, "title": "副县长、县公安局局长", "start": "unknown", "end": "present", "rank": "副处级", "note": "一级警长"},
    # 王崇东
    {"person_id": 10, "org_id": 2, "title": "县政府党组成员", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # 姜岱盛
    {"person_id": 11, "org_id": 2, "title": "四级调研员、副处级干部", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # 杨朝辉
    {"person_id": 12, "org_id": 1, "title": "县委领导（疑似副书记）", "start": "unknown", "end": "present", "rank": "副处级", "note": "主持县第十六次党代会预备会议"},
    # 宋永波
    {"person_id": 13, "org_id": 1, "title": "县委领导", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # 李海源
    {"person_id": 14, "org_id": 1, "title": "县委领导", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # 刘东涛
    {"person_id": 15, "org_id": 1, "title": "县委领导", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # 陈天虹
    {"person_id": 16, "org_id": 1, "title": "县委领导", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # 谢育
    {"person_id": 17, "org_id": 1, "title": "县委领导", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # 遇长波
    {"person_id": 18, "org_id": 1, "title": "县委领导", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # 马贤军
    {"person_id": 19, "org_id": 4, "title": "县人大常委会领导", "start": "unknown", "end": "present", "rank": "正处级", "note": ""},
    # 赵升龙
    {"person_id": 20, "org_id": 5, "title": "县政协领导", "start": "unknown", "end": "present", "rank": "正处级", "note": ""},
    # 许春宇
    {"person_id": 21, "org_id": 5, "title": "县政协领导", "start": "unknown", "end": "present", "rank": "正处级", "note": ""},
]

relationships = [
    # 书记↔县长
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "杨春柏（县委书记）与韩健（县长）为党政主要领导搭档", "overlap_org": "中共喀左县委/县政府", "overlap_period": "未知至今", "confidence": "confirmed"},
    # 党政领导与县政府班子成员
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记与常务副县长", "overlap_org": "喀左县委/县政府", "overlap_period": "未知至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "县长与常务副县长（协助县长工作）", "overlap_org": "喀左县政府", "overlap_period": "未知至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "县委书记与县委常委、副县长", "overlap_org": "喀左县委", "overlap_period": "未知至今", "confidence": "confirmed"},
    # 政府班子成员间
    {"person_a": 3, "person_b": 5, "type": "同事", "context": "同为县政府副县长，房家阳为县委常委", "overlap_org": "喀左县政府", "overlap_period": "未知至今", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 6, "type": "同事", "context": "常务副县长与副县长", "overlap_org": "喀左县政府", "overlap_period": "未知至今", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 7, "type": "同事", "context": "常务副县长与副县长", "overlap_org": "喀左县政府", "overlap_period": "未知至今", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 8, "type": "同事", "context": "常务副县长与副县长", "overlap_org": "喀左县政府", "overlap_period": "未知至今", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 9, "type": "同事", "context": "常务副县长与副县长（公安局长）", "overlap_org": "喀左县政府", "overlap_period": "未知至今", "confidence": "confirmed"},
    # 县委班子成员间
    {"person_a": 1, "person_b": 12, "type": "同事", "context": "县委书记与县委副书记/领导", "overlap_org": "喀左县委", "overlap_period": "未知至今", "confidence": "plausible"},
    {"person_a": 1, "person_b": 13, "type": "同事", "context": "县委书记与县委领导", "overlap_org": "喀左县委", "overlap_period": "未知至今", "confidence": "plausible"},
    {"person_a": 1, "person_b": 14, "type": "同事", "context": "县委书记与县委领导", "overlap_org": "喀左县委", "overlap_period": "未知至今", "confidence": "plausible"},
    # 人大和政协
    {"person_a": 1, "person_b": 19, "type": "党政人大", "context": "县委书记与县人大领导", "overlap_org": "喀左县", "overlap_period": "未知至今", "confidence": "plausible"},
    {"person_a": 2, "person_b": 19, "type": "党政人大", "context": "县长与县人大领导", "overlap_org": "喀左县", "overlap_period": "未知至今", "confidence": "plausible"},
    {"person_a": 1, "person_b": 20, "type": "党政政协", "context": "县委书记与县政协领导", "overlap_org": "喀左县", "overlap_period": "未知至今", "confidence": "plausible"},
]


# ── HELPERS ──────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return 'r,g,b' string based on role."""
    post = p.get("current_post", "")
    if "书记" in post and "县委" in post:
        return "255,50,50"  # Red - Party Secretary
    if any(t in post for t in ["县长", "副县长", "区长"]):
        return "50,100,255"  # Blue - Government
    if "纪委" in post or "监委" in post:
        return "255,165,0"   # Orange - Discipline
    if "人大" in post:
        return "200,255,255"  # Cyan
    if "政协" in post:
        return "255,240,200"  # Cream
    return "100,100,100"  # Grey - other


def is_top_leader(p):
    return p["id"] in [1, 2]  # 书记 and 县长


# ── BUILD FUNCTIONS ──────────────────────────────────────────────────

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"],
             r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()

    print(f"Database created: {DB_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append('    <description>喀喇沁左翼蒙古族自治县 leadership network - Party, Government, and associated organizations</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="organization" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="ethnicity" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth", ""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("ethnicity", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        org_colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "开发区": "200,255,200",
            "人大": "200,255,255",
            "政协": "255,240,200",
        }
        oc = org_colors.get(o["type"], "200,200,200")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append(f'          <attvalue for="4" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # person → organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person ↔ person (relationship)
    for r in relationships:
        eid += 1
        weight = "2.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"GEXF graph created: {GEXF_PATH}")
    print(f"  Edges: {eid}")


def main():
    print("=" * 60)
    print("喀喇沁左翼蒙古族自治县 Leadership Network Builder")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    print("=" * 60)
    build_db()
    build_gexf()
    print("=" * 60)
    print("Build complete!")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    main()
