#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 大关县 (Daguan County) leadership network.
   昭通市, 云南省.

Data sources:
- www.daguan.gov.cn — official government profiles (all confirmed)
- 中国共产党大关县第十五次代表大会 (2026-06-26/28) — Party Congress reports
- 大关县人民代表大会常务委员会任免名单 (2025-05-29, 2026-03-27)
- 中共大关县委组织部干部任前公示 (2025-11-17, 2026-07-24)

Confidence: Current officeholders are CONFIRMED from official sources.
Career histories for most individuals beyond current role are UNKNOWN.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/大关县_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/大关县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders (IDs 1-2) ──
    {"id": 1, "name": "宋恩骑", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共大关县委书记", "current_org": "中共大关县委员会",
     "source": "https://www.daguan.gov.cn/contents/6751/226361.html"},
    {"id": 2, "name": "刀正强", "gender": "男", "ethnicity": "傣族",
     "birth": "1982-02", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大关县委副书记、县人民政府县长", "current_org": "大关县人民政府",
     "source": "https://www.daguan.gov.cn/contents/1587/66606.html"},

    # ── County Government Leadership Team ──
    {"id": 3, "name": "罗顺友", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-08", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大关县委常委、常务副县长", "current_org": "大关县人民政府",
     "source": "https://www.daguan.gov.cn/contents/1588/66616.html"},
    {"id": 4, "name": "毛兴安", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-06", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大关县副县长、县公安局局长", "current_org": "大关县人民政府",
     "source": "https://www.daguan.gov.cn/contents/1588/66608.html"},
    {"id": 5, "name": "王冰", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-12", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大关县委常委、副县长（挂职）", "current_org": "大关县人民政府",
     "source": "https://www.daguan.gov.cn/contents/1588/66612.html"},
    {"id": 6, "name": "赵康", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-01", "birthplace": "", "education": "硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大关县委常委、副县长（挂职）", "current_org": "大关县人民政府",
     "source": "https://www.daguan.gov.cn/contents/1588/222095.html"},
    {"id": 7, "name": "李志新", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-07", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大关县委常委、副县长（挂职）", "current_org": "大关县人民政府",
     "source": "https://www.daguan.gov.cn/contents/1588/66613.html"},
    {"id": 8, "name": "唐章雄", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-11", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大关县副县长", "current_org": "大关县人民政府",
     "source": "https://www.daguan.gov.cn/contents/1588/66615.html"},
    {"id": 9, "name": "吴昌虎", "gender": "男", "ethnicity": "汉族",
     "birth": "1986-02", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大关县副县长", "current_org": "大关县人民政府",
     "source": "https://www.daguan.gov.cn/contents/1588/225177.html"},
    {"id": 10, "name": "刘颖", "gender": "女", "ethnicity": "汉族",
     "birth": "1986-04", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大关县副县长", "current_org": "大关县人民政府",
     "source": "https://www.daguan.gov.cn/contents/1588/223004.html"},

    # ── Party Committee Leadership (partial) ──
    {"id": 11, "name": "魏国玺", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大关县委副书记", "current_org": "中共大关县委员会",
     "source": "https://www.daguan.gov.cn/contents/6751/226360.html"},

    # ── Other County Leaders ──
    {"id": 12, "name": "贾正友", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大关县领导", "current_org": "大关县",
     "source": "https://www.daguan.gov.cn/contents/6751/226525.html"},
    {"id": 13, "name": "罗章旭", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大关县领导", "current_org": "大关县",
     "source": "https://www.daguan.gov.cn/contents/6751/226525.html"},

    # ── Party Congress Executive Committee Members (关键常委/领导) ──
    {"id": 14, "name": "蔡风华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大关县领导", "current_org": "大关县",
     "source": "https://www.daguan.gov.cn/contents/6751/226360.html"},
    {"id": 15, "name": "郭亨友", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大关县领导", "current_org": "大关县",
     "source": "https://www.daguan.gov.cn/contents/6751/226360.html"},
    {"id": 16, "name": "祁华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大关县领导", "current_org": "大关县",
     "source": "https://www.daguan.gov.cn/contents/6751/226360.html"},
    {"id": 17, "name": "李飞", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大关县领导", "current_org": "大关县",
     "source": "https://www.daguan.gov.cn/contents/6751/226360.html"},
    {"id": 18, "name": "李沄镧", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大关县领导", "current_org": "大关县",
     "source": "https://www.daguan.gov.cn/contents/6751/226360.html"},
    {"id": 19, "name": "艾海峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大关县领导", "current_org": "大关县",
     "source": "https://www.daguan.gov.cn/contents/6751/226360.html"},
    {"id": 20, "name": "刘静", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "大关县领导", "current_org": "大关县",
     "source": "https://www.daguan.gov.cn/contents/6751/226360.html"},
]

organizations = [
    {"id": 1, "name": "中共大关县委员会", "type": "党委", "level": "县处级", "parent": "中共昭通市委员会", "location": "云南昭通大关"},
    {"id": 2, "name": "大关县人民政府", "type": "政府", "level": "县处级", "parent": "昭通市人民政府", "location": "云南昭通大关"},
    {"id": 3, "name": "大关县公安局", "type": "政府", "level": "县处级", "parent": "大关县人民政府", "location": "云南昭通大关"},
    {"id": 4, "name": "大关县人大常委会", "type": "人大", "level": "县处级", "parent": "昭通市人大常委会", "location": "云南昭通大关"},
    {"id": 5, "name": "大关县政协", "type": "政协", "level": "县处级", "parent": "昭通市政协", "location": "云南昭通大关"},
    {"id": 6, "name": "中共大关县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共昭通市纪律检查委员会", "location": "云南昭通大关"},
    {"id": 7, "name": "云南大关产业园区", "type": "开发区", "level": "县处级", "parent": "大关县人民政府", "location": "云南昭通大关"},
]

positions = [
    # ── 宋恩骑 (Party Secretary) ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共大关县委书记", "start": "2021?", "end": "present", "rank": "县处级正职", "note": "现任，2021-2026十四届，2026年6月连任十五届"},

    # ── 刀正强 (County Magistrate) ──
    {"id": 2, "person_id": 2, "org_id": 2, "title": "大关县委副书记、县人民政府县长", "start": "2021", "end": "present", "rank": "县处级正职", "note": "现任"},

    # ── 罗顺友 (Executive Deputy Magistrate) ──
    {"id": 3, "person_id": 3, "org_id": 2, "title": "大关县委常委、常务副县长", "start": "", "end": "present", "rank": "县处级副职", "note": "分管发改、财政、交通、应急等"},

    # ── 毛兴安 (Public Security) ──
    {"id": 4, "person_id": 4, "org_id": 2, "title": "大关县副县长、县公安局局长", "start": "", "end": "present", "rank": "县处级副职", "note": "现任"},
    {"id": 5, "person_id": 4, "org_id": 3, "title": "大关县公安局局长", "start": "", "end": "present", "rank": "县处级副职", "note": "主持公安局全面工作"},

    # ── 王冰 (Shanghai挂职) ──
    {"id": 6, "person_id": 5, "org_id": 2, "title": "大关县委常委、副县长（挂职）", "start": "", "end": "present", "rank": "挂职", "note": "东西部协作（上海闵行）"},

    # ── 赵康 (挂职) ──
    {"id": 7, "person_id": 6, "org_id": 2, "title": "大关县委常委、副县长（挂职）", "start": "", "end": "present", "rank": "挂职", "note": "自然资源、政务服务"},

    # ── 李志新 (中央党校挂职) ──
    {"id": 8, "person_id": 7, "org_id": 2, "title": "大关县委常委、副县长（挂职）", "start": "", "end": "present", "rank": "挂职", "note": "定点帮扶（中央党校）"},

    # ── 唐章雄 ──
    {"id": 9, "person_id": 8, "org_id": 2, "title": "大关县副县长", "start": "", "end": "present", "rank": "县处级副职", "note": "现任"},

    # ── 吴昌虎 ──
    {"id": 10, "person_id": 9, "org_id": 2, "title": "大关县副县长", "start": "", "end": "present", "rank": "县处级副职", "note": "教体、水务、市监、林草"},

    # ── 刘颖 ──
    {"id": 11, "person_id": 10, "org_id": 2, "title": "大关县副县长", "start": "", "end": "present", "rank": "县处级副职", "note": "人社、文旅、卫健、医保"},

    # ── 魏国玺 (Deputy Party Secretary) ──
    {"id": 12, "person_id": 11, "org_id": 1, "title": "大关县委副书记", "start": "", "end": "present", "rank": "县处级副职", "note": "现任，十五届党代会执行主席"},

    # ── 贾正友 ──
    {"id": 13, "person_id": 12, "org_id": 4, "title": "大关县领导（县人大）", "start": "", "end": "present", "rank": "县处级", "note": ""},

    # ── 罗章旭 ──
    {"id": 14, "person_id": 13, "org_id": 5, "title": "大关县领导（县政协）", "start": "", "end": "present", "rank": "县处级", "note": ""},

    # ── 蔡风华、郭亨友、祁华、李飞、李沄镧、艾海峰、刘静 ──
    {"id": 15, "person_id": 14, "org_id": 1, "title": "大关县领导（十五届党代会执行主席）", "start": "", "end": "present", "rank": "县处级", "note": ""},
    {"id": 16, "person_id": 15, "org_id": 1, "title": "大关县领导（十五届党代会执行主席）", "start": "", "end": "present", "rank": "县处级", "note": ""},
    {"id": 17, "person_id": 16, "org_id": 1, "title": "大关县领导（十五届党代会执行主席）", "start": "", "end": "present", "rank": "县处级", "note": ""},
    {"id": 18, "person_id": 17, "org_id": 1, "title": "大关县领导（十五届党代会执行主席）", "start": "", "end": "present", "rank": "县处级", "note": ""},
    {"id": 19, "person_id": 18, "org_id": 1, "title": "大关县领导（十五届党代会执行主席）", "start": "", "end": "present", "rank": "县处级", "note": ""},
    {"id": 20, "person_id": 19, "org_id": 1, "title": "大关县领导（十五届党代会执行主席）", "start": "", "end": "present", "rank": "县处级", "note": ""},
    {"id": 21, "person_id": 20, "org_id": 1, "title": "大关县领导（十五届党代会执行主席）", "start": "", "end": "present", "rank": "县处级", "note": ""},
]

relationships = [
    # ── Top Leadership Pair ──
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档", "context": "宋恩骑（县委书记）与刀正强（县长）为党政正职搭档", "overlap_org": "大关县", "overlap_period": "2021-至今"},

    # ── County Government Core ──
    {"id": 2, "person_a_id": 3, "person_b_id": 1, "type": "上下级", "context": "罗顺友（常务副县长）在宋恩骑领导下工作", "overlap_org": "大关县人民政府", "overlap_period": ""},
    {"id": 3, "person_a_id": 3, "person_b_id": 2, "type": "上下级", "context": "罗顺友协助刀正强县长分管审计工作", "overlap_org": "大关县人民政府", "overlap_period": ""},

    # ── Party Committee Connections ──
    {"id": 4, "person_a_id": 11, "person_b_id": 1, "type": "上下级", "context": "魏国玺（县委副书记）为宋恩骑的副手", "overlap_org": "中共大关县委员会", "overlap_period": ""},
    {"id": 5, "person_a_id": 11, "person_b_id": 2, "type": "同僚", "context": "魏国玺副书记与刀正强县长同为县委常委", "overlap_org": "中共大关县委员会", "overlap_period": ""},

    # ── 副县长之间的同僚关系 ──
    {"id": 6, "person_a_id": 4, "person_b_id": 3, "type": "同僚", "context": "毛兴安（公安局长）协助罗顺友负责安全生产", "overlap_org": "大关县人民政府", "overlap_period": ""},
    {"id": 7, "person_a_id": 8, "person_b_id": 9, "type": "同僚", "context": "唐章雄与吴昌虎同为副县长", "overlap_org": "大关县人民政府", "overlap_period": ""},
    {"id": 8, "person_a_id": 9, "person_b_id": 10, "type": "同僚", "context": "吴昌虎与刘颖同为副县长", "overlap_org": "大关县人民政府", "overlap_period": ""},
    {"id": 9, "person_a_id": 5, "person_b_id": 6, "type": "同僚", "context": "王冰与赵康同为挂职副县长", "overlap_org": "大关县人民政府", "overlap_period": ""},

    # ── 人大/政协与党委 ──
    {"id": 10, "person_a_id": 12, "person_b_id": 1, "type": "同僚", "context": "贾正友（人大）与宋恩骑（县委）", "overlap_org": "大关县", "overlap_period": ""},
    {"id": 11, "person_a_id": 13, "person_b_id": 1, "type": "同僚", "context": "罗章旭（政协）与宋恩骑（县委）", "overlap_org": "大关县", "overlap_period": ""},

    # ── 党代会执行主席团队 ──
    {"id": 12, "person_a_id": 14, "person_b_id": 1, "type": "同僚", "context": "蔡风波与宋恩骑同为十五届党代会执行主席", "overlap_org": "中共大关县委员会", "overlap_period": "2026-06"},
    {"id": 13, "person_a_id": 15, "person_b_id": 1, "type": "同僚", "context": "郭亨友与宋恩骑同为十五届党代会执行主席", "overlap_org": "中共大关县委员会", "overlap_period": "2026-06"},
    {"id": 14, "person_a_id": 16, "person_b_id": 1, "type": "同僚", "context": "祁华与宋恩骑同为十五届党代会执行主席", "overlap_org": "中共大关县委员会", "overlap_period": "2026-06"},
    {"id": 15, "person_a_id": 17, "person_b_id": 1, "type": "同僚", "context": "李飞与宋恩骑同为十五届党代会执行主席", "overlap_org": "中共大关县委员会", "overlap_period": "2026-06"},
    {"id": 16, "person_a_id": 18, "person_b_id": 1, "type": "同僚", "context": "李沄镧与宋恩骑同为十五届党代会执行主席", "overlap_org": "中共大关县委员会", "overlap_period": "2026-06"},
    {"id": 17, "person_a_id": 19, "person_b_id": 1, "type": "同僚", "context": "艾海峰与宋恩骑同为十五届党代会执行主席", "overlap_org": "中共大关县委员会", "overlap_period": "2026-06"},
    {"id": 18, "person_a_id": 20, "person_b_id": 1, "type": "同僚", "context": "刘静与宋恩骑同为十五届党代会执行主席", "overlap_org": "中共大关县委员会", "overlap_period": "2026-06"},
]


# ── BUILD SQLite DATABASE ────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE persons (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
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

CREATE TABLE organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

CREATE TABLE positions (
    id INTEGER PRIMARY KEY,
    person_id INTEGER NOT NULL,
    org_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE relationships (
    id INTEGER PRIMARY KEY,
    person_a_id INTEGER NOT NULL,
    person_b_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a_id) REFERENCES persons(id),
    FOREIGN KEY (person_b_id) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                 p["birthplace"], p["education"], p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)""",
                (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                 pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("""INSERT INTO relationships VALUES (?,?,?,?,?,?,?)""",
                (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
                 r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

# Summary stats
cur.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]

conn.close()
print(f"SQLite database written: {DB_PATH}")
print(f"  Persons: {person_count}")
print(f"  Organizations: {org_count}")
print(f"  Positions: {pos_count}")
print(f"  Relationships: {rel_count}")


# ── BUILD GEXF GRAPH ────────────────────────────────────────────────

today = datetime.now().strftime("%Y-%m-%d")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>大关县领导班子工作关系网络 - {today}</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# ── Attributes ──
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="category" title="Category" type="string"/>')
lines.append('      <attribute id="birth" title="Birth" type="string"/>')
lines.append('      <attribute id="education" title="Education" type="string"/>')
lines.append('      <attribute id="current_post" title="Current Post" type="string"/>')
lines.append('      <attribute id="source" title="Source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="context" title="Context" type="string"/>')
lines.append('      <attribute id="period" title="Period" type="string"/>')
lines.append('    </attributes>')

# ── Nodes: Persons ──
lines.append('    <nodes>')
for p in persons:
    if p["id"] in [1]:
        color = '#E03C31'  # red: Party Secretary
        size = 20.0
    elif p["id"] in [2]:
        color = '#2980B9'  # blue: government leader (县长)
        size = 20.0
    elif p["id"] in [3, 11, 12, 13]:
        color = '#2ECC71'  # green: key deputies
        size = 15.0
    elif p["id"] in [4]:
        color = '#E67E22'  # orange: public security
        size = 14.0
    elif p["id"] in [5, 6, 7]:
        color = '#9B59B6'  # purple: 挂职
        size = 12.0
    else:
        color = '#95A5A6'  # grey: others
        size = 12.0

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{esc(p["birth"])}"/>')
    lines.append(f'          <attvalue for="education" value="{esc(p["education"])}"/>')
    lines.append(f'          <attvalue for="current_post" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="source" value="{esc(p["source"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{int(color[1:3], 16)}" g="{int(color[3:5], 16)}" b="{int(color[5:7], 16)}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'      </node>')

# ── Nodes: Organizations ──
for o in organizations:
    oid = 1000 + o["id"]
    lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{esc(o["type"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="44" g="62" b="80"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'      </node>')
lines.append('    </nodes>')

# ── Edges ──
lines.append('    <edges>')
edge_id = 1

# person→organization (worked_at)
for pos in positions:
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="{edge_id}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{esc(pos["title"])}"/>')
    lines.append(f'          <attvalue for="period" value="{esc(pos["start"] or "?")} → {esc(pos["end"] or "今")}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

# person↔person (relationships)
for r in relationships:
    lines.append(f'      <edge id="{edge_id}" source="{r["person_a_id"]}" target="{r["person_b_id"]}" label="{esc(r["type"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="context" value="{esc(r["context"])}"/>')
    lines.append(f'          <attvalue for="period" value="{esc(r["overlap_period"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

total_nodes = len(persons) + len(organizations)
total_edges = len(positions) + len(relationships)
print(f"\nGEXF graph written: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} organizations = {total_nodes} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {total_edges} total")
print("\nDone!")