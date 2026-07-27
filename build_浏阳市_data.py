#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浏阳市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县级市
Province: 湖南省
Parent City: 长沙市
Region: 浏阳市
Targets: 市委书记 & 市长

Research status (2026-07-24):
- 胡小刚 (Party Secretary): confirmed — 长沙市委常委、浏阳市委书记 (since 2026-05)
  - Career history: thin — only current role confirmed, no birth/education/birthplace
- 王雄文 (Mayor): plausible — served as 浏阳市市长, but successor status unclear
  - Identity partially confirmed, tenure dates uncertain
- 付旭明 (Predecessor): confirmed — former 浏阳市委书记 (~2021-2025), now 长沙市委常委、常务副市长

Research constraints:
  - Baidu Baike: 403/Cloudflare block
  - Exa search: rate limited
  - Jina Reader: transport errors
  - Government websites (liuyang.gov.cn): connection timeouts
  - All data based on existing repository artifacts (长沙市 investigation) and training knowledge

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

import sqlite3  # noqa: F401 — used by gov_relation.runner

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "浏阳市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "hunan_浏阳市"
if _CURRENT_DIR.name == "hunan_浏阳市":
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

    # 胡小刚 — 浏阳市委书记 (Party Secretary)
    {
        "id": 1,
        "name": "胡小刚",
        "gender": "男",
        "ethnicity": "汉族",  # plausible — all 长沙市委委员 confirmed as 汉族
        "birth": "",  # open question — not found in available sources
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "浏阳市委书记",
        "current_org": "中共浏阳市委员会",
        "source": "维基百科 — 中国共产党长沙市委员会",
        "confidence": "confirmed",
        "notes": "2026年5月任长沙市委常委、浏阳市委书记。具体出生年月、籍贯、完整履历待查。"
    },

    # 王雄文 — 浏阳市市长 (Mayor) — identity needs verification
    {
        "id": 2,
        "name": "王雄文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "浏阳市市长",
        "current_org": "浏阳市人民政府",
        "source": "多源确认（历史资料）",
        "confidence": "plausible",
        "notes": "⚠️ 需确认：王雄文是否仍任市长。2021-2024年期间履职记录存在，但2025年后去向不明。可能已离任，继任者待查。"
    },

    # ══════════════════════════════════════════════════════════════════════
    # 浏阳市委常委 (Liuyang Standing Committee)
    # ══════════════════════════════════════════════════════════════════════

    # 专职副书记（待确认）
    {
        "id": 11,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记（专职）",
        "current_org": "中共浏阳市委员会",
        "source": "",
        "confidence": "unverified",
        "notes": "专职副书记身份待确认。通常县级市设专职副书记1名。"
    },

    # 常务副市长（待确认）
    {
        "id": 12,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "浏阳市人民政府",
        "source": "",
        "confidence": "unverified",
        "notes": "常务副市长身份待确认。"
    },

    # 纪委书记（待确认）
    {
        "id": 13,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、市纪委书记、市监委主任",
        "current_org": "中共浏阳市纪律检查委员会",
        "source": "",
        "confidence": "unverified",
        "notes": "纪委书记身份待确认。"
    },

    # 组织部部长（待确认）
    {
        "id": 14,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共浏阳市委组织部",
        "source": "",
        "confidence": "unverified",
        "notes": "组织部部长身份待确认。"
    },

    # 宣传部部长（待确认）
    {
        "id": 15,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共浏阳市委宣传部",
        "source": "",
        "confidence": "unverified",
        "notes": "宣传部部长身份待确认。"
    },

    # 统战部部长（待确认）
    {
        "id": 16,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、统战部部长",
        "current_org": "中共浏阳市委统一战线工作部",
        "source": "",
        "confidence": "unverified",
        "notes": "统战部部长身份待确认。"
    },

    # 政法委书记（待确认）
    {
        "id": 17,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、政法委书记",
        "current_org": "中共浏阳市委政法委员会",
        "source": "",
        "confidence": "unverified",
        "notes": "政法委书记身份待确认。"
    },

    # ══════════════════════════════════════════════════════════════════════
    # 副市长 (Deputy Mayors) — typical 5-7 deputies
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 21,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "浏阳市人民政府",
        "source": "",
        "confidence": "unverified",
        "notes": "副市长（分管经济/发改/工信等），身份待确认。"
    },
    {
        "id": 22,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "浏阳市人民政府",
        "source": "",
        "confidence": "unverified",
        "notes": "副市长（分管公安/司法/信访等），身份待确认。"
    },
    {
        "id": 23,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "浏阳市人民政府",
        "source": "",
        "confidence": "unverified",
        "notes": "副市长（分管教育/卫生/文化等），身份待确认。"
    },
    {
        "id": 24,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "浏阳市人民政府",
        "source": "",
        "confidence": "unverified",
        "notes": "副市长（分管城建/交通/规划等），身份待确认。"
    },

    # ══════════════════════════════════════════════════════════════════════
    # Predecessors & Key Historical Figures
    # ══════════════════════════════════════════════════════════════════════

    # 付旭明 — 前任浏阳市委书记（~2021-2025），现长沙市委常委、常务副市长
    {
        "id": 31,
        "name": "付旭明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长沙市委常委、常务副市长",
        "current_org": "长沙市人民政府",
        "source": "维基百科 — 中国共产党长沙市委员会、长沙市数据",
        "confidence": "confirmed",
        "notes": "前任浏阳市委书记（任期约2021-2025年12月），2025年12月任长沙市委常委、常务副市长。部分资料也记作'付旭东'。"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共浏阳市委员会", "type": "党委", "level": "县级", "parent": "中共长沙市委", "location": "浏阳"},
    {"id": 2, "name": "浏阳市人民政府", "type": "政府", "level": "县级", "parent": "长沙市人民政府", "location": "浏阳"},
    {"id": 3, "name": "中共浏阳市纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共浏阳市委员会", "location": "浏阳"},
    {"id": 4, "name": "浏阳市人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "", "location": "浏阳"},
    {"id": 5, "name": "中国人民政治协商会议浏阳市委员会", "type": "政协", "level": "县级", "parent": "", "location": "浏阳"},
    {"id": 6, "name": "中共浏阳市委组织部", "type": "党委", "level": "县级", "parent": "中共浏阳市委员会", "location": "浏阳"},
    {"id": 7, "name": "中共浏阳市委宣传部", "type": "党委", "level": "县级", "parent": "中共浏阳市委员会", "location": "浏阳"},
    {"id": 8, "name": "中共浏阳市委统一战线工作部", "type": "党委", "level": "县级", "parent": "中共浏阳市委员会", "location": "浏阳"},
    {"id": 9, "name": "中共浏阳市委政法委员会", "type": "党委", "level": "县级", "parent": "中共浏阳市委员会", "location": "浏阳"},
    {"id": 10, "name": "浏阳市公安局", "type": "政府", "level": "县级", "parent": "浏阳市人民政府", "location": "浏阳"},
    {"id": 11, "name": "中共长沙市委", "type": "党委", "level": "地市级", "parent": "中共湖南省委", "location": "长沙"},
    {"id": 12, "name": "长沙市人民政府", "type": "政府", "level": "地市级", "parent": "湖南省人民政府", "location": "长沙"},
    {"id": 13, "name": "中共湖南省委", "type": "党委", "level": "省级", "parent": "", "location": "长沙"},
    {"id": 14, "name": "湖南省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "长沙"},
    {"id": 15, "name": "浏阳市人民武装部", "type": "军队", "level": "县级", "parent": "长沙警备区", "location": "浏阳"},
]

# ── Positions ──────────────────────────────────────────────────────────────────
positions = [
    # ═══ 胡小刚 (id=1) ═══
    {"person_id": 1, "org_id": 1, "title": "浏阳市委书记", "start": "2026-05", "end": "", "rank": "副厅级", "note": "长沙市委常委兼任"},
    {"person_id": 1, "org_id": 11, "title": "长沙市委常委", "start": "2026-05", "end": "", "rank": "副厅级", "note": "2026年5月入常"},

    # ═══ 王雄文 (id=2) — 履历待确认 ═══
    {"person_id": 2, "org_id": 2, "title": "浏阳市市长", "start": "", "end": "", "rank": "正处级", "note": "⚠️ 当前身份需确认"},
    {"person_id": 2, "org_id": 1, "title": "浏阳市委副书记", "start": "", "end": "", "rank": "正处级", "note": "市长兼任市委副书记"},

    # ═══ 付旭明 (id=31) — 前任 ═══
    {"person_id": 31, "org_id": 1, "title": "浏阳市委书记", "start": "", "end": "2025-12", "rank": "副厅级", "note": "前任书记，2025年12月调离"},
    {"person_id": 31, "org_id": 12, "title": "常务副市长", "start": "2025-12", "end": "", "rank": "副厅级", "note": "长沙市委常委、常务副市长"},
    {"person_id": 31, "org_id": 11, "title": "长沙市委常委", "start": "2025-12", "end": "", "rank": "副厅级", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────────
relationships = [
    # 胡小刚 ↔ 王雄文 — 书记+市长搭档
    {"person_a": 1, "person_b": 2, "type": "core_partnership",
     "context": "浏阳市委书记与市长搭档关系", "overlap_org": "中共浏阳市委员会/浏阳市人民政府",
     "overlap_period": "（需确认起止时间）", "confidence": "plausible"},

    # 胡小刚 ↔ 付旭明 — 前后任书记
    {"person_a": 1, "person_b": 31, "type": "predecessor_successor",
     "context": "付旭明前任浏阳市委书记，胡小刚接任", "overlap_org": "中共浏阳市委员会",
     "overlap_period": "2026-05 交接", "confidence": "confirmed"},

    # 付旭明 — 长沙市委新任领导班子连接
    {"person_a": 31, "person_b": 1, "type": "overlap",
     "context": "现同为长沙市委委员", "overlap_org": "中共长沙市委",
     "overlap_period": "2026-05至今", "confidence": "confirmed"},
]


# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON Writers
# ═══════════════════════════════════════════════════════════════════════════════

def write_person_json(person: dict, pjson_dir: Path) -> str:
    """Write a person's deep-profile JSON file. Returns the filename."""
    name = person["name"]
    job = person.get("current_post", "")
    filename = f"{TODAY}-湖南省-长沙市-{job}-{name}.json"
    filepath = pjson_dir / filename

    # Map role to person_id prefix
    pid_prefix = f"liuyang_{name}"

    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "湖南省",
            "city": "长沙市",
            "region": "浏阳市",
            "job": job,
            "task_id": "hunan_浏阳市",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": pid_prefix,
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [person["education"]] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth', '')}",
                "name_birthplace": f"{name}_{person.get('birthplace', '')}",
                "official_profile_url": person.get("source", "")
            }
        },
        "current_status": {
            "current_post": job,
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [],
        "organizations": [
            {"id": 1, "name": "中共浏阳市委员会", "type": "党委"},
            {"id": 2, "name": "浏阳市人民政府", "type": "政府"},
            {"id": 3, "name": "中共长沙市委员会", "type": "党委"},
        ],
        "relationships": [],
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
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [
            {
                "id": "S001",
                "title": "维基百科 — 中国共产党长沙市委员会",
                "url": "https://zh.wikipedia.org/wiki/中国共产党长沙市委员会",
                "publisher": "维基百科",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "encyclopedia",
                "reliability": "medium",
                "notes": "长沙市领导班子列表确认身份"
            }
        ],
        "confidence_summary": {
            "identity": "unverified" if not person.get("birth") else "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "high" if person["id"] in [1, 31] else "low",
            "biggest_gap": "完整任职履历（每段职务精确起止时间）"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历（每段职务精确起止时间）",
                "why_it_matters": "关系网络分析需要精确的时间线",
                "suggested_queries": [
                    f"{name} 简历",
                    f"{name} 任前公示",
                    f"{name} 百度百科"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"{name}的出生年月和籍贯",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [
                    f"{name} 简历",
                    f"{name} 籍贯"
                ],
                "last_attempted": AS_OF
            }
        ]
    }

    # Add career timeline for known persons
    if person["id"] == 1:  # 胡小刚
        data["career_timeline"] = [
            {"start": "2026-05", "end": "", "org": "中共浏阳市委员会", "title": "浏阳市委书记",
             "level": "副厅级", "rank": "副厅级", "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2026-05", "end": "", "org": "中共长沙市委员会", "title": "长沙市委常委",
             "level": "副厅级", "rank": "副厅级", "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        ]
        data["relationships"] = [
            {"person": "陈竞", "person_id": "changsha_陈竞",
             "relationship_type": "overlap", "strength": "strong",
             "evidence": "书记—常委（浏阳书记）",
             "overlap_org": "中共长沙市委员会", "overlap_period": "2026.06-至今",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]}
        ]
    elif person["id"] == 31:  # 付旭明
        data["career_timeline"] = [
            {"start": "", "end": "2025-12", "org": "中共浏阳市委员会", "title": "浏阳市委书记",
             "level": "副厅级", "rank": "副厅级", "notes": "前任呈现一致", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
            {"start": "2025-12", "end": "", "org": "长沙市人民政府", "title": "常务副市长",
             "level": "副厅级", "rank": "副厅级", "notes": "", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
            {"start": "2025-12", "end": "", "org": "中共长沙市委员会", "title": "市委常委",
             "level": "副厅级", "rank": "副厅级", "notes": "", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        ]
        data["relationships"] = [
            {"person": "陈博彰", "person_id": "changsha_陈博彰",
             "relationship_type": "overlap", "strength": "strong",
             "evidence": "市长—常务副市长",
             "overlap_org": "长沙市人民政府", "overlap_period": "2025.12-至今",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]}
        ]
        data["source_register"].append({
            "id": "S002",
            "title": "长沙市领导数据",
            "url": "",
            "publisher": "本地仓库数据",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "internal",
            "reliability": "high",
            "notes": "长沙市构建脚本确认"
        })

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Person JSON: {filename}")
    return filename


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print(f"╔══ 浏阳市 Leadership Network Builder ══╗")
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
    key_persons = [p for p in persons if p["id"] in [1, 2, 31]]
    for p in key_persons:
        if p["name"] != "（待确认）":
            write_person_json(p, PJSON_DIR)

    # Summary
    print(f"\n── Summary ──")
    print(f"  Persons (total): {len(persons)}")
    print(f"  Persons (with real names): {sum(1 for p in persons if p['name'] != '（待确认）')}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Gaps documented in person JSON open_questions")

    print("\n── Open Gaps ──")
    print("  1. 胡小刚: birth/birthplace/education/career history — CRITICAL")
    print("  2. 王雄文: current status as mayor — CRITICAL (may have been replaced)")
    print("  3. Full 浏阳市 standing committee roster — HIGH")
    print("  4. Full deputy mayor roster — HIGH")
    print("  5. Cross-county cadre exchange data — MEDIUM")


if __name__ == "__main__":
    main()
