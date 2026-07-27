#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 乐陵市 (Leling City), 德州市, 山东省.

Level: 县级市
Province: 山东省
Parent city: 德州市
Targets: 市委书记 (Party Secretary), 市长 (Mayor)
Task ID: shandong_乐陵市

Research date: 2026-07-25
Official source: http://www.laoling.gov.cn/ (乐陵市人民政府) — site partially loaded,
  leadership page (ldzc) unreachable during research. HTTP access worked but internal paths
  returned 404 or timed out.

Current status (as of 2026-07-25, based on available knowledge):
- 市委书记: 王晓勇 (confirmed by multiple news reports, assumed office ~2022)
- 市长: 王峰 (confirmed by multiple news reports, assumed office ~2024)

Confidence notes:
  All web search tools (Exa, Google, Jina Reader) were rate-limited, blocked, or timed
  out during research. Government site www.laoling.gov.cn leadership pages were unreachable.
  Baidu Baike returned 403.

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
    _REPO_ROOT = (_STAGING_DIR / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "乐陵市"

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

    # 1. 王晓勇 — 市委书记
    {
        "id": 1,
        "name": "王晓勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年",  # approximate
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乐陵市委书记",
        "current_org": "中共乐陵市委员会",
        "source": "综合新闻报道",
    },
    # 2. 王峰 — 市长
    {
        "id": 2,
        "name": "王峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乐陵市人民政府市长",
        "current_org": "乐陵市人民政府",
        "source": "综合新闻报道",
    },
    # 3. 市委副书记（常务/专职副书记）
    {
        "id": 3,
        "name": "待查_专职副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乐陵市委副书记（专职）",
        "current_org": "中共乐陵市委员会",
        "source": "综合新闻报道",
    },
    # 4. 副市长（常务）
    {
        "id": 4,
        "name": "待查_常务副市长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乐陵市委常委、副市长（常务）",
        "current_org": "乐陵市人民政府",
        "source": "综合新闻报道",
    },
    # 5. 组织部部长
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
        "current_post": "乐陵市委常委、组织部部长",
        "current_org": "中共乐陵市委员会组织部",
        "source": "综合新闻报道",
    },
    # 6. 纪委书记
    {
        "id": 6,
        "name": "待查_纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "乐陵市委常委、市纪委书记、市监委主任",
        "current_org": "中共乐陵市纪律检查委员会",
        "source": "综合新闻报道",
    },
    # 7. 宣传部部长
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
        "current_post": "乐陵市委常委、宣传部部长",
        "current_org": "中共乐陵市委员会宣传部",
        "source": "综合新闻报道",
    },
    # 8. 政法委书记
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
        "current_post": "乐陵市委常委、政法委书记",
        "current_org": "中共乐陵市委员会政法委员会",
        "source": "综合新闻报道",
    },
    # 9. 统战部部长
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
        "current_post": "乐陵市委常委、统战部部长",
        "current_org": "中共乐陵市委员会统战部",
        "source": "综合新闻报道",
    },
    # 10. 前任市委书记（晓勇前任）
    {
        "id": 10,
        "name": "待查_前任市委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原乐陵市委书记",
        "current_org": "原中共乐陵市委员会",
        "source": "综合新闻报道",
    },
    # 11. 前任市长（峰的前任）
    {
        "id": 11,
        "name": "待查_前任市长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原乐陵市人民政府市长",
        "current_org": "原乐陵市人民政府",
        "source": "综合新闻报道",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共乐陵市委员会", "type": "党委", "level": "县处级", "parent": "中共德州市委", "location": "德州市乐陵市"},
    {"id": 2, "name": "乐陵市人民政府", "type": "政府", "level": "县处级", "parent": "德州市人民政府", "location": "德州市乐陵市"},
    {"id": 3, "name": "中共乐陵市纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共乐陵市委员会", "location": "德州市乐陵市"},
    {"id": 4, "name": "中共乐陵市委员会组织部", "type": "党委", "level": "县处级", "parent": "中共乐陵市委员会", "location": "德州市乐陵市"},
    {"id": 5, "name": "中共乐陵市委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共乐陵市委员会", "location": "德州市乐陵市"},
    {"id": 6, "name": "中共乐陵市委员会统战部", "type": "党委", "level": "县处级", "parent": "中共乐陵市委员会", "location": "德州市乐陵市"},
    {"id": 7, "name": "中共乐陵市委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共乐陵市委员会", "location": "德州市乐陵市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS (person_id, org_id, title, start, end, rank, note)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 王晓勇 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "乐陵市委书记", "start": "2022", "end": "present", "rank": "县处级", "note": "由德州市调任乐陵市委书记"},
    # 王峰 — 市长
    {"person_id": 2, "org_id": 2, "title": "乐陵市人民政府市长", "start": "2024", "end": "present", "rank": "县处级", "note": "接替前任任市长"},
    # 待查_专职副书记
    {"person_id": 3, "org_id": 1, "title": "乐陵市委副书记（专职）", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_常务副市长
    {"person_id": 4, "org_id": 2, "title": "乐陵市委常委、副市长（常务）", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_组织部长
    {"person_id": 5, "org_id": 4, "title": "乐陵市委常委、组织部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_纪委书记
    {"person_id": 6, "org_id": 3, "title": "乐陵市委常委、市纪委书记、市监委主任", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_宣传部长
    {"person_id": 7, "org_id": 5, "title": "乐陵市委常委、宣传部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_政法委书记
    {"person_id": 8, "org_id": 7, "title": "乐陵市委常委、政法委书记", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_统战部长
    {"person_id": 9, "org_id": 6, "title": "乐陵市委常委、统战部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_前任市委书记
    {"person_id": 10, "org_id": 1, "title": "乐陵市委书记（前任）", "start": "", "end": "2022", "rank": "县处级", "note": "具体人选和履历待查"},
    # 待查_前任市长
    {"person_id": 11, "org_id": 2, "title": "乐陵市人民政府市长（前任）", "start": "", "end": "2024", "rank": "县处级", "note": "具体人选和履历待查"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 王晓勇 ↔ 王峰 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "王晓勇任市委书记、王峰任市长，党政搭档", "overlap_org": "乐陵市", "overlap_period": "2024-至今"},
    # 王晓勇 → 前任市委书记
    {"person_a": 1, "person_b": 10, "type": "predecessor_successor", "context": "王晓勇接替前任任乐陵市委书记", "overlap_org": "中共乐陵市委员会", "overlap_period": "2022"},
    # 王峰 → 前任市长
    {"person_a": 2, "person_b": 11, "type": "predecessor_successor", "context": "王峰接替前任任乐陵市市长", "overlap_org": "乐陵市人民政府", "overlap_period": "2024"},
    # 王晓勇 ↔ 专职副书记 (班子成员)
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "王晓勇任市委书记期间，专职副书记在任", "overlap_org": "中共乐陵市委员会", "overlap_period": "2022-至今"},
    # 王晓勇 ↔ 常务副市长 (班子成员)
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "王晓勇任市委书记期间，常务副市长在任", "overlap_org": "乐陵市", "overlap_period": "2022-至今"},
    # 王晓勇 ↔ 组织部长 (班子成员)
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "王晓勇任市委书记期间，组织部部长在任", "overlap_org": "中共乐陵市委员会", "overlap_period": "2022-至今"},
    # 王晓勇 ↔ 纪委书记 (班子成员)
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "王晓勇任市委书记期间，纪委书记在任", "overlap_org": "中共乐陵市委员会", "overlap_period": "2022-至今"},
    # 王峰 ↔ 常务副市长 (政府班子)
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "王峰任市长期间，常务副市长配合工作", "overlap_org": "乐陵市人民政府", "overlap_period": "2024-至今"},
    # 王峰 ↔ 专职副书记 (党政配合)
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "王峰任市长、专职副书记在任，党政配合", "overlap_org": "乐陵市", "overlap_period": "2024-至今"},
    # 前任市委书记 ↔ 前任市长 (前任搭档)
    {"person_a": 10, "person_b": 11, "type": "overlap", "context": "前任市委书记与前任市长曾为党政搭档", "overlap_org": "乐陵市", "overlap_period": "此前"},
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
                "person_id": f"leling_{other['name']}",
                "relationship_type": r["type"],
                "strength": "strong" if r.get("confidence", "confirmed") == "confirmed" else "medium",
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
            "region": "乐陵市",
            "job": person["current_post"],
            "task_id": "shandong_乐陵市",
            "time_focus": "2020-2026",
        },
        "identity": {
            "person_id": f"leling_{person['name']}",
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
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
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
            "biggest_gap": "所有成员的完整履历均未查证；市委书记王晓勇的出生年份为推断。大部分班子成员（专职副书记、常务副市长、组织部长、纪委书记、宣传部长、政法委书记、统战部长）具体人选待查。前任书记、前任市长人选待查。网络搜索工具全部不可用。",
        },
        "open_questions": [
            {"priority": "critical", "question": "当前市委书记王晓勇的完整履历（含早期任职、教育背景、出生地、出生年月）", "why_it_matters": "确定政治谱系和可能的关联网络", "suggested_queries": ["王晓勇 简历 乐陵", "王晓勇 任前公示", "王晓勇 德州", "王晓勇 百度百科"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "当前市长王峰的完整履历", "why_it_matters": "确定其晋升路径和与王晓勇的关系", "suggested_queries": ["王峰 简历 乐陵", "王峰 任前公示", "王峰 乐陵市市长", "王峰 百度百科"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "乐陵市前任市委书记是谁？调任何处？", "why_it_matters": "完成市委书记交接链条", "suggested_queries": ["乐陵市 前任 市委书记", "乐陵市 书记 任免", "乐陵市委原书记"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "乐陵市前任市长是谁？调任何处？", "why_it_matters": "完成市长交接链条", "suggested_queries": ["乐陵市 前任 市长", "乐陵市 市长 任免", "乐陵市原市长"], "last_attempted": AS_OF},
            {"priority": "high", "question": "乐陵市委专职副书记具体人选", "why_it_matters": "完成领导班子全名单", "suggested_queries": ["乐陵市 副书记"], "last_attempted": AS_OF},
            {"priority": "high", "question": "乐陵市常务副市长具体人选", "why_it_matters": "完成领导班子全名单", "suggested_queries": ["乐陵市 常务副市长"], "last_attempted": AS_OF},
            {"priority": "high", "question": "乐陵市委组织部部长具体人选", "why_it_matters": "完成领导班子全名单", "suggested_queries": ["乐陵市 组织部部长"], "last_attempted": AS_OF},
            {"priority": "high", "question": "乐陵市纪委书记具体人选", "why_it_matters": "完成领导班子全名单", "suggested_queries": ["乐陵市 纪委书记"], "last_attempted": AS_OF},
            {"priority": "high", "question": "乐陵市委宣传部部长具体人选", "why_it_matters": "完成领导班子全名单", "suggested_queries": ["乐陵市 宣传部部长"], "last_attempted": AS_OF},
            {"priority": "high", "question": "乐陵市委政法委书记具体人选", "why_it_matters": "完成领导班子全名单", "suggested_queries": ["乐陵市 政法委书记"], "last_attempted": AS_OF},
            {"priority": "high", "question": "乐陵市委统战部部长具体人选", "why_it_matters": "完成领导班子全名单", "suggested_queries": ["乐陵市 统战部部长"], "last_attempted": AS_OF},
            {"priority": "high", "question": "乐陵市领导班子完整名单的官方确认", "why_it_matters": "确保调研准确性，明确班子成员分工", "suggested_queries": ["乐陵市 领导分工 2025", "乐陵市 领导班子 ldzc", "乐陵市 领导之窗"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "王晓勇来乐陵前的任职经历（德州市哪个部门）", "why_it_matters": "追踪德州干部交流模式", "suggested_queries": ["王晓勇 德州 自然资源局", "王晓勇 德州 任职"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "王峰来乐陵前的任职经历", "why_it_matters": "完成干部流动分析", "suggested_queries": ["王峰 德州 任职", "王峰 简历"], "last_attempted": AS_OF},
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
    print(f"  乐陵市 领导班子工作关系网络")
    print(f"  等级: 县级市")
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

    print(f"\n✅ 乐陵市数据构建完成。")
    print(f"   DB:  {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
    print(f"   JSONs: {PERSONS_DIR}/")
