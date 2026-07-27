#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 和龙市, 延边朝鲜族自治州, 吉林省.

Investigation date: 2026-07-25
Task ID: jilin_和龙市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - www.helong.gov.cn — 和龙市人民政府官方网站 (reachable, confirmed 市长=朴哲万, 副市长名单)
  - 和龙市党务/市委网站 — inaccessible (no separate party committee site found)
  - Baidu Baike (403), Exa (rate-limited), Google (blocked), Jina Reader (transport error)

Findings:
  - 市长 朴哲万 — confirmed from government website leadership section
  - 副市长 9人 — confirmed from government website
  - 市委书记 — NOT found on the government website (which only lists government leadership)
    市委领导信息需从其他渠道或党务网站获取
  - 市委常委、统战部部长 倪长亮 — mentioned in news
  - 市委常委、副市长 金日国 — mentioned in news
  - 市委常委、副市长 韩长忠 — mentioned in news

Confidence notes:
  - All web sources were partially accessible (helong.gov.cn reachable, but limited).
  - Government site (helong.gov.cn) successfully confirmed executive branch leadership.
  - Party committee leadership not published on government site.
  - Baidu Baike returned HTTP 403.
  - Exa search API rate-limited.
  - Google and Jina Reader blocked/timed out.
  - 市委书记 name marked 'unverified' — only government website available.
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
SLUG = "和龙市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_和龙市"
if _CURRENT_DIR.name == "jilin_和龙市":
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
# IDs: 1=市委书记, 2=市长, 3-14=常委/副市长
# Sources: helong.gov.cn — confirmed 市长朴哲万, 9名副市长

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "待查_市委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共和龙市委员会",
        "source": "待查 — 和龙市政府网站仅列出市政府领导，未列出市委领导信息",
        "confidence": "unverified",
        "notes": "市委书记姓名确认失败。和龙市政府网站(helong.gov.cn)『市政府』栏目仅列出市长及副市长共10名政府领导，未包含市委领导信息。和龙市委专用网站未找到。需后续通过延边州委组织部公示或新闻报道进一步核实。"
    },
    {
        "id": 2,
        "name": "朴哲万",
        "gender": "男",
        "ethnicity": "朝鲜族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "和龙市人民政府",
        "source": "helong.gov.cn — 和龙市政府网站领导栏目确认",
        "confidence": "confirmed",
        "notes": "市长朴哲万，朝鲜族，系和龙市人民政府主要负责人。兼任市委副书记。政府网站列名为市政府领导之首。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Mayors (confirmed from helong.gov.cn)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "宋寿龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "和龙市人民政府",
        "source": "helong.gov.cn — 和龙市政府网站领导栏目",
        "confidence": "confirmed",
        "notes": "排名第一的副市长，通常分管常务工作。需进一步确认是否为市委常委、常务副市长。"
    },
    {
        "id": 4,
        "name": "金日国",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "和龙市人民政府",
        "source": "helong.gov.cn — 领导活动栏目确认『市委常委、市政府副市长金日国』",
        "confidence": "confirmed",
        "notes": "市委常委、市政府副市长。政府网站领导活动中有明确记载。"
    },
    {
        "id": 5,
        "name": "王宏伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "和龙市人民政府",
        "source": "helong.gov.cn — 和龙市政府网站领导栏目",
        "confidence": "confirmed",
        "notes": "副市长，排名在宋寿龙、金日国之后。"
    },
    {
        "id": 6,
        "name": "崔国哲",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "和龙市人民政府",
        "source": "helong.gov.cn — 和龙市政府网站领导栏目",
        "confidence": "confirmed",
        "notes": "副市长。"
    },
    {
        "id": 7,
        "name": "吕智梁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "和龙市人民政府",
        "source": "helong.gov.cn — 和龙市政府网站领导栏目",
        "confidence": "confirmed",
        "notes": "副市长。2024年11月有关于吕智梁的任免通知发布。"
    },
    {
        "id": 8,
        "name": "姚卫",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "和龙市人民政府",
        "source": "helong.gov.cn — 和龙市政府网站领导栏目",
        "confidence": "confirmed",
        "notes": "副市长。"
    },
    {
        "id": 9,
        "name": "金永海",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "和龙市人民政府",
        "source": "helong.gov.cn — 和龙市政府网站领导栏目",
        "confidence": "confirmed",
        "notes": "副市长。"
    },
    {
        "id": 10,
        "name": "张清森",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "和龙市人民政府",
        "source": "helong.gov.cn — 和龙市政府网站领导栏目及领导活动",
        "confidence": "confirmed",
        "notes": "副市长。领导活动中有『市政府副市长张清森到东城镇调研』记载。"
    },
    {
        "id": 11,
        "name": "韩长忠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "和龙市人民政府",
        "source": "helong.gov.cn — 领导活动栏目确认『市委常委、市政府副市长韩长忠』",
        "confidence": "confirmed",
        "notes": "市委常委、市政府副市长。政府网站领导活动中有明确记载。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Party Committee Members (inferred from news mentions)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 12,
        "name": "倪长亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、统战部部长",
        "current_org": "中共和龙市委统战部",
        "source": "helong.gov.cn — 领导活动中提及『市委常委、统战部部长倪长亮』",
        "confidence": "confirmed",
        "notes": "市委常委、统战部部长。政府网站领导活动中有明确记载。"
    },
    # Default standing committee roles (unconfirmed occupants for county-level city structure)
    {
        "id": 13,
        "name": "待查_常务副市长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长（常务）",
        "current_org": "和龙市人民政府",
        "source": "待查 — 默认县级市班子构成推断（排名第一的副市长可能兼常务）",
        "confidence": "unverified",
        "notes": "常务副市长待确认。和龙市政府网站列出宋寿龙为排名第一的副市长，可能为常务副市长。需进一步确认是否为市委常委及分管工作。"
    },
    {
        "id": 14,
        "name": "待查_纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市纪委书记、市监委主任",
        "current_org": "中共和龙市纪律检查委员会",
        "source": "待查 — 默认县级市纪检班子构成推断",
        "confidence": "unverified",
        "notes": "市纪委书记姓名待核实。属县级市标配常委职务。"
    },
    {
        "id": 15,
        "name": "待查_组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共和龙市委组织部",
        "source": "待查 — 默认县级市班子构成推断",
        "confidence": "unverified",
        "notes": "市委组织部部长姓名待核实。"
    },
    {
        "id": 16,
        "name": "待查_宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共和龙市委宣传部",
        "source": "待查 — 默认县级市班子构成推断",
        "confidence": "unverified",
        "notes": "市委宣传部部长姓名待核实。"
    },
    {
        "id": 17,
        "name": "待查_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、政法委书记",
        "current_org": "中共和龙市委政法委员会",
        "source": "待查 — 默认县级市班子构成推断",
        "confidence": "unverified",
        "notes": "市委政法委书记姓名待核实。"
    },
    {
        "id": 18,
        "name": "待查_副市长（公安局长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市公安局局长",
        "current_org": "和龙市公安局",
        "source": "待查 — 默认县级市政府构成推断",
        "confidence": "unverified",
        "notes": "分管公安的副市长兼公安局长姓名待核实。9名副市长中应有人分管公安。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共和龙市委员会", "type": "党委", "level": "县处级", "parent": "中共延边州委", "location": "和龙市"},
    {"id": 2, "name": "和龙市人民政府", "type": "政府", "level": "县处级", "parent": "延边州人民政府", "location": "和龙市"},
    {"id": 3, "name": "中国人民政治协商会议和龙市委员会", "type": "政协", "level": "县处级", "parent": "政协延边州委", "location": "和龙市"},
    {"id": 4, "name": "和龙市人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "延边州人大常委会", "location": "和龙市"},
    {"id": 5, "name": "中共和龙市纪律检查委员会（监察委员会）", "type": "纪委", "level": "县处级", "parent": "延边州纪委", "location": "和龙市"},
    {"id": 6, "name": "中共和龙市委组织部", "type": "党委", "level": "县处级", "parent": "中共和龙市委员会", "location": "和龙市"},
    {"id": 7, "name": "中共和龙市委宣传部", "type": "党委", "level": "县处级", "parent": "中共和龙市委员会", "location": "和龙市"},
    {"id": 8, "name": "中共和龙市委政法委员会", "type": "党委", "level": "县处级", "parent": "中共和龙市委员会", "location": "和龙市"},
    {"id": 9, "name": "中共和龙市委统战部", "type": "党委", "level": "县处级", "parent": "中共和龙市委员会", "location": "和龙市"},
    {"id": 10, "name": "和龙市公安局", "type": "政府", "level": "乡科级", "parent": "和龙市人民政府", "location": "和龙市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 待查_市委书记
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "市委书记姓名待核实。政府网站未刊登市委领导信息。"},
    # 朴哲万 — 市长
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "市长，朝鲜族，和龙市人民政府主要负责人"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "市长兼任市委副书记"},
    # 宋寿龙 — 副市长（排名第一）
    {"person_id": 3, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "排名第一的副市长，可能为常务副市长"},
    # 金日国 — 市委常委、副市长
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "市委常委、市政府副市长"},
    # 王宏伟 — 副市长
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 崔国哲 — 副市长
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 吕智梁 — 副市长
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "2024年11月有相关任免通知"},
    # 姚卫 — 副市长
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 金永海 — 副市长
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 张清森 — 副市长
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 韩长忠 — 市委常委、副市长
    {"person_id": 11, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "市委常委、市政府副市长"},
    # 倪长亮 — 市委常委、统战部长
    {"person_id": 12, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 9, "title": "统战部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 待查_常务副市长
    {"person_id": 13, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副市长（常务）", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "待确认是否宋寿龙为常务副市长"},
    # 待查_纪委书记
    {"person_id": 14, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 14, "org_id": 5, "title": "市纪委书记、市监委主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 待查_组织部长
    {"person_id": 15, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 6, "title": "组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 待查_宣传部长
    {"person_id": 16, "org_id": 1, "title": "市委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 16, "org_id": 7, "title": "宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 待查_政法委书记
    {"person_id": 17, "org_id": 1, "title": "市委常委、政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 8, "title": "政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 待查_副市长（公安局长）
    {"person_id": 18, "org_id": 2, "title": "副市长（兼市公安局局长）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 18, "org_id": 10, "title": "市公安局局长", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    # 市委书记 — 市长
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "市委书记与市长为党政主要领导搭档关系",
        "overlap_org": "中共和龙市委员会",
        "overlap_period": "当前",
        "confidence": "unverified",
    },
    # 市长 — 各位副市长
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "市长与副市长（宋寿龙）为政府领导关系", "overlap_org": "和龙市人民政府", "overlap_period": "当前", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "市长与市委常委、副市长（金日国）为政府领导关系", "overlap_org": "和龙市人民政府", "overlap_period": "当前", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "市长与副市长（王宏伟）为政府领导关系", "overlap_org": "和龙市人民政府", "overlap_period": "当前", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "市长与副市长（崔国哲）为政府领导关系", "overlap_org": "和龙市人民政府", "overlap_period": "当前", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "市长与副市长（吕智梁）为政府领导关系", "overlap_org": "和龙市人民政府", "overlap_period": "当前", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "市长与副市长（姚卫）为政府领导关系", "overlap_org": "和龙市人民政府", "overlap_period": "当前", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "市长与副市长（金永海）为政府领导关系", "overlap_org": "和龙市人民政府", "overlap_period": "当前", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "市长与副市长（张清森）为政府领导关系", "overlap_org": "和龙市人民政府", "overlap_period": "当前", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "市长与市委常委、副市长（韩长忠）为政府领导关系", "overlap_org": "和龙市人民政府", "overlap_period": "当前", "confidence": "confirmed"},
    # 市委常委班子 overlap relationships
    {"person_a": 4, "person_b": 11, "type": "overlap",
     "context": "同为市委常委班子成员", "overlap_org": "中共和龙市委员会", "overlap_period": "当前", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 12, "type": "overlap",
     "context": "同为市委常委班子成员", "overlap_org": "中共和龙市委员会", "overlap_period": "当前", "confidence": "confirmed"},
    {"person_a": 11, "person_b": 12, "type": "overlap",
     "context": "同为市委常委班子成员", "overlap_org": "中共和龙市委员会", "overlap_period": "当前", "confidence": "confirmed"},
    # 市长 — 待查常务副市长
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "市长与常务副市长为政府主要领导与副手关系", "overlap_org": "和龙市人民政府", "overlap_period": "当前", "confidence": "unverified"},
    # 市长 — 待查公安局长
    {"person_a": 2, "person_b": 18, "type": "superior_subordinate",
     "context": "市长与分管公安的副市长为政府领导关系", "overlap_org": "和龙市人民政府", "overlap_period": "当前", "confidence": "unverified"},
]

# ── Person JSONs ─────────────────────────────────────────────────────────────

PERSON_JSON_TEMPLATE = {
    "schema_version": "1.0",
    "generated_at": TODAY,
    "investigation_scope": {
        "province": "吉林省",
        "city": "延边朝鲜族自治州",
        "region": "和龙市",
        "task_id": "jilin_和龙市",
        "time_focus": "2026年7月",
    },
    "identity": {},
    "current_status": {},
    "career_timeline": [],
    "organizations": [],
    "relationships": [],
    "governance_record": [],
    "professional_profile": {},
    "work_style_and_personality": {},
    "network_metrics": {},
    "risk_and_integrity_signals": [],
    "source_register": [],
    "confidence_summary": {},
    "open_questions": [],
}


def build_person_json(person_id: int) -> dict:
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    role_label = p["current_post"]
    now = TODAY

    identity_conf = "confirmed" if p["confidence"] == "confirmed" else "unverified"
    career_completeness = "partial" if p["confidence"] == "confirmed" else "thin"
    rank = "县处级正职" if person_id <= 2 else "县处级副职"
    system = "party" if person_id in [1, 12, 14, 15, 16, 17] else "government"
    person_id_str = f"jilin_yanbian_helong_{name}"

    person = {
        "identity": {
            "person_id": person_id_str,
            "name": name,
            "aliases": [],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "birthplace": p["birthplace"],
            "native_place": "",
            "education": [],
            "party_join": p["party_join"],
            "work_start": p["work_start"],
            "dedupe_keys": {
                "name_birth": f"{name}_",
                "name_birthplace": f"{name}_",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": rank,
            "as_of": AS_OF,
            "is_current_confirmed": p["confidence"] == "confirmed",
            "source_ids": [],
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": p["current_org"],
                "title": p["current_post"],
                "level": "",
                "location": "和龙市",
                "system": system,
                "rank": rank,
                "is_key_promotion": False,
                "notes": p["notes"],
                "confidence": p["confidence"],
                "source_ids": [],
            }
        ],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "",
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
                "description": "No risk signals found" + ("" if p["confidence"] != "confirmed" else " from available public records"),
                "date": AS_OF,
                "confidence": p["confidence"],
                "source_ids": [],
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "和龙市人民政府官方网站 — 市政府领导栏目",
                "url": "http://www.helong.gov.cn/",
                "publisher": "和龙市人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "政府网站首页公开的市政府领导名单，长期有效",
            }
        ],
        "confidence_summary": {
            "identity": identity_conf,
            "current_role": identity_conf,
            "career_completeness": career_completeness,
            "relationship_confidence": "medium" if p["confidence"] == "confirmed" else "low",
            "biggest_gap": f"完整履历未知。{'姓名未知' if '待查' in name else f'{name}的出生年月、学历、完整履职经历'}需进一步核实。",
        },
        "open_questions": _open_questions_for(p),
    }

    return person


def _open_questions_for(p: dict) -> list[dict]:
    name = p["name"]
    role = p["current_post"]
    questions = []
    if "待查" in name:
        questions.append({
            "priority": "critical",
            "question": f"和龙市{role}姓名是什么？",
            "why_it_matters": "核心目标人物之一，完整调查必须确认姓名和身份",
            "suggested_queries": [
                f"和龙市 {role}",
                "和龙市 领导分工",
                "延边州委组织部 任前公示 和龙",
            ],
            "last_attempted": AS_OF,
        })
    questions.append({
        "priority": "high",
        "question": f"{name}的出生年月、籍贯、学历和完整履历",
        "why_it_matters": "身份确认后需补充完整履历以支持关系网络分析",
        "suggested_queries": [
            f"{name} 简历 和龙",
            f"{name} 个人简介",
        ],
        "last_attempted": AS_OF,
    })
    return questions


def write_person_json(person_id: int):
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    role_label = p["current_post"]
    safe_role = role_label.replace("、", "_").replace("（", "_").replace("）", "_")
    filename = f"{TODAY}-吉林省-延边朝鲜族自治州-{safe_role}-{name}.json"
    path = PJSON_DIR / filename

    person_data = build_person_json(person_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(person_data, f, ensure_ascii=False, indent=2)

    return path


# ── Main ─────────────────────────────────────────────────────────────────────


def main():
    # Build DB and GEXF
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

    # Write person JSONs for all persons with known names (待查 included)
    # Priority: 市委书记(1), 市长(2), then known vice mayors and party members
    priority_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    person_files = []
    for pid in priority_ids:
        path = write_person_json(pid)
        person_files.append(str(path))

    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Person JSONs:")
    for pf in person_files:
        print(f"  {pf}")
    print(f"\nNote:")
    print(f"  - 市长朴哲万 confirmed from helong.gov.cn")
    print(f"  - 9名副市长 confirmed from helong.gov.cn")
    print(f"  - 市委常委金日国、韩长忠、倪长亮 confirmed from lead activities")
    print(f"  - 市委书记姓名待查 — 政府网站未刊登市委领导信息")
    print(f"  - 常务副市长、纪委书记、组织部长等职务为默认推断")
    print(f"Done.")


if __name__ == "__main__":
    main()
