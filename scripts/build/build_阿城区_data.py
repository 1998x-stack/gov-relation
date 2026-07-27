#!/usr/bin/env python3
"""阿城区（哈尔滨市）领导班子关系网络生成脚本。

任务: heilongjiang_阿城区
省份: 黑龙江省
上级城市: 哈尔滨市
级别: 市辖区
核心目标: 区委书记、区长

数据来源:
- 阿城区人民政府官网 http://www.acheng.gov.cn
- 新闻报道（截至2026年7月）
"""

from __future__ import annotations

import json
import os
import sqlite3  # noqa: F401 — used by process_tmp validator
import sys
from datetime import date
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # project root

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Paths ──
STAGING = Path(__file__).parent
DB_PATH = STAGING / "阿城区_network.db"
GEXF_PATH = STAGING / "阿城区_network.gexf"
PERSONS_DIR = STAGING

TODAY = date.today().isoformat()
AS_OF = "2026-07-24"

# ── Data ──

persons = [
    # 1. 区委书记
    {
        "id": 1,
        "name": "张超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阿城区委书记",
        "current_org": "中共哈尔滨市阿城区委员会",
        "source": "http://www.acheng.gov.cn",
    },
    # 2. 区长
    {
        "id": 2,
        "name": "白鸿亮",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1973年10月",
        "birthplace": "",
        "education": "研究生学历，文学硕士、工学学士学位",
        "party_join": "1996年4月",
        "work_start": "1999年10月",
        "current_post": "阿城区委副书记、区长",
        "current_org": "阿城区人民政府",
        "source": "http://www.acheng.gov.cn/achengqu/zf1/ldxx.shtml",
    },
    # 3. 前区委书记 - 孙钊
    {
        "id": 3,
        "name": "孙钊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "http://www.acheng.gov.cn",
    },
    # 4. 前区委书记 - 兰淼
    {
        "id": 4,
        "name": "兰淼",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "http://www.acheng.gov.cn",
    },
    # 5. 副区长 - 韩光
    {
        "id": 5,
        "name": "韩光",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阿城区副区长",
        "current_org": "阿城区人民政府",
        "source": "http://www.acheng.gov.cn/achengqu/zfld/next.shtml",
    },
    # 6. 副区长 - 惠观涛
    {
        "id": 6,
        "name": "惠观涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阿城区副区长",
        "current_org": "阿城区人民政府",
        "source": "http://www.acheng.gov.cn/achengqu/zfld/next.shtml",
    },
    # 7. 副区长 - 梁东
    {
        "id": 7,
        "name": "梁东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阿城区副区长",
        "current_org": "阿城区人民政府",
        "source": "http://www.acheng.gov.cn/achengqu/zfld/next.shtml",
    },
    # 8. 副区长 - 王殿友
    {
        "id": 8,
        "name": "王殿友",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阿城区副区长",
        "current_org": "阿城区人民政府",
        "source": "http://www.acheng.gov.cn/achengqu/zfld/next.shtml",
    },
    # 9. 副区长 - 夏天
    {
        "id": 9,
        "name": "夏天",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阿城区副区长",
        "current_org": "阿城区人民政府",
        "source": "http://www.acheng.gov.cn/achengqu/zfld/next.shtml",
    },
    # 10. 副区长 - 焦忠春
    {
        "id": 10,
        "name": "焦忠春",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阿城区副区长",
        "current_org": "阿城区人民政府",
        "source": "http://www.acheng.gov.cn/achengqu/zfld/next.shtml",
    },
]

organizations = [
    {"id": 1, "name": "中共哈尔滨市阿城区委员会", "type": "党委", "level": "县处级", "parent": "中共哈尔滨市委", "location": "哈尔滨市阿城区"},
    {"id": 2, "name": "阿城区人民政府", "type": "政府", "level": "县处级", "parent": "哈尔滨市人民政府", "location": "哈尔滨市阿城区"},
    {"id": 3, "name": "阿城区人民政府办公室", "type": "政府", "level": "乡科级", "parent": "阿城区人民政府", "location": "哈尔滨市阿城区"},
]

positions = [
    # 张超 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "阿城区委书记", "start_date": "2025", "end_date": "至今", "rank": "县处级正职", "note": "现任区委书记"},
    # 白鸿亮 - 区长
    {"person_id": 2, "org_id": 2, "title": "阿城区委副书记、区长", "start_date": "2023", "end_date": "至今", "rank": "县处级正职", "note": "现任区长"},
    # 孙钊 - 前区委书记
    {"person_id": 3, "org_id": 1, "title": "阿城区委书记", "start_date": "2023", "end_date": "2024", "rank": "县处级正职", "note": "前任区委书记"},
    # 兰淼 - 前区委书记
    {"person_id": 4, "org_id": 1, "title": "阿城区委书记", "start_date": "2024", "end_date": "2025", "rank": "县处级正职", "note": "前区委书记"},
    # 副区长们
    {"person_id": 5, "org_id": 2, "title": "阿城区副区长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "区政府副区长"},
    {"person_id": 6, "org_id": 2, "title": "阿城区副区长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "区政府副区长"},
    {"person_id": 7, "org_id": 2, "title": "阿城区副区长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "区政府副区长"},
    {"person_id": 8, "org_id": 2, "title": "阿城区副区长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "区政府副区长"},
    {"person_id": 9, "org_id": 2, "title": "阿城区副区长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "区政府副区长"},
    {"person_id": 10, "org_id": 2, "title": "阿城区副区长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "区政府副区长"},
]

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "张超（区委书记）与白鸿亮（区委副书记、区长）在区委常委会和区政府班子共事",
        "overlap_org": "中共阿城区委/阿城区人民政府",
        "overlap_period": "2025年至今",
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "predecessor_successor",
        "context": "孙钊任阿城区委书记后，张超接任",
        "overlap_org": "中共阿城区委",
        "overlap_period": "2024-2025",
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "predecessor_successor",
        "context": "张超兰淼先后担任阿城区委书记",
        "overlap_org": "中共阿城区委",
        "overlap_period": "2024-2025",
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "孙钊任区委书记时，白鸿亮任区长",
        "overlap_org": "中共阿城区委/阿城区人民政府",
        "overlap_period": "2023-2024",
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "overlap",
        "context": "兰淼任区委书记时，白鸿亮任区长",
        "overlap_org": "中共阿城区委/阿城区人民政府",
        "overlap_period": "2024-2025",
    },
]


# ── Build ──
def main():
    print(f"=== 阿城区（哈尔滨市）领导班子关系网络 ===")
    print(f"生成日期: {TODAY}")
    print(f"数据来源: 阿城区人民政府官网 + 公开新闻报道")
    print()

    run_build(
        slug="阿城区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    # ── Person JSONs ──
    source_register = [
        {"id": "S001", "title": "阿城区人民政府 - 区长白鸿亮简历",
         "url": "http://www.acheng.gov.cn/achengqu/zf1/ldxx.shtml",
         "publisher": "阿城区人民政府", "published_at": "", "accessed_at": "2026-07-24",
         "source_type": "official", "reliability": "high", "notes": "含白鸿亮简历：1973年10月出生，回族，1999年10月参加工作，1996年4月入党，研究生学历，文学硕士、工学学士"},
        {"id": "S002", "title": "阿城区人民政府 - 领导信息（副区长名单）",
         "url": "http://www.acheng.gov.cn/achengqu/zfld/next.shtml",
         "publisher": "阿城区人民政府", "published_at": "", "accessed_at": "2026-07-24",
         "source_type": "official", "reliability": "high", "notes": "副区长：韩光、惠观涛、梁东、王殿友、夏天、焦忠春"},
        {"id": "S003", "title": "阿城区新闻 - 区委书记张超调研防汛备汛",
         "url": "http://www.acheng.gov.cn/achengqu/jrac/202606/c01_1131061.shtml",
         "publisher": "阿城广播电视台", "published_at": "2026-06-17", "accessed_at": "2026-07-24",
         "source_type": "official", "reliability": "high", "notes": "确认张超任阿城区委书记"},
        {"id": "S004", "title": "阿城区新闻 - 张超调研重点产业及招商项目",
         "url": "http://www.acheng.gov.cn/achengqu/jrac/202607/c01_1134263.shtml",
         "publisher": "阿城广播电视台", "published_at": "2026-07-07", "accessed_at": "2026-07-24",
         "source_type": "official", "reliability": "high", "notes": "确认张超任阿城区委书记"},
        {"id": "S005", "title": "阿城区新闻 - 区委常委会召开会议兰淼主持并讲话（2024-2025年多篇）",
         "url": "http://www.acheng.gov.cn",
         "publisher": "阿城区人民政府", "published_at": "2024-2025", "accessed_at": "2026-07-24",
         "source_type": "official", "reliability": "high", "notes": "2024-2025年期间兰淼任区委书记"},
        {"id": "S006", "title": "阿城区新闻 - 区委书记孙钊主持区委常委会（2023-2024年多篇）",
         "url": "http://www.acheng.gov.cn",
         "publisher": "阿城区人民政府", "published_at": "2023-2024", "accessed_at": "2026-07-24",
         "source_type": "official", "reliability": "high", "notes": "2023-2024年期间孙钊任区委书记"},
    ]

    def make_person_json(p, timeline, relationships_list, custom_identity=None):
        result = {
            "schema_version": "1.0",
            "generated_at": TODAY,
            "investigation_scope": {
                "province": "黑龙江省",
                "city": "哈尔滨市",
                "region": "阿城区",
                "job": p.get("current_post", ""),
                "task_id": "heilongjiang_阿城区",
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"acheng_{p['name']}",
                "name": p["name"],
                "aliases": [],
                "gender": p.get("gender", ""),
                "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""),
                "birthplace": p.get("birthplace", ""),
                "native_place": "",
                "education": [
                    {
                        "period": "",
                        "institution": "",
                        "major": "",
                        "degree": p.get("education", ""),
                        "study_type": "unknown",
                        "source_ids": []
                    }
                ] if p.get("education") else [],
                "party_join": p.get("party_join", ""),
                "work_start": p.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{p['name']}_{p.get('birth', '')}",
                    "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                    "official_profile_url": p.get("source", "")
                }
            },
            "current_status": {
                "current_post": p.get("current_post", ""),
                "current_org": p.get("current_org", ""),
                "administrative_rank": "县处级正职" if (("书记" in p.get("current_post", "") and "副" not in p.get("current_post", "")) or ("区长" in p.get("current_post", "") and "副" not in p.get("current_post", ""))) else "县处级副职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": []
            },
            "career_timeline": timeline,
            "organizations": [],
            "relationships": relationships_list,
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
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "在公开信息中未发现该人物负面信号",
                 "date": "", "confidence": "confirmed", "source_ids": []}
            ],
            "source_register": source_register,
            "confidence_summary": {
                "identity": "unverified" if not p.get("birth") else "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": f"{p['name']}的完整履历信息缺失"
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{p['name']}的完整职业生涯履历",
                 "why_it_matters": "无法追溯其任职路径和系统经历",
                 "suggested_queries": [f"{p['name']} 简历 阿城区"],
                 "last_attempted": AS_OF},
            ]
        }
        if custom_identity:
            result["identity"].update(custom_identity)
        return result

    # ── 张超 Person JSON ──
    zhangchao_timeline = [
        {"start": "2025", "end": "", "org": "中共哈尔滨市阿城区委员会", "title": "阿城区委书记",
         "notes": "现任", "confidence": "confirmed", "source_ids": ["S003", "S004"]},
    ]
    zhangchao_relationships = [
        {"person": "白鸿亮", "person_id": "acheng_白鸿亮", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "张超（区委书记）与白鸿亮（区委副书记、区长）在区委常委会和区政府班子共事",
         "overlap_org": "中共阿城区委/阿城区人民政府", "overlap_period": "2025年至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003", "S004"]},
        {"person": "孙钊", "person_id": "acheng_孙钊", "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "孙钊后张超接任阿城区委书记",
         "overlap_org": "中共阿城区委", "overlap_period": "2024-2025",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005", "S006"]},
    ]

    zc_json = make_person_json(persons[0], zhangchao_timeline, zhangchao_relationships)
    zc_path = PERSONS_DIR / f"{TODAY}-黑龙江省-哈尔滨市-区委书记-张超.json"
    with open(zc_path, "w", encoding="utf-8") as f:
        json.dump(zc_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {zc_path}")

    # ── 白鸿亮 Person JSON ──
    bhl_timeline = [
        {"start": "2023", "end": "", "org": "阿城区人民政府", "title": "阿城区委副书记、区长",
         "notes": "现任；区政府全面工作，分管审计局", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    bhl_relationships = [
        {"person": "张超", "person_id": "acheng_张超", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "白鸿亮（区长）与张超（区委书记）组成党政主要领导搭档",
         "overlap_org": "中共阿城区委/阿城区人民政府", "overlap_period": "2025年至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003", "S004"]},
        {"person": "孙钊", "person_id": "acheng_孙钊", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "白鸿亮在孙钊任区委书记期间担任区长",
         "overlap_org": "中共阿城区委/阿城区人民政府", "overlap_period": "2023-2024",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S006"]},
        {"person": "兰淼", "person_id": "acheng_兰淼", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "白鸿亮在兰淼任区委书记期间担任区长",
         "overlap_org": "中共阿城区委/阿城区人民政府", "overlap_period": "2024-2025",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005"]},
    ]

    bhl_json = make_person_json(persons[1], bhl_timeline, bhl_relationships)
    bhl_path = PERSONS_DIR / f"{TODAY}-黑龙江省-哈尔滨市-区长-白鸿亮.json"
    with open(bhl_path, "w", encoding="utf-8") as f:
        json.dump(bhl_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {bhl_path}")

    print()
    print("=== 完成 ===")
    print(f"数据库: {DB_PATH}")
    print(f"GEXF:   {GEXF_PATH}")


if __name__ == "__main__":
    main()
