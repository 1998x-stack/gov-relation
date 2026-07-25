#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 船营区, 吉林市, 吉林省.

Investigation date: 2026-07-25
Task ID: jilin_船营区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.jlcy.gov.cn — 吉林市船营区人民政府官方网站 (primary, current as of July 2026)
  - jlcy.gov.cn/ldzc/ — 政府领导分工页面 (confirmed current roster as of 2025-08 updates)
  - www.jlcity.gov.cn — 吉林市人民政府官方网站 (city-level news confirming district activity)
  - jlcy.gov.cn/cyzw/ — 船营要闻 (July 2026 news confirming区委活动)

Confidence notes:
  - Government roster (区长、副区长): confirmed via official leadership page (2026-07-25)
  - 张宏国 bio (1975.05,省委党校研究生): confirmed from official profile
  - 李冰 bio (1976.12,市发改委→丰满区): confirmed from official profile
  - Deputy mayors' bios: confirmed from official profiles
  - 区委书记: NOT listed on government portal — this is a critical open gap
  - Party secretary name needs verification from 船营区委网站 or 吉林市委组织部任前公示
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
SLUG = "船营区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_船营区"
if _CURRENT_DIR.name == "jilin_船营区":
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
# IDs: 1=区委书记(unknown), 2=代区长, 3=常务副区长, 4-8=副区长, 9=区委副书记(unknown)

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # CRITICAL GAP: 区委书记
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共吉林市船营区委员会",
        "source": "未公开 — 需从船营区委网站或吉林市委组织部确认",
        "confidence": "unverified",
        "notes": "⚠️ 关键信息缺口！区政府领导页面（jlcy.gov.cn/ldzc/）未列出区委书记信息，需从船营区委官方网站或吉林市委组织部任前公示中确认现任区委书记姓名和履历。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 2,
        "name": "张宏国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年5月",
        "birthplace": "",  # open question
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "区委副书记、副区长、代区长",
        "current_org": "吉林市船营区人民政府",
        "source": "https://www.jlcy.gov.cn/ldzc/202404/t20240417_1201907.html",
        "confidence": "confirmed",
        "notes": "1975年5月生，汉族，中共党员，省委党校研究生学历。曾任舒兰市人民政府副市长，吉林市丰满区委常委、区纪委书记、监委主任，吉林市丰满区委常委、区政府党组副书记、区政府副区长，吉林市船营区委副书记。现任吉林市船营区委副书记，区政府副区长、代区长。领导区政府全面工作，分管区审计局。"
    },
    {
        "id": 3,
        "name": "李冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年12月",
        "birthplace": "",  # open question
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "2004年8月",
        "current_post": "区委常委、常务副区长",
        "current_org": "吉林市船营区人民政府",
        "source": "https://www.jlcy.gov.cn/ldzc/202404/t20240417_1201905.html",
        "confidence": "confirmed",
        "notes": "1976年12月出生，2004年8月参加工作，1997年4月入党，研究生学历。曾任吉林市发展和改革委员会产业协调处副处长、长吉一体化办公室规划处处长、城市建设处（服务业发展处）处长、丰满区副区长。现任吉林市船营区委常委、常务副区长。负责区政府常务工作。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Mayors (from official leadership page)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 4,
        "name": "李晶娜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981年6月",
        "birthplace": "",  # open question
        "education": "省委党校在职研究生学历",
        "party_join": "无党派人士",
        "work_start": "2005年11月",
        "current_post": "副区长",
        "current_org": "吉林市船营区人民政府",
        "source": "https://www.jlcy.gov.cn/ldzc/202404/t20240417_1201904.html",
        "confidence": "confirmed",
        "notes": "1981年6月出生，2005年11月参加工作，无党派人士，省委党校在职研究生学历。曾任蛟河市司法局副局长、蛟河市河北街道办事处主任、蛟河市人大常委会副主任。现任吉林市船营区人民政府副区长。分管区教育局、区民政局、区卫生健康局、区残联。"
    },
    {
        "id": 5,
        "name": "蔡俊锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年3月",
        "birthplace": "",  # open question
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "2005年8月",
        "current_post": "副区长",
        "current_org": "吉林市船营区人民政府",
        "source": "https://www.jlcy.gov.cn/ldzc/202404/t20240424_1203216.html",
        "confidence": "confirmed",
        "notes": "1982年3月出生，2005年8月参加工作，2005年6月入党，研究生学历。曾任磐石市河南街道办事处副主任，磐石市明城镇副镇长、党委副书记、人大副主席，磐石市吉昌镇党委书记、镇长、副书记，舒兰市人民政府副市长。现为船营区副区长。"
    },
    {
        "id": 6,
        "name": "林伟东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年3月",
        "birthplace": "",  # open question
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1995年3月",
        "current_post": "副区长",
        "current_org": "吉林市船营区人民政府",
        "source": "https://www.jlcy.gov.cn/ldzc/202404/t20240417_1201902.html",
        "confidence": "confirmed",
        "notes": "1973年3月出生，1995年3月参加工作，2003年8月入党，大学学历。曾任丰满经济开发区规划建设环保局局长、丰满区征地拆迁工作办公室副主任、主任、丰满区房屋征收经办中心主任、丰满区残疾人联合会理事长、丰满区前二道乡党委书记、乡长、副书记、丰满经济开发区党工委书记、管委会主任（副县局级）。现为船营区副区长。"
    },
    {
        "id": 7,
        "name": "王振宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年11月",
        "birthplace": "",  # open question
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1996年9月",
        "current_post": "副区长、市公安局船营分局局长",
        "current_org": "吉林市船营区人民政府",
        "source": "https://www.jlcy.gov.cn/ldzc/202404/t20240417_1201901.html",
        "confidence": "confirmed",
        "notes": "1971年11月出生，1996年9月参加工作，2000年7月入党，大学学历。曾任吉林市公安局政治部综合处副处长、国内安全保卫支队二处处长、公路交通治安分局政委、公共交通治安管理支队支队长、情报指挥中心主任。现任船营区副区长、市公安局船营分局局长、党委书记。"
    },
    {
        "id": 8,
        "name": "刘喆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989年3月",
        "birthplace": "",  # open question
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "2012年9月",
        "current_post": "副区长",
        "current_org": "吉林市船营区人民政府",
        "source": "https://www.jlcy.gov.cn/ldzc/202404/t20240417_1201903.html",
        "confidence": "confirmed",
        "notes": "1989年3月出生，2012年9月参加工作，2010年11月入党，在职研究生学历。曾任吉林省蛟河市天岗镇副镇长，蛟河市黄松甸镇党委副书记、镇长、书记。现任吉林市船营区人民政府副区长。分管区农业农村局、区林业和畜牧业管理局、区交通局、各乡（镇）人民政府。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共吉林市船营区委员会", "type": "党委", "level": "县处级", "parent": "中共吉林市委员会", "location": "吉林市船营区"},
    {"id": 2, "name": "吉林市船营区人民政府", "type": "政府", "level": "县处级", "parent": "吉林市人民政府", "location": "吉林市船营区"},
    {"id": 3, "name": "吉林市公安局船营分局", "type": "政府", "level": "乡科级", "parent": "吉林市公安局", "location": "吉林市船营区"},
    {"id": 4, "name": "吉林市船营区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "吉林市人大常委会", "location": "吉林市船营区"},
    {"id": 5, "name": "中国人民政治协商会议吉林市船营区委员会", "type": "政协", "level": "县处级", "parent": "吉林市政协", "location": "吉林市船营区"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 区委书记（待确认）
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "⚠️ 待确认——姓名和履历需从区委网站或任前公示确认"},
    # 张宏国 — 代区长
    {"person_id": 2, "org_id": 2, "title": "副区长、代区长", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任船营区委副书记、副区长、代区长，领导区政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "兼任区委副书记"},
    # 李冰 — 常务副区长
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "区委常委、常务副区长"},
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "区委常委"},
    # 李晶娜 — 副区长
    {"person_id": 4, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "负责教育、民政、卫生健康等工作"},
    # 蔡俊锋 — 副区长
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "负责工信、商务、街道办事处等工作"},
    # 林伟东 — 副区长
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "负责住建、城管、房屋征收等工作"},
    # 王振宇 — 副区长、公安局长
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "负责公安、司法、退役军人事务、信访等工作"},
    {"person_id": 7, "org_id": 3, "title": "局长、党委书记", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": "市公安局船营分局局长、党委书记"},
    # 刘喆 — 副区长
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "负责农业农村、林业畜牧、交通等工作"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 区委书记（待确认）↔ 张宏国 (Party Secretary – District Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—区长搭档", "overlap_org": "中共吉林市船营区委员会", "overlap_period": "2025-2026"},
    # 张宏国 ↔ 李冰 (Mayor – Executive Deputy Mayor)
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "区长—常务副区长", "overlap_org": "吉林市船营区人民政府", "overlap_period": "2025-2026"},
    # 张宏国 ↔ 李晶娜
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "区长—副区长", "overlap_org": "吉林市船营区人民政府", "overlap_period": "2025-2026"},
    # 张宏国 ↔ 蔡俊锋
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "区长—副区长", "overlap_org": "吉林市船营区人民政府", "overlap_period": "2025-2026"},
    # 张宏国 ↔ 林伟东
    {"person_a": 2, "person_b": 6, "type": "共事", "context": "区长—副区长", "overlap_org": "吉林市船营区人民政府", "overlap_period": "2025-2026"},
    # 张宏国 ↔ 王振宇
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "区长—副区长、公安局长", "overlap_org": "吉林市船营区人民政府", "overlap_period": "2025-2026"},
    # 张宏国 ↔ 刘喆
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "区长—副区长", "overlap_org": "吉林市船营区人民政府", "overlap_period": "2025-2026"},
    # 李冰 ↔ other deputy mayors (常务副区长—副区长)
    {"person_a": 3, "person_b": 4, "type": "共事", "context": "常务副区长—副区长", "overlap_org": "吉林市船营区人民政府", "overlap_period": "2025-2026"},
    {"person_a": 3, "person_b": 5, "type": "共事", "context": "常务副区长—副区长", "overlap_org": "吉林市船营区人民政府", "overlap_period": "2025-2026"},
    {"person_a": 3, "person_b": 6, "type": "共事", "context": "常务副区长—副区长", "overlap_org": "吉林市船营区人民政府", "overlap_period": "2025-2026"},
    {"person_a": 3, "person_b": 7, "type": "共事", "context": "常务副区长—副区长", "overlap_org": "吉林市船营区人民政府", "overlap_period": "2025-2026"},
    {"person_a": 3, "person_b": 8, "type": "共事", "context": "常务副区长—副区长", "overlap_org": "吉林市船营区人民政府", "overlap_period": "2025-2026"},
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
    slug_id = f"chuanying_{name}"

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
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "unverified",
            "source_ids": ["S001"],
        })

    # Add gap entries for core figures with limited data
    if name == "（待确认）":
        career_timeline = [{
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "区委书记姓名和履历均未知。需从船营区委官方网站或吉林市委组织部任前公示中确认。",
            "confidence": "unverified",
            "source_ids": [],
        }]
    elif pid <= 3 and len(career_timeline) <= 2:
        # Add a gap entry for core leaders with sparse data
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "早期履历",
            "title": "",
            "notes": "公开资料仅列出近期任职经历，早期履历（出生地、教育经历、最初参加工作至此前任职务间）待查。百度百科403禁止访问。",
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
            "person_id": f"chuanying_{other_name}",
            "relationship_type": "overlap",
            "strength": "strong" if r["type"] == "共事" else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "unverified",
            "source_ids": ["S001"],
        })

    # Source register
    source_url = person.get("source", "")
    sources = [
        {
            "id": "S001",
            "title": "吉林市船营区人民政府领导分工页面",
            "url": "https://www.jlcy.gov.cn/ldzc/",
            "publisher": "吉林市船营区人民政府",
            "published_at": "2025-08-20",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "2025年8月更新的区政府领导分工页面，包含每位区领导的简历和分工",
        }
    ]

    # Current post and org (handle the "待确认" case)
    if name == "（待确认）":
        current_post = "区委书记（待确认）"
        current_org = "中共吉林市船营区委员会"
        is_confirmed = False
    else:
        current_post = person.get("current_post", "")
        current_org = person.get("current_org", "")
        is_confirmed = person.get("confidence") == "confirmed"

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "吉林省",
            "city": "吉林市",
            "region": "船营区",
            "job": current_post,
            "task_id": "jilin_船营区",
            "time_focus": "2025-2026年",
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
                "official_profile_url": source_url,
            },
        },
        "current_status": {
            "current_post": current_post,
            "current_org": current_org,
            "administrative_rank": "县处级正职" if pid <= 2 else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": is_confirmed,
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
            "career_completeness": "thin" if not person.get("work_start") else "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "籍贯未确认" if not person.get("birthplace") else "早期履历待补充",
        },
        "open_questions": [
            {
                "priority": "critical" if name == "（待确认）" else "high",
                "question": f"{'现任船营区委书记姓名和完整履历' if name == '（待确认）' else name + '的籍贯、早期履历'}",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [f"船营区 区委书记", "吉林市 船营区 任前公示"] if name == "（待确认）" else [f"{name} 籍贯", f"{name} 简历"],
                "last_attempted": AS_OF,
            },
        ],
    }

    # Determine filename
    if name == "（待确认）":
        fname = f"{TODAY}-吉林省-吉林市-区委书记-待确认.json"
    else:
        fname = f"{TODAY}-吉林省-吉林市-{person['current_post'].split('、')[0]}-{name}.json"
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

    # Write person JSONs for core figures
    print("  Writing person JSONs...")
    core_ids = {1, 2, 3}  # 区委书记(待确认), 代区长, 常务副区长
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
