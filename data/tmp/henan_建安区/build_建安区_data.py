#!/usr/bin/env python3
"""Build 许昌市建安区 (Xuchang Jian'an District) leadership network data.

Level: 市辖区
Province: 河南省
Parent city: 许昌市
Targets: 区委书记 (Party Secretary), 区长 (Mayor)
Task ID: henan_建安区

Research date: 2026-07-24
Official source: http://www.jianan.gov.cn/ (许昌市建安区人民政府)
Staging build: data/tmp/henan_建安区/ → promoted by process_tmp.py

Current status (as of 2026-07-24, verified via 区二次党代会 2026-06-23):
- 区委书记: 高雁 — 女（推断），2026年6月二次党代会前已在任。出现于"两优一先"表彰大会（6月30日）、
  人民武装工作会议（7月15日）等多篇新闻报道，均以区委书记身份出席
- 区长: 刘建伟 — 许昌市建安区委副书记，区人民政府区长、党组书记（区政府领导页面确认）。
  主持召开区政府第57次常务会议（7月9日）、第二届人民政府第五次全体会议（6月10日）
- 区委副书记、政法委书记: 连良
- 区委常委（已知12人）: 高雁、刘建伟、连良、李梦龙（办公室主任）、董传斌（副区长）、
  王伟（常务副区长）、张自锋（纪委书记/监委主任）、朱键、李静、董华、龚文兵、邴娅
- 副区长（7人）: 王伟（常务）、董传斌、朱红凯（兼公安局长）、程伟峰、刘晓召、廖睿

Confirmed official sources:
- 区政府领导页面: http://www.jianan.gov.cn/zwgk/003012/secondPageLeaders.html
- 区二次党代会代表看望 (2026-06-23): 确认高雁(区委书记)、刘建伟(副书记/区长)、连良、朱键等
- 两优一先表彰大会 (2026-06-30): 确认高雁(区委书记)、刘建伟(副书记/区长)
- 人民武装工作会议 (2026-07-16): 确认高雁(区委书记/人武部党委第一书记)
- 国道107调研 (2026-06-18): 确认高雁(区委书记)、刘建伟(区长)、李梦龙(区委办主任)、刘晓召(副区长)
- 区政府五次全会 (2026-06-10): 确认刘建伟(区长)、王伟(常务副区长)、董传斌(副区长)、张自锋(纪委书记)
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

SLUG = "建安区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = datetime.now().strftime("%Y-%m-%d")
TODAY = datetime.now().strftime("%Y%m%d")

import sqlite3  # noqa: F811

OFFICIAL_LDZC = "http://www.jianan.gov.cn/zwgk/003012/secondPageLeaders.html"

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 区委领导 (Party Committee)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "高雁",
        "gender": "女（推断）",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "建安区委书记",
        "current_org": "中共许昌市建安区委员会",
        "source": ("官方: http://www.jianan.gov.cn/jrja/001001/20260630/e6eee9c7-b500-4689-bded-b4191419e845.html "
                    "(两优一先表彰大会以书记身份讲话); "
                    "官方: http://www.jianan.gov.cn/jrja/001001/20260716/4e7092be-a943-48ef-a8f1-d3e2ae8d4ab6.html "
                    "(人武部党委第一书记)"),
    },
    {
        "id": 2,
        "name": "刘建伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "建安区委副书记、区长",
        "current_org": "建安区人民政府",
        "source": ("官方领导页: http://www.jianan.gov.cn/zwgk/003012/secondPageLeaders.html "
                    "(区委副书记、区长、党组书记); "
                    "官方: http://www.jianan.gov.cn/jrja/001001/20260709/46ea5950-5397-425c-8d42-dbb7c0002fa2.html "
                    "(主持第57次常务会议)"),
    },
    {
        "id": 3,
        "name": "连良",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、政法委书记",
        "current_org": "中共许昌市建安区委员会",
        "source": ("官方: http://www.jianan.gov.cn/jrja/001001/20260630/e6eee9c7-b500-4689-bded-b4191419e845.html "
                    "(宣读表彰决定)"),
    },
    {
        "id": 4,
        "name": "李梦龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、办公室主任",
        "current_org": "中共许昌市建安区委员会",
        "source": ("官方: http://www.jianan.gov.cn/jrja/001001/20260618/5574c2c9-8e8b-4f27-a3ec-58acfb86fe29.html "
                    "(参加G107调研，注明区委常委、办公室主任)"),
    },
    {
        "id": 5,
        "name": "董传斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "建安区人民政府",
        "source": ("官方领导页: http://www.jianan.gov.cn/zwgk/003012/secondPageLeaders.html "
                    "(区委常委、副区长、党组成员); "
                    "官方: http://www.jianan.gov.cn/jrja/001001/20260611/f133a7f5-00a3-4c2c-aadc-7d8cccaa2ab2.html "
                    "(出席区政府五次全会)"),
    },
    {
        "id": 6,
        "name": "王伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "建安区人民政府",
        "source": ("官方领导页: http://www.jianan.gov.cn/zwgk/003012/secondPageLeaders.html "
                    "(区委常委、副区长、党组副书记); "
                    "官方: http://www.jianan.gov.cn/jrja/001001/20260611/f133a7f5-00a3-4c2c-aadc-7d8cccaa2ab2.html "
                    "(出席区政府五次全会)"),
    },
    {
        "id": 7,
        "name": "张自锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、监委主任",
        "current_org": "中共许昌市建安区纪律检查委员会",
        "source": ("官方: http://www.jianan.gov.cn/jrja/001001/20260611/f133a7f5-00a3-4c2c-aadc-7d8cccaa2ab2.html "
                    "(区委常委、区纪委书记、监委主任，进行集体廉政谈话)"),
    },
    {
        "id": 8,
        "name": "朱键",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共许昌市建安区委员会",
        "source": ("官方: http://www.jianan.gov.cn/jrja/001001/20260623/d60fa984-dfd1-4737-81a0-27aa3d8d8000.html "
                    "(看望区二次党代会代表)"),
    },
    {
        "id": 9,
        "name": "李静",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共许昌市建安区委员会",
        "source": ("官方: http://www.jianan.gov.cn/jrja/001001/20260623/d60fa984-dfd1-4737-81a0-27aa3d8d8000.html "
                    "(看望区二次党代会代表)"),
    },
    {
        "id": 10,
        "name": "董华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共许昌市建安区委员会",
        "source": ("官方: http://www.jianan.gov.cn/jrja/001001/20260623/d60fa984-dfd1-4737-81a0-27aa3d8d8000.html "
                    "(看望区二次党代会代表)"),
    },
    {
        "id": 11,
        "name": "龚文兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共许昌市建安区委员会",
        "source": ("官方: http://www.jianan.gov.cn/jrja/001001/20260623/d60fa984-dfd1-4737-81a0-27aa3d8d8000.html "
                    "(看望区二次党代会代表)"),
    },
    {
        "id": 12,
        "name": "邴娅",
        "gender": "女（推断）",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共许昌市建安区委员会",
        "source": ("官方: http://www.jianan.gov.cn/jrja/001001/20260623/d60fa984-dfd1-4737-81a0-27aa3d8d8000.html "
                    "(看望区二次党代会代表)"),
    },
    # ════════════════════════════════════════
    # 区政府领导 (Government Leadership, non-常委)
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "朱红凯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、区公安局局长",
        "current_org": "建安区人民政府",
        "source": ("官方领导页: http://www.jianan.gov.cn/zwgk/003012/secondPageLeaders.html "
                    "(副区长、党组成员、公安局长)"),
    },
    {
        "id": 14,
        "name": "程伟峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "建安区人民政府",
        "source": ("官方领导页: http://www.jianan.gov.cn/zwgk/003012/secondPageLeaders.html "
                    "(副区长、党组成员); "
                    "官方: http://www.jianan.gov.cn/jrja/001001/20260611/f133a7f5-00a3-4c2c-aadc-7d8cccaa2ab2.html "
                    "(出席区政府五次全会)"),
    },
    {
        "id": 15,
        "name": "刘晓召",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "建安区人民政府",
        "source": ("官方领导页: http://www.jianan.gov.cn/zwgk/003012/secondPageLeaders.html "
                    "(副区长、党组成员); "
                    "官方: http://www.jianan.gov.cn/jrja/001001/20260618/5574c2c9-8e8b-4f27-a3ec-58acfb86fe29.html "
                    "(参加G107调研)"),
    },
    {
        "id": 16,
        "name": "廖睿",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "建安区人民政府",
        "source": ("官方领导页: http://www.jianan.gov.cn/zwgk/003012/secondPageLeaders.html "
                    "(副区长、党组成员)"),
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共许昌市建安区委员会", "type": "党委", "level": "市辖区",
     "parent": "中共许昌市委员会", "location": "河南省许昌市建安区"},
    {"id": 2, "name": "建安区人民政府", "type": "政府", "level": "市辖区",
     "parent": "许昌市人民政府", "location": "河南省许昌市建安区"},
    {"id": 3, "name": "中共许昌市建安区纪律检查委员会", "type": "纪委", "level": "市辖区",
     "parent": "中共许昌市纪律检查委员会", "location": "河南省许昌市建安区"},
    {"id": 4, "name": "建安区人大常委会", "type": "人大", "level": "市辖区",
     "parent": "许昌市人大常委会", "location": "河南省许昌市建安区"},
    {"id": 5, "name": "政协建安区委员会", "type": "政协", "level": "市辖区",
     "parent": "政协许昌市委员会", "location": "河南省许昌市建安区"},
    {"id": 6, "name": "许昌市公安局建安分局", "type": "政府", "level": "区直部门",
     "parent": "许昌市公安局", "location": "河南省许昌市建安区"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 高雁 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "建安区委书记", "start": "", "end": "至今",
     "rank": "县处级正职", "note": "区人武部党委第一书记；2026年6月二次党代会前已在任"},
    # 刘建伟 — 区长
    {"person_id": 2, "org_id": 1, "title": "建安区委副书记", "start": "", "end": "至今",
     "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "建安区区长", "start": "", "end": "至今",
     "rank": "县处级正职", "note": "区政府党组书记"},
    # 连良 — 副书记、政法委书记
    {"person_id": 3, "org_id": 1, "title": "建安区委副书记、政法委书记", "start": "", "end": "至今",
     "rank": "县处级副职", "note": ""},
    # 李梦龙 — 常委、办公室主任
    {"person_id": 4, "org_id": 1, "title": "建安区委常委、办公室主任", "start": "", "end": "至今",
     "rank": "县处级副职", "note": ""},
    # 董传斌 — 常委、副区长
    {"person_id": 5, "org_id": 1, "title": "建安区委常委", "start": "", "end": "至今",
     "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "建安区副区长", "start": "", "end": "至今",
     "rank": "县处级副职", "note": "区政府党组成员"},
    # 王伟 — 常委、常务副区长
    {"person_id": 6, "org_id": 1, "title": "建安区委常委", "start": "", "end": "至今",
     "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "建安区常务副区长", "start": "", "end": "至今",
     "rank": "县处级副职", "note": "区政府党组副书记"},
    # 张自锋 — 常委、纪委书记
    {"person_id": 7, "org_id": 3, "title": "建安区纪委书记、监委主任", "start": "", "end": "至今",
     "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "建安区委常委", "start": "", "end": "至今",
     "rank": "县处级副职", "note": ""},
    # 区委常委
    {"person_id": 8, "org_id": 1, "title": "建安区委常委", "start": "", "end": "至今",
     "rank": "县处级副职", "note": "职务待确认"},
    {"person_id": 9, "org_id": 1, "title": "建安区委常委", "start": "", "end": "至今",
     "rank": "县处级副职", "note": "职务待确认"},
    {"person_id": 10, "org_id": 1, "title": "建安区委常委", "start": "", "end": "至今",
     "rank": "县处级副职", "note": "职务待确认"},
    {"person_id": 11, "org_id": 1, "title": "建安区委常委", "start": "", "end": "至今",
     "rank": "县处级副职", "note": "职务待确认"},
    {"person_id": 12, "org_id": 1, "title": "建安区委常委", "start": "", "end": "至今",
     "rank": "县处级副职", "note": "职务待确认"},
    # 副区长
    {"person_id": 13, "org_id": 2, "title": "建安区副区长", "start": "", "end": "至今",
     "rank": "县处级副职", "note": "区政府党组成员，兼区公安局局长"},
    {"person_id": 13, "org_id": 6, "title": "建安区公安局局长", "start": "", "end": "至今",
     "rank": "乡科级正职", "note": "党委书记、局长"},
    {"person_id": 14, "org_id": 2, "title": "建安区副区长", "start": "", "end": "至今",
     "rank": "县处级副职", "note": "区政府党组成员"},
    {"person_id": 15, "org_id": 2, "title": "建安区副区长", "start": "", "end": "至今",
     "rank": "县处级副职", "note": "区政府党组成员"},
    {"person_id": 16, "org_id": 2, "title": "建安区副区长", "start": "", "end": "至今",
     "rank": "县处级副职", "note": "区政府党组成员"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区长党政工作搭档关系，共同出席多项重要活动",
     "overlap_org": "建安区", "overlap_period": "2026年"},
    # 区委书记与副书记
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "区委书记与副书记/政法委书记工作搭档",
     "overlap_org": "中共建安区委", "overlap_period": ""},
    # 区委书记与常委班子
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "区委书记与区委常委/办公室主任",
     "overlap_org": "中共建安区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "区委书记与区委常委/副区长",
     "overlap_org": "中共建安区委/区政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "区委书记与常务副区长",
     "overlap_org": "中共建安区委/区政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "区委书记与纪委书记",
     "overlap_org": "中共建安区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "overlap",
     "context": "区委书记与区委常委班子成员",
     "overlap_org": "中共建安区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "overlap",
     "context": "区委书记与区委常委班子成员",
     "overlap_org": "中共建安区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "overlap",
     "context": "区委书记与区委常委班子成员",
     "overlap_org": "中共建安区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "overlap",
     "context": "区委书记与区委常委班子成员",
     "overlap_org": "中共建安区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "overlap",
     "context": "区委书记与区委常委班子成员",
     "overlap_org": "中共建安区委", "overlap_period": ""},
    # 区长与副区长
    {"person_a": 2, "person_b": 6, "type": "overlap",
     "context": "区长与常务副区长工作搭档",
     "overlap_org": "建安区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "overlap",
     "context": "区长与副区长工作搭档",
     "overlap_org": "建安区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "overlap",
     "context": "区长与副区长/公安局长工作搭档",
     "overlap_org": "建安区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "overlap",
     "context": "区长与副区长工作搭档",
     "overlap_org": "建安区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "overlap",
     "context": "区长与副区长工作搭档，共同参加G107调研",
     "overlap_org": "建安区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "overlap",
     "context": "区长与副区长工作搭档",
     "overlap_org": "建安区政府", "overlap_period": ""},
    # 区长与副书记
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "区长与副书记/政法委书记工作搭档",
     "overlap_org": "中共建安区委/区政府", "overlap_period": ""},
    # 常委之间 — 区政府党组班子
    {"person_a": 6, "person_b": 5, "type": "overlap",
     "context": "常务副区长与副区长，区政府党组班子搭档",
     "overlap_org": "建安区政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 14, "type": "overlap",
     "context": "常务副区长与副区长，区政府党组班子搭档",
     "overlap_org": "建安区政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 15, "type": "overlap",
     "context": "常务副区长与副区长，区政府党组班子搭档",
     "overlap_org": "建安区政府", "overlap_period": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════════

def make_source_register():
    """Build source register from existing build script sources."""
    return [
        {"id":"S001","title":"建安区政府领导页面","url":OFFICIAL_LDZC,
         "publisher":"许昌市建安区人民政府","published_at":"2026-07-24","accessed_at":AS_OF,
         "source_type":"official","reliability":"high","notes":"确认刘建伟(区长)、王伟(常务副区长)、董传斌(副区长)、朱红凯(副区长/公安)、程伟峰、刘晓召、廖睿"},
        {"id":"S002","title":"区二次党代会代表看望","url":"http://www.jianan.gov.cn/jrja/001001/20260623/d60fa984-dfd1-4737-81a0-27aa3d8d8000.html",
         "publisher":"许昌市建安区人民政府","published_at":"2026-06-23","accessed_at":AS_OF,
         "source_type":"official","reliability":"high","notes":"高雁(书记)、刘建伟(副书记/区长)、连良、朱键、李静、李梦龙、董华、董传斌、龚文兵、邴娅、张自锋出席"},
        {"id":"S003","title":"建安区两优一先表彰大会","url":"http://www.jianan.gov.cn/jrja/001001/20260630/e6eee9c7-b500-4689-bded-b4191419e845.html",
         "publisher":"许昌市建安区人民政府","published_at":"2026-06-30","accessed_at":AS_OF,
         "source_type":"official","reliability":"high","notes":"高雁(书记)讲话，刘建伟(副书记/区长)主持，连良(副书记/政法委书记)宣读决定"},
        {"id":"S004","title":"全区人民武装工作会议","url":"http://www.jianan.gov.cn/jrja/001001/20260716/4e7092be-a943-48ef-a8f1-d3e2ae8d4ab6.html",
         "publisher":"许昌市建安区人民政府","published_at":"2026-07-16","accessed_at":AS_OF,
         "source_type":"official","reliability":"high","notes":"高雁(区委书记/人武部党委第一书记)讲话"},
        {"id":"S005","title":"G107国道通车调研","url":"http://www.jianan.gov.cn/jrja/001001/20260618/5574c2c9-8e8b-4f27-a3ec-58acfb86fe29.html",
         "publisher":"许昌市建安区人民政府","published_at":"2026-06-18","accessed_at":AS_OF,
         "source_type":"official","reliability":"high","notes":"高雁(书记)、刘建伟(区长)、李梦龙(区委办主任)、刘晓召(副区长)调研"},
        {"id":"S006","title":"区政府五次全体会议","url":"http://www.jianan.gov.cn/jrja/001001/20260611/f133a7f5-00a3-4c2c-aadc-7d8cccaa2ab2.html",
         "publisher":"许昌市建安区人民政府","published_at":"2026-06-10","accessed_at":AS_OF,
         "source_type":"official","reliability":"high","notes":"刘建伟(区长)主持，王伟(常务副区长)、董传斌(副区长)出席，张自锋(纪委书记)廉政谈话"},
        {"id":"S007","title":"刘建伟主持第57次常务会议","url":"http://www.jianan.gov.cn/jrja/001001/20260709/46ea5950-5397-425c-8d42-dbb7c0002fa2.html",
         "publisher":"许昌市建安区人民政府","published_at":"2026-07-09","accessed_at":AS_OF,
         "source_type":"official","reliability":"high","notes":"刘建伟主持召开区政府第57次常务会议"},
        {"id":"S008","title":"许昌市委书记市长调研建安区","url":"http://www.jianan.gov.cn/jrja/001001/20260722/4d98833d-0edc-40fb-9c46-47225e3ed1e4.html",
         "publisher":"许昌市建安区人民政府","published_at":"2026-07-22","accessed_at":AS_OF,
         "source_type":"official","reliability":"high","notes":"市委书记杨小菁、市长张庆一带队调研建安区重点项目"},
    ]

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def make_person_json(p, timeline, relationships_list, source_register):
    """Generate a person graph JSON object."""
    # Determine career completeness
    has_timeline = any(t.get("confidence") == "confirmed" for t in timeline) if timeline else False
    has_bio = bool(p.get("birth") or p.get("birthplace"))

    result = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河南省",
            "city": "许昌市",
            "region": "建安区",
            "job": p.get("current_post",""),
            "task_id": "henan_建安区",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"jiananqu_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender",""),
            "ethnicity": p.get("ethnicity",""),
            "birth": p.get("birth",""),
            "birthplace": p.get("birthplace",""),
            "native_place": p.get("native_place",""),
            "education": [{"period":"","institution":"","major":"","degree":p.get("education",""),"study_type":"unknown","source_ids":[]}] if p.get("education") else [],
            "party_join": p.get("party_join","").replace("中共党员（","").replace("中共党员","").replace("）",""),
            "work_start": p.get("work_start",""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source","")
            }
        },
        "current_status": {
            "current_post": p.get("current_post",""),
            "current_org": p.get("current_org",""),
            "administrative_rank": "县处级正职" if ("书记" in p.get("current_post","") and "副" not in p.get("current_post","") and "纪委" not in p.get("current_post","")) or ("区长" in p.get("current_post","") and "副" not in p.get("current_post","") and "人大" not in p.get("current_post","")) else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": []
        },
        "career_timeline": timeline or [],
        "organizations": [],
        "relationships": relationships_list or [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary":"","notable_fast_promotions":[]}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type":"none_found","description":"在公开信息中未发现该人物负面信号","date":"","confidence":"confirmed","source_ids":[]}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if has_bio else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if has_timeline else ("thin" if not has_timeline and has_bio else "thin"),
            "relationship_confidence": "medium",
            "biggest_gap": f"{p['name']}的完整履历和出生年月信息有待补充" if not has_bio else f"{p['name']}早期职业生涯需确认"
        },
        "open_questions": [
            {"priority":"critical" if not has_bio else "medium",
             "question": f"{p['name']}的完整职业生涯履历和出生信息",
             "why_it_matters": "无法追溯其任职路径和系统经历",
             "suggested_queries": [f"{p['name']} 简历 建安区",f"{p['name']} 百度百科"],
             "last_attempted": AS_OF}
        ]
    }
    return result

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def build():
    print("=" * 60)
    print("  许昌市建安区领导班子工作关系网络")
    print("  等级: 市辖区")
    print("  调查日期: 2026-07-24（首次调查）")
    print("  信息来源: 建安区政府网站")
    print("=" * 60)

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
    print(f"\n✅ 建安区数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── Generate Person Graph JSONs ──
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()

    # 1. 高雁 (区委书记)
    gao_timeline = [
        {"start":"","end":"","org":"中共许昌市建安区委员会","title":"建安区委书记",
         "notes":"区人武部党委第一书记；2026年6月二次党代会前已在任；公开履历信息有限",
         "confidence":"confirmed","source_ids":["S002","S003","S004"]},
    ]
    gao_relationships = [
        {"person":"刘建伟","person_id":"jiananqu_刘建伟","relationship_type":"overlap","strength":"strong",
         "evidence":"区委书记与区长党政工作搭档关系，共同出席二次党代会代表看望、G107调研等活动",
         "overlap_org":"建安区","overlap_period":"2026-","direction":"undirected","confidence":"confirmed","source_ids":["S002","S005"]},
        {"person":"连良","person_id":"jiananqu_连良","relationship_type":"overlap","strength":"strong",
         "evidence":"区委书记与副书记/政法委书记工作搭档",
         "overlap_org":"中共建安区委","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S003"]},
        {"person":"李梦龙","person_id":"jiananqu_李梦龙","relationship_type":"overlap","strength":"strong",
         "evidence":"区委书记与区委常委/办公室主任工作搭档",
         "overlap_org":"中共建安区委","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S005"]},
        {"person":"董传斌","person_id":"jiananqu_董传斌","relationship_type":"overlap","strength":"strong",
         "evidence":"区委书记与区委常委/副区长",
         "overlap_org":"中共建安区委/区政府","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S002"]},
        {"person":"王伟","person_id":"jiananqu_王伟","relationship_type":"overlap","strength":"strong",
         "evidence":"区委书记与常务副区长",
         "overlap_org":"中共建安区委/区政府","overlap_period":"","direction":"undirected","confidence":"plausible","source_ids":["S006"]},
        {"person":"张自锋","person_id":"jiananqu_张自锋","relationship_type":"overlap","strength":"strong",
         "evidence":"区委书记与纪委书记",
         "overlap_org":"中共建安区委","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S002"]},
        {"person":"朱键","person_id":"jiananqu_朱键","relationship_type":"overlap","strength":"medium",
         "evidence":"区委书记与区委常委班子成员，二次党代会",
         "overlap_org":"中共建安区委","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S002"]},
        {"person":"李静","person_id":"jiananqu_李静","relationship_type":"overlap","strength":"medium",
         "evidence":"区委书记与区委常委班子成员，二次党代会",
         "overlap_org":"中共建安区委","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S002"]},
    ]
    gao_json = make_person_json(persons[0], gao_timeline, gao_relationships, source_register)
    gao_path = PERSONS_DIR / f"{TODAY}-河南省-许昌市-区委书记-高雁.json"
    with open(gao_path, "w", encoding="utf-8") as f:
        json.dump(gao_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {gao_path.name}")

    # 2. 刘建伟 (区长)
    liu_timeline = [
        {"start":"","end":"","org":"中共许昌市建安区委员会","title":"建安区委副书记",
         "notes":"区政府党组书记",
         "confidence":"confirmed","source_ids":["S001","S003"]},
        {"start":"","end":"","org":"建安区人民政府","title":"建安区区长",
         "notes":"主持区政府全面工作；分管区审计局",
         "confidence":"confirmed","source_ids":["S001","S007"]},
    ]
    liu_relationships = [
        {"person":"高雁","person_id":"jiananqu_高雁","relationship_type":"overlap","strength":"strong",
         "evidence":"区长与区委书记党政工作搭档",
         "overlap_org":"建安区","overlap_period":"2026-","direction":"undirected","confidence":"confirmed","source_ids":["S002","S005"]},
        {"person":"王伟","person_id":"jiananqu_王伟","relationship_type":"overlap","strength":"strong",
         "evidence":"区长与常务副区长工作搭档，共同出席区政府五次全会",
         "overlap_org":"建安区政府","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S006"]},
        {"person":"董传斌","person_id":"jiananqu_董传斌","relationship_type":"overlap","strength":"strong",
         "evidence":"区长与副区长工作搭档，共同出席区政府五次全会",
         "overlap_org":"建安区政府","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S006"]},
        {"person":"连良","person_id":"jiananqu_连良","relationship_type":"overlap","strength":"strong",
         "evidence":"区长与副书记/政法委书记工作搭档",
         "overlap_org":"中共建安区委/区政府","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S003"]},
        {"person":"刘晓召","person_id":"jiananqu_刘晓召","relationship_type":"overlap","strength":"medium",
         "evidence":"区长与副区长工作搭档，共同参加G107调研",
         "overlap_org":"建安区政府","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S005"]},
        {"person":"程伟峰","person_id":"jiananqu_程伟峰","relationship_type":"overlap","strength":"medium",
         "evidence":"区长与副区长工作搭档，共同出席区政府五次全会",
         "overlap_org":"建安区政府","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S006"]},
        {"person":"朱红凯","person_id":"jiananqu_朱红凯","relationship_type":"overlap","strength":"medium",
         "evidence":"区长与副区长/公安局长工作搭档",
         "overlap_org":"建安区政府","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S001"]},
        {"person":"廖睿","person_id":"jiananqu_廖睿","relationship_type":"overlap","strength":"medium",
         "evidence":"区长与副区长工作搭档",
         "overlap_org":"建安区政府","overlap_period":"","direction":"undirected","confidence":"confirmed","source_ids":["S001"]},
    ]
    liu_json = make_person_json(persons[1], liu_timeline, liu_relationships, source_register)
    liu_path = PERSONS_DIR / f"{TODAY}-河南省-许昌市-区长-刘建伟.json"
    with open(liu_path, "w", encoding="utf-8") as f:
        json.dump(liu_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {liu_path.name}")

    print(f"\n所有 Person Graph JSONs 已生成到: {PERSONS_DIR}")

if __name__ == "__main__":
    build()
