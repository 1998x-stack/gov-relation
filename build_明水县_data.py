#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 明水县 (Mingshui County), 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_明水县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - www.mingshui.gov.cn (明水县人民政府官网) — confirmed as-of 2026-07-24
    - 马福 (县委书记): confirmed via multiple news articles ("县委书记马福")
    - 邓吉喆 (县长): confirmed via news ("县委副书记、县长邓吉喆")
  - mp.weixin.qq.com — 明水发布 official WeChat account (primary news distribution channel)

Confidence notes:
  - 马福 (县委书记): confirmed via official government news (县委书记马福); detailed career history unverified
  - 邓吉喆 (县委副书记、县长): confirmed via official government news; detailed career history unverified
  - 王玉林 (县委常委、副县长): confirmed via news mention
  - 李艳昌 (副县长): confirmed via news mention
  - 徐建、谢俊杰、刘春霞 (县领导): mentioned in news but exact titles unverified
  - Full party committee roster (副书记、纪委书记、组织部长等): unverified — leadership page not accessible
  - Career histories for all leaders: unverified — only current names and titles confirmed
  - Exa search was rate-limited; Baidu returned CAPTCHA; Jina reader transport errors
  - Official leadership page (ldxx/) returned 403; government site uses dynamic navigation
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "明水县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "马福",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共明水县委员会",
        "source": "https://mp.weixin.qq.com/s/dJnWmq4jbiihr62U2Enkdg"
    },
    {
        "id": 2,
        "name": "邓吉喆",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县长",
        "current_org": "明水县人民政府",
        "source": "https://mp.weixin.qq.com/s/8mUUy1kkvarN7gRyi8z8wA"
    },
    # ═══════ 县委常委/副县长 ═══════
    {
        "id": 3,
        "name": "王玉林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "明水县人民政府",
        "source": "https://mp.weixin.qq.com/s/8mUUy1kkvarN7gRyi8z8wA"
    },
    {
        "id": 4,
        "name": "李艳昌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "明水县人民政府",
        "source": "https://mp.weixin.qq.com/s/8mUUy1kkvarN7gRyi8z8wA"
    },
    {
        "id": 5,
        "name": "徐建",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "明水县人民政府",
        "source": "https://mp.weixin.qq.com/s/dJnWmq4jbiihr62U2Enkdg"
    },
    {
        "id": 6,
        "name": "谢俊杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "明水县人民政府",
        "source": "https://mp.weixin.qq.com/s/dJnWmq4jbiihr62U2Enkdg"
    },
    {
        "id": 7,
        "name": "刘春霞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "明水县人民政府",
        "source": "https://mp.weixin.qq.com/s/dJnWmq4jbiihr62U2Enkdg"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共明水县委员会", "type": "党委", "level": "县级", "parent": "中共绥化市委员会", "location": "明水县"},
    {"id": 2, "name": "明水县人民政府", "type": "政府", "level": "县级", "parent": "绥化市人民政府", "location": "明水县"},
]

# ── Positions (person → org with title) ────────────────────────────────────
positions = [
    # 马福
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 邓吉喆
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "", "rank": "正处级", "note": "县委副书记、县长，主持县政府全面工作"},
    # 王玉林
    {"person_id": 3, "org_id": 2, "title": "县委常委、副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 李艳昌
    {"person_id": 4, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 徐建
    {"person_id": 5, "org_id": 2, "title": "县领导", "start_date": "", "end_date": "", "rank": "", "note": "具体职务待确认"},
    # 谢俊杰
    {"person_id": 6, "org_id": 2, "title": "县领导", "start_date": "", "end_date": "", "rank": "", "note": "具体职务待确认"},
    # 刘春霞
    {"person_id": 7, "org_id": 2, "title": "县领导", "start_date": "", "end_date": "", "rank": "", "note": "具体职务待确认"},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 马福 ↔ 邓吉喆（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "马福任县委书记，邓吉喆任县长，为明水县党政正职搭档", "overlap_org": "明水县", "overlap_period": ""},
    # 邓吉喆 ↔ 王玉林（政府班子）
    {"person_a": 2, "person_b": 3, "type": "政府班子", "context": "王玉林任县委常委、副县长，邓吉喆为县长", "overlap_org": "明水县人民政府", "overlap_period": ""},
    # 邓吉喆 ↔ 李艳昌（政府班子）
    {"person_a": 2, "person_b": 4, "type": "政府班子", "context": "李艳昌任副县长，邓吉喆为县长", "overlap_org": "明水县人民政府", "overlap_period": ""},
    # 邓吉喆 ↔ 徐建（政府班子）
    {"person_a": 2, "person_b": 5, "type": "政府班子", "context": "徐建参加县长主持的经济运行分析会议，为县政府班子成员", "overlap_org": "明水县人民政府", "overlap_period": ""},
    # 邓吉喆 ↔ 谢俊杰（政府班子）
    {"person_a": 2, "person_b": 6, "type": "政府班子", "context": "谢俊杰参加县长主持的专项调研陪同活动", "overlap_org": "明水县人民政府", "overlap_period": ""},
    # 马福 ↔ 徐建（县委班子）
    {"person_a": 1, "person_b": 5, "type": "县委班子", "context": "徐建陪同县委书记马福开展民政领域专项调研", "overlap_org": "明水县", "overlap_period": ""},
    # 马福 ↔ 谢俊杰（县委班子）
    {"person_a": 1, "person_b": 6, "type": "县委班子", "context": "谢俊杰陪同县委书记马福开展民政领域专项调研", "overlap_org": "明水县", "overlap_period": ""},
    # 马福 ↔ 刘春霞（县委班子）
    {"person_a": 1, "person_b": 7, "type": "县委班子", "context": "刘春霞陪同县委书记马福开展民政领域专项调研", "overlap_org": "明水县", "overlap_period": ""},
]

# ── Main ────────────────────────────────────────────────────────────────────
def main() -> None:
    sys.path.insert(0, str(BASE))
    from gov_relation.runner import run_build

    # Write DB+GEXF to staging
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

    # Write person JSON files
    person_files = [
        {
            "id": 1,
            "name": "马福",
            "job": "县委书记",
            "data": {
                "schema_version": "1.0",
                "generated_at": AS_OF,
                "investigation_scope": {
                    "province": "黑龙江省",
                    "city": "绥化市",
                    "region": "明水县",
                    "job": "县委书记",
                    "task_id": "heilongjiang_明水县",
                    "time_focus": "2026"
                },
                "identity": {
                    "person_id": "mingshui_mafu",
                    "name": "马福",
                },
                "current_status": {
                    "current_post": "县委书记",
                    "current_org": "中共明水县委员会",
                    "administrative_rank": "正处级",
                    "as_of": AS_OF,
                    "is_current_confirmed": True,
                    "source_ids": ["S001"]
                },
                "career_timeline": [],
                "organizations": [],
                "relationships": [
                    {
                        "person": "邓吉喆",
                        "person_id": "mingshui_dengjizhe",
                        "relationship_type": "overlap",
                        "strength": "strong",
                        "evidence": "马福任县委书记，邓吉喆任县长，为明水县党政正职搭档",
                        "overlap_org": "明水县",
                        "confidence": "confirmed",
                        "source_ids": ["S001", "S002"]
                    }
                ],
                "governance_record": [
                    {
                        "period": "2026-07",
                        "domain": "livelihood",
                        "achievement_or_event": "带队开展民政领域专项调研，强调养老服务、民生保障、惠民政策落实",
                        "role_in_event": "调研带队",
                        "location": "明水县",
                        "confidence": "confirmed",
                        "source_ids": ["S001"]
                    }
                ],
                "professional_profile": {
                    "primary_specializations": [],
                    "secondary_specializations": [],
                    "career_pattern": "unknown",
                    "systems_experience": [],
                    "geographic_pattern": [],
                    "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
                },
                "work_style_and_personality": {
                    "public_style_indicators": [
                        {
                            "trait": "grassroots_oriented",
                            "evidence": "深入民政领域专项调研，聚焦养老服务和民生保障，强调补短板、强弱项、提质效",
                            "confidence": "plausible",
                            "source_ids": ["S001"]
                        }
                    ],
                    "speech_themes": ["以人民为中心", "养老服务", "民生保障", "社区养老"],
                    "management_signals": ["强调部门协同联动", "四个体系闭环落实"],
                    "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
                },
                "risk_and_integrity_signals": [
                    {"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified"}
                ],
                "source_register": [
                    {"id": "S001", "title": "县委书记马福深入民政领域开展专项调研", "url": "https://mp.weixin.qq.com/s/dJnWmq4jbiihr62U2Enkdg", "publisher": "明水发布（明水县人民政府）", "published_at": "2026-07-20", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认县委书记职务"},
                    {"id": "S002", "title": "县委副书记、县长邓吉喆主持召开全县经济运行分析会议", "url": "https://mp.weixin.qq.com/s/8mUUy1kkvarN7gRyi8z8wA", "publisher": "明水发布（明水县人民政府）", "published_at": "2026-07-20", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认县长职务及党政搭档关系"}
                ],
                "confidence_summary": {
                    "identity": "plausible",
                    "current_role": "confirmed",
                    "career_completeness": "thin",
                    "relationship_confidence": "medium",
                    "biggest_gap": "马福的完整履历（出生年份、籍贯、教育背景、晋升路径）未找到"
                },
                "open_questions": [
                    {
                        "priority": "critical",
                        "question": "马福的完整履历是什么？出生年份、籍贯、教育背景、工作经历？",
                        "why_it_matters": "作为当前一把手，其职业背景对理解政治网络至关重要",
                        "suggested_queries": ["马福 简历 明水 县委书记", "马福 任前公示 绥化"],
                        "last_attempted": AS_OF
                    },
                    {
                        "priority": "high",
                        "question": "马福何时调任明水县委书记？前任是谁？来自哪个岗位？",
                        "why_it_matters": "了解县委书记交接历史和政治网络变化",
                        "suggested_queries": ["明水县 前任 县委书记", "明水县 县委 书记 任职时间", "马福 绥化 任职"],
                        "last_attempted": AS_OF
                    }
                ]
            }
        },
        {
            "id": 2,
            "name": "邓吉喆",
            "job": "县长",
            "data": {
                "schema_version": "1.0",
                "generated_at": AS_OF,
                "investigation_scope": {
                    "province": "黑龙江省",
                    "city": "绥化市",
                    "region": "明水县",
                    "job": "县长",
                    "task_id": "heilongjiang_明水县",
                    "time_focus": "2026"
                },
                "identity": {
                    "person_id": "mingshui_dengjizhe",
                    "name": "邓吉喆",
                },
                "current_status": {
                    "current_post": "县长",
                    "current_org": "明水县人民政府",
                    "administrative_rank": "正处级",
                    "as_of": AS_OF,
                    "is_current_confirmed": True,
                    "source_ids": ["S002"]
                },
                "career_timeline": [],
                "organizations": [],
                "relationships": [
                    {
                        "person": "马福",
                        "person_id": "mingshui_mafu",
                        "relationship_type": "overlap",
                        "strength": "strong",
                        "evidence": "邓吉喆任县长，马福任县委书记，为明水县党政正职搭档",
                        "overlap_org": "明水县",
                        "confidence": "confirmed",
                        "source_ids": ["S001", "S002"]
                    },
                    {
                        "person": "王玉林",
                        "person_id": "mingshui_wangyulin",
                        "relationship_type": "overlap",
                        "strength": "medium",
                        "evidence": "邓吉喆任县长，王玉林任县委常委、副县长，参加经济运行分析会议",
                        "overlap_org": "明水县人民政府",
                        "confidence": "confirmed",
                        "source_ids": ["S002"]
                    },
                    {
                        "person": "李艳昌",
                        "person_id": "mingshui_liyanchang",
                        "relationship_type": "overlap",
                        "strength": "medium",
                        "evidence": "邓吉喆任县长，李艳昌任副县长，参加经济运行分析会议",
                        "overlap_org": "明水县人民政府",
                        "confidence": "confirmed",
                        "source_ids": ["S002"]
                    }
                ],
                "governance_record": [
                    {
                        "period": "2026-07",
                        "domain": "economic_development",
                        "achievement_or_event": "主持召开全县经济运行分析会议，全面复盘上半年经济指标，部署下半年稳增长工作",
                        "role_in_event": "主持",
                        "location": "明水县",
                        "confidence": "confirmed",
                        "source_ids": ["S002"]
                    }
                ],
                "professional_profile": {
                    "primary_specializations": ["经济管理", "政府工作"],
                    "secondary_specializations": [],
                    "career_pattern": "unknown",
                    "systems_experience": ["政府"],
                    "geographic_pattern": [],
                    "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
                },
                "work_style_and_personality": {
                    "public_style_indicators": [
                        {
                            "trait": "pragmatic",
                            "evidence": "主持召开经济运行分析会议，强调锚定全年目标、补齐缺口、稳增长，体现务实经济管理风格",
                            "confidence": "plausible",
                            "source_ids": ["S002"]
                        }
                    ],
                    "speech_themes": ["稳增长", "补齐短板", "招商引资", "安全生产"],
                    "management_signals": ["强调部门协同和数据会商", "严格督导问效"],
                    "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
                },
                "risk_and_integrity_signals": [
                    {"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified"}
                ],
                "source_register": [
                    {"id": "S002", "title": "县委副书记、县长邓吉喆主持召开全县经济运行分析会议", "url": "https://mp.weixin.qq.com/s/8mUUy1kkvarN7gRyi8z8wA", "publisher": "明水发布（明水县人民政府）", "published_at": "2026-07-20", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认县长职务及政府班子成员关系"},
                    {"id": "S001", "title": "县委书记马福深入民政领域开展专项调研", "url": "https://mp.weixin.qq.com/s/dJnWmq4jbiihr62U2Enkdg", "publisher": "明水发布（明水县人民政府）", "published_at": "2026-07-20", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "党政搭档关系确认"}
                ],
                "confidence_summary": {
                    "identity": "plausible",
                    "current_role": "confirmed",
                    "career_completeness": "thin",
                    "relationship_confidence": "medium",
                    "biggest_gap": "邓吉喆的完整履历（出生年份、籍贯、教育背景、晋升路径）未找到"
                },
                "open_questions": [
                    {
                        "priority": "critical",
                        "question": "邓吉喆的完整履历是什么？出生年份、籍贯、教育背景、工作经历？",
                        "why_it_matters": "作为县政府一把手，其职业背景对理解政治网络至关重要",
                        "suggested_queries": ["邓吉喆 简历 明水 县长", "邓吉喆 任前公示 绥化"],
                        "last_attempted": AS_OF
                    },
                    {
                        "priority": "high",
                        "question": "邓吉喆何时调任明水县长？前任县长是谁？",
                        "why_it_matters": "了解县长交接历史和政治网络变化",
                        "suggested_queries": ["明水县 前任 县长", "明水县 县长 任职时间", "邓吉喆 绥化 任职"],
                        "last_attempted": AS_OF
                    },
                    {
                        "priority": "medium",
                        "question": "邓吉喆的籍贯/出生地是哪里？",
                        "why_it_matters": "同乡关系分析",
                        "suggested_queries": ["邓吉喆 籍贯", "邓吉喆 出生地"],
                        "last_attempted": AS_OF
                    }
                ]
            }
        },
    ]

    for pf in person_files:
        fname = f"{TODAY}-黑龙江省-绥化市-{pf['job']}-{pf['name']}.json"
        path = PERSONS_DIR / fname
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pf["data"], f, ensure_ascii=False, indent=2)
        print(f"  ✅ Person JSON: {path}")

    # ── Copy to canonical paths ────────────────────────────────────────
    import shutil

    CANONICAL_DB.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_GEXF.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_BUILD.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_PERSONS.mkdir(parents=True, exist_ok=True)

    shutil.copy2(DB_PATH, CANONICAL_DB)
    shutil.copy2(GEXF_PATH, CANONICAL_GEXF)
    shutil.copy2(__file__, CANONICAL_BUILD)

    for pf in person_files:
        src = PERSONS_DIR / f"{TODAY}-黑龙江省-绥化市-{pf['job']}-{pf['name']}.json"
        dst = CANONICAL_PERSONS / src.name
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  ✅ Canonical person JSON: {dst}")

    print(f"\n📦 Canonical build script: {CANONICAL_BUILD}")
    print(f"📦 Canonical DB: {CANONICAL_DB}")
    print(f"📦 Canonical GEXF: {CANONICAL_GEXF}")
    print(f"\n✅ Done — {SLUG} data build complete.")


if __name__ == "__main__":
    main()
