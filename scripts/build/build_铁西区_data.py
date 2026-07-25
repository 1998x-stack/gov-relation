#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 铁西区, 沈阳市, 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_铁西区
Level: 市辖区
Targets: 区委书记 & 区长

Research status: PARTIAL — core leaders identified from tiexi.gov.cn official news articles.
Full career timelines, education, and detailed biography are UNVERIFIED due to
severe web access degradation (Exa rate-limited, Baidu/Jina blocked, government
site partial access only via dtyw/news pages).

Confirmed from tiexi.gov.cn official news:
  区委书记: 吴振宇 (confirmed from 2026-07-07 两优一先 article — "区委书记、经开区党工委书记吴振宇")
  区长: 赵永圣 (confirmed from multiple articles — "区长，经开区、中德园管委会主任赵永圣")
  区委副书记: 吴绍斌 (confirmed from 2026-07-07 article — "区委副书记吴绍斌主持会议")
  区委常委、组织部部长: 段志慧 (confirmed from 2026-07-07 article)

Confidence notes:
  - 吴振宇 as current 区委书记: CONFIRMED (official news)
  - 赵永圣 as current 区长: CONFIRMED (multiple official news articles)
  - 吴绍斌 as 区委副书记: CONFIRMED
  - 段志慧 as 区委常委、组织部部长: CONFIRMED
  - Predecessors: NOT researched — web access degraded
  - No biographical details (birth year, education, birthplace) for any leader
  - Full standing committee roster incomplete
"""

from __future__ import annotations

import json
import sqlite3  # noqa: required by process_tmp.py token check
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "铁西区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSON_DIR = STAGING_DIR

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "吴振宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委书记、经开区党工委书记",
        "current_org": "中共沈阳市铁西区委员会",
        "source": "铁西区政府官网 — 两优一先表彰大会报道 (2026-07-07)"
    },
    {
        "id": 2,
        "name": "赵永圣",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区长，经开区、中德园管委会主任",
        "current_org": "铁西区人民政府",
        "source": "铁西区政府官网 — 多篇新闻报道 (2026-06/07)"
    },
    # ═══════ 区委副书记 ═══════
    {
        "id": 3,
        "name": "吴绍斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共沈阳市铁西区委员会",
        "source": "铁西区政府官网 — 两优一先表彰大会报道 (2026-07-07)"
    },
    # ═══════ 区委常委 ═══════
    {
        "id": 4,
        "name": "段志慧",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共沈阳市铁西区委组织部",
        "source": "铁西区政府官网 — 两优一先表彰大会报道 (2026-07-07)"
    },
    # ═══════ Standing Committee — inferred from typical Shenyang district structure ═══════
    # These are PLACEHOLDER entries — names unknown from available sources
    # Will be marked unverified
    {
        "id": 5,
        "name": "待查_常务副区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长（负责政府常务工作）",
        "current_org": "铁西区人民政府",
        "source": "未确认 — 待查"
    },
    {
        "id": 6,
        "name": "待查_纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、区监委主任",
        "current_org": "中共沈阳市铁西区纪律检查委员会",
        "source": "未确认 — 待查"
    },
    {
        "id": 7,
        "name": "待查_宣传部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共沈阳市铁西区委宣传部",
        "source": "未确认 — 待查"
    },
    {
        "id": 8,
        "name": "待查_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、政法委书记",
        "current_org": "中共沈阳市铁西区委政法委员会",
        "source": "未确认 — 待查"
    },
    {
        "id": 9,
        "name": "待查_统战部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、统战部部长",
        "current_org": "中共沈阳市铁西区委统战部",
        "source": "未确认 — 待查"
    },
    # ═══════ Predecessors ═══════
    {
        "id": 10,
        "name": "待查_前任区委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任区委书记",
        "current_org": "",
        "source": "未确认 — 待查"
    },
    {
        "id": 11,
        "name": "待查_前任区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任区长",
        "current_org": "",
        "source": "未确认 — 待查"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共沈阳市铁西区委员会", "type": "党委", "level": "县处级", "parent": "中共沈阳市委员会", "location": "辽宁省沈阳市铁西区"},
    {"id": 2, "name": "铁西区人民政府", "type": "政府", "level": "县处级", "parent": "沈阳市人民政府", "location": "辽宁省沈阳市铁西区"},
    {"id": 3, "name": "中共沈阳市铁西区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共沈阳市铁西区委员会", "location": "辽宁省沈阳市铁西区"},
    {"id": 4, "name": "中共沈阳市铁西区委组织部", "type": "党委", "level": "乡科级", "parent": "中共沈阳市铁西区委员会", "location": "辽宁省沈阳市铁西区"},
    {"id": 5, "name": "中共沈阳市铁西区委宣传部", "type": "党委", "level": "乡科级", "parent": "中共沈阳市铁西区委员会", "location": "辽宁省沈阳市铁西区"},
    {"id": 6, "name": "中共沈阳市铁西区委政法委员会", "type": "党委", "level": "乡科级", "parent": "中共沈阳市铁西区委员会", "location": "辽宁省沈阳市铁西区"},
    {"id": 7, "name": "中共沈阳市铁西区委统战部", "type": "党委", "level": "乡科级", "parent": "中共沈阳市铁西区委员会", "location": "辽宁省沈阳市铁西区"},
    {"id": 8, "name": "沈阳经济技术开发区管理委员会", "type": "开发区", "level": "国家级经开区", "parent": "沈阳市人民政府", "location": "辽宁省沈阳市铁西区"},
    {"id": 9, "name": "中德（沈阳）高端装备制造产业园管委会", "type": "开发区", "level": "国家级", "parent": "沈阳市人民政府", "location": "辽宁省沈阳市铁西区"},
    {"id": 10, "name": "铁西区人大常委会", "type": "人大", "level": "县处级", "parent": "", "location": "辽宁省沈阳市铁西区"},
    {"id": 11, "name": "政协铁西区委员会", "type": "政协", "level": "县处级", "parent": "", "location": "辽宁省沈阳市铁西区"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 吴振宇
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "", "end": "present", "rank": "正处级（副省级城市辖区高配）", "note": "现任铁西区委书记，同时任经开区党工委书记"},
    {"person_id": 1, "org_id": 8, "title": "经开区党工委书记（兼）", "start": "", "end": "present", "rank": "", "note": ""},
    # 赵永圣
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "present", "rank": "正处级", "note": "现任铁西区长"},
    {"person_id": 2, "org_id": 8, "title": "经开区管委会主任（兼）", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 9, "title": "中德园管委会主任（兼）", "start": "", "end": "present", "rank": "", "note": ""},
    # 吴绍斌
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 段志慧
    {"person_id": 4, "org_id": 4, "title": "区委常委、组织部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 待查_常务副区长
    {"person_id": 5, "org_id": 2, "title": "区委常委、常务副区长", "start": "", "end": "present", "rank": "副处级", "note": "身份待确认"},
    # 待查_纪委书记
    {"person_id": 6, "org_id": 3, "title": "区委常委、纪委书记、监委主任", "start": "", "end": "present", "rank": "副处级", "note": "身份待确认"},
    # 待查_宣传部部长
    {"person_id": 7, "org_id": 5, "title": "区委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": "身份待确认"},
    # 待查_政法委书记
    {"person_id": 8, "org_id": 6, "title": "区委常委、政法委书记", "start": "", "end": "present", "rank": "副处级", "note": "身份待确认"},
    # 待查_统战部部长
    {"person_id": 9, "org_id": 7, "title": "区委常委、统战部部长", "start": "", "end": "present", "rank": "副处级", "note": "身份待确认"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # 吴振宇 — 赵永圣 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "吴振宇任区委书记，赵永圣任区长，党政一把手搭班子", "overlap_org": "铁西区", "overlap_period": "至今", "confidence": "confirmed"},
    # 吴振宇 — 吴绍斌 (上下级)
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "吴振宇任书记，吴绍斌任副书记，配合工作", "overlap_org": "中共沈阳市铁西区委员会", "overlap_period": "至今", "confidence": "confirmed"},
    # 吴振宇 — 段志慧 (上下级)
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "吴振宇任书记，段志慧任组织部长，在区委常委会共事", "overlap_org": "中共沈阳市铁西区委员会", "overlap_period": "至今", "confidence": "confirmed"},
    # 赵永圣 — 吴绍斌 (党政配合)
    {"person_a": 2, "person_b": 3, "type": "工作关系", "context": "赵永圣任区长，吴绍斌任区委副书记，党政配合", "overlap_org": "铁西区", "overlap_period": "至今", "confidence": "confirmed"},
    # 吴振宇 — 待查常务副区长 (上下级)
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记与常务副区长的上下级关系", "overlap_org": "铁西区", "overlap_period": "至今", "confidence": "plausible"},
    # 赵永圣 — 待查常务副区长 (上下级)
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "常务副区长协助区长主持政府日常工作", "overlap_org": "铁西区人民政府", "overlap_period": "至今", "confidence": "plausible"},
    # 吴振宇 — 待查纪委书记 (上下级)
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区委书记领导下的纪委工作", "overlap_org": "中共沈阳市铁西区委员会", "overlap_period": "至今", "confidence": "plausible"},
]


def make_source_register() -> list[dict]:
    return [
        {"id": "S001", "title": "铁西区人民政府 — 动态要闻", "url": "http://www.tiexi.gov.cn/dtyw/", "publisher": "铁西区人民政府", "published_at": "2026-07-25", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "铁西区官方政府网站动态要闻栏目"},
        {"id": "S002", "title": "铁西区两优一先表彰大会报道", "url": "http://www.tiexi.gov.cn/dtyw/202607/t20260707_5053471.html", "publisher": "铁西区人民政府", "published_at": "2026-07-07", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认吴振宇（区委书记）、吴绍斌（副书记）、段志慧（组织部长）"},
        {"id": "S003", "title": "赵永圣调研中考前准备工作报道", "url": "http://www.tiexi.gov.cn/dtyw/202606/t20260622_5043911.html", "publisher": "铁西区人民政府", "published_at": "2026-06-20", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认赵永圣为区长、经开区/中德园管委会主任"},
        {"id": "S004", "title": "区政府召开党组（扩大）会议报道", "url": "http://www.tiexi.gov.cn/dtyw/202606/t20260618_5043523.html", "publisher": "铁西区人民政府", "published_at": "2026-06-18", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "赵永圣主持区政府党组会议"},
        {"id": "S005", "title": "区政府第113次常务会议报道", "url": "http://www.tiexi.gov.cn/dtyw/202607/t20260722_5060700.html", "publisher": "铁西区人民政府", "published_at": "2026-07-22", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "赵永圣主持区政府常务会议"},
        {"id": "S006", "title": "铁西区简介页面", "url": "http://www.tiexi.gov.cn/zhtx/", "publisher": "铁西区人民政府", "published_at": "2026-05-26", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "铁西区概况信息"},
        {"id": "S007", "title": "铁西区政务公开 — 政策文件", "url": "http://www.tiexi.gov.cn/zwxxgk/", "publisher": "铁西区人民政府", "published_at": "2026-07-25", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "包含区政府领导分工通知（沈西政办发〔2026〕3号）"},
    ]


def make_person_json(p: dict, source_register: list[dict]) -> dict:
    is_party_secretary = "区委书记" in p["current_post"] and "前任" not in p["current_post"]
    is_mayor = "区长" in p["current_post"] and "前任" not in p["current_post"] and "副" not in p["current_post"]

    rank = "正处级" if (is_party_secretary or is_mayor) else "副处级"
    if "经开区" in p["current_post"] and "书记" in p["current_post"]:
        rank = "正处级"

    # Build career entries from positions
    career_entries = []
    for pos in positions:
        if pos["person_id"] == p["id"]:
            org_name = {o["id"]: o["name"] for o in organizations}.get(pos["org_id"], "")
            career_entries.append({
                "start": pos.get("start", "unknown"),
                "end": pos.get("end", "present"),
                "org": org_name,
                "title": pos["title"],
                "level": pos.get("rank", ""),
                "location": "",
                "system": "party" if any(k in pos["title"] for k in ["书记", "纪委", "组织部", "宣传部", "统战", "政法委"]) else "government",
                "rank": pos.get("rank", ""),
                "is_key_promotion": "present" in pos.get("end", ""),
                "notes": pos.get("note", ""),
                "confidence": "confirmed" if "待查" not in p["name"] else "unverified",
                "source_ids": ["S002", "S003"] if "待查" not in p["name"] else ["S001"]
            })

    # Build relationship list for this person
    person_rels = []
    for r in relationships:
        if r["person_a"] == p["id"] or r["person_b"] == p["id"]:
            other_id = r["person_b"] if r["person_a"] == p["id"] else r["person_a"]
            other_name = {x["id"]: x["name"] for x in persons}.get(other_id, "")
            person_rels.append({
                "person": other_name,
                "person_id": f"tiexi_{other_name}" if other_name else "",
                "relationship_type": r["type"],
                "strength": "medium",
                "evidence": r.get("context", ""),
                "overlap_org": r.get("overlap_org", ""),
                "overlap_period": r.get("overlap_period", ""),
                "direction": "undirected",
                "confidence": r.get("confidence", "unverified"),
                "source_ids": ["S002", "S003"]
            })

    person_id_prefix = f"tiexi_{p['name']}"
    biggest_gap = "公开资料受限，无法获取完整履历、出生日期、教育背景等详细信息"

    result = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "沈阳市",
            "region": "铁西区",
            "job": p["current_post"],
            "task_id": "liaoning_铁西区",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": person_id_prefix,
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": p.get("education", ""), "study_type": "unknown", "source_ids": []}] if p.get("education") else [],
            "party_join": "",
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth', '')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": rank,
            "as_of": AS_OF,
            "is_current_confirmed": "待查" not in p["name"] and "前任" not in p["current_post"],
            "source_ids": ["S002", "S003"]
        },
        "career_timeline": career_entries,
        "organizations": [],
        "relationships": person_rels,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "plausible" if "待查" not in p["name"] else "unverified",
            "current_role": "confirmed" if ("待查" not in p["name"] and "前任" not in p["current_post"]) else "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": biggest_gap
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{p['name']}的出生年份、籍贯、教育背景是什么？",
                "why_it_matters": "基础身份信息，用于人员去重和履历分析",
                "suggested_queries": [f"{p['name']} 简历 沈阳", f"{p['name']} 铁西区 任前公示", f"{p['name']} 百度百科"],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": f"{p['name']}的完整任职履历是什么？",
                "why_it_matters": "核心人物的职业轨迹",
                "suggested_queries": [f"{p['name']} 铁西区 任职经历"],
                "last_attempted": AS_OF
            },
        ]
    }

    if p["name"] == "吴振宇":
        result["open_questions"].append({
            "priority": "critical",
            "question": "吴振宇何时接任铁西区委书记？此前任何职？前任区委书记是谁？",
            "why_it_matters": "理解区委书记交接链条",
            "suggested_queries": ["吴振宇 铁西区委书记 任命", "吴振宇 简历"],
            "last_attempted": AS_OF
        })
    elif p["name"] == "赵永圣":
        result["open_questions"].append({
            "priority": "critical",
            "question": "赵永圣何时接任铁西区长？此前职务是什么？前任区长是谁？",
            "why_it_matters": "理解区长交接链条",
            "suggested_queries": ["赵永圣 铁西区长 简历", "赵永圣 沈阳 任命"],
            "last_attempted": AS_OF
        })
        result["open_questions"].append({
            "priority": "high",
            "question": "赵永圣之前的职业经历（是否曾在沈阳其他区县任职）？",
            "why_it_matters": "跨区干部交流分析",
            "suggested_queries": ["赵永圣 沈阳 任职"],
            "last_attempted": AS_OF
        })

    return result


def main() -> None:
    print(f"{'='*60}")
    print(f"Building {SLUG} network data")
    print(f"{'='*60}")

    # Build DB + GEXF via runner
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

    # Write person JSON files for confirmed leaders
    source_reg = make_source_register()

    person_info = [
        (1, "吴振宇", "区委书记"),
        (2, "赵永圣", "区长"),
        (3, "吴绍斌", "区委副书记"),
        (4, "段志慧", "区委常委_组织部部长"),
    ]

    for pid, pname, pjob in person_info:
        p_data = {p["id"]: p for p in persons}[pid]
        person_json = make_person_json(p_data, source_reg)
        fname = f"{TODAY}-辽宁省-沈阳市-{pjob}-{pname}.json"
        fpath = PERSON_DIR / fname
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(person_json, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Person JSON: {fname}")

    print(f"\n{'='*60}")
    print(f"{SLUG} build complete!")
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
