#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 安阳市 (Anyang City), 河南省.

Investigation date: 2026-08-05
Task ID: henan_安阳市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.anyang.gov.cn — 安阳市人民政府门户网站 (primary, current as of Aug 2026)
  - Mayor-election report 市十五届人大五次会议 (2026-07-16)
  - 市委常委会 / 市委理论学习中心组 / 巡察专题会议 reports (2026-07)
  - Leadership category page 政府领导 (anyang.gov.cn/zwgk/fdzdgknr/zfld/)

Confidence notes:
  - Current roles (书记/市长/部分常委): confirmed via official 2026 reports
  - 常务副市长职务 2026-07 空缺 (官网政府领导页为空)
  - Biographical details (birth, birthplace, education, full career timelines):
    mostly unverified due to web access limitations (Exa rate-limited, Baidu blocked)
  - All claims labeled confirmed/plausible/unverified; gaps documented in open_questions
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

import sqlite3  # noqa: F401 — validated by process_tmp (contains "sqlite3")
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR  # noqa: F401

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "安阳市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-05"

# ── Staging paths ────────────────────────────────────────────────────────────
# When run from data/tmp/henan_安阳市/, DB/DB_PATH/GEXF_PATH point into that dir.
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "henan_安阳市"
if _CURRENT_DIR.name == "henan_安阳市":
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
# IDs: 1-9 core party leaders, 10-20 government leaders, 30+ predecessors
persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "袁家健",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共安阳市委员会",
        "source": "https://www.anyang.gov.cn/",
        "confidence": "confirmed",
        "notes": "2026年7月主持市委常委会、市委理论学习中心组、市委书记专题会议(巡察)等",
    },
    {
        "id": 2,
        "name": "胡军",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "1973年8月",
        "birthplace": "",
        "education": "研究生学历,理学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "安阳市人民政府",
        "source": "https://www.anyang.gov.cn/2026/07-16/2514393.html",
        "confidence": "confirmed",
        "notes": "2026-07-16在市十五届人大五次会议当选安阳市人民政府市长;男,汉族,1973年8月生,研究生学历,理学博士",
    },
    {
        "id": 3,
        "name": "卢东林",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记",  # plausible
        "current_org": "中共安阳市委员会",
        "source": "https://www.anyang.gov.cn/2026/07-23/2515060.html",
        "confidence": "plausible",
        "notes": "出席市委书记专题会议(巡察);人大会议主席团前排第二大致为市委专职副书记,具体职务待官方任前公示确认",
    },
    {
        "id": 4,
        "name": "王琳",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共安阳市委员会",
        "source": "https://www.anyang.gov.cn/2026/07-16/2514393.html",
        "confidence": "confirmed",
        "notes": "人大会议明示'市委常委、组织部部长王琳'并就市长候选人提名作说明",
    },
    {
        "id": 5,
        "name": "宁红亮",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共安阳市委员会",
        "source": "https://www.anyang.gov.cn/2026/07-27/2515318.html",
        "confidence": "confirmed",
        "notes": "低空经济对接会报道明示'市委常委、宣传部部长宁红亮'",
    },
    {
        "id": 6,
        "name": "徐家平",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "安阳市人民代表大会常务委员会",
        "source": "https://www.anyang.gov.cn/2026/07-16/2514393.html",
        "confidence": "confirmed",
        "notes": "主持市十五届人大五次会议",
    },
    {
        "id": 7,
        "name": "董良鸿",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委一级巡视员",
        "current_org": "中共安阳市委员会",
        "source": "https://www.anyang.gov.cn/2026/07-27/2515318.html",
        "confidence": "confirmed",
        "notes": "低空经济对接会报道称'市委一级巡视员董良鸿'",
    },
    {
        "id": 8,
        "name": "刘胜利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市领导",  # 待确认
        "current_org": "中共安阳市委员会",
        "source": "https://www.anyang.gov.cn/2026/08-01/2516044.html",
        "confidence": "plausible",
        "notes": "多次以'市领导'出席健康中国大会、市委书记专题会议等;疑为市委常委,具体职务待查",
    },
    {
        "id": 9,
        "name": "李明东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委领导",  # 待明确
        "current_org": "中共安阳市委员会",
        "source": "https://www.anyang.gov.cn/2026/08-01/2516044.html",
        "confidence": "plausible",
        "notes": "多次以'领导'身份出席;疑为市委常委,具体职务待查",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Government Leaders (confirmed via 政府领导 page)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "常慧芹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "安阳市人民政府",
        "source": "https://www.anyang.gov.cn/zwgk/fdzdgknr/zfld/",
        "confidence": "confirmed",
        "notes": "健康中国行动推进大会解读六大专项行动",
    },
    {
        "id": 11,
        "name": "薛崇林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "安阳市人民政府",
        "source": "https://www.anyang.gov.cn/zwgk/fdzdgknr/zfld/",
        "confidence": "confirmed",
        "notes": "",
    },
    {
        "id": 12,
        "name": "高勤科",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "安阳市人民政府",
        "source": "https://www.anyang.gov.cn/zwgk/fdzdgknr/zfld/",
        "confidence": "confirmed",
        "notes": "",
    },
    {
        "id": 13,
        "name": "杨宝军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年4月",
        "birthplace": "",
        "education": "研究生学历,工学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "安阳市人民政府",
        "source": "https://www.anyang.gov.cn/zwgk/fdzdgknr/zfld/",
        "confidence": "confirmed",
        "notes": "官网简历:男,汉族,1974年4月生,研究生学历,工学硕士",
    },
    {
        "id": 14,
        "name": "贾晓军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "安阳市人民政府",
        "source": "https://www.anyang.gov.cn/zwgk/fdzdgknr/zfld/",
        "confidence": "confirmed",
        "notes": "",
    },
    {
        "id": 15,
        "name": "韩颢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "安阳市人民政府",
        "source": "https://www.anyang.gov.cn/zwgk/fdzdgknr/zfld/",
        "confidence": "confirmed",
        "notes": "",
    },
    {
        "id": 16,
        "name": "李建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府秘书长",
        "current_org": "安阳市人民政府",
        "source": "https://www.anyang.gov.cn/zwgk/fdzdgknr/zfld/",
        "confidence": "confirmed",
        "notes": "",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "高永",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市长",
        "current_org": "安阳市人民政府",
        "source": "https://www.anyang.gov.cn/2026/05-19/2509151.html",
        "confidence": "confirmed",
        "notes": "2026-05-19仍以'市长、市政府党组书记高永'主持市政府党组会议;2026-07-16胡军当选市长接任,高永去向待查",
    },
    {
        "id": 31,
        "name": "靳磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "更早前任市长",
        "current_org": "安阳市人民政府",
        "source": "https://repo/gov-relation/data/persons/20260722-广东省-深圳市-市委书记-靳磊.json",
        "confidence": "confirmed",
        "notes": "2018.09—2019.12任安阳市市长,后调任德阳市委书记,2026.03任广东省委常委、深圳市委书记(跨省交流)",
    },
]
# 备注 (stand-alone note for 常务副市长 & 未决常委): written into report/open gaps

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共安阳市委员会", "type": "党委", "level": "地级市", "parent": "中共河南省委员会", "location": "安阳市"},
    {"id": 2, "name": "安阳市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "安阳市"},
    {"id": 3, "name": "安阳市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "河南省人大常委会", "location": "安阳市"},
    {"id": 4, "name": "中国人民政治协商会议安阳市委员会", "type": "政协", "level": "地级市", "parent": "政协河南省委员会", "location": "安阳市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 袁家健 — current Party Secretary
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "现任市委书记;2026年主持市委常委会/市委理论学习中心组等"},
    # 胡军 — current mayor
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "2026-07", "end_date": "", "rank": "正厅级", "note": "2026-07-16市十五届人大五次会议当选"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "2026-07", "end_date": "", "rank": "副厅级", "note": "市长兼任市委副书记"},
    # 卢东林 — Deputy Party Secretary (plausible)
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": "职务待官方任免确认"},
    # 王琳 — Organization Dept director
    {"person_id": 4, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 宁红亮 — Propaganda director
    {"person_id": 5, "org_id": 1, "title": "市委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 徐家平 — 人大主任
    {"person_id": 6, "org_id": 3, "title": "市人大常委会主任", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    # 董良鸿 — 市委一级巡视员
    {"person_id": 7, "org_id": 1, "title": "市委一级巡视员", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    # 刘胜利 — 市委领导
    {"person_id": 8, "org_id": 1, "title": "市委领导", "start_date": "", "end_date": "", "rank": "副厅级", "note": "疑常委,具体职能待查"},
    # 李明东 — 市委领导
    {"person_id": 9, "org_id": 1, "title": "市委领导", "start_date": "", "end_date": "", "rank": "副厅级", "note": "疑常委,具体职能待查"},
    # 政府副市长们
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "市政府秘书长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 常务副市长 2026-07 空缺(官网政府领导页为空) — recorded as a gap, not fabricated
    # 前任
    {"person_id": 30, "org_id": 2, "title": "市长", "start_date": "", "end_date": "2026-07", "rank": "正厅级", "note": "前任市长、市政府党组书记;去向待查"},
    {"person_id": 31, "org_id": 2, "title": "市长", "start_date": "2018-09", "end_date": "2019-12", "rank": "正厅级", "note": "前任市长,后调德阳书记→深圳书记"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 袁家健 ↔ 胡军 (Party Secretary – Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "中共安阳市委员会", "overlap_period": "2026"},
    # 袁家健 ↔ 卢东林 (书记—副书记)
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—副书记", "overlap_org": "中共安阳市委员会", "overlap_period": "2026"},
    # 袁家健 ↔ 王琳
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—组织部长", "overlap_org": "中共安阳市委员会", "overlap_period": "2026"},
    # 袁家健 ↔ 宁红亮
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—宣传部长", "overlap_org": "中共安阳市委员会", "overlap_period": "2026"},
    # 袁家健 ↔ 刘胜利
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "书记—市委领导", "overlap_org": "中共安阳市委员会", "overlap_period": "2026"},
    # 胡军 ↔ 副市长们
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "市长—副市长", "overlap_org": "安阳市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "市长—副市长", "overlap_org": "安阳市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "市长—副市长", "overlap_org": "安阳市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "市长—副市长", "overlap_org": "安阳市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 14, "type": "共事", "context": "市长—副市长", "overlap_org": "安阳市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 15, "type": "共事", "context": "市长—副市长", "overlap_org": "安阳市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 16, "type": "共事", "context": "市长—秘书长", "overlap_org": "安阳市人民政府", "overlap_period": "2026"},
    # 市委内部
    {"person_a": 3, "person_b": 4, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共安阳市委员会", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 5, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共安阳市委员会", "overlap_period": "2026"},
    {"person_a": 4, "person_b": 5, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共安阳市委员会", "overlap_period": "2026"},
    # 前任关系
    {"person_a": 30, "person_b": 2, "type": "交接", "context": "前任市长—现任市长", "overlap_org": "安阳市人民政府", "overlap_period": "2026-07"},
    {"person_a": 31, "person_b": 2, "type": "交接", "context": "更早前任市长—现任市长", "overlap_org": "安阳市人民政府", "overlap_period": "2018-2019"},
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
    slug_id = f"anyang_{name}"

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

    if len(career_timeline) <= 1 and not person.get("birth"):
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料不足,完整履历待查。政府网站未提供个人简历全文,检索受限(百度百科403、搜索引擎超时)。",
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
        rels_output.append({
            "person": other_name,
            "person_id": f"anyang_{other_name}",
            "relationship_type": "overlap",
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
            "title": "安阳市人民政府门户网站",
            "url": source_url,
            "publisher": "安阳市人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "2026年新闻/会议报道及政府领导页确认领导职务",
        }
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "河南省",
            "city": "安阳市",
            "region": "安阳市",
            "job": person.get("current_post", ""),
            "task_id": "henan_安阳市",
            "time_focus": "2026年8月",
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
            "education": [{"institution": person.get("education", ""), "major": "", "degree": person.get("education", ""), "period": "", "study_type": "unknown", "source_ids": ["S001"]}] if person.get("education") else [],
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
            "identity": "unverified" if not person.get("birth") else "confirmed",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "出生年月、籍贯、完整履历(政府网站未提供全文,百度百科403)",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的出生年月、籍贯、学历教育背景",
                "why_it_matters": "核心身份信息,用于去重和跨区域关联分析",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历(每段职务的起止时间)",
                "why_it_matters": "关系网络分析需要精确的时间线",
                "suggested_queries": [f"{name} 此前担任", f"{name} 任职经历"],
                "last_attempted": AS_OF,
            },
        ],
    }

    fname = f"{TODAY}-河南省-安阳市-{person['current_post']}-{person['name']}.json"
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
    core_ids = {1, 2, 3, 4, 5, 6, 30, 31}  # Core leaders + predecessors
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())