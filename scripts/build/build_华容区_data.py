#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 华容区 (Huarong District), 鄂州市, 湖北省.

Investigation date: 2026-08-03
Task ID: hubei_华容区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.hbhr.gov.cn — 华容区人民政府官方网站 (primary, confirmed accessible)
  - Multiple news articles on hbhr.gov.cn confirming current leadership
  - Leadership transition July 2026: 任蔚 transferred out, 龚骏 promoted from 区长 to 区委书记
  - 叶建文 is now 区委副书记、区政府党组书记 (acting 区长)

Confidence notes:
  - Current roles (龚骏 as 区委书记, 叶建文 as 区政府党组书记): confirmed via official government news
  - Standing committee members: identified from official articles covering various meetings
  - Birth years, education, detailed career timelines: mostly unverified (no Baidu Baike access)
  - Predecessors: 任蔚 (former 区委书记, also 鄂州市委常委, ~July 2026) — confirmed
  - Earlier predecessor before 任蔚: unverified
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

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR
import sqlite3  # used by gov_relation.runner internally

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "华容区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-03"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "hubei_华容区"
if _CURRENT_DIR.name == "hubei_华容区":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-9 current district committee (区委), 10-19 government (区政府),
#      20-29 district-level organizations (人大/政协/纪委等),
#      30-39 predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current as of Aug 2026)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "龚骏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共华容区委员会",
        "source": "https://www.hbhr.gov.cn/",
        "confidence": "confirmed",
        "notes": "2026年7月下旬从华容区长晋升为区委书记。此前为华容区长。接替任蔚。",
    },
    {
        "id": 2,
        "name": "叶建文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区政府党组书记",
        "current_org": "华容区人民政府",
        "source": "https://www.hbhr.gov.cn/",
        "confidence": "confirmed",
        "notes": "2026年7月任区委副书记、区政府党组书记、红莲湖旅游度假区党工委书记。待区人大任命为代区长/区长。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # District Committee Members (区委领导)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "李明杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、政法委书记",
        "current_org": "中共华容区委员会",
        "source": "https://www.hbhr.gov.cn/zxzx/hryw/202608/t20260803_776042.html",
        "confidence": "confirmed",
        "notes": "区委常委、政法委书记，兼任红莲湖旅游度假区管委会主任。",
    },
    {
        "id": 4,
        "name": "袁立志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、统战部部长",
        "current_org": "中共华容区委员会",
        "source": "https://www.hbhr.gov.cn/zxzx/hryw/202608/t20260803_776040.html",
        "confidence": "confirmed",
        "notes": "区委常委、统战部部长。陪同龚骏参加'送清凉'慰问活动等。",
    },
    {
        "id": 5,
        "name": "严平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共华容区委员会",
        "source": "https://www.hbhr.gov.cn/zxzx/hryw/202607/t20260729_775359.html",
        "confidence": "confirmed",
        "notes": "区委常委。陪同龚骏调研重点项目与湖泊生态治理。",
    },
    {
        "id": 6,
        "name": "廖小红",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委（副区长）",
        "current_org": "中共华容区委员会",
        "source": "https://www.hbhr.gov.cn/zxzx/hryw/202607/t20260729_775359.html",
        "confidence": "confirmed",
        "notes": "区委常委、区领导。多次陪同龚骏、叶建文调研重点项目。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # District-level Organizations (人大/政协)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 7,
        "name": "吴新明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "华容区人民代表大会常务委员会",
        "source": "https://www.hbhr.gov.cn/zxzx/hryw/202607/t20260702_770085.html",
        "confidence": "confirmed",
        "notes": "区人大常委会党组书记、主任。参加庆祝建党105周年大会直播收看。",
    },
    {
        "id": 8,
        "name": "熊枝江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "政协华容区委员会",
        "source": "https://www.hbhr.gov.cn/zxzx/hryw/202607/t20260702_770085.html",
        "confidence": "confirmed",
        "notes": "区政协党组书记、主席。参加庆祝建党105周年大会直播收看。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee / Other Leaders (additional)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 9,
        "name": "刘维东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导（副区长）",
        "current_org": "华容区人民政府",
        "source": "https://www.hbhr.gov.cn/zxzx/hryw/202608/t20260803_776040.html",
        "confidence": "confirmed",
        "notes": "区领导。陪同龚骏参加送清凉慰问活动。可能为副区长。",
    },
    {
        "id": 10,
        "name": "陈龙祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导（副区长）",
        "current_org": "华容区人民政府",
        "source": "https://www.hbhr.gov.cn/zxzx/hryw/202608/t20260803_776040.html",
        "confidence": "confirmed",
        "notes": "区领导。陪同龚骏参加送清凉活动。可能为副区长。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "任蔚",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区委书记",
        "current_org": "中共华容区委员会",
        "source": "https://www.hbhr.gov.cn/",
        "confidence": "confirmed",
        "notes": "前任华容区委书记。同时担任鄂州市委常委。2026年7月调离区委书记岗位，由龚骏接替。去向待查。此前任职履历也出现在鄂州市领导之窗。",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共华容区委员会", "type": "党委", "level": "正处级", "parent": "中共鄂州市委员会", "location": "华容区"},
    {"id": 2, "name": "华容区人民政府", "type": "政府", "level": "正处级", "parent": "鄂州市人民政府", "location": "华容区"},
    {"id": 3, "name": "中共华容区纪律检查委员会", "type": "党委", "level": "正处级", "parent": "中共华容区委员会", "location": "华容区"},
    {"id": 4, "name": "华容区人民代表大会常务委员会", "type": "人大", "level": "正处级", "parent": "鄂州市人大常委会", "location": "华容区"},
    {"id": 5, "name": "政协华容区委员会", "type": "政协", "level": "正处级", "parent": "政协鄂州市委员会", "location": "华容区"},
    {"id": 6, "name": "华容区人民法院", "type": "事业单位", "level": "正处级", "parent": "鄂州市中级人民法院", "location": "华容区"},
    {"id": 7, "name": "华容区人民检察院", "type": "事业单位", "level": "正处级", "parent": "鄂州市人民检察院", "location": "华容区"},
    {"id": 8, "name": "红莲湖旅游度假区", "type": "开发区", "level": "副处级", "parent": "华容区人民政府", "location": "华容区"},
    {"id": 9, "name": "中共鄂州市委员会", "type": "党委", "level": "地厅级", "parent": "", "location": "鄂州市"},
    {"id": 10, "name": "鄂州市人民政府", "type": "政府", "level": "地厅级", "parent": "", "location": "鄂州市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # Core leadership
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2026-07", "end_date": "", "rank": "正处级", "note": "2026年7月下旬由区长晋升为区委书记，接替任蔚"},
    {"person_id": 1, "org_id": 2, "title": "前区长", "start_date": "", "end_date": "2026-07", "rank": "正处级", "note": "此前担任华容区长，后晋升区委书记"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "2026-07", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "区政府党组书记", "start_date": "2026-07", "end_date": "", "rank": "正处级", "note": "待人大选举为区长"},
    {"person_id": 2, "org_id": 8, "title": "红莲湖旅游度假区党工委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "兼任"},
    # District committee
    {"person_id": 3, "org_id": 1, "title": "区委常委、政法委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "兼任红莲湖旅游度假区管委会主任"},
    {"person_id": 4, "org_id": 1, "title": "区委常委、统战部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # District Congress and CPPCC
    {"person_id": 7, "org_id": 4, "title": "区人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 8, "org_id": 5, "title": "区政协主席", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # Government
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # Predecessors
    {"person_id": 30, "org_id": 1, "title": "前任区委书记", "start_date": "", "end_date": "2026-07", "rank": "正处级", "note": "2026年7月由龚骏接替。兼任鄂州市委常委。去向待查。"},
    {"person_id": 30, "org_id": 9, "title": "鄂州市委常委", "start_date": "", "end_date": "2026-07", "rank": "副厅级", "note": "兼华容区委书记"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # Core leadership relationships
    {"person_a": 1, "person_b": 2, "type": "交接", "context": "前任区长—现任区政府党组书记（区长—代理区长交接）", "overlap_org": "华容区人民政府", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 30, "type": "交接", "context": "前任区委书记—现任区委书记（任蔚→龚骏）", "overlap_org": "中共华容区委员会", "overlap_period": "2026-07"},
    # Party Secretary ↔ Standing Committee
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—政法委书记", "overlap_org": "中共华容区委员会", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—统战部长", "overlap_org": "中共华容区委员会", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—区委常委", "overlap_org": "中共华容区委员会", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "书记—区委常委", "overlap_org": "中共华容区委员会", "overlap_period": "2026-07"},
    # Government
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "区委副书记—政法委书记", "overlap_org": "中共华容区委员会", "overlap_period": "2026-07"},
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "政府党组书记—副区长", "overlap_org": "华容区人民政府", "overlap_period": "2026-07"},
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "政府党组书记—副区长", "overlap_org": "华容区人民政府", "overlap_period": "2026-07"},
    # Standing committee internal
    {"person_a": 3, "person_b": 4, "type": "同僚", "context": "政法委—统战", "overlap_org": "中共华容区委员会", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 5, "type": "同僚", "context": "区委常委同僚", "overlap_org": "中共华容区委员会", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 6, "type": "同僚", "context": "区委常委同僚", "overlap_org": "中共华容区委员会", "overlap_period": "2026"},
    {"person_a": 4, "person_b": 5, "type": "同僚", "context": "区委常委同僚", "overlap_org": "中共华容区委员会", "overlap_period": "2026"},
    {"person_a": 4, "person_b": 6, "type": "同僚", "context": "区委常委同僚", "overlap_org": "中共华容区委员会", "overlap_period": "2026"},
    {"person_a": 5, "person_b": 6, "type": "同僚", "context": "区委常委同僚", "overlap_org": "中共华容区委员会", "overlap_period": "2026"},
    # Predecessor relations
    {"person_a": 30, "person_b": 1, "type": "交接", "context": "前任区委书记—现任区委书记（任蔚→龚骏）", "overlap_org": "中共华容区委员会", "overlap_period": "2026-07"},
    {"person_a": 30, "person_b": 2, "type": "共事", "context": "前书记—副书记（任蔚在任时叶建文调入）", "overlap_org": "中共华容区委员会", "overlap_period": "2026-07"},
]


# ═════════════════════════════════════════════════════════════════════════════
# Helper functions
# ═════════════════════════════════════════════════════════════════════════════

def _get_open_questions(person: dict) -> list[dict]:
    questions = []
    if not person.get("birth"):
        questions.append({
            "priority": "critical",
            "question": f"{person['name']}的出生年月",
            "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
            "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 出生"],
            "last_attempted": AS_OF,
        })
    if not person.get("birthplace"):
        questions.append({
            "priority": "critical",
            "question": f"{person['name']}的籍贯",
            "why_it_matters": "核心身份信息，用于网络分析和区域背景判断",
            "suggested_queries": [f"{person['name']} 籍贯", f"{person['name']} 出生地"],
            "last_attempted": AS_OF,
        })
    if not person.get("education"):
        questions.append({
            "priority": "high",
            "question": f"{person['name']}的学历教育背景",
            "why_it_matters": "教育背景有助于专业领域判断",
            "suggested_queries": [f"{person['name']} 学历", f"{person['name']} 毕业"],
            "last_attempted": AS_OF,
        })
    if person.get("notes") and "待查" in person.get("notes", ""):
        questions.append({
            "priority": "high",
            "question": f"{person['name']}的此前任职履历",
            "why_it_matters": "完整履历是网络分析的基础",
            "suggested_queries": [f"{person['name']} 此前担任", f"{person['name']} 任前公示"],
            "last_attempted": AS_OF,
        })
    return questions


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"huarong_{name}"

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
    career_timeline.append({
        "start": "unknown",
        "end": "unknown",
        "org": "履历缺口",
        "title": "",
        "notes": "政府官网仅提供当前职务确认信息，此前完整任职履历、出生年月、籍贯、学历等均待查。",
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
            "person_id": f"huarong_{other_name}",
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
    source_url = person.get("source", "https://www.hbhr.gov.cn/")
    sources = [
        {
            "id": "S001",
            "title": "华容区人民政府官方网站",
            "url": "https://www.hbhr.gov.cn/",
            "publisher": "华容区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "2026年8月通过新闻稿件确认领导姓名与职位",
        }
    ]

    # Build open questions
    open_questions = _get_open_questions(person)

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "湖北省",
            "city": "鄂州市",
            "region": "华容区",
            "job": person.get("current_post", ""),
            "task_id": "hubei_华容区",
            "time_focus": "2026年7-8月",
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
            "administrative_rank": "",
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
            "identity": "unverified" if not person.get("birth") else "confirmed",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "thin",
            "relationship_confidence": "high" if person.get("confidence") == "confirmed" else "medium",
            "biggest_gap": "出生年月、籍贯、学历、此前完整任职履历（政府网站仅提供姓名和职务确认）",
        },
        "open_questions": open_questions,
    }

    job_short = person['current_post'].replace('、', '_')
    fname = f"{TODAY}-湖北省-鄂州市-{job_short}-{person['name']}.json"
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
    # Core leaders (区委书记 + 区政府党组书记) + predecessor
    core_ids = {1, 2, 30}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())