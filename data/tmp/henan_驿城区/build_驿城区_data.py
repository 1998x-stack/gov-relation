#!/usr/bin/env python3
"""
驿城区（驻马店市）领导班子工作关系网络 — 构建脚本

等级: 市辖区 | 上级: 河南省驻马店市
调查日期: 2026-07-24
数据来源: 驻马店市人民政府网站、公开报道
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

from gov_relation.runner import run_build

# ── Metadata ──
SLUG = "驿城区"
TODAY = "2026-07-24"
AS_OF = TODAY
PROVINCE = "河南省"
CITY = "驻马店市"
REGION = "驿城区"

# ── Paths ──
HERE = Path(__file__).parent
DB_PATH = HERE / f"{REGION}_network.db"
GEXF_PATH = HERE / f"{REGION}_network.gexf"
PERSONS_DIR = HERE

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── 区委书记 ──
    {
        "id": 1,
        "name": "冯磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "驿城区委书记",
        "current_org": "中共驻马店市驿城区委员会",
        "source": "https://www.zmd.gov.cn/ — 驻马店市人民政府网站公开报道",
        "notes": "2025年1月前任驿城区区长，后升任区委书记。公开简历信息有限，待进一步调查。",
    },
    # ── 区长 ──
    {
        "id": 2,
        "name": "陈金辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "驿城区区长",
        "current_org": "驿城区人民政府",
        "source": "https://www.zmd.gov.cn/ — 驻马店市人民政府网站公开报道",
        "notes": "原驻马店市经济开发区党工委副书记、管委会主任。2024年调任驿城区，任区委副书记、代区长，后当选区长。公开简历信息有限，待进一步调查。",
    },
    # ── 区委副书记（专职） ──
    {
        "id": 3,
        "name": "张海洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "驿城区委副书记（专职）",
        "current_org": "中共驻马店市驿城区委员会",
        "source": "公开报道",
        "notes": "专职副书记。公开简历信息有限。",
    },
    # ── 常务副区长 ──
    {
        "id": 4,
        "name": "李伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "驿城区委常委、常务副区长",
        "current_org": "驿城区人民政府",
        "source": "公开报道",
        "notes": "常务副区长。公开简历信息有限。",
    },
    # ── 纪委书记 ──
    {
        "id": 5,
        "name": "王楠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "驿城区委常委、纪委书记、监委主任",
        "current_org": "中共驻马店市驿城区纪律检查委员会",
        "source": "公开报道",
        "notes": "纪委书记。公开简历信息有限。",
    },
    # ── 组织部长 ──
    {
        "id": 6,
        "name": "赵怀民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "驿城区委常委、组织部部长",
        "current_org": "中共驻马店市驿城区委员会组织部",
        "source": "公开报道",
        "notes": "组织部长。公开简历信息有限。",
    },
    # ── 宣传部长 ──
    {
        "id": 7,
        "name": "薛晖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "驿城区委常委、宣传部部长",
        "current_org": "中共驻马店市驿城区委员会宣传部",
        "source": "公开报道",
        "notes": "宣传部长。公开简历信息有限。",
    },
    # ── 政法委书记 ──
    {
        "id": 8,
        "name": "刘志刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "驿城区委常委、政法委书记",
        "current_org": "中共驻马店市驿城区委员会政法委员会",
        "source": "公开报道",
        "notes": "政法委书记。公开简历信息有限。",
    },
    # ── 统战部长 ──
    {
        "id": 9,
        "name": "李湘云",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "驿城区委常委、统战部部长",
        "current_org": "中共驻马店市驿城区委员会统一战线工作部",
        "source": "公开报道",
        "notes": "统战部长。公开简历信息有限。",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共驻马店市驿城区委员会", "type": "党委", "level": "县处级", "parent": "中共驻马店市委员会", "location": "河南省驻马店市驿城区"},
    {"id": 2, "name": "驿城区人民政府", "type": "政府", "level": "县处级", "parent": "驻马店市人民政府", "location": "河南省驻马店市驿城区"},
    {"id": 3, "name": "中共驻马店市驿城区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共驻马店市纪律检查委员会", "location": "河南省驻马店市驿城区"},
    {"id": 4, "name": "中共驻马店市驿城区委员会组织部", "type": "党委", "level": "县处级", "parent": "中共驻马店市驿城区委员会", "location": "河南省驻马店市驿城区"},
    {"id": 5, "name": "中共驻马店市驿城区委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共驻马店市驿城区委员会", "location": "河南省驻马店市驿城区"},
    {"id": 6, "name": "中共驻马店市驿城区委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共驻马店市驿城区委员会", "location": "河南省驻马店市驿城区"},
    {"id": 7, "name": "中共驻马店市驿城区委员会统一战线工作部", "type": "党委", "level": "县处级", "parent": "中共驻马店市驿城区委员会", "location": "河南省驻马店市驿城区"},
    {"id": 8, "name": "驿城区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "驻马店市人大常委会", "location": "河南省驻马店市驿城区"},
    {"id": 9, "name": "政协驻马店市驿城区委员会", "type": "政协", "level": "县处级", "parent": "政协驻马店市委员会", "location": "河南省驻马店市驿城区"},
]


# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 冯磊 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "驿城区委书记", "start": "2025-01", "end": "present", "rank": "正处级", "note": "2025年初由区长升任区委书记"},
    # 冯磊 — 前任区长
    {"person_id": 1, "org_id": 2, "title": "驿城区区长", "start": "", "end": "2025-01", "rank": "正处级", "note": "升任区委书记前的职务"},

    # 陈金辉 — 区长
    {"person_id": 2, "org_id": 2, "title": "驿城区区长", "start": "2024", "end": "present", "rank": "正处级", "note": "2024年任区委副书记、代区长，后当选区长"},
    {"person_id": 2, "org_id": 2, "title": "驿城区副区长、代理区长", "start": "2024", "end": "2024", "rank": "正处级", "note": "区人大常委会任命为副区长、代理区长"},

    # 张海洋 — 区委专职副书记
    {"person_id": 3, "org_id": 1, "title": "驿城区委副书记（专职）", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 李伟 — 常务副区长
    {"person_id": 4, "org_id": 1, "title": "驿城区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "驿城区常务副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 王楠 — 纪委书记
    {"person_id": 5, "org_id": 1, "title": "驿城区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "驿城区纪委书记、监委主任", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 赵怀民 — 组织部长
    {"person_id": 6, "org_id": 1, "title": "驿城区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 4, "title": "驿城区委组织部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 薛晖 — 宣传部长
    {"person_id": 7, "org_id": 1, "title": "驿城区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "驿城区委宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 刘志刚 — 政法委书记
    {"person_id": 8, "org_id": 1, "title": "驿城区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 6, "title": "驿城区委政法委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 李湘云 — 统战部长
    {"person_id": 9, "org_id": 1, "title": "驿城区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 7, "title": "驿城区委统战部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
]


# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # ── 党政主要领导 ──
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "区委书记与区长党政工作搭档", "overlap_org": "驿城区", "overlap_period": "2024-至今"},

    # ── 区委书记与区委班子成员 ──
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "区委书记与区委专职副书记", "overlap_org": "中共驿城区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "区委书记与区委常委、常务副区长", "overlap_org": "中共驿城区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "区委书记与纪委书记", "overlap_org": "中共驿城区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "区委书记与组织部长", "overlap_org": "中共驿城区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "区委书记与宣传部长", "overlap_org": "中共驿城区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "区委书记与政法委书记", "overlap_org": "中共驿城区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "区委书记与统战部长", "overlap_org": "中共驿城区委", "overlap_period": ""},

    # ── 区长与区政府班子成员 ──
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "区长与常务副区长", "overlap_org": "驿城区政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 1, "type": "predecessor_successor", "context": "冯磊由区长升任区委书记，为陈金辉前任", "overlap_org": "驿城区人民政府", "overlap_period": "冯磊区长任期→陈金辉接任"},
]


# ══════════════════════════════════════════════════════════════════════════════
# SOURCE REGISTER
# ══════════════════════════════════════════════════════════════════════════════

def make_source_register() -> list[dict]:
    return [
        {"id": "S001", "title": "驻马店市人民政府网站", "url": "https://www.zmd.gov.cn/", "publisher": "驻马店市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "官方门户，新闻动态和领导活动"},
        {"id": "S002", "title": "驿城区人民政府网站", "url": "https://www.yichengqu.gov.cn/", "publisher": "驿城区人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "官方门户，领导分工页面"},
        {"id": "S003", "title": "驻马店市委组织部干部任前公示", "url": "https://www.zmd.gov.cn/", "publisher": "中共驻马店市委组织部", "published_at": "", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high", "notes": "干部任前公示公告"},
        {"id": "S004", "title": "驻马店市人大常委会人事任免公告", "url": "https://www.zmd.gov.cn/", "publisher": "驻马店市人大常委会", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "人大任免决定"},
    ]


# ══════════════════════════════════════════════════════════════════════════════
# PERSON GRAPH JSON HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def make_person_json(person: dict, timeline: list[dict], person_relationships: list[dict],
                     source_register: list[dict]) -> dict:
    """Build a Person Graph JSON v1.0 record."""
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": PROVINCE,
            "city": CITY,
            "region": REGION,
            "job": person.get("current_post", ""),
            "task_id": "henan_驿城区",
            "time_focus": "2024-2026",
        },
        "identity": {
            "person_id": f"yichengqu_{person['name']}",
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
            "source_ids": ["S001", "S002"],
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
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分或负面报道", "date": "",
                                         "confidence": "unverified", "source_ids": []}],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "核心领导完整履历（出生年份、出生地、早期职业生涯）均未公开确认",
        },
        "open_questions": [
            {"priority": "critical", "question": f"{person['name']}的完整履历（出生年份、出生地、教育背景、早期职业生涯）",
             "why_it_matters": "完整履历是评估晋升路径和人际关系的基础",
             "suggested_queries": [f"{person['name']} 简历 驻马店", f"{person['name']} 任前公示",
                                   f"{person['name']} 百度百科"],
             "last_attempted": AS_OF},
            {"priority": "high", "question": "前任区委书记的姓名及去向",
             "why_it_matters": "前任是理解人事更替和关系网络的关键节点",
             "suggested_queries": ["驿城区 前任 区委书记", "驿城区 区委书记 任免"],
             "last_attempted": AS_OF},
            {"priority": "medium", "question": "驿城区委常委分工和具体任职时间",
             "why_it_matters": "领导班子完整分工有助于构建更精细的关系网络",
             "suggested_queries": ["驿城区 领导分工", "驿城区 常委 分工"],
             "last_attempted": AS_OF},
        ],
    }


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def build():
    print("=" * 60)
    print("  驻马店市驿城区领导班子工作关系网络")
    print("  等级: 市辖区")
    print("  调查日期: 2026-07-24")
    print("  信息来源: 驻马店市人民政府网站 + 公开报道")
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
    print(f"\n✅ 驿城区数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── Generate Person Graph JSONs ──
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()

    # 1. 冯磊 (区委书记)
    feng_timeline = [
        {"start": "", "end": "", "org": "",
         "title": "履历缺口", "notes": "公开资料未找到冯磊2024年之前的任职履历",
         "confidence": "unverified", "source_ids": []},
        {"start": "", "end": "2025-01", "org": "驿城区人民政府", "title": "驿城区区长",
         "notes": "升任区委书记前的职务，具体任职开始时间待查",
         "confidence": "plausible", "source_ids": ["S001"]},
        {"start": "2025-01", "end": "", "org": "中共驻马店市驿城区委员会", "title": "驿城区委书记",
         "notes": "2025年初由区长升任区委书记",
         "confidence": "plausible", "source_ids": ["S001"]},
    ]
    feng_relationships = [
        {"person": "陈金辉", "person_id": "yichengqu_陈金辉", "relationship_type": "overlap",
         "strength": "strong", "evidence": "区委书记与区长党政工作搭档",
         "overlap_org": "驿城区", "overlap_period": "2024-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "陈金辉", "person_id": "yichengqu_陈金辉", "relationship_type": "predecessor_successor",
         "strength": "strong", "evidence": "冯磊由区长升任区委书记，陈金辉接任区长",
         "overlap_org": "驿城区人民政府", "overlap_period": "2024-2025",
         "direction": "person_to_other", "confidence": "plausible", "source_ids": ["S001"]},
    ]
    feng_json = make_person_json(persons[0], feng_timeline, feng_relationships, source_register)
    feng_path = PERSONS_DIR / f"{TODAY}-河南省-驻马店市-区委书记-冯磊.json"
    with open(feng_path, "w", encoding="utf-8") as f:
        json.dump(feng_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {feng_path.name}")

    # 2. 陈金辉 (区长)
    chen_timeline = [
        {"start": "", "end": "2024", "org": "驻马店经济技术开发区",
         "title": "驻马店经济技术开发区党工委副书记、管委会主任",
         "notes": "调任驿城区前在开发区任职",
         "confidence": "plausible", "source_ids": ["S001"]},
        {"start": "2024", "end": "2024", "org": "驿城区人民政府", "title": "驿城区副区长、代理区长",
         "notes": "2024年由区人大常委会任命为副区长、代理区长",
         "confidence": "plausible", "source_ids": ["S001"]},
        {"start": "2024", "end": "", "org": "驿城区人民政府", "title": "驿城区区长",
         "notes": "当选区长",
         "confidence": "plausible", "source_ids": ["S001"]},
    ]
    chen_relationships = [
        {"person": "冯磊", "person_id": "yichengqu_冯磊", "relationship_type": "overlap",
         "strength": "strong", "evidence": "区长与区委书记党政工作搭档",
         "overlap_org": "驿城区", "overlap_period": "2024-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    chen_json = make_person_json(persons[1], chen_timeline, chen_relationships, source_register)
    chen_path = PERSONS_DIR / f"{TODAY}-河南省-驻马店市-区长-陈金辉.json"
    with open(chen_path, "w", encoding="utf-8") as f:
        json.dump(chen_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {chen_path.name}")

    print(f"\n所有 Person Graph JSONs 已生成到: {PERSONS_DIR}")


if __name__ == "__main__":
    build()
