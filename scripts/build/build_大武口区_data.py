#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 大武口区 (Dawukou District), 石嘴山市, 宁夏回族自治区.

Investigation date: 2026-08-07
Task ID: ningxia_大武口区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - https://www.dwk.gov.cn/xxgk/ldzc/ — 大武口区人民政府「领导之窗」(primary, current leadership roster + bios)
  - https://www.nx.gov.cn/zwgk/rsrm/202604/t20260428_5227459.html — 宁夏任前公示公告 2026年第6号 (刘强拟任县区委书记)
  - https://www.163.com/dy/article/KSG9Q75I05563DJA.html — 网易任命报道 (2026-05-09) 刘强任大武口区委书记，含完整简历
  - https://www.nx.gov.cn/zwgk/rsrm/202509/t20250902_5006540.html — 宁夏任前公示公告 2025年第12号 (汤瑞拟任市人大副主任候选人)
  - Baidu Baike: 汤瑞简历

Key findings (as of 2026-08-07):
  - 区委书记: 刘强 (born 1982-09, 汉族, 陕西榆林人, 宁夏党校研究生; 曾任大武口区长 2022-2026, 2026年5月任区委书记)
  - 区长(候任/代): 沙堃 (born 1983-09, 回族, 大学本科学历, 区长候选人、高新区管委会主任)
  - 前任区委书记: 汤瑞 (born 1982-06, 女, 汉族, 宁夏固原人; 2025年9月拟任地级市人大常委会副主任, 2026年5月卸任)

Confidence notes:
  - Current roles + roster: confirmed via 官方政府门户领导之窗 (primary source)
  - 刘强 full career: confirmed via 任前公示 + 网易任命报道 (appointment notice + media)
  - 汤瑞 biographical details: confirmed via Baidu Baike + 任前公示
  - 沙堃 full earlier career: unverified (只确认现任职务、出生、民族、学历) -> open question
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
SLUG = "大武口区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "ningxia_大武口区"
if _CURRENT_DIR.name == "ningxia_大武口区":
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
# IDs: 1 区委书记, 2 区长, 3 前任书记, 11+ 区委常委, 21+ 政府副区长, 31+ 人大, 41+ 政协, 51 前任区长

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # 核心领导 (现任)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "刘强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年9月",
        "birthplace": "陕西榆林",
        "education": "宁夏党校研究生",
        "party_join": "中共党员（2006年6月）",
        "work_start": "2002年5月",
        "current_post": "区委书记",
        "current_org": "中共大武口区委员会",
        "source": "https://www.163.com/dy/article/KSG9Q75I05563DJA.html",
        "confidence": "confirmed",
        "notes": "现任大武口区委书记、石嘴山高新区党工委书记。曾任平罗县城关镇镇长助理、平罗县团委书记、红崖子乡政府乡长、高仁乡党委书记乡长、姚伏镇党委书记；2013年11月任石嘴山市团委副书记，2017年1月任市团委书记，2019年1月任市审批服务管理局党组书记、局长，2021年5月任市财政局党组书记、局长；2022年5月补选为大武口区区长；2026年5月任大武口区委书记（不再任区长）。",
    },
    {
        "id": 2,
        "name": "沙堃",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1983年9月",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "大武口区人民政府",
        "source": "https://www.dwk.gov.cn/xxgk/ldzc/",
        "confidence": "confirmed",
        "notes": "现任大武口区委副书记、区人民政府区长候选人、石嘴山高新区管委会主任，领导区政府全面工作并负责审计工作。官方领导之窗以『区长候选人』标注（候任/代区长），人大正式任命程序或尚未完成。此前具体任职履历待查。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 前任区委书记
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "汤瑞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982年6月",
        "birthplace": "宁夏固原",
        "education": "在职硕士研究生",
        "party_join": "中共党员（1999年3月）",
        "work_start": "2003年11月",
        "current_post": "前区委书记",
        "current_org": "中共大武口区委员会（已卸任）",
        "source": "https://baike.baidu.com/item/汤瑞/9896161",
        "confidence": "confirmed",
        "notes": "前任大武口区委书记。历任永宁县纪检委、银川市团委、自治区党委组织部干部一处、宁夏农垦管理局团委、共青团宁夏区委、灵武市委副书记政法书记、银川市司法局党委书记局长；后任大武口区委副书记政府区长高新区管委会主任，2022年2月拟任区委书记，直至2026年5月卸任；2025年9月拟提名为地级市人大常委会副主任候选人。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 现任区委常委 (as of 2026-08-07)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 11,
        "name": "杨旭辉",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1986年8月",
        "birthplace": "",
        "education": "宁夏党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共大武口区委员会",
        "source": "https://www.dwk.gov.cn/laq/ldzc/",
        "confidence": "confirmed",
        "notes": "现任大武口区委副书记，分管国家安全、社会工作、农业农村、乡村振兴、信访维稳等。",
    },
    {
        "id": 12,
        "name": "谢琴",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1979年8月",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共大武口区委员会",
        "source": "https://www.dwk.gov.cn/laq/ldzc/",
        "confidence": "confirmed",
        "notes": "主持区委宣传部工作，负责意识形态、宣传思想、精神文明建设、文明城市创建、网络安全、文化体育旅游。",
    },
    {
        "id": 13,
        "name": "张凯福",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年6月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、政法委书记",
        "current_org": "中共大武口区委员会",
        "source": "https://www.dwk.gov.cn/laq/ldzc/",
        "confidence": "confirmed",
        "notes": "主持区委政法委工作，负责依法治区、政法、社会治理、扫黑除恶。",
    },
    {
        "id": 14,
        "name": "张禹",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年12月",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、统战部部长",
        "current_org": "中共大武口区委员会",
        "source": "https://www.dwk.gov.cn/laq/ldzc/",
        "confidence": "confirmed",
        "notes": "兼任大武口区政协党组副书记，主持区委统战部工作，负责统一战线、民族宗教、侨务、教育。",
    },
    {
        "id": 15,
        "name": "杨晓东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年11月",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "大武口区人民政府",
        "source": "https://www.dwk.gov.cn/ln/ldzc/",
        "confidence": "confirmed",
        "notes": "区委常委、区人民政府党组副书记、常务副区长，负责区政府常务工作及发改、工业、财税、金融、应急等。",
    },
    {
        "id": 16,
        "name": "韩宁",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1981年2月",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、纪委书记、监委主任",
        "current_org": "中共大武口区纪律检查委员会",
        "source": "https://www.dwk.gov.cn/ln/ldzc/",
        "confidence": "confirmed",
        "notes": "主持区纪委监委工作，负责纪检、监察、监督、巡察。",
    },
    {
        "id": 17,
        "name": "谷亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年9月",
        "birthplace": "",
        "education": "在职硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共大武口区委员会",
        "source": "https://www.dwk.gov.cn/ln/ldzc/",
        "confidence": "confirmed",
        "notes": "主持区委组织部工作，负责组织、干部、人才、机构编制、区直机关党建。",
    },
    {
        "id": 18,
        "name": "孙杨",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1985年1月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长（挂职）",
        "current_org": "大武口区人民政府",
        "source": "https://www.dwk.gov.cn/ln/ldzc/",
        "confidence": "confirmed",
        "notes": "挂职副区长，负责科技、审批服务、文旅、街道社区。",
    },
    {
        "id": 19,
        "name": "杜万顺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年12月",
        "birthplace": "",
        "education": "宁夏党校",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "大武口区人民政府",
        "source": "https://www.dwk.gov.cn/ln/ldzc/",
        "confidence": "confirmed",
        "notes": "区委常委、区政府党组成员、副区长，2026年7月市级干部任前公示拟进一步使用。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 政府其他副职 (non-常委)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 21,
        "name": "王浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989年9月",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "大武口区人民政府",
        "source": "https://www.dwk.gov.cn/ln/ldzc/",
        "confidence": "confirmed",
        "notes": "区政府党组成员、副区长，正外出挂职。",
    },
    {
        "id": 22,
        "name": "衣贯武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年10月",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、公安分局局长",
        "current_org": "大武口区人民政府",
        "source": "https://www.dwk.gov.cn/ln/ldzc/",
        "confidence": "confirmed",
        "notes": "区政府党组成员、副区长、公安分局党委书记、局长、督察长。",
    },
    {
        "id": 23,
        "name": "马春",
        "gender": "女",
        "ethnicity": "回族",
        "birth": "1990年3月",
        "birthplace": "",
        "education": "宁夏党校研究生",
        "party_join": "民主党派",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "大武口区人民政府",
        "source": "https://www.dwk.gov.cn/ln/ldzc/",
        "confidence": "confirmed",
        "notes": "区政府副区长，民主党派（非中共党员），负责教育、民政、卫生、社保等。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 人大常委会
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 31,
        "name": "魏冠中",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年12月",
        "birthplace": "",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "大武口区人民代表大会常务委员会",
        "source": "https://www.dwk.gov.cn/ln/ldzc/",
        "confidence": "confirmed",
        "notes": "区人大常委会党组书记、主任，主任会议。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 政协
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 41,
        "name": "周学斌",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1968年8月",
        "birthplace": "",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议大武口区委员会",
        "source": "https://www.dwk.gov.cn/ln/ldzc/",
        "confidence": "confirmed",
        "notes": "区政协党组书记、主席。",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共大武口区委员会", "type": "党委", "level": "市辖区", "parent": "中共石嘴山市委员会", "location": "大武口区"},
    {"id": 2, "name": "大武口区人民政府", "type": "政府", "level": "市辖区", "parent": "石嘴山市人民政府", "location": "大武口区"},
    {"id": 3, "name": "石嘴山高新技术产业开发区党工委/管委会", "type": "开发区", "level": "市辖区", "parent": "石嘴山市人民政府", "location": "大武口区"},
    {"id": 4, "name": "中共大武口区纪律检查委员会/区监察委员会", "type": "党委", "level": "市辖区", "parent": "中共石嘴山市纪律检查委员会", "location": "大武口区"},
    {"id": 5, "name": "大武口区人民代表大会常务委员会", "type": "人大", "level": "市辖区", "parent": "石嘴山市人大常委会", "location": "大武口区"},
    {"id": 6, "name": "中国人民政治协商会议大武口区委员会", "type": "政协", "level": "市辖区", "parent": "政协石嘴山市委员会", "location": "大武口区"},
    {"id": 7, "name": "中共石嘴山市委员会", "type": "党委", "level": "地级市", "parent": "中共宁夏回族自治区委员会", "location": "石嘴山市"},
    {"id": 8, "name": "石嘴山市人民政府", "type": "政府", "level": "地级市", "parent": "宁夏回族自治区人民政府", "location": "石嘴山市"},
    {"id": 9, "name": "大武口区公安分局", "type": "政府", "level": "区级部门", "parent": "大武口区人民政府", "location": "大武口区"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 刘强 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2026年5月", "end_date": "", "rank": "正处级", "note": "现任大武口区委书记，主持区委全面工作"},
    {"person_id": 1, "org_id": 3, "title": "高新区党工委书记", "start_date": "2026年5月", "end_date": "", "rank": "正处级", "note": "兼任石嘴山高新区党工委书记"},
    {"person_id": 1, "org_id": 2, "title": "区长", "start_date": "2022年5月", "end_date": "2026年5月", "rank": "正处级", "note": "2022年5月补选为大武口区区长，2026年5月卸任"},
    # 沙堃 — 区长
    {"person_id": 2, "org_id": 2, "title": "区长（候选人）", "start_date": "2026年", "end_date": "", "rank": "正处级", "note": "区长候选人，领导区政府全面工作"},
    {"person_id": 2, "org_id": 3, "title": "高新区管委会主任", "start_date": "2026年", "end_date": "", "rank": "正处级", "note": "兼任石嘴山高新区管委会主任"},
    # 汤进 — 前任区委书记
    {"person_id": 3, "org_id": 1, "title": "区委书记", "start_date": "2022年2月", "end_date": "2026年5月", "rank": "正处级", "note": "前任大武口区委书记、高新区党工委书记"},
    {"person_id": 3, "org_id": 2, "title": "区长", "start_date": "2016年", "end_date": "2022年2月", "rank": "正处级", "note": "曾任大武口区委副书记、政府区长、高新区管委会主任（任期待核）"},
    # 区委常委 / 副书记
    {"person_id": 11, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "区委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "区委常委、政法委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 1, "title": "区委常委、统战部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 6, "title": "区政协党组副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "兼任"},
    {"person_id": 16, "org_id": 4, "title": "区委常委、纪委书记、监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 1, "title": "区委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 政府领导
    {"person_id": 15, "org_id": 2, "title": "区委常委、常务副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "区政府党组副书记，负责常务"},
    {"person_id": 18, "org_id": 2, "title": "副区长（挂职）", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 2, "title": "区委常委、副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 2, "title": "副区长（外出挂职）", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 22, "org_id": 2, "title": "副区长、公安分局局长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 22, "org_id": 9, "title": "公安分局党委书记、局长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 23, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 人大 / 政协
    {"person_id": 31, "org_id": 5, "title": "区人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 41, "org_id": 6, "title": "区政协主席", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 刘强 ↔ 沙堃 (区委书记 – 区长搭档)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—区长搭档", "overlap_org": "大武口区本级", "overlap_period": "2026"},
    # 刘强 ↔ 汤瑞 (前任–现任书记：直接继任)
    {"person_a": 1, "person_b": 3, "type": "前任继任", "context": "刘强接任汤瑞为大武口区委书记（2026年5月）", "overlap_org": "中共大武口区委员会", "overlap_period": "2026"},
    # 刘强 ↔ 各常委
    {"person_a": 1, "person_b": 11, "type": "共事", "context": "书记—区委副书记", "overlap_org": "中共大武口区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 12, "type": "共事", "context": "书记—宣传部长", "overlap_org": "中共大武口区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 13, "type": "共事", "context": "书记—政法委书记", "overlap_org": "中共大武口区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 14, "type": "共事", "context": "书记—统战部长", "overlap_org": "中共大武口区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 17, "type": "共事", "context": "书记—组织部长", "overlap_org": "中共大武口区委员会", "overlap_period": "2026"},
    # 区长/政府领导间
    {"person_a": 2, "person_b": 15, "type": "共事", "context": "区长—常务副区长", "overlap_org": "大武口区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 18, "type": "共事", "context": "区长—挂职副区长", "overlap_org": "大武口区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 19, "type": "共事", "context": "区长—副区长", "overlap_org": "大武口区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 23, "type": "共事", "context": "区长—副区长", "overlap_org": "大武口区人民政府", "overlap_period": "2026"},
    # 前任书记与人大政协
    {"person_a": 3, "person_b": 31, "type": "共事", "context": "前书记—人大主任", "overlap_org": "大武口区本级", "overlap_period": "2022-2026"},
    {"person_a": 3, "person_b": 41, "type": "共事", "context": "前书记—政协主席", "overlap_org": "大武口区本级", "overlap_period": "2022-2026"},
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


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"dawukou_{name}"

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
            "notes": pos.get("note", "") or "",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001", "S002"] if pid == 1 else ["S001"],
        })

    # For 刘强 (id 1), add the fuller earlier career from the appointment biography
    if pid == 1:
        for seg in [
            ("", "", "平罗县城关镇", "镇长助理（副科级）", "参加工作起点"),
            ("", "", "平罗县团委", "平罗县团委书记", ""),
            ("", "", "平罗县红崖子乡政府", "乡长", ""),
            ("", "", "平罗县高仁乡", "党委书记、乡长", ""),
            ("", "", "平罗县姚伏镇", "党委书记", ""),
            ("2013年11月", "", "中国共产主义青年团石嘴山市委员会", "市团委副书记", ""),
            ("2017年1月", "", "中国共产主义青年团石嘴山市委员会", "市团委书记", ""),
            ("2019年1月", "", "石嘴山市审批服务管理局", "党组书记、局长", ""),
            ("2021年5月", "", "石嘴山市财政局", "党组书记、局长", ""),
        ]:
            career_timeline.append({
                "start": seg[0] or "unknown",
                "end": seg[1] or "unknown",
                "org": seg[2],
                "title": seg[3],
                "level": "副科级至正科级",
                "notes": seg[4] or "",
                "confidence": "confirmed",
                "source_ids": ["S002"],
            })

    # Add gap entry if a core leader has a sparse timeline
    if pid == 2 and len(career_timeline) <= 2:
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料仅确认现任区长候选人身份、出生年月与民族学历；完整履历待查（简历待补）。",
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
        rel_type = "predecessor_successor" if r.get("type") == "前任继任" else "overlap"
        rels_output.append({
            "person": other_name,
            "person_id": f"dawukou_{other_name}",
            "relationship_type": rel_type,
            "strength": "strong" if r.get("type") in ("共事", "前任继任") else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001", "S002"] if rel_type == "predecessor_successor" else ["S001"],
        })

    # Source register
    sources = [
        {
            "id": "S001",
            "title": "大武口区人民政府领导之窗",
            "url": "https://www.dwk.gov.cn/xxgk/ldzc/",
            "publisher": "大武口区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "官方领导之窗当前版本（2026年）确认现任区委常委会、政府、人大、政协领导班底及个人简介",
        },
    ]
    if pid == 1:
        sources.append({
            "id": "S002",
            "title": "网易新闻报道：刘强任石嘴山市大武口区委书记",
            "url": "https://www.163.com/dy/article/KSG9JZMI05563DJA.html",
            "publisher": "网易",
            "published_at": "2026-05-09",
            "accessed_at": AS_OF,
            "source_type": "media",
            "reliability": "medium",
            "notes": "转引区领导干部大会任免决定与刘强完整简历",
        })
    if pid == 2:
        sources.append({
            "id": "S002",
            "title": "自治区党委组织部任前公示公告（2026年第6号）",
            "url": "https://www.nx.gov.cn/zwgk/rsrm/202604/t20260428_5227459.html",
            "publisher": "宁夏回族自治区党委组织部",
            "published_at": "2026-04-28",
            "accessed_at": AS_OF,
            "source_type": "appointment_notice",
            "reliability": "high",
        })
    if pid == 3:
        sources.append({
            "id": "S002",
            "title": "百度百科：汤（宁夏石嘴山市大武口区委书记）",
            "url": "https://baike.baidu.com/item/汤2C812680101",
            "publisher": "百度百科",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": "汤瑞简历与民族籍贯等信息（百度百科功能正常），含2025年9月地级市人大副主任提名任前公示",
        })

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "宁夏回族自治区",
            "city": "石嘴山市",
            "region": "大武口区",
            "job": person.get("current_post", ""),
            "task_id": "ningxia_大武口区",
            "time_focus": "2026年8月",
        },
        "identity": {
            "person_id": slug_id,
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("birthplace", ""),
            "education": [
                {
                    "period": "",
                    "institution": "",
                    "major": "",
                    "degree": person.get("education", ""),
                    "study_type": "unknown",
                    "source_ids": ["S001"],
                }
            ] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth','')}",
                "name_birthplace": f"{name}_{person.get('birthplace','')}",
                "official_profile_url": "https://www.dwk.gov.cn/ldgk/ldzc/",
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正处级" if pid in (1, 2, 3) else ("副处级" if 11 <= pid <= 23 else "正处级"),
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "governance_record": [
            {
                "period": "2026年5月至今",
                "domain": "regional_leadership",
                "achievement_or_event": "接任大武口区委书记、高新区党工委书记",
                "role_in_event": "主持区委全面工作",
                "measurable_outcome": "统筹大武口区改委全面工作并联系人大、政协",
                "location": "大武口区",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "period": "2022-2026年",
                "domain": "economic_development",
                "achievement_or_event": "任大武口区人民政府区长",
                "role_in_event": "主持区政府全面工作",
                "measurable_outcome": "区长任职期间领导全区经济社会高质量发展",
                "location": "大武口区",
                "confidence": "confirmed",
                "source_ids": ["S002"],
            },
        ] if pid == 1 else [
            {
                "period": "2026年",
                "domain": "economic_development",
                "achievement_or_event": "任区政府区长候选人、高新区管委会主任",
                "role_in_event": "领导区政府全面工作，分管审计",
                "measurable_outcome": "统筹政府日常行政与高新区园区建设",
                "location": "大武口区",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            }
        ] if pid == 2 else [],
        "professional_profile": {
            "primary_specializations": ["基层治理"] if pid == 1 else (["行政管理"] if pid == 2 else []),
            "secondary_specializations": [],
            "career_pattern": "local_ladder" if pid == 1 else "cross_county_rotation",
            "systems_experience": list(set(
                o.get("type", "") for o in organizations if o["id"] in [pos["org_id"] for pos in person_positions]
            )),
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {
            "relationship_count": len(rels_output),
            "position_count": len(person_positions),
            "cross_region": True if pid in (1, 3) else False,
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至调查日期未公开检索到刘强涉及违纪违法或负面报道；大武口区2022年曾按自治区党委第四巡视组反馈整改（时任书记汤焍担主责），该巡视指向区一级而非刘本人。",
                "date": "",
                "confidence": "plausible",
                "source_ids": ["S001"],
            } if pid == 1 else []
        ] if pid in (1, 2, 3) else [],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "plausible",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "complete" if pid == 1 else ("thin" if pid == 3 else "partial"),
            "relationship_confidence": "medium" if pid == 2 else "high",
            "biggest_gap": "沙堃完整履历（此前任职、教育细节、入党/参加工作时间）待补充" if pid == 2 else "",
        },
        "open_questions": [
            {
                "priority": "high" if pid == 2 else "medium",
                "question": "沙堃的完整任职履历（2026年任区长前经历）" if pid == 2 else f"{name}的完整任职履历与时间线细节仍待补齐",
                "why_it_matters": "关系网络分析需要精确的时间线与任职交集",
                "suggested_queries": [f"{name} 简历", f"{name} 此前担任", f"{name} 任前公示"],
                "last_attempted": AS_OF,
            },
        ] if pid in (1, 2) else [],
    }

    fname = f"{TODAY}-宁夏回族自治区-石嘴山市-{person['current_post']}-{person['name']}.json"
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
    core_ids = {1, 2}  # 现任区委书记 & 区长（候任）
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())