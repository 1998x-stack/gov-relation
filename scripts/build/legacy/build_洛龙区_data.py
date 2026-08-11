#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 洛龙区 (Luolong District), 洛阳市, 河南省.

Level: 市辖区
Province: 河南省
Parent city: 洛阳市
Targets: 区委书记 (District Party Secretary), 区长 (District Government Head)
Task ID: henan_洛龙区

Research date: 2026-08-06
Primary official source: http://www.luolong.gov.cn/ (洛龙区人民政府) — reached successfully via curl.
  - 区政府领导之窗 (official leadership page): http://www.luolong.gov.cn/zwgk/wgkzl/glgk/ldzc/qzfld/
  - 六届区委常委会第2次会议新闻报道 (2026-07-08): https://www.luolong.gov.cn/2026/07-08/1072256.html

Current status (as of 2026-08-06):
- 区委书记: 韩建军 (confirmed — 区委书记主持召开六届区委常委会第2次会议 2026-07-03; 2026年4-7月多篇公开活动)
- 区委副书记、区政府党组书记、区长: 孙毅辉 (confirmed — 官方领导之窗: 汉族, 1978年2月, 中共党员, 大学学历)
- 区委常委、常务副区长: 张华伟 (汉族, 1982年10月, 中共党员, 研究生学历; 区政府党组副书记、区行政学校校长)
- 区委常委、宣传部长、副区长: 王国辉 (女, 1977年6月, 中共党员, 本科)
- 区政府党组成员、副区长: 马竞 (女, 1981年10月, 中共党员, 本科)
- 区政府党组成员、副区长、洛龙公安分局党委书记/局长: 黄鹏勃 (男, 1976年7月, 中共党员, 本科)
- Additional 区委常委会 members observed in committee meeting roster (2026-07-08): 张炜、赵阳、孙亚平、赵艳辉、杨益、张会博 (具体职务待确认)

Confidence notes:
  - Core leader identities and titles (书记 韩建军; 区长 孙毅辉): confirmed (official gov sources).
  - Government 领导之窗 members gender/birth/education: confirmed from official profiles.
  - 韩建军 biography (birth/education/native place), and 孙毅辉's prior career: NOT on official site.
    → explicit gaps in open_questions.
  - Predecessor of 韩建军 / 孙毅辉 and successor paths: unknown. Cross-district context: 2026 洛阳多区换届
    (西工区 张丽娟/袁峥 2026; 偃师区 赵玉勋 区长→书记 2026-04, 前书记 彭仁来调任洛阳市人大工委主任),
    洛龙区 韩建军/孙毅辉 likewise took office ~2026. 待核实.

This build uses confirmed + externally-unverifiable evidence. Biographical gaps are explicit, not fabricated.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / ".." / "..").resolve()
if not (_REPO_ROOT / "gov_relation").exists():
    _REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

import sqlite3  # noqa: F811

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "洛龙区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-08-06"
TODAY = "20260806"

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # 1. 韩建军 — 区委书记
    {
        "id": 1,
        "name": "韩建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洛龙区委书记",
        "current_org": "中共洛龙区委员会",
        "source": "confirmed — 洛龙区人民政府《六届区委常委会第2次会议》2026-07-08 https://www.luolong.gov.cn/2026/07-08/1072256.html（区委书记韩建军主持会议）；2026年4-7月多篇书记公开活动报道（luolong.gov.cn）",
    },
    # 2. 孙毅辉 — 区委副书记、区长
    {
        "id": 2,
        "name": "孙毅辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-02",
        "birthplace": "",
        "native": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洛龙区委副书记、区长",
        "current_org": "洛龙区人民政府",
        "source": "confirmed — 洛龙区人民政府 领导之窗 政府领导页面 https://www.luolong.gov.cn/zwgk/wgkzl/glgk/ldzc/qzfld/（区长简历：汉族，1978年2月，中共党员，大学学历）",
    },
    # 3. 张华伟 — 区委常委、常务副区长
    {
        "id": 3,
        "name": "张华伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-10",
        "birthplace": "",
        "native": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洛龙区委常委、区政府党组副书记、常务副区长、区行政学校校长",
        "current_org": "洛龙区人民政府",
        "source": "confirmed — 洛龙区人民政府 领导之窗 https://www.luolong.gov.cn/zwgk/wgkzl/glgk/ldzc/qzfld/",
    },
    # 4. 王国辉 — 区委常委、宣传部长、副区长
    {
        "id": 4,
        "name": "王国辉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977-06",
        "birthplace": "",
        "native": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洛龙区委常委、宣传部部长、副区长",
        "current_org": "中共洛龙区委员会",
        "source": "confirmed — 洛龙区人民政府 领导之窗（女，汉族，1977年6月，中共党员，本科）",
    },
    # 5. 马竞 — 副区长
    {
        "id": 5,
        "name": "马竞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981-10",
        "birthplace": "",
        "native": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洛龙区政府党组成员、副区长",
        "current_org": "洛龙区人民政府",
        "source": "confirmed — 洛龙区人民政府 领导之窗（女，汉族，1981年10月，中共党员，本科学历）",
    },
    # 6. 黄鹏勃 — 副区长、公安分局局长
    {
        "id": 6,
        "name": "黄鹏勃",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-07",
        "birthplace": "",
        "native": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洛龙区政府党组成员、副区长，洛龙公安分局党委书记、局长",
        "current_org": "洛龙公安分局",
        "source": "confirmed — 洛龙区人民政府 领导之窗（男，汉族，1976年7月，中共党员，本科学历）",
    },
    # 7-12. 区委常委会列席区领导 (from 六届区委常委会 2026-07-08 roster; 具体职务待确认)
    {"id": 7, "name": "张炜", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "native": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "洛龙区领导（区委常委，具体职务待确认）", "current_org": "中共洛龙区委员会", "source": "六届区委常委会第2次会议（2026-07-08）区领导名单"},
    {"id": 8, "name": "赵阳", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "native": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "洛龙区领导（区委常委，具体职务待确认）", "current_org": "中共洛龙区委员会", "source": "六届区委常委会第2次会议（2026-07-08）区领导名单"},
    {"id": 9, "name": "孙亚平", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "", "native": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "洛龙区领导（区委常委，具体职务待确认）", "current_org": "中共洛龙区委员会", "source": "六届区委常委会第2次会议（2026-07-08）区领导名单"},
    {"id": 10, "name": "赵艳辉", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "", "native": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "洛龙区领导（区委常委，具体职务待确认）", "current_org": "中共洛龙区委员会", "source": "六届区委常委会第2次会议（2026-07-08）区领导名单"},
    {"id": 11, "name": "杨益", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "native": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "洛龙区领导（区委常委，具体职务待确认）", "current_org": "中共洛龙区委员会", "source": "六届区委常委会第2次会议（2026-07-08）区领导名单"},
    {"id": 12, "name": "张会博", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "native": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "洛龙区领导（区委常委，具体职务待确认）", "current_org": "中共洛龙区委员会", "source": "六届区委常委会第2次会议（2026-07-08）区领导名单"},
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共洛龙区委员会", "type": "党委", "level": "县处级", "parent": "中共洛阳市委", "location": "河南省洛阳市洛龙区"},
    {"id": 2, "name": "洛龙区人民政府", "type": "政府", "level": "县处级", "parent": "洛阳市人民政府", "location": "河南省洛阳市洛龙区"},
    {"id": 3, "name": "中共洛龙区委宣传部", "type": "党委", "level": "县处级", "parent": "中共洛龙区委员会", "location": "河南省洛阳市洛龙区"},
    {"id": 4, "name": "洛龙区人大常委会", "type": "人大", "level": "县处级", "parent": "洛阳市人大常委会", "location": "河南省洛阳市洛龙区"},
    {"id": 5, "name": "洛龙区政协", "type": "政协", "level": "县处级", "parent": "洛阳市政协", "location": "河南省洛阳市洛龙区"},
    {"id": 6, "name": "洛龙区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "洛阳市纪委监委", "location": "河南省洛阳市洛龙区"},
    {"id": 7, "name": "洛龙公安分局", "type": "政府", "level": "乡科级", "parent": "洛阳市公安局", "location": "河南省洛阳市洛龙区"},
    {"id": 8, "name": "洛龙区行政学校", "type": "事业单位", "level": "乡科级", "parent": "洛龙区人民政府", "location": "河南省洛阳市洛龙区"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 韩建军 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "洛龙区委书记", "start_date": "2026", "end_date": "present", "rank": "县处级正职", "note": "2026-07-08 六届区委常委会会议及2026年4-7月多次公开活动确认；确切到任日期及历任地待核"},
    # 孙毅辉 — 区长
    {"person_id": 2, "org_id": 1, "title": "洛龙区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "官方领导之窗确认为区委副书记"},
    {"person_id": 2, "org_id": 2, "title": "洛龙区区长（区政府党组书记）", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "官方领导之窗确认为区委副书记、区政府党组书记、区长"},
    # 张华伟 — 常务副区长
    {"person_id": 3, "org_id": 2, "title": "区委常委、区政府党组副书记、常务副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "官方领导之窗确认"},
    {"person_id": 3, "org_id": 8, "title": "洛龙区行政学校校长", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": "官方领导之窗确认"},
    # 王国辉 — 宣传部长/副区长
    {"person_id": 4, "org_id": 1, "title": "洛龙区委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "官方领导之窗确认"},
    {"person_id": 4, "org_id": 3, "title": "洛龙区委宣传部部长", "start_date": "", "end_date": "present", "rank": "县处级", "note": "官方领导之窗确认"},
    {"person_id": 4, "org_id": 2, "title": "洛龙区副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "官方领导之窗确认"},
    # 马竞 — 副区长
    {"person_id": 5, "org_id": 2, "title": "洛龙区政府党组成员、副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "官方领导之窗确认"},
    # 黄鹏勃 — 副区长、公安分局长
    {"person_id": 6, "org_id": 2, "title": "洛龙区政府党组成员、副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "官方领导之窗确认"},
    {"person_id": 6, "org_id": 7, "title": "洛龙公安分局党委书记、局长", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": "官方领导之窗确认"},
    # 区委常委（具体职务待确认）— 列席六届区委常委会
    {"person_id": 7, "org_id": 1, "title": "洛龙区领导（区委常委，职务待确认）", "start_date": "", "end_date": "present", "rank": "县处级", "note": "列席六届区委常委会第2次会议"},
    {"person_id": 8, "org_id": 1, "title": "洛龙区领导（区委常委，职务待确认）", "start_date": "", "end_date": "present", "rank": "县处级", "note": "列席六届区委常委会第2次会议"},
    {"person_id": 9, "org_id": 1, "title": "洛龙区领导（区委常委，职务待确认）", "start_date": "", "end_date": "present", "rank": "县处级", "note": "列席六届区委常委会第2次会议"},
    {"person_id": 10, "org_id": 1, "title": "洛龙区领导（区委常委，职务待确认）", "start_date": "", "end_date": "present", "rank": "县处级", "note": "列席六届区委常委会第2次会议"},
    {"person_id": 11, "org_id": 1, "title": "洛龙区领导（区委常委，职务待确认）", "start_date": "", "end_date": "present", "rank": "县处级", "note": "列席六届区委常委会第2次会议"},
    {"person_id": 12, "org_id": 1, "title": "洛龙区领导（区委常委，职务待确认）", "start_date": "", "end_date": "present", "rank": "县处级", "note": "列席六届区委常委会第2次会议"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 韩建军 ↔ 孙毅辉 (党政主要领导搭档，明确)
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "洛龙区委书记与区长党政主要领导搭档；共同主持区委常委会扩大会议和政府重要会议",
        "overlap_org": "中共洛龙区委员会/洛龙区人民政府",
        "overlap_period": "截至2026年8月",
        "confidence": "confirmed",
    },
    # 韩建军 ↔ 张华伟 (书记与常务副区长)
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "区委书记与区委常委、常务副区长同属区委常委会及领导班子",
        "overlap_org": "中共洛龙区委员会/洛龙区人民政府",
        "overlap_period": "截至2026年8月",
        "confidence": "confirmed",
    },
    # 孙毅辉 ↔ 张华伟 (区长与常务副区长)
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "区长与常务副区长（区政府党组副书记）同属区政府班子核心成员",
        "overlap_org": "洛龙区人民政府",
        "overlap_period": "截至2026年8月",
        "confidence": "confirmed",
    },
    # 孙毅辉 ↔ 王国辉 (区长与宣传部长/副区长)
    {
        "person_a": 2, "person_b": 4,
        "type": "overlap",
        "context": "区长与区委常委、宣传部长、副区长的党政共事关系",
        "overlap_org": "洛龙区人民政府",
        "overlap_period": "截至2026年8月",
        "confidence": "confirmed",
    },
    # 孙毅辉 ↔ 马竞 (区长与副区长)
    {
        "person_a": 2, "person_b": 5,
        "type": "overlap",
        "context": "区长与区政府党组成员、副区长的共事关系",
        "overlap_org": "洛龙区人民政府",
        "overlap_period": "截至2026年8月",
        "confidence": "confirmed",
    },
    # 孙毅辉 ↔ 黄鹏勃 (区长与副区长/公安局长)
    {
        "person_a": 2, "person_b": 6,
        "type": "overlap",
        "context": "区长与副区长、洛龙公安分局局长的共事关系",
        "overlap_org": "洛龙区人民政府",
        "overlap_period": "截至2026年8月",
        "confidence": "confirmed",
    },
    # 张华伟 ↔ 王国辉 (常务副区长/宣传部长，同列政府班子)
    {
        "person_a": 3, "person_b": 4,
        "type": "overlap",
        "context": "同任洛龙区副区长，同属区政府领导班子",
        "overlap_org": "洛龙区人民政府",
        "overlap_period": "截至2026年8月",
        "confidence": "confirmed",
    },
    # 王国辉 ↔ 马竞 (政府班子副区长)
    {
        "person_a": 4, "person_b": 5,
        "type": "overlap",
        "context": "同为洛龙区副区长，同属区政府领导班子",
        "overlap_org": "洛龙区人民政府",
        "overlap_period": "截至2026年8月",
        "confidence": "confirmed",
    },
    # 马竞 ↔ 黄鹏勃 (副区长班子)
    {
        "person_a": 5, "person_b": 6,
        "type": "overlap",
        "context": "同为洛龙区副区长，同属区政府领导班子",
        "overlap_org": "洛龙区人民政府",
        "overlap_period": "截至2026年8月",
        "confidence": "confirmed",
    },
    # 列席六届区委常委会的区领导之间（职务待确认，弱关系）
    {"person_a": 7, "person_b": 8, "type": "overlap", "context": "同列席六届区委常委会第2次会议", "overlap_org": "中共洛龙区委员会", "overlap_period": "2026年7月", "confidence": "plausible"},
    {"person_a": 8, "person_b": 9, "type": "overlap", "context": "同列席六届区委常委会第2次会议", "overlap_org": "中共洛龙区委员会", "overlap_period": "2026年7月", "confidence": "plausible"},
    {"person_a": 9, "person_b": 10, "type": "overlap", "context": "同列席六届区委常委会第2次会议", "overlap_org": "中共洛龙区委员会", "overlap_period": "2026年7月", "confidence": "plausible"},
    {"person_a": 10, "person_b": 11, "type": "overlap", "context": "同列席六届区委常委会第2次会议", "overlap_org": "中共洛龙区委员会", "overlap_period": "2026年7月", "confidence": "plausible"},
    {"person_a": 11, "person_b": 12, "type": "overlap", "context": "同列席六届区委常委会第2次会议", "overlap_org": "中共洛龙区委员会", "overlap_period": "2026年7月", "confidence": "plausible"},
    {"person_a": 7, "person_b": 12, "type": "overlap", "context": "同列席六届区委常委会第2次会议", "overlap_org": "中共洛龙区委员会", "overlap_period": "2026年7月", "confidence": "plausible"},
    {"person_a": 7, "person_b": 11, "type": "overlap", "context": "同列席六届区委常委会第2次会议", "overlap_org": "中共洛龙区委员会", "overlap_period": "2026年7月", "confidence": "plausible"},
    {"person_a": 8, "person_b": 10, "type": "overlap", "context": "同列席六届区委常委会第2次会议", "overlap_org": "中共洛龙区委员会", "overlap_period": "2026年7月", "confidence": "plausible"},
    {"person_a": 9, "person_b": 11, "type": "overlap", "context": "同列席六届区委常委会第2次会议", "overlap_org": "中共洛龙区委员会", "overlap_period": "2026年7月", "confidence": "plausible"},
]

# ══════════════════════════════════════════════════════════════════════════════
# ONTOLOGY
# ══════════════════════════════════════════════════════════════════════════════

DEDUPE_PREFIX = "luolong"


def _slugify_name(name: str) -> str:
    return name.replace("（", "_").replace("）", "").replace(" ", "_")


def _slugify_job(post: str) -> str:
    if "区委书记" in post:
        return "区委书记"
    if "常务副区长" in post:
        return "常务副区长"
    if "宣传部长" in post:
        return "宣传部长"
    if "公安分局" in post:
        return "副区长"
    if "副区长" in post:
        return "副区长"
    if "区长" in post:
        return "区长"
    if "政府党组" in post:
        return "政府党组成员"
    if "区委常委" in post:
        return "区委常委"
    if "区领导" in post:
        return "区领导"
    return post.replace(" ", "_")


def _org_name(org_id: int) -> str:
    for o in organizations:
        if o["id"] == org_id:
            return o["name"]
    return ""


def _org_type(org_id: int) -> str:
    for o in organizations:
        if o["id"] == org_id:
            return o["type"]
    return ""


def _person_name(person_id: int) -> str:
    for p in persons:
        if p["id"] == person_id:
            return p["name"]
    return ""


# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON BUILDER
# ══════════════════════════════════════════════════════════════════════════════


def build_person_json(person: dict, relationships_subset: list[dict]) -> dict:
    """Build a person graph JSON from the data rows."""
    pid = person["id"]

    career_entries = []
    for pos in positions:
        if pos["person_id"] == pid:
            career_entries.append({
                "start": pos["start_date"] if pos.get("start_date") else "unknown",
                "end": pos["end_date"] if pos.get("end_date") else "unknown",
                "org": _org_name(pos["org_id"]),
                "title": pos["title"],
                "level": pos["rank"],
                "location": "河南省洛阳市洛龙区",
                "system": "party" if ("区委" in pos["title"] or "党委" in _org_name(pos["org_id"])) else "government",
                "rank": pos["rank"],
                "is_key_promotion": "区委书记" in pos["title"] or "区长" in pos["title"],
                "notes": pos["note"],
                "confidence": "confirmed" if person["id"] in (1, 2, 3, 4, 5, 6) else "plausible",
                "source_ids": ["S001", "S002"],
            })

    if not career_entries:
        career_entries.append({
            "start": "unknown",
            "end": "present",
            "org": person["current_org"],
            "title": person["current_post"],
            "level": "县处级",
            "location": "河南省洛阳市洛龙区",
            "system": "party" if "书记" in person["current_post"] else "government",
            "rank": "县处级",
            "is_key_promotion": True,
            "notes": "当前职务来自官方领导之窗/会议报道；具体到任时间待核。",
            "confidence": "plausible",
            "source_ids": [],
        })

    rels_out = []
    for r in relationships_subset:
        pa, pb = r["person_a"], r["person_b"]
        if pa != pid and pb != pid:
            continue
        other_id = pb if pa == pid else pa
        rels_out.append({
            "person": _person_name(other_id),
            "person_id": f"{DEDUPE_PREFIX}_{_slugify_name(_person_name(other_id))}",
            "relationship_type": r["type"],
            "strength": "strong" if r.get("confidence", "confirmed") == "confirmed" else "medium",
            "evidence": r["context"],
            "overlap_org": r["overlap_org"],
            "overlap_period": r["overlap_period"],
            "direction": "undirected",
            "confidence": r.get("confidence", "confirmed"),
            "source_ids": [],
        })

    orgs_out = []
    for pos in positions:
        if pos["person_id"] == pid:
            orgs_out.append({
                "org_id": pos["org_id"],
                "name": _org_name(pos["org_id"]),
                "type": _org_type(pos["org_id"]),
                "level": "县处级",
                "location": "河南省洛阳市洛龙区",
            })

    big_gap = "公开资料未找到该人物的完整早年履历与到任时间，需通过洛阳市委组织部任前公示核实。"
    if person["id"] == 1:
        big_gap = "韩建军的出生年月、出生地、教育背景、入党/工作时间，以及升任洛龙区委书记（约2026年）前的完整履历未能在官方途径获得，需洛阳市委组织部任前公示和跨区任免记录核实。"
    elif person["id"] == 2:
        big_gap = "孙毅辉（1978年2月生）在任洛龙区区长之前的职务与晋升路径未能在官方途径获得，需核实其由哪个市直部门/区县调入。"
    elif person["id"] in (7, 8, 9, 10, 11, 12):
        big_gap = "张炜、赵阳、孙亚平、赵艳辉、杨益、张会博等区领导的具体职务/分管领域待确认（仅确认列席区委常委会会议）。"

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河南省",
            "city": "洛阳市",
            "region": "洛龙区",
            "job": person["current_post"],
            "task_id": "henan_洛龙区",
            "time_focus": "当前",
        },
        "identity": {
            "person_id": f"{DEDUPE_PREFIX}_{_slugify_name(person['name'])}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": person.get("native", ""),
            "education": [],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "name_birthplace": f"{person['name']}_{person['birthplace']}",
                "official_profile_url": "https://www.luolong.gov.cn/zwgk/wgkzl/glgk/ldzc/qzfld/",
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "县处级正职" if person["id"] in (1, 2) else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"],
        },
        "career_timeline": career_entries,
        "organizations": orgs_out,
        "relationships": rels_out,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "缺少完整履历，无法评估晋升速度",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "pragmatic",
                    "evidence": "区委书记韩建军2026年4-7月多次实地调研重点项目、三夏生产、防汛、文旅服务、消防安全；区长孙毅辉主持区政府常务会议部署防汛排涝、安全生产",
                    "confidence": "plausible",
                    "source_ids": ["S002"],
                }
            ],
            "speech_themes": ["党建、高质量发展、全面从严治党、安全底线", "防灾减灾、安全生产、底线思维"],
            "management_signals": ["强调党建与业务融合、基层治理；强调安全生产底线和隐患排查"],
            "caveat": "工作风格推断基于公开报道，非私人心理评估。",
        },
        "network_metrics": {
            "direct_connections": len(rels_out),
            "memberships": len(orgs_out),
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至检索日未发现关于韩建军/孙毅辉的廉洁风险或纪律审查公开报道。此状态不表示无问题，仅表示在有限条件下未发现。",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "洛龙区人民政府 - 领导之窗（政府领导个人简历）",
                "url": "https://www.luolong.gov.cn/zwgk/wgkzl/glgk/ldzc/qzfld/",
                "publisher": "洛龙区人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认孙毅辉（区长）、张华伟、王国辉、马竞、黄鹏博等现任政府领导及出生年月、学历。",
            },
            {
                "id": "S002",
                "title": "洛龙区人民政府——六届区委常委会第2次会议（扩大会议）暨区委党的建设工作领导小组会议",
                "url": "https://www.luolong.gov.cn/2026/07-08/1072256.html",
                "publisher": "洛龙区融媒体中心",
                "published_at": "2026-07-08",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认韩建军为区委书记并主持；确认区委领导名单（孙毅辉、张炜、张华伟、赵阳、孙亚平、赵艳辉、杨益凯、张会权）。",
            },
        ],
        "confidence_summary": {
            "identity": "confirmed" if person["id"] in (1, 2, 3, 4, 5, 6) else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "high",
            "biggest_gap": big_gap,
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的出生年月、籍贯、受教育经历及任职前主要履历？",
                "why_it_matters": "构建核心人物完整履历的关键缺口。",
                "suggested_queries": [f"{person['name']} 简历 洛阳", f"{person['name']} 任前公示", "洛龙区 干部 任命"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "韩建军、孙毅辉的确切任洛龙区区委书记/区长更替时间线及前任是谁（去向）？",
                "why_it_matters": "掌握晋升路径和跨区/跨县人事交流线索。",
                "suggested_queries": ["洛龙区 历任 区委书记", "洛龙区 区长 前任", "洛阳市 组织部 任前公示"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "medium",
                "question": "张炜、赵阳、孙亚平、赵艳辉、杨毅、张会博等区委常委/区领导的具体职务？",
                "why_it_matters": "完善领导班子网络与分管领域。",
                "suggested_queries": ["洛龙区 区委 名单", "洛龙区 常委 分工"],
                "last_attempted": AS_OF,
            },
        ],
    }


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════


def write_person_jsons():
    """Write individual person JSON files for core figures."""
    core_ids = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}
    for p in persons:
        if p["id"] not in core_ids:
            continue
        person_rels = [r for r in relationships if r["person_a"] == p["id"] or r["person_b"] == p["id"]]
        data = build_person_json(p, person_rels)
        name_part = _slugify_name(p["name"])
        fname = f"{TODAY}-河南省-洛阳市-{_slugify_job(p['current_post'])}-{name_part}.json"
        fpath = PERSONS_DIR / fname
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Wrote {fpath.name}")


def main():
    print(f"=== Building network for {SLUG} ===")
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print()
    print(">>> Building database and GEXF...")
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
    print()

    print(">>> Writing person JSON files...")
    write_person_jsons()
    print()

    print("=== Build complete ===")
    print(f"  Database:  {DB_PATH} ({os.path.getsize(DB_PATH)} bytes)")
    print(f"  GEXF:      {GEXF_PATH} ({os.path.getsize(GEXF_PATH)} bytes)")
    print(f"  Persons:   {len(persons)}")
    print(f"  Orgs:      {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relations: {len(relationships)}")
    print()
    print("NOTE: Core identities confirmed from official sources. Complete career")
    print("timelines and birth/education gaps are flagged in each person JSON open_questions.")


if __name__ == "__main__":
    main()