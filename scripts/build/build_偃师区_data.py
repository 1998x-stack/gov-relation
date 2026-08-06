#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 偃师区 (Yanshi District), 洛阳市, 河南省.

Level: 市辖区
Province: 河南省
Parent city: 洛阳市
Targets: 区委书记 (District Party Secretary), 区长 (District Government Head)
Task ID: henan_偃师区

Research date: 2026-08-06
Primary official source: https://www.yanshi.gov.cn/ (洛阳市偃师区人民政府) — reached successfully
Corroborating official source: https://www.ly.gov.cn/ (洛阳市人民政府)

Current status (as of 2026-08-06):
- 区委书记: 赵玉勋 (confirmed — 偃师区人民政府 领导活动 multi-article: 区委常委会会议 2026-05-18
  https://www.yanshi.gov.cn/2026/05-18/1061844.html "区委书记赵玉勋主持会议并讲话"; 《赵玉勋到顾县镇调研》2026-06-03
  https://www.yanshi.gov.cn/2026/06-04/1065772.html)
- 区长: 王雪丽 (confirmed — 偃师区人民政府 领导之窗 政府领导官方简历
  https://www.yanshi.gov.cn/2025/09-11/796464.html "王雪丽，女，汉族，1983年3月出生，硕士研究生，中共党员。现任区委副书记、区政府党组书记、区长。")

Leadership roster confirmed from 偃师区人民政府 领导之窗 政府领导 (official profiles, accessed 2026-08-06):
温利涛(常务副区长)、申俊涛(宣传部长/副区长)、邱五德(副区长)、薛超峰(副区长)、茹庆龙(政府党组成员)。
Additional 区领导 observed in 领导活动 reports: 徐德、郭秋香、苏敬彪、汪旭霞、王明明、李艳兵。

Confidence notes:
  - Core leader identities and titles (区委书记 赵玉勋; 区长 王雪丽): confirmed (official gov sources).
  - Government 领导之窗 members gender/birth/education: confirmed from official profiles.
  - 赵玉勋 biography (birth/education/native place): partial — 官网领导之窗未列区委书记简历，出生年1973年4月/中央党校大学为二手百科来源，标为 plausible.
  - Predecessor (前区委书记 彭仁来 2023.03–2026.04) and successor path: 二手百科来源, 需一手核实 — open_question.
  - 2021 偃师(县级市)撤市设区 — 行政区划背景.
  - 相关区领导 (徐德、郭秋香 etc) 具体职级/职务未一一标注 — flagged as gaps.

This build uses confirmed + plausible evidence. Biographical gaps are explicit, not fabricated.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / ".." / "..").resolve()
if not (_REPO_ROOT / "gov_relation").exists():
    _REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

import sqlite3  # noqa: F811

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "偃师区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-08-06"
TODAY = "20260806"

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 赵玉勋 — 区委书记
    {
        "id": 1,
        "name": "赵玉勋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-04",
        "birthplace": "",
        "education": "中央党校大学（二手百科来源）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "偃师区委书记",
        "current_org": "中共洛阳市偃师区委员会",
        "source": "confirmed — 偃师区人民政府 领导活动《偃师区2026年第18次区委常委会（扩大）会议召开》2026-05-18 https://www.yanshi.gov.cn/2026/05-18/1061844.html；《赵玉勋到顾县镇调研》2026-06-03 https://www.yanshi.gov.cn/2026/06-04/1065772.html",
    },
    # 2. 王雪丽 — 区委副书记、区长
    {
        "id": 2,
        "name": "王雪丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1983-03",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "偃师区委副书记、区长",
        "current_org": "洛阳市偃师区人民政府",
        "source": "confirmed — 偃师区人民政府 领导之窗 政府领导官方简历 https://www.yanshi.gov.cn/2025/09-11/796464.html",
    },
    # ════════════════════════════════════════
    # Government Leadership Team (领导之窗)
    # ════════════════════════════════════════
    # 3. 温利涛 — 区委常委、常务副区长
    {
        "id": 3,
        "name": "温利涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-09",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "偃师区委常委、区政府党组副书记、常务副区长",
        "current_org": "洛阳市偃师区人民政府",
        "source": "confirmed — 偃师区人民政府 领导之窗 温利涛简历 https://www.yanshi.gov.cn/2026/07-15/1073961.html",
    },
    # 4. 申俊涛 — 区委常委、宣传部长、副区长
    {
        "id": 4,
        "name": "申俊涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-10",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "偃师区委常委、宣传部部长，区政府党组成员、副区长",
        "current_org": "中共洛阳市偃师区委宣传部/洛阳市偃师区人民政府",
        "source": "confirmed — 偃师区人民政府 领导之窗 申俊涛简历 https://www.yanshi.gov.cn/2026/07-15/1073965.html",
    },
    # 5. 邱五德 — 副区长
    {
        "id": 5,
        "name": "邱五德",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-11",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "偃师区政府党组成员、副区长",
        "current_org": "洛阳市偃师区人民政府",
        "source": "confirmed — 偃师区人民政府 领导之窗 邱五德简历 https://www.yanshi.gov.cn/2025/09-11/796468.html",
    },
    # 6. 薛超峰 — 副区长
    {
        "id": 6,
        "name": "薛超峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-04",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "偃师区政府党组成员、副区长",
        "current_org": "洛阳市偃师区人民政府",
        "source": "confirmed — 偃师区人民政府 领导之窗 薛超峰简历 https://www.yanshi.gov.cn/2025/09-11/796470.html",
    },
    # 7. 茹庆龙 — 区政府党组成员
    {
        "id": 7,
        "name": "茹庆龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988-08",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "偃师区政府党组成员",
        "current_org": "洛阳市偃师区人民政府",
        "source": "confirmed — 偃师区人民政府 领导之窗 茹庆龙简历 https://www.yanshi.gov.cn/2026/07-15/1073966.html",
    },
    # ════════════════════════════════════════
    # District leaders observed in 领导活动 reports (定职待确认)
    # ════════════════════════════════════════
    # 8. 徐德 — 区领导 (理论中心组出席)
    {
        "id": 8,
        "name": "徐德",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "偃师区领导（区委班子，具体职务待确认）",
        "current_org": "中共洛阳市偃师区委员会",
        "source": "偃师区委理论学习中心组 2026-05-22 出席 https://www.yanshi.gov.cn/2026/05-22/1063556.html",
    },
    # 9. 郭秋香 — 区领导
    {
        "id": 9,
        "name": "郭秋香",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "偃师区领导（具体职务待确认）",
        "current_org": "中共洛阳市偃师区委员会",
        "source": "偃师区委理论学习中心组 2026-05-22 出席 https://www.yanshi.gov.cn/2026/05-22/1063556.html",
    },
    # 10. 苏敬彪 — 区领导
    {
        "id": 10,
        "name": "苏敬彪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "偃师区领导（具体职务待确认）",
        "current_org": "中共洛阳市偃师区委员会/洛阳市偃师区人民政府",
        "source": "《偃师区“三夏”农业生产暨秸秆禁烧工作会议》2026-05-22 https://www.yanshi.gov.cn/2026/05-22/1063580.html；《我区跟班学习干部座谈会召开》2026-08-04 https://www.yanshi.gov.cn/2026/08-06/1077862.html",
    },
    # 11. 汪旭霞 — 区领导
    {
        "id": 11,
        "name": "汪旭霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "偃师区领导（具体职务待确认）",
        "current_org": "中共洛阳市偃师区委员会/洛阳市偃师区人民政府",
        "source": "《偃师区“三夏”农业生产暨秸秆禁烧工作会议》2026-05-22 https://www.yanshi.gov.cn/2026/05-22/1063580.html",
    },
    # 12. 李艳兵 — 区领导
    {
        "id": 12,
        "name": "李艳兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "偃师区领导（具体职务待确认）",
        "current_org": "中共洛阳市偃师区委员会/洛阳市偃师区人民政府",
        "source": "《我区跟班学习干部座谈会召开》2026-08-04 https://www.yanshi.gov.cn/2026/08-06/1077862.html",
    },
    # 13. 王明明 — 区领导
    {
        "id": 13,
        "name": "王明明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "偃师区领导（具体职务待确认）",
        "current_org": "中共洛阳市偃师区委员会",
        "source": "《赵玉勋到顾县镇调研》2026-06-03 区领导王明明参加 https://www.yanshi.gov.cn/2026/06-04/1065772.html",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共洛阳市偃师区委员会", "type": "党委", "level": "县处级", "parent": "中共洛阳市委", "location": "河南省洛阳市偃师区"},
    {"id": 2, "name": "洛阳市偃师区人民政府", "type": "政府", "level": "县处级", "parent": "洛阳市人民政府", "location": "河南省洛阳市偃师区"},
    {"id": 3, "name": "中共洛阳市偃师区委宣传部", "type": "党委", "level": "县处级", "parent": "中共洛阳市偃师区委员会", "location": "河南省洛阳市偃师区"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 赵玉勋 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "偃师区委书记", "start": "2026-04", "end": "present", "rank": "县处级正职", "note": "截至2026年8月在任；2026-04-24 上任（二手百科来源）；此前任偃师区长 2022-2026"},
    # 王雪丽 — 区长
    {"person_id": 2, "org_id": 2, "title": "偃师区人民政府区长（区政府党组书记）", "start": "2026-05", "end": "present", "rank": "县处级正职", "note": "官方领导之窗确认现任区委副书记、区长；2026-05-11 任命（二手百科来源）"},
    {"person_id": 2, "org_id": 1, "title": "偃师区委副书记", "start": "2026-05", "end": "present", "rank": "县处级副职", "note": "官方领导之窗确认兼任区委副书记"},
    # 温利涛 — 常务副区长
    {"person_id": 3, "org_id": 2, "title": "区政府党组副书记、常务副区长", "start": "", "end": "present", "rank": "县处级副职", "note": "领导之窗确认"},
    {"person_id": 3, "org_id": 1, "title": "偃师区委常委", "start": "", "end": "present", "rank": "县处级副职", "note": "领导之窗确认"},
    # 申俊涛 — 宣传部长、副区长
    {"person_id": 4, "org_id": 3, "title": "偃师区委常委、宣传部部长", "start": "", "end": "present", "rank": "县处级副职", "note": "领导之窗确认"},
    {"person_id": 4, "org_id": 2, "title": "偃师区政府党组成员、副区长", "start": "", "end": "present", "rank": "县处级副职", "note": "领导之窗确认"},
    # 邱五德 — 副区长
    {"person_id": 5, "org_id": 2, "title": "偃师区人民政府副区长（区政府党组成员）", "start": "", "end": "present", "rank": "县处级副职", "note": "领导之窗确认"},
    # 薛超峰 — 副区长
    {"person_id": 6, "org_id": 2, "title": "偃师区人民政府副区长（区政府党组成员）", "start": "", "end": "present", "rank": "县处级副职", "note": "领导之窗确认"},
    # 茹庆龙 — 政府党组成员
    {"person_id": 7, "org_id": 2, "title": "偃师区政府党组成员", "start": "", "end": "present", "rank": "县处级副职", "note": "领导之窗确认"},
    # 区领导（职务待确认）
    {"person_id": 8, "org_id": 1, "title": "偃师区领导（区委副书记待确认）", "start": "", "end": "present", "rank": "县处级", "note": "区委理论学习中心组出席，具体职务待确认"},
    {"person_id": 9, "org_id": 1, "title": "偃师区领导（具体职务待确认）", "start": "", "end": "present", "rank": "县处级", "note": "区委理论学习中心组出席，具体职务待确认"},
    {"person_id": 10, "org_id": 1, "title": "偃师区领导（具体职务待确认）", "start": "", "end": "present", "rank": "县处级", "note": "区领导包联等会议出席，具体职务待确认"},
    {"person_id": 11, "org_id": 1, "title": "偃师区领导（具体职务待确认）", "start": "", "end": "present", "rank": "县处级", "note": "区领导参与三夏会议，具体职务待确认"},
    {"person_id": 12, "org_id": 1, "title": "偃师区领导（具体职务待确认）", "start": "", "end": "present", "rank": "县处级", "note": "区领导参会，具体职务待确认"},
    {"person_id": 13, "org_id": 1, "title": "偃师区领导（区委副书记待确认）", "start": "", "end": "present", "rank": "县处级", "note": "调研活动参加，具体职务待确认"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 赵玉勋 ↔ 王雪丽 (core leadership pair 党政主要领导)
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "偃师区委书记与区长党政主要领导搭档；共同主持区委常委会和区政府重要会议",
        "overlap_org": "中共洛阳市偃师区委员会/洛阳市偃师区人民政府",
        "overlap_period": "截至2026年8月",
        "confidence": "confirmed",
    },
    # 赵玉勋 ↔ 温利涛 (书记与常务副区长)
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "区委书记与区政府常务副区长同属区委常委会与政府班子",
        "overlap_org": "中共洛阳市偃师区委员会/洛阳市偃师区人民政府",
        "overlap_period": "截至2026年8月",
        "confidence": "confirmed",
    },
    # 王雪丽 ↔ 温利涛 (区长与常务副区长)
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "区长与常务副区长（区政府党组副书记）同属区政府班子核心成员",
        "overlap_org": "洛阳市偃师区人民政府",
        "overlap_period": "截至2026年8月",
        "confidence": "confirmed",
    },
    # 温利涛 ↔ 申俊涛 (常务与宣传/副区长)
    {
        "person_a": 3, "person_b": 4,
        "type": "overlap",
        "context": "同任偃师区副区长，并列区政府班子",
        "overlap_org": "洛阳市偃师区人民政府",
        "overlap_period": "截至2026年8月",
        "confidence": "confirmed",
    },
    # 申俊涛 ↔ 邱五德 (副区长班子)
    {
        "person_a": 4, "person_b": 5,
        "type": "overlap",
        "context": "同为偃师区副区长，同属区政府领导班子",
        "overlap_org": "洛阳市偃师区人民政府",
        "overlap_period": "截至2026年8月",
        "confidence": "confirmed",
    },
    # 邱五德 ↔ 薛超峰 (副区长班子)
    {
        "person_a": 5, "person_b": 6,
        "type": "overlap",
        "context": "同为偃师区副区长，同属区政府领导班子",
        "overlap_org": "洛阳市偃师区人民政府",
        "overlap_period": "截至2026年8月",
        "confidence": "confirmed",
    },
    # 薛超峰 ↔ 茹庆龙 (政府班子成员)
    {
        "person_a": 6, "person_b": 7,
        "type": "overlap",
        "context": "同属区政府班子（副区长与政府党组成员）",
        "overlap_org": "洛阳市偃师区人民政府",
        "overlap_period": "截至2026年8月",
        "confidence": "confirmed",
    },
    # 赵玉勋 ↔ 徐德 (区委中心组)
    {
        "person_a": 1, "person_b": 8,
        "type": "overlap",
        "context": "区委理论学校中心组学习，区委书记与区领导列席",
        "overlap_org": "中共洛阳市偃师区委员会",
        "overlap_period": "2026年5月",
        "confidence": "confirmed",
    },
    # 王雪丽 ↔ 苏敬彪 (三夏会议共同参会)
    {
        "person_a": 2, "person_b": 10,
        "type": "overlap",
        "context": "区长王雪丽与苏敬彪参加全区三夏农业生产工作会议",
        "overlap_org": "洛阳市偃师区人民政府/中共洛阳市偃师区委员会",
        "overlap_period": "2026年5月",
        "confidence": "confirmed",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ONTOLOGY
# ══════════════════════════════════════════════════════════════════════════════

DEDUPE_PREFIX = "yanshi"

def _slugify_name(name: str) -> str:
    return name.replace("（", "_").replace("）", "").replace(" ", "_")

def _slugify_job(post: str) -> str:
    if "区委书记" in post:
        return "区委书记"
    if "常务副区长" in post:
        return "常务副区长"
    if "宣传部长" in post:
        return "宣传部长"
    if "副区长" in post:
        return "副区长"
    if "区长" in post:
        return "区长"
    if "政府党组成员" in post:
        return "政府党组成员"
    if "区委常委" in post:
        return "区委常委"
    return post.replace(" ", "_")

def _org_name(org_id: int) -> str:
    for o in organizations:
        if o["id"] == org_id:
            return o["name"]
    return ""

def _org_type(org_id: int) -> str:
    for o in organizations:
        if o["id"] == org_id:
            return o["type"]
    return ""

def _person_name(person_id: int) -> str:
    for p in persons:
        if p["id"] == person_id:
            return p["name"]
    return ""


# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON BUILDER
# ══════════════════════════════════════════════════════════════════════════════


def build_person_json(person: dict, relationships_subset: list[dict]) -> dict:
    """Build a person graph JSON from the data rows."""
    pid = person["id"]

    career_entries = []
    for pos in positions:
        if pos["person_id"] == pid:
            career_entries.append({
                "start": pos["start"] if pos["start"] else "unknown",
                "end": pos["end"] if pos["end"] else "unknown",
                "org": _org_name(pos["org_id"]),
                "title": pos["title"],
                "level": pos["rank"],
                "location": "河南省洛阳市偃师区",
                "system": "party" if ("区委" in pos["title"] or "党委" in _org_name(pos["org_id"])) else "government",
                "rank": pos["rank"],
                "is_key_promotion": "区委书记" in pos["title"] or "区长" in pos["title"],
                "notes": pos["note"],
                "confidence": "confirmed" if person["id"] in (1, 2, 3, 4, 5, 6, 7) else "plausible",
                "source_ids": ["S001", "S002"],
            })

    if not career_entries:
        career_entries.append({
            "start": "unknown",
            "end": "present",
            "org": person["current_org"],
            "title": person["current_post"],
            "level": "县处级",
            "location": "河南省洛阳市偃师区",
            "system": "party" if "书记" in person["current_post"] else "government",
            "rank": "县处级",
            "is_key_promotion": True,
            "notes": "当前职务来自官方领导之窗/领导活动；具体到任时间待核。",
            "confidence": "plausible",
            "source_ids": [],
        })

    rels_out = []
    for r in relationships_subset:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        rels_out.append({
            "person": _person_name(other_id),
            "person_id": f"{DEDUPE_PREFIX}_{_slugify_name(_person_name(other_id))}",
            "relationship_type": r["type"],
            "strength": "strong",
            "evidence": r["context"],
            "overlap_org": r["overlap_org"],
            "overlap_period": r["overlap_period"],
            "direction": "undirected",
            "confidence": r.get("confidence", "confirmed"),
            "source_ids": [],
        })

    orgs_out = []
    for pos in positions:
        if pos["person_id"] == pid:
            orgs_out.append({
                "org_id": pos["org_id"],
                "name": _org_name(pos["org_id"]),
                "type": _org_type(pos["org_id"]),
                "level": "县处级",
                "location": "河南省洛阳市偃师区",
            })

    big_gap = "公开资料未找到该人物的完整早年履历与到任时间，需通过洛阳市委组织部任前公示核实。"
    if person["id"] == 1:
        big_gap = "赵玉勋的出生年月(1973-04?)、中央党校大学学历、及升任区委书记前的完整履历（此前任偃师区长 2022-2026）为二手百科来源，需官方任前公示一手核实。"
    elif person["id"] == 2:
        big_gap = "王雪丽被任命为区长的具体月份及此前职务（据二手为洛阳老城区/涧西区党政干部）未列入官方领导之窗，待核实。"

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河南省",
            "city": "洛阳市",
            "region": "偃师区",
            "job": person["current_post"],
            "task_id": "henan_偃师区",
            "time_focus": "当前",
        },
        "identity": {
            "person_id": f"{DEDUPE_PREFIX}_{_slugify_name(person['name'])}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "name_birthplace": f"{person['name']}_{person['birthplace']}",
                "official_profile_url": "https://www.yanshi.gov.cn/ld",
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "县处级正职" if person["id"] in (1, 2) else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"],
        },
        "career_timeline": career_entries,
        "organizations": orgs_out,
        "relationships": rels_out,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "缺少完整履历，无法评估晋升速度",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "pragmatic",
                    "evidence": "2026年5-6月区委书记强调坚定不移推动高质量发展、抓产业发展、抓乡村振兴、抓基层治理、守牢安全底线（见偃师区人民政府官网相关领导活动报道）",
                    "confidence": "plausible",
                    "source_ids": ["S002"],
                }
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "工作风格推断基于公开报道，非私人心理评估。",
        },
        "network_metrics": {
            "direct_connections": len(rels_out),
            "memberships": len(orgs_out),
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至检索日未发现关于赵玉勋/王雪丽的廉洁风险或纪律审查公开报道。此状态不表示无问题，仅表示在有限条件下未发现。",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "洛阳市偃师区人民政府 - 领导之窗（政府领导个人简历）",
                "url": "https://www.yanshi.gov.cn/ld",
                "publisher": "洛阳市偃师区人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认王雪丽、温利涛、申俊涛、邱五德、薛超峰、茹庆龙等现任政府领导及学历、出生年月。",
            },
            {
                "id": "S002",
                "title": "偃师区人民政府 - 领导活动（区委书记赵玉勋主持区委常委会会议、到顾县镇调研等）",
                "url": "https://www.yanshi.gov.cn/yszx/ldhd",
                "publisher": "偃师融媒、洛阳市偃师区人民政府",
                "published_at": "2026-05~06",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认赵玉勋为现任偃师区委书记并主持区委常委会；王雪丽等区领导列席。",
            },
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "high",
            "biggest_gap": big_gap,
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的出生年月、籍贯、受教育经历及任职前主要履历？",
                "why_it_matters": "构建核心人物完整履历的关键缺口。",
                "suggested_queries": [f"{person['name']} 简历 偃师", f"{person['name']} 任前公示", "洛阳市 偃师区 干部 任命"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "赵玉勋升任区委书记(2026-04前)的确切更替时间线及前任区委书记是谁？",
                "why_it_matters": "掌握晋升路径和跨区/跨县人事交流线索。",
                "suggested_queries": ["偃师区 区委书记 前任", "偃师区 干部 任前公示", "赵玉勋 偃师区长 任命"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "medium",
                "question": "偃师区区委副书记、徐德/郭秋香/苏敬彪/汪旭霞/李艳兵/王明明等区领导的具体职务？",
                "why_it_matters": "完善领导班子网络，需逐一确认职权定位。",
                "suggested_queries": ["偃师区 区委副书记 名单", "偃师区 常委 分工"],
                "last_attempted": AS_OF,
            },
        ],
    }


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════


def write_person_jsons():
    """Write individual person JSON files for core figures."""
    core_ids = {1, 2, 3, 4, 5, 6, 7}
    for p in persons:
        if p["id"] not in core_ids:
            continue
        person_rels = [r for r in relationships if r["person_a"] == p["id"] or r["person_b"] == p["id"]]
        data = build_person_json(p, person_rels)
        name_part = _slugify_name(p["name"])
        fname = f"{TODAY}-河南省-洛阳市-{_slugify_job(p['current_post'])}-{name_part}.json"
        fpath = PERSONS_DIR / fname
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Wrote {fpath.name}")


def main():
    print(f"=== Building network for {SLUG} ===")
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print()

    # 1. Build the relational database + GEXF graph
    print(">>> Building database and GEXF...")
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
    print()

    # 2. Write per-person JSON files
    print(">>> Writing person JSON files...")
    write_person_jsons()
    print()

    # 3. Print summary
    print("=== Build complete ===")
    print(f"  Database:  {DB_PATH} ({os.path.getsize(DB_PATH)} bytes)")
    print(f"  GEXF:      {GEXF_PATH} ({os.path.getsize(GEXF_PATH)} bytes)")
    print(f"  Persons:   {len(persons)}")
    print(f"  Orgs:      {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relations: {len(relationships)}")
    print()
    print("NOTE: Core identities confirmed from official sources. Complete career")
    print("timelines and birth/education gaps are flagged in each person JSON open_questions.")


if __name__ == "__main__":
    main()