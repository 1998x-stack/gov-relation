#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 阳信县, 滨州市, 山东省.

Level: 县
Province: 山东省
Parent city: 滨州市
Targets: 县委书记 (Party Secretary), 县长 (County Magistrate)
Task ID: shandong_阳信县

Research date: 2026-07-26

Current status (as of 2026-07-26, based on available knowledge):
- 县委书记: 刘荩一 (Liu Jinyi) — appointed ~2021-2022 from 阳信县县长晋升
- 县长: 宋全星 (Song Quanxing) — appointed ~2022, from 阳信县委副书记晋升

Confidence notes:
  All web search tools (Exa, Baidu, Jina Reader, Google, Bing, DuckDuckGo) were
  rate-limited, blocked, or timed out during research. Government website
  www.yangxin.gov.cn was unreachable (timeout).

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

SLUG = "阳信县"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-26"
TODAY = "20260726"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 刘荩一 — 县委书记（原县长晋升）
    {
        "id": 1,
        "name": "刘荩一",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共阳信县委书记",
        "current_org": "中共阳信县委员会",
        "source": "推断（基于知识库）",
    },
    # 2. 宋全星 — 县长
    {
        "id": 2,
        "name": "宋全星",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "阳信县人民政府县长",
        "current_org": "阳信县人民政府",
        "source": "推断（基于知识库）",
    },
    # 3. 县委副书记（专职）
    {
        "id": 3,
        "name": "待查_县委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "阳信县委副书记（专职）",
        "current_org": "中共阳信县委员会",
        "source": "待查",
    },
    # 4. 县委常委、副县长（常务）
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
        "current_post": "阳信县委常委、副县长（常务）",
        "current_org": "阳信县人民政府",
        "source": "待查",
    },
    # 5. 县委常委、组织部部长
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
        "current_post": "阳信县委常委、组织部部长",
        "current_org": "中共阳信县委员会组织部",
        "source": "待查",
    },
    # 6. 县委常委、县纪委书记、县监委主任
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
        "current_post": "阳信县委常委、县纪委书记、县监委主任",
        "current_org": "中共阳信县纪律检查委员会",
        "source": "待查",
    },
    # 7. 县委常委、宣传部部长
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
        "current_post": "阳信县委常委、宣传部部长",
        "current_org": "中共阳信县委员会宣传部",
        "source": "待查",
    },
    # 8. 县委常委、政法委书记
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
        "current_post": "阳信县委常委、政法委书记",
        "current_org": "中共阳信县委员会政法委员会",
        "source": "待查",
    },
    # 9. 县委常委、统战部部长
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
        "current_post": "阳信县委常委、统战部部长",
        "current_org": "中共阳信县委员会统战部",
        "source": "待查",
    },
    # 10. 县委常委、县委办公室主任
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
        "current_post": "阳信县委常委、县委办公室主任",
        "current_org": "中共阳信县委员会办公室",
        "source": "待查",
    },
    # 11. 前任县委书记: 栾兴刚 (约2016-2021)
    {
        "id": 11,
        "name": "栾兴刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原阳信县委书记",
        "current_org": "原中共阳信县委员会",
        "source": "推断（基于知识库）",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共阳信县委员会", "type": "党委", "level": "县处级", "parent": "中共滨州市委", "location": "滨州市阳信县"},
    {"id": 2, "name": "阳信县人民政府", "type": "政府", "level": "县处级", "parent": "滨州市人民政府", "location": "滨州市阳信县"},
    {"id": 3, "name": "中共阳信县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共阳信县委员会", "location": "滨州市阳信县"},
    {"id": 4, "name": "中共阳信县委员会组织部", "type": "党委", "level": "县处级", "parent": "中共阳信县委员会", "location": "滨州市阳信县"},
    {"id": 5, "name": "中共阳信县委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共阳信县委员会", "location": "滨州市阳信县"},
    {"id": 6, "name": "中共阳信县委员会统战部", "type": "党委", "level": "县处级", "parent": "中共阳信县委员会", "location": "滨州市阳信县"},
    {"id": 7, "name": "中共阳信县委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共阳信县委员会", "location": "滨州市阳信县"},
    {"id": 8, "name": "中共阳信县委员会办公室", "type": "党委", "level": "县处级", "parent": "中共阳信县委员会", "location": "滨州市阳信县"},
    {"id": 9, "name": "阳信县人大常委会", "type": "人大", "level": "县处级", "parent": "滨州市人大常委会", "location": "滨州市阳信县"},
    {"id": 10, "name": "阳信县政协", "type": "政协", "level": "县处级", "parent": "滨州市政协", "location": "滨州市阳信县"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS (person_id, org_id, title, start, end, rank, note)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 刘荩一 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "中共阳信县委书记", "start": "2021-2022", "end": "present", "rank": "县处级", "note": "从阳信县县长转任县委书记（推测）"},
    {"person_id": 1, "org_id": 2, "title": "阳信县人民政府县长（前任职务）", "start": "", "end": "2021-2022", "rank": "县处级", "note": "后转任县委书记"},
    # 宋全星 — 县长
    {"person_id": 2, "org_id": 2, "title": "阳信县人民政府县长", "start": "2022", "end": "present", "rank": "县处级", "note": "接替刘荩一任县长（推测）"},
    {"person_id": 2, "org_id": 1, "title": "中共阳信县委副书记（前任职务）", "start": "", "end": "2022", "rank": "县处级", "note": "后晋升县长"},
    # 待查_县委副书记
    {"person_id": 3, "org_id": 1, "title": "阳信县委副书记（专职）", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_常务副县长
    {"person_id": 4, "org_id": 2, "title": "阳信县委常委、副县长（常务）", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_组织部长
    {"person_id": 5, "org_id": 4, "title": "阳信县委常委、组织部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_纪委书记
    {"person_id": 6, "org_id": 3, "title": "阳信县委常委、县纪委书记、县监委主任", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_宣传部长
    {"person_id": 7, "org_id": 5, "title": "阳信县委常委、宣传部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_政法委书记
    {"person_id": 8, "org_id": 7, "title": "阳信县委常委、政法委书记", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_统战部长
    {"person_id": 9, "org_id": 6, "title": "阳信县委常委、统战部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_县委办主任
    {"person_id": 10, "org_id": 8, "title": "阳信县委常委、县委办公室主任", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 栾兴刚 — 前任县委书记
    {"person_id": 11, "org_id": 1, "title": "中共阳信县委书记（前任）", "start": "2016", "end": "2021-2022", "rank": "县处级", "note": "栾兴刚，刘荩一接任"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 刘荩一 ↔ 宋全星 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "刘荩一任县委书记、宋全星任县长，党政搭档", "overlap_org": "阳信县", "overlap_period": "2022-至今", "confidence": "plausible"},
    # 刘荩一 → 栾兴刚 (前任书记-现任书记)
    {"person_a": 1, "person_b": 11, "type": "predecessor_successor", "context": "刘荩一接替栾兴刚任阳信县委书记", "overlap_org": "中共阳信县委员会", "overlap_period": "2021-2022", "confidence": "plausible"},
    # 刘荩一 → 自己（前任县长-现任书记，县内晋升）
    {"person_a": 1, "person_b": 1, "type": "promotion_chain", "context": "刘荩一从阳信县县长晋升为县委书记", "overlap_org": "阳信县", "overlap_period": "2021-2022", "confidence": "plausible"},
    # 刘荩一 ↔ 宋全星 (前后任县长)
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "刘荩一任县长后转任县委书记，宋全星接任县长", "overlap_org": "阳信县人民政府", "overlap_period": "2022", "confidence": "plausible"},
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
        if other_id == pid:
            continue  # Skip self-references
        other = next((p for p in persons if p["id"] == other_id and p["id"] != pid), None)
        if other:
            rel_entries.append({
                "person": other["name"],
                "person_id": f"yangxin_{other['name']}",
                "relationship_type": r["type"],
                "strength": "medium" if r.get("confidence") == "plausible" else "weak",
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
            "city": "滨州市",
            "region": "阳信县",
            "job": person["current_post"],
            "task_id": "shandong_阳信县",
            "time_focus": "2016-2026",
        },
        "identity": {
            "person_id": f"yangxin_{person['name']}",
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
            "geographic_pattern": ["滨州市"],
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
            {"id": "S001", "title": "综合知识库", "url": "", "publisher": "综合", "published_at": "", "accessed_at": AS_OF, "source_type": "inferred", "reliability": "low", "notes": "所有搜索工具均不可用，信息来自预训练知识"},
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "所有县领导的完整履历均未查证；县委书记刘荩一、县长宋全星的基本信息（出生年份、籍贯、教育背景）全部未知。全部7名县委常委待查。前任县委书记栾兴刚的去向待查。",
        },
        "open_questions": [
            {"priority": "critical", "question": "当前县委书记刘荩一的完整履历（含出生信息、教育背景、早期任职、晋升路径）", "why_it_matters": "确定政治谱系和可能的关联网络", "suggested_queries": ["刘荩一 简历 阳信县", "刘荩一 百度百科", "刘荩一 滨州"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "当前县长宋全星的完整履历", "why_it_matters": "确定其晋升路径和与刘荩一的关系", "suggested_queries": ["宋全星 简历 阳信县", "宋全星 任前公示", "宋全星 滨州"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "阳信县委领导班子全体成员名单（县委副书记、常务副县长、组织部长、纪委书记、宣传部长、政法委书记、统战部长、县委办主任）", "why_it_matters": "完成全县领导班子全名单", "suggested_queries": ["阳信县 领导分工", "阳信县 领导班子 2025", "阳信县 领导之窗"], "last_attempted": AS_OF},
            {"priority": "high", "question": "前任县委书记栾兴刚的调任去向", "why_it_matters": "追踪滨州干部交流模式", "suggested_queries": ["栾兴刚 调任", "栾兴刚 滨州 现任"], "last_attempted": AS_OF},
            {"priority": "high", "question": "阳信县党政领导班子的官方确认（通过yangxin.gov.cn领导之窗页面）", "why_it_matters": "确保调研准确性", "suggested_queries": ["site:yangxin.gov.cn 领导分工", "site:yangxin.gov.cn 阳信县领导"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "刘荩一之前的阳信县县长是谁？刘荩一何时开始担任县长？", "why_it_matters": "完成县长更替时间线", "suggested_queries": ["阳信县 县长 历任", "刘荩一 阳信县 县长 任职"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "栾兴刚之前的阳信县委书记是谁？", "why_it_matters": "完成县委书记更替时间线", "suggested_queries": ["阳信县 县委书记 历任"], "last_attempted": AS_OF},
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
        filename = f"{TODAY}-山东省-滨州市-{job_slug}-{p['name']}.json"
        filepath = PERSONS_DIR / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  JSON: {filename}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"  阳信县 领导班子工作关系网络")
    print(f"  等级: 县")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 知识库（搜索受限，需进一步验证）")
    print(f"{'='*60}")

    # Deduplicate person list for person IDs 11 (栾兴刚) and 13 (栾兴刚 去向)
    # Only keep position 11 as the core person, skip 13 as it's the same person
    # Actually the positions table only references person 11

    run_build(
        slug=SLUG,
        persons=persons,  # No duplicates
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print("\n--- Writing person JSONs ---")
    os.makedirs(PERSONS_DIR, exist_ok=True)
    write_person_jsons()

    print(f"\n✅ 阳信县数据构建完成。")
    print(f"   DB:  {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
    print(f"   JSONs: {PERSONS_DIR}/")
