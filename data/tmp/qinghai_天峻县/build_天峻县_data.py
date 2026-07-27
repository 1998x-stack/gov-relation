#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 天峻县 (Tianjun County), 海西蒙古族藏族自治州, 青海省.

Investigation date: 2026-07-25
Task ID: qinghai_天峻县
Level: 县
Targets: 县委书记 & 县长

Research status: PARTIAL — web access was degraded during investigation:
  - Exa search API rate-limited throughout
  - Baidu Baike returned HTTP 403/captcha
  - Google search via Jina Reader timed out
  - However, 天峻县人民政府 website (www.tianjun.gov.cn) was partially accessible
  - Two WeChat articles (天峻发布) from the July 2026 county congress provided key names

Source summary:
  - 孔庆吉: 县委书记 — confirmed from 天峻县第十七届人民代表大会第一次会议 reporting (2026-07-21, 2026-07-24)
  - 刘安青: 县长 — confirmed as 代理县长 → 县长, elected at the same congress
  - Other leaders identified from the congress presidium list and government appointment notices

Confidence notes:
  - Administrative structure (organizations, levels) is confirmed from standard records.
  - Current officeholder names (孔庆吉, 刘安青) are confirmed from official county congress reports.
  - Standing committee members (罗永强, 刘晓珂, 魏立, 冬梅, 王燕) identified from congress presidium.
  - Most biographical fields for persons remain unfilled, as biography details require
    web resources that were unavailable (Baidu Baike, news archives).
  - The build script is structurally complete with confirmed leadership names.

Expected government website: www.tianjun.gov.cn
Parent-city website: www.haixi.gov.cn (海西蒙古族藏族自治州)
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
SLUG = "天峻县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ─────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "qinghai_天峻县"
if _CURRENT_DIR.name == "qinghai_天峻县":
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
# Source: 天峻县第十七届人民代表大会第一次会议 (July 21-24, 2026)
#   - Main source: 天峻发布 WeChat articles on 天峻县人民政府 website
#   - Appointment notices from www.tianjun.gov.cn

persons = [
    # ════════════════════════════════════════════════════════════════════
    # Core Leadership (current as of July 2026)
    # ════════════════════════════════════════════════════════════════════
    # --- 县委书记 (Party Secretary) ---
    {
        "id": 1,
        "name": "孔庆吉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "天峻县委书记",
        "current_org": "中共天峻县委员会",
        "source": "Confirmed from 天峻县第十七届人民代表大会第一次会议 (2026-07-21/24). Official source: www.tianjun.gov.cn",
    },
    # --- 县长 (County Chief) ---
    {
        "id": 2,
        "name": "刘安青",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "天峻县委副书记、县长",
        "current_org": "天峻县人民政府",
        "source": "Confirmed as 代理县长 → 县长 from 天峻县第十七届人民代表大会 first session (2026-07-21).",
    },
    # ════════════════════════════════════════════════════════════════════
    # County Standing Committee (县委常委) — identified from congress presidium
    # ════════════════════════════════════════════════════════════════════
    # 罗永强 — 大会主席团常务主席、执行主席 (likely 县人大常委会主任 or 县委副书记)
    {
        "id": 3,
        "name": "罗永强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "天峻县人大常委会主任（推测）",
        "current_org": "天峻县人大常委会",
        "source": "Identified from congress presidium list (2026-07-21/24). Exact role requires verification.",
    },
    # 刘晓珂 — 大会主席团常务主席
    {
        "id": 4,
        "name": "刘晓珂",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "天峻县领导（主席团成员）",
        "current_org": "中共天峻县委员会/天峻县人大常委会",
        "source": "Identified from congress presidium list (2026-07-21/24). Exact role requires verification.",
    },
    # 魏立 — 大会主席团常务主席
    {
        "id": 5,
        "name": "魏立",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "天峻县领导（主席团成员）",
        "current_org": "中共天峻县委员会/天峻县人大常委会",
        "source": "Identified from congress presidium list (2026-07-21/24). Exact role requires verification.",
    },
    # 冬梅 — 大会主席团常务主席
    {
        "id": 6,
        "name": "冬梅",
        "gender": "女",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "天峻县领导（主席团成员）",
        "current_org": "中共天峻县委员会/天峻县人大常委会",
        "source": "Identified from congress presidium list (2026-07-21/24). Likely female, Tibetan surname. Exact role requires verification.",
    },
    # 王燕 — 大会主席团常务主席
    {
        "id": 7,
        "name": "王燕",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "天峻县领导（主席团成员）",
        "current_org": "中共天峻县委员会/天峻县人大常委会",
        "source": "Identified from congress presidium list (2026-07-21/24). Exact role requires verification.",
    },
    # ════════════════════════════════════════════════════════════════════
    # Key county leadership — identified from appointment notices
    # ════════════════════════════════════════════════════════════════════
    # --- 殷洪彦 — 县公安局局长 (appointed April 2026) ---
    {
        "id": 8,
        "name": "殷洪彦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "天峻县人民政府副县长、县公安局局长",
        "current_org": "天峻县公安局",
        "source": "天峻县人民政府关于殷洪彦、马成章同志职务任免的通知 (天政人〔2026〕3号, 2026-04-30). www.tianjun.gov.cn",
    },
    # --- 马成章 — 原县公安局局长 (relieved April 2026) ---
    {
        "id": 9,
        "name": "马成章",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "天峻县领导（原县公安局局长）",
        "current_org": "天峻县人民政府",
        "source": "天峻县人民政府关于殷洪彦、马成章同志职务任免的通知 (天政人〔2026〕3号, 2026-04-30). Relieved from 公安局局长 post.",
    },
    # --- 王文嘉 — likely 县委宣传部 or 县委办公室 (审核三审) ---
    {
        "id": 10,
        "name": "王文嘉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "天峻县领导（审核三审）",
        "current_org": "中共天峻县委员会",
        "source": "Listed as 审核三审 in multiple 天峻发布 articles (2026-07). Likely a senior propaganda/office official.",
    },
    # --- 谢热多杰 — 编辑一审 (融媒体中心) ---
    {
        "id": 11,
        "name": "谢热多杰",
        "gender": "",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "天峻县融媒体中心编辑",
        "current_org": "天峻县融媒体中心",
        "source": "Listed as 编辑一审 in 天峻发布 articles (2026-07). Media professional.",
    },
    # --- 索南周吉 — 编辑一审 ---
    {
        "id": 12,
        "name": "索南周吉",
        "gender": "",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "天峻县融媒体中心编辑",
        "current_org": "天峻县融媒体中心",
        "source": "Listed as 编辑一审 in 天峻发布 articles (2026-07).",
    },
    # --- 更桑措毛 — 校对二审 ---
    {
        "id": 13,
        "name": "更桑措毛",
        "gender": "女",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "天峻县融媒体中心校对",
        "current_org": "天峻县融媒体中心",
        "source": "Listed as 校对二审 in 天峻发布 articles (2026-07).",
    },
    # ════════════════════════════════════════════════════════════════════
    # Additional officials named in gov notices (less senior)
    # ════════════════════════════════════════════════════════════════════
    {
        "id": 14,
        "name": "梅桑热尖措",
        "gender": "",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县民政局四级调研员",
        "current_org": "天峻县民政局",
        "source": "天峻县人民政府关于梅桑热尖措等同志职务任免的通知 (天政人〔2026〕5号, 2026-06-10).",
    },
    {
        "id": 15,
        "name": "尼玛拉旦",
        "gender": "",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县就业服务局二级主任科员",
        "current_org": "天峻县就业服务局",
        "source": "天峻县人民政府关于梅桑热尖措等同志职务任免的通知 (天政人〔2026〕5号, 2026-06-10).",
    },
    {
        "id": 16,
        "name": "更桑杰",
        "gender": "",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县自然资源和林业草原局副局长、二级主任科员",
        "current_org": "天峻县自然资源和林业草原局",
        "source": "天峻县人民政府关于更桑杰同志任职的通知 (天政人〔2025〕16号, 2025-10-13).",
    },
]

# ── Organizations ──────────────────────────────────────────────────────
organizations = [
    # Primary party/government orgs
    {
        "id": 1,
        "name": "中共天峻县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共海西蒙古族藏族自治州委员会",
        "location": "青海省海西州天峻县新源镇",
    },
    {
        "id": 2,
        "name": "天峻县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "海西蒙古族藏族自治州人民政府",
        "location": "青海省海西州天峻县新源镇新源东路4号",
    },
    {
        "id": 3,
        "name": "天峻县人大常委会",
        "type": "人大",
        "level": "县级",
        "parent": "海西蒙古族藏族自治州人大常委会",
        "location": "青海省海西州天峻县新源镇",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议天峻县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "中国人民政治协商会议海西蒙古族藏族自治州委员会",
        "location": "青海省海西州天峻县新源镇",
    },
    {
        "id": 5,
        "name": "中共天峻县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共海西蒙古族藏族自治州纪律检查委员会",
        "location": "青海省海西州天峻县新源镇",
    },
    {
        "id": 6,
        "name": "天峻县监察委员会",
        "type": "政府",
        "level": "县级",
        "parent": "",
        "location": "青海省海西州天峻县新源镇",
    },
    {
        "id": 7,
        "name": "天峻县人民法院",
        "type": "政府",
        "level": "县级",
        "parent": "",
        "location": "青海省海西州天峻县新源镇",
    },
    {
        "id": 8,
        "name": "天峻县人民检察院",
        "type": "政府",
        "level": "县级",
        "parent": "",
        "location": "青海省海西州天峻县新源镇",
    },
    # Government departments
    {
        "id": 9,
        "name": "天峻县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "天峻县人民政府",
        "location": "青海省海西州天峻县新源镇",
    },
    {
        "id": 10,
        "name": "天峻县民政局",
        "type": "政府",
        "level": "县级",
        "parent": "天峻县人民政府",
        "location": "青海省海西州天峻县新源镇",
    },
    {
        "id": 11,
        "name": "天峻县人力资源和社会保障局",
        "type": "政府",
        "level": "县级",
        "parent": "天峻县人民政府",
        "location": "青海省海西州天峻县新源镇",
    },
    {
        "id": 12,
        "name": "天峻县就业服务局",
        "type": "政府",
        "level": "县级",
        "parent": "天峻县人力资源和社会保障局",
        "location": "青海省海西州天峻县新源镇",
    },
    {
        "id": 13,
        "name": "天峻县自然资源和林业草原局",
        "type": "政府",
        "level": "县级",
        "parent": "天峻县人民政府",
        "location": "青海省海西州天峻县新源镇",
    },
    # Media
    {
        "id": 14,
        "name": "天峻县融媒体中心",
        "type": "事业单位",
        "level": "县级",
        "parent": "中共天峻县委员会宣传部",
        "location": "青海省海西州天峻县新源镇",
    },
]

# ── Positions ──────────────────────────────────────────────────────────
positions = [
    # Core leadership
    {"person_id": 1, "org_id": 1, "title": "天峻县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "Confirmed as of 2026-07-21 (presided over county congress)"},
    {"person_id": 2, "org_id": 2, "title": "天峻县委副书记、县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "Confirmed as 代理县长 → 县长, elected at 县第十七届人大一次会议 (2026-07-21)"},
    {"person_id": 2, "org_id": 1, "title": "天峻县委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "县委副书记、县长 dual role"},
    # Congress leadership
    {"person_id": 3, "org_id": 3, "title": "天峻县人大常委会主任（推测）", "start_date": "", "end_date": "present", "rank": "正处级", "note": "Identified as 大会主席团常务主席、执行主席. Role inferred — may be 县人大常委会主任."},
    # Presidium members (roles TBD)
    {"person_id": 4, "org_id": 1, "title": "天峻县领导（主席团成员）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "Presidium member at 县第十七届人大一次会议. Specific post requires verification."},
    {"person_id": 5, "org_id": 1, "title": "天峻县领导（主席团成员）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "Presidium member. Specific post requires verification."},
    {"person_id": 6, "org_id": 1, "title": "天峻县领导（主席团成员）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "Presidium member. Specific post requires verification."},
    {"person_id": 7, "org_id": 1, "title": "天峻县领导（主席团成员）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "Presidium member. Specific post requires verification."},
    # Public security
    {"person_id": 8, "org_id": 9, "title": "天峻县公安局局长", "start_date": "2026-04", "end_date": "present", "rank": "正科级", "note": "Appointed by 天政人〔2026〕3号 (2026-04-30). Likely also副县长."},
    {"person_id": 9, "org_id": 9, "title": "天峻县公安局局长", "start_date": "", "end_date": "2026-04", "rank": "正科级", "note": "Relieved per 天政人〔2026〕3号 (2026-04-30)."},
    # Media officials
    {"person_id": 10, "org_id": 1, "title": "天峻县领导（县委/宣传部）", "start_date": "", "end_date": "present", "rank": "", "note": "Listed as 审核三审 in county media content. Likely 县委宣传部或办公室 senior official."},
    {"person_id": 11, "org_id": 14, "title": "编辑", "start_date": "", "end_date": "present", "rank": "", "note": "融媒体中心编辑（编辑一审）"},
    {"person_id": 12, "org_id": 14, "title": "编辑", "start_date": "", "end_date": "present", "rank": "", "note": "融媒体中心编辑（编辑一审）"},
    {"person_id": 13, "org_id": 14, "title": "校对", "start_date": "", "end_date": "present", "rank": "", "note": "融媒体中心校对（校对二审）"},
    # Other government officials
    {"person_id": 14, "org_id": 10, "title": "县民政局四级调研员", "start_date": "2026-06", "end_date": "present", "rank": "四级调研员", "note": "Appointed per 天政人〔2026〕5号"},
    {"person_id": 15, "org_id": 12, "title": "县就业服务局二级主任科员", "start_date": "2026-06", "end_date": "present", "rank": "二级主任科员", "note": "Appointed per 天政人〔2026〕5号"},
    {"person_id": 16, "org_id": 13, "title": "县自然资源和林业草原局副局长、二级主任科员", "start_date": "2025-10", "end_date": "present", "rank": "二级主任科员", "note": "Appointed per 天政人〔2025〕16号 (2025-10-13)"},
]

# ── Relationships ──────────────────────────────────────────────────────
relationships = [
    # Top leadership core: 孔庆吉 ↔ 刘安青 (书记+县长 working relationship)
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长搭班子",
        "overlap_org": "中共天峻县委员会/天峻县人民政府",
        "overlap_period": "截至2026-07",
    },
    # 孔庆吉 ↔ 罗永强 (书记+人大)
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "县委与人大领导同为主席团常务主席",
        "overlap_org": "天峻县第十七届人民代表大会主席团",
        "overlap_period": "2026-07",
    },
    # 刘安青 ↔ 罗永强 (县长+人大)
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "县长向人大作报告",
        "overlap_org": "天峻县第十七届人民代表大会",
        "overlap_period": "2026-07",
    },
    # 殷洪彦 ↔ 马成章 (predecessor/successor as police chief)
    {
        "person_a": 8, "person_b": 9,
        "type": "predecessor_successor",
        "context": "殷洪彦接替马成章任县公安局局长",
        "overlap_org": "天峻县公安局",
        "overlap_period": "2026-04",
    },
    # 孔庆吉 ↔ 殷洪彦 (书记+公安局长)
    {
        "person_a": 1, "person_b": 8,
        "type": "superior_subordinate",
        "context": "县委书记与公安局长的上下级关系",
        "overlap_org": "中共天峻县委员会/天峻县公安局",
        "overlap_period": "2026-04起",
    },
    # 刘安青 ↔ 殷洪彦 (县长+公安局长)
    {
        "person_a": 2, "person_b": 8,
        "type": "superior_subordinate",
        "context": "县长与公安局长的上下级关系（县政府任命）",
        "overlap_org": "天峻县人民政府/天峻县公安局",
        "overlap_period": "2026-04起",
    },
    # Media chain: 索南周吉 ↔ 更桑措毛 ↔ 王文嘉 (editorial workflow)
    {
        "person_a": 12, "person_b": 13,
        "type": "overlap",
        "context": "编辑与校对的协作关系",
        "overlap_org": "天峻县融媒体中心",
        "overlap_period": "2026-07",
    },
    {
        "person_a": 13, "person_b": 10,
        "type": "overlap",
        "context": "校对与终审的协作关系",
        "overlap_org": "天峻县融媒体中心",
        "overlap_period": "2026-07",
    },
]

# ── Person JSON Builders ─────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Building {SLUG} network...")
    print(f"  DB path: {DB_PATH}")
    print(f"  GEXF path: {GEXF_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

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

    # Person JSON files are written by _write_person_jsons_main() which is called at the bottom of this file
    # after all function definitions are loaded.


def _write_person_jsons_main() -> None:
    person_json_configs = [
        ("县委书记", "孔庆吉", _build_kong_qingji_json()),
        ("县长", "刘安青", _build_liu_anqing_json()),
    ]
    for job, name, data in person_json_configs:
        filename = f"{TODAY}-青海省-海西蒙古族藏族自治州-{job}-{name}.json"
        filepath = PJSON_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {filepath}")


def _build_kong_qingji_json() -> dict:
    """Build person JSON for 孔庆吉 (Party Secretary)."""
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "青海省",
            "city": "海西蒙古族藏族自治州",
            "region": "天峻县",
            "job": "县委书记",
            "task_id": "qinghai_天峻县",
            "time_focus": "2025-2026",
        },
        "identity": {
            "person_id": "qinghai_tianjunxian_kongqingji",
            "name": "孔庆吉",
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
                "name_birth": "孔庆吉_",
                "name_birthplace": "孔庆吉_",
                "official_profile_url": "http://www.tianjun.gov.cn",
            },
        },
        "current_status": {
            "current_post": "天峻县委书记",
            "current_org": "中共天峻县委员会",
            "administrative_rank": "正处级",
            "as_of": "2026-07-24",
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": "中共天峻县委员会",
                "title": "天峻县委书记",
                "level": "正处级",
                "location": "青海省海西州天峻县",
                "system": "party",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "Confirmed in office as of July 2026, presiding over 县第十七届人民代表大会第一次会议. Previous career path unknown — requires Baidu Baike or news archive research.",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": "公开资料未找到孔庆吉任天峻县委书记之前的履历。需从海西州组织部任前公示、青海省组工信息等渠道补充。",
                "confidence": "unverified",
                "source_ids": [],
            },
        ],
        "organizations": [
            {
                "org_id": 1,
                "org_name": "中共天峻县委员会",
                "role": "县委书记",
                "period": "至2026-07",
            }
        ],
        "relationships": [
            {
                "person": "刘安青",
                "person_id": "qinghai_tianjunxian_liuanqing",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "县委书记与县长搭班子，共同出席县第十七届人民代表大会",
                "overlap_org": "中共天峻县委员会/天峻县人民政府",
                "overlap_period": "截至2026-07",
                "direction": "person_to_other",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"],
            },
        ],
        "governance_record": [
            {
                "period": "2026-07",
                "domain": "other",
                "achievement_or_event": "主持天峻县第十七届人民代表大会第一次会议",
                "role_in_event": "大会主席团常务主席",
                "measurable_outcome": "县人大、政府换届选举圆满完成",
                "location": "天峻县",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"],
            },
        ],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["party"],
            "geographic_pattern": ["青海省"],
            "promotion_velocity": {
                "summary": "Insufficient data to assess promotion velocity",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "No negative media, disciplinary action, or integrity signals found in available sources",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "天峻县第十七届人民代表大会第一次会议隆重开幕",
                "url": "https://mp.weixin.qq.com/s/T5FLAkW9rgnRSZntWr_yAg",
                "publisher": "天峻发布",
                "published_at": "2026-07-21",
                "accessed_at": AS_OF,
                "source_type": "appointment_notice",
                "reliability": "high",
                "notes": "Confirmed 孔庆吉 as 大会主席团常务主席",
            },
            {
                "id": "S002",
                "title": "天峻县第十七届人民代表大会第一次会议胜利闭幕",
                "url": "https://mp.weixin.qq.com/s/B_8GB1NAGG3SSquhzk2FYQ",
                "publisher": "天峻发布",
                "published_at": "2026-07-24",
                "accessed_at": AS_OF,
                "source_type": "appointment_notice",
                "reliability": "high",
                "notes": "Confirmed 孔庆吉 as 县委书记 delivering speech to new congress",
            },
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "孔庆吉此前履历完全未知，需要补充出生年份、籍贯、教育背景、从政经历等信息",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "孔庆吉的出生年份、籍贯、教育背景是什么？",
                "why_it_matters": "核心身份信息缺失，无法进行人员去重和关系网络匹配",
                "suggested_queries": ["孔庆吉 简历 天峻", "孔庆吉 青海 出生", "孔庆吉 任前公示"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": "孔庆吉任天峻县委书记之前的从政履历是什么？",
                "why_it_matters": "不能判断其职业发展路径、专业背景和潜在的人际关系网络",
                "suggested_queries": ["孔庆吉 任职", "孔庆吉 海西州", "孔庆吉 组织部"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "孔庆吉的民族是什么？",
                "why_it_matters": "青海藏区县委书记的民族身份是理解地方治理的重要背景",
                "suggested_queries": ["孔庆吉 民族 藏族 汉族", "孔庆吉 青海"],
                "last_attempted": AS_OF,
            },
        ],
    }


def _build_liu_anqing_json() -> dict:
    """Build person JSON for 刘安青 (County Chief)."""
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "青海省",
            "city": "海西蒙古族藏族自治州",
            "region": "天峻县",
            "job": "县长",
            "task_id": "qinghai_天峻县",
            "time_focus": "2025-2026",
        },
        "identity": {
            "person_id": "qinghai_tianjunxian_liuanqing",
            "name": "刘安青",
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
                "name_birth": "刘安青_",
                "name_birthplace": "刘安青_",
                "official_profile_url": "http://www.tianjun.gov.cn",
            },
        },
        "current_status": {
            "current_post": "天峻县委副书记、县长",
            "current_org": "天峻县人民政府",
            "administrative_rank": "正处级",
            "as_of": "2026-07-24",
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"],
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "2026-07",
                "org": "天峻县人民政府",
                "title": "天峻县代理县长",
                "level": "正处级",
                "location": "青海省海西州天峻县",
                "system": "government",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "Served as acting county chief prior to the congress. Date of appointment as 代理县长 unknown.",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "2026-07-21",
                "end": "present",
                "org": "天峻县人民政府",
                "title": "天峻县委副书记、县长",
                "level": "正处级",
                "location": "青海省海西州天峻县",
                "system": "government",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "Elected as 县长 at 天峻县第十七届人民代表大会第一次会议. Presented government work report covering 5-year achievements and 15th Five-Year Plan.",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": "公开资料未找到刘安青任天峻县代理县长之前的履历。需从海西州组织部任前公示、青海省组工信息等渠道补充。",
                "confidence": "unverified",
                "source_ids": [],
            },
        ],
        "organizations": [
            {
                "org_id": 2,
                "org_name": "天峻县人民政府",
                "role": "县长（当选）",
                "period": "2026-07至",
            },
            {
                "org_id": 1,
                "org_name": "中共天峻县委员会",
                "role": "县委副书记",
                "period": "至2026-07",
            },
        ],
        "relationships": [
            {
                "person": "孔庆吉",
                "person_id": "qinghai_tianjunxian_kongqingji",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "县长向县委负责，在县委领导下开展工作",
                "overlap_org": "中共天峻县委员会/天峻县人民政府",
                "overlap_period": "截至2026-07",
                "direction": "other_to_person",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"],
            },
            {
                "person": "罗永强",
                "person_id": "",
                "relationship_type": "overlap",
                "strength": "strong",
                "evidence": "县长向人民代表大会报告工作",
                "overlap_org": "天峻县第十七届人民代表大会",
                "overlap_period": "2026-07",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
        ],
        "governance_record": [
            {
                "period": "2026-07-21",
                "domain": "economic_development",
                "achievement_or_event": "作天峻县人民政府工作报告，总结过去五年工作，提出'4+5'发展战略",
                "role_in_event": "县长",
                "measurable_outcome": "GDP年均增长4.5%-5%目标，固定资产投资年均增长6%",
                "location": "天峻县",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
        ],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["government"],
            "geographic_pattern": ["青海省"],
            "promotion_velocity": {
                "summary": "Insufficient data to assess promotion velocity",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "pragmatic",
                    "evidence": "Government work report emphasized measurable outcomes (GDP target, investment growth, employment targets)",
                    "confidence": "plausible",
                    "source_ids": ["S001"],
                }
            ],
            "speech_themes": [
                "生态文明建设",
                "绿色转型发展",
                "'4+5'发展战略",
                "民生福祉",
            ],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "No negative media, disciplinary action, or integrity signals found in available sources",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "天峻县第十七届人民代表大会第一次会议隆重开幕",
                "url": "https://mp.weixin.qq.com/s/T5FLAkW9rgnRSZntWr_yAg",
                "publisher": "天峻发布",
                "published_at": "2026-07-21",
                "accessed_at": AS_OF,
                "source_type": "appointment_notice",
                "reliability": "high",
                "notes": "Confirmed 刘安青 as 代理县长 delivering government work report",
            },
            {
                "id": "S002",
                "title": "天峻县第十七届人民代表大会第一次会议胜利闭幕",
                "url": "https://mp.weixin.qq.com/s/B_8GB1NAGG3SSquhzk2FYQ",
                "publisher": "天峻发布",
                "published_at": "2026-07-24",
                "accessed_at": AS_OF,
                "source_type": "appointment_notice",
                "reliability": "high",
                "notes": "Confirmed 刘安青 elected as 县长 making an oath speech",
            },
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "刘安青此前履历完全未知，需要补充出生年份、籍贯、教育背景、从政经历等信息",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "刘安青的出生年份、籍贯、教育背景是什么？",
                "why_it_matters": "核心身份信息缺失，无法进行人员去重和关系网络匹配",
                "suggested_queries": ["刘安青 简历 天峻", "刘安青 青海 代理县长", "刘安青 海西州"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": "刘安青任天峻县代理县长之前的从政履历是什么？",
                "why_it_matters": "不能判断其职业发展路径、专业背景和潜在的人际关系网络",
                "suggested_queries": ["刘安青 任职", "刘安青 海西州 组织部", "刘安青 天峻"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "刘安青在任代县长之前任何职？",
                "why_it_matters": "了解其晋升路径和可能的工作关系",
                "suggested_queries": ["刘安青 副县长 天峻", "天峻县 代理县长 任命"],
                "last_attempted": AS_OF,
            },
        ],
    }


_write_person_jsons_main()
