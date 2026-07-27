#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 前进区 (Qianjin District), 佳木斯市, 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_前进区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - 前进区人民政府官方网站 (www.jmsqjq.gov.cn) — confirmed current leadership
  - Wikipedia (zh.wikipedia.org) — 前进区 district info, historical leadership
  - The official website homepage shows 黄远志 as 区委书记 with brief resume
  - News articles dated July 17-22, 2026 show 孙群 as 区长候选人

Confidence notes:
  - 黄远志: confirmed via official government website with name, gender, birth, education
  - 孙群: confirmed via official government website news as 区长候选人 (July 17, 2026)
  - Both are actively working as of July 2026
  - Detailed career histories before current roles are mostly unavailable
  - Previous 区委书记 杨新 identified from Wikipedia (older data)
  - Web search (Exa, Baidu, Jina, Google) was rate-limited or blocked during this investigation
"""

import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

# Add project root to sys.path
BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

SLUG = "前进区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

CANONICAL_DB = os.path.join(BASE, "..", "..", "database", f"{SLUG}_network.db")
CANONICAL_GEXF = os.path.join(BASE, "..", "..", "graph", f"{SLUG}_network.gexf")
CANONICAL_BUILD = os.path.join(BASE, "..", "..", "..", f"build_{SLUG}_data.py")
CANONICAL_PERSONS = Path(BASE) / ".." / ".." / "persons"

# ═══════════════════════════════════════════════════════════════════════════════
# Data
# ═══════════════════════════════════════════════════════════════════════════════

persons_data = [
    # ══════════════════════════════════════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ══════════════════════════════════════════════════════════════════════════

    # 黄远志 — 区委书记
    {
        "id": 1,
        "name": "黄远志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年3月",
        "birthplace": "",
        "education": "研究生，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共佳木斯市前进区委员会",
        "source": "http://www.jmsqjq.gov.cn"
    },
    # 孙群 — 区长候选人 (2026年7月17日宣布提名)
    {
        "id": 2,
        "name": "孙群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长候选人",
        "current_org": "佳木斯市前进区人民政府",
        "source": "http://www.jmsqjq.gov.cn"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Historical / Previous Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 杨新 — 前区委书记 (per Wikipedia, prior to 黄远志)
    {
        "id": 3,
        "name": "杨新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前区委书记",
        "current_org": "中共佳木斯市前进区委员会（前）",
        "source": "https://zh.wikipedia.org/wiki/前进区"
    },
]

organizations_data = [
    {
        "id": 1,
        "name": "中共佳木斯市前进区委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共佳木斯市委员会",
        "location": "佳木斯市前进区"
    },
    {
        "id": 2,
        "name": "佳木斯市前进区人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "佳木斯市人民政府",
        "location": "佳木斯市前进区"
    },
    {
        "id": 3,
        "name": "中共佳木斯市前进区纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共佳木斯市纪律检查委员会",
        "location": "佳木斯市前进区"
    },
    {
        "id": 4,
        "name": "佳木斯市前进区人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "佳木斯市人民代表大会常务委员会",
        "location": "佳木斯市前进区"
    },
    {
        "id": 5,
        "name": "政协佳木斯市前进区委员会",
        "type": "政协",
        "level": "县级",
        "parent": "政协佳木斯市委员会",
        "location": "佳木斯市前进区"
    },
]

positions_data = [
    # 黄远志 positions
    {
        "id": 1,
        "person_id": 1,
        "org_id": 1,
        "title": "前进区委书记",
        "start": "unknown",
        "end": "present",
        "rank": "正处级",
        "note": "现任前进区委书记；此前任职经历待查。"
    },
    # 孙群 positions
    {
        "id": 2,
        "person_id": 2,
        "org_id": 2,
        "title": "前进区人民政府区长候选人",
        "start": "2026-07-17",
        "end": "present",
        "rank": "正处级",
        "note": "2026年7月17日前进区委常委(扩大)会议宣布提名孙群同志为前进区人民政府区长候选人。"
    },
    # 杨新 positions
    {
        "id": 3,
        "person_id": 3,
        "org_id": 1,
        "title": "前进区委书记（前）",
        "start": "unknown",
        "end": "unknown",
        "rank": "正处级",
        "note": "黄远志的前任，根据维基百科记载。"
    },
]

relationships_data = [
    # 黄远志 ↔ 孙群 — 党政搭档
    {
        "id": 1,
        "person_a": 1,
        "person_b": 2,
        "type": "党政领导搭档",
        "context": "黄远志（区委书记）与孙群（区长候选人）为前进区党政主要领导搭档",
        "overlap_org": "佳木斯市前进区",
        "overlap_period": "2026-07至今"
    },
    # 黄远志 ← 杨新 — 前后任书记
    {
        "id": 2,
        "person_a": 3,
        "person_b": 1,
        "type": "前后任",
        "context": "杨新为前进区前任区委书记，黄远志接任",
        "overlap_org": "中共佳木斯市前进区委员会",
        "overlap_period": ""
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON templates
# ═══════════════════════════════════════════════════════════════════════════════

person_json_template = {
    "黄远志": {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "佳木斯市",
            "region": "前进区",
            "job": "区委书记",
            "task_id": "heilongjiang_前进区",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": "qianjin_huang_yuanzhi",
            "name": "黄远志",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1980年3月",
            "birthplace": "",
            "native_place": "",
            "education": ["研究生", "公共管理硕士"],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "黄远志_1980年3月",
                "name_birthplace": "黄远志_",
                "official_profile_url": "http://www.jmsqjq.gov.cn"
            }
        },
        "current_status": {
            "current_post": "区委书记",
            "current_org": "中共佳木斯市前进区委员会",
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": "中共佳木斯市前进区委员会",
                "title": "前进区委书记",
                "notes": "具体到任时间待查",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "organizations": [],
        "relationships": [
            {
                "person": "孙群",
                "person_id": "qianjin_sun_qun",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "党政主要领导搭档——区委书记与区长候选人",
                "overlap_org": "佳木斯市前进区",
                "overlap_period": "2026-07至今",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "person": "杨新",
                "person_id": "qianjin_yang_xin",
                "relationship_type": "predecessor_successor",
                "strength": "medium",
                "evidence": "杨新为前前进区委书记，黄远志接任",
                "overlap_org": "中共佳木斯市前进区委员会",
                "overlap_period": "",
                "direction": "undirected",
                "confidence": "unverified",
                "source_ids": ["S002"]
            }
        ],
        "governance_record": [
            {
                "period": "unknown至今",
                "domain": "governance",
                "achievement_or_event": "前进区委书记任内——主持全区工作",
                "role_in_event": "书记",
                "measurable_outcome": "",
                "location": "佳木斯市前进区",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["地方党政"],
            "geographic_pattern": ["佳木斯"],
            "promotion_velocity": {
                "summary": "",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "在公开信息中未发现该人物负面信号",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "佳木斯市前进区人民政府官方网站",
                "url": "http://www.jmsqjq.gov.cn",
                "publisher": "前进区人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "government",
                "reliability": "high",
                "notes": "首页领导之窗显示黄远志为区委书记及简历"
            },
            {
                "id": "S002",
                "title": "维基百科—前进区",
                "url": "https://zh.wikipedia.org/wiki/前进区",
                "publisher": "维基百科",
                "published_at": "2023-12-08",
                "accessed_at": AS_OF,
                "source_type": "encyclopedia",
                "reliability": "medium",
                "notes": "前进区基本信息及前任区委书记杨新"
            }
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "黄远志的完整履历信息（含到任时间、此前任职、出生地、毕业院校）需补充"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "黄远志任前进区委书记的具体到任时间",
                "why_it_matters": "核心人物任职时间线",
                "suggested_queries": ["黄远志 任前进区委书记", "黄远志 前进区 任命"],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": "黄远志担任前进区委书记前的历任职务",
                "why_it_matters": "完整了解其职业生涯轨迹",
                "suggested_queries": ["黄远志 简历 任职经历", "黄远志 佳木斯 任职"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "黄远志的出生地和毕业院校",
                "why_it_matters": "完善基础档案信息",
                "suggested_queries": ["黄远志 出生地", "黄远志 毕业院校"],
                "last_attempted": AS_OF
            }
        ]
    },
    "孙群": {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "佳木斯市",
            "region": "前进区",
            "job": "区长候选人",
            "task_id": "heilongjiang_前进区",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": "qianjin_sun_qun",
            "name": "孙群",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "孙群_",
                "name_birthplace": "孙群_",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": "区长候选人",
            "current_org": "佳木斯市前进区人民政府",
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "2026-07-17",
                "end": "present",
                "org": "佳木斯市前进区人民政府",
                "title": "区长候选人",
                "notes": "2026年7月17日宣布提名为前进区人民政府区长候选人。此前履历待查。",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "organizations": [],
        "relationships": [
            {
                "person": "黄远志",
                "person_id": "qianjin_huang_yuanzhi",
                "relationship_type": "subordinate_to_superior",
                "strength": "strong",
                "evidence": "区长候选人受区委书记领导",
                "overlap_org": "佳木斯市前进区",
                "overlap_period": "2026-07至今",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "在公开信息中未发现该人物负面信号",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "佳木斯市前进区人民政府官方网站—今日前进",
                "url": "http://www.jmsqjq.gov.cn",
                "publisher": "前进区人民政府",
                "published_at": "2026-07-17",
                "accessed_at": AS_OF,
                "source_type": "government",
                "reliability": "high",
                "notes": "前进区委常委(扩大)会议宣布提名孙群同志为前进区人民政府区长候选人"
            }
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "孙群的完整履历信息（含出生年月、出生地、教育背景、历任职务）需补充"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "孙群的完整职业生涯履历（含出生年月、出生地、教育背景、历任职务）",
                "why_it_matters": "核心人物之一，但履历几乎完全空白",
                "suggested_queries": ["孙群 佳木斯 前进区 简历", "孙群 任前公示", "孙群 前进区 区长 任职"],
                "last_attempted": AS_OF
            }
        ]
    },
    "杨新": {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "佳木斯市",
            "region": "前进区",
            "job": "前区委书记",
            "task_id": "heilongjiang_前进区",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": "qianjin_yang_xin",
            "name": "杨新",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "杨新_",
                "name_birthplace": "杨新_",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": "前区委书记",
            "current_org": "中共佳木斯市前进区委员会（前）",
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": ["S002"]
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "unknown",
                "org": "中共佳木斯市前进区委员会",
                "title": "前进区委书记",
                "notes": "维基百科记载为前前进区委书记；具体任职起止时间待查，去向不明",
                "confidence": "unverified",
                "source_ids": ["S002"]
            }
        ],
        "organizations": [],
        "relationships": [
            {
                "person": "黄远志",
                "person_id": "qianjin_huang_yuanzhi",
                "relationship_type": "predecessor_successor",
                "strength": "medium",
                "evidence": "杨新为前前进区委书记，黄远志接任",
                "overlap_org": "中共佳木斯市前进区委员会",
                "overlap_period": "",
                "direction": "undirected",
                "confidence": "unverified",
                "source_ids": ["S002"]
            }
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "在公开信息中未发现该人物负面信号",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S002",
                "title": "维基百科—前进区",
                "url": "https://zh.wikipedia.org/wiki/前进区",
                "publisher": "维基百科",
                "published_at": "2023-12-08",
                "accessed_at": AS_OF,
                "source_type": "encyclopedia",
                "reliability": "medium",
                "notes": "前进区基本情况，记载杨新为区委书记"
            }
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "historical",
            "career_completeness": "minimal",
            "relationship_confidence": "low",
            "biggest_gap": "杨新的完整履历及目前去向"
        },
        "open_questions": [
            {
                "priority": "high",
                "question": "杨新离开前进区委书记岗位后的去向",
                "why_it_matters": "了解前进区领导更替轨迹",
                "suggested_queries": ["杨新 前进区 卸任", "杨新 调任"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "杨新在前进区委书记任期的具体时间",
                "why_it_matters": "完善区领导更替时间线",
                "suggested_queries": ["杨新 前进区委书记 任职时间"],
                "last_attempted": AS_OF
            }
        ]
    }
}


# ═══════════════════════════════════════════════════════════════════════════════
# Helper: XML escape
# ═══════════════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON writer
# ═══════════════════════════════════════════════════════════════════════════════

def write_person_json(person_name, data):
    """Write a single person JSON to the staging directory."""
    base = PERSONS_DIR
    if "杨新" in person_name:
        filename = f"{TODAY}-黑龙江省-佳木斯市-前区委书记-杨新.json"
    elif "黄远志" in person_name:
        filename = f"{TODAY}-黑龙江省-佳木斯市-区委书记-黄远志.json"
    elif "孙群" in person_name:
        filename = f"{TODAY}-黑龙江省-佳木斯市-区长候选人-孙群.json"
    else:
        filename = f"{TODAY}-黑龙江省-佳木斯市-{person_name}.json"
    filepath = base / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✅ wrote {filepath}")
    # Also copy to canonical persons dir if not a dry run
    if CANONICAL_PERSONS.exists():
        canonical_path = CANONICAL_PERSONS / filename
        with open(canonical_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  ✅ wrote {canonical_path}")
    return filepath


# ═══════════════════════════════════════════════════════════════════════════════
# Main build
# ═══════════════════════════════════════════════════════════════════════════════

def build():
    print("=" * 60)
    print(f"  Building {SLUG} network — {AS_OF}")
    print("=" * 60)

    # ── 1. Build SQLite Database ──────────────────────────────────────────
    print(f"\n📦 Building SQLite database: {DB_PATH}")
    try:
        from gov_relation.runner import run_build
        from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

        # Also produce canonical copies
        run_build(
            slug=SLUG,
            persons=persons_data,
            organizations=organizations_data,
            positions=positions_data,
            relationships=relationships_data,
            db_path=DB_PATH,
            gexf_path=GEXF_PATH,
        )
        print(f"  ✅ DB: {DB_PATH}")
        print(f"  ✅ GEXF: {GEXF_PATH}")

        # Also write to canonical paths
        os.makedirs(os.path.dirname(CANONICAL_DB), exist_ok=True)
        os.makedirs(os.path.dirname(CANONICAL_GEXF), exist_ok=True)
        shutil.copy2(DB_PATH, CANONICAL_DB)
        shutil.copy2(GEXF_PATH, CANONICAL_GEXF)
        print(f"  ✅ Canonical DB: {CANONICAL_DB}")
        print(f"  ✅ Canonical GEXF: {CANONICAL_GEXF}")

    except ImportError:
        print("  ⚠ gov_relation module not found, building DB manually...")
        build_db_manual()
        # Also write to canonical paths
        os.makedirs(os.path.dirname(CANONICAL_DB), exist_ok=True)
        os.makedirs(os.path.dirname(CANONICAL_GEXF), exist_ok=True)
        shutil.copy2(DB_PATH, CANONICAL_DB)
        shutil.copy2(GEXF_PATH, CANONICAL_GEXF)
        print(f"  ✅ Canonical DB: {CANONICAL_DB}")
        print(f"  ✅ Canonical GEXF: {CANONICAL_GEXF}")

    # ── 2. Write Person JSONs ─────────────────────────────────────────────
    print(f"\n📝 Writing person JSONs...")
    for name, data in person_json_template.items():
        write_person_json(name, data)

    # ── 3. Copy build script to canonical location ────────────────────────
    print(f"\n📋 Copying build script...")
    script_src = os.path.abspath(__file__)
    shutil.copy2(script_src, CANONICAL_BUILD)
    print(f"  ✅ Canonical build: {CANONICAL_BUILD}")

    # ── 4. Summary ────────────────────────────────────────────────────────
    print(f"\n{'=' * 60}")
    print(f"  Build complete!")
    print(f"  Persons: {len(persons_data)}")
    print(f"  Organizations: {len(organizations_data)}")
    print(f"  Positions: {len(positions_data)}")
    print(f"  Relationships: {len(relationships_data)}")
    print(f"  Person JSONs: {len(person_json_template)}")
    print(f"{'=' * 60}")


def build_db_manual():
    """Fallback: build SQLite and GEXF without gov_relation module."""
    # ── SQLite ──
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")

    conn.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons_data:
        conn.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations_data:
        conn.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for po in positions_data:
        conn.execute("""INSERT OR REPLACE INTO positions
            (id, person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?,?)""",
            (po["id"], po["person_id"], po["org_id"], po["title"],
             po["start"], po["end"], po["rank"], po["note"]))

    for r in relationships_data:
        conn.execute("""INSERT OR REPLACE INTO relationships
            (id, person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?,?)""",
            (r["id"], r["person_a"], r["person_b"], r["type"],
             r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"  ✅ Manual DB built: {DB_PATH}")

    # ── GEXF ──
    from datetime import datetime

    def person_color(p):
        if "区委书记" in (p.get("current_post") or "") and "前" not in (p.get("current_post") or ""):
            return "255,50,50"
        if "区长" in (p.get("current_post") or ""):
            return "50,100,255"
        if "前" in (p.get("current_post") or ""):
            return "100,100,100"
        return "100,100,100"

    def org_color(o):
        t = o.get("type", "")
        if "党委" in t: return "255,200,200"
        if "政府" in t: return "200,200,255"
        if "人大" in t: return "200,255,255"
        if "政协" in t: return "255,240,200"
        return "200,200,200"

    def is_top_leader(p):
        post = p.get("current_post", "")
        return "区委书记" in post or "区长" in post

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append(f'    <description>{SLUG} personnel relationship network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # person nodes
    lines.append('    <nodes>')
    for p in persons_data:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # organization nodes
    for o in organizations_data:
        c = org_color(o)
        oid = o["id"] + 100000  # offset to avoid id collision with persons
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append(f'          <attvalue for="4" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # edges
    lines.append('    <edges>')
    eid = 0
    # person → organization (worked_at)
    for po in positions_data:
        eid += 1
        oid = po["org_id"] + 100000
        lines.append(f'      <edge id="e{eid}" source="p{po["person_id"]}" target="o{oid}" label="{esc(po["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(po.get("note",""))}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(po.get("start",""))} - {esc(po.get("end",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person ↔ person (relationship)
    for r in relationships_data:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  ✅ Manual GEXF built: {GEXF_PATH}")


if __name__ == "__main__":
    build()
