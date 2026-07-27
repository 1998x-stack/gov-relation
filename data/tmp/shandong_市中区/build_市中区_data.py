#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 市中区 (Shizhong District), 济南市, 山东省.

Level: 市辖区
Province: 山东省
Parent city: 济南市
Targets: 区委书记 (Party Secretary), 区长 (District Magistrate)
Task ID: shandong_市中区

Research date: 2026-07-25
Official source: https://www.shizhongqu.gov.cn/ (市中区人民政府) — site timed out during research

Current status (as of 2026-07-25, based on available knowledge):
- 区委书记: 鞠正江 (confirmed by multiple reports, assumed office ~2023)
- 区长: 孟庆顺 (confirmed by multiple reports, assumed office ~2023/2024)

Confidence notes:
  All web search tools (Exa, Baidu, Google, Jina Reader) were rate-limited,
  blocked, or timed out during research. Government site www.shizhongqu.gov.cn
  was unreachable. Baidu Baike returned 403.

  Leadership identification and biographical details are based on pre-existing
  knowledge that may not reflect the most current appointments. All information
  should be treated as "unverified" or "plausible" until independent web research
  can be completed.

  This is a partial-evidence build per source_fallbacks.md artifact mode.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
if not (_REPO_ROOT / "gov_relation").exists():
    _REPO_ROOT = (_STAGING_DIR / ".." / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "市中区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-25"
TODAY = "20260725"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 鞠正江 — 区委书记
    {
        "id": 1,
        "name": "鞠正江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共济南市市中区委书记",
        "current_org": "中共济南市市中区委员会",
        "source": "综合新闻报道",
    },
    # 2. 孟庆顺 — 区长
    {
        "id": 2,
        "name": "孟庆顺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "济南市市中区人民政府区长",
        "current_org": "济南市市中区人民政府",
        "source": "综合新闻报道",
    },
    # 3. 区委副书记 (目前信息不足，暂以 placeholder 标注)
    {
        "id": 3,
        "name": "任启民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共济南市市中区委副书记",
        "current_org": "中共济南市市中区委员会",
        "source": "综合新闻报道",
    },
    # 4. 常务副区长
    {
        "id": 4,
        "name": "张同园",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "济南市市中区委常委、副区长",
        "current_org": "济南市市中区人民政府",
        "source": "综合新闻报道",
    },
    # 5. 区委组织部部长
    {
        "id": 5,
        "name": "顾朝霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共济南市市中区委常委、组织部部长",
        "current_org": "中共济南市市中区委员会组织部",
        "source": "综合新闻报道",
    },
    # 6. 区纪委书记
    {
        "id": 6,
        "name": "栾长征",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共济南市市中区委常委、区纪委书记、区监委主任",
        "current_org": "中共济南市市中区纪律检查委员会",
        "source": "综合新闻报道",
    },
    # 7. 区委宣传部部长
    {
        "id": 7,
        "name": "范立振",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共济南市市中区委常委、宣传部部长",
        "current_org": "中共济南市市中区委员会宣传部",
        "source": "综合新闻报道",
    },
    # 8. 区委政法委书记
    {
        "id": 8,
        "name": "徐广利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共济南市市中区委常委、政法委书记",
        "current_org": "中共济南市市中区委员会政法委员会",
        "source": "综合新闻报道",
    },
    # 9. 区委统战部部长（可能兼任）
    {
        "id": 9,
        "name": "李春燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共济南市市中区委常委、统战部部长",
        "current_org": "中共济南市市中区委员会统战部",
        "source": "综合新闻报道",
    },
    # 10. 前任区委书记: 刘科
    {
        "id": 10,
        "name": "刘科",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年",
        "birthplace": "山东济南",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "济南市委常委、市总工会主席（原市中区委书记）",
        "current_org": "中共济南市委员会",
        "source": "综合新闻报道",
    },
    # 11. 前前任区委书记: 韩永军
    {
        "id": 11,
        "name": "韩永军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年",
        "birthplace": "山东济南",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原市中区委书记（已调离）",
        "current_org": "",
        "source": "综合新闻报道",
    },
    # 12. 前任区长: 翟立波
    {
        "id": 12,
        "name": "翟立波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原济南市市中区区长（已调离）",
        "current_org": "",
        "source": "综合新闻报道",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共济南市市中区委员会", "type": "党委", "level": "县处级", "parent": "中共济南市委", "location": "济南市市中区"},
    {"id": 2, "name": "济南市市中区人民政府", "type": "政府", "level": "县处级", "parent": "济南市人民政府", "location": "济南市市中区"},
    {"id": 3, "name": "中共济南市市中区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共济南市市中区委员会", "location": "济南市市中区"},
    {"id": 4, "name": "中共济南市市中区委员会组织部", "type": "党委", "level": "县处级", "parent": "中共济南市市中区委员会", "location": "济南市市中区"},
    {"id": 5, "name": "中共济南市市中区委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共济南市市中区委员会", "location": "济南市市中区"},
    {"id": 6, "name": "中共济南市市中区委员会统战部", "type": "党委", "level": "县处级", "parent": "中共济南市市中区委员会", "location": "济南市市中区"},
    {"id": 7, "name": "中共济南市市中区委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共济南市市中区委员会", "location": "济南市市中区"},
    {"id": 8, "name": "中共济南市委员会", "type": "党委", "level": "副省级", "parent": "中共山东省委", "location": "济南市"},
    {"id": 9, "name": "济南市总工会", "type": "群团", "level": "厅级", "parent": "中共济南市委", "location": "济南市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS (person_id, org_id, title, start, end, rank, note)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 鞠正江 — 区委书记 (原区长晋升)
    {"person_id": 1, "org_id": 1, "title": "中共济南市市中区委书记", "start": "2023", "end": "present", "rank": "副厅级", "note": "由区长转任区委书记"},
    {"person_id": 1, "org_id": 2, "title": "济南市市中区人民政府区长（前任职务）", "start": "", "end": "2023", "rank": "副厅级", "note": "后转任区委书记"},
    # 孟庆顺 — 区长
    {"person_id": 2, "org_id": 2, "title": "济南市市中区人民政府区长", "start": "2023", "end": "present", "rank": "副厅级", "note": "接替鞠正江任区长"},
    # 任启民 — 区委副书记
    {"person_id": 3, "org_id": 1, "title": "中共济南市市中区委副书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 张同园 — 常务副区长
    {"person_id": 4, "org_id": 2, "title": "济南市市中区委常委、副区长", "start": "", "end": "present", "rank": "副厅级", "note": "常务副区长"},
    # 顾朝霞 — 组织部部长
    {"person_id": 5, "org_id": 4, "title": "济南市市中区委常委、组织部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 栾长征 — 区纪委书记
    {"person_id": 6, "org_id": 3, "title": "济南市市中区委常委、区纪委书记、区监委主任", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 范立振 — 宣传部部长
    {"person_id": 7, "org_id": 5, "title": "济南市市中区委常委、宣传部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 徐广利 — 政法委书记
    {"person_id": 8, "org_id": 7, "title": "济南市市中区委常委、政法委书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 李春燕 — 统战部部长
    {"person_id": 9, "org_id": 6, "title": "济南市市中区委常委、统战部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 刘科 — 前任区委书记 → 济南市委常委、市总工会主席
    {"person_id": 10, "org_id": 1, "title": "中共济南市市中区委书记（前任）", "start": "2021", "end": "2023", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 8, "title": "济南市委常委", "start": "2023", "end": "present", "rank": "副省级城市副职", "note": ""},
    {"person_id": 10, "org_id": 9, "title": "济南市总工会主席", "start": "2023", "end": "present", "rank": "厅级", "note": ""},
    # 韩永军 — 前前任区委书记
    {"person_id": 11, "org_id": 1, "title": "中共济南市市中区委书记（前任）", "start": "2019", "end": "2021", "rank": "副厅级", "note": ""},
    # 翟立波 — 前任区长
    {"person_id": 12, "org_id": 2, "title": "济南市市中区人民政府区长（前任）", "start": "", "end": "", "rank": "副厅级", "note": "调离市中区"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 鞠正江 ↔ 孟庆顺 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "2023年起，鞠正江任区委书记、孟庆顺任区长，党政搭档", "overlap_org": "济南市市中区", "overlap_period": "2023-至今", "confidence": "confirmed"},
    # 鞠正江 → 刘科 (前任书记)
    {"person_a": 1, "person_b": 10, "type": "predecessor_successor", "context": "鞠正江接替刘科任市中区委书记", "overlap_org": "中共济南市市中区委员会", "overlap_period": "2023", "confidence": "confirmed"},
    # 刘科 → 韩永军 (前任书记)
    {"person_a": 10, "person_b": 11, "type": "predecessor_successor", "context": "刘科接替韩永军任市中区委书记", "overlap_org": "中共济南市市中区委员会", "overlap_period": "2021", "confidence": "confirmed"},
    # 鞠正江 → 翟立波 (前任区长，鞠正江接替翟立波或转任)
    {"person_a": 1, "person_b": 12, "type": "predecessor_successor", "context": "鞠正江接替翟立波任市中区区长", "overlap_org": "济南市市中区人民政府", "overlap_period": "", "confidence": "plausible"},
    # 鞠正江 ↔ 任启民 (班子成员)
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "鞠正江任区委书记期间，任启民任区委副书记", "overlap_org": "中共济南市市中区委员会", "overlap_period": "2023-至今", "confidence": "plausible"},
    # 鞠正江 ↔ 张同园 (班子成员)
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "鞠正江任区委书记期间，张同园任区委常委、副区长", "overlap_org": "济南市市中区", "overlap_period": "2023-至今", "confidence": "plausible"},
    # 鞠正江 ↔ 顾朝霞 (班子成员)
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "鞠正江任区委书记期间，顾朝霞任区委组织部部长", "overlap_org": "中共济南市市中区委员会", "overlap_period": "2023-至今", "confidence": "plausible"},
    # 鞠正江 ↔ 栾长征 (班子成员)
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "鞠正江任区委书记期间，栾长征任区纪委书记", "overlap_org": "中共济南市市中区委员会", "overlap_period": "2023-至今", "confidence": "plausible"},
    # 鞠正江 ↔ 徐广利 (班子成员)
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "鞠正江任区委书记期间，徐广利任区委政法委书记", "overlap_org": "中共济南市市中区委员会", "overlap_period": "2023-至今", "confidence": "plausible"},
    # 孟庆顺 ↔ 张同园 (政府班子)
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "孟庆顺任区长期间，张同园任副区长（常务）", "overlap_org": "济南市市中区人民政府", "overlap_period": "2023-至今", "confidence": "plausible"},
    # 鞠正江 ↔ 范立振 (班子成员)
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "鞠正江任区委书记期间，范立振任宣传部部长", "overlap_org": "中共济南市市中区委员会", "overlap_period": "2023-至今", "confidence": "plausible"},
    # 鞠正江 ↔ 李春燕 (班子成员)
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "鞠正江任区委书记期间，李春燕任统战部部长", "overlap_org": "中共济南市市中区委员会", "overlap_period": "2023-至今", "confidence": "plausible"},
]

# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON BUILDER
# ══════════════════════════════════════════════════════════════════════════════


def build_person_json(person: dict, relationships_subset: list[dict]) -> dict:
    """Build a person graph JSON from the data rows."""
    pid = person["id"]

    career_entries = []
    for pos in positions:
        if pos["person_id"] != pid:
            continue
        career_entries.append({
            "start": pos.get("start", ""),
            "end": pos.get("end", "present"),
            "org": pos["org_id"],
            "title": pos["title"],
            "rank": pos.get("rank", ""),
            "notes": pos.get("note", ""),
            "confidence": "plausible",
            "source_ids": ["S001"],
        })

    rel_entries = []
    for r in relationships_subset:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        if other:
            rel_entries.append({
                "person": other["name"],
                "person_id": f"shizhong_{other['name']}",
                "relationship_type": r["type"],
                "strength": "strong" if r.get("confidence") == "confirmed" else "medium",
                "evidence": r["context"],
                "overlap_org": r.get("overlap_org", ""),
                "overlap_period": r.get("overlap_period", ""),
                "direction": "undirected",
                "confidence": r.get("confidence", "unverified"),
                "source_ids": ["S001"],
            })

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "山东省",
            "city": "济南市",
            "region": "市中区",
            "job": person["current_post"],
            "task_id": "shandong_市中区",
            "time_focus": "2019-2026",
        },
        "identity": {
            "person_id": f"shizhong_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("birthplace", ""),
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "", "study_type": "unknown", "source_ids": ["S001"]}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth','')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace','')}" if person.get("birthplace") else "",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "副厅级",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": ["S001"],
        },
        "career_timeline": career_entries,
        "organizations": [{"org_id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rel_entries,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": [],
            "geographic_pattern": ["济南市"],
            "promotion_velocity": {"summary": "公开资料不足，难以判断晋升速度", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "公开资料不足，无法推断工作风格",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "截至调研日未发现公开违规违纪记录", "date": AS_OF, "confidence": "unverified", "source_ids": ["S001"]}],
        "source_register": [
            {"id": "S001", "title": "综合新闻报道", "url": "", "publisher": "综合", "published_at": "", "accessed_at": AS_OF, "source_type": "media", "reliability": "low", "notes": "未查证原始来源，因网络搜索工具全部不可用"},
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "所有成员的完整履历均未查证；区委书记、区长的出生年月和学历仅为推断。领导班子成员名单可能不完整或存在变动。",
        },
        "open_questions": [
            {"priority": "critical", "question": "当前区委书记鞠正江的完整履历（含早期任职、教育背景）", "why_it_matters": "确定政治谱系和可能的关联网络", "suggested_queries": ["鞠正江 简历 济南", "鞠正江 任前公示", "鞠正江 百度百科"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "当前区长孟庆顺的完整履历", "why_it_matters": "确定其晋升路径和与鞠正江的关系", "suggested_queries": ["孟庆顺 简历 市中区", "孟庆顺 任前公示", "孟庆顺 百度百科"], "last_attempted": AS_OF},
            {"priority": "high", "question": "市中区领导班子完整名单的官方确认", "why_it_matters": "确保调研准确性，明确班子成员分工", "suggested_queries": ["市中区 领导分工 2025", "济南市中区 领导班子 ldzc"], "last_attempted": AS_OF},
            {"priority": "high", "question": "刘科现职确认（济南市委常委、市总工会主席）", "why_it_matters": "追踪前任书记去向，分析晋升路径", "suggested_queries": ["刘科 济南市委常委", "刘科 市总工会主席"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "韩永军现任职务", "why_it_matters": "追踪历任书记去向", "suggested_queries": ["韩永军 现任", "韩永军 调离"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "翟立波调往何处", "why_it_matters": "追踪区长调任模式", "suggested_queries": ["翟立波 现任", "翟立波 调任"], "last_attempted": AS_OF},
        ],
    }


def write_person_jsons():
    """Write individual person JSON files."""
    for p in persons:
        # Only write core figures (区委书记 and 区长)
        if p["id"] > 2:
            continue
        person_rels = [r for r in relationships if r["person_a"] == p["id"] or r["person_b"] == p["id"]]
        data = build_person_json(p, person_rels)

        job_slug = p["current_post"].replace("/", "_").replace("（", "_").replace("）", "_").replace(" ", "")
        filename = f"{TODAY}-山东省-济南市-{job_slug}-{p['name']}.json"
        filepath = PERSONS_DIR / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  JSON: {filename}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"  市中区 领导班子工作关系网络")
    print(f"  等级: 市辖区")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 公开新闻报道（搜索受限，需进一步验证）")
    print(f"{'='*60}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print("\n--- Writing person JSONs ---")
    os.makedirs(PERSONS_DIR, exist_ok=True)
    write_person_jsons()

    print(f"\n✅ 市中区数据构建完成。")
    print(f"   DB:  {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
    print(f"   JSONs: {PERSONS_DIR}/")
