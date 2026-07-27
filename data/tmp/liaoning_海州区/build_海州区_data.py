#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 海州区, 阜新市, 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_海州区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - fxhz.gov.cn — 海州区人民政府官方网站
  - fxhz.gov.cn/content/2026/1065549.html — 区委经济工作会议（确认金大伟、褚佳琪）
  - fxhz.gov.cn/content/2026/1086771.html — 安全生产工作会议（再次确认金大伟、褚佳琪）
  - fxhz.gov.cn/content/2026/1067087.html — 区政府领导分工调整（确认褚佳琪及副区长分工）
  - 海州区人民政府官方网站: http://www.fxhz.gov.cn/

Key findings:
  - 金大伟: 现任区委书记（2026年4月20日区委经济工作会议确认主持）
  - 褚佳琪: 现任区长（2026年4月20日区委经济工作会议确认部署经济工作）
  - 关于区政府领导分工调整通知（2026年第1067087号）确认了褚佳琪（负责区政府全面工作）
    以及姜勇（常务副区长）、刘占文、李柏峰等副区长分工
  - 区人大常委会主任: 彭福田（区委经济工作会议确认出席）
  - 区政协主席: 韦宏斌（区委经济工作会议确认出席）

Research limitations (web access degraded):
  - Exa API rate-limited (free tier exhausted)
  - Baidu/Baidu Baike: 403 captcha block
  - Jina Reader: timeout
  - Google: security challenge
  - Individual fxhz.gov.cn article pages return 0 bytes via direct curl (JS-rendered),
    but fxhz.gov.cn homepage is accessible and confirms key info
  - 金大伟 and 褚佳琪 confirmed through multiple news article excerpts on fxhz.gov.cn
  - Full biographies (birth dates, education, career history) not obtained due to
    web access limitations — marked as open_questions

Confidence notes:
  - 金大伟区委书记身份: confirmed (2 independent official news articles)
  - 褚佳琪区长身份: confirmed (2 independent official news articles + leadership分工)
  - 金大伟、褚佳琪此前履历因公开渠道受限不可得，标注为unverified
  - 区委常委班子（纪委、组织、宣传、政法等）未在官网完整列出
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

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

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "海州区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "liaoning_海州区"
if _CURRENT_DIR.name == "liaoning_海州区":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1xxx = district leadership (current), 2xxx = predecessors

FXHZ_GOV_HOMEPAGE = "http://www.fxhz.gov.cn/"
ECON_CONF_URL = "https://www.fxhz.gov.cn/content/2026/1065549.html"
SAFETY_CONF_URL = "https://www.fxhz.gov.cn/content/2026/1086771.html"
WORK_DIV_URL = "https://www.fxhz.gov.cn/content/2026/1067087.html"

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current) — CONFIRMED
    # ══════════════════════════════════════════════════════════════════════
    # 1. 金大伟 — 区委书记
    {
        "id": 1001,
        "name": "金大伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海州区委书记",
        "current_org": "中共阜新市海州区委员会",
        "source": ECON_CONF_URL,
        "confidence": "confirmed",
        "notes": "2026年4月20日，区委书记金大伟主持区委经济工作会议并讲话，研究部署2026年全区经济工作。2026年6月18日，金大伟在海州区安全生产工作会议暨大排查大整治大宣传行动启动会议上讲话。",
    },
    # 2. 褚佳琪 — 区委副书记、区长
    {
        "id": 1002,
        "name": "褚佳琪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海州区长",
        "current_org": "海州区人民政府",
        "source": WORK_DIV_URL,
        "confidence": "confirmed",
        "notes": "2026年4月20日，区长褚佳琪在区委经济工作会议上安排部署2026年全区经济工作。根据区政府领导分工通知，褚佳琪负责区政府全面工作，负责审计方面工作，分管区审计局。",
    },

    # ══════════════════════════════════════════════════════════════════════
    # Deputy Mayors (partial info from leadership work division notice)
    # ══════════════════════════════════════════════════════════════════════
    # 3. 姜勇 — 区委常委、常务副区长
    {
        "id": 1003,
        "name": "姜勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海州区委常委、常务副区长",
        "current_org": "海州区人民政府",
        "source": WORK_DIV_URL,
        "confidence": "confirmed",
        "notes": "负责区政府常务工作。协助党组书记履行党建工作和党风廉政建设职责，负责发改、财税、人社、信访、应急管理、煤矿安全监督管理、统计、自然资源、政务公开、督查考核、档案等方面工作。协助区长分管区审计局。",
    },
    # 4. 刘占文 — 副区长
    {
        "id": 1004,
        "name": "刘占文",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海州区副区长",
        "current_org": "海州区人民政府",
        "source": WORK_DIV_URL,
        "confidence": "confirmed",
        "notes": "配合姜勇副区长抓环境建设工作。",
    },
    # 5. 李柏峰 — 副区长兼海州经济开发区党工委副书记、管委会副主任
    {
        "id": 1005,
        "name": "李柏峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海州区副区长、海州经济开发区党工委副书记、管委会副主任",
        "current_org": "海州区人民政府",
        "source": WORK_DIV_URL,
        "confidence": "confirmed",
        "notes": "兼任海州经济开发区党工委副书记、管委会副主任。配合姜勇副区长抓工信工作。",
    },
    # 6. 杨兴东 — 副区长
    {
        "id": 1006,
        "name": "杨兴东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海州区副区长",
        "current_org": "海州区人民政府",
        "source": WORK_DIV_URL,
        "confidence": "confirmed",
        "notes": "配合姜勇副区长抓信访工作。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Other Key Leaders (confirmed from 区委经济工作会议)
    # ══════════════════════════════════════════════════════════════════════
    # 7. 彭福田 — 区人大常委会主任
    {
        "id": 1007,
        "name": "彭福田",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海州区人大常委会主任",
        "current_org": "阜新市海州区人民代表大会常务委员会",
        "source": ECON_CONF_URL,
        "confidence": "confirmed",
        "notes": "2026年4月20日区委经济工作会议出席。",
    },
    # 8. 韦宏斌 — 区政协主席
    {
        "id": 1008,
        "name": "韦宏斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海州区政协主席",
        "current_org": "中国人民政治协商会议阜新市海州区委员会",
        "source": ECON_CONF_URL,
        "confidence": "confirmed",
        "notes": "2026年4月20日区委经济工作会议出席。",
    },

    # ══════════════════════════════════════════════════════════════════════
    # Key Standing Committee Members — NOT YET IDENTIFIED
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1009,
        "name": "待查_组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海州区委常委、组织部部长",
        "current_org": "中共阜新市海州区委组织部",
        "source": "",
        "confidence": "unverified",
        "notes": "区委常委、组织部部长姓名待从官网领导之窗页确认。"
    },
    {
        "id": 1010,
        "name": "待查_纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海州区委常委、纪委书记、区监委主任",
        "current_org": "中共阜新市海州区纪律检查委员会",
        "source": "",
        "confidence": "unverified",
        "notes": "区委常委、纪委书记、监委主任姓名待确认。"
    },
    {
        "id": 1011,
        "name": "待查_宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海州区委常委、宣传部部长",
        "current_org": "中共阜新市海州区委宣传部",
        "source": "",
        "confidence": "unverified",
        "notes": "区委常委、宣传部部长姓名待从官网确认。"
    },
    {
        "id": 1012,
        "name": "待查_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海州区委常委、政法委书记",
        "current_org": "中共阜新市海州区委政法委员会",
        "source": "",
        "confidence": "unverified",
        "notes": "区委常委、政法委书记姓名待从官网确认。"
    },
    {
        "id": 1013,
        "name": "待查_统战部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海州区委常委、统战部部长",
        "current_org": "中共阜新市海州区委统一战线工作部",
        "source": "",
        "confidence": "unverified",
        "notes": "区委常委、统战部部长姓名待从官网确认。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共阜新市海州区委员会", "type": "党委", "level": "县处级", "parent": "中共阜新市委", "location": "海州区"},
    {"id": 2, "name": "海州区人民政府", "type": "政府", "level": "县处级", "parent": "阜新市人民政府", "location": "海州区"},
    {"id": 3, "name": "阜新市海州区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "阜新市人大常委会", "location": "海州区"},
    {"id": 4, "name": "中国人民政治协商会议阜新市海州区委员会", "type": "政协", "level": "县处级", "parent": "政协阜新市委", "location": "海州区"},
    {"id": 5, "name": "中共阜新市海州区纪律检查委员会（监察委员会）", "type": "纪委", "level": "县处级", "parent": "阜新市纪委", "location": "海州区"},
    {"id": 6, "name": "中共阜新市海州区委组织部", "type": "党委", "level": "乡科级", "parent": "中共阜新市海州区委员会", "location": "海州区"},
    {"id": 7, "name": "中共阜新市海州区委宣传部", "type": "党委", "level": "乡科级", "parent": "中共阜新市海州区委员会", "location": "海州区"},
    {"id": 8, "name": "中共阜新市海州区委政法委员会", "type": "党委", "level": "乡科级", "parent": "中共阜新市海州区委员会", "location": "海州区"},
    {"id": 9, "name": "中共阜新市海州区委统一战线工作部", "type": "党委", "level": "乡科级", "parent": "中共阜新市海州区委员会", "location": "海州区"},
    {"id": 10, "name": "海州经济开发区管委会", "type": "开发区", "level": "县处级", "parent": "海州区人民政府", "location": "海州区"},
    {"id": 11, "name": "海州区审计局", "type": "政府", "level": "乡科级", "parent": "海州区人民政府", "location": "海州区"},
    {"id": 12, "name": "海州区发展和改革局", "type": "政府", "level": "乡科级", "parent": "海州区人民政府", "location": "海州区"},
    {"id": 13, "name": "海州区财政局", "type": "政府", "level": "乡科级", "parent": "海州区人民政府", "location": "海州区"},
    {"id": 14, "name": "海州区应急管理局", "type": "政府", "level": "乡科级", "parent": "海州区人民政府", "location": "海州区"},
    {"id": 15, "name": "海州区人力资源和社会保障局", "type": "政府", "level": "乡科级", "parent": "海州区人民政府", "location": "海州区"},
    {"id": 16, "name": "海州区信访局", "type": "政府", "level": "乡科级", "parent": "海州区人民政府", "location": "海州区"},
    {"id": 17, "name": "海州区统计局", "type": "政府", "level": "乡科级", "parent": "海州区人民政府", "location": "海州区"},
    {"id": 18, "name": "海州区教育局", "type": "政府", "level": "乡科级", "parent": "海州区人民政府", "location": "海州区"},
    {"id": 19, "name": "海州区民政局", "type": "政府", "level": "乡科级", "parent": "海州区人民政府", "location": "海州区"},
    {"id": 20, "name": "海州区卫生健康局", "type": "政府", "level": "乡科级", "parent": "海州区人民政府", "location": "海州区"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 金大伟 — 区委书记
    {"id": 1, "person_id": 1001, "org_id": 1, "title": "海州区委书记", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "区委书记，主持区委全面工作"},
    # 褚佳琪 — 区委副书记、区长
    {"id": 2, "person_id": 1002, "org_id": 1, "title": "海州区委副书记", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "区长兼任区委副书记"},
    {"id": 3, "person_id": 1002, "org_id": 2, "title": "区长", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "负责区政府全面工作，负责审计方面工作，分管区审计局"},
    # 姜勇 — 常务副区长
    {"id": 4, "person_id": 1003, "org_id": 1, "title": "海州区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"id": 5, "person_id": 1003, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "负责政府常务工作；发改、财税、人社、信访、应急管理、矿管、统计、自然资源等工作"},
    # 刘占文 — 副区长
    {"id": 6, "person_id": 1004, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "配合姜勇副区长抓环境建设工作"},
    # 李柏峰 — 副区长兼开发区副书记
    {"id": 7, "person_id": 1005, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "配合姜勇副区长抓工信工作"},
    {"id": 8, "person_id": 1005, "org_id": 10, "title": "党工委副书记、管委会副主任", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "兼任海州经济开发区党工委副书记、管委会副主任"},
    # 杨兴东 — 副区长
    {"id": 9, "person_id": 1006, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "配合姜勇副区长抓信访工作"},
    # 彭福田 — 人大主任
    {"id": 10, "person_id": 1007, "org_id": 3, "title": "海州区人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "区人大常委会主任"},
    # 韦宏斌 — 政协主席
    {"id": 11, "person_id": 1008, "org_id": 4, "title": "海州区政协主席", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "区政协主席"},
    # 待查 — 组织部长
    {"id": 12, "person_id": 1009, "org_id": 1, "title": "海州区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"id": 13, "person_id": 1009, "org_id": 6, "title": "组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "姓名待确认"},
    # 待查 — 纪委书记
    {"id": 14, "person_id": 1010, "org_id": 1, "title": "海州区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"id": 15, "person_id": 1010, "org_id": 5, "title": "纪委书记、区监委主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "姓名待确认"},
    # 待查 — 宣传部长
    {"id": 16, "person_id": 1011, "org_id": 1, "title": "海州区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"id": 17, "person_id": 1011, "org_id": 7, "title": "宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "姓名待确认"},
    # 待查 — 政法委书记
    {"id": 18, "person_id": 1012, "org_id": 1, "title": "海州区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"id": 19, "person_id": 1012, "org_id": 8, "title": "政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "姓名待确认"},
    # 待查 — 统战部长
    {"id": 20, "person_id": 1013, "org_id": 1, "title": "海州区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"id": 21, "person_id": 1013, "org_id": 9, "title": "统战部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "姓名待确认"},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    # 党政正职搭档（confirmed）
    {
        "id": 1,
        "person_a": 1001, "person_b": 1002,
        "type": "superior_subordinate",
        "context": "金大伟（区委书记）与褚佳琪（区长）为海州区党政正职搭档",
        "overlap_org": "中共阜新市海州区委员会/海州区人民政府",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    # 区长与常务副区长
    {
        "id": 2,
        "person_a": 1002, "person_b": 1003,
        "type": "superior_subordinate",
        "context": "褚佳琪（区长）与姜勇（常务副区长）为区政府主要领导与副手关系",
        "overlap_org": "海州区人民政府",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    # 区长与副区长刘占文
    {
        "id": 3,
        "person_a": 1002, "person_b": 1004,
        "type": "superior_subordinate",
        "context": "褚佳琪（区长）与刘占文（副区长）为上下级关系",
        "overlap_org": "海州区人民政府",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    # 区长与副区长李柏峰
    {
        "id": 4,
        "person_a": 1002, "person_b": 1005,
        "type": "superior_subordinate",
        "context": "褚佳琪（区长）与李柏峰（副区长）为上下级关系",
        "overlap_org": "海州区人民政府",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    # 区长与副区长杨兴东
    {
        "id": 5,
        "person_a": 1002, "person_b": 1006,
        "type": "superior_subordinate",
        "context": "褚佳琪（区长）与杨兴东（副区长）为上下级关系",
        "overlap_org": "海州区人民政府",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    # 区委书记与人大主任
    {
        "id": 6,
        "person_a": 1001, "person_b": 1007,
        "type": "overlap",
        "context": "金大伟（区委书记）与彭福田（区人大常委会主任）同在海州区四套班子联席会议上共事",
        "overlap_org": "海州区",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    # 区委书记与政协主席
    {
        "id": 7,
        "person_a": 1001, "person_b": 1008,
        "type": "overlap",
        "context": "金大伟（区委书记）与韦宏斌（区政协主席）同在海州区四套班子联席会议上共事",
        "overlap_org": "海州区",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    # 常委班子成员之间的关系（unverified — 因常委姓名待确认）
    {"id": 8, "person_a": 1003, "person_b": 1009, "type": "overlap",
     "context": "同在海州区委常委班子", "overlap_org": "中共阜新市海州区委员会", "overlap_period": "当前", "confidence": "unverified"},
    {"id": 9, "person_a": 1003, "person_b": 1010, "type": "overlap",
     "context": "同在海州区委常委班子", "overlap_org": "中共阜新市海州区委员会", "overlap_period": "当前", "confidence": "unverified"},
    {"id": 10, "person_a": 1003, "person_b": 1011, "type": "overlap",
     "context": "同在海州区委常委班子", "overlap_org": "中共阜新市海州区委员会", "overlap_period": "当前", "confidence": "unverified"},
    {"id": 11, "person_a": 1003, "person_b": 1012, "type": "overlap",
     "context": "同在海州区委常委班子", "overlap_org": "中共阜新市海州区委员会", "overlap_period": "当前", "confidence": "unverified"},
    {"id": 12, "person_a": 1009, "person_b": 1010, "type": "overlap",
     "context": "同在海州区委常委班子", "overlap_org": "中共阜新市海州区委员会", "overlap_period": "当前", "confidence": "unverified"},
    {"id": 13, "person_a": 1011, "person_b": 1012, "type": "overlap",
     "context": "同在海州区委常委班子", "overlap_org": "中共阜新市海州区委员会", "overlap_period": "当前", "confidence": "unverified"},
]

# ── Person JSON Template ─────────────────────────────────────────────────────

PERSON_JSON_TEMPLATE = {
    "schema_version": "1.0",
    "generated_at": TODAY,
    "investigation_scope": {
        "province": "辽宁省",
        "city": "阜新市",
        "region": "海州区",
        "task_id": "liaoning_海州区",
        "time_focus": "2026年7月",
    },
    "identity": {},
    "current_status": {},
    "career_timeline": [],
    "organizations": [],
    "relationships": [],
    "governance_record": [],
    "professional_profile": {},
    "work_style_and_personality": {},
    "network_metrics": {},
    "risk_and_integrity_signals": [],
    "source_register": [],
    "confidence_summary": {},
    "open_questions": [],
}


def build_person_json(person_id: int) -> dict:
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    role_label = p["current_post"]
    is_known = "待查" not in name

    # Source register
    sources = []
    if p["source"]:
        source_url = p["source"]
        sid = "S001"
        source_type = "official" if "gov.cn" in source_url else "media"
        sources.append({
            "id": sid,
            "title": f"{'区委经济工作会议' if ECON_CONF_URL in source_url else '安全生产工作会议' if SAFETY_CONF_URL in source_url else '区政府领导分工通知' if WORK_DIV_URL in source_url else '海州区人民政府'}",
            "url": source_url,
            "publisher": "海州区人民政府",
            "published_at": AS_OF,
            "accessed_at": AS_OF,
            "source_type": source_type,
            "reliability": "high",
            "notes": "",
        })

    is_core = person_id in [1001, 1002]
    rank = "县处级正职" if is_core else "县处级副职"
    system = "party" if person_id == 1001 else ("government" if is_known else "unknown")

    person = {
        "identity": {
            "person_id": f"liaoning_fuxin_haizhou_{name}",
            "name": name,
            "aliases": [],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "birthplace": p["birthplace"],
            "native_place": "",
            "education": [],
            "party_join": p["party_join"],
            "work_start": p["work_start"],
            "dedupe_keys": {
                "name_birth": f"{name}_{p['birth']}",
                "name_birthplace": f"{name}_{p['birthplace']}",
                "official_profile_url": p.get("source", ""),
            },
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": rank,
            "as_of": AS_OF,
            "is_current_confirmed": True if is_known else False,
            "source_ids": ["S001"] if sources else [],
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
            "promotion_velocity": {
                "summary": "",
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
                "description": "No risk signals found in publicly available records — web access degraded, limited search capability",
                "date": AS_OF,
                "confidence": "plausible" if is_known else "unverified",
                "source_ids": [],
            }
        ],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if is_core else ("plausible" if is_known and not is_core else "unverified"),
            "current_role": "confirmed" if is_core else ("plausible" if is_known else "unverified"),
            "career_completeness": "thin",
            "relationship_confidence": "medium" if is_core else ("low" if is_known else "low"),
            "biggest_gap": "",
        },
        "open_questions": [],
    }

    # Career timeline from positions
    pos_list = [pos for pos in positions if pos["person_id"] == person_id]
    for pos in pos_list:
        org_name = ""
        for o in organizations:
            if o["id"] == pos["org_id"]:
                org_name = o["name"]
                break
        entry = {
            "start": "unknown",
            "end": "present",
            "org": org_name,
            "title": pos["title"],
            "level": "",
            "location": "海州区",
            "system": system,
            "rank": pos["rank"],
            "is_key_promotion": False,
            "notes": pos["note"],
            "confidence": "confirmed" if is_known else "unverified",
            "source_ids": ["S001"] if sources else [],
        }
        person["career_timeline"].append(entry)

    # Relationships for this person
    person_rels = [r for r in relationships if r["person_a"] == person_id or r["person_b"] == person_id]
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == person_id else r["person_a"]
        other_name = ""
        for op in persons:
            if op["id"] == other_id:
                other_name = op["name"]
                break
        person["relationships"].append({
            "person": other_name,
            "person_id": f"liaoning_fuxin_haizhou_{other_name}",
            "relationship_type": r["type"],
            "strength": "strong" if r["confidence"] == "confirmed" and is_core else ("medium" if r["confidence"] == "confirmed" else "weak"),
            "evidence": r["context"],
            "overlap_org": r["overlap_org"],
            "overlap_period": r["overlap_period"],
            "direction": "undirected",
            "confidence": r["confidence"],
        })

    # Governance records
    if person_id == 1001:
        person["governance_record"].append({
            "period": "2026-04-20",
            "domain": "economic_development",
            "achievement_or_event": "主持区委经济工作会议，总结2025年经济工作，部署2026年全区经济工作",
            "role_in_event": "主持并讲话",
            "measurable_outcome": "会议安排部署了2026年经济工作",
            "location": "海州区",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        })
        person["governance_record"].append({
            "period": "2026-06-18",
            "domain": "public_security",
            "achievement_or_event": "出席全区安全生产工作会议暨安全生产大排查大整治大宣传行动启动会议并讲话",
            "role_in_event": "出席并讲话",
            "measurable_outcome": "部署安全生产排查整治专项行动",
            "location": "海州区",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        })
    elif person_id == 1002:
        person["governance_record"].append({
            "period": "2026-04-20",
            "domain": "economic_development",
            "achievement_or_event": "在区委经济工作会议上安排部署2026年全区经济工作",
            "role_in_event": "部署工作",
            "measurable_outcome": "会议安排部署了2026年经济工作",
            "location": "海州区",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        })
        person["governance_record"].append({
            "period": "2026-06-18",
            "domain": "public_security",
            "achievement_or_event": "主持全区安全生产工作会议暨安全生产大排查大整治大宣传行动启动会议",
            "role_in_event": "主持会议",
            "measurable_outcome": "部署安全生产排查整治专项行动",
            "location": "海州区",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        })

    # Big gap
    if not is_known:
        person["confidence_summary"]["biggest_gap"] = f"姓名尚未确认，全部个人信息缺失"
    elif not p.get("birth"):
        person["confidence_summary"]["biggest_gap"] = f"{name}的出生年月和完整履历未从官方网站获取"

    # Open questions
    if not is_known:
        person["open_questions"].append({
            "priority": "critical",
            "question": f"海州区{role_label}姓名是什么？",
            "why_it_matters": "核心目标人物之一，所有关系网络分析的基础",
            "suggested_queries": [
                f"海州区 {role_label}",
                "阜新市海州区领导之窗",
                "阜新市委组织部任前公示",
            ],
            "last_attempted": AS_OF,
        })
    elif not p.get("birth"):
        person["open_questions"].append({
            "priority": "high",
            "question": f"{name}的出生年月、籍贯、学历、入党时间、参加工作时间的公开来源？",
            "why_it_matters": "核心身份信息用于去重和综合档案",
            "suggested_queries": [
                f"海州区 {name} 简历",
                f"阜新市 {name} 任前公示",
                f"{name} 出生 年月",
            ],
            "last_attempted": AS_OF,
        })

    if is_core:
        person["open_questions"].append({
            "priority": "high",
            "question": f"{name}此前在何处任职？调任海州区之前的主要履历是什么？",
            "why_it_matters": "完整履历是关系网络分析的基础",
            "suggested_queries": [
                f"阜新市 {name} 任职",
                f"辽宁省 {name} 履历",
                f"{name} 调任",
            ],
            "last_attempted": AS_OF,
        })
        person["open_questions"].append({
            "priority": "medium",
            "question": f"{name}的前任是谁？前任的去向？",
            "why_it_matters": "前任-继任关系是重要的网络边",
            "suggested_queries": [
                "海州区前任区委书记",
                "海州区前任区长",
                "阜新市海州区领导历史",
            ],
            "last_attempted": AS_OF,
        })

    return person


def write_person_json(person_id: int):
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    role_label = p["current_post"]
    safe_role = role_label.replace("、", "_").replace("，", "_")
    filename = f"{TODAY}-辽宁省-阜新市-{safe_role}-{name}.json"
    path = PJSON_DIR / filename

    person_data = build_person_json(person_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(person_data, f, ensure_ascii=False, indent=2)

    return path


# ── Main ─────────────────────────────────────────────────────────────────────


def main():
    # Build DB and GEXF
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
    person_files = []
    for pid in [1001, 1002]:
        path = write_person_json(pid)
        person_files.append(str(path))

    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Person JSONs:")
    for pf in person_files:
        print(f"  {pf}")
    print(f"Done.")


if __name__ == "__main__":
    main()
