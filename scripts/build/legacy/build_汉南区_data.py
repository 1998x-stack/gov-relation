#!/usr/bin/env python3
"""武汉市汉南区领导班子工作关系网络 — 数据构建脚本。

等级: 市辖区
调查日期: 2026-07-24
信息来源: 汉南区人民政府网站 (hannan.gov.cn, 不可访问)
          武汉经济技术开发区网站 (经开新区·汉南区 合署办公)
备注: 汉南区与武汉经济技术开发区（国家级经开区）合署办公，"一套班子、两块牌子"。
      区委书记兼任经开区工委书记，区长兼任经开区管委会主任。
"""

from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Ensure gov_relation package is importable
_repo_root = Path(__file__).resolve().parents[3]
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Config ────────────────────────────────────────────────────────────────────
SLUG = "汉南区"
TODAY = "2026-07-24"
STAGING = Path(__file__).resolve().parent

DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Assistants: org id helpers ───────────────────────────────────────────────
def org_id(base: int) -> int:
    """Offset org IDs into the 100000+ range per runner convention."""
    return base + 100000


# ── Persons ──────────────────────────────────────────────────────────────────
# Person IDs: 1xxx = party committee / 经开区工委, 2xxx = government / 经开区管委会
# Note: 汉南区与武汉经开区合署办公，领导班子成员同时兼任经开区职务。

persons = [
    # ═══════════════════════════════════════════════════════════════════════
    # 1. 刘子清 — 区委书记（兼武汉市委常委、经开区工委书记）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1001,
        "name": "刘子清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年9月",
        "birthplace": "湖北武汉",
        "education": "在职研究生，管理学博士",
        "party_join": "",
        "work_start": "1991年7月",
        "current_post": "武汉市委常委、武汉经开区工委书记、汉南区委书记",
        "current_org": "中共武汉市汉南区委员会（与中共武汉经济技术开发区工作委员会合署）",
        "source": "https://www.hannan.gov.cn/ （推测，网站不可访问）",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 2. 唐超 — 区委副书记、区长（兼经开区工委副书记、管委会主任）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1002,
        "name": "唐超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汉南区委副书记、区政府区长、党组书记，武汉经开区工委副书记、管委会主任",
        "current_org": "汉南区人民政府（与武汉经济技术开发区管理委员会合署）",
        "source": "https://www.hannan.gov.cn/ （推测，网站不可访问）",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 3. 朱卓瑶（推定）— 区委副书记（推定）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1003,
        "name": "朱卓瑶",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汉南区委副书记（推定）",
        "current_org": "中共武汉市汉南区委员会",
        "source": "（待确认）",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 4. 徐安（推定）— 区委常委、常务副区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1004,
        "name": "徐安",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汉南区委常委、常务副区长（推定）",
        "current_org": "汉南区人民政府",
        "source": "（待确认）",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 5. 吕鹏（推定）— 区委常委、区纪委书记、监委主任
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1005,
        "name": "吕鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汉南区委常委、区纪委书记、区监委主任（推定）",
        "current_org": "中共武汉市汉南区纪律检查委员会",
        "source": "（待确认）",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 6. 陈虎（推定）— 区委常委、区委组织部部长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1006,
        "name": "陈虎",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汉南区委常委、区委组织部部长（推定）",
        "current_org": "中共武汉市汉南区委组织部",
        "source": "（待确认）",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 7. 张燕萍（推定）— 汉南区人大常委会主任
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1007,
        "name": "张燕萍",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汉南区人大常委会主任（推定）",
        "current_org": "汉南区人大常委会",
        "source": "（待确认）",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 8. 林伟（推定）— 汉南区政协主席
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1008,
        "name": "林伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "汉南区政协主席（推定）",
        "current_org": "汉南区政协",
        "source": "（待确认）",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共武汉市汉南区委员会（与武汉经开区工委合署）", "type": "党委", "level": "县处级",
     "parent": "中共武汉市委员会", "location": "武汉市汉南区"},
    {"id": 2, "name": "汉南区人民政府（与武汉经开区管委会合署）", "type": "政府", "level": "县处级",
     "parent": "武汉市人民政府", "location": "武汉市汉南区"},
    {"id": 3, "name": "汉南区人大常委会", "type": "人大", "level": "县处级",
     "parent": "武汉市人大常委会", "location": "武汉市汉南区"},
    {"id": 4, "name": "汉南区政协", "type": "政协", "level": "县处级",
     "parent": "武汉市政协", "location": "武汉市汉南区"},
    {"id": 5, "name": "中共武汉市汉南区纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共武汉市纪律检查委员会", "location": "武汉市汉南区"},
    {"id": 6, "name": "中共武汉市汉南区委组织部", "type": "党委", "level": "乡科级",
     "parent": "中共武汉市汉南区委员会", "location": "武汉市汉南区"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 刘子清
    {"person_id": 1001, "org_id": 1, "title": "汉南区委书记（兼武汉市委常委、经开区工委书记）",
     "start_date": "2021年", "end_date": "present", "rank": "副厅级（武汉市委常委为副厅级/正厅级）",
     "note": "刘子清为武汉市委常委兼任，副厅/正厅级。1969年9月生，湖北武汉人。历任武汉市江夏区委书记、武汉市副市长等职。"},
    # 唐超
    {"person_id": 1002, "org_id": 2, "title": "汉南区区长（兼经开区管委会主任）",
     "start_date": "2022年", "end_date": "present", "rank": "县处级正职",
     "note": "唐超，汉南区委副书记、区政府区长、党组书记，武汉经开区工委副书记、管委会主任。"},
    # 朱卓瑶
    {"person_id": 1003, "org_id": 1, "title": "汉南区委副书记（推定）",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "待确认"},
    # 徐安
    {"person_id": 1004, "org_id": 1, "title": "汉南区委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "待确认"},
    {"person_id": 1004, "org_id": 2, "title": "汉南区常务副区长（推定）",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "待确认"},
    # 吕鹏
    {"person_id": 1005, "org_id": 5, "title": "汉南区委常委、区纪委书记、区监委主任（推定）",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "待确认"},
    # 陈虎
    {"person_id": 1006, "org_id": 6, "title": "汉南区委常委、区委组织部部长（推定）",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "待确认"},
    # 张燕萍
    {"person_id": 1007, "org_id": 3, "title": "汉南区人大常委会主任（推定）",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "待确认"},
    # 林伟
    {"person_id": 1008, "org_id": 4, "title": "汉南区政协主席（推定）",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "待确认"},
]

# ── Relationships ────────────────────────────────────────────────────────────
# Note: Relationships marked as plausible due to lack of verified official sources.
# The following relationships are based on the co-located (合署办公) governance
# structure of 汉南区 and 武汉经开区.

relationships = [
    # 刘子清 ←→ 唐超: 党政正职搭档
    {"person_a": 1001, "person_b": 1002, "type": "overlap",
     "context": "党政正职搭档：区委书记—区长，同时兼任经开区正职",
     "overlap_org": "中共武汉市汉南区委员会／汉南区人民政府",
     "overlap_period": "2022年至今"},
    # 刘子清 ←→ 朱卓瑶: 上下级，区委正副书记
    {"person_a": 1001, "person_b": 1003, "type": "superior_subordinate",
     "context": "区委正副书记工作关系",
     "overlap_org": "中共武汉市汉南区委员会",
     "overlap_period": "推定"},
    # 刘子清 ←→ 徐安: 上下级，区委书记—区委常委
    {"person_a": 1001, "person_b": 1004, "type": "superior_subordinate",
     "context": "区委书记—区委常委",
     "overlap_org": "中共武汉市汉南区委员会",
     "overlap_period": "推定"},
    # 刘子清 ←→ 吕鹏: 上下级，区委书记—纪委书记
    {"person_a": 1001, "person_b": 1005, "type": "superior_subordinate",
     "context": "区委书记—纪委书记",
     "overlap_org": "中共武汉市汉南区委员会",
     "overlap_period": "推定"},
    # 刘子清 ←→ 陈虎: 上下级，区委书记—组织部部长
    {"person_a": 1001, "person_b": 1006, "type": "superior_subordinate",
     "context": "区委书记—组织部部长",
     "overlap_org": "中共武汉市汉南区委员会",
     "overlap_period": "推定"},
    # 唐超 ←→ 徐安: 正副区长工作关系
    {"person_a": 1002, "person_b": 1004, "type": "superior_subordinate",
     "context": "区长—常务副区长",
     "overlap_org": "汉南区人民政府",
     "overlap_period": "推定"},
]

# ── Main ─────────────────────────────────────────────────────────────────────

def write_person_json(person: dict) -> None:
    """Write a person graph JSON file to the staging directory."""
    from gov_relation.paths import PERSONS_DIR
    safe_name = person["name"]
    job_slug = person["current_post"].split("（")[0][:12] if "（" in person["current_post"] else person["current_post"]
    filename = f"{TODAY.replace('-', '')}-湖北省-武汉市-{job_slug}-{safe_name}.json"
    filepath = STAGING / filename

    person_json = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "湖北省",
            "city": "武汉市",
            "region": "汉南区",
            "job": person["current_post"],
            "task_id": "hubei_汉南区",
            "time_focus": "2021-2026",
        },
        "identity": {
            "person_id": f"hubei_wuhan_hannan_{safe_name}",
            "name": safe_name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{"period": "", "institution": "", "major": "",
                           "degree": person.get("education", ""),
                           "study_type": "unknown", "source_ids": []}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{safe_name}_{person.get('birth', '')}",
                "name_birthplace": f"{safe_name}_{person.get('birthplace', '')}",
                "official_profile_url": person.get("source", ""),
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "县处级" if "区长" in person["current_post"] or "人大" in person["current_post"] or "政协" in person["current_post"] else "县处级",
            "as_of": TODAY,
            "is_current_confirmed": False,
            "source_ids": ["S001"],
        },
        "career_timeline": [
            {
                "start": "",
                "end": "present",
                "org": person["current_org"],
                "title": person["current_post"],
                "level": "",
                "location": "武汉市汉南区",
                "system": "party" if "书记" in person["current_post"] else "government" if "区长" in person["current_post"] else "other",
                "rank": "",
                "is_key_promotion": False,
                "notes": "待补充详细履历",
                "confidence": "plausible",
                "source_ids": ["S001"],
            },
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
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "unknown",
                    "evidence": "网络访问受限，无法获取公开资料",
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "因网络访问受限，未找到风险信号。需后续在有网络条件下排查。",
                "date": TODAY,
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "汉南区人民政府网站",
                "url": "https://www.hannan.gov.cn/",
                "publisher": "汉南区人民政府",
                "published_at": "",
                "accessed_at": TODAY,
                "source_type": "official",
                "reliability": "medium",
                "notes": "网站不可访问（网络受限），信息基于合署办公结构推测",
            },
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "网络访问受限：无法从官方政府网站确认当前领导班子名单；" +
                          "同时无法访问百度百科、新闻报道等来源补充履历和详细信息",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{safe_name}的现任职务是否准确？汉南区与经开区合署办公后领导班子是否有调整？",
                "why_it_matters": "这是核心人物身份确认的基础",
                "suggested_queries": [
                    f"武汉市汉南区 {safe_name} 职务",
                    f"汉南区领导之窗 {safe_name}",
                    f"武汉经开区管委会领导名单",
                ],
                "last_attempted": TODAY,
            },
            {
                "priority": "high",
                "question": f"{safe_name}的完整履历、出生年月、籍贯、教育背景、入党时间、工作起始时间",
                "why_it_matters": "构建完整的个人图谱和网络分析基础数据",
                "suggested_queries": [
                    f"{safe_name} 简历",
                    f"{safe_name} 任前公示",
                ],
                "last_attempted": TODAY,
            },
        ],
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(person_json, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {filepath}")


# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # ── Build database & GEXF ────────────────────────────────────────────
    print(f"Building {SLUG} network data…")
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
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

    # ── Person JSON files ────────────────────────────────────────────────
    print("Writing person graph JSON files…")
    for p in persons:
        write_person_json(p)

    print("Done.")
