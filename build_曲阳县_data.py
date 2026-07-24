#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
曲阳县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 保定市
Region: 曲阳县
Targets: 县委书记 & 县长

Research Sources:
- 曲县人民政府门户网站 (www.quyang.gov.cn) — 运行正常，2026年7月仍有新闻更新
- 县政府网站"领导之窗"确认代县长为刘京
- 县委书记待确认（网站为JS渲染SPA，Weblet无法获取完整内容）

Research Date: 2026-07-24

Research limitations:
  - Exa search API: rate-limited
  - Baidu Baike/Search: 403 blocked
  - Google/Bing: blocked/unreachable
  - Jina Reader: timeout
  - Government site: JS-rendered SPA, only static shell accessible

Confirmed leadership (as of 2026-07-24):
- 代县长: 刘京 — 曲阳县人民政府官网"领导之窗"确认
- 县委书记: 待确认 — 公开搜索受限，未能查证现任县委书记姓名

All unverified biographical details (birth year, birthplace, education, early career)
labeled as such pending deeper research.
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "曲阳县"
TASK_ID = "hebei_曲阳县"
TMP_DIR = _REPO_ROOT / "data" / "tmp" / TASK_ID
AS_OF = "2026-07-24"

DB_PATH = TMP_DIR / f"{SLUG}_network.db"
GEXF_PATH = TMP_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = TMP_DIR


# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 县委领导 (Party Committee)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "待确认县委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "曲阳县委书记（待确认）",
        "current_org": "中共曲阳县委员会",
        "source": "因搜索受限，尚未确认现任县委书记姓名。官方任职时间待查。"
    },
    # ════════════════════════════════════════
    # 县政府领导
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "刘京",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "曲阳县代县长",
        "current_org": "曲阳县人民政府",
        "source": "曲阳县人民政府官网\"领导之窗\"确认 (www.quyang.gov.cn)"
    },
]

# Note: The county government website uses JS rendering (SPA). The leadership
# window only shows 代县长：刘京. The names of deputy mayors and other
# county committee members (县委副书记, 常务副县长, 纪委书记, etc.) could
# not be retrieved due to web access limitations.


# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共曲阳县委员会",
        "type": "党委",
        "level": "县处级",
        "location": "保定市曲阳县"
    },
    {
        "id": 2,
        "name": "曲阳县人民政府",
        "type": "政府",
        "level": "县处级",
        "location": "保定市曲阳县"
    },
    {
        "id": 3,
        "name": "中共保定市委",
        "type": "党委",
        "level": "地市级",
        "location": "保定市"
    },
    {
        "id": 4,
        "name": "保定市人民政府",
        "type": "政府",
        "level": "地市级",
        "location": "保定市"
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 待确认县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记（待确认姓名）", "start": "", "end": "至今", "rank": "正县处级", "note": "现任县委书记姓名待通过更深入检索确认"},

    # 刘京 — 代县长
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "至今", "rank": "正县处级", "note": "兼任县委副书记（推断）"},
    {"person_id": 2, "org_id": 2, "title": "代县长", "start": "", "end": "至今", "rank": "正县处级", "note": "曲阳县人民政府代县长，负责县政府全面工作"},
]


# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 核心关系：县委书记 ↔ 代县长
    {
        "person_a": 1,  # 待确认县委书记
        "person_b": 2,  # 刘京
        "type": "overlap",
        "context": "县委书记与代县长党政正职搭档关系",
        "overlap_org": "中共曲阳县委员会/曲阳县人民政府",
        "overlap_period": "至今"
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# RUN
# ══════════════════════════════════════════════════════════════════════════════

def create_person_json(person: dict) -> None:
    """Create a deep person profile JSON."""
    pid = person["id"]
    name = person["name"]
    job = person["current_post"]

    # Build filename
    name_slug = name
    # Extract a short job title for the filename
    if "县委书记" in job:
        short_job = "县委书记"
    elif "县长" in job and "代" in job:
        short_job = "代县长"
    elif "县长" in job:
        short_job = "县长"
    elif "副县长" in job:
        short_job = "副县长"
    elif "副书记" in job:
        short_job = "县委副书记"
    elif "书记" in job:
        short_job = "书记"
    else:
        short_job = job
    fname = f"{AS_OF}-河北省-保定市-{short_job}-{name_slug}.json"
    fpath = PERSONS_DIR / fname

    # Gather positions for this person
    person_positions = [p for p in positions if p["person_id"] == pid]
    # Gather relationships for this person
    person_rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]

    is_placeholder = "待确认" in name

    identity_fields = {
        "person_id": f"hebei_quyang_{'dai_queren' if is_placeholder else name}_{AS_OF}",
        "name": name,
        "aliases": [],
        "gender": person.get("gender", ""),
        "ethnicity": person.get("ethnicity", ""),
        "birth": person.get("birth", ""),
        "birthplace": person.get("birthplace", ""),
        "native_place": person.get("native_place", ""),
        "education": [],
        "party_join": person.get("party_join", ""),
        "work_start": person.get("work_start", ""),
        "dedupe_keys": {
            "name_birth": f"{name}_",
            "name_birthplace": f"{name}_",
            "official_profile_url": "https://www.quyang.gov.cn/"
        }
    }

    career_timeline = []
    for pos in person_positions:
        org_name = ""
        for o in organizations:
            if o["id"] == pos["org_id"]:
                org_name = o["name"]
                break
        is_party = "委" in org_name and "管" not in org_name
        career_timeline.append({
            "start": pos.get("start", ""),
            "end": pos.get("end", ""),
            "org": org_name,
            "title": pos["title"],
            "level": pos.get("rank", ""),
            "location": "保定市曲阳县",
            "system": "party" if is_party else "government",
            "rank": pos.get("rank", ""),
            "is_key_promotion": True,
            "notes": pos.get("note", ""),
            "confidence": "unverified" if is_placeholder else "confirmed",
            "source_ids": ["S001"]
        })

    rel_list = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other_name = ""
        for p in persons:
            if p["id"] == other_id:
                other_name = p["name"]
                break
        rel_list.append({
            "person": other_name,
            "person_id": f"hebei_quyang_{other_name}_{AS_OF}",
            "relationship_type": r.get("type", ""),
            "strength": "strong",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if not is_placeholder else "unverified",
            "source_ids": ["S001"]
        })

    is_core = pid in (1, 2)
    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河北省",
            "city": "保定市",
            "region": "曲阳县",
            "job": job,
            "task_id": "hebei_曲阳县",
            "time_focus": "2025-2026"
        },
        "identity": identity_fields,
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正县处级",
            "as_of": AS_OF,
            "is_current_confirmed": False if is_placeholder else True,
            "source_ids": ["S001"]
        },
        "career_timeline": career_timeline,
        "organizations": [o["name"] for o in organizations],
        "relationships": rel_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["party", "government"] if is_core else [],
            "geographic_pattern": ["曲阳县"],
            "promotion_velocity": {
                "summary": "",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {
            "direct_connections": len(person_rels),
            "organization_count": len(set(p["org_id"] for p in person_positions)),
            "centrality_estimate": "high" if is_core else "medium"
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": f"{'未搜索到公开信息' if is_placeholder else '未发现公开的纪律处分、审计问题或负面报道'}",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "曲阳县人民政府门户网站",
                "url": "https://www.quyang.gov.cn/",
                "publisher": "曲阳县人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "县政府官网\"领导之窗\"确认代县长为刘京"
            }
        ],
        "confidence_summary": {
            "identity": "unverified" if is_placeholder else "plausible",
            "current_role": "unverified" if is_placeholder else "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "现任县委书记姓名未确认；所有人物缺少出生年份、籍贯、教育背景和完整履历信息"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"现任曲阳县委书记姓名？",
                "why_it_matters": "县委书记是一把手，是关系网络的核心节点",
                "suggested_queries": ["曲阳县 县委书记 现任", "曲阳县委 书记 保定 任职"],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": f"{'刘京' if not is_placeholder else name}的出生年份和籍贯？",
                "why_it_matters": "核心身份标识字段，用于去重和跨地区网络关联",
                "suggested_queries": [f"{'刘京' if not is_placeholder else name} 曲阳 简历", f"{'刘京' if not is_placeholder else name} 出生"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"{'刘京' if not is_placeholder else name}的完整履历（历任职务及时间线）？",
                "why_it_matters": "构建完整职业生涯时间线，识别跨地区调动和系统内转岗",
                "suggested_queries": [f"{'刘京' if not is_placeholder else name} 任职", f"{'刘京' if not is_placeholder else name} 工作经历"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "曲阳县县委常委领导班子完整名单？",
                "why_it_matters": "党委班子成员是关系网络的重要节点",
                "suggested_queries": ["曲阳县委领导班子", "曲阳县 县委常委"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "曲阳县副县长及其他政府领导班子成员？",
                "why_it_matters": "县政府/人大/政协领导班子构成",
                "suggested_queries": ["曲阳县 副县长 分工", "曲阳县 领导分工"],
                "last_attempted": AS_OF
            }
        ]
    }

    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath}")


if __name__ == "__main__":
    TMP_DIR.mkdir(parents=True, exist_ok=True)

    # Run main build
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Create person JSON for each person
    for p in persons:
        create_person_json(p)

    print(f"\nDone: {SLUG}")
    print(f"  DB:      {DB_PATH}")
    print(f"  GEXF:    {GEXF_PATH}")
    print(f"  Persons: {PERSONS_DIR}")
