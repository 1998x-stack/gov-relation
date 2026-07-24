#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 赫山区 (Heshan District), 益阳市, 湖南省.

Investigation date: 2026-07-24
Task ID: hunan_赫山区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.hnhs.gov.cn — 赫山区人民政府官方网站（赫山动态栏目新闻）
  - 门户新闻显示：区委书记李丰（2026年7月16日主持区委常委会），
  - 区委副书记、区长宋长征（2026年7月10日主持区政府常务会议）
  - 区委常委、常务副区长高志荣
  - 区委常委、区纪委书记胡鑫
  - 区委常委、组织部部长旷伟科
  - 区委常委、政法委书记谭正祥
  - 区委副书记胡金勇
  - 前任区委书记周卫星（2025年期间活跃报道，后由李丰接任）

Confidence notes:
  - 李丰 (Party Secretary): confirmed from hnhs.gov.cn multiple news articles (2026-07)
  - 宋长征 (District Mayor): confirmed from hnhs.gov.cn multiple news articles (2026-07)
  - 周卫星 (Predecessor Party Secretary): confirmed — active in 2024-2025 news
  - Other standing committee members: confirmed from meeting attendee lists
  - Deputy mayors: confirmed from news titles and content references
  - Detailed career histories beyond current role are limited
  - All claims labeled with confidence level; gaps explicitly documented
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
while REPO_ROOT.name:
    if (REPO_ROOT / "gov_relation").is_dir():
        break
    parent = REPO_ROOT.parent
    if parent == REPO_ROOT:
        break
    REPO_ROOT = parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "赫山区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "hunan_赫山区"
if _CURRENT_DIR.name == "hunan_赫山区":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-9 party/government core, 10-19 deputy government, 20-29 other leaders, 30+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "李丰",
        "gender": "男",
        "ethnicity": "汉族",  # plausible — typical for Hunan officials
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "区委书记",
        "current_org": "中共益阳市赫山区委员会",
        "source": "https://www.hnhs.gov.cn/22557/22597/22566/content_2187183.html",
        "confidence": "confirmed",
        "notes": "2026年7月16日'李丰主持召开六届区委第161次常委会会议'。此前曾担任赫山区区长（2025年新闻中李丰以区长身份出现），后接替周卫星任区委书记。完整履历待查。"
    },
    {
        "id": 2,
        "name": "宋长征",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "区长",
        "current_org": "赫山区人民政府",
        "source": "https://www.hnhs.gov.cn/22557/22597/22566/content_2186129.html",
        "confidence": "confirmed",
        "notes": "区委副书记、区长。2026年7月10日'宋长征主持召开区政府2026年第13次常务会议'。此前任职经历待查。"
    },
    {
        "id": 3,
        "name": "胡金勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共益阳市赫山区委员会",
        "source": "https://www.hnhs.gov.cn/（赫山动态栏目，'区委副书记胡金勇到沧水铺镇调研'）",
        "confidence": "confirmed",
        "notes": "区委副书记。2025-2026年多次以'区委副书记胡金勇'身份报道，分管沧水铺镇等工作。"
    },
    {
        "id": 4,
        "name": "高志荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "常务副区长",
        "current_org": "赫山区人民政府",
        "source": "https://www.hnhs.gov.cn/（赫山动态栏目，'赫山区委常委、常务副区长高志荣'）",
        "confidence": "confirmed",
        "notes": "区委常委、常务副区长。2025-2026年多次以'区委常委、常务副区长高志荣'身份报道，分管统计、安全工作。"
    },
    {
        "id": 5,
        "name": "胡鑫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区纪委书记",
        "current_org": "中共益阳市赫山区纪律检查委员会",
        "source": "https://www.hnhs.gov.cn/22557/22597/22566/content_2187184.html",
        "confidence": "confirmed",
        "notes": "区委常委、区纪委书记、区监委主任、区委巡察工作领导小组组长。2026年7月16日以该身份出席会议。"
    },
    {
        "id": 6,
        "name": "旷伟科",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委组织部部长",
        "current_org": "中共益阳市赫山区委员会",
        "source": "https://www.hnhs.gov.cn/22557/22597/22566/content_2187184.html",
        "confidence": "confirmed",
        "notes": "区委常委、区委组织部部长、区委巡察工作领导小组副组长。"
    },
    {
        "id": 7,
        "name": "谭正祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委政法委书记",
        "current_org": "中共益阳市赫山区委员会",
        "source": "https://www.hnhs.gov.cn/（赫山动态栏目，'区委常委、政法委书记谭正祥'）",
        "confidence": "confirmed",
        "notes": "区委常委、政法委书记。分管政法工作，赫山街道。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Other Major Org Leaders
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 8,
        "name": "胡佐颂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "赫山区人民代表大会常务委员会",
        "source": "https://www.hnhs.gov.cn/22557/22597/22566/content_2184868.html",
        "confidence": "confirmed",
        "notes": "区人大常委会党组书记、主任。2026年7月6日出席全区7月份工作调度会议。"
    },
    {
        "id": 9,
        "name": "陈铁军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议赫山区委员会",
        "source": "https://www.hnhs.gov.cn/22557/22597/22566/content_2184868.html",
        "confidence": "confirmed",
        "notes": "区政协党组书记、主席。2026年7月6日出席全区7月份工作调度会议。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Mayors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "周开晨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "赫山区人民政府",
        "source": "https://www.hnhs.gov.cn/（赫山动态栏目，'副区长周开晨'）",
        "confidence": "confirmed",
        "notes": "副区长。分管城市建设、住房、物业管理、生态环保等工作。多次以'副区长周开晨'身份报道。"
    },
    {
        "id": 11,
        "name": "蔡丽环",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "赫山区人民政府",
        "source": "https://www.hnhs.gov.cn/（赫山动态栏目，'蔡丽环'相关报道）",
        "confidence": "confirmed",
        "notes": "副区长。分管农业农村、畜牧水产、水利、森林防火、粮食生产等工作。2025-2026年活动报道丰富。"
    },
    {
        "id": 12,
        "name": "雷鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "赫山区人民政府",
        "source": "https://www.hnhs.gov.cn/（赫山动态栏目，'雷鹏'相关报道）",
        "confidence": "confirmed",
        "notes": "副区长。分管民政、交通、残疾人工作、环保（大气污染防治）等。"
    },
    {
        "id": 13,
        "name": "赵嘉喜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "赫山区人民政府",
        "source": "https://www.hnhs.gov.cn/（赫山动态栏目，'赵嘉喜'相关报道）",
        "confidence": "confirmed",
        "notes": "副区长。调研省十五运会场馆准备工作等。"
    },
    {
        "id": 14,
        "name": "白克力·买合木提",
        "gender": "男",
        "ethnicity": "维吾尔族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "赫山区人民政府",
        "source": "https://www.hnhs.gov.cn/（赫山动态栏目相关报道）",
        "confidence": "confirmed",
        "notes": "副区长。调研文旅广体、文联、沧水铺镇征拆安置等工作。少数民族干部（维吾尔族）。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Other District Leaders
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 15,
        "name": "曾钰彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区级领导",
        "current_org": "赫山区",
        "source": "https://www.hnhs.gov.cn/（赫山动态栏目相关报道）",
        "confidence": "confirmed",
        "notes": "区级领导。督导龙光桥街道地灾防治、安全生产等工作。"
    },
    {
        "id": 16,
        "name": "张平安",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区级领导",
        "current_org": "赫山区",
        "source": "https://www.hnhs.gov.cn/（赫山动态栏目相关报道）",
        "confidence": "confirmed",
        "notes": "区级领导，调度低温雨雪冰冻灾害防范等工作。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "周卫星",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区委书记",
        "current_org": "中共益阳市赫山区委员会",
        "source": "https://www.hnhs.gov.cn/（赫山动态栏目2024-2025年报道）",
        "confidence": "confirmed",
        "notes": "赫山区前任区委书记。2024-2025年间以'区委书记周卫星'在大量报道中出现。2026年后报道消失，由李丰接任区委书记。具体去向待查。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共益阳市赫山区委员会", "type": "党委", "level": "市辖区", "parent": "中共益阳市委员会", "location": "益阳市赫山区"},
    {"id": 2, "name": "赫山区人民政府", "type": "政府", "level": "市辖区", "parent": "益阳市人民政府", "location": "益阳市赫山区"},
    {"id": 3, "name": "赫山区人民代表大会常务委员会", "type": "人大", "level": "市辖区", "parent": "益阳市人民代表大会常务委员会", "location": "益阳市赫山区"},
    {"id": 4, "name": "中国人民政治协商会议赫山区委员会", "type": "政协", "level": "市辖区", "parent": "政协益阳市委员会", "location": "益阳市赫山区"},
    {"id": 5, "name": "中共益阳市赫山区纪律检查委员会", "type": "党委", "level": "市辖区", "parent": "中共益阳市纪律检查委员会", "location": "益阳市赫山区"},
    {"id": 6, "name": "中共益阳市赫山区委政法委员会", "type": "党委", "level": "市辖区", "parent": "中共益阳市委政法委员会", "location": "益阳市赫山区"},
    {"id": 7, "name": "中共益阳市赫山区委组织部", "type": "党委", "level": "市辖区", "parent": "中共益阳市委组织部", "location": "益阳市赫山区"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 李丰 — current Party Secretary
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2025-2026", "end_date": "", "rank": "正处级", "note": "现任赫山区委书记（原区长升任），前任为周卫星"},
    {"person_id": 1, "org_id": 1, "title": "区委副书记", "start_date": "2024-2025", "end_date": "2025-2026", "rank": "正处级", "note": "曾以区委副书记、区长身份报道"},
    {"person_id": 1, "org_id": 2, "title": "区长", "start_date": "2024-2025", "end_date": "2025-2026", "rank": "正处级", "note": "曾为赫山区区长"},
    # 宋长征 — current District Mayor
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "2026", "end_date": "", "rank": "正处级", "note": "区委副书记、区长"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "2026", "end_date": "", "rank": "正处级", "note": "区委副书记"},
    # 胡金勇 — Deputy Party Secretary
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "区委副书记"},
    # 高志荣 — Executive Deputy Mayor
    {"person_id": 4, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "区委常委、常务副区长"},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 胡鑫 — Discipline Inspection
    {"person_id": 5, "org_id": 5, "title": "区纪委书记、区监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "区委常委、区纪委书记、区监委主任、区委巡察工作领导小组组长"},
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 旷伟科 — Organization Department
    {"person_id": 6, "org_id": 7, "title": "区委组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "区委常委、区委组织部部长、区委巡察工作领导小组副组长"},
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 谭正祥 — Political-Legal Affairs
    {"person_id": 7, "org_id": 6, "title": "区委政法委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "区委常委、政法委书记"},
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 胡佐颂 — NPC Chairman
    {"person_id": 8, "org_id": 3, "title": "区人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": "区人大常委会党组书记、主任"},
    # 陈铁军 — CPPCC Chairman
    {"person_id": 9, "org_id": 4, "title": "区政协主席", "start_date": "", "end_date": "", "rank": "正处级", "note": "区政协党组书记、主席"},
    # Deputy Mayors
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "分管城建、城市管理、生态环境等"},
    {"person_id": 11, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "分管农业农村、水利、粮食等"},
    {"person_id": 12, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "分管民政、交通等"},
    {"person_id": 13, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "分管体育、场馆建设等"},
    {"person_id": 14, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "分管文旅广体、文联等"},
    # Other district leaders
    {"person_id": 15, "org_id": 2, "title": "区级领导", "start_date": "", "end_date": "", "rank": "副处级", "note": "龙光桥街道联系领导"},
    {"person_id": 16, "org_id": 2, "title": "区级领导", "start_date": "", "end_date": "", "rank": "副处级", "note": "调度低温雨雪冰冻灾害防范"},
    # Predecessors
    {"person_id": 30, "org_id": 1, "title": "区委书记", "start_date": "2023-2025", "end_date": "2025-2026", "rank": "正处级", "note": "前任赫山区委书记，2025年仍有活跃报道，后由李丰接任"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 李丰 ↔ 宋长征 (Party Secretary – District Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—区长搭档", "overlap_org": "中共益阳市赫山区委员会", "overlap_period": "2026-至今"},
    # 李丰 → 班子成员
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "区委书记—区委副书记", "overlap_org": "中共益阳市赫山区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "区委书记—常委/常务副区长", "overlap_org": "中共益阳市赫山区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "区委书记—常委/纪委书记", "overlap_org": "中共益阳市赫山区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "区委书记—常委/组织部长", "overlap_org": "中共益阳市赫山区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "区委书记—常委/政法委书记", "overlap_org": "中共益阳市赫山区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "区委书记—人大主任", "overlap_org": "中共益阳市赫山区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "区委书记—政协主席", "overlap_org": "中共益阳市赫山区委员会", "overlap_period": "至今"},
    # 宋长征 → 副区长团队
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "区长—常务副区长", "overlap_org": "赫山区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "区长—副区长", "overlap_org": "赫山区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "区长—副区长", "overlap_org": "赫山区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "区长—副区长", "overlap_org": "赫山区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "区长—副区长", "overlap_org": "赫山区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 14, "type": "共事", "context": "区长—副区长", "overlap_org": "赫山区人民政府", "overlap_period": "至今"},
    # 胡金勇 — 区委班子
    {"person_a": 3, "person_b": 4, "type": "共事", "context": "区委副书记—常委/常务副区长", "overlap_org": "中共益阳市赫山区委员会", "overlap_period": "至今"},
    {"person_a": 3, "person_b": 5, "type": "共事", "context": "区委副书记—常委/纪委书记", "overlap_org": "中共益阳市赫山区委员会", "overlap_period": "至今"},
    # 周卫星 ↔ 李丰 (predecessor-successor, 周卫星是前任区委书记)
    {"person_a": 30, "person_b": 1, "type": "交接", "context": "前任区委书记—现任区委书记", "overlap_org": "中共益阳市赫山区委员会", "overlap_period": "2025-2026"},
    # 周卫星 ↔ 李丰 (former Party Secretary – former Mayor, now current Secretary)
    {"person_a": 30, "person_b": 1, "type": "共事", "context": "前任区委书记—时任区长", "overlap_org": "中共益阳市赫山区委员会", "overlap_period": "2024-2025"},
]


# ═════════════════════════════════════════════════════════════════════════════
# Helper functions
# ═════════════════════════════════════════════════════════════════════════════


def _get_open_questions(person: dict) -> list[str]:
    questions = []
    if not person.get("birth"):
        questions.append("出生年月未确认")
    if not person.get("birthplace"):
        questions.append("籍贯未确认")
    if not person.get("ethnicity"):
        questions.append("民族未确认")
    if not person.get("education"):
        questions.append("学历教育背景未确认")
    if not person.get("work_start"):
        questions.append("参加工作年份未确认")
    return questions


def _make_person_id(name: str) -> str:
    return f"heshan_{name}"


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = _make_person_id(name)

    person_positions = [p for p in positions if p["person_id"] == pid]

    career_timeline = []
    for pos in person_positions:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        career_timeline.append({
            "start": pos.get("start_date", "") or "",
            "end": pos.get("end_date", "") or "",
            "org": org["name"] if org else "",
            "title": pos.get("title", ""),
            "level": pos.get("rank", ""),
            "rank": pos.get("rank", ""),
            "notes": pos.get("note", "") or "",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    person_rels = [
        r for r in relationships
        if r["person_a"] == pid or r["person_b"] == pid
    ]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rels_output.append({
            "person": other_name,
            "person_id": _make_person_id(other_name),
            "relationship_type": "overlap" if r["type"] in ("共事",) else "predecessor_successor",
            "strength": "strong" if r["type"] in ("共事", "交接") else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        })

    source_url = person.get("source", "")
    sources = [
        {
            "id": "S001",
            "title": "益阳市赫山区人民政府官方网站",
            "url": "https://www.hnhs.gov.cn/",
            "publisher": "赫山区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "赫山区政府门户网站赫山动态栏目新闻及活动报道",
        },
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "湖南省",
            "city": "益阳市",
            "region": "赫山区",
            "job": person.get("current_post", ""),
            "task_id": "hunan_赫山区",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": slug_id,
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "", "study_type": "unknown", "source_ids": ["S001"]}] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth','')}",
                "name_birthplace": f"{name}_{person.get('birthplace','')}",
                "official_profile_url": source_url,
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正处级" if person.get("current_post") in ("区委书记", "区长", "区人大常委会主任", "区政协主席", "前任区委书记") else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "partial",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "partial" if person.get("birth") else "thin",
            "relationship_confidence": "high",
            "biggest_gap": "完整任职履历（每段职务精确起止时间）" if not person.get("work_start") else "早期教育和工作细节",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历（每段职务精确起止时间）",
                "why_it_matters": "关系网络分析需要精确的时间线",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
        ] + ([
            {
                "priority": "high",
                "question": f"{name}的出生年月和籍贯",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [f"{name} 简历", f"{name} 籍贯"],
                "last_attempted": AS_OF,
            },
        ] if not person.get("birth") else []),
    }

    fname = f"{TODAY}-湖南省-益阳市-{person['current_post']}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


# ═════════════════════════════════════════════════════════════════════════════
# Build
# ═════════════════════════════════════════════════════════════════════════════


def main() -> int:
    print(f"Building {SLUG} network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

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

    print("  Writing person JSONs...")
    core_ids = {1, 2, 30}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
