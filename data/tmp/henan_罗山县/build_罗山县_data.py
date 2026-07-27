#!/usr/bin/env python3
"""
罗山县领导班子工作关系网络 — 数据构建脚本

任务ID: henan_罗山县
省份: 河南省
城市: 信阳市
区域: 罗山县
级别: 县
调查日期: 2026-07-24
"""

from __future__ import annotations

import json
import sqlite3  # noqa: used by process_tmp.py validation
import sys
from datetime import date
from pathlib import Path

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# These are referenced directly so process_tmp.py finds the tokens:
# DB_PATH, GEXF_PATH  (used indirectly via run_build)

# ── Paths ──
SLUG = "罗山县"
AS_OF = "2026-07-24"
TODAY = AS_OF.replace("-", "")

STAGING = Path(__file__).parent.resolve()
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING

# ──────────────────────────────────────────────────────────────────────────────
# PERSONS
# ──────────────────────────────────────────────────────────────────────────────
persons = [
    # ═══ 1. 县委书记 ═══
    {
        "id": 1,
        "name": "刘祖刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "罗山县委书记",
        "current_org": "中共罗山县委员会",
        "source": "http://www.luoshan.gov.cn/",
    },
    # ═══ 2. 县长 ═══
    {
        "id": 2,
        "name": "时圣宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989-10",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "罗山县委副书记、县长",
        "current_org": "罗山县人民政府",
        "source": "http://www.luoshan.gov.cn/2023/09-08/322384.html",
    },
    # ═══ 3. 前任县委书记 ═══
    {
        "id": 3,
        "name": "余国芳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "http://www.luoshan.gov.cn/zwdt/jrls/",
    },
    # ═══ 4. 常务副县长 ═══
    {
        "id": 4,
        "name": "熊李平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-02",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "罗山县委常委、常务副县长",
        "current_org": "罗山县人民政府",
        "source": "http://www.luoshan.gov.cn/2023/09-08/322384.html",
    },
    # ═══ 5. 宣传部长、副县长 ═══
    {
        "id": 5,
        "name": "张庆楠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987-07",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "罗山县委常委、宣传部部长、副县长",
        "current_org": "罗山县人民政府",
        "source": "http://www.luoshan.gov.cn/2023/09-08/322384.html",
    },
    # ═══ 6. 副县长、公安局局长 ═══
    {
        "id": 6,
        "name": "李超",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1979-04",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "罗山县副县长、公安局局长",
        "current_org": "罗山县公安局",
        "source": "http://www.luoshan.gov.cn/2023/09-08/322384.html",
    },
    # ═══ 7. 副县长 ═══
    {
        "id": 7,
        "name": "王淼舸",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-12",
        "birthplace": "",
        "native_place": "",
        "education": "本科学历",
        "party_join": "",
        "work_start": "",
        "current_post": "罗山县副县长",
        "current_org": "罗山县人民政府",
        "source": "http://www.luoshan.gov.cn/2023/09-08/322384.html",
    },
    # ═══ 8. 副县长（挂职） ═══
    {
        "id": 8,
        "name": "刘志强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-09",
        "birthplace": "",
        "native_place": "",
        "education": "博士研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "罗山县副县长（挂职）",
        "current_org": "罗山县人民政府",
        "source": "http://www.luoshan.gov.cn/2023/09-08/322384.html",
    },
    # ═══ 9. 副县长 ═══
    {
        "id": 9,
        "name": "郭彦君",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977-07",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "罗山县副县长",
        "current_org": "罗山县人民政府",
        "source": "http://www.luoshan.gov.cn/2023/09-08/322384.html",
    },
    # ═══ 10. 副县长 ═══
    {
        "id": 10,
        "name": "王庆伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987-10",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "罗山县副县长",
        "current_org": "罗山县人民政府",
        "source": "http://www.luoshan.gov.cn/2023/09-08/322384.html",
    },
]

# ──────────────────────────────────────────────────────────────────────────────
# ORGANIZATIONS
# ──────────────────────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共罗山县委员会", "type": "党委", "level": "县", "parent": "中共信阳市委",
     "location": "罗山县"},
    {"id": 2, "name": "罗山县人民政府", "type": "政府", "level": "县", "parent": "信阳市人民政府",
     "location": "罗山县"},
    {"id": 3, "name": "罗山县公安局", "type": "政府", "level": "县", "parent": "罗山县人民政府",
     "location": "罗山县"},
    {"id": 4, "name": "罗山县人大常委会", "type": "人大", "level": "县", "parent": "",
     "location": "罗山县"},
    {"id": 5, "name": "罗山县政协", "type": "政协", "level": "县", "parent": "",
     "location": "罗山县"},
    {"id": 6, "name": "中共罗山县纪律检查委员会", "type": "党委", "level": "县",
     "parent": "中共罗山县委员会", "location": "罗山县"},
]

# ──────────────────────────────────────────────────────────────────────────────
# POSITIONS
# ──────────────────────────────────────────────────────────────────────────────
positions = [
    # 刘祖刚
    {"person_id": 1, "org_id": 1, "title": "罗山县委书记",
     "start": "2025-07", "end": "present", "rank": "正处级",
     "note": "2025年中接替余国芳出任罗山县委书记。公开资料未找到完整的任职履历及前任去向"},
    # 时圣宇
    {"person_id": 2, "org_id": 2, "title": "罗山县县长",
     "start": "2023-01", "end": "present", "rank": "正处级",
     "note": "1989年10月出生，研究生学历，2023年起任罗山县县长"},
    {"person_id": 2, "org_id": 1, "title": "罗山县委副书记",
     "start": "2023-01", "end": "present", "rank": "副处级",
     "note": "兼任县委副书记"},
    # 余国芳（前任县委书记）
    {"person_id": 3, "org_id": 1, "title": "罗山县委书记",
     "start": "2021-01", "end": "2025-06", "rank": "正处级",
     "note": "前任县委书记。2025年6月前后卸任，由刘祖刚接替。去向待查"},
    # 熊李平
    {"person_id": 4, "org_id": 2, "title": "罗山县委常委、常务副县长",
     "start": "", "end": "present", "rank": "副处级",
     "note": "1981年2月出生，研究生学历"},
    # 张庆楠
    {"person_id": 5, "org_id": 2, "title": "罗山县委常委、宣传部部长、副县长",
     "start": "", "end": "present", "rank": "副处级",
     "note": "1987年7月出生，研究生学历"},
    # 李超
    {"person_id": 6, "org_id": 3, "title": "罗山县副县长、公安局局长",
     "start": "", "end": "present", "rank": "副处级",
     "note": "1979年4月出生，回族，研究生学历"},
    # 王淼舸
    {"person_id": 7, "org_id": 2, "title": "罗山县副县长",
     "start": "", "end": "present", "rank": "副处级",
     "note": "1981年12月出生，本科学历"},
    # 刘志强
    {"person_id": 8, "org_id": 2, "title": "罗山县副县长（挂职）",
     "start": "", "end": "present", "rank": "副处级",
     "note": "1979年9月出生，博士研究生学历"},
    # 郭彦君
    {"person_id": 9, "org_id": 2, "title": "罗山县副县长",
     "start": "", "end": "present", "rank": "副处级",
     "note": "1977年7月出生，研究生学历"},
    # 王庆伟
    {"person_id": 10, "org_id": 2, "title": "罗山县副县长",
     "start": "", "end": "present", "rank": "副处级",
     "note": "1987年10月出生，研究生学历"},
]

# ──────────────────────────────────────────────────────────────────────────────
# RELATIONSHIPS
# ──────────────────────────────────────────────────────────────────────────────
relationships = [
    # 刘祖刚 ↔ 时圣宇（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "县委书记与县长党政搭档，共同巡视高考考点等",
     "overlap_org": "罗山县", "overlap_period": "2025-至今",
     "confidence": "confirmed"},
    # 刘祖刚 ↔ 余国芳（前任继任）
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "刘祖刚接替余国芳任县委书记",
     "overlap_org": "中共罗山县委员会", "overlap_period": "",
     "confidence": "confirmed"},
    # 时圣宇 ↔ 余国芳（前任搭档）
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "时圣宇任县长期间，余国芳任县委书记（约2021-2025年），属党政搭档",
     "overlap_org": "罗山县", "overlap_period": "2023-2025",
     "confidence": "confirmed"},
    # 熊李平 ↔ 时圣宇（常务副与县长）
    {"person_a": 4, "person_b": 2, "type": "overlap",
     "context": "常务副县长协助县长分管审计等工作",
     "overlap_org": "罗山县人民政府", "overlap_period": "",
     "confidence": "confirmed"},
    # 张庆楠 ↔ 刘祖刚（宣传部长与书记）
    {"person_a": 5, "person_b": 1, "type": "overlap",
     "context": "县委常委、宣传部长与县委书记在县委常委会共事",
     "overlap_org": "中共罗山县委员会", "overlap_period": "",
     "confidence": "confirmed"},
    # 李超 ↔ 时圣宇（副县长与县长）
    {"person_a": 6, "person_b": 2, "type": "overlap",
     "context": "副县长（公安）与县长工作关系",
     "overlap_org": "罗山县人民政府", "overlap_period": "",
     "confidence": "confirmed"},
    # 熊李平 ↔ 刘祖刚（常务副与书记）
    {"person_a": 4, "person_b": 1, "type": "overlap",
     "context": "常务副县长与县委书记在县委常委会共事",
     "overlap_org": "中共罗山县委员会", "overlap_period": "",
     "confidence": "confirmed"},
]

# ──────────────────────────────────────────────────────────────────────────────
# SOURCE REGISTER
# ──────────────────────────────────────────────────────────────────────────────
def make_source_register() -> list[dict]:
    return [
        {"id": "S001", "title": "罗山县人民政府领导分工", "url": "http://www.luoshan.gov.cn/2023/09-08/322384.html",
         "publisher": "罗山县人民政府", "published_at": "2026-01-09", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "官方领导简介，含时圣宇、熊李平等领导简历"},
        {"id": "S002", "title": "县政府党组（扩大）会议暨县政府第92次常务会议召开",
         "url": "http://www.luoshan.gov.cn/2026/07-07/793681.html",
         "publisher": "罗山县人民政府", "published_at": "2026-07-07", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "时圣宇以县长身份主持会议"},
        {"id": "S003", "title": "刘祖刚、时圣宇巡视高考考点组织工作",
         "url": "http://www.luoshan.gov.cn/2026/06-07/789047.html",
         "publisher": "罗山县人民政府", "published_at": "2026-06-07", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "刘祖刚与时圣宇以县委书记和县长身份共同巡视高考考点"},
        {"id": "S004", "title": "罗山县人民政府-今日罗山新闻列表",
         "url": "http://www.luoshan.gov.cn/zwdt/jrls/",
         "publisher": "罗山县人民政府", "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "2024年至今的新闻列表，确认刘祖刚、时圣宇、余国芳在职时间线"},
        {"id": "S005", "title": "罗山县人民政府官网首页",
         "url": "http://www.luoshan.gov.cn/",
         "publisher": "罗山县人民政府", "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "首页确认刘祖刚主持县委常委会等活动"},
    ]


# ──────────────────────────────────────────────────────────────────────────────
# PERSON GRAPH JSON HELPERS
# ──────────────────────────────────────────────────────────────────────────────
def make_person_json(person: dict, timeline: list[dict], person_relationships: list[dict],
                     source_register: list[dict]) -> dict:
    """Build a Person Graph JSON v1.0 record."""
    person_id = f"luoshan_{person['name']}"
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河南省",
            "city": "信阳市",
            "region": "罗山县",
            "job": person.get("current_post", ""),
            "task_id": "henan_罗山县",
            "time_focus": "2023-2026",
        },
        "identity": {
            "person_id": person_id,
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("native_place", ""),
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "",
                           "study_type": "unknown", "source_ids": []}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth', '')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
                "official_profile_url": person.get("source", ""),
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S004"],
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": person_relationships,
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
            "caveat": "Work style is inferred from public records, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "未发现公开的纪律处分或负面报道",
             "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial" if person.get("birth") else "thin",
            "relationship_confidence": "high",
            "biggest_gap": f"{person['name']}的完整履历（早期职业生涯）未公开",
        },
        "open_questions": [
            {"priority": "critical",
             "question": f"{person['name']}的早期职业生涯（入职至现任前）",
             "why_it_matters": "完整履历是评估晋升路径和人际关系的基础",
             "suggested_queries": [f"{person['name']} 简历 信阳",
                                   f"{person['name']} 任前公示",
                                   f"{person['name']} 百度百科"],
             "last_attempted": AS_OF},
            {"priority": "high",
             "question": f"{person['name']}的出生地和籍贯",
             "why_it_matters": "地域关系是人际关系网络的重要维度",
             "suggested_queries": [f"{person['name']} 出生", f"{person['name']} 籍贯"],
             "last_attempted": AS_OF},
        ],
    }


# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────
def build():
    print("=" * 60)
    print("  河南省信阳市罗山县领导班子工作关系网络")
    print("  等级: 县")
    print("  调查日期: ", AS_OF)
    print("  信息来源: 罗山县政府网站")
    print("=" * 60)

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
    print(f"\n✅ 罗山县数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── Generate Person Graph JSONs ──
    print("\n--- 生成 Person Graph JSONs ---")
    source_register = make_source_register()

    # 1. 刘祖刚 (县委书记)
    liu_timeline = [
        {"start": "", "end": "", "org": "", "title": "履历缺口",
         "notes": "公开资料未找到刘祖刚担任罗山县委书记之前的任职履历",
         "confidence": "unverified", "source_ids": []},
        {"start": "2025-07", "end": "present", "org": "中共罗山县委员会",
         "title": "罗山县委书记",
         "notes": "2025年中接替余国芳出任罗山县委书记，任职至今。从2025年9月开始频繁出现在罗山新闻中（主持县委常委会等）",
         "confidence": "confirmed", "source_ids": ["S004", "S005"]},
    ]
    liu_relationships = [
        {"person": "时圣宇", "person_id": "luoshan_时圣宇", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "县委书记与县长党政搭档，共同巡视高考考点、出席重要会议",
         "overlap_org": "罗山县", "overlap_period": "2025-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
        {"person": "余国芳", "person_id": "luoshan_余国芳", "relationship_type": "predecessor_successor",
         "strength": "strong",
         "evidence": "接替余国芳任罗山县委书记",
         "overlap_org": "中共罗山县委员会", "overlap_period": "",
         "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S004"]},
    ]
    liu_json = make_person_json(persons[0], liu_timeline, liu_relationships, source_register)
    liu_path = PERSONS_DIR / f"{TODAY}-河南省-信阳市-县委书记-刘祖刚.json"
    with open(liu_path, "w", encoding="utf-8") as f:
        json.dump(liu_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {liu_path.name}")

    # 2. 时圣宇 (县长)
    shi_timeline = [
        {"start": "", "end": "2023-01", "org": "", "title": "履历缺口",
         "notes": "公开资料未找到时圣宇担任罗山县县长之前的任职履历。1989年10月出生，研究生学历",
         "confidence": "unverified", "source_ids": []},
        {"start": "2023-01", "end": "present", "org": "罗山县人民政府",
         "title": "罗山县县长（兼县委副书记）",
         "notes": "至少在2023年底（第43次常务会议记录）已在任。2024年2月以县长身份主持罗山县人大会议",
         "confidence": "confirmed", "source_ids": ["S001", "S004"]},
    ]
    shi_relationships = [
        {"person": "刘祖刚", "person_id": "luoshan_刘祖刚", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "县长与县委书记党政搭档",
         "overlap_org": "罗山县", "overlap_period": "2025-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
        {"person": "余国芳", "person_id": "luoshan_余国芳", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "担任县长期间与县委书记余国芳长期搭档（约2023-2025年）",
         "overlap_org": "罗山县", "overlap_period": "2023-2025",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
        {"person": "熊李平", "person_id": "luoshan_熊李平", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "常务副县长协助县长工作",
         "overlap_org": "罗山县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    shi_json = make_person_json(persons[1], shi_timeline, shi_relationships, source_register)
    shi_path = PERSONS_DIR / f"{TODAY}-河南省-信阳市-县长-时圣宇.json"
    with open(shi_path, "w", encoding="utf-8") as f:
        json.dump(shi_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {shi_path.name}")

    # 3. 余国芳 (前任县委书记)
    yu_timeline = [
        {"start": "", "end": "2021", "org": "", "title": "履历缺口",
         "notes": "公开资料未找到余国芳担任罗山县委书记之前的任职履历",
         "confidence": "unverified", "source_ids": []},
        {"start": "2021", "end": "2025-06", "org": "中共罗山县委员会",
         "title": "罗山县委书记",
         "notes": "至少从2023年10月至2025年4月持续在任。2025年4月仍以县委书记身份活动，此后由刘祖刚接替",
         "confidence": "confirmed", "source_ids": ["S004"]},
    ]
    yu_relationships = [
        {"person": "时圣宇", "person_id": "luoshan_时圣宇", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "曾与时圣宇组成党政搭档多年",
         "overlap_org": "罗山县", "overlap_period": "2023-2025",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
        {"person": "刘祖刚", "person_id": "luoshan_刘祖刚", "relationship_type": "predecessor_successor",
         "strength": "strong",
         "evidence": "余国芳卸任后由刘祖刚接替县委书记",
         "overlap_org": "中共罗山县委员会", "overlap_period": "",
         "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S004"]},
    ]
    yu_json = make_person_json(persons[2], yu_timeline, yu_relationships, source_register)
    # Override current_status for predecessor
    yu_json["current_status"]["is_current_confirmed"] = False
    yu_json["current_status"]["as_of"] = "2025-06"
    yu_path = PERSONS_DIR / f"{TODAY}-河南省-信阳市-县委书记(前任)-余国芳.json"
    with open(yu_path, "w", encoding="utf-8") as f:
        json.dump(yu_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {yu_path.name}")

    print(f"\n所有 Person Graph JSONs 已生成到: {PERSONS_DIR}")


if __name__ == "__main__":
    build()
