#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 武城县 (Wucheng County), 德州市, 山东省.

Level: 县
Province: 山东省
Parent city: 德州市
Targets: 县委书记 (Party Secretary), 县长 (County Magistrate)
Task ID: shandong_武城县

Research date: 2026-07-25

Current status (as of 2026-07-25, based on available knowledge):
- 县委书记: 待查 — All web search tools were blocked/rate-limited during research.
- 县长: 待查 — All web search tools were blocked/rate-limited during research.

Confidence notes:
  All web search tools (Exa rate-limited, Baidu/Google/Bing/DuckDuckGo timed out,
  Jina Reader transport errors, government website www.wucheng.gov.cn accessible
  only for homepage — leadership page routes all returned 404 or timed out) were
  unavailable during research.

  Leadership identification cannot be confirmed without working web search.
  All information should be treated as "unverified" pending independent research.

  This is a partial-evidence build per source_fallbacks.md artifact mode.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

STAGING_DIR = Path(__file__).resolve().parent
REPO_ROOT = (STAGING_DIR / ".." / ".." / "..").resolve()
if not (REPO_ROOT / "gov_relation").exists():
    REPO_ROOT = (STAGING_DIR / ".." / ".." / ".." / "..").resolve()
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "武城县"

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-25"
TODAY = "20260725"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership — UNVERIFIED
    # All web search tools unavailable during research.
    # Names and roles marked as "待查" (to be checked).
    # ════════════════════════════════════════

    # 1. 县委书记 — 待查 (Party Secretary)
    {
        "id": 1,
        "name": "待查_县委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共武城县委书记",
        "current_org": "中共武城县委员会",
        "source": "待查 — 网络搜索工具全部不可用",
    },
    # 2. 县长 — 待查 (County Magistrate)
    {
        "id": 2,
        "name": "待查_县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武城县人民政府县长",
        "current_org": "武城县人民政府",
        "source": "待查 — 网络搜索工具全部不可用",
    },
    # 3. 县委副书记（专职副书记）— 待查
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
        "current_post": "中共武城县委副书记",
        "current_org": "中共武城县委员会",
        "source": "待查",
    },
    # 4. 县委常委、副县长（常务）— 待查
    {
        "id": 4,
        "name": "待查_常务副县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武城县委常委、副县长",
        "current_org": "武城县人民政府",
        "source": "待查",
    },
    # 5. 县委常委、纪委书记、监委主任 — 待查
    {
        "id": 5,
        "name": "待查_纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武城县委常委、县纪委书记、县监委主任",
        "current_org": "中共武城县纪律检查委员会",
        "source": "待查",
    },
    # 6. 县委常委、组织部部长 — 待查
    {
        "id": 6,
        "name": "待查_组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武城县委常委、组织部部长",
        "current_org": "中共武城县委组织部",
        "source": "待查",
    },
    # 7. 县委常委、宣传部部长 — 待查
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
        "current_post": "武城县委常委、宣传部部长",
        "current_org": "中共武城县委宣传部",
        "source": "待查",
    },
    # 8. 县委常委、政法委书记 — 待查
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
        "current_post": "武城县委常委、政法委书记",
        "current_org": "中共武城县委政法委员会",
        "source": "待查",
    },
    # 9. 县委常委、统战部部长 — 待查
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
        "current_post": "武城县委常委、统战部部长",
        "current_org": "中共武城县委统战部",
        "source": "待查",
    },
    # 10. 县委常委、县委办公室主任 — 待查
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
        "current_post": "武城县委常委、县委办公室主任",
        "current_org": "中共武城县委办公室",
        "source": "待查",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共武城县委员会", "type": "党委", "level": "县处级", "parent": "中共德州市委", "location": "德州市武城县"},
    {"id": 2, "name": "武城县人民政府", "type": "政府", "level": "县处级", "parent": "德州市人民政府", "location": "德州市武城县"},
    {"id": 3, "name": "中共武城县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共武城县委员会", "location": "德州市武城县"},
    {"id": 4, "name": "中共武城县委组织部", "type": "党委", "level": "县处级", "parent": "中共武城县委员会", "location": "德州市武城县"},
    {"id": 5, "name": "中共武城县委宣传部", "type": "党委", "level": "县处级", "parent": "中共武城县委员会", "location": "德州市武城县"},
    {"id": 6, "name": "中共武城县委统战部", "type": "党委", "level": "县处级", "parent": "中共武城县委员会", "location": "德州市武城县"},
    {"id": 7, "name": "中共武城县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共武城县委员会", "location": "德州市武城县"},
    {"id": 8, "name": "中共武城县委办公室", "type": "党委", "level": "县处级", "parent": "中共武城县委员会", "location": "德州市武城县"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS (person_id, org_id, title, start, end, rank, note)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 县委书记（待查）
    {"person_id": 1, "org_id": 1, "title": "中共武城县委书记", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 县长（待查）
    {"person_id": 2, "org_id": 2, "title": "武城县人民政府县长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 专职副书记（待查）
    {"person_id": 3, "org_id": 1, "title": "中共武城县委副书记", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 常务副县长（待查）
    {"person_id": 4, "org_id": 2, "title": "武城县委常委、副县长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 县纪委书记（待查）
    {"person_id": 5, "org_id": 3, "title": "武城县委常委、县纪委书记、县监委主任", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 组织部部长（待查）
    {"person_id": 6, "org_id": 4, "title": "武城县委常委、组织部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 宣传部部长（待查）
    {"person_id": 7, "org_id": 5, "title": "武城县委常委、宣传部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 政法委书记（待查）
    {"person_id": 8, "org_id": 7, "title": "武城县委常委、政法委书记", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 统战部部长（待查）
    {"person_id": 9, "org_id": 6, "title": "武城县委常委、统战部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 县委办公室主任（待查）
    {"person_id": 10, "org_id": 8, "title": "武城县委常委、县委办公室主任", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # No relationships can be confirmed without knowing the current leaders.
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
            "confidence": "unverified",
            "source_ids": ["S001"],
        })

    rel_entries = []
    for r in relationships_subset:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id and p["id"] != pid), None)
        if other:
            rel_entries.append({
                "person": other["name"],
                "person_id": f"wucheng_{other['name']}",
                "relationship_type": r.get("type", "unknown"),
                "strength": "weak",
                "evidence": r.get("context", ""),
                "overlap_org": r.get("overlap_org", ""),
                "overlap_period": r.get("overlap_period", ""),
                "direction": "undirected",
                "confidence": "unverified",
                "source_ids": ["S001"],
            })

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "山东省",
            "city": "德州市",
            "region": "武城县",
            "job": person["current_post"],
            "task_id": "shandong_武城县",
            "time_focus": "",
        },
        "identity": {
            "person_id": f"wucheng_{person['name']}",
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
            "promotion_velocity": {"summary": "公开资料不足，无法判断", "notable_fast_promotions": []},
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
            {"id": "S001", "title": "综合搜索（未成功）", "url": "", "publisher": "综合", "published_at": "", "accessed_at": AS_OF, "source_type": "inferred", "reliability": "low", "notes": "所有Web搜索工具（Exa、百度、Google、Bing、DuckDuckGo、Jina Reader）均不可用。武城县政府网站www.wucheng.gov.cn首页可访问但领导之窗页面404/超时。"},
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "全部领导班子成员具体人选和履历均待查。所有网络搜索工具在调研期间均不可用。",
        },
        "open_questions": [
            {"priority": "critical", "question": "武城县现任县委书记姓名和完整履历", "why_it_matters": "核心目标人物，关系网络中心", "suggested_queries": ["武城县 县委书记", "武城县委书记 简历", "武城县 领导之窗"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "武城县现任县长姓名和完整履历", "why_it_matters": "核心目标人物，政府一把手", "suggested_queries": ["武城县 县长", "武城县县长 简历"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "武城县县委领导班子完整名单（含专职副书记、常务副县长、县纪委书记、组织部长、宣传部长、政法委书记、统战部长、县委办主任）", "why_it_matters": "完整领导班子是网络分析的基础", "suggested_queries": ["武城县 领导班子", "武城县委 常委", "武城县 领导分工"], "last_attempted": AS_OF},
            {"priority": "high", "question": "武城县政府网站领导之窗页面的正确URL", "why_it_matters": "领导之窗是最可靠的官方来源", "suggested_queries": ["site:wucheng.gov.cn 领导", "武城县 领导分工 2025"], "last_attempted": AS_OF},
            {"priority": "high", "question": "武城县前任县委书记和前任县长的姓名和去向", "why_it_matters": "了解德州干部交流模式", "suggested_queries": ["武城县委原书记", "武城县原县长 调任"], "last_attempted": AS_OF},
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
    print(f"  武城县 领导班子工作关系网络")
    print(f"  等级: 县")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 公开搜索受限 — 全部 Web 搜索工具不可用")
    print(f"  所有领导班子成员标注为「待查」需后续实地调研")
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

    print(f"\n✅ 武城县数据构建完成。")
    print(f"   DB:  {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
    print(f"   JSONs: {PERSONS_DIR}/")
