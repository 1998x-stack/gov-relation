#!/usr/bin/env python3
"""Build script for 临沂市兰山区 cadre exchange network investigation.

Data sourced from official 兰山区政府 website (www.lyls.gov.cn),
leadership page (gk2/qzfld.htm), news articles dated July 2026,
and Zh.wikipedia.org district overview.

As-of date: 2026-07-25
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

AS_OF = "2026-07-25"
AS_OF_SHORT = AS_OF.replace("-", "")
PROV = "山东省"
CITY = "临沂市"
REGION = "兰山区"
SLUG = "兰山区"
TASK_ID = f"shandong_{SLUG}"

# Paths using project convention
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR, TMP_DIR

DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"
TASK_TMP = TMP_DIR / TASK_ID
PERSONS_OUT = TASK_TMP / "persons"

TASK_TMP.mkdir(parents=True, exist_ok=True)
PERSONS_OUT.mkdir(parents=True, exist_ok=True)

# =========================================================================
# DATA — persons, organizations, positions, relationships
# =========================================================================

# Confirmation sources (all from ly ls.gov.cn official news & leadership page):
# - www.lyls.gov.cn/gk2/qzfld/ck.htm  — 程凯 leadership profile (2026-07)
# - www.lyls.gov.cn/gk2/qzfld/lyx.htm — 刘元迅 leadership profile
# - www.lyls.gov.cn/gk2/qzfld/tzc.htm — 田宗春 leadership profile
# - www.lyls.gov.cn/gk2/qzfld/gxx.htm — 高兴先 leadership profile
# - www.lyls.gov.cn/gk2/qzfld/cjq.htm — 曹景强 leadership profile
# - www.lyls.gov.cn/gk2/qzfld/zl.htm  — 赵磊 leadership profile
# - www.lyls.gov.cn/gk2/qzfld/zt.htm  — 赵童 leadership profile
# - www.lyls.gov.cn/gk2/qzfld/lhb.htm — 刘海波 leadership profile
# - www.lyls.gov.cn — multiple news articles showing 程凯 as 区长 active through 2026-07-24

PERSONS_DATA = [
    # ── Top Leaders ──
    {
        "id": 1, "name": "刘波", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "兰山区委书记", "current_org": "中共临沂市兰山区委员会",
        "source": "http://www.lyls.gov.cn/ — 区委书记刘波在巡察工作会议中出现 (2026-04)"
    },
    {
        "id": 2, "name": "程凯", "gender": "男", "ethnicity": "汉族",
        "birth": "1977年4月", "birthplace": "",
        "education": "大学学历", "party_join": "中共党员", "work_start": "",
        "current_post": "兰山区委副书记、区长", "current_org": "临沂市兰山区人民政府",
        "source": "http://www.lyls.gov.cn/gk2/qzfld/ck.htm"
    },
    # ── Government Deputy Leaders ──
    {
        "id": 3, "name": "刘元迅", "gender": "男", "ethnicity": "汉族",
        "birth": "1973年12月", "birthplace": "",
        "education": "省委党校研究生", "party_join": "中共党员", "work_start": "",
        "current_post": "兰山区委常委、副区长（常务）", "current_org": "临沂市兰山区人民政府",
        "source": "http://www.lyls.gov.cn/gk2/qzfld/lyx.htm"
    },
    {
        "id": 4, "name": "田宗春", "gender": "男", "ethnicity": "汉族",
        "birth": "1968年9月", "birthplace": "",
        "education": "大学学历", "party_join": "中共党员", "work_start": "",
        "current_post": "兰山商城管委会主任、党委书记", "current_org": "兰山商城管理委员会",
        "source": "http://www.lyls.gov.cn/gk2/qzfld/tzc.htm"
    },
    {
        "id": 5, "name": "高兴先", "gender": "男", "ethnicity": "汉族",
        "birth": "1975年6月", "birthplace": "",
        "education": "大学学历", "party_join": "中共党员", "work_start": "",
        "current_post": "兰山区副区长、公安分局局长", "current_org": "临沂市兰山区人民政府",
        "source": "http://www.lyls.gov.cn/gk2/qzfld/gxx.htm"
    },
    {
        "id": 6, "name": "曹景强", "gender": "男", "ethnicity": "汉族",
        "birth": "1975年5月", "birthplace": "",
        "education": "大学学历", "party_join": "中共党员", "work_start": "",
        "current_post": "兰山区副区长", "current_org": "临沂市兰山区人民政府",
        "source": "http://www.lyls.gov.cn/gk2/qzfld/cjq.htm"
    },
    {
        "id": 7, "name": "赵磊", "gender": "男", "ethnicity": "汉族",
        "birth": "1977年6月", "birthplace": "",
        "education": "省委党校研究生", "party_join": "中共党员", "work_start": "",
        "current_post": "兰山区副区长", "current_org": "临沂市兰山区人民政府",
        "source": "http://www.lyls.gov.cn/gk2/qzfld/zl.htm"
    },
    {
        "id": 8, "name": "赵童", "gender": "女", "ethnicity": "汉族",
        "birth": "1984年2月", "birthplace": "",
        "education": "研究生", "party_join": "中共党员", "work_start": "",
        "current_post": "兰山区副区长", "current_org": "临沂市兰山区人民政府",
        "source": "http://www.lyls.gov.cn/gk2/qzfld/zt.htm"
    },
    {
        "id": 9, "name": "刘海波", "gender": "男", "ethnicity": "汉族",
        "birth": "1979年5月", "birthplace": "",
        "education": "大学学历", "party_join": "中共党员", "work_start": "",
        "current_post": "兰山区政府党组成员、办公室主任", "current_org": "临沂市兰山区人民政府办公室",
        "source": "http://www.lyls.gov.cn/gk2/qzfld/lhb.htm"
    },
]

# Organizations
ORGANIZATIONS_DATA = [
    {"id": 1, "name": "中共临沂市兰山区委员会", "type": "党委", "level": "县级", "parent": "中共临沂市委", "location": "临沂市兰山区"},
    {"id": 2, "name": "临沂市兰山区人民政府", "type": "政府", "level": "县级", "parent": "临沂市人民政府", "location": "临沂市兰山区"},
    {"id": 3, "name": "兰山商城管理委员会", "type": "事业单位", "level": "县级", "parent": "临沂市兰山区人民政府", "location": "临沂市兰山区"},
    {"id": 4, "name": "临沂市公安局兰山分局", "type": "政府", "level": "县级", "parent": "临沂市公安局", "location": "临沂市兰山区"},
    {"id": 5, "name": "临沂市兰山区人民政府办公室", "type": "政府", "level": "县级", "parent": "临沂市兰山区人民政府", "location": "临沂市兰山区"},
    {"id": 6, "name": "临沂市兰山区财政局", "type": "政府", "level": "县级", "parent": "临沂市兰山区人民政府", "location": "临沂市兰山区"},
    {"id": 7, "name": "临沂市兰山区商务局", "type": "政府", "level": "县级", "parent": "临沂市兰山区人民政府", "location": "临沂市兰山区"},
]

# Positions
POSITIONS_DATA = [
    {"person_id": 1, "org_id": 1, "title": "兰山区委书记", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "兰山区委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "兰山区区长", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "兰山区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "兰山区副区长（常务）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "协助区长分管财政、审计"},
    {"person_id": 4, "org_id": 2, "title": "兰山区领导（商城管委会）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "兼临沂商城管委会副主任"},
    {"person_id": 4, "org_id": 3, "title": "兰山商城管委会主任、党委书记", "start_date": "", "end_date": "", "rank": "县处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "兰山区副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "分管公安、司法、退役军人等"},
    {"person_id": 5, "org_id": 4, "title": "兰山公安分局局长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "二级高级警长"},
    {"person_id": 6, "org_id": 2, "title": "兰山区副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "分管住建、综合执法、交通运输等"},
    {"person_id": 7, "org_id": 2, "title": "兰山区副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "分管生态环境、民政、人社等"},
    {"person_id": 8, "org_id": 2, "title": "兰山区副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "分管教育体育、水务、农业农村、文旅等"},
    {"person_id": 9, "org_id": 5, "title": "兰山区政府办公室主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "区政府党组成员"},
]

# Relationships
RELATIONSHIPS_DATA = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记—区长", "overlap_org": "中共兰山区委/兰山区政府", "overlap_period": "2023?-至今"},
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "区长—常务副区长", "overlap_org": "兰山区政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "区长—副区长", "overlap_org": "兰山区政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "区长—副区长", "overlap_org": "兰山区政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "区长—副区长", "overlap_org": "兰山区政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "区长—副区长", "overlap_org": "兰山区政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "区长—商城管委会", "overlap_org": "兰山区政府/商城", "overlap_period": "至今"},
    {"person_a": 3, "person_b": 5, "type": "同僚", "context": "常务副区长—副区长", "overlap_org": "兰山区政府", "overlap_period": "至今"},
    {"person_a": 3, "person_b": 6, "type": "同僚", "context": "常务副区长—副区长", "overlap_org": "兰山区政府", "overlap_period": "至今"},
    {"person_a": 3, "person_b": 7, "type": "同僚", "context": "常务副区长—副区长", "overlap_org": "兰山区政府", "overlap_period": "至今"},
    {"person_a": 3, "person_b": 8, "type": "同僚", "context": "常务副区长—副区长", "overlap_org": "兰山区政府", "overlap_period": "至今"},
    {"person_a": 5, "person_b": 6, "type": "同僚", "context": "副区长—副区长", "overlap_org": "兰山区政府", "overlap_period": "至今"},
    {"person_a": 6, "person_b": 7, "type": "同僚", "context": "副区长—副区长", "overlap_org": "兰山区政府", "overlap_period": "至今"},
    {"person_a": 7, "person_b": 8, "type": "同僚", "context": "副区长—副区长", "overlap_org": "兰山区政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "区长—办公室主任", "overlap_org": "兰山区政府", "overlap_period": "至今"},
]


# =========================================================================
# Build functions
# =========================================================================

def build_database():
    from gov_relation.runner import run_build
    run_build(
        slug=SLUG,
        persons=PERSONS_DATA,
        organizations=ORGANIZATIONS_DATA,
        positions=POSITIONS_DATA,
        relationships=RELATIONSHIPS_DATA,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

def build_gexf():
    """GEXF is already built by run_build, but we can also create additional detail."""
    pass

def write_person_json():
    """Write detailed person JSON files for key figures."""
    persons_detail = {
        2: {
            "name": "程凯",
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1977年4月",
            "birthplace": "",
            "native_place": "",
            "education": "大学学历",
            "party_join": "中共党员",
            "work_start": "",
            "current_post": "兰山区委副书记、区长",
            "current_org": "临沂市兰山区人民政府",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "sources": [
                {"id": "S001", "title": "兰山区人民政府 — 程凯领导简介", "url": "http://www.lyls.gov.cn/gk2/qzfld/ck.htm", "publisher": "兰山区人民政府", "published_at": "2026", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
                {"id": "S002", "title": "程凯到部分重点项目现场办公", "url": "http://www.lyls.gov.cn/info/1055/334841.htm", "publisher": "兰山区人民政府", "published_at": "2026-07-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
                {"id": "S003", "title": "全区大气污染防治重点工作调度会议召开", "url": "http://www.lyls.gov.cn/info/1055/334361.htm", "publisher": "兰山区人民政府", "published_at": "2026-07-23", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
            ],
            "career_entries": [],
            "confidence_summary": {
                "overall": "confirmed",
                "current_post": "confirmed",
                "basic_info": "confirmed",
                "career_history": "missing",
                "education": "confirmed",
            },
            "open_questions": [
                "程凯在担任兰山区区长之前的任职经历？",
                "程凯的籍贯和出生地？",
                "程凯的入党时间和参加工作年份？",
                "程凯何时被任命为代区长/区长？",
            ],
        },
        1: {
            "name": "刘波",
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": "",
            "party_join": "中共党员",
            "work_start": "",
            "current_post": "兰山区委书记",
            "current_org": "中共临沂市兰山区委员会",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "sources": [
                {"id": "S101", "title": "区委第四巡察组向区文联党组反馈巡察情况", "url": "http://www.lyls.gov.cn/", "publisher": "兰山区人民政府", "published_at": "2026-04-10", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
                {"id": "S102", "title": "刘波会见中科纳米产业集团客人", "url": "http://www.lyls.gov.cn/", "publisher": "兰山区人民政府", "published_at": "2026-04-25", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
            ],
            "career_entries": [],
            "confidence_summary": {
                "overall": "partial",
                "current_post": "confirmed",
                "basic_info": "missing",
                "career_history": "missing",
            },
            "open_questions": [
                "刘波的完整履历？",
                "刘波在担任区委书记前是否曾任兰山区区长？",
                "刘波的出生年月、籍贯、教育背景？",
            ],
        },
    }

    for pid, detail in persons_detail.items():
        p_data = next(p for p in PERSONS_DATA if p["id"] == pid)
        job_short = "区委书记" if "书记" in p_data["current_post"] and "副" not in p_data["current_post"].split("书记")[0] else "区长" if "区长" in p_data["current_post"] else p_data["current_post"].split("、")[0]
        
        person_json = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": PROV,
                "city": CITY,
                "region": REGION,
                "job": job_short,
                "task_id": TASK_ID,
                "time_focus": AS_OF,
            },
            "identity": {
                "person_id": f"lanshan_{detail['name']}",
                "name": detail["name"],
                "aliases": [],
                "gender": detail["gender"],
                "ethnicity": detail["ethnicity"],
                "birth": detail["birth"],
                "birthplace": detail["birthplace"],
                "native_place": detail["native_place"],
                "education": [],
                "party_join": detail["party_join"],
                "work_start": detail["work_start"],
                "dedupe_keys": {
                    "name_birth": f"{detail['name']}_{detail['birth']}",
                    "official_profile_url": detail["sources"][0]["url"],
                },
            },
            "current_status": {
                "current_post": detail["current_post"],
                "current_org": detail["current_org"],
                "administrative_rank": "县处级正职" if pid in (1, 2) else "县处级副职",
                "as_of": detail["as_of"],
                "is_current_confirmed": detail["is_current_confirmed"],
                "source_ids": [s["id"] for s in detail["sources"]],
            },
            "career_timeline": detail["career_entries"],
            "organizations": [],
            "relationships": [],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "数据不足，无法评估晋升速度", "notable_fast_promotions": []},
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "公开数据不足，无法评估工作风格",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": f"截至{AS_OF}，公开渠道未发现该人员的纪律处分、审计问题或负面报道",
                    "date": AS_OF,
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "source_register": detail["sources"],
            "confidence_summary": detail["confidence_summary"],
            "open_questions": detail["open_questions"],
        }

        filename = f"{AS_OF_SHORT}-{PROV}-{CITY}-{REGION}-{job_short}-{detail['name']}.json"
        filepath = PERSONS_OUT / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(person_json, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {filename}")


def main():
    print(f"\n{'='*60}")
    print(f"  {REGION} 领导班子工作关系网络 — 数据构建脚本")
    print(f"  As of: {AS_OF}")
    print(f"{'='*60}\n")

    print("[1/3] 构建数据库 + GEXF...")
    from gov_relation.runner import run_build
    run_build(
        slug=SLUG,
        persons=PERSONS_DATA,
        organizations=ORGANIZATIONS_DATA,
        positions=POSITIONS_DATA,
        relationships=RELATIONSHIPS_DATA,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print("[2/3] 写入人物 JSON...")
    write_person_json()

    print(f"\n{'='*60}")
    print(f"  构建完成！")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  JSON: {PERSONS_OUT}/")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
