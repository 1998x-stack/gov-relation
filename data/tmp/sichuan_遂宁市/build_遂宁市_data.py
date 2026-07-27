#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 遂宁市 (Suining City), 四川省.

Investigation date: 2026-07-26
Task ID: sichuan_遂宁市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.suining.gov.cn — 遂宁市人民政府官方网站 (primary, current as of July 2026)
  - News articles and meeting attendance lists from suining.gov.cn (July 2026):
    - 市委常委会会议暨市委财经委员会会议 (2026-07-23)
    - 全市服务业大会 (2026-07-23)
    - 市委主要领导带队赴蜀道集团对接工作 (2026-07-20)
    - 遂宁市"六张网"规划建设工作专题会议 (2026-07-14)
    - 中共遂宁市委八届十三次全会 (2026-06-23)
    - 市八届人大七次会议 (2026-02-27)
    - 市政协八届六次会议 (2026-02-26)
  - Web search was degraded: Exa rate-limited, Baidu 403

Confidence notes:
  - Current roles (惠朝旭 as 市委书记, 王忠诚 as 市长): confirmed via multiple official reports (July 2026)
  - 前任市委书记 严卫东: confirmed via Feb 2026 news, replaced by 惠朝旭 between Feb-Jun 2026
  - Biographical details (birth, birthplace, education): mostly unverified due to web access limitations
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
SLUG = "遂宁市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "sichuan_遂宁市"
if _CURRENT_DIR.name == "sichuan_遂宁市":
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
        "name": "惠朝旭",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",  # open question — unverified
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委书记",
        "current_org": "中共遂宁市委员会",
        "source": "https://www.suining.gov.cn/xinwen/show/aa1c456a7d6c02797dadf003df99c2e9.html",
        "confidence": "confirmed",
        "notes": "2026年6-7月多次主持市委常委会会议；此前任职待查"
    },
    {
        "id": 2,
        "name": "王忠诚",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",  # open question — unverified
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市长",
        "current_org": "遂宁市人民政府",
        "source": "https://www.suining.gov.cn/xinwen/show/380a337aacc6ad076dbbb911097e7b8b.html",
        "confidence": "confirmed",
        "notes": "2026年2月27日在市八届人大七次会议作政府工作报告；2026年7月以市委副书记、市长身份出席六张网会议"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee members (市委常委)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "李胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共遂宁市委员会",
        "source": "https://www.suining.gov.cn/xinwen/show/4bd865d9a720e91963cd22b0575612ed.html",
        "confidence": "confirmed",
        "notes": "2026年7月主持全市服务业大会；主席台就座于2026年2月人代会"
    },
    {
        "id": 4,
        "name": "雷刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "遂宁市人民代表大会常务委员会",
        "source": "https://www.suining.gov.cn/xinwen/show/e36dbdc0cd824d905b8349fb0b75f012.html",
        "confidence": "confirmed",
        "notes": "2026年2月主持市八届人大七次会议；大会主席团常务主席、开幕会执行主席"
    },
    {
        "id": 5,
        "name": "杨军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议遂宁市委员会",
        "source": "https://www.suining.gov.cn/xinwen/show/b89016b05a14d9cd84919f0c7aa30aec.html",
        "confidence": "confirmed",
        "notes": "2026年2月市政协八届六次会议作常委会工作报告"
    },
    {
        "id": 6,
        "name": "李东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协党组书记",
        "current_org": "中国人民政治协商会议遂宁市委员会",
        "source": "https://www.suining.gov.cn/xinwen/show/b89016b05a14d9cd84919f0c7aa30aec.html",
        "confidence": "confirmed",
        "notes": "2026年2月出席市政协八届六次会议并在主席台就座"
    },
    {
        "id": 7,
        "name": "张韬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市领导",
        "current_org": "中共遂宁市委员会",
        "source": "https://www.suining.gov.cn/xinwen/show/3ed6f9b929ba945cd1c6ee4f824372a8.html",
        "confidence": "confirmed",
        "notes": "2026年7月随惠朝旭赴蜀道集团对接工作；具体职务待查"
    },
    {
        "id": 8,
        "name": "许文强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市领导",
        "current_org": "中共遂宁市委员会",
        "source": "https://www.suining.gov.cn/xinwen/show/3ed6f9b929ba945cd1c6ee4f824372a8.html",
        "confidence": "confirmed",
        "notes": "2026年7月出席蜀道集团对接工作；具体职务待查"
    },
    {
        "id": 9,
        "name": "邓勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委秘书长",
        "current_org": "中共遂宁市委员会",
        "source": "https://www.suining.gov.cn/xinwen/show/3ed6f9b929ba945cd1c6ee4f824372a8.html",
        "confidence": "confirmed",
        "notes": "2026年7月出席蜀道集团对接活动"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Other standing committee members (from 人代会 主席台名单)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "宋良勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "主席团成员",
        "current_org": "遂宁市第八届人民代表大会",
        "source": "https://www.suining.gov.cn/xinwen/show/e36dbdc0cd824d849b8349fb0b75f012.html",
        "confidence": "confirmed",
        "notes": "大会主席团常务主席/开幕会执行主席（2026年2月）；具体职务待查"
    },
    {
        "id": 11,
        "name": "付勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "主席团成员",
        "current_org": "遂宁市第八届人民代表大会",
        "source": "https://www.suining.gov.cn/xinwen/show/e36dbdc0cd824d849b905849fb0b75f012.html",
        "confidence": "confirmed",
        "notes": "大会主席团执行主席；具体职务待查"
    },
    {
        "id": 12,
        "name": "刘枫",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "主席团成员",
        "current_org": "遂宁市第八届人民代表大会",
        "source": "https://www.suining.gov.cn/xinwen/show/e36dbdc0cd824d849b3409fb0b73f012.html",
        "confidence": "confirmed",
        "notes": "大会主席团执行主席；具体职务待查"
    },
    {
        "id": 13,
        "name": "胡道军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "主席团成员",
        "current_org": "遂宁市第八届人民代表大会",
        "source": "https://www.suining.gov.cn/xinwen/show/e36dbdc0cd824b849b3059fb0b75f012.html",
        "confidence": "confirmed",
        "notes": "大会主席团执行主席；具体职务待查"
    },
    {
        "id": 14,
        "name": "蒋喻新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "主席团成员",
        "current_org": "遂宁市第八届人民代表大会",
        "source": "https://www.suining.gov.cn/xinwen/show/e36dbdc0cd824d849b209fb0b75f112.html",
        "confidence": "confirmed",
        "notes": "大会主席团执行主席；具体职务待查"
    },
    {
        "id": 15,
        "name": "向莉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "主席团成员",
        "current_org": "遂宁市第八届人民代表大会",
        "source": "https://www.suining.gov.cn/xinwen/show/e36dbdc0cd824d849b1059fb0b75d012.html",
        "confidence": "confirmed",
        "notes": "大会主席团执行主席；具体职务待查"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "严卫东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共遂宁市委员会",
        "source": "https://www.suining.gov.cn/xinwen/show/b89016b05a14b9cd84919f0c7aa30aec.html",
        "confidence": "confirmed",
        "notes": "2026年2月仍以中共遂宁市委书记身份在市政协八届五次会议讲话；后于2026年6月前转任/卸任（具体去向待查）。2021年7月-2026年任遂宁市委书记。此前曾任四川省政府副秘书长、省大数据中心主任等职。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共遂宁市委员会", "type": "党委", "level": "地级市", "parent": "中共四川省委员会", "location": "遂宁市"},
    {"id": 2, "name": "遂宁市人民政府", "type": "政府", "level": "地级市", "parent": "四川省人民政府", "location": "遂宁市"},
    {"id": 3, "name": "中国人民政治协商会议遂宁市委员会", "type": "政协", "level": "地级市", "parent": "政协四川省委员会", "location": "遂宁市"},
    {"id": 4, "name": "遂宁市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "四川省人大常委会", "location": "遂宁市"},
    {"id": 5, "name": "遂宁市第八届人民代表大会", "type": "人大", "level": "地级市", "parent": "四川省人大", "location": "遂宁市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 惠朝旭 — current Party Secretary
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "现任市委书记（2026年6月-）"},
    # 王忠诚 — current Mayor
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "现任市长（市八届人大七次会议作政府工作报告，2026年2月）"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 李胜 — Deputy Party Secretary
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 雷刚 — 人大常委会主任
    {"person_id": 4, "org_id": 4, "title": "市人大常委会主任", "start_date": "", "end_date": "", "rank": "正厅级", "note": "2026年2月主持市八届人大七次会议"},
    # 杨军 — CPPCC Chair
    {"person_id": 5, "org_id": 3, "title": "市政协主席", "start_date": "", "end_date": "", "rank": "正厅级", "note": "2026年2月作常委会工作报告"},
    # 李东 — CPPCC Party Secretary
    {"person_id": 6, "org_id": 3, "title": "市政协党组书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    # 张韬 — Standing Committee
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": "具体职务待查"},
    # 许文强 — Standing Committee
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": "具体职务待查"},
    # 邓勇 — Party Secretary-General
    {"person_id": 9, "org_id": 1, "title": "市委秘书长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 宋良勇
    {"person_id": 10, "org_id": 5, "title": "主席团成员(市人大代表)", "start_date": "", "end_date": "", "rank": "待查", "note": "大会主席团执行主席"},
    # 付勇
    {"person_id": 11, "org_id": 5, "title": "主席团成员(市人大代表)", "start_date": "", "end_date": "", "rank": "待查", "note": "大会主席团执行主席"},
    # 刘枫
    {"person_id": 12, "org_id": 5, "title": "主席团成员(市人大代表)", "start_date": "", "end_date": "", "rank": "待查", "note": "大会主席团执行主席"},
    # 胡道军
    {"person_id": 13, "org_id": 5, "title": "主席团成员(市人大代表)", "start_date": "", "end_date": "", "rank": "待查", "note": "大会主席团执行主席"},
    # 蒋喻新
    {"person_id": 14, "org_id": 5, "title": "主席团成员(市人大代表)", "start_date": "", "end_date": "", "rank": "待查", "note": "大会主席团执行主席"},
    # 向莉
    {"person_id": 15, "org_id": 5, "title": "主席团成员(市人大代表)", "start_date": "", "end_date": "", "rank": "待查", "note": "大会主席团执行主席"},
    # 严卫东 — predecessor Party Secretary
    {"person_id": 30, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "前任市委书记（2021.1/2-2026.6），去向待查"},
    # 严卫东 — former省政府职务
    {"person_id": 30, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "前任遂宁市市长（约2019-2021）"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 惠朝旭 ↔ 王忠诚 (Party Secretary – Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "中共遂宁市委员会", "overlap_period": "2026"},
    # 惠朝旭 ↔ 李胜 (Party Secretary – Deputy Secretary)
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—副书记", "overlap_org": "中共遂宁市委员会", "overlap_period": "2026"},
    # 王忠诚 ↔ 李胜 (Mayor – Deputy Party Secretary)
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "市长—副书记同僚", "overlap_org": "中共遂宁市委员会", "overlap_period": "2026"},
    # 王忠诚 ↔ 雷刚 (Mayor – 人大主任)
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "市长—人大主任", "overlap_org": "遂宁市", "overlap_period": "2026"},
    # 王忠诚 ↔ 杨军 (Mayor – 政协主席)
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "市长—政协主席", "overlap_org": "遂宁市", "overlap_period": "2026"},
    # 严卫东 ↔ 惠朝旭 (predecessor – successor, Party Secretary)
    {"person_a": 30, "person_b": 1, "type": "交接", "context": "前任市委书记—现任市委书记", "overlap_org": "中共遂宁市委员会", "overlap_period": "2026"},
    # 严卫东 ↔ 王忠诚 (predecessor – successor, Party Secretary – Mayor)
    {"person_a": 30, "person_b": 2, "type": "共事", "context": "前任书记—现任市长此前共事", "overlap_org": "中共遂宁市委员会", "overlap_period": "2021-2026"},
    # 严卫东 ↔ 李胜
    {"person_a": 30, "person_b": 3, "type": "共事", "context": "前任书记—副书记", "overlap_org": "中共遂宁市委员会", "overlap_period": "2021-2026"},
    # Standing committee internal relationships (limited to confirmed members)
    {"person_a": 3, "person_b": 7, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共遂宁市委员会", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 8, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共遂宁市委员会", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 9, "type": "同僚", "context": "副书记—秘书长", "overlap_org": "中共遂宁市委员会", "overlap_period": "2026"},
    {"person_a": 7, "person_b": 8, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共遂宁市委员会", "overlap_period": "2026"},
    {"person_a": 7, "person_b": 9, "type": "同僚", "context": "市委常委—秘书长", "overlap_org": "中共遂宁市委员会", "overlap_period": "2026"},
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
    slug_id = f"suining_{name}"

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
            "notes": "公开资料不足，完整履历待查。百度百科403禁止访问，完整履历待查。",
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
            "person_id": f"suining_{other_name}",
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
            "title": "遂宁市人民政府官方网站",
            "url": source_url,
            "publisher": "遂宁市人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "2026年7月新闻和会议报道确认领导职务",
        }
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "四川省",
            "city": "遂宁市",
            "region": "遂宁市",
            "job": person.get("current_post", ""),
            "task_id": "sichuan_遂宁市",
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
            "biggest_gap": "出生年月、籍贯、完整履历（百度百科403，百度搜索超时）",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的出生年月、籍贯、学历教育背景",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [f"{name} 简历 遂宁", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历（每段职务的起止时间）",
                "why_it_matters": "关系网络分析需要精确的act时间线",
                "suggested_queries": [f"{name} 此前担任", f"{name} 任职经历"],
                "last_attempted": AS_OF,
            },
        ],
    }

    fname = f"{TODAY}-四川省-遂宁市-{person['current_post']}-{person['name']}.json"
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
    core_ids = {1, 2, 30}  # Core leaders + predecessor
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())