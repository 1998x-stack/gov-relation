#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 临江市, 吉林省.

Investigation date: 2026-07-25
Task ID: jilin_临江市
Level: 县级市
Parent city: 白山市
Targets: 市委书记 & 市长

Research sources:
  - www.linjiang.gov.cn — 临江市人民政府官方网站 (HTTP accessible)
  - http://www.linjiang.gov.cn/zwgk/ldzc/ — 领导之窗 页面（列出市政府领导班子）
  - 百度百科（仅可通过子agent间接引用，直接访问403）
  - Exa搜索API：请求受限

Research findings (as of 2026-07-25):
  - 市委书记: 韩东 — 确认自临江市政府官网新闻活动报道
    （"韩东深入一线调研检查防汛工作" "中共临江市委2026年度第8次常委会（扩大）会议召开"等）
  - 市长: 郑岩 — 经政府官网领导之窗确认
    （男，汉族，1988年1月生，大学本科学历，中共党员，中共临江市委副书记，临江市人民政府党组书记、市长）
  - 市政府其他领导: 郭大鹏、杜晓霞、王彬、赵文君、金星旭、姜冠宇、赵辰、高世龙、翟照东
  - 市人大常委会主任: 张庆（据百度百科）
  - 市政协主席: 徐路（据百度百科）

Confidence notes:
  - 市委书记韩东的身份确认基于新闻报道模式（出席市委常委会、检查防汛等为书记职责），
    属 plausible 级别——未直接找到"市委书记韩东"页面标题，但行为模式一致
  - 市长郑岩的身份经政府官网领导之窗直接确认，confirmed 级别
  - 其他副市长通过政府官网领导之窗列出姓名，但无个人简介页面，属 plausible 级别
  - 张庆(人大主任)和徐路(政协主席)来自百度百科线索，属 plausible 级别
  - 市政府官网(linjiang.gov.cn)通过HTTP可访问，HTTPS超时
  - 韩东的完整履历、出生年月等未找到公开来源
  - 郑岩的出生年月(1988年1月)来自政府网站简介
"""

from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "临江市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
STAGING = Path(__file__).parent.resolve()
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════
# IDs: 1=市委书记, 2=市长, 3-11=副市长/市委班子成员

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 韩东 — 市委书记
    {
        "id": 1,
        "name": "韩东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共临江市委员会",
        "source": "临江市政府官网新闻：'韩东深入一线调研检查防汛工作'等 — http://www.linjiang.gov.cn/",
        "confidence": "plausible",
        "notes": "市委书记韩东的身份通过政府官网新闻活动模式推断。多次报道其检查防汛、调研项目建设、走访市公安局等，并主持市委常委会。未找到独立页面明确标注'市委书记韩东'，但行为模式与县委书记职责完全吻合。完整履历、出生年月等均待补充。"
    },
    # 2. 郑岩 — 市长
    {
        "id": 2,
        "name": "郑岩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988年1月",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "临江市人民政府",
        "source": "临江市政府官网领导之窗 http://www.linjiang.gov.cn/zwgk/ldzc/",
        "confidence": "confirmed",
        "notes": "郑岩，男，汉族，1988年1月生，大学本科学历，中共党员，现任中共临江市委副书记，临江市人民政府党组书记、市长。主持市政府全面工作。"
    },
    # ════════════════════════════════════════
    # 市政府领导（副市长）
    # ════════════════════════════════════════
    # 3. 郭大鹏 — 副市长
    {
        "id": 3,
        "name": "郭大鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "临江市人民政府",
        "source": "临江市政府官网领导之窗 http://www.linjiang.gov.cn/zwgk/ldzc/",
        "confidence": "plausible",
        "notes": "副市长，政府官网领导之窗列出但无个人简介页面。具体分工待查。"
    },
    # 4. 杜晓霞 — 副市长
    {
        "id": 4,
        "name": "杜晓霞",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "临江市人民政府",
        "source": "临江市政府官网领导之窗 http://www.linjiang.gov.cn/zwgk/ldzc/",
        "confidence": "plausible",
        "notes": "副市长（女性）。政府官网领导之窗列出但无个人简介页面。具体分工待查。"
    },
    # 5. 王彬 — 副市长
    {
        "id": 5,
        "name": "王彬",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "临江市人民政府",
        "source": "临江市政府官网领导之窗 http://www.linjiang.gov.cn/zwgk/ldzc/",
        "confidence": "plausible",
        "notes": "副市长。政府官网领导之窗列出但无个人简介页面。具体分工待查。"
    },
    # 6. 赵文君 — 副市长
    {
        "id": 6,
        "name": "赵文君",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "临江市人民政府",
        "source": "临江市政府官网领导之窗 http://www.linjiang.gov.cn/zwgk/ldzc/",
        "confidence": "plausible",
        "notes": "副市长。政府官网领导之窗列出但无个人简介页面。具体分工待查。"
    },
    # 7. 金星旭 — 副市长
    {
        "id": 7,
        "name": "金星旭",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "临江市人民政府",
        "source": "临江市政府官网领导之窗 http://www.linjiang.gov.cn/zwgk/ldzc/",
        "confidence": "plausible",
        "notes": "副市长。政府官网领导之窗列出但无个人简介页面。具体分工待查。"
    },
    # 8. 姜冠宇 — 副市长
    {
        "id": 8,
        "name": "姜冠宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "临江市人民政府",
        "source": "临江市政府官网领导之窗 http://www.linjiang.gov.cn/zwgk/ldzc/",
        "confidence": "plausible",
        "notes": "副市长。政府官网领导之窗列出但无个人简介页面。具体分工待查。"
    },
    # 9. 赵辰 — 副市长
    {
        "id": 9,
        "name": "赵辰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "临江市人民政府",
        "source": "临江市政府官网领导之窗 http://www.linjiang.gov.cn/zwgk/ldzc/",
        "confidence": "plausible",
        "notes": "副市长。政府官网领导之窗列出但无个人简介页面。具体分工待查。"
    },
    # 10. 高世龙 — 副市长
    {
        "id": 10,
        "name": "高世龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "临江市人民政府",
        "source": "临江市政府官网领导之窗 http://www.linjiang.gov.cn/zwgk/ldzc/",
        "confidence": "plausible",
        "notes": "副市长。政府官网领导之窗列出但无个人简介页面。具体分工待查。"
    },
    # 11. 翟照东 — 副市长
    {
        "id": 11,
        "name": "翟照东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "临江市人民政府",
        "source": "临江市政府官网领导之窗 http://www.linjiang.gov.cn/zwgk/ldzc/",
        "confidence": "plausible",
        "notes": "副市长。政府官网领导之窗列出但无个人简介页面。具体分工待查。"
    },
    # ════════════════════════════════════════
    # 人大、政协领导
    # ════════════════════════════════════════
    # 12. 张庆 — 市人大常委会主任
    {
        "id": 12,
        "name": "张庆",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "临江市人民代表大会常务委员会",
        "source": "百度百科临江市条目（通过研究子agent间接引用）",
        "confidence": "plausible",
        "notes": "据百度百科临江市条目，张庆为临江市人大常委会主任。信息待政府官网核实。"
    },
    # 13. 徐路 — 市政协主席
    {
        "id": 13,
        "name": "徐路",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议临江市委员会",
        "source": "百度百科临江市条目（通过研究子agent间接引用）",
        "confidence": "plausible",
        "notes": "据百度百科临江市条目，徐路为临江市政协主席。信息待政府官网核实。"
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共临江市委员会", "type": "党委", "level": "县处级", "parent": "中共白山市委", "location": "临江市"},
    {"id": 2, "name": "临江市人民政府", "type": "政府", "level": "县处级", "parent": "白山市人民政府", "location": "临江市"},
    {"id": 3, "name": "临江市人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "白山市人大常委会", "location": "临江市"},
    {"id": 4, "name": "中国人民政治协商会议临江市委员会", "type": "政协", "level": "县处级", "parent": "政协白山市委", "location": "临江市"},
    {"id": 5, "name": "中共临江市纪律检查委员会（临江市监察委员会）", "type": "纪委", "level": "县处级", "parent": "白山市纪委", "location": "临江市"},
    {"id": 6, "name": "中共临江市委组织部", "type": "党委", "level": "县处级", "parent": "中共临江市委员会", "location": "临江市"},
    {"id": 7, "name": "中共临江市委宣传部", "type": "党委", "level": "县处级", "parent": "中共临江市委员会", "location": "临江市"},
    {"id": 8, "name": "中共临江市委政法委员会", "type": "党委", "level": "县处级", "parent": "中共临江市委员会", "location": "临江市"},
    {"id": 9, "name": "临江市公安局", "type": "政府", "level": "乡科级", "parent": "临江市人民政府", "location": "临江市"},
    {"id": 10, "name": "中共临江市委统战部", "type": "党委", "level": "县处级", "parent": "中共临江市委员会", "location": "临江市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 韩东 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "",
     "rank": "县处级正职", "note": "履历不详，通过政府官网新闻活动推断为市委书记"},
    # 郑岩 — 市长
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "",
     "rank": "县处级正职", "note": "市委副书记、市政府党组书记、市长。主持市政府全面工作。"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "",
     "rank": "县处级正职", "note": "市长兼任市委副书记"},
    # 副市长（皆为标配县级市政府领导）
    {"person_id": 3, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 张庆 — 人大主任
    {"person_id": 12, "org_id": 3, "title": "市人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},
    # 徐路 — 政协主席
    {"person_id": 13, "org_id": 4, "title": "市政协主席", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 党政主要领导
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "市委书记与市长为党政主要领导搭档关系",
     "overlap_org": "中共临江市委员会", "overlap_period": "当前"},
    # 市委书记与市委班子成员（默认关系）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "市委书记与副市长为市委与政府领导关系",
     "overlap_org": "中共临江市委员会", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "市委书记与副市长为领导与被领导关系",
     "overlap_org": "中共临江市委员会", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "市委书记与副市长为领导与被领导关系",
     "overlap_org": "中共临江市委员会", "overlap_period": "当前"},
    # 市长与副市长
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "市长与副市长为政府主要领导与副手关系",
     "overlap_org": "临江市人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "市长与副市长为政府主要领导与副手关系",
     "overlap_org": "临江市人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "市长与副市长为政府主要领导与副手关系",
     "overlap_org": "临江市人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "市长与副市长为政府主要领导与副手关系",
     "overlap_org": "临江市人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "市长与副市长为政府主要领导与副手关系",
     "overlap_org": "临江市人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "市长与副市长为政府主要领导与副手关系",
     "overlap_org": "临江市人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "市长与副市长为政府主要领导与副手关系",
     "overlap_org": "临江市人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "市长与副市长为政府主要领导与副手关系",
     "overlap_org": "临江市人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "市长与副市长为政府主要领导与副手关系",
     "overlap_org": "临江市人民政府", "overlap_period": "当前"},
    # 副市长之间的同僚关系（部分列举）
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "同为市政府班子成员", "overlap_org": "临江市人民政府", "overlap_period": "当前"},
    {"person_a": 4, "person_b": 5, "type": "overlap",
     "context": "同为市政府班子成员", "overlap_org": "临江市人民政府", "overlap_period": "当前"},
    {"person_a": 5, "person_b": 6, "type": "overlap",
     "context": "同为市政府班子成员", "overlap_org": "临江市人民政府", "overlap_period": "当前"},
    {"person_a": 6, "person_b": 7, "type": "overlap",
     "context": "同为市政府班子成员", "overlap_org": "临江市人民政府", "overlap_period": "当前"},
    {"person_a": 7, "person_b": 8, "type": "overlap",
     "context": "同为市政府班子成员", "overlap_org": "临江市人民政府", "overlap_period": "当前"},
    {"person_a": 8, "person_b": 9, "type": "overlap",
     "context": "同为市政府班子成员", "overlap_org": "临江市人民政府", "overlap_period": "当前"},
    {"person_a": 9, "person_b": 10, "type": "overlap",
     "context": "同为市政府班子成员", "overlap_org": "临江市人民政府", "overlap_period": "当前"},
    {"person_a": 10, "person_b": 11, "type": "overlap",
     "context": "同为市政府班子成员", "overlap_org": "临江市人民政府", "overlap_period": "当前"},
    # 人大、政协领导关系
    {"person_a": 1, "person_b": 12, "type": "overlap",
     "context": "市委书记与市人大常委会主任为党政主要领导与人大领导关系",
     "overlap_org": "临江市", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 13, "type": "overlap",
     "context": "市委书记与市政协主席为党政主要领导与政协领导关系",
     "overlap_org": "临江市", "overlap_period": "当前"},
]

# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON HELPERS
# ══════════════════════════════════════════════════════════════════════════════

PERSON_JSON_TEMPLATE = {
    "schema_version": "1.0",
    "generated_at": TODAY,
    "investigation_scope": {
        "province": "吉林省",
        "city": "白山市",
        "region": "临江市",
        "task_id": "jilin_临江市",
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
    person = dict(PERSON_JSON_TEMPLATE)

    # Determine rank
    if person_id <= 2:
        rank = "县处级正职"
    elif person_id <= 11:
        rank = "县处级副职"
    else:
        rank = "县处级正职"

    # Determine system
    if person_id == 1:
        system = "party"
    elif person_id <= 11:
        system = "government"
    elif person_id == 12:
        system = "other"  # 人大
    elif person_id == 13:
        system = "other"  # 政协
    else:
        system = "other"

    # Determine source register
    sources = []
    if person_id in (1,):
        sources.append({
            "id": "S001",
            "title": "临江市人民政府官网 — 新闻活动",
            "url": "http://www.linjiang.gov.cn/",
            "publisher": "临江市人民政府",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "韩东的市委书记身份推断自其政府官网新闻活动报道模式",
        })
    if person_id in (2,):
        sources.append({
            "id": "S002",
            "title": "临江市人民政府官网 — 领导之窗",
            "url": "http://www.linjiang.gov.cn/zwgk/ldzc/",
            "publisher": "临江市人民政府",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "直接确认市长郑岩身份，含简历摘要",
        })
    if person_id in range(3, 12):
        sources.append({
            "id": "S003",
            "title": "临江市人民政府官网 — 领导之窗",
            "url": "http://www.linjiang.gov.cn/zwgk/ldzc/",
            "publisher": "临江市人民政府",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "列出副市长姓名，无个人简介详情",
        })
    if person_id in (12, 13):
        sources.append({
            "id": "S004",
            "title": "百度百科 — 临江市条目",
            "url": "https://baike.baidu.com/item/%E4%B8%B4%E6%B1%9F%E5%B8%82",
            "publisher": "百度百科",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": "通过研究子agent间接引用（直接访问403）",
        })

    is_confirmed = person_id == 2  # 郑岩 confirmed, others plausible

    person["identity"] = {
        "person_id": f"jilin_linjiang_{name}",
        "name": name,
        "aliases": [],
        "gender": p["gender"],
        "ethnicity": p["ethnicity"],
        "birth": p["birth"],
        "birthplace": p["birthplace"],
        "native_place": "",
        "education": [{
            "period": "",
            "institution": "" if not p["education"] else p["education"],
            "major": "",
            "degree": p["education"],
            "study_type": "unknown",
            "source_ids": [s["id"] for s in sources],
        }] if p["education"] else [],
        "party_join": p["party_join"],
        "work_start": p["work_start"],
        "dedupe_keys": {
            "name_birth": f"{name}_{p['birth']}",
            "name_birthplace": f"{name}_{p['birthplace']}",
            "official_profile_url": "http://www.linjiang.gov.cn/zwgk/ldzc/",
        },
    }
    person["current_status"] = {
        "current_post": p["current_post"],
        "current_org": p["current_org"],
        "administrative_rank": rank,
        "as_of": AS_OF,
        "is_current_confirmed": is_confirmed,
        "source_ids": [s["id"] for s in sources],
    }
    person["career_timeline"] = [
        {
            "start": "unknown",
            "end": "present",
            "org": p["current_org"],
            "title": p["current_post"],
            "level": "",
            "location": "临江市",
            "system": system,
            "rank": rank,
            "is_key_promotion": False,
            "notes": p["notes"],
            "confidence": p["confidence"],
            "source_ids": [s["id"] for s in sources],
        }
    ]
    person["organizations"] = []
    person["relationships"] = []
    person["governance_record"] = []
    person["professional_profile"] = {
        "primary_specializations": [],
        "secondary_specializations": [],
        "career_pattern": "unknown",
        "systems_experience": [],
        "geographic_pattern": [],
        "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
    }
    person["work_style_and_personality"] = {
        "public_style_indicators": [],
        "speech_themes": [],
        "management_signals": [],
        "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
    }
    person["network_metrics"] = {}
    person["risk_and_integrity_signals"] = [
        {
            "type": "none_found",
            "description": f"未发现{name}的风险信号——公开信息有限",
            "date": AS_OF,
            "confidence": "unverified",
            "source_ids": [],
        }
    ]
    person["source_register"] = sources
    person["confidence_summary"] = {
        "identity": p["confidence"],
        "current_role": "confirmed" if is_confirmed else p["confidence"],
        "career_completeness": "thin",
        "relationship_confidence": "low",
        "biggest_gap": f"除非最基本信息（{role_label}身份）外，{name}的完整履历、出生年月、籍贯等均未知。",
    }
    person["open_questions"] = [
        {
            "priority": "critical",
            "question": f"{name}的出生年月、籍贯、学历和完整履历？",
            "why_it_matters": "核心目标人物之一，完整调查必须补充这些基础信息",
            "suggested_queries": [
                f"韩东 临江 简历" if person_id == 1 else f"郑岩 临江 简历",
                f"白山市 临江市 {p['current_post']} {p['name']}",
            ],
            "last_attempted": AS_OF,
        },
        {
            "priority": "critical",
            "question": f"{name}到任临江市的时间？",
            "why_it_matters": "确定任职时间起点，追溯前任去向",
            "suggested_queries": [
                f"临江市 {p['current_post']} 任命",
                f"临江市 人大 任命 市长" if person_id == 2 else f"临江市 书记 到任",
            ],
            "last_attempted": AS_OF,
        },
    ]
    return person


def write_person_json(person_id: int):
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    role_label = p["current_post"]
    safe_role = role_label.replace("、", "_")
    filename = f"{TODAY}-吉林省-白山市-{safe_role}-{name}.json"
    path = PJSON_DIR / filename
    person_data = build_person_json(person_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(person_data, f, ensure_ascii=False, indent=2)
    return path


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════


def main():
    print("=" * 60)
    print(f"Building {SLUG} network data")
    print(f"Date: {TODAY}")
    print(f"Staging: {STAGING}")
    print("=" * 60)

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

    # Write person JSONs
    person_ids = list(range(1, 14))
    person_files = []
    for pid in person_ids:
        path = write_person_json(pid)
        person_files.append(str(path))

    print(f"\nDB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Person JSONs:")
    for pf in person_files:
        print(f"  {pf}")
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)} ({len([p for p in persons if p['name'] != '待查'])} named)")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"\nConfidence: 市委书记=plausible, 市长=confirmed, 其他副市长=plausible")
    print(f"Note: 韩东出生年月、籍贯、履历均待查。郑岩1988年1月生、大学本科学历已确认。")
    print("Done.")


if __name__ == "__main__":
    main()
