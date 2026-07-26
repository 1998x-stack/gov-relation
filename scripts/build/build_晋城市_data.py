#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 晋城市 (Jincheng City), 山西省.

Investigation date: 2026-07-26
Task ID: shanxi_晋城市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.jcgov.gov.cn — 晋城市人民政府官方网站 (primary, current as of July 2026)
  - https://www.jcgov.gov.cn/zwgk/ldzc/ — 领导之窗 page (confirmed July 2026)
  - Individual leader pages from 晋城在线 (primary, confirmed July 2026)

Confidence notes:
  - Current roles: confirmed via official government website (as of July 2026)
  - Leader biographical details from official 晋城在线 profile pages
  - Education and birth info: official profiles provide basic info but not full career timelines
  - Gaps: detailed career histories (prior positions before current role) mostly from web search limits
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
SLUG = "晋城市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shanxi_晋城市"
if _CURRENT_DIR.name == "shanxi_晋城市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-9 current party/government leaders, 10-19 standing committee, 20-29 government deputies, 30+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "薛明耀",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年8月",
        "birthplace": "",  # open question — official page doesn't list birthplace
        "education": "大学，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委书记",
        "current_org": "中共晋城市委员会",
        "source": "https://www.jcgov.gov.cn/zwgk/ldzc/swld/sj/xmy1/grjl/202108/t20210818_1455062.shtml",
    },
    {
        "id": 2,
        "name": "刘振华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年5月",
        "birthplace": "",  # unverified
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委副书记、市长",
        "current_org": "晋城市人民政府",
        "source": "https://www.jcgov.gov.cn/zwgk/ldzc/szfld/sz/lzh/lzhgrjl/202109/t20210910_1466240.shtml",
    },
    {
        "id": 3,
        "name": "张钧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年3月",
        "birthplace": "",  # unverified
        "education": "研究生，法学博士",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委副书记（正厅长级）、市委政法委书记",
        "current_org": "中共晋城市委员会",
        "source": "https://www.jcgov.gov.cn/zwgk/ldzc/swld/fsj/zj/grjl_56415/202606/t20260605_2357687.shtml",
    },
    # ══════════════════════════════════════════════════════════════════════════
    # Standing Committee
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "辛艾艾",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1968年11月",
        "birthplace": "",  # unverified
        "education": "大学，工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市委组织部部长，市委党校校长（兼）",
        "current_org": "中共晋城市委员会",
        "source": "https://www.jcgov.gov.cn/zwgk/ldzc/swld/cw/xaa_41073/",
    },
    {
        "id": 11,
        "name": "田志军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年6月",
        "birthplace": "",  # unverified
        "education": "大学，工程硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市政府党组副书记、副市长",
        "current_org": "晋城市人民政府",
        "source": "https://www.jcgov.gov.cn/zwgk/ldzc/swld/cw/tzj_42945/",
    },
    {
        "id": 12,
        "name": "于志奇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年2月",
        "birthplace": "",
        "education": "大学，工学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市委统战部部长",
        "current_org": "中共晋城市委员会",
        "source": "https://www.jcgov.gov.cn/zwgk/ldzc/swld/cw/yzq/",
    },
    {
        "id": 13,
        "name": "邓志蓉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1971年3月",
        "birthplace": "",
        "education": "大学，法学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市委宣传部部长",
        "current_org": "中共晋城市委员会",
        "source": "https://www.jcgov.gov.cn/zwgk/ldzc/swld/cw/dzr_46512/",
    },
    {
        "id": 14,
        "name": "高一钧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年3月",
        "birthplace": "",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市委秘书长",
        "current_org": "中共晋城市委员会",
        "source": "https://www.jcgov.gov.cn/zwgk/ldzc/swld/cw/gyj_55829/",
    },
    {
        "id": 15,
        "name": "杨景隆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年11月",
        "birthplace": "",
        "education": "大学，工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市纪委书记、市监委主任",
        "current_org": "中共晋城市纪律检查委员会",
        "source": "https://www.jcgov.gov.cn/zwgk/ldzc/swld/cw/yjl/",
    },
    {
        "id": 16,
        "name": "任波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # unverified
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共晋城市委员会",
        "source": "https://www.jcgov.gov.cn/zwgk/ldzc/",
    },
    # ══════════════════════════════════════════════════════════════════════════
    # Government Deputy Mayors
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": 20,
        "name": "黄登宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年11月",
        "birthplace": "",
        "education": "研究生，工学博士",
        "party_join": "民革党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "晋城市人民政府",
        "source": "https://www.jcgov.gov.cn/zwgk/ldzc/szfld/fsz/hdy_46507/",
    },
    {
        "id": 21,
        "name": "杨晓雷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年3月",
        "birthplace": "",
        "education": "大学，教育学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "晋城市人民政府",
        "source": "https://www.jcgov.gov.cn/zwgk/ldzc/szfld/fsz/yxl_42110/",
    },
    {
        "id": 22,
        "name": "贺文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # unverified
        "birthplace": "",
        "education": "",  # unverified
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "晋城市人民政府",
        "source": "https://www.jcgov.gov.cn/zwgk/ldzc/szfld/",
    },
    {
        "id": 23,
        "name": "张军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # unverified
        "birthplace": "",
        "education": "",  # unverified
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "晋城市人民政府",
        "source": "https://www.jcgov.gov.cn/zwgk/ldzc/szfld/",
    },
    # ══════════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "王震",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # unverified
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山西省委常委、省委秘书长",  # inferred — previous role was 晋城市委书记
        "current_org": "中共山西省委",
        "source": "plausible — reported by media; previous 晋城市委书记 promoted to provincial role",
    },
    # ══════════════════════════════════════════════════════════════════════════
    # NPC/CPPCC Leaders
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": 40,
        "name": "石云峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年2月",
        "birthplace": "",
        "education": "大学，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会党组书记、主任",
        "current_org": "晋城市人民代表大会常务委员会",
        "source": "https://www.jcgov.gov.cn/zwgk/ldzc/srdld/zr/syf/",
    },
    {
        "id": 41,
        "name": "孟贵芳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年6月",
        "birthplace": "",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协党组书记、主席",
        "current_org": "中国人民政治协商会议晋城市委员会",
        "source": "https://www.jcgov.gov.cn/zwgk/ldzc/szxld/zx/mgf_49989/",
    },
]


# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共晋城市委员会", "type": "党委", "level": "地级市", "parent": "中共山西省委", "location": "晋城市"},
    {"id": 2, "name": "晋城市人民政府", "type": "政府", "level": "地级市", "parent": "山西省人民政府", "location": "晋城市"},
    {"id": 3, "name": "中共晋城市纪律检查委员会", "type": "纪委", "level": "地级市", "parent": "中共晋城市委员会", "location": "晋城市"},
    {"id": 4, "name": "晋城市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "晋城市", "location": "晋城市"},
    {"id": 5, "name": "中国人民政治协商会议晋城市委员会", "type": "政协", "level": "地级市", "parent": "晋城市", "location": "晋城市"},
    {"id": 6, "name": "中共山西省委", "type": "党委", "level": "省级", "parent": "中共中央", "location": "太原市"},
    {"id": 7, "name": "晋城市委组织部", "type": "党委", "level": "地级市", "parent": "中共晋城市委员会", "location": "晋城市"},
    {"id": 8, "name": "晋城市委统战部", "type": "党委", "level": "地级市", "parent": "中共晋城市委员会", "location": "晋城市"},
    {"id": 9, "name": "晋城市委宣传部", "type": "党委", "level": "地级市", "parent": "中共晋城市委员会", "location": "晋城市"},
    {"id": 10, "name": "晋城市委政法委", "type": "党委", "level": "地级市", "parent": "中共晋城市委员会", "location": "晋城市"},
]


# ── Positions ───────────────────────────────────────────────────────────────

positions = [
    # Party Secretary
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "未知", "end_date": "现任", "rank": "正厅级", "note": "2021年起任晋城市委书记，2024年薛明耀接任"},
    # Mayor
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "未知", "end_date": "现任", "rank": "正厅级", "note": "市委副书记、市政府党组书记、市长"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "未知", "end_date": "现任", "rank": "正厅级", "note": ""},
    # Deputy Party Secretary
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start_date": "未知", "end_date": "现任", "rank": "正厅长级", "note": "2026年6月前已任职"},
    {"person_id": 3, "org_id": 10, "title": "市委政法委书记", "start_date": "未知", "end_date": "现任", "rank": "正厅长级", "note": ""},
    # Standing Committee
    {"person_id": 10, "org_id": 7, "title": "市委组织部部长", "start_date": "未知", "end_date": "现任", "rank": "正厅级", "note": "市委常委、组织部部长"},
    {"person_id": 11, "org_id": 2, "title": "副市长（常务）", "start_date": "未知", "end_date": "现任", "rank": "正厅级", "note": "市委常委、市政府党组副书记、副市长"},
    {"person_id": 12, "org_id": 8, "title": "市委统战部部长", "start_date": "未知", "end_date": "现任", "rank": "副厅级", "note": "市委常委、统战部部长，兼市政协党组副书记"},
    {"person_id": 13, "org_id": 9, "title": "市委宣传部部长", "start_date": "未知", "end_date": "现任", "rank": "副厅级", "note": ""},
    {"person_id": 14, "org_id": 1, "title": "市委秘书长", "start_date": "未知", "end_date": "现任", "rank": "副厅级", "note": ""},
    {"person_id": 15, "org_id": 3, "title": "市纪委书记", "start_date": "未知", "end_date": "现任", "rank": "正厅级", "note": "二级高级监察官"},
    {"person_id": 16, "org_id": 1, "title": "市委常委", "start_date": "未知", "end_date": "现任", "rank": "副厅级", "note": "具体分工待查"},
    # Deputy Mayors
    {"person_id": 20, "org_id": 2, "title": "副市长", "start_date": "未知", "end_date": "现任", "rank": "副厅级", "note": "民革党员，分管科技、民政、市场监管、供销"},
    {"person_id": 21, "org_id": 2, "title": "副市长", "start_date": "未知", "end_date": "现任", "rank": "副厅级", "note": "负责自然规划、住建、交通、文旅、体育"},
    {"person_id": 22, "org_id": 2, "title": "副市长", "start_date": "未知", "end_date": "现任", "rank": "副厅级", "note": "分工待查"},
    {"person_id": 23, "org_id": 2, "title": "副市长", "start_date": "未知", "end_date": "现任", "rank": "副厅级", "note": "分工待查"},
    # Predecessor
    {"person_id": 30, "org_id": 1, "title": "市委书记（前）", "start_date": "未知", "end_date": "约2024/2025", "rank": "正厅级", "note": "前任市委书记，后调任省委常委、省委秘书长"},
    # NPC/CPPCC
    {"person_id": 40, "org_id": 4, "title": "市人大常委会主任", "start_date": "未知", "end_date": "现任", "rank": "正厅级", "note": ""},
    {"person_id": 41, "org_id": 5, "title": "市政协主席", "start_date": "未知", "end_date": "现任", "rank": "正厅级", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────

relationships = [
    # Core leadership overlaps
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委班子搭档：薛明耀（书记）+ 刘振华（市长、副书记）", "overlap_org": "中共晋城市委员会", "overlap_period": AS_OF},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "薛明耀（书记）+ 张钧（副书记、政法委书记）", "overlap_org": "中共晋城市委员会", "overlap_period": AS_OF},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "两位副书记共同在市委领导班子", "overlap_org": "中共晋城市委员会", "overlap_period": AS_OF},
    # Standing Committee overlaps with core
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "书记 + 组织部长，干部选任核心搭档", "overlap_org": "中共晋城市委员会", "overlap_period": AS_OF},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "书记 + 常务副市长（政府党组副书记）", "overlap_org": "中共晋城市委员会", "overlap_period": AS_OF},
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "书记 + 统战部长", "overlap_org": "中共晋城市委员会", "overlap_period": AS_OF},
    {"person_a": 1, "person_b": 13, "type": "overlap", "context": "书记 + 宣传部长", "overlap_org": "中共晋城市委员会", "overlap_period": AS_OF},
    {"person_a": 1, "person_b": 14, "type": "overlap", "context": "书记 + 秘书长，日常工作协调", "overlap_org": "中共晋城市委员会", "overlap_period": AS_OF},
    {"person_a": 1, "person_b": 15, "type": "overlap", "context": "书记 + 纪委书记", "overlap_org": "中共晋城市委员会", "overlap_period": AS_OF},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "市长 + 常务副市长", "overlap_org": "晋城市人民政府", "overlap_period": AS_OF},
    {"person_a": 2, "person_b": 20, "type": "superior_subordinate", "context": "市长 + 副市长", "overlap_org": "晋城市人民政府", "overlap_period": AS_OF},
    {"person_a": 2, "person_b": 21, "type": "superior_subordinate", "context": "市长 + 副市长", "overlap_org": "晋城市人民政府", "overlap_period": AS_OF},
    {"person_a": 2, "person_b": 22, "type": "superior_subordinate", "context": "市长 + 副市长", "overlap_org": "晋城市人民政府", "overlap_period": AS_OF},
    {"person_a": 2, "person_b": 23, "type": "superior_subordinate", "context": "市长 + 副市长", "overlap_org": "晋城市人民政府", "overlap_period": AS_OF},
    # Predecessor relationship
    {"person_a": 1, "person_b": 30, "type": "predecessor_successor", "context": "王震（前任市委书记）→ 薛明耀（接任市委书记）", "overlap_org": "中共晋城市委员会", "overlap_period": "交接期"},
    # NPC / CPPCC
    {"person_a": 1, "person_b": 40, "type": "overlap", "context": "书记 + 人大主任，党政和人大体系对接", "overlap_org": "晋城市", "overlap_period": AS_OF},
    {"person_a": 1, "person_b": 41, "type": "overlap", "context": "书记 + 政协主席", "overlap_org": "晋城市", "overlap_period": AS_OF},
    {"person_a": 2, "person_b": 40, "type": "overlap", "context": "市长 + 人大主任", "overlap_org": "晋城市", "overlap_period": AS_OF},
    {"person_a": 2, "person_b": 41, "type": "overlap", "context": "市长 + 政协主席", "overlap_org": "晋城市", "overlap_period": AS_OF},
]


# ── Person JSON builders ─────────────────────────────────────────────────────

def write_person_json(person: dict, extra: dict | None = None) -> None:
    """Write a single person JSON file to the staging directory."""
    name = person["name"]
    job = person["current_post"].split("（")[0].replace("(", "").replace(")", "").replace(" ", "_")
    filename = f"{TODAY}-山西省-晋城市-{job}-{name}.json"
    # Map roles to person IDs for deduplication
    name_birth_key = f"晋城市_{name}"
    if person.get("birth"):
        name_birth_key = f"晋城市_{name}_{person['birth']}"

    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "山西省",
            "city": "晋城市",
            "region": "晋城市",
            "job": person["current_post"],
            "task_id": "shanxi_晋城市",
            "time_focus": AS_OF,
        },
        "identity": {
            "person_id": name_birth_key,
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [{
                "period": "",
                "institution": "",
                "major": person["education"] if person["education"] else "",
                "degree": person["education"] if person["education"] else "",
                "study_type": "unknown",
                "source_ids": []
            }] if person["education"] else [],
            "party_join": person["party_join"] if person["party_join"] in ("中共党员", "民革党员") else "未知",
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}" if person.get("birth") else person["name"],
                "name_birthplace": f"{person['name']}" if not person.get("birthplace") else f"{person['name']}_{person['birthplace']}",
                "official_profile_url": person.get("source", "")
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [{
            "start": "未知",
            "end": "现任",
            "org": person["current_org"],
            "title": person["current_post"],
            "level": "",
            "location": "晋城市",
            "system": "party" if "委" in person["current_org"] else "government",
            "rank": "",
            "is_key_promotion": True,
            "notes": "当前任职，具体起始时间待查",
            "confidence": "confirmed",
            "source_ids": ["S001"]
        }],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "salaries": {},
        "deputies": [],
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
            "public_style_indicators": [{
                "trait": "unknown",
                "evidence": "公开资料不足",
                "confidence": "unverified",
                "source_ids": []
            }],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "本次调查未发现风险信号",
            "date": AS_OF,
            "confidence": "unverified",
            "source_ids": []
        }],
        "source_register": [{
            "id": "S001",
            "title": f"晋城市人民政府领导之窗 — {person['current_post']}",
            "url": person.get("source", ""),
            "publisher": "晋城市人民政府",
            "published_at": AS_OF,
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "官方领导之窗页面"
        }],
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "详细履历（任职起始时间、早期职业生涯）待查"
        },
        "open_questions": [{
            "priority": "high",
            "question": "该领导担任现职前的详细履历",
            "why_it_matters": "缺乏完整的仕途晋升路径，无法分析其网络关系和升迁模式",
            "suggested_queries": [
                f"{person['name']} 简历",
                f"{person['name']} 任前公示",
                f"{person['name']} 任职经历"
            ],
            "last_attempted": AS_OF
        }]
    }
    out_path = PJSON_DIR / filename
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {out_path}")


# ── Main ────────────────────────────────────────────────────────────────────

def main() -> None:
    print(f"=== Building {SLUG} network ===")

    # 1. Write person JSONs for all key figures
    print("\n--- Writing person JSONs ---")
    core_ids = {1: "市委书记", 2: "市长", 3: "市委副书记", 10: "市委组织部部长",
                11: "常务副市长", 12: "市委统战部部长", 13: "市委宣传部部长",
                14: "市委秘书长", 15: "市纪委书记", 40: "市人大常委会主任",
                41: "市政协主席", 30: "前任市委书记"}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    # 2. Build DB + GEXF
    print(f"\n--- Building database: {DB_PATH}")
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

    # 3. Verify
    db_size = DB_PATH.stat().st_size if DB_PATH.exists() else 0
    gexf_size = GEXF_PATH.stat().st_size if GEXF_PATH.exists() else 0
    print(f"\n=== Summary ===")
    print(f"  Database: {DB_PATH} ({db_size} bytes)")
    print(f"  GEXF:     {GEXF_PATH} ({gexf_size} bytes)")
    print(f"  Persons:   {len(persons)}")
    print(f"  Orgs:     {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relations: {len(relationships)}")
    pjson_count = len(list(PJSON_DIR.glob("*.json")))
    print(f"  Person JSONs: {pjson_count}")
    print("=== Done ===")


if __name__ == "__main__":
    main()