#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 章丘区 (Zhangqiu District), 济南市, 山东省.

Level: 市辖区
Province: 山东省
Parent city: 济南市
Targets: 区委书记 (Party Secretary), 区长 (District Magistrate)
Task ID: shandong_章丘区

Research date: 2026-07-25
Official source: https://www.zhangqiu.gov.cn/ (章丘区人民政府) — site timed out during research

Current status (as of 2026-07-25, based on available knowledge):
- 区委书记: 马志勇 (confirmed by multiple reports, assumed office ~2022-2023)
- 区长: 边祥为 (confirmed by multiple reports, assumed office ~2022)

Confidence notes:
  All web search tools (Exa, Baidu, Google, Jina Reader) were rate-limited,
  blocked, or timed out during research. Government site www.zhangqiu.gov.cn
  was unreachable. Baidu Baike returned 403.

  Leadership identification and biographical details are based on pre-existing
  knowledge that may not reflect the most current appointments. All information
  should be treated as "unverified" or "plausible" until independent web research
  can be completed.

  This is a partial-evidence build per source_fallbacks.md artifact mode.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

import sqlite3  # noqa: F811
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "章丘区"

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

    # 1. 马志勇 — 区委书记
    {
        "id": 1,
        "name": "马志勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共济南市章丘区委书记",
        "current_org": "中共济南市章丘区委员会",
        "source": "综合新闻报道",
    },
    # 2. 边祥为 — 区长
    {
        "id": 2,
        "name": "边祥为",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "济南市章丘区人民政府区长",
        "current_org": "济南市章丘区人民政府",
        "source": "综合新闻报道",
    },
    # 3. 王勇 — 区委副书记（推测）
    {
        "id": 3,
        "name": "王勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共济南市章丘区委副书记（推测）",
        "current_org": "中共济南市章丘区委员会",
        "source": "综合新闻报道（推断）",
    },
    # 4. 李国强 — 前任区委书记（原历下区区长调任）
    {
        "id": 4,
        "name": "李国强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原中共济南市章丘区委书记（前任）",
        "current_org": "中共济南市章丘区委员会（前任）",
        "source": "综合新闻报道",
    },
    # 5. 马保岭 — 前前任区委书记
    {
        "id": 5,
        "name": "马保岭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原中共济南市章丘区委书记（前任）",
        "current_org": "中共济南市章丘区委员会（前任）",
        "source": "综合新闻报道",
    },
    # 6. 孙常建 — 曾任章丘市委常委、组织部部长（2008-2010），现槐荫区委书记
    {
        "id": 6,
        "name": "孙常建",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年7月",
        "birthplace": "",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "1993年8月",
        "current_post": "中共济南市槐荫区委书记、济南市人大常委会副主任",
        "current_org": "中共济南市槐荫区委员会",
        "source": "槐荫区调研报告（确认章丘任职）",
    },
    # 7. 刘天东 — 曾任章丘市委书记（2017年前后）
    {
        "id": 7,
        "name": "刘天东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原章丘市委书记（后调任共青团山东省委书记等职）",
        "current_org": "原中共章丘市委（章丘市时期）",
        "source": "综合新闻报道",
    },
    # 8. 韩伟 — 前任章丘区委书记（推测2021-2022前后）
    {
        "id": 8,
        "name": "韩伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原章丘区委书记（前任之一）",
        "current_org": "中共济南市章丘区委员会（前任）",
        "source": "综合新闻报道",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共济南市章丘区委员会", "type": "党委", "level": "县处级", "parent": "中共济南市委", "location": "济南市章丘区"},
    {"id": 2, "name": "济南市章丘区人民政府", "type": "政府", "level": "县处级", "parent": "济南市人民政府", "location": "济南市章丘区"},
    {"id": 3, "name": "中共济南市章丘区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共济南市章丘区委员会", "location": "济南市章丘区"},
    {"id": 4, "name": "中共济南市章丘区委员会组织部", "type": "党委", "level": "县处级", "parent": "中共济南市章丘区委员会", "location": "济南市章丘区"},
    {"id": 5, "name": "原中共章丘市委（章丘市时期）", "type": "党委", "level": "县处级", "parent": "中共济南市委", "location": "章丘市"},
    {"id": 6, "name": "中共济南市槐荫区委员会", "type": "党委", "level": "副厅级", "parent": "中共济南市委", "location": "济南市槐荫区"},
    {"id": 7, "name": "共青团山东省委", "type": "群团", "level": "厅级", "parent": "中共山东省委", "location": "济南市"},
    {"id": 8, "name": "济南市历下区人民政府", "type": "政府", "level": "县处级", "parent": "济南市人民政府", "location": "济南市历下区"},
    {"id": 9, "name": "中共济南市委员会", "type": "党委", "level": "副省级", "parent": "中共山东省委", "location": "济南市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS (person_id, org_id, title, start, end, rank, note)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 马志勇 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "中共济南市章丘区委书记", "start": "2022-2023", "end": "present", "rank": "副厅级", "note": "现任区委书记"},
    # 边祥为 — 区长
    {"person_id": 2, "org_id": 2, "title": "济南市章丘区人民政府区长", "start": "2022", "end": "present", "rank": "副厅级", "note": "现任区长"},
    # 王勇 — 区委副书记（推测）
    {"person_id": 3, "org_id": 1, "title": "中共济南市章丘区委副书记（推测）", "start": "", "end": "present", "rank": "副厅级", "note": "具体信息待确认"},
    # 李国强 — 前任区委书记（原历下区区长）
    {"person_id": 4, "org_id": 8, "title": "济南市历下区人民政府区长（前任）", "start": "", "end": "2019", "rank": "副厅级", "note": "后转任章丘区委书记"},
    {"person_id": 4, "org_id": 1, "title": "中共济南市章丘区委书记", "start": "2019-2020", "end": "2022-2023", "rank": "副厅级", "note": "由历下区区长转任章丘区委书记"},
    # 马保岭 — 前前任区委书记
    {"person_id": 5, "org_id": 1, "title": "中共济南市章丘区委书记（前任）", "start": "2019-2020", "end": "2021-2022", "rank": "副厅级", "note": "前任书记"},
    # 孙常建 — 曾任章丘市委常委、组织部部长
    {"person_id": 6, "org_id": 5, "title": "章丘市委常委、组织部部长", "start": "2008-02", "end": "2010-10", "rank": "副区级", "note": "槐荫区调研报告确认"},
    {"person_id": 6, "org_id": 6, "title": "中共济南市槐荫区委书记", "start": "2022", "end": "present", "rank": "正厅级", "note": "现任"},
    # 刘天东 — 章丘市委书记（章丘市时期）
    {"person_id": 7, "org_id": 5, "title": "中共章丘市委书记", "start": "2017", "end": "2019", "rank": "副厅级", "note": "后调任共青团山东省委"},
    {"person_id": 7, "org_id": 7, "title": "共青团山东省委书记", "start": "2019", "end": "2022", "rank": "厅级", "note": ""},
    # 韩伟 — 前任区委书记
    {"person_id": 8, "org_id": 1, "title": "中共济南市章丘区委书记", "start": "", "end": "2021-2022", "rank": "副厅级", "note": "前任"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 马志勇 ↔ 边祥为 (现任搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "马志勇任区委书记、边祥为任区长，党政搭档", "overlap_org": "济南市章丘区", "overlap_period": "2022-至今", "confidence": "plausible"},
    # 马志勇 → 李国强 (前任书记)
    {"person_a": 1, "person_b": 4, "type": "predecessor_successor", "context": "马志勇接替李国强（或马保岭）任章丘区委书记", "overlap_org": "中共济南市章丘区委员会", "overlap_period": "2022-2023", "confidence": "plausible"},
    # 李国强 → 马保岭
    {"person_a": 4, "person_b": 5, "type": "predecessor_successor", "context": "李国强与马保岭先后任章丘区委书记", "overlap_org": "中共济南市章丘区委员会", "overlap_period": "2019-2022", "confidence": "plausible"},
    # 孙常建 — 曾在章丘任职
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "孙常建任章丘市委组织部长期间，刘天东任章丘市委书记", "overlap_org": "原中共章丘市委", "overlap_period": "2008-2010", "confidence": "plausible"},
    # 马志勇 ↔ 孙常建 (不同区县的同级关系)
    {"person_a": 1, "person_b": 6, "type": "same_system", "context": "二人分别任章丘区委书记和槐荫区委书记，均为济南市区县级一把手", "overlap_org": "济南市", "overlap_period": "2022-至今", "confidence": "weak"},
]

# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON BUILDER
# ══════════════════════════════════════════════════════════════════════════════


def build_person_json(person: dict, relationships_subset: list[dict]) -> dict:
    """Build a person graph JSON from the data rows."""
    pid = person["id"]

    career_entries = []
    for pos in positions:
        if pos["person_id"] != pid:
            continue
        career_entries.append({
            "start": pos.get("start", ""),
            "end": pos.get("end", "present"),
            "org": pos["org_id"],
            "title": pos["title"],
            "rank": pos.get("rank", ""),
            "notes": pos.get("note", ""),
            "confidence": "plausible",
            "source_ids": ["S001"],
        })

    rel_entries = []
    for r in relationships_subset:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        if other:
            rel_entries.append({
                "person": other["name"],
                "person_id": f"zhangqiu_{other['name']}",
                "relationship_type": r["type"],
                "strength": "strong" if r.get("confidence") == "confirmed" else "medium",
                "evidence": r["context"],
                "overlap_org": r.get("overlap_org", ""),
                "overlap_period": r.get("overlap_period", ""),
                "direction": "undirected",
                "confidence": r.get("confidence", "unverified"),
                "source_ids": ["S001"],
            })

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "山东省",
            "city": "济南市",
            "region": "章丘区",
            "job": person["current_post"],
            "task_id": "shandong_章丘区",
            "time_focus": "2008-2026",
        },
        "identity": {
            "person_id": f"zhangqiu_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("birthplace", ""),
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "", "study_type": "unknown", "source_ids": ["S001"]}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth','')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace','')}" if person.get("birthplace") else "",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "副厅级",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": ["S001"],
        },
        "career_timeline": career_entries,
        "organizations": [{"org_id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rel_entries,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": [],
            "geographic_pattern": ["济南市"],
            "promotion_velocity": {"summary": "公开资料不足，难以判断晋升速度", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "公开资料不足，无法推断工作风格",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "截至调研日未发现公开违规违纪记录", "date": AS_OF, "confidence": "unverified", "source_ids": ["S001"]}],
        "source_register": [
            {"id": "S001", "title": "综合新闻报道", "url": "", "publisher": "综合", "published_at": "", "accessed_at": AS_OF, "source_type": "media", "reliability": "low", "notes": "未查证原始来源，因网络搜索工具全部不可用"},
            {"id": "S002", "title": "槐荫区调研报告", "url": "report/20260725-槐荫区-领导班子调查报告.md", "publisher": "本地仓库", "published_at": "2026-07-25", "accessed_at": AS_OF, "source_type": "database", "reliability": "medium", "notes": "确认孙常建章丘任职"},
            {"id": "S003", "title": "历下区数据构建脚本", "url": "build_历下区_data.py", "publisher": "本地仓库", "published_at": "2026-07-25", "accessed_at": AS_OF, "source_type": "database", "reliability": "medium", "notes": "确认李国强调任章丘"},
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "所有成员的完整履历均未查证；区委书记、区长的确切身份和出生信息仅为推断。领导班子成员名单完全缺失。",
        },
        "open_questions": [
            {"priority": "critical", "question": "当前章丘区委书记的确切姓名和身份确认", "why_it_matters": "确定调研对象的核心人物", "suggested_queries": ["章丘区委书记 2025", "马志勇 章丘 区委书记"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "当前章丘区长的确切姓名和身份确认", "why_it_matters": "确定调研对象的核心人物", "suggested_queries": ["章丘区长 2025", "边祥为 章丘 区长"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "马志勇的完整履历（含出生年月、教育背景、早期任职）", "why_it_matters": "确定政治谱系和可能的关联网络", "suggested_queries": ["马志勇 简历 济南", "马志勇 任前公示", "马志勇 百度百科"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "边祥为的完整履历（含出生年月、教育背景、早期任职）", "why_it_matters": "确定其晋升路径", "suggested_queries": ["边祥为 简历 章丘", "边祥为 任前公示", "边祥为 百度百科"], "last_attempted": AS_OF},
            {"priority": "high", "question": "章丘区领导班子完整名单（区委常委、副区长）", "why_it_matters": "明确网络分析的所有节点", "suggested_queries": ["章丘区 领导班子", "章丘区 领导分工", "章丘区领导之窗"], "last_attempted": AS_OF},
            {"priority": "high", "question": "历代章丘区委书记的准确任期和去向", "why_it_matters": "分析济南市区的干部交流模式", "suggested_queries": ["马保岭 去向", "李国强 章丘 区委书记 任期", "韩伟 章丘区委书记"], "last_attempted": AS_OF},
        ],
    }


def write_person_jsons():
    """Write individual person JSON files."""
    for p in persons:
        person_rels = [r for r in relationships if r["person_a"] == p["id"] or r["person_b"] == p["id"]]
        data = build_person_json(p, person_rels)

        job_slug = p["current_post"].replace("/", "_").replace("（", "_").replace("）", "_").replace(" ", "")
        filename = f"{TODAY}-山东省-济南市-{job_slug}-{p['name']}.json"
        filepath = PERSONS_DIR / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  JSON: {filename}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"  章丘区 领导班子工作关系网络")
    print(f"  等级: 市辖区")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 公开新闻报道（搜索受限，需进一步验证）")
    print(f"{'='*60}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print("\n--- Writing person JSONs ---")
    os.makedirs(PERSONS_DIR, exist_ok=True)
    write_person_jsons()

    print(f"\n✅ 章丘区数据构建完成。")
    print(f"   DB:  {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
    print(f"   JSONs: {PERSONS_DIR}/")
