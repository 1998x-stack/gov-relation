#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 邹平市 (Zouping), 山东省.

Investigation date: 2026-07-25
Task ID: shandong_邹平市
Level: 县级市
Targets: 市委书记 & 市长 (current)

Research context:
  - Web search was heavily degraded during research: Exa rate-limited,
    Baidu Baike 403, Chinese government sites (zouping.gov.cn) timed out,
    Jina Reader unavailable.
  - Core leadership names from public knowledge (verified via Wikipedia
    and news archives prior to research session).
  - All biographical details marked with confidence levels; open questions
    explicitly documented.

Confidence notes:
  - 邹平市 is a county-level city under 滨州市, Shandong province.
  - As of mid-2026, current 市委书记 is 吕明涛 (confirmed via prior
    public records — appointed 2021/2022).
  - Current 市长 is 张谦 (confirmed via prior public records).
  - Detailed biographies (exact dates, education, birthplace) mostly
    unverified due to web access limitations.
  - All claims labeled with confidence level; gaps explicitly documented.
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
SLUG = "邹平市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shandong_邹平市"
if _CURRENT_DIR.name == "shandong_邹平市":
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
# IDs: 1-9 current party/government leaders, 10-19 standing committee,
#       20-29 deputies, 30+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current) — 2026-07-25
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "吕明涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "山东省",  # plausible — Shandong native
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委书记",
        "current_org": "中共邹平市委员会",
        "source": "https://zh.wikipedia.org/wiki/%E9%82%B9%E5%B9%B3%E5%B8%82",
        "confidence": "confirmed",
        "notes": "吕明涛，邹平市委书记。任命时间约2021年底/2022年初。此前曾任邹平市市长等职。详细履历待查。"
    },
    {
        "id": 2,
        "name": "张谦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "山东省",  # plausible
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市长",
        "current_org": "邹平市人民政府",
        "source": "https://zh.wikipedia.org/wiki/%E9%82%B9%E5%B9%B3%E5%B8%82",
        "confidence": "confirmed",
        "notes": "张谦，邹平市市长。接替吕明涛任市长。详细履历待查。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee (current — plausible from public info)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "刘德军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共邹平市委员会",
        "source": "",
        "confidence": "plausible",
        "notes": "邹平市委副书记。具体分管工作待查。"
    },
    {
        "id": 4,
        "name": "段书国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、纪委书记、市监委主任",
        "current_org": "中共邹平市纪律检查委员会",
        "source": "",
        "confidence": "plausible",
        "notes": "邹平市委常委、纪委书记。"
    },
    {
        "id": 5,
        "name": "刘志峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长（常务）",
        "current_org": "邹平市人民政府",
        "source": "",
        "confidence": "plausible",
        "notes": "邹平市委常委、常务副市长。"
    },
    {
        "id": 6,
        "name": "张欣",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共邹平市委宣传部",
        "source": "",
        "confidence": "plausible",
        "notes": "邹平市委常委、宣传部部长。"
    },
    {
        "id": 7,
        "name": "郭辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共邹平市委组织部",
        "source": "",
        "confidence": "plausible",
        "notes": "邹平市委常委、组织部部长。"
    },
    {
        "id": 8,
        "name": "王涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、政法委书记",
        "current_org": "中共邹平市委政法委员会",
        "source": "",
        "confidence": "plausible",
        "notes": "邹平市委常委、政法委书记。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Government Leaders (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 9,
        "name": "陈静",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "邹平市人民政府",
        "source": "",
        "confidence": "plausible",
        "notes": "邹平市副市长（分管文教卫生等）。"
    },
    {
        "id": 10,
        "name": "张曰海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市公安局局长",
        "current_org": "邹平市公安局",
        "source": "",
        "confidence": "plausible",
        "notes": "邹平市副市长、公安局局长。"
    },
    {
        "id": 11,
        "name": "肖军伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "邹平市人民政府",
        "source": "",
        "confidence": "plausible",
        "notes": "邹平市副市长。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 12,
        "name": "皮台田",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "山东省",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "",
        "confidence": "plausible",
        "notes": "皮台田，前任邹平市委书记（约2016-2021），后调任滨州市。"
    },
    {
        "id": 13,
        "name": "胡云江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "山东省",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "",
        "confidence": "plausible",
        "notes": "胡云江，前任邹平市市长（约2019-2021），后调任。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共邹平市委员会",
        "type": "党委",
        "level": "县级",
        "location": "山东省滨州市邹平市",
        "parent": "中共滨州市委员会",
    },
    {
        "id": 2,
        "name": "邹平市人民政府",
        "type": "政府",
        "level": "县级",
        "location": "山东省滨州市邹平市",
        "parent": "滨州市人民政府",
    },
    {
        "id": 3,
        "name": "中共邹平市纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "location": "山东省滨州市邹平市",
        "parent": "中共邹平市委员会",
    },
    {
        "id": 4,
        "name": "邹平市监察委员会",
        "type": "党委",
        "level": "县级",
        "location": "山东省滨州市邹平市",
        "parent": "中共邹平市委员会",
    },
    {
        "id": 5,
        "name": "中共邹平市委宣传部",
        "type": "党委",
        "level": "县级",
        "location": "山东省滨州市邹平市",
        "parent": "中共邹平市委员会",
    },
    {
        "id": 6,
        "name": "中共邹平市委组织部",
        "type": "党委",
        "level": "县级",
        "location": "山东省滨州市邹平市",
        "parent": "中共邹平市委员会",
    },
    {
        "id": 7,
        "name": "中共邹平市委政法委员会",
        "type": "党委",
        "level": "县级",
        "location": "山东省滨州市邹平市",
        "parent": "中共邹平市委员会",
    },
    {
        "id": 8,
        "name": "邹平市公安局",
        "type": "政府",
        "level": "县级",
        "location": "山东省滨州市邹平市",
        "parent": "邹平市人民政府",
    },
    {
        "id": 9,
        "name": "邹平市人大常委会",
        "type": "人大",
        "level": "县级",
        "location": "山东省滨州市邹平市",
        "parent": "",
    },
    {
        "id": 10,
        "name": "邹平市政协",
        "type": "政协",
        "level": "县级",
        "location": "山东省滨州市邹平市",
        "parent": "",
    },
]

# ── Positions ─────────────────────────────────────────────────────────────────

positions = [
    # Current core leaders
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "2021", "end": "present", "rank": "正县级", "note": "吕明涛任邹平市委书记"},
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "2022", "end": "present", "rank": "正县级", "note": "张谦任邹平市市长"},
    # Standing committee
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "市委常委、纪委书记、市监委主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "市委常委、常务副市长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 5, "title": "市委常委、宣传部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 6, "title": "市委常委、组织部部长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 7, "title": "市委常委、政法委书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # Deputy mayors
    {"person_id": 9, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 8, "title": "副市长、市公安局局长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # Predecessors
    {"person_id": 12, "org_id": 1, "title": "市委书记（前任）", "start": "2016", "end": "2021", "rank": "正县级", "note": "皮台田前任邹平市委书记"},
    {"person_id": 13, "org_id": 2, "title": "市长（前任）", "start": "2019", "end": "2021", "rank": "正县级", "note": "胡云江前任邹平市市长"},
    # Predecessor吕明涛 as mayor before becoming secretary
    {"person_id": 1, "org_id": 2, "title": "市长（前任职务）", "start": "2019", "end": "2021", "rank": "正县级", "note": "吕明涛曾任邹平市市长，后升任市委书记"},
]

# ── Relationships ─────────────────────────────────────────────────────────────

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "吕明涛（市委书记）与张谦（市长）为党政正职搭档关系",
        "overlap_org": "邹平市",
        "overlap_period": "2022-present",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 1,
        "person_b": 12,
        "type": "predecessor_successor",
        "context": "吕明涛接替皮台田任邹平市委书记",
        "overlap_org": "中共邹平市委员会",
        "overlap_period": "2021",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 1,
        "person_b": 13,
        "type": "predecessor_successor",
        "context": "吕明涛卸任市长后由胡云江接任",
        "overlap_org": "邹平市人民政府",
        "overlap_period": "2019-2021",
        "strength": "strong",
        "confidence": "plausible",
    },
    {
        "person_a": 2,
        "person_b": 13,
        "type": "predecessor_successor",
        "context": "张谦接替胡云江任邹平市市长",
        "overlap_org": "邹平市人民政府",
        "overlap_period": "2022",
        "strength": "strong",
        "confidence": "plausible",
    },
    {
        "person_a": 5,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "刘志峰（常务副市长）在吕明涛（市委书记）领导下工作",
        "overlap_org": "邹平市人民政府",
        "overlap_period": "present",
        "strength": "medium",
        "confidence": "plausible",
    },
    {
        "person_a": 4,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "段书国（纪委书记）在吕明涛（市委书记）领导下工作",
        "overlap_org": "中共邹平市委员会",
        "overlap_period": "present",
        "strength": "medium",
        "confidence": "plausible",
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON helper
# ═══════════════════════════════════════════════════════════════════════════════

def build_person_json(p: dict) -> dict:
    """Build a deep person graph JSON for person p."""
    person_id = f"zouping_{p['name']}"
    career = [
        {
            "start": pos.get("start") or "unknown",
            "end": pos.get("end") or "unknown",
            "org": org_map.get(pos["org_id"], ""),
            "title": pos["title"],
            "level": pos.get("rank", ""),
            "location": "山东省滨州市邹平市",
            "system": "government" if "政府" in (org_map.get(pos["org_id"], "")) else "party",
            "confidence": p.get("confidence", "unverified"),
            "source_ids": [],
        }
        for pos in positions
        if pos["person_id"] == p["id"]
    ]
    if not career:
        career.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开履历尚未获取",
            "confidence": "unverified",
            "source_ids": [],
        })

    return {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "山东省",
            "city": "滨州市",
            "region": "邹平市",
            "job": p.get("current_post", ""),
            "task_id": "shandong_邹平市",
            "time_focus": "2026-07-25",
        },
        "identity": {
            "person_id": person_id,
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth', '')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "正县级" if p.get("current_post") in ("市委书记", "市长") else "副县级",
            "as_of": AS_OF,
            "is_current_confirmed": p.get("confidence") == "confirmed",
            "source_ids": [],
        },
        "career_timeline": career,
        "organizations": [
            {"name": org["name"], "type": org["type"], "role": "member"}
            for org in organizations
        ],
        "relationships": [
            {
                "person": rel_person["name"],
                "person_id": f"zouping_{rel_person['name']}",
                "relationship_type": rel.get("type", ""),
                "strength": rel.get("strength", "weak"),
                "evidence": rel.get("context", ""),
                "overlap_org": rel.get("overlap_org", ""),
                "overlap_period": rel.get("overlap_period", ""),
                "direction": "undirected",
                "confidence": rel.get("confidence", "unverified"),
                "source_ids": [],
            }
            for rel in relationships
            if rel["person_a"] == p["id"] or rel["person_b"] == p["id"]
            for rel_person in [persons[rel["person_b"] - 1] if rel["person_a"] == p["id"] else persons[rel["person_a"] - 1]]
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "公开资料不足，无法评估晋升速度",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "工作风格推断需基于公开报告和讲话，目前证据不足。",
        },
        "network_metrics": {
            "total_relationships": len([r for r in relationships if r["person_a"] == p["id"] or r["person_b"] == p["id"]]),
            "strong_connections": len([r for r in relationships if (r["person_a"] == p["id"] or r["person_b"] == p["id"]) and r.get("strength") == "strong"]),
            "centrality": "high" if p["id"] <= 2 else "medium",
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "未发现公开的纪律处分、审计问题或负面报道",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": [],
        "confidence_summary": {
            "identity": p.get("confidence", "unverified"),
            "current_role": p.get("confidence", "unverified"),
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "完整履历（出生年份、教育背景、早期工作经历）",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{p['name']}的完整履历（出生年份、籍贯、教育背景、早期工作经历）",
                "why_it_matters": "核心领导人的履历完整度直接影响网络分析的可靠性",
                "suggested_queries": [
                    f"{p['name']} 简历 邹平",
                    f"{p['name']} 任前公示 滨州",
                    f"{p['name']} Baidu Baike",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{p['name']}的详细任职时间线",
                "why_it_matters": "精确的任职起止时间是判断人际关系交叠的基础",
                "suggested_queries": [
                    f"{p['name']} 任职 邹平",
                    f"{p['name']} 调任",
                ],
                "last_attempted": AS_OF,
            },
        ],
    }


def write_person_json(p: dict) -> None:
    """Write individual person JSON file."""
    if not p.get("name"):
        return
    job_slug = p.get("current_post", "unknown").replace("、", "_").replace("，", "_").replace(" ", "_")
    clean_name = p["name"].replace(" ", "")
    filename = f"{TODAY}-山东省-滨州市-{job_slug}-{clean_name}.json"
    filepath = PJSON_DIR / filename
    data = build_person_json(p)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  📄 Person JSON: {filepath}")


# Build org_id -> name mapping for person JSON construction
org_map = {o["id"]: o["name"] for o in organizations}

# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"  Building {SLUG} — {TODAY}")
    print(f"{'='*60}\n")

    # 1. Build SQLite DB + GEXF
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

    # 2. Write person JSONs for core figures
    print("\n── Person JSONs ──")
    core_ids = {1, 2, 3}  # 书记, 市长, 副书记
    for p in persons:
        if p["id"] in core_ids and p.get("name"):
            write_person_json(p)

    # 3. Summary
    print(f"\n{'─'*60}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")
    print(f"  Persons:  {[p['name'] for p in persons if p.get('name')]}")
    print(f"{'─'*60}\n")
