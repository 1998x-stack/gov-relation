#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 彭阳县 (Pengyang County), 固原市, 宁夏回族自治区.

Investigation date: 2026-08-07
Task ID: ningxia_彭阳县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - Official county government website (www.pengyang.gov.cn) leadership pages (领导之窗)
    were directly accessible (HTTP 200).
  - Current leadership roster and individual profiles confirmed from official pages.
  - Exa search API was rate-limited; Baidu was not used. Reliance on primary gov source.

Key leadership (current, as of 2026-07):
  - 宋亚俊 — 县委书记 (男，汉族，1976-10，宁夏党校研究生)
  - 张翼 — 县委副书记、县长 (男，汉族，1982-04，研究生)
  - 陈淑重 — 县委副书记、政府党组副书记、副县长 (1985-12)
  - 倪金栋 — 县委副书记、政法委书记、党校校长 (1982-02)
  - 伍福升 — 县委常委、县政府党组副书记、副县长 (回族，1986-02)
  - 崔丽菲 — 县委常委、副县长 (女，1986-09)
  - 田野 — 县委常委、副县长 (1984-07)
  - 罗金彩 — 副县长 (女，1977-05)
  - 叶永禄、马占兵 — 副县长提名人选 (2026-07)
  - 人大主任 何少庸；政协主席 马文山

Confidence notes (following source_fallbacks.md partial-evidence mode):
  - Current roles: CONFIRMED from official profiles (primary source).
  - Predecessors (前任书记/前任县长) of 宋亚俊/张翼: UNVERIFIED — full timeline before
    current tenure and prior officeholders not individually documented in this session.
  - Deputies' early careers / full timelines: UNVERIFIED — only current profile available.
  - Standing committee members 李国栋/李志强/单国典/杨洁/安金国: listed on roster but
    individual 分工 profiles not retrieved — careers mostly unverified.
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
SLUG = "彭阳县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

# ── Staging paths ─────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "ningxia_彭阳县"
if _CURRENT_DIR.name == "ningxia_彭阳县":
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
        "title": "彭阳县领导之窗（县委、县政府、人大、政协）",
        "url": "https://www.pengyang.gov.cn/xxgk_13872/ldzc/",
        "note": "汇总页：县委书记宋亚俊、县长张翼及全体班子成员列表",
    },
    "S002": {
        "title": "宋亚俊 profile — 县委书记",
        "url": "https://www.pengyang.gov.cn/xxgk_13872/ldzc/zgpyxwyh/202102/t20210210_2598745.html",
        "note": "男，汉族，1976年10月出生，宁夏党校研究生学历",
    },
    "S003": {
        "title": "张翼 profile — 县长",
        "url": "https://www.pengyang.gov.cn/xxgk_13872/ldzc/pyxrmzf/201708/t20170815_435141.html",
        "note": "男，汉族，1982年4月出生，研究生学历；县委副书记、政府党组书记、县长、王洼产业园区工委书记",
    },
    "S004": {
        "title": "陈淑重 profile — 县委副书记/副县长",
        "url": "https://www.pengyang.gov.cn/xxgk_13872/ldzc/zgpyxwyh/202312/t20231205_4373915.html",
        "note": "男，汉族，1985年12月出生，大学学历，闽宁协作分工",
    },
    "S005": {
        "title": "倪金栋 profile — 县委副书记、政法委书记",
        "url": "https://www.pengyang.gov.cn/xxgk_13872/ldzc/zgpyxwyh/201811/t20181122_1176905.html",
        "note": "男，汉族，1982年2月出生，大学学历，政法、农业农村、乡村振兴"
    },
    "S006": {
        "title": "伍福升 profile — 县委常委/副县长",
        "url": "https://www.pengyang.gov.cn/xxgk_13872/ldzc/zgpyxwyh/202108/t20210829_2995409.html",
        "note": "男，回族，1986年2月出生，政府党组副书记",
    },
    "S007": {
        "title": "崔丽菲 profile — 县委常委/副县长",
        "url": "https://www.pengyang.gov.cn/xxgk_13872/ldzc/zgpyxwyh/202408/t20240809_4619405.html",
        "note": "女，汉族，1986年9月出生，在职硕士研究生",
    },
    "S008": {
        "title": "田野 profile — 县委常委/副县长",
        "url": "https://www.pengyang.gov.cn/xxgk_13872/ldzc/zgpyxwyh/202607/t20260731_5303212.html",
        "note": "男，汉族，1984年7月出生，大学学历",
    },
    "S009": {
        "title": "罗金彩 profile — 副县长",
        "url": "https://www.pengyang.gov.cn/xxgk_13872/ldzc/pyxrmzf/202606/t20260618_5269212.html",
        "note": "女，汉族，1977年5月出生，在职大学学历",
    },
    "S010": {
        "title": "叶永禄副县长提名人选",
        "url": "https://www.pengyang.gov.cn/xxgk_13872/ldzc/pyxrmzf/202607/t20260731_5303113.html",
        "note": "2026-07 提名为副县长候选人",
    },
    "S011": {
        "title": "马占兵副县长提名人选",
        "url": "https://www.pengyang.gov.cn/xxgk_13872/ldzc/pyxrmzf/202607/t20260731_5303122.html",
        "note": "2026-07 提名为副县长候选人",
    },
    "S012": {
        "title": "何少庸 人大主任 profile",
        "url": "https://www.pengyang.gov.cn/xxgk_13872/ldzc/pyxrdcwh/201708/t20170815_435121.html",
        "note": "县人大常委会主任",
    },
    "S013": {
        "title": "马文山 政协主席 profile",
        "url": "https://www.pengyang.gov.cn/xxgk_13872/ldzc/zxpyxwyh/202108/t20210830_2997005.html",
        "note": "政协彭阳县委员会主席",
    },
}


# ── Persons ────────────────────────────────────────────────────────────
# Core leadership confirmed; 常委 in circulation without profile bio marked as gap placeholders.
persons = [
    # ══════ 核心领导 (Current Core) ══════
    {
        "id": 1,
        "name": "宋亚俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-10",
        "birthplace": "",
        "education": "宁夏党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "彭阳县委书记",
        "current_org": "中国共产党彭阳县委员会",
        "source": "S002: 男，汉族，1976年10月出生，宁夏党校研究生学历，现任中共彭阳县委书记",
    },
    {
        "id": 2,
        "name": "张翼",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-04",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "彭阳县委副书记、县长",
        "current_org": "彭阳县人民政府",
        "source": "S003: 男，汉族，1982年4月出生，研究生学历；县委副书记、政府党组书记、县长、王洼产业园区工委书记",
    },
    # ══════ 领导班子成员 (Leadership Team) ══════
    {
        "id": 3,
        "name": "陈淑重",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-12",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "彭阳县委副书记、政府党组副书记、副县长",
        "current_org": "中国共产党彭阳县委员会",
        "source": "S004",
    },
    {
        "id": 4,
        "name": "倪金栋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-02",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "彭阳县委副书记、政法委书记、党校校长",
        "current_org": "中国共产党彭阳县委员会",
        "source": "S005",
    },
    {
        "id": 5,
        "name": "伍福升",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1986-02",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "彭阳县委常委、县政府党组副书记、副县长",
        "current_org": "彭阳县人民政府",
        "source": "S006",
    },
    {
        "id": 6,
        "name": "崔丽菲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1986-09",
        "birthplace": "",
        "education": "在职硕士研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "彭阳县委常委、副县长",
        "current_org": "彭阳县人民政府",
        "source": "S007",
    },
    {
        "id": 7,
        "name": "田野",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-07",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "彭阳县委常委、副县长",
        "current_org": "彭阳县人民政府",
        "source": "S008",
    },
    {
        "id": 8,
        "name": "罗金彩",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977-05",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "",
        "work_start": "",
        "current_post": "彭阳县副县长",
        "current_org": "彭阳县人民政府",
        "source": "S009",
    },
    {
        "id": 9,
        "name": "叶永禄",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "彭阳县副县长提名人选",
        "current_org": "彭阳县人民政府",
        "source": "S010: 2026-07 提名为副县长候选人",
    },
    {
        "id": 10,
        "name": "马占兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "彭阳县副县长提名人选",
        "current_org": "彭阳县人民政府",
        "source": "S011: 2026-07 提名为副县长候选人",
    },
    {
        "id": 11,
        "name": "何少庸",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "彭阳县人大常委会主任",
        "current_org": "彭阳县人民代表大会常务委员会",
        "source": "S012",
    },
    {
        "id": 12,
        "name": "马文山",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "政协彭阳县委员会主席",
        "current_org": "政协彭阳县委员会",
        "source": "S013",
    },
    # ══ 县委常委会其他成员 (roster only, no bio/profile) ══
    {
        "id": 13,
        "name": "待查_李国栋",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "彭阳县委常委",
        "current_org": "中国共产党彭阳县委员会",
        "source": "S001: 领导之窗列出为县委常委（未获取个人分工/简历）",
    },
    {
        "id": 14,
        "name": "待查_李志强",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "彭阳县委常委",
        "current_org": "中国共产党彭阳县委员会",
        "source": "S001: 领导之窗列出为县委常委（未获取个人分工/简历）",
    },
    {
        "id": 15,
        "name": "待查_单国典",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "彭阳县委常委",
        "current_org": "中国共产党彭阳县委员会",
        "source": "S001: 领导之窗列出为县委常委（未获取个人分工/简历）",
    },
    {
        "id": 16,
        "name": "待查_杨洁",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "彭阳县委常委",
        "current_org": "中国共产党彭阳县委员会",
        "source": "S001: 领导之窗列出为县委常委（未获取个人分工/简历）",
    },
    {
        "id": 17,
        "name": "待查_安金国",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "彭阳县委常委",
        "current_org": "中国共产党彭阳县委员会",
        "source": "S001: 领导之窗列出为县委常委（未获取个人分工/简历）",
    },
]


# ── Organizations ──────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中国共产党彭阳县委员会", "type": "党委",
     "level": "县处级", "parent": "中国共产党固原市委员会",
     "location": "宁夏回族自治区固原市彭阳县"},
    {"id": 2, "name": "彭阳县人民政府", "type": "政府",
     "level": "县处级", "parent": "固原市人民政府",
     "location": "宁夏回族自治区固原市彭阳县"},
    {"id": 3, "name": "中共彭阳县委政法委员会", "type": "党委",
     "level": "县处级", "parent": "中国共产党彭阳县委员会",
     "location": "宁夏回族自治区固原市彭阳县"},
    {"id": 4, "name": "彭阳县委党校", "type": "党委",
     "level": "县处级", "parent": "中国共产党彭阳县委员会",
     "location": "宁夏回族自治区固原市彭阳县"},
    {"id": 5, "name": "彭阳县人民代表大会常务委员会", "type": "人大",
     "level": "县处级", "parent": "固原市人民代表大会常务委员会",
     "location": "宁夏回族自治区固原市彭阳县"},
    {"id": 6, "name": "政协彭阳县委员会", "type": "政协",
     "level": "县处级", "parent": "政协固原市委员会",
     "location": "宁夏回族自治区固原市彭阳县"},
    {"id": 7, "name": "王洼产业园区管理委员会", "type": "开发区",
     "level": "县级", "parent": "彭阳县人民政府",
     "location": "宁夏回族自治区固原市彭阳县"},
]


# ── Positions ──────────────────────────────────────────────────────────
positions = [
    # 宋亚俊 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "彭阳县委书记",
     "start_date": "不详", "end_date": "present",
     "rank": "正处级",
     "note": "主持县委全面工作，联系人大常委会、政协彭阳县委员会和县人武部"},
    # 张翼 — 县长
    {"person_id": 2, "org_id": 1, "title": "彭阳县委副书记",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "与县长职务同步（县长为政府一把手）"},
    {"person_id": 2, "org_id": 2, "title": "彭阳县委副书记、县长",
     "start_date": "", "end_date": "present",
     "rank": "正处级",
     "note": "县政府党组书记；负责审计工作"},
    {"person_id": 2, "org_id": 7, "title": "王洼产业园区工委书记",
     "start_date": "", "end_date": "present", "rank": "", "note": "县长兼任"},
    # 陈淑重
    {"person_id": 3, "org_id": 1, "title": "彭阳县委副书记",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "政府党组副书记，兼任副县长"},
    {"person_id": 3, "org_id": 2, "title": "副县长（政府党组副书记）",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "闽宁协作分工，配合倪金栋抓农业/乡村振兴"},
    # 倪金栋
    {"person_id": 4, "org_id": 1, "title": "彭阳县委副书记",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "协助书记处理县委日常工作"},
    {"person_id": 4, "org_id": 3, "title": "县委政法委书记",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "平安建设、信访维稳、司法行政"},
    {"person_id": 4, "org_id": 4, "title": "县委党校校长",
     "start_date": "", "end_date": "present", "rank": "", "note": "党校校长"},
    # 伍福升
    {"person_id": 5, "org_id": 1, "title": "彭阳县委常委",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "县政府党组副书记、副县长",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 崔丽菲
    {"person_id": 6, "org_id": 1, "title": "彭阳县委常委",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "县政府党组成员、副县长",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 田野
    {"person_id": 7, "org_id": 1, "title": "彭阳县委常委",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "县政府党组成员、副县长",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 罗金彩
    {"person_id": 8, "org_id": 2, "title": "县政府党组成员、副县长",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 叶永禄 / 马占兵 (提名人选)
    {"person_id": 9, "org_id": 2, "title": "副县长（提名人选）",
     "start_date": "2026-07", "end_date": "", "rank": "副处级", "note": "提名人选"},
    {"person_id": 10, "org_id": 2, "title": "副县长（提名人选）",
     "start_date": "2026-07", "end_date": "", "rank": "副处级", "note": "提名人选"},
    # 人大 / 政协
    {"person_id": 11, "org_id": 5, "title": "彭阳县人大常委会主任",
     "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 12, "org_id": 6, "title": "政协彭阳县委员会主席",
     "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 常委 placeholders
    {"person_id": 13, "org_id": 1, "title": "彭阳县委常委",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 1, "title": "彭阳县委常委",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 1, "title": "彭阳县委常委",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 1, "title": "彭阳县委常委",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 1, "title": "彭阳县委常委",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
]


# ── Relationships ──────────────────────────────────────────────────────
relationships = [
    # 核心党政搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "宋亚俊（县委书记）与张翼（县委副书记、县长），彭阳县党政主要领导",
     "overlap_org": "中国共产党彭阳县委员会/彭阳县人民政府",
     "overlap_period": "现任"},
    # 书记 — 各副书记 / 常委（班子同僚）
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "宋亚俊（书记）与陈淑重（县委副书记、副县长）同为县委领导班子",
     "overlap_org": "中国共产党彭阳县委员会",
     "overlap_period": "现任"},
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "宋亚俊（书记）与倪金栋（县委副书记、政法委书记）协助书记处理县委日常工作",
     "overlap_org": "中国共产党彭阳县委员会",
     "overlap_period": "现任"},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "宋亚俊（书记）与伍福升（县委常委、副县长）同为县委常委会班子成员",
     "overlap_org": "中国共产党彭阳县委员会",
     "overlap_period": "现任"},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "宋亚俊（书记）与崔丽菲（县委常委、副县长）同为县委常委会班子成员",
     "overlap_org": "中国共产党彭阳县委员会",
     "overlap_period": "现任"},
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "宋亚俊（书记）与田野（县委常委、副县长）同为县委常委会班子成员",
     "overlap_org": "中国共产党彭阳县委员会",
     "overlap_period": "现任"},
    # 倪金栋 — 陈淑重 (农业农村/乡村振兴分工协同)
    {"person_a": 4, "person_b": 3, "type": "overlap",
     "context": "陈淑重负责闽宁协作，配合倪金栋负责农业农村、乡村振兴",
     "overlap_org": "彭阳县人民政府",
     "overlap_period": "现任"},
    # 政府班子内部
    {"person_a": 2, "person_b": 5, "type": "overlap",
     "context": "张翼（县长）与伍福升（县政府党组副书记、常务副县长）同县政府班子",
     "overlap_org": "彭阳县人民政府",
     "overlap_period": "现任"},
    {"person_a": 2, "person_b": 6, "type": "overlap",
     "context": "张翼（县长）与崔丽菲（副县长）同县政府班子",
     "overlap_org": "彭阳县人民政府",
     "overlap_period": "现任"},
    {"person_a": 2, "person_b": 7, "type": "overlap",
     "context": "张翼（县长）与田野（副县长）同县政府班子",
     "overlap_org": "彭阳县人民政府",
     "overlap_period": "现任"},
    {"person_a": 2, "person_b": 8, "type": "overlap",
     "context": "张翼（县长）与罗金彩（副县长）同县政府班子",
     "overlap_org": "彭阳县人民政府",
     "overlap_period": "现任"},
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "张翼（县长）与陈淑重（政府党组副书记、副县长）同县政府班子",
     "overlap_org": "彭阳县人民政府",
     "overlap_period": "现任"},
]


# ── Person JSON generation ─────────────────────────────────────────────

def make_person_json_songyajun() -> dict:
    """Generate person JSON for 宋亚俊 (县委书记)."""
    return {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "宁夏回族自治区",
            "city": "固原市",
            "region": "彭阳县",
            "job": "县委书记",
            "task_id": "ningxia_彭阳县",
            "time_focus": "现任"
        },
        "identity": {
            "person_id": "ningxia_guyuan_pengyang_songyajun",
            "name": "宋亚俊",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1976-10",
            "birthplace": "",
            "native_place": "",
            "education": [
                {"period": "", "institution": "宁夏回族自治区党校（研究生学历）",
                 "major": "", "degree": "研究生",
                 "study_type": "party_school", "source_ids": ["S002"]}
            ],
            "party_join": "",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "宋亚俊_1976-10",
                "name_birthplace": "宋亚俊_",
                "official_profile_url": SOURCES["S002"]["url"]
            }
        },
        "current_status": {
            "current_post": "彭阳县委书记",
            "current_org": "中国共产党彭阳县委员会",
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"]
        },
        "career_timeline": [
            {
                "start": "至今",
                "end": "至今",
                "org": "中国共产党彭阳县委员会",
                "title": "彭阳县委书记",
                "level": "县级",
                "location": "宁夏回族自治区固原市彭阳县",
                "system": "party",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "主持县委全面工作，联系县人大常委会、政协彭阳县委员会和县人武部。官方领导之窗确认现任。",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"]
            },
            {
                "start": "不详",
                "end": "接任县委书记之前",
                "org": "履历缺口",
                "title": "",
                "notes": "公开任职以前的完整履历（此前在固原市或区县任职情况）未从可得页面核实到。",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "organizations": [
            {"org_id": "org_py_county_party", "name": "中国共产党彭阳县委员会",
             "type": "党委", "level": "县级", "parent": "中国共产党固原市委员会",
             "location": "宁夏回族自治区固原市彭阳县",
             "relation_to_person": "当前任职单位", "confidence": "confirmed",
             "source_ids": ["S001", "S002"]}
        ],
        "relationships": [
            {"person": "张翼", "person_id": "ningxia_guyuan_pengyang_zhangyi",
             "relationship_type": "superior_subordinate", "strength": "strong",
             "evidence": "宋亚俊（县委书记）与张翼（县委副书记、县长）是彭阳县党政主要领导搭档。",
             "overlap_org": "彭阳县", "overlap_period": "现任",
             "direction": "other_to_person", "confidence": "confirmed",
             "source_ids": ["S001", "S003"]},
            {"person": "倪金栋", "person_id": "ningxia_guyuan_pengyang_nijindong",
             "relationship_type": "overlap", "strength": "medium",
             "evidence": "倪金栋为县委副书记、政法委书记，协助书记处理县委日常工作。",
             "overlap_org": "中国共产党彭阳县委员会", "overlap_period": "现任",
             "direction": "person_to_other", "confidence": "confirmed",
             "source_ids": ["S005"]},
            {"person": "陈淑重", "person_id": "ningxia_guyuan_pengyang_chenshuzhong",
             "relationship_type": "overlap", "strength": "medium",
             "evidence": "陈淑重为县委副书记、副县长，属县委班子。",
             "overlap_org": "中国共产党彭阳县委员会", "overlap_period": "现任",
             "direction": "person_to_other", "confidence": "confirmed",
             "source_ids": ["S004"]}
        ],
        "governance_record": [
            {"period": "现任", "domain": "other",
             "achievement_or_event": "主持县委全面工作",
             "role_in_event": "县委书记",
             "measurable_outcome": "", "location": "彭阳县",
             "confidence": "confirmed", "source_ids": ["S002"]}
        ],
        "professional_profile": {
            "primary_specializations": ["party_leadership"],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": ["party"],
            "geographic_pattern": ["宁夏回族自治区", "固原市", "彭阳县"],
            "promotion_velocity": {
                "summary": "履历时间线不完整，无法评估整体晋升速度。",
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
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {
            "total_relationships": 3,
            "strong_edges": 1,
            "unique_organizations": 1,
            "known_predecessors": [],
            "known_successors": []
        },
        "risk_and_integrity_signals": [
            {"type": "none_found",
             "description": "截至2026年8月，未发现公开记录中的纪律处分、审计问题或负面报道。",
             "date": AS_OF, "confidence": "plausible", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": SOURCES["S001"]["title"],
             "url": SOURCES["S001"]["url"], "publisher": "彭阳县人民政府",
             "published_at": "", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high",
             "notes": "领导之窗汇总页"},
            {"id": "S002", "title": SOURCES["S002"]["title"],
             "url": SOURCES["S002"]["url"], "publisher": "彭阳县人民政府",
             "published_at": "", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high",
             "notes": "县委书记宋亚俊个人页面"}
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "宋亚俊接任县委书记前的完整履历未核实"
        },
        "open_questions": [
            {"priority": "critical",
             "question": "宋亚俊的出生地、出生年份完整信息及入党/入职时间？",
             "why_it_matters": "补全基础身份信息用于去重。",
             "suggested_queries": ["宋亚俊 简历", "宋亚俊 彭阳县委书记 出生地", "宋亚俊 任命"],
             "last_attempted": AS_OF},
            {"priority": "high",
             "question": "宋亚俊此前担任的职务与晋升路径？",
             "why_it_matters": "评估其职业轨迹与跨部门交流。",
             "suggested_queries": ["宋亚俊 此前任职", "固原市委 任前公示 宋亚俊"],
             "last_attempted": AS_OF},
            {"priority": "medium",
             "question": "前任彭阳县委书记是谁、去向如何？",
             "why_it_matters": "了解干部交流与交接模式。",
             "suggested_queries": ["彭阳县委 前任书记", "彭阳县 领导任免"],
             "last_attempted": AS_OF}
        ]
    }


def make_person_json_zhangyi() -> dict:
    """Generate person JSON for 张翼 (县长)."""
    return {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "宁夏回族自治区",
            "city": "固原市",
            "region": "彭阳县",
            "job": "县长",
            "task_id": "ningxia_彭阳县",
            "time_focus": "现任"
        },
        "identity": {
            "person_id": "ningxia_guyuan_pengyang_zhangyi",
            "name": "张翼",
            "aliases": ["张  翼"],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1982-04",
            "birthplace": "",
            "native_place": "",
            "education": [
                {"period": "", "institution": "（研究生学历，院校未列明）",
                 "major": "", "degree": "研究生",
                 "study_type": "unknown", "source_ids": ["S003"]}
            ],
            "party_join": "",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "张翼_1982-04",
                "name_birthplace": "张翼_",
                "official_profile_url": SOURCES["S003"]["url"]
            }
        },
        "current_status": {
            "current_post": "彭阳县委副书记、县长",
            "current_org": "彭阳县人民政府",
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S003"]
        },
        "career_timeline": [
            {
                "start": "至今",
                "end": "至今",
                "org": "彭阳县人民政府",
                "title": "彭阳县委副书记、县政府党组书记、县长",
                "level": "县级",
                "location": "宁夏回族自治区固原市彭阳县",
                "system": "government",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "县委副书记、县政府党组书记、县长、王洼产业园区工委书记。负县政府全面工作及审计工作。",
                "confidence": "confirmed",
                "source_ids": ["S001", "S003"]
            },
            {
                "start": "不详",
                "end": "接任县长之前",
                "org": "履历缺口",
                "title": "",
                "notes": "公开资料页面未逐项列明张翼此前完整任职经历。",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "organizations": [
            {"org_id": "org_py_county_gov", "name": "彭阳县人民政府",
             "type": "政府", "level": "县级", "parent": "固原市人民政府",
             "location": "宁夏回族自治区固原市彭阳县",
             "relation_to_person": "当前任职单位", "confidence": "confirmed",
             "source_ids": ["S003"]},
            {"org_id": "org_py_wangwa", "name": "王洼产业园区管理委员会",
             "type": "开发区", "level": "县级", "location": "宁夏回族自治区固原市彭阳县",
             "relation_to_person": "兼任工委书记", "confidence": "confirmed",
             "source_ids": ["S003"]}
        ],
        "relationships": [
            {"person": "宋亚俊", "person_id": "ningxia_guyuan_pengyang_songyajun",
             "relationship_type": "superior_subordinate", "strength": "strong",
             "evidence": "张翼与宋亚俊是彭阳县党政主要领导搭档（书记与县长）。",
             "overlap_org": "彭阳县", "overlap_period": "现任",
             "direction": "person_to_other", "confidence": "confirmed",
             "source_ids": ["S001", "S003"]},
            {"person": "伍福升", "person_id": "ningxia_guyuan_pengyang_wufusheng",
             "relationship_type": "overlap", "strength": "medium",
             "evidence": "伍福升为县政府党组副书记、常务副县长，属县政府班子。",
             "overlap_org": "彭阳县人民政府", "overlap_period": "现任",
             "direction": "person_to_other", "confidence": "confirmed",
             "source_ids": ["S006"]},
            {"person": "罗金彩", "person_id": "ningxia_guyuan_pengyang_luojincai",
             "relationship_type": "overlap", "strength": "medium",
             "evidence": "罗金彩为县政府副县长。",
             "overlap_org": "彭阳县人民政府", "overlap_period": "现任",
             "direction": "person_to_other", "confidence": "confirmed",
             "source_ids": ["S009"]}
        ],
        "governance_record": [
            {"period": "现任", "domain": "economic_development",
             "achievement_or_event": "统筹县政府全面工作，负责审计工作",
             "role_in_event": "县长",
             "measurable_outcome": "", "location": "彭阳县",
             "confidence": "confirmed", "source_ids": ["S003"]}
        ],
        "professional_profile": {
            "primary_specializations": ["government_administration"],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": ["party", "government", "development_zone"],
            "geographic_pattern": ["宁夏回族自治区", "固原市", "彭阳县"],
            "promotion_velocity": {
                "summary": "履历时间线不完整，无法评估整体晋升速度。",
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
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "network_metrics": {
            "total_relationships": 3,
            "strong_edges": 1,
            "unique_organizations": 2,
            "known_predecessors": [],
            "known_successors": []
        },
        "risk_and_integrity_signals": [
            {"type": "none_found",
             "description": "截至2026年8月，未发现公开记录中关于张翼的纪律处分、审计问题或负面报道。",
             "date": AS_OF, "confidence": "plausible", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": SOURCES["S001"]["title"],
             "url": SOURCES["S001"]["url"], "publisher": "彭阳县人民政府",
             "published_at": "", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high",
             "notes": "领导之窗汇总页"},
            {"id": "S003", "title": SOURCES["S003"]["title"],
             "url": SOURCES["S003"]["url"], "publisher": "彭阳县人民政府",
             "published_at": "", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high",
             "notes": "县长张翼个人页面"}
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "张翼接任县长前的完整履历未核实"
        },
        "open_questions": [
            {"priority": "critical",
             "question": "张翼的出生地、入党时间、入职时间、研究生院校及专业？",
             "why_it_matters": "补全身份信息用于去重与研究。",
             "suggested_queries": ["张翼 彭阳县长 简历", "张冀 固原市政府 任职", "张翼 任前公示"],
             "last_attempted": AS_OF},
            {"priority": "high",
             "question": "张翼此前的职务与晋升路径（如固原市直部门或其他县区）？",
             "why_it_matters": "了解县长选任来源与跨县交流。",
             "suggested_queries": ["张翼 固原 任职经历", "彭阳县 提名县长 张翼"],
             "last_attempted": AS_OF},
            {"priority": "medium",
             "question": "前任县长是谁？去向如何？",
             "why_it_matters": "理解干部交流模式。",
             "suggested_queries": ["彭阳县 前任县长", "彭阳县 政府领导 任免"],
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
    songyajun = make_person_json_songyajun()
    zhangyi = make_person_json_zhangyi()

    write_person_json(songyajun, "县委书记-宋亚俊")
    write_person_json(zhangyi, "县长-张翼")

    print(f"\nDone. Staged artifacts in: {STAGING}")
    print(f"  1. Build script: {__file__}")
    print(f"  2. Database: {DB_PATH}")
    print(f"  3. GEXF: {GEXF_PATH}")
    print(f"  4. Person JSONs: {PJSON_DIR}")

    print(f"\nSummary:")
    print(f"  Persons: {len(persons)} (including {sum(1 for p in persons if '待查' not in p['name'])} named)")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Sources: {len(SOURCES)} official URLs")


if __name__ == "__main__":
    main()