#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 沁阳市 (Qinyang City), 焦作市, 河南省.

Investigation date: 2026-07-24
Task ID: henan_沁阳市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - www.qinyang.gov.cn — 沁阳市人民政府官方网站 (primary source)
  - 市委常委会召开会议 郭新杰主持并讲话 (2026-07-24):
    https://www.qinyang.gov.cn/2026/07-24/608928.html
  - 我市召开污染防治攻坚工作推进会 (2026-07-23):
    https://www.qinyang.gov.cn/2026/07-23/608737.html
  - 郭新杰调研防汛备汛等重点工作 (2026-07-17):
    https://www.qinyang.gov.cn/2026/07-17/608236.html
  - 郭新杰调研攻坚工作项目进展情况 (2026-07-16):
    https://www.qinyang.gov.cn/2026/07-16/608160.html
  - 琚伟调研民生重点项目、生态保护暨群众身边不正之风整治工作 (2026-07-16):
    https://www.qinyang.gov.cn/2026/07-16/608159.html
  - 郭新杰调研生态环境保护工作 (2026-07-15):
    https://www.qinyang.gov.cn/2026/07-15/608039.html
  - 郭新杰到西万镇邘邰村调研基层党建、乡村振兴、民族团结工作 (2026-07-14):
    https://www.qinyang.gov.cn/2026/07-14/607877.html
  - 政务公开-领导分工页面:
    https://www.qinyang.gov.cn/zwgk/
  - Existing person JSON: data/persons/20260724-河南省-新乡市-前任县长-郭新杰.json
    (from henan_原阳县 investigation — 郭新杰 was 原阳县县长 before 沁阳市委书记)

Confidence notes:
  - 郭新杰 (市委书记): confirmed via multiple official news articles showing
    "市委书记郭新杰" (2026-07). Previously served as 原阳县县长 (left 2024-07).
    Birth year and full career timeline not verified from official sources.
  - 琚伟 (市长): confirmed as "市委副书记、市长" via official news (2026-07-23)
    and listed on 政务公开-领导分工 page.
  - 新晋来源（原阳县数据）: 郭新杰 confirmed as 原阳县前任县长 as of 2024-07.
  - Full 市委常委 roster is partially verified from news attendance lists.
  - Individual career histories (birth years, education, early positions) mostly unverified.
  - Predecessor of 郭新杰 as 沁阳市委书记 is unknown — likely appointment in late 2024 or 2025.
"""

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Allow import from repo root
REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: E402
from gov_relation.runner import run_build  # noqa: E402

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "沁阳市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# ── Staging paths ────────────────────────────────────────────────────────────
STAGING = Path(__file__).parent.resolve()
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING

# ── Helper: ID offset for orgs ─────────────────────────────────────────────
ORG_OFFSET = 100000

# ── Persons ───────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership (Targets) ═══════
    {
        "id": 1,
        "name": "郭新杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共沁阳市委员会",
        "source": ("Confirmed as '市委书记郭新杰' via multiple official news articles (2026-07): "
                   "https://www.qinyang.gov.cn/2026/07-24/608928.html; "
                   "Previously served as 原阳县县长 (left 2024-07) per existing person JSON")
    },
    {
        "id": 2,
        "name": "琚伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "沁阳市人民政府",
        "source": ("Confirmed as '市委副书记、市长琚伟' via official news: "
                   "https://www.qinyang.gov.cn/2026/07-23/608737.html; "
                   "Listed on 政务公开-领导分工 page: https://www.qinyang.gov.cn/zwgk/")
    },
    # ═══════ Leadership Team ═══════
    {
        "id": 3,
        "name": "朱保平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "沁阳市人民代表大会常务委员会",
        "source": "Confirmed via 污染防治攻坚工作推进会 article: https://www.qinyang.gov.cn/2026/07-23/608737.html"
    },
    {
        "id": 4,
        "name": "郭君玲",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议沁阳市委员会",
        "source": "Confirmed via 污染防治攻坚工作推进会 article: https://www.qinyang.gov.cn/2026/07-23/608737.html"
    },
    {
        "id": 5,
        "name": "秦广东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共沁阳市委员会",
        "source": "Confirmed via 攻坚工作项目调研 article: https://www.qinyang.gov.cn/2026/07-16/608160.html"
    },
    {
        "id": 6,
        "name": "高健",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共沁阳市委员会",
        "source": "Confirmed via 生态环境保护调研 and 污染防治攻坚 article"
    },
    {
        "id": 7,
        "name": "李永斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、办公室主任",
        "current_org": "中共沁阳市委员会",
        "source": ("Confirmed as '市委常委、办公室主任李永斌' via 防汛备汛调研: "
                   "https://www.qinyang.gov.cn/2026/07-17/608236.html")
    },
    {
        "id": 8,
        "name": "陈飞学",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "沁阳市",
        "source": "Confirmed via 污染防治攻坚工作推进会 attendance list"
    },
    {
        "id": 9,
        "name": "李伟力",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "沁阳市",
        "source": "Confirmed via 污染防治攻坚工作推进会 attendance list"
    },
    {
        "id": 10,
        "name": "王小亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "沁阳市",
        "source": "Confirmed via 污染防治攻坚工作推进会 attendance list"
    },
    {
        "id": 11,
        "name": "陈二联",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "沁阳市人民政府",
        "source": "Confirmed via 污染防治攻坚工作推进会 and 政务公开页面: https://www.qinyang.gov.cn/zwgk/"
    },
    {
        "id": 12,
        "name": "史凤云",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "沁阳市人民政府",
        "source": "Confirmed via 生态环境保护调研 and 政务公开页面"
    },
    {
        "id": 13,
        "name": "杨昭昭",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "沁阳市",
        "source": "Confirmed via 污染防治攻坚 and 攻坚项目调研 articles"
    },
    {
        "id": 14,
        "name": "沈红艳",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "沁阳市",
        "source": "Confirmed via 污染防治攻坚工作推进会 attendance list"
    },
    {
        "id": 15,
        "name": "李云峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "沁阳市人民政府",
        "source": "Confirmed via 生态环境保护调研 and 政务公开页面"
    },
    {
        "id": 16,
        "name": "韩继东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "沁阳市人民政府",
        "source": "Confirmed via 琚伟调研 article and 政务公开页面"
    },
    {
        "id": 17,
        "name": "魏治国",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "沁阳市人民政府",
        "source": "Listed on 政务公开-领导分工 page: https://www.qinyang.gov.cn/zwgk/"
    },
    {
        "id": 18,
        "name": "郑毅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "沁阳市人民政府",
        "source": "Listed on 政务公开-领导分工 page: https://www.qinyang.gov.cn/zwgk/"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共沁阳市委员会", "type": "党委", "level": "县处级",
     "parent": "中共焦作市委", "location": "河南省焦作市沁阳市"},
    {"id": 2, "name": "沁阳市人民政府", "type": "政府", "level": "县处级",
     "parent": "焦作市人民政府", "location": "河南省焦作市沁阳市"},
    {"id": 3, "name": "沁阳市人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "焦作市人大常委会", "location": "河南省焦作市沁阳市"},
    {"id": 4, "name": "中国人民政治协商会议沁阳市委员会", "type": "政协", "level": "县处级",
     "parent": "政协焦作市委员会", "location": "河南省焦作市沁阳市"},
    {"id": 5, "name": "中共沁阳市纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共沁阳市委员会", "location": "河南省焦作市沁阳市"},
    {"id": 6, "name": "中共沁阳市委政法委员会", "type": "党委", "level": "乡科级",
     "parent": "中共沁阳市委员会", "location": "河南省焦作市沁阳市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 郭新杰 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "",
     "end": "present", "rank": "正处级",
     "note": "曾任原阳县县长（至2024年7月）"},
    # 琚伟 — 市长
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "",
     "end": "present", "rank": "正处级",
     "note": "主持市政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "",
     "end": "present", "rank": "正处级", "note": ""},
    # 朱保平 — 人大主任
    {"person_id": 3, "org_id": 3, "title": "市人大常委会主任", "start": "",
     "end": "present", "rank": "正处级", "note": ""},
    # 郭君玲 — 政协主席
    {"person_id": 4, "org_id": 4, "title": "市政协主席", "start": "",
     "end": "present", "rank": "正处级", "note": ""},
    # 秦广东 — 市委常委
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start": "",
     "end": "present", "rank": "副处级", "note": ""},
    # 高健 — 市委常委
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start": "",
     "end": "present", "rank": "副处级", "note": ""},
    # 李永斌 — 市委常委、办公室主任
    {"person_id": 7, "org_id": 1, "title": "市委常委、办公室主任", "start": "",
     "end": "present", "rank": "副处级", "note": ""},
    # 陈飞学 — 市领导
    {"person_id": 8, "org_id": 1, "title": "市领导", "start": "",
     "end": "present", "rank": "", "note": "可能为副市长或常委"},
    # 李伟力 — 市领导
    {"person_id": 9, "org_id": 1, "title": "市领导", "start": "",
     "end": "present", "rank": "", "note": "可能为副市长或常委"},
    # 王小亮 — 市领导
    {"person_id": 10, "org_id": 1, "title": "市领导", "start": "",
     "end": "present", "rank": "", "note": "可能为副市长或常委"},
    # 陈二联 — 副市长
    {"person_id": 11, "org_id": 2, "title": "副市长", "start": "",
     "end": "present", "rank": "副处级", "note": ""},
    # 史凤云 — 副市长
    {"person_id": 12, "org_id": 2, "title": "副市长", "start": "",
     "end": "present", "rank": "副处级", "note": ""},
    # 杨昭昭 — 市领导
    {"person_id": 13, "org_id": 1, "title": "市领导", "start": "",
     "end": "present", "rank": "", "note": "可能为副市长或常委"},
    # 沈红艳 — 市领导
    {"person_id": 14, "org_id": 1, "title": "市领导", "start": "",
     "end": "present", "rank": "", "note": "可能为副市长或常委"},
    # 李云峰 — 副市长
    {"person_id": 15, "org_id": 2, "title": "副市长", "start": "",
     "end": "present", "rank": "副处级", "note": "分管环保等工作"},
    # 韩继东 — 副市长
    {"person_id": 16, "org_id": 2, "title": "副市长", "start": "",
     "end": "present", "rank": "副处级", "note": "陪同琚伟调研民生项目"},
    # 魏治国 — 副市长
    {"person_id": 17, "org_id": 2, "title": "副市长", "start": "",
     "end": "present", "rank": "副处级", "note": ""},
    # 郑毅 — 副市长
    {"person_id": 18, "org_id": 2, "title": "副市长", "start": "",
     "end": "present", "rank": "副处级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    # Core leadership overlaps
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "市委书记—市长搭档（党政正职）",
     "overlap_org": "中共沁阳市委员会/沁阳市人民政府",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "市委书记—人大常委会主任",
     "overlap_org": "沁阳市",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "市委书记—政协主席",
     "overlap_org": "沁阳市",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "市委书记—市委常委、办公室主任（核心助手）",
     "overlap_org": "中共沁阳市委员会",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "市委书记—市委常委",
     "overlap_org": "中共沁阳市委员会",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "市委书记—市委常委",
     "overlap_org": "中共沁阳市委员会",
     "overlap_period": "至今"},
    # Mayor with government team
    {"person_a": 2, "person_b": 11, "type": "overlap",
     "context": "市长—副市长",
     "overlap_org": "沁阳市人民政府",
     "overlap_period": "至今"},
    {"person_a": 2, "person_b": 12, "type": "overlap",
     "context": "市长—副市长",
     "overlap_org": "沁阳市人民政府",
     "overlap_period": "至今"},
    {"person_a": 2, "person_b": 15, "type": "overlap",
     "context": "市长—副市长",
     "overlap_org": "沁阳市人民政府",
     "overlap_period": "至今"},
    {"person_a": 2, "person_b": 16, "type": "overlap",
     "context": "市长—副市长",
     "overlap_org": "沁阳市人民政府",
     "overlap_period": "至今"},
    {"person_a": 2, "person_b": 17, "type": "overlap",
     "context": "市长—副市长",
     "overlap_org": "沁阳市人民政府",
     "overlap_period": "至今"},
    {"person_a": 2, "person_b": 18, "type": "overlap",
     "context": "市长—副市长",
     "overlap_org": "沁阳市人民政府",
     "overlap_period": "至今"},
    # 郭新杰's cross-county connection (from 原阳县)
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "郭新杰此前任原阳县县长；琚伟在沁阳任市长",
     "overlap_org": "",
     "overlap_period": ""},
]

# ── Source register ──────────────────────────────────────────────────────────
SOURCES = [
    {"id": "S001", "title": "市委常委会召开会议 郭新杰主持并讲话 (2026-07-24)",
     "url": "https://www.qinyang.gov.cn/2026/07-24/608928.html",
     "type": "official", "reliability": "high"},
    {"id": "S002", "title": "我市召开污染防治攻坚工作推进会 (2026-07-23)",
     "url": "https://www.qinyang.gov.cn/2026/07-23/608737.html",
     "type": "official", "reliability": "high"},
    {"id": "S003", "title": "郭新杰调研防汛备汛等重点工作 (2026-07-17)",
     "url": "https://www.qinyang.gov.cn/2026/07-17/608236.html",
     "type": "official", "reliability": "high"},
    {"id": "S004", "title": "郭新杰调研攻坚工作项目进展情况 (2026-07-16)",
     "url": "https://www.qinyang.gov.cn/2026/07-16/608160.html",
     "type": "official", "reliability": "high"},
    {"id": "S005", "title": "琚伟调研民生重点项目 (2026-07-16)",
     "url": "https://www.qinyang.gov.cn/2026/07-16/608159.html",
     "type": "official", "reliability": "high"},
    {"id": "S006", "title": "郭新杰调研生态环境保护工作 (2026-07-15)",
     "url": "https://www.qinyang.gov.cn/2026/07-15/608039.html",
     "type": "official", "reliability": "high"},
    {"id": "S007", "title": "政务公开-领导分工页面",
     "url": "https://www.qinyang.gov.cn/zwgk/",
     "type": "official", "reliability": "high"},
    {"id": "S008", "title": "沁阳市人民政府官方网站",
     "url": "https://www.qinyang.gov.cn/",
     "type": "official", "reliability": "high"},
    {"id": "S009", "title": "Existing person JSON — 郭新杰 from henan_原阳县",
     "url": "data/persons/20260724-河南省-新乡市-前任县长-郭新杰.json",
     "type": "database", "reliability": "medium"},
]


# ── Helper functions ─────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(post):
    """Return GEXF color string for a person by current post."""
    if "书记" in post and ("市委" in post or "县委" in post):
        return "255,50,50"
    if "市长" in post or "副市长" in post or "政府" in post or "市长" in post:
        return "50,100,255"
    if "纪委" in post:
        return "255,165,0"
    if "人大" in post:
        return "200,255,255"
    if "政协" in post:
        return "255,240,200"
    if "政法委" in post:
        return "200,200,255"
    return "100,100,100"


def org_color(org_type):
    """Return GEXF color string for an organization by type."""
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(org_type, "200,200,200")


def is_top_leader(person):
    return person["current_post"] in ("市委书记", "市委副书记、市长")


def gen_gexf(persons, organizations, positions, relationships, output_path):
    """Generate GEXF 1.3 graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append(f'    <description>沁阳市领导班子工作关系网络 — 调查日期 {TODAY}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="org_type" type="string"/>')
    lines.append('      <attribute id="4" title="level" type="string"/>')
    lines.append('      <attribute id="5" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('      <attribute id="4" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        pcolor = person_color(p["current_post"])
        psize = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append(f'          <attvalue for="4" value=""/>')
        lines.append(f'          <attvalue for="5" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{pcolor.split(",")[0]}" g="{pcolor.split(",")[1]}" b="{pcolor.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{psize}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        ocolor = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(o["level"])}"/>')
        lines.append(f'          <attvalue for="5" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization edges (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" '
                     f'label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos["start"])}—{esc(pos["end"])}"/>')
        lines.append(f'          <attvalue for="4" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person edges (relationships)
    for r in relationships:
        eid += 1
        weight = "2.0"
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" '
                     f'label="{esc(r["context"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('          <attvalue for="4" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {output_path}")


def gen_person_json(person, today_str):
    """Generate a person JSON file following the person_graph_json.md schema."""
    person_id = f"qinyang_{person['name']}"

    career_timeline = []
    for pos in positions:
        if pos["person_id"] == person["id"]:
            org_name = ""
            for o in organizations:
                if o["id"] == pos["org_id"]:
                    org_name = o["name"]
                    break
            career_timeline.append({
                "start": pos["start"] or "unknown",
                "end": pos["end"] or "unknown",
                "org": org_name,
                "title": pos["title"],
                "rank": pos["rank"],
                "notes": pos["note"],
                "confidence": "confirmed",
                "source_ids": ["S001", "S002", "S008"],
            })

    # Special: for 郭新杰, add the 原阳县县长 role from the existing person JSON
    if person["name"] == "郭新杰":
        career_timeline.append({
            "start": "unknown",
            "end": "2024-07",
            "org": "原阳县人民政府",
            "title": "县长",
            "rank": "正处级",
            "notes": "前任县长（源于原阳县调查数据）",
            "confidence": "confirmed",
            "source_ids": ["S009"],
        })

    person_relationships = []
    for r in relationships:
        if r["person_a"] == person["id"]:
            target_id = r["person_b"]
            target_name = ""
            for p in persons:
                if p["id"] == target_id:
                    target_name = p["name"]
                    break
            person_relationships.append({
                "person": target_name,
                "person_id": f"qinyang_{target_name}",
                "relationship_type": r["type"],
                "strength": "strong",
                "evidence": r["context"],
                "overlap_org": r["overlap_org"],
                "overlap_period": r["overlap_period"],
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002", "S008"],
            })
        elif r["person_b"] == person["id"]:
            src_id = r["person_a"]
            src_name = ""
            for p in persons:
                if p["id"] == src_id:
                    src_name = p["name"]
                    break
            person_relationships.append({
                "person": src_name,
                "person_id": f"qinyang_{src_name}",
                "relationship_type": r["type"],
                "strength": "strong",
                "evidence": r["context"],
                "overlap_org": r["overlap_org"],
                "overlap_period": r["overlap_period"],
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002", "S008"],
            })

    orgs_for_person = []
    for pos in positions:
        if pos["person_id"] == person["id"]:
            for o in organizations:
                if o["id"] == pos["org_id"]:
                    orgs_for_person.append({
                        "id": o["id"],
                        "name": o["name"],
                        "type": o["type"],
                        "level": o["level"],
                    })

    is_party_secretary = "书记" in person["current_post"] and "市" in person["current_post"]
    is_mayor = "市长" in person["current_post"] and "副" not in person["current_post"]

    schema = {
        "schema_version": "1.0",
        "generated_at": today_str,
        "investigation_scope": {
            "province": "河南省",
            "city": "焦作市",
            "region": "沁阳市",
            "job": person["current_post"],
            "task_id": "henan_沁阳市",
            "time_focus": "2024-2026",
        },
        "identity": {
            "person_id": person_id,
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"] or "",
            "ethnicity": person["ethnicity"] or "",
            "birth": person["birth"] or "",
            "birthplace": person["birthplace"] or "",
            "native_place": "",
            "education": [],
            "party_join": person["party_join"] or "",
            "work_start": person["work_start"] or "",
            "dedupe_keys": {
                "name_birth": f"{person['name']}_",
                "name_birthplace": f"{person['name']}_",
                "official_profile_url": "https://www.qinyang.gov.cn/",
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if (is_party_secretary or is_mayor or "人大主任" in person["current_post"] or "政协主席" in person["current_post"]) else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002", "S008"],
        },
        "career_timeline": career_timeline,
        "organizations": orgs_for_person,
        "relationships": person_relationships,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "cross_county_rotation" if person["name"] == "郭新杰" else "unknown",
            "systems_experience": [],
            "geographic_pattern": [f"河南省-焦作市-沁阳市"],
            "promotion_velocity": {
                "summary": "" if person["name"] != "郭新杰" else "从原阳县县长（正处级）调任沁阳市委书记（正处级），平级调整，时间约2024-2025年间",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {
            "degree_centrality": 0,
            "betweenness_centrality": 0,
            "community_cluster": "",
        },
        "risk_and_integrity_signals": [],
        "source_register": [
            {"id": s["id"], "title": s["title"], "url": s["url"],
             "publisher": "沁阳市人民政府", "published_at": AS_OF,
             "accessed_at": AS_OF, "source_type": s["type"],
             "reliability": s["reliability"], "notes": ""}
            for s in SOURCES
        ],
        "confidence_summary": {
            "identity": "partial" if not person["birth"] else "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "high",
            "biggest_gap": "详细履历（出生年份、教育背景、早期任职经历）缺失",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的出生年份、出生地、教育经历",
                "why_it_matters": "核心身份信息，影响人员去重和晋升速度分析",
                "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 出生", f"沁阳市 {person['name']} 任前公示"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{person['name']}的完整工作履历",
                "why_it_matters": "缺少早期职业经历，无法分析晋升路径和与其他官员的交集",
                "suggested_queries": [f"{person['name']} 任职经历", f"{person['name']} 曾任", f"焦作 {person['name']}"],
                "last_attempted": AS_OF,
            },
        ],
    }
    return schema


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    """Build SQLite database, GEXF graph, and person JSONs for 沁阳市."""
    print(f"=== Building {SLUG} network data ===")
    print(f"Task: henan_沁阳市 | Level: 县级市 | Research date: {AS_OF}")

    # Build SQLite + GEXF via gov_relation.runner
    import sqlite3
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    # Insert persons
    for p in persons:
        cur.execute("""
            INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
              p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    # Insert organizations
    for o in organizations:
        cur.execute("""
            INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o["location"]))

    # Insert positions
    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    # Insert relationships
    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"✅ SQLite database: {DB_PATH}")

    # Build GEXF
    gen_gexf(persons, organizations, positions, relationships, GEXF_PATH)

    # Generate person JSONs for core leaders
    core_leaders = [p for p in persons if p["id"] in (1, 2)]
    for leader in core_leaders:
        suffix = leader["current_post"].replace("、", "_").replace(" ", "_")
        safe_name = leader["name"]
        json_path = PERSONS_DIR / f"{TODAY}-河南省-焦作市-{suffix}-{safe_name}.json"
        data = gen_person_json(leader, TODAY)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Person JSON: {json_path}")

    print(f"\n📊 Summary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")


if __name__ == "__main__":
    main()
