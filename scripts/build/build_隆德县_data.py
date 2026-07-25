#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 隆德县 (Longde County), 固原市, 宁夏回族自治区.

Investigation date: 2026-07-25
Task ID: ningxia_隆德县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - Official county government website (www.nxld.gov.cn) news articles were directly accessible
  - 领导之窗 page is OUTDATED — still shows 袁秉和 as party secretary
  - Current leadership confirmed from 2026 news articles

Key timeline:
  - Until ~March 2024: 朱红社 as 县长, 刘斌 as 县委书记
  - June 2024: 刘永龙 appeared as 县长候选人, confirmed 县长 by August 2024
  - July 2025: 刘斌 still 县委书记 (last confirmed sighting)
  - Feb 2026: 刘永龙 last confirmed as 县长
  - Between Feb-May 2026: 刘永龙 promoted to 县委书记, 刘斌 departed
  - May 2026: 田玉铭 appeared as 县长候选人
  - June 2026: 田玉铭 confirmed as 县长
  - July 2026: Current leaders are 刘永龙 (县委书记) and 田玉铭 (县长)

Person JSON files:
  - data/tmp/ningxia_隆德县/YYYYMMDD-宁夏回族自治区-固原市-县委书记-刘永龙.json
  - data/tmp/ningxia_隆德县/YYYYMMDD-宁夏回族自治区-固原市-县长-田玉铭.json

Confidence notes:
  - Current role for 刘永龙 (县委书记) and 田玉铭 (县长): CONFIRMED from official news
  - 刘永龙's pre-2024 June career: UNVERIFIED — no public sources found
  - 田玉铭's pre-2026 May career: UNVERIFIED — no public sources found
  - 刘斌 (former 县委书记) departure destination: UNVERIFIED
  - 朱红社 (former 县长) departure destination: UNVERIFIED
  - 袁秉和 (earlier 县委书记) full timeline: UNVERIFIED
  - 刘永龙/田玉铭 birth info, education: UNVERIFIED — not listed on government news
  - Full leadership roster (常委, 副县长): UNVERIFIED — not available from news articles
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Module path setup ─────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
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
SLUG = "隆德县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ─────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "ningxia_隆德县"
if _CURRENT_DIR.name == "ningxia_隆德县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Official Source URLs (all verified accessible) ─────────────────────
SOURCES = {
    "S001": {
        "title": "2026年第一次为企业纾困解难集中办公会",
        "url": "https://www.nxld.gov.cn/xwzx/szyw/202605/t20260515_5240858.html",
        "note": "刘永龙以县委书记身份出席，田玉铭以县长候选人身份主持",
    },
    "S002": {
        "title": "县安委会2026年第四次全体（扩大）会议",
        "url": "https://www.nxld.gov.cn/xwzx/szyw/202606/t20260604_5256352.html",
        "note": "田玉铭以县长、县安委会主任身份主持",
    },
    "S003": {
        "title": "县人民政府第五次全体（扩大）会议",
        "url": "https://www.nxld.gov.cn/xwzx/szyw/202602/t20260212_5170746.html",
        "note": "刘永龙最后一次以县长身份主持会议",
    },
    "S004": {
        "title": "全县防汛工作安排部署会",
        "url": "https://www.nxld.gov.cn/xwzx/szyw/202507/t20250729_4974477.html",
        "note": "刘斌以县委书记、刘永龙以县长身份共同出席",
    },
    "S005": {
        "title": "县人民政府专题会议（刘永龙首次以县长候选人出现）",
        "url": "https://www.nxld.gov.cn/xwzx/szyw/202406/t20240626_4576220.html",
        "note": "刘永龙首次出现，作为县委副书记、政府县长候选人",
    },
    "S006": {
        "title": "2025年第一次为企业纾困解难集中办公会",
        "url": "https://www.nxld.gov.cn/xwzx/szyw/202502/t20250221_4831867.html",
        "note": "刘斌、刘永龙共同出席",
    },
    "S007": {
        "title": "隆德县领导之窗（袁秉和，已过时）",
        "url": "https://www.nxld.gov.cn/zwgk/ldzc/",
        "note": "页面仍列出袁秉和主持县委全面工作，未更新反映刘永龙接任",
    },
    "S008": {
        "title": "朱红社以县长身份主持会议",
        "url": "https://www.nxld.gov.cn/xwzx/szyw/202403/t20240328_4498305.html",
        "note": "朱红社最后一次以县长身份出现",
    },
}

# ── Persons ────────────────────────────────────────────────────────────
# Known current and former leadership. Deputies (常委, 副县长) are unverified
# from available sources and marked as gaps.
persons = [
    # ════════════════════════════════════════════════════════════════════
    # Current Core Leadership
    # ════════════════════════════════════════════════════════════════════
    # --- 县委书记 (Party Secretary) — CONFIRMED from S001, S003, S004 ---
    {
        "id": 1,
        "name": "刘永龙",
        "gender": "",          # unverified
        "ethnicity": "",       # unverified
        "birth": "",           # unverified
        "birthplace": "",      # unverified
        "education": "",       # unverified
        "party_join": "",
        "work_start": "",
        "current_post": "隆德县委书记",
        "current_org": "中国共产党隆德县委员会",
        "source": "S001: 2026-05-15以县委书记身份出席纾困解难集中办公会",
    },
    # --- 县长 (County Chief) — CONFIRMED from S001, S002 ---
    {
        "id": 2,
        "name": "田玉铭",
        "gender": "",          # unverified
        "ethnicity": "",       # unverified
        "birth": "",           # unverified
        "birthplace": "",      # unverified
        "education": "",       # unverified
        "party_join": "",
        "work_start": "",
        "current_post": "隆德县委副书记、县长",
        "current_org": "隆德县人民政府",
        "source": "S001: 2026-05-15以县长候选人身份出现; S002: 2026-06-04以县长身份主持",
    },
    # ════════════════════════════════════════════════════════════════════
    # Former Leadership
    # ════════════════════════════════════════════════════════════════════
    # --- 前任县委书记 — CONFIRMED but departure destination unknown ---
    {
        "id": 3,
        "name": "刘斌",
        "gender": "",          # unverified
        "ethnicity": "",       # unverified
        "birth": "",           # unverified
        "birthplace": "",      # unverified
        "education": "",       # unverified
        "party_join": "",
        "work_start": "",
        "current_post": "隆德县委原书记（去向待查）",
        "current_org": "",
        "source": "S004: 2025-07-29以县委书记身份主持防汛会; S006: 2025-02-21共同出席",
    },
    # --- 更早前任县委书记 — listed on 领导之窗 (outdated) ---
    {
        "id": 4,
        "name": "袁秉和",
        "gender": "",          # unverified
        "ethnicity": "",       # unverified
        "birth": "",           # unverified
        "birthplace": "",      # unverified
        "education": "",       # unverified
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "S007: 隆德县领导之窗仍列出其为主持县委全面工作的领导（页面已过时）",
    },
    # --- 前任县长 — CONFIRMED but departure destination unknown ---
    {
        "id": 5,
        "name": "朱红社",
        "gender": "",          # unverified
        "ethnicity": "",       # unverified
        "birth": "",           # unverified
        "birthplace": "",      # unverified
        "education": "",       # unverified
        "party_join": "",
        "work_start": "",
        "current_post": "隆德县委原副书记、县长（去向待查）",
        "current_org": "",
        "source": "S008: 2024-03-28以县长身份主持会议（最后一次出现）",
    },
    # ════════════════════════════════════════════════════════════════════
    # Key Deputy Positions (Standing Committee + Government)
    # ════════════════════════════════════════════════════════════════════
    # These positions exist in a standard county structure but the specific
    # officeholders could NOT be identified from available sources.
    {
        "id": 10,
        "name": "待查_县委副书记（专职）",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "隆德县委副书记（专职）",
        "current_org": "中国共产党隆德县委员会",
        "source": "待查 — 未从公开新闻中找到该职务任职者",
    },
    {
        "id": 11,
        "name": "待查_常务副县长",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "隆德县委常委、常务副县长",
        "current_org": "隆德县人民政府",
        "source": "待查 — 未从公开新闻中找到该职务任职者",
    },
    {
        "id": 12,
        "name": "待查_纪委书记",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "隆德县委常委、县纪委书记、县监委主任",
        "current_org": "中国共产党隆德县纪律检查委员会",
        "source": "待查 — 未从公开新闻中找到该职务任职者",
    },
    {
        "id": 13,
        "name": "待查_组织部部长",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "隆德县委常委、组织部部长",
        "current_org": "隆德县委组织部",
        "source": "待查 — 未从公开新闻中找到该职务任职者",
    },
    {
        "id": 14,
        "name": "待查_宣传部部长",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "隆德县委常委、宣传部部长",
        "current_org": "中国共产党隆德县委员会",
        "source": "待查 — 未从公开新闻中找到该职务任职者",
    },
    {
        "id": 15,
        "name": "待查_政法委书记",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "隆德县委常委、政法委书记",
        "current_org": "中国共产党隆德县委员会",
        "source": "待查 — 未从公开新闻中找到该职务任职者",
    },
    {
        "id": 16,
        "name": "待查_统战部部长",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "隆德县委常委、统战部部长",
        "current_org": "中国共产党隆德县委员会",
        "source": "待查 — 未从公开新闻中找到该职务任职者",
    },
    {
        "id": 17,
        "name": "待查_副县长1",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "隆德县副县长",
        "current_org": "隆德县人民政府",
        "source": "待查 — 未从公开新闻中找到该职务任职者",
    },
    {
        "id": 18,
        "name": "待查_副县长2",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "隆德县副县长",
        "current_org": "隆德县人民政府",
        "source": "待查 — 未从公开新闻中找到该职务任职者",
    },
    # 人大主任, 政协主席
    {
        "id": 20,
        "name": "待查_人大主任",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "隆德县人大常委会主任",
        "current_org": "隆德县人民代表大会常务委员会",
        "source": "待查 — 未从公开新闻中找到该职务任职者",
    },
    {
        "id": 21,
        "name": "待查_政协主席",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "政协隆德县委员会主席",
        "current_org": "政协隆德县委员会",
        "source": "待查 — 未从公开新闻中找到该职务任职者",
    },
]

# ── Organizations ──────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中国共产党隆德县委员会", "type": "党委",
     "level": "县处级", "parent": "中国共产党固原市委员会",
     "location": "宁夏回族自治区固原市隆德县"},
    {"id": 2, "name": "隆德县人民政府", "type": "政府",
     "level": "县处级", "parent": "固原市人民政府",
     "location": "宁夏回族自治区固原市隆德县"},
    {"id": 3, "name": "中国共产党隆德县纪律检查委员会", "type": "党委",
     "level": "县处级", "parent": "中国共产党隆德县委员会",
     "location": "宁夏回族自治区固原市隆德县"},
    {"id": 4, "name": "隆德县委组织部", "type": "党委",
     "level": "县处级", "parent": "中国共产党隆德县委员会",
     "location": "宁夏回族自治区固原市隆德县"},
    {"id": 5, "name": "隆德县人民代表大会常务委员会", "type": "人大",
     "level": "县处级", "parent": "固原市人民代表大会常务委员会",
     "location": "宁夏回族自治区固原市隆德县"},
    {"id": 6, "name": "政协隆德县委员会", "type": "政协",
     "level": "县处级", "parent": "政协固原市委员会",
     "location": "宁夏回族自治区固原市隆德县"},
    {"id": 7, "name": "隆德县应急管理局", "type": "政府",
     "level": "乡科级", "parent": "隆德县人民政府",
     "location": "宁夏回族自治区固原市隆德县"},
    {"id": 8, "name": "隆德县安全生产委员会", "type": "政府",
     "level": "县级", "parent": "隆德县人民政府",
     "location": "宁夏回族自治区固原市隆德县"},
]

# ── Positions ──────────────────────────────────────────────────────────
positions = [
    # 刘永龙 — 县委书记 (current)
    {"person_id": 1, "org_id": 1, "title": "隆德县委书记",
     "start_date": "2026-05（推定）", "end_date": "present",
     "rank": "正处级",
     "note": "2026年2月最后一次以县长身份出现；2026年5月13日首次以县委书记身份出席活动"},
    # 刘永龙 — 县长 (former)
    {"person_id": 1, "org_id": 2, "title": "隆德县委副书记、县长",
     "start_date": "2024-08（推定）", "end_date": "2026-05（推定）",
     "rank": "正处级",
     "note": "2024年6月24日首次以县长候选人身份出现；2024年8月确认为县长；2026年2月12日最后一次以县长身份主持"},
    # 田玉铭 — 县长 (current)
    {"person_id": 2, "org_id": 2, "title": "隆德县委副书记、县长",
     "start_date": "2026-06（推定）", "end_date": "present",
     "rank": "正处级",
     "note": "2026年5月13日以县长候选人身份首次出现；2026年6月4日以县长、县安委会主任身份主持"},
    {"person_id": 2, "org_id": 8, "title": "隆德县安委会主任",
     "start_date": "2026-06（推定）", "end_date": "present",
     "rank": "", "note": "县长兼任"},
    # 刘斌 — 前任县委书记
    {"person_id": 3, "org_id": 1, "title": "隆德县委书记（前任）",
     "start_date": "不详", "end_date": "2025后-2026初（推定）",
     "rank": "正处级",
     "note": "2025年7月29日最后一次以县委书记身份出现；接任者刘永龙于2026年5月以县委书记身份出现"},
    # 袁秉和 — 更早前任县委书记
    {"person_id": 4, "org_id": 1, "title": "隆德县委书记（前任）",
     "start_date": "不详", "end_date": "不详",
     "rank": "正处级",
     "note": "政府网站领导之窗仍列其为主持县委全面工作的领导（页面过时未更新）"},
    # 朱红社 — 前任县长
    {"person_id": 5, "org_id": 2, "title": "隆德县委副书记、县长（前任）",
     "start_date": "不详", "end_date": "2024-03后",
     "rank": "正处级",
     "note": "2024年3月28日最后一次以县长身份出席会议"},
    # Deputy positions (placeholder)
    {"person_id": 10, "org_id": 1, "title": "县委副书记（专职）",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "县委常委",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "常务副县长",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "县委常委、县纪委书记",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 3, "title": "县纪委书记、县监委主任",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "县委常委、组织部部长",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 1, "title": "县委常委、宣传部部长",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 1, "title": "县委常委、政法委书记",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 1, "title": "县委常委、统战部部长",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 5, "title": "隆德县人大常委会主任",
     "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 21, "org_id": 6, "title": "政协隆德县委员会主席",
     "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────
relationships = [
    # Current top leadership
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "刘永龙（县委书记）与田玉铭（县长），隆德县党政主要领导搭档",
     "overlap_org": "中国共产党隆德县委员会/隆德县人民政府",
     "overlap_period": "2026年5月起"},
    # Predecessor-successor: 刘斌 -> 刘永龙 (县委书记)
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor",
     "context": "刘斌为前任县委书记，刘永龙接任县委书记",
     "overlap_org": "中国共产党隆德县委员会",
     "overlap_period": "2025-2026"},
    # Predecessor-successor: 袁秉和 -> 刘斌 -> 刘永龙
    {"person_a": 4, "person_b": 3, "type": "predecessor_successor",
     "context": "袁秉和为更早前任县委书记，刘斌接任",
     "overlap_org": "中国共产党隆德县委员会",
     "overlap_period": "不详"},
    # Predecessor-successor: 朱红社 -> 刘永龙 (县长)
    {"person_a": 5, "person_b": 1, "type": "predecessor_successor",
     "context": "朱红社为前任县长，刘永龙（后升任书记）接任县长",
     "overlap_org": "隆德县人民政府",
     "overlap_period": "2024年"},
    # Predecessor-successor: 刘永龙 -> 田玉铭 (县长)
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "刘永龙从县长升任县委书记后，田玉铭接任县长",
     "overlap_org": "隆德县人民政府",
     "overlap_period": "2026年5月"},
    # Historical overlap: 刘斌 + 刘永龙 worked together
    {"person_a": 3, "person_b": 1, "type": "overlap",
     "context": "刘斌（县委书记）与刘永龙（县长）约两年的党政搭档关系",
     "overlap_org": "中国共产党隆德县委员会/隆德县人民政府",
     "overlap_period": "2024年下半年至2025年中"},
]

# ── Person JSON generation ─────────────────────────────────────────────

def make_person_json_liuyonglong() -> dict:
    """Generate person JSON for 刘永龙 (县委书记)."""
    return {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "宁夏回族自治区",
            "city": "固原市",
            "region": "隆德县",
            "job": "县委书记",
            "task_id": "ningxia_隆德县",
            "time_focus": "2024-2026"
        },
        "identity": {
            "person_id": "ningxia_guyuan_longde_liuyonglong",
            "name": "刘永龙",
            "aliases": [],
            "gender": "",
            "ethnicity": "",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "刘永龙_",
                "name_birthplace": "刘永龙_",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": "隆德县委书记",
            "current_org": "中国共产党隆德县委员会",
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S003"]
        },
        "career_timeline": [
            {
                "start": "2026-05（推定）",
                "end": "至今",
                "org": "中国共产党隆德县委员会",
                "title": "隆德县委书记",
                "level": "县级",
                "location": "宁夏回族自治区固原市隆德县",
                "system": "party",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "2026年5月13日首次以县委书记身份出席活动（县纾困解难集中办公会）。此前约2026年2月仍为县长。具体升任日期待查。",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "start": "2024-06（县长候选人）",
                "end": "2026-05（推定）",
                "org": "隆德县人民政府",
                "title": "隆德县委副书记、县长",
                "level": "县级",
                "location": "宁夏回族自治区固原市隆德县",
                "system": "government",
                "rank": "正处级",
                "is_key_promotion": False,
                "notes": "2024年6月24日首次以'县委副书记、政府县长候选人'身份出现。2024年8月已确认为县长。2026年2月12日最后一次以县长身份主持会议。",
                "confidence": "confirmed",
                "source_ids": ["S003", "S005"]
            },
            {
                "start": "未知",
                "end": "2024年6月",
                "org": "履历缺口",
                "title": "",
                "notes": "公开资料未发现刘永龙2024年6月之前的履历信息。可能曾在固原市其他县区或市直部门任职。",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "organizations": [
            {"org_id": "org_ld_county_party", "name": "中国共产党隆德县委员会",
             "type": "党委", "level": "县级", "parent": "中国共产党固原市委员会",
             "location": "宁夏回族自治区固原市隆德县",
             "relation_to_person": "当前任职单位", "confidence": "confirmed",
             "source_ids": ["S001"]},
            {"org_id": "org_ld_county_gov", "name": "隆德县人民政府",
             "type": "政府", "level": "县级", "parent": "固原市人民政府",
             "location": "宁夏回族自治区固原市隆德县",
             "relation_to_person": "前任任职单位（县长）", "confidence": "confirmed",
             "source_ids": ["S003", "S005"]}
        ],
        "relationships": [
            {"person": "刘斌", "person_id": "ningxia_guyuan_longde_liubin",
             "relationship_type": "superior_subordinate", "strength": "strong",
             "evidence": "刘斌作为隆德县委书记，刘永龙作为县长，二人有约一年的党政搭档关系（至少2024年8月至2025年7月）。",
             "overlap_org": "隆德县", "overlap_period": "2024年8月至2025年7月",
             "direction": "other_to_person", "confidence": "confirmed",
             "source_ids": ["S004"]},
            {"person": "朱红社", "person_id": "ningxia_guyuan_longde_zhuhongshe",
             "relationship_type": "predecessor_successor", "strength": "strong",
             "evidence": "朱红社是刘永龙的前任隆德县长，2024年3月最后一次以县长身份出现，2024年6月刘永龙接任县长候选人。",
             "overlap_org": "隆德县人民政府", "overlap_period": "2024年",
             "direction": "person_to_other", "confidence": "confirmed",
             "source_ids": ["S008"]},
            {"person": "田玉铭", "person_id": "ningxia_guyuan_longde_tianyuming",
             "relationship_type": "predecessor_successor", "strength": "strong",
             "evidence": "刘永龙从县长升任县委书记后，田玉铭接任县长候选人并于2026年6月确认为县长；二人有党政搭档关系。",
             "overlap_org": "隆德县", "overlap_period": "2026年5月起",
             "direction": "person_to_other", "confidence": "confirmed",
             "source_ids": ["S001", "S002"]}
        ],
        "governance_record": [
            {"period": "2026年2月", "domain": "economic_development",
             "achievement_or_event": "主持召开县人民政府第五次全体（扩大）会议",
             "role_in_event": "主持会议（时任县长）",
             "measurable_outcome": "", "location": "隆德县",
             "confidence": "confirmed", "source_ids": ["S003"]},
            {"period": "2026年5月", "domain": "economic_development",
             "achievement_or_event": "出席2026年第一次为企业纾困解难集中办公会",
             "role_in_event": "出席会议并讲话（以县委书记身份）",
             "measurable_outcome": "", "location": "隆德县",
             "confidence": "confirmed", "source_ids": ["S001"]}
        ],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": ["party", "government"],
            "geographic_pattern": ["宁夏回族自治区", "固原市", "隆德县"],
            "promotion_velocity": {
                "summary": "2024年6月以县长候选人身份至隆德县，约2个月内正式成为县长。至2026年5月（约2年）升任县委书记。但此前履历不明，无法评估整体晋升速度。",
                "notable_fast_promotions": ["县长→县委书记：约2年（2024年6月县长候选人→2026年5月县委书记）"]
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "unknown", "evidence": "",
                 "confidence": "unverified", "source_ids": []}
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment. No behavioral data available for this figure."
        },
        "network_metrics": {
            "total_relationships": 3,
            "strong_edges": 3,
            "unique_organizations": 2,
            "known_predecessors": ["朱红社（前县长）", "刘斌（前县委书记）"],
            "known_successors": ["田玉铭（现任县长，为其接任者）"]
        },
        "risk_and_integrity_signals": [
            {"type": "none_found",
             "description": "截至2026年7月，未发现刘永龙在公开记录中有纪律处分、审计问题或负面媒体报道。",
             "date": AS_OF, "confidence": "plausible", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "2026年第一次为企业纾困解难集中办公会",
             "url": SOURCES["S001"]["url"], "publisher": "隆德县人民政府",
             "published_at": "2026-05-15", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high",
             "notes": "刘永龙以县委书记身份出席"},
            {"id": "S002", "title": "县安委会2026年第四次全体（扩大）会议",
             "url": SOURCES["S002"]["url"], "publisher": "隆德县人民政府",
             "published_at": "2026-06-04", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high",
             "notes": "田玉铭以县长身份出现，确认刘永龙已不再是县长"},
            {"id": "S003", "title": "县人民政府第五次全体（扩大）会议",
             "url": SOURCES["S003"]["url"], "publisher": "隆德县人民政府",
             "published_at": "2026-02-12", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high",
             "notes": "刘永龙最后一次以县长身份主持"},
            {"id": "S004", "title": "全县防汛工作安排部署会",
             "url": SOURCES["S004"]["url"], "publisher": "隆德县人民政府",
             "published_at": "2025-07-29", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high",
             "notes": "刘斌（县委书记）与刘永龙（县长）共同出席"},
            {"id": "S005", "title": "县人民政府专题会议",
             "url": SOURCES["S005"]["url"], "publisher": "隆德县人民政府",
             "published_at": "2024-06-26", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high",
             "notes": "刘永龙首次出现，作为'县委副书记、政府县长候选人'"},
            {"id": "S008", "title": "朱红社以县长身份主持会议",
             "url": SOURCES["S008"]["url"], "publisher": "隆德县人民政府",
             "published_at": "2024-03-28", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high",
             "notes": "朱红社最后一次以县长身份出现"}
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "high",
            "biggest_gap": "2024年6月前全部履历（出生、教育、入党、此前职务）均为未知"
        },
        "open_questions": [
            {"priority": "critical",
             "question": "刘永龙的出生年份、出生地、民族、教育背景是什么？",
             "why_it_matters": "基础身份信息缺失，影响人员去重和网络分析。",
             "suggested_queries": ["刘永龙 简历", "刘永龙 宁夏 固原 出生", "刘永龙 百度百科"],
             "last_attempted": AS_OF},
            {"priority": "critical",
             "question": "刘永龙2024年6月之前的职业生涯是怎样的？他在哪个部门/地区任职？",
             "why_it_matters": "无法评估其职业轨迹和专业背景。",
             "suggested_queries": ["刘永龙 隆德县 副县长", "刘永龙 固原市 任职", "固原市委组织部 任前公示 刘永龙"],
             "last_attempted": AS_OF},
            {"priority": "high",
             "question": "刘永龙的具体入党时间？",
             "why_it_matters": "评估党内资历。",
             "suggested_queries": ["刘永龙 入党", "刘永龙 政治面貌"],
             "last_attempted": AS_OF},
            {"priority": "medium",
             "question": "刘永龙从县长升任县委书记的具体任命日期？",
             "why_it_matters": "明确关键晋升时间点。",
             "suggested_queries": ["隆德县 干部任免 刘永龙", "固原市委 任命 刘永龙 县委书记"],
             "last_attempted": AS_OF},
            {"priority": "medium",
             "question": "前任县委书记刘斌的去向？",
             "why_it_matters": "了解干部交流模式。",
             "suggested_queries": ["刘斌 隆德县 去向", "刘斌 宁夏 任职"],
             "last_attempted": AS_OF}
        ]
    }


def make_person_json_tianyuming() -> dict:
    """Generate person JSON for 田玉铭 (县长)."""
    return {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "宁夏回族自治区",
            "city": "固原市",
            "region": "隆德县",
            "job": "县长",
            "task_id": "ningxia_隆德县",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": "ningxia_guyuan_longde_tianyuming",
            "name": "田玉铭",
            "aliases": [],
            "gender": "",
            "ethnicity": "",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "田玉铭_",
                "name_birthplace": "田玉铭_",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": "隆德县委副书记、县长",
            "current_org": "隆德县人民政府",
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"]
        },
        "career_timeline": [
            {
                "start": "2026-06（推定）",
                "end": "至今",
                "org": "隆德县人民政府",
                "title": "隆德县委副书记、县长",
                "level": "县级",
                "location": "宁夏回族自治区固原市隆德县",
                "system": "government",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "2026年5月13日首次以'县委副书记、县长候选人'身份出现。2026年6月4日已以县长、县安委会主任身份主持全县安全生产会议。",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"]
            },
            {
                "start": "未知",
                "end": "2026年5月",
                "org": "履历缺口",
                "title": "",
                "notes": "公开资料未发现田玉铭2026年5月之前的履历信息。可能曾在固原市其他县区、市直部门或其他地市任职。",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "organizations": [
            {"org_id": "org_ld_county_gov", "name": "隆德县人民政府",
             "type": "政府", "level": "县级", "parent": "固原市人民政府",
             "location": "宁夏回族自治区固原市隆德县",
             "relation_to_person": "当前任职单位", "confidence": "confirmed",
             "source_ids": ["S002"]},
            {"org_id": "org_ld_safety", "name": "隆德县安全生产委员会",
             "type": "政府", "level": "县级", "parent": "隆德县人民政府",
             "location": "宁夏回族自治区固原市隆德县",
             "relation_to_person": "兼任职务", "confidence": "confirmed",
             "source_ids": ["S002"]}
        ],
        "relationships": [
            {"person": "刘永龙", "person_id": "ningxia_guyuan_longde_liuyonglong",
             "relationship_type": "superior_subordinate", "strength": "strong",
             "evidence": "刘永龙（县委书记）与田玉铭（县长）是隆德县党政主要领导搭档。刘永龙从县长升任县委书记后，田玉铭接任县长。",
             "overlap_org": "隆德县", "overlap_period": "2026年5月起",
             "direction": "other_to_person", "confidence": "confirmed",
             "source_ids": ["S001", "S002"]}
        ],
        "governance_record": [
            {"period": "2026年6月", "domain": "public_security",
             "achievement_or_event": "主持县安委会2026年第四次全体（扩大）会议，部署全县安全生产工作",
             "role_in_event": "主持（以县长、县安委会主任身份）",
             "measurable_outcome": "", "location": "隆德县",
             "confidence": "confirmed", "source_ids": ["S002"]}
        ],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["government"],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "田玉铭2026年5月以县长候选人身份首次出现，2026年6月确认为县长。但此前履历完全未知，无法评估晋升轨迹。",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "unknown", "evidence": "",
                 "confidence": "unverified", "source_ids": []}
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment. No behavioral data available for this figure."
        },
        "network_metrics": {
            "total_relationships": 1,
            "strong_edges": 1,
            "unique_organizations": 2,
            "known_predecessors": ["刘永龙（前县长，现县委书记）"],
            "known_successors": []
        },
        "risk_and_integrity_signals": [
            {"type": "none_found",
             "description": "截至2026年7月，未发现田玉铭在公开记录中有纪律处分、审计问题或负面媒体报道。",
             "date": AS_OF, "confidence": "plausible", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "2026年第一次为企业纾困解难集中办公会",
             "url": SOURCES["S001"]["url"], "publisher": "隆德县人民政府",
             "published_at": "2026-05-15", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high",
             "notes": "田玉铭以县委副书记、县长候选人身份主持"},
            {"id": "S002", "title": "县安委会2026年第四次全体（扩大）会议",
             "url": SOURCES["S002"]["url"], "publisher": "隆德县人民政府",
             "published_at": "2026-06-04", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high",
             "notes": "田玉铭以县长、县安委会主任身份主持"}
        ],
        "confidence_summary": {
            "identity": "thin",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "田玉铭的全部履历（出生、教育、入党、此前职务）均为未知"
        },
        "open_questions": [
            {"priority": "critical",
             "question": "田玉铭的出生年份、出生地、民族、教育背景是什么？",
             "why_it_matters": "基础身份信息缺失，影响人员去重和网络分析。",
             "suggested_queries": ["田玉铭 简历", "田玉铭 宁夏 固原", "田玉铭 百度百科"],
             "last_attempted": AS_OF},
            {"priority": "critical",
             "question": "田玉铭2026年5月之前的职业生涯是怎样的？他从哪个部门/地区调任至隆德县？",
             "why_it_matters": "无法评估其职业轨迹和专业背景。",
             "suggested_queries": ["田玉铭 固原市 任职", "固原市委组织部 任前公示 田玉铭"],
             "last_attempted": AS_OF},
            {"priority": "high",
             "question": "田玉铭此前是否为隆德县常务副县长或固原市市直部门负责人？",
             "why_it_matters": "了解县长选任来源模式。",
             "suggested_queries": ["田玉铭 常务副县长", "隆德县 提名 县长 田玉铭"],
             "last_attempted": AS_OF}
        ]
    }


def write_person_json(data: dict, filename_suffix: str) -> Path:
    """Write a person JSON file and return the path."""
    filename = f"{TODAY}-宁夏回族自治区-固原市-{filename_suffix}.json"
    path = PJSON_DIR / filename
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {path}")
    return path


# ── Build ──────────────────────────────────────────────────────────────
def main() -> None:
    print(f"Building {SLUG} leadership network...")
    print(f"  Staging: {STAGING}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

    # Build database and GEXF using the runner
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
    liuyonglong = make_person_json_liuyonglong()
    tianyuming = make_person_json_tianyuming()

    write_person_json(liuyonglong, "县委书记-刘永龙")
    write_person_json(tianyuming, "县长-田玉铭")

    print(f"\nDone. Staged artifacts in: {STAGING}")
    print(f"  1. Build script: {__file__}")
    print(f"  2. Database: {DB_PATH}")
    print(f"  3. GEXF: {GEXF_PATH}")
    print(f"  4. Person JSONs: {PJSON_DIR}")

    # Print summary
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)} (including {sum(1 for p in persons if '待查' not in p['name'])} named)")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Sources: {len(SOURCES)} official URLs")


if __name__ == "__main__":
    main()
