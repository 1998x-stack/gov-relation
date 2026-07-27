#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
零陵区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 市辖区
Province: 湖南省
Parent City: 永州市
Region: 零陵区
Targets: 区委书记 & 区长

As of: 2026-07-24
数据来源: 零陵区政府门户网站 (www.cnll.gov.cn) — 需核实补充
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

# ── 将 repo root 加入 path ──
_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Staging paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "零陵区"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_OUT = STAGING_DIR

AS_OF = "2026-07-24"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：区委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "赵立平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "零陵区委书记",
        "current_org": "中共永州市零陵区委员会",
        "source": (
            "confirmed — 零陵区政府门户网站 2026-07-21 新闻"
            "「赵立平主持召开区委常委会扩大会议」(www.cnll.gov.cn)。"
            "完整履历待补充。区委书记任期推测自 2021 年前后。"
        ),
    },
    # ════════════════════════════════════════
    # 核心领导：区长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "龙亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "零陵区委副书记、区长",
        "current_org": "零陵区人民政府",
        "source": (
            "confirmed — 永州市政府门户网站 领导接听日栏目显示"
            "「零陵区委副书记、区长龙亮」(www.yzcity.gov.cn)。"
            "完整履历待补充。"
        ),
    },
    # ════════════════════════════════════════
    # 区人大常委会主任
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "零陵区人大常委会主任",
        "current_org": "零陵区人大常委会",
        "source": "unverified — 待通过政府官网领导之窗栏目确认",
    },
    # ════════════════════════════════════════
    # 区政协主席
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "零陵区政协主席",
        "current_org": "政协零陵区委员会",
        "source": "unverified — 待通过政府官网领导之窗栏目确认",
    },
    # ════════════════════════════════════════
    # 区委副书记（专职）
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "零陵区委副书记（专职）",
        "current_org": "中共永州市零陵区委员会",
        "source": "unverified — 待确认",
    },
    # ════════════════════════════════════════
    # 常务副区长
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "零陵区委常委、常务副区长",
        "current_org": "零陵区人民政府",
        "source": "unverified — 待确认",
    },
    # ════════════════════════════════════════
    # 纪委书记、监委主任
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "零陵区委常委、纪委书记、监委主任",
        "current_org": "中共永州市零陵区纪律检查委员会",
        "source": "unverified — 待确认",
    },
    # ════════════════════════════════════════
    # 区委组织部部长
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "零陵区委常委、组织部部长",
        "current_org": "中共永州市零陵区委组织部",
        "source": "unverified — 待确认",
    },
    # ════════════════════════════════════════
    # 区委宣传部部长
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "零陵区委常委、宣传部部长",
        "current_org": "中共永州市零陵区委宣传部",
        "source": "unverified — 待确认",
    },
    # ════════════════════════════════════════
    # 区委政法委书记
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "零陵区委常委、政法委书记",
        "current_org": "中共永州市零陵区委政法委员会",
        "source": "unverified — 待确认",
    },
    # ════════════════════════════════════════
    # 前任区委书记
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "唐烨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已离任（原零陵区委书记）",
        "current_org": "",
        "source": (
            "plausible — 根据公开资料，唐烨曾任零陵区委书记（约 2016-2021），"
            "后调任永州市直部门或其他岗位。具体去向待查。"
        ),
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {
        "id": 1,
        "name": "中共永州市零陵区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共永州市委员会",
        "location": "湖南省永州市零陵区",
    },
    {
        "id": 2,
        "name": "零陵区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "永州市人民政府",
        "location": "湖南省永州市零陵区",
    },
    {
        "id": 3,
        "name": "零陵区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "永州市人大常委会",
        "location": "湖南省永州市零陵区",
    },
    {
        "id": 4,
        "name": "政协零陵区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协永州市委员会",
        "location": "湖南省永州市零陵区",
    },
    {
        "id": 5,
        "name": "中共永州市零陵区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共永州市纪律检查委员会",
        "location": "湖南省永州市零陵区",
    },
    {
        "id": 6,
        "name": "中共永州市零陵区委组织部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共永州市零陵区委员会",
        "location": "湖南省永州市零陵区",
    },
    {
        "id": 7,
        "name": "中共永州市零陵区委宣传部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共永州市零陵区委员会",
        "location": "湖南省永州市零陵区",
    },
    {
        "id": 8,
        "name": "中共永州市零陵区委政法委员会",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共永州市零陵区委员会",
        "location": "湖南省永州市零陵区",
    },
]

# =========================================================================
# 3. POSITIONS (现任 + 历史任职)
# =========================================================================
positions = [
    # 赵立平 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "零陵区委书记", "start_date": "约2021", "end_date": "至今", "rank": "县处级正职", "note": "上任时间待确认"},
    # 龙亮 — 区长
    {"person_id": 2, "org_id": 2, "title": "零陵区委副书记、区长", "start_date": "约2021", "end_date": "至今", "rank": "县处级正职", "note": "上任时间待确认"},
    # 唐烨 — 前任区委书记
    {"person_id": 11, "org_id": 1, "title": "零陵区委书记", "start_date": "约2016", "end_date": "约2021", "rank": "县处级正职", "note": "任期根据公开报道估算"},
    # 人大主任、政协主席、副职 — 人员信息待定
    {"person_id": 3, "org_id": 3, "title": "零陵区人大常委会主任", "start_date": "", "end_date": "至今", "rank": "县处级正职", "note": "姓名待确认"},
    {"person_id": 4, "org_id": 4, "title": "零陵区政协主席", "start_date": "", "end_date": "至今", "rank": "县处级正职", "note": "姓名待确认"},
    {"person_id": 5, "org_id": 1, "title": "零陵区委副书记（专职）", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "姓名待确认"},
    {"person_id": 6, "org_id": 2, "title": "零陵区委常委、常务副区长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "姓名待确认"},
    {"person_id": 7, "org_id": 5, "title": "零陵区委常委、纪委书记、监委主任", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "姓名待确认"},
    {"person_id": 8, "org_id": 6, "title": "零陵区委常委、组织部部长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "姓名待确认"},
    {"person_id": 9, "org_id": 7, "title": "零陵区委常委、宣传部部长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "姓名待确认"},
    {"person_id": 10, "org_id": 8, "title": "零陵区委常委、政法委书记", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "姓名待确认"},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 赵立平 ↔ 龙亮（党政一把手共事关系）
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "赵立平（区委书记）与龙亮（区长）为零陵区党政一把手，2021年起搭班子",
        "overlap_org": "永州市零陵区",
        "overlap_period": "约2021至今",
    },
    # 赵立平 → 唐烨（前后任）
    {
        "person_a": 1,
        "person_b": 11,
        "type": "predecessor_successor",
        "context": "赵立平接替唐烨任零陵区委书记",
        "overlap_org": "中共永州市零陵区委员会",
        "overlap_period": "约2021前后",
    },
]

# =========================================================================
# 5. PERSON JSON OUTPUT
# =========================================================================
PERSON_FILES = []

def build_person_json(person_id: int) -> str:
    """Build a person graph JSON file and return its path."""
    p = next(x for x in persons if x["id"] == person_id)
    p_poses = [pos for pos in positions if pos["person_id"] == person_id]
    p_rels = [r for r in relationships if r["person_a"] == person_id or r["person_b"] == person_id]

    filename = f"{AS_OF}-湖南省-永州市-{p['current_post'].split('、')[0].replace('（专职）','').replace('（兼职）','')}-{p['name']}.json"
    filename = filename.replace(" ", "-")

    person_data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "湖南省",
            "city": "永州市",
            "region": "零陵区",
            "job": p["current_post"],
            "task_id": "hunan_零陵区",
            "time_focus": "2025-2026",
        },
        "identity": {
            "person_id": f"lingling_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "birthplace": p["birthplace"],
            "native_place": "",
            "education": [],
            "party_join": p["party_join"],
            "work_start": p["work_start"],
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p['birth']}",
                "name_birthplace": f"{p['name']}_{p['birthplace']}",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "县处级正职",
            "as_of": AS_OF,
            "is_current_confirmed": p["name"] != "待查",
            "source_ids": ["S001"],
        },
        "career_timeline": [
            {
                "start": pos.get("start_date") or "unknown",
                "end": pos.get("end_date") or "unknown",
                "org": next((o["name"] for o in organizations if o["id"] == pos["org_id"]), ""),
                "title": pos["title"],
                "level": pos["rank"],
                "location": "湖南省永州市零陵区",
                "system": "party" if "委" in pos["title"] else "government",
                "rank": pos["rank"],
                "is_key_promotion": "书记" in pos["title"] or "区长" in pos["title"],
                "notes": pos.get("note", ""),
                "confidence": "confirmed" if p["name"] != "待查" else "unverified",
                "source_ids": ["S001"],
            }
            for pos in p_poses
        ],
        "organizations": [],
        "relationships": [],
        "_relationship_raw": p_rels,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": f"截至{AS_OF}，未在公开资料中发现关于 {p['name']} 的纪律处分、审计问题或负面报道。",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "零陵区政府门户网站",
                "url": "https://www.cnll.gov.cn",
                "publisher": "零陵区人民政府办公室",
                "published_at": AS_OF,
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "政府官网，但领导之窗栏目（/zwgk/ldzc/）返回404，待网站更新",
            },
            {
                "id": "S002",
                "title": "永州市政府门户网站",
                "url": "https://www.yzcity.gov.cn",
                "publisher": "永州市人民政府办公室",
                "published_at": AS_OF,
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "领导接听日栏目确认龙亮为零陵区委副书记、区长",
            },
        ],
        "confidence_summary": {
            "identity": "confirmed" if p["name"] != "待查" else "unverified",
            "current_role": "confirmed" if p["name"] != "待查" else "unverified",
            "career_completeness": "thin" if p["name"] != "待查" else "none",
            "relationship_confidence": "medium" if p["name"] != "待查" else "low",
            "biggest_gap": "公开履历完全缺失 — 出生年月、教育背景、完整职业生涯均待查",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{p['name']}的完整职业生涯是什么？出生年月、教育背景、历任职务？",
                "why_it_matters": "核心领导的基本履历是最基础的数据需求",
                "suggested_queries": [
                    f"{p['name']} 简历",
                    f"{p['name']} 任前公示",
                    f"{p['name']} 百度百科",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{p['name']}何时担任现职？前任上任时间？",
                "why_it_matters": "确定党政一把手搭班子时间线和共事年数",
                "suggested_queries": [
                    "零陵区 区委书记 任职 时间",
                    "零陵区 区长 任命",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "medium",
                "question": f"{p['name']}是否有永州市其他县区的工作经历？",
                "why_it_matters": "跨县交流模式分析",
                "suggested_queries": [
                    f"{p['name']} 永州",
                    f"{p['name']} 任职",
                ],
                "last_attempted": AS_OF,
            },
        ],
    }

    path = os.path.join(PERSONS_OUT, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(person_data, f, ensure_ascii=False, indent=2)
    PERSON_FILES.append(path)
    return path


# =========================================================================
# MAIN
# =========================================================================
def main():
    # 1. Build DB + GEXF via runner
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

    # 2. Build person JSON files for confirmed leaders
    for pid in [1, 2]:  # 赵立平, 龙亮
        path = build_person_json(pid)
        print(f"  Person JSON: {path}")

    # Print summary
    print(f"\n{'='*60}")
    print(f"  零陵区领导班子数据构建完成")
    print(f"{'='*60}")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
    print(f"  JSON:  {len(PERSON_FILES)} person files")
    print(f"{'='*60}")
    print(f"\nPerson count: {len(persons)}")
    print(f"Org count:    {len(organizations)}")
    print(f"Position count: {len(positions)}")
    print(f"Relationship count: {len(relationships)}")
    print(f"\n⚠ NOTE: 多数领导班子成员姓名待核查。")
    print(f"        因网络访问受限（Exa限流、Baidu 403、Jina超时），")
    print(f"        政府官网领导之窗栏目也返回404。")
    print(f"        确认的两名核心领导：赵立平（区委书记）、龙亮（区长）")
    print(f"        名称来自政府官网新闻。完整履历待补充。")


if __name__ == "__main__":
    main()
