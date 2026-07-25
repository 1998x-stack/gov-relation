#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 刚察县 (Gangcha County), 海北藏族自治州, 青海省.

Investigation date: 2026-07-25
Task ID: qinghai_刚察县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - 刚察县人民政府门户网站 (www.gangcha.gov.cn) — official news and work activity reports
  - 刚察县庆祝建党105周年暨"两优一先"表彰大会 (ID 329999) — confirmed 县委书记张启峰
  - 工作动态 reports (IDs 330044, 330111, 330149, 330085, 330071) — confirmed leadership roster
  - 刚察县第十八届人民代表大会第一次会议 (ID 330125) — confirmed presidium leadership
  
Status: GOOD — Core 2 leaders confirmed with names from official government sources.
         Deputies and institutional leaders confirmed from multiple official activity reports.
         Career timelines and biographical details remain UNVERIFIED — no resumés were found.

Confidence notes:
  - Current officeholder names for all 18 persons are confirmed from official government activity reports.
  - Biographical fields (birth, education, birthplace, party_join, work_start) are UNVERIFIED.
  - Career timelines are completely missing — no resume data was found in available sources.
  - The 县委书记 and 县长 names are marked with high confidence from multiple official sources.
  - Some deputy roles may overlap or have transitioned during the July 2026 election period.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Module path setup ─────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parents[0]
for parent_count in range(0, 6):
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ──────────────────────────────────────────────────────────
SLUG = "刚察县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ─────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "qinghai_刚察县"
if _CURRENT_DIR.name == "qinghai_刚察县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ────────────────────────────────────────────────────────────
# All names confirmed from official government website activity reports.
# Biographical fields are unfilled — official resume data not found.

persons = [
    # ════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ════════════════════════════════════════════════════════════════════
    # --- 县委书记 (Party Secretary) ---
    {
        "id": 1,
        "name": "张启峰",
        "gender": "",           # unverified
        "ethnicity": "",        # unverified
        "birth": "",            # unverified
        "birthplace": "",       # unverified
        "education": "",        # unverified
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "刚察县委书记",
        "current_org": "中共刚察县委员会",
        "source": "Confirmed from 刚察县庆祝建党105周年大会 (ID 329999) and 刚察县第十八届人大第一次会议 (ID 330125)",
    },
    # --- 县长 (County Chief) ---
    {
        "id": 2,
        "name": "刘力",
        "gender": "男",         # inferred from 他 in reports
        "ethnicity": "",        # unverified
        "birth": "",            # unverified
        "birthplace": "",       # unverified
        "education": "",        # unverified
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "刚察县委副书记、县长",
        "current_org": "刚察县人民政府",
        "source": ("Confirmed from multiple official work activity reports (IDs 330149, 330111, 330071, 330085). "
                    "Held position of 县委副书记、县人民政府党组书记、代理县长 in July 2026. "
                    "Elected as 县长 at the 刚察县第十八届人民代表大会第一次会议 (July 2026)."),
    },
    # ════════════════════════════════════════════════════════════════════
    # County Standing Committee (县委常委)
    # ════════════════════════════════════════════════════════════════════
    # --- 县委副书记、政法委书记 (Deputy Party Secretary, Political-Legal Affairs) ---
    {
        "id": 3,
        "name": "尕藏",
        "gender": "",           # unverified
        "ethnicity": "",        # unverified (likely 藏族 given name)
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "刚察县委副书记、政法委书记",
        "current_org": "中共刚察县委员会",
        "source": "Confirmed from 刚察县庆祝建党105周年大会 (ID 329999)",
    },
    # --- 县委副书记、副县长 (援青) (Deputy Party Secretary, Deputy County Chief, Aid-Qinghai) ---
    {
        "id": 4,
        "name": "曹立海",
        "gender": "",           # unverified
        "ethnicity": "",        # unverified
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "刚察县委副书记、县人民政府副县长（援青）",
        "current_org": "刚察县人民政府",
        "source": "Confirmed from official work activity reports (IDs 330149, 330111)",
    },
    # --- 县委副书记、副县长 (援青) (Deputy Party Secretary, Deputy County Chief, Aid-Qinghai) ---
    {
        "id": 5,
        "name": "孟永超",
        "gender": "",           # unverified
        "ethnicity": "",        # unverified
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "刚察县委副书记、县人民政府副县长（援青）",
        "current_org": "刚察县人民政府",
        "source": "Confirmed from official work activity reports (IDs 330149, 330044, 330111)",
    },
    # --- 县委常委、县人民政府党组副书记 (Standing Committee, Deputy Party Secretary of Government) ---
    {
        "id": 6,
        "name": "祁海涛",
        "gender": "",           # unverified
        "ethnicity": "",        # unverified
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "刚察县委常委、县人民政府党组副书记",
        "current_org": "刚察县人民政府",
        "source": "Confirmed from official work activity reports (IDs 330149, 330111)",
    },
    # --- 县委常委、副县长 (Standing Committee, Deputy County Chief) ---
    {
        "id": 7,
        "name": "郑文家",
        "gender": "",           # unverified
        "ethnicity": "",        # unverified
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "刚察县委常委、县人民政府副县长",
        "current_org": "刚察县人民政府",
        "source": "Confirmed from official work activity reports (ID 330044)",
    },
    # --- 县委常委、组织部部长 (Standing Committee, Organization Department Head) ---
    {
        "id": 8,
        "name": "李慧青",
        "gender": "",           # unverified
        "ethnicity": "",        # unverified
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "刚察县委常委、组织部部长",
        "current_org": "中共刚察县委组织部",
        "source": "Confirmed from 刚察县庆祝建党105周年大会 (ID 329999)",
    },
    # ════════════════════════════════════════════════════════════════════
    # County Government Deputies (副县长)
    # ════════════════════════════════════════════════════════════════════
    {
        "id": 9,
        "name": "马生莲",
        "gender": "",           # unverified
        "ethnicity": "",        # unverified
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "刚察县副县长",
        "current_org": "刚察县人民政府",
        "source": "Confirmed from official work activity reports (ID 330044)",
    },
    {
        "id": 10,
        "name": "聂才郎",
        "gender": "",           # unverified
        "ethnicity": "",        # unverified (likely 藏族)
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "刚察县副县长",
        "current_org": "刚察县人民政府",
        "source": "Confirmed from official work activity reports (IDs 330149, 330111, 330044)",
    },
    {
        "id": 11,
        "name": "韩锋",
        "gender": "",           # unverified
        "ethnicity": "",        # unverified
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "刚察县副县长",
        "current_org": "刚察县人民政府",
        "source": "Confirmed from official work activity reports (IDs 330149, 330111)",
    },
    {
        "id": 12,
        "name": "才旺",
        "gender": "",           # unverified
        "ethnicity": "",        # unverified (likely 藏族)
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "刚察县副县长",
        "current_org": "刚察县人民政府",
        "source": "Confirmed from official work activity reports (ID 330044)",
    },
    # ════════════════════════════════════════════════════════════════════
    # 县级领导 (County-level leaders — 人大、政协、两院)
    # ════════════════════════════════════════════════════════════════════
    {
        "id": 13,
        "name": "周有全",
        "gender": "",           # unverified
        "ethnicity": "",        # unverified
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "刚察县人大常委会主任",
        "current_org": "刚察县人民代表大会常务委员会",
        "source": ("Confirmed from 刚察县第十七届人大常委会第三十九次会议 (ID 330070) "
                    "and 刚察县第十八届人大第一次会议 (ID 330125)"),
    },
    {
        "id": 14,
        "name": "熊静",
        "gender": "",           # unverified
        "ethnicity": "",        # unverified
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "刚察县人民法院党组书记",
        "current_org": "刚察县人民法院",
        "source": "Confirmed from 刚察县第十八届人大第一次会议 (ID 330125)",
    },
    {
        "id": 15,
        "name": "苏小锋",
        "gender": "",           # unverified
        "ethnicity": "",        # unverified
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "刚察县人民检察院检察长",
        "current_org": "刚察县人民检察院",
        "source": "Confirmed from 刚察县第十八届人大第一次会议 (ID 330125)",
    },
    # --- 县人民政府党组成员 ---
    {
        "id": 16,
        "name": "郑卓卡",
        "gender": "",           # unverified
        "ethnicity": "",        # unverified (likely 藏族)
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "刚察县人民政府党组成员",
        "current_org": "刚察县人民政府",
        "source": "Confirmed from official work activity reports (IDs 330149, 330111)",
    },
    # --- 海北州委书记 (parent city, for graph completeness) ---
    {
        "id": 17,
        "name": "张峰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "海北州委书记",
        "current_org": "中共海北藏族自治州委员会",
        "source": "Confirmed from build_海北藏族自治州_data.py and official news articles",
    },
    # --- 海北州长 (parent city) ---
    {
        "id": 18,
        "name": "张胜源",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1972年4月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "1993年11月",
        "work_start": "1992年7月",
        "current_post": "海北州州长",
        "current_org": "海北藏族自治州人民政府",
        "source": "Confirmed from build_海北藏族自治州_data.py and 海北州领导之窗",
    },
]

# ── Organizations ──────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共刚察县委员会", "type": "党委",
     "level": "县处级", "parent": "中共海北藏族自治州委员会",
     "location": "青海省海北藏族自治州刚察县"},
    {"id": 2, "name": "刚察县人民政府", "type": "政府",
     "level": "县处级", "parent": "海北藏族自治州人民政府",
     "location": "青海省海北藏族自治州刚察县"},
    {"id": 3, "name": "中共刚察县委组织部", "type": "党委",
     "level": "县处级", "parent": "中共刚察县委员会",
     "location": "青海省海北藏族自治州刚察县"},
    {"id": 4, "name": "中共刚察县委政法委员会", "type": "党委",
     "level": "县处级", "parent": "中共刚察县委员会",
     "location": "青海省海北藏族自治州刚察县"},
    {"id": 5, "name": "刚察县人民代表大会常务委员会", "type": "人大",
     "level": "县处级", "parent": "海北藏族自治州人民代表大会常务委员会",
     "location": "青海省海北藏族自治州刚察县"},
    {"id": 6, "name": "政协刚察县委员会", "type": "政协",
     "level": "县处级", "parent": "政协海北藏族自治州委员会",
     "location": "青海省海北藏族自治州刚察县"},
    {"id": 7, "name": "刚察县人民法院", "type": "政府",
     "level": "县处级", "parent": "刚察县人民政府",
     "location": "青海省海北藏族自治州刚察县"},
    {"id": 8, "name": "刚察县人民检察院", "type": "政府",
     "level": "县处级", "parent": "刚察县人民政府",
     "location": "青海省海北藏族自治州刚察县"},
    {"id": 9, "name": "中共海北藏族自治州委员会", "type": "党委",
     "level": "地厅级", "parent": "中共青海省委员会",
     "location": "青海省海北藏族自治州海晏县西海镇"},
    {"id": 10, "name": "海北藏族自治州人民政府", "type": "政府",
     "level": "地厅级", "parent": "青海省人民政府",
     "location": "青海省海北藏族自治州海晏县西海镇"},
]

# ── Positions ──────────────────────────────────────────────────────────
positions = [
    # Core leadership
    {"person_id": 1, "org_id": 1, "title": "刚察县委书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "刚察县委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "Previously 代理县长, elected 县长 at 刚察县第十八届人大第一次会议 (July 2026)"},
    # Standing Committee
    {"person_id": 3, "org_id": 1, "title": "县委副书记、政法委书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 4, "title": "政法委书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "县委副书记（援青）",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "Aid-Qinghai cadre"},
    {"person_id": 4, "org_id": 2, "title": "副县长（援青）",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "Aid-Qinghai cadre"},
    {"person_id": 5, "org_id": 1, "title": "县委副书记（援青）",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "Aid-Qinghai cadre"},
    {"person_id": 5, "org_id": 2, "title": "副县长（援青）",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "Aid-Qinghai cadre"},
    {"person_id": 6, "org_id": 1, "title": "县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "县人民政府党组副书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "县委常委、组织部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 3, "title": "组织部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # Government deputies
    {"person_id": 9, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "县人民政府党组成员",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # NPC, Court, Procuratorate
    {"person_id": 13, "org_id": 5, "title": "县人大常委会主任",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 14, "org_id": 7, "title": "县人民法院党组书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 15, "org_id": 8, "title": "县人民检察院检察长",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # Parent city leadership
    {"person_id": 17, "org_id": 9, "title": "海北州委书记",
     "start_date": "", "end_date": "present", "rank": "地厅级正职", "note": ""},
    {"person_id": 18, "org_id": 9, "title": "海北州委副书记",
     "start_date": "", "end_date": "present", "rank": "地厅级正职", "note": ""},
    {"person_id": 18, "org_id": 10, "title": "州长",
     "start_date": "", "end_date": "present", "rank": "地厅级正职", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────
relationships = [
    # Top leadership core
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长，党政主要领导工作搭档",
     "overlap_org": "中共刚察县委员会/刚察县人民政府",
     "overlap_period": "current"},
    # Party Secretary — Standing Committee
    {"person_a": 3, "person_b": 1, "type": "overlap",
     "context": "县委副书记、政法委书记协助县委书记工作",
     "overlap_org": "中共刚察县委员会", "overlap_period": "current"},
    {"person_a": 4, "person_b": 1, "type": "overlap",
     "context": "县委副书记（援青）在县委班子中工作",
     "overlap_org": "中共刚察县委员会", "overlap_period": "current"},
    {"person_a": 5, "person_b": 1, "type": "overlap",
     "context": "县委副书记（援青）在县委班子中工作",
     "overlap_org": "中共刚察县委员会", "overlap_period": "current"},
    {"person_a": 6, "person_b": 1, "type": "overlap",
     "context": "县委常委、县政府党组副书记与县委书记工作关系",
     "overlap_org": "中共刚察县委员会", "overlap_period": "current"},
    {"person_a": 7, "person_b": 1, "type": "overlap",
     "context": "县委常委、副县长与县委书记工作关系",
     "overlap_org": "中共刚察县委员会", "overlap_period": "current"},
    {"person_a": 8, "person_b": 1, "type": "overlap",
     "context": "组织部部长与县委书记工作关系",
     "overlap_org": "中共刚察县委员会", "overlap_period": "current"},
    # County Chief — Deputy relationships
    {"person_a": 6, "person_b": 2, "type": "superior_subordinate",
     "context": "县政府党组副书记协助县长工作",
     "overlap_org": "刚察县人民政府", "overlap_period": "current"},
    {"person_a": 7, "person_b": 2, "type": "superior_subordinate",
     "context": "副县长协助县长工作",
     "overlap_org": "刚察县人民政府", "overlap_period": "current"},
    {"person_a": 9, "person_b": 2, "type": "superior_subordinate",
     "context": "副县长协助县长工作",
     "overlap_org": "刚察县人民政府", "overlap_period": "current"},
    {"person_a": 10, "person_b": 2, "type": "superior_subordinate",
     "context": "副县长协助县长工作",
     "overlap_org": "刚察县人民政府", "overlap_period": "current"},
    {"person_a": 11, "person_b": 2, "type": "superior_subordinate",
     "context": "副县长协助县长工作",
     "overlap_org": "刚察县人民政府", "overlap_period": "current"},
    {"person_a": 12, "person_b": 2, "type": "superior_subordinate",
     "context": "副县长协助县长工作",
     "overlap_org": "刚察县人民政府", "overlap_period": "current"},
    {"person_a": 16, "person_b": 2, "type": "superior_subordinate",
     "context": "县政府党组成员协助县长工作",
     "overlap_org": "刚察县人民政府", "overlap_period": "current"},
    # Standing Committee peer relationships
    {"person_a": 6, "person_b": 7, "type": "overlap",
     "context": "县委常委班子工作关系",
     "overlap_org": "中共刚察县委员会", "overlap_period": "current"},
    {"person_a": 4, "person_b": 5, "type": "overlap",
     "context": "援青副书记共同工作",
     "overlap_org": "中共刚察县委员会", "overlap_period": "current"},
    # County Government peer relationships
    {"person_a": 9, "person_b": 10, "type": "overlap",
     "context": "县政府领导班子成员",
     "overlap_org": "刚察县人民政府", "overlap_period": "current"},
    {"person_a": 10, "person_b": 11, "type": "overlap",
     "context": "县政府领导班子成员",
     "overlap_org": "刚察县人民政府", "overlap_period": "current"},
    {"person_a": 11, "person_b": 12, "type": "overlap",
     "context": "县政府领导班子成员",
     "overlap_org": "刚察县人民政府", "overlap_period": "current"},
    # NPC and Institutional leadership
    {"person_a": 13, "person_b": 1, "type": "overlap",
     "context": "人大主任与县委书记工作关系",
     "overlap_org": "中共刚察县委员会", "overlap_period": "current"},
    # Parent city reporting relationship
    {"person_a": 1, "person_b": 17, "type": "superior_subordinate",
     "context": "刚察县委书记受海北州委领导",
     "overlap_org": "中共海北藏族自治州委员会", "overlap_period": "current"},
    {"person_a": 2, "person_b": 18, "type": "superior_subordinate",
     "context": "刚察县长受海北州政府领导",
     "overlap_org": "海北藏族自治州人民政府", "overlap_period": "current"},
]

# ── Person JSON data ────────────────────────────────────────────────────
PERSON_JSON_TEMPLATE = {
    "schema_version": "1.0",
    "generated_at": TODAY,
    "investigation_scope": {
        "province": "青海省",
        "city": "海北藏族自治州",
        "region": "刚察县",
        "job": "",
        "task_id": "qinghai_刚察县",
        "time_focus": "current"
    },
    "identity": {
        "person_id": "",
        "name": "",
        "aliases": [],
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": [],
        "party_join": "中共党员",
        "work_start": "",
        "dedupe_keys": {
            "name_birth": "",
            "name_birthplace": "",
            "official_profile_url": ""
        }
    },
    "current_status": {
        "current_post": "",
        "current_org": "",
        "administrative_rank": "",
        "as_of": AS_OF,
        "is_current_confirmed": True,
        "source_ids": []
    },
    "career_timeline": [
        {
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料中未找到该人物的详细履历信息。需从刚察县人民政府官网领导之窗页面或海北州委组织部任前公示补充。",
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
            "summary": "未知 — 未获取到履历信息",
            "notable_fast_promotions": []
        }
    },
    "work_style_and_personality": {
        "public_style_indicators": [
            {
                "trait": "unknown",
                "evidence": "当前岗位职能活动已有公开报道，但个人工作风格信息暂未收集",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "speech_themes": [],
        "management_signals": [],
        "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
    },
    "network_metrics": {
        "direct_reports": [],
        "peer_relations": [],
        "organizational_affiliations": [],
        "centrality_estimate": "unknown"
    },
    "risk_and_integrity_signals": [
        {
            "type": "none_found",
            "description": "截至2026年7月，未检索到该人物的任何纪律审查、审计问题或负面媒体报道信息。",
            "date": AS_OF,
            "confidence": "unverified",
            "source_ids": []
        }
    ],
    "source_register": [
        {
            "id": "S001",
            "title": "刚察县人民政府门户网站",
            "url": "https://www.gangcha.gov.cn/",
            "publisher": "刚察县人民政府",
            "published_at": AS_OF,
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "官方活动报道证实了主要领导名单"
        },
        {
            "id": "S002",
            "title": "刚察县庆祝建党105周年暨两优一先表彰大会",
            "url": "https://www.gangcha.gov.cn/html/2175/329999.html",
            "publisher": "刚察县人民政府",
            "published_at": "2026-07-01",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "证实县委书记张启峰任职"
        },
        {
            "id": "S003",
            "title": "刚察县第十八届人民代表大会第一次会议",
            "url": "https://www.gangcha.gov.cn/html/2175/330125.html",
            "publisher": "刚察县人民政府",
            "published_at": "2026-07-22",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "证实人大主席团、法院、检察院领导"
        },
        {
            "id": "S004",
            "title": "刚察县工作动态汇总",
            "url": "https://www.gangcha.gov.cn/html/2175/330149.html",
            "publisher": "刚察县人民政府",
            "published_at": "2026-07-24",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "证实县政府领导班子日常活动"
        },
        {
            "id": "S005",
            "title": "刚察县第十七届人大常委会第三十九次会议",
            "url": "https://www.gangcha.gov.cn/html/2175/330070.html",
            "publisher": "刚察县人民政府",
            "published_at": "2026-07-10",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "证实县人大常委会主任周有全"
        }
    ],
    "confidence_summary": {
        "identity": "plausible",
        "current_role": "confirmed",
        "career_completeness": "thin",
        "relationship_confidence": "medium",
        "biggest_gap": "所有核心人物的详细履历（出生、教育、工作经历）均未找到。需要从刚察县领导之窗页面、百度百科或海北州委组织部任前公示补充。"
    },
    "open_questions": [
        {
            "priority": "high",
            "question": "县委书记张启峰的完整履历（出生年份、教育背景、工作经历）？",
            "why_it_matters": "核心调查目标之一——县级一把手，了解其职业背景可揭示干部培养路径",
            "suggested_queries": ["张启峰 简历 刚察", "张启峰 海北", "张启峰 青海"],
            "last_attempted": AS_OF
        },
        {
            "priority": "high",
            "question": "县长刘力的完整履历（出生年份、教育背景、此前职务）？",
            "why_it_matters": "核心调查目标之二——县政府一把手，了解其晋升路径",
            "suggested_queries": ["刘力 刚察 县长 简历", "刘力 刚察 代理县长"],
            "last_attempted": AS_OF
        },
        {
            "priority": "medium",
            "question": "县委副书记尕藏的完整姓名和履历？",
            "why_it_matters": "第三号人物，负责政法工作",
            "suggested_queries": ["尕藏 刚察 副书记 简历", "刚察 政法委书记 尕藏"],
            "last_attempted": AS_OF
        },
        {
            "priority": "medium",
            "question": "刚察县前县委书记的去向和现任？",
            "why_it_matters": "了解干部晋升通道和交流网络",
            "suggested_queries": ["刚察县 前任县委书记", "刚察县委原书记"],
            "last_attempted": AS_OF
        },
        {
            "priority": "low",
            "question": "县政协主席的姓名？",
            "why_it_matters": "完善县级领导班子的完整图谱",
            "suggested_queries": ["刚察县政协主席"],
            "last_attempted": AS_OF
        }
    ]
}


def write_person_json(person_id: int, name: str, post: str, org: str, rank: str,
                      filename_suffix: str) -> None:
    """Write a person JSON file to the staging directory."""
    data = PERSON_JSON_TEMPLATE.copy()
    data["investigation_scope"]["job"] = post
    data["identity"]["person_id"] = f"gangcha_{name}"
    data["identity"]["name"] = name
    data["current_status"]["current_post"] = post
    data["current_status"]["current_org"] = org
    data["current_status"]["administrative_rank"] = rank
    # Relationships (only for the two core leaders)
    if person_id == 1:
        data["relationships"].append({
            "person": "刘力",
            "person_id": "gangcha_刘力",
            "relationship_type": "superior_subordinate",
            "strength": "strong",
            "evidence": "县委书记与县长为党政主要领导工作搭档关系，共同参加党代会等人大会务活动",
            "overlap_org": "中共刚察县委员会",
            "overlap_period": "current",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001", "S004"]
        })
    if person_id == 2:
        data["relationships"].append({
            "person": "张启峰",
            "person_id": "gangcha_张启峰",
            "relationship_type": "superior_subordinate",
            "strength": "strong",
            "evidence": "县长与县委书记为党政主要领导工作搭档关系",
            "overlap_org": "中共刚察县委员会",
            "overlap_period": "current",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001", "S004"]
        })
    filename = f"{TODAY}-青海省-海北藏族自治州-{filename_suffix}.json"
    path = PJSON_DIR / filename
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {path}")


# ── Build ──────────────────────────────────────────────────────────────
def main() -> None:
    print(f"Building {SLUG} leadership network...")
    print(f"  Staging: {STAGING}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

    # Build database and GEXF
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    # Write person JSONs for core leaders
    print("  Writing person JSONs...")
    write_person_json(1, "张启峰", "刚察县委书记",
                      "中共刚察县委员会", "县处级正职", "县委书记-张启峰")
    write_person_json(2, "刘力", "刚察县委副书记、县长",
                      "刚察县人民政府", "县处级正职", "县长-刘力")

    print(f"\nDone. Staged artifacts in: {STAGING}")
    print(f"  1. Build script: {__file__}")
    print(f"  2. Database: {DB_PATH}")
    print(f"  3. GEXF: {GEXF_PATH}")
    print(f"  4. Person JSONs: {PJSON_DIR}")


if __name__ == "__main__":
    main()
