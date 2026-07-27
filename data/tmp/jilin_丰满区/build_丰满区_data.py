#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 丰满区 (Fengman District), 吉林市, 吉林省.

Investigation date: 2026-07-25
Task ID: jilin_丰满区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - 吉林市人民政府官方网站 (www.jlcity.gov.cn) — 吉林市领导页面确认
  - Web search was severely degraded: Exa rate-limited, Baidu Baike 403 blocked,
    Google Search blocked, www.jlsfmq.gov.cn (丰满区政府网站) unreachable/timeout,
    Jina reader timeout
  - 付彦平 (吉林市副市长) previously served as 丰满区委书记 per city government data

Confidence notes:
  - Current officeholders are identified from available cross-references:
    - Previous data from city-level research shows 付彦平 as 副市长 of 吉林市
    - Based on available cross-references, 丰满区 leadership pattern follows
      standard district-level organization
  - All biographical details (birth, birthplace, education) are unverified due to
    web access limitations - the district government site is unreachable
  - Claims labeled with confidence level; gaps explicitly documented
  - Full career timelines and complete leadership roster will require future
    research when web access is restored
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "../../..").resolve()
# Try alternative repo root layouts
for candidate in [_REPO_ROOT, _STAGING_DIR / "../../../.."]:
    if (candidate / "gov_relation").is_dir():
        _REPO_ROOT = candidate.resolve()
        break
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "丰满区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
STAGING = _STAGING_DIR
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-2 core leaders, 3-6 key deputies, 7-12 standing committee,
#      13-15 government deputy heads, 20-21 predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════════
    # Core Leadership (current) — names from cross-referenced city-level data
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "待查_区委书记",  # placeholder — official name unobtainable due to site blocking
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共吉林市丰满区委员会",
        "source": "丰满区政府网站 (www.jlsfmq.gov.cn) 无法访问",
        "confidence": "unverified",
        "notes": ("丰满区前任区委书记可能为付彦平（现吉林市副市长）。"
                  "现任区委书记姓名待查。丰满区政府网站完全无法访问。"
                  "2026年7月公开报道中未见新任书记明确信息。"
                  "基于吉林市辖区常规模式推定设区委书记一职。")
    },
    {
        "id": 2,
        "name": "待查_区长",  # placeholder — official name unobtainable
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "吉林市丰满区人民政府",
        "source": "丰满区政府网站 (www.jlsfmq.gov.cn) 无法访问",
        "confidence": "unverified",
        "notes": ("丰满区现任区长姓名待查。"
                  "区政府网站无法访问。"
                  "基于吉林市辖区常规模式推定设区长一职。")
    },
    # ══════════════════════════════════════════════════════════════════════════
    # Known Relevant Persons (from city-level data with district overlap)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "付彦平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "吉林市人民政府",
        "source": "https://www.jlcity.gov.cn/jlszf/20zfld/",
        "confidence": "confirmed",
        "notes": ("现任吉林市人民政府副市长。"
                  "此前曾任丰满区委书记。"
                  "2026年7月24日吉林市政府网站领导页面显示为副市长。")
    },
    # ══════════════════════════════════════════════════════════════════════════
    # Deputy leaders / Standing Committee (roles defined but names unknown)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "待查_常务副区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "常务副区长",
        "current_org": "吉林市丰满区人民政府",
        "source": "丰满区政府网站无法访问",
        "confidence": "unverified",
        "notes": "丰满区常务副区长姓名待查。区政府网站无法访问。"
    },
    {
        "id": 4,
        "name": "待查_纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区纪委书记",
        "current_org": "中共吉林市丰满区纪律检查委员会",
        "source": "丰满区政府网站无法访问",
        "confidence": "unverified",
        "notes": "丰满区纪委书记姓名待查。"
    },
    {
        "id": 5,
        "name": "待查_组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委组织部长",
        "current_org": "中共吉林市丰满区委员会组织部",
        "source": "丰满区政府网站无法访问",
        "confidence": "unverified",
        "notes": "丰满区委组织部长姓名待查。"
    },
    {
        "id": 6,
        "name": "待查_宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委宣传部长",
        "current_org": "中共吉林市丰满区委员会宣传部",
        "source": "丰满区政府网站无法访问",
        "confidence": "unverified",
        "notes": "丰满区委宣传部长姓名待查。"
    },
    {
        "id": 7,
        "name": "待查_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委政法委书记",
        "current_org": "中共吉林市丰满区委员会政法委员会",
        "source": "丰满区政府网站无法访问",
        "confidence": "unverified",
        "notes": "丰满区委政法委书记姓名待查。"
    },
    # ══════════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": 20,
        "name": "付彦平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区委书记",
        "current_org": "中共吉林市丰满区委员会",
        "source": "吉林市人民政府网站",
        "confidence": "plausible",
        "notes": "付彦平此前曾任丰满区委书记，后升任吉林市副市长。这是已知的唯一前任信息。"
    },
    {
        "id": 21,
        "name": "待查_前任区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区长",
        "current_org": "吉林市丰满区人民政府",
        "source": "丰满区政府网站无法访问",
        "confidence": "unverified",
        "notes": "丰满区前任区长姓名及去向待查。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共吉林市丰满区委员会", "type": "党委", "level": "县处级", "parent": "中共吉林市委员会", "location": "吉林市丰满区"},
    {"id": 2, "name": "吉林市丰满区人民政府", "type": "政府", "level": "县处级", "parent": "吉林市人民政府", "location": "吉林市丰满区"},
    {"id": 3, "name": "中共吉林市丰满区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共吉林市纪律检查委员会", "location": "吉林市丰满区"},
    {"id": 4, "name": "中共吉林市丰满区委员会组织部", "type": "党委", "level": "县处级", "parent": "中共吉林市丰满区委员会", "location": "吉林市丰满区"},
    {"id": 5, "name": "中共吉林市丰满区委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共吉林市丰满区委员会", "location": "吉林市丰满区"},
    {"id": 6, "name": "中共吉林市丰满区委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共吉林市丰满区委员会", "location": "吉林市丰满区"},
    {"id": 7, "name": "吉林市丰满区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "吉林市人大常委会", "location": "吉林市丰满区"},
    {"id": 8, "name": "中国人民政治协商会议吉林市丰满区委员会", "type": "政协", "level": "县处级", "parent": "政协吉林市委员会", "location": "吉林市丰满区"},
    {"id": 9, "name": "吉林市人民政府", "type": "政府", "level": "地级市", "parent": "吉林省人民政府", "location": "吉林市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # Current leaders (placeholder names - names unknown)
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "现任丰满区委书记，姓名待查"},
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "", "rank": "正处级", "note": "现任丰满区区长，姓名待查"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "区长兼任区委副书记"},
    # Deputy leaders
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "姓名待查"},
    {"person_id": 4, "org_id": 3, "title": "区纪委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "姓名待查"},
    {"person_id": 5, "org_id": 4, "title": "区委组织部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "姓名待查"},
    {"person_id": 6, "org_id": 5, "title": "区委宣传部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "姓名待查"},
    {"person_id": 7, "org_id": 6, "title": "区委政法委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "姓名待查"},
    # 付彦平 — current role at city level
    {"person_id": 10, "org_id": 9, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "现任吉林市人民政府副市长"},
    # Predecessors
    {"person_id": 20, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "前任丰满区委书记，现吉林市副市长"},
    {"person_id": 21, "org_id": 2, "title": "区长", "start_date": "", "end_date": "", "rank": "正处级", "note": "前任丰满区区长，姓名及去向待查"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # Leadership team relationships (structural — based on roles, not named individuals)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—区长搭档（推定）", "overlap_org": "中共吉林市丰满区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—常务副区长（推定）", "overlap_org": "中共吉林市丰满区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—纪委书记（推定）", "overlap_org": "中共吉林市丰满区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—组织部长（推定）", "overlap_org": "中共吉林市丰满区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "书记—宣传部长（推定）", "overlap_org": "中共吉林市丰满区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "书记—政法委书记（推定）", "overlap_org": "中共吉林市丰满区委员会", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "区长—常务副区长（推定）", "overlap_org": "吉林市丰满区人民政府", "overlap_period": "2026"},
    # 付彦平 connections
    {"person_a": 20, "person_b": 1, "type": "交接", "context": "前任区委书记—现任区委书记", "overlap_org": "中共吉林市丰满区委员会", "overlap_period": ""},
    {"person_a": 10, "person_b": 20, "type": "同一人", "context": "付彦平现任吉林市副市长、前任丰满区委书记", "overlap_org": "吉林市人民政府/中共吉林市丰满区委员会", "overlap_period": ""},
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
    if "待查" in person.get("name", ""):
        questions.append("姓名完全未知——丰满区政府网站(www.jlsfmq.gov.cn)无法访问")
    return questions


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"fengman_{name.replace('待查_', 'unknown_')}"

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
            "source_ids": ["S001"] if person.get("source") and "无法" not in person.get("source", "") else [],
        })

    # Add gap entry if career is unknown
    if "待查" in name or not person.get("birth"):
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "丰满区政府网站(www.jlsfmq.gov.cn)完全无法访问；百度百科403禁止访问；搜索引擎超时。姓名和履历均无法获取。",
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
            "person_id": f"fengman_{other_name.replace('待查_', 'unknown_')}",
            "relationship_type": "overlap",
            "strength": "strong" if r["type"] in ("共事", "同一人") else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"] if person.get("source") and "无法" not in person.get("source", "") else [],
        })

    # Source register
    source_url = person.get("source", "")
    sources = []
    if "无法" not in source_url and source_url:
        sources.append({
            "id": "S001",
            "title": "吉林市人民政府官方网站",
            "url": "https://www.jlcity.gov.cn/",
            "publisher": "吉林市人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "2026年7月吉林市政府领导页面。付彦平履历由此确认。",
        })

    is_unknown = "待查" in name

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "吉林省",
            "city": "吉林市",
            "region": "丰满区",
            "job": person.get("current_post", ""),
            "task_id": "jilin_丰满区",
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
            "education": [
                {
                    "period": "",
                    "institution": "",
                    "major": "",
                    "degree": person.get("education", ""),
                    "study_type": "unknown",
                    "source_ids": [],
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
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正处级" if person.get("current_post") in ("区委书记", "区长") else ("副处级" if person.get("current_post") in ("常务副区长", "区纪委书记", "区委组织部长", "区委宣传部长", "区委政法委书记") else ""),
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"] if not is_unknown else [],
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
            "identity": "unverified" if is_unknown else ("confirmed" if person.get("confidence") == "confirmed" else "plausible"),
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "核心领导人姓名、出生年月、籍贯、完整履历——丰满区政府网站完全无法访问",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person.get('current_post', '丰满区领导')}的姓名",
                "why_it_matters": "核心目标人物身份信息，用于关系网络构建",
                "suggested_queries": [f"丰满区 {person.get('current_post', '')}", "吉林市丰满区领导之窗"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{name}的出生年月、籍贯、学历教育背景",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示"],
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

    # For known people (付彦平), add better open questions
    if name == "付彦平":
        record["open_questions"] = [
            {
                "priority": "critical",
                "question": "付彦平担任丰满区委书记的具体起止时间",
                "why_it_matters": "确认丰满区前任书记任期，用于接替关系分析",
                "suggested_queries": ["付彦平 丰满区 区委书记 任职时间"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": "付彦平的出生年月、籍贯、学历教育背景",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": ["付彦平 简历", "付彦平 任前公示"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "付彦平的完整任职履历",
                "why_it_matters": "丰满区—吉林市副市长的晋升路径包括哪些关键节点",
                "suggested_queries": ["付彦平 吉林市 任职", "付彦平 此前担任"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "medium",
                "question": "付彦平与丰满区现任领导班子的关系",
                "why_it_matters": "前任书记提拔后与旧部的联系可能构成关系网络中的重要连线",
                "suggested_queries": ["付彦平 丰满区 报道"],
                "last_attempted": AS_OF,
            },
        ]

    fname = f"{TODAY}-吉林省-吉林市-{person['current_post']}-{name}.json"
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
    # Core leaders + known persons
    core_ids = {1, 2, 10, 20, 21}  # 区委书记, 区长, 付彦平, predecessors
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
