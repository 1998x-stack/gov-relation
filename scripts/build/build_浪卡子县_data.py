#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浪卡子县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 西藏自治区
Parent City: 山南市
Region: 浪卡子县
Targets: 县委书记 & 县长

Research Sources:
- 浪卡子县人民政府官网 (www.langkazi.gov.cn):
  - 普布扎西（县长）个人页面: http://www.langkazi.gov.cn/zwgk/ldzc/201901/t20190115_10404.html
  - "县委书记罗云主持召开十一届县委常委会会议": http://www.langkazi.gov.cn/xwzx/lkzyw/202607/t20260717_173670.html
  - "县委书记罗云主持召开十届县委常委会会议": http://www.langkazi.gov.cn/xwzx/lkzyw/202601/t20260127_163866.html
  - "罗云深入打隆镇调研指导防汛工作": http://www.langkazi.gov.cn/xwzx/lkzyw/202606/t20260617_171264.html
  - "普布扎西主持召开浪卡子县十五届人民政府第一次党组会议": http://www.langkazi.gov.cn/xwzx/lkzyw/202607/t20260731_174145.html
  - "罗云带队开展'三大节日'慰问活动": http://www.langkazi.gov.cn/xwzx/lkzyw/202601/t20260115_163217.html
  - "县委书记罗云督导食品安全工作": 出自动政府网站领导活动栏目2026-01-13

Research Date: 2026-08-03

Gaps:
- 县委书记罗云的出生年月、民族、籍贯、学历、完整履历暂缺（县委领导简历通常不在政府网站上公布）
- 领导班子其他成员（白玛维色、孙益民、边巴次仁、梅国斌、尼玛、布琼次仁、元旦）的具体职务分工暂缺
- 前任县委书记信息暂缺
- 纪委书记、组织部长、宣传部长、统战部长、政法委书记等常委暂缺
- 人大常委会主任、政协主席姓名暂缺
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "浪卡子县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "罗云",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "浪卡子县委书记",
        "current_org": "中共浪卡子县委员会",
        "source": "浪卡子县人民政府官网新闻：'县委书记罗云'多次出现在2026年的公开报道中。来源：http://www.langkazi.gov.cn/xwzx/lkzyw/202607/t20260717_173670.html — '罗云主持召开十一届县委常委会会议'"
    },
    {
        "id": 2,
        "name": "普布扎西",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1978年2月",
        "birthplace": "西藏岗巴",
        "education": "研究生学历",
        "party_join": "2004年12月",
        "work_start": "2002年7月",
        "current_post": "浪卡子县委副书记、县长",
        "current_org": "浪卡子县人民政府",
        "source": "http://www.langkazi.gov.cn/zwgk/ldzc/201901/t20190115_10404.html — 普布扎西，男，藏族，1978年2月出生，西藏岗巴人，研究生学历，2004年12月入党，2002年7月参加工作。现任西藏自治区浪卡子县委副书记、县长。"
    },
    # ════════════════════════════════════════
    # Other Leaders (from 领导之窗 sidebar)
    # TO BE CONFIRMED — roles and details TBD
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "白玛维色",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "浪卡子县领导",
        "current_org": "浪卡子县人民政府",
        "source": "浪卡子县人民政府官网领导之窗栏目的名称为表 —— 白玛维色出现在领导栏目名单中"
    },
    {
        "id": 4,
        "name": "孙益民",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "浪卡子县领导",
        "current_org": "浪卡子县人民政府",
        "source": "浪卡子县人民政府官网领导之窗栏目的名称为表"
    },
    {
        "id": 5,
        "name": "边巴次仁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "浪卡子县领导",
        "current_org": "浪卡子县人民政府",
        "source": "浪卡子县人民政府官网领导之窗栏目的名称为表"
    },
    {
        "id": 6,
        "name": "梅国斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "浪卡子县领导",
        "current_org": "浪卡子县人民政府",
        "source": "浪卡子县人民政府官网领导之窗栏目的名称为表"
    },
    {
        "id": 7,
        "name": "尼玛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "浪卡子县领导",
        "current_org": "浪卡子县人民政府",
        "source": "浪卡子县人民政府官网领导之窗栏目的名称为表"
    },
    {
        "id": 8,
        "name": "布琼次仁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "浪卡子县领导",
        "current_org": "浪卡子县人民政府",
        "source": "浪卡子县人民政府官网领导之窗栏目的名称为表"
    },
    {
        "id": 9,
        "name": "元旦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "浪卡子县领导",
        "current_org": "浪卡子县人民政府",
        "source": "浪卡子县人民政府官网领导之窗栏目的名称为表"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共浪卡子县委员会",
        "type": "党委",
        "level": "县级",
        "location": "山南市浪卡子县",
        "parent": "中共山南市委"
    },
    {
        "id": 2,
        "name": "浪卡子县人民政府",
        "type": "政府",
        "level": "县级",
        "location": "山南市浪卡子县",
        "parent": "山南市人民政府"
    },
    {
        "id": 3,
        "name": "浪卡子县人大常委会",
        "type": "人大",
        "level": "县级",
        "location": "山南市浪卡子县",
        "parent": "山南市人大常委会"
    },
    {
        "id": 4,
        "name": "政协浪卡子县委员会",
        "type": "政协",
        "level": "县级",
        "location": "山南市浪卡子县",
        "parent": "政协山南市委员会"
    },
    {
        "id": 5,
        "name": "中共浪卡子县纪律检查委员会",
        "type": "纪委",
        "level": "县级",
        "location": "山南市浪卡子县",
        "parent": "中共山南市纪律检查委员会"
    },
    {
        "id": 6,
        "name": "中共浪卡子县委组织部",
        "type": "党委部门",
        "level": "县级",
        "location": "山南市浪卡子县",
        "parent": "中共浪卡子县委员会"
    },
    {
        "id": 7,
        "name": "中共浪卡子县委宣传部",
        "type": "党委部门",
        "level": "县级",
        "location": "山南市浪卡子县",
        "parent": "中共浪卡子县委员会"
    },
    {
        "id": 8,
        "name": "中共浪卡子县委统战部",
        "type": "党委部门",
        "level": "县级",
        "location": "山南市浪卡子县",
        "parent": "中共浪卡子县委员会"
    },
    {
        "id": 9,
        "name": "中共浪卡子县委政法委",
        "type": "政法系统",
        "level": "县级",
        "location": "山南市浪卡子县",
        "parent": "中共浪卡子县委员会"
    },
    {
        "id": 10,
        "name": "浪卡子县审计局",
        "type": "政府部门",
        "level": "县级",
        "location": "山南市浪卡子县",
        "parent": "浪卡子县人民政府"
    },
    {
        "id": 11,
        "name": "浪卡子县发展和改革委员会",
        "type": "政府部门",
        "level": "县级",
        "location": "山南市浪卡子县",
        "parent": "浪卡子县人民政府"
    },
    # Career historical orgs for 普布扎西
    {
        "id": 12,
        "name": "仲巴县计委",
        "type": "政府部门",
        "level": "县级",
        "location": "日喀则市仲巴县",
        "parent": "仲巴县人民政府"
    },
    {
        "id": 13,
        "name": "仲巴县商务局",
        "type": "政府部门",
        "level": "县级",
        "location": "日喀则市仲巴县",
        "parent": "仲巴县人民政府"
    },
    {
        "id": 14,
        "name": "仲巴县水利局",
        "type": "政府部门",
        "level": "县级",
        "location": "日喀则市仲巴县",
        "parent": "仲巴县人民政府"
    },
    {
        "id": 15,
        "name": "西藏自治区发展和改革委员会",
        "type": "政府部门",
        "level": "自治区级",
        "location": "拉萨市",
        "parent": "西藏自治区人民政府"
    },
    {
        "id": 16,
        "name": "西藏自治区节能监察中心",
        "type": "事业单位",
        "level": "自治区级",
        "location": "拉萨市",
        "parent": "西藏自治区发展和改革委员会"
    },
]

# 3. Positions
positions = [
    # 罗云 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "浪卡子县委书记", "start": "", "end": "present", "rank": "正处级", "note": "自2026年1月以县委书记身份出现在公开报道中"},
    # 普布扎西 — 县长（完整履历）
    {"person_id": 2, "org_id": 2, "title": "浪卡子县委副书记、县长", "start": "2025.05", "end": "present", "rank": "正处级", "note": "主持县政府全面工作，分管县审计局"},
    {"person_id": 2, "org_id": 15, "title": "西藏自治区发展和改革委员会国民经济和体制改革综合处处长", "start": "2024.05", "end": "2025.04", "rank": "正处级", "note": "前任：国民经济综合处处长，后更名为国民经济和体制改革综合处"},
    {"person_id": 2, "org_id": 15, "title": "西藏自治区发展和改革委员会国民经济综合处处长", "start": "2023.04", "end": "2024.05", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 15, "title": "西藏自治区发展和改革委员会经济运行调节处处长", "start": "2021.04", "end": "2023.04", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 15, "title": "西藏自治区发展和改革委员会农村经济处处长", "start": "2019.04", "end": "2021.04", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 15, "title": "西藏自治区发展和改革委员会固定资产投资处副处长", "start": "2016.12", "end": "2019.04", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 15, "title": "西藏自治区发展和改革委员会国民经济综合处副处长", "start": "2013.11", "end": "2016.12", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 16, "title": "西藏自治区节能监察中心主任科员", "start": "2011.01", "end": "2013.11", "rank": "正科级", "note": ""},
    {"person_id": 2, "org_id": 15, "title": "西藏自治区发展和改革委员会发展研究中心主任科员", "start": "2009.08", "end": "2011.01", "rank": "正科级", "note": ""},
    {"person_id": 2, "org_id": 15, "title": "西藏自治区发展和改革委员会发展研究中心副主任科员", "start": "2008.05", "end": "2009.08", "rank": "副科级", "note": ""},
    {"person_id": 2, "org_id": 14, "title": "仲巴县水利局副局长兼县电厂厂长", "start": "2006.05", "end": "2008.05", "rank": "副科级", "note": ""},
    {"person_id": 2, "org_id": 13, "title": "仲巴县商务局副主任科员兼县电厂厂长", "start": "2004.11", "end": "2006.05", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 13, "title": "仲巴县商务局科员兼县电厂厂长", "start": "2004.01", "end": "2004.11", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 12, "title": "仲巴县计委科员", "start": "2002.07", "end": "2004.01", "rank": "", "note": ""},
    # 其他领导（基本信息待确认）
    {"person_id": 3, "org_id": 2, "title": "浪卡子县领导", "start": "", "end": "present", "rank": "", "note": "具体职务待确认"},
    {"person_id": 4, "org_id": 2, "title": "浪卡子县领导", "start": "", "end": "present", "rank": "", "note": "具体职务待确认"},
    {"person_id": 5, "org_id": 2, "title": "浪卡子县领导", "start": "", "end": "present", "rank": "", "note": "具体职务待确认"},
    {"person_id": 6, "org_id": 2, "title": "浪卡子县领导", "start": "", "end": "present", "rank": "", "note": "具体职务待确认"},
    {"person_id": 7, "org_id": 2, "title": "浪卡子县领导", "start": "", "end": "present", "rank": "", "note": "具体职务待确认"},
    {"person_id": 8, "org_id": 2, "title": "浪卡子县领导", "start": "", "end": "present", "rank": "", "note": "具体职务待确认"},
    {"person_id": 9, "org_id": 2, "title": "浪卡子县领导", "start": "", "end": "present", "rank": "", "note": "具体职务待确认"},
]

# 4. Relationships
relationships = [
    # 罗云 — 普布扎西：党政一把手
    {"person_a": 1, "person_b": 2, "type": "党政一把手", "context": "罗云（县委书记）与普布扎西（县长）为浪卡子县党政主要负责人", "overlap_org": "浪卡子县", "overlap_period": "2025年至今"},
    # 普布扎西任县长（由区发改委空降）
    {"person_a": 2, "person_b": 1, "type": "上级任命", "context": "普布扎西自西藏自治区发改委处长空降至浪卡子县任县长", "overlap_org": "浪卡子县人民政府", "overlap_period": "2025.05至今"},
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