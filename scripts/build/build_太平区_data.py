#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 太平区, 阜新市, 辽宁省.

Usage:
    python3 build_太平区_data.py
    python3 scripts/build/build_太平区_data.py

Investigation date: 2026-08-06
Task ID: liaoning_太平区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - fxtp.gov.cn — 太平区人民政府官方网站 (www.fxtp.gov.cn)
  - www.fxtp.gov.cn/channel/11373/index.html — 政府领导页面 (确认区长李亮及各位副区长)
  - www.fxtp.gov.cn/channel/22771/index.html — 区长李亮个人简历页 (出生1981.07, 研究生)
  - www.fxtp.gov.cn/content/2026/1085481.html — 2026-04-30 区政府领导分工通知 (确认郑晔、芦闯、许辉、芦阳、李海静、孙东兴分工)
  - www.fxtp.gov.cn/content/2026/1090150.html — 2026-07-14"区委书记邹亮"赴高德街道调研 (确认区委书记邹亮)
  - www.fxtp.gov.cn/content/2026/1096263.html — 2026-07-27芦闯洽谈电商项目 (区委常委、副区长)
  - www.fxtp.gov.cn/content/2026/1087788.html — 2026-05-29安全生产月会议 (区委常委、副区长郑晔主持)
  - www.fxtp.gov.cn/content/2026/1090361.html — 2026-07-16教育暑期安全会议 (副区长许辉主持)
  - www.fxtp.gov.cn/content/2026/1029679.html — 太平区2026年政府工作报告 (2025-12-24区长张雪峰作报告)
  - www.fuxin.gov.cn/content/2025/994436.html — 2025-06-23"太平区委书记邹亮、区长张雪峰" (确认前任搭档)
  - 新邱区调查 confirmation: 张雪峰 2026-02 调任新邱区委书记 (scripts/build/build_新邱区_data.py)

Key findings:
  - 邹亮: 现任区委书记 (2026-07-14官方新闻确认; 2025-06-23已任区委书记)
  - 李亮: 现任区长 (官方领导页确认, 男1981-07生, 汉族, 中共党员, 研究生)
  - 郑晔: 区委常委、副区长（负责日常工作, 即常务副区长）
  - 芦闯: 区委常委、副区长
  - 许辉/芦阳/李海静/孙善长/孙东兴: 副区长
  - 前任区长 张雪峰: 2025年任太平区长 → 2026-02 跨区调任新邱区委书记
  - 太平区属阜新市5区2县之一（海州、新邱、太平、清河门、细河、阜蒙县、彰武县）

Research limitations (web access degraded):
  - Exa API rate-limited (free tier exhausted)
  - Baidu/Baidu Baike: 403 captcha block
  - Bing/Jina Reader: timeout
  - 邹亮、李亮两人完整履历（出生地、此前任职）未从公开渠道获得，标注为 open_questions
  - 区委常委中纪委/组织/宣传/政法等部长名单未在官网列出

Confidence notes:
  - 邹亮区委书记身份: confirmed (2 independent官方新闻: 2025-06-23阜新市网 + 2026-07-14太平区网)
  - 李亮区长身份: confirmed (官方领导页个人简历 + 2026-04-30分工通知)
  - 各位副区长职务: confirmed (2026-04-30分工通知)
  - 张雪峰前任区长及去向: confirmed (新邱区官方新闻 2026-03-20 张雪峰任新邱区委书记)
"""

from __future__ import annotations

import json
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
SLUG = "太平区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "liaoning_太平区"
if _CURRENT_DIR.name == "liaoning_太平区":
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

FXTP_GOV_HOMEPAGE = "http://www.fxtp.gov.cn/"
LEADERSHIP_PAGE = "https://www.fxtp.gov.cn/channel/11373/index.html"
MAYOR_PAGE = "https://www.fxtp.gov.cn/channel/22771/index.html"
WORK_DIV_URL = "https://www.fxtp.gov.cn/content/2026/1085481.html"
ZOU_NEWS = "https://www.fxtp.gov.cn/content/2026/1090150.html"
LUCHUANG_NEWS = "https://www.fxtp.gov.cn/content/2026/1096263.html"
ZHENGYE_NEWS = "https://www.fxtp.gov.cn/content/2026/1087788.html"
XUHUI_NEWS = "https://www.fxtp.gov.cn/content/2026/1090361.html"
GOV_REPORT_2026 = "https://www.fxtp.gov.cn/content/2026/1029679.html"
FUXIN_TP_2025 = "https://www.fuxin.gov.cn/content/2025/994436.html"

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current) — CONFIRMED
    # ══════════════════════════════════════════════════════════════════════
    # 1. 邹亮 — 区委书记
    {
        "id": 1001,
        "name": "邹亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "太平区委书记",
        "current_org": "中共阜新市太平区委员会",
        "source": ZOU_NEWS,
        "confidence": "confirmed",
        "notes": "区委书记。2026-07-14深入高德街道调研指导基层治理、防汛、安全生产；2025-06-23（阜新市政府网）以太平区委书记身份与区长张雪峰推进功能涂料项目。",
    },
    # 2. 李亮 — 区委副书记、区长
    {
        "id": 1002,
        "name": "李亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-07",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "太平区区长",
        "current_org": "太平区人民政府",
        "source": MAYOR_PAGE,
        "confidence": "confirmed",
        "notes": "李亮，男，1981年07月生，汉族，中共党员，研究生学历。现任太平区委副书记、区人民政府党组书记、区长，主持区政府全面工作。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 区政府班子（区委常委、副区长）— CONFIRMED via 分工通知
    # ══════════════════════════════════════════════════════════════════════
    # 3. 郑晔 — 区委常委、常务副区长（负责日常工作）
    {
        "id": 1003,
        "name": "郑晔",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "太平区委常委、常务副区长",
        "current_org": "太平区人民政府",
        "source": WORK_DIV_URL,
        "confidence": "confirmed",
        "notes": "区委常委、副区长（负责区政府日常工作）。2026-04-30分工：负责发展改革、科技、财税、国资、金融、人社、应急管理、矿山安全、信访稳定、消防等工作；主持2026年安全生产月启动部署会。",
    },
    # 4. 芦闯 — 区委常委、副区长
    {
        "id": 1004,
        "name": "芦闯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "太平区委常委、副区长",
        "current_org": "太平区人民政府",
        "source": LUCHUANG_NEWS,
        "confidence": "confirmed",
        "notes": "区委常委、副区长。负责住建、民政、招商引资、外资外贸、农业农村、水利、交通等工作。2026-07-27赴岫岩洽谈电商产业项目；分管区住建局、区民政局、区商务局、区农业农村局。",
    },
    # 5. 许辉 — 副区长
    {
        "id": 1005,
        "name": "许辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "太平区副区长",
        "current_org": "太平区人民政府",
        "source": XUHUI_NEWS,
        "confidence": "confirmed",
        "notes": "副区长。负责教育、体育、文化、旅游、卫生、统计等工作。2026-07-16主持召开2026年教育领域暑假安全工作暨防范学生溺水工作会议。",
    },
    # 6. 芦阳 — 副区长、兼太平公安分局局长
    {
        "id": 1006,
        "name": "芦阳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "太平区副区长、太平公安分局局长",
        "current_org": "太平区人民政府",
        "source": WORK_DIV_URL,
        "confidence": "confirmed",
        "notes": "副区长、兼任太平公安分局局长，负责公安、司法、社会稳定等方面工作，协助负责消防和信访稳定。",
    },
    # 7. 李海静 — 副区长
    {
        "id": 1007,
        "name": "李海静",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "太平区副区长",
        "current_org": "太平区人民政府",
        "source": WORK_DIV_URL,
        "confidence": "confirmed",
        "notes": "副区长。负责工业、退役军人事务、市场监管、食品药品安全、质量监督、营商环境建设、策数据产业发展等。",
    },
    # 8. 孙善长 — 副区长
    {
        "id": 1008,
        "name": "孙善长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "太平区副区长",
        "current_org": "太平区人民政府",
        "source": LEADERSHIP_PAGE,
        "confidence": "confirmed",
        "notes": "副区长。2026-07-10赴长三角地区开展招商引资活动。",
    },
    # 9. 孙东兴 — 副区长
    {
        "id": 1009,
        "name": "孙东兴",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "太平区副区长",
        "current_org": "太平区人民政府",
        "source": WORK_DIV_URL,
        "confidence": "confirmed",
        "notes": "副区长。协助开展金融监督管理工作，协调联系驻区金融机构。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessor (前任)
    # ══════════════════════════════════════════════════════════════════════
    # 10. 张雪峰 — 前任区长（跨区调任新邱区委书记）
    {
        "id": 2001,
        "name": "张雪峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新邱区委书记（原太平区长）",
        "current_org": "中共新邱区委员会",
        "source": FUXIN_TP_2025,
        "confidence": "confirmed",
        "notes": "原太平区区长（约2021-2026-02），2025-12-24作太平区2026年政府工作报告；2026年2月左右调任新邱区委书记。跨区平级调动，属于阜新市县级干部交流。在任太平区长期间推进功能涂料项目、调研万达铸业等。",
    },
    # 11. 待查_纪委书记
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
        "current_post": "太平区委常委、纪委书记、监委主任",
        "current_org": "中共阜新市太平区纪律检查委员会",
        "source": "",
        "confidence": "unverified",
        "notes": "区委常委、纪委书记、区监委主任姓名待从官网确认。",
    },
    # 12. 待查—组织部长
    {
        "id": 1011,
        "name": "待查_组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "太平区委常委、组织部部长",
        "current_org": "中共阜新市太平区委组织部",
        "source": "",
        "confidence": "unverified",
        "notes": "区委常委、组织部部长姓名待确认。",
    },
    # 13. 待查—宣传部长
    {
        "id": 1012,
        "name": "待查_宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "太平区委常委、宣传部部长",
        "current_org": "中共阜新市太平区委宣传部",
        "source": "",
        "confidence": "unverified",
        "notes": "区委常委、宣传部部长姓名待确认。",
    },
    # 14. 待查—政法委书记
    {
        "id": 1013,
        "name": "待查_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "太平区委常委、政法委书记",
        "current_org": "中共阜新市太平区委政法委员会",
        "source": "",
        "confidence": "unverified",
        "notes": "区委常委、政法委书记姓名待确认。",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共阜新市太平区委员会", "type": "党委", "level": "县处级", "parent": "中共阜新市委", "location": "阜新市太平区"},
    {"id": 2, "name": "太平区人民政府", "type": "政府", "level": "县处级", "parent": "阜新市人民政府", "location": "阜新市太平区"},
    {"id": 3, "name": "阜新市太平区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "阜新市人大常委会", "location": "阜新市太平区"},
    {"id": 4, "name": "中国人民政治协商会议阜新市太平区委员会", "type": "政协", "level": "县处级", "parent": "政协阜新市委", "location": "阜新市太平区"},
    {"id": 5, "name": "中共阜新市太平区纪律检查委员会（监察委员会）", "type": "纪委", "level": "县处级", "parent": "阜新市纪委", "location": "阜新市太平区"},
    {"id": 6, "name": "中共阜新市太平区委组织部", "type": "党委", "level": "乡科级", "parent": "中共阜新市太平区委员会", "location": "阜新市太平区"},
    {"id": 7, "name": "中共阜新市太平区委宣传部", "type": "党委", "level": "乡科级", "parent": "中共阜新市太平区委员会", "location": "阜新市太平区"},
    {"id": 8, "name": "中共阜新市太平区委政法委员会", "type": "党委", "level": "乡科级", "parent": "中共阜新市太平区委员会", "location": "阜新市太平区"},
    {"id": 9, "name": "太平公安分局", "type": "政府", "level": "乡科级", "parent": "太平区人民政府", "location": "阜新市太平区"},
    {"id": 10, "name": "太平区审计局", "type": "政府", "level": "乡科级", "parent": "太平区人民政府", "location": "阜新市太平区"},
    {"id": 11, "name": "太平区发展和改革局", "type": "政府", "level": "乡科级", "parent": "太平区人民政府", "location": "阜新市太平区"},
    {"id": 12, "name": "太平区财政局", "type": "政府", "level": "乡科级", "parent": "太平区人民政府", "location": "阜新市太平区"},
    {"id": 13, "name": "太平区人力资源和社会保障局", "type": "政府", "level": "乡科级", "parent": "太平区人民政府", "location": "阜新市太平区"},
    {"id": 14, "name": "太平区应急管理局", "type": "政府", "level": "乡科级", "parent": "太平区人民政府", "location": "阜新市太平区"},
    {"id": 15, "name": "太平区住房和城乡建设局", "type": "政府", "level": "乡科级", "parent": "太平区人民政府", "location": "阜新市太平区"},
    {"id": 16, "name": "太平区民政局", "type": "政府", "level": "乡科级", "parent": "太平区人民政府", "location": "阜新市太平区"},
    {"id": 17, "name": "太平区商务局", "type": "政府", "level": "乡科级", "parent": "太平区人民政府", "location": "阜新市太平区"},
    {"id": 18, "name": "太平区农业农村局", "type": "政府", "level": "乡科级", "parent": "太平区人民政府", "location": "阜新市太平区"},
    {"id": 19, "name": "太平区教育局", "type": "政府", "level": "乡科级", "parent": "太平区人民政府", "location": "阜新市太平区"},
    {"id": 20, "name": "太平区卫生健康局", "type": "政府", "level": "乡科级", "parent": "太平区人民政府", "location": "阜新市太平区"},
    {"id": 21, "name": "太平区司法局", "type": "政府", "level": "乡科级", "parent": "太平区人民政府", "location": "阜新市太平区"},
    {"id": 22, "name": "太平区工业和信息化局", "type": "政府", "level": "乡科级", "parent": "太平区人民政府", "location": "阜新市太平区"},
    {"id": 23, "name": "太平区市场监督管理局", "type": "政府", "level": "乡科级", "parent": "太平区人民政府", "location": "阜新市太平区"},
    {"id": 24, "name": "太平区退役军人事务局", "type": "政府", "level": "乡科级", "parent": "太平区人民政府", "location": "阜新市太平区"},
    {"id": 25, "name": "中共新邱区委员会", "type": "党委", "level": "县处级", "parent": "中共阜新市委", "location": "阜新市新邱区"},
    {"id": 26, "name": "阜新市人民政府", "type": "政府", "level": "地厅级", "parent": "辽宁省人民政府", "location": "阜新市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 邹亮 — 区委书记
    {"id": 1, "person_id": 1001, "org_id": 1, "title": "太平区委书记", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "区委书记，主持区委全面工作。2026年7月官方新闻确认在任"},
    # 李亮 — 区委副书记、区长
    {"id": 2, "person_id": 1002, "org_id": 1, "title": "太平区委副书记", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "区长兼任区委副书记"},
    {"id": 3, "person_id": 1002, "org_id": 2, "title": "区长", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "主持区政府全面工作，分管区审计局，联系区人大、区政协、区法院、区检察院"},
    # 郑晔 — 区委常委、常务副区长
    {"id": 4, "person_id": 1003, "org_id": 1, "title": "太平区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"id": 5, "person_id": 1003, "org_id": 2, "title": "区委常委、常务副区长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "负责区政府日常工作；发改、科技、财税、国资国企、金融、人社、应急管理、矿山安全、信访稳定、消防等"},
    # 芦闯 — 区委常委、副区长
    {"id": 6, "person_id": 1004, "org_id": 1, "title": "太平区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"id": 7, "person_id": 1004, "org_id": 2, "title": "区委常委、副区长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "负责住建、民政、招商引资、外资外贸、农业农村、林业、乡村振兴、水利、交通等"},
    # 许辉 — 副区长
    {"id": 8, "person_id": 1005, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "负责教育、体育、文化、旅游、卫生、统计等；2026-07-16主持教育暑期安全工作会"},
    # 芦阳 — 副区长、兼公安分局局长
    {"id": 9, "person_id": 1006, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "兼任太平公安分局局长，负责公安、司法、社会稳定"},
    {"id": 10, "person_id": 1006, "org_id": 9, "title": "太平公安分局局长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "兼任太平公安分局局长"},
    # 李海静 — 副区长
    {"id": 11, "person_id": 1007, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "负责工业、退役军人事务、市场监管、营商环境、数据产业发展"},
    # 孙善长 — 副区长
    {"id": 12, "person_id": 1008, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "负责招商引资等工作，2026-07-10赴长三角开展招商"},
    # 孙东兴 — 副区长
    {"id": 13, "person_id": 1009, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "协助开展金融监督管理工作"},
    # 张雪峰 — 前任区长
    {"id": 14, "person_id": 2001, "org_id": 2, "title": "区长", "start_date": "2025", "end_date": "2026-02", "rank": "县处级正职",
     "note": "2025年任太平区长；2026-02调任新邱区委书记"},
    {"id": 15, "person_id": 2001, "org_id": 25, "title": "新邱区委书记", "start_date": "2026-02", "end_date": "", "rank": "县处级正职",
     "note": "跨区调任，接替刘昕"},
    # 待查 — 纪委书记
    {"id": 16, "person_id": 1010, "org_id": 1, "title": "太平区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"id": 17, "person_id": 1010, "org_id": 5, "title": "纪委书记、区监委主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "姓名待确认"},
    # 待查 — 组织部长
    {"id": 18, "person_id": 1011, "org_id": 1, "title": "太平区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"id": 19, "person_id": 1011, "org_id": 6, "title": "组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "姓名待确认"},
    # 待查 — 宣传部长
    {"id": 20, "person_id": 1012, "org_id": 1, "title": "太平区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"id": 21, "person_id": 1012, "org_id": 7, "title": "宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "姓名待确认"},
    # 待查 — 政法委书记
    {"id": 22, "person_id": 1013, "org_id": 1, "title": "太平区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"id": 23, "person_id": 1013, "org_id": 8, "title": "政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "姓名待确认"},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    # 党政正职搭档（confirmed）
    {"id": 1, "person_a": 1001, "person_b": 1002, "type": "党政搭档",
     "context": "邹亮（区委书记）与李亮（区长）为太平区现任党政正职搭档", "overlap_org": "太平区", "overlap_period": "当前", "confidence": "confirmed"},
    # 区长与前任搭档（confirmed）
    {"id": 2, "person_a": 1001, "person_b": 2001, "type": "predecessor_successor",
     "context": "邹亮（区委书记，继续留任）与张雪峰（原区长）为前任搭档；2026-02张雪峰调离太平", "overlap_org": "太平区", "overlap_period": "2025-2026-02", "confidence": "confirmed"},
    # 张雪峰 → 李亮（前任继任区长）
    {"id": 3, "person_a": 2001, "person_b": 1002, "type": "predecessor_successor",
     "context": "张雪峰（原太平区长）离职调任新邱区委书记，李亮接任太平区长", "overlap_org": "太平区人民政府", "overlap_period": "2026-02交接", "confidence": "confirmed"},
    # 区长与常务副区长郑晔
    {"id": 5, "person_a": 1002, "person_b": 1003, "type": "superior_subordinate",
     "context": "李亮（区长）与郑晔（常务副区长，负责日常工作）为上下级", "overlap_org": "太平区人民政府", "overlap_period": "当前", "confidence": "confirmed"},
    # 区长与区委常委、副区长芦闯
    {"id": 6, "person_a": 1002, "person_b": 1004, "type": "superior_subordinate",
     "context": "李亮（区长）与芦闯（区委常委、副区长）为上下级", "overlap_org": "太平区人民政府", "overlap_period": "当前", "confidence": "confirmed"},
    # 区长与副区长许辉
    {"id": 7, "person_a": 1002, "person_b": 1005, "type": "superior_subordinate",
     "context": "李亮（区长）与许辉（副区长）为上下级", "overlap_org": "太平区人民政府", "overlap_period": "当前", "confidence": "confirmed"},
    # 区长与副区长芦阳
    {"id": 8, "person_a": 1002, "person_b": 1006, "type": "superior_subordinate",
     "context": "李亮（区长）与芦阳（副区长兼公安局长）为上下级", "overlap_org": "太平区人民政府", "overlap_period": "当前", "confidence": "confirmed"},
    # 区长与副区长李海静
    {"id": 9, "person_a": 1002, "person_b": 1007, "type": "superior_subordinate",
     "context": "李亮（区长）与李海静（副区长）为上下级", "overlap_org": "太平区人民政府", "overlap_period": "当前", "confidence": "confirmed"},
    # 区长与副区长孙善长
    {"id": 10, "person_a": 1002, "person_b": 1008, "type": "superior_subordinate",
     "context": "李亮（区长）与孙善长（副区长）为上下级", "overlap_org": "太平区人民政府", "overlap_period": "当前", "confidence": "confirmed"},
    # 区长与副区长孙东兴
    {"id": 11, "person_a": 1002, "person_b": 1009, "type": "superior_subordinate",
     "context": "李亮（区长）与孙东兴（副区长）为上下级", "overlap_org": "太平区人民政府", "overlap_period": "当前", "confidence": "confirmed"},
    # 区委书记与人大主任 / 政协主席（无直接确认，跳过）
    # 常委相互（unverified — 因少数常委姓名待确认）
    {"id": 12, "person_a": 1003, "person_b": 1004, "type": "overlap",
     "context": "同任太平区委常委、副区长（郑晔、芦闯）", "overlap_org": "中共阜新市太平区委员会", "overlap_period": "当前", "confidence": "confirmed"},
    {"id": 13, "person_a": 1003, "person_b": 1010, "type": "overlap",
     "context": "同任太平区委常委班子", "overlap_org": "中共阜新市太平区委员会", "overlap_period": "当前", "confidence": "unverified"},
    {"id": 14, "person_a": 1003, "person_b": 1011, "type": "overlap",
     "context": "同任太平区委常委班子", "overlap_org": "中共阜新市太平区委员会", "overlap_period": "当前", "confidence": "unverified"},
    {"id": 15, "person_a": 1003, "person_b": 1012, "type": "overlap",
     "context": "同任太平区委常委班子", "overlap_org": "中共阜新市太平区委员会", "overlap_period": "当前", "confidence": "unverified"},
    {"id": 16, "person_a": 1003, "person_b": 1013, "type": "overlap",
     "context": "同任太平区委常委班子", "overlap_org": "中共阜新市太平区委员会", "overlap_period": "当前", "confidence": "unverified"},
]

# ── Person JSON Template ─────────────────────────────────────────────────────

PERSON_JSON_TEMPLATE = {
    "schema_version": "1.0",
    "generated_at": TODAY,
    "investigation_scope": {
        "province": "辽宁省",
        "city": "阜新市",
        "region": "太平区",
        "task_id": "liaoning_太平区",
        "time_focus": "2025-2026",
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


def _sources_for(p):
    """Build source register for a person based on its primary source URL."""
    url = p.get("source", "")
    if not url:
        return []
    s_type = "official" if "gov.cn" in url else "media"
    title = "太平区人民政府"
    if MAYOR_PAGE in url:
        title = "太平区人民政府-区长李亮"
    elif WORK_DIV_URL in url:
        title = "关于调整区政府班子成员工作分工的通知"
    elif ZOU_NEWS in url:
        title = "区委书记邹亮赴高德街道调研"
    elif LUCHUANG_NEWS in url:
        title = "芦闯赴岫岩洽谈笛尔逊电商产业园项目"
    elif ZHENGYE_NEWS in url:
        title = "太平区召开2026年安全生产月启动会议"
    elif XUHUI_NEWS in url:
        title = "太平区2026年教育领域暑假安全工作暨防范学生溺水工作会议"
    elif LEADERSHIP_PAGE in url:
        title = "太平区人民政府-政府领导"
    elif FUXIN_TP_2025 in url:
        title = "阜新市政府网-太平区委书记邹亮、区长张雪峰推进功能涂料项目"
    return [{
        "id": "S001",
        "title": title,
        "url": url,
        "publisher": "阜新市太平区人民政府",
        "published_at": AS_OF,
        "accessed_at": AS_OF,
        "source_type": s_type,
        "reliability": "high",
        "notes": "",
    }]


def build_person_json(person_id: int) -> dict:
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    role_label = p["current_post"]
    is_known = "待查" not in name
    is_core = person_id in [1001, 1002, 2001]
    rank = "县处级正职" if is_core else "县处级副职"
    system = "party" if person_id == 1001 else ("government" if is_known else "unknown")

    sources = _sources_for(p)

    person = {
        "identity": {
            "person_id": f"liaoning_fuxin_taiping_{name}",
            "name": name,
            "aliases": [],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "birthplace": p["birthplace"],
            "native_place": "",
            "education": [{
                "period": "",
                "institution": "",
                "major": "",
                "degree": p["education"],
                "study_type": "unknown",
                "source_ids": ["S001"] if sources else [],
            }] if p.get("education") else [],
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
            "career_pattern": "cross_county_rotation" if person_id == 2001 else "unknown",
            "systems_experience": ["party", "government"] if is_core else [],
            "geographic_pattern": ["太平区", "新邱区"] if person_id == 2001 else ["太平区"],
            "promotion_velocity": {
                "summary": "张雪峰：太平区长→新邱区委书记，跨区平级调动" if person_id == 2001 else "",
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
                "description": "截至2026年8月，未发现公开的纪律处分或负面报道（网页访问受限，覆盖有限）",
                "date": AS_OF,
                "confidence": "plausible" if is_known else "unverified",
                "source_ids": [],
            }
        ],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if is_core else ("plausible" if is_known else "unverified"),
            "current_role": "confirmed" if is_core else ("plausible" if is_known else "unverified"),
            "career_completeness": "thin",
            "relationship_confidence": "medium" if is_core else "low",
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
            "start": pos["start_date"] or "unknown",
            "end": pos["end_date"] or "present",
            "org": org_name,
            "title": pos["title"],
            "level": "",
            "location": "阜新市太平区",
            "system": system,
            "rank": pos["rank"],
            "is_key_promotion": bool(pos["start_date"] and pos["start_date"].startswith("2026") and pos["title"] == "新邱区委书记"),
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
            "person_id": f"liaoning_fuxin_taiping_{other_name}",
            "relationship_type": r["type"],
            "strength": "strong" if r["confidence"] == "confirmed" and is_core else ("medium" if r["confidence"] == "confirmed" else "weak"),
            "evidence": r["context"],
            "overlap_org": r["overlap_org"],
            "overlap_period": r["overlap_period"],
            "direction": "undirected",
            "confidence": r["confidence"],
        })

    # Governance records for core leaders
    if person_id == 1001:
        person["governance_record"].append({
            "period": "2026-07-14",
            "domain": "public_security",
            "achievement_or_event": "区委书记邹亮赴高德街道调研，查看汛期防汛隐患点位排查及人员转移，部署安全生产、矛盾纠纷化解、民生服务",
            "role_in_event": "调研部署",
            "measurable_outcome": "提出筑牢责任担当、强化大局意识、树立正确政绩观三点要求",
            "location": "太平区",
            "confidence": "confirmed",
            "source_ids": ["S001"] if sources else [],
        })
        person["work_style_and_personality"]["public_style_indicators"] = [
            {
                "trait": "grassroots_oriented",
                "evidence": "深入街道社区一线调研防汛、安全、民生，强调'多做打基础、利长远、惠民生的实事'",
                "confidence": "confirmed",
                "source_ids": ["S001"] if sources else [],
            }
        ]
        person["work_style_and_personality"]["speech_themes"] = ["正确政绩观", "基层治理", "安全生产", "民生实事"]
    elif person_id == 1002:
        person["governance_record"].append({
            "period": "2026-05-13",
            "domain": "economic_development",
            "achievement_or_event": "区长李亮会同市商务局领导赴企业洽谈食品产业、开展以商招商，推进啤酒科技产业园项目/雪树精酿精酿啤酒合作",
            "role_in_event": "牵头洽谈",
            "measurable_outcome": "推动食品/啤酒产业招商引资",
            "location": "太平区",
            "confidence": "plausible",
            "source_ids": [],
        })
        person["work_style_and_personality"]["public_style_indicators"] = [
            {
                "trait": "grassroots_oriented",
                "evidence": "区长李亮多次下基层进企业调研（粮食储备库、以商招商、啤酒项目洽谈）",
                "confidence": "plausible",
                "source_ids": [],
            }
        ]
    elif person_id == 2001:
        person["governance_record"].append({
            "period": "2025-12-24",
            "domain": "economic_development",
            "achievement_or_event": "以太平区区长身份在区十九届人大五次会议上作2026年政府工作报告，回顾'十四五'及2025年成绩",
            "role_in_event": "作报告",
            "measurable_outcome": "GDP年均增速4.4%，规上工业总产值259.9亿元，三次产业结构1:39:60",
            "location": "太平区",
            "confidence": "confirmed",
            "source_ids": ["S001"] if sources else [],
        })

    # Big gap
    if not is_known:
        person["confidence_summary"]["biggest_gap"] = "姓名尚未确认，全部个人信息缺失"
    elif not p.get("birth"):
        person["confidence_summary"]["biggest_gap"] = f"{name}的出生年月和完整履历未从官方网站获取"
    else:
        person["confidence_summary"]["biggest_gap"] = f"{name}除当前职务外的完整历史职务信息缺失"

    # Open questions
    if not is_known:
        person["open_questions"].append({
            "priority": "critical",
            "question": f"太平区{role_label}姓名及基本信息？",
            "why_it_matters": "核心职务人物，关系网络分析基础",
            "suggested_queries": [f"太平区 {role_label}", "阜新市委组织部任前公示", "太平区领导之窗"],
            "last_attempted": AS_OF,
        })
    elif not p.get("birth"):
        person["open_questions"].append({
            "priority": "high",
            "question": f"{name}的出生年月、籍贯、学历、入党时间、工作起点如何？",
            "why_it_matters": "核心人物身份信息用于去重与综合档案",
            "suggested_queries": [f"阜新市 {name} 简历", f"{name} 太平区 任前公示", f"{name} 出生年月"],
            "last_attempted": AS_OF,
        })
    if is_core:
        person["open_questions"].append({
            "priority": "high",
            "question": f"{name}在担任太平区职务前的履历，以及在太平区的历任职务？",
            "why_it_matters": "完整历史轨迹是关系网络与晋升路径分析基础",
            "suggested_queries": [f"阜新市 {name} 任职", f"{name} 调任 太平区", f"太平区 {name} 历史任职"],
            "last_attempted": AS_OF,
        })

    return person


def write_person_json(person_id: int):
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    safe_role = p["current_post"].replace("、", "_").replace("，", "_")
    filename = f"{TODAY}-辽宁省-阜新市-{safe_role}-{name}.json"
    path = PJSON_DIR / filename
    person_data = build_person_json(person_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(person_data, f, ensure_ascii=False, indent=2)
    return path


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
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
    for pid in [1001, 1002, 2001]:
        path = write_person_json(pid)
        person_files.append(str(path))

    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Person JSONs:")
    for pf in person_files:
        print(f"  {pf}")
    print("Done.")


if __name__ == "__main__":
    main()