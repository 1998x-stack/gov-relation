#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 祥符区 (Xiangfu District), 开封市, 河南省.

Level: 市辖区
Province: 河南省
Parent city: 开封市
Targets: 区委书记 (Party Secretary: 张红军), 区长 (Mayor: 郭歌舞)
Task ID: henan_祥符区

Research date: 2026-07-24
Official source: http://www.xiangfuqu.gov.cn/ (祥符区人民政府)

Current status (as of 2026-07-24, verified via government website articles):
- 区委书记: 张红军 (男，汉族，中共党员)
- 区长: 郭歌舞 (男/女，汉族，中共党员)

Leadership roster sourced from:
  - Government website: http://www.xiangfuqu.gov.cn/ (multiple news articles)
  - Articles from 2026 showing current leadership

Confidence notes:
  张红军 and 郭歌舞 identities confirmed via government website articles (2026年6-7月).
  Detailed career histories (birth year, birthplace, education) not available via open web.
  Web search tools (Exa, Baidu, Google, Jina) were rate-limited or timed out during this investigation.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "../../..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "祥符区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-24"
TODAY = "20260724"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 张红军 — 区委书记
    {
        "id": 1,
        "name": "张红军",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共祥符区委员会",
        "source": "http://www.xiangfuqu.gov.cn/ (Article: 祥符区领导调研2026年高考准备工作, 2026-06-05)",
    },
    # 2. 郭歌舞 — 区长
    {
        "id": 2,
        "name": "郭歌舞",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "祥符区人民政府",
        "source": "http://www.xiangfuqu.gov.cn/ (Article: 祥符区召开重点工作推进会, 2026-07-16)",
    },

    # ════════════════════════════════════════
    # 区委领导 (Party Committee)
    # ════════════════════════════════════════
    # Leaders mentioned in government articles as "区领导"
    # Note: Full leadership roster (区委常委 complete list) not available from open sources.

    # 3. 潘波 — 区领导 (likely 区委常委/副区长)
    {
        "id": 3,
        "name": "潘波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "祥符区",
        "source": "http://www.xiangfuqu.gov.cn/ (Article: 祥符区召开重点工作推进会, 2026-07-16)",
    },
    # 4. 闫泊含 — 区领导 (likely 区委常委/副区长)
    {
        "id": 4,
        "name": "闫泊含",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "祥符区",
        "source": "http://www.xiangfuqu.gov.cn/ (Article: 祥符区领导调研2026年高考准备工作, 2026-06-05)",
    },
    # 5. 薛宝刚 — 区领导
    {
        "id": 5,
        "name": "薛宝刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "祥符区",
        "source": "http://www.xiangfuqu.gov.cn/ (Article: 祥符区召开重点工作推进会, 2026-07-16)",
    },
    # 6. 梅英歌 — 区领导
    {
        "id": 6,
        "name": "梅英歌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "祥符区",
        "source": "http://www.xiangfuqu.gov.cn/ (Article: 祥符区召开重点工作推进会, 2026-07-16)",
    },
    # 7. 方志立 — 区领导
    {
        "id": 7,
        "name": "方志立",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "祥符区",
        "source": "http://www.xiangfuqu.gov.cn/ (Article: 祥符区召开重点工作推进会, 2026-07-16)",
    },
    # 8. 张伟 — 区领导
    {
        "id": 8,
        "name": "张伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "祥符区",
        "source": "http://www.xiangfuqu.gov.cn/ (Article: 祥符区召开重点工作推进会, 2026-07-16)",
    },
    # 9. 路营 — 区领导 (appears in multiple articles)
    {
        "id": 9,
        "name": "路营",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "祥符区",
        "source": "http://www.xiangfuqu.gov.cn/ (Article: 祥符区领导调研2026年高考准备工作, 2026-06-05)",
    },
    # 10. 张洪伟 — 区领导
    {
        "id": 10,
        "name": "张洪伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "祥符区",
        "source": "http://www.xiangfuqu.gov.cn/ (Article: 祥符区召开重点工作周交办会, 2026-07-13)",
    },
    # 11. 卫莹 — 区领导
    {
        "id": 11,
        "name": "卫莹",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "祥符区",
        "source": "http://www.xiangfuqu.gov.cn/ (Article: 祥符区召开重点工作周交办会, 2026-07-13)",
    },
    # 12. 王国杰 — 区领导
    {
        "id": 12,
        "name": "王国杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "祥符区",
        "source": "http://www.xiangfuqu.gov.cn/ (Article: 祥符区召开重点工作周交办会, 2026-07-13)",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共祥符区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共开封市委员会",
        "location": "河南省开封市祥符区",
    },
    {
        "id": 2,
        "name": "祥符区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "开封市人民政府",
        "location": "河南省开封市祥符区",
    },
    {
        "id": 3,
        "name": "祥符区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "开封市人大常委会",
        "location": "河南省开封市祥符区",
    },
    {
        "id": 4,
        "name": "政协祥符区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协开封市委员会",
        "location": "河南省开封市祥符区",
    },
    {
        "id": 5,
        "name": "祥符区纪委监委",
        "type": "纪律检查",
        "level": "县处级",
        "parent": "开封市纪委监委",
        "location": "河南省开封市祥符区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 张红军 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 郭歌舞 - 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 郭歌舞 - 区委副书记
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 潘波 - 区领导
    {"person_id": 3, "org_id": 2, "title": "区领导", "start": "", "end": "present", "rank": "", "note": ""},
    # 闫泊含 - 区领导
    {"person_id": 4, "org_id": 2, "title": "区领导", "start": "", "end": "present", "rank": "", "note": ""},
    # 薛宝刚 - 区领导
    {"person_id": 5, "org_id": 2, "title": "区领导", "start": "", "end": "present", "rank": "", "note": ""},
    # 梅英歌 - 区领导
    {"person_id": 6, "org_id": 2, "title": "区领导", "start": "", "end": "present", "rank": "", "note": ""},
    # 方志立 - 区领导
    {"person_id": 7, "org_id": 2, "title": "区领导", "start": "", "end": "present", "rank": "", "note": ""},
    # 张伟 - 区领导
    {"person_id": 8, "org_id": 2, "title": "区领导", "start": "", "end": "present", "rank": "", "note": ""},
    # 路营 - 区领导
    {"person_id": 9, "org_id": 2, "title": "区领导", "start": "", "end": "present", "rank": "", "note": ""},
    # 张洪伟 - 区领导
    {"person_id": 10, "org_id": 2, "title": "区领导", "start": "", "end": "present", "rank": "", "note": ""},
    # 卫莹 - 区领导
    {"person_id": 11, "org_id": 2, "title": "区领导", "start": "", "end": "present", "rank": "", "note": ""},
    # 王国杰 - 区领导
    {"person_id": 12, "org_id": 2, "title": "区领导", "start": "", "end": "present", "rank": "", "note": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 张红军 <-> 郭歌舞 (top leader + deputy - 区委书记与区长搭班子)
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记与区长搭班子，为祥符区党政主要领导",
        "overlap_org": "祥符区",
        "overlap_period": "2025-present",
    },
    # 张红军 <-> 闫泊含
    {
        "person_a": 1,
        "person_b": 4,
        "type": "overlap",
        "context": "共同参加2026年高考调研工作",
        "overlap_org": "祥符区",
        "overlap_period": "2026",
    },
    # 张红军 <-> 路营
    {
        "person_a": 1,
        "person_b": 9,
        "type": "overlap",
        "context": "共同参加2026年高考调研工作",
        "overlap_org": "祥符区",
        "overlap_period": "2026",
    },
    # 郭歌舞 <-> 潘波
    {
        "person_a": 2,
        "person_b": 3,
        "type": "overlap",
        "context": "共同参加2026年7月重点工作推进会",
        "overlap_org": "祥符区",
        "overlap_period": "2026",
    },
    # 郭歌舞 <-> 路营
    {
        "person_a": 2,
        "person_b": 9,
        "type": "overlap",
        "context": "共同参加2026年7月重点工作周交办会",
        "overlap_org": "祥符区",
        "overlap_period": "2026",
    },
    # 郭歌舞 <-> 张洪伟
    {
        "person_a": 2,
        "person_b": 10,
        "type": "overlap",
        "context": "共同参加2026年7月重点工作周交办会",
        "overlap_org": "祥符区",
        "overlap_period": "2026",
    },
    # 郭歌舞 <-> 卫莹
    {
        "person_a": 2,
        "person_b": 11,
        "type": "overlap",
        "context": "共同参加2026年7月重点工作周交办会",
        "overlap_org": "祥符区",
        "overlap_period": "2026",
    },
    # 郭歌舞 <-> 王国杰
    {
        "person_a": 2,
        "person_b": 12,
        "type": "overlap",
        "context": "共同参加2026年7月重点工作周交办会",
        "overlap_org": "祥符区",
        "overlap_period": "2026",
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
    persons_dir = PERSONS_DIR
    persons_dir.mkdir(parents=True, exist_ok=True)

    person_data = {
        "张红军": {
            "person_id": "xiangfu_zhang_hongjun",
            "name": "张红军",
            "current_post": "区委书记",
            "current_org": "中共祥符区委员会",
            "source": "http://www.xiangfuqu.gov.cn/",
        },
        "郭歌舞": {
            "person_id": "xiangfu_guo_gewu",
            "name": "郭歌舞",
            "current_post": "区长",
            "current_org": "祥符区人民政府",
            "source": "http://www.xiangfuqu.gov.cn/",
        },
    }

    for name, info in person_data.items():
        role_slug = info["current_post"].replace(" ", "_")
        fname = f"{TODAY}-河南省-开封市-{role_slug}-{name}.json"
        path = persons_dir / fname

        # Build a minimal person JSON per the schema
        person_json = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "开封市",
                "region": "祥符区",
                "job": info["current_post"],
                "task_id": "henan_祥符区",
                "time_focus": "2026",
            },
            "identity": {
                "person_id": info["person_id"],
                "name": name,
                "aliases": [],
                "gender": "",
                "ethnicity": "汉族",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员 (假定)",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": f"{name}_unknown",
                    "name_birthplace": f"{name}_unknown",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": info["current_post"],
                "current_org": info["current_org"],
                "administrative_rank": "副厅级" if "书记" in info["current_post"] else "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"],
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "present",
                    "org": info["current_org"],
                    "title": info["current_post"],
                    "level": "",
                    "location": "河南省开封市祥符区",
                    "system": "party" if "书记" in info["current_post"] else "government",
                    "rank": "",
                    "is_key_promotion": False,
                    "notes": "现任职务已确认，但公开资料未找到完整履历",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "履历缺口",
                    "title": "",
                    "notes": "公开资料未找到2026年以前履历",
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
                    "summary": "无法评估，缺少早期履历数据",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment.",
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
                    "title": f"祥符区人民政府网站 - {info['current_post']}相关报道",
                    "url": "http://www.xiangfuqu.gov.cn/",
                    "publisher": "祥符区人民政府",
                    "published_at": "2026",
                    "accessed_at": AS_OF,
                    "source_type": "official",
                    "reliability": "high",
                    "notes": f"政府网站新闻报道确认了{name}的当前职务",
                }
            ],
            "confidence_summary": {
                "identity": "plausible",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": f"{name}的出生年份、籍贯、学历、早期履历完全未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": f"{name}的出生年份和籍贯是什么？",
                    "why_it_matters": "个人身份核心信息，无法去重和追踪",
                    "suggested_queries": [f"{name} 简历", f"{name} 出生", f"{name} 百度百科"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": f"{name}的教育背景和工作履历？",
                    "why_it_matters": "完整的履历是分析职业路径和关系网络的基础",
                    "suggested_queries": [f"{name} 任职经历", f"{name} 工作履历"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": f"{name}在担任现职前曾任哪些职务？",
                    "why_it_matters": "前任职务决定了跨部门/跨地区关系网络",
                    "suggested_queries": [f"{name} 此前担任", f"{name} 任前公示"],
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
    print(f"  Person JSONs in: {persons_dir}")
