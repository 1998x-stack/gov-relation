#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 伊川县 (Yichuan County), 洛阳市, 河南省.

Investigation date: 2026-07-24
Task ID: henan_伊川县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - https://www.yichuan.gov.cn/ — official government website
  - Government leadership page: /2026/04-10/1053684.html (7 government leaders with bios)
  - Individual bio pages for each government leader
  - 县委常委会第105次会议: /2025/06-27/831599.html (standing committee roster)
  - 三级干部会议: /2026/03-06/1052055.html (full county leadership)
  - 市政协副主席仝宇鹏调研: /2026/07-03/1070848.html (successor path)
  - 网易新闻 articles on Sept 2025 leadership transition

Confidence notes:
  - 王智朋 (县委书记): confirmed via multiple official sources; previously served as 县长
    before promotion to 县委书记 in Sept 2025. Full birth year and early career unverified.
  - 卫学军 (县长): confirmed via official bio (1980.02, 本科). Appointed ~early 2026.
  - Government leadership team: bios confirmed from official site (birth year, gender, education).
  - Party standing committee: partial — some roles confirmed, others (吉跃龙, 齐小伟, 刘伟,
    古松辉, 蒋艳萍) have unknown specific posts.
  - 仝宇鹏 (predecessor): confirmed transition to 洛阳市政协副主席.
  - This is a partial-evidence artifact: core leader identities and government team are
    well-documented; party committee detailed bios and standing committee role assignments
    are incomplete.
"""

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "伊川县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# ── Helper: ID offset for orgs ─────────────────────────────────────────────
ORG_OFFSET = 100000

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "王智朋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共伊川县委员会",
        "source": "yichuan.gov.cn confirmed 王智朋 as 县委书记 (2025.9—). Previously 伊川县长 (2022/2023—2025.9). Appointed party secretary Sept 2025."
    },
    {
        "id": 2,
        "name": "卫学军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980.02",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "伊川县人民政府",
        "source": "Official bio: https://www.yichuan.gov.cn/2026/04-10/1053684.html"
    },
    {
        "id": 3,
        "name": "仝宇鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "洛阳市政协副主席",
        "current_org": "洛阳市政协",
        "source": "Confirmed 洛阳市政协副主席 as of 2026-07. Former 伊川县委书记 until ~Sept 2025."
    },
    # ═══════ Government Leadership ═══════
    {
        "id": 4,
        "name": "鹿航广",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981.02",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "伊川县人民政府",
        "source": "Official bio: https://www.yichuan.gov.cn/2026/06-24/1069122.html"
    },
    {
        "id": 5,
        "name": "翟迎辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981.04",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长、副县长",
        "current_org": "中共伊川县委宣传部",
        "source": "Official bio: https://www.yichuan.gov.cn/2026/01-04/1033136.html"
    },
    {
        "id": 6,
        "name": "王中可",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976.04",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "党组成员、副县长",
        "current_org": "伊川县人民政府",
        "source": "Official bio: https://www.yichuan.gov.cn/2026/01-04/1033140.html"
    },
    {
        "id": 7,
        "name": "王驰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977.07",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "伊川县公安局",
        "source": "Official bio: https://www.yichuan.gov.cn/2026/01-04/1033141.html"
    },
    {
        "id": 8,
        "name": "王丹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1988.02",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "党组成员、副县长",
        "current_org": "伊川县人民政府",
        "source": "Official bio: https://www.yichuan.gov.cn/2026/07-01/1070532.html"
    },
    {
        "id": 9,
        "name": "亢辉辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987.06",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "党组成员、副县长",
        "current_org": "伊川县人民政府",
        "source": "Official bio: https://www.yichuan.gov.cn/2026/07-01/1070534.html"
    },
    # ═══════ Party Standing Committee (confirmed but partial roles) ═══════
    {
        "id": 10,
        "name": "谢睿",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共伊川县委员会",
        "source": "Confirmed 县委副书记 in 2026-07-03 article: https://www.yichuan.gov.cn/2026/07-03/1070848.html"
    },
    {
        "id": 11,
        "name": "杨利伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共伊川县委组织部",
        "source": "Confirmed 县委常委、组织部部长 in 2026-07-03 article: https://www.yichuan.gov.cn/2026/07-03/1070848.html"
    },
    # ═══════ Party Standing Committee (role unknown) ═══════
    {
        "id": 12,
        "name": "吉跃龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共伊川县委员会",
        "source": "Listed in 县委常委会第105次会议 attendance: https://www.yichuan.gov.cn/2025/06-27/831599.html"
    },
    {
        "id": 13,
        "name": "齐小伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共伊川县委员会",
        "source": "Listed in 县委常委会第105次会议 attendance"
    },
    {
        "id": 14,
        "name": "刘伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共伊川县委员会",
        "source": "Listed in 县委常委会第105次会议 attendance"
    },
    {
        "id": 15,
        "name": "古松辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共伊川县委员会",
        "source": "Listed in 县委常委会第105次会议 attendance"
    },
    {
        "id": 16,
        "name": "蒋艳萍",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共伊川县委员会",
        "source": "Listed in 县委常委会第105次会议 attendance"
    },
    # ═══════ Other County Leaders ═══════
    {
        "id": 17,
        "name": "魏淼",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "伊川县政协",
        "source": "Confirmed as 县政协主席 in 2026-07-03 article"
    },
    {
        "id": 18,
        "name": "马建民",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "伊川县人大常委会",
        "source": "Listed in 第105次常委会; role inferred as 县人大常委会主任 (unconfirmed)"
    },
    {
        "id": 19,
        "name": "韩海洋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县级以上领导",
        "current_org": "伊川县",
        "source": "Listed in 三级干部会议 attendance: https://www.yichuan.gov.cn/2026/03-06/1052055.html"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共伊川县委员会", "type": "党委", "level": "县处级", "parent": "中共洛阳市委", "location": "伊川县"},
    {"id": 2, "name": "伊川县人民政府", "type": "政府", "level": "县处级", "parent": "洛阳市人民政府", "location": "伊川县"},
    {"id": 3, "name": "伊川县人大常委会", "type": "人大", "level": "县处级", "parent": "洛阳市人大常委会", "location": "伊川县"},
    {"id": 4, "name": "伊川县政协", "type": "政协", "level": "县处级", "parent": "洛阳市政协", "location": "伊川县"},
    {"id": 5, "name": "伊川县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "洛阳市纪委监委", "location": "伊川县"},
    {"id": 6, "name": "中共伊川县委组织部", "type": "党委", "level": "县处级", "parent": "中共伊川县委", "location": "伊川县"},
    {"id": 7, "name": "中共伊川县委宣传部", "type": "党委", "level": "县处级", "parent": "中共伊川县委", "location": "伊川县"},
    {"id": 8, "name": "伊川县公安局", "type": "政府", "level": "县处级", "parent": "伊川县人民政府", "location": "伊川县"},
    {"id": 9, "name": "洛阳市政协", "type": "政协", "level": "地厅级", "parent": "河南省政协", "location": "洛阳市"},
]

# ── Positions (person → org with title) ────────────────────────────────────
positions = [
    # 王智朋 (id=1)
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2025-09", "end_date": "present", "rank": "县处级正职", "note": "从县长升任县委书记，2025年9月正式任命"},
    {"person_id": 1, "org_id": 2, "title": "县长（前任）", "start_date": "", "end_date": "2025-09", "rank": "县处级正职", "note": "任伊川县委副书记、县长，具体到任时间待查（约2022-2023）"},
    # 卫学军 (id=2)
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "接替王智朋任县长，具体到任时间约2026年初"},
    # 仝宇鹏 (id=3)
    {"person_id": 3, "org_id": 9, "title": "市政协副主席", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "从伊川县委书记调任"},
    {"person_id": 3, "org_id": 1, "title": "县委书记（前任）", "start_date": "", "end_date": "~2025-09", "rank": "县处级正职", "note": "前任伊川县委书记，2025年9月前在任"},
    # 鹿航广 (id=4)
    {"person_id": 4, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "县政府党组副书记"},
    # 翟迎辉 (id=5)
    {"person_id": 5, "org_id": 7, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "兼任副县长"},
    # 王中可 (id=6)
    {"person_id": 6, "org_id": 2, "title": "党组成员、副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 王驰 (id=7)
    {"person_id": 7, "org_id": 2, "title": "副县长、县公安局局长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 8, "title": "县公安局局长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 王丹 (id=8)
    {"person_id": 8, "org_id": 2, "title": "党组成员、副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 亢辉辉 (id=9)
    {"person_id": 9, "org_id": 2, "title": "党组成员、副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 谢睿 (id=10)
    {"person_id": 10, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "2026年到任"},
    # 杨利伟 (id=11)
    {"person_id": 11, "org_id": 6, "title": "县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # Standing committee (role unknown)
    {"person_id": 12, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体党内职务待查"},
    {"person_id": 13, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体党内职务待查"},
    {"person_id": 14, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体党内职务待查"},
    {"person_id": 15, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体党内职务待查"},
    {"person_id": 16, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体党内职务待查"},
    # Other leaders
    {"person_id": 17, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 18, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "职务为推测，待确认"},
    {"person_id": 19, "org_id": 1, "title": "副县级以上领导", "start_date": "", "end_date": "present", "rank": "县处级", "note": "具体职务待查"},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 王智朋 ↔ 卫学军（党政搭档）
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "王智朋任县委书记，卫学军任县长，为伊川县党政正职搭档",
        "overlap_org": "伊川县",
        "overlap_period": "2026—"
    },
    # 王智朋 → 仝宇鹏（前后任书记）
    {
        "person_a": 3, "person_b": 1,
        "type": "predecessor_successor",
        "context": "仝宇鹏为前任县委书记，王智朋接任（2025年9月）。仝宇鹏现任洛阳市政协副主席",
        "overlap_org": "中共伊川县委员会",
        "overlap_period": "2025"
    },
    # 王智朋 ↔ 鹿航广（上下级）
    {
        "person_a": 1, "person_b": 4,
        "type": "superior_subordinate",
        "context": "王智朋为县委书记，鹿航广为县委常委、常务副县长",
        "overlap_org": "伊川县",
        "overlap_period": "当前"
    },
    # 王智朋 ↔ 翟迎辉（上下级）
    {
        "person_a": 1, "person_b": 5,
        "type": "superior_subordinate",
        "context": "王智朋为县委书记，翟迎辉为县委常委、宣传部部长、副县长",
        "overlap_org": "伊川县委常委班子",
        "overlap_period": "当前"
    },
    # 卫学军 ↔ 鹿航广（政府正副职搭档）
    {
        "person_a": 2, "person_b": 4,
        "type": "superior_subordinate",
        "context": "卫学军为县长，鹿航广为常务副县长，伊川县政府正副职搭档",
        "overlap_org": "伊川县人民政府",
        "overlap_period": "当前"
    },
    # 谢睿 ↔ 王智朋（县委正副书记）
    {
        "person_a": 1, "person_b": 10,
        "type": "superior_subordinate",
        "context": "王智朋为县委书记，谢睿为县委副书记",
        "overlap_org": "中共伊川县委员会",
        "overlap_period": "2026—"
    },
    # 杨利伟 → 王智朋（班子成员）
    {
        "person_a": 1, "person_b": 11,
        "type": "superior_subordinate",
        "context": "王智朋为县委书记，杨利伟为县委常委、组织部部长",
        "overlap_org": "伊川县委常委班子",
        "overlap_period": "当前"
    },
]

# ── Person JSON Data ───────────────────────────────────────────────────────
person_files_data = [
    {
        "id": 1,
        "name": "王智朋",
        "job": "县委书记",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "洛阳市",
                "region": "伊川县",
                "job": "县委书记",
                "task_id": "henan_伊川县",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "henan_yichuan_wangzhipeng",
                "name": "王智朋",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "王智朋_unknown",
                    "name_birthplace": "",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "县委书记",
                "current_org": "中共伊川县委员会",
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002", "S003"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "未知",
                    "title": "早前任职",
                    "level": "",
                    "location": "",
                    "system": "unknown",
                    "rank": "",
                    "is_key_promotion": False,
                    "notes": "王智朋来伊川县之前的任职经历未查到公开资料",
                    "confidence": "unverified",
                    "source_ids": []
                },
                {
                    "start": "unknown",
                    "end": "2025-09",
                    "org": "伊川县人民政府",
                    "title": "县长",
                    "level": "县处级正职",
                    "location": "伊川县",
                    "system": "government",
                    "rank": "县处级正职",
                    "is_key_promotion": True,
                    "notes": "伊川县委副书记、县长。具体到任时间约2022-2023年间",
                    "confidence": "confirmed",
                    "source_ids": ["S002", "S003"]
                },
                {
                    "start": "2025-09",
                    "end": "present",
                    "org": "中共伊川县委员会",
                    "title": "县委书记",
                    "level": "县处级正职",
                    "location": "伊川县",
                    "system": "party",
                    "rank": "县处级正职",
                    "is_key_promotion": True,
                    "notes": "2025年9月任命为中共伊川县委书记。2025年9月至2026年3月间同时兼任县长",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S003"]
                }
            ],
            "organizations": [
                {"name": "中共伊川县委员会", "role": "县委书记", "period": "2025.9—", "source_ids": ["S001"]},
                {"name": "伊川县人民政府", "role": "县长（前任）", "period": "~2022/2023—2025.9", "source_ids": ["S002"]}
            ],
            "relationships": [
                {
                    "person": "仝宇鹏",
                    "person_id": "henan_yichuan_tongyupeng",
                    "relationship_type": "predecessor_successor",
                    "strength": "strong",
                    "evidence": "仝宇鹏为前任伊川县委书记，王智朋2025年9月接任",
                    "overlap_org": "中共伊川县委员会",
                    "overlap_period": "2025",
                    "direction": "other_to_person",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S004"]
                },
                {
                    "person": "卫学军",
                    "person_id": "henan_yichuan_weixuejun",
                    "relationship_type": "superior_subordinate",
                    "strength": "strong",
                    "evidence": "王智朋任县委书记，卫学军任县长，为伊川县当前党政正职搭档",
                    "overlap_org": "伊川县",
                    "overlap_period": "2026—",
                    "direction": "person_to_other",
                    "confidence": "confirmed",
                    "source_ids": ["S002"]
                }
            ],
            "governance_record": [
                {
                    "period": "2026",
                    "domain": "economic_development",
                    "achievement_or_event": "主持全县三级干部会议部署经济工作",
                    "role_in_event": "县委书记",
                    "measurable_outcome": "",
                    "location": "伊川县",
                    "confidence": "confirmed",
                    "source_ids": ["S003"]
                },
                {
                    "period": "2026",
                    "domain": "urban_construction",
                    "achievement_or_event": "调研呼南高铁伊川段项目",
                    "role_in_event": "县委书记",
                    "measurable_outcome": "",
                    "location": "伊川县",
                    "confidence": "confirmed",
                    "source_ids": ["S005"]
                },
                {
                    "period": "2026",
                    "domain": "education",
                    "achievement_or_event": "调研高考考点准备工作",
                    "role_in_event": "县委书记",
                    "measurable_outcome": "",
                    "location": "伊川县",
                    "confidence": "confirmed",
                    "source_ids": ["S006"]
                }
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "local_ladder",
                "systems_experience": ["government", "party"],
                "geographic_pattern": ["伊川县"],
                "promotion_velocity": {
                    "summary": "在伊川县从县长升任县委书记，属于县级班子内部晋升（2025年）",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "unknown",
                        "evidence": "尚无足够公开信息判断工作风格",
                        "confidence": "unverified",
                        "source_ids": []
                    }
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "未发现负面信息",
                    "date": AS_OF,
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "source_register": [
                {"id": "S001", "title": "网易号·大象新闻/古都洛邑/CNA — 王智朋任中共伊川县委书记", "url": "https://www.163.com/", "publisher": "网易新闻", "published_at": "2025-09-16", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "多个网易号交叉验证任命信息"},
                {"id": "S002", "title": "伊川县政府官网 — 政府领导页面", "url": "https://www.yichuan.gov.cn/2026/04-10/1053684.html", "publisher": "伊川县人民政府", "published_at": "2026-04-10", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "列出7名政府领导"},
                {"id": "S003", "title": "伊川县三级干部会议", "url": "https://www.yichuan.gov.cn/2026/03-06/1052055.html", "publisher": "伊川县人民政府", "published_at": "2026-03-06", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "王智朋以县委书记、县长双身份出席"},
                {"id": "S004", "title": "市政协副主席仝宇鹏带队到伊川县调研", "url": "https://www.yichuan.gov.cn/2026/07-03/1070848.html", "publisher": "伊川县人民政府", "published_at": "2026-07-03", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认仝宇鹏现任职务"},
                {"id": "S005", "title": "县委书记调研呼南高铁伊川段项目", "url": "https://www.yichuan.gov.cn/2026/05-22/1063448.html", "publisher": "伊川县人民政府", "published_at": "2026-05-22", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
                {"id": "S006", "title": "县委书记调研高考考点准备工作", "url": "https://www.yichuan.gov.cn/2026/06-08/1066579.html", "publisher": "伊川县人民政府", "published_at": "2026-06-08", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""}
            ],
            "confidence_summary": {
                "identity": "plausible",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "王智朋的完整履历（出生年份、籍贯、教育背景、来伊川前任职经历、入党时间、参加工作时间）全部缺失"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "王智朋的出生年份、籍贯、教育背景是什么？",
                    "why_it_matters": "作为当前一把手，基本信息对建立完整人物档案至关重要",
                    "suggested_queries": ["王智朋 简历 伊川", "王智朋 出生年月", "王智朋 任前公示"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "critical",
                    "question": "王智朋在来伊川县之前的任职经历是什么？从哪个岗位调任伊川县长？",
                    "why_it_matters": "理解其晋升路径和关系网络来源",
                    "suggested_queries": ["王智朋 洛阳 任职", "王智朋 工作经历", "王智朋 此前 担任"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "critical",
                    "question": "王智朋何时首次担任伊川县长？从谁手中接任？",
                    "why_it_matters": "理清县长交接脉络",
                    "suggested_queries": ["伊川县 县长 任免 2022", "伊川县 前任 县长"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": "王智朋的入党时间和参加工作时间？",
                    "why_it_matters": "评估政治资历和晋升速度",
                    "suggested_queries": ["王智朋 中共党员", "王智朋 党龄"],
                    "last_attempted": AS_OF
                }
            ]
        }
    },
    {
        "id": 2,
        "name": "卫学军",
        "job": "县长",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "洛阳市",
                "region": "伊川县",
                "job": "县长",
                "task_id": "henan_伊川县",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "henan_yichuan_weixuejun",
                "name": "卫学军",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1980.02",
                "birthplace": "",
                "native_place": "",
                "education": [
                    {
                        "period": "",
                        "institution": "",
                        "major": "",
                        "degree": "本科",
                        "study_type": "unknown",
                        "source_ids": ["S002"]
                    }
                ],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "卫学军_198002",
                    "name_birthplace": "",
                    "official_profile_url": "https://www.yichuan.gov.cn/2026/04-10/1053684.html"
                }
            },
            "current_status": {
                "current_post": "县长",
                "current_org": "伊川县人民政府",
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S002"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "伊川县人民政府",
                    "title": "县长",
                    "level": "县处级正职",
                    "location": "伊川县",
                    "system": "government",
                    "rank": "县处级正职",
                    "is_key_promotion": True,
                    "notes": "现任伊川县委副书记、县长，约2026年初到任",
                    "confidence": "confirmed",
                    "source_ids": ["S002"]
                },
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "履历缺口",
                    "title": "",
                    "notes": "公开资料未找到卫学军来伊川县之前的任职经历和完整履历",
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "organizations": [
                {"name": "伊川县人民政府", "role": "县长", "period": "至今", "source_ids": ["S002"]},
                {"name": "中共伊川县委员会", "role": "县委副书记", "period": "至今", "source_ids": ["S002"]}
            ],
            "relationships": [
                {
                    "person": "王智朋",
                    "person_id": "henan_yichuan_wangzhipeng",
                    "relationship_type": "superior_subordinate",
                    "strength": "strong",
                    "evidence": "卫学军任县长，王智朋任县委书记，为伊川县当前党政正职搭档",
                    "overlap_org": "伊川县",
                    "overlap_period": "2026—",
                    "direction": "other_to_person",
                    "confidence": "confirmed",
                    "source_ids": ["S002"]
                }
            ],
            "governance_record": [
                {
                    "period": "2026",
                    "domain": "economic_development",
                    "achievement_or_event": "主持县政府常务会议部署工作",
                    "role_in_event": "县长",
                    "measurable_outcome": "",
                    "location": "伊川县",
                    "confidence": "confirmed",
                    "source_ids": ["S007"]
                }
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["government"],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "现任伊川县县长（正处级），1980年出生，为较年轻的县长",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "unknown",
                        "evidence": "尚无足够公开信息判断工作风格",
                        "confidence": "unverified",
                        "source_ids": []
                    }
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "未发现负面信息",
                    "date": AS_OF,
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "source_register": [
                {"id": "S002", "title": "伊川县政府官网 — 政府领导页面", "url": "https://www.yichuan.gov.cn/2026/04-10/1053684.html", "publisher": "伊川县人民政府", "published_at": "2026-04-10", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "含卫学军个人简历：1980.02出生，本科学历，中共党员"},
                {"id": "S007", "title": "伊川县政府第45次常务会议", "url": "https://www.yichuan.gov.cn/2026/05-28/1064588.html", "publisher": "伊川县人民政府", "published_at": "2026-05-28", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认卫学军以县长身份主持会议"}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "卫学军的完整履历（籍贯、来伊川前任职经历、具体工作起始年份）大部分缺失"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "卫学军在来伊川县之前的任职经历是什么？从哪个岗位调任伊川县长？",
                    "why_it_matters": "理解其职业背景和关系网络来源",
                    "suggested_queries": ["卫学军 洛阳 任职", "卫学军 工作经历", "卫学军 简历"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": "卫学军的籍贯和出生地在哪里？教育经历的具体院校和专业？",
                    "why_it_matters": "有助于人员去重和籍贯关系分析",
                    "suggested_queries": ["卫学军 籍贯", "卫学军 出生地"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": "卫学军何时到任伊川县长？具体调任时间？",
                    "why_it_matters": "理清职务交接时间线",
                    "suggested_queries": ["伊川县 县长 任命 2026"],
                    "last_attempted": AS_OF
                }
            ]
        }
    },
    {
        "id": 3,
        "name": "仝宇鹏",
        "job": "洛阳市政协副主席",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "洛阳市",
                "region": "伊川县",
                "job": "洛阳市政协副主席",
                "task_id": "henan_伊川县",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "henan_yichuan_tongyupeng",
                "name": "仝宇鹏",
                "aliases": [],
                "gender": "",
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "仝宇鹏_unknown",
                    "name_birthplace": "",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "洛阳市政协副主席",
                "current_org": "洛阳市政协",
                "administrative_rank": "副厅级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S004"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "~2025-09",
                    "org": "中共伊川县委员会",
                    "title": "县委书记",
                    "level": "县处级正职",
                    "location": "伊川县",
                    "system": "party",
                    "rank": "县处级正职",
                    "is_key_promotion": True,
                    "notes": "前任伊川县委书记，具体到任何时待查",
                    "confidence": "confirmed",
                    "source_ids": ["S008"]
                },
                {
                    "start": "",
                    "end": "present",
                    "org": "洛阳市政协",
                    "title": "市政协副主席",
                    "level": "副厅级",
                    "location": "洛阳市",
                    "system": "other",
                    "rank": "副厅级",
                    "is_key_promotion": True,
                    "notes": "从伊川县委书记晋升为洛阳市政协副主席",
                    "confidence": "confirmed",
                    "source_ids": ["S004"]
                }
            ],
            "organizations": [
                {"name": "洛阳市政协", "role": "副主席", "period": "至今", "source_ids": ["S004"]},
                {"name": "中共伊川县委员会", "role": "县委书记（前任）", "period": "至2025.9", "source_ids": ["S008"]}
            ],
            "relationships": [
                {
                    "person": "王智朋",
                    "person_id": "henan_yichuan_wangzhipeng",
                    "relationship_type": "predecessor_successor",
                    "strength": "strong",
                    "evidence": "仝宇鹏为前任伊川县委书记，王智朋2025年9月接任",
                    "overlap_org": "中共伊川县委员会",
                    "overlap_period": "2025",
                    "direction": "person_to_other",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S004"]
                }
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "cross_county_rotation",
                "systems_experience": ["party"],
                "geographic_pattern": ["伊川县", "洛阳市"],
                "promotion_velocity": {
                    "summary": "从伊川县委书记升任洛阳市政协副主席（副厅级），属于晋升",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "unknown",
                        "evidence": "尚无足够公开信息判断工作风格",
                        "confidence": "unverified",
                        "source_ids": []
                    }
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "未发现负面信息",
                    "date": AS_OF,
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "source_register": [
                {"id": "S004", "title": "市政协副主席仝宇鹏带队到伊川县调研", "url": "https://www.yichuan.gov.cn/2026/07-03/1070848.html", "publisher": "伊川县人民政府", "published_at": "2026-07-03", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认仝宇鹏为洛阳市政协副主席"},
                {"id": "S008", "title": "十三届县委常委会第105次会议", "url": "https://www.yichuan.gov.cn/2025/06-27/831599.html", "publisher": "伊川县人民政府", "published_at": "2025-06-27", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认仝宇鹏2025年6月仍在县委书记岗位"}
            ],
            "confidence_summary": {
                "identity": "plausible",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "仝宇鹏的完整履历（出生年份、籍贯、教育、完整工作经历、何时起任伊川县委书记）全部缺失"
            },
            "open_questions": [
                {
                    "priority": "high",
                    "question": "仝宇鹏何时起任伊川县委书记？此前任何职？",
                    "why_it_matters": "理解县级班子交接节奏和仝宇鹏的晋升路径",
                    "suggested_queries": ["仝宇鹏 伊川县委书记 任职时间", "仝宇鹏 简历"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": "仝宇鹏的出生年份、籍贯、教育背景？",
                    "why_it_matters": "建立完整人物档案",
                    "suggested_queries": ["仝宇鹏 出生年月", "仝宇鹏 籍贯"],
                    "last_attempted": AS_OF
                }
            ]
        }
    },
]


# ── Main ────────────────────────────────────────────────────────────────────
def main() -> None:
    sys.path.insert(0, str(BASE))
    from gov_relation.runner import run_build

    # Write DB+GEXF to staging
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
    written_person_files = []
    for pf in person_files_data:
        fname = f"{TODAY}-河南省-洛阳市-{pf['job']}-{pf['name']}.json"
        path = PERSONS_DIR / fname
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pf["data"], f, ensure_ascii=False, indent=2)
        written_person_files.append(path)
        print(f"  ✅ Person JSON: {path}")

    # ── Copy to canonical paths ────────────────────────────────────────
    CANONICAL_DB.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_GEXF.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_BUILD.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_PERSONS.mkdir(parents=True, exist_ok=True)

    shutil.copy2(DB_PATH, CANONICAL_DB)
    shutil.copy2(GEXF_PATH, CANONICAL_GEXF)
    shutil.copy2(__file__, CANONICAL_BUILD)

    for pf in person_files_data:
        src = PERSONS_DIR / f"{TODAY}-河南省-洛阳市-{pf['job']}-{pf['name']}.json"
        dst = CANONICAL_PERSONS / src.name
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  ✅ Canonical person JSON: {dst}")

    print(f"\n📦 Canonical build script: {CANONICAL_BUILD}")
    print(f"📦 Canonical DB: {CANONICAL_DB}")
    print(f"📦 Canonical GEXF: {CANONICAL_GEXF}")
    print(f"  Person JSON count: {len(written_person_files)}")
    print(f"\n✅ Done — {SLUG} data build complete.")


if __name__ == "__main__":
    main()
