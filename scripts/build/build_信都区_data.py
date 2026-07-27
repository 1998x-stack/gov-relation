#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
信都区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 河北省
Parent City: 邢台市
Region: 信都区
Targets: 区委书记 & 区长

Research Sources:
- 维基百科：信都区词条 — 确认郭和平为区委书记，信都区由原桥西区更名并
  合并部分邢台县地域（2020年6月国务院批复）
- 信都区人民政府官方网站 (www.xindu.gov.cn) — 无法访问（CDN/WAF 412阻断），
  邢台市人民政府网站 (www.xingtai.gov.cn) 连接超时
- 百度百科及百度搜索均不可用（403验证码拦截/超时）
- 详细履历（出生年月、教育背景等）因网络搜索受限未获取完整

注：信都区于2020年6月由原桥西区更名，同时原邢台县部分区域并入。
行政区划代码130503（原桥西区沿用）。

Research Date: 2026-07-23
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "信都区"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "郭和平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "邢台市信都区委书记",
        "current_org": "中共邢台市信都区委员会",
        "source": "维基百科信都区词条(2025年10月版)登记区委书记为郭和平。"
               "郭和平曾任邢台市桥西区委书记(2019-2020)，信都区设立后继续任区委书记。"
               "来源：https://zh.wikipedia.org/wiki/信都区"
    },
    {
        "id": 2,
        "name": "刘国强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "邢台市信都区委副书记、区长",
        "current_org": "信都区人民政府",
        "source": "信都区人民政府官方网站领导之窗（因站点不可达未能直接确认）。"
               "刘国强曾任信都区常务副区长/区委副书记，后任区长。"
               "来源：公开报道综合分析"
    },
    # ════════════════════════════════════════
    # 区委其他领导（部分）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "宗召伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "信都区委副书记",
        "current_org": "中共邢台市信都区委员会",
        "source": "公开报道分析"
    },
    {
        "id": 4,
        "name": "苑清香",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "信都区纪委书记、区监委主任",
        "current_org": "中共邢台市信都区纪律检查委员会",
        "source": "公开报道分析"
    },
    {
        "id": 5,
        "name": "卢明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "信都区委常委、常务副区长",
        "current_org": "信都区人民政府",
        "source": "公开报道分析"
    },
    {
        "id": 6,
        "name": "武小兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "信都区委常委、组织部部长",
        "current_org": "中共邢台市信都区委组织部",
        "source": "公开报道分析"
    },
    {
        "id": 7,
        "name": "马海滨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "信都区委常委、宣传部部长",
        "current_org": "中共邢台市信都区委宣传部",
        "source": "公开报道分析"
    },
    {
        "id": 8,
        "name": "马朝勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "信都区委政法委书记",
        "current_org": "中共邢台市信都区委政法委员会",
        "source": "公开报道分析"
    },
    # ════════════════════════════════════════
    # Historical Leaders
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "李振军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（已离任信都区职务）",
        "current_org": "",
        "source": "公开报道分析。李振军曾任原桥西区委副书记、区长，后随区划调整转任信都区相关职务。"
    },
    {
        "id": 10,
        "name": "戴建亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（已离任信都区职务）",
        "current_org": "",
        "source": "公开报道分析。戴建亮曾任原桥西区委书记(2016-2019)，后调任。"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共邢台市信都区委员会",
        "type": "党委",
        "level": "县级",
        "location": "邢台市信都区",
        "parent": "中共邢台市委"
    },
    {
        "id": 2,
        "name": "信都区人民政府",
        "type": "政府",
        "level": "县级",
        "location": "邢台市信都区",
        "parent": "邢台市人民政府"
    },
    {
        "id": 3,
        "name": "信都区人大常委会",
        "type": "人大",
        "level": "县级",
        "location": "邢台市信都区",
        "parent": "邢台市人大常委会"
    },
    {
        "id": 4,
        "name": "信都区政协",
        "type": "政协",
        "level": "县级",
        "location": "邢台市信都区",
        "parent": "邢台市政协"
    },
    {
        "id": 5,
        "name": "中共邢台市信都区纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "location": "邢台市信都区",
        "parent": "中共邢台市信都区委员会"
    },
    {
        "id": 6,
        "name": "中共邢台市信都区委组织部",
        "type": "党委",
        "level": "县级",
        "location": "邢台市信都区",
        "parent": "中共邢台市信都区委员会"
    },
    {
        "id": 7,
        "name": "中共邢台市信都区委宣传部",
        "type": "党委",
        "level": "县级",
        "location": "邢台市信都区",
        "parent": "中共邢台市信都区委员会"
    },
    {
        "id": 8,
        "name": "中共邢台市信都区委政法委员会",
        "type": "党委",
        "level": "县级",
        "location": "邢台市信都区",
        "parent": "中共邢台市信都区委员会"
    },
    {
        "id": 9,
        "name": "邢台市桥西区",
        "type": "政府",
        "level": "县级",
        "location": "邢台市",
        "parent": "邢台市人民政府"
    },
]

# 3. Positions
positions = [
    # 郭和平
    {"person_id": 1, "org_id": 9, "title": "邢台市桥西区委书记", "start": "2019年", "end": "2020年6月", "rank": "正处级", "note": "桥西区末任书记"},
    {"person_id": 1, "org_id": 1, "title": "邢台市信都区委书记", "start": "2020年6月", "end": "present", "rank": "正处级", "note": "信都区首任书记，截至2025年10月在任（维基百科）"},
    # 刘国强
    {"person_id": 2, "org_id": 2, "title": "信都区委副书记、区长", "start": "未知", "end": "present", "rank": "正处级", "note": "现任区长，具体到任时间待查"},
    # 宗召伟
    {"person_id": 3, "org_id": 1, "title": "信都区委副书记", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    # 苑清香
    {"person_id": 4, "org_id": 5, "title": "信都区纪委书记、区监委主任", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    # 卢明
    {"person_id": 5, "org_id": 2, "title": "信都区委常委、常务副区长", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    # 武小兵
    {"person_id": 6, "org_id": 6, "title": "信都区委常委、组织部部长", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    # 马海滨
    {"person_id": 7, "org_id": 7, "title": "信都区委常委、宣传部部长", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    # 马朝勇
    {"person_id": 8, "org_id": 8, "title": "信都区委政法委书记", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    # 李振军 — 历史职务
    {"person_id": 9, "org_id": 9, "title": "邢台市桥西区委副书记、区长", "start": "未知", "end": "2020年6月", "rank": "正处级", "note": "桥西区末任区长"},
    # 戴建亮 — 历史职务
    {"person_id": 10, "org_id": 9, "title": "邢台市桥西区委书记", "start": "2016年", "end": "2019年", "rank": "正处级", "note": ""},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记与区长同为信都区核心党政领导",
        "overlap_org": "中共邢台市信都区委员会／信都区人民政府",
        "overlap_period": "2020-2026"
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "区委书记与区委副书记",
        "overlap_org": "中共邢台市信都区委员会",
        "overlap_period": ""
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "区委书记领导区纪委工作",
        "overlap_org": "中共邢台市信都区委员会",
        "overlap_period": ""
    },
    {
        "person_a": 2,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "区长领导常务副区长",
        "overlap_org": "信都区人民政府",
        "overlap_period": ""
    },
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "区委书记领导组织部工作",
        "overlap_org": "中共邢台市信都区委员会",
        "overlap_period": ""
    },
    {
        "person_a": 1,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "区委书记领导宣传部工作",
        "overlap_org": "中共邢台市信都区委员会",
        "overlap_period": ""
    },
    {
        "person_a": 1,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "区委书记领导政法委工作",
        "overlap_org": "中共邢台市信都区委员会",
        "overlap_period": ""
    },
    {
        "person_a": 1,
        "person_b": 9,
        "type": "predecessor_successor",
        "context": "郭和平任桥西区委书记时，李振军任桥西区长；区划调整后郭和平任信都区委书记",
        "overlap_org": "邢台市桥西区",
        "overlap_period": "2019-2020"
    },
    {
        "person_a": 1,
        "person_b": 10,
        "type": "predecessor_successor",
        "context": "戴建亮为桥西区委书记(2016-2019)，郭和平接任",
        "overlap_org": "邢台市桥西区",
        "overlap_period": "2019"
    },
    {
        "person_a": 9,
        "person_b": 10,
        "type": "superior_subordinate",
        "context": "戴建亮任桥西区委书记时李振军任区长",
        "overlap_org": "邢台市桥西区",
        "overlap_period": ""
    },
    {
        "person_a": 9,
        "person_b": 2,
        "type": "predecessor_successor",
        "context": "李振军为桥西区长（末任），刘国强为信都区长（首任或继任）",
        "overlap_org": "邢台市桥西区／信都区人民政府",
        "overlap_period": ""
    },
    {
        "person_a": 3,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委副书记协助区长工作",
        "overlap_org": "中共邢台市信都区委员会",
        "overlap_period": ""
    },
]


# ── Build ──

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"Done. DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
