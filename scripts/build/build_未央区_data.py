#!/usr/bin/env python3
"""Build 西安市未央区 (Weiyang District, Xi'an) leadership network data.

Level: 市辖区
Province: 陕西省
Parent city: 西安市
Targets: 区委书记 (Party Secretary), 区长 (Mayor)
Task ID: shaanxi_未央区

Research date: 2026-07-25
Official source: http://www.weiyang.gov.cn/ (西安市未央区人民政府)

Current status (as of 2026-07-25, verified via weiyang.gov.cn):
- 区委书记: 王小育 — confirmed by dwgk/ page (区委领导 section)
- 区委副书记、区长: 王红武 — confirmed by zwgk/ page (区长之窗 section)
- 区委副书记: 张云伟
- 区委常委: 王保静, 王静, 张水利, 张旭华, 杨柏松, 车飞, 侯运生
  (其中: 王保静 — 区纪委书记、监委主任; 车飞 — 区委常委、副区长)
- 副区长: 程希文, 张永辉, 薛凡, 王健, 王卫（兼公安未央分局局长）

Leadership transition:
- 王小育 previously served as 未央区区长 (at least 2022-2025, per government work reports
  for 区十八届人大二次、三次、四次会议), promoted to 区委书记 (timing ~early 2026 or late 2025)
- 王红武 succeeded 王小育 as 区长, also serves as 区委副书记
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "../../..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "未央区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = datetime.now().strftime("%Y-%m-%d")
TODAY = datetime.now().strftime("%Y%m%d")

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ══════════════════════════════════════════════════
    # 区委领导 (Party Committee)
    # ══════════════════════════════════════════════════

    # ── 区委书记 ──
    {
        "id": 1,
        "name": "王小育",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "未央区委书记",
        "current_org": "中共西安市未央区委员会",
        "source": "http://www.weiyang.gov.cn/dwgk/",
        "notes": "区政府官网党务公开页确认'书记：王小育'。此前长期担任未央区区长（至少2022-2025年）。出生年份、籍贯、教育等个人信息待补充。",
    },

    # ── 区委副书记、区长 ──
    {
        "id": 2,
        "name": "王红武",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "未央区委副书记、区长",
        "current_org": "西安市未央区人民政府",
        "source": "http://www.weiyang.gov.cn/zwgk/",
        "notes": "区政府官网政务公开'区长之窗'确认'区委副书记、区长：王红武'。领导区政府全面工作。分管区财政局（区国有资产管理局）、区审计局。更新日期：2026-05-14。",
    },

    # ── 区委副书记 ──
    {
        "id": 3,
        "name": "张云伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "未央区委副书记",
        "current_org": "中共西安市未央区委员会",
        "source": "http://www.weiyang.gov.cn/dwgk/",
        "notes": "区政府官网党务公开页确认为区委副书记。",
    },

    # ── 区委常委 ──
    {
        "id": 4,
        "name": "王保静",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、区监委主任",
        "current_org": "中共西安市未央区纪律检查委员会",
        "source": "http://www.weiyang.gov.cn/dwgk/yw/2080576149843922946.html",
        "notes": "2026年7月23日新闻确认'区委常委、区纪委书记、区监委主任王保静到草滩街道督导防汛与消防安全工作'",
    },
    {
        "id": 5,
        "name": "王静",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "未央区委常委",
        "current_org": "中共西安市未央区委员会",
        "source": "http://www.weiyang.gov.cn/dwgk/",
        "notes": "区政府官网党务公开页确认'常委：王静'。女性（姓名推断）。",
    },
    {
        "id": 6,
        "name": "张水利",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "未央区委常委",
        "current_org": "中共西安市未央区委员会",
        "source": "http://www.weiyang.gov.cn/dwgk/",
        "notes": "区政府官网党务公开页确认为区委常委。",
    },
    {
        "id": 7,
        "name": "张旭华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "未央区委常委",
        "current_org": "中共西安市未央区委员会",
        "source": "http://www.weiyang.gov.cn/dwgk/",
        "notes": "区政府官网党务公开页确认为区委常委。",
    },
    {
        "id": 8,
        "name": "杨柏松",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "未央区委常委",
        "current_org": "中共西安市未央区委员会",
        "source": "http://www.weiyang.gov.cn/dwgk/",
        "notes": "区政府官网党务公开页确认为区委常委。",
    },
    {
        "id": 9,
        "name": "车飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "西安市未央区人民政府",
        "source": "http://www.weiyang.gov.cn/zwgk/qczc/1.html",
        "notes": "区政府官网'区长之窗'确认'区委常委、副区长：车飞'。同时列入区委常委名单。",
    },
    {
        "id": 10,
        "name": "侯运生",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "未央区委常委",
        "current_org": "中共西安市未央区委员会",
        "source": "http://www.weiyang.gov.cn/dwgk/",
        "notes": "区政府官网党务公开页确认为区委常委。",
    },

    # ══════════════════════════════════════════════════
    # 区政府领导 (Government Leadership)
    # ══════════════════════════════════════════════════

    {
        "id": 11,
        "name": "程希文",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "西安市未央区人民政府",
        "source": "http://www.weiyang.gov.cn/zwgk/qczc/1.html",
        "notes": "区政府官网'区长之窗'确认为副区长。",
    },
    {
        "id": 12,
        "name": "张永辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "西安市未央区人民政府",
        "source": "http://www.weiyang.gov.cn/zwgk/qczc/1.html",
        "notes": "区政府官网'区长之窗'确认为副区长。",
    },
    {
        "id": 13,
        "name": "薛凡",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "西安市未央区人民政府",
        "source": "http://www.weiyang.gov.cn/zwgk/qczc/1.html",
        "notes": "区政府官网'区长之窗'确认为副区长。",
    },
    {
        "id": 14,
        "name": "王健",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "西安市未央区人民政府",
        "source": "http://www.weiyang.gov.cn/zwgk/qczc/1.html",
        "notes": "区政府官网'区长之窗'确认为副区长。",
    },
    {
        "id": 15,
        "name": "王卫",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、公安未央分局局长",
        "current_org": "西安市公安局未央分局",
        "source": "http://www.weiyang.gov.cn/zwgk/qczc/1.html",
        "notes": "区政府官网'区长之窗'确认为'副区长、公安未央分局局长：王卫'。",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共西安市未央区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共西安市委",
        "location": "西安市未央区",
    },
    {
        "id": 2,
        "name": "西安市未央区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "西安市人民政府",
        "location": "西安市未央区",
    },
    {
        "id": 3,
        "name": "中共西安市未央区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共西安市纪委",
        "location": "西安市未央区",
    },
    {
        "id": 4,
        "name": "西安市公安局未央分局",
        "type": "政府",
        "level": "乡科级",
        "parent": "西安市公安局",
        "location": "西安市未央区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 王小育
    {"person_id": "p1", "org_id": 1, "title": "未央区委书记", "start": "", "end": "present", "rank": "副厅级", "note": "党务公开页确认'书记：王小育'。此前长期任区长。"},
    {"person_id": "p1", "org_id": 2, "title": "未央区区长（前任）", "start": "", "end": "", "rank": "副厅级", "note": "至少2022年至2025年担任区长（2023-2025年政府工作报告均以区长身份发布）。"},

    # 王红武
    {"person_id": "p2", "org_id": 2, "title": "未央区区长", "start": "", "end": "present", "rank": "副厅级", "note": "区长之窗确认'区委副书记、区长：王红武'。更新日期：2026-05-14。领导区政府全面工作。"},
    {"person_id": "p2", "org_id": 1, "title": "未央区委副书记", "start": "", "end": "present", "rank": "副厅级", "note": "同时担任区委副书记。"},

    # 张云伟
    {"person_id": "p3", "org_id": 1, "title": "未央区委副书记", "start": "", "end": "present", "rank": "", "note": "党务公开页确认为区委副书记。"},

    # 王保静
    {"person_id": "p4", "org_id": 3, "title": "区纪委书记、区监委主任", "start": "", "end": "present", "rank": "", "note": "2026年7月23日新闻确认。也是区委常委。"},
    {"person_id": "p4", "org_id": 1, "title": "未央区委常委", "start": "", "end": "present", "rank": "", "note": "党务公开页确认为区委常委。"},

    # 王静
    {"person_id": "p5", "org_id": 1, "title": "未央区委常委", "start": "", "end": "present", "rank": "", "note": "党务公开页确认为区委常委。"},

    # 张水利
    {"person_id": "p6", "org_id": 1, "title": "未央区委常委", "start": "", "end": "present", "rank": "", "note": "党务公开页确认为区委常委。"},

    # 张旭华
    {"person_id": "p7", "org_id": 1, "title": "未央区委常委", "start": "", "end": "present", "rank": "", "note": "党务公开页确认为区委常委。"},

    # 杨柏松
    {"person_id": "p8", "org_id": 1, "title": "未央区委常委", "start": "", "end": "present", "rank": "", "note": "党务公开页确认为区委常委。"},

    # 车飞
    {"person_id": "p9", "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "", "note": "区长之窗确认'区委常委、副区长：车飞'。"},
    {"person_id": "p9", "org_id": 1, "title": "未央区委常委", "start": "", "end": "present", "rank": "", "note": "党务公开页确认为区委常委。"},

    # 侯运生
    {"person_id": "p10", "org_id": 1, "title": "未央区委常委", "start": "", "end": "present", "rank": "", "note": "党务公开页确认为区委常委。"},

    # 程希文
    {"person_id": "p11", "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "", "note": "区长之窗确认为副区长。"},

    # 张永辉
    {"person_id": "p12", "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "", "note": "区长之窗确认为副区长。"},

    # 薛凡
    {"person_id": "p13", "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "", "note": "区长之窗确认为副区长。"},

    # 王健
    {"person_id": "p14", "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "", "note": "区长之窗确认为副区长。"},

    # 王卫
    {"person_id": "p15", "org_id": 4, "title": "公安未央分局局长", "start": "", "end": "present", "rank": "", "note": "区长之窗确认'副区长、公安未央分局局长：王卫'。"},
    {"person_id": "p15", "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "", "note": "兼任副区长。"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 王小育 ↔ 王红武 （前任-后任：区长交接）
    {
        "person_a": "p1",
        "person_b": "p2",
        "type": "predecessor_successor",
        "context": "王小育此前担任未央区区长，王红武接任区长。两人同时在区委班子共事（王小育为书记，王红武为副书记）。",
        "overlap_org": "中共西安市未央区委员会",
        "overlap_period": "至present",
        "confidence": "confirmed",
    },
    # 王小育 → 区委常委（领导关系）
    {
        "person_a": "p1",
        "person_b": "p4",
        "type": "superior_subordinate",
        "context": "区委书记与纪委书记同届区委班子",
        "overlap_org": "中共西安市未央区委员会",
        "overlap_period": "至present",
        "confidence": "confirmed",
    },
    {
        "person_a": "p1",
        "person_b": "p5",
        "type": "superior_subordinate",
        "context": "区委书记与区委常委同届班子",
        "overlap_org": "中共西安市未央区委员会",
        "overlap_period": "至present",
        "confidence": "confirmed",
    },
    {
        "person_a": "p1",
        "person_b": "p6",
        "type": "superior_subordinate",
        "context": "区委书记与区委常委同届班子",
        "overlap_org": "中共西安市未央区委员会",
        "overlap_period": "至present",
        "confidence": "confirmed",
    },
    {
        "person_a": "p1",
        "person_b": "p7",
        "type": "superior_subordinate",
        "context": "区委书记与区委常委同届班子",
        "overlap_org": "中共西安市未央区委员会",
        "overlap_period": "至present",
        "confidence": "confirmed",
    },
    {
        "person_a": "p1",
        "person_b": "p8",
        "type": "superior_subordinate",
        "context": "区委书记与区委常委同届班子",
        "overlap_org": "中共西安市未央区委员会",
        "overlap_period": "至present",
        "confidence": "confirmed",
    },
    {
        "person_a": "p1",
        "person_b": "p9",
        "type": "superior_subordinate",
        "context": "区委书记与区委常委同届班子",
        "overlap_org": "中共西安市未央区委员会",
        "overlap_period": "至present",
        "confidence": "confirmed",
    },
    {
        "person_a": "p1",
        "person_b": "p10",
        "type": "superior_subordinate",
        "context": "区委书记与区委常委同届班子",
        "overlap_org": "中共西安市未央区委员会",
        "overlap_period": "至present",
        "confidence": "confirmed",
    },
    # 王红武 ↔ 区政府领导（区长与副区长共事）
    {
        "person_a": "p2",
        "person_b": "p9",
        "type": "overlap",
        "context": "区长与副区长（区委常委兼任）同届政府班子",
        "overlap_org": "西安市未央区人民政府",
        "overlap_period": "至present",
        "confidence": "confirmed",
    },
    {
        "person_a": "p2",
        "person_b": "p11",
        "type": "overlap",
        "context": "区长与副区长同届政府班子",
        "overlap_org": "西安市未央区人民政府",
        "overlap_period": "至present",
        "confidence": "confirmed",
    },
    {
        "person_a": "p2",
        "person_b": "p12",
        "type": "overlap",
        "context": "区长与副区长同届政府班子",
        "overlap_org": "西安市未央区人民政府",
        "overlap_period": "至present",
        "confidence": "confirmed",
    },
    {
        "person_a": "p2",
        "person_b": "p13",
        "type": "overlap",
        "context": "区长与副区长同届政府班子",
        "overlap_org": "西安市未央区人民政府",
        "overlap_period": "至present",
        "confidence": "confirmed",
    },
    {
        "person_a": "p2",
        "person_b": "p14",
        "type": "overlap",
        "context": "区长与副区长同届政府班子",
        "overlap_org": "西安市未央区人民政府",
        "overlap_period": "至present",
        "confidence": "confirmed",
    },
    {
        "person_a": "p2",
        "person_b": "p15",
        "type": "overlap",
        "context": "区长与副区长兼公安局长同届政府班子",
        "overlap_org": "西安市未央区人民政府",
        "overlap_period": "至present",
        "confidence": "confirmed",
    },
    # 张云伟（副书记）↔ 书记、区长
    {
        "person_a": "p3",
        "person_b": "p1",
        "type": "superior_subordinate",
        "context": "区委书记与区委副书记同届区委班子",
        "overlap_org": "中共西安市未央区委员会",
        "overlap_period": "至present",
        "confidence": "confirmed",
    },
    {
        "person_a": "p3",
        "person_b": "p2",
        "type": "overlap",
        "context": "两位区委副书记同届区委班子",
        "overlap_org": "中共西安市未央区委员会",
        "overlap_period": "至present",
        "confidence": "confirmed",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# SOURCE REGISTER (shared)
# ══════════════════════════════════════════════════════════════════════════════

_source_register = [
    {
        "id": "S001",
        "title": "未央区党务公开——区委领导",
        "url": "http://www.weiyang.gov.cn/dwgk/",
        "publisher": "西安市未央区人民政府",
        "published_at": "2026-07",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "确认区委书记王小育，副书记王红武、张云伟，常委王保静、王静、张水利、张旭华、杨柏松、车飞、侯运生",
    },
    {
        "id": "S002",
        "title": "未央区政府信息公开——区长之窗",
        "url": "http://www.weiyang.gov.cn/zwgk/qczc/1.html",
        "publisher": "西安市未央区人民政府",
        "published_at": "2026-05-14",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "确认区长王红武，副区长车飞、程希文、张永辉、薛凡、王健、王卫。更新日期2026-05-14。区长分工：领导区政府全面工作，分管财政局、审计局。",
    },
    {
        "id": "S003",
        "title": "未央区人民政府首页",
        "url": "http://www.weiyang.gov.cn/",
        "publisher": "西安市未央区人民政府",
        "published_at": "2026-07",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "首页新闻栏目，可获取最新政府活动和领导活动动态。",
    },
    {
        "id": "S004",
        "title": "区委常委、区纪委书记王保静督导防汛与消防安全工作",
        "url": "http://www.weiyang.gov.cn/dwgk/yw/2080576149843922946.html",
        "publisher": "西安市未央区人民政府",
        "published_at": "2026-07-23",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "确认王保静为区委常委、区纪委书记、区监委主任",
    },
    {
        "id": "S005",
        "title": "未央区委主要领导调研重点项目建设情况",
        "url": "http://www.weiyang.gov.cn/xwzx/wyyw/",
        "publisher": "西安市未央区人民政府",
        "published_at": "2026-07-22",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "确认区委主要领导调研活动（未直接点名具体人，但提'区委主要领导'）",
    },
    {
        "id": "S006",
        "title": "未央区政府工作报告——王小育（2023-2025）、王红武（2026）",
        "url": "http://www.weiyang.gov.cn/zwgk/ghjh/zfgzbg/",
        "publisher": "西安市未央区人民政府",
        "published_at": "2023-2026",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "2022-2025年政府工作报告以王小育区长名义发布；2026年政府工作报告以王红武区长名义发布（区十八届人大五次会议）。确认区长交接。",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON HELPERS
# ══════════════════════════════════════════════════════════════════════════════


def make_person_json(person, timeline_items, relationship_list, is_secretary):
    """Build a person graph JSON following the schema."""
    scope_job = "未央区委书记" if is_secretary else "未央区长"
    biggest_gap = "缺失出生年份、籍贯、教育背景和完整履历；缺失王小育从区长晋升书记的具体时间" if is_secretary else "缺失出生年份、籍贯、教育背景和完整履历；缺失王红武任区长前的职务轨迹"

    open_qs = [
        {
            "priority": "critical",
            "question": f"{person['name']}的出生年份、籍贯和教育背景是什么？",
            "why_it_matters": "用于人员去重和晋升速度分析",
            "suggested_queries": [
                f"{person['name']} 简历 未央区",
                f"{person['name']} 出生 籍贯 学历",
                f"{person['name']} 西安 任职经历"
            ],
            "last_attempted": AS_OF
        },
        {
            "priority": "high",
            "question": f"{person['name']}在担任现职前的工作履历是什么？",
            "why_it_matters": "完整的晋升路径揭示工作关系网络",
            "suggested_queries": [
                f"{person['name']} 此前担任",
                f"{person['name']} 调任 未央区",
                f"{person['name']} 历任"
            ],
            "last_attempted": AS_OF
        }
    ]
    if is_secretary:
        open_qs.append({
            "priority": "high",
            "question": "王小育从区长晋升区委书记的具体时间和任命文件是什么？",
            "why_it_matters": "确认交接时间线和西安市跨区/市级干部调整规律",
            "suggested_queries": [
                "王小育 任未央区委书记 任命",
                "王小育 未央区委书记 任前公示",
                "西安市委组织部 未央区 干部任免"
            ],
            "last_attempted": AS_OF
        })
    else:
        open_qs.append({
            "priority": "high",
            "question": "王红武担任区长前曾任哪些职务？是否来自西安市其他区县或市直部门？",
            "why_it_matters": "确认交接来源和跨区/系统流动模式",
            "suggested_queries": [
                "王红武 未央区 此前任职",
                "王红武 西安 任职",
                "王红武 任前公示"
            ],
            "last_attempted": AS_OF
        })

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "陕西省",
            "city": "西安市",
            "region": "未央区",
            "job": scope_job,
            "task_id": "shaanxi_未央区",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": f"weiyang_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("native_place", ""),
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth', '')}" if person.get("birth") else person["name"],
                "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}" if person.get("birthplace") else person["name"],
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "副厅级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002", "S003"]
        },
        "career_timeline": timeline_items,
        "organizations": [],
        "relationships": relationship_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "无法评估——缺少出生年份和完整履历",
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
                "confidence": "unverified",
                "date": "",
                "description": "公开资料中未发现纪律处分、审计问题或负面报道。2026年7月纪检监察巡视信息待核实。",
                "source_ids": []
            }
        ],
        "source_register": _source_register,
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": biggest_gap
        },
        "open_questions": open_qs
    }


def write_person_json(person, timeline_items, relationship_list, is_secretary):
    data = make_person_json(person, timeline_items, relationship_list, is_secretary)
    # Parse job title from current_post
    job_short = "区委书记" if is_secretary else "区长"
    path = PERSONS_DIR / f"{TODAY}-陕西省-西安市-{job_short}-{person['name']}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {path.name}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════


def main():
    os.makedirs(_STAGING_DIR, exist_ok=True)

    # Build DB + GEXF
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
    print("\n--- Person JSONs ---")

    # 王小育 — 区委书记
    xxy_timeline = [
        {
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "level": "",
            "location": "",
            "system": "other",
            "rank": "",
            "is_key_promotion": False,
            "notes": "公开资料未找到王小育担任未央区区长前的完整履历",
            "confidence": "unverified",
            "source_ids": []
        },
        {
            "start": "",
            "end": "",
            "org": "西安市未央区人民政府",
            "title": "未央区区长",
            "level": "副厅级",
            "location": "西安市未央区",
            "system": "government",
            "rank": "",
            "is_key_promotion": True,
            "notes": "至少从2022年（十八届人大二次会议）到2025年（十八届人大四次会议）担任区长。2023年1月、2024年2月、2025年3月分别以区长身份作政府工作报告。",
            "confidence": "confirmed",
            "source_ids": ["S006"]
        },
        {
            "start": "",
            "end": "present",
            "org": "中共西安市未央区委员会",
            "title": "未央区委书记",
            "level": "副厅级",
            "location": "西安市未央区",
            "system": "party",
            "rank": "",
            "is_key_promotion": True,
            "notes": "从区长晋升为区委书记。具体任命时间待确认（2026年7月党务公开页已显示为书记）。",
            "confidence": "confirmed",
            "source_ids": ["S001", "S003"]
        },
    ]
    xxy_relationships = [
        {
            "person": "王红武",
            "person_id": "weiyang_wanghongwu",
            "relationship_type": "predecessor_successor",
            "strength": "strong",
            "evidence": "王小育原为区长，王红武接任区长；两人同时在区委班子（书记+副书记）",
            "overlap_org": "中共西安市未央区委员会",
            "overlap_period": "2026至present",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001", "S002"]
        },
        {
            "person": "张云伟",
            "person_id": "weiyang_zhangyunwei",
            "relationship_type": "overlap",
            "strength": "medium",
            "evidence": "区委书记与区委副书记同届区委班子",
            "overlap_org": "中共西安市未央区委员会",
            "overlap_period": "至present",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"]
        },
        {
            "person": "王保静",
            "person_id": "weiyang_wangbaojing",
            "relationship_type": "overlap",
            "strength": "medium",
            "evidence": "区委书记与区纪委书记同届区委常委会",
            "overlap_org": "中共西安市未央区委员会",
            "overlap_period": "至present",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001", "S004"]
        },
    ]
    write_person_json(persons[0], xxy_timeline, xxy_relationships, is_secretary=True)

    # 王红武 — 区长
    whw_timeline = [
        {
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "level": "",
            "location": "",
            "system": "other",
            "rank": "",
            "is_key_promotion": False,
            "notes": "公开资料未找到王红武担任未央区长前的完整履历",
            "confidence": "unverified",
            "source_ids": []
        },
        {
            "start": "",
            "end": "present",
            "org": "西安市未央区人民政府",
            "title": "未央区区长",
            "level": "副厅级",
            "location": "西安市未央区",
            "system": "government",
            "rank": "",
            "is_key_promotion": True,
            "notes": "2026年3月区十八届人大五次会议以区长身份作政府工作报告。区长之窗更新日期2026-05-14。领导区政府全面工作，分管区财政局（区国有资产管理局）、区审计局。",
            "confidence": "confirmed",
            "source_ids": ["S002", "S006"]
        },
        {
            "start": "",
            "end": "present",
            "org": "中共西安市未央区委员会",
            "title": "未央区委副书记",
            "level": "副厅级",
            "location": "西安市未央区",
            "system": "party",
            "rank": "",
            "is_key_promotion": False,
            "notes": "同时担任区委副书记。",
            "confidence": "confirmed",
            "source_ids": ["S001"]
        },
    ]
    whw_relationships = [
        {
            "person": "王小育",
            "person_id": "weiyang_wangxiaoyu",
            "relationship_type": "predecessor_successor",
            "strength": "strong",
            "evidence": "王红武接替王小育任区长；两人同时在区委班子（副书记+书记）",
            "overlap_org": "中共西安市未央区委员会",
            "overlap_period": "2026至present",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001", "S002"]
        },
        {
            "person": "车飞",
            "person_id": "weiyang_chefei",
            "relationship_type": "overlap",
            "strength": "medium",
            "evidence": "区长与区委常委、副区长同届政府班子",
            "overlap_org": "西安市未央区人民政府",
            "overlap_period": "至present",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S002"]
        },
        {
            "person": "程希文",
            "person_id": "weiyang_chengxiwen",
            "relationship_type": "overlap",
            "strength": "medium",
            "evidence": "区长与副区长同届政府班子",
            "overlap_org": "西安市未央区人民政府",
            "overlap_period": "至present",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S002"]
        },
    ]
    write_person_json(persons[1], whw_timeline, whw_relationships, is_secretary=False)

    print(f"\n{'='*60}")
    print(f"未央区 Network Build Complete")
    print(f"{'='*60}")
    print(f"Staging dir: {_STAGING_DIR}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")


if __name__ == "__main__":
    main()
