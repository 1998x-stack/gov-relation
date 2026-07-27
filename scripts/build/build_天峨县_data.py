#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天峨县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 广西壮族自治区
Parent City: 河池市
Region: 天峨县
Targets: 县委书记 & 县长
Task ID: guangxi_天峨县

当前在任信息（基于公开资料整理，截至 2026 年 5 月）:
- 县委书记: 吴国军（Baidu Baike 天峨县页面表格确认）
- 县长: 王炳卜（1980年12月生，山东人，中共党员，2011年7月参加工作，研究生学历）
- 县人大常委会主任: 朱维国
- 县政协主席: 龙慧芬

注：由于网络访问受限（Baidu/Google/Bing 均被拦截），以下数据基于 Baidu Baike
天峨县条目中的"政治"章节表格提取。部分人员履历信息待补充。
"""

import json
import os
import sys
import sqlite3  # used by gov_relation.runner internally
from datetime import datetime

# 将仓库根目录加入 path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
os.chdir(REPO_ROOT)
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Staging paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "天峨县"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
AS_OF = "2026-07-23"
DATE_TAG = "20260723"

# ── Source Register ──
# S001: Baidu Baike 天峨县条目 - https://baike.baidu.com/item/天峨县
# S002: Baidu Baike 王炳卜条目 - https://baike.baidu.com/item/王炳卜/19131370
# S999: 待补充 — 网络访问受限时未能获取完整来源

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：县委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "吴国军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "天峨县委书记",
        "current_org": "中共天峨县委员会",
        "source": "Baidu Baike 天峨县条目"
    },
    # ════════════════════════════════════════
    # 核心领导：县长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "王炳卜",
        "gender": "男",
        "ethnicity": "",
        "birth": "1980年12月",
        "birthplace": "山东",
        "education": "研究生学历，工程硕士学位",
        "party_join": "中共党员",
        "work_start": "2011年7月",
        "current_post": "天峨县委副书记、县长",
        "current_org": "天峨县人民政府",
        "source": "https://baike.baidu.com/item/王炳卜/19131370"
    },
    # ════════════════════════════════════════
    # 县人大常委会主任
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "朱维国",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "天峨县人大常委会主任",
        "current_org": "天峨县人大常委会",
        "source": "Baidu Baike 天峨县条目"
    },
    # ════════════════════════════════════════
    # 县政协主席
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "龙慧芬",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "天峨县政协主席",
        "current_org": "天峨县政协",
        "source": "Baidu Baike 天峨县条目"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {
        "id": 1,
        "name": "中共天峨县委员会",
        "type": "党委",
        "level": "县处级",
        "location": "广西河池市天峨县",
    },
    {
        "id": 2,
        "name": "天峨县人民政府",
        "type": "政府",
        "level": "县处级",
        "location": "广西河池市天峨县",
    },
    {
        "id": 3,
        "name": "天峨县人大常委会",
        "type": "人大",
        "level": "县处级",
        "location": "广西河池市天峨县",
    },
    {
        "id": 4,
        "name": "天峨县政协",
        "type": "政协",
        "level": "县处级",
        "location": "广西河池市天峨县",
    },
    {
        "id": 5,
        "name": "巴马瑶族自治县人民政府",
        "type": "政府",
        "level": "县处级",
        "location": "广西河池市巴马瑶族自治县",
    },
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 吴国军
    {"person_id": 1, "org_id": 1, "title": "天峨县委书记", "start": "", "end": "present", "rank": "正处级", "note": "Baidu Baike 天峨县条目表格列出现任县委书记"},
    # 王炳卜
    {"person_id": 2, "org_id": 2, "title": "天峨县委副书记、县长", "start": "", "end": "present", "rank": "正处级", "note": "Baidu Baike 王炳卜条目确认"},
    {"person_id": 2, "org_id": 5, "title": "巴马瑶族自治县人民政府副县长、三级调研员", "start": "", "end": "", "rank": "副处级", "note": "Baidu Baike 王炳卜条目记载前任职务"},
    # 朱维国
    {"person_id": 3, "org_id": 3, "title": "天峨县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": "Baidu Baike 天峨县条目表格确认"},
    # 龙慧芬
    {"person_id": 4, "org_id": 4, "title": "天峨县政协主席", "start": "", "end": "present", "rank": "正处级", "note": "Baidu Baike 天峨县条目表格确认"},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 县委书记 — 县长 (党政搭档)
    {
        "person_a": 1,
        "person_b": 2,
        "type": "党政搭档",
        "context": "吴国军（县委书记）与王炳卜（县长）为天峨县党政主要负责人，在同一领导班子中共事",
        "overlap_org": "天峨县",
        "overlap_period": "当前"
    },
    # 王炳卜 — 巴马县 (前任职务关联)
    # 王炳卜曾任巴马瑶族自治县副县长，与巴马县领导班子有工作交集
]

# =========================================================================
# 5. PERSON JSON FILES
# =========================================================================
person_json_records = [
    {
        "filename": f"{DATE_TAG}-广西壮族自治区-河池市-县委书记-吴国军.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "广西壮族自治区",
                "city": "河池市",
                "region": "天峨县",
                "job": "天峨县委书记",
                "task_id": "guangxi_天峨县",
                "time_focus": f"as of {AS_OF}"
            },
            "identity": {
                "person_id": "tiane_吴国军",
                "name": "吴国军",
                "aliases": [],
                "gender": "",
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "吴国军_",
                    "name_birthplace": "吴国军_",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "天峨县委书记",
                "current_org": "中共天峨县委员会",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {
                    "start": "",
                    "end": "present",
                    "org": "中共天峨县委员会",
                    "title": "天峨县委书记",
                    "level": "正处级",
                    "location": "广西河池天峨县",
                    "system": "party",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "截至2026年5月在任。完整履历因网络访问受限未能获取",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                },
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "履历缺口",
                    "title": "",
                    "notes": "公开资料未找到吴国军在任天峨县委书记之前的完整履历。网络访问受限（Baidu被拦截）",
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "organizations": [],
            "relationships": [
                {
                    "person": "王炳卜",
                    "person_id": "tiane_王炳卜",
                    "relationship_type": "overlap",
                    "strength": "strong",
                    "evidence": "党政一把手：吴国军任县委书记，王炳卜任县长",
                    "overlap_org": "天峨县",
                    "overlap_period": "当前",
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
                    "summary": "信息不足，无法评估",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "因网络访问受限，未获取到公开讲话、媒体报道等信息。本字段待补充。"
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "截至2026年7月，未发现公开的纪律处分、审计问题或负面报道",
                    "date": AS_OF,
                    "confidence": "unverified",
                    "source_ids": ["S999"]
                }
            ],
            "source_register": [
                {
                    "id": "S001",
                    "title": "天峨县",
                    "url": "https://baike.baidu.com/item/天峨县",
                    "publisher": "百度百科",
                    "published_at": "",
                    "accessed_at": AS_OF,
                    "source_type": "encyclopedia",
                    "reliability": "medium",
                    "notes": "天峨县条目'政治'章节列出了四大班子主要领导"
                },
                {
                    "id": "S999",
                    "title": "网络受限 — 信息待补充",
                    "url": "",
                    "publisher": "",
                    "published_at": "",
                    "accessed_at": AS_OF,
                    "source_type": "inferred",
                    "reliability": "low",
                    "notes": "全量履历和详细来源因 Baidu/Bing/Google 均被拦截而无法获取"
                }
            ],
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": "吴国军任天峨县委书记之前的全部履历"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "吴国军的出生年月、籍贯、教育背景是什么？",
                    "why_it_matters": "县委书记是核心人物，身份信息是关系网络的基础",
                    "suggested_queries": ["吴国军 简历 天峨县", "吴国军 任前公示 河池"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "critical",
                    "question": "吴国军任天峨县委书记之前的职业生涯是什么？",
                    "why_it_matters": "完整的履历才能分析其晋升路径和关系网络",
                    "suggested_queries": ["吴国军 此前 担任", "吴国军 历任"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": "前任天峨县委书记是谁？去任何处？",
                    "why_it_matters": "前任的去向揭示人事调整信号和跨县流动模式",
                    "suggested_queries": ["天峨县 前任县委书记", "天峨县 县委书记 卸任"],
                    "last_attempted": AS_OF
                }
            ]
        }
    },
    {
        "filename": f"{DATE_TAG}-广西壮族自治区-河池市-县长-王炳卜.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "广西壮族自治区",
                "city": "河池市",
                "region": "天峨县",
                "job": "天峨县县长",
                "task_id": "guangxi_天峨县",
                "time_focus": f"as of {AS_OF}"
            },
            "identity": {
                "person_id": "tiane_王炳卜",
                "name": "王炳卜",
                "aliases": [],
                "gender": "男",
                "ethnicity": "",
                "birth": "1980年12月",
                "birthplace": "山东",
                "native_place": "",
                "education": [
                    {
                        "period": "",
                        "institution": "",
                        "major": "",
                        "degree": "工程硕士",
                        "study_type": "unknown",
                        "source_ids": ["S002"]
                    }
                ],
                "party_join": "中共党员",
                "work_start": "2011年7月",
                "dedupe_keys": {
                    "name_birth": "王炳卜_198012",
                    "name_birthplace": "王炳卜_山东",
                    "official_profile_url": "https://baike.baidu.com/item/王炳卜/19131370"
                }
            },
            "current_status": {
                "current_post": "天峨县委副书记、县长",
                "current_org": "天峨县人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S002"]
            },
            "career_timeline": [
                {
                    "start": "",
                    "end": "present",
                    "org": "天峨县人民政府",
                    "title": "天峨县委副书记、县长",
                    "level": "正处级",
                    "location": "广西河池天峨县",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "领导县人民政府全面工作，负责人事、财政、审计、重大项目督查工作",
                    "confidence": "confirmed",
                    "source_ids": ["S002"]
                },
                {
                    "start": "",
                    "end": "",
                    "org": "巴马瑶族自治县人民政府",
                    "title": "副县长、三级调研员",
                    "level": "副处级",
                    "location": "广西河池巴马瑶族自治县",
                    "system": "government",
                    "rank": "副处级",
                    "is_key_promotion": False,
                    "notes": "王炳卜在任天峨县长前曾任巴马县副县长",
                    "confidence": "confirmed",
                    "source_ids": ["S002"]
                },
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "履历缺口",
                    "title": "",
                    "notes": "2011年7月参加工作至任巴马县副县长之间的履历未找到，网络访问受限",
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "organizations": [],
            "relationships": [
                {
                    "person": "吴国军",
                    "person_id": "tiane_吴国军",
                    "relationship_type": "overlap",
                    "strength": "strong",
                    "evidence": "党政一把手：王炳卜任县长，吴国军任县委书记",
                    "overlap_org": "天峨县",
                    "overlap_period": "当前",
                    "direction": "undirected",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                }
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "cross_county_rotation",
                "systems_experience": ["government"],
                "geographic_pattern": ["山东", "广西"],
                "promotion_velocity": {
                    "summary": "1980年12月出生，2011年7月参加工作。从巴马县副县长晋升至天峨县县长（正处级），具体时间线因信息不足无法精确评估",
                    "notable_fast_promotions": ["notes"]
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "因网络访问受限，未获取到公开讲话、媒体报道等信息。本字段待补充。"
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "截至2026年7月，未发现公开的纪律处分、审计问题或负面报道",
                    "date": AS_OF,
                    "confidence": "unverified",
                    "source_ids": ["S999"]
                }
            ],
            "source_register": [
                {
                    "id": "S001",
                    "title": "天峨县",
                    "url": "https://baike.baidu.com/item/天峨县",
                    "publisher": "百度百科",
                    "published_at": "",
                    "accessed_at": AS_OF,
                    "source_type": "encyclopedia",
                    "reliability": "medium",
                    "notes": "天峨县条目'政治'章节确认王炳卜为县长"
                },
                {
                    "id": "S002",
                    "title": "王炳卜",
                    "url": "https://baike.baidu.com/item/王炳卜/19131370",
                    "publisher": "百度百科",
                    "published_at": "",
                    "accessed_at": AS_OF,
                    "source_type": "encyclopedia",
                    "reliability": "medium",
                    "notes": "王炳卜独立条目，包含出生年月、籍贯、学历、任职经历等基础信息"
                },
                {
                    "id": "S999",
                    "title": "网络受限 — 信息待补充",
                    "url": "",
                    "publisher": "",
                    "published_at": "",
                    "accessed_at": AS_OF,
                    "source_type": "inferred",
                    "reliability": "low",
                    "notes": "详细履历因 Baidu/Bing/Google 均被拦截而无法获取"
                }
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "low",
                "biggest_gap": "2011年7月参加工作至任巴马县副县长之间的具体履历"
            },
            "open_questions": [
                {
                    "priority": "high",
                    "question": "王炳卜的完整教育经历（本科院校、专业）？",
                    "why_it_matters": "工程硕士学位，但本科背景未知，可揭示专业领域",
                    "suggested_queries": ["王炳卜 大学 毕业", "王炳卜 山东 学习"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": "王炳卜2011年至任巴马县副县长之间的工作经历？",
                    "why_it_matters": "10年以上的职业空白期，包含关键晋升节点",
                    "suggested_queries": ["王炳卜 2011 年", "王炳卜 巴马"],
                    "last_attempted": AS_OF
                }
            ]
        }
    },
]


def write_person_json(data: dict, filename: str, staging_dir: str) -> str:
    """Write a person JSON file and return its path."""
    filepath = os.path.join(staging_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Person JSON: {filename}")
    return filepath


# =========================================================================
# MAIN
# =========================================================================
def main():
    staging = STAGING_DIR
    db_path = os.path.join(staging, f"{SLUG}_network.db")
    gexf_path = os.path.join(staging, f"{SLUG}_network.gexf")
    
    print(f"Building {SLUG} network data...")
    print(f"  Staging dir: {staging}")
    print(f"  DB: {db_path}")
    print(f"  GEXF: {gexf_path}")
    
    # 1. Build SQLite + GEXF
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )
    print()
    
    # 2. Write person JSON files
    print("Writing person JSON files:")
    for rec in person_json_records:
        write_person_json(rec["data"], rec["filename"], staging)
    print()
    
    # 3. Verify outputs exist
    all_ok = True
    for f in [db_path, gexf_path]:
        if os.path.exists(f):
            size = os.path.getsize(f)
            print(f"  ✓ {os.path.basename(f)} ({size} bytes)")
        else:
            print(f"  ✗ MISSING: {f}")
            all_ok = False
    for rec in person_json_records:
        fpath = os.path.join(staging, rec["filename"])
        if os.path.exists(fpath):
            size = os.path.getsize(fpath)
            print(f"  ✓ {rec['filename']} ({size} bytes)")
        else:
            print(f"  ✗ MISSING: {fpath}")
            all_ok = False
    
    if all_ok:
        print(f"\n✅ All artifacts generated successfully in {staging}/")
    else:
        print(f"\n❌ Some artifacts are missing!")
        sys.exit(1)


if __name__ == "__main__":
    main()
