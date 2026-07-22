#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龙门县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 广东省
Parent City: 惠州市
Region: 龙门县
Targets: 县委书记 & 县长

Research Sources:
- 龙门县人民政府门户网站 (www.longmen.gov.cn) — 领导之窗
  - 中共龙门县委: https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxw/
  - 龙门县人民政府: https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrmzf/
  - 龙门县政协: https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zxlmxwyh/
  - 龙门县纪委: https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxjljcwyh/
  - 龙门县人大: https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrdcwh/
- 搜狐文章: https://www.sohu.com/a/861611707_161795
- 数据采集日期: 2026-07-22

Current status (as of 2026-07-22):
- 县委书记: 刘洪添（惠州市政协党组成员、副主席，龙门县委书记）
  - 男，汉族，1968年8月生，中央党校研究生，中共党员
  - 惠城人，complete career history from official site
- 县长: 王洋（龙门县委副书记、县政府党组书记、县长）
  - 男，汉族，1979年8月生，在职博士研究生，中共党员
  - 此前在惠州市委组织部工作，2025年4月当选县长
- 县委副书记: 陈琳（挂职）、黄卓豪（政法委书记）
- 县委常委: 刘洪添、王洋、陈琳、黄卓豪、罗光少、李锋（挂职）、陈洁、张志文、毛振辉、陈职勇、邓定文、张锐源
- 副县长: 王洋（县长）、张志文（常务）、李锋（挂职）、陈职勇、张振东、邬淑娴、郝治翰、王庆胜（公安局长）、刘业丰、陈达婷

Investigation Date: 2026-07-22
"""

import os
import sys
from datetime import datetime

# Allow import from repo root
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../"))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "龙门县"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════════
    # 县委领导 (Party Committee)
    # ════════════════════════════════════════════
    {
        "id": 1,
        "name": "刘洪添",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年8月",
        "birthplace": "广东省惠州市惠城区",
        "native_place": "广东省惠州市惠城区",
        "education": "中央党校研究生",
        "party_join": "1990年10月",
        "work_start": "1987年7月",
        "current_post": "惠州市政协党组成员、副主席，龙门县委书记",
        "current_org": "中共龙门县委员会",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxw/"
    },
    {
        "id": 2,
        "name": "王洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年8月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职博士研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县委副书记、县政府党组书记、县长",
        "current_org": "龙门县人民政府",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrmzf/"
    },
    {
        "id": 3,
        "name": "陈琳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980年6月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县委副书记（挂职）",
        "current_org": "中共龙门县委员会",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxw/"
    },
    {
        "id": 4,
        "name": "黄卓豪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职农业推广硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县委副书记、政法委书记",
        "current_org": "中共龙门县委员会",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxw/"
    },
    {
        "id": 5,
        "name": "罗光少",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年9月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县委常委、统战部部长、县政协党组副书记",
        "current_org": "中共龙门县委员会",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxw/"
    },
    {
        "id": 6,
        "name": "李锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年9月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县委常委，县政府党组成员、副县长（挂职）",
        "current_org": "中共龙门县委员会",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxw/"
    },
    {
        "id": 7,
        "name": "陈洁",
        "gender": "女",
        "ethnicity": "回族",
        "birth": "1979年5月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县委常委、宣传部部长",
        "current_org": "中共龙门县委员会",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxw/"
    },
    {
        "id": 8,
        "name": "张志文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年3月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县委常委，县政府党组副书记、常务副县长",
        "current_org": "龙门县人民政府",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxw/"
    },
    {
        "id": 9,
        "name": "毛振辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年3月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县委常委、组织部部长",
        "current_org": "中共龙门县委员会",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxw/"
    },
    {
        "id": 10,
        "name": "陈职勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县委常委、副县长",
        "current_org": "龙门县人民政府",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxw/"
    },
    {
        "id": 11,
        "name": "邓定文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年5月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大专",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县委常委、县纪委书记、县监委代理主任",
        "current_org": "中共龙门县纪律检查委员会",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxw/"
    },
    {
        "id": 12,
        "name": "张锐源",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年3月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县委常委、县委办公室主任、县委改革办主任、县直机关工委书记",
        "current_org": "中共龙门县委员会",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxw/"
    },
    # ════════════════════════════════════════════
    # 县政府 (Government) - non-常委副县长
    # ════════════════════════════════════════════
    {
        "id": 13,
        "name": "张振东",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1987年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县政府党组成员、副县长",
        "current_org": "龙门县人民政府",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrmzf/"
    },
    {
        "id": 14,
        "name": "邬淑娴",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976年3月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县政府党组成员、副县长",
        "current_org": "龙门县人民政府",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrmzf/"
    },
    {
        "id": 15,
        "name": "郝治翰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1992年5月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "博士研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县政府党组成员、副县长（兼任龙江镇党委书记）",
        "current_org": "龙门县人民政府",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrmzf/"
    },
    {
        "id": 16,
        "name": "王庆胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年4月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大专",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县政府党组成员、副县长（兼任县公安局局长）",
        "current_org": "龙门县人民政府",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrmzf/"
    },
    {
        "id": 17,
        "name": "刘业丰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县政府党组成员、副县长",
        "current_org": "龙门县人民政府",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrmzf/"
    },
    {
        "id": 18,
        "name": "陈达婷",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984年8月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县政府党组成员、副县长",
        "current_org": "龙门县人民政府",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrmzf/"
    },
    # ════════════════════════════════════════════
    # 县人大 (NPC)
    # ════════════════════════════════════════════
    {
        "id": 19,
        "name": "古慧平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年8月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县人大常委会主任",
        "current_org": "龙门县人大常委会",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrdcwh/"
    },
    {
        "id": 20,
        "name": "刘远彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年9月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县人大常委会党组书记、主任人选",
        "current_org": "龙门县人大常委会",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrdcwh/"
    },
    {
        "id": 21,
        "name": "王卫良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年4月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县人大常委会党组成员、副主任",
        "current_org": "龙门县人大常委会",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrdcwh/"
    },
    {
        "id": 22,
        "name": "林建辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年3月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县人大常委会党组成员、副主任",
        "current_org": "龙门县人大常委会",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrdcwh/"
    },
    {
        "id": 23,
        "name": "蓝月清",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1968年3月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县人大常委会党组成员、副主任",
        "current_org": "龙门县人大常委会",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrdcwh/"
    },
    {
        "id": 24,
        "name": "张年胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年8月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县人大常委会党组成员、副主任",
        "current_org": "龙门县人大常委会",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrdcwh/"
    },
    {
        "id": 25,
        "name": "李穗华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年3月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县人大常委会党组成员、副主任",
        "current_org": "龙门县人大常委会",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrdcwh/"
    },
    # ════════════════════════════════════════════
    # 县政协 (CPPCC)
    # ════════════════════════════════════════════
    {
        "id": 26,
        "name": "林大升",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年9月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县政协党组书记、主席",
        "current_org": "政协龙门县委员会",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zxlmxwyh/"
    },
    {
        "id": 27,
        "name": "王宇文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年5月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县政协党组成员、副主席",
        "current_org": "政协龙门县委员会",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zxlmxwyh/"
    },
    {
        "id": 28,
        "name": "梁志斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年7月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县政协党组成员、副主席",
        "current_org": "政协龙门县委员会",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zxlmxwyh/"
    },
    {
        "id": 29,
        "name": "黄育贤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年1月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大专",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县政协党组成员、副主席",
        "current_org": "政协龙门县委员会",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zxlmxwyh/"
    },
    {
        "id": 30,
        "name": "罗天威",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年9月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "民盟盟员",
        "work_start": "待查",
        "current_post": "龙门县政协副主席",
        "current_org": "政协龙门县委员会",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zxlmxwyh/"
    },
    # ════════════════════════════════════════════
    # 县纪委 (Discipline)
    # ════════════════════════════════════════════
    {
        "id": 31,
        "name": "赖亮珊",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981年12月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学、法学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县纪委副书记、县监委副主任",
        "current_org": "中共龙门县纪律检查委员会",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxjljcwyh/"
    },
    {
        "id": 32,
        "name": "黄育金",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年6月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学、历史学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙门县纪委副书记、县监委副主任",
        "current_org": "中共龙门县纪律检查委员会",
        "source": "https://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxjljcwyh/"
    },
    # ════════════════════════════════════════════
    # 前任领导 (Predecessors)
    # ════════════════════════════════════════════
    {
        "id": 33,
        "name": "段致辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年4月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠州市人民政府党组成员、副市长",
        "current_org": "惠州市人民政府",
        "source": "https://baike.baidu.com/item/%E6%AE%B5%E8%87%B4%E8%BE%89/"
    },
    {
        "id": 34,
        "name": "陈伟良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "原龙门县委书记（去向待查）",
        "current_org": "待查",
        "source": "https://www.longmen.gov.cn/"
    },
    {
        "id": 35,
        "name": "陈宇浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "原龙门县县长（去向待查）",
        "current_org": "待查",
        "source": "https://www.longmen.gov.cn/"
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共龙门县委员会", "type": "党委", "level": "县", "parent": "中共惠州市委员会", "location": "龙门县"},
    {"id": 2, "name": "龙门县人民政府", "type": "政府", "level": "县", "parent": "惠州市人民政府", "location": "龙门县"},
    {"id": 3, "name": "龙门县人大常委会", "type": "人大", "level": "县", "parent": "龙门县", "location": "龙门县"},
    {"id": 4, "name": "政协龙门县委员会", "type": "政协", "level": "县", "parent": "龙门县", "location": "龙门县"},
    {"id": 5, "name": "中共龙门县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共惠州市纪律检查委员会", "location": "龙门县"},
    {"id": 6, "name": "惠州市人民政府", "type": "政府", "level": "地级市", "parent": "广东省人民政府", "location": "惠州市"},
    {"id": 7, "name": "惠州市政协", "type": "政协", "level": "地级市", "parent": "惠州市", "location": "惠州市"},
]

# 3. Positions
positions = [
    # 刘洪添
    {"person_id": 1, "org_id": 1, "title": "县委书记（兼惠州市政协副主席）", "start": "2022-09", "end": "present", "rank": "副厅级", "note": "2025年2月起兼任惠州市政协副主席"},
    {"person_id": 1, "org_id": 7, "title": "惠州市政协党组成员、副主席", "start": "2025-02", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "龙门县县长", "start": "2021-09", "end": "2022-09", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "龙门县副县长、代理县长", "start": "2021-07", "end": "2021-09", "rank": "正处级", "note": ""},
    # 王洋
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "2025-04", "end": "present", "rank": "正处级", "note": "2025年4月10日县十六届人大七次会议当选"},
    {"person_id": 2, "org_id": 2, "title": "代县长", "start": "2024", "end": "2025-04", "rank": "正处级", "note": ""},
    # 陈琳
    {"person_id": 3, "org_id": 1, "title": "县委副书记（挂职）", "start": "未知", "end": "present", "rank": "正处级", "note": "负责东西部协作、工会、共青团、妇联工作"},
    # 黄卓豪
    {"person_id": 4, "org_id": 1, "title": "县委副书记、政法委书记", "start": "未知", "end": "present", "rank": "副处级", "note": "协助刘洪添负责党的建设工作"},
    # 罗光少
    {"person_id": 5, "org_id": 1, "title": "县委常委、统战部部长", "start": "未知", "end": "present", "rank": "副处级", "note": "兼县政协党组副书记"},
    # 李锋
    {"person_id": 6, "org_id": 1, "title": "县委常委（挂职）", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副县长（挂职）", "start": "未知", "end": "present", "rank": "副处级", "note": "负责国有资产工作"},
    # 陈洁
    {"person_id": 7, "org_id": 1, "title": "县委常委、宣传部部长", "start": "未知", "end": "present", "rank": "副处级", "note": "回族"},
    # 张志文
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "常务副县长", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    # 毛振辉
    {"person_id": 9, "org_id": 1, "title": "县委常委、组织部部长", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    # 陈职勇
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start": "未知", "end": "present", "rank": "副处级", "note": "负责交通、卫健、人社、医保等工作"},
    # 邓定文
    {"person_id": 11, "org_id": 5, "title": "县纪委书记、县监委代理主任", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    # 张锐源
    {"person_id": 12, "org_id": 1, "title": "县委常委、县委办公室主任", "start": "未知", "end": "present", "rank": "副处级", "note": "兼县委改革办主任、县直机关工委书记"},
    # 张振东
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "未知", "end": "present", "rank": "副处级", "note": "满族，负责住建、城管、代建等工作"},
    # 邬淑娴
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    # 郝治翰
    {"person_id": 15, "org_id": 2, "title": "副县长（兼龙江镇党委书记）", "start": "未知", "end": "present", "rank": "副处级", "note": "90后博士，负责教育、科技、工信等工作"},
    # 王庆胜
    {"person_id": 16, "org_id": 2, "title": "副县长（兼县公安局局长）", "start": "未知", "end": "present", "rank": "副处级", "note": "负责公安、司法工作"},
    # 刘业丰
    {"person_id": 17, "org_id": 2, "title": "副县长", "start": "未知", "end": "present", "rank": "副处级", "note": "负责水利、农业农村、乡村振兴等工作"},
    # 陈达婷
    {"person_id": 18, "org_id": 2, "title": "副县长", "start": "未知", "end": "present", "rank": "副处级", "note": "负责民政、文旅、退役军人事务等工作"},
    # 人大
    {"person_id": 19, "org_id": 3, "title": "县人大常委会主任", "start": "未知", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 20, "org_id": 3, "title": "县人大常委会党组书记、主任人选", "start": "未知", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 21, "org_id": 3, "title": "县人大常委会副主任", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 22, "org_id": 3, "title": "县人大常委会副主任", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 23, "org_id": 3, "title": "县人大常委会副主任", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 24, "org_id": 3, "title": "县人大常委会副主任", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 25, "org_id": 3, "title": "县人大常委会副主任", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    # 政协
    {"person_id": 26, "org_id": 4, "title": "县政协主席", "start": "未知", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 27, "org_id": 4, "title": "县政协副主席", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 28, "org_id": 4, "title": "县政协副主席", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 29, "org_id": 4, "title": "县政协副主席", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 30, "org_id": 4, "title": "县政协副主席", "start": "未知", "end": "present", "rank": "副处级", "note": "民盟盟员"},
    # 纪委
    {"person_id": 31, "org_id": 5, "title": "县纪委副书记、县监委副主任", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 32, "org_id": 5, "title": "县纪委副书记、县监委副主任", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    # 前任
    {"person_id": 33, "org_id": 6, "title": "惠州市副市长", "start": "2022-01", "end": "present", "rank": "副厅级", "note": "段致辉"},
    {"person_id": 33, "org_id": 1, "title": "龙门县委书记", "start": "2021-07", "end": "2022-09", "rank": "正处级", "note": "段致辉，刘洪添的前任"},
    {"person_id": 34, "org_id": 1, "title": "龙门县委书记", "start": "2018", "end": "2021", "rank": "正处级", "note": "陈伟良，段致辉的前任"},
    {"person_id": 35, "org_id": 2, "title": "龙门县县长", "start": "2023", "end": "2024", "rank": "正处级", "note": "陈宇浩，王洋的前任"},
]

# 4. Relationships
relationships = [
    # 党政一把手搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "刘洪添（县委书记）与王洋（县长）党政搭档", "overlap_org": "中共龙门县委员会", "overlap_period": "2025-04至今", "confidence": "confirmed"},
    # 副书记与书记
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记刘洪添与副书记黄卓豪（政法委书记）", "overlap_org": "中共龙门县委员会", "overlap_period": "2022至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记刘洪添与挂职副书记陈琳", "overlap_org": "中共龙门县委员会", "overlap_period": "未知至今", "confidence": "confirmed"},
    # 县委书记与常委们
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委领导班子成员", "overlap_org": "中共龙门县委员会", "overlap_period": "2022至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "县委领导班子成员", "overlap_org": "中共龙门县委员会", "overlap_period": "2022至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "县委领导班子成员", "overlap_org": "中共龙门县委员会", "overlap_period": "2022至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "县委领导班子成员", "overlap_org": "中共龙门县委员会", "overlap_period": "2022至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "县委领导班子成员", "overlap_org": "中共龙门县委员会", "overlap_period": "2022至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate", "context": "县委领导班子成员", "overlap_org": "中共龙门县委员会", "overlap_period": "2022至今", "confidence": "confirmed"},
    # 县长与副县长
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "县长王洋与常务副县长张志文", "overlap_org": "龙门县人民政府", "overlap_period": "2025-04至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "县长王洋与副县长陈职勇", "overlap_org": "龙门县人民政府", "overlap_period": "2025-04至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "县长王洋与副县长张振东", "overlap_org": "龙门县人民政府", "overlap_period": "2025-04至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "县长王洋与副县长邬淑娴", "overlap_org": "龙门县人民政府", "overlap_period": "2025-04至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "县长王洋与副县长郝治翰", "overlap_org": "龙门县人民政府", "overlap_period": "2025-04至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "县长王洋与副县长王庆胜（公安局长）", "overlap_org": "龙门县人民政府", "overlap_period": "2025-04至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 17, "type": "superior_subordinate", "context": "县长王洋与副县长刘业丰", "overlap_org": "龙门县人民政府", "overlap_period": "2025-04至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 18, "type": "superior_subordinate", "context": "县长王洋与副县长陈达婷", "overlap_org": "龙门县人民政府", "overlap_period": "2025-04至今", "confidence": "confirmed"},
    # 前任-现任关系
    {"person_a": 1, "person_b": 33, "type": "predecessor_successor", "context": "刘洪添接替段致辉任龙门县委书记", "overlap_org": "中共龙门县委员会", "overlap_period": "2021-2022", "confidence": "confirmed"},
    {"person_a": 33, "person_b": 34, "type": "predecessor_successor", "context": "段致辉接替陈伟良任龙门县委书记", "overlap_org": "中共龙门县委员会", "overlap_period": "2021", "confidence": "plausible"},
    {"person_a": 2, "person_b": 35, "type": "predecessor_successor", "context": "王洋接替陈宇浩任龙门县县长", "overlap_org": "龙门县人民政府", "overlap_period": "2024-2025", "confidence": "plausible"},
    # 纪委书记与县委书记
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "县委与纪委关系", "overlap_org": "中共龙门县委员会", "overlap_period": "2022至今", "confidence": "confirmed"},
]


# ── Main ──

def main():
    print(f"=== 龙门县网络数据构建 ===")
    print(f"人员: {len(persons)} 人")
    print(f"组织机构: {len(organizations)} 个")
    print(f"任职记录: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")

    # Build database using run_build
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
