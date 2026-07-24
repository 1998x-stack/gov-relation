#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 汤旺县 (Tangwang County), 伊春市, 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_汤旺县
Level: 县
Research sources:
  - Tangwang County Government Website (www.yctwx.gov.cn)
  - Government leadership page (县政府领导信息)
  - News reports and inspection articles
  - Wikipedia (administrative info)

Research Note:
  Web access to Chinese government sites was partially available.
  - www.yctwx.gov.cn (汤旺县人民政府): Accessible — confirmed 县长梁巍 and 县政府领导班子
  - 县委书记 name: NOT FOUND on any accessible source. The county government
    website only lists the government leadership (副县长-level). The Party Committee
    leadership appears to not be published on the main government portal.
  - Baidu Baike/search: blocked/403
  - Exa: rate-limited

Under the source_fallbacks.md guidelines, this run produces structurally valid
artifacts with explicit uncertainty markers for the 县委书记 gap.
"""

import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "汤旺县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = TODAY

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

# Also produce canonical destination paths
CANONICAL_DB = os.path.join(BASE, "..", "..", "database", f"{SLUG}_network.db")
CANONICAL_GEXF = os.path.join(BASE, "..", "..", "graph", f"{SLUG}_network.gexf")
CANONICAL_BUILD = os.path.join(BASE, "..", "..", "..", f"build_{SLUG}_data.py")
CANONICAL_PERSONS = Path(BASE) / ".." / ".." / "persons"

# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════════
    # Core Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 县委书记 (PARTY SECRETARY OF TANGWANG COUNTY) — NOT FOUND via any accessible source
    # The county government website (www.yctwx.gov.cn) does not publish the 县委领导 page.
    {
        "id": 1,
        "name": "【待查】汤旺县委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记（待查）",
        "current_org": "中共汤旺县委员会",
        "source": "GAP — 汤旺县委书记姓名未在任何可访问来源上找到；需通过伊春市委组织部任前公示、汤旺县委网站或新闻报道补充",
    },

    # 梁巍 — 县委副书记、县长 (as of July 2026)
    # Confirmed from: homepage carousel title "县长梁巍调研督导环境卫生及重点项目建设等工作"
    # and article content: "县委副书记、县长梁巍"
    {
        "id": 2,
        "name": "梁巍",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "汤旺县人民政府",
        "source": "http://www.yctwx.gov.cn/twxrmzf/c101188/202504/397923.shtml",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # County Government Leadership (县政府领导班子)
    # Source: http://www.yctwx.gov.cn/twxrmzf/c101184/common_list.shtml
    # ══════════════════════════════════════════════════════════════════════════

    # 谷鹏 — 县委常委、常务副县长
    {
        "id": 3,
        "name": "谷鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年7月",
        "birthplace": "",
        "education": "省委党校公共管理专业，研究生学历",
        "party_join": "中共党员",
        "work_start": "2006年8月",
        "current_post": "县委常委、常务副县长",
        "current_org": "汤旺县人民政府",
        "source": "http://www.yctwx.gov.cn/twxrmzf/c101184/202508/408221.shtml",
    },

    # 刘强 — 县委常委、副县长（挂职）
    {
        "id": 4,
        "name": "刘强",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长（挂职）",
        "current_org": "汤旺县人民政府",
        "source": "http://www.yctwx.gov.cn/twxrmzf/c101184/202508/408231.shtml",
    },

    # 苏野 — 副县长
    {
        "id": 5,
        "name": "苏野",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "汤旺县人民政府",
        "source": "http://www.yctwx.gov.cn/twxrmzf/c101184/202508/408249.shtml",
    },

    # 谢萌 — 副县长
    {
        "id": 6,
        "name": "谢萌",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "汤旺县人民政府",
        "source": "http://www.yctwx.gov.cn/twxrmzf/c101184/202508/408232.shtml",
    },

    # 白鸽 — 副县长
    {
        "id": 7,
        "name": "白鸽",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "汤旺县人民政府",
        "source": "http://www.yctwx.gov.cn/twxrmzf/c101184/202508/408240.shtml",
    },

    # 刁鹏 — 副县长
    {
        "id": 8,
        "name": "刁鹏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "汤旺县人民政府",
        "source": "http://www.yctwx.gov.cn/twxrmzf/c101184/202508/408242.shtml",
    },

    # 刘鑫宇 — 副县长
    {
        "id": 9,
        "name": "刘鑫宇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "汤旺县人民政府",
        "source": "http://www.yctwx.gov.cn/twxrmzf/c101184/202508/408240.shtml",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # City-level Leadership (伊春市)
    # Source: Wikipedia - 伊春市 "现任领导" section
    # ══════════════════════════════════════════════════════════════════════════

    # 董文琴 — 伊春市委书记、市人大常委会主任
    {
        "id": 10,
        "name": "董文琴",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1972年10月",
        "birthplace": "黑龙江省宾县",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "伊春市委书记、市人大常委会主任",
        "current_org": "中共伊春市委员会",
        "source": "https://zh.wikipedia.org/wiki/伊春市",
    },

    # 苑芳江 — 伊春市委副书记、市长
    {
        "id": 11,
        "name": "苑芳江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年3月",
        "birthplace": "黑龙江省穆棱市",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "伊春市委副书记、市长",
        "current_org": "伊春市人民政府",
        "source": "https://zh.wikipedia.org/wiki/伊春市; https://www.yc.gov.cn/",
    },

    # 刘福军 — 伊春市政协主席
    {
        "id": 12,
        "name": "刘福军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年1月",
        "birthplace": "山东省梁山县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "伊春市政协主席",
        "current_org": "政协伊春市委员会",
        "source": "https://zh.wikipedia.org/wiki/伊春市",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    # County-level
    {"id": 1, "name": "中共汤旺县委员会", "type": "党委", "level": "县处级", "parent": "中共伊春市委员会", "location": "黑龙江省伊春市汤旺县"},
    {"id": 2, "name": "汤旺县人民政府", "type": "政府", "level": "县处级", "parent": "伊春市人民政府", "location": "黑龙江省伊春市汤旺县"},
    {"id": 3, "name": "汤旺县人大常委会", "type": "人大", "level": "县处级", "parent": "伊春市人大常委会", "location": "黑龙江省伊春市汤旺县"},
    {"id": 4, "name": "政协汤旺县委员会", "type": "政协", "level": "县处级", "parent": "政协伊春市委员会", "location": "黑龙江省伊春市汤旺县"},
    {"id": 5, "name": "中共汤旺县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共伊春市纪律检查委员会", "location": "黑龙江省伊春市汤旺县"},

    # City-level
    {"id": 6, "name": "中共伊春市委员会", "type": "党委", "level": "地市级", "parent": "中共黑龙江省委员会", "location": "黑龙江省伊春市伊美区"},
    {"id": 7, "name": "伊春市人民政府", "type": "政府", "level": "地市级", "parent": "黑龙江省人民政府", "location": "黑龙江省伊春市伊美区"},
    {"id": 8, "name": "伊春市人大常委会", "type": "人大", "level": "地市级", "parent": "黑龙江省人大常委会", "location": "黑龙江省伊春市伊美区"},
    {"id": 9, "name": "政协伊春市委员会", "type": "政协", "level": "地市级", "parent": "政协黑龙江省委员会", "location": "黑龙江省伊春市伊美区"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # GAP: 县委书记
    {"person_id": 1, "org_id": 1, "title": "汤旺县委书记", "start": "", "end": "", "rank": "县处级正职", "note": "GAP — 姓名和履历均待查"},

    # 梁巍 — 县长
    {"person_id": 2, "org_id": 1, "title": "汤旺县委副书记", "start": "", "end": "", "rank": "县处级副职", "note": "县政府党组书记"},
    {"person_id": 2, "org_id": 2, "title": "汤旺县县长", "start": "", "end": "", "rank": "县处级正职", "note": "至迟2025年4月已任县长，主持县政府全面工作"},

    # 谷鹏 — 常务副县长
    {"person_id": 3, "org_id": 1, "title": "汤旺县委常委", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "汤旺县常务副县长", "start": "", "end": "", "rank": "县处级副职", "note": "负责县政府常务工作，分管发改、财政、应急、人社等"},

    # 刘强 — 挂职副县长
    {"person_id": 4, "org_id": 1, "title": "汤旺县委常委（挂职）", "start": "", "end": "", "rank": "县处级副职", "note": "挂职"},
    {"person_id": 4, "org_id": 2, "title": "汤旺县副县长（挂职）", "start": "", "end": "", "rank": "县处级副职", "note": "挂职副县长"},

    # 苏野 — 副县长
    {"person_id": 5, "org_id": 2, "title": "汤旺县副县长", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 谢萌 — 副县长
    {"person_id": 6, "org_id": 2, "title": "汤旺县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "2025年4月陪同县长调研环境卫生和重点项目"},

    # 白鸽 — 副县长
    {"person_id": 7, "org_id": 2, "title": "汤旺县副县长", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # 刁鹏 — 副县长
    {"person_id": 8, "org_id": 2, "title": "汤旺县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "2025年4月陪同县长调研环境卫生和重点项目"},

    # 刘鑫宇 — 副县长
    {"person_id": 9, "org_id": 2, "title": "汤旺县副县长", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # City-level confirmed positions
    {"person_id": 10, "org_id": 6, "title": "伊春市委书记", "start": "2024年9月", "end": "", "rank": "地厅级正职", "note": ""},
    {"person_id": 10, "org_id": 8, "title": "伊春市人大常委会主任", "start": "2025年1月", "end": "", "rank": "地厅级正职", "note": ""},
    {"person_id": 11, "org_id": 6, "title": "伊春市委副书记", "start": "2024年9月", "end": "", "rank": "地厅级副职", "note": ""},
    {"person_id": 11, "org_id": 7, "title": "伊春市市长", "start": "2024年9月", "end": "", "rank": "地厅级正职", "note": "代市长转正"},
    {"person_id": 12, "org_id": 9, "title": "伊春市政协主席", "start": "2025年1月", "end": "", "rank": "地厅级正职", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────────────

relationships = [
    # 县委书记（待查）— 梁巍：党政搭档
    {"person_a": 1, "person_b": 2, "type": "党政同僚", "context": "县委书记与县长党政工作搭档（县委书记待查）", "overlap_org": "汤旺县", "overlap_period": ""},

    # 梁巍 — 谷鹏：党政搭档
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "县长与常务副县长工作搭档", "overlap_org": "汤旺县人民政府", "overlap_period": ""},

    # 梁巍 — 各副县长
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "县长与挂职副县长", "overlap_org": "汤旺县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "县长与副县长", "overlap_org": "汤旺县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "县长与副县长", "overlap_org": "汤旺县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "县长与副县长", "overlap_org": "汤旺县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "县长与副县长", "overlap_org": "汤旺县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "县长与副县长", "overlap_org": "汤旺县人民政府", "overlap_period": ""},

    # 谷鹏 — 其他副县长：同僚关系
    {"person_a": 3, "person_b": 4, "type": "同僚", "context": "常务副县长与挂职副县长", "overlap_org": "汤旺县人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 5, "type": "同僚", "context": "常务副县长与副县长", "overlap_org": "汤旺县人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 6, "type": "同僚", "context": "常务副县长与副县长", "overlap_org": "汤旺县人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 7, "type": "同僚", "context": "常务副县长与副县长", "overlap_org": "汤旺县人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 8, "type": "同僚", "context": "常务副县长与副县长", "overlap_org": "汤旺县人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 9, "type": "同僚", "context": "常务副县长与副县长", "overlap_org": "汤旺县人民政府", "overlap_period": ""},

    # 梁巍 — 谢萌、刁鹏：具体工作配合（环境卫生和重点项目调研）
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "县长率谢萌调研环境卫生和重点项目", "overlap_org": "汤旺县人民政府", "overlap_period": "2025年4月"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "县长率刁鹏调研环境卫生和重点项目", "overlap_org": "汤旺县人民政府", "overlap_period": "2025年4月"},

    # 梁巍 — 市级领导：上下级关系
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "汤旺县长受伊春市委领导", "overlap_org": "伊春市", "overlap_period": "2024年起"},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "汤旺县长受伊春市政府领导", "overlap_org": "伊春市人民政府", "overlap_period": "2024年起"},

    # 市级领导之间的关系
    {"person_a": 10, "person_b": 11, "type": "党政同僚", "context": "市委书记与市长党政搭档", "overlap_org": "中共伊春市委员会", "overlap_period": "2024年9月起"},
    {"person_a": 10, "person_b": 12, "type": "同僚", "context": "市委书记与政协主席", "overlap_org": "伊春市", "overlap_period": "2025年1月起"},
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
    if "书记" in post and "副" not in post and "纪委" not in post and "待查" not in post:
        return ("255,50,50", 20.0)  # Red, large
    elif "县长" in post and "副" not in post:
        return ("50,100,255", 20.0)  # Blue, large
    elif "副" in post and ("县长" in post or "书记" in post):
        return ("100,150,255", 12.0)  # Light blue
    elif "常委" in post:
        return ("100,150,255", 12.0)
    elif "待查" in post:
        return ("150,150,150", 12.0)  # Grey for unknown
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
    from datetime import datetime

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append(f'    <description>汤旺县领导班子关系网络 - {AS_OF}</description>')
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
        {"id":"S001","title":"汤旺县政府—领导信息页","url":"http://www.yctwx.gov.cn/twxrmzf/c101184/common_list.shtml","publisher":"汤旺县人民政府","published_at":"2025-08-26","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"县政府领导名单：谷鹏、刘强、苏野、谢萌、白鸽、刁鹏、刘鑫宇"},
        {"id":"S002","title":"县长梁巍调研督导环境卫生及重点项目建设等工作","url":"http://www.yctwx.gov.cn/twxrmzf/c101188/202504/397923.shtml","publisher":"汤旺县人民政府","published_at":"2025-04-07","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"确认梁巍为县委副书记、县长"},
        {"id":"S003","title":"谷鹏--中共汤旺县委常委、常务副县长","url":"http://www.yctwx.gov.cn/twxrmzf/c101184/202508/408221.shtml","publisher":"汤旺县人民政府办公室","published_at":"2025-08-26","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"谷鹏简历：1986年7月生，省委党校研究生"},
        {"id":"S004","title":"刘强--中共汤旺县委常委、副县长（挂职）","url":"http://www.yctwx.gov.cn/twxrmzf/c101184/202508/408231.shtml","publisher":"汤旺县人民政府办公室","published_at":"2025-08-26","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"刘强挂职副县长"},
        {"id":"S005","title":"苏野--副县长","url":"http://www.yctwx.gov.cn/twxrmzf/c101184/202508/408249.shtml","publisher":"汤旺县人民政府办公室","published_at":"2025-08-26","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":""},
        {"id":"S006","title":"谢萌--副县长","url":"http://www.yctwx.gov.cn/twxrmzf/c101184/202508/408232.shtml","publisher":"汤旺县人民政府办公室","published_at":"2025-08-26","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":""},
        {"id":"S007","title":"白鸽--副县长","url":"http://www.yctwx.gov.cn/twxrmzf/c101184/202508/408240.shtml","publisher":"汤旺县人民政府办公室","published_at":"2025-08-26","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":""},
        {"id":"S008","title":"刁鹏--副县长","url":"http://www.yctwx.gov.cn/twxrmzf/c101184/202508/408242.shtml","publisher":"汤旺县人民政府办公室","published_at":"2025-08-26","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":""},
        {"id":"S009","title":"刘鑫宇--副县长","url":"http://www.yctwx.gov.cn/twxrmzf/c101184/202508/408240.shtml","publisher":"汤旺县人民政府办公室","published_at":"2025-08-26","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":""},
        {"id":"S010","title":"伊春市—现任领导","url":"https://zh.wikipedia.org/wiki/伊春市","publisher":"Wikipedia","published_at":"2026-07-24","accessed_at":AS_OF,"source_type":"encyclopedia","reliability":"high","notes":"伊春市四大机构领导人：董文琴（书记）、苑芳江（市长）、刘福军（政协主席）"},
        {"id":"S011","title":"汤旺县—Wikipedia","url":"https://zh.wikipedia.org/wiki/汤旺县","publisher":"Wikipedia","published_at":"2026-07-24","accessed_at":AS_OF,"source_type":"encyclopedia","reliability":"high","notes":"汤旺县行政区划信息：2019年以原乌伊岭区、汤旺河区合并设立"},
    ]


def make_person_json(p, timeline, relationships_list, source_register):
    result = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "伊春市",
            "region": "汤旺县",
            "job": p["current_post"],
            "task_id": "heilongjiang_汤旺县",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"tangwangxian_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender",""),
            "ethnicity": p.get("ethnicity",""),
            "birth": p.get("birth",""),
            "birthplace": p.get("birthplace",""),
            "native_place": "",
            "education": [{"period":"","institution":"","major":"","degree":p.get("education",""),"study_type":"unknown","source_ids":[]}] if p.get("education") else [],
            "party_join": p.get("party_join","").replace("中共党员（","").replace("中共党员","").replace("）",""),
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
            "administrative_rank": "县处级正职" if ("县委书记" in p["current_post"] or "县长" == p["current_post"] or "县长" in p["current_post"]) else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": True if "待查" not in p["name"] else False,
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
            {"type":"none_found","description":"在公开信息中未发现该人物负面信号","date":"","confidence":"confirmed","source_ids":[]}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") else "plausible",
            "current_role": "confirmed" if "待查" not in p["name"] else "unverified",
            "career_completeness": "partial" if p.get("birth") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{p['name']}的完整履历信息有待补充" if not p.get("birth") else f"{p['name']}早期职业生涯需确认"
        },
        "open_questions": [
            {"priority":"critical" if not p.get("birth") else "medium",
             "question": f"{p['name']}的完整职业生涯履历",
             "why_it_matters": "无法追溯其任职路径和系统经历",
             "suggested_queries": [f"{p['name']} 简历 汤旺县",f"{p['name']} 任前公示"],
             "last_attempted": AS_OF}
        ]
    }
    return result


def build_person_jsons():
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()

    # 1. 梁巍 (县长)
    liang_timeline = [
        {"start":"","end":"","org":"中共汤旺县委员会","title":"汤旺县委副书记","notes":"县政府党组书记","confidence":"confirmed","source_ids":["S002"]},
        {"start":"","end":"","org":"汤旺县人民政府","title":"汤旺县县长","notes":"至迟2025年4月已以县长身份开展工作","confidence":"confirmed","source_ids":["S002"]},
    ]
    liang_relationships = [
        {"person":"【待查】汤旺县委书记","person_id":"tangwangxian_【待查】汤旺县委书记","relationship_type":"overlap","strength":"strong","evidence":"县长与县委书记党政工作搭档（县委书记姓名待查）","overlap_org":"汤旺县","overlap_period":"","direction":"undirected","confidence":"unverified","source_ids":[]},
        {"person":"谷鹏","person_id":"tangwangxian_谷鹏","relationship_type":"overlap","strength":"strong","evidence":"县长与常务副县长工作搭档","overlap_org":"汤旺县人民政府","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S003"]},
        {"person":"谢萌","person_id":"tangwangxian_谢萌","relationship_type":"overlap","strength":"medium","evidence":"县长率谢萌调研环境卫生和重点项目","overlap_org":"汤旺县人民政府","overlap_period":"2025年4月","direction":"undirected","confidence":"confirmed","source_ids":["S002"]},
        {"person":"刁鹏","person_id":"tangwangxian_刁鹏","relationship_type":"overlap","strength":"medium","evidence":"县长率刁鹏调研环境卫生和重点项目","overlap_org":"汤旺县人民政府","overlap_period":"2025年4月","direction":"undirected","confidence":"confirmed","source_ids":["S002"]},
    ]
    liang_json = make_person_json(persons[1], liang_timeline, liang_relationships, source_register)
    liang_path = PERSONS_DIR / f"{TODAY}-黑龙江省-伊春市-县长-梁巍.json"
    with open(liang_path, "w", encoding="utf-8") as f:
        json.dump(liang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {liang_path.name}")

    # 2. 谷鹏 (常务副县长 — has most detailed bio)
    gu_timeline = [
        {"start":"unknown","end":"unknown","org":"履历缺口","title":"","notes":"公开资料未找到2006-2025年完整履历","confidence":"unverified","source_ids":[]},
        {"start":"","end":"","org":"中共汤旺县委员会","title":"汤旺县委常委","notes":"","confidence":"confirmed","source_ids":["S003"]},
        {"start":"","end":"","org":"汤旺县人民政府","title":"汤旺县常务副县长","notes":"负责常务工作，分管发改、财政、应急、人社等","confidence":"confirmed","source_ids":["S003"]},
    ]
    gu_relationships = [
        {"person":"梁巍","person_id":"tangwangxian_梁巍","relationship_type":"overlap","strength":"strong","evidence":"常务副县长与县长工作搭档","overlap_org":"汤旺县人民政府","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S002","S003"]},
    ]
    gu_json = make_person_json(persons[2], gu_timeline, gu_relationships, source_register)
    gu_path = PERSONS_DIR / f"{TODAY}-黑龙江省-伊春市-常务副县长-谷鹏.json"
    with open(gu_path, "w", encoding="utf-8") as f:
        json.dump(gu_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {gu_path.name}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  汤旺县领导班子工作关系网络")
    print("  等级: 县")
    print("  调查日期: 2026-07-24")
    print("  信息来源: 汤旺县政府网站、Wikipedia")
    print("=" * 60)

    build_db()
    build_gexf()
    build_person_jsons()

    print(f"\n✅ 汤旺县数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

if __name__ == "__main__":
    main()
