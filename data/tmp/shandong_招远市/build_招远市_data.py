#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 招远市 (Zhaoyuan City), 山东省.

Investigation date: 2026-07-25
Task ID: shandong_招远市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - www.zhaoyuan.gov.cn — 招远市人民政府官方网站 (primary, current as of July 2026)
  - Leadership page: https://www.zhaoyuan.gov.cn/col/col49650/index.html (confirmed 市长/副市长)
  - Mayor detail: https://www.zhaoyuan.gov.cn/col/col118126/index.html (李鹏程, confirmed)
  - Deputy mayor details: various /col/ pages (confirmed)
  - Wikipedia zh/en for geographic and administrative info
  - Web search was degraded: Baidu Baike 403, Exa rate-limited, Jina Reader timeouts

Confirmed current officeholders (as of 2026-07):
  市长: 李鹏程 (official profile on zhaoyuan.gov.cn)
  副市长: 逄阳 (兼市委常委、市委办公室主任), 刘福利, 荆兴业, 李晓东 (兼公安局长), 徐营

  Note: 市委书记 information is NOT available on the zhaoyuan.gov.cn site
  (which only lists 市政府领导, not 市委领导). The name of the current
  Party Secretary is marked as unverified.

Confidence notes:
  - Current roles of 市长 and 副市长: confirmed via official government profiles (July 2026)
  - 李鹏程's identity: confirmed via official profile (男,汉族,1980.01出生,省委党校研究生,中共党员)
  - 逄阳's identity: confirmed via official profile (男,汉族,1986.05出生,省委党校研究生,中共党员)
  - 刘福利's identity: confirmed via official profile (男,汉族,1976.04出生,省委党校研究生,中共党员)
  - 荆兴业's identity: confirmed via official profile (男,汉族,1986.11出生,大学,中共党员)
  - 李晓东's identity: confirmed via official profile (男,汉族,1981.11出生,大学,中共党员)
  - 徐营's identity: confirmed via official profile (男,汉族,1986.10出生,研究生,哲学硕士,中共党员)
  - 市委书记 identity: unverified — not listed on government site, web search degraded
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
SLUG = "招远市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shandong_招远市"
if _CURRENT_DIR.name == "shandong_招远市":
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
    # The zhaoyuan.gov.cn site only lists 市政府领导, not 市委领导.
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
        "current_org": "中共招远市委员会",
        "source": "https://www.zhaoyuan.gov.cn/",
        "confidence": "unverified",
        "notes": "市委书记姓名未从官方渠道确认。zhaoyuan.gov.cn仅有市政府领导名单。建议通过烟台市委组织部网站或招远市委官网进一步确认。"
    },
    {
        "id": 2,
        "name": "李鹏程",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年1月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "招远市人民政府",
        "source": "https://www.zhaoyuan.gov.cn/col/col118126/index.html",
        "confidence": "confirmed",
        "notes": "招远市委副书记，市政府党组书记、市长。主持市政府全面工作，负责财税、审计等方面的工作。分管市财政局（市国有资产监督管理局）、市审计局。1980年1月生，省委党校研究生学历。2026年7月多次出席市政府常务会议及调研活动。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Mayors (副市长) — all confirmed via official government site
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "逄阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年5月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市委办公室主任、副市长",
        "current_org": "中共招远市委员会",
        "source": "https://www.zhaoyuan.gov.cn/col/col111992/index.html",
        "confidence": "confirmed",
        "notes": "招远市委常委、市委办公室主任，市政府党组成员、副市长。负责工业和信息化、住房和城乡建设、文化和旅游等方面的工作。分管市工业和信息化局、市住房和城乡建设局、市文化和旅游局。1986年5月生，省委党校研究生学历。"
    },
    {
        "id": 4,
        "name": "刘福利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年4月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "招远市人民政府",
        "source": "https://www.zhaoyuan.gov.cn/col/col60618/index.html",
        "confidence": "confirmed",
        "notes": "招远市人民政府党组成员、副市长，兼任市红十字会会长、市计划生育协会会长。负责教育和体育、科学技术、卫生健康、医疗保障、疫情防控等方面的工作。分管市教育和体育局、市科学技术局、市卫生健康局、市医疗保障局等。1976年4月生，省委党校研究生学历。"
    },
    {
        "id": 5,
        "name": "荆兴业",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年11月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "招远市人民政府",
        "source": "https://www.zhaoyuan.gov.cn/col/col60619/index.html",
        "confidence": "confirmed",
        "notes": "招远市人民政府党组成员、副市长。负责交通运输、水务、农业农村、乡村振兴、扶贫、生态环境等方面的工作。分管市交通运输局、市水务局、市农业农村局（市乡村振兴局、市畜牧兽医局）、市供销合作社联合社。1986年11月生，大学学历。"
    },
    {
        "id": 6,
        "name": "李晓东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年11月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市公安局局长",
        "current_org": "招远市人民政府",
        "source": "https://www.zhaoyuan.gov.cn/col/col118422/index.html",
        "confidence": "confirmed",
        "notes": "招远市人民政府党组成员、副市长，市公安局党委书记、局长、督察长、四级高级警长，兼任市委政法委员会副书记。负责公安、司法、退役军人事务、信访等方面的工作。分管市公安局、市司法局、市退役军人事务局、市信访局。1981年11月生，大学学历。"
    },
    {
        "id": 7,
        "name": "徐营",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年10月",
        "birthplace": "",
        "education": "研究生、哲学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "招远市人民政府",
        "source": "https://www.zhaoyuan.gov.cn/col/col119963/index.html",
        "confidence": "confirmed",
        "notes": "招远市人民政府党组成员、副市长。负责民政、市场监管、综合行政执法、林业等方面的工作。分管市民政局、市市场监督管理局、市综合行政执法局（市城市管理局）、市林业局、市罗山省级自然保护区管理服务中心等。1986年10月生，研究生学历，哲学硕士。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共招远市委员会", "type": "党委", "level": "县级市", "parent": "中共烟台市委员会", "location": "招远市"},
    {"id": 2, "name": "招远市人民政府", "type": "政府", "level": "县级市", "parent": "烟台市人民政府", "location": "招远市"},
    {"id": 3, "name": "招远市人大常委会", "type": "人大", "level": "县级市", "parent": "烟台市人大常委会", "location": "招远市"},
    {"id": 4, "name": "招远市政协", "type": "政协", "level": "县级市", "parent": "烟台市政协", "location": "招远市"},
    {"id": 5, "name": "中共招远市委办公室", "type": "党委", "level": "县级市", "parent": "中共招远市委员会", "location": "招远市"},
    {"id": 6, "name": "招远市公安局", "type": "政府", "level": "县级市", "parent": "招远市人民政府", "location": "招远市"},
    {"id": 7, "name": "招远市财政局", "type": "政府", "level": "县级市", "parent": "招远市人民政府", "location": "招远市"},
    {"id": 8, "name": "招远市审计局", "type": "政府", "level": "县级市", "parent": "招远市人民政府", "location": "招远市"},
    {"id": 9, "name": "招远市工业和信息化局", "type": "政府", "level": "县级市", "parent": "招远市人民政府", "location": "招远市"},
    {"id": 10, "name": "招远市教育和体育局", "type": "政府", "level": "县级市", "parent": "招远市人民政府", "location": "招远市"},
    {"id": 11, "name": "招远市交通运输局", "type": "政府", "level": "县级市", "parent": "招远市人民政府", "location": "招远市"},
    {"id": 12, "name": "招远市农业农村局", "type": "政府", "level": "县级市", "parent": "招远市人民政府", "location": "招远市"},
    {"id": 13, "name": "招远市卫生健康局", "type": "政府", "level": "县级市", "parent": "招远市人民政府", "location": "招远市"},
    {"id": 14, "name": "招远市市场监督管理局", "type": "政府", "level": "县级市", "parent": "招远市人民政府", "location": "招远市"},
    {"id": 15, "name": "招远市综合行政执法局", "type": "政府", "level": "县级市", "parent": "招远市人民政府", "location": "招远市"},
    {"id": 16, "name": "招远市信访局", "type": "政府", "level": "县级市", "parent": "招远市人民政府", "location": "招远市"},
    {"id": 17, "name": "招远市司法局", "type": "政府", "level": "县级市", "parent": "招远市人民政府", "location": "招远市"},
    {"id": 18, "name": "招远市林业局", "type": "政府", "level": "县级市", "parent": "招远市人民政府", "location": "招远市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 【待查】市委书记 (name unverified)
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正处级（县级市）", "note": "现任市委书记，姓名待确证"},
    # 李鹏程 — 市长
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "正处级（县级市）", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市长、党组书记", "start_date": "", "end_date": "", "rank": "正处级（县级市）", "note": "主持市政府全面工作，负责财税、审计"},
    # 逄阳 — 市委常委、市委办公室主任、副市长
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 5, "title": "市委办公室主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "副市长、党组成员", "start_date": "", "end_date": "", "rank": "副处级", "note": "负责工信、住建、文旅等"},
    # 刘福利 — 副市长
    {"person_id": 4, "org_id": 2, "title": "副市长、党组成员", "start_date": "", "end_date": "", "rank": "副处级", "note": "负责教育体育、科技、卫健、医保等"},
    # 荆兴业 — 副市长
    {"person_id": 5, "org_id": 2, "title": "副市长、党组成员", "start_date": "", "end_date": "", "rank": "副处级", "note": "负责交通、水务、农业农村、乡村振兴、生态环境等"},
    # 李晓东 — 副市长、公安局长
    {"person_id": 6, "org_id": 2, "title": "副市长、党组成员", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 6, "title": "党委书记、局长、督察长", "start_date": "", "end_date": "", "rank": "副处级", "note": "四级高级警长"},
    # 徐营 — 副市长
    {"person_id": 7, "org_id": 2, "title": "副市长、党组成员", "start_date": "", "end_date": "", "rank": "副处级", "note": "负责民政、市场监管、综合行政执法、林业等"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 市委书记 ↔ 李鹏程 (Party Secretary – Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "中共招远市委员会", "overlap_period": "2026"},
    # 李鹏程 ↔ 逄阳 (Mayor – Deputy Mayor, Standing Committee)
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "市长—副市长（市委常委）", "overlap_org": "招远市人民政府", "overlap_period": "2026"},
    # 李鹏程 ↔ 刘福利
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "市长—副市长", "overlap_org": "招远市人民政府", "overlap_period": "2026"},
    # 李鹏程 ↔ 荆兴业
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "市长—副市长", "overlap_org": "招远市人民政府", "overlap_period": "2026"},
    # 李鹏程 ↔ 李晓东
    {"person_a": 2, "person_b": 6, "type": "共事", "context": "市长—副市长", "overlap_org": "招远市人民政府", "overlap_period": "2026"},
    # 李鹏程 ↔ 徐营
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "市长—副市长", "overlap_org": "招远市人民政府", "overlap_period": "2026"},
    # 逄阳 ↔ 刘福利 (Deputy Mayor peers)
    {"person_a": 3, "person_b": 4, "type": "同僚", "context": "副市长同僚", "overlap_org": "招远市人民政府", "overlap_period": "2026"},
    # 逄阳 ↔ 荆兴业
    {"person_a": 3, "person_b": 5, "type": "同僚", "context": "副市长同僚", "overlap_org": "招远市人民政府", "overlap_period": "2026"},
    # 逄阳 ↔ 李晓东
    {"person_a": 3, "person_b": 6, "type": "同僚", "context": "副市长同僚", "overlap_org": "招远市人民政府", "overlap_period": "2026"},
    # 逄阳 ↔ 徐营
    {"person_a": 3, "person_b": 7, "type": "同僚", "context": "副市长同僚", "overlap_org": "招远市人民政府", "overlap_period": "2026"},
    # 刘福利 ↔ 荆兴业
    {"person_a": 4, "person_b": 5, "type": "同僚", "context": "副市长同僚", "overlap_org": "招远市人民政府", "overlap_period": "2026"},
    # 刘福利 ↔ 李晓东
    {"person_a": 4, "person_b": 6, "type": "同僚", "context": "副市长同僚", "overlap_org": "招远市人民政府", "overlap_period": "2026"},
    # 刘福利 ↔ 徐营
    {"person_a": 4, "person_b": 7, "type": "同僚", "context": "副市长同僚", "overlap_org": "招远市人民政府", "overlap_period": "2026"},
    # 荆兴业 ↔ 李晓东
    {"person_a": 5, "person_b": 6, "type": "同僚", "context": "副市长同僚", "overlap_org": "招远市人民政府", "overlap_period": "2026"},
    # 荆兴业 ↔ 徐营
    {"person_a": 5, "person_b": 7, "type": "同僚", "context": "副市长同僚", "overlap_org": "招远市人民政府", "overlap_period": "2026"},
    # 李晓东 ↔ 徐营
    {"person_a": 6, "person_b": 7, "type": "同僚", "context": "副市长同僚", "overlap_org": "招远市人民政府", "overlap_period": "2026"},
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
    slug_id = f"zhaoyuan_{name}"

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
            "person_id": f"zhaoyuan_{other_name}",
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
            "title": "招远市人民政府官方网站",
            "url": source_url,
            "publisher": "招远市人民政府",
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
            "city": "招远市",
            "region": "招远市",
            "job": person.get("current_post", ""),
            "task_id": "shandong_招远市",
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
            "question": "招远市委书记姓名确认",
            "why_it_matters": "核心目标人物之一，缺少姓名则无法进行任何关系分析",
            "suggested_queries": ["招远市 市委书记 现任", "烟台招远 市委领导", "招远市委 领导分工"],
            "last_attempted": AS_OF,
        })

    fname = f"{TODAY}-山东省-招远市-{person['current_post']}-{person['name']}.json"
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
    core_ids = {1, 2}  # 市委书记(待查), 李鹏程
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
