#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 牟平区 (Muping District), 烟台市, 山东省.

Level: 市辖区
Province: 山东省
Parent city: 烟台市
Targets: 区委书记 (Party Secretary), 区长 (District Magistrate)
Task ID: shandong_牟平区

Research date: 2026-07-25
Official source: https://www.muping.gov.cn/ (牟平区人民政府) — site uses SPA rendering, leadership pages not extractable

Current status (as of 2026-07-25, based on Baidu Baike 牟平区条目 "政治" section, updated 2026年6月):
- 区委书记: 陈钢
- 区长: 王磊
- 区人大常委会主任: 纪刚
- 区政协主席: 曹东辉

Confidence notes:
  All web search tools (Exa, Baidu, Google, Jina Reader) were rate-limited,
  blocked, or timed out during research. Government site www.muping.gov.cn
  uses JS-heavy rendering and leadership column pages return the main portal
  template only. Baidu Baike returned 403 on individual person pages and on
  direct item URL. Baidu search return 403/captcha.

  Leadership identification is from the subagent which successfully loaded
  the Baidu Baike 牟平区 page (political section) listing 区委书记陈钢 and
  区长王磊 as of 2026年6月. No biographical details (birth year, birthplace,
  education, career timeline) for either leader could be retrieved.

  This is a partial-evidence build per source_fallbacks.md artifact mode.
"""

from __future__ import annotations

import json
import os
import sqlite3  # noqa: F401 — used transitively via gov_relation.runner
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

SLUG = "牟平区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-25"
TODAY = "20260725"

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 陈钢 — 区委书记
    {
        "id": 1,
        "name": "陈钢",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共烟台市牟平区委书记",
        "current_org": "中共烟台市牟平区委员会",
        "source": "百度百科-牟平区条目「政治」章节 (2026年6月更新); 待补充公开资料",
    },
    # 2. 王磊 — 区长
    {
        "id": 2,
        "name": "王磊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "烟台市牟平区区长",
        "current_org": "牟平区人民政府",
        "source": "百度百科-牟平区条目「政治」章节 (2026年6月更新); 待补充公开资料",
    },
    # ════════════════════════════════════════
    # Other Key Leadership (from Baidu Baike)
    # ════════════════════════════════════════

    # 3. 纪刚 — 区人大常委会主任
    {
        "id": 3,
        "name": "纪刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "牟平区人大常委会主任",
        "current_org": "烟台市牟平区人民代表大会常务委员会",
        "source": "百度百科-牟平区条目「政治」章节 (2026年6月更新)",
    },
    # 4. 曹东辉 — 区政协主席
    {
        "id": 4,
        "name": "曹东辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "牟平区政协主席",
        "current_org": "中国人民政治协商会议烟台市牟平区委员会",
        "source": "百度百科-牟平区条目「政治」章节 (2026年6月更新)",
    },
    # ════════════════════════════════════════
    # Leadership Team (placeholders — names unknown)
    # ════════════════════════════════════════

    # 5. 区委副书记（专职副书记）
    {
        "id": 5,
        "name": "（待查）区委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共牟平区委副书记",
        "current_org": "中共烟台市牟平区委员会",
        "source": "待查",
    },
    # 6. 区纪委书记
    {
        "id": 6,
        "name": "（待查）区纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "牟平区纪委书记、监委主任",
        "current_org": "中共烟台市牟平区纪律检查委员会",
        "source": "待查",
    },
    # 7. 组织部部长
    {
        "id": 7,
        "name": "（待查）组织部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "牟平区委组织部部长",
        "current_org": "中共烟台市牟平区委组织部",
        "source": "待查",
    },
    # 8. 宣传部部长
    {
        "id": 8,
        "name": "（待查）宣传部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "牟平区委宣传部部长",
        "current_org": "中共烟台市牟平区委宣传部",
        "source": "待查",
    },
    # 9. 政法委书记
    {
        "id": 9,
        "name": "（待查）政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "牟平区委政法委书记",
        "current_org": "中共烟台市牟平区委政法委员会",
        "source": "待查",
    },
    # 10. 常务副区长
    {
        "id": 10,
        "name": "（待查）常务副区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "牟平区常务副区长",
        "current_org": "牟平区人民政府",
        "source": "待查",
    },
    # ════════════════════════════════════════
    # Predecessors (unknown)
    # ════════════════════════════════════════

    # 11. 前任区委书记
    {
        "id": 11,
        "name": "（待查）前任区委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "已离任",
        "current_org": "",
        "source": "待查",
    },
    # 12. 前任区长
    {
        "id": 12,
        "name": "（待查）前任区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "已离任",
        "current_org": "",
        "source": "待查",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共烟台市牟平区委员会", "type": "党委", "level": "县处级", "parent": "中共烟台市委", "location": "烟台市牟平区"},
    {"id": 2, "name": "牟平区人民政府", "type": "政府", "level": "县处级", "parent": "烟台市人民政府", "location": "烟台市牟平区"},
    {"id": 3, "name": "中共烟台市牟平区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共烟台市纪委", "location": "烟台市牟平区"},
    {"id": 4, "name": "中共烟台市牟平区委组织部", "type": "党委部门", "level": "乡科级", "parent": "中共烟台市牟平区委员会", "location": "烟台市牟平区"},
    {"id": 5, "name": "中共烟台市牟平区委宣传部", "type": "党委部门", "level": "乡科级", "parent": "中共烟台市牟平区委员会", "location": "烟台市牟平区"},
    {"id": 6, "name": "中共烟台市牟平区委政法委员会", "type": "党委部门", "level": "乡科级", "parent": "中共烟台市牟平区委员会", "location": "烟台市牟平区"},
    {"id": 7, "name": "烟台市牟平区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "烟台市人大常委会", "location": "烟台市牟平区"},
    {"id": 8, "name": "中国人民政治协商会议烟台市牟平区委员会", "type": "政协", "level": "县处级", "parent": "烟台市政协", "location": "烟台市牟平区"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 陈钢 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "中共烟台市牟平区委书记", "start_date": "", "end_date": "至今", "rank": "正处级", "note": "2026年6月百度百科确认在任"},
    # 王磊 — 区长
    {"person_id": 2, "org_id": 2, "title": "烟台市牟平区区长", "start_date": "", "end_date": "至今", "rank": "正处级", "note": "2026年6月百度百科确认在任"},
    # 纪刚 — 区人大常委会主任
    {"person_id": 3, "org_id": 7, "title": "牟平区人大常委会主任", "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    # 曹东辉 — 区政协主席
    {"person_id": 4, "org_id": 8, "title": "牟平区政协主席", "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    # 待查副书记
    {"person_id": 5, "org_id": 1, "title": "中共牟平区委副书记", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "姓名待查"},
    # 待查纪委书记
    {"person_id": 6, "org_id": 3, "title": "牟平区纪委书记、监委主任", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "姓名待查"},
    # 待查组织部长
    {"person_id": 7, "org_id": 4, "title": "牟平区委组织部部长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "姓名待查"},
    # 待查宣传部长
    {"person_id": 8, "org_id": 5, "title": "牟平区委宣传部部长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "姓名待查"},
    # 待查政法委书记
    {"person_id": 9, "org_id": 6, "title": "牟平区委政法委书记", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "姓名待查"},
    # 待查常务副区长
    {"person_id": 10, "org_id": 2, "title": "牟平区常务副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "姓名待查"},
    # 前任区委书记
    {"person_id": 11, "org_id": 1, "title": "中共烟台市牟平区委书记（前任）", "start_date": "", "end_date": "（已离任）", "rank": "正处级", "note": "姓名待查"},
    # 前任区长
    {"person_id": 12, "org_id": 2, "title": "烟台市牟平区区长（前任）", "start_date": "", "end_date": "（已离任）", "rank": "正处级", "note": "姓名待查"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 书记 — 区长：党政搭档
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—区长党政搭档", "overlap_org": "牟平区", "overlap_period": "截至2026年6月"},
    # 书记 — 人大主任
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "区委书记—区人大常委会主任", "overlap_org": "牟平区", "overlap_period": "截至2026年6月"},
    # 书记 — 政协主席
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "区委书记—区政协主席", "overlap_org": "牟平区", "overlap_period": "截至2026年6月"},
    # 区长 — 人大主任
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "区长—区人大常委会主任", "overlap_org": "牟平区", "overlap_period": "截至2026年6月"},
    # 区长 — 政协主席
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "区长—区政协主席", "overlap_org": "牟平区", "overlap_period": "截至2026年6月"},
    # 前任区委书记 → 现任（如果已知前任姓名后可确认）
    # FIXME: Add predecessor relationship when names are known
]

# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON HELPERS
# ══════════════════════════════════════════════════════════════════════════════


def write_person_json(person: dict, job: str) -> None:
    """Write a person graph JSON file following person_graph_json.md schema."""
    person_id_slug = f"muping_{person['name']}".replace("（", "_").replace("）", "_").replace(" ", "_")

    json_data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "山东省",
            "city": "烟台市",
            "region": "牟平区",
            "job": job,
            "task_id": "shandong_牟平区",
            "time_focus": "2026-07-25"
        },
        "identity": {
            "person_id": person_id_slug,
            "name": person["name"],
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
                "name_birth": f"{person['name']}_{person.get('birth', '')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "未知",
                "end": "present" if person.get("current_post") else "未知",
                "org": person.get("current_org", "待查"),
                "title": person.get("current_post", "待查"),
                "level": "正处级",
                "location": "烟台市牟平区",
                "system": "party" if "书记" in (person.get("current_post", "")) else "government",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "大部分履历待补充；仅知当前职务",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "organizations": [
            {
                "org_id": o["id"],
                "name": o["name"],
                "type": o["type"],
                "role": person.get("current_post", ""),
                "period": "至今",
                "source_ids": []
            }
            for o in organizations
            if o["name"] == person.get("current_org", "")
        ],
        "relationships": [
            {
                "person": r_target_name,
                "person_id": "",
                "relationship_type": r_type,
                "strength": "medium",
                "evidence": r_context,
                "overlap_org": r_overlap,
                "overlap_period": r_period,
                "direction": "undirected",
                "confidence": "plausible",
                "source_ids": []
            }
            for r_target_name, r_type, r_context, r_overlap, r_period in _get_relationships_for(person["id"])
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "资料不足，无法评估晋升速度",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "未在公开资料中发现负面信号（搜索受限，结论待验证）",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": ["S001"]
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "百度百科-牟平区",
                "url": "https://baike.baidu.com/item/%E7%89%9F%E5%B9%B3%E5%8C%BA",
                "publisher": "百度百科",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "encyclopedia",
                "reliability": "low",
                "notes": "403禁止直接访问；子代理通过浏览器成功加载了页面内容"
            }
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": f"{person['name']}的完整履历（出生年份、籍贯、教育背景、历任职务均缺失）"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的完整履历（出生年份、籍贯、教育背景、历任职务、晋升时间线）",
                "why_it_matters": "无法验证当前岗位任职资格和晋升路径",
                "suggested_queries": [
                    f"{person['name']} 简历 烟台",
                    f"{person['name']} 任前公示",
                    f"{person['name']} 牟平区",
                    f"{person['name']} 百度百科"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"{person['name']}的籍贯和出生地",
                "why_it_matters": "识别可能的同乡关系网络",
                "suggested_queries": [
                    f"{person['name']} 籍贯 出生",
                ],
                "last_attempted": AS_OF
            }
        ]
    }

    clean_name = person["name"].replace("（", "_").replace("）", "_")
    filename = f"{TODAY}-山东省-烟台市-{job}-{clean_name}.json"
    filepath = Path(PERSONS_DIR) / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Person JSON: {filepath.name}")


def _get_relationships_for(person_id: int) -> list[tuple[str, str, str, str, str]]:
    """Return (target_name, type, context, overlap_org, overlap_period) for a person."""
    results = []
    person_map = {p["id"]: p["name"] for p in persons}
    for r in relationships:
        if r["person_a"] == person_id:
            results.append((
                person_map.get(r["person_b"], "未知"),
                r["type"],
                r["context"],
                r["overlap_org"],
                r["overlap_period"],
            ))
        elif r["person_b"] == person_id:
            results.append((
                person_map.get(r["person_a"], "未知"),
                r["type"],
                r["context"],
                r["overlap_org"],
                r["overlap_period"],
            ))
    return results


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    print(f"=== Building {SLUG} network ===")

    # 1. Build database + GEXF
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
    print(f"  ✓ Database: {DB_PATH}")
    print(f"  ✓ GEXF: {GEXF_PATH}")

    # 2. Write person JSONs for core figures
    print("\n--- Person JSONs ---")
    for pid, job in [(1, "区委书记"), (2, "区长")]:
        p = next(p_ for p_ in persons if p_["id"] == pid)
        write_person_json(p, job)

    # 3. Summary
    print("\n--- Summary ---")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"\nAll artifacts in: {_STAGING_DIR}")
    print("Done.")


if __name__ == "__main__":
    main()
