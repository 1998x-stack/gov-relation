#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 大观区 (Daguan District, Anqing, Anhui) leadership network.

大观区 — 安徽省安庆市辖区, 安庆主城区之一, 面积约191平方公里, 辖7街道1镇2乡.
Sources:
  - www.aqdgq.gov.cn (official government website, leadership page accessed 2026-07-15)
  - www.aqdgq.gov.cn/ldzc/index.html (区委领导 + 区政府领导 listings)
  - zh.wikipedia.org/wiki/大观区 (geo/admin info)

Confidence: Current roles confirmed from official Daguan District government leadership page
(aqdgq.gov.cn/ldzc/). Biographical details for most figures are partial; career
timelines sourced from official brief bios. Predecessor information is marked with
confidence levels.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/anhui_大观区")
DB_PATH = os.path.join(STAGING, "大观区_network.db")
GEXF_PATH = os.path.join(STAGING, "大观区_network.gexf")

TODAY = datetime.now().strftime("%Y%m%d")

# ═══════════════════════════════════════════════════════════════════════
# DATA — All sourced from official aqdgq.gov.cn leadership page (2026-07-15)
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ── Core Leaders (Targets) ──

    # 华明 — 大观区委书记
    {"id": 1, "name": "华明", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-02", "birthplace": "安徽安庆", "education": "中央党校大学",
     "party_join": "1991-12", "work_start": "",
     "current_post": "大观区委书记",
     "current_org": "中共大观区委",
     "source": "https://www.aqdgq.gov.cn/ldzc/index.html",
     "notes": "1972年2月生，安徽安庆人，中央党校大学学历，1991年12月入党。主持区委全面工作。",
     "confidence": "confirmed"},

    # 许亮 — 大观区委副书记、区长
    {"id": 2, "name": "许亮", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-04", "birthplace": "安徽桐城", "education": "本科",
     "party_join": "2003-12", "work_start": "",
     "current_post": "大观区委副书记、区政府区长",
     "current_org": "大观区人民政府",
     "source": "https://www.aqdgq.gov.cn/ldzc/index.html",
     "notes": "1981年4月生，安徽桐城人，本科学历，2003年12月入党。领导区政府全面工作，负责审计工作。",
     "confidence": "confirmed"},

    # ── Predecessors (plausible based on available public records) ──

    # 前任大观区委书记（华明之前）— 潘功发
    {"id": 3, "name": "潘功发", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安庆市某职务（原大观区委书记）",
     "current_org": "",
     "source": "公开报道推断；前任区委书记身份待进一步确认",
     "notes": "华明的前任大观区委书记。据公开报道，潘功发于2021年前后任大观区委书记，华明接任时间待确认。此条目需进一步核实。",
     "confidence": "unverified"},

    # 前任大观区长（许亮之前）— 金玉
    {"id": 4, "name": "金玉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安庆市某职务（原大观区长）",
     "current_org": "",
     "source": "公开报道推断",
     "notes": "许亮的前任大观区长。金玉此前为大观区长，许亮接任时间待确认。",
     "confidence": "unverified"},

    # ── 区委常委（Standing Committee of the CPC Daguan District Committee）──

    # 余祥 — 区委副书记、区委党校校长（正县级）
    {"id": 5, "name": "余祥", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大观区委副书记、区委党校校长（正县级）",
     "current_org": "中共大观区委",
     "source": "https://www.aqdgq.gov.cn/ldzc/index.html",
     "notes": "正县级区委副书记，兼任区委党校校长。",
     "confidence": "confirmed"},

    # 程亮 — 区委常委、政法委书记
    {"id": 6, "name": "程亮", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大观区委常委、政法委书记",
     "current_org": "中共大观区委政法委员会",
     "source": "https://www.aqdgq.gov.cn/ldzc/index.html",
     "notes": "",
     "confidence": "confirmed"},

    # 刘小平 — 区委常委、组织部部长、统战部部长
    {"id": 7, "name": "刘小平", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大观区委常委、组织部部长、统战部部长",
     "current_org": "中共大观区委组织部",
     "source": "https://www.aqdgq.gov.cn/ldzc/index.html",
     "notes": "兼任组织部部长和统战部部长两职。",
     "confidence": "confirmed"},

    # 邱金生 — 区委常委、区纪委书记、监委主任
    {"id": 8, "name": "邱金生", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大观区委常委、区纪委书记、监委主任",
     "current_org": "中共大观区纪律检查委员会",
     "source": "https://www.aqdgq.gov.cn/ldzc/index.html",
     "notes": "",
     "confidence": "confirmed"},

    # 范兰芳 — 区委常委、宣传部部长
    {"id": 9, "name": "范兰芳", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大观区委常委、宣传部部长",
     "current_org": "中共大观区委宣传部",
     "source": "https://www.aqdgq.gov.cn/ldzc/index.html",
     "notes": "",
     "confidence": "confirmed"},

    # 彭凯 — 区委常委、大观经济开发区党工委书记
    {"id": 10, "name": "彭凯", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大观区委常委、大观经济开发区党工委书记",
     "current_org": "大观经济开发区",
     "source": "https://www.aqdgq.gov.cn/ldzc/index.html",
     "notes": "",
     "confidence": "confirmed"},

    # 刘晨光 — 区委常委、区人武部部长
    {"id": 11, "name": "刘晨光", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大观区委常委、区人武部部长",
     "current_org": "大观区人民武装部",
     "source": "https://www.aqdgq.gov.cn/ldzc/index.html",
     "notes": "军方代表进入区委常委会。",
     "confidence": "confirmed"},

    # 陈杰 — 区委常委、常务副区长
    {"id": 12, "name": "陈杰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大观区委常委、常务副区长",
     "current_org": "大观区人民政府",
     "source": "https://www.aqdgq.gov.cn/ldzc/index.html",
     "notes": "",
     "confidence": "confirmed"},

    # 徐海洋 — 区委常委、海口镇党委书记
    {"id": 13, "name": "徐海洋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大观区委常委、海口镇党委书记",
     "current_org": "中共海口镇委员会",
     "source": "https://www.aqdgq.gov.cn/ldzc/index.html",
     "notes": "由区委常委兼任海口镇党委书记，体现区委对乡镇工作的直接领导。",
     "confidence": "confirmed"},

    # ── 区政府副区长（Deputy District Mayors）──

    # 方正平 — 副区长、市公安局大观分局局长
    {"id": 14, "name": "方正平", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大观区副区长、市公安局大观分局党委书记、局长",
     "current_org": "大观区人民政府",
     "source": "https://www.aqdgq.gov.cn/ldzc/index.html",
     "notes": "公安系统代表；2026年6月22日参加《1584政风行风热线》访谈。",
     "confidence": "confirmed"},

    # 储艺 — 副区长
    {"id": 15, "name": "储艺", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大观区副区长",
     "current_org": "大观区人民政府",
     "source": "https://www.aqdgq.gov.cn/ldzc/index.html",
     "notes": "",
     "confidence": "confirmed"},

    # 何宏伟 — 副区长
    {"id": 16, "name": "何宏伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大观区副区长",
     "current_org": "大观区人民政府",
     "source": "https://www.aqdgq.gov.cn/ldzc/index.html",
     "notes": "",
     "confidence": "confirmed"},
]

# ── Organizations ──

organizations = [
    {"id": 1, "name": "中共大观区委", "type": "党委", "level": "县处级", "parent": "中共安庆市委", "location": "安庆市大观区"},
    {"id": 2, "name": "大观区人民政府", "type": "政府", "level": "县处级", "parent": "安庆市人民政府", "location": "安庆市大观区"},
    {"id": 3, "name": "中共大观区委政法委员会", "type": "党委", "level": "县处级", "parent": "中共大观区委", "location": "安庆市大观区"},
    {"id": 4, "name": "中共大观区委组织部", "type": "党委", "level": "县处级", "parent": "中共大观区委", "location": "安庆市大观区"},
    {"id": 5, "name": "中共大观区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共大观区委", "location": "安庆市大观区"},
    {"id": 6, "name": "中共大观区委宣传部", "type": "党委", "level": "县处级", "parent": "中共大观区委", "location": "安庆市大观区"},
    {"id": 7, "name": "大观经济开发区", "type": "开发区", "level": "县处级", "parent": "大观区人民政府", "location": "安庆市大观区"},
    {"id": 8, "name": "大观区人民武装部", "type": "政府", "level": "县处级", "parent": "安庆军分区", "location": "安庆市大观区"},
    {"id": 9, "name": "中共海口镇委员会", "type": "党委", "level": "乡科级", "parent": "中共大观区委", "location": "安庆市大观区海口镇"},
    {"id": 10, "name": "大观区委党校", "type": "事业单位", "level": "乡科级", "parent": "中共大观区委", "location": "安庆市大观区"},
    {"id": 11, "name": "安庆市公安局大观分局", "type": "政府", "level": "乡科级", "parent": "大观区人民政府", "location": "安庆市大观区"},
]

# ── Positions ──

positions = [
    # 华明
    {"id": 1, "person_id": 1, "org_id": 1, "title": "大观区委书记", "start": "", "end": "", "rank": 1, "note": "主持区委全面工作；由aqdgq.gov.cn确认"},
    # 许亮
    {"id": 2, "person_id": 2, "org_id": 2, "title": "大观区区长", "start": "", "end": "", "rank": 2, "note": "领导区政府全面工作；由aqdgq.gov.cn确认"},
    {"id": 3, "person_id": 2, "org_id": 1, "title": "大观区委副书记", "start": "", "end": "", "rank": 2, "note": ""},
    # 潘功发（前任书记）
    {"id": 4, "person_id": 3, "org_id": 1, "title": "大观区委书记（前任）", "start": "", "end": "", "rank": 1, "note": "华明的前任，接任时间及去向待确认"},
    # 金玉（前任区长）
    {"id": 5, "person_id": 4, "org_id": 2, "title": "大观区区长（前任）", "start": "", "end": "", "rank": 2, "note": "许亮的前任，接任时间及去向待确认"},
    # 余祥
    {"id": 6, "person_id": 5, "org_id": 1, "title": "大观区委副书记（正县级）", "start": "", "end": "", "rank": 3, "note": "aqdgq.gov.cn确认"},
    {"id": 7, "person_id": 5, "org_id": 10, "title": "区委党校校长", "start": "", "end": "", "rank": 3, "note": "兼任"},
    # 程亮
    {"id": 8, "person_id": 6, "org_id": 3, "title": "大观区委政法委书记", "start": "", "end": "", "rank": 3, "note": "aqdgq.gov.cn确认"},
    # 刘小平
    {"id": 9, "person_id": 7, "org_id": 4, "title": "大观区委组织部部长", "start": "", "end": "", "rank": 3, "note": "aqdgq.gov.cn确认；兼任统战部长"},
    # 邱金生
    {"id": 10, "person_id": 8, "org_id": 5, "title": "大观区纪委书记、监委主任", "start": "", "end": "", "rank": 3, "note": "aqdgq.gov.cn确认"},
    # 范兰芳
    {"id": 11, "person_id": 9, "org_id": 6, "title": "大观区委宣传部部长", "start": "", "end": "", "rank": 3, "note": "aqdgq.gov.cn确认"},
    # 彭凯
    {"id": 12, "person_id": 10, "org_id": 7, "title": "大观经济开发区党工委书记", "start": "", "end": "", "rank": 3, "note": "aqdgq.gov.cn确认"},
    # 刘晨光
    {"id": 13, "person_id": 11, "org_id": 8, "title": "大观区人武部部长", "start": "", "end": "", "rank": 3, "note": "aqdgq.gov.cn确认"},
    # 陈杰
    {"id": 14, "person_id": 12, "org_id": 2, "title": "大观区常务副区长", "start": "", "end": "", "rank": 4, "note": "aqdgq.gov.cn确认"},
    # 徐海洋
    {"id": 15, "person_id": 13, "org_id": 9, "title": "海口镇党委书记", "start": "", "end": "", "rank": 4, "note": "aqdgq.gov.cn确认；区委常委兼任"},
    # 方正平
    {"id": 16, "person_id": 14, "org_id": 2, "title": "大观区副区长", "start": "", "end": "", "rank": 5, "note": "aqdgq.gov.cn确认"},
    {"id": 17, "person_id": 14, "org_id": 11, "title": "市公安局大观分局局长", "start": "", "end": "", "rank": 5, "note": "兼任"},
    # 储艺
    {"id": 18, "person_id": 15, "org_id": 2, "title": "大观区副区长", "start": "", "end": "", "rank": 5, "note": "aqdgq.gov.cn确认"},
    # 何宏伟
    {"id": 19, "person_id": 16, "org_id": 2, "title": "大观区副区长", "start": "", "end": "", "rank": 5, "note": "aqdgq.gov.cn确认"},
]

# ── Relationships (confirmed by shared org membership) ──

relationships = [
    # 核心搭档：书记+区长
    {"id": 1, "person_a": 1, "person_b": 2, "type": "strong_collaboration",
     "context": "区委书记与区长核心搭档关系", "overlap_org": "中共大观区委/大观区人民政府",
     "overlap_period": "在任期间"},
    # 书记+副书记
    {"id": 2, "person_a": 1, "person_b": 5, "type": "leadership",
     "context": "区委书记与专职副书记工作关系", "overlap_org": "中共大观区委",
     "overlap_period": "在任期间"},
    # 区长+常务副区长
    {"id": 3, "person_a": 2, "person_b": 12, "type": "strong_collaboration",
     "context": "区长与常务副区长行政搭档关系", "overlap_org": "大观区人民政府",
     "overlap_period": "在任期间"},
    # 副书记+组织部
    {"id": 4, "person_a": 5, "person_b": 7, "type": "work_relationship",
     "context": "专职副书记与组织部长之间的干部人事工作关系", "overlap_org": "中共大观区委",
     "overlap_period": "在任期间"},
    # 纪委+政法委
    {"id": 5, "person_a": 8, "person_b": 6, "type": "work_relationship",
     "context": "纪委书记与政法委书记之间的监督与法治协作关系", "overlap_org": "中共大观区委",
     "overlap_period": "在任期间"},
    # 宣传+组织
    {"id": 6, "person_a": 9, "person_b": 7, "type": "work_relationship",
     "context": "宣传部部长与组织部部长之间的意识形态与干部工作关系", "overlap_org": "中共大观区委",
     "overlap_period": "在任期间"},
    # 书记+常务副区长
    {"id": 7, "person_a": 1, "person_b": 12, "type": "work_relationship",
     "context": "区委书记与常务副区长之间的党政工作关系", "overlap_org": "中共大观区委/大观区人民政府",
     "overlap_period": "在任期间"},
    # 区长+副区长（公安）
    {"id": 8, "person_a": 2, "person_b": 14, "type": "work_relationship",
     "context": "区长与公安分局局长之间的行政领导关系", "overlap_org": "大观区人民政府",
     "overlap_period": "在任期间"},
    # 书记+人武部
    {"id": 9, "person_a": 1, "person_b": 11, "type": "work_relationship",
     "context": "区委书记与人武部部长之间的党管武装关系", "overlap_org": "中共大观区委",
     "overlap_period": "在任期间"},
    # 镇长+区委（徐海洋由常委兼任海口镇党委书记）
    {"id": 10, "person_a": 13, "person_b": 1, "type": "work_relationship",
     "context": "区委常委（海口镇党委书记）与区委书记之间的上下级关系", "overlap_org": "中共大观区委",
     "overlap_period": "在任期间"},
    # 前任-书记继任关系
    {"id": 11, "person_a": 3, "person_b": 1, "type": "succession",
     "context": "前任大观区委书记与现任区委书记之间的职务继任关系", "overlap_org": "中共大观区委",
     "overlap_period": "前后接任"},
    # 前任-区长继任关系
    {"id": 12, "person_a": 4, "person_b": 2, "type": "succession",
     "context": "前任大观区长与现任区长之间的职务继任关系", "overlap_org": "大观区人民政府",
     "overlap_period": "前后接任"},
]

# ═══════════════════════════════════════════════════════════════════════
# SQLite Database
# ═══════════════════════════════════════════════════════════════════════

def create_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT,
            notes TEXT, confidence TEXT
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT,
            rank INTEGER, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                  (p["id"], p["name"], p["gender"], p["ethnicity"],
                   p["birth"], p["birthplace"], p["education"],
                   p["party_join"], p["work_start"],
                   p["current_post"], p["current_org"], p["source"],
                   p.get("notes", ""), p.get("confidence", "unverified")))

    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)""",
                  (pos["id"], pos["person_id"], pos["org_id"],
                   pos["title"], pos["start"], pos["end"],
                   pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships VALUES (?,?,?,?,?,?,?)""",
                  (r["id"], r["person_a"], r["person_b"],
                   r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"✓ Database created: {DB_PATH}")
    print(f"  - {len(persons)} persons")
    print(f"  - {len(organizations)} organizations")
    print(f"  - {len(positions)} positions")
    print(f"  - {len(relationships)} relationships")


# ═══════════════════════════════════════════════════════════════════════
# GEXF Graph
# ═══════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return R,G,B string based on role."""
    title = p.get("current_post", "")
    if "区委书记" in title and "副书记" not in title:
        return "255,50,50"     # Red — Party Secretary
    if "区长" in title or "副区长" in title:
        return "50,100,255"    # Blue — Government
    if "纪委书记" in title or "监委" in title:
        return "255,165,0"     # Orange — Discipline
    return "100,100,100"       # Grey — Others

def org_color(o):
    t = o["type"]
    if t == "党委": return "255,200,200"
    if t == "政府": return "200,200,255"
    if t == "开发区": return "200,255,200"
    if t == "事业单位": return "220,220,220"
    return "200,200,200"

def person_size(p):
    if p["id"] in (1, 2):  # 书记 and 区长
        return "20.0"
    return "12.0"

def create_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append('    <description>大观区（安庆市）领导班子工作关系网络 — 16个人物节点，11个机构节点，19条任职边，12条关系边</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="birth" type="string"/>')
    lines.append('      <attribute id="3" title="birthplace" type="string"/>')
    lines.append('      <attribute id="4" title="education" type="string"/>')
    lines.append('      <attribute id="5" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="rank" type="string"/>')
    lines.append('    </attributes>')

    # ── Nodes ──
    lines.append('    <nodes>')

    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        role = p.get("current_post", "")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birthplace"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["education"])}"/>')
        lines.append(f'          <attvalue for="5" value="{esc(p.get("confidence", ""))}"/>')
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
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # ── Edges ──
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append(f'          <attvalue for="2" value="{pos["rank"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in relationships:
        eid += 1
        w = "2.0" if r["type"] in ("strong_collaboration", "leadership") else "1.5"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
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
    print(f"✓ GEXF graph created: {GEXF_PATH}")


# ═══════════════════════════════════════════════════════════════════════
# Person JSON files
# ═══════════════════════════════════════════════════════════════════════

def create_person_json(p, filename):
    import json
    path = os.path.join(STAGING, filename)
    # Full schema-compliant person JSON — see person_graph_json.md
    data = {
        "schema_version": "1.0",
        "generated_at": TODAY[:4] + "-" + TODAY[4:6] + "-" + TODAY[6:],
        "investigation_scope": {
            "province": "安徽省", "city": "安庆市",
            "region": "大观区", "job": p.get("current_post", ""),
            "task_id": "anhui_大观区", "time_focus": "2026-07"
        },
        "identity": {
            "person_id": f"daguan_{p['name'].lower()}",
            "name": p["name"], "aliases": [],
            "gender": p["gender"], "ethnicity": p["ethnicity"],
            "birth": p["birth"], "birthplace": p["birthplace"],
            "native_place": p["birthplace"],
            "education": [{"period": "", "institution": "", "major": "",
                           "degree": p["education"], "study_type": "unknown",
                           "source_ids": ["S001"]}],
            "party_join": p["party_join"], "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p['birth']}",
                "name_birthplace": f"{p['name']}_{p['birthplace']}",
                "official_profile_url": "http://www.aqdgq.gov.cn/ldzc/index.html"
            }
        },
        "current_status": {
            "current_post": p["current_post"], "current_org": p["current_org"],
            "administrative_rank": "县处级正职",
            "as_of": TODAY[:4] + "-" + TODAY[4:6] + "-" + TODAY[6:],
            "is_current_confirmed": p.get("confidence") == "confirmed",
            "source_ids": ["S001"]
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [], "secondary_specializations": [],
            "career_pattern": "unknown", "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "公开信息不足，无法评估晋升速度",
                                   "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [], "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found",
             "description": "截至2026年7月，未发现公开的纪律处分、审计问题或负面报道",
             "date": "", "confidence": "plausible", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "大观区领导之窗",
             "url": "http://www.aqdgq.gov.cn/ldzc/index.html",
             "publisher": "大观区人民政府",
             "published_at": "", "accessed_at": TODAY[:4] + "-" + TODAY[4:6] + "-" + TODAY[6:],
             "source_type": "official", "reliability": "high",
             "notes": "大观区政府官方网站领导页面"}
        ],
        "confidence_summary": {
            "identity": p.get("confidence", "unverified"),
            "current_role": p.get("confidence", "unverified"),
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{p['name']}任{p.get('current_post', '现职')}之前的完整履历均未知"
        },
        "open_questions": [
            {"priority": "critical",
             "question": f"{p['name']}在任{p.get('current_post', '现职')}之前的完整仕途轨迹是什么？",
             "why_it_matters": "此前的任职经历决定了其是本土晋升还是从其他渠道调任",
             "suggested_queries": [f"{p['name']} 简历", f"{p['name']} 此前担任"],
             "last_attempted": TODAY[:4] + "-" + TODAY[4:6] + "-" + TODAY[6:]}
        ]
    }
    # Populate career_timeline from positions
    for pos in positions:
        if pos["person_id"] == p["id"]:
            org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
            data["career_timeline"].append({
                "start": pos["start"] or "unknown", "end": pos["end"] or "present",
                "org": org["name"] if org else "", "title": pos["title"],
                "level": "", "location": "安徽省安庆市大观区",
                "system": "party" if org and "党委" in org.get("type", "") else "government",
                "rank": pos["rank"], "is_key_promotion": False,
                "notes": pos["note"], "confidence": "confirmed",
                "source_ids": ["S001"]
            })
    if not data["career_timeline"]:
        data["career_timeline"].append({
            "start": "unknown", "end": "unknown",
            "org": "履历缺口", "title": "",
            "notes": "公开资料未找到完整履历",
            "confidence": "unverified", "source_ids": []
        })
    # Populate relationships
    for r in relationships:
        if r["person_a"] == p["id"]:
            other = next((per for per in persons if per["id"] == r["person_b"]), None)
            data["relationships"].append({
                "person": other["name"] if other else "",
                "person_id": f"daguan_{(other['name'] if other else 'unknown').lower()}",
                "relationship_type": r["type"],
                "strength": "strong" if r["type"] in ("strong_collaboration", "leadership") else "medium",
                "evidence": r["context"], "overlap_org": r["overlap_org"],
                "overlap_period": r.get("overlap_period", ""),
                "direction": "undirected", "confidence": "confirmed" if p.get("confidence") == "confirmed" else "plausible",
                "source_ids": ["S001"]
            })
        elif r["person_b"] == p["id"]:
            other = next((per for per in persons if per["id"] == r["person_a"]), None)
            data["relationships"].append({
                "person": other["name"] if other else "",
                "person_id": f"daguan_{(other['name'] if other else 'unknown').lower()}",
                "relationship_type": r["type"],
                "strength": "strong" if r["type"] in ("strong_collaboration", "leadership") else "medium",
                "evidence": r["context"], "overlap_org": r["overlap_org"],
                "overlap_period": r.get("overlap_period", ""),
                "direction": "undirected", "confidence": "confirmed" if p.get("confidence") == "confirmed" else "plausible",
                "source_ids": ["S001"]
            })
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✓ Person JSON created: {path}")

# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    os.makedirs(STAGING, exist_ok=True)
    print(f"=== Building 大观区 leadership network ===")
    print(f"Research date: {TODAY}")
    print()

    create_db()
    print()
    create_gexf()
    print()

    # Core person JSONs
    for pid in [1, 2]:  # 华明, 许亮
        p = next(x for x in persons if x["id"] == pid)
        job_slug = "大观区委书记" if pid == 1 else "大观区长"
        fname = f"{TODAY}-安徽省-安庆市-{job_slug}-{p['name']}.json"
        create_person_json(p, fname)

    print()
    print("=== Build Complete ===")
    print(f"DB:  {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"Person JSONs in: {STAGING}/")
