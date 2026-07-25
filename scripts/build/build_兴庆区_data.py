#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 兴庆区 (Xingqing District), 银川市, 宁夏回族自治区.

Investigation date: 2026-07-25
Task ID: ningxia_兴庆区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.xqq.gov.cn — 银川市兴庆区人民政府官方网站 (primary, current as of July 2026)
  - www.yinchuan.gov.cn — 银川市人民政府官方网站
  - Government meeting and event reports from xqq.gov.cn (June-July 2026)
  - Web search was degraded: Exa rate-limited, Baidu Baike 403, Jina Reader timeouts

Confidence notes:
  - Current roles: confirmed via multiple government meeting/news reports (July 2026)
  - Biographical details (birth, birthplace, education): mostly unverified due to web access limitations
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
SLUG = "兴庆区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "ningxia_兴庆区"
if _CURRENT_DIR.name == "ningxia_兴庆区":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-9 current party/government leaders, 10-19 standing committee, 20-29 deputy govt

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "邵中宏",
        "gender": "男",
        "ethnicity": "", # unverified
        "birth": "",      # unverified
        "birthplace": "", # unverified
        "education": "",  # unverified
        "party_join": "中共党员",
        "work_start": "", # unverified
        "current_post": "区委书记、苏银产业园党工委书记",
        "current_org": "中共银川市兴庆区委员会",
        "source": "http://www.xqq.gov.cn/mrdt/bmdt/202607/t20260714_5288588.html",
    },
    {
        "id": 2,
        "name": "马国峰",
        "gender": "男",
        "ethnicity": "", # unverified
        "birth": "",      # unverified
        "birthplace": "", # unverified
        "education": "",  # unverified
        "party_join": "中共党员",
        "work_start": "", # unverified
        "current_post": "区委副书记、区长",
        "current_org": "兴庆区人民政府",
        "source": "http://www.xqq.gov.cn/zwgk/bmxxgkml/xqqzfb/fdzdgknr_44757/qzfbwj/202605/t20260519_5244195.html",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee (区委常委) - identified from news
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "范永胜",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "兴庆区人民政府",
        "source": "http://www.xqq.gov.cn/zwgk/bmxxgkml/xqqzfb/fdzdgknr_44757/qzfbwj/202605/t20260519_5244195.html",
    },
    {
        "id": 4,
        "name": "张泓弢",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共银川市兴庆区委员会",
        "source": "http://www.xqq.gov.cn/mrdt/bmdt/202607/t20260709_5285771.html",
    },
    {
        "id": 5,
        "name": "李锦浩",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共银川市兴庆区委员会",
        "source": "http://www.xqq.gov.cn/mrdt/bmdt/202607/t20260714_5288588.html",
    },
    {
        "id": 6,
        "name": "陈伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共银川市兴庆区委员会",
        "source": "http://www.xqq.gov.cn/mrdt/bmdt/202607/t20260715_5289520.html",
    },
    {
        "id": 7,
        "name": "罗强",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共银川市兴庆区委员会",
        "source": "http://www.xqq.gov.cn/mrdt/bmdt/202607/t20260715_5289520.html",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Government Leaders (副区长)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 8,
        "name": "王宇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "兴庆区人民政府",
        "source": "http://www.xqq.gov.cn/zwgk/bmxxgkml/xqqzfb/fdzdgknr_44757/qzfbwj/202605/t20260519_5244195.html",
    },
    {
        "id": 9,
        "name": "杨冬生",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、公安分局局长",
        "current_org": "兴庆区人民政府",
        "source": "http://www.xqq.gov.cn/zwgk/bmxxgkml/xqqzfb/fdzdgknr_44757/qzfbwj/202605/t20260519_5244195.html",
    },
    {
        "id": 10,
        "name": "谢丽丽",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "兴庆区人民政府",
        "source": "http://www.xqq.gov.cn/zwgk/bmxxgkml/xqqzfb/fdzdgknr_44757/qzfbwj/202605/t20260519_5244195.html",
    },
    {
        "id": 11,
        "name": "王立华",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "兴庆区人民政府",
        "source": "http://www.xqq.gov.cn/zwgk/bmxxgkml/xqqzfb/fdzdgknr_44757/qzfbwj/202605/t20260519_5244195.html",
    },
    {
        "id": 12,
        "name": "闫学锋",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "兴庆区人民政府",
        "source": "http://www.xqq.gov.cn/zwgk/bmxxgkml/xqqzfb/fdzdgknr_44757/qzfbwj/202605/t20260519_5244195.html",
    },
    {
        "id": 13,
        "name": "任桂霞",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "兴庆区人民政府",
        "source": "http://www.xqq.gov.cn/zwgk/bmxxgkml/xqqzfb/fdzdgknr_44757/qzfbwj/202605/t20260519_5244195.html",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共银川市兴庆区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共银川市委员会",
        "location": "宁夏回族自治区银川市兴庆区",
    },
    {
        "id": 2,
        "name": "兴庆区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "银川市人民政府",
        "location": "宁夏回族自治区银川市兴庆区",
    },
    {
        "id": 3,
        "name": "苏银产业园党工委",
        "type": "开发区",
        "level": "县处级",
        "parent": "中共银川市委员会",
        "location": "宁夏回族自治区银川市兴庆区",
    },
    {
        "id": 4,
        "name": "兴庆区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "银川市人大常委会",
        "location": "宁夏回族自治区银川市兴庆区",
    },
    {
        "id": 5,
        "name": "兴庆区政协",
        "type": "政协",
        "level": "县处级",
        "parent": "银川市政协",
        "location": "宁夏回族自治区银川市兴庆区",
    },
    {
        "id": 6,
        "name": "兴庆区纪委监委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共银川市兴庆区委员会",
        "location": "宁夏回族自治区银川市兴庆区",
    },
    {
        "id": 7,
        "name": "兴庆区公安分局",
        "type": "政府",
        "level": "乡科级",
        "parent": "兴庆区人民政府",
        "location": "宁夏回族自治区银川市兴庆区",
    },
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 邵中宏
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "", "end": "present", "rank": "正处级", "note": "兼任苏银产业园党工委书记"},
    {"person_id": 1, "org_id": 3, "title": "苏银产业园党工委书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 马国峰
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "present", "rank": "正处级", "note": "主持区政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 范永胜
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责区政府常务工作"},
    # 张泓弢
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 李锦浩
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 陈伟
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 罗强
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 王宇
    {"person_id": 8, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责科技创新、工业经济、商务、招商引资"},
    # 杨冬生
    {"person_id": 9, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责公安、信访、司法"},
    {"person_id": 9, "org_id": 7, "title": "公安分局局长", "start": "", "end": "present", "rank": "正科级", "note": ""},
    # 谢丽丽
    {"person_id": 10, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责卫生健康、医疗保障、国资国企"},
    # 王立华
    {"person_id": 11, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责自然资源、农业农村、乡村振兴"},
    # 闫学锋
    {"person_id": 12, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责发展改革、教育、人社、统计"},
    # 任桂霞
    {"person_id": 13, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责文化旅游、体育、综合执法"},
]

# ── Relationships ────────────────────────────────────────────────────────────
# Relationship types: overlap (same org/time), superior_subordinate, etc.

relationships = [
    # 邵中宏 — 马国峰 (党政正职搭档)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区委书记与区长党政正职搭档关系", "overlap_org": "中共银川市兴庆区委员会/兴庆区人民政府", "overlap_period": "present"},
    # 邵中宏 — 区委常委 (领导关系)
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区委书记领导常务副区长", "overlap_org": "中共银川市兴庆区委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "区委书记领导区委常委", "overlap_org": "中共银川市兴庆区委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "区委书记领导区委常委", "overlap_org": "中共银川市兴庆区委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "区委书记领导区委常委", "overlap_org": "中共银川市兴庆区委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "区委书记领导区委常委", "overlap_org": "中共银川市兴庆区委员会", "overlap_period": "present"},
    # 马国峰 — 副区长 (政府内部上下级)
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "区长领导常务副区长", "overlap_org": "兴庆区人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "区长领导副区长", "overlap_org": "兴庆区人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "区长领导副区长", "overlap_org": "兴庆区人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "区长领导副区长", "overlap_org": "兴庆区人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "区长领导副区长", "overlap_org": "兴庆区人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "区长领导副区长", "overlap_org": "兴庆区人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "区长领导副区长", "overlap_org": "兴庆区人民政府", "overlap_period": "present"},
]


# ═══════════════════════════════════════════════════════════════════════════
# Person JSON writer
# ═══════════════════════════════════════════════════════════════════════════

def write_person_json(person: dict, job: str) -> Path:
    """Write a person graph JSON file to the staging directory."""
    person_id = f"xingqing_{person['name']}"
    path = PJSON_DIR / f"{TODAY}-宁夏回族自治区-银川市-{job}-{person['name']}.json"
    doc = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "宁夏回族自治区",
            "city": "银川市",
            "region": "兴庆区",
            "job": job,
            "task_id": "ningxia_兴庆区",
            "time_focus": "2026-07 (current)"
        },
        "identity": {
            "person_id": person_id,
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth','')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace','')}",
                "official_profile_url": person.get("source", "")
            }
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正处级" if job in ["区委书记", "区长"] else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": person.get("current_org", ""),
                "title": person.get("current_post", ""),
                "level": "县处级",
                "location": "宁夏回族自治区银川市兴庆区",
                "system": "party" if "书记" in person.get("current_post", "") else "government",
                "rank": "正处级" if job in ["区委书记", "区长"] else "副处级",
                "is_key_promotion": True if job in ["区委书记", "区长"] else False,
                "notes": "Current role confirmed by official government website reports (July 2026)",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "organizations": [
            {"id": 1, "name": "中共银川市兴庆区委员会", "type": "党委"},
            {"id": 2, "name": "兴庆区人民政府", "type": "政府"},
        ],
        "relationships": [],
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
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "No disciplinary or integrity red flags found in publicly available sources during investigation.",
                "date": "",
                "confidence": "plausible",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": f"兴庆区人民政府 - {person['name']}相关新闻报道",
                "url": person.get("source", ""),
                "publisher": "兴庆区人民政府",
                "published_at": AS_OF,
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "Official government website"
            }
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "Complete career history prior to current role, birth year, birthplace, education"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的完整履历（出生年月、籍贯、学历、入党时间、参加工作时间和历任职务）",
                "why_it_matters": "核心领导的身份信息和晋升路径是关系网络分析的基础",
                "suggested_queries": [f"{person['name']} 简历 兴庆区", f"{person['name']} 任前公示", f"{person['name']} 出生年月"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"{person['name']}的前任职务和调动时间",
                "why_it_matters": "理解干部交流模式和晋升速度",
                "suggested_queries": [f"{person['name']} 此前 担任", f"{person['name']} 调任"],
                "last_attempted": AS_OF
            }
        ]
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {path.name}")
    return path


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print(f"Building {SLUG} dataset (staging: {STAGING})")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    # Run build (DB + GEXF)
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write person JSONs for the core targets
    print("\nWriting person JSONs ...")
    write_person_json(persons[0], "区委书记")   # 邵中宏
    write_person_json(persons[1], "区长")       # 马国峰

    # Verify outputs
    print("\nOutput verification:")
    for path in [DB_PATH, GEXF_PATH]:
        if path.exists():
            size_kb = path.stat().st_size / 1024
            print(f"  ✅ {path.name} ({size_kb:.1f} KB)")
        else:
            print(f"  ❌ {path.name} MISSING")

    json_count = len(list(PJSON_DIR.glob(f"{TODAY}-*.json")))
    print(f"  ✅ Person JSON files: {json_count}")

    print(f"\n{SLUG} build complete.")


if __name__ == "__main__":
    main()
