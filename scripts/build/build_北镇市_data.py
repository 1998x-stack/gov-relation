#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
北镇市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县级市
Province: 辽宁省
Parent City: 锦州市
Region: 北镇市
Targets: 市委书记 & 市长

数据来源: 本次调研网络全访问路劣化（Exa 限流、百度和 Br/Google/r.jina.ai 超时、
beizhen.gov.cn 传输错误），北镇市核心领导姓名与履历未能从实时来源核验。
故采用「structurally valid artifacts + 显式不确定性」模式：
- 领导班子职位框架已按锦州市代管县级市标准构建立体结构；
- 核心领导职位（市委书记、市长）以「待查」占位，biography 字段留空；
- 已确认事实仅限 parent_city（锦州市）现职框架，源自本仓库既有可信产物。
所有偏差已在字段与 report/open_gaps.md 中显式标注。
"""

import json
import os
import sys
from datetime import datetime

# 确保可以导入 gov_relation 包
BASE = os.path.dirname(os.path.abspath(__file__))
# 向上查找 repo root（包含 gov_relation 包的目录），此脚本可能在 data/tmp/ 或 scripts/build/ 两处运行
_candidate = BASE
while True:
    if os.path.isdir(os.path.join(_candidate, "gov_relation")):
        break
    parent = os.path.abspath(os.path.join(_candidate, ".."))
    if parent == _candidate:
        raise RuntimeError("无法定位包含 gov_relation 包的仓库根目录")
    _candidate = parent
REPO_ROOT = _candidate
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── 路径 ──
SLUG = "北镇市"
STAGING_DIR = BASE
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

AS_OF = "2026-08-06"
TODAY = AS_OF

# =========================================================================
# 1. PERSONS
# =========================================================================
# 核心领导（市委书记 / 市长）因本次网络关闭无法确认姓名，采取「待查」占位，
# 与仓库内既有多区域产物（如 xxx-锦州市-区委书记-待查.json）的约定一致。
persons = [
    # ════════════════════════════════════════
    # 核心领导：北镇市市委书记（待查）
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "【待确认】北镇市委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员（职级内默认）",
        "work_start": "",
        "current_post": "北镇市委书记",
        "current_org": "中共北镇市委员会",
        "source": "待查 — 网络全路劣化，无法确认现任书记姓名；需锦州市委组织部任前公示或北镇市政府官网领导之窗确认",
    },
    # ════════════════════════════════════════
    # 核心领导：北镇市委副书记、市长（待查）
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "待确认（北镇市长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员（职级内默认）",
        "work_start": "",
        "current_post": "北镇市委副书记、市长",
        "current_org": "北镇市人民政府",
        "source": "待查 — 网络全路关闭，无法确认现任市长姓名；需北镇市政府官网领导分工或人大任命公告确认",
    },
    # ════════════════════════════════════════
    # 市委副书记（待确认）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "待确认（市委副书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "北镇市委副书记",
        "current_org": "中共北镇市委员会",
        "source": "待查 — 需政府官网确认",
    },
    # ════════════════════════════════════════
    # 市人大常委会主任（待确认）
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "待确认（市人大主任）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "北镇市人大常委会主任",
        "current_org": "北镇市人大常委会",
        "source": "待查 — 需政府官网确认",
    },
    # ════════════════════════════════════════
    # 市政协主席（待确认）
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "待确认（市政协主席）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "北镇市政协主席",
        "current_org": "北镇市政协",
        "source": "待查 — 需政府官网确认",
    },
    # ════════════════════════════════════════
    # 北镇市委常委、常务副市长（待确认）
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "待确认（常务副市长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "北镇市委常委、常务副市长",
        "current_org": "北镇市人民政府",
        "source": "待查 — 需政府官网确认",
    },
    # ════════════════════════════════════════
    # 北镇市纪委书记（待确认）
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "待确认（市纪委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "北镇市委常委、纪委书记",
        "current_org": "中共北镇市纪律检查委员会",
        "source": "待查 — 需政府官网确认",
    },
    # ════════════════════════════════════════
    # 北镇市委组织部部长（待确认）
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "待确认（组织部部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "北镇市委常委、组织部部长",
        "current_org": "中共北镇市委员会组织部",
        "source": "待查 — 需政府官网确认",
    },
    # ════════════════════════════════════════
    # 北镇市委宣传部部长（待确认）
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "待确认（宣传部部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "北镇市委常委、宣传部部长",
        "current_org": "中共北镇市委员会宣传部",
        "source": "待查 — 需政府官网确认",
    },
    # ════════════════════════════════════════
    # 北镇市委政法委书记（待确认）
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "待确认（政法委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "北镇市委常委、政法委书记",
        "current_org": "中共北镇市委员会政法委员会",
        "source": "待查 — 需政府官网确认",
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共北镇市委员会", "type": "党委", "level": "县级", "parent": "中共锦州市委员会", "location": "北镇市"},
    {"id": 2, "name": "北镇市人民政府", "type": "政府", "level": "县级", "parent": "锦州市人民政府", "location": "北镇市"},
    {"id": 3, "name": "北镇市人大常委会", "type": "人大", "level": "县级", "parent": "锦州市人大常委会", "location": "北镇市"},
    {"id": 4, "name": "北镇市政协", "type": "政协", "level": "县级", "parent": "锦州市政协", "location": "北镇市"},
    {"id": 5, "name": "中共北镇市纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共锦州市纪律检查委员会", "location": "北镇市"},
    {"id": 6, "name": "中共北镇市委员会组织部", "type": "党委", "level": "县级", "parent": "中共北镇市委员会", "location": "北镇市"},
    {"id": 7, "name": "中共北镇市委员会宣传部", "type": "党委", "level": "县级", "parent": "中共北镇市委员会", "location": "北镇市"},
    {"id": 8, "name": "中共北镇市委员会政法委员会", "type": "党委", "level": "县级", "parent": "中共北镇市委员会", "location": "北镇市"},
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    {"person_id": 1, "org_id": 1, "title": "北镇市委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "待查 — 网络关闭无法确认姓名"},
    {"person_id": 2, "org_id": 2, "title": "北镇市委副书记、市长", "start_date": "", "end_date": "", "rank": "正处级", "note": "待查 — 网络关闭无法确认姓名"},
    {"person_id": 3, "org_id": 1, "title": "北镇市委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "待查"},
    {"person_id": 4, "org_id": 3, "title": "北镇市人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": "待查"},
    {"person_id": 5, "org_id": 4, "title": "北镇市政协主席", "start_date": "", "end_date": "", "rank": "正处级", "note": "待查"},
    {"person_id": 6, "org_id": 2, "title": "北镇市委常委、常务副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": "待查"},
    {"person_id": 7, "org_id": 5, "title": "北镇市委常委、纪委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "待查"},
    {"person_id": 8, "org_id": 6, "title": "北镇市委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "待查"},
    {"person_id": 9, "org_id": 7, "title": "北镇市委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "待查"},
    {"person_id": 10, "org_id": 8, "title": "北镇市委常委、政法委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "待查"},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
# 市委书记与市长是北镇市领导班子的「一把手-二把手」搭档关系，
# 此关系为结构性事实，不依赖具体姓名，可在姓名确认后补充动力序与 overlap_period。
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "领导关系",
        "context": "北镇市委书记与市长同属北镇市领导班子核心搭档（一把手-二把手结构）",
        "overlap_org": "中共北镇市委员会",
        "overlap_period": "待确认（现任领导班子在任期）",
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

    # 写 person JSON 到 staging
    write_person_json()

    validate()


def write_person_json():
    """为两个核心职位生成 person JSON 文件（以「待查」占位，姓名确认后替换）。"""
    persons_dir = STAGING_DIR

    # ── 市委书记（待查）──
    shuji = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "锦州市",
            "region": "北镇市",
            "job": "市委书记",
            "task_id": "liaoning_北镇市",
            "time_focus": "2024-2026",
        },
        "identity": {
            "person_id": "beizhen_shuji_unconfirmed",
            "name": "待确认（北镇市委书记）",
            "aliases": [],
            "gender": "",
            "ethnicity": "",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "待确认_",
                "name_birthplace": "待确认_",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": "北镇市委书记",
            "current_org": "中共北镇市委员会",
            "administrative_rank": "正处级",
            "as_of": "",
            "is_current_confirmed": False,
            "source_ids": [],
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": "本次调研网络全路由关闭（Exa 限流、百度/必应/Google/r.jina.ai 超时、beizhen.gov.cn 不可达），无法确认现任北镇市委书记姓名，更无法获取其履历。需锦州市委组织部任前公示或北镇市政府官网领导之窗确认。",
                "confidence": "unverified",
                "source_ids": [],
            },
        ],
        "organizations": [
            {"id": 1, "name": "中共北镇市委员会", "role": "市委书记", "period": "未知（待确认）"}
        ],
        "relationships": [],
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
                "description": "未发现任何可核验信号（因网络关闭无法进行公开搜索搜证）",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            },
        ],
        "source_register": [],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "现任北镇市委书记姓名及全部履历均未确认",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "现任北镇市委书记姓名、出生年月、籍贯、教育背景、入党时间、参加工作时间？",
                "why_it_matters": "任务核心目标（一把手）信息完全缺失，网络恢复后必须补全",
                "suggested_queries": ["北镇市 市委书记 任前公示", "北镇市 领导之窗 市委书记", "site:beizhen.gov.cn 市委书记"],
                "last_attempted": "2026-08-06",
            },
            {
                "priority": "critical",
                "question": "现任北镇市委书记在履任前担任什么职务，晋升路径？",
                "why_it_matters": "无法追溯其治绩与提拔背景",
                "suggested_queries": ["北镇市 市委书记 简历", "北镇 书记 此前 担任"],
                "last_attempted": "2026-08-06",
            },
        ],
    }

    # ── 市长（待查）──
    shizhang = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "锦州市",
            "region": "北镇市",
            "job": "市长",
            "task_id": "liaoning_北镇市",
            "time_focus": "2024-2026",
        },
        "identity": {
            "person_id": "beizhen_shizhang_unconfirmed",
            "name": "待确认（北镇市长）",
            "aliases": [],
            "gender": "",
            "ethnicity": "",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "待确认_",
                "name_birthplace": "待确认_",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": "北镇市委副书记、市长",
            "current_org": "北镇市人民政府",
            "administrative_rank": "正处级",
            "as_of": "",
            "is_current_confirmed": False,
            "source_ids": [],
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": "本次调研网络全出口关闭，无法录入现任北镇市长姓名及履历。需北镇市人民政府官网领导分工或锦州市人大任命公告确认。",
                "confidence": "unverified",
                "source_ids": [],
            },
        ],
        "organizations": [
            {"id": 2, "name": "北镇市人民政府", "role": "市长", "period": "未知（待确认）"}
        ],
        "relationships": [],
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
                "description": "未发现任何可核验信号（因网络不可访问无法搜证）",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            },
        ],
        "source_register": [],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "现任北镇市长姓名及全部履历均未确认",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "现任北镇市长姓名、出生年月、籍贯、教育背景、入党时间、参加工作时间？",
                "why_it_matters": "任务核心目标（二把手）信息缺失，网络无法执行必须补全",
                "suggested_queries": ["北镇市 市长 任前公示", "北镇市 政府 领导分工 市长", "北镇 市长 人大任命"],
                "last_attempted": "2026-08-06",
            },
            {
                "priority": "critical",
                "question": "现任市长在担任北镇市长前的完整履历？",
                "why_it_matters": "无法追溯其治绩与晋升路径",
                "suggested_queries": ["北镇市 市长 简历", "北镇 市长 此前 担任"],
                "last_attempted": "2026-08-06",
            },
        ],
    }

    for obj, filename, label in [
        (shuji, f"{AS_OF}-辽宁省-锦州市-市委书记-待确认.json", "市委书记（待确认）"),
        (shizhang, f"{AS_OF}-辽宁省-锦州市-市长-待确认.json", "市长（待确认）"),
    ]:
        path = os.path.join(persons_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {path}")
        with open(path, "r", encoding="utf-8") as f:
            json.load(f)
        print(f"    ✓ JSON 验证通过")


def validate():
    errors = []

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

    if os.path.exists(GEXF_PATH):
        with open(GEXF_PATH, "r", encoding="utf-8") as f:
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
        sys.exit(1)
    else:
        print("\n✓ 全部验证通过")


if __name__ == "__main__":
    main()