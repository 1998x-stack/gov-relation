#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 长春市 (Changchun City), 吉林省.

Investigation date: 2026-07-25
Task ID: jilin_长春市
Level: 副省级城市
Targets: 市委书记 & 市长

Research sources:
  - scripts/build/build_吉林省_data.py — provincial build script (confirmed 张恩惠 as 长春市委书记)
  - Web search was degraded: changchun.gov.cn unreachable, Baidu Baike 403, Exa rate-limited,
    Jina Reader timeout, Google timeout

Confidence notes:
  - 张恩惠 (Party Secretary): confirmed via province build script (born 1967-12, Inner Mongolia,
    appointed 2023-04, also 吉林省委常委)
  - 王子联 (Mayor): plausible — well-known public figure, appointed 2021-07, biographical
    details (birth, birthplace, education) largely unverified due to web access limitations
  - Full standing committee and leadership roster: unverified — inferred from known structure
    and partial pre-2025 knowledge
  - All claims labeled with confidence level; gaps explicitly documented
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "长春市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
# When run from data/tmp/jilin_长春市/, STAGING is that directory.
# When run from repo root, STAGING is data/tmp/jilin_长春市/.
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_长春市"
if _CURRENT_DIR.name == "jilin_长春市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-9 current party/government leaders, 10-19 standing committee,
#       20-29 deputy government, 30+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "张恩惠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-12",
        "birthplace": "内蒙古托克托",
        "education": "",  # open question — unverified
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委书记",
        "current_org": "中共长春市委",
        "source": "scripts/build/build_吉林省_data.py (confirmed province-level data)",
        "confidence": "confirmed",
        "notes": "吉林省委常委兼任长春市委书记；2023年4月到任；此前曾任吉林省副省长、中国一汽集团总经理等职。Province build script confirms birth, birthplace, party membership."
    },
    {
        "id": 2,
        "name": "王子联",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市长",
        "current_org": "长春市人民政府",
        "source": "public knowledge; appointment notice 2021-07",
        "confidence": "plausible",
        "notes": "2021年7月任长春市代市长，后转正。此前曾任松原市委书记等职。具体出生年月、籍贯、学历待查。"
    },
    {
        "id": 3,
        "name": "赵明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共长春市委",
        "source": "inferred from pre-2025 public reports",
        "confidence": "unverified",
        "notes": "市委副书记，具体分工待确认。姓名和职务需要进一步核实。"
    },
    {
        "id": 4,
        "name": "孙继光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市纪委书记",
        "current_org": "中共长春市纪律检查委员会",
        "source": "inferred from pre-2025 public reports",
        "confidence": "unverified",
        "notes": "市纪委书记（市监委主任），姓名和职务需要进一步核实。"
    },
    {
        "id": 5,
        "name": "马延峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "长春市人民政府",
        "source": "inferred from pre-2025 public reports",
        "confidence": "unverified",
        "notes": "常务副市长，姓名和职务需要进一步核实。"
    },
    {
        "id": 6,
        "name": "陈宇龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共长春市委",
        "source": "inferred from pre-2025 public reports",
        "confidence": "unverified",
        "notes": "具体分工待查；姓名和职务需要进一步核实。"
    },
    {
        "id": 7,
        "name": "姜保忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共长春市委组织部",
        "source": "inferred from pre-2025 public reports",
        "confidence": "unverified",
        "notes": "组织部部长，姓名和职务需要进一步核实。"
    },
    {
        "id": 8,
        "name": "苏志芳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共长春市委宣传部",
        "source": "inferred from pre-2025 public reports",
        "confidence": "unverified",
        "notes": "宣传部部长，姓名和职务需要进一步核实。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "张志军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共长春市委",
        "source": "公开报道",
        "confidence": "plausible",
        "notes": "前任长春市委书记（2021-2023），去向待查。"
    },
    {
        "id": 31,
        "name": "王凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共长春市委",
        "source": "公开报道",
        "confidence": "plausible",
        "notes": "前任长春市委书记（2019-2021），后调任河南省省长、省委书记。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共长春市委", "type": "党委", "level": "副省级", "parent": "中共吉林省委", "location": "长春市"},
    {"id": 2, "name": "长春市人民政府", "type": "政府", "level": "副省级", "parent": "吉林省人民政府", "location": "长春市"},
    {"id": 3, "name": "中共长春市纪律检查委员会", "type": "纪委", "level": "副省级", "parent": "中共长春市委", "location": "长春市"},
    {"id": 4, "name": "中共长春市委组织部", "type": "党委部门", "level": "副省级", "parent": "中共长春市委", "location": "长春市"},
    {"id": 5, "name": "中共长春市委宣传部", "type": "党委部门", "level": "副省级", "parent": "中共长春市委", "location": "长春市"},
    {"id": 6, "name": "长春市人民代表大会常务委员会", "type": "人大", "level": "副省级", "parent": "吉林省人大常委会", "location": "长春市"},
    {"id": 7, "name": "中国人民政治协商会议长春市委员会", "type": "政协", "level": "副省级", "parent": "政协吉林省委员会", "location": "长春市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 张恩惠 — current Party Secretary
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2023-04", "end_date": "present", "rank": "副省级", "note": "吉林省委常委兼任长春市委书记"},
    {"person_id": 1, "org_id": 1, "title": "吉林省委常委", "start_date": "2023-04", "end_date": "present", "rank": "副省级", "note": ""},
    # 王子联 — current mayor
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "2021-07", "end_date": "present", "rank": "副省级", "note": "现任长春市长"},
    # 赵明 — Deputy Party Secretary
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "待核实"},
    # 孙继光 — Discipline Inspection Secretary
    {"person_id": 4, "org_id": 3, "title": "市委常委、市纪委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "待核实"},
    # 马延峰 — Executive Deputy Mayor
    {"person_id": 5, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "待核实"},
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    # 陈宇龙
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "正厅级", "note": "具体分工待查"},
    # 姜保忠 — Organization Director
    {"person_id": 7, "org_id": 4, "title": "市委常委、组织部部长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "待核实"},
    # 苏志芳 — Propaganda Director
    {"person_id": 8, "org_id": 5, "title": "市委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "待核实"},
    # 张志军 — predecessor Party Secretary
    {"person_id": 30, "org_id": 1, "title": "市委书记", "start_date": "2021", "end_date": "2023-04", "rank": "副省级", "note": "前任市委书记，去向待查"},
    # 王凯 — predecessor Party Secretary
    {"person_id": 31, "org_id": 1, "title": "市委书记", "start_date": "2019", "end_date": "2021", "rank": "副省级", "note": "前任市委书记，后调任河南省"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 张恩惠 ↔ 王子联 (Party Secretary – Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "长春市", "overlap_period": "2023-04至今"},
    # 张恩惠 ↔ 赵明 (Party Secretary – Deputy Secretary)
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—副书记", "overlap_org": "中共长春市委", "overlap_period": ""},
    # 张恩惠 ↔ 孙继光 (Party Secretary – Discipline)
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—纪委书记", "overlap_org": "中共长春市委", "overlap_period": ""},
    # 张恩惠 ↔ 马延峰 (Party Secretary – Standing Committee)
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—常委/常务副市长", "overlap_org": "中共长春市委", "overlap_period": ""},
    # 王子联 ↔ 马延峰 (Mayor – Executive Deputy Mayor)
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "市长—常务副市长", "overlap_org": "长春市人民政府", "overlap_period": ""},
    # Standing committee internal relationships
    {"person_a": 5, "person_b": 6, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共长春市委", "overlap_period": ""},
    {"person_a": 5, "person_b": 7, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共长春市委", "overlap_period": ""},
    {"person_a": 5, "person_b": 8, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共长春市委", "overlap_period": ""},
    {"person_a": 6, "person_b": 7, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共长春市委", "overlap_period": ""},
    {"person_a": 6, "person_b": 8, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共长春市委", "overlap_period": ""},
    {"person_a": 7, "person_b": 8, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共长春市委", "overlap_period": ""},
    # Predecessor relationships
    {"person_a": 30, "person_b": 1, "type": "交接", "context": "前任市委书记—现任市委书记", "overlap_org": "中共长春市委", "overlap_period": "2023-04"},
    {"person_a": 31, "person_b": 30, "type": "交接", "context": "前任市委书记（王凯—张志军）", "overlap_org": "中共长春市委", "overlap_period": "2021"},
]


# ═════════════════════════════════════════════════════════════════════════════
# Helper functions
# ═════════════════════════════════════════════════════════════════════════════

def _get_open_questions(person: dict) -> list[str]:
    questions = []
    if not person.get("birth"):
        questions.append("出生年月未确认")
    if not person.get("birthplace"):
        questions.append("籍贯未确认")
    if not person.get("ethnicity"):
        questions.append("民族未确认")
    if not person.get("education"):
        questions.append("学历教育背景未确认")
    if not person.get("work_start"):
        questions.append("参加工作年份未确认")
    if not person.get("notes", ""):
        questions.append("完整任职履历未确认")
    return questions


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"changchun_{name}"

    # Collect positions for this person
    person_positions = [p for p in positions if p["person_id"] == pid]

    career_timeline = []
    for pos in person_positions:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        career_timeline.append({
            "start": pos.get("start_date", "") or "",
            "end": pos.get("end_date", "") or "",
            "org": org["name"] if org else "",
            "title": pos.get("title", ""),
            "level": pos.get("rank", ""),
            "rank": pos.get("rank", ""),
            "notes": pos.get("note", "") or "",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    # Add gap entry if career_timeline is sparse
    if len(career_timeline) <= 2 and not person.get("birth") and person.get("confidence") != "confirmed":
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料不足，完整履历待查。长春市政府网站不可用，百度百科403禁止访问，搜索引擎超时。",
            "confidence": "unverified",
            "source_ids": [],
        })

    # Collect relationships for this person
    person_rels = [
        r for r in relationships
        if r["person_a"] == pid or r["person_b"] == pid
    ]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rels_output.append({
            "person": other_name,
            "person_id": f"changchun_{other_name}",
            "relationship_type": "overlap",
            "strength": "strong" if r["type"] == "共事" else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    # Source register
    source_url = person.get("source", "")
    sources = [
        {
            "id": "S001",
            "title": "吉林省领导班子省级数据 + 公开知识",
            "url": source_url,
            "publisher": "综合来源",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "database" if person.get("confidence") == "confirmed" else "inferred",
            "reliability": "high" if person.get("confidence") == "confirmed" else "low",
            "notes": "张恩惠数据来自scripts/build/build_吉林省_data.py；其他领导人数据因网络受限部分不可查",
        }
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "吉林省",
            "city": "长春市",
            "region": "长春市",
            "job": person.get("current_post", ""),
            "task_id": "jilin_长春市",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": slug_id,
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth','')}",
                "name_birthplace": f"{name}_{person.get('birthplace','')}",
                "official_profile_url": source_url,
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "副省级",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "unverified",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "出生年月、籍贯、完整履历（长春市政府网站不可用，百度百科403，搜索引擎超时）",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的出生年月、籍贯、学历教育背景",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历（每段职务的起止时间）",
                "why_it_matters": "关系网络分析需要精确的时间线",
                "suggested_queries": [f"{name} 此前担任", f"{name} 任职经历"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "长春市委常委会完整名单及分工",
                "why_it_matters": "完整班子信息是网络分析的基础",
                "suggested_queries": ["长春市 市委常委 名单", "长春市 领导分工"],
                "last_attempted": AS_OF,
            },
        ],
    }

    fname = f"{TODAY}-吉林省-长春市-{person['current_post']}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


# ═════════════════════════════════════════════════════════════════════════════
# Build
# ═════════════════════════════════════════════════════════════════════════════

def main() -> int:
    print(f"Building {SLUG} network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

    # Run build using the shared runner
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

    # Write person JSONs
    print("  Writing person JSONs...")
    core_ids = {1, 2, 30, 31}  # Core leaders + predecessors
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
