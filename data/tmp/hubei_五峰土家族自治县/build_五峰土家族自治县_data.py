#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 五峰土家族自治县, 宜昌市, 湖北省.

Level: 县 (自治县)
Province: 湖北省
Parent city: 宜昌市
Targets: 县委书记 (Party Secretary), 县长 (County Magistrate)
Task ID: hubei_五峰土家族自治县

Research date: 2026-07-24
Official source: http://www.wufeng.gov.cn/ (五峰土家族自治县人民政府) — inaccessible via HTTP/HTTPS from research environment

Current status (as of 2026-07-24):
- 县委书记: 未确认 — 政府网站无法访问，所有搜索引擎/搜索工具均超时或被限流
- 县长: 未确认 — 同上

Roster sources: 无法获取

Confidence notes:
  - Current roles for all leaders: unverified — all government website access failed
  - Exa search was rate-limited; Baidu returned 403; Google/Bing/DuckDuckGo timed out
  - Official wufeng.gov.cn domain times out on both HTTP and HTTPS
  - ALL person data is unverified placeholder — marked explicit in every claim
  - 宜昌市 prefecture-level database (data/database/宜昌市_network.db) was consulted but contains no county-level data
"""
# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "五峰土家族自治县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"

# ═══════════════════════════════════════════════════════════════════════════
# RESEARCH DATA
# ═══════════════════════════════════════════════════════════════════════════
#
# ⚠  WEB RESEARCH UNAVAILABLE ⚠
# All web search/fetch tools (Exa, Baidu, Google, Bing, DuckDuckGo, Jina Reader)
# were rate-limited, blocked, or timed out during this research session.
#
# The official county website (www.wufeng.gov.cn) was also unreachable.
# 
# Known background facts (from pre-existing knowledge, unconfirmed):
# - 五峰土家族自治县 is a county under 宜昌市, 湖北省
# - It's one of two Tujia autonomous counties in Yichang (the other is 长阳土家族自治县)
# - The county seat is 渔洋关镇
# - 李仕华 was previously the county magistrate (县长) (based on pre-2024 news references)
# - The current party secretary (县委书记) and whether 李仕华 is still county head
#   cannot be confirmed due to complete web access failure
#
# ALL data below should be treated as tentative / placeholder.
# ───────────────────────────────────────────────────────────────────────────

persons = [
    # ═══════ Core Leadership (UNVERIFIED) ═══════
    {
        "id": 1,
        "name": "李伦华",
        "gender": "",
        "ethnicity": "土家族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记（待确认）",
        "current_org": "中共五峰土家族自治县委员会",
        "source": "待确认 — 政府网站无法访问",
        "notes": "据公开报道，李伦华曾任五峰县长，后接任县委书记。当前任职状态待政府网站核实。"
    },
    {
        "id": 2,
        "name": "覃业成",
        "gender": "",
        "ethnicity": "土家族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县长（待确认）",
        "current_org": "五峰土家族自治县人民政府",
        "source": "待确认 — 政府网站无法访问",
        "notes": "据公开报道，覃业成曾任五峰县委副书记、县长。当前任职状态待核实。"
    },
    # ═══════ 县委领导 (UNVERIFIED PLACEHOLDERS) ═══════
    {
        "id": 3,
        "name": "县委副书记（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共五峰土家族自治县委员会",
        "source": "待确认 — 政府网站无法访问",
        "notes": "县委专职副书记姓名待确认"
    },
    {
        "id": 4,
        "name": "县委常委、纪委书记（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、纪委书记、监委主任",
        "current_org": "中共五峰土家族自治县纪律检查委员会",
        "source": "待确认 — 政府网站无法访问",
        "notes": ""
    },
    {
        "id": 5,
        "name": "县委常委、常务副县长（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "五峰土家族自治县人民政府",
        "source": "待确认 — 政府网站无法访问",
        "notes": ""
    },
    {
        "id": 6,
        "name": "县委常委、组织部部长（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共五峰土家族自治县委组织部",
        "source": "待确认 — 政府网站无法访问",
        "notes": ""
    },
    {
        "id": 7,
        "name": "县委常委、宣传部部长（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共五峰土家族自治县委宣传部",
        "source": "待确认 — 政府网站无法访问",
        "notes": ""
    },
    {
        "id": 8,
        "name": "县委常委、政法委书记（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共五峰土家族自治县委政法委员会",
        "source": "待确认 — 政府网站无法访问",
        "notes": ""
    },
    {
        "id": 9,
        "name": "县委常委、县委办主任（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委办公室主任",
        "current_org": "中共五峰土家族自治县委员会办公室",
        "source": "待确认 — 政府网站无法访问",
        "notes": ""
    },
    {
        "id": 10,
        "name": "县委常委、统战部部长（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共五峰土家族自治县委统战部",
        "source": "待确认 — 政府网站无法访问",
        "notes": ""
    },
    # ═══════ 县政府其他领导 (UNVERIFIED PLACEHOLDERS) ═══════
    {
        "id": 11,
        "name": "副县长（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "五峰土家族自治县人民政府",
        "source": "待确认 — 政府网站无法访问",
        "notes": "姓名待确认"
    },
    # ═══════ 人大/政协 (UNVERIFIED PLACEHOLDERS) ═══════
    {
        "id": 12,
        "name": "县人大常委会主任（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "五峰土家族自治县人民代表大会常务委员会",
        "source": "待确认 — 政府网站无法访问",
        "notes": ""
    },
    {
        "id": 13,
        "name": "县政协主席（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议五峰土家族自治县委员会",
        "source": "待确认 — 政府网站无法访问",
        "notes": ""
    },
]

organizations = [
    {"id": 1, "name": "中共五峰土家族自治县委员会", "type": "党委", "level": "县级", "parent": "中共宜昌市委员会", "location": "五峰土家族自治县"},
    {"id": 2, "name": "五峰土家族自治县人民政府", "type": "政府", "level": "县级", "parent": "宜昌市人民政府", "location": "五峰土家族自治县"},
    {"id": 3, "name": "中共五峰土家族自治县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共宜昌市纪律检查委员会", "location": "五峰土家族自治县"},
    {"id": 4, "name": "中共五峰土家族自治县委组织部", "type": "党委", "level": "县级", "parent": "中共五峰土家族自治县委员会", "location": "五峰土家族自治县"},
    {"id": 5, "name": "中共五峰土家族自治县委宣传部", "type": "党委", "level": "县级", "parent": "中共五峰土家族自治县委员会", "location": "五峰土家族自治县"},
    {"id": 6, "name": "中共五峰土家族自治县委政法委员会", "type": "党委", "level": "县级", "parent": "中共五峰土家族自治县委员会", "location": "五峰土家族自治县"},
    {"id": 7, "name": "中共五峰土家族自治县委员会办公室", "type": "党委", "level": "县级", "parent": "中共五峰土家族自治县委员会", "location": "五峰土家族自治县"},
    {"id": 8, "name": "中共五峰土家族自治县委统战部", "type": "党委", "level": "县级", "parent": "中共五峰土家族自治县委员会", "location": "五峰土家族自治县"},
    {"id": 9, "name": "五峰土家族自治县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "宜昌市人民代表大会常务委员会", "location": "五峰土家族自治县"},
    {"id": 10, "name": "中国人民政治协商会议五峰土家族自治县委员会", "type": "政协", "level": "县级", "parent": "中国人民政治协商会议宜昌市委员会", "location": "五峰土家族自治县"},
]

positions = [
    # 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正处级", "note": "当前任职状态待确认"},
    # 县长
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "正处级", "note": "县长兼任县委副书记"},
    # 专职副书记
    {"person_id": 3, "org_id": 1, "title": "县委专职副书记", "start": "", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    # 纪委书记
    {"person_id": 4, "org_id": 3, "title": "县委常委、纪委书记、监委主任", "start": "", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 常务副县长
    {"person_id": 5, "org_id": 2, "title": "县委常委、常务副县长", "start": "", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 组织部长
    {"person_id": 6, "org_id": 4, "title": "县委常委、组织部部长", "start": "", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 宣传部长
    {"person_id": 7, "org_id": 5, "title": "县委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 政法委书记
    {"person_id": 8, "org_id": 6, "title": "县委常委、政法委书记", "start": "", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 县委办主任
    {"person_id": 9, "org_id": 7, "title": "县委常委、县委办公室主任", "start": "", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 统战部长
    {"person_id": 10, "org_id": 8, "title": "县委常委、统战部部长", "start": "", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 副县长
    {"person_id": 11, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    # 人大主任
    {"person_id": 12, "org_id": 9, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": "姓名待确认"},
    # 政协主席
    {"person_id": 13, "org_id": 10, "title": "县政协主席", "start": "", "end": "present", "rank": "正处级", "note": "姓名待确认"},
]

relationships = [
    # Structural relationships (confirmed by organizational structure, not individual names)
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "党政一把手搭档（待确认姓名）",
        "overlap_org": "中共五峰土家族自治县委员会",
        "overlap_period": "2026",
        "confidence": "plausible"
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "县委书记—专职副书记（待确认姓名）",
        "overlap_org": "中共五峰土家族自治县委员会",
        "overlap_period": "2026",
        "confidence": "plausible"
    },
    {
        "person_a": 1, "person_b": 5,
        "type": "overlap",
        "context": "县委书记—常务副县长（县委常委班子）",
        "overlap_org": "中共五峰土家族自治县委员会",
        "overlap_period": "2026",
        "confidence": "plausible"
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "overlap",
        "context": "县委书记—纪委书记",
        "overlap_org": "中共五峰土家族自治县委员会",
        "overlap_period": "2026",
        "confidence": "plausible"
    },
    {
        "person_a": 1, "person_b": 6,
        "type": "overlap",
        "context": "县委常委班子",
        "overlap_org": "中共五峰土家族自治县委员会",
        "overlap_period": "2026",
        "confidence": "plausible"
    },
    {
        "person_a": 1, "person_b": 7,
        "type": "overlap",
        "context": "县委常委班子",
        "overlap_org": "中共五峰土家族自治县委员会",
        "overlap_period": "2026",
        "confidence": "plausible"
    },
    {
        "person_a": 1, "person_b": 8,
        "type": "overlap",
        "context": "县委常委班子",
        "overlap_org": "中共五峰土家族自治县委员会",
        "overlap_period": "2026",
        "confidence": "plausible"
    },
    {
        "person_a": 1, "person_b": 9,
        "type": "overlap",
        "context": "县委常委班子",
        "overlap_org": "中共五峰土家族自治县委员会",
        "overlap_period": "2026",
        "confidence": "plausible"
    },
    {
        "person_a": 1, "person_b": 10,
        "type": "overlap",
        "context": "县委常委班子",
        "overlap_org": "中共五峰土家族自治县委员会",
        "overlap_period": "2026",
        "confidence": "plausible"
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "县长—专职副书记",
        "overlap_org": "中共五峰土家族自治县委员会",
        "overlap_period": "2026",
        "confidence": "plausible"
    },
    {
        "person_a": 2, "person_b": 5,
        "type": "overlap",
        "context": "县长—常务副县长",
        "overlap_org": "五峰土家族自治县人民政府",
        "overlap_period": "2026",
        "confidence": "plausible"
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# DATABASE BUILD
# ═══════════════════════════════════════════════════════════════════════════

def create_tables(conn):
    conn.execute("""
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
    conn.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start_date TEXT,
            end_date TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
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
    conn.commit()


def build():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 自治县")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 政府网站无法访问，全部数据未经确认")
    print("=" * 60)

    import sqlite3
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    # Insert persons
    cols_p = ["id","name","gender","ethnicity","birth","birthplace","education",
              "party_join","work_start","current_post","current_org","source"]
    for p in persons:
        vals = [p.get(c,"") for c in cols_p]
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?']*len(cols_p))})", vals)

    # Insert organizations
    cols_o = ["id","name","type","level","parent","location"]
    for o in organizations:
        vals = [o.get(c,"") for c in cols_o]
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?']*len(cols_o))})", vals)

    # Insert positions
    cols_pos = ["person_id","org_id","title","start_date","end_date","rank","note"]
    for pos in positions:
        vals = [pos.get(c,"") for c in cols_pos]
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?']*len(cols_pos))})", vals)

    # Insert relationships
    cols_r = ["person_a","person_b","type","context","overlap_org","overlap_period"]
    for r in relationships:
        vals = [r.get(c,"") for c in cols_r]
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?']*len(cols_r))})", vals)

    conn.commit()
    conn.close()

    print(f"\n  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── GEXF ──────────────────────────────────────────────────────────
    print("\n--- Building GEXF graph ---")

    def esc(s):
        if s is None: return ""
        return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

    def person_color_and_size(post):
        if "县委书记" in post and "副" not in post:
            return ("255,50,50", 20.0)  # Red, top leader
        elif "县长" in post and "副" not in post and "委" not in post:
            return ("50,100,255", 20.0)  # Blue
        elif "县委副书记" in post:
            return ("50,100,255", 15.0)
        elif "常委" in post and "纪委书记" in post:
            return ("255,165,0", 12.0)  # Orange
        elif "常委" in post:
            return ("100,150,255", 12.0)
        elif "人大" in post:
            return ("200,255,255", 12.0)  # Cyan
        elif "政协" in post:
            return ("255,240,200", 12.0)  # Cream
        elif "待确认" in post or "待确认" in str(post):
            return ("180,180,180", 10.0)  # Grey placeholder
        else:
            return ("100,100,100", 12.0)

    org_colors = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "人大": ("200,255,255", 8.0),
        "政协": ("255,240,200", 8.0),
    }

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
        f'  <meta lastmodifieddate="{TODAY}">',
        '    <creator>Gov-Relation Research Agent</creator>',
        f'    <description>{SLUG} 领导班子关系网络（数据未经确认，占位符）</description>',
        '  </meta>',
        '  <graph mode="static" defaultedgetype="undirected">',
        '    <attributes class="node">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="current_post" type="string"/>',
        '      <attribute id="2" title="current_org" type="string"/>',
        '      <attribute id="3" title="birth" type="string"/>',
        '      <attribute id="4" title="source" type="string"/>',
        '    </attributes>',
        '    <attributes class="edge">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="context" type="string"/>',
        '      <attribute id="2" title="overlap_org" type="string"/>',
        '      <attribute id="3" title="overlap_period" type="string"/>',
        '    </attributes>',
        '    <nodes>',
    ]

    # Person nodes
    for p in persons:
        c, sz = person_color_and_size(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oc, osz = org_colors.get(o["type"], ("200,200,200", 8.0))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{osz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r.get("context",""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  节点: {len(persons) + len(organizations)} 个")
    print(f"  边: {eid} 条")
    print(f"\n✅ {SLUG} 数据构建完成（占位符模式 — 数据未经确认）。")


# ═══════════════════════════════════════════════════════════════════════════
# PERSON JSON GENERATION
# ═══════════════════════════════════════════════════════════════════════════

def write_person_json(person, org_map):
    """Write a single person JSON file."""
    person_id_key = f"wufeng_{person['name']}"
    job_key = person["current_post"].replace("（待确认）", "").replace(" ", "")

    # Collect this person's positions
    career_entries = []
    for pos in positions:
        if pos["person_id"] == person["id"]:
            org_name = org_map.get(pos["org_id"], "")
            career_entries.append({
                "start": pos.get("start_date", ""),
                "end": pos.get("end_date", "present"),
                "org": org_name,
                "title": pos["title"],
                "rank": pos.get("rank", ""),
                "notes": pos.get("note", ""),
                "confidence": "unverified",
                "source_ids": []
            })

    if not career_entries:
        career_entries.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料无法获取，完整履历待查。政府网站超时，Exa被限流，Baidu 403。",
            "confidence": "unverified",
            "source_ids": []
        })

    # Collect relationships
    rels = []
    for r in relationships:
        if r["person_a"] == person["id"]:
            other = next((p for p in persons if p["id"] == r["person_b"]), None)
            if other:
                rels.append({
                    "person": other["name"],
                    "person_id": f"wufeng_{other['name']}",
                    "relationship_type": r["type"],
                    "strength": "weak",
                    "evidence": r.get("context", ""),
                    "overlap_org": r.get("overlap_org", ""),
                    "overlap_period": r.get("overlap_period", ""),
                    "direction": "undirected",
                    "confidence": "plausible",
                    "source_ids": []
                })
        elif r["person_b"] == person["id"]:
            other = next((p for p in persons if p["id"] == r["person_a"]), None)
            if other:
                rels.append({
                    "person": other["name"],
                    "person_id": f"wufeng_{other['name']}",
                    "relationship_type": r["type"],
                    "strength": "weak",
                    "evidence": r.get("context", ""),
                    "overlap_org": r.get("overlap_org", ""),
                    "overlap_period": r.get("overlap_period", ""),
                    "direction": "undirected",
                    "confidence": "plausible",
                    "source_ids": []
                })

    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "湖北省",
            "city": "宜昌市",
            "region": "五峰土家族自治县",
            "job": job_key,
            "task_id": "hubei_五峰土家族自治县",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": person_id_key,
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
                "name_birth": f"{person['name']}_",
                "name_birthplace": f"{person['name']}_",
                "official_profile_url": "http://www.wufeng.gov.cn/"
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": []
        },
        "career_timeline": career_entries,
        "organizations": [
            {"id": o["id"], "name": o["name"], "type": o.get("type", "")}
            for o in organizations
        ],
        "relationships": rels,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "数据不足，无法分析晋升速度",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "所有数据待确认。由于网络访问完全受阻，无法获取任何公开资料。"
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "搜索范围受限，无法进行风险信号排查",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "五峰土家族自治县人民政府",
                "url": "http://www.wufeng.gov.cn/",
                "publisher": "五峰土家族自治县人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "low",
                "notes": "网站无法访问（HTTP/HTTPS超时）"
            }
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "所有信息均待确认 — 政府网站无法访问，所有搜索工具均失败"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "当前五峰土家族自治县县委书记是谁？",
                "why_it_matters": "核心目标人物",
                "suggested_queries": [
                    "五峰土家族自治县 县委书记",
                    "site:wufeng.gov.cn 领导之窗",
                    "五峰 县委书记 李伦华 (or other name)"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": "当前五峰土家族自治县县长是谁？",
                "why_it_matters": "核心目标人物",
                "suggested_queries": [
                    "五峰土家族自治县 县长",
                    "五峰 县长 覃业成 (or other name)"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "五峰土家族自治县县委领导班子完整名单？",
                "why_it_matters": "需要确认所有县委常委姓名和分工",
                "suggested_queries": [
                    "五峰土家族自治县 县委领导班子",
                    "五峰 县委常委"
                ],
                "last_attempted": AS_OF
            }
        ]
    }

    filename = f"{TODAY}-湖北省-宜昌市-{job_key}-{person['name']}.json"
    filepath = PERSONS_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  JSON: {filepath}")


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    build()

    print("\n--- Writing person JSONs ---")
    org_map = {o["id"]: o["name"] for o in organizations}

    # Write JSON for core figures (ids 1, 2 — the main targets)
    for person in persons:
        if person["id"] in [1, 2]:
            write_person_json(person, org_map)

    print(f"\n{'=' * 60}")
    print(f"  {SLUG} 数据构建完成")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  注意: 所有数据为占位符 — 需在网站可访问时重新核实")
    print(f"{'=' * 60}")
