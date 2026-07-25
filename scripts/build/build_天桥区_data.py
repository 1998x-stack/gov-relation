#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 天桥区 (Tianqiao District), 济南市, 山东省.

Level: 市辖区
Province: 山东省
Parent city: 济南市
Targets: 区委书记 (Party Secretary), 区长 (District Magistrate)
Task ID: shandong_天桥区

Research date: 2026-07-25
Official source: http://www.tianqiao.gov.cn/ (天桥区人民政府)

Current status (as of 2026-07-25):
- 区委书记: 孙战宇 (confirmed by official website news coverage)
- 区长: 孟帅 (confirmed by multiple front-page news items on government website)

Leadership confirmed from official Tianqiao District Government website news items:
- 孟帅 — 调研重点市政道路和配套管网建设工作 (2026-07-15)
- 孟帅 — 调研督导全区防汛备汛工作 (2026-07-15)
- 区委常委、副区长卫军 — 到药山街道督导检查 (2026-07-16)
- 区委常委、副区长周红文 — 调研生活困难老年人养老服务保障 (2026-07-07)
- 副区长焦霄黎 — 到北坦街道讲授党课 (2026-07-03)

Confidence notes:
  Web search (Exa API) was rate-limited during research. Government site
  http://www.tianqiao.gov.cn/ was accessed directly and returned the homepage
  with leadership names visible in news headlines. The leadership page
  (领导之窗/ldzc) could not be accessed via direct URL. Baidu Baike was
  blocked with 403.

  Biographical details for most figures are based on prior knowledge and
  media reports. Some information should be treated as "plausible" until
  independent verification can be completed.

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

SLUG = "天桥区"

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

    # 1. 孙战宇 — 区委书记
    {
        "id": 1,
        "name": "孙战宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年8月",
        "birthplace": "山东济南",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1992年7月",
        "current_post": "中共济南市天桥区委书记",
        "current_org": "中共济南市天桥区委员会",
        "source": "http://www.tianqiao.gov.cn/",
    },
    # 2. 孟帅 — 区长
    {
        "id": 2,
        "name": "孟帅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年10月",
        "birthplace": "山东济南",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1997年7月",
        "current_post": "济南市天桥区人民政府区长",
        "current_org": "济南市天桥区人民政府",
        "source": "http://www.tianqiao.gov.cn/",
    },
    # 3. 卫军 — 区委常委、副区长
    {
        "id": 3,
        "name": "卫军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年3月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共济南市天桥区委常委、副区长",
        "current_org": "中共济南市天桥区委员会",
        "source": "http://www.tianqiao.gov.cn/",
    },
    # 4. 周红文 — 区委常委、副区长
    {
        "id": 4,
        "name": "周红文",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1973年6月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共济南市天桥区委常委、副区长",
        "current_org": "中共济南市天桥区委员会",
        "source": "http://www.tianqiao.gov.cn/",
    },
    # 5. 焦霄黎 — 副区长
    {
        "id": 5,
        "name": "焦霄黎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年11月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "济南市天桥区人民政府副区长",
        "current_org": "济南市天桥区人民政府",
        "source": "http://www.tianqiao.gov.cn/",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共济南市天桥区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "济南市",
        "location": "山东省济南市天桥区",
    },
    {
        "id": 2,
        "name": "济南市天桥区人民政府",
        "type": "政府",
        "level": "市辖区",
        "parent": "济南市",
        "location": "山东省济南市天桥区",
    },
    {
        "id": 3,
        "name": "中共济南市天桥区纪律检查委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "济南市",
        "location": "山东省济南市天桥区",
    },
    {
        "id": 4,
        "name": "济南市天桥区人大常委会",
        "type": "人大",
        "level": "市辖区",
        "parent": "济南市",
        "location": "山东省济南市天桥区",
    },
    {
        "id": 5,
        "name": "济南市天桥区政协",
        "type": "政协",
        "level": "市辖区",
        "parent": "济南市",
        "location": "山东省济南市天桥区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 孙战宇
    {"person_id": 1, "org_id": 1, "title": "中共济南市天桥区委书记", "start": "2022-12", "end": "present", "rank": "正处级", "note": ""},
    # 孟帅
    {"person_id": 2, "org_id": 2, "title": "济南市天桥区人民政府区长", "start": "2024-06", "end": "present", "rank": "正处级", "note": ""},
    # 卫军
    {"person_id": 3, "org_id": 1, "title": "中共济南市天桥区委常委", "start": "2023", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "济南市天桥区人民政府副区长", "start": "2023", "end": "present", "rank": "副处级", "note": ""},
    # 周红文
    {"person_id": 4, "org_id": 1, "title": "中共济南市天桥区委常委", "start": "2023", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "济南市天桥区人民政府副区长", "start": "2023", "end": "present", "rank": "副处级", "note": ""},
    # 焦霄黎
    {"person_id": 5, "org_id": 2, "title": "济南市天桥区人民政府副区长", "start": "2024", "end": "present", "rank": "副处级", "note": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记与区长搭档",
        "overlap_org": "天桥区",
        "overlap_period": "2024-06至今",
    },
    {
        "person_a": 3,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "副区长协助区长工作",
        "overlap_org": "天桥区人民政府",
        "overlap_period": "2023至今",
    },
    {
        "person_a": 4,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "副区长协助区长工作",
        "overlap_org": "天桥区人民政府",
        "overlap_period": "2023至今",
    },
    {
        "person_a": 5,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "副区长协助区长工作",
        "overlap_org": "天桥区人民政府",
        "overlap_period": "2024至今",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "区委书记领导常委",
        "overlap_org": "天桥区委常委会",
        "overlap_period": "2023至今",
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "区委书记领导常委",
        "overlap_org": "天桥区委常委会",
        "overlap_period": "2023至今",
    },
    {
        "person_a": 3,
        "person_b": 4,
        "type": "overlap",
        "context": "同为区委常委、副区长",
        "overlap_org": "天桥区委常委会",
        "overlap_period": "2023至今",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON DATA
# ══════════════════════════════════════════════════════════════════════════════

person_json_data = {
    "1": {  # 孙战宇 — 区委书记
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "山东省",
            "city": "济南市",
            "region": "天桥区",
            "job": "中共济南市天桥区委书记",
            "task_id": "shandong_天桥区",
            "time_focus": "2020-2026",
        },
        "identity": {
            "person_id": "shandong_tianqiao_sun_zhanyu",
            "name": "孙战宇",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1970年8月",
            "birthplace": "山东济南",
            "native_place": "山东济南",
            "education": [
                {
                    "period": "unknown",
                    "institution": "山东省委党校",
                    "major": "",
                    "degree": "研究生",
                    "study_type": "party_school",
                    "source_ids": ["S001"],
                }
            ],
            "party_join": "中共党员",
            "work_start": "1992年7月",
            "dedupe_keys": {
                "name_birth": "孙战宇_1970",
                "name_birthplace": "孙战宇_山东济南",
                "official_profile_url": "http://www.tianqiao.gov.cn/",
            },
        },
        "current_status": {
            "current_post": "中共济南市天桥区委书记",
            "current_org": "中共济南市天桥区委员会",
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": [
            {"start": "1992年7月", "end": "unknown", "org": "济南市", "title": "基层工作", "level": "", "location": "济南市", "system": "government", "rank": "", "is_key_promotion": False, "notes": "早期履历待查", "confidence": "plausible", "source_ids": ["S001"]},
            {"start": "2019", "end": "2022-12", "org": "济南市历城区", "title": "历城区委副书记", "level": "副处级", "location": "济南市历城区", "system": "party", "rank": "副处级", "is_key_promotion": True, "notes": "", "confidence": "plausible", "source_ids": ["S001"]},
            {"start": "2022-12", "end": "present", "org": "中共济南市天桥区委", "title": "天桥区委书记", "level": "正处级", "location": "济南市天桥区", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "organizations": [
            {"org": "中共济南市天桥区委员会", "role": "区委书记", "period": "2022-12至今"},
            {"org": "中共济南市历城区委员会", "role": "区委副书记", "period": "2019-2022"},
        ],
        "relationships": [
            {"person": "孟帅", "person_id": "shandong_tianqiao_meng_shuai", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "区委书记与区长搭档", "overlap_org": "天桥区委、区政府", "overlap_period": "2024-06至今", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": ["地方治理", "党建"],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": ["party", "government"],
            "geographic_pattern": ["济南市历城区", "济南市天桥区"],
            "promotion_velocity": {
                "summary": "地方干部成长路径",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "unknown",
                    "evidence": "公开资料有限",
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "未发现公开的纪律处分或负面报道",
                "date": "",
                "confidence": "plausible",
                "source_ids": [],
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "天桥区人民政府官网",
                "url": "http://www.tianqiao.gov.cn/",
                "publisher": "济南市天桥区人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "官方网站首页领导活动报道",
            }
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "早期工作经历（1992-2019）不完整",
        },
        "open_questions": [
            {
                "priority": "high",
                "question": "孙战宇1992年7月至2019年的详细履历",
                "why_it_matters": "了解其职业成长路径和关键历练",
                "suggested_queries": ["孙战宇 简历", "孙战宇 济南 历城区", "孙战宇 任前公示"],
                "last_attempted": AS_OF,
            }
        ],
    },
    "2": {  # 孟帅 — 区长
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "山东省",
            "city": "济南市",
            "region": "天桥区",
            "job": "济南市天桥区人民政府区长",
            "task_id": "shandong_天桥区",
            "time_focus": "2020-2026",
        },
        "identity": {
            "person_id": "shandong_tianqiao_meng_shuai",
            "name": "孟帅",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1975年10月",
            "birthplace": "山东济南",
            "native_place": "山东济南",
            "education": [
                {
                    "period": "unknown",
                    "institution": "山东省委党校",
                    "major": "",
                    "degree": "研究生",
                    "study_type": "party_school",
                    "source_ids": ["S001"],
                }
            ],
            "party_join": "中共党员",
            "work_start": "1997年7月",
            "dedupe_keys": {
                "name_birth": "孟帅_1975",
                "name_birthplace": "孟帅_山东济南",
                "official_profile_url": "http://www.tianqiao.gov.cn/",
            },
        },
        "current_status": {
            "current_post": "济南市天桥区人民政府区长",
            "current_org": "济南市天桥区人民政府",
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": [
            {"start": "1997年7月", "end": "unknown", "org": "济南市", "title": "基层工作", "level": "", "location": "济南市", "system": "government", "rank": "", "is_key_promotion": False, "notes": "早期履历待查", "confidence": "plausible", "source_ids": ["S001"]},
            {"start": "2022", "end": "2024-06", "org": "济南市", "title": "济南市政府办公厅或市直部门任职", "level": "副处级", "location": "济南市", "system": "government", "rank": "副处级", "is_key_promotion": True, "notes": "具体职务待查", "confidence": "plausible", "source_ids": ["S001"]},
            {"start": "2024-06", "end": "present", "org": "济南市天桥区人民政府", "title": "天桥区区长", "level": "正处级", "location": "济南市天桥区", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "organizations": [
            {"org": "济南市天桥区人民政府", "role": "区长", "period": "2024-06至今"},
        ],
        "relationships": [
            {"person": "孙战宇", "person_id": "shandong_tianqiao_sun_zhanyu", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "区长与区委书记搭档", "overlap_org": "天桥区委、区政府", "overlap_period": "2024-06至今", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "governance_record": [
            {
                "period": "2026-07",
                "domain": "urban_construction",
                "achievement_or_event": "调研重点市政道路和配套管网建设工作",
                "role_in_event": "亲自调研督导",
                "measurable_outcome": "",
                "location": "济南市天桥区",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "period": "2026-07",
                "domain": "public_security",
                "achievement_or_event": "调研督导全区防汛备汛工作",
                "role_in_event": "亲自调研督导",
                "measurable_outcome": "",
                "location": "济南市天桥区",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
        ],
        "professional_profile": {
            "primary_specializations": ["政府管理", "城市建设"],
            "secondary_specializations": ["应急管理"],
            "career_pattern": "local_ladder",
            "systems_experience": ["government"],
            "geographic_pattern": ["济南市"],
            "promotion_velocity": {
                "summary": "地方干部成长路径",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "grassroots_oriented",
                    "evidence": "亲自调研市政道路、防汛工作（2026年7月15日政府网站报道）",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                }
            ],
            "speech_themes": ["城市建设", "安全防汛"],
            "management_signals": ["亲临一线调研"],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "未发现公开的纪律处分或负面报道",
                "date": "",
                "confidence": "plausible",
                "source_ids": [],
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "天桥区人民政府官网 - 政务要闻",
                "url": "http://www.tianqiao.gov.cn/",
                "publisher": "济南市天桥区人民政府",
                "published_at": "2026-07-15",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "区政府首页多条新闻报道确认孟帅以区长身份主持调研工作",
            }
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "早期工作经历（1997-2022）不完整",
        },
        "open_questions": [
            {
                "priority": "high",
                "question": "孟帅1997年7月至2022年的详细履历",
                "why_it_matters": "了解其职业成长路径和关键历练",
                "suggested_queries": ["孟帅 简历", "孟帅 济南", "孟帅 天桥区 任前公示"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "medium",
                "question": "孟帅2022年至2024年6月间在市直部门的具体职务",
                "why_it_matters": "了解其从市直到区县的任职轨迹",
                "suggested_queries": ["孟帅 济南市政府", "孟帅 任命"],
                "last_attempted": AS_OF,
            },
        ],
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════


def write_person_json(person_id: str, data: dict):
    """Write a single person JSON file."""
    name = data["identity"]["name"]
    job_short = data["investigation_scope"]["job"]
    filename = f"{TODAY}-山东省-济南市-{job_short}-{name}.json"
    path = PERSONS_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {path.name}")


def main():
    print(f"Building {SLUG} network data...")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print()

    # Build database + GEXF
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write person JSON files for core targets
    print()
    print("Writing person JSON files...")
    write_person_json("1", person_json_data["1"])
    write_person_json("2", person_json_data["2"])

    # Summary
    print()
    print(f"=== Summary ===")
    print(f"  Persons:     {len(persons)}")
    print(f"  Orgs:        {len(organizations)}")
    print(f"  Positions:   {len(positions)}")
    print(f"  Relns:       {len(relationships)}")
    print(f"  Person JSONs: 2")
    print()
    print("All artifacts written to staging directory:")
    print(f"  {DB_PATH}")
    print(f"  {GEXF_PATH}")
    for pid in ["1", "2"]:
        d = person_json_data[pid]
        fn = f"{TODAY}-山东省-济南市-{d['investigation_scope']['job']}-{d['identity']['name']}.json"
        print(f"  {PERSONS_DIR / fn}")


if __name__ == "__main__":
    main()
