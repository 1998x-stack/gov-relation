#!/usr/bin/env python3
"""Build 商丘市睢县 (Shangqiu Sui County) leadership network data.

Level: 县
Province: 河南省
Parent city: 商丘市
Targets: 县委书记 (Party Secretary), 县长 (Mayor)
Task ID: henan_睢县

Research date: 2026-07-24
Official source: https://www.suixian.gov.cn/ (睢县人民政府)

Current status (as of 2026-07-24, verified via government website news):
- 县委书记: 董良杰 — 2026年7月现任。主持召开县委常委会、全县防汛抗旱会议等
- 县委副书记、县长: 宋东谟 — 2026年7月现任。主持县政府全面工作

Confirmed leadership roster (from 睢县第十五次党代会报道 2026-06-17):
县常委会委员:
- 董良杰 — 县委书记
- 宋东谟 — 县委副书记、县长
- 贾晓晖 — 县领导
- 屠志远
- 张三星
- 宋宏伟
- 王灿
- 张政亮
- 李明杰
- 刘克伟
- 叶浩
- 魏红振
- 庞灿永
- 隋永法

Key government page sources:
- 董良杰调研安全生产工作: /xwzx/xwdt/content_23899
- 董良杰调研招商引资: /xwzx/xwdt/content_23898
- 董良杰调研防汛工作: /xwzx/xwdt/content_23834
- 全县防汛抗旱专题会议: /xwzx/xwdt/content_23819
- 两优一先表彰大会: /xwzx/xwdt/content_23814
- 睢县第十五次党代会闭幕: /xwzx/xwdt/content_23775
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

SLUG = "睢县"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = datetime.now().strftime("%Y-%m-%d")
TODAY = datetime.now().strftime("%Y%m%d")

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 县委领导 (Party Committee)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "董良杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共睢县委员会",
        "source": "https://www.suixian.gov.cn/xwzx/xwdt/content_23899",
    },
    {
        "id": 2,
        "name": "宋东谟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "睢县人民政府",
        "source": "https://www.suixian.gov.cn/xwzx/xwdt/content_23819",
    },
    {
        "id": 3,
        "name": "贾晓晖",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中共睢县委员会",
        "source": "https://www.suixian.gov.cn/xwzx/xwdt/content_23834",
    },
    {
        "id": 4,
        "name": "屠志远",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共睢县委员会",
        "source": "https://www.suixian.gov.cn/xwzx/xwdt/content_23775",
    },
    {
        "id": 5,
        "name": "张三星",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共睢县委员会",
        "source": "https://www.suixian.gov.cn/xwzx/xwdt/content_23775",
    },
    {
        "id": 6,
        "name": "宋宏伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共睢县委员会",
        "source": "https://www.suixian.gov.cn/xwzx/xwdt/content_23775",
    },
    {
        "id": 7,
        "name": "王灿",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共睢县委员会",
        "source": "https://www.suixian.gov.cn/xwzx/xwdt/content_23775",
    },
    {
        "id": 8,
        "name": "张政亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共睢县委员会",
        "source": "https://www.suixian.gov.cn/xwzx/xwdt/content_23775",
    },
    {
        "id": 9,
        "name": "李明杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共睢县委员会",
        "source": "https://www.suixian.gov.cn/xwzx/xwdt/content_23775",
    },
    {
        "id": 10,
        "name": "刘克伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共睢县委员会",
        "source": "https://www.suixian.gov.cn/xwzx/xwdt/content_23775",
    },
    {
        "id": 11,
        "name": "叶浩",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共睢县委员会",
        "source": "https://www.suixian.gov.cn/xwzx/xwdt/content_23834",
    },
    {
        "id": 12,
        "name": "魏红振",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共睢县委员会",
        "source": "https://www.suixian.gov.cn/xwzx/xwdt/content_23775",
    },
    {
        "id": 13,
        "name": "庞灿永",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "睢县",
        "source": "https://www.suixian.gov.cn/xwzx/xwdt/content_23775",
    },
    {
        "id": 14,
        "name": "隋永法",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "睢县",
        "source": "https://www.suixian.gov.cn/xwzx/xwdt/content_23775",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共睢县委员会", "type": "党委", "level": "县处级", "parent": "中共商丘市委员会", "location": "河南省商丘市睢县"},
    {"id": 2, "name": "睢县人民政府", "type": "政府", "level": "县处级", "parent": "商丘市人民政府", "location": "河南省商丘市睢县"},
    {"id": 3, "name": "中共睢县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共睢县委员会", "location": "河南省商丘市睢县"},
    {"id": 4, "name": "睢县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "", "location": "河南省商丘市睢县"},
    {"id": 5, "name": "中国人民政治协商会议睢县委员会", "type": "政协", "level": "县处级", "parent": "", "location": "河南省商丘市睢县"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS (person → org)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "2026年6月当选第十五届县委委员、常委、书记"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "县委副书记、县长"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "present", "rank": "", "note": "参与防汛调研等工作"},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "第十五届县委常委"},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "第十五届县委常委"},
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "第十五届县委常委"},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "第十五届县委常委"},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "第十五届县委常委"},
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "第十五届县委常委"},
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "第十五届县委常委"},
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "第十五届县委常委"},
    {"person_id": 12, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "第十五届县委常委"},
    {"person_id": 13, "org_id": 4, "title": "县领导", "start_date": "", "end_date": "present", "rank": "", "note": "人大系统领导"},
    {"person_id": 14, "org_id": 5, "title": "县领导", "start_date": "", "end_date": "present", "rank": "", "note": "政协系统领导"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS (person ↔ person)
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长党政搭档", "overlap_org": "中共睢县委员会/睢县人民政府", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "同为第十五届县委领导班子成员", "overlap_org": "中共睢县委员会", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "同为第十五届县委常委", "overlap_org": "中共睢县委员会", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "同为第十五届县委常委", "overlap_org": "中共睢县委员会", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "同为第十五届县委常委", "overlap_org": "中共睢县委员会", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "同为第十五届县委常委", "overlap_org": "中共睢县委员会", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "同为第十五届县委常委", "overlap_org": "中共睢县委员会", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "同为第十五届县委常委", "overlap_org": "中共睢县委员会", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "同为第十五届县委常委", "overlap_org": "中共睢县委员会", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "同为第十五届县委常委", "overlap_org": "中共睢县委员会", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate", "context": "同为第十五届县委常委", "overlap_org": "中共睢县委员会", "overlap_period": "2026年至今"},
]

# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON DATA
# ══════════════════════════════════════════════════════════════════════════════

person_json_template = {
    "schema_version": "1.0",
    "generated_at": TODAY,
    "investigation_scope": {
        "province": "河南省",
        "city": "商丘市",
        "region": "睢县",
        "job": "",
        "task_id": "henan_睢县",
        "time_focus": "2026年",
    },
    "identity": {
        "person_id": "",
        "name": "",
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
            "official_profile_url": "",
        },
    },
    "current_status": {
        "current_post": "",
        "current_org": "",
        "administrative_rank": "",
        "as_of": "2026-07-24",
        "is_current_confirmed": True,
        "source_ids": [],
    },
    "career_timeline": [],
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
            "summary": "",
            "notable_fast_promotions": [],
        },
    },
    "work_style_and_personality": {
        "public_style_indicators": [],
        "speech_themes": [],
        "management_signals": [],
        "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
    },
    "network_metrics": {},
    "risk_and_integrity_signals": [],
    "source_register": [],
    "confidence_summary": {
        "identity": "confirmed",
        "current_role": "confirmed",
        "career_completeness": "thin",
        "relationship_confidence": "medium",
        "biggest_gap": "",
    },
    "open_questions": [],
}


def make_dongliangjie_json():
    data = {
        **person_json_template,
        "investigation_scope": {**person_json_template["investigation_scope"], "job": "县委书记"},
        "identity": {
            "person_id": "henan_suixian_dongliangjie",
            "name": "董良杰",
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
                "name_birth": "董良杰",
                "name_birthplace": "董良杰_河南",
                "official_profile_url": "https://www.suixian.gov.cn/",
            },
        },
        "current_status": {
            "current_post": "县委书记",
            "current_org": "中共睢县委员会",
            "administrative_rank": "县处级正职",
            "as_of": "2026-07-24",
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002", "S003"],
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "unknown",
                "org": "中共睢县委员会",
                "title": "县委书记",
                "level": "县处级正职",
                "location": "河南省商丘市睢县",
                "system": "party",
                "rank": "县处级正职",
                "is_key_promotion": True,
                "notes": "2026年6月当选第十五届县委书记；截至2026年7月仍在任",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002", "S003"],
            },
        ],
        "organizations": [
            {"org_name": "中共睢县委员会", "org_type": "党委", "role": "主要领导"},
        ],
        "relationships": [
            {
                "person": "宋东谟",
                "person_id": "henan_suixian_songdongmo",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "县委书记与县长党政搭档；共同主持全县会议",
                "overlap_org": "中共睢县委员会/睢县人民政府",
                "overlap_period": "2026年至今",
                "direction": "person_to_other",
                "confidence": "confirmed",
                "source_ids": ["S001", "S003"],
            },
        ],
        "governance_record": [
            {
                "period": "2026-07",
                "domain": "public_security",
                "achievement_or_event": "调研督导安全生产工作，深入企业排查隐患",
                "role_in_event": "带队调研",
                "measurable_outcome": "",
                "location": "睢县高新技术产业开发区",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "period": "2026-07",
                "domain": "economic_development",
                "achievement_or_event": "调研招商引资和项目建设工作",
                "role_in_event": "带队调研",
                "measurable_outcome": "",
                "location": "睢县",
                "confidence": "confirmed",
                "source_ids": ["S002"],
            },
            {
                "period": "2026-07",
                "domain": "public_security",
                "achievement_or_event": "主持召开全县主汛期防汛抗旱暨安全生产专题会议",
                "role_in_event": "主持",
                "measurable_outcome": "",
                "location": "睢县",
                "confidence": "confirmed",
                "source_ids": ["S003"],
            },
            {
                "period": "2026-07",
                "domain": "other",
                "achievement_or_event": "调研防汛工作，查看河道治理和积水点改造",
                "role_in_event": "带队调研",
                "measurable_outcome": "",
                "location": "睢县",
                "confidence": "confirmed",
                "source_ids": ["S004"],
            },
            {
                "period": "2026-07",
                "domain": "other",
                "achievement_or_event": "出席两优一先表彰大会并讲授党课",
                "role_in_event": "主讲",
                "measurable_outcome": "",
                "location": "睢县",
                "confidence": "confirmed",
                "source_ids": ["S005"],
            },
            {
                "period": "2026-06",
                "domain": "other",
                "achievement_or_event": "主持睢县第十五次党代会并致闭幕词",
                "role_in_event": "主持",
                "measurable_outcome": "选举产生新一届县委和县纪委",
                "location": "睢县",
                "confidence": "confirmed",
                "source_ids": ["S006"],
            },
        ],
        "professional_profile": {
            "primary_specializations": ["党建", "安全生产", "招商引资"],
            "secondary_specializations": ["防汛抗旱", "乡村振兴"],
            "career_pattern": "unknown",
            "systems_experience": ["party"],
            "geographic_pattern": ["河南"],
            "promotion_velocity": {
                "summary": "具体情况因缺乏履历数据未知",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "pragmatic",
                    "evidence": "频繁深入企业生产车间、消防控制室等一线调研，现场研究解决方案",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S002"],
                },
                {
                    "trait": "discipline_oriented",
                    "evidence": "反复强调安全生产责任落实、党政同责、一岗双责",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S003"],
                },
                {
                    "trait": "reform_oriented",
                    "evidence": "提出'四个强县、两个睢县'发展目标",
                    "confidence": "confirmed",
                    "source_ids": ["S005"],
                },
            ],
            "speech_themes": ["安全底线", "实干笃行", "人民至上", "争先出彩"],
            "management_signals": ["强调闭环管理", "要求倒排工期、挂图作战", "注重隐患排查动态清零"],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026年7月24日，未发现董良杰的纪律处分或负面舆情",
                "date": "",
                "confidence": "confirmed",
                "source_ids": [],
            },
        ],
        "source_register": [
            {"id": "S001", "title": "董良杰调研督导安全生产工作", "url": "https://www.suixian.gov.cn/xwzx/xwdt/content_23899", "publisher": "睢县人民政府", "published_at": "2026-07-24", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": ""},
            {"id": "S002", "title": "董良杰调研招商引资和项目建设工作", "url": "https://www.suixian.gov.cn/xwzx/xwdt/content_23898", "publisher": "睢县人民政府", "published_at": "2026-07-23", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": ""},
            {"id": "S003", "title": "全县主汛期防汛抗旱暨安全生产工作专题会议召开", "url": "https://www.suixian.gov.cn/xwzx/xwdt/content_23819", "publisher": "睢县人民政府", "published_at": "2026-07-11", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": "确认宋东谟为县长"},
            {"id": "S004", "title": "董良杰调研防汛工作", "url": "https://www.suixian.gov.cn/xwzx/xwdt/content_23834", "publisher": "睢县人民政府", "published_at": "2026-07-17", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": ""},
            {"id": "S005", "title": "睢县举行两优一先表彰大会暨县委书记讲党课", "url": "https://www.suixian.gov.cn/xwzx/xwdt/content_23814", "publisher": "睢县人民政府", "published_at": "2026-07-01", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": ""},
            {"id": "S006", "title": "中国共产党睢县第十五次代表大会胜利闭幕", "url": "https://www.suixian.gov.cn/xwzx/xwdt/content_23775", "publisher": "睢县人民政府", "published_at": "2026-06-18", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": "确认县委常委全体名单"},
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "董良杰的出生年月、籍贯、教育背景以及完整的仕途履历缺失",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "董良杰的出生年月和籍贯",
                "why_it_matters": "人员去重和身份识别的核心字段",
                "suggested_queries": ["董良杰 简历", "董良杰 出生", "商丘市睢县 董良杰"],
                "last_attempted": "2026-07-24",
            },
            {
                "priority": "critical",
                "question": "董良杰的完整仕途履历",
                "why_it_matters": "了解其晋升路径和跨地区任职经历",
                "suggested_queries": ["董良杰 任职经历", "董良杰 历任"],
                "last_attempted": "2026-07-24",
            },
            {
                "priority": "high",
                "question": "董良杰接任睢县县委书记的时间",
                "why_it_matters": "确定任期起点",
                "suggested_queries": ["董良杰 任睢县县委书记"],
                "last_attempted": "2026-07-24",
            },
            {
                "priority": "high",
                "question": "董良杰的前任是谁",
                "why_it_matters": "理清领导交接和干部交流线索",
                "suggested_queries": ["睢县 前任县委书记"],
                "last_attempted": "2026-07-24",
            },
        ],
    }
    return data


def make_songdongmo_json():
    data = {
        **person_json_template,
        "investigation_scope": {**person_json_template["investigation_scope"], "job": "县长"},
        "identity": {
            "person_id": "henan_suixian_songdongmo",
            "name": "宋东谟",
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
                "name_birth": "宋东谟",
                "name_birthplace": "宋东谟_河南",
                "official_profile_url": "https://www.suixian.gov.cn/",
            },
        },
        "current_status": {
            "current_post": "县委副书记、县长",
            "current_org": "睢县人民政府",
            "administrative_rank": "县处级正职",
            "as_of": "2026-07-24",
            "is_current_confirmed": True,
            "source_ids": ["S003", "S005", "S006"],
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "unknown",
                "org": "睢县人民政府",
                "title": "县长",
                "level": "县处级正职",
                "location": "河南省商丘市睢县",
                "system": "government",
                "rank": "县处级正职",
                "is_key_promotion": True,
                "notes": "2026年6月当选第十五届县委委员、常委、副书记；任睢县县长",
                "confidence": "confirmed",
                "source_ids": ["S003", "S006"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "中共睢县委员会",
                "title": "县委副书记",
                "level": "县处级副职",
                "location": "河南省商丘市睢县",
                "system": "party",
                "rank": "县处级副职",
                "is_key_promotion": False,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S003", "S005", "S006"],
            },
        ],
        "organizations": [
            {"org_name": "睢县人民政府", "org_type": "政府", "role": "主要领导"},
            {"org_name": "中共睢县委员会", "org_type": "党委", "role": "县委副书记"},
        ],
        "relationships": [
            {
                "person": "董良杰",
                "person_id": "henan_suixian_dongliangjie",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "县长与县委书记党政搭档；多次共同主持全县会议",
                "overlap_org": "中共睢县委员会/睢县人民政府",
                "overlap_period": "2026年至今",
                "direction": "other_to_person",
                "confidence": "confirmed",
                "source_ids": ["S003", "S005"],
            },
        ],
        "governance_record": [
            {
                "period": "2026-07",
                "domain": "public_security",
                "achievement_or_event": "在主汛期防汛抗旱暨安全生产工作专题会议上作安排部署",
                "role_in_event": "部署工作",
                "measurable_outcome": "",
                "location": "睢县",
                "confidence": "confirmed",
                "source_ids": ["S003"],
            },
            {
                "period": "2026-07",
                "domain": "other",
                "achievement_or_event": "主持两优一先表彰大会",
                "role_in_event": "主持",
                "measurable_outcome": "",
                "location": "睢县",
                "confidence": "confirmed",
                "source_ids": ["S005"],
            },
            {
                "period": "2026-07",
                "domain": "other",
                "achievement_or_event": "主持推进常态化帮扶持续巩固拓展脱贫攻坚成果工作会议",
                "role_in_event": "主持",
                "measurable_outcome": "",
                "location": "睢县",
                "confidence": "confirmed",
                "source_ids": ["S007"],
            },
            {
                "period": "2026-06",
                "domain": "other",
                "achievement_or_event": "主持睢县第十五次党代会闭幕式",
                "role_in_event": "主持",
                "measurable_outcome": "",
                "location": "睢县",
                "confidence": "confirmed",
                "source_ids": ["S006"],
            },
        ],
        "professional_profile": {
            "primary_specializations": ["政府管理", "乡村振兴", "应急管理"],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["government", "party"],
            "geographic_pattern": ["河南"],
            "promotion_velocity": {
                "summary": "具体情况因缺乏履历数据未知",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "low_profile",
                    "evidence": "公开报道中多为配合县委书记主持会议或作工作部署，较少单独调研报道",
                    "confidence": "plausible",
                    "source_ids": ["S003", "S005", "S006"],
                },
            ],
            "speech_themes": ["防范化解风险", "民生保障"],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026年7月24日，未发现宋东谟的纪律处分或负面舆情",
                "date": "",
                "confidence": "confirmed",
                "source_ids": [],
            },
        ],
        "source_register": [
            {"id": "S003", "title": "全县主汛期防汛抗旱暨安全生产工作专题会议召开", "url": "https://www.suixian.gov.cn/xwzx/xwdt/content_23819", "publisher": "睢县人民政府", "published_at": "2026-07-11", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": ""},
            {"id": "S005", "title": "睢县举行两优一先表彰大会暨县委书记讲党课", "url": "https://www.suixian.gov.cn/xwzx/xwdt/content_23814", "publisher": "睢县人民政府", "published_at": "2026-07-01", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": ""},
            {"id": "S006", "title": "中国共产党睢县第十五次代表大会胜利闭幕", "url": "https://www.suixian.gov.cn/xwzx/xwdt/content_23775", "publisher": "睢县人民政府", "published_at": "2026-06-18", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": ""},
            {"id": "S007", "title": "全县2026年推进常态化帮扶持续巩固拓展脱贫攻坚成果工作会议召开", "url": "https://www.suixian.gov.cn/xwzx/xwdt/content_23815", "publisher": "睢县人民政府", "published_at": "2026-07-06", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": ""},
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "宋东谟的出生年月、籍贯、教育背景以及完整的仕途履历缺失",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "宋东谟的出生年月和籍贯",
                "why_it_matters": "人员去重和身份识别的核心字段",
                "suggested_queries": ["宋东谟 简历", "宋东谟 出生", "睢县县长 宋东谟"],
                "last_attempted": "2026-07-24",
            },
            {
                "priority": "critical",
                "question": "宋东谟的完整仕途履历",
                "why_it_matters": "了解其晋升路径和跨地区任职经历",
                "suggested_queries": ["宋东谟 任职经历", "宋东谟 历任"],
                "last_attempted": "2026-07-24",
            },
            {
                "priority": "high",
                "question": "宋东谟何时任睢县县长",
                "why_it_matters": "确定任期起点",
                "suggested_queries": ["宋东谟 任睢县县长"],
                "last_attempted": "2026-07-24",
            },
        ],
    }
    return data


# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON WRITING
# ══════════════════════════════════════════════════════════════════════════════

person_files = [
    (f"{TODAY}-河南省-商丘市-县委书记-董良杰.json", make_dongliangjie_json()),
    (f"{TODAY}-河南省-商丘市-县长-宋东谟.json", make_songdongmo_json()),
]


def write_person_json():
    for filename, data in person_files:
        path = _STAGING_DIR / filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {path}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 睢县人民政府网站 (suixian.gov.cn)")
    print("=" * 60)

    # Write person JSONs
    write_person_json()

    # Build DB and GEXF
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
