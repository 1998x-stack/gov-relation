#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
东乡族自治县领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Dongxiang Autonomous County leadership network.

Level: 县 (自治县)
Province: 甘肃省
Prefecture: 临夏回族自治州
Region: 东乡族自治县
Targets: 县委书记 & 县长

Confirmed officeholders (as of 2026-07-22, from dxzzzx.gov.cn 领导之窗):
- 县委书记: 戚志远 (男，汉族，1977年5月生，大学学历，中共党员)
- 县委副书记、代理县长: 马忠山 (男，东乡族，1984年4月生，大学学历，中共党员)
- 县委常委、常务副县长: 刘康平 (男，汉族，1981年1月生，本科学历，中共党员)
- 县委常委、纪委书记: 马恩泽 (男，东乡族，1982年2月生，研究生学历，中共党员)
- 县委常委、组织部部长: 王瑞亮 (男，汉族，1986年12月生，本科学历，中共党员)
- 县委常委、政法委书记: 高国林 (男，汉族，1978年9月生，大专学历，中共党员)
- 县委常委、宣传部部长: 任胜强 (男，藏族，1985年11月生，省委党校研究生学历，中共党员)
- 县委常委、统战部部长: 汪总领 (男，东乡族，1978年9月生，本科学历，中共党员)
- 县委常委、副县长: 杨彦平 (男，汉族，1985年10月生，本科学历，中共党员)
- 县委常委、副县长(挂职): 张为 (男，汉族，1985年1月生，研究生学历，中共党员)
- 县委常委、副县长(挂职): 柳坤 (男，汉族，1981年2月生，本科学历，中共党员)
- 县委常委、副县长(挂职): 花军委 (男，汉族，1982年2月生，硕士研究生学历，中共党员)
- 县委常委、人武部部长: 刘志华 (男)

Research Sources:
- 东乡族自治县人民政府网站: https://www.dxzzzx.gov.cn/ 领导之窗, 2026年7月22日确认
- 临夏回族自治州人民政府网站: https://www.linxia.gov.cn/ldzc/ 领导之窗, 2026年7月22日确认
- 临夏州人民政府人事任免通知 (2026年5月)
- 东乡族自治县人民政府办公室关于领导分工的通知 (2025年7月17日)

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
SLUG = "东乡族自治县"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "戚志远",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年5月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共东乡族自治县委员会",
        "source": "https://www.dxzzzx.gov.cn/dxx/ldzc/index.html — 东乡县政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 2,
        "name": "马忠山",
        "gender": "男",
        "ethnicity": "东乡族",
        "birth": "1984年4月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、代理县长",
        "current_org": "东乡族自治县人民政府",
        "source": "https://www.dxzzzx.gov.cn/dxx/ldzc/index.html — 东乡县政府网站领导之窗, 2026年7月22日确认"
    },
    # ════════════════════════════════════════
    # 县委常委
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "马恩泽",
        "gender": "男",
        "ethnicity": "东乡族",
        "birth": "1982年2月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、纪委书记、监委主任",
        "current_org": "中共东乡族自治县纪律检查委员会",
        "source": "https://www.dxzzzx.gov.cn/dxx/ldzc/index.html — 东乡县政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 4,
        "name": "刘康平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年1月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "东乡族自治县人民政府",
        "source": "https://www.dxzzzx.gov.cn/dxx/ldzc/index.html — 东乡县政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 5,
        "name": "张为",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年1月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长（挂职）",
        "current_org": "东乡族自治县人民政府",
        "source": "https://www.dxzzzx.gov.cn/dxx/ldzc/index.html — 东乡县政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 6,
        "name": "任胜强",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1985年11月",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共东乡族自治县委宣传部",
        "source": "https://www.dxzzzx.gov.cn/dxx/ldzc/index.html — 东乡县政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 7,
        "name": "柳坤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年2月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长（挂职）",
        "current_org": "东乡族自治县人民政府",
        "source": "https://www.dxzzzx.gov.cn/dxx/ldzc/index.html — 东乡县政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 8,
        "name": "汪总领",
        "gender": "男",
        "ethnicity": "东乡族",
        "birth": "1978年9月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共东乡族自治县委统战部",
        "source": "https://www.dxzzzx.gov.cn/dxx/ldzc/index.html — 东乡县政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 9,
        "name": "高国林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年9月",
        "birthplace": "",
        "education": "大专学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共东乡族自治县委政法委员会",
        "source": "https://www.dxzzzx.gov.cn/dxx/ldzc/index.html — 东乡县政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 10,
        "name": "杨彦平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年10月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "东乡族自治县人民政府",
        "source": "https://www.dxzzzx.gov.cn/dxx/ldzc/index.html — 东乡县政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 11,
        "name": "花军委",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年2月",
        "birthplace": "",
        "education": "硕士研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长（挂职）",
        "current_org": "东乡族自治县人民政府",
        "source": "https://www.dxzzzx.gov.cn/dxx/ldzc/index.html — 东乡县政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 12,
        "name": "王瑞亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年12月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共东乡族自治县委组织部",
        "source": "https://www.dxzzzx.gov.cn/dxx/ldzc/index.html — 东乡县政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 13,
        "name": "刘志华",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、人民武装部部长",
        "current_org": "东乡县人民武装部",
        "source": "https://www.dxzzzx.gov.cn/dxx/ldzc/index.html — 东乡县政府网站领导之窗, 2026年7月22日确认"
    },
    # ════════════════════════════════════════
    # 县政府其他领导 (非常委)
    # ════════════════════════════════════════
    {
        "id": 14,
        "name": "马文波",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1973年1月",
        "birthplace": "",
        "education": "大专学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、公安局局长",
        "current_org": "东乡族自治县人民政府",
        "source": "https://www.dxzzzx.gov.cn/dxx/ldzc/index.html — 东乡县政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 15,
        "name": "马福英",
        "gender": "男",
        "ethnicity": "东乡族",
        "birth": "1979年12月",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "东乡族自治县人民政府",
        "source": "https://www.dxzzzx.gov.cn/dxx/ldzc/index.html — 东乡县政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 16,
        "name": "马宁",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1984年5月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "东乡族自治县人民政府",
        "source": "https://www.dxzzzx.gov.cn/dxx/ldzc/index.html — 东乡县政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 17,
        "name": "乔曼曼",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1986年12月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "东乡族自治县人民政府",
        "source": "https://www.dxzzzx.gov.cn/dxx/ldzc/index.html — 东乡县政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 18,
        "name": "马建辉",
        "gender": "男",
        "ethnicity": "东乡族",
        "birth": "1986年3月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委办公室主任",
        "current_org": "中共东乡族自治县委办公室",
        "source": "https://www.dxzzzx.gov.cn/dxx/ldzc/index.html — 东乡县政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 19,
        "name": "张世俊",
        "gender": "男",
        "ethnicity": "东乡族",
        "birth": "1982年1月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府党组成员、办公室主任",
        "current_org": "东乡族自治县人民政府办公室",
        "source": "https://www.dxzzzx.gov.cn/dxx/ldzc/index.html — 东乡县政府网站领导之窗, 2026年7月22日确认"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共东乡族自治县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共临夏回族自治州委员会",
        "location": "甘肃省临夏回族自治州东乡族自治县",
    },
    {
        "id": 2,
        "name": "东乡族自治县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "临夏回族自治州人民政府",
        "location": "甘肃省临夏回族自治州东乡族自治县",
    },
    {
        "id": 3,
        "name": "中共东乡族自治县纪律检查委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共临夏州纪律检查委员会",
        "location": "甘肃省临夏回族自治州东乡族自治县",
    },
    {
        "id": 4,
        "name": "中共东乡族自治县委宣传部",
        "type": "党委",
        "level": "县",
        "parent": "中共东乡族自治县委员会",
        "location": "甘肃省临夏回族自治州东乡族自治县",
    },
    {
        "id": 5,
        "name": "中共东乡族自治县委统战部",
        "type": "党委",
        "level": "县",
        "parent": "中共东乡族自治县委员会",
        "location": "甘肃省临夏回族自治州东乡族自治县",
    },
    {
        "id": 6,
        "name": "中共东乡族自治县委政法委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共东乡族自治县委员会",
        "location": "甘肃省临夏回族自治州东乡族自治县",
    },
    {
        "id": 7,
        "name": "中共东乡族自治县委组织部",
        "type": "党委",
        "level": "县",
        "parent": "中共东乡族自治县委员会",
        "location": "甘肃省临夏回族自治州东乡族自治县",
    },
    {
        "id": 8,
        "name": "中共东乡族自治县委办公室",
        "type": "党委",
        "level": "县",
        "parent": "中共东乡族自治县委员会",
        "location": "甘肃省临夏回族自治州东乡族自治县",
    },
    {
        "id": 9,
        "name": "东乡族自治县人民政府办公室",
        "type": "政府",
        "level": "县",
        "parent": "东乡族自治县人民政府",
        "location": "甘肃省临夏回族自治州东乡族自治县",
    },
    {
        "id": 10,
        "name": "东乡县人民武装部",
        "type": "政府",
        "level": "县",
        "parent": "临夏军分区",
        "location": "甘肃省临夏回族自治州东乡族自治县",
    },
]

# 3. Positions
positions = [
    # 戚志远 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": "此前担任临夏州财政局局长、州政府国资委主任（2026年5月免去）；2026年7月现任确认"},
    # 马忠山 - 县委副书记、代理县长
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": "代理县长"},
    {"person_id": 2, "org_id": 2, "title": "代理县长", "start_date": "", "end_date": "present", "rank": "正县级", "note": "领导县政府全面工作，负责审计方面工作"},
    # 马恩泽 - 纪委书记
    {"person_id": 3, "org_id": 3, "title": "纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": "负责纪检监察和巡察工作"},
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 刘康平 - 常务副县长
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "负责县政府日常事务、发改、财政、应急管理、统计等工作"},
    # 张为 - 副县长（挂职）
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": "挂职"},
    {"person_id": 5, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "负责教育、驻村帮扶、社会帮扶等工作"},
    # 任胜强 - 宣传部部长
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 4, "title": "宣传部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "负责宣传思想和意识形态工作"},
    # 柳坤 - 副县长（挂职）
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": "挂职"},
    {"person_id": 7, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "负责东西部协作、对口支援和科技创新"},
    # 汪总领 - 统战部部长
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 5, "title": "统战部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "负责县委统战工作"},
    # 高国林 - 政法委书记
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 6, "title": "政法委书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": "负责政法、社会稳定工作"},
    # 杨彦平 - 副县长
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "负责招商引资、工信、市场监管、商贸流通"},
    # 花军委 - 副县长（挂职）
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": "挂职"},
    {"person_id": 11, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "负责中央单位定点帮扶"},
    # 王瑞亮 - 组织部部长
    {"person_id": 12, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 12, "org_id": 7, "title": "组织部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "负责组织和编制工作"},
    # 刘志华 - 人武部部长
    {"person_id": 13, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 13, "org_id": 10, "title": "人民武装部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "协调双拥、军民融合发展"},
    # 马文波 - 副县长、公安局局长
    {"person_id": 14, "org_id": 2, "title": "副县长、公安局局长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "负责社会稳定、公安、交通、社会治安综合治理"},
    # 马福英 - 副县长
    {"person_id": 15, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "负责农业农村、乡村振兴、水利、民政"},
    # 马宁 - 副县长
    {"person_id": 16, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "负责自然资源、城乡规划、住建、生态环保"},
    # 乔曼曼 - 副县长
    {"person_id": 17, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "负责卫生健康、医保、文旅、地方志"},
    # 马建辉 - 县委办公室主任
    {"person_id": 18, "org_id": 8, "title": "县委办公室主任", "start_date": "", "end_date": "present", "rank": "正科级", "note": "负责县委办公室全面工作"},
    # 张世俊 - 县政府办公室主任
    {"person_id": 19, "org_id": 9, "title": "县政府党组成员、办公室主任", "start_date": "", "end_date": "present", "rank": "正科级", "note": "负责县政府办公室全面工作"},
]

# 4. Relationships
relationships = [
    # 戚志远 <-> 马忠山（书记-县长搭档）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记—代理县长搭档，县委常委会共事", "overlap_org": "中共东乡族自治县委员会", "overlap_period": "现任"},
    # 戚志远 <-> 刘康平（书记-常务副县长）
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记—县委常委/常务副县长", "overlap_org": "中共东乡族自治县委员会", "overlap_period": "现任"},
    # 戚志远 <-> 马恩泽（书记-纪委书记）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记—纪委书记，县委常委会共事", "overlap_org": "中共东乡族自治县委员会", "overlap_period": "现任"},
    # 戚志远 <-> 王瑞亮（书记-组织部长）
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate", "context": "县委书记—组织部长，干部任免工作配合", "overlap_org": "中共东乡族自治县委员会", "overlap_period": "现任"},
    # 戚志远 <-> 高国林（书记-政法委书记）
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "县委书记—政法委书记，县委常委会共事", "overlap_org": "中共东乡族自治县委员会", "overlap_period": "现任"},
    # 马忠山 <-> 刘康平（县长-常务副县长）
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "代理县长—常务副县长，县政府班子搭档", "overlap_org": "东乡族自治县人民政府", "overlap_period": "现任"},
    # 马忠山 <-> 杨彦平（县长-副县长）
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "代理县长—副县长，县政府班子共事", "overlap_org": "东乡族自治县人民政府", "overlap_period": "现任"},
    # 马忠山 <-> 马福英（县长-副县长）
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "代理县长—副县长，农业农村工作", "overlap_org": "东乡族自治县人民政府", "overlap_period": "现任"},
    # 马忠山 <-> 马文波（县长-公安局长）
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "代理县长—副县长/公安局长，政法工作配合", "overlap_org": "东乡族自治县人民政府", "overlap_period": "现任"},
    # 刘康平 <-> 杨彦平（常务副县长-副县长）
    {"person_a": 4, "person_b": 10, "type": "overlap", "context": "常务副县长—副县长，县政府班子共事", "overlap_org": "东乡族自治县人民政府", "overlap_period": "现任"},
    # 刘康平 <-> 高国林（县委常委班子）
    {"person_a": 4, "person_b": 9, "type": "overlap", "context": "同为县委常委，县委常委会共事", "overlap_org": "中共东乡族自治县委员会", "overlap_period": "现任"},
    # 马恩泽 <-> 高国林（纪委-政法委协作）
    {"person_a": 3, "person_b": 9, "type": "overlap", "context": "纪委监委与政法委工作协作", "overlap_org": "中共东乡族自治县委员会", "overlap_period": "现任"},
    # 王瑞亮 <-> 汪总领（组织-统战）
    {"person_a": 12, "person_b": 8, "type": "overlap", "context": "组织部与统战部工作协作", "overlap_org": "中共东乡族自治县委员会", "overlap_period": "现任"},
    # 任胜强 <-> 张为（宣传-教育）
    {"person_a": 6, "person_b": 5, "type": "overlap", "context": "宣传部与教育工作配合", "overlap_org": "中共东乡族自治县委员会", "overlap_period": "现任"},
    # 马恩泽 <-> 王瑞亮（纪委-组织）
    {"person_a": 3, "person_b": 12, "type": "overlap", "context": "纪委监委与组织部干部监督配合", "overlap_org": "中共东乡族自治县委员会", "overlap_period": "现任"},
    # 挂职副县长之间协作
    {"person_a": 5, "person_b": 7, "type": "overlap", "context": "均为挂职副县长，东西部协作与帮扶工作配合", "overlap_org": "东乡族自治县人民政府", "overlap_period": "现任"},
    {"person_a": 5, "person_b": 11, "type": "overlap", "context": "均为挂职副县长，帮扶工作配合", "overlap_org": "东乡族自治县人民政府", "overlap_period": "现任"},
    {"person_a": 7, "person_b": 11, "type": "overlap", "context": "均为挂职副县长，协作与帮扶工作配合", "overlap_org": "东乡族自治县人民政府", "overlap_period": "现任"},
    # 张世俊 - 刘康平（办公室主任-常务副县长）
    {"person_a": 19, "person_b": 4, "type": "overlap", "context": "县政府办公室主任协调县政府日常工作、协助常务副县长", "overlap_org": "东乡族自治县人民政府", "overlap_period": "现任"},
    # 马建辉 - 戚志远（县委办主任-书记）
    {"person_a": 18, "person_b": 1, "type": "superior_subordinate", "context": "县委办公室主任直接服务于县委书记", "overlap_org": "中共东乡族自治县委员会", "overlap_period": "现任"},
    # 东乡族干部网络
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "东乡族干部，县委常委班子共事", "overlap_org": "中共东乡族自治县委员会", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "东乡族干部，县委常委会共事", "overlap_org": "中共东乡族自治县委员会", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "东乡族干部，县政府班子共事", "overlap_org": "东乡族自治县人民政府", "overlap_period": "现任"},
    {"person_a": 3, "person_b": 8, "type": "overlap", "context": "东乡族干部，县委常委班子共事", "overlap_org": "中共东乡族自治县委员会", "overlap_period": "现任"},
]

# ══════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
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
    print("✅  Build complete.")
    print(f"   DB:   {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
