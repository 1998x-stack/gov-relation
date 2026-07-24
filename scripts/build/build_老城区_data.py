#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 老城区 (Laocheng District), 洛阳市, 河南省.

Level: 市辖区
Province: 河南省
Parent city: 洛阳市
Targets: 区委书记 (Party Secretary: 周新), 区长 (Mayor: 王锋)
Task ID: henan_老城区

Research date: 2026-07-24
Official source: http://www.lylc.gov.cn/ (老城区人民政府)

Current status (as of 2026-07-24):
- 区委书记: 周新 (confirmed via 洛阳市人民政府 site, 2026-07-23 news item)
- 区长: 王锋 (confirmed via 老城区政务公开 page, listed as 区委副书记、区政府党组书记、区长)

Leadership roster sourced from:
  - 洛阳市人民政府: https://www.ly.gov.cn/ (news listing: 老城区委书记周新主持召开专题会议)
  - 老城区政务公开: https://www.lylc.gov.cn/zwgk/ (government leadership listing)
  - 老城区人民政府: http://www.lylc.gov.cn/

Confidence notes:
  周新 (区委书记) identity confirmed via city government news.
  王锋 (区长) identity confirmed via district government leadership listing.
  Government deputy leaders partially identified: 滕婕, 何婧, 刘亚巍, 师建龙, 许宏涛, 刘亮亮.
  Party committee roster not directly available (区委领导班子 members not listed).
  Detailed career histories before current roles not publicly available from web fetch sources.
  Baidu Baike, Exa, Jina Reader, and general web search tools were rate-limited or timed out.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "..").resolve()  # tmp/henan_老城区/../.. = repo root
# Fall back to locate correct root
if not (_REPO_ROOT / "gov_relation").exists():
    # Try going up more levels if this is nested tmp
    _REPO_ROOT = (_STAGING_DIR / "../../..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "老城区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-24"
TODAY = "20260724"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 周新 — 区委书记
    {
        "id": 1,
        "name": "周新",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共老城区委员会",
        "source": "https://www.ly.gov.cn/ (洛阳市人民政府 - 县区新闻, 2026-07-23)",
    },
    # 2. 王锋 — 区长
    {
        "id": 2,
        "name": "王锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "老城区人民政府",
        "source": "https://www.lylc.gov.cn/zwgk/ (老城区政务公开 - 政府领导), 王锋 区委副书记、区政府党组书记、区长",
    },

    # ════════════════════════════════════════
    # 区政府领导 (Government Deputy Leaders)
    # ════════════════════════════════════════

    # 3. 滕婕 — 副区长 (roles not fully detailed from list)
    {
        "id": 3,
        "name": "滕婕",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "老城区人民政府",
        "source": "https://www.lylc.gov.cn/zwgk/ (老城区政务公开 - 政府领导列表)",
    },
    # 4. 何婧 — 副区长
    {
        "id": 4,
        "name": "何婧",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "老城区人民政府",
        "source": "https://www.lylc.gov.cn/zwgk/ (老城区政务公开 - 政府领导列表)",
    },
    # 5. 刘亚巍 — 副区长
    {
        "id": 5,
        "name": "刘亚巍",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "老城区人民政府",
        "source": "https://www.lylc.gov.cn/zwgk/ (老城区政务公开 - 政府领导列表)",
    },
    # 6. 师建龙 — 副区长
    {
        "id": 6,
        "name": "师建龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "老城区人民政府",
        "source": "https://www.lylc.gov.cn/zwgk/ (老城区政务公开 - 政府领导列表)",
    },
    # 7. 许宏涛 — 副区长
    {
        "id": 7,
        "name": "许宏涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "老城区人民政府",
        "source": "https://www.lylc.gov.cn/zwgk/ (老城区政务公开 - 政府领导列表)",
    },
    # 8. 刘亮亮 — 副区长
    {
        "id": 8,
        "name": "刘亮亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "老城区人民政府",
        "source": "https://www.lylc.gov.cn/zwgk/ (老城区政务公开 - 政府领导列表)",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共老城区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共洛阳市委员会",
        "location": "河南省洛阳市老城区",
    },
    {
        "id": 2,
        "name": "老城区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "洛阳市人民政府",
        "location": "河南省洛阳市老城区",
    },
    {
        "id": 3,
        "name": "老城区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "洛阳市人大常委会",
        "location": "河南省洛阳市老城区",
    },
    {
        "id": 4,
        "name": "政协老城区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协洛阳市委员会",
        "location": "河南省洛阳市老城区",
    },
    {
        "id": 5,
        "name": "老城区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共洛阳市纪律检查委员会",
        "location": "河南省洛阳市老城区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── Core Leadership ──
    # 周新 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记",
     "start": "", "end": "present",
     "rank": "正处级",
     "note": "Confirmed as of 2026-07-23 via 洛阳市人民政府 news"},
    # 王锋 - 区长
    {"person_id": 2, "org_id": 2, "title": "区长",
     "start": "", "end": "present",
     "rank": "正处级",
     "note": "Confirmed as 区委副书记、区政府党组书记、区长 via 老城区政务公开页"},

    # ── Government Deputy Leaders ──
    # 滕婕 - 副区长
    {"person_id": 3, "org_id": 2, "title": "副区长",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": "Listed in government leadership section; exact portfolio unknown"},
    # 何婧 - 副区长
    {"person_id": 4, "org_id": 2, "title": "副区长",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": "Listed in government leadership section; exact portfolio unknown"},
    # 刘亚巍 - 副区长
    {"person_id": 5, "org_id": 2, "title": "副区长",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": "Listed in government leadership section; exact portfolio unknown"},
    # 师建龙 - 副区长
    {"person_id": 6, "org_id": 2, "title": "副区长",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": "Listed in government leadership section; exact portfolio unknown"},
    # 许宏涛 - 副区长
    {"person_id": 7, "org_id": 2, "title": "副区长",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": "Listed in government leadership section; exact portfolio unknown"},
    # 刘亮亮 - 副区长
    {"person_id": 8, "org_id": 2, "title": "副区长",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": "Listed in government leadership section; exact portfolio unknown"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 周新 <-> 王锋: 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记周新与区长王锋党政主要领导搭档; 共同负责老城区全面工作",
     "overlap_org": "中共老城区委员会/老城区人民政府",
     "overlap_period": "截至2026年7月"},
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════


def make_source_register() -> list[dict]:
    return [
        {
            "id": "S001",
            "title": "洛阳市人民政府 - 县区新闻",
            "url": "https://www.ly.gov.cn/",
            "publisher": "洛阳市人民政府",
            "published_at": "2026-07-23",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "新闻条目：老城区委书记周新主持召开专题会议",
        },
        {
            "id": "S002",
            "title": "老城区人民政府 - 政务公开 - 领导信息",
            "url": "https://www.lylc.gov.cn/zwgk/",
            "publisher": "老城区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "政府领导页面列出：王锋（区委副书记、区政府党组书记、区长）及六位副区长",
        },
        {
            "id": "S003",
            "title": "老城区人民政府官网",
            "url": "http://www.lylc.gov.cn/",
            "publisher": "老城区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "首页新闻动态显示周新主持书记专题会议",
        },
        {
            "id": "S004",
            "title": "Wikipedia-老城区",
            "url": "https://zh.wikipedia.org/wiki/老城区",
            "publisher": "Wikipedia",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": "老城区行政区划信息; 信息框未列当前领导名单",
        },
    ]


def generate_person_json(job: str, name: str) -> dict:
    """Generate per-person graph JSON following person_graph_json.md schema."""
    person_id_str = f"laocheng_{name}"

    # ── 周新 (区委书记) ──
    if name == "周新":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "洛阳市",
                "region": "老城区",
                "job": "区委书记",
                "task_id": "henan_老城区",
                "time_focus": "当前",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "周新",
                "aliases": [],
                "gender": "",
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "周新_",
                    "name_birthplace": "周新_",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": "区委书记",
                "current_org": "中共老城区委员会",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S003"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "present",
                    "org": "中共老城区委员会",
                    "title": "区委书记",
                    "level": "正处级",
                    "location": "河南省洛阳市老城区",
                    "system": "party",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "Confirmed as of 2026-07-23 via 洛阳市人民政府 news. 具體到任時間、此前職務不明。",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
            ],
            "organizations": [
                {"org_id": 1, "name": "中共老城区委员会", "type": "党委",
                 "level": "县处级", "location": "河南省洛阳市老城区"},
            ],
            "relationships": [
                {"person": "王锋", "person_id": "laocheng_王锋",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区委书记与区长党政主要领导搭档",
                 "overlap_org": "中共老城区委员会/老城区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S002"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["party"],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "公开源不足，无法分析晋升速度",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "unknown",
                        "evidence": "缺少公开报道以推断工作风格",
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
                    "description": "截至2026年7月，未发现公开的纪律处分、审计问题或负面报道",
                    "date": "",
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "source_register": make_source_register(),
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "high",
                "biggest_gap": "完整履历：周新任区委书记前的教育背景、出生日期、籍贯和全部任职经历均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "周新的出生日期、籍贯和毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["周新 简历 老城区", "周新 洛阳 区委书记 简历", "周新 出生 籍贯"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "周新何时开始担任老城区区委书记？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和前任交接",
                    "suggested_queries": ["周新 任 老城区 区委书记", "周新 任前公示", "老城区 区委书记 前任"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "周新的完整职业生涯履历？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["周新 工作 经历 洛阳", "周新 曾担任"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    # ── 王锋 (区长) ──
    if name == "王锋":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "洛阳市",
                "region": "老城区",
                "job": "区长",
                "task_id": "henan_老城区",
                "time_focus": "当前",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "王锋",
                "aliases": [],
                "gender": "",
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "王锋_",
                    "name_birthplace": "王锋_",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": "区长",
                "current_org": "老城区人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S002"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "present",
                    "org": "老城区人民政府",
                    "title": "区长",
                    "level": "正处级",
                    "location": "河南省洛阳市老城区",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "Listed as 区委副书记、区政府党组书记、区长 on 老城区政务公开页. 具體到任時間、此前職務不明。",
                    "confidence": "confirmed",
                    "source_ids": ["S002"],
                },
            ],
            "organizations": [
                {"org_id": 2, "name": "老城区人民政府", "type": "政府",
                 "level": "县处级", "location": "河南省洛阳市老城区"},
            ],
            "relationships": [
                {"person": "周新", "person_id": "laocheng_周新",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区长与区委书记党政主要领导搭档",
                 "overlap_org": "中共老城区委员会/老城区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S002"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["government"],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "公开源不足，无法分析晋升速度",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "low_profile",
                        "evidence": "无公开新闻报道可确认其具体工作风格",
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
                    "description": "截至2026年7月，未发现公开的纪律处分、审计问题或负面报道",
                    "date": "",
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "source_register": make_source_register(),
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "high",
                "biggest_gap": "完整履历：王锋任区长前的教育背景、出生日期、籍贯和全部任职经历均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "王锋的出生日期、籍贯和毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["王锋 简历 老城区", "王锋 洛阳 区长 简历", "王锋 出生 籍贯"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "王锋何时开始担任老城区区长？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和前任交接",
                    "suggested_queries": ["王锋 任 老城区 区长", "王锋 任前公示", "老城区 区长 前任"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "王锋的完整职业生涯履历？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["王锋 工作 经历 洛阳", "王锋 曾担任"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    return None


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════


def main():
    # Create DB and GEXF via runner
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write person JSONs
    for p in persons:
        job = p["current_post"]
        name = p["name"]
        if name in ("周新", "王锋"):
            data = generate_person_json(job, name)
            if data:
                person_path = PERSONS_DIR / f"{TODAY}-河南省-洛阳市-{job}-{name}.json"
                with open(person_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"  Person JSON: {person_path.relative_to(_REPO_ROOT)}")

    print("\nDone.")


if __name__ == "__main__":
    main()
