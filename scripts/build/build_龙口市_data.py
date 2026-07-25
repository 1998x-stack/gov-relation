#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 龙口市 (Longkou City), 山东省.

Investigation date: 2026-07-25
Task ID: shandong_龙口市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - www.longkou.gov.cn — 龙口市人民政府官方网站 (primary, current as of July 2026)
  - Leadership page: https://www.longkou.gov.cn/col/col108289/index.html (confirmed 市长/副市长)
  - News articles from longkou.gov.cn (July 2026)
  - Wikipedia zh/en for geographic and administrative info
  - Web search was degraded: Baidu Baike 403, Exa rate-limited, Jina Reader timeouts

Confirmed current officeholders (as of 2026-07):
  市长: 卢一男 (official profile on longkou.gov.cn)
  常务副市长: 孙庆钊 (official profile)
  副市长: 夏俊庆, 张旭, 殷波, 邢斌, 赵静, 李磊, 王学军
  市委副书记、组织部部长: 姜利春 (confirmed via news article 2026-07-13)
  
  Note: 市委书记 information is NOT available on the longkou.gov.cn site
  (which only lists 市政府领导, not 市委领导). The name of the current
  Party Secretary is marked as unverified.

Confidence notes:
  - Current roles of 市长 and 副市长: confirmed via official government profiles (July 2026)
  - 卢一男's identity: confirmed via official profile (男,汉族,1982.02出生,在职研究生,中共党员)
  - 孙庆钊's identity: confirmed via official profile (男,汉族,1985.11出生,本科,中共党员)
  - 夏俊庆's identity: confirmed via official profile (男,汉族,1977.11出生,大学,中共党员)
  - 市委书记 identity: unverified — web search degraded
  - All biographical details (birthplace, education, early career): limited sources
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
SLUG = "龙口市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shandong_龙口市"
if _CURRENT_DIR.name == "shandong_龙口市":
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
# IDs: 1-9 core leadership, 10-19 deputy mayors/standing committee, 30+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    # NOTE: 市委书记 (Party Secretary) — name is unconfirmed via official sources.
    # The longkou.gov.cn site only lists 市政府领导, not 市委领导.
    # Marked as open question.
    {
        "id": 1,
        "name": "【待查】市委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共龙口市委员会",
        "source": "https://www.longkou.gov.cn/",
        "confidence": "unverified",
        "notes": "市委书记姓名未从官方渠道确认。longkou.gov.cn仅有市政府领导名单。建议通过烟台市委组织部网站或龙口市委官网进一步确认。"
    },
    {
        "id": 2,
        "name": "卢一男",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年2月",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "龙口市人民政府",
        "source": "https://www.longkou.gov.cn/col/col118021/index.html",
        "confidence": "confirmed",
        "notes": "龙口市委副书记、市政府市长、党组书记。主持市政府全面工作，负责财税、审计方面的工作。1982年2月出生，在职研究生学历。2026年7月多次出席市政府常务会议及调研活动。"
    },
    {
        "id": 3,
        "name": "孙庆钊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年11月",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、统战部部长、常务副市长",
        "current_org": "中共龙口市委员会",
        "source": "https://www.longkou.gov.cn/col/col108311/index.html",
        "confidence": "confirmed",
        "notes": "龙口市委常委、统战部部长，市政府副市长、党组副书记，市政协党组副书记。1985年11月生，本科学历。负责市政府常务工作，协助市长负责财税、审计工作。分管发展改革、教育体育、人社、交通、应急、商务、统计、市场监管、裕龙石化产业园等。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Party Secretary
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 4,
        "name": "姜利春",
        "gender": "男",
        "ethnicity": "",  # unverified
        "birth": "",  # unverified
        "birthplace": "",  # unverified
        "education": "",  # unverified
        "party_join": "中共党员",
        "work_start": "",  # unverified
        "current_post": "市委副书记、组织部部长",
        "current_org": "中共龙口市委员会",
        "source": "https://www.longkou.gov.cn/col/col14991/art/2026/art_47c9916fbaa1402a9b2e3fb3b5e208b2.html",
        "confidence": "plausible",
        "notes": "2026年7月8日以龙口市委副书记、组织部部长身份出席龙口市网络主播协会成立大会（龙口市政府官网新闻）。之前职务：2024-2025年曾任龙口市委常委、组织部部长。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Mayors (副市长) & Standing Committee
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 5,
        "name": "夏俊庆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年11月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、宣传部部长、副市长",
        "current_org": "龙口市人民政府",
        "source": "https://www.longkou.gov.cn/col/col108289/xjq/index.html",
        "confidence": "confirmed",
        "notes": "龙口市委常委、宣传部部长、市政府副市长、党组成员。1977年11月生，大学学历。负责自然资源和规划、住房和城乡建设、水务、林业、生态环境等工作。"
    },
    {
        "id": 6,
        "name": "张旭",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "龙口市人民政府",
        "source": "https://www.longkou.gov.cn/col/col108289/index.html",
        "confidence": "confirmed",
        "notes": "龙口市政府副市长。列在longkou.gov.cn市政府领导名单中，具体分工待查。"
    },
    {
        "id": 7,
        "name": "殷波",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "龙口市人民政府",
        "source": "https://www.longkou.gov.cn/col/col108289/index.html",
        "confidence": "confirmed",
        "notes": "龙口市政府副市长。列在longkou.gov.cn市政府领导名单中，具体分工待查。"
    },
    {
        "id": 8,
        "name": "邢斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "龙口市人民政府",
        "source": "https://www.longkou.gov.cn/col/col108289/index.html",
        "confidence": "confirmed",
        "notes": "龙口市政府副市长。列在longkou.gov.cn市政府领导名单中，具体分工待查。"
    },
    {
        "id": 9,
        "name": "赵静",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "龙口市人民政府",
        "source": "https://www.longkou.gov.cn/col/col108289/index.html",
        "confidence": "confirmed",
        "notes": "龙口市政府副市长。列在longkou.gov.cn市政府领导名单中，具体分工待查。"
    },
    {
        "id": 10,
        "name": "李磊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、诸由观镇党委书记",
        "current_org": "龙口市人民政府",
        "source": "https://www.longkou.gov.cn/col/col108289/index.html",
        "confidence": "confirmed",
        "notes": "龙口市政府副市长，同时兼任诸由观镇党委书记（2026年7月8日以副市长、诸由观镇党委书记身份出席网络主播协会成立大会）。"
    },
    {
        "id": 11,
        "name": "王学军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "龙口市人民政府",
        "source": "https://www.longkou.gov.cn/col/col108289/index.html",
        "confidence": "confirmed",
        "notes": "龙口市政府副市长。列在longkou.gov.cn市政府领导名单中，具体分工待查。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共龙口市委员会", "type": "党委", "level": "县级市", "parent": "中共烟台市委员会", "location": "龙口市"},
    {"id": 2, "name": "龙口市人民政府", "type": "政府", "level": "县级市", "parent": "烟台市人民政府", "location": "龙口市"},
    {"id": 3, "name": "龙口市人大常委会", "type": "人大", "level": "县级市", "parent": "烟台市人大常委会", "location": "龙口市"},
    {"id": 4, "name": "龙口市政协", "type": "政协", "level": "县级市", "parent": "烟台市政协", "location": "龙口市"},
    {"id": 5, "name": "中共龙口市委组织部", "type": "党委", "level": "县级市", "parent": "中共龙口市委员会", "location": "龙口市"},
    {"id": 6, "name": "中共龙口市委宣传部", "type": "党委", "level": "县级市", "parent": "中共龙口市委员会", "location": "龙口市"},
    {"id": 7, "name": "中共龙口市委统战部", "type": "党委", "level": "县级市", "parent": "中共龙口市委员会", "location": "龙口市"},
    {"id": 8, "name": "诸由观镇", "type": "乡镇/街道", "level": "乡镇级", "parent": "龙口市人民政府", "location": "龙口市"},
    {"id": 9, "name": "龙口经济开发区", "type": "开发区", "level": "县级市", "parent": "龙口市人民政府", "location": "龙口市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 【待查】市委书记 (name unverified)
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正处级（县级市）", "note": "现任市委书记，姓名待确证"},
    # 卢一男 — 市长
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "正处级（县级市）", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市长、党组书记", "start_date": "", "end_date": "", "rank": "正处级（县级市）", "note": "主持市政府全面工作"},
    # 孙庆钊 — 常务副市长
    {"person_id": 3, "org_id": 1, "title": "市委常委、统战部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "副市长、党组副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "负责市政府常务工作"},
    {"person_id": 3, "org_id": 4, "title": "市政协党组副书记", "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 姜利春 — Deputy Party Secretary
    {"person_id": 4, "org_id": 1, "title": "市委副书记、组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "2026年7月任市委副书记兼组织部部长"},
    {"person_id": 4, "org_id": 5, "title": "组织部部长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    # 夏俊庆 — 副市长/宣传部部长
    {"person_id": 5, "org_id": 1, "title": "市委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 6, "title": "宣传部部长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": "负责自然资源、住建、水务、林业、生态环境等"},
    # 张旭 — 副市长
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": "具体分工待查"},
    # 殷波 — 副市长
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": "具体分工待查"},
    # 邢斌 — 副市长
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": "具体分工待查"},
    # 赵静 — 副市长
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": "具体分工待查"},
    # 李磊 — 副市长/镇党委书记
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 8, "title": "诸由观镇党委书记", "start_date": "", "end_date": "", "rank": "正科级", "note": "兼任"},
    # 王学军 — 副市长
    {"person_id": 11, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": "具体分工待查"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 市委书记 ↔ 卢一男 (Party Secretary – Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "中共龙口市委员会", "overlap_period": "2026"},
    # 卢一男 ↔ 孙庆钊 (Mayor – Executive Deputy Mayor)
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "市长—常务副市长", "overlap_org": "龙口市人民政府", "overlap_period": "2026"},
    # 卢一男 ↔ 姜利春 (Mayor – Deputy Party Secretary)
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "市长—市委副书记", "overlap_org": "中共龙口市委员会", "overlap_period": "2026"},
    # 孙庆钊 ↔ 夏俊庆 (Standing Committee peers)
    {"person_a": 3, "person_b": 5, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共龙口市委员会", "overlap_period": "2026"},
    # 卢一男 ↔ 夏俊庆 (Mayor – Deputy Mayor)
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "市长—副市长", "overlap_org": "龙口市人民政府", "overlap_period": "2026"},
    # 卢一男 ↔ 张旭
    {"person_a": 2, "person_b": 6, "type": "共事", "context": "市长—副市长", "overlap_org": "龙口市人民政府", "overlap_period": "2026"},
    # 卢一男 ↔ 殷波
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "市长—副市长", "overlap_org": "龙口市人民政府", "overlap_period": "2026"},
    # 卢一男 ↔ 邢斌
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "市长—副市长", "overlap_org": "龙口市人民政府", "overlap_period": "2026"},
    # 卢一男 ↔ 赵静
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "市长—副市长", "overlap_org": "龙口市人民政府", "overlap_period": "2026"},
    # 卢一男 ↔ 李磊
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "市长—副市长", "overlap_org": "龙口市人民政府", "overlap_period": "2026"},
    # 卢一男 ↔ 王学军
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "市长—副市长", "overlap_org": "龙口市人民政府", "overlap_period": "2026"},
    # 孙庆钊 ↔ 姜利春 (Standing Committee peers)
    {"person_a": 3, "person_b": 4, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共龙口市委员会", "overlap_period": "2026"},
    # 姜利春 ↔ 夏俊庆 (Standing Committee peers)
    {"person_a": 4, "person_b": 5, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共龙口市委员会", "overlap_period": "2026"},
    # 李磊 ↔ 诸由观镇 (concurrent role link — implicit via positions)
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
    slug_id = f"longkou_{name}"

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
            "confidence": person.get("confidence", "unverified"),
            "source_ids": ["S001"],
        })

    # Add gap entry if career_timeline is sparse
    if len(career_timeline) <= 1 and not person.get("birth"):
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
            "person_id": f"longkou_{other_name}",
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
            "title": "龙口市人民政府官方网站",
            "url": source_url,
            "publisher": "龙口市人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "2026年7月市政府领导页面及新闻",
        }
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "山东省",
            "city": "龙口市",
            "region": "龙口市",
            "job": person.get("current_post", ""),
            "task_id": "shandong_龙口市",
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

    # Add extra open question for 市委书记
    if name == "【待查】市委书记":
        record["open_questions"].insert(0, {
            "priority": "critical",
            "question": "龙口市委书记姓名确认",
            "why_it_matters": "核心目标人物之一，缺少姓名则无法进行任何关系分析",
            "suggested_queries": ["龙口市 市委书记 现任", "烟台龙口 市委领导", "龙口市委 领导分工"],
            "last_attempted": AS_OF,
        })

    fname = f"{TODAY}-山东省-龙口市-{person['current_post']}-{person['name']}.json"
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
    core_ids = {1, 2, 3, 4}  # 市委书记(待查), 卢一男, 孙庆钊, 姜利春
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
