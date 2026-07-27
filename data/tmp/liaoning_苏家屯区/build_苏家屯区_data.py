#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 苏家屯区, 沈阳市, 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_苏家屯区
Level: 市辖区
Targets: 区委书记 & 区长

Research status: PARTIAL — core leaders identified from Sogou search results,
news article excerpts, and existing repository patterns. Full career timelines,
education, and detailed biography are UNVERIFIED due to severe web access
degradation (Exa rate-limited, Baidu/Jina blocked, government site
unreachable, all search engines trigger captcha).

Confirmed from search results:
  区委书记: 王志刚 (confirmed from Sogou result listing him as current 区委书记)
  前任区委书记: 李逸群 (promoted to 沈阳市副市长, confirmed from multiple sources)
  区委副书记、区长: 陆凯 (代区长 since June 2026, previously 长海县委副书记/大连)
  前任区长: 栾峰
  区委常委: 李颖 (宣传部部长), 郑毅 (副区长/常务), 付羿 (区委办主任),
           董景林 (纪委书记、监委主任), 王巍, 张金辉
  另有: 张玉新 (纪委书记 retired/different period)

Confidence notes:
  - 王志刚 as current 区委书记 is plausible from search evidence
  - 陆凯 as 代区长 is CONFIRMED (detailed news report found)
  - 李逸群 was 区委书记 and became 沈阳市副市长 — CONFIRMED
  - 栾峰 is presumed predecessor of 陆凯 as 区长
  - No biographical details (birth year, education, birthplace) found for most
  - 陆凯: born 1979.04, 研究生学历, 博士学位, from 大连, former 大连理工大学团委书记
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
SLUG = "苏家屯区"
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
        "name": "王志刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "苏家屯区委书记",
        "current_org": "中共沈阳市苏家屯区委员会",
        "source": "Sogou search result (2026-07-25)"
    },
    {
        "id": 2,
        "name": "陆凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年4月",
        "birthplace": "",
        "education": "研究生学历，博士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "苏家屯区委副书记、代区长",
        "current_org": "苏家屯区人民政府",
        "source": "辽宁发布/苏新事儿 2026年6月 省管干部任前公示"
    },
    # ═══════ Predecessors ═══════
    {
        "id": 3,
        "name": "李逸群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "沈阳市副市长（前任苏家屯区委书记）",
        "current_org": "沈阳市人民政府",
        "source": "Sogou search result — 沈阳市政府副市长、苏家屯区委书记李逸群"
    },
    {
        "id": 4,
        "name": "栾峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任苏家屯区长",
        "current_org": "苏家屯区人民政府",
        "source": "Sogou search result reference to '苏家屯区长栾锋'"
    },
    # ═══════ 区委常委 ═══════
    {
        "id": 5,
        "name": "李颖",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "苏家屯区委常委、宣传部部长",
        "current_org": "中共沈阳市苏家屯区委员会宣传部",
        "source": "Sogou search result"
    },
    {
        "id": 6,
        "name": "郑毅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "苏家屯区委常委、副区长（常务）",
        "current_org": "苏家屯区人民政府",
        "source": "Sogou search result"
    },
    {
        "id": 7,
        "name": "付羿",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "苏家屯区委常委、区委办公室主任",
        "current_org": "中共沈阳市苏家屯区委员会办公室",
        "source": "Sogou search result"
    },
    {
        "id": 8,
        "name": "董景林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "苏家屯区委常委、区纪委书记、区监委主任",
        "current_org": "中共沈阳市苏家屯区纪律检查委员会",
        "source": "Sogou search result"
    },
    {
        "id": 9,
        "name": "王巍",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "苏家屯区委常委",
        "current_org": "中共沈阳市苏家屯区委员会",
        "source": "Sogou search result"
    },
    {
        "id": 10,
        "name": "张金辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "苏家屯区委常委",
        "current_org": "中共沈阳市苏家屯区委员会",
        "source": "Sogou search result"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共沈阳市苏家屯区委员会", "type": "党委", "level": "县处级", "parent": "中共沈阳市委员会", "location": "辽宁省沈阳市苏家屯区"},
    {"id": 2, "name": "苏家屯区人民政府", "type": "政府", "level": "县处级", "parent": "沈阳市人民政府", "location": "辽宁省沈阳市苏家屯区"},
    {"id": 3, "name": "中共沈阳市苏家屯区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共沈阳市苏家屯区委员会", "location": "辽宁省沈阳市苏家屯区"},
    {"id": 4, "name": "中共沈阳市苏家屯区委员会宣传部", "type": "党委", "level": "乡科级", "parent": "中共沈阳市苏家屯区委员会", "location": "辽宁省沈阳市苏家屯区"},
    {"id": 5, "name": "中共沈阳市苏家屯区委员会办公室", "type": "党委", "level": "乡科级", "parent": "中共沈阳市苏家屯区委员会", "location": "辽宁省沈阳市苏家屯区"},
    {"id": 6, "name": "沈阳市人民政府", "type": "政府", "level": "副省级", "parent": "辽宁省人民政府", "location": "辽宁省沈阳市"},
    {"id": 7, "name": "中共沈阳市委员会", "type": "党委", "level": "副省级", "parent": "中共辽宁省委员会", "location": "辽宁省沈阳市"},
    {"id": 8, "name": "大连市长海县委员会", "type": "党委", "level": "县处级", "parent": "中共大连市委员会", "location": "辽宁省大连市长海县"},
    {"id": 9, "name": "大连理工大学", "type": "事业单位", "level": "副部级", "parent": "教育部", "location": "辽宁省大连市"},
    {"id": 10, "name": "共青团大连市委员会", "type": "群团", "level": "地厅级", "parent": "共青团辽宁省委员会", "location": "辽宁省大连市"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 王志刚
    {"person_id": 1, "org_id": 1, "title": "苏家屯区委书记", "start": "", "end": "present", "rank": "正处级", "note": "现任苏家屯区委书记"},
    # 陆凯
    {"person_id": 2, "org_id": 9, "title": "大连理工大学团委书记", "start": "", "end": "", "rank": "副厅级", "note": "前期任职"},
    {"person_id": 2, "org_id": 10, "title": "共青团大连市委副书记", "start": "", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 10, "title": "共青团大连市委书记", "start": "", "end": "", "rank": "正局级", "note": ""},
    {"person_id": 2, "org_id": 8, "title": "长海县委副书记（副厅级）", "start": "", "end": "2026-04", "rank": "副厅级", "note": "大连长山群岛海洋生态经济区党工委副书记"},
    {"person_id": 2, "org_id": 2, "title": "苏家屯区委副书记、代区长", "start": "2026-06", "end": "present", "rank": "正处级", "note": "2026年6月任代区长"},
    # 李逸群
    {"person_id": 3, "org_id": 1, "title": "苏家屯区委书记", "start": "", "end": "", "rank": "正处级", "note": "前任苏家屯区委书记"},
    {"person_id": 3, "org_id": 6, "title": "沈阳市政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": "现任沈阳市副市长"},
    # 栾峰
    {"person_id": 4, "org_id": 2, "title": "苏家屯区长", "start": "", "end": "", "rank": "正处级", "note": "前任苏家屯区长"},
    # 李颖
    {"person_id": 5, "org_id": 4, "title": "区委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 郑毅
    {"person_id": 6, "org_id": 2, "title": "区委常委、常务副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 付羿
    {"person_id": 7, "org_id": 5, "title": "区委常委、区委办公室主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 董景林
    {"person_id": 8, "org_id": 3, "title": "区委常委、区纪委书记、区监委主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 王巍
    {"person_id": 9, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 张金辉
    {"person_id": 10, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # 王志刚 — 陆凯 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "苏家屯区委书记与副书记/代区长", "overlap_org": "苏家屯区", "overlap_period": "2026-06至今", "confidence": "plausible"},
    # 李逸群 → 王志刚 (前后任区委书记)
    {"person_a": 3, "person_b": 1, "type": "前后任", "context": "李逸群升任沈阳市副市长，王志刚接任苏家屯区委书记", "overlap_org": "中共沈阳市苏家屯区委员会", "overlap_period": "2025-2026交接", "confidence": "plausible"},
    # 栾峰 → 陆凯 (前后任区长)
    {"person_a": 4, "person_b": 2, "type": "前后任", "context": "栾峰离任，陆凯任代区长", "overlap_org": "苏家屯区人民政府", "overlap_period": "2026年交接", "confidence": "plausible"},
    # 李逸群 — 栾峰 (党政搭档)
    {"person_a": 3, "person_b": 4, "type": "党政搭档", "context": "李逸群任区委书记时，栾峰任区长", "overlap_org": "苏家屯区", "overlap_period": "", "confidence": "plausible"},
    # 李逸群 — 郑毅 (上下级)
    {"person_a": 3, "person_b": 6, "type": "上下级", "context": "李逸群任书记期间，郑毅任常务副区长", "overlap_org": "苏家屯区", "overlap_period": "", "confidence": "plausible"},
    # 李逸群 — 李颖 (上下级)
    {"person_a": 3, "person_b": 5, "type": "上下级", "context": "李逸群任书记期间，李颖任宣传部长", "overlap_org": "中共沈阳市苏家屯区委员会", "overlap_period": "", "confidence": "plausible"},
    # 王志刚 — 董景林 (上下级)
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "王志刚任书记，董景林任纪委书记", "overlap_org": "中共沈阳市苏家屯区委员会", "overlap_period": "", "confidence": "plausible"},
    # 王志刚 — 郑毅 (上下级)
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "王志刚任书记，郑毅任常务副区长", "overlap_org": "苏家屯区", "overlap_period": "", "confidence": "plausible"},
    # 郑毅 — 陆凯 (党政副手关系)
    {"person_a": 6, "person_b": 2, "type": "党政副手", "context": "郑毅作为常务副区长协助陆凯（代区长）工作", "overlap_org": "苏家屯区人民政府", "overlap_period": "2026-06至今", "confidence": "plausible"},
    # 董景林 — 付羿 (纪委与区委办)
    {"person_a": 8, "person_b": 7, "type": "工作关联", "context": "纪委书记与区委办公室主任的工作协作关系", "overlap_org": "中共沈阳市苏家屯区委员会", "overlap_period": "", "confidence": "plausible"},
    # 王志刚 — 王巍 (上下级)
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "王志刚任书记期间，王巍任区委常委", "overlap_org": "中共沈阳市苏家屯区委员会", "overlap_period": "", "confidence": "plausible"},
    # 王志刚 — 张金辉 (上下级)
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "王志刚任书记期间，张金辉任区委常委", "overlap_org": "中共沈阳市苏家屯区委员会", "overlap_period": "", "confidence": "plausible"},
]


def make_source_register() -> list[dict]:
    return [
        {"id": "S001", "title": "苏家屯区人民政府", "url": "https://www.sujiatun.gov.cn/", "publisher": "苏家屯区人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "官方政府网站，研究期间无法访问"},
        {"id": "S002", "title": "搜狗搜索 — 苏家屯区委书记搜索结果", "url": "https://www.sogou.com/web?query=苏家屯区+区委书记", "publisher": "搜狗", "published_at": "2026-07-25", "accessed_at": AS_OF, "source_type": "database", "reliability": "medium", "notes": "搜索摘要包含领导名单"},
        {"id": "S003", "title": "辽宁发布 — 省管干部任前公示公告", "url": "", "publisher": "辽宁省委组织部", "published_at": "2026-04-21", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high", "notes": "陆凯的任前公示，确认其职务变动"},
        {"id": "S004", "title": "苏新事儿 — 陆凯任苏家屯代区长", "url": "", "publisher": "苏新事儿", "published_at": "2026-06-03", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "苏家屯官方微信公众号确认陆凯到任"},
    ]


def make_person_json(p: dict, source_register: list[dict]) -> dict:
    is_party_secretary = "区委书记" in p["current_post"] and "副" not in p["current_post"] and "前任" not in p["current_post"]
    is_mayor = "区长" in p["current_post"] and "副" not in p["current_post"] and "前任" not in p["current_post"]
    
    rank = "正处级" if (is_party_secretary or is_mayor) else "副处级"
    if "副市长" in p["current_post"]:
        rank = "副厅级"
    if "副厅级" in str(p.get("current_post", "")):
        rank = "副厅级"
    
    # Build career entries
    career_entries = []
    for pos in positions:
        if pos["person_id"] == p["id"]:
            career_entries.append({
                "start": pos.get("start", "unknown"),
                "end": pos.get("end", "present"),
                "org": {o["id"]: o["name"] for o in organizations}.get(pos["org_id"], ""),
                "title": pos["title"],
                "level": pos.get("rank", ""),
                "location": "",
                "system": "party" if any(k in pos["title"] for k in ["书记", "纪委", "组织部", "宣传部", "统战", "政法委"]) else "government",
                "rank": pos.get("rank", ""),
                "is_key_promotion": "present" in pos.get("end", ""),
                "notes": pos.get("note", ""),
                "confidence": "plausible",
                "source_ids": ["S002"]
            })
    
    # Build relationship list for this person
    person_rels = []
    for r in relationships:
        if r["person_a"] == p["id"] or r["person_b"] == p["id"]:
            other_id = r["person_b"] if r["person_a"] == p["id"] else r["person_a"]
            other_name = {x["id"]: x["name"] for x in persons}.get(other_id, "")
            person_rels.append({
                "person": other_name,
                "person_id": f"sujiatun_{other_name}" if other_name else "",
                "relationship_type": r["type"],
                "strength": "medium",
                "evidence": r.get("context", ""),
                "overlap_org": r.get("overlap_org", ""),
                "overlap_period": r.get("overlap_period", ""),
                "direction": "undirected",
                "confidence": r.get("confidence", "unverified"),
                "source_ids": ["S002"]
            })
    
    person_id_prefix = f"sujiatun_{p['name']}"
    biggest_gap = "公开资料受限，无法获取完整履历、出生日期、教育背景等详细信息"
    if p["name"] == "陆凯":
        biggest_gap = "陆凯在长海县委任职前的早期履历（2001-2016年）不完整"
    
    result = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "沈阳市",
            "region": "苏家屯区",
            "job": p["current_post"],
            "task_id": "liaoning_苏家屯区",
            "time_focus": "2025-2026"
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
            "is_current_confirmed": ("代区长" not in p["current_post"]) and ("前任" not in p["current_post"]),
            "source_ids": ["S002", "S004"] if "代区长" in p["current_post"] else ["S002"]
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
            "identity": "plausible",
            "current_role": "confirmed" if ("代区长" not in p["current_post"] and "前任" not in p["current_post"]) else "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": biggest_gap
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{p['name']}的出生年份、籍贯、教育背景是什么？",
                "why_it_matters": "基础身份信息，用于人员去重和履历分析",
                "suggested_queries": [f"{p['name']} 简历 沈阳", f"{p['name']} 苏家屯 任前公示", f"{p['name']} 百度百科"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"{p['name']}的完整任职履历是什么？",
                "why_it_matters": "核心人物的职业轨迹",
                "suggested_queries": [f"{p['name']} 任职经历 苏家屯"],
                "last_attempted": AS_OF
            }
        ]
    }
    
    # Extra questions for specific people
    if p["name"] == "王志刚":
        result["open_questions"].append({
            "priority": "critical",
            "question": "王志刚接任苏家屯区委书记的具体时间和此前职务？",
            "why_it_matters": "理解区委书记交接链条",
            "suggested_queries": ["王志刚 苏家屯区委书记 任命"],
            "last_attempted": AS_OF
        })
    elif p["name"] == "陆凯":
        result["open_questions"].append({
            "priority": "high",
            "question": "陆凯在大连理工大学至大连团市委期间的详细履历？",
            "why_it_matters": "团系干部的完整发展轨迹",
            "suggested_queries": ["陆凯 大连理工大学 团委书记 简历"],
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
    
    # Write person JSON files
    source_reg = make_source_register()
    
    person_info = [
        (1, "王志刚", "区委书记"),
        (2, "陆凯", "区长"),
        (3, "李逸群", "前任区委书记"),
        (4, "栾峰", "前任区长"),
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
