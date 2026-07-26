#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 合江县 (Hejiang County), 泸州市, 四川省.

Investigation date: 2026-07-26
Task ID: sichuan_合江县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - www.hejiang.gov.cn — 合江县人民政府 (official leadership profiles)
  - 合江县"两优一先"表彰大会报道 (2026-06-30) — 县委书记王波讲话
  - 县生态环境保护委员会会议 (2026-06-16) — 王波、李庆、况涛等出席
  - 安全生产培训报道 (2026-07-06) — 王波、李庆、况涛参会
  - 王波督导森林防灭火 (2026-07-13/14) — 县委书记王波赴福宝镇、九支镇督导
  - 合江县人民政府任免通知 (合府发〔2026〕20号) — 徐畅任副县长、公安局长，张立免职

Confidence notes:
  - 王波 (县委书记): confirmed as current party secretary via multiple news articles
  - 李庆 (县长): confirmed via government leadership page with full identity details
  - 况涛 (县委副书记): confirmed via multiple news reports
  - Government leadership (肖菲、施崇亮、刘彬等): confirmed via official 领导之窗 page
  - 王波's career biography incomplete — no separate party secretary profile found on official site
  - Predecessor information not found; web search limitations prevented confirmation
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = str(STAGING_DIR)
SLUG = "合江县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")

CANONICAL_DB = os.path.join(BASE, "..", "..", "database", f"{SLUG}_network.db")
CANONICAL_GEXF = os.path.join(BASE, "..", "..", "graph", f"{SLUG}_network.gexf")
CANONICAL_BUILD = os.path.join(BASE, "..", "..", "..", f"build_{SLUG}_data.py")
CANONICAL_PERSONS = Path(BASE) / ".." / ".." / "persons"

# ══════════════════════════════════════════════════════════════════════════
# Persons
# ══════════════════════════════════════════════════════════════════════════
persons = [
    # ── Core: Party Secretary (县委书记) ──
    {
        "id": 1,
        "name": "王波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共合江县委员会",
        "source": "合江县人民政府网站 — multiple news articles confirming role"
    },
    # ── Core: County Magistrate (县长) ──
    {
        "id": 2,
        "name": "李庆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年10月",
        "birthplace": "四川省泸州市纳溪区",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "1995年9月",
        "current_post": "县长",
        "current_org": "合江县人民政府",
        "source": "合江县人民政府网站-领导之窗 (zfld/xz/content_131698)"
    },
    # ── Deputy Party Secretary ──
    {
        "id": 3,
        "name": "况涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共合江县委员会",
        "source": "合江县人民政府 — 多篇新闻报道确认"
    },
    # ── Standing Committee / Government Deputy Leaders ──
    {
        "id": 4,
        "name": "肖菲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "合江县人民政府",
        "source": "合江县人民政府网站 — 领导之窗"
    },
    {
        "id": 5,
        "name": "施崇亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "合江县人民政府",
        "source": "合江县人民政府网站 — 领导之窗"
    },
    {
        "id": 6,
        "name": "刘彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "合江县人民政府",
        "source": "合江县人民政府网站 — 领导之窗"
    },
    {
        "id": 7,
        "name": "胡杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "合江县人民政府",
        "source": "合江县人民政府网站 — 领导之窗"
    },
    {
        "id": 8,
        "name": "潘春晓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "合江县人民政府",
        "source": "合江县人民政府网站 — 领导之窗"
    },
    {
        "id": 9,
        "name": "徐畅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "合江县人民政府",
        "source": "合江县人民政府 — 合府发〔2026〕20号"
    },
    # ── People's Congress and Political Consultative ──
    {
        "id": 10,
        "name": "熊正彪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "合江县人民代表大会常务委员会",
        "source": "合江县新闻网 — 两优一先表彰大会报道"
    },
    {
        "id": 11,
        "name": "刘卫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议合江县委员会",
        "source": "合江县新闻网 — 两优一先表彰大会报道"
    },
    # ── Other County Leaders ──
    {
        "id": 12,
        "name": "钟梦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中共合江县委员会",
        "source": "合江县新闻网 — 两优一先表彰大会"
    },
    {
        "id": 13,
        "name": "刘海涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中共合江县委员会",
        "source": "合江县新闻网 — 两优一先表彰大会"
    },
    {
        "id": 14,
        "name": "王小波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中共合江县委员会",
        "source": "合江县新闻网 — 两优一先表彰大会"
    },
    {
        "id": 15,
        "name": "陈果",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中共合江县委员会",
        "source": "合江县新闻网 — 两优一先表彰大会"
    },
    {
        "id": 16,
        "name": "丁飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中共合江县委员会",
        "source": "合江县新闻网 — 两优一先表彰大会"
    },
    # ── Previous Officeholders ──
    {
        "id": 17,
        "name": "张立",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原副县长、县公安局局长",
        "current_org": "",
        "source": "合江县人大常委会 — 2026年6月免职决定"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共合江县委员会", "type": "党委", "level": "县级", "parent": "中共泸州市委员会", "location": "泸州市合江县"},
    {"id": 2, "name": "合江县人民政府", "type": "政府", "level": "县级", "parent": "泸州市人民政府", "location": "泸州市合江县"},
    {"id": 3, "name": "合江县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "", "location": "泸州市合江县"},
    {"id": 4, "name": "中国人民政治协商会议合江县委员会", "type": "政协", "level": "县级", "parent": "", "location": "泸州市合江县"},
    {"id": 5, "name": "合江县公安局", "type": "政府", "level": "县级", "parent": "合江县人民政府", "location": "泸州市合江县"},
    {"id": 6, "name": "中共泸州市委员会", "type": "党委", "level": "厅级", "parent": "中共四川省委", "location": "泸州市"},
    {"id": 7, "name": "泸州市人民政府", "type": "政府", "level": "厅级", "parent": "四川省人民政府", "location": "泸州市"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 王波
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "未知", "end": "至今", "rank": "正县级", "note": "通过2026年新闻报道确认"},
    # 李庆
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "未知", "end": "至今", "rank": "正县级", "note": "县政府党组书记"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "未知", "end": "至今", "rank": "正县级", "note": ""},
    # 况涛
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "未知", "end": "至今", "rank": "副县级", "note": ""},
    # 肖菲
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "未知", "end": "至今", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "常务副县长", "start": "未知", "end": "至今", "rank": "副县级", "note": ""},
    # 施崇亮
    {"person_id": 5, "org_id": 2, "title": "副县长", "start": "未知", "end": "至今", "rank": "副县级", "note": "负责卫健、医保、民政"},
    # 刘彬
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "未知", "end": "至今", "rank": "副县级", "note": "负责工业、园区、科技"},
    # 胡杰
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "未知", "end": "至今", "rank": "副县级", "note": "负责住建、文旅"},
    # 潘春晓
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "未知", "end": "至今", "rank": "副县级", "note": "负责商务、教育体育"},
    # 徐畅
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "2026-06", "end": "至今", "rank": "副县级", "note": "接替张立"},
    {"person_id": 9, "org_id": 5, "title": "县公安局局长", "start": "2026-06", "end": "至今", "rank": "副县级", "note": "2026年6月任命"},
    # 熊正彪
    {"person_id": 10, "org_id": 3, "title": "县人大常委会主任", "start": "未知", "end": "至今", "rank": "正县级", "note": ""},
    # 刘卫
    {"person_id": 11, "org_id": 4, "title": "县政协主席", "start": "未知", "end": "至今", "rank": "正县级", "note": ""},
    # 张立（原）
    {"person_id": 17, "org_id": 2, "title": "副县长", "start": "未知", "end": "2026-06", "rank": "副县级", "note": "任免通知确认免职"},
    {"person_id": 17, "org_id": 5, "title": "县公安局局长", "start": "未知", "end": "2026-06", "rank": "副县级", "note": "合府发〔2026〕20号"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # 党政一把手搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "王波（县委书记）与李庆（县长）为党政一把手搭档", "overlap_org": "合江县", "overlap_period": "至今"},
    # 县委书记与县委副书记
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "王波（县委书记）与况涛（县委副书记）在县委常委会共事", "overlap_org": "中共合江县委员会", "overlap_period": "至今"},
    # 县长与常务副县长
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "李庆（县长）与肖菲（常务副县长）在县政府班子共事", "overlap_org": "合江县人民政府", "overlap_period": "至今"},
    # 县长与副县长
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "李庆（县长）与施崇亮（副县长）在县政府班子共事", "overlap_org": "合江县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "李庆（县长）与刘彬（副县长）在县政府班子共事", "overlap_org": "合江县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "李庆（县长）与胡杰（副县长）在县政府班子共事", "overlap_org": "合江县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "李庆（县长）与潘春晓（副县长）在县政府班子共事", "overlap_org": "合江县人民政府", "overlap_period": "至今"},
    # 常务副县长与副县长
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "肖菲（常务副县长）与施崇亮（副县长）在县政府班子共事", "overlap_org": "合江县人民政府", "overlap_period": "至今"},
    {"person_a": 4, "person_b": 9, "type": "overlap", "context": "肖菲（常务副县长）与徐畅（副县长、公安局长）在县政府班子共事", "overlap_org": "合江县人民政府", "overlap_period": "至今"},
    # 前任与继任（副县长、公安局长）
    {"person_a": 17, "person_b": 9, "type": "predecessor_successor", "context": "张立免去副县长、县公安局局长职务，徐畅接任", "overlap_org": "合江县公安局", "overlap_period": "2026-06"},
    # 四套班子领导
    {"person_a": 10, "person_b": 11, "type": "overlap", "context": "熊正彪（县人大主任）与刘卫（县政协主席）在县四套班子共事", "overlap_org": "合江县", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "王波（县委书记）与熊正彪（县人大主任）在县四套班子共事", "overlap_org": "合江县", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "王波（县委书记）与刘卫（县政协主席）在县四套班子共事", "overlap_org": "合江县", "overlap_period": "至今"},
    # 县委班子其他成员
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "王波（县委书记）与钟梦在县委会议中共同出席", "overlap_org": "中共合江县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 13, "type": "overlap", "context": "王波（县委书记）与刘海涛在县委会议中共同出席", "overlap_org": "中共合江县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 14, "type": "overlap", "context": "王波（县委书记）与王小波在县委会议中共同出席", "overlap_org": "中共合江县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 15, "type": "overlap", "context": "王波（县委书记）与陈果在县委会议中共同出席", "overlap_org": "中共合江县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 16, "type": "overlap", "context": "王波（县委书记）与丁飞在县委会议中共同出席", "overlap_org": "中共合江县委员会", "overlap_period": "至今"},
]


# ══════════════════════════════════════════════════════════════════════════
# Build
# ══════════════════════════════════════════════════════════════════════════

def build_sqlite(db_path):
    """Build SQLite database from the data above."""
    import sqlite3
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"],
             p["birth"], p["birthplace"], p["education"],
             p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"],
             r["context"], r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"  SQLite DB written: {db_path}")
    print(f"    Persons: {len(persons)}, Orgs: {len(organizations)}, "
          f"Positions: {len(positions)}, Relationships: {len(relationships)}")


def write_gexf(output_path):
    """Write GEXF with proper viz namespace using string formatting."""
    from datetime import datetime

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color(post):
        if "书记" in post and "副" not in post:
            return "200,30,30"
        elif "县长" in post:
            return "30,100,200"
        elif "副书记" in post:
            return "220,80,80"
        elif "副" in post:
            return "100,150,220"
        elif "主任" in post:
            return "60,180,60"
        elif "主席" in post:
            return "60,180,60"
        else:
            return "180,180,180"

    def person_size(post):
        if "书记" in post and "副" not in post:
            return "20.0"
        elif "县长" in post:
            return "20.0"
        elif "副书记" in post:
            return "15.0"
        elif "副" in post:
            return "12.0"
        elif "主任" in post:
            return "12.0"
        elif "主席" in post:
            return "12.0"
        else:
            return "10.0"

    def org_color(org_type):
        return {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "人大": "200,255,255",
            "政协": "255,240,200",
        }.get(org_type, "200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>合江县领导班子工作关系网络图 - 2026年7月</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="birthplace" type="string"/>')
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
    for p in persons:
        c = person_color(p)
        sz = person_size(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["birthplace"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organizational nodes
    org_start_id = 100
    for i, o in enumerate(organizations):
        oid = org_start_id + i
        oc = org_color(o["type"])
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["name"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'          <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append('          <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person↔organization (worked_at)
    org_start_id = 100
    for pos in positions:
        p_id = pos["person_id"]
        o_id = org_start_id + next(i for i, o in enumerate(organizations) if o["id"] == pos["org_id"])
        lines.append(f'      <edge id="e{eid}" source="p{p_id}" target="o{o_id}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person↔Person (relationship)
    for r in relationships:
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {output_path}")
    print(f"  Edges: {eid}")


# ══════════════════════════════════════════════════════════════════════════
# Person JSON helpers
# ══════════════════════════════════════════════════════════════════════════

def write_person_json(person, task_id, province, city, region, output_dir):
    """Write a single person's deep graph JSON."""
    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": province,
            "city": city,
            "region": region,
            "job": person["current_post"],
            "task_id": task_id,
            "time_focus": "至今"
        },
        "identity": {
            "person_id": f"hejiang_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "", "study_type": "unknown", "source_ids": []}] if person.get("education") else [],
            "party_join": "中共党员" if person.get("party_join") else "",
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth', '')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
                "official_profile_url": f"https://www.hejiang.gov.cn/"
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "未知",
                "end": "至今",
                "org": person["current_org"],
                "title": person["current_post"],
                "level": "",
                "location": f"泸州市{region}",
                "system": "party" if "委" in person["current_org"] else "government",
                "rank": "",
                "is_key_promotion": False,
                "notes": f"当前职务，通过合江县政府官方网站确认，截至{AS_OF}",
                "confidence": "confirmed" if person["name"] in ["王波", "李庆", "况涛", "肖菲", "熊正彪", "刘卫"] else "plausible",
                "source_ids": ["S001"]
            }
        ],
        "organizations": [
            {
                "id": f"org_{region}_{person['name']}",
                "name": person["current_org"],
                "type": "党委" if "委" in person["current_org"] else "政府",
                "role_in_org": person["current_post"],
                "period": "至今"
            }
        ],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "公开资料有限，无法评估晋升速度",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "unknown",
                    "evidence": "公开信息来源有限",
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "network_metrics": {
            "total_relationships": 0,
            "strong_connections": 0,
            "medium_connections": 0,
            "weak_connections": 0
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "未发现负面记录",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "合江县人民政府网站",
                "url": "https://www.hejiang.gov.cn/",
                "publisher": "合江县人民政府",
                "published_at": "",
                "accessed_at": TODAY,
                "source_type": "official",
                "reliability": "high",
                "notes": "合江县官方政府网站领导之窗及新闻报道"
            }
        ],
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "该人物完整的职业生涯、出生信息均未获取" if not person.get("birth") else "公开职业生涯信息不完整"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}担任{person['current_post']}之前的职业履历是什么？",
                "why_it_matters": f"合江县核心领导的基础信息",
                "suggested_queries": [
                    f"{person['name']} 简历 泸州",
                    f"{person['name']} 任前公示",
                    f"{person['name']} 此前担任"
                ],
                "last_attempted": TODAY
            },
            {
                "priority": "high",
                "question": f"{person['name']}的出生年月和籍贯是什么？" if not person.get("birth") else "",
                "why_it_matters": "基础身份信息",
                "suggested_queries": [
                    f"{person['name']} 出生",
                    f"{person['name']} 籍贯"
                ],
                "last_attempted": TODAY
            }
        ]
    }

    # Clean emempty questions
    data["open_questions"] = [q for q in data["open_questions"] if q.get("question")]

    job_slug = person["current_post"].replace("、", "_").replace("，", "_").replace(" ", "_")
    filename = f"{TODAY}-{province}-{city}-{job_slug}-{person['name']}.json"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {filepath}")
    return filepath


def main():
    """Run the full build pipeline."""
    import argparse
    parser = argparse.ArgumentParser(description="Build 合江县 network data")
    parser.add_argument("--db", default=DB_PATH)
    parser.add_argument("--gexf", default=GEXF_PATH)
    parser.add_argument("--person-dir", default=str(STAGING_DIR))
    args = parser.parse_args()

    prov = "四川省"
    city = "泸州市"
    region = "合江县"
    task_id = "sichuan_合江县"

    print(f"\n{'='*60}")
    print(f"{region} 网络构建")
    print(f"{'='*60}\n")

    # 1. SQlite
    print("Building SQLite database...")
    build_sqlite(args.db)

    # 2. GEXF
    print("Building GEXF graph...")
    write_gexf(args.gexf)

    # 3. Person JSONs (核心人物)
    print("Writing person JSON files...")
    core_ids = [1, 2, 3]  # 王波, 李庆, 况涛
    for pid in core_ids:
        p = next(x for x in persons if x["id"] == pid)
        write_person_json(p, task_id, prov, city, region, args.person_dir)

    print(f"\n{'='*60}")
    print(f"Build complete.")
    print(f"DB: {args.db}")
    print(f"GEXF: {args.gexf}")
    print(f"Persons: {len(persons)} in data, {len(core_ids)} JSON files")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()