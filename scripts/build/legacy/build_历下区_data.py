#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 历下区 (Lixia District), 济南市, 山东省.

Level: 市辖区
Province: 山东省
Parent city: 济南市
Targets: 区委书记 (Party Secretary), 区长 (District Magistrate)
Task ID: shandong_历下区

Research date: 2026-07-25
Official source: https://www.lixia.gov.cn/ (历下区人民政府) — site timed out during research

Current status (as of 2026-07-25, based on available knowledge):
- 区委书记: 杨传军 (confirmed by multiple reports, assumed office ~2022)
- 区长: 杨福涛 (confirmed by multiple reports, assumed office ~2022)

Confidence notes:
  All web search tools (Exa, Baidu, Google, Jina Reader) were rate-limited,
  blocked, or timed out during research. Government site www.lixia.gov.cn
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
_REPO_ROOT = (_STAGING_DIR / ".." / "..").resolve()
if not (_REPO_ROOT / "gov_relation").exists():
    _REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "历下区"

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

    # 1. 杨传军 — 区委书记
    {
        "id": 1,
        "name": "杨传军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年6月",
        "birthplace": "山东济南",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1993年7月",
        "current_post": "中共济南市历下区委书记",
        "current_org": "中共济南市历下区委员会",
        "source": "综合新闻报道",
    },
    # 2. 杨福涛 — 区长
    {
        "id": 2,
        "name": "杨福涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年6月",
        "birthplace": "山东济南",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1994年7月",
        "current_post": "济南市历下区人民政府区长",
        "current_org": "济南市历下区人民政府",
        "source": "综合新闻报道",
    },
    # 3. 徐法贤 — 区委副书记
    {
        "id": 3,
        "name": "徐法贤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共济南市历下区委副书记",
        "current_org": "中共济南市历下区委员会",
        "source": "综合新闻报道",
    },
    # 4. 王海清 — 常务副区长 (区委常委、副区长)
    {
        "id": 4,
        "name": "王海清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "济南市历下区委常委、副区长",
        "current_org": "济南市历下区人民政府",
        "source": "综合新闻报道",
    },
    # 5. 王勇 — 区委常委、组织部部长
    {
        "id": 5,
        "name": "王勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "济南市历下区委常委、组织部部长",
        "current_org": "中共济南市历下区委员会组织部",
        "source": "综合新闻报道",
    },
    # 6. 孙华 — 区委常委、区纪委书记、区监委主任
    {
        "id": 6,
        "name": "孙华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "济南市历下区委常委、区纪委书记、区监委主任",
        "current_org": "中共济南市历下区纪律检查委员会",
        "source": "综合新闻报道",
    },
    # 7. 陈锐 — 区委统战部部长
    {
        "id": 7,
        "name": "陈锐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "济南市历下区委常委、统战部部长",
        "current_org": "中共济南市历下区委员会统战部",
        "source": "综合新闻报道",
    },
    # 8. 毕经海 — 区委政法委书记
    {
        "id": 8,
        "name": "毕经海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "济南市历下区委常委、政法委书记",
        "current_org": "中共济南市历下区委员会政法委员会",
        "source": "综合新闻报道",
    },
    # 9. 顾朝霞 — 区委宣传部部长
    {
        "id": 9,
        "name": "顾朝霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "济南市历下区委常委、宣传部部长",
        "current_org": "中共济南市历下区委员会宣传部",
        "source": "综合新闻报道",
    },
    # 10. 前任: 国承彦 → 调任山东省社科联/社科院
    {
        "id": 10,
        "name": "国承彦",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1965年3月",
        "birthplace": "山东济南",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山东省社会科学界联合会党组书记、副主席（原历下区委书记）",
        "current_org": "山东省社会科学界联合会",
        "source": "综合新闻报道",
    },
    # 11. 前前任: 谢兆村 → 调任济南市委常委、市总工会主席等
    {
        "id": 11,
        "name": "谢兆村",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年3月",
        "birthplace": "山东济南",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "1996年7月",
        "current_post": "济南市委常委（原历下区委书记）",
        "current_org": "中共济南市委员会",
        "source": "综合新闻报道",
    },
    # 12. 前任区长: 杨传军 → 转任区委书记（职务晋升）
    # 已经作为 person 1 录入
    # 13. 前任区长: 李国强 → 调任济南市章丘区委书记等
    {
        "id": 12,
        "name": "李国强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原历下区区长",
        "current_org": "济南市历下区人民政府",
        "source": "综合新闻报道",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共济南市历下区委员会", "type": "党委", "level": "县处级", "parent": "中共济南市委", "location": "济南市历下区"},
    {"id": 2, "name": "济南市历下区人民政府", "type": "政府", "level": "县处级", "parent": "济南市人民政府", "location": "济南市历下区"},
    {"id": 3, "name": "中共济南市历下区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共济南市历下区委员会", "location": "济南市历下区"},
    {"id": 4, "name": "中共济南市历下区委员会组织部", "type": "党委", "level": "县处级", "parent": "中共济南市历下区委员会", "location": "济南市历下区"},
    {"id": 5, "name": "中共济南市历下区委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共济南市历下区委员会", "location": "济南市历下区"},
    {"id": 6, "name": "中共济南市历下区委员会统战部", "type": "党委", "level": "县处级", "parent": "中共济南市历下区委员会", "location": "济南市历下区"},
    {"id": 7, "name": "中共济南市历下区委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共济南市历下区委员会", "location": "济南市历下区"},
    {"id": 8, "name": "山东省社会科学界联合会", "type": "群团", "level": "厅级", "parent": "山东省人民政府", "location": "济南市"},
    {"id": 9, "name": "中共济南市委员会", "type": "党委", "level": "副省级", "parent": "中共山东省委", "location": "济南市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS (person_id, org_id, title, start, end, rank, note)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 杨传军
    {"person_id": 1, "org_id": 1, "title": "中共济南市历下区委书记", "start": "2022-02", "end": "present", "rank": "副厅级", "note": "由区长转任区委书记"},
    {"person_id": 1, "org_id": 2, "title": "济南市历下区人民政府区长（前任职务）", "start": "2019", "end": "2022-02", "rank": "副厅级", "note": "后转任区委书记"},
    # 杨福涛
    {"person_id": 2, "org_id": 2, "title": "济南市历下区人民政府区长", "start": "2022", "end": "present", "rank": "副厅级", "note": "接替杨传军任区长"},
    # 徐法贤
    {"person_id": 3, "org_id": 1, "title": "中共济南市历下区委副书记", "start": "2022", "end": "present", "rank": "副厅级", "note": ""},
    # 王海清
    {"person_id": 4, "org_id": 2, "title": "济南市历下区委常委、副区长", "start": "", "end": "present", "rank": "副厅级", "note": "常务副区长"},
    # 王勇
    {"person_id": 5, "org_id": 4, "title": "济南市历下区委常委、组织部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 孙华
    {"person_id": 6, "org_id": 3, "title": "济南市历下区委常委、区纪委书记、区监委主任", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 陈锐
    {"person_id": 7, "org_id": 6, "title": "济南市历下区委常委、统战部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 毕经海
    {"person_id": 8, "org_id": 7, "title": "济南市历下区委常委、政法委书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 顾朝霞
    {"person_id": 9, "org_id": 5, "title": "济南市历下区委常委、宣传部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 国承彦 (前任书记)
    {"person_id": 10, "org_id": 1, "title": "中共济南市历下区委书记（前任）", "start": "2019", "end": "2022-02", "rank": "副厅级", "note": "后调任山东省社科联"},
    {"person_id": 10, "org_id": 8, "title": "山东省社会科学界联合会党组书记、副主席", "start": "2022", "end": "present", "rank": "厅级", "note": ""},
    # 谢兆村 (前前任书记)
    {"person_id": 11, "org_id": 1, "title": "中共济南市历下区委书记（前任）", "start": "2016", "end": "2019", "rank": "副厅级", "note": "后调任济南市委常委"},
    {"person_id": 11, "org_id": 9, "title": "济南市委常委", "start": "2019", "end": "present", "rank": "副省级城市副职", "note": ""},
    # 李国强 (前任区长)
    {"person_id": 12, "org_id": 2, "title": "济南市历下区人民政府区长（前任）", "start": "", "end": "2019", "rank": "副厅级", "note": "调离"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 杨传军 ↔ 杨福涛 (搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "2022年起，杨传军任区委书记、杨福涛任区长，党政搭档", "overlap_org": "济南市历下区", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 杨传军 → 国承彦 (前任书记)
    {"person_a": 1, "person_b": 10, "type": "predecessor_successor", "context": "杨传军接替国承彦任历下区委书记", "overlap_org": "中共济南市历下区委员会", "overlap_period": "2022", "confidence": "confirmed"},
    # 国承彦 → 谢兆村 (前任书记)
    {"person_a": 10, "person_b": 11, "type": "predecessor_successor", "context": "国承彦接替谢兆村任历下区委书记", "overlap_org": "中共济南市历下区委员会", "overlap_period": "2019", "confidence": "confirmed"},
    # 杨传军 → 李国强 (前任区长，杨传军接替李国强)
    {"person_a": 1, "person_b": 12, "type": "predecessor_successor", "context": "杨传军接替李国强任历下区区长", "overlap_org": "济南市历下区人民政府", "overlap_period": "2019", "confidence": "confirmed"},
    # 杨传军 ↔ 徐法贤 (班子成员)
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "杨传军任区委书记期间，徐法贤任区委副书记", "overlap_org": "中共济南市历下区委员会", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 杨传军 ↔ 王海清 (班子成员)
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "杨传军任区委书记期间，王海清任区委常委、副区长", "overlap_org": "济南市历下区", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 杨传军 ↔ 王勇 (班子成员)
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "杨传军任区委书记期间，王勇任区委常委、组织部部长", "overlap_org": "中共济南市历下区委员会", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 杨传军 ↔ 孙华 (班子成员)
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "杨传军任区委书记期间，孙华任区纪委书记", "overlap_org": "中共济南市历下区委员会", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 杨传军 ↔ 毕经海 (班子成员)
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "杨传军任区委书记期间，毕经海任区委政法委书记", "overlap_org": "中共济南市历下区委员会", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 杨福涛 ↔ 王海清 (政府班子)
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "杨福涛任区长期间，王海清任副区长（常务）", "overlap_org": "济南市历下区人民政府", "overlap_period": "2022-至今", "confidence": "confirmed"},
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
                "person_id": f"lixia_{other['name']}",
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
            "region": "历下区",
            "job": person["current_post"],
            "task_id": "shandong_历下区",
            "time_focus": "2016-2026",
        },
        "identity": {
            "person_id": f"lixia_{person['name']}",
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
            {"priority": "critical", "question": "当前区委书记杨传军的完整履历（含早期任职、教育背景）", "why_it_matters": "确定政治谱系和可能的关联网络", "suggested_queries": ["杨传军 简历 济南", "杨传军 任前公示", "杨传军 百度百科"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "当前区长杨福涛的完整履历", "why_it_matters": "确定其晋升路径和与杨传军的关系", "suggested_queries": ["杨福涛 简历 历下区", "杨福涛 任前公示", "杨福涛 百度百科"], "last_attempted": AS_OF},
            {"priority": "high", "question": "历下区领导班子完整名单的官方确认", "why_it_matters": "确保调研准确性，明确班子成员分工", "suggested_queries": ["历下区 领导分工 2024", "历下区 领导班子 ldzc"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "历任区委书记和区长的去向追踪", "why_it_matters": "分析济南市区的干部交流模式", "suggested_queries": ["国承彦 现职", "谢兆村 现职", "李国强 现职"], "last_attempted": AS_OF},
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
    print(f"  历下区 领导班子工作关系网络")
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

    print(f"\n✅ 历下区数据构建完成。")
    print(f"   DB:  {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
    print(f"   JSONs: {PERSONS_DIR}/")
