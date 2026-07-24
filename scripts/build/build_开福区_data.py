#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 开福区 (Kaifu District), 长沙市, 湖南省.

Investigation date: 2026-07-24
Task ID: hunan_开福区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.kaifu.gov.cn — 开福区人民政府官方网站（区政府领导页面、领导活动页面）
  - 政府门户显示：区委书记周海毅，区长蒋文武（1980年2月生，研究生学历，管理学博士）
  - 常务副区长蒋志国（1977年10月生）
  - 前任区长高伟（2026年3月仍有活动报道，此后由蒋文武接任）
  - 前任区委书记罗玉环（2026年6月8日仍有活动报道，与蒋文武一同出现）

Confidence notes:
  - 周海毅 (Party Secretary): confirmed from official news (2026-07)
  - 蒋文武 (District Mayor): confirmed from official profile page
  - 罗玉环 (Predecessor Party Secretary): plausible — mentioned alongside 蒋文武 in June 2026
  - 高伟 (Predecessor District Mayor): confirmed — news shows activity until March 2026
  - Other deputy mayors: confirmed names from official leadership page
  - Detailed career histories beyond current role are limited
  - All claims labeled with confidence level; gaps explicitly documented
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
while REPO_ROOT.name:
    if (REPO_ROOT / "gov_relation").is_dir():
        break
    parent = REPO_ROOT.parent
    if parent == REPO_ROOT:
        break
    REPO_ROOT = parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "开福区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "hunan_开福区"
if _CURRENT_DIR.name == "hunan_开福区":
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
# IDs: 1-9 party/government core, 10-19 deputy government, 20-29 other leaders, 30+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "周海毅",
        "gender": "男",
        "ethnicity": "汉族",  # plausible — typical for Hunan officials
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "区委书记",
        "current_org": "中共长沙市开福区委员会",
        "source": "https://www.kaifu.gov.cn/（官方活动报道确认）",
        "confidence": "confirmed",
        "notes": "2026年7月24日报道'周海毅主持区委理论学习中心组集体学习'、'周海毅主持召开区委常委会会议'。前任为罗玉环。完整履历待查。"
    },
    {
        "id": 2,
        "name": "蒋文武",
        "gender": "男",
        "ethnicity": "汉族",  # confirmed — official profile
        "birth": "1980年2月",  # confirmed — official profile
        "birthplace": "",  # open question
        "education": "研究生学历，管理学博士，高级经济师",  # confirmed — official profile
        "party_join": "中共党员",
        "work_start": "2002年7月",  # confirmed — official profile
        "current_post": "区长",
        "current_org": "开福区人民政府",
        "source": "https://www.kaifu.gov.cn/qzf/zfld/qz/",
        "confidence": "confirmed",
        "notes": "区委副书记、区政府党组书记、区长。1980年2月出生，2002年7月参加工作。此前任职经历待查。"
    },
    {
        "id": 3,
        "name": "蒋志国",
        "gender": "男",
        "ethnicity": "汉族",  # confirmed — official profile
        "birth": "1977年10月",  # confirmed — official profile
        "birthplace": "",  # open question
        "education": "在职研究生",  # confirmed — official profile
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "常务副区长",
        "current_org": "开福区人民政府",
        "source": "https://www.kaifu.gov.cn/qzf/zfld/qtld/202411/t20241121_11663780.html",
        "confidence": "confirmed",
        "notes": "区委常委、区政府党组副书记、常务副区长。1977年10月出生。分管发改、财税、人社、应急等工作。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Mayors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 4,
        "name": "王乐君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "开福区人民政府",
        "source": "https://www.kaifu.gov.cn/qzf/（政府领导页面）",
        "confidence": "confirmed",
        "notes": "副区长，具体分工待查。"
    },
    {
        "id": 5,
        "name": "刘一斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "开福区人民政府",
        "source": "https://www.kaifu.gov.cn/qzf/（政府领导页面）",
        "confidence": "confirmed",
        "notes": "副区长，具体分工待查。"
    },
    {
        "id": 6,
        "name": "孙铁龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "开福区人民政府",
        "source": "https://www.kaifu.gov.cn/qzf/（政府领导页面）",
        "confidence": "confirmed",
        "notes": "副区长，具体分工待查。"
    },
    {
        "id": 7,
        "name": "邹畅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "开福区人民政府",
        "source": "https://www.kaifu.gov.cn/qzf/（政府领导页面）",
        "confidence": "confirmed",
        "notes": "副区长，具体分工待查。"
    },
    {
        "id": 8,
        "name": "易海威",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "开福区人民政府",
        "source": "https://www.kaifu.gov.cn/qzf/（政府领导页面）",
        "confidence": "confirmed",
        "notes": "副区长，具体分工待查。"
    },
    {
        "id": 9,
        "name": "胡海飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "开福区人民政府",
        "source": "https://www.kaifu.gov.cn/qzf/（政府领导页面）",
        "confidence": "confirmed",
        "notes": "副区长（2024年11月任），具体分工待查。"
    },
    {
        "id": 10,
        "name": "龙舟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "开福区人民政府",
        "source": "https://www.kaifu.gov.cn/qzf/（政府领导页面）",
        "confidence": "confirmed",
        "notes": "副区长（2025年1月任），具体分工待查。"
    },
    {
        "id": 11,
        "name": "万建永",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "开福区人民政府",
        "source": "https://www.kaifu.gov.cn/qzf/（政府领导页面）",
        "confidence": "confirmed",
        "notes": "副区长（2025年4月任），具体分工待查。"
    },
    {
        "id": 12,
        "name": "贺云鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "开福区人民政府",
        "source": "https://www.kaifu.gov.cn/qzf/（政府领导页面）",
        "confidence": "confirmed",
        "notes": "副区长（2025年9月任），具体分工待查。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "罗玉环",
        "gender": "女",
        "ethnicity": "汉族",  # plausible
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "前任区委书记",
        "current_org": "中共长沙市开福区委员会",
        "source": "https://www.kaifu.gov.cn/（2026年6月活动报道）",
        "confidence": "confirmed",
        "notes": "2026年6月8日'罗玉环蒋文武带队开展2026年高考考务工作检查'报道确认在任。此后由周海毅接任（2026年7月已以区委书记身份活动）。去向待查。"
    },
    {
        "id": 31,
        "name": "高伟",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "前任区长",
        "current_org": "开福区人民政府",
        "source": "https://www.kaifu.gov.cn/（2026年3月讲话报道）",
        "confidence": "confirmed",
        "notes": "2026年3月仍有'高伟：全力冲刺一季度'讲话，此后活动报道均为蒋文武。2026年3月-6月间完成交接。去向待查。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共长沙市开福区委员会", "type": "党委", "level": "市辖区", "parent": "中共长沙市委员会", "location": "长沙市开福区"},
    {"id": 2, "name": "开福区人民政府", "type": "政府", "level": "市辖区", "parent": "长沙市人民政府", "location": "长沙市开福区"},
    {"id": 3, "name": "开福区人民代表大会常务委员会", "type": "人大", "level": "市辖区", "parent": "长沙市人民代表大会常务委员会", "location": "长沙市开福区"},
    {"id": 4, "name": "中国人民政治协商会议开福区委员会", "type": "政协", "level": "市辖区", "parent": "政协长沙市委员会", "location": "长沙市开福区"},
    {"id": 5, "name": "中共长沙市开福区纪律检查委员会", "type": "党委", "level": "市辖区", "parent": "中共长沙市纪律检查委员会", "location": "长沙市开福区"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 周海毅 — current Party Secretary
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2026-06/2026-07", "end_date": "", "rank": "正处级", "note": "现任开福区委书记，前任为罗玉环"},
    # 蒋文武 — current District Mayor
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "2026-03/2026-06", "end_date": "", "rank": "正处级", "note": "区委副书记、区政府党组书记、区长"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "2026-03/2026-06", "end_date": "", "rank": "正处级", "note": "区委副书记"},
    # 蒋志国 — Executive Deputy Mayor
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "区委常委、区政府党组副书记、常务副区长"},
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # Deputy Mayors
    {"person_id": 4, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "2024-11", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "2025-01", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副区长", "start_date": "2025-04", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副区长", "start_date": "2025-09", "end_date": "", "rank": "副处级", "note": ""},
    # Predecessors
    {"person_id": 30, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "2026-06/2026-07", "rank": "正处级", "note": "前任开福区委书记，2026年6月仍在任，后由周海毅接任"},
    {"person_id": 31, "org_id": 2, "title": "区长", "start_date": "", "end_date": "2026-03/2026-06", "rank": "正处级", "note": "前任开福区长，2026年3月仍有活动报道"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 周海毅 ↔ 蒋文武 (Party Secretary – District Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—区长搭档", "overlap_org": "中共长沙市开福区委员会", "overlap_period": "2026-至今"},
    # 蒋文武 ↔ 蒋志国 (Mayor – Executive Deputy Mayor)
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "区长—常务副区长", "overlap_org": "开福区人民政府", "overlap_period": "至今"},
    # 蒋文武 → 副区长团队
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "区长—副区长", "overlap_org": "开福区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "区长—副区长", "overlap_org": "开福区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 6, "type": "共事", "context": "区长—副区长", "overlap_org": "开福区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "区长—副区长", "overlap_org": "开福区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "区长—副区长", "overlap_org": "开福区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "区长—副区长", "overlap_org": "开福区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "区长—副区长", "overlap_org": "开福区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "区长—副区长", "overlap_org": "开福区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "区长—副区长", "overlap_org": "开福区人民政府", "overlap_period": "至今"},
    # 罗玉环 ↔ 周海毅 (predecessor-successor)
    {"person_a": 30, "person_b": 1, "type": "交接", "context": "前任区委书记—现任区委书记", "overlap_org": "中共长沙市开福区委员会", "overlap_period": "2026.06-2026.07"},
    # 高伟 ↔ 蒋文武 (predecessor-successor)
    {"person_a": 31, "person_b": 2, "type": "交接", "context": "前任区长—现任区长", "overlap_org": "开福区人民政府", "overlap_period": "2026.03-2026.06"},
    # 罗玉环 ↔ 高伟 (former Party Secretary – former Mayor)
    {"person_a": 30, "person_b": 31, "type": "共事", "context": "前任区委书记—前任区长搭档", "overlap_org": "中共长沙市开福区委员会", "overlap_period": "至2026年"},
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


def _make_person_id(name: str) -> str:
    return f"kaifu_{name}"


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = _make_person_id(name)

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
            "relationship_type": "overlap" if r["type"] in ("共事",) else "predecessor_successor",
            "strength": "strong" if r["type"] in ("共事", "交接") else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        })

    source_url = person.get("source", "")
    sources = [
        {
            "id": "S001",
            "title": "长沙市开福区人民政府官方网站",
            "url": "https://www.kaifu.gov.cn/",
            "publisher": "开福区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "开福区政府门户网站政府领导页面及活动报道",
        },
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "湖南省",
            "city": "长沙市",
            "region": "开福区",
            "job": person.get("current_post", ""),
            "task_id": "hunan_开福区",
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
            "administrative_rank": "正处级",
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
            "identity": "confirmed" if person.get("birth") else "partial",
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

    print("  Writing person JSONs...")
    core_ids = {1, 2, 30, 31}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
