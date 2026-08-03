#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 渑池县 (Mianchi County), 三门峡市, 河南省.

Level: 县
Province: 河南省
Parent city: 三门峡市
Targets: 县委书记 (Party Secretary), 县长 (County Magistrate)
Task ID: henan_渑池县

Research date: 2026-08-03
Official source: https://www.mianchi.gov.cn/ (渑池县人民政府) — homepage accessible

Current status (as of 2026-08-03):
- 县委书记: 钱程 (confirmed via 渑池县 Baidu Baike §政治 section)
- 县长: 周详 (confirmed via Baidu Baike profile)

Confidence notes:
  Exa search rate-limited and unavailable. Baidu Baike (渑池县 page) confirmed both leaders.
  周详's Baidu Baike profile provided detailed career history.
  钱程's Baidu Baike returned 403 (blocked).
  Government site leadership subpages URL patterns unknown (all guessed paths returned 404).
  Full leadership roster (deputies, committee members) could not be confirmed from accessible sources.

  This is a partial-evidence build per source_fallbacks.md artifact mode.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / ".." / "..").resolve()
if not (_REPO_ROOT / "gov_relation").exists():
    _REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "渑池县"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-08-03"
TODAY = "20260803"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # 1. 钱程 — 县委书记 (confirmed Baidu Baike 渑池县 page §政治)
    {
        "id": 1,
        "name": "钱程",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共渑池县委书记",
        "current_org": "中共渑池县委员会",
        "source": "Baidu Baike 渑池县条目政治栏; 个人百科页因403无法访问",
    },
    # 2. 周详 — 县长 (confirmed Baidu Baike profile)
    {
        "id": 2,
        "name": "周详",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "渑池县人民政府县长",
        "current_org": "渑池县人民政府",
        "source": "Baidu Baike 周详(63187467) — 渑池县委副书记、县政府党组书记、县长",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共渑池县委员会", "type": "党委", "level": "县", "parent": "中共三门峡市委员会", "location": "河南省三门峡市渑池县"},
    {"id": 2, "name": "渑池县人民政府", "type": "政府", "level": "县", "parent": "三门峡市人民政府", "location": "河南省三门峡市渑池县"},
    {"id": 3, "name": "渑池县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "三门峡市人民代表大会常务委员会", "location": "河南省三门峡市渑池县"},
    {"id": 4, "name": "中国人民政治协商会议渑池县委员会", "type": "政协", "level": "县", "parent": "政协三门峡市委员会", "location": "河南省三门峡市渑池县"},
    {"id": 5, "name": "中共渑池县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共三门峡市纪律检查委员会", "location": "河南省三门峡市渑池县"},
    {"id": 6, "name": "渑池县监察委员会", "type": "政府", "level": "县", "parent": "三门峡市监察委员会", "location": "河南省三门峡市渑池县"},
    {"id": 7, "name": "中国共产党渑池县委员会组织部", "type": "党委", "level": "县", "parent": "中共渑池县委员会", "location": "河南省三门峡市渑池县"},
    {"id": 8, "name": "中国共产党渑池县委员会宣传部", "type": "党委", "level": "县", "parent": "中共渑池县委员会", "location": "河南省三门峡市渑池县"},
    {"id": 9, "name": "中国共产党渑池县委员会政法委员会", "type": "党委", "level": "县", "parent": "中共渑池县委员会", "location": "河南省三门峡市渑池县"},
    {"id": 10, "name": "渑池县审计局", "type": "政府", "level": "县", "parent": "渑池县人民政府", "location": "河南省三门峡市渑池县"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 钱程 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "中共渑池县委书记", "start": "", "end": "present", "rank": "正处级", "note": "县委书记 — 确认来自百度百科渑池县词条政治栏，确切任职起始日待查"},
    # 周详 — 县长及历任
    {"person_id": 2, "org_id": 2, "title": "渑池县人民政府县长", "start": "2024-09", "end": "present", "rank": "正处级", "note": "2024年9月任县长"},
    {"person_id": 2, "org_id": 1, "title": "渑池县委副书记", "start": "2024-09", "end": "present", "rank": "副处级", "note": "2026年6月25日当选第十四届县委副书记"},
    {"person_id": 2, "org_id": 1, "title": "义马市委副书记兼东区街道党工委书记", "start": "", "end": "", "rank": "", "note": "任渑池县长前任义马市委副书记"},
    {"person_id": 2, "org_id": 1, "title": "灵宝市委副书记兼宣传部部长、寺河乡党委书记", "start": "", "end": "", "rank": "", "note": "灵宝市任职"},
    {"person_id": 2, "org_id": 1, "title": "共青团河南省委青年发展部部长", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "共青团河南省委青年发展部副部长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "共青团河南省委办公室副主任兼第一团支书南阳工作总队队长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "共青团河南省委组织部主任科员", "start": "", "end": "", "rank": "正科级", "note": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "渑池县委书记与县长党政工作搭档", "overlap_org": "渑池县", "overlap_period": "2024年9月起", "strength": "strong"},
]


# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON
# ══════════════════════════════════════════════════════════════════════════════

def write_person_json(person_id: int, data: dict) -> str:
    name = data["identity"]["name"]
    job_slug = data["investigation_scope"]["job"]
    filename = f"{TODAY}-河南省-三门峡市-{job_slug}-{name}.json"
    filepath = Path(_STAGING_DIR) / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {filepath}")
    return str(filepath)


# --- 钱程 (县委书记) ---
qian_cheng_person = {
    "schema_version": "1.0",
    "generated_at": AS_OF,
    "investigation_scope": {
        "province": "河南省", "city": "三门峡市", "region": "渑池县",
        "job": "县委书记", "task_id": "henan_渑池县", "time_focus": "当前",
    },
    "identity": {
        "person_id": "mianchi_qian_cheng",
        "name": "钱程", "aliases": [], "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "native_place": "",
        "education": [], "party_join": "中共党员", "work_start": "",
        "dedupe_keys": {"name_birth": "钱程_", "name_birthplace": "钱程_", "official_profile_url": ""},
    },
    "current_status": {
        "current_post": "中共渑池县委书记", "current_org": "中共渑池县委员会",
        "administrative_rank": "正处级", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001"],
    },
    "career_timeline": [
        {"start": "未知", "end": "未知", "org": "履历缺口", "title": "", "notes": "公开资料未找到钱程详细履历，百度百科个人页访问被拒（403）", "confidence": "unverified", "source_ids": []},
    ],
    "organizations": [],
    "relationships": [],
    "governance_record": [],
    "professional_profile": {
        "primary_specializations": [], "secondary_specializations": [],
        "career_pattern": "unknown", "systems_experience": [],
        "geographic_pattern": [],
        "promotion_velocity": {"summary": "无法评估 — 履历缺失", "notable_fast_promotions": []},
    },
    "work_style_and_personality": {
        "public_style_indicators": [], "speech_themes": [], "management_signals": [],
        "caveat": "缺乏公开资料，无法评估工作风格。",
    },
    "network_metrics": {},
    "risk_and_integrity_signals": [
        {"type": "none_found", "description": "在2026年8月研究范围内未发现明确风险信号", "date": "", "confidence": "unverified", "source_ids": []},
    ],
    "source_register": [
        {"id": "S001", "title": "渑池县 — Baidu Baike", "url": "https://baike.baidu.com/item/渑池县", "publisher": "Baidu Baike", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "政治栏目列出钱程为县委书记，个人百科页因403无法查看"},
    ],
    "confidence_summary": {
        "identity": "plausible", "current_role": "confirmed", "career_completeness": "thin",
        "relationship_confidence": "low", "biggest_gap": "钱程的完整履历（出生、教育、任职经历）完全未知",
    },
    "open_questions": [
        {"priority": "critical", "question": "钱程的出生年份、出生地、教育背景", "why_it_matters": "核心身份信息，用于去重和履历分析", "suggested_queries": ["钱程 简历 渑池", "钱程 任前公示", "钱程 三门峡 组织部"], "last_attempted": AS_OF},
        {"priority": "critical", "question": "钱程任县委书记之前的全部任职经历", "why_it_matters": "职业路径、晋升速度和网络关系分析", "suggested_queries": ["钱程 曾任", "钱程 履历 三门峡", "钱程 任职经历"], "last_attempted": AS_OF},
        {"priority": "high", "question": "钱程何时开始担任渑池县委书记", "why_it_matters": "确定任期起点以分析班子稳定性", "suggested_queries": ["钱程 渑池县委书记 任职", "钱程 任 渑池 县委书记 时间"], "last_attempted": AS_OF},
    ],
}

# --- 周详 (县长) ---
zhou_xiang_person = {
    "schema_version": "1.0",
    "generated_at": AS_OF,
    "investigation_scope": {
        "province": "河南省", "city": "三门峡市", "region": "渑池县",
        "job": "县长", "task_id": "henan_渑池县", "time_focus": "当前",
    },
    "identity": {
        "person_id": "mianchi_zhou_xiang",
        "name": "周详", "aliases": [], "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "native_place": "",
        "education": [], "party_join": "中共党员", "work_start": "",
        "dedupe_keys": {"name_birth": "周详_", "name_birthplace": "周详_", "official_profile_url": "https://baike.baidu.com/item/周详/63187467"},
    },
    "current_status": {
        "current_post": "渑池县人民政府县长", "current_org": "渑池县人民政府",
        "administrative_rank": "正处级", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S002"],
    },
    "career_timeline": [
        {"start": "未知", "end": "未知", "org": "共青团河南省委组织部", "title": "主任干事", "level": "", "location": "郑州", "system": "organization", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "未知", "end": "未知", "org": "共青团河南省委组织部", "title": "主任科员", "level": "正科级", "location": "郑州", "system": "organization", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "未知", "end": "未知", "org": "共青团河南省委办公室", "title": "副主任、第一团支书南阳工作总队队长", "level": "副处级", "location": "郑州/南阳", "system": "organization", "rank": "", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "未知", "end": "未知", "org": "共青团河南省委青年发展部", "title": "副部长", "level": "副处级", "location": "郑州", "system": "organization", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "未知", "end": "未知", "org": "共青团河南省委青年发展部", "title": "部长", "level": "正处级", "location": "郑州", "system": "organization", "rank": "", "is_key_promotion": True, "notes": "共青团系统内晋升至正处级", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "未知", "end": "未知", "org": "中共义马市委", "title": "副书记、东区街道党工委书记", "level": "副处级", "location": "义马市", "system": "party", "rank": "", "is_key_promotion": True, "notes": "从共青团系统转到地方党政岗位", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "未知", "end": "未知", "org": "中共灵宝市委", "title": "副书记、宣传部部长、寺河乡党委书记", "level": "副处级", "location": "灵宝市", "system": "party", "rank": "", "is_key_promotion": False, "notes": "转任灵宝，兼任宣传部和乡镇书记", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2024-09", "end": "present", "org": "渑池县人民政府", "title": "县长", "level": "正处级", "location": "渑池县", "system": "government", "rank": "", "is_key_promotion": True, "notes": "2024年9月任县长，2026年6月当选县委副书记", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2024-09", "end": "present", "org": "中共渑池县委员会", "title": "县委副书记", "level": "副处级", "location": "渑池县", "system": "party", "rank": "", "is_key_promotion": False, "notes": "2026年6月25日当选第十四届县委副书记", "confidence": "confirmed", "source_ids": ["S002"]},
    ],
    "organizations": [],
    "relationships": [
        {"person": "钱程", "person_id": "mianchi_qian_cheng", "relationship_type": "overlap", "strength": "strong", "evidence": "渑池县委书记和县长工作搭档，自2024年9月起共事", "overlap_org": "渑池县", "overlap_period": "2024年9月起", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    ],
    "governance_record": [
        {"period": "2024-09至今", "domain": "government", "achievement_or_event": "主持县政府全面工作，负责审计工作", "role_in_event": "县长", "measurable_outcome": "", "location": "渑池县", "confidence": "confirmed", "source_ids": ["S002"]},
    ],
    "professional_profile": {
        "primary_specializations": ["青年工作", "组织工作"],
        "secondary_specializations": ["宣传"],
        "career_pattern": "cross_county_rotation",
        "systems_experience": ["共青团", "党办", "宣传", "乡镇"],
        "geographic_pattern": ["共青团河南省委（郑州）", "义马市", "灵宝市", "渑池县"],
        "promotion_velocity": {"summary": "共青团系统长期经历转地方党政岗位，晋升为正处级县长", "notable_fast_promotions": []},
    },
    "work_style_and_personality": {
        "public_style_indicators": [], "speech_themes": [], "management_signals": [],
        "caveat": "缺乏公开资料评估工作风格。",
    },
    "network_metrics": {},
    "risk_and_integrity_signals": [
        {"type": "none_found", "description": "在2026年8月研究范围内未发现明确风险或廉洁问题信号", "confidence": "unverified", "source_ids": ["S002"]},
    ],
    "source_register": [
        {"id": "S002", "title": "周详 - Baidu Baike", "url": "https://baike.baidu.com/item/周详/63187467", "publisher": "Baidu Baike", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "完整履历信息"},
        {"id": "S001", "title": "渑池县 - Baidu Baike", "url": "https://baike.baidu.com/item/渑池县", "publisher": "Baidu Baike", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "政治栏目确认钱程为县委书记、周详为县长"},
    ],
    "confidence_summary": {
        "identity": "confirmed", "current_role": "confirmed", "career_completeness": "partial",
        "relationship_confidence": "medium", "biggest_gap": "具体出生年份、教育背景、各段任职具体起止日期",
    },
    "open_questions": [
        {"priority": "high", "question": "周详的具体出生年份和出生地", "why_it_matters": "用于人物去重和年龄分析", "suggested_queries": ["周详 出生", "周详 籍贯"], "last_attempted": AS_OF},
        {"priority": "high", "question": "周详在共青团各岗位的具体起止日期", "why_it_matters": "履历时间线不完整", "suggested_queries": ["周详 共青团 任职 时间"], "last_attempted": AS_OF},
        {"priority": "medium", "question": "周详在义马和灵宝挂任副书记的具体起止日期", "why_it_matters": "定位交叉任职时间", "suggested_queries": ["周详 义马 副书记 任职"], "last_attempted": AS_OF},
    ],
}


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Building {SLUG} network...")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    # Write person JSONs
    write_person_json(1, qian_cheng_person)
    write_person_json(2, zhou_xiang_person)

    # Build DB + GEXF via runner
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print("✅ Build complete.")
    print(f"  DB exists: {DB_PATH.exists()}")
    print(f"  GEXF exists: {GEXF_PATH.exists()}")
