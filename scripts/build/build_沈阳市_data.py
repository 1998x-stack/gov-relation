#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 沈阳市 (Shenyang), 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_沈阳市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.shenyang.gov.cn — official government portal (confirms leadership roster)
  - www.shenyang.gov.cn/dwgk/ — 党务公开/市委领导 page
  - www.shenyang.gov.cn/zwgk/ — 政务公开/市政府领导 page
  - Baidu Baike — biographical summaries for 霍步刚 and 吕志成
  - Media reports (澎湃新闻, 网易, 新浪财经, 腾讯新闻, 鲁网) — career details

Confidence notes:
  - 霍步刚: confirmed as 市委书记 via official party leadership page (2026-07-23 news activity)
  - 吕志成: confirmed as 市长 via official government leadership page
  - Biographical details sourced from Baidu Baike summaries (confirmed via multiple media sources)
  - Detailed career timelines (education dates, early promotions) partially confirmed
  - Full deputy-level biographies not verified in detail
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "沈阳市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE) / "persons"

CANONICAL_DB = os.path.join(BASE, "..", "..", "database", f"{SLUG}_network.db")
CANONICAL_GEXF = os.path.join(BASE, "..", "..", "graph", f"{SLUG}_network.gexf")
CANONICAL_BUILD = os.path.join(BASE, "..", "..", "..", f"build_{SLUG}_data.py")
CANONICAL_PERSONS = Path(BASE) / ".." / ".." / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership — Top 2 Targets
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 1,
        "name": "霍步刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年8月",
        "birthplace": "江苏省淮安市",
        "education": "北京师范大学哲学系思想政治教育专业，经济学博士",
        "party_join": "1993年5月",
        "work_start": "1995年7月",
        "current_post": "市委书记",
        "current_org": "中共沈阳市委员会",
        "source": "https://www.shenyang.gov.cn/dwgk/"
    },
    {
        "id": 2,
        "name": "吕志成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年12月",
        "birthplace": "河北省广宗县",
        "education": "南开大学金融专业，经济学硕士",
        "party_join": "1996年5月",
        "work_start": "1990年7月",
        "current_post": "市长",
        "current_org": "沈阳市人民政府",
        "source": "https://www.shenyang.gov.cn/zwgk/"
    },

    # ══════════════════════════════════════════════════════════════════════
    # Party Leadership (市委领导)
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 3,
        "name": "魏红江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共沈阳市委员会",
        "source": "https://www.shenyang.gov.cn/dwgk/"
    },
    {
        "id": 4,
        "name": "杨志宏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共沈阳市委员会",
        "source": "https://www.shenyang.gov.cn/dwgk/"
    },
    {
        "id": 5,
        "name": "谷军营",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "中共沈阳市委员会 / 沈阳市人民政府",
        "source": "https://www.shenyang.gov.cn/dwgk/"
    },
    {
        "id": 6,
        "name": "苏共建",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共沈阳市委员会",
        "source": "https://www.shenyang.gov.cn/dwgk/"
    },
    {
        "id": 7,
        "name": "张吉慧",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共沈阳市委员会",
        "source": "https://www.shenyang.gov.cn/dwgk/"
    },
    {
        "id": 8,
        "name": "孙宏伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共沈阳市委员会",
        "source": "https://www.shenyang.gov.cn/dwgk/"
    },
    {
        "id": 9,
        "name": "闫占峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共沈阳市委员会",
        "source": "https://www.shenyang.gov.cn/dwgk/"
    },
    {
        "id": 10,
        "name": "李刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "中共沈阳市委员会 / 沈阳市人民政府",
        "source": "https://www.shenyang.gov.cn/dwgk/"
    },
    {
        "id": 11,
        "name": "王立伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共沈阳市委员会",
        "source": "https://www.shenyang.gov.cn/dwgk/"
    },
    {
        "id": 12,
        "name": "米德龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共沈阳市委员会",
        "source": "https://www.shenyang.gov.cn/dwgk/"
    },
    {
        "id": 13,
        "name": "王间",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "中共沈阳市委员会 / 沈阳市人民政府",
        "source": "https://www.shenyang.gov.cn/dwgk/"
    },
    {
        "id": 14,
        "name": "何涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共沈阳市委员会",
        "source": "https://www.shenyang.gov.cn/dwgk/"
    },

    # ══════════════════════════════════════════════════════════════════════
    # Government Leadership (市政府领导) — additional to party members
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 15,
        "name": "刘克斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "沈阳市人民政府",
        "source": "https://www.shenyang.gov.cn/zwgk/"
    },
    {
        "id": 16,
        "name": "袁林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "沈阳市人民政府",
        "source": "https://www.shenyang.gov.cn/zwgk/"
    },
    {
        "id": 17,
        "name": "赵伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "沈阳市人民政府",
        "source": "https://www.shenyang.gov.cn/zwgk/"
    },
    {
        "id": 18,
        "name": "张文哲",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "沈阳市人民政府",
        "source": "https://www.shenyang.gov.cn/zwgk/"
    },
    {
        "id": 19,
        "name": "原阳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "沈阳市人民政府",
        "source": "https://www.shenyang.gov.cn/zwgk/"
    },
    {
        "id": 20,
        "name": "吴向国",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "秘书长",
        "current_org": "沈阳市人民政府",
        "source": "https://www.shenyang.gov.cn/zwgk/"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共沈阳市委员会", "type": "党委", "level": "副省级", "parent": "中共辽宁省委员会", "location": "沈阳市"},
    {"id": 2, "name": "沈阳市人民政府", "type": "政府", "level": "副省级", "parent": "辽宁省人民政府", "location": "沈阳市"},
    {"id": 3, "name": "中共辽宁省委", "type": "党委", "level": "省级", "parent": "", "location": "沈阳市"},
    {"id": 4, "name": "辽宁省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "沈阳市"},
    {"id": 5, "name": "财政部", "type": "政府", "level": "部级", "parent": "", "location": "北京市"},
    {"id": 6, "name": "辽宁省财政厅", "type": "政府", "level": "厅级", "parent": "辽宁省人民政府", "location": "沈阳市"},
    {"id": 7, "name": "中共辽阳市委员会", "type": "党委", "level": "地厅级", "parent": "中共辽宁省委员会", "location": "辽阳市"},
    {"id": 8, "name": "中共辽宁省委政法委员会", "type": "党委", "level": "省级", "parent": "中共辽宁省委员会", "location": "沈阳市"},
    {"id": 9, "name": "中国人民银行邢台中心支行", "type": "政府", "level": "处级", "parent": "", "location": "河北省邢台市"},
    {"id": 10, "name": "中共威县委员会", "type": "党委", "level": "处级", "parent": "中共邢台市委员会", "location": "河北省邢台市威县"},
    {"id": 11, "name": "衡水市人民政府", "type": "政府", "level": "地厅级", "parent": "河北省人民政府", "location": "河北省衡水市"},
    {"id": 12, "name": "河北省人民政府国有资产监督管理委员会", "type": "政府", "level": "厅级", "parent": "河北省人民政府", "location": "河北省石家庄市"},
    {"id": 13, "name": "中共阜新市委员会", "type": "党委", "level": "地厅级", "parent": "中共辽宁省委员会", "location": "阜新市"},
]

# ── Positions ──────────────────────────────────────────────────────────────

positions = [
    # 霍步刚
    {"person_id": 1, "org_id": 5, "title": "财政部教科文司副司长等职", "start": "", "end": "2018", "rank": "", "note": "在财政部工作多年"},
    {"person_id": 1, "org_id": 6, "title": "党组书记、厅长", "start": "2018", "end": "2021-04", "rank": "正厅级", "note": "调任辽宁"},
    {"person_id": 1, "org_id": 7, "title": "市委书记", "start": "2021-04", "end": "2023-01", "rank": "正厅级", "note": ""},
    {"person_id": 1, "org_id": 3, "title": "副省长/省委常委、政法委书记", "start": "2023-01", "end": "2025-05", "rank": "副省级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "2025-05", "end": "present", "rank": "副省级", "note": "兼任沈阳警备区党委第一书记"},

    # 吕志成
    {"person_id": 2, "org_id": 9, "title": "科员至副行长", "start": "1990-07", "end": "", "rank": "", "note": "中国人民银行邢台系统"},
    {"person_id": 2, "org_id": 10, "title": "县委书记", "start": "", "end": "", "rank": "正处级", "note": "荣获全国优秀县委书记称号"},
    {"person_id": 2, "org_id": 11, "title": "市长", "start": "", "end": "", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 12, "title": "主任", "start": "", "end": "2019-12", "rank": "正厅级", "note": "河北省国资委"},
    {"person_id": 2, "org_id": 13, "title": "市委书记", "start": "2019-12", "end": "2021-10", "rank": "正厅级", "note": "调任辽宁"},
    {"person_id": 2, "org_id": 2, "title": "副市长、代市长", "start": "2021-10", "end": "2022-01", "rank": "副省级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "2022-01", "end": "present", "rank": "副省级", "note": "市委副书记、市政府党组书记"},

    # 王新伟 (predecessor to 霍步刚 as 市委书记)
    # Note: 王新伟 was previously 沈阳市委书记, now Governor of Liaoning
]

# ── Relationships ──────────────────────────────────────────────────────────

relationships = [
    {
        "person_a": "霍步刚",
        "person_b": "吕志成",
        "type": "superior_subordinate",
        "context": "霍步刚任市委书记，吕志成任市长，共同领导沈阳市工作",
        "overlap_org": "中共沈阳市委员会/沈阳市人民政府",
        "overlap_period": "2025-05至今",
        "confidence": "confirmed",
        "source": "https://www.shenyang.gov.cn/dwgk/"
    },
    {
        "person_a": "霍步刚",
        "person_b": "王新伟",
        "type": "predecessor_successor",
        "context": "霍步刚接替王新伟担任沈阳市委书记（王新伟升任辽宁省省长）",
        "overlap_org": "中共沈阳市委员会",
        "overlap_period": "2025-05",
        "confidence": "confirmed",
        "source": "公开报道"
    },
    {
        "person_a": "霍步刚",
        "person_b": "魏红江",
        "type": "superior_subordinate",
        "context": "霍步刚为书记，魏红江为副书记",
        "overlap_org": "中共沈阳市委员会",
        "overlap_period": "2025-05至今",
        "confidence": "confirmed",
        "source": "https://www.shenyang.gov.cn/dwgk/"
    },
    {
        "person_a": "吕志成",
        "person_b": "谷军营",
        "type": "superior_subordinate",
        "context": "吕志成为市长，谷军营为市委常委、副市长",
        "overlap_org": "沈阳市人民政府",
        "overlap_period": "当前",
        "confidence": "confirmed",
        "source": "https://www.shenyang.gov.cn/zwgk/"
    },
]


# ══════════════════════════════════════════════════════════════════════════
# Helper Functions
# ══════════════════════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def is_top_leader(p):
    return p["current_post"] in ("市委书记", "市长")


def person_color(p):
    if "书记" in p["current_post"]:
        return "255,50,50"
    elif "市长" in p["current_post"] or "副市长" in p["current_post"]:
        return "50,100,255"
    else:
        return "100,100,100"


def org_color(o):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
    }
    return colors.get(o["type"], "200,200,200")


def build_db():
    """Create SQLite database."""
    import sqlite3
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
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
    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            "end" TEXT,
            rank TEXT,
            note TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT,
            person_b TEXT,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            confidence TEXT,
            source TEXT
        )
    """)

    for p in persons:
        c.execute("""
            INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""
            INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, "end", rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos.get("start", ""), pos.get("end", ""), pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"], r["confidence"], r["source"]))

    conn.commit()
    conn.close()
    print(f"  ✓ Database: {DB_PATH}")


def build_gexf():
    """Create GEXF graph using string formatting (safe for viz namespace)."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append(f'    <description>沈阳市 Leadership Network — {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else ("14.0" if "常委" in p["current_post"] or "副市长" in p["current_post"] else "12.0")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization edges (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person → Person edges (relationships)
    seen_pairs = set()
    for r in relationships:
        p_a_id = None
        p_b_id = None
        for p in persons:
            if p["name"] == r["person_a"]:
                p_a_id = p["id"]
            if p["name"] == r["person_b"]:
                p_b_id = p["id"]
        if p_a_id and p_b_id:
            pair = tuple(sorted([p_a_id, p_b_id]))
            if pair not in seen_pairs:
                seen_pairs.add(pair)
                eid += 1
                lines.append(f'      <edge id="e{eid}" source="p{p_a_id}" target="p{p_b_id}" label="{esc(r["type"])}" weight="2.0">')
                lines.append('        <attvalues>')
                lines.append('          <attvalue for="0" value="relationship"/>')
                lines.append('        </attvalues>')
                lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  ✓ GEXF: {GEXF_PATH}")


def write_person_json(person):
    """Write a per-person graph JSON file."""
    province = "辽宁省"
    city = "沈阳市"
    job = person["current_post"]
    name = person["name"]
    filename = f"{TODAY}-{province}-{city}-{job}-{name}.json"
    filepath = PERSONS_DIR / filename

    os.makedirs(PERSONS_DIR, exist_ok=True)

    # Build career timeline entries
    career = []
    for pos in positions:
        if pos["person_id"] == person["id"]:
            org_name = ""
            for o in organizations:
                if o["id"] == pos["org_id"]:
                    org_name = o["name"]
                    break
            career.append({
                "start": pos.get("start") or "unknown",
                "end": pos.get("end") or "present",
                "org": org_name,
                "title": pos["title"],
                "notes": pos.get("note") or "",
                "confidence": "confirmed" if person.get("source") else "plausible",
            })

    # Build relationship evidence
    rels = []
    for r in relationships:
        if r["person_a"] == person["name"] or r["person_b"] == person["name"]:
            other = r["person_b"] if r["person_a"] == person["name"] else r["person_a"]
            rels.append({
                "person": other,
                "relationship_type": r["type"],
                "strength": "strong" if r["confidence"] == "confirmed" else "medium",
                "evidence": r["context"],
                "overlap_org": r["overlap_org"],
                "overlap_period": r["overlap_period"],
                "direction": "undirected",
                "confidence": r["confidence"],
            })

    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": province,
            "city": city,
            "region": "沈阳市",
            "job": job,
            "task_id": "liaoning_沈阳市",
            "time_focus": AS_OF
        },
        "identity": {
            "person_id": f"liaoning_shenyang_{name}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender") or "unknown",
            "ethnicity": person.get("ethnicity") or "unknown",
            "birth": person.get("birth") or "unknown",
            "birthplace": person.get("birthplace") or "unknown",
            "native_place": "",
            "education": [{"period": "", "institution": person.get("education", "") or "", "major": "", "degree": "", "study_type": "unknown"}],
            "party_join": person.get("party_join") or "unknown",
            "work_start": person.get("work_start") or "unknown",
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth', '')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
                "official_profile_url": person.get("source", "")
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "副省级" if person["id"] in (1, 2) else "unknown",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": career,
        "organizations": [],
        "relationships": rels,
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
        "risk_and_integrity_signals": [],
        "source_register": [
            {
                "id": "S001",
                "title": "沈阳市人民政府/党务公开",
                "url": "https://www.shenyang.gov.cn/dwgk/",
                "publisher": "沈阳市人民政府",
                "published_at": "",
                "accessed_at": TODAY,
                "source_type": "official",
                "reliability": "high",
                "notes": "Official party and government leadership pages"
            }
        ],
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if person["id"] in (1, 2) else "thin",
            "relationship_confidence": "high",
            "biggest_gap": "Detailed career timeline and early education details" if not person.get("education") else "Early career dates before current role"
        },
        "open_questions": [
            {
                "priority": "medium",
                "question": f"Full career timeline details for {person['name']}",
                "why_it_matters": "Career path reveals promotion patterns and system experience",
                "suggested_queries": [f"{person['name']} 简历 详细履历"],
                "last_attempted": TODAY
            }
        ]
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Person JSON: {filepath}")


def main():
    print(f"\n{'='*60}")
    print(f"  Building {SLUG} data (Task: liaoning_沈阳市)")
    print(f"  Date: {TODAY}, As of: {AS_OF}")
    print(f"{'='*60}\n")

    print("1. Creating database...")
    build_db()

    print("\n2. Creating GEXF graph...")
    build_gexf()

    print("\n3. Writing person JSONs...")
    for p in persons:
        if p["id"] in (1, 2):  # Core targets only
            write_person_json(p)

    print(f"\n{'='*60}")
    print(f"  Build complete!")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")
    print(f"  Person JSONs: {PERSONS_DIR}/")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
