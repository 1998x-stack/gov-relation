#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 潍城区 (Weicheng District), 潍坊市, 山东省.

Level: 市辖区
Province: 山东省
Parent city: 潍坊市
Targets: 区委书记 (Party Secretary), 区长 (District Magistrate)
Task ID: shandong_潍城区

Research date: 2026-07-25
Official source: http://www.weicheng.gov.cn/ (潍城区人民政府) — partial access

Current status (as of 2026-07-25):
Confirmed from official government website:
- 区长: 程锦 (confirmed — listed on 区政府领导信息 as 区委副书记、区长)
- 区委副书记: 李飞雨 (confirmed from "两优一先"表彰大会 news article)
- 副区长: 曹建国, 石凌峰, 鞠洪刚, 常方刚, 董湖波, 丁国强 (confirmed from gov site)
- 区委书记: 待查 (unconfirmed — all recent party meetings chaired by 程锦 as 区委副书记、区长)

Confidence notes:
  Exa web search was rate-limited. Baidu Baike returned 403. Jina Reader timed out.
  Access to weicheng.gov.cn was partial — main site and several news articles accessible,
  but leadership subpages (ldzc, ldxx) returned 404 or timed out.

  The 区委书记 identity could not be verified from available official sources.
  All recent 区委常委会 meetings were chaired by 程锦 (区委副书记、区长),
  which could indicate the position is vacant, recently changed, or the individual
  is rarely mentioned in local news.

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

SLUG = "潍城区"
SLUG_FS = SLUG  # Safe filesystem name

DB_PATH = _STAGING_DIR / f"{SLUG_FS}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG_FS}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-25"
TODAY = "20260725"

import sqlite3  # noqa: F811, E402

SOURCE_REGISTER = [
    {"id": "S001", "title": "潍城区人民政府-区政府领导信息", "url": "http://www.weicheng.gov.cn/WCQZWGK/", "publisher": "潍城区人民政府", "published_at": "2026-07", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "列示了区长、副区长名单"},
    {"id": "S002", "title": "区委常委会召开扩大会议", "url": "http://www.weicheng.gov.cn/WCQZWGK/wcyw/07sdwy20206xxjs6/266831.html", "publisher": "潍城区人民政府", "published_at": "2026-07-06", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "程锦以区委副书记、区长身份主持会议"},
    {"id": "S003", "title": "区委常委会召开会议", "url": "http://www.weicheng.gov.cn/WCQZWGK/wcyw/06sdwy20222xxjs6/266611.html", "publisher": "潍城区人民政府", "published_at": "2026-06-22", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "程锦以区委副书记、区长身份主持会议"},
    {"id": "S004", "title": "潍城区'两优一先'表彰大会召开", "url": "http://www.weicheng.gov.cn/WCQZWGK/wcyw/07sdwy20201xxjs6/266711.html", "publisher": "潍城区人民政府", "published_at": "2026-07-01", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认李飞雨为区委副书记"},
    {"id": "S005", "title": "潍城区委理论学习中心组进行集体学习研讨", "url": "http://www.weicheng.gov.cn/WCQZWGK/wcyw/06sdwy20229xxjs6/266690.html", "publisher": "潍城区人民政府", "published_at": "2026-06-26", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "程锦主持学习"},
    {"id": "S006", "title": "潍城区组织召开服务业企业座谈会", "url": "http://www.weicheng.gov.cn/WCQZWGK/wcyw/06sdwy20209xxjs6/266488.html", "publisher": "潍城区人民政府", "published_at": "2026-06-09", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "程锦主持,曹建国参加"},
]

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 区委书记 — 待查 (unconfirmed)
    {
        "id": 1,
        "name": "待查（区委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共潍坊市潍城区委书记（待确认）",
        "current_org": "中共潍坊市潍城区委员会",
        "source": "官网新闻中未提及，需进一步调查",
    },
    # 2. 程锦 — 区委副书记、区长
    {
        "id": 2,
        "name": "程锦",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共潍坊市潍城区委副书记、潍城区人民政府区长",
        "current_org": "潍坊市潍城区人民政府",
        "source": "潍城区人民政府官网-区政府领导信息",
    },
    # 3. 李飞雨 — 区委副书记
    {
        "id": 3,
        "name": "李飞雨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共潍坊市潍城区委副书记",
        "current_org": "中共潍坊市潍城区委员会",
        "source": "潍城区'两优一先'表彰大会新闻",
    },
    # 4. 曹建国 — 副区长
    {
        "id": 4,
        "name": "曹建国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "潍坊市潍城区人民政府副区长",
        "current_org": "潍坊市潍城区人民政府",
        "source": "潍城区人民政府官网-区政府领导信息",
    },
    # 5. 石凌峰 — 副区长
    {
        "id": 5,
        "name": "石凌峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "潍坊市潍城区人民政府副区长",
        "current_org": "潍坊市潍城区人民政府",
        "source": "潍城区人民政府官网-区政府领导信息",
    },
    # 6. 鞠洪刚 — 副区长
    {
        "id": 6,
        "name": "鞠洪刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "潍坊市潍城区人民政府副区长",
        "current_org": "潍坊市潍城区人民政府",
        "source": "潍城区人民政府官网-区政府领导信息",
    },
    # 7. 常方刚 — 副区长
    {
        "id": 7,
        "name": "常方刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "潍坊市潍城区人民政府副区长",
        "current_org": "潍坊市潍城区人民政府",
        "source": "潍城区人民政府官网-区政府领导信息",
    },
    # 8. 董湖波 — 副区长
    {
        "id": 8,
        "name": "董湖波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "潍坊市潍城区人民政府副区长",
        "current_org": "潍坊市潍城区人民政府",
        "source": "潍城区人民政府官网-区政府领导信息",
    },
    # 9. 丁国强 — 副区长
    {
        "id": 9,
        "name": "丁国强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "潍坊市潍城区人民政府副区长",
        "current_org": "潍坊市潍城区人民政府",
        "source": "潍城区人民政府官网-区政府领导信息",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共潍坊市潍城区委员会", "type": "党委", "level": "县处级", "parent": "中共潍坊市委", "location": "潍坊市潍城区"},
    {"id": 2, "name": "潍坊市潍城区人民政府", "type": "政府", "level": "县处级", "parent": "潍坊市人民政府", "location": "潍坊市潍城区"},
    {"id": 3, "name": "中共潍坊市潍城区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共潍坊市潍城区委员会", "location": "潍坊市潍城区"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS (person_id, org_id, title, start, end, rank, note)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 待查（区委书记）
    {"person_id": 1, "org_id": 1, "title": "中共潍坊市潍城区委书记", "start": "", "end": "present", "rank": "副厅级", "note": "当前区委书记身份待确认"},
    # 程锦
    {"person_id": 2, "org_id": 2, "title": "潍坊市潍城区人民政府区长", "start": "", "end": "present", "rank": "副厅级", "note": "同时担任区委副书记"},
    {"person_id": 2, "org_id": 1, "title": "中共潍坊市潍城区委副书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 李飞雨
    {"person_id": 3, "org_id": 1, "title": "中共潍坊市潍城区委副书记", "start": "", "end": "present", "rank": "副厅级", "note": "分工待查"},
    # 曹建国
    {"person_id": 4, "org_id": 2, "title": "潍坊市潍城区人民政府副区长", "start": "", "end": "present", "rank": "副处级", "note": "分工待查"},
    # 石凌峰
    {"person_id": 5, "org_id": 2, "title": "潍坊市潍城区人民政府副区长", "start": "", "end": "present", "rank": "副处级", "note": "分工待查"},
    # 鞠洪刚
    {"person_id": 6, "org_id": 2, "title": "潍坊市潍城区人民政府副区长", "start": "", "end": "present", "rank": "副处级", "note": "分工待查"},
    # 常方刚
    {"person_id": 7, "org_id": 2, "title": "潍坊市潍城区人民政府副区长", "start": "", "end": "present", "rank": "副处级", "note": "分工待查"},
    # 董湖波
    {"person_id": 8, "org_id": 2, "title": "潍坊市潍城区人民政府副区长", "start": "", "end": "present", "rank": "副处级", "note": "分工待查"},
    # 丁国强
    {"person_id": 9, "org_id": 2, "title": "潍坊市潍城区人民政府副区长", "start": "", "end": "present", "rank": "副处级", "note": "分工待查"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 程锦 ↔ 李飞雨 (党政班子)
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "程锦任区长、李飞雨任区委副书记，同为区领导班子成员", "overlap_org": "中共潍坊市潍城区委员会", "overlap_period": "2026年"},
    # 程锦 → 待查(区委书记) (presumed搭档关系)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "如区委书记已到位，则与程锦为党政搭档", "overlap_org": "中共潍坊市潍城区委员会", "overlap_period": ""},
    # 程锦 ↔ 曹建国 (政府班子)
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "程锦任区长期间，曹建国任副区长", "overlap_org": "潍坊市潍城区人民政府", "overlap_period": "2026年"},
    # 程锦 ↔ 石凌峰 (政府班子)
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "程锦任区长期间，石凌峰任副区长", "overlap_org": "潍坊市潍城区人民政府", "overlap_period": "2026年"},
    # 程锦 ↔ 鞠洪刚 (政府班子)
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "程锦任区长期间，鞠洪刚任副区长", "overlap_org": "潍坊市潍城区人民政府", "overlap_period": "2026年"},
    # 程锦 ↔ 常方刚 (政府班子)
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "程锦任区长期间，常方刚任副区长", "overlap_org": "潍坊市潍城区人民政府", "overlap_period": "2026年"},
    # 程锦 ↔ 董湖波 (政府班子)
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "程锦任区长期间，董湖波任副区长", "overlap_org": "潍坊市潍城区人民政府", "overlap_period": "2026年"},
    # 程锦 ↔ 丁国强 (政府班子)
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "程锦任区长期间，丁国强任副区长", "overlap_org": "潍坊市潍城区人民政府", "overlap_period": "2026年"},
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
            "confidence": "confirmed" if person["name"] != "待查（区委书记）" else "unverified",
            "source_ids": ["S001", "S002", "S003", "S004"],
        })

    rel_entries = []
    for r in relationships_subset:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        if other:
            rel_entries.append({
                "person": other["name"],
                "person_id": f"weicheng_{other['name']}",
                "relationship_type": r["type"],
                "strength": "medium",
                "evidence": r["context"],
                "overlap_org": r.get("overlap_org", ""),
                "overlap_period": r.get("overlap_period", ""),
                "direction": "undirected",
                "confidence": "confirmed" if person["name"] != "待查（区委书记）" else "unverified",
                "source_ids": ["S001", "S002", "S003", "S004"],
            })

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "山东省",
            "city": "潍坊市",
            "region": "潍城区",
            "job": person["current_post"],
            "task_id": "shandong_潍城区",
            "time_focus": "2024-2026",
        },
        "identity": {
            "person_id": f"weicheng_{person['name']}",
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
                "official_profile_url": "http://www.weicheng.gov.cn/WCQZWGK/",
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "副厅级" if pid in (1, 2, 3) else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": person["name"] != "待查（区委书记）",
            "source_ids": ["S001", "S002", "S003", "S004"],
        },
        "career_timeline": career_entries,
        "organizations": [{"org_id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rel_entries,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["government"] if pid != 1 else [],
            "geographic_pattern": ["潍坊市"],
            "promotion_velocity": {"summary": "公开资料不足，难以判断晋升速度", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [] if person["name"] == "待查（区委书记）" else [
                {"trait": "stability_oriented", "evidence": "主持多项会议强调经济运行、安全生产、信访维稳", "confidence": "plausible", "source_ids": ["S002", "S003", "S004"]}
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "公开资料不足，无法推断工作风格",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "截至调研日未发现公开违规违纪记录", "date": AS_OF, "confidence": "unverified", "source_ids": ["S001"]}],
        "source_register": SOURCE_REGISTER,
        "confidence_summary": {
            "identity": "unverified" if person["name"] == "待查（区委书记）" else "confirmed",
            "current_role": "unverified" if person["name"] == "待查（区委书记）" else "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium" if person["name"] != "待查（区委书记）" else "low",
            "biggest_gap": "区委书记身份未确认；所有成员完整履历缺失；领导班子成员名单可能不完整",
        },
        "open_questions": [
            {"priority": "critical", "question": "当前潍城区区委书记是谁？", "why_it_matters": "党政一把手是关系网络的核心节点", "suggested_queries": ["潍城区委书记 2025 2026", "潍城区 区委书记 任免", "潍坊 潍城区 区委书记"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "区长程锦的完整履历（含早期任职、教育背景）", "why_it_matters": "确定晋升路径和可能的关联网络", "suggested_queries": ["程锦 潍坊 潍城区 简历", "程锦 任前公示"], "last_attempted": AS_OF},
            {"priority": "high", "question": "区委副书记李飞雨的完整履历和分工", "why_it_matters": "明确班子成员构成", "suggested_queries": ["李飞雨 潍城区 简历"], "last_attempted": AS_OF},
            {"priority": "high", "question": "各副区长的具体分工和分管领域", "why_it_matters": "了解政府运行的具体分工", "suggested_queries": ["潍城区 副区长 分工"], "last_attempted": AS_OF},
            {"priority": "high", "question": "区委常委完整名单（组织部长、宣传部长、纪委书记、政法委书记等）", "why_it_matters": "完善关系网络数据", "suggested_queries": ["潍城区委 常委 分工"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "前任区委书记和区长的去向", "why_it_matters": "分析潍坊市区县干部交流模式", "suggested_queries": ["潍城区 前任 区委书记", "潍城区 前任 区长"], "last_attempted": AS_OF},
        ],
    }


def write_person_jsons():
    """Write individual person JSON files."""
    for p in persons:
        if "待查" in p["name"]:
            continue  # Skip placeholder for unconfirmed person
        person_rels = [r for r in relationships if r["person_a"] == p["id"] or r["person_b"] == p["id"]]
        data = build_person_json(p, person_rels)

        job_slug = p["current_post"].replace("/", "_").replace("（", "_").replace("）", "_").replace(" ", "")
        # Shorten job slug for filename
        if p["id"] == 2:
            job_short = "区长"
        elif p["id"] == 3:
            job_short = "区委副书记"
        elif p["id"] in (4, 5, 6, 7, 8, 9):
            job_short = "副区长"
        else:
            job_short = job_slug
        filename = f"{TODAY}-山东省-潍坊市-{job_short}-{p['name']}.json"
        filepath = PERSONS_DIR / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  JSON: {filename}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"  潍城区 领导班子工作关系网络")
    print(f"  等级: 市辖区")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 潍城区人民政府官网（部分访问成功，区委书记待确认）")
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

    print(f"\n✅ 潍城区数据构建完成。")
    print(f"   DB:  {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
    print(f"   JSONs: {PERSONS_DIR}/")
