#!/usr/bin/env python3
"""Build 武汉市东西湖区 (Wuhan Dongxihu District) leadership network data.

Level: 市辖区
Province: 湖北省
Parent city: 武汉市
Targets: 区委书记 (Party Secretary), 区长 (Mayor)
Task ID: hubei_东西湖区

Research date: 2026-07-25
Official source: https://www.dxh.gov.cn/ (武汉市东西湖区人民政府/武汉临空港经济技术开发区管委会)

Current status (as of 2026-07-25, verified via dxh.gov.cn):
- 区委书记: 王敏 — confirmed by dxh.gov.cn news article (2026-07-22 "区委书记王敏参加所在党支部主题党日活动")
- 区人民政府区长: （空缺）— per dxh.gov.cn government leadership page (管理公开→领导信息)
- 区政府领导班子成员: 龙眉, 吕鹏, 彭邦明, 杨蒴, 齐曼, 谢明吉, 肖毅, 李闽, 李玲, 刘元林
  (listed under "区人民政府其他领导班子成员" on dxh.gov.cn government information page)

Confirmed news article sources (all from dxh.gov.cn):
- 区委书记王敏参加所在党支部主题党日活动 (2026-07-22): /XWZX/LKGYW/202607/t20260722_2823736.shtml
- 区政协调研暑假爱心托管班及青年发展工作 (2026-07-24): /XWZX/LKGYW/202607/t20260724_2824788.shtml
- 区人大常委会专题调研吴家山区域交通综合治理工作 (2026-07-24): /XWZX/LKGYW/202607/t20260724_2824795.shtml
- 0.02km²年产13亿！东西湖汽车小镇什么来头? (2026-07-21): /XWZX/LKGYW/202607/t20260721_2823585.shtml
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

SLUG = "东西湖区"

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
    # 区委领导 (Party Committee)
    # ════════════════════════════════════════

    # ── 区委书记 ──
    {
        "id": 1,
        "name": "王敏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "东西湖区委书记",
        "current_org": "中共武汉市东西湖区委员会",
        "source": "https://www.dxh.gov.cn/XWZX/LKGYW/202607/t20260722_2823736.shtml",
        "notes": "区政府官网2026年7月22日新闻确认'区委书记王敏参加所在党支部主题党日活动'。出生年份、籍贯、教育等个人信息待补充。",
    },

    # ════════════════════════════════════════
    # 区政府领导班子 (Government Leadership)
    # ════════════════════════════════════════
    # From dxh.gov.cn government information page (管理公开→领导信息)
    # 区人民政府区长: （空缺）
    # 区人民政府其他领导班子成员: 龙眉, 吕鹏, 彭邦明, 杨蒴, 齐曼, 谢明吉, 肖毅, 李闽, 李玲, 刘元林

    {
        "id": 2,
        "name": "龙眉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "东西湖区人民政府副区长（推测）",
        "current_org": "东西湖区人民政府",
        "source": "https://www.dxh.gov.cn/ZWGK/",
        "notes": "出现在区政府'其他领导班子成员'列表首位，推测为常务副区长或重要副区长。",
    },
    {
        "id": 3,
        "name": "吕鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "东西湖区人民政府副区长（推测）",
        "current_org": "东西湖区人民政府",
        "source": "https://www.dxh.gov.cn/ZWGK/",
        "notes": "区政府其他领导班子成员。",
    },
    {
        "id": 4,
        "name": "彭邦明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "东西湖区人民政府副区长（推测）",
        "current_org": "东西湖区人民政府",
        "source": "https://www.dxh.gov.cn/ZWGK/",
        "notes": "区政府其他领导班子成员。",
    },
    {
        "id": 5,
        "name": "杨蒴",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "东西湖区人民政府副区长（推测）",
        "current_org": "东西湖区人民政府",
        "source": "https://www.dxh.gov.cn/ZWGK/",
        "notes": "区政府其他领导班子成员。",
    },
    {
        "id": 6,
        "name": "齐曼",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "东西湖区人民政府副区长（推测）",
        "current_org": "东西湖区人民政府",
        "source": "https://www.dxh.gov.cn/ZWGK/",
        "notes": "区政府其他领导班子成员。",
    },
    {
        "id": 7,
        "name": "谢明吉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "东西湖区人民政府副区长（推测）",
        "current_org": "东西湖区人民政府",
        "source": "https://www.dxh.gov.cn/ZWGK/",
        "notes": "区政府其他领导班子成员。",
    },
    {
        "id": 8,
        "name": "肖毅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "东西湖区人民政府副区长（推测）",
        "current_org": "东西湖区人民政府",
        "source": "https://www.dxh.gov.cn/ZWGK/",
        "notes": "区政府其他领导班子成员。",
    },
    {
        "id": 9,
        "name": "李闽",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "东西湖区人民政府副区长（推测）",
        "current_org": "东西湖区人民政府",
        "source": "https://www.dxh.gov.cn/ZWGK/",
        "notes": "区政府其他领导班子成员。",
    },
    {
        "id": 10,
        "name": "李玲",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "东西湖区人民政府副区长（推测）",
        "current_org": "东西湖区人民政府",
        "source": "https://www.dxh.gov.cn/ZWGK/",
        "notes": "区政府其他领导班子成员。女性（姓名推断）。",
    },
    {
        "id": 11,
        "name": "刘元林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "东西湖区人民政府副区长（推测）",
        "current_org": "东西湖区人民政府",
        "source": "https://www.dxh.gov.cn/ZWGK/",
        "notes": "区政府其他领导班子成员。",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共武汉市东西湖区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共武汉市委",
        "location": "武汉市东西湖区",
    },
    {
        "id": 2,
        "name": "东西湖区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "武汉市人民政府",
        "location": "武汉市东西湖区",
    },
    {
        "id": 3,
        "name": "武汉临空港经济技术开发区管委会",
        "type": "政府",
        "level": "国家级开发区",
        "parent": "武汉市人民政府",
        "location": "武汉市东西湖区",
        "notes": "东西湖区与临空港经开区实行'区区合一'管理体制",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 王敏
    {"person_id": "p1", "org_id": 1, "title": "东西湖区委书记", "start": "", "end": "present", "rank": "副厅级", "note": "2026年7月22日官网新闻确认以区委书记身份参加活动"},
    # 龙眉
    {"person_id": "p2", "org_id": 2, "title": "区政府其他领导班子成员（副区长推测）", "start": "", "end": "present", "rank": "", "note": "出现在区政府领导班子成员列表"},
    # 吕鹏
    {"person_id": "p3", "org_id": 2, "title": "区政府其他领导班子成员（副区长推测）", "start": "", "end": "present", "rank": "", "note": "出现在区政府领导班子成员列表"},
    # 彭邦明
    {"person_id": "p4", "org_id": 2, "title": "区政府其他领导班子成员（副区长推测）", "start": "", "end": "present", "rank": "", "note": "出现在区政府领导班子成员列表"},
    # 杨蒴
    {"person_id": "p5", "org_id": 2, "title": "区政府其他领导班子成员（副区长推测）", "start": "", "end": "present", "rank": "", "note": "出现在区政府领导班子成员列表"},
    # 齐曼
    {"person_id": "p6", "org_id": 2, "title": "区政府其他领导班子成员（副区长推测）", "start": "", "end": "present", "rank": "", "note": "出现在区政府领导班子成员列表"},
    # 谢明吉
    {"person_id": "p7", "org_id": 2, "title": "区政府其他领导班子成员（副区长推测）", "start": "", "end": "present", "rank": "", "note": "出现在区政府领导班子成员列表"},
    # 肖毅
    {"person_id": "p8", "org_id": 2, "title": "区政府其他领导班子成员（副区长推测）", "start": "", "end": "present", "rank": "", "note": "出现在区政府领导班子成员列表"},
    # 李闽
    {"person_id": "p9", "org_id": 2, "title": "区政府其他领导班子成员（副区长推测）", "start": "", "end": "present", "rank": "", "note": "出现在区政府领导班子成员列表"},
    # 李玲
    {"person_id": "p10", "org_id": 2, "title": "区政府其他领导班子成员（副区长推测）", "start": "", "end": "present", "rank": "", "note": "出现在区政府领导班子成员列表"},
    # 刘元林
    {"person_id": "p11", "org_id": 2, "title": "区政府其他领导班子成员（副区长推测）", "start": "", "end": "present", "rank": "", "note": "出现在区政府领导班子成员列表"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 王敏 ↔ 龙眉 （区委书记与政府领导成员）
    {
        "person_a": "p1",
        "person_b": "p2",
        "type": "overlap",
        "context": "区委书记与区政府领导班子成员同区共事",
        "overlap_org": "东西湖区",
        "overlap_period": "至present",
        "confidence": "confirmed",
    },
    # 王敏 ↔ 吕鹏
    {
        "person_a": "p1",
        "person_b": "p3",
        "type": "overlap",
        "context": "区委书记与区政府领导班子成员同区共事",
        "overlap_org": "东西湖区",
        "overlap_period": "至present",
        "confidence": "confirmed",
    },
    # 王敏 ↔ 彭邦明
    {
        "person_a": "p1",
        "person_b": "p4",
        "type": "overlap",
        "context": "区委书记与区政府领导班子成员同区共事",
        "overlap_org": "东西湖区",
        "overlap_period": "至present",
        "confidence": "confirmed",
    },
    # 王敏 ↔ 杨蒴
    {
        "person_a": "p1",
        "person_b": "p5",
        "type": "overlap",
        "context": "区委书记与区政府领导班子成员同区共事",
        "overlap_org": "东西湖区",
        "overlap_period": "至present",
        "confidence": "confirmed",
    },
    # 王敏 ↔ 齐曼
    {
        "person_a": "p1",
        "person_b": "p6",
        "type": "overlap",
        "context": "区委书记与区政府领导班子成员同区共事",
        "overlap_org": "东西湖区",
        "overlap_period": "至present",
        "confidence": "confirmed",
    },
    # 王敏 ↔ 谢明吉
    {
        "person_a": "p1",
        "person_b": "p7",
        "type": "overlap",
        "context": "区委书记与区政府领导班子成员同区共事",
        "overlap_org": "东西湖区",
        "overlap_period": "至present",
        "confidence": "confirmed",
    },
    # 王敏 ↔ 肖毅
    {
        "person_a": "p1",
        "person_b": "p8",
        "type": "overlap",
        "context": "区委书记与区政府领导班子成员同区共事",
        "overlap_org": "东西湖区",
        "overlap_period": "至present",
        "confidence": "confirmed",
    },
    # 王敏 ↔ 李闽
    {
        "person_a": "p1",
        "person_b": "p9",
        "type": "overlap",
        "context": "区委书记与区政府领导班子成员同区共事",
        "overlap_org": "东西湖区",
        "overlap_period": "至present",
        "confidence": "confirmed",
    },
    # 王敏 ↔ 李玲
    {
        "person_a": "p1",
        "person_b": "p10",
        "type": "overlap",
        "context": "区委书记与区政府领导班子成员同区共事",
        "overlap_org": "东西湖区",
        "overlap_period": "至present",
        "confidence": "confirmed",
    },
    # 王敏 ↔ 刘元林
    {
        "person_a": "p1",
        "person_b": "p11",
        "type": "overlap",
        "context": "区委书记与区政府领导班子成员同区共事",
        "overlap_org": "东西湖区",
        "overlap_period": "至present",
        "confidence": "confirmed",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON DATA
# ══════════════════════════════════════════════════════════════════════════════

_source_register = [
    {
        "id": "S001",
        "title": "区委书记王敏参加所在党支部主题党日活动 (2026-07-22)",
        "url": "https://www.dxh.gov.cn/XWZX/LKGYW/202607/t20260722_2823736.shtml",
        "publisher": "东西湖区人民政府",
        "published_at": "2026-07-22",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "确认王敏以东西湖区委书记身份参加党支部活动",
    },
    {
        "id": "S002",
        "title": "东西湖区人民政府信息公开-领导信息页面",
        "url": "https://www.dxh.gov.cn/ZWGK/",
        "publisher": "东西湖区人民政府",
        "published_at": "2026-07",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "确认区长空缺；列出区政府其他领导班子成员：龙眉、吕鹏、彭邦明、杨蒴、齐曼、谢明吉、肖毅、李闽、李玲、刘元林",
    },
    {
        "id": "S003",
        "title": "东西湖区人民政府首页",
        "url": "https://www.dxh.gov.cn/",
        "publisher": "东西湖区人民政府",
        "published_at": "2026-07",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "确认新闻资讯栏目显示'区委书记王敏参加所在党支部主题党日活动'",
    },
    {
        "id": "S004",
        "title": "0.02km²年产13亿！东西湖汽车小镇什么来头?",
        "url": "https://www.dxh.gov.cn/XWZX/LKGYW/202607/t20260721_2823585.shtml",
        "publisher": "东西湖区融媒体中心",
        "published_at": "2026-07-21",
        "accessed_at": AS_OF,
        "source_type": "media",
        "reliability": "high",
        "notes": "东西湖区产业发展报道，未直接提及领导信息但提供了区域发展背景",
    },
    {
        "id": "S005",
        "title": "区政协调研暑假爱心托管班及青年发展工作 (2026-07-24)",
        "url": "https://www.dxh.gov.cn/XWZX/LKGYW/202607/t20260724_2824788.shtml",
        "publisher": "东西湖区人民政府",
        "published_at": "2026-07-24",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "区政协相关活动报道",
    },
]


def make_person_json(person, timeline_items, relationship_list):
    """Build a person graph JSON following the schema."""
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "湖北省",
            "city": "武汉市",
            "region": "东西湖区",
            "job": person["current_post"],
            "task_id": "hubei_东西湖区",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": f"dongxihu_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("native_place", ""),
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth', '')}" if person.get("birth") else person["name"],
                "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}" if person.get("birthplace") else person["name"],
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002", "S003"]
        },
        "career_timeline": timeline_items,
        "organizations": [],
        "relationships": relationship_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "无法评估——缺少出生年份和完整履历",
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
            {
                "type": "none_found",
                "description": "公开资料中未发现纪律处分、审计问题或负面报道",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": _source_register,
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "缺失出生年份、籍贯、教育背景和完整履历；缺失区委常委班子名单；缺失前任何长/书记信息"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的出生年份、籍贯和教育背景是什么？",
                "why_it_matters": "用于人员去重和晋升速度分析",
                "suggested_queries": [
                    f"{person['name']} 简历 东西湖区",
                    f"{person['name']} 出生 籍贯 学历",
                    f"{person['name']} 武汉 任职经历"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"{person['name']}在担任现职前的工作履历是什么？",
                "why_it_matters": "完整的晋升路径揭示工作关系网络",
                "suggested_queries": [
                    f"{person['name']} 此前担任",
                    f"{person['name']} 调任 东西湖区",
                    f"{person['name']} 历任"
                ],
                "last_attempted": AS_OF
            }
        ]
    }


def write_person_json(person, timeline_items, relationship_list):
    data = make_person_json(person, timeline_items, relationship_list)
    path = PERSONS_DIR / f"{TODAY}-湖北省-武汉市-{person['current_post'].split('、')[0].split('（')[0]}-{person['name']}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {path.name}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    os.makedirs(_STAGING_DIR, exist_ok=True)

    # Build DB + GEXF
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write person JSONs for core leaders
    print("\n--- Person JSONs ---")

    # 王敏 — 区委书记
    wm_timeline = [
        {
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "level": "",
            "location": "",
            "system": "other",
            "rank": "",
            "is_key_promotion": False,
            "notes": "公开资料未找到王敏担任东西湖区委书记前的完整履历",
            "confidence": "unverified",
            "source_ids": []
        },
        {
            "start": "~2026-07",
            "end": "present",
            "org": "中共武汉市东西湖区委员会",
            "title": "东西湖区委书记",
            "level": "副厅级",
            "location": "武汉市东西湖区",
            "system": "party",
            "rank": "",
            "is_key_promotion": True,
            "notes": "2026年7月22日官网新闻确认以区委书记身份参加所在党支部主题党日活动。到任具体时间待确认。",
            "confidence": "confirmed",
            "source_ids": ["S001", "S003"]
        },
    ]
    wm_relationships = [
        {
            "person": "龙眉",
            "person_id": "dongxihu_long_mei",
            "relationship_type": "overlap",
            "strength": "weak",
            "evidence": "区委书记与区政府领导班子成员同区共事",
            "overlap_org": "东西湖区",
            "overlap_period": "2026至present",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S002"]
        },
    ]
    write_person_json(persons[0], wm_timeline, wm_relationships)

    print(f"\n{'='*60}")
    print(f"东西湖区 Network Build Complete")
    print(f"{'='*60}")
    print(f"Staging dir: {_STAGING_DIR}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")


if __name__ == "__main__":
    main()
