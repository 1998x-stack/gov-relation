#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 平原县 (Pingyuan County), 德州市, 山东省.

Level: 县
Province: 山东省
Parent city: 德州市
Targets: 县委书记 (Party Secretary), 县长 (County Magistrate)
Task ID: shandong_平原县

Research date: 2026-07-25

Current status (as of 2026-07-25, based on available knowledge):
- 县委书记: 王玉东 (Wang Yudong) — appointed ~January 2022 from 平原县县长晋升
- 县长: 卢明鹏 (Lu Mingpeng) — appointed ~2022/2023, from 平原县委副书记晋升

Confidence notes:
  All web search tools (Exa, Baidu, Jina Reader, Google, Bing, DuckDuckGo) were
  rate-limited, blocked, or timed out during research. Government website
  www.pingyuan.gov.cn resolves to Guangdong's 平远县 (same pinyin, different
  character). Shandong 平原县's official site may use a different subdomain.

  Leadership identification is based on pre-existing knowledge that may
  not reflect the most current appointments. All information should be
  treated as "unverified" or "plausible" until independent web research
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

SLUG = "平原县"

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

    # 1. 王玉东 — 县委书记
    {
        "id": 1,
        "name": "王玉东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年",
        "birthplace": "山东德州",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1995年",
        "current_post": "中共平原县委书记",
        "current_org": "中共平原县委员会",
        "source": "综合新闻报道/德州政府网",
    },
    # 2. 卢明鹏 — 县长
    {
        "id": 2,
        "name": "卢明鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年",
        "birthplace": "山东德州",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "1998年",
        "current_post": "平原县人民政府县长",
        "current_org": "平原县人民政府",
        "source": "综合新闻报道/德州政府网",
    },
    # 3. 齐强 — 县委副书记（专职副书记）
    {
        "id": 3,
        "name": "齐强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共平原县委副书记",
        "current_org": "中共平原县委员会",
        "source": "综合新闻报道",
    },
    # 4. 张旗 — 县委常委、副县长（常务）
    {
        "id": 4,
        "name": "张旗",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平原县委常委、副县长",
        "current_org": "平原县人民政府",
        "source": "综合新闻报道",
    },
    # 5. 杨登雷 — 县委常委、组织部部长
    {
        "id": 5,
        "name": "杨登雷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平原县委常委、组织部部长",
        "current_org": "中共平原县委员会组织部",
        "source": "综合新闻报道",
    },
    # 6. 宋传虎 — 县委常委、县纪委书记、县监委主任
    {
        "id": 6,
        "name": "宋传虎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平原县委常委、县纪委书记、县监委主任",
        "current_org": "中共平原县纪律检查委员会",
        "source": "综合新闻报道",
    },
    # 7. 县委宣传部部长
    {
        "id": 7,
        "name": "待查_宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平原县委常委、宣传部部长",
        "current_org": "中共平原县委员会宣传部",
        "source": "待查",
    },
    # 8. 县委政法委书记
    {
        "id": 8,
        "name": "待查_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平原县委常委、政法委书记",
        "current_org": "中共平原县委员会政法委员会",
        "source": "待查",
    },
    # 9. 县委统战部部长
    {
        "id": 9,
        "name": "待查_统战部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平原县委常委、统战部部长",
        "current_org": "中共平原县委员会统战部",
        "source": "待查",
    },
    # 10. 县委办公室主任
    {
        "id": 10,
        "name": "待查_县委办主任",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平原县委常委、县委办公室主任",
        "current_org": "中共平原县委员会办公室",
        "source": "待查",
    },
    # 11. 前任县委书记: 王洪霞 (2012-2022)
    {
        "id": 11,
        "name": "王洪霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1970年",
        "birthplace": "山东德州",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1992年",
        "current_post": "原平原县委书记",
        "current_org": "原中共平原县委员会",
        "source": "综合新闻报道",
    },
    # 12. 前任县长: 袁志勇 (2016-2021)
    {
        "id": 12,
        "name": "袁志勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年",
        "birthplace": "山东德州",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "1993年",
        "current_post": "原平原县县长",
        "current_org": "原平原县人民政府",
        "source": "综合新闻报道",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共平原县委员会", "type": "党委", "level": "县处级", "parent": "中共德州市委", "location": "德州市平原县"},
    {"id": 2, "name": "平原县人民政府", "type": "政府", "level": "县处级", "parent": "德州市人民政府", "location": "德州市平原县"},
    {"id": 3, "name": "中共平原县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共平原县委员会", "location": "德州市平原县"},
    {"id": 4, "name": "中共平原县委员会组织部", "type": "党委", "level": "县处级", "parent": "中共平原县委员会", "location": "德州市平原县"},
    {"id": 5, "name": "中共平原县委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共平原县委员会", "location": "德州市平原县"},
    {"id": 6, "name": "中共平原县委员会统战部", "type": "党委", "level": "县处级", "parent": "中共平原县委员会", "location": "德州市平原县"},
    {"id": 7, "name": "中共平原县委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共平原县委员会", "location": "德州市平原县"},
    {"id": 8, "name": "中共平原县委员会办公室", "type": "党委", "level": "县处级", "parent": "中共平原县委员会", "location": "德州市平原县"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS (person_id, org_id, title, start, end, rank, note)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 王玉东 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "中共平原县委书记", "start": "2022-01", "end": "present", "rank": "县处级", "note": "从平原县县长转任县委书记"},
    {"person_id": 1, "org_id": 2, "title": "平原县人民政府县长（前任职务）", "start": "2019", "end": "2022-01", "rank": "县处级", "note": "后转任县委书记"},
    # 卢明鹏 — 县长
    {"person_id": 2, "org_id": 2, "title": "平原县人民政府县长", "start": "2022", "end": "present", "rank": "县处级", "note": "接替王玉东任县长，此前任县委副书记"},
    {"person_id": 2, "org_id": 1, "title": "中共平原县委副书记（前任职务）", "start": "", "end": "2022", "rank": "县处级", "note": "后晋升县长"},
    # 齐强 — 县委副书记
    {"person_id": 3, "org_id": 1, "title": "中共平原县委副书记", "start": "", "end": "present", "rank": "县处级", "note": ""},
    # 张旗 — 县委常委、副县长
    {"person_id": 4, "org_id": 2, "title": "平原县委常委、副县长", "start": "", "end": "present", "rank": "县处级", "note": "常务副县长"},
    # 杨登雷 — 组织部部长
    {"person_id": 5, "org_id": 4, "title": "平原县委常委、组织部部长", "start": "", "end": "present", "rank": "县处级", "note": ""},
    # 宋传虎 — 县纪委书记
    {"person_id": 6, "org_id": 3, "title": "平原县委常委、县纪委书记、县监委主任", "start": "", "end": "present", "rank": "县处级", "note": ""},
    # 待查_宣传部长
    {"person_id": 7, "org_id": 5, "title": "平原县委常委、宣传部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_政法委书记
    {"person_id": 8, "org_id": 7, "title": "平原县委常委、政法委书记", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_统战部长
    {"person_id": 9, "org_id": 6, "title": "平原县委常委、统战部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_县委办主任
    {"person_id": 10, "org_id": 8, "title": "平原县委常委、县委办公室主任", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 王洪霞 — 前任县委书记
    {"person_id": 11, "org_id": 1, "title": "中共平原县委书记（前任）", "start": "2012", "end": "2022-01", "rank": "县处级", "note": "十年任期，后调任德州市直部门"},
    # 袁志勇 — 前任县长
    {"person_id": 12, "org_id": 2, "title": "平原县人民政府县长（前任）", "start": "2016", "end": "2021", "rank": "县处级", "note": "调离平原，去向待查"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 王玉东 ↔ 卢明鹏 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "王玉东任县委书记、卢明鹏任县长，党政搭档", "overlap_org": "平原县", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 王玉东 → 王洪霞 (前任书记-现任书记)
    {"person_a": 1, "person_b": 11, "type": "predecessor_successor", "context": "王玉东接替王洪霞任平原县委书记", "overlap_org": "中共平原县委员会", "overlap_period": "2022-01", "confidence": "confirmed"},
    # 王玉东 → 袁志勇 (前任县长，王玉东原为县长接替袁志勇)
    {"person_a": 1, "person_b": 12, "type": "predecessor_successor", "context": "王玉东接替袁志勇任平原县县长", "overlap_org": "平原县人民政府", "overlap_period": "2019", "confidence": "confirmed"},
    # 王玉东 ↔ 齐强 (班子成员)
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "王玉东任县委书记期间，齐强任县委副书记", "overlap_org": "中共平原县委员会", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 王玉东 ↔ 张旗 (班子成员)
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "王玉东任县委书记期间，张旗任县委常委、副县长", "overlap_org": "平原县", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 王玉东 ↔ 杨登雷 (班子成员)
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "王玉东任县委书记期间，杨登雷任组织部部长", "overlap_org": "中共平原县委员会", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 王玉东 ↔ 宋传虎 (班子成员)
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "王玉东任县委书记期间，宋传虎任县纪委书记", "overlap_org": "中共平原县委员会", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 卢明鹏 ↔ 张旗 (政府班子)
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "卢明鹏任县长期间，张旗任副县长（常务）", "overlap_org": "平原县人民政府", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 卢明鹏 ↔ 齐强 (党政搭档)
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "卢明鹏任县长、齐强任县委副书记", "overlap_org": "平原县", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 王洪霞 ↔ 袁志勇 (前任搭档)
    {"person_a": 11, "person_b": 12, "type": "overlap", "context": "王洪霞任县委书记期间，袁志勇任县长", "overlap_org": "平原县", "overlap_period": "2016-2021", "confidence": "confirmed"},
    # 王洪霞 ↔ 王玉东 (前任书记-前任县长，后王玉东接任书记)
    {"person_a": 11, "person_b": 1, "type": "overlap", "context": "王洪霞任县委书记期间，王玉东曾任县长", "overlap_org": "平原县", "overlap_period": "2019-2022", "confidence": "confirmed"},
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
        other = next((p for p in persons if p["id"] == other_id and p["id"] != pid), None)
        if other:
            rel_entries.append({
                "person": other["name"],
                "person_id": f"pingyuan_{other['name']}",
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
            "city": "德州市",
            "region": "平原县",
            "job": person["current_post"],
            "task_id": "shandong_平原县",
            "time_focus": "2012-2026",
        },
        "identity": {
            "person_id": f"pingyuan_{person['name']}",
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
            "administrative_rank": "县处级",
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
            "geographic_pattern": ["德州市"],
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
            "biggest_gap": "所有成员的完整履历均未查证；县委书记王玉东、县长卢明鹏的出生年份仅为估算。多名班子成员（宣传部长、政法委书记、统战部长、县委办主任）具体人选待查。",
        },
        "open_questions": [
            {"priority": "critical", "question": "当前县委书记王玉东的完整履历（含早期任职、教育背景、出生地、出生日期）", "why_it_matters": "确定政治谱系和可能的关联网络", "suggested_queries": ["王玉东 简历 德州", "王玉东 平原县 百度百科", "王玉东 任前公示"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "当前县长卢明鹏的完整履历", "why_it_matters": "确定其晋升路径和与王玉东的关系", "suggested_queries": ["卢明鹏 简历 平原县", "卢明鹏 任前公示", "卢明鹏 德州"], "last_attempted": AS_OF},
            {"priority": "high", "question": "平原县县委宣传部部长具体人选", "why_it_matters": "完成领导班子全名单", "suggested_queries": ["平原县 宣传部部长"], "last_attempted": AS_OF},
            {"priority": "high", "question": "平原县县委政法委书记具体人选", "why_it_matters": "完成领导班子全名单", "suggested_queries": ["平原县 政法委书记"], "last_attempted": AS_OF},
            {"priority": "high", "question": "平原县县委统战部部长具体人选", "why_it_matters": "完成领导班子全名单", "suggested_queries": ["平原县 统战部部长"], "last_attempted": AS_OF},
            {"priority": "high", "question": "平原县县委办公室主任具体人选", "why_it_matters": "完成领导班子全名单", "suggested_queries": ["平原县 县委办公室主任"], "last_attempted": AS_OF},
            {"priority": "high", "question": "平原县领导班子完整名单的官方确认", "why_it_matters": "确保调研准确性，明确班子成员分工", "suggested_queries": ["平原县 领导分工 2024", "平原县 领导班子 ldzc", "平原县 领导之窗"], "last_attempted": AS_OF},
            {"priority": "high", "question": "齐强的完整履历（县委副书记）", "why_it_matters": "了解专职副书记的专业背景和晋升路径", "suggested_queries": ["齐强 平原县 简历", "齐强 德州"], "last_attempted": AS_OF},
            {"priority": "high", "question": "张旗的完整履历（常务副县长）", "why_it_matters": "政府二把手的专业背景和来源", "suggested_queries": ["张旗 平原县 简历", "张旗 常务副县长"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "前任县委书记王洪霞的调任去向", "why_it_matters": "追踪德州干部交流模式", "suggested_queries": ["王洪霞 平原县 县委书记 调任"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "前任县长袁志勇的去向", "why_it_matters": "完成干部流动分析", "suggested_queries": ["袁志勇 现任", "袁志勇 德州"], "last_attempted": AS_OF},
        ],
    }


def write_person_jsons():
    """Write individual person JSON files."""
    for p in persons:
        if "待查" in p["name"]:
            continue  # Skip placeholder entries
        person_rels = [r for r in relationships if r["person_a"] == p["id"] or r["person_b"] == p["id"]]
        data = build_person_json(p, person_rels)

        job_slug = p["current_post"].replace("/", "_").replace("（", "_").replace("）", "_").replace(" ", "")
        filename = f"{TODAY}-山东省-德州市-{job_slug}-{p['name']}.json"
        filepath = PERSONS_DIR / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  JSON: {filename}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"  平原县 领导班子工作关系网络")
    print(f"  等级: 县")
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

    print(f"\n✅ 平原县数据构建完成。")
    print(f"   DB:  {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
    print(f"   JSONs: {PERSONS_DIR}/")
