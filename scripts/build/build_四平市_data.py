#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 四平市 (Siping City), 吉林省.

Investigation date: 2026-08-03
Task ID: jilin_四平市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.siping.gov.cn — 四平市人民政府官方网站 (primary, confirmed as of 2026-08-03)
  - Homepage leadership section confirms 王相民 as 市委书记 and 陈德明 as 市长
  - Government site homepage news and meeting reports (July-August 2026)
  - Web search was degraded: Baidu Baike 403, Exa rate-limited, Google/Bing blocked/timeout

Confidence notes:
  - Current roles: confirmed via government official homepage (2026-08-03)
  - 王相民: "1970年5月出生, 吉林镇赉人, 中共党员, 硕士研究生" — confirmed from official bio
  - 陈德明: "1969年4月生, 吉林扶余人, 1994年7月参加工作, 大学学历工学学士" — confirmed from official bio
  - Biographical details (education, full career timeline): partially unverified due to web access limitations
  - 郭灵计 as predecessor (~2021-2024) → 湖南省委组织部部长 — confirmed via cross-province report
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
SLUG = "四平市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-03"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_四平市"
if _CURRENT_DIR.name == "jilin_四平市":
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
# IDs: 1-2 core leaders (current), 3-9 standing committee, 10-16 deputy mayors,
#      17-20人大/政协, 21-22 predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "王相民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年5月",
        "birthplace": "吉林镇赉",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "1992年7月",
        "current_post": "市委书记",
        "current_org": "中共四平市委员会",
        "source": "http://www.siping.gov.cn/",
        "confidence": "confirmed",
        "notes": "1970年5月出生, 汉族, 吉林镇赉人, 1996年6月入党, 1992年7月参加工作, 硕士研究生学历。现任四平市委书记。2026年7月多次主持市委常委会会议、调研吉林师范大学校地合作、走访慰问驻平部队。此前任职经历和完整履历受限。"
    },
    {
        "id": 2,
        "name": "陈德明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年4月",
        "birthplace": "吉林扶余",
        "education": "大学学历工学学士",
        "native_place": "吉林扶余",
        "party_join": "中共党员",
        "work_start": "1994年7月",
        "current_post": "市长",
        "current_org": "四平市人民政府",
        "source": "http://www.siping.gov.cn/",
        "confidence": "confirmed",
        "notes": "1969年4月生, 汉族, 吉林扶余人, 1994年7月参加工作, 1992年9月入党, 大学学历, 工学学士。现任四平市委副书记、市长, 市政府党组书记。2026年7月调研重点工业企业、主持召开上半年经济运行分析会议、市政府党组会议。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 四平市人大/政协/监委领导 (from 2026年1月市人大会议)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "刘宝双",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "四平市人民代表大会常务委员会",
        "source": "http://www.siping.gov.cn/",
        "confidence": "confirmed",
        "notes": "2026年1月14日在四平市第九届人民代表大会第六次会议上当选为市人大常委会副主任。"
    },
    {
        "id": 4,
        "name": "毕志杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会秘书长",
        "current_org": "四平市人民代表大会常务委员会",
        "source": "http://www.siping.gov.cn/",
        "confidence": "confirmed",
        "notes": "2026年1月14日当选为市人大常委会秘书长。此前曾任梨树县委副书记、县长。是梨树县委常委会成员，与赵光辉(县委书记)为党政搭档。"
    },
    {
        "id": 5,
        "name": "沈静兰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市监察委员会主任",
        "current_org": "四平市监察委员会",
        "source": "http://www.siping.gov.cn/",
        "confidence": "confirmed",
        "notes": "2026年1月14日当选为市监察委员会主任。"
    },
    {
        "id": 6,
        "name": "张怀胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市中级人民法院院长",
        "current_org": "四平市中级人民法院",
        "source": "http://www.siping.gov.cn/",
        "confidence": "confirmed",
        "notes": "2026年1月14日当选为市中级人民法院院长。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 四平市副市长 (from official news — 市政府领导班子)
    # 新闻提到"陈德明调研重点工业企业", 四平市副市长名单待补充
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 7,
        "name": "张恒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "四平市人民政府",
        "source": "伊通县调查数据(本地数据)",
        "confidence": "confirmed",
        "notes": "曾任伊通满族自治县委书记(2021年7月前), 后升任四平市副市长。从伊通县委书记直提四平市副市长是最典型的县→市级提拔案例。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessor — 市委书记
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 8,
        "name": "郭灵计",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年",
        "birthplace": "山西隰县",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "湖南省委组织部部长",
        "current_org": "中共湖南省委组织部",
        "source": "report/20260714-湖南省-跨省干部交流.md (本地repo报告)",
        "confidence": "confirmed",
        "notes": "曾任四平市委书记(~2021-2024), 后调任湖南省委组织部部长。1968年生, 山西隰县人, 中央党校研究生学历。这是吉林省→湖南省的重要跨省干部交流案例。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessor — 市长
    # 据公开新闻, 之前市长为胡斌(?)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 9,
        "name": "胡斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "卸任",
        "current_org": "",
        "source": "新闻报道",
        "confidence": "plausible",
        "notes": "推测为陈德明之前的四平市长。据报道胡斌曾任四平市长, 后调任吉林省体育局局长或省直部门。具体去向待查。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共四平市委员会", "type": "党委", "level": "地级市", "parent": "中共吉林省委员会", "location": "四平市"},
    {"id": 2, "name": "四平市人民政府", "type": "政府", "level": "地级市", "parent": "吉林省人民政府", "location": "四平市"},
    {"id": 3, "name": "四平市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "吉林省人大常委会", "location": "四平市"},
    {"id": 4, "name": "四平市监察委员会", "type": "党委", "level": "地级市", "parent": "吉林省监察委员会", "location": "四平市"},
    {"id": 5, "name": "四平市中级人民法院", "type": "政府", "level": "地级市", "parent": "吉林省高级人民法院", "location": "四平市"},
    {"id": 6, "name": "政协四平市委员会", "type": "政协", "level": "地级市", "parent": "政协吉林省委员会", "location": "四平市"},
    {"id": 7, "name": "中共湖南省委组织部", "type": "党委", "level": "省级", "parent": "中共湖南省委员会", "location": "长沙市"},
    {"id": 8, "name": "中共吉林省委组织部", "type": "党委", "level": "省级", "parent": "中共吉林省委员会", "location": "长春市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 王相民 — current Party Secretary
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "现任四平市委书记, 主持市委全面工作。1970年5月生, 吉林镇赉人。"},
    # 陈德明 — current mayor
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "现任四平市委副书记、市长、市政府党组书记, 领导市政府全面工作。"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "兼任市委副书记。"},
    # 刘宝双 — 人大副主任
    {"person_id": 3, "org_id": 3, "title": "市人大常委会副主任", "start_date": "2026-01-14", "end_date": "", "rank": "副厅级", "note": "2026年1月14日当选。"},
    # 毕志杰 — 人大秘书长
    {"person_id": 4, "org_id": 3, "title": "市人大常委会秘书长", "start_date": "2026-01-14", "end_date": "", "rank": "正处级", "note": "2026年1月14日当选。此前任梨树县委副书记、县长。"},
    {"person_id": 4, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "2026-01", "rank": "县处级正职", "note": "2026年1月前的曾任岗位。梨树县委副书记、县长。"},
    # 沈静兰 — 监委主任
    {"person_id": 5, "org_id": 4, "title": "市监察委员会主任", "start_date": "2026-01-14", "end_date": "", "rank": "副厅级", "note": "2026年1月14日当选。"},
    # 张怀胜 — 中院院长
    {"person_id": 6, "org_id": 5, "title": "市中级人民法院院长", "start_date": "2026-01-14", "end_date": "", "rank": "副厅级", "note": "2026年1月14日当选。"},
    # 张恒 — 副市长
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "2021年7月从伊通县委书记升任四平市副市长。"},
    {"person_id": 7, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "2021-07", "rank": "正处级", "note": "曾任伊通满族自治县委书记。"},
    # 郭灵计 — 前任市委书记
    {"person_id": 8, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "四平市委原书记(~2021-2024), 后调任湖南省委组织部部长。"},
    {"person_id": 8, "org_id": 7, "title": "部长", "start_date": "", "end_date": "", "rank": "副省级", "note": "现任湖南省委组织部部长。"},
    # 胡斌 — 前任市长
    {"person_id": 9, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "四平市原市长, 早于陈德明任职。具体任期和去向待查。"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 王相民 ↔ 陈德明 (Party Secretary – Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "中共四平市委员会", "overlap_period": "2024-至今"},
    # 王相民 ↔ 刘宝双
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—人大副主任", "overlap_org": "四平市领导班子", "overlap_period": "2026"},
    # 王相民 ↔ 毕志杰
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—人大秘书长", "overlap_org": "四平市领导班子", "overlap_period": "2026"},
    # 王相民 ↔ 沈静兰
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—监委主任", "overlap_org": "四平市领导班子", "overlap_period": "2026"},
    # 王相民 ↔ 张怀胜
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "书记—中院院长", "overlap_org": "四平市领导班子", "overlap_period": "2026"},
    # 王相民 ↔ 张恒
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "书记—副市长(下属)", "overlap_org": "四平市领导班子", "overlap_period": "2026"},
    # 陈德明 ↔ 张恒 (Mayor – Deputy Mayor)
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "市长—副市长", "overlap_org": "四平市人民政府", "overlap_period": "2026"},
    # 王相民 ↔ 郭灵计 (predecessor-successor)
    {"person_a": 1, "person_b": 8, "type": "前后任", "context": "王相民是郭灵计的继任者, 郭灵计调任湖南组织部部长", "overlap_org": "中共四平市委员会", "overlap_period": "约2024"},
    # 陈德明 ↔ 胡斌 (可能的前后任)
    {"person_a": 2, "person_b": 9, "type": "前后任", "context": "胡斌为陈德明前的四平市长(推测), 具体继任时间点和去向待查", "overlap_org": "四平市人民政府", "overlap_period": ""},
    # 毕志杰 ↔ 郭灵计 (梨树县长→市人大秘书长)
    {"person_a": 4, "person_b": 8, "type": "上下级", "context": "毕志杰任梨树县长(县处级)时为郭灵枪(市委书记)的下属", "overlap_org": "四平市", "overlap_period": ""},
    # 张恒 ↔ 郭灵计 (之前下属关系)
    {"person_a": 7, "person_b": 8, "type": "上下级", "context": "张任伊通县委书记时, 郭灵计为四平市委书记(上级)", "overlap_org": "四平市", "overlap_period": ""},
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
    return questions


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"siping_{name}"

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
            "confidence": "confirmed" if person.get("confidence") == "confirmed" and pos.get("start_date") else "plausible",
            "source_ids": ["S001"],
        })

    # Add gap entry if sparse
    if len(career_timeline) <= 2:
        if not person.get("birth") or not person.get("work_start"):
            career_timeline.append({
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": "公开资料不足, 完整履历待查。政府网站首页仅提供简要学历, 未提供完整历任职务。百度百科403禁止访问, 搜索引擎超时。",
                "confidence": "unverified",
                "source_ids": [],
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
            "person_id": f"siping_{other_name}",
            "relationship_type": "overlap" if r["type"] == "共事" else "predecessor_successor" if r["type"] == "前后任" else "superior_subordinate",
            "strength": "strong" if r["type"] in ("共事", "前后任") else "medium",
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
            "title": "四平市人民政府官方网站",
            "url": "http://www.siping.gov.cn/",
            "publisher": "四平市人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "2026年8月政府网站首页领导栏目和会议报道确认领导职务",
        },
        {
            "id": "S002",
            "title": "四平市第九届人民代表大会第六次会议公告",
            "url": "http://www.siping.gov.cn/",
            "publisher": "四平市人民代表大会常务委员会",
            "published_at": "2026-01-14",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认刘宝双、毕志杰、沈静兰、张怀胜当选职务",
        },
    ]

    # Add predecessor source if applicable
    if person["id"] == 8:
        sources.append({
            "id": "S003",
            "title": "湖南省跨省干部交流报告",
            "url": "report/20260714-湖南省-跨省干部交流.md",
            "publisher": "本地调查报告",
            "published_at": "2026-07-14",
            "accessed_at": AS_OF,
            "source_type": "database",
            "reliability": "medium",
            "notes": "确认郭灵计从四平市委书记调任湖南省委组织部部长",
        })

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "吉林省",
            "city": "四平市",
            "region": "四平市",
            "job": person.get("current_post", ""),
            "task_id": "jilin_四平市",
            "time_focus": "2026年7-8月",
        },
        "identity": {
            "person_id": slug_id,
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("native_place", ""),
            "education": [
                {
                    "period": "",
                    "institution": person.get("education", "") if person.get("education") else "",
                    "major": "",
                    "degree": person.get("education", ""),
                    "study_type": "unknown",
                    "source_ids": ["S001"],
                }
            ] if person.get("education") else [],
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
        "governance_record": [
            {
                "period": "2026-07",
                "domain": "public_security",
                "achievement_or_event": "走访慰问部分驻平部队和市消防救援支队并召开座谈会",
                "role_in_event": "共同出席",
                "measurable_outcome": "",
                "location": "四平市",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "period": "2026-07",
                "domain": "education",
                "achievement_or_event": "到吉林师范大学调研并召开校地战略合作座谈会",
                "role_in_event": "调研",
                "measurable_outcome": "",
                "location": "四平市",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "period": "2026-07",
                "domain": "economic_development",
                "achievement_or_event": "启迪科技园（四平）暨四平市国际贸易园区启动仪式举行",
                "role_in_event": "出席",
                "measurable_outcome": "",
                "location": "四平市",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
        ] if person["id"] in (1, 2) else [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": list(set(
                o.get("type", "") for o in organizations if o["id"] in [pos["org_id"] for pos in person_positions]
            )),
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "pragmatic",
                    "evidence": "2026年7月多次主持市委常委会和理论学习中心组会议, 部署经济运行和城市建设工作",
                    "confidence": "plausible",
                    "source_ids": ["S001"],
                }
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "公开渠道未发现该人员的纪律处分、审查调查或负面报道",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": ["S001"],
            }
        ] if person["id"] in (1, 2) else [],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "unverified",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "完整履历（此前任职经历）——百度百科403, 搜索引擎超时" if person["id"] in (1, 2) else "部分身份信息待确认",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历",
                "why_it_matters": "关系网络分析需要精确的时间线和历任职务",
                "suggested_queries": [f"{name} 简历 四平", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{name}的教育背景细节（毕业院校、专业）",
                "why_it_matters": "有助于识别校友网络关系",
                "suggested_queries": [f"{name} 毕业", f"{name} 学历"],
                "last_attempted": AS_OF,
            },
        ],
    }

    fname = f"{TODAY}-吉林省-四平市-{person['current_post']}-{person['name']}.json"
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
    core_ids = {1, 2, 3, 4, 5, 6, 7, 8}  # Core figures
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())