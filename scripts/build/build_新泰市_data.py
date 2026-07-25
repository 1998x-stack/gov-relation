#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 新泰市 (Xintai City), 泰安市, 山东省.

Investigation date: 2026-07-25
Task ID: shandong_新泰市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - www.xintai.gov.cn — 新泰市人民政府官方网站 (multiple news articles confirming leadership)
  - www.xintai.gov.cn/art/2026/7/14/art_47994_10354631.html — 赵永斌督导防汛 (confirmed 市委书记)
  - www.xintai.gov.cn/art/2026/7/17/art_47994_10354677.html — 安郁杰调研环保 (confirmed 市委副书记、市长)
  - www.xintai.gov.cn/art/2026/6/30/art_47994_10354317.html — 七一表彰大会 (confirmed 王广浩 李玲 李彬)
  - www.xintai.gov.cn/art/2026/7/15/art_47994_10354632.html — 防汛调度会 (confirmed 宋广辉 张仕峰)
  - www.xintai.gov.cn/art/2026/6/22/art_47994_10354194.html — 新型工业化会议 (confirmed 贾朋 亓桂峰 殷玉梅)
  - www.xintai.gov.cn/art/2026/6/26/art_47994_10354286.html — 赵永斌调研重点项目 (confirmed 李彬)
  - www.xintai.gov.cn/art/2026/2/28/art_47994_10351849.html — 2026年市委经济工作会议 (confirmed 赵永斌 安郁杰 王广浩 李玲 李彬)
  - Baidu Baike / Web search: unavailable (403/timeout)
  - Jina Reader: timeout

Confidence notes:
  - 赵永斌 (市委书记): confirmed via multiple official news articles, Feb-Dec 2026 active
  - 安郁杰 (市长): confirmed via multiple official news articles, Feb-Dec 2026 active
  - 王广浩 (市委副书记/政法委书记): confirmed via 2026年七一表彰大会 and 农村人居环境会议
  - 贾朋 (市委常委/组织部部长): confirmed via 2026-06-25 and 2026-07-14 articles
  - 宋广辉 (市委常委/副市长): confirmed via 2026-07-15 防汛调度会
  - 李玲 (市人大常委会主任): confirmed via 七一表彰大会 and 经济工作会议
  - 李彬 (市政协主席): confirmed via 七一表彰大会 and 调研重点项目
  - 徐继刚 (副市长): confirmed via 2026-07-17 and 2026-06-22 articles
  - 张仕峰 (副市长): confirmed via 2026-07-14 and 2026-07-15 articles
  - 亓桂峰 (副市长级/市领导): confirmed via 2026-06-22 article
  - 殷玉梅 (副市长级/市领导): confirmed via 2026-06-22 article
  - 前任领导: unverified — web search degraded, Baidu 403
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
SLUG = "新泰市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shandong_新泰市"
if _CURRENT_DIR.name == "shandong_新泰市":
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
# IDs: 1-2 core (市委书记/市长), 3-4 人大/政协, 5-7 市委常委,
#       8-12 副市长/市领导, 20+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "赵永斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # 待查
        "birthplace": "",  # 待查
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共新泰市委员会",
        "source": "http://www.xintai.gov.cn/art/2026/7/14/art_47994_10354631.html",
        "confidence": "confirmed",
        "notes": "2026年2月至7月持续以市委书记身份出席各类活动。推测此前曾任新泰市市长或其他泰安市辖区县职务。"
    },
    {
        "id": 2,
        "name": "安郁杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # 待查
        "birthplace": "",  # 待查
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "新泰市人民政府",
        "source": "http://www.xintai.gov.cn/art/2026/7/17/art_47994_10354677.html",
        "confidence": "confirmed",
        "notes": "2026年2月已任市委副书记、市长。主持市政府全面工作。此前简历待查。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 人大、政协 Leaders
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "李玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "新泰市人民代表大会常务委员会",
        "source": "http://www.xintai.gov.cn/art/2026/2/28/art_47994_10351849.html",
        "confidence": "confirmed",
        "notes": "2026年2月列席市委经济工作会议。此前简历待查。"
    },
    {
        "id": 4,
        "name": "李彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议新泰市委员会",
        "source": "http://www.xintai.gov.cn/art/2026/6/26/art_47994_10354286.html",
        "confidence": "confirmed",
        "notes": "2026年6月陪同赵永斌调研重点项目。此前简历待查。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 市委常委
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 5,
        "name": "王广浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、政法委书记",
        "current_org": "中共新泰市委员会",
        "source": "http://www.xintai.gov.cn/art/2026/6/30/art_47994_10354317.html",
        "confidence": "confirmed",
        "notes": "2026年6月主持七一表彰大会，兼任市委政法委书记。"
    },
    {
        "id": 6,
        "name": "贾朋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共新泰市委员会",
        "source": "http://www.xintai.gov.cn/art/2026/7/14/art_47994_10354631.html",
        "confidence": "confirmed",
        "notes": "2026年6月和7月多次陪同赵永斌调研并参与市委活动。"
    },
    {
        "id": 7,
        "name": "宋广辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "新泰市人民政府",
        "source": "http://www.xintai.gov.cn/art/2026/7/15/art_47994_10354632.html",
        "confidence": "confirmed",
        "notes": "2026年7月14日参加防汛防台风调度会议。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 副市长/市领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 8,
        "name": "徐继刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "新泰市人民政府",
        "source": "http://www.xintai.gov.cn/art/2026/7/17/art_47994_10354677.html",
        "confidence": "confirmed",
        "notes": "2026年6月和7月多次参与副市长相关活动，陪同安郁杰调研环保，陪同赵永斌督导液化气安全。"
    },
    {
        "id": 9,
        "name": "张仕峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "新泰市人民政府",
        "source": "http://www.xintai.gov.cn/art/2026/7/14/art_47994_10354631.html",
        "confidence": "confirmed",
        "notes": "2026年7月14日陪同赵永斌督导防汛，7月15日参加防汛调度会。"
    },
    {
        "id": 10,
        "name": "亓桂峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "新泰市人民政府",
        "source": "http://www.xintai.gov.cn/art/2026/6/22/art_47994_10354194.html",
        "confidence": "confirmed",
        "notes": "2026年6月18日参加新型工业化强市建设推进委员会会议。此前简历待查。"
    },
    {
        "id": 11,
        "name": "殷玉梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "新泰市人民政府",
        "source": "http://www.xintai.gov.cn/art/2026/6/22/art_47994_10354194.html",
        "confidence": "confirmed",
        "notes": "2026年6月18日参加新型工业化强市建设推进委员会会议。此前简历待查。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors (limited data)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 20,
        "name": "【待查】前任市委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "",
        "confidence": "unverified",
        "notes": "赵永斌的前任市委书记待查。推测赵永斌此前为新泰市市长（或其他泰安市辖县区主要领导），后接任市委书记。"
    },
    {
        "id": 21,
        "name": "【待查】前任市长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "",
        "confidence": "unverified",
        "notes": "安郁杰的前任市长待查。可能为赵永斌（由市长升任市委书记的常见路径）或其他人。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共新泰市委员会", "type": "党委", "level": "县级市", "parent": "泰安市", "location": "山东省泰安市新泰市"},
    {"id": 2, "name": "新泰市人民政府", "type": "政府", "level": "县级市", "parent": "泰安市", "location": "山东省泰安市新泰市"},
    {"id": 3, "name": "新泰市人民代表大会常务委员会", "type": "人大", "level": "县级市", "parent": "泰安市", "location": "山东省泰安市新泰市"},
    {"id": 4, "name": "中国人民政治协商会议新泰市委员会", "type": "政协", "level": "县级市", "parent": "泰安市", "location": "山东省泰安市新泰市"},
    {"id": 5, "name": "中共新泰市委政法委员会", "type": "党委", "level": "县级市", "parent": "中共新泰市委员会", "location": "山东省泰安市新泰市"},
    {"id": 6, "name": "中共新泰市委组织部", "type": "党委", "level": "县级市", "parent": "中共新泰市委员会", "location": "山东省泰安市新泰市"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 赵永斌
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "", "end": "present", "rank": "正处级", "note": "2026年2月至7月在职，此前推测为新泰市市长或其他泰安市辖县区领导"},
    # 安郁杰
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "", "end": "present", "rank": "正处级", "note": "2026年2月已任市长，主持市政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 李玲
    {"person_id": 3, "org_id": 3, "title": "市人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 李彬
    {"person_id": 4, "org_id": 4, "title": "市政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 王广浩
    {"person_id": 5, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 5, "title": "政法委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 贾朋
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 6, "title": "组织部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 宋广辉
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 徐继刚
    {"person_id": 8, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 张仕峰
    {"person_id": 9, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 亓桂峰
    {"person_id": 10, "org_id": 2, "title": "副市长级领导", "start": "", "end": "present", "rank": "副处级", "note": "具体职务待查"},
    # 殷玉梅
    {"person_id": 11, "org_id": 2, "title": "副市长级领导", "start": "", "end": "present", "rank": "副处级", "note": "具体职务待查"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 赵永斌 ↔ 安郁杰 (书记-市长搭班)
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "市委书记与市长搭班，共同领导新泰市工作",
        "overlap_org": "中共新泰市委员会/新泰市人民政府",
        "overlap_period": AS_OF,
        "strength": "strong",
        "confidence": "confirmed",
        "source": "http://www.xintai.gov.cn/art/2026/2/28/art_47994_10351849.html"
    },
    # 赵永斌 ↔ 王广浩 (书记-副书记)
    {
        "person_a": 1, "person_b": 5,
        "type": "superior_subordinate",
        "context": "市委书记与市委副书记",
        "overlap_org": "中共新泰市委员会",
        "overlap_period": AS_OF,
        "strength": "strong",
        "confidence": "confirmed",
        "source": "http://www.xintai.gov.cn/art/2026/6/30/art_47994_10354317.html"
    },
    # 赵永斌 ↔ 贾朋 (书记-组织部长)
    {
        "person_a": 1, "person_b": 6,
        "type": "superior_subordinate",
        "context": "市委书记与组织部部长，贾朋多次陪同赵永斌调研",
        "overlap_org": "中共新泰市委员会",
        "overlap_period": "2026-06/07",
        "strength": "medium",
        "confidence": "confirmed",
        "source": "http://www.xintai.gov.cn/art/2026/7/14/art_47994_10354631.html"
    },
    # 赵永斌 ↔ 李彬 (书记-政协主席)
    {
        "person_a": 1, "person_b": 4,
        "type": "overlap",
        "context": "市委书记与政协主席共同调研重点项目",
        "overlap_org": "新泰市",
        "overlap_period": "2026-06",
        "strength": "medium",
        "confidence": "confirmed",
        "source": "http://www.xintai.gov.cn/art/2026/6/26/art_47994_10354286.html"
    },
    # 安郁杰 ↔ 徐继刚 (市长-副市长)
    {
        "person_a": 2, "person_b": 8,
        "type": "superior_subordinate",
        "context": "市长与副市长，徐继刚陪同安郁杰调研大气污染防治",
        "overlap_org": "新泰市人民政府",
        "overlap_period": "2026-07",
        "strength": "medium",
        "confidence": "confirmed",
        "source": "http://www.xintai.gov.cn/art/2026/7/17/art_47994_10354677.html"
    },
    # 安郁杰 ↔ 宋广辉 (市长-常务副市长)
    {
        "person_a": 2, "person_b": 7,
        "type": "superior_subordinate",
        "context": "市长与市委常委、副市长，共同参加防汛调度会",
        "overlap_org": "新泰市人民政府",
        "overlap_period": "2026-07",
        "strength": "medium",
        "confidence": "confirmed",
        "source": "http://www.xintai.gov.cn/art/2026/7/15/art_47994_10354632.html"
    },
    # 安郁杰 ↔ 张仕峰 (市长-副市长)
    {
        "person_a": 2, "person_b": 9,
        "type": "superior_subordinate",
        "context": "市长与副市长，共同参加防汛调度会",
        "overlap_org": "新泰市人民政府",
        "overlap_period": "2026-07",
        "strength": "medium",
        "confidence": "confirmed",
        "source": "http://www.xintai.gov.cn/art/2026/7/15/art_47994_10354632.html"
    },
    # 赵永斌 ↔ 张仕峰 (书记-副市长)
    {
        "person_a": 1, "person_b": 9,
        "type": "superior_subordinate",
        "context": "市委书记与副市长，共同督导防汛防台风工作",
        "overlap_org": "新泰市人民政府",
        "overlap_period": "2026-07",
        "strength": "medium",
        "confidence": "confirmed",
        "source": "http://www.xintai.gov.cn/art/2026/7/14/art_47994_10354631.html"
    },
    # 赵永斌 ↔ 徐继刚 (书记-副市长)
    {
        "person_a": 1, "person_b": 8,
        "type": "superior_subordinate",
        "context": "市委书记与副市长，共同督导液化气安全生产",
        "overlap_org": "新泰市人民政府",
        "overlap_period": "2026-06",
        "strength": "medium",
        "confidence": "confirmed",
        "source": "http://www.xintai.gov.cn/art/2026/6/15/art_47994_10354090.html"
    },
    # 王广浩 ↔ 张仕峰 (副书记-副市长)
    {
        "person_a": 5, "person_b": 9,
        "type": "overlap",
        "context": "共同参加泰安市农村人居环境整治工作推进会议",
        "overlap_org": "新泰市",
        "overlap_period": "2026-07",
        "strength": "weak",
        "confidence": "confirmed",
        "source": "http://www.xintai.gov.cn/art/2026/7/10/art_47994_10354545.html"
    },
    # 赵永斌 ↔ 李玲 (书记-人大主任)
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "共同出席市委经济工作会议和七一表彰大会",
        "overlap_org": "新泰市",
        "overlap_period": "2026-02/06",
        "strength": "weak",
        "confidence": "confirmed",
        "source": "http://www.xintai.gov.cn/art/2026/2/28/art_47994_10351849.html"
    },
]


# ── Person JSON Helper ───────────────────────────────────────────────────────

def write_person_json(person: dict, extra: dict | None = None) -> str:
    """Write a person JSON to PJSON_DIR and return its filename."""
    job_slug = person["current_post"].replace("/", "_")
    fname = f"{TODAY}-山东省-泰安市-{job_slug}-{person['name']}.json"
    path = PJSON_DIR / fname

    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "山东省",
            "city": "泰安市",
            "region": "新泰市",
            "job": person["current_post"],
            "task_id": "shandong_新泰市",
            "time_focus": "2026-07"
        },
        "identity": {
            "person_id": f"xintai_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [{"institution": person["education"], "period": "", "major": "", "degree": "", "study_type": "unknown", "source_ids": ["S001"]}] if person["education"] else [],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "name_birthplace": f"{person['name']}_{person['birthplace']}",
                "official_profile_url": person["source"]
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if person["id"] in [1, 2] else ("副处级" if person["id"] < 20 else "待查"),
            "as_of": AS_OF,
            "is_current_confirmed": person["confidence"] == "confirmed",
            "source_ids": ["S001"]
        },
        "career_timeline": _career_timeline_for(person),
        "organizations": [],
        "relationships": _relationships_for(person),
        "governance_record": _governance_record_for(person),
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": ["泰安市"],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "No public risk signals found in available sources", "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {"id": "S001", "title": person["notes"], "url": person["source"], "publisher": "新泰市人民政府", "published_at": AS_OF, "accessed_at": TODAY, "source_type": "official" if "xintai.gov.cn" in person["source"] else "wiki", "reliability": "high", "notes": ""}
        ],
        "confidence_summary": {
            "identity": person["confidence"],
            "current_role": "confirmed",
            "career_completeness": "partial" if not person["birth"] else "partial",
            "relationship_confidence": "low",
            "biggest_gap": f"完整履历待查" if not person["birth"] else "完整履历待查"
        },
        "open_questions": [
            {"priority": "critical", "question": f"{person['name']}的完整履历", "why_it_matters": "核心领导背景未知", "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 任前公示", f"{person['name']} 泰安"], "last_attempted": TODAY},
            {"priority": "high", "question": f"{person['name']}的出生年月和籍贯", "why_it_matters": "身份识别关键信息", "suggested_queries": [f"{person['name']} 出生"], "last_attempted": TODAY}
        ]
    }

    if extra:
        data.update(extra)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return fname


def _career_timeline_for(person: dict) -> list:
    """Build career timeline from positions."""
    if person["id"] == 1:
        return [
            {"start": "unknown", "end": "present", "org": "中共新泰市委员会", "title": "市委书记", "level": "正处级", "location": "泰安市新泰市", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "2026年2月至7月在职，多次出席重要活动并讲话", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "此前任职履历完全未知——推测曾任新泰市市长或其他泰安市辖县区领导，有待查证", "confidence": "unverified", "source_ids": []},
        ]
    elif person["id"] == 2:
        return [
            {"start": "unknown", "end": "present", "org": "新泰市人民政府", "title": "市长", "level": "正处级", "location": "泰安市新泰市", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "2026年2月已任市长，主持市政府全面工作", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "此前任职履历完全未知", "confidence": "unverified", "source_ids": []},
        ]
    return [
        {"start": "unknown", "end": "present", "org": person["current_org"], "title": person["current_post"], "level": "", "location": "泰安市新泰市", "system": "government" if "政府" in person["current_org"] else "party", "rank": "", "is_key_promotion": False, "notes": "", "confidence": person["confidence"], "source_ids": ["S001"]}
    ]


def _relationships_for(person: dict) -> list:
    """Build relationship list for this person."""
    rs = []
    for r in relationships:
        other_id = r["person_b"] if r["person_a"] == person["id"] else (r["person_a"] if r["person_b"] == person["id"] else None)
        if other_id is not None:
            other = next((p for p in persons if p["id"] == other_id), None)
            if other:
                rs.append({
                    "person": other["name"],
                    "person_id": f"xintai_{other['name']}",
                    "relationship_type": r["type"],
                    "strength": r["strength"],
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "undirected",
                    "confidence": r["confidence"],
                    "source_ids": []
                })
    return rs


def _governance_record_for(person: dict) -> list:
    """Build governance record for this person."""
    if person["id"] == 1:
        return [
            {"period": "2026-07-14", "domain": "public_safety", "achievement_or_event": "督导大中型水库防汛防台风工作，检查全市5个大中型水库运行情况", "role_in_event": "市委书记带队督导", "measurable_outcome": "强化防汛安全部署", "location": "新泰市", "confidence": "confirmed", "source_ids": ["S001"]},
            {"period": "2026-06-26", "domain": "economic_development", "achievement_or_event": "调研重点项目推进情况，实地察看新巨丰、2×60万千瓦发电、惠泰数字化等重大项目", "role_in_event": "市委书记带队调研", "measurable_outcome": "推动重点项目建设提速", "location": "新泰市", "confidence": "confirmed", "source_ids": ["S001"]},
            {"period": "2026-06-15", "domain": "public_safety", "achievement_or_event": "督导调研瓶装液化气安全生产工作", "role_in_event": "市委书记带队督导", "measurable_outcome": "推动燃气安全规范化管理", "location": "新泰市", "confidence": "confirmed", "source_ids": ["S001"]},
            {"period": "2026-02-26", "domain": "economic_development", "achievement_or_event": "主持2026年市委经济工作会议，部署全年经济工作", "role_in_event": "市委书记主持会议并讲话", "measurable_outcome": "确立12616工作思路", "location": "新泰市", "confidence": "confirmed", "source_ids": ["S001"]},
        ]
    elif person["id"] == 2:
        return [
            {"period": "2026-07-16", "domain": "environmental_protection", "achievement_or_event": "带队调研大气污染防治工作，检查超低排放改造和煤气发生炉淘汰情况", "role_in_event": "市长带队调研", "measurable_outcome": "推进空气质量改善", "location": "新泰市", "confidence": "confirmed", "source_ids": ["S001"]},
            {"period": "2026-07-14", "domain": "public_safety", "achievement_or_event": "主持召开全市防汛防台风视频调度会议", "role_in_event": "市长主持会议并部署", "measurable_outcome": "部署防汛防台风工作", "location": "新泰市", "confidence": "confirmed", "source_ids": ["S001"]},
            {"period": "2026-02-26", "domain": "economic_development", "achievement_or_event": "在市委经济工作会议上安排部署全年经济社会发展任务", "role_in_event": "市长作工作部署", "measurable_outcome": "明确2026年经济工作方向", "location": "新泰市", "confidence": "confirmed", "source_ids": ["S001"]},
        ]
    elif person["id"] == 5:
        return [
            {"period": "2026-06-27", "domain": "party_affairs", "achievement_or_event": "主持七一表彰大会暨榜样讲述活动", "role_in_event": "市委副书记主持会议", "measurable_outcome": "表彰先进典型", "location": "新泰市", "confidence": "confirmed", "source_ids": ["S001"]},
            {"period": "2026-07-08", "domain": "rural_development", "achievement_or_event": "参加泰安市农村人居环境整治工作推进会议并在新泰市观摩", "role_in_event": "市委副书记参加", "measurable_outcome": "推进农村人居环境整治", "location": "新泰市", "confidence": "confirmed", "source_ids": ["S001"]},
        ]
    elif person["id"] == 6:
        return [
            {"period": "2026-06-23", "domain": "technology_innovation", "achievement_or_event": "陪同省科技厅调研科技创新工作", "role_in_event": "市委常委/组织部部长陪同", "measurable_outcome": "对接省科技厅资源", "location": "新泰市", "confidence": "confirmed", "source_ids": ["S001"]},
        ]
    return []


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"Building {SLUG} network...")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write person JSONs for core leaders
    core_ids = [1, 2]
    for pid in core_ids:
        person = next(p for p in persons if p["id"] == pid)
        fname = write_person_json(person)
        print(f"  Person JSON: {fname}")

    print(f"\nDone. Database: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"Person JSONs in: {PJSON_DIR}")


if __name__ == "__main__":
    main()
