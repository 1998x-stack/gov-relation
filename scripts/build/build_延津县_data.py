#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 延津县 (Yanjin County), 新乡市, 河南省.

Investigation date: 2026-07-24
Task ID: henan_延津县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - No direct web access available (Exa rate-limited, Baidu 403/CAPTCHA,
    government site yanjin.gov.cn timed out, Jina Reader timed out)
  - Existing repo artifact: build_新乡市_data.py confirms 延津县 is under 新乡市
  - Source_fallbacks.md guidelines applied: partial-evidence artifact mode

Confidence notes:
  - Web access was fully degraded during this investigation. All biographical
    fields (names, genders, ethnicities, birth dates, education, party membership,
    career histories) are UNVERIFIED.
  - The build script, DB, GEXF, and person JSONs are structurally valid but
    contain placeholder data with explicit uncertainty markers.
  - Core leader names are NOT confirmed from any accessible source.
  - This is a partial-evidence artifact — all claims should be treated as
    "unverified" until confirmed via official government channels.
"""

from __future__ import annotations

import json
import os
import shutil
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "延津县"
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
# ⚠ ALL BIOGRAPHICAL DATA IS UNVERIFIED due to complete web access degradation.
# Names are placeholders — real names need to be confirmed via yanjin.gov.cn
# or official 新乡市 organization department notices.

persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "",        # UNVERIFIED — needs confirmation
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共延津县委员会",
        "source": ""
    },
    {
        "id": 2,
        "name": "",        # UNVERIFIED — needs confirmation
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县长",
        "current_org": "延津县人民政府",
        "source": ""
    },
    # ═══════ 副县长 (deputy mayors) — UNVERIFIED ═══════
    # Positions exist structurally even with unknown names
    {
        "id": 3,
        "name": "",        # UNVERIFIED
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "延津县人民政府",
        "source": ""
    },
    {
        "id": 4,
        "name": "",        # UNVERIFIED
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "延津县人民政府",
        "source": ""
    },
    {
        "id": 5,
        "name": "",        # UNVERIFIED
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "延津县人民政府",
        "source": ""
    },
    {
        "id": 6,
        "name": "",        # UNVERIFIED
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "延津县人民政府",
        "source": ""
    },
    {
        "id": 7,
        "name": "",        # UNVERIFIED
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "延津县人民政府",
        "source": ""
    },
    # ═══════ 县委常委 (Standing Committee members) — UNVERIFIED ═══════
    {
        "id": 8,
        "name": "",        # UNVERIFIED — 县委副书记
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共延津县委员会",
        "source": ""
    },
    {
        "id": 9,
        "name": "",        # UNVERIFIED — 常务副县长
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "延津县人民政府",
        "source": ""
    },
    {
        "id": 10,
        "name": "",        # UNVERIFIED — 纪委书记
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、纪委书记",
        "current_org": "中共延津县纪律检查委员会",
        "source": ""
    },
    {
        "id": 11,
        "name": "",        # UNVERIFIED — 组织部长
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共延津县委员会组织部",
        "source": ""
    },
    {
        "id": 12,
        "name": "",        # UNVERIFIED — 政法委书记
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共延津县委员会政法委员会",
        "source": ""
    },
    {
        "id": 13,
        "name": "",        # UNVERIFIED — 宣传部长
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "work_start": "",
        "party_join": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共延津县委员会宣传部",
        "source": ""
    },
    {
        "id": 14,
        "name": "",        # UNVERIFIED — 统战部长
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共延津县委员会统战部",
        "source": ""
    },
    # ═══════ 前任 Predecessors — UNVERIFIED ═══════
    {
        "id": 15,
        "name": "",        # UNVERIFIED — 前任县委书记
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任县委书记",
        "current_org": "中共延津县委员会",
        "source": ""
    },
    {
        "id": 16,
        "name": "",        # UNVERIFIED — 前任县长
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任县长",
        "current_org": "延津县人民政府",
        "source": ""
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共延津县委员会", "type": "党委", "level": "县级", "parent": "中共新乡市委员会", "location": "延津县"},
    {"id": 2, "name": "延津县人民政府", "type": "政府", "level": "县级", "parent": "新乡市人民政府", "location": "延津县"},
    {"id": 3, "name": "中共延津县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共新乡市纪律检查委员会", "location": "延津县"},
    {"id": 4, "name": "中共延津县委员会组织部", "type": "党委", "level": "县级", "parent": "中共延津县委员会", "location": "延津县"},
    {"id": 5, "name": "中共延津县委员会政法委员会", "type": "党委", "level": "县级", "parent": "中共延津县委员会", "location": "延津县"},
    {"id": 6, "name": "中共延津县委员会宣传部", "type": "党委", "level": "县级", "parent": "中共延津县委员会", "location": "延津县"},
    {"id": 7, "name": "中共延津县委员会统战部", "type": "党委", "level": "县级", "parent": "中共延津县委员会", "location": "延津县"},
    {"id": 8, "name": "延津县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "新乡市人民代表大会常务委员会", "location": "延津县"},
    {"id": 9, "name": "中国人民政治协商会议延津县委员会", "type": "政协", "level": "县级", "parent": "政协新乡市委员会", "location": "延津县"},
]

# ── Positions (person → org with title) ────────────────────────────────────
positions = [
    # 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 县长
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 副县长
    {"person_id": 3, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 县委副书记
    {"person_id": 8, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 常务副县长
    {"person_id": 9, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 纪委书记
    {"person_id": 10, "org_id": 3, "title": "县委常委、纪委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 组织部长
    {"person_id": 11, "org_id": 4, "title": "县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 政法委书记
    {"person_id": 12, "org_id": 5, "title": "县委常委、政法委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 宣传部长
    {"person_id": 13, "org_id": 6, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 统战部长
    {"person_id": 14, "org_id": 7, "title": "县委常委、统战部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 前任县委书记
    {"person_id": 15, "org_id": 1, "title": "前任县委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 前任县长
    {"person_id": 16, "org_id": 2, "title": "前任县长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 县委书记 ↔ 县长（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记与县长为延津县党政正职搭档", "overlap_org": "延津县", "overlap_period": ""},
    # 县长 ↔ 副县长（政府班子）
    {"person_a": 2, "person_b": 3, "type": "政府班子", "context": "副县长在县长领导下工作", "overlap_org": "延津县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "政府班子", "context": "副县长在县长领导下工作", "overlap_org": "延津县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "政府班子", "context": "副县长在县长领导下工作", "overlap_org": "延津县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "政府班子", "context": "副县长在县长领导下工作", "overlap_org": "延津县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "政府班子", "context": "副县长在县长领导下工作", "overlap_org": "延津县人民政府", "overlap_period": ""},
    # 县委书记 ↔ 县委副书记
    {"person_a": 1, "person_b": 8, "type": "党政班子", "context": "县委副书记协助县委书记工作", "overlap_org": "中共延津县委员会", "overlap_period": ""},
    # 县委书记 ↔ 常务副县长
    {"person_a": 1, "person_b": 9, "type": "党政班子", "context": "常务副县长为县委常委", "overlap_org": "中共延津县委员会", "overlap_period": ""},
    # 县委书记 ↔ 纪委书记
    {"person_a": 1, "person_b": 10, "type": "党政班子", "context": "纪委书记为县委常委", "overlap_org": "中共延津县委员会", "overlap_period": ""},
    # 县委书记 ↔ 组织部长
    {"person_a": 1, "person_b": 11, "type": "党政班子", "context": "组织部长为县委常委", "overlap_org": "中共延津县委员会", "overlap_period": ""},
    # 县委书记 ↔ 政法委书记
    {"person_a": 1, "person_b": 12, "type": "党政班子", "context": "政法委书记为县委常委", "overlap_org": "中共延津县委员会", "overlap_period": ""},
    # 县委书记 ↔ 宣传部长
    {"person_a": 1, "person_b": 13, "type": "党政班子", "context": "宣传部长为县委常委", "overlap_org": "中共延津县委员会", "overlap_period": ""},
    # 县委书记 ↔ 统战部长
    {"person_a": 1, "person_b": 14, "type": "党政班子", "context": "统战部长为县委常委", "overlap_org": "中共延津县委员会", "overlap_period": ""},
    # 前任 ↔ 现任 县委书记
    {"person_a": 15, "person_b": 1, "type": "交接", "context": "前任县委书记与现任县委书记交接", "overlap_org": "中共延津县委员会", "overlap_period": ""},
    # 前任 ↔ 现任 县长
    {"person_a": 16, "person_b": 2, "type": "交接", "context": "前任县长与现任县长交接", "overlap_org": "延津县人民政府", "overlap_period": ""},
    # 县委常委间同僚关系
    {"person_a": 8, "person_b": 9, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共延津县委员会", "overlap_period": ""},
    {"person_a": 8, "person_b": 10, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共延津县委员会", "overlap_period": ""},
    {"person_a": 8, "person_b": 11, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共延津县委员会", "overlap_period": ""},
    {"person_a": 8, "person_b": 12, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共延津县委员会", "overlap_period": ""},
    {"person_a": 8, "person_b": 13, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共延津县委员会", "overlap_period": ""},
    {"person_a": 8, "person_b": 14, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共延津县委员会", "overlap_period": ""},
    {"person_a": 9, "person_b": 10, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共延津县委员会", "overlap_period": ""},
    {"person_a": 9, "person_b": 11, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共延津县委员会", "overlap_period": ""},
    {"person_a": 9, "person_b": 12, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共延津县委员会", "overlap_period": ""},
    {"person_a": 9, "person_b": 13, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共延津县委员会", "overlap_period": ""},
    {"person_a": 9, "person_b": 14, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共延津县委员会", "overlap_period": ""},
    {"person_a": 10, "person_b": 11, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共延津县委员会", "overlap_period": ""},
    {"person_a": 10, "person_b": 12, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共延津县委员会", "overlap_period": ""},
    {"person_a": 10, "person_b": 13, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共延津县委员会", "overlap_period": ""},
    {"person_a": 10, "person_b": 14, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共延津县委员会", "overlap_period": ""},
    {"person_a": 11, "person_b": 12, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共延津县委员会", "overlap_period": ""},
    {"person_a": 11, "person_b": 13, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共延津县委员会", "overlap_period": ""},
    {"person_a": 11, "person_b": 14, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共延津县委员会", "overlap_period": ""},
    {"person_a": 12, "person_b": 13, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共延津县委员会", "overlap_period": ""},
    {"person_a": 12, "person_b": 14, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共延津县委员会", "overlap_period": ""},
    {"person_a": 13, "person_b": 14, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共延津县委员会", "overlap_period": ""},
]


# ── Main ────────────────────────────────────────────────────────────────────
def main() -> None:
    sys.path.insert(0, str(BASE))
    from gov_relation.runner import run_build

    print(f"Building {SLUG} network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")
    print(f"  AS OF:    {AS_OF}")
    print(f"  ⚠ NOTE: All biographical data is UNVERIFIED due to complete web access degradation.")
    print(f"  ⚠ NOTE: Person names are placeholders until confirmed via yanjin.gov.cn.")

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

    # Write person JSON files for core leaders (IDs 1 & 2)
    person_files = [
        {
            "id": 1,
            "name": "待确认",    # placeholder
            "job": "县委书记",
            "data": {
                "schema_version": "1.0",
                "generated_at": AS_OF,
                "investigation_scope": {
                    "province": "河南省",
                    "city": "新乡市",
                    "region": "延津县",
                    "job": "县委书记",
                    "task_id": "henan_延津县",
                    "time_focus": "2026"
                },
                "identity": {
                    "person_id": "yanjin_secretary",
                    "name": "待确认",
                    "gender": "",
                    "ethnicity": "",
                    "birth": "",
                    "birthplace": "",
                    "education": [],
                    "party_join": "",
                    "work_start": ""
                },
                "current_status": {
                    "current_post": "县委书记",
                    "current_org": "中共延津县委员会",
                    "administrative_rank": "正处级",
                    "as_of": AS_OF,
                    "is_current_confirmed": False,
                    "source_ids": []
                },
                "career_timeline": [],
                "organizations": [],
                "relationships": [
                    {
                        "person": "待确认",
                        "person_id": "yanjin_mayor",
                        "relationship_type": "overlap",
                        "strength": "strong",
                        "evidence": "县委书记与县长为延津县党政正职搭档（结构关系，姓名未确认）",
                        "overlap_org": "延津县",
                        "confidence": "unverified",
                        "source_ids": []
                    }
                ],
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
                "risk_and_integrity_signals": [
                    {"type": "none_found", "description": "未发现负面信息（因网络受限，搜索范围有限）", "date": AS_OF, "confidence": "unverified"}
                ],
                "source_register": [],
                "confidence_summary": {
                    "identity": "unverified",
                    "current_role": "unverified",
                    "career_completeness": "thin",
                    "relationship_confidence": "low",
                    "biggest_gap": "所有信息均未确认——县委书记姓名、履历籍贯、教育背景完全未知"
                },
                "open_questions": [
                    {
                        "priority": "critical",
                        "question": "延津县现任县委书记是谁？姓名、出生年份、籍贯、教育背景、完整履历？",
                        "why_it_matters": "作为当前一把手，其身份是本次调查的核心目标",
                        "suggested_queries": ["延津县 县委书记 现任", "延津县 书记 简历", "site:yanjin.gov.cn 书记"],
                        "last_attempted": AS_OF
                    },
                    {
                        "priority": "critical",
                        "question": "现任县委书记何时上任？前任是谁？前任去了哪里？",
                        "why_it_matters": "了解政治交接和跨区域调动网络",
                        "suggested_queries": ["延津县 前任 县委书记", "延津县 书记 任职时间"],
                        "last_attempted": AS_OF
                    }
                ]
            }
        },
        {
            "id": 2,
            "name": "待确认",    # placeholder
            "job": "县长",
            "data": {
                "schema_version": "1.0",
                "generated_at": AS_OF,
                "investigation_scope": {
                    "province": "河南省",
                    "city": "新乡市",
                    "region": "延津县",
                    "job": "县长",
                    "task_id": "henan_延津县",
                    "time_focus": "2026"
                },
                "identity": {
                    "person_id": "yanjin_mayor",
                    "name": "待确认",
                    "gender": "",
                    "ethnicity": "",
                    "birth": "",
                    "birthplace": "",
                    "education": [],
                    "party_join": "",
                    "work_start": ""
                },
                "current_status": {
                    "current_post": "县长",
                    "current_org": "延津县人民政府",
                    "administrative_rank": "正处级",
                    "as_of": AS_OF,
                    "is_current_confirmed": False,
                    "source_ids": []
                },
                "career_timeline": [],
                "organizations": [],
                "relationships": [
                    {
                        "person": "待确认",
                        "person_id": "yanjin_secretary",
                        "relationship_type": "overlap",
                        "strength": "strong",
                        "evidence": "县长与县委书记为延津县党政正职搭档（结构关系，姓名未确认）",
                        "overlap_org": "延津县",
                        "confidence": "unverified",
                        "source_ids": []
                    }
                ],
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
                "risk_and_integrity_signals": [
                    {"type": "none_found", "description": "未发现负面信息（因网络受限，搜索范围有限）", "date": AS_OF, "confidence": "unverified"}
                ],
                "source_register": [],
                "confidence_summary": {
                    "identity": "unverified",
                    "current_role": "unverified",
                    "career_completeness": "thin",
                    "relationship_confidence": "low",
                    "biggest_gap": "所有信息均未确认——县长姓名、履历、籍贯、教育背景完全未知"
                },
                "open_questions": [
                    {
                        "priority": "critical",
                        "question": "延津县现任县长是谁？姓名、出生年份、籍贯、教育背景、完整履历？",
                        "why_it_matters": "作为县政府一把手，其身份是本次调查的核心目标",
                        "suggested_queries": ["延津县 县长 现任", "延津县 县长 简历", "site:yanjin.gov.cn 县长"],
                        "last_attempted": AS_OF
                    },
                    {
                        "priority": "critical",
                        "question": "现任县长何时上任？前任是谁？前任去了哪里？",
                        "why_it_matters": "了解政府领导交接和市县交流网络",
                        "suggested_queries": ["延津县 前任 县长", "延津县 县长 任职时间"],
                        "last_attempted": AS_OF
                    }
                ]
            }
        },
    ]

    for pf in person_files:
        fname = f"{TODAY}-河南省-新乡市-{pf['job']}-{pf['name']}.json"
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

    for pf in person_files:
        src = PERSONS_DIR / f"{TODAY}-河南省-新乡市-{pf['job']}-{pf['name']}.json"
        dst = CANONICAL_PERSONS / src.name
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  ✅ Canonical person JSON: {dst}")

    print(f"\n📦 Canonical build script: {CANONICAL_BUILD}")
    print(f"📦 Canonical DB: {CANONICAL_DB}")
    print(f"📦 Canonical GEXF: {CANONICAL_GEXF}")
    print(f"\n⚠ NOTE: All data is UNVERIFIED due to complete web access degradation.")
    print(f"⚠ Names, biographies, and relationships need confirmation from:")
    print(f"⚠   - https://www.yanjin.gov.cn/ldzc/")
    print(f"⚠   - 新乡市 组织部 任前公示")
    print(f"⚠   - Baidu Baike")
    print(f"\n✅ Done — {SLUG} data build complete (partial-evidence mode).")


if __name__ == "__main__":
    main()
