#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 西华县 (Xihua County), 周口市, 河南省.

Investigation date: 2026-07-25
Task ID: henan_西华县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - https://www.xihua.gov.cn/ — official government website
  - Government leadership page: /template/viewList?catalogId=... (8 government leaders with bios)
  - Individual bio pages for each government leader (潘建甫, 张权, 张超杰, 王超,
    张翠霞, 龙文钦, 马凯歌, 张瀚文)
  - 县委理论学习中心组集体学习（扩大）报告会: standing committee roster
  - 西华县第十五次党代会开幕: confirmed leadership lineup
  - 全县经济运行工作专题会议: leadership attendance
  - 全县污染防治攻坚工作推进会: leadership attendance

Confidence notes:
  - 马昭才 (县委书记): confirmed via multiple official sources; previously served as 县长
    before promotion to party secretary. Exact promotion date unknown (prior to 2026).
  - 潘建甫 (县长): confirmed via official bio (研究生学历, 汉族). Appointed as 县长.
  - Government leadership team: bios confirmed from official site (birth year, gender, education).
  - Party standing committee: partial — some roles confirmed, others have unknown specific posts.
  - This is a partial-evidence artifact: core leader identities and government team are
    well-documented; party committee detailed bios are incomplete.
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
SLUG = "西华县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

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
        "name": "马昭才",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共西华县委员会",
        "source": "xihua.gov.cn confirmed 马昭才 as 县委书记 (as of 2026). Previously 西华县长 before promotion to party secretary. Source: 全县污染防治攻坚工作推进会 (2026-07-18), 县第十五次党代会 (2026-06-24)."
    },
    {
        "id": 2,
        "name": "潘建甫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "西华县人民政府",
        "source": "Official bio: https://www.xihua.gov.cn/template/viewList?catalogId=4d1dc73cae054ded965ced288a1a1b19&id=s_4707369fb8cb4f3fba3ad7053eb26bab"
    },
    # ═══════ Government Leadership ═══════
    {
        "id": 3,
        "name": "张权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983.09",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "西华县人民政府",
        "source": "Official bio: https://www.xihua.gov.cn/template/viewList?catalogId=4d1dc73cae054ded965ced288a1a1b19&id=s_7017b606be6b41e08e66d8ef4a6a8a2f"
    },
    {
        "id": 4,
        "name": "张超杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981.08",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "西华县人民政府",
        "source": "Official bio: https://www.xihua.gov.cn/template/viewList?catalogId=4d1dc73cae054ded965ced288a1a1b19&id=s_a69a88cdae4940e9a5de3d75107ba37c"
    },
    {
        "id": 5,
        "name": "王超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972.09",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部长、副县长",
        "current_org": "中共西华县委宣传部",
        "source": "Official bio: https://www.xihua.gov.cn/template/viewList?catalogId=4d1dc73cae054ded965ced288a1a1b19&id=s_8ec40295ec0144a4950c1c14cf27c4e3"
    },
    {
        "id": 6,
        "name": "张翠霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1973.09",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "",  # 无党派人士
        "work_start": "",
        "current_post": "副县长",
        "current_org": "西华县人民政府",
        "source": "Official bio: https://www.xihua.gov.cn/template/viewList?catalogId=4d1dc73cae054ded965ced288a1a1b19&id=s_ca2708c078de48bfab021dbe407caa2a"
    },
    {
        "id": 7,
        "name": "龙文钦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969.12",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "西华县公安局",
        "source": "Official bio: https://www.xihua.gov.cn/template/viewList?catalogId=4d1dc73cae054ded965ced288a1a1b19&id=s_35861a8b8c8d4c42b893bb487fa89d95"
    },
    {
        "id": 8,
        "name": "马凯歌",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1985.06",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "西华县人民政府",
        "source": "Official bio: https://www.xihua.gov.cn/template/viewList?catalogId=4d1dc73cae054ded965ced288a1a1b19&id=s_db592ce1867046828354daa5e43e1be6"
    },
    {
        "id": 9,
        "name": "张瀚文",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1989.12",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "西华县人民政府",
        "source": "Official bio: https://www.xihua.gov.cn/template/viewList?catalogId=4d1dc73cae054ded965ced288a1a1b19&id=s_2003e00beeb94ec0aa40d90e6d31d7d6"
    },
    # ═══════ Party Standing Committee (confirmed roles) ═══════
    {
        "id": 10,
        "name": "李磊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共西华县委统战部",
        "source": "Confirmed in 全县污染防治攻坚工作推进会 (2026-07-18): 县委常委、统战部部长李磊"
    },
    {
        "id": 11,
        "name": "闫忠玉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共西华县委员会",
        "source": "Listed in 县第十五次党代会 (2026-06-24) as 大会执行主席"
    },
    {
        "id": 12,
        "name": "张雪芳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共西华县委员会",
        "source": "Attended 县委理论学习中心组集体学习（扩大）报告会 (2026-07-19) and 全县污染防治攻坚工作推进会 (2026-07-18)"
    },
    {
        "id": 13,
        "name": "冯保卫",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共西华县委员会",
        "source": "Attended 县委理论学习中心组集体学习（扩大）报告会 (2026-07-19) and 县第十五次党代会 (2026-06-24)"
    },
    {
        "id": 14,
        "name": "闵杰伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共西华县委员会",
        "source": "Attended 县委理论学习中心组集体学习（扩大）报告会 (2026-07-19) and 县第十五次党代会 (2026-06-24)"
    },
    {
        "id": 15,
        "name": "郑昊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共西华县委员会",
        "source": "Attended 县委理论学习中心组集体学习（扩大）报告会 (2026-07-19) and 全县污染防治攻坚工作推进会 (2026-07-18)"
    },
    {
        "id": 16,
        "name": "马灵钧",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共西华县委员会",
        "source": "Attended 全县污染防治攻坚工作推进会 (2026-07-18)"
    },
    # ═══════ Predecessor/Former Leaders ═══════
    {
        "id": 17,
        "name": "田庆杰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任县委书记",
        "current_org": "中共西华县委员会",
        "source": "Former 西华县委书记, predecessor to 马昭才. Exact timeline unverified."
    },
    # ═══════ Other County Leaders ═══════
    {
        "id": 18,
        "name": "李霞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "上级调研领导",
        "current_org": "",
        "source": "Visited 西华 for investigation: https://www.xihua.gov.cn/sitesources/xhxrmzf/page_pc/xwzx/xhyw/articlea80296f6423c4331a53ea3bc7a2671cb.html"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共西华县委员会", "type": "党委", "level": "县处级", "parent": "中共周口市委员会", "location": "西华县"},
    {"id": 2, "name": "西华县人民政府", "type": "政府", "level": "县处级", "parent": "周口市人民政府", "location": "西华县"},
    {"id": 3, "name": "西华县公安局", "type": "政府", "level": "乡科级", "parent": "西华县人民政府", "location": "西华县"},
    {"id": 4, "name": "中共西华县委宣传部", "type": "党委", "level": "乡科级", "parent": "中共西华县委员会", "location": "西华县"},
    {"id": 5, "name": "中共西华县委统战部", "type": "党委", "level": "乡科级", "parent": "中共西华县委员会", "location": "西华县"},
    {"id": 6, "name": "中共西华县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共西华县委员会", "location": "西华县"},
    {"id": 7, "name": "西华县人大常委会", "type": "人大", "level": "县处级", "parent": "", "location": "西华县"},
    {"id": 8, "name": "西华县政协", "type": "政协", "level": "县处级", "parent": "", "location": "西华县"},
    {"id": 9, "name": "西华县人民检察院", "type": "事业单位", "level": "县处级", "parent": "", "location": "西华县"},
    {"id": 10, "name": "西华县人民法院", "type": "事业单位", "level": "县处级", "parent": "", "location": "西华县"},
    {"id": 11, "name": "黄泛区农场", "type": "事业单位", "level": "县处级", "parent": "", "location": "西华县"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 马昭才
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "现任西华县委书记，此前曾任西华县长"},
    {"person_id": 1, "org_id": 2, "title": "县长（前任）", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "曾任西华县长，后升任县委书记"},
    # 潘建甫
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "现任西华县委副书记、县政府县长"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 张权
    {"person_id": 3, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "协助县长处理县政府常务工作"},
    # 张超杰
    {"person_id": 4, "org_id": 2, "title": "县委常委、副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责土地、住建、城管、市场监管"},
    # 王超
    {"person_id": 5, "org_id": 4, "title": "县委常委、宣传部长、副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责工信科技、商务、生态环境、交通运输"},
    # 张翠霞
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责卫生健康、疾病防控、医保医药、民政"},
    # 龙文钦
    {"person_id": 7, "org_id": 3, "title": "副县长、县公安局局长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责公安、司法、信访"},
    # 马凯歌
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责农业农村、乡村振兴、粮食、供销、民族宗教"},
    # 张瀚文
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责文旅文创、教育体育、退役军人"},
    # 李磊
    {"person_id": 10, "org_id": 5, "title": "县委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 闫忠玉
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待查"},
    # 张雪芳
    {"person_id": 12, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待查"},
    # 冯保卫
    {"person_id": 13, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待查"},
    # 闵杰伟
    {"person_id": 14, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待查"},
    # 郑昊
    {"person_id": 15, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待查"},
    # 马灵钧
    {"person_id": 16, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待查"},
    # 田庆杰（前任县委书记）
    {"person_id": 17, "org_id": 1, "title": "县委书记（前任）", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "前任西华县委书记"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # 党政正职关系
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记—县长搭档", "overlap_org": "西华县", "overlap_period": "2026—"},
    # 前任-继任关系
    {"person_a": 17, "person_b": 1, "type": "predecessor_successor", "context": "田庆杰为前任县委书记，马昭才接任", "overlap_org": "中共西华县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "马昭才升任县委书记后，潘建甫接任县长", "overlap_org": "西华县人民政府", "overlap_period": "2026—"},
    # 县委常委班子共事关系
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记与常务副县长", "overlap_org": "中共西华县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记与县委常委、副县长", "overlap_org": "中共西华县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委书记与县委常委、宣传部长", "overlap_org": "中共西华县委员会", "overlap_period": "present"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长与常务副县长", "overlap_org": "西华县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "县长与副县长", "overlap_org": "西华县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "县长与副县长", "overlap_org": "西华县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "县长与副县长", "overlap_org": "西华县人民政府", "overlap_period": "present"},
]


# ── Person JSON Data ──────────────────────────────────────────────────────
person_files_data = [
    {
        "id": 1,
        "name": "马昭才",
        "job": "县委书记",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "周口市",
                "region": "西华县",
                "job": "县委书记",
                "task_id": "henan_西华县",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "henan_xihua_mazhaocai",
                "name": "马昭才",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "马昭才_unknown",
                    "name_birthplace": "",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "县委书记",
                "current_org": "中共西华县委员会",
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002", "S003"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "西华县人民政府",
                    "title": "县长",
                    "level": "县处级正职",
                    "location": "西华县",
                    "system": "government",
                    "rank": "县处级正职",
                    "is_key_promotion": True,
                    "notes": "曾任西华县长，后升任县委书记",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                },
                {
                    "start": "unknown",
                    "end": "present",
                    "org": "中共西华县委员会",
                    "title": "县委书记",
                    "level": "县处级正职",
                    "location": "西华县",
                    "system": "party",
                    "rank": "县处级正职",
                    "is_key_promotion": True,
                    "notes": "现任西华县委书记，主持县委全面工作",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S002", "S003"]
                },
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "履历缺口",
                    "title": "",
                    "notes": "公开资料未找到马昭才的完整履历（出生年份、籍贯、教育背景、早期任职经历）",
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "organizations": [
                {"name": "中共西华县委员会", "role": "县委书记", "period": "至今", "source_ids": ["S001"]},
                {"name": "西华县人民政府", "role": "县长（前任）", "period": "前任", "source_ids": ["S001"]}
            ],
            "relationships": [
                {
                    "person": "潘建甫",
                    "person_id": "henan_xihua_panjianfu",
                    "relationship_type": "superior_subordinate",
                    "strength": "strong",
                    "evidence": "马昭才任县委书记，潘建甫任县长，为西华县当前党政正职搭档",
                    "overlap_org": "西华县",
                    "overlap_period": "2026—",
                    "direction": "other_to_person",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S003"]
                },
                {
                    "person": "田庆杰",
                    "person_id": "henan_xihua_tianqingjie",
                    "relationship_type": "predecessor_successor",
                    "strength": "strong",
                    "evidence": "田庆杰为前任西华县委书记，马昭才接任",
                    "overlap_org": "中共西华县委员会",
                    "overlap_period": "",
                    "direction": "other_to_person",
                    "confidence": "plausible",
                    "source_ids": []
                }
            ],
            "governance_record": [
                {
                    "period": "2026",
                    "domain": "economic_development",
                    "achievement_or_event": "主持全县经济运行工作专题会议，部署稳增长任务",
                    "role_in_event": "县委书记",
                    "measurable_outcome": "",
                    "location": "西华县",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                },
                {
                    "period": "2026",
                    "domain": "discipline",
                    "achievement_or_event": "主持污染防治攻坚工作推进会，强调责任落实",
                    "role_in_event": "县委书记",
                    "measurable_outcome": "",
                    "location": "西华县",
                    "confidence": "confirmed",
                    "source_ids": ["S003"]
                },
                {
                    "period": "2026",
                    "domain": "economic_development",
                    "achievement_or_event": "主持财经领导小组暨财源建设工作会议",
                    "role_in_event": "县委书记",
                    "measurable_outcome": "",
                    "location": "西华县",
                    "confidence": "confirmed",
                    "source_ids": ["S002"]
                },
                {
                    "period": "2026",
                    "domain": "other",
                    "achievement_or_event": "代表县委向县第十五次党代会作工作报告",
                    "role_in_event": "县委书记",
                    "measurable_outcome": "",
                    "location": "西华县",
                    "confidence": "confirmed",
                    "source_ids": ["S004"]
                }
            ],
            "professional_profile": {
                "primary_specializations": ["economic_development", "party_leadership"],
                "secondary_specializations": [],
                "career_pattern": "local_ladder",
                "systems_experience": ["party", "government"],
                "geographic_pattern": ["西华县"],
                "promotion_velocity": {
                    "summary": "从西华县长升任县委书记，符合县级党政正职晋升路径",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "pragmatic",
                        "evidence": "在财经领导小组会议上强调'抓财源就是抓发展，稳财源就是稳大局'，体现务实经济工作导向",
                        "confidence": "plausible",
                        "source_ids": ["S002"]
                    },
                    {
                        "trait": "discipline_oriented",
                        "evidence": "在污染防治推进会要求'对责任落实不到位的严肃追责问责，以铁的纪律倒逼责任落地'",
                        "confidence": "plausible",
                        "source_ids": ["S003"]
                    }
                ],
                "speech_themes": ["高质量发展", "项目建设", "财源建设", "污染防治攻坚"],
                "management_signals": ["精细化调度机制", "问题导向、目标导向、结果导向"],
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
                {"id": "S001", "title": "全县经济运行工作专题会议", "url": "https://www.xihua.gov.cn/sitesources/xhxrmzf/page_pc/xwzx/xhyw/articleb813940653c4421a8520f8c48374ce1d.html", "publisher": "西华县人民政府", "published_at": "2026-07-21", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认马昭才以县委书记身份出席会议"},
                {"id": "S002", "title": "马昭才主持召开财经领导小组暨财源建设工作会议", "url": "https://www.xihua.gov.cn/sitesources/xhxrmzf/page_pc/xwzx/xhyw/article4380bf441316430183a35804d90af41e.html", "publisher": "西华县人民政府", "published_at": "2026-07-17", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认马昭才为县委书记"},
                {"id": "S003", "title": "全县污染防治攻坚工作推进会", "url": "https://www.xihua.gov.cn/sitesources/xhxrmzf/page_pc/xwzx/xhyw/article71f2908f9f064538bcf28cc870463e9a.html", "publisher": "西华县人民政府", "published_at": "2026-07-18", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "马昭才以县委书记身份讲话，潘建甫以县长身份主持"},
                {"id": "S004", "title": "中国共产党西华县第十五次代表大会开幕", "url": "https://www.xihua.gov.cn/sitesources/xhxrmzf/page_pc/xwzx/tpxw/articlef860d9ee326a4b9db366daa9ad2f8246.html", "publisher": "西华县人民政府", "published_at": "2026-06-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "马昭才代表县委作工作报告"},
                {"id": "S005", "title": "县委理论学习中心组集体学习（扩大）报告会", "url": "https://www.xihua.gov.cn/sitesources/xhxrmzf/page_pc/xwzx/xhyw/article76863d8f43cc41d1833f4681ba9e89b3.html", "publisher": "西华县人民政府", "published_at": "2026-07-19", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认县委常委班子名单"}
            ],
            "confidence_summary": {
                "identity": "plausible",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "马昭才的完整履历（出生年份、籍贯、教育背景、早期任职经历、来西华前的工作经历）大部分缺失"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "马昭才的出生年份和籍贯是什么？",
                    "why_it_matters": "建立完整人物档案和人员去重",
                    "suggested_queries": ["马昭才 出生年月", "马昭才 简历", "马昭才 籍贯"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "critical",
                    "question": "马昭才何时担任西华县长？又何时升任县委书记？",
                    "why_it_matters": "理清职务交接时间线和晋升节奏",
                    "suggested_queries": ["马昭才 西华县长 任命", "马昭才 县委书记 任命"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": "马昭才在来西华县之前的工作经历是什么？",
                    "why_it_matters": "理解其职业背景和关系网络来源",
                    "suggested_queries": ["马昭才 周口 任职", "马昭才 工作经历"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": "马昭才的教育背景是什么？毕业于哪所院校？",
                    "why_it_matters": "完善人物档案信息",
                    "suggested_queries": ["马昭才 教育", "马昭才 学历"],
                    "last_attempted": AS_OF
                }
            ]
        }
    },
    {
        "id": 2,
        "name": "潘建甫",
        "job": "县长",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "周口市",
                "region": "西华县",
                "job": "县长",
                "task_id": "henan_西华县",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "henan_xihua_panjianfu",
                "name": "潘建甫",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [
                    {
                        "period": "",
                        "institution": "",
                        "major": "",
                        "degree": "研究生学历",
                        "study_type": "unknown",
                        "source_ids": ["S006"]
                    }
                ],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "潘建甫_unknown",
                    "name_birthplace": "",
                    "official_profile_url": "https://www.xihua.gov.cn/template/viewList?catalogId=4d1dc73cae054ded965ced288a1a1b19&id=s_4707369fb8cb4f3fba3ad7053eb26bab"
                }
            },
            "current_status": {
                "current_post": "县长",
                "current_org": "西华县人民政府",
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S006", "S003"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "present",
                    "org": "西华县人民政府",
                    "title": "县长",
                    "level": "县处级正职",
                    "location": "西华县",
                    "system": "government",
                    "rank": "县处级正职",
                    "is_key_promotion": True,
                    "notes": "现任西华县委副书记、县政府县长，主持县政府全面工作",
                    "confidence": "confirmed",
                    "source_ids": ["S006", "S003"]
                },
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "履历缺口",
                    "title": "",
                    "notes": "公开资料未找到潘建甫来西华县之前的任职经历和完整履历",
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "organizations": [
                {"name": "西华县人民政府", "role": "县长", "period": "至今", "source_ids": ["S006"]},
                {"name": "中共西华县委员会", "role": "县委副书记", "period": "至今", "source_ids": ["S006"]}
            ],
            "relationships": [
                {
                    "person": "马昭才",
                    "person_id": "henan_xihua_mazhaocai",
                    "relationship_type": "superior_subordinate",
                    "strength": "strong",
                    "evidence": "潘建甫任县长，马昭才任县委书记，为西华县当前党政正职搭档",
                    "overlap_org": "西华县",
                    "overlap_period": "2026—",
                    "direction": "person_to_other",
                    "confidence": "confirmed",
                    "source_ids": ["S003", "S006"]
                },
                {
                    "person": "张权",
                    "person_id": "henan_xihua_zhangquan",
                    "relationship_type": "overlap",
                    "strength": "strong",
                    "evidence": "张权任常务副县长，协助潘建甫处理县政府常务工作",
                    "overlap_org": "西华县人民政府",
                    "overlap_period": "present",
                    "direction": "person_to_other",
                    "confidence": "confirmed",
                    "source_ids": ["S007"]
                }
            ],
            "governance_record": [
                {
                    "period": "2026",
                    "domain": "economic_development",
                    "achievement_or_event": "主持县政府常务会议，部署安全生产和环保工作",
                    "role_in_event": "县长",
                    "measurable_outcome": "",
                    "location": "西华县",
                    "confidence": "confirmed",
                    "source_ids": ["S008"]
                },
                {
                    "period": "2026",
                    "domain": "other",
                    "achievement_or_event": "主持中国共产党西华县第十五次代表大会开幕式",
                    "role_in_event": "县长",
                    "measurable_outcome": "",
                    "location": "西华县",
                    "confidence": "confirmed",
                    "source_ids": ["S004"]
                }
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["government"],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "现任西华县县长（正处级），研究生学历",
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
                {"id": "S006", "title": "西华县政府官网 — 潘建甫领导信息", "url": "https://www.xihua.gov.cn/template/viewList?catalogId=4d1dc73cae054ded965ced288a1a1b19&id=s_4707369fb8cb4f3fba3ad7053eb26bab", "publisher": "西华县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "含潘建甫简历：研究生学历，中共党员，现任西华县委副书记、县政府县长"},
                {"id": "S007", "title": "西华县政府官网 — 张权领导信息", "url": "https://www.xihua.gov.cn/template/viewList?catalogId=4d1dc73cae054ded965ced288a1a1b19&id=s_7017b606be6b41e08e66d8ef4a6a8a2f", "publisher": "西华县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认张权协助县长处理县政府常务工作"},
                {"id": "S008", "title": "潘建甫主持召开县政府常务会议", "url": "https://www.xihua.gov.cn/sitesources/xhxrmzf/page_pc/xwzx/xhyw/article54227b1ccd844334956b7c11a5d67934.html", "publisher": "西华县人民政府", "published_at": "2026-07-16", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认潘建甫以县长身份主持县政府常务会议"},
                {"id": "S003", "title": "全县污染防治攻坚工作推进会", "url": "https://www.xihua.gov.cn/sitesources/xhxrmzf/page_pc/xwzx/xhyw/article71f2908f9f064538bcf28cc870463e9a.html", "publisher": "西华县人民政府", "published_at": "2026-07-18", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "潘建甫以县长身份主持会议"},
                {"id": "S004", "title": "中国共产党西华县第十五次代表大会开幕", "url": "https://www.xihua.gov.cn/sitesources/xhxrmzf/page_pc/xwzx/tpxw/articlef860d9ee326a4b9db366daa9ad2f8246.html", "publisher": "西华县人民政府", "published_at": "2026-06-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "潘建甫主持党代会开幕式"}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "潘建甫的完整履历（出生年份、籍贯、来西华前任职经历、具体工作起始年份）大部分缺失"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "潘建甫的出生年份和籍贯是什么？",
                    "why_it_matters": "建立完整人物档案和人员去重",
                    "suggested_queries": ["潘建甫 出生年月", "潘建甫 简历", "潘建甫 籍贯"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": "潘建甫在来西华县之前的任职经历是什么？从哪个岗位调任西华县长？",
                    "why_it_matters": "理解其职业背景和关系网络来源",
                    "suggested_queries": ["潘建甫 周口 任职", "潘建甫 工作经历"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": "潘建甫的具体教育经历（院校和专业）是什么？",
                    "why_it_matters": "有助于院校关系分析",
                    "suggested_queries": ["潘建甫 毕业院校"],
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
        fname = f"{TODAY}-河南省-周口市-{pf['job']}-{pf['name']}.json"
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
        src = PERSONS_DIR / f"{TODAY}-河南省-周口市-{pf['job']}-{pf['name']}.json"
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
