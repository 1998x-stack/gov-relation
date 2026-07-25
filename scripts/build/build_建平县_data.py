#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 建平县, 朝阳市, 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_建平县
Level: 县
Targets: 县委书记 & 县长

Research status: WEB ACCESS COMPLETELY DEGRADED
  - Exa API: rate-limited (free tier exhausted)
  - Baidu: 403 captcha block
  - Jina Reader: timeout
  - Official 建平县人民政府网站 (www.jianping.gov.cn): timeout / unreachable
  - Baidu Baike: timeout
  - Wikipedia: timeout
  - Google: block

No external web sources could be accessed. All names and details are marked as "待查"
(to be investigated). This script creates structurally valid artifacts with explicit
uncertainty, ready for data-fill when web access is restored.

Current officeholders (UNVERIFIED — from general knowledge of Liaoning cadres):
  - 县委书记: 待查（县委书记）
  - 县委副书记、县长: 待查（县长）

Known facts about 建平县:
  - 建平县 is a county under 朝阳市, 辽宁省
  - It is located in western Liaoning, bordering Inner Mongolia
  - The county government website is www.jianping.gov.cn

Person JSONs for the two core leaders also written alongside build.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
for parent_count in [3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # required by process_tmp validator

from gov_relation.runner import run_build
from gov_relation.paths import PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "建平县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
DB_PATH = _CURRENT_DIR / f"{SLUG}_network.db"
GEXF_PATH = _CURRENT_DIR / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    # ── 县委书记 ──
    {
        "id": 1,
        "name": "待查（县委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中国共产党建平县委员会",
        "source": "https://www.jianping.gov.cn/",
    },
    # ── 县委副书记、县长 ──
    {
        "id": 2,
        "name": "待查（县长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "建平县人民政府",
        "source": "https://www.jianping.gov.cn/",
    },
    # ── 其他县领导 —— 待查（待网络恢复后补充姓名和具体分工） ──
    {
        "id": 3,
        "name": "待查（常务副县长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "建平县人民政府",
        "source": "https://www.jianping.gov.cn/",
    },
    {
        "id": 4,
        "name": "待查（县纪委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中国共产党建平县纪律检查委员会",
        "source": "https://www.jianping.gov.cn/",
    },
    {
        "id": 5,
        "name": "待查（组织部部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中国共产党建平县委员会组织部",
        "source": "https://www.jianping.gov.cn/",
    },
    {
        "id": 6,
        "name": "待查（政法委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中国共产党建平县委员会政法委员会",
        "source": "https://www.jianping.gov.cn/",
    },
    {
        "id": 7,
        "name": "待查（宣传部部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中国共产党建平县委员会宣传部",
        "source": "https://www.jianping.gov.cn/",
    },
    {
        "id": 8,
        "name": "待查（副县长/公安局长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "建平县公安局",
        "source": "https://www.jianping.gov.cn/",
    },
    {
        "id": 9,
        "name": "待查（县人大常委会主任）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "建平县人民代表大会常务委员会",
        "source": "https://www.jianping.gov.cn/",
    },
    {
        "id": 10,
        "name": "待查（县政协主席）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议建平县委员会",
        "source": "https://www.jianping.gov.cn/",
    },
]

# ── Organizations ──────────────────────────────────────────────────────────────
organizations = [
    {"id": 0, "name": "中国共产党建平县委员会", "type": "党委", "level": "县处级",
     "parent": "中国共产党朝阳市委员会", "location": "辽宁省朝阳市建平县"},
    {"id": 1, "name": "建平县人民政府", "type": "政府", "level": "县处级",
     "parent": "朝阳市人民政府", "location": "辽宁省朝阳市建平县"},
    {"id": 2, "name": "建平县公安局", "type": "政府", "level": "乡科级",
     "parent": "建平县人民政府", "location": "辽宁省朝阳市建平县"},
    {"id": 3, "name": "中国共产党建平县纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中国共产党建平县委员会", "location": "辽宁省朝阳市建平县"},
    {"id": 4, "name": "中国共产党建平县委员会组织部", "type": "党委", "level": "乡科级",
     "parent": "中国共产党建平县委员会", "location": "辽宁省朝阳市建平县"},
    {"id": 5, "name": "中国共产党建平县委员会政法委员会", "type": "党委", "level": "乡科级",
     "parent": "中国共产党建平县委员会", "location": "辽宁省朝阳市建平县"},
    {"id": 6, "name": "中国共产党建平县委员会宣传部", "type": "党委", "level": "乡科级",
     "parent": "中国共产党建平县委员会", "location": "辽宁省朝阳市建平县"},
    {"id": 7, "name": "建平县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "", "location": "辽宁省朝阳市建平县"},
    {"id": 8, "name": "中国人民政治协商会议建平县委员会", "type": "政协", "level": "县处级",
     "parent": "", "location": "辽宁省朝阳市建平县"},
    {"id": 9, "name": "建平县人民政府办公室", "type": "政府", "level": "乡科级",
     "parent": "建平县人民政府", "location": "辽宁省朝阳市建平县"},
    {"id": 10, "name": "辽宁建平经济开发区管理委员会", "type": "开发区", "level": "",
     "parent": "建平县人民政府", "location": "辽宁省朝阳市建平县"},
]

# ── Positions ──────────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 0, "title": "县委书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "姓名待确认。建平县人民政府网站无法访问。"},
    {"person_id": 2, "org_id": 0, "title": "县委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 2, "org_id": 1, "title": "县长",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "县政府党组书记。姓名待确认。"},
    {"person_id": 3, "org_id": 0, "title": "县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 3, "org_id": 1, "title": "常务副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "县政府党组副书记，负责县政府常务工作。"},
    {"person_id": 4, "org_id": 0, "title": "县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 4, "org_id": 3, "title": "县纪委书记、县监委主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 5, "org_id": 0, "title": "县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 5, "org_id": 4, "title": "组织部部长",
     "start_date": "", "end_date": "present", "rank": "乡科级正职",
     "note": ""},
    {"person_id": 6, "org_id": 0, "title": "县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 6, "org_id": 5, "title": "政法委书记",
     "start_date": "", "end_date": "present", "rank": "乡科级正职",
     "note": ""},
    {"person_id": 7, "org_id": 0, "title": "县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 7, "org_id": 6, "title": "宣传部部长",
     "start_date": "", "end_date": "present", "rank": "乡科级正职",
     "note": ""},
    {"person_id": 8, "org_id": 1, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "县政府党组成员"},
    {"person_id": 8, "org_id": 2, "title": "县公安局局长",
     "start_date": "", "end_date": "present", "rank": "乡科级正职",
     "note": "县公安局党组书记、督察长"},
    {"person_id": 9, "org_id": 7, "title": "县人大常委会主任",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": ""},
    {"person_id": 10, "org_id": 8, "title": "县政协主席",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────────
relationships = [
    # 县委书记 - 县长：党政一把手搭档
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "县委书记与县长党政搭档",
     "overlap_org": "建平县", "overlap_period": ""},
    # 县委书记 - 人大主任
    {"person_a": 1, "person_b": 9, "type": "overlap",
     "context": "县委书记与人大常委会主任",
     "overlap_org": "建平县", "overlap_period": ""},
    # 县委书记 - 政协主席
    {"person_a": 1, "person_b": 10, "type": "overlap",
     "context": "县委书记与政协主席",
     "overlap_org": "建平县", "overlap_period": ""},
    # 县长 - 常务副县长
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "县长与常务副县长工作关系",
     "overlap_org": "建平县人民政府", "overlap_period": ""},
    # 县长 - 公安局长
    {"person_a": 2, "person_b": 8, "type": "overlap",
     "context": "县长与分管公安副县长",
     "overlap_org": "建平县人民政府", "overlap_period": ""},
    # 县委常委之间的同级关系
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "同为县委常委",
     "overlap_org": "建平县委常委班子", "overlap_period": ""},
    {"person_a": 3, "person_b": 5, "type": "overlap",
     "context": "同为县委常委",
     "overlap_org": "建平县委常委班子", "overlap_period": ""},
    {"person_a": 3, "person_b": 6, "type": "overlap",
     "context": "同为县委常委",
     "overlap_org": "建平县委常委班子", "overlap_period": ""},
    {"person_a": 3, "person_b": 7, "type": "overlap",
     "context": "同为县委常委",
     "overlap_org": "建平县委常委班子", "overlap_period": ""},
    {"person_a": 4, "person_b": 5, "type": "overlap",
     "context": "同为县委常委",
     "overlap_org": "建平县委常委班子", "overlap_period": ""},
    {"person_a": 4, "person_b": 6, "type": "overlap",
     "context": "同为县委常委",
     "overlap_org": "建平县委常委班子", "overlap_period": ""},
    {"person_a": 4, "person_b": 7, "type": "overlap",
     "context": "同为县委常委",
     "overlap_org": "建平县委常委班子", "overlap_period": ""},
    {"person_a": 5, "person_b": 6, "type": "overlap",
     "context": "同为县委常委",
     "overlap_org": "建平县委常委班子", "overlap_period": ""},
    {"person_a": 5, "person_b": 7, "type": "overlap",
     "context": "同为县委常委",
     "overlap_org": "建平县委常委班子", "overlap_period": ""},
    {"person_a": 6, "person_b": 7, "type": "overlap",
     "context": "同为县委常委",
     "overlap_org": "建平县委常委班子", "overlap_period": ""},
]


# ── Person JSON Helpers ────────────────────────────────────────────────────────

def write_person_json(person: dict, job: str, task_id: str) -> None:
    """Write a per-person graph JSON file into the staging directory."""
    name = person["name"]
    fname = f"{TODAY}-辽宁省-朝阳市-{job}-{name}.json"
    path = _CURRENT_DIR / fname
    source_id = "S001"

    is_unknown = "待查" in name

    profile = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "朝阳市",
            "region": "建平县",
            "job": job,
            "task_id": task_id,
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"jianping_{name}",
            "name": name,
            "aliases": [],
            "gender": "",
            "ethnicity": "汉族" if not is_unknown else "",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": f"{name}_",
                "name_birthplace": f"{name}_",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "县处级正职" if "书记" in person["current_post"] or "县长" in person["current_post"] else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": not is_unknown,
            "source_ids": [source_id]
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": person["current_org"],
                "title": person["current_post"],
                "level": "县处级",
                "location": "辽宁省朝阳市建平县",
                "system": "party" if "书记" in person["current_post"] and "副" not in person["current_post"] else "government",
                "rank": "县处级正职" if "书记" in person["current_post"] or "县长" in person["current_post"] else "县处级副职",
                "is_key_promotion": True,
                "notes": "因网络完全受限，当前职务无法确认。需恢复网络后查证。" if is_unknown else "网络完全受限，仅知当前职务。",
                "confidence": "unverified",
                "source_ids": [source_id]
            }
        ],
        "organizations": [],
        "relationships": [
            {
                "person": "待查（县长）" if job == "县委书记" else "待查（县委书记）",
                "person_id": "jianping_待查（县长）" if job == "县委书记" else "jianping_待查（县委书记）",
                "relationship_type": "overlap",
                "strength": "weak",
                "evidence": "县委书记与县长，党政主要负责人关系",
                "overlap_org": "中共建平县委员会/建平县人民政府",
                "overlap_period": "任期待查",
                "direction": "undirected",
                "confidence": "unverified",
                "source_ids": [source_id]
            }
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "",
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
        "risk_and_integrity_signals": [],
        "source_register": [
            {
                "id": source_id,
                "title": "建平县人民政府官方网站",
                "url": "https://www.jianping.gov.cn/",
                "publisher": "建平县人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "unreachable",
                "notes": "网站无法访问（超时）。多次尝试均失败。此外，Exa API rate-limited、百度 403 验证码、Jina Reader 超时、谷歌被屏蔽。所有外部网络搜索均不可用。"
            }
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "所有信息均未确认。因网络访问完全受限（政府网站、百度、谷歌、Exa均无法访问），县委书记、县长及领导班子全体成员的姓名、履历、关系等全部信息缺失。"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"建平县{job}的姓名",
                "why_it_matters": "核心领导人的身份信息是整个调查的基础",
                "suggested_queries": [
                    f"建平县 {person['current_post']} 现任",
                    f"建平县 领导之窗"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": f"建平县{job}的完整履历",
                "why_it_matters": "履历是关系网络分析的基础数据",
                "suggested_queries": [
                    f"建平县 {person['current_post']} 简历",
                    f"建平县 {person['current_post']} 任前公示"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": "能否通过朝阳市组织部任前公示查到建平县领导班子信息",
                "why_it_matters": "朝阳市网站可能比建平县本级网站更稳定",
                "suggested_queries": [
                    "朝阳市 组织部 任前公示 建平",
                    "朝阳市 人大 任命 建平 县长"
                ],
                "last_attempted": AS_OF
            }
        ]
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {path.name}")


# ── Main ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # 1. Build DB and GEXF via runner
    print(f"Building database and GEXF for {SLUG}...")
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

    # 2. Write person JSONs for core leaders
    print("Writing person JSONs...")
    write_person_json(persons[0], "县委书记", "liaoning_建平县")
    write_person_json(persons[1], "县长", "liaoning_建平县")

    print(f"\nDone. Files created in {_CURRENT_DIR}/")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
    print("  Person JSONs for 县委书记 and 县长")
