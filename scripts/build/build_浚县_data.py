#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 浚县 (Jun County), 鹤壁市, 河南省.

Level: 县
Province: 河南省
Parent city: 鹤壁市
Targets: 县委书记 (Party Secretary), 县长 (County Magistrate)
Task ID: henan_浚县

Research date: 2026-07-24
Official source: https://www.xunxian.gov.cn/ (浚县人民政府) — site timed out during research

Current status (as of 2026-07-24):
- 县委书记: 王远征（已离任，去向：淇县县委书记）→ 继任者待确认
- 县长: 待确认

Confidence notes:
  All web search tools (Exa, Baidu, Bing, Google, Jina Reader) were rate-limited,
  blocked, or timed out during research. Government site https://www.xunxian.gov.cn/
  timed out via webfetch. Baidu Baike returned 403. Baidu search returned captcha.

  淇县 (neighboring county) research confirmed that 王远征 was formerly 淇县县委书记
  after leaving 浚县. His exact departure date from 浚县 and the current 浚县 leadership
  could not be verified from live web sources.

  All information should be treated as "unverified" until independent web research
  can be completed. The artifacts below use confidence="unverified" or "plausible"
  throughout.

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

SLUG = "浚县"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-24"
TODAY = "20260724"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 王远征 — 前任县委书记（2021年前后-2024年/2025年初在任？后调任淇县县委书记）
    {
        "id": 1,
        "name": "王远征",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（曾任浚县县委书记，后调任淇县县委书记）",
        "current_org": "（已离任）",
        "source": "未确认 — 基于淇县调查推知。王远征曾任浚县县委书记后调任淇县。",
    },
    # 2. 浚县县长 — 姓名待确认
    {
        "id": 2,
        "name": "（县长待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浚县人民政府县长",
        "current_org": "浚县人民政府",
        "source": "未确认 — 需通过浚县政府官网或鹤壁市委组织部公示验证",
    },
    # 3. 浚县县委书记（现任）— 姓名待确认
    {
        "id": 3,
        "name": "（县委书记待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共浚县县委书记",
        "current_org": "中共浚县委员会",
        "source": "未确认 — 王远征离任后继任者待确认",
    },
    # ════════════════════════════════════════
    # Leadership Team (Placeholders)
    # ════════════════════════════════════════
    # 4. 县委副书记 (deputy secretary) — name unknown
    {
        "id": 4,
        "name": "（县委副书记待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浚县县委副书记",
        "current_org": "中共浚县委员会",
        "source": "待查 — 需通过浚县政府官网领导之窗页面确认",
    },
    # 5. 常务副县长 (executive deputy county magistrate) — name unknown
    {
        "id": 5,
        "name": "（常务副县长待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浚县县委常委、常务副县长",
        "current_org": "浚县人民政府",
        "source": "待查",
    },
    # 6. 纪委书记 (discipline inspection secretary) — name unknown
    {
        "id": 6,
        "name": "（纪委书记待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浚县县委常委、纪委书记、监委主任",
        "current_org": "中共浚县纪律检查委员会",
        "source": "待查",
    },
    # 7. 组织部长 (organization department head) — name unknown
    {
        "id": 7,
        "name": "（组织部长待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浚县县委常委、组织部长",
        "current_org": "中共浚县县委组织部",
        "source": "待查",
    },
    # 8. 政法委书记 (political-legal committee secretary) — name unknown
    {
        "id": 8,
        "name": "（政法委书记待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浚县县委常委、政法委书记",
        "current_org": "中共浚县县委政法委员会",
        "source": "待查",
    },
    # 9. 宣传部长 (propaganda department head) — name unknown
    {
        "id": 9,
        "name": "（宣传部长待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浚县县委常委、宣传部长",
        "current_org": "中共浚县县委宣传部",
        "source": "待查",
    },
    # 10. 统战部长 (united front department head) — name unknown
    {
        "id": 10,
        "name": "（统战部长待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浚县县委常委、统战部长",
        "current_org": "中共浚县县委统战部",
        "source": "待查",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共浚县委员会", "type": "党委", "level": "县处级", "parent": "中共鹤壁市委", "location": "河南省鹤壁市浚县"},
    {"id": 2, "name": "浚县人民政府", "type": "政府", "level": "县处级", "parent": "鹤壁市人民政府", "location": "河南省鹤壁市浚县"},
    {"id": 3, "name": "中共浚县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共浚县委员会", "location": "河南省鹤壁市浚县"},
    {"id": 4, "name": "浚县监察委员会", "type": "党委", "level": "县处级", "parent": "中共浚县委员会", "location": "河南省鹤壁市浚县"},
    {"id": 5, "name": "中共浚县县委组织部", "type": "党委", "level": "县处级", "parent": "中共浚县委员会", "location": "河南省鹤壁市浚县"},
    {"id": 6, "name": "中共浚县县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共浚县委员会", "location": "河南省鹤壁市浚县"},
    {"id": 7, "name": "中共浚县县委宣传部", "type": "党委", "level": "县处级", "parent": "中共浚县委员会", "location": "河南省鹤壁市浚县"},
    {"id": 8, "name": "中共浚县县委统战部", "type": "党委", "level": "县处级", "parent": "中共浚县委员会", "location": "河南省鹤壁市浚县"},
    {"id": 9, "name": "浚县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "", "location": "河南省鹤壁市浚县"},
    {"id": 10, "name": "中国人民政治协商会议浚县委员会", "type": "政协", "level": "县处级", "parent": "", "location": "河南省鹤壁市浚县"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 王远征 — 前任县委书记
    {"person_id": 1, "org_id": 1, "title": "浚县县委书记（前任）", "start": "", "end": "", "rank": "县处级正职", "note": "后调任淇县县委书记"},
    # 县长（待确认）
    {"person_id": 2, "org_id": 2, "title": "浚县人民政府县长", "start": "", "end": "present", "rank": "县处级正职", "note": "到任时间待确认"},
    {"person_id": 2, "org_id": 1, "title": "浚县县委副书记", "start": "", "end": "present", "rank": "县处级副职", "note": "兼任县委副书记"},
    # 县委书记（现任，待确认）
    {"person_id": 3, "org_id": 1, "title": "浚县县委书记（现任）", "start": "", "end": "present", "rank": "县处级正职", "note": "姓名待确认"},
    # Other leadership positions (placeholders)
    {"person_id": 4, "org_id": 1, "title": "浚县县委副书记", "start": "", "end": "present", "rank": "县处级副职", "note": "待确认"},
    {"person_id": 5, "org_id": 2, "title": "浚县县委常委、常务副县长", "start": "", "end": "present", "rank": "县处级副职", "note": "待确认"},
    {"person_id": 6, "org_id": 3, "title": "浚县县委常委、纪委书记", "start": "", "end": "present", "rank": "县处级副职", "note": "待确认"},
    {"person_id": 6, "org_id": 4, "title": "浚县监委主任", "start": "", "end": "present", "rank": "县处级副职", "note": "待确认"},
    {"person_id": 7, "org_id": 5, "title": "浚县县委常委、组织部长", "start": "", "end": "present", "rank": "县处级副职", "note": "待确认"},
    {"person_id": 8, "org_id": 6, "title": "浚县县委常委、政法委书记", "start": "", "end": "present", "rank": "县处级副职", "note": "待确认"},
    {"person_id": 9, "org_id": 7, "title": "浚县县委常委、宣传部长", "start": "", "end": "present", "rank": "县处级副职", "note": "待确认"},
    {"person_id": 10, "org_id": 8, "title": "浚县县委常委、统战部长", "start": "", "end": "present", "rank": "县处级副职", "note": "待确认"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 前任县委书记 → 现任县委书记（待确认）
    {
        "person_a": 1, "person_b": 3,
        "type": "predecessor_successor",
        "context": "王远征离任浚县县委书记后，由继任者接替",
        "overlap_org": "中共浚县委员会",
        "overlap_period": "",
    },
    # 县委书记（现任）↔ 县长（党政搭档）
    {
        "person_a": 3, "person_b": 2,
        "type": "overlap",
        "context": "县委书记与县长党政主要领导搭档关系",
        "overlap_org": "中共浚县委员会/浚县人民政府",
        "overlap_period": "截至2026年7月",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON BUILDER
# ══════════════════════════════════════════════════════════════════════════════


def build_person_json(person: dict, relationships_subset: list[dict]) -> dict:
    """Build a person graph JSON from the data rows."""
    pid = person["id"]

    career_entries = []
    for pos in positions:
        if pos["person_id"] == pid:
            career_entries.append({
                "start": pos["start"] if pos["start"] else "unknown",
                "end": pos["end"] if pos["end"] else "unknown",
                "org": _org_name(pos["org_id"]),
                "title": pos["title"],
                "level": pos["rank"],
                "location": "河南省鹤壁市浚县",
                "system": "party" if "县委" in pos["title"] or "书记" in pos["title"] else "government",
                "rank": pos["rank"],
                "is_key_promotion": "县委书记" in pos["title"] or "县长" in pos["title"],
                "notes": pos["note"],
                "confidence": "plausible",
                "source_ids": [],
            })

    rels_out = []
    for r in relationships_subset:
        other_pid = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other_name = _person_name(other_pid)
        rels_out.append({
            "person": other_name,
            "person_id": f"xunxian_{_slugify_name(other_name)}",
            "relationship_type": r["type"],
            "strength": "strong",
            "evidence": r["context"],
            "overlap_org": r["overlap_org"],
            "overlap_period": r["overlap_period"],
            "direction": "undirected",
            "confidence": "plausible",
            "source_ids": [],
        })

    orgs_out = []
    seen_orgs = set()
    for pos in positions:
        if pos["person_id"] == pid and pos["org_id"] not in seen_orgs:
            seen_orgs.add(pos["org_id"])
            orgs_out.append({
                "org_id": pos["org_id"],
                "name": _org_name(pos["org_id"]),
                "type": _org_type(pos["org_id"]),
                "level": "县处级",
                "location": "河南省鹤壁市浚县",
            })

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河南省",
            "city": "鹤壁市",
            "region": "浚县",
            "job": person["current_post"],
            "task_id": "henan_浚县",
            "time_focus": "当前",
        },
        "identity": {
            "person_id": f"xunxian_{_slugify_name(person['name'])}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "name_birthplace": f"{person['name']}_{person['birthplace']}",
                "official_profile_url": "https://www.xunxian.gov.cn/",
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "县处级正职",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": [],
        },
        "career_timeline": career_entries if career_entries else [
            {
                "start": "unknown",
                "end": "present",
                "org": person["current_org"],
                "title": person["current_post"],
                "level": "县处级正职",
                "location": "河南省鹤壁市浚县",
                "system": "party" if "书记" in person["current_post"] else "government",
                "rank": "县处级正职",
                "is_key_promotion": True,
                "notes": f"网络搜索工具均受限无法获取完整履历。当前职务信息需通过浚县政府官网 https://www.xunxian.gov.cn/ 或鹤壁市委组织部任前公示验证。",
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "organizations": orgs_out,
        "relationships": rels_out,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "无法评估 — 缺少履历数据",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "unknown",
                    "evidence": "因网络搜索受限，无法分析公开工作风格",
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "工作风格推断需要公开报道、讲话和政府工作报告作为依据。当前阶段无法进行此分析。",
        },
        "network_metrics": {
            "direct_connections": len(rels_out),
            "memberships": len(orgs_out),
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "网络搜索受限，未发现任何廉洁风险信号。此状态不代表无问题，仅表示在有限条件下未发现问题。",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "浚县人民政府官网",
                "url": "https://www.xunxian.gov.cn/",
                "publisher": "浚县人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "网站访问超时。待后续重试。",
            }
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "所有搜索渠道均受限（Exa 限流、百度 403、Bing 超时、Jina Reader 超时、政府网站超时）。姓名、完整履历、出生信息、教育背景、到任时间均需验证。",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "浚县现任县委书记是谁？王远征离任后由谁接替？",
                "why_it_matters": "这是本次调查的核心目标人物。",
                "suggested_queries": [
                    "浚县 县委书记 2025 2026",
                    "浚县 县委书记 任命 鹤壁",
                    "鹤壁市 组织部 浚县 干部任免",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": "浚县现任县长是谁？其履历如何？",
                "why_it_matters": "这是本次调查的第二核心目标人物。",
                "suggested_queries": [
                    "浚县 县长 现任",
                    "浚县 县长 简历",
                    "浚县 人大 任命 县长",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": "王远征在浚县的任职起止时间",
                "why_it_matters": "了解浚县与淇县间的干部交流路径",
                "suggested_queries": [
                    "王远征 浚县 县委书记 任职",
                    "王远征 调任 淇县",
                    "王远征 简历 鹤壁",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "浚县县委领导班子完整名单（包括所有县委常委）",
                "why_it_matters": "构建完整网络图谱的基础",
                "suggested_queries": [
                    "浚县县委 领导班子",
                    "浚县 领导分工",
                    "浚县 领导之窗",
                ],
                "last_attempted": AS_OF,
            },
        ],
    }


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════


def _org_name(org_id: int) -> str:
    for o in organizations:
        if o["id"] == org_id:
            return o["name"]
    return ""


def _org_type(org_id: int) -> str:
    for o in organizations:
        if o["id"] == org_id:
            return o["type"]
    return ""


def _person_name(person_id: int) -> str:
    for p in persons:
        if p["id"] == person_id:
            return p["name"]
    return ""


def _slugify_name(name: str) -> str:
    """Create a simple slug from a Chinese name."""
    return name.replace("（", "_").replace("）", "").replace(" ", "_")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════


def write_person_jsons():
    """Write individual person JSON files."""
    for p in persons:
        skip_placeholders = "待确认" in p["name"]
        person_rels = [r for r in relationships if r["person_a"] == p["id"] or r["person_b"] == p["id"]]
        data = build_person_json(p, person_rels)
        name_part = _slugify_name(p["name"])
        fname = f"{TODAY}-河南省-鹤壁市-{_slugify_job(p['current_post'])}-{name_part}.json"
        fpath = PERSONS_DIR / fname
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Wrote {fpath}")


def _slugify_job(post: str) -> str:
    """Extract a short job title from a Chinese post string."""
    if "前任" in post and "县委书记" in post:
        return "前任县委书记"
    if "县委书记" in post:
        return "县委书记"
    if "县长" in post:
        return "县长"
    if "副书记" in post:
        return "县委副书记"
    if "常务副县长" in post:
        return "常务副县长"
    if "纪委书记" in post:
        return "纪委书记"
    if "组织部长" in post:
        return "组织部长"
    if "政法委书记" in post:
        return "政法委书记"
    if "宣传部长" in post:
        return "宣传部长"
    if "统战部长" in post:
        return "统战部长"
    return post.replace(" ", "_")


def main():
    print(f"=== Building network for {SLUG} ===")
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print()

    # 1. Build the relational database + GEXF graph
    print(">>> Building database and GEXF...")
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
    print()

    # 2. Write per-person JSON files
    print(">>> Writing person JSON files...")
    write_person_jsons()
    print()

    # 3. Print summary
    print("=== Build complete ===")
    print(f"  Database:  {DB_PATH} ({os.path.getsize(DB_PATH)} bytes)")
    print(f"  GEXF:      {GEXF_PATH} ({os.path.getsize(GEXF_PATH)} bytes)")
    print(f"  Persons:   {len(persons)}")
    print(f"  Orgs:      {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relations: {len(relationships)}")
    print()
    print("NOTE: All data is marked as unverified/plausible due to complete")
    print("web search unavailability (Exa rate-limited, Baidu 403, Bing timeout,")
    print("Jina Reader timeout, government site timed out). Verify all facts before use.")


if __name__ == "__main__":
    main()
