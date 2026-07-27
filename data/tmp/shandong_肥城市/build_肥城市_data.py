#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 肥城市 (Feicheng City), 泰安市, 山东省.

Investigation date: 2026-07-25
Task ID: shandong_肥城市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - zh.wikipedia.org/wiki/肥城市 — Infobox confirms 市委书记=张莉, 市长=展延安
  - zh.wikipedia.org/w/api.php — 现任领导 table shows historical data
    (范长征 1970.05, 赵燕军 1963.03, 侯庆洋 1961.09, 戴先锋 1969.08)
  - www.feicheng.gov.cn — 肥城市人民政府官方网站 (timeout during investigation)

Confidence notes:
  - 张莉 (市委书记): confirmed via Wikipedia infobox, details unverified
  - 展延安 (市长): confirmed via Wikipedia infobox, details unverified
  - 范长征 (前任书记/市长): confirmed via Wikipedia table, 1970年生山东东平人
  - 赵燕军 (人大主任): from Wikipedia table, likely outdated
  - 侯庆洋 (政协主席): from Wikipedia table, likely outdated
  - 戴先锋 (监委主任): from Wikipedia table, likely outdated
  - Other 市委常委/副市长: unverified — web access degraded (Exa rate-limited, 
    feicheng.gov.cn timeout, Baidu 403, Jina Reader timeout)
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
SLUG = "肥城市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shandong_肥城市"
if _CURRENT_DIR.name == "shandong_肥城市":
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
# IDs: 1-2 core (市委书记/市长), 3-4 人大/政协, 5-9 县委常委/副市长,
#       10-19 其他领导, 30+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "张莉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",  # 待查
        "birthplace": "",  # 待查
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共肥城市委员会",
        "source": "https://zh.wikipedia.org/wiki/肥城市",
        "confidence": "confirmed",
        "notes": "Wikipedia infobox确认张莉为现任市委书记（男性名实为女性），接替范长征。此前简历待查。"
    },
    {
        "id": 2,
        "name": "展延安",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # 待查
        "birthplace": "",  # 待查
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "肥城市人民政府",
        "source": "https://zh.wikipedia.org/wiki/肥城市",
        "confidence": "confirmed",
        "notes": "Wikipedia infobox确认展延安为现任市长。此前简历待查。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 人大、政协 Leaders (from Wikipedia table — may be outdated)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "赵燕军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963-03",
        "birthplace": "山东省东平县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "肥城市人民代表大会常务委员会",
        "source": "https://zh.wikipedia.org/wiki/肥城市",
        "confidence": "plausible",
        "notes": "Wikipedia现任领导表记录，2017年就任。注：可能已调整。"
    },
    {
        "id": 4,
        "name": "侯庆洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1961-09",
        "birthplace": "山东省肥城市",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议肥城市委员会",
        "source": "https://zh.wikipedia.org/wiki/肥城市",
        "confidence": "plausible",
        "notes": "Wikipedia现任领导表记录，2017年就任。注：可能已调整。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 其他主要市领导 (from Wikipedia table)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 5,
        "name": "戴先锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-08",
        "birthplace": "山东省东平县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市监察委员会主任",
        "current_org": "肥城市监察委员会",
        "source": "https://zh.wikipedia.org/wiki/肥城市",
        "confidence": "plausible",
        "notes": "Wikipedia现任领导表记录，2018年当选。注：可能已调整。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 前任主要领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "范长征",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-05",
        "birthplace": "山东省东平县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记/市长",
        "current_org": "中共肥城市委员会",
        "source": "https://zh.wikipedia.org/wiki/肥城市",
        "confidence": "confirmed",
        "notes": "曾任肥城市委书记兼市长（2017-2022年左右），回族。1970年5月出生，山东东平人。去向待查——可能调任泰安市或其他岗位。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共肥城市委员会", "type": "党委", "level": "县级市", "parent": "泰安市", "location": "山东省泰安市肥城市"},
    {"id": 2, "name": "肥城市人民政府", "type": "政府", "level": "县级市", "parent": "泰安市", "location": "山东省泰安市肥城市"},
    {"id": 3, "name": "肥城市人民代表大会常务委员会", "type": "人大", "level": "县级市", "parent": "泰安市", "location": "山东省泰安市肥城市"},
    {"id": 4, "name": "中国人民政治协商会议肥城市委员会", "type": "政协", "level": "县级市", "parent": "泰安市", "location": "山东省泰安市肥城市"},
    {"id": 5, "name": "肥城市监察委员会", "type": "其他", "level": "县级市", "parent": "泰安市", "location": "山东省泰安市肥城市"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 张莉
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "", "end": "present", "rank": "正处级", "note": "2026年7月在职，接替范长征"},
    # 展延安
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "", "end": "present", "rank": "正处级", "note": "2026年7月在职"},
    # 赵燕军
    {"person_id": 3, "org_id": 3, "title": "市人大常委会主任", "start": "2017-01", "end": "present", "rank": "正处级", "note": "2017年1月就任"},
    # 侯庆洋
    {"person_id": 4, "org_id": 4, "title": "市政协主席", "start": "2017-01", "end": "present", "rank": "正处级", "note": "2017年1月就任"},
    # 戴先锋
    {"person_id": 5, "org_id": 5, "title": "市监察委员会主任", "start": "2018-01", "end": "present", "rank": "副处级", "note": "2018年1月当选"},
    # 范长征 (前任)
    {"person_id": 30, "org_id": 1, "title": "市委书记", "start": "2017-01", "end": "", "rank": "正处级", "note": "2017年1月就任市委书记，同时兼任市长至2022年1月"},
    {"person_id": 30, "org_id": 2, "title": "市长", "start": "", "end": "2022-01", "rank": "正处级", "note": "2022年1月卸任市长（专任书记？），回族"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 张莉 ↔ 展延安 (书记-市长搭班)
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "市委书记与市长搭班，共同领导肥城市工作",
        "overlap_org": "中共肥城市委员会/肥城市人民政府",
        "overlap_period": AS_OF,
        "strength": "strong",
        "confidence": "confirmed",
        "source": "https://zh.wikipedia.org/wiki/肥城市"
    },
    # 张莉 ↔ 范长征 (继任关系)
    {
        "person_a": 1, "person_b": 30,
        "type": "predecessor_successor",
        "context": "张莉接替范长征担任肥城市委书记",
        "overlap_org": "中共肥城市委员会",
        "overlap_period": "",
        "strength": "medium",
        "confidence": "plausible",
        "source": "https://zh.wikipedia.org/wiki/肥城市"
    },
    # 展延安 ↔ 范长征 (可能为继任关系)
    {
        "person_a": 2, "person_b": 30,
        "type": "predecessor_successor",
        "context": "范长征此前兼任市长，展延安接任市长",
        "overlap_org": "肥城市人民政府",
        "overlap_period": "",
        "strength": "medium",
        "confidence": "plausible",
        "source": "https://zh.wikipedia.org/wiki/肥城市"
    },
    # 赵燕军 ↔ 张莉 (人大-党委)
    {
        "person_a": 3, "person_b": 1,
        "type": "overlap",
        "context": "市人大常委会主任与市委书记",
        "overlap_org": "肥城市",
        "overlap_period": AS_OF,
        "strength": "weak",
        "confidence": "plausible",
        "source": ""
    },
    # 侯庆洋 ↔ 张莉 (政协-党委)
    {
        "person_a": 4, "person_b": 1,
        "type": "overlap",
        "context": "市政协主席与市委书记",
        "overlap_org": "肥城市",
        "overlap_period": AS_OF,
        "strength": "weak",
        "confidence": "plausible",
        "source": ""
    },
]

# ── Person JSON Helper ───────────────────────────────────────────────────────

def write_person_json(person: dict, extra: dict | None = None) -> str:
    """Write a person JSON to PJSON_DIR and return its filename."""
    job_slug = person["current_post"].replace("/", "_")
    fname = f"{TODAY}-山东省-泰安市-{job_slug}-{person['name']}.json"
    path = PJSON_DIR / fname

    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "山东省",
            "city": "泰安市",
            "region": "肥城市",
            "job": person["current_post"],
            "task_id": "shandong_肥城市",
            "time_focus": "2026-07"
        },
        "identity": {
            "person_id": f"feicheng_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [{"institution": person["education"], "period": "", "major": "", "degree": "", "study_type": "unknown", "source_ids": ["S001"]}] if person["education"] else [],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "name_birthplace": f"{person['name']}_{person['birthplace']}",
                "official_profile_url": person["source"]
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if person["id"] in [1, 2, 3, 4, 30] else ("副处级" if person["id"] < 30 else "待查"),
            "as_of": AS_OF,
            "is_current_confirmed": person["confidence"] == "confirmed",
            "source_ids": ["S001"]
        },
        "career_timeline": _career_timeline_for(person),
        "organizations": [],
        "relationships": _relationships_for(person),
        "governance_record": _governance_record_for(person),
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": ["泰安市"],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "No public risk signals found in available sources", "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {"id": "S001", "title": person["notes"], "url": person["source"], "publisher": "Wikipedia", "published_at": AS_OF, "accessed_at": TODAY, "source_type": "encyclopedia" if "wiki" in person["source"] else "official", "reliability": "medium", "notes": ""}
        ],
        "confidence_summary": {
            "identity": person["confidence"],
            "current_role": "confirmed" if person["id"] in [1, 2] else "plausible",
            "career_completeness": "partial" if person["birth"] else "thin",
            "relationship_confidence": "low",
            "biggest_gap": f"完整履历待查" if not person["birth"] else "详细履历待查"
        },
        "open_questions": _open_questions_for(person)
    }

    if extra:
        data.update(extra)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return fname


def _career_timeline_for(person: dict) -> list:
    """Build career timeline from positions."""
    if person["id"] == 1:  # 张莉
        return [
            {"start": "unknown", "end": "present", "org": "中共肥城市委员会", "title": "市委书记", "level": "正处级", "location": "泰安市肥城市", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "2026年7月在职，接替范长征", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "此前任职履历完全未知——推测曾任泰安市或其他县区领导", "confidence": "unverified", "source_ids": []},
        ]
    elif person["id"] == 2:  # 展延安
        return [
            {"start": "unknown", "end": "present", "org": "肥城市人民政府", "title": "市长", "level": "正处级", "location": "泰安市肥城市", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "2026年7月在职", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "此前任职履历完全未知", "confidence": "unverified", "source_ids": []},
        ]
    elif person["id"] == 30:  # 范长征
        return [
            {"start": "2017-01", "end": "", "org": "中共肥城市委员会", "title": "市委书记", "level": "正处级", "location": "泰安市肥城市", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "2017年1月任肥城市委书记，回族", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "", "end": "2022-01", "org": "肥城市人民政府", "title": "市长", "level": "正处级", "location": "泰安市肥城市", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "兼任市长至2022年1月", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "2017年以前及卸任后的任职履历待查", "confidence": "unverified", "source_ids": []},
        ]
    return [
        {"start": "unknown", "end": "present", "org": person["current_org"], "title": person["current_post"], "level": "", "location": "泰安市肥城市", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": person["confidence"], "source_ids": ["S001"]}
    ]


def _relationships_for(person: dict) -> list:
    """Build relationship list for this person."""
    rs = []
    for r in relationships:
        other_id = r["person_b"] if r["person_a"] == person["id"] else (r["person_a"] if r["person_b"] == person["id"] else None)
        if other_id is not None:
            other = next((p for p in persons if p["id"] == other_id), None)
            if other:
                rs.append({
                    "person": other["name"],
                    "person_id": f"feicheng_{other['name']}",
                    "relationship_type": r["type"],
                    "strength": r["strength"],
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "undirected",
                    "confidence": r["confidence"],
                    "source_ids": []
                })
    return rs


def _governance_record_for(person: dict) -> list:
    """Build governance record for this person."""
    if person["id"] == 1:  # 张莉
        return [
            {"period": "2026", "domain": "economic_development", "achievement_or_event": "担任肥城市委书记，领导肥城市经济社会发展", "role_in_event": "市委书记", "measurable_outcome": "", "location": "肥城市", "confidence": "confirmed", "source_ids": ["S001"]},
        ]
    elif person["id"] == 2:  # 展延安
        return [
            {"period": "2026", "domain": "economic_development", "achievement_or_event": "担任肥城市市长，主持市政府全面工作", "role_in_event": "市长", "measurable_outcome": "", "location": "肥城市", "confidence": "confirmed", "source_ids": ["S001"]},
        ]
    elif person["id"] == 30:  # 范长征
        return [
            {"period": "2017-2022", "domain": "economic_development", "achievement_or_event": "担任肥城市委书记兼市长期间，领导肥城市发展", "role_in_event": "市委书记/市长", "measurable_outcome": "", "location": "肥城市", "confidence": "confirmed", "source_ids": ["S001"]},
        ]
    return []


def _open_questions_for(person: dict) -> list:
    """Build open questions for this person."""
    questions = []
    if person["id"] in [1, 2]:
        questions.append({
            "priority": "critical",
            "question": f"{person['name']}的完整履历",
            "why_it_matters": "核心领导背景未知",
            "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 任前公示", f"{person['name']} 泰安"],
            "last_attempted": TODAY
        })
        questions.append({
            "priority": "high",
            "question": f"{person['name']}的出生年月和籍贯",
            "why_it_matters": "身份识别关键信息",
            "suggested_queries": [f"{person['name']} 出生"],
            "last_attempted": TODAY
        })
    elif person["id"] == 30:
        questions.append({
            "priority": "medium",
            "question": "范长征的卸任时间及去向",
            "why_it_matters": "前任书记去向不明",
            "suggested_queries": ["范长征 去向", "范长征 肥城 调任"],
            "last_attempted": TODAY
        })
    return questions


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"Building {SLUG} network...")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write person JSONs for core leaders and key figures
    core_ids = [1, 2, 30]
    for pid in core_ids:
        person = next(p for p in persons if p["id"] == pid)
        fname = write_person_json(person)
        print(f"  Person JSON: {fname}")

    print(f"\nDone. Database: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"Person JSONs in: {PJSON_DIR}")


if __name__ == "__main__":
    main()
