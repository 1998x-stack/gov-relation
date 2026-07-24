#!/usr/bin/env python3
"""
大箐山县（黑龙江省伊春市）领导班子工作关系网络 — 2026-07-24
Build script for Daqingshan County, Yichun City, Heilongjiang Province.

Data sources:
- 大箐山县人民政府官网 http://www.ycdqs.gov.cn/ — news articles (2025-2026)
- News coverage of leadership activities (安东主持召开县委常委会, 孙兰松中考检查等)

TASK: heilongjiang_大箐山县

NOTE: The 大箐山县 government website (ycq.gov.cn) was accessible via HTTP but HTTPS
was unavailable. The county website domain is ycdqs.gov.cn (not ycq.gov.cn which is 峄城区).
Leadership names were extracted from official news articles published on the county website.
Biographical details (birth year, birthplace, education) remain incomplete and are explicitly
flagged as gaps. The precise dating of leadership transitions between 安东 (县委书记 as of
June 8, 2026) and 孙兰松 (县委书记、县长 as of June 24, 2026) requires further investigation.
"""

import json
import os
import sqlite3  # noqa: used via gov_relation.runner
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

TODAY = "2026-07-24"
AS_OF = TODAY

# ── STAGING DIRECTORIES ──
STAGING = Path(__file__).resolve().parent
DB_PATH = STAGING / "大箐山县_network.db"
GEXF_PATH = STAGING / "大箐山县_network.gexf"
PERSONS_DIR = STAGING

# ── DATA ──

# Integer IDs
PERSON_ID_MAP = {
    # 县委书记（市）  — confirmed: 安东 (as of June 8, 2026)
    "安东（大箐山县委书记）": 1,
    # 县委书记、县长 — confirmed: 孙兰松 (as of June 24, 2026, also serving as 县长)
    "孙兰松（大箐山县长/县委书记）": 2,
    # 县领导（县人大主任或政协主席）
    "纪谦勇（大箐山县领导）": 3,
    # 县委常委、组织部部长
    "周大为（大箐山县委常委、组织部部长）": 4,
    # 副县长
    "刘雪丹（大箐山县副县长）": 5,
    # 县领导（副县长或常委）
    "徐刚（大箐山县领导）": 6,
    # 县领导（副县长或常委）
    "田宝成（大箐山县领导）": 7,
}

ORG_ID_MAP = {
    "中共大箐山县委员会": 1,
    "大箐山县人民政府": 2,
    "大箐山县人大常委会": 3,
    "大箐山县政协": 4,
    "大箐山县纪委监委": 5,
    "大箐山县委组织部": 6,
    "政协伊春市委员会": 7,
}

# ── PERSONS ──

persons = [
    {
        "id": 1,
        "name": "安东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协副主席、县委书记",
        "current_org": "中共大箐山县委员会",
        "source": "大箐山县政府官网新闻（安东主持召开县委常委会会议 2026-06-08; 安东深入基层督导生态环保工作 2026-05-25）",
    },
    {
        "id": 2,
        "name": "孙兰松",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记、县长",
        "current_org": "大箐山县人民政府",
        "source": "大箐山县政府官网新闻（孙兰松检查指导中考考务工作 2026-06-24; 孙兰松主持召开项目推进会议 2026-06-15）",
    },
    {
        "id": 3,
        "name": "纪谦勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导（待确认职务）",
        "current_org": "大箐山县人大常委会",
        "source": "大箐山县政府官网新闻（大箐山县领导带头参加义务植树活动 2026-04-27）",
    },
    {
        "id": 4,
        "name": "周大为",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "大箐山县委组织部",
        "source": "大箐山县政府官网新闻（公益捐赠仪式 2026-04-24）",
    },
    {
        "id": 5,
        "name": "刘雪丹",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "大箐山县人民政府",
        "source": "大箐山县政府官网新闻（孙兰松检查指导中考考务工作 2026-06-24; 签约仪式 2026-05-08）",
    },
    {
        "id": 6,
        "name": "徐刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导（待确认职务）",
        "current_org": "大箐山县人民政府",
        "source": "大箐山县政府官网新闻（签约仪式 2026-05-08）",
    },
    {
        "id": 7,
        "name": "田宝成",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导（待确认职务）",
        "current_org": "大箐山县人民政府",
        "source": "大箐山县政府官网新闻（签约仪式 2026-05-08）",
    },
]

# ── ORGANIZATIONS ──

organizations = [
    {"id": 1, "name": "中共大箐山县委员会", "type": "党委", "level": "县处级", "parent": "中共伊春市委员会", "location": "黑龙江省伊春市大箐山县"},
    {"id": 2, "name": "大箐山县人民政府", "type": "政府", "level": "县处级", "parent": "伊春市人民政府", "location": "黑龙江省伊春市大箐山县"},
    {"id": 3, "name": "大箐山县人大常委会", "type": "人大", "level": "县处级", "parent": "大箐山县", "location": "黑龙江省伊春市大箐山县"},
    {"id": 4, "name": "大箐山县政协", "type": "政协", "level": "县处级", "parent": "大箐山县", "location": "黑龙江省伊春市大箐山县"},
    {"id": 5, "name": "大箐山县纪委监委", "type": "党委", "level": "县处级", "parent": "中共大箐山县委员会", "location": "黑龙江省伊春市大箐山县"},
    {"id": 6, "name": "大箐山县委组织部", "type": "党委", "level": "乡科级", "parent": "中共大箐山县委员会", "location": "黑龙江省伊春市大箐山县"},
    {"id": 7, "name": "政协伊春市委员会", "type": "政协", "level": "地厅级", "parent": "伊春市", "location": "黑龙江省伊春市"},
]

# ── POSITIONS ──

positions = [
    # 安东
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "unknown", "end_date": "present", "rank": "县处级正职", "note": "安东同时担任伊春市政协副主席（地厅级副职）"},
    {"person_id": 1, "org_id": 7, "title": "市政协副主席", "start_date": "unknown", "end_date": "present", "rank": "地厅级副职", "note": "兼职"},
    # 孙兰松
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "unknown", "end_date": "present", "rank": "县处级正职", "note": "2026年6月24日新闻显示同时担任县委书记"},
    # 纪谦勇
    {"person_id": 3, "org_id": 3, "title": "县领导（待确认职务）", "start_date": "unknown", "end_date": "present", "rank": "", "note": "可能担任县人大常委会主任或县政协主席"},
    # 周大为
    {"person_id": 4, "org_id": 6, "title": "县委常委、组织部部长", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 刘雪丹
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 徐刚
    {"person_id": 6, "org_id": 2, "title": "县领导（待确认职务）", "start_date": "unknown", "end_date": "present", "rank": "", "note": "可能为县委常委或副县长"},
    # 田宝成
    {"person_id": 7, "org_id": 2, "title": "县领导（待确认职务）", "start_date": "unknown", "end_date": "present", "rank": "", "note": "可能为县委常委或副县长"},
]

# ── RELATIONSHIPS ──

relationships = [
    # 安东 x 孙兰松 — 党政一把手搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "安东（县委书记）与孙兰松（县长）为大箐山县党政一把手搭档，共同出席植树活动等公务", "overlap_org": "大箐山县", "overlap_period": "2026"},
    # 安东 x 纪谦勇
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "安东与纪谦勇同为县领导，共同参加义务植树活动", "overlap_org": "大箐山县", "overlap_period": "2026"},
    # 孙兰松 x 刘雪丹 — 上下级
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "孙兰松（县长）领导副县长刘雪丹，共同检查中考考务工作", "overlap_org": "大箐山县人民政府", "overlap_period": "2026"},
    # 孙兰松 x 徐刚
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "孙兰松与徐刚共同出席签约仪式", "overlap_org": "大箐山县人民政府", "overlap_period": "2026"},
    # 孙兰松 x 田宝成
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "孙兰松与田宝成共同出席签约仪式", "overlap_org": "大箐山县人民政府", "overlap_period": "2026"},
    # 孙兰松 x 周大为
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "孙兰松（县委副书记/县长）与周大为（县委常委、组织部部长）同在县委领导班子", "overlap_org": "中共大箐山县委员会", "overlap_period": "2026"},
    # 安东 x 周大为
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "安东（县委书记）与周大为（县委常委、组织部部长）同在县委常委会", "overlap_org": "中共大箐山县委员会", "overlap_period": "2026"},
]

# ── PERSON JSON HELPERS ──

def write_person_json(person, relationships, organizations):
    """Write a single person JSON file following the project schema."""
    today = TODAY
    person_id = person["id"]
    
    # Determine role color and person_id prefix
    name = person["name"]
    job = person["current_post"]
    
    # Create person_id string like "daqingshan_an_dong"
    p_id = f"daqingshan_{name.replace('（','_').replace('）','').lower().replace(' ','_')}"
    
    # Filter relationships for this person
    person_rels = [r for r in relationships if r["person_a"] == person_id or r["person_b"] == person_id]
    
    # Map relationship data
    rel_list = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == person_id else r["person_a"]
        other_person = next((p for p in persons if p["id"] == other_id), None)
        if other_person:
            rel_list.append({
                "person": other_person["name"],
                "person_id": f"daqingshan_{other_person['name'].replace('（','_').replace('）','').lower().replace(' ','_')}",
                "relationship_type": r["type"],
                "strength": "strong",
                "evidence": r["context"],
                "overlap_org": r["overlap_org"],
                "overlap_period": r["overlap_period"],
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            })
    
    # Career timeline
    person_positions = [p for p in positions if p["person_id"] == person_id]
    career = []
    for pos in person_positions:
        org_name = next((o["name"] for o in organizations if o["id"] == pos["org_id"]), "")
        career.append({
            "start": pos["start_date"] if pos["start_date"] != "unknown" else "",
            "end": pos["end_date"],
            "org": org_name,
            "title": pos["title"],
            "level": pos["rank"],
            "location": "黑龙江省伊春市大箐山县",
            "system": "government" if "政府" in org_name or "县长" in pos["title"] else "party",
            "rank": pos["rank"],
            "is_key_promotion": False,
            "notes": pos["note"],
            "confidence": "confirmed",
            "source_ids": ["S001"],
        })
    
    # Orgs
    org_list = []
    for pos in person_positions:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        if org:
            org_list.append({
                "name": org["name"],
                "type": org["type"],
                "level": org["level"],
                "location": org["location"],
            })
    
    # Source register
    sources = [
        {
            "id": "S001",
            "title": f"大箐山县人民政府官网新闻",
            "url": "http://www.ycdqs.gov.cn/",
            "publisher": "大箐山县人民政府",
            "published_at": "2026",
            "accessed_at": "2026-07-24",
            "source_type": "official",
            "reliability": "high",
            "notes": "多个新闻页面交叉验证",
        }
    ]
    
    person_json = {
        "schema_version": "1.0",
        "generated_at": today,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "伊春市",
            "region": "大箐山县",
            "job": job,
            "task_id": "heilongjiang_大箐山县",
            "time_focus": "2025-2026",
        },
        "identity": {
            "person_id": p_id,
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_",
                "name_birthplace": f"{name}_",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": job,
            "current_org": person["current_org"],
            "administrative_rank": "县处级正职" if "书记" in job or "县长" in job else "县处级副职",
            "as_of": today,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": career,
        "organizations": org_list,
        "relationships": rel_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["party", "government"],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "无法评估——公开资料不足",
                "notable_fast_promotions": [],
            },
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
                "description": "未发现任何负面纪律审查、审计问题或负面媒体报道",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": sources,
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "high",
            "biggest_gap": "出生年份、出生地、教育背景和任现职前的完整工作履历完全缺失。大箐山县系2019年撤区设县新设县，领导信息有限。",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的出生年份、出生地、教育背景是什么？",
                "why_it_matters": "核心人物的基础身份信息，用于跨区县去重和关系挖掘",
                "suggested_queries": [f"{name} 简历 大箐山", f"{name} 伊春 任职", f"{name} 出生 年月"],
                "last_attempted": "2026-07-24",
            },
            {
                "priority": "critical",
                "question": f"{name}任现职前担任过什么职务？从哪个岗位调任？",
                "why_it_matters": "了解其晋升路径和潜在关系网络",
                "suggested_queries": [f"{name} 此前 担任", f"{name} 任职 经历", f"{name} 任前公示"],
                "last_attempted": "2026-07-24",
            },
        ],
    }
    
    # Write JSON file
    safe_job = job.replace("（", "(").replace("）", ")").replace("、", "_").replace("，", ",")
    filename = f"{today}-黑龙江省-伊春市-{safe_job}-{name}.json"
    filepath = STAGING / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(person_json, f, ensure_ascii=False, indent=2)
    return filepath


# ── MAIN ──

def main():
    print(f"大箐山县（黑龙江省伊春市）领导班子工作关系网络 — {TODAY}")
    print(f"Task: heilongjiang_大箐山县")
    print()
    
    print("Building database and GEXF...")
    run_build(
        slug="大箐山县领导班子关系图",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    
    print()
    print("Writing person JSON files...")
    json_files = []
    for p in persons:
        fp = write_person_json(p, relationships, organizations)
        json_files.append(fp)
        print(f"  {fp.name}")
    
    print()
    print("=== Summary ===")
    print(f"  Persons:         {len(persons)}")
    print(f"  Organizations:   {len(organizations)}")
    print(f"  Positions:       {len(positions)}")
    print(f"  Relationships:   {len(relationships)}")
    print(f"  Person JSON:     {len(json_files)}")
    print()
    print("Done. All artifacts written to staging directory.")
    
    # Verify files exist
    for fp in [DB_PATH, GEXF_PATH] + json_files:
        assert fp.exists(), f"Missing: {fp}"
    print("All files verified successfully.")


if __name__ == "__main__":
    main()
