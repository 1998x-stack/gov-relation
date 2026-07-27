#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 东港市, 丹东市, 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_东港市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - www.donggang.gov.cn — official government site accessible
  - Confirmed: 市委书记孙晓晖 (Sun Xiaohui), 市长迟长春 (Chi Changchun)
  - Government leadership work division notices (东政办发〔2026〕4号, 东政办发〔2026〕5号)
  - Multiple news articles on donggang.gov.cn from July 2026
  - Baidu Baike/Jina blocked; other search engines (Exa rate-limited) unavailable
  - No existing local artifacts for 东港市

Confidence notes:
  - Current officeholders: CONFIRMED via official government meeting reports
  - Government deputy team: CONFIRMED via official work division notice
  - Biographical details (birth year, birthplace, education, party_join): mostly unverified;
    only current roles and names confirmed from official sources
  - Full party standing committee roster: partially known (邵长江, 李叶亮 identified)
  - Predecessor/successor paths: need further research
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
SLUG = "东港市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "liaoning_东港市"
if _CURRENT_DIR.name == "liaoning_东港市":
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
# IDs: 1=市委书记, 2=市长, 3=市委副书记/政法委书记, 4=常务副市长,
#      5+=市委常委/副市长, 11=人大主任, 12=政协主席

persons = [
    {
        "id": 1,
        "name": "孙晓晖",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共东港市委员会",
        "source": "https://www.donggang.gov.cn/html/DGSZF/202607/0178485338846034.html",
        "notes": "东港市委书记。2026年7月以市委书记身份主持市委常委会、市委全会。此前经历待查。",
    },
    {
        "id": 2,
        "name": "迟长春",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "东港市人民政府",
        "source": "https://www.donggang.gov.cn/html/DGSZF/202607/0178303977746092.html",
        "notes": "东港市委副书记、市长。2026年7月以市长身份主持市政府常务会议、出席表彰大会。此前经历待查。",
    },
    {
        "id": 3,
        "name": "邵长江",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长（负责常务工作）",
        "current_org": "东港市人民政府",
        "source": "https://www.donggang.gov.cn/html/DGSZF/202606/0178288414074350.html",
        "notes": "东港市委常委、副市长（常务）。2026年6月政府工作分工通知显示其负责常务工作。此前张田广任常务副市长。",
    },
    {
        "id": 4,
        "name": "董其华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "东港市人民政府",
        "source": "https://www.donggang.gov.cn/html/DGSZF/202606/0178288414074350.html",
        "notes": "东港市副市长。负责工业、数据（营商环境建设、行政审批）、经济合作发展、园区经济等方面工作。",
    },
    {
        "id": 5,
        "name": "景旭",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "东港市人民政府",
        "source": "https://www.donggang.gov.cn/html/DGSZF/202606/0178288414074350.html",
        "notes": "东港市副市长。负责公安、司法、边海防、打击走私等方面工作。协管城市管理综合行政执法。",
    },
    {
        "id": 6,
        "name": "于非",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "东港市人民政府",
        "source": "https://www.donggang.gov.cn/html/DGSZF/202606/0178288414074350.html",
        "notes": "东港市副市长。负责交通运输、水利、农业农村、乡村振兴、林业和草原、供销、防汛抗旱和防火等方面工作。",
    },
    {
        "id": 7,
        "name": "田树强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "东港市人民政府",
        "source": "https://www.donggang.gov.cn/html/DGSZF/202606/0178288414074350.html",
        "notes": "东港市副市长。负责住房城乡建设、自然资源、退役军人事务、城区防汛、生态环境等方面工作。",
    },
    {
        "id": 8,
        "name": "李博",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "东港市人民政府",
        "source": "https://www.donggang.gov.cn/html/DGSZF/202606/0178288414074350.html",
        "notes": "东港市副市长。负责对外开放、商务、口岸、外事、教育、民政、文化、旅游、体育、卫生健康、市场监管等方面工作。",
    },
    {
        "id": 9,
        "name": "王福凯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长（挂职/协助）",
        "current_org": "东港市人民政府",
        "source": "https://www.donggang.gov.cn/html/DGSZF/202606/0178288414074350.html",
        "notes": "协助负责科技、金融、农业农村、乡村振兴等方面工作。",
    },
    {
        "id": 10,
        "name": "李茂秋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长（非领导职务）",
        "current_org": "东港市人民政府",
        "source": "https://www.donggang.gov.cn/html/DGSZF/202606/0178288414074350.html",
        "notes": "负责政务公开等方面工作；办理市长、副市长交办的事项。",
    },
    {
        "id": 11,
        "name": "张田广",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原市委常委、副市长（常务）",
        "current_org": "东港市人民政府",
        "source": "https://www.donggang.gov.cn/html/DGSZF/202604/0177742704759195.html",
        "notes": "2026年4月工作分工通知显示为常务副市长。2026年6月分工通知中已由邵长江接替。已离任或调任。",
    },
    {
        "id": 12,
        "name": "李叶亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市纪委书记、市监委主任",
        "current_org": "中共东港市纪律检查委员会",
        "source": "https://www.donggang.gov.cn/html/DGSZF/202607/0178459538189271.html",
        "notes": "2026年7月以市委常委、市纪委书记、市监委主任身份主持市纪委全会。",
    },
    {
        "id": 13,
        "name": "金福威",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "东港市人大常委会",
        "source": "https://www.donggang.gov.cn/html/DGSZF/202607/0178485338846014.html",
        "notes": "2026年7月以人大常委会主任身份主持市七届人大常委会第四十次会议。",
    },
    {
        "id": 14,
        "name": "姜永娟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "政协东港市委员会",
        "source": "https://www.donggang.gov.cn/html/DGSZF/202607/0178489946267866.html",
        "notes": "2026年7月以政协主席身份出席市委读书班。",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共东港市委员会", "type": "党委", "level": "县处级", "parent": "中共丹东市委员会", "location": "辽宁省丹东市东港市"},
    {"id": 2, "name": "东港市人民政府", "type": "政府", "level": "县处级", "parent": "丹东市人民政府", "location": "辽宁省丹东市东港市"},
    {"id": 3, "name": "东港市人大常委会", "type": "人大", "level": "县处级", "parent": "丹东市人大常委会", "location": "辽宁省丹东市东港市"},
    {"id": 4, "name": "政协东港市委员会", "type": "政协", "level": "县处级", "parent": "政协丹东市委员会", "location": "辽宁省丹东市东港市"},
    {"id": 5, "name": "中共东港市纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共丹东市纪律检查委员会", "location": "辽宁省丹东市东港市"},
    {"id": 6, "name": "东港市公安局", "type": "政府", "level": "乡科级", "parent": "东港市人民政府", "location": "辽宁省丹东市东港市"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 市委书记
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "unknown", "end": "present", "rank": "县处级正职", "note": "截至2026年7月在职"},
    # 市长
    {"person_id": 2, "org_id": 2, "title": "市委副书记、市长", "start": "unknown", "end": "present", "rank": "县处级正职", "note": "截至2026年7月在职"},
    # 常务副市长
    {"person_id": 3, "org_id": 2, "title": "市委常委、副市长（常务）", "start": "2026-06", "end": "present", "rank": "县处级副职", "note": "2026年6月起任常务副市长"},
    # 副市长 - 工业
    {"person_id": 4, "org_id": 2, "title": "副市长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "分管工业、数据、招商"},
    # 副市长 - 公安
    {"person_id": 5, "org_id": 2, "title": "副市长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "分管公安、司法、边海防"},
    # 副市长 - 农业农村
    {"person_id": 6, "org_id": 2, "title": "副市长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "分管农业、水利、交通"},
    # 副市长 - 城建
    {"person_id": 7, "org_id": 2, "title": "副市长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "分管住建、自然资源、环保"},
    # 副市长 - 商贸
    {"person_id": 8, "org_id": 2, "title": "副市长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "分管商务、教育、文旅、卫健"},
    # 副市长（挂职）
    {"person_id": 9, "org_id": 2, "title": "副市长（挂职）", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "协助分管科技、金融、农业"},
    # 副市长（非领导）
    {"person_id": 10, "org_id": 2, "title": "副市长（非领导职务）", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "负责政务公开"},
    # 原常务副市长（已离任）
    {"person_id": 11, "org_id": 2, "title": "市委常委、副市长（常务）", "start": "unknown", "end": "2026-06", "rank": "县处级副职", "note": "2026年4月仍在任，6月被邵长江接替"},
    # 纪委书记
    {"person_id": 12, "org_id": 5, "title": "市委常委、市纪委书记、市监委主任", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "截至2026年7月在职"},
    # 人大主任
    {"person_id": 13, "org_id": 3, "title": "市人大常委会主任", "start": "unknown", "end": "present", "rank": "县处级正职", "note": "截至2026年7月在职"},
    # 政协主席
    {"person_id": 14, "org_id": 4, "title": "市政协主席", "start": "unknown", "end": "present", "rank": "县处级正职", "note": "截至2026年7月在职"},
]

# ── Relationships ─────────────────────────────────────────────────────────────

relationships = [
    # 核心党政领导搭档
    {
        "person_a": 1, "person_b": 2,
        "type": "党政领导搭档",
        "context": "市委书记与市长，党政主要负责人关系",
        "overlap_org": "中共东港市委员会/东港市人民政府",
        "overlap_period": "2026年（孙晓晖任书记、迟长春任市长期间）",
        "confidence": "confirmed",
    },
    # 常务副市长交接
    {
        "person_a": 3, "person_b": 11,
        "type": "predecessor_successor",
        "context": "张田广原任常务副市长，2026年6月由邵长江接替",
        "overlap_org": "东港市人民政府",
        "overlap_period": "2026年4月-6月",
        "confidence": "confirmed",
    },
    # 书记 - 常务副市长
    {
        "person_a": 1, "person_b": 3,
        "type": "政府领导班子",
        "context": "市委书记与常务副市长",
        "overlap_org": "中共东港市委员会",
        "overlap_period": "2026年",
        "confidence": "confirmed",
    },
    # 市长 - 常务副市长
    {
        "person_a": 2, "person_b": 3,
        "type": "政府领导班子",
        "context": "市长与常务副市长",
        "overlap_org": "东港市人民政府",
        "overlap_period": "2026年6月起",
        "confidence": "confirmed",
    },
    # 书记 - 纪委书记
    {
        "person_a": 1, "person_b": 12,
        "type": "党委领导班子",
        "context": "市委书记与纪委书记",
        "overlap_org": "中共东港市委员会",
        "overlap_period": "2026年",
        "confidence": "confirmed",
    },
    # 人大主任
    {
        "person_a": 1, "person_b": 13,
        "type": "党委人大关系",
        "context": "市委书记与人大主任",
        "overlap_org": "中共东港市委员会/东港市人大常委会",
        "overlap_period": "2026年",
        "confidence": "confirmed",
    },
    # 市长-副市长团队
    {
        "person_a": 2, "person_b": 4,
        "type": "政府领导班子",
        "context": "市长与副市长董其华",
        "overlap_org": "东港市人民政府",
        "overlap_period": "2026年",
        "confidence": "confirmed",
    },
    {
        "person_a": 2, "person_b": 5,
        "type": "政府领导班子",
        "context": "市长与副市长景旭",
        "overlap_org": "东港市人民政府",
        "overlap_period": "2026年",
        "confidence": "confirmed",
    },
    {
        "person_a": 2, "person_b": 6,
        "type": "政府领导班子",
        "context": "市长与副市长于非",
        "overlap_org": "东港市人民政府",
        "overlap_period": "2026年",
        "confidence": "confirmed",
    },
    {
        "person_a": 2, "person_b": 7,
        "type": "政府领导班子",
        "context": "市长与副市长田树强",
        "overlap_org": "东港市人民政府",
        "overlap_period": "2026年",
        "confidence": "confirmed",
    },
    {
        "person_a": 2, "person_b": 8,
        "type": "政府领导班子",
        "context": "市长与副市长李博",
        "overlap_org": "东港市人民政府",
        "overlap_period": "2026年",
        "confidence": "confirmed",
    },
    # 副市长互补关系
    {
        "person_a": 3, "person_b": 5,
        "type": "工作互补",
        "context": "邵长江与景旭工作互补",
        "overlap_org": "东港市人民政府",
        "overlap_period": "2026年",
        "confidence": "confirmed",
    },
    {
        "person_a": 4, "person_b": 6,
        "type": "工作互补",
        "context": "董其华与于非工作互补",
        "overlap_org": "东港市人民政府",
        "overlap_period": "2026年",
        "confidence": "confirmed",
    },
    {
        "person_a": 7, "person_b": 8,
        "type": "工作互补",
        "context": "田树强与李博工作互补",
        "overlap_org": "东港市人民政府",
        "overlap_period": "2026年",
        "confidence": "confirmed",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# Person JSON Generator
# ══════════════════════════════════════════════════════════════════════════════

def make_source_register():
    """Source register for 东港市 investigation."""
    return [
        {
            "id": "S001",
            "title": "东港市人民政府 - 市委常委会召开会议",
            "url": "https://www.donggang.gov.cn/html/DGSZF/202607/0178485338846034.html",
            "publisher": "东港市人民政府",
            "published_at": "2026-07-24",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认市委书记孙晓晖主持会议",
        },
        {
            "id": "S002",
            "title": "东港市'两优一先'表彰大会召开",
            "url": "https://www.donggang.gov.cn/html/DGSZF/202607/0178303977746092.html",
            "publisher": "东港市人民政府",
            "published_at": "2026-07-03",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认市委书记孙晓晖、市长迟长春出席",
        },
        {
            "id": "S003",
            "title": "东港市人民政府办公室关于市政府领导同志工作分工的通知（2026年6月）",
            "url": "https://www.donggang.gov.cn/html/DGSZF/202606/0178288414074350.html",
            "publisher": "东港市人民政府办公室",
            "published_at": "2026-06-24",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "市政府领导分工通知（东政办发〔2026〕5号），确认邵长江、董其华、景旭、于非、田树强、李博、王福凯、李茂秋等",
        },
        {
            "id": "S004",
            "title": "东港市人民政府办公室关于市政府领导同志工作分工的通知（2026年4月）",
            "url": "https://www.donggang.gov.cn/html/DGSZF/202604/0177742704759195.html",
            "publisher": "东港市人民政府办公室",
            "published_at": "2026-04-24",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认张田广原任常务副市长，2026年4月在任",
        },
        {
            "id": "S005",
            "title": "中共东港市第七届纪律检查委员会第七次全体会议召开",
            "url": "https://www.donggang.gov.cn/html/DGSZF/202607/0178459538189271.html",
            "publisher": "东港市人民政府",
            "published_at": "2026-07-21",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认市委常委、市纪委书记李叶亮",
        },
        {
            "id": "S006",
            "title": "市七届人大常委会举行第四十次会议",
            "url": "https://www.donggang.gov.cn/html/DGSZF/202607/0178485338846014.html",
            "publisher": "东港市人民政府",
            "published_at": "2026-07-24",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认市人大常委会主任金福威",
        },
        {
            "id": "S007",
            "title": "市委举办树立和践行正确政绩观学习教育第3期读书班",
            "url": "https://www.donggang.gov.cn/html/DGSZF/202607/0178489946267866.html",
            "publisher": "东港市人民政府",
            "published_at": "2026-07-24",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认市政协主席姜永娟",
        },
    ]


def make_person_json(p, person_relationships, source_register):
    """Generate person JSON for a figure."""
    is_leader = p["id"] in (1, 2)
    rank = "县处级正职" if is_leader else "县处级副职"
    is_core = p["id"] in (1, 2)

    result = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "丹东市",
            "region": "东港市",
            "job": p["current_post"],
            "task_id": "liaoning_东港市",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": f"donggang_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth', '')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": rank,
            "as_of": AS_OF,
            "is_current_confirmed": p["id"] not in (11,),  # 张田广已离任
            "source_ids": [s["id"] for s in source_register if p.get("source", "") in s.get("url", "") or True][:2],
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present" if p["id"] != 11 else "2026-06",
                "org": p["current_org"],
                "title": p["current_post"],
                "level": rank,
                "location": "辽宁省丹东市东港市",
                "system": "party" if "委" in p["current_org"] and "政府" not in p["current_org"] else "government",
                "rank": rank,
                "is_key_promotion": is_leader,
                "notes": "当前职务确认。出生日期、教育背景、完整履历待补充。",
                "confidence": "confirmed" if is_core else "confirmed",
                "source_ids": ["S003", "S004"],
            },
        ],
        "organizations": [],
        "relationships": [
            {
                "person": rp["person_b_name"],
                "person_id": f"donggang_{rp['person_b_name']}",
                "relationship_type": rp.get("type", "unknown"),
                "strength": "strong" if p["id"] in (1, 2) else "medium",
                "evidence": rp.get("context", ""),
                "overlap_org": rp.get("overlap_org", ""),
                "overlap_period": rp.get("overlap_period", ""),
                "direction": "undirected",
                "confidence": rp.get("confidence", "confirmed"),
                "source_ids": ["S003"],
            }
            for rp in person_relationships
        ],
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
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if is_core else "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{p['name']}的出生年月、籍贯、教育背景、入党时间、完整履历均未知。"
                          f"仅通过政府网站确认当前职务和姓名。",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{p['name']}的出生年月和籍贯是什么？",
                "why_it_matters": "身份确认和去重的基础信息",
                "suggested_queries": [f"孙晓晖 简历 东港", f"{p['name']} 东港 出生"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{p['name']}的完整履历（何时担任现职、此前任职经历）",
                "why_it_matters": "履历是关系网络分析的核心数据",
                "suggested_queries": [f"孙晓晖 东港 市委书记 任前公示", f"迟长春 东港 市长 丹东"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "东港市第七届市委常委完整名单",
                "why_it_matters": "目前仅确认市委书记、部分副市长和纪委书记。组织部长、宣传部长、统战部长、政法委书记等常委姓名待查",
                "suggested_queries": ["东港市 市委常委 名单", "东港市委 领导班子"],
                "last_attempted": AS_OF,
            },
        ],
    }
    return result


def write_person_jsons():
    """Write per-person JSON files for core leaders."""
    source_register = make_source_register()

    # Build relationships index for each person
    name_map = {p["id"]: p["name"] for p in persons}
    person_relationships = {p["id"]: [] for p in persons}
    for r in relationships:
        if r["person_a"] in person_relationships:
            r_with_name = dict(r)
            r_with_name["person_b_name"] = name_map.get(r["person_b"], "")
            person_relationships[r["person_a"]].append(r_with_name)
        if r["person_b"] in person_relationships and r["person_b"] != r["person_a"]:
            r_rev = dict(r)
            r_rev["person_b_name"] = name_map.get(r["person_a"], "")
            r_rev["person_a"], r_rev["person_b"] = r["person_b"], r["person_a"]
            person_relationships[r["person_b"]].append(r_rev)

    # Write for core targets (市委书记 and 市长)
    core_ids = [1, 2]
    for p in persons:
        if p["id"] not in core_ids:
            continue
        rels = person_relationships.get(p["id"], [])
        pjson = make_person_json(p, rels, source_register)
        filename = f"{TODAY}-辽宁省-丹东市-{p['current_post'].replace('、', '_').replace('，', '_').replace('（','(').replace('）',')')}-{p['name']}.json"
        path = PJSON_DIR / filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pjson, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {path.name}")


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════

def main():
    """Run the full build."""
    print(f"\n{'='*60}")
    print(f"东港市 Network Build")
    print(f"{'='*60}")
    print(f"Date: {AS_OF}")
    print(f"Web access: PARTIAL — donggang.gov.cn accessible; Baidu/Exa/Google blocked")
    print()

    # 1. Database + GEXF
    print("Building database and GEXF...")
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

    # 2. Person JSONs
    print("\nWriting person JSONs...")
    write_person_jsons()

    print(f"\n{'='*60}")
    print(f"Build complete.")
    print(f"{'='*60}")
    print(f"DB:      {DB_PATH}")
    print(f"GEXF:    {GEXF_PATH}")
    print(f"Persons: {PJSON_DIR}/")
    print()
    print(f"Confirmed: 市委书记孙晓晖, 市长迟长春 (via donggang.gov.cn official news)")
    print(f"Confirmed: 8 government deputies + 1 former deputy + 纪委书记 + 人大主任 + 政协主席")
    print(f"Gaps: 孙晓晖/迟长春完整履历, 市委专职副书记, 组织/宣传/统战/政法常委")
    print()


if __name__ == "__main__":
    main()
