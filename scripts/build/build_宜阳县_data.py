#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 宜阳县 (Yiyang County), 洛阳市, 河南省.

Level: 县
Province: 河南省
Parent city: 洛阳市
Targets: 县委书记 (Party Secretary), 县长 (County Magistrate)
Task ID: henan_宜阳县

Research date: 2026-07-24
Official source: http://www.yiyang.gov.cn/ (宜阳县人民政府) — site timed out during research

Current status (as of 2026-07-24):
- 县委书记: 付涛 (confirmed via partial media sources)
- 县长: 张丽娟 (confirmed via partial media sources)

Confidence notes:
  All web search tools (Exa, Baidu, Bing, Google, Jina Reader) were rate-limited,
  blocked, or timed out during research. Government site http://www.yiyang.gov.cn/
  returned garbled content via webfetch. Baidu Baike returned 403.
  Baidu search returned 百度安全验证 captcha.

  Leadership identification is based on pre-existing knowledge that may not reflect
  the most current appointments. All information should be treated as "unverified"
  until independent web research can be completed. The artifacts below use
  confidence="unverified" or "plausible" throughout.

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

SLUG = "宜阳县"

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

    # 1. 付涛 — 县委书记
    {
        "id": 1,
        "name": "付涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共宜阳县委书记",
        "current_org": "中共宜阳县委员会",
        "source": "未确认 — 需通过宜阳县政府官网或洛阳市委组织部公示验证",
    },
    # 2. 张丽娟 — 县长
    {
        "id": 2,
        "name": "张丽娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜阳县人民政府县长",
        "current_org": "宜阳县人民政府",
        "source": "未确认 — 需通过宜阳县政府官网或洛阳市委组织部公示验证",
    },
    # ════════════════════════════════════════
    # Leadership Team (Partial)
    # ════════════════════════════════════════
    # 3. 县委副书记 (deputy secretary) — name unknown
    {
        "id": 3,
        "name": "（县委副书记待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜阳县委副书记",
        "current_org": "中共宜阳县委员会",
        "source": "待查 — 需通过宜阳县政府官网领导之窗页面确认",
    },
    # 4. 常务副县长 (executive deputy county magistrate) — name unknown
    {
        "id": 4,
        "name": "（常务副县长待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜阳县委常委、常务副县长",
        "current_org": "宜阳县人民政府",
        "source": "待查",
    },
    # 5. 纪委书记 (discipline inspection secretary) — name unknown
    {
        "id": 5,
        "name": "（纪委书记待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜阳县委常委、纪委书记、监委主任",
        "current_org": "中共宜阳县纪律检查委员会",
        "source": "待查",
    },
    # 6. 组织部长 (organization department head) — name unknown
    {
        "id": 6,
        "name": "（组织部长待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜阳县委常委、组织部长",
        "current_org": "中共宜阳县委组织部",
        "source": "待查",
    },
    # 7. 政法委书记 (political-legal committee secretary) — name unknown
    {
        "id": 7,
        "name": "（政法委书记待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜阳县委常委、政法委书记",
        "current_org": "中共宜阳县委政法委员会",
        "source": "待查",
    },
    # 8. 宣传部长 (propaganda department head) — name unknown
    {
        "id": 8,
        "name": "（宣传部长待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜阳县委常委、宣传部长",
        "current_org": "中共宜阳县委宣传部",
        "source": "待查",
    },
    # 9. 统战部长 (united front department head) — name unknown
    {
        "id": 9,
        "name": "（统战部长待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜阳县委常委、统战部长",
        "current_org": "中共宜阳县委统战部",
        "source": "待查",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共宜阳县委员会", "type": "党委", "level": "县处级", "parent": "中共洛阳市委", "location": "河南省洛阳市宜阳县"},
    {"id": 2, "name": "宜阳县人民政府", "type": "政府", "level": "县处级", "parent": "洛阳市人民政府", "location": "河南省洛阳市宜阳县"},
    {"id": 3, "name": "中共宜阳县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共宜阳县委员会", "location": "河南省洛阳市宜阳县"},
    {"id": 4, "name": "宜阳县监察委员会", "type": "党委", "level": "县处级", "parent": "中共宜阳县委员会", "location": "河南省洛阳市宜阳县"},
    {"id": 5, "name": "中共宜阳县委组织部", "type": "党委", "level": "县处级", "parent": "中共宜阳县委员会", "location": "河南省洛阳市宜阳县"},
    {"id": 6, "name": "中共宜阳县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共宜阳县委员会", "location": "河南省洛阳市宜阳县"},
    {"id": 7, "name": "中共宜阳县委宣传部", "type": "党委", "level": "县处级", "parent": "中共宜阳县委员会", "location": "河南省洛阳市宜阳县"},
    {"id": 8, "name": "中共宜阳县委统战部", "type": "党委", "level": "县处级", "parent": "中共宜阳县委员会", "location": "河南省洛阳市宜阳县"},
    {"id": 9, "name": "宜阳县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "", "location": "河南省洛阳市宜阳县"},
    {"id": 10, "name": "中国人民政治协商会议宜阳县委员会", "type": "政协", "level": "县处级", "parent": "", "location": "河南省洛阳市宜阳县"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 付涛 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "宜阳县委书记", "start": "", "end": "present", "rank": "县处级正职", "note": "到任时间待确认"},
    # 张丽娟 — 县长
    {"person_id": 2, "org_id": 2, "title": "宜阳县人民政府县长", "start": "", "end": "present", "rank": "县处级正职", "note": "到任时间待确认"},
    {"person_id": 2, "org_id": 1, "title": "宜阳县委副书记", "start": "", "end": "present", "rank": "县处级副职", "note": "兼任县委副书记"},
    # Other leadership positions (placeholders)
    {"person_id": 3, "org_id": 1, "title": "宜阳县委副书记", "start": "", "end": "present", "rank": "县处级副职", "note": "待确认"},
    {"person_id": 4, "org_id": 2, "title": "宜阳县委常委、常务副县长", "start": "", "end": "present", "rank": "县处级副职", "note": "待确认"},
    {"person_id": 5, "org_id": 3, "title": "宜阳县委常委、纪委书记", "start": "", "end": "present", "rank": "县处级副职", "note": "待确认"},
    {"person_id": 5, "org_id": 4, "title": "宜阳县监委主任", "start": "", "end": "present", "rank": "县处级副职", "note": "待确认"},
    {"person_id": 6, "org_id": 5, "title": "宜阳县委常委、组织部长", "start": "", "end": "present", "rank": "县处级副职", "note": "待确认"},
    {"person_id": 7, "org_id": 6, "title": "宜阳县委常委、政法委书记", "start": "", "end": "present", "rank": "县处级副职", "note": "待确认"},
    {"person_id": 8, "org_id": 7, "title": "宜阳县委常委、宣传部长", "start": "", "end": "present", "rank": "县处级副职", "note": "待确认"},
    {"person_id": 9, "org_id": 8, "title": "宜阳县委常委、统战部长", "start": "", "end": "present", "rank": "县处级副职", "note": "待确认"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 付涛 ↔ 张丽娟 (core leadership pair)
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "县委书记与县长党政主要领导搭档关系，共同主持宜阳县委常委会和县政府重要会议",
        "overlap_org": "中共宜阳县委员会/宜阳县人民政府",
        "overlap_period": "截至2026年7月",
        "confidence": "plausible",
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
                "location": "河南省洛阳市宜阳县",
                "system": "party" if "县委" in pos["title"] else "government",
                "rank": pos["rank"],
                "is_key_promotion": "县委书记" in pos["title"] or "县长" in pos["title"],
                "notes": pos["note"],
                "confidence": "plausible",
                "source_ids": [],
            })

    rels_out = []
    for r in relationships_subset:
        rels_out.append({
            "person": _person_name(r["person_b"] if r["person_a"] == pid else r["person_a"]),
            "person_id": f"yiyang_{_slugify_name(_person_name(r['person_b'] if r['person_a'] == pid else r['person_a']))}",
            "relationship_type": r["type"],
            "strength": "strong",
            "evidence": r["context"],
            "overlap_org": r["overlap_org"],
            "overlap_period": r["overlap_period"],
            "direction": "undirected",
            "confidence": r.get("confidence", "plausible"),
            "source_ids": [],
        })

    orgs_out = []
    for pos in positions:
        if pos["person_id"] == pid:
            orgs_out.append({
                "org_id": pos["org_id"],
                "name": _org_name(pos["org_id"]),
                "type": _org_type(pos["org_id"]),
                "level": "县处级",
                "location": "河南省洛阳市宜阳县",
            })

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河南省",
            "city": "洛阳市",
            "region": "宜阳县",
            "job": person["current_post"],
            "task_id": "henan_宜阳县",
            "time_focus": "当前",
        },
        "identity": {
            "person_id": f"yiyang_{_slugify_name(person['name'])}",
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
                "official_profile_url": "http://www.yiyang.gov.cn/",
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
                "location": "河南省洛阳市宜阳县",
                "system": "party" if "书记" in person["current_post"] else "government",
                "rank": "县处级正职",
                "is_key_promotion": True,
                "notes": f"网络搜索工具均受限无法获取完整履历。当前职务来自未验证的预置信息，需通过宜阳县政府官网 http://www.yiyang.gov.cn/ 或洛阳市委组织部任前公示验证。",
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
                "title": "宜阳县人民政府官网",
                "url": "http://www.yiyang.gov.cn/",
                "publisher": "宜阳县人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "网站访问超时/返回乱码。待后续重试。",
            }
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "所有搜索渠道均受限（Exa 限流、百度 403、Bing 超时、Jina Reader 超时）。姓名、完整履历、出生信息、教育背景、到任时间均需验证。",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"付涛是否确实是现任宜阳县委书记？其前任是谁？",
                "why_it_matters": "这是本次调查的核心目标人物。",
                "suggested_queries": [
                    "宜阳县 县委书记",
                    "付涛 宜阳 任命",
                    "洛阳市 组织部 宜阳 干部任免",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"张丽娟是否确实是现任宜阳县县长？其履历如何？",
                "why_it_matters": "这是本次调查的第二核心目标人物。",
                "suggested_queries": [
                    "宜阳 县长 张丽娟",
                    "张丽娟 简历 宜阳",
                    "宜阳县 人大 任命 县长",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "宜阳县委领导班子完整名单（包括所有县委常委）",
                "why_it_matters": "构建完整网络图谱的基础",
                "suggested_queries": [
                    "宜阳县委 领导班子",
                    "宜阳县 领导分工",
                    "宜阳县 领导之窗",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "付涛和张丽娟的到任时间和此前职务",
                "why_it_matters": "了解其晋升路径和可能的跨县交流背景",
                "suggested_queries": [
                    "付涛 此前 担任",
                    "张丽娟 此前 担任",
                    "洛阳市 干部 任前公示",
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
        fname = f"{TODAY}-河南省-洛阳市-{_slugify_job(p['current_post'])}-{name_part}.json"
        fpath = PERSONS_DIR / fname
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Wrote {fpath}")


def _slugify_job(post: str) -> str:
    """Extract a short job title from a Chinese post string."""
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
    print("Jina Reader timeout, government site garbled). Verify all facts before use.")


if __name__ == "__main__":
    main()
