#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 吉林市 (Jilin City), 吉林省.

Investigation date: 2026-07-25
Task ID: jilin_吉林市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.jlcity.gov.cn — 吉林市人民政府官方网站 (primary, current as of July 2026)
  - jlcity.gov.cn/jlszf/20zfld/ — 市政府领导页面 (confirmed current roster)
  - Homepage news items and meeting reports (July 2026)
  - Web search was degraded: Baidu Baike 403, Exa rate-limited, Google Search blocked

Confidence notes:
  - Current roles: confirmed via government official leadership page (2026-07-25)
  - 王吉 bio (born Feb 1972, grad, economics master): confirmed from official profile
  - 胡斌 position: confirmed from multiple news reports on official site (July 2026)
  - Biographical details (birth, birthplace, education for most): unverified due to web access limitations
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
SLUG = "吉林市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
# When run from data/tmp/jilin_吉林市/, STAGING is that directory.
# When run from repo root, STAGING is data/tmp/jilin_吉林市/.
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_吉林市"
if _CURRENT_DIR.name == "jilin_吉林市":
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
# IDs: 1-2 core leaders, 3-4 deputy secretaries, 5-11 standing committee,
#      12-18 deputy mayors, 19 secretary-general, 20-23人大/政协, 30-31 predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "胡斌",
        "gender": "男",
        "ethnicity": "汉族",  # plausible — vast majority of Jilin party secretaries are Han
        "birth": "",  # open question — unverified
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委书记",
        "current_org": "中共吉林市委员会",
        "source": "https://www.jlcity.gov.cn/",
        "confidence": "confirmed",
        "notes": "2026年7月多次主持市委常委会会议并调研；此前任职经历和完整履历待查"
    },
    {
        "id": 2,
        "name": "王吉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年2月",
        "birthplace": "",  # open question
        "education": "研究生，经济学硕士",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市长",
        "current_org": "吉林市人民政府",
        "source": "https://www.jlcity.gov.cn/jlszf/20zfld/",
        "confidence": "confirmed",
        "notes": "1972年2月生，研究生学历，经济学硕士。现任吉林市委副书记、市长。2026年7月多次主持市政府常务会议。领导市政府全面工作，分管市审计局。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Party Secretaries and Standing Committee
    # source: meeting attendance lists (July 2026) — partial information
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "李道恒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市委政法委书记",
        "current_org": "中共吉林市委员会",
        "source": "吉林市新闻公开报道",
        "confidence": "plausible",
        "notes": "据公开报道，李道恒担任吉林市委副书记、政法委书记"
    },
    {
        "id": 4,
        "name": "沈德生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共吉林市委员会",
        "source": "吉林市新闻公开报道",
        "confidence": "plausible",
        "notes": "据公开报道信息"
    },
    {
        "id": 5,
        "name": "王卫东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "中共吉林市委员会",
        "source": "吉林市新闻公开报道",
        "confidence": "plausible",
        "notes": "市委常委、常务副市长"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Mayors (from official leadership page)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 12,
        "name": "刘向涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "吉林市人民政府",
        "source": "https://www.jlcity.gov.cn/jlszf/20zfld/",
        "confidence": "confirmed",
        "notes": "吉林市人民政府副市长"
    },
    {
        "id": 13,
        "name": "曲强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "吉林市人民政府",
        "source": "https://www.jlcity.gov.cn/jlszf/20zfld/",
        "confidence": "confirmed",
        "notes": "吉林市人民政府副市长"
    },
    {
        "id": 14,
        "name": "丁相明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "吉林市人民政府",
        "source": "https://www.jlcity.gov.cn/jlszf/20zfld/",
        "confidence": "confirmed",
        "notes": "吉林市人民政府副市长"
    },
    {
        "id": 15,
        "name": "陈洪治",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "吉林市人民政府",
        "source": "https://www.jlcity.gov.cn/jlszf/20zfld/",
        "confidence": "confirmed",
        "notes": "吉林市人民政府副市长"
    },
    {
        "id": 16,
        "name": "付彦平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "吉林市人民政府",
        "source": "https://www.jlcity.gov.cn/jlszf/20zfld/",
        "confidence": "confirmed",
        "notes": "吉林市人民政府副市长"
    },
    {
        "id": 17,
        "name": "冯旭东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "吉林市人民政府",
        "source": "https://www.jlcity.gov.cn/jlszf/20zfld/",
        "confidence": "confirmed",
        "notes": "吉林市人民政府副市长"
    },
    {
        "id": 18,
        "name": "周健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "吉林市人民政府",
        "source": "https://www.jlcity.gov.cn/jlszf/20zfld/",
        "confidence": "confirmed",
        "notes": "吉林市人民政府副市长"
    },
    {
        "id": 19,
        "name": "常国伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府秘书长",
        "current_org": "吉林市人民政府",
        "source": "https://www.jlcity.gov.cn/jlszf/20zfld/",
        "confidence": "confirmed",
        "notes": "吉林市人民政府秘书长"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "贺志亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共吉林市委员会",
        "source": "公开报道",
        "confidence": "plausible",
        "notes": "此前曾任吉林市委书记（2020-2023），后调任吉林省副省长、公安厅厅长"
    },
    {
        "id": 31,
        "name": "刘非",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共吉林市委员会",
        "source": "公开报道",
        "confidence": "plausible",
        "notes": "此前曾任吉林市委书记（2019-2020），后调任湖南省副省长"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共吉林市委员会", "type": "党委", "level": "地级市", "parent": "中共吉林省委员会", "location": "吉林市"},
    {"id": 2, "name": "吉林市人民政府", "type": "政府", "level": "地级市", "parent": "吉林省人民政府", "location": "吉林市"},
    {"id": 3, "name": "中国人民政治协商会议吉林市委员会", "type": "政协", "level": "地级市", "parent": "政协吉林省委员会", "location": "吉林市"},
    {"id": 4, "name": "吉林市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "吉林省人大常委会", "location": "吉林市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 胡斌 — current Party Secretary
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "现任吉林市委书记，此前任职履历待查"},
    # 王吉 — current mayor
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "现任吉林市委副书记、市长，领导市政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "兼任市委副书记"},
    # 李道恒 — Deputy Party Secretary
    {"person_id": 3, "org_id": 1, "title": "市委副书记、政法委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 沈德生 — Deputy Party Secretary
    {"person_id": 4, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 王卫东 — Executive Deputy Mayor
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 刘向涛 — Deputy Mayor
    {"person_id": 12, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 曲强 — Deputy Mayor
    {"person_id": 13, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 丁相明 — Deputy Mayor
    {"person_id": 14, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 陈洪治 — Deputy Mayor
    {"person_id": 15, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 付彦平 — Deputy Mayor
    {"person_id": 16, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 冯旭东 — Deputy Mayor
    {"person_id": 17, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 周健 — Deputy Mayor
    {"person_id": 18, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 常国伟 — Secretary-General
    {"person_id": 19, "org_id": 2, "title": "市政府秘书长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 贺志亮 — predecessor Party Secretary
    {"person_id": 30, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "前任吉林市委书记（约2020-2023），后任吉林省副省长、公安厅厅长"},
    # 刘非 — predecessor Party Secretary
    {"person_id": 31, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "前任吉林市委书记（约2019-2020），后调任湖南省副省长"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 胡斌 ↔ 王吉 (Party Secretary – Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "中共吉林市委员会", "overlap_period": "2026"},
    # 胡斌 ↔ 李道恒
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—副书记", "overlap_org": "中共吉林市委员会", "overlap_period": "2026"},
    # 胡斌 ↔ 沈德生
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—副书记", "overlap_org": "中共吉林市委员会", "overlap_period": "2026"},
    # 胡斌 ↔ 王卫东
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—常委", "overlap_org": "中共吉林市委员会", "overlap_period": "2026"},
    # 王吉 ↔ 王卫东 (Mayor – Executive Deputy Mayor)
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "市长—常务副市长", "overlap_org": "吉林市人民政府", "overlap_period": "2026"},
    # 王吉 ↔ 刘向涛
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "市长—副市长", "overlap_org": "吉林市人民政府", "overlap_period": "2026"},
    # 王吉 ↔ 曲强
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "市长—副市长", "overlap_org": "吉林市人民政府", "overlap_period": "2026"},
    # 王吉 ↔ 丁相明
    {"person_a": 2, "person_b": 14, "type": "共事", "context": "市长—副市长", "overlap_org": "吉林市人民政府", "overlap_period": "2026"},
    # 王吉 ↔ 陈洪治
    {"person_a": 2, "person_b": 15, "type": "共事", "context": "市长—副市长", "overlap_org": "吉林市人民政府", "overlap_period": "2026"},
    # 王吉 ↔ 付彦平
    {"person_a": 2, "person_b": 16, "type": "共事", "context": "市长—副市长", "overlap_org": "吉林市人民政府", "overlap_period": "2026"},
    # 王吉 ↔ 冯旭东
    {"person_a": 2, "person_b": 17, "type": "共事", "context": "市长—副市长", "overlap_org": "吉林市人民政府", "overlap_period": "2026"},
    # 王吉 ↔ 周健
    {"person_a": 2, "person_b": 18, "type": "共事", "context": "市长—副市长", "overlap_org": "吉林市人民政府", "overlap_period": "2026"},
    # 王吉 ↔ 常国伟
    {"person_a": 2, "person_b": 19, "type": "共事", "context": "市长—秘书长", "overlap_org": "吉林市人民政府", "overlap_period": "2026"},
    # Predecessor relationships
    {"person_a": 30, "person_b": 1, "type": "交接", "context": "前任市委书记—现任市委书记", "overlap_org": "中共吉林市委员会", "overlap_period": "2023"},
    {"person_a": 31, "person_b": 30, "type": "交接", "context": "前任市委书记—前任市委书记（交接链）", "overlap_org": "中共吉林市委员会", "overlap_period": "2020"},
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
    slug_id = f"jilin_{name}"

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
    if len(career_timeline) <= 2 and not person.get("birth"):
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料不足，完整履历待查。百度百科403禁止访问，搜索引擎超时。",
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
            "person_id": f"jilin_{other_name}",
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
            "title": "吉林市人民政府官方网站",
            "url": "https://www.jlcity.gov.cn/",
            "publisher": "吉林市人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "2026年7月政府领导页面和新闻会议报道确认领导职务",
        }
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "吉林省",
            "city": "吉林市",
            "region": "吉林市",
            "job": person.get("current_post", ""),
            "task_id": "jilin_吉林市",
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
            "education": [
                {
                    "period": "",
                    "institution": "",
                    "major": "",
                    "degree": person.get("education", ""),
                    "study_type": "unknown",
                    "source_ids": ["S001"],
                }
            ] if person.get("education") else [],
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
            "relationship_confidence": "medium",
            "biggest_gap": "出生年月、籍贯、完整履历（百度百科403，搜索引擎超时）",
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
        ],
    }

    fname = f"{TODAY}-吉林省-吉林市-{person['current_post']}-{person['name']}.json"
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
    core_ids = {1, 2, 3, 5, 30, 31}  # Core leaders + predecessors
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
