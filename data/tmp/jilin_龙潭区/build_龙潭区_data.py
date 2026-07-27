#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 龙潭区 (Longtan District), 吉林市, 吉林省.

Investigation date: 2026-07-25
Task ID: jilin_龙潭区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.longtan.gov.cn — 龙潭区人民政府官方网站 (primary, current as of July 2026)
  - www.jlcity.gov.cn — 吉林市人民政府官方网站
  - Confirmed via news articles on longtan.gov.cn (July 2026):
    * 孙璐 — 龙潭区人大常委会主任
    * 郭艳飞 — 龙潭区委常委、政法委书记

Confidence notes:
  - Longtan District government website is active and contains news up to July 2026
  - Government leadership page (区长/副区长) not directly accessible on the site
  - Party leadership (区委书记) not published on the district government domain
  - Web search (Exa, Jina Reader, Baidu) all unavailable during investigation
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
SLUG = "龙潭区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_龙潭区"
if _CURRENT_DIR.name == "jilin_龙潭区":
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
# IDs: 1区委书记, 2区长, 3人大主任, 4政法委书记, 5-8 deputy leaders
# Names for 区委书记 and 区长 are not confirmed (web search unavailable)

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "待查(龙潭区委书记)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共吉林市龙潭区委员会",
        "source": "http://www.longtan.gov.cn/",
        "confidence": "unverified",
        "notes": "核心目标人物之一。龙潭区网站未公布区委领导信息。需从吉林市委组织部任前公示或新闻报道中查找。"
    },
    {
        "id": 2,
        "name": "待查(龙潭区长)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区长",
        "current_org": "龙潭区人民政府",
        "source": "http://www.longtan.gov.cn/",
        "confidence": "unverified",
        "notes": "核心目标人物之一。龙潭区政府领导页面未找到。需通过吉林市委组织部公示或政府网站领导分工页面查找。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Confirmed Leadership (from news articles)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "孙璐",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "龙潭区人民代表大会常务委员会",
        "source": "http://www.longtan.gov.cn/sllt/jrlt/202607/t20260720_1329297.html",
        "confidence": "confirmed",
        "notes": "2026年7月17日率专题视察组对区法院参与综治中心实质解纷情况开展视察。来源：龙潭区政府网站新闻。"
    },
    {
        "id": 4,
        "name": "郭艳飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、政法委书记",
        "current_org": "中共龙潭区委政法委员会",
        "source": "http://www.longtan.gov.cn/sllt/jrlt/202607/t20260720_1329297.html",
        "confidence": "confirmed",
        "notes": "2026年7月17日陪同区人大常委会主任孙璐视察。来源：龙潭区政府网站新闻。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Typical Standing Committee members (推定)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 5,
        "name": "待查(龙潭区委副书记)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共吉林市龙潭区委员会",
        "source": "",  # inferred from organizational structure
        "confidence": "unverified",
        "notes": "按区级组织结构推定设有1-2名区委副书记（通常区长兼任一名）"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共吉林市龙潭区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共吉林市委员会",
        "location": "吉林省吉林市龙潭区"
    },
    {
        "id": 2,
        "name": "龙潭区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "吉林市人民政府",
        "location": "吉林省吉林市龙潭区"
    },
    {
        "id": 3,
        "name": "龙潭区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "吉林市人民代表大会常务委员会",
        "location": "吉林省吉林市龙潭区"
    },
    {
        "id": 4,
        "name": "中共龙潭区委政法委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共吉林市龙潭区委员会",
        "location": "吉林省吉林市龙潭区"
    },
    {
        "id": 5,
        "name": "中共龙潭区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共吉林市龙潭区委员会",
        "location": "吉林省吉林市龙潭区"
    },
    {
        "id": 6,
        "name": "龙潭区监察委员会",
        "type": "政府",
        "level": "县处级",
        "parent": "龙潭区人民政府",
        "location": "吉林省吉林市龙潭区"
    },
    {
        "id": 7,
        "name": "中国人民政治协商会议龙潭区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协吉林市委员会",
        "location": "吉林省吉林市龙潭区"
    },
    {
        "id": 8,
        "name": "中共龙潭区委组织部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共吉林市龙潭区委员会",
        "location": "吉林省吉林市龙潭区"
    },
    {
        "id": 9,
        "name": "中共龙潭区委宣传部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共吉林市龙潭区委员会",
        "location": "吉林省吉林市龙潭区"
    },
    {
        "id": 10,
        "name": "吉林市龙潭区人民政府办公室",
        "type": "政府",
        "level": "乡科级",
        "parent": "龙潭区人民政府",
        "location": "吉林省吉林市龙潭区"
    },
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    # 区委书记 — 推定存在
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},
    # 区长 — 推定存在
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},
    # 孙璐 — 区人大常委会主任
    {"person_id": 3, "org_id": 3, "title": "区人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "截至2026年7月在任"},
    # 郭艳飞 — 区委常委、政法委书记
    {"person_id": 4, "org_id": 4, "title": "区委常委、政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "2026年7月在任"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 区委书记 — 区长 (推定搭档关系)
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "推定：区委书记与区长为党政一把手搭档关系",
        "overlap_org": "龙潭区",
        "overlap_period": "",
        "confidence": "unverified",
        "source": ""
    },
    # 区人大常委会 — 政府 (法定监督关系)
    {
        "person_a": 3,
        "person_b": 2,
        "type": "overlap",
        "context": "推定：区人大常委会主任对区长有法定监督关系",
        "overlap_org": "龙潭区",
        "overlap_period": "",
        "confidence": "unverified",
        "source": "http://www.longtan.gov.cn/sllt/jrlt/202607/t20260720_1329297.html"
    },
    # 政法委书记 — 区委书记 (上下级)
    {
        "person_a": 4,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "推定：政法委书记受区委书记领导，属于区委常委会班子成员",
        "overlap_org": "中共吉林市龙潭区委员会",
        "overlap_period": "",
        "confidence": "unverified",
        "source": ""
    },
]

# ── Build ─────────────────────────────────────────────────────────────────────
def write_person_json(person: dict) -> None:
    """Write a single person JSON file in the staging directory."""
    from datetime import date

    name = person["name"]
    job = person["current_post"]
    # Simplify the filename for unknown persons
    safe_name = name.replace(" ", "_").replace("(", "（").replace(")", "）")
    filename = f"{TODAY}-吉林省-吉林市-{job}-{safe_name}.json"
    filepath = PJSON_DIR / filename

    # Build a minimal person JSON following the schema
    person_json = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "吉林省",
            "city": "吉林市",
            "region": "龙潭区",
            "job": job,
            "task_id": "jilin_龙潭区",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"longtan_{safe_name}",
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
                "name_birth": f"{person['name']}_{person.get('birth', '')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
                "official_profile_url": person.get("source", "")
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": person["confidence"] == "confirmed",
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": person.get("current_org", ""),
                "title": person["current_post"],
                "level": "",
                "location": "吉林省吉林市龙潭区",
                "system": "party" if "委" in person.get("current_post", "") else "government",
                "rank": "",
                "is_key_promotion": False,
                "notes": person.get("notes", ""),
                "confidence": person["confidence"],
                "source_ids": ["S001"]
            }
        ],
        "organizations": [
            {
                "org_name": person.get("current_org", ""),
                "org_type": "政府" if "政府" in person.get("current_org", "") else "党委",
                "role": person["current_post"],
                "period": "",
                "source_ids": ["S001"]
            }
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
                "description": "未发现公开的违纪或负面信息。调查范围：龙潭区政府网站新闻检索。",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "龙潭区人民政府官方网站",
                "url": person.get("source", "http://www.longtan.gov.cn/"),
                "publisher": "龙潭区人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": ""
            }
        ],
        "confidence_summary": {
            "identity": person["confidence"],
            "current_role": person["confidence"],
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": person.get("notes", "完整履历缺失")
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"该人物姓名信息不完整，需通过吉林市委组织部任前公示或新闻报道确认",
                "why_it_matters": "核心目标人物，姓名是最基础的信息",
                "suggested_queries": [
                    f"龙潭区 {person['current_post']}",
                    "吉林市委组织部 任前公示 龙潭区",
                    "吉林市龙潭区 领导分工"
                ],
                "last_attempted": AS_OF
            }
        ]
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(person_json, f, ensure_ascii=False, indent=2)

    print(f"  ✓ Person JSON: {filepath.name}")


def main() -> int:
    print(f"Building {SLUG} network data...")
    print(f"  Staging: {STAGING}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

    # Build DB + GEXF
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write individual person JSONs
    print("  Writing person JSON files...")
    for p in persons:
        write_person_json(p)

    print(f"\n✅ {SLUG} build complete.")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Person JSONs: {len(persons)} files in {PJSON_DIR}")

    # Validation summary
    print(f"\n📊 Summary:")
    print(f"  Persons: {len(persons)} ({sum(1 for p in persons if p['confidence']=='confirmed')} confirmed, "
          f"{sum(1 for p in persons if p['confidence']=='unverified')} unverified)")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
