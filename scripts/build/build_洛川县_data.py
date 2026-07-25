#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 洛川县, 陕西省延安市.

Investigation date: 2026-07-25
Task ID: shaanxi_洛川县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - www.lcx.gov.cn — 洛川县人民政府官方网站 (primary, accessed July 2026)
  - 洛川县政府网站领导之窗 (https://www.lcx.gov.cn/zfxxgk/fdzdgknr/ldzc/)
  - 洛川县政府网站新闻中心（本地要闻栏目）
  - Wikipedia: Luochuan County (general info)

Confidence notes:
  - All 8 政府领导 (县长 + 7 副县长): confirmed via official leadership pages
  - 县委书记 张继东: confirmed via multiple news articles on lcx.gov.cn (May-July 2026)
  - 县委班子 (政法委书记 杨延宏, 宣传部长 郝煦): confirmed via news
  - 前任县长 张晶: plausible, from news records
  - 前任县委书记 王明智: plausible, inferred from public information
  - Full career histories: thin - most officials only have basic bio (birth year, education) from leadership pages
"""

from __future__ import annotations

import sqlite3  # noqa — used by gov_relation.runner via import

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

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "洛川县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shaanxi_洛川县"
if _CURRENT_DIR.name == "shaanxi_洛川县":
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
# IDs: 1-9 县委/县政府领导, 10-11 县委其他领导, 12-13 前任

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # 县委主要领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1, "name": "张继东", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委书记", "current_org": "中共洛川县委员会",
        "source": "http://www.lcx.gov.cn 新闻中心 2026年3-7月"
    },
    {
        "id": 2, "name": "薛延飞", "gender": "男", "ethnicity": "汉族",
        "birth": "1978年8月", "birthplace": "", "education": "研究生学历，法学博士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委副书记、县长", "current_org": "洛川县人民政府",
        "source": "https://www.lcx.gov.cn/zfxxgk/fdzdgknr/ldzc/xc/xyf/1.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 县政府领导班子
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3, "name": "苏凯麒", "gender": "男", "ethnicity": "汉族",
        "birth": "1990年3月", "birthplace": "", "education": "研究生学历，工学博士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、县政府党组副书记、副县长", "current_org": "洛川县人民政府",
        "source": "https://www.lcx.gov.cn/zfxxgk/fdzdgknr/ldzc/cwfxc/skq/1.html"
    },
    {
        "id": 4, "name": "刘建锋", "gender": "男", "ethnicity": "汉族",
        "birth": "1974年11月", "birthplace": "", "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、副县长", "current_org": "洛川县人民政府",
        "source": "https://www.lcx.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/ljf/1.html"
    },
    {
        "id": 5, "name": "鲁强", "gender": "男", "ethnicity": "汉族",
        "birth": "1980年9月", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长、县公安局局长", "current_org": "洛川县人民政府",
        "source": "https://www.lcx.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/lq/1.html"
    },
    {
        "id": 6, "name": "杜耀华", "gender": "男", "ethnicity": "汉族",
        "birth": "1984年10月", "birthplace": "", "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长", "current_org": "洛川县人民政府",
        "source": "https://www.lcx.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/dyh/1.html"
    },
    {
        "id": 7, "name": "韩东辉", "gender": "男", "ethnicity": "汉族",
        "birth": "1975年6月", "birthplace": "", "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长", "current_org": "洛川县人民政府",
        "source": "https://www.lcx.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/hdh/1.html"
    },
    {
        "id": 8, "name": "张春红", "gender": "女", "ethnicity": "汉族",
        "birth": "1981年6月", "birthplace": "", "education": "本科学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长", "current_org": "洛川县人民政府",
        "source": "https://www.lcx.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/zch/1.html"
    },
    {
        "id": 9, "name": "张龙", "gender": "男", "ethnicity": "汉族",
        "birth": "1988年3月", "birthplace": "", "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长（挂职）", "current_org": "洛川县人民政府",
        "source": "https://www.lcx.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/zl/1.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 县委其他领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 10, "name": "杨延宏", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、政法委书记", "current_org": "中共洛川县委员会",
        "source": "http://www.lcx.gov.cn 新闻中心 2026年7月"
    },
    {
        "id": 11, "name": "郝煦", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、宣传部部长", "current_org": "中共洛川县委员会",
        "source": "http://www.lcx.gov.cn 新闻中心 2026年7月"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 前任
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 12, "name": "张晶", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任县长", "current_org": "洛川县人民政府",
        "source": "http://www.lcx.gov.cn 新闻中心 — 2025年3月以县长身份调研"
    },
    {
        "id": 13, "name": "王明智", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任县委书记", "current_org": "中共洛川县委员会",
        "source": "推测 — 曾任洛川县委书记，后升任延安市副市长"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共洛川县委员会", "type": "党委", "level": "县级", "parent": "中共延安市委", "location": "洛川县"},
    {"id": 2, "name": "洛川县人民政府", "type": "政府", "level": "县级", "parent": "延安市人民政府", "location": "洛川县"},
    {"id": 3, "name": "中共洛川县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共洛川县委员会", "location": "洛川县"},
    {"id": 4, "name": "洛川县监察委员会", "type": "党委", "level": "县级", "parent": "中共洛川县委员会", "location": "洛川县"},
    {"id": 5, "name": "中共洛川县委政法委员会", "type": "党委", "level": "县级", "parent": "中共洛川县委员会", "location": "洛川县"},
    {"id": 6, "name": "中共洛川县委宣传部", "type": "党委", "level": "县级", "parent": "中共洛川县委员会", "location": "洛川县"},
    {"id": 7, "name": "洛川县公安局", "type": "政府", "level": "科级", "parent": "洛川县人民政府", "location": "洛川县"},
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    # 张继东
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "",
     "rank": "正处级", "note": "2026年7月仍任，负责县委全面工作"},
    # 薛延飞
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "",
     "rank": "正处级", "note": "主持县政府全面工作；分管财政局、审计局"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "",
     "rank": "正处级", "note": "县长兼任县委副书记"},
    # 苏凯麒
    {"person_id": 3, "org_id": 2, "title": "县政府党组副书记、副县长", "start": "", "end": "",
     "rank": "副处级", "note": "县政府二把手；1990年生/工学博士"},
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start": "", "end": "",
     "rank": "副处级", "note": "县委常委会成员"},
    # 刘建锋
    {"person_id": 4, "org_id": 2, "title": "副县长", "start": "", "end": "",
     "rank": "副处级", "note": "曾任乡镇党委书记、统战部部长等"},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "",
     "rank": "副处级", "note": "县委常委会成员"},
    # 鲁强
    {"person_id": 5, "org_id": 2, "title": "副县长", "start": "", "end": "",
     "rank": "副处级", "note": "兼任县公安局局长；曾任黄龙县副县长/公安局长"},
    {"person_id": 5, "org_id": 7, "title": "县公安局局长", "start": "", "end": "",
     "rank": "正科级", "note": "兼任县公安局局长"},
    # 杜耀华
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "", "end": "",
     "rank": "副处级", "note": "曾任市政府部门副县级正职"},
    # 韩东辉
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "", "end": "",
     "rank": "副处级", "note": "曾任洛川县苹果产业管理局局长（本地晋升）；2026年4月陪同县委书记检查农业农村和苹果产业"},
    # 张春红(女)
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "", "end": "",
     "rank": "副处级", "note": "曾任延安市委宣传部新闻科科长"},
    # 张龙(挂职)
    {"person_id": 9, "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "",
     "rank": "副处级", "note": "省委组织部选派挂职；曾任秦农银行系统"},
    # 杨延宏
    {"person_id": 10, "org_id": 5, "title": "政法委书记", "start": "", "end": "",
     "rank": "副处级", "note": "县委常委、政法委书记；2026年7月3日出席活动"},
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "", "end": "",
     "rank": "副处级", "note": "县委常委会成员"},
    # 郝煦
    {"person_id": 11, "org_id": 6, "title": "宣传部部长", "start": "", "end": "",
     "rank": "副处级", "note": "县委常委、宣传部部长；2026年7月3日出席活动"},
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start": "", "end": "",
     "rank": "副处级", "note": "县委常委会成员"},
    # 张晶 (前任县长)
    {"person_id": 12, "org_id": 2, "title": "县长", "start": "", "end": "约2025年",
     "rank": "正处级", "note": "前任县长；2025年3月仍以县长身份调研；薛延飞接任"},
    # 王明智 (前任县委书记)
    {"person_id": 13, "org_id": 1, "title": "县委书记", "start": "", "end": "",
     "rank": "正处级", "note": "前任县委书记；推测后升任延安市副市长"},
]

# ── Relationships ──────────────────────────────────────────────────────────────
relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记与县长，县委与县政府一把手", "overlap_org": "洛川县", "overlap_period": ""},
    # 县委书记 x 县委常委/副县长
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记与县委常委/县政府党组副书记", "overlap_org": "中共洛川县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记与县委常委/副县长", "overlap_org": "中共洛川县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县委书记与副县长韩东辉，共同检查农业农村和苹果产业项目", "overlap_org": "洛川县人民政府", "overlap_period": "2026年4月"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "县委书记与政法委书记", "overlap_org": "中共洛川县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "县委书记与宣传部长", "overlap_org": "中共洛川县委", "overlap_period": ""},
    # 县长 x 副县长
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "县长与县政府党组副书记（副县长/常务）", "overlap_org": "洛川县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "县长与副县长", "overlap_org": "洛川县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "县长与副县长/公安局长", "overlap_org": "洛川县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "县长与副县长", "overlap_org": "洛川县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "县长与副县长", "overlap_org": "洛川县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "县长与副县长", "overlap_org": "洛川县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "县长与挂职副县长", "overlap_org": "洛川县人民政府", "overlap_period": ""},
    # 前任与现任
    {"person_a": 12, "person_b": 2, "type": "predecessor_successor", "context": "张晶为前任县长，薛延飞接任", "overlap_org": "洛川县人民政府", "overlap_period": "约2025年"},
    {"person_a": 13, "person_b": 1, "type": "predecessor_successor", "context": "王明智为前任县委书记，张继东接任（推测）", "overlap_org": "中共洛川县委", "overlap_period": ""},
]


# ══════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════

def make_source_register():
    return [
        {"id": "S001", "title": "洛川县人民政府网站", "url": "http://www.lcx.gov.cn/", "publisher": "洛川县人民政府", "published_at": "2026-07-25", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "洛川县人民政府官方网站"},
        {"id": "S002", "title": "洛川县政府领导之窗 — 薛延飞", "url": "https://www.lcx.gov.cn/zfxxgk/fdzdgknr/ldzc/xc/xyf/1.html", "publisher": "洛川县人民政府", "published_at": "2025-07-10", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "薛延飞：县长，1978年8月生，法学博士"},
        {"id": "S003", "title": "洛川县政府领导之窗 — 苏凯麒", "url": "https://www.lcx.gov.cn/zfxxgk/fdzdgknr/ldzc/cwfxc/skq/1.html", "publisher": "洛川县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "苏凯麒：县委常委/党组副书记/副县长，1990年3月生，工学博士"},
        {"id": "S004", "title": "洛川县政府领导之窗 — 刘建锋", "url": "https://www.lcx.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/ljf/1.html", "publisher": "洛川县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "刘建锋：县委常委/副县长，1974年11月生"},
        {"id": "S005", "title": "洛川县政府领导之窗 — 鲁强", "url": "https://www.lcx.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/lq/1.html", "publisher": "洛川县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "鲁强：副县长/公安局长，1980年9月生"},
        {"id": "S006", "title": "洛川县政府领导之窗 — 杜耀华", "url": "https://www.lcx.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/dyh/1.html", "publisher": "洛川县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "杜耀华：副县长，1984年10月生"},
        {"id": "S007", "title": "洛川县政府领导之窗 — 韩东辉", "url": "https://www.lcx.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/hdh/1.html", "publisher": "洛川县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "韩东辉：副县长，1975年6月生"},
        {"id": "S008", "title": "洛川县政府领导之窗 — 张春红", "url": "https://www.lcx.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/zch/1.html", "publisher": "洛川县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "张春红：副县长（女），1981年6月生"},
        {"id": "S009", "title": "洛川县政府领导之窗 — 张龙", "url": "https://www.lcx.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/zl/1.html", "publisher": "洛川县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "张龙：副县长（挂职），1988年3月生"},
        {"id": "S010", "title": "张继东检查五一假期全县安全生产、社会治安等重点工作", "url": "http://www.lcx.gov.cn/xwzx/", "publisher": "融媒体", "published_at": "2026-05-04", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认张继东以洛川县委书记身份工作"},
        {"id": "S011", "title": "张继东检查春季农业农村工作", "url": "http://www.lcx.gov.cn/xwzx/", "publisher": "融媒体", "published_at": "2026-04-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "张继东、韩东辉共同检查"},
        {"id": "S012", "title": "洛川县人大常委会/县委会议新闻", "url": "http://www.lcx.gov.cn/xwzx/", "publisher": "融媒体", "published_at": "2026-07", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "杨延宏(政法委书记)、郝煦(宣传部长)确认"},
    ]


def make_person_json(person, timeline, relationships_list, source_register, gaps=None):
    """Build a person graph JSON following the schema."""
    pfname = f"luochuan_{person['name']}"
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "陕西省",
            "city": "延安市",
            "region": "洛川县",
            "job": person["current_post"],
            "task_id": "shaanxi_洛川县",
            "time_focus": "2025-2026"
        },
        "identity": {
            "person_id": pfname,
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": person["education"], "study_type": "unknown", "source_ids": []}] if person["education"] else [],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}" if person["birth"] else person["name"],
                "name_birthplace": f"{person['name']}_{person['birthplace']}" if person["birthplace"] else person["name"],
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if ("书记" in person["current_post"] and "副" not in person["current_post"]) or person["current_post"] == "县委副书记、县长" or person["current_post"] in ["前任县长", "前任县委书记"] else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": []
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": relationships_list,
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
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现负面公开记录", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{person['name']}的完整早期履历不明确"
        },
        "open_questions": (gaps if gaps else [
            {"priority": "high", "question": f"{person['name']}的完整职业履历是什么？", "why_it_matters": "无法分析晋升路径和跨部门经验", "suggested_queries": [f"{person['name']} 简历 洛川"], "last_attempted": AS_OF},
        ])
    }


# ══════════════════════════════════════════════════════════════════════════
# Build Function
# ══════════════════════════════════════════════════════════════════════════

def build():
    print("=" * 60)
    print("  洛川县领导班子工作关系网络")
    print("  等级: 县")
    print(f"  调查日期: {AS_OF}")
    print("  信息来源: 洛川县人民政府网站")
    print("=" * 60)

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print(f"\n  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── Generate Person Graph JSONs ──
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()

    # 1. 张继东 (县委书记)
    zhang_timeline = [
        {"start": "", "end": "", "org": "中共洛川县委员会", "title": "县委书记", "notes": "2026年3-7月期间频繁调研苹果产业、安全生产、网络意识形态、森林防火等工作", "confidence": "confirmed", "source_ids": ["S010", "S011"]},
    ]
    zhang_relationships = [
        {"person": "薛延飞", "person_id": "luochuan_薛延飞", "relationship_type": "overlap", "strength": "strong", "evidence": "县委书记与县长，党政一把手搭档", "overlap_org": "洛川县", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "苏凯麒", "person_id": "luochuan_苏凯麒", "relationship_type": "overlap", "strength": "strong", "evidence": "县委书记与县委常委", "overlap_org": "中共洛川县委", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "刘建锋", "person_id": "luochuan_刘建锋", "relationship_type": "overlap", "strength": "strong", "evidence": "县委书记与县委常委", "overlap_org": "中共洛川县委", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "韩东辉", "person_id": "luochuan_韩东辉", "relationship_type": "overlap", "strength": "strong", "evidence": "共同检查农业农村和苹果产业工作", "overlap_org": "洛川县人民政府", "overlap_period": "2026年4月", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S011"]},
        {"person": "杨延宏", "person_id": "luochuan_杨延宏", "relationship_type": "overlap", "strength": "strong", "evidence": "县委书记与政法委书记", "overlap_org": "中共洛川县委", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S012"]},
        {"person": "郝煦", "person_id": "luochuan_郝煦", "relationship_type": "overlap", "strength": "strong", "evidence": "县委书记与宣传部长", "overlap_org": "中共洛川县委", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S012"]},
    ]
    zhang_gaps = [
        {"priority": "critical", "question": "张继东的出生年份和籍贯是？", "why_it_matters": "核心人物身份信息缺失", "suggested_queries": ["张继东 洛川 简历 出生"], "last_attempted": AS_OF},
        {"priority": "critical", "question": "张继东的完整职业履历是什么？", "why_it_matters": "无法分析晋升路径", "suggested_queries": ["张继东 任前公示", "张继东 历任 职务"], "last_attempted": AS_OF},
        {"priority": "high", "question": "张继东的前任县委书记是谁？", "why_it_matters": "了解交接背景", "suggested_queries": ["洛川县 前任 县委书记 调任"], "last_attempted": AS_OF},
    ]
    zhang_json = make_person_json(persons[0], zhang_timeline, zhang_relationships, source_register, zhang_gaps)
    zhang_path = PJSON_DIR / f"{TODAY}-陕西省-延安市-县委书记-张继东.json"
    with open(zhang_path, "w", encoding="utf-8") as f:
        json.dump(zhang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {zhang_path.name}")

    # 2. 薛延飞 (县长)
    xue_timeline = [
        {"start": "", "end": "", "org": "洛川县人民政府", "title": "县委副书记、县长", "notes": "主持县政府全面工作；分管财政局、审计局", "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    xue_relationships = [
        {"person": "张继东", "person_id": "luochuan_张继东", "relationship_type": "overlap", "strength": "strong", "evidence": "县长与县委书记，党政搭档", "overlap_org": "洛川县", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "苏凯麒", "person_id": "luochuan_苏凯麒", "relationship_type": "overlap", "strength": "strong", "evidence": "县长与县政府党组副书记（常务副）", "overlap_org": "洛川县人民政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "刘建锋", "person_id": "luochuan_刘建锋", "relationship_type": "overlap", "strength": "strong", "evidence": "县长与副县长", "overlap_org": "洛川县人民政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "韩东辉", "person_id": "luochuan_韩东辉", "relationship_type": "overlap", "strength": "medium", "evidence": "县长与副县长", "overlap_org": "洛川县人民政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "张晶", "person_id": "luochuan_张晶", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "薛延飞接替张晶任县长", "overlap_org": "洛川县人民政府", "overlap_period": "约2025年", "direction": "other_to_person", "confidence": "plausible", "source_ids": []},
    ]
    xue_gaps = [
        {"priority": "high", "question": "薛延飞的籍贯和完整职业履历？", "why_it_matters": "了解晋升路径", "suggested_queries": ["薛延飞 简历 洛川", "薛延飞 任前公示"], "last_attempted": AS_OF},
        {"priority": "high", "question": "薛延飞任县长前的职务是什么？", "why_it_matters": "了解来洛川前的经历", "suggested_queries": ["薛延飞 此前 担任", "薛延飞 调任 洛川"], "last_attempted": AS_OF},
    ]
    xue_json = make_person_json(persons[1], xue_timeline, xue_relationships, source_register, xue_gaps)
    xue_path = PJSON_DIR / f"{TODAY}-陕西省-延安市-县长-薛延飞.json"
    with open(xue_path, "w", encoding="utf-8") as f:
        json.dump(xue_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {xue_path.name}")

    # 3. 苏凯麒 (常务副县长)
    su_timeline = [
        {"start": "", "end": "", "org": "洛川县人民政府", "title": "县委常委、县政府党组副书记、副县长", "notes": "县政府二把手；1990年3月生/工学博士", "confidence": "confirmed", "source_ids": ["S003"]},
    ]
    su_relationships = [
        {"person": "张继东", "person_id": "luochuan_张继东", "relationship_type": "overlap", "strength": "strong", "evidence": "县委常委与县委书记", "overlap_org": "中共洛川县委", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
        {"person": "薛延飞", "person_id": "luochuan_薛延飞", "relationship_type": "overlap", "strength": "strong", "evidence": "县政府党组副书记与县长", "overlap_org": "洛川县人民政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
    ]
    su_gaps = [
        {"priority": "high", "question": "苏凯麒的籍贯和博士院校专业？", "why_it_matters": "了解其技术背景和培养路径", "suggested_queries": ["苏凯麒 工学博士 院校", "苏凯麒 洛川 简历"], "last_attempted": AS_OF},
    ]
    su_json = make_person_json(persons[2], su_timeline, su_relationships, source_register, su_gaps)
    su_path = PJSON_DIR / f"{TODAY}-陕西省-延安市-常务副县长-苏凯麒.json"
    with open(su_path, "w", encoding="utf-8") as f:
        json.dump(su_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {su_path.name}")

    print(f"\n所有 Person Graph JSONs 已生成到: {PJSON_DIR}")


if __name__ == "__main__":
    build()
