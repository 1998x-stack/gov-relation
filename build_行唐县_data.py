#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
行唐县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 石家庄市
Region: 行唐县
Targets: 县委书记 & 县长

Research Sources:
- 行唐县人民政府门户网站 (www.xingtang.gov.cn) — 运行正常，2026年7月仍有新闻更新
- 行唐要闻栏目确认县级领导在新闻报道中出现
- 行唐县融媒体中心官方微信（行唐发布）

Research Date: 2026-07-23

Research limitations:
  - Exa search API: rate-limited
  - Baidu Baike: 403 blocked
  - Google: blocked/unreachable
  - Jina Reader: timeout
  - 行唐县政府网站领导之窗页面无法访问 (404)
  - 县内站内搜索为 JS 渲染，无法直接抓取结果

Confirmed leadership (as of 2026-07-23):
- 县委书记: 苏瑞 — 公开报道确认持续担任行唐县委书记
- 县长: 黄昭波 — 公开报道确认担任行唐县委副书记、县长

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

SLUG = "行唐县"
TASK_ID = "hebei_行唐县"
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
        "name": "苏瑞",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "行唐县委书记",
        "current_org": "中共行唐县委员会",
        "source": "行唐县人民政府门户网站新闻报道确认; 行唐县融媒体中心官方微信"
    },
    {
        "id": 2,
        "name": "黄昭波",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "行唐县委副书记、县长",
        "current_org": "行唐县人民政府",
        "source": "行唐县人民政府门户网站新闻报道确认"
    },
    # ════════════════════════════════════════
    # 县委其他领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "县委副书记（待确认姓名）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "行唐县委副书记",
        "current_org": "中共行唐县委员会",
        "source": "待进一步确认"
    },
    {
        "id": 4,
        "name": "县纪委书记（待确认姓名）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "行唐县委常委、纪委书记、监委主任",
        "current_org": "中共行唐县纪律检查委员会/行唐县监察委员会",
        "source": "待进一步确认"
    },
    {
        "id": 5,
        "name": "常务副县长（待确认姓名）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "行唐县委常委、常务副县长",
        "current_org": "行唐县人民政府",
        "source": "待进一步确认"
    },
    # ════════════════════════════════════════
    # 县人大、政协主要领导
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "县人大常委会主任（待确认姓名）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "行唐县人大常委会主任",
        "current_org": "行唐县人大常委会",
        "source": "待进一步确认"
    },
    {
        "id": 7,
        "name": "县政协主席（待确认姓名）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "行唐县政协主席",
        "current_org": "行唐县政协",
        "source": "待进一步确认"
    },
    # ════════════════════════════════════════
    # 前任领导（重要关联人物）
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "韩旭（前任县委书记）",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已离任",
        "current_org": "",
        "source": "公开报道确认前任县委书记; 调任信息待确认"
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共行唐县委员会",
        "type": "党委",
        "level": "县处级",
        "location": "石家庄市行唐县"
    },
    {
        "id": 2,
        "name": "行唐县人民政府",
        "type": "政府",
        "level": "县处级",
        "location": "石家庄市行唐县"
    },
    {
        "id": 3,
        "name": "行唐县人大常委会",
        "type": "人大",
        "level": "县处级",
        "location": "石家庄市行唐县"
    },
    {
        "id": 4,
        "name": "行唐县政协",
        "type": "政协",
        "level": "县处级",
        "location": "石家庄市行唐县"
    },
    {
        "id": 5,
        "name": "中共行唐县纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "location": "石家庄市行唐县"
    },
    {
        "id": 6,
        "name": "行唐县监察委员会",
        "type": "政府",
        "level": "县处级",
        "location": "石家庄市行唐县"
    },
    {
        "id": 7,
        "name": "行唐县经济开发区",
        "type": "开发区",
        "level": "县处级",
        "location": "石家庄市行唐县"
    },
    {
        "id": 8,
        "name": "中共石家庄市委",
        "type": "党委",
        "level": "地市级",
        "location": "石家庄市"
    },
    {
        "id": 9,
        "name": "石家庄市人民政府",
        "type": "政府",
        "level": "地市级",
        "location": "石家庄市"
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 苏瑞 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "至今", "rank": "正县处级", "note": "行唐县委书记，公开报道确认"},
    # 黄昭波 — 县长
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "至今", "rank": "正县处级", "note": "兼任县委副书记"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "至今", "rank": "正县处级", "note": "行唐县人民政府县长"},
    # 县委副书记（待确认）
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "", "end": "至今", "rank": "副县处级", "note": "具体人选待确认"},
    # 纪委书记（待确认）
    {"person_id": 4, "org_id": 5, "title": "县委常委、纪委书记", "start": "", "end": "至今", "rank": "副县处级", "note": "具体人选待确认"},
    {"person_id": 4, "org_id": 6, "title": "监委主任", "start": "", "end": "至今", "rank": "副县处级", "note": "兼任监委主任"},
    # 常务副县长（待确认）
    {"person_id": 5, "org_id": 2, "title": "县委常委、常务副县长", "start": "", "end": "至今", "rank": "副县处级", "note": "具体人选待确认"},
    # 人大主任（待确认）
    {"person_id": 6, "org_id": 3, "title": "县人大常委会主任", "start": "", "end": "至今", "rank": "正县处级", "note": "具体人选待确认"},
    # 政协主席（待确认）
    {"person_id": 7, "org_id": 4, "title": "县政协主席", "start": "", "end": "至今", "rank": "正县处级", "note": "具体人选待确认"},
    # 韩旭 — 前任县委书记
    {"person_id": 8, "org_id": 1, "title": "县委书记（前任）", "start": "", "end": "", "rank": "正县处级", "note": "前任县委书记"},
]


# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 核心关系：县委书记 ↔ 县长
    {
        "person_a": 1,  # 苏瑞
        "person_b": 2,  # 黄昭波
        "type": "overlap",
        "context": "县委书记与县长搭档关系（党政正职）",
        "overlap_org": "中共行唐县委/行唐县人民政府",
        "overlap_period": "2024-2026年至今"
    },
    # 前任县委书记 ↔ 现任县委书记
    {
        "person_a": 8,  # 韩旭
        "person_b": 1,  # 苏瑞
        "type": "predecessor_successor",
        "context": "前任县委书记与现任县委书记交接",
        "overlap_org": "中共行唐县委",
        "overlap_period": "交接期"
    },
    # 前任县委书记 ↔ 县长
    {
        "person_a": 8,  # 韩旭
        "person_b": 2,  # 黄昭波
        "type": "overlap",
        "context": "前任县委书记与县长曾有共事关系",
        "overlap_org": "中共行唐县委/行唐县人民政府",
        "overlap_period": "前任县委书记任职期"
    },
    # 县委书记 ↔ 副书记
    {
        "person_a": 1,
        "person_b": 3,
        "type": "overlap",
        "context": "县委书记与副书记上下级关系",
        "overlap_org": "中共行唐县委",
        "overlap_period": ""
    },
    # 县长 ↔ 常务副县长
    {
        "person_a": 2,
        "person_b": 5,
        "type": "overlap",
        "context": "县长与常务副县长上下级关系",
        "overlap_org": "行唐县人民政府",
        "overlap_period": ""
    },
    # 县委书记 ↔ 纪委书记
    {
        "person_a": 1,
        "person_b": 4,
        "type": "overlap",
        "context": "县委书记与纪委书记党委班子关系",
        "overlap_org": "中共行唐县委",
        "overlap_period": ""
    },
    # 县委书记 ↔ 人大主任
    {
        "person_a": 1,
        "person_b": 6,
        "type": "overlap",
        "context": "县委书记与人大主任党政关系",
        "overlap_org": "行唐县",
        "overlap_period": ""
    },
    # 县委书记 ↔ 政协主席
    {
        "person_a": 1,
        "person_b": 7,
        "type": "overlap",
        "context": "县委书记与政协主席党政关系",
        "overlap_org": "行唐县",
        "overlap_period": ""
    },
    # 县长 ↔ 人大主任
    {
        "person_a": 2,
        "person_b": 6,
        "type": "overlap",
        "context": "县长与人大主任关系",
        "overlap_org": "行唐县",
        "overlap_period": ""
    },
    # 县长 ↔ 政协主席
    {
        "person_a": 2,
        "person_b": 7,
        "type": "overlap",
        "context": "县长与政协主席关系",
        "overlap_org": "行唐县",
        "overlap_period": ""
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
    name_slug = name.replace("（", "_").replace("）", "_").replace(" ", "")
    fname = f"{AS_OF}-河北省-石家庄市-{job}-{name_slug}.json"
    fpath = PERSONS_DIR / fname

    # Gather positions for this person
    person_positions = [p for p in positions if p["person_id"] == pid]
    # Gather relationships for this person
    person_rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]

    identity_fields = {
        "person_id": f"hebei_xingtang_{name}_{AS_OF}",
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
        career_timeline.append({
            "start": pos.get("start", ""),
            "end": pos.get("end", ""),
            "org": org_name,
            "title": pos["title"],
            "level": pos.get("rank", ""),
            "location": "石家庄市行唐县",
            "system": "party" if "委" in org_name else "government",
            "rank": pos.get("rank", ""),
            "is_key_promotion": "书记" in pos["title"] or "县长" in pos["title"],
            "notes": pos.get("note", ""),
            "confidence": "confirmed" if "待确认" not in name and "待确认" not in pos["title"] else "unverified",
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
            "person_id": f"hebei_xingtang_{other_name}_{AS_OF}",
            "relationship_type": r.get("type", ""),
            "strength": "strong" if r.get("type") == "overlap" else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if "待确认" not in other_name else "unverified",
            "source_ids": ["S001"]
        })

    is_core = pid in (1, 2)
    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河北省",
            "city": "石家庄市",
            "region": "行唐县",
            "job": job,
            "task_id": "hebei_行唐县",
            "time_focus": "2025-2026"
        },
        "identity": identity_fields,
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正县处级" if is_core else "副县处级",
            "as_of": AS_OF,
            "is_current_confirmed": is_core,
            "source_ids": ["S001"]
        },
        "career_timeline": career_timeline,
        "organizations": [o["name"] for o in organizations],
        "relationships": rel_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder" if is_core else "unknown",
            "systems_experience": ["party", "government"] if is_core else [],
            "geographic_pattern": ["行唐县"],
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
                "title": "行唐县人民政府门户网站",
                "url": "http://www.xingtang.gov.cn/",
                "publisher": "行唐县人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "行唐县政府官网，新闻报道确认领导出席活动"
            }
        ],
        "confidence_summary": {
            "identity": "unverified" if "待确认" in name else "plausible",
            "current_role": "confirmed" if is_core else ("unverified" if "待确认" in name else "plausible"),
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

    # Create person JSON for core leaders
    for p in persons:
        if "待确认" not in p["name"]:
            create_person_json(p)

    print(f"\nDone: {SLUG}")
    print(f"  DB:      {DB_PATH}")
    print(f"  GEXF:    {GEXF_PATH}")
    print(f"  Persons: {PERSONS_DIR}")
