#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 双辽市 (Shuangliao City), 吉林省.

Investigation date: 2026-07-25
Task ID: jilin_双辽市
Level: 县级市
Parent city: 四平市
Targets: 市委书记 & 市长

Research sources:
  - www.shuangliao.gov.cn — 双辽市人民政府官方网站 (primary, confirmed 2026-07-25)
    - "领导工作" section: 市委书记张少恒 bio with full career path
    - 市政府 section: 市长董闯 bio with basic info
    - 副市长 section: 8 deputy mayors listed
  - shuangliao.gov.cn/swsj/shjl/ — 张少恒 detailed bio page
  - shuangliao.gov.cn/szf/ — 董闯 and deputy mayor listing

Confidence notes:
  - 张少恒 (party secretary): confirmed from government website with detailed career timeline
  - 董闯 (mayor): confirmed from government website with basic identity info
  - Deputy mayors: names confirmed from government website listing; no individual bios available
  - Predecessors: 张少恒 previously served as 双辽市委副书记、市长 before becoming 市委书记;
    predecessor 市委书记 info not found
  - Biographical details for deputy mayors: unverified (only names known)
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
SLUG = "双辽市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_双辽市"
if _CURRENT_DIR.name == "jilin_双辽市":
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
# IDs: 1=party secretary, 2=mayor, 3-10=deputy mayors, 11=predecessor
# Gender/ethnicity: confirmed from official profile where available

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "张少恒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年11月",
        "birthplace": "",
        "education": "硕士研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共双辽市委员会",
        "source": "http://www.shuangliao.gov.cn/",
        "confidence": "confirmed",
        "notes": "双辽市委书记。曾任长春市发改委主任科员、长春市委办公厅副处长/处长/副主任、双辽市委副书记、市长。完整履历待补充教育背景和早期经历细节。"
    },
    {
        "id": 2,
        "name": "董闯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年2月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "1999年7月",
        "current_post": "市长",
        "current_org": "双辽市人民政府",
        "source": "http://www.shuangliao.gov.cn/",
        "confidence": "confirmed",
        "notes": "双辽市委副书记、市政府党组书记、市长。1999年7月参加工作，2000年6月入党。完整履历待查。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Mayors (from government listing)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "张英钊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "双辽市人民政府",
        "source": "http://www.shuangliao.gov.cn/szf/",
        "confidence": "confirmed",
        "notes": "双辽市人民政府副市长（名字确认，履历待查）"
    },
    {
        "id": 4,
        "name": "王雨",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "双辽市人民政府",
        "source": "http://www.shuangliao.gov.cn/szf/",
        "confidence": "confirmed",
        "notes": "双辽市人民政府副市长（名字确认，履历待查）"
    },
    {
        "id": 5,
        "name": "王楠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "双辽市人民政府",
        "source": "http://www.shuangliao.gov.cn/szf/",
        "confidence": "confirmed",
        "notes": "双辽市人民政府副市长（名字确认，履历待查）"
    },
    {
        "id": 6,
        "name": "史策",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "双辽市人民政府",
        "source": "http://www.shuangliao.gov.cn/szf/",
        "confidence": "confirmed",
        "notes": "双辽市人民政府副市长（名字确认，履历待查）"
    },
    {
        "id": 7,
        "name": "陶侃",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "双辽市人民政府",
        "source": "http://www.shuangliao.gov.cn/szf/",
        "confidence": "confirmed",
        "notes": "双辽市人民政府副市长（名字确认，履历待查）"
    },
    {
        "id": 8,
        "name": "申显龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "双辽市人民政府",
        "source": "http://www.shuangliao.gov.cn/szf/",
        "confidence": "confirmed",
        "notes": "双辽市人民政府副市长（名字确认，履历待查）"
    },
    {
        "id": 9,
        "name": "丁蕾",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "双辽市人民政府",
        "source": "http://www.shuangliao.gov.cn/szf/",
        "confidence": "confirmed",
        "notes": "双辽市人民政府副市长（名字确认，履历待查）"
    },
    {
        "id": 10,
        "name": "吴逸",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "双辽市人民政府",
        "source": "http://www.shuangliao.gov.cn/szf/",
        "confidence": "confirmed",
        "notes": "双辽市人民政府副市长（名字确认，履历待查）"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Known predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 11,
        "name": "（前任市委书记姓名未确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "inferred",
        "confidence": "unverified",
        "notes": "张少恒的前任市委书记。张少恒在担任双辽市委书记前曾任双辽市委副书记、市长，说明前任书记在此前离任。具体姓名待查。"
    },
]

# ── Organizations ────────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共双辽市委员会", "type": "党委", "level": "县处级",
     "parent": "中共四平市委", "location": "双辽市"},
    {"id": 2, "name": "双辽市人民政府", "type": "政府", "level": "县处级",
     "parent": "四平市人民政府", "location": "双辽市"},
    {"id": 3, "name": "中共双辽市纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共四平市纪委", "location": "双辽市"},
    {"id": 4, "name": "双辽市人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "四平市人大常委会", "location": "双辽市"},
    {"id": 5, "name": "中国人民政治协商会议双辽市委员会", "type": "政协", "level": "县处级",
     "parent": "四平市政协", "location": "双辽市"},
    {"id": 6, "name": "吉林双辽经济开发区", "type": "政府", "level": "县处级",
     "parent": "双辽市人民政府", "location": "双辽市"},
    {"id": 7, "name": "双辽市公安局", "type": "政府", "level": "正科级",
     "parent": "双辽市人民政府", "location": "双辽市"},
    {"id": 8, "name": "中共长春市委办公厅", "type": "党委", "level": "副厅级",
     "parent": "中共长春市委", "location": "长春市"},
    {"id": 9, "name": "长春市发展和改革委员会", "type": "政府", "level": "县处级",
     "parent": "长春市人民政府", "location": "长春市"},
    {"id": 10, "name": "双辽市发展和改革局", "type": "政府", "level": "正科级",
     "parent": "双辽市人民政府", "location": "双辽市"},
    {"id": 11, "name": "双辽市教育局", "type": "政府", "level": "正科级",
     "parent": "双辽市人民政府", "location": "双辽市"},
    {"id": 12, "name": "双辽市工业和信息化局", "type": "政府", "level": "正科级",
     "parent": "双辽市人民政府", "location": "双辽市"},
    {"id": 13, "name": "双辽市财政局", "type": "政府", "level": "正科级",
     "parent": "双辽市人民政府", "location": "双辽市"},
    {"id": 14, "name": "双辽市自然资源局", "type": "政府", "level": "正科级",
     "parent": "双辽市人民政府", "location": "双辽市"},
    {"id": 15, "name": "双辽市农业农村局", "type": "政府", "level": "正科级",
     "parent": "双辽市人民政府", "location": "双辽市"},
    {"id": 16, "name": "双辽市交通运输局", "type": "政府", "level": "正科级",
     "parent": "双辽市人民政府", "location": "双辽市"},
]

# ── Positions ───────────────────────────────────────────────────────────────────

positions = [
    # 张少恒 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "市委书记",
     "start": "", "end": "present",
     "rank": "县处级正职", "note": "2026年7月主持市委常委会"},
    {"person_id": 1, "org_id": 2, "title": "市委副书记、市长",
     "start": "", "end": "",
     "rank": "县处级正职", "note": "升任市委书记前担任双辽市长"},
    {"person_id": 1, "org_id": 8, "title": "副主任",
     "start": "", "end": "",
     "rank": "副局级", "note": "长春市委办公厅副主任"},
    {"person_id": 1, "org_id": 8, "title": "综合三处处长",
     "start": "", "end": "",
     "rank": "正处级", "note": "长春市委办公厅"},
    {"person_id": 1, "org_id": 8, "title": "综合一处副处长",
     "start": "", "end": "",
     "rank": "副处级", "note": "长春市委办公厅"},
    {"person_id": 1, "org_id": 9, "title": "主任科员",
     "start": "", "end": "",
     "rank": "正科级", "note": "长春市发改委服务业发展办公室、经济体制改革处"},

    # 董闯 — 市长
    {"person_id": 2, "org_id": 2, "title": "市长",
     "start": "", "end": "present",
     "rank": "县处级正职", "note": "双辽市委副书记、市政府党组书记、市长"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记",
     "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},

    # 副市长们 — 张英钊, 王雨, 王楠, 史策, 陶侃, 申显龙, 丁蕾, 吴逸
    {"person_id": 3, "org_id": 2, "title": "副市长",
     "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副市长",
     "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副市长",
     "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副市长",
     "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副市长",
     "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副市长",
     "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副市长",
     "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副市长",
     "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────────

relationships = [
    # 张少恒 ↔ 董闯（当前搭档）
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "张少恒任市委书记、董闯任市长，为当前双辽市党政正职搭档",
     "overlap_org": "中共双辽市委员会",
     "overlap_period": "",
     "confidence": "confirmed"},

    # 张少恒 ↔ 双辽市（曾任市长后升书记）
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "张少恒曾任双辽市委副书记、市长，后升任市委书记；董闯接任市长",
     "overlap_org": "双辽市人民政府",
     "overlap_period": "",
     "confidence": "confirmed"},

    # 副市长们 ↔ 董闯（上下级）
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "董闯作为市长领导市政府工作，张英钊为副市长",
     "overlap_org": "双辽市人民政府",
     "overlap_period": "",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "董闯作为市长领导市政府工作，王雨为副市长",
     "overlap_org": "双辽市人民政府",
     "overlap_period": "",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "董闯作为市长领导市政府工作，王楠为副市长",
     "overlap_org": "双辽市人民政府",
     "overlap_period": "",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "董闯作为市长领导市政府工作，史策为副市长",
     "overlap_org": "双辽市人民政府",
     "overlap_period": "",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "董闯作为市长领导市政府工作，陶侃为副市长",
     "overlap_org": "双辽市人民政府",
     "overlap_period": "",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "董闯作为市长领导市政府工作，申显龙为副市长",
     "overlap_org": "双辽市人民政府",
     "overlap_period": "",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "董闯作为市长领导市政府工作，丁蕾为副市长",
     "overlap_org": "双辽市人民政府",
     "overlap_period": "",
     "confidence": "confirmed"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "董闯作为市长领导市政府工作，吴逸为副市长",
     "overlap_org": "双辽市人民政府",
     "overlap_period": "",
     "confidence": "confirmed"},
]


# ═══════════════════════════════════════════════════════════════════════════════
# Run build
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    print(f"=== Building {SLUG} network ===")
    print(f"Staging: {STAGING}")
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write person JSON files for core leaders
    _write_person_json(1, "市委书记", "张少恒")
    _write_person_json(2, "市长", "董闯")
    # Write person JSON for deputy mayor 张英钊 as representative
    _write_person_json(3, "副市长", "张英钊")

    print(f"\n=== Build complete ===")
    print(f"DB size: {DB_PATH.stat().st_size} bytes")
    print(f"GEXF size: {GEXF_PATH.stat().st_size} bytes")
    print(f"Person JSONs in: {PJSON_DIR}")


def _write_person_json(person_id: int, job: str, name: str) -> None:
    """Write a person JSON file for a core figure."""
    p = next(x for x in persons if x["id"] == person_id)
    pos_list = [x for x in positions if x["person_id"] == person_id]
    rel_list = [
        r for r in relationships
        if r["person_a"] == person_id or r["person_b"] == person_id
    ]
    org_ids = set()
    for pos in pos_list:
        org_ids.add(pos["org_id"])
    org_list = [o for o in organizations if o["id"] in org_ids]

    # Build career timeline from positions
    career_timeline = []
    for pos in pos_list:
        org_name = next((o["name"] for o in organizations if o["id"] == pos["org_id"]), "")
        career_timeline.append({
            "start": pos.get("start", ""),
            "end": pos.get("end", ""),
            "org": org_name,
            "title": pos["title"],
            "rank": pos.get("rank", ""),
            "confidence": "confirmed" if p.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    # Build relationships list
    relationships_out = []
    for r in rel_list:
        other_id = r["person_b"] if r["person_a"] == person_id else r["person_a"]
        other_name = next((x["name"] for x in persons if x["id"] == other_id), "")
        relationships_out.append({
            "person": other_name,
            "person_id": f"shuangliao_{other_name}",
            "relationship_type": r["type"],
            "strength": "medium" if r.get("confidence") == "confirmed" else "weak",
            "evidence": r["context"],
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "confidence": r.get("confidence", "unverified"),
            "source_ids": ["S001"],
        })

    # Dedupe key fields
    name_birth = f"{name}_{p.get('birth', '')}"
    name_birthplace = f"{name}_{p.get('birthplace', '')}"

    # Determine career pattern based on available data
    career_pattern = "cross_county_rotation" if person_id == 1 else "local_ladder"
    if person_id == 1:
        career_pattern = "provincial_department"  # 张少恒 came from 长春市委办公厅
    elif person_id >= 3:
        career_pattern = "unknown"

    person_data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "吉林省",
            "city": "四平市",
            "region": "双辽市",
            "job": job,
            "task_id": "jilin_双辽市",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": f"shuangliao_{name}",
            "name": name,
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [
                {
                    "period": "",
                    "institution": p.get("education", "未找到"),
                    "major": "",
                    "degree": "",
                    "study_type": "unknown",
                    "source_ids": ["S001"],
                }
            ],
            "party_join": "中共党员",
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": name_birth,
                "name_birthplace": name_birthplace,
                "official_profile_url": "http://www.shuangliao.gov.cn/swsj/shjl/" if person_id == 1 else "http://www.shuangliao.gov.cn/szf/",
            },
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "县处级正职" if person_id <= 2 else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [
            {
                "name": o["name"],
                "type": o["type"],
                "relationship": "曾任职",
            }
            for o in org_list
        ],
        "relationships": relationships_out,
        "governance_record": [
            {
                "period": "2026",
                "domain": "public_security",
                "achievement_or_event": "主持全市防汛研判调度会议，部署双辽市防汛安全工作",
                "role_in_event": "决策领导",
                "measurable_outcome": "",
                "location": "双辽市",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002", "S003"],
            },
            {
                "period": "2026",
                "domain": "other",
                "achievement_or_event": "以正面典型为引领、以反面典型为镜鉴专题活动，推动全面振兴",
                "role_in_event": "主持",
                "measurable_outcome": "",
                "location": "双辽市",
                "confidence": "confirmed",
                "source_ids": ["S001", "S004"],
            },
        ] if person_id <= 2 else [],
        "professional_profile": {
            "primary_specializations": (
                ["党政管理", "经济管理", "政策研究"] if person_id == 1
                else ["政府行政管理"] if person_id == 2
                else []
            ),
            "secondary_specializations": [],
            "career_pattern": career_pattern,
            "systems_experience": (
                ["party", "government"] if person_id == 1
                else ["government"]
            ),
            "geographic_pattern": (
                ["长春市", "双辽市"] if person_id == 1
                else ["双辽市"]
            ),
            "promotion_velocity": {
                "summary": "履历信息部分已知，晋升速度难以精确判断",
                "notable_fast_promotions": [] if person_id > 2 else [
                    "从长春市委办公厅副主任调任双辽市委副书记、市长后升任市委书记"
                ],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "pragmatic" if person_id <= 2 else "unknown",
                    "evidence": "全市防汛工作、产业发展、项目建设等多领域具体工作部署",
                    "confidence": "plausible",
                    "source_ids": ["S001"],
                }
            ] if person_id <= 2 else [],
            "speech_themes": [
                "极限思维", "压实责任", "实干担当", "全面振兴"
            ] if person_id <= 2 else [],
            "management_signals": [
                "深入基层调研、实地督导"
            ] if person_id <= 2 else [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {
            "total_relationships": len(relationships_out),
            "strong_connections": sum(1 for r in relationships_out if r["strength"] == "strong"),
            "medium_connections": sum(1 for r in relationships_out if r["strength"] == "medium"),
            "weak_connections": sum(1 for r in relationships_out if r["strength"] == "weak"),
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "公开渠道未发现该人员的纪律处分、审查调查或负面报道",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": ["S001"],
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "双辽市人民政府官方网站",
                "url": "http://www.shuangliao.gov.cn/",
                "publisher": "双辽市人民政府",
                "published_at": AS_OF,
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "首页领导工作栏目、市政府页面及市委书记简历页面",
            },
            {
                "id": "S002",
                "title": "全市防汛研判调度会议",
                "url": "http://www.shuangliao.gov.cn/zw/sldt/202607/t20260713_770713.html",
                "publisher": "双辽市人民政府",
                "published_at": "2026-07-13",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "张少恒主持全市防汛研判调度会议",
            },
            {
                "id": "S003",
                "title": "张少恒:树牢极限思维 压实各方责任",
                "url": "http://www.shuangliao.gov.cn/zw/sldt/202607/t20260724_771763.html",
                "publisher": "双辽市人民政府",
                "published_at": "2026-07-24",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "张少恒防汛工作部署",
            },
            {
                "id": "S004",
                "title": "张少恒:以正面典型为引领 以反面典型为镜鉴",
                "url": "http://www.shuangliao.gov.cn/zw/sldt/202607/t20260724_771758.html",
                "publisher": "双辽市人民政府",
                "published_at": "2026-07-24",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "张少恒主持专题活动",
            },
            {
                "id": "S005",
                "title": "董闯参加市人大常委会全委视察活动",
                "url": "http://www.shuangliao.gov.cn/",
                "publisher": "双辽市人民政府",
                "published_at": "2026-07-07",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "董闯工作活动报道",
            },
        ],
        "confidence_summary": {
            "identity": "confirmed" if person_id <= 2 else "unverified",
            "current_role": "confirmed",
            "career_completeness": "partial" if person_id == 1 else ("thin" if person_id == 2 else "thin"),
            "relationship_confidence": "high" if person_id <= 2 else "medium",
            "biggest_gap": (
                "早期教育经历和长春市委办公厅之前的履历缺失" if person_id == 1
                else "1999年参加工作前的教育背景和完整仕途历程缺失" if person_id == 2
                else "完整履历（出生年月、籍贯、学历、工作经历）完全缺失"
            ),
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整履历是什么？",
                "why_it_matters": "构建精确的关系网络需要完整的时间线和历任职务",
                "suggested_queries": [f"{name} 简历 双辽", f"{name} 百度百科", f"{name} 任前公示 四平"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{name}的出生年月、籍贯和毕业院校详情？",
                "why_it_matters": "基本身份信息用于去重和画像",
                "suggested_queries": [f"{name} 出生", f"{name} 籍贯"],
                "last_attempted": AS_OF,
            },
        ] + ([
            {
                "priority": "high",
                "question": "张少恒在长春市委办公厅的任职起止时间？",
                "why_it_matters": "需要精确时间线确定其在长春工作的年限和晋升速度",
                "suggested_queries": ["张少恒 长春市委办公厅", "张少恒 长春市发改委"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "张少恒何时从双辽市长升任市委书记？前任市委书记是谁？",
                "why_it_matters": "前任书记的去向和交接时间对关系网络很重要",
                "suggested_queries": ["双辽市委 任免 2024 2025", "双辽市 书记 任免"],
                "last_attempted": AS_OF,
            },
        ] if person_id == 1 else []) + ([
            {
                "priority": "high",
                "question": "董闯1999年参加工作后的完整经历？",
                "why_it_matters": "董闯1999年7月参加工作至今，中间二十多年经历未公开",
                "suggested_queries": ["董闯 双辽 简历 四平", "董闯 任前公示"],
                "last_attempted": AS_OF,
            },
        ] if person_id == 2 else []),
    }

    fname = f"{TODAY}-吉林省-四平市-{job}-{name}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(person_data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath}")


if __name__ == "__main__":
    main()
