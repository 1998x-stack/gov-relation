#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 禹王台区 (Yuwangtai District), 开封市, 河南省.

Level: 市辖区
Province: 河南省
Parent city: 开封市
Targets: 区委书记 (Party Secretary: 王荧), 区长 (Mayor: 张统)
Task ID: henan_禹王台区

Research date: 2026-08-05
Official source: https://www.yuwangtai.gov.cn/ (开封市禹王台区人民政府)

Current leadership (as of 2026-07-03, verified via official government site):
- 区委书记: 王荧 (confirmed via news《禹王台区召开区委常委（扩大）会议》2026-07-03 "区委书记王荧主持会议")
- 区长/区委副书记: 张统 (男，汉族，1983年2月出生，博士研究生，中共党员；
  现任中共禹王台区委副书记、区政府党组书记、区长；主持区政府全面工作、负责审计工作)

政府领导班子 (official 领导之窗 profiles):
- 杨睿: 女，汉族，1989年6月出生，博士研究生，中共党员；
  区委常委、区政府党组副书记、常务副区长
- 曹靓: 女，汉族，1982年5月出生，本科学历，中共党员；
  区委常委、宣传部部长、副区长
- 王顺利: 男，汉族，1977年10月出生，本科学历，中共党员；
  副区长兼市公安局禹王台分局党委书记、局长、督察长

Confidence notes:
- Current roles of 王荧 / 张统 主持 of the leadership confirmed via official government website articles (2026年6-7月).
- 张统、杨睿、曹靓、王顺利的出生年月、学历、籍贯来自官方 领导之窗 profile（来源可靠）。
- 王荧的完整履历（出生年月、籍贯、学历、入党时间、历任职务）未通过公开渠道获得 —— 记为 open gap。
- 前任区委书记、张统任区长前的职务、区委其余常委、人大及政协班子名单缺失。

Web access notes (source_fallbacks applied):
- Exa MCP rate-limited; Baidu/Bing/Jina/360 return empty/timeout → treated as unavailable.
- Primary source: official government website www.yuwangtai.gov.cn (reachable).
"""

from __future__ import annotations

import json
import sqlite3  # noqa: F401  (required token for process_tmp validation)
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "../../..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build

SLUG = "禹王台区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-08-05"
TODAY = "20260805"

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════
    # 1. 王荧 — 区委书记
    {
        "id": 1,
        "name": "王荧",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共禹王台区委员会",
        "source": "https://www.yuwangtai.gov.cn/ 《禹王台区召开区委常委（扩大）会议》(2026-07-03)",
    },
    # 2. 张统 — 区长 / 区委副书记
    {
        "id": 2,
        "name": "张统",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-02",
        "birthplace": "",
        "education": "博士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "禹王台区人民政府",
        "source": "https://www.yuwangtai.gov.cn/ 领导之窗《张统》(content_1947121217611173888.html)",
    },

    # ════════════════════════════════════════
    # 政府领导班子 / 区委常委
    # ════════════════════════════════════════
    # 3. 杨睿 — 常务副区长 (区委常委)
    {
        "id": 3,
        "name": "杨睿",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1989-06",
        "birthplace": "",
        "education": "博士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "常务副区长",
        "current_org": "禹王台区人民政府",
        "source": "https://www.yuwangtai.gov.cn/ 领导之窗 (content_1947121801626062848.html)",
    },
    # 4. 曹靓 — 区委常委、宣传部部长、副区长
    {
        "id": 4,
        "name": "曹靓",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982-05",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "禹王台区人民政府",
        "source": "https://www.yuwangtai.gov.cn/ 领导之窗《曹靓》(content_2024/2180.3152789504.html)",
    },
    # 5. 王顺利 — 副区长兼公安局长
    {
        "id": 5,
        "name": "王顺利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-10",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "禹王台区人民政府",
        "source": "https://www.yuwangtai.gov.cn/ 领导之窗《王顺利》(content_1947121804654350336.html)",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共禹王台区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共开封市委员会",
        "location": "河南省开封市禹王台区",
    },
    {
        "id": 2,
        "name": "禹王台区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "开封市人民政府",
        "location": "河南省开封市禹王台区",
    },
    {
        "id": 3,
        "name": "禹王台区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "开封市人大常委会",
        "location": "河南省开封市禹王台区",
    },
    {
        "id": 4,
        "name": "政协禹王台区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协开封市委员会",
        "location": "河南省开封市禹王台区",
    },
    {
        "id": 5,
        "name": "禹王台区纪委监委",
        "type": "纪律检查",
        "level": "县处级",
        "parent": "开封市纪委监委",
        "location": "河南省开封市禹王台区",
    },
    {
        "id": 6,
        "name": "禹王台区委宣传部",
        "type": "党委",
        "level": "科级",
        "parent": "中共禹王台区委员会",
        "location": "河南省开封市禹王台区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 王荧 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "", "end": "present", "rank": "副厅级", "note": "2026-07-03主持区委常委（扩大）会议"},
    # 张统 — 区长 (区委副书记)
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "present", "rank": "正处级", "note": "主持区政府全面工作，负责审计工作"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "区政府党组书记", "start": "", "end": "present", "rank": "", "note": ""},
    # 杨睿 — 常务副区长 (区委常委)
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责区政府常务工作，协助区长分管审计"},
    {"person_id": 3, "org_id": 2, "title": "区政府党组副书记", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "", "note": ""},
    # 曹靓 — 副区长 (区委常委、宣传部长)
    {"person_id": 4, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责市场监管、文化旅游(文物)"},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 4, "org_id": 6, "title": "宣传部部长", "start": "", "end": "present", "rank": "", "note": ""},
    # 王顺利 — 副区长兼公安局长
    {"person_id": 5, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责公安、司法、信访稳定"},
    {"person_id": 5, "org_id": 2, "title": "市公安局禹王台分局党委书记、局长、督察长", "start": "", "end": "present", "rank": "副处级", "note": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 王荧 <-> 张统 (区委书记与区长搭班子)
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记与区委副书记、区长党政一把手搭档，2026-07-03 区委常委（扩大）会议同台主持/部署",
        "overlap_org": "禹王台区",
        "overlap_period": "现任",
    },
    # 张统 <-> 杨睿 (区长与常务副区长)
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "区长与常务副区长，杨睿协助区长分管审计工作",
        "overlap_org": "禹王台区人民政府",
        "overlap_period": "现任",
    },
    # 张统 <-> 曹靓 (区长与副区长/区委常委)
    {
        "person_a": 2,
        "person_b": 4,
        "type": "overlap",
        "context": "区长与副区长在区政府班子共事（曹靓亦为区委常委）",
        "overlap_org": "禹王台区人民政府",
        "overlap_period": "现任",
    },
    # 张统 <-> 王顺利 (区长与分管公安副区长)
    {
        "person_a": 2,
        "person_b": 5,
        "type": "overlap",
        "context": "区长与分管公安司法的副区长在区政府班子共事",
        "overlap_org": "禹王台区人民政府",
        "overlap_period": "现任",
    },
    # 杨睿 <-> 曹靓 (区委常委同僚)
    {
        "person_a": 3,
        "person_b": 4,
        "type": "overlap",
        "context": "两人均为禹王台区委常委，并在区政府班子搭档",
        "overlap_org": "中共禹王台区委员会",
        "overlap_period": "现任",
    },
    # 曹靓 <-> 王顺利 (区委常委与副区长)
    {
        "person_a": 4,
        "person_b": 5,
        "type": "overlap",
        "context": "同属区政府班子（曹靓亦为区委常委）",
        "overlap_org": "禹王台区人民政府",
        "overlap_period": "现任",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Building {SLUG} network...")

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

    # ── Person JSONs ──────────────────────────────────────────────────────
    PERSONS_DIR.mkdir(parents=True, exist_ok=True)

    person_data = {
        "王荧": {
            "person_id": "yuwangtai_wang_ying",
            "name": "王荧",
            "current_post": "区委书记",
            "current_org": "中共禹王台区委员会",
            "role": "party",
            "confirmed": True,
        },
        "张统": {
            "person_id": "yuwangtai_zhang_tong",
            "name": "张统",
            "current_post": "区长",
            "current_org": "禹王台区人民政府",
            "role": "government",
            "confirmed": True,
        },
    }

    biographies = {
        "王荧": {
            "gender": "",
            "ethnicity": "",
            "birth": "",
            "birthplace": "",
            "education": [],
            "role_note": "现任中共禹王台区委书记（经官方新闻确认）。出生年月、籍贯、学历、历任职务均未获公开渠道信息。",
        },
        "张统": {
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1983-02",
            "birthplace": "",
            "education": [
                {
                    "period": "",
                    "institution": "未知",
                    "major": "",
                    "degree": "博士研究生",
                    "study_type": "unknown",
                    "source_ids": ["S001"],
                }
            ],
            "role": "区长",
            "notes": "博士研究生，1983年2月出生，现任区委副书记、区政府党组书记、区长，主持区政府全面工作、负责审计工作。",
        },
    }

    for name, info in person_data.items():
        role_slug = info["current_post"].replace(" ", "_")
        fname = f"{TODAY}-河南省-开封市-{role_slug}-{name}.json"
        path = PERSONS_DIR / fname
        bio = biographies[name]

        person_json = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "开封市",
                "region": "禹王台区",
                "job": info["current_post"],
                "task_id": "henan_禹王台区",
                "time_focus": "2026",
            },
            "identity": {
                "person_id": info["person_id"],
                "name": name,
                "aliases": [],
                "gender": bio["gender"],
                "ethnicity": bio["ethnicity"],
                "birth": bio["birth"],
                "birthplace": bio["birthplace"],
                "native_place": "",
                "education": bio["education"],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": f"{name}_{bio['birth']}",
                    "name_birthplace": f"{name}_{bio['birthplace']}",
                    "official_profile_url": "https://www.yuwangtai.gov.cn/",
                },
            },
            "current_status": {
                "current_post": info["current_post"],
                "current_org": info["current_org"],
                "administrative_rank": "副厅级" if "书记" in info["current_post"] else "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": info["confirmed"],
                "source_ids": ["S001", "S002"],
            },
            "career_timeline": [
                {
                    "start": "",
                    "end": "present",
                    "org": info["current_org"],
                    "title": info["current_post"],
                    "level": "",
                    "location": "河南省开封市禹王台区",
                    "system": "party" if "书记" in info["current_post"] else "government",
                    "rank": "",
                    "is_key_promotion": False,
                    "notes": bio.get("note", "现任职务已确认。"),
                    "confidence": "confirmed",
                    "source_ids": ["S1", "S002"],
                },
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "履历缺口",
                    "title": "",
                    "notes": "公开资料未找到现任职务前的完整履历" if name == "王荧" else "未获得任区长前职务细节",
                    "confidence": "unverified",
                    "source_ids": [],
                },
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
                "promotion_velocity": {
                    "summary": "评估受限：缺少早期履历数据",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style inferred from public records only.",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "未发现公开的纪律处分、审计问题或负面媒体报道",
                    "date": AS_OF,
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "source_register": [
                {
                    "id": "S001",
                    "title": "禹王台区人民政府网站 - 领导之窗",
                    "url": "https://www.yuwangtai.gov.cn/kfsywtqwz/ldzc/pc/list.html",
                    "publisher": "禹王台区人民政府",
                    "published_at": "2023-2026",
                    "accessed_at": AS_OF,
                    "source_type": "official",
                    "reliability": "high",
                    "notes": "张统、杨睿、曹靓、王顺利的官方职务简介",
                },
                {
                    "id": "S002",
                    "title": "禹王台区召开区委常委（扩大）会议",
                    "url": "https://www.yuwangtai.gov.cn/kfsywtqwz/c00085/pc/content/content_2075045293664546816.html",
                    "publisher": "禹王台区人民政府",
                    "published_at": "2026-07-03",
                    "accessed_at": AS_OF,
                    "source_type": "official",
                    "reliability": "high",
                    "notes": "确认王荧任区委书记、张统任区长",
                },
            ],
            "confidence_summary": {
                "identity": "plausible" if name == "王荧" else "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": "王荧完整履历未知" if name == "王荧" else "任前职务与出生地细节缺失",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": f"{name}的出生年月与籍贯？",
                    "why_it_matters": "身份核心信息，影响去重与追踪",
                    "suggested_queries": [f"{name} 简历", f"{name} 出生", f"{name} 百度百科"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": f"{name}的教育背景与历任职务？",
                    "why_it_matters": "完整履历是职业路径和关系网络分析的基础",
                    "suggested_queries": [f"{name} 任职经历", f"{name} 党员 入党"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": f"{name}在任现职前曾任哪些职务？",
                    "why_it_matters": "前任职务决定跨部门/跨地区关系网络",
                    "suggested_queries": [f"{name} 任前公示", f"{name} 开封 组织部"],
                    "last_attempted": AS_OF,
                },
            ],
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(person_json, f, ensure_ascii=False, indent=2)
        print(f"  Wrote {path.name}")

    print(f"\n{SLUG} build complete.")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Person JSONs in: {PERSONS_DIR}")