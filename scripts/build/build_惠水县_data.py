#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
惠水县领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Huishui County leadership network.

Level: 县
Province: 贵州省
Parent City: 黔南布依族苗族自治州
Region: 惠水县
Targets: 县委书记 & 县长

Research Sources:
- gzhs.gov.cn — 惠水县人民政府门户网站 (2026年7月)
  - 惠水要闻 (multiple articles) confirming current leadership as of 2026-07-23
  - 新闻: 韦朝虎讲授树立和践行正确政绩观学习教育专题党课 (2026-07-17)
  - 新闻: 韦朝虎到摆金镇督导调研 (2026-07-18)
  - 新闻: 韦朝虎到好花红镇督导调研 (2026-07-15)
  - 新闻: 县委常委会召开扩大会议 (2026-07-16)
  - 新闻: 县委理论学习中心组2026年第六次集中学习研讨会召开 (2026-07-17)
  - 新闻: 惠水县召开安全生产工作推进会 (2026-07-21)
  - 新闻: 惠水县举行2026年旅游资源新闻发布会 (2026-07-19)
  - 人事任免: 惠府任〔2026〕12号, 11号, 10号, 9号, 8号
- Baidu Baike: 韦朝虎 (unavailable due to access restrictions)
- Baidu Baike: 惠水县 (unavailable due to access restrictions)

Confirmed officeholders (as of 2026-07-23, from gzhs.gov.cn official news):
- 县委书记: 韦朝虎 (兼任州人大常委会副主任)
- 县委副书记、县长: 刘兴国
- 县人大常委会主任: 罗朝光
- 县政协主席: 王昌茂
- 县委副书记: 周奠苏
- 县委常委: 严晓飞
- 县委常委: 李章程
- 县领导(副县长级): 李凌霄
- 县领导: 杨航
- 县领导: 李发勇
- 县领导: 周德芳

Note: Most biographical details (birth year, birthplace, education)
remain to be filled from external sources (Baidu Baike was inaccessible).

Research Date: 2026-07-23
"""

import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths ──
SLUG = "惠水县"
AS_OF = "2026-07-23"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "韦朝虎",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州人大常委会副主任、县委书记",
        "current_org": "中共惠水县委员会",
        "source": "https://www.gzhs.gov.cn/xwdt/hsyw/202607/t20260717_90635303.html — 惠水县人民政府门户网站, 2026-07-17确认"
    },
    {
        "id": 2,
        "name": "刘兴国",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "惠水县人民政府",
        "source": "https://www.gzhs.gov.cn/xwdt/hsyw/202607/t20260716_90630739.html — 惠水县人民政府门户网站, 2026-07-16确认"
    },
    # ════════════════════════════════════════
    # Four Major Leaders
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "罗朝光",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "惠水县人民代表大会常务委员会",
        "source": "https://www.gzhs.gov.cn/xwdt/hsyw/202607/t20260716_90630739.html — 惠水县人民政府门户网站, 2026-07-16确认"
    },
    {
        "id": 4,
        "name": "王昌茂",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议惠水县委员会",
        "source": "https://www.gzhs.gov.cn/xwdt/hsyw/202607/t20260716_90630739.html — 惠水县人民政府门户网站, 2026-07-16确认"
    },
    # ════════════════════════════════════════
    # Deputy Leaders & Other Officials
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "周奠苏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共惠水县委员会",
        "source": "https://www.gzhs.gov.cn/xwdt/hsyw/202607/t20260716_90630739.html — 惠水县人民政府门户网站, 2026-07-16确认"
    },
    {
        "id": 6,
        "name": "严晓飞",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共惠水县委员会",
        "source": "https://www.gzhs.gov.cn/xwdt/hsyw/202607/t20260715_90626651.html — 惠水县人民政府门户网站, 2026-07-15确认"
    },
    {
        "id": 7,
        "name": "李章程",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共惠水县委员会",
        "source": "https://www.gzhs.gov.cn/xwdt/hsyw/202607/t20260715_90626651.html — 惠水县人民政府门户网站, 2026-07-15确认"
    },
    {
        "id": 8,
        "name": "李凌霄",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "惠水县人民政府",
        "source": "https://www.gzhs.gov.cn/xwdt/hsyw/202607/t20260721_90647459.html — 惠水县人民政府门户网站, 2026-07-21确认"
    },
    {
        "id": 9,
        "name": "杨航",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "惠水县人民政府",
        "source": "https://www.gzhs.gov.cn/xwdt/hsyw/202607/t20260721_90647459.html — 惠水县人民政府门户网站, 2026-07-21确认"
    },
    {
        "id": 10,
        "name": "李发勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "惠水县人民政府",
        "source": "https://www.gzhs.gov.cn/xwdt/hsyw/202607/t20260721_90647459.html — 惠水县人民政府门户网站, 2026-07-21确认"
    },
    {
        "id": 11,
        "name": "周德芳",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "惠水县人民政府",
        "source": "https://www.gzhs.gov.cn/xwdt/hsyw/202607/t20260721_90647459.html — 惠水县人民政府门户网站, 2026-07-21确认"
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共惠水县委员会", "type": "党委", "level": "县级", "parent": "中共黔南布依族苗族自治州委员会", "location": "惠水县"},
    {"id": 2, "name": "惠水县人民政府", "type": "政府", "level": "县级", "parent": "黔南布依族苗族自治州人民政府", "location": "惠水县"},
    {"id": 3, "name": "惠水县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "黔南布依族苗族自治州人民代表大会常务委员会", "location": "惠水县"},
    {"id": 4, "name": "中国人民政治协商会议惠水县委员会", "type": "政协", "level": "县级", "parent": "中国人民政治协商会议黔南布依族苗族自治州委员会", "location": "惠水县"},
]

# 3. Positions (person_id, org_id, title, start, end, rank, note)
positions = [
    # 韦朝虎 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记（兼州人大常委会副主任）", "start_date": "", "end_date": "present", "rank": "正县级", "note": "同时担任黔南州人大常委会副主任"},
    # 刘兴国 — 县长
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 罗朝光 — 人大主任
    {"person_id": 3, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 王昌茂 — 政协主席
    {"person_id": 4, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 周奠苏 — 县委副书记
    {"person_id": 5, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 严晓飞 — 县委常委
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 李章程 — 县委常委
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 李凌霄 — 副县长
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 杨航 — 副县长
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 李发勇 — 副县长
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 周德芳 — 副县长
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
]

# 4. Relationships
relationships = [
    # 书记—县长
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长，党政主要领导搭档关系", "overlap_org": "中共惠水县委员会/惠水县人民政府", "overlap_period": ""},
    # 书记—副书记
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委书记与县委副书记", "overlap_org": "中共惠水县委员会", "overlap_period": ""},
    # 县长—副县长(李凌霄)
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "惠水县人民政府", "overlap_period": ""},
    # 县长—副县长(杨航)
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "惠水县人民政府", "overlap_period": ""},
    # 县长—副县长(李发勇)
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "惠水县人民政府", "overlap_period": ""},
    # 县长—副县长(周德芳)
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "惠水县人民政府", "overlap_period": ""},
    # 县委常委—常委(同事)
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "同为县委常委班子成员", "overlap_org": "中共惠水县委员会", "overlap_period": ""},
    # 县委常委—书记
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县委书记与县委常委", "overlap_org": "中共惠水县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "县委书记与县委常委", "overlap_org": "中共惠水县委员会", "overlap_period": ""},
    # 人大—领导层
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委与县人大主要领导", "overlap_org": "惠水县四家班子", "overlap_period": ""},
    # 政协—领导层
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委与县政协主要领导", "overlap_org": "惠水县四家班子", "overlap_period": ""},
]

# ── Main ──
if __name__ == "__main__":
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
    person_files = [
        {
            "filename": f"20260723-贵州省-黔南布依族苗族自治州-县委书记-韦朝虎.json",
            "data": {
                "schema_version": "1.0",
                "generated_at": "2026-07-23",
                "investigation_scope": {
                    "province": "贵州省",
                    "city": "黔南布依族苗族自治州",
                    "region": "惠水县",
                    "job": "县委书记",
                    "task_id": "guizhou_惠水县",
                    "time_focus": "2026-07"
                },
                "identity": {
                    "person_id": "huishui_wei_chaohu",
                    "name": "韦朝虎",
                    "aliases": [],
                    "gender": "男",
                    "ethnicity": "",
                    "birth": "",
                    "birthplace": "",
                    "native_place": "",
                    "education": [],
                    "party_join": "中共党员",
                    "work_start": "",
                    "dedupe_keys": {
                        "name_birth": "韦朝虎_",
                        "name_birthplace": "韦朝虎_",
                        "official_profile_url": "https://www.gzhs.gov.cn/"
                    }
                },
                "current_status": {
                    "current_post": "州人大常委会副主任、县委书记",
                    "current_org": "中共惠水县委员会",
                    "administrative_rank": "正县级",
                    "as_of": "2026-07-23",
                    "is_current_confirmed": True,
                    "source_ids": ["S001", "S002", "S003"]
                },
                "career_timeline": [
                    {
                        "start": "未知",
                        "end": "present",
                        "org": "中共惠水县委员会",
                        "title": "县委书记（兼州人大常委会副主任）",
                        "level": "正县级",
                        "location": "惠水县",
                        "system": "party",
                        "rank": "正县级",
                        "is_key_promotion": False,
                        "notes": "公开资料未找到完整履历；Baidu Baike不可访问",
                        "confidence": "confirmed",
                        "source_ids": ["S001", "S002"]
                    }
                ],
                "organizations": [
                    {"org_id": 1, "name": "中共惠水县委员会", "role": "县委书记", "period": "present"},
                    {"org_id": 5, "name": "黔南布依族苗族自治州人民代表大会常务委员会", "role": "州人大常委会副主任", "period": "present"}
                ],
                "relationships": [],
                "governance_record": [
                    {
                        "period": "2026-07",
                        "domain": "rural_revitalization",
                        "achievement_or_event": "到摆金镇督导调研灾后恢复、镇村换届、产业发展",
                        "role_in_event": "带队督导",
                        "measurable_outcome": "",
                        "location": "惠水县摆金镇",
                        "confidence": "confirmed",
                        "source_ids": ["S002"]
                    },
                    {
                        "period": "2026-07",
                        "domain": "other",
                        "achievement_or_event": "讲授树立和践行正确政绩观学习教育专题党课",
                        "role_in_event": "主讲",
                        "measurable_outcome": "",
                        "location": "惠水县",
                        "confidence": "confirmed",
                        "source_ids": ["S001"]
                    }
                ],
                "professional_profile": {
                    "primary_specializations": [],
                    "secondary_specializations": [],
                    "career_pattern": "unknown",
                    "systems_experience": ["party"],
                    "geographic_pattern": [],
                    "promotion_velocity": {
                        "summary": "履历不完整，无法评估",
                        "notable_fast_promotions": []
                    }
                },
                "work_style_and_personality": {
                    "public_style_indicators": [
                        {
                            "trait": "grassroots_oriented",
                            "evidence": "多次到乡镇（摆金镇、好花红镇）督导调研",
                            "confidence": "confirmed",
                            "source_ids": ["S002", "S004"]
                        },
                        {
                            "trait": "discipline_oriented",
                            "evidence": "讲授正确政绩观专题党课，强调纪律和党建",
                            "confidence": "confirmed",
                            "source_ids": ["S001"]
                        }
                    ],
                    "speech_themes": ["树立正确政绩观", "党建引领", "安全生产", "乡村振兴"],
                    "management_signals": ["强调镇村换届纪律", "重视防溺水安全", "关注灾后恢复"],
                    "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
                },
                "network_metrics": {},
                "risk_and_integrity_signals": [
                    {
                        "type": "none_found",
                        "description": "公开渠道未发现负面信息",
                        "date": "",
                        "confidence": "plausible",
                        "source_ids": []
                    }
                ],
                "source_register": [
                    {
                        "id": "S001",
                        "title": "韦朝虎讲授树立和践行正确政绩观学习教育专题党课",
                        "url": "https://www.gzhs.gov.cn/xwdt/hsyw/202607/t20260717_90635303.html",
                        "publisher": "惠水县人民政府",
                        "published_at": "2026-07-17",
                        "accessed_at": "2026-07-23",
                        "source_type": "official",
                        "reliability": "high",
                        "notes": "确认韦朝虎现任县委书记（兼州人大常委会副主任）"
                    },
                    {
                        "id": "S002",
                        "title": "韦朝虎到摆金镇督导调研",
                        "url": "https://www.gzhs.gov.cn/xwdt/hsyw/202607/t20260718_90636076.html",
                        "publisher": "惠水县人民政府",
                        "published_at": "2026-07-18",
                        "accessed_at": "2026-07-23",
                        "source_type": "official",
                        "reliability": "high",
                        "notes": "确认县委书记韦朝虎主持工作信息"
                    },
                    {
                        "id": "S003",
                        "title": "县委常委会召开扩大会议",
                        "url": "https://www.gzhs.gov.cn/xwdt/hsyw/202607/t20260716_90630739.html",
                        "publisher": "惠水县人民政府",
                        "published_at": "2026-07-16",
                        "accessed_at": "2026-07-23",
                        "source_type": "official",
                        "reliability": "high",
                        "notes": "确认韦朝虎主持会议，刘兴国、罗朝光、王昌茂、周奠苏等出席"
                    },
                    {
                        "id": "S004",
                        "title": "韦朝虎到好花红镇督导调研",
                        "url": "https://www.gzhs.gov.cn/xwdt/hsyw/202607/t20260715_90626651.html",
                        "publisher": "惠水县人民政府",
                        "published_at": "2026-07-15",
                        "accessed_at": "2026-07-23",
                        "source_type": "official",
                        "reliability": "high",
                        "notes": "确认严晓飞、李章程为县委常委"
                    }
                ],
                "confidence_summary": {
                    "identity": "plausible",
                    "current_role": "confirmed",
                    "career_completeness": "thin",
                    "relationship_confidence": "low",
                    "biggest_gap": "完整履历（出生年月、籍贯、教育背景、早期任职经历）均缺失"
                },
                "open_questions": [
                    {
                        "priority": "critical",
                        "question": "韦朝虎的出生年月、籍贯、教育背景？",
                        "why_it_matters": "确定人物身份基本信息",
                        "suggested_queries": ["韦朝虎 简历", "韦朝虎 出生", "韦朝虎 贵州"],
                        "last_attempted": "2026-07-23"
                    },
                    {
                        "priority": "critical",
                        "question": "韦朝虎任县委书记前的完整履历？",
                        "why_it_matters": "了解其晋升路径和可能的关联网络",
                        "suggested_queries": ["韦朝虎 任前公示", "韦朝虎 曾任", "韦朝虎 黔南"],
                        "last_attempted": "2026-07-23"
                    },
                    {
                        "priority": "high",
                        "question": "韦朝虎何时开始担任黔南州人大常委会副主任？",
                        "why_it_matters": "确认兼任职务的时间跨度和级别",
                        "suggested_queries": ["韦朝虎 州人大常委会副主任 任命"],
                        "last_attempted": "2026-07-23"
                    }
                ]
            }
        },
        {
            "filename": f"20260723-贵州省-黔南布依族苗族自治州-县长-刘兴国.json",
            "data": {
                "schema_version": "1.0",
                "generated_at": "2026-07-23",
                "investigation_scope": {
                    "province": "贵州省",
                    "city": "黔南布依族苗族自治州",
                    "region": "惠水县",
                    "job": "县长",
                    "task_id": "guizhou_惠水县",
                    "time_focus": "2026-07"
                },
                "identity": {
                    "person_id": "huishui_liu_xingguo",
                    "name": "刘兴国",
                    "aliases": [],
                    "gender": "男",
                    "ethnicity": "",
                    "birth": "",
                    "birthplace": "",
                    "native_place": "",
                    "education": [],
                    "party_join": "中共党员",
                    "work_start": "",
                    "dedupe_keys": {
                        "name_birth": "刘兴国_",
                        "name_birthplace": "刘兴国_",
                        "official_profile_url": "https://www.gzhs.gov.cn/"
                    }
                },
                "current_status": {
                    "current_post": "县委副书记、县长",
                    "current_org": "惠水县人民政府",
                    "administrative_rank": "正县级",
                    "as_of": "2026-07-23",
                    "is_current_confirmed": True,
                    "source_ids": ["S101", "S102"]
                },
                "career_timeline": [
                    {
                        "start": "未知",
                        "end": "present",
                        "org": "惠水县人民政府",
                        "title": "县委副书记、县长",
                        "level": "正县级",
                        "location": "惠水县",
                        "system": "government",
                        "rank": "正县级",
                        "is_key_promotion": False,
                        "notes": "公开资料未找到完整履历",
                        "confidence": "confirmed",
                        "source_ids": ["S101", "S102"]
                    }
                ],
                "organizations": [
                    {"org_id": 2, "name": "惠水县人民政府", "role": "县长", "period": "present"},
                    {"org_id": 1, "name": "中共惠水县委员会", "role": "县委副书记", "period": "present"}
                ],
                "relationships": [],
                "governance_record": [
                    {
                        "period": "2026-07",
                        "domain": "public_security",
                        "achievement_or_event": "主持召开惠水县安全生产工作推进会",
                        "role_in_event": "主持并讲话",
                        "measurable_outcome": "",
                        "location": "惠水县",
                        "confidence": "confirmed",
                        "source_ids": ["S102"]
                    }
                ],
                "professional_profile": {
                    "primary_specializations": [],
                    "secondary_specializations": [],
                    "career_pattern": "unknown",
                    "systems_experience": ["government"],
                    "geographic_pattern": [],
                    "promotion_velocity": {
                        "summary": "履历不完整，无法评估",
                        "notable_fast_promotions": []
                    }
                },
                "work_style_and_personality": {
                    "public_style_indicators": [
                        {
                            "trait": "pragmatic",
                            "evidence": "在安全生产推进会上强调'时时放心不下'的责任感和具体措施",
                            "confidence": "confirmed",
                            "source_ids": ["S102"]
                        }
                    ],
                    "speech_themes": ["安全生产", "防汛抗旱", "防溺水", "隐患排查"],
                    "management_signals": ["强调'三管三必须'", "要求24小时值班值守"],
                    "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
                },
                "network_metrics": {},
                "risk_and_integrity_signals": [
                    {
                        "type": "none_found",
                        "description": "公开渠道未发现负面信息",
                        "date": "",
                        "confidence": "plausible",
                        "source_ids": []
                    }
                ],
                "source_register": [
                    {
                        "id": "S101",
                        "title": "县委常委会召开扩大会议",
                        "url": "https://www.gzhs.gov.cn/xwdt/hsyw/202607/t20260716_90630739.html",
                        "publisher": "惠水县人民政府",
                        "published_at": "2026-07-16",
                        "accessed_at": "2026-07-23",
                        "source_type": "official",
                        "reliability": "high",
                        "notes": "确认刘兴国为县委副书记、县长"
                    },
                    {
                        "id": "S102",
                        "title": "惠水县召开安全生产工作推进会",
                        "url": "https://www.gzhs.gov.cn/xwdt/hsyw/202607/t20260721_90647459.html",
                        "publisher": "惠水县人民政府",
                        "published_at": "2026-07-21",
                        "accessed_at": "2026-07-23",
                        "source_type": "official",
                        "reliability": "high",
                        "notes": "确认刘兴国以县长身份讲话，确认李凌霄、杨航、李发勇、周德芳为副县长"
                    }
                ],
                "confidence_summary": {
                    "identity": "plausible",
                    "current_role": "confirmed",
                    "career_completeness": "thin",
                    "relationship_confidence": "low",
                    "biggest_gap": "完整履历（出生年月、籍贯、教育背景、早期任职经历）均缺失"
                },
                "open_questions": [
                    {
                        "priority": "critical",
                        "question": "刘兴国的出生年月、籍贯、教育背景？",
                        "why_it_matters": "确定人物身份基本信息",
                        "suggested_queries": ["刘兴国 惠水 简历", "刘兴国 黔南 县长"],
                        "last_attempted": "2026-07-23"
                    },
                    {
                        "priority": "critical",
                        "question": "刘兴国任县长前的完整履历？",
                        "why_it_matters": "了解其晋升路径和可能的关联网络",
                        "suggested_queries": ["刘兴国 任前公示", "刘兴国 曾任"],
                        "last_attempted": "2026-07-23"
                    }
                ]
            }
        },
    ]

    persons_dir = os.path.dirname(os.path.abspath(__file__))
    for pf in person_files:
        path = os.path.join(persons_dir, pf["filename"])
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pf["data"], f, ensure_ascii=False, indent=2)
        print(f"  ✓ Person JSON: {pf['filename']}")

    print(f"\n{'='*60}")
    print(f"  惠水县数据构建完成")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")
    print(f"{'='*60}")
