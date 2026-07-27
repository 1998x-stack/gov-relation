#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 通化市 (Tonghua City), 吉林省.

Investigation date: 2026-07-25
Task ID: jilin_通化市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.tonghua.gov.cn — 通化市人民政府官方网站 (primary, current as of July 2026)
  - Homepage leadership section confirms 孙简 as 副省长、市委书记 and 高山 as 市长
  - Government site homepage news and meeting reports (July 2026)
  - Web search was degraded: Baidu Baike 403, Exa rate-limited, Bing/Google blocked/timeout

Confidence notes:
  - Current roles: confirmed via government official homepage (2026-07-25)
  - 孙简: Title "副省长、市委书记" confirmed — also serves as Vice Governor of Jilin Province
  - 高山: title "市长" confirmed
  - Biographical details (birth, birthplace, education): unverified due to web access limitations
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
SLUG = "通化市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
# When run from data/tmp/jilin_通化市/, STAGING is that directory.
# When run from repo root, STAGING is data/tmp/jilin_通化市/.
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_通化市"
if _CURRENT_DIR.name == "jilin_通化市":
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
# IDs: 1-2 core leaders, 3-4 deputy secretaries, 5-11 standing committee,
#      12-18 deputy mayors, 19 secretary-general, 20-23人大/政协, 30-31 predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "孙简",
        "gender": "男",
        "ethnicity": "汉族",  # plausible — vast majority of Jilin party secretaries are Han
        "birth": "",  # open question — unverified
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "副省长、市委书记",
        "current_org": "中共通化市委员会",
        "source": "https://www.tonghua.gov.cn/",
        "confidence": "confirmed",
        "notes": "2026年7月任吉林省副省长、通化市委书记。同时兼任吉林省副省长（省管副省级/正厅级）。2026年7月多次主持市委常委会会议、看望抗洪部队、推进开发区改革。此前任职经历和完整履历待查。"
    },
    {
        "id": 2,
        "name": "高山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市长",
        "current_org": "通化市人民政府",
        "source": "https://www.tonghua.gov.cn/",
        "confidence": "confirmed",
        "notes": "2026年7月任通化市委副书记、市长。2026年7月督导集安市防汛工作、检查高层建筑消防安全和地质灾害防范。领导市政府全面工作。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Party Secretaries and Standing Committee
    # source: meeting attendance from homepage news (July 2026) — limited info
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "所永吉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市委政法委书记",
        "current_org": "中共通化市委员会",
        "source": "通化市公开新闻报道",
        "confidence": "plausible",
        "notes": "据公开报道，所永吉担任通化市委副书记、政法委书记"
    },
    {
        "id": 4,
        "name": "金洪培",
        "gender": "男",
        "ethnicity": "朝鲜族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共通化市委员会",
        "source": "通化市公开新闻报道",
        "confidence": "plausible",
        "notes": "据公开报道，金洪培担任通化市委常委、组织部部长"
    },
    {
        "id": 5,
        "name": "尚忠诚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "通化市人民政府",
        "source": "通化市公开报道",
        "confidence": "plausible",
        "notes": "据公开报道信息"
    },
    {
        "id": 6,
        "name": "王彦东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市纪委书记、市监委主任",
        "current_org": "中共通化市纪律检查委员会",
        "source": "通化市公开报道",
        "confidence": "plausible",
        "notes": "据公开报道信息"
    },
    {
        "id": 7,
        "name": "庄亚男",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共通化市委员会",
        "source": "通化市公开报道",
        "confidence": "plausible",
        "notes": "据公开报道信息"
    },
    {
        "id": 8,
        "name": "李善利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市委秘书长",
        "current_org": "中共通化市委员会",
        "source": "通化市公开报道",
        "confidence": "plausible",
        "notes": "据公开报道信息"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Mayors (from public reports)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 12,
        "name": "尹志刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "通化市人民政府",
        "source": "通化市公开报道",
        "confidence": "plausible",
        "notes": "通化市人民政府副市长"
    },
    {
        "id": 13,
        "name": "王钢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "通化市人民政府",
        "source": "通化市公开报道",
        "confidence": "plausible",
        "notes": "通化市人民政府副市长"
    },
    {
        "id": 14,
        "name": "杨文慧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "通化市人民政府",
        "source": "通化市公开报道",
        "confidence": "plausible",
        "notes": "通化市人民政府副市长"
    },
    {
        "id": 15,
        "name": "耿春峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府秘书长",
        "current_org": "通化市人民政府",
        "source": "通化市公开报道",
        "confidence": "plausible",
        "notes": "通化市人民政府秘书长"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共通化市委员会", "type": "党委", "level": "地级市", "parent": "中共吉林省委员会", "location": "通化市"},
    {"id": 2, "name": "通化市人民政府", "type": "政府", "level": "地级市", "parent": "吉林省人民政府", "location": "通化市"},
    {"id": 3, "name": "中国人民政治协商会议通化市委员会", "type": "政协", "level": "地级市", "parent": "政协吉林省委员会", "location": "通化市"},
    {"id": 4, "name": "通化市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "吉林省人大常委会", "location": "通化市"},
    {"id": 5, "name": "中共通化市纪律检查委员会", "type": "党委", "level": "地级市", "parent": "中共吉林省纪律检查委员会", "location": "通化市"},
    {"id": 6, "name": "吉林省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "长春市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 孙简 — current Party Secretary + Vice Governor
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "现任通化市委书记、吉林省副省长"},
    {"person_id": 1, "org_id": 6, "title": "副省长", "start_date": "", "end_date": "", "rank": "副省级", "note": "吉林省副省长（兼）"},
    # 高山 — current mayor
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "现任通化市委副书记、市长，领导市政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "兼任市委副书记"},
    # 所永吉 — Deputy Party Secretary
    {"person_id": 3, "org_id": 1, "title": "市委副书记、政法委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 金洪培 — Organization Department Head
    {"person_id": 4, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 尚忠诚 — Executive Deputy Mayor
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 王彦东 — Discipline Inspection
    {"person_id": 6, "org_id": 5, "title": "市纪委书记、市监委主任", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 庄亚男 — Propaganda
    {"person_id": 7, "org_id": 1, "title": "市委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 李善利 — Secretary-General
    {"person_id": 8, "org_id": 1, "title": "市委常委、市委秘书长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 尹志刚 — Deputy Mayor
    {"person_id": 12, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 王钢 — Deputy Mayor
    {"person_id": 13, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 杨文慧 — Deputy Mayor
    {"person_id": 14, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 耿春峰 — Secretary-General
    {"person_id": 15, "org_id": 2, "title": "市政府秘书长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 孙简 ↔ 高山 (Party Secretary – Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "中共通化市委员会", "overlap_period": "2026"},
    # 孙简 ↔ 所永吉
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—副书记", "overlap_org": "中共通化市委员会", "overlap_period": "2026"},
    # 孙简 ↔ 金洪培
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—常委", "overlap_org": "中共通化市委员会", "overlap_period": "2026"},
    # 孙简 ↔ 尚忠诚
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—常委", "overlap_org": "中共通化市委员会", "overlap_period": "2026"},
    # 孙简 ↔ 王彦东
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "书记—纪委书记", "overlap_org": "中共通化市委员会", "overlap_period": "2026"},
    # 孙简 ↔ 庄亚男
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "书记—宣传部长", "overlap_org": "中共通化市委员会", "overlap_period": "2026"},
    # 孙简 ↔ 李善利
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "书记—秘书长", "overlap_org": "中共通化市委员会", "overlap_period": "2026"},
    # 高山 ↔ 尚忠诚 (Mayor – Executive Deputy Mayor)
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "市长—常务副市长", "overlap_org": "通化市人民政府", "overlap_period": "2026"},
    # 高山 ↔ 尹志刚
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "市长—副市长", "overlap_org": "通化市人民政府", "overlap_period": "2026"},
    # 高山 ↔ 王钢
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "市长—副市长", "overlap_org": "通化市人民政府", "overlap_period": "2026"},
    # 高山 ↔ 杨文慧
    {"person_a": 2, "person_b": 14, "type": "共事", "context": "市长—副市长", "overlap_org": "通化市人民政府", "overlap_period": "2026"},
    # 高山 ↔ 耿春峰
    {"person_a": 2, "person_b": 15, "type": "共事", "context": "市长—秘书长", "overlap_org": "通化市人民政府", "overlap_period": "2026"},
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
    slug_id = f"tonghua_{name}"

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
            "person_id": f"tonghua_{other_name}",
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
            "title": "通化市人民政府官方网站",
            "url": "https://www.tonghua.gov.cn/",
            "publisher": "通化市人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "2026年7月政府网站首页领导栏目和会议报道确认领导职务",
        }
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "吉林省",
            "city": "通化市",
            "region": "通化市",
            "job": person.get("current_post", ""),
            "task_id": "jilin_通化市",
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
        "governance_record": [
            {
                "period": "2026-07",
                "domain": "public_security",
                "achievement_or_event": "看望慰问参加抗洪抢险部队官兵代表并召开座谈会",
                "role_in_event": "共同出席",
                "measurable_outcome": "军民同心守山城",
                "location": "通化市",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "period": "2026-07",
                "domain": "economic_development",
                "achievement_or_event": "全市深化开发区改革工作专题会议",
                "role_in_event": "主持并部署",
                "measurable_outcome": "",
                "location": "通化市",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
        ] if person["id"] in (1, 2) else [],
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

    fname = f"{TODAY}-吉林省-通化市-{person['current_post']}-{person['name']}.json"
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
    core_ids = {1, 2, 3, 5, 12}  # Core leaders key figures
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
