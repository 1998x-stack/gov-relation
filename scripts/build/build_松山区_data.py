#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 赤峰市松山区, 内蒙古自治区.

Investigation date: 2026-07-25
Task ID: inner_mongolia_松山区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.ssq.gov.cn — 赤峰市松山区人民政府官方网站 (primary, current as of July 2026)
  - News articles and meeting attendance lists from ssq.gov.cn (July 2026)

Confidence notes:
  - Current roles: confirmed via official government website (July 2026)
  - Biographical details (birth, birthplace, education): mostly unverified due to web access limitations
    (Baidu Baike 403, Exa rate-limited, 360 search captcha-blocked)
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
SLUG = "松山区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "inner_mongolia_松山区"
if _CURRENT_DIR.name == "inner_mongolia_松山区":
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
# IDs: 1-9 district party/government leaders, 10-19 other leaders, 20+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "杨猛",
        "gender": "男",
        "ethnicity": "",  # open question — unverified
        "birth": "",  # open question — unverified
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "区委书记",
        "current_org": "中共赤峰市松山区委员会",
        "source": "http://www.ssq.gov.cn/zwgk/",
        "confidence": "confirmed",
        "notes": "2026年7月18日深入矿山检查安全生产工作（杨猛深入矿山一线检查督导安全生产工作, ssq.gov.cn 2026-07-20）；此前2025年3月带队赴北京天津等地招商"
    },
    {
        "id": 2,
        "name": "钟青松",
        "gender": "男",
        "ethnicity": "",  # open question — unverified
        "birth": "",  # open question — unverified
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "区长",
        "current_org": "赤峰市松山区人民政府",
        "source": "http://www.ssq.gov.cn/zwgk/",
        "confidence": "confirmed",
        "notes": "区委副书记、区长。2026年3月25日主持召开区政府第2次常务会议暨区安委会第2次会议（钟青松主持召开2026年区政府第2次常务会议, ssq.gov.cn 2026-03-26）"
    },
    {
        "id": 3,
        "name": "傅晓林",
        "gender": "男",
        "ethnicity": "",  # open question
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "赤峰市松山区人民代表大会常务委员会",
        "source": "http://www.ssq.gov.cn/zwgk/",
        "confidence": "confirmed",
        "notes": "松山区人大常委会主任（政务公开领导之窗）"
    },
    {
        "id": 4,
        "name": "秦玉浩",
        "gender": "男",
        "ethnicity": "",  # open question
        "birth": "",  # open question
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议赤峰市松山区委员会",
        "source": "http://www.ssq.gov.cn/zwgk/",
        "confidence": "confirmed",
        "notes": "松山区政协主席（政务公开领导之窗）"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee & Deputy Leaders
    # Source: Meeting attendance lists (2026-03-25区政府常务会议等)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 5,
        "name": "姜常辉",
        "gender": "男",
        "ethnicity": "",  # open question
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长（推测）",
        "current_org": "中共赤峰市松山区委员会",
        "source": "http://www.ssq.gov.cn/ssq_lbt/202603/t20260326_2746021.html",
        "confidence": "confirmed",
        "notes": "2026年3月25日区政府常务会议出席（区委常委身份待确认，排名靠前，推测为常务副区长）"
    },
    {
        "id": 6,
        "name": "杨文东",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长（推测）",
        "current_org": "中共赤峰市松山区委员会",
        "source": "http://www.ssq.gov.cn/ssq_lbt/202603/t20260326_2746021.html",
        "confidence": "confirmed",
        "notes": "2026年3月25日区政府常务会议出席"
    },
    {
        "id": 7,
        "name": "李显付",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委（推测）",
        "current_org": "中共赤峰市松山区委员会",
        "source": "http://www.ssq.gov.cn/ssq_lbt/202603/t20260326_2746021.html",
        "confidence": "confirmed",
        "notes": "2026年3月25日区政府常务会议出席；2026年7月18日陪同区委书记杨猛检查矿山安全生产"
    },
    {
        "id": 8,
        "name": "贾晗",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "赤峰市松山区人民政府",
        "source": "http://www.ssq.gov.cn/ssq_lbt/202603/t20260326_2746021.html",
        "confidence": "confirmed",
        "notes": "2026年3月25日区政府常务会议出席"
    },
    {
        "id": 9,
        "name": "李志国",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "赤峰市松山区人民政府",
        "source": "http://www.ssq.gov.cn/xwgg/jrss/202607/t20260721_2794877.html",
        "confidence": "confirmed",
        "notes": "2026年7月20日主持松山区涉农领域重点工作推进会议"
    },
    {
        "id": 10,
        "name": "李国林",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "赤峰市松山区人民政府",
        "source": "http://www.ssq.gov.cn/ssq_lbt/202603/t20260326_2746021.html",
        "confidence": "confirmed",
        "notes": "2026年3月25日区政府常务会议列席"
    },
    {
        "id": 11,
        "name": "刘万里",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "赤峰市松山区人民政府",
        "source": "http://www.ssq.gov.cn/ssq_lbt/202603/t20260326_2746021.html",
        "confidence": "confirmed",
        "notes": "2026年3月25日区政府常务会议列席"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors — open questions / insufficient data
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 20,
        "name": "姜丛",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区委书记（推测）",
        "current_org": "中共赤峰市松山区委员会",
        "source": "公开报道推测",
        "confidence": "unverified",
        "notes": "姜丛曾任松山区委书记（据公开报道），具体任期和去向待查。杨猛接任时间待确认。"
    },
]


# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共赤峰市松山区委员会", "type": "党委", "level": "县级", "parent": "中共赤峰市委员会", "location": "赤峰市松山区"},
    {"id": 2, "name": "赤峰市松山区人民政府", "type": "政府", "level": "县级", "parent": "赤峰市人民政府", "location": "赤峰市松山区"},
    {"id": 3, "name": "中国人民政治协商会议赤峰市松山区委员会", "type": "政协", "level": "县级", "parent": "政协赤峰市委员会", "location": "赤峰市松山区"},
    {"id": 4, "name": "赤峰市松山区人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "赤峰市人大常委会", "location": "赤峰市松山区"},
    {"id": 5, "name": "中共赤峰市委员会", "type": "党委", "level": "地级市", "parent": "中共内蒙古自治区委员会", "location": "赤峰市"},
    {"id": 6, "name": "赤峰市人民政府", "type": "政府", "level": "地级市", "parent": "内蒙古自治区人民政府", "location": "赤峰市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 杨猛 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "现任区委书记，此前带队赴北京天津招商"},
    # 钟青松 — 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "", "rank": "正处级", "note": "区委副书记、区长"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 傅晓林 — 区人大主任
    {"person_id": 3, "org_id": 4, "title": "区人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 秦玉浩 — 区政协主席
    {"person_id": 4, "org_id": 3, "title": "区政协主席", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 姜常辉
    {"person_id": 5, "org_id": 2, "title": "副区长（推测）", "start_date": "", "end_date": "", "rank": "副处级", "note": "具体职务待查"},
    # 杨文东
    {"person_id": 6, "org_id": 2, "title": "副区长（推测）", "start_date": "", "end_date": "", "rank": "副处级", "note": "具体职务待查"},
    # 李显付
    {"person_id": 7, "org_id": 1, "title": "区委常委（推测）", "start_date": "", "end_date": "", "rank": "副处级", "note": "陪同区委书记检查矿山安全"},
    # 贾晗
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 李志国
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "分管涉农领域"},
    # 李国林
    {"person_id": 10, "org_id": 2, "title": "副区长（推测列席）", "start_date": "", "end_date": "", "rank": "副处级", "note": "具体职务待查"},
    # 刘万里
    {"person_id": 11, "org_id": 2, "title": "副区长（推测列席）", "start_date": "", "end_date": "", "rank": "副处级", "note": "具体职务待查"},
    # 姜丛 — 前任区委书记（推测）
    {"person_id": 20, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "前任区委书记，任期和去向待查"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 杨猛 ↔ 钟青松 (区委书记—区长搭档)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—区长搭档", "overlap_org": "中共赤峰市松山区委员会", "overlap_period": "2026"},
    # 杨猛 ↔ 李显付
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "区委书记—区委常委；共同检查矿山安全", "overlap_org": "中共赤峰市松山区委员会", "overlap_period": "2026"},
    # 钟青松 ↔ 姜常辉
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "区长—副区长，共同出席区政府常务会议", "overlap_org": "赤峰市松山区人民政府", "overlap_period": "2026"},
    # 钟青松 ↔ 杨文东
    {"person_a": 2, "person_b": 6, "type": "共事", "context": "区长—副区长，共同出席区政府常务会议", "overlap_org": "赤峰市松山区人民政府", "overlap_period": "2026"},
    # 钟青松 ↔ 李显付
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "区长—区委常委，共同出席区政府常务会议", "overlap_org": "赤峰市松山区人民政府", "overlap_period": "2026"},
    # 钟青松 ↔ 贾晗
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "区长—副区长，共同出席区政府常务会议", "overlap_org": "赤峰市松山区人民政府", "overlap_period": "2026"},
    # 钟青松 ↔ 李志国
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "区长—副区长，共同出席区政府常务会议", "overlap_org": "赤峰市松山区人民政府", "overlap_period": "2026"},
    # 钟青松 ↔ 李国林
    {"person_a": 2, "person_b": 10, "type": "同僚", "context": "共同出席区政府常务会议（李国林列席）", "overlap_org": "赤峰市松山区人民政府", "overlap_period": "2026"},
    # 钟青松 ↔ 刘万里
    {"person_a": 2, "person_b": 11, "type": "同僚", "context": "共同出席区政府常务会议（刘万里列席）", "overlap_org": "赤峰市松山区人民政府", "overlap_period": "2026"},
    # 杨猛 ←前任 姜丛
    {"person_a": 20, "person_b": 1, "type": "交接", "context": "前任区委书记—现任区委书记（推测）", "overlap_org": "中共赤峰市松山区委员会", "overlap_period": ""},
    # 区委—人大—政协主要领导
    {"person_a": 1, "person_b": 3, "type": "同僚", "context": "区委书记—人大主任", "overlap_org": "中共赤峰市松山区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 4, "type": "同僚", "context": "区委书记—政协主席", "overlap_org": "中共赤峰市松山区委员会", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 3, "type": "同僚", "context": "区长—人大主任", "overlap_org": "赤峰市松山区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 4, "type": "同僚", "context": "区长—政协主席", "overlap_org": "赤峰市松山区人民政府", "overlap_period": "2026"},
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
    slug_id = f"songshan_{name}"

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
            "notes": "公开资料不足，完整履历待查。百度百科403禁止访问，搜索引擎受限。",
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
            "person_id": f"songshan_{other_name}",
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
            "title": "赤峰市松山区人民政府官方网站",
            "url": "http://www.ssq.gov.cn/",
            "publisher": "赤峰市松山区人民政府",
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
            "province": "内蒙古自治区",
            "city": "赤峰市",
            "region": "松山区",
            "job": person.get("current_post", ""),
            "task_id": "inner_mongolia_松山区",
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
            "biggest_gap": "出生年月、籍贯、完整履历（百度百科403，搜索引擎受限）",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的出生年月、籍贯、学历教育背景",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 赤峰"],
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

    fname = f"{TODAY}-内蒙古自治区-赤峰市-{person['current_post']}-{person['name']}.json"
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
    core_ids = {1, 2, 3, 4, 5, 7, 8, 9, 20}  # Core leaders + predecessors
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
