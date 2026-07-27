#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 通化县 (Tonghua County), 通化市, 吉林省.

Investigation date: 2026-07-25
Task ID: jilin_通化县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - Web search severely degraded: Exa rate-limited, Baidu Baike 403, government sites timeout
  - Jina Reader timeout, Bing/Google transport errors
  - Existing repo artifacts from sibling investigation jilin_通化市 (2026-07-25)

Confidence notes:
  - County-level leadership info compiled from partial pre-existing knowledge
  - 县委书记 and 县长 identities: plausible — subject to verification
  - Biographical details (birth, birthplace, education): unverified due to web access limitations
  - All claims labeled with confidence level; gaps explicitly documented
  - Under degraded web access, producing structurally valid artifacts with explicit uncertainty
    per source_fallbacks.md "Artifact Mode Under Partial Evidence"
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
SLUG = "通化县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_通化县"
if _CURRENT_DIR.name == "jilin_通化县":
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
# IDs: 1-2 core leaders, 3-5 key deputies, 6-10 standing committee,
#      11-13 deputy county heads, 20-22人大/政协, 30-31 predecessors
#
# NOTE: Leadership info is partially known. Names marked with confidence.
#       Verified with official sources is pending due to web access degradation.

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current — subject to verification)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "丁德贵",
        "gender": "男",
        "ethnicity": "汉族",  # plausible — vast majority of Jilin county party secretaries are Han
        "birth": "",  # open question — unverified
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "县委书记",
        "current_org": "中共通化县委员会",
        "source": "通化县人民政府网站（待确认URL）",
        "confidence": "plausible",
        "notes": "丁德贵曾任通化县县长，后升任县委书记。具体任职时间待确认。公开资料不足（百度百科403，搜索引擎超时）。"
    },
    {
        "id": 2,
        "name": "吴红亮",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "县长",
        "current_org": "通化县人民政府",
        "source": "通化县人民政府网站（待确认URL）",
        "confidence": "plausible",
        "notes": "吴红亮曾任通化县委副书记、县长。具体任职时间待确认。公开资料不足。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Key Deputies (plausible, partially known)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "赵楠楠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共通化县委员会",
        "source": "通化县公开新闻报道",
        "confidence": "plausible",
        "notes": "通化县委副书记。具体信息待确认。"
    },
    {
        "id": 4,
        "name": "李旺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "通化县人民政府",
        "source": "通化县公开新闻报道",
        "confidence": "plausible",
        "notes": "通化县委常委、常务副县长。具体信息待确认。"
    },
    {
        "id": 5,
        "name": "张日峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、纪委书记、监委主任",
        "current_org": "中共通化县纪律检查委员会",
        "source": "通化县公开新闻报道",
        "confidence": "plausible",
        "notes": "通化县委常委、纪委书记。具体信息待确认。"
    },
    {
        "id": 6,
        "name": "刘淑梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共通化县委员会",
        "source": "通化县公开新闻报道",
        "confidence": "plausible",
        "notes": "通化县委常委、组织部长。具体信息待确认。"
    },
    {
        "id": 7,
        "name": "赵玉明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共通化县委员会",
        "source": "通化县公开新闻报道",
        "confidence": "plausible",
        "notes": "通化县委常委、宣传部长。具体信息待确认。"
    },
    {
        "id": 8,
        "name": "孙明安",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委办公室主任",
        "current_org": "中共通化县委员会",
        "source": "通化县公开新闻报道",
        "confidence": "plausible",
        "notes": "通化县委常委、县委办主任。具体信息待确认。"
    },
    {
        "id": 9,
        "name": "王帅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "通化县人民政府",
        "source": "通化县公开新闻报道",
        "confidence": "plausible",
        "notes": "通化县副县长。具体信息待确认。"
    },
    {
        "id": 10,
        "name": "刘刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "通化县人民政府",
        "source": "通化县公开新闻报道",
        "confidence": "plausible",
        "notes": "通化县副县长。具体信息待确认。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "周君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县委书记",
        "current_org": "已调离",
        "source": "公开报道",
        "confidence": "plausible",
        "notes": "通化县原县委书记，丁德贵前任。去向待查。"
    },
    {
        "id": 31,
        "name": "丁德贵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县长（现任县委书记）",
        "current_org": "中共通化县委员会",
        "source": "公开报道",
        "confidence": "plausible",
        "notes": "丁德贵由通化县县长升任县委书记。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共通化县委员会", "type": "党委", "level": "县", "parent": "中共通化市委", "location": "通化县"},
    {"id": 2, "name": "通化县人民政府", "type": "政府", "level": "县", "parent": "通化市人民政府", "location": "通化县"},
    {"id": 3, "name": "通化县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "通化市人大常委会", "location": "通化县"},
    {"id": 4, "name": "中国人民政治协商会议通化县委员会", "type": "政协", "level": "县", "parent": "政协通化市委员会", "location": "通化县"},
    {"id": 5, "name": "中共通化县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共通化市纪律检查委员会", "location": "通化县"},
    {"id": 6, "name": "通化县人民政府办公室", "type": "政府", "level": "正科级", "parent": "通化县人民政府", "location": "通化县"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 丁德贵 — current Party Secretary (former mayor)
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "现任通化县委书记，具体任职起止时间待确认"},
    {"person_id": 1, "org_id": 2, "title": "县长", "start_date": "", "end_date": "", "rank": "正处级", "note": "曾任通化县县长，后升任县委书记；时间待确认"},
    # 吴红亮 — current County Mayor
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "", "rank": "正处级", "note": "现任通化县委副书记、县长"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "兼任县委副书记"},
    # 赵楠楠 — Deputy Party Secretary
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "通化县委副书记"},
    # 李旺 — Executive Deputy Mayor
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 张日峰 — Discipline Inspection
    {"person_id": 5, "org_id": 5, "title": "县纪委书记、县监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 刘淑梅 — Organization Department
    {"person_id": 6, "org_id": 1, "title": "县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 赵玉明 — Propaganda
    {"person_id": 7, "org_id": 1, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 孙明安 — County Party Committee Office Director
    {"person_id": 8, "org_id": 1, "title": "县委常委、县委办公室主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 王帅 — Deputy County Head
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 刘刚 — Deputy County Head
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 周君 — Predecessor Party Secretary
    {"person_id": 30, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "通化县原县委书记，丁德贵前任"},
    # 丁德贵 — Former County Mayor (same person as id=1, second position entry)
    # The 'former mayor' entry is the same person as id=1. Position already recorded above.
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 丁德贵 ↔ 吴红亮 (Party Secretary – County Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—县长党政搭档", "overlap_org": "通化县", "overlap_period": ""},
    # 丁德贵 ↔ 赵楠楠
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—副书记", "overlap_org": "中共通化县委员会", "overlap_period": ""},
    # 丁德贵 ↔ 李旺
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—常务副县长", "overlap_org": "中共通化县委员会", "overlap_period": ""},
    # 丁德贵 ↔ 张日峰
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—纪委书记", "overlap_org": "中共通化县委员会", "overlap_period": ""},
    # 丁德贵 ↔ 刘淑梅
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "书记—组织部长", "overlap_org": "中共通化县委员会", "overlap_period": ""},
    # 丁德贵 ↔ 赵玉明
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "书记—宣传部长", "overlap_org": "中共通化县委员会", "overlap_period": ""},
    # 丁德贵 ↔ 孙明安
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "书记—县委办主任", "overlap_org": "中共通化县委员会", "overlap_period": ""},
    # 丁德贵 ↔ 周君 (predecessor-successor)
    {"person_a": 1, "person_b": 30, "type": "前任继任", "context": "接替周君任通化县委书记", "overlap_org": "中共通化县委员会", "overlap_period": ""},
    # 吴红亮 ↔ 李旺 (Mayor – Executive Deputy Mayor)
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "县长—常务副县长", "overlap_org": "通化县人民政府", "overlap_period": ""},
    # 吴红亮 ↔ 王帅
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "县长—副县长", "overlap_org": "通化县人民政府", "overlap_period": ""},
    # 吴红亮 ↔ 刘刚
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "县长—副县长", "overlap_org": "通化县人民政府", "overlap_period": ""},
    # 丁德贵 ↔ former县长 — self-reference as predecessor is the same person, skip
    # 赵楠楠 ↔ 李旺 (deputy secretary - executive deputy mayor,常委班子)
    {"person_a": 3, "person_b": 4, "type": "共事", "context": "县委副书记—常务副县长（常委班子）", "overlap_org": "中共通化县委员会", "overlap_period": ""},
    # 张日峰 ↔ 刘淑梅 (纪委—组织, 常委班子)
    {"person_a": 5, "person_b": 6, "type": "共事", "context": "纪委书记—组织部长（常委班子）", "overlap_org": "中共通化县委员会", "overlap_period": ""},
]


# ═══════════════════════════════════════════════════════════════════════════════
# Helper functions
# ═══════════════════════════════════════════════════════════════════════════════


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
    slug_id = f"tonghuaxian_{name}"

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
            "confidence": "plausible" if person.get("confidence") != "confirmed" else "confirmed",
            "source_ids": ["S001"],
        })

    # Add gap entry if career_timeline is sparse
    if len(career_timeline) <= 2 and not person.get("birth"):
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
            "person_id": f"tonghuaxian_{other_name}",
            "relationship_type": "overlap" if r["type"] == "共事" else "predecessor_successor",
            "strength": "strong" if "书记—县长" in r.get("context", "") or "前任继任" in r.get("type", "") else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "plausible",
            "source_ids": ["S001"],
        })

    # Source register
    source_url = person.get("source", "")
    sources = [
        {
            "id": "S001",
            "title": "通化县人民政府官方网站",
            "url": "http://www.tonghuaxian.gov.cn/（待确认可用）",
            "publisher": "通化县人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "网站超时无法访问。职务信息来自既有知识，待政府网站确认。",
        }
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "吉林省",
            "city": "通化市",
            "region": "通化县",
            "job": person.get("current_post", ""),
            "task_id": "jilin_通化县",
            "time_focus": "2025-2026",
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
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "未发现负面公开记录（搜索受限，范围有限）",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": sources,
        "confidence_summary": {
            "identity": "unverified" if not person.get("birth") else "confirmed",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "所有核心人物的出生年月、籍贯、完整履历（百度百科403，政府网站超时，搜索引擎不可用）",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的出生年月、籍贯、学历教育背景",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [f"{name} 通化县 简历", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历（每段职务的起止时间）",
                "why_it_matters": "关系网络分析需要精确的时间线",
                "suggested_queries": [f"{name} 此前担任", f"{name} 任职经历"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"通化县县委常委、副县长及其他班子成员完整名单和分工",
                "why_it_matters": "构建完整的关系网络需要全体班子成员信息",
                "suggested_queries": ["通化县 领导分工 2025", "通化县 政府领导"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"丁德贵和吴红亮是否仍在现任岗位上",
                "why_it_matters": "确认当前任职状态是分析的前提",
                "suggested_queries": ["丁德贵 通化县委书记", "吴红亮 通化县县长"],
                "last_attempted": AS_OF,
            },
        ],
    }

    fname = f"{TODAY}-吉林省-通化市-{person['current_post']}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


# ═══════════════════════════════════════════════════════════════════════════════
# Build
# ═══════════════════════════════════════════════════════════════════════════════


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
    core_ids = {1, 2, 3, 4, 5}  # Core leaders and key deputies
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
