#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 正阳县 (Zhengyang County), 驻马店市, 河南省.

Investigation date: 2026-07-24
Task ID: henan_正阳县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - https://www.zhengyang.gov.cn/ — official government website
  - Government leadership page: /zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202410/t20241022_319958.html (张燕 bio)
  - Government leadership page: /zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202410/t20241022_319957.html (梁浩 bio)
  - Government leadership page: /zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202410/t20241022_319955.html (翟剑毅 bio)
  - Government leadership page: /zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202410/t20241022_319953.html (陈喜中 bio)
  - Government leadership page: /zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202410/t20241022_319951.html (郑永 bio)
  - Government leadership page: /zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202504/t20250422_602983.html (马兴立 bio)
  - Government leadership page: /zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202604/t20260427_698389.html (王红涛 bio)
  - News: /zwyw/zwyw/202607/t20260720_712634.html (县委常委扩大会议, confirmed 刘磊 as 县委书记)
  - News: /zwyw/zwyw/202607/t20260720_712632.html (县委常委会, confirmed 刘磊 presiding, full standing committee roster)

Confidence notes:
  - 刘磊 (县委书记): confirmed via multiple official news articles (2026-07-17 县委常委扩大会议, 县委常委会).
    Full biography (birth year, education, career timeline) unverified.
  - 张燕 (县长): confirmed via official portrait bio page. Female, 研究生学历, 中共党员.
    Full biography (birth year, birthplace, career timeline) unverified.
  - Government deputy leadership team: 7 bios confirmed from official site.
  - Party standing committee: partial — 9 members named from news, but some roles unknown.
  - Predecessor information: not yet researched.
  - This is a partial-evidence artifact: core leader identities and government team are
    well-documented; party committee detailed bios are incomplete.
"""

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "正阳县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# ── Helper: ID offset for orgs ─────────────────────────────────────────────
ORG_OFFSET = 100000

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "刘磊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共正阳县委员会",
        "source": "Official news confirmed 刘磊 as 县委书记 presiding 县委常委扩大会议 (2026-07-17): https://www.zhengyang.gov.cn/zwyw/zwyw/202607/t20260720_712634.html"
    },
    {
        "id": 2,
        "name": "张燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "正阳县人民政府",
        "source": "Official bio: https://www.zhengyang.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202410/t20241022_319958.html"
    },
    # ═══════ Government Leadership ═══════
    {
        "id": 3,
        "name": "梁浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981.06",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "正阳县人民政府",
        "source": "Official bio: https://www.zhengyang.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202410/t20241022_319957.html"
    },
    {
        "id": 4,
        "name": "翟剑毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982.09",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长、副县长",
        "current_org": "中共正阳县委宣传部",
        "source": "Official bio: https://www.zhengyang.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202410/t20241022_319955.html"
    },
    {
        "id": 5,
        "name": "陈喜中",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974.02",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "正阳县公安局",
        "source": "Official bio: https://www.zhengyang.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202410/t20241022_319953.html"
    },
    {
        "id": 6,
        "name": "郑永",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979.12",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "正阳县人民政府",
        "source": "Official bio: https://www.zhengyang.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202410/t20241022_319951.html"
    },
    {
        "id": 7,
        "name": "马兴立",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985.06",
        "birthplace": "",
        "education": "农学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "正阳县人民政府",
        "source": "Official bio: https://www.zhengyang.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202504/t20250422_602983.html"
    },
    {
        "id": 8,
        "name": "王红涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987.07",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "正阳县人民政府",
        "source": "Official bio: https://www.zhengyang.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202604/t20260427_698389.html"
    },
    # ═══════ Standing Committee (additional members from news) ═══════
    {
        "id": 9,
        "name": "徐永辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共正阳县委员会",
        "source": "Confirmed from 县委常委会 meeting (2026-07-17): https://www.zhengyang.gov.cn/zwyw/zwyw/202607/t20260720_712632.html"
    },
    {
        "id": 10,
        "name": "刘楠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共正阳县委员会",
        "source": "Confirmed from 县委常委会 meeting (2026-07-17): https://www.zhengyang.gov.cn/zwyw/zwyw/202607/t20260720_712632.html"
    },
    {
        "id": 11,
        "name": "刘帅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共正阳县委员会",
        "source": "Confirmed from 县委常委会 meeting (2026-07-17): https://www.zhengyang.gov.cn/zwyw/zwyw/202607/t20260720_712632.html"
    },
    {
        "id": 12,
        "name": "刘天坤",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共正阳县委员会",
        "source": "Confirmed from 县委常委会 meeting (2026-07-17): https://www.zhengyang.gov.cn/zwyw/zwyw/202607/t20260720_712632.html"
    },
    {
        "id": 13,
        "name": "孙道怀",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共正阳县委员会",
        "source": "Confirmed from 县委常委会 meeting (2026-07-17): https://www.zhengyang.gov.cn/zwyw/zwyw/202607/t20260720_712632.html"
    },
    {
        "id": 14,
        "name": "杨永",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共正阳县委员会",
        "source": "Confirmed from 县委常委会 meeting (2026-07-17): https://www.zhengyang.gov.cn/zwyw/zwyw/202607/t20260720_712632.html"
    },
    # ═══════ People's Congress & Political Consultative ═══════
    {
        "id": 15,
        "name": "胡敬忠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "正阳县人大常委会",
        "source": "Confirmed from 县委常委会 meeting (2026-07-17): https://www.zhengyang.gov.cn/zwyw/zwyw/202607/t20260720_712632.html"
    },
    {
        "id": 16,
        "name": "李迎春",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协正阳县委员会",
        "source": "Confirmed from 县委常委会 meeting (2026-07-17): https://www.zhengyang.gov.cn/zwyw/zwyw/202607/t20260720_712632.html"
    },
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {"id": ORG_OFFSET + 1, "name": "中共正阳县委员会", "type": "党委", "level": "县处级", "parent": "中共驻马店市委", "location": "河南省驻马店市正阳县"},
    {"id": ORG_OFFSET + 2, "name": "正阳县人民政府", "type": "政府", "level": "县处级", "parent": "驻马店市人民政府", "location": "河南省驻马店市正阳县"},
    {"id": ORG_OFFSET + 3, "name": "中共正阳县委宣传部", "type": "党委", "level": "正科级", "parent": "中共正阳县委员会", "location": "河南省驻马店市正阳县"},
    {"id": ORG_OFFSET + 4, "name": "正阳县公安局", "type": "政府", "level": "正科级", "parent": "正阳县人民政府", "location": "河南省驻马店市正阳县"},
    {"id": ORG_OFFSET + 5, "name": "正阳县人大常委会", "type": "人大", "level": "县处级", "parent": "驻马店市人大常委会", "location": "河南省驻马店市正阳县"},
    {"id": ORG_OFFSET + 6, "name": "政协正阳县委员会", "type": "政协", "level": "县处级", "parent": "政协驻马店市委员会", "location": "河南省驻马店市正阳县"},
]

# ── Positions ───────────────────────────────────────────────────────────────
positions = [
    # 刘磊
    {"person_id": 1, "org_id": ORG_OFFSET + 1, "title": "县委书记", "start": "", "end": "present", "rank": "县处级正职", "note": ""},
    # 张燕
    {"person_id": 2, "org_id": ORG_OFFSET + 1, "title": "县委副书记", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": ORG_OFFSET + 2, "title": "县长", "start": "", "end": "present", "rank": "县处级正职", "note": ""},
    # 梁浩
    {"person_id": 3, "org_id": ORG_OFFSET + 1, "title": "县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": ORG_OFFSET + 2, "title": "常务副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 翟剑毅
    {"person_id": 4, "org_id": ORG_OFFSET + 1, "title": "县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": ORG_OFFSET + 3, "title": "宣传部部长", "start": "", "end": "present", "rank": "正科级", "note": ""},
    {"person_id": 4, "org_id": ORG_OFFSET + 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 陈喜中
    {"person_id": 5, "org_id": ORG_OFFSET + 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": "兼县公安局局长"},
    {"person_id": 5, "org_id": ORG_OFFSET + 4, "title": "县公安局局长", "start": "", "end": "present", "rank": "正科级", "note": ""},
    # 郑永
    {"person_id": 6, "org_id": ORG_OFFSET + 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 马兴立
    {"person_id": 7, "org_id": ORG_OFFSET + 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 王红涛
    {"person_id": 8, "org_id": ORG_OFFSET + 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # Standing committee members
    {"person_id": 9, "org_id": ORG_OFFSET + 1, "title": "县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": ORG_OFFSET + 1, "title": "县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": ORG_OFFSET + 1, "title": "县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": ORG_OFFSET + 1, "title": "县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": ORG_OFFSET + 1, "title": "县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 14, "org_id": ORG_OFFSET + 1, "title": "县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 胡敬忠
    {"person_id": 15, "org_id": ORG_OFFSET + 5, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "县处级正职", "note": ""},
    # 李迎春
    {"person_id": 16, "org_id": ORG_OFFSET + 6, "title": "县政协主席", "start": "", "end": "present", "rank": "县处级正职", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "刘磊(县委书记)与张燕(县委副书记、县长)为县委主要党政领导搭档",
        "overlap_org": 100001,
        "overlap_period": "当前",
        "source": "https://www.zhengyang.gov.cn/zwyw/zwyw/202607/t20260720_712634.html"
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "刘磊(县委书记)与梁浩(县委常委、常务副县长)为上下级关系",
        "overlap_org": 100001,
        "overlap_period": "当前",
        "source": "https://www.zhengyang.gov.cn/zwyw/zwyw/202607/t20260720_712632.html"
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "superior_subordinate",
        "context": "张燕(县长)与梁浩(常务副县长)为县政府主要正副职搭档",
        "overlap_org": 100002,
        "overlap_period": "当前",
        "source": "https://www.zhengyang.gov.cn/zwgk/"
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "superior_subordinate",
        "context": "张燕(县长)与翟剑毅(副县长)为县政府正副职",
        "overlap_org": 100002,
        "overlap_period": "当前",
        "source": "https://www.zhengyang.gov.cn/zwgk/"
    },
    {
        "person_a": 2, "person_b": 5,
        "type": "superior_subordinate",
        "context": "张燕(县长)与陈喜中(副县长)为县政府正副职",
        "overlap_org": 100002,
        "overlap_period": "当前",
        "source": "https://www.zhengyang.gov.cn/zwgk/"
    },
    {
        "person_a": 2, "person_b": 6,
        "type": "superior_subordinate",
        "context": "张燕(县长)与郑永(副县长)为县政府正副职",
        "overlap_org": 100002,
        "overlap_period": "当前",
        "source": "https://www.zhengyang.gov.cn/zwgk/"
    },
    {
        "person_a": 2, "person_b": 7,
        "type": "superior_subordinate",
        "context": "张燕(县长)与马兴立(副县长)为县政府正副职",
        "overlap_org": 100002,
        "overlap_period": "当前",
        "source": "https://www.zhengyang.gov.cn/zwgk/"
    },
    {
        "person_a": 2, "person_b": 8,
        "type": "superior_subordinate",
        "context": "张燕(县长)与王红涛(副县长)为县政府正副职",
        "overlap_org": 100002,
        "overlap_period": "当前",
        "source": "https://www.zhengyang.gov.cn/zwgk/"
    },
]

# ── GEXF string-formatting helpers ──────────────────────────────────────────
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    role = p.get("current_post", "")
    if "县委书记" in role or "县委" in role and "书记" in role:
        return "255,50,50"
    if "县长" in role:
        return "50,100,255"
    if "副县长" in role or "常务" in role:
        return "80,130,255"
    if "县人大常委会主任" in role:
        return "200,255,255"
    if "县政协主席" in role:
        return "255,240,200"
    return "100,100,100"

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
    return "200,200,200"

# ── SQLite Database ─────────────────────────────────────────────────────────
def build_db():
    import sqlite3
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    cur.execute("""CREATE TABLE persons(
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    cur.execute("""CREATE TABLE organizations(
        id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    cur.execute("""CREATE TABLE positions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER, title TEXT,
        start TEXT, "end" TEXT, rank TEXT, note TEXT
    )""")
    cur.execute("""CREATE TABLE relationships(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER, type TEXT,
        context TEXT, overlap_org INTEGER, overlap_period TEXT,
        source TEXT
    )""")

    for p in persons:
        cur.execute("INSERT INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                    (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                     p["birthplace"], p["education"], p["party_join"],
                     p["work_start"], p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        cur.execute("INSERT INTO organizations VALUES(?,?,?,?,?,?)",
                    (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        cur.execute("INSERT INTO positions(person_id, org_id, title, start, end, rank, note) VALUES(?,?,?,?,?,?,?)",
                    (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))
    for r in relationships:
        cur.execute("INSERT INTO relationships(person_a, person_b, type, context, overlap_org, overlap_period, source) VALUES(?,?,?,?,?,?,?)",
                    (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"], r["source"]))

    conn.commit()
    conn.close()
    print(f"  Database written: {DB_PATH}")

# ── GEXF Graph ──────────────────────────────────────────────────────────────
def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append(f'    <description>正阳县 (Zhengyang County) leadership network - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="label" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if p["id"] in (1, 2) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Org nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges: person -> organization
    lines.append('    <edges>')
    eid = 1
    for pos in positions:
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Edges: person <-> person (relationships)
    for r in relationships:
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {GEXF_PATH}")

# ── Main ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Building 正阳县 leadership network...")
    build_db()
    build_gexf()

    # Write person JSONs
    for p in persons:
        if p["id"] in (1, 2):
            fn = f"{TODAY}-河南省-驻马店市-{p['current_post']}-{p['name']}.json"
            path = PERSONS_DIR / fn
            if not path.exists():
                print(f"  Person JSON not auto-generated: {fn}")
                print(f"    (person JSONs are created manually per schema)")
    print(f"  Build complete! DB: {DB_PATH}, GEXF: {GEXF_PATH}")
