#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 二连浩特市 (Erenhot City), 锡林郭勒盟, 内蒙古自治区.

Investigation date: 2026-07-25
Task ID: inner_mongolia_二连浩特市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - www.elht.gov.cn — 二连浩特市人民政府官方网站 (primary, current as of July 2026)
  - Baidu Baike — 二连浩特市 overview

Confidence notes:
  - Current roles: partially confirmed via available web sources
  - Biographical details: extremely limited due to web access constraints (Exa rate-limited, Baidu 403, government sites JS-heavy rendering, search engines blocked)
  - Party secretary and mayor identities: names confirmed from search results
  - All claims labeled with confidence level; gaps explicitly documented
  - This is a partial-evidence artifact — uncertainty is explicit
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
for parent_count in [3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "二连浩特市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "inner_mongolia_二连浩特市"
if _CURRENT_DIR.name == "inner_mongolia_二连浩特市":
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
# IDs: 1-9 party committee, 10-19 government leadership, 20+ predecessors/others

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership — current (as of July 2026)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "王三石",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共二连浩特市委员会",
        "source": "二连浩特市人民政府网站及公开报道",
        "notes": "【推定】王三石在公开报道中以二连浩特市委书记身份出现。具体任职时间及完整简历待确认。"
    },
    {
        "id": 2,
        "name": "马海涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "二连浩特市人民政府",
        "source": "二连浩特市人民政府网站及公开报道",
        "notes": "【推定】马海涛在公开报道中以二连浩特市长身份出现。具体任职时间及完整简历待确认。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 市人大
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "闫红",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "二连浩特市人民代表大会常务委员会",
        "source": "推断（基于公开报道）",
        "notes": "【待确认】可能为二连浩特市人大常委会主任。具体任职信息待核实。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 市政协
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 4,
        "name": "朝格",
        "gender": "",
        "ethnicity": "蒙古族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "政协二连浩特市委员会",
        "source": "推断（基于公开报道）",
        "notes": "【待确认】可能为二连浩特市政协主席。具体任职信息待核实。"
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中国共产党二连浩特市委员会", "type": "党委", "level": "县级"},
    {"id": 2, "name": "二连浩特市人民政府", "type": "政府", "level": "县级"},
    {"id": 3, "name": "二连浩特市人民代表大会常务委员会", "type": "人大", "level": "县级"},
    {"id": 4, "name": "中国人民政治协商会议二连浩特市委员会", "type": "政协", "level": "县级"},
    {"id": 5, "name": "中国共产党二连浩特市纪律检查委员会", "type": "纪委", "level": "县级"},
    {"id": 6, "name": "二连浩特市监察委员会", "type": "监察", "level": "县级"},
    {"id": 7, "name": "中共二连浩特市委组织部", "type": "党委", "level": "县级"},
    {"id": 8, "name": "中共二连浩特市委宣传部", "type": "党委", "level": "县级"},
    {"id": 9, "name": "中共二连浩特市委统战部", "type": "党委", "level": "县级"},
    {"id": 10, "name": "中共二连浩特市委政法委员会", "type": "党委", "level": "县级"},
    {"id": 11, "name": "二连浩特边境经济合作区", "type": "开发区", "level": "县级"},
]

# ── Positions ─────────────────────────────────────────────────────────────────

positions = [
    # Current positions
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "unknown", "end": "present", "rank": "正处级", "note": "【待确认】王三石现任二连浩特市委书记"},
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "unknown", "end": "present", "rank": "正处级", "note": "【待确认】马海涛现任二连浩特市长"},
    {"person_id": 3, "org_id": 3, "title": "市人大常委会主任", "start": "unknown", "end": "present", "rank": "正处级", "note": "【待确认】"},
    {"person_id": 4, "org_id": 4, "title": "市政协主席", "start": "unknown", "end": "present", "rank": "正处级", "note": "【待确认】"},
]

# ── Relationships ─────────────────────────────────────────────────────────────

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "党委政府主要领导搭档关系",
        "confidence": "plausible",
        "source": "推定（基于职务关系）",
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "党委和人大领导共事",
        "confidence": "unverified",
        "source": "推定（基于职务关系）",
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "政府和人大领导工作关系",
        "confidence": "unverified",
        "source": "推定（基于职务关系）",
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "overlap",
        "context": "党委和政协领导工作关系",
        "confidence": "unverified",
        "source": "推定（基于职务关系）",
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "overlap",
        "context": "政府和政协领导工作关系",
        "confidence": "unverified",
        "source": "推定（基于职务关系）",
    },
]


# ════════════════════════════════════════════════════════════════════════════
# Person JSON output
# ════════════════════════════════════════════════════════════════════════════

def write_person_json(person, job):
    """Write a person graph JSON file."""
    pid = person["id"]
    name = person["name"]
    filename = f"{TODAY}-内蒙古自治区-锡林郭勒盟-{job}-{name}.json"
    filepath = PJSON_DIR / filename

    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "内蒙古自治区",
            "city": "锡林郭勒盟",
            "region": "二连浩特市",
            "job": job,
            "task_id": "inner_mongolia_二连浩特市",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": f"erlianhaote_{name}",
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
                "name_birth": f"{name}_",
                "name_birthplace": f"{name}_",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": person["current_org"],
                "title": person["current_post"],
                "level": "县处级",
                "location": "内蒙古自治区锡林郭勒盟二连浩特市",
                "system": "party" if "书记" in person["current_post"] and "纪委" not in person["current_post"] else "government" if "市长" in person["current_post"] else "other",
                "rank": "正处级",
                "is_key_promotion": False,
                "notes": person.get("notes", "详细信息待查"),
                "confidence": "plausible" if person["id"] in [1, 2] else "unverified",
                "source_ids": ["S001"]
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": f"公开资料未找到{name}的完整履历。二连浩特市政府网站为JS渲染页面，无法通过文本抓取获取'领导之窗'页面的详细简历信息。建议：使用浏览器直接访问elht.gov.cn的'领导之窗'栏目，或查看锡林郭勒盟委组织部任前公示。",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "organizations": [
            {"org_id": 1, "name": "中国共产党二连浩特市委员会", "type": "党委", "role": "领导职务"},
            {"org_id": 2, "name": "二连浩特市人民政府", "type": "政府", "role": "领导职务"}
        ],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "数据不足，无法评估晋升速度",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "数据不足，无法评估工作风格"
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026年7月，未在公开资料中发现相关风险信号。注意：搜索范围受限（Exa限流、Baidu 403、搜索引擎均超时），此结论可能不全面。",
                "date": "2026-07-25",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "二连浩特市人民政府官方网站",
                "url": "http://www.elht.gov.cn/",
                "publisher": "二连浩特市人民政府",
                "published_at": "",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "medium",
                "notes": "JS渲染页面，文本抓取只能获取首页框架，无法获取领导之窗详细内容"
            }
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": f"缺少{name}的出生信息、教育背景、完整工作履历及确切任职确认"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的确切任职信息（职务、任职时间、完整简历）",
                "why_it_matters": "这是调查的核心目标人物",
                "suggested_queries": [f"二连浩特市 {name} 简历", f"锡林郭勒盟 {name} 任前公示", "二连浩特市 领导之窗"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "critical",
                "question": f"二连浩特市当前{job}的完整履历",
                "why_it_matters": "需要了解核心人物的完整职业生涯",
                "suggested_queries": [f"{name} 工作经历", f"{name} 出生 籍贯"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "high",
                "question": "二连浩特市常委班子完整名单",
                "why_it_matters": "需要了解领导班子成员构成，包括副書記、紀委、組織、宣傳等",
                "suggested_queries": ["二连浩特市 市委常委 班子", "二连浩特市 领导分工"],
                "last_attempted": "2026-07-25"
            }
        ]
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Person JSON created: {filepath}")


# ════════════════════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════════════════════

def build():
    """Run the full data build."""
    print(f"\n{'='*60}")
    print(f"Building {SLUG} Network Data")
    print(f"{'='*60}")
    print(f"Date: {AS_OF}")
    print(f"Staging: {STAGING}")
    print()

    # Use the modern runner
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

    print("\n--- Person JSON files ---")
    job_map = {1: "市委书记", 2: "市长", 3: "市人大常委会主任", 4: "市政协主席"}
    for p in persons:
        job = job_map.get(p["id"], "领导")
        write_person_json(p, job)

    print(f"\n{'='*60}")
    print(f"{SLUG} Network Build Complete")
    print(f"{'='*60}")
    print(f"Persons:     {len(persons)}")
    print(f"Orgs:        {len(organizations)}")
    print(f"Positions:   {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")
    print(f"Person JSONs: {PJSON_DIR / f'{TODAY}-内蒙古自治区-锡林郭勒盟-*-*.json'}")
    print()


if __name__ == "__main__":
    build()
