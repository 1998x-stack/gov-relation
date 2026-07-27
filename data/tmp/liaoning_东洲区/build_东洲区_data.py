#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 东洲区, 抚顺市, 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_东洲区
Level: 市辖区
Targets: 区委书记 & 区长

Research status: WEB ACCESS DEGRADED
  - Exa API rate-limited (free tier exhausted)
  - Baidu: 403 captcha block
  - Baidu Baike: 403
  - Jina Reader: timeout
  - Bing/DuckDuckGo/Yahoo: timeout
  - Official 东洲区政府网站 (www.fsdzq.gov.cn): timeout/unreachable
  - 抚顺市人民政府网站 (www.fushun.gov.cn): accessible (front page only)
  - 辽宁省人民政府网站 (www.ln.gov.cn): accessible (front page only)

Current officeholders: UNVERIFIED
  - Web access to 东洲区政府网站 and leadership pages <https://www.fsdzq.gov.cn/>
    was completely blocked. Unable to confirm current 区委书记 and 区长 names.
  - Person names marked as "待查东洲区委书记" and "待查东洲区长" until official
    sources can be accessed.

Confidence notes:
  - The district structure (orgs, level, parent) is confirmed from general knowledge
    of Chinese administrative divisions and the 抚顺市人民政府 website listing 东洲区
    as one of its 4 districts.
  - All person information (names, biographies, career timelines) needs web access to
    official 东洲区 leadership pages.
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
SLUG = "东洲区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "liaoning_东洲区"
if _CURRENT_DIR.name == "liaoning_东洲区":
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
# IDs: 1=区委书记, 2=区长
# Current officeholders UNVERIFIED due to web access degradation.
# Names marked as "待查" until official sources can be consulted.

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership — UNVERIFIED
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "待查东洲区委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "东洲区委书记",
        "current_org": "中共抚顺市东洲区委员会",
        "source": "东洲区人民政府网站暂无法访问: https://www.fsdzq.gov.cn/",
        "confidence": "unverified",
        "notes": "当前东洲区委书记姓名待确认。因 www.fsdzq.gov.cn 无法访问，暂未能获取区委书记姓名。需要从以下渠道补充：(1) 东洲区政府网站领导之窗页；(2) 抚顺市任前公示；(3) 辽宁省组织部干部任免公告。",
    },
    {
        "id": 2,
        "name": "待查东洲区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "东洲区人民政府",
        "source": "东洲区人民政府网站暂无法访问: https://www.fsdzq.gov.cn/",
        "confidence": "unverified",
        "notes": "当前东洲区长姓名待确认。因 www.fsdzq.gov.cn 无法访问，暂未能获取区长姓名。需要从以下渠道补充：(1) 东洲区政府网站领导之窗页；(2) 抚顺市人大任命公告；(3) 抚顺市人民政府网站县区动态。",
    },

    # ══════════════════════════════════════════════════════════════════════
    # Key Standing Committee Members — ALL UNVERIFIED
    # The following are typical 区委常委 positions for a 市辖区.
    # Their names need to be filled when official sources become accessible.
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "待查常务副区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "东洲区委常委、常务副区长",
        "current_org": "东洲区人民政府",
        "source": "",
        "confidence": "unverified",
        "notes": "区委常委、常务副区长姓名待确认。"
    },
    {
        "id": 4,
        "name": "待查组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "东洲区委常委、组织部部长",
        "current_org": "中共抚顺市东洲区委组织部",
        "source": "",
        "confidence": "unverified",
        "notes": "区委常委、组织部部长姓名待确认。"
    },
    {
        "id": 5,
        "name": "待查纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "东洲区委常委、纪委书记、区监委主任",
        "current_org": "中共抚顺市东洲区纪律检查委员会",
        "source": "",
        "confidence": "unverified",
        "notes": "区委常委、纪委书记、监委主任姓名待确认。"
    },
    {
        "id": 6,
        "name": "待查宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "东洲区委常委、宣传部部长",
        "current_org": "中共抚顺市东洲区委宣传部",
        "source": "",
        "confidence": "unverified",
        "notes": "区委常委、宣传部部长姓名待确认。"
    },
    {
        "id": 7,
        "name": "待查政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "东洲区委常委、政法委书记",
        "current_org": "中共抚顺市东洲区委政法委员会",
        "source": "",
        "confidence": "unverified",
        "notes": "区委常委、政法委书记姓名待确认。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
# These are structurally confirmed from the administrative division system.
organizations = [
    {"id": 1, "name": "中共抚顺市东洲区委员会", "type": "党委", "level": "县处级", "parent": "中共抚顺市委", "location": "东洲区"},
    {"id": 2, "name": "东洲区人民政府", "type": "政府", "level": "县处级", "parent": "抚顺市人民政府", "location": "东洲区"},
    {"id": 3, "name": "抚顺市东洲区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "抚顺市人大常委会", "location": "东洲区"},
    {"id": 4, "name": "中国人民政治协商会议抚顺市东洲区委员会", "type": "政协", "level": "县处级", "parent": "政协抚顺市委", "location": "东洲区"},
    {"id": 5, "name": "中共抚顺市东洲区纪律检查委员会（监察委员会）", "type": "纪委", "level": "县处级", "parent": "抚顺市纪委", "location": "东洲区"},
    {"id": 6, "name": "中共抚顺市东洲区委组织部", "type": "党委", "level": "乡科级", "parent": "中共抚顺市东洲区委员会", "location": "东洲区"},
    {"id": 7, "name": "中共抚顺市东洲区委宣传部", "type": "党委", "level": "乡科级", "parent": "中共抚顺市东洲区委员会", "location": "东洲区"},
    {"id": 8, "name": "中共抚顺市东洲区委政法委员会", "type": "党委", "level": "乡科级", "parent": "中共抚顺市东洲区委员会", "location": "东洲区"},
    {"id": 9, "name": "中共抚顺市东洲区委统一战线工作部", "type": "党委", "level": "乡科级", "parent": "中共抚顺市东洲区委员会", "location": "东洲区"},
    {"id": 10, "name": "抚顺市东洲区公安局", "type": "政府", "level": "乡科级", "parent": "东洲区人民政府", "location": "东洲区"},
    {"id": 11, "name": "东洲区发展和改革局", "type": "政府", "level": "乡科级", "parent": "东洲区人民政府", "location": "东洲区"},
    {"id": 12, "name": "东洲区教育局", "type": "政府", "level": "乡科级", "parent": "东洲区人民政府", "location": "东洲区"},
    {"id": 13, "name": "东洲区财政局", "type": "政府", "level": "乡科级", "parent": "东洲区人民政府", "location": "东洲区"},
    {"id": 14, "name": "东洲区住房和城乡建设局", "type": "政府", "level": "乡科级", "parent": "东洲区人民政府", "location": "东洲区"},
    {"id": 15, "name": "东洲区工业和信息化局", "type": "政府", "level": "乡科级", "parent": "东洲区人民政府", "location": "东洲区"},
    {"id": 16, "name": "东洲区民政局", "type": "政府", "level": "乡科级", "parent": "东洲区人民政府", "location": "东洲区"},
    {"id": 17, "name": "东洲区卫生健康局", "type": "政府", "level": "乡科级", "parent": "东洲区人民政府", "location": "东洲区"},
    {"id": 18, "name": "抚顺市东洲区人民法院", "type": "政府", "level": "县处级", "parent": "抚顺市中级人民法院", "location": "东洲区"},
    {"id": 19, "name": "抚顺市东洲区人民检察院", "type": "政府", "level": "县处级", "parent": "抚顺市人民检察院", "location": "东洲区"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 区委书记
    {"person_id": 1, "org_id": 1, "title": "东洲区委书记", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "当前东洲区委书记，姓名待确认"},
    # 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "东洲区人民政府区长，姓名待确认"},
    {"person_id": 2, "org_id": 1, "title": "东洲区委副书记", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "区长兼任区委副书记"},
    # 常务副区长
    {"person_id": 3, "org_id": 1, "title": "东洲区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "区政府党组副书记，分管常务工作"},
    # 组织部长
    {"person_id": 4, "org_id": 1, "title": "东洲区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 6, "title": "组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 纪委书记
    {"person_id": 5, "org_id": 1, "title": "东洲区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 5, "title": "纪委书记、区监委主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 宣传部长
    {"person_id": 6, "org_id": 1, "title": "东洲区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 7, "title": "宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 政法委书记
    {"person_id": 7, "org_id": 1, "title": "东洲区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 8, "title": "政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    # 党政正职搭档 — unverified
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "东洲区委书记与区长为当前党政主要领导搭档关系（姓名待确认）",
        "overlap_org": "中共抚顺市东洲区委员会/东洲区人民政府",
        "overlap_period": "当前",
        "confidence": "unverified",
    },
    # 常务副区长与区长
    {
        "person_a": 2, "person_b": 3,
        "type": "superior_subordinate",
        "context": "区长与常务副区长为政府主要领导与副手关系",
        "overlap_org": "东洲区人民政府",
        "overlap_period": "当前",
        "confidence": "unverified",
    },
    # 组织部长与区委书记
    {
        "person_a": 1, "person_b": 4,
        "type": "superior_subordinate",
        "context": "区委书记与组织部长为党委系统上下级关系",
        "overlap_org": "中共抚顺市东洲区委员会",
        "overlap_period": "当前",
        "confidence": "unverified",
    },
    # 纪委书记与区委书记
    {
        "person_a": 1, "person_b": 5,
        "type": "superior_subordinate",
        "context": "区委书记与纪委书记为党委系统上下级关系",
        "overlap_org": "中共抚顺市东洲区委员会",
        "overlap_period": "当前",
        "confidence": "unverified",
    },
    # 常委班子成员
    {
        "person_a": 3, "person_b": 4,
        "type": "overlap",
        "context": "同为东洲区委常委班子成员",
        "overlap_org": "中共抚顺市东洲区委员会",
        "overlap_period": "当前",
        "confidence": "unverified",
    },
    {
        "person_a": 3, "person_b": 6,
        "type": "overlap",
        "context": "同为东洲区委常委班子成员",
        "overlap_org": "中共抚顺市东洲区委员会",
        "overlap_period": "当前",
        "confidence": "unverified",
    },
    {
        "person_a": 4, "person_b": 7,
        "type": "overlap",
        "context": "同为东洲区委常委班子成员",
        "overlap_org": "中共抚顺市东洲区委员会",
        "overlap_period": "当前",
        "confidence": "unverified",
    },
    {
        "person_a": 5, "person_b": 7,
        "type": "overlap",
        "context": "同为东洲区委常委班子成员",
        "overlap_org": "中共抚顺市东洲区委员会",
        "overlap_period": "当前",
        "confidence": "unverified",
    },
]

# ── Person JSONs ─────────────────────────────────────────────────────────────

PERSON_JSON_TEMPLATE = {
    "schema_version": "1.0",
    "generated_at": TODAY,
    "investigation_scope": {
        "province": "辽宁省",
        "city": "抚顺市",
        "region": "东洲区",
        "task_id": "liaoning_东洲区",
        "time_focus": "2026年7月",
    },
    "identity": {},
    "current_status": {},
    "career_timeline": [],
    "organizations": [],
    "relationships": [],
    "governance_record": [],
    "professional_profile": {},
    "work_style_and_personality": {},
    "network_metrics": {},
    "risk_and_integrity_signals": [],
    "source_register": [],
    "confidence_summary": {},
    "open_questions": [],
}


def build_person_json(person_id: int) -> dict:
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    role_label = p["current_post"]
    now = TODAY

    # Source register
    sources = []
    if p["source"]:
        source_url = p["source"]
        sid = "S001"
        source_type = "official" if "gov.cn" in source_url else "media"
        sources.append({
            "id": sid,
            "title": f"{role_label}确认来源",
            "url": source_url.split(": ")[-1] if ": " in source_url else source_url,
            "publisher": "东洲区人民政府",
            "published_at": AS_OF,
            "accessed_at": AS_OF,
            "source_type": source_type,
            "reliability": "high",
            "notes": "",
        })

    is_core = person_id <= 2
    rank = "县处级正职" if is_core else "县处级副职"
    system = "party" if person_id in [1] else ("discipline" if person_id == 5 else "government")

    person = {
        "identity": {
            "person_id": f"liaoning_fushun_dongzhou_{name}",
            "name": name,
            "aliases": [],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "birthplace": p["birthplace"],
            "native_place": "",
            "education": [],
            "party_join": p["party_join"],
            "work_start": p["work_start"],
            "dedupe_keys": {
                "name_birth": f"{name}_{p['birth']}",
                "name_birthplace": f"{name}_{p['birthplace']}",
                "official_profile_url": p["source"].split(": ")[-1] if ": " in p.get("source", "") else "",
            },
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": rank,
            "as_of": AS_OF,
            "is_current_confirmed": False if "待查" in name else True,
            "source_ids": ["S001"] if sources else [],
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "No risk signals found in publicly available records — web access degraded, limited search capability",
                "date": AS_OF,
                "confidence": "unverified" if "待查" in name else "plausible",
                "source_ids": [],
            }
        ],
        "source_register": sources,
        "confidence_summary": {
            "identity": "unverified" if "待查" in name else "plausible",
            "current_role": "unverified" if "待查" in name else "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low" if "待查" in name else "medium",
            "biggest_gap": "",
        },
        "open_questions": [],
    }

    # Career timeline from positions
    pos_list = [pos for pos in positions if pos["person_id"] == person_id]
    for pos in pos_list:
        org_name = ""
        for o in organizations:
            if o["id"] == pos["org_id"]:
                org_name = o["name"]
                break
        entry = {
            "start": pos["start_date"] if pos["start_date"] else "unknown",
            "end": pos["end_date"] if pos["end_date"] else "present",
            "org": org_name,
            "title": pos["title"],
            "level": "",
            "location": "东洲区",
            "system": system,
            "rank": pos["rank"],
            "is_key_promotion": False,
            "notes": pos["note"],
            "confidence": "unverified" if "待查" in name else "confirmed",
            "source_ids": ["S001"] if sources else [],
        }
        person["career_timeline"].append(entry)

    # Relationships for this person
    person_rels = [r for r in relationships if r["person_a"] == person_id or r["person_b"] == person_id]
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == person_id else r["person_a"]
        other_name = ""
        for op in persons:
            if op["id"] == other_id:
                other_name = op["name"]
                break
        person["relationships"].append({
            "person": other_name,
            "person_id": f"liaoning_fushun_dongzhou_{other_name}",
            "relationship_type": r["type"],
            "strength": "weak",
            "evidence": r["context"],
            "overlap_org": r["overlap_org"],
            "overlap_period": r["overlap_period"],
            "direction": "undirected",
            "confidence": r["confidence"],
        })

    # Big gap
    if "待查" in name:
        person["confidence_summary"]["biggest_gap"] = f"{name}（{role_label}）的姓名尚未确认，全部个人信息缺失"
    elif not p.get("birth"):
        person["confidence_summary"]["biggest_gap"] = f"{name}的出生年月和完整履历未从官方网站获取"

    # Open questions
    if "待查" in name:
        person["open_questions"].append({
            "priority": "critical",
            "question": f"东洲区{role_label}姓名是什么？",
            "why_it_matters": "核心目标人物之一，所有关系网络分析的基础",
            "suggested_queries": [
                f"东洲区 {role_label}",
                "抚顺市东洲区领导之窗",
                "抚顺市委组织部任前公示",
            ],
            "last_attempted": AS_OF,
        })
    if not p.get("birth"):
        person["open_questions"].append({
            "priority": "high",
            "question": f"{name}的出生年月、籍贯、学历？",
            "why_it_matters": "核心身份信息用于去重和综合档案",
            "suggested_queries": [f"东洲区 {name} 简历"],
            "last_attempted": AS_OF,
        })

    return person


def write_person_json(person_id: int):
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    role_label = p["current_post"]
    safe_role = role_label.replace("、", "_")
    filename = f"{TODAY}-辽宁省-抚顺市-{safe_role}-{name}.json"
    path = PJSON_DIR / filename

    person_data = build_person_json(person_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(person_data, f, ensure_ascii=False, indent=2)

    return path


# ── Main ─────────────────────────────────────────────────────────────────────


def main():
    # Build DB and GEXF
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

    # Write person JSONs for all persons
    person_files = []
    for pid in [1, 2, 3, 4, 5, 6, 7]:
        path = write_person_json(pid)
        person_files.append(str(path))

    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Person JSONs:")
    for pf in person_files:
        print(f"  {pf}")
    print(f"Done.")


if __name__ == "__main__":
    main()
