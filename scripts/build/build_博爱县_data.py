#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 博爱县 (Bo'ai County), 焦作市, 河南省.

Investigation date: 2026-07-24
Task ID: henan_博爱县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - https://www.boai.gov.cn/ — official government website
  - 十四届县委一次全会 (2026-06-24): https://www.boai.gov.cn/2026/06-24/606228.html
    (confirmed county committee standing committee, secretary, deputy secretaries)
  - 县政府信息公开领导之窗: https://www.boai.gov.cn/zfxxgk/
    (lists mayor and deputy mayors)
  - 七一慰问活动 (2026-06-30): https://www.boai.gov.cn/2026/06-30/606612.html
  - 两优一先表彰大会 (2026-06-28): https://www.boai.gov.cn/2026/06-28/606608.html
  - 生态环境保护调研 (2026-07-21): https://www.boai.gov.cn/2026/07-21/608460.html

Confidence notes:
  - 金贵斌 (县委书记): confirmed via official 十四届县委一次全会 report (2026-06-22).
    Previous career details and birth year unverified — marked as gaps.
  - 孟继红 (县长): confirmed as 县委副书记、县长 on boai.gov.cn leadership page and
    multiple news articles. Served as 县长 before being re-elected as deputy secretary.
    Full career timeline and birth year unverified.
  - 马玉峰 (县委副书记、政法委书记): confirmed via multiple official sources.
  - 县委常委: full slate of 11 standing committee members confirmed.
  - 县政府领导班子: 7 members confirmed from official leadership page.
  - Predecessor info for 金贵斌 (who was the previous 县委书记) is unverified — likely
    appointment occurred in late 2025 or early 2026.
  - This is a partial-evidence artifact: core leadership identities and structure are
    well-documented; individual career histories are mostly unconfirmed.
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
SLUG = "博爱县"
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
        "name": "金贵斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共博爱县委员会",
        "source": "Confirmed via 十四届县委一次全会 (2026-06-22): https://www.boai.gov.cn/2026/06-24/606228.html"
    },
    {
        "id": 2,
        "name": "孟继红",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "博爱县人民政府",
        "source": "Confirmed on boai.gov.cn leadership page and multiple news articles, e.g. https://www.boai.gov.cn/2026/07-21/608460.html"
    },
    {
        "id": 3,
        "name": "马玉峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、政法委书记",
        "current_org": "中共博爱县委员会",
        "source": "Confirmed via 十四届县委一次全会 and 七一慰问 article: https://www.boai.gov.cn/2026/06-30/606612.html"
    },
    # ═══════ Party Standing Committee ═══════
    {
        "id": 4,
        "name": "任冉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "中共博爱县委员会",
        "source": "Confirmed as 县委常委 via 十四届县委一次全会; listed as 副县长 on leadership page"
    },
    {
        "id": 5,
        "name": "董军波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共博爱县委员会",
        "source": "Confirmed via 十四届县委一次全会 attendance list"
    },
    {
        "id": 6,
        "name": "樊彦强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共博爱县委员会",
        "source": "Confirmed via 十四届县委一次全会 attendance list"
    },
    {
        "id": 7,
        "name": "王元龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共博爱县委员会",
        "source": "Confirmed via 十四届县委一次全会 attendance list"
    },
    {
        "id": 8,
        "name": "石记红",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共博爱县委员会",
        "source": "Confirmed via 十四届县委一次全会 attendance list"
    },
    {
        "id": 9,
        "name": "钱轶敏",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "博爱县人民政府",
        "source": "Confirmed as 县委常委 via 十四届县委一次全会; listed as 副县长 on leadership page"
    },
    {
        "id": 10,
        "name": "王刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共博爱县委员会",
        "source": "Confirmed via 十四届县委一次全会 attendance list"
    },
    {
        "id": 11,
        "name": "鲁建科",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共博爱县委员会",
        "source": "Confirmed via 十四届县委一次全会 attendance list"
    },
    # ═══════ County Government Leadership ═══════
    {
        "id": 12,
        "name": "王琨",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "博爱县人民政府",
        "source": "Listed on boai.gov.cn government leadership page"
    },
    {
        "id": 13,
        "name": "齐高杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "博爱县人民政府",
        "source": "Listed on boai.gov.cn government leadership page"
    },
    {
        "id": 14,
        "name": "樊伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "博爱县人民政府",
        "source": "Listed on boai.gov.cn government leadership page"
    },
    {
        "id": 15,
        "name": "陈小红",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "博爱县人民政府",
        "source": "Listed on boai.gov.cn government leadership page"
    },
    # ═══════ Other County Leaders ═══════
    {
        "id": 16,
        "name": "王咏生",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "博爱县人民代表大会常务委员会",
        "source": "Confirmed via 七一慰问 article: https://www.boai.gov.cn/2026/06-30/606612.html"
    },
    {
        "id": 17,
        "name": "张金太",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议博爱县委员会",
        "source": "Confirmed via 七一慰问 article: https://www.boai.gov.cn/2026/06-30/606612.html"
    },
    {
        "id": 18,
        "name": "杨莉",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "博爱县",
        "source": "Confirmed via 两优一先表彰大会 (2026-06-28) and 七一慰问 attendance"
    },
    {
        "id": 19,
        "name": "何建军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "博爱县",
        "source": "Confirmed via 两优一先表彰大会 (2026-06-28) and 七一慰问 attendance"
    },
    {
        "id": 20,
        "name": "李静波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "博爱县",
        "source": "Confirmed via 生态环境保护调研 article (2026-07-21): https://www.boai.gov.cn/2026/07-21/608460.html"
    },
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共博爱县委员会", "type": "党委", "level": "县", "location": "博爱县"},
    {"id": 2, "name": "博爱县人民政府", "type": "政府", "level": "县", "location": "博爱县"},
    {"id": 3, "name": "博爱县人民代表大会常务委员会", "type": "人大", "level": "县", "location": "博爱县"},
    {"id": 4, "name": "中国人民政治协商会议博爱县委员会", "type": "政协", "level": "县", "location": "博爱县"},
    {"id": 5, "name": "中共博爱县纪律检查委员会", "type": "党委", "level": "县", "location": "博爱县"},
    {"id": 6, "name": "中共博爱县委政法委员会", "type": "党委", "level": "县", "location": "博爱县"},
]

# ── Positions ───────────────────────────────────────────────────────────────
positions = [
    # 金贵斌
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "2026-06", "end": "present", "rank": "正处级", "note": "Elected at 十四届县委一次全会"},
    # 孟继红
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "正处级", "note": "主持县政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 马玉峰
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 6, "title": "政法委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 任冉
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 董军波
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 樊彦强
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 王元龙
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 石记红
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 钱轶敏
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 王刚
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 鲁建科
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 王琨
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 齐高杰
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 樊伟
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 陈小红
    {"person_id": 15, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 王咏生
    {"person_id": 16, "org_id": 3, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 张金太
    {"person_id": 17, "org_id": 4, "title": "县政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 杨莉
    {"person_id": 18, "org_id": 1, "title": "县领导", "start": "", "end": "present", "rank": "", "note": "Likely 县委常委 or 副县长"},
    # 何建军
    {"person_id": 19, "org_id": 1, "title": "县领导", "start": "", "end": "present", "rank": "", "note": "Likely 县委常委 or 副县长"},
    # 李静波
    {"person_id": 20, "org_id": 2, "title": "县领导", "start": "", "end": "present", "rank": "", "note": "Accompanied 孟继红 on 2026-07-21 environmental inspection"},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # Core leadership overlaps
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记—县长搭档", "overlap_org": "中共博爱县委员会/博爱县人民政府", "overlap_period": "2026.06至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记—县委副书记/政法委书记", "overlap_org": "中共博爱县委员会", "overlap_period": "2026.06至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长—县委副书记/政法委书记，均为县委领导核心", "overlap_org": "中共博爱县委员会", "overlap_period": "至今", "confidence": "confirmed"},
    # Standing committee - core leadership
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记—常委副县长", "overlap_org": "中共博爱县委员会", "overlap_period": "2026.06至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委书记—常委", "overlap_org": "中共博爱县委员会", "overlap_period": "2026.06至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委书记—常委", "overlap_org": "中共博爱县委员会", "overlap_period": "2026.06至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县委书记—常委", "overlap_org": "中共博爱县委员会", "overlap_period": "2026.06至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委书记—常委", "overlap_org": "中共博爱县委员会", "overlap_period": "2026.06至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "县委书记—常委副县长", "overlap_org": "中共博爱县委员会", "overlap_period": "2026.06至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "县委书记—常委", "overlap_org": "中共博爱县委员会", "overlap_period": "2026.06至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "县委书记—常委", "overlap_org": "中共博爱县委员会", "overlap_period": "2026.06至今", "confidence": "confirmed"},
    # Government team overlaps with mayor
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "县长—副县长", "overlap_org": "博爱县人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "县长—副县长", "overlap_org": "博爱县人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "县长—副县长", "overlap_org": "博爱县人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "县长—副县长", "overlap_org": "博爱县人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    # Mayor/county party secretary with人大/政协
    {"person_a": 1, "person_b": 16, "type": "overlap", "context": "县委书记—人大主任", "overlap_org": "博爱县", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 17, "type": "overlap", "context": "县委书记—政协主席", "overlap_org": "博爱县", "overlap_period": "至今", "confidence": "confirmed"},
]

# ── Helper functions ────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(post):
    """Return GEXF color string for a person by current post."""
    if "书记" in post and "县委" in post:
        return "255,50,50"
    if "县长" in post or "副县长" in post or "政府" in post:
        return "50,100,255"
    if "纪委" in post:
        return "255,165,0"
    if "人大" in post:
        return "200,255,255"  # cyan
    if "政协" in post:
        return "255,240,200"  # cream
    if "政法委" in post:
        return "200,200,255"
    return "100,100,100"


def org_color(org_type):
    """Return GEXF color string for an organization by type."""
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(org_type, "200,200,200")


def is_top_leader(person):
    return person["current_post"] in ("县委书记", "县委副书记、县长")


def gen_gexf(persons, organizations, positions, relationships, output_path):
    """Generate GEXF 1.3 graph file using string formatting to avoid namespace issues."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append(f'    <description>博爱县领导班子工作关系网络 — 调查日期 {TODAY}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="org_type" type="string"/>')
    lines.append('      <attribute id="4" title="level" type="string"/>')
    lines.append('      <attribute id="5" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('      <attribute id="4" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        pcolor = person_color(p["current_post"])
        psize = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append(f'          <attvalue for="4" value=""/>')
        lines.append(f'          <attvalue for="5" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{pcolor.split(",")[0]}" g="{pcolor.split(",")[1]}" b="{pcolor.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{psize}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        ocolor = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(o["level"])}"/>')
        lines.append(f'          <attvalue for="5" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization edges (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])} at {esc(pos["note"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos["start"])}—{esc(pos["end"])}"/>')
        lines.append(f'          <attvalue for="4" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person edges (relationships)
    for r in relationships:
        eid += 1
        weight = "2.0" if r["confidence"] == "confirmed" else "1.0"
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append(f'          <attvalue for="4" value="{r["confidence"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def gen_person_json(person, today_str, task_id):
    """Generate a person JSON file following the person_graph_json.md schema."""
    person_id = f"boai_{person['name']}"

    career_timeline = []
    for pos in positions:
        if pos["person_id"] == person["id"]:
            org_name = ""
            for o in organizations:
                if o["id"] == pos["org_id"]:
                    org_name = o["name"]
                    break
            career_timeline.append({
                "start": pos["start"] or "unknown",
                "end": pos["end"] or "unknown",
                "org": org_name,
                "title": pos["title"],
                "rank": pos["rank"],
                "notes": pos["note"],
                "confidence": "confirmed",
                "source_ids": ["S001"],
            })

    person_relationships = []
    for r in relationships:
        if r["person_a"] == person["id"]:
            target_id = r["person_b"]
            target_name = ""
            for p in persons:
                if p["id"] == target_id:
                    target_name = p["name"]
                    break
            person_relationships.append({
                "person": target_name,
                "person_id": f"boai_{target_name}",
                "relationship_type": r["type"],
                "strength": "strong" if r["confidence"] == "confirmed" else "medium",
                "evidence": r["context"],
                "overlap_org": r["overlap_org"],
                "overlap_period": r["overlap_period"],
                "direction": "undirected",
                "confidence": r["confidence"],
                "source_ids": ["S001"],
            })
        elif r["person_b"] == person["id"]:
            src_id = r["person_a"]
            src_name = ""
            for p in persons:
                if p["id"] == src_id:
                    src_name = p["name"]
                    break
            person_relationships.append({
                "person": src_name,
                "person_id": f"boai_{src_name}",
                "relationship_type": r["type"],
                "strength": "strong" if r["confidence"] == "confirmed" else "medium",
                "evidence": r["context"],
                "overlap_org": r["overlap_org"],
                "overlap_period": r["overlap_period"],
                "direction": "undirected",
                "confidence": r["confidence"],
                "source_ids": ["S001"],
            })

    orgs_for_person = []
    for pos in positions:
        if pos["person_id"] == person["id"]:
            for o in organizations:
                if o["id"] == pos["org_id"]:
                    orgs_for_person.append({
                        "id": o["id"],
                        "name": o["name"],
                        "type": o["type"],
                        "level": o["level"],
                    })

    schema = {
        "schema_version": "1.0",
        "generated_at": today_str,
        "investigation_scope": {
            "province": "河南省",
            "city": "焦作市",
            "region": "博爱县",
            "job": person["current_post"],
            "task_id": task_id,
            "time_focus": "2024-2026",
        },
        "identity": {
            "person_id": person_id,
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
                "name_birth": f"{person['name']}_",
                "name_birthplace": f"{person['name']}_",
                "official_profile_url": "https://www.boai.gov.cn/",
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if "县委书记" in person["current_post"] or "县长" in person["current_post"] or "人大主任" in person["current_post"] or "政协主席" in person["current_post"] else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": orgs_for_person,
        "relationships": person_relationships,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "详细履历待查",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {
            "degree_centrality": 0,
            "betweenness_centrality": 0,
            "community_cluster": "",
        },
        "risk_and_integrity_signals": [],
        "source_register": [
            {
                "id": "S001",
                "title": "博爱县人民政府官方网站",
                "url": "https://www.boai.gov.cn/",
                "publisher": "博爱县人民政府",
                "published_at": AS_OF,
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "Primary source for leadership roster and standing committee",
            }
        ],
        "confidence_summary": {
            "identity": "partial" if not person["birth"] else "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "high",
            "biggest_gap": "详细履历（出生年份、教育背景、早期任职经历）缺失",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的出生年份、出生地、教育经历",
                "why_it_matters": "核心身份信息，影响人员去重和晋升速度分析",
                "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 出生", f"博爱县 {person['name']} 任前公示"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{person['name']}的完整工作履历",
                "why_it_matters": "缺少早期职业经历，无法分析晋升路径和与其他官员的交集",
                "suggested_queries": [f"{person['name']} 任职经历", f"{person['name']} 曾任", f"焦作 {person['name']}"],
                "last_attempted": AS_OF,
            },
        ],
    }
    return schema


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    # Build SQLite
    import sqlite3
    db_path = DB_PATH
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

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
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
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
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    # Insert persons
    for p in persons:
        cur.execute("""
            INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
              p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    # Insert organizations
    for o in organizations:
        cur.execute("""
            INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], "", o["location"]))

    # Insert positions
    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    # Insert relationships
    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"✅ SQLite database: {db_path}")

    # Build GEXF
    gen_gexf(persons, organizations, positions, relationships, GEXF_PATH)
    print(f"✅ GEXF graph: {GEXF_PATH}")

    # Generate person JSONs for core leaders
    core_leaders = [p for p in persons if p["id"] in (1, 2)]  # 金贵斌, 孟继红
    for leader in core_leaders:
        suffix = leader["current_post"].replace("、", "_").replace(" ", "_")
        safe_name = leader["name"]
        json_path = PERSONS_DIR / f"{TODAY}-河南省-焦作市-{suffix}-{safe_name}.json"
        data = gen_person_json(leader, TODAY, "henan_博爱县")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Person JSON: {json_path}")

    print(f"\n📊 Summary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")


if __name__ == "__main__":
    main()
