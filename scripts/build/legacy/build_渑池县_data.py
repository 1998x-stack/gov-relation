#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 渑池县 (Mianchi County), 三门峡市, 河南省.

Investigation date: 2026-07-24
Task ID: henan_渑池县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - Official website: www.mianchi.gov.cn (leadership page, news articles)
  - News article dated 2026-07-24: confirms 钱程 as 县委书记, 周详 as 县长
  - Government leadership page: confirms 周详 as 县委副书记、县长 (as of 2026-07-14)
  - Also confirmed: 马东 (县委常委、常务副县长), 牛英瑛 (县委常委、副县长),
    辛毅伟 (副县长、县公安局局长), 刘会 (副县长), 李磊 (副县长),
    张灵伟 (副县长), 姚开胜 (副县长, 民进会员)

Confidence notes:
  - 钱程 (县委书记): confirmed via official news from 2026-07-22/24
  - 周详 (县长): confirmed via official leadership page and news articles
  - Full career timelines and biographical details for both leaders are mostly unavailable
    from current sources (leadership pages show only basic info).
  - This is a partial-evidence artifact: core leader identities are confirmed through
    official sources but detailed biographies are gaps.
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
SLUG = "渑池县"
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
        "name": "钱程",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共渑池县委员会",
        "source": "2026年7月22日县委理论学习中心组学习会议新闻报道确认钱程为渑池县委书记（来源：渑池县人民政府网站2026-07-24发布）"
    },
    {
        "id": 2,
        "name": "周详",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县长",
        "current_org": "渑池县人民政府",
        "source": "渑池县人民政府领导之窗页面确认周详为渑池县委副书记、县政府县长（来源：www.mianchi.gov.cn 2026-07-14更新）"
    },
    # ═══════ Key Deputies ═══════
    {
        "id": 3,
        "name": "马东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "常务副县长",
        "current_org": "渑池县人民政府",
        "source": "渑池县人民政府领导之窗确认马东为县委常委、县政府副县长，负责常务工作"
    },
    {
        "id": 4,
        "name": "牛英瑛",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "渑池县人民政府",
        "source": "渑池县人民政府领导之窗确认牛英瑛为县委常委、副县长"
    },
    {
        "id": 5,
        "name": "辛毅伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "渑池县人民政府",
        "source": "渑池县人民政府领导之窗确认辛毅伟为副县长、县公安局局长"
    },
    {
        "id": 6,
        "name": "刘会",
        "gender": "男",
        "ethnicity": "汉",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "渑池县人民政府",
        "source": "渑池县人民政府领导之窗确认刘会为副县长"
    },
    {
        "id": 7,
        "name": "李磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "渑池县人民政府",
        "source": "渑池县人民政府领导之窗确认李磊为副县长"
    },
    {
        "id": 8,
        "name": "张灵伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "渑池县人民政府",
        "source": "渑池县人民政府领导之窗确认张灵伟为副县长"
    },
    {
        "id": 9,
        "name": "姚开胜",
        "gender": "男",
        "ethnicity": "汉",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "渑池县人民政府",
        "source": "渑池县人民政府领导之窗确认姚开胜为副县长（中国民主促进会会员）"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共渑池县委员会", "type": "党委", "level": "县处级", "parent": "中共三门峡市委", "location": "渑池县"},
    {"id": 2, "name": "渑池县人民政府", "type": "政府", "level": "县处级", "parent": "三门峡市人民政府", "location": "渑池县"},
    {"id": 3, "name": "渑池县人大常委会", "type": "人大", "level": "县处级", "parent": "三门峡市人大常委会", "location": "渑池县"},
    {"id": 4, "name": "渑池县政协", "type": "政协", "level": "县处级", "parent": "三门峡市政协", "location": "渑池县"},
    {"id": 5, "name": "渑池县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "三门峡市纪委监委", "location": "渑池县"},
    {"id": 6, "name": "渑池县公安局", "type": "政府", "level": "县处级", "parent": "渑池县人民政府", "location": "渑池县"},
]

# ── Positions (person → org with title) ────────────────────────────────────
positions = [
    # 钱程
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "2026年7月仍在任，具体到任时间待查"},
    # 周详
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 马东
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责县政府常务工作"},
    # 牛英瑛
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责人力资源和社会保障、教育体育、民政、卫生健康等"},
    # 辛毅伟
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "兼任县公安局局长"},
    {"person_id": 5, "org_id": 6, "title": "局长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "县公安局局长"},
    # 刘会
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责商务、生态环境、文化旅游等"},
    # 李磊
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责农业农村、乡村振兴、水利等"},
    # 张灵伟
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责自然资源、住建、城管、交通等"},
    # 姚开胜
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责科技工作，中国民主促进会会员"},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 钱程 ↔ 周详（党政搭档）
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "钱程任县委书记，周详任县长，为渑池县党政正职搭档",
        "overlap_org": "渑池县",
        "overlap_period": "当前"
    },
    # 周详 ↔ 马东（上下级）
    {
        "person_a": 2, "person_b": 3,
        "type": "superior_subordinate",
        "context": "周详任县长，马东任常务副县长协助县长工作",
        "overlap_org": "渑池县人民政府",
        "overlap_period": "当前"
    },
    # 钱程 ↔ 马东（县委常委同僚）
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "钱程任县委书记，马东任县委常委、常务副县长，为县委常委会成员",
        "overlap_org": "中共渑池县委员会",
        "overlap_period": "当前"
    },
    # 钱程 ↔ 牛英瑛（县委常委同僚）
    {
        "person_a": 1, "person_b": 4,
        "type": "overlap",
        "context": "钱程任县委书记，牛英瑛任县委常委、副县长，为县委常委会成员",
        "overlap_org": "中共渑池县委员会",
        "overlap_period": "当前"
    },
]

# ── Person JSON Data ───────────────────────────────────────────────────────
person_files_data = [
    {
        "id": 1,
        "name": "钱程",
        "job": "县委书记",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "三门峡市",
                "region": "渑池县",
                "job": "县委书记",
                "task_id": "henan_渑池县",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "henan_mianchi_qiancheng",
                "name": "钱程",
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
                    "name_birth": "",
                    "name_birthplace": "",
                    "official_profile_url": "http://www.mianchi.gov.cn/（渑池县政府网站）"
                }
            },
            "current_status": {
                "current_post": "县委书记",
                "current_org": "中共渑池县委员会",
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "present",
                    "org": "中共渑池县委员会",
                    "title": "县委书记",
                    "level": "县处级正职",
                    "location": "渑池县",
                    "system": "party",
                    "rank": "县处级正职",
                    "is_key_promotion": True,
                    "notes": "2026年7月22日主持县委理论学习中心组学习会议，确认仍在任",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                },
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "履历缺口",
                    "title": "",
                    "notes": "公开资料未找到钱程来渑池县任职前的工作经历、出生信息、教育背景、来渑池任职的时间等",
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "organizations": [
                {
                    "name": "中共渑池县委员会",
                    "role": "县委书记",
                    "period": "至今",
                    "source_ids": ["S001"]
                }
            ],
            "relationships": [
                {
                    "person": "周详",
                    "person_id": "henan_mianchi_zhouxiang",
                    "relationship_type": "superior_subordinate",
                    "strength": "strong",
                    "evidence": "钱程任县委书记，周详任县长，为渑池县党政正职搭档",
                    "overlap_org": "渑池县",
                    "overlap_period": "当前",
                    "direction": "person_to_other",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                },
                {
                    "person": "马东",
                    "person_id": "henan_mianchi_madong",
                    "relationship_type": "overlap",
                    "strength": "medium",
                    "evidence": "同为县委常委班子成员",
                    "overlap_org": "中共渑池县委员会",
                    "overlap_period": "当前",
                    "direction": "person_to_other",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                },
                {
                    "person": "牛英瑛",
                    "person_id": "henan_mianchi_niuyingying",
                    "relationship_type": "overlap",
                    "strength": "medium",
                    "evidence": "同为县委常委班子成员",
                    "overlap_org": "中共渑池县委员会",
                    "overlap_period": "当前",
                    "direction": "person_to_other",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                }
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["party"],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "现任渑池县委书记（正处级），具体任职时间和晋升速度待查",
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
                    "confidence": "unverified"
                }
            ],
            "source_register": [
                {
                    "id": "S001",
                    "title": "渑池县人民政府网站 - 县委理论学习中心组学习会议召开",
                    "url": "http://www.mianchi.gov.cn/23319/2026/7/2291428.html",
                    "publisher": "渑池县人民政府",
                    "published_at": "2026-07-24",
                    "accessed_at": AS_OF,
                    "source_type": "official",
                    "reliability": "high",
                    "notes": "新闻报道确认县委书记钱程主持会议，为当前县领导身份的最权威来源"
                },
                {
                    "id": "S002",
                    "title": "渑池县人民政府网站 - 政府领导栏目",
                    "url": "http://www.mianchi.gov.cn/23340/0000/zhengfuxinxi-1.html",
                    "publisher": "渑池县人民政府",
                    "published_at": "2026-07-14",
                    "accessed_at": AS_OF,
                    "source_type": "official",
                    "reliability": "high",
                    "notes": "政府领导列表确认周详为县委副书记、县长，及各位副县长信息"
                }
            ],
            "confidence_summary": {
                "identity": "plausible",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "钱程的完整履历（出生年份、籍贯、教育背景、来渑池前的任职经历、任县委书记的具体时间）全部缺失"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "钱程的完整履历是什么？出生年份、籍贯、教育背景、全部工作经历？",
                    "why_it_matters": "作为当前一把手，其职业背景对理解政治网络至关重要",
                    "suggested_queries": ["钱程 简历 渑池", "钱程 任前公示 三门峡", "钱程 出生年月"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "critical",
                    "question": "钱程何时调任渑池县委书记？前任县委书记是谁？调任何处？",
                    "why_it_matters": "了解县委交接历史和县委书记的来源/去向网络",
                    "suggested_queries": ["渑池县 前任 县委书记", "渑池县 县委书记 任免 2024 2025"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": "钱程在来渑池县之前的任职经历是什么？来自哪个系统？",
                    "why_it_matters": "了解其成长路径和关系网络来源",
                    "suggested_queries": ["钱程 三门峡 任职", "钱程 工作经历"],
                    "last_attempted": AS_OF
                }
            ]
        }
    },
    {
        "id": 2,
        "name": "周详",
        "job": "县长",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "三门峡市",
                "region": "渑池县",
                "job": "县长",
                "task_id": "henan_渑池县",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "henan_mianchi_zhouxiang",
                "name": "周详",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "",
                    "name_birthplace": "",
                    "official_profile_url": "http://www.mianchi.gov.cn/23340/616861152/1821244.html"
                }
            },
            "current_status": {
                "current_post": "县长",
                "current_org": "渑池县人民政府",
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "present",
                    "org": "中共渑池县委员会",
                    "title": "县委副书记",
                    "level": "县处级副职",
                    "location": "渑池县",
                    "system": "party",
                    "rank": "县处级副职",
                    "is_key_promotion": False,
                    "notes": "周详在渑池县任县委副书记、县政府县长",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S002"]
                },
                {
                    "start": "unknown",
                    "end": "present",
                    "org": "渑池县人民政府",
                    "title": "县长",
                    "level": "县处级正职",
                    "location": "渑池县",
                    "system": "government",
                    "rank": "县处级正职",
                    "is_key_promotion": True,
                    "notes": "主持县人民政府全面工作，负责审计方面工作。分管县审计局。",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S002"]
                },
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "履历缺口",
                    "title": "",
                    "notes": "公开资料未找到周详来渑池县之前的任职经历、出生信息、教育背景等",
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "organizations": [
                {
                    "name": "渑池县人民政府",
                    "role": "县长",
                    "period": "至今",
                    "source_ids": ["S001", "S002"]
                },
                {
                    "name": "中共渑池县委员会",
                    "role": "县委副书记",
                    "period": "至今",
                    "source_ids": ["S001", "S002"]
                }
            ],
            "relationships": [
                {
                    "person": "钱程",
                    "person_id": "henan_mianchi_qiancheng",
                    "relationship_type": "superior_subordinate",
                    "strength": "strong",
                    "evidence": "周详任县长，钱程任县委书记，为渑池县党政正职搭档",
                    "overlap_org": "渑池县",
                    "overlap_period": "当前",
                    "direction": "other_to_person",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                },
                {
                    "person": "马东",
                    "person_id": "henan_mianchi_madong",
                    "relationship_type": "superior_subordinate",
                    "strength": "strong",
                    "evidence": "周详任县长，马东任常务副县长协助县长分管审计及常务工作",
                    "overlap_org": "渑池县人民政府",
                    "overlap_period": "当前",
                    "direction": "person_to_other",
                    "confidence": "confirmed",
                    "source_ids": ["S002"]
                },
                {
                    "person": "牛英瑛",
                    "person_id": "henan_mianchi_niuyingying",
                    "relationship_type": "overlap",
                    "strength": "medium",
                    "evidence": "同为县政府班子成员",
                    "overlap_org": "渑池县人民政府",
                    "overlap_period": "当前",
                    "direction": "person_to_other",
                    "confidence": "confirmed",
                    "source_ids": ["S002"]
                },
                {
                    "person": "张灵伟",
                    "person_id": "henan_mianchi_zhanglingwei",
                    "relationship_type": "overlap",
                    "strength": "medium",
                    "evidence": "共同调研（2026年7月23日巡河调研中张灵伟参加）",
                    "overlap_org": "渑池县人民政府",
                    "overlap_period": "当前",
                    "direction": "person_to_other",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                }
            ],
            "governance_record": [
                {
                    "period": "2026-07",
                    "domain": "rural_revitalization",
                    "achievement_or_event": "调研坡头乡韩家坑村和汪坟村基层党建、村集体产业发展、和美乡村建设",
                    "role_in_event": "带队调研并作工作部署",
                    "measurable_outcome": "",
                    "location": "渑池县坡头乡",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                },
                {
                    "period": "2026-07",
                    "domain": "public_security",
                    "achievement_or_event": "开展河长制黄河巡河，检查防汛备汛、地质灾害隐患排查工作",
                    "role_in_event": "带队检查",
                    "measurable_outcome": "",
                    "location": "渑池县",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                },
                {
                    "period": "2026-07",
                    "domain": "economic_development",
                    "achievement_or_event": "调研重点项目建设工作",
                    "role_in_event": "带队调研",
                    "measurable_outcome": "",
                    "location": "渑池县",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                }
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["government", "party"],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "现任渑池县县长（正处级），具体任职时间和晋升速度待查",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "grassroots_oriented",
                        "evidence": "多次深入乡镇（坡头乡韩家坑村、汪坟村、陈村乡白浪村）和基层一线（243省道红土坡段地质灾害点）调研检查",
                        "confidence": "plausible",
                        "source_ids": ["S001"]
                    },
                    {
                        "trait": "pragmatic",
                        "evidence": "在地质灾害隐患排查、防汛备汛、项目建设等具体事务上有明确的部署和要求",
                        "confidence": "plausible",
                        "source_ids": ["S001"]
                    }
                ],
                "speech_themes": [
                    "党建引领乡村振兴",
                    "人民至上、生命至上",
                    "黄河流域生态保护和高质量发展"
                ],
                "management_signals": [
                    "强调软弱涣散整顿后半篇文章",
                    "要求常态化开展隐患点巡查监测"
                ],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "未发现负面信息",
                    "date": AS_OF,
                    "confidence": "unverified"
                }
            ],
            "source_register": [
                {
                    "id": "S001",
                    "title": "渑池县人民政府 - 周详开展河长制黄河巡河并调研等工作",
                    "url": "http://www.mianchi.gov.cn/23319/2026/7/2291434.html",
                    "publisher": "渑池县人民政府",
                    "published_at": "2026-07-24",
                    "accessed_at": AS_OF,
                    "source_type": "official",
                    "reliability": "high",
                    "notes": "新闻报道确认周详为县委副书记、县长，并记录其工作活动"
                },
                {
                    "id": "S002",
                    "title": "渑池县人民政府政府领导栏目 - 周详页面",
                    "url": "http://www.mianchi.gov.cn/23340/616861152/1821244.html",
                    "publisher": "渑池县人民政府",
                    "published_at": "2026-07-14",
                    "accessed_at": AS_OF,
                    "source_type": "official",
                    "reliability": "high",
                    "notes": "领导之窗页面确认周详性别、民族、职务、分工和个人简历"
                }
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "medium",
                "biggest_gap": "周详的完整履历（出生年份、籍贯、教育背景、来渑池前的任职经历、任县长的具体时间）全部缺失"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "周详的完整履历是什么？出生年份、籍贯、教育背景、全部工作经历？",
                    "why_it_matters": "作为当前县长，其职业背景对理解政府运行和政治网络至关重要",
                    "suggested_queries": ["周详 简历 渑池", "周详 任前公示 三门峡", "周详 出生年月"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "critical",
                    "question": "周详何时调任渑池县县长？前任县长是谁？调任何处？",
                    "why_it_matters": "了解县长交接历史和周详的来源/前任去向",
                    "suggested_queries": ["渑池县 县长 任免 2024 2025", "渑池县 前任 县长"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": "周详来渑池县之前的任职经历是什么？从哪个岗位调来？",
                    "why_it_matters": "了解其职业背景和关系网络来源",
                    "suggested_queries": ["周详 三门峡 任职", "周详 工作经历"],
                    "last_attempted": AS_OF
                }
            ]
        }
    }
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
    for pf in person_files_data:
        fname = f"{TODAY}-河南省-三门峡市-{pf['job']}-{pf['name']}.json"
        path = PERSONS_DIR / fname
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pf["data"], f, ensure_ascii=False, indent=2)
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
        src = PERSONS_DIR / f"{TODAY}-河南省-三门峡市-{pf['job']}-{pf['name']}.json"
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
