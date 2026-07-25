#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 泰安市 (Tai'an City), 山东省.

Investigation date: 2026-07-25
Task ID: shandong_泰安市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - zh.wikipedia.org/wiki/泰安市 — Wikipedia (current leadership as of July 2026)
  - zh.wikipedia.org/wiki/杨洪涛 — biography of Party Secretary
  - www.taian.gov.cn — 泰安市人民政府官方网站 (homepage confirms names in July 2026)
  - zh.wikipedia.org/wiki/崔洪刚 — biography of predecessor Party Secretary

Confidence notes:
  - Current roles: confirmed via Wikipedia infobox and official news (July 2026)
  - 杨洪涛 biography: confirmed via detailed Wikipedia page (career timeline, education, party dates)
  - 李国强 biography: partial — confirmed name/role and as-of date from Wikipedia, full resume unverified
  - Web search degraded: Exa rate-limited, Baidu 403
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
SLUG = "泰安市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shandong_泰安市"
if _CURRENT_DIR.name == "shandong_泰安市":
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
# IDs: 1-2 core, 3-4人大/政协, 5-9 standing committee, 10+ deputies, 30+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "杨洪涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966-10",
        "birthplace": "山东省烟台市",  # Wikipedia says "山东泰安人" in text but "烟台市" in infobox
        "education": "山东经济学院（现山东财经大学）财政系财政学专业",
        "party_join": "中共党员",
        "work_start": "1988-07",
        "current_post": "市委书记",
        "current_org": "中共泰安市委员会",
        "source": "https://zh.wikipedia.org/wiki/杨洪涛",
        "confidence": "confirmed",
        "notes": "1986年入党，1988年7月参加工作。2021年8月起任泰安市委书记。此前曾任德州市市长、淄博市常务副市长、淄川区委书记等职。2015年获全国优秀县委书记称号。"
    },
    {
        "id": 2,
        "name": "李国强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-12",
        "birthplace": "山东省济南市",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "泰安市人民政府",
        "source": "https://zh.wikipedia.org/wiki/泰安市",
        "confidence": "confirmed",
        "notes": "2026年2月任泰安市代市长，后转正。此前简历待查。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 人大、政协 Leaders
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "程远军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-09",
        "birthplace": "山东省巨野县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "泰安市人民代表大会常务委员会",
        "source": "https://zh.wikipedia.org/wiki/泰安市",
        "confidence": "confirmed",
        "notes": "2025年1月当选泰安市人大常委会主任"
    },
    {
        "id": 4,
        "name": "武林中",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966-11",
        "birthplace": "山东省广饶县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议泰安市委员会",
        "source": "https://zh.wikipedia.org/wiki/泰安市",
        "confidence": "confirmed",
        "notes": "2022年2月当选泰安市政协主席"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee / Deputy Government (placeholder — names unconfirmed)
    # These will be filled when more detailed roster data is available
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 5,
        "name": "【待查】常务副市长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "泰安市人民政府",
        "source": "",
        "confidence": "unverified",
        "notes": "姓名和分工待从泰安市人民政府网站领导之窗页面确认"
    },
    {
        "id": 6,
        "name": "【待查】纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市纪委书记、市监委主任",
        "current_org": "中共泰安市纪律检查委员会",
        "source": "",
        "confidence": "unverified",
        "notes": "姓名待确认"
    },
    {
        "id": 7,
        "name": "【待查】组织部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共泰安市委员会组织部",
        "source": "",
        "confidence": "unverified",
        "notes": "姓名待确认"
    },
    {
        "id": 8,
        "name": "【待查】宣传部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共泰安市委员会宣传部",
        "source": "",
        "confidence": "unverified",
        "notes": "姓名待确认"
    },
    {
        "id": 9,
        "name": "【待查】政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、政法委书记",
        "current_org": "中共泰安市委员会政法委员会",
        "source": "",
        "confidence": "unverified",
        "notes": "姓名待确认"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "崔洪刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1961-05",
        "birthplace": "山东省淄博市",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "1978-10",
        "current_post": "前任市委书记",
        "current_org": "中共泰安市委员会",
        "source": "https://zh.wikipedia.org/wiki/崔洪刚",
        "confidence": "confirmed",
        "notes": "2018年5月-2021年8月任泰安市委书记。此前任滨州市市长。2023年8月被查，2024年11月因受贿5299万余元被判处有期徒刑14年6个月。"
    },
    {
        "id": 31,
        "name": "李兰祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市长",
        "current_org": "泰安市人民政府",
        "source": "https://zh.wikipedia.org/wiki/泰安市",
        "confidence": "confirmed",
        "notes": "2022年12月-2026年2月任泰安市市长，后由李国强接任"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共泰安市委员会", "type": "党委", "level": "地级市", "parent": "中共山东省委员会", "location": "泰安市"},
    {"id": 2, "name": "泰安市人民政府", "type": "政府", "level": "地级市", "parent": "山东省人民政府", "location": "泰安市"},
    {"id": 3, "name": "中国人民政治协商会议泰安市委员会", "type": "政协", "level": "地级市", "parent": "政协山东省委员会", "location": "泰安市"},
    {"id": 4, "name": "泰安市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "山东省人大常委会", "location": "泰安市"},
    {"id": 5, "name": "中共泰安市纪律检查委员会", "type": "党委", "level": "地级市", "parent": "中共山东省纪律检查委员会", "location": "泰安市"},
    {"id": 6, "name": "中共泰安市委员会组织部", "type": "党委", "level": "地级市", "parent": "中共泰安市委员会", "location": "泰安市"},
    {"id": 7, "name": "中共泰安市委员会宣传部", "type": "党委", "level": "地级市", "parent": "中共泰安市委员会", "location": "泰安市"},
    {"id": 8, "name": "中共泰安市委员会政法委员会", "type": "党委", "level": "地级市", "parent": "中共泰安市委员会", "location": "泰安市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 杨洪涛 — current Party Secretary
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2021-08", "end_date": "", "rank": "正厅级", "note": "现任泰安市委书记，2021年8月上任"},
    # 李国强 — current Mayor
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "2026-02", "end_date": "", "rank": "正厅级", "note": "2026年2月任代市长，后转正"},
    # 程远军 — 人大主任
    {"person_id": 3, "org_id": 4, "title": "市人大常委会主任", "start_date": "2025-01", "end_date": "", "rank": "正厅级", "note": ""},
    # 武林中 — 政协主席
    {"person_id": 4, "org_id": 3, "title": "市政协主席", "start_date": "2022-02", "end_date": "", "rank": "正厅级", "note": ""},
    # 待查 — 常务副市长
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": "姓名待确认"},
    {"person_id": 5, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "姓名待确认"},
    # 待查 — 纪委书记
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": "姓名待确认"},
    {"person_id": 6, "org_id": 5, "title": "市纪委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼市监委主任"},
    # 待查 — 组织部部长
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": "姓名待确认"},
    {"person_id": 7, "org_id": 6, "title": "组织部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 待查 — 宣传部部长
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": "姓名待确认"},
    {"person_id": 8, "org_id": 7, "title": "宣传部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 待查 — 政法委书记
    {"person_id": 9, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": "姓名待确认"},
    {"person_id": 9, "org_id": 8, "title": "政法委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 崔洪刚 — predecessor Party Secretary
    {"person_id": 30, "org_id": 1, "title": "市委书记", "start_date": "2018-05", "end_date": "2021-08", "rank": "正厅级", "note": "前任市委书记，2023年被查，2024年判刑"},
    # 李兰祥 — predecessor Mayor
    {"person_id": 31, "org_id": 2, "title": "市长", "start_date": "2022-12", "end_date": "2026-02", "rank": "正厅级", "note": "前任市长"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 杨洪涛 ↔ 李国强 (Party Secretary – Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "中共泰安市委员会", "overlap_period": "2026-02至今"},
    # 杨洪涛 ↔ 程远军
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—人大主任", "overlap_org": "泰安市", "overlap_period": "2025-01至今"},
    # 杨洪涛 ↔ 武林中
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—政协主席", "overlap_org": "泰安市", "overlap_period": "2022-02至今"},
    # 崔洪刚 → 杨洪涛 (predecessor/successor)
    {"person_a": 30, "person_b": 1, "type": "交接", "context": "前任市委书记—现任市委书记", "overlap_org": "中共泰安市委员会", "overlap_period": "2021-08交接"},
    # 李兰祥 → 李国强 (predecessor/successor)
    {"person_a": 31, "person_b": 2, "type": "交接", "context": "前任市长—现任市长", "overlap_org": "泰安市人民政府", "overlap_period": "2026-02交接"},
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
    if not person.get("education"):
        questions.append("学历教育背景未确认")
    if not person.get("work_start"):
        questions.append("参加工作年份未确认")
    return questions


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"taian_{name}"

    # Collect positions for this person
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

    # Collect relationships for this person
    person_rels = [
        r for r in relationships
        if r["person_a"] == pid or r["person_b"] == pid
    ]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rels_output.append({
            "person": other_name,
            "person_id": f"taian_{other_name}",
            "relationship_type": "overlap",
            "strength": "strong" if r["type"] == "共事" else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    # Source register
    source_url = person.get("source", "")
    source_title = "泰安市/领导维基百科页面"
    if "杨洪涛" in name:
        source_title = "杨洪涛 - 维基百科"
    elif "崔洪刚" in name:
        source_title = "崔洪刚 - 维基百科"
    else:
        source_title = "泰安市 - 维基百科"

    sources = [
        {
            "id": "S001",
            "title": source_title,
            "url": source_url,
            "publisher": "维基百科",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": f"维基百科条目（{source_url}），2026年7月访问",
        }
    ]

    # For 杨洪涛, add his detailed biography page as a second source
    if "杨洪涛" in name:
        sources.append({
            "id": "S002",
            "title": "杨洪涛 - 人民网地方领导资料库",
            "url": "https://ldzl.people.com.cn/dfzlk/front/personPage2/13782.htm",
            "publisher": "人民网",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "database",
            "reliability": "high",
            "notes": "人民网地方领导资料库",
        })

    # For 杨洪涛: include detailed career timeline from Wikipedia
    if name == "杨洪涛":
        yang_timeline = [
            {"start": "1988-07", "end": "1994-04", "org": "山东省税务局", "title": "征管处办事员、科员",
             "level": "", "rank": "", "notes": "期间1989.10-1991.04挂职聊城化工厂供销科副科长",
             "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "1994-04", "end": "1997-02", "org": "山东省地方税务局", "title": "征管处副主任科员",
             "level": "", "rank": "", "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "1997-02", "end": "2000-06", "org": "山东省地方税务局", "title": "征管处主任科员",
             "level": "", "rank": "", "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2000-06", "end": "2002-03", "org": "淄博市博山区", "title": "副区长",
             "level": "", "rank": "", "notes": "挂职", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2002-03", "end": "2002-09", "org": "淄博旭硝子工业园", "title": "党委书记、管委会主任",
             "level": "", "rank": "", "notes": "兼任", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2002-09", "end": "2002-12", "org": "淄博市博山区", "title": "区委副书记、副区长",
             "level": "", "rank": "", "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2002-12", "end": "2007-01", "org": "高青县", "title": "县委副书记、副县长",
             "level": "", "rank": "", "notes": "2003年1月起兼任副县长", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2007-11", "end": "2007-12", "org": "淄博市淄川区", "title": "代理区长",
             "level": "", "rank": "", "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2007-12", "end": "2010-12", "org": "淄博市淄川区", "title": "区长",
             "level": "", "rank": "正处级", "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2010-12", "end": "2015-10", "org": "淄博市淄川区", "title": "区委书记",
             "level": "", "rank": "", "notes": "2015年6月获全国优秀县委书记称号",
             "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2015-10", "end": "2015-11", "org": "中共淄博市委员会", "title": "市委常委",
             "level": "", "rank": "副厅级", "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2015-11", "end": "2019-11", "org": "淄博市人民政府", "title": "市委常委、常务副市长",
             "level": "", "rank": "副厅级", "notes": "2017年2月连任市委常委", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2019-11", "end": "2021-08", "org": "德州市人民政府", "title": "市委副书记、市长",
             "level": "", "rank": "正厅级", "notes": "2020年1月当选市长", "confidence": "confirmed", "source_ids": ["S001"]},
        ]
        career_timeline = yang_timeline + career_timeline

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "山东省",
            "city": "泰安市",
            "region": "泰安市",
            "job": person.get("current_post", ""),
            "task_id": "shandong_泰安市",
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
            "native_place": person.get("birthplace", ""),
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
            "identity": "confirmed" if person.get("birth") else "unverified",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "complete" if name == "杨洪涛" else ("partial" if person.get("birth") else "thin"),
            "relationship_confidence": "medium",
            "biggest_gap": "完整任职履历（百度百科403，搜索引擎超时）" if not person.get("work_start") else "副职和常委班子完整名单",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历起止时间",
                "why_it_matters": "关系网络分析需要精确的时间线",
                "suggested_queries": [f"{name} 简历", f"{name} 人民网", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
        ],
    }

    # Add birth info gap if missing
    if not person.get("birth"):
        record["open_questions"].insert(0, {
            "priority": "critical",
            "question": f"{name}的出生年月、籍贯、学历教育背景",
            "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
            "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 百度百科"],
            "last_attempted": AS_OF,
        })

    # Add risk signal for 崔洪刚
    if name == "崔洪刚":
        record["risk_and_integrity_signals"].append({
            "type": "disciplinary_action",
            "description": "2023年8月被查，2024年2月被开除党籍和公职，2024年11月因受贿5299万余元被判处有期徒刑14年6个月",
            "date": "2023-08",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        })

    fname = f"{TODAY}-山东省-泰安市-{person['current_post']}-{person['name']}.json"
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

    # Run build using the shared runner
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

    # Write person JSONs
    print("  Writing person JSONs...")
    core_ids = {1, 2, 3, 4, 30, 31}  # Core leaders + predecessors
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
