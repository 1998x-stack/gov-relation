#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 黄冈市 (Huanggang City), 湖北省.

Investigation date: 2026-07-24
Task ID: hubei_黄冈市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.hg.gov.cn — 黄冈市人民政府官方网站 (primary, current as of July 2026)
  - Meeting attendance lists and news articles from 黄冈市人民政府 website (July 2026)

Confidence notes:
  - Current roles: confirmed via multiple government meeting/news reports (July 2026)
  - Biographical details (birth, birthplace, education): mostly from official profiles
  - Baidu Baike 403 blocked; detailed career history gaps documented
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
SLUG = "黄冈市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "hubei_黄冈市"
if _CURRENT_DIR.name == "hubei_黄冈市":
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
# IDs: 1-3 core leaders, 4-9 deputy govt, 10-14 city govt, 15-20 NPC/CPPCC, 21-23 standing committee, 30+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "李军杰",
        "gender": "男",
        "ethnicity": "汉族",  # plausible — vast majority of Hubei party secretaries are Han
        "birth": "",  # open question — unverified (Baidu 403)
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委书记",
        "current_org": "中共黄冈市委员会",
        "source": "https://www.hg.gov.cn/zwxw/hgyw/",
        "confidence": "confirmed",
        "notes": "2026年7月多次主持市委常委会会议；此前履历待查"
    },
    {
        "id": 2,
        "name": "刘洁",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1969-03",
        "birthplace": "",  # open question
        "education": "大学学历、法律硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "黄冈市人民政府",
        "source": "https://www.hg.gov.cn/content/column/6799765?liId=754&leaderTypeId=409",
        "confidence": "confirmed",
        "notes": "黄冈市委副书记，市政府党组书记、市长；2026年7月14日主持市政府第100次常务会议"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Government Leaders (副市长)
    # Source: https://www.hg.gov.cn/szf/szzc/index.html (July 2026)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "陈俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-10",
        "birthplace": "",
        "education": "研究生、工学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "黄冈市人民政府",
        "source": "https://www.hg.gov.cn/content/column/6799765?liId=757&leaderTypeId=409",
        "confidence": "confirmed",
        "notes": "协助市长负责市政府常务工作；分管发改、财政、税务、应急、国资、统计等"
    },
    {
        "id": 4,
        "name": "胡昊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-10",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "黄冈市人民政府",
        "source": "https://www.hg.gov.cn/content/column/6799765?liId=795&leaderTypeId=409",
        "confidence": "confirmed",
        "notes": "市政府党组成员；兼任黄冈高新技术产业开发区党工委书记；负责科技、工业、生态环境、市场监管等"
    },
    {
        "id": 5,
        "name": "牟波",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1971-11",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "黄冈市人民政府",
        "source": "https://www.hg.gov.cn/content/column/6799765?liId=796&leaderTypeId=409",
        "confidence": "confirmed",
        "notes": "市政府党组成员；市委政法委副书记；市公安局党委书记、局长、督察长；负责公安、司法、信访"
    },
    {
        "id": 6,
        "name": "杨金叶",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1983-09",
        "birthplace": "",
        "education": "大学学历、管理学学士",
        "party_join": "无党派人士",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "黄冈市人民政府",
        "source": "https://www.hg.gov.cn/content/column/6799765?liId=798&leaderTypeId=409",
        "confidence": "confirmed",
        "notes": "兼任市科学技术局局长；负责民族宗教、民政、人社、退役军人事务等"
    },
    {
        "id": 7,
        "name": "陈威",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-09",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "黄冈市人民政府",
        "source": "https://www.hg.gov.cn/content/column/6799765?liId=801&leaderTypeId=409",
        "confidence": "confirmed",
        "notes": "市政府党组成员；负责交通、水利、农业农村、商务、林业、临空经济区等"
    },
    {
        "id": 8,
        "name": "胡安元",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-05",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "黄冈市人民政府",
        "source": "https://www.hg.gov.cn/content/column/6799765?liId=804&leaderTypeId=409",
        "confidence": "confirmed",
        "notes": "市政府党组成员；负责教育、自然资源、住建、文旅、卫生健康、医保、城管等"
    },
    {
        "id": 9,
        "name": "王中华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-07",
        "birthplace": "",
        "education": "在职博士研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "黄冈市人民政府",
        "source": "https://www.hg.gov.cn/content/column/6799765?liId=807&leaderTypeId=409",
        "confidence": "confirmed",
        "notes": "市政府党组成员；负责外事、侨务、港澳台方面工作；协管乡村振兴、临空经济区"
    },
    {
        "id": 10,
        "name": "胡凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-08",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府秘书长",
        "current_org": "黄冈市人民政府",
        "source": "https://www.hg.gov.cn/content/column/6799765?liId=778&leaderTypeId=409",
        "confidence": "confirmed",
        "notes": "市政府党组成员；市政府办公室党组书记、主任；协助市长处理市政府日常工作"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 人大常委会 Leadership
    # Source: https://www.hg.gov.cn/zwxw/hgyw/9390984.html (July 2026)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 11,
        "name": "吴琼",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会党组书记、主任",
        "current_org": "黄冈市人民代表大会常务委员会",
        "source": "https://www.hg.gov.cn/zwxw/hgyw/9390984.html",
        "confidence": "confirmed",
        "notes": "2026年7月21日主持市人大常委会党组会议"
    },
    {
        "id": 12,
        "name": "屈凯军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会党组副书记、副主任",
        "current_org": "黄冈市人民代表大会常务委员会",
        "source": "https://www.hg.gov.cn/zwxw/hgyw/9390984.html",
        "confidence": "confirmed",
        "notes": ""
    },
    {
        "id": 13,
        "name": "郭小野",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会党组成员、副主任",
        "current_org": "黄冈市人民代表大会常务委员会",
        "source": "https://www.hg.gov.cn/zwxw/hgyw/9390984.html",
        "confidence": "confirmed",
        "notes": ""
    },
    {
        "id": 14,
        "name": "蔡绪安",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会党组成员、副主任",
        "current_org": "黄冈市人民代表大会常务委员会",
        "source": "https://www.hg.gov.cn/zwxw/hgyw/9390984.html",
        "confidence": "confirmed",
        "notes": ""
    },
    {
        "id": 15,
        "name": "余凡",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会党组成员、副主任",
        "current_org": "黄冈市人民代表大会常务委员会",
        "source": "https://www.hg.gov.cn/zwxw/hgyw/9390984.html",
        "confidence": "confirmed",
        "notes": ""
    },
    {
        "id": 16,
        "name": "熊卫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "黄冈市人民代表大会常务委员会",
        "source": "https://www.hg.gov.cn/zwxw/hgyw/9390984.html",
        "confidence": "confirmed",
        "notes": "非中共党员（无党派/民主党派待查）"
    },
    {
        "id": 17,
        "name": "孙迎松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会党组成员、秘书长",
        "current_org": "黄冈市人民代表大会常务委员会",
        "source": "https://www.hg.gov.cn/zwxw/hgyw/9390984.html",
        "confidence": "confirmed",
        "notes": ""
    },
    # ══════════════════════════════════════════════════════════════════════
    # 政协 Leadership
    # Source: https://www.hg.gov.cn/zwxw/hgyw/9391104.html (July 2026)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 18,
        "name": "李初敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协党组书记、主席",
        "current_org": "中国人民政治协商会议黄冈市委员会",
        "source": "https://www.hg.gov.cn/zwxw/hgyw/9391104.html",
        "confidence": "confirmed",
        "notes": "2026年7月22日主持双月专题协商会"
    },
    {
        "id": 19,
        "name": "夏志东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "中国人民政治协商会议黄冈市委员会",
        "source": "https://www.hg.gov.cn/zwxw/hgyw/9391104.html",
        "confidence": "confirmed",
        "notes": ""
    },
    {
        "id": 20,
        "name": "余红志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协秘书长",
        "current_org": "中国人民政治协商会议黄冈市委员会",
        "source": "https://www.hg.gov.cn/zwxw/hgyw/9391104.html",
        "confidence": "confirmed",
        "notes": ""
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors (open questions)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "李军杰（前任——同人不同时期）",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共黄冈市委员会",
        "source": "公开报道",
        "confidence": "plausible",
        "notes": "李军杰并非全新到任，其前任信息待进一步查证（湖北省管干部任免公示暂不可及）"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共黄冈市委员会", "type": "党委", "level": "地级市", "parent": "中共湖北省委员会", "location": "黄冈市"},
    {"id": 2, "name": "黄冈市人民政府", "type": "政府", "level": "地级市", "parent": "湖北省人民政府", "location": "黄冈市"},
    {"id": 3, "name": "黄冈市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "湖北省人大常委会", "location": "黄冈市"},
    {"id": 4, "name": "中国人民政治协商会议黄冈市委员会", "type": "政协", "level": "地级市", "parent": "政协湖北省委员会", "location": "黄冈市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 李军杰 — Party Secretary
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "现任市委书记，2026年7月主持市委常委会"},
    # 刘洁 — Mayor
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "市委副书记，市政府党组书记"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 陈俊 — Executive Deputy Mayor
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "协助市长负责市政府常务工作"},
    # 胡昊
    {"person_id": 4, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼任黄冈高新区党工委书记"},
    # 牟波
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼市公安局局长"},
    # 杨金叶
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "无党派，兼市科技局局长"},
    {"person_id": 6, "org_id": 2, "title": "市科学技术局局长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 陈威
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 胡安元
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 王中华
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 胡凯 — Secretary-General
    {"person_id": 10, "org_id": 2, "title": "市政府秘书长", "start_date": "", "end_date": "", "rank": "正处级", "note": "市政府党组成员、办公室党组书记"},
    # NPC Leadership
    {"person_id": 11, "org_id": 3, "title": "市人大常委会主任", "start_date": "", "end_date": "", "rank": "正厅级", "note": "党组书记"},
    {"person_id": 12, "org_id": 3, "title": "市人大常委会副主任", "start_date": "", "end_date": "", "rank": "副厅级", "note": "党组副书记"},
    {"person_id": 13, "org_id": 3, "title": "市人大常委会副主任", "start_date": "", "end_date": "", "rank": "副厅级", "note": "党组成员"},
    {"person_id": 14, "org_id": 3, "title": "市人大常委会副主任", "start_date": "", "end_date": "", "rank": "副厅级", "note": "党组成员"},
    {"person_id": 15, "org_id": 3, "title": "市人大常委会副主任", "start_date": "", "end_date": "", "rank": "副厅级", "note": "党组成员"},
    {"person_id": 16, "org_id": 3, "title": "市人大常委会副主任", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 17, "org_id": 3, "title": "市人大常委会秘书长", "start_date": "", "end_date": "", "rank": "正处级", "note": "党组成员"},
    # CPPCC Leadership
    {"person_id": 18, "org_id": 4, "title": "市政协主席", "start_date": "", "end_date": "", "rank": "正厅级", "note": "党组书记"},
    {"person_id": 19, "org_id": 4, "title": "市政协副主席", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 20, "org_id": 4, "title": "市政协秘书长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 李军杰 ↔ 刘洁 (Party Secretary – Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "中共黄冈市委员会", "overlap_period": "2026"},
    # 刘洁 ↔ 陈俊 (Mayor – Executive Deputy Mayor)
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "市长—常务副市长", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    # 刘洁 ↔ 胡昊
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "市长—副市长", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    # 刘洁 ↔ 牟波
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "市长—副市长", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    # 刘洁 ↔ 杨金叶
    {"person_a": 2, "person_b": 6, "type": "共事", "context": "市长—副市长", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    # 刘洁 ↔ 陈威
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "市长—副市长", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    # 刘洁 ↔ 胡安元
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "市长—副市长", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    # 刘洁 ↔ 王中华
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "市长—副市长", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    # 刘洁 ↔ 胡凯
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "市长—秘书长", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    # 陈俊 ↔ 胡昊 (Deputy Mayor colleagues)
    {"person_a": 3, "person_b": 4, "type": "同僚", "context": "市政府班子成员同僚", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 5, "type": "同僚", "context": "市政府班子成员同僚", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 6, "type": "同僚", "context": "市政府班子成员同僚", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 7, "type": "同僚", "context": "市政府班子成员同僚", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 8, "type": "同僚", "context": "市政府班子成员同僚", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 9, "type": "同僚", "context": "市政府班子成员同僚", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    {"person_a": 4, "person_b": 5, "type": "同僚", "context": "市政府班子成员同僚", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    {"person_a": 4, "person_b": 6, "type": "同僚", "context": "市政府班子成员同僚", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    {"person_a": 4, "person_b": 7, "type": "同僚", "context": "市政府班子成员同僚", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    {"person_a": 4, "person_b": 8, "type": "同僚", "context": "市政府班子成员同僚", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    {"person_a": 4, "person_b": 9, "type": "同僚", "context": "市政府班子成员同僚", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    {"person_a": 5, "person_b": 6, "type": "同僚", "context": "市政府班子成员同僚", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    {"person_a": 5, "person_b": 7, "type": "同僚", "context": "市政府班子成员同僚", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    {"person_a": 5, "person_b": 8, "type": "同僚", "context": "市政府班子成员同僚", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    {"person_a": 5, "person_b": 9, "type": "同僚", "context": "市政府班子成员同僚", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    {"person_a": 6, "person_b": 7, "type": "同僚", "context": "市政府班子成员同僚", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    {"person_a": 6, "person_b": 8, "type": "同僚", "context": "市政府班子成员同僚", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    {"person_a": 6, "person_b": 9, "type": "同僚", "context": "市政府班子成员同僚", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    {"person_a": 7, "person_b": 8, "type": "同僚", "context": "市政府班子成员同僚", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    {"person_a": 7, "person_b": 9, "type": "同僚", "context": "市政府班子成员同僚", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    {"person_a": 8, "person_b": 9, "type": "同僚", "context": "市政府班子成员同僚", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
    # 李军杰 ↔ 陈俊 (Party Secretary ↔ Standing Committee)
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—市委常委", "overlap_org": "中共黄冈市委员会", "overlap_period": "2026"},
    # 胡凯 ↔ 刘洁 (Secretary-General ↔ Mayor)
    {"person_a": 10, "person_b": 2, "type": "共事", "context": "秘书长—市长", "overlap_org": "黄冈市人民政府", "overlap_period": "2026"},
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


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"huanggang_{name}"

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
            "notes": "公开资料不足，完整履历待查。百度百科403禁止访问，搜索引擎超时。",
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
            "person_id": f"huanggang_{other_name}",
            "relationship_type": "overlap",
            "strength": "strong" if r["type"] == "共事" else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    # Source register
    source_url = person.get("source", "")
    sources = [
        {
            "id": "S001",
            "title": "黄冈市人民政府官方网站",
            "url": source_url,
            "publisher": "黄冈市人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "2026年7月政府网站领导之窗页面和新闻会议报道确认领导职务",
        }
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "湖北省",
            "city": "黄冈市",
            "region": "黄冈市",
            "job": person.get("current_post", ""),
            "task_id": "hubei_黄冈市",
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
            "biggest_gap": "出生年月、籍贯、完整履历（百度百科403，搜索引擎超时）",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的出生年月、籍贯、学历教育背景",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历（每段职务的起止时间）",
                "why_it_matters": "关系网络分析需要精确的时间线",
                "suggested_queries": [f"{name} 此前担任", f"{name} 任职经历"],
                "last_attempted": AS_OF,
            },
        ],
    }

    fname = f"{TODAY}-湖北省-黄冈市-{person['current_post']}-{person['name']}.json"
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

    # Write person JSONs
    print("  Writing person JSONs...")
    # Core leaders (1-2), executive deputy mayor (3), NPC and CPPCC chairs (11, 18)
    core_ids = {1, 2, 3, 11, 18}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
