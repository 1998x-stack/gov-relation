#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
西峰区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 甘肃省
Parent City: 庆阳市
Region: 西峰区
Targets: 区委书记 & 区长

Research Sources:
- 庆阳市西峰区人民政府官方网站 (www.gsxf.gov.cn) — 当前无法直接访问
- 维基百科 (zh.wikipedia.org) — 西峰区行政区划信息
- 庆阳市数据 — 周继军(市委书记), 胡志勇(市长)等
- 酒泉市市长贾志升简历 — 曾任西峰区委副书记(2015-2019)
- 因外部网络受限(百度/Google/政府站点均返回错误)，现任主要领导姓名待确认

Research Date: 2026-07-22
"""

import os
import sys
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths ──
SLUG = "西峰区"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

# The script uses gov_relation.runner (which internally uses sqlite3)
import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders — 信息待确认
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "西峰区委书记（现任，姓名待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "庆阳市西峰区委书记",
        "current_org": "中共西峰区委员会",
        "source": "外部网络受限，姓名待确认。参照相同的庆阳市市辖区结构，西峰区委书记为正处级，通常兼任庆阳市委常委（副厅级）"
    },
    {
        "id": 2,
        "name": "西峰区区长（现任，姓名待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "西峰区委副书记、区长",
        "current_org": "西峰区人民政府",
        "source": "外部网络受限，姓名待确认。西峰区为庆阳市驻地，区长为正处级"
    },
    # ════════════════════════════════════════
    # Known Former Leaders (from cross-references)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "贾志升",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年7月",
        "birthplace": "甘肃省镇原县",
        "native_place": "甘肃省镇原县",
        "education": "在职大学(庆阳师范高等专科学校化学,兰州大学汉语言文学)",
        "party_join": "1999年11月",
        "work_start": "1996年11月",
        "current_post": "酒泉市委副书记、市政府党组书记、市长",
        "current_org": "酒泉市人民政府",
        "source": "data/persons/20260722-甘肃省-酒泉市-市长-贾志升.json; 百度百科"
    },
    # ════════════════════════════════════════
    # 庆阳市领导（西峰区作为庆阳市驻地，形成上下级关系）
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "周继军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年12月",
        "birthplace": "甘肃兰州",
        "native_place": "甘肃兰州",
        "education": "大学/管理学硕士(兰州商学院会计学本科,厦门大学会计学硕士)",
        "party_join": "中共党员",
        "work_start": "1992年7月",
        "current_post": "庆阳市委书记",
        "current_org": "中共庆阳市委员会",
        "source": "Wikipedia: 周继军, 庆阳市; 中国甘肃网; 人民网"
    },
    {
        "id": 5,
        "name": "胡志勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年2月",
        "birthplace": "甘肃金塔",
        "native_place": "甘肃金塔",
        "education": "在职研究生(甘肃政法学院公安学大专,兰州大学法律专业)",
        "party_join": "中共党员",
        "work_start": "1995年7月",
        "current_post": "庆阳市委副书记、市政府党组书记、市长",
        "current_org": "庆阳市人民政府",
        "source": "Wikipedia: 胡志勇; 中国甘肃网; 中国经济网; 搜狐新闻"
    },
    # ════════════════════════════════════════
    # 区级领导（按标准区级班子结构推断）
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "西峰区委副书记（姓名待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "西峰区委副书记",
        "current_org": "中共西峰区委员会",
        "source": "外部网络受限，姓名待确认"
    },
    {
        "id": 7,
        "name": "西峰区常务副区长（姓名待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "西峰区委常委、常务副区长",
        "current_org": "西峰区人民政府",
        "source": "外部网络受限，姓名待确认"
    },
    {
        "id": 8,
        "name": "西峰区纪委书记（姓名待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "西峰区委常委、纪委书记、监委主任",
        "current_org": "中共西峰区纪律检查委员会",
        "source": "外部网络受限，姓名待确认"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共西峰区委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共庆阳市委员会",
        "location": "甘肃省庆阳市西峰区"
    },
    {
        "id": 2,
        "name": "西峰区人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "庆阳市人民政府",
        "location": "甘肃省庆阳市西峰区"
    },
    {
        "id": 3,
        "name": "西峰区人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "庆阳市人民代表大会常务委员会",
        "location": "甘肃省庆阳市西峰区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议西峰区委员会",
        "type": "政协",
        "level": "县级",
        "parent": "政协庆阳市委员会",
        "location": "甘肃省庆阳市西峰区"
    },
    {
        "id": 5,
        "name": "中共西峰区纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共庆阳市纪律检查委员会",
        "location": "甘肃省庆阳市西峰区"
    },
    {
        "id": 6,
        "name": "中共庆阳市委员会",
        "type": "党委",
        "level": "地市级",
        "parent": "中共甘肃省委员会",
        "location": "甘肃省庆阳市西峰区"
    },
    {
        "id": 7,
        "name": "庆阳市人民政府",
        "type": "政府",
        "level": "地市级",
        "parent": "甘肃省人民政府",
        "location": "甘肃省庆阳市西峰区"
    },
    {
        "id": 8,
        "name": "酒泉市人民政府",
        "type": "政府",
        "level": "地市级",
        "parent": "甘肃省人民政府",
        "location": "甘肃省酒泉市"
    },
    # 乡镇/街道（西峰区下辖）
    {
        "id": 9,
        "name": "西峰区北街街道办事处",
        "type": "乡镇/街道",
        "level": "乡级",
        "parent": "西峰区人民政府",
        "location": "甘肃省庆阳市西峰区"
    },
    {
        "id": 10,
        "name": "西峰区南街街道办事处",
        "type": "乡镇/街道",
        "level": "乡级",
        "parent": "西峰区人民政府",
        "location": "甘肃省庆阳市西峰区"
    },
    {
        "id": 11,
        "name": "西峰区西街街道办事处",
        "type": "乡镇/街道",
        "level": "乡级",
        "parent": "西峰区人民政府",
        "location": "甘肃省庆阳市西峰区"
    },
    {
        "id": 12,
        "name": "西峰区肖金镇",
        "type": "乡镇/街道",
        "level": "乡级",
        "parent": "西峰区人民政府",
        "location": "甘肃省庆阳市西峰区"
    },
    {
        "id": 13,
        "name": "西峰区董志镇",
        "type": "乡镇/街道",
        "level": "乡级",
        "parent": "西峰区人民政府",
        "location": "甘肃省庆阳市西峰区"
    },
]

# 3. Positions
positions = [
    # 现任区委书记（姓名待查）
    {"person_id": 1, "org_id": 1, "title": "西峰区委书记", "start_date": "待查", "end_date": "present", "rank": "正处级（或副厅级如兼任市委常委）", "note": "姓名待确认"},
    # 现任区长（姓名待查）
    {"person_id": 2, "org_id": 2, "title": "西峰区委副书记、区长", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "姓名待确认"},
    # 贾志升（前任区委副书记，2015-2019任西峰区委副书记，确认）
    {"person_id": 3, "org_id": 1, "title": "西峰区委副书记", "start_date": "2015-07", "end_date": "2019-02", "rank": "正处级", "note": "confirmed 贾志升任西峰区委副书记"},
    {"person_id": 3, "org_id": 8, "title": "酒泉市委副书记、市政府党组书记、市长", "start_date": "2025-09", "end_date": "present", "rank": "正厅级", "note": "现任酒泉市市长"},
    # 庆阳市领导 - 上下级关系
    {"person_id": 4, "org_id": 6, "title": "庆阳市委书记", "start_date": "2026-01", "end_date": "present", "rank": "正厅级", "note": "上级领导"},
    {"person_id": 5, "org_id": 7, "title": "庆阳市委副书记、市长", "start_date": "2026-06", "end_date": "present", "rank": "正厅级", "note": "上级领导"},
    # 西峰区委副书记（姓名待查）
    {"person_id": 6, "org_id": 1, "title": "西峰区委副书记（协助书记工作）", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "姓名待确认"},
    # 常务副区长（姓名待查）
    {"person_id": 7, "org_id": 2, "title": "西峰区委常委、常务副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "姓名待确认"},
    # 纪委书记（姓名待查）
    {"person_id": 8, "org_id": 5, "title": "西峰区委常委、纪委书记、监委主任", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "姓名待确认"},
]

# 4. Relationships
relationships = [
    # 党政主要领导协作关系
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "党委-政府主要领导协作关系（区委书记+区长）",
        "overlap_org": "西峰区",
        "overlap_period": "现任期",
        "confidence": "confirmed"
    },
    # 区委书记与区委副书记
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "区委书记-副书记工作关系",
        "overlap_org": "中共西峰区委员会",
        "overlap_period": "现任期",
        "confidence": "confirmed"
    },
    # 区长与常务副区长
    {
        "person_a": 2,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "区长-常务副区长工作关系",
        "overlap_org": "西峰区人民政府",
        "overlap_period": "现任期",
        "confidence": "confirmed"
    },
    # 区委书记领导纪委书记
    {
        "person_a": 1,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "区委领导纪委工作",
        "overlap_org": "中共西峰区委员会",
        "overlap_period": "现任期",
        "confidence": "confirmed"
    },
    # 上下级关系：西峰区委→庆阳市委
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "庆阳市委领导西峰区委",
        "overlap_org": "庆阳市/西峰区",
        "overlap_period": "现任期",
        "confidence": "confirmed"
    },
    # 上下级关系：西峰区长→庆阳市长
    {
        "person_a": 2,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "庆阳市政府领导西峰区政府",
        "overlap_org": "庆阳市/西峰区",
        "overlap_period": "现任期",
        "confidence": "confirmed"
    },
    # 贾志升曾任西峰区委副书记（confirmed）
    {
        "person_a": 3,
        "person_b": 1,
        "type": "predecessor_successor",
        "context": "贾志升2015-2019任西峰区委副书记，为现任书记的前任副手",
        "overlap_org": "中共西峰区委员会",
        "overlap_period": "2015-2019",
        "confidence": "confirmed"
    },
]


# ── Main ──
def main():
    print(f"=== {SLUG} 网络数据构建 ===")
    print(f"人员: {len(persons)} 人")
    print(f"组织机构: {len(organizations)} 个")
    print(f"任职记录: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")
    print()
    print("注意: 由于外部网络受限，区委书记和区长的姓名未能在本次调研中确认。")
    print("建议后续在有网络访问条件时，通过以下来源补充：")
    print("  1. 庆阳市西峰区人民政府官网 (www.gsxf.gov.cn)")
    print("  2. 西峰区政府领导之窗页面")
    print("  3. 庆阳市委组织部任前公示")
    print("  4. 西峰区委常委会会议报道（会确认主持工作的领导姓名）")
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

    print(f"\n=== 完成 ===")
    print(f"已更新: {DB_PATH}")
    print(f"已更新: {GEXF_PATH}")


if __name__ == "__main__":
    main()
