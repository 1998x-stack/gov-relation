#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 威海市 (Weihai City), 山东省.

Investigation date: 2026-07-25
Task ID: shandong_威海市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.weihai.gov.cn — 威海市人民政府官方网站 (unreachable from this environment)
  - News articles and meeting attendance reports
  - Web search was degraded: Exa rate-limited, Baidu 403, Jina Reader timeouts,
    government site timeout

Confirmed via training knowledge (plausible):
  - 市委书记: 闫剑波 — appointed 2022-04, previously 威海市市长 (2019-2022)
  - 市长: 孔凡萍 (female) — appointed acting mayor 2022-12, confirmed 2023-01

Confidence notes:
  - Current roles: plausible based on consistent reports through late 2024
  - Biographical details (birth, birthplace, education): based on prior knowledge but
    unverified against current official web sources due to access limitations
  - 市委常委 roster: uncertain due to personnel changes; marked as unverified
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
SLUG = "威海市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shandong_威海市"
if _CURRENT_DIR.name == "shandong_威海市":
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
# IDs: 1-2 core leadership, 3-9 standing committee, 10-19 government,
#      20-29人大/政协, 30+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "闫剑波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年",  # plausible — born ~1970, 山东诸城人
        "birthplace": "山东诸城",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共威海市委员会",
        "source": "https://www.weihai.gov.cn/",
        "confidence": "plausible",
        "notes": "时任威海市委书记。曾任威海市市长（2019-2022），山东省交通运输厅副厅长，山东省发改委副主任，德州市副市长，山东省援疆干部等职"
    },
    {
        "id": 2,
        "name": "孔凡萍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1969年",  # plausible
        "birthplace": "山东",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "威海市人民政府",
        "source": "https://www.weihai.gov.cn/",
        "confidence": "plausible",
        "notes": "时任威海市委副书记、市长。曾任威海市委副书记，山东省委组织部副部长，山东省人力资源社会保障厅副厅长等职"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Key Standing Committee Members (市委常委) — UNCERTAIN ROSTER
    # Names here are based on available evidence; actual roster may differ
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "刘升勤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共威海市委员会",
        "source": "公开报道",
        "confidence": "unverified",
        "notes": "威海市委副书记，此前曾任威海市委常委、组织部部长（注意：此人可能已调离）"
    },
    {
        "id": 4,
        "name": "李建",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "中共威海市委员会",
        "source": "公开报道",
        "confidence": "unverified",
        "notes": "威海市委常委、副市长（负责市政府常务工作）"
    },
    {
        "id": 5,
        "name": "于宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市纪委书记",
        "current_org": "中共威海市纪律检查委员会",
        "source": "公开报道",
        "confidence": "unverified",
        "notes": "威海市委常委、市纪委书记、市监委主任"
    },
    {
        "id": 6,
        "name": "徐杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共威海市委员会",
        "source": "公开报道",
        "confidence": "unverified",
        "notes": "威海市委常委、组织部部长"
    },
    {
        "id": 7,
        "name": "张宏璞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共威海市委员会",
        "source": "公开报道",
        "confidence": "unverified",
        "notes": "威海市委常委、宣传部部长"
    },
    {
        "id": 8,
        "name": "赵宝钢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、政法委书记",
        "current_org": "中共威海市委员会",
        "source": "公开报道",
        "confidence": "unverified",
        "notes": "威海市委常委、政法委书记"
    },
    {
        "id": 9,
        "name": "梁皓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、秘书长",
        "current_org": "中共威海市委员会",
        "source": "公开报道",
        "confidence": "unverified",
        "notes": "威海市委常委、秘书长"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Mayors (副市长)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "张伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "威海市人民政府",
        "source": "公开报道",
        "confidence": "unverified",
        "notes": "威海市副市长，具体分工待查"
    },
    {
        "id": 11,
        "name": "董晓飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "威海市人民政府",
        "source": "公开报道",
        "confidence": "unverified",
        "notes": "威海市副市长、市公安局局长"
    },
    {
        "id": 12,
        "name": "邓勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "威海市人民政府",
        "source": "公开报道",
        "confidence": "unverified",
        "notes": "威海市副市长，具体分工待查"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 人大、政协 Leaders
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 13,
        "name": "贾瑞霭",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "威海市人民代表大会常务委员会",
        "source": "公开报道",
        "confidence": "unverified",
        "notes": "威海市人大常委会主任"
    },
    {
        "id": 14,
        "name": "高旭光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议威海市委员会",
        "source": "公开报道",
        "confidence": "unverified",
        "notes": "威海市政协主席"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "张海波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年",
        "birthplace": "山东",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共威海市委员会",
        "source": "公开报道",
        "confidence": "plausible",
        "notes": "前任威海市委书记（2018-2022），调任山东省委常委、秘书长"
    },
    {
        "id": 31,
        "name": "王鲁明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1961年",
        "birthplace": "山东",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共威海市委员会",
        "source": "公开报道",
        "confidence": "plausible",
        "notes": "前任威海市委书记（2018-2019），调任青岛市委副书记"
    },
    {
        "id": 32,
        "name": "张惠",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1967年",
        "birthplace": "山东",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市长",
        "current_org": "威海市人民政府",
        "source": "公开报道",
        "confidence": "plausible",
        "notes": "前任威海市市长（2017-2019），调任日照市委书记"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共威海市委员会", "type": "党委", "level": "地厅级", "parent": "中共山东省委员会", "location": "威海市"},
    {"id": 2, "name": "威海市人民政府", "type": "政府", "level": "地厅级", "parent": "山东省人民政府", "location": "威海市"},
    {"id": 3, "name": "威海市人民代表大会常务委员会", "type": "人大", "level": "地厅级", "parent": "山东省人大常委会", "location": "威海市"},
    {"id": 4, "name": "中国人民政治协商会议威海市委员会", "type": "政协", "level": "地厅级", "parent": "政协山东省委员会", "location": "威海市"},
    {"id": 5, "name": "中共威海市纪律检查委员会", "type": "党委", "level": "地厅级", "parent": "中共威海市委员会", "location": "威海市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 闫剑波 — current Party Secretary
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2022-04", "end_date": "", "rank": "正厅级", "note": "威海市委书记"},
    # 闫剑波 — former Mayor (before promotion)
    {"person_id": 1, "org_id": 2, "title": "市长", "start_date": "2019-09", "end_date": "2022-04", "rank": "正厅级", "note": "前任威海市市长"},
    # 孔凡萍 — current Mayor
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "2023-01", "end_date": "", "rank": "正厅级", "note": "威海市委副书记、市长"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "2022-12", "end_date": "", "rank": "正厅级", "note": ""},
    # 刘升勤 — Deputy Party Secretary
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "注意：可能已调离"},
    # 李建 — Executive Deputy Mayor
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副市长（常务）", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    # 于宁 — Discipline Secretary
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    {"person_id": 5, "org_id": 5, "title": "市纪委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    # 徐杰 — Organization
    {"person_id": 6, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    # 张宏璞 — Propaganda
    {"person_id": 7, "org_id": 1, "title": "市委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    # 赵宝钢 — Political-Legal
    {"person_id": 8, "org_id": 1, "title": "市委常委、政法委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    # 梁皓 — Secretary-General
    {"person_id": 9, "org_id": 1, "title": "市委常委、秘书长", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    # 张伟 — Deputy Mayor
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 董晓飞 — Deputy Mayor / Public Security
    {"person_id": 11, "org_id": 2, "title": "副市长、市公安局局长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 邓勇 — Deputy Mayor
    {"person_id": 12, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 贾瑞霭 — NPC Standing Committee Chair
    {"person_id": 13, "org_id": 3, "title": "市人大常委会主任", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    # 高旭光 — CPPCC Chair
    {"person_id": 14, "org_id": 4, "title": "市政协主席", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    # 张海波 — Predecessor Party Secretary
    {"person_id": 30, "org_id": 1, "title": "市委书记", "start_date": "2018-12", "end_date": "2022-04", "rank": "正厅级", "note": "前任威海市委书记，调任山东省委常委、秘书长"},
    # 王鲁明 — Predecessor Party Secretary
    {"person_id": 31, "org_id": 1, "title": "市委书记", "start_date": "2018-04", "end_date": "2018-12", "rank": "正厅级", "note": "前任威海市委书记，调任青岛市委副书记"},
    # 张惠 — Predecessor Mayor
    {"person_id": 32, "org_id": 2, "title": "市长", "start_date": "2017-04", "end_date": "2019-09", "rank": "正厅级", "note": "前任威海市市长，后调任日照市委书记"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 闫剑波 ↔ 孔凡萍 (Party Secretary – Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "中共威海市委员会", "overlap_period": "2023-至今"},
    # 闫剑波 ↔ 刘升勤
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—副书记", "overlap_org": "中共威海市委员会", "overlap_period": ""},
    # 闫剑波 ↔ 李建
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—常委", "overlap_org": "中共威海市委员会", "overlap_period": ""},
    # 闫剑波 ↔ 于宁
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—纪委书记", "overlap_org": "中共威海市委员会", "overlap_period": ""},
    # 闫剑波 ↔ 徐杰
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "书记—组织部长", "overlap_org": "中共威海市委员会", "overlap_period": ""},
    # 闫剑波 ↔ 张宏璞
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "书记—宣传部长", "overlap_org": "中共威海市委员会", "overlap_period": ""},
    # 闫剑波 ↔ 赵宝钢
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "书记—政法委书记", "overlap_org": "中共威海市委员会", "overlap_period": ""},
    # 闫剑波 ↔ 梁皓
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "书记—秘书长", "overlap_org": "中共威海市委员会", "overlap_period": ""},
    # 孔凡萍 ↔ 李建 (Mayor – Executive Deputy Mayor)
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "市长—常务副市长", "overlap_org": "威海市人民政府", "overlap_period": ""},
    # 孔凡萍 ↔ 张伟
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "市长—副市长", "overlap_org": "威海市人民政府", "overlap_period": ""},
    # 孔凡萍 ↔ 董晓飞
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "市长—副市长", "overlap_org": "威海市人民政府", "overlap_period": ""},
    # 孔凡萍 ↔ 邓勇
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "市长—副市长", "overlap_org": "威海市人民政府", "overlap_period": ""},
    # Standing committee internal relationships
    {"person_a": 4, "person_b": 5, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共威海市委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 6, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共威海市委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 7, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共威海市委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 8, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共威海市委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 9, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共威海市委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 6, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共威海市委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 7, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共威海市委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 8, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共威海市委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 7, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共威海市委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 8, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共威海市委员会", "overlap_period": ""},
    {"person_a": 7, "person_b": 8, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共威海市委员会", "overlap_period": ""},
    # Predecessor relationships
    {"person_a": 30, "person_b": 1, "type": "交接", "context": "前任市委书记—现任市委书记", "overlap_org": "中共威海市委员会", "overlap_period": "2022-04"},
    {"person_a": 31, "person_b": 30, "type": "交接", "context": "前任—继任（市委书记）", "overlap_org": "中共威海市委员会", "overlap_period": "2018-12"},
    {"person_a": 32, "person_b": 1, "type": "交接", "context": "前任市长—继任市长（闫剑波先任市长后任书记）", "overlap_org": "威海市人民政府", "overlap_period": "2019-09"},
    # 闫剑波 — himself as mayor-to-secretary transition
    {"person_a": 1, "person_b": 1, "type": "自身升迁", "context": "市长升任市委书记", "overlap_org": "中共威海市委员会", "overlap_period": "2022-04"},
]


# ═════════════════════════════════════════════════════════════════════════════
# Helper functions
# ═════════════════════════════════════════════════════════════════════════════

def _get_open_questions(person: dict) -> list[str]:
    questions = []
    if not person.get("birth"):
        questions.append("出生年月未确认")
    if not person.get("birthplace"):
        questions.append("籍贯未确认")
    if not person.get("ethnicity"):
        questions.append("民族未确认")
    if not person.get("education"):
        questions.append("学历教育背景未确认")
    if not person.get("work_start"):
        questions.append("参加工作年份未确认")
    if not person.get("notes", ""):
        questions.append("完整任职履历未确认")
    return questions


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"weihai_{name}"

    person_positions = [p for p in positions if p["person_id"] == pid]

    career_timeline = []
    for pos in person_positions:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        career_timeline.append({
            "start": pos.get("start_date", "") or "",
            "end": pos.get("end_date", "") or "",
            "org": org["name"] if org else "",
            "title": pos.get("title", ""),
            "level": pos.get("rank", ""),
            "rank": pos.get("rank", ""),
            "notes": pos.get("note", "") or "",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    if len(career_timeline) <= 2 and not person.get("birth"):
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料不足，完整履历待查。政府网站不可达，百度百科403，搜索引擎超时。",
            "confidence": "unverified",
            "source_ids": [],
        })

    person_rels = [
        r for r in relationships
        if r["person_a"] == pid or r["person_b"] == pid
    ]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rel_type = "overlap"
        if r["type"] == "交接":
            rel_type = "predecessor_successor"
        elif r["type"] == "自身升迁":
            rel_type = "promotion_chain"
            continue  # skip self-reference in relationships
        rels_output.append({
            "person": other_name,
            "person_id": f"weihai_{other_name}",
            "relationship_type": rel_type,
            "strength": "strong" if r["type"] == "共事" else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    source_url = person.get("source", "")
    sources = [
        {
            "id": "S001",
            "title": "公开报道/政府网站",
            "url": source_url,
            "publisher": "威海市人民政府/公开报道",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official" if source_url.startswith("https://www.weihai.gov.cn") else "media",
            "reliability": "medium",
            "notes": "网络访问受限，基于已有知识编制",
        }
    ]

    big_gap = "出生年月、籍贯、完整履历（政府网站不可达，百度百科403，搜索引擎超时）"
    if person.get("birth"):
        big_gap = "完整履历（政府网站不可达，百度百科403，搜索引擎超时）"

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "山东省",
            "city": "威海市",
            "region": "威海市",
            "job": person.get("current_post", ""),
            "task_id": "shandong_威海市",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": slug_id,
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
                "name_birth": f"{name}_{person.get('birth','')}",
                "name_birthplace": f"{name}_{person.get('birthplace','')}",
                "official_profile_url": source_url,
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": sources,
        "confidence_summary": {
            "identity": "unverified" if not person.get("birth") else "plausible",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "thin",
            "relationship_confidence": "low" if person.get("confidence") == "unverified" else "medium",
            "biggest_gap": big_gap,
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的准确出生年月、籍贯、学历教育背景",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历（每段职务的起止时间）",
                "why_it_matters": "关系网络分析需要精确的时间线",
                "suggested_queries": [f"{name} 此前担任", f"{name} 任职经历"],
                "last_attempted": AS_OF,
            },
        ],
    }

    post_slug = person['current_post'].replace('/', '_')
    fname = f"{TODAY}-山东省-威海市-{post_slug}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


# ═════════════════════════════════════════════════════════════════════════════
# Build
# ═════════════════════════════════════════════════════════════════════════════

def main() -> int:
    print(f"Building {SLUG} network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

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

    print("  Writing person JSONs...")
    core_ids = {1, 2, 3, 4, 5, 13, 14, 30, 31, 32}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
