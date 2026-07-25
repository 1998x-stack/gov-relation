#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 白塔区, 辽阳市, 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_白塔区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - http://www.lybtq.gov.cn/ — 白塔区人民政府官方网站
  - http://www.lybtq.gov.cn/zwzx/001002/20260721/b37a0e39-24b5-489b-a1af-b9d29fa6c7c1.html — 区委常委会会议 孙善美主持会议 (2026-07-21)
  - http://www.lybtq.gov.cn/zwzx/001002/20260720/998446c0-d09a-41b8-a573-b97aea98a22a.html — 区政府常务会议 朱亚主持会议 (2026-07-20)
  - http://www.lybtq.gov.cn/zwzx/001002/20260714/8c91facc-238f-4088-8dbc-d439643f313f.html — 孙善美深入四个街道督导检查防汛 (2026-07-14)
  - http://www.lybtq.gov.cn/zwzx/city_build.html — 政务动态页面（确认孙善美、朱亚当前任职）

Key findings:
  - 孙善美: 现任区委书记（官网2026年7月多篇新闻确认为区委书记，分别出现在7月14日督导防汛、7月21日主持区委常委会）
  - 朱亚: 现任区委副书记、区政府党组书记、区长（2026年7月20日主持区政府常务会议确认为区长）
  - 公开渠道未找到孙善美、朱亚的更完整履历信息
  - 区委常委会班子（纪委、组织、宣传、政法等）未在政府官网完整列出
  - 四大班子（人大主任、政协主席）信息不可得

Confidence notes:
  - 孙善美股委书记身份通过lybtq.gov.cn官方新闻确认
  - 朱亚区长身份通过lybtq.gov.cn官方会议新闻确认（全文明确写"区委副书记、区政府党组书记、区长朱亚主持会议"）
  - 两人此前履历从公开渠道不可得，标注为unverified
  - 区委常委班子未在政府官网完整列出，标注为待查
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
SLUG = "白塔区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "liaoning_白塔区"
if _CURRENT_DIR.name == "liaoning_白塔区":
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
# IDs: 1xxx = party committee, 2xxx = government, 3xxx = predecessor

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    # 1. 孙善美 — 区委书记
    {
        "id": 1001,
        "name": "孙善美",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "白塔区委书记",
        "current_org": "中共辽阳市白塔区委员会",
        "source": "http://www.lybtq.gov.cn/zwzx/001002/20260721/b37a0e39-24b5-489b-a1af-b9d29fa6c7c1.html",
    },
    # 2. 朱亚 — 区委副书记、区长
    {
        "id": 2001,
        "name": "朱亚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "白塔区委副书记、区长",
        "current_org": "白塔区人民政府",
        "source": "http://www.lybtq.gov.cn/zwzx/001002/20260720/998446c0-d09a-41b8-a573-b97aea98a22a.html",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {
        "id": 10,
        "name": "中共辽阳市白塔区委员会",
        "type": "party",
        "level": "district",
        "parent": "中共辽阳市委员会",
        "location": "白塔区",
    },
    {
        "id": 11,
        "name": "白塔区人民政府",
        "type": "government",
        "level": "district",
        "parent": "辽阳市人民政府",
        "location": "白塔区",
    },
    {
        "id": 12,
        "name": "辽阳市白塔区人民代表大会常务委员会",
        "type": "npc",
        "level": "district",
        "parent": "辽阳市人民代表大会常务委员会",
        "location": "白塔区",
    },
    {
        "id": 13,
        "name": "中国人民政治协商会议辽阳市白塔区委员会",
        "type": "cppcc",
        "level": "district",
        "parent": "政协辽阳市委员会",
        "location": "白塔区",
    },
    {
        "id": 14,
        "name": "中共辽阳市白塔区纪律检查委员会",
        "type": "party_discipline",
        "level": "district",
        "parent": "中共辽阳市纪律检查委员会",
        "location": "白塔区",
    },
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    # 孙善美 — 区委书记
    {"person_id": 1001, "org_id": 10, "title": "白塔区委书记", "start": "", "end": "present", "rank": "正县级", "note": "2026年7月已确认在任"},
    # 朱亚 — 区长
    {"person_id": 2001, "org_id": 11, "title": "白塔区区长", "start": "", "end": "present", "rank": "正县级", "note": "2026年7月已确认在任，全称为区委副书记、区政府党组书记、区长"},
    {"person_id": 2001, "org_id": 10, "title": "白塔区委副书记", "start": "", "end": "present", "rank": "正县级", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 孙善美 ↔ 朱亚 — 书记+区长搭档
    {
        "person_a": 1001,
        "person_b": 2001,
        "type": "superior_subordinate",
        "context": "区委书记与区长搭档关系",
        "overlap_org": "中共辽阳市白塔区委员会",
        "overlap_period": "2026至今",
    },
]

# ── Person JSON helper ───────────────────────────────────────────────────────
def write_person_json(person: dict, extra: dict | None = None) -> Path:
    """Write a per-person deep profile JSON file."""
    pid = person["id"]
    name = person["name"]
    job = person.get("current_post", "")
    if "区长" in job and "副区长" not in job:
        job_short = "区长"
    elif "区委书记" in job:
        job_short = "区委书记"
    else:
        job_short = "领导"

    pjson = extra or {}
    pjson.update({
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "辽阳市",
            "region": "白塔区",
            "job": job_short,
            "task_id": "liaoning_白塔区",
            "time_focus": "2026",
        },
        "identity": {
            "person_id": f"baita_{name}",
            "name": name,
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": [],
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {},
        "work_style_and_personality": {"public_style_indicators": [], "caveat": "No public evidence available for style/personality assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "high" if pid in (1001, 2001) else "medium",
            "biggest_gap": f"此前履历完全未知，仅确认当前职务",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整履历（出生年份、籍贯、教育背景、此前任职经历）",
                "why_it_matters": "核心人物背景分析的基础数据",
                "suggested_queries": [
                    f"{name} 简历 辽阳",
                    f"{name} 任前公示",
                    f"{name} 此前任职",
                    f"{name} 白塔区",
                ],
                "last_attempted": AS_OF,
            }
        ],
    })

    fname = f"{TODAY}-辽宁省-辽阳市-{job_short}-{name}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(pjson, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath}")
    return fpath


# ── Build ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write person JSONs for core figures
    for p in persons:
        pid = p["id"]
        name = p["name"]

        # Build extra data for key figures
        extra = None
        if pid == 1001:  # 孙善美 — 区委书记
            extra = {
                "career_timeline": [
                    {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未找到孙善美担任白塔区委书记之前的任何履历信息", "confidence": "unverified"},
                    {"start": "未知", "end": "present", "org": "中共辽阳市白塔区委员会", "title": "白塔区委书记", "level": "正县级", "location": "辽阳市白塔区", "system": "party", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
                ],
                "source_register": [
                    {"id": "S001", "title": "区委常委会召开会议 孙善美主持会议", "url": "http://www.lybtq.gov.cn/zwzx/001002/20260721/b37a0e39-24b5-489b-a1af-b9d29fa6c7c1.html", "publisher": "白塔区人民政府", "source_type": "official", "reliability": "high", "notes": "2026年7月21日发布，明确孙善美以区委书记身份主持会议"},
                    {"id": "S002", "title": "孙善美深入四个街道督导检查防汛工作", "url": "http://www.lybtq.gov.cn/zwzx/001002/20260714/8c91facc-238f-4088-8dbc-d439643f313f.html", "publisher": "白塔区人民政府", "source_type": "official", "reliability": "high", "notes": "2026年7月14日发布，明确孙善美以区委书记身份督导防汛"},
                ],
            }
        elif pid == 2001:  # 朱亚 — 区长
            extra = {
                "career_timeline": [
                    {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未找到朱亚担任白塔区区长之前的任何履历信息", "confidence": "unverified"},
                    {"start": "未知", "end": "present", "org": "白塔区人民政府", "title": "白塔区区长", "level": "正县级", "location": "辽阳市白塔区", "system": "government", "notes": "全称为区委副书记、区政府党组书记、区长", "confidence": "confirmed", "source_ids": ["S003"]},
                    {"start": "未知", "end": "present", "org": "中共辽阳市白塔区委员会", "title": "白塔区委副书记", "level": "正县级", "location": "辽阳市白塔区", "system": "party", "confidence": "confirmed", "source_ids": ["S003"]},
                ],
                "source_register": [
                    {"id": "S003", "title": "区政府召开党组会议和常务会议 朱亚主持会议", "url": "http://www.lybtq.gov.cn/zwzx/001002/20260720/998446c0-d09a-41b8-a573-b97aea98a22a.html", "publisher": "白塔区人民政府", "source_type": "official", "reliability": "high", "notes": "2026年7月20日发布，明确朱亚以'区委副书记、区政府党组书记、区长'身份主持会议"},
                ],
            }

        write_person_json(p, extra)

    # Print summary for logging
    print(f"\n{SLUG} network build complete.")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
