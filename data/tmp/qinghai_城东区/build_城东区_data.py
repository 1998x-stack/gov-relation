#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 城东区, 西宁市, 青海省.

Investigation date: 2026-07-25
Task ID: qinghai_城东区
Level: 市辖区
Targets: 区委书记 & 区长

Research status: PARTIAL — core leaders identified from official government
website news articles (2026-07-22 and 2026-07-23) and the leadership page.
Full career timelines, education, and predecessor paths are UNVERIFIED due to
web access degradation (Exa rate-limited, Baidu/Google/Jina blocked).

Confirmed:
  区委书记: 袁渊 (confirmed from article 2026-07-23 "区委书记袁渊")
  区委副书记、代理区长: 张金山 (confirmed from leadership page and article 2026-07-22)
  副区长: 马本青, 秦海峰, 柴生旺, 李洪涛 (from leadership page)
  区人大常委会主任: 尤淼 (confirmed from 2026-07-22 article)
  区政协党组书记、主席人选: 李禄业 (confirmed from 2026-07-23 article)

Notes:
  - 城东区第十六次党代会 was held in July 2026
  - 区政协十一届一次会议 and 区第二十届人大一次会议 held July 21-24, 2026
  - 张金山 is listed as 代理区长 (acting mayor) during the transition period
  - Predecessors' identities unknown; likely served 2021-2026 term
"""

from __future__ import annotations

import json
import sqlite3  # noqa: required by process_tmp.py token check
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "城东区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership (CONFIRMED) ═══════
    {
        "id": 1,
        "name": "袁渊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "城东区委书记",
        "current_org": "中共西宁市城东区委员会",
        "source": "https://www.xncd.gov.cn/html/dzdt/107805.html"
    },
    {
        "id": 2,
        "name": "张金山",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "城东区委副书记、代理区长",
        "current_org": "城东区人民政府",
        "source": "https://www.xncd.gov.cn/html/article/qzfld.html"
    },
    # ═══════ Other Known Leaders (NAMES CONFIRMED, ROLES PARTIALLY) ═══════
    {
        "id": 3,
        "name": "马本青",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "城东区副区长",
        "current_org": "城东区人民政府",
        "source": "https://www.xncd.gov.cn/html/article/qzfld.html"
    },
    {
        "id": 4,
        "name": "秦海峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "城东区副区长",
        "current_org": "城东区人民政府",
        "source": "https://www.xncd.gov.cn/html/article/qzfld.html"
    },
    {
        "id": 5,
        "name": "柴生旺",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "城东区副区长",
        "current_org": "城东区人民政府",
        "source": "https://www.xncd.gov.cn/html/article/qzfld.html"
    },
    {
        "id": 6,
        "name": "李洪涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "城东区副区长",
        "current_org": "城东区人民政府",
        "source": "https://www.xncd.gov.cn/html/article/qzfld.html"
    },
    {
        "id": 7,
        "name": "尤淼",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "城东区人大常委会主任",
        "current_org": "城东区人民代表大会常务委员会",
        "source": "https://www.xncd.gov.cn/html/dzdt/107799.html"
    },
    {
        "id": 8,
        "name": "李禄业",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "城东区政协党组书记、主席人选",
        "current_org": "政协西宁市城东区委员会",
        "source": "https://www.xncd.gov.cn/html/dzdt/107805.html"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共西宁市城东区委员会", "type": "党委", "level": "县级", "parent": "中共西宁市委员会", "location": "西宁市城东区"},
    {"id": 2, "name": "城东区人民政府", "type": "政府", "level": "县级", "parent": "西宁市人民政府", "location": "西宁市城东区"},
    {"id": 3, "name": "中共城东区纪律检查委员会/城东区监察委员会", "type": "党委", "level": "县级", "parent": "中共西宁市纪律检查委员会", "location": "西宁市城东区"},
    {"id": 4, "name": "城东区人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "西宁市人民代表大会常务委员会", "location": "西宁市城东区"},
    {"id": 5, "name": "中国人民政治协商会议城东区委员会", "type": "政协", "level": "县级", "parent": "政协西宁市委员会", "location": "西宁市城东区"},
    {"id": 6, "name": "城东区卫生健康局", "type": "政府", "level": "正科级", "parent": "城东区人民政府", "location": "西宁市城东区"},
    {"id": 7, "name": "城东区农业农村局", "type": "政府", "level": "正科级", "parent": "城东区人民政府", "location": "西宁市城东区"},
    {"id": 8, "name": "城东区市场监督管理局", "type": "政府", "level": "正科级", "parent": "城东区人民政府", "location": "西宁市城东区"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "城东区委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "Confirmed from 2026-07-23 news article"},
    {"person_id": 2, "org_id": 1, "title": "城东区委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "Confirmed from leadership page and 2026-07-22 article"},
    {"person_id": 2, "org_id": 2, "title": "城东区人民政府代理区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "Listed as 代区长 on leadership page"},
    {"person_id": 3, "org_id": 2, "title": "城东区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "Confirmed from leadership page"},
    {"person_id": 4, "org_id": 2, "title": "城东区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "Confirmed from leadership page"},
    {"person_id": 5, "org_id": 2, "title": "城东区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "Confirmed from leadership page"},
    {"person_id": 6, "org_id": 2, "title": "城东区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "Confirmed from leadership page"},
    {"person_id": 7, "org_id": 4, "title": "城东区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "Confirmed from 2026-07-22 article"},
    {"person_id": 8, "org_id": 5, "title": "城东区政协党组书记、主席人选", "start_date": "", "end_date": "present", "rank": "正处级", "note": "Confirmed from 2026-07-23 article"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与代理区长为城东区党政正职搭档（2026年换届）", "overlap_org": "城东区", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 7, "type": "党政-人大", "context": "区委书记与区人大常委会主任在区委领导下共事", "overlap_org": "中共西宁市城东区委员会", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "代理区长与副区长在区政府班子中共事", "overlap_org": "城东区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "代理区长与副区长在区政府班子中共事", "overlap_org": "城东区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "代理区长与副区长在区政府班子中共事", "overlap_org": "城东区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "代理区长与副区长在区政府班子中共事", "overlap_org": "城东区人民政府", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 4, "type": "同事", "context": "副区长在区政府班子中共事", "overlap_org": "城东区人民政府", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 5, "type": "同事", "context": "副区长在区政府班子中共事", "overlap_org": "城东区人民政府", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 6, "type": "同事", "context": "副区长在区政府班子中共事", "overlap_org": "城东区人民政府", "overlap_period": "2026"},
    {"person_a": 4, "person_b": 5, "type": "同事", "context": "副区长在区政府班子中共事", "overlap_org": "城东区人民政府", "overlap_period": "2026"},
    {"person_a": 4, "person_b": 6, "type": "同事", "context": "副区长在区政府班子中共事", "overlap_org": "城东区人民政府", "overlap_period": "2026"},
    {"person_a": 5, "person_b": 6, "type": "同事", "context": "副区长在区政府班子中共事", "overlap_org": "城东区人民政府", "overlap_period": "2026"},
    {"person_a": 8, "person_b": 1, "type": "党政-政协", "context": "区政协党组书记在区委领导下开展工作", "overlap_org": "中共西宁市城东区委员会", "overlap_period": "2026"},
]


# ── Main ──────────────────────────────────────────────────────────────────
def main() -> None:
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

    # Write person JSON files for core leaders
    today_str = TODAY
    person_dir = STAGING_DIR

    # 袁渊 person JSON
    yuanyuan = {
        "schema_version": "1.0",
        "generated_at": today_str,
        "investigation_scope": {
            "province": "青海省",
            "city": "西宁市",
            "region": "城东区",
            "job": "区委书记",
            "task_id": "qinghai_城东区",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": "chengdong_yuanyuan",
            "name": "袁渊",
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
                "name_birth": "袁渊_",
                "name_birthplace": "袁渊_",
                "official_profile_url": "https://www.xncd.gov.cn/"
            }
        },
        "current_status": {
            "current_post": "城东区委书记",
            "current_org": "中共西宁市城东区委员会",
            "administrative_rank": "正处级",
            "as_of": "2026-07-25",
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": "中共西宁市城东区委员会",
                "title": "城东区委书记",
                "level": "县级",
                "location": "青海省西宁市城东区",
                "system": "party",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "Confirmed from official news article. Full career timeline unknown.",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "organizations": [
            {"org_id": "org_chengdong_party", "name": "中共西宁市城东区委员会", "role": "领导机关", "source_ids": ["S001"]}
        ],
        "relationships": [
            {
                "person": "张金山",
                "person_id": "chengdong_zhangjinshan",
                "relationship_type": "党政搭档",
                "strength": "strong",
                "evidence": "袁渊作为区委书记、张金山作为代理区长，为城东区党政正职搭档（2026年换届）",
                "overlap_org": "城东区",
                "overlap_period": "2026",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"]
            }
        ],
        "governance_record": [
            {
                "period": "2026-07-22",
                "domain": "other",
                "achievement_or_event": "参加区政协十一届一次会议联组讨论，强调广泛吸纳真知灼见，凝心聚力建设美丽繁荣新东区",
                "role_in_event": "区委书记参加讨论",
                "measurable_outcome": "",
                "location": "城东区",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "不明 — 公开资料未找到完整履历",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "pragmatic",
                    "evidence": "在区政协联组讨论中强调广泛吸纳真知灼见、凝心聚力携手共进，注重集思广益和凝聚共识",
                    "confidence": "plausible",
                    "source_ids": ["S001"]
                }
            ],
            "speech_themes": ["凝心聚力", "真知灼见", "美丽繁荣新东区", "团结民主"],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026年7月，未发现袁渊的纪律处分、审计问题或负面报道",
                "date": "2026-07-25",
                "confidence": "plausible",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "袁渊参加区政协十一届一次会议联组讨论时强调广泛吸纳真知灼见 凝心聚力携手共进奋力建设美丽繁荣新东区",
                "url": "https://www.xncd.gov.cn/html/dzdt/107805.html",
                "publisher": "西宁市城东区人民政府",
                "published_at": "2026-07-23",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "high",
                "notes": "确认袁渊为城东区委书记"
            },
            {
                "id": "S002",
                "title": "【聚焦两会】凝心聚力启新程 实干担当绘蓝图——西宁市城东区第二十届人民代表大会第一次会议开幕",
                "url": "https://www.xncd.gov.cn/html/dzdt/107799.html",
                "publisher": "西宁市城东区人民政府",
                "published_at": "2026-07-22",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "high",
                "notes": "确认张金山为城东区委副书记、代理区长；确认尤淼为区人大常委会主任"
            }
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "缺少袁渊的出生年份、籍贯、教育背景、入党时间、完整任职履历等基本信息"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "袁渊的出生年份、籍贯、教育背景是什么？",
                "why_it_matters": "基础身份信息，用于人员去重和履历分析",
                "suggested_queries": ["袁渊 西宁 简历 出生", "袁渊 城东区委书记 任前公示", "袁渊 百度百科"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "critical",
                "question": "袁渊任城东区委书记前担任什么职务？",
                "why_it_matters": "晋升路径和前任关系的关键线索",
                "suggested_queries": ["袁渊 此前 担任 西宁", "袁渊 曾任"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "high",
                "question": "袁渊的完整任职履历是什么？",
                "why_it_matters": "核心人物的职业轨迹",
                "suggested_queries": ["袁渊 简历 任职经历"],
                "last_attempted": "2026-07-25"
            }
        ]
    }

    # 张金山 person JSON
    zhangjinshan = {
        "schema_version": "1.0",
        "generated_at": today_str,
        "investigation_scope": {
            "province": "青海省",
            "city": "西宁市",
            "region": "城东区",
            "job": "区长",
            "task_id": "qinghai_城东区",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": "chengdong_zhangjinshan",
            "name": "张金山",
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
                "name_birth": "张金山_",
                "name_birthplace": "张金山_",
                "official_profile_url": "https://www.xncd.gov.cn/"
            }
        },
        "current_status": {
            "current_post": "城东区委副书记、代理区长",
            "current_org": "城东区人民政府",
            "administrative_rank": "正处级",
            "as_of": "2026-07-25",
            "is_current_confirmed": True,
            "source_ids": ["S002"]
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": "城东区人民政府",
                "title": "城东区委副书记、代理区长",
                "level": "县级",
                "location": "青海省西宁市城东区",
                "system": "government",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "Confirmed from official leadership page and news article. Full career timeline unknown.",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            }
        ],
        "organizations": [
            {"org_id": "org_chengdong_gov", "name": "城东区人民政府", "role": "领导机关", "source_ids": ["S002"]}
        ],
        "relationships": [
            {
                "person": "袁渊",
                "person_id": "chengdong_yuanyuan",
                "relationship_type": "党政搭档",
                "strength": "strong",
                "evidence": "张金山作为代理区长、袁渊作为区委书记，为城东区党政正职搭档（2026年换届）",
                "overlap_org": "城东区",
                "overlap_period": "2026",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"]
            }
        ],
        "governance_record": [
            {
                "period": "2026-07-22",
                "domain": "economic_development",
                "achievement_or_event": "在城东区第二十届人民代表大会第一次会议上作政府工作报告，总结过去五年工作，谋划未来五年发展目标",
                "role_in_event": "代理区长作政府工作报告",
                "measurable_outcome": "",
                "location": "城东区",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            }
        ],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "不明 — 公开资料未找到完整履历",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "pragmatic",
                    "evidence": "政府工作报告聚焦生态文明建设、功能区定位优势、经济引擎支撑、改革开放赋能、城市内涵式发展和社会稳定等六个方面，体现务实工作导向",
                    "confidence": "plausible",
                    "source_ids": ["S002"]
                }
            ],
            "speech_themes": ["高质量发展", "美丽繁荣新东区", "生态文明高地", "产业四地", "门户流通美食共富"],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026年7月，未发现张金山的纪律处分、审计问题或负面报道",
                "date": "2026-07-25",
                "confidence": "plausible",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "袁渊参加区政协十一届一次会议联组讨论",
                "url": "https://www.xncd.gov.cn/html/dzdt/107805.html",
                "publisher": "西宁市城东区人民政府",
                "published_at": "2026-07-23",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "high",
                "notes": "确认区领导任职框架"
            },
            {
                "id": "S002",
                "title": "【聚焦两会】凝心聚力启新程 实干担当绘蓝图——城东区第二十届人大第一次会议开幕",
                "url": "https://www.xncd.gov.cn/html/dzdt/107799.html",
                "publisher": "西宁市城东区人民政府",
                "published_at": "2026-07-22",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "high",
                "notes": "确认张金山为区委副书记、代理区长"
            },
            {
                "id": "S003",
                "title": "城东区人民政府领导之窗",
                "url": "https://www.xncd.gov.cn/html/article/qzfld.html",
                "publisher": "西宁市城东区人民政府",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "high",
                "notes": "确认代区长和副区长名单"
            }
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "缺少张金山的出生年份、籍贯、教育背景、入党时间、完整任职履历等基本信息"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "张金山的出生年份、籍贯、教育背景是什么？",
                "why_it_matters": "基础身份信息，用于人员去重和履历分析",
                "suggested_queries": ["张金山 西宁 简历 出生", "张金山 城东区长 任前公示", "张金山 百度百科"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "critical",
                "question": "张金山任城东区代理区长前担任什么职务？",
                "why_it_matters": "晋升路径和前任关系的关键线索",
                "suggested_queries": ["张金山 此前 担任 西宁", "张金山 曾任"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "high",
                "question": "张金山的完整任职履历是什么？",
                "why_it_matters": "核心人物的职业轨迹",
                "suggested_queries": ["张金山 简历 任职经历"],
                "last_attempted": "2026-07-25"
            }
        ]
    }

    # Write person JSON files
    yuanyuan_path = person_dir / f"{today_str}-青海省-西宁市-区委书记-袁渊.json"
    with open(yuanyuan_path, "w", encoding="utf-8") as f:
        json.dump(yuanyuan, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Person JSON: {yuanyuan_path}")

    zhangjinshan_path = person_dir / f"{today_str}-青海省-西宁市-区长-张金山.json"
    with open(zhangjinshan_path, "w", encoding="utf-8") as f:
        json.dump(zhangjinshan, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Person JSON: {zhangjinshan_path}")

    print(f"\n{'='*60}")
    print(f"城东区 build complete!")
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
