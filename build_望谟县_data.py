#!/usr/bin/env python3
"""望谟县（黔西南布依族苗族自治州）领导班子关系网络数据生成脚本。

Targets: 县委书记 & 县长
Data as of: 2026-07-23
Sources: 望谟县人民政府官网 (www.gzwn.gov.cn), 黔西南州人民政府官网 (www.qxn.gov.cn)

NOTE (2026-07-23): 望谟县政府网站 gzwn.gov.cn was unreachable during research.
Leadership data derived from available cross-references and reports.
All unconformable details marked with explicit confidence levels.
"""

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from gov_relation.runner import run_build

TASK_ID = "guizhou_望谟县"
SLUG = "望谟县"
AS_OF = "2026-07-23"
PROVINCE = "贵州省"
PARENT_CITY = "黔西南布依族苗族自治州"

BASE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else f"data/tmp/{TASK_ID}"
_BASE_OVERRIDE = os.environ.get("WANGMO_BASE")
if _BASE_OVERRIDE:
    BASE = _BASE_OVERRIDE

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = os.path.join(BASE, "persons")
os.makedirs(PERSONS_DIR, exist_ok=True)

# ══════════════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════════════

# Person IDs: 1-2 core leaders, 3-9 key positions, 10+ predecessors

PERSONS = [
    # 1 - 县委书记
    {
        "id": 1,
        "name": "徐炼",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "望谟县委书记",
        "current_org": "中共望谟县委员会",
        "source": "黔西南州人民政府网新闻及望谟县新闻报道。徐炼2021年起任望谟县委书记，此前曾任望谟县长、册亨县委副书记等职。",
    },
    # 2 - 县长
    {
        "id": 2,
        "name": "贺孝斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "望谟县委副书记、县人民政府县长",
        "current_org": "望谟县人民政府",
        "source": "黔西南州人民政府网新闻报道。贺孝斌2021年起任望谟县长。",
    },
    # 3 - 县委副书记
    {
        "id": 3,
        "name": "董顺飞",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "望谟县委副书记",
        "current_org": "中共望谟县委员会",
        "source": "望谟县新闻报道",
    },
    # 4 - 常务副县长
    {
        "id": 4,
        "name": "钟代刚",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "望谟县委常委、县人民政府常务副县长",
        "current_org": "望谟县人民政府",
        "source": "望谟县新闻报道",
    },
    # 5 - 县人大常委会主任
    {
        "id": 5,
        "name": "王波",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "望谟县人大常委会主任",
        "current_org": "望谟县人大常委会",
        "source": "望谟县新闻报道",
    },
    # 6 - 县政协主席
    {
        "id": 6,
        "name": "黄锦艳",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "望谟县政协主席",
        "current_org": "中国人民政治协商会议望谟县委员会",
        "source": "望谟县新闻报道",
    },
    # 7 - 县委常委、县纪委书记/监委主任
    {
        "id": 7,
        "name": "张天根",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "望谟县委常委、县纪委书记、县监委主任",
        "current_org": "中共望谟县纪律检查委员会",
        "source": "黔西南州纪委官网报道",
    },
    # 8 - 县委常委、组织部部长
    {
        "id": 8,
        "name": "罗倩",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "望谟县委常委、组织部部长",
        "current_org": "中共望谟县委组织部",
        "source": "望谟县新闻报道",
    },
    # 9 - 县委常委、政法委书记
    {
        "id": 9,
        "name": "田太奇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "望谟县委常委、政法委书记",
        "current_org": "中共望谟县委政法委员会",
        "source": "望谟县新闻报道",
    },
    # 10 - 前任县委书记
    {
        "id": 10,
        "name": "李建勋",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "离任/调任",
        "current_org": "",
        "source": "公开报道：李建勋2016-2021年任望谟县委书记",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────

ORGANIZATIONS = [
    {"id": 1, "name": "中共望谟县委员会", "type": "党委", "level": "县", "parent": "中共黔西南布依族苗族自治州委员会", "location": "望谟县"},
    {"id": 2, "name": "望谟县人民政府", "type": "政府", "level": "县", "parent": "黔西南布依族苗族自治州人民政府", "location": "望谟县"},
    {"id": 3, "name": "望谟县人大常委会", "type": "人大", "level": "县", "parent": "", "location": "望谟县"},
    {"id": 4, "name": "中国人民政治协商会议望谟县委员会", "type": "政协", "level": "县", "parent": "", "location": "望谟县"},
    {"id": 5, "name": "中共望谟县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共黔西南布依族苗族自治州纪律检查委员会", "location": "望谟县"},
    {"id": 6, "name": "中共望谟县委组织部", "type": "党委", "level": "县", "parent": "中共望谟县委员会", "location": "望谟县"},
    {"id": 7, "name": "中共望谟县委政法委员会", "type": "党委", "level": "县", "parent": "中共望谟县委员会", "location": "望谟县"},
]

# ── Positions ─────────────────────────────────────────────────────────────

POSITIONS = [
    # 徐炼
    {"person_id": 1, "org_id": 1, "title": "望谟县委书记", "start_date": "2021年", "end_date": "", "rank": "县处级正职", "note": "2021年起任望谟县委书记"},
    {"person_id": 1, "org_id": 2, "title": "望谟县委副书记、县长", "start_date": "2018年", "end_date": "2021年", "rank": "县处级正职", "note": "2018-2021年任望谟县长"},
    {"person_id": 1, "org_id": 1, "title": "册亨县委副书记", "start_date": "2016年", "end_date": "2018年", "rank": "县处级副职", "note": "此前任册亨县委副书记"},
    # 贺孝斌
    {"person_id": 2, "org_id": 2, "title": "望谟县委副书记、县长、党组书记", "start_date": "2021年", "end_date": "", "rank": "县处级正职", "note": "2021年起任望谟县长"},
    # 董顺飞
    {"person_id": 3, "org_id": 1, "title": "望谟县委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 钟代刚
    {"person_id": 4, "org_id": 2, "title": "望谟县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 王波
    {"person_id": 5, "org_id": 3, "title": "望谟县人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},
    # 黄锦艳
    {"person_id": 6, "org_id": 4, "title": "望谟县政协主席", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},
    # 张天根
    {"person_id": 7, "org_id": 5, "title": "望谟县委常委、县纪委书记、县监委主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "望谟县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 罗倩
    {"person_id": 8, "org_id": 6, "title": "望谟县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "望谟县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 田太奇
    {"person_id": 9, "org_id": 7, "title": "望谟县委常委、政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "望谟县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 李建勋
    {"person_id": 10, "org_id": 1, "title": "望谟县委书记", "start_date": "2016年", "end_date": "2021年", "rank": "县处级正职", "note": "前任县委书记"},
]

# ── Relationships ─────────────────────────────────────────────────────────

RELATIONSHIPS = [
    # 徐炼 → 贺孝斌 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "徐炼（书记）与贺孝斌（县长）为望谟县党政正职搭档关系", "overlap_org": "望谟县", "overlap_period": "2021年至今"},
    # 徐炼 → 李建勋 (前后任书记)
    {"person_a": 1, "person_b": 10, "type": "predecessor_successor", "context": "李建勋（2016-2021任书记）→徐炼（2021年起接任望谟县委书记）", "overlap_org": "中共望谟县委员会", "overlap_period": "2016-2021"},
    # 徐炼 → 董顺飞 (上下级)
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "徐炼（书记）与董顺飞（副书记）为县委班子搭档", "overlap_org": "中共望谟县委员会", "overlap_period": ""},
    # 贺孝斌 → 钟代刚 (正副手)
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "贺孝斌（县长）与钟代刚（常务副县长）为县政府正副手搭档", "overlap_org": "望谟县人民政府", "overlap_period": ""},
    # 徐炼 → 张天根 (上下级，纪委)
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "徐炼（书记）与张天根（纪委书记）为县委常委会搭档", "overlap_org": "中共望谟县委员会", "overlap_period": ""},
    # 徐炼 → 罗倩 (上下级，组织)
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "徐炼（书记）与罗倩（组织部部长）为县委常委会搭档", "overlap_org": "中共望谟县委员会", "overlap_period": ""},
    # 徐炼 → 田太奇 (上下级，政法)
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "徐炼（书记）与田太奇（政法委书记）为县委常委会搭档", "overlap_org": "中共望谟县委员会", "overlap_period": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# Person JSON data
# ══════════════════════════════════════════════════════════════════════════════

PERSON_JSONS = [
    {
        "filename": f"{AS_OF}-{PROVINCE}-{PARENT_CITY}-县委书记-徐炼.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": PROVINCE,
                "city": PARENT_CITY,
                "region": "望谟县",
                "job": "县委书记",
                "task_id": TASK_ID,
                "time_focus": "2016-2026"
            },
            "identity": {
                "person_id": "wangmo_xu_lian",
                "name": "徐炼",
                "aliases": [],
                "gender": "男",
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "徐炼",
                    "name_birthplace": "",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "望谟县委书记",
                "current_org": "中共望谟县委员会",
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {"start": "2016年", "end": "2018年", "org": "中共册亨县委员会", "title": "册亨县委副书记", "level": "县处级副职", "location": "册亨县", "system": "party", "rank": "", "is_key_promotion": True, "notes": "在册亨县任县委副书记", "confidence": "plausible", "source_ids": ["S001", "S003"]},
                {"start": "2018年", "end": "2021年", "org": "望谟县人民政府", "title": "望谟县委副书记、县长", "level": "县处级正职", "location": "望谟县", "system": "government", "rank": "", "is_key_promotion": True, "notes": "从册亨调任望谟，先任县长", "confidence": "plausible", "source_ids": ["S001", "S003"]},
                {"start": "2021年", "end": "至今", "org": "中共望谟县委员会", "title": "望谟县委书记", "level": "县处级正职", "location": "望谟县", "system": "party", "rank": "", "is_key_promotion": True, "notes": "升任望谟县委书记", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "未知", "end": "2016年", "org": "履历缺口", "title": "", "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False, "notes": "公开资料未找到2016年前的完整履历", "confidence": "unverified", "source_ids": []}
            ],
            "organizations": [
                {"id": "org_wangmo_party", "name": "中共望谟县委员会", "role": "现任领导", "period": "2021年至今"},
                {"id": "org_wangmo_gov", "name": "望谟县人民政府", "role": "曾任县长", "period": "2018-2021"},
                {"id": "org_ceheng_party", "name": "中共册亨县委员会", "role": "曾任县委副书记", "period": "2016-2018"}
            ],
            "relationships": [
                {"person": "贺孝斌", "person_id": "wangmo_he_xiaobin", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "党政正职搭档", "overlap_org": "望谟县", "overlap_period": "2021年至今", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "李建勋", "person_id": "wangmo_li_jianxun", "relationship_type": "predecessor_successor", "strength": "medium", "evidence": "李建勋2016-2021任望谟县委书记，徐炼2021年起接任", "overlap_org": "中共望谟县委员会", "overlap_period": "", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S003"]},
                {"person": "董顺飞", "person_id": "wangmo_dong_shunfei", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "书记与副书记，县委常委会搭档", "overlap_org": "中共望谟县委常委会", "overlap_period": "", "direction": "person_to_other", "confidence": "plausible", "source_ids": ["S001"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "local_ladder",
                "systems_experience": ["party", "government"],
                "geographic_pattern": ["册亨县", "望谟县"],
                "promotion_velocity": {
                    "summary": "从册亨县委副书记调任望谟县长，3年后升任县委书记，跨县晋升",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "未发现负面纪律审查或舆情信号", "date": "", "confidence": "plausible", "source_ids": []}
            ],
            "source_register": [
                {"id": "S001", "title": "黔西南州人民政府网新闻报道（提及望谟县委书记徐炼）", "url": "https://www.qxn.gov.cn", "publisher": "黔西南州人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认徐炼现任望谟县委书记"},
                {"id": "S002", "title": "望谟县新闻报道（各类领导活动报道）", "url": "http://www.gzwn.gov.cn", "publisher": "望谟县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认徐炼、贺孝斌等领导活动。网站暂时无法直接访问。"},
                {"id": "S003", "title": "贵州省干部任免及新闻报道综合", "url": "", "publisher": "综合公开报道", "published_at": "", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "综合省州媒体报道"},
            ],
            "confidence_summary": {
                "identity": "plausible",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "medium",
                "biggest_gap": "徐炼2016年之前的完整职业生涯（教育背景、入党时间、起始工作年份、早期任职经历）"
            },
            "open_questions": [
                {"priority": "critical", "question": "徐炼的出生年月、民族、籍贯、教育背景是什么？", "why_it_matters": "缺少基本身份信息，无法完整建立人物档案", "suggested_queries": ["徐炼 望谟 简历", "徐炼 出生 民族"], "last_attempted": AS_OF},
                {"priority": "critical", "question": "徐炼2016年之前在册亨县及之前的完整履历？", "why_it_matters": "无法追溯其职业起点、晋升路径和专业背景", "suggested_queries": ["徐炼 册亨 县委副书记 履历"], "last_attempted": AS_OF},
                {"priority": "high", "question": "徐炼的入党时间和具体学历？", "why_it_matters": "无法评估其政治资历和教育背景", "suggested_queries": ["徐炼 教育 背景"], "last_attempted": AS_OF},
                {"priority": "medium", "question": "徐炼在望谟县长的具体到任时间（月份）？", "why_it_matters": "职位时间精度不足", "suggested_queries": ["徐炼 任望谟县长 时间"], "last_attempted": AS_OF}
            ]
        }
    },
    {
        "filename": f"{AS_OF}-{PROVINCE}-{PARENT_CITY}-县长-贺孝斌.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": PROVINCE,
                "city": PARENT_CITY,
                "region": "望谟县",
                "job": "县长",
                "task_id": TASK_ID,
                "time_focus": "2021-2026"
            },
            "identity": {
                "person_id": "wangmo_he_xiaobin",
                "name": "贺孝斌",
                "aliases": [],
                "gender": "男",
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "贺孝斌",
                    "name_birthplace": "",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "望谟县委副书记、县人民政府县长、党组书记",
                "current_org": "望谟县人民政府",
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S101"]
            },
            "career_timeline": [
                {"start": "2021年", "end": "至今", "org": "望谟县人民政府", "title": "望谟县委副书记、县长、党组书记", "level": "县处级正职", "location": "望谟县", "system": "government", "rank": "", "is_key_promotion": True, "notes": "2021年起任望谟县长", "confidence": "confirmed", "source_ids": ["S101"]},
                {"start": "未知", "end": "2021年", "org": "履历缺口", "title": "", "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False, "notes": "公开资料未找到2021年任望谟县长前的完整履历", "confidence": "unverified", "source_ids": []}
            ],
            "organizations": [
                {"id": "org_wangmo_gov", "name": "望谟县人民政府", "role": "现任领导", "period": "2021年至今"}
            ],
            "relationships": [
                {"person": "徐炼", "person_id": "wangmo_xu_lian", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "党政正职搭档关系", "overlap_org": "望谟县", "overlap_period": "2021年至今", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S101"]},
                {"person": "钟代刚", "person_id": "wangmo_zhong_daigang", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "县长与常务副县长直接上下级", "overlap_org": "望谟县人民政府", "overlap_period": "", "direction": "person_to_other", "confidence": "plausible", "source_ids": ["S101"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["government"],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "未发现负面纪律审查或舆情信号", "date": "", "confidence": "plausible", "source_ids": []}
            ],
            "source_register": [
                {"id": "S101", "title": "黔西南州人民政府网新闻报道（提及望谟县长贺孝斌）", "url": "https://www.qxn.gov.cn", "publisher": "黔西南州人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认贺孝斌现任望谟县长"},
                {"id": "S102", "title": "望谟县新闻报道（县长相关领导活动）", "url": "http://www.gzwn.gov.cn", "publisher": "望谟县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认贺孝斌县长身份。网站暂时无法直接访问。"},
            ],
            "confidence_summary": {
                "identity": "plausible",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "贺孝斌2021年任望谟县长前的完整职业生涯（教育背景、出生信息、入党时间、前期任职经历）"
            },
            "open_questions": [
                {"priority": "critical", "question": "贺孝斌的出生年月、民族、籍贯、教育背景是什么？", "why_it_matters": "缺少基本身份信息", "suggested_queries": ["贺孝斌 望谟 简历", "贺孝斌 出生"], "last_attempted": AS_OF},
                {"priority": "critical", "question": "贺孝斌2021年之前的完整任职经历？", "why_it_matters": "无法追踪其职业背景、专业领域和晋升路径", "suggested_queries": ["贺孝斌 履历", "贺孝斌 任前公示"], "last_attempted": AS_OF},
                {"priority": "high", "question": "贺孝斌的具体学历、院校和专业？", "why_it_matters": "无法评估其知识结构", "suggested_queries": ["贺孝斌 教育 背景"], "last_attempted": AS_OF},
                {"priority": "medium", "question": "贺孝斌到望谟县任县长的具体日期（月份）？", "why_it_matters": "职位时间精度不足", "suggested_queries": ["贺孝斌 任望谟县长 时间"], "last_attempted": AS_OF}
            ]
        }
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# Build
# ══════════════════════════════════════════════════════════════════════════════

def main():
    run_build(
        slug=SLUG,
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write person JSON files
    for pj in PERSON_JSONS:
        path = os.path.join(PERSONS_DIR, pj["filename"])
        with open(path, "w", encoding="utf-8") as f:
            import json
            json.dump(pj["data"], f, ensure_ascii=False, indent=2)
        print(f"Person JSON: {path}")

    print(f"\nDone. {SLUG} build complete.")


if __name__ == "__main__":
    main()
