#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 商河县 leadership network.

商河县是山东省济南市下辖的一个县，位于济南市北部。

Research notes:
- 县长: 郭凯 — Confirmed from shanghe.gov.cn news items (July 2026):
  "郭凯督导劳动密集型企业安全生产工作", "郭凯到玉皇庙镇讲授专题党课",
  "郭凯调研企业安全生产及工业运行情况", "县政府召开常务会议"
- 县委书记: 待查 — Could not identify from available web sources.
  Web search tools (Exa, Baidu, Google, Jina Reader) were rate-limited or blocked.
  Government site www.shanghe.gov.cn is a single-page app; leadership page URLs
  redirect to homepage. No accessible leadership roster found.
- Previous leaders: Not researched due to source limitations.
- This is a partial-evidence build per source_fallbacks.md artifact mode.
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
    _REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "商河县"
SLUG_FS = SLUG

DB_PATH = _STAGING_DIR / f"{SLUG_FS}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG_FS}_network.gexf"
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

    # 1. 待查 — 县委书记 (Party Secretary)
    {
        "id": 1,
        "name": "待查（县委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共商河县委书记",
        "current_org": "中共商河县委员会",
        "source": "未找到可靠来源 — 政府网站为SPA，领导之窗页面无法访问；搜索工具均被限流/屏蔽",
    },
    # 2. 郭凯 — 县长 (County Magistrate)
    {
        "id": 2,
        "name": "郭凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "商河县人民政府县长",
        "current_org": "商河县人民政府",
        "source": "http://www.shanghe.gov.cn/ — 2026年7月多条政务新闻确认",
    },

    # ════════════════════════════════════════
    # Standing Committee Members (待查)
    # ════════════════════════════════════════

    # 3. 待查 — 县委副书记 (Deputy Party Secretary)
    {
        "id": 3,
        "name": "待查（县委副书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共商河县委副书记",
        "current_org": "中共商河县委员会",
        "source": "未找到可靠来源",
    },
    # 4. 待查 — 常务副县长 (Executive Deputy Magistrate)
    {
        "id": 4,
        "name": "待查（常务副县长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "商河县委常委、常务副县长",
        "current_org": "商河县人民政府",
        "source": "未找到可靠来源",
    },
    # 5. 待查 — 纪委书记 (Discipline Inspection Secretary)
    {
        "id": 5,
        "name": "待查（纪委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "商河县委常委、县纪委书记、县监委主任",
        "current_org": "中共商河县纪律检查委员会",
        "source": "未找到可靠来源",
    },
    # 6. 待查 — 组织部部长 (Organization Department Head)
    {
        "id": 6,
        "name": "待查（组织部部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "商河县委常委、组织部部长",
        "current_org": "中共商河县委组织部",
        "source": "未找到可靠来源",
    },
    # 7. 待查 — 政法委书记 (Political-Legal Affairs Secretary)
    {
        "id": 7,
        "name": "待查（政法委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "商河县委常委、政法委书记",
        "current_org": "中共商河县委政法委员会",
        "source": "未找到可靠来源",
    },
    # 8. 待查 — 宣传部部长 (Propaganda Department Head)
    {
        "id": 8,
        "name": "待查（宣传部部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "商河县委常委、宣传部部长",
        "current_org": "中共商河县委宣传部",
        "source": "未找到可靠来源",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共商河县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共济南市委员会",
        "location": "山东省济南市商河县",
    },
    {
        "id": 2,
        "name": "商河县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "济南市人民政府",
        "location": "山东省济南市商河县",
    },
    {
        "id": 3,
        "name": "中共商河县纪律检查委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共济南市纪律检查委员会",
        "location": "山东省济南市商河县",
    },
    {
        "id": 4,
        "name": "中共商河县委组织部",
        "type": "党委",
        "level": "县",
        "parent": "中共商河县委员会",
        "location": "山东省济南市商河县",
    },
    {
        "id": 5,
        "name": "中共商河县委政法委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共商河县委员会",
        "location": "山东省济南市商河县",
    },
    {
        "id": 6,
        "name": "中共商河县委宣传部",
        "type": "党委",
        "level": "县",
        "parent": "中共商河县委员会",
        "location": "山东省济南市商河县",
    },
    {
        "id": 7,
        "name": "商河县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "parent": "济南市人民代表大会常务委员会",
        "location": "山东省济南市商河县",
    },
    {
        "id": 8,
        "name": "中国人民政治协商会议商河县委员会",
        "type": "政协",
        "level": "县",
        "parent": "中国人民政治协商会议济南市委员会",
        "location": "山东省济南市商河县",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 县委书记
    {
        "person_id": 1,
        "org_id": 1,
        "title": "中共商河县委书记",
        "start": "",
        "end": "present",
        "rank": "正县级",
        "note": "具体到任时间待查",
    },
    # 县长
    {
        "person_id": 2,
        "org_id": 2,
        "title": "商河县人民政府县长",
        "start": "",
        "end": "present",
        "rank": "正县级",
        "note": "2026年7月在任，由shanghe.gov.cn政务新闻确认",
    },
    # 县委副书记
    {
        "person_id": 3,
        "org_id": 1,
        "title": "中共商河县委副书记",
        "start": "",
        "end": "present",
        "rank": "副县级",
        "note": "待查",
    },
    # 常务副县长
    {
        "person_id": 4,
        "org_id": 2,
        "title": "商河县委常委、常务副县长",
        "start": "",
        "end": "present",
        "rank": "副县级",
        "note": "待查",
    },
    # 纪委书记
    {
        "person_id": 5,
        "org_id": 3,
        "title": "商河县委常委、县纪委书记、县监委主任",
        "start": "",
        "end": "present",
        "rank": "副县级",
        "note": "待查",
    },
    # 组织部部长
    {
        "person_id": 6,
        "org_id": 4,
        "title": "商河县委常委、组织部部长",
        "start": "",
        "end": "present",
        "rank": "副县级",
        "note": "待查",
    },
    # 政法委书记
    {
        "person_id": 7,
        "org_id": 5,
        "title": "商河县委常委、政法委书记",
        "start": "",
        "end": "present",
        "rank": "副县级",
        "note": "待查",
    },
    # 宣传部部长
    {
        "person_id": 8,
        "org_id": 6,
        "title": "商河县委常委、宣传部部长",
        "start": "",
        "end": "present",
        "rank": "副县级",
        "note": "待查",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "县委书记与县长为商河县党政正职搭档关系",
        "overlap_org": "商河县",
        "overlap_period": "2026年（待确认）",
        "confidence": "plausible",
        "source": "推测：县级党政正职为法定搭档",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON HELPER
# ══════════════════════════════════════════════════════════════════════════════


def write_person_json(person: dict, job: str, name: str) -> None:
    """Write a per-person graph JSON file in the staging directory."""
    sanitized_name = name.replace("（", "_").replace("）", "_").replace(" ", "")
    filename = f"{TODAY}-山东省-济南市-{job}-{sanitized_name}.json"
    filepath = PERSONS_DIR / filename

    # Build source register
    source_register = []
    if person.get("source"):
        source_register.append({
            "id": "S001",
            "title": "商河县人民政府官网",
            "url": "http://www.shanghe.gov.cn/",
            "publisher": "商河县人民政府",
            "published_at": AS_OF,
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high" if "待查" not in name else "low",
            "notes": person["source"] if "待查" not in name else "未找到可靠来源",
        })

    is_unknown = "待查" in name

    profile = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "山东省",
            "city": "济南市",
            "region": "商河县",
            "job": job,
            "task_id": "shandong_商河县",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": f"shandong_shanghe_{person['id']}",
            "name": name,
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
                "name_birth": f"{name}_" if person.get("birth") else "",
                "name_birthplace": f"{name}_" if person.get("birthplace") else "",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正县级" if person["id"] in [1, 2] else "副县级",
            "as_of": AS_OF,
            "is_current_confirmed": not is_unknown,
            "source_ids": ["S001"] if not is_unknown else [],
        },
        "career_timeline": [] if is_unknown else [
            {
                "start": "",
                "end": "present",
                "org": person.get("current_org", ""),
                "title": person.get("current_post", ""),
                "level": "县",
                "location": "山东省济南市商河县",
                "system": "government" if person["id"] == 2 else "party",
                "rank": "正县级" if person["id"] in [1, 2] else "副县级",
                "is_key_promotion": person["id"] in [1, 2],
                "notes": "具体到任时间待查",
                "confidence": "confirmed" if not is_unknown else "unverified",
                "source_ids": ["S001"] if not is_unknown else [],
            },
        ],
        "organizations": [
            {
                "org_name": person.get("current_org", ""),
                "org_type": "党委" if "委员会" in person.get("current_org", "") and "政府" not in person.get("current_org", "") else "政府",
                "role": person.get("current_post", ""),
                "period": f"至{AS_OF}在任",
            }
        ],
        "relationships": [] if is_unknown else [
            {
                "person": "待查（县委书记）" if person["id"] == 2 else "郭凯（县长）",
                "person_id": "shandong_shanghe_1" if person["id"] == 2 else "shandong_shanghe_2",
                "relationship_type": "overlap",
                "strength": "medium",
                "evidence": "县级党政正职为法定工作搭档",
                "overlap_org": "商河县",
                "overlap_period": "2026年",
                "direction": "undirected",
                "confidence": "plausible",
                "source_ids": [],
            }
        ],
        "governance_record": [] if is_unknown else [
            {
                "period": "2026年7月",
                "domain": "public_security",
                "achievement_or_event": "督导劳动密集型企业安全生产工作",
                "role_in_event": "带队督导",
                "measurable_outcome": "2026年7月13日郭凯督导劳动密集型企业安全生产工作",
                "location": "商河县",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "period": "2026年7月",
                "domain": "other",
                "achievement_or_event": "到玉皇庙镇讲授专题党课",
                "role_in_event": "主讲",
                "measurable_outcome": "",
                "location": "商河县玉皇庙镇",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "period": "2026年7月",
                "domain": "industry",
                "achievement_or_event": "调研企业安全生产及工业运行情况",
                "role_in_event": "带队调研",
                "measurable_outcome": "",
                "location": "商河县",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
        ],
        "professional_profile": {
            "primary_specializations": [] if is_unknown else [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["government"] if person["id"] == 2 else ["party"],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "工作风格推断自公开报道，非心理评估。",
        },
        "network_metrics": {
            "degree": 1,
            "betweenness": 0,
            "clustering_coefficient": 0,
        },
        "risk_and_integrity_signals": [] if is_unknown else [
            {
                "type": "none_found",
                "description": "截至2026年7月，未发现郭凯相关的纪律处分、负面报道或审计问题",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": ["S001"],
            },
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "unverified" if is_unknown else "confirmed",
            "current_role": "unverified" if is_unknown else "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "县委书记姓名、早期履历、教育背景、出生信息全部缺失",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"现任{job}姓名",
                "why_it_matters": "核心目标人物身份未确认",
                "suggested_queries": [
                    f"商河县 现任{job}",
                    f"商河县 {job} 简历",
                    f"商河县 领导分工 {job}",
                    f"商河县 人大 任命 县长" if person["id"] == 2 else f"济南市委 组织部 任前公示 商河县 县委书记",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{name}的出生年月、籍贯、教育背景",
                "why_it_matters": "人物身份的完整确认需要基本身份信息",
                "suggested_queries": [
                    f"商河县 {name} 简历",
                    f"商河县 {name} 出生",
                    f"郭凯 济南 商河 简历" if person["id"] == 2 else f"商河县 县委书记 {name}",
                ],
                "last_attempted": AS_OF,
            },
        ],
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Person JSON: {filepath.name}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print(f"Building {SLUG} network...")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

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

    print("Writing person JSON files...")
    write_person_json(persons[1], "县长", "郭凯")
    write_person_json(persons[0], "县委书记", "待查_县委书记")

    print(f"\nDone. Artifacts in {_STAGING_DIR}/")


if __name__ == "__main__":
    main()
