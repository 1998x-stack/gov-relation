#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 岐山县, 宝鸡市, 陕西省.

Investigation date: 2026-07-25
Task ID: shaanxi_岐山县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - www.qishan.gov.cn — 岐山县人民政府官方网站 (unreachable — timed out)
  - www.baoji.gov.cn — 宝鸡市人民政府官方网站 (unreachable — timed out)
  - Baidu Baike (403), Exa (rate-limited), Google (blocked), DuckDuckGo (timed out)
  - Jina Reader (timed out), Wikipedia (timed out)

Known connections from existing repo data:
  - 张建科 (渭滨区委书记, b. 1973-03, 陕西省岐山县) — confirmed connection via 宝鸡市 build script

Confidence notes:
  - All web sources were unreachable from the research environment (July 2026).
  - Government sites (qishan.gov.cn, baoji.gov.cn) all timed out.
  - Baidu Baike returned HTTP 403.
  - Exa search API rate-limited.
  - Wikipedia and Jina Reader timed out.
  - All current-role claims are labeled 'unverified' due to inability to confirm
    via live web sources in this session.
  - 县委书记姓名: 待查 — per established pattern when county party secretary name
    is not confirmable on government pages.
  - 县长姓名: 待查 — same treatment.
  - Artifacts created with explicit uncertainty per partial evidence mode.
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
SLUG = "岐山县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shaanxi_岐山县"
if _CURRENT_DIR.name == "shaanxi_岐山县":
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
# IDs: 1=县委书记, 2=县长, 3-8=常委/副县长

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
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
        "current_post": "县委书记",
        "current_org": "中共岐山县委员会",
        "source": "待查 — 岐山县政府官网(qishan.gov.cn)无法访问",
        "confidence": "unverified",
        "notes": "县委书记姓名确认失败。县政府网站qishan.gov.cn及所有子页面均超时无法访问。宝鸡市政府网站同样不可达。未找到任何可靠的公开来源确认当前在任县委书记姓名。需后续通过宝鸡市委组织部公示或新闻报道进一步核实。"
    },
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
        "current_post": "县委副书记、县长",
        "current_org": "岐山县人民政府",
        "source": "待查 — 岐山县政府官网(qishan.gov.cn)无法访问",
        "confidence": "unverified",
        "notes": "县长姓名确认失败。与县委书记同因网络不可达而无法确认。县政府官网全部超时。需后续核实。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Key Standing Committee Members (inferred default org structure)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "待查_常务副县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长（常务）",
        "current_org": "岐山县人民政府",
        "source": "待查 — 默认县级班子构成推断",
        "confidence": "unverified",
        "notes": "常务副县长姓名待核实。县级政府一般配备一名常务副县长。具体信息需从岐山县政府网站领导分工页面获取。"
    },
    {
        "id": 4,
        "name": "待查_纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共岐山县纪律检查委员会",
        "source": "待查 — 默认县级纪检班子构成推断",
        "confidence": "unverified",
        "notes": "县纪委书记姓名待核实。属县级标配常委职务。"
    },
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
        "current_post": "县委常委、组织部部长",
        "current_org": "中共岐山县委组织部",
        "source": "待查 — 默认县级班子构成推断",
        "confidence": "unverified",
        "notes": "县委组织部部长姓名待核实。"
    },
    {
        "id": 6,
        "name": "待查_宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共岐山县委宣传部",
        "source": "待查 — 默认县级班子构成推断",
        "confidence": "unverified",
        "notes": "县委宣传部部长姓名待核实。"
    },
    {
        "id": 7,
        "name": "待查_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共岐山县委政法委员会",
        "source": "待查 — 默认县级班子构成推断",
        "confidence": "unverified",
        "notes": "县委政法委书记姓名待核实。"
    },
    {
        "id": 8,
        "name": "待查_副县长（公安局长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "岐山县公安局",
        "source": "待查 — 默认县级政府构成推断",
        "confidence": "unverified",
        "notes": "分管公安的副县长兼公安局长姓名待核实。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Known Related Persons (from existing repo data)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 9,
        "name": "张建科",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-03",
        "birthplace": "陕西省岐山县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "渭滨区委书记",
        "current_org": "中共宝鸡市渭滨区委",
        "source": "宝鸡市 build script (scripts/build/build_宝鸡市_data.py)",
        "confidence": "confirmed",
        "notes": "岐山籍在外领导干部。出生于岐山县，现任宝鸡市渭滨区委书记。与岐山县有地缘联系。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共岐山县委员会", "type": "党委", "level": "县处级", "parent": "中共宝鸡市委", "location": "岐山县"},
    {"id": 2, "name": "岐山县人民政府", "type": "政府", "level": "县处级", "parent": "宝鸡市人民政府", "location": "岐山县"},
    {"id": 3, "name": "中国人民政治协商会议岐山县委员会", "type": "政协", "level": "县处级", "parent": "政协宝鸡市委", "location": "岐山县"},
    {"id": 4, "name": "岐山县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "宝鸡市人大常委会", "location": "岐山县"},
    {"id": 5, "name": "中共岐山县纪律检查委员会（监察委员会）", "type": "纪委", "level": "县处级", "parent": "宝鸡市纪委", "location": "岐山县"},
    {"id": 6, "name": "中共岐山县委组织部", "type": "党委", "level": "县处级", "parent": "中共岐山县委员会", "location": "岐山县"},
    {"id": 7, "name": "中共岐山县委宣传部", "type": "党委", "level": "县处级", "parent": "中共岐山县委员会", "location": "岐山县"},
    {"id": 8, "name": "中共岐山县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共岐山县委员会", "location": "岐山县"},
    {"id": 9, "name": "岐山县公安局", "type": "政府", "level": "乡科级", "parent": "岐山县人民政府", "location": "岐山县"},
    {"id": 10, "name": "中共宝鸡市渭滨区委", "type": "党委", "level": "县处级", "parent": "中共宝鸡市委", "location": "宝鸡市渭滨区"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 待查_县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "县委书记姓名待核实。所有政府网站不可达。"},
    # 待查_县长
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "县长姓名待核实。"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "县长兼任县委副书记"},
    # 待查_常务副县长
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "副县长（常务）", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "分管发改、财政、应急、人社等"},
    # 待查_纪委书记
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 5, "title": "县纪委书记、县监委主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 待查_组织部长
    {"person_id": 5, "org_id": 1, "title": "县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": ""},
    {"person_id": 5, "org_id": 6, "title": "组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 待查_宣传部长
    {"person_id": 6, "org_id": 1, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": ""},
    {"person_id": 6, "org_id": 7, "title": "宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 待查_政法委书记
    {"person_id": 7, "org_id": 1, "title": "县委常委、政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": ""},
    {"person_id": 7, "org_id": 8, "title": "政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 待查_副县长（公安局长）
    {"person_id": 8, "org_id": 2, "title": "副县长（兼县公安局局长）", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": ""},
    {"person_id": 8, "org_id": 9, "title": "县公安局局长", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": ""},
    # 张建科
    {"person_id": 9, "org_id": 10, "title": "渭滨区委书记", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "岐山籍在外干部"},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长为党政主要领导搭档关系",
        "overlap_org": "中共岐山县委员会",
        "overlap_period": "当前",
        "confidence": "unverified",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与常务副县长为县委与政府领导关系",
        "overlap_org": "中共岐山县委员会",
        "overlap_period": "当前",
        "confidence": "unverified",
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县长与常务副县长为政府主要领导与副手关系",
        "overlap_org": "岐山县人民政府",
        "overlap_period": "当前",
        "confidence": "unverified",
    },
    {
        "person_a": 2,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "县长与分管公安的副县长为政府领导关系",
        "overlap_org": "岐山县人民政府",
        "overlap_period": "当前",
        "confidence": "unverified",
    },
    {
        "person_a": 3,
        "person_b": 4,
        "type": "overlap",
        "context": "同为县委常委班子成员",
        "overlap_org": "中共岐山县委员会",
        "overlap_period": "当前",
        "confidence": "unverified",
    },
    {
        "person_a": 3,
        "person_b": 5,
        "type": "overlap",
        "context": "同为县委常委班子成员",
        "overlap_org": "中共岐山县委员会",
        "overlap_period": "当前",
        "confidence": "unverified",
    },
    {
        "person_a": 4,
        "person_b": 5,
        "type": "overlap",
        "context": "同为县委常委班子成员",
        "overlap_org": "中共岐山县委员会",
        "overlap_period": "当前",
        "confidence": "unverified",
    },
    {
        "person_a": 5,
        "person_b": 6,
        "type": "overlap",
        "context": "同为县委常委班子成员",
        "overlap_org": "中共岐山县委员会",
        "overlap_period": "当前",
        "confidence": "unverified",
    },
    {
        "person_a": 6,
        "person_b": 7,
        "type": "overlap",
        "context": "同为县委常委班子成员",
        "overlap_org": "中共岐山县委员会",
        "overlap_period": "当前",
        "confidence": "unverified",
    },
    # 岐山籍在外领导干部关系
    {
        "person_a": 1,
        "person_b": 9,
        "type": "hometown_connection",
        "context": "张建科籍贯为岐山县，与岐山县委书记有地缘联系",
        "overlap_org": "",
        "overlap_period": "",
        "confidence": "confirmed",
    },
    {
        "person_a": 2,
        "person_b": 9,
        "type": "hometown_connection",
        "context": "张建科籍贯为岐山县，与岐山县长有地缘联系",
        "overlap_org": "",
        "overlap_period": "",
        "confidence": "confirmed",
    },
]

# ── Person JSONs ─────────────────────────────────────────────────────────────

PERSON_JSON_TEMPLATE = {
    "schema_version": "1.0",
    "generated_at": TODAY,
    "investigation_scope": {
        "province": "陕西省",
        "city": "宝鸡市",
        "region": "岐山县",
        "task_id": "shaanxi_岐山县",
        "time_focus": "2026年7月",
    },
    "identity": {},
    "current_status": {},
    "career_timeline": [],
    "organizations": [],
    "relationships": [],
    "governance_record": [],
    "professional_profile": {},
    "work_style_and_personality": {},
    "network_metrics": {},
    "risk_and_integrity_signals": [],
    "source_register": [],
    "confidence_summary": {},
    "open_questions": [],
}


def build_person_json(person_id: int) -> dict:
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    role_label = p["current_post"]

    person = {
        "identity": {
            "person_id": f"shaanxi_baoji_qishan_{name}",
            "name": name,
            "aliases": [],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "birthplace": p["birthplace"],
            "native_place": "",
            "education": [],
            "party_join": p["party_join"],
            "work_start": p["work_start"],
            "dedupe_keys": {
                "name_birth": f"{name}_{p['birth']}",
                "name_birthplace": f"{name}_{p['birthplace']}",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "县处级正职" if person_id <= 2 else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": person_id == 9,  # only 张建科 is confirmed
            "source_ids": [],
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": p["current_org"],
                "title": p["current_post"],
                "level": "",
                "location": "岐山县" if person_id <= 8 else "宝鸡市渭滨区",
                "system": "party" if person_id == 1 else "government",
                "rank": "县处级正职" if person_id <= 2 else "县处级副职",
                "is_key_promotion": False,
                "notes": p["notes"],
                "confidence": "unverified" if person_id != 9 else "confirmed",
                "source_ids": [],
            }
        ],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
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
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "No risk signals found — name unverified, no records to review",
                "date": AS_OF,
                "confidence": "unverified" if person_id != 9 else "confirmed",
                "source_ids": [],
            }
        ],
        "source_register": [],
        "confidence_summary": {
            "identity": "confirmed" if person_id == 9 else "unverified",
            "current_role": "confirmed" if person_id == 9 else "unverified",
            "career_completeness": "thin" if person_id != 9 else "partial",
            "relationship_confidence": "low",
            "biggest_gap": f"姓名完全未知。因政府网站和公共网络均不可达，{role_label}姓名无法确认。",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"岐山县{role_label}姓名是什么？",
                "why_it_matters": "核心目标人物之一，完整调查必须确认姓名和身份",
                "suggested_queries": [
                    f"岐山县 {p['current_post']}",
                    f"岐山县 领导分工 {p['current_post']}",
                    "岐山县政府 领导之窗",
                    "宝鸡市委组织部 任前公示 岐山",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{name}的出生年月、籍贯、学历和完整履历",
                "why_it_matters": "身份确认后需补充完整履历",
                "suggested_queries": [
                    f"岐山县 {p['current_post']} 简历",
                ],
                "last_attempted": AS_OF,
            },
        ],
    }

    return person


def write_person_json(person_id: int):
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    role_label = p["current_post"]
    safe_role = role_label.replace("、", "_").replace("（", "_").replace("）", "_")
    filename = f"{TODAY}-陕西省-宝鸡市-{safe_role}-{name}.json"
    path = PJSON_DIR / filename

    person_data = build_person_json(person_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(person_data, f, ensure_ascii=False, indent=2)

    return path


# ── Main ─────────────────────────────────────────────────────────────────────


def main():
    # Build DB and GEXF
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

    # Write person JSONs for core leaders (1-8, 9 is bonus context)
    person_files = []
    for pid in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        path = write_person_json(pid)
        person_files.append(str(path))

    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Person JSONs:")
    for pf in person_files:
        print(f"  {pf}")
    print(f"\nNote: Persons 1-8 are '待查_*' — unverified due to web access failure.")
    print(f"      Person 9 (张建科) is a confirmed 岐山籍 leader from existing repo data.")
    print(f"      Government sites (qishan.gov.cn) timed out; Baidu 403; Exa rate-limited.")
    print(f"Done.")


if __name__ == "__main__":
    main()
