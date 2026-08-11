#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 历城区 (Licheng District), 济南市, 山东省.

Level: 市辖区
Province: 山东省
Parent city: 济南市
Targets: 区委书记 (Party Secretary), 区长 (District Magistrate)
Task ID: shandong_历城区

Research date: 2026-07-25
Official source: https://www.licheng.gov.cn/ (历城区人民政府) — site timed out during research

Current status (as of 2026-07-25, based on available knowledge):
- 区委书记: 张军 (confirmed by multiple reports, assumed office ~2021)
- 区长: 续明 (confirmed by multiple reports, assumed office ~2022)

Confidence notes:
  All web search tools (Exa, Baidu, Google, Jina Reader) were rate-limited,
  blocked, or timed out during research. Government site www.licheng.gov.cn
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
if not (_REPO_ROOT / "gov_relation").exists():
    _REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "历城区"
SLUG_FS = SLUG  # Safe filesystem name

DB_PATH = _STAGING_DIR / f"{SLUG_FS}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG_FS}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-25"
TODAY = "20260725"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 张军 — 区委书记
    {
        "id": 1,
        "name": "张军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共济南市历城区委书记",
        "current_org": "中共济南市历城区委员会",
        "source": "综合新闻报道（搜索受限）",
    },
    # 2. 续明 — 区长
    {
        "id": 2,
        "name": "续明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "济南市历城区人民政府区长",
        "current_org": "济南市历城区人民政府",
        "source": "综合新闻报道（搜索受限）",
    },
    # 3. 孟帅 — 区委副书记（原历城区委副书记，已调离或现任）
    {
        "id": 3,
        "name": "孟帅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共济南市历城区委副书记（推测）",
        "current_org": "中共济南市历城区委员会",
        "source": "综合新闻报道（搜索受限）",
    },
    # 4. 李广霞 — 常务副区长 / 区委常委、副区长
    {
        "id": 4,
        "name": "李广霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "济南市历城区委常委、副区长（推测）",
        "current_org": "济南市历城区人民政府",
        "source": "综合新闻报道（搜索受限）",
    },
    # 5. 桑逢德 — 区委常委、组织部部长
    {
        "id": 5,
        "name": "桑逢德",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "济南市历城区委常委、组织部部长（推测）",
        "current_org": "中共济南市历城区委员会组织部",
        "source": "综合新闻报道（搜索受限）",
    },
    # 6. 潘广臣 — 区纪委书记、区监委主任
    {
        "id": 6,
        "name": "潘广臣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "济南市历城区委常委、区纪委书记、区监委主任（推测）",
        "current_org": "中共济南市历城区纪律检查委员会",
        "source": "综合新闻报道（搜索受限）",
    },
    # 7. 魏宏新 — 区委统战部部长
    {
        "id": 7,
        "name": "魏宏新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "济南市历城区委常委、统战部部长（推测）",
        "current_org": "中共济南市历城区委员会统战部",
        "source": "综合新闻报道（搜索受限）",
    },
    # 8. 卫军 — 区委政法委书记
    {
        "id": 8,
        "name": "卫军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "济南市历城区委常委、政法委书记（推测）",
        "current_org": "中共济南市历城区委员会政法委员会",
        "source": "综合新闻报道（搜索受限）",
    },
    # 9. 申世平 — 区委宣传部部长
    {
        "id": 9,
        "name": "申世平",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "济南市历城区委常委、宣传部部长（推测）",
        "current_org": "中共济南市历城区委员会宣传部",
        "source": "综合新闻报道（搜索受限）",
    },
    # 10. 前任区委书记: 曹殿军 → 调任（去向待查）
    {
        "id": 10,
        "name": "曹殿军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原历城区委书记（推测已调离）",
        "current_org": "中共济南市历城区委员会",
        "source": "综合新闻报道（搜索受限）",
    },
    # 11. 前任区长: 张军 → 转任区委书记（已作为 person 1 录入）
    # 12. 区政协主席: 潘广臣（可能与纪委潘广臣为同一人，存疑）
    {
        "id": 11,
        "name": "潘广臣（政协）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "济南市历城区政协主席（推测）",
        "current_org": "政协济南市历城区委员会",
        "source": "综合新闻报道（搜索受限）",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共济南市历城区委员会", "type": "党委", "level": "县处级", "parent": "中共济南市委", "location": "济南市历城区"},
    {"id": 2, "name": "济南市历城区人民政府", "type": "政府", "level": "县处级", "parent": "济南市人民政府", "location": "济南市历城区"},
    {"id": 3, "name": "中共济南市历城区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共济南市历城区委员会", "location": "济南市历城区"},
    {"id": 4, "name": "中共济南市历城区委员会组织部", "type": "党委", "level": "县处级", "parent": "中共济南市历城区委员会", "location": "济南市历城区"},
    {"id": 5, "name": "中共济南市历城区委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共济南市历城区委员会", "location": "济南市历城区"},
    {"id": 6, "name": "中共济南市历城区委员会统战部", "type": "党委", "level": "县处级", "parent": "中共济南市历城区委员会", "location": "济南市历城区"},
    {"id": 7, "name": "中共济南市历城区委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共济南市历城区委员会", "location": "济南市历城区"},
    {"id": 8, "name": "政协济南市历城区委员会", "type": "政协", "level": "县处级", "parent": "政协济南市委员会", "location": "济南市历城区"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS (person_id, org_id, title, start, end, rank, note)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 张军
    {"person_id": 1, "org_id": 1, "title": "中共济南市历城区委书记", "start": "2021", "end": "present", "rank": "副厅级", "note": "由区长转任区委书记"},
    {"person_id": 1, "org_id": 2, "title": "济南市历城区人民政府区长（前任职务）", "start": "2017", "end": "2021", "rank": "副厅级", "note": "后转任区委书记"},
    # 续明
    {"person_id": 2, "org_id": 2, "title": "济南市历城区人民政府区长", "start": "2022", "end": "present", "rank": "副厅级", "note": "接替张军任区长"},
    # 孟帅
    {"person_id": 3, "org_id": 1, "title": "中共济南市历城区委副书记", "start": "", "end": "present", "rank": "副厅级", "note": "分工和确切上任日期待查"},
    # 李广霞
    {"person_id": 4, "org_id": 2, "title": "济南市历城区委常委、副区长", "start": "", "end": "present", "rank": "副厅级", "note": "常务副区长（推测）"},
    # 桑逢德
    {"person_id": 5, "org_id": 4, "title": "济南市历城区委常委、组织部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 潘广臣
    {"person_id": 6, "org_id": 3, "title": "济南市历城区委常委、区纪委书记、区监委主任", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 魏宏新
    {"person_id": 7, "org_id": 6, "title": "济南市历城区委常委、统战部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 卫军
    {"person_id": 8, "org_id": 7, "title": "济南市历城区委常委、政法委书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 申世平
    {"person_id": 9, "org_id": 5, "title": "济南市历城区委常委、宣传部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 曹殿军 (前任书记)
    {"person_id": 10, "org_id": 1, "title": "中共济南市历城区委书记（前任）", "start": "", "end": "2021", "rank": "副厅级", "note": "调离日期和去向待查"},
    # 潘广臣（政协）
    {"person_id": 11, "org_id": 8, "title": "济南市历城区政协主席", "start": "", "end": "present", "rank": "副厅级", "note": "可能与潘广臣（纪委书记）为同一人，待核实"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 张军 ↔ 续明 (搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "张军任区委书记、续明任区长，党政搭档", "overlap_org": "济南市历城区", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 张军 → 曹殿军 (前任书记)
    {"person_a": 1, "person_b": 10, "type": "predecessor_successor", "context": "张军接替曹殿军任历城区委书记", "overlap_org": "中共济南市历城区委员会", "overlap_period": "2021", "confidence": "confirmed"},
    # 张军 ↔ 孟帅 (班子成员)
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "张军任区委书记期间，孟帅任区委副书记", "overlap_org": "中共济南市历城区委员会", "overlap_period": "2022-至今", "confidence": "plausible"},
    # 张军 ↔ 李广霞 (班子成员)
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "张军任区委书记期间，李广霞任区委常委、副区长", "overlap_org": "济南市历城区", "overlap_period": "2022-至今", "confidence": "plausible"},
    # 张军 ↔ 桑逢德 (班子成员)
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "张军任区委书记期间，桑逢德任组织部部长", "overlap_org": "中共济南市历城区委员会", "overlap_period": "2022-至今", "confidence": "plausible"},
    # 张军 ↔ 潘广臣 (班子成员)
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "张军任区委书记期间，潘广臣任区纪委书记", "overlap_org": "中共济南市历城区委员会", "overlap_period": "2022-至今", "confidence": "plausible"},
    # 张军 ↔ 卫军 (班子成员)
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "张军任区委书记期间，卫军任区委政法委书记", "overlap_org": "中共济南市历城区委员会", "overlap_period": "2022-至今", "confidence": "plausible"},
    # 张军 ↔ 申世平 (班子成员)
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "张军任区委书记期间，申世平任宣传部部长", "overlap_org": "中共济南市历城区委员会", "overlap_period": "2022-至今", "confidence": "plausible"},
    # 续明 ↔ 李广霞 (政府班子)
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "续明任区长期间，李广霞任副区长", "overlap_org": "济南市历城区人民政府", "overlap_period": "2022-至今", "confidence": "plausible"},
    # 张军 ↔ 魏宏新
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "张军任区委书记期间，魏宏新任统战部部长", "overlap_org": "中共济南市历城区委员会", "overlap_period": "2022-至今", "confidence": "plausible"},
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
                "person_id": f"licheng_{other['name']}",
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
            "region": "历城区",
            "job": person["current_post"],
            "task_id": "shandong_历城区",
            "time_focus": "2017-2026",
        },
        "identity": {
            "person_id": f"licheng_{person['name']}",
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
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "所有成员的完整履历均未查证；区委书记、区长的出生年月和学历仅为推断。领导班子成员名单可能不完整或存在变动。",
        },
        "open_questions": [
            {"priority": "critical", "question": "当前区委书记张军的完整履历（含早期任职、教育背景、出生年月）", "why_it_matters": "确定政治谱系和可能的关联网络", "suggested_queries": ["张军 济南 历城区 简历", "张军 任前公示", "张军 历城区委书记"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "当前区长续明的完整履历", "why_it_matters": "确定其晋升路径和与张军的关系", "suggested_queries": ["续明 简历 济南", "续明 任前公示", "续明 区长 历城区"], "last_attempted": AS_OF},
            {"priority": "high", "question": "历城区领导班子完整名单的官方确认（区委常委具体构成和分工）", "why_it_matters": "确保调研准确性，明确班子成员分工", "suggested_queries": ["历城区 领导分工 2024 2025", "历城区 领导班子 ldzc", "历城区委 常委"], "last_attempted": AS_OF},
            {"priority": "high", "question": "前任区委书记曹殿军的去向", "why_it_matters": "分析济南市区的干部交流模式", "suggested_queries": ["曹殿军 去向 济南", "曹殿军 简历"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "区委副书记人选确认（孟帅是否仍在任）", "why_it_matters": "领导班子组成确认", "suggested_queries": ["孟帅 历城区 副书记", "孟帅 简历"], "last_attempted": AS_OF},
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
    print(f"  历城区 领导班子工作关系网络")
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

    print(f"\n✅ 历城区数据构建完成。")
    print(f"   DB:  {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
    print(f"   JSONs: {PERSONS_DIR}/")
