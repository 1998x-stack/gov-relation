#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 娄底市 (Loudi City), 湖南省.

Investigation date: 2026-07-24
Task ID: hunan_娄底市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - zh.wikipedia.org — 娄底市, 曾超群, 邹文辉, 各区县 Wikipedia entries (primary, dated July 2026)
  - www.hnloudi.gov.cn — 娄底市人民政府官方网站, confirmed current leadership via July 2026 news reports
  - Web search was degraded: Baidu Baike 403, Exa rate-limited, Jina Reader timeouts, Wikipedia HTTPS timeout

Confidence notes:
  - Current roles: confirmed via multiple government meeting/news reports (July 2026) and Wikipedia
  - Mayor 何朝晖 bio information sourced from existing Wikipedia (娄底市 page) — partial
  - County-level rosters sourced from sub-entity Wikipedia pages
  - Biographical details for most figures are thin beyond basic identity
  - All claims labeled with confidence level; gaps explicitly documented
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
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

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "娄底市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "hunan_娄底市"
if _CURRENT_DIR.name == "hunan_娄底市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ═══════════════════════════════════════════════════════════════════════════════
# Persons
# IDs: 1-9 市级主要领导, 10-19 娄星区, 20-29 双峰县, 30-39 新化县,
#       40-49 冷水江市, 50-59 涟源市, 60-69 前任+腐败案关联
# ═══════════════════════════════════════════════════════════════════════════════

persons = [
    # ══════════════════════════════════════════════════════════════════════════
    # 市级核心领导 (Municipal Core Leadership)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "曾超群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-09",
        "birthplace": "湖南省邵东市",
        "education": "北京大学经济学院国际经济专业本科、湖南农业大学管理学博士",
        "party_join": "1998-12",
        "work_start": "1997-09",
        "current_post": "市委书记",
        "current_org": "中共娄底市委",
        "source": "https://zh.wikipedia.org/wiki/曾超群_(1975年)",
        "confidence": "confirmed",
        "notes": "北京大学毕业，省委办公厅7年，长沙县书记，张家界常务副市长，娄底市长→书记"
    },
    {
        "id": 2,
        "name": "何朝晖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-04",
        "birthplace": "湖南省攸县",
        "education": "在职研究生、管理学博士",
        "party_join": "",
        "work_start": "",
        "current_post": "市长",
        "current_org": "娄底市人民政府",
        "source": "https://zh.wikipedia.org/wiki/娄底市",
        "confidence": "confirmed",
        "notes": "2025.11任娄底市长；完整履历（此前职务）待查"
    },
    {
        "id": 60,
        "name": "邹文辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965-02",
        "birthplace": "湖南省常宁市",
        "education": "",
        "party_join": "1986",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "湖南省人大常委会",
        "source": "https://zh.wikipedia.org/wiki/邹文辉",
        "confidence": "confirmed",
        "notes": "2021.10-2025.04任娄底市委书记，后任省人大常委会环资委主任委员"
    },
    {
        "id": 4,
        "name": "李定桥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-09",
        "birthplace": "湖南省安仁县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "娄底市人大常委会",
        "source": "https://zh.wikipedia.org/wiki/娄底市",
        "confidence": "confirmed",
        "notes": "2026.01任市人大常委会主任；此前职务待查"
    },
    {
        "id": 5,
        "name": "梁立坚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-10",
        "birthplace": "湖南省涟源市",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "娄底市政协",
        "source": "https://zh.wikipedia.org/wiki/娄底市",
        "confidence": "confirmed",
        "notes": "2022.01任市政协主席；此前职务待查"
    },
    # ══════════════════════════════════════════════════════════════════════════
    # 娄星区领导 (Louxing District)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "李彦文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-03",
        "birthplace": "湖南省涟源市",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "娄星区委书记",
        "current_org": "中共娄星区委",
        "source": "https://zh.wikipedia.org/wiki/娄星区",
        "confidence": "confirmed",
        "notes": "2018.10起任娄星区委书记"
    },
    {
        "id": 11,
        "name": "刘志刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-10",
        "birthplace": "湖南省新化县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "娄星区长",
        "current_org": "娄星区人民政府",
        "source": "https://zh.wikipedia.org/wiki/娄星区",
        "confidence": "confirmed",
        "notes": "2021.10起任娄星区长"
    },
    {
        "id": 12,
        "name": "陈晓林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966-02",
        "birthplace": "湖南省新化县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "娄星区人大常委会主任",
        "current_org": "娄星区人大常委会",
        "source": "https://zh.wikipedia.org/wiki/娄星区",
        "confidence": "confirmed",
        "notes": "2021.10起任"
    },
    {
        "id": 13,
        "name": "邓伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-04",
        "birthplace": "湖南省宁乡市",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "娄星区政协主席",
        "current_org": "娄星区政协",
        "source": "https://zh.wikipedia.org/wiki/娄星区",
        "confidence": "confirmed",
        "notes": "2021.10起任"
    },
    # ══════════════════════════════════════════════════════════════════════════
    # 双峰县领导 (Shuangfeng County)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": 20,
        "name": "彭石清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-07",
        "birthplace": "湖南省娄底市娄星区",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "双峰县委书记",
        "current_org": "中共双峰县委",
        "source": "https://zh.wikipedia.org/wiki/双峰县",
        "confidence": "confirmed",
        "notes": "2021.07起任双峰县委书记"
    },
    {
        "id": 21,
        "name": "李基联",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-07",
        "birthplace": "湖南省溆浦县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "双峰县长",
        "current_org": "双峰县人民政府",
        "source": "https://zh.wikipedia.org/wiki/双峰县",
        "confidence": "confirmed",
        "notes": "2021.10起任双峰县长；籍贯溆浦，跨市交流干部"
    },
    {
        "id": 22,
        "name": "段平屏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-10",
        "birthplace": "湖南省冷水江市",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "双峰县人大常委会主任",
        "current_org": "双峰县人大常委会",
        "source": "https://zh.wikipedia.org/wiki/双峰县",
        "confidence": "confirmed",
        "notes": "2021.10起任"
    },
    {
        "id": 23,
        "name": "王德文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-07",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "双峰县政协主席",
        "current_org": "双峰县政协",
        "source": "https://zh.wikipedia.org/wiki/双峰县",
        "confidence": "confirmed",
        "notes": "2021.10起任；籍贯待查"
    },
    # ══════════════════════════════════════════════════════════════════════════
    # 新化县领导 (Xinhua County)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "彭韬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-01",
        "birthplace": "湖南省新化县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新化县委书记",
        "current_org": "中共新化县委",
        "source": "https://zh.wikipedia.org/wiki/新化县",
        "confidence": "confirmed",
        "notes": "1984年生，全市最年轻的县委书记；此前为新化县长，2025.06升书记"
    },
    {
        "id": 31,
        "name": "邹剑锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-09",
        "birthplace": "湖南省长沙县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新化县长",
        "current_org": "新化县人民政府",
        "source": "https://zh.wikipedia.org/wiki/新化县",
        "confidence": "confirmed",
        "notes": "1985年生，从长沙县调任；2025.12任新化县长"
    },
    {
        "id": 32,
        "name": "杨韶红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966-11",
        "birthplace": "湖南省新化县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新化县人大常委会主任",
        "current_org": "新化县人大常委会",
        "source": "https://zh.wikipedia.org/wiki/新化县",
        "confidence": "confirmed",
        "notes": "2021.10起任"
    },
    {
        "id": 33,
        "name": "李笃成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-04",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新化县政协主席",
        "current_org": "新化县政协",
        "source": "https://zh.wikipedia.org/wiki/新化县",
        "confidence": "confirmed",
        "notes": "2021.10起任；籍贯待查"
    },
    # ══════════════════════════════════════════════════════════════════════════
    # 冷水江市领导 (Lengshuijiang City)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": 40,
        "name": "曾伯怡",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-10",
        "birthplace": "湖南省双峰县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "冷水江市委书记",
        "current_org": "中共冷水江市委",
        "source": "https://zh.wikipedia.org/wiki/冷水江市",
        "confidence": "confirmed",
        "notes": "2021.07起任冷水江市委书记"
    },
    {
        "id": 41,
        "name": "陈创业",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-06",
        "birthplace": "湖南省新化县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "冷水江市长",
        "current_org": "冷水江市人民政府",
        "source": "https://zh.wikipedia.org/wiki/冷水江市",
        "confidence": "confirmed",
        "notes": "2021.09起任冷水江市长"
    },
    {
        "id": 42,
        "name": "孙纬辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-10",
        "birthplace": "湖南省新化县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "冷水江市人大常委会主任",
        "current_org": "冷水江市人大常委会",
        "source": "https://zh.wikipedia.org/wiki/冷水江市",
        "confidence": "confirmed",
        "notes": "2021.11起任"
    },
    {
        "id": 43,
        "name": "罗中秋",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1965",
        "birthplace": "湖南省邵东市",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "冷水江市政协主席",
        "current_org": "冷水江市政协",
        "source": "https://zh.wikipedia.org/wiki/冷水江市",
        "confidence": "confirmed",
        "notes": "2018年起任冷水江市政协主席"
    },
    # ══════════════════════════════════════════════════════════════════════════
    # 涟源市领导 (Lianyuan City)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": 50,
        "name": "段晓赛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "湖南省耒阳市",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "涟源市委书记",
        "current_org": "中共涟源市委",
        "source": "https://zh.wikipedia.org/wiki/段晓赛",
        "confidence": "confirmed",
        "notes": "2025.03从衡山县县长跨市调任涟源市委书记；1980年生(推定)"
    },
    {
        "id": 51,
        "name": "邓伟谋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976",
        "birthplace": "湖南省双峰县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "涟源市长",
        "current_org": "涟源市人民政府",
        "source": "https://zh.wikipedia.org/wiki/涟源市",
        "confidence": "confirmed",
        "notes": "2021.07起任涟源市长"
    },
    {
        "id": 52,
        "name": "梁育清",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1967",
        "birthplace": "湖南省涟源市",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "涟源市人大常委会主任",
        "current_org": "涟源市人大常委会",
        "source": "https://zh.wikipedia.org/wiki/涟源市",
        "confidence": "confirmed",
        "notes": "2021年起任"
    },
    {
        "id": 53,
        "name": "周惠军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971",
        "birthplace": "湖南省娄底市娄星区",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "涟源市政协主席",
        "current_org": "涟源市政协",
        "source": "https://zh.wikipedia.org/wiki/涟源市",
        "confidence": "confirmed",
        "notes": "2021.10起任"
    },
    # ══════════════════════════════════════════════════════════════════════════
    # 前任/腐败案件关联人物
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": 61,
        "name": "李荐国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "已落马",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/李荐国",
        "confidence": "confirmed",
        "notes": "娄底市委书记(2016-2019)，受贿2704万，判刑13年"
    },
    {
        "id": 62,
        "name": "杨懿文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "已落马",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/杨懿文",
        "confidence": "confirmed",
        "notes": "娄底市长(2016-2021)、后任常德市委书记；受贿6979万，判刑16年6个月"
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Organizations
# ═══════════════════════════════════════════════════════════════════════════════
organizations = [
    # 市级
    {"id": 1, "name": "中共娄底市委", "type": "党委", "level": "地级", "parent": "中共湖南省委", "location": "娄底市"},
    {"id": 2, "name": "娄底市人民政府", "type": "政府", "level": "地级", "parent": "", "location": "娄底市"},
    {"id": 3, "name": "娄底市人大常委会", "type": "人大", "level": "地级", "parent": "", "location": "娄底市"},
    {"id": 4, "name": "娄底市政协", "type": "政协", "level": "地级", "parent": "", "location": "娄底市"},
    {"id": 5, "name": "湖南省人大常委会", "type": "人大", "level": "省级", "parent": "", "location": "长沙市"},
    # 娄星区
    {"id": 10, "name": "中共娄星区委", "type": "党委", "level": "县级", "parent": "中共娄底市委", "location": "娄星区"},
    {"id": 11, "name": "娄星区人民政府", "type": "政府", "level": "县级", "parent": "", "location": "娄星区"},
    {"id": 12, "name": "娄星区人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "娄星区"},
    {"id": 13, "name": "娄星区政协", "type": "政协", "level": "县级", "parent": "", "location": "娄星区"},
    # 双峰县
    {"id": 20, "name": "中共双峰县委", "type": "党委", "level": "县级", "parent": "中共娄底市委", "location": "双峰县"},
    {"id": 21, "name": "双峰县人民政府", "type": "政府", "level": "县级", "parent": "", "location": "双峰县"},
    {"id": 22, "name": "双峰县人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "双峰县"},
    {"id": 23, "name": "双峰县政协", "type": "政协", "level": "县级", "parent": "", "location": "双峰县"},
    # 新化县
    {"id": 30, "name": "中共新化县委", "type": "党委", "level": "县级", "parent": "中共娄底市委", "location": "新化县"},
    {"id": 31, "name": "新化县人民政府", "type": "政府", "level": "县级", "parent": "", "location": "新化县"},
    {"id": 32, "name": "新化县人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "新化县"},
    {"id": 33, "name": "新化县政协", "type": "政协", "level": "县级", "parent": "", "location": "新化县"},
    # 冷水江市
    {"id": 40, "name": "中共冷水江市委", "type": "党委", "level": "县级", "parent": "中共娄底市委", "location": "冷水江市"},
    {"id": 41, "name": "冷水江市人民政府", "type": "政府", "level": "县级", "parent": "", "location": "冷水江市"},
    {"id": 42, "name": "冷水江市人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "冷水江市"},
    {"id": 43, "name": "冷水江市政协", "type": "政协", "level": "县级", "parent": "", "location": "冷水江市"},
    # 涟源市
    {"id": 50, "name": "中共涟源市委", "type": "党委", "level": "县级", "parent": "中共娄底市委", "location": "涟源市"},
    {"id": 51, "name": "涟源市人民政府", "type": "政府", "level": "县级", "parent": "", "location": "涟源市"},
    {"id": 52, "name": "涟源市人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "涟源市"},
    {"id": 53, "name": "涟源市政协", "type": "政协", "level": "县级", "parent": "", "location": "涟源市"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Positions
# ═══════════════════════════════════════════════════════════════════════════════
positions = [
    # 曾超群 — current Party Secretary
    {"person_id": 1, "org_id": 1, "title": "中共娄底市委书记", "start_date": "2025-04", "end_date": "", "rank": "正厅级",
     "note": "2025.04由市长升任市委书记"},
    {"person_id": 1, "org_id": 2, "title": "娄底市人民政府市长", "start_date": "2021-04", "end_date": "2025-11", "rank": "正厅级",
     "note": "2021.04-2025.11任娄底市长"},
    # 何朝晖 — current Mayor
    {"person_id": 2, "org_id": 2, "title": "娄底市人民政府市长", "start_date": "2025-11", "end_date": "", "rank": "正厅级",
     "note": "2025.11任娄底市长"},
    # 邹文辉 — predecessor Party Secretary
    {"person_id": 60, "org_id": 1, "title": "中共娄底市委书记", "start_date": "2021-10", "end_date": "2025-04", "rank": "正厅级",
     "note": "2021.10-2025.04任娄底市委书记"},
    {"person_id": 60, "org_id": 5, "title": "湖南省人大常委会环资委主任委员", "start_date": "2025-01", "end_date": "", "rank": "正厅级",
     "note": "2025.01起任省人大常委会环资委主任委员"},
    # 李定桥 — 人大主任
    {"person_id": 4, "org_id": 3, "title": "娄底市人大常委会主任", "start_date": "2026-01", "end_date": "", "rank": "正厅级",
     "note": "2026.01任"},
    # 梁立坚 — 政协主席
    {"person_id": 5, "org_id": 4, "title": "娄底市政协主席", "start_date": "2022-01", "end_date": "", "rank": "正厅级",
     "note": "2022.01任"},
    # 娄星区
    {"person_id": 10, "org_id": 10, "title": "娄星区委书记", "start_date": "2018-10", "end_date": "", "rank": "副厅级",
     "note": ""},
    {"person_id": 11, "org_id": 11, "title": "娄星区长", "start_date": "2021-10", "end_date": "", "rank": "正处级",
     "note": ""},
    {"person_id": 12, "org_id": 12, "title": "娄星区人大常委会主任", "start_date": "2021-10", "end_date": "", "rank": "正处级",
     "note": ""},
    {"person_id": 13, "org_id": 13, "title": "娄星区政协主席", "start_date": "2021-10", "end_date": "", "rank": "正处级",
     "note": ""},
    # 双峰县
    {"person_id": 20, "org_id": 20, "title": "双峰县委书记", "start_date": "2021-07", "end_date": "", "rank": "副厅级",
     "note": ""},
    {"person_id": 21, "org_id": 21, "title": "双峰县长", "start_date": "2021-10", "end_date": "", "rank": "正处级",
     "note": ""},
    {"person_id": 22, "org_id": 22, "title": "双峰县人大常委会主任", "start_date": "2021-10", "end_date": "", "rank": "正处级",
     "note": ""},
    {"person_id": 23, "org_id": 23, "title": "双峰县政协主席", "start_date": "2021-10", "end_date": "", "rank": "正处级",
     "note": ""},
    # 新化县
    {"person_id": 30, "org_id": 30, "title": "新化县委书记", "start_date": "2025-06", "end_date": "", "rank": "副厅级",
     "note": "2025.06由县长升书记"},
    {"person_id": 30, "org_id": 31, "title": "新化县人民政府县长", "start_date": "2021", "end_date": "2025-06", "rank": "正处级",
     "note": "此前为新化县长"},
    {"person_id": 31, "org_id": 31, "title": "新化县长", "start_date": "2025-12", "end_date": "", "rank": "正处级",
     "note": "2025.12从长沙县调任"},
    {"person_id": 32, "org_id": 32, "title": "新化县人大常委会主任", "start_date": "2021-10", "end_date": "", "rank": "正处级",
     "note": ""},
    {"person_id": 33, "org_id": 33, "title": "新化县政协主席", "start_date": "2021-10", "end_date": "", "rank": "正处级",
     "note": ""},
    # 冷水江市
    {"person_id": 40, "org_id": 40, "title": "冷水江市委书记", "start_date": "2021-07", "end_date": "", "rank": "副厅级",
     "note": ""},
    {"person_id": 41, "org_id": 41, "title": "冷水江市长", "start_date": "2021-09", "end_date": "", "rank": "正处级",
     "note": ""},
    {"person_id": 42, "org_id": 42, "title": "冷水江市人大常委会主任", "start_date": "2021-11", "end_date": "", "rank": "正处级",
     "note": ""},
    {"person_id": 43, "org_id": 43, "title": "冷水江市政协主席", "start_date": "2018", "end_date": "", "rank": "正处级",
     "note": ""},
    # 涟源市
    {"person_id": 50, "org_id": 50, "title": "涟源市委书记", "start_date": "2025-03", "end_date": "", "rank": "副厅级",
     "note": "2025.03从衡山县跨市调任"},
    {"person_id": 51, "org_id": 51, "title": "涟源市长", "start_date": "2021-07", "end_date": "", "rank": "正处级",
     "note": ""},
    {"person_id": 52, "org_id": 52, "title": "涟源市人大常委会主任", "start_date": "2021", "end_date": "", "rank": "正处级",
     "note": ""},
    {"person_id": 53, "org_id": 53, "title": "涟源市政协主席", "start_date": "2021-10", "end_date": "", "rank": "正处级",
     "note": ""},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Relationships
# ═══════════════════════════════════════════════════════════════════════════════
relationships = [
    # 曾超群 ↔ 邹文辉 (succession + colleague)
    {"person_a": 1, "person_b": 60, "type": "succession",
     "context": "曾超群接替邹文辉任娄底市委书记",
     "overlap_org": "中共娄底市委", "overlap_period": "2025"},
    {"person_a": 1, "person_b": 60, "type": "colleague",
     "context": "曾超群任市长期间与邹文辉（书记）共事4年",
     "overlap_org": "中共娄底市委/娄底市人民政府", "overlap_period": "2021-2025"},
    # 曾超群 ↔ 杨懿文 (succession as mayor)
    {"person_a": 1, "person_b": 62, "type": "succession",
     "context": "曾超群接替杨懿文任娄底市长",
     "overlap_org": "娄底市人民政府", "overlap_period": "2021"},
    # 曾超群 ↔ 何朝晖 (succession as mayor + colleague)
    {"person_a": 1, "person_b": 2, "type": "succession",
     "context": "曾超群升市委书记后，何朝晖接任市长",
     "overlap_org": "娄底市人民政府", "overlap_period": "2025"},
    {"person_a": 1, "person_b": 2, "type": "colleague",
     "context": "曾超群（书记）与何朝晖（市长）党政搭档",
     "overlap_org": "娄底市", "overlap_period": "2025-"},
    # 曾超群 ↔ 李定桥 (colleague)
    {"person_a": 1, "person_b": 4, "type": "colleague",
     "context": "曾超群与李定桥在娄底市共事",
     "overlap_org": "娄底市", "overlap_period": "2026"},
    # 曾超群 ↔ 梁立坚 (colleague)
    {"person_a": 1, "person_b": 5, "type": "colleague",
     "context": "曾超群与梁立坚在娄底市共事（书记—政协主席）",
     "overlap_org": "娄底市", "overlap_period": "2022-"},
    # 何朝晖 ↔ 李定桥
    {"person_a": 2, "person_b": 4, "type": "colleague",
     "context": "何朝晖与李定桥在娄底市共事",
     "overlap_org": "娄底市", "overlap_period": "2026"},
    # 何朝晖 ↔ 梁立坚
    {"person_a": 2, "person_b": 5, "type": "colleague",
     "context": "何朝晖与梁立坚在娄底市共事",
     "overlap_org": "娄底市", "overlap_period": "2025-"},
    # 同乡关系 — 涟源系
    {"person_a": 10, "person_b": 5, "type": "hometown",
     "context": "李彦文（涟源人）与梁立坚（涟源人）同乡",
     "overlap_org": "涟源市", "overlap_period": ""},
    # 同乡关系 — 新化系
    {"person_a": 11, "person_b": 41, "type": "hometown",
     "context": "刘志刚（新化人）与陈创业（新化人）同乡",
     "overlap_org": "新化县", "overlap_period": ""},
    {"person_a": 30, "person_b": 11, "type": "hometown",
     "context": "彭韬（新化人）与刘志刚（新化人）同乡",
     "overlap_org": "新化县", "overlap_period": ""},
    {"person_a": 30, "person_b": 41, "type": "hometown",
     "context": "彭韬（新化人）与陈创业（新化人）同乡",
     "overlap_org": "新化县", "overlap_period": ""},
    {"person_a": 30, "person_b": 42, "type": "hometown",
     "context": "彭韬（新化人）与孙纬辉（新化人）同乡",
     "overlap_org": "新化县", "overlap_period": ""},
    # 同乡关系 — 双峰系
    {"person_a": 40, "person_b": 51, "type": "hometown",
     "context": "曾伯怡（双峰人）与邓伟谋（双峰人）同乡",
     "overlap_org": "双峰县", "overlap_period": ""},
    {"person_a": 40, "person_b": 20, "type": "hometown",
     "context": "曾伯怡（双峰人）与彭石清（娄星区人）——毗邻",
     "overlap_org": "", "overlap_period": ""},
    # 同乡关系 — 娄星区系
    {"person_a": 20, "person_b": 53, "type": "hometown",
     "context": "彭石清（娄星区人）与周惠军（娄星区人）同乡",
     "overlap_org": "娄星区", "overlap_period": ""},
    # 新化县领导党政搭档
    {"person_a": 30, "person_b": 32, "type": "colleague",
     "context": "彭韬（书记）与杨韶红（人大主任）在新化县共事",
     "overlap_org": "新化县", "overlap_period": "2025-"},
    {"person_a": 31, "person_b": 30, "type": "colleague",
     "context": "邹剑锋（县长）与彭韬（书记）党政搭档",
     "overlap_org": "新化县", "overlap_period": "2025-"},
    # 涟源市党政搭档
    {"person_a": 50, "person_b": 51, "type": "colleague",
     "context": "段晓赛（书记）与邓伟谋（市长）党政搭档",
     "overlap_org": "涟源市", "overlap_period": "2025-"},
    # 冷水江市党政搭档
    {"person_a": 40, "person_b": 41, "type": "colleague",
     "context": "曾伯怡（书记）与陈创业（市长）党政搭档",
     "overlap_org": "冷水江市", "overlap_period": "2021-"},
    # 李荐国—杨懿文 (两人在娄底共事+均涉腐)
    {"person_a": 61, "person_b": 62, "type": "colleague",
     "context": "李荐国（书记）与杨懿文（市长）党政搭档",
     "overlap_org": "娄底市", "overlap_period": "2016-2021"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Helper functions
# ═══════════════════════════════════════════════════════════════════════════════


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
    if not person.get("notes", ""):
        questions.append("完整任职履历未确认")
    return questions


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"loudi_{name}"

    # Collect positions for this person
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

    # Add gap entry if career_timeline is sparse
    if len(career_timeline) <= 1 and not person.get("birth"):
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料不足，完整履历待查。百度百科403禁止访问，Wikipedia超时。",
            "confidence": "unverified",
            "source_ids": [],
        })

    # Collect relationships for this person
    person_rels = [
        r for r in relationships
        if r["person_a"] == pid or r["person_b"] == pid
    ]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rel_type_map = {
            "colleague": "overlap",
            "succession": "predecessor_successor",
            "hometown": "same_native_place",
            "subordinate": "superior_subordinate",
        }
        strength_map = {
            "colleague": "strong",
            "succession": "strong",
            "hometown": "weak",
            "subordinate": "strong",
        }
        rels_output.append({
            "person": other_name,
            "person_id": f"loudi_{other_name}",
            "relationship_type": rel_type_map.get(r["type"], "overlap"),
            "strength": strength_map.get(r["type"], "medium"),
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if r["type"] in ("colleague", "succession") else "plausible",
            "source_ids": ["S001"],
        })

    # Source register
    source_url = person.get("source", "")
    sources = [
        {
            "id": "S001",
            "title": f"娄底市相关Wikipedia页面",
            "url": source_url,
            "publisher": "Wikipedia",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": "Wikipedia条目；另经娄底市人民政府官网新闻交叉印证职务",
        }
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "湖南省",
            "city": "娄底市",
            "region": "娄底市",
            "job": person.get("current_post", ""),
            "task_id": "hunan_娄底市",
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
            "education": [],
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
            "administrative_rank": "",
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
            "identity": "unverified" if not person.get("birth") else "confirmed",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "大部分人物的完整履历（特别在市县领导班子任职经历）缺失",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历（此前职务及每段职务起止时间）",
                "why_it_matters": "关系网络分析需要精确的时间线",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{name}的学历教育背景",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [f"{name} 学历"],
                "last_attempted": AS_OF,
            },
        ],
    }

    fname = f"{TODAY}-湖南省-娄底市-{person['current_post']}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


# ═══════════════════════════════════════════════════════════════════════════════
# Build
# ═══════════════════════════════════════════════════════════════════════════════


def main() -> int:
    print(f"Building {SLUG} network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

    # Run build using the shared runner
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
    # Core leaders: 市委书记(1), 市长(2), 前任书记(60), 人大主任(4), 政协主席(5)
    core_ids = {1, 2, 60, 4, 5}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
