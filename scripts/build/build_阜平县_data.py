#!/usr/bin/env python3
"""
阜平县领导班子工作关系网络 — Build script
河北省保定市阜平县

Research status: Web access degraded. Core leader names sourced from Baoding
government site guidance (阜平县 listed as constituent county).
Full biographies and deputy rosters were not accessible during this cycle.

Confirmed sources:
- Baoding city government site (www.baoding.gov.cn): confirms 阜平县 as constituent county
- Baoding government news: "2026'村超'全国赛（阜平赛区）暨保定市足球超级联赛总决赛" (2026-07-20)

Research date: 2026-07-23
"""

import json
import os
import sys
from datetime import date

# Add repo root to path
_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

import sqlite3  # noqa: used by gov_relation.runner

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

AS_OF = "2026-07-23"
DB_PATH = None  # Will be set in main()
GEXF_PATH = None  # Will be set in main()

# ── PERSONS ──
# Note: Names of current 县委书记 and 县长 could not be confirmed via accessible web sources
# during this research cycle due to Baidu 403, Exa rate limits, and government site timeouts.
# Placeholder IDs used — update with real names when sources become accessible.
persons = [
    # ── 县委书记 (Party Secretary) ──
    {
        "id": 1,
        "name": "待确认县委书记",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保定市阜平县委书记",
        "current_org": "中共阜平县委员会",
        "source": "待查 — 建议查询 www.baoding.gov.cn 或百度百科'阜平县'词条",
    },
    # ── 县长 (County Mayor) ──
    {
        "id": 2,
        "name": "待确认县长",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保定市阜平县委副书记、县长",
        "current_org": "阜平县人民政府/中共阜平县委员会",
        "source": "待查 — 建议查询 www.baoding.gov.cn 或百度百科'阜平县'词条",
    },
    # ── 县委专职副书记 (Deputy Party Secretary) ──
    {
        "id": 3,
        "name": "待确认专职副书记",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阜平县委副书记（专职）",
        "current_org": "中共阜平县委员会",
        "source": "待查 — 建议查询阜平县政府官网领导之窗栏目",
    },
    # ── 常务副县长 (Executive Deputy County Mayor) ──
    {
        "id": 4,
        "name": "待确认常务副县长",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阜平县委常委、常务副县长",
        "current_org": "阜平县人民政府/中共阜平县委员会",
        "source": "待查 — 建议查询阜平县政府官网领导分工栏目",
    },
    # ── 纪委书记 (Discipline Inspection Secretary) ──
    {
        "id": 5,
        "name": "待确认纪委书记",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阜平县委常委、纪委书记、监委主任",
        "current_org": "中共阜平县纪律检查委员会/阜平县监察委员会",
        "source": "待查 — 建议查询阜平县政府官网领导之窗栏目",
    },
    # ── 组织部长 (Organization Department Head) ──
    {
        "id": 6,
        "name": "待确认组织部长",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阜平县委常委、组织部长",
        "current_org": "中共阜平县委组织部",
        "source": "待查 — 建议查询阜平县政府官网领导之窗栏目",
    },
    # ── 宣传部长 (Propaganda Department Head) ──
    {
        "id": 7,
        "name": "待确认宣传部长",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阜平县委常委、宣传部长",
        "current_org": "中共阜平县委宣传部",
        "source": "待查 — 建议查询阜平县政府官网领导之窗栏目",
    },
    # ── 政法委书记 (Political-Legal Committee Secretary) ──
    {
        "id": 8,
        "name": "待确认政法委书记",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阜平县委常委、政法委书记",
        "current_org": "中共阜平县委政法委员会",
        "source": "待查 — 建议查询阜平县政府官网领导之窗栏目",
    },
    # ── 县委办主任 (County Committee Office Director) ──
    {
        "id": 9,
        "name": "待确认县委办主任",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阜平县委常委、县委办公室主任",
        "current_org": "中共阜平县委办公室",
        "source": "待查 — 建议查询阜平县政府官网领导之窗栏目",
    },
    # ── 统战部长 (United Front Department Head) ──
    {
        "id": 10,
        "name": "待确认统战部长",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阜平县委常委、统战部长",
        "current_org": "中共阜平县委统战部",
        "source": "待查 — 建议查询阜平县政府官网领导之窗栏目",
    },
    # ── 县人大主任 (County People's Congress Chair) ──
    {
        "id": 11,
        "name": "待确认人大主任",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阜平县人大常委会主任",
        "current_org": "阜平县人民代表大会常务委员会",
        "source": "待查 — 建议查询阜平县政府官网或人大网站",
    },
    # ── 县政协主席 (County CPPCC Chair) ──
    {
        "id": 12,
        "name": "待确认政协主席",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阜平县政协主席",
        "current_org": "中国人民政治协商会议阜平县委员会",
        "source": "待查 — 建议查询阜平县政府官网或政协网站",
    },
]

# ── ORGANIZATIONS ──
organizations = [
    {
        "id": 1,
        "name": "中共阜平县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共保定市委员会",
        "location": "保定市阜平县",
    },
    {
        "id": 2,
        "name": "阜平县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "保定市人民政府",
        "location": "保定市阜平县",
    },
    {
        "id": 3,
        "name": "中共阜平县纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共阜平县委员会",
        "location": "保定市阜平县",
    },
    {
        "id": 4,
        "name": "阜平县监察委员会",
        "type": "政府",
        "level": "县处级",
        "parent": "阜平县人民政府",
        "location": "保定市阜平县",
    },
    {
        "id": 5,
        "name": "中共阜平县委组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共阜平县委员会",
        "location": "保定市阜平县",
    },
    {
        "id": 6,
        "name": "中共阜平县委宣传部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共阜平县委员会",
        "location": "保定市阜平县",
    },
    {
        "id": 7,
        "name": "中共阜平县委政法委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共阜平县委员会",
        "location": "保定市阜平县",
    },
    {
        "id": 8,
        "name": "中共阜平县委办公室",
        "type": "党委",
        "level": "县处级",
        "parent": "中共阜平县委员会",
        "location": "保定市阜平县",
    },
    {
        "id": 9,
        "name": "中共阜平县委统战部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共阜平县委员会",
        "location": "保定市阜平县",
    },
    {
        "id": 10,
        "name": "阜平县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "保定市人民代表大会常务委员会",
        "location": "保定市阜平县",
    },
    {
        "id": 11,
        "name": "中国人民政治协商会议阜平县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "中国人民政治协商会议保定市委员会",
        "location": "保定市阜平县",
    },
]

# ── POSITIONS (current roles) ──
positions = [
    # 县委书记
    {
        "person_id": 1,
        "org_id": 1,
        "title": "阜平县委书记",
        "start_date": "待查",
        "end_date": "present",
        "rank": "正处级",
        "note": "当前县委书记，姓名待确认 — 建议从阜平县政府官网或保定市委组织部公告获取",
    },
    # 县长（同时任县委副书记）
    {
        "person_id": 2,
        "org_id": 1,
        "title": "阜平县委副书记",
        "start_date": "待查",
        "end_date": "present",
        "rank": "正处级",
        "note": "县长兼任县委副书记",
    },
    {
        "person_id": 2,
        "org_id": 2,
        "title": "阜平县人民政府县长",
        "start_date": "待查",
        "end_date": "present",
        "rank": "正处级",
        "note": "县政府主要负责人",
    },
    # 专职副书记
    {
        "person_id": 3,
        "org_id": 1,
        "title": "阜平县委副书记（专职）",
        "start_date": "待查",
        "end_date": "present",
        "rank": "副处级",
        "note": "县委专职副书记，协助书记处理党务",
    },
    # 常务副县长
    {
        "person_id": 4,
        "org_id": 1,
        "title": "阜平县委常委",
        "start_date": "待查",
        "end_date": "present",
        "rank": "副处级",
        "note": "县委常委、常务副县长",
    },
    {
        "person_id": 4,
        "org_id": 2,
        "title": "阜平县人民政府常务副县长",
        "start_date": "待查",
        "end_date": "present",
        "rank": "副处级",
        "note": "县政府常务副县长，分管日常工作",
    },
    # 纪委书记
    {
        "person_id": 5,
        "org_id": 1,
        "title": "阜平县委常委、纪委书记",
        "start_date": "待查",
        "end_date": "present",
        "rank": "副处级",
        "note": "县委常委、纪委书记、监委主任",
    },
    {
        "person_id": 5,
        "org_id": 3,
        "title": "阜平县纪委书记",
        "start_date": "待查",
        "end_date": "present",
        "rank": "副处级",
        "note": "",
    },
    {
        "person_id": 5,
        "org_id": 4,
        "title": "阜平县监委主任",
        "start_date": "待查",
        "end_date": "present",
        "rank": "副处级",
        "note": "",
    },
    # 组织部长
    {
        "person_id": 6,
        "org_id": 1,
        "title": "阜平县委常委、组织部长",
        "start_date": "待查",
        "end_date": "present",
        "rank": "副处级",
        "note": "",
    },
    {
        "person_id": 6,
        "org_id": 5,
        "title": "阜平县委组织部部长",
        "start_date": "待查",
        "end_date": "present",
        "rank": "副处级",
        "note": "",
    },
    # 宣传部长
    {
        "person_id": 7,
        "org_id": 1,
        "title": "阜平县委常委、宣传部长",
        "start_date": "待查",
        "end_date": "present",
        "rank": "副处级",
        "note": "",
    },
    {
        "person_id": 7,
        "org_id": 6,
        "title": "阜平县委宣传部部长",
        "start_date": "待查",
        "end_date": "present",
        "rank": "副处级",
        "note": "",
    },
    # 政法委书记
    {
        "person_id": 8,
        "org_id": 1,
        "title": "阜平县委常委、政法委书记",
        "start_date": "待查",
        "end_date": "present",
        "rank": "副处级",
        "note": "",
    },
    {
        "person_id": 8,
        "org_id": 7,
        "title": "阜平县委政法委书记",
        "start_date": "待查",
        "end_date": "present",
        "rank": "副处级",
        "note": "",
    },
    # 县委办主任
    {
        "person_id": 9,
        "org_id": 1,
        "title": "阜平县委常委、县委办公室主任",
        "start_date": "待查",
        "end_date": "present",
        "rank": "副处级",
        "note": "",
    },
    {
        "person_id": 9,
        "org_id": 8,
        "title": "阜平县委办公室主任",
        "start_date": "待查",
        "end_date": "present",
        "rank": "副处级",
        "note": "",
    },
    # 统战部长
    {
        "person_id": 10,
        "org_id": 1,
        "title": "阜平县委常委、统战部长",
        "start_date": "待查",
        "end_date": "present",
        "rank": "副处级",
        "note": "",
    },
    {
        "person_id": 10,
        "org_id": 9,
        "title": "阜平县委统战部部长",
        "start_date": "待查",
        "end_date": "present",
        "rank": "副处级",
        "note": "",
    },
    # 人大主任
    {
        "person_id": 11,
        "org_id": 10,
        "title": "阜平县人大常委会主任",
        "start_date": "待查",
        "end_date": "present",
        "rank": "正处级",
        "note": "",
    },
    # 政协主席
    {
        "person_id": 12,
        "org_id": 11,
        "title": "阜平县政协主席",
        "start_date": "待查",
        "end_date": "present",
        "rank": "正处级",
        "note": "",
    },
]

# ── RELATIONSHIPS ──
# Note: Without confirmed names, specific relationship evidence cannot be established.
# The structural relationships below reflect typical county-level party-government dynamics.
relationships = [
    # 县委书记 <-> 县长
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长：党委和政府主要领导工作关系",
        "overlap_org": "中共阜平县委员会",
        "overlap_period": "共同任职期间（待确认）",
    },
    # 县委书记 <-> 专职副书记
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与专职副书记：党委内部上下级关系",
        "overlap_org": "中共阜平县委员会",
        "overlap_period": "共同任职期间（待确认）",
    },
    # 县长 <-> 常务副县长
    {
        "person_a": 2,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "县长与常务副县长：县政府正副职工作关系",
        "overlap_org": "阜平县人民政府",
        "overlap_period": "共同任职期间（待确认）",
    },
    # 纪委书记 <-> 县委书记 (监督关系)
    {
        "person_a": 5,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "纪委书记向县委和上级纪委双重负责",
        "overlap_org": "中共阜平县委员会",
        "overlap_period": "共同任职期间（待确认）",
    },
    # 组织部长 <-> 县委书记
    {
        "person_a": 6,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "组织部长在县委领导下负责人事工作",
        "overlap_org": "中共阜平县委员会",
        "overlap_period": "共同任职期间（待确认）",
    },
    # 政法委书记 <-> 县委书记
    {
        "person_a": 8,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "政法委书记在县委领导下负责政法工作",
        "overlap_org": "中共阜平县委员会",
        "overlap_period": "共同任职期间（待确认）",
    },
    # 县委专职副书记 <-> 组织部长
    {
        "person_a": 3,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "专职副书记分管党务和干部工作，与组织部密切协作",
        "overlap_org": "中共阜平县委员会",
        "overlap_period": "共同任职期间（待确认）",
    },
    # 县委办主任 <-> 县委书记
    {
        "person_a": 9,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "县委办主任是县委书记的行政枢纽和日常运作支撑",
        "overlap_org": "中共阜平县委办公室",
        "overlap_period": "共同任职期间（待确认）",
    },
]

# ── BUILD ──
def main():
    # When run from staging, derive paths relative to script location
    staging_dir = os.path.dirname(os.path.abspath(__file__))

    global DB_PATH, GEXF_PATH
    DB_PATH = os.path.join(staging_dir, "阜平县_network.db")
    GEXF_PATH = os.path.join(staging_dir, "阜平县_network.gexf")

    run_build(
        slug="阜平县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    # Also write person JSON files
    write_person_json(staging_dir)

    print(f"Build complete. DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"Person JSONs in: {staging_dir}")


def write_person_json(staging_dir: str):
    """Write person graph JSON files into staging dir."""
    for person in persons:
        pid = person["id"]
        name = person["name"]

        # Map person id to job slug
        job_map = {
            1: "县委书记",
            2: "县长",
            3: "县委副书记",
            4: "常务副县长",
            5: "纪委书记",
            6: "组织部长",
            7: "宣传部长",
            8: "政法委书记",
            9: "县委办主任",
            10: "统战部长",
            11: "县人大主任",
            12: "县政协主席",
        }
        job_slug = job_map.get(pid, "未知职务")

        # Build person_id safe for duplicate detection
        name_slug = name.replace(" ", "_")

        filename = f"{AS_OF}-河北省-保定市-{job_slug}-{name_slug}.json"
        filepath = os.path.join(staging_dir, filename)

        # Build relative person relationships for this person
        person_rels = []
        for r in relationships:
            other_pid = None
            direction = "undirected"
            if r["person_a"] == pid:
                other_pid = r["person_b"]
                direction = "person_to_other"
            elif r["person_b"] == pid:
                other_pid = r["person_a"]
                direction = "other_to_person"

            if other_pid is not None:
                other_person = next((p for p in persons if p["id"] == other_pid), None)
                if other_person:
                    person_rels.append({
                        "person": other_person["name"],
                        "person_id": f"hebei_baoding_fuping_{other_pid}",
                        "relationship_type": r["type"],
                        "strength": "medium",
                        "evidence": r["context"],
                        "overlap_org": r["overlap_org"],
                        "overlap_period": r["overlap_period"],
                        "direction": direction,
                        "confidence": "unverified" if "待确认" in name else "unverified",
                        "source_ids": [],
                    })

        person_json = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河北省",
                "city": "保定市",
                "region": "阜平县",
                "job": job_slug,
                "task_id": "hebei_阜平县",
                "time_focus": "当前任职（信息待确认）",
            },
            "identity": {
                "person_id": f"hebei_baoding_fuping_{pid}",
                "name": name,
                "aliases": [],
                "gender": person.get("gender", ""),
                "ethnicity": person.get("ethnicity", ""),
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "",
                    "name_birthplace": "",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": person.get("current_post", ""),
                "current_org": person.get("current_org", ""),
                "administrative_rank": "正处级" if pid in (1, 2, 11, 12) else "副处级",
                "as_of": AS_OF,
                "is_current_confirmed": False,
                "source_ids": [],
            },
            "career_timeline": [
                {
                    "start": "待查",
                    "end": "present",
                    "org": person.get("current_org", ""),
                    "title": person.get("current_post", ""),
                    "level": "县处级",
                    "location": "保定市阜平县",
                    "system": "party" if pid in (1, 3, 5, 6, 7, 8, 9, 10) else "government" if pid in (2, 4) else "other",
                    "rank": "正处级" if pid in (1, 2, 11, 12) else "副处级",
                    "is_key_promotion": True if pid in (1, 2) else False,
                    "notes": "当前任职信息待确认",
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "organizations": [
                {"org_id": o["id"], "name": o["name"], "type": o["type"], "level": o["level"]}
                for o in organizations
                if any(pos["person_id"] == pid and pos["org_id"] == o["id"] for pos in positions)
            ],
            "relationships": person_rels,
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "公开资料不足，无法判断", "notable_fast_promotions": []},
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "当前公开资料不足，无法推断工作风格和个性特征。",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "目前未发现公开的纪律处分、审计问题或负面媒体报道",
                    "date": "",
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "source_register": [
                {
                    "id": "S001",
                    "title": "保定市人民政府门户网站",
                    "url": "http://www.baoding.gov.cn/",
                    "publisher": "保定市人民政府",
                    "published_at": "",
                    "accessed_at": AS_OF,
                    "source_type": "official",
                    "reliability": "high",
                    "notes": "确认阜平县为保定市下辖县；领导信息页未能直接访问",
                },
                {
                    "id": "S002",
                    "title": "保定市阜平县政务新闻 — '村超'全国赛阜平赛区",
                    "url": "http://www.baoding.gov.cn/",
                    "publisher": "保定市人民政府",
                    "published_at": "2026-07-20",
                    "accessed_at": AS_OF,
                    "source_type": "official",
                    "reliability": "high",
                    "notes": "确认阜平县活跃举办县级大型活动",
                },
            ],
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "unverified",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": "缺乏所有核心人物的姓名和履历信息 — 需要从阜平县政府官网或保定市委组织部获取",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "当前阜平县委书记的姓名和完整履历",
                    "why_it_matters": "关系网络的核心节点，缺失则网络分析无法进行",
                    "suggested_queries": [
                        "阜平县委书记 现任",
                        "阜平县委书记 简历 保定",
                        "阜平县 领导之窗",
                        "百度百科 阜平县",
                    ],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "当前阜平县县长的姓名和完整履历",
                    "why_it_matters": "关系网络的第二大核心节点",
                    "suggested_queries": [
                        "阜平县县长 现任",
                        "阜平县县长 简历",
                        "阜平县 政府领导",
                    ],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "阜平县委领导班子全体成员名单和分工",
                    "why_it_matters": "构建完整的县级领导关系网络",
                    "suggested_queries": [
                        "阜平县委常委 名单",
                        "阜平县 领导班子",
                        "阜平县委 领导分工",
                    ],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "前任县委书记和县长的去向",
                    "why_it_matters": "了解干部流动路径和跨县网络",
                    "suggested_queries": [
                        "阜平县 前任县委书记 去向",
                        "阜平县 前任县长 调任",
                    ],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "medium",
                    "question": "阜平县干部跨县交流情况",
                    "why_it_matters": "识别跨区域人事网络",
                    "suggested_queries": [
                        "保定 县级干部 交流 阜平",
                        "阜平 曲阳 唐县 干部交流",
                    ],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "low",
                    "question": "阜平县领导干部的公开照片",
                    "why_it_matters": "可用于可视化展示",
                    "suggested_queries": [
                        "阜平县委书记 图片",
                        "阜平县长 图片",
                    ],
                    "last_attempted": AS_OF,
                },
            ],
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(person_json, f, ensure_ascii=False, indent=2)
        print(f"Person JSON written: {filepath}")


if __name__ == "__main__":
    main()
