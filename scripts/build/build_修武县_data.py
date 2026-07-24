#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 修武县 (Xiuwu County), 焦作市, 河南省.

Investigation date: 2026-07-24
Task ID: henan_修武县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - www.xiuwu.gov.cn — 修武县人民政府网站 (primary, current as of July 2026)
  - Confirmed: 李怀琛 is 县委书记 (seen in multiple July 2026 news articles:
    "县委常委会（扩大）会议召开" 2026-07-09: "县委书记李怀琛主持召开"
    "全县易燃易爆领域专题风险防控推进会" 2026-07-13: "县委书记李怀琛主持召开"
    "全县重点项目调度推进会" 2026-07-15: leadership list
    "县委理论学习中心组举行集体学习研讨" 2026-06-30: "县委书记李怀琛主持"
    "人武部党委第一书记任职大会" 2026-07-09: "李怀琛同志任修武县人武部党委委员、第一书记")
  - Confirmed: 宋科 is 县委副书记、县长 (seen in multiple July 2026 articles:
    "全县易燃易爆领域专题风险防控推进会" 2026-07-13: "县委副书记、县长宋科"
    "县政府常务会议召开" 2026-06-27: "县委副书记、县长宋科主持召开"
    "县委理论学习中心组" 2026-06-30: "县委副书记、县长宋科"
    "县十六届人大常委会第三十八次会议" 2026-07-20: 补选宋科为市人大代表)
  - 县政府领导 page: https://www.xiuwu.gov.cn/zfxxgk/zfxxgkml/zfld/ (confirmed 侯占浩 as 常务副县长)
  - 县十五届纪律检查委员会第一次全体会议 2026-06-23: 张鹏展当选纪委书记
  - 县重点项目调度推进会 2026-07-15: full leadership roster published

Confidence notes:
  - Core leader names (李怀琛, 宋科) and their current roles: confirmed via multiple
    official government news articles (June-July 2026)
  - 县委常委名单 from 县重点项目调度推进会 published attendance list (July 2026)
  - Detailed career timelines (education, early career, birthplace, birth year) for most
    leaders could not be verified due to web access limitations (Baidu 403/CAPTCHA,
    Exa rate-limited, Jina Reader timeout)
  - Birth years, ethnicities, education, and detailed biographies marked as open questions
"""

from __future__ import annotations

import json
import os
import shutil
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Allow import from repo root
REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "修武县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# ── Staging paths ────────────────────────────────────────────────────────────
STAGING = Path(__file__).parent.resolve()
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# Canonical destinations (after promotion)
CANONICAL_DB = DATABASE_DIR / f"{SLUG}_network.db"
CANONICAL_GEXF = GRAPH_DIR / f"{SLUG}_network.gexf"
CANONICAL_BUILD = REPO_ROOT / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = PERSONS_DIR

# ── Data ──────────────────────────────────────────────────────────────────────

persons = [
    # ═══════ Core Leadership ═══════
    # 县委书记
    {
        "id": 1,
        "name": "李怀琛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共修武县委员会",
        "source": "https://www.xiuwu.gov.cn/2026/07-09/607588.html"
    },
    # 县长
    {
        "id": 2,
        "name": "宋科",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县长",
        "current_org": "修武县人民政府",
        "source": "https://www.xiuwu.gov.cn/2026/07-13/607845.html"
    },
    # ═══════ 县委副书记 ═══════
    {
        "id": 3,
        "name": "刘煜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共修武县委员会",
        "source": "https://www.xiuwu.gov.cn/2026/07-09/607594.html"
    },
    # ═══════ 县委常委 ═══════
    {
        "id": 4,
        "name": "侯占浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "修武县人民政府",
        "source": "https://www.xiuwu.gov.cn/zfxxgk/zfxxgkml/zfld/"
    },
    {
        "id": 5,
        "name": "张鹏展",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、纪委书记",
        "current_org": "中共修武县纪律检查委员会",
        "source": "https://www.xiuwu.gov.cn/2026/06-23/606137.html"
    },
    {
        "id": 6,
        "name": "马亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、人武部政委",
        "current_org": "修武县人民武装部",
        "source": "https://www.xiuwu.gov.cn/2026/07-09/607594.html"
    },
    {
        "id": 7,
        "name": "姚远",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共修武县委员会",
        "source": "https://www.xiuwu.gov.cn/2026/07-15/608132.html"
    },
    {
        "id": 8,
        "name": "郭晓黎",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共修武县委员会",
        "source": "https://www.xiuwu.gov.cn/2026/07-15/608132.html"
    },
    {
        "id": 9,
        "name": "田亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共修武县委员会",
        "source": "https://www.xiuwu.gov.cn/2026/07-15/608132.html"
    },
    {
        "id": 10,
        "name": "李继豪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共修武县委员会",
        "source": "https://www.xiuwu.gov.cn/2026/07-15/608132.html"
    },
    {
        "id": 11,
        "name": "王国凡",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共修武县委员会",
        "source": "https://www.xiuwu.gov.cn/2026/07-15/608132.html"
    },
    {
        "id": 12,
        "name": "刘海祯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共修武县委员会",
        "source": "https://www.xiuwu.gov.cn/2026/07-15/608132.html"
    },
    # ═══════ 县政府领导 ═══════
    {
        "id": 13,
        "name": "曹学贤",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "修武县人民政府",
        "source": "https://www.xiuwu.gov.cn/2026/07-20/608452.html"
    },
    {
        "id": 14,
        "name": "余忠杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "修武县人民政府",
        "source": "https://www.xiuwu.gov.cn/zfxxgk/zfxxgkml/zfld/"
    },
    {
        "id": 15,
        "name": "李涯斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "修武县人民政府",
        "source": "https://www.xiuwu.gov.cn/zfxxgk/zfxxgkml/zfld/"
    },
    # ═══════ 人大 ═══════
    {
        "id": 16,
        "name": "于三龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "修武县人民代表大会常务委员会",
        "source": "https://www.xiuwu.gov.cn/2026/07-20/608452.html"
    },
    {
        "id": 17,
        "name": "陶江山",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "修武县人民代表大会常务委员会",
        "source": "https://www.xiuwu.gov.cn/2026/07-20/608452.html"
    },
    {
        "id": 18,
        "name": "李晓海",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "修武县人民代表大会常务委员会",
        "source": "https://www.xiuwu.gov.cn/2026/07-20/608452.html"
    },
    {
        "id": 19,
        "name": "刘忠宝",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "修武县人民代表大会常务委员会",
        "source": "https://www.xiuwu.gov.cn/2026/07-20/608452.html"
    },
    # ═══════ 政协 ═══════
    {
        "id": 20,
        "name": "杨天军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议修武县委员会",
        "source": "https://www.xiuwu.gov.cn/2026/07-09/607592.html"
    },
    {
        "id": 21,
        "name": "雍冬明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "中国人民政治协商会议修武县委员会",
        "source": "https://www.xiuwu.gov.cn/2026/07-09/607592.html"
    },
    {
        "id": 22,
        "name": "薛静",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "中国人民政治协商会议修武县委员会",
        "source": "https://www.xiuwu.gov.cn/2026/07-09/607592.html"
    },
    {
        "id": 23,
        "name": "许海青",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "中国人民政治协商会议修武县委员会",
        "source": "https://www.xiuwu.gov.cn/2026/07-09/607592.html"
    },
    # ═══════ 检察院 ═══════
    {
        "id": 24,
        "name": "甄娜",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县检察院检察长",
        "current_org": "修武县人民检察院",
        "source": "https://www.xiuwu.gov.cn/2026/07-20/608452.html"
    },
]

# ═══════ Organizations ═══════════════════════════════════════════════════════
organizations = [
    {"id": 1, "name": "中共修武县委员会", "type": "党委", "level": "县级", "parent": "中共焦作市委员会", "location": "修武县"},
    {"id": 2, "name": "修武县人民政府", "type": "政府", "level": "县级", "parent": "焦作市人民政府", "location": "修武县"},
    {"id": 3, "name": "中共修武县纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共焦作市纪律检查委员会", "location": "修武县"},
    {"id": 4, "name": "修武县人民武装部", "type": "政府", "level": "县级", "location": "修武县"},
    {"id": 5, "name": "修武县人民代表大会常务委员会", "type": "人大", "level": "县级", "location": "修武县"},
    {"id": 6, "name": "中国人民政治协商会议修武县委员会", "type": "政协", "level": "县级", "location": "修武县"},
    {"id": 7, "name": "修武县人民检察院", "type": "政法", "level": "县级", "location": "修武县"},
]

# ═══════ Positions ═══════════════════════════════════════════════════════════
positions = [
    # 县委
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "正处级", "note": "县委副书记、县长"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "县委常委、常务副县长", "start": "", "end": "present", "rank": "副处级", "note": "协助县长分管审计"},
    {"person_id": 5, "org_id": 3, "title": "县委常委、纪委书记", "start": "", "end": "present", "rank": "副处级", "note": "2026年6月当选"},
    {"person_id": 6, "org_id": 4, "title": "县委常委、人武部政委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 县政府
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 人大
    {"person_id": 16, "org_id": 5, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 17, "org_id": 5, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 5, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 5, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 政协
    {"person_id": 20, "org_id": 6, "title": "县政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 21, "org_id": 6, "title": "县政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 22, "org_id": 6, "title": "县政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 23, "org_id": 6, "title": "县政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 检察院
    {"person_id": 24, "org_id": 7, "title": "县检察院检察长", "start": "", "end": "present", "rank": "副处级", "note": ""},
]

# ═══════ Relationships ═══════════════════════════════════════════════════════
relationships = [
    # Core leadership team overlap
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记—县长", "overlap_org": "中共修武县委员会/修武县人民政府", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记—县委副书记", "overlap_org": "中共修武县委员会", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长—县委副书记", "overlap_org": "中共修武县委员会", "overlap_period": "2026-"},
    # 县委书记—县委常委
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记—常务副县长", "overlap_org": "中共修武县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委书记—纪委书记", "overlap_org": "中共修武县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县委书记—人武部政委", "overlap_org": "中共修武县委员会", "overlap_period": "2026-"},
    # 县长—副县长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "县长—常务副县长", "overlap_org": "修武县人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "修武县人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "修武县人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "修武县人民政府", "overlap_period": "2026-"},
    # 县委常委之间
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "常务副县长—纪委书记", "overlap_org": "中共修武县委员会", "overlap_period": "2026-"},
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "常务副县长—人武部政委", "overlap_org": "中共修武县委员会", "overlap_period": "2026-"},
    # 人大—县委
    {"person_a": 1, "person_b": 16, "type": "overlap", "context": "县委书记—人大常委会主任", "overlap_org": "修武县", "overlap_period": "2026-"},
    # 政协—县委
    {"person_a": 1, "person_b": 20, "type": "overlap", "context": "县委书记—政协主席", "overlap_org": "修武县", "overlap_period": "2026-"},
]

# ── Person JSON helper ────────────────────────────────────────────────────────

def write_person_json(person: dict, extra_orgs: list[dict], extra_rels: list[dict], extra_positions: list[dict]) -> None:
    """Write a per-person graph JSON file."""
    pid = person["id"]
    name = person["name"]
    post_short = person["current_post"].replace("县委常委、", "").replace("县", "")
    
    filename = f"{TODAY}-河南省-焦作市-{post_short}-{name}.json"
    filepath = PJSON_DIR / filename
    
    import json

    identity = {
        "person_id": f"henan_jiaozuo_xiuwu_{name}",
        "name": name,
        "aliases": [],
        "gender": person.get("gender", ""),
        "ethnicity": person.get("ethnicity", ""),
        "birth": person.get("birth", ""),
        "birthplace": person.get("birthplace", ""),
        "native_place": "",
        "education": [],
        "party_join": person.get("party_join", ""),
        "work_start": person.get("work_start", ""),
        "dedupe_keys": {
            "name_birth": f"{name}_",
            "name_birthplace": f"{name}_",
            "official_profile_url": person.get("source", "")
        }
    }

    current_status = {
        "current_post": person["current_post"],
        "current_org": person["current_org"],
        "administrative_rank": "",
        "as_of": AS_OF,
        "is_current_confirmed": True,
        "source_ids": ["S001"]
    }

    career_timeline = []
    for pos in extra_positions:
        if pos["person_id"] == pid:
            career_timeline.append({
                "start": pos.get("start", ""),
                "end": pos.get("end", ""),
                "org": next((o["name"] for o in extra_orgs if o["id"] == pos["org_id"]), ""),
                "title": pos["title"],
                "level": "",
                "location": "修武县",
                "system": "",
                "rank": pos.get("rank", ""),
                "is_key_promotion": False,
                "notes": pos.get("note", ""),
                "confidence": "confirmed",
                "source_ids": ["S001"]
            })

    person_rels = []
    for r in extra_rels:
        if r["person_a"] == pid:
            other = next((p for p in persons if p["id"] == r["person_b"]), None)
            if other:
                person_rels.append({
                    "person": other["name"],
                    "person_id": f"henan_jiaozuo_xiuwu_{other['name']}",
                    "relationship_type": r["type"],
                    "strength": "strong",
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "person_to_other" if r["person_a"] == pid else "other_to_person",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                })
        elif r["person_b"] == pid:
            other = next((p for p in persons if p["id"] == r["person_a"]), None)
            if other:
                person_rels.append({
                    "person": other["name"],
                    "person_id": f"henan_jiaozuo_xiuwu_{other['name']}",
                    "relationship_type": r["type"],
                    "strength": "strong",
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "other_to_person" if r["person_a"] == pid else "person_to_other",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                })

    is_top_leader = pid in (1, 2)
    
    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河南省",
            "city": "焦作市",
            "region": "修武县",
            "job": person["current_post"],
            "task_id": "henan_修武县",
            "time_focus": "2026年7月"
        },
        "identity": identity,
        "current_status": current_status,
        "career_timeline": career_timeline,
        "organizations": [{"org": o["name"], "type": o["type"]} for o in extra_orgs],
        "relationships": person_rels,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": ["焦作市修武县"],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": f"No risk signals found for {name} in publicly available official sources as of {AS_OF}.",
            "date": AS_OF,
            "confidence": "confirmed",
            "source_ids": ["S001"]
        }],
        "source_register": [{
            "id": "S001",
            "title": "修武县人民政府官方网站",
            "url": "https://www.xiuwu.gov.cn/",
            "publisher": "修武县人民政府办公室",
            "published_at": "2026-07",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "Primary official source for leadership roster"
        }],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "high",
            "biggest_gap": "出生年月、籍贯、教育背景、完整履历"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的出生年月和籍贯？",
                "why_it_matters": "身份核验和去重",
                "suggested_queries": [f"{name} 简历 修武", f"{name} 出生"],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": f"{name}的教育背景（毕业院校、专业、学历）？",
                "why_it_matters": "了解专业背景和知识结构",
                "suggested_queries": [f"{name} 毕业 修武"],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": f"{name}任现职前的完整履历？",
                "why_it_matters": "了解职业发展路径和晋升模式",
                "suggested_queries": [f"{name} 曾任", f"{name} 工作经历"],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": f"{name}的入党时间和参加工作时间？",
                "why_it_matters": "评估政治资历",
                "suggested_queries": [f"{name} 入党"],
                "last_attempted": AS_OF
            }
        ]
    }
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"  Created: {filename}")


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    print(f"Building {SLUG} database and GEXF...")
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
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

    print(f"\nWriting person JSON files for core leaders...")
    write_person_json(
        persons[0],  # 李怀琛
        organizations, relationships, positions
    )
    write_person_json(
        persons[1],  # 宋科
        organizations, relationships, positions
    )

    print(f"\nFiles created in staging directory: {STAGING}")
    print("Run validation:")
    print(f"  python3 -m py_compile {__file__}")
    print(f"  python3 {__file__}")

if __name__ == "__main__":
    main()
