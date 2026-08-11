#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 兰西县 (Lanxi County), 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_兰西县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - hljlanxi.gov.cn (兰西县人民政府官网) — 领导视窗 (confirmed as-of 2026-07-24)
    - 张久利 (县长): confirmed via official leadership page with bio details
    - 6副县长: confirmed via official leadership page
  - hljlanxi.gov.cn news articles — 吴迪 (县委书记): confirmed as 县委书记 via multiple news items
  - zh.wikipedia.org — 兰西县 page for basic info

Confidence notes:
  - 吴迪 (县委书记): confirmed via official government news (县委书记吴迪); detailed career history unverified
  - 张久利 (县长): confirmed via official government leadership page (born 1979-03, male, Han, graduate degree)
  - Deputy mayors: confirmed via official leadership page (names only)
  - Full party committee roster (副书记、纪委书记、组织部长等): unverified — not available on public government site
  - Career histories for most leaders: unverified — only current names and titles confirmed
  - Exa search was rate-limited; Baidu returned CAPTCHA
"""
# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "兰西县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / "build_兰西县_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "吴迪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共兰西县委员会",
        "source": "https://www.hljlanxi.gov.cn/lx/lxyw/202607/c12_237992.shtml"
    },
    {
        "id": 2,
        "name": "张久利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年3月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "县长",
        "current_org": "兰西县人民政府",
        "source": "https://www.hljlanxi.gov.cn/lx/ldxx/ldsc.shtml"
    },
    # ═══════ 副县长 ═══════
    {
        "id": 3,
        "name": "聂艳双",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "兰西县人民政府",
        "source": "https://www.hljlanxi.gov.cn/lx/ldxx/ldsc.shtml"
    },
    {
        "id": 4,
        "name": "怀龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "兰西县人民政府",
        "source": "https://www.hljlanxi.gov.cn/lx/ldxx/ldsc.shtml"
    },
    {
        "id": 5,
        "name": "林士权",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "兰西县人民政府",
        "source": "https://www.hljlanxi.gov.cn/lx/ldxx/ldsc.shtml"
    },
    {
        "id": 6,
        "name": "满志广",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "兰西县人民政府",
        "source": "https://www.hljlanxi.gov.cn/lx/ldxx/ldsc.shtml"
    },
    {
        "id": 7,
        "name": "胡小东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "兰西县人民政府",
        "source": "https://www.hljlanxi.gov.cn/lx/ldxx/ldsc.shtml"
    },
    {
        "id": 8,
        "name": "田国林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "兰西县人民政府",
        "source": "https://www.hljlanxi.gov.cn/lx/ldxx/ldsc.shtml"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共兰西县委员会", "type": "党委", "level": "县级", "parent": "中共绥化市委员会", "location": "兰西县"},
    {"id": 2, "name": "兰西县人民政府", "type": "政府", "level": "县级", "parent": "绥化市人民政府", "location": "兰西县"},
]

# ── Positions (person → org with title) ────────────────────────────────────
positions = [
    # 吴迪
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 张久利
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "", "rank": "正处级", "note": "主持县政府全面工作，主管财政局（国有资产监督管理办公室）、审计局"},
    # 聂艳双
    {"person_id": 3, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 怀龙
    {"person_id": 4, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 林士权
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 满志广
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 胡小东
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 田国林
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 吴迪 ↔ 张久利（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "吴迪任县委书记，张久利任县长，为兰西县党政正职搭档", "overlap_org": "兰西县", "overlap_period": ""},
    # 张久利 ↔ 聂艳双（政府班子）
    {"person_a": 2, "person_b": 3, "type": "政府班子", "context": "聂艳双任副县长，张久利为县长", "overlap_org": "兰西县人民政府", "overlap_period": ""},
    # 张久利 ↔ 怀龙（政府班子）
    {"person_a": 2, "person_b": 4, "type": "政府班子", "context": "怀龙任副县长，张久利为县长", "overlap_org": "兰西县人民政府", "overlap_period": ""},
    # 张久利 ↔ 林士权（政府班子）
    {"person_a": 2, "person_b": 5, "type": "政府班子", "context": "林士权任副县长，张久利为县长", "overlap_org": "兰西县人民政府", "overlap_period": ""},
    # 张久利 ↔ 满志广（政府班子）
    {"person_a": 2, "person_b": 6, "type": "政府班子", "context": "满志广任副县长，张久利为县长", "overlap_org": "兰西县人民政府", "overlap_period": ""},
    # 张久利 ↔ 胡小东（政府班子）
    {"person_a": 2, "person_b": 7, "type": "政府班子", "context": "胡小东任副县长，张久利为县长", "overlap_org": "兰西县人民政府", "overlap_period": ""},
    # 张久利 ↔ 田国林（政府班子）
    {"person_a": 2, "person_b": 8, "type": "政府班子", "context": "田国林任副县长，张久利为县长", "overlap_org": "兰西县人民政府", "overlap_period": ""},
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
            "name": "吴迪",
            "job": "县委书记",
            "data": {
                "schema_version": "1.0",
                "generated_at": AS_OF,
                "investigation_scope": {
                    "province": "黑龙江省",
                    "city": "绥化市",
                    "region": "兰西县",
                    "job": "县委书记",
                    "task_id": "heilongjiang_兰西县",
                    "time_focus": "2026"
                },
                "identity": {
                    "person_id": "lanxi_wudi",
                    "name": "吴迪",
                },
                "current_status": {
                    "current_post": "县委书记",
                    "current_org": "中共兰西县委员会",
                    "administrative_rank": "正处级",
                    "as_of": AS_OF,
                    "is_current_confirmed": True,
                    "source_ids": ["S001"]
                },
                "career_timeline": [],
                "organizations": [],
                "relationships": [
                    {
                        "person": "张久利",
                        "person_id": "lanxi_zhangjiuli",
                        "relationship_type": "overlap",
                        "strength": "strong",
                        "evidence": "吴迪任县委书记，张久利任县长，为兰西县党政正职搭档",
                        "overlap_org": "兰西县",
                        "confidence": "confirmed",
                        "source_ids": ["S001", "S002"]
                    }
                ],
                "governance_record": [
                    {
                        "period": "2026-07",
                        "domain": "rural_revitalization",
                        "achievement_or_event": "到远大镇调研督导树立和践行正确政绩观学习教育、土地延包试点、农业生产、信访稳定等重点工作",
                        "role_in_event": "调研督导",
                        "location": "兰西县远大镇",
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
                            "evidence": "深入远大镇调研督导多项重点工作，强调树立和践行正确政绩观、群众立场",
                            "confidence": "plausible",
                            "source_ids": ["S001"]
                        }
                    ],
                    "speech_themes": ["正确政绩观", "群众立场", "基层治理", "乡村振兴"],
                    "management_signals": ["强调四个体系闭环落实机制"],
                    "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
                },
                "risk_and_integrity_signals": [
                    {"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified"}
                ],
                "source_register": [
                    {"id": "S001", "title": "吴迪到远大镇调研督导重点工作", "url": "https://www.hljlanxi.gov.cn/lx/lxyw/202607/c12_237992.shtml", "publisher": "兰西县人民政府", "published_at": "2026-07-21", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认县委书记职务"},
                    {"id": "S002", "title": "兰西县人民政府领导视窗", "url": "https://www.hljlanxi.gov.cn/lx/ldxx/ldsc.shtml", "publisher": "兰西县人民政府", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "县领导信息页面"}
                ],
                "confidence_summary": {
                    "identity": "plausible",
                    "current_role": "confirmed",
                    "career_completeness": "thin",
                    "relationship_confidence": "medium",
                    "biggest_gap": "吴迪的完整履历（出生年份、籍贯、教育背景、晋升路径）未找到"
                },
                "open_questions": [
                    {
                        "priority": "critical",
                        "question": "吴迪的完整履历是什么？出生年份、籍贯、教育背景、工作经历？",
                        "why_it_matters": "作为当前一把手，其职业背景对理解政治网络至关重要",
                        "suggested_queries": ["吴迪 简历 兰西 县委书记", "吴迪 任前公示 绥化"],
                        "last_attempted": AS_OF
                    },
                    {
                        "priority": "high",
                        "question": "吴迪何时调任兰西县委书记？前任是谁？",
                        "why_it_matters": "了解县委书记交接历史和政治网络变化",
                        "suggested_queries": ["兰西县 前任 县委书记", "兰西县 县委 书记 任职时间"],
                        "last_attempted": AS_OF
                    }
                ]
            }
        },
        {
            "id": 2,
            "name": "张久利",
            "job": "县长",
            "data": {
                "schema_version": "1.0",
                "generated_at": AS_OF,
                "investigation_scope": {
                    "province": "黑龙江省",
                    "city": "绥化市",
                    "region": "兰西县",
                    "job": "县长",
                    "task_id": "heilongjiang_兰西县",
                    "time_focus": "2026"
                },
                "identity": {
                    "person_id": "lanxi_zhangjiuli",
                    "name": "张久利",
                    "gender": "男",
                    "ethnicity": "汉族",
                    "birth": "1979年3月",
                    "education": [{"degree": "研究生", "study_type": "unknown"}]
                },
                "current_status": {
                    "current_post": "县长",
                    "current_org": "兰西县人民政府",
                    "administrative_rank": "正处级",
                    "as_of": AS_OF,
                    "is_current_confirmed": True,
                    "source_ids": ["S003"]
                },
                "career_timeline": [],
                "organizations": [],
                "relationships": [
                    {
                        "person": "吴迪",
                        "person_id": "lanxi_wudi",
                        "relationship_type": "overlap",
                        "strength": "strong",
                        "evidence": "张久利任县长，吴迪任县委书记，为兰西县党政正职搭档",
                        "overlap_org": "兰西县",
                        "confidence": "confirmed",
                        "source_ids": ["S001", "S002", "S003"]
                    }
                ],
                "governance_record": [
                    {
                        "period": "2026-02至2026-06",
                        "domain": "economic_development",
                        "achievement_or_event": "主持召开兰西县人民政府第二至第六次常务会议，部署全县经济工作",
                        "role_in_event": "主持",
                        "location": "兰西县",
                        "confidence": "confirmed",
                        "source_ids": ["S004"]
                    },
                    {
                        "period": "2026-07",
                        "domain": "public_security",
                        "achievement_or_event": "主持召开全县防汛工作推进会，部署防汛防灾工作",
                        "role_in_event": "主持",
                        "location": "兰西县",
                        "confidence": "confirmed",
                        "source_ids": ["S005"]
                    }
                ],
                "professional_profile": {
                    "primary_specializations": ["政府管理", "财政审计"],
                    "secondary_specializations": [],
                    "career_pattern": "unknown",
                    "systems_experience": ["政府"],
                    "geographic_pattern": [],
                    "promotion_velocity": {"summary": "1979年出生，研究生学历，当前为正处级县长", "notable_fast_promotions": []}
                },
                "work_style_and_personality": {
                    "public_style_indicators": [
                        {
                            "trait": "pragmatic",
                            "evidence": "分工主持县政府全面工作，主管财政局和审计局，体现务实管理风格",
                            "confidence": "plausible",
                            "source_ids": ["S003"]
                        }
                    ],
                    "speech_themes": [],
                    "management_signals": [],
                    "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
                },
                "risk_and_integrity_signals": [
                    {"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified"}
                ],
                "source_register": [
                    {"id": "S003", "title": "兰西县人民政府县长信息", "url": "https://www.hljlanxi.gov.cn/lx/ldxx/ldsc.shtml", "publisher": "兰西县人民政府", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "县长官方简历页"},
                    {"id": "S004", "title": "兰西县人民政府常务会议公告", "url": "https://www.hljlanxi.gov.cn/lx/zdhyxx/", "publisher": "兰西县人民政府", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "政府常务会议系列新闻"},
                    {"id": "S005", "title": "张久利主持召开全县防汛工作推进会", "url": "https://www.hljlanxi.gov.cn/lx/lxyw/202607/c12_236974.shtml", "publisher": "兰西县人民政府", "published_at": "2026-07-06", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"}
                ],
                "confidence_summary": {
                    "identity": "confirmed",
                    "current_role": "confirmed",
                    "career_completeness": "partial",
                    "relationship_confidence": "medium",
                    "biggest_gap": "张久利完整履历（早期工作经历、晋升路径、教育背景详情）未找到"
                },
                "open_questions": [
                    {
                        "priority": "critical",
                        "question": "张久利来兰西县之前的任职经历是什么？完整的晋升路径？",
                        "why_it_matters": "了解县长的职业背景和政治网络",
                        "suggested_queries": ["张久利 简历 绥化", "张久利 任前公示", "张久利 兰西 县长 任职历程"],
                        "last_attempted": AS_OF
                    },
                    {
                        "priority": "medium",
                        "question": "张久利的研究生学历的具体院校和专业是什么？",
                        "why_it_matters": "校友关系网络分析",
                        "suggested_queries": ["张久利 毕业院校", "张久利 兰西 县长 学历"],
                        "last_attempted": AS_OF
                    },
                    {
                        "priority": "medium",
                        "question": "张久利的籍贯/出生地是哪里？",
                        "why_it_matters": "同乡关系分析",
                        "suggested_queries": ["张久利 籍贯", "张久利 出生地"],
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
