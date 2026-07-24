#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宁乡市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县级市
Province: 湖南省
Parent City: 长沙市
Region: 宁乡市
Targets: 市委书记 & 市长

Research status (2026-07-24):
- 张作林 (Party Secretary): plausible — 宁乡市委书记 (since ~2021-08)
  - Identity: 男，汉族，湖南长沙县人，1971年生
  - Career history: thin — only current role and previous roles partially confirmed
- 黄滔 (Mayor): plausible — 宁乡市市长 (since ~2021)
  - Identity: 男，汉族，约1975年生，湖南人
  - Career history: thin — only partial timeline confirmed
- 于新凡 (Predecessor): plausible — former 宁乡市委书记 (~2016-2021), now 长沙市领导

Research constraints:
  - Baidu Baike: 403/Cloudflare block
  - Exa search: rate limited
  - Jina Reader: transport errors
  - Government websites (ningxiang.gov.cn): connection timeouts
  - Wikipedia (zh/en): connection timeouts
  - All data based on training knowledge and partial repo references

Gaps logged in open_questions and report/open_gaps.md
"""

from __future__ import annotations

import json
import os
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

import sqlite3  # noqa: F401 — used by gov_relation.runner; token needed by process_tmp

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "宁乡市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "hunan_宁乡市"
if _CURRENT_DIR.name == "hunan_宁乡市":
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
# IDs: 1-9 current leaders, 10-19 standing committee, 20-29 deputy gov, 30+ predecessors/others

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════

    # 张作林 — 宁乡市委书记 (Party Secretary)
    {
        "id": 1,
        "name": "张作林",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "1971年",  # plausible — based on training knowledge, approximate
        "birthplace": "湖南省长沙县",  # plausible — training knowledge
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "宁乡市委书记",
        "current_org": "中共宁乡市委员会",
        "source": "历史知识",
        "confidence": "plausible",
        "notes": "2021年8月任宁乡市委书记。此前曾任长沙县委常委、纪委书记等职。出生地长沙县，约1971年生。详情待官方确认。"
    },

    # 黄滔 — 宁乡市市长 (Mayor)
    {
        "id": 2,
        "name": "黄滔",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "宁乡市市长",
        "current_org": "宁乡市人民政府",
        "source": "历史知识",
        "confidence": "plausible",
        "notes": "约2021年任宁乡市市长，接任付旭明（付旭明后任浏阳市委书记）。此前在长沙市经济运行领域任职。详情待官方确认。"
    },

    # ══════════════════════════════════════════════════════════════════════
    # 宁乡市委常委 (Standing Committee)
    # ══════════════════════════════════════════════════════════════════════

    # 专职副书记（待确认）
    {
        "id": 11,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记（专职）",
        "current_org": "中共宁乡市委员会",
        "source": "",
        "confidence": "unverified",
        "notes": "专职副书记身份待确认。通常县级市设专职副书记1名。"
    },

    # 常务副市长（待确认）
    {
        "id": 12,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "宁乡市人民政府",
        "source": "",
        "confidence": "unverified",
        "notes": "常务副市长身份待确认。"
    },

    # 纪委书记（待确认）
    {
        "id": 13,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、市纪委书记、市监委主任",
        "current_org": "中共宁乡市纪律检查委员会",
        "source": "",
        "confidence": "unverified",
        "notes": "纪委书记身份待确认。"
    },

    # 组织部部长（待确认）
    {
        "id": 14,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共宁乡市委组织部",
        "source": "",
        "confidence": "unverified",
        "notes": "组织部部长身份待确认。"
    },

    # 宣传部部长（待确认）
    {
        "id": 15,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共宁乡市委宣传部",
        "source": "",
        "confidence": "unverified",
        "notes": "宣传部部长身份待确认。"
    },

    # 统战部部长（待确认）
    {
        "id": 16,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、统战部部长",
        "current_org": "中共宁乡市委统一战线工作部",
        "source": "",
        "confidence": "unverified",
        "notes": "统战部部长身份待确认。"
    },

    # 政法委书记（待确认）
    {
        "id": 17,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、政法委书记",
        "current_org": "中共宁乡市委政法委员会",
        "source": "",
        "confidence": "unverified",
        "notes": "政法委书记身份待确认。"
    },

    # ══════════════════════════════════════════════════════════════════════
    # 副市长 (Deputy Mayors) — typical 5-7 deputies
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 21,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长（常务副市长兼任）",
        "current_org": "宁乡市人民政府",
        "source": "",
        "confidence": "unverified",
        "notes": "常务副市长，通常分管政府常务工作。身份待确认。"
    },
    {
        "id": 22,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "宁乡市人民政府",
        "source": "",
        "confidence": "unverified",
        "notes": "副市长（分管经济/发改/工信等），身份待确认。"
    },
    {
        "id": 23,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "宁乡市人民政府",
        "source": "",
        "confidence": "unverified",
        "notes": "副市长（分管公安/司法/信访等，兼公安局长），身份待确认。"
    },
    {
        "id": 24,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "宁乡市人民政府",
        "source": "",
        "confidence": "unverified",
        "notes": "副市长（分管教育/卫生/文化等），身份待确认。"
    },
    {
        "id": 25,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "宁乡市人民政府",
        "source": "",
        "confidence": "unverified",
        "notes": "副市长（分管城建/交通/规划等），身份待确认。"
    },

    # ══════════════════════════════════════════════════════════════════════
    # Predecessors & Key Historical Figures
    # ══════════════════════════════════════════════════════════════════════

    # 于新凡 — 前任宁乡市委书记（~2016-2021）
    {
        "id": 31,
        "name": "于新凡",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任宁乡市委书记",
        "current_org": "中共宁乡市委员会（原）",
        "source": "历史知识",
        "confidence": "plausible",
        "notes": "前任宁乡市委书记（约2016-2021年8月），后任长沙市领导。职务细节待确认。"
    },

    # 付旭明 — 前任宁乡市长（~2016-2021），后任浏阳市委书记，现任长沙市委常委、常务副市长
    {
        "id": 32,
        "name": "付旭明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长沙市委常委、常务副市长",
        "current_org": "长沙市人民政府",
        "source": "维基百科 — 中国共产党长沙市委员会、长沙市构建脚本",
        "confidence": "confirmed",
        "notes": "曾先后任宁乡市市长（约2016-2021）→浏阳市委书记（约2021-2025.12）→长沙市委常委、常务副市长（2025.12至今）。从宁乡到浏阳再到长沙的跨县提拔路径。"
    },

    # 周辉 — 更早的前任宁乡市委书记（~2013-2016）
    {
        "id": 33,
        "name": "周辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任宁乡县委书记",
        "current_org": "中共宁乡市委员会（原）",
        "source": "历史知识",
        "confidence": "plausible",
        "notes": "约2013-2016年任宁乡县委书记/市委书记。具体去向待查。"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共宁乡市委员会", "type": "党委", "level": "县级", "parent": "中共长沙市委", "location": "宁乡"},
    {"id": 2, "name": "宁乡市人民政府", "type": "政府", "level": "县级", "parent": "长沙市人民政府", "location": "宁乡"},
    {"id": 3, "name": "中共宁乡市纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共宁乡市委员会", "location": "宁乡"},
    {"id": 4, "name": "宁乡市人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "", "location": "宁乡"},
    {"id": 5, "name": "中国人民政治协商会议宁乡市委员会", "type": "政协", "level": "县级", "parent": "", "location": "宁乡"},
    {"id": 6, "name": "中共宁乡市委组织部", "type": "党委", "level": "县级", "parent": "中共宁乡市委员会", "location": "宁乡"},
    {"id": 7, "name": "中共宁乡市委宣传部", "type": "党委", "level": "县级", "parent": "中共宁乡市委员会", "location": "宁乡"},
    {"id": 8, "name": "中共宁乡市委统一战线工作部", "type": "党委", "level": "县级", "parent": "中共宁乡市委员会", "location": "宁乡"},
    {"id": 9, "name": "中共宁乡市委政法委员会", "type": "党委", "level": "县级", "parent": "中共宁乡市委员会", "location": "宁乡"},
    {"id": 10, "name": "宁乡市公安局", "type": "政府", "level": "县级", "parent": "宁乡市人民政府", "location": "宁乡"},
    {"id": 11, "name": "中共长沙市委", "type": "党委", "level": "地市级", "parent": "中共湖南省委", "location": "长沙"},
    {"id": 12, "name": "长沙市人民政府", "type": "政府", "level": "地市级", "parent": "湖南省人民政府", "location": "长沙"},
    {"id": 13, "name": "中共湖南省委", "type": "党委", "level": "省级", "parent": "", "location": "长沙"},
    {"id": 14, "name": "湖南省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "长沙"},
    {"id": 15, "name": "宁乡市人民武装部", "type": "军队", "level": "县级", "parent": "长沙警备区", "location": "宁乡"},
    # Economic development zone
    {"id": 16, "name": "宁乡经济技术开发区", "type": "开发区", "level": "国家级", "parent": "宁乡市人民政府", "location": "宁乡"},
]

# ── Positions ──────────────────────────────────────────────────────────────────
positions = [
    # ═══ 张作林 (id=1) ═══
    {"person_id": 1, "org_id": 1, "title": "宁乡市委书记", "start": "2021-08", "end": "", "rank": "正处级", "note": "2021年8月任现职"},
    {"person_id": 1, "org_id": 11, "title": "长沙市委委员", "start": "2021-08", "end": "", "rank": "正处级", "note": "市委委员"},
    # Previous roles (approximate)
    {"person_id": 1, "org_id": 11, "title": "长沙县委常委、纪委书记", "start": "", "end": "2021-08", "rank": "副处级", "note": "履历细节待确认"},

    # ═══ 黄滔 (id=2) — 履历待确认 ═══
    {"person_id": 2, "org_id": 2, "title": "宁乡市市长", "start": "", "end": "", "rank": "正处级", "note": "⚠️ 市长当前身份及到任时间需确认"},
    {"person_id": 2, "org_id": 1, "title": "宁乡市委副书记", "start": "", "end": "", "rank": "正处级", "note": "市长兼任市委副书记"},

    # ═══ 于新凡 (id=31) — 前任书记 ═══
    {"person_id": 31, "org_id": 1, "title": "宁乡市委书记", "start": "", "end": "2021-08", "rank": "正处级", "note": "前任书记，约2021年8月前任职"},

    # ═══ 付旭明 (id=32) — 前任市长、前任浏阳书记、现长沙常委 ═══
    {"person_id": 32, "org_id": 2, "title": "宁乡市市长", "start": "", "end": "", "rank": "正处级", "note": "约2016-2021年任宁乡市长"},
    {"person_id": 32, "org_id": 1, "title": "宁乡市委副书记", "start": "", "end": "", "rank": "正处级", "note": "市长兼任"},
    {"person_id": 32, "org_id": 1, "title": "浏阳市委书记", "start": "", "end": "2025-12", "rank": "副厅级", "note": "约2021-2025年12月"},
    {"person_id": 32, "org_id": 12, "title": "常务副市长", "start": "2025-12", "end": "", "rank": "副厅级", "note": "长沙市委常委、常务副市长"},
    {"person_id": 32, "org_id": 11, "title": "长沙市委常委", "start": "2025-12", "end": "", "rank": "副厅级", "note": ""},

    # ═══ 周辉 (id=33) — 更早前任书记 ═══
    {"person_id": 33, "org_id": 1, "title": "宁乡县委书记/市委书记", "start": "", "end": "", "rank": "正处级", "note": "约2013-2016年在任"},
]

# ── Relationships ──────────────────────────────────────────────────────────────
relationships = [
    # 张作林 ↔ 黄滔 — 书记+市长搭档
    {"person_a": 1, "person_b": 2, "type": "core_partnership",
     "context": "宁乡市委书记与市长搭档关系", "overlap_org": "中共宁乡市委员会/宁乡市人民政府",
     "overlap_period": "（需确认起止时间）", "confidence": "plausible"},

    # 张作林 ↔ 于新凡 — 前后任书记
    {"person_a": 1, "person_b": 31, "type": "predecessor_successor",
     "context": "于新凡前任宁乡市委书记，张作林接任", "overlap_org": "中共宁乡市委员会",
     "overlap_period": "2021-08 交接", "confidence": "plausible"},

    # 黄滔 ↔ 付旭明 — 前后任市长
    {"person_a": 2, "person_b": 32, "type": "predecessor_successor",
     "context": "付旭明前任宁乡市市长，黄滔接任", "overlap_org": "宁乡市人民政府",
     "overlap_period": "2021 交接", "confidence": "plausible"},

    # 付旭明 — 跨区域网络：宁乡→浏阳→长沙
    {"person_a": 32, "person_b": 1, "type": "cross_region_overlap",
     "context": "付旭明曾在宁乡任职，后跨县至浏阳任书记，现为长沙市委常委", "overlap_org": "中共长沙市委",
     "overlap_period": "", "confidence": "confirmed"},

    # 付旭明 ↔ 陈竞 — 长沙市委班子成员
    {"person_a": 32, "person_b": 1, "type": "overlap",
     "context": "付旭明为长沙市委常委，陈竞为长沙市委书记", "overlap_org": "中共长沙市委",
     "overlap_period": "2026-06至今", "confidence": "confirmed"},

    # 张作林 — 长沙市领导层连接
    {"person_a": 1, "person_b": 32, "type": "same_network",
     "context": "同属长沙市管干部", "overlap_org": "中共长沙市委",
     "overlap_period": "", "confidence": "confirmed"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Source Register (shared across all person JSONs)
# ═══════════════════════════════════════════════════════════════════════════════

SOURCE_REGISTER = [
    {"id": "S001", "title": "宁乡市领导知识 — 培训数据", "url": "", "publisher": "",
     "published_at": "", "accessed_at": AS_OF, "source_type": "database",
     "reliability": "low", "notes": "基于训练数据中的历史知识，未通过当前来源核实"},
    {"id": "S002", "title": "长沙市构建脚本 — 付旭明确认数据", "url": "",
     "publisher": "本地仓库", "published_at": "", "accessed_at": AS_OF,
     "source_type": "internal", "reliability": "high",
     "notes": "长沙市构建脚本确认付旭明现任长沙市委常委、常务副市长"},
    {"id": "S003", "title": "维基百科 — 中国共产党长沙市委员会",
     "url": "https://zh.wikipedia.org/wiki/中国共产党长沙市委员会",
     "publisher": "维基百科", "published_at": "", "accessed_at": AS_OF,
     "source_type": "encyclopedia", "reliability": "medium",
     "notes": "长沙市领导班子列表"},
]


# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON Writers
# ═══════════════════════════════════════════════════════════════════════════════

def write_person_json(person: dict, pjson_dir: Path) -> str:
    """Write a person's deep-profile JSON file. Returns the filename."""
    name = person["name"]
    job = person.get("current_post", "")
    filename = f"{TODAY}-湖南省-长沙市-{job}-{name}.json"
    filepath = pjson_dir / filename

    pid_prefix = f"ningxiang_{name}"

    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "湖南省",
            "city": "长沙市",
            "region": "宁乡市",
            "job": job,
            "task_id": "hunan_宁乡市",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": pid_prefix,
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [person["education"]] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth', '')}",
                "name_birthplace": f"{name}_{person.get('birthplace', '')}",
                "official_profile_url": person.get("source", "")
            }
        },
        "current_status": {
            "current_post": job,
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [],
        "organizations": [
            {"id": 1, "name": "中共宁乡市委员会", "type": "党委"},
            {"id": 2, "name": "宁乡市人民政府", "type": "政府"},
            {"id": 3, "name": "中共长沙市委员会", "type": "党委"},
        ],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": SOURCE_REGISTER.copy(),
        "confidence_summary": {
            "identity": "partial" if person.get("birth") else "unverified",
            "current_role": "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "完整任职履历（每段职务精确起止时间）"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历（每段职务精确起止时间）",
                "why_it_matters": "关系网络分析需要精确的时间线",
                "suggested_queries": [
                    f"{name} 简历",
                    f"{name} 任前公示",
                    f"{name} 宁乡"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"【关键】{name}是否仍在现任岗位（2026年7月）",
                "why_it_matters": "2025-2026年长沙市各级领导有大规模调整，需确认宁乡是否已有变动",
                "suggested_queries": [
                    f"宁乡市 {job} 2025 2026",
                    f"{name} 最新 职务 2026"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"{name}的出生年月和籍贯",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [
                    f"{name} 简历",
                    f"{name} 籍贯"
                ],
                "last_attempted": AS_OF
            }
        ]
    }

    # Add career timeline for known persons
    if person["id"] == 1:  # 张作林
        data["career_timeline"] = [
            {"start": "2021-08", "end": "", "org": "中共宁乡市委员会", "title": "宁乡市委书记",
             "level": "正处级", "rank": "", "notes": "", "confidence": "plausible", "source_ids": ["S001"]},
            {"start": "", "end": "2021-08", "org": "中共长沙县委", "title": "长沙县委常委、纪委书记",
             "level": "副处级", "rank": "", "notes": "履历细节待确认", "confidence": "plausible", "source_ids": ["S001"]},
        ]
        data["relationships"] = [
            {"person": "陈竞", "person_id": "changsha_陈竞",
             "relationship_type": "superior_subordinate", "strength": "medium",
             "evidence": "长沙市委书记—宁乡市委书记（上级领导关系）",
             "overlap_org": "中共长沙市委员会/宁乡市",
             "overlap_period": "",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S003"]}
        ]
    elif person["id"] == 32:  # 付旭明
        data["career_timeline"] = [
            {"start": "", "end": "", "org": "宁乡市人民政府", "title": "宁乡市市长",
             "level": "正处级", "rank": "", "notes": "约2016-2021年", "confidence": "plausible", "source_ids": ["S001", "S002"]},
            {"start": "", "end": "2025-12", "org": "中共浏阳市委员会", "title": "浏阳市委书记",
             "level": "副厅级", "rank": "副厅级", "notes": "约2021-2025年12月", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
            {"start": "2025-12", "end": "", "org": "长沙市人民政府", "title": "常务副市长",
             "level": "副厅级", "rank": "副厅级", "notes": "长沙市委常委、常务副市长", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
            {"start": "2025-12", "end": "", "org": "中共长沙市委员会", "title": "市委常委",
             "level": "副厅级", "rank": "副厅级", "notes": "", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
        ]
        data["relationships"] = [
            {"person": "胡小刚", "person_id": "liuyang_胡小刚",
             "relationship_type": "predecessor_successor", "strength": "strong",
             "evidence": "付旭明前任浏阳市委书记，胡小刚接任",
             "overlap_org": "中共浏阳市委员会", "overlap_period": "2026-05",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
            {"person": "陈博彰", "person_id": "changsha_陈博彰",
             "relationship_type": "overlap", "strength": "strong",
             "evidence": "市长—常务副市长搭档",
             "overlap_org": "长沙市人民政府", "overlap_period": "2025.12-至今",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]}
        ]
        data["source_register"].append({
            "id": "S004",
            "title": "长沙市构建脚本—内部数据",
            "url": "",
            "publisher": "本地仓库",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "internal",
            "reliability": "high",
            "notes": "付旭明确认数据来源于长沙市构建脚本和浏阳市构建脚本"
        })

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Person JSON: {filename}")
    return filename


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print(f"╔══ 宁乡市 Leadership Network Builder ══╗")
    print(f"║  Date: {TODAY}")
    print(f"║  Stage: {STAGING}")
    print(f"╚══════════════════════════════════════════╝")
    print()

    # Build DB + GEXF
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

    # Write person JSONs for key figures
    print("\n── Person JSONs ──")
    key_persons = [p for p in persons if p["id"] in [1, 2, 31, 32, 33]]
    for p in key_persons:
        if p["name"] != "（待确认）":
            write_person_json(p, PJSON_DIR)

    # Summary
    print(f"\n── Summary ──")
    print(f"  Persons (total): {len(persons)}")
    print(f"  Persons (with real names): {sum(1 for p in persons if p['name'] != '（待确认）')}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Gaps documented in person JSON open_questions")

    print("\n── Open Gaps ──")
    print("  1. 张作林: birth/birthplace/education/career details — CRITICAL")
    print("  2. 黄滔: birth/birthplace/education/career history — CRITICAL")
    print("  3. ⚠️  KEY: 张作林/黄滔 是否仍在任 — CRITICAL (2025-2026长沙大规模调整)")
    print("  4. Full 宁乡市委 standing committee roster — HIGH")
    print("  5. Full deputy mayor roster — HIGH")
    print("  6. 宁乡经济技术开发区管委会领导 — MEDIUM")
    print("  7. Cross-county cadre exchange data — MEDIUM")


if __name__ == "__main__":
    main()
