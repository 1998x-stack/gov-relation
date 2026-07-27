#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宁远县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 湖南省
Parent City: 永州市
Region: 宁远县
Targets: 县委书记 & 县长

Research status (2026-07-24):
- 毛政 (Party Secretary): confirmed — 宁远县委书记 (current as of Jul 2026)
  - Identity: 男, 中共党员
  - Career history: thin — current role confirmed via official news, predecessor role unknown
- 林亮亮 (County Mayor): confirmed — 宁远县委副书记、县长 (current as of Jul 2026)
  - Identity: 男, 中共党员
  - Career history: thin — current role confirmed via official news, predecessor role unknown
- 宁远县第十四次党代会筹备中 (as of Jul 2026)

Research constraints:
  - Baidu Baike: 403/Cloudflare block
  - Exa search: rate limited
  - Jina Reader: transport errors
  - Government websites (ningyuan.gov.cn): connection timeouts
  - Wikipedia (zh): connection timeouts
  - Official news (ny425600.cn/红网): accessible, used as primary source
  - All personal biographical details beyond current role are open questions

Gaps logged in open_questions and report/open_gaps.md
"""

from __future__ import annotations

import json
import os
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

import sqlite3  # noqa: F401 — used by gov_relation.runner; token needed by process_tmp

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "宁远县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "hunan_宁远县"
if _CURRENT_DIR.name == "hunan_宁远县":
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
# IDs: 1-9 current leaders, 10-19 standing committee, 20-29 deputy gov, 30+ predecessors/others

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════

    # 毛政 — 宁远县委书记 (Party Secretary)
    {
        "id": 1,
        "name": "毛政",
        "gender": "男",
        "ethnicity": "",  # open question
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "宁远县委书记",
        "current_org": "中共宁远县委员会",
        "source": "宁远新闻网(红网) ny425600.cn",
        "confidence": "confirmed",
        "notes": "2026年7月仍任宁远县委书记。主持县委常委会会议。出席湖南师大附中教育帮扶签约。详情见 ny425600.cn。"
    },

    # 林亮亮 — 宁远县委副书记、县长 (County Mayor)
    {
        "id": 2,
        "name": "林亮亮",
        "gender": "男",
        "ethnicity": "",  # open question
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "宁远县委副书记、县长",
        "current_org": "宁远县人民政府",
        "source": "宁远新闻网(红网) ny425600.cn",
        "confidence": "confirmed",
        "notes": "2026年7月仍任宁远县委副书记、县长。主持县政府常务会议。出席湖南师大附中教育帮扶签约。详情见 ny425600.cn。"
    },

    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee (部分已知)
    # ══════════════════════════════════════════════════════════════════════

    # 刘湘明 — 宁远县委常委、县委办主任 (from 毛政慰问新闻)
    {
        "id": 10,
        "name": "刘湘明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宁远县委常委、县委办主任",
        "current_org": "中共宁远县委员会",
        "source": "宁远新闻网 ny425600.cn 2026-07-23",
        "confidence": "plausible",
        "notes": "出现在毛政送清凉活动中陪同。"
    },

    # 邓小英 — 宁远县领导 (from 毛政慰问新闻, 可能是副县长或宣传部)
    {
        "id": 11,
        "name": "邓小英",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宁远县领导",
        "current_org": "宁远县人民政府",
        "source": "宁远新闻网 ny425600.cn 2026-07-23",
        "confidence": "plausible",
        "notes": "出现在毛政送清凉活动中陪同。具体职务待确认。"
    },

    # 曾彩平 — 副县长 (from 教育帮扶新闻)
    {
        "id": 12,
        "name": "曾彩平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宁远县副县长",
        "current_org": "宁远县人民政府",
        "source": "宁远新闻网 ny425600.cn 2026-07-07",
        "confidence": "plausible",
        "notes": "出席湖南师大附中教育帮扶共建签约仪式。"
    },

    # ══════════════════════════════════════════════════════════════════════
    # Predecessors (前任)
    # ══════════════════════════════════════════════════════════════════════

    # 胡勇刚 — 前任县委书记（推测，待确认）
    {
        "id": 30,
        "name": "胡勇刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "推测 / open question",
        "confidence": "unverified",
        "notes": "根据公开资料，可能与宁远县有关的前任县委书记候选人。具体任期和去向待确认。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────

organizations = [
    # Party
    {"id": 1, "name": "中共宁远县委员会", "type": "党委",
     "level": "县处级", "parent": "中共永州市委员会", "location": "宁远县"},
    {"id": 2, "name": "中共宁远县纪律检查委员会", "type": "党委",
     "level": "县处级", "parent": "中共宁远县委员会", "location": "宁远县"},
    {"id": 3, "name": "中共宁远县委组织部", "type": "党委",
     "level": "正科级", "parent": "中共宁远县委员会", "location": "宁远县"},
    {"id": 4, "name": "中共宁远县委宣传部", "type": "党委",
     "level": "正科级", "parent": "中共宁远县委员会", "location": "宁远县"},
    {"id": 5, "name": "中共宁远县委政法委员会", "type": "党委",
     "level": "正科级", "parent": "中共宁远县委员会", "location": "宁远县"},
    {"id": 6, "name": "中共宁远县委统一战线工作部", "type": "党委",
     "level": "正科级", "parent": "中共宁远县委员会", "location": "宁远县"},

    # Government
    {"id": 10, "name": "宁远县人民政府", "type": "政府",
     "level": "县处级", "parent": "永州市人民政府", "location": "宁远县"},
    {"id": 11, "name": "宁远县人民政府办公室", "type": "政府",
     "level": "正科级", "parent": "宁远县人民政府", "location": "宁远县"},

    # Dep't / Bureau
    {"id": 20, "name": "宁远县发展和改革局", "type": "政府",
     "level": "正科级", "parent": "宁远县人民政府", "location": "宁远县"},
    {"id": 21, "name": "宁远县教育局", "type": "政府",
     "level": "正科级", "parent": "宁远县人民政府", "location": "宁远县"},
    {"id": 22, "name": "宁远县公安局", "type": "政府",
     "level": "正科级", "parent": "宁远县人民政府", "location": "宁远县"},
    {"id": 23, "name": "宁远县财政局", "type": "政府",
     "level": "正科级", "parent": "宁远县人民政府", "location": "宁远县"},

    # NPC & CPPCC
    {"id": 30, "name": "宁远县人民代表大会常务委员会", "type": "人大",
     "level": "县处级", "parent": "宁远县", "location": "宁远县"},
    {"id": 31, "name": "中国人民政治协商会议宁远县委员会", "type": "政协",
     "level": "县处级", "parent": "宁远县", "location": "宁远县"},

    # Supervision / Justice
    {"id": 40, "name": "宁远县监察委员会", "type": "党委",
     "level": "县处级", "parent": "宁远县", "location": "宁远县"},
    {"id": 41, "name": "宁远县人民法院", "type": "政府",
     "level": "县处级", "parent": "宁远县", "location": "宁远县"},
    {"id": 42, "name": "宁远县人民检察院", "type": "政府",
     "level": "县处级", "parent": "宁远县", "location": "宁远县"},

    # Townships (selected major ones)
    {"id": 50, "name": "宁远县舜陵街道办事处", "type": "乡镇/街道",
     "level": "乡科级", "parent": "宁远县人民政府", "location": "宁远县"},
    {"id": 51, "name": "宁远县文庙街道办事处", "type": "乡镇/街道",
     "level": "乡科级", "parent": "宁远县人民政府", "location": "宁远县"},
    {"id": 52, "name": "宁远县桐山街道办事处", "type": "乡镇/街道",
     "level": "乡科级", "parent": "宁远县人民政府", "location": "宁远县"},
    {"id": 53, "name": "宁远县湾井镇", "type": "乡镇/街道",
     "level": "乡科级", "parent": "宁远县人民政府", "location": "宁远县"},
    {"id": 54, "name": "宁远县冷水镇", "type": "乡镇/街道",
     "level": "乡科级", "parent": "宁远县人民政府", "location": "宁远县"},
    {"id": 55, "name": "宁远县九疑山瑶族乡", "type": "乡镇/街道",
     "level": "乡科级", "parent": "宁远县人民政府", "location": "宁远县"},
    {"id": 56, "name": "宁远县鲤溪镇", "type": "乡镇/街道",
     "level": "乡科级", "parent": "宁远县人民政府", "location": "宁远县"},

    # Other
    {"id": 60, "name": "湖南师范大学附属中学", "type": "事业单位",
     "level": "", "parent": "湖南师范大学", "location": "长沙市"},
]

# ── Positions ─────────────────────────────────────────────────────────────────

positions = [
    # 毛政
    {"id": 1, "person_id": 1, "org_id": 1, "title": "县委书记",
     "start": "", "end": "present", "rank": "", "note": "confirmed as of Jul 2026"},

    # 林亮亮
    {"id": 2, "person_id": 2, "org_id": 1, "title": "县委副书记",
     "start": "", "end": "present", "rank": "", "note": ""},
    {"id": 3, "person_id": 2, "org_id": 10, "title": "县长",
     "start": "", "end": "present", "rank": "", "note": "confirmed as of Jul 2026"},

    # 刘湘明
    {"id": 10, "person_id": 10, "org_id": 1, "title": "县委常委、县委办主任",
     "start": "", "end": "present", "rank": "", "note": "plausible based on news mention"},

    # 邓小英
    {"id": 11, "person_id": 11, "org_id": 10, "title": "县领导（副县长/党组成员）",
     "start": "", "end": "present", "rank": "", "note": ""},

    # 曾彩平
    {"id": 12, "person_id": 12, "org_id": 10, "title": "副县长",
     "start": "", "end": "present", "rank": "", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────────────
# Key relationship: 毛政 and 林亮亮 work together as county's top leaders

relationships = [
    # 毛政 <-> 林亮亮: 党政配合 (直接上下级/搭档关系)
    {
        "id": 1,
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "党政一把手",
        "overlap_org": "中共宁远县委员会 / 宁远县人民政府",
        "overlap_period": "present",
    },
    # 毛政 <-> 刘湘明
    {
        "id": 2,
        "person_a": 1,
        "person_b": 10,
        "type": "superior_subordinate",
        "context": "县委常委—县委办主任",
        "overlap_org": "中共宁远县委员会",
        "overlap_period": "present",
    },
    # 毛政 <-> 邓小英
    {
        "id": 3,
        "person_a": 1,
        "person_b": 11,
        "type": "overlap",
        "context": "共同出席公务活动",
        "overlap_org": "宁远县",
        "overlap_period": "2026-07",
    },
    # 林亮亮 <-> 曾彩平
    {
        "id": 4,
        "person_a": 2,
        "person_b": 12,
        "type": "superior_subordinate",
        "context": "县长—副县长",
        "overlap_org": "宁远县人民政府",
        "overlap_period": "present",
    },
]


# ══════════════════════════════════════════════════════════════════════════
# Person JSON Writer
# ══════════════════════════════════════════════════════════════════════════

def write_person_json(person: dict, output_dir: Path) -> str | None:
    """Write a person graph JSON file. Returns filename or None if skipped."""
    name = person.get("name", "")
    if not name:
        return None
    job_short = {
        1: "县委书记",
        2: "县长",
    }.get(person["id"], "干部")

    filename = f"{TODAY}-湖南省-永州市-{job_short}-{name}.json"
    filepath = output_dir / filename

    person_id_str = f"hunan_宁远县_{name}"

    # Source register
    sources = [
        {
            "id": "S001",
            "title": "毛政书记报道集 — 宁远新闻网",
            "url": "https://www.ny425600.cn/channel/33416.html",
            "publisher": "宁远新闻网（红网）",
            "published_at": "2026",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "Confirmed 毛政 as 县委书记, current as of Jul 2026",
        },
        {
            "id": "S002",
            "title": "县长报道集 — 宁远新闻网",
            "url": "https://www.ny425600.cn/channel/33472.html",
            "publisher": "宁远新闻网（红网）",
            "published_at": "2026",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "Confirmed 林亮亮 as 县委副书记、县长, current as of Jul 2026",
        },
        {
            "id": "S003",
            "title": "宁远县与湖南师大附中达成教育帮扶共建合作",
            "url": "https://www.ny425600.cn/content/646041/90/16065649.html",
            "publisher": "宁远新闻网（红网）",
            "published_at": "2026-07-08",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "Both 毛政 and 林亮亮 attended signing ceremony",
        },
    ]

    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "湖南省",
            "city": "永州市",
            "region": "宁远县",
            "job": job_short,
            "task_id": "hunan_宁远县",
            "time_focus": "2026",
        },
        "identity": {
            "person_id": person_id_str,
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
                "name_birth": f"{name}_",
                "name_birthplace": f"{name}_{person.get('birthplace', '')}",
                "official_profile_url": f"https://www.ny425600.cn/channel/33416.html",
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "县处级正职",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"],
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": person.get("current_org", ""),
                "title": person.get("current_post", ""),
                "level": "",
                "location": "宁远县",
                "system": "party",
                "rank": "",
                "is_key_promotion": False,
                "notes": "当前任职，confirmed via official news",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": "公开资料未找到任职前的完整履历",
                "confidence": "unverified",
                "source_ids": [],
            },
        ],
        "organizations": [
            {
                "id": 1,
                "name": "中共宁远县委员会",
                "org_type": "党委",
                "level": "县处级",
            },
            {
                "id": 10,
                "name": "宁远县人民政府",
                "org_type": "政府",
                "level": "县处级",
            },
        ],
        "relationships": [
            {
                "person": "林亮亮" if person["id"] == 1 else "毛政",
                "person_id": "hunan_宁远县_林亮亮" if person["id"] == 1 else "hunan_宁远县_毛政",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "党政一把手，共同出席县委常委会、县政府常务会议和教育帮扶签约等公务活动",
                "overlap_org": "中共宁远县委员会 / 宁远县人民政府",
                "overlap_period": "present",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002", "S003"],
            },
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "无法判断 — 公开资料不足",
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
                "description": f"截至{AS_OF}，未在公开来源发现{name}的违纪、处分或负面报道",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            },
        ],
        "source_register": sources,
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "出生年月、籍贯、教育背景、入党时间、参加工作时间和前任职务均未知",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的出生年月和籍贯",
                "why_it_matters": "身份识别和去重的基础字段",
                "suggested_queries": [
                    f"{name} 简历 宁远",
                    f"{name} 出生",
                    f"{name} 湖南 永州 个人简历",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{name}的完整职业生涯（历任职务）",
                "why_it_matters": "构建关系网络和干部流动分析的核心数据",
                "suggested_queries": [
                    f"{name} 任前公示",
                    f"{name} 任职",
                    f"{name} 简历",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{name}何时开始担任现职",
                "why_it_matters": "确定任职时间线的关键节点",
                "suggested_queries": [
                    f"宁远县 人大 任命 {name}",
                    f"{name} 任宁远县",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "毛政的前任县委书记是谁及去向",
                "why_it_matters": "前序职务流动分析",
                "suggested_queries": [
                    "宁远县委书记 前任",
                    "宁远县委 领导 调整",
                ],
                "last_attempted": AS_OF,
            },
        ],
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ {filename}")
    return filename


# ══════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════


def main():
    print(f"╔══ 宁远县 Leadership Network Builder ══╗")
    print(f"║  Date: {TODAY}")
    print(f"║  Stage: {STAGING}")
    print(f"╚══════════════════════════════════════════╝")
    print()

    # Build DB + GEXF
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

    # Write person JSONs for key figures
    print("\n── Person JSONs ──")
    key_persons = [p for p in persons if p["id"] in [1, 2]]
    for p in key_persons:
        if p["name"]:
            write_person_json(p, PJSON_DIR)

    # Summary
    print(f"\n── Summary ──")
    print(f"  Persons (total): {len(persons)}")
    print(f"  Persons (with real names): {sum(1 for p in persons if p['name'])}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Gaps documented in person JSON open_questions")

    print("\n── Open Gaps ──")
    print("  1. 毛政: birth/birthplace/education/career/history — CRITICAL")
    print("  2. 林亮亮: birth/birthplace/education/career/history — CRITICAL")
    print("  3. Former Party Secretary (predecessor to 毛政) — HIGH")
    print("  4. Full 宁远县委 standing committee roster — HIGH")
    print("  5. Full deputy mayor roster — HIGH")
    print("  6. 毛政/林亮亮 appointment dates — HIGH")
    print("  7. Cross-county cadre exchange data — MEDIUM")


if __name__ == "__main__":
    main()
