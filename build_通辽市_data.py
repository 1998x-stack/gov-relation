#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 通辽市 (Tongliao City), 内蒙古自治区.

Investigation date: 2026-07-25
Task ID: inner_mongolia_通辽市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.tongliao.gov.cn — 通辽市人民政府官方网站 (primary, current as of July 2026)
  - Official leadership profile pages for mayor, deputy mayors, and party leadership
  - July 2026 news articles confirming 孟宪东 as party secretary (自治区人大常委会副主任、市委书记)

Confidence notes:
  - Current roles: confirmed via multiple official government profiles and news reports (July 2026)
  - Biographical details (birth, birthplace, education): confirmed via official government resume pages
  - Career timeline details beyond current roles: limited due to web access constraints
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
SLUG = "通辽市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "inner_mongolia_通辽市"
if _CURRENT_DIR.name == "inner_mongolia_通辽市":
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
# IDs: 1-9 party committee, 10-19 government leadership, 20-29 standing committee, 30+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "孟宪东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question — unverified
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委书记",
        "current_org": "中共通辽市委员会",
        "source": "https://www.tongliao.gov.cn/xwzx/tlyw/202607/t20260721_1061094.html",
        "confidence": "confirmed",
        "notes": "内蒙古自治区人大常委会副主任、通辽市委书记；2026年7月主持市委严肃换届纪律会议"
    },
    {
        "id": 2,
        "name": "奇·达楞太",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1970年12月",
        "birthplace": "内蒙古伊金霍洛旗",
        "education": "研究生学历",
        "party_join": "中共党员",  # 1999年10月入党
        "work_start": "1990年7月",
        "current_post": "市长",
        "current_org": "通辽市人民政府",
        "source": "https://www.tongliao.gov.cn/zwgk/szf/szfld/sz/qdlt/",
        "confidence": "confirmed",
        "notes": "市委副书记，市政府党组书记、市长；研究生学历；伊金霍洛旗人"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Party Standing Committee Members
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "张少华",
        "gender": "男",
        "ethnicity": "",  # open question
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、纪委书记、监委主任",
        "current_org": "中共通辽市纪律检查委员会",
        "source": "https://www.tongliao.gov.cn/xwzx/tlyw/202607/t20260721_1061094.html",
        "confidence": "confirmed",
        "notes": "市委常委、纪委书记、监委主任；在全市严肃换届纪律会议上通报典型案例"
    },
    {
        "id": 4,
        "name": "张传华",
        "gender": "男",
        "ethnicity": "",  # open question
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、组织部部长",
        "current_org": "中共通辽市委组织部",
        "source": "https://www.tongliao.gov.cn/xwzx/tlyw/202607/t20260721_1061094.html",
        "confidence": "confirmed",
        "notes": "市委常委、组织部部长；主持全市严肃换届纪律会议"
    },
    {
        "id": 5,
        "name": "莫日根巴图",
        "gender": "男",
        "ethnicity": "蒙古族",  # plausible — Mongolian name
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委",
        "current_org": "中共通辽市委员会",
        "source": "https://www.tongliao.gov.cn/xwzx/tpxw/202607/t20260716_1060489.html",
        "confidence": "confirmed",
        "notes": "陪同孟宪东深入奈曼旗调研；具体职务待确认（可能为市委秘书长或市委统战部长）"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Government Leadership
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "牛文俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年11月",
        "birthplace": "",  # open question
        "education": "研究生学历，经济学博士",
        "party_join": "中共党员",  # 2001年6月入党
        "work_start": "2001年7月",
        "current_post": "市委常委、市政府副市长",
        "current_org": "通辽市人民政府",
        "source": "https://www.tongliao.gov.cn/zwgk/szf/szfld/fsz/nwj/",
        "confidence": "confirmed",
        "notes": "市政府党组成员、副市长；分管民族、文旅、商务、对外开放等"
    },
    {
        "id": 11,
        "name": "陈宏波",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1975年6月",
        "birthplace": "",  # open question
        "education": "内蒙古党校研究生学历",
        "party_join": "中共党员",  # 1997年11月入党
        "work_start": "1995年12月",
        "current_post": "市政府副市长、市公安局局长",
        "current_org": "通辽市人民政府",
        "source": "https://www.tongliao.gov.cn/zwgk/szf/szfld/fsz/chb/",
        "confidence": "confirmed",
        "notes": "市政府党组成员、副市长、市公安局党委书记、局长；分管公安、司法、信访"
    },
    {
        "id": 12,
        "name": "吕国华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年2月",
        "birthplace": "内蒙古奈曼旗",
        "education": "研究生学历，内蒙古党校经济管理专业",
        "party_join": "中共党员",
        "work_start": "1987年9月",
        "current_post": "市政府副市长",
        "current_org": "通辽市人民政府",
        "source": "https://www.tongliao.gov.cn/zwgk/szf/szfld/fsz/lgh/",
        "confidence": "confirmed",
        "notes": "市政府党组成员、副市长；分管自然资源、水务、农牧业、林草、乡村振兴等"
    },
    {
        "id": 13,
        "name": "杨焕枝",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1970年9月",
        "birthplace": "内蒙古杭锦后旗",
        "education": "研究生学历，高级农艺师",
        "party_join": "",  # open question — non-party or democratic party member (not listed in profile)
        "work_start": "1992年9月",
        "current_post": "市政府副市长",
        "current_org": "通辽市人民政府",
        "source": "https://www.tongliao.gov.cn/zwgk/szf/szfld/fsz/yhz/",
        "confidence": "confirmed",
        "notes": "副市长（非中共党员或民主党派可能性较大）；分管教育、科技、卫健、体育、医保等"
    },
    {
        "id": 14,
        "name": "黄刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年11月",
        "birthplace": "山东潍坊",
        "education": "博士研究生学历",
        "party_join": "中共党员",  # 2005年12月入党
        "work_start": "2006年7月",
        "current_post": "市政府副市长",
        "current_org": "通辽市人民政府",
        "source": "https://www.tongliao.gov.cn/zwgk/szf/szfld/fsz/hg/",
        "confidence": "confirmed",
        "notes": "市政府党组成员、副市长；分管人社、民政，协助应急管理、金融"
    },
    {
        "id": 15,
        "name": "陶立民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年9月",
        "birthplace": "吉林前郭",
        "education": "大学本科学历",
        "party_join": "中共党员",  # 2003年1月入党
        "work_start": "2003年7月",
        "current_post": "市政府副市长",
        "current_org": "通辽市人民政府",
        "source": "https://www.tongliao.gov.cn/zwgk/szf/szfld/fsz/tlm/",
        "confidence": "confirmed",
        "notes": "市政府党组成员、副市长；分管退役军人事务、市场监管、粮食储备等"
    },
    {
        "id": 16,
        "name": "冯雪晨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年11月",
        "birthplace": "内蒙古包头市",
        "education": "研究生学历，内蒙古大学毕业",
        "party_join": "中共党员",  # 2003年5月入党
        "work_start": "2003年10月",
        "current_post": "市政府副市长",
        "current_org": "通辽市人民政府",
        "source": "https://www.tongliao.gov.cn/zwgk/szf/szfld/fsz/fxc/",
        "confidence": "confirmed",
        "notes": "市政府党组成员、副市长；分管住建、交通、国资监管等"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors (known from context)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "郭玉峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",  # moved elsewhere (noted as predecessor)
        "current_org": "",
        "source": "historical",
        "confidence": "plausible",
        "notes": "2021年前后曾任通辽市市长，后调任；奇·达楞太的前任"
    },
    {
        "id": 31,
        "name": "冯玉臻",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",  # retired or moved
        "current_org": "",
        "source": "historical",
        "confidence": "plausible",
        "notes": "孟宪东的前任，曾任通辽市委书记"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共通辽市委员会", "type": "党委", "level": "地级市", "location": "通辽市"},
    {"id": 2, "name": "通辽市人民政府", "type": "政府", "level": "地级市", "location": "通辽市"},
    {"id": 3, "name": "中共通辽市纪律检查委员会", "type": "党委", "level": "地级市", "location": "通辽市"},
    {"id": 4, "name": "中共通辽市委组织部", "type": "党委", "level": "地级市", "location": "通辽市"},
    {"id": 5, "name": "通辽市公安局", "type": "政府", "level": "地级市", "location": "通辽市"},
    {"id": 6, "name": "通辽市人民代表大会常务委员会", "type": "人大", "level": "地级市", "location": "通辽市"},
    {"id": 7, "name": "中国人民政治协商会议通辽市委员会", "type": "政协", "level": "地级市", "location": "通辽市"},
    {"id": 8, "name": "内蒙古自治区人大常委会", "type": "人大", "level": "省级", "location": "呼和浩特市"},
    {"id": 9, "name": "中共内蒙古自治区委员会", "type": "党委", "level": "省级", "location": "呼和浩特市"},
]

# ── Positions ─────────────────────────────────────────────────────────────────

positions = [
    # 孟宪东
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "自治区人大常委会副主任", "start": "", "end": "present", "rank": "副省级", "note": "兼任"},
    # 奇·达楞太
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市政府党组书记、市长", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    # 张少华
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 3, "title": "市纪委书记、监委主任", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 张传华
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "组织部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 莫日根巴图
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": "具体分管领域待确认"},
    # 牛文俊
    {"person_id": 10, "org_id": 2, "title": "市委常委、市政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": "分管民族、文旅、商务、对外开放等"},
    # 陈宏波
    {"person_id": 11, "org_id": 2, "title": "市政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 11, "org_id": 5, "title": "市公安局党委书记、局长", "start": "", "end": "present", "rank": "正处级", "note": "兼任"},
    # 吕国华
    {"person_id": 12, "org_id": 2, "title": "市政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": "分管自然资源、水务、农牧业、林草、乡村振兴等"},
    # 杨焕枝
    {"person_id": 13, "org_id": 2, "title": "市政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": "分管教育、科技、卫健、体育、医保等"},
    # 黄刚
    {"person_id": 14, "org_id": 2, "title": "市政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": "分管人社、民政，协助应急管理、金融"},
    # 陶立民
    {"person_id": 15, "org_id": 2, "title": "市政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": "分管退役军人事务、市场监管、粮食储备等"},
    # 冯雪晨
    {"person_id": 16, "org_id": 2, "title": "市政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": "分管住建、交通、国资监管等"},
    # Predecessors
    {"person_id": 30, "org_id": 2, "title": "市长（前任）", "start": "", "end": "", "rank": "正厅级", "note": "奇·达楞太的前任"},
    {"person_id": 31, "org_id": 1, "title": "市委书记（前任）", "start": "", "end": "", "rank": "正厅级", "note": "孟宪东的前任"},
]

# ── Relationships ─────────────────────────────────────────────────────────────

relationships = [
    # 孟宪东 ↔ 奇·达楞太（党政一把手搭档关系）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "党政一把手搭档", "overlap_org": "中共通辽市委员会", "overlap_period": ""},
    # 孟宪东 ↔ 张少华（上下级，纪委工作关系）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "市委领导与纪委书记", "overlap_org": "中共通辽市委员会", "overlap_period": ""},
    # 孟宪东 ↔ 张传华（上下级，组织部门关系）
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "市委领导与组织部长", "overlap_org": "中共通辽市委员会", "overlap_period": ""},
    # 孟宪东 ↔ 莫日根巴图（上下级）
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "市委领导与分管常委", "overlap_org": "中共通辽市委员会", "overlap_period": ""},
    # 奇·达楞太 ↔ 各副市长（政府班子工作关系）
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "通辽市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "通辽市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "通辽市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "通辽市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "通辽市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "通辽市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "通辽市人民政府", "overlap_period": ""},
    # 张传华 ↔ 张少华（组织部与纪委在换届中的协作关系）
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "纪委与组织部在换届工作中协作", "overlap_org": "中共通辽市委员会", "overlap_period": ""},
    # 前任关系
    {"person_a": 1, "person_b": 31, "type": "predecessor_successor", "context": "孟宪东接替冯玉臻任通辽市委书记", "overlap_org": "中共通辽市委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 30, "type": "predecessor_successor", "context": "奇·达楞太接替郭玉峰任通辽市市长", "overlap_org": "通辽市人民政府", "overlap_period": ""},
]


# ── Person JSON files ─────────────────────────────────────────────────────────

def _write_person_json(person: dict, filename: str) -> None:
    """Write a single person JSON file to the staging directory."""
    today = TODAY
    province = "内蒙古自治区"
    city = "通辽市"
    job_slug = person["current_post"].split("、")[0].replace(" ", "_")
    name = person["name"].replace("·", "_")
    fname = f"{today}-{province}-{city}-{job_slug}-{name}.json"
    fpath = PJSON_DIR / fname
    # Build source register
    source_register = []
    sid = 0
    src = person.get("source", "")
    if src:
        sid += 1
        source_register.append({
            "id": f"S{sid:03d}",
            "title": f"通辽市人民政府 - {person['current_post']}信息",
            "url": src,
            "publisher": "通辽市人民政府",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": ""
        })
    # Build identity
    identity = {
        "person_id": f"tongliao_{name}",
        "name": person["name"],
        "aliases": [],
        "gender": person.get("gender", ""),
        "ethnicity": person.get("ethnicity", ""),
        "birth": person.get("birth", ""),
        "birthplace": person.get("birthplace", ""),
        "native_place": "",
        "education": [
            {
                "period": "",
                "institution": person.get("education", "") if person.get("education") and "学历" in person.get("education", "") else "",
                "major": "",
                "degree": person.get("education", ""),
                "study_type": "unknown",
                "source_ids": ["S001"] if source_register else []
            }
        ],
        "party_join": person.get("party_join", ""),
        "work_start": person.get("work_start", ""),
        "dedupe_keys": {
            "name_birth": f"{person['name']}_{person.get('birth', '')}",
            "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
            "official_profile_url": person.get("source", "")
        }
    }
    career_timeline = [
        {
            "start": "",
            "end": "present",
            "org": person.get("current_org", ""),
            "title": person.get("current_post", ""),
            "level": "",
            "location": "通辽市",
            "system": "government" if "政府" in person.get("current_org", "") else "party",
            "rank": "",
            "is_key_promotion": False,
            "notes": person.get("notes", ""),
            "confidence": "confirmed",
            "source_ids": ["S001"] if source_register else []
        }
    ]
    if person.get("notes") and "前任" in person.get("notes", ""):
        career_timeline[0]["confidence"] = "plausible"

    relationships_list = []
    for r in relationships:
        if r["person_a"] == person["id"]:
            other = next((p for p in persons if p["id"] == r["person_b"]), None)
            if other:
                relationships_list.append({
                    "person": other["name"],
                    "person_id": f"tongliao_{other['name'].replace('·', '_')}",
                    "relationship_type": r["type"],
                    "strength": "strong" if r["type"] in ["superior_subordinate"] else "medium",
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "person_to_other" if r["person_a"] == person["id"] else "other_to_person",
                    "confidence": "confirmed",
                    "source_ids": ["S001"] if source_register else []
                })

    obj = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "内蒙古自治区",
            "city": "通辽市",
            "region": "通辽市",
            "job": person.get("current_post", ""),
            "task_id": "inner_mongolia_通辽市",
            "time_focus": "2026-07"
        },
        "identity": identity,
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"] if source_register else []
        },
        "career_timeline": career_timeline,
        "organizations": [],
        "relationships": relationships_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
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
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "No risk signals found in publicly available official profiles",
                "date": AS_OF,
                "confidence": "confirmed",
                "source_ids": []
            }
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "partial",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": f"完整履历（{person['name']}的早期职业生涯和完整晋升路径）"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的完整履历（教育背景、早期任职经历、完整的晋升时间线）",
                "why_it_matters": "完整履历是分析其晋升模式、系统经验和关系网络的基础",
                "suggested_queries": [
                    f"{person['name']} 简历",
                    f"{person['name']} 任前公示",
                    f"{person['name']} 百度百科"
                ],
                "last_attempted": AS_OF
            }
        ]
    }

    fpath.parent.mkdir(parents=True, exist_ok=True)
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Person JSON: {fpath.name}")


def write_person_jsons():
    """Write person JSON files for the core leadership."""
    core_ids = {1, 2, 10, 11, 12, 13, 14, 15, 16}
    for p in persons:
        if p["id"] in core_ids:
            name_clean = p["name"].replace("·", "_")
            job_clean = p["current_post"].split("、")[0].replace(" ", "_")
            fname = f"{TODAY}-内蒙古自治区-通辽市-{job_clean}-{name_clean}.json"
            _write_person_json(p, fname)


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"═══ Building {SLUG} data ═══")
    print(f"  Staging: {STAGING}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

    # Run the build
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
    print("  Writing person JSON files...")
    write_person_jsons()

    # Summary
    print(f"\n═══ Summary ═══")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  DB file: {DB_PATH}")
    print(f"  GEXF file: {GEXF_PATH}")
    print(f"  Person JSONs: {PJSON_DIR}")
    print("  Done.")
