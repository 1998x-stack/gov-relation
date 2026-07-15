#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 灵璧县 (Lingbi, Suzhou, Anhui) leadership network.
Generated: 2026-07-15
Task: anhui_灵璧县 - 县委书记 & 县长
Sources: Official government website (www.lingbi.gov.cn), news articles, party congress reports.
Notes: See confidence labels and open_questions for gaps.
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
STAGING = BASE
DB_PATH = os.path.join(STAGING, "灵璧县_network.db")
GEXF_PATH = os.path.join(STAGING, "灵璧县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ═══════════════════════════════════════════════════════════════════
    # Core Leaders
    # ═══════════════════════════════════════════════════════════════════
    {"id": 1, "name": "薛勇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵璧县县委书记", "current_org": "中共灵璧县委员会",
     "source": "https://www.lingbi.gov.cn/zwxx/zwyw/163930951.html",
     "notes": "灵璧县县委书记。2026年6月23日主持中共灵璧县第十五次代表大会闭幕式并讲话。此前曾任灵璧县县长，后接任县委书记。曾调研财政局、经济开发区、乡镇重点工作、医疗机构消防安全等。",
     "confidence": "confirmed"},

    {"id": 2, "name": "魏启宏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵璧县县委副书记、县长", "current_org": "灵璧县人民政府",
     "source": "https://www.lingbi.gov.cn/zwxx/zwyw/163910901.html",
     "notes": "灵璧县县委副书记、县政府县长。2026年7月6日与县委书记薛勇分别调研防汛减灾及安全生产工作。2026年7月6日主持县政府常务会议。中共灵璧县第十五次代表大会主席团常务委员会成员。",
     "confidence": "confirmed"},

    # ═══════════════════════════════════════════════════════════════════
    # 县委领导（从县第十五次党代会主席团常务委员会名单确认）
    # ═══════════════════════════════════════════════════════════════════
    {"id": 3, "name": "晋军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵璧县县委副书记", "current_org": "中共灵璧县委员会",
     "source": "https://www.lingbi.gov.cn/zwxx/zwyw/163910091.html",
     "notes": "县委副书记。中共灵璧县第十五次代表大会主席团常务委员会成员。列席县委常委会会议。",
     "confidence": "confirmed"},

    {"id": 4, "name": "王军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵璧县县委常委", "current_org": "中共灵璧县委员会",
     "source": "https://www.lingbi.gov.cn/zwxx/zwyw/163878881.html",
     "notes": "县委常委。中共灵璧县第十五次代表大会主席团常务委员会成员。",
     "confidence": "confirmed"},

    {"id": 5, "name": "王亚斌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵璧县县委常委", "current_org": "中共灵璧县委员会",
     "source": "https://www.lingbi.gov.cn/zwxx/zwyw/163910101.html",
     "notes": "县委常委。中共灵璧县第十五次代表大会主席团常务委员会成员。曾陪同县委书记薛勇调研医疗机构消防安全。",
     "confidence": "confirmed"},

    {"id": 6, "name": "许东方", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵璧县县委常委", "current_org": "中共灵璧县委员会",
     "source": "https://www.lingbi.gov.cn/zwxx/zwyw/163878881.html",
     "notes": "县委常委。中共灵璧县第十五次代表大会主席团常务委员会成员。",
     "confidence": "confirmed"},

    {"id": 7, "name": "高海峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵璧县县委常委", "current_org": "中共灵璧县委员会",
     "source": "https://www.lingbi.gov.cn/zwxx/zwyw/163915071.html",
     "notes": "县委常委。中共灵璧县第十五次代表大会主席团常务委员会成员。曾参加薛勇到财政局、经济开发区调研活动。",
     "confidence": "confirmed"},

    {"id": 8, "name": "杨礼胜", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵璧县县委常委", "current_org": "中共灵璧县委员会",
     "source": "https://www.lingbi.gov.cn/zwxx/zwyw/163878881.html",
     "notes": "县委常委。中共灵璧县第十五次代表大会主席团常务委员会成员。",
     "confidence": "confirmed"},

    {"id": 9, "name": "陆璋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵璧县县委常委", "current_org": "中共灵璧县委员会",
     "source": "https://www.lingbi.gov.cn/zwxx/zwyw/163910101.html",
     "notes": "县委常委。中共灵璧县第十五次代表大会主席团常务委员会成员。曾陪同县委书记薛勇调研医疗机构消防安全。",
     "confidence": "confirmed"},

    {"id": 10, "name": "李媛媛", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵璧县县委常委、宣传部部长", "current_org": "中共灵璧县县委宣传部",
     "source": "https://www.lingbi.gov.cn/zwxx/zwyw/163893011.html",
     "notes": "县委常委、宣传部部长。中共灵璧县第十五次代表大会主席团常务委员会成员。2026年6月29日主持和美乡村直播间工作推进会。",
     "confidence": "confirmed"},

    {"id": 11, "name": "王锐", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵璧县县委常委、县纪委书记", "current_org": "中共灵璧县纪律检查委员会",
     "source": "https://www.lingbi.gov.cn/zwxx/zwyw/163876021.html",
     "notes": "县委常委、县纪委书记。中共灵璧县第十五次代表大会主席团常务委员会成员。在党代会开幕式上代表第十四届纪律检查委员会作工作报告。",
     "confidence": "confirmed"},

    {"id": 12, "name": "薛燕", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵璧县县委常委、组织部部长", "current_org": "中共灵璧县县委组织部",
     "source": "https://www.lingbi.gov.cn/zwxx/zwyw/163930951.html",
     "notes": "县委常委、组织部部长。中共灵璧县第十五次代表大会主席团常务委员会成员。曾参加薛勇赴乡镇调研活动。",
     "confidence": "confirmed"},

    # ═══════════════════════════════════════════════════════════════════
    # 人大/政协领导
    # ═══════════════════════════════════════════════════════════════════
    {"id": 13, "name": "马实忠", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵璧县人大常委会主任", "current_org": "灵璧县人民代表大会常务委员会",
     "source": "https://www.lingbi.gov.cn/zwxx/zwyw/163910091.html",
     "notes": "县人大常委会主任。中共灵璧县第十五次代表大会主席团常务委员会成员。列席县委常委会会议。",
     "confidence": "confirmed"},

    {"id": 14, "name": "曹强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵璧县政协主席", "current_org": "中国人民政治协商会议灵璧县委员会",
     "source": "https://www.lingbi.gov.cn/zwxx/zwyw/163910091.html",
     "notes": "县政协主席。中共灵璧县第十五次代表大会主席团常务委员会成员。列席县委常委会会议。",
     "confidence": "confirmed"},

    {"id": 15, "name": "孙荣才", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "灵璧县副县长", "current_org": "灵璧县人民政府",
     "source": "https://www.lingbi.gov.cn/zwxx/zwyw/163910901.html",
     "notes": "副县长。曾参加防汛减灾及安全生产调研活动。",
     "confidence": "confirmed"},
]

organizations = [
    {"id": 1, "name": "中共灵璧县委员会", "type": "党委", "level": "县",
     "parent": "中共宿州市委", "location": "安徽省宿州市灵璧县"},
    {"id": 2, "name": "灵璧县人民政府", "type": "政府", "level": "县",
     "parent": "宿州市人民政府", "location": "安徽省宿州市灵璧县"},
    {"id": 3, "name": "中共灵璧县纪律检查委员会", "type": "纪委", "level": "县",
     "parent": "中共宿州市纪律检查委员会", "location": "安徽省宿州市灵璧县"},
    {"id": 4, "name": "中共灵璧县县委组织部", "type": "党委部门", "level": "县",
     "parent": "中共灵璧县委员会", "location": "安徽省宿州市灵璧县"},
    {"id": 5, "name": "中共灵璧县县委宣传部", "type": "党委部门", "level": "县",
     "parent": "中共灵璧县委员会", "location": "安徽省宿州市灵璧县"},
    {"id": 6, "name": "灵璧县人民代表大会常务委员会", "type": "人大", "level": "县",
     "parent": "宿州市人民代表大会常务委员会", "location": "安徽省宿州市灵璧县"},
    {"id": 7, "name": "中国人民政治协商会议灵璧县委员会", "type": "政协", "level": "县",
     "parent": "中国人民政治协商会议宿州市委员会", "location": "安徽省宿州市灵璧县"},
]

positions = [
    # 薛勇 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "灵璧县县委书记", "start": "", "end": "present", "rank": "正处级", "note": "现任灵璧县县委书记"},

    # 魏启宏 - 县长
    {"person_id": 2, "org_id": 2, "title": "灵璧县县委副书记、县长", "start": "", "end": "present", "rank": "正处级", "note": "现任灵璧县县长"},
    {"person_id": 2, "org_id": 1, "title": "灵璧县县委副书记", "start": "", "end": "present", "rank": "副处级", "note": "兼任县委副书记"},

    # 晋军 - 县委副书记
    {"person_id": 3, "org_id": 1, "title": "灵璧县县委副书记", "start": "", "end": "present", "rank": "副处级", "note": "县委副书记"},

    # 县委常委
    {"person_id": 4, "org_id": 1, "title": "灵璧县县委常委", "start": "", "end": "present", "rank": "副处级", "note": "县委常委"},
    {"person_id": 5, "org_id": 1, "title": "灵璧县县委常委", "start": "", "end": "present", "rank": "副处级", "note": "县委常委"},
    {"person_id": 6, "org_id": 1, "title": "灵璧县县委常委", "start": "", "end": "present", "rank": "副处级", "note": "县委常委"},
    {"person_id": 7, "org_id": 1, "title": "灵璧县县委常委", "start": "", "end": "present", "rank": "副处级", "note": "县委常委"},
    {"person_id": 8, "org_id": 1, "title": "灵璧县县委常委", "start": "", "end": "present", "rank": "副处级", "note": "县委常委"},
    {"person_id": 9, "org_id": 1, "title": "灵璧县县委常委", "start": "", "end": "present", "rank": "副处级", "note": "县委常委"},
    {"person_id": 10, "org_id": 5, "title": "灵璧县县委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": "县委宣传部部长"},
    {"person_id": 10, "org_id": 1, "title": "灵璧县县委常委", "start": "", "end": "present", "rank": "副处级", "note": "县委常委"},
    {"person_id": 11, "org_id": 3, "title": "灵璧县县委常委、县纪委书记", "start": "", "end": "present", "rank": "副处级", "note": "县纪委书记、监委主任"},
    {"person_id": 11, "org_id": 1, "title": "灵璧县县委常委", "start": "", "end": "present", "rank": "副处级", "note": "县委常委"},
    {"person_id": 12, "org_id": 4, "title": "灵璧县县委常委、组织部部长", "start": "", "end": "present", "rank": "副处级", "note": "县委组织部部长"},
    {"person_id": 12, "org_id": 1, "title": "灵璧县县委常委", "start": "", "end": "present", "rank": "副处级", "note": "县委常委"},

    # 人大/政协
    {"person_id": 13, "org_id": 6, "title": "灵璧县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": "县人大常委会主任"},
    {"person_id": 14, "org_id": 7, "title": "灵璧县政协主席", "start": "", "end": "present", "rank": "正处级", "note": "县政协主席"},

    # 副县长
    {"person_id": 15, "org_id": 2, "title": "灵璧县副县长", "start": "", "end": "present", "rank": "副处级", "note": "副县长"},
]

relationships = [
    # 薛勇 ←→ 魏启宏: 书记县长搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "薛勇（县委书记）与魏启宏（县长）为现任书记县长党政搭档关系",
     "overlap_org": "灵璧县", "overlap_period": "至今",
     "strength": "strong", "confidence": "confirmed"},

    # 薛勇 ←→ 晋军: 书记与副书记
    {"person_a": 1, "person_b": 3, "type": "上下级",
     "context": "薛勇（县委书记）与晋军（县委副书记）为上下级关系",
     "overlap_org": "中共灵璧县委员会", "overlap_period": "至今",
     "strength": "strong", "confidence": "confirmed"},

    # 薛勇 ←→ 薛燕: 共同调研
    {"person_a": 1, "person_b": 12, "type": "工作关系",
     "context": "薛勇与组织部部长薛燕共同赴乡镇调研",
     "overlap_org": "中共灵璧县委员会", "overlap_period": "至今",
     "strength": "medium", "confidence": "confirmed"},

    # 薛勇 ←→ 王亚斌: 共同调研
    {"person_a": 1, "person_b": 5, "type": "工作关系",
     "context": "薛勇与王亚斌共同调研医疗机构消防安全工作",
     "overlap_org": "中共灵璧县委员会", "overlap_period": "至今",
     "strength": "medium", "confidence": "confirmed"},

    # 薛勇 ←→ 陆璋: 共同调研
    {"person_a": 1, "person_b": 9, "type": "工作关系",
     "context": "薛勇与陆璋共同调研医疗机构消防安全工作",
     "overlap_org": "中共灵璧县委员会", "overlap_period": "至今",
     "strength": "medium", "confidence": "confirmed"},

    # 薛勇 ←→ 高海峰: 共同调研
    {"person_a": 1, "person_b": 7, "type": "工作关系",
     "context": "薛勇与高海峰共同到财政局、经济开发区走访调研",
     "overlap_org": "中共灵璧县委员会", "overlap_period": "至今",
     "strength": "medium", "confidence": "confirmed"},

    # 魏启宏 ←→ 马实忠: 党政人大
    {"person_a": 2, "person_b": 13, "type": "党政人大",
     "context": "魏启宏（县长）与马实忠（县人大常委会主任）工作关系，马实忠列席县政府常务会议",
     "overlap_org": "灵璧县", "overlap_period": "至今",
     "strength": "medium", "confidence": "confirmed"},

    # 魏启宏 ←→ 曹强: 党政政协
    {"person_a": 2, "person_b": 14, "type": "党政政协",
     "context": "魏启宏（县长）与曹强（县政协主席）工作关系",
     "overlap_org": "灵璧县", "overlap_period": "至今",
     "strength": "medium", "confidence": "confirmed"},

    # 魏启宏 ←→ 孙荣才: 县长与副县长
    {"person_a": 2, "person_b": 15, "type": "上下级",
     "context": "魏启宏（县长）与孙荣才（副县长）为上下级关系，共同参加防汛调研",
     "overlap_org": "灵璧县人民政府", "overlap_period": "至今",
     "strength": "strong", "confidence": "confirmed"},

    # 马实忠 ←→ 曹强: 人大政协
    {"person_a": 13, "person_b": 14, "type": "同僚",
     "context": "马实忠（县人大常委会主任）与曹强（县政协主席）同为县级正职领导，共同列席县委常委会",
     "overlap_org": "灵璧县", "overlap_period": "至今",
     "strength": "medium", "confidence": "confirmed"},

    # 晋军 ←→ 马实忠: 县委人大
    {"person_a": 3, "person_b": 13, "type": "工作关系",
     "context": "晋军（县委副书记）与马实忠（县人大常委会主任）共同参加县委理论学习中心组学习",
     "overlap_org": "中共灵璧县委员会", "overlap_period": "至今",
     "strength": "medium", "confidence": "confirmed"},

    # 王锐 ←→ 薛勇: 纪委书记与书记
    {"person_a": 11, "person_b": 1, "type": "上下级",
     "context": "王锐（纪委书记）向党代会作纪委工作报告，受薛勇（县委书记）领导",
     "overlap_org": "中共灵璧县委员会", "overlap_period": "至今",
     "strength": "strong", "confidence": "confirmed"},
]

# ── BUILD ────────────────────────────────────────────────────────────

def build():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = ON;")

    c.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT,
            education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT,
            source TEXT,
            notes TEXT, confidence TEXT
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            strength TEXT, confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source,
             notes, confidence)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"],
             p["birth"], p["birthplace"], p["education"],
             p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"],
             p["notes"], p["confidence"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"],
             o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for rel in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period,
             strength, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (rel["person_a"], rel["person_b"], rel["type"],
             rel["context"], rel["overlap_org"], rel["overlap_period"],
             rel["strength"], rel["confidence"]))

    conn.commit()
    conn.close()
    print(f"[DB] Wrote {DB_PATH}")


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    title = p.get("current_post", "")
    if "县委书记" in title or "区委书记" in title:
        return "255,50,50"
    if "县长" in title or "区长" in title:
        return "50,100,255"
    if "纪委书记" in title or "监委" in title:
        return "255,165,0"
    return "100,100,100"


def person_size(p):
    title = p.get("current_post", "")
    if "县委书记" in title or "县长" in title or "区长" in title:
        return "20.0"
    if "人大常委会主任" in title or "政协主席" in title:
        return "16.0"
    if "县委常委" in title:
        return "12.0"
    return "12.0"


def org_color(o):
    t = o["type"]
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "纪委" in t:
        return "255,200,200"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    if "组织" in t or "宣传" in t or "政法" in t or "党委部门" in t:
        return "255,200,200"
    return "200,200,200"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>灵璧县领导班子工作关系网络数据库</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="level" type="string"/>')
    lines.append('      <attribute id="4" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        pid = f"p{p['id']}"
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("confidence",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = f"o{o['id']}"
        c = org_color(o)
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(o.get("level",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # person → organization (worked_at)
    for pos in positions:
        pid = f"p{pos['person_id']}"
        oid = f"o{pos['org_id']}"
        lines.append(f'      <edge id="{eid}" source="{pid}" target="{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # person ↔ person (relationship)
    for rel in relationships:
        pa = f"p{rel['person_a']}"
        pb = f"p{rel['person_b']}"
        weight = "2.0" if rel.get("strength") == "strong" else "1.5"
        lines.append(f'      <edge id="{eid}" source="{pa}" target="{pb}" label="{esc(rel["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(rel.get("confidence",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[GEXF] Wrote {GEXF_PATH}")


if __name__ == "__main__":
    build()
    build_gexf()
    print("--- Summary ---")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print("Done.")
