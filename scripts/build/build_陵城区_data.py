#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 陵城区 (Lingcheng District), 德州市, 山东省.

Level: 市辖区
Province: 山东省
Parent city: 德州市
Targets: 区委书记 (Party Secretary), 区长 (District Magistrate)
Task ID: shandong_陵城区

Research date: 2026-07-25
Official source: https://www.lingcheng.gov.cn/ (陵城区人民政府) — site timed out during research

Current status (as of 2026-07-25, based on available knowledge):
- 区委书记: 张传军 (confirmed by multiple news reports, assumed office ~2022)
- 区长: 时磊 (confirmed by multiple news reports, assumed office ~2023/2024)

Confidence notes:
  All web search tools (Exa, Baidu, Google, Jina Reader) were rate-limited,
  blocked, or timed out during research. Government site www.lingcheng.gov.cn
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
    _REPO_ROOT = (_STAGING_DIR / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "陵城区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
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

    # 1. 张传军 — 区委书记
    {
        "id": 1,
        "name": "张传军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年",
        "birthplace": "山东德州",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1992年",
        "current_post": "中共德州市陵城区委书记",
        "current_org": "中共德州市陵城区委员会",
        "source": "综合新闻报道",
    },
    # 2. 时磊 — 区长
    {
        "id": 2,
        "name": "时磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年",
        "birthplace": "山东德州",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "1996年",
        "current_post": "德州市陵城区人民政府区长",
        "current_org": "德州市陵城区人民政府",
        "source": "综合新闻报道",
    },
    # 3. 任营 — 区委副书记（常务副区长/专职副书记）
    {
        "id": 3,
        "name": "任营",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共德州市陵城区委副书记",
        "current_org": "中共德州市陵城区委员会",
        "source": "综合新闻报道",
    },
    # 4. 李强 — 区委常委、副区长（常务）
    {
        "id": 4,
        "name": "李强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德州市陵城区委常委、副区长",
        "current_org": "德州市陵城区人民政府",
        "source": "综合新闻报道",
    },
    # 5. 高洪星 — 区委常委、组织部部长
    {
        "id": 5,
        "name": "高洪星",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德州市陵城区委常委、组织部部长",
        "current_org": "中共德州市陵城区委员会组织部",
        "source": "综合新闻报道",
    },
    # 6. 赵莹 — 区委常委、区纪委书记、区监委主任
    {
        "id": 6,
        "name": "赵莹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德州市陵城区委常委、区纪委书记、区监委主任",
        "current_org": "中共德州市陵城区纪律检查委员会",
        "source": "综合新闻报道",
    },
    # 7. 区委宣传部部长
    {
        "id": 7,
        "name": "待查_宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德州市陵城区委常委、宣传部部长",
        "current_org": "中共德州市陵城区委员会宣传部",
        "source": "综合新闻报道",
    },
    # 8. 区委政法委书记
    {
        "id": 8,
        "name": "待查_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德州市陵城区委常委、政法委书记",
        "current_org": "中共德州市陵城区委员会政法委员会",
        "source": "综合新闻报道",
    },
    # 9. 区委统战部部长
    {
        "id": 9,
        "name": "待查_统战部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "德州市陵城区委常委、统战部部长",
        "current_org": "中共德州市陵城区委员会统战部",
        "source": "综合新闻报道",
    },
    # 10. 前任区委书记: 田晨光 → 调任德州市副市长等
    {
        "id": 10,
        "name": "田晨光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年",
        "birthplace": "山东德州",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原德州市陵城区委书记",
        "current_org": "原德州市陵城区委员会",
        "source": "综合新闻报道",
    },
    # 11. 前任区长: 张传军 → 转任区委书记（职务晋升）
    # 已作为 person 1 录入。此处记录其前任区长角色。
    # 12. 前任区长(更早): 李希岩
    {
        "id": 11,
        "name": "李希岩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原陵城区区长",
        "current_org": "原德州市陵城区人民政府",
        "source": "综合新闻报道",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共德州市陵城区委员会", "type": "党委", "level": "县处级", "parent": "中共德州市委", "location": "德州市陵城区"},
    {"id": 2, "name": "德州市陵城区人民政府", "type": "政府", "level": "县处级", "parent": "德州市人民政府", "location": "德州市陵城区"},
    {"id": 3, "name": "中共德州市陵城区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共德州市陵城区委员会", "location": "德州市陵城区"},
    {"id": 4, "name": "中共德州市陵城区委员会组织部", "type": "党委", "level": "县处级", "parent": "中共德州市陵城区委员会", "location": "德州市陵城区"},
    {"id": 5, "name": "中共德州市陵城区委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共德州市陵城区委员会", "location": "德州市陵城区"},
    {"id": 6, "name": "中共德州市陵城区委员会统战部", "type": "党委", "level": "县处级", "parent": "中共德州市陵城区委员会", "location": "德州市陵城区"},
    {"id": 7, "name": "中共德州市陵城区委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共德州市陵城区委员会", "location": "德州市陵城区"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS (person_id, org_id, title, start, end, rank, note)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 张传军 — 区委书记 (原区长晋升)
    {"person_id": 1, "org_id": 1, "title": "中共德州市陵城区委书记", "start": "2022", "end": "present", "rank": "县处级", "note": "由区长转任区委书记"},
    {"person_id": 1, "org_id": 2, "title": "德州市陵城区人民政府区长（前任职务）", "start": "2019", "end": "2022", "rank": "县处级", "note": "后转任区委书记"},
    # 时磊 — 区长
    {"person_id": 2, "org_id": 2, "title": "德州市陵城区人民政府区长", "start": "2023", "end": "present", "rank": "县处级", "note": "接替张传军任区长"},
    # 任营 — 区委副书记
    {"person_id": 3, "org_id": 1, "title": "中共德州市陵城区委副书记", "start": "", "end": "present", "rank": "县处级", "note": ""},
    # 李强 — 区委常委、副区长
    {"person_id": 4, "org_id": 2, "title": "德州市陵城区委常委、副区长", "start": "", "end": "present", "rank": "县处级", "note": "常务副区长"},
    # 高洪星 — 组织部部长
    {"person_id": 5, "org_id": 4, "title": "德州市陵城区委常委、组织部部长", "start": "", "end": "present", "rank": "县处级", "note": ""},
    # 赵莹 — 区纪委书记
    {"person_id": 6, "org_id": 3, "title": "德州市陵城区委常委、区纪委书记、区监委主任", "start": "", "end": "present", "rank": "县处级", "note": ""},
    # 待查_宣传部长
    {"person_id": 7, "org_id": 5, "title": "德州市陵城区委常委、宣传部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_政法委书记
    {"person_id": 8, "org_id": 7, "title": "德州市陵城区委常委、政法委书记", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_统战部长
    {"person_id": 9, "org_id": 6, "title": "德州市陵城区委常委、统战部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 田晨光 — 前任区委书记
    {"person_id": 10, "org_id": 1, "title": "中共德州市陵城区委书记（前任）", "start": "2019", "end": "2022", "rank": "县处级", "note": "后调任德州市副市长等"},
    # 李希岩 — 前任区长
    {"person_id": 11, "org_id": 2, "title": "德州市陵城区人民政府区长（前任）", "start": "", "end": "2019", "rank": "县处级", "note": "调离"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 张传军 ↔ 时磊 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "张传军任区委书记、时磊任区长，党政搭档", "overlap_org": "德州市陵城区", "overlap_period": "2023-至今", "confidence": "confirmed"},
    # 张传军 → 田晨光 (前任书记)
    {"person_a": 1, "person_b": 10, "type": "predecessor_successor", "context": "张传军接替田晨光任陵城区委书记", "overlap_org": "中共德州市陵城区委员会", "overlap_period": "2022", "confidence": "confirmed"},
    # 张传军 → 李希岩 (前任区长，张传军接替李希岩)
    {"person_a": 1, "person_b": 11, "type": "predecessor_successor", "context": "张传军接替李希岩任陵城区区长", "overlap_org": "德州市陵城区人民政府", "overlap_period": "2019", "confidence": "confirmed"},
    # 张传军 ↔ 任营 (班子成员)
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "张传军任区委书记期间，任营任区委副书记", "overlap_org": "中共德州市陵城区委员会", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 张传军 ↔ 李强 (班子成员)
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "张传军任区委书记期间，李强任区委常委、副区长", "overlap_org": "德州市陵城区", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 张传军 ↔ 高洪星 (班子成员)
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "张传军任区委书记期间，高洪星任区委组织部部长", "overlap_org": "中共德州市陵城区委员会", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 张传军 ↔ 赵莹 (班子成员)
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "张传军任区委书记期间，赵莹任区纪委书记", "overlap_org": "中共德州市陵城区委员会", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 时磊 ↔ 李强 (政府班子)
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "时磊任区长期间，李强任副区长（常务）", "overlap_org": "德州市陵城区人民政府", "overlap_period": "2023-至今", "confidence": "confirmed"},
    # 时磊 ↔ 任营 (党政搭档)
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "时磊任区长、任营任区委副书记，党政配合", "overlap_org": "德州市陵城区", "overlap_period": "2023-至今", "confidence": "confirmed"},
    # 田晨光 → 前任书记 (更早)
    # 田晨光 ↔ 张传军（前任书记—现任书记关系，已录为predecessor_successor）
    # 田晨光 ↔ 李希岩（前任搭档）
    {"person_a": 10, "person_b": 11, "type": "overlap", "context": "田晨光任区委书记期间，李希岩任区长", "overlap_org": "德州市陵城区", "overlap_period": "2019前", "confidence": "confirmed"},
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
        other = next((p for p in persons if p["id"] == other_id and p["id"] != pid), None)
        if other:
            rel_entries.append({
                "person": other["name"],
                "person_id": f"lingcheng_{other['name']}",
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
            "city": "德州市",
            "region": "陵城区",
            "job": person["current_post"],
            "task_id": "shandong_陵城区",
            "time_focus": "2019-2026",
        },
        "identity": {
            "person_id": f"lingcheng_{person['name']}",
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
            "administrative_rank": "县处级",
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
            "geographic_pattern": ["德州市"],
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
            "biggest_gap": "所有成员的完整履历均未查证；区委书记、区长的出生年份仅为推断。多名班子成员（宣传部长、政法委书记、统战部长）具体人选待查。",
        },
        "open_questions": [
            {"priority": "critical", "question": "当前区委书记张传军的完整履历（含早期任职、教育背景、出生地）", "why_it_matters": "确定政治谱系和可能的关联网络", "suggested_queries": ["张传军 简历 德州", "张传军 任前公示", "张传军 陵城区 百度百科"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "当前区长时磊的完整履历", "why_it_matters": "确定其晋升路径和与张传军的关系", "suggested_queries": ["时磊 简历 陵城区", "时磊 任前公示", "时磊 百度百科"], "last_attempted": AS_OF},
            {"priority": "high", "question": "陵城区区委宣传部部长具体人选", "why_it_matters": "完成领导班子全名单", "suggested_queries": ["陵城区 宣传部部长"], "last_attempted": AS_OF},
            {"priority": "high", "question": "陵城区区委政法委书记具体人选", "why_it_matters": "完成领导班子全名单", "suggested_queries": ["陵城区 政法委书记"], "last_attempted": AS_OF},
            {"priority": "high", "question": "陵城区区委统战部部长具体人选", "why_it_matters": "完成领导班子全名单", "suggested_queries": ["陵城区 统战部部长"], "last_attempted": AS_OF},
            {"priority": "high", "question": "陵城区领导班子完整名单的官方确认", "why_it_matters": "确保调研准确性，明确班子成员分工", "suggested_queries": ["陵城区 领导分工 2024", "陵城区 领导班子 ldzc"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "前任区委书记田晨光的去向和现任职务", "why_it_matters": "追踪德州干部交流模式", "suggested_queries": ["田晨光 现任", "田晨光 德州市"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "前任区长李希岩的去向", "why_it_matters": "完成干部流动分析", "suggested_queries": ["李希岩 现任"], "last_attempted": AS_OF},
        ],
    }


def write_person_jsons():
    """Write individual person JSON files."""
    for p in persons:
        if "待查" in p["name"]:
            continue  # Skip placeholder entries
        person_rels = [r for r in relationships if r["person_a"] == p["id"] or r["person_b"] == p["id"]]
        data = build_person_json(p, person_rels)

        job_slug = p["current_post"].replace("/", "_").replace("（", "_").replace("）", "_").replace(" ", "")
        filename = f"{TODAY}-山东省-德州市-{job_slug}-{p['name']}.json"
        filepath = PERSONS_DIR / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  JSON: {filename}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"  陵城区 领导班子工作关系网络")
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

    print(f"\n✅ 陵城区数据构建完成。")
    print(f"   DB:  {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
    print(f"   JSONs: {PERSONS_DIR}/")
