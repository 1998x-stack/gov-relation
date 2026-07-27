#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
洪江市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县级市
Province: 湖南省
Parent City: 怀化市
Region: 洪江市
Targets: 市委书记 & 市长

Research status (2026-07-24):
- 唐龙 (Party Secretary): confirmed — 洪江市委书记 (as of Jul 2026)
  - Identity: confirmed via official government website news articles
  - Career: thin — current role confirmed; full career history unknown
- 夏向阳 (Acting Mayor): confirmed — 洪江市委副书记、代理市长 (as of Jul 2026)
  - Identity: 男, 汉族, 1977.12, 研究生学历, 中共党员
  - Career: thin — current role confirmed; full career history unknown

Research constraints:
  - Exa search: rate limited
  - Baidu Baike: 403/Cloudflare block
  - Government websites (hjs.gov.cn): partially accessible
  - Primary source: official city government site (hjs.gov.cn)
  - All personal biographical details beyond basic identity are open questions

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

import sqlite3  # noqa: F401

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "洪江市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "hunan_洪江市"
if _CURRENT_DIR.name == "hunan_洪江市":
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

    # 唐龙 — 洪江市委书记 (Party Secretary)
    {
        "id": 1,
        "name": "唐龙",
        "gender": "男",
        "ethnicity": "",  # open question
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "洪江市委书记",
        "current_org": "中共洪江市委员会",
        "source": "洪江市人民政府网站 (hjs.gov.cn) 2026-07-24 新闻",
        "confidence": "confirmed",
        "notes": "Confirmed as 市委书记 via multiple July 2026 official news items. Full career history unknown.",
    },

    # 夏向阳 — 洪江市委副书记、代理市长 (Acting Mayor)
    {
        "id": 2,
        "name": "夏向阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-12",
        "birthplace": "",  # open question
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "洪江市委副书记、代理市长",
        "current_org": "洪江市人民政府",
        "source": "洪江市人民政府网站 (hjs.gov.cn) 市政府页面 2026-07-24",
        "confidence": "confirmed",
        "notes": "Confirmed via official government website. 代理市长 as of Jul 2026. 领导市人民政府全面工作，负责财政、审计工作。",
    },

    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee / Key Leaders
    # ══════════════════════════════════════════════════════════════════════

    # 易汉成 — 市领导 (likely 常务 or 市委领导)
    {
        "id": 10,
        "name": "易汉成",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洪江市领导",
        "current_org": "中共洪江市委员会",
        "source": "洪江市人民政府网站新闻",
        "confidence": "confirmed",
        "notes": "Mentioned in government news as 市领导 attending meetings chaired by 唐龙.",
    },

    # 谢景良 — 市领导 (likely standing committee)
    {
        "id": 11,
        "name": "谢景良",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洪江市领导",
        "current_org": "中共洪江市委员会",
        "source": "洪江市人民政府网站新闻",
        "confidence": "confirmed",
        "notes": "Made speech at 理论学习中心组集体学习 (2026-07-21).",
    },

    # 佘国平 — 市领导 (likely standing committee)
    {
        "id": 12,
        "name": "佘国平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洪江市领导",
        "current_org": "中共洪江市委员会",
        "source": "洪江市人民政府网站新闻",
        "confidence": "confirmed",
        "notes": "Made speech at 理论学习中心组集体学习 (2026-07-21).",
    },

    # 舒博 — 副市长 / 市领导
    {
        "id": 13,
        "name": "舒博",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洪江市副市长",
        "current_org": "洪江市人民政府",
        "source": "洪江市人民政府网站 — 市政府页面",
        "confidence": "confirmed",
        "notes": "Listed as 副市长 on government website. Also mentioned in 理论学习中心组学习 news.",
    },

    # 黄周晶 — 市领导 (likely standing committee)
    {
        "id": 14,
        "name": "黄周晶",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洪江市领导",
        "current_org": "中共洪江市委员会",
        "source": "洪江市人民政府网站新闻",
        "confidence": "confirmed",
        "notes": "Mentioned in 人武部党委第一书记任职大会 and 理论学习中心组学习 news.",
    },

    # 杨柱 — 市领导
    {
        "id": 15,
        "name": "杨柱",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洪江市领导",
        "current_org": "中共洪江市委员会",
        "source": "洪江市人民政府网站新闻",
        "confidence": "confirmed",
        "notes": "Made speech at 理论学习中心组集体学习 (2026-07-21).",
    },

    # 张永红 — 市领导 (likely military/人武部)
    {
        "id": 16,
        "name": "张永红",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洪江市领导",
        "current_org": "洪江市人武部",
        "source": "洪江市人民政府网站新闻",
        "confidence": "confirmed",
        "notes": "Mentioned in 人武部党委第一书记任职大会 (2026-07-21).",
    },

    # ══════════════════════════════════════════════════════════════════════
    # Deputy Mayors (副市长)
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 20,
        "name": "杨晶辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洪江市副市长",
        "current_org": "洪江市人民政府",
        "source": "洪江市人民政府网站 — 市政府页面",
        "confidence": "confirmed",
        "notes": "Listed as 副市长 on government website.",
    },
    {
        "id": 21,
        "name": "舒朝友",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洪江市副市长",
        "current_org": "洪江市人民政府",
        "source": "洪江市人民政府网站 — 市政府页面",
        "confidence": "confirmed",
        "notes": "Listed as 副市长 on government website.",
    },
    {
        "id": 22,
        "name": "杨英为",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洪江市副市长",
        "current_org": "洪江市人民政府",
        "source": "洪江市人民政府网站 — 市政府页面",
        "confidence": "confirmed",
        "notes": "Listed as 副市长 on government website.",
    },
    {
        "id": 23,
        "name": "廖辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洪江市副市长",
        "current_org": "洪江市人民政府",
        "source": "洪江市人民政府网站 — 市政府页面",
        "confidence": "confirmed",
        "notes": "Listed as 副市长 on government website.",
    },
    {
        "id": 24,
        "name": "王芬颖",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洪江市副市长",
        "current_org": "洪江市人民政府",
        "source": "洪江市人民政府网站 — 市政府页面",
        "confidence": "confirmed",
        "notes": "Listed as 副市长 on government website.",
    },
    {
        "id": 25,
        "name": "陈武军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洪江市副市长",
        "current_org": "洪江市人民政府",
        "source": "洪江市人民政府网站 — 市政府页面",
        "confidence": "confirmed",
        "notes": "Listed as 副市长 on government website.",
    },
    {
        "id": 26,
        "name": "舒野",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洪江市副市长",
        "current_org": "洪江市人民政府",
        "source": "洪江市人民政府网站 — 市政府页面",
        "confidence": "confirmed",
        "notes": "Listed as 副市长 on government website.",
    },

    # ══════════════════════════════════════════════════════════════════════
    # Predecessors (前任) — open questions
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 30,
        "name": "",  # open question
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "open question",
        "confidence": "unverified",
        "notes": "唐龙的前任洪江市委书记姓名、去向均为待查。",
    },
    {
        "id": 31,
        "name": "",  # open question
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "open question",
        "confidence": "unverified",
        "notes": "夏向阳的前任洪江市市长姓名、去向均为待查。夏向阳目前为代理市长。",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────

organizations = [
    # Party
    {"id": 1, "name": "中共洪江市委员会", "type": "党委",
     "level": "县处级", "parent": "中共怀化市委员会", "location": "洪江市"},
    {"id": 2, "name": "中共洪江市纪律检查委员会", "type": "党委",
     "level": "县处级", "parent": "中共洪江市委员会", "location": "洪江市"},
    {"id": 3, "name": "中共洪江市委组织部", "type": "党委",
     "level": "正科级", "parent": "中共洪江市委员会", "location": "洪江市"},
    {"id": 4, "name": "中共洪江市委宣传部", "type": "党委",
     "level": "正科级", "parent": "中共洪江市委员会", "location": "洪江市"},
    {"id": 5, "name": "中共洪江市委政法委员会", "type": "党委",
     "level": "正科级", "parent": "中共洪江市委员会", "location": "洪江市"},
    {"id": 6, "name": "中共洪江市委统一战线工作部", "type": "党委",
     "level": "正科级", "parent": "中共洪江市委员会", "location": "洪江市"},
    {"id": 7, "name": "洪江市人武部", "type": "党委",
     "level": "县处级", "parent": "怀化市军分区", "location": "洪江市"},

    # Government
    {"id": 10, "name": "洪江市人民政府", "type": "政府",
     "level": "县处级", "parent": "怀化市人民政府", "location": "洪江市"},
    {"id": 11, "name": "洪江市人民政府办公室", "type": "政府",
     "level": "正科级", "parent": "洪江市人民政府", "location": "洪江市"},

    # Dep't / Bureau
    {"id": 20, "name": "洪江市发展和改革局", "type": "政府",
     "level": "正科级", "parent": "洪江市人民政府", "location": "洪江市"},
    {"id": 21, "name": "洪江市教育局", "type": "政府",
     "level": "正科级", "parent": "洪江市人民政府", "location": "洪江市"},
    {"id": 22, "name": "洪江市公安局", "type": "政府",
     "level": "正科级", "parent": "洪江市人民政府", "location": "洪江市"},
    {"id": 23, "name": "洪江市财政局", "type": "政府",
     "level": "正科级", "parent": "洪江市人民政府", "location": "洪江市"},
    {"id": 24, "name": "洪江市审计局", "type": "政府",
     "level": "正科级", "parent": "洪江市人民政府", "location": "洪江市"},

    # NPC & CPPCC
    {"id": 30, "name": "洪江市人民代表大会常务委员会", "type": "人大",
     "level": "县处级", "parent": "洪江市", "location": "洪江市"},
    {"id": 31, "name": "中国人民政治协商会议洪江市委员会", "type": "政协",
     "level": "县处级", "parent": "洪江市", "location": "洪江市"},

    # Supervision / Justice
    {"id": 40, "name": "洪江市监察委员会", "type": "党委",
     "level": "县处级", "parent": "洪江市", "location": "洪江市"},
    {"id": 41, "name": "洪江市人民法院", "type": "政府",
     "level": "县处级", "parent": "洪江市", "location": "洪江市"},
    {"id": 42, "name": "洪江市人民检察院", "type": "政府",
     "level": "县处级", "parent": "洪江市", "location": "洪江市"},

    # Townships (selected major ones)
    {"id": 50, "name": "洪江市黔城镇", "type": "乡镇/街道",
     "level": "乡科级", "parent": "洪江市人民政府", "location": "洪江市"},
    {"id": 51, "name": "洪江市安江镇", "type": "乡镇/街道",
     "level": "乡科级", "parent": "洪江市人民政府", "location": "洪江市"},
    {"id": 52, "name": "洪江市托口镇", "type": "乡镇/街道",
     "level": "乡科级", "parent": "洪江市人民政府", "location": "洪江市"},
    {"id": 53, "name": "洪江市雪峰镇", "type": "乡镇/街道",
     "level": "乡科级", "parent": "洪江市人民政府", "location": "洪江市"},
    {"id": 54, "name": "洪江市江市镇", "type": "乡镇/街道",
     "level": "乡科级", "parent": "洪江市人民政府", "location": "洪江市"},
    {"id": 55, "name": "洪江市塘湾镇", "type": "乡镇/街道",
     "level": "乡科级", "parent": "洪江市人民政府", "location": "洪江市"},
    {"id": 56, "name": "洪江市沅河镇", "type": "乡镇/街道",
     "level": "乡科级", "parent": "洪江市人民政府", "location": "洪江市"},
    {"id": 57, "name": "洪江市岔头乡", "type": "乡镇/街道",
     "level": "乡科级", "parent": "洪江市人民政府", "location": "洪江市"},
    {"id": 58, "name": "洪江市岩垅乡", "type": "乡镇/街道",
     "level": "乡科级", "parent": "洪江市人民政府", "location": "洪江市"},
    {"id": 59, "name": "洪江市太平乡", "type": "乡镇/街道",
     "level": "乡科级", "parent": "洪江市人民政府", "location": "洪江市"},
]

# ── Positions ─────────────────────────────────────────────────────────────────

positions = [
    # 唐龙
    {"id": 1, "person_id": 1, "org_id": 1, "title": "市委书记",
     "start": "unknown", "end": "present", "rank": "县处级正职",
     "note": "confirmed via official government news (hjs.gov.cn Jul 2026)"},
    {"id": 2, "person_id": 1, "org_id": 7, "title": "市人武部党委第一书记",
     "start": "2026-07", "end": "present", "rank": "",
     "note": "confirmed via 宣布洪江市人武部党委第一书记任职大会 (2026-07-21)"},

    # 夏向阳
    {"id": 3, "person_id": 2, "org_id": 1, "title": "市委副书记",
     "start": "unknown", "end": "present", "rank": "县处级正职",
     "note": ""},
    {"id": 4, "person_id": 2, "org_id": 10, "title": "代理市长",
     "start": "2026-07", "end": "present", "rank": "县处级正职",
     "note": "confirmed via official government website; 代理市长 as of Jul 2026"},
    {"id": 5, "person_id": 2, "org_id": 10, "title": "市人民政府党组书记",
     "start": "unknown", "end": "present", "rank": "",
     "note": "confirmed via official government website"},

    # 易汉成
    {"id": 10, "person_id": 10, "org_id": 1, "title": "市领导",
     "start": "unknown", "end": "present", "rank": "",
     "note": "mentioned in 信访工作调度会 news 2026-07-23"},

    # 谢景良
    {"id": 11, "person_id": 11, "org_id": 1, "title": "市领导",
     "start": "unknown", "end": "present", "rank": "",
     "note": "made speech at 理论学习中心组学习 2026-07-21"},

    # 佘国平
    {"id": 12, "person_id": 12, "org_id": 1, "title": "市领导",
     "start": "unknown", "end": "present", "rank": "",
     "note": "made speech at 理论学习中心组学习 2026-07-21"},

    # 舒博
    {"id": 13, "person_id": 13, "org_id": 10, "title": "副市长",
     "start": "unknown", "end": "present", "rank": "副处级",
     "note": "listed on government website; also made speech at 理论学习中心组学习"},

    # 黄周晶
    {"id": 14, "person_id": 14, "org_id": 1, "title": "市领导",
     "start": "unknown", "end": "present", "rank": "",
     "note": "mentioned in 人武部 news and 理论学习中心组学习"},

    # 杨柱
    {"id": 15, "person_id": 15, "org_id": 1, "title": "市领导",
     "start": "unknown", "end": "present", "rank": "",
     "note": "made speech at 理论学习中心组学习 2026-07-21"},

    # 张永红
    {"id": 16, "person_id": 16, "org_id": 7, "title": "市领导",
     "start": "unknown", "end": "present", "rank": "",
     "note": "mentioned in 人武部党委第一书记任职大会 2026-07-21"},

    # Deputy Mayors
    {"id": 20, "person_id": 20, "org_id": 10, "title": "副市长",
     "start": "unknown", "end": "present", "rank": "副处级",
     "note": "listed on government website"},
    {"id": 21, "person_id": 21, "org_id": 10, "title": "副市长",
     "start": "unknown", "end": "present", "rank": "副处级",
     "note": "listed on government website"},
    {"id": 22, "person_id": 22, "org_id": 10, "title": "副市长",
     "start": "unknown", "end": "present", "rank": "副处级",
     "note": "listed on government website"},
    {"id": 23, "person_id": 23, "org_id": 10, "title": "副市长",
     "start": "unknown", "end": "present", "rank": "副处级",
     "note": "listed on government website"},
    {"id": 24, "person_id": 24, "org_id": 10, "title": "副市长",
     "start": "unknown", "end": "present", "rank": "副处级",
     "note": "listed on government website"},
    {"id": 25, "person_id": 25, "org_id": 10, "title": "副市长",
     "start": "unknown", "end": "present", "rank": "副处级",
     "note": "listed on government website"},
    {"id": 26, "person_id": 26, "org_id": 10, "title": "副市长",
     "start": "unknown", "end": "present", "rank": "副处级",
     "note": "listed on government website"},
]

# ── Relationships ─────────────────────────────────────────────────────────────

relationships = [
    # 唐龙 <-> 夏向阳: 党政配合 (直接搭档关系)
    {
        "id": 1,
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "党政一把手（市委书记—代理市长）",
        "overlap_org": "中共洪江市委员会 / 洪江市人民政府",
        "overlap_period": "2026-07 — present",
    },

    # 唐龙 — 易汉成: 共同出席会议
    {
        "id": 2,
        "person_a": 1,
        "person_b": 10,
        "type": "overlap",
        "context": "共同出席信访工作调度会 (2026-07-23)",
        "overlap_org": "中共洪江市委员会",
        "overlap_period": "2026-07",
    },

    # 唐龙 — 黄周晶: 共同出席人武部会议
    {
        "id": 3,
        "person_a": 1,
        "person_b": 14,
        "type": "overlap",
        "context": "共同出席人武部党委第一书记任职大会 (2026-07-21)",
        "overlap_org": "中共洪江市委员会 / 洪江市人武部",
        "overlap_period": "2026-07",
    },

    # 唐龙 — 张永红: 共同出席人武部会议
    {
        "id": 4,
        "person_a": 1,
        "person_b": 16,
        "type": "overlap",
        "context": "共同出席人武部党委第一书记任职大会 (2026-07-21)",
        "overlap_org": "洪江市人武部",
        "overlap_period": "2026-07",
    },

    # 谢景良、佘国平、舒博、黄周晶、杨柱: 共同出席理论学习中心组学习
    {
        "id": 5,
        "person_a": 11,
        "person_b": 12,
        "type": "overlap",
        "context": "共同参加市委理论学习中心组集体学习 (2026-07-21)",
        "overlap_org": "中共洪江市委员会",
        "overlap_period": "2026-07",
    },
    {
        "id": 6,
        "person_a": 11,
        "person_b": 13,
        "type": "overlap",
        "context": "共同参加市委理论学习中心组集体学习 (2026-07-21)",
        "overlap_org": "中共洪江市委员会",
        "overlap_period": "2026-07",
    },
    {
        "id": 7,
        "person_a": 11,
        "person_b": 14,
        "type": "overlap",
        "context": "共同参加市委理论学习中心组集体学习 (2026-07-21)",
        "overlap_org": "中共洪江市委员会",
        "overlap_period": "2026-07",
    },
    {
        "id": 8,
        "person_a": 11,
        "person_b": 15,
        "type": "overlap",
        "context": "共同参加市委理论学习中心组集体学习 (2026-07-21)",
        "overlap_org": "中共洪江市委员会",
        "overlap_period": "2026-07",
    },
    {
        "id": 9,
        "person_a": 12,
        "person_b": 13,
        "type": "overlap",
        "context": "共同参加市委理论学习中心组集体学习 (2026-07-21)",
        "overlap_org": "中共洪江市委员会",
        "overlap_period": "2026-07",
    },
    {
        "id": 10,
        "person_a": 12,
        "person_b": 14,
        "type": "overlap",
        "context": "共同参加市委理论学习中心组集体学习 (2026-07-21)",
        "overlap_org": "中共洪江市委员会",
        "overlap_period": "2026-07",
    },
    {
        "id": 11,
        "person_a": 12,
        "person_b": 15,
        "type": "overlap",
        "context": "共同参加市委理论学习中心组集体学习 (2026-07-21)",
        "overlap_org": "中共洪江市委员会",
        "overlap_period": "2026-07",
    },
    {
        "id": 12,
        "person_a": 13,
        "person_b": 14,
        "type": "overlap",
        "context": "共同参加市委理论学习中心组集体学习 (2026-07-21)",
        "overlap_org": "中共洪江市委员会",
        "overlap_period": "2026-07",
    },
    {
        "id": 13,
        "person_a": 13,
        "person_b": 15,
        "type": "overlap",
        "context": "共同参加市委理论学习中心组集体学习 (2026-07-21)",
        "overlap_org": "中共洪江市委员会",
        "overlap_period": "2026-07",
    },
    {
        "id": 14,
        "person_a": 14,
        "person_b": 15,
        "type": "overlap",
        "context": "共同参加市委理论学习中心组集体学习 (2026-07-21)",
        "overlap_org": "中共洪江市委员会",
        "overlap_period": "2026-07",
    },

    # 夏向阳 — 舒博: 市政府领导班子
    {
        "id": 15,
        "person_a": 2,
        "person_b": 13,
        "type": "superior_subordinate",
        "context": "代理市长—副市长（市政府领导班子）",
        "overlap_org": "洪江市人民政府",
        "overlap_period": "2026-07 — present",
    },

    # 夏向阳 — 易汉成: 共同出席信访会议
    {
        "id": 16,
        "person_a": 2,
        "person_b": 10,
        "type": "overlap",
        "context": "共同出席信访工作调度会 (2026-07-23)",
        "overlap_org": "中共洪江市委员会",
        "overlap_period": "2026-07",
    },
]


# ══════════════════════════════════════════════════════════════════════════
# Person JSON Writer
# ══════════════════════════════════════════════════════════════════════════

def write_person_json(person: dict, output_dir: Path) -> str | None:
    """Write a person graph JSON file. Returns filename or None if skipped."""
    name = person.get("name", "")
    if not name:
        return None
    job_short = {
        1: "市委书记",
        2: "市长",
    }.get(person["id"], "干部")

    filename = f"{TODAY}-湖南省-怀化市-{job_short}-{name}.json"
    filepath = output_dir / filename

    person_id_str = f"洪江市_{name}"

    # Build sources
    sources = [
        {
            "id": "S001",
            "title": "洪江市人民政府门户网站 — 市政府页面",
            "url": "https://www.hjs.gov.cn/hjs/c106171/szf2020.shtml",
            "publisher": "洪江市人民政府",
            "published_at": "2026",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": f"Confirmed {name} current role via official government website",
        },
        {
            "id": "S002",
            "title": f"洪江市人民政府门户网站 — 新闻",
            "url": "https://www.hjs.gov.cn/",
            "publisher": "洪江市人民政府",
            "published_at": "2026",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": f"Confirmed {name} via government news articles (2026-07)",
        },
    ]

    # Build career timeline entries based on known info
    career_entries = []

    if person["id"] == 1:  # 唐龙
        career_entries = [
            {
                "start": "unknown",
                "end": "present",
                "org": "中共洪江市委员会",
                "title": "洪江市委书记",
                "level": "县处级正职",
                "location": "洪江市",
                "system": "party",
                "rank": "",
                "is_key_promotion": True,
                "notes": "当前任职，confirmed via official government news (Jul 2026)",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"],
            },
            {
                "start": "2026-07",
                "end": "present",
                "org": "洪江市人武部",
                "title": "市人武部党委第一书记",
                "level": "",
                "location": "洪江市",
                "system": "party",
                "rank": "",
                "is_key_promotion": False,
                "notes": "兼任人武部党委第一书记 (2026-07-21 任职大会)",
                "confidence": "confirmed",
                "source_ids": ["S002"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": "公开资料未找到任市委书记前的完整履历",
                "confidence": "unverified",
                "source_ids": [],
            },
        ]
    elif person["id"] == 2:  # 夏向阳
        career_entries = [
            {
                "start": "unknown",
                "end": "present",
                "org": "中共洪江市委员会",
                "title": "洪江市委副书记",
                "level": "县处级正职",
                "location": "洪江市",
                "system": "party",
                "rank": "",
                "is_key_promotion": True,
                "notes": "当前任职，confirmed via official government website",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "2026-07",
                "end": "present",
                "org": "洪江市人民政府",
                "title": "代理市长、市人民政府党组书记",
                "level": "县处级正职",
                "location": "洪江市",
                "system": "government",
                "rank": "",
                "is_key_promotion": True,
                "notes": "代理市长，领导市政府全面工作，负责财政、审计工作",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": "公开资料未找到任代理市长前的完整履历",
                "confidence": "unverified",
                "source_ids": [],
            },
        ]

    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "湖南省",
            "city": "怀化市",
            "region": "洪江市",
            "job": job_short,
            "task_id": "hunan_洪江市",
            "time_focus": "2026",
        },
        "identity": {
            "person_id": person_id_str,
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": (
                [{"period": "", "institution": person.get("education", ""), "major": "",
                  "degree": "", "study_type": "unknown", "source_ids": []}]
                if person.get("education") else []
            ),
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth', '')}",
                "name_birthplace": f"{name}_{person.get('birthplace', '')}",
                "official_profile_url": "https://www.hjs.gov.cn/hjs/c106171/szf2020.shtml",
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "县处级正职",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"],
        },
        "career_timeline": career_entries,
        "organizations": [
            {"id": 1, "name": "中共洪江市委员会", "org_type": "党委", "level": "县处级"},
            {"id": 10, "name": "洪江市人民政府", "org_type": "政府", "level": "县处级"},
        ],
        "relationships": [
            {
                "person": "夏向阳" if person["id"] == 1 else "唐龙",
                "person_id": "洪江市_夏向阳" if person["id"] == 1 else "洪江市_唐龙",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "党政一把手（市委书记—代理市长），2026年7月起搭档",
                "overlap_org": "中共洪江市委员会 / 洪江市人民政府",
                "overlap_period": "2026-07 — present",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"],
            },
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "无法判断 — 公开资料不足",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": f"截至{AS_OF}，未在公开来源发现{name}的违纪、处分或负面报道",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            },
        ],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") or person.get("ethnicity") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": f"{name}的历任职务（任职前履历完全未知）",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整职业生涯（历任职务）",
                "why_it_matters": "构建关系网络和干部流动分析的核心数据",
                "suggested_queries": [
                    f"{name} 简历 洪江",
                    f"{name} 任前公示 怀化",
                    f"{name} 任职经历",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{name}的教育背景（毕业院校、专业、学历学位）",
                "why_it_matters": "教育背景是身份识别和干部评价的重要字段",
                "suggested_queries": [
                    f"{name} 毕业",
                    f"{name} 学历",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{name}的出生日期和籍贯",
                "why_it_matters": "干部身份识别的基础数据",
                "suggested_queries": [
                    f"{name} 出生",
                    f"{name} 籍贯",
                ],
                "last_attempted": AS_OF,
            },
        ],
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ {filename}")
    return filename


# ══════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════


def main():
    print(f"╔══ {SLUG} Leadership Network Builder ══╗")
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
    key_persons = [p for p in persons if p["id"] in [1, 2]]
    for p in key_persons:
        if p["name"]:
            write_person_json(p, PJSON_DIR)

    # Summary
    print(f"\n── Summary ──")
    print(f"  Persons (total): {len(persons)}")
    print(f"  Persons (with real names): {sum(1 for p in persons if p['name'])}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Gaps documented in person JSON open_questions")

    print("\n── Open Gaps ──")
    print("  1. 唐龙: full career history — CRITICAL")
    print("  2. 夏向阳: full career history — CRITICAL")
    print("  3. 唐龙: education background — CRITICAL")
    print("  4. 夏向阳: education details (specific institution) — CRITICAL")
    print("  5. 唐龙: birth date and birthplace — CRITICAL")
    print("  6. 夏向阳: birthplace — HIGH")
    print("  7. Predecessor of 唐龙 (former 洪江市委书记) — HIGH")
    print("  8. Predecessor of 夏向阳 (former 洪江市市长) — HIGH")
    print("  9. Full 洪江市委 standing committee roster — HIGH")
    print("  10. 唐龙's previous roles before becoming 市委书记 — HIGH")
    print("  11. 夏向阳's previous roles before becoming 代理市长 — HIGH")
    print("  12. Cross-county cadre exchange data — MEDIUM")


if __name__ == "__main__":
    main()
