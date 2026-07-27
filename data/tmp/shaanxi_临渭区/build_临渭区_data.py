#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 临渭区, 渭南市, 陕西省.

Investigation date: 2026-07-25
Task ID: shaanxi_临渭区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - 临渭区人民政府官方网站 (www.linwei.gov.cn) — multiple news articles confirming current leadership
  - 百度百科 — 马世仓 biography
  - Appointment notices from 临渭区人大常委会

Confidence notes:
  - 菊峰（区委书记）: 多次在区委常委会和全区大会报道中明确标注"区委书记菊峰"，当前身份确认
  - 马世仓（区委副书记、代区长）: 百度百科有基本履历、区人大常委会任命决定确认
  - 菊峰的完整履历（出生年份、籍贯、教育背景、早期任职）尚未找到，标为待查
  - 区政府领导分工信息从新闻报道中部分提取
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

sys.path.insert(0, os.path.abspath(os.path.join(BASE, "..", "..", "..")))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "临渭区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

STAGING_DIR = Path(BASE)
DB_PATH = str(STAGING_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(STAGING_DIR / f"{SLUG}_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════════
# Data
# ═══════════════════════════════════════════════════════════════════════════════

persons_data = [
    # ══════════════════════════════════════════════════════════════════════════
    # Party Committee (区委) Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 菊峰 — 区委书记
    {
        "id": 1,
        "name": "菊峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共渭南市临渭区委员会",
        "source": "临渭区政府官网新闻多次确认（2026年7月6日、7月13日、7月17日、7月21日等多篇报道认证'区委书记菊峰'）"
    },
    # 马世仓 — 区委副书记、代区长
    {
        "id": 2,
        "name": "马世仓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年12月",
        "birthplace": "陕西蒲城",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、代区长",
        "current_org": "渭南市临渭区人民政府",
        "source": "https://baike.baidu.com/item/马世仓"
    },
    # 李云鹏 — 区委常委、副区长
    {
        "id": 3,
        "name": "李云鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "渭南市临渭区人民政府",
        "source": "临渭区政府官网在线访谈（2026年5月9日）和调研报道（2026年7月14日）确认"
    },
    # 马博 — 区级领导（具体职务待确认）
    {
        "id": 4,
        "name": "马博",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区级领导",
        "current_org": "渭南市临渭区",
        "source": "临渭区政府官网报道：菊峰调研人民街道、解放街道时'区级领导马博…参加'（2026-07-06）"
    },
    # 阮光民 — 副区长
    {
        "id": 5,
        "name": "阮光民",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "渭南市临渭区人民政府",
        "source": "临渭区政府官网在线访谈（2026年7月13日）和调研报道（2026年7月14日）确认"
    },
]

organizations_data = [
    {
        "id": 1,
        "name": "中共渭南市临渭区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共渭南市委员会",
        "location": "渭南市临渭区"
    },
    {
        "id": 2,
        "name": "渭南市临渭区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "渭南市人民政府",
        "location": "渭南市临渭区"
    },
    {
        "id": 3,
        "name": "渭南市临渭区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "渭南市人民代表大会常务委员会",
        "location": "渭南市临渭区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议渭南市临渭区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协渭南市委员会",
        "location": "渭南市临渭区"
    },
    {
        "id": 5,
        "name": "中共渭南市临渭区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共渭南市纪律检查委员会",
        "location": "渭南市临渭区"
    },
]

positions_data = [
    # 区委（党委系统）
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "confirmed via multiple news articles (2026-07-06 onward)"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "2026-06", "end_date": "present", "rank": "正处级", "note": "appointed as acting district mayor June 2026"},
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "confirmed via online interview 2026-05-09"},

    # 区政府
    {"person_id": 2, "org_id": 2, "title": "代区长", "start_date": "2026-06", "end_date": "present", "rank": "正处级", "note": "2026年6月24日区人大常委会任命为副区长、代区长"},
    {"person_id": 3, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "confirmed via multiple news articles"},
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "confirmed via online interview 2026-07-13"},
]

relationships_data = [
    # 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记——代区长党政搭档", "overlap_org": "中共临渭区委/临渭区人民政府", "overlap_period": "2026-06-present"},
    {"person_a": 1, "person_b": 2, "type": "会议互动", "context": "'两优一先'表彰大会：菊峰讲话，马世仓主持（2026-07-06）", "overlap_org": "中共临渭区委", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 2, "type": "会议互动", "context": "上半年重点工作点评会：菊峰讲话，马世仓主持（2026-07-15）", "overlap_org": "中共临渭区委/临渭区人民政府", "overlap_period": "2026-07"},

    # 区长与副区长
    {"person_a": 2, "person_b": 3, "type": "党政搭档", "context": "代区长——区委常委、副区长工作关系", "overlap_org": "临渭区人民政府", "overlap_period": "2026-06-present"},
    {"person_a": 2, "person_b": 5, "type": "党政搭档", "context": "代区长——副区长工作关系", "overlap_org": "临渭区人民政府", "overlap_period": "2026-06-present"},
    {"person_a": 2, "person_b": 3, "type": "调研同组", "context": "马世仓调研自然资源局等，李云鹏参加（2026-07-14）", "overlap_org": "临渭区人民政府", "overlap_period": "2026-07"},

    # 区委书记与区领导
    {"person_a": 1, "person_b": 4, "type": "调研同组", "context": "菊峰调研人民街道、解放街道，马博参加（2026-07-02）", "overlap_org": "中共临渭区委", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 5, "type": "调研同组", "context": "菊峰调研人民街道、解放街道，阮光民参加（2026-07-02）", "overlap_org": "中共临渭区委", "overlap_period": "2026-07"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON generation
# ═══════════════════════════════════════════════════════════════════════════════

PERSON_JSON_TEMPLATE = {
    "菊峰": {
        "filename": f"{TODAY}-陕西省-渭南市-临渭区-区委书记-菊峰.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "陕西省",
                "city": "渭南市",
                "region": "临渭区",
                "job": "区委书记",
                "task_id": "shaanxi_临渭区",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "linwei_ju_feng",
                "name": "菊峰",
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
                    "name_birth": "菊峰_未知",
                    "name_birthplace": "菊峰_未知",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "区委书记",
                "current_org": "中共渭南市临渭区委员会",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002", "S003", "S004"]
            },
            "career_timeline": [
                {"start": "unknown", "end": "present", "org": "渭南市临渭区委员会", "title": "区委书记", "level": "县处级", "location": "陕西渭南", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "当前在任", "confidence": "confirmed", "source_ids": ["S001", "S002", "S003", "S004"]},
                {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未找到菊峰任临渭区委书记前的完整履历", "confidence": "unverified", "source_ids": []},
            ],
            "organizations": [],
            "relationships": [
                {"person": "马世仓", "person_id": "linwei_ma_shicang", "relationship_type": "overlap", "strength": "strong", "evidence": "区委书记——代区长党政搭档，多次共同出席全区会议", "overlap_org": "中共临渭区委/临渭区人民政府", "overlap_period": "2026-06-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
                {"person": "阮光民", "person_id": "linwei_ruan_guangmin", "relationship_type": "overlap", "strength": "medium", "evidence": "菊峰调研基层，阮光民陪同参加", "overlap_org": "中共临渭区委", "overlap_period": "2026-07", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
                {"person": "马博", "person_id": "linwei_ma_bo", "relationship_type": "overlap", "strength": "medium", "evidence": "菊峰调研基层，马博陪同参加", "overlap_org": "中共临渭区委", "overlap_period": "2026-07", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
            ],
            "governance_record": [
                {"period": "2026-07", "domain": "urban_construction", "achievement_or_event": "调研人民街道、解放街道，部署城市精细化管理和民生保障工作", "role_in_event": "带队调研并主持座谈", "measurable_outcome": "", "location": "渭南临渭区", "confidence": "confirmed", "source_ids": ["S004"]},
                {"period": "2026-07", "domain": "economic_development", "achievement_or_event": "主持召开2026年上半年重点工作点评会，部署经济稳增长、项目建设、招商引资", "role_in_event": "主持会议并讲话", "measurable_outcome": "", "location": "渭南临渭区", "confidence": "confirmed", "source_ids": ["S003"]},
            ],
            "professional_profile": {
                "primary_specializations": ["党的建设", "经济工作", "城市治理"],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["party", "government"],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "当前确认职务为临渭区委书记，此前履历待查", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "discipline_oriented", "evidence": "多次强调全面从严治党、正风肃纪反腐", "confidence": "plausible", "source_ids": ["S001", "S002"]},
                    {"trait": "pragmatic", "evidence": "讲话中强调紧抓项目建设和具体工作落实，年初目标清单化管理", "confidence": "plausible", "source_ids": ["S003"]},
                ],
                "speech_themes": ["党建引领", "高质量发展", "城市精细化管理", "民生保障"],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分、审计问题或负面报道", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [
                {"id": "S001", "title": "临渭区召开'两优一先'表彰大会 菊峰出席并讲话 马世仓主持", "url": "https://www.linwei.gov.cn/xwzx/bdxw/2073944405546545154.html", "publisher": "临渭区人民政府", "published_at": "2026-07-06", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认菊峰为区委书记"},
                {"id": "S002", "title": "临渭区委常委会召开会议 菊峰主持", "url": "https://www.linwei.gov.cn/xwzx/bdxw/2079364296652414978.html", "publisher": "临渭区人民政府", "published_at": "2026-07-21", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认菊峰为区委书记"},
                {"id": "S003", "title": "临渭区召开2026年上半年重点工作点评会 菊峰讲话 马世仓主持", "url": "https://www.linwei.gov.cn/xwzx/bdxw/2077914057566842882.html", "publisher": "临渭区人民政府", "published_at": "2026-07-17", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "区委书记菊峰讲话"},
                {"id": "S004", "title": "菊峰调研人民街道 解放街道工作", "url": "https://www.linwei.gov.cn/xwzx/bdxw/2073943685319507970.html", "publisher": "临渭区人民政府", "published_at": "2026-07-06", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "区委书记菊峰调研"},
            ],
            "confidence_summary": {"identity": "partial", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": "菊峰完整的履历（出生年份、籍贯、教育背景、此前所有任职经历）"},
            "open_questions": [
                {"priority": "critical", "question": "菊峰的完整履历（出生年份、籍贯、教育背景、此前所有任职经历）", "why_it_matters": "关键人物，履历缺失严重影响关系网络分析", "suggested_queries": ["菊峰 简历 渭南", "菊峰 任前公示", "菊峰 百度百科"], "last_attempted": AS_OF},
                {"priority": "high", "question": "菊峰何时就任临渭区委书记？前任是谁？", "why_it_matters": "确定任期起点和前任去向", "suggested_queries": ["临渭区 前任区委书记", "临渭区 区委书记 任命"], "last_attempted": AS_OF},
            ]
        }
    },
    "马世仓": {
        "filename": f"{TODAY}-陕西省-渭南市-临渭区-代区长-马世仓.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {"province": "陕西省", "city": "渭南市", "region": "临渭区", "job": "代区长", "task_id": "shaanxi_临渭区", "time_focus": "2026"},
            "identity": {
                "person_id": "linwei_ma_shicang",
                "name": "马世仓",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1979年12月",
                "birthplace": "陕西蒲城",
                "native_place": "陕西蒲城",
                "education": ["大学学历"],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {"name_birth": "马世仓_1979年12月", "name_birthplace": "马世仓_陕西蒲城", "official_profile_url": "https://baike.baidu.com/item/马世仓"}
            },
            "current_status": {"current_post": "区委副书记、代区长", "current_org": "渭南市临渭区人民政府", "administrative_rank": "正处级", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S101", "S102"]},
            "career_timeline": [
                {"start": "unknown", "end": "unknown", "org": "潼关县委", "title": "县委常委、纪委书记、监委会主任", "level": "县处级", "location": "陕西潼关", "system": "discipline", "rank": "副处级", "is_key_promotion": False, "notes": "曾任潼关县纪委书记", "confidence": "confirmed", "source_ids": ["S101"]},
                {"start": "2025-04", "end": "2026-07", "org": "渭南市行政审批服务局", "title": "局长", "level": "地厅级", "location": "陕西渭南", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "2025年4月任行政审批服务局局长, 2026年7月3日免职", "confidence": "confirmed", "source_ids": ["S101"]},
                {"start": "2026-06", "end": "present", "org": "渭南市临渭区人民政府", "title": "副区长、代区长", "level": "县处级", "location": "陕西渭南", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "2026年6月24日区人大常委会任命", "confidence": "confirmed", "source_ids": ["S101", "S102"]},
            ],
            "organizations": [],
            "relationships": [
                {"person": "菊峰", "person_id": "linwei_ju_feng", "relationship_type": "overlap", "strength": "strong", "evidence": "区委书记——代区长党政搭档", "overlap_org": "中共临渭区委/临渭区人民政府", "overlap_period": "2026-06-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S102"]},
                {"person": "李云鹏", "person_id": "linwei_li_yunpeng", "relationship_type": "overlap", "strength": "strong", "evidence": "代区长——区委常委、副区长工作搭档", "overlap_org": "临渭区人民政府", "overlap_period": "2026-06-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S103"]},
                {"person": "阮光民", "person_id": "linwei_ruan_guangmin", "relationship_type": "overlap", "strength": "strong", "evidence": "代区长——副区长工作搭档", "overlap_org": "临渭区人民政府", "overlap_period": "2026-06-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S103"]},
            ],
            "governance_record": [
                {"period": "2026-07", "domain": "public_service", "achievement_or_event": "调研区行政审批局，部署优化营商环境", "role_in_event": "带队调研", "measurable_outcome": "", "location": "渭南临渭区", "confidence": "confirmed", "source_ids": ["S103"]},
                {"period": "2026-07", "domain": "environment", "achievement_or_event": "调研生态环境临渭分局，部署大气治理和水环境治理", "role_in_event": "带队调研", "measurable_outcome": "", "location": "渭南临渭区", "confidence": "confirmed", "source_ids": ["S103"]},
            ],
            "professional_profile": {
                "primary_specializations": ["纪检监察", "行政审批", "自然资源"],
                "secondary_specializations": [],
                "career_pattern": "从潼关县纪委书记→市行政审批局长→临渭区代区长，跨纪检监察、行政审批、区县政府多岗位",
                "systems_experience": ["discipline", "government"],
                "geographic_pattern": ["陕西蒲城→潼关→渭南"],
                "promotion_velocity": {"summary": "从县纪委书记到市局一把手再到区代区长，经历丰富，属于稳步晋升", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "pragmatic", "evidence": "调研中强调'全力打造一流营商环境高地'，要求'清单化管理、项目化推进'", "confidence": "plausible", "source_ids": ["S103"]},
                    {"trait": "discipline_oriented", "evidence": "曾任潼关县纪委书记，在调研中强调'坚守红线'、'问题整改动真碰硬'", "confidence": "plausible", "source_ids": ["S101", "S103"]},
                ],
                "speech_themes": ["优化营商环境", "生态环境保护", "高质量发展"],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分或负面报道", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [
                {"id": "S101", "title": "马世仓 - 百度百科", "url": "https://baike.baidu.com/item/马世仓", "publisher": "百度百科", "published_at": "2026", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "包含基本履历和任免信息"},
                {"id": "S102", "title": "临渭区召开'两优一先'表彰大会", "url": "https://www.linwei.gov.cn/xwzx/bdxw/2073944405546545154.html", "publisher": "临渭区人民政府", "published_at": "2026-07-06", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认马世仓为区委副书记、代区长"},
                {"id": "S103", "title": "马世仓调研自然资源 生态环境及行政审批重点工作", "url": "https://www.linwei.gov.cn/xwzx/bdxw/2076824413204041730.html", "publisher": "临渭区人民政府", "published_at": "2026-07-14", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认代区长身份及调研内容"},
            ],
            "confidence_summary": {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "partial", "relationship_confidence": "high", "biggest_gap": "马世仓在潼关县纪委书记的具体起止时间及更早的职业生涯"},
            "open_questions": [
                {"priority": "high", "question": "马世仓任潼关县纪委书记的具体起止时间", "why_it_matters": "准确的时间线对关系网络分析重要", "suggested_queries": ["马世仓 潼关 纪委书记 任职时间"], "last_attempted": AS_OF},
                {"priority": "medium", "question": "马世仓更早期的职业生涯（大学毕业后到潼关县纪委书记之前）", "why_it_matters": "完善简历完整性", "suggested_queries": ["马世仓 早期 履历"], "last_attempted": AS_OF},
            ]
        }
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

def write_person_json(data: dict, filename: str) -> Path:
    path = STAGING_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {path}")
    return path

def main():
    print(f"Building network for {SLUG}...")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print()

    run_build(
        slug=SLUG,
        persons=persons_data,
        organizations=organizations_data,
        positions=positions_data,
        relationships=relationships_data,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print()

    print("Writing person JSON files...")
    for key, entry in PERSON_JSON_TEMPLATE.items():
        write_person_json(entry["data"], entry["filename"])

    print()
    print("=" * 60)
    print(f"Build complete for {SLUG}")
    print(f"  {len(persons_data)} persons")
    print(f"  {len(organizations_data)} organizations")
    print(f"  {len(positions_data)} positions")
    print(f"  {len(relationships_data)} relationships")
    print(f"  {len(PERSON_JSON_TEMPLATE)} person JSONs")
    print("=" * 60)

if __name__ == "__main__":
    main()
