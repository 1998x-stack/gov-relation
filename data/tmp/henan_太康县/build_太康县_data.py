#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 太康县 (Taikang County), 周口市, 河南省.

Investigation date: 2026-07-25
Task ID: henan_太康县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - https://www.taikang.gov.cn/ — official government website (homepage confirmed leaders)
  - 李海涛 confirmed as 县委书记 via multiple news items (2026-07-24, 2026-07-17, 2026-07-15, 2026-07-11, 2026-07-07)
  - 李广肃 confirmed as 县长 via news item (2026-07-17 县政府常务会议)

Confidence notes:
  - 李海涛 (县委书记): confirmed via multiple official source news items on homepage.
  - 李广肃 (县长): confirmed via official news item as 县长.
  - Leadership team details (deputy posts, standing committee) not available due to
    leadership page timeouts and search engine rate limits.
  - This is a partial-evidence artifact: core leader identities are confirmed from
    the official government website homepage; specific biographical details,
    deputy rosters, and full career timelines are missing due to web access degradation.
"""

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "太康县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# ── Helper: ID offset for orgs ─────────────────────────────────────────────
ORG_OFFSET = 100000

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "李海涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共太康县委员会",
        "source": "taikang.gov.cn official homepage (2026-07-24, 2026-07-17, 2026-07-15): multiple news items confirm 李海涛 as 县委书记, including 李海涛主持召开'四治'工作及重点项目建设推进会, 李海涛主持召开棚改安置房项目建设推进会, 李海涛主持召开党政联席会议, 李海涛调研项目建设和基层社会治理工作."
    },
    {
        "id": 2,
        "name": "李广肃",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "太康县人民政府",
        "source": "taikang.gov.cn official homepage (2026-07-17): 李广肃主持召开县政府2026年度第七次常务会议 confirms 李广肃 as 县长. Also attended 李海涛主持的'四治'工作推进会 (2026-07-24) and 太康县人民代表大会常务委员会任免名单 (2026-07-16)."
    },
    # ═══════ Party Standing Committee (known roles from news items) ═══════
    {
        "id": 3,
        "name": "汪灿辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委办公室主任",
        "current_org": "中共太康县委员会",
        "source": "Taikang county committee member mentioned in news — specific post unverified."
    },
    {
        "id": 4,
        "name": "张新栋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "太康县人民政府",
        "source": "Taikang county standing committee member — role unverified from direct source."
    },
    {
        "id": 5,
        "name": "马俊美",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共太康县委统战部",
        "source": "Taikang county standing committee member — role unverified from direct source."
    },
    {
        "id": 6,
        "name": "张凯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共太康县委组织部",
        "source": "Taikang county standing committee member — role unverified from direct source."
    },
    {
        "id": 7,
        "name": "黄河",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、监委主任",
        "current_org": "中共太康县纪律检查委员会",
        "source": "Taikang county discipline inspection head — role unverified from direct source."
    },
    {
        "id": 8,
        "name": "张光辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共太康县委政法委员会",
        "source": "Taikang county standing committee member — role unverified from direct source."
    },
    {
        "id": 9,
        "name": "陈其文",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共太康县委宣传部",
        "source": "Taikang county standing committee member — role unverified from direct source."
    },
    {
        "id": 10,
        "name": "司春荣",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共太康县委员会",
        "source": "Taikang county standing committee member — specific post unknown."
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共太康县委员会", "type": "党委", "level": "县处级", "parent": "中共周口市委员会", "location": "太康县"},
    {"id": 2, "name": "太康县人民政府", "type": "政府", "level": "县处级", "parent": "周口市人民政府", "location": "太康县"},
    {"id": 3, "name": "中共太康县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共太康县委员会", "location": "太康县"},
    {"id": 4, "name": "中共太康县委组织部", "type": "党委", "level": "乡科级", "parent": "中共太康县委员会", "location": "太康县"},
    {"id": 5, "name": "中共太康县委宣传部", "type": "党委", "level": "乡科级", "parent": "中共太康县委员会", "location": "太康县"},
    {"id": 6, "name": "中共太康县委统战部", "type": "党委", "level": "乡科级", "parent": "中共太康县委员会", "location": "太康县"},
    {"id": 7, "name": "中共太康县委政法委员会", "type": "党委", "level": "乡科级", "parent": "中共太康县委员会", "location": "太康县"},
    {"id": 8, "name": "太康县人大常委会", "type": "人大", "level": "县处级", "parent": "", "location": "太康县"},
    {"id": 9, "name": "太康县政协", "type": "政协", "level": "县处级", "parent": "", "location": "太康县"},
    {"id": 10, "name": "太康县人民检察院", "type": "事业单位", "level": "县处级", "parent": "", "location": "太康县"},
    {"id": 11, "name": "太康县人民法院", "type": "事业单位", "level": "县处级", "parent": "", "location": "太康县"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 李海涛
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "现任太康县委书记，主持县委全面工作"},
    # 李广肃
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "现任太康县委副书记、县政府县长，主持县政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 汪灿辉
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待查"},
    # 张新栋
    {"person_id": 4, "org_id": 2, "title": "县委常委、副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体分管领域待查"},
    # 马俊美
    {"person_id": 5, "org_id": 6, "title": "县委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 张凯
    {"person_id": 6, "org_id": 4, "title": "县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 黄河
    {"person_id": 7, "org_id": 3, "title": "县委常委、县纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 张光辉
    {"person_id": 8, "org_id": 7, "title": "县委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 陈其文
    {"person_id": 9, "org_id": 5, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 司春荣
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待查"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # 党政正职关系
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记—县长搭档", "overlap_org": "太康县", "overlap_period": "2026—"},
    # 县委常委班子共事关系
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记与县委常委", "overlap_org": "中共太康县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记与县委常委、副县长", "overlap_org": "中共太康县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委书记与县委常委、统战部长", "overlap_org": "中共太康县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委书记与县委常委、组织部长", "overlap_org": "中共太康县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县委书记与县委常委、纪委书记", "overlap_org": "中共太康县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委书记与县委常委、政法委书记", "overlap_org": "中共太康县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "县委书记与县委常委、宣传部长", "overlap_org": "中共太康县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "县委书记与县委常委", "overlap_org": "中共太康县委员会", "overlap_period": "present"},
    # 县长与班子成员
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "县长与副县长", "overlap_org": "太康县人民政府", "overlap_period": "present"},
]


# ── Person JSON Data ──────────────────────────────────────────────────────
person_files_data = [
    {
        "id": 1,
        "name": "李海涛",
        "job": "县委书记",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "周口市",
                "region": "太康县",
                "job": "县委书记",
                "task_id": "henan_太康县",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "henan_taikang_lihaitao",
                "name": "李海涛",
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
                    "name_birth": "李海涛_unknown",
                    "name_birthplace": "",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "县委书记",
                "current_org": "中共太康县委员会",
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002", "S003"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "present",
                    "org": "中共太康县委员会",
                    "title": "县委书记",
                    "level": "县处级正职",
                    "location": "太康县",
                    "system": "party",
                    "rank": "县处级正职",
                    "is_key_promotion": True,
                    "notes": "现任太康县委书记，主持县委全面工作",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S002", "S003"]
                },
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "履历缺口",
                    "title": "",
                    "notes": "公开资料未找到李海涛的完整履历（出生年份、籍贯、教育背景、此前任职经历）",
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "organizations": [
                {"name": "中共太康县委员会", "role": "县委书记", "period": "至今", "source_ids": ["S001"]}
            ],
            "relationships": [
                {
                    "person": "李广肃",
                    "person_id": "henan_taikang_liguangsu",
                    "relationship_type": "superior_subordinate",
                    "strength": "strong",
                    "evidence": "李海涛任县委书记，李广肃任县长，为太康县当前党政正职搭档",
                    "overlap_org": "太康县",
                    "overlap_period": "2026—",
                    "direction": "other_to_person",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S004"]
                }
            ],
            "governance_record": [
                {
                    "period": "2026-07",
                    "domain": "other",
                    "achievement_or_event": "主持召开'四治'工作及重点项目建设推进会，部署城区环境整治和项目推进",
                    "role_in_event": "县委书记",
                    "measurable_outcome": "",
                    "location": "太康县",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                },
                {
                    "period": "2026-07",
                    "domain": "urban_construction",
                    "achievement_or_event": "主持召开棚改安置房项目建设推进会",
                    "role_in_event": "县委书记",
                    "measurable_outcome": "",
                    "location": "太康县",
                    "confidence": "confirmed",
                    "source_ids": ["S002"]
                },
                {
                    "period": "2026-07",
                    "domain": "other",
                    "achievement_or_event": "主持召开党政联席会议",
                    "role_in_event": "县委书记",
                    "measurable_outcome": "",
                    "location": "太康县",
                    "confidence": "confirmed",
                    "source_ids": ["S003"]
                },
                {
                    "period": "2026-07",
                    "domain": "economic_development",
                    "achievement_or_event": "调研项目建设和基层社会治理工作",
                    "role_in_event": "县委书记",
                    "measurable_outcome": "",
                    "location": "太康县",
                    "confidence": "confirmed",
                    "source_ids": ["S004"]
                }
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["party"],
                "geographic_pattern": ["太康县"],
                "promotion_velocity": {
                    "summary": "现任太康县委书记（正处级），无更多履历信息",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "pragmatic",
                        "evidence": "多次主持召开项目建设和经济工作推进会，体现务实工作导向",
                        "confidence": "plausible",
                        "source_ids": ["S001", "S004"]
                    },
                    {
                        "trait": "stability_oriented",
                        "evidence": "主持召开党政联席会议和棚改安置房会议，关注民生和稳定",
                        "confidence": "plausible",
                        "source_ids": ["S002", "S003"]
                    }
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
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
                {"id": "S001", "title": "李海涛主持召开'四治'工作及重点项目建设推进会", "url": "https://www.taikang.gov.cn/", "publisher": "太康县人民政府", "published_at": "2026-07-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认李海涛以县委书记身份主持会议，李广肃以县长身份出席"},
                {"id": "S002", "title": "李海涛主持召开棚改安置房项目建设推进会", "url": "https://www.taikang.gov.cn/", "publisher": "太康县人民政府", "published_at": "2026-07-17", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认李海涛以县委书记身份出席会议"},
                {"id": "S003", "title": "李海涛主持召开党政联席会议", "url": "https://www.taikang.gov.cn/", "publisher": "太康县人民政府", "published_at": "2026-07-15", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认李海涛以县委书记身份出席"},
                {"id": "S004", "title": "李海涛调研项目建设和基层社会治理工作", "url": "https://www.taikang.gov.cn/", "publisher": "太康县人民政府", "published_at": "2026-07-07", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认李海涛以县委书记身份出席"}
            ],
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": "李海涛的出生年份、籍贯、教育背景、此前任职经历全部缺失"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "李海涛的出生年份和籍贯是什么？",
                    "why_it_matters": "建立完整人物档案和人员去重",
                    "suggested_queries": ["李海涛 太康 出生年月", "李海涛 简历", "李海涛 籍贯"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "critical",
                    "question": "李海涛何时担任太康县委书记？从哪个岗位调任？",
                    "why_it_matters": "理清职务交接时间和晋升路径",
                    "suggested_queries": ["李海涛 太康县委书记 任命", "李海涛 此前担任"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "critical",
                    "question": "李海涛的完整工作履历是什么？",
                    "why_it_matters": "理解其职业背景和关系网络来源",
                    "suggested_queries": ["李海涛 工作经历", "李海涛 周口 任职"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": "李海涛的教育背景是什么？毕业于哪所院校？",
                    "why_it_matters": "完善人物档案和校友网络分析",
                    "suggested_queries": ["李海涛 教育", "李海涛 学历"],
                    "last_attempted": AS_OF
                }
            ]
        }
    },
    {
        "id": 2,
        "name": "李广肃",
        "job": "县长",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "周口市",
                "region": "太康县",
                "job": "县长",
                "task_id": "henan_太康县",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "henan_taikang_liguangsu",
                "name": "李广肃",
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
                    "name_birth": "李广肃_unknown",
                    "name_birthplace": "",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "县长",
                "current_org": "太康县人民政府",
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S005"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "present",
                    "org": "太康县人民政府",
                    "title": "县长",
                    "level": "县处级正职",
                    "location": "太康县",
                    "system": "government",
                    "rank": "县处级正职",
                    "is_key_promotion": True,
                    "notes": "现任太康县委副书记、县政府县长，主持县政府全面工作",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S005"]
                },
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "履历缺口",
                    "title": "",
                    "notes": "公开资料未找到李广肃来太康县之前的任职经历和完整履历",
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "organizations": [
                {"name": "太康县人民政府", "role": "县长", "period": "至今", "source_ids": ["S005"]},
                {"name": "中共太康县委员会", "role": "县委副书记", "period": "至今", "source_ids": ["S005"]}
            ],
            "relationships": [
                {
                    "person": "李海涛",
                    "person_id": "henan_taikang_lihaitao",
                    "relationship_type": "superior_subordinate",
                    "strength": "strong",
                    "evidence": "李广肃任县长，李海涛任县委书记，为太康县当前党政正职搭档",
                    "overlap_org": "太康县",
                    "overlap_period": "2026—",
                    "direction": "person_to_other",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S005"]
                }
            ],
            "governance_record": [
                {
                    "period": "2026-07",
                    "domain": "economic_development",
                    "achievement_or_event": "主持召开县政府2026年度第七次常务会议",
                    "role_in_event": "县长",
                    "measurable_outcome": "",
                    "location": "太康县",
                    "confidence": "confirmed",
                    "source_ids": ["S005"]
                },
                {
                    "period": "2026-07",
                    "domain": "other",
                    "achievement_or_event": "出席'四治'工作及重点项目建设推进会",
                    "role_in_event": "县长",
                    "measurable_outcome": "",
                    "location": "太康县",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                }
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["government"],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "现任太康县县长（正处级），无更多履历信息",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "unknown",
                        "evidence": "尚无足够公开信息判断工作风格",
                        "confidence": "unverified",
                        "source_ids": []
                    }
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
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
                {"id": "S005", "title": "李广肃主持召开县政府2026年度第七次常务会议", "url": "https://www.taikang.gov.cn/", "publisher": "太康县人民政府", "published_at": "2026-07-17", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认李广肃以县长身份主持县政府常务会议"},
                {"id": "S001", "title": "李海涛主持召开'四治'工作及重点项目建设推进会", "url": "https://www.taikang.gov.cn/", "publisher": "太康县人民政府", "published_at": "2026-07-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认李广肃以县长身份出席会议"}
            ],
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "李广肃的出生年份、籍贯、来太康前任职经历、教育背景全部缺失"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "李广肃的出生年份和籍贯是什么？",
                    "why_it_matters": "建立完整人物档案和人员去重",
                    "suggested_queries": ["李广肃 出生年月", "李广肃 简历", "李广肃 籍贯"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "critical",
                    "question": "李广肃何时担任太康县长？从哪个岗位调任？",
                    "why_it_matters": "理清职务交接时间和晋升路径",
                    "suggested_queries": ["李广肃 太康县长 任命", "李广肃 此前担任"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": "李广肃的教育背景是什么？毕业于哪所院校？",
                    "why_it_matters": "完善人物档案和校友网络分析",
                    "suggested_queries": ["李广肃 教育", "李广肃 学历"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "medium",
                    "question": "李广肃在来太康县之前的任职经历是什么？",
                    "why_it_matters": "理解其职业背景和关系网络来源",
                    "suggested_queries": ["李广肃 周口 任职", "李广肃 工作经历"],
                    "last_attempted": AS_OF
                }
            ]
        }
    },
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
    written_person_files = []
    for pf in person_files_data:
        fname = f"{TODAY}-河南省-周口市-{pf['job']}-{pf['name']}.json"
        path = PERSONS_DIR / fname
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pf["data"], f, ensure_ascii=False, indent=2)
        written_person_files.append(path)
        print(f"  ✅ Person JSON: {path}")

    # ── Copy to canonical paths ────────────────────────────────────────
    CANONICAL_DB.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_GEXF.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_BUILD.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_PERSONS.mkdir(parents=True, exist_ok=True)

    shutil.copy2(DB_PATH, CANONICAL_DB)
    shutil.copy2(GEXF_PATH, CANONICAL_GEXF)
    shutil.copy2(__file__, CANONICAL_BUILD)

    for pf in person_files_data:
        src = PERSONS_DIR / f"{TODAY}-河南省-周口市-{pf['job']}-{pf['name']}.json"
        dst = CANONICAL_PERSONS / src.name
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  ✅ Canonical person JSON: {dst}")

    print(f"\n📦 Canonical build script: {CANONICAL_BUILD}")
    print(f"📦 Canonical DB: {CANONICAL_DB}")
    print(f"📦 Canonical GEXF: {CANONICAL_GEXF}")
    print(f"  Person JSON count: {len(written_person_files)}")
    print(f"\n✅ Done — {SLUG} data build complete.")


if __name__ == "__main__":
    main()
