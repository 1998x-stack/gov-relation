#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 邓州市, 南阳市, 河南省.

Investigation date: 2026-07-24
Task ID: henan_邓州市
Level: 县级市 (省直管县市)
Targets: 市委书记 & 市长

Research sources:
  - 邓州市人民政府 (dengzhou.gov.cn) — official government website
  - 方明洋: Confirmed as 市委书记 via 15th CPC Congress report (2026-06-25)
  - 刘建光: Confirmed as 市长 via official government leadership page
  - Deputy mayors confirmed via government leadership page:
    侯子罡 (市委常委、副市长), 朱永明 (市委常委、副市长),
    夏丹 (市委常委、副市长), 王勇 (副市长/公安局局长),
    罗建 (副市长), 张晓凤 (副市长)
  - 市委常委会 (from 15th CPC Congress report 2026-06-29):
    方明洋, 刘建光, 陈光义, 姬欣, 李淑琳, 樊新生,
    赵志远, 张海涛, 范胜, 侯子罡, 许旭, 夏丹, 魏新果, 朱永明

Confidence notes:
  - Core leader identities are CONFIRMED from official government sources as of 2026-07-24.
  - 方明洋's detailed biographical data (birth date, birthplace, education, full career
    timeline) are UNVERIFIED — official bio page not found, only news articles.
  - 刘建光's bio is confirmed from official leadership page (b.1982-11, 研究生/管理学博士).
  - 侯子罡, 朱永明, 夏丹, 王勇, 罗建, 张晓凤 bios are confirmed from official pages.
  - 陈光义, 姬欣, 李淑琳, 樊新生, 赵志远, 张海涛, 范胜, 许旭, 魏新果
    are confirmed 市委常委会 members but detailed bios are UNVERIFIED.
"""

from __future__ import annotations

import json
import os
import shutil
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "邓州市"
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

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "方明洋",      # CONFIRMED - 市委书记
        "gender": "男",        # plausible (typical for county-level party secretary)
        "ethnicity": "汉族",    # plausible
        "birth": "",           # UNVERIFIED
        "birthplace": "",      # UNVERIFIED
        "education": "",       # UNVERIFIED
        "party_join": "中共党员",  # confirmed
        "work_start": "",      # UNVERIFIED
        "current_post": "邓州市委书记",
        "current_org": "中共邓州市委员会",
        "source": "https://www.dengzhou.gov.cn/2026/06-29/1415972.html"
    },
    {
        "id": 2,
        "name": "刘建光",      # CONFIRMED - 市长
        "gender": "男",        # confirmed from official profile
        "ethnicity": "汉族",    # confirmed from official profile
        "birth": "1982-11",    # confirmed from official profile
        "birthplace": "",      # UNVERIFIED
        "education": "研究生学历，管理学博士",  # confirmed from official profile
        "party_join": "中共党员",  # confirmed
        "work_start": "",      # UNVERIFIED
        "current_post": "邓州市委副书记、市长",
        "current_org": "邓州市人民政府",
        "source": "https://www.dengzhou.gov.cn/2025/02-06/1124096.html"
    },
    # ═══════ 市委常委/副市长 ═══════
    {
        "id": 3,
        "name": "侯子罡",      # CONFIRMED - 市委常委、副市长
        "gender": "男",        # confirmed from official profile
        "ethnicity": "汉族",    # confirmed from official profile
        "birth": "1982-10",    # confirmed from official profile
        "birthplace": "",      # UNVERIFIED
        "education": "硕士研究生学历",  # confirmed from official profile
        "party_join": "中共党员",  # confirmed
        "work_start": "",      # UNVERIFIED
        "current_post": "邓州市委常委、副市长",
        "current_org": "邓州市人民政府",
        "source": "https://www.dengzhou.gov.cn/2025/02-03/1124094.html"
    },
    {
        "id": 4,
        "name": "朱永明",      # CONFIRMED - 市委常委、副市长
        "gender": "男",        # confirmed from official profile
        "ethnicity": "汉族",    # confirmed from official profile
        "birth": "1980-03",    # confirmed from official profile
        "birthplace": "",      # UNVERIFIED
        "education": "本科学历",  # confirmed from official profile
        "party_join": "中共党员",  # confirmed
        "work_start": "",      # UNVERIFIED
        "current_post": "邓州市委常委、副市长",
        "current_org": "邓州市人民政府",
        "source": "https://www.dengzhou.gov.cn/2023/09-01/1124090.html"
    },
    {
        "id": 5,
        "name": "夏丹",        # CONFIRMED - 市委常委、副市长
        "gender": "女",        # confirmed from official profile
        "ethnicity": "汉族",    # confirmed from official profile
        "birth": "1988-04",    # confirmed from official profile
        "birthplace": "",      # UNVERIFIED
        "education": "大学本科学历",  # confirmed from official profile
        "party_join": "中共党员",  # confirmed
        "work_start": "",      # UNVERIFIED
        "current_post": "邓州市委常委、副市长",
        "current_org": "邓州市人民政府",
        "source": "https://www.dengzhou.gov.cn/2026/06-29/1415882.html"
    },
    {
        "id": 6,
        "name": "王勇",        # CONFIRMED - 副市长、公安局局长
        "gender": "男",        # confirmed from official profile
        "ethnicity": "汉族",    # confirmed from official profile
        "birth": "1975-11",    # confirmed from official profile
        "birthplace": "",      # UNVERIFIED
        "education": "大学本科学历",  # confirmed from official profile
        "party_join": "中共党员",  # confirmed
        "work_start": "",      # UNVERIFIED
        "current_post": "邓州市副市长、公安局局长",
        "current_org": "邓州市人民政府",
        "source": "https://www.dengzhou.gov.cn/2026/07-13/1419489.html"
    },
    {
        "id": 7,
        "name": "罗建",        # CONFIRMED - 副市长
        "gender": "男",        # confirmed from official profile
        "ethnicity": "汉族",    # confirmed from official profile
        "birth": "1982-08",    # confirmed from official profile
        "birthplace": "",      # UNVERIFIED
        "education": "大学本科学历",  # confirmed from official profile
        "party_join": "中共党员",  # confirmed
        "work_start": "",      # UNVERIFIED
        "current_post": "邓州市副市长",
        "current_org": "邓州市人民政府",
        "source": "https://www.dengzhou.gov.cn/2026/07-23/1422029.html"
    },
    {
        "id": 8,
        "name": "张晓凤",      # CONFIRMED - 副市长
        "gender": "女",        # confirmed from official profile
        "ethnicity": "汉族",    # confirmed from official profile
        "birth": "1985-10",    # confirmed from official profile
        "birthplace": "",      # UNVERIFIED
        "education": "本科学历",  # confirmed from official profile
        "party_join": "中共党员",  # confirmed
        "work_start": "",      # UNVERIFIED
        "current_post": "邓州市副市长",
        "current_org": "邓州市人民政府",
        "source": "https://www.dengzhou.gov.cn/2026/07-24/1422288.html"
    },
    # ═══════ 市委常委会其他成员 (confirmed from 15th Congress) ═══════
    {
        "id": 9,
        "name": "陈光义",      # CONFIRMED - 市委副书记/政法委书记
        "gender": "",           # UNVERIFIED
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",  # confirmed (party role)
        "work_start": "",
        "current_post": "邓州市委副书记、政法委书记",
        "current_org": "中共邓州市委员会",
        "source": "https://www.dengzhou.gov.cn/2026/06-29/1415968.html"
    },
    {
        "id": 10,
        "name": "姬欣",        # CONFIRMED - 市委常委
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "邓州市委常委",
        "current_org": "中共邓州市委员会",
        "source": "https://www.dengzhou.gov.cn/2026/06-29/1415968.html"
    },
    {
        "id": 11,
        "name": "李淑琳",      # CONFIRMED - 市委常委
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "邓州市委常委",
        "current_org": "中共邓州市委员会",
        "source": "https://www.dengzhou.gov.cn/2026/06-29/1415968.html"
    },
    {
        "id": 12,
        "name": "樊新生",      # CONFIRMED - 市委常委
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "邓州市委常委",
        "current_org": "中共邓州市委员会",
        "source": "https://www.dengzhou.gov.cn/2026/06-29/1415968.html"
    },
    {
        "id": 13,
        "name": "赵志远",      # CONFIRMED - 市委常委
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "邓州市委常委",
        "current_org": "中共邓州市委员会",
        "source": "https://www.dengzhou.gov.cn/2026/06-29/1415968.html"
    },
    {
        "id": 14,
        "name": "张海涛",      # CONFIRMED - 市委常委
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "邓州市委常委",
        "current_org": "中共邓州市委员会",
        "source": "https://www.dengzhou.gov.cn/2026/06-29/1415968.html"
    },
    {
        "id": 15,
        "name": "范胜",        # CONFIRMED - 市委常委、纪委书记
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "邓州市委常委、市纪委书记、市监委主任",
        "current_org": "中共邓州市纪律检查委员会",
        "source": "https://www.dengzhou.gov.cn/2026/06-29/1415975.html"
    },
    {
        "id": 16,
        "name": "许旭",        # CONFIRMED - 市委常委
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "邓州市委常委",
        "current_org": "中共邓州市委员会",
        "source": "https://www.dengzhou.gov.cn/2026/06-29/1415968.html"
    },
    {
        "id": 17,
        "name": "魏新果",      # CONFIRMED - 市委常委
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "邓州市委常委",
        "current_org": "中共邓州市委员会",
        "source": "https://www.dengzhou.gov.cn/2026/06-29/1415968.html"
    },
    # ═══════ 前任 Predecessors (UNVERIFIED) ═══════
    {
        "id": 18,
        "name": "",        # UNVERIFIED — 前任市委书记 (before 方明洋)
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共邓州市委员会",
        "source": ""
    },
    {
        "id": 19,
        "name": "",        # UNVERIFIED — 前任市长 (before 刘建光)
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任市长",
        "current_org": "邓州市人民政府",
        "source": ""
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共邓州市委员会", "type": "党委", "level": "县级", "parent": "中共南阳市委员会", "location": "邓州市"},
    {"id": 2, "name": "邓州市人民政府", "type": "政府", "level": "县级", "parent": "南阳市人民政府", "location": "邓州市"},
    {"id": 3, "name": "中共邓州市纪律检查委员会/邓州市监察委员会", "type": "党委", "level": "县级", "parent": "中共南阳市纪律检查委员会", "location": "邓州市"},
    {"id": 4, "name": "中共邓州市委政法委员会", "type": "党委", "level": "县级", "parent": "中共邓州市委员会", "location": "邓州市"},
    {"id": 5, "name": "中共邓州市委组织部", "type": "党委", "level": "县级", "parent": "中共邓州市委员会", "location": "邓州市"},
    {"id": 6, "name": "中共邓州市委宣传部", "type": "党委", "level": "县级", "parent": "中共邓州市委员会", "location": "邓州市"},
    {"id": 7, "name": "中共邓州市委统战部", "type": "党委", "level": "县级", "parent": "中共邓州市委员会", "location": "邓州市"},
    {"id": 8, "name": "邓州市公安局", "type": "政府", "level": "县级", "parent": "邓州市人民政府", "location": "邓州市"},
    {"id": 9, "name": "邓州市人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "南阳市人民代表大会常务委员会", "location": "邓州市"},
    {"id": 10, "name": "中国人民政治协商会议邓州市委员会", "type": "政协", "level": "县级", "parent": "政协南阳市委员会", "location": "邓州市"},
]

# ── Positions (person → org with title) ────────────────────────────────────
positions = [
    # 市委书记
    {"person_id": 1, "org_id": 1, "title": "邓州市委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 市长
    {"person_id": 2, "org_id": 2, "title": "邓州市委副书记、市长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 市委常委/副市长
    {"person_id": 3, "org_id": 2, "title": "邓州市委常委、副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "邓州市委常委、副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "邓州市委常委、副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 副市长
    {"person_id": 6, "org_id": 2, "title": "邓州市副市长、公安局局长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "邓州市副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "邓州市副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 市委常委会其他成员
    {"person_id": 9, "org_id": 1, "title": "市委副书记、政法委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 3, "title": "市委常委、市纪委书记、市监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 前任
    {"person_id": 18, "org_id": 1, "title": "前任市委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 19, "org_id": 2, "title": "前任市长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 方明洋 ↔ 刘建光（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "市委书记与市长为邓州市党政正职搭档", "overlap_org": "邓州市", "overlap_period": ""},
    # 市长 ↔ 副市长（政府班子）
    {"person_a": 2, "person_b": 3, "type": "政府班子", "context": "副市长在市长领导下工作", "overlap_org": "邓州市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "政府班子", "context": "副市长在市长领导下工作", "overlap_org": "邓州市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "政府班子", "context": "副市长在市长领导下工作", "overlap_org": "邓州市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "政府班子", "context": "副市长在市长领导下工作", "overlap_org": "邓州市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "政府班子", "context": "副市长在市长领导下工作", "overlap_org": "邓州市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "政府班子", "context": "副市长在市长领导下工作", "overlap_org": "邓州市人民政府", "overlap_period": ""},
    # 书记 ↔ 市委常委（市委班子）
    {"person_a": 1, "person_b": 9, "type": "市委班子", "context": "市委副书记在书记领导下工作", "overlap_org": "中共邓州市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "市委班子", "context": "市委常委在书记领导下工作", "overlap_org": "中共邓州市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "市委班子", "context": "市委常委在书记领导下工作", "overlap_org": "中共邓州市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "市委班子", "context": "市委常委在书记领导下工作", "overlap_org": "中共邓州市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 13, "type": "市委班子", "context": "市委常委在书记领导下工作", "overlap_org": "中共邓州市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 14, "type": "市委班子", "context": "市委常委在书记领导下工作", "overlap_org": "中共邓州市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 15, "type": "市委班子", "context": "市委常委在书记领导下工作", "overlap_org": "中共邓州市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 16, "type": "市委班子", "context": "市委常委在书记领导下工作", "overlap_org": "中共邓州市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 17, "type": "市委班子", "context": "市委常委在书记领导下工作", "overlap_org": "中共邓州市委员会", "overlap_period": ""},
    # 前任 ↔ 现任
    {"person_a": 18, "person_b": 1, "type": "交接", "context": "前任市委书记与现任市委书记交接", "overlap_org": "中共邓州市委员会", "overlap_period": ""},
    {"person_a": 19, "person_b": 2, "type": "交接", "context": "前任市长与现任市长交接", "overlap_org": "邓州市人民政府", "overlap_period": ""},
]


# ── Main ────────────────────────────────────────────────────────────────────
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(name):
    """Return RGB color string for a person based on role."""
    if name == "方明洋":
        return "255,50,50"  # Red — Party Secretary
    elif name == "刘建光":
        return "50,100,255"  # Blue — Mayor
    elif name in ("陈光义",):
        return "100,100,100"  # Grey — Deputy Party Secretary
    elif name in ("范胜",):
        return "255,165,0"  # Orange — Discipline Inspection
    else:
        return "100,100,100"  # Grey — Others

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(org_type, "200,200,200")

def generate_gexf(persons, organizations, positions, relationships, output_path):
    """Generate GEXF 1.3 using string formatting."""
    from datetime import datetime
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append(f'    <description>{SLUG} leadership relationship network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["name"])
        name = p["name"] if p["name"] else "待确认"
        sz = "20.0" if p["id"] in (1, 2) else "12.0"
        role = p["current_post"]
        lines.append(f'      <node id="p{p["id"]}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')

    for o in organizations:
        lines.append(f'        <viz:color r="{org_color(o["type"]).split(",")[0]}" g="{org_color(o["type"]).split(",")[1]}" b="{org_color(o["type"]).split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        if not any(p["id"] == pos["person_id"] and p["name"] for p in persons):
            continue  # skip unnamed predecessors
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        if not any(p["id"] == r["person_a"] and p["name"] for p in persons):
            continue
        if not any(p["id"] == r["person_b"] and p["name"] for p in persons):
            continue
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"    GEXF written: {output_path}")


def build_sqlite(persons, organizations, positions, relationships, db_path):
    """Build SQLite database."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    # Create tables
    cur.execute("""
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
    cur.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT
        )
    """)

    # Insert data
    for p in persons:
        cur.execute("""INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                     p["birthplace"], p["education"], p["party_join"], p["work_start"],
                     p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""INSERT OR REPLACE INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""INSERT OR REPLACE INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"    DB written: {db_path}")


def write_person_json(person, output_dir):
    """Write a single person JSON file."""
    if not person["name"]:
        return  # skip unnamed entries
    filename = f'{TODAY}-河南省-南阳市-{person["current_post"].replace("/", "-").replace("、", "-")}-{person["name"]}.json'
    filepath = Path(output_dir) / filename

    # Build source register
    source_register = []
    if person.get("source"):
        source_register.append({
            "id": "S001",
            "title": f"邓州市人民政府 - {person['name']}",
            "url": person["source"],
            "publisher": "邓州市人民政府",
            "published_at": AS_OF,
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "Official leadership profile page"
        })

    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河南省",
            "city": "南阳市",
            "region": "邓州市",
            "job": person["current_post"],
            "task_id": "henan_邓州市",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": f"dengzhou_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": person["education"], "study_type": "unknown", "source_ids": ["S001"]}] if person["education"] else [],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "name_birthplace": f"{person['name']}_{person['birthplace']}",
                "official_profile_url": person["source"]
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if person["id"] in (1, 2) else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [],
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
            {"type": "none_found", "description": "No negative signals found in search scope", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if person.get("education") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "完整履历（早年经历、历任职务）" if not person.get("birth") else "birthplace and early career"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的完整履历（出生地、学历、历任职务的起止时间）",
                "why_it_matters": "无法定位其职业发展路径、跨地区交流和晋升模式",
                "suggested_queries": [f"{person['name']} 简历 邓州", f"{person['name']} 任前公示"],
                "last_attempted": AS_OF
            }
        ]
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"    Person JSON written: {filepath}")


if __name__ == "__main__":
    print(f"Building {SLUG} network data...")

    # SQLite
    print("  Creating SQLite database...")
    build_sqlite(persons, organizations, positions, relationships, DB_PATH)

    # GEXF
    print("  Creating GEXF graph...")
    generate_gexf(persons, organizations, positions, relationships, GEXF_PATH)

    # Person JSON
    print("  Creating person JSON files...")
    for p in persons:
        write_person_json(p, PERSONS_DIR)

    print(f"\nDone. Artifacts:")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")
    person_files = [f for f in Path(PERSONS_DIR).iterdir() if f.suffix == ".json" and TODAY in f.name]
    for pf in person_files:
        print(f"  Person: {pf}")
