#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
独山县领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Dushan County leadership network.

Level: 县
Province: 贵州省
Parent City: 黔南布依族苗族自治州
Region: 独山县
Targets: 县委书记 & 县长

Research Sources:
- dushan.gov.cn — 独山县人民政府门户网站 (2026年7月)
  - 领导之窗·县委: https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xw/
  - 领导之窗·县政府: https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xzf/
  - 领导之窗·县人大: https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xrd/
  - 领导之窗·县政协: https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xzx/
  - 张正伟简历: http://www.dushan.gov.cn/zwgk/zfgk/ldzc/xw/202511/t20251127_88989600.html
  - 龚传书简历: http://www.dushan.gov.cn/zwgk/zfgk/ldzc/xzf/202208/t20220822_76141417.html

Confirmed officeholders (as of 2026-07-23, from dushan.gov.cn official leadership pages):
- 县委书记: 张正伟 (1978年12月生，男，汉族，研究生学历)
- 县委副书记、县长: 龚传书 (1979年6月生，男，汉族，研究生学历)
- 县委常委、县委政法委书记: 罗毅
- 县委常委、县委办公室主任: 李崇骁
- 县委常委、常务副县长: 刘峰
- 县委常委、县委组织部部长: 文斯奇
- 县委常委、县纪委书记: 张磊
- 县人大常委会党组书记、主任: 杨李林
- 县政协党组书记、主席: 陈刚

Note: Most biographical details (birthplace, education institutions, early career)
remain to be filled from external sources.

Research Date: 2026-07-23
"""

import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths ──
SLUG = "独山县"
AS_OF = "2026-07-23"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "张正伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年12月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记、兼贵州独山经济开发区党工委书记",
        "current_org": "中共独山县委员会",
        "source": "https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xw/ — 独山县人民政府门户网站领导之窗, accessed 2026-07-23"
    },
    {
        "id": 2,
        "name": "龚传书",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年6月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县人民政府党组书记、县长、兼贵州独山经济开发区党工委副书记、管理委员会主任",
        "current_org": "独山县人民政府",
        "source": "https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xzf/ — 独山县人民政府门户网站领导之窗, accessed 2026-07-23"
    },
    # ════════════════════════════════════════
    # 县委常委
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "罗毅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委政法委书记",
        "current_org": "中共独山县委员会政法委员会",
        "source": "https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xw/ — 独山县人民政府门户网站领导之窗, accessed 2026-07-23"
    },
    {
        "id": 4,
        "name": "李崇骁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委办公室主任、县直属机关工委书记",
        "current_org": "中共独山县委员会办公室",
        "source": "https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xw/ — 独山县人民政府门户网站领导之窗, accessed 2026-07-23"
    },
    {
        "id": 5,
        "name": "刘峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县人民政府党组副书记、常务副县长、县国有企业工作委员会书记",
        "current_org": "独山县人民政府",
        "source": "https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xzf/ — 独山县人民政府门户网站领导之窗, accessed 2026-07-23"
    },
    {
        "id": 6,
        "name": "文斯奇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委组织部部长、县委党校校长（兼）",
        "current_org": "中共独山县委组织部",
        "source": "https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xw/ — 独山县人民政府门户网站领导之窗, accessed 2026-07-23"
    },
    {
        "id": 7,
        "name": "张磊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监察委员会主任、贵州独山经济开发区党工委委员、纪检监察工委书记（兼）",
        "current_org": "中共独山县纪律检查委员会",
        "source": "https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xw/ — 独山县人民政府门户网站领导之窗, accessed 2026-07-23"
    },
    # ════════════════════════════════════════
    # 县政府副县长（非县委常委）
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "陈明春",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人民政府党组成员、副县长",
        "current_org": "独山县人民政府",
        "source": "https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xzf/ — 独山县人民政府门户网站领导之窗, accessed 2026-07-23"
    },
    {
        "id": 9,
        "name": "宋慧",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人民政府党组成员、副县长、县卫健工委书记、县教育局工委副书记、县红十字会会长、县计划生育协会会长候选人",
        "current_org": "独山县人民政府",
        "source": "https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xzf/ — 独山县人民政府门户网站领导之窗, accessed 2026-07-23"
    },
    {
        "id": 10,
        "name": "刘流",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人民政府党组成员、副县长",
        "current_org": "独山县人民政府",
        "source": "https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xzf/ — 独山县人民政府门户网站领导之窗, accessed 2026-07-23"
    },
    {
        "id": 11,
        "name": "王其林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人民政府党组成员、副县长",
        "current_org": "独山县人民政府",
        "source": "https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xzf/ — 独山县人民政府门户网站领导之窗, accessed 2026-07-23"
    },
    {
        "id": 12,
        "name": "孙富斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人民政府党组成员、县人民政府办公室党组书记、主任",
        "current_org": "独山县人民政府办公室",
        "source": "https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xzf/ — 独山县人民政府门户网站领导之窗, accessed 2026-07-23"
    },
    # ════════════════════════════════════════
    # 县人大常委会
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "杨李林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会党组书记、主任",
        "current_org": "独山县人民代表大会常务委员会",
        "source": "https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xrd/ — 独山县人民政府门户网站领导之窗, accessed 2026-07-23"
    },
    {
        "id": 14,
        "name": "张永扬",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会党组副书记、副主任、三级调研员",
        "current_org": "独山县人民代表大会常务委员会",
        "source": "https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xrd/ — 独山县人民政府门户网站领导之窗, accessed 2026-07-23"
    },
    {
        "id": 15,
        "name": "杨正江",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会党组成员、副主任、兼县总工会主席",
        "current_org": "独山县人民代表大会常务委员会",
        "source": "https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xrd/ — 独山县人民政府门户网站领导之窗, accessed 2026-07-23"
    },
    {
        "id": 16,
        "name": "罗小龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会党组成员、副主任",
        "current_org": "独山县人民代表大会常务委员会",
        "source": "https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xrd/ — 独山县人民政府门户网站领导之窗, accessed 2026-07-23"
    },
    {
        "id": 17,
        "name": "黎兴勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会党组成员、副主任",
        "current_org": "独山县人民代表大会常务委员会",
        "source": "https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xrd/ — 独山县人民政府门户网站领导之窗, accessed 2026-07-23"
    },
    {
        "id": 18,
        "name": "艾其科",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会党组成员、副主任",
        "current_org": "独山县人民代表大会常务委员会",
        "source": "https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xrd/ — 独山县人民政府门户网站领导之窗, accessed 2026-07-23"
    },
    # ════════════════════════════════════════
    # 县政协
    # ════════════════════════════════════════
    {
        "id": 19,
        "name": "陈刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协党组书记、主席",
        "current_org": "中国人民政治协商会议独山县委员会",
        "source": "https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xzx/ — 独山县人民政府门户网站领导之窗, accessed 2026-07-23"
    },
    {
        "id": 20,
        "name": "莫正勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协党组副书记、副主席",
        "current_org": "中国人民政治协商会议独山县委员会",
        "source": "https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xzx/ — 独山县人民政府门户网站领导之窗, accessed 2026-07-23"
    },
    {
        "id": 21,
        "name": "王国斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协党组成员、副主席",
        "current_org": "中国人民政治协商会议独山县委员会",
        "source": "https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xzx/ — 独山县人民政府门户网站领导之窗, accessed 2026-07-23"
    },
    {
        "id": 22,
        "name": "卢延明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协党组成员、副主席",
        "current_org": "中国人民政治协商会议独山县委员会",
        "source": "https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xzx/ — 独山县人民政府门户网站领导之窗, accessed 2026-07-23"
    },
    {
        "id": 23,
        "name": "欧朝武",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协党组成员、副主席",
        "current_org": "中国人民政治协商会议独山县委员会",
        "source": "https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xzx/ — 独山县人民政府门户网站领导之窗, accessed 2026-07-23"
    },
    {
        "id": 24,
        "name": "蒙继春",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协党组成员、副主席",
        "current_org": "中国人民政治协商会议独山县委员会",
        "source": "https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xzx/ — 独山县人民政府门户网站领导之窗, accessed 2026-07-23"
    },
    {
        "id": 25,
        "name": "罗家琼",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席、县财政局局长",
        "current_org": "中国人民政治协商会议独山县委员会",
        "source": "https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xzx/ — 独山县人民政府门户网站领导之窗, accessed 2026-07-23"
    },
    {
        "id": 26,
        "name": "周友学",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协党组成员、机关党组书记、秘书长",
        "current_org": "中国人民政治协商会议独山县委员会",
        "source": "https://www.dushan.gov.cn/zwgk/zfgk/ldzc/xzx/ — 独山县人民政府门户网站领导之窗, accessed 2026-07-23"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共独山县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共黔南布依族苗族自治州委员会",
        "location": "贵州省黔南布依族苗族自治州独山县"
    },
    {
        "id": 2,
        "name": "独山县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "黔南布依族苗族自治州人民政府",
        "location": "贵州省黔南布依族苗族自治州独山县"
    },
    {
        "id": 3,
        "name": "中共独山县纪律检查委员会",
        "type": "纪委",
        "level": "县级",
        "parent": "中共黔南布依族苗族自治州纪律检查委员会",
        "location": "贵州省黔南布依族苗族自治州独山县"
    },
    {
        "id": 4,
        "name": "独山县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "黔南布依族苗族自治州人民代表大会常务委员会",
        "location": "贵州省黔南布依族苗族自治州独山县"
    },
    {
        "id": 5,
        "name": "中国人民政治协商会议独山县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "中国人民政治协商会议黔南布依族苗族自治州委员会",
        "location": "贵州省黔南布依族苗族自治州独山县"
    },
    {
        "id": 6,
        "name": "中共独山县委政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共独山县委员会",
        "location": "贵州省黔南布依族苗族自治州独山县"
    },
    {
        "id": 7,
        "name": "中共独山县委办公室",
        "type": "党委",
        "level": "县级",
        "parent": "中共独山县委员会",
        "location": "贵州省黔南布依族苗族自治州独山县"
    },
    {
        "id": 8,
        "name": "中共独山县委组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共独山县委员会",
        "location": "贵州省黔南布依族苗族自治州独山县"
    },
    {
        "id": 9,
        "name": "独山县人民政府办公室",
        "type": "政府",
        "level": "县级",
        "parent": "独山县人民政府",
        "location": "贵州省黔南布依族苗族自治州独山县"
    },
    {
        "id": 10,
        "name": "贵州独山经济开发区",
        "type": "开发区",
        "level": "县级",
        "parent": "独山县人民政府",
        "location": "贵州省黔南布依族苗族自治州独山县"
    },
    {
        "id": 11,
        "name": "独山县总工会",
        "type": "群团",
        "level": "县级",
        "parent": "中共独山县委员会",
        "location": "贵州省黔南布依族苗族自治州独山县"
    },
    {
        "id": 12,
        "name": "独山县财政局",
        "type": "政府",
        "level": "县级",
        "parent": "独山县人民政府",
        "location": "贵州省黔南布依族苗族自治州独山县"
    },
]

# 3. Positions - map persons to organizations with titles
positions = [
    # 张正伟
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持县委全面工作"},
    {"person_id": 1, "org_id": 10, "title": "贵州独山经济开发区党工委书记（兼）", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 龚传书
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县人民政府党组书记、县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "领导县政府全面工作"},
    {"person_id": 2, "org_id": 10, "title": "贵州独山经济开发区党工委副书记、管委会主任（兼）", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 罗毅
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 6, "title": "县委政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 李崇骁
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 7, "title": "县委办公室主任、县直属机关工委书记", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 刘峰
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "县人民政府党组副书记、常务副县长、县国有企业工作委员会书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 文斯奇
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 8, "title": "县委组织部部长、县委党校校长（兼）", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 张磊
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 3, "title": "县纪委书记、县监察委员会主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼贵州独山经济开发区党工委委员、纪检监察工委书记"},
    # 陈明春 (副县长)
    {"person_id": 8, "org_id": 2, "title": "县人民政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 宋慧 (副县长)
    {"person_id": 9, "org_id": 2, "title": "县人民政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼县卫健工委书记、县教育局工委副书记"},
    # 刘流 (副县长)
    {"person_id": 10, "org_id": 2, "title": "县人民政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 王其林 (副县长)
    {"person_id": 11, "org_id": 2, "title": "县人民政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 孙富斌 (县政府办公室主任)
    {"person_id": 12, "org_id": 2, "title": "县人民政府党组成员", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
    {"person_id": 12, "org_id": 9, "title": "县人民政府办公室党组书记、主任", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
    # 杨李林
    {"person_id": 13, "org_id": 4, "title": "县人大常委会党组书记、主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持县人大常委会及党组全面工作"},
    # 张永扬
    {"person_id": 14, "org_id": 4, "title": "县人大常委会党组副书记、副主任、三级调研员", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 杨正江
    {"person_id": 15, "org_id": 4, "title": "县人大常委会党组成员、副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼县总工会主席"},
    {"person_id": 15, "org_id": 11, "title": "县总工会主席（兼）", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 罗小龙
    {"person_id": 16, "org_id": 4, "title": "县人大常委会党组成员、副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 黎兴勇
    {"person_id": 17, "org_id": 4, "title": "县人大常委会党组成员、副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 艾其科
    {"person_id": 18, "org_id": 4, "title": "县人大常委会党组成员、副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 陈刚
    {"person_id": 19, "org_id": 5, "title": "县政协党组书记、主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持县政协全面工作"},
    # 莫正勇
    {"person_id": 20, "org_id": 5, "title": "县政协党组副书记、副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 王国斌
    {"person_id": 21, "org_id": 5, "title": "县政协党组成员、副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 卢延明
    {"person_id": 22, "org_id": 5, "title": "县政协党组成员、副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 欧朝武
    {"person_id": 23, "org_id": 5, "title": "县政协党组成员、副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 蒙继春
    {"person_id": 24, "org_id": 5, "title": "县政协党组成员、副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 罗家琼
    {"person_id": 25, "org_id": 5, "title": "县政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 25, "org_id": 12, "title": "县财政局局长", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
    # 周友学
    {"person_id": 26, "org_id": 5, "title": "县政协党组成员、机关党组书记、秘书长", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
]

# 4. Relationships (evidence-based, person-to-person)
relationships = [
    # 张正伟 ↔ 龚传书 (党政搭档)
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "县委书记与县长党政搭档，共同主持独山县全面工作",
        "overlap_org": "中共独山县委员会/独山县人民政府",
        "overlap_period": "present",
    },
    # 张正伟 ↔ 刘峰 (县委常委班子成员)
    {
        "person_a": 1,
        "person_b": 5,
        "type": "overlap",
        "context": "县委常委班子，张正伟为书记，刘峰为县委常委、常务副县长",
        "overlap_org": "中共独山县委员会",
        "overlap_period": "present",
    },
    # 张正伟 ↔ 文斯奇 (组织部长归书记领导)
    {
        "person_a": 1,
        "person_b": 6,
        "type": "overlap",
        "context": "县委常委班子，文斯奇为县委常委、组织部部长",
        "overlap_org": "中共独山县委员会",
        "overlap_period": "present",
    },
    # 张正伟 ↔ 罗毅 (政法委书记归书记领导)
    {
        "person_a": 1,
        "person_b": 3,
        "type": "overlap",
        "context": "县委常委班子，罗毅为县委常委、政法委书记",
        "overlap_org": "中共独山县委员会",
        "overlap_period": "present",
    },
    # 张正伟 ↔ 李崇骁 (办公室主任关联)
    {
        "person_a": 1,
        "person_b": 4,
        "type": "overlap",
        "context": "县委常委班子，李崇骁为县委常委、县委办公室主任",
        "overlap_org": "中共独山县委员会",
        "overlap_period": "present",
    },
    # 张正伟 ↔ 张磊 (纪委书记关联)
    {
        "person_a": 1,
        "person_b": 7,
        "type": "overlap",
        "context": "县委常委班子，张磊为县委常委、县纪委书记",
        "overlap_org": "中共独山县委员会",
        "overlap_period": "present",
    },
    # 龚传书 ↔ 刘峰 (县长-常务副县长搭档)
    {
        "person_a": 2,
        "person_b": 5,
        "type": "overlap",
        "context": "县长与常务副县长搭档关系",
        "overlap_org": "独山县人民政府",
        "overlap_period": "present",
    },
    # 龚传书 ↔ 陈明春 (县长-副县长)
    {
        "person_a": 2,
        "person_b": 8,
        "type": "overlap",
        "context": "县政府班子成员",
        "overlap_org": "独山县人民政府",
        "overlap_period": "present",
    },
    # 龚传书 ↔ 宋慧 (县长-副县长)
    {
        "person_a": 2,
        "person_b": 9,
        "type": "overlap",
        "context": "县政府班子成员",
        "overlap_org": "独山县人民政府",
        "overlap_period": "present",
    },
    # 龚传书 ↔ 刘流 (县长-副县长)
    {
        "person_a": 2,
        "person_b": 10,
        "type": "overlap",
        "context": "县政府班子成员",
        "overlap_org": "独山县人民政府",
        "overlap_period": "present",
    },
    # 龚传书 ↔ 王其林 (县长-副县长)
    {
        "person_a": 2,
        "person_b": 11,
        "type": "overlap",
        "context": "县政府班子成员",
        "overlap_org": "独山县人民政府",
        "overlap_period": "present",
    },
    # 杨李林 ↔ 张永扬 (人大主任-副主任)
    {
        "person_a": 13,
        "person_b": 14,
        "type": "overlap",
        "context": "县人大常委会主任-副主任搭档",
        "overlap_org": "独山县人民代表大会常务委员会",
        "overlap_period": "present",
    },
    # 陈刚 ↔ 莫正勇 (政协主席-副主席)
    {
        "person_a": 19,
        "person_b": 20,
        "type": "overlap",
        "context": "县政协领导班子成员",
        "overlap_org": "中国人民政治协商会议独山县委员会",
        "overlap_period": "present",
    },
]


# =========================================================================
# HELPERS
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(current_post):
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp and "纪委" not in cp:
        return "255,50,50"
    if "县长" in cp and "副" not in cp:
        return "50,100,255"
    if "副书记" in cp:
        return "220,80,80"
    if "常委" in cp and "纪委" in cp:
        return "255,165,0"
    if "常委" in cp:
        return "180,100,180"
    if "副" in cp and ("县长" in cp or "区长" in cp):
        return "100,150,220"
    if "主任" in cp or "人大" in cp:
        return "60,180,60"
    if "主席" in cp or "政协" in cp:
        return "60,180,60"
    if "副县长" in cp:
        return "100,150,220"
    return "100,100,100"


def person_size(current_post):
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp and "纪委" not in cp:
        return "20.0"
    if "县长" in cp and "副" not in cp:
        return "18.0"
    if "副书记" in cp:
        return "15.0"
    if "常委" in cp:
        return "12.0"
    if "副主任" in cp or "副主席" in cp or "副县长" in cp:
        return "12.0"
    if "主任" in cp or "主席" in cp:
        return "14.0"
    return "10.0"


def person_shape(current_post):
    cp = current_post or ""
    if "书记" in cp:
        return "square"
    if "人大" in cp or "政协" in cp:
        return "diamond"
    if "副" in cp:
        return "triangle"
    return "circle"


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "开发区": "200,255,200",
        "纪委": "255,200,150",
        "群团": "255,220,255",
    }
    return colors.get(org_type, "200,200,200")


def build_person_json(person, timeline, rels, sources):
    p = person
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "贵州省",
            "city": "黔南布依族苗族自治州",
            "region": "独山县",
            "job": p.get("current_post", "").split("、")[-1] if "、" in p.get("current_post", "") else p.get("current_post", "").split("、")[0].split("兼")[0].strip("、"),
            "task_id": "guizhou_独山县",
            "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"dushan_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [
                {
                    "period": "",
                    "institution": "",
                    "major": "",
                    "degree": "",
                    "study_type": "unknown",
                    "source_ids": []
                }
            ],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source", "")
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "正处级" if ("书记" in p.get("current_post","") or "县长" in p.get("current_post","")) else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": rels,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "No risk signals found through available public sources",
            "date": "",
            "confidence": "unverified",
            "source_ids": []
        }],
        "source_register": sources,
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"Earlier career timeline before current role for {p['name']}"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"Complete career timeline before current role for {p['name']} - full position history",
                "why_it_matters": "Cannot assess career pattern, promotion velocity, or network building without full timeline",
                "suggested_queries": [f"{p['name']} 简历 独山", f"{p['name']} 任职经历", f"{p['name']} 百度百科"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"Birthplace and native place for {p['name']}",
                "why_it_matters": "Essential for identity deduplication and native-place network analysis",
                "suggested_queries": [f"{p['name']} 籍贯"],
                "last_attempted": AS_OF
            },
            {
                "priority": "medium",
                "question": f"Education details (institution, major, degree type) for {p['name']}",
                "why_it_matters": "Alumni networks are important relationship channels",
                "suggested_queries": [f"{p['name']} 毕业"],
                "last_attempted": AS_OF
            }
        ]
    }


def build_person_jsons():
    """Build and write person JSON files for 张正伟 and 龚传书."""
    now = AS_OF.replace("-", "")

    sources = [
        {"id": "S001", "title": "独山县人民政府门户网站·领导之窗",
         "url": "https://www.dushan.gov.cn/zwgk/zfgk/ldzc/",
         "publisher": "独山县人民政府",
         "published_at": "",
         "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "Official leadership roster page with biographies"},
        {"id": "S002", "title": "张正伟简历页",
         "url": "http://www.dushan.gov.cn/zwgk/zfgk/ldzc/xw/202511/t20251127_88989600.html",
         "publisher": "独山县人民政府",
         "published_at": "2025-11-27",
         "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "县委书记张正伟官方简历"},
        {"id": "S003", "title": "龚传书简历页",
         "url": "http://www.dushan.gov.cn/zwgk/zfgk/ldzc/xzf/202208/t20220822_76141417.html",
         "publisher": "独山县人民政府",
         "published_at": "2022-08-22",
         "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "县长龚传书官方简历"},
    ]

    # ── 张正伟 person JSON ──
    zzw_timeline = [
        {"start": "", "end": "present",
         "org": "中共独山县委员会",
         "title": "县委书记、兼贵州独山经济开发区党工委书记",
         "level": "正处级",
         "location": "贵州省黔南州独山县",
         "system": "party",
         "rank": "正处级",
         "is_key_promotion": True,
         "notes": "主持县委全面工作；1978年12月生，汉族，研究生学历",
         "confidence": "confirmed",
         "source_ids": ["S001", "S002"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到张正伟任独山县委书记之前的完整履历",
         "confidence": "unverified",
         "source_ids": []},
    ]
    zzw_relationships = [
        {"person": "龚传书", "person_id": "dushan_龚传书",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "目前独山县县委书记与县长党政搭档",
         "overlap_org": "中共独山县委员会/独山县人民政府",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "刘峰", "person_id": "dushan_刘峰",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "县委常委班子，张正伟为班长",
         "overlap_org": "中共独山县委员会",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "文斯奇", "person_id": "dushan_文斯奇",
         "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "县委常委班子同事",
         "overlap_org": "中共独山县委员会",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "罗毅", "person_id": "dushan_罗毅",
         "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "县委常委班子同事",
         "overlap_org": "中共独山县委员会",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "李崇骁", "person_id": "dushan_李崇骁",
         "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "县委常委班子同事，李崇骁兼县委办公室主任",
         "overlap_org": "中共独山县委员会",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "张磊", "person_id": "dushan_张磊",
         "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "县委常委班子同事，张磊为县纪委书记",
         "overlap_org": "中共独山县委员会",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    zzw_json = build_person_json(persons[0], zzw_timeline, zzw_relationships, sources)
    zzw_json["investigation_scope"]["job"] = "县委书记"
    zzw_path = os.path.join(PERSONS_DIR, f"{now}-贵州省-黔南布依族苗族自治州-县委书记-张正伟.json")
    with open(zzw_path, "w", encoding="utf-8") as f:
        json.dump(zzw_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {zzw_path}")

    # ── 龚传书 person JSON ──
    gcs_timeline = [
        {"start": "", "end": "present",
         "org": "独山县人民政府",
         "title": "县委副书记、县人民政府党组书记、县长、兼贵州独山经济开发区党工委副书记、管理委员会主任",
         "level": "正处级",
         "location": "贵州省黔南州独山县",
         "system": "government",
         "rank": "正处级",
         "is_key_promotion": True,
         "notes": "领导县政府全面工作；1979年6月生，汉族，研究生学历",
         "confidence": "confirmed",
         "source_ids": ["S001", "S003"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到龚传书任独山县县长之前的完整履历",
         "confidence": "unverified",
         "source_ids": []},
    ]
    gcs_relationships = [
        {"person": "张正伟", "person_id": "dushan_张正伟",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "目前独山县县长与县委书记党政搭档",
         "overlap_org": "独山县人民政府/中共独山县委员会",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "刘峰", "person_id": "dushan_刘峰",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "县长与常务副县长搭档",
         "overlap_org": "独山县人民政府",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "陈明春", "person_id": "dushan_陈明春",
         "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "县政府班子成员",
         "overlap_org": "独山县人民政府",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "宋慧", "person_id": "dushan_宋慧",
         "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "县政府班子成员",
         "overlap_org": "独山县人民政府",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "刘流", "person_id": "dushan_刘流",
         "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "县政府班子成员",
         "overlap_org": "独山县人民政府",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "王其林", "person_id": "dushan_王其林",
         "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "县政府班子成员",
         "overlap_org": "独山县人民政府",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    gcs_json = build_person_json(persons[1], gcs_timeline, gcs_relationships, sources)
    gcs_json["investigation_scope"]["job"] = "县长"
    gcs_path = os.path.join(PERSONS_DIR, f"{now}-贵州省-黔南布依族苗族自治州-县长-龚传书.json")
    with open(gcs_path, "w", encoding="utf-8") as f:
        json.dump(gcs_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {gcs_path}")


# =========================================================================
# BUILD FUNCTIONS
# =========================================================================

def build_db():
    """Build SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '',
            party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '',
            source TEXT DEFAULT ''
        );

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );

        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute("""INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,
                       party_join,work_start,current_post,current_org,source)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
                     p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
                     p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""),
                     p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location)
                       VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"],
                     o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note)
                       VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"],
                     pos.get("start_date", ""), pos.get("end_date", ""),
                     pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period)
                       VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"], r["context"],
                     r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


def build_gexf():
    """Build GEXF graph file."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>{SLUG}领导班子关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes - persons
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        cp = p.get("current_post", "")
        color = person_color(cp)
        size = person_size(cp)
        shape = person_shape(cp)
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(cp)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o["type"])
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('        <viz:shape value="hexagon"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]+100000}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ person (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")


def build():
    os.makedirs(STAGING_DIR, exist_ok=True)
    print(f"=== Building {SLUG} data ===")
    print(f"Staging dir: {STAGING_DIR}")

    build_db()
    build_gexf()
    build_person_jsons()

    print(f"\n=== Build complete ===")


if __name__ == "__main__":
    build()
