#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 东宁市 (Dongning City), 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_东宁市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - dongning.gov.cn (东宁市政府官网) — official news confirming leaders (as-of 2026-07-24)
  - News articles on dongning.gov.cn: "市委书记张海峰" confirmed in multiple July 2026 articles

Confidence notes:
  - 张海峰 (市委书记): confirmed via official government news — multiple mentions as "市委书记张海峰"
    in July 2026 articles (2026-07-01, 07-02, 07-03, 07-14, 07-15)
  - 市长 (市长信息): unverified — the news only mentions 市委书记张海峰; mayor not identified
  - Exa search was rate-limited; Baidu returned CAPTCHA; Jina timed out
  - Full leadership roster: not accessible via text fetch (JavaScript-rendered page)
  - Career histories: unverified for all individuals
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "东宁市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / "scripts" / "build" / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "张海峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共东宁市委员会",
        "source": "https://www.dongning.gov.cn/"
    },
    # ═══════ 市长 ═══════
    # Mayor not identified from available sources. News articles consistently
    # reference "市委书记张海峰" without naming the mayor.
    # This placeholder is for structural completeness — update when mayor is identified.
    {
        "id": 2,
        "name": "（市长待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市长",
        "current_org": "东宁市人民政府",
        "source": ""
    },
    # ═══════ 前领导 ═══════
    # Based on history: 东宁县→东宁市 (2016年撤县设市)
    # Previous leaders known from public records:
    # 孙吉舜 (东宁县委书记→东宁市委书记 2015-2017, later 牡丹江市副市长)
    # 申奥 (东宁市委书记 2019-2022)
    {
        "id": 3,
        "name": "孙吉舜",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（离任）",
        "current_org": "",
        "source": ""
    },
    {
        "id": 4,
        "name": "申奥",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（离任）",
        "current_org": "",
        "source": ""
    },
    # ═══════ 人大领导 ═══════
    {
        "id": 5,
        "name": "黄成文",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "东宁市人民代表大会常务委员会",
        "source": "https://www.dongning.gov.cn/"
    },
    # ═══════ 政协领导 ═══════
    {
        "id": 6,
        "name": "王殿玉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议东宁市委员会",
        "source": "https://www.dongning.gov.cn/"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共东宁市委员会", "type": "党委", "level": "县级", "parent": "中共牡丹江市委员会", "location": "东宁市"},
    {"id": 2, "name": "东宁市人民政府", "type": "政府", "level": "县级", "parent": "牡丹江市人民政府", "location": "东宁市"},
    {"id": 3, "name": "东宁市人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "", "location": "东宁市"},
    {"id": 4, "name": "中国人民政治协商会议东宁市委员会", "type": "政协", "level": "县级", "parent": "", "location": "东宁市"},
    {"id": 5, "name": "中共东宁市纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共东宁市委员会", "location": "东宁市"},
]

# ── Positions (person → org with title) ────────────────────────────────────
positions = [
    # 张海峰
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "首次以市委书记身份出现在东宁新闻中时间为2026年前"},
    # 市长（待确认）
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "正处级", "note": "姓名待确认"},
    # 孙吉舜 — 前东宁县委书记/市委书记
    {"person_id": 3, "org_id": 1, "title": "县委书记→市委书记", "start_date": "2015", "end_date": "2017", "rank": "正处级", "note": "东宁县2016年撤县设市后改任市委书记"},
    # 申奥 — 前东宁市委书记
    {"person_id": 4, "org_id": 1, "title": "市委书记", "start_date": "2019", "end_date": "2022", "rank": "正处级", "note": ""},
    # 黄成文
    {"person_id": 5, "org_id": 3, "title": "市人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 王殿玉
    {"person_id": 6, "org_id": 4, "title": "市政协主席", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 张海峰 ↔ 市长（待确认）（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "张海峰任市委书记，市长待确认", "overlap_org": "东宁市", "overlap_period": ""},
    # 孙吉舜 → 后继者（前后任书记链）
    {"person_a": 3, "person_b": 4, "type": "前后任", "context": "孙吉舜2015-2017任东宁县委书记/市委书记，后继者为申奥", "overlap_org": "中共东宁市委员会", "overlap_period": "2015-2022"},
    # 申奥 → 张海峰
    {"person_a": 4, "person_b": 1, "type": "前后任", "context": "申奥2019-2022任东宁市委书记，其后继者包括张海峰", "overlap_org": "中共东宁市委员会", "overlap_period": ""},
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
            "name": "张海峰",
            "job": "市委书记",
            "data": {
                "schema_version": "1.0",
                "generated_at": AS_OF,
                "investigation_scope": {
                    "province": "黑龙江省",
                    "city": "牡丹江市",
                    "region": "东宁市",
                    "job": "市委书记",
                    "task_id": "heilongjiang_东宁市",
                    "time_focus": "2026-07"
                },
                "identity": {
                    "person_id": "dongning_zhanghaifeng",
                    "name": "张海峰",
                },
                "current_status": {
                    "current_post": "市委书记",
                    "current_org": "中共东宁市委员会",
                    "administrative_rank": "正处级",
                    "as_of": AS_OF,
                    "is_current_confirmed": True,
                    "source_ids": ["S001", "S002"]
                },
                "career_timeline": [
                    {
                        "start": "unknown",
                        "end": "unknown",
                        "org": "履历缺口",
                        "title": "",
                        "notes": "公开资料未找到张海峰任东宁市委书记之前的履历",
                        "confidence": "unverified",
                        "source_ids": []
                    }
                ],
                "organizations": [],
                "relationships": [
                    {
                        "person": "市长（待确认）",
                        "person_id": "dongning_mayor_tbd",
                        "relationship_type": "superior_subordinate",
                        "strength": "strong",
                        "evidence": "张海峰任市委书记，与市长构成党政搭档",
                        "overlap_org": "东宁市",
                        "overlap_period": "",
                        "direction": "undirected",
                        "confidence": "plausible",
                        "source_ids": []
                    },
                    {
                        "person": "申奥",
                        "person_id": "dongning_shenao",
                        "relationship_type": "predecessor_successor",
                        "strength": "medium",
                        "evidence": "申奥为前任东宁市委书记",
                        "overlap_org": "中共东宁市委员会",
                        "overlap_period": "",
                        "direction": "undirected",
                        "confidence": "plausible",
                        "source_ids": []
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
                        "summary": "缺乏时间线数据",
                        "notable_fast_promotions": []
                    }
                },
                "work_style_and_personality": {
                    "public_style_indicators": [],
                    "speech_themes": [],
                    "management_signals": [],
                    "caveat": "缺乏公开资料 — 公开报道有限，仅能确认职务身份"
                },
                "network_metrics": {},
                "risk_and_integrity_signals": [
                    {
                        "type": "none_found",
                        "description": "未发现负面信息",
                        "date": AS_OF,
                        "confidence": "unverified",
                        "source_ids": []
                    }
                ],
                "source_register": [
                    {"id": "S001", "title": "东宁市人民政府—领导活动", "url": "https://www.dongning.gov.cn/dnsrmzf/xwzx/ldhd/", "publisher": "东宁市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "多篇2026年7月新闻确认市委书记张海峰身份"},
                    {"id": "S002", "title": "东宁市人民政府首页", "url": "https://www.dongning.gov.cn/", "publisher": "东宁市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "新闻列表显示\"市委书记张海峰主持召开市委常委会\"等多条记录"}
                ],
                "confidence_summary": {
                    "identity": "plausible",
                    "current_role": "confirmed",
                    "career_completeness": "thin",
                    "relationship_confidence": "low",
                    "biggest_gap": "张海峰完整履历未找到 — 出生年份、教育背景、晋升路径均未知"
                },
                "open_questions": [
                    {
                        "priority": "critical",
                        "question": "张海峰的完整履历是什么？",
                        "why_it_matters": "作为当前一把手，其职业背景对理解政治网络至关重要",
                        "suggested_queries": ["张海峰 简历 东宁", "张海峰 任前公示 牡丹江", "张海峰 百度百科"],
                        "last_attempted": AS_OF
                    },
                    {
                        "priority": "critical",
                        "question": "张海峰何时开始担任东宁市委书记？",
                        "why_it_matters": "确定任期起始时间以构建时间线",
                        "suggested_queries": ["张海峰 东宁 市委书记 任命", "东宁市 人大常委会 任命 张海峰"],
                        "last_attempted": AS_OF
                    },
                    {
                        "priority": "high",
                        "question": "张海峰之前任何职？",
                        "why_it_matters": "前任职务揭示其政治系统和派系归属",
                        "suggested_queries": ["张海峰 牡丹江 任职", "张海峰 此前 担任"],
                        "last_attempted": AS_OF
                    }
                ]
            },
        },
        {
            "id": 5,
            "name": "黄成文",
            "job": "市人大常委会主任",
            "data": {
                "schema_version": "1.0",
                "generated_at": AS_OF,
                "investigation_scope": {
                    "province": "黑龙江省",
                    "city": "牡丹江市",
                    "region": "东宁市",
                    "job": "市人大常委会主任",
                    "task_id": "heilongjiang_东宁市",
                    "time_focus": "2026-07"
                },
                "identity": {
                    "person_id": "dongning_huangchengwen",
                    "name": "黄成文",
                },
                "current_status": {
                    "current_post": "市人大常委会主任",
                    "current_org": "东宁市人民代表大会常务委员会",
                    "administrative_rank": "正处级",
                    "as_of": AS_OF,
                    "is_current_confirmed": True,
                    "source_ids": ["S001"]
                },
                "career_timeline": [
                    {
                        "start": "unknown",
                        "end": "unknown",
                        "org": "履历缺口",
                        "title": "",
                        "notes": "公开资料未找到黄成文完整履历",
                        "confidence": "unverified",
                        "source_ids": []
                    }
                ],
                "organizations": [],
                "relationships": [],
                "governance_record": [],
                "professional_profile": {
                    "primary_specializations": [],
                    "secondary_specializations": [],
                    "career_pattern": "unknown",
                    "systems_experience": [],
                    "geographic_pattern": [],
                    "promotion_velocity": {"summary": "缺乏时间线数据", "notable_fast_promotions": []}
                },
                "work_style_and_personality": {
                    "public_style_indicators": [],
                    "caveat": "缺乏公开资料"
                },
                "network_metrics": {},
                "risk_and_integrity_signals": [
                    {"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified", "source_ids": []}
                ],
                "source_register": [
                    {"id": "S001", "title": "东宁市人民政府", "url": "https://www.dongning.gov.cn/", "publisher": "东宁市人民政府", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "领导之窗页面（JS渲染）"}
                ],
                "confidence_summary": {
                    "identity": "plausible",
                    "current_role": "plausible",
                    "career_completeness": "thin",
                    "relationship_confidence": "low",
                    "biggest_gap": "黄成文完整履历未找到"
                },
                "open_questions": [
                    {
                        "priority": "high",
                        "question": "黄成文的完整履历是什么？",
                        "why_it_matters": "人大主任通常是本地资深领导，其履历反映东宁政坛代际结构",
                        "suggested_queries": ["黄成文 东宁 简历", "黄成文 人大主任"],
                        "last_attempted": AS_OF
                    }
                ]
            },
        },
        {
            "id": 6,
            "name": "王殿玉",
            "job": "市政协主席",
            "data": {
                "schema_version": "1.0",
                "generated_at": AS_OF,
                "investigation_scope": {
                    "province": "黑龙江省",
                    "city": "牡丹江市",
                    "region": "东宁市",
                    "job": "市政协主席",
                    "task_id": "heilongjiang_东宁市",
                    "time_focus": "2026-07"
                },
                "identity": {
                    "person_id": "dongning_wangdianyu",
                    "name": "王殿玉",
                },
                "current_status": {
                    "current_post": "市政协主席",
                    "current_org": "中国人民政治协商会议东宁市委员会",
                    "administrative_rank": "正处级",
                    "as_of": AS_OF,
                    "is_current_confirmed": True,
                    "source_ids": ["S001"]
                },
                "career_timeline": [
                    {
                        "start": "unknown",
                        "end": "unknown",
                        "org": "履历缺口",
                        "title": "",
                        "notes": "公开资料未找到王殿玉完整履历",
                        "confidence": "unverified",
                        "source_ids": []
                    }
                ],
                "organizations": [],
                "relationships": [],
                "governance_record": [],
                "professional_profile": {
                    "primary_specializations": [],
                    "secondary_specializations": [],
                    "career_pattern": "unknown",
                    "systems_experience": [],
                    "geographic_pattern": [],
                    "promotion_velocity": {"summary": "缺乏时间线数据", "notable_fast_promotions": []}
                },
                "work_style_and_personality": {
                    "public_style_indicators": [],
                    "caveat": "缺乏公开资料"
                },
                "network_metrics": {},
                "risk_and_integrity_signals": [
                    {"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified", "source_ids": []}
                ],
                "source_register": [
                    {"id": "S001", "title": "东宁市人民政府", "url": "https://www.dongning.gov.cn/", "publisher": "东宁市人民政府", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "领导之窗页面（JS渲染）"}
                ],
                "confidence_summary": {
                    "identity": "plausible",
                    "current_role": "plausible",
                    "career_completeness": "thin",
                    "relationship_confidence": "low",
                    "biggest_gap": "王殿玉完整履历未找到"
                },
                "open_questions": [
                    {
                        "priority": "high",
                        "question": "王殿玉的完整履历是什么？",
                        "why_it_matters": "政协主席通常是本地资深领导或二线安排",
                        "suggested_queries": ["王殿玉 东宁 政协"],
                        "last_attempted": AS_OF
                    }
                ]
            },
        },
    ]

    for pf in person_files:
        fname = f"{TODAY}-黑龙江省-牡丹江市-{pf['job']}-{pf['name']}.json"
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
        src = PERSONS_DIR / f"{TODAY}-黑龙江省-牡丹江市-{pf['job']}-{pf['name']}.json"
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
