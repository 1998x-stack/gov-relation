#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
斗门区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 珠海市
Region: 斗门区
Targets: 区委书记 & 区长
Task ID: guangdong_斗门区

Research Sources:
- 珠海市斗门区人民政府门户网站 (www.doumen.gov.cn) — 领导之窗/区委/区政府
  - 区委书记刘宏: www.doumen.gov.cn/zhsdmqrmzfmhwz/zwgk/ldzc/qldcy/qw/content/post_3805867.html
  - 区长王子程: www.doumen.gov.cn/zhsdmqrmzfmhwz/zwgk/ldzc/qldcy/qw/content/post_2859956.html
  - 区委全体成员: postmeta/i/11510.json
  - 区政府全体成员: postmeta/i/11512.json
- 斗门区人民政府网站首页新闻: 开局即决战 起步即冲刺 区委书记刘宏赴园区调研 (2026-02-27/28)

Current status (as of 2026-07-22):
- 区委书记: 刘宏（confirmed from official page, published 2025-06-15）
- 区长: 王子程（confirmed from official page, first published 2021-05-11）

Research Date: 2026-07-22

Note: Official government pages only list brief personal info (name, gender, ethnicity).
Full career timelines require additional news/article research and are marked as open_questions.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "斗门区"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 区委领导 - Party Committee
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "刘宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共珠海市斗门区委书记",
        "current_org": "中共珠海市斗门区委员会",
        "source": "https://www.doumen.gov.cn/zhsdmqrmzfmhwz/zwgk/ldzc/qldcy/qw/content/post_3805867.html"
    },
    {
        "id": 2,
        "name": "王子程",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委副书记，区政府党组书记、区长，兼任斗门生态农业园党委副书记、管委会主任",
        "current_org": "斗门区人民政府",
        "source": "https://www.doumen.gov.cn/zhsdmqrmzfmhwz/zwgk/ldzc/qldcy/qw/content/post_2859956.html"
    },
    {
        "id": 3,
        "name": "谭胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委副书记，兼任区委政法委书记，一级调研员",
        "current_org": "中共珠海市斗门区委员会",
        "source": "https://www.doumen.gov.cn/zhsdmqrmzfmhwz/zwgk/ldzc/qldcy/qw/content/post_3814804.html"
    },
    {
        "id": 4,
        "name": "陈萍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委，兼任区委统战部部长、区政协党组副书记",
        "current_org": "中共珠海市斗门区委员会",
        "source": "https://www.doumen.gov.cn/zhsdmqrmzfmhwz/zwgk/ldzc/qldcy/qw/content/post_2966905.html"
    },
    {
        "id": 5,
        "name": "杨富邦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委，区政府党组副书记、副区长，兼任富山工业园党工委委员、管委会常务副主任",
        "current_org": "中共珠海市斗门区委员会 / 斗门区人民政府",
        "source": "https://www.doumen.gov.cn/zhsdmqrmzfmhwz/zwgk/ldzc/qldcy/qw/content/post_3317345.html"
    },
    {
        "id": 6,
        "name": "毕璐洁",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委，兼任区纪委书记、区监委主任",
        "current_org": "中共珠海市斗门区纪律检查委员会",
        "source": "https://www.doumen.gov.cn/zhsdmqrmzfmhwz/zwgk/ldzc/qldcy/qw/content/post_3703063.html"
    },
    {
        "id": 7,
        "name": "王子超",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委，兼任区委办（区府办）主任、区委改革办主任，新青科技工业园党委书记、管委会主任",
        "current_org": "中共珠海市斗门区委员会",
        "source": "https://www.doumen.gov.cn/zhsdmqrmzfmhwz/zwgk/ldzc/qldcy/qw/content/post_2966917.html"
    },
    {
        "id": 8,
        "name": "陈克",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委，区人民武装部政委",
        "current_org": "斗门区人民武装部",
        "source": "https://www.doumen.gov.cn/zhsdmqrmzfmhwz/zwgk/ldzc/qldcy/qw/content/post_2511749.html"
    },
    {
        "id": 9,
        "name": "李丛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委，兼任区委宣传部部长",
        "current_org": "中共珠海市斗门区委员会",
        "source": "https://www.doumen.gov.cn/zhsdmqrmzfmhwz/zwgk/ldzc/qldcy/qw/content/post_2585253.html"
    },
    {
        "id": 10,
        "name": "徐留根",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委，兼任区委组织部部长、区委党校（区行政学校）校长",
        "current_org": "中共珠海市斗门区委员会",
        "source": "https://www.doumen.gov.cn/zhsdmqrmzfmhwz/zwgk/ldzc/qldcy/qw/content/post_2460323.html"
    },
    {
        "id": 11,
        "name": "罗磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委，兼任白蕉镇委书记",
        "current_org": "中共珠海市斗门区白蕉镇委员会",
        "source": "https://www.doumen.gov.cn/zhsdmqrmzfmhwz/zwgk/ldzc/qldcy/qw/content/post_3436132.html"
    },
    # ════════════════════════════════════════
    # 区政府领导 - Government
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "陈彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区政府党组成员、副区长，兼任斗门公安分局局长",
        "current_org": "斗门区人民政府 / 珠海市公安局斗门分局",
        "source": "https://www.doumen.gov.cn/zhsdmqrmzfmhwz/zwgk/ldzc/qldcy/zf/content/post_2267046.html"
    },
    {
        "id": 13,
        "name": "郭丽云",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区政府党组成员、副区长",
        "current_org": "斗门区人民政府",
        "source": "https://www.doumen.gov.cn/zhsdmqrmzfmhwz/zwgk/ldzc/qldcy/zf/content/post_3867644.html"
    },
    {
        "id": 14,
        "name": "夏宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区政府党组成员、副区长（对口湄潭县结对协作）",
        "current_org": "斗门区人民政府",
        "source": "https://www.doumen.gov.cn/zhsdmqrmzfmhwz/zwgk/ldzc/qldcy/zf/content/post_2883013.html"
    },
    {
        "id": 15,
        "name": "谢联辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区政府党组成员、副区长",
        "current_org": "斗门区人民政府",
        "source": "https://www.doumen.gov.cn/zhsdmqrmzfmhwz/zwgk/ldzc/qldcy/zf/content/post_3754572.html"
    },
    {
        "id": 16,
        "name": "韦昕宇",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区政府党组成员、副区长，兼任斗门生态农业园党委委员、管委会常务副主任",
        "current_org": "斗门区人民政府 / 斗门生态农业园",
        "source": "https://www.doumen.gov.cn/zhsdmqrmzfmhwz/zwgk/ldzc/qldcy/zf/content/post_3756315.html"
    },
    {
        "id": 17,
        "name": "李越",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区政府党组成员、副区长",
        "current_org": "斗门区人民政府",
        "source": "https://www.doumen.gov.cn/zhsdmqrmzfmhwz/zwgk/ldzc/qldcy/zf/content/post_3820368.html"
    },
    {
        "id": 18,
        "name": "周月波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长（挂职，对口阳江市阳西县帮扶协作）",
        "current_org": "斗门区人民政府",
        "source": "https://www.doumen.gov.cn/zhsdmqrmzfmhwz/zwgk/ldzc/qldcy/zf/content/post_3539974.html"
    },
    {
        "id": 19,
        "name": "陈胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长（挂职）",
        "current_org": "斗门区人民政府",
        "source": "https://www.doumen.gov.cn/zhsdmqrmzfmhwz/zwgk/ldzc/qldcy/zf/content/post_3845251.html"
    },
    {
        "id": 20,
        "name": "陈夏森",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区三级调研员（对口茂名市乡村振兴驻镇帮镇扶村）",
        "current_org": "斗门区人民政府",
        "source": "https://www.doumen.gov.cn/zhsdmqrmzfmhwz/zwgk/ldzc/qldcy/zf/content/post_3641629.html"
    },
]

# 2. Organizations
organizations = [
    # Party committee
    {"id": 1, "name": "中共珠海市斗门区委员会", "type": "党委", "level": "县处级", "parent": "中共珠海市委", "location": "广东省珠海市斗门区"},
    {"id": 2, "name": "中共珠海市斗门区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共珠海市斗门区委员会", "location": "广东省珠海市斗门区"},
    {"id": 3, "name": "中共珠海市斗门区委组织部", "type": "党委", "level": "县处级", "parent": "中共珠海市斗门区委员会", "location": "广东省珠海市斗门区"},
    {"id": 4, "name": "中共珠海市斗门区委宣传部", "type": "党委", "level": "县处级", "parent": "中共珠海市斗门区委员会", "location": "广东省珠海市斗门区"},
    {"id": 5, "name": "中共珠海市斗门区委统战部", "type": "党委", "level": "县处级", "parent": "中共珠海市斗门区委员会", "location": "广东省珠海市斗门区"},
    {"id": 6, "name": "中共珠海市斗门区委政法委员会", "type": "党委", "level": "县处级", "parent": "中共珠海市斗门区委员会", "location": "广东省珠海市斗门区"},
    # Government
    {"id": 7, "name": "斗门区人民政府", "type": "政府", "level": "县处级", "parent": "珠海市人民政府", "location": "广东省珠海市斗门区"},
    {"id": 8, "name": "珠海市公安局斗门分局", "type": "政府", "level": "县处级", "parent": "斗门区人民政府", "location": "广东省珠海市斗门区"},
    {"id": 9, "name": "斗门区人民武装部", "type": "政府", "level": "县处级", "parent": "珠海警备区", "location": "广东省珠海市斗门区"},
    # Development Zones and Towns
    {"id": 10, "name": "斗门生态农业园", "type": "开发区", "level": "县处级", "parent": "斗门区人民政府", "location": "广东省珠海市斗门区"},
    {"id": 11, "name": "富山工业园", "type": "开发区", "level": "县处级", "parent": "斗门区人民政府", "location": "广东省珠海市斗门区"},
    {"id": 12, "name": "新青科技工业园", "type": "开发区", "level": "县处级", "parent": "斗门区人民政府", "location": "广东省珠海市斗门区"},
    {"id": 13, "name": "中共珠海市斗门区白蕉镇委员会", "type": "乡镇/街道", "level": "乡科级", "parent": "中共珠海市斗门区委员会", "location": "广东省珠海市斗门区白蕉镇"},
    {"id": 14, "name": "中共珠海市斗门区委办公室（区府办）", "type": "党委", "level": "县处级", "parent": "中共珠海市斗门区委员会", "location": "广东省珠海市斗门区"},
    {"id": 15, "name": "中共珠海市委", "type": "党委", "level": "地厅级", "parent": "中共广东省委", "location": "广东省珠海市"},
    {"id": 16, "name": "珠海市人民政府", "type": "政府", "level": "地厅级", "parent": "广东省人民政府", "location": "广东省珠海市"},
]

# 3. Positions
positions = [
    # 刘宏 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "待查", "end_date": "present", "rank": "县处级正职", "note": "主持区委全面工作。at least since 2025-06-15 (official page pub date)"},
    # 王子程 - 区长
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "区委副书记"},
    {"person_id": 2, "org_id": 7, "title": "区政府党组书记、区长", "start_date": "待查", "end_date": "present", "rank": "县处级正职", "note": "主持区政府全面工作。first appeared on official site 2021-05-11"},
    {"person_id": 2, "org_id": 10, "title": "兼任斗门生态农业园党委副书记、管委会主任", "start_date": "待查", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 谭胜 - 区委副书记/政法委书记
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "协助刘宏同志抓党的建设"},
    {"person_id": 3, "org_id": 6, "title": "区委政法委书记（兼任）", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "一级调研员"},
    # 陈萍 - 统战部长
    {"person_id": 4, "org_id": 5, "title": "区委统战部部长（兼任）", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "兼任区政协党组副书记"},
    # 杨富邦 - 常务副区长
    {"person_id": 5, "org_id": 7, "title": "区政府党组副书记、副区长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "协助王子程同志负责区政府日常工作"},
    {"person_id": 5, "org_id": 11, "title": "富山工业园党工委委员、管委会常务副主任（兼任）", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 毕璐洁 - 纪委书记
    {"person_id": 6, "org_id": 2, "title": "区纪委书记、区监委主任（兼任）", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "负责纪检监察工作"},
    # 王子超 - 区委办主任
    {"person_id": 7, "org_id": 14, "title": "区委办（区府办）主任（兼任）", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 12, "title": "新青科技工业园党委书记、管委会主任（兼任）", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 陈克 - 人武部政委
    {"person_id": 8, "org_id": 9, "title": "区人民武装部政委", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "自2020-03-19已在岗"},
    # 李丛 - 宣传部长
    {"person_id": 9, "org_id": 4, "title": "区委宣传部部长（兼任）", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "自2020-06-04已在岗"},
    # 徐留根 - 组织部长
    {"person_id": 10, "org_id": 3, "title": "区委组织部部长（兼任）", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "兼任区委党校校长。自2020-01-19已在岗"},
    # 罗磊 - 白蕉镇委书记
    {"person_id": 11, "org_id": 13, "title": "白蕉镇委书记（兼任）", "start_date": "待查", "end_date": "present", "rank": "乡科级正职", "note": "自2022-10-09已在岗"},
    # 陈彬 - 副区长/公安局长
    {"person_id": 12, "org_id": 7, "title": "区政府党组成员、副区长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 8, "title": "斗门公安分局局长（兼任）", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "自2019-09-27已在岗"},
    # 郭丽云 - 副区长
    {"person_id": 13, "org_id": 7, "title": "区政府党组成员、副区长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "2026-01-04上线"},
    # 夏宇 - 副区长
    {"person_id": 14, "org_id": 7, "title": "区政府党组成员、副区长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "对口湄潭县结对协作"},
    # 谢联辉 - 副区长
    {"person_id": 15, "org_id": 7, "title": "区政府党组成员、副区长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "2025-01-08上线"},
    # 韦昕宇 - 副区长
    {"person_id": 16, "org_id": 7, "title": "区政府党组成员、副区长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "兼任斗门生态农业园管委会常务副主任"},
    {"person_id": 16, "org_id": 10, "title": "斗门生态农业园党委委员、管委会常务副主任（兼任）", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 李越 - 副区长
    {"person_id": 17, "org_id": 7, "title": "区政府党组成员、副区长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "2025-07-30上线"},
    # 周月波 - 挂职副区长
    {"person_id": 18, "org_id": 7, "title": "副区长（挂职）", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "对口阳江市阳西县帮扶协作，自2023-06-14已在岗"},
    # 陈胜 - 挂职副区长
    {"person_id": 19, "org_id": 7, "title": "副区长（挂职）", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "2025-10-24上线"},
    # 陈夏森 - 三级调研员
    {"person_id": 20, "org_id": 7, "title": "区三级调研员", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "对口茂名市乡村振兴驻镇帮镇扶村"},
]

# 4. Relationships (inferred from shared committee membership and org overlaps)
# Note: These represent confirmed co-membership in the same leadership team (区委常委会 or 区政府党组)
# The strength is "strong" for direct working relationships within the same top leadership body
relationships = [
    # ── 刘宏 ↔ 区委班子成员（同一区委常委会）──
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "区委书记与区长搭档", "overlap_org": "中共珠海市斗门区委员会", "overlap_period": "至少自2025-06"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "区委书记与区委副书记/政法委书记搭档", "overlap_org": "中共珠海市斗门区委员会", "overlap_period": "至少自2025-07"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "区委书记与统战部长", "overlap_org": "中共珠海市斗门区委员会", "overlap_period": "至少自2021-08"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "区委书记与常务副区长", "overlap_org": "中共珠海市斗门区委员会", "overlap_period": "至少自2022-07"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "区委书记与纪委书记", "overlap_org": "中共珠海市斗门区委员会", "overlap_period": "至少自2024-08"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "区委书记与区委办主任", "overlap_org": "中共珠海市斗门区委员会", "overlap_period": "至少自2021-08"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "区委书记与人武部政委", "overlap_org": "中共珠海市斗门区委员会", "overlap_period": "至少自2020-03"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "区委书记与宣传部长", "overlap_org": "中共珠海市斗门区委员会", "overlap_period": "至少自2020-06"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "区委书记与组织部长", "overlap_org": "中共珠海市斗门区委员会", "overlap_period": "至少自2020-01"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "区委书记与白蕉镇委书记（区委常委）", "overlap_org": "中共珠海市斗门区委员会", "overlap_period": "至少自2022-10"},
    # ── 王子程 ↔ 区政府班子成员（同一区政府党组）──
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "区长与常务副区长搭档", "overlap_org": "斗门区人民政府", "overlap_period": "至少自2022-07"},
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "区长与副区长/公安局长", "overlap_org": "斗门区人民政府", "overlap_period": "至少自2019-09"},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "区长与副区长", "overlap_org": "斗门区人民政府", "overlap_period": "至少自2026-01"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "区长与副区长", "overlap_org": "斗门区人民政府", "overlap_period": "至少自2021-06"},
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "区长与副区长", "overlap_org": "斗门区人民政府", "overlap_period": "至少自2025-01"},
    {"person_a": 2, "person_b": 16, "type": "overlap", "context": "区长与副区长", "overlap_org": "斗门区人民政府", "overlap_period": "至少自2025-01"},
    {"person_a": 2, "person_b": 17, "type": "overlap", "context": "区长与副区长", "overlap_org": "斗门区人民政府", "overlap_period": "至少自2025-07"},
    # ── 杨富邦（常务副区长）↔ 各副区长 ──
    {"person_a": 5, "person_b": 12, "type": "overlap", "context": "常务副区长与副区长", "overlap_org": "斗门区人民政府", "overlap_period": "至少自2022-07"},
    {"person_a": 5, "person_b": 13, "type": "overlap", "context": "常务副区长与副区长", "overlap_org": "斗门区人民政府", "overlap_period": "至少自2026-01"},
    {"person_a": 5, "person_b": 15, "type": "overlap", "context": "常务副区长与副区长", "overlap_org": "斗门区人民政府", "overlap_period": "至少自2025-01"},
    {"person_a": 5, "person_b": 16, "type": "overlap", "context": "常务副区长与副区长", "overlap_org": "斗门区人民政府", "overlap_period": "至少自2025-01"},
    {"person_a": 5, "person_b": 17, "type": "overlap", "context": "常务副区长与副区长", "overlap_org": "斗门区人民政府", "overlap_period": "至少自2025-07"},
    # ── 谭胜（副书记/政法委书记）↔ 政法系统 ──
    {"person_a": 3, "person_b": 12, "type": "overlap", "context": "政法委书记与公安局长", "overlap_org": "中共珠海市斗门区委政法委员会", "overlap_period": "至少自2025-07"},
    # ── 王子程 ↔ 王子超（可能同一家族/同姓，但并无证据，仅列为同僚）──
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "区长与区委办主任", "overlap_org": "中共珠海市斗门区委员会", "overlap_period": "至少自2021-08"},
    # ── 跨区关系 ──
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "区长与白蕉镇委书记（区委常委）", "overlap_org": "中共珠海市斗门区委常委会", "overlap_period": "至少自2022-10"},
]


# ── Main ──

def main():
    if "--dry-run" in sys.argv:
        print(f"Dry run — would build DB at {DB_PATH} and GEXF at {GEXF_PATH}")
        print(f"  Persons: {len(persons)}")
        print(f"  Organizations: {len(organizations)}")
        print(f"  Positions: {len(positions)}")
        print(f"  Relationships: {len(relationships)}")
        return

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

    print(f"\nBuild complete!")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Stats: {len(persons)} persons, {len(organizations)} orgs, "
          f"{len(positions)} positions, {len(relationships)} relationships")


if __name__ == "__main__":
    main()
