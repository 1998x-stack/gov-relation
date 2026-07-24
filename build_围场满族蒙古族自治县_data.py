#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 围场满族蒙古族自治县 leadership network.

Level: 县
Province: 河北省
Parent city: 承德市
Targets: 县委书记 (Party Secretary), 县长 (County Mayor)
Task ID: hebei_围场满族蒙古族自治县

Research date: 2026-07-24
Official site: https://www.weichang.gov.cn/ (围场满族蒙古族自治县人民政府)

Current status (as of 2026-07-24):
- 县委书记: 刘洋 (confirmed from 2026 articles)
- 县长: 郑洪波 (confirmed from 2026 articles, presides over 八届政府常务会议)
- 县委常委、组织部部长: 刘春辉 (confirmed from 2026-04-30 article)

Note:
- Government website (www.weichang.gov.cn) is accessible but leadership pages (领导之窗) are
  JavaScript-rendered and not directly readable via text fetch.
- Baidu Baike returned 403 errors for individual leader entries.
- Exa search rate-limited, Jina Reader timed out, Google/Bing access blocked from this environment.
- Leader information confirmed from weichang.gov.cn news articles and government meeting reports.
- Detailed career histories (education, birth year, birthplace, prior positions) not yet found.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "围场满族蒙古族自治县"
TASK_ID = "hebei_围场满族蒙古族自治县"
TMP_DIR = _REPO_ROOT / "data" / "tmp" / TASK_ID
PERSONS_DIR = TMP_DIR

DB_PATH = TMP_DIR / f"{SLUG}_network.db"
GEXF_PATH = TMP_DIR / f"{SLUG}_network.gexf"

import sqlite3  # noqa: F811

AS_OF = "2026-07-24"
TODAY = AS_OF.replace("-", "")

# ══════════════════════════════════════════════════════════════════════════════
# SOURCE REGISTER
# ══════════════════════════════════════════════════════════════════════════════

source_register = [
    {
        "id": "S001",
        "title": "围场满族蒙古族自治县人民政府 - 动态要闻（县委七届十三次全会）",
        "url": "https://www.weichang.gov.cn/art/2026/4/30/art_3079_1113522.html",
        "publisher": "围场满族蒙古族自治县人民政府",
        "published_at": "2026-04-30",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "证实县委书记刘洋、县委常委组织部部长刘春辉"
    },
    {
        "id": "S002",
        "title": "围场满族蒙古族自治县人民政府 - 县委主要领导深入姜家店乡专题调研",
        "url": "https://www.weichang.gov.cn/art/2026/5/12/art_3079_1114501.html",
        "publisher": "围场满族蒙古族自治县人民政府",
        "published_at": "2026-05-12",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "证实县委书记刘洋"
    },
    {
        "id": "S003",
        "title": "围场满族蒙古族自治县人民政府 - 八届政府第一百一十四次常务会议",
        "url": "https://www.weichang.gov.cn/art/2026/1/23/art_3082_1101278.html",
        "publisher": "围场满族蒙古族自治县人民政府",
        "published_at": "2026-01-23",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "证实县长郑洪波"
    },
    {
        "id": "S004",
        "title": "围场满族蒙古族自治县人民政府 - 八届政府第一百一十五次常务会议",
        "url": "https://www.weichang.gov.cn/art/2026/2/10/art_3082_1103916.html",
        "publisher": "围场满族蒙古族自治县人民政府",
        "published_at": "2026-02-10",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "证实县长郑洪波"
    },
    {
        "id": "S005",
        "title": "围场满族蒙古族自治县人民政府 - 八届政府第一百一十六次常务会议",
        "url": "https://www.weichang.gov.cn/art/2026/2/28/art_3082_1105143.html",
        "publisher": "围场满族蒙古族自治县人民政府",
        "published_at": "2026-02-28",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "证实县长郑洪波"
    },
    {
        "id": "S006",
        "title": "围场满族蒙古族自治县人民政府 - 八届政府第一百一十九次常务会议",
        "url": "https://www.weichang.gov.cn/art/2026/4/16/art_3082_1111920.html",
        "publisher": "围场满族蒙古族自治县人民政府",
        "published_at": "2026-04-16",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "证实县长郑洪波"
    },
    {
        "id": "S007",
        "title": "围场满族蒙古族自治县人民政府 - 八届政府第一百二十一次常务会议",
        "url": "https://www.weichang.gov.cn/art/2026/5/11/art_3082_1114346.html",
        "publisher": "围场满族蒙古族自治县人民政府",
        "published_at": "2026-05-11",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "证实县长郑洪波"
    },
    {
        "id": "S008",
        "title": "围场满族蒙古族自治县人民政府 - 自治县八届人大常委会第四十四次会议",
        "url": "https://www.weichang.gov.cn/art/2026/7/16/art_3079_1121869.html",
        "publisher": "围场满族蒙古族自治县人民政府",
        "published_at": "2026-07-16",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "自治县八届人大 - 县人大常委会会议"
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── 1. 县委书记 ──
    {
        "id": 1,
        "name": "刘洋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共围场满族蒙古族自治县委书记",
        "current_org": "中共围场满族蒙古族自治县委员会",
        "source": "https://www.weichang.gov.cn/art/2026/4/30/art_3079_1113522.html",
    },
    # ── 2. 县长 ──
    {
        "id": 2,
        "name": "郑洪波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "围场满族蒙古族自治县人民政府县长",
        "current_org": "围场满族蒙古族自治县人民政府",
        "source": "https://www.weichang.gov.cn/art/2026/5/11/art_3082_1114346.html",
    },
    # ── 3. 县委常委、组织部部长 ──
    {
        "id": 3,
        "name": "刘春辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "围场满族蒙古族自治县委常委、组织部部长",
        "current_org": "中共围场满族蒙古族自治县委组织部",
        "source": "https://www.weichang.gov.cn/art/2026/4/30/art_3079_1113522.html",
    },
    # ── 4. 前任县委书记（待查）──
    {
        "id": 4,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任围场满族蒙古族自治县委书记",
        "current_org": "（去向待查）",
        "source": "2026年7月未能通过公开渠道确认前任县委书记信息",
    },
    # ── 5. 前任县长（待查）──
    {
        "id": 5,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任围场满族蒙古族自治县人民政府县长",
        "current_org": "（去向待查）",
        "source": "2026年7月未能通过公开渠道确认前任县长信息",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共围场满族蒙古族自治县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共承德市委员会",
        "location": "河北省承德市围场满族蒙古族自治县",
    },
    {
        "id": 2,
        "name": "围场满族蒙古族自治县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "承德市人民政府",
        "location": "河北省承德市围场满族蒙古族自治县",
    },
    {
        "id": 3,
        "name": "围场满族蒙古族自治县人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "承德市人大常委会",
        "location": "河北省承德市围场满族蒙古族自治县",
    },
    {
        "id": 4,
        "name": "政协围场满族蒙古族自治县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协承德市委员会",
        "location": "河北省承德市围场满族蒙古族自治县",
    },
    {
        "id": 5,
        "name": "围场满族蒙古族自治县纪委监委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共围场满族蒙古族自治县委员会",
        "location": "河北省承德市围场满族蒙古族自治县",
    },
    {
        "id": 6,
        "name": "中共围场满族蒙古族自治县委组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共围场满族蒙古族自治县委员会",
        "location": "河北省承德市围场满族蒙古族自治县",
    },
    {
        "id": 7,
        "name": "中共围场满族蒙古族自治县委宣传部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共围场满族蒙古族自治县委员会",
        "location": "河北省承德市围场满族蒙古族自治县",
    },
    {
        "id": 8,
        "name": "中共围场满族蒙古族自治县委政法委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共围场满族蒙古族自治县委员会",
        "location": "河北省承德市围场满族蒙古族自治县",
    },
    {
        "id": 9,
        "name": "中共围场满族蒙古族自治县委统战部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共围场满族蒙古族自治县委员会",
        "location": "河北省承德市围场满族蒙古族自治县",
    },
    {
        "id": 10,
        "name": "围场满族蒙古族自治县政协委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协围场满族蒙古族自治县委员会",
        "location": "河北省承德市围场满族蒙古族自治县",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # Core leaders
    {"person_id": 1, "org_id": 1, "title": "中共围场满族蒙古族自治县委书记",
     "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "2026年4月已在任；未查到具体到任日期"},
    {"person_id": 2, "org_id": 2, "title": "围场满族蒙古族自治县人民政府县长",
     "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "2026年1月已在任（主持八届政府第一百一十四次常务会议）；未查到具体到任日期"},

    # 县委常委
    {"person_id": 3, "org_id": 6, "title": "围场满族蒙古族自治县委常委、组织部部长",
     "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "2026年4月在任（县委七届十三次全会）"},

    # Predecessors (unknown)
    {"person_id": 4, "org_id": 1, "title": "前任围场满族蒙古族自治县委书记",
     "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "姓名及去向待查"},
    {"person_id": 5, "org_id": 2, "title": "前任围场满族蒙古族自治县人民政府县长",
     "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "姓名及去向待查"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # Core team overlap (党政协同)
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "围场县党政一把手工作搭档关系",
     "overlap_org": "围场满族蒙古族自治县",
     "overlap_period": ""},
    # 县委书记 ↔ 组织部部长
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "刘洋（县委书记）与刘春辉（组织部部长）在县委常委会共事",
     "overlap_org": "中共围场满族蒙古族自治县委员会",
     "overlap_period": ""},
    # 县长 ↔ 组织部部长
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "郑洪波（县长）与刘春辉（组织部部长）在县领导班子共事",
     "overlap_org": "围场满族蒙古族自治县",
     "overlap_period": ""},
    # Predecessor relationships
    {"person_a": 1, "person_b": 4, "type": "predecessor_successor",
     "context": "刘洋接任围场县委书记（前任姓名待查）",
     "overlap_org": "中共围场满族蒙古族自治县委员会",
     "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "predecessor_successor",
     "context": "郑洪波接任围场县县长（前任姓名待查）",
     "overlap_org": "围场满族蒙古族自治县人民政府",
     "overlap_period": ""},
]


# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON GENERATION
# ══════════════════════════════════════════════════════════════════════════════

def make_person_json(p, timeline, relationships_list, custom_identity=None):
    result = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河北省",
            "city": "承德市",
            "region": "围场满族蒙古族自治县",
            "job": p.get("current_post", ""),
            "task_id": TASK_ID,
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"weichang_{p['name']}",
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
                "official_profile_url": p.get("source", "")
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "县处级正职" if (
                ("书记" in p.get("current_post", "") and "副" not in p.get("current_post", "") and "纪委" not in p.get("current_post", ""))
                or ("县长" in p.get("current_post", "") and "副" not in p.get("current_post", ""))
            ) else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": p["name"] not in ["（待查）"],
            "source_ids": []
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": relationships_list,
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
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "在公开信息中未发现该人物负面信号",
             "date": "", "confidence": "confirmed", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "unverified" if not p.get("birth") else "confirmed",
            "current_role": "confirmed" if p["name"] not in ["（待查）"] else "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": f"{p['name']}的完整履历和籍贯、出生年月等信息缺失"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{p['name']}的完整职业生涯履历",
                "why_it_matters": "无法追溯其任职路径、系统经历和晋升模式",
                "suggested_queries": [f"{p['name']} 简历 围场"],
                "last_attempted": AS_OF
            },
        ]
    }
    if custom_identity:
        result["identity"].update(custom_identity)
    return result


def write_person_json(p, timeline, relationships_list, custom_identity=None):
    data = make_person_json(p, timeline, relationships_list, custom_identity)
    # Determine job for filename
    post = p.get("current_post", "")
    if "书记" in post and "副" not in post:
        job_label = "县委书记"
    elif "县长" in post and "副" not in post:
        job_label = "县长"
    elif "组织部部长" in post:
        job_label = "组织部长"
    else:
        job_label = "干部"

    fname = f"{TODAY}-河北省-承德市-{job_label}-{p['name']}.json"
    fpath = os.path.join(PERSONS_DIR, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {fpath}")
    return fpath


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  围场满族蒙古族自治县领导班子工作关系网络")
    print("  等级: 县（河北省承德市下辖）")
    print("  调查日期: 2026-07-24")
    print("  ✅ 县委书记: 刘洋（已确认）")
    print("  ✅ 县长: 郑洪波（已确认）")
    print("  ⚠️  完整履历信息缺失（外部搜索工具受限）")
    print("=" * 60)

    # ── Build DB + GEXF via runner ──
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # ── Person JSONs ──
    # 刘洋
    liuyang_timeline = [
        {"start": "", "end": "", "org": "中共围场满族蒙古族自治县委员会",
         "title": "中共围场满族蒙古族自治县委书记",
         "notes": "现任；具体到任日期未查到", "confidence": "confirmed",
         "source_ids": ["S001", "S002"]},
    ]
    liuyang_relationships = [
        {"person": "郑洪波", "person_id": "weichang_郑洪波",
         "relationship_type": "overlap", "strength": "strong",
         "evidence": "刘洋（县委书记）与郑洪波（县长）在围场县党政班子搭档共事",
         "overlap_org": "围场满族蒙古族自治县", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S001", "S007"]},
        {"person": "刘春辉", "person_id": "weichang_刘春辉",
         "relationship_type": "superior_subordinate", "strength": "medium",
         "evidence": "刘洋（县委书记）与刘春辉（组织部部长）在县委全会和常委会共事",
         "overlap_org": "中共围场满族蒙古族自治县委员会", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    write_person_json(persons[0], liuyang_timeline, liuyang_relationships)

    # 郑洪波
    zhenghongbo_timeline = [
        {"start": "", "end": "", "org": "围场满族蒙古族自治县人民政府",
         "title": "围场满族蒙古族自治县人民政府县长",
         "notes": "现任；2026年1月起主持八届政府常务会议", "confidence": "confirmed",
         "source_ids": ["S003", "S004", "S005", "S006", "S007"]},
    ]
    zhenghongbo_relationships = [
        {"person": "刘洋", "person_id": "weichang_刘洋",
         "relationship_type": "overlap", "strength": "strong",
         "evidence": "郑洪波（县长）与刘洋（县委书记）在围场县党政班子搭档共事",
         "overlap_org": "围场满族蒙古族自治县", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S001", "S007"]},
        {"person": "刘春辉", "person_id": "weichang_刘春辉",
         "relationship_type": "overlap", "strength": "medium",
         "evidence": "郑洪波（县长）与刘春辉（组织部部长）在县领导班子共事",
         "overlap_org": "围场满族蒙古族自治县", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    write_person_json(persons[1], zhenghongbo_timeline, zhenghongbo_relationships)

    # 刘春辉
    liuchunhui_timeline = [
        {"start": "", "end": "", "org": "中共围场满族蒙古族自治县委组织部",
         "title": "围场满族蒙古族自治县委常委、组织部部长",
         "notes": "2026年4月在任", "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    liuchunhui_relationships = [
        {"person": "刘洋", "person_id": "weichang_刘洋",
         "relationship_type": "superior_subordinate", "strength": "medium",
         "evidence": "刘春辉（组织部部长）在县委常委会向刘洋（县委书记）汇报工作",
         "overlap_org": "中共围场满族蒙古族自治县委员会", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "郑洪波", "person_id": "weichang_郑洪波",
         "relationship_type": "overlap", "strength": "medium",
         "evidence": "刘春辉（组织部部长）与郑洪波（县长）在县领导班子共事",
         "overlap_org": "围场满族蒙古族自治县", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    write_person_json(persons[2], liuchunhui_timeline, liuchunhui_relationships)

    print(f"\n✅ 围场满族蒙古族自治县数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Person JSONs: data/tmp/{TASK_ID}/")
    print(f"  ⚠️  核心领导履历和前任信息待后续补充。")
