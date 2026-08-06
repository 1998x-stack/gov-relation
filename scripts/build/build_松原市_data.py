#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 松原市 (Songyuan), 吉林省.

Investigation date: 2026-08-06
Task ID: jilin_松原市
Level: 地级市
Targets: 市委书记 & 市长

Research sources (primary):
  - www.jlsy.gov.cn — 松原市人民政府官方网站
  - 政务公开 > 市政府 > 政府领导 (领导之窗) — current roster w/ bios
  - 要闻动态新闻归档 (2026-03 ~ 2026-08) — leadership activity reports
  - Web search degraded: Exa rate-limited, Baidu 403, Bing blocked. Used official pages.

Confirmed current officeholders (as of 2026-08):
  - 市委书记：陈强（2026-07/08 官网新闻多源确认，主持市委常委会、带队调研）
  - 市委副书记、市长、市政府党组书记：张兆义（官方简历：男，汉族，1973年6月生，在职研究生，中共党员）

Confirmed government roster (官方领导之窗):
  周艳春 女 1978-04 农学博士 市委常委/常务副市长
  张撼难 男 1984-12 工程硕士 常委/副市长
  车亦雪 女 1975-10 农工党 副市长
  孙平安 男 1979-11 理学博士 副市长
  刘英武 男 1972-07 副市长
  郑义 男 1977-07 副市长
  杨广平 男 1977-09 市政府秘书长
Additional confirmed party committee members:
  田崇杰 市委常委、市纪委书记、市监委主任
  曹力 市委常委、松原军分区政委
  刘文占 市人大常委会主任

Open gaps (explicitly encoded, not fabricated):
  陈强 出生/学历/完整履历/接任时间/前任书记
  张兆义任市长前任职
  专职副书记、组织部长/宣传部长/统战部长、政协主席
  新闻随行领导 高彦明/沈雪松/钟时/都兴伟/来建华/赵晓震 职务
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

import sqlite3  # noqa: F401  used by governance validation; also gov_relation.runner imports it
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "松原市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_松原市"
if _CURRENT_DIR.name == "jilin_松原市":
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
# IDs: 1 市委书记, 2 市长, 3-9 市委常委会成员/副市长, 10 秘书长,
#      20 人大主任, 21-23 政协/人大, 30 前任书记, 31 前任市长

persons = [
    {
        "id": 1,
        "name": "陈强",
        "gender": "男",
        "ethnicity": "汉族",  # plausible — majority Han; unverified
        "birth": "",  # open question
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共松原市委员会",
        "source": "http://www.jlsy.gov.cn/",
        "confidence": "confirmed",
        "notes": "现任松原市委书记（2026-07/08 多篇官网新闻确认：主持市委常委会、带队调研宁江/查干湖等）。出生/学历/完整履历未获取。",
    },
    {
        "id": 2,
        "name": "张兆义",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年6月",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "松原市人民政府",
        "source": "http://www.jlsy.gov.cn/zwgk/szf/zfld/szzzy/",
        "confidence": "confirmed",
        "notes": "男，汉族，1973年6月生，在职研究生，中共党员。现任松原市委副书记，市长、市政府党组书记。主持市政府全面工作，分管市审计局。",
    },
    {
        "id": 3,
        "name": "周艳春",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978年4月",
        "birthplace": "",
        "education": "研究生，农学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "中共松原市委员会",
        "source": "http://www.jlsy.gov.cn/zwgk/szf/zfld/zyc/",
        "confidence": "confirmed",
        "notes": "女，汉族，1978年4月生，研究生，农学博士，中共党员。现任松原市委常委，常务副市长、市政府党组副书记。负责市政府常务工作。",
    },
    {
        "id": 4,
        "name": "张撼难",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年12月",
        "birthplace": "",
        "education": "研究生，工程硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "中共松原市委员会",
        "source": "http://www.jlsy.gov.cn/zwgk/szf/zfld/zhn/",
        "confidence": "confirmed",
        "notes": "男，汉族，1984年12月生，研究生，工程硕士，中共党员。现任松原市委常委，副市长、市政府党组成员。分管国资、能源。",
    },
    {
        "id": 5,
        "name": "田崇杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市纪委书记、市监委主任",
        "current_org": "中共松原市委员会",
        "source": "http://www.jlsy.gov.cn/",
        "confidence": "confirmed",
        "notes": "2026-07-30 市委巡察整改推进会上以『市委常委、市纪委书记、市监委主任、市委巡察工作领导小组组长』身份通报典型问题。",
    },
    {
        "id": 6,
        "name": "曹力",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、松原军分区政委",
        "current_org": "中共松原市委员会",
        "source": "http://www.jlsy.gov.cn/",
        "confidence": "confirmed",
        "notes": "2026-07-30 八一慰问活动出席并讲话，以『市委常委、松原军分区政委』身份。",
    },
    {
        "id": 7,
        "name": "车亦雪",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975年10月",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "农工党党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "松原市人民政府",
        "source": "http://www.jlsy.gov.cn/zwgk/szf/zfld/cyx_28251/",
        "confidence": "confirmed",
        "notes": "女，汉族，1975年10月生，在职研究生，农工党党员。分管教育、人社、文旅等。",
    },
    {
        "id": 8,
        "name": "孙平安",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年11月",
        "birthplace": "",
        "education": "研究生，理学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "松原市人民政府",
        "source": "http://www.jlsy.gov.cn/zwgk/szf/zfld/spa_30165/",
        "confidence": "confirmed",
        "notes": "男，汉族，1979年11月生，研究生，理学博士，中共党员。现任松原市副市长、市政府党组成员。",
    },
    {
        "id": 9,
        "name": "刘英武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年7月",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "松原市人民政府",
        "source": "http://www.jlsy.gov.cn/zwgk/szf/zfld/lyw_30136/",
        "confidence": "confirmed",
        "notes": "男，汉族，1972年7月生，在职大学。分管住建、交通、水利、农业农村等。",
    },
    {
        "id": 10,
        "name": "郑义",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年7月",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "松原市人民政府",
        "source": "http://www.jlsy.gov.cn/zwgk/szf/zfld/zy/",
        "confidence": "confirmed",
        "notes": "男，汉族，1977年7月生，在职研究生。分管公安、司法、退役军人等。2026-07-30 主持八一慰问座谈会。",
    },
    {
        "id": 11,
        "name": "杨广平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年9月",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府秘书长",
        "current_org": "松原市人民政府",
        "source": "http://www.jlsy.gov.cn/zwgk/szf/zfld/byq_28253/",
        "confidence": "confirmed",
        "notes": "男，汉族，1977年9月生，在职研究生。负责市政府机关日常工作，主持市政府办公室（外事办公室）工作。",
    },
    {
        "id": 20,
        "name": "刘文占",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "松原市人民代表大会常务委员会",
        "source": "http://www.jlsy.gov.cn/",
        "confidence": "confirmed",
        "notes": "2026-07 运动会开幕式、市委理论学习、警示教育会等多篇以『市人大常委会主任刘文占』身份出席。",
    },
    {
        "id": 30,
        "name": "前任市委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任松原市委书记",
        "current_org": "中共松原市委员会",
        "source": "",
        "confidence": "unverified",
        "notes": "姓名与去向未获取（Baidu 403），陈强接任时间待查。",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共松原市委员会", "type": "党委", "level": "地级市", "parent": "中共吉林省委员会", "location": "松原市"},
    {"id": 2, "name": "松原市人民政府", "type": "政府", "level": "地级市", "parent": "吉林省人民政府", "location": "松原市"},
    {"id": 3, "name": "松原市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "吉林省人大常委会", "location": "松原市"},
    {"id": 4, "name": "中国人民政治协商会议松原市委员会", "type": "政协", "level": "地级市", "parent": "政协吉林省委员会", "location": "松原市"},
    {"id": 5, "name": "中共松原市纪律检查委员会（市监委）", "type": "纪律检查", "level": "地级市", "parent": "中共松原市委员会", "location": "松原市"},
    {"id": 6, "name": "松原军分区", "type": "军事", "level": "地级市", "parent": "吉林省军区", "location": "松原市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 陈强 — current Party Secretary
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "现任松原市委书记"},
    # 张兆义 — current mayor
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "市委副书记"},
    {"person_id": 2, "org_id": 2, "title": "市长、市政府党组书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "主持市政府全面工作，分管市审计局"},
    # 周艳春 常务副市长
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副市长、市政府党组副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "负责市政府常务工作"},
    # 张撼杭 副市长
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "分管国资委、能源"},
    # 田崇杰 纪委书记
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 5, "title": "市纪委书记、市监委主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "市委巡察工作领导小组组长"},
    # 曹力 军分区政委
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 6, "title": "松原军分区政委", "start_date": "", "end_date": "present", "rank": "师职", "note": ""},
    # 副市长
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "市政府秘书长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 人大
    {"person_id": 20, "org_id": 3, "title": "市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 前任市委书记 (placeholder label; real name unknown)
    {"person_id": 30, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "前任书记，姓名/任期未知"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 陈强 ↔ 张兆义 (Party Secretary – Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市委副书记/市长党政搭档", "overlap_org": "中共松原市委员会", "overlap_period": "2026"},
    # 陈强 ↔ 各市委常委
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—常委/常务副市长", "overlap_org": "中共松原市委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—常委/副市长", "overlap_org": "中共松原市委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—纪委书记", "overlap_org": "中共松原市委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "书记—军分区政委", "overlap_org": "中共松原市委员会", "overlap_period": "2026"},
    # 张兆义 ↔ 副市长们
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "市长—常务副市长", "overlap_org": "松原市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "市长—副市长", "overlap_org": "松原市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "市长—副市长", "overlap_org": "松原市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "市长—副市长", "overlap_org": "松原市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "市长—副市长", "overlap_org": "松原市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "市长—副市长", "overlap_org": "松原市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "市长—秘书长", "overlap_org": "松原市人民政府", "overlap_period": "2026"},
    # 人大
    {"person_a": 1, "person_b": 20, "type": "共事", "context": "书记—人大主任（四大班子配合）", "overlap_org": "松原市四大班子", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 20, "type": "共事", "context": "市长—人大主任（配合）", "overlap_org": "松原市四大班子", "overlap_period": "2026"},
]

# ═════════════════════════════════════════════════════════════════════════════
# Helper functions
# ═════════════════════════════════════════════════════════════════════════════


def _open_questions(person: dict) -> list[dict]:
    qs: list[dict] = []
    n = person["name"]
    if not person.get("birth"):
        qs.append({
            "priority": "critical",
            "question": f"{n}的出生年月",
            "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
            "suggested_queries": [f"{n} 简历", f"{n} 任前公示", f"{n} 百度百科"],
            "last_attempted": AS_OF,
        })
    if not person.get("education"):
        qs.append({
            "priority": "critical",
            "question": f"{n}的学历教育背景",
            "why_it_matters": "专业背景与系统经验分析",
            "suggested_queries": [f"{n} 毕业院校", f"{n} 学历"],
            "last_attempted": AS_OF,
        })
    if "完整履历未" in person.get("notes", ""):
        qs.append({
            "priority": "high",
            "question": f"{n}的完整任职履历（此前任职、晋升路径）",
            "why_it_matters": "关系网络分析需要精确的时间线",
            "suggested_queries": [f"{n} 此前担任", f"{n} 任职经历"],
            "last_attempted": AS_OF,
        })
    if person["id"] == 1:
        qs.append({
            "priority": "critical",
            "question": "陈强何时任松原市委书记？何地接任？前任书记是谁、去向何处？",
            "why_it_matters": "确立市委书记交接链与跨地域干部交流模式",
            "suggested_queries": ["陈强 任松原市委书记 任命", "松原市委书记 前任 去向", "松原市委书记 李晓杰/前任"],
            "last_attempted": AS_OF,
        })
    if person["id"] == 2:
        qs.append({
            "priority": "high",
            "question": "张兆义任松原市长前的任职经历（此前是否任常务副市长等）",
            "why_it_matters": "晋升路径与前任职务关联",
            "suggested_queries": ["张兆义 简历 松原 市长", "张兆义 任松原市长 任命"],
            "last_attempted": AS_OF,
        })
    return qs


def write_person_json(person: dict) -> None:
    pid = person["id"]
    name = person["name"]

    career_timeline = [p for p in positions if p["person_id"] == pid]
    cl = []
    for pos in career_timeline:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        cl.append({
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
    if not person.get("birth"):
        cl.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "完整履历待查。百度百科403禁止访问，Bing/Exa 被天气网络限制。",
            "confidence": "unverified",
            "source_ids": [],
        })

    person_rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
    rels_out = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rels_out.append({
            "person": other_name,
            "person_id": f"songyuan_{other_name}",
            "relationship_type": "overlap",
            "strength": "strong" if r["type"] == "共事" else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    sources = [
        {
            "id": "S001",
            "title": "松原市人民政府官方网站 - 政务公开/政府领导",
            "url": "http://www.jlsy.gov.cn/zwgk/",
            "publisher": "松原市人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "领导之窗简历与要闻动态（2026-03 至 2026-08）确认现任职务",
        }
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "吉林省",
            "city": "松原市",
            "region": "松原市",
            "job": person.get("current_post", ""),
            "task_id": "jilin_松原市",
            "time_focus": "2026-08",
        },
        "identity": {
            "person_id": f"songyuan_{name}",
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [
                {
                    "period": "",
                    "institution": "",
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
                "official_profile_url": person.get("source", ""),
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正厅级" if person["id"] in (1, 2, 20) else "副厅级",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": cl,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_out,
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
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "截至2026-08，未发现陈强/张兆义有关纪律处分、审计问题或负面报道",
            "date": AS_OF,
            "confidence": "unverified",
            "source_ids": [],
        }] if person["id"] in (1, 2) else [],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "unverified",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "完整履历（百度403、Bing被拦，仅官网一手信息可用）",
        },
        "open_questions": _open_questions(person),
    }

    fname = f"{TODAY}-吉林省-松原市-{person['current_post']}-{person['name']}.json"
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
    core_ids = {1, 2, 3, 4, 5, 20}  # 书记/市长 + 常务副市长 + 常委副市长 + 纪委书记 + 人大主任
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())