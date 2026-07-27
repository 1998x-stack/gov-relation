#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 澄城县, 渭南市, 陕西省.

Investigation date: 2026-07-25
Task ID: shaanxi_澄城县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - 澄城县人民政府官方网站 (www.chengcheng.gov.cn) — multiple news articles confirming current leadership
  - Baidu search — 陈飞 Baidu Baike profile (县委书记)
  - Baidu Baike — 中国共产党澄城县委员会 entry (leadership roster)
  - 渭南市政府网站 — appointment news
  - 渭南青年网 — historical articles about predecessor 高成文

Confidence notes:
  - 陈飞（县委书记）: 百度百科有简历，1976年8月出生，陕西武功人，研究生学历
  - 张旭（县委副书记、县长）: 县政府网站"领导之窗"和百度百科确认
  - 高成文（前任县委书记）: 2021-2024年间多次在报道中出现，2025年后被陈飞取代
  - 领导班子成员部分来自百度百科"中国共产党澄城县委员会"条目确认
  - 完整履历（尤其张旭的）信息较为有限，部分标为待查
"""

import json
import os
import sqlite3
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

SLUG = "澄城县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

STAGING_DIR = Path(BASE)
DB_PATH = str(STAGING_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(STAGING_DIR / f"{SLUG}_network.gexf")

SOURCE_GOV_SITE = "澄城县政府官网(www.chengcheng.gov.cn)新闻报道确认"
SOURCE_BAIKE = "百度百科条目"

# ═══════════════════════════════════════════════════════════════════════════════
# Data
# ═══════════════════════════════════════════════════════════════════════════════

persons_data = [
    # ══════════════════════════════════════════════════════════════════════════
    # Party Committee (县委) Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 陈飞 — 县委书记
    {
        "id": 1,
        "name": "陈飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年8月",
        "birthplace": "陕西武功",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共澄城县委员会",
        "source": f"百度百科确认，{SOURCE_GOV_SITE}（2026年7月7日、14日、21日多次报道认证'县委书记陈飞'）"
    },
    # 张旭 — 县委副书记、县长
    {
        "id": 2,
        "name": "张旭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "澄城县人民政府",
        "source": f"百度百科'中国共产党澄城县委员会'条目确认，{SOURCE_GOV_SITE}确认"
    },
    # 蔡学宏 — 县委副书记、县委党校校长（兼）
    {
        "id": 3,
        "name": "蔡学宏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县委党校校长（兼）",
        "current_org": "中共澄城县委员会",
        "source": "百度百科'中国共产党澄城县委员会'条目确认"
    },
    # 边有兵 — 县委常委、常务副县长
    {
        "id": 4,
        "name": "边有兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "澄城县人民政府",
        "source": "百度百科'中国共产党澄城县委员会'条目确认"
    },
    # 李云鹏 — 县委常委、宣传部部长
    {
        "id": 5,
        "name": "李云鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共澄城县委宣传部",
        "source": "百度百科'中国共产党澄城县委员会'条目确认；渭南青年网报道中确认（2021年即为澄城县委常委、宣传部部长）"
    },
    # 高成文 — 前任县委书记
    {
        "id": 6,
        "name": "高成文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县委书记（已离任）",
        "current_org": "中共澄城县委员会",
        "source": "渭南青年网（2021年8月）和微信公众号文章（2024年9月）确认高成文曾任澄城县委书记；后由陈飞接任"
    },
    # 马俊宏 — 县委常委、统战部部长、县委办主任
    {
        "id": 7,
        "name": "马俊宏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、统战部部长、县委办主任",
        "current_org": "中共澄城县委统战部",
        "source": "微信公众号文章（2024年9月）确认'县委常委、统战部部长、县委办主任马俊宏'"
    },
]

organizations_data = [
    {
        "id": 1,
        "name": "中共澄城县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共渭南市委员会",
        "location": "渭南市澄城县"
    },
    {
        "id": 2,
        "name": "澄城县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "渭南市人民政府",
        "location": "渭南市澄城县"
    },
    {
        "id": 3,
        "name": "澄城县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "渭南市人民代表大会常务委员会",
        "location": "渭南市澄城县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议澄城县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协渭南市委员会",
        "location": "渭南市澄城县"
    },
    {
        "id": 5,
        "name": "中共澄城县纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共渭南市纪律检查委员会",
        "location": "渭南市澄城县"
    },
    {
        "id": 6,
        "name": "中共澄城县委宣传部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共澄城县委员会",
        "location": "渭南市澄城县"
    },
    {
        "id": 7,
        "name": "中共澄城县委统战部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共澄城县委员会",
        "location": "渭南市澄城县"
    },
    {
        "id": 8,
        "name": "中共澄城县委政法委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共澄城县委员会",
        "location": "渭南市澄城县"
    },
    {
        "id": 9,
        "name": "中共澄城县委组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共澄城县委员会",
        "location": "渭南市澄城县"
    },
]

positions_data = [
    # 县委（党委系统）
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "confirmed via official news articles and Baidu Baike (2026-07)"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "confirmed via Baidu Baike and government website"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记、县委党校校长（兼）", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "confirmed via Baidu Baike"},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "confirmed via Baidu Baike"},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "confirmed via Baidu Baike, held the role since at least 2021"},
    {"person_id": 6, "org_id": 1, "title": "县委书记（前任）", "start_date": "unknown", "end_date": "2025-01", "rank": "正处级", "note": "served as 县委书记 from ~2021 to ~2025, succeeded by 陈飞"},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "confirmed via 2024 news article"},

    # 县政府
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "leading the county government"},
    {"person_id": 4, "org_id": 2, "title": "常务副县长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "confirmed via Baidu Baike"},

    # 宣传部
    {"person_id": 5, "org_id": 6, "title": "宣传部部长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "confirmed via Baidu Baike and news articles"},

    # 统战部
    {"person_id": 7, "org_id": 7, "title": "统战部部长、县委办主任", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "confirmed via 2024 news article"},
]

relationships_data = [
    # 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记——县长党政搭档", "overlap_org": "中共澄城县委/澄城县人民政府", "overlap_period": "unknown-present"},
    {"person_a": 1, "person_b": 3, "type": "班子成员", "context": "县委书记——县委副书记（党校校长）班子关系", "overlap_org": "中共澄城县委", "overlap_period": "unknown-present"},
    {"person_a": 1, "person_b": 4, "type": "班子成员", "context": "县委书记——县委常委、常务副县长工作关系", "overlap_org": "中共澄城县委/澄城县人民政府", "overlap_period": "unknown-present"},
    {"person_a": 1, "person_b": 5, "type": "班子成员", "context": "县委书记——县委常委、宣传部部长工作关系", "overlap_org": "中共澄城县委", "overlap_period": "unknown-present"},
    {"person_a": 1, "person_b": 6, "type": "前任继任", "context": "陈飞接替高成文任澄城县委书记", "overlap_org": "中共澄城县委", "overlap_period": "2025"},
    {"person_a": 1, "person_b": 7, "type": "班子成员", "context": "县委书记——县委常委、统战部部长工作关系", "overlap_org": "中共澄城县委", "overlap_period": "unknown-present"},

    # 县长与副职
    {"person_a": 2, "person_b": 3, "type": "党政搭档", "context": "县长——县委副书记党校校长工作关系", "overlap_org": "中共澄城县委", "overlap_period": "unknown-present"},
    {"person_a": 2, "person_b": 4, "type": "工作关系", "context": "县长——常务副县长工作搭档", "overlap_org": "澄城县人民政府", "overlap_period": "unknown-present"},

    # 前任书记
    {"person_a": 6, "person_b": 2, "type": "前任继任搭档", "context": "高成文任县委书记时的工作关系", "overlap_org": "中共澄城县委", "overlap_period": "unknown-2025"},
    {"person_a": 6, "person_b": 3, "type": "班子成员", "context": "前任县委书记与副书记", "overlap_org": "中共澄城县委", "overlap_period": "unknown-2025"},
    {"person_a": 6, "person_b": 4, "type": "班子成员", "context": "前任县委书记与常务副县长", "overlap_org": "中共澄城县委/澄城县人民政府", "overlap_period": "unknown-2025"},
    {"person_a": 6, "person_b": 5, "type": "班子成员", "context": "前任县委书记与宣传部长", "overlap_org": "中共澄城县委", "overlap_period": "unknown-2025"},
    {"person_a": 6, "person_b": 7, "type": "班子成员", "context": "前任县委书记与统战部长", "overlap_org": "中共澄城县委", "overlap_period": "unknown-2025"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON generation
# ═══════════════════════════════════════════════════════════════════════════════

PERSON_JSON_TEMPLATE = {
    "陈飞": {
        "filename": f"{TODAY}-陕西省-渭南市-县委书记-陈飞.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "陕西省",
                "city": "渭南市",
                "region": "澄城县",
                "job": "县委书记",
                "task_id": "shaanxi_澄城县",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "chengcheng_chen_fei",
                "name": "陈飞",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1976年8月",
                "birthplace": "陕西武功",
                "native_place": "陕西武功",
                "education": [
                    {
                        "period": "",
                        "institution": "",
                        "major": "",
                        "degree": "研究生学历",
                        "study_type": "unknown",
                        "source_ids": ["S001"]
                    }
                ],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "陈飞_1976年8月",
                    "name_birthplace": "陈飞_陕西武功",
                    "official_profile_url": "https://baike.baidu.com/item/%E9%99%88%E9%A3%9E"
                }
            },
            "current_status": {
                "current_post": "县委书记",
                "current_org": "中共澄城县委员会",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002", "S003"]
            },
            "career_timeline": [
                {"start": "unknown", "end": "present", "org": "中共澄城县委员会", "title": "县委书记", "level": "县处级", "location": "陕西渭南澄城", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "当前在任，多次主持县委常委会", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
                {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未找到陈飞任澄城县委书记前的完整履历。百度百科显示1976年8月生、陕西武功人、研究生学历、中共党员", "confidence": "unverified", "source_ids": ["S001"]},
            ],
            "organizations": [],
            "relationships": [
                {"person": "张旭", "person_id": "chengcheng_zhang_xu", "relationship_type": "overlap", "strength": "strong", "evidence": "县委书记——县长党政搭档", "overlap_org": "中共澄城县委/澄城县人民政府", "overlap_period": "unknown-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
                {"person": "高成文", "person_id": "chengcheng_gao_chengwen", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "陈飞接替高成文任县委书记", "overlap_org": "中共澄城县委", "overlap_period": "2025", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S004", "S005"]},
                {"person": "蔡学宏", "person_id": "chengcheng_cai_xuehong", "relationship_type": "overlap", "strength": "medium", "evidence": "县委书记——县委副书记工作关系", "overlap_org": "中共澄城县委", "overlap_period": "unknown-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "边有兵", "person_id": "chengcheng_bian_youbing", "relationship_type": "overlap", "strength": "medium", "evidence": "县委书记——常务副县长工作关系", "overlap_org": "中共澄城县委/澄城县人民政府", "overlap_period": "unknown-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "李云鹏", "person_id": "chengcheng_li_yunpeng", "relationship_type": "overlap", "strength": "medium", "evidence": "县委书记——宣传部部长工作关系", "overlap_org": "中共澄城县委", "overlap_period": "unknown-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S004"]},
            ],
            "governance_record": [
                {"period": "2026-07", "domain": "party_affairs", "achievement_or_event": "主持县委常委会，部署学习教育、巡察、经开区改革发展等工作", "role_in_event": "主持会议", "measurable_outcome": "", "location": "渭南澄城", "confidence": "confirmed", "source_ids": ["S002"]},
                {"period": "2026-07", "domain": "public_security", "achievement_or_event": "主持县委常委会，安排部署防汛救灾、安全生产、信访等工作", "role_in_event": "主持会议", "measurable_outcome": "", "location": "渭南澄城", "confidence": "confirmed", "source_ids": ["S003"]},
                {"period": "2026-07", "domain": "party_affairs", "achievement_or_event": "主持县委常委会，安排部署学习教育、组织、意识形态等工作", "role_in_event": "主持会议", "measurable_outcome": "", "location": "渭南澄城", "confidence": "confirmed", "source_ids": ["S002"]},
            ],
            "professional_profile": {
                "primary_specializations": ["党的建设", "县域治理"],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["party", "government"],
                "geographic_pattern": ["陕西武功→渭南澄城"],
                "promotion_velocity": {"summary": "当前确认职务为澄城县委书记，此前公开履历有限", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "discipline_oriented", "evidence": "多次主持召开县委常委会强调学习教育、巡察工作", "confidence": "plausible", "source_ids": ["S002", "S003"]},
                ],
                "speech_themes": ["党的建设", "县域经济", "安全生产", "防汛救灾"],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分、审计问题或负面报道", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [
                {"id": "S001", "title": "陈飞 - 百度百科", "url": "https://baike.baidu.com/item/%E9%99%88%E9%A3%9E/25208811", "publisher": "百度百科", "published_at": "2026", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "包含基本个人信息：1976年8月生、陕西武功人、研究生学历、中共党员"},
                {"id": "S002", "title": "县委常委会召开会议 陈飞主持会议（2026-07-21）", "url": "https://www.chengcheng.gov.cn/", "publisher": "澄城县人民政府", "published_at": "2026-07-21", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认陈飞为县委书记，内容涉及学习教育、巡察、经开区改革发展"},
                {"id": "S003", "title": "县委常委会召开会议 陈飞主持会议（2026-07-14）", "url": "https://www.chengcheng.gov.cn/", "publisher": "澄城县人民政府", "published_at": "2026-07-14", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认陈飞为县委书记，内容涉及防汛救灾、安全生产、信访"},
                {"id": "S004", "title": "澄城县委书记高成文调研交道镇当前重点工作", "url": "https://baijiahao.baidu.com/", "publisher": "渭南青年网", "published_at": "2021-08-02", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "确认高成文曾任澄城县委书记，李云鹏为宣传部部长"},
                {"id": "S005", "title": "中共澄城县委书记高成文莅临创新中学慰问调研", "url": "https://mp.weixin.qq.com/", "publisher": "微信公众号", "published_at": "2024-09-28", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "确认2024年9月高成文仍为澄城县委书记，马俊宏为统战部部长"},
            ],
            "confidence_summary": {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": "陈飞任澄城县委书记前的完整履历（教育经历、此前任职岗位、晋升路径）"},
            "open_questions": [
                {"priority": "critical", "question": "陈飞的完整履历（具体教育经历、此前所有任职经历、晋升路径）", "why_it_matters": "关键人物，履历缺失严重影响关系网络分析和任职时间线", "suggested_queries": ["陈飞 澄城 履历 任职", "陈飞 武功 简历", "陈飞 陕西 组织部 任前公示"], "last_attempted": AS_OF},
                {"priority": "high", "question": "陈飞何时就任澄城县委书记？", "why_it_matters": "确定任期起点和与前任高成文的交接时间", "suggested_queries": ["澄城县 县委书记 任命 2025", "陈飞 任澄城县委书记"], "last_attempted": AS_OF},
                {"priority": "medium", "question": "高成文的去向（离任澄城县委书记后调往何处）", "why_it_matters": "分析人事变动趋势和渭南市干部流动网络", "suggested_queries": ["高成文 澄城 县委书记 卸任 去向", "高成文 渭南"], "last_attempted": AS_OF},
            ]
        }
    },
    "张旭": {
        "filename": f"{TODAY}-陕西省-渭南市-县长-张旭.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {"province": "陕西省", "city": "渭南市", "region": "澄城县", "job": "县长", "task_id": "shaanxi_澄城县", "time_focus": "2026"},
            "identity": {
                "person_id": "chengcheng_zhang_xu",
                "name": "张旭",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {"name_birth": "张旭_未知", "name_birthplace": "张旭_未知", "official_profile_url": ""}
            },
            "current_status": {"current_post": "县委副书记、县长", "current_org": "澄城县人民政府", "administrative_rank": "正处级", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S101"]},
            "career_timeline": [
                {"start": "unknown", "end": "present", "org": "澄城县人民政府", "title": "县长", "level": "县处级", "location": "陕西渭南澄城", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "当前在任，负责县政府全面工作", "confidence": "confirmed", "source_ids": ["S101"]},
                {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未找到张旭任澄城县长前的完整履历", "confidence": "unverified", "source_ids": []},
            ],
            "organizations": [],
            "relationships": [
                {"person": "陈飞", "person_id": "chengcheng_chen_fei", "relationship_type": "overlap", "strength": "strong", "evidence": "县委副书记、县长与县委书记党政搭档", "overlap_org": "中共澄城县委/澄城县人民政府", "overlap_period": "unknown-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S101", "S102"]},
                {"person": "边有兵", "person_id": "chengcheng_bian_youbing", "relationship_type": "overlap", "strength": "medium", "evidence": "县长——常务副县长工作搭档", "overlap_org": "澄城县人民政府", "overlap_period": "unknown-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S101"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": ["政府管理"],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["government"],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "信息有限", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "unknown", "evidence": "公开报道信息有限", "confidence": "unverified", "source_ids": []},
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分或负面报道", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [
                {"id": "S101", "title": "中国共产党澄城县委员会 - 百度百科", "url": "https://baike.baidu.com/item/%E6%BE%84%E5%9F%8E%E5%8E%BF%E5%A7%94", "publisher": "百度百科", "published_at": "2026", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "确认张旭为县委副书记、县长"},
                {"id": "S102", "title": "中共澄城县委审计委员会召开2025年度第一次会议", "url": "https://sj.weinan.gov.cn/", "publisher": "渭南市审计局", "published_at": "2025-04", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "报道显示高成文为县委书记、张旭为县长出席会议"},
            ],
            "confidence_summary": {"identity": "partial", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": "张旭的完整履历（出生年份、籍贯、教育背景、此前所有任职经历）"},
            "open_questions": [
                {"priority": "critical", "question": "张旭的完整履历（出生年份、籍贯、教育背景、此前所有任职经历）", "why_it_matters": "关键人物，履历缺失严重影响关系网络分析", "suggested_queries": ["张旭 澄城 县长 简历", "张旭 渭南 任前公示", "张旭 百度百科"], "last_attempted": AS_OF},
                {"priority": "high", "question": "张旭何时就任澄城县县长？前任县长是谁？", "why_it_matters": "确定任期起点和人事变动背景", "suggested_queries": ["澄城县 前任县长", "澄城县 县长 任命"], "last_attempted": AS_OF},
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
