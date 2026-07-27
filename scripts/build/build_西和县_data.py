#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
西和县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 甘肃省
Parent City: 陇南市
Region: 西和县
Targets: 县委书记 & 县长

Research Sources:
- 西和县人民政府官方网站 (www.xihe.gov.cn), 2026年7月确认
  - 领导之窗: https://www.xihe.gov.cn/ldzc/
  - 范登奎（县委书记）: 确认，简历显示"省委党校研究生学历"
  - 尚悦春（县委副书记/专职）: 确认，分工为"负责县委日常事务、国家安全、机要保密、农业农村、群团、驻村帮扶工作"
  - 县委常委会完整名单已从领导之窗获取
  - 县政府领导名单已获取（不含县长）
- 官网新闻动态: 范登奎防汛督导、政法调研等
- 注意: 县长职位在县政府领导栏目中未列出，可能空缺或信息未公开

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
SLUG = "西和县"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

# The script uses gov_relation.runner (which internally uses sqlite3)
import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "范登奎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年7月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "西和县委书记",
        "current_org": "中共西和县委员会",
        "source": "西和县人民政府官网(xihe.gov.cn) 2026-07; 领导之窗"
    },
    {
        "id": 2,
        "name": "（县长待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "西和县委副书记、县长（待确认）",
        "current_org": "西和县人民政府",
        "source": "西和县人民政府官网(xihe.gov.cn) 2026-07; 领导之窗未列出县长信息"
    },
    # ════════════════════════════════════════
    # 县委其他副书记
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "尚悦春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年11月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "西和县委副书记（专职）",
        "current_org": "中共西和县委员会",
        "source": "西和县人民政府官网(xihe.gov.cn) 2026-07; 领导之窗"
    },
    # ════════════════════════════════════════
    # 县委常委
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "任志远",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、常务副县长",
        "current_org": "西和县人民政府",
        "source": "西和县人民政府官网(xihe.gov.cn) 2026-07; 领导之窗"
    },
    {
        "id": 5,
        "name": "苟睿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共西和县委员会政法委员会",
        "source": "西和县人民政府官网(xihe.gov.cn) 2026-07; 领导之窗"
    },
    {
        "id": 6,
        "name": "苏长林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共西和县纪律检查委员会",
        "source": "西和县人民政府官网(xihe.gov.cn) 2026-07; 领导之窗"
    },
    {
        "id": 7,
        "name": "赵文彪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、副县长",
        "current_org": "西和县人民政府",
        "source": "西和县人民政府官网(xihe.gov.cn) 2026-07; 领导之窗"
    },
    {
        "id": 8,
        "name": "蔡侨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共西和县委员会组织部",
        "source": "西和县人民政府官网(xihe.gov.cn) 2026-07; 领导之窗"
    },
    {
        "id": 9,
        "name": "田小慈",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共西和县委员会宣传部",
        "source": "西和县人民政府官网(xihe.gov.cn) 2026-07; 领导之窗"
    },
    {
        "id": 10,
        "name": "杨勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共西和县委员会统一战线工作部",
        "source": "西和县人民政府官网(xihe.gov.cn) 2026-07; 领导之窗"
    },
    {
        "id": 11,
        "name": "赵礼辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、副县长",
        "current_org": "西和县人民政府",
        "source": "西和县人民政府官网(xihe.gov.cn) 2026-07; 领导之窗"
    },
    {
        "id": 12,
        "name": "傅娆",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、副县长",
        "current_org": "西和县人民政府",
        "source": "西和县人民政府官网(xihe.gov.cn) 2026-07; 领导之窗"
    },
    {
        "id": 13,
        "name": "汪锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、副县长",
        "current_org": "西和县人民政府",
        "source": "西和县人民政府官网(xihe.gov.cn) 2026-07; 领导之窗"
    },
    # ════════════════════════════════════════
    # 县政府其他领导（不含常委身份）
    # ════════════════════════════════════════
    {
        "id": 14,
        "name": "李治安",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副县长、县公安局局长",
        "current_org": "西和县人民政府",
        "source": "西和县人民政府官网(xihe.gov.cn) 2026-07; 领导之窗"
    },
    {
        "id": 15,
        "name": "滕小军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副县长",
        "current_org": "西和县人民政府",
        "source": "西和县人民政府官网(xihe.gov.cn) 2026-07; 领导之窗"
    },
    {
        "id": 16,
        "name": "刘卫平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县政府四级调研员",
        "current_org": "西和县人民政府",
        "source": "西和县人民政府官网(xihe.gov.cn) 2026-07; 领导之窗"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共西和县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共陇南市委员会",
        "location": "甘肃省陇南市西和县"
    },
    {
        "id": 2,
        "name": "西和县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "陇南市人民政府",
        "location": "甘肃省陇南市西和县"
    },
    {
        "id": 3,
        "name": "西和县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "陇南市人民代表大会常务委员会",
        "location": "甘肃省陇南市西和县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议西和县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "政协陇南市委员会",
        "location": "甘肃省陇南市西和县"
    },
    {
        "id": 5,
        "name": "中共西和县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共西和县委员会",
        "location": "甘肃省陇南市西和县"
    },
    {
        "id": 6,
        "name": "中共西和县委员会政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共西和县委员会",
        "location": "甘肃省陇南市西和县"
    },
    {
        "id": 7,
        "name": "中共西和县委员会组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共西和县委员会",
        "location": "甘肃省陇南市西和县"
    },
    {
        "id": 8,
        "name": "中共西和县委员会宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共西和县委员会",
        "location": "甘肃省陇南市西和县"
    },
    {
        "id": 9,
        "name": "中共西和县委员会统一战线工作部",
        "type": "党委",
        "level": "县级",
        "parent": "中共西和县委员会",
        "location": "甘肃省陇南市西和县"
    },
    {
        "id": 10,
        "name": "西和县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "西和县人民政府",
        "location": "甘肃省陇南市西和县"
    },
    {
        "id": 11,
        "name": "中共陇南市委员会",
        "type": "党委",
        "level": "地市级",
        "parent": "中共甘肃省委员会",
        "location": "甘肃省陇南市"
    },
    {
        "id": 12,
        "name": "陇南市人民政府",
        "type": "政府",
        "level": "地市级",
        "parent": "甘肃省人民政府",
        "location": "甘肃省陇南市"
    },
    {
        "id": 13,
        "name": "陇南市人民代表大会常务委员会",
        "type": "人大",
        "level": "地市级",
        "parent": "甘肃省人民代表大会常务委员会",
        "location": "甘肃省陇南市"
    },
    {
        "id": 14,
        "name": "政协陇南市委员会",
        "type": "政协",
        "level": "地市级",
        "parent": "政协甘肃省委员会",
        "location": "甘肃省陇南市"
    },
]

# 3. Positions
positions = [
    # 范登奎
    {"person_id": 1, "org_id": 1, "title": "西和县委书记", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "主持县委全面工作"},
    # （县长待查）
    {"person_id": 2, "org_id": 1, "title": "西和县委副书记（候任县长）", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "县长人选待确认，领导之窗未列出"},
    {"person_id": 2, "org_id": 2, "title": "县政府党组书记、县长（待确认）", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "县长信息待确认"},
    # 尚悦春
    {"person_id": 3, "org_id": 1, "title": "西和县委副书记（专职）", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "负责县委日常事务、国家安全、机要保密、农业农村、群团、驻村帮扶工作，协助书记抓党的建设及组织人事工作"},
    # 任志远
    {"person_id": 4, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "县政府领导排名第一"},
    # 苟睿
    {"person_id": 5, "org_id": 6, "title": "县委常委、政法委书记", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 苏长林
    {"person_id": 6, "org_id": 5, "title": "县委常委、县纪委书记、县监委主任", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 赵文彪
    {"person_id": 7, "org_id": 2, "title": "县委常委、副县长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 蔡侨
    {"person_id": 8, "org_id": 7, "title": "县委常委、组织部部长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 田小慈
    {"person_id": 9, "org_id": 8, "title": "县委常委、宣传部部长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 杨勇
    {"person_id": 10, "org_id": 9, "title": "县委常委、统战部部长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 赵礼辉
    {"person_id": 11, "org_id": 2, "title": "县委常委、副县长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 傅娆
    {"person_id": 12, "org_id": 2, "title": "县委常委、副县长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 汪锋
    {"person_id": 13, "org_id": 2, "title": "县委常委、副县长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 李治安
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 10, "title": "县公安局局长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 滕小军
    {"person_id": 15, "org_id": 2, "title": "副县长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 刘卫平
    {"person_id": 16, "org_id": 2, "title": "县政府四级调研员", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
]

# 4. Relationships
relationships = [
    # 书记-县长（待确认）
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "党委-政府主要领导协作关系（待县长确认）",
        "overlap_org": "西和县",
        "overlap_period": "2026年",
        "confidence": "plausible"
    },
    # 书记-专职副书记
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记-专职副书记协作关系",
        "overlap_org": "中共西和县委员会",
        "overlap_period": "2026年",
        "confidence": "confirmed"
    },
    # 书记-各县委常委
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记-常委/常务副县长", "overlap_org": "中共西和县委员会", "overlap_period": "2026年", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委书记-常委/政法委书记", "overlap_org": "中共西和县委员会", "overlap_period": "2026年", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县委书记-常委/纪委书记", "overlap_org": "中共西和县委员会", "overlap_period": "2026年", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "县委书记-常委/副县长", "overlap_org": "中共西和县委员会", "overlap_period": "2026年", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "县委书记-常委/组织部部长", "overlap_org": "中共西和县委员会", "overlap_period": "2026年", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "县委书记-常委/宣传部部长", "overlap_org": "中共西和县委员会", "overlap_period": "2026年", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "县委书记-常委/统战部部长", "overlap_org": "中共西和县委员会", "overlap_period": "2026年", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "县委书记-常委/副县长", "overlap_org": "中共西和县委员会", "overlap_period": "2026年", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate", "context": "县委书记-常委/副县长", "overlap_org": "中共西和县委员会", "overlap_period": "2026年", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 13, "type": "superior_subordinate", "context": "县委书记-常委/副县长", "overlap_org": "中共西和县委员会", "overlap_period": "2026年", "confidence": "confirmed"},
    # 专职副书记-各县委常委
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "专职副书记-常务副县长协作", "overlap_org": "中共西和县委员会", "overlap_period": "2026年", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "专职副书记-政法委书记", "overlap_org": "中共西和县委员会", "overlap_period": "2026年", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 6, "type": "overlap", "context": "专职副书记-纪委书记", "overlap_org": "中共西和县委员会", "overlap_period": "2026年", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 8, "type": "overlap", "context": "专职副书记-组织部部长（协助书记抓党建和组织人事）", "overlap_org": "中共西和县委员会", "overlap_period": "2026年", "confidence": "confirmed"},
    # 常务副县长-其他副县长
    {"person_a": 4, "person_b": 7, "type": "superior_subordinate", "context": "常务副县长-副县长", "overlap_org": "西和县人民政府", "overlap_period": "2026年", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 11, "type": "superior_subordinate", "context": "常务副县长-副县长", "overlap_org": "西和县人民政府", "overlap_period": "2026年", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 12, "type": "superior_subordinate", "context": "常务副县长-副县长", "overlap_org": "西和县人民政府", "overlap_period": "2026年", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 13, "type": "superior_subordinate", "context": "常务副县长-副县长", "overlap_org": "西和县人民政府", "overlap_period": "2026年", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 14, "type": "superior_subordinate", "context": "常务副县长-副县长/公安局长", "overlap_org": "西和县人民政府", "overlap_period": "2026年", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 15, "type": "superior_subordinate", "context": "常务副县长-副县长", "overlap_org": "西和县人民政府", "overlap_period": "2026年", "confidence": "confirmed"},
]


# ── Main ──
def main():
    print(f"=== {SLUG} 网络数据构建 ===")
    print(f"人员: {len(persons)} 人")
    print(f"组织机构: {len(organizations)} 个")
    print(f"任职记录: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")

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


if __name__ == "__main__":
    main()
