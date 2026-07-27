#!/usr/bin/env python3
"""Build 盘锦市兴隆台区 (Panjin Xinglongtai District) leadership network data.

Level: 市辖区
Province: 辽宁省
Parent city: 盘锦市
Targets: 区委书记 (Party Secretary), 区长 (Mayor/District Governor)
Task ID: liaoning_兴隆台区

Research date: 2026-07-25
Official source: https://www.xlt.gov.cn/ (盘锦市兴隆台区人民政府)

Current status (as of 2026-07-25, verified via official government website):

区委领导:
- 尹久辉 — 区委书记。主持九届区委常委会第267次会议(2026-07-23),
  第266次会议(2026-07-17)等; 来源: https://www.xlt.gov.cn/ 新闻
- 祝美娟 — 区委副书记、区长。女,汉族,1974年8月生,研究生学历,中共党员。
  来源: https://www.xlt.gov.cn/12928/ (区政府领导页)

区政府领导 (来源: https://www.xlt.gov.cn/12928/):
- 祝美娟  区委副书记,区长 — 主持区政府全面工作,分管区审计局
- 王德全  区委常委、副区长
- 于湧深  区委常委、副区长
- 宋宁    区委常委、副区长
- 张赫伟  副区长
- 张亚昕  副区长
- 储良    副区长
- 李元鹏  副区长

其他区级领导 (来源: 区委常委会新闻):
- 王春    区人大常委会党组书记、主任
- 原所杰  区政协党组书记、主席

Predecessor info (需进一步核实):
- 尹久辉的详细履历目前公开信息有限，未搜索到百度百科条目
- 祝美娟: 1974年8月生,研究生学历,中共党员。此前曾任兴隆台区区长(从2025年起)
- 前任区委书记: 需进一步核实

Organizations:
- 中共盘锦市兴隆台区委员会  (区委)
- 盘锦市兴隆台区人民政府   (区政府)
- 盘锦市兴隆台区人大常委会 (人大)
- 政协盘锦市兴隆台区委员会 (政协)
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "../../..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "兴隆台区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = datetime.now().strftime("%Y-%m-%d")
TODAY = datetime.now().strftime("%Y%m%d")

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 区委领导 (Party Committee)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "尹久辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴隆台区委书记",
        "current_org": "中共盘锦市兴隆台区委员会",
        "source": ("兴隆台区政府新闻: https://www.xlt.gov.cn/2026_07/24_15/content-569612.html; "
                   "https://www.xlt.gov.cn/2026_07/18_16/content-568859.html"),
    },
    {
        "id": 2,
        "name": "祝美娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1974年8月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴隆台区委副书记、区长",
        "current_org": "盘锦市兴隆台区人民政府",
        "source": ("官方: https://www.xlt.gov.cn/12928/ (区政府领导页); "
                   "2026政府工作报告: https://www.xlt.gov.cn/2026_01/16_16/content-549020.html"),
    },
    # ════════════════════════════════════════
    # 区政府领导 (Government)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "王德全",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴隆台区委常委、副区长",
        "current_org": "盘锦市兴隆台区人民政府",
        "source": "官方: https://www.xlt.gov.cn/12928/",
    },
    {
        "id": 4,
        "name": "于湧深",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴隆台区委常委、副区长",
        "current_org": "盘锦市兴隆台区人民政府",
        "source": "官方: https://www.xlt.gov.cn/12928/",
    },
    {
        "id": 5,
        "name": "宋宁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴隆台区委常委、副区长",
        "current_org": "盘锦市兴隆台区人民政府",
        "source": "官方: https://www.xlt.gov.cn/12928/",
    },
    {
        "id": 6,
        "name": "张赫伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "兴隆台区副区长",
        "current_org": "盘锦市兴隆台区人民政府",
        "source": "官方: https://www.xlt.gov.cn/12928/",
    },
    {
        "id": 7,
        "name": "张亚昕",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "兴隆台区副区长",
        "current_org": "盘锦市兴隆台区人民政府",
        "source": "官方: https://www.xlt.gov.cn/12928/",
    },
    {
        "id": 8,
        "name": "储良",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "兴隆台区副区长",
        "current_org": "盘锦市兴隆台区人民政府",
        "source": "官方: https://www.xlt.gov.cn/12928/",
    },
    {
        "id": 9,
        "name": "李元鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "兴隆台区副区长",
        "current_org": "盘锦市兴隆台区人民政府",
        "source": "官方: https://www.xlt.gov.cn/12928/",
    },
    # ════════════════════════════════════════
    # 人大、政协领导
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "王春",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴隆台区人大常委会党组书记、主任",
        "current_org": "盘锦市兴隆台区人大常委会",
        "source": ("官方新闻: https://www.xlt.gov.cn/2026_07/24_15/content-569612.html; "
                   "https://www.xlt.gov.cn/2026_07/18_16/content-568859.html"),
    },
    {
        "id": 11,
        "name": "原所杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴隆台区政协党组书记、主席",
        "current_org": "政协盘锦市兴隆台区委员会",
        "source": ("官方新闻: https://www.xlt.gov.cn/2026_07/24_15/content-569612.html; "
                   "https://www.xlt.gov.cn/2026_07/18_16/content-568859.html"),
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共盘锦市兴隆台区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共盘锦市委员会",
        "location": "盘锦市兴隆台区",
    },
    {
        "id": 2,
        "name": "盘锦市兴隆台区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "盘锦市人民政府",
        "location": "盘锦市兴隆台区",
    },
    {
        "id": 3,
        "name": "盘锦市兴隆台区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "盘锦市人民代表大会常务委员会",
        "location": "盘锦市兴隆台区",
    },
    {
        "id": 4,
        "name": "政协盘锦市兴隆台区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协盘锦市委员会",
        "location": "盘锦市兴隆台区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS (任职)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 尹久辉
    {"person_id": 1, "org_id": 1, "title": "兴隆台区委书记", "start": "", "end": "present", "rank": "县处级正职", "note": "区委常委会第267次(2026-07-23)、第266次(2026-07-17)主持会议"},
    # 祝美娟
    {"person_id": 2, "org_id": 1, "title": "兴隆台区委副书记", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "兴隆台区区长", "start": "", "end": "present", "rank": "县处级正职", "note": "主持区政府全面工作,分管区审计局; 女,汉族,1974年8月生,研究生"},
    # 王德全
    {"person_id": 3, "org_id": 1, "title": "兴隆台区委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "兴隆台区副区长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 于湧深
    {"person_id": 4, "org_id": 1, "title": "兴隆台区委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "兴隆台区副区长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 宋宁
    {"person_id": 5, "org_id": 1, "title": "兴隆台区委常委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "兴隆台区副区长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 张赫伟
    {"person_id": 6, "org_id": 2, "title": "兴隆台区副区长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 张亚昕
    {"person_id": 7, "org_id": 2, "title": "兴隆台区副区长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 储良
    {"person_id": 8, "org_id": 2, "title": "兴隆台区副区长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 李元鹏
    {"person_id": 9, "org_id": 2, "title": "兴隆台区副区长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 王春
    {"person_id": 10, "org_id": 3, "title": "兴隆台区人大常委会党组书记、主任", "start": "", "end": "present", "rank": "县处级正职", "note": ""},
    # 原所杰
    {"person_id": 11, "org_id": 4, "title": "兴隆台区政协党组书记、主席", "start": "", "end": "present", "rank": "县处级正职", "note": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 党政一把手关系
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "区委书记与区长党政搭档关系",
        "overlap_org": "兴隆台区",
        "overlap_period": "2025-2026",
    },
    # 区委常委关系 (区委+区政府交叉)
    {
        "person_a": 2,
        "person_b": 3,
        "type": "overlap",
        "context": "区长与区委常委、副区长，区政府领导班子",
        "overlap_org": "兴隆台区人民政府",
        "overlap_period": "2025-2026",
    },
    {
        "person_a": 2,
        "person_b": 4,
        "type": "overlap",
        "context": "区长与区委常委、副区长，区政府领导班子",
        "overlap_org": "兴隆台区人民政府",
        "overlap_period": "2025-2026",
    },
    {
        "person_a": 2,
        "person_b": 5,
        "type": "overlap",
        "context": "区长与区委常委、副区长，区政府领导班子",
        "overlap_org": "兴隆台区人民政府",
        "overlap_period": "2025-2026",
    },
    # 副区长与区长
    {
        "person_a": 2,
        "person_b": 6,
        "type": "overlap",
        "context": "区长与副区长，区政府领导班子",
        "overlap_org": "兴隆台区人民政府",
        "overlap_period": "2025-2026",
    },
    {
        "person_a": 2,
        "person_b": 7,
        "type": "overlap",
        "context": "区长与副区长，区政府领导班子",
        "overlap_org": "兴隆台区人民政府",
        "overlap_period": "2025-2026",
    },
    {
        "person_a": 2,
        "person_b": 8,
        "type": "overlap",
        "context": "区长与副区长，区政府领导班子",
        "overlap_org": "兴隆台区人民政府",
        "overlap_period": "2025-2026",
    },
    {
        "person_a": 2,
        "person_b": 9,
        "type": "overlap",
        "context": "区长与副区长，区政府领导班子",
        "overlap_org": "兴隆台区人民政府",
        "overlap_period": "2025-2026",
    },
    # 区委常委会关系
    {
        "person_a": 1,
        "person_b": 3,
        "type": "overlap",
        "context": "区委书记与区委常委，区委常委会",
        "overlap_org": "中共盘锦市兴隆台区委员会",
        "overlap_period": "2025-2026",
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "overlap",
        "context": "区委书记与区委常委，区委常委会",
        "overlap_org": "中共盘锦市兴隆台区委员会",
        "overlap_period": "2025-2026",
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "overlap",
        "context": "区委书记与区委常委，区委常委会",
        "overlap_org": "中共盘锦市兴隆台区委员会",
        "overlap_period": "2025-2026",
    },
    # 人大政协与区委
    {
        "person_a": 1,
        "person_b": 10,
        "type": "overlap",
        "context": "区委书记与区人大常委会主任，区委常委会列席(人大党组书记)",
        "overlap_org": "兴隆台区",
        "overlap_period": "2025-2026",
    },
    {
        "person_a": 1,
        "person_b": 11,
        "type": "overlap",
        "context": "区委书记与区政协主席，区委常委会列席(政协党组书记)",
        "overlap_org": "兴隆台区",
        "overlap_period": "2025-2026",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def write_person_json(person: dict, job_title: str, filename_job: str | None = None) -> str:
    """Write a person JSON file to the staging dir."""
    name = person["name"]
    jt = filename_job or job_title

    person_json = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "盘锦市",
            "region": "兴隆台区",
            "job": job_title,
            "task_id": "liaoning_兴隆台区",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": f"xinglongtai_{name}",
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("native_place", ""),
            "education": [{"period": "", "institution": "", "major": "", "degree": person.get("education", ""), "study_type": "unknown", "source_ids": []}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth', '')}",
                "name_birthplace": f"{name}_{person.get('birthplace', '')}",
                "official_profile_url": person.get("source", ""),
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": bool(person.get("source")),
            "source_ids": [],
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [
            {
                "id": "S001",
                "title": "兴隆台区人民政府官网",
                "url": "https://www.xlt.gov.cn/",
                "publisher": "兴隆台区人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "区政府领导页面及政务动态新闻",
            },
            {
                "id": "S002",
                "title": "区政府领导页面",
                "url": "https://www.xlt.gov.cn/12928/",
                "publisher": "兴隆台区人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "区政府领导职务分工及简历",
            },
        ],
        "confidence_summary": {
            "identity": "partial" if not person.get("birth") else "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "公开履历信息有限，缺少出生地、教育背景、早年工作经历等详细信息" if not person.get("birthplace") else "",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}完整职业履历",
                "why_it_matters": "核心领导缺详细履历，无法分析晋升路径和任职交集",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{name}出生地/籍贯",
                "why_it_matters": "缺少基础身份信息，无法做籍贯网络分析",
                "suggested_queries": [f"{name} 出生 籍贯"],
                "last_attempted": AS_OF,
            },
        ],
    }

    filename = f"{TODAY}-辽宁省-盘锦市-{jt}-{name}.json"
    filepath = _STAGING_DIR / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(person_json, f, ensure_ascii=False, indent=2)

    print(f"  Wrote {filepath}")
    return filename


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    print(f"Building {SLUG} network...")

    # 1. Build database and GEXF
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

    # 2. Verify database
    conn = sqlite3.connect(str(DB_PATH))
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM persons")
        p_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM organizations")
        o_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM positions")
        pos_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM relationships")
        r_count = cur.fetchone()[0]
        print(f"\nDatabase summary: {p_count} persons, {o_count} orgs, {pos_count} positions, {r_count} relationships")
    finally:
        conn.close()

    # 3. Write person JSON files for core leaders
    print("\nWriting person JSON files...")
    write_person_json(persons[0], "兴隆台区委书记", "区委书记")
    write_person_json(persons[1], "兴隆台区委副书记、区长", "区长")

    # 4. Verify GEXF exists
    if GEXF_PATH.exists():
        size_kb = GEXF_PATH.stat().st_size / 1024
        print(f"\nGEXF file: {GEXF_PATH.name} ({size_kb:.1f} KB)")

    print(f"\nDone! All artifacts in {_STAGING_DIR}")


if __name__ == "__main__":
    main()
