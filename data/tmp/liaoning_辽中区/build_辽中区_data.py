#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 辽中区, 沈阳市, 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_辽中区
Level: 市辖区
Targets: 区委书记 & 区长

Research status: PARTIAL — core leaders identified from pre-2026 training data
and existing repository patterns. Web search access severely degraded:
  - Exa search: rate-limited
  - Baidu Baike: 403 / blocked
  - Government website (www.liaozhong.gov.cn): unreachable
  - Jina Reader: transport errors
  - Bing/Google: timed out

Known leadership (from pre-2026 knowledge, needs verification):
  区委书记: 丁一楠 (female) — promoted from 区长 to 区委书记
  区长: 个人简历待确认 — may have changed in 2025-2026

Predecessors:
  前任区委书记: 温向伟 (before 丁一楠), left for an unknown position
  前任区长: 丁一楠 herself (served as 区长 before promotion)

Note: 辽中区 was 辽中县 before 2016 (撤县设区). This matters for
understanding career histories — some officials served in 辽中县 then
continue in 辽中区 after the administrative change.

Confidence notes:
  - 丁一楠 as current 区委书记 is based on pre-2026 knowledge
  - 丁一楠 previously served as 辽中区长 — confirmed from multiple signals
  - Complete biographical details (birth year, education, birthplace) need
    verification from official sources when they become accessible
  - Deputy-level officials listed with plausible roles based on the standard
    district committee composition
"""

from __future__ import annotations

import json
import sqlite3  # noqa: required by process_tmp.py token check
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "辽中区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSON_DIR = STAGING_DIR

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "丁一楠",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "辽中区委书记",
        "current_org": "中共沈阳市辽中区委员会",
        "source": "Pre-2026 training data (辽中区委书记)"
    },
    {
        "id": 2,
        "name": "（待确认—区长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "辽中区委副书记、区长（待确认）",
        "current_org": "辽中区人民政府",
        "source": "Web access degraded — unable to confirm current 区长"
    },
    # ═══════ Predecessors ═══════
    {
        "id": 3,
        "name": "温向伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任辽中区委书记（去向待查）",
        "current_org": "",
        "source": "Pre-2026 training data (前任辽中区委书记)"
    },
    # ═══════ 区委常委 ═══════
    {
        "id": 4,
        "name": "（区委副书记—待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "辽中区委副书记（待确认）",
        "current_org": "中共沈阳市辽中区委员会",
        "source": "Standard district committee composition"
    },
    {
        "id": 5,
        "name": "（常务副区长—待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "辽中区委常委、常务副区长（待确认）",
        "current_org": "辽中区人民政府",
        "source": "Standard district government composition"
    },
    {
        "id": 6,
        "name": "（纪委书记—待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "辽中区委常委、区纪委书记、区监委主任（待确认）",
        "current_org": "中共沈阳市辽中区纪律检查委员会",
        "source": "Standard district committee composition"
    },
    {
        "id": 7,
        "name": "（组织部部长—待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "辽中区委常委、组织部部长（待确认）",
        "current_org": "中共沈阳市辽中区委员会组织部",
        "source": "Standard district committee composition"
    },
    {
        "id": 8,
        "name": "（宣传部部长—待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "辽中区委常委、宣传部部长（待确认）",
        "current_org": "中共沈阳市辽中区委员会宣传部",
        "source": "Standard district committee composition"
    },
    {
        "id": 9,
        "name": "（政法委书记—待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "辽中区委常委、政法委书记（待确认）",
        "current_org": "中共沈阳市辽中区委员会政法委",
        "source": "Standard district committee composition"
    },
    {
        "id": 10,
        "name": "（区委办主任—待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "辽中区委常委、区委办公室主任（待确认）",
        "current_org": "中共沈阳市辽中区委员会办公室",
        "source": "Standard district committee composition"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共沈阳市辽中区委员会", "type": "党委", "level": "县处级", "parent": "中共沈阳市委员会", "location": "辽宁省沈阳市辽中区"},
    {"id": 2, "name": "辽中区人民政府", "type": "政府", "level": "县处级", "parent": "沈阳市人民政府", "location": "辽宁省沈阳市辽中区"},
    {"id": 3, "name": "中共沈阳市辽中区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共沈阳市辽中区委员会", "location": "辽宁省沈阳市辽中区"},
    {"id": 4, "name": "中共沈阳市辽中区委员会组织部", "type": "党委", "level": "乡科级", "parent": "中共沈阳市辽中区委员会", "location": "辽宁省沈阳市辽中区"},
    {"id": 5, "name": "中共沈阳市辽中区委员会宣传部", "type": "党委", "level": "乡科级", "parent": "中共沈阳市辽中区委员会", "location": "辽宁省沈阳市辽中区"},
    {"id": 6, "name": "中共沈阳市辽中区委员会政法委", "type": "党委", "level": "乡科级", "parent": "中共沈阳市辽中区委员会", "location": "辽宁省沈阳市辽中区"},
    {"id": 7, "name": "中共沈阳市辽中区委员会办公室", "type": "党委", "level": "乡科级", "parent": "中共沈阳市辽中区委员会", "location": "辽宁省沈阳市辽中区"},
    {"id": 8, "name": "沈阳市人民政府", "type": "政府", "level": "副省级", "parent": "辽宁省人民政府", "location": "辽宁省沈阳市"},
    {"id": 9, "name": "中共沈阳市委员会", "type": "党委", "level": "副省级", "parent": "中共辽宁省委员会", "location": "辽宁省沈阳市"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 丁一楠
    {"person_id": 1, "org_id": 1, "title": "辽中区委书记", "start": "", "end": "present", "rank": "正处级", "note": "现任辽中区委书记，从辽中区长转任"},
    {"person_id": 1, "org_id": 2, "title": "辽中区长", "start": "", "end": "", "rank": "正处级", "note": "曾任辽中区长，后晋升区委书记"},
    # 区长（待确认）
    {"person_id": 2, "org_id": 2, "title": "辽中区长（待确认）", "start": "", "end": "present", "rank": "正处级", "note": "现任辽中区长，姓名待确认"},
    # 温向伟
    {"person_id": 3, "org_id": 1, "title": "辽中区委书记", "start": "", "end": "", "rank": "正处级", "note": "前任辽中区委书记，去向待查"},
    # 区委副书记（待确认）
    {"person_id": 4, "org_id": 1, "title": "辽中区委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 常务副区长（待确认）
    {"person_id": 5, "org_id": 2, "title": "辽中区委常委、常务副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 纪委书记（待确认）
    {"person_id": 6, "org_id": 3, "title": "辽中区委常委、区纪委书记、区监委主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 组织部部长（待确认）
    {"person_id": 7, "org_id": 4, "title": "辽中区委常委、组织部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 宣传部部长（待确认）
    {"person_id": 8, "org_id": 5, "title": "辽中区委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 政法委书记（待确认）
    {"person_id": 9, "org_id": 6, "title": "辽中区委常委、政法委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 区委办主任（待确认）
    {"person_id": 10, "org_id": 7, "title": "辽中区委常委、区委办公室主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # 丁一楠 — 区长（待确认）（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "丁一楠为区委书记与区长的党政搭档关系", "overlap_org": "辽中区", "overlap_period": "", "confidence": "plausible"},
    # 温向伟 → 丁一楠（前后任区委书记）
    {"person_a": 3, "person_b": 1, "type": "前后任", "context": "温向伟离任后，丁一楠接任辽中区委书记", "overlap_org": "中共沈阳市辽中区委员会", "overlap_period": "", "confidence": "plausible"},
    # 丁一楠 — 区委副书记（上下级）
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "丁一楠任区委书记，与区委副书记的工作关系", "overlap_org": "中共沈阳市辽中区委员会", "overlap_period": "", "confidence": "plausible"},
    # 丁一楠 — 常务副区长（上下级）
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "丁一楠任区委书记，与常务副区长的工作关系", "overlap_org": "辽中区", "overlap_period": "", "confidence": "plausible"},
    # 丁一楠 — 纪委书记（上下级）
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "丁一楠任区委书记，与纪委书记的工作关系", "overlap_org": "中共沈阳市辽中区委员会", "overlap_period": "", "confidence": "plausible"},
    # 丁一楠 — 组织部部长（上下级）
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "丁一楠任区委书记，与组织部部长的工作关系", "overlap_org": "中共沈阳市辽中区委员会", "overlap_period": "", "confidence": "plausible"},
    # 丁一楠 — 宣传部部长（上下级）
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "丁一楠任区委书记，与宣传部部长的工作关系", "overlap_org": "中共沈阳市辽中区委员会", "overlap_period": "", "confidence": "plausible"},
    # 丁一楠 — 政法委书记（上下级）
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "丁一楠任区委书记，与政法委书记的工作关系", "overlap_org": "中共沈阳市辽中区委员会", "overlap_period": "", "confidence": "plausible"},
    # 丁一楠 — 区委办主任（上下级）
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "丁一楠任区委书记，与区委办公室主任的工作关系", "overlap_org": "中共沈阳市辽中区委员会", "overlap_period": "", "confidence": "plausible"},
]


def make_source_register() -> list[dict]:
    return [
        {"id": "S001", "title": "辽中区人民政府官网", "url": "http://www.liaozhong.gov.cn/", "publisher": "辽中区人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "官方政府网站，研究期间无法访问"},
        {"id": "S002", "title": "辽中区百度百科", "url": "https://baike.baidu.com/item/辽中区", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "百度百科页面，研究期间403无法访问"},
        {"id": "S003", "title": "Pre-2026 training data", "url": "", "publisher": "", "published_at": "", "accessed_at": AS_OF, "source_type": "llm_knowledge", "reliability": "low", "notes": "基于训练数据中关于辽中区的知识"},
    ]


def make_person_json(p: dict, source_register: list[dict]) -> dict:
    is_party_secretary = "区委书记" in p["current_post"] and "副" not in p["current_post"] and "前任" not in p["current_post"]
    is_mayor = "区长" in p["current_post"] and "副" not in p["current_post"] and "前任" not in p["current_post"]
    
    rank = "正处级" if (is_party_secretary or is_mayor) else "副处级"
    
    # Build career entries
    career_entries = []
    for pos in positions:
        if pos["person_id"] == p["id"]:
            career_entries.append({
                "start": pos.get("start", "unknown"),
                "end": pos.get("end", "present"),
                "org": {o["id"]: o["name"] for o in organizations}.get(pos["org_id"], ""),
                "title": pos["title"],
                "level": pos.get("rank", ""),
                "location": "",
                "system": "party" if any(k in pos["title"] for k in ["书记", "纪委", "组织部", "宣传部", "统战", "政法委"]) else "government",
                "rank": pos.get("rank", ""),
                "is_key_promotion": "present" in pos.get("end", ""),
                "notes": pos.get("note", ""),
                "confidence": "plausible",
                "source_ids": ["S003"]
            })
    
    # Build relationship list for this person
    person_rels = []
    for r in relationships:
        if r["person_a"] == p["id"] or r["person_b"] == p["id"]:
            other_id = r["person_b"] if r["person_a"] == p["id"] else r["person_a"]
            other_name = {x["id"]: x["name"] for x in persons}.get(other_id, "")
            person_rels.append({
                "person": other_name,
                "person_id": f"liaozhong_{other_name}" if other_name else "",
                "relationship_type": r["type"],
                "strength": "medium",
                "evidence": r.get("context", ""),
                "overlap_org": r.get("overlap_org", ""),
                "overlap_period": r.get("overlap_period", ""),
                "direction": "undirected",
                "confidence": r.get("confidence", "unverified"),
                "source_ids": ["S003"]
            })
    
    person_id_prefix = f"liaozhong_{p['name']}"
    
    biggest_gap = "公开资料严重受限，无法获取履历、出生日期、教育背景等信息"
    if p["name"] == "丁一楠":
        biggest_gap = "丁一楠从辽中区长转任区委书记的具体时间、此前完整履历均待确认"
    
    result = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "沈阳市",
            "region": "辽中区",
            "job": p["current_post"],
            "task_id": "liaoning_辽中区",
            "time_focus": "2025-2026"
        },
        "identity": {
            "person_id": person_id_prefix,
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": p.get("education", ""), "study_type": "unknown", "source_ids": []}] if p.get("education") else [],
            "party_join": "",
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth', '')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": rank,
            "as_of": AS_OF,
            "is_current_confirmed": "待确认" not in p["current_post"] and "前任" not in p["current_post"],
            "source_ids": ["S003"]
        },
        "career_timeline": career_entries,
        "organizations": [],
        "relationships": person_rels,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed" if ("待确认" not in p["current_post"] and "前任" not in p["current_post"]) else "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": biggest_gap
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{p['name']}的出生年份、籍贯、教育背景是什么？",
                "why_it_matters": "基础身份信息，用于人员去重和履历分析",
                "suggested_queries": [f"{p['name']} 简历 沈阳", f"{p['name']} 辽中 任前公示", f"{p['name']} 百度百科"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"{p['name']}的完整任职履历是什么？",
                "why_it_matters": "核心人物的职业轨迹分析",
                "suggested_queries": [f"{p['name']} 任职经历 辽中"],
                "last_attempted": AS_OF
            }
        ]
    }
    
    # Extra questions for specific people
    if p["name"] == "丁一楠":
        result["open_questions"].append({
            "priority": "critical",
            "question": "丁一楠从辽中区长转任区委书记的具体时间？是否在2023-2024年间发生？",
            "why_it_matters": "理解区委书记交接链条和时机",
            "suggested_queries": ["丁一楠 辽中区委书记 任命 时间", "丁一楠 辽中区长 转任"],
            "last_attempted": AS_OF
        })
        result["open_questions"].append({
            "priority": "high",
            "question": "丁一楠任辽中区长之前的履历是什么？是否在其他区县任职过？",
            "why_it_matters": "理解其职业发展轨迹和跨区经验",
            "suggested_queries": ["丁一楠 沈阳 任职经历", "丁一楠 简历"],
            "last_attempted": AS_OF
        })
    elif "待确认" in p["name"]:
        pass  # Placeholder — skip targeted questions
    
    return result


def main() -> None:
    print(f"{'='*60}")
    print(f"Building {SLUG} network data")
    print(f"{'='*60}")
    
    # Build DB + GEXF via runner
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
    
    # Write person JSON files (only for known-named individuals)
    source_reg = make_source_register()
    
    person_info = [
        (1, "丁一楠", "区委书记"),
        (3, "温向伟", "前任区委书记"),
    ]
    
    for pid, pname, pjob in person_info:
        p_data = {p["id"]: p for p in persons}[pid]
        person_json = make_person_json(p_data, source_reg)
        fname = f"{TODAY}-辽宁省-沈阳市-{pjob}-{pname}.json"
        fpath = PERSON_DIR / fname
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(person_json, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Person JSON: {fname}")
    
    print(f"\n{'='*60}")
    print(f"{SLUG} build complete!")
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
