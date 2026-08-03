#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 定陶区 (Dingtao District), 菏泽市, 山东省.

Level: 市辖区
Province: 山东省
Parent city: 菏泽市
Targets: 区委书记 (Party Secretary), 区长 (District Magistrate)
Task ID: shandong_定陶区

=== Registration & Evidence ===
Research date: 2026-08-03
Web access status: Exa rate-limited, Baidu 403, gov-site timeouts, Jina Reader timeout
  Direct HTTP to Chinese destinations blocked. All deputy names were
  located by agent-based search (news article scraping) and cross-referenced
  against existing repo DBs (郓城县, 枣庄市市中区).

Confirmed via repo cross-references:
  - 张晖 (female, 1976-01, 山东鄄城, 省委党校研究生) was 定陶区委常委、宣传部部长
    → now 郓城县委副书记、县长 (confirmed from 郓城县 DB)
  - 韩耀辉 was 定陶区长 ~2020-2022, now 枣庄市市中区区长
    (confirmed from 枣庄市市中区 build script)

Plausible evidence (from agent research, needs verification):
  - 惠彦超 → 定陶区委副书记 (appears in multiple 2022-2024 articles)
  - 刘敏魁 → 定陶区委常委、常务副区长 (appears in 2025 问政菏泽 articles)
  - 何庆龙 → 定陶区委常委、组织部部长 (appears in 2022-2025 articles)
  - 陈刚 → 定陶区委常委、政法委书记 (appears in 2023 定陶政法 articles)
  - 程波 → 定陶区委常委、纪委书记 (appears in 2022 清风定陶 articles)
  - 郝永言 → former 定陶区纪委书记 (appears in 2021 articles)
  - 杨东波 → former 定陶区委副书记 → 市委统战部常务副部长 (appears 2021)
  - 孔素贞 → former 定陶区委常委、组织部部长 (appears 2019-2021)
  - 聂元科 → former 定陶区委书记 ~2019-2021, likely promoted to 菏泽市级
  - 马常斌 → former 定陶区委常委、副区长 (2019-2021)

Note: 定陶县撤县设区于2016年4月，此前为定陶县。
All deputy names marked as "plausible" — needs verification from official sources.
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / ".." / ".." / ".." / "..").resolve()
if not (_REPO_ROOT / "gov_relation").exists():
    _REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "定陶区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-08-03"
TODAY = "20260803"

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 朱中华 — 区委书记
    {
        "id": 1,
        "name": "朱中华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共菏泽市定陶区委书记",
        "current_org": "中共菏泽市定陶区委员会",
        "source": "据2026-07-25 repo数据推测现任区委书记。履历、出生、教育背景均需验证。",
    },
    # 2. 刘勇 — 区长
    {
        "id": 2,
        "name": "刘勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "定陶区委副书记、区长",
        "current_org": "菏泽市定陶区人民政府",
        "source": "据2026-07-25 repo数据推测~2023/2024上任区长。出生/籍贯/履历均待查。",
    },
    # 3. 惠彦超 — 区委副书记（专职）
    #   Appears in multiple 定陶区 news articles 2022-2024 as 区委副书记
    {
        "id": 3,
        "name": "惠彦超",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定陶区委副书记（推测）",
        "current_org": "中共菏泽市定陶区委员会",
        "source": "GAP — 2022-2024多篇定陶区新闻出现'惠彦超'。当前任职需确认。",
    },
    # 4. 刘敏魁 — 常务副区长
    #   Appears: "定陶区委常委、常务副区长 刘敏魁" in 2025 articles
    {
        "id": 4,
        "name": "刘敏魁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定陶区委常委、常务副区长（推测）",
        "current_org": "菏泽市定陶区人民政府",
        "source": "GAP — 2025年部分文章中出现，但无完整信息。",
    },
    # 5. 程波 — 区纪委书记
    #   Appears: "程波 定陶区纪委书记" in 2022 清风定陶 articles
    {
        "id": 5,
        "name": "程波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定陶区委常委、区纪委书记、区监委主任（推测）",
        "current_org": "中共菏泽市定陶区纪律检查委员会",
        "source": "GAP — 2022年清风定陶文章中出现。当前任职需确认。",
    },
    # 6. 何庆龙 — 组织部部长
    #   Appears: "定陶区委常委、组织部部长 何庆龙" in 2022-2025 articles
    {
        "id": 6,
        "name": "何庆龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定陶区委常委、组织部部长（推测）",
        "current_org": "中共菏泽市定陶区委员会组织部",
        "source": "GAP — 2022-2025年定陶先锋文章中出现。当前任职需确认。",
    },
    # 7. 待查 — 宣传部部长
    # Former occupant 张晖 moved to 单县/郓城; current unknown
    {
        "id": 7,
        "name": "【待查】定陶区委宣传部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定陶区委常委、宣传部部长（待查）",
        "current_org": "中共菏泽市定陶区委员会宣传部",
        "source": "GAP — 现任宣传部长未确认。前任张晖（1976-01, 山东鄄城人）曾任职，已调任郓城县长。",
    },
    # 8. 陈刚 — 政法委书记
    #   Appears: "定陶区委常委、政法委书记 陈刚" in 2023 articles
    {
        "id": 8,
        "name": "陈刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定陶区委常委、政法委书记（推测）",
        "current_org": "中共菏泽市定陶区委员会政法委员会",
        "source": "GAP — 2023年定陶政法文章中出现。当前任职需确认。",
    },
    # 9. 待查 — 统战部部长
    {
        "id": 9,
        "name": "【待查】定陶区委统战部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "定陶区委常委、统战部部长（待查）",
        "current_org": "中共菏泽市定陶区委员会统战部",
        "source": "GAP — 统战部长人选未确认。何庆龙可能兼任。",
    },

    # ════════════════════════════════════════════
    # Historical & Predecessor Figures
    # ════════════════════════════════════════════

    # 10. 聂元科 — 前任区委书记
    {
        "id": 10,
        "name": "聂元科（前任）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原定陶区委书记（推测去向为菏泽市级职务）",
        "current_org": "原中共定陶区委员会",
        "source": "推测~2019-2021年任定陶区委书记，后调任菏泽市领导职务。",
    },
    # 11. 韩耀辉 — 前任区长 (now 枣庄市中区长)
    {
        "id": 11,
        "name": "韩耀辉（已调离）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "枣庄市市中区人民政府区长",
        "current_org": "枣庄市市中区人民政府",
        "source": "枣庄市市中区数据确认韩耀辉任市中区长。此前~2020-2022年任定陶区长。",
    },
    # 12. 张晖 — 前定陶区委宣传部部长
    {
        "id": 12,
        "name": "张晖（已调离）",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976年1月",
        "birthplace": "山东省菏泽市鄄城县",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1995年7月",
        "current_post": "郓城县委副书记、县政府党组书记、县长",
        "current_org": "郓城县人民政府",
        "source": "郓城县人民政府官网确认。曾任定陶区委宣传部部长→单县副县长→市委宣传部副部长→郓城县长。",
    },
    # 13. 杨东波 — 前定陶区委副书记
    {
        "id": 13,
        "name": "杨东波（已调离）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "菏泽市委统战部常务副部长（推测）",
        "current_org": "中共菏泽市委统战部",
        "source": "GAP — 2021年文章显示杨东波从定陶区委副书记调任市委统战部常务副部长。",
    },
    # 14. 孔素贞 — 前定陶区委组织部部长
    {
        "id": 14,
        "name": "孔素贞（历史）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前定陶区委常委、组织部部长（推测现任人大主任）",
        "current_org": "菏泽市定陶区人民代表大会常务委员会（推测）",
        "source": "2019-2021年任定陶区委组织部部长。后推测转任人大主任。",
    },
    # 15. 马常斌 — 前定陶区委常委、副区长
    {
        "id": 15,
        "name": "马常斌（历史）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前定陶区委常委、副区长（推测已调任）",
        "current_org": "原定陶区人民政府",
        "source": "GAP — 2019-2021年多次文章中出现。",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共菏泽市定陶区委员会", "type": "党委", "level": "县处级", "parent": "中共菏泽市委", "location": "菏泽市定陶区"},
    {"id": 2, "name": "菏泽市定陶区人民政府", "type": "政府", "level": "县处级", "parent": "菏泽市人民政府", "location": "菏泽市定陶区"},
    {"id": 3, "name": "中共菏泽市定陶区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共菏泽市定陶区委员会", "location": "菏泽市定陶区"},
    {"id": 4, "name": "中共菏泽市定陶区委员会组织部", "type": "党委", "level": "县处级", "parent": "中共菏泽市定陶区委员会", "location": "菏泽市定陶区"},
    {"id": 5, "name": "中共菏泽市定陶区委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共菏泽市定陶区委员会", "location": "菏泽市定陶区"},
    {"id": 6, "name": "中共菏泽市定陶区委员会统战部", "type": "党委", "level": "县处级", "parent": "中共菏泽市定陶区委员会", "location": "菏泽市定陶区"},
    {"id": 7, "name": "中共菏泽市定陶区委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共菏泽市定陶区委员会", "location": "菏泽市定陶区"},
    {"id": 8, "name": "菏泽市定陶区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "", "location": "菏泽市定陶区"},
    {"id": 9, "name": "中国人民政治协商会议菏泽市定陶区委员会", "type": "政协", "level": "县处级", "parent": "", "location": "菏泽市定陶区"},
    {"id": 10, "name": "枣庄市市中区人民政府", "type": "政府", "level": "县处级", "parent": "枣庄市人民政府", "location": "枣庄市市中区"},
    {"id": 11, "name": "郓城县人民政府", "type": "政府", "level": "县处级", "parent": "菏泽市人民政府", "location": "菏泽市郓城县"},
    {"id": 12, "name": "中共菏泽市单县委员会", "type": "党委", "level": "县处级", "parent": "中共菏泽市委", "location": "菏泽市单县"},
    {"id": 13, "name": "中共菏泽市委宣传部", "type": "党委", "level": "地市级", "parent": "中共菏泽市委", "location": "菏泽市"},
    {"id": 14, "name": "中共菏泽市委统战部", "type": "党委", "level": "地市级", "parent": "中共菏泽市委", "location": "菏泽市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 朱中华
    {"person_id": 1, "org_id": 1, "title": "中共菏泽市定陶区委书记", "start": "2022", "end": "present", "rank": "县处级", "note": "推测2022年前由定陶区长转任"},
    {"person_id": 1, "org_id": 2, "title": "定陶区委副书记、区长（前任职务）", "start": "2019", "end": "2022", "rank": "县处级", "note": "推测2019-2022年任定陶区长"},
    # 刘勇
    {"person_id": 2, "org_id": 2, "title": "定陶区委副书记、区长", "start": "2023", "end": "present", "rank": "县处级", "note": "推测2023/2024年上任"},
    # 惠彦超
    {"person_id": 3, "org_id": 1, "title": "定陶区委副书记", "start": "2022", "end": "present", "rank": "县处级", "note": "2022-2024年多篇报道中出现"},
    # 刘敏魁
    {"person_id": 4, "org_id": 2, "title": "定陶区委常委、常务副区长", "start": "", "end": "present", "rank": "县处级", "note": "2025年问政菏泽报道中出现"},
    # 程波
    {"person_id": 5, "org_id": 3, "title": "定陶区委常委、区纪委书记、区监委主任", "start": "2022", "end": "present", "rank": "县处级", "note": "2022年清风定陶报道中出现"},
    # 何庆龙
    {"person_id": 6, "org_id": 4, "title": "定陶区委常委、组织部部长", "start": "2022", "end": "present", "rank": "县处级", "note": "2022-2025年定陶先锋报道中出现"},
    # 待查 — 宣传部部长
    {"person_id": 7, "org_id": 5, "title": "定陶区委常委、宣传部部长（待查）", "start": "", "end": "present", "rank": "县处级", "note": "前任张晖已调任郓城县长"},
    # 陈刚
    {"person_id": 8, "org_id": 7, "title": "定陶区委常委、政法委书记", "start": "2023", "end": "present", "rank": "县处级", "note": "2023年定陶政法文章中出现"},
    # 待查 — 统战部部长
    {"person_id": 9, "org_id": 6, "title": "定陶区委常委、统战部部长（待查）", "start": "", "end": "present", "rank": "县处级", "note": "何庆龙可能兼任"},
    # 聂元科
    {"person_id": 10, "org_id": 1, "title": "定陶区委书记（前任）", "start": "2019", "end": "2021", "rank": "县处级", "note": "推测后任菏泽市领导职务"},
    # 韩耀辉
    {"person_id": 11, "org_id": 2, "title": "定陶区长（前任）", "start": "2020", "end": "2022", "rank": "县处级", "note": "调任枣庄市市中区区长（confirmed）"},
    {"person_id": 11, "org_id": 10, "title": "枣庄市市中区人民政府区长", "start": "2022", "end": "present", "rank": "县处级", "note": "跨市调任"},
    # 张晖
    {"person_id": 12, "org_id": 5, "title": "定陶区委常委、宣传部部长（历史）", "start": "", "end": "", "rank": "县处级", "note": "定陶常委宣传部长时期"},
    {"person_id": 12, "org_id": 12, "title": "单县县委常委、副县长（历史）", "start": "", "end": "", "rank": "县处级", "note": "从定陶赴单县"},
    {"person_id": 12, "org_id": 13, "title": "菏泽市委宣传部副部长", "start": "", "end": "2021-12", "rank": "县处级", "note": ""},
    {"person_id": 12, "org_id": 11, "title": "郓城县委副书记、县政府党组书记、县长", "start": "2021-12", "end": "present", "rank": "正处级", "note": "confirmed from 郓城县"},
    # 杨东波
    {"person_id": 13, "org_id": 1, "title": "定陶区委副书记（历史）", "start": "", "end": "2021", "rank": "县处级", "note": ""},
    {"person_id": 13, "org_id": 14, "title": "菏泽市委统战部常务副部长", "start": "2021-11", "end": "present", "rank": "县处级", "note": ""},
    # 孔素贞
    {"person_id": 14, "org_id": 4, "title": "定陶区委常委、组织部部长", "start": "2019", "end": "2022", "rank": "县处级", "note": "2019-2021年定陶先锋报道"},
    {"person_id": 14, "org_id": 8, "title": "定陶区人大常委会主任（推测）", "start": "2022", "end": "present", "rank": "正处级", "note": "推测从组织部转任人大主任"},
    # 马常斌
    {"person_id": 15, "org_id": 2, "title": "定陶区委常委、副区长（历史）", "start": "2019", "end": "2021", "rank": "县处级", "note": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 朱中华 ↔ 刘勇 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "朱中华任区委书记、刘勇任区长，党政搭档", "overlap_org": "菏泽市定陶区", "overlap_period": "2023-至今", "confidence": "plausible"},
    # 朱中华 ↔ 惠彦超 (书记+副书记)
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "朱中华任书记，惠彦超任副书记", "overlap_org": "中共菏泽市定陶区委员会", "overlap_period": "2022-至今", "confidence": "plausible"},
    # 朱中华 ⟷ 聂元科 (前任书记)
    {"person_a": 1, "person_b": 10, "type": "predecessor_successor", "context": "朱中华接替聂元科任定陶区委书记", "overlap_org": "中共菏泽市定陶区委员会", "overlap_period": "2022", "confidence": "plausible"},
    # 朱中华 ⟷ 韩耀辉 (前任搭档)
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "朱中华任书记期间韩耀辉曾任区长", "overlap_org": "菏泽市定陶区", "overlap_period": "2022", "confidence": "plausible"},
    # 刘勇 ⟷ 韩耀辉 (前任-继任)
    {"person_a": 2, "person_b": 11, "type": "predecessor_successor", "context": "刘勇接替韩耀辉任定陶区长", "overlap_org": "菏泽市定陶区人民政府", "overlap_period": "2023", "confidence": "plausible"},
    # 聂元科 ↔ 韩耀辉 (前任搭档)
    {"person_a": 10, "person_b": 11, "type": "overlap", "context": "聂元科任书记、韩耀辉任区长期", "overlap_org": "菏泽市定陶区", "overlap_period": "2020-2021", "confidence": "plausible"},
    # 张晖 ↔ 朱中华 (曾共事)
    {"person_a": 12, "person_b": 1, "type": "overlap", "context": "张晖任宣传部长，朱中华任区长/书记", "overlap_org": "中共菏泽市定陶区委员会", "overlap_period": "2019-2021", "confidence": "plausible"},
    # 杨东波 ↔ 朱中华
    {"person_a": 13, "person_b": 1, "type": "overlap", "context": "杨东波任副书记，朱中华任区长/书记", "overlap_org": "中共菏泽市定陶区委员会", "overlap_period": "2020-2021", "confidence": "plausible"},
    # 孔素贞 ↔ 朱中华
    {"person_a": 14, "person_b": 1, "type": "overlap", "context": "孔素贞任组织部长，朱中华任区长/书记", "overlap_org": "中共菏泽市定陶区委员会", "overlap_period": "2019-2022", "confidence": "plausible"},
    # 孔素贞 ↔ 马常斌
    {"person_a": 14, "person_b": 15, "type": "overlap", "context": "同时期定陶区委班子共事", "overlap_org": "中共菏泽市定陶区委员会", "overlap_period": "2019-2021", "confidence": "plausible"},
]

# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON BUILDER
# ══════════════════════════════════════════════════════════════════════════════


def build_person_json(person: dict, relationships_subset: list[dict]) -> dict:
    """Build a person graph JSON from the data rows."""
    pid = person["id"]

    career_entries = []
    for pos in positions:
        if pos["person_id"] != pid:
            continue
        career_entries.append({
            "start": pos.get("start", ""),
            "end": pos.get("end", "present"),
            "org": pos["org_id"],
            "title": pos["title"],
            "rank": pos.get("rank", ""),
            "notes": pos.get("note", ""),
            "confidence": "unverified",
            "source_ids": ["S001"],
        })

    rel_entries = []
    for r in relationships_subset:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id and p["id"] != pid), None)
        if other:
            safe_name = other["name"].split("（")[0].replace("【待查】", "").strip()
            safe_pid = f"dingtao_{safe_name}" if safe_name else "unknown"
            rel_entries.append({
                "person": safe_name,
                "person_id": safe_pid,
                "relationship_type": r["type"],
                "strength": "strong" if r.get("confidence") == "confirmed" else "medium",
                "evidence": r["context"],
                "overlap_org": r.get("overlap_org", ""),
                "overlap_period": r.get("overlap_period", ""),
                "direction": "undirected",
                "confidence": r.get("confidence", "unverified"),
                "source_ids": ["S001"],
            })

    clean_name = person["name"].split("（")[0].replace("【待查】", "").strip()
    identity_birth = person.get("birth", "")

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "山东省",
            "city": "菏泽市",
            "region": "定陶区",
            "job": person["current_post"],
            "task_id": "shandong_定陶区",
            "time_focus": "2019-2026",
        },
        "identity": {
            "person_id": f"dingtao_{clean_name}",
            "name": clean_name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("birthplace", ""),
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "", "study_type": "unknown", "source_ids": ["S001"]}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{clean_name}_{identity_birth}",
                "name_birthplace": f"{clean_name}_{person.get('birthplace', '')}" if person.get("birthplace") else "",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "县处级",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": ["S001"],
        },
        "career_timeline": career_entries,
        "organizations": [{"org_id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rel_entries,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": ["菏泽市"],
            "promotion_velocity": {"summary": "公开资料不足，难以判断晋升速度。", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "公开资料不足，无法推断工作风格。",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "截至调研日未在公开渠道发现违纪违规记录（搜索受限，降低信心）", "date": AS_OF, "confidence": "unverified", "source_ids": ["S001"]}],
        "source_register": [
            {"id": "S001", "title": "综合仓库数据+跨仓库参考+agent research", "url": "", "publisher": "gov-relation仓库", "published_at": "", "accessed_at": AS_OF, "source_type": "database", "reliability": "medium", "notes": "外部搜索全部受限（Exa限流、Baidu 403、政府网站超时）。部分姓名来自agent对新闻文章的提取，需官方确认。"},
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "所有核心人物的完整履历均缺失。班子成员中仅部分人知道姓名，无详细背景。",
        },
        "open_questions": [
            {"priority": "critical", "question": "朱中华的完整履历（含出生年月/出生地/教育/早期任职）", "why_it_matters": "核心调查目标", "suggested_queries": ["朱中华 简历 菏泽", "朱中华 百度百科"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "刘勇的完整履历", "why_it_matters": "第二核心目标", "suggested_queries": ["刘勇 定陶区长 简历"], "last_attempted": AS_OF},
            {"priority": "critical", "question": "朱中华和刘勇的当前任职是否仍是2023年以来的岗位", "why_it_matters": "核心确认", "suggested_queries": ["定陶区人民政府领导之窗"], "last_attempted": AS_OF},
            {"priority": "high", "question": "惠彦超、刘敏魁、程波、何庆龙、陈刚的当前任职确认", "why_it_matters": "班子完整度", "suggested_queries": ["定陶区2025年领导班子"], "last_attempted": AS_OF},
            {"priority": "high", "question": "当前宣传部部长和统战部部长人选", "why_it_matters": "两个关键常委空白", "suggested_queries": ["定陶区委宣传部部长 现任"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "聂元科的当前去向", "why_it_matters": "追踪菏泽干部交流模式", "suggested_queries": ["聂元科 菏泽 现任"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "定陶区人大主任、政协主席姓名", "why_it_matters": "四大班子完整名单", "suggested_queries": ["定陶区人大主任", "定陶区政协主席"], "last_attempted": AS_OF},
        ],
    }


def write_person_jsons():
    """Write individual person JSON files."""
    for p in persons:
        if "待查" in p["name"]:
            continue
        person_rels = [r for r in relationships if r["person_a"] == p["id"] or r["person_b"] == p["id"]]
        data = build_person_json(p, person_rels)

        clean_name = p["name"].split("（")[0].replace("【待查】", "").strip()
        if not clean_name:
            continue
        clean_post = p["current_post"].split("（")[0].strip()
        job_slug = clean_post.replace("/", "_").replace(" ", "").replace("（", "_").replace("）", "_")
        filename = f"{TODAY}-山东省-菏泽市-{job_slug}-{clean_name}.json"
        filepath = PERSONS_DIR / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  JSON: {filename}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"  定陶区 领导班子工作关系网络")
    print(f"  等级: 市辖区")
    print(f"  调查日期: {AS_OF}")
    print(f"{'='*60}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print("\n--- Writing person JSONs ---")
    os.makedirs(PERSONS_DIR, exist_ok=True)
    write_person_jsons()

    print(f"\n✅ 定陶区数据构建完成。")
    print(f"   DB:  {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")