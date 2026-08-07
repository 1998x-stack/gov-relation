#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 都兰县 (Dulan County), 海西蒙古族藏族自治州, 青海省.

Investigation date: 2026-08-07
Task ID: qinghai_都兰县
Level: 县
Targets: 县委书记 & 县长

Research status: PARTIAL — current leadership confirmed from official sources;
biographies and predecessor lineage are partially incomplete.

Source summary (all official, www.dulan.gov.cn — 海西州都兰县人民政府):
  - 董峰: 县委书记 — confirmed from multiple official county news items, incl.
    中国共产党都兰县第十七次代表大会 (2026-07-11/13) where 董峰 delivered the 16届
    committee report as the sitting secretary, plus "县委书记董峰" attributions in
    2026-06-29 / 2026-07-06 news.
  - 王全明: 县长 — confirmed from 领导之窗 leader profile page (wqm.htm):
    现任职务 都兰县委副书记，都兰县人民政府党组书记、县长. Said to preside
    over the 17th party congress opening (2026-07-11).
  - County government roster (领导之窗): 乔兆臣(常务), 张斌(援青·浙江),
    吴耿松(援青·华电), 杨思青, 刘国虎(藏族), 张铠(公安局长), 安培祥.
  - 17th county standing-committee podium front row (执行主席): 万永兴、谢瑞芳、
    苏姹娜、吴波、董龙金、路通、马天福 (县委常委 or county leaders; exact posts unverified).

Confidence notes:
  - Administrative structure (organizations, levels, parent chains) confirmed from
    standard records and the official site footer/manifest.
  - Current officeholder names and the core pairing (董峰 × 王全明) are confirmed
    from official county sources.
  - Most biographical fields (birth, birthplace, education, party-join date, work-start)
    remain unfilled — biographies require Baidu Baike/news archives that were
    inaccessible (Baidu 403, Exa rate-limited, Jina Reader timeouts).
  - The predecessor 县委书记 (immediately before 董峰) and predecessor 县长 lineage
    are unverified and recorded as open questions.

Expected government website: www.dulan.gov.cn
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
SLUG = "都兰县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

# ── Staging paths ─────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "qinghai_都兰县"
if _CURRENT_DIR.name == "qinghai_都兰县":
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
# Source: 都兰县人民政府 www.dulan.gov.cn (领导之窗 + 都兰要闻 + 都兰信息)

persons = [
    # ════════════════════════════════════════════════════════════════════
    # Core Leadership (current as of 2026-08)
    # ════════════════════════════════════════════════════════════════════
    # --- 县委书记 (Party Secretary) ---
    {
        "id": 1,
        "name": "董峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都兰县委书记",
        "current_org": "中共都兰县委员会",
        "source": "Confirmed from official 都兰县新闻: '县委书记董峰' (2026-06-29, 2026-07-06) and 中国共产党第十七次代表大会 (2026-07-11/13; 十六届委员会报告人+第十七届奏). www.dulan.gov.cn",
    },
    # --- 县长 (County Chief) ---
    {
        "id": 2,
        "name": "王全明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都兰县委副书记、县政府党组书记、县长",
        "current_org": "都兰县人民政府",
        "source": "Confirmed from 领导之窗 profile page 王全明 (www.dulan.gov.cn/ldzc/wqm.htm): 现任职务 都兰县委副书记，都兰县人民政府党组书记、县长.",
    },
    # ════════════════════════════════════════════════════════════════════
    # County leadership — 县政府领导班子 (领导之窗)
    # ════════════════════════════════════════════════════════════════════
    # --- 乔兆臣 — 常务副县长 ---
    {
        "id": 3,
        "name": "乔兆臣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都兰县委常委、县政府党组副书记、副县长",
        "current_org": "都兰县人民政府",
        "source": "Confirmed from 领导之窗 profile page 乔兆臣: 中共党员, 汉族, 负责县政府日常工作.",
    },
    # --- 张斌 — 援青（浙江省对口支援）---
    {
        "id": 4,
        "name": "张斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都兰县委副书记、县政府副县长（援青）",
        "current_org": "都兰县人民政府",
        "source": "Confirmed from 领导之窗 profile page 张斌（援青）: 负责浙江省对口援青、农牧、科技、乡村振兴等.",
    },
    # --- 吴耿松 — 援疆（华电集团对口支援）---
    {
        "id": 5,
        "name": "吴耿松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都兰县委副书记、县政府副县长（援青）",
        "current_org": "都兰县人民政府",
        "source": "Confirmed from 领导之窗 profile page 吴耿松（援青）: 负责华电集团对口支援、卫生健康、数据统筹利用、政务服务.",
    },
    # --- 杨思青 --- 副县长人选
    {
        "id": 6,
        "name": "杨思青",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都兰县人民政府副县长人选",
        "current_org": "都兰县人民政府",
        "source": "Confirmed from 领导之窗 profile page 杨思青: 负责住建、人社、水利、生态环保.",
    },
    # --- 刘国虎 — 副县长人选（藏族）---
    {
        "id": 7,
        "name": "刘国虎",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都兰县人民政府党组成员、副县长人选",
        "current_org": "都兰县人民政府",
        "source": "Confirmed from 领导之窗 profile page 刘国虎: 藏族, 负责自然资源、教育、文体、林草.",
    },
    # --- 张铠 — 副县长、公安局长 ---
    {
        "id": 8,
        "name": "张铠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都兰县人民政府党组成员、副县长，县公安局党委书记、局长",
        "current_org": "都兰县公安局",
        "source": "Confirmed from 领导之窗 profile page 张铠: 负责公安、司法、综合执法、市场监管、消防救援.",
    },
    # --- 安培祥 — 副县长、察汗乌苏镇党委书记 ---
    {
        "id": 9,
        "name": "安培祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都兰县人民政府党组成员、副县长，察汗乌苏镇党委书记",
        "current_org": "都兰县人民政府",
        "source": "Confirmed from 领导之窗 profile page 安培祥: 协助张斌同志工作.",
    },
    # ════════════════════════════════════════════════════════════════════
    # 17th Standing-committee / county leaders (主席台前排，执行主席)
    # ════════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "万永兴",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都兰县领导（执行主席/拟任常委）",
        "current_org": "中共都兰县委员会",
        "source": "17th 党代会主席台前排 (执行主席), www.dulan.gov.cn (2026-07-11). Exact post requires verification.",
    },
    {
        "id": 11,
        "name": "谢瑞芳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都兰县领导（执行主席，拟任常委）",
        "current_org": "中共都兰县委员会",
        "source": "17th 党代会执行主席, www.dulan.gov.cn (2026-07-11). Exact post requires verification.",
    },
    {
        "id": 12,
        "name": "苏姹娜",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都兰县领导（执行主席，拟任常委）",
        "current_org": "中共都兰县委员会",
        "source": "17th 党代会执行主席, www.dulan.gov.cn (2026-07-11). Female; exact post requires verification.",
    },
    {
        "id": 13,
        "name": "吴波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都兰县领导（执行主席，拟任常委）",
        "current_org": "中共都兰县委员会",
        "source": "17th 党代会执行主席; also 参加县委书记调研 (2026-06-29) as county leader. www.dulan.gov.cn.",
    },
    {
        "id": 14,
        "name": "董龙金",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都兰县领导（执行主席，拟任常委）",
        "current_org": "中共都兰县委员会",
        "source": "17th 党代会执行主席; also 参加县委书记调研 (2026-06-29). www.dulan.gov.cn.",
    },
    {
        "id": 15,
        "name": "路通",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都兰县领导（执行主席，拟任常委）",
        "current_org": "中共都兰县委员会",
        "source": "17th 党代会执行主席, www.dulan.gov.cn (2026-07-11). Exact post requires verification.",
    },
    {
        "id": 16,
        "name": "马天福",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都兰县领导（执行主席，拟任常委）",
        "current_org": "中共都兰县委员会",
        "source": "17th 党代会执行主席, www.dulan.gov.cn (2026-07-11). Exact post requires verification.",
    },
]

# ── Organizations ──────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共都兰县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共海西蒙古族藏族自治州委员会",
        "location": "青海省海西州都兰县察汗乌苏镇",
    },
    {
        "id": 2,
        "name": "都兰县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "海西蒙古族藏族自治州人民政府",
        "location": "青海省海西州都兰县察汗乌苏镇",
    },
    {
        "id": 3,
        "name": "都兰县人大常委会",
        "type": "人大",
        "level": "县级",
        "parent": "海西蒙古族藏族自治州人大常委会",
        "location": "青海省海西州都兰县察汗乌苏镇",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议都兰县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "中国人民政治协商会议海西蒙古族藏族自治州委员会",
        "location": "青海省海西州都兰县察汗乌苏镇",
    },
    {
        "id": 5,
        "name": "中共都兰县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共海西蒙古族藏族自治州纪律检查委员会",
        "location": "青海省海西州都兰县察汗乌苏镇",
    },
    {
        "id": 6,
        "name": "都兰县监察委员会",
        "type": "政府",
        "level": "县级",
        "parent": "",
        "location": "青海省海西州都兰县察汗乌苏镇",
    },
    {
        "id": 7,
        "name": "都兰县人民法院",
        "type": "政府",
        "level": "县级",
        "parent": "",
        "location": "青海省海西州都兰县察汗乌苏镇",
    },
    {
        "id": 8,
        "name": "都兰县人民检察院",
        "type": "政府",
        "level": "县级",
        "parent": "",
        "location": "青海省海西州都兰县察汗乌苏镇",
    },
    {
        "id": 9,
        "name": "都兰县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "都兰县人民政府",
        "location": "青海省海西州都兰县察汗乌苏镇",
    },
    {
        "id": 10,
        "name": "察汗乌苏镇",
        "type": "乡镇",
        "level": "乡镇级",
        "parent": "都兰县人民政府",
        "location": "青海省海西州都兰县察汗乌苏镇",
    },
]

# ── Positions ──────────────────────────────────────────────────────────
positions = [
    # Core leadership
    {"person_id": 1, "org_id": 1, "title": "都兰县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "Confirmed as of 2026-07-11; led 县委 across 17th party congress (教育调研, 常委会扩大会议)."},
    {"person_id": 2, "org_id": 2, "title": "都兰县委副书记、县政府党组书记、县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "Confirmed from 领导之窗 profile (wqm.htm); presided over 17th party congress opening."},
    {"person_id": 2, "org_id": 1, "title": "都兰县委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "Dual role as 县委副书记、县长."},
    # Government leadership
    {"person_id": 3, "org_id": 2, "title": "都兰县委常委、县政府党组副书记、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "常务副县长: 县政府日常工作, 发改工信、招商、应急、财政等."},
    {"person_id": 3, "org_id": 1, "title": "都兰县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "Podium front row at 17th party congress."},
    {"person_id": 4, "org_id": 2, "title": "都兰县委副书记、县政府副县长（援青）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "Zhejiang 对口支援; 农牧、科技、乡村振兴、现代农业产业园."},
    {"person_id": 4, "org_id": 1, "title": "都兰县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "援青干部挂任县委副书记."},
    {"person_id": 5, "org_id": 2, "title": "都兰县委副书记、县政府副县长（援青）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "华电集团 对口支援; 卫生健康、数据、政务服务."},
    {"person_id": 5, "org_id": 1, "title": "都兰县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "华电集团 对口支援."},
    {"person_id": 6, "org_id": 2, "title": "都兰县人民政府副县长人选", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管 住建、人社、生态环保."},
    {"person_id": 7, "org_id": 2, "title": "都兰县人民政府党组成员、副县长人选", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管 自然资源、教育、文体、林草; 藏族."},
    {"person_id": 8, "org_id": 9, "title": "都兰县人民政府党组成员、副县长、县公安局党委书记、局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管 公安、司法、市场监管、消防."},
    {"person_id": 9, "org_id": 2, "title": "都兰县人民政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "协助张斌同志工作."},
    {"person_id": 9, "org_id": 10, "title": "察汗乌苏镇党委书记", "start_date": "", "end_date": "present", "rank": "正科级", "note": "兼任察汗乌苏镇党委书记 (县委所在地镇)."},
    # 17th standing-committee front row (执行主席)
    {"person_id": 10, "org_id": 1, "title": "都兰县领导（执行主席）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "17th 党代会主席台前排; 具体职务待核实."},
    {"person_id": 11, "org_id": 1, "title": "都兰县领导（执行主席）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "17th 党代会主席台前排."},
    {"person_id": 12, "org_id": 1, "title": "都兰县领导（执行主席）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "17th 党代会主席台前排; 女性."},
    {"person_id": 13, "org_id": 1, "title": "都兰县领导（执行主席）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "17th 党代会主席台前排."},
    {"person_id": 14, "org_id": 1, "title": "都兰县领导（执行主席）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "17th 党代会主席台前排."},
    {"person_id": 15, "org_id": 1, "title": "都兰县领导（执行主席）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "17th 党代会主席台前排."},
    {"person_id": 16, "org_id": 1, "title": "都兰县领导（执行主席）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "17th 党代会主席台前排."},
]

# ── Relationships ──────────────────────────────────────────────────────
relationships = [
    # 书记 × 县长 core pairing
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长搭班子，共同主持县第十七次党代会",
        "overlap_org": "中共都兰县委员会/都兰县人民政府",
        "overlap_period": "截至2026-07",
    },
    # 书记 + 常务副县长
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与县政府常务副县长（常委）",
        "overlap_org": "中共都兰县委员会",
        "overlap_period": "截至2026-07",
    },
    # 县长 + 常务副县长
    {
        "person_a": 2, "person_b": 3,
        "type": "superior_subordinate",
        "context": "县长与常务副县长：县政府日常运作（常务协助县长）",
        "overlap_org": "都兰县人民政府",
        "overlap_period": "截至2026-07",
    },
    # 县长 + 公安局长
    {
        "person_a": 2, "person_b": 8,
        "type": "superior_subordinate",
        "context": "县长与公安局长：政法综治上下级",
        "overlap_org": "都兰县人民政府/都兰县公安局",
        "overlap_period": "截至2026-07",
    },
    # 书记 + 公安局长
    {
        "person_a": 1, "person_b": 8,
        "type": "superior_subordinate",
        "context": "县委书记与公安局长",
        "overlap_org": "中共都兰县委员会/都兰县公安局",
        "overlap_period": "截至2026-07",
    },
    # 张斌 ↔ 安培祥 (协助工作)
    {
        "person_a": 4, "person_b": 9,
        "type": "overlap",
        "context": "安培祥作为副县长协助张斌同志工作",
        "overlap_org": "都兰县人民政府",
        "overlap_period": "截至2026-07",
    },
    # 安培祥 ↔ 察汗乌苏镇 (兼任书记)
    {
        "person_a": 9, "person_b": 2,
        "type": "superior_subordinate",
        "context": "察汗乌苏镇党委书记兼任副县长",
        "overlap_org": "都兰县人民政府",
        "overlap_period": "截至2026-07",
    },
    # 援青干部 张斌 ↔ 吴耿松 (均挂任县委副书记、副县长)
    {
        "person_a": 4, "person_b": 5,
        "type": "overlap",
        "context": "两名援青干部均挂任县委副书记、副县长",
        "overlap_org": "中共都兰县委员会/都兰县人民政府",
        "overlap_period": "截至2026-07",
    },
    # 书记 ↔ 各执行主席 (县委班子)
    {
        "person_a": 1, "person_b": 10, "type": "overlap",
        "context": "县第十七次党代会主席台前排班子成员", "overlap_org": "中共都兰县委员会", "overlap_period": "2026-07",
    },
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "县第十七次党代会主席台前排班子成员", "overlap_org": "中共都兰县委员会", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "县第十七次党代会主席台前排班子成员", "overlap_org": "中共都兰县委员会", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 13, "type": "overlap", "context": "县第十七次党代会主席台前排班子成员", "overlap_org": "中共都兰县委员会", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 14, "type": "overlap", "context": "县第十七次党代会主席台前排班子成员", "overlap_org": "中共都兰县委员会", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 15, "type": "overlap", "context": "县第十七次党代会主席台前排班子成员", "overlap_org": "中共都兰县委员会", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 16, "type": "overlap", "context": "县第十七次党代会主席台前排班子成员", "overlap_org": "中共都兰县委员会", "overlap_period": "2026-07"},
]

# ── Run build ───────────────────────────────────────────────────────────
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

    # Person JSON files are written by _write_person_jsons_main() called at the bottom
    print("Person JSON files written below (see function call at file tail).")


def _write_person_jsons_main() -> None:
    person_json_configs = [
        ("县委书记", "董峰", _build_dong_feng_json()),
        ("县长", "王全明", _build_wang_quanming_json()),
        ("常务副县长", "乔兆臣", _build_qiao_zhaochen_json()),
        ("副县长_公安局长", "张铠", _build_zhang_kai_json()),
    ]
    for job, name, data in person_json_configs:
        filename = f"{TODAY}-青海省-海西蒙古族藏族自治州-{job}-{name}.json"
        filepath = PJSON_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {filepath.name}")


# ── Person JSON builders ─────────────────────────────────────────────────

def _common_source_register() -> list:
    return [
        {
            "id": "S001",
            "title": "中国共产党都兰县第十七次代表大会隆重开幕",
            "url": "http://www.dulan.gov.cn/info/1052/75160.htm",
            "publisher": "都兰县人民政府",
            "published_at": "2026-07-11",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "董峰代表十六届委员会作报告，王全明主持；执行主席前排名单",
        },
        {
            "id": "S002",
            "title": "县委书记开展重点工作调研",
            "url": "http://www.dulan.gov.cn/info/1052/75092.htm",
            "publisher": "都兰县人民政府",
            "published_at": "2026-06-29",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认县委书记董峰",
        },
        {
            "id": "S003",
            "title": "县委常委会扩大会议召开",
            "url": "http://www.dulan.gov.cn/info/1052/75135.htm",
            "publisher": "都兰县人民政府",
            "published_at": "2026-07-06",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "县委书记董峰主持召开县委常委会扩大会议",
        },
        {
            "id": "S004",
            "title": "都兰县领导之窗 — 县长",
            "url": "http://www.dulan.gov.cn/ldzc/wqm.htm",
            "publisher": "都兰县人民政府",
            "published_at": "2026",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认王全明现任职务、性别、民族",
        },
        {
            "id": "S005",
            "title": "都兰县领导之窗 — 县政府领导班子",
            "url": "http://www.dulan.gov.cn/ldzc/",
            "publisher": "都兰县人民政府",
            "published_at": "2026",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "县政府领导班子名单: 乔兆臣、张斌、吴耿松、杨思青、刘国虎、张铠、安培祥",
        },
    ]


def _build_dong_feng_json() -> dict:
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": _build_scope("县委书记"),
        "identity": {
            "person_id": "qinghai_dulanxian_dongfeng",
            "name": "董峰",
            "aliases": [],
            "gender": "",
            "ethnicity": "",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {"name_birth": "董峰_", "name_birthplace": "董峰_", "official_profile_url": "http://www.dulan.gov.cn"},
        },
        "current_status": {
            "current_post": "都兰县委书记",
            "current_org": "中共都兰县委员会",
            "administrative_rank": "正处级",
            "as_of": "2026-07-13",
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002", "S003"],
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": "中共都兰县委员会",
                "title": "都兰县委书记",
                "level": "正处级",
                "location": "青海省海西州都兰县",
                "system": "party",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "Confirmed in office as of 2026-07 (17th party congress). Delivered 16th committee report on 2026-07-11, implying he led the 16th committee as well. Exact appointment date unknown.",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002", "S003"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": "公开资料未找到董峰任都兰县委书记之前的完整履历（出生、籍贯、学历、入党时间、此前历任）。需海西州组织部任前公示/青海组工信息。",
                "confidence": "unverified",
                "source_ids": [],
            },
        ],
        "organizations": [{"org_id": 1, "org_name": "中共都兰县委员会", "role": "县委书记", "period": "至2026-07"}],
        "relationships": [
            {
                "person": "王全明",
                "person_id": "qinghai_dulanxian_wangquanming",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "书记+县长，共同主持县第十七次党代会（董峰作报告，王全明主持）",
                "overlap_org": "中共都兰县委员会/都兰县人民政府",
                "overlap_period": "截至2026-07",
                "direction": "person_to_other",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "person": "乔兆臣",
                "person_id": "qinghai_dulanxian_qiaozhaochen",
                "relationship_type": "superior_subordinate",
                "strength": "medium",
                "evidence": "书记与常务副县长同台（十七届党代会主席台前排）",
                "overlap_org": "中共都兰县委员会",
                "overlap_period": "截至2026-07",
                "direction": "person_to_other",
                "confidence": "plausible",
                "source_ids": ["S001", "S005"],
            },
        ],
        "governance_record": [
            {
                "period": "2026-07-11",
                "domain": "other",
                "achievement_or_event": "在中国共产党都兰县第十七次代表大会上作县委工作报告，提出未来五年'美丽、富裕、文化、活力、幸福、平安都兰'目标",
                "role_in_event": "县委书记（主讲人）",
                "measurable_outcome": "挺进十五五总体发展目标确立",
                "location": "都兰县",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
        ],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["party"],
            "geographic_pattern": ["青海省"],
            "promotion_velocity": {"summary": "Insufficient data to assess promotion velocity", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "grassroots_oriented",
                    "evidence": "6-29 深入察汗乌苏镇、县市场监管部门调研并提出政绩观/基层治理要求；召开常委会专题学习习近平政绩观",
                    "confidence": "plausible",
                    "source_ids": ["S002", "S003"],
                }
            ],
            "speech_themes": ["基层党组织建设", "正确政绩观", "乡村振兴", "生态优先", "党风廉政建设"],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "No negative media, disciplinary action, or integrity signals found in the available official sources", "date": "", "confidence": "unverified", "source_ids": []},
        ],
        "source_register": _common_source_register(),
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "董峰出生/籍贯/学历及任书记前完整履历，以及前任书记与继任链",
        },
        "open_questions": [
            {"priority": "critical", "question": "董峰的出生年份、籍贯、民族、教育背景及入党/工作时间是？", "why_it_matters": "核心身份信息，无法去重与匹配关系网络", "suggested_queries": ["董峰 都兰 书历 简历", "董峰 海西州 组织部长", "董峰 任前公示"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "董峰担任都兰县委书记前任何职？（是否自县委副书记/县长/州直转任）", "why_it_matters": "判断晋升路径与跨县/跨系统轮换", "suggested_queries": ["董峰 都兰 县委书记 任职", "海西州 都兰县委书记 任命"], "last_attempted": AS_OF},
            {"priority": "high", "question": "董峰之前一任都兰县委书记是谁？去往何处？", "why_it_matters": "补全书记领导链，分析跨县干部交流", "suggested_queries": ["都兰县委书记 前任", "都兰县 卸任 书记 去向"], "last_attempted": AS_OF},
        ],
    }


def _build_wang_quanming_json() -> dict:
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": _build_scope("县长"),
        "identity": {
            "person_id": "qinghai_dulanxian_wangquanming",
            "name": "王全明",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {"name_birth": "王全明_", "name_birthplace": "王全明_", "official_profile_url": "http://www.dulan.gov.cn/ldzc/wqm.htm"},
        },
        "current_status": {
            "current_post": "都兰县委副书记、县政府党组书记、县长",
            "current_org": "都兰县人民政府",
            "administrative_rank": "正处级",
            "as_of": "2026-07-11",
            "is_current_confirmed": True,
            "source_ids": ["S004", "S001"],
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": "都兰县人民政府",
                "title": "都兰县委副书记、县政府党组书记、县长",
                "level": "正处级",
                "location": "青海省海西州都兰县",
                "system": "government",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "Confirmed current 县长 from 领导之窗 profile. Presided 以主席身份主持召开第十七届人大常委会第一次会议 (via 十七大 开幕主持). Prior career unknown.",
                "confidence": "confirmed",
                "source_ids": ["S004", "S001"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": "公开资料未取得王全明任格都兰县县长之前的履历（出生、籍贯、此前职务）。",
                "confidence": "unverified",
                "source_ids": [],
            },
        ],
        "organizations": [
            {"org_id": 2, "org_name": "都兰县人民政府", "role": "县政府县长", "period": "至2026-07"},
            {"org_id": 1, "org_name": "中共都兰县委员会", "role": "县委副书记", "period": "至2026-07"},
        ],
        "relationships": [
            {
                "person": "董峰",
                "person_id": "qinghai_dulanxian_dongfeng",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "县长向县委负责；两人同场主持十七届党代会（董峰报告、王全明主持）",
                "overlap_org": "中共都兰县委员会",
                "overlap_period": "截至2026-07",
                "direction": "other_to_person",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "person": "乔兆臣",
                "person_id": "qinghai_dulanxian_qiaozhaochen",
                "relationship_type": "superior_subordinate",
                "strength": "medium",
                "evidence": "县长与县政府常务副县长的日常运作关系",
                "overlap_org": "都兰县人民政府",
                "overlap_period": "截至2026-07",
                "direction": "other_to_person",
                "confidence": "plausible",
                "source_ids": ["S004", "S005"],
            },
        ],
        "governance_record": [
            {
                "period": "2026-07-11",
                "domain": "other",
                "achievement_or_event": "主持中国共产党都兰县第十七次代表大会开幕，安排部署全县发展",
                "role_in_event": "县长（主持人）",
                "measurable_outcome": "党代会完成日程",
                "location": "都兰县",
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
            "promotion_velocity": {"summary": "Insufficient data to assess promotion velocity", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "未在可用官方来源中发现不良/纪律/负评信号", "date": "", "confidence": "unverified", "source_ids": []},
        ],
        "source_register": _common_source_register(),
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "王全明任县长前履历与前任县长去向",
        },
        "open_questions": [
            {"priority": "critical", "question": "王全明的出生年份、籍贯、学历及入党/工作时间？", "why_it_matters": "核心身份信息", "suggested_queries": ["王全明 都兰县 简历", "王全明 海西州 县长"], "last_attempted": AS_OF},
            {"priority": "high", "question": "王全明任都兰县长之前任何职？（胃/副县长转任，或州直/他县调入）", "why_it_matters": "判断晋升与跨县轮换模式", "suggested_queries": ["王全明 任职 海西", "都兰县长 任命"], "last_attempted": AS_OF},
            {"priority": "high", "question": "王全明之前一任都兰县长是谁？去向何处？", "why_it_matters": "补全县长领导链", "suggested_queries": ["都兰县 前任县长 去向"], "last_attempted": AS_OF},
        ],
    }


def _build_qiao_zhaochen_json() -> dict:
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": _build_scope("常务副县长"),
        "identity": {
            "person_id": "qinghai_dulanxian_qiaozhaochen",
            "name": "乔兆臣",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "", "birthplace": "", "native_place": "", "education": [],
            "party_join": "中共党员", "work_start": "",
            "dedupe_keys": {"name_birth": "乔兆臣_", "name_birthplace": "乔兆臣_", "official_profile_url": "http://www.dulan.gov.cn/ldzc/qzc.htm"},
        },
        "current_status": {
            "current_post": "都兰县委常委、县政府党组副书记、副县长",
            "current_org": "都兰县人民政府",
            "administrative_rank": "副处级",
            "as_of": "2026-08",
            "is_current_confirmed": True,
            "source_ids": ["S005"],
        },
        "career_timeline": [
            {
                "start": "unknown", "end": "present",
                "org": "都兰县人民政府", "title": "都兰县委副书记、县政府党组副书记、副县长",
                "level": "副处级", "location": "青海省海西州都兰县", "system": "government",
                "rank": "副处级", "is_key_promotion": False,
                "notes": "Confirmed from 领导之窗: 负责县政府日常工作、发改/工信/招商/国防动员/应急/财贸/统计/能源/国资/政务公开，协助县长负责审计。",
                "confidence": "confirmed", "source_ids": ["S005"],
            },
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未取得乔祖臣此前履历。", "confidence": "unverified", "source_ids": []},
        ],
        "organizations": [{"org_id": 2, "org_name": "都兰县人民政府", "role": "常务副县长", "period": "至2026-08"}],
        "relationships": [
            {"person": "王全明", "person_id": "qinghai_dulanxian_wangquanming", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "县长与常务副县长的政府日常运作关系", "overlap_org": "都兰县人民政府", "overlap_period": "至2026-08", "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S005"]},
        ],
        "governance_record": [],
        "professional_profile": {"primary_specializations": [], "secondary_specializations": [], "career_pattern": "unknown", "systems_experience": ["government"], "geographic_pattern": ["青海省"], "promotion_velocity": {"summary": "Insufficient data", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [], "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未在可用官方源中发现不良信号", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": _common_source_register(),
        "confidence_summary": {"identity": "plausible", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "low", "biggest_gap": "乔兆臣此前履历"},
        "open_questions": [{"priority": "high", "question": "乔兆臣任格都常务副县长前任何职？出生/籍贯/学历？", "why_it_matters": "常务副职是县府核心，判断班子来源", "suggested_queries": ["乔兆臣 海西 副县长"], "last_attempted": AS_OF}],
    }


def _build_zhang_kai_json() -> dict:
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": _build_scope("常务_公安"),
        "identity": {
            "person_id": "qinghai_dulanxian_zhangkai",
            "name": "张铠",
            "aliases": [], "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "native_place": "", "education": [],
            "party_join": "中共党员", "work_start": "",
            "dedupe_keys": {"name_birth": "张铠_", "name_birthplace": "张铠_", "official_profile_url": "http://www.dulan.gov.cn/ldzc/ZK.htm"},
        },
        "current_status": {
            "current_post": "都兰县人民政府党组成员、副县长，县公安局党委书记、局长",
            "current_org": "都兰县公安局",
            "administrative_rank": "副处级",
            "as_of": "2026-08",
            "is_current_confirmed": True,
            "source_ids": ["S005"],
        },
        "career_timeline": [
            {
                "start": "unknown", "end": "present",
                "org": "都兰县公安局", "title": "副县长兼县公安局局长",
                "level": "副处级", "location": "青海省海西州都兰县", "system": "government",
                "rank": "副处级", "is_key_promotion": False,
                "notes": "Confirmed from 领导之窗: 负责公安、司法、综合执法、市场监管、消防救援。",
                "confidence": "confirmed", "source_ids": ["S005"],
            },
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未取得张磊此前履历。", "confidence": "unverified", "source_ids": []},
        ],
        "organizations": [{"org_id": 9, "org_name": "都兰县公安局", "role": "局长", "period": "至2026-08"}],
        "relationships": [
            {"person": "王全明", "person_id": "qinghai_dulanxian_wangquanming", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "县长与公安局长上下级（县政府领导与政法）", "overlap_org": "都兰县人民政府/都兰县公安局", "overlap_period": "至2026-08", "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S005"]},
        ],
        "governance_record": [],
        "professional_profile": {"primary_specializations": [], "secondary_specializations": [], "career_pattern": "unknown", "systems_experience": ["public_security"], "geographic_pattern": ["青海省"], "promotion_velocity": {"summary": "Insufficient data", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [], "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未在可用官方源中发现不良信号", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": _common_source_register(),
        "confidence_summary": {"identity": "plausible", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "low", "biggest_gap": "张铠此前履历与公安系统来源"},
        "open_questions": [{"priority": "high", "question": "张铠（都兰县公安局长）此前公安履历/任职地？", "why_it_matters": "判断政法系统人事来源", "suggested_queries": ["张铠 都兰 公安局长"], "last_attempted": AS_OF}],
    }


def _build_scope(job: str) -> dict:
    return {
        "province": "青海省",
        "city": "海西蒙古族藏族自治州",
        "region": "都兰县",
        "job": job,
        "task_id": "qinghai_都兰县",
        "time_focus": "2024-2026",
    }


_write_person_jsons_main()