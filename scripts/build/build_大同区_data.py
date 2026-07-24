#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 大同区 (Datong District), 大庆市, 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_大同区
Research sources:
  - Datong District Government Website (www.dqdt.gov.cn)
  - Government leadership page (领导组织)
  - News reports and inspection articles
"""

import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "大同区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = TODAY

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

SLUG = "大同区"

# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════════
    # Core Leadership (区委书记 & 区长)
    # ══════════════════════════════════════════════════════════════════════════

    # 诸葛祥龙 — 区委书记 (as of July 2026)
    # Born 1982, 浙江大学构造地质专业研究生学历硕士学位,
    # 曾任大庆油田储气库分公司经理,
    # 2021.11 任大同区委副书记、代区长,
    # 2021.12 当选大同区区长,
    # 2024.12 任大同区委书记
    {"id": 1, "name": "诸葛祥龙", "gender": "男", "ethnicity": "",
     "birth": "1982年", "birthplace": "", "education": "浙江大学构造地质专业，研究生学历，硕士学位",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委书记", "current_org": "中共大庆市大同区委员会",
     "source": "http://www.dqdt.gov.cn/datong/zgqwsj/202212/c05_102059.shtml"},

    # 李文章 — 区长、区委副书记 (as of July 2026)
    # 此前曾任萨尔图区委常委、副区长
    {"id": 2, "name": "李文章", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区长", "current_org": "大庆市大同区人民政府",
     "source": "http://www.dqdt.gov.cn/datong/qzfqz/202602/c05_403283.shtml"},

    # ══════════════════════════════════════════════════════════════════════════
    # District Party Standing Committee (区委常委)
    # ══════════════════════════════════════════════════════════════════════════

    # 马强 — 区委副书记
    {"id": 3, "name": "马强", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委副书记", "current_org": "中共大庆市大同区委员会",
     "source": "http://www.dqdt.gov.cn/datong/zgqwfsj/202510/c05_102062.shtml"},

    # 徐海芳 — 区委常委、组织部部长
    {"id": 4, "name": "徐海芳", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、组织部部长", "current_org": "中共大庆市大同区委员会",
     "source": "http://www.dqdt.gov.cn/datong/zgqwcw/202510/c05_102063.shtml"},

    # 李元光 — 区委常委、宣传部部长、统战部部长
    {"id": 5, "name": "李元光", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、宣传部部长、统战部部长", "current_org": "中共大庆市大同区委员会",
     "source": "http://www.dqdt.gov.cn/datong/zgqwcw/202510/c05_102067.shtml"},

    # 张宝春 — 区委常委、副区长
    {"id": 6, "name": "张宝春", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、副区长", "current_org": "大庆市大同区人民政府",
     "source": "http://www.dqdt.gov.cn/datong/zgqwcw/202412/c05_365062.shtml"},

    # 饶利侠 — 区委常委、纪委书记、监委主任
    {"id": 7, "name": "饶利侠", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、纪委书记、监委主任", "current_org": "中共大庆市大同区纪律检查委员会",
     "source": "http://www.dqdt.gov.cn/datong/zgqwcw/202510/c05_392194.shtml"},

    # 张国辉 — 区委常委、武装部政治委员
    {"id": 8, "name": "张国辉", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、武装部政治委员", "current_org": "大庆市大同区人民武装部",
     "source": "http://www.dqdt.gov.cn/datong/zgqwcw/202510/c05_102065.shtml"},

    # ══════════════════════════════════════════════════════════════════════════
    # Deputy Mayors (副区长)
    # ══════════════════════════════════════════════════════════════════════════

    # 高振波 — 副区长、大同公安分局局长
    {"id": 9, "name": "高振波", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副区长、大同公安分局局长", "current_org": "大庆市大同区人民政府",
     "source": "http://www.dqdt.gov.cn/datong/qzffqz/202305/c05_281653.shtml"},

    # 郑立国 — 副区长
    {"id": 10, "name": "郑立国", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副区长", "current_org": "大庆市大同区人民政府",
     "source": "http://www.dqdt.gov.cn/datong/qzffqz/202412/c05_365064.shtml"},

    # 魏玉峰 — 副区长
    {"id": 11, "name": "魏玉峰", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副区长", "current_org": "大庆市大同区人民政府",
     "source": "http://www.dqdt.gov.cn/datong/qzffqz/202510/c05_392197.shtml"},

    # ══════════════════════════════════════════════════════════════════════════
    # 人大 & 政协 Leaders
    # ══════════════════════════════════════════════════════════════════════════

    # 孙有斌 — 区人大常委会主任
    {"id": 12, "name": "孙有斌", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区人大常委会主任", "current_org": "大庆市大同区人大常委会",
     "source": "http://www.dqdt.gov.cn/datong/qrdzr/202510/c05_102072.shtml"},

    # 吕国信 — 区政协主席
    {"id": 13, "name": "吕国信", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区政协主席", "current_org": "政协大庆市大同区委员会",
     "source": "http://www.dqdt.gov.cn/datong/qzxzx/202510/c05_102080.shtml"},
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共大庆市大同区委员会", "type": "党委", "level": "县处级", "parent": "中共大庆市委员会", "location": "黑龙江省大庆市大同区"},
    {"id": 2, "name": "大庆市大同区人民政府", "type": "政府", "level": "县处级", "parent": "大庆市人民政府", "location": "黑龙江省大庆市大同区"},
    {"id": 3, "name": "中共大庆市大同区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共大庆市大同区委员会", "location": "黑龙江省大庆市大同区"},
    {"id": 4, "name": "大庆市大同区人大常委会", "type": "人大", "level": "县处级", "parent": "大庆市大同区", "location": "黑龙江省大庆市大同区"},
    {"id": 5, "name": "政协大庆市大同区委员会", "type": "政协", "level": "县处级", "parent": "大庆市大同区", "location": "黑龙江省大庆市大同区"},
    {"id": 6, "name": "大庆市公安局大同分局", "type": "政府", "level": "乡科级", "parent": "大庆市大同区人民政府", "location": "黑龙江省大庆市大同区"},
    {"id": 7, "name": "大庆市大同区人民武装部", "type": "政府", "level": "乡科级", "parent": "大庆军分区", "location": "黑龙江省大庆市大同区"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 诸葛祥龙 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "大同区委书记", "start": "2024-12", "end": "", "rank": "县处级正职", "note": "2024年12月由区长升任区委书记；此前曾任大庆油田储气库分公司经理"},
    {"person_id": 1, "org_id": 2, "title": "大同区区长（原任）", "start": "2021-11", "end": "2024-12", "rank": "县处级正职", "note": "2021年11月任代区长，12月当选区长；2024年12月升任区委书记"},
    {"person_id": 1, "org_id": 1, "title": "大同区委副书记（原任）", "start": "2021-11", "end": "2024-12", "rank": "县处级副职", "note": ""},

    # 李文章 — 区长
    {"person_id": 2, "org_id": 2, "title": "大同区区长", "start": "", "end": "", "rank": "县处级正职", "note": "此前曾任萨尔图区委常委、副区长（待确认具体到任大同区时间）"},
    {"person_id": 2, "org_id": 1, "title": "大同区委副书记", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 马强 — 专职副书记
    {"person_id": 3, "org_id": 1, "title": "大同区委副书记", "start": "", "end": "", "rank": "县处级副职", "note": "专职副书记"},

    # 徐海芳
    {"person_id": 4, "org_id": 1, "title": "大同区委常委、组织部部长", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 李元光
    {"person_id": 5, "org_id": 1, "title": "大同区委常委、宣传部部长、统战部部长", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 张宝春
    {"person_id": 6, "org_id": 1, "title": "大同区委常委", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "大同区副区长", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 饶利侠
    {"person_id": 7, "org_id": 3, "title": "大同区纪委书记、监委主任", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "大同区委常委", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 张国辉
    {"person_id": 8, "org_id": 7, "title": "大同区武装部政治委员", "start": "", "end": "", "rank": "正团级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "大同区委常委", "start": "", "end": "", "rank": "县处级副职", "note": "武装部政委兼任区委常委"},

    # 高振波
    {"person_id": 9, "org_id": 2, "title": "大同区副区长", "start": "", "end": "", "rank": "县处级副职", "note": "分管公安、司法、信访等工作"},
    {"person_id": 9, "org_id": 6, "title": "大同公安分局局长", "start": "", "end": "", "rank": "乡科级正职", "note": ""},

    # 郑立国
    {"person_id": 10, "org_id": 2, "title": "大同区副区长", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 魏玉峰
    {"person_id": 11, "org_id": 2, "title": "大同区副区长", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 孙有斌
    {"person_id": 12, "org_id": 4, "title": "大同区人大常委会主任", "start": "", "end": "", "rank": "县处级正职", "note": ""},

    # 吕国信
    {"person_id": 13, "org_id": 5, "title": "大同区政协主席", "start": "", "end": "", "rank": "县处级正职", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────────────

relationships = [
    # 诸葛祥龙 — 李文章：党政搭档
    {"person_a": 1, "person_b": 2, "type": "党政同僚", "context": "区委书记与区长党政工作搭档", "overlap_org": "大同区", "overlap_period": ""},

    # 诸葛祥龙 — 马强：书记与专职副书记
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记与专职副书记", "overlap_org": "中共大同区委", "overlap_period": ""},

    # 诸葛祥龙 — 各常委：书记与常委
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记与组织部部长", "overlap_org": "中共大同区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记与宣传部部长", "overlap_org": "中共大同区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区委书记与副区长", "overlap_org": "中共大同区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "区委书记与纪委书记", "overlap_org": "中共大同区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "区委书记与武装部政委", "overlap_org": "中共大同区委", "overlap_period": ""},

    # 李文章 — 各副区长：区长与副职
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "区长与副区长", "overlap_org": "大同区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "区长与副区长、公安分局局长", "overlap_org": "大同区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "区长与副区长", "overlap_org": "大同区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "区长与副区长", "overlap_org": "大同区人民政府", "overlap_period": ""},

    # 李文章 — 马强：区长与专职副书记
    {"person_a": 2, "person_b": 3, "type": "同僚", "context": "区长与区委副书记党政同僚", "overlap_org": "中共大同区委", "overlap_period": ""},

    # 区委常委之间：同僚
    {"person_a": 3, "person_b": 4, "type": "同僚", "context": "区委常委", "overlap_org": "中共大同区委", "overlap_period": ""},
    {"person_a": 3, "person_b": 5, "type": "同僚", "context": "区委常委", "overlap_org": "中共大同区委", "overlap_period": ""},
    {"person_a": 3, "person_b": 6, "type": "同僚", "context": "区委常委", "overlap_org": "中共大同区委", "overlap_period": ""},
    {"person_a": 3, "person_b": 7, "type": "同僚", "context": "区委常委", "overlap_org": "中共大同区委", "overlap_period": ""},
    {"person_a": 3, "person_b": 8, "type": "同僚", "context": "区委常委", "overlap_org": "中共大同区委", "overlap_period": ""},
    {"person_a": 4, "person_b": 5, "type": "同僚", "context": "区委常委", "overlap_org": "中共大同区委", "overlap_period": ""},
    {"person_a": 4, "person_b": 6, "type": "同僚", "context": "区委常委", "overlap_org": "中共大同区委", "overlap_period": ""},
    {"person_a": 4, "person_b": 7, "type": "同僚", "context": "区委常委", "overlap_org": "中共大同区委", "overlap_period": ""},
    {"person_a": 4, "person_b": 8, "type": "同僚", "context": "区委常委", "overlap_org": "中共大同区委", "overlap_period": ""},
    {"person_a": 5, "person_b": 6, "type": "同僚", "context": "区委常委", "overlap_org": "中共大同区委", "overlap_period": ""},
    {"person_a": 5, "person_b": 7, "type": "同僚", "context": "区委常委", "overlap_org": "中共大同区委", "overlap_period": ""},
    {"person_a": 5, "person_b": 8, "type": "同僚", "context": "区委常委", "overlap_org": "中共大同区委", "overlap_period": ""},
    {"person_a": 6, "person_b": 7, "type": "同僚", "context": "区委常委", "overlap_org": "中共大同区委", "overlap_period": ""},
    {"person_a": 6, "person_b": 8, "type": "同僚", "context": "区委常委", "overlap_org": "中共大同区委", "overlap_period": ""},
    {"person_a": 7, "person_b": 8, "type": "同僚", "context": "区委常委", "overlap_org": "中共大同区委", "overlap_period": ""},

    # 张宝春 — 其他副区长（同为副区长）
    {"person_a": 6, "person_b": 9, "type": "同僚", "context": "副区长同僚", "overlap_org": "大同区人民政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 10, "type": "同僚", "context": "副区长同僚", "overlap_org": "大同区人民政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 11, "type": "同僚", "context": "副区长同僚", "overlap_org": "大同区人民政府", "overlap_period": ""},
    {"person_a": 9, "person_b": 10, "type": "同僚", "context": "副区长同僚", "overlap_org": "大同区人民政府", "overlap_period": ""},
    {"person_a": 9, "person_b": 11, "type": "同僚", "context": "副区长同僚", "overlap_org": "大同区人民政府", "overlap_period": ""},
    {"person_a": 10, "person_b": 11, "type": "同僚", "context": "副区长同僚", "overlap_org": "大同区人民政府", "overlap_period": ""},

    # 人大 & 政协 与主要领导
    {"person_a": 1, "person_b": 12, "type": "同僚", "context": "区委书记与人大主任", "overlap_org": "大同区", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "同僚", "context": "区长与人大主任", "overlap_org": "大同区", "overlap_period": ""},
    {"person_a": 1, "person_b": 13, "type": "同僚", "context": "区委书记与政协主席", "overlap_org": "大同区", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "同僚", "context": "区长与政协主席", "overlap_org": "大同区", "overlap_period": ""},
]


# ══════════════════════════════════════════════════════════════════════════════
# SQLite DB Builder
# ══════════════════════════════════════════════════════════════════════════════

esc = lambda s: str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;") if s is not None else ""

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Drop existing tables
    for t in ("relationships","positions","organizations","persons"):
        cur.execute(f"DROP TABLE IF EXISTS {t}")
    
    # Create tables
    cur.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    cur.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    cur.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER,
        title TEXT, start_date TEXT, end_date TEXT,
        rank TEXT, note TEXT
    )""")
    cur.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT
    )""")
    
    for p in persons:
        cur.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],
                     p["birthplace"],p["education"],p["party_join"],p["work_start"],
                     p["current_post"],p["current_org"],p["source"]))
    for o in organizations:
        cur.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                    (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
    for pos in positions:
        cur.execute("INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)",
                    (pos["person_id"],pos["org_id"],pos["title"],pos.get("start",""),pos.get("end",""),pos.get("rank",""),pos.get("note","")))
    for r in relationships:
        cur.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                    (r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))
    
    conn.commit()
    conn.close()
    print(f"  DB: {DB_PATH} ({len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships)")


# ══════════════════════════════════════════════════════════════════════════════
# GEXF Graph Builder
# ══════════════════════════════════════════════════════════════════════════════

def person_color(post):
    if "书记" in post and "副" not in post and "纪委" not in post:
        return ("255,50,50", 20.0)  # Red, large = party secretary
    elif "区长" in post and "副" not in post:
        return ("50,100,255", 20.0)  # Blue, large = government head
    elif "副" in post and ("区长" in post or "书记" in post):
        return ("100,150,255", 12.0)  # Light blue
    elif "常委" in post:
        return ("100,150,255", 12.0)
    elif "人大" in post or "主任" in post:
        return ("200,255,255", 12.0)  # Cyan
    elif "政协" in post or "主席" in post:
        return ("255,240,200", 12.0)  # Cream
    elif "纪委" in post or "监委" in post:
        return ("255,165,0", 12.0)  # Orange
    else:
        return ("100,100,100", 12.0)

def org_color(org_type):
    colors = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "纪委": ("255,200,200", 8.0),
        "人大": ("200,255,255", 8.0),
        "政协": ("255,240,200", 8.0),
    }
    return colors.get(org_type, ("200,200,200", 8.0))


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append(f'    <description>大同区领导班子关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    
    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')
    
    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')
    
    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c, sz = person_color(p["current_post"])
        lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # Organization nodes
    for o in organizations:
        c, sz = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    
    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person -> Organization (worked at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    # Person <-> Person (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="{r["person_a"]}" target="{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    
    lines.append('  </graph>')
    lines.append('</gexf>')
    
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH}")


# ══════════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════════

def make_source_register():
    return [
        {"id":"S001","title":"大同区政府—领导组织·区委书记页","url":"http://www.dqdt.gov.cn/datong/zgqwsj/202212/c05_102059.shtml","publisher":"大庆市大同区人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"诸葛祥龙，中共大同区委书记"},
        {"id":"S002","title":"大同区政府—领导组织·区长页","url":"http://www.dqdt.gov.cn/datong/qzfqz/202602/c05_403283.shtml","publisher":"大庆市大同区人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"李文章，中共大同区委副书记、区人民政府区长"},
        {"id":"S003","title":"大同区政府—领导组织·副书记页","url":"http://www.dqdt.gov.cn/datong/zgqwfsj/202602/c05_403284.shtml","publisher":"大庆市大同区人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"李文章（区长页同步确认）"},
        {"id":"S004","title":"大同区政府—领导组织总页","url":"http://www.dqdt.gov.cn/datong/ldzz/open_lingdao.shtml","publisher":"大庆市大同区人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"完整领导班子名单及链接"},
        {"id":"S005","title":"区委书记诸葛祥龙作专题党课辅导","url":"http://www.dqdt.gov.cn/datong/zwyw/202607/c05_415127.shtml","publisher":"大庆市大同区人民政府","published_at":"2026-07-01","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"报道确认诸葛祥龙以区委书记身份出席活动"},
        {"id":"S006","title":"李文章调研企业运营生产情况","url":"http://www.dqdt.gov.cn/datong/zwyw/202606/c05_414672.shtml","publisher":"大庆市大同区人民政府","published_at":"2026-06-28","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"确认李文章以区委副书记、区长身份调研"},
        {"id":"S007","title":"大同区委十一届第109次常委会会议","url":"http://www.dqdt.gov.cn/datong/zwyw/202607/c05_416441.shtml","publisher":"大庆市大同区人民政府","published_at":"2026-07-18","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"诸葛祥龙主持会议"},
        {"id":"S008","title":"智能高端节能输变电设备项目签约","url":"http://www.dqdt.gov.cn/datong/zwyw/202607/c05_415702.shtml","publisher":"大庆市大同区人民政府","published_at":"2026-07-09","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"诸葛祥龙、李文章共同出席签约仪式"},
        {"id":"S009","title":"大同区政府—徐海芳常委页","url":"http://www.dqdt.gov.cn/datong/zgqwcw/202510/c05_102063.shtml","publisher":"大庆市大同区人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"徐海芳，区委常委、组织部部长"},
        {"id":"S010","title":"大同区政府—李元光常委页","url":"http://www.dqdt.gov.cn/datong/zgqwcw/202510/c05_102067.shtml","publisher":"大庆市大同区人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"李元光，区委常委、宣传部部长、统战部部长"},
        {"id":"S011","title":"大同区政府—张宝春常委页","url":"http://www.dqdt.gov.cn/datong/zgqwcw/202412/c05_365062.shtml","publisher":"大庆市大同区人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"张宝春，区委常委、副区长"},
        {"id":"S012","title":"大同区政府—饶利侠常委页","url":"http://www.dqdt.gov.cn/datong/zgqwcw/202510/c05_392194.shtml","publisher":"大庆市大同区人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"饶利侠，区委常委、纪委书记、监委主任"},
        {"id":"S013","title":"大同区政府—张国辉常委页","url":"http://www.dqdt.gov.cn/datong/zgqwcw/202510/c05_102065.shtml","publisher":"大庆市大同区人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"张国辉，区委常委、武装部政治委员"},
        {"id":"S014","title":"大同区政府—高振波副区长页","url":"http://www.dqdt.gov.cn/datong/qzffqz/202305/c05_281653.shtml","publisher":"大庆市大同区人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"高振波，副区长、大同公安分局局长"},
        {"id":"S015","title":"大同区政府—郑立国副区长页","url":"http://www.dqdt.gov.cn/datong/qzffqz/202412/c05_365064.shtml","publisher":"大庆市大同区人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"郑立国，副区长"},
        {"id":"S016","title":"大同区政府—魏玉峰副区长页","url":"http://www.dqdt.gov.cn/datong/qzffqz/202510/c05_392197.shtml","publisher":"大庆市大同区人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"魏玉峰，副区长"},
        {"id":"S017","title":"大同区政府—孙有斌人大主任页","url":"http://www.dqdt.gov.cn/datong/qrdzr/202510/c05_102072.shtml","publisher":"大庆市大同区人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"孙有斌，区人大常委会主任"},
        {"id":"S018","title":"大同区政府—吕国信政协主席页","url":"http://www.dqdt.gov.cn/datong/qzxzx/202510/c05_102080.shtml","publisher":"大庆市大同区人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"吕国信，区政协主席"},
    ]


def make_person_json(p, timeline, relationships_list, source_register):
    result = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "大庆市",
            "region": "大同区",
            "job": p["current_post"],
            "task_id": "heilongjiang_大同区",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"datongqu_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender",""),
            "ethnicity": p.get("ethnicity",""),
            "birth": p.get("birth",""),
            "birthplace": p.get("birthplace",""),
            "native_place": "",
            "education": [],
            "party_join": p.get("party_join",""),
            "work_start": p.get("work_start",""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source","")
            }
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "县处级正职" if ("区委书记" == p["current_post"] or "区长" == p["current_post"] or "人大" in p["current_post"] or "政协" in p["current_post"]) else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": []
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": relationships_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary":"","notable_fast_promotions":[]}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type":"none_found","description":"在公开信息中未发现该人物负面信号","date":"","confidence":"unverified","source_ids":[]}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "high",
            "biggest_gap": f"{p['name']}的完整履历信息（出生日期、教育背景、早期职业生涯）有待补充"
        },
        "open_questions": [
            {"priority":"critical",
             "question": f"{p['name']}的完整职业生涯履历（出生日期、教育背景、历任职务）",
             "why_it_matters": "无法追溯其任职路径、系统经历和晋升速度",
             "suggested_queries": [f"{p['name']} 简历 大庆",f"{p['name']} 大同区",f"{p['name']} 任前公示"],
             "last_attempted": AS_OF}
        ]
    }
    return result


def build_person_jsons():
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()

    # 1. 诸葛祥龙 (区委书记)
    zhuge_timeline = [
        {"start":"2024-12","end":"","org":"中共大庆市大同区委员会","title":"大同区委书记","notes":"2024年12月由区长升任区委书记；主持区委全面工作","confidence":"confirmed","source_ids":["S001","S005","S007"]},
        {"start":"2021-11","end":"2024-12","org":"大庆市大同区人民政府","title":"大同区区长","notes":"2021年11月任代区长，12月当选区长","confidence":"confirmed","source_ids":["S001"]},
        {"start":"","end":"2021-11","org":"大庆油田储气库分公司","title":"大庆油田储气库分公司经理","notes":"此前任职，具体时间待确认","confidence":"plausible","source_ids":[]},
    ]
    zhuge_relationships = [
        {"person":"李文章","person_id":"datongqu_李文章","relationship_type":"overlap","strength":"strong","evidence":"区委书记与区长党政工作搭档","overlap_org":"大同区","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S002","S006"]},
        {"person":"马强","person_id":"datongqu_马强","relationship_type":"overlap","strength":"medium","evidence":"区委书记与专职副书记","overlap_org":"中共大同区委","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S004"]},
    ]
    zhuge_json = make_person_json(persons[0], zhuge_timeline, zhuge_relationships, source_register)
    zhuge_path = PERSONS_DIR / f"{TODAY}-黑龙江省-大庆市-区委书记-诸葛祥龙.json"
    with open(zhuge_path, "w", encoding="utf-8") as f:
        json.dump(zhuge_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {zhuge_path.name}")

    # 2. 李文章 (区长)
    li_timeline = [
        {"start":"","end":"","org":"中共大庆市大同区委员会","title":"大同区委副书记","notes":"","confidence":"confirmed","source_ids":["S002","S003"]},
        {"start":"","end":"","org":"大庆市大同区人民政府","title":"大同区区长","notes":"主持区政府全面工作","confidence":"confirmed","source_ids":["S002","S006"]},
        {"start":"","end":"","org":"中共大庆市萨尔图区委员会","title":"萨尔图区委常委、副区长","notes":"此前曾任此职；具体时间待确认","confidence":"plausible","source_ids":[]},
    ]
    li_relationships = [
        {"person":"诸葛祥龙","person_id":"datongqu_诸葛祥龙","relationship_type":"overlap","strength":"strong","evidence":"区长与区委书记党政工作搭档","overlap_org":"大同区","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S001","S002"]},
    ]
    li_json = make_person_json(persons[1], li_timeline, li_relationships, source_register)
    li_path = PERSONS_DIR / f"{TODAY}-黑龙江省-大庆市-区长-李文章.json"
    with open(li_path, "w", encoding="utf-8") as f:
        json.dump(li_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {li_path.name}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  大庆市大同区领导班子工作关系网络")
    print("  等级: 市辖区")
    print(f"  调查日期: {AS_OF}")
    print("  信息来源: 大同区政府网站")
    print("=" * 60)
    
    build_db()
    build_gexf()
    build_person_jsons()
    
    print(f"\n✅ 大同区数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

if __name__ == "__main__":
    main()
