#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
惠州市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 地级市
Province: 广东省
Parent City: N/A (地级市)
Region: 惠州市
Targets: 市委书记 & 市长

Research Sources:
- 惠州市人民政府门户网站 (www.huizhou.gov.cn) — 领导之窗 (https://www.huizhou.gov.cn/zwgk/ldzc/index.html)
- 数据采集日期: 2026-07-22
- 官方来源确认，所有现任职务均有据可查

Current status (as of 2026-07-22):
- 市委书记: 刘吉（兼任市人大常委会主任）
- 市长: 陈宇航（市委副书记）
- 市委常委: 刘吉、陈宇航、赖建华、黄维玉、黄细花(女)、黎明、王滨、张军、黎炳盛、黄伟东
- 市委秘书长: 冯起忠
- 副市长: 王滨、曲维震、段致辉、赖志光、曹洪彬
- 市纪委书记: 黄伟东

Research Date: 2026-07-22
Evidence Note: Leadership roster confirmed from official government website (www.huizhou.gov.cn).
Biographical details for most figures are still to be collected from external sources;
incomplete fields are marked accordingly.
"""

import os
import sys
from datetime import datetime

# Allow import from repo root
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "惠州市"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════════
    # 市委领导
    # ════════════════════════════════════════════
    {
        "id": 1,
        "name": "刘吉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共惠州市委书记、市人大常委会主任",
        "current_org": "中共惠州市委员会",
        "source": "惠州市政府官网领导之窗 (confirmed) — 市委书记、市人大常委会主任"
    },
    {
        "id": 2,
        "name": "陈宇航",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠州市委副书记、市长",
        "current_org": "惠州市人民政府",
        "source": "惠州市政府官网领导之窗 (confirmed) — 市委副书记、市长"
    },
    {
        "id": 3,
        "name": "赖建华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠州市委常委",
        "current_org": "中共惠州市委员会",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    {
        "id": 4,
        "name": "黄维玉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠州市委常委",
        "current_org": "中共惠州市委员会",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    {
        "id": 5,
        "name": "黄细花",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠州市委常委",
        "current_org": "中共惠州市委员会",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    {
        "id": 6,
        "name": "黎明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠州市委常委",
        "current_org": "中共惠州市委员会",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    {
        "id": 7,
        "name": "王滨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠州市委常委、副市长",
        "current_org": "惠州市人民政府",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    {
        "id": 8,
        "name": "张军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠州市委常委",
        "current_org": "中共惠州市委员会",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    {
        "id": 9,
        "name": "黎炳盛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠州市委常委",
        "current_org": "中共惠州市委员会",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    {
        "id": 10,
        "name": "黄伟东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠州市委常委、市纪委书记、市监委主任",
        "current_org": "中共惠州市纪律检查委员会",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    # ════════════════════════════════════════════
    # 市委秘书长
    # ════════════════════════════════════════════
    {
        "id": 11,
        "name": "冯起忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠州市委秘书长、市人大常委会副主任",
        "current_org": "中共惠州市委员会",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    # ════════════════════════════════════════════
    # 市政府其他副市长
    # ════════════════════════════════════════════
    {
        "id": 12,
        "name": "曲维震",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "惠州市副市长",
        "current_org": "惠州市人民政府",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    {
        "id": 13,
        "name": "段致辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠州市副市长",
        "current_org": "惠州市人民政府",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    {
        "id": 14,
        "name": "赖志光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠州市副市长",
        "current_org": "惠州市人民政府",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    {
        "id": 15,
        "name": "曹洪彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠州市副市长",
        "current_org": "惠州市人民政府",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    {
        "id": 16,
        "name": "陈惠强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠州市政府秘书长",
        "current_org": "惠州市人民政府",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    # ════════════════════════════════════════════
    # 市人大常委会
    # ════════════════════════════════════════════
    {
        "id": 17,
        "name": "张伟荣",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "惠州市人大常委会副主任",
        "current_org": "惠州市人民代表大会常务委员会",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    {
        "id": 18,
        "name": "邱伟泽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "惠州市人大常委会副主任",
        "current_org": "惠州市人民代表大会常务委员会",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    {
        "id": 19,
        "name": "朱文转",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "惠州市人大常委会副主任",
        "current_org": "惠州市人民代表大会常务委员会",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    {
        "id": 20,
        "name": "李箫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "惠州市人大常委会副主任兼秘书长",
        "current_org": "惠州市人民代表大会常务委员会",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    # ════════════════════════════════════════════
    # 市政协
    # ════════════════════════════════════════════
    {
        "id": 21,
        "name": "温勇瑜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠州市政协主席",
        "current_org": "中国人民政治协商会议惠州市委员会",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    {
        "id": 22,
        "name": "黄晓霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "惠州市政协副主席",
        "current_org": "中国人民政治协商会议惠州市委员会",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    {
        "id": 23,
        "name": "王正印",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "惠州市政协副主席",
        "current_org": "中国人民政治协商会议惠州市委员会",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    {
        "id": 24,
        "name": "刘恒蓉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "惠州市政协副主席",
        "current_org": "中国人民政治协商会议惠州市委员会",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    {
        "id": 25,
        "name": "吴欣",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "惠州市政协副主席",
        "current_org": "中国人民政治协商会议惠州市委员会",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    {
        "id": 26,
        "name": "林利育",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "惠州市政协副主席",
        "current_org": "中国人民政治协商会议惠州市委员会",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    {
        "id": 27,
        "name": "胡雪平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "惠州市政协副主席",
        "current_org": "中国人民政治协商会议惠州市委员会",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    {
        "id": 28,
        "name": "刘洪添",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "惠州市政协副主席",
        "current_org": "中国人民政治协商会议惠州市委员会",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    {
        "id": 29,
        "name": "侯文慧",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "惠州市政协副主席",
        "current_org": "中国人民政治协商会议惠州市委员会",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    {
        "id": 30,
        "name": "朱向阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "惠州市政协秘书长",
        "current_org": "中国人民政治协商会议惠州市委员会",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    # ════════════════════════════════════════════
    # 市纪委
    # ════════════════════════════════════════════
    {
        "id": 31,
        "name": "徐焕亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠州市纪委副书记",
        "current_org": "中共惠州市纪律检查委员会",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    {
        "id": 32,
        "name": "陈红雨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠州市纪委副书记",
        "current_org": "中共惠州市纪律检查委员会",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    {
        "id": 33,
        "name": "姚毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠州市纪委副书记",
        "current_org": "中共惠州市纪律检查委员会",
        "source": "惠州市政府官网领导之窗 (confirmed)"
    },
    # ════════════════════════════════════════════
    # 前任领导（关键人物）
    # ════════════════════════════════════════════
    {
        "id": 34,
        "name": "温金荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "前任惠州市市长",
        "current_org": "惠州市人民政府",
        "source": "公开资料 — 前任惠州市长，刘吉接任市委书记后由温金荣接任市长"
    },
    {
        "id": 35,
        "name": "麦教猛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "前任惠州市市长（已调任广东省市场监管局）",
        "current_org": "广东省市场监督管理局",
        "source": "现有仓库数据 (confirmed) — 引自赤坎区调研数据：麦教猛曾任惠州市长、广东省市场监管局局长"
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共惠州市委员会", "type": "党委", "level": "地级", "parent": "中共广东省委员会", "location": "广东省惠州市"},
    {"id": 2, "name": "惠州市人民政府", "type": "政府", "level": "地级", "parent": "广东省人民政府", "location": "广东省惠州市"},
    {"id": 3, "name": "惠州市人民代表大会常务委员会", "type": "人大", "level": "地级", "parent": "广东省人民代表大会常务委员会", "location": "广东省惠州市"},
    {"id": 4, "name": "中国人民政治协商会议惠州市委员会", "type": "政协", "level": "地级", "parent": "中国人民政治协商会议广东省委员会", "location": "广东省惠州市"},
    {"id": 5, "name": "中共惠州市纪律检查委员会", "type": "纪委", "level": "地级", "parent": "中共广东省纪律检查委员会", "location": "广东省惠州市"},
    {"id": 6, "name": "惠州市监察委员会", "type": "监察", "level": "地级", "parent": "广东省监察委员会", "location": "广东省惠州市"},
    {"id": 7, "name": "广东省市场监督管理局", "type": "政府", "level": "省级", "parent": "广东省人民政府", "location": "广东省广州市"},
]

# 3. Positions
positions = [
    # 刘吉 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "中共惠州市委书记", "start": "待查", "end": "present", "rank": "正厅级", "note": "兼任市人大常委会主任"},
    {"person_id": 1, "org_id": 3, "title": "惠州市人大常委会主任", "start": "待查", "end": "present", "rank": "正厅级", "note": ""},

    # 陈宇航 — 市长
    {"person_id": 2, "org_id": 2, "title": "惠州市市长", "start": "待查", "end": "present", "rank": "正厅级", "note": "市委副书记"},
    {"person_id": 2, "org_id": 1, "title": "惠州市委副书记", "start": "待查", "end": "present", "rank": "正厅级", "note": ""},

    # 赖建华 — 市委常委
    {"person_id": 3, "org_id": 1, "title": "惠州市委常委", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},

    # 黄维玉 — 市委常委
    {"person_id": 4, "org_id": 1, "title": "惠州市委常委", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},

    # 黄细花 — 市委常委
    {"person_id": 5, "org_id": 1, "title": "惠州市委常委", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},

    # 黎明 — 市委常委
    {"person_id": 6, "org_id": 1, "title": "惠州市委常委", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},

    # 王滨 — 市委常委、副市长
    {"person_id": 7, "org_id": 1, "title": "惠州市委常委", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "惠州市副市长", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},

    # 张军 — 市委常委
    {"person_id": 8, "org_id": 1, "title": "惠州市委常委", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},

    # 黎炳盛 — 市委常委
    {"person_id": 9, "org_id": 1, "title": "惠州市委常委", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},

    # 黄伟东 — 市委常委、市纪委书记
    {"person_id": 10, "org_id": 1, "title": "惠州市委常委", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 5, "title": "惠州市纪委书记", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 6, "title": "惠州市监委主任", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},

    # 冯起忠 — 市委秘书长、市人大常委会副主任
    {"person_id": 11, "org_id": 1, "title": "惠州市委秘书长", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 11, "org_id": 3, "title": "惠州市人大常委会副主任", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},

    # 曲维震 — 副市长
    {"person_id": 12, "org_id": 2, "title": "惠州市副市长", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},

    # 段致辉 — 副市长
    {"person_id": 13, "org_id": 2, "title": "惠州市副市长", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},

    # 赖志光 — 副市长
    {"person_id": 14, "org_id": 2, "title": "惠州市副市长", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},

    # 曹洪彬 — 副市长
    {"person_id": 15, "org_id": 2, "title": "惠州市副市长", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},

    # 陈惠强 — 市政府秘书长
    {"person_id": 16, "org_id": 2, "title": "惠州市政府秘书长", "start": "待查", "end": "present", "rank": "正处级", "note": ""},

    # 市人大常委会
    {"person_id": 17, "org_id": 3, "title": "惠州市人大常委会副主任", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 18, "org_id": 3, "title": "惠州市人大常委会副主任", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 19, "org_id": 3, "title": "惠州市人大常委会副主任", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 20, "org_id": 3, "title": "惠州市人大常委会副主任兼秘书长", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},

    # 市政协
    {"person_id": 21, "org_id": 4, "title": "惠州市政协主席", "start": "待查", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 22, "org_id": 4, "title": "惠州市政协副主席", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 23, "org_id": 4, "title": "惠州市政协副主席", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 24, "org_id": 4, "title": "惠州市政协副主席", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 25, "org_id": 4, "title": "惠州市政协副主席", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 26, "org_id": 4, "title": "惠州市政协副主席", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 27, "org_id": 4, "title": "惠州市政协副主席", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 28, "org_id": 4, "title": "惠州市政协副主席", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 29, "org_id": 4, "title": "惠州市政协副主席", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 30, "org_id": 4, "title": "惠州市政协秘书长", "start": "待查", "end": "present", "rank": "正处级", "note": ""},

    # 市纪委
    {"person_id": 31, "org_id": 5, "title": "惠州市纪委副书记", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 32, "org_id": 5, "title": "惠州市纪委副书记", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 33, "org_id": 5, "title": "惠州市纪委副书记", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},

    # 前任领导
    {"person_id": 34, "org_id": 2, "title": "惠州市市长（前任）", "start": "待查", "end": "待查", "rank": "正厅级", "note": "前任市长，刘吉升任书记后接任市长"},
    {"person_id": 35, "org_id": 2, "title": "惠州市市长（前任）", "start": "待查", "end": "待查", "rank": "正厅级", "note": ""},
    {"person_id": 35, "org_id": 7, "title": "广东省市场监督管理局局长", "start": "待查", "end": "待查", "rank": "正厅级", "note": ""},
]

# 4. Relationships (key working relationships)
relationships = [
    # 刘吉 — 陈宇航（书记—市长搭档）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书记与市长—党政一把手搭档", "overlap_org": "中共惠州市委员会/惠州市人民政府", "overlap_period": "现任"},
    # 刘吉 — 黄伟东（书记—纪委书记监督关系）
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "市委书记与市纪委书记—同级党委与纪委监督关系", "overlap_org": "中共惠州市委员会", "overlap_period": "现任"},
    # 陈宇航 — 王滨（市长—副市长）
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "市长与副市长—政府领导班子", "overlap_org": "惠州市人民政府", "overlap_period": "现任"},
    # 陈宇航 — 曲维震（市长—副市长）
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "市长与副市长—政府领导班子", "overlap_org": "惠州市人民政府", "overlap_period": "现任"},
    # 陈宇航 — 段致辉（市长—副市长）
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "市长与副市长—政府领导班子", "overlap_org": "惠州市人民政府", "overlap_period": "现任"},
    # 陈宇航 — 赖志光（市长—副市长）
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "市长与副市长—政府领导班子", "overlap_org": "惠州市人民政府", "overlap_period": "现任"},
    # 陈宇航 — 曹洪彬（市长—副市长）
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "市长与副市长—政府领导班子", "overlap_org": "惠州市人民政府", "overlap_period": "现任"},
    # 刘吉 — 冯起忠（书记—秘书长）
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "市委书记与市委秘书长—直接工作关系", "overlap_org": "中共惠州市委员会", "overlap_period": "现任"},
    # 陈宇航 — 陈惠强（市长—秘书长）
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "市长与市政府秘书长—直接工作关系", "overlap_org": "惠州市人民政府", "overlap_period": "现任"},
    # 刘吉 — 温金荣（书记—前任市长，交接关系）
    {"person_a": 1, "person_b": 34, "type": "predecessor_successor", "context": "市委书记与前市长—刘吉升任书记后温金荣接任市长", "overlap_org": "惠州市人民政府", "overlap_period": "待查"},
    # 温金荣 — 麦教猛（市长前后任）
    {"person_a": 34, "person_b": 35, "type": "predecessor_successor", "context": "两任惠州市长前后任关系", "overlap_org": "惠州市人民政府", "overlap_period": "待查"},
]


# ════════════════════════════════════════════
# Build
# ════════════════════════════════════════════
def main():
    print(f"Building {SLUG} network...")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
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

    # Verify
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    try:
        for table in ["persons", "organizations", "positions", "relationships"]:
            count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"  {table}: {count} rows")
    finally:
        conn.close()

    print(f"\nDatabase: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Done.")


if __name__ == "__main__":
    main()
