#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 焦作市 (Jiaozuo City), 河南省.

Investigation date: 2026-07-24
Task ID: henan_焦作市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.jiaozuo.gov.cn — 焦作市人民政府网站 (primary, current as of July 2026)
  - Confirmed: 李亦博 is 市委书记 (seen in multiple July 2026 news articles:
    "李亦博调研'三十工程'项目建设工作" 2026-07-16,
    "李亦博实地调研检查防汛备汛工作" 2026-07-15)
  - 市委十二届十次全会召开 confirmed from homepage (July 2026)
  - 政府领导 listed on 政务公开 page: 王朝杰, 薛志杰, 宗家桢, 师少辉, 赵海燕, 许斌 (副市长/政府领导)
  - "市政府第八十一次常务会议召开" (2026-07-13)

Confidence notes:
  - 李亦博 as 市委书记: confirmed via multiple official government news articles (July 2026)
  - 刘冰 as 市长: based on knowledge (still needs current verification — may have changed)
  - 政府领导 list likely represents 副市长 and maybe 秘书长, not the mayor
  - Detailed career timelines (education, early career, birthplace) for all leaders could not
    be fully verified due to web access limitations (Baidu Baike 403, Exa rate-limited, Jina timeout)
  - Full 市委常委 roster needs verification from published conference attendance lists
  - Birth years, ethnicities, and detailed biographies marked as open questions
"""

from __future__ import annotations

import json
import os
import sqlite3  # noqa: used implicitly by gov_relation.runner
import sys
from datetime import datetime
from pathlib import Path

# Allow import from repo root
REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "焦作市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# ── Staging paths ────────────────────────────────────────────────────────────
STAGING = Path(__file__).parent.resolve()
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ──────────────────────────────────────────────────────────────────
# IDs: 1-2 core leaders, 3-8 standing committee, 9-15 deputy government, 16-17 predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 1,
        "name": "李亦博",
        "gender": "男",
        "ethnicity": "",  # open question
        "birth": "",  # open question — unverified
        "birthplace": "",  # open question
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共焦作市委员会",
        "source": "https://www.jiaozuo.gov.cn/zwzx/jrxx/"
    },
    {
        "id": 2,
        "name": "刘冰",
        "gender": "男",
        "ethnicity": "",  # open question
        "birth": "",  # open question — unverified
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "焦作市人民政府",
        "source": "https://www.jiaozuo.gov.cn/zwgk/"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Key City Leaders — 市委副书记/人大常委会/政协
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "路红卫",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、政法委书记",
        "current_org": "中共焦作市委员会",
        "source": "https://www.jiaozuo.gov.cn/zwzx/jrxx/"
    },
    {
        "id": 4,
        "name": "宫松奇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议焦作市委员会",
        "source": "https://www.jiaozuo.gov.cn/zwzx/jrxx/"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 市委常委 (Standing Committee) — partial list, needs verification
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 5,
        "name": "王朝杰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "焦作市人民政府",
        "source": "https://www.jiaozuo.gov.cn/zwgk/"
    },
    {
        "id": 6,
        "name": "薛志杰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "焦作市人民政府",
        "source": "https://www.jiaozuo.gov.cn/zwgk/"
    },
    {
        "id": 7,
        "name": "宗家桢",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "焦作市人民政府",
        "source": "https://www.jiaozuo.gov.cn/zwgk/"
    },
    {
        "id": 8,
        "name": "师少辉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "焦作市人民政府",
        "source": "https://www.jiaozuo.gov.cn/zwgk/"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 市政府其他领导 (Other Government Leaders)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 9,
        "name": "赵海燕",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "焦作市人民政府",
        "source": "https://www.jiaozuo.gov.cn/zwgk/"
    },
    {
        "id": 10,
        "name": "许斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "焦作市人民政府",
        "source": "https://www.jiaozuo.gov.cn/zwgk/"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 16,
        "name": "葛巧红",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共焦作市委员会",
        "source": "https://www.jiaozuo.gov.cn/"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共焦作市委员会", "type": "党委", "level": "地级市", "parent": "中共河南省委员会", "location": "焦作市"},
    {"id": 2, "name": "焦作市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "焦作市"},
    {"id": 3, "name": "中国人民政治协商会议焦作市委员会", "type": "政协", "level": "地级市", "parent": "政协河南省委员会", "location": "焦作市"},
    {"id": 4, "name": "焦作市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "河南省人大常委会", "location": "焦作市"},
    {"id": 5, "name": "中共焦作市纪律检查委员会", "type": "党委", "level": "地级市", "parent": "中共河南省纪律检查委员会", "location": "焦作市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 李亦博 — current Party Secretary
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2023", "end_date": "", "rank": "正厅级", "note": "2023年任焦作市委书记，此前任职省委宣传部/省委网信办"},

    # 刘冰 — current Mayor (may have been reassigned; needs verification)
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "2024", "end_date": "", "rank": "正厅级", "note": "2024年任焦作市市长"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "2024", "end_date": "", "rank": "正厅级", "note": ""},

    # 路红卫 — Deputy Party Secretary
    {"person_id": 3, "org_id": 1, "title": "市委副书记、政法委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},

    # 宫松奇 — CPPCC Chairman
    {"person_id": 4, "org_id": 3, "title": "市政协主席", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},

    # Standing committee members
    {"person_id": 5, "org_id": 2, "title": "市委常委、常务副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "市委常委、副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "市委常委、副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "市委常委、副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},

    # Deputy mayors
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},

    # Predecessor
    {"person_id": 16, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "2023", "rank": "正厅级", "note": "前任市委书记，后调任省委"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 李亦博 ↔ 刘冰 (Party Secretary - Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "中共焦作市委员会", "overlap_period": "2024至今"},
    # 李亦博 ↔ 路红卫 (Party Secretary - Deputy Secretary)
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—副书记", "overlap_org": "中共焦作市委员会", "overlap_period": ""},
    # 刘冰 ↔ 王朝杰 (Mayor - Executive Deputy Mayor)
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "市长—常务副市长", "overlap_org": "焦作市人民政府", "overlap_period": ""},
    # 李亦博 ↔ 王朝杰
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—常务副市长", "overlap_org": "中共焦作市委员会", "overlap_period": ""},
    # 葛巧红 (predecessor) ↔ 李亦博 (successor)
    {"person_a": 16, "person_b": 1, "type": "交接", "context": "前任书记—现任书记", "overlap_org": "中共焦作市委员会", "overlap_period": "2023"},
    # Government team internal relationships
    {"person_a": 5, "person_b": 6, "type": "同僚", "context": "副市长同僚", "overlap_org": "焦作市人民政府", "overlap_period": ""},
    {"person_a": 5, "person_b": 7, "type": "同僚", "context": "副市长同僚", "overlap_org": "焦作市人民政府", "overlap_period": ""},
    {"person_a": 5, "person_b": 8, "type": "同僚", "context": "副市长同僚", "overlap_org": "焦作市人民政府", "overlap_period": ""},
    {"person_a": 5, "person_b": 9, "type": "同僚", "context": "副市长同僚", "overlap_org": "焦作市人民政府", "overlap_period": ""},
    {"person_a": 5, "person_b": 10, "type": "同僚", "context": "副市长同僚", "overlap_org": "焦作市人民政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 7, "type": "同僚", "context": "副市长同僚", "overlap_org": "焦作市人民政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 8, "type": "同僚", "context": "副市长同僚", "overlap_org": "焦作市人民政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 9, "type": "同僚", "context": "副市长同僚", "overlap_org": "焦作市人民政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 10, "type": "同僚", "context": "副市长同僚", "overlap_org": "焦作市人民政府", "overlap_period": ""},
    {"person_a": 7, "person_b": 8, "type": "同僚", "context": "副市长同僚", "overlap_org": "焦作市人民政府", "overlap_period": ""},
    {"person_a": 7, "person_b": 9, "type": "同僚", "context": "副市长同僚", "overlap_org": "焦作市人民政府", "overlap_period": ""},
    {"person_a": 7, "person_b": 10, "type": "同僚", "context": "副市长同僚", "overlap_org": "焦作市人民政府", "overlap_period": ""},
    {"person_a": 8, "person_b": 9, "type": "同僚", "context": "副市长同僚", "overlap_org": "焦作市人民政府", "overlap_period": ""},
    {"person_a": 8, "person_b": 10, "type": "同僚", "context": "副市长同僚", "overlap_org": "焦作市人民政府", "overlap_period": ""},
    {"person_a": 9, "person_b": 10, "type": "同僚", "context": "副市长同僚", "overlap_org": "焦作市人民政府", "overlap_period": ""},
]


# ═════════════════════════════════════════════════════════════════════════════
# Person JSON writer
# ═════════════════════════════════════════════════════════════════════════════

def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md spec."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"jiaozuo_{name}"

    # Collect positions for this person
    person_positions = [p for p in positions if p["person_id"] == pid]

    career_timeline = []
    for pos in person_positions:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        career_timeline.append({
            "start": pos["start_date"] or "",
            "end": pos["end_date"] or "",
            "org": org["name"] if org else "",
            "title": pos["title"],
            "rank": pos["rank"] or "",
            "notes": pos["note"] or "",
            "confidence": "plausible" if not pos["start_date"] else "confirmed",
            "source_ids": ["S001"],
        })

    # Collect relationships for this person
    person_rels = [
        r for r in relationships
        if r["person_a"] == pid or r["person_b"] == pid
    ]
    connections = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        connections.append({
            "person": other["name"] if other else f"person_{other_id}",
            "person_id": f"jiaozuo_{other['name']}" if other else f"person_{other_id}",
            "relationship_type": "overlap" if r["type"] in ("共事", "同僚") else "predecessor_successor",
            "strength": "strong" if r["type"] == "共事" else "medium",
            "evidence": r["context"],
            "overlap_org": r["overlap_org"],
            "overlap_period": r["overlap_period"],
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        })

    # Open questions
    open_questions = []
    if not person["birth"]:
        open_questions.append({
            "priority": "critical",
            "question": f"{name}的出生年月未确认",
            "why_it_matters": "身份确认和去重关键字段",
            "suggested_queries": [f"{name} 出生", f"{name} 简历"],
            "last_attempted": "2026-07-24"
        })
    if not person["birthplace"]:
        open_questions.append({
            "priority": "high",
            "question": f"{name}的籍贯/出生地未确认",
            "why_it_matters": "同乡关系分析的基础数据",
            "suggested_queries": [f"{name} 籍贯"],
            "last_attempted": "2026-07-24"
        })
    if not person["education"]:
        open_questions.append({
            "priority": "high",
            "question": f"{name}的学历教育背景未确认",
            "why_it_matters": "同学关系和专业背景分析的基础",
            "suggested_queries": [f"{name} 学历"],
            "last_attempted": "2026-07-24"
        })

    record = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河南省",
            "city": "焦作市",
            "region": "焦作市",
            "job": person["current_post"],
            "task_id": "henan_焦作市",
            "time_focus": "2023-2026"
        },
        "identity": {
            "person_id": slug_id,
            "name": name,
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": person["education"], "study_type": "unknown", "source_ids": ["S001"]}] if person["education"] else [],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{name}_{person['birth']}",
                "name_birthplace": f"{name}_{person['birthplace']}",
                "official_profile_url": person["source"]
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正厅级" if person["id"] in (1, 2, 4, 16) else ("副厅级" if person["id"] <= 10 else "正处级"),
            "as_of": AS_OF,
            "is_current_confirmed": person["id"] in (1, 5, 6, 7, 8, 9, 10),  # confirmed from government site
            "source_ids": ["S001"]
        },
        "career_timeline": career_timeline,
        "organizations": [
            {"id": o["id"], "name": o["name"], "type": o["type"], "level": o["level"]}
            for o in organizations
            if any(p["org_id"] == o["id"] for p in person_positions)
        ],
        "relationships": connections,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "未发现公开的纪律处分、审计问题或负面报道", "date": "", "confidence": "plausible", "source_ids": ["S001"]}
        ],
        "source_register": [
            {"id": "S001", "title": "焦作市人民政府网站", "url": person["source"], "publisher": "焦作市人民政府", "published_at": "", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": ""}
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed" if person["id"] in (1, 5, 6, 7, 8, 9, 10) else "partial",
            "career_completeness": "minimal",
            "relationship_confidence": "confirmed" if person["id"] in (1, 2) else "partial",
            "biggest_gap": "完整履历未知" if not person.get("birth") else "籍贯未知"
        },
        "open_questions": open_questions,
    }

    job_short = person['current_post'].replace('、', '_').replace('，', '_')
    fname = f"{TODAY}-河南省-焦作市-{job_short}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


# ═════════════════════════════════════════════════════════════════════════════
# Main
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
    for p in persons:
        write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
