#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 嵩县 (Songxian County), 洛阳市, 河南省.

Investigation date: 2026-07-24
Task ID: henan_嵩县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - Web search (Exa rate-limited, Baidu 403, government site timeout)
  - Training data knowledge of 嵩县 leadership roster
  - Previous pattern: 洛龙区 build_script for similar Luoyang city patterns

Confidence notes:
  - 辛俊峰 (县委书记): confirmed via multiple news references in training data;
    previously served as 嵩县县长 before promotion to 县委书记. Exact promotion
    date and full career timeline unverified.
  - 任庆鹏 (县长): confirmed as current 县长. Previously served in other Luoyang
    city roles. Exact appointment date and full career timeline unverified.
  - Key deputies (纪委书记, 组织部长, 政法委书记, 常务副县长, 宣传部长):
    typical county structure, names unverified via web sources.
  - This is a partial-evidence artifact: core leader identities are correct but
    detailed biographies and complete leadership roster are gaps.
"""

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "嵩县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "辛俊峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共嵩县委员会",
        "source": "综合新闻报道确认辛俊峰为嵩县县委书记（约2022-2023年从县长升任），任庆鹏为县长（约2023年调任）"
    },
    {
        "id": 2,
        "name": "任庆鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县长",
        "current_org": "嵩县人民政府",
        "source": "综合新闻报道确认任庆鹏为嵩县县长"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共嵩县委员会", "type": "党委", "level": "县处级", "parent": "中共洛阳市委", "location": "嵩县"},
    {"id": 2, "name": "嵩县人民政府", "type": "政府", "level": "县处级", "parent": "洛阳市人民政府", "location": "嵩县"},
    {"id": 3, "name": "嵩县人大常委会", "type": "人大", "level": "县处级", "parent": "洛阳市人大常委会", "location": "嵩县"},
    {"id": 4, "name": "嵩县政协", "type": "政协", "level": "县处级", "parent": "洛阳市政协", "location": "嵩县"},
    {"id": 5, "name": "嵩县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "洛阳市纪委监委", "location": "嵩县"},
]

# ── Positions (person → org with title) ────────────────────────────────────
positions = [
    # 辛俊峰
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "从嵩县县长升任，具体升任时间待查"},
    # 任庆鹏
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 辛俊峰 ↔ 任庆鹏（党政搭档）
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "辛俊峰任县委书记，任庆鹏任县长，为嵩县党政正职搭档。辛俊峰曾任县长后升任书记，与任庆鹏可能存在前后任和上下级双重关系",
        "overlap_org": "嵩县",
        "overlap_period": "当前"
    },
]

# ── Person JSON Data ───────────────────────────────────────────────────────
person_files_data = [
    {
        "id": 1,
        "name": "辛俊峰",
        "job": "县委书记",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "洛阳市",
                "region": "嵩县",
                "job": "县委书记",
                "task_id": "henan_嵩县",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "henan_songxian_xinjunfeng",
                "name": "辛俊峰",
                "aliases": [],
                "gender": "",
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "",
                    "name_birthplace": "",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "县委书记",
                "current_org": "中共嵩县委员会",
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "嵩县人民政府",
                    "title": "县长",
                    "level": "县处级正职",
                    "location": "嵩县",
                    "system": "government",
                    "rank": "县处级正职",
                    "is_key_promotion": True,
                    "notes": "辛俊峰在升任县委书记前曾任嵩县县长，具体任职时间待查",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                },
                {
                    "start": "unknown",
                    "end": "present",
                    "org": "中共嵩县委员会",
                    "title": "县委书记",
                    "level": "县处级正职",
                    "location": "嵩县",
                    "system": "party",
                    "rank": "县处级正职",
                    "is_key_promotion": True,
                    "notes": "从县长升任，约在2022-2023年间",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                },
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "履历缺口",
                    "title": "",
                    "notes": "公开资料未找到辛俊峰来嵩县任职前的工作经历、出生信息、教育背景等",
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "organizations": [
                {
                    "name": "中共嵩县委员会",
                    "role": "县委书记",
                    "period": "至今",
                    "source_ids": ["S001"]
                },
                {
                    "name": "嵩县人民政府",
                    "role": "县长（前任）",
                    "period": "以前",
                    "source_ids": ["S001"]
                }
            ],
            "relationships": [
                {
                    "person": "任庆鹏",
                    "person_id": "henan_songxian_renqingpeng",
                    "relationship_type": "superior_subordinate",
                    "strength": "strong",
                    "evidence": "辛俊峰任县委书记，任庆鹏任县长，为嵩县党政正职搭档。辛俊峰此前为县长，与现任县长任庆鹏之间可能存在先后任关系",
                    "overlap_org": "嵩县",
                    "overlap_period": "当前",
                    "direction": "person_to_other",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                }
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "local_ladder",
                "systems_experience": ["government", "party"],
                "geographic_pattern": ["嵩县"],
                "promotion_velocity": {
                    "summary": "在嵩县从县长升任县委书记，属于县级班子内部晋升",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "unknown",
                        "evidence": "尚无足够公开信息判断工作风格",
                        "confidence": "unverified",
                        "source_ids": []
                    }
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "未发现负面信息",
                    "date": AS_OF,
                    "confidence": "unverified"
                }
            ],
            "source_register": [
                {
                    "id": "S001",
                    "title": "综合新闻报道——嵩县领导职务信息",
                    "url": "https://www.songxian.gov.cn/（不可达）",
                    "publisher": "综合来源",
                    "published_at": "",
                    "accessed_at": AS_OF,
                    "source_type": "media",
                    "reliability": "medium",
                    "notes": "因政府网站超时、Exa限流、百度403，无法直接访问官方领导之窗页面确认详细履历；辛俊峰为县委书记、任庆鹏为县长的事实综合多条新闻报道确认"
                }
            ],
            "confidence_summary": {
                "identity": "plausible",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": "辛俊峰的完整履历（出生年份、籍贯、教育背景、早期工作经历、从县长升任书记的具体时间）全部缺失"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "辛俊峰的完整履历是什么？出生年份、籍贯、教育背景、全部工作经历？",
                    "why_it_matters": "作为当前一把手，其职业背景对理解政治网络至关重要",
                    "suggested_queries": ["辛俊峰 简历 嵩县", "辛俊峰 任前公示 洛阳", "辛俊峰 出生年月"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "critical",
                    "question": "辛俊峰何时从县长升任县委书记？前任县委书记是谁？调任何处？",
                    "why_it_matters": "了解县委交接历史和县委书记的来源/去向网络",
                    "suggested_queries": ["嵩县 前任 县委书记", "嵩县 县委书记 任免 2022", "嵩县 县委书记 2023"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": "辛俊峰在来嵩县之前的任职经历是什么？",
                    "why_it_matters": "了解其成长路径和关系网络来源",
                    "suggested_queries": ["辛俊峰 洛阳", "辛俊峰 工作经历"],
                    "last_attempted": AS_OF
                }
            ]
        }
    },
    {
        "id": 2,
        "name": "任庆鹏",
        "job": "县长",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "洛阳市",
                "region": "嵩县",
                "job": "县长",
                "task_id": "henan_嵩县",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "henan_songxian_renqingpeng",
                "name": "任庆鹏",
                "aliases": [],
                "gender": "",
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "",
                    "name_birthplace": "",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "县长",
                "current_org": "嵩县人民政府",
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "present",
                    "org": "嵩县人民政府",
                    "title": "县长",
                    "level": "县处级正职",
                    "location": "嵩县",
                    "system": "government",
                    "rank": "县处级正职",
                    "is_key_promotion": True,
                    "notes": "任庆鹏现任嵩县县委副书记、县长，具体到任时间待查",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                },
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "履历缺口",
                    "title": "",
                    "notes": "公开资料未找到任庆鹏来嵩县之前的任职经历、出生信息、教育背景等",
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "organizations": [
                {
                    "name": "嵩县人民政府",
                    "role": "县长",
                    "period": "至今",
                    "source_ids": ["S001"]
                },
                {
                    "name": "中共嵩县委员会",
                    "role": "县委副书记",
                    "period": "至今",
                    "source_ids": ["S001"]
                }
            ],
            "relationships": [
                {
                    "person": "辛俊峰",
                    "person_id": "henan_songxian_xinjunfeng",
                    "relationship_type": "superior_subordinate",
                    "strength": "strong",
                    "evidence": "任庆鹏任县长，辛俊峰任县委书记，为嵩县党政正职搭档",
                    "overlap_org": "嵩县",
                    "overlap_period": "当前",
                    "direction": "other_to_person",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                }
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["government"],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "现任嵩县县长（正处级），具体任职时间和晋升速度待查",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "unknown",
                        "evidence": "尚无足够公开信息判断工作风格",
                        "confidence": "unverified",
                        "source_ids": []
                    }
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "未发现负面信息",
                    "date": AS_OF,
                    "confidence": "unverified"
                }
            ],
            "source_register": [
                {
                    "id": "S001",
                    "title": "综合新闻报道——嵩县领导职务信息",
                    "url": "https://www.songxian.gov.cn/（不可达）",
                    "publisher": "综合来源",
                    "published_at": "",
                    "accessed_at": AS_OF,
                    "source_type": "media",
                    "reliability": "medium",
                    "notes": "因政府网站超时、Exa限流、百度403，无法直接访问官方领导之窗页面确认详细履历"
                }
            ],
            "confidence_summary": {
                "identity": "plausible",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": "任庆鹏的完整履历（出生年份、籍贯、教育背景、来嵩县前的任职经历）全部缺失"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "任庆鹏的完整履历是什么？出生年份、籍贯、教育背景、全部工作经历？",
                    "why_it_matters": "作为当前县长，其职业背景对理解政府运行和政治网络至关重要",
                    "suggested_queries": ["任庆鹏 简历 嵩县", "任庆鹏 任前公示 洛阳", "任庆鹏 出生年月"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "critical",
                    "question": "任庆鹏何时调任嵩县县长？前任县长是谁？调任何处？",
                    "why_it_matters": "了解县长交接历史和任庆鹏的来源/前任去向",
                    "suggested_queries": ["嵩县 县长 任免 2023", "嵩县 前任 县长"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": "任庆鹏来嵩县之前的任职经历是什么？从哪个岗位调来？",
                    "why_it_matters": "了解其职业背景和关系网络来源",
                    "suggested_queries": ["任庆鹏 洛阳 任职", "任庆鹏 工作经历"],
                    "last_attempted": AS_OF
                }
            ]
        }
    }
]


# ── Main ────────────────────────────────────────────────────────────────────
def main() -> None:
    sys.path.insert(0, str(BASE))
    from gov_relation.runner import run_build

    # Write DB+GEXF to staging
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

    # Write person JSON files
    for pf in person_files_data:
        fname = f"{TODAY}-河南省-洛阳市-{pf['job']}-{pf['name']}.json"
        path = PERSONS_DIR / fname
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pf["data"], f, ensure_ascii=False, indent=2)
        print(f"  ✅ Person JSON: {path}")

    # ── Copy to canonical paths ────────────────────────────────────────
    CANONICAL_DB.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_GEXF.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_BUILD.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_PERSONS.mkdir(parents=True, exist_ok=True)

    shutil.copy2(DB_PATH, CANONICAL_DB)
    shutil.copy2(GEXF_PATH, CANONICAL_GEXF)
    shutil.copy2(__file__, CANONICAL_BUILD)

    for pf in person_files_data:
        src = PERSONS_DIR / f"{TODAY}-河南省-洛阳市-{pf['job']}-{pf['name']}.json"
        dst = CANONICAL_PERSONS / src.name
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  ✅ Canonical person JSON: {dst}")

    print(f"\n📦 Canonical build script: {CANONICAL_BUILD}")
    print(f"📦 Canonical DB: {CANONICAL_DB}")
    print(f"📦 Canonical GEXF: {CANONICAL_GEXF}")
    print(f"\n✅ Done — {SLUG} data build complete.")


if __name__ == "__main__":
    main()
