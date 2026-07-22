#!/usr/bin/env python3
"""
云浮市云城区领导班子工作关系网络 — 数据构建脚本

生成:
  - data/database/云城区_network.db
  - data/graph/云城区_network.gexf

数据来源:
  - 云城区人民政府门户网站领导之窗 (2026-07-22)
    http://www.yfyunchengqu.gov.cn/ycqrmzf/ldbz/index.html
  - 各领导个人页面 (2026-07-22)
"""

import os
import sqlite3
import sys
from datetime import datetime

# ── 路径 ──────────────────────────────────────────────────────────────
TMP = "data/tmp/guangdong_云城区"
DB_PATH = os.path.join(TMP, "云城区_network.db")
GEXF_PATH = os.path.join(TMP, "云城区_network.gexf")


# ── 数据 ──────────────────────────────────────────────────────────────

persons = [
    {
        "id": 1,
        "name": "叶伟光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-11",
        "birthplace": "",
        "education": "中央党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "中共云城区委书记",
        "current_org": "中共云城区委员会",
        "source": "http://www.yfyunchengqu.gov.cn/ycqrmzf/ldbz/qwldbz/qwsj/content/post_1616846.html",
    },
    {
        "id": 2,
        "name": "陈晓周",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-09",
        "birthplace": "广东揭西",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "1995-07",
        "current_post": "云城区委副书记、区长",
        "current_org": "云城区人民政府",
        "source": "http://www.yfyunchengqu.gov.cn/ycqrmzf/ldbz/qwldbz/qwfsj/content/post_449.html",
    },
    {
        "id": 3,
        "name": "邓世民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-01",
        "birthplace": "",
        "education": "农业推广硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、政法委书记",
        "current_org": "中共云城区委员会",
        "source": "http://www.yfyunchengqu.gov.cn/ycqrmzf/ldbz/qwldbz/qwfsj/content/post_1787099.html",
    },
    {
        "id": 4,
        "name": "利学时",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共云城区委员会",
        "source": "http://www.yfyunchengqu.gov.cn/ycqrmzf/ldbz/index.html",
    },
    {
        "id": 5,
        "name": "林燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976-01",
        "birthplace": "广东罗定",
        "education": "在职大专、农业推广硕士",
        "party_join": "2004-12",
        "work_start": "2003-01",
        "current_post": "区委常委、统战部部长",
        "current_org": "中共云城区委员会",
        "source": "http://www.yfyunchengqu.gov.cn/ycqrmzf/ldbz/qwldbz/qwcw/content/post_1413800.html",
    },
    {
        "id": 6,
        "name": "朱必波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "云城区人民政府",
        "source": "http://www.yfyunchengqu.gov.cn/ycqrmzf/ldbz/index.html",
    },
    {
        "id": 7,
        "name": "宋正伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共云城区委员会",
        "source": "http://www.yfyunchengqu.gov.cn/ycqrmzf/ldbz/index.html",
    },
    {
        "id": 8,
        "name": "陈作宏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共云城区委员会",
        "source": "http://www.yfyunchengqu.gov.cn/ycqrmzf/ldbz/index.html",
    },
    {
        "id": 9,
        "name": "甘树兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共云城区委员会",
        "source": "http://www.yfyunchengqu.gov.cn/ycqrmzf/ldbz/index.html",
    },
    {
        "id": 10,
        "name": "陈友泉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共云城区委员会",
        "source": "http://www.yfyunchengqu.gov.cn/ycqrmzf/ldbz/index.html",
    },
    {
        "id": 11,
        "name": "彭庆林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共云城区委员会",
        "source": "http://www.yfyunchengqu.gov.cn/ycqrmzf/ldbz/index.html",
    },
    {
        "id": 12,
        "name": "尹章生",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共云城区委员会",
        "source": "http://www.yfyunchengqu.gov.cn/ycqrmzf/ldbz/index.html",
    },
    {
        "id": 13,
        "name": "邓腾芳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "云城区人民政府",
        "source": "http://www.yfyunchengqu.gov.cn/ycqrmzf/ldbz/index.html",
    },
    {
        "id": 14,
        "name": "冯桂聪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "云城区人民政府",
        "source": "http://www.yfyunchengqu.gov.cn/ycqrmzf/ldbz/index.html",
    },
    {
        "id": 15,
        "name": "谭捷",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "云城区人民政府",
        "source": "http://www.yfyunchengqu.gov.cn/ycqrmzf/ldbz/index.html",
    },
    {
        "id": 16,
        "name": "祝传伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "云城区人民政府",
        "source": "http://www.yfyunchengqu.gov.cn/ycqrmzf/ldbz/index.html",
    },
    {
        "id": 17,
        "name": "王木强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "云城区人大常委会",
        "source": "http://www.yfyunchengqu.gov.cn/ycqrmzf/ldbz/index.html",
    },
    {
        "id": 18,
        "name": "李润",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "云城区政协",
        "source": "http://www.yfyunchengqu.gov.cn/ycqrmzf/ldbz/index.html",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共云城区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共云浮市委员会",
        "location": "广东省云浮市云城区",
    },
    {
        "id": 2,
        "name": "云城区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "云浮市人民政府",
        "location": "广东省云浮市云城区",
    },
    {
        "id": 3,
        "name": "云城区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "云浮市人大常委会",
        "location": "广东省云浮市云城区",
    },
    {
        "id": 4,
        "name": "云城区政协",
        "type": "政协",
        "level": "县处级",
        "parent": "政协云浮市委员会",
        "location": "广东省云浮市云城区",
    },
    {
        "id": 5,
        "name": "云城区委统战部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共云城区委员会",
        "location": "广东省云浮市云城区",
    },
    {
        "id": 6,
        "name": "云城区委政法委",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共云城区委员会",
        "location": "广东省云浮市云城区",
    },
    {
        "id": 7,
        "name": "云城区纪委监委",
        "type": "纪律检查",
        "level": "县处级",
        "parent": "中共云城区委员会",
        "location": "广东省云浮市云城区",
    },
    {
        "id": 8,
        "name": "云城街道办事处",
        "type": "乡镇/街道",
        "level": "乡科级",
        "parent": "云城区人民政府",
        "location": "广东省云浮市云城区",
    },
]

positions = [
    # 叶伟光
    {"person_id": 1, "org_id": 1, "title": "中共云城区委书记", "start": "", "end": "present", "rank": "正处级", "note": "主持区委全面工作"},
    # 陈晓周
    {"person_id": 2, "org_id": 2, "title": "云城区区长", "start": "", "end": "present", "rank": "正处级", "note": "主持区政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "云城区委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 邓世民
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 6, "title": "区委政法委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 8, "title": "云城街道党工委书记", "start": "", "end": "present", "rank": "正科级", "note": ""},
    # 利学时
    {"person_id": 4, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 林燕
    {"person_id": 5, "org_id": 5, "title": "区委常委、统战部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 朱必波
    {"person_id": 6, "org_id": 2, "title": "区委常委、副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 宋正伟
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 陈作宏
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 甘树兵
    {"person_id": 9, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 陈友泉
    {"person_id": 10, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 彭庆林
    {"person_id": 11, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 尹章生
    {"person_id": 12, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 邓腾芳
    {"person_id": 13, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 冯桂聪
    {"person_id": 14, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 谭捷
    {"person_id": 15, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 祝传伟
    {"person_id": 16, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 王木强
    {"person_id": 17, "org_id": 3, "title": "区人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 李润
    {"person_id": 18, "org_id": 4, "title": "区政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
]

relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "叶伟光（区委书记）与陈晓周（区长）为云城区现任党政一把手", "overlap_org": "中共云城区委员会/云城区人民政府", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 区委书记与区委副书记
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "叶伟光与邓世民（副书记、政法委书记）", "overlap_org": "中共云城区委员会", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "叶伟光与利学时（副书记）", "overlap_org": "中共云城区委员会", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 区委书记与常委
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "叶伟光与林燕（常委、统战部长）", "overlap_org": "中共云城区委员会", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "叶伟光与朱必波（常委、副区长）", "overlap_org": "中共云城区委员会", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "叶伟光与宋正伟（常委）", "overlap_org": "中共云城区委员会", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "叶伟光与陈作宏（常委）", "overlap_org": "中共云城区委员会", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "叶伟光与甘树兵（常委）", "overlap_org": "中共云城区委员会", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "叶伟光与陈友泉（常委）", "overlap_org": "中共云城区委员会", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "叶伟光与彭庆林（常委）", "overlap_org": "中共云城区委员会", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 12, "type": "上下级", "context": "叶伟光与尹章生（常委）", "overlap_org": "中共云城区委员会", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    # 区长与副区长
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "陈晓周与朱必波（常务副区长）", "overlap_org": "云城区人民政府", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "陈晓周与邓腾芳（副区长）", "overlap_org": "云城区人民政府", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "陈晓周与冯桂聪（副区长）", "overlap_org": "云城区人民政府", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 15, "type": "上下级", "context": "陈晓周与谭捷（副区长）", "overlap_org": "云城区人民政府", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 16, "type": "上下级", "context": "陈晓周与祝传伟（副区长）", "overlap_org": "云城区人民政府", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    # 副书记之间
    {"person_a": 3, "person_b": 4, "type": "同级", "context": "邓世民与利学时（均为区委副书记）", "overlap_org": "中共云城区委员会", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    # 人大/政协与区委
    {"person_a": 1, "person_b": 17, "type": "协同", "context": "区委书记与区人大常委会主任", "overlap_org": "云城区", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 18, "type": "协同", "context": "区委书记与区政协主席", "overlap_org": "云城区", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
]


# ── BUILD FUNCTIONS ──────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_db():
    """Create SQLite database with all data."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
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
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
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
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            strength TEXT,
            confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"], r["strength"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"  DB written: {DB_PATH}")
    print(f"  Persons: {len(persons)}, Orgs: {len(organizations)}, Positions: {len(positions)}, Relationships: {len(relationships)}")


def person_color(p):
    """Return 'r,g,b' color string based on role."""
    post = p.get("current_post", "")
    if "书记" in post and "副" not in post and "总" not in post:
        return "255,50,50"
    elif ("区长" in post or "县长" in post or "市长" in post) and "副" not in post:
        return "50,100,255"
    elif "副书记" in post:
        return "150,50,255"
    elif "常委" in post:
        return "100,100,255"
    elif "主任" in post or "主席" in post:
        return "100,100,100"
    else:
        return "100,100,100"


def org_color(o):
    """Return 'r,g,b' color string for organization type."""
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "纪律检查": "255,220,200",
        "乡镇/街道": "255,255,200",
    }
    return colors.get(o.get("type", ""), "200,200,200")


def is_top_leader(p):
    """Check if person is a top leader (party secretary or mayor)."""
    post = p.get("current_post", "")
    return ("书记" in post and "副" not in post and "总" not in post) or \
           (("区长" in post or "县长" in post or "市长" in post) and "副" not in post)


def build_gexf():
    """Generate GEXF graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append('    <description>云城区领导班子工作关系网络 — 包含区委领导、区政府领导、区人大、区政协及其相互关系</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('      <attribute id="3" title="level" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="strength" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
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
        lines.append(f'          <attvalue for="2" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(o.get("level", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('          <attvalue for="1" value="1.0"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in relationships:
        eid += 1
        w = "2.0" if r.get("strength") == "strong" else "1.5"
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r.get("type", ""))}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("strength", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("confidence", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {GEXF_PATH}")
    print(f"  Person nodes: {len(persons)}, Org nodes: {len(organizations)}, Edges: {eid}")


def main():
    print("Building 云城区 leadership network...")
    os.makedirs(TMP, exist_ok=True)
    build_db()
    build_gexf()
    print("Done.")

    # Summary
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM persons")
    print(f"  Total persons in DB: {c.fetchone()[0]}")
    c.execute("SELECT COUNT(*) FROM organizations")
    print(f"  Total organizations in DB: {c.fetchone()[0]}")
    c.execute("SELECT COUNT(*) FROM positions")
    print(f"  Total positions in DB: {c.fetchone()[0]}")
    c.execute("SELECT COUNT(*) FROM relationships")
    print(f"  Total relationships in DB: {c.fetchone()[0]}")
    conn.close()


if __name__ == "__main__":
    main()
