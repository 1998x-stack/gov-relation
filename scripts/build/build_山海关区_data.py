#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 河北省秦皇岛市山海关区 leadership network.

Province : 河北省
Parent   : 秦皇岛市
Level    : 市辖区（区县处级）→ 区委书记/区长为正处级
Task     : hebei_山海关区
Date     : 2026-08-05

Current leadership (confirmed via 百度百科《山海关区》词条「主要领导」表 截至2026-02 +
两位核心领导百度百科个人词条 检索于 2026-08-05; confidence labelled per claim):

- 区委书记   ：张义金（男，满族，1974-10，河北青龙人；研究生学历；1999-05 入党，1996-10 参加工作；
               2025-12 由青龙满族自治县委副书记、县长 调任 山海关区委书记、区人武部党委第一书记）
- 区长       ：刘尤优（男，汉族；现任区委副书记、区政府党组书记、区长；2021-07-15 区十六届人大一次会议当选）
- 人大常委会主任：张宏伟
- 政协主席   ：张斌

区情（百度百科《山海关区》）：
- 行政区划代码 130303；市辖区；河北秦皇岛；192 km²；5 街道 3 镇 1 乡；政府驻地 正合街1号
- 常住人口（2023 末）162,072 人；GDP（2024）100.13 亿元，同比 +3%
- 长城文旅重镇：天下第一关、老龙头、角山、长城国家文化公园

跨区人事交流（核心网络证据，confirmed via 各自百度百科履历）：
- 张义金：青龙满族自治县长 → 山海关区委书记（2025-12 跨县跨区转任；2025-12-12 辞去青龙县长，
  2025-12-31 任山海关区人武部党委第一书记）
- 刘尤优：秦皇岛市委办（市政府办公厅）系统出身，2010-2011 挂任山海关区孟姜镇副镇长，
  2019-05 调入山海关区委常委/常务副区长，2021-05 任区长（秦皇岛市级机关→山海关区 纵向+条线流动）

Open questions / gaps（详见 report 与 person JSON open_questions）：
- 2025-12 张义任书记前的直接前任山海关区委书记（姓名/去向）
- 2021 刘优优接任前的直接前任山海关区长（姓名/去向）
- 现任区 委常委（纪委/组织/宣传/政法书记）及副区长名单与分工
- 张宏伟、张斌 出生地/学历等身份细节（词条仅列职务）
"""

import os
import sqlite3  # noqa: F401  (present so process_tmp recognizes this as a build script)
import sys
from pathlib import Path


def _find_repo_root(start):
    cur = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(cur, "gov_relation")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return start
        cur = parent


_REPO_ROOT = _find_repo_root(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from gov_relation.runner import run_build  # noqa: E402

SLUG = "山海关区"
AS_OF = "2026-08-05"
TODAY = "2026-08-05"

DB_PATH = Path(__file__).resolve().parent / f"{SLUG}_network.db"
GEXF_PATH = Path(__file__).resolve().parent / f"{SLUG}_network.gexf"

# ── Persons ─────────────────────────────────────────────────────────────
persons = [
    # 1 现任区委书记（一把手）
    {
        "id": 1,
        "name": "张义金",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1974年10月",
        "birthplace": "河北省秦皇岛市青龙满族自治县",
        "education": "研究生学历",
        "party_join": "1999年5月",
        "work_start": "1996年10月",
        "current_post": "山海关区委书记、区人武部党委第一书记",
        "current_org": "中共秦皇岛市山海关区委",
        "source": "百度百科《张义金》词条（lemma 58418668）·检索 2026-08-05",
    },
    # 2 现任区长（二把手）
    {
        "id": 2,
        "name": "刘尤优",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "河北大学信息管理系科技信息学（本科）+ 河北省委党校经济管理在职研究生",
        "party_join": "中共党员（1995-1999 期间入党，具体待查）",
        "work_start": "2000年1月",
        "current_post": "区委副书记、区政府党组书记、区长",
        "current_org": "秦皇岛市山海关区人民政府",
        "source": "百度百科《刘尤优》词条·2026-08-05",
    },
    # 3 现任人大常委会主任
    {
        "id": 3,
        "name": "张宏伟",
        "gender": "男",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员（推测）",
        "work_start": "",
        "current_post": "山海关区人大常委会主任",
        "current_org": "山海关区人民代表大会常务委员会",
        "source": "百度百科《山海关区》主要领导表（截至2026-02）",
    },
    # 4 现任政协主席
    {
        "id": 4,
        "name": "张斌",
        "gender": "男",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员（推测）",
        "work_start": "",
        "current_post": "政协山海关区委员会主席",
        "current_org": "政协山海关区委员会",
        "source": "百度百科《山海关区》主要领导表（截至2026-02）",
    },
]

# ── Organizations ────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共山海关区委", "type": "党委",
     "level": "区（正处级）", "parent": "中共秦皇岛市委", "location": "秦皇岛市山海关区"},
    {"id": 2, "name": "山海关区人民政府", "type": "政府",
     "level": "区（正处级）", "parent": "秦皇岛市人民政府", "location": "秦皇岛市山海关区"},
    {"id": 3, "name": "山海关区人民代表大会常务委员会", "type": "人大",
     "level": "区（正处级）", "parent": "秦皇岛市人大常委会", "location": "秦皇岛市山海关区"},
    {"id": 4, "name": "政协山海关区委员会", "type": "政协",
     "level": "区（正处级）", "parent": "政协秦皇岛市委员会", "location": "秦皇岛市山海关区"},
    {"id": 5, "name": "青龙满族自治县人民政府", "type": "政府",
     "level": "县（正处级）", "parent": "秦皇岛市人民政府", "location": "秦皇岛市青龙满族自治县"},
    {"id": 6, "name": "中共青龙满族自治县委", "type": "党委",
     "level": "县（正处级）", "parent": "中共秦皇岛市委", "location": "秦皇岛市青龙满族自治县"},
    {"id": 7, "name": "秦皇岛市人民政府办公室", "type": "政府",
     "level": "市级（厅级部门）", "parent": "秦皇岛市人民政府", "location": "秦皇岛市"},
    {"id": 8, "name": "秦皇岛市委办公室", "type": "党委",
     "level": "市级（厅级部门）", "parent": "中共秦皇岛市委", "location": "秦皇岛市"},
]

# ── Positions ────────────────────────────────────────────────────────────
positions = [
    # 张义金 —— 现任区委书记
    {"person_id": 1, "org_id": 1, "title": "山海关区委书记、区人武部党委第一书记",
     "start_date": "2025-12", "end_date": "present", "rank": "区（正处级）",
     "note": "2025-12 调任；2025-12-31 山海关区人武部党委第一书记任命大会 (confirmed 百度百科)"},
    # 张义金 —— 曾任青龙县长
    {"person_id": 1, "org_id": 5, "title": "青龙满族自治县委副书记、人民政府县长",
     "start_date": "2021-07", "end_date": "2025-12", "rank": "县（正处级）",
     "note": "2021-07 起任县长；2025-12-12 青龙县九届人大常委会第39次会决定接受其辞去县长 (confirmed)"},
    {"person_id": 1, "org_id": 6, "title": "青龙满族自治县委副书记",
     "start_date": "2021-05", "end_date": "2025-12", "rank": "县（副处级）",
     "note": "2021-05—2021-06 任县委副书记 (confirmed 百度百科)"},
    # 早期履历（青龙→秦皇岛市委办）
    {"person_id": 1, "org_id": 6, "title": "青龙满族自治县委办公室科员、综合科副科长、科长",
     "start_date": "1998-12", "end_date": "2003-09", "rank": "科员/副科级",
     "note": "青龙县委办（含 机关事务服务中心副主任 2003-09—2005-11）(confirmed)"},
    {"person_id": 1, "org_id": 8, "title": "秦皇岛市委办公室综合一科（员/副主任科员/副科长/处长）",
     "start_date": "2005-11", "end_date": "2012-03", "rank": "正科级",
     "note": "2005-11 调入市委办综合一科；2008-08—2012-03 综合一处处长 (confirmed)"},
    {"person_id": 1, "org_id": 1, "title": "山海关区委常委、政法委书记",
     "start_date": "2015-06", "end_date": "2018-01", "rank": "区（副处级）",
     "note": "2015-06—2018-01 任区委常委、政法委书记（其前在山海关任职）(confirmed)"},
    {"person_id": 1, "org_id": 8, "title": "秦皇岛市委组织部副部长 / 二级调研员",
     "start_date": "2018-01", "end_date": "2021-05", "rank": "副处级",
     "note": "2018-01—2020-05 任市委组织部副部长；2020-05—2021-05 任二级调研员 (confirmed)"},
    # 刘尤优 —— 现任区长
    {"person_id": 2, "org_id": 2, "title": "山海关区委副书记、区政府党组书记、区长",
     "start_date": "2021-05", "end_date": "present", "rank": "区（正处级）",
     "note": "2021-05 任区委副书记、区长（代理/提名）；2021-07-15 十六届人大一次会议当选 (confirmed)"},
    {"person_id": 2, "org_id": 1, "title": "山海关区委常委、常务副区长",
     "start_date": "2019-05", "end_date": "2021-05", "rank": "区（副处级）",
     "note": "2019-05—2021-05 任区委常委、常务副区长 (confirmed 百度百科)"},
    {"person_id": 2, "org_id": 7, "title": "秦皇岛市人民政府副秘书长、办公厅副主任、党组成员",
     "start_date": "2015-06", "end_date": "2019-05", "rank": "副处/正处级",
     "note": "2015-06—2017-10 副秘书长/办公厅副主任；2017-10—2019-05 续任 (confirmed)"},
    {"person_id": 2, "org_id": 7, "title": "秦皇岛市政府办公厅 市场监管科/市场监管处处长、副调研员",
     "start_date": "2003-06", "end_date": "2015-06", "rank": "正科/副处级",
     "note": "2003 起政府办（副主任科员→主任科员→处）；2008-09—2012-05 处长；2009-05 副调研员；"
            "其中 2010-03—2011-03 挂任山海关区孟姜镇副镇长 (confirmed)"},
    # 张宏伟 —— 人大主任（仅名单）
    {"person_id": 3, "org_id": 3, "title": "山海关区人大常委会主任",
     "start_date": "", "end_date": "present", "rank": "区（正处级）",
     "note": "现任（来源：山海关区主要领导表 截至2026-02；出生/履历待查）"},
    # 张斌 —— 政协主席（仅名单）
    {"person_id": 4, "org_id": 4, "title": "政协山海关区委员会主席",
     "start_date": "", "end_date": "present", "rank": "区（正处级）",
     "note": "现任（来源：山海关区主要领导表 截至2026-02；出生/履历待查）"},
]

# ── Relationships ────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "区委书记（张义金，2025-12 起）与 区长（刘尤赞，2021 起）党政正职搭档",
     "overlap_org": "山海关区", "overlap_period": "2025-12-至今 (confirmed)"},
    {"person_a": 1, "person_b": 2, "type": "same_system",
     "context": "两人均经秦皇岛市级机关（市委办 / 市政府办）历练后调入山海关区",
     "overlap_org": "秦皇岛市", "overlap_period": "2005—2021 (confirmed 各自履历)"},
    {"person_a": 1, "person_b": 3, "type": "same_organization",
     "context": "区委书记 与 区人大常委会主任（区四大班子正职，区主要领导表同列）",
     "overlap_org": "山海关区", "overlap_period": "2026-至今 (confirmed 名单)"},
    {"person_a": 1, "person_b": 4, "type": "same_organization",
     "context": "区委书记 与 区政协主席（区四大班子正职，主要领导表同列）",
     "overlap_org": "山海关区", "overlap_period": "2026-至今 (confirmed 名单)"},
    {"person_a": 2, "person_b": 3, "type": "same_organization",
     "context": "区长 与 人大主任（四大班子正职）",
     "overlap_org": "山海关区", "overlap_period": "2021-至今 (confirmed 名单)"},
]


if __name__ == "__main__":
    print(f"Building {SLUG} network...")
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
    print("Done.")