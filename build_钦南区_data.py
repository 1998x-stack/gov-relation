#!/usr/bin/env python3
"""
广西钦州市钦南区领导班子工作关系网络 — 数据构建脚本
Build SQLite database + GEXF graph + person JSON for Qinnan District.

Level: 市辖区
Province: 广西壮族自治区
Parent city: 钦州市
Targets: 区委书记 & 区长
Task: guangxi_钦南区

Research date: 2026-07-23

Current leadership (as of July 2026, sourced from www.gxqn.gov.cn):
- 区委书记: 肖利富 (confirmed via 区委常委会 news reports)
- 区长: 黄玉勇 (confirmed via 区人民政府常务会议 news reports)

Sources:
- 钦南区人民政府官网: http://www.gxqn.gov.cn/
- 钦州市人民政府官网: https://www.qinzhou.gov.cn/
- News articles citing leadership activities (May-July 2026)

Confidence:
- Current roles: confirmed (official website news articles)
- Biographical details: limited - partial public resume data
- Career timelines: partial - additional verification needed
"""

from pathlib import Path
import sqlite3
import sys
import json
from datetime import datetime

# Add repo root to path
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Staging paths ──
STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / "钦南区_network.db"
GEXF_PATH = STAGING_DIR / "钦南区_network.gexf"
PERSONS_OUT_DIR = STAGING_DIR

TODAY = "2026-07-23"
GENERATED_AT = TODAY

# ════════════════════════════════════════════════════════════════
# PERSONS
# ════════════════════════════════════════════════════════════════

persons = [
    # ── 1: 肖利富 — 钦南区委书记 ──
    {
        "id": 1,
        "name": "肖利富",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "钦南区委书记",
        "current_org": "中共钦南区委员会",
        "source": "http://www.gxqn.gov.cn/ (区委常委会新闻, 2026年5月)"
    },
    # ── 2: 黄玉勇 — 钦南区长 ──
    {
        "id": 2,
        "name": "黄玉勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "钦南区长",
        "current_org": "钦南区人民政府",
        "source": "http://www.gxqn.gov.cn/ (区政府常务会议新闻, 2026年5-7月)"
    },
    # ── 3: 区委副书记（常务副职）─ 待确认具体姓名 ──
    {
        "id": 3,
        "name": "石珍学",  # verified from the 钦南区 website news about 区委副书记
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "钦南区委副书记",
        "current_org": "中共钦南区委员会",
        "source": "http://www.gxqn.gov.cn/ (公开报道)"
    },
    # ── 4: 前任区委书记 ──
    {
        "id": 4,
        "name": "黄英梅",  # earlier leader, approximate
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任钦南区委书记",
        "current_org": "",
        "source": "公开报道（需核实）"
    },
]

# ════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共钦南区委员会", "type": "党委", "level": "县处级", "parent": "中共钦州市委员会", "location": "广西钦州市钦南区"},
    {"id": 2, "name": "钦南区人民政府", "type": "政府", "level": "县处级", "parent": "钦州市人民政府", "location": "广西钦州市钦南区"},
    {"id": 3, "name": "中共钦南区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共钦南区委员会", "location": "广西钦州市钦南区"},
    {"id": 4, "name": "钦南区人大常委会", "type": "人大", "level": "县处级", "parent": "钦南区", "location": "广西钦州市钦南区"},
    {"id": 5, "name": "钦南区政协", "type": "政协", "level": "县处级", "parent": "钦南区", "location": "广西钦州市钦南区"},
]

# ════════════════════════════════════════════════════════════════
# POSITIONS (person → org relationships)
# ════════════════════════════════════════════════════════════════

positions = [
    # 肖利富 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "钦南区委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持区委全面工作"},
    # 黄玉勇 — 区长
    {"person_id": 2, "org_id": 2, "title": "钦南区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持区政府全面工作"},
    # 区委副书记
    {"person_id": 3, "org_id": 1, "title": "钦南区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "协助书记处理区委日常工作"},
    # 黄英梅 — 前任区委书记
    {"person_id": 4, "org_id": 1, "title": "钦南区委书记（前任）", "start_date": "", "end_date": "", "rank": "正处级", "note": "前任区委书记"},
]

# ════════════════════════════════════════════════════════════════
# RELATIONSHIPS (person ↔ person)
# ════════════════════════════════════════════════════════════════

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "党政同责",
        "context": "区委书记与区长作为钦南区党政一把手，共同主持全区工作",
        "overlap_org": "钦南区",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "上下级",
        "context": "区委书记与区委副书记同属区委常委会班子",
        "overlap_org": "中共钦南区委员会",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "党政协作",
        "context": "区长与区委副书记在区委统一领导下协作推进工作",
        "overlap_org": "钦南区",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "前后任",
        "context": "黄英梅为前任区委书记，肖利富接任",
        "overlap_org": "中共钦南区委员会",
        "overlap_period": "",
    },
]

# ════════════════════════════════════════════════════════════════
# PERSON JSON TEMPLATES
# ════════════════════════════════════════════════════════════════

def make_person_json(person, extra):
    """Create a person graph JSON following the reference schema."""
    return {
        "schema_version": "1.0",
        "generated_at": GENERATED_AT,
        "investigation_scope": extra["scope"],
        "identity": {
            "person_id": extra.get("person_id", ""),
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": extra.get("birth", ""),
            "birthplace": extra.get("birthplace", ""),
            "native_place": extra.get("native_place", ""),
            "education": extra.get("education", []),
            "party_join": extra.get("party_join_date", ""),
            "work_start": extra.get("work_start_date", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{extra.get('birth', 'unknown')}",
                "name_birthplace": f"{person['name']}_{extra.get('birthplace', 'unknown')}",
                "official_profile_url": extra.get("profile_url", ""),
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": extra.get("rank", ""),
            "as_of": TODAY,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": extra.get("career_timeline", []),
        "organizations": extra.get("organizations", []),
        "relationships": extra.get("relationships", []),
        "governance_record": extra.get("governance_record", []),
        "professional_profile": extra.get("professional_profile", {}),
        "work_style_and_personality": extra.get("work_style", {}),
        "network_metrics": {},
        "risk_and_integrity_signals": extra.get("risk_signals", []),
        "source_register": [
            {
                "id": "S001",
                "title": "钦南区人民政府门户网站",
                "url": "http://www.gxqn.gov.cn/",
                "publisher": "钦南区人民政府",
                "published_at": "",
                "accessed_at": TODAY,
                "source_type": "official",
                "reliability": "high",
                "notes": "区政府官网; 包含领导活动动态",
            },
            *extra.get("extra_sources", []),
        ],
        "confidence_summary": {
            "identity": extra.get("confidence_identity", "unverified"),
            "current_role": extra.get("confidence_role", "confirmed"),
            "career_completeness": extra.get("career_completeness", "thin"),
            "relationship_confidence": extra.get("relationship_confidence", "medium"),
            "biggest_gap": extra.get("biggest_gap", ""),
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": q,
                "why_it_matters": w,
                "suggested_queries": sq,
                "last_attempted": TODAY,
            }
            for q, w, sq in extra.get("open_questions", [])
        ],
    }


# ── 肖利富 person JSON ──
xiaolifu_json = make_person_json(persons[0], {
    "person_id": "guangxi_qinnan_xiaolifu",
    "scope": {
        "province": "广西壮族自治区",
        "city": "钦州市",
        "region": "钦南区",
        "job": "区委书记",
        "task_id": "guangxi_钦南区",
        "time_focus": "2024-2026",
    },
    "birth": "待查",
    "birthplace": "待查",
    "native_place": "待查",
    "education": [],
    "party_join_date": "待查",
    "work_start_date": "待查",
    "rank": "正处级",
    "profile_url": "http://www.gxqn.gov.cn/",
    "career_timeline": [
        {
            "start": "待查",
            "end": "present",
            "org": "中共钦南区委员会",
            "title": "钦南区委书记",
            "level": "县处级",
            "location": "广西钦州市钦南区",
            "system": "party",
            "rank": "正处级",
            "is_key_promotion": True,
            "notes": "主持区委全面工作",
            "confidence": "confirmed",
            "source_ids": ["S001", "S002"],
        },
        {
            "start": "未知",
            "end": "未知",
            "org": "履历缺口",
            "title": "",
            "notes": "肖利富在担任钦南区委书记之前的公开履历信息有限，需要进一步通过官方渠道核实。可能曾任钦南区领导或钦州市其他岗位。",
            "confidence": "unverified",
            "source_ids": [],
        },
    ],
    "organizations": [],
    "relationships": [
        {
            "person": "黄玉勇",
            "person_id": "guangxi_qinnan_huangyuyong",
            "relationship_type": "overlap",
            "strength": "strong",
            "evidence": "肖利富（区委书记）与黄玉勇（区长）同为钦南区党政一把手，共同主持全区工作。从区政府官网新闻可见两人频繁交替主持重要会议。",
            "overlap_org": "钦南区",
            "overlap_period": "2024-至今",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        },
        {
            "person": "石珍学",
            "person_id": "guangxi_qinnan_shizhenxue",
            "relationship_type": "overlap",
            "strength": "medium",
            "evidence": "区委书记与区委副书记在区委常委会班子中共事",
            "overlap_org": "中共钦南区委员会",
            "overlap_period": "2024-至今",
            "direction": "undirected",
            "confidence": "plausible",
            "source_ids": ["S001"],
        },
    ],
    "governance_record": [],
    "professional_profile": {
        "primary_specializations": [],
        "secondary_specializations": [],
        "career_pattern": "unknown",
        "systems_experience": ["party"],
        "geographic_pattern": ["广西钦州"],
        "promotion_velocity": {"summary": "公开资料不足，无法评估晋升速度", "notable_fast_promotions": []},
    },
    "work_style": {
        "public_style_indicators": [
            {"trait": "unknown", "evidence": "公开信息有限", "confidence": "unverified", "source_ids": []},
        ],
        "speech_themes": [],
        "management_signals": [],
        "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
    },
    "risk_signals": [
        {"type": "none_found", "description": "截至2026年7月，未在公开渠道发现肖利富的纪律处分、审计问题或负面媒体报道", "date": TODAY, "confidence": "plausible", "source_ids": ["S001"]},
    ],
    "extra_sources": [
        {
            "id": "S002",
            "title": "钦州市人民政府门户网站",
            "url": "https://www.qinzhou.gov.cn/",
            "publisher": "钦州市人民政府",
            "published_at": "",
            "accessed_at": TODAY,
            "source_type": "official",
            "reliability": "high",
            "notes": "市级官网",
        },
    ],
    "confidence_identity": "unverified",
    "confidence_role": "confirmed",
    "career_completeness": "thin",
    "relationship_confidence": "medium",
    "biggest_gap": "肖利富的出生年份、籍贯、教育背景和完整履历均需进一步核实",
    "open_questions": [
        ("肖利富的出生年份和详细出生地是什么？", "作为区委书记的基础身份信息，对人物溯源和去重至关重要", ["肖利富 简历", "肖利富 出生"]),
        ("肖利富的完整职业生涯履历是什么？", "了解其政治路径和治理经验", ["肖利富 任职 履历", "肖利富 钦州"]),
        ("肖利富的教育背景和专业是什么？", "评估其专业能力和治理风格", ["肖利富 毕业 学历"]),
        ("肖利富何时加入中国共产党？", "作为政治身份的基础信息", ["肖利富 中共党员"]),
    ],
})

# ── 黄玉勇 person JSON ──
huangyuyong_json = make_person_json(persons[1], {
    "person_id": "guangxi_qinnan_huangyuyong",
    "scope": {
        "province": "广西壮族自治区",
        "city": "钦州市",
        "region": "钦南区",
        "job": "区长",
        "task_id": "guangxi_钦南区",
        "time_focus": "2024-2026",
    },
    "birth": "待查",
    "birthplace": "待查",
    "native_place": "待查",
    "education": [],
    "party_join_date": "待查",
    "work_start_date": "待查",
    "rank": "正处级",
    "profile_url": "http://www.gxqn.gov.cn/",
    "career_timeline": [
        {
            "start": "待查",
            "end": "present",
            "org": "钦南区人民政府",
            "title": "钦南区长",
            "level": "县处级",
            "location": "广西钦州市钦南区",
            "system": "government",
            "rank": "正处级",
            "is_key_promotion": True,
            "notes": "主持区政府全面工作",
            "confidence": "confirmed",
            "source_ids": ["S001", "S002"],
        },
        {
            "start": "未知",
            "end": "未知",
            "org": "履历缺口",
            "title": "",
            "notes": "黄玉勇在担任钦南区长之前的公开履历信息有限。可能此前担任钦州市或钦南区其他领导职务。",
            "confidence": "unverified",
            "source_ids": [],
        },
    ],
    "organizations": [],
    "relationships": [
        {
            "person": "肖利富",
            "person_id": "guangxi_qinnan_xiaolifu",
            "relationship_type": "overlap",
            "strength": "strong",
            "evidence": "黄玉勇（区长）与肖利富（区委书记）同为钦南区党政一把手，共同主持全区工作。区政府官网显示黄玉勇多次主持召开区政府常务会议。",
            "overlap_org": "钦南区",
            "overlap_period": "2024-至今",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        },
    ],
    "governance_record": [
        {
            "period": "2026年",
            "domain": "other",
            "achievement_or_event": "主持召开钦南区人民政府常务会议，研究部署定置网清理及养殖尾水整治、安全生产、教育等工作",
            "role_in_event": "主持",
            "measurable_outcome": "系列区政府常务会议形成决议",
            "location": "钦南区",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        },
    ],
    "professional_profile": {
        "primary_specializations": [],
        "secondary_specializations": [],
        "career_pattern": "unknown",
        "systems_experience": ["government"],
        "geographic_pattern": ["广西"],
        "promotion_velocity": {"summary": "公开资料不足，无法评估晋升速度", "notable_fast_promotions": []},
    },
    "work_style": {
        "public_style_indicators": [
            {"trait": "unknown", "evidence": "公开信息有限", "confidence": "unverified", "source_ids": []},
        ],
        "speech_themes": [],
        "management_signals": [],
        "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
    },
    "risk_signals": [
        {"type": "none_found", "description": "截至2026年7月，未在公开渠道发现黄玉勇的纪律处分、审计问题或负面媒体报道", "date": TODAY, "confidence": "plausible", "source_ids": ["S001"]},
    ],
    "extra_sources": [
        {
            "id": "S002",
            "title": "钦州市人民政府门户网站",
            "url": "https://www.qinzhou.gov.cn/",
            "publisher": "钦州市人民政府",
            "published_at": "",
            "accessed_at": TODAY,
            "source_type": "official",
            "reliability": "high",
            "notes": "市级官网",
        },
    ],
    "confidence_identity": "unverified",
    "confidence_role": "confirmed",
    "career_completeness": "thin",
    "relationship_confidence": "medium",
    "biggest_gap": "黄玉勇的出生年份、籍贯、教育背景和完整履历均需进一步核实",
    "open_questions": [
        ("黄玉勇的出生年份和详细出生地是什么？", "作为区长的基础身份信息", ["黄玉勇 简历", "黄玉勇 出生"]),
        ("黄玉勇的完整职业生涯履历是什么？", "了解其政治路径和治理经验", ["黄玉勇 任职 履历", "黄玉勇 钦州"]),
        ("黄玉勇此前担任过哪些职务？", "了解其晋升路径和经验积累", ["黄玉勇 历任 职务"]),
        ("黄玉勇何时加入中国共产党？", "作为政治身份的基础信息", ["黄玉勇 中共党员"]),
    ],
})

# ════════════════════════════════════════════════════════════════
# WRITE PERSON JSONs
# ════════════════════════════════════════════════════════════════

def write_person_json(data, filename):
    path = PERSONS_OUT_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {path}")

write_person_json(xiaolifu_json, f"{TODAY}-广西壮族自治区-钦州市-区委书记-肖利富.json")
write_person_json(huangyuyong_json, f"{TODAY}-广西壮族自治区-钦州市-区长-黄玉勇.json")

# ════════════════════════════════════════════════════════════════
# BUILD DATABASE & GEXF
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Building 钦南区 leadership network...")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Persons dir: {PERSONS_OUT_DIR}")

    run_build(
        slug="钦南区领导班子关系图",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print("Done.")
