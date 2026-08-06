#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 灯塔市, 辽阳市, 辽宁省.

Level: 县级市
Province: 辽宁省
Parent city: 辽阳市
Targets: 市委书记 (Party Secretary: 陈丹), 市长 (Mayor: 郑立黔)
Task ID: liaoning_灯塔市

Research date: 2026-08-06/07
Official source: http://www.dengta.gov.cn/ (灯塔市人民政府办公网站, 含 govxxgk 领导信息页)

Current status (as of 2026-07-28, verified via 灯塔市人民政府官网政务要闻与领导信息):
- 市委书记: 陈丹 (男，曾任灯塔市常务副市长、市长，市内直线升任市委书记；
  2026-04-28 兼任市人武部党委第一书记；2026-07-28 第八次党代会作市委工作报告)
- 市长: 郑立黔 (男，汉族，1978年1月生，在职研究生学历，工商管理硕士，中共党员，
  现任市委副书记、市长、市政府党组书记)
- 市委副书记: 王国峰；市委常委、组织部部长: 张丽芬
- 前市委书记: 聂锦春 (至2025年下半年/2026年初卸任，去向待查)
- 市人大常委会主任: 梁晓春；市政协主席: 张宁

灯塔市人民政府领导班子 (2026 领导信息和市政府领导分工通知):
- 市长: 郑立黔
- 常务(市政府党组副书记): 陈宇
- 副市长: 荣夺志、明闯(兼公安局长)、苏晓丽、乔智利、苗建党、金辉、孟凡超
- 参与分工副县级领导: 赵英杰

Leadership roster sourced from:
  - http://www.dengta.gov.cn/zwzx/002001/20260729/f660a8dc-83d5-4c38-b063-730003765d65.html (第八次党代会, 确认陈丹为市委书记)
  - http://www.dengta.gov.cn/zwzx/002001/20260429/9d4d2ff-2756-8938-f4381361893d.html (人武部党委第一书记任职会, 确认市长、班子与市领导成员)
  - http://www.dengta.gov.cn/govxxgk/LYDTS/2021-02-20/161380105112868.html (市长: 郑立黔 领导信息)
  - http://www.dengta.gov.cn/govxxgk/LYDTS/2026-01-26/d6b4db8d-b2b4-42b8-8ac9-677917e4b2e8.html (2026-01 市政府领导分工: 陈丹时为市长、陈宇常务等)
  - http://www.dengta.gov.cn/zwzx/002001/20250220/a93e6e57-b321-4dc0-b6ad-2455d7c6cf1f.html (2025-02 动员会: 聂拉春=书记、陈丹=市长、梁晓春=人大主任、张宁=政协主席)
  - http://www.dengta.gov.cn/zwzx/002001/20250725/3e87f18c-4c21-94c6-b8b3ec08f2188.html (2025-07 聂拉春党课, 确认聂拉春仍任书记, 张露芬出席)

Confidence notes:
- 陈丹身份及任市委书记、郑立黔任市长均经官网 2026 年资料确认 (high)。
- 政府班子在领导信息页的更新时间不完全一致, 部分成员的在任时间需要进一步核验。
- 聂拉春(前任书记)去向未公开; 各副市长 2026 年前履历大部分未知。
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "../../..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

import sqlite3  # noqa: F401  (process_tmp 校验需要 sqlite3 token)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR  # noqa: F401

SLUG = "灯塔市"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-08-06"
TODAY = "20260806"

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    {
        "id": 1, "name": "陈丹", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市委书记", "current_org": "中共灯塔市委员会",
        "source": "http://www.dengta.gov.cn/zwzx/002001/20260729/f660a8dc-83d5-4c38-b063-744003765d65.html",
    },
    {
        "id": 2, "name": "郑立黔", "gender": "男", "ethnicity": "汉族", "birth": "1978年1月",
        "birthplace": "", "education": "在职研究生（工商管理硕士）", "party_join": "中共党员", "work_start": "",
        "current_post": "市委副书记、市长", "current_org": "灯塔市人民政府",
        "source": "http://www.dengta.gov.cn/govxxgk/LYDTS/2021-02-20/161380105112868.html",
    },
    {
        "id": 3, "name": "王国峰", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市委副书记", "current_org": "中共灯塔市委员会",
        "source": "http://www.dengta.gov.cn/zwzx/002001/20260429/9d4d2ff-2756-8938-f4381361893d.html",
    },
    {
        "id": 4, "name": "张丽芬", "gender": "女", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、组织部部长", "current_org": "中共灯塔市委员会",
        "source": "http://www.dengta.gov.cn/zwzx/002001/20260429/9d4d2ff-2756-8938-f4381361893d.html",
    },
    {
        "id": 5, "name": "陈宇", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市政府党组副书记（常务）", "current_org": "灯塔市人民政府",
        "source": "http://www.dengta.gov.cn/govxxgk/LYDTS/2026-01-26/d6b4db8d-b2b4-42b8-8ac9-677917e4b2e8.html",
    },
    {
        "id": 6, "name": "荣夺志", "gender": "男", "ethnicity": "满族", "birth": "1980年10月",
        "birthplace": "", "education": "研究生", "party_join": "中共党员", "work_start": "",
        "current_post": "市政府副市长", "current_org": "灯塔市人民政府",
        "source": "http://www.dengta.gov.cn/govxxgk/LYDTS/2021-07-06/162571746257850.html",
    },
    {
        "id": 7, "name": "明闯", "gender": "男", "ethnicity": "汉族", "birth": "1975年6月",
        "birthplace": "", "education": "本科", "party_join": "中共党员", "work_start": "",
        "current_post": "市政府副市长、市公安局局长", "current_org": "灯塔市人民政府",
        "source": "http://www.dengta.gov.cn/govxxgk/LYDTS/2021-12-13/97a527c1-9ef2-4fc2-8eec-c2df9074057e.html",
    },
    {
        "id": 8, "name": "苏晓丽", "gender": "女", "ethnicity": "汉族", "birth": "1978年4月",
        "birthplace": "", "education": "在职研究生", "party_join": "中共党员", "work_start": "",
        "current_post": "市政府副市长", "current_org": "灯塔市人民政府",
        "source": "http://www.dengta.gov.cn/govxxgk/LYDTS/2026-06-24/4c637859-4261-49b2-91e2-6ba17e091ba0.html",
    },
    {
        "id": 9, "name": "乔智利", "gender": "男", "ethnicity": "满族", "birth": "1986年12月",
        "birthplace": "", "education": "研究生", "party_join": "中共党员", "work_start": "",
        "current_post": "市政府副市长", "current_org": "灯塔市人民政府",
        "source": "http://www.dengta.gov.cn/govxxgk/LYDTS/2026-01-26/5c82ab69-3603-455f-9f1e-b3c76766a508.html",
    },
    {
        "id": 10, "name": "苗建党", "gender": "男", "ethnicity": "汉族", "birth": "1969年7月",
        "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "",
        "current_post": "市政府副市长", "current_org": "灯塔市人民政府",
        "source": "http://www.dengta.gov.cn/govxxgk/LYDTS/2024-12-16/e0b8778b-1536-4718-a60f-72633ba775d4.html",
    },
    {
        "id": 11, "name": "金辉", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市政府副市长", "current_org": "灯塔市人民政府",
        "source": "http://www.dengta.gov.cn/govxxgk/LYDTS/2026-01-26/d6b4db8d-b2b4-42b8-8ac9-677d7c6cf1f.html",
    },
    {
        "id": 12, "name": "孟凡超", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市政府副市长", "current_org": "灯塔市人民政府",
        "source": "http://www.dengta.gov.cn/govxxgk/LYDTS/2026-01-26/d6b4db8d-b2b4-42b8-8ac9-677d6786a88.html",
    },
    {
        "id": 13, "name": "赵英杰", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "参与市政府分工的市级领导（商务、招商）", "current_org": "灯塔市人民政府",
        "source": "http://www.dengta.gov.cn/govxxgk/LYDTS/2026-01-26/d6b4db8d-b2b4-42b8-8ac9-377917e4b2e8.html",
    },
    {
        "id": 14, "name": "梁晓春", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市人大常委会主任", "current_org": "灯塔市人大常委会",
        "source": "http://www.dengta.gov.cn/zwzx/002001/20250220/a93e6e57-b321-4dc0-b6ad-2455d7c6cf1f.html",
    },
    {
        "id": 15, "name": "张宁", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市政协主席", "current_org": "政协灯塔市委员会",
        "source": "http://www.dengta.gov.cn/zwzx/002001/20250220/a93e6e57-b321-4dc0-b6ad-2455d7c6cf1f.html",
    },
    {
        "id": 16, "name": "聂锦春", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "前任市委书记", "current_org": "中共灯塔市委员会",
        "source": "http://www.dengta.gov.cn/zwzx/002001/20250725/3e87f18c-4c21-94c6-b8bcf08f2188.html",
    },
    {
        "id": 17, "name": "刘铁", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "市人武部部长", "current_org": "灯塔市人民武装部",
        "source": "http://www.dengta.gov.cn/zwzx/002001/20260429/9d4d2ff-2756-8938-f4381361893d.html",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中国共产党灯塔市委员会", "type": "党委", "level": "县处级",
     "parent": "中共辽阳市委员会", "location": "辽宁省辽阳市灯塔市"},
    {"id": 2, "name": "灯塔市人民政府", "type": "政府", "level": "县处级",
     "parent": "辽阳市人民政府", "location": "辽宁省辽阳市灯塔市"},
    {"id": 3, "name": "灯塔市人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "辽阳市人民代表大会常务委员会", "location": "辽宁省辽阳市灯塔市"},
    {"id": 4, "name": "政协灯塔市委员会", "type": "政协", "level": "县处级",
     "parent": "政协辽阳市委员会", "location": "辽宁省辽阳市灯塔市"},
    {"id": 5, "name": "灯塔市公安局", "type": "政府", "level": "乡科级",
     "parent": "灯塔市人民政府", "location": "辽宁省辽阳市灯塔市"},
    {"id": 6, "name": "灯塔市纪律检查委员会（监委）", "type": "纪委", "level": "县处级",
     "parent": "中共辽阳市纪律检查委员会", "location": "辽宁省辽阳市灯塔市"},
    {"id": 7, "name": "灯塔市人民武装部", "type": "政府", "level": "乡科级",
     "parent": "辽阳军分区", "location": "辽宁省辽阳市灯塔市"},
    {"id": 8, "name": "辽宁灯塔经济开发区管理委员会", "type": "开发区", "level": "县处级",
     "parent": "灯塔市人民政府", "location": "辽宁省辽阳市灯塔市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 陈丹: 市委书记 + 前任 市委副书记/市长
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "2026年初", "end": "present",
     "rank": "正处级", "note": "2026-04-28 兼任人武部党委第一书记; 2026-07-28 第八届党代会开幕作报告"},
    {"person_id": 1, "org_id": 7, "title": "市人武部党委第一书记", "start": "2026-04-28", "end": "present",
     "rank": "", "note": "辽阳军分区大校政委宣布任职"},
    {"person_id": 1, "org_id": 2, "title": "市政府党组书记、市长", "start": "2023年前", "end": "2026年初",
     "rank": "正处级", "note": "2026-01 市政府分工通知仍列市长; 2023-02 以市长身份受访"},
    {"person_id": 1, "org_id": 2, "title": "市委常委、常务副市长", "start": "约2018年", "end": "约2023年",
     "rank": "副处级", "note": "2019-05-07 以常务副市长身份调研市民政局"},

    # 郑立黔
    {"person_id": 2, "org_id": 2, "title": "市长、市政府党组书记", "start": "2026年初", "end": "present",
     "rank": "正处级", "note": "主持市政府及党组全面工作，分管审计局"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "2026年初", "end": "present",
     "rank": "副处级", "note": "市委副书记、市长"},

    # 王国峰 张丽芬 陈宇
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start": "", "end": "present",
     "rank": "副处级", "note": "2026-04-28 出席人武部任职会"},
    {"person_id": 4, "org_id": 1, "title": "市委常委、组织部部长", "start": "", "end": "present",
     "rank": "副处级", "note": "2026-04-28 出席人武部任职会"},
    {"person_id": 5, "org_id": 2, "title": "市政府党组副书记（常务副市长）", "start": "", "end": "present",
     "rank": "副处级", "note": "负责政府常务，兼任辽宁灯塔经济开发区管委会主任"},

    # 副市长
    {"person_id": 6, "org_id": 2, "title": "市委常委、市政府副市长", "start": "", "end": "present",
     "rank": "副处级", "note": "负责农业农村、水利、生态环境等"},
    {"person_id": 7, "org_id": 2, "title": "市政府副市长、市公安局局长", "start": "", "end": "present",
     "rank": "副处级", "note": "负责公安、司法、社会稳定等"},
    {"person_id": 7, "org_id": 5, "title": "市公安局局长", "start": "", "end": "present",
     "rank": "正科级", "note": "兼任市公安局局长"},
    {"person_id": 8, "org_id": 2, "title": "市政府副市长", "start": "", "end": "present",
     "rank": "副处级", "note": "负责教育、文旅、卫健"},
    {"person_id": 9, "org_id": 2, "title": "市政府副市长", "start": "", "end": "present",
     "rank": "副处级", "note": "负责工业信息化、大数据、市场监管"},
    {"person_id": 10, "org_id": 2, "title": "市政府副市长", "start": "", "end": "present",
     "rank": "副处级", "note": "负责科技、金融"},
    {"person_id": 11, "org_id": 2, "title": "市政府副市长", "start": "", "end": "present",
     "rank": "副处级", "note": "负责教育、民政、文旅"},
    {"person_id": 12, "org_id": 2, "title": "市政府副市长", "start": "", "end": "present",
     "rank": "副处级", "note": "负责自然资源、住建、交通"},
    {"person_id": 13, "org_id": 2, "title": "参与市政府分工的市级领导", "start": "", "end": "present",
     "rank": "副处级", "note": "负责商务、招商引资"},

    # 人大 / 政协
    {"person_id": 14, "org_id": 3, "title": "市人大常委会主任", "start": "", "end": "present",
     "rank": "正处级", "note": "2025-02 确认"},
    {"person_id": 15, "org_id": 4, "title": "市政协主席", "start": "", "end": "present",
     "rank": "正处级", "note": "2025-02 确认"},

    # 前任
    {"person_id": 16, "org_id": 1, "title": "市委书记", "start": "待查", "end": "约2026年初",
     "rank": "正处级", "note": "2025-07-23 仍任市委书记; 约2026 卸任"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "市委书记与市长党政主要领导搭档", "overlap_org": "中共灯塔市委员会/灯塔市人民政府",
     "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "陈丹由市长转任书记，郑立黔接任市长", "overlap_org": "灯塔市人民政府",
     "overlap_period": "2026年"},

    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "市委书记与市委副书记", "overlap_org": "中共灯塔市委员会", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "市委书记与组织部长", "overlap_org": "中共灯塔市委员会", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "市委书记与常务副市长", "overlap_org": "中共灯塔市委员会/灯塔市人民政府", "overlap_period": "2026年"},

    {"person_a": 2, "person_b": 5, "type": "overlap",
     "context": "市长与常务副市长政府班子", "overlap_org": "灯塔市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "市长与副市长",
     "overlap_org": "灯塔市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "市长与副市长（公安局长）",
     "overlap_org": "灯塔市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "市长与副市长",
     "overlap_org": "灯塔市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "市长与副市长",
     "overlap_org": "灯塔市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "市长与副市长",
     "overlap_org": "灯塔市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "市长与副市长",
     "overlap_org": "灯塔市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "市长与副市长",
     "overlap_org": "灯塔市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "市长与参与分工市级领导",
     "overlap_org": "灯塔市人民政府", "overlap_period": "2026年"},

    {"person_a": 1, "person_b": 14, "type": "overlap", "context": "市委书记与人大主任（四套班子）",
     "overlap_org": "灯塔市", "overlap_period": "2025-2026年"},
    {"person_a": 1, "person_b": 15, "type": "overlap", "context": "市委书记与政协主席（四套班子）",
     "overlap_org": "灯塔市", "overlap_period": "2025-2026年"},

    {"person_a": 16, "person_b": 1, "type": "predecessor_successor",
     "context": "前任书记聂锦春与现任书记陈丹交接", "overlap_org": "中共灯塔市委员会",
     "overlap_period": "2025-2026年"},
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "市长与市委组织部长（市委常委）", "overlap_org": "中共灯塔市委员会", "overlap_period": "2026年"},
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════


def make_source_register() -> list[dict]:
    return [
        {"id": "S001", "title": "中国共产党灯塔市第八次代表大会开幕",
         "url": "http://www.dengta.gov.cn/zwzx/002001/20260729/f660a8dc-83d5-4c38-b063-744003765d65.html",
         "publisher": "灯塔市人民政府", "published_at": "2026-07-29", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "确认陈丹代表第七届市委作报告并主持大会，为现任市委书记"},
        {"id": "S002", "title": "灯塔市人武部党委第一书记任职大会召开",
         "url": "http://www.dengta.gov.cn/zwzx/002001/20260429/9d4d2ff-2756-8938-f4381361893d.html",
         "publisher": "灯塔市人民政府门户", "published_at": "2026-04-29", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "确认陈丹=市委书记/人武部第一书记; 郑立黔=市委副书记/市长; 王国峰=市委副书记; 张丽芬=组织部长"},
        {"id": "S003", "title": "领导信息——市长：郑立黔",
         "url": "http://www.dengta.gov.cn/govxxgk/LYDTS/2021-02-20/161380105112868.html",
         "publisher": "灯塔市人民政府办公室", "published_at": "2026-04-17", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "郑立黔：男，汉族，1978年1月生，在职研究生学历，工商管理硕士，中共党员，市委副书记、市长、市政府党组书记"},
        {"id": "S004", "title": "灯塔市人民政府办公室关于市政府领导同志分工的通知（2026年第1期，1-26发布）",
         "url": "http://www.dengta.gov.cn/govxxgk/LYDTS/2026-01-26/d6b4db8d-b2b4-42b8-8ac9-677d6d9e4b2e8.html",
         "publisher": "灯塔市人民政府办公室", "published_at": "2026-01-26", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "2026-01 市政府分工：陈丹为市长、陈宇为党组副书记常务，荣/明/金/孟/乔/苗等为副市长"},
        {"id": "S005", "title": "灯塔全面振兴新突破三年行动攻坚之年总结暨决战之年动员会召开",
         "url": "http://www.dengta.gov.cn/zwzx/002001/20250220/2af0d152-b321-4dc0-b6ad-2455d7c6cf1f.html",
         "publisher": "灯塔市人民政府门户", "published_at": "2025-02-19", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "聂锦春为市委书记(2025-02)，陈丹为市长；梁晓春与人主，张宁为政协主席"},
        {"id": "S006", "title": "聂锦春为全市年轻干部代表讲授学习教育专题党课并座谈",
         "url": "http://www.dengta.gov.cn/zwzx/002001/20250725/3e87f91-4c21-90d6-8e93-b8bcf08f2188.html",
         "publisher": "灯塔市人民政府门户", "published_at": "2025-07-25", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "2025-07-23 聂锦春为市委书记；出席有 陈宇、张丽芬等"},
        {"id": "S007", "title": "灯塔市人民政府网站领导信息（govxxgk 领导班子）",
         "url": "http://www.dengta.gov.cn/govxxgk/LYDTS/",
         "publisher": "灯塔市人民政府办公室", "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "各副市长出生信息/学历分页，供检索"},
    ]


def generate_person_json(job: str, name: str) -> dict:
    """Generate a single person-graph JSON for 陈丹 (书记) and 郑立黔 (市长)."""
    if name == "陈丹":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "辽宁省", "city": "辽阳市", "region": "灯塔市", "job": job,
                "task_id": "liaoning_灯塔市", "time_focus": "2025-2026",
            },
            "identity": {
                "person_id": "dengta_chen_dan", "name": "陈丹", "aliases": [],
                "gender": "男", "ethnicity": "待查", "birth": "", "birthplace": "",
                "native_place": "",
                "education": [{"period": "", "institution": "待查", "major": "", "degree": "",
                               "study_type": "unknown", "source_ids": []}],
                "party_join": "中共党员", "work_start": "",
                "dedupe_keys": {
                    "name_birth": "陈丹_unknown",
                    "official_profile_url": "http://www.dengta.gov.cn/zwzx/002001/20260729/f660a8dc-83d5-4c38-b063-744003765d65.html",
                },
            },
            "current_status": {
                "current_post": "市委书记", "current_org": "中国共产党灯塔市委员会",
                "administrative_rank": "正处级（县级市委书记）", "as_of": AS_OF,
                "is_current_confirmed": True, "source_ids": ["S001", "S002"],
            },
            "career_timeline": [
                {"start": "2026年初", "end": "present", "org": "中共灯塔市委员会", "title": "市委书记",
                 "level": "县处级", "location": "灯塔市", "system": "party", "rank": "正处级",
                 "is_key_promotion": True,
                 "notes": "2026-04-28 兼任市人武部党委书记第一书记，2026-07-28 第八次党代会开幕并作市委工作报告",
                 "confidence": "confirmed", "source_ids": ["S001", "S002"]},
                {"start": "约2023年前后", "end": "2026年初", "org": "灯塔市人民政府", "title": "市政府党组书记、市长",
                 "level": "县处级", "location": "灯塔市", "system": "government", "rank": "正处级",
                 "is_key_promotion": True,
                 "notes": "2023-02 以市长身份受访；2026-01 市政府分工仍列名市长",
                 "confidence": "confirmed", "source_ids": ["S004"]},
                {"start": "约2018年", "end": "约2023年", "org": "灯塔市人民政府", "title": "市委常委、常务副市长",
                 "level": "县处级", "location": "灯塔市", "system": "government", "rank": "副处级",
                 "is_key_promotion": False,
                 "notes": "2019-05 以市委常委、常务副市长身份调研市民政系统",
                 "confidence": "confirmed", "source_ids": []},
                {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "level": "",
                 "location": "", "system": "other", "rank": "", "is_key_promotion": False,
                 "notes": "任常务副市长前的出生、籍贯、学历、入党、工作起始等公开资料未检索到",
                 "confidence": "unverified", "source_ids": []},
            ],
            "organizations": [
                {"name": "中共灯塔市委员会", "role": "市委书记"},
                {"name": "灯塔市人民政府", "role": "市长（前任）"},
            ],
            "relationships": [
                {"person": "郑立黔", "person_id": "dengta_zhengliqian", "relationship_type": "co_leadership",
                 "strength": "strong", "evidence": "市委书记与市长搭档", "overlap_org": "灯塔市",
                 "overlap_period": "2026-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
                {"person": "王国峰", "person_id": "dengta_wangguofeng", "relationship_type": "co_leadership",
                 "strength": "medium", "evidence": "市委常委会（副书记）", "overlap_org": "灯塔市",
                 "overlap_period": "2026-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
                {"person": "遨锦春", "person_id": "dengta_niejinchun", "relationship_type": "predecessor_successor",
                 "strength": "medium", "evidence": "前任市委书记", "overlap_org": "灯塔市",
                 "overlap_period": "2025-2026", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005", "S006"]},
            ],
            "governance_record": [
                {"period": "2026-07", "domain": "party", "achievement_or_event": "主持第八次党代会并作市委工作报告",
                 "role_in_event": "市委书记", "measurable_outcome": "", "location": "灯塔市",
                 "confidence": "confirmed", "source_ids": ["S001"]},
            ],
            "professional_profile": {
                "primary_specializations": ["经济/产业招商", "区域发展政策"],
                "secondary_specializations": [],
                "career_pattern": "local_ladder",
                "systems_experience": ["government", "party"],
                "geographic_pattern": ["辽阳市灯塔市"],
                "promotion_velocity": {"summary": "同城由常务副市长→市长→市委书记逐级提升",
                                       "notable_fast_promotions": ["市长→市委书记（约2025-2026）"]},
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "pragmatic_oriented", "evidence": "多次以市长身份部署三年行动决胜任务",
                     "confidence": "plausible", "source_ids": []}],
                "speech_themes": ["中国式现代化灯塔实践", "全面振兴", "高质量发展"],
                "management_signals": [], "caveat": "工作风格依据公开记录推测。",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "截至2026-08未发现公开纪律处分或负面报道",
                 "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": make_source_register(),
            "confidence_summary": {
                "identity": "partial", "current_role": "confirmed", "career_completeness": "partial",
                "relationship_confidence": "high", "biggest_gap": "陈丹出生年、籍贯、教育、任常务副市长前履历均未知"},
            "open_questions": [
                {"priority": "critical", "question": "陈丹出生年月、籍贯、教育背景、入党时间",
                 "why_it_matters": "基本身份信息, 档案去重", "suggested_queries": ["陈丹 灯塔市 简历"],
                 "last_attempted": AS_OF},
                {"priority": "high", "question": "陈丹任常务副市长（约2018年）前的职业履历",
                 "why_it_matters": "判断全市工作履历与成长路径", "suggested_queries": ["陈丹 灯塔 副市长 任职公示"],
                 "last_attempted": AS_OF},
                {"priority": "medium", "question": "前任书记聂锦春卸任后的去向与交接时点",
                 "why_it_matters": "市级干部交流去向", "suggested_queries": ["严锦春 卸任 灯塔"],
                 "last_attempted": AS_OF},
            ],
        }
    if name == "郑立黔":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "辽宁省", "city": "辽阳市", "region": "灯塔市", "job": job,
                "task_id": "liaoning_灯塔市", "time_focus": "2025-2026",
            },
            "identity": {
                "person_id": "dengta_zhengliqian", "name": "郑立黔", "aliases": [],
                "gender": "男", "ethnicity": "汉族", "birth": "1978年1月", "birthplace": "",
                "native_place": "",
                "education": [{"period": "", "institution": "在职（工商管理硕士）", "major": "工商管理",
                               "degree": "硕士", "study_type": "part_time", "source_ids": ["S003"]}],
                "party_join": "中共党员", "work_start": "",
                "dedupe_keys": {
                    "name_birth": "郑立黔_1978-01",
                    "official_profile_url": "http://www.dengta.gov.cn/govxxgk/LYDTS/2021-02-20/161380105112868.html",
                },
            },
            "current_status": {
                "current_post": "市长", "current_org": "灯塔市人民政府（市委副书记、市政府党组书记）",
                "administrative_rank": "正处级（县级市市长）", "as_of": AS_OF,
                "is_current_confirmed": True, "source_ids": ["S002", "S003"],
            },
            "career_timeline": [
                {"start": "2026年初", "end": "present", "org": "灯塔市人民政府", "title": "市政府党组书记、市长",
                 "level": "县处级", "location": "灯塔市", "system": "government", "rank": "正处级",
                 "is_key_promotion": True,
                 "notes": "领导信息页2026-04-17；2026-04-28 以市长身份人道会出席",
                 "confidence": "confirmed", "source_ids": ["S002", "S003"]},
                {"start": "2026年初", "end": "present", "org": "中共灯塔市委员会", "title": "市委副书记",
                 "level": "县处级", "location": "灯塔市", "system": "party", "rank": "副处级",
                 "is_key_promotion": False, "notes": "市委副书记、市长", "confidence": "confirmed",
                 "source_ids": ["S002", "S003"]},
                {"start": "unknown", "end": "2026年前", "org": "辽阳市域", "title": "后备/副职",
                 "level": "", "location": "辽阳市", "system": "other", "rank": "",
                 "is_key_promotion": False,
                 "notes": "搜索索引中出现在弓长岭区/河道治理会议（2021-2024）可减跨县区交流可能，未证实",
                 "confidence": "plausible", "source_ids": []},
            ],
            "organizations": [
                {"name": "灯塔市人民政府", "role": "市长、市政府党组书记"},
                {"name": "中共灯塔市委员会", "role": "市委副书记"},
            ],
            "relationships": [
                {"person": "陈丹", "person_id": "dengta_chen_dan", "relationship_type": "co_leadership",
                 "strength": "strong", "evidence": "市委书记与市长搭档", "overlap_org": "灯塔市",
                 "overlap_period": "2026-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
                {"person": "陈宇", "person_id": "dengta_chen_qi", "relationship_type": "co_leadership",
                 "strength": "medium", "evidence": "市政府常务工作任配班", "overlap_org": "灯塔市人民政府",
                 "overlap_period": "2026-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
            ],
            "governance_record": [
                {"period": "2026-04", "domain": "government", "achievement": "出任市长并出席人武部第一书记会",
                 "role": "市长", "measurable_outcome": "", "location": "灯塔市",
                 "confidence": "confirmed", "source_ids": ["S002"]},
            ],
            "professional_profile": {
                "primary_specializations": ["财政、审计", "政府行政管理"],
                "secondary_specializations": [],
                "career_pattern": "local_ladder",
                "systems_experience": ["government"],
                "geographic_pattern": ["辽阳市"],
                "promotion_velocity": {"summary": "2026年初担任灯塔市长，此前履历不详",
                                       "notable_fast_promotions": []},
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "unknown", "evidence": "公开报道有限", "confidence": "unverified", "source_ids": []}],
                "speech_themes": [], "management_signals": [], "caveat": "工作风格依据公开记录推测。",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "截至2026-08未发现公开纪律问题。",
                 "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": make_source_register(),
            "confidence_summary": {
                "identity": "confirmed", "current_role": "confirmed", "career_completeness": "partial",
                "relationship_confidence": "high", "biggest_gap": "郑立黔源于2026前完整履历（籍贯、此前职务）",
            },
            "open_questions": [
                {"priority": "critical", "question": "郑立黔任灯塔市长前（2026前）任职于辽阳的县区/系统",
                 "why_it_matters": "判断升迁路径与跨县区交流", "suggested_queries": ["郑立黔 简历 辽阳市长"],
                 "last_attempted": AS_OF},
                {"priority": "high", "question": "郑立黔籍贯与毕业院校详情",
                 "why_it_matters": "档案身份", "suggested_queries": ["郑立黔 出生 简历"],
                 "last_attempted": AS_OF},
            ],
        }
    return {}


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    person_configs = [
        ("市委书记", "陈丹"),
        ("市长", "郑立黔"),
    ]

    for job, name in person_configs:
        data = generate_person_json(job, name)
        if data:
            fname = f"{TODAY}-辽宁省-辽阳市-{job}-{name}.json"
            fpath = PERSONS_DIR / fname
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  Wrote {fpath}")

    print(f"\nDone. Output files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Person JSONs in: {PERSONS_DIR}")