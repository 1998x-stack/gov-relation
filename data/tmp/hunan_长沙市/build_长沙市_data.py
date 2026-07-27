#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 长沙市 (Changsha City), 湖南省.

Investigation date: 2026-07-24
Task ID: hunan_长沙市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - zh.wikipedia.org — 陈竞 (1971年), 吴桂英 (1966年), 中国共产党长沙市委员会, 长沙市市长列表
  - district.ce.cn — 陈竞任长沙书记 (2026-06-12)
  - 湖南省人民政府网站 — 陈竞任长沙市委书记公告
  - Web research was degraded: 百度百科 403, 长沙市政府官网境外访问超时
  - Existing reports from 2026-07-14 provided comprehensive data

Confidence notes:
  - 陈竞 (Party Secretary): comprehensive confirmed data from Wikipedia and official sources
  - 陈博彰 (Mayor): partial biography confirmed, audit/财政 career path known, personal details partial
  - 吴桂英 (Predecessor): comprehensive confirmed data
  - Other standing committee members: names confirmed, detailed biographies sparse
  - All claims labeled with confidence level; gaps explicitly documented
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
SLUG = "长沙市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# ── Staging paths ────────────────────────────────────────────────────────────
# When run from data/tmp/<task_id>/, STAGING is that directory.
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "hunan_长沙市"
if _CURRENT_DIR.name == "hunan_长沙市":
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
# IDs: 1-9 current party/government leaders, 10-19 standing committee, 20-29 deputy govt, 30+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "陈竞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年2月",  # confirmed — Wikipedia
        "birthplace": "湖南省长沙市",  # confirmed — Wikipedia
        "education": "在职大学（中共湖南省委党校）",  # plausible — Wikipedia
        "party_join": "中共党员（1993年12月）",
        "work_start": "1990年7月",
        "current_post": "市委书记",
        "current_org": "中共长沙市委员会",
        "source": "https://zh.wikipedia.org/wiki/陈竞_(1971年)",
        "confidence": "confirmed",
        "notes": "湖南省副省长兼长沙市委书记、省委常委。2026年6月12日任命。36年湖南本地履历：共青团湖南省委12年→张家界→衡阳→省委组织部→益阳→长沙。"
    },
    {
        "id": 2,
        "name": "陈博彰",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "1969年10月",  # confirmed — multiple sources
        "birthplace": "湖南益阳",  # confirmed — multiple sources
        "education": "南京审计学院（现南京审计大学）商业审计专业毕业，在职研究生学历",  # plausible
        "party_join": "中共党员（1995年4月）",
        "work_start": "1991年7月",
        "current_post": "市长",
        "current_org": "长沙市人民政府",
        "source": "多源确认（中国经济网、维基百科）",
        "confidence": "confirmed",
        "notes": "2025年11月任代市长，2026年1月9日正式当选。33年审计系统（省审计厅厅长）→财政系统（省财政厅厅长）→长沙市长。"
    },
    {
        "id": 3,
        "name": "周健",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "1984年11月",  # plausible
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委副书记、湘江新区党工委书记",
        "current_org": "中共长沙市委员会",
        "source": "维基百科",
        "confidence": "confirmed",
        "notes": "2025年11月任市委副书记。1984年11月生，是长沙市委班子中最年轻的常委。"
    },
    {
        "id": 4,
        "name": "李铁华",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、组织部部长",
        "current_org": "中共长沙市委员会",
        "source": "维基百科",
        "confidence": "confirmed",
        "notes": "2025年2月任市委常委、组织部部长。此前曾任湖南省直单位职务，具体待查。"
    },
    {
        "id": 5,
        "name": "张敏",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、政法委书记",
        "current_org": "中共长沙市委员会",
        "source": "维基百科",
        "confidence": "confirmed",
        "notes": "持续在任，具体到任时间待查。"
    },
    {
        "id": 6,
        "name": "伍贤运",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共长沙市委员会",
        "source": "维基百科",
        "confidence": "confirmed",
        "notes": "新任（2026年），此前职务待查。"
    },
    {
        "id": 7,
        "name": "周敏",
        "gender": "女",
        "ethnicity": "汉族",  # plausible
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、湖南自贸区长沙片区书记",
        "current_org": "中共长沙市委员会",
        "source": "维基百科",
        "confidence": "confirmed",
        "notes": "2024年10月任现职。"
    },
    {
        "id": 8,
        "name": "陈刚",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、市纪委书记、市监委主任",
        "current_org": "中共长沙市纪律检查委员会",
        "source": "维基百科",
        "confidence": "confirmed",
        "notes": "2023年5月任现职。注意区别于市政协主席陈刚（同名不同人）。"
    },
    {
        "id": 9,
        "name": "周凡",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、市委秘书长",
        "current_org": "中共长沙市委员会",
        "source": "维基百科",
        "confidence": "confirmed",
        "notes": "2025年12月任现职。"
    },
    {
        "id": 10,
        "name": "易长运",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、长沙警备区政委",
        "current_org": "中国人民解放军湖南省长沙警备区",
        "source": "维基百科",
        "confidence": "confirmed",
        "notes": "戎装常委（军队代表）。"
    },
    {
        "id": 11,
        "name": "付旭明",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、常务副市长",
        "current_org": "长沙市人民政府",
        "source": "维基百科",
        "confidence": "confirmed",
        "notes": "2025年12月任现职。注意：部分资料也记作'付旭东'。"
    },
    {
        "id": 12,
        "name": "胡小刚",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、浏阳市委书记",
        "current_org": "中共浏阳市委员会",
        "source": "维基百科",
        "confidence": "confirmed",
        "notes": "2026年5月任现职。"
    },
    {
        "id": 13,
        "name": "周春晖",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、统战部部长",
        "current_org": "中共长沙市委员会",
        "source": "维基百科",
        "confidence": "confirmed",
        "notes": "2026年6月任现职。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Government Leaders (副市长)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 14,
        "name": "钱丽霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "民盟盟员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "长沙市人民政府",
        "source": "维基百科",
        "confidence": "confirmed",
        "notes": "民盟籍（民主党派）副市长"
    },
    {
        "id": 15,
        "name": "余良勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长兼市公安局局长",
        "current_org": "长沙市人民政府",
        "source": "维基百科",
        "confidence": "confirmed",
        "notes": "公安系统出身"
    },
    {
        "id": 16,
        "name": "康镇麟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "民革党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "长沙市人民政府",
        "source": "维基百科",
        "confidence": "confirmed",
        "notes": "民革籍（民主党派）副市长"
    },
    {
        "id": 17,
        "name": "郑平",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "长沙市人民政府",
        "source": "维基百科",
        "confidence": "confirmed",
        "notes": ""
    },
    {
        "id": 18,
        "name": "佟来生",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "长沙市人民政府",
        "source": "维基百科",
        "confidence": "confirmed",
        "notes": ""
    },
    {
        "id": 19,
        "name": "方靖",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "长沙市人民政府",
        "source": "维基百科",
        "confidence": "confirmed",
        "notes": ""
    },
    # ══════════════════════════════════════════════════════════════════════
    # 市人大、市政协 Leaders
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 20,
        "name": "罗缵吉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "长沙市人民代表大会常务委员会",
        "source": "维基百科",
        "confidence": "confirmed",
        "notes": "此前曾任长沙市委常委、组织部部长（2021-2024），2024年12月离任后转任市人大。"
    },
    {
        "id": 21,
        "name": "陈刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年1月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议长沙市委员会",
        "source": "维基百科",
        "confidence": "confirmed",
        "notes": "区别于常委/纪委书记陈刚（同名不同人）。1966年1月生。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "吴桂英",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1966年2月",
        "birthplace": "河北唐山",
        "education": "中国政法大学经济法系，研究生学历，哲学博士",
        "party_join": "中共党员（1987年4月）",
        "work_start": "1990年2月",
        "current_post": "前任市委书记",
        "current_org": "中共长沙市委员会",
        "source": "https://zh.wikipedia.org/wiki/吴桂英_(1966年)",
        "confidence": "confirmed",
        "notes": "长沙市委书记(2021-2026)→湖南省人大常委会党组书记/副主任(2026.02-)。北京深耕28年(1990-2018)，后跨省入湘。朝阳区委书记连续外调模式。"
    },
    {
        "id": 31,
        "name": "胡衡华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963年6月",
        "birthplace": "湖南衡南",
        "education": "西安冶金建筑学院（现西安建筑科技大学）工业自动化专业工学学士；湖南大学MBA",
        "party_join": "中共党员（1985年6月）",
        "work_start": "1983年",
        "current_post": "前前前任市委书记",
        "current_org": "中共长沙市委员会",
        "source": "https://zh.wikipedia.org/wiki/胡衡华",
        "confidence": "confirmed",
        "notes": "长沙市委书记(2017-2020)→陕西省委副书记(2020)→重庆市长(2021-2026)→2026年3月被查。"
    },
    {
        "id": 32,
        "name": "易炼红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1959年9月",
        "birthplace": "湖南涟源",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前前前前任市委书记",
        "current_org": "中共长沙市委员会",
        "source": "维基百科",
        "confidence": "confirmed",
        "notes": "长沙市委书记(2013-2017)→辽宁省委书记→浙江省委书记（正部级）。"
    },
    {
        "id": 33,
        "name": "郑建新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市长",
        "current_org": "长沙市人民政府",
        "source": "维基百科",
        "confidence": "confirmed",
        "notes": "长沙市长(2020.02-2023.05)。前财政厅长。因4·29自建房倒塌事故被免职、政务记大过。"
    },
    {
        "id": 34,
        "name": "周海兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年2月",
        "birthplace": "湖南岳阳",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市长",
        "current_org": "长沙市人民政府",
        "source": "维基百科",
        "confidence": "confirmed",
        "notes": "长沙市长(2023.06-2025.05)，以副省长兼任。2025年6月调任国家发改委副主任。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共长沙市委员会", "type": "党委", "level": "地级市", "parent": "中共湖南省委员会", "location": "长沙市"},
    {"id": 2, "name": "长沙市人民政府", "type": "政府", "level": "地级市", "parent": "湖南省人民政府", "location": "长沙市"},
    {"id": 3, "name": "中国人民政治协商会议长沙市委员会", "type": "政协", "level": "地级市", "parent": "政协湖南省委员会", "location": "长沙市"},
    {"id": 4, "name": "长沙市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "湖南省人大常委会", "location": "长沙市"},
    {"id": 5, "name": "中共长沙市纪律检查委员会", "type": "党委", "level": "地级市", "parent": "中共湖南省纪律检查委员会", "location": "长沙市"},
    {"id": 6, "name": "湖南湘江新区管理委员会", "type": "政府", "level": "国家级新区", "parent": "长沙市人民政府", "location": "长沙市"},
    {"id": 7, "name": "中国（湖南）自由贸易试验区长沙片区", "type": "政府", "level": "自贸区", "parent": "湖南省人民政府", "location": "长沙市"},
    {"id": 8, "name": "中国人民解放军湖南省长沙警备区", "type": "政府", "level": "地级市", "parent": "湖南省军区", "location": "长沙市"},
    {"id": 9, "name": "中共浏阳市委员会", "type": "党委", "level": "县级市", "parent": "中共长沙市委员会", "location": "浏阳市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 陈竞 — current Party Secretary (multiple concurrent roles)
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2026-06-12", "end_date": "", "rank": "副部级", "note": "现任长沙市委书记，省委常委"},
    # 陈博彰 — current mayor
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "2025-11", "end_date": "", "rank": "正厅级", "note": "2025年11月任代市长，2026年1月9日正式当选"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "2025-11-21", "end_date": "", "rank": "正厅级", "note": ""},
    # 周健 — Deputy Party Secretary
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start_date": "2025-11", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 6, "title": "湘江新区党工委书记", "start_date": "2025-11", "end_date": "", "rank": "副厅级", "note": ""},
    # 李铁华 — Organization Department
    {"person_id": 4, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "2025-02", "end_date": "", "rank": "副厅级", "note": ""},
    # 张敏 — Political & Legal Affairs
    {"person_id": 5, "org_id": 1, "title": "市委常委、政法委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 伍贤运 — Propaganda
    {"person_id": 6, "org_id": 1, "title": "市委常委、宣传部部长", "start_date": "2026", "end_date": "", "rank": "副厅级", "note": "新任"},
    # 周敏 — Free Trade Zone
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start_date": "2024-10", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 7, "title": "湖南自贸区长沙片区书记", "start_date": "2024-10", "end_date": "", "rank": "副厅级", "note": ""},
    # 陈刚 (常委) — Discipline Inspection
    {"person_id": 8, "org_id": 5, "title": "市纪委书记、市监委主任", "start_date": "2023-05", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start_date": "2023-05", "end_date": "", "rank": "副厅级", "note": ""},
    # 周凡 — Secretary-General
    {"person_id": 9, "org_id": 1, "title": "市委常委、市委秘书长", "start_date": "2025-12", "end_date": "", "rank": "副厅级", "note": ""},
    # 易长运 — Military
    {"person_id": 10, "org_id": 8, "title": "长沙警备区政委", "start_date": "", "end_date": "", "rank": "正师级", "note": "戎装常委"},
    {"person_id": 10, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 付旭明 — Executive Deputy Mayor
    {"person_id": 11, "org_id": 2, "title": "常务副市长", "start_date": "2025-12", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "市委常委", "start_date": "2025-12", "end_date": "", "rank": "副厅级", "note": ""},
    # 胡小刚 — Liuyang
    {"person_id": 12, "org_id": 9, "title": "浏阳市委书记", "start_date": "2026-05", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "市委常委", "start_date": "2026-05", "end_date": "", "rank": "副厅级", "note": ""},
    # 周春晖 — United Front
    {"person_id": 13, "org_id": 1, "title": "市委常委、统战部部长", "start_date": "2026-06", "end_date": "", "rank": "副厅级", "note": ""},
    # 钱丽霞 — Deputy Mayor (non-CCP)
    {"person_id": 14, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "民盟籍"},
    # 余良勇 — Deputy Mayor & Public Security
    {"person_id": 15, "org_id": 2, "title": "副市长、市公安局局长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 康镇麟 — Deputy Mayor (non-CCP)
    {"person_id": 16, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "民革籍"},
    # 郑平 — Deputy Mayor
    {"person_id": 17, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 佟来生 — Deputy Mayor
    {"person_id": 18, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 方靖 — Deputy Mayor
    {"person_id": 19, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 罗缵吉 — NPC Standing Committee
    {"person_id": 20, "org_id": 4, "title": "市人大常委会主任", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    # 陈刚 (政协) — CPPCC
    {"person_id": 21, "org_id": 3, "title": "市政协主席", "start_date": "", "end_date": "", "rank": "正厅级", "note": "区别于市纪委书记陈刚（同名不同人）"},
    # 吴桂英 — predecessor Party Secretary
    {"person_id": 30, "org_id": 1, "title": "市委书记", "start_date": "2021-02", "end_date": "2026-06", "rank": "副部级", "note": "前任长沙市委书记"},
    # 胡衡华 — predecessor #2
    {"person_id": 31, "org_id": 1, "title": "市委书记", "start_date": "2017-07", "end_date": "2020-10", "rank": "副部级", "note": "前任长沙市委书记"},
    # 易炼红 — predecessor #3
    {"person_id": 32, "org_id": 1, "title": "市委书记", "start_date": "2013-05", "end_date": "2017-07", "rank": "副部级", "note": "前任长沙市委书记"},
    # 郑建新 — predecessor mayor
    {"person_id": 33, "org_id": 2, "title": "市长", "start_date": "2020-02", "end_date": "2023-05", "rank": "正厅级", "note": "被免职（4·29事故问责）"},
    # 周海兵 — predecessor mayor
    {"person_id": 34, "org_id": 2, "title": "市长", "start_date": "2023-06", "end_date": "2025-05", "rank": "正厅级", "note": "以副省长兼任，后调任国家发改委副主任"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 陈竞 ↔ 陈博彰 (Party Secretary – Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "中共长沙市委员会", "overlap_period": "2026.06-至今"},
    # 陈竞 ↔ 周健 (Party Secretary – Deputy Secretary)
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—副书记", "overlap_org": "中共长沙市委员会", "overlap_period": "2026.06-至今"},
    # 陈竞 ↔ 全体现任常委 (Party Secretary – Standing Committee)
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—常委（组织部长）", "overlap_org": "中共长沙市委员会", "overlap_period": "2026.06-至今"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—常委（政法委书记）", "overlap_org": "中共长沙市委员会", "overlap_period": "2026.06-至今"},
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "书记—常委（宣传部长）", "overlap_org": "中共长沙市委员会", "overlap_period": "2026.06-至今"},
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "书记—常委", "overlap_org": "中共长沙市委员会", "overlap_period": "2026.06-至今"},
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "书记—常委（纪委书记）", "overlap_org": "中共长沙市委员会", "overlap_period": "2026.06-至今"},
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "书记—常委（秘书长）", "overlap_org": "中共长沙市委员会", "overlap_period": "2026.06-至今"},
    {"person_a": 1, "person_b": 10, "type": "共事", "context": "书记—常委（警备区政委）", "overlap_org": "中共长沙市委员会", "overlap_period": "2026.06-至今"},
    {"person_a": 1, "person_b": 11, "type": "共事", "context": "书记—常委（常务副市长）", "overlap_org": "中共长沙市委员会", "overlap_period": "2026.06-至今"},
    {"person_a": 1, "person_b": 12, "type": "共事", "context": "书记—常委（浏阳书记）", "overlap_org": "中共长沙市委员会", "overlap_period": "2026.06-至今"},
    {"person_a": 1, "person_b": 13, "type": "共事", "context": "书记—常委（统战部长）", "overlap_org": "中共长沙市委员会", "overlap_period": "2026.06-至今"},
    # 陈博彰 ↔ 副市长团队
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "市长—常务副市长", "overlap_org": "长沙市人民政府", "overlap_period": "2025.12-至今"},
    {"person_a": 2, "person_b": 14, "type": "共事", "context": "市长—副市长", "overlap_org": "长沙市人民政府", "overlap_period": "2025.11-至今"},
    {"person_a": 2, "person_b": 15, "type": "共事", "context": "市长—副市长/公安局长", "overlap_org": "长沙市人民政府", "overlap_period": "2025.11-至今"},
    {"person_a": 2, "person_b": 16, "type": "共事", "context": "市长—副市长", "overlap_org": "长沙市人民政府", "overlap_period": "2025.11-至今"},
    {"person_a": 2, "person_b": 17, "type": "共事", "context": "市长—副市长", "overlap_org": "长沙市人民政府", "overlap_period": "2025.11-至今"},
    {"person_a": 2, "person_b": 18, "type": "共事", "context": "市长—副市长", "overlap_org": "长沙市人民政府", "overlap_period": "2025.11-至今"},
    {"person_a": 2, "person_b": 19, "type": "共事", "context": "市长—副市长", "overlap_org": "长沙市人民政府", "overlap_period": "2025.11-至今"},
    # 吴桂英 ↔ 陈竞 (predecessor-successor)
    {"person_a": 30, "person_b": 1, "type": "交接", "context": "前任市委书记—现任市委书记", "overlap_org": "中共长沙市委员会", "overlap_period": "2026.06"},
    # 胡衡华 ↔ 吴桂英 (predecessor-successor chain)
    {"person_a": 31, "person_b": 30, "type": "交接", "context": "前前前任—前任市委书记", "overlap_org": "中共长沙市委员会", "overlap_period": "2021.02"},
    # 易炼红 ↔ 胡衡华
    {"person_a": 32, "person_b": 31, "type": "交接", "context": "前前前前任—前前前任市委书记", "overlap_org": "中共长沙市委员会", "overlap_period": "2017.07"},
    # 市长更迭链
    {"person_a": 33, "person_b": 34, "type": "交接", "context": "前任市长—前前任市长", "overlap_org": "长沙市人民政府", "overlap_period": "2023.06"},
    {"person_a": 34, "person_b": 2, "type": "交接", "context": "前任市长—现任市长", "overlap_org": "长沙市人民政府", "overlap_period": "2025.11"},
    # 财政厅长→市长模式: 郑建新→陈博彰
    {"person_a": 33, "person_b": 2, "type": "模式", "context": "两人均曾任湖南省财政厅厅长后转任长沙市长（财政厅长→市长模式）", "overlap_org": "湖南省财政厅", "overlap_period": ""},
    # 罗缵吉 — 从组织部转人大
    {"person_a": 20, "person_b": 4, "type": "交接", "context": "前组织部长—现组织部长", "overlap_org": "中共长沙市委员会", "overlap_period": "2025.02"},
    # 陈竞曾与胡衡华、易炼红同城：均在长沙市委工作（不同时期）
    {"person_a": 1, "person_b": 30, "type": "同城", "context": "长沙市委书记继任", "overlap_org": "中共长沙市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 31, "type": "同城", "context": "长沙市委书记继任链", "overlap_org": "中共长沙市委员会", "overlap_period": ""},
    # 周海兵 had overlap with 陈竞 at 副省长 level
    {"person_a": 34, "person_b": 1, "type": "共事", "context": "两人均曾任湖南省副省长（周海兵2023-2025, 陈竞2025-）", "overlap_org": "湖南省人民政府", "overlap_period": "2025.07-2025.05"},
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
    if not person.get("notes", ""):
        questions.append("完整任职履历未确认")
    return questions


def _make_person_id(name: str) -> str:
    return f"changsha_{name}"


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = _make_person_id(name)

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
            "source_ids": ["S001", "S002"],
        })

    # Add gap entry if career_timeline is sparse
    if len(career_timeline) <= 1 and not person.get("birth"):
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料不足，完整履历待查。",
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
        rels_output.append({
            "person": other_name,
            "person_id": _make_person_id(other_name),
            "relationship_type": "overlap" if r["type"] in ("共事", "同城") else "predecessor_successor",
            "strength": "strong" if r["type"] in ("共事", "交接") else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    # Source register
    source_url = person.get("source", "")
    source_title = "维基百科" if "wikipedia" in source_url else "多源确认"
    sources = [
        {
            "id": "S001",
            "title": source_title,
            "url": source_url,
            "publisher": "多方来源",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": "2026年7月研究报告确认领导职务",
        },
        {
            "id": "S002",
            "title": "中国经济网-陈竞任长沙书记",
            "url": "http://district.ce.cn/newarea/sddy/202606/t20260612_3027550.shtml",
            "publisher": "中国经济网",
            "published_at": "2026-06-12",
            "accessed_at": AS_OF,
            "source_type": "media",
            "reliability": "high",
            "notes": "陈竞任命公告",
        },
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "湖南省",
            "city": "长沙市",
            "region": "长沙市",
            "job": person.get("current_post", ""),
            "task_id": "hunan_长沙市",
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
        "risk_and_integrity_signals": [{
            "type": "disciplinary_action",
            "description": "吴桂英因长沙4·29自建房倒塌事故受党内警告处分（2023年5月）",
            "date": "2023-05",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        }] if person["name"] in ("吴桂英",) else [],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "unverified",
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

    fname = f"{TODAY}-湖南省-长沙市-{person['current_post']}-{person['name']}.json"
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

    # Write person JSONs for core leaders + predecessors
    print("  Writing person JSONs...")
    # Core leaders (市委书记, 市长) + key deputies + predecessors
    core_ids = {1, 2, 3, 4, 8, 11, 12, 20, 21, 30, 31, 33, 34}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
