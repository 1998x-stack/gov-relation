#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 望奎县 (Wangku County), 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_望奎县
Level: 县
Parent city: 绥化市
Targets: 县委书记 & 县长

Research sources:
  - Wikipedia (zh.wikipedia.org) — 望奎县 basic geography and admin divisions
  - No official government leadership page could be accessed (wangku.gov.cn unreachable/HTTP timeouts)
  - Exa search was rate-limited; Baidu returned CAPTCHA; Jina Reader timed out
  - Suihua government site (suihua.gov.cn) unreachable

Confidence notes:
  - 望奎县 geography and administrative divisions: confirmed via Wikipedia
  - Current county leadership (县委书记 & 县长): detailed biographies could NOT be verified
    due to complete web access failure for this region
  - This artifact set uses placeholder/pending data for the core leadership with
    clear uncertainty markers
  - All confidence labels marked "unverified" where web evidence is absent
  - A dedicated deep-dive is needed when official sites become accessible
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "望奎县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / "scripts" / "build" / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# ══════════════════════════════════════════════════════════════════════════
# Persons
# ══════════════════════════════════════════════════════════════════════════
# NOTE: Due to complete web access failure for 望奎县 (wangku.gov.cn unreachable,
# Exa/Baidu/Jina all blocked/timeout), the current county leadership names are
# UNVERIFIED. The placeholder entries below reflect the known office structure.
# A follow-up investigation is REQUIRED once sites become accessible.

persons = [
    # ═══════ Core Leadership — 县委书记 & 县长 ═══════
    # These entries are placeholders until web evidence can be obtained.
    # 望奎县官方网站 (wangku.gov.cn) 领导之窗页面无法访问。

    {
        "id": 1,
        "name": "待确认 (县委书记)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共望奎县委员会",
        "source": "待查 — 望奎县人民政府官网领导之窗 (www.wangku.gov.cn/wk/ldzc/) 当前不可达"
    },
    {
        "id": 2,
        "name": "待确认 (县长)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县长",
        "current_org": "望奎县人民政府",
        "source": "待查 — 望奎县人民政府官网领导之窗 (www.wangku.gov.cn/wk/ldzc/) 当前不可达"
    },

    # ═══════ Key Deputy Leadership (placeholder) ═══════
    {
        "id": 3,
        "name": "待确认 (常务副县长)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "望奎县人民政府",
        "source": "待查"
    },
    {
        "id": 4,
        "name": "待确认 (县人大常委会主任)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "望奎县人民代表大会常务委员会",
        "source": "待查"
    },
    {
        "id": 5,
        "name": "待确认 (县政协主席)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议望奎县委员会",
        "source": "待查"
    },
    {
        "id": 6,
        "name": "待确认 (县纪委书记)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共望奎县纪律检查委员会",
        "source": "待查"
    },
    {
        "id": 7,
        "name": "待确认 (县委副书记)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共望奎县委员会",
        "source": "待查"
    },
]

# ══════════════════════════════════════════════════════════════════════════
# Organizations
# ══════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共望奎县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共绥化市委员会",
        "location": "望奎县"
    },
    {
        "id": 2,
        "name": "望奎县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "绥化市人民政府",
        "location": "望奎县"
    },
    {
        "id": 3,
        "name": "望奎县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "绥化市人民代表大会常务委员会",
        "location": "望奎县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议望奎县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "中国人民政治协商会议绥化市委员会",
        "location": "望奎县"
    },
    {
        "id": 5,
        "name": "中共望奎县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共绥化市纪律检查委员会",
        "location": "望奎县"
    },
    {
        "id": 6,
        "name": "中共绥化市委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中共黑龙江省委员会",
        "location": "绥化市"
    },
    {
        "id": 7,
        "name": "绥化市人民政府",
        "type": "政府",
        "level": "地级",
        "parent": "黑龙江省人民政府",
        "location": "绥化市"
    },
    {
        "id": 8,
        "name": "绥化市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级",
        "parent": "黑龙江省人民代表大会常务委员会",
        "location": "绥化市"
    },
    {
        "id": 9,
        "name": "中国人民政治协商会议绥化市委员会",
        "type": "政协",
        "level": "地级",
        "parent": "中国人民政治协商会议黑龙江省委员会",
        "location": "绥化市"
    },
    # 望奎县下辖乡镇 (from Wikipedia - confirmed)
    {
        "id": 10,
        "name": "望奎镇",
        "type": "乡镇/街道",
        "level": "乡镇级",
        "parent": "望奎县人民政府",
        "location": "望奎县"
    },
    {
        "id": 11,
        "name": "通江镇",
        "type": "乡镇/街道",
        "level": "乡镇级",
        "parent": "望奎县人民政府",
        "location": "望奎县"
    },
    {
        "id": 12,
        "name": "卫星镇",
        "type": "乡镇/街道",
        "level": "乡镇级",
        "parent": "望奎县人民政府",
        "location": "望奎县"
    },
    {
        "id": 13,
        "name": "海丰镇",
        "type": "乡镇/街道",
        "level": "乡镇级",
        "parent": "望奎县人民政府",
        "location": "望奎县"
    },
    {
        "id": 14,
        "name": "莲花镇",
        "type": "乡镇/街道",
        "level": "乡镇级",
        "parent": "望奎县人民政府",
        "location": "望奎县"
    },
    {
        "id": 15,
        "name": "惠七满族镇",
        "type": "乡镇/街道",
        "level": "乡镇级",
        "parent": "望奎县人民政府",
        "location": "望奎县"
    },
    {
        "id": 16,
        "name": "先锋镇",
        "type": "乡镇/街道",
        "level": "乡镇级",
        "parent": "望奎县人民政府",
        "location": "望奎县"
    },
    {
        "id": 17,
        "name": "火箭镇",
        "type": "乡镇/街道",
        "level": "乡镇级",
        "parent": "望奎县人民政府",
        "location": "望奎县"
    },
    {
        "id": 18,
        "name": "东郊镇",
        "type": "乡镇/街道",
        "level": "乡镇级",
        "parent": "望奎县人民政府",
        "location": "望奎县"
    },
    {
        "id": 19,
        "name": "灯塔镇",
        "type": "乡镇/街道",
        "level": "乡镇级",
        "parent": "望奎县人民政府",
        "location": "望奎县"
    },
    {
        "id": 20,
        "name": "灵山满族乡",
        "type": "乡镇/街道",
        "level": "乡镇级",
        "parent": "望奎县人民政府",
        "location": "望奎县"
    },
    {
        "id": 21,
        "name": "后三乡",
        "type": "乡镇/街道",
        "level": "乡镇级",
        "parent": "望奎县人民政府",
        "location": "望奎县"
    },
    {
        "id": 22,
        "name": "东升乡",
        "type": "乡镇/街道",
        "level": "乡镇级",
        "parent": "望奎县人民政府",
        "location": "望奎县"
    },
    {
        "id": 23,
        "name": "恭六乡",
        "type": "乡镇/街道",
        "level": "乡镇级",
        "parent": "望奎县人民政府",
        "location": "望奎县"
    },
    {
        "id": 24,
        "name": "厢白满族乡",
        "type": "乡镇/街道",
        "level": "乡镇级",
        "parent": "望奎县人民政府",
        "location": "望奎县"
    },
]

# ══════════════════════════════════════════════════════════════════════════
# Positions
# ══════════════════════════════════════════════════════════════════════════
# All positions are UNVERIFIED — based on standard county leadership structure.
# Names and exact tenure need official source confirmation.

positions = [
    # Core leadership — placeholder positions
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "未确认——望奎县政府官网不可达"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "未确认——望奎县政府官网不可达"},

    # Deputy leadership — placeholder positions
    {"person_id": 3, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "未确认"},
    {"person_id": 4, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "未确认"},
    {"person_id": 5, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": "未确认"},
    {"person_id": 6, "org_id": 5, "title": "县委常委、县纪委书记、县监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "未确认"},
    {"person_id": 7, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "未确认"},
]

# ══════════════════════════════════════════════════════════════════════════
# Relationships
# ══════════════════════════════════════════════════════════════════════════
# Standard governance relationships — all unverified pending name confirmation.

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长为望奎县党政主要领导搭档关系",
        "overlap_org": "望奎县",
        "overlap_period": "至今"
    },
    {
        "person_a": 1, "person_b": 7,
        "type": "superior_subordinate",
        "context": "县委书记与县委副书记为县委领导班子搭档",
        "overlap_org": "中共望奎县委员会",
        "overlap_period": "至今"
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与常务副县长为党政领导关系",
        "overlap_org": "望奎县",
        "overlap_period": "至今"
    },
    {
        "person_a": 1, "person_b": 6,
        "type": "superior_subordinate",
        "context": "县委书记与纪委书记为县委领导班子搭档",
        "overlap_org": "中共望奎县委员会",
        "overlap_period": "至今"
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "superior_subordinate",
        "context": "县长与常务副县长为县政府领导班子搭档",
        "overlap_org": "望奎县人民政府",
        "overlap_period": "至今"
    },
    {
        "person_a": 2, "person_b": 7,
        "type": "overlap",
        "context": "县长与县委副书记跨党政系统共事",
        "overlap_org": "望奎县",
        "overlap_period": "至今"
    },
    {
        "person_a": 4, "person_b": 5,
        "type": "overlap",
        "context": "县人大常委会主任与县政协主席同为县级正职领导",
        "overlap_org": "望奎县",
        "overlap_period": "至今"
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "overlap",
        "context": "县委书记与县人大常委会主任为党政人大系统交叉",
        "overlap_org": "望奎县",
        "overlap_period": "至今"
    },
    {
        "person_a": 1, "person_b": 5,
        "type": "overlap",
        "context": "县委书记与县政协主席为党政政协系统交叉",
        "overlap_org": "望奎县",
        "overlap_period": "至今"
    },
]


# ══════════════════════════════════════════════════════════════════════════
# Helper: XML escape
# ══════════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ══════════════════════════════════════════════════════════════════════════
# Build database
# ══════════════════════════════════════════════════════════════════════════

def build_db(db_path):
    import sqlite3

    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    cur.execute("PRAGMA foreign_keys = ON;")
    cur.execute("PRAGMA encoding = 'UTF-8';")

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
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
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
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
            start_date TEXT,
            end_date TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    # Insert persons
    for p in persons:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
             p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"])
        )

    # Insert organizations
    for o in organizations:
        cur.execute(
            "INSERT INTO organizations (id, name, type, level, parent, location) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
        )

    # Insert positions
    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"],
             pos["end_date"], pos["rank"], pos["note"])
        )

    # Insert relationships
    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (r["person_a"], r["person_b"], r["type"], r["context"],
             r["overlap_org"], r["overlap_period"])
        )

    conn.commit()
    conn.close()


# ══════════════════════════════════════════════════════════════════════════
# Build GEXF
# ══════════════════════════════════════════════════════════════════════════

def person_color(p):
    """Return 'r,g,b' string for a person node based on role."""
    role = p.get("current_post", "")
    if "书记" in role and "纪委" not in role and "县委" in role or "书记" in role and "县委" in role:
        return "255,50,50"      # Red — Party Secretary
    elif "县长" in role or "区长" in role or "市长" in role:
        return "50,100,255"     # Blue — Mayor/County Head
    elif "纪委书记" in role or "监委" in role or "纪委" in role:
        return "255,165,0"      # Orange — Discipline Inspection
    else:
        return "100,100,100"    # Grey — Others


def org_color(o):
    """Return 'r,g,b' string for an organization node."""
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"    # Pink
    elif "政府" in t:
        return "200,200,255"    # Light blue
    elif "人大" in t:
        return "200,255,255"    # Cyan
    elif "政协" in t:
        return "255,240,200"    # Cream
    elif "开发区" in t:
        return "200,255,200"    # Light green
    elif "乡镇" in t or "街道" in t:
        return "255,255,200"    # Light yellow
    elif "事业" in t:
        return "220,220,220"    # Light grey
    elif "群团" in t:
        return "255,220,255"    # Light purple
    else:
        return "200,200,200"


def is_top_leader(p):
    role = p.get("current_post", "")
    return "书记" in role or "县长" in role


def build_gexf(gexf_path):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append(f'    <description>望奎县 Personnel Network — 黑龙江省绥化市 (investigation: {AS_OF})</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="level" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="县级"/>')
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
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person ↔ Person (relationship)
    for r in relationships:
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(str(gexf_path), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ══════════════════════════════════════════════════════════════════════════
# Write person JSON
# ══════════════════════════════════════════════════════════════════════════

def write_person_json(person, persons_dir, confidence="unverified"):
    """Write per-person graph JSON file."""
    job = person["current_post"].replace("、", "_").replace("，", "_").replace(" ", "")
    name = person["name"].replace(" ", "")
    filename = f"{TODAY}-黑龙江省-绥化市-{job}-{name}.json"
    filepath = persons_dir / filename

    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "绥化市",
            "region": "望奎县",
            "job": person["current_post"],
            "task_id": "heilongjiang_望奎县",
            "time_focus": "current"
        },
        "identity": {
            "person_id": f"wangku_{person['id']}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"] or "",
            "ethnicity": person["ethnicity"] or "",
            "birth": person["birth"] or "",
            "birthplace": person["birthplace"] or "",
            "native_place": "",
            "education": [],
            "party_join": person["party_join"] or "",
            "work_start": person["work_start"] or "",
            "dedupe_keys": {
                "name_birth": "",
                "name_birthplace": "",
                "official_profile_url": "https://www.wangku.gov.cn/wk/ldzc/"
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if "书记" in person["current_post"] or "县长" in person["current_post"] else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": []
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": "公开资料未找到该人物的任何任职履历。望奎县政府官网(www.wangku.gov.cn)领导之窗页面无法访问",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "无可用信息",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "unknown",
                    "evidence": "因官网和搜索工具均无法获取信息，该人物工作风格无任何公开线索",
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "因网站无法访问和搜索工具受限，未发现风险信号",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "望奎县人民政府 — 领导之窗",
                "url": "https://www.wangku.gov.cn/wk/ldzc/",
                "publisher": "望奎县人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "页面无法访问（HTTP timeout）"
            },
            {
                "id": "S002",
                "title": "绥化市人民政府 — 领导之窗",
                "url": "https://www.suihua.gov.cn/sh/ldzc/",
                "publisher": "绥化市人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "页面无法访问（HTTP timeout）"
            }
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "县委书记和县长的姓名、性别、民族、出生年月、教育背景、全部履历均未知"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"望奎县{person['current_post']}的姓名是什么？",
                "why_it_matters": "这是本次调查的核心目标人物——县党政一把手",
                "suggested_queries": [
                    "望奎县 现任 县委书记",
                    "site:wangku.gov.cn 领导 分工",
                    "绥化市 望奎县 领导之窗",
                    "望奎县 人大 任命 县长"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"{person['current_post']}的出生年月、民族、籍贯是什么？",
                "why_it_matters": "基本的身份标识信息，用于人物去重和履历分析",
                "suggested_queries": [
                    f"望奎县{person['current_post']} 简历",
                    f"望奎县{person['current_post']} 出生"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"{person['current_post']}的教育背景（毕业院校、专业、学历）是什么？",
                "why_it_matters": "教育背景影响职业路径和专业化判断",
                "suggested_queries": [],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": f"{person['current_post']}的完整职业生涯（历任职务及起止时间）是什么？",
                "why_it_matters": "完整的履历是构建人物关系网络的基础",
                "suggested_queries": [],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"望奎县前任{person['current_post']}是谁？去向如何？",
                "why_it_matters": "了解望奎县人事更替模式和跨县/市调动路径",
                "suggested_queries": [
                    "望奎县 前任 县委书记",
                    "望奎县 前任 县长"
                ],
                "last_attempted": AS_OF
            }
        ]
    }

    with open(str(filepath), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return filepath


# ══════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════

def main():
    print(f"Building data for {SLUG}...")

    # Build database
    print(f"  Writing DB: {DB_PATH}")
    build_db(DB_PATH)
    print(f"    OK — {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # Build GEXF
    print(f"  Writing GEXF: {GEXF_PATH}")
    build_gexf(GEXF_PATH)
    print(f"    OK")

    # Write person JSON for core leaders
    person_files = []
    for p in persons:
        if p["id"] in (1, 2):  # Only write for core leaders
            pf = write_person_json(p, PERSONS_DIR, confidence="unverified")
            person_files.append(str(pf))
            print(f"  Person JSON: {pf.name}")

    # Verify outputs
    db_size = os.path.getsize(str(DB_PATH))
    gexf_size = os.path.getsize(str(GEXF_PATH))
    print(f"\n  DB size: {db_size:,} bytes")
    print(f"  GEXF size: {gexf_size:,} bytes")

    print(f"\nDone! Artifacts in {STAGING_DIR}")
    print(f"  Run: python3 scripts/process_tmp.py data/tmp/heilongjiang_望奎县")
    print(f"  Then: python3 scripts/process_tmp.py data/tmp/heilongjiang_望奎县 --apply")


if __name__ == "__main__":
    main()
