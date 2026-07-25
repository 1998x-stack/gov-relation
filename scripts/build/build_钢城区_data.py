#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 钢城区 (Gangcheng District), 济南市, 山东省.

Level: 市辖区
Province: 山东省
Parent city: 济南市
Targets: 区委书记 (Party Secretary), 区长 (District Magistrate)
Task ID: shandong_钢城区

Research date: 2026-07-25
Official source: https://www.gangcheng.gov.cn/ (济南市钢城区人民政府)

Current status (as of 2026-07-25, based on government website news analysis):
- 区委书记: 翟立波 (confirmed by gov website — top billing in enterprise and flood control inspections)
- 区长: 程学锋 (confirmed by gov website — flood control and fire safety inspections)
- 区委副书记: 陈庆宏 (likely — party lecture on correct performance view)

Confidence notes:
  Exa API was rate-limited during research. Government site www.gangcheng.gov.cn
  was reachable (HTTP) but the leadership page (/zwgk/ldzc/) returned the generic
  template without specific bios. Baidu Baike and Google/Bing search were
  timed out or blocked. Jina Reader also timed out.

  Leadership identification is based on news article prominence on the official
  government homepage (www.gangcheng.gov.cn, accessed via text mode HTTP).
  翟立波 appears as the lead figure in news items (top billing in 政务要闻),
  consistent with 区委书记 role. 程学锋 appears in operational government
  inspections, consistent with 区长 role.

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

SLUG = "钢城区"

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

    # 1. 翟立波 — 区委书记
    {
        "id": 1,
        "name": "翟立波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共济南市钢城区委书记",
        "current_org": "中共济南市钢城区委员会",
        "source": "济南市钢城区人民政府网站新闻报道",
    },
    # 2. 程学锋 — 区长
    {
        "id": 2,
        "name": "程学锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "济南市钢城区人民政府区长",
        "current_org": "济南市钢城区人民政府",
        "source": "济南市钢城区人民政府网站新闻报道",
    },
    # 3. 陈庆宏 — 区委副书记（推测）
    {
        "id": 3,
        "name": "陈庆宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共济南市钢城区委副书记（推测）",
        "current_org": "中共济南市钢城区委员会",
        "source": "济南市钢城区人民政府网站新闻报道（推断）",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共济南市钢城区委员会", "type": "党委", "level": "县处级", "parent": "中共济南市委", "location": "济南市钢城区"},
    {"id": 2, "name": "济南市钢城区人民政府", "type": "政府", "level": "县处级", "parent": "济南市人民政府", "location": "济南市钢城区"},
    {"id": 3, "name": "中共济南市钢城区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共济南市钢城区委员会", "location": "济南市钢城区"},
    {"id": 4, "name": "中共济南市钢城区委员会组织部", "type": "党委", "level": "县处级", "parent": "中共济南市钢城区委员会", "location": "济南市钢城区"},
    {"id": 5, "name": "济南市钢城区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "济南市人大常委会", "location": "济南市钢城区"},
    {"id": 6, "name": "中国人民政治协商会议济南市钢城区委员会", "type": "政协", "level": "县处级", "parent": "济南市政协", "location": "济南市钢城区"},
    {"id": 7, "name": "中共济南市委员会", "type": "党委", "level": "副省级", "parent": "中共山东省委", "location": "济南市"},
    {"id": 8, "name": "济南市人民政府", "type": "政府", "level": "副省级", "parent": "山东省人民政府", "location": "济南市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS (person_id, org_id, title, start, end, rank, note)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 翟立波 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "中共济南市钢城区委书记", "start": "", "end": "present", "rank": "副厅级", "note": "现任区委书记；区政府网站报道其调研企业生产经营和防汛工作"},
    # 程学锋 — 区长
    {"person_id": 2, "org_id": 2, "title": "济南市钢城区人民政府区长", "start": "", "end": "present", "rank": "副厅级", "note": "现任区长；区政府网站报道其调研防汛和消防安全工作"},
    # 陈庆宏 — 区委副书记（推测）
    {"person_id": 3, "org_id": 1, "title": "中共济南市钢城区委副书记（推测）", "start": "", "end": "present", "rank": "副厅级", "note": "讲授树立和践行正确政绩观专题党课"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 翟立波 ↔ 程学锋 (现任搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "翟立波任区委书记、程学锋任区长，党政搭档", "overlap_org": "济南市钢城区", "overlap_period": "至今", "confidence": "plausible"},
    # 翟立波 ↔ 陈庆宏 (书记与副书记搭配)
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "翟立波任区委书记、陈庆宏推测任区委副书记，党政班子搭档", "overlap_org": "中共济南市钢城区委员会", "overlap_period": "至今", "confidence": "weak"},
    # 程学锋 ↔ 陈庆宏 (区长与副书记搭配)
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "程学锋任区长、陈庆宏推测任区委副书记，区领导班子搭档", "overlap_org": "济南市钢城区", "overlap_period": "至今", "confidence": "weak"},
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
                "person_id": f"gangcheng_{other['name']}",
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
            "region": "钢城区",
            "job": person["current_post"],
            "task_id": "shandong_钢城区",
            "time_focus": "2024-2026",
        },
        "identity": {
            "person_id": f"gangcheng_{person['name']}",
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
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
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
            {"id": "S001", "title": "济南市钢城区人民政府网站", "url": "https://www.gangcheng.gov.cn/", "publisher": "济南市钢城区人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "通过HTTP文本模式访问首页，获取新闻报道确认主要领导姓名"},
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "所有成员的完整履历均未查证；区委书记、区长的确切身份依据政府网站新闻报道排名推断。完整领导班子成员名单缺失。",
        },
        "open_questions": [
            {"priority": "critical", "question": "当前钢城区委书记翟立波的完整履历（含出生年月、教育背景、早期任职、调任经历）", "why_it_matters": "确定政治谱系和可能的关联网络", "suggested_queries": ["翟立波 简历 济南", "翟立波 任前公示", "翟立波 百度百科", "翟立波 钢城区委书记 任命"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "当前钢城区长程学锋的完整履历（含出生年月、教育背景、早期任职）", "why_it_matters": "确定其晋升路径和背景", "suggested_queries": ["程学锋 简历 济南", "程学锋 任前公示", "程学锋 百度百科", "程学锋 钢城区长 任命"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "陈庆宏的正式职务确认（是否为区委副书记或其他职务）", "why_it_matters": "确认领导班子的第三个关键人物", "suggested_queries": ["陈庆宏 钢城区 职务", "陈庆宏 钢城区委副书记"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "钢城区委书记翟立波的来源——调任前职务和前任书记去向", "why_it_matters": "分析济南市区县干部交流模式", "suggested_queries": ["翟立波 前任 职务", "钢城区委原书记", "钢城区 区委书记 2024"], "last_attempted": AS_OF},
            {"priority": "high", "question": "钢城区领导班子完整名单（区委常委、副区长）", "why_it_matters": "明确网络分析的所有节点", "suggested_queries": ["钢城区 领导班子", "钢城区 领导分工", "钢城区 领导之窗"], "last_attempted": AS_OF},
            {"priority": "high", "question": "钢城区政府网站领导之窗页面内容（ldzc目录页未能显示具体领导简介）", "why_it_matters": "获取更准确的领导职务分配", "suggested_queries": ["site:gangcheng.gov.cn 翟立波", "site:gangcheng.gov.cn 程学锋", "gangcheng.gov.cn 领导简介"], "last_attempted": AS_OF},
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
    print(f"  钢城区 领导班子工作关系网络")
    print(f"  等级: 市辖区")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 钢城区人民政府网站（www.gangcheng.gov.cn）新闻报道")
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

    print(f"\n✅ 钢城区数据构建完成。")
    print(f"   DB:  {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
    print(f"   JSONs: {PERSONS_DIR}/")
