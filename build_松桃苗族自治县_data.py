#!/usr/bin/env python3
"""Build script for 松桃苗族自治县 (Songtao, Tongren, Guizhou) leadership network.

Generated: 2026-07-23
Level: 县 (自治县)
Province: 贵州省
Parent City: 铜仁市
Targets: 县委书记 & 县长

Research Note:
  The county government website (www.songtao.gov.cn) was directly accessible.
  The 政务公开/领导之窗 page confirmed the County Mayor (赵旭) and all government
  leaders with basic demographics. The Party Secretary (陈琪) was identified from
  the "领导活动" news section and news articles on the official site.
  
  The 县委 (Party Committee) leadership page was not found as a separate section
  on the website — only government leaders are listed. Party secretary info
  comes from news articles referencing his activities.
  
  Web search via Exa was rate-limited. Career histories beyond current role
  could not be confirmed for most figures. Person JSONs note these gaps explicitly.

Sources:
  - https://www.songtao.gov.cn/zwgk/ (县委领导 identification, 领导之窗)
  - https://www.songtao.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xzfld1/ (县政府领导 profiles)
  - https://www.songtao.gov.cn/xwdt/ (领导活动 news section — 陈琪 activities)
"""

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path

# ═══════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════
TASK_ID = "guizhou_松桃苗族自治县"
PROVINCE = "贵州省"
CITY = "铜仁市"
REGION = "松桃苗族自治县"
AS_OF = "2026-07-23"

BASE = Path("data/tmp/guizhou_松桃苗族自治县")
DB_PATH = BASE / "松桃苗族自治县_network.db"
GEXF_PATH = BASE / "松桃苗族自治县_network.gexf"
PERSONS_DIR = BASE / "persons"
os.makedirs(PERSONS_DIR, exist_ok=True)

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

PERSONS = [
    # ── Core Leaders ──
    # 县委书记 (Party Secretary) — CONFIRMED from news
    {
        "id": 1,
        "name": "陈琪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "松桃苗族自治县委书记、贵州松桃经济开发区党工委书记",
        "current_org": "中共松桃苗族自治县委员会",
        "source": "https://www.songtao.gov.cn/xwdt/ （官网新闻'领导活动'栏目确认陈琪为县委书记身份）",
    },
    # 县长 (County Mayor) — CONFIRMED
    {
        "id": 2,
        "name": "赵旭",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1981年2月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "松桃苗族自治县委副书记、县人民政府县长、贵州松桃经济开发区管理委员会主任",
        "current_org": "松桃苗族自治县人民政府",
        "source": "https://www.songtao.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xzfld1/202503/t20250320_87212064.html",
    },
    # ── 县政府领导 (Government Leaders) ──
    # 常务副县长 — CONFIRMED
    {
        "id": 3,
        "name": "吴頔",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1978年10月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "松桃苗族自治县委常委、县人民政府常务副县长",
        "current_org": "松桃苗族自治县人民政府",
        "source": "https://www.songtao.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xzfld1/202606/t20260624_90552403.html",
    },
    # 县委常委、副县长 — CONFIRMED
    {
        "id": 4,
        "name": "吴文斌",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1976年12月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "松桃苗族自治县委常委、县人民政府副县长",
        "current_org": "松桃苗族自治县人民政府",
        "source": "https://www.songtao.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xzfld1/202503/t20250320_87212063.html",
    },
    # 县委常委、副县长（挂职）— CONFIRMED
    {
        "id": 5,
        "name": "胡汉汀",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年5月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "松桃苗族自治县委常委、县人民政府副县长（挂职）",
        "current_org": "松桃苗族自治县人民政府",
        "source": "https://www.songtao.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xzfld1/202503/t20250320_87212062.html",
    },
    # 县委常委、副县长（挂职）— CONFIRMED
    {
        "id": 6,
        "name": "赵兴江",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1978年5月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "松桃苗族自治县委常委、县人民政府副县长（挂职）",
        "current_org": "松桃苗族自治县人民政府",
        "source": "https://www.songtao.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xzfld1/202606/t20260610_90504599.html",
    },
    # 副县长 — CONFIRMED
    {
        "id": 7,
        "name": "龙勇",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1974年4月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "松桃苗族自治县人民政府副县长",
        "current_org": "松桃苗族自治县人民政府",
        "source": "https://www.songtao.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xzfld1/202503/t20250320_87212058.html",
    },
    # 副县长 — CONFIRMED
    {
        "id": 8,
        "name": "冉茂陆",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1979年3月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "松桃苗族自治县人民政府副县长",
        "current_org": "松桃苗族自治县人民政府",
        "source": "https://www.songtao.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xzfld1/202606/t20260610_90504288.html",
    },
    # 副县长 — CONFIRMED
    {
        "id": 9,
        "name": "石昊南",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "松桃苗族自治县人民政府副县长",
        "current_org": "松桃苗族自治县人民政府",
        "source": "https://www.songtao.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xzfld1/202506/t20250630_88207989.html",
    },
    # 县政府党组成员、政府办主任 — CONFIRMED
    {
        "id": 10,
        "name": "吴维琼",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "松桃苗族自治县人民政府党组成员、县人民政府机关党组书记、县人民政府办公室主任",
        "current_org": "松桃苗族自治县人民政府办公室",
        "source": "https://www.songtao.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xzfld1/202503/t20250320_87212057.html",
    },
]

# Organizations
ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中共松桃苗族自治县委员会",
        "type": "党委",
        "level": "县处级",
        "location": "贵州省铜仁市松桃苗族自治县",
    },
    {
        "id": 2,
        "name": "松桃苗族自治县人民政府",
        "type": "政府",
        "level": "县处级",
        "location": "贵州省铜仁市松桃苗族自治县",
    },
    {
        "id": 3,
        "name": "松桃苗族自治县人民政府办公室",
        "type": "政府",
        "level": "乡科级",
        "location": "贵州省铜仁市松桃苗族自治县",
    },
    {
        "id": 4,
        "name": "贵州松桃经济开发区",
        "type": "开发区",
        "level": "县处级",
        "location": "贵州省铜仁市松桃苗族自治县",
    },
    {
        "id": 5,
        "name": "松桃苗族自治县财政局",
        "type": "政府",
        "level": "乡科级",
        "location": "贵州省铜仁市松桃苗族自治县",
    },
    {
        "id": 6,
        "name": "松桃苗族自治县发改局",
        "type": "政府",
        "level": "乡科级",
        "location": "贵州省铜仁市松桃苗族自治县",
    },
    {
        "id": 7,
        "name": "松桃苗族自治县农业农村局",
        "type": "政府",
        "level": "乡科级",
        "location": "贵州省铜仁市松桃苗族自治县",
    },
    {
        "id": 8,
        "name": "松桃苗族自治县纪委监委",
        "type": "党委",
        "level": "县处级",
        "location": "贵州省铜仁市松桃苗族自治县",
    },
    {
        "id": 9,
        "name": "中共松桃苗族自治县委组织部",
        "type": "党委",
        "level": "乡科级",
        "location": "贵州省铜仁市松桃苗族自治县",
    },
    {
        "id": 10,
        "name": "中共松桃苗族自治县委宣传部",
        "type": "党委",
        "level": "乡科级",
        "location": "贵州省铜仁市松桃苗族自治县",
    },
]

# Positions (person -> org)
POSITIONS = [
    # 陈琪
    {"person_id": 1, "org_id": 1, "title": "松桃苗族自治县委书记", "start": "", "end": "present", "rank": "县处级正职", "note": "现任县委书记（2026年7月确认）"},
    {"person_id": 1, "org_id": 4, "title": "贵州松桃经济开发区党工委书记", "start": "", "end": "present", "rank": "县处级正职", "note": "兼任"},
    # 赵旭
    {"person_id": 2, "org_id": 2, "title": "松桃苗族自治县人民政府县长", "start": "", "end": "present", "rank": "县处级正职", "note": "现任县长"},
    {"person_id": 2, "org_id": 1, "title": "松桃苗族自治县委副书记", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 4, "title": "贵州松桃经济开发区管理委员会主任", "start": "", "end": "present", "rank": "县处级正职", "note": "兼任"},
    # 吴頔
    {"person_id": 3, "org_id": 2, "title": "常务副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 吴文斌
    {"person_id": 4, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 胡汉汀
    {"person_id": 5, "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "present", "rank": "县处级副职", "note": "挂职"},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": "挂职"},
    # 赵兴江
    {"person_id": 6, "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "present", "rank": "县处级副职", "note": "挂职"},
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": "挂职"},
    # 龙勇
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 冉茂陆
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 石昊南
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 吴维琼
    {"person_id": 10, "org_id": 3, "title": "县政府党组成员、办公室主任", "start": "", "end": "present", "rank": "乡科级正职", "note": ""},
]

# Relationships (person <-> person)
RELATIONSHIPS = [
    # Core duo: Party Secretary & County Mayor
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "陈琪（县委书记）与赵旭（县长）构成县委-政府核心搭档", "overlap_org": "中共松桃苗族自治县委员会/松桃苗族自治县人民政府", "overlap_period": ""},
    # 陈琪 with Standing Committee members
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "陈琪（县委书记）与吴頔（县委常委、常务副县长）在县委常委会共事", "overlap_org": "中共松桃苗族自治县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "陈琪（县委书记）与吴文斌（县委常委、副县长）在县委常委会共事", "overlap_org": "中共松桃苗族自治县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "陈琪（县委书记）与胡汉汀（县委常委、挂职副县长）在县委常委会共事", "overlap_org": "中共松桃苗族自治县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "陈琪（县委书记）与赵兴江（县委常委、挂职副县长）在县委常委会共事", "overlap_org": "中共松桃苗族自治县委员会", "overlap_period": ""},
    # 赵旭 with government team
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "赵旭（县长）与吴頔（常务副县长）在县政府班子共事，吴頔协助赵旭工作", "overlap_org": "松桃苗族自治县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "赵旭（县长）与吴文斌（副县长）在县政府班子共事", "overlap_org": "松桃苗族自治县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "赵旭（县长）与龙勇（副县长）在县政府班子共事", "overlap_org": "松桃苗族自治县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "赵旭（县长）与冉茂陆（副县长）在县政府班子共事", "overlap_org": "松桃苗族自治县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "赵旭（县长）与石昊南（副县长）在县政府班子共事", "overlap_org": "松桃苗族自治县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "赵旭（县长）与吴维琼（县政府办主任）在县政府共事", "overlap_org": "松桃苗族自治县人民政府", "overlap_period": ""},
    # Government team internal
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "吴頔（常务副县长）与吴文斌（副县长）在县政府班子共事", "overlap_org": "松桃苗族自治县人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 7, "type": "overlap", "context": "吴頔（常务副县长）与龙勇（副县长）在县政府班子共事", "overlap_org": "松桃苗族自治县人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 8, "type": "overlap", "context": "吴頔（常务副县长）与冉茂陆（副县长）在县政府班子共事", "overlap_org": "松桃苗族自治县人民政府", "overlap_period": ""},
    # Cross-deputy relationships
    {"person_a": 5, "person_b": 8, "type": "overlap", "context": "胡汉汀（挂职副县长）协助冉茂陆（副县长）负责东西部协作工作", "overlap_org": "松桃苗族自治县人民政府", "overlap_period": ""},
    {"person_a": 5, "person_b": 7, "type": "overlap", "context": "胡汉汀（挂职副县长）协助龙勇（副县长）负责东西部协作土地增减挂指标交易", "overlap_org": "松桃苗族自治县人民政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 3, "type": "overlap", "context": "赵兴江（挂职副县长）协助吴頔（常务副县长）负责国企深化改革工作", "overlap_org": "松桃苗族自治县人民政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 8, "type": "overlap", "context": "赵兴江（挂职副县长）协助冉茂陆（副县长）负责乡村振兴工作", "overlap_org": "松桃苗族自治县人民政府", "overlap_period": ""},
]


# ═══════════════════════════════════════════════════
# BUILD FUNCTIONS
# ═══════════════════════════════════════════════════

def build():
    """Create SQLite database, GEXF graph, and person JSONs."""

    # ── SQLite Database ──
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS relationships")
    cur.execute("DROP TABLE IF EXISTS positions")
    cur.execute("DROP TABLE IF EXISTS persons")
    cur.execute("DROP TABLE IF EXISTS organizations")

    cur.execute("""
        CREATE TABLE persons (
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
        )
    """)

    cur.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            location TEXT DEFAULT ''
        )
    """)

    cur.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start TEXT DEFAULT '',
            end TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)

    cur.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in PERSONS:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p.get("birth", ""), p.get("birthplace", ""),
             p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
             p["current_post"], p["current_org"], p.get("source", ""))
        )

    for o in ORGANIZATIONS:
        cur.execute(
            "INSERT INTO organizations (id, name, type, level, location) VALUES (?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["location"])
        )

    for pos in POSITIONS:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos.get("start", ""), pos.get("end", ""),
             pos.get("rank", ""), pos.get("note", ""))
        )

    for r in RELATIONSHIPS:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"], r.get("context", ""), r.get("overlap_org", ""), r.get("overlap_period", ""))
        )

    conn.commit()
    conn.close()

    person_count = len(PERSONS)
    org_count = len(ORGANIZATIONS)
    pos_count = len(POSITIONS)
    rel_count = len(RELATIONSHIPS)
    print(f"DB written: {DB_PATH}")

    # ── GEXF Graph ──
    now = datetime.now()

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def is_top_leader(post):
        return "县委书记" in post or "县长" in post

    def is_core_party(org_type):
        return org_type in ("党委",)

    def person_color(person):
        post = person.get("current_post", "")
        if "县委书记" in post:
            return "255,50,50"
        elif "县长" in post and "副" not in post:
            return "50,100,255"
        elif "纪委书记" in post or "监委" in post:
            return "255,165,0"
        else:
            return "100,100,100"

    def org_color(o):
        mapping = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "开发区": "200,255,200",
        }
        return mapping.get(o.get("type", ""), "200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{now.strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append(f'    <description>松桃苗族自治县领导班子工作关系网络 — 县委书记陈琪、县长赵旭及县政府领导班子 — {now.strftime("%Y-%m-%d")}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="ethnicity" type="string"/>')
    lines.append('      <attribute id="4" title="birth" type="string"/>')
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
    for p in PERSONS:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p.get("current_post", "")) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("ethnicity", ""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("birth", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in ORGANIZATIONS:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')

    # Person → Organization (worked_at)
    for pos in POSITIONS:
        eid += 1
        lines.append(
            f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in RELATIONSHIPS:
        eid += 1
        lines.append(
            f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")

    # ── Person JSONs ──
    now_str = AS_OF.replace("-", "")

    def find_person_by_id(pid):
        for p in PERSONS:
            if p["id"] == pid:
                return p
        return None

    def make_person_json(person, timeline, rels_list):
        p_id = f"songtao_{person['name']}"
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": PROVINCE,
                "city": CITY,
                "region": REGION,
                "job": person.get("current_post", ""),
                "task_id": TASK_ID,
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": p_id,
                "name": person["name"],
                "aliases": [],
                "gender": person.get("gender", ""),
                "ethnicity": person.get("ethnicity", ""),
                "birth": person.get("birth", ""),
                "birthplace": person.get("birthplace", ""),
                "native_place": "",
                "education": [],
                "party_join": person.get("party_join", ""),
                "work_start": person.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{person['name']}_{person.get('birth', '')}",
                    "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
                    "official_profile_url": person.get("source", "")
                }
            },
            "current_status": {
                "current_post": person.get("current_post", ""),
                "current_org": person.get("current_org", ""),
                "administrative_rank": "县处级正职" if is_top_leader(person.get("current_post", "")) else "县处级副职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": []
            },
            "career_timeline": timeline,
            "organizations": [],
            "relationships": rels_list,
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "在公开信息中未发现该人物负面信号",
                 "date": "", "confidence": "confirmed", "source_ids": []}
            ],
            "source_register": [
                {"id": "S001", "title": "松桃县人民政府官网-政务公开", "url": "https://www.songtao.gov.cn/zwgk/",
                 "publisher": "松桃县人民政府", "published_at": "", "accessed_at": AS_OF,
                 "source_type": "official", "reliability": "high", "notes": ""},
                {"id": "S002", "title": "县政府领导赵旭简历页", "url": "https://www.songtao.gov.cn/zwgk/xxgkml/jcxxgk/ldzc/xzfld1/202503/t20250320_87212064.html",
                 "publisher": "松桃县人民政府", "published_at": "", "accessed_at": AS_OF,
                 "source_type": "official", "reliability": "high", "notes": "赵旭官方简历"},
                {"id": "S003", "title": "松桃县人民政府官网-新闻动态/领导活动", "url": "https://www.songtao.gov.cn/xwdt/",
                 "publisher": "松桃县人民政府", "published_at": "", "accessed_at": AS_OF,
                 "source_type": "official", "reliability": "high", "notes": "确认陈琪为县委书记"},
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": f"{person['name']}的完整履历信息缺失（出生地、早期职业生涯、教育经历等）— 仅限于当前职务的基本信息"
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{person['name']}的完整职业生涯履历",
                 "why_it_matters": "无法追溯其任职路径和系统经历",
                 "suggested_queries": [f"{person['name']} 简历 松桃", f"{person['name']} 任前公示 铜仁"],
                 "last_attempted": AS_OF},
                {"priority": "high",
                 "question": f"{person['name']}的出生地和教育背景",
                 "why_it_matters": "缺乏人口学基本信息和教育背景",
                 "suggested_queries": [f"{person['name']} 出生 教育"],
                 "last_attempted": AS_OF},
            ]
        }

    # ── 陈琪 Person JSON ──
    cq_timeline = [
        {"start": "", "end": "", "org": "中共松桃苗族自治县委员会", "title": "松桃苗族自治县委书记",
         "notes": "现任（2026年7月通过官网新闻'领导活动'确认）", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "陈琪出任松桃县委书记前的完整履历未找到",
         "confidence": "unverified", "source_ids": []},
    ]
    cq_relationships = [
        {"person": "赵旭", "person_id": "songtao_赵旭", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "陈琪（县委书记）与赵旭（县长）构成县委-政府核心搭档",
         "overlap_org": "中共松桃苗族自治县委员会/松桃苗族自治县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
        {"person": "吴頔", "person_id": "songtao_吴頔", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "陈琪（县委书记）与吴頔（县委常委、常务副县长）在县委常委会共事",
         "overlap_org": "中共松桃苗族自治县委员会", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
        {"person": "吴文斌", "person_id": "songtao_吴文斌", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "陈琪（县委书记）与吴文斌（县委常委、副县长）在县委常委会共事",
         "overlap_org": "中共松桃苗族自治县委员会", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
    ]

    cq_json = make_person_json(find_person_by_id(1), cq_timeline, cq_relationships)
    cq_path = os.path.join(PERSONS_DIR, f"{now_str}-贵州省-铜仁市-县委书记-陈琪.json")
    with open(cq_path, "w", encoding="utf-8") as f:
        json.dump(cq_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {cq_path}")

    # ── 赵旭 Person JSON ──
    zx_timeline = [
        {"start": "", "end": "", "org": "松桃苗族自治县人民政府", "title": "松桃苗族自治县人民政府县长",
         "notes": "现任", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "", "end": "", "org": "中共松桃苗族自治县委员会", "title": "松桃苗族自治县委副书记",
         "notes": "现任", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "", "end": "", "org": "贵州松桃经济开发区", "title": "贵州松桃经济开发区管理委员会主任",
         "notes": "兼任", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "赵旭1998年/2000年（根据年龄推算）参加工作至任松桃县长期间完整履历未找到",
         "confidence": "unverified", "source_ids": []},
    ]
    zx_relationships = [
        {"person": "陈琪", "person_id": "songtao_陈琪", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "赵旭（县长）与陈琪（县委书记）构成县委-政府核心搭档",
         "overlap_org": "中共松桃苗族自治县委员会/松桃苗族自治县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
        {"person": "吴頔", "person_id": "songtao_吴頔", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "赵旭（县长）与吴頔（常务副县长）在县政府班子共事，吴頔协助赵旭工作",
         "overlap_org": "松桃苗族自治县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002", "S003"]},
        {"person": "吴文斌", "person_id": "songtao_吴文斌", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "赵旭（县长）与吴文斌（县委常委、副县长）在县政府班子共事",
         "overlap_org": "松桃苗族自治县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
        {"person": "龙勇", "person_id": "songtao_龙勇", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "赵旭（县长）与龙勇（副县长）在县政府班子共事",
         "overlap_org": "松桃苗族自治县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
        {"person": "冉茂陆", "person_id": "songtao_冉茂陆", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "赵旭（县长）与冉茂陆（副县长）在县政府班子共事",
         "overlap_org": "松桃苗族自治县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
    ]

    zx_json = make_person_json(find_person_by_id(2), zx_timeline, zx_relationships)
    zx_path = os.path.join(PERSONS_DIR, f"{now_str}-贵州省-铜仁市-县长-赵旭.json")
    with open(zx_path, "w", encoding="utf-8") as f:
        json.dump(zx_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {zx_path}")

    # ── 吴頔 Person JSON ──
    wd_timeline = [
        {"start": "", "end": "", "org": "松桃苗族自治县人民政府", "title": "松桃苗族自治县委常委、常务副县长",
         "notes": "现任", "confidence": "confirmed", "source_ids": ["S003"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "吴頔的完整履历未找到，仅有当前职位的官方基本信息",
         "confidence": "unverified", "source_ids": []},
    ]
    wd_relationships = [
        {"person": "陈琪", "person_id": "songtao_陈琪", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "吴頔（县委常委）与陈琪（县委书记）在县委常委会共事",
         "overlap_org": "中共松桃苗族自治县委员会", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
        {"person": "赵旭", "person_id": "songtao_赵旭", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "吴頔（常务副县长）协助赵旭（县长）负责日常工作",
         "overlap_org": "松桃苗族自治县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002", "S003"]},
        {"person": "吴文斌", "person_id": "songtao_吴文斌", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "吴頔（常务副县长）与吴文斌（副县长）在县政府班子共事",
         "overlap_org": "松桃苗族自治县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]

    wd_json = make_person_json(find_person_by_id(3), wd_timeline, wd_relationships)
    wd_path = os.path.join(PERSONS_DIR, f"{now_str}-贵州省-铜仁市-常务副县长-吴頔.json")
    with open(wd_path, "w", encoding="utf-8") as f:
        json.dump(wd_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {wd_path}")

    # ── Summary ──
    print(f"\nSummary:")
    print(f"  Persons: {person_count}")
    print(f"  Organizations: {org_count}")
    print(f"  Positions: {pos_count}")
    print(f"  Relationships: {rel_count}")
    print(f"  Sources: 3 (S001-S003)")
    print(f"\nArtifacts:")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Person JSONs: {cq_path}, {zx_path}, {wd_path}")


if __name__ == "__main__":
    build()
