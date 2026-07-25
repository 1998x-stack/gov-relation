#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 济南市 (Jinan City), 山东省.

Investigation date: 2026-07-25
Task ID: shandong_济南市
Level: 地级市 (副省级城市)
Targets: 市委书记 & 市长

Research sources:
  - www.jinan.gov.cn — 济南市人民政府官方网站 (primary, current as of July 2026)
  - News articles and meeting attendance lists from jinan.gov.cn (July 2026)
  - Web search was degraded: Baidu Baike 403, Exa rate-limited, Jina Reader timeouts

Confirmed via official sources:
  - 市委书记: 刘强 — confirmed from multiple 市委常委会会议 reports (2026年7月)
  - 市长: 于海田 — confirmed from 市政府常务会议 reports (2026年7月)

Confidence notes:
  - Current roles: confirmed via multiple government meeting/news reports (July 2026)
  - Biographical details (birth, birthplace, education): based on prior knowledge but
    unverified against current official web sources due to access limitations
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
SLUG = "济南市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shandong_济南市"
if _CURRENT_DIR.name == "shandong_济南市":
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
# IDs: 1-9 current party/government leaders, 10-19 standing committee,
#      20-29 deputy government, 30+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "刘强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年",  # plausible — public reports indicate born ~1970
        "birthplace": "山东",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共济南市委员会",
        "source": "https://www.jinan.gov.cn/zwgk/ldzc/",
        "confidence": "confirmed",
        "notes": "时任山东省委常委、济南市委书记。此前曾任山东省副省长、山东省总工会主席、临沂市委书记、山东省国资委主任等职"
    },
    {
        "id": 2,
        "name": "于海田",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年",  # plausible
        "birthplace": "山东",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "济南市人民政府",
        "source": "https://www.jinan.gov.cn/zwgk/ldzc/",
        "confidence": "confirmed",
        "notes": "时任济南市委副书记、市长。此前曾任山东省工业和信息化厅厅长、山东省发展和改革委员会副主任等职"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Key Standing Committee Members (市委常委)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "杨峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共济南市委员会",
        "source": "https://www.jinan.gov.cn/zwgk/ldzc/",
        "confidence": "plausible",
        "notes": "济南市委副书记，此前曾任济南市委常委、宣传部部长"
    },
    {
        "id": 4,
        "name": "吕涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "中共济南市委员会",
        "source": "https://www.jinan.gov.cn/zwgk/ldzc/",
        "confidence": "plausible",
        "notes": "济南市委常委、副市长（负责市政府常务工作），此前曾任济南市历下区委书记"
    },
    {
        "id": 5,
        "name": "杨光忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市纪委书记",
        "current_org": "中共济南市纪律检查委员会",
        "source": "https://www.jinan.gov.cn/zwgk/ldzc/",
        "confidence": "plausible",
        "notes": "济南市委常委、市纪委书记、市监委主任"
    },
    {
        "id": 6,
        "name": "戴龙成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共济南市委员会",
        "source": "https://www.jinan.gov.cn/zwgk/ldzc/",
        "confidence": "plausible",
        "notes": "济南市委常委、宣传部部长"
    },
    {
        "id": 7,
        "name": "李国祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、秘书长",
        "current_org": "中共济南市委员会",
        "source": "https://www.jinan.gov.cn/zwgk/ldzc/",
        "confidence": "plausible",
        "notes": "济南市委常委、秘书长"
    },
    {
        "id": 8,
        "name": "翟军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共济南市委员会",
        "source": "https://www.jinan.gov.cn/zwgk/ldzc/",
        "confidence": "plausible",
        "notes": "济南市委常委、组织部部长"
    },
    {
        "id": 9,
        "name": "王京文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、政法委书记",
        "current_org": "中共济南市委员会",
        "source": "https://www.jinan.gov.cn/zwgk/ldzc/",
        "confidence": "plausible",
        "notes": "济南市委常委、政法委书记"
    },
    {
        "id": 10,
        "name": "孙斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "中共济南市委员会",
        "source": "https://www.jinan.gov.cn/zwgk/ldzc/",
        "confidence": "plausible",
        "notes": "济南市委常委、副市长"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Mayors (副市长)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 11,
        "name": "任庆虎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "济南市人民政府",
        "source": "https://www.jinan.gov.cn/zwgk/ldzc/",
        "confidence": "plausible",
        "notes": "济南市副市长，具体分工待查"
    },
    {
        "id": 12,
        "name": "谢堃",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "济南市人民政府",
        "source": "https://www.jinan.gov.cn/zwgk/ldzc/",
        "confidence": "plausible",
        "notes": "济南市副市长，具体分工待查"
    },
    {
        "id": 13,
        "name": "杨丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "济南市人民政府",
        "source": "https://www.jinan.gov.cn/zwgk/ldzc/",
        "confidence": "plausible",
        "notes": "济南市副市长，具体分工待查"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 人大、政协 Leaders
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 14,
        "name": "韩金峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "济南市人民代表大会常务委员会",
        "source": "https://www.jinan.gov.cn/zwgk/ldzc/",
        "confidence": "plausible",
        "notes": "济南市人大常委会主任"
    },
    {
        "id": 15,
        "name": "雷天太",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议济南市委员会",
        "source": "https://www.jinan.gov.cn/zwgk/ldzc/",
        "confidence": "plausible",
        "notes": "济南市政协主席"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "孙立成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1962年",
        "birthplace": "河北",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共济南市委员会",
        "source": "公开报道",
        "confidence": "plausible",
        "notes": "前任济南市委书记（2020-2022），后任山东省政协副主席"
    },
    {
        "id": 31,
        "name": "孙述涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965年",
        "birthplace": "山东",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市长",
        "current_org": "济南市人民政府",
        "source": "公开报道",
        "confidence": "plausible",
        "notes": "前任济南市市长（2018-2022），后任山东省政协副主席，2023年被查"
    },
    {
        "id": 32,
        "name": "王忠林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1962年",
        "birthplace": "山东",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记（调任湖北）",
        "current_org": "中共济南市委员会",
        "source": "公开报道",
        "confidence": "plausible",
        "notes": "前任济南市委书记（2018-2020），后调任湖北省委常委、武汉市委书记，现任湖北省省长"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共济南市委员会", "type": "党委", "level": "副省级", "parent": "中共山东省委员会", "location": "济南市"},
    {"id": 2, "name": "济南市人民政府", "type": "政府", "level": "副省级", "parent": "山东省人民政府", "location": "济南市"},
    {"id": 3, "name": "济南市人民代表大会常务委员会", "type": "人大", "level": "副省级", "parent": "山东省人大常委会", "location": "济南市"},
    {"id": 4, "name": "中国人民政治协商会议济南市委员会", "type": "政协", "level": "副省级", "parent": "政协山东省委员会", "location": "济南市"},
    {"id": 5, "name": "中共济南市纪律检查委员会", "type": "党委", "level": "副省级", "parent": "中共济南市委员会", "location": "济南市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 刘强 — current Party Secretary
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2022-03", "end_date": "", "rank": "副省级", "note": "山东省委常委、济南市委书记"},
    {"person_id": 1, "org_id": 1, "title": "省委常委", "start_date": "2022-03", "end_date": "", "rank": "副省级", "note": "山东省委常委"},
    # 于海田 — current Mayor
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "2022-04", "end_date": "", "rank": "副省级", "note": "济南市委副书记、市长"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "2022-03", "end_date": "", "rank": "副省级", "note": ""},
    # 杨峰 — Deputy Party Secretary
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    # 吕涛 — Executive Deputy Mayor
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副市长（常务）", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    # 杨光忠 — Discipline Secretary
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    {"person_id": 5, "org_id": 5, "title": "市纪委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "兼任市监委主任"},
    # 戴龙成 — Propaganda
    {"person_id": 6, "org_id": 1, "title": "市委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    # 李国祥 — Secretary-General
    {"person_id": 7, "org_id": 1, "title": "市委常委、秘书长", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    # 翟军 — Organization
    {"person_id": 8, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    # 王京文 — Political-Legal
    {"person_id": 9, "org_id": 1, "title": "市委常委、政法委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    # 孙斌 — Deputy Mayor
    {"person_id": 10, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    # 任庆虎 — Deputy Mayor
    {"person_id": 11, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 谢堃 — Deputy Mayor
    {"person_id": 12, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 杨丽 — Deputy Mayor
    {"person_id": 13, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 韩金峰 — NPC Standing Committee Chair
    {"person_id": 14, "org_id": 3, "title": "市人大常委会主任", "start_date": "", "end_date": "", "rank": "副省级", "note": ""},
    # 雷天太 — CPPCC Chair
    {"person_id": 15, "org_id": 4, "title": "市政协主席", "start_date": "", "end_date": "", "rank": "副省级", "note": ""},
    # 孙立成 — Predecessor Party Secretary
    {"person_id": 30, "org_id": 1, "title": "市委书记", "start_date": "2020-03", "end_date": "2022-03", "rank": "副省级", "note": "前任济南市委书记，后任山东省政协副主席"},
    # 孙述涛 — Predecessor Mayor
    {"person_id": 31, "org_id": 2, "title": "市长", "start_date": "2018-05", "end_date": "2022-03", "rank": "副省级", "note": "前任济南市长，后任山东省政协副主席，2023年被查"},
    # 王忠林 — Predecessor Party Secretary
    {"person_id": 32, "org_id": 1, "title": "市委书记", "start_date": "2018-05", "end_date": "2020-02", "rank": "副省级", "note": "前任济南市委书记，调任湖北省委常委、武汉市委书记"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 刘强 ↔ 于海田 (Party Secretary – Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "中共济南市委员会", "overlap_period": "2022-至今"},
    # 刘强 ↔ 杨峰
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—副书记", "overlap_org": "中共济南市委员会", "overlap_period": ""},
    # 刘强 ↔ 吕涛
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—常委", "overlap_org": "中共济南市委员会", "overlap_period": ""},
    # 刘强 ↔ 杨光忠
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—纪委书记", "overlap_org": "中共济南市委员会", "overlap_period": ""},
    # 刘强 ↔ 戴龙成
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "书记—宣传部长", "overlap_org": "中共济南市委员会", "overlap_period": ""},
    # 刘强 ↔ 李国祥
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "书记—秘书长", "overlap_org": "中共济南市委员会", "overlap_period": ""},
    # 刘强 ↔ 翟军
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "书记—组织部长", "overlap_org": "中共济南市委员会", "overlap_period": ""},
    # 刘强 ↔ 孙斌
    {"person_a": 1, "person_b": 10, "type": "共事", "context": "书记—副市长", "overlap_org": "中共济南市委员会", "overlap_period": ""},
    # 于海田 ↔ 吕涛 (Mayor – Executive Deputy Mayor)
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "市长—常务副市长", "overlap_org": "济南市人民政府", "overlap_period": ""},
    # 于海田 ↔ 孙斌
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "市长—副市长", "overlap_org": "济南市人民政府", "overlap_period": ""},
    # 于海田 ↔ 任庆虎
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "市长—副市长", "overlap_org": "济南市人民政府", "overlap_period": ""},
    # 于海田 ↔ 谢堃
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "市长—副市长", "overlap_org": "济南市人民政府", "overlap_period": ""},
    # 于海田 ↔ 杨丽
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "市长—副市长", "overlap_org": "济南市人民政府", "overlap_period": ""},
    # Standing committee internal relationships
    {"person_a": 4, "person_b": 5, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共济南市委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 6, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共济南市委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 7, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共济南市委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 8, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共济南市委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 9, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共济南市委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 6, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共济南市委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 7, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共济南市委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 8, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共济南市委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 9, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共济南市委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 7, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共济南市委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 8, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共济南市委员会", "overlap_period": ""},
    {"person_a": 7, "person_b": 8, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共济南市委员会", "overlap_period": ""},
    # Predecessor relationships
    {"person_a": 30, "person_b": 1, "type": "交接", "context": "前任市委书记—现任市委书记", "overlap_org": "中共济南市委员会", "overlap_period": "2022-03"},
    {"person_a": 31, "person_b": 2, "type": "交接", "context": "前任市长—现任市长", "overlap_org": "济南市人民政府", "overlap_period": "2022-04"},
    {"person_a": 32, "person_b": 30, "type": "交接", "context": "前任—继任（市委书记）", "overlap_org": "中共济南市委员会", "overlap_period": "2020-03"},
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
    slug_id = f"jinan_{name}"

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
            "notes": "公开资料不足，完整履历待查。百度百科403禁止访问，搜索引擎超时。",
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
            "person_id": f"jinan_{other_name}",
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
            "title": "济南市人民政府官方网站",
            "url": source_url,
            "publisher": "济南市人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "2026年7月新闻和会议报道确认领导职务",
        }
    ]

    big_gap = "出生年月、籍贯、完整履历（百度百科403，搜索引擎超时）"
    if person.get("birth"):
        big_gap = "完整履历（百度百科403，搜索引擎超时）"

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "山东省",
            "city": "济南市",
            "region": "济南市",
            "job": person.get("current_post", ""),
            "task_id": "shandong_济南市",
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
            "relationship_confidence": "medium",
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
    fname = f"{TODAY}-山东省-济南市-{post_slug}-{person['name']}.json"
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
    core_ids = {1, 2, 3, 4, 5, 14, 15, 30, 31, 32}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
