#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
藤县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 广西壮族自治区
Parent City: 梧州市
Region: 藤县
Targets: 县委书记 & 县长

数据来源:
- 藤县人民政府门户网站 (http://www.tengxian.gov.cn/) — 领导活动报道 (2026-07)
- "县委常委会召开会议 杨正沛主持" (2026-07-13)
- "杨正沛等县四家班子领导参加投票选举人大代表" (2026-07-22)
- "余强调研登革热防控及爱国卫生运动工作" (2026-07-21)
- "杨正沛督导检查登革热防控及爱国卫生运动工作" (2026-07-20)
- "杨正沛在藤县'两优一先'表彰大会上强调…" (2026-07-14)
- "杨正沛到塘步镇督导检查防汛备汛工作" (2026-07-13)
- "藤县召开近期重点工作视频调度会" (2026-07-20)
"""

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ── Ensure gov_relation is importable ──
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))

# ── Paths ──
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "藤县"
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-22"
TODAY = AS_OF

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：县委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "杨正沛",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "藤县县委书记",
        "current_org": "中共藤县委员会",
        "source": "confirmed — 藤县政府门户网站「县委常委会召开会议 杨正沛主持」(2026-07-13)、「杨正沛等县四家班子领导参加投票选举人大代表」(2026-07-22)、「杨正沛督导检查登革热防控及爱国卫生运动工作」(2026-07-20)、「杨正沛在藤县'两优一先'表彰大会上强调…」(2026-07-14)。来源: http://www.tengxian.gov.cn/",
    },
    # ════════════════════════════════════════
    # 县长（推测）
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "余强",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "藤县县委副书记、县长（推测）",
        "current_org": "藤县人民政府",
        "source": "plausible — 藤县政府门户网站「余强调研登革热防控及爱国卫生运动工作」(2026-07-21)。余强以独立调研身份出现，与杨正沛的督导检查形成书记/县长分工模式，推测余强为县长。需进一步确认来源: http://www.tengxian.gov.cn/",
    },
    # ════════════════════════════════════════
    # 县人大常委会主任（推测）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "待查（人大主任）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "藤县人大常委会主任",
        "current_org": "藤县人民代表大会常务委员会",
        "source": "unverified — 网站提及「县四家班子领导」，人大主任属四家班子之一，但姓名未在首页文章中出现。",
    },
    # ════════════════════════════════════════
    # 县政协主席（推测）
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "待查（政协主席）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "藤县政协主席",
        "current_org": "中国人民政治协商会议藤县委员会",
        "source": "unverified — 网站提及「县四家班子领导」，政协主席属四家班子之一，但姓名未在首页文章中出现。",
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共藤县委员会", "type": "党委", "level": "县", "parent": "中共梧州市委员会", "location": "梧州市藤县"},
    {"id": 2, "name": "藤县人民政府", "type": "政府", "level": "县", "parent": "梧州市人民政府", "location": "梧州市藤县"},
    {"id": 3, "name": "藤县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "梧州市人民代表大会常务委员会", "location": "梧州市藤县"},
    {"id": 4, "name": "中国人民政治协商会议藤县委员会", "type": "政协", "level": "县", "parent": "中国人民政治协商会议梧州市委员会", "location": "梧州市藤县"},
    {"id": 5, "name": "中共藤县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共梧州市纪律检查委员会", "location": "梧州市藤县"},
    {"id": 6, "name": "藤县监察委员会", "type": "政府", "level": "县", "parent": "梧州市监察委员会", "location": "梧州市藤县"},
    {"id": 7, "name": "中共藤县委员会组织部", "type": "党委", "level": "县", "parent": "中共藤县委员会", "location": "梧州市藤县"},
    {"id": 8, "name": "中共藤县委员会政法委员会", "type": "党委", "level": "县", "parent": "中共藤县委员会", "location": "梧州市藤县"},
    {"id": 9, "name": "中共藤县委员会宣传部", "type": "党委", "level": "县", "parent": "中共藤县委员会", "location": "梧州市藤县"},
    {"id": 10, "name": "藤县人民政府办公室", "type": "政府", "level": "县", "parent": "藤县人民政府", "location": "梧州市藤县"},
    {"id": 11, "name": "藤县发展和改革局", "type": "政府", "level": "县", "parent": "藤县人民政府", "location": "梧州市藤县"},
    {"id": 12, "name": "藤县公安局", "type": "政府", "level": "县", "parent": "藤县人民政府", "location": "梧州市藤县"},
    {"id": 13, "name": "藤县财政局", "type": "政府", "level": "县", "parent": "藤县人民政府", "location": "梧州市藤县"},
    {"id": 14, "name": "藤县农业农村局", "type": "政府", "level": "县", "parent": "藤县人民政府", "location": "梧州市藤县"},
    {"id": 15, "name": "藤县自然资源局", "type": "政府", "level": "县", "parent": "藤县人民政府", "location": "梧州市藤县"},
    {"id": 16, "name": "藤县水利局", "type": "政府", "level": "县", "parent": "藤县人民政府", "location": "梧州市藤县"},
    {"id": 17, "name": "藤县教育局", "type": "政府", "level": "县", "parent": "藤县人民政府", "location": "梧州市藤县"},
    {"id": 18, "name": "藤县住房建设和保障局", "type": "政府", "level": "县", "parent": "藤县人民政府", "location": "梧州市藤县"},
    {"id": 19, "name": "藤县交通运输局", "type": "政府", "level": "县", "parent": "藤县人民政府", "location": "梧州市藤县"},
]

# =========================================================================
# 3. POSITIONS (任职记录)
# =========================================================================
positions = [
    # 杨正沛
    {"person_id": 1, "org_id": 1, "title": "藤县县委书记", "start_date": "待查", "end_date": "至今", "rank": "县处级正职", "note": "2026年7月以县委书记身份公开活动"},
    # 余强
    {"person_id": 2, "org_id": 2, "title": "藤县县委副书记、县长（推测）", "start_date": "待查", "end_date": "至今", "rank": "县处级正职", "note": "2026年7月以领导身份调研；正式职务需确认"},
    # 人大主任（待确认姓名）
    {"person_id": 3, "org_id": 3, "title": "藤县人大常委会主任", "start_date": "待查", "end_date": "至今", "rank": "县处级正职", "note": "姓名待查"},
    # 政协主席（待确认姓名）
    {"person_id": 4, "org_id": 4, "title": "藤县政协主席", "start_date": "待查", "end_date": "至今", "rank": "县处级正职", "note": "姓名待查"},
]

# =========================================================================
# 4. RELATIONSHIPS (关系)
# =========================================================================
relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "杨正沛（县委书记）与余强（推测县长）的党政正职搭档关系。根据藤县政府网站2026年7月活动报道，两人同时出现在登革热防控工作中，分别以督导检查和调研形式分工，形成典型的书记/县长协作模式。",
        "overlap_org": "中共藤县委员会/藤县人民政府",
        "overlap_period": "2026年（推测）至今",
    },
]

# =========================================================================
# 5. BUILD
# =========================================================================
def build_database(db_path):
    """Create SQLite DB and insert all data."""
    conn = sqlite3.connect(str(db_path))
    try:
        # Create tables
        from gov_relation.schema import create_tables, insert_persons, insert_organizations, insert_positions, insert_relationships
        create_tables(conn, overwrite=True)
        insert_persons(conn, persons)
        insert_organizations(conn, organizations)
        insert_positions(conn, positions)
        insert_relationships(conn, relationships)
        print(f"DB ready: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")
    finally:
        conn.close()


def build_gexf(gexf_path):
    """Generate GEXF graph file."""
    from gov_relation.gexf import GEXFBuilder
    builder = GEXFBuilder(title=SLUG)
    for p in persons:
        builder.add_person(
            id=p["id"],
            name=p.get("name", ""),
            current_post=p.get("current_post", ""),
            current_org=p.get("current_org", ""),
            gender=p.get("gender", ""),
            ethnicity=p.get("ethnicity", ""),
            birth=p.get("birth", ""),
            source=p.get("source", ""),
        )
    for o in organizations:
        builder.add_organization(
            id=o["id"] + 100000,
            name=o.get("name", ""),
            org_type=o.get("type", ""),
            level=o.get("level", ""),
            location=o.get("location", ""),
        )
    for r in relationships:
        builder.add_relationship(
            source=r["person_a"],
            target=r["person_b"],
            rel_type=r.get("type", ""),
            context=r.get("context", ""),
            overlap_org=r.get("overlap_org", ""),
            overlap_period=r.get("overlap_period", ""),
        )
    builder.write(gexf_path)
    print(f"GEXF ready: {gexf_path}")


def build_person_json(person, filename):
    """Write a single person JSON file per reference schema."""
    output_path = PERSONS_DIR / filename
    person_id = f"guangxi_wuzhou_tengxian_{person['name']}".replace("(", "").replace(")", "")
    
    doc = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "梧州市",
            "region": "藤县",
            "job": person["current_post"],
            "task_id": "guangxi_藤县",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": person_id,
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", "待查"),
            "ethnicity": person.get("ethnicity", "待查"),
            "birth": person.get("birth", "待查"),
            "birthplace": person.get("birthplace", "待查"),
            "native_place": "待查",
            "education": [],
            "party_join": "中共党员",
            "work_start": "待查",
            "dedupe_keys": {
                "name_birth": f"{person['name']}_待查",
                "name_birthplace": f"{person['name']}_待查",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "县处级正职",
            "as_of": AS_OF,
            "is_current_confirmed": person["name"] not in ["待查（人大主任）", "待查（政协主席）"],
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "待查",
                "end": "至今",
                "org": person["current_org"],
                "title": person["current_post"],
                "level": "县处级正职",
                "location": "广西梧州市藤县",
                "system": "party" if "书记" in person["current_post"] else "government",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "2026年7月公开活动确认在任",
                "confidence": "confirmed" if person["name"] not in ["待查（人大主任）", "待查（政协主席）"] else "unverified",
                "source_ids": ["S001"]
            }
        ],
        "organizations": [
            {
                "org_name": person["current_org"],
                "org_type": "党委" if "委员会" in person["current_org"] and "人民" not in person["current_org"] else "政府" if "人民政府" in person["current_org"] else "人大" if "人民代表" in person["current_org"] else "政协",
                "level": "县"
            }
        ],
        "relationships": [
            {
                "person": "余强" if person["id"] == 1 else "杨正沛" if person["id"] == 2 else "待查",
                "person_id": "",
                "relationship_type": "superior_subordinate",
                "strength": "medium",
                "evidence": "同时在藤县2026年7月登革热防控工作中以各自角色出现",
                "overlap_org": "藤县",
                "overlap_period": "2026年",
                "direction": "undirected",
                "confidence": "plausible",
                "source_ids": ["S001"]
            }
        ] if person["id"] in [1, 2] else [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "公开履历不足，无法评估",
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
                "description": "截至2026年7月，公开渠道未发现该人员负面纪律或审计信息",
                "date": "2026-07-22",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "藤县人民政府门户网站 — 领导活动报道",
                "url": "http://www.tengxian.gov.cn/",
                "publisher": "藤县人民政府办公室",
                "published_at": "2026-07-22",
                "accessed_at": "2026-07-22",
                "source_type": "official",
                "reliability": "high",
                "notes": "网站首页新闻列表确认杨正沛为县委书记，余强为县级领导"
            }
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed" if person["name"] not in ["待查（人大主任）", "待查（政协主席）"] else "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "公开履历、出生日期、教育背景、完整任职经历均缺失；县长余强的正式职务名称和人大主任、政协主席姓名需确认"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的出生年月、籍贯、学历是什么？",
                "why_it_matters": "基础身份信息缺失，无法进行人物去重和履历分析",
                "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 出生", f"{person['name']} 广西"],
                "last_attempted": "2026-07-22"
            },
            {
                "priority": "critical",
                "question": f"{person['name']}的完整任职履历（历任职务及时间）是什么？",
                "why_it_matters": "无法构建职业轨迹和分析关系网络",
                "suggested_queries": [f"{person['name']} 任职", f"{person['name']} 工作经历"],
                "last_attempted": "2026-07-22"
            }
        ]
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {output_path}")


def main():
    print(f"=== 藤县数据构建 ({TODAY}) ===")
    
    # Run from staging directory
    os.chdir(str(STAGING_DIR))
    
    # 1. Database
    print("\n--- Building database ---")
    build_database(DB_PATH)
    
    # 2. GEXF
    print("\n--- Building GEXF ---")
    build_gexf(GEXF_PATH)
    
    # 3. Person JSONs
    print("\n--- Building person JSONs ---")
    # 杨正沛 — 县委书记
    build_person_json(persons[0], f"{TODAY}-广西壮族自治区-梧州市-县委书记-杨正沛.json")
    # 余强 — 县长（推测）
    build_person_json(persons[1], f"{TODAY}-广西壮族自治区-梧州市-县长-余强.json")
    
    print("\n=== Build complete ===")


if __name__ == "__main__":
    main()
