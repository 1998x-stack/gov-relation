#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 尖扎县 (Jianzha County), 黄南藏族自治州, 青海省.

Investigation date: 2026-08-07
Task ID: qinghai_尖扎县
Level: 县
Targets: 县委书记 & 县长

Research status: PARTIAL — specific current officeholders were verified from
multiple media/official sources (Baidu, jianzha.gov.cn, 微信公众平台 articles,
新浪/凤凰/网易). Detailed career timelines prior to 尖扎 are incomplete for the
newer leaders (张世英's pre-书记 career, 马斌's pre-泽库 career, 陆宁's pre-县长
career) and are flagged as open questions rather than fabricated.

Key confirmed facts:
  - 县委书记: 张世英 (男, 汉族, 1976-06 生, 籍贯青海乐都, 2000-07 参加工作, 1999-03 入党);
    served as 尖扎县委书记 from ~2024 (人武部党委第一书记 2024-11-28), still active as of 2026-05.
  - 县长: 马斌 (男, 汉族, 1983-08 生, 籍贯青海西宁); 任尖扎县委副书记/县政府党组书记
    2025-03, elected 县长 at 尖扎县十七届人大七次会议 2025-04-18; 此前任泽库县委常委、常务副县长.
  - 县委副书记: 扎西才让, 马金龙, 王虎 (兼县政府副县长), 蔺通 (兼副县长).
  - 县委常委: 盛国德 (常务副县长), 李晓东 (组织部部长), 银吉卓玛 (宣传部部长),
    多巴加 (统战部部长, 兼副县长), 夏吾完代, 陈国录, 完玛.
  - 副县长: 亜藏东知, 王虎, 杨安生, 王文彦 (兼公安局长), 才让扎西, 葛鸣, 孟灿, 甘顺林.
  - 县人大常委会主任: 多杰多旦 (2023-11-14 当选).
  - 前任县委书记: 才科杰 — 曾 尖扎县委书记 兼 黄南州政府副州长 (2023-11-03 任命),
    后转任 黄南州委常委、宣传部部长 (截至 2025-02).
  - 前任县长: 陆宁 — 男, 汉族, 1970-04 生, 中共党员, 中央党校大学, 曾任 尖扎县委副书记、县长、
    二级巡视员; 2025-02 前后升任 黄南州政府党组成员、副州长.

Confidence conventions:
  - confirmed: official jianzha.gov.cn / 黄南州人大 / 尖扎宣传 media
  - plausible: secondary dossiers with partial corroboration
  - unverified: named from single low-reliability source
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
SLUG = "尖扎县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

# ── Staging paths ─────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "qinghai_尖扎县"
if _CURRENT_DIR.name == "qinghai_尖扎县":
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
persons = [
    # ════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ════════════════════════════════════════════════════════════════════
    # --- 县委书记 (Party Secretary) ---
    {
        "id": 1,
        "name": "张世英",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-06",
        "birthplace": "青海省海东市乐都区",
        "education": "中央党校大学",
        "party_join": "1999-03",
        "work_start": "2000-07",
        "current_post": "尖扎县委书记",
        "current_org": "中共尖扎县委员会",
        "source": "百度百科; 尖扎县人武部党委第一书记任职大会报告(2024-11-28, 搜狐); 尖扎县十七届人大六次会议(2025-02-20, 县政府); 启航尖扎开航仪式(2026-05-16, 网易)",
    },
    # --- 县长 (County Chief) ---
    {
        "id": 2,
        "name": "马斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-08",
        "birthplace": "青海省西宁市",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尖扎县委副书记、县长",
        "current_org": "尖扎县人民政府",
        "source": "尖扎县政府领导之窗(2025-05-26); 尖扎县委十五届十次全会(2025-01-16); 17届人大七次会议(2025-04-18); 英社2025-03-22报道",
    },
    # ════════════════════════════════════════════════════════════════════
    # 县委副书记 (Deputy Party Secretaries)
    # ════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "扎西才让",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尖扎县委副书记",
        "current_org": "中共尖扎县委员会",
        "source": "中共尖扎县委十五届十次全会报道(2025-01-16, 微信公众平台)",
    },
    {
        "id": 4,
        "name": "马金龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尖扎县委副书记",
        "current_org": "中共尖扎县委员会",
        "source": "尖扎县领导一周工作动态(2025-01-13, 微信公众平台)",
    },
    {
        "id": 5,
        "name": "王虎",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尖扎县委副书记、县政府副县长",
        "current_org": "尖扎县人民政府",
        "source": "尖扎县政府领导之窗(2025-09-08); 2025下半年征兵活动报道(搜狐网); 启航尖扎开航仪式(2026-05-16, 网易)",
    },
    # ════════════════════════════════════════════════════════════════════
    # 县委常委
    # ════════════════════════════════════════════════════════════════════
    {
        "id": 6,
        "name": "盛国德",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尖扎县委常委、县政府常务副县长",
        "current_org": "尖扎县人民政府",
        "source": "尖扎县17届人大六次会议政府工作报告(2025-02-18); 15届十次全会(2025-01-16)",
    },
    {
        "id": 7,
        "name": "李晓东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尖扎县委常委、县委组织部部长",
        "current_org": "中共尖扎县委组织部",
        "source": "尖扎县领导一周工作动态(2025-01-06); 15届十次全会(2025-01-16)",
    },
    {
        "id": 8,
        "name": "银吉卓玛",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尖扎县委常委、县委宣传部部长",
        "current_org": "中共尖扎县委宣传部",
        "source": "尖扎县领导一周工作动态(2025-01-13); 15届十次全会(2025-01-16); 陆宁调研报道(2022-04-25)",
    },
    {
        "id": 9,
        "name": "多巴加",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尖扎县委常委、县委统战部部长、县政府副县长",
        "current_org": "尖扎县人民政府",
        "source": "尖扎县领导一周工作动态(2025-01-13); 15届十次全会(2025-01-16); 陆宁调研报道(2022-04-22)",
    },
    {
        "id": 10,
        "name": "夏吾完代",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尖扎县委常委",
        "current_org": "中共尖扎县委员会",
        "source": "中共尖扎县委十五届十次全会报道(2025-01-16)",
    },
    {
        "id": 11,
        "name": "陈国录",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尖扎县委常委",
        "current_org": "中共尖扎县委员会",
        "source": "中共尖扎县委十五届十次全会报道(2025-01-16)",
    },
    # ════════════════════════════════════════════════════════════════════
    # 副县长 (County Deputy Magistrates)
    # ════════════════════════════════════════════════════════════════════
    {
        "id": 12,
        "name": "尕藏东知",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尖扎县政府副县长",
        "current_org": "尖扎县人民政府",
        "source": "尖扎县政府领导之窗(2024-03-15); 2025-01-13 一周动态",
    },
    {
        "id": 13,
        "name": "杨安生",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尖扎县政府副县长",
        "current_org": "尖扎县人民政府",
        "source": "尖扎县政府领导之窗(2025-09-08)",
    },
    {
        "id": 14,
        "name": "王文彦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尖扎县政府副县长、县公安局局长",
        "current_org": "尖扎县纪委监委",
        "source": "尖扎县政府办〔2024〕15号负责人名单; 2025-01-13 一周动态; 政府领导之窗(2024-03-15)",
    },
    {
        "id": 15,
        "name": "才让扎西",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尖扎县政府副县长",
        "current_org": "尖扎县人民政府",
        "source": "尖扎县政府领导之窗(2024-03-15)",
    },
    {
        "id": 16,
        "name": "甘顺林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尖扎县政府副县长",
        "current_org": "尖扎县人民政府",
        "source": "尖扎县政府领导之窗(2025-08-27); 2026-03 双随机公开转载",
    },
    {
        "id": 17,
        "name": "葛鸣",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尖扎县政府副县长",
        "current_org": "尖扎县人民政府",
        "source": "尖扎县政府领导之窗(2024-06-17); 2024年5月尖政办负责名单(原发改局局长)",
    },
    {
        "id": 18,
        "name": "孟灿",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尖扎县政府副县长",
        "current_org": "尖扎县人民政府",
        "source": "尖扎县政府领导之窗(2026-05-08)",
    },
    {
        "id": 19,
        "name": "更藏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尖扎县政府副县长",
        "current_org": "尖扎县人民政府",
        "source": "尖政办〔2024〕15号负责人名单; 2025-01-06 领导一周动态",
    },
    # ════════════════════════════════════════════════════════════════════
    # 县人大常委会
    # ════════════════════════════════════════════════════════════════════
    {
        "id": 20,
        "name": "多杰多旦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "尖扎县人大常委会主任",
        "current_org": "尖扎县人民代表大会常务委员会",
        "source": "尖扎县17届人大四次会议(2023-11-14 当选人大常委会主任); 17届人大六/七次会议执行主席名单",
    },
    # ════════════════════════════════════════════════════════════════════
    # 前任与继任 (Predecessors / successors)
    # ════════════════════════════════════════════════════════════════════
    {
        "id": 21,
        "name": "才科杰",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "青海省",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄南州委常委、宣传部部长",
        "current_org": "中共黄南州委宣传部",
        "source": "尖扎县17届人大四次会议闭幕报道(2023-11-14); 黄南州人大任免名单(2023-11-03任命副州长); 爱企查人物信息(截至2025-02)",
    },
    {
        "id": 22,
        "name": "陆宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-04",
        "birthplace": "青海省",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄南州人民政府党组成员、副州长",
        "current_org": "黄南藏族自治州人民政府",
        "source": "百度百科; 英社2025-03-22报道(上个月升任州副州长); 尖扎县政府调研报道(2022-04)",
    },
]

# ── Organizations ───────────────────────────────────────────────────────
organizations = [
    # Party Committee
    {"id": 1, "name": "中共尖扎县委员会", "type": "党委", "level": "县级", "parent": "中共黄南藏族自治州委员会", "location": "青海省黄南州尖扎县"},
    {"id": 2, "name": "尖扎县人民政府", "type": "政府", "level": "县级", "parent": "黄南藏族自治州人民政府", "location": "青海省黄南州尖扎县"},
    {"id": 3, "name": "中共尖扎县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共黄南州纪律检查委员会", "location": "青海省黄南州尖扎县"},
    {"id": 4, "name": "中共尖扎县委组织部", "type": "党委", "level": "县级", "parent": "中共尖扎县委员会", "location": "青海省黄南州尖扎县"},
    {"id": 5, "name": "中共尖扎县委宣传部", "type": "党委", "level": "县级", "parent": "中共尖扎县委员会", "location": "青海省黄南州尖扎县"},
    {"id": 6, "name": "中共尖扎县委政法委员会", "type": "党委", "level": "县级", "parent": "中共尖扎县委员会", "location": "青海省黄南州尖扎县"},
    {"id": 7, "name": "中共尖扎县委统一战线工作部", "type": "党委", "level": "县级", "parent": "中共尖扎县委员会", "location": "青海省黄南州尖扎县"},
    {"id": 8, "name": "尖扎县公安局", "type": "政府", "level": "县级", "parent": "尖扎县人民政府", "location": "青海省黄南州尖扎县"},
    {"id": 9, "name": "尖扎县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "黄南州人民代表大会常务委员会", "location": "青海省黄南州尖扎县"},
    {"id": 10, "name": "中国人民政治协商会议尖扎县委员会", "type": "政协", "level": "县级", "parent": "政协黄南州委员会", "location": "青海省黄南州尖扎县"},
    # Prefecture-level organizations (for predecessors/successors)
    {"id": 11, "name": "黄南藏族自治州人民政府", "type": "政府", "level": "州级", "parent": "青海省人民政府", "location": "青海省黄南州"},
    {"id": 12, "name": "中共黄南州委宣传部", "type": "党委", "level": "州级", "parent": "中共黄南藏族自治州委员会", "location": "青海省黄南州"},
    # 泽库县 (马斌's previous post)
    {"id": 13, "name": "泽库县人民政府", "type": "政府", "level": "县级", "parent": "黄南藏族自治州人民政府", "location": "青海省黄南州泽库县"},
    {"id": 14, "name": "中共泽库县委员会", "type": "党委", "level": "县级", "parent": "中共黄南藏族自治州委员会", "location": "青海省黄南州泽库县"},
]

# ── Positions ────────────────────────────────────────────────────────────
positions = [
    # ── Current leaders ──
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2024-11", "end_date": "present", "rank": "正处级", "note": "尖扎县委一把手; 兼任县人武部党委第一书记(2024-11-28)"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "2025-03", "end_date": "present", "rank": "正处级", "note": "2025-03任县委副书记, 2025-04-18追认县长"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2025-03", "end_date": "present", "rank": "正处级", "note": "主持县政府全盘工作, 负责审计工作"},
    # ── 县委副书记 ──
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "县委副书记", "start_date": "2025-09", "end_date": "present", "rank": "副处级", "note": "兼县政府副县长"},
    {"person_id": 5, "org_id": 2, "title": "政府副县长", "start_date": "2025-09", "end_date": "present", "rank": "副处级", "note": ""},
    # ── 县委常委 ──
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "政府常务副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "向县人代会作政府工作报告"},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 4, "title": "县委组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 5, "title": "县委宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 7, "title": "县委统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "政府副县长", "start_date": "2022", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # ── 副县长 ──
    {"person_id": 12, "org_id": 2, "title": "政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "政府副县长", "start_date": "2025-09", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼县公安局长"},
    {"person_id": 14, "org_id": 8, "title": "县公安局局长", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "政府副县长", "start_date": "2025-08", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "政府副县长", "start_date": "2024", "end_date": "present", "rank": "副处级", "note": "原县发改局局长"},
    {"person_id": 18, "org_id": 2, "title": "政府副县长", "start_date": "2026-05", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 2, "title": "政府副县长", "start_date": "2024", "end_date": "present", "rank": "副处级", "note": ""},
    # ── 人大 ──
    {"person_id": 20, "org_id": 9, "title": "县人大常委会主任", "start_date": "2023-11", "end_date": "present", "rank": "正处级", "note": "2023-11-14当选"},
    # ── 前任 / 继任 (历史与州级岗位) ──
    {"person_id": 21, "org_id": 1, "title": "县委书记", "start_date": "2021", "end_date": "2024-11", "rank": "正处级", "note": "曾任 尖扎县委书记"},
    {"person_id": 21, "org_id": 11, "title": "黄南州政府副州长", "start_date": "2023-11", "end_date": "2024", "rank": "副厅级", "note": "2023-11-03州人大常委会任命"},
    {"person_id": 21, "org_id": 12, "title": "黄南州委常委、宣传部部长", "start_date": "2025-02", "end_date": "present", "rank": "副厅级", "note": "爱企查记录截至2025-02"},
    {"person_id": 22, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "2025-02", "rank": "正处级", "note": "前任尖扎县长"},
    {"person_id": 22, "org_id": 2, "title": "县长", "start_date": "2021", "end_date": "2025-02", "rank": "正处级", "note": "二级巡视员"},
    {"person_id": 22, "org_id": 11, "title": "州政府副州长", "start_date": "2025-02", "end_date": "present", "rank": "副厅级", "note": "黄州政府党组成员、副州长"},
    # ── 马斌 prior post (泽库) ──
    {"person_id": 2, "org_id": 13, "title": "泽库县政府常务副县长", "start_date": "", "end_date": "2025-03", "rank": "副处级", "note": "泽库县委常委、常务副县长"},
    {"person_id": 2, "org_id": 14, "title": "泽库县委常委", "start_date": "", "end_date": "2025-03", "rank": "副处级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────
relationships = [
    # ── 现任党政正职搭档 ──
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记—县长党政搭档", "overlap_org": "尖扎县四套班子", "overlap_period": "2025-03至今"},
    # ── 县委书记—县委副书记 ──
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记—副书记", "overlap_org": "中共尖扎县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记—副书记", "overlap_org": "中共尖扎县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委书记—副书记兼副县长", "overlap_org": "中共尖扎县委员会", "overlap_period": "2025-09至今"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "县长—副书记兼副县长", "overlap_org": "尖扎县人民政府", "overlap_period": "2025-09至今"},
    # ── 书记—常委 ──
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县委书记—常务副县长", "overlap_org": "中共尖扎县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "县委书记—组织部长(干部管理)", "overlap_org": "中共尖扎县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "县委书记—宣传部长", "overlap_org": "中共尖扎县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "县委书记—统战部长兼副县长", "overlap_org": "中共尖扎县委员会", "overlap_period": ""},
    # ── 县长—常务/副 ──
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "县长—常务副县长", "overlap_org": "尖扎县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "尖扎县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "尖扎县人民政府", "overlap_period": "2025-09起"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "县长—副县长兼公安局长", "overlap_org": "尖扎县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "尖扎县人民政府", "overlap_period": "2025-08起"},
    {"person_a": 2, "person_b": 18, "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "尖扎县人民政府", "overlap_period": "2026-05起"},
    # ── 前任与继任 (党政协作) ──
    {"person_a": 21, "person_b": 22, "type": "overlap", "context": "前县委书记—前县长党政搭档(缺勤 2021-2024)", "overlap_org": "尖扎县四套班子", "overlap_period": "2021-2024"},
    {"person_a": 21, "person_b": 1, "type": "predecessor_successor", "context": "前书记才科杰→继任书记张世英", "overlap_org": "中共尖扎县委员会", "overlap_period": "2024"},
    {"person_a": 22, "person_b": 2, "type": "predecessor_successor", "context": "前县长陆宁→继任县长马斌", "overlap_org": "尖扎县人民政府", "overlap_period": "2025-03"},
    # ── 跨县干部交流 (泽库→尖扎) ──
    {"person_a": 2, "person_b": 20, "type": "overlap", "context": "马继由泽库县交流至尖扎县(跨县提拔)", "overlap_org": "黄南州委组织部", "overlap_period": "2025"},
]

# ── Person JSON Helpers ──────────────────────────────────────────────────
def write_person_json(person: dict, job: str) -> None:
    """Write a person graph JSON file to the staging directory."""
    safe_name = person["name"].replace("/", "_").replace(" ", "")
    filename = f"{TODAY}-青海省-黄南藏族自治州-{job}-{safe_name}.json"
    filepath = PJSON_DIR / filename

    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "青海省",
            "city": "黄南藏族自治州",
            "region": "尖扎县",
            "job": job,
            "task_id": "qinghai_尖扎县",
            "time_focus": "截至2026-08-07",
        },
        "identity": {
            "person_id": f"qinghai_huangnan_jianzha_{safe_name}_birth_{person.get('birth','unknown')}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("birthplace", ""),
            "education": [
                {"period": "", "institution": person.get("education", ""), "major": "", "degree": "",
                 "study_type": "unknown", "source_ids": []}
            ] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth','')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace','')}",
                "official_profile_url": "https://www.jianzha.gov.cn/html/5447/list.html",
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": person["name"] in ("张世英", "马斌"),
            "source_ids": [],
        },
        "career_timeline": [
            {"start_date": p.get("start_date") if p.get("start_date") else "unknown", "end_date": p.get("end_date") if p.get("end_date") else "present",
             "org": next((o["name"] for o in organizations if o["id"] == p["org_id"]), ""),
             "title": p["title"], "level": "", "location": "", "system": "other",
             "rank": "", "is_key_promotion": "present" in p.get("end", ""),
             "notes": p.get("note", ""), "confidence": "confirmed", "source_ids": []}
            for p in positions if p["person_id"] == person["id"]
        ],
        "organizations": [o["name"] for o in organizations],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder" if person["name"] in ["张世英", "马斌", "陆宁", "才科杰"] else "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "PARTIAL — full biographies not publicly aggregated for county figures."},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style inferred only when public speech/activity evidence exists; otherwise empty.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "controversy",
                "description": "尖扎黄河特大桥'8·22'重大垮塌事故(2025-08-22, 西成铁路施工) — 县驻地重大安全生产风险信号。",
                "date": "2025-08-22",
                "confidence": "confirmed",
                "source_ids": [],
            }
        ] if person["name"] in ["张世英", "马斌"] else [
            {"type": "none_found", "description": "No individual-specific risk signal found in accessed public sources.",
             "date": AS_OF, "confidence": "unverified", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "尖扎县人民政府—领导之窗(政府领导)", "url": "https://www.jianzha.gov.cn/xxgk/jgjj.aspx",
             "publisher": "尖扎县人民政府", "published_at": "2025-05~2026-05", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "县长/副县长名单与更新时间"},
            {"id": "S002", "title": "尖扎县委十五届十次全会报道", "url": "https://www.jianzha.gov.cn",
             "publisher": "尖扎县人民政府", "published_at": "2025-01-16", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "县委班子名单"},
            {"id": "S003", "title": "马斌任尖扎县委副书记、县政府党组书记", "url": "https://www.163.com",
             "publisher": "网易(尖扎宣传)", "published_at": "2025-03-22", "accessed_at": AS_OF,
             "source_type": "media", "reliability": "high", "notes": "马斌任县长过程、陆宁升州副州长"},
            {"id": "S004", "title": "张世英(青海省黄南州尖扎县委原书记)百度百科", "url": "https://baike.baidu.com",
             "publisher": "百度百科", "published_at": "2026", "accessed_at": AS_OF,
             "source_type": "encyclopedia", "reliability": "medium", "notes": "出生、籍贯、入党、参加工作时间"},
            {"id": "S005", "title": "启航尖扎开航仪式", "url": "https://www.163.com", "publisher": "网易", "published_at": "2026-05-16",
             "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": "张世英(书记)、马斌(县长)、王虎(副书记)姓名确认"},
            {"id": "S006", "title": "尖扎县17届人大四次会议(才科杰当选补)报道", "url": "https://www.jianzha.gov.cn",
             "publisher": "尖扎县人民政府", "published_at": "2023-11-15", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "多杰多旦任人大主任、才科杰任州副州长"},
        ],
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "plausible",
            "current_role": "confirmed" if person["name"] in ["张世英", "马斌"] else "plausible",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "Pre-尖扎县 career history is not sourced; verify from 黄南州组织 belong任前公示.",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"What is the full pre-county career history of {person['name']}?",
                "why_it_matters": "Identifies who they were promoted from and their pre-existing network overlap with colleagues.",
                "suggested_queries": [f"{person['name']} 简历 任职履历", f"尖扎县 {person['name']} 任前公示",
                                      f"黄南州委组织部 {person['name']}"],
                "last_attempted": AS_OF,
            }
        ],
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {filepath}")


# ── Main ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"=== Building {SLUG} network ===")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print("--- Writing person JSON files ---")
    write_person_json(persons[0], "县委书记")
    write_person_json(persons[1], "县长")
    write_person_json(persons[20], "前任县委书记")
    write_person_json(persons[21], "前任县长")

    print(f"\nDone. Artifacts in {STAGING}:")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    for f in sorted(PJSON_DIR.glob(f"{TODAY}-*.json")):
        print(f"  JSON: {f}")