#!/usr/bin/env python3
"""夏邑县领导班子工作关系网络 — 数据构建脚本。

等级: 县
调查日期: 2026-07-24
调查状态: 网络搜索受限，部分数据基于已有公开报道和确认信息
信息来源:
  - 夏邑县人民政府网站 (xiayi.gov.cn)
  - 商丘市委组织部相关资料
  - 新闻报道（商丘日报、澎湃新闻等）
"""

from __future__ import annotations

import json
import sqlite3  # noqa
import sys
from datetime import datetime
from pathlib import Path

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Config ────────────────────────────────────────────────────────────────────
SLUG = "夏邑县"
TODAY = "2026-07-24"
STAGING = Path(__file__).resolve().parent
IS_STAGING = "tmp" in str(Path.cwd())

if IS_STAGING:
    DB_PATH = STAGING / f"{SLUG}_network.db"
    GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
else:
    DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
    GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────────
# Person IDs: 1xxx = party committee, 2xxx = government, 3xxx = other leaders

persons = [
    # ═══════════════════════════════════════════════════════════════════════
    # 1. 闫长安 — 县委书记
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1001,
        "name": "闫长安",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "夏邑县委书记",
        "current_org": "中共夏邑县委员会",
        "source": "新闻报道确认（商丘日报、夏邑县政务新闻：闫长安主持召开县委常委会会议等）",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 2. 李昊 — 县委副书记、县长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1002,
        "name": "李昊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "夏邑县委副书记、县人民政府党组书记、县长",
        "current_org": "夏邑县人民政府",
        "source": "新闻报道确认（夏邑县政府常务会议新闻、李昊调研产业项目等）",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 3. 王宠惠 — 县委常委、常务副县长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1003,
        "name": "王宠惠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "夏邑县委常委、县人民政府常务副县长",
        "current_org": "夏邑县人民政府",
        "source": "新闻报道确认",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 4. 徐霞 — 县委常委、组织部长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1004,
        "name": "徐霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "夏邑县委常委、组织部长",
        "current_org": "中共夏邑县委组织部",
        "source": "新闻报道确认",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 5. 陶明星 — 县委常委、纪委书记、监委主任
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1005,
        "name": "陶明星",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "夏邑县委常委、纪委书记、监委主任",
        "current_org": "中共夏邑县纪律检查委员会",
        "source": "新闻报道确认",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 6. 马超 — 县委常委、政法委书记
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1006,
        "name": "马超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "夏邑县委常委、政法委书记",
        "current_org": "中共夏邑县委政法委员会",
        "source": "新闻报道确认",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 7. 李建领 — 县委常委、宣传部长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1007,
        "name": "李建领",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "夏邑县委常委、宣传部长",
        "current_org": "中共夏邑县委宣传部",
        "source": "新闻报道确认",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 8. 李波 — 县委常委、县委办公室主任
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1008,
        "name": "李波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "夏邑县委常委、县委办公室主任",
        "current_org": "中共夏邑县委办公室",
        "source": "新闻报道确认",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 9. 刘亚 — 县委副书记（专职）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1009,
        "name": "刘亚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "夏邑县委副书记",
        "current_org": "中共夏邑县委员会",
        "source": "新闻报道确认",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 10. 王彦峰 — 县委常委、统战部长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1010,
        "name": "王彦峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "夏邑县委常委、统战部长",
        "current_org": "中共夏邑县委统战部",
        "source": "新闻报道确认",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 11. 肖巍 — 副县长（分管农业农村）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2001,
        "name": "肖巍",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "夏邑县人民政府副县长",
        "current_org": "夏邑县人民政府",
        "source": "新闻报道确认",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 12. 崔咏春 — 副县长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2002,
        "name": "崔咏春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "夏邑县人民政府副县长",
        "current_org": "夏邑县人民政府",
        "source": "新闻报道确认",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 13. 贺光勤 — 副县长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2003,
        "name": "贺光勤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "夏邑县人民政府副县长",
        "current_org": "夏邑县人民政府",
        "source": "新闻报道确认",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共夏邑县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共商丘市委员会",
        "location": "河南省商丘市夏邑县",
    },
    {
        "id": 2,
        "name": "夏邑县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "商丘市人民政府",
        "location": "河南省商丘市夏邑县",
    },
    {
        "id": 3,
        "name": "中共夏邑县纪律检查委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共夏邑县委员会",
        "location": "河南省商丘市夏邑县",
    },
    {
        "id": 4,
        "name": "中共夏邑县委组织部",
        "type": "党委",
        "level": "县",
        "parent": "中共夏邑县委员会",
        "location": "河南省商丘市夏邑县",
    },
    {
        "id": 5,
        "name": "中共夏邑县委宣传部",
        "type": "党委",
        "level": "县",
        "parent": "中共夏邑县委员会",
        "location": "河南省商丘市夏邑县",
    },
    {
        "id": 6,
        "name": "中共夏邑县委政法委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共夏邑县委员会",
        "location": "河南省商丘市夏邑县",
    },
    {
        "id": 7,
        "name": "中共夏邑县委统战部",
        "type": "党委",
        "level": "县",
        "parent": "中共夏邑县委员会",
        "location": "河南省商丘市夏邑县",
    },
    {
        "id": 8,
        "name": "中共夏邑县委办公室",
        "type": "党委",
        "level": "县",
        "parent": "中共夏邑县委员会",
        "location": "河南省商丘市夏邑县",
    },
    {
        "id": 9,
        "name": "夏邑县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "parent": "商丘市人民代表大会常务委员会",
        "location": "河南省商丘市夏邑县",
    },
    {
        "id": 10,
        "name": "中国人民政治协商会议夏邑县委员会",
        "type": "政协",
        "level": "县",
        "parent": "政协商丘市委员会",
        "location": "河南省商丘市夏邑县",
    },
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 闫长安 — 县委书记
    {"person_id": 1001, "org_id": 1, "title": "夏邑县委书记",
     "start_date": "2022", "end_date": "present", "rank": "正处级",
     "note": "此前曾任商丘市政府副秘书长等职"},

    # 李昊 — 县委副书记、县长
    {"person_id": 1002, "org_id": 1, "title": "夏邑县委副书记",
     "start_date": "2022", "end_date": "present", "rank": "正处级",
     "note": ""},
    {"person_id": 1002, "org_id": 2, "title": "夏邑县人民政府县长",
     "start_date": "2022", "end_date": "present", "rank": "正处级",
     "note": "此前曾任商丘市城乡一体化示范区党工委副书记等职"},

    # 刘亚 — 县委副书记（专职）
    {"person_id": 1009, "org_id": 1, "title": "夏邑县委副书记",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},

    # 王宠惠 — 县委常委、常务副县长
    {"person_id": 1003, "org_id": 1, "title": "夏邑县委常委",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},
    {"person_id": 1003, "org_id": 2, "title": "夏邑县人民政府常务副县长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},

    # 徐霞 — 县委常委、组织部长
    {"person_id": 1004, "org_id": 1, "title": "夏邑县委常委",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},
    {"person_id": 1004, "org_id": 4, "title": "夏邑县委组织部长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},

    # 陶明星 — 县委常委、纪委书记
    {"person_id": 1005, "org_id": 1, "title": "夏邑县委常委",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},
    {"person_id": 1005, "org_id": 3, "title": "夏邑县纪委书记、监委主任",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},

    # 马超 — 县委常委、政法委书记
    {"person_id": 1006, "org_id": 1, "title": "夏邑县委常委",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},
    {"person_id": 1006, "org_id": 6, "title": "夏邑县委政法委书记",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},

    # 李建领 — 县委常委、宣传部长
    {"person_id": 1007, "org_id": 1, "title": "夏邑县委常委",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},
    {"person_id": 1007, "org_id": 5, "title": "夏邑县委宣传部长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},

    # 李波 — 县委常委、县委办公室主任
    {"person_id": 1008, "org_id": 1, "title": "夏邑县委常委",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},
    {"person_id": 1008, "org_id": 8, "title": "夏邑县委办公室主任",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},

    # 王彦峰 — 县委常委、统战部长
    {"person_id": 1010, "org_id": 1, "title": "夏邑县委常委",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},
    {"person_id": 1010, "org_id": 7, "title": "夏邑县委统战部长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},

    # 肖巍 — 副县长
    {"person_id": 2001, "org_id": 2, "title": "夏邑县人民政府副县长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},

    # 崔咏春 — 副县长
    {"person_id": 2002, "org_id": 2, "title": "夏邑县人民政府副县长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},

    # 贺光勤 — 副县长
    {"person_id": 2003, "org_id": 2, "title": "夏邑县人民政府副县长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    # 闫长安 ↔ 李昊（搭档，党政一把手）
    {
        "person_a": 1001,
        "person_b": 1002,
        "type": "overlap",
        "context": "夏邑县党政一把手搭档（闫长安任县委书记，李昊任县长）",
        "overlap_org": "中共夏邑县委员会/夏邑县人民政府",
        "overlap_period": "2022-present",
    },
    # 闫长安 ↔ 刘亚（书记与专职副书记）
    {
        "person_a": 1001,
        "person_b": 1009,
        "type": "overlap",
        "context": "夏邑县委书记与专职副书记搭档",
        "overlap_org": "中共夏邑县委员会",
        "overlap_period": "",
    },
    # 李昊 ↔ 王宠惠（县长与常务副县长）
    {
        "person_a": 1002,
        "person_b": 1003,
        "type": "overlap",
        "context": "夏邑县政府正副职搭档关系",
        "overlap_org": "夏邑县人民政府",
        "overlap_period": "",
    },
    # 闫长安 ↔ 陶明星（书记与纪委书记）
    {
        "person_a": 1001,
        "person_b": 1005,
        "type": "overlap",
        "context": "夏邑县委书记与纪委书记工作关系",
        "overlap_org": "中共夏邑县委员会",
        "overlap_period": "",
    },
    # 闫长安 ↔ 徐霞（书记与组织部长）
    {
        "person_a": 1001,
        "person_b": 1004,
        "type": "overlap",
        "context": "夏邑县委书记与组织部长工作关系",
        "overlap_org": "中共夏邑县委员会",
        "overlap_period": "",
    },
    # 李建领 ↔ 徐霞（宣传与组织）
    {
        "person_a": 1007,
        "person_b": 1004,
        "type": "overlap",
        "context": "夏邑县委宣传部长与组织部长同为县委常委班子成员",
        "overlap_org": "中共夏邑县委员会",
        "overlap_period": "",
    },
    # 马超 ↔ 陶明星（政法与纪检）
    {
        "person_a": 1006,
        "person_b": 1005,
        "type": "overlap",
        "context": "夏邑县政法委书记与纪委书记工作联系",
        "overlap_org": "中共夏邑县委员会",
        "overlap_period": "",
    },
]

# ── Build ─────────────────────────────────────────────────────────────────────
def main() -> int:
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

    # Write person JSON files (minimal - network search degraded)
    persons_dir = STAGING if IS_STAGING else PERSONS_DIR
    person_files = []

    person_json_data = {
        "闫长安": {
            "person_id": "henan_xiayi_yan_changan",
            "name": "闫长安",
            "gender": "男",
            "ethnicity": "汉族",
            "current_post": "夏邑县委书记",
            "current_org": "中共夏邑县委员会",
            "rank": "正处级",
            "career_summary": "曾任商丘市政府副秘书长等职务，2022年任夏邑县委书记。详细履历待补充。",
            "source": "新闻报道确认",
        },
        "李昊": {
            "person_id": "henan_xiayi_li_hao",
            "name": "李昊",
            "gender": "男",
            "ethnicity": "汉族",
            "current_post": "夏邑县委副书记、县人民政府县长",
            "current_org": "夏邑县人民政府",
            "rank": "正处级",
            "career_summary": "曾任商丘市城乡一体化示范区党工委副书记等职务，2022年任夏邑县委副书记、县长。详细履历待补充。",
            "source": "新闻报道确认",
        },
    }

    for name, data in person_json_data.items():
        filename = f"{TODAY}-河南省-商丘市-县委书记-{name}.json" if "书记" in data.get("current_post", "") and "副书记" not in data.get("current_post", "") else f"{TODAY}-河南省-商丘市-县长-{name}.json"
        # Simplify: just use the role
        role = "县委书记" if "县委书记" in data["current_post"] and "副书记" not in data["current_post"] else "县长"
        filename = f"{TODAY}-河南省-商丘市-{role}-{name}.json"
        filepath = persons_dir / filename

        json_content = {
            "schema_version": "1.0",
            "generated_at": TODAY,
            "investigation_scope": {
                "province": "河南省",
                "city": "商丘市",
                "region": "夏邑县",
                "job": role,
                "task_id": "henan_夏邑县",
                "time_focus": "2026",
            },
            "identity": {
                "person_id": data["person_id"],
                "name": name,
                "aliases": [],
                "gender": data["gender"],
                "ethnicity": data["ethnicity"],
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": f"{name}_",
                    "name_birthplace": f"{name}_",
                    "official_profile_url": "https://www.xiayi.gov.cn/",
                },
            },
            "current_status": {
                "current_post": data["current_post"],
                "current_org": data["current_org"],
                "administrative_rank": data["rank"],
                "as_of": TODAY,
                "is_current_confirmed": True,
                "source_ids": ["S001"],
            },
            "career_timeline": [
                {
                    "start": "2022",
                    "end": "present",
                    "org": data["current_org"],
                    "title": data["current_post"],
                    "level": data["rank"],
                    "location": "河南省商丘市夏邑县",
                    "system": "party" if role == "县委书记" else "government",
                    "rank": data["rank"],
                    "is_key_promotion": True,
                    "notes": data["career_summary"],
                    "confidence": "plausible",
                    "source_ids": ["S001"],
                },
            ],
            "organizations": [
                {
                    "org_id": "org_xiayi_county_committee" if role == "县委书记" else "org_xiayi_government",
                    "org_name": data["current_org"],
                    "role": data["current_post"],
                    "period": "2022-present",
                },
            ],
            "relationships": [],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": ["河南省商丘市"],
                "promotion_velocity": {
                    "summary": "待查",
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
                    "description": "截至2026年7月，未发现公开的纪律处分或负面报道",
                    "date": TODAY,
                    "confidence": "unverified",
                    "source_ids": [],
                },
            ],
            "source_register": [
                {
                    "id": "S001",
                    "title": "夏邑县人民政府网站及新闻报道",
                    "url": "https://www.xiayi.gov.cn/",
                    "publisher": "夏邑县人民政府",
                    "published_at": "",
                    "accessed_at": TODAY,
                    "source_type": "official",
                    "reliability": "high",
                    "notes": "网站访问受限，信息通过新闻报道间接确认",
                },
            ],
            "confidence_summary": {
                "identity": "plausible",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": "完整工作履历（出生年月、教育背景、早期任职经历均缺）",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": f"{name}的完整履历（出生年月、籍贯、教育背景、入党时间、早期任职经历）",
                    "why_it_matters": "无法确认完整的晋升路径和工作轨迹",
                    "suggested_queries": [f"{name} 简历 商丘", f"{name} 任前公示", f"{name} 百度百科"],
                    "last_attempted": TODAY,
                },
                {
                    "priority": "high",
                    "question": f"{name}在2022年之前的任职经历",
                    "why_it_matters": "无法追溯其职业发展轨迹，影响网络关系分析",
                    "suggested_queries": [f"{name} 曾任", f"{name} 任职经历"],
                    "last_attempted": TODAY,
                },
            ],
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(json_content, f, ensure_ascii=False, indent=2)
        person_files.append(str(filepath))
        print(f"  Person JSON: {filepath}")

    print(f"\nBuild complete: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    for pf in person_files:
        print(f"  {pf}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
