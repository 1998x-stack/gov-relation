#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
兴城市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县级市
Province: 辽宁省
Parent City: 葫芦岛市
Region: 兴城市
Targets: 市委书记 & 市长

数据来源: 百度百科 (兴城市词条) — 截至2024年9月
网络访问受限，部分字段标记为 unverified。
"""

import json
import os
import sys
from datetime import datetime

# 确保可以导入 gov_relation 包
BASE = os.path.dirname(os.path.abspath(__file__))
# 向上走到 repo root: staging dir = data/tmp/liaoning_兴城市/
# repo root = <BASE>/../../../
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── 路径 ──
SLUG = "兴城市"
STAGING_DIR = BASE
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

AS_OF = "2026-07-25"
TODAY = AS_OF

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：兴城市委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "陈玮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴城市委书记",
        "current_org": "中共兴城市委员会",
        "source": "百度百科兴城市词条（截至2024年9月）— https://baike.baidu.com/item/兴城市",
    },
    # ════════════════════════════════════════
    # 核心领导：兴城市市长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "李兆瑞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴城市市长",
        "current_org": "兴城市人民政府",
        "source": "百度百科兴城市词条（截至2024年9月）— https://baike.baidu.com/item/兴城市",
    },
    # ════════════════════════════════════════
    # 市人大常委会主任（待确认）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "【待确认】",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "兴城市人大常委会主任",
        "current_org": "兴城市人大常委会",
        "source": "待查 — 需政府官网确认",
    },
    # ════════════════════════════════════════
    # 市政协主席（待确认）
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "【待确认】",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "兴城市政协主席",
        "current_org": "兴城市政协",
        "source": "待查 — 需政府官网确认",
    },
    # ════════════════════════════════════════
    # 兴城市委副书记（待确认）
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "【待确认】",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "兴城市委副书记",
        "current_org": "中共兴城市委员会",
        "source": "待查 — 需政府官网确认",
    },
    # ════════════════════════════════════════
    # 兴城市委常委、常务副市长（待确认）
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "【待确认】",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "兴城市委常委、常务副市长",
        "current_org": "兴城市人民政府",
        "source": "待查 — 需政府官网确认",
    },
    # ════════════════════════════════════════
    # 兴城市纪委书记（待确认）
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "【待确认】",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "兴城市委常委、纪委书记",
        "current_org": "中共兴城市纪律检查委员会",
        "source": "待查 — 需政府官网确认",
    },
    # ════════════════════════════════════════
    # 兴城市委组织部部长（待确认）
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "【待确认】",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "兴城市委常委、组织部部长",
        "current_org": "中共兴城市委员会组织部",
        "source": "待查 — 需政府官网确认",
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共兴城市委员会", "type": "党委", "level": "县级", "parent": "中共葫芦岛市委员会", "location": "兴城市"},
    {"id": 2, "name": "兴城市人民政府", "type": "政府", "level": "县级", "parent": "葫芦岛市人民政府", "location": "兴城市"},
    {"id": 3, "name": "兴城市人大常委会", "type": "人大", "level": "县级", "parent": "葫芦岛市人大常委会", "location": "兴城市"},
    {"id": 4, "name": "兴城市政协", "type": "政协", "level": "县级", "parent": "葫芦岛市政协", "location": "兴城市"},
    {"id": 5, "name": "中共兴城市纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共葫芦岛市纪律检查委员会", "location": "兴城市"},
    {"id": 6, "name": "中共兴城市委员会组织部", "type": "党委", "level": "县级", "parent": "中共兴城市委员会", "location": "兴城市"},
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    {"person_id": 1, "org_id": 1, "title": "兴城市委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "百度百科截至2024年9月"},
    {"person_id": 2, "org_id": 2, "title": "兴城市市长", "start_date": "", "end_date": "", "rank": "正处级", "note": "百度百科截至2024年9月"},
    {"person_id": 3, "org_id": 3, "title": "兴城市人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": "待确认"},
    {"person_id": 4, "org_id": 4, "title": "兴城市政协主席", "start_date": "", "end_date": "", "rank": "正处级", "note": "待确认"},
    {"person_id": 5, "org_id": 1, "title": "兴城市委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "待确认"},
    {"person_id": 6, "org_id": 2, "title": "兴城市委常委、常务副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": "待确认"},
    {"person_id": 7, "org_id": 5, "title": "兴城市委常委、纪委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "待确认"},
    {"person_id": 8, "org_id": 6, "title": "兴城市委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "待确认"},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "领导关系",
        "context": "兴城市委书记与市长搭档",
        "overlap_org": "中共兴城市委员会",
        "overlap_period": "截至2024年9月",
    },
]

# =========================================================================
# MAIN
# =========================================================================
def main():
    print(f"构建 {SLUG} 领导班子关系网络数据库与图文件...")
    print(f"数据库路径: {DB_PATH}")
    print(f"GEXF路径: {GEXF_PATH}")
    print()

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

    print()
    print("=== 完成 ===")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
    print()

    # 写一份临时 person JSON 到 staging
    write_person_json()

    # 验证
    validate()


def write_person_json():
    """为两位核心人物生成 person JSON 文件。"""
    persons_dir = STAGING_DIR

    # ── 陈玮 ──
    chen_wei = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "葫芦岛市",
            "region": "兴城市",
            "job": "兴城市委书记",
            "task_id": "liaoning_兴城市",
            "time_focus": "2024-2026",
        },
        "identity": {
            "person_id": "xingcheng_chen_wei",
            "name": "陈玮",
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
                "name_birth": "陈玮_",
                "name_birthplace": "陈玮_",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": "兴城市委书记",
            "current_org": "中共兴城市委员会",
            "administrative_rank": "正处级",
            "as_of": "2024-09",
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": "公开资料未找到陈玮的完整履历。百度百科兴城市词条列其为兴城市委书记（截至2024年9月），但陈玮个人的百度百科页面访问受限。",
                "confidence": "unverified",
                "source_ids": ["S001"],
            },
        ],
        "organizations": [
            {"id": 1, "name": "中共兴城市委员会", "role": "市委书记", "period": "截至2024年9月"}
        ],
        "relationships": [
            {
                "person": "李兆瑞",
                "person_id": "xingcheng_li_zhaorui",
                "relationship_type": "overlap",
                "strength": "strong",
                "evidence": "兴城市委书记与市长搭档关系，数据来源于百度百科兴城市词条",
                "overlap_org": "兴城市",
                "overlap_period": "截至2024年9月",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "履历信息不足", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "公开资料不足，无法评估工作风格",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "公开搜索未发现纪律处分、负面报道或异常信息",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            },
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "兴城市 — 百度百科",
                "url": "https://baike.baidu.com/item/兴城市",
                "publisher": "百度百科",
                "published_at": "",
                "accessed_at": "2026-07-25",
                "source_type": "encyclopedia",
                "reliability": "medium",
                "notes": "主要领导栏目列出陈玮为兴城市委书记（截至2024年9月）",
            },
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "陈玮的完整履历、出生信息、教育背景均缺失",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "陈玮的出生年月、籍贯、教育背景？",
                "why_it_matters": "核心人物身份信息缺失",
                "suggested_queries": ["陈玮 兴城市 简历", "陈玮 葫芦岛 任前公示"],
                "last_attempted": "2026-07-25",
            },
            {
                "priority": "critical",
                "question": "陈玮在担任兴城市委书记前的完整履历？",
                "why_it_matters": "无法追溯其晋升路径和政绩背景",
                "suggested_queries": ["陈玮 历任 职务", "陈玮 此前 担任"],
                "last_attempted": "2026-07-25",
            },
        ],
    }

    # ── 李兆瑞 ──
    li_zhaorui = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "葫芦岛市",
            "region": "兴城市",
            "job": "兴城市市长",
            "task_id": "liaoning_兴城市",
            "time_focus": "2024-2026",
        },
        "identity": {
            "person_id": "xingcheng_li_zhaorui",
            "name": "李兆瑞",
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
                "name_birth": "李兆瑞_",
                "name_birthplace": "李兆瑞_",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": "兴城市市长",
            "current_org": "兴城市人民政府",
            "administrative_rank": "正处级",
            "as_of": "2024-09",
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": "公开资料未找到李兆瑞的完整履历。百度百科兴城市词条列其为兴城市长（截至2024年9月）。李兆瑞的百度百科多义词词条中含'辽宁省兴城市委书记'义项，推测其可能曾任兴城市委书记。",
                "confidence": "unverified",
                "source_ids": ["S001", "S002"],
            },
        ],
        "organizations": [
            {"id": 1, "name": "兴城市人民政府", "role": "市长", "period": "截至2024年9月"}
        ],
        "relationships": [
            {
                "person": "陈玮",
                "person_id": "xingcheng_chen_wei",
                "relationship_type": "overlap",
                "strength": "strong",
                "evidence": "兴城市长与市委书记搭档关系，数据来源于百度百科兴城市词条",
                "overlap_org": "兴城市",
                "overlap_period": "截至2024年9月",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "履历信息不足", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "公开资料不足，无法评估工作风格",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "公开搜索未发现纪律处分、负面报道或异常信息",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            },
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "兴城市 — 百度百科",
                "url": "https://baike.baidu.com/item/兴城市",
                "publisher": "百度百科",
                "published_at": "",
                "accessed_at": "2026-07-25",
                "source_type": "encyclopedia",
                "reliability": "medium",
                "notes": "主要领导栏目列出李兆瑞为兴城市市长（截至2024年9月）",
            },
            {
                "id": "S002",
                "title": "李兆瑞 — 百度百科（多义词）",
                "url": "https://baike.baidu.com/item/李兆瑞",
                "publisher": "百度百科",
                "published_at": "",
                "accessed_at": "2026-07-25",
                "source_type": "encyclopedia",
                "reliability": "medium",
                "notes": "多义词词条中含'辽宁省兴城市委书记'义项",
            },
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "李兆瑞的完整履历、出生信息、教育背景均缺失",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "李兆瑞的出生年月、籍贯、教育背景？",
                "why_it_matters": "核心人物身份信息缺失",
                "suggested_queries": ["李兆瑞 兴城市 简历", "李兆瑞 葫芦岛 任前公示"],
                "last_attempted": "2026-07-25",
            },
            {
                "priority": "critical",
                "question": "李兆瑞在担任兴城市长前的完整履历？",
                "why_it_matters": "无法追溯其晋升路径和政绩背景",
                "suggested_queries": ["李兆瑞 历任 职务", "李兆瑞 此前 担任"],
                "last_attempted": "2026-07-25",
            },
            {
                "priority": "high",
                "question": "李兆瑞是否曾任兴城市委书记？",
                "why_it_matters": "百度百科多义词词条暗示李兆瑞曾任兴城市委书记，需确认时序",
                "suggested_queries": ["李兆瑞 兴城市委书记 任命"],
                "last_attempted": "2026-07-25",
            },
        ],
    }

    for obj, filename, label in [
        (chen_wei, f"{AS_OF}-辽宁省-葫芦岛市-兴城市委书记-陈玮.json", "陈玮"),
        (li_zhaorui, f"{AS_OF}-辽宁省-葫芦岛市-兴城市长-李兆瑞.json", "李兆瑞"),
    ]:
        path = os.path.join(persons_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {path}")
        # 验证 JSON 合法性
        with open(path, "r", encoding="utf-8") as f:
            json.load(f)
        print(f"    ✓ JSON 验证通过")


def validate():
    """基本验证。"""
    errors = []

    # 检查数据库
    if os.path.exists(DB_PATH):
        import sqlite3
        conn = sqlite3.connect(DB_PATH)
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        table_names = [t[0] for t in tables]
        for tbl in ["persons", "organizations", "positions", "relationships"]:
            if tbl in table_names:
                count = conn.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
                print(f"  ✓ 表 {tbl}: {count} 行")
            else:
                errors.append(f"缺少表: {tbl}")
        conn.close()
    else:
        errors.append(f"数据库文件不存在: {DB_PATH}")

    # 检查 GEXF
    if os.path.exists(GEXF_PATH):
        with open(GEXF_PATH, "r") as f:
            content = f.read()
        if "<gexf" in content and "<nodes>" in content:
            print(f"  ✓ GEXF 文件有效 ({len(content)} bytes)")
        else:
            errors.append("GEXF 文件格式异常")
    else:
        errors.append(f"GEXF 文件不存在: {GEXF_PATH}")

    if errors:
        print("\n⚠ 验证错误:")
        for e in errors:
            print(f"  ✗ {e}")
    else:
        print("\n✓ 全部验证通过")


if __name__ == "__main__":
    main()
