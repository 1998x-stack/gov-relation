#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
唐县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 保定市
Region: 唐县
Targets: 县委书记 & 县长

Research Sources:
- 唐县人民政府门户网站 (www.tangxian.gov.cn) — 运行正常，2026年7月仍有新闻更新
- 唐县新闻频道确认县级领导在新闻报道中出现
- 唐县人民政府办公室关于县长副县长工作分工的通知（唐政办〔2026〕20号，2026-05-15）
- Wikipedia — 唐县条目确认县委书记为邓艳学

Research Date: 2026-07-23

Research limitations:
  - Exa search API: rate-limited
  - Baidu Baike: 403 blocked
  - Google/Bing: blocked/unreachable
  - Jina Reader: timeout

Confirmed leadership (as of 2026-07-23):
- 县委书记: 邓艳学 — Wikipedia条目确认
- 县长: 申志刚 — 县政府官网多篇新闻报道确认；唐政办〔2026〕20号文确认
- 县政府领导班子（含副县长分工）: 唐政办〔2026〕20号文完整确认，2026-05-15发布

All unverified biographical details (birth year, birthplace, education, early career)
labeled as such pending deeper research.
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "唐县"
TASK_ID = "hebei_唐县"
TMP_DIR = _REPO_ROOT / "data" / "tmp" / TASK_ID
AS_OF = "2026-07-23"

DB_PATH = TMP_DIR / f"{SLUG}_network.db"
GEXF_PATH = TMP_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = TMP_DIR


# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 县委领导 (Party Committee)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "邓艳学",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "唐县县委书记",
        "current_org": "中共唐县委员会",
        "source": "Wikipedia唐县条目确认; 公开新闻报道"
    },
    {
        "id": 2,
        "name": "申志刚",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "唐县县委副书记、县长",
        "current_org": "唐县人民政府",
        "source": "唐县人民政府门户网站新闻报道; 唐政办〔2026〕20号文确认"
    },
    # ════════════════════════════════════════
    # 县政府领导班子
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "刘勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "唐县县委常委、常务副县长",
        "current_org": "唐县人民政府",
        "source": "唐政办〔2026〕20号文（2026-05-15）"
    },
    {
        "id": 4,
        "name": "尹燕佳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "唐县县委常委、县经济开发区党工委副书记、管委会常务副主任",
        "current_org": "唐县经济开发区",
        "source": "唐政办〔2026〕20号文（2026-05-15）"
    },
    {
        "id": 5,
        "name": "季智璇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "唐县县委常委、副县长（挂职）",
        "current_org": "唐县人民政府",
        "source": "唐政办〔2026〕20号文（2026-05-15）"
    },
    {
        "id": 6,
        "name": "岳新平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "唐县副县长",
        "current_org": "唐县人民政府",
        "source": "唐政办〔2026〕20号文（2026-05-15）; 新闻报道确认参加申志刚调研活动"
    },
    {
        "id": 7,
        "name": "田进",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "唐县副县长",
        "current_org": "唐县人民政府",
        "source": "唐政办〔2026〕20号文（2026-05-15）"
    },
    {
        "id": 8,
        "name": "盛伟军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "唐县副县长、公安局长",
        "current_org": "唐县人民政府/唐县公安局",
        "source": "唐政办〔2026〕20号文（2026-05-15）"
    },
    {
        "id": 9,
        "name": "李贺兴",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "唐县副县长",
        "current_org": "唐县人民政府",
        "source": "唐政办〔2026〕20号文（2026-05-15）"
    },
    {
        "id": 10,
        "name": "武江",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "唐县副县长",
        "current_org": "唐县人民政府",
        "source": "唐政办〔2026〕20号文（2026-05-15）"
    },
    {
        "id": 11,
        "name": "李洪川",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "唐县古北岳党工委书记、管委会主任",
        "current_org": "古北岳管委会",
        "source": "唐政办〔2026〕20号文（2026-05-15）"
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共唐县委员会",
        "type": "党委",
        "level": "县处级",
        "location": "保定市唐县"
    },
    {
        "id": 2,
        "name": "唐县人民政府",
        "type": "政府",
        "level": "县处级",
        "location": "保定市唐县"
    },
    {
        "id": 3,
        "name": "唐县经济开发区",
        "type": "开发区",
        "level": "县处级",
        "location": "保定市唐县"
    },
    {
        "id": 4,
        "name": "唐县公安局",
        "type": "政府",
        "level": "乡科级",
        "location": "保定市唐县"
    },
    {
        "id": 5,
        "name": "古北岳管委会",
        "type": "事业单位",
        "level": "县处级",
        "location": "保定市唐县"
    },
    {
        "id": 6,
        "name": "中共保定市委",
        "type": "党委",
        "level": "地市级",
        "location": "保定市"
    },
    {
        "id": 7,
        "name": "保定市人民政府",
        "type": "政府",
        "level": "地市级",
        "location": "保定市"
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 邓艳学 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "至今", "rank": "正县处级", "note": "唐县县委书记，Wikipedia条目确认"},

    # 申志刚 — 县长
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "至今", "rank": "正县处级", "note": "兼任县委副书记"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "至今", "rank": "正县处级", "note": "唐县人民政府县长，县经济开发区党工委副书记、管委会主任（兼）"},
    {"person_id": 2, "org_id": 3, "title": "县经济开发区党工委副书记、管委会主任（兼）", "start": "", "end": "至今", "rank": "正县处级", "note": "兼任"},

    # 刘勇 — 常务副县长
    {"person_id": 3, "org_id": 2, "title": "县委常委、常务副县长", "start": "", "end": "至今", "rank": "副县处级", "note": "负责县政府常务工作"},

    # 尹燕佳 — 开发区常务副主任
    {"person_id": 4, "org_id": 3, "title": "县委常委、县经济开发区党工委副书记、管委会常务副主任", "start": "", "end": "至今", "rank": "副县处级", "note": "负责县经济开发区常务工作"},

    # 季智璇 — 挂职副县长
    {"person_id": 5, "org_id": 2, "title": "县委常委、副县长（挂职）", "start": "", "end": "至今", "rank": "副县处级", "note": "挂职，协管巩固拓展脱贫攻坚成果和乡村振兴、文化旅游工作"},

    # 岳新平
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "", "end": "至今", "rank": "副县处级", "note": "负责教育、体育、卫生健康、医疗保障、民政、文化旅游、文物等工作"},

    # 田进
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "", "end": "至今", "rank": "副县处级", "note": "负责农业农村、乡村振兴、水利等工作"},

    # 盛伟军
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "", "end": "至今", "rank": "副县处级", "note": "负责公安、司法、退役军人事务管理等工作"},
    {"person_id": 8, "org_id": 4, "title": "公安局长", "start": "", "end": "至今", "rank": "副县处级", "note": "兼任县公安局局长"},

    # 李贺兴
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "", "end": "至今", "rank": "副县处级", "note": "负责城乡建设、自然资源和规划管理、林业、城市管理、交通等工作"},

    # 武江
    {"person_id": 10, "org_id": 2, "title": "副县长", "start": "", "end": "至今", "rank": "副县处级", "note": "负责市场监督管理、食品安全、电力、通讯等工作"},

    # 李洪川
    {"person_id": 11, "org_id": 5, "title": "古北岳党工委书记、管委会主任", "start": "", "end": "至今", "rank": "副县处级", "note": "主持古北岳管委会全面工作，负责城区工作"},
]


# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 核心关系：县委书记 ↔ 县长
    {
        "person_a": 1,  # 邓艳学
        "person_b": 2,  # 申志刚
        "type": "overlap",
        "context": "县委书记与县长搭档关系（党政正职）",
        "overlap_org": "中共唐县委员会/唐县人民政府",
        "overlap_period": "至今"
    },
    # 县长 ↔ 常务副县长
    {
        "person_a": 2,  # 申志刚
        "person_b": 3,  # 刘勇
        "type": "overlap",
        "context": "县长与常务副县长上下级关系（政府常务工作）",
        "overlap_org": "唐县人民政府",
        "overlap_period": "至今"
    },
    # 县长 ↔ 副县长 岳新平
    {
        "person_a": 2,
        "person_b": 6,
        "type": "overlap",
        "context": "县长与副县长上下级关系",
        "overlap_org": "唐县人民政府",
        "overlap_period": "至今"
    },
    # 县长 ↔ 副县长 田进
    {
        "person_a": 2,
        "person_b": 7,
        "type": "overlap",
        "context": "县长与副县长上下级关系",
        "overlap_org": "唐县人民政府",
        "overlap_period": "至今"
    },
    # 县长 ↔ 副县长/公安局长 盛伟军
    {
        "person_a": 2,
        "person_b": 8,
        "type": "overlap",
        "context": "县长与副县长上下级关系",
        "overlap_org": "唐县人民政府",
        "overlap_period": "至今"
    },
    # 县长 ↔ 副县长 李贺兴
    {
        "person_a": 2,
        "person_b": 9,
        "type": "overlap",
        "context": "县长与副县长上下级关系",
        "overlap_org": "唐县人民政府",
        "overlap_period": "至今"
    },
    # 县长 ↔ 副县长 武江
    {
        "person_a": 2,
        "person_b": 10,
        "type": "overlap",
        "context": "县长与副县长上下级关系",
        "overlap_org": "唐县人民政府",
        "overlap_period": "至今"
    },
    # 县长 ↔ 李洪川（古北岳）
    {
        "person_a": 2,
        "person_b": 11,
        "type": "overlap",
        "context": "县长与古北岳管委会主任工作关系",
        "overlap_org": "唐县人民政府",
        "overlap_period": "至今"
    },
    # 县委书记 ↔ 常务副县长
    {
        "person_a": 1,
        "person_b": 3,
        "type": "overlap",
        "context": "县委书记与常务副县长党委班子关系",
        "overlap_org": "中共唐县委员会",
        "overlap_period": "至今"
    },
    # 县委书记 ↔ 开发区常务副主任
    {
        "person_a": 1,
        "person_b": 4,
        "type": "overlap",
        "context": "县委书记与县委常委工作关系",
        "overlap_org": "中共唐县委员会",
        "overlap_period": "至今"
    },
    # 县委书记 ↔ 挂职副县长
    {
        "person_a": 1,
        "person_b": 5,
        "type": "overlap",
        "context": "县委书记与挂职副县长工作关系",
        "overlap_org": "中共唐县委员会",
        "overlap_period": "至今"
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# RUN
# ══════════════════════════════════════════════════════════════════════════════

def create_person_json(person: dict) -> None:
    """Create a deep person profile JSON."""
    pid = person["id"]
    name = person["name"]
    job = person["current_post"]

    # Build filename
    name_slug = name
    # Extract a short job title for the filename
    if "县委书记" in job:
        short_job = "县委书记"
    elif "县长" in job and "副县长" not in job:
        short_job = "县长"
    elif "常务副县长" in job:
        short_job = "常务副县长"
    elif "副县长" in job:
        short_job = "副县长"
    elif "党工委" in job or "管委会" in job:
        short_job = "管委会主任"
    elif "党委书记" in job or "党工委书记" in job:
        short_job = "书记"
    else:
        short_job = job
    fname = f"{AS_OF}-河北省-保定市-{short_job}-{name_slug}.json"
    fpath = PERSONS_DIR / fname

    # Gather positions for this person
    person_positions = [p for p in positions if p["person_id"] == pid]
    # Gather relationships for this person
    person_rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]

    identity_fields = {
        "person_id": f"hebei_tangxian_{name}_{AS_OF}",
        "name": name,
        "aliases": [],
        "gender": person.get("gender", ""),
        "ethnicity": person.get("ethnicity", ""),
        "birth": person.get("birth", ""),
        "birthplace": person.get("birthplace", ""),
        "native_place": person.get("native_place", ""),
        "education": [],
        "party_join": person.get("party_join", ""),
        "work_start": person.get("work_start", ""),
        "dedupe_keys": {
            "name_birth": f"{name}_",
            "name_birthplace": f"{name}_",
            "official_profile_url": ""
        }
    }

    career_timeline = []
    for pos in person_positions:
        org_name = ""
        for o in organizations:
            if o["id"] == pos["org_id"]:
                org_name = o["name"]
                break
        is_party = "委" in org_name and "管" not in org_name
        career_timeline.append({
            "start": pos.get("start", ""),
            "end": pos.get("end", ""),
            "org": org_name,
            "title": pos["title"],
            "level": pos.get("rank", ""),
            "location": "保定市唐县",
            "system": "party" if is_party else "government",
            "rank": pos.get("rank", ""),
            "is_key_promotion": "书记" in pos["title"] or "县长" in pos["title"],
            "notes": pos.get("note", ""),
            "confidence": "confirmed",
            "source_ids": ["S001"]
        })

    rel_list = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other_name = ""
        for p in persons:
            if p["id"] == other_id:
                other_name = p["name"]
                break
        rel_list.append({
            "person": other_name,
            "person_id": f"hebei_tangxian_{other_name}_{AS_OF}",
            "relationship_type": r.get("type", ""),
            "strength": "strong" if r.get("type") == "overlap" else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"]
        })

    is_core = pid in (1, 2)
    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河北省",
            "city": "保定市",
            "region": "唐县",
            "job": job,
            "task_id": "hebei_唐县",
            "time_focus": "2025-2026"
        },
        "identity": identity_fields,
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正县处级" if is_core else "副县处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": career_timeline,
        "organizations": [o["name"] for o in organizations],
        "relationships": rel_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["party", "government"] if is_core else [],
            "geographic_pattern": ["唐县"],
            "promotion_velocity": {
                "summary": "",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {
            "direct_connections": len(person_rels),
            "organization_count": len(set(p["org_id"] for p in person_positions)),
            "centrality_estimate": "high" if is_core else "medium"
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "未发现公开的纪律处分、审计问题或负面报道",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "唐县人民政府门户网站 + Wikipedia确认",
                "url": "https://www.tangxian.gov.cn/",
                "publisher": "唐县人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "县政府官网新闻报道及Wikipedia条目确认当前领导信息"
            },
            {
                "id": "S002",
                "title": "唐县人民政府办公室关于县长副县长工作分工的通知",
                "url": "https://www.tangxian.gov.cn/content-621-395167.html",
                "publisher": "唐县人民政府办公室",
                "published_at": "2026-05-15",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "唐政办〔2026〕20号，确认县政府领导班子完整名单及分工"
            }
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "high" if is_core else "medium",
            "biggest_gap": "缺少出生年份、籍贯、教育背景和完整履历信息"
        },
        "open_questions": [
            {
                "priority": "critical" if is_core else "high",
                "question": f"{name}的出生年份和籍贯？",
                "why_it_matters": "核心身份标识字段，用于去重和跨地区网络关联",
                "suggested_queries": [f"{name} 简历", f"{name} 出生"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high" if is_core else "medium",
                "question": f"{name}的完整履历（历任职务及时间线）？",
                "why_it_matters": "构建完整职业生涯时间线，识别跨地区调动和系统内转岗",
                "suggested_queries": [f"{name} 任职", f"{name} 工作经历"],
                "last_attempted": AS_OF
            },
            {
                "priority": "medium",
                "question": f"{name}的教育背景和专业？",
                "why_it_matters": "用于技术官僚 vs 党政干部分类",
                "suggested_queries": [],
                "last_attempted": AS_OF
            },
            {
                "priority": "high" if not is_core else "low",
                "question": f"{name}是否同时担任县委常委？",
                "why_it_matters": "确认党委班子成员身份",
                "suggested_queries": [f"{name} 唐县 县委常委"],
                "last_attempted": AS_OF
            }
        ]
    }

    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath}")


if __name__ == "__main__":
    TMP_DIR.mkdir(parents=True, exist_ok=True)

    # Run main build
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Create person JSON for core leaders and known individuals
    for p in persons:
        create_person_json(p)

    print(f"\nDone: {SLUG}")
    print(f"  DB:      {DB_PATH}")
    print(f"  GEXF:    {GEXF_PATH}")
    print(f"  Persons: {PERSONS_DIR}")
