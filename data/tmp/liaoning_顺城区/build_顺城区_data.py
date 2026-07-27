#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 顺城区, 抚顺市, 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_顺城区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - fssc.gov.cn — 顺城区人民政府官方网站
  - fssc.gov.cn/ld.asp — 领导之窗页面
  - fssc.gov.cn/search.asp — 站内搜索（确认赵效飞、薛强等任职）
  - baike.baidu.com — 百度百科顺城区词条（2024年12月快照）

Key findings:
  - 赵效飞: 现任区委书记（官网59条新闻确认，首次出现在2025年7月）
  - 薛强: 现任区长（1980年7月生，2024年11月任代区长，2025年3月转正）
  - 张卓: 常务副区长（1980年1月生，汉族）
  - 周诗杰: 副区长（1984年10月生，汉族）
  - 金学飞: 副区长兼公安局长（1972年2月生，满族）
  - 刘丽: 副区长（1975年7月生，汉族）
  - 张巍: 前任区委书记（至2025年初）
  - 李培育: 前任区长（2021-2024年任职）

Confidence notes:
  - 赵效飞区委书记身份通过fssc.gov.cn大量新闻确认
  - 薛强完整身份通过官网领导页面确认
  - 赵效飞、薛强此前履历公开渠道不可得，标注为unverified
  - 区委常委班子（纪委、组织、宣传、政法等）未在政府官网完整列出
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
SLUG = "顺城区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "liaoning_顺城区"
if _CURRENT_DIR.name == "liaoning_顺城区":
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
# IDs: 1xxx = party committee, 2xxx = government, 3xxx = predecessor

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    # 1. 赵效飞 — 区委书记
    {
        "id": 1001,
        "name": "赵效飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "顺城区委书记",
        "current_org": "中共抚顺市顺城区委员会",
        "source": "http://www.fssc.gov.cn/search.asp?sname=%C7%F8%CE%AF%CA%E9%BC%C7",
    },
    # 2. 薛强 — 区委副书记、区长
    {
        "id": 1002,
        "name": "薛强",
        "gender": "男",
        "ethnicity": "",
        "birth": "1980年7月",
        "birthplace": "",
        "education": "大学学历，学士学位",
        "party_join": "",
        "work_start": "",
        "current_post": "顺城区委副书记、区长",
        "current_org": "顺城区人民政府",
        "source": "http://www.fssc.gov.cn/ld.asp?s=775",
    },
    # 3. 张卓 — 区委常委、常务副区长
    {
        "id": 1003,
        "name": "张卓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年1月",
        "birthplace": "",
        "education": "大学工学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "顺城区委常委、分管日常工作的副区长（三级调研员）",
        "current_org": "顺城区人民政府",
        "source": "http://www.fssc.gov.cn/ld.asp?s=1518",
    },
    # 4. 周诗杰 — 区委常委、副区长
    {
        "id": 1004,
        "name": "周诗杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年10月",
        "birthplace": "",
        "education": "大学学历，公共管理硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "顺城区委常委、副区长",
        "current_org": "顺城区人民政府",
        "source": "http://www.fssc.gov.cn/ld.asp?s=782",
    },
    # 5. 金学飞 — 副区长、公安分局局长
    {
        "id": 2001,
        "name": "金学飞",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1972年2月",
        "birthplace": "",
        "education": "大学文化",
        "party_join": "",
        "work_start": "",
        "current_post": "顺城区副区长，顺城公安分局党组书记、局长",
        "current_org": "抚顺市公安局顺城分局",
        "source": "http://www.fssc.gov.cn/ld.asp?s=762",
    },
    # 6. 刘丽 — 副区长、河北乡党委书记
    {
        "id": 2002,
        "name": "刘丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975年7月",
        "birthplace": "",
        "education": "中央党校大学",
        "party_join": "",
        "work_start": "",
        "current_post": "顺城区副区长，河北乡党委书记",
        "current_org": "顺城区人民政府",
        "source": "http://www.fssc.gov.cn/ld.asp?s=783",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    # 7. 张巍 — 前任区委书记
    {
        "id": 3001,
        "name": "张巍",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "已离任（前任顺城区委书记）",
        "current_org": "",
        "source": "https://baike.baidu.com/item/%E9%A1%BA%E5%9F%8E%E5%8C%BA/247994",
    },
    # 8. 李培育 — 前任区长
    {
        "id": 3002,
        "name": "李培育",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "已离任（前任顺城区区长）",
        "current_org": "",
        "source": "http://www.fssc.gov.cn/search.asp?sname=%C0%EE%C5%E0%D3%FD",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 人大 & 政协
    # ══════════════════════════════════════════════════════════════════════
    # 9. 冷之泉 — 区人大常委会主任
    {
        "id": 4001,
        "name": "冷之泉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "顺城区人大常委会主任",
        "current_org": "顺城区人民代表大会常务委员会",
        "source": "https://baike.baidu.com/item/%E9%A1%BA%E5%9F%8E%E5%8C%BA/247994",
    },
    # 10. 张鑫 — 区政协主席
    {
        "id": 4002,
        "name": "张鑫",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "顺城区政协主席",
        "current_org": "中国人民政治协商会议抚顺市顺城区委员会",
        "source": "https://baike.baidu.com/item/%E9%A1%BA%E5%9F%8E%E5%8C%BA/247994",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {
        "id": 10,
        "name": "中共抚顺市顺城区委员会",
        "type": "party",
        "level": "district",
        "parent": "中共抚顺市委员会",
        "location": "顺城区",
    },
    {
        "id": 11,
        "name": "顺城区人民政府",
        "type": "government",
        "level": "district",
        "parent": "抚顺市人民政府",
        "location": "顺城区",
    },
    {
        "id": 12,
        "name": "抚顺市公安局顺城分局",
        "type": "government",
        "level": "district",
        "parent": "抚顺市公安局",
        "location": "顺城区",
    },
    {
        "id": 13,
        "name": "顺城区人民代表大会常务委员会",
        "type": "npc",
        "level": "district",
        "parent": "抚顺市人民代表大会常务委员会",
        "location": "顺城区",
    },
    {
        "id": 14,
        "name": "中国人民政治协商会议抚顺市顺城区委员会",
        "type": "cppcc",
        "level": "district",
        "parent": "政协抚顺市委员会",
        "location": "顺城区",
    },
    {
        "id": 15,
        "name": "中共抚顺市顺城区纪律检查委员会",
        "type": "party_discipline",
        "level": "district",
        "parent": "中共抚顺市纪律检查委员会",
        "location": "顺城区",
    },
    {
        "id": 16,
        "name": "河北乡党委",
        "type": "party",
        "level": "township",
        "parent": "中共抚顺市顺城区委员会",
        "location": "顺城区河北乡",
    },
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    # 赵效飞 — 区委书记
    {"person_id": 1001, "org_id": 10, "title": "顺城区委书记", "start": "2025-07", "end": "present", "rank": "正县级", "note": "官网首次出现为2025年7月"},
    # 薛强 — 区长
    {"person_id": 1002, "org_id": 11, "title": "顺城区区长", "start": "2024-11", "end": "present", "rank": "正县级", "note": "2024年11月20日任代区长，约2025年3月转正"},
    {"person_id": 1002, "org_id": 10, "title": "顺城区委副书记", "start": "2024-11", "end": "present", "rank": "副厅?", "note": ""},
    # 张卓 — 常务副区长
    {"person_id": 1003, "org_id": 11, "title": "顺城区委常委、分管日常工作的副区长", "start": "", "end": "present", "rank": "副县级（三级调研员）", "note": "负责区政府常务工作"},
    {"person_id": 1003, "org_id": 10, "title": "顺城区委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 周诗杰 — 副区长
    {"person_id": 1004, "org_id": 11, "title": "顺城区委常委、副区长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 1004, "org_id": 10, "title": "顺城区委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 金学飞 — 副区长兼公安局长
    {"person_id": 2001, "org_id": 11, "title": "顺城区副区长", "start": "", "end": "present", "rank": "副县级", "note": "负责公安、司法、信访、突发事件"},
    {"person_id": 2001, "org_id": 12, "title": "顺城公安分局党组书记、局长", "start": "", "end": "present", "rank": "", "note": ""},
    # 刘丽 — 副区长
    {"person_id": 2002, "org_id": 11, "title": "顺城区副区长", "start": "", "end": "present", "rank": "副县级", "note": "负责教育、交通、退役、市场监管等"},
    {"person_id": 2002, "org_id": 16, "title": "河北乡党委书记", "start": "", "end": "present", "rank": "", "note": "兼任"},
    # 张巍 — 前任区委书记
    {"person_id": 3001, "org_id": 10, "title": "顺城区委书记（前任）", "start": "", "end": "2025", "rank": "正县级", "note": "百度百科2024年12月仍列其为区委书记"},
    # 李培育 — 前任区长
    {"person_id": 3002, "org_id": 11, "title": "顺城区区长（前任）", "start": "2021-12", "end": "2024-11", "rank": "正县级", "note": "2021年12月任代区长，2024年11月离任由薛强接任"},
    # 冷之泉 — 人大主任
    {"person_id": 4001, "org_id": 13, "title": "顺城区人大常委会主任", "start": "", "end": "present", "rank": "正县级", "note": ""},
    # 张鑫 — 政协主席
    {"person_id": 4002, "org_id": 14, "title": "顺城区政协主席", "start": "", "end": "present", "rank": "正县级", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 赵效飞 ↔ 薛强 — 书记+区长搭档
    {
        "person_a": 1001,
        "person_b": 1002,
        "type": "superior_subordinate",
        "context": "区委书记与区长搭档关系",
        "overlap_org": "中共抚顺市顺城区委员会",
        "overlap_period": "2025至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 赵效飞 ↔ 张卓 — 书记+常务副区长
    {
        "person_a": 1001,
        "person_b": 1003,
        "type": "superior_subordinate",
        "context": "区委书记与常务副区长",
        "overlap_org": "中共抚顺市顺城区委员会",
        "overlap_period": "2025至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 赵效飞 ↔ 周诗杰 — 书记+副区长
    {
        "person_a": 1001,
        "person_b": 1004,
        "type": "superior_subordinate",
        "context": "区委书记与副区长",
        "overlap_org": "中共抚顺市顺城区委员会",
        "overlap_period": "2025至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 薛强 ↔ 张卓 — 区长+常务副区长
    {
        "person_a": 1002,
        "person_b": 1003,
        "type": "overlap",
        "context": "区长与常务副区长（区政府班子正副职）",
        "overlap_org": "顺城区人民政府",
        "overlap_period": "2024至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 薛强 ↔ 周诗杰 — 区长+副区长
    {
        "person_a": 1002,
        "person_b": 1004,
        "type": "overlap",
        "context": "区长与副区长（区政府班子）",
        "overlap_org": "顺城区人民政府",
        "overlap_period": "2024至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 张卓 ↔ 周诗杰 — 同为政府副职
    {
        "person_a": 1003,
        "person_b": 1004,
        "type": "overlap",
        "context": "同为顺城区副区长",
        "overlap_org": "顺城区人民政府",
        "overlap_period": "至今",
        "strength": "medium",
        "confidence": "confirmed",
    },
    # 金学飞 ↔ 刘丽 — 同为副区长
    {
        "person_a": 2001,
        "person_b": 2002,
        "type": "overlap",
        "context": "同为顺城区副区长",
        "overlap_org": "顺城区人民政府",
        "overlap_period": "至今",
        "strength": "medium",
        "confidence": "confirmed",
    },
    # 赵效飞 ↔ 张巍 — 前后任书记
    {
        "person_a": 1001,
        "person_b": 3001,
        "type": "predecessor_successor",
        "context": "赵效飞接替张巍任顺城区委书记",
        "overlap_org": "中共抚顺市顺城区委员会",
        "overlap_period": "2025",
        "strength": "medium",
        "confidence": "confirmed",
    },
    # 薛强 ↔ 李培育 — 前后任区长
    {
        "person_a": 1002,
        "person_b": 3002,
        "type": "predecessor_successor",
        "context": "薛强接替李培育任顺城区区长",
        "overlap_org": "顺城区人民政府",
        "overlap_period": "2024",
        "strength": "medium",
        "confidence": "confirmed",
    },
]

# ── Person JSON helper ───────────────────────────────────────────────────────
def write_person_json(person: dict, extra: dict | None = None) -> Path:
    """Write a per-person deep profile JSON file."""
    pid = person["id"]
    name = person["name"]
    job = person.get("current_post", "")
    if "区长" in job and "副区长" not in job:
        job_short = "区长"
    elif "区委书记" in job:
        job_short = "区委书记"
    elif "人大常委会主任" in job:
        job_short = "区人大常委会主任"
    elif "政协主席" in job:
        job_short = "区政协主席"
    elif "常务" in job:
        job_short = "常务副区长"
    elif "副区长" in job:
        job_short = "副区长"
    elif pid == 3001:
        job_short = "前任区委书记"
    elif pid == 3002:
        job_short = "前任区长"
    else:
        job_short = "领导"

    pjson = extra or {}
    pjson.update({
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "抚顺市",
            "region": "顺城区",
            "job": job_short,
            "task_id": "liaoning_顺城区",
            "time_focus": "2024-2026",
        },
        "identity": {
            "person_id": f"shuncheng_{name}",
            "name": name,
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "education": [{"institution": person.get("education", ""), "study_type": "unknown"}] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "as_of": AS_OF,
            "is_current_confirmed": pid not in (3001, 3002),
            "source_ids": [],
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {},
        "work_style_and_personality": {"public_style_indicators": [], "caveat": "No public evidence available for style/personality assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [],
        "confidence_summary": {
            "identity": "confirmed" if person.get("gender") or person.get("birth") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if person.get("birth") else "thin",
            "relationship_confidence": "high" if pid in (1001, 1002) else "medium",
            "biggest_gap": f"此前履历完全未知" if pid in (1001, 1002) else "缺出生等基本信息",
        },
        "open_questions": [
            {
                "priority": "critical" if pid in (1001, 1002) else "high",
                "question": f"{name}的完整履历" if pid in (1001, 1002) else f"{name}的出生年份和籍贯",
                "why_it_matters": "核心人物背景分析的核心数据",
                "suggested_queries": [f"{name} 简历 抚顺", f"{name} 任前公示", f"{name} 此前任职"],
                "last_attempted": AS_OF,
            }
        ],
    })

    fname = f"{TODAY}-辽宁省-抚顺市-{job_short}-{name}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(pjson, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath}")
    return fpath


# ── Build ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write person JSONs for core figures
    for p in persons:
        pid = p["id"]
        name = p["name"]
        job = p.get("current_post", "")

        # Build extra data for key figures
        extra = None
        if pid == 1001:  # 赵效飞 — 区委书记
            extra = {
                "career_timeline": [
                    {"start": "unknown", "end": "2025-06", "org": "履历缺口", "title": "", "notes": "公开资料未找到赵效飞2025年7月之前的任何履历", "confidence": "unverified"},
                    {"start": "2025-07", "end": "present", "org": "中共抚顺市顺城区委员会", "title": "顺城区委书记", "level": "正县级", "location": "抚顺市顺城区", "system": "party", "confidence": "confirmed", "source_ids": ["S001"]},
                ],
                "source_register": [
                    {"id": "S001", "title": "顺城区政府官网新闻（59条含赵效飞）", "url": "http://www.fssc.gov.cn/search.asp?sname=%C7%F8%CE%AF%CA%E9%BC%C7", "publisher": "顺城区人民政府", "source_type": "official", "reliability": "high", "notes": "站内搜索'区委书记'返回59条结果全部指向赵效飞"},
                ],
            }
        elif pid == 1002:  # 薛强 — 区长
            extra = {
                "career_timeline": [
                    {"start": "unknown", "end": "2024-10", "org": "履历缺口", "title": "", "notes": "公开资料未找到薛强2024年11月之前的任何履历", "confidence": "unverified"},
                    {"start": "2024-11", "end": "2025-02", "org": "顺城区人民政府", "title": "顺城区代区长", "level": "正县级", "location": "抚顺市顺城区", "system": "government", "notes": "2024年11月20日区人大常委会任命为代区长", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
                    {"start": "2025-03", "end": "present", "org": "顺城区人民政府", "title": "顺城区区长", "level": "正县级", "location": "抚顺市顺城区", "system": "government", "notes": "约2025年3月正式转正", "confidence": "confirmed", "source_ids": ["S002"]},
                ],
                "source_register": [
                    {"id": "S002", "title": "薛强—顺城区政府领导之窗", "url": "http://www.fssc.gov.cn/ld.asp?s=775", "publisher": "顺城区人民政府", "source_type": "official", "reliability": "high", "notes": "含照片、分工、简历"},
                    {"id": "S003", "title": "顺城区人大常委会关于薛强为代理区长的决定", "url": "http://www.fssc.gov.cn/search.asp?sname=%D1%A6%C7%BF", "publisher": "顺城区人民政府", "source_type": "official", "reliability": "high", "notes": "2024年11月20日决定"},
                ],
            }
        elif pid == 1003:  # 张卓
            extra = {
                "career_timeline": [
                    {"start": "unknown", "end": "present", "org": "顺城区人民政府", "title": "顺城区委常委、分管日常工作的副区长", "level": "副县级（三级调研员）", "location": "抚顺市顺城区", "system": "government", "confidence": "confirmed", "source_ids": ["S004"]},
                ],
                "source_register": [
                    {"id": "S004", "title": "张卓—顺城区政府领导之窗", "url": "http://www.fssc.gov.cn/ld.asp?s=1518", "publisher": "顺城区人民政府", "source_type": "official", "reliability": "high"},
                ],
            }
        elif pid == 1004:  # 周诗杰
            extra = {
                "career_timeline": [
                    {"start": "unknown", "end": "present", "org": "顺城区人民政府", "title": "顺城区委常委、副区长", "level": "副县级", "location": "抚顺市顺城区", "system": "government", "confidence": "confirmed", "source_ids": ["S005"]},
                ],
                "source_register": [
                    {"id": "S005", "title": "周诗杰—顺城区政府领导之窗", "url": "http://www.fssc.gov.cn/ld.asp?s=782", "publisher": "顺城区人民政府", "source_type": "official", "reliability": "high"},
                ],
            }
        elif pid == 3001:  # 张巍
            extra = {
                "career_timeline": [
                    {"start": "", "end": "2024-12", "org": "中共抚顺市顺城区委员会", "title": "顺城区委书记", "level": "正县级", "location": "抚顺市顺城区", "system": "party", "notes": "百度百科2024年12月快照仍显示为区委书记", "confidence": "confirmed", "source_ids": ["S006"]},
                    {"start": "2025", "end": "unknown", "org": "去向未知", "title": "", "notes": "离任后去向不明", "confidence": "unverified"},
                ],
                "source_register": [
                    {"id": "S006", "title": "百度百科—顺城区", "url": "https://baike.baidu.com/item/%E9%A1%BA%E5%9F%8E%E5%8C%BA/247994", "publisher": "百度百科", "source_type": "encyclopedia", "reliability": "medium"},
                ],
            }
        elif pid == 3002:  # 李培育
            extra = {
                "career_timeline": [
                    {"start": "2021-12", "end": "2023", "org": "顺城区人民政府", "title": "顺城区代区长", "level": "正县级", "location": "抚顺市顺城区", "system": "government", "notes": "2021年12月首次以代区长身份出现", "confidence": "confirmed", "source_ids": ["S007"]},
                    {"start": "2023", "end": "2024-11", "org": "顺城区人民政府", "title": "顺城区区长", "level": "正县级", "location": "抚顺市顺城区", "system": "government", "notes": "约2023年3月转正", "confidence": "confirmed", "source_ids": ["S007"]},
                    {"start": "2024-11", "end": "unknown", "org": "去向未知", "title": "", "notes": "离任后去向不明", "confidence": "unverified"},
                ],
                "source_register": [
                    {"id": "S007", "title": "顺城区政府官网站内搜索李培育", "url": "http://www.fssc.gov.cn/search.asp?sname=%C0%EE%C5%E0%D3%FD", "publisher": "顺城区人民政府", "source_type": "official", "reliability": "high", "notes": "134条搜索结果"},
                ],
            }

        write_person_json(p, extra)

    # Print summary for logging
    print(f"\n{SLUG} network build complete.")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
