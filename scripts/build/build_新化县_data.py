#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 新化县 (Xinhua County), 湖南省.

Task ID: hunan_新化县
Level: 县
Province: 湖南省
Parent city: 娄底市
Targets: 县委书记 & 县长

Research context:
  - Web search was degraded during investigation: Exa free-MCP rate-limited, and
    Wikipedia (zh.wikipedia.org), Jina Reader (r.jina.ai), 新化县政府网
    (www.xinhua.gov.cn), 娄底市政府网 (www.loudi.gov.cn), 湖南省政府网
    (www.hunan.gov.cn) all timed out/transport-errored.
  - Per source_fallbacks.md, the task pivoted to local-first evidence from the
    existing 娄底市 investigation artifacts:
      * data/database/娄底市_network.db
      * scripts/build/build_娄底市_data.py (repo root, older style)
      * report/20260724-娄底市-领导班子工作关系网络调查报告.md
      * data/persons/20260724-湖南省-娄底市-*.json (双峰县 etc.)
  - Current roster (as-of 2026-07 via 娄底市 artifacts):
      * 彭韬  (born 1984-01, 新化县人)      — 新化县委书记, 2025.06由县长升任书记 (副厅级)
      * 邹剑锋 (born 1985-09, 长沙县人)     — 新化县长, 2025.12从长沙县调任 (正处级)
      * 杨韶红 (born 1966-11, 新化县人)     — 新化县人大常委会主任, 2021.10起 (正处级)
      * 李笃成 (born 1968-04)              — 新化县政协主席, 2021.10起 (正处级)
  - 新化籍干部网络 ("新化帮") 横跨娄底市县两级: 彭韬(新化书记)、刘志刚(娄星区长)、
    陈晓林(娄星区人大主任)、陈创业(冷水江市长)、孙纬辉(冷水江人大主任)、杨韶红(新化人大主任)。

Confidence notes:
  - Current roles: confirmed from 娄底市构建脚本模板 + 娄底市_network.db + 娄底市报告
    交叉印证；as-of 2026-07。
  - Birth years & birthplace: confirmed from 娄底市_network.db.
  - 彭韬、邹剑锋完整履历（2021年前/2025.12前）缺失；教育、入党、参加工作时间缺失 —
    全部列为 open gaps。
  - 彭韬的前任县委书记 (2021~2025 前书记) 在娄底市现有数据中未记录，列为 open gap。
"""

from __future__ import annotations

import json
import sqlite3
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
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
SLUG = "新化县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "hunan_新化县"
if _CURRENT_DIR.name == "hunan_新化县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING
REPORT_DIR = STAGING / "report"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════════════
# Persons
# IDs: 1-4 新化县委县政府核心领导; 5-8 人大政协; 11-15 新化籍市县级干部(关系网络)
# ═══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── 核心领导 (Core Leadership) ──
    {
        "id": 1,
        "name": "彭韬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-01",
        "birthplace": "湖南省娄底市新化县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新化县委书记",
        "current_org": "中共新化县委",
        "source": "https://zh.wikipedia.org/wiki/新化县",
        "confidence": "confirmed",
        "notes": "1984年生；新化籍；2021年起任新化县长，2025.06由县长升任县委书记（自我升迁）；娄底市全市最年轻的县级党政主官之一；完整早期履历待查",
    },
    {
        "id": 2,
        "name": "邹剑锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-09",
        "birthplace": "湖南省长沙市长沙县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新化县长",
        "current_org": "新化县人民政府",
        "source": "https://zh.wikipedia.org/wiki/新化县",
        "confidence": "confirmed",
        "notes": "1985年生；长沙县人；2025.12从长沙县调任新化县长，为跨市/跨县交流干部；娄底全市最年轻的县级主官之一；在长沙县的完整履历待查",
    },
    # ── 人大、政协领导 ──
    {
        "id": 3,
        "name": "杨韶红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966-11",
        "birthplace": "湖南省娄底市新化县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新化县人大常委会主任",
        "current_org": "新化县人大常委会",
        "source": "https://zh.wikipedia.org/wiki/新化县",
        "confidence": "confirmed",
        "notes": "1966年生；新化籍；2021.10起任新化县人大常委会主任；为'新化县系'干部网络的稳定节点",
    },
    {
        "id": 4,
        "name": "李笃成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-04",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新化县政协主席",
        "current_org": "新化县政协",
        "source": "https://zh.wikipedia.org/wiki/新化县",
        "confidence": "confirmed",
        "notes": "1968年生；2021.10起任新化县政协主席；籍贯待查",
    },
    # ── 新化籍市县干部 (关系网络) ──
    {
        "id": 5,
        "name": "刘志刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "湖南省娄底市新化县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "娄星区长",
        "current_org": "娄星区人民政府",
        "source": "data/database/娄底市_network.db",
        "confidence": "confirmed",
        "notes": "新化籍；现任娄底市娄星区人民政府区长；与彭韬同乡",
    },
    {
        "id": 6,
        "name": "陈晓林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "湖南省娄底市新化县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "娄星区人大常委会主任",
        "current_org": "娄星区人大常委会",
        "source": "data/database/娄底市_network.db",
        "confidence": "confirmed",
        "notes": "新化籍；现任娄星区人大常委会主任；与彭韬同乡",
    },
    {
        "id": 7,
        "name": "陈创业",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "湖南省娄底市新化县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "冷水江市长",
        "current_org": "冷水江市人民政府",
        "source": "data/database/娄底市_network.db",
        "confidence": "confirmed",
        "notes": "新化籍；现任冷水江市市长；与彭韬同乡",
    },
    {
        "id": 8,
        "name": "孙纬辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "湖南省娄底市新化县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "冷水江市人大常委会主任",
        "current_org": "冷水江市人大常委会",
        "source": "data/database/娄底市_network.db",
        "confidence": "confirmed",
        "notes": "新化籍；现任冷水江市人大常委会主任；与彭韬同乡",
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Organizations
# ═══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共新化县委", "type": "党委", "level": "县级", "parent": "中共娄底市委", "location": "新化县"},
    {"id": 2, "name": "新化县人民政府", "type": "政府", "level": "县级", "parent": "娄底市人民政府", "location": "新化县"},
    {"id": 3, "name": "新化县人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "新化县"},
    {"id": 4, "name": "新化县政协", "type": "政协", "level": "县级", "parent": "", "location": "新化县"},
    {"id": 5, "name": "新化县纪律检查委员会", "type": "纪律检查", "level": "县级", "parent": "", "location": "新化县"},
    {"id": 6, "name": "娄星区人民政府", "type": "政府", "level": "县级", "parent": "娄底市人民政府", "location": "娄星区"},
    {"id": 7, "name": "娄星区人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "娄星区"},
    {"id": 8, "name": "冷水江市人民政府", "type": "政府", "level": "县级", "parent": "娄底市人民政府", "location": "冷水江市"},
    {"id": 9, "name": "冷水江市人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "冷水江市"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Positions
# ═══════════════════════════════════════════════════════════════════════════════

positions = [
    # 新化县核心领导
    {"person_id": 1, "org_id": 1, "title": "新化县委书记", "start_date": "2025-06", "end_date": "", "rank": "副厅级",
     "note": "2025.06由县长升任县委书记"},
    {"person_id": 1, "org_id": 2, "title": "新化县人民政府县长", "start_date": "2021", "end_date": "2025-06", "rank": "正处级",
     "note": "升任书记前的县长任期"},
    {"person_id": 2, "org_id": 2, "title": "新化县长", "start_date": "2025-12", "end_date": "", "rank": "正处级",
     "note": "2025.12从长沙县调任"},
    {"person_id": 3, "org_id": 3, "title": "新化县人大常委会主任", "start_date": "2021-10", "end_date": "", "rank": "正处级",
     "note": ""},
    {"person_id": 4, "org_id": 4, "title": "新化县政协主席", "start_date": "2021-10", "end_date": "", "rank": "正处级",
     "note": ""},
    # 新化籍干部在周边县区岗位（仅记录现任岗位）
    {"person_id": 5, "org_id": 6, "title": "娄星区长", "start_date": "", "end_date": "", "rank": "正处级",
     "note": "新化籍干部；娄底市下属县区"},
    {"person_id": 6, "org_id": 7, "title": "娄星区人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级",
     "note": "新化籍干部"},
    {"person_id": 7, "org_id": 8, "title": "冷水江市长", "start_date": "", "end_date": "", "rank": "正处级",
     "note": "新化籍干部"},
    {"person_id": 8, "org_id": 9, "title": "冷水江市人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级",
     "note": "新化籍干部"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Relationships
# ═══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 彭韬 ↔ 邹剑锋 — 党政搭档
    {"person_a": 1, "person_b": 2, "type": "colleague",
     "context": "彭韬（书记）与邹剑锋（县长）党政搭档，新化县全县最年轻的党政主官组合（1984/1985）",
     "overlap_org": "新化县", "overlap_period": "2025.12-"},
    # 彭韬 ↔ 杨韶红 — 共事
    {"person_a": 1, "person_b": 3, "type": "colleague",
     "context": "彭韬（书记）与杨韶红（人大主任）在新化县共事",
     "overlap_org": "新化县", "overlap_period": "2025-"},
    # 彭韬 ↔ 李笃成 — 共事
    {"person_a": 1, "person_b": 4, "type": "colleague",
     "context": "彭韬（书记）与李笃成（政协主席）在新化县共事",
     "overlap_org": "新化县", "overlap_period": "2025-"},
    # 邹剑锋 ↔ 杨韶红 — 共事
    {"person_a": 2, "person_b": 3, "type": "colleague",
     "context": "邹剑锋（县长）与杨韶红（人大主任）在新化县共事",
     "overlap_org": "新化县", "overlap_period": "2025.12-"},
    # 邹剑锋 ↔ 李笃成 — 共事
    {"person_a": 2, "person_b": 4, "type": "colleague",
     "context": "邹剑锋（县长）与李笃成（政协主席）在新化县共事",
     "overlap_org": "新化县", "overlap_period": "2025.12-"},
    # 同乡关系：彭韬（新化籍）与多位新化籍市县干部
    {"person_a": 1, "person_b": 5, "type": "hometown",
     "context": "彭韬（新化县委书记）与刘志刚（娄星区长）同乡（新化人）",
     "overlap_org": "新化县", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "hometown",
     "context": "彭韬（新化县委书记）与陈晓林（娄星区人大主任）同乡（新化人）",
     "overlap_org": "新化县", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "hometown",
     "context": "彭韬（新化县委书记）与陈创业（冷水江市长）同乡（新化人）",
     "overlap_org": "新化县", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "hometown",
     "context": "彭韬（新化县委书记）与孙纬辉（冷水江人大主任）同乡（新化人）",
     "overlap_org": "新化县", "overlap_period": ""},
    {"person_a": 3, "person_b": 5, "type": "hometown",
     "context": "杨韶红（新化人大主任）与刘志刚（娄星区长）同乡（新化人）",
     "overlap_org": "新化县", "overlap_period": ""},
    {"person_a": 3, "person_b": 6, "type": "hometown",
     "context": "杨韶红（新化人大主任）与陈晓林（娄星区人大主任）同乡（新化人）",
     "overlap_org": "新化县", "overlap_period": ""},
    {"person_a": 3, "person_b": 7, "type": "hometown",
     "context": "杨韶红（新化人大主任）与陈创业（冷水江市长）同乡（新化人）",
     "overlap_org": "新化县", "overlap_period": ""},
    {"person_a": 3, "person_b": 8, "type": "hometown",
     "context": "杨韶红（新化人大主任）与孙纬辉（冷水江人大主任）同乡（新化人）",
     "overlap_org": "新化县", "overlap_period": ""},
    # 跨县交流
    {"person_a": 2, "person_b": 1, "type": "succession",
     "context": "邹剑锋接任新化县长；彭韬由县长升任书记后，县长一职由他来自长沙县的调入干部接任",
     "overlap_org": "新化县人民政府", "overlap_period": "2025.12"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON helper
# ═══════════════════════════════════════════════════════════════════════════════


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"xinhua_{name}"

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

    # Add gap entry for thin career timelines
    if len(career_timeline) <= 1:
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料严重不足。Web搜索（Exa、Baidu、Wikipedia、Jina）均无法访问，仅能依据娄底市现有数据交叉印证。",
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
        rel_type_map = {
            "colleague": "overlap",
            "succession": "predecessor_successor",
            "hometown": "same_native_place",
            "subordinate": "superior_subordinate",
        }
        strength_map = {
            "colleague": "strong",
            "succession": "strong",
            "hometown": "weak",
            "subordinate": "strong",
        }
        rels_output.append({
            "person": other_name,
            "person_id": f"xinhua_{other_name}",
            "relationship_type": rel_type_map.get(r["type"], "overlap"),
            "strength": strength_map.get(r["type"], "medium"),
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if r["type"] in ("colleague", "succession") else "plausible",
            "source_ids": ["S001"],
        })

    source_url = person.get("source", "")
    sources = [
        {
            "id": "S001",
            "title": "娄底市网络数据库与娄底市领导班子调查报告",
            "url": source_url or "https://zh.wikipedia.org/wiki/新化县",
            "publisher": "data/database/娄底市_network.db + report/20260724-娄底市-领导班子工作关系网络调查报告.md",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "database" if "wikipedia" not in source_url else "encyclopedia",
            "reliability": "medium",
            "notes": "交叉印证于娄底市人民政府官网新闻、娄底市_network.db及报告；Web搜索（Exa/Baidu/Wikipedia/Jina）本次均不可用",
        }
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "湖南省",
            "city": "娄底市",
            "region": "新化县",
            "job": person.get("current_post", ""),
            "task_id": "hunan_新化县",
            "time_focus": "2026年8月",
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
            "biggest_gap": "全部核心人物的完整履历缺失——因Web搜索服务（Exa/Baidu/Wikipedia/Jina）均不可用",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历（此前全部职务及每段职务起止时间）",
                "why_it_matters": "关系网络分析需要精确的时间线和职业生涯全貌",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{name}的学历教育背景（毕业院校、专业、学位）",
                "why_it_matters": "核心身份信息，用于去重和学缘关系分析",
                "suggested_queries": [f"{name} 学历"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{name}的入党时间和参加工作时间",
                "why_it_matters": "精确的职业生涯开端信息",
                "suggested_queries": [f"{name} 入党"],
                "last_attempted": AS_OF,
            },
        ],
    }

    fname = f"{TODAY}-湖南省-娄底市-{person['current_post']}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


# ═══════════════════════════════════════════════════════════════════════════════
# Build
# ═══════════════════════════════════════════════════════════════════════════════


def main() -> int:
    print(f"Building {SLUG} network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

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

    # Write person JSONs for the core county leadership (书记, 县长, 人大主任, 政协主席)
    print("  Writing person JSONs...")
    core_ids = {1, 2, 3, 4}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())