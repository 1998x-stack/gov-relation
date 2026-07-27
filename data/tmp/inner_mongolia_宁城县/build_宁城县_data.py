#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 宁城县, 赤峰市, 内蒙古自治区.

Investigation date: 2026-07-25
Task ID: inner_mongolia_宁城县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - www.ningchengxian.gov.cn — 宁城县人民政府官方网站 (primary, current as of July 2026)
  - Official leadership bios from 领导之窗 section (ldzc/) accessed 2026-07-25

Confidence notes:
  - Current government roles: confirmed via official government website (January 2026 bios)
  - County Party Secretary (县委书记): NOT found on government website — this is a party
    position and the 县委 leadership page is not publicly listed on the government portal.
    The government site's 领导之窗 only lists the government team (县长 and 副县长s).
  - Biographical details for confirmed persons sourced from official bios.
  - All claims labeled with confidence level; gaps explicitly documented.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "宁城县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "inner_mongolia_宁城县"
if _CURRENT_DIR.name == "inner_mongolia_宁城县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-5 confirmed government leaders, 6-9 other confirmed/suggested persons

persons = [
    # ══════════════════════════════════════════════════════════════════════════
    # Core Leadership - Government Side (confirmed from official bios)
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "张文泽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年9月",
        "birthplace": "内蒙古喀喇沁旗",
        "education": "研究生学历",
        "party_join": "2001年7月",
        "work_start": "1998年9月",
        "current_post": "县委副书记、县长",
        "current_org": "中共宁城县委员会 / 宁城县人民政府",
        "source": "http://www.ningchengxian.gov.cn/zwgk/xxgk/zfxxgkml/jgsz/ldzc/202501/t20250124_2531223.html",
        "confidence": "confirmed",
        "notes": "1977年9月出生，内蒙古喀喇沁旗人；研究生学历；1998年9月参加工作，2001年7月入党。主持县政府全面工作，分管审计局。"
    },
    {
        "id": 2,
        "name": "卢振超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年10月",
        "birthplace": "赤峰市翁牛特旗",
        "education": "本科学历",
        "party_join": "2002年12月",
        "work_start": "2004年12月",
        "current_post": "县委常委、常务副县长",
        "current_org": "中共宁城县委员会 / 宁城县人民政府",
        "source": "http://www.ningchengxian.gov.cn/zwgk/xxgk/zfxxgkml/jgsz/ldzc/202211/t20221124_1907659.html",
        "confidence": "confirmed",
        "notes": "1981年10月出生，赤峰市翁牛特旗人；本科学历；2004年12月参加工作，2002年12月入党。负责县政府常务工作。"
    },
    {
        "id": 3,
        "name": "于利民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年11月",
        "birthplace": "内蒙古宁城县",
        "education": "研究生学历",
        "party_join": "1995年6月",
        "work_start": "1996年7月",
        "current_post": "副县长",
        "current_org": "宁城县人民政府",
        "source": "http://www.ningchengxian.gov.cn/zwgk/xxgk/zfxxgkml/jgsz/ldzc/202111/t20211118_1470013.html",
        "confidence": "confirmed",
        "notes": "1975年11月出生，内蒙古宁城县人（本地干部）；研究生学历；1996年7月参加工作，1995年6月入党。负责工业经济、招商引资、交通运输、市场监管等工作。"
    },
    {
        "id": 4,
        "name": "贾富强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年9月",
        "birthplace": "河南省郑州市",
        "education": "北京理工大学法学专业",
        "party_join": "2001年11月",
        "work_start": "2003年7月",
        "current_post": "县委常委、副县长",
        "current_org": "中共宁城县委员会 / 宁城县人民政府",
        "source": "http://www.ningchengxian.gov.cn/zwgk/xxgk/zfxxgkml/jgsz/ldzc/202403/t20240320_2281796.html",
        "confidence": "confirmed",
        "notes": "1979年9月出生于河南省郑州市；1999年考入北京理工大学法学专业；2003年7月参加工作，2001年11月入党。协助京蒙协作、对外开放和招商引资工作。"
    },
    {
        "id": 5,
        "name": "赫连玉罡",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年10月",
        "birthplace": "赤峰市元宝山区",
        "education": "本科学历",
        "party_join": "1998年6月",
        "work_start": "1989年11月",
        "current_post": "县委常委、副县长",
        "current_org": "中共宁城县委员会 / 宁城县人民政府",
        "source": "http://www.ningchengxian.gov.cn/zwgk/xxgk/zfxxgkml/jgsz/ldzc/202403/t20240322_2283764.html",
        "confidence": "confirmed",
        "notes": "1973年10月出生于赤峰市元宝山区；本科学历；1989年11月参加工作，1998年6月入党。协助定点帮扶、对外开放和招商引资工作。"
    },
]

# ── Open Questions/Potential Additional Persons ──────────────────────────────
# 县委书记: Not found on government website (party position). Name unknown.
# 白景利: 副县长 — mentioned in 贾富强's bio as '协助白景利副县长'. Could be a副县长 or 县委副书记.
#          Still being confirmed.

# ── Organizations ────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共宁城县委员会", "type": "党委", "level": "县处级", "parent": "中共赤峰市委员会", "location": "赤峰市宁城县"},
    {"id": 2, "name": "宁城县人民政府", "type": "政府", "level": "县处级", "parent": "赤峰市人民政府", "location": "赤峰市宁城县"},
    {"id": 3, "name": "宁城县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "赤峰市人民代表大会常务委员会", "location": "赤峰市宁城县"},
    {"id": 4, "name": "中国人民政治协商会议宁城县委员会", "type": "政协", "level": "县处级", "parent": "中国人民政治协商会议赤峰市委员会", "location": "赤峰市宁城县"},
    {"id": 5, "name": "中共宁城县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共赤峰市纪律检查委员会", "location": "赤峰市宁城县"},
    {"id": 6, "name": "中共宁城县委组织部", "type": "党委", "level": "县处级", "parent": "中共宁城县委员会", "location": "赤峰市宁城县"},
    {"id": 7, "name": "宁城县审计局", "type": "政府", "level": "乡科级", "parent": "宁城县人民政府", "location": "赤峰市宁城县"},
    {"id": 8, "name": "宁城县财政局", "type": "政府", "level": "乡科级", "parent": "宁城县人民政府", "location": "赤峰市宁城县"},
    {"id": 9, "name": "赤峰承接产业转移开发区", "type": "开发区", "level": "县处级", "parent": "宁城县人民政府", "location": "赤峰市宁城县"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 张文泽
    {"person_id": 1, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "正处级", "note": "县委副书记"},
    {"person_id": 1, "org_id": 2, "title": "县长、政府党组书记", "start": "", "end": "present", "rank": "正处级", "note": "主持县政府全面工作，分管审计局"},
    # 卢振超
    {"person_id": 2, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "常务副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责县政府常务工作"},
    # 于利民
    {"person_id": 3, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责工业经济、招商引资、交通运输、市场监管"},
    # 贾富强
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "协助京蒙协作、对外开放和招商引资"},
    # 赫连玉罡
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "协助定点帮扶、对外开放和招商引资"},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    # 党政搭档关系
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县长与常务副县长工作搭档", "overlap_org": "宁城县人民政府", "overlap_period": "present"},
    # 县委常委班子的共事关系
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "同为县委常委", "overlap_org": "中共宁城县委员会", "overlap_period": "present"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "同为县委常委", "overlap_org": "中共宁城县委员会", "overlap_period": "present"},
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "同为县委常委", "overlap_org": "中共宁城县委员会", "overlap_period": "present"},
    # 政府班子共事关系
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "宁城县人民政府", "overlap_period": "present"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "宁城县人民政府", "overlap_period": "present"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "宁城县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "常务副县长与副县长", "overlap_org": "宁城县人民政府", "overlap_period": "present"},
    # 张三（于利民）本地成长干部，与其他从外地调任的常委差异
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "本地干部与京蒙协作挂职干部", "overlap_org": "宁城县人民政府", "overlap_period": "present"},
]


# ══════════════════════════════════════════════════════════════════════════════
# Person JSON Generator
# ══════════════════════════════════════════════════════════════════════════════

def make_source_register():
    return [
        {"id": "S001", "title": "宁城县政府网站—张文泽简历", "url": "http://www.ningchengxian.gov.cn/zwgk/xxgk/zfxxgkml/jgsz/ldzc/202501/t20250124_2531223.html", "publisher": "宁城县人民政府", "published_at": "2026-01-15", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "张文泽: 县委副书记、县长"},
        {"id": "S002", "title": "宁城县政府网站—卢振超简历", "url": "http://www.ningchengxian.gov.cn/zwgk/xxgk/zfxxgkml/jgsz/ldzc/202211/t20221124_1907659.html", "publisher": "宁城县人民政府", "published_at": "2026-01-15", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "卢振超: 县委常委、常务副县长"},
        {"id": "S003", "title": "宁城县政府网站—于利民简历", "url": "http://www.ningchengxian.gov.cn/zwgk/xxgk/zfxxgkml/jgsz/ldzc/202111/t20211118_1470013.html", "publisher": "宁城县人民政府", "published_at": "2026-01-15", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "于利民: 副县长"},
        {"id": "S004", "title": "宁城县政府网站—贾富强简历", "url": "http://www.ningchengxian.gov.cn/zwgk/xxgk/zfxxgkml/jgsz/ldzc/202403/t20240320_2281796.html", "publisher": "宁城县人民政府", "published_at": "2026-01-15", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "贾富强: 县委常委、副县长"},
        {"id": "S005", "title": "宁城县政府网站—赫连玉罡简历", "url": "http://www.ningchengxian.gov.cn/zwgk/xxgk/zfxxgkml/jgsz/ldzc/202403/t20240322_2283764.html", "publisher": "宁城县人民政府", "published_at": "2026-01-15", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "赫连玉罡: 县委常委、副县长"},
    ]


def make_person_json(person, timeline, relationships_list, source_register):
    """Build a person graph JSON following the schema."""
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "内蒙古自治区",
            "city": "赤峰市",
            "region": "宁城县",
            "job": person["current_post"],
            "task_id": "inner_mongolia_宁城县",
            "time_focus": "2024-2026"
        },
        "identity": {
            "person_id": f"ningchengxian_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "", "study_type": "unknown", "source_ids": ["S001"]}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}" if person["birth"] else person["name"],
                "name_birthplace": f"{person['name']}_{person['birthplace']}" if person["birthplace"] else person["name"],
                "official_profile_url": person.get("source", "")
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if person["id"] == 1 else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": relationships_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "cross_county_rotation" if person.get("birthplace", "").find("宁城") == -1 and person["id"] != 3 else "local_ladder",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "unknown",
                    "evidence": "信息不足无法判断",
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现负面公开记录", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "缺少完整职业履历（早期工作经历和教育细节）"
        },
        "open_questions": [
            {"priority": "high", "question": f"{person['name']}的完整职业履历是什么？", "why_it_matters": "无法分析晋升路径和跨部门经验", "suggested_queries": [f"{person['name']} 任职经历 简历"], "last_attempted": AS_OF},
        ]
    }


def build():
    print("=" * 60)
    print("  宁城县领导班子工作关系网络")
    print("  等级: 县")
    print(f"  调查日期: {AS_OF}")
    print("  信息来源: 宁城县人民政府官方网站")
    print("=" * 60)

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=str(DB_PATH),
        gexf_path=str(GEXF_PATH),
        overwrite=True,
    )

    print(f"\n  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── Generate Person Graph JSONs ──
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()

    person_data_map = {
        "张文泽": {
            "timeline": [
                {"start": "", "end": "present", "org": "宁城县人民政府", "title": "县长、政府党组书记", "notes": "主持县政府全面工作，分管审计局", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "", "end": "present", "org": "中共宁城县委员会", "title": "县委副书记", "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
            ],
            "relationships": [
                {"person": "卢振超", "person_id": "ningchengxian_卢振超", "relationship_type": "overlap", "strength": "strong", "evidence": "县长与常务副县长党政搭档", "overlap_org": "宁城县人民政府", "overlap_period": "present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
                {"person": "于利民", "person_id": "ningchengxian_于利民", "relationship_type": "overlap", "strength": "medium", "evidence": "县长与副县长工作关系", "overlap_org": "宁城县人民政府", "overlap_period": "present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
            ]
        },
        "卢振超": {
            "timeline": [
                {"start": "", "end": "present", "org": "宁城县人民政府", "title": "常务副县长", "notes": "负责县政府常务工作", "confidence": "confirmed", "source_ids": ["S002"]},
                {"start": "", "end": "present", "org": "中共宁城县委员会", "title": "县委常委", "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
            ],
            "relationships": [
                {"person": "张文泽", "person_id": "ningchengxian_张文泽", "relationship_type": "overlap", "strength": "strong", "evidence": "常务副县长与县长工作搭档", "overlap_org": "宁城县人民政府", "overlap_period": "present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
            ]
        },
        "于利民": {
            "timeline": [
                {"start": "", "end": "present", "org": "宁城县人民政府", "title": "副县长", "notes": "负责工业经济、招商引资、交通运输、市场监管", "confidence": "confirmed", "source_ids": ["S003"]},
            ],
            "relationships": [
                {"person": "张文泽", "person_id": "ningchengxian_张文泽", "relationship_type": "overlap", "strength": "medium", "evidence": "副县长与县长工作关系", "overlap_org": "宁城县人民政府", "overlap_period": "present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
            ]
        },
        "贾富强": {
            "timeline": [
                {"start": "", "end": "present", "org": "宁城县人民政府", "title": "副县长", "notes": "协助京蒙协作、对外开放和招商引资", "confidence": "confirmed", "source_ids": ["S004"]},
                {"start": "", "end": "present", "org": "中共宁城县委员会", "title": "县委常委", "notes": "", "confidence": "confirmed", "source_ids": ["S004"]},
                {"start": "1999年9月", "end": "2003年7月", "org": "北京理工大学", "title": "法学专业学生", "notes": "", "confidence": "confirmed", "source_ids": ["S004"]},
            ],
            "relationships": [
                {"person": "张文泽", "person_id": "ningchengxian_张文泽", "relationship_type": "overlap", "strength": "medium", "evidence": "县委常委、副县长与县长工作关系", "overlap_org": "中共宁城县委员会/宁城县人民政府", "overlap_period": "present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S004"]},
            ]
        },
        "赫连玉罡": {
            "timeline": [
                {"start": "", "end": "present", "org": "宁城县人民政府", "title": "副县长", "notes": "协助定点帮扶、对外开放和招商引资", "confidence": "confirmed", "source_ids": ["S005"]},
                {"start": "", "end": "present", "org": "中共宁城县委员会", "title": "县委常委", "notes": "", "confidence": "confirmed", "source_ids": ["S005"]},
            ],
            "relationships": [
                {"person": "张文泽", "person_id": "ningchengxian_张文泽", "relationship_type": "overlap", "strength": "medium", "evidence": "县委常委、副县长与县长工作关系", "overlap_org": "中共宁城县委员会/宁城县人民政府", "overlap_period": "present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S005"]},
            ]
        },
    }

    for p in persons:
        pname = p["name"]
        if pname in person_data_map:
            data = person_data_map[pname]
            pjson = make_person_json(p, data["timeline"], data["relationships"], source_register)
            pname_clean = pname
            # Determine job suffix
            job_map = {1: "县长", 2: "常务副县长", 3: "副县长", 4: "县委常委副县长", 5: "县委常委副县长"}
            job = job_map.get(p["id"], "副县长")
            pjson_path = PJSON_DIR / f"{TODAY}-内蒙古自治区-赤峰市-{job}-{pname_clean}.json"
            with open(pjson_path, "w", encoding="utf-8") as f:
                json.dump(pjson, f, ensure_ascii=False, indent=2)
            print(f"  Person JSON: {pjson_path.name}")

    print(f"\n所有 Person Graph JSONs 已生成到: {PJSON_DIR}")


if __name__ == "__main__":
    build()
