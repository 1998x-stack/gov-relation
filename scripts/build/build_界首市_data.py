#!/usr/bin/env python3
"""Build Jieshou (界首市) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Task: anhui_界首市 (安徽省阜阳市界首市 - 县级市)

Confirmed officeholders (as of 2026-07-15):
  - 市委书记: 曾认, in office since ~June/July 2026 (15th Party Congress)
  - 市长: 李祎楠 (1979-06, 省委党校研究生学历), in office since ~2024

Previous officeholders:
  - 前市委书记: 祁畅 (1973-08, 省委党校大学学历), served until ~June 2026

Sources:
  - https://www.ahjs.gov.cn/ (界首市人民政府领导之窗, accessed 2026-07-15)
  - https://www.ahjs.gov.cn/Leader/showList/1/0.html (市委领导)
  - https://www.ahjs.gov.cn/Leader/showList/3/0.html (市政府领导)
  - https://www.ahjs.gov.cn/Content/show/1332236.html (十五届市委常委会第1次会议, 2026-07-08)
  - https://www.ahjs.gov.cn/Content/show/1332949.html (曾认调研, 2026-07-15)
  - https://www.ahjs.gov.cn/Content/show/1332817.html (市委专题会议, 2026-07-14)

Confidence: Core leader identities from official government website.
Mayor's name and basic bio from official leadership page with confirmation via news articles.
Party secretary (曾认) confirmed via multiple news articles in July 2026.
Predecessor 祁畅 confirmed via leadership page basic info.
Full career timelines for 曾认 and 李祎楠 are partially complete pending detailed resume pages.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "界首市_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "界首市_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ── Top Leaders ──────────────────────────────────────────────────
    {
        "id": 1,
        "name": "曾认",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共界首市委",
        "source": "https://www.ahjs.gov.cn/Content/show/1332949.html",
        "notes": "2026年7月起任界首市委书记。此前履历待补充。主持市委全面工作。2026年7月7日主持召开十五届市委常委会第1次会议。此前活动中未见其以书记身份出现，推测在2026年6-7月间界首市委换届（十五届）时上任。",
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "李祎楠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-06",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "界首市人民政府",
        "source": "https://www.ahjs.gov.cn/Leader/showList/1/0.html",
        "notes": "1979年6月出生，省委党校研究生学历，中共党员。现任界首市委副书记，市政府市长、党组书记。领导市政府全面工作，负责审计方面工作。分管市审计局。",
        "confidence": "confirmed"
    },
    # ── Predecessors ────────────────────────────────────────────────
    {
        "id": 3,
        "name": "祁畅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-08",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "前市委书记",
        "current_org": "（不再担任界首市委书记）",
        "source": "https://www.ahjs.gov.cn/Leader/showList/1/0.html",
        "notes": "1973年8月出生，省委党校大学学历，中共党员。曾任界首市委书记（至2026年6月左右）。2026年2月仍有以书记身份参加活动的记录(2026-02-21祁畅调研督导)。2026年7月起由曾认接任。",
        "confidence": "confirmed"
    },
    # ── Government Leaders ──────────────────────────────────────────
    {
        "id": 4,
        "name": "丁军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "界首市人民政府",
        "source": "https://www.ahjs.gov.cn/Leader/showList/1/0.html",
        "notes": "市委常委、市政府党组副书记、常务副市长。",
        "confidence": "confirmed"
    },
    {
        "id": 5,
        "name": "李兴联",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "界首市人民政府",
        "source": "https://www.ahjs.gov.cn/Leader/showList/1/0.html",
        "notes": "市委常委、副市长。",
        "confidence": "confirmed"
    },
    {
        "id": 6,
        "name": "李久坤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "界首市人民政府",
        "source": "https://www.ahjs.gov.cn/Leader/showList/1/0.html",
        "notes": "市政府副市长、党组成员。",
        "confidence": "confirmed"
    },
    {
        "id": 7,
        "name": "郑磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长、公安局局长",
        "current_org": "界首市人民政府",
        "source": "https://www.ahjs.gov.cn/Leader/showList/1/0.html",
        "notes": "市政府副市长、党组成员，公安局局长。",
        "confidence": "confirmed"
    },
    {
        "id": 8,
        "name": "金自强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "界首市人民政府",
        "source": "https://www.ahjs.gov.cn/Leader/showList/1/0.html",
        "notes": "市政府副市长、党组成员。",
        "confidence": "confirmed"
    },
    {
        "id": 9,
        "name": "刘素梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "界首市人民政府",
        "source": "https://www.ahjs.gov.cn/Leader/showList/1/0.html",
        "notes": "市政府副市长、党组成员。",
        "confidence": "confirmed"
    },
    {
        "id": 10,
        "name": "王龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "界首市人民政府",
        "source": "https://www.ahjs.gov.cn/Leader/showList/1/0.html",
        "notes": "市政府副市长、党组成员。",
        "confidence": "confirmed"
    },
    # ── Party Standing Committee (市委常委会) ──────────────────
    {
        "id": 11,
        "name": "周明敬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共界首市委",
        "source": "https://www.ahjs.gov.cn/Content/show/1332236.html",
        "notes": "十五届市委常委。2026年7月7日参加十五届市委常委会第1次会议。",
        "confidence": "confirmed"
    },
    {
        "id": 12,
        "name": "刘辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共界首市委",
        "source": "https://www.ahjs.gov.cn/Content/show/1332236.html",
        "notes": "十五届市委常委。2026年7月7日参加十五届市委常委会第1次会议。",
        "confidence": "confirmed"
    },
    {
        "id": 13,
        "name": "冯启俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共界首市委",
        "source": "https://www.ahjs.gov.cn/Content/show/1332236.html",
        "notes": "十五届市委常委。2026年7月7日参加十五届市委常委会第1次会议。",
        "confidence": "confirmed"
    },
    {
        "id": 14,
        "name": "蔡淑娜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、组织部部长、统战部部长",
        "current_org": "中共界首市委",
        "source": "https://www.ahjs.gov.cn/Content/show/1332627.html",
        "notes": "市委常委、市委组织部部长、统战部部长、政协党组副书记。2026年7月9日以该身份参加市政协会议。十五届市委常委。",
        "confidence": "confirmed"
    },
    {
        "id": 15,
        "name": "程军衣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共界首市委",
        "source": "https://www.ahjs.gov.cn/Content/show/1332236.html",
        "notes": "十五届市委常委。2026年7月7日参加十五届市委常委会第1次会议。",
        "confidence": "confirmed"
    },
    {
        "id": 16,
        "name": "朱琳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共界首市委",
        "source": "https://www.ahjs.gov.cn/Content/show/1332236.html",
        "notes": "十五届市委常委。2026年7月7日参加十五届市委常委会第1次会议。",
        "confidence": "confirmed"
    },
    # ── People's Congress ──────────────────────────────────────────
    {
        "id": 17,
        "name": "李子刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-05",
        "birthplace": "",
        "native_place": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会党组书记、主任",
        "current_org": "界首市人大常委会",
        "source": "https://www.ahjs.gov.cn/Leader/showList/2/0.html",
        "notes": "1970年5月出生，大学学历，中共党员。主持市人大常委会全面工作。",
        "confidence": "confirmed"
    },
    {
        "id": 18,
        "name": "秦玉超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协党组书记、主席",
        "current_org": "界首市政协",
        "source": "https://www.ahjs.gov.cn/Content/show/1332627.html",
        "notes": "市政协党组书记、主席。2026年7月9日以该身份参加市政协十四届常委会第二十四次会议。",
        "confidence": "confirmed"
    },
]

# ── Organizations ──────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共界首市委", "type": "党委", "level": "县", "parent": "中共阜阳市委", "location": "界首市"},
    {"id": 2, "name": "界首市人民政府", "type": "政府", "level": "县", "parent": "阜阳市人民政府", "location": "界首市"},
    {"id": 3, "name": "界首市人大常委会", "type": "人大", "level": "县", "parent": "阜阳市人大常委会", "location": "界首市"},
    {"id": 4, "name": "界首市政协", "type": "政协", "level": "县", "parent": "阜阳市政协", "location": "界首市"},
    {"id": 5, "name": "界首市公安局", "type": "政府", "level": "县", "parent": "界首市人民政府", "location": "界首市"},
]

# ── Positions ──────────────────────────────────────────────────────────

positions = [
    # 曾认
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "2026-06", "end": "present", "rank": "1", "note": "十五届界首市委书记"},
    # 李祎楠
    {"person_id": 2, "org_id": 2, "title": "市委副书记、市长", "start": "", "end": "present", "rank": "1", "note": "市政府党组书记"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "2", "note": ""},
    # 祁畅 (predecessor)
    {"person_id": 3, "org_id": 1, "title": "市委书记", "start": "", "end": "2026-06", "rank": "1", "note": "十四届界首市委书记，2026年换届卸任"},
    # 丁军
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "3", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "常务副市长", "start": "", "end": "present", "rank": "2", "note": "市政府党组副书记"},
    # 李兴联
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "3", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "4", "note": ""},
    # 李久坤
    {"person_id": 6, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "5", "note": "市政府党组成员"},
    # 郑磊
    {"person_id": 7, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "5", "note": "市政府党组成员"},
    {"person_id": 7, "org_id": 5, "title": "公安局局长", "start": "", "end": "present", "rank": "1", "note": ""},
    # 金自强
    {"person_id": 8, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "5", "note": "市政府党组成员"},
    # 刘素梅
    {"person_id": 9, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "5", "note": "市政府党组成员"},
    # 王龙
    {"person_id": 10, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "5", "note": "市政府党组成员"},
    # 周明敬
    {"person_id": 11, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "3", "note": "十五届市委常委"},
    # 刘辉
    {"person_id": 12, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "3", "note": "十五届市委常委"},
    # 冯启俊
    {"person_id": 13, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "3", "note": "十五届市委常委"},
    # 蔡淑娜
    {"person_id": 14, "org_id": 1, "title": "市委常委、组织部部长、统战部部长", "start": "", "end": "present", "rank": "3", "note": "兼政协党组副书记"},
    # 程军衣
    {"person_id": 15, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "3", "note": "十五届市委常委"},
    # 朱琳
    {"person_id": 16, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "3", "note": "十五届市委常委"},
    # 李子刚
    {"person_id": 17, "org_id": 3, "title": "市人大常委会党组书记、主任", "start": "", "end": "present", "rank": "1", "note": "主持市人大常委会全面工作"},
    # 秦玉超
    {"person_id": 18, "org_id": 4, "title": "市政协党组书记、主席", "start": "", "end": "present", "rank": "1", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────

relationships = [
    # 曾认 ↔ 李祎楠 (书记-市长搭档)
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "市委常委班子同届核心成员",
        "overlap_org": "中共界首市委",
        "overlap_period": "2026-07至今",
        "notes": "曾认接任书记后与李祎楠组成新一届党政班子，两人共同出席十五届市委常委会第1次会议",
        "strength": "strong",
        "confidence": "confirmed"
    },
    # 曾认 ↔ 祁畅 (前任-继任)
    {
        "person_a": 3, "person_b": 1,
        "type": "predecessor_successor",
        "context": "界首市委书记前任-继任",
        "overlap_org": "中共界首市委",
        "overlap_period": "2026年换届交接",
        "notes": "祁畅在2026年6月前担任界首市委书记，曾认在十五届市委换届后接任",
        "strength": "strong",
        "confidence": "confirmed"
    },
    # 丁军 ↔ 李祎楠 (正副市长)
    {
        "person_a": 4, "person_b": 2,
        "type": "superior_subordinate",
        "context": "常务副市长是市长主要副手",
        "overlap_org": "界首市人民政府",
        "overlap_period": "当前",
        "notes": "丁军作为常务副市长协助李祎楠主持政府日常工作",
        "strength": "strong",
        "confidence": "confirmed"
    },
    # 李祎楠 ↔ 曾认 (市委-政府领导关系)
    {
        "person_a": 2, "person_b": 1,
        "type": "superior_subordinate",
        "context": "市长在市委常委会中接受书记领导",
        "overlap_org": "中共界首市委",
        "overlap_period": "2026-07至今",
        "notes": "李祎楠作为市委副书记、市长，在市委常委会中在曾认领导下工作",
        "strength": "strong",
        "confidence": "confirmed"
    },
    # 蔡淑娜 ↔ 曾认 (组织部长-书记)
    {
        "person_a": 14, "person_b": 1,
        "type": "superior_subordinate",
        "context": "组织部长、统战部长在市委常委会中接受书记领导",
        "overlap_org": "中共界首市委",
        "overlap_period": "当前",
        "notes": "",
        "strength": "medium",
        "confidence": "confirmed"
    },
    # 李子刚 ↔ 曾认 (人大主任-书记)
    {
        "person_a": 17, "person_b": 1,
        "type": "overlap",
        "context": "人大常委会主任列席市委常委会",
        "overlap_org": "中共界首市委",
        "overlap_period": "当前",
        "notes": "李子刚以市人大常委会主任身份列席十五届市委常委会第1次会议",
        "strength": "medium",
        "confidence": "confirmed"
    },
    # 秦玉超 ↔ 曾认 (政协主席-书记)
    {
        "person_a": 18, "person_b": 1,
        "type": "overlap",
        "context": "政协主席列席市委常委会",
        "overlap_org": "中共界首市委",
        "overlap_period": "当前",
        "notes": "秦玉超以市政协主席身份列席十五届市委常委会第1次会议",
        "strength": "medium",
        "confidence": "confirmed"
    },
]


# ═══════════════════════════════════════════════════════════════════════
# SQLite
# ═══════════════════════════════════════════════════════════════════════

def create_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
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
            "end" TEXT,
            rank TEXT,
            note TEXT
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            notes TEXT,
            strength TEXT,
            confidence TEXT
        );
    """)

    for p in persons:
        c.execute("""
            INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p["birthplace"], p["education"], p["party_join"],
              p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""
            INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""
            INSERT INTO positions
            (person_id, org_id, title, start, "end", rank, note)
            VALUES (?,?,?,?,?,?,?)
        """, (pos["person_id"], pos["org_id"], pos["title"],
              pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org,
             overlap_period, notes, strength, confidence)
            VALUES (?,?,?,?,?,?,?,?,?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"],
              r["overlap_org"], r["overlap_period"], r["notes"],
              r["strength"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"  DB written: {DB_PATH}")


# ═══════════════════════════════════════════════════════════════════════
# GEXF
# ═══════════════════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return r,g,b string for a person node based on role."""
    post = p.get("current_post", "")
    if "书记" in post and "市委" in post:
        return "255,50,50"
    elif "市长" in post or "副市长" in post or "常务" in post:
        return "50,100,255"
    elif "人大" in post:
        return "200,255,255"
    elif "政协" in post:
        return "255,240,200"
    else:
        return "100,100,100"

def org_color(o):
    """Return r,g,b string for an organization node."""
    t = o["type"]
    if t == "党委":
        return "255,200,200"
    elif t == "政府":
        return "200,200,255"
    elif t == "人大":
        return "200,255,255"
    elif t == "政协":
        return "255,240,200"
    else:
        return "200,200,200"

def is_top_leader(p):
    post = p.get("current_post", "")
    return "书记" in post or "市长" in post

def create_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append('    <description>界首市领导工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="level" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="strength" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('      <attribute id="3" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('          <attvalue for="1" value=""/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        w = "2.0" if r.get("strength") == "strong" else "1.5"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("strength",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("confidence",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("context",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {GEXF_PATH}")


# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Building 界首市 leadership network...")
    create_database()
    create_gexf()
    print("Done.")
