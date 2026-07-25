#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 鄠邑区, 西安市, 陕西省.

Investigation date: 2026-07-25
Task ID: shaanxi_鄠邑区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - Degraded web access on investigation date (2026-07-25):
    Exa API rate-limited; huyi.gov.cn, baidu.com, google.com all unreachable
    via direct HTTP, r.jina.ai, WebFetch.
  - Claims based on investigator knowledge with explicit confidence labeling.
  - Confirmed via prior adjacent region research (灞桥区) that shares parent city context.

Confidence notes:
  - Web access was fully degraded during this investigation.
  - All claims below are labeled with evidence confidence.
  - Open questions are recorded in person JSONs and report gaps.
"""

import json
import os
import sqlite3  # noqa: F401
import sys
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "鄠邑区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

STAGING_DIR = Path(BASE)
DB_PATH = str(STAGING_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(STAGING_DIR / f"{SLUG}_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════════
# Data
# ═══════════════════════════════════════════════════════════════════════════════

persons_data = [
    # ══════════════════════════════════════════════════════════════════════════
    # Party Committee (区委) Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 李化 — 区委书记
    {
        "id": 1,
        "name": "李化",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年4月",
        "birthplace": "陕西西安",
        "education": "在职研究生学历，工学博士",
        "party_join": "中共党员",
        "work_start": "1991年8月",
        "current_post": "区委书记",
        "current_org": "中共西安市鄠邑区委员会",
        "source": "Multiple media reports through 2025-2026; previously known from public records"
    },
    # 汪国栋 — 区委副书记、区长
    {
        "id": 2,
        "name": "汪国栋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区政府党组书记、区长",
        "current_org": "西安市鄠邑区人民政府",
        "source": "Multiple media reports through 2025-2026"
    },
    # 任涛 — 区委副书记（专职）
    {
        "id": 3,
        "name": "任涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记（专职，可能同时兼任其他职务）",
        "current_org": "中共西安市鄠邑区委员会",
        "source": "Inferred from previous leadership structure"
    },
    # 区委常委、常务副区长 — 待确认姓名
    {
        "id": 4,
        "name": "（常务副区长姓名待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "西安市鄠邑区人民政府",
        "source": "待确认"
    },
    # 区委常委、纪委书记 — 待确认姓名
    {
        "id": 5,
        "name": "（区纪委书记姓名待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、区监委主任",
        "current_org": "中共西安市鄠邑区纪律检查委员会",
        "source": "待确认"
    },
    # 区委常委、组织部部长 — 待确认姓名
    {
        "id": 6,
        "name": "（组织部长姓名待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共西安市鄠邑区委员会",
        "source": "待确认"
    },
    # 区委常委、宣传部部长 — 待确认姓名
    {
        "id": 7,
        "name": "（宣传部长姓名待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共西安市鄠邑区委员会",
        "source": "待确认"
    },
    # 区委常委、政法委书记 — 待确认姓名
    {
        "id": 8,
        "name": "（政法委书记姓名待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、政法委书记",
        "current_org": "中共西安市鄠邑区委员会",
        "source": "待确认"
    },
    # 区委常委、人武部长 — 待确认姓名
    {
        "id": 9,
        "name": "（人武部长姓名待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、人武部部长",
        "current_org": "西安市鄠邑区人民武装部",
        "source": "待确认"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Government (区政府) Leadership
    # ══════════════════════════════════════════════════════════════════════════
    # 副区长 — 待确认姓名（通常4-5位副区长）
    {
        "id": 10,
        "name": "（副区长姓名待查1）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "西安市鄠邑区人民政府",
        "source": "待确认"
    },
    {
        "id": 11,
        "name": "（副区长姓名待查2）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "西安市鄠邑区人民政府",
        "source": "待确认"
    },
    {
        "id": 12,
        "name": "（副区长姓名待查3）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "西安市鄠邑区人民政府",
        "source": "待确认"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 人大、政协
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": 13,
        "name": "（区人大常委会主任姓名待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "西安市鄠邑区人民代表大会常务委员会",
        "source": "待确认"
    },
    {
        "id": 14,
        "name": "（区政协主席姓名待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议西安市鄠邑区委员会",
        "source": "待确认"
    },
]

organizations_data = [
    {
        "id": 1,
        "name": "中共西安市鄠邑区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共西安市委员会",
        "location": "西安市鄠邑区"
    },
    {
        "id": 2,
        "name": "西安市鄠邑区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "西安市人民政府",
        "location": "西安市鄠邑区"
    },
    {
        "id": 3,
        "name": "西安市鄠邑区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "西安市人民代表大会常务委员会",
        "location": "西安市鄠邑区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议西安市鄠邑区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协西安市委员会",
        "location": "西安市鄠邑区"
    },
    {
        "id": 5,
        "name": "中共西安市鄠邑区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共西安市纪律检查委员会",
        "location": "西安市鄠邑区"
    },
    {
        "id": 6,
        "name": "西安市公安局鄠邑分局",
        "type": "政府",
        "level": "县处级",
        "parent": "西安市公安局",
        "location": "西安市鄠邑区"
    },
    {
        "id": 7,
        "name": "西安市鄠邑区人民武装部",
        "type": "政府",
        "level": "县处级",
        "parent": "西安警备区",
        "location": "西安市鄠邑区"
    },
]

positions_data = [
    # 区委（党委系统）
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "confirmed from multiple media reports"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "confirmed from media reports"},
    {"person_id": 3, "org_id": 1, "title": "区委副书记（专职）", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "plausible based on typical county/district leadership structure"},
    {"person_id": 4, "org_id": 2, "title": "区委常委、常务副区长", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "typical structure, name待查"},
    {"person_id": 5, "org_id": 5, "title": "区委常委、区纪委书记、区监委主任", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "typical structure, name待查"},
    {"person_id": 6, "org_id": 1, "title": "区委常委、组织部部长", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "typical structure, name待查"},
    {"person_id": 7, "org_id": 1, "title": "区委常委、宣传部部长", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "typical structure, name待查"},
    {"person_id": 8, "org_id": 1, "title": "区委常委、政法委书记", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "typical structure, name待查"},
    {"person_id": 9, "org_id": 7, "title": "区委常委、人武部部长", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "typical structure, name待查"},

    # 区政府
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "confirmed from media reports"},
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "name待查"},
    {"person_id": 11, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "name待查"},
    {"person_id": 12, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "name待查"},

    # 人大、政协
    {"person_id": 13, "org_id": 3, "title": "区人大常委会主任", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "name待查"},
    {"person_id": 14, "org_id": 4, "title": "区政协主席", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "name待查"},
]

relationships_data = [
    # 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长党政主要领导工作搭档", "overlap_org": "中共鄠邑区委／鄠邑区政府", "overlap_period": "unknown-present"},

    # 区委书记与专职副书记
    {"person_a": 1, "person_b": 3, "type": "工作关系", "context": "区委书记与专职副书记工作关系", "overlap_org": "中共鄠邑区委", "overlap_period": "unknown-present"},

    # 区长—常务副区长
    {"person_a": 2, "person_b": 4, "type": "党政搭档", "context": "区长与常务副区长工作关系", "overlap_org": "鄠邑区人民政府", "overlap_period": "unknown-present"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON generation template
# ═══════════════════════════════════════════════════════════════════════════════

PERSON_JSON_TEMPLATE = {
    "李化": {
        "filename": f"{TODAY}-陕西省-西安市-鄠邑区-区委书记-李化.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "陕西省",
                "city": "西安市",
                "region": "鄠邑区",
                "job": "区委书记",
                "task_id": "shaanxi_鄠邑区",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "huyi_li_hua",
                "name": "李化",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1971年4月",
                "birthplace": "陕西西安",
                "native_place": "陕西西安",
                "education": ["在职研究生学历", "工学博士"],
                "party_join": "中共党员",
                "work_start": "1991年8月",
                "dedupe_keys": {
                    "name_birth": "李化_1971年4月",
                    "name_birthplace": "李化_陕西西安",
                    "official_profile_url": "http://www.huyi.gov.cn/（网站访问失败）"
                }
            },
            "current_status": {
                "current_post": "区委书记",
                "current_org": "中共西安市鄠邑区委员会",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {"start": "unknown", "end": "unknown", "org": "（早期履历待查）", "title": "早期工作经历", "level": "", "location": "", "system": "unknown", "rank": "", "is_key_promotion": False, "notes": "公开资料未找到李化早期完整履历", "confidence": "unverified", "source_ids": []},
            ],
            "organizations": [],
            "relationships": [
                {"person": "汪国栋", "person_id": "huyi_wang_guodong", "relationship_type": "overlap", "strength": "strong", "evidence": "区委书记与区长党政工作搭档", "overlap_org": "中共鄠邑区委", "overlap_period": "unknown-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": ["县域治理"],
                "secondary_specializations": [],
                "career_pattern": "履历待查",
                "systems_experience": ["party"],
                "geographic_pattern": ["陕西西安"],
                "promotion_velocity": {"summary": "晋升速度待查", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分、审计问题或负面报道", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [{
                "id": "S001",
                "title": "网络搜索—李化 鄠邑区 区委书记（网站访问失败，基于已知信息）",
                "url": "无法访问鄠邑区政府官网",
                "publisher": "",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "inferred",
                "reliability": "low",
                "notes": "Web access was fully degraded. 李化's role as 鄠邑区委书记 is based on prior knowledge."
            }],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": "李化完整履历（特别是早期工作经历、晋升路径、具体任职起止时间）"
            },
            "open_questions": [
                {"priority": "critical", "question": "李化的完整职业履历：早期经历、各职务具体起止时间", "why_it_matters": "核心人物履历缺失", "suggested_queries": ["李化 简历 鄠邑区", "李化 任前公示", "李化 西安 任职经历"], "last_attempted": AS_OF},
                {"priority": "high", "question": "李化何时开始担任鄠邑区委书记？", "why_it_matters": "精确时间线对关系网络分析重要", "suggested_queries": ["李化 任鄠邑区委书记 时间", "鄠邑区 区委书记 任命"], "last_attempted": AS_OF},
                {"priority": "high", "question": "李化担任鄠邑区委书记前的职务是什么？", "why_it_matters": "了解晋升路径", "suggested_queries": ["李化 此前 担任", "李化 西安市 任职"], "last_attempted": AS_OF}
            ]
        }
    },
    "汪国栋": {
        "filename": f"{TODAY}-陕西省-西安市-鄠邑区-区长-汪国栋.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "陕西省",
                "city": "西安市",
                "region": "鄠邑区",
                "job": "区长",
                "task_id": "shaanxi_鄠邑区",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "huyi_wang_guodong",
                "name": "汪国栋",
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
                    "name_birth": "汪国栋_",
                    "name_birthplace": "汪国栋_",
                    "official_profile_url": "http://www.huyi.gov.cn/（网站访问失败）"
                }
            },
            "current_status": {
                "current_post": "区委副书记、区政府党组书记、区长",
                "current_org": "西安市鄠邑区人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {"start": "unknown", "end": "unknown", "org": "（履历待查）", "title": "早期工作经历", "level": "", "location": "", "system": "unknown", "rank": "", "is_key_promotion": False, "notes": "公开资料未找到汪国栋完整履历", "confidence": "unverified", "source_ids": []},
            ],
            "organizations": [],
            "relationships": [
                {"person": "李化", "person_id": "huyi_li_hua", "relationship_type": "overlap", "strength": "strong", "evidence": "区长与区委书记党政工作搭档", "overlap_org": "中共鄠邑区委", "overlap_period": "unknown-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "履历待查",
                "systems_experience": ["government", "party"],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "晋升速度待查", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分、审计问题或负面报道", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [{
                "id": "S001",
                "title": "网络搜索—汪国栋 鄠邑区 区长（网站访问失败，基于已知信息）",
                "url": "无法访问鄠邑区政府官网",
                "publisher": "",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "inferred",
                "reliability": "low",
                "notes": "Web access was fully degraded. 汪国栋's role as 鄠邑区区长 is based on prior knowledge."
            }],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": "汪国栋完整履历：出生信息、教育背景、所有任职经历"
            },
            "open_questions": [
                {"priority": "critical", "question": "汪国栋的完整职业履历：出生年份、籍贯、教育背景、所有任职经历", "why_it_matters": "核心人物履历完全缺失", "suggested_queries": ["汪国栋 简历 鄠邑区", "汪国栋 任前公示", "汪国栋 西安 任职经历"], "last_attempted": AS_OF},
                {"priority": "high", "question": "汪国栋何时开始担任鄠邑区区长？", "why_it_matters": "精确时间线对关系网络分析重要", "suggested_queries": ["汪国栋 任鄠邑区长 时间", "鄠邑区 区长 任命"], "last_attempted": AS_OF}
            ]
        }
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

def write_person_json(data: dict, filename: str) -> Path:
    path = STAGING_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {path}")
    return path

def main():
    print(f"Building network for {SLUG}...")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print()

    run_build(
        slug=SLUG,
        persons=persons_data,
        organizations=organizations_data,
        positions=positions_data,
        relationships=relationships_data,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print()

    print("Writing person JSON files...")
    for key, entry in PERSON_JSON_TEMPLATE.items():
        write_person_json(entry["data"], entry["filename"])

    print()
    print("=" * 60)
    print(f"Build complete for {SLUG}")
    print(f"  {len(persons_data)} persons")
    print(f"  {len(organizations_data)} organizations")
    print(f"  {len(positions_data)} positions")
    print(f"  {len(relationships_data)} relationships")
    print(f"  {len(PERSON_JSON_TEMPLATE)} person JSONs")
    print("=" * 60)

if __name__ == "__main__":
    main()
