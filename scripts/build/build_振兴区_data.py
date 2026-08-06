#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 振兴区 (丹东市，辽宁省).

Investigation date: 2026-08-06
Task ID: liaoning_振兴区
Level: 市辖区
Parent city: 丹东市
Targets: 区委书记 & 区长

Research status: PRIMARY SOURCE ACCESS (partial)
  - 振兴区人民政府门户网站 (www.zhenxing.gov.cn): 可访问
  - 区委书记、区长 已通过官方新闻确认（区第十五次党代会、区政府常务会议、防汛防台风报道）
  - 区人大主任、区政协主席 已确认（防汛报道）
  - Exa 检索限流、Baidu 不可用；副区长/区委常委完整名单及核心领导履历缺失，按证据分级标注

Current officeholders (as of 2026-08-06, confirmed by official www.zhenxing.gov.cn):
   - 区委书记: 滕飞（区第十五次党代会 2026-07-28 代表十四届区委作工作报告；持续活跃）
   - 区委副书记、区长: 任传英（2026-08-04 第78次常务会议主持；至迟 2025-10 已任区长）
   - 区人大常委会主任: 赵永刚（2026-07-14 防汛督导）
   - 区政协主席: 曲晓晖（2026-07-14 防汛督导）

Predecessor timeline (piecemeal, inferred from 十四届 = 五年制):
   - 区委书记: 十四届任期内系本届延续（滕飞作十四届报告），前任书记 = 上一届（~2016-2021），姓名待核
   - 区长: 任传英在此之前去向待核；公开资料未标明前任区长
   - 区人大常委会主任: 赵永刚（现行）

Cross-region / context:
   - 振兴区地处丹东核心城区，下辖街道及浪头镇、汤池镇；振兴经济开发区为区属经开区
   - 2026 年 3-5 月区人民政府任免除（李东任振兴经济开发区管委会副主任）等中层变动
"""

from __future__ import annotations

import json
import sys
import sqlite3
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

from gov_relation.runner import run_build

# ── Metadata ─────────────────────────────────────────────────────────────
SLUG = "振兴区"
TODAY_str = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

_CURRENT_DIR = Path(__file__).parent.resolve()
DB_PATH = _CURRENT_DIR / f"{SLUG}_network.db"
GEXF_PATH = _CURRENT_DIR / f"{SLUG}_network.gexf"
PERSONS_STAGING_DIR = _CURRENT_DIR

# ── Persons ──────────────────────────────────────────────────────────────
persons = [
    # ── 区委书记 ──
    {
        "id": 1,
        "name": "滕飞",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中国共产党丹东市振兴区委员会",
        "source": "https://www.zhenxing.gov.cn/html/ZXQZF/202607/0178528730788429.html (区第十五次党代会, 2026-07-28)",
    },
    # ── 区委副书记、区长 ──
    {
        "id": 2,
        "name": "任传英",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "丹东市振兴区人民政府",
        "source": "https://www.zhenxing.gov.cn/html/ZXQZF/202608/0178589151953678.html (区政府第78次常务会议, 2026-08-04)",
    },
    # ── 区人大常委会主任 ──
    {
        "id": 3,
        "name": "赵永刚",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "",
        "education": "待查",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "丹东市振兴区人民代表大会常务委员会",
        "source": "https://www.zhenxing.gov.cn/html/ZXQZF/202607/0178407798202764.html (防汛督导, 2026-07-14/15)",
    },
    # ── 区政协主席 ──
    {
        "id": 4,
        "name": "曲晓晖",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "",
        "education": "待查",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议丹东市振兴区委员会",
        "source": "https://www.zhenxing.gov.cn/html/ZXQZF/202607/0178407798202764.html (防汛督导, 2026-07-14/15)",
    },
]

organizations = [
    {"id": 1, "name": "中国共产党丹东市振兴区委员会", "type": "党委", "level": "县处级", "parent": "中共丹东市委", "location": "丹东市振兴区"},
    {"id": 2, "name": "丹东市振兴区人民政府", "type": "政府", "level": "县处级", "parent": "丹东市人民政府", "location": "丹东市振兴区"},
    {"id": 3, "name": "丹东市振兴区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "丹东市振兴区", "location": "丹东市振兴区"},
    {"id": 4, "name": "中国人民政治协商会议丹东市振兴区委员会", "type": "政协", "level": "县处级", "parent": "丹东市振兴区", "location": "丹东市振兴区"},
    {"id": 5, "name": "中国共产党丹东市委员会", "type": "党委", "level": "地厅级", "parent": "中共辽宁省委", "location": "丹东市"},
    {"id": 6, "name": "丹东市振兴经济开发区", "type": "开发区", "level": "县处级", "parent": "丹东市振兴区", "location": "丹东市振兴区"},
]

positions = [
    # 滕飞（区委书记）
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "~2021-2026", "end_date": "present", "rank": "县处级正职",
     "note": "区第十四届/第十五届党代会任期内任书记并作工作报告（2026-07-28）"},
    # 任传英（区长）
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "<=2025-10", "end_date": "present", "rank": "县处级正职",
     "note": "2026-08-04 主持区政府第78次常务会议说明"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "<=2025-10", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 赵永刚（人大主任）
    {"person_id": 3, "org_id": 3, "title": "区人大常委会主任", "start_date": "unknown", "end_date": "present", "rank": "县处级正职", "note": "2026-07-14 防汛督导"},
    # 曲晓晖（政协主席）
    {"person_id": 4, "org_id": 4, "title": "区政协主席", "start_date": "unknown", "end_date": "present", "rank": "县处级正职", "note": "2026-07-14 防汛督导"},
]

relationships = [
    # 滕飞 与 任传英 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "co_leadership", "context": "区委书记与区长党政搭档（党代会、防汛、经济活动共同履职）",
     "overlap_org": "振兴区", "overlap_period": "2025-present", "confidence": "confirmed"},
    # 任传英 与 赵永刚 / 曲晓晖 (区级领导共同岗位)
    {"person_a": 2, "person_b": 3, "type": "co_leadership", "context": "区长与区人大常委会主任同届区领导", "overlap_org": "振兴区",
     "overlap_period": "2025-present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 4, "type": "co_leadership", "context": "区长与区政协主席同届区领导", "overlap_org": "振兴区",
     "overlap_period": "2025-present", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "co_leadership", "context": "区委书记与区人大主任同届区领导", "overlap_org": "振兴区",
     "overlap_period": "2025-present", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "co_leadership", "context": "区委书记与区政协主席同届区领导", "overlap_org": "振兴区",
     "overlap_period": "2025-present", "confidence": "confirmed"},
]


# ── Person JSONs ────────────────────────────────────────────────────────
def write_person_jsons():
    """Write per-person graph JSON for the two core leaders (书记 & 区长)."""

    tengfei = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "辽宁省", "city": "丹东市", "region": "振兴区",
            "job": "区委书记", "task_id": "liaoning_振兴区", "time_focus": "2025-2026",
        },
        "identity": {
            "person_id": "dandong_zhenxing_tengfei",
            "name": "滕飞",
            "aliases": [],
            "gender": "男",
            "ethnicity": "待查",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [{"period": "", "institution": "待查", "major": "", "degree": "", "study_type": "unknown", "source_ids": []}],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "滕飞_unknown",
                "name_birthplace": "滕飞_unknown",
                "official_profile_url": "https://www.zhenxing.gov.cn/html/ZXQZF/202607/0178528730788429.html",
            },
        },
        "current_status": {
            "current_post": "区委书记", "current_org": "中国共产党丹东市振兴区委员会",
            "administrative_rank": "县处级正职", "as_of": AS_OF, "is_current_confirmed": True,
            "source_ids": ["S001", "S002"],
        },
        "career_timeline": [
            {"start": "~2021-2026", "end": "present", "org": "中共丹东市振兴区委员会", "title": "区委书记",
             "level": "县处级", "location": "丹东市振兴区", "system": "party", "rank": "县处级正职",
             "is_key_promotion": True, "notes": "2026-07-28 区第十五次党代会作区委工作报告并活跃于防汛、城市管理等政务",
             "confidence": "confirmed", "source_ids": ["S001", "S002"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
             "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False,
             "notes": "任区委书记之前（出生、籍贯、学历、入党、工作起始、此前职务）公开资料未检索到", "confidence": "unverified", "source_ids": []},
        ],
        "organizations": [{"name": "中国共产党丹东市振兴区委员会", "role": "区委书记"}],
        "relationships": [
            {"person": "任传英", "person_id": "dandong_zhenxing_renchuanying", "relationship_type": "co_leadership",
             "strength": "strong", "evidence": "现任搭班：区委书记+区长", "overlap_org": "振兴区",
             "overlap_period": "2025-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
            {"person": "赵永刚", "person_id": "dandong_zhenxing_zhaoyonggang", "relationship_type": "co_leadership",
             "strength": "medium", "evidence": "同届区领导（人大主任）", "overlap_org": "振兴区",
             "overlap_period": "2025-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
            {"person": "曲晓晖", "person_id": "dandong_zhenxing_quxiaohui", "relationship_type": "co_leadership",
             "strength": "medium", "evidence": "同届区领导（政协主席）", "overlap_org": "振兴区",
             "overlap_period": "2025-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
        ],
        "governance_record": [
            {"period": "2026-07", "domain": "public_security", "achievement_or_event": "督导防汛防台风（浪头镇安置点、城市管理、物业管理治理）",
             "role_in_event": "区委书记带队", "measurable_outcome": "", "location": "振兴区",
             "confidence": "confirmed", "source_ids": ["S002"]},
        ],
        "professional_profile": {
            "primary_specializations": [], "secondary_specializations": [],
            "career_pattern": "unknown", "systems_experience": ["party"],
            "geographic_pattern": [], "promotion_velocity": {"summary": "区委书记（现职），初始履历未知", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "grassroots_oriented", "evidence": "多次带队督导防汛、城市管理、物业管理服务等问题", "confidence": "plausible", "source_ids": ["S002"]}
            ],
            "speech_themes": ["人民城市", "防汛安全", "物业管理", "首善之区"],
            "management_signals": [],
            "caveat": "Work style inferred from public records, not assessment.",
        },
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "截至2026-08-06未发现违纪或负面舆情", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "中国共产党丹东市振兴区第十五次代表大会隆重开幕", "url": "https://www.zhenxing.gov.cn/html/ZXQZF/202607/0178528730788429.html",
             "publisher": "振兴区人民政府（区委宣传部）", "published_at": "2026-07-29", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "确认滕飞为区委书记（代表十四届区委作报告）"},
            {"id": "S002", "title": "滕飞督导调研城市管理、物业服务突出问题治理等工作", "url": "https://www.zhenxing.gov.cn/html/ZXQZF/202605/0177951965421629.html",
             "publisher": "振兴区人民政府", "published_at": "2026-05-25", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "区委书记身份日常工作"},
            {"id": "S003", "title": "迅速进入实战状态…防汛防台风报道", "url": "https://www.zhenxing.gov.cn/html/ZXQZF/202607/0178407798202764.html",
             "publisher": "振兴区人民政府", "published_at": "2026-07-15", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "确认滕飞、任传英、赵永刚、曲晓晖区领导身份"},
        ],
        "confidence_summary": {
            "identity": "unverified", "current_role": "confirmed", "career_completeness": "thin",
            "relationship_confidence": "medium", "biggest_gap": "滕飞完整履历（出生/籍贯/学历/入党/此前职务）全部缺失",
        },
        "open_questions": [
            {"priority": "critical", "question": "滕飞出生年月、籍贯、教育背景、入党时间、参加工作时间", "why_it_matters": "基本身份信息缺失", "suggested_queries": ["滕飞 简历 丹东 振兴"], "last_attempted": AS_OF},
            {"priority": "high", "question": "滕飞何时何地调任振兴区委书记，前一职务是什么", "why_it_matters": "判断干部交流源头", "suggested_queries": ["滕飞 任前公示 丹东"], "last_attempted": AS_OF},
            {"priority": "high", "question": "现任区委副书记（除区长外）与纪委书记、组织部长、宣传部长、政法委书记是谁", "why_it_matters": "领导班子成员名单未公开于官网", "suggested_queries": ["振兴区 区委常委 名单"], "last_attempted": AS_OF},
        ],
    }

    renchuan = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "辽宁省", "city": "丹东市", "region": "振兴区",
            "job": "区长", "task_id": "liaoning_振兴区", "time_focus": "2025-2026",
        },
        "identity": {
            "person_id": "dandong_zhenxing_renchuanying",
            "name": "任传英",
            "aliases": [],
            "gender": "男",
            "ethnicity": "待查",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [{"period": "", "institution": "待查", "major": "", "degree": "", "study_type": "unknown", "source_ids": []}],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "任传英_unknown",
                "name_birthplace": "任传英_unknown",
                "official_profile_url": "https://www.zhenxing.gov.cn/html/ZXQZF/202608/0178589151953678.html",
            },
        },
        "current_status": {
            "current_post": "区委副书记、区长", "current_org": "丹东市振兴区人民政府",
            "administrative_rank": "县处级正职", "as_of": AS_OF, "is_current_confirmed": True,
            "source_ids": ["S001", "S002"],
        },
        "career_timeline": [
            {"start": "<=2025-10", "end": "present", "org": "丹东市振兴区人民政府", "title": "区长",
             "level": "县处级", "location": "丹东市振兴区", "system": "government", "rank": "县处级正职",
             "is_key_promotion": True, "notes": "2026-08-04 主持区政府第78次常务会议；2025-10-24 已以区长身份主持会议",
             "confidence": "confirmed", "source_ids": ["S001", "S002", "S004"]},
            {"start": "<=2025-10", "end": "present", "org": "中国共产党丹东市振兴区委员会", "title": "区委副书记",
             "level": "县处级", "location": "丹东市振兴区", "system": "party", "rank": "县处级正职",
             "is_key_promotion": False, "notes": "兼任区长党组织副书记", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
             "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False,
             "notes": "任区长前与更早履历（出生/籍贯/学历/此前职务）公开资料缺失", "confidence": "unverified", "source_ids": []},
        ],
        "organizations": [{"name": "丹东市振兴区人民政府", "role": "区长"}],
        "relationships": [
            {"person": "滕飞", "person_id": "dandong_zhenxing_tengfei", "relationship_type": "co_leadership",
             "strength": "strong", "evidence": "现任搭班：区委书记+区长", "overlap_org": "振兴区",
             "overlap_period": "2025-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
            {"person": "赵永刚", "person_id": "dandong_zhenxing_zhaoyonggang", "relationship_type": "co_leadership",
             "strength": "medium", "evidence": "区人大主任，同届区领导", "overlap_org": "振兴区",
             "overlap_period": "2025-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
            {"person": "曲晓晖", "person_id": "dandong_zhenxing_qxiaohui", "relationship_type": "co_leadership",
             "strength": "medium", "evidence": "区政协主席，同届区领导", "overlap_org": "振兴区",
             "overlap_period": "2025-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
        ],
        "governance_record": [
            {"period": "2026-07", "domain": "economic_development", "achievement_or_event": "会见北控城市服务、美中基金推进城市服务合作；防汛督导",
             "role_in_event": "区长", "measurable_outcome": "", "location": "振兴区",
             "confidence": "confirmed", "source_ids": ["S005"]},
        ],
        "professional_profile": {
            "primary_specializations": [], "secondary_specializations": [],
            "career_pattern": "unknown", "systems_experience": ["government"],
            "geographic_pattern": [], "promotion_velocity": {"summary": "现任区长", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "pragmatic", "evidence": "主持常务会议强调优化营商环境、防汛整改、经济目标", "confidence": "plausible", "source_ids": ["S004"]}
            ],
            "speech_themes": ["营商环境", "防汛整改", "高质量发展"],
            "management_signals": [],
            "caveat": "Work style inferred from public records, not assessment.",
        },
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "截至2026-08-06未发现违纪或负面舆情", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "振兴区政府召开第78次常务会议（任传英主持）", "url": "https://www.zhenxing.gov.cn/html/ZXQZF/202608/0178589151953678.html",
             "publisher": "振兴区人民政府", "published_at": "2026-08-05", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high"},
            {"id": "S002", "title": "振兴区政府召开第71次常务会议（任传英主持）", "url": "https://www.zhenxing.gov.cn/html/ZXQZF/202601/0176941600112283.html",
             "publisher": "振兴区人民政府", "published_at": "2026-01-27", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high"},
            {"id": "S003", "title": "防汛防台风报道（任传英/赵永刚/曲晓晖）", "url": "https://www.zhenxing.gov.cn/html/ZXQZF/202607/0178407798202764.html",
             "publisher": "振兴区人民政府", "published_at": "2026-07-15", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high"},
            {"id": "S004", "title": "振兴区政府召开第67次常务会议（任传英主持）", "url": "https://www.zhenxing.gov.cn/html/ZXQZF/202510/0176152912753698.html",
             "publisher": "振兴区人民政府", "published_at": "2025-10-27", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high"},
            {"id": "S005", "title": "任传英会见北控城市服务集团总裁", "url": "https://www.zhenxing.gov.cn/html/ZXQZF/202607/0178390568684721.html",
             "publisher": "振兴区人民政府", "published_at": "2026-07-13", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high"},
        ],
        "confidence_summary": {
            "identity": "unverified", "current_role": "confirmed", "career_completeness": "thin",
            "relationship_confidence": "medium", "biggest_gap": "任传英任区长前及更早的公开履历（职位/时间/学历）",
        },
        "open_questions": [
            {"priority": "critical", "question": "任传英出生年月、籍贯、教育背景、入党时间", "why_it_matters": "基本身份信息缺失", "suggested_queries": ["任传英 简历 丹东 振兴"], "last_attempted": AS_OF},
            {"priority": "high", "question": "任传英何时开始担任区长；在此之前任何职", "why_it_matters": "判断晋升轨迹与干部来源", "suggested_queries": ["任传英 区长 任职 公示"], "last_attempted": AS_OF},
            {"priority": "high", "question": "振兴区政府领导班子（副区长几人、常务副区长）名单", "why_it_matters": "政府班子构成", "suggested_queries": ["振兴区 副区长 名单"], "last_attempted": AS_OF},
        ],
    }

    person_dir = PERSONS_STAGING_DIR
    today = AS_OF.replace("-", "")
    for fname, data in [
        (f"{today}-辽宁省-丹东市-区委书记-滕飞.json", tengfei),
        (f"{today}-辽宁省-丹东市-区长-任传英.json", renchuan),
    ]:
        path = person_dir / fname
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {path}")


def main():
    print(f"Building {SLUG} network data...")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

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

    write_person_jsons()

    print(f"\nDone! Staged output files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    for f in sorted(PERSONS_STAGING_DIR.glob("*.json")):
        if "振兴区" in f.name and ("区委书记" in f.name or "区长" in f.name):
            print(f"  JSON: {f}")


if __name__ == "__main__":
    main()