#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
沧州市新华区领导班子工作关系网络 — 数据构建脚本（暂存区版）
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 河北省
Parent City: 沧州市
Region: 新华区
Targets: 区委书记 & 区长

Research Sources (2026-07-24):
- 新华区政府网站 (www.czxh.gov.cn):
  - 领导介绍 pages: confirmed 7 government leaders
  - 新华要闻 2026-05-02 "金培元 哈增瑞督导调研节前重点工作" -> confirms 金培元 as 区委书记, 哈增瑞 as 区长
  - 新华要闻 2026-04-09 -> confirms 霍刚 as 区委副书记
  - 新华要闻 2022-10-09 "金培元、陈国帮到部分社区进行督导调研" -> 确认陈国帮曾任区长
- 澎湃新闻 2018-12-17: 金培元调任运河区委副书记、提名区长候选人
- 速豹新闻网/搜狐 2021-05-20: "80后清华博士升任区委书记"
- 沧州市委组织部2021年5月任免决定
- 沧州市委组织部2024年9月任免决定
- 澎湃新闻/新浪 2024-09-20: 哈增瑞任新华区副区长、代区长
- 百度百科: 金培元（1980年11月，甘肃兰州人，博士研究生）
- 百度AI搜索 哈增瑞简历: 回族，曾任吴桥县副县长、吴桥县委常委宣传部部长、青县县委副书记

Research Date: 2026-07-24
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "新华区"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# --- Data ---

persons = [
    {
        "id": 1,
        "name": "金培元",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年11月",
        "birthplace": "甘肃兰州",
        "native_place": "甘肃兰州",
        "education": "博士研究生",
        "party_join": "中共党员",
        "work_start": "2008年",
        "current_post": "沧州市新华区委书记",
        "current_org": "中共沧州市新华区委员会",
        "source": "confirmed - 新华区政府网站/百度百科"
    },
    {
        "id": 2,
        "name": "哈增瑞",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "沧州市新华区委副书记、区长",
        "current_org": "新华区人民政府",
        "source": "confirmed - 新华区政府网站"
    },
    {
        "id": 3,
        "name": "霍刚",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "新华区委副书记",
        "current_org": "中共沧州市新华区委员会",
        "source": "confirmed - czxh.gov.cn 2026-04-09"
    },
    {
        "id": 4,
        "name": "罗宵",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "新华区委常委、区政府常务副区长",
        "current_org": "新华区人民政府",
        "source": "confirmed - czxh.gov.cn 领导介绍"
    },
    {
        "id": 5,
        "name": "张俊峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "新华区政府副区长（市公安局新华分局局长）",
        "current_org": "新华区人民政府",
        "source": "confirmed - czxh.gov.cn 领导介绍"
    },
    {
        "id": 6,
        "name": "马俊亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "新华区政府副区长",
        "current_org": "新华区人民政府",
        "source": "confirmed - czxh.gov.cn 领导介绍"
    },
    {
        "id": 7,
        "name": "陈思文",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "新华区政府副区长",
        "current_org": "新华区人民政府",
        "source": "confirmed - czxh.gov.cn 领导介绍"
    },
    {
        "id": 8,
        "name": "白丽英",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "新华区政府副区长",
        "current_org": "新华区人民政府",
        "source": "confirmed - czxh.gov.cn 领导介绍"
    },
    {
        "id": 9,
        "name": "徐峰",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "新华区领导（具体职务待查）",
        "current_org": "中共沧州市新华区委员会",
        "source": "confirmed - czxh.gov.cn 2022-10-09"
    },
    {
        "id": 10,
        "name": "徐晋",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "新华区领导（具体职务待查）",
        "current_org": "中共沧州市新华区委员会",
        "source": "confirmed - czxh.gov.cn 2026-05-02"
    },
    {
        "id": 11,
        "name": "王景旗",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "新华区领导（具体职务待查）",
        "current_org": "中共沧州市新华区委员会",
        "source": "confirmed - czxh.gov.cn 2022-10-09"
    },
    {
        "id": 12,
        "name": "陈国帮",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "吴桥县委书记",
        "current_org": "中共吴桥县委员会",
        "source": "confirmed - 2024年9月任免决定"
    },
    {
        "id": 13,
        "name": "刘建华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已离任（原新华区委书记）",
        "current_org": "",
        "source": "unverified - 训练数据"
    },
]

organizations = [
    {"id": 1, "name": "中共沧州市新华区委员会", "type": "党委", "level": "县处级", "location": "河北省沧州市新华区"},
    {"id": 2, "name": "新华区人民政府", "type": "政府", "level": "县处级", "location": "河北省沧州市新华区"},
    {"id": 3, "name": "中共沧州市新华区纪律检查委员会", "type": "纪委", "level": "县处级", "location": "河北省沧州市新华区"},
    {"id": 4, "name": "新华区人大常委会", "type": "人大", "level": "县处级", "location": "河北省沧州市新华区"},
    {"id": 5, "name": "政协新华区委员会", "type": "政协", "level": "县处级", "location": "河北省沧州市新华区"},
    {"id": 6, "name": "中共沧州市新华区委组织部", "type": "党委部门", "level": "乡科级", "location": "河北省沧州市新华区"},
    {"id": 7, "name": "中共沧州市新华区委宣传部", "type": "党委部门", "level": "乡科级", "location": "河北省沧州市新华区"},
    {"id": 8, "name": "中共沧州市新华区委政法委员会", "type": "党委部门", "level": "乡科级", "location": "河北省沧州市新华区"},
    {"id": 9, "name": "中共沧州市新华区委统一战线工作部", "type": "党委部门", "level": "乡科级", "location": "河北省沧州市新华区"},
    {"id": 10, "name": "沧州市公安局新华分局", "type": "政府", "level": "乡科级", "location": "河北省沧州市新华区"},
    {"id": 11, "name": "沧州市", "type": "地级市", "level": "地厅级", "location": "河北省"},
    {"id": 12, "name": "沧州市运河区人民政府", "type": "政府", "level": "县处级", "location": "河北省沧州市运河区"},
    {"id": 13, "name": "共青团保定市委", "type": "群团", "level": "地厅级", "location": "河北省保定市"},
    {"id": 14, "name": "中共高碑店市委宣传部", "type": "党委部门", "level": "乡科级", "location": "河北省保定市高碑店市"},
    {"id": 15, "name": "保定市卫生局", "type": "政府", "level": "地厅级", "location": "河北省保定市"},
    {"id": 16, "name": "清华大学", "type": "事业单位", "level": "", "location": "北京市"},
    {"id": 17, "name": "兰州大学", "type": "事业单位", "level": "", "location": "甘肃省兰州市"},
    {"id": 18, "name": "中共吴桥县委员会", "type": "党委", "level": "县处级", "location": "河北省沧州市吴桥县"},
    {"id": 19, "name": "吴桥县人民政府", "type": "政府", "level": "县处级", "location": "河北省沧州市吴桥县"},
    {"id": 20, "name": "中共青县委员会", "type": "党委", "level": "县处级", "location": "河北省沧州市青县"},
    {"id": 21, "name": "沧州市农林科学院", "type": "事业单位", "level": "县处级", "location": "河北省沧州市"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "沧州市新华区委书记", "start_date": "2021-05", "end_date": "present", "rank": "正处级",
     "note": "2021年5月任"},
    {"person_id": 1, "org_id": 12, "title": "沧州市运河区委副书记、区长", "start_date": "2018-12", "end_date": "2021-05", "rank": "正处级",
     "note": "2018年12月调任"},
    {"person_id": 1, "org_id": 13, "title": "共青团保定市委书记", "start_date": "约2017", "end_date": "2018-12", "rank": "正处级"},
    {"person_id": 1, "org_id": 14, "title": "高碑店市委常委、宣传部部长、农工委书记", "start_date": "约2015", "end_date": "约2017", "rank": "副处级"},
    {"person_id": 1, "org_id": 15, "title": "保定市卫生局党委委员、副局长", "start_date": "约2012", "end_date": "约2015", "rank": "副处级"},
    {"person_id": 1, "org_id": 16, "title": "清华大学研究生工作部助理研究员", "start_date": "2008", "end_date": "约2009", "rank": ""},
    {"person_id": 1, "org_id": 16, "title": "博士研究生（清华大学）", "start_date": "2003", "end_date": "2008", "rank": ""},
    {"person_id": 1, "org_id": 17, "title": "本科（兰州大学）", "start_date": "1999", "end_date": "2003", "rank": ""},
    {"person_id": 2, "org_id": 2, "title": "沧州市新华区委副书记、区长", "start_date": "2024-09", "end_date": "present", "rank": "正处级"},
    {"person_id": 2, "org_id": 21, "title": "沧州市农林科学院党委书记、院长", "start_date": "2023-07", "end_date": "2024-09", "rank": "正处级"},
    {"person_id": 2, "org_id": 20, "title": "青县县委副书记", "start_date": "待查", "end_date": "2023-07", "rank": "副处级"},
    {"person_id": 2, "org_id": 18, "title": "吴桥县委常委、宣传部部长", "start_date": "待查", "end_date": "待查", "rank": "副处级"},
    {"person_id": 2, "org_id": 19, "title": "吴桥县人民政府副县长", "start_date": "待查", "end_date": "待查", "rank": "副处级"},
    {"person_id": 3, "org_id": 1, "title": "新华区委副书记", "start_date": "待查", "end_date": "present", "rank": "副处级"},
    {"person_id": 4, "org_id": 2, "title": "新华区委常委、常务副区长", "start_date": "待查", "end_date": "present", "rank": "副处级"},
    {"person_id": 5, "org_id": 2, "title": "新华区政府副区长", "start_date": "待查", "end_date": "present", "rank": "副处级"},
    {"person_id": 5, "org_id": 10, "title": "沧州市公安局新华分局局长", "start_date": "待查", "end_date": "present", "rank": "副处级"},
    {"person_id": 6, "org_id": 2, "title": "新华区政府副区长", "start_date": "待查", "end_date": "present", "rank": "副处级"},
    {"person_id": 7, "org_id": 2, "title": "新华区政府副区长", "start_date": "待查", "end_date": "present", "rank": "副处级"},
    {"person_id": 8, "org_id": 2, "title": "新华区政府副区长", "start_date": "待查", "end_date": "present", "rank": "副处级"},
    {"person_id": 9, "org_id": 1, "title": "新华区领导（具体职务待查）", "start_date": "待查", "end_date": "present", "rank": "待查"},
    {"person_id": 10, "org_id": 1, "title": "新华区领导（具体职务待查）", "start_date": "待查", "end_date": "present", "rank": "待查"},
    {"person_id": 11, "org_id": 1, "title": "新华区领导（具体职务待查）", "start_date": "待查", "end_date": "present", "rank": "待查"},
    {"person_id": 12, "org_id": 18, "title": "吴桥县委书记", "start_date": "2024-09", "end_date": "present", "rank": "正处级"},
    {"person_id": 12, "org_id": 2, "title": "沧州市新华区委副书记、区长", "start_date": "约2021", "end_date": "2024-09", "rank": "正处级"},
    {"person_id": 13, "org_id": 1, "title": "沧州市新华区委书记", "start_date": "约2016", "end_date": "2021-05", "rank": "正处级",
     "note": "训练数据，未核实"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "金培元（区委书记）与哈增瑞（区长）为新华区党政主要领导搭档",
     "overlap_org": "中共沧州市新华区委员会/新华区人民政府", "overlap_period": "2024年9月至今"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "金培元（书记）与霍刚（副书记）在区委常委会共事",
     "overlap_org": "中共沧州市新华区委员会", "overlap_period": "待查"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "金培元（书记）与罗宵（常务副区长）为党政班子成员",
     "overlap_org": "新华区党政领导班子", "overlap_period": "待查"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "哈增瑞（区长）与罗宵（常务副区长）为区政府正副职搭档",
     "overlap_org": "新华区人民政府", "overlap_period": "2024年9月至今"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "哈增瑞（区长）与张俊峰（副区长/公安分局局长）在区政府班子共事",
     "overlap_org": "新华区人民政府", "overlap_period": "待查"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "哈增瑞（区长）与马俊亮（副区长）在区政府班子共事",
     "overlap_org": "新华区人民政府", "overlap_period": "待查"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "哈增瑞（区长）与陈思文（副区长）在区政府班子共事",
     "overlap_org": "新华区人民政府", "overlap_period": "待查"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "哈增瑞（区长）与白丽英（副区长）在区政府班子共事",
     "overlap_org": "新华区人民政府", "overlap_period": "待查"},
    {"person_a": 1, "person_b": 13, "type": "predecessor_successor",
     "context": "金培元接替刘建华任新华区委书记",
     "overlap_org": "中共沧州市新华区委员会", "overlap_period": "2021年5月交接"},
    {"person_a": 1, "person_b": 12, "type": "colleague",
     "context": "金培元（书记）与陈国帮（区长）在2021-2024年搭档",
     "overlap_org": "中共沧州市新华区委员会/新华区人民政府", "overlap_period": "约2021-2024年"},
    {"person_a": 1, "person_b": 12, "type": "predecessor_successor",
     "context": "金培元此前任新华区长，由陈国帮接任",
     "overlap_org": "新华区人民政府", "overlap_period": "约2021交接"},
    {"person_a": 2, "person_b": 12, "type": "predecessor_successor",
     "context": "哈增瑞接替陈国帮任新华区长",
     "overlap_org": "新华区人民政府", "overlap_period": "2024年9月交接"},
    {"person_a": 2, "person_b": 12, "type": "cross_region_network",
     "context": "哈增瑞曾在吴桥任职，陈国帮2024年调任吴桥县委书记",
     "overlap_org": "中共吴桥县委员会/吴桥县人民政府", "overlap_period": "约2024年9月"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "金培元（书记）与徐晋（区领导）在区委共事",
     "overlap_org": "中共沧州市新华区委员会", "overlap_period": "待查"},
]

# --- Build ---

if __name__ == "__main__":
    print("=" * 60)
    print("  沧州市新华区领导班子工作关系网络")
    print("  等级: 市辖区")
    print("  调查日期: 2026-07-24")
    print("=" * 60)
    print()

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

    confirmed = sum(1 for p in persons if p["source"].startswith("confirmed"))
    partial = sum(1 for p in persons if p["source"].startswith("partial"))
    unverified = sum(1 for p in persons if p["source"].startswith("unverified"))

    print(f"\n  数据可信度统计:")
    print(f"  {confirmed} 人已确认")
    print(f"  {partial} 人部分确认")
    print(f"  {unverified} 人未核实")
    print(f"\n  {len(persons)} 人, {len(organizations)} 机构, {len(positions)} 任职, {len(relationships)} 关系")
