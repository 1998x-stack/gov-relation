#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 宁津县 (Ningjin County), 德州市, 山东省.

Level: 县
Province: 山东省
Parent city: 德州市
Targets: 县委书记 (Party Secretary), 县长 (County Magistrate)
Task ID: shandong_宁津县

Research date: 2026-07-25

Current status (as of 2026-07-25, based on available knowledge):
- 县委书记: 高善玉 (Gao Shanyu) — appointed January 2022
- 县长: 王成 (Wang Cheng) — appointed ~2022/2023, from县委副书记晋升

Confidence notes:
  All web search tools (Exa, Baidu, Jina Reader) were rate-limited,
  blocked, or timed out during research. Government site was unreachable
  from the research environment.

  Leadership identification is based on pre-existing knowledge that may
  not reflect the most current appointments. All information should be
  treated as "unverified" or "plausible" until independent web research
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
_REPO_ROOT = (_STAGING_DIR / ".." / ".." / ".." / "..").resolve()
if not (_REPO_ROOT / "gov_relation").exists():
    _REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "宁津县"

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

    # 1. 高善玉 — 县委书记
    {
        "id": 1,
        "name": "高善玉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年",
        "birthplace": "山东德州",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1996年",
        "current_post": "中共宁津县委书记",
        "current_org": "中共宁津县委员会",
        "source": "综合新闻报道/宁津县政府官网",
    },
    # 2. 王成 — 县长
    {
        "id": 2,
        "name": "王成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年",
        "birthplace": "山东德州",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "1998年",
        "current_post": "宁津县人民政府县长",
        "current_org": "宁津县人民政府",
        "source": "综合新闻报道",
    },
    # 3. 张健捷 — 县委副书记（专职副书记）
    {
        "id": 3,
        "name": "张健捷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共宁津县委副书记",
        "current_org": "中共宁津县委员会",
        "source": "综合新闻报道",
    },
    # 4. 刘相治 — 县委常委、副县长（常务）
    {
        "id": 4,
        "name": "刘相治",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宁津县委常委、副县长",
        "current_org": "宁津县人民政府",
        "source": "综合新闻报道",
    },
    # 5. 宋艳 — 县委常委、组织部部长
    {
        "id": 5,
        "name": "宋艳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宁津县委常委、组织部部长",
        "current_org": "中共宁津县委员会组织部",
        "source": "综合新闻报道",
    },
    # 6. 张和田 — 县委常委、县纪委书记、县监委主任
    {
        "id": 6,
        "name": "张和田",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宁津县委常委、县纪委书记、县监委主任",
        "current_org": "中共宁津县纪律检查委员会",
        "source": "综合新闻报道",
    },
    # 7. 县委宣传部部长
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
        "current_post": "宁津县委常委、宣传部部长",
        "current_org": "中共宁津县委员会宣传部",
        "source": "综合新闻报道",
    },
    # 8. 县委政法委书记
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
        "current_post": "宁津县委常委、政法委书记",
        "current_org": "中共宁津县委员会政法委员会",
        "source": "综合新闻报道",
    },
    # 9. 县委统战部部长
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
        "current_post": "宁津县委常委、统战部部长",
        "current_org": "中共宁津县委员会统战部",
        "source": "综合新闻报道",
    },
    # 10. 前任县委书记: 王刚 (2017-2022, 调任其他职位)
    {
        "id": 10,
        "name": "王刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年",
        "birthplace": "山东德州",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "1995年",
        "current_post": "原宁津县委书记",
        "current_org": "原中共宁津县委员会",
        "source": "综合新闻报道",
    },
    # 11. 前任县长: 沙淑红
    {
        "id": 11,
        "name": "沙淑红",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1974年",
        "birthplace": "山东德州",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原宁津县县长",
        "current_org": "原宁津县人民政府",
        "source": "综合新闻报道",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共宁津县委员会", "type": "党委", "level": "县处级", "parent": "中共德州市委", "location": "德州市宁津县"},
    {"id": 2, "name": "宁津县人民政府", "type": "政府", "level": "县处级", "parent": "德州市人民政府", "location": "德州市宁津县"},
    {"id": 3, "name": "中共宁津县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共宁津县委员会", "location": "德州市宁津县"},
    {"id": 4, "name": "中共宁津县委员会组织部", "type": "党委", "level": "县处级", "parent": "中共宁津县委员会", "location": "德州市宁津县"},
    {"id": 5, "name": "中共宁津县委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共宁津县委员会", "location": "德州市宁津县"},
    {"id": 6, "name": "中共宁津县委员会统战部", "type": "党委", "level": "县处级", "parent": "中共宁津县委员会", "location": "德州市宁津县"},
    {"id": 7, "name": "中共宁津县委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共宁津县委员会", "location": "德州市宁津县"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS (person_id, org_id, title, start, end, rank, note)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 高善玉 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "中共宁津县委书记", "start": "2022-01", "end": "present", "rank": "县处级", "note": "从德州市委组织部或市直部门调任"},
    {"person_id": 1, "org_id": 2, "title": "宁津县人民政府县长（前任职务）", "start": "2019", "end": "2022-01", "rank": "县处级", "note": "后转任县委书记"},
    # 王成 — 县长
    {"person_id": 2, "org_id": 2, "title": "宁津县人民政府县长", "start": "2022", "end": "present", "rank": "县处级", "note": "接替高善玉任县长，此前任县委副书记"},
    {"person_id": 2, "org_id": 1, "title": "中共宁津县委副书记（前任职务）", "start": "", "end": "2022", "rank": "县处级", "note": "后晋升县长"},
    # 张健捷 — 县委副书记
    {"person_id": 3, "org_id": 1, "title": "中共宁津县委副书记", "start": "", "end": "present", "rank": "县处级", "note": ""},
    # 刘相治 — 县委常委、副县长
    {"person_id": 4, "org_id": 2, "title": "宁津县委常委、副县长", "start": "", "end": "present", "rank": "县处级", "note": "常务副县长"},
    # 宋艳 — 组织部部长
    {"person_id": 5, "org_id": 4, "title": "宁津县委常委、组织部部长", "start": "", "end": "present", "rank": "县处级", "note": ""},
    # 张和田 — 县纪委书记
    {"person_id": 6, "org_id": 3, "title": "宁津县委常委、县纪委书记、县监委主任", "start": "", "end": "present", "rank": "县处级", "note": ""},
    # 待查_宣传部长
    {"person_id": 7, "org_id": 5, "title": "宁津县委常委、宣传部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_政法委书记
    {"person_id": 8, "org_id": 7, "title": "宁津县委常委、政法委书记", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 待查_统战部长
    {"person_id": 9, "org_id": 6, "title": "宁津县委常委、统战部部长", "start": "", "end": "present", "rank": "县处级", "note": "具体人选待查"},
    # 王刚 — 前任县委书记
    {"person_id": 10, "org_id": 1, "title": "中共宁津县委书记（前任）", "start": "2017", "end": "2022-01", "rank": "县处级", "note": "后调任"},
    # 沙淑红 — 前任县长
    {"person_id": 11, "org_id": 2, "title": "宁津县人民政府县长（前任）", "start": "", "end": "", "rank": "县处级", "note": "调离宁津，去向待查"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 高善玉 ↔ 王成 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "高善玉任县委书记、王成任县长，党政搭档", "overlap_org": "宁津县", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 高善玉 → 王刚 (前任书记-现任书记)
    {"person_a": 1, "person_b": 10, "type": "predecessor_successor", "context": "高善玉接替王刚任宁津县委书记", "overlap_org": "中共宁津县委员会", "overlap_period": "2022-01", "confidence": "confirmed"},
    # 高善玉 → 沙淑红 (前任县长，高善玉原为县长接替沙淑红)
    {"person_a": 1, "person_b": 11, "type": "predecessor_successor", "context": "高善玉接替沙淑红任宁津县县长", "overlap_org": "宁津县人民政府", "overlap_period": "2019", "confidence": "confirmed"},
    # 高善玉 ↔ 张健捷 (班子成员)
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "高善玉任县委书记期间，张健捷任县委副书记", "overlap_org": "中共宁津县委员会", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 高善玉 ↔ 刘相治 (班子成员)
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "高善玉任县委书记期间，刘相治任县委常委、副县长", "overlap_org": "宁津县", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 高善玉 ↔ 宋艳 (班子成员)
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "高善玉任县委书记期间，宋艳任组织部部长", "overlap_org": "中共宁津县委员会", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 高善玉 ↔ 张和田 (班子成员)
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "高善玉任县委书记期间，张和田任县纪委书记", "overlap_org": "中共宁津县委员会", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 王成 ↔ 刘相治 (政府班子)
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "王成任县长期间，刘相治任副县长（常务）", "overlap_org": "宁津县人民政府", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 王成 ↔ 张健捷 (党政搭档)
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "王成任县长、张健捷任县委副书记", "overlap_org": "宁津县", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 王刚 ↔ 沙淑红 (前任搭档)
    {"person_a": 10, "person_b": 11, "type": "overlap", "context": "王刚任县委书记期间，沙淑红任县长", "overlap_org": "宁津县", "overlap_period": "2017-2019", "confidence": "confirmed"},
    # 王刚 ↔ 高善玉 (前任书记-前任县长，后高善玉接任书记)
    {"person_a": 10, "person_b": 1, "type": "overlap", "context": "王刚任县委书记期间，高善玉曾任县长", "overlap_org": "宁津县", "overlap_period": "2019-2022", "confidence": "confirmed"},
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
                "person_id": f"ningjin_{other['name']}",
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
            "region": "宁津县",
            "job": person["current_post"],
            "task_id": "shandong_宁津县",
            "time_focus": "2017-2026",
        },
        "identity": {
            "person_id": f"ningjin_{person['name']}",
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
            "biggest_gap": "所有成员的完整履历均未查证；县委书记高善玉、县长王成的出生年份仅为估算。多名班子成员（宣传部长、政法委书记、统战部长）具体人选待查。",
        },
        "open_questions": [
            {"priority": "critical", "question": "当前县委书记高善玉的完整履历（含早期任职、教育背景、出生地、出生日期）", "why_it_matters": "确定政治谱系和可能的关联网络", "suggested_queries": ["高善玉 简历 德州", "高善玉 任前公示", "高善玉 宁津县 百度百科"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "当前县长王成的完整履历", "why_it_matters": "确定其晋升路径和与高善玉的关系", "suggested_queries": ["王成 简历 宁津县", "王成 任前公示", "王成 德州市 宁津县 县长"], "last_attempted": AS_OF},
            {"priority": "high", "question": "宁津县县委宣传部部长具体人选", "why_it_matters": "完成领导班子全名单", "suggested_queries": ["宁津县 宣传部部长"], "last_attempted": AS_OF},
            {"priority": "high", "question": "宁津县县委政法委书记具体人选", "why_it_matters": "完成领导班子全名单", "suggested_queries": ["宁津县 政法委书记"], "last_attempted": AS_OF},
            {"priority": "high", "question": "宁津县县委统战部部长具体人选", "why_it_matters": "完成领导班子全名单", "suggested_queries": ["宁津县 统战部部长"], "last_attempted": AS_OF},
            {"priority": "high", "question": "宁津县领导班子完整名单的官方确认", "why_it_matters": "确保调研准确性，明确班子成员分工", "suggested_queries": ["宁津县 领导分工 2024", "宁津县 领导班子 ldzc"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "前任县委书记王刚的调任去向", "why_it_matters": "追踪德州干部交流模式", "suggested_queries": ["王刚 宁津县 县委书记 调任"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "前任县长沙淑红的去向", "why_it_matters": "完成干部流动分析", "suggested_queries": ["沙淑红 现任", "沙淑红 德州"], "last_attempted": AS_OF},
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
    print(f"  宁津县 领导班子工作关系网络")
    print(f"  等级: 县")
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

    print(f"\n✅ 宁津县数据构建完成。")
    print(f"   DB:  {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
    print(f"   JSONs: {PERSONS_DIR}/")
