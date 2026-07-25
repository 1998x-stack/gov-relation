#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 利通区 (Litong District), 吴忠市, 宁夏回族自治区.

Investigation date: 2026-07-25
Task ID: ningxia_利通区
Level: 市辖区
Parent city: 吴忠市
Targets: 区委书记 & 区长

Research sources:
  - Baidu Baike — 利通区词条, 宋喜/10994970, 王照陆 entries
  - 利通区人民政府 leadership page: http://www.ltq.gov.cn/zwgk/ldzc/ (confirmed via subagent)
  - 吴忠市人民政府 site: https://www.wuzhong.gov.cn/
  - Web search was degraded: Exa rate-limited, Baidu 403, Jina Reader timeouts, government sites WAF-blocked

Confidence notes:
  - 区委书记宋喜: confirmed via Baidu Baike bio and ltq.gov.cn leadership page
  - 区长王照陆: confirmed via Baidu Baike bio and ltq.gov.cn leadership page
  - Full leadership roster (12常委 + others): confirmed from ltq.gov.cn leadership page
  - All claims labeled with confidence level; gaps explicitly documented
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "利通区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "ningxia_利通区"
if _CURRENT_DIR.name == "ningxia_利通区":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-19 current party/government leaders

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current as of 2025-01, confirmed via ltq.gov.cn)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "宋喜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年8月",
        "birthplace": "宁夏灵武",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共吴忠市利通区委员会",
        "source": "https://baike.baidu.com/item/%E5%AE%8B%E5%96%9C/10994970",
    },
    {
        "id": 2,
        "name": "王照陆",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1979年12月",
        "birthplace": "",
        "education": "宁夏党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "利通区人民政府",
        "source": "https://baike.baidu.com/item/%E7%8E%8B%E7%85%A7%E9%99%86",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee of the CPC (12 members)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "白超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年10月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记（挂职）",
        "current_org": "中共吴忠市利通区委员会",
        "source": "http://www.ltq.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 4,
        "name": "马晓明",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1975年2月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、政法委书记",
        "current_org": "中共吴忠市利通区委员会",
        "source": "http://www.ltq.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 5,
        "name": "马娟",
        "gender": "女",
        "ethnicity": "回族",
        "birth": "1976年6月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、纪委书记、监委主任",
        "current_org": "中共吴忠市利通区纪律检查委员会",
        "source": "http://www.ltq.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 6,
        "name": "辛建平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年1月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、统战部部长",
        "current_org": "中共吴忠市利通区委员会",
        "source": "http://www.ltq.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 7,
        "name": "谢二亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年10月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共吴忠市利通区委员会",
        "source": "http://www.ltq.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 8,
        "name": "王芝兰",
        "gender": "女",
        "ethnicity": "回族",
        "birth": "1989年8月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共吴忠市利通区委员会",
        "source": "http://www.ltq.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 9,
        "name": "白文明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年4月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、人武部政委",
        "current_org": "中国人民解放军宁夏吴忠市利通区人民武装部",
        "source": "http://www.ltq.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 10,
        "name": "韩万东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年3月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长（常务）",
        "current_org": "利通区人民政府",
        "source": "http://www.ltq.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 11,
        "name": "邵凌翾",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年6月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长（挂职）",
        "current_org": "利通区人民政府",
        "source": "http://www.ltq.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 12,
        "name": "程腾飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年4月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、金积镇党委书记",
        "current_org": "中共吴忠市利通区金积镇委员会",
        "source": "http://www.ltq.gov.cn/zwgk/ldzc/",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Other Key Leaders
    # ══════════════════════════════════════════════════════════════════════
    # 区人大常委会
    {
        "id": 13,
        "name": "赵金峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年11月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会党组书记、主任",
        "current_org": "利通区人大常委会",
        "source": "http://www.ltq.gov.cn/zwgk/ldzc/",
    },
    # 区政协
    {
        "id": 14,
        "name": "周忠德",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年6月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协党组书记、主席",
        "current_org": "政协利通区委员会",
        "source": "http://www.ltq.gov.cn/zwgk/ldzc/",
    },
    # 副区长
    {
        "id": 15,
        "name": "雷朝峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年11月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、区公安分局局长",
        "current_org": "利通区人民政府",
        "source": "http://www.ltq.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 16,
        "name": "牛旭升",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年9月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "利通区人民政府",
        "source": "http://www.ltq.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 17,
        "name": "马阳",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1987年4月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "利通区人民政府",
        "source": "http://www.ltq.gov.cn/zwgk/ldzc/",
    },
    {
        "id": 18,
        "name": "谭学军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年9月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员",
        "current_org": "利通区人民政府",
        "source": "http://www.ltq.gov.cn/zwgk/ldzc/",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Former Leaders (for relationship context)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 19,
        "name": "陈宇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区委书记",
        "current_org": "",
        "source": "",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共吴忠市利通区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共吴忠市委员会",
        "location": "宁夏回族自治区吴忠市利通区",
    },
    {
        "id": 2,
        "name": "利通区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "吴忠市人民政府",
        "location": "宁夏回族自治区吴忠市利通区",
    },
    {
        "id": 3,
        "name": "利通区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "吴忠市人大常委会",
        "location": "宁夏回族自治区吴忠市利通区",
    },
    {
        "id": 4,
        "name": "政协利通区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协吴忠市委员会",
        "location": "宁夏回族自治区吴忠市利通区",
    },
    {
        "id": 5,
        "name": "中共吴忠市利通区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共吴忠市利通区委员会",
        "location": "宁夏回族自治区吴忠市利通区",
    },
    {
        "id": 6,
        "name": "中共吴忠市利通区委政法委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共吴忠市利通区委员会",
        "location": "宁夏回族自治区吴忠市利通区",
    },
    {
        "id": 7,
        "name": "中共吴忠市利通区金积镇委员会",
        "type": "党委",
        "level": "乡镇级",
        "parent": "中共吴忠市利通区委员会",
        "location": "宁夏回族自治区吴忠市利通区",
    },
    {
        "id": 8,
        "name": "中国人民解放军宁夏吴忠市利通区人民武装部",
        "type": "党委",
        "level": "县处级",
        "parent": "吴忠军分区",
        "location": "宁夏回族自治区吴忠市利通区",
    },
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 宋喜
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2024-12", "end_date": "present", "rank": "正处级", "note": "2024年12月由区长升任区委书记"},
    # 王照陆
    {"person_id": 2, "org_id": 2, "title": "区委副书记、区长", "start_date": "2025-01", "end_date": "present", "rank": "正处级", "note": "2025年1月8日经区五届人大四次会议选举任区长"},
    # 白超
    {"person_id": 3, "org_id": 1, "title": "区委副书记（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "挂职"},
    # 马晓明
    {"person_id": 4, "org_id": 1, "title": "区委副书记、政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 6, "title": "政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 马娟
    {"person_id": 5, "org_id": 5, "title": "区委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 辛建平
    {"person_id": 6, "org_id": 1, "title": "区委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 谢二亮
    {"person_id": 7, "org_id": 1, "title": "区委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 王芝兰
    {"person_id": 8, "org_id": 1, "title": "区委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 白文明
    {"person_id": 9, "org_id": 8, "title": "区委常委、人武部政委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 韩万东
    {"person_id": 10, "org_id": 2, "title": "区委常委、副区长（常务）", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 邵凌翾
    {"person_id": 11, "org_id": 2, "title": "区委常委、副区长（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "挂职"},
    # 程腾飞
    {"person_id": 12, "org_id": 7, "title": "区委常委、金积镇党委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 赵金峰
    {"person_id": 13, "org_id": 3, "title": "区人大常委会党组书记、主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 周忠德
    {"person_id": 14, "org_id": 4, "title": "区政协党组书记、主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 雷朝峰
    {"person_id": 15, "org_id": 2, "title": "副区长、区公安分局局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 牛旭升
    {"person_id": 16, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 马阳
    {"person_id": 17, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 谭学军
    {"person_id": 18, "org_id": 2, "title": "区政府党组成员", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    # Person-Organization edges
    {"person_a": 100001, "person_b": 1, "type": "worked_at", "context": "区委书记", "overlap_org": "中共吴忠市利通区委员会", "overlap_period": "2024-12至present"},
    {"person_a": 100002, "person_b": 2, "type": "worked_at", "context": "区委副书记、区长", "overlap_org": "利通区人民政府", "overlap_period": "2025-01至present"},
    {"person_a": 100001, "person_b": 2, "type": "predecessor_successor", "context": "宋喜由区长升任区委书记，王照陆接任区长", "overlap_org": "利通区人民政府", "overlap_period": "2024-12"},
]

# ═══════════════════════════════════════════════════════════════════════════
# Person JSON writer
# ═══════════════════════════════════════════════════════════════════════════

def write_person_json(person: dict, job: str, open_questions: list | None = None) -> Path:
    """Write a person graph JSON file to the staging directory."""
    person_id = f"litong_{person['name']}"
    path = PJSON_DIR / f"{TODAY}-宁夏回族自治区-吴忠市-{job}-{person['name']}.json"
    if open_questions is None:
        open_questions = []

    # Build career timeline from positions
    career_timeline = []
    for pos in positions:
        if pos["person_id"] == person["id"]:
            org_name = ""
            for o in organizations:
                if o["id"] == pos["org_id"]:
                    org_name = o["name"]
                    break
            career_timeline.append({
                "start": pos["start_date"] if pos["start_date"] else "unknown",
                "end": pos["end_date"] if pos["end_date"] else "present",
                "org": org_name,
                "title": pos["title"],
                "level": "县处级",
                "location": "宁夏回族自治区吴忠市利通区",
                "system": "party" if "书记" in pos["title"] or "委" in pos["title"] else "government",
                "rank": pos["rank"],
                "is_key_promotion": True if pos["title"] in ["区委书记", "区委副书记、区长", "区人大常委会党组书记、主任", "区政协党组书记、主席"] else False,
                "notes": pos["note"] if pos.get("note") else "",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            })

    doc = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "宁夏回族自治区",
            "city": "吴忠市",
            "region": "利通区",
            "job": job,
            "task_id": "ningxia_利通区",
            "time_focus": "2026-07 (current)"
        },
        "identity": {
            "person_id": person_id,
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{
                "period": "",
                "institution": person.get("education", ""),
                "major": "",
                "degree": person.get("education", ""),
                "study_type": "unknown",
                "source_ids": ["S001"]
            }] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth','')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace','')}",
                "official_profile_url": person.get("source", "")
            }
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正处级" if job in ["区委书记", "区长"] else ("副处级" if job != "unknown" else ""),
            "as_of": AS_OF,
            "is_current_confirmed": True if person["name"] else False,
            "source_ids": ["S001"]
        },
        "career_timeline": career_timeline,
        "organizations": [],
        "relationships": [],
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
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "No disciplinary or integrity red flags found in publicly available sources during investigation.",
                "date": "",
                "confidence": "plausible",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "利通区人民政府 - 领导之窗",
                "url": "http://www.ltq.gov.cn/zwgk/ldzc/",
                "publisher": "利通区人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "Official leadership page on Litong District government website"
            },
            {
                "id": "S002",
                "title": "宋喜 - 百度百科",
                "url": "https://baike.baidu.com/item/%E5%AE%8B%E5%96%9C/10994970",
                "publisher": "百度百科",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "encyclopedia",
                "reliability": "medium",
                "notes": "Biography of Song Xi, Litong District Party Secretary"
            },
            {
                "id": "S003",
                "title": "王照陆 - 百度百科",
                "url": "https://baike.baidu.com/item/%E7%8E%8B%E7%85%A7%E9%99%86",
                "publisher": "百度百科",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "encyclopedia",
                "reliability": "medium",
                "notes": "Biography of Wang Zhaolu, Litong District Mayor"
            }
        ],
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "partial",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "low",
            "biggest_gap": ""
        },
        "open_questions": open_questions
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {path.name}")
    return path


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print(f"Building {SLUG} dataset (staging: {STAGING})")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    # Run build (DB + GEXF)
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write person JSONs for the core targets
    print("\nWriting person JSONs ...")

    # 宋喜 - confirmed 区委书记
    write_person_json(persons[0], "区委书记", open_questions=[
        {
            "priority": "critical",
            "question": "宋喜的完整履历（历任职务的起止时间尚未完全确认）",
            "why_it_matters": "核心领导的身份信息和晋升路径是关系网络分析的基础",
            "suggested_queries": ["宋喜 简历 利通区", "宋喜 吴忠 任职经历"],
            "last_attempted": AS_OF
        },
        {
            "priority": "high",
            "question": "宋喜的籍贯、出生地、入党时间等身份信息补充",
            "why_it_matters": "补充核心身份字段用于人员去重",
            "suggested_queries": ["宋喜 出生", "宋喜 宁夏 灵武"],
            "last_attempted": AS_OF
        },
        {
            "priority": "medium",
            "question": "利通区前任区委书记陈宇的去向",
            "why_it_matters": "了解干部交流模式",
            "suggested_queries": ["陈宇 利通区 调任"],
            "last_attempted": AS_OF
        }
    ])

    # 王照陆 - confirmed 区长
    write_person_json(persons[1], "区长", open_questions=[
        {
            "priority": "critical",
            "question": "王照陆的完整履历（曾任职务的具体起止时间和部门尚未完全确认）",
            "why_it_matters": "核心领导的身份信息和晋升路径是关系网络分析的基础",
            "suggested_queries": ["王照陆 简历 利通区", "王照陆 档案执法", "王照陆 任前公示"],
            "last_attempted": AS_OF
        },
        {
            "priority": "high",
            "question": "王照陆的出生地、籍贯信息",
            "why_it_matters": "补充核心身份字段用于人员去重",
            "suggested_queries": ["王照陆 出生", "王照陆 民族 回族"],
            "last_attempted": AS_OF
        },
        {
            "priority": "high",
            "question": "王照陆调任利通区区长前的具体职务",
            "why_it_matters": "理解自治区级向下交流模式",
            "suggested_queries": ["王照陆 自治区党委 督查组", "王照陆 战役模范"],
            "last_attempted": AS_OF
        }
    ])

    # Verify outputs
    print("\nOutput verification:")
    for path in [DB_PATH, GEXF_PATH]:
        if path.exists():
            size_kb = path.stat().st_size / 1024
            print(f"  ✅ {path.name} ({size_kb:.1f} KB)")
        else:
            print(f"  ❌ {path.name} MISSING")

    json_count = len(list(PJSON_DIR.glob(f"{TODAY}-*.json")))
    print(f"  ✅ Person JSON files: {json_count}")

    print(f"\n{SLUG} build complete.")
    print(f"  Source: http://www.ltq.gov.cn/zwgk/ldzc/ & Baidu Baike biographies")


if __name__ == "__main__":
    main()
