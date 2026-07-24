#!/usr/bin/env python3
"""Build 张家口市桥西区 (Zhangjiakou Qiaoxi District) leadership network data.

Level: 市辖区
Province: 河北省
Parent city: 张家口市
Targets: 区委书记 (Party Secretary), 区长 (Mayor)
Task ID: hebei_桥西区

Research date: 2026-07-24
Official source: http://www.zjkqxq.gov.cn/ (张家口市桥西区人民政府)

Current status (as of 2026-07-24):
- 区委书记: 左克平 — 2026年6月前后由区长转任区委书记；
  7月1日以区委书记身份出席全区"两优一先"表彰大会；
  7月18日区第十二次党代会代表十一届区委作报告，7月19日主持闭幕大会，连任
- 区长: 戈录伟 — 新任区长，7月18日第十二次党代会执行主席并主持开幕式
- 前任区委书记: 尚秀伟 — 至少在2026年5月13日仍为区委书记，后调离

Key source pages:
- http://www.zjkqxq.gov.cn/single/98/45066.html (左克平任区长时页面)
- http://www.zjkqxq.gov.cn/single/12/96126.html (第十二次党代会开幕)
- http://www.zjkqxq.gov.cn/single/11/96120.html (第十二次党代会闭幕)
- http://www.zjkqxq.gov.cn/single/22/96118.html (纪委第一次全会)
- http://www.zjkqxq.gov.cn/single/22/96017.html (两优一先表彰大会)
- http://www.zjkqxq.gov.cn/single/22/94810.html (冬春招商座谈会, 尚秀伟+左克平)
- http://www.zjkqxq.gov.cn/single/22/95505.html (尚秀伟5月仍为书记)
"""

from __future__ import annotations

import sys
from pathlib import Path

# When run from data/tmp/hebei_桥西区/, resolve repo root three levels up
_SCRIPT_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPT_DIR.parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "桥西区"

_STAGING_DIR = _SCRIPT_DIR  # data/tmp/hebei_桥西区/
DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 区委领导 (Party Committee)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "左克平",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桥西区委书记",
        "current_org": "中共张家口市桥西区委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/11/96120.html "
                    "(第十二次党代会闭幕, 左克平主持); "
                    "http://www.zjkqxq.gov.cn/single/22/96017.html "
                    "(7月1日两优一先表彰, 首次以书记身份出现)"),
    },
    {
        "id": 2,
        "name": "戈录伟",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桥西区委副书记、区长",
        "current_org": "桥西区人民政府",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/12/96126.html "
                    "(第十二次党代会开幕, 戈录伟主持)"),
    },
    {
        "id": 3,
        "name": "吉树强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共张家口市桥西区委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/12/96126.html "
                    "(十二次党代会主席团成员/执行主席)"),
    },
    {
        "id": 4,
        "name": "胡海飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共张家口市桥西区委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/12/96126.html "
                    "(十二次党代会主席团成员/执行主席)"),
    },
    {
        "id": 5,
        "name": "马玉红",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共张家口市桥西区委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/12/96126.html "
                    "(十二次党代会主席团成员/执行主席)"),
    },
    {
        "id": 6,
        "name": "杨建章",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共张家口市桥西区委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/12/96126.html "
                    "(十二次党代会主席团成员/执行主席)"),
    },
    {
        "id": 7,
        "name": "孙丹峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区纪委书记",
        "current_org": "中共张家口市桥西区纪律检查委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/22/96118.html "
                    "(十二届纪委第一次全体会议, 孙丹峰当选书记)"),
    },
    {
        "id": 8,
        "name": "卢宗生",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共张家口市桥西区委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/12/96126.html "
                    "(十二次党代会主席团成员/执行主席)"),
    },
    {
        "id": 9,
        "name": "李艳娇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共张家口市桥西区委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/12/96126.html "
                    "(十二次党代会主席团成员/执行主席)"),
    },
    {
        "id": 10,
        "name": "刘建",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共张家口市桥西区委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/12/96126.html "
                    "(十二次党代会主席团成员/执行主席)"),
    },
    {
        "id": 11,
        "name": "刘海军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共张家口市桥西区委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/12/96126.html "
                    "(十二次党代会主席团成员, 在主席台就座)"),
    },
    {
        "id": 12,
        "name": "杨巍洁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "桥西区人民政府",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/98/45063.html "
                    "(常务副区长分工及履历); "
                    "http://www.zjkqxq.gov.cn/single/22/94810.html "
                    "(以区领导身份参加招商座谈会)"),
    },
    # ════════════════════════════════════════
    # 区政府领导 (Government Leadership)
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "黄向义",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "桥西区人民政府",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/98/55582.html "
                    "(副区长分工及履历)"),
    },
    {
        "id": 14,
        "name": "陈建民",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、公安分局局长",
        "current_org": "桥西区人民政府",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/98/45062.html "
                    "(副区长分工及履历)"),
    },
    {
        "id": 15,
        "name": "王平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "桥西区人民政府",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/98/60237.html "
                    "(副区长分工及履历)"),
    },
    {
        "id": 16,
        "name": "倪明远",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "桥西区人民政府",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/98/55577.html "
                    "(副区长分工及履历)"),
    },
    {
        "id": 17,
        "name": "王则栋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "桥西区人民政府",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/98/45061.html "
                    "(副区长分工及履历)"),
    },
    {
        "id": 18,
        "name": "尚秀伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任桥西区委书记（已离任）",
        "current_org": "待查",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/22/96017.html "
                    "(2026年7月前为区委书记; "
                    "http://www.zjkqxq.gov.cn/single/22/95505.html 5月13日仍主持学习会议)"),
    },
    {
        "id": 19,
        "name": "李明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "待查",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/22/94810.html "
                    "(2026年2月冬春招商座谈会以区领导身份参加)"),
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共张家口市桥西区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共张家口市委员会",
        "location": "河北省张家口市桥西区",
    },
    {
        "id": 2,
        "name": "桥西区人民政府",
        "type": "政府",
        "level": "市辖区",
        "parent": "张家口市人民政府",
        "location": "河北省张家口市桥西区",
    },
    {
        "id": 3,
        "name": "中共张家口市桥西区纪律检查委员会",
        "type": "纪委",
        "level": "市辖区",
        "parent": "中共张家口市纪律检查委员会",
        "location": "河北省张家口市桥西区",
    },
    {
        "id": 4,
        "name": "桥西区人大常委会",
        "type": "人大",
        "level": "市辖区",
        "parent": "张家口市人大常委会",
        "location": "河北省张家口市桥西区",
    },
    {
        "id": 5,
        "name": "政协桥西区委员会",
        "type": "政协",
        "level": "市辖区",
        "parent": "政协张家口市委员会",
        "location": "河北省张家口市桥西区",
    },
    {
        "id": 6,
        "name": "张家口市公安局桥西分局",
        "type": "政府",
        "level": "区直部门",
        "parent": "张家口市公安局",
        "location": "河北省张家口市桥西区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 区委领导
    {"person_id": 1, "org_id": 1, "title": "桥西区委书记", "start": "2026-06", "end": "至今", "rank": "正处级", "note": "2026年6月前后由区长转任；7月第十二次党代会连任"},
    {"person_id": 1, "org_id": 2, "title": "桥西区区长", "start": "", "end": "2026-06", "rank": "正处级", "note": "2026年2月仍为区长；任区长起始时间待查"},
    {"person_id": 1, "org_id": 1, "title": "桥西区委副书记", "start": "", "end": "2026-06", "rank": "副处级", "note": "区长同时任区委副书记"},
    {"person_id": 2, "org_id": 2, "title": "桥西区区长", "start": "2026-07", "end": "至今", "rank": "正处级", "note": "第十二次党代会执行主席并主持开幕式"},
    {"person_id": 2, "org_id": 1, "title": "桥西区委副书记", "start": "2026-07", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": "十二次党代会执行主席"},
    {"person_id": 4, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": "十二次党代会执行主席"},
    {"person_id": 5, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": "十二次党代会执行主席"},
    {"person_id": 6, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": "十二次党代会执行主席"},
    {"person_id": 7, "org_id": 3, "title": "桥西区纪委书记", "start": "", "end": "至今", "rank": "副处级", "note": "十二届纪委第一次全会当选；受主席团委托主持会议"},
    {"person_id": 7, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": "十二次党代会执行主席"},
    {"person_id": 9, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": "十二次党代会执行主席"},
    {"person_id": 10, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": "十二次党代会执行主席"},
    {"person_id": 11, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": "十二次党代会主席团成员，在主席台就座"},
    {"person_id": 12, "org_id": 2, "title": "桥西区常务副区长", "start": "", "end": "至今", "rank": "副处级", "note": "区委常委、区政府党组副书记"},
    {"person_id": 12, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": "主席台就座"},
    # 区政府领导
    {"person_id": 13, "org_id": 2, "title": "桥西区副区长", "start": "", "end": "至今", "rank": "副处级", "note": "区政府党组成员；招商引资、商务、工信、园区建设等"},
    {"person_id": 14, "org_id": 2, "title": "桥西区副区长", "start": "", "end": "至今", "rank": "副处级", "note": "区政府党组成员，兼公安分局局长"},
    {"person_id": 14, "org_id": 6, "title": "桥西公安分局局长", "start": "", "end": "至今", "rank": "正科级", "note": "党委书记、局长、督察长"},
    {"person_id": 15, "org_id": 2, "title": "桥西区副区长", "start": "", "end": "至今", "rank": "副处级", "note": "区政府党组成员；农业农村、林业、水务、生态环境等"},
    {"person_id": 16, "org_id": 2, "title": "桥西区副区长", "start": "", "end": "至今", "rank": "副处级", "note": "市场监管、教育体育科技、卫生健康、文旅等"},
    {"person_id": 17, "org_id": 2, "title": "桥西区副区长", "start": "", "end": "至今", "rank": "副处级", "note": "区政府党组成员；住建、城管、自然资源规划等"},
    # 前任领导
    {"person_id": 18, "org_id": 1, "title": "桥西区委书记", "start": "", "end": "2026-06", "rank": "正处级", "note": "2026年5月13日仍为书记；约6月离任；去向待查"},
    # 其他区领导
    {"person_id": 19, "org_id": 1, "title": "区领导", "start": "", "end": "至今", "rank": "", "note": "2026年2月参加冬春招商座谈会; 具体职务待查"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "区委书记与区长党政工作搭档关系，共同担任第十二次党代会执行主席", "overlap_org": "桥西区", "overlap_period": "2026-"},
    # 区委常委班子
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "区委书记与区委常委班子成员", "overlap_org": "中共桥西区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "区委书记与区委常委班子成员", "overlap_org": "中共桥西区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "区委书记与区委常委班子成员", "overlap_org": "中共桥西区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "区委书记与区委常委班子成员", "overlap_org": "中共桥西区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "区委书记与纪委书记", "overlap_org": "中共桥西区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "区委书记与区委常委班子成员", "overlap_org": "中共桥西区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "区委书记与区委常委班子成员", "overlap_org": "中共桥西区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "区委书记与区委常委班子成员", "overlap_org": "中共桥西区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "区委书记与区委常委班子成员", "overlap_org": "中共桥西区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "区委书记与常务副区长", "overlap_org": "中共桥西区委/区政府", "overlap_period": ""},
    # 前任与继任
    {"person_a": 1, "person_b": 18, "type": "predecessor_successor", "context": "左克平接替尚秀伟任桥西区委书记", "overlap_org": "中共桥西区委", "overlap_period": "2026-06"},
    # 区长与副区长
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "区长与常务副区长工作搭档", "overlap_org": "桥西区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "区长与副区长工作搭档", "overlap_org": "桥西区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "区长与副区长工作搭档", "overlap_org": "桥西区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "区长与副区长工作搭档", "overlap_org": "桥西区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "overlap", "context": "区长与副区长工作搭档", "overlap_org": "桥西区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 17, "type": "overlap", "context": "区长与副区长工作搭档", "overlap_org": "桥西区政府", "overlap_period": ""},
    # 前任区委书记与副区长（共事时期）
    {"person_a": 18, "person_b": 1, "type": "superior_subordinate", "context": "尚秀伟为区委书记时，左克平为区长", "overlap_org": "中共桥西区委/区政府", "overlap_period": "至2026-06"},
    {"person_a": 18, "person_b": 12, "type": "overlap", "context": "前任书记与常务副区长", "overlap_org": "中共桥西区委", "overlap_period": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  张家口市桥西区领导班子工作关系网络")
    print("  等级: 市辖区")
    print("  调查日期: 2026-07-24")
    print("  信息来源: 桥西区政府网站 www.zjkqxq.gov.cn")
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
    print(f"\n✅ 桥西区数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")
