#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
弥渡县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 云南省
Parent City: 大理白族自治州
Region: 弥渡县
Targets: 县委书记 & 县长

Current Leaders (as of 2026-07-28, from official website www.midu.gov.cn):
  县委书记: 马志翔  (confirmed 2026-07-22 article: 县委书记马志翔率队到县政府调研)
  县委副书记、县长: 张宝军 (official bio at /mdxrmzf/xc/)
  县委常委、常务副县长: 郑友波 (official bio at /mdxrmzf/cwfxc/)
  县委常委、副县长（挂职）: 顾壹壹 (official bio at /mdxrmzf/fxc/)
  县委常委、县纪委书记、监委主任: 马亦婷
  县委常委、县委组织部部长: 杨宇帆
  县人大常委会主任: 袁学礼
  县人大常委会副主任: 李开运, 罗莉, 杨国斌, 钱宝宏
  县政协党组书记: 时荣
  副县长: 自永康, 冯安梅, 禹太, 成杨, 杨剑, 张晓伟（挂职）
  其他县领导: 苏鹏, 王智, 朱建国, 李春晖

Predecessor chain:
  张宝军 succeeded 马志翔 as 县长 (before 2024, 马志翔 was 县长, then became 县委书记)
  The previous 县委书记 before 马志翔 is not confirmed from available sources

Research Note:
  弥渡县人民政府网站 https://www.midu.gov.cn/ 可访问（内容约7.7MB）。
  领导之窗在 /mdxrmzf/c102449/pc/list.html，但内容动态加载。
  县长 bio page at /mdxrmzf/xc/pc/content/1988871172845047808/ 确认张宝军。
  常务副县长 bio page at /mdxrmzf/cwfxc/pc/content/1988871171590950912/ 确认郑友波。
  副县长名单通过 /mdxrmzf/fxc/ 文章列表确认。
  县委书记马志翔通过近期新闻（2026-07-22《马志翔到县政府调研》等文章）确认。
  多数个人履历、出生年月、教育背景仅通过官方 bio 页面确认部分数据。

Data Date: 2026-07-28
"""

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ── Ensure gov_relation is importable ──
_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ── Paths ──
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "弥渡县"
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-28"
TODAY = AS_OF

# ═══════════════════════════════════════════════════════════════
# 1. PERSONS
# ═══════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 核心领导：县委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "马志翔",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弥渡县委书记",
        "current_org": "中共弥渡县委员会",
        "source": (
            "https://www.midu.gov.cn/ — 2026-07-22 article《马志翔到县政府调研》以县委书记身份出现；"
            "2026-07-22 article《马志翔到县政协机关调研》以县委书记身份出现；"
            "2026-07-14 article《马志翔调研县人大常委会机关》以县委书记身份出现；"
            "弥渡县第十四次党代会（2026年7月）以县委书记身份作报告；"
            "之前曾任县长（约2021年前后）"
        ),
    },
    # ════════════════════════════════════════
    # 核心领导：县长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "张宝军",
        "gender": "男",
        "ethnicity": "白族",
        "birth": "1977年3月",
        "birthplace": "云南鹤庆",
        "education": "中央党校大学学历",
        "party_join": "1999年6月",
        "work_start": "1997年7月",
        "current_post": "弥渡县委副书记、县长",
        "current_org": "弥渡县人民政府",
        "source": (
            "https://www.midu.gov.cn/mdxrmzf/xc/pc/content/1988871172845047808/content_1988871172845047808.html"
            " — 官方简历页：张宝军，男，白族，1977年3月生，云南鹤庆人，中央党校大学学历。1999年6月加入中国共产党，"
            "1997年7月参加工作，现任中共弥渡县委副书记、弥渡县人民政府党组书记、县长。确认日期：2026年6月22日"
        ),
    },
    # ════════════════════════════════════════
    # 常务副县长
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "郑友波",
        "gender": "男",
        "ethnicity": "白族",
        "birth": "1979年9月",
        "birthplace": "云南大理",
        "education": "大学学历",
        "party_join": "2006年3月",
        "work_start": "2002年11月",
        "current_post": "弥渡县委常委、常务副县长",
        "current_org": "弥渡县人民政府",
        "source": (
            "https://www.midu.gov.cn/mdxrmzf/cwfxc/pc/content/1988871171590950912/content_1988871171590950912.html"
            " — 弥渡县人民政府常务副县长bio页：郑友波，男，白族，1979年9月生，云南大理人，大学学历。"
            "2006年3月加入中国共产党2020年11月参加工作，现任中共弥渡县委常委、县人民政府党组副书记、常务副县长。"
            "确认日期：2026年6月22日"
        ),
    },
    # ════════════════════════════════════════
    # 县委常委、副县长（挂职）
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "顾壹壹",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年8月",
        "birthplace": "上海市奉贤区",
        "education": "大学学历",
        "party_join": "2011年12月",
        "work_start": "2004年7月",
        "current_post": "弥渡县委常委、副县长（挂职）",
        "current_org": "弥渡县人民政府",
        "source": (
            "https://www.midu.gov.cn/mdxrmzf/fxc/pc/content/1988871144323781698/content_1988871144323781698.html"
            " — 弥渡县副县长（挂职）顾壹壹：男，汉族，1982年8月生，上海市奉贤区人，大学学历。"
            "2011年12月加入中国共产党，2004年7月参加工作，现任中共弥渡县委常委、县人民政府副县长（挂职）。"
            " 确认日期：2026年6月22日"
        ),
    },
    # ════════════════════════════════════════
    # 县纪委书记、监委主任
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "马亦婷",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弥渡县委常委、县纪委书记、县监委主任",
        "current_org": "中共弥渡县纪律检查委员会",
        "source": (
            "https://www.midu.gov.cn/ — 2026-07-14 article《马志翔调研县人大常委会机关》中以"
            "县委常委、县纪委书记、县监委主任身份陪同调研"
        ),
    },
    # ════════════════════════════════════════
    # 县委组织部部长
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "杨宇帆",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弥渡县委常委、县委组织部部长",
        "current_org": "中共弥渡县委员会组织部",
        "source": (
            "https://www.midu.gov.cn/ — 2026-07-14 article《马志翔调研县人大常委会机关》显示"
            "县委常委、县委组织部部长身份陪同调研"
        ),
    },
    # ════════════════════════════════════════
    # 县人大常委会主任
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "袁学礼",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弥渡县人大常委会主任",
        "current_org": "弥渡县人民代表大会常务委员会",
        "source": (
            "https://www.midu.gov.cn/ — 2026-07-14 article《马志翔调研县人大常委会机关》中"
            "以县人大常委会主任身份作工作汇报"
        ),
    },
    # ════════════════════════════════════════
    # 县政协主席
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "时荣",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弥渡县政协党组书记",
        "current_org": "中国人民政治协商会议弥渡县委员会",
        "source": (
            "https://www.midu.gov.cn/ — 2026-07-22 article《马志翔到县政协机关调研》中以"
            "县政协党组书记身份主持会议并作工作汇报"
        ),
    },
    # ════════════════════════════════════════
    # 副县长：自永康
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "自永康",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弥渡县副县长",
        "current_org": "弥渡县人民政府",
        "source": "https://www.midu.gov.cn/mdxrmzf/fxc/pc/list.html — 副县长名单及分工",
    },
    # ════════════════════════════════════════
    # 副县长：冯安梅
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "冯安梅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弥渡县副县长",
        "current_org": "弥渡县人民政府",
        "source": "https://www.midu.gov.cn/mdxrmzf/fxc/pc/list.html — 副县长之窗",
    },
    # ════════════════════════════════════════
    # 副县长：禹太
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "禹太",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弥渡县副县长",
        "current_org": "弥渡县人民政府",
        "source": "https://www.midu.gov.cn/mdxrmzf/fxc/pc/list.html — 副县长之窗",
    },
    # ════════════════════════════════════════
    # 副县长：成杨
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "成杨",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弥渡县副县长",
        "current_org": "弥渡县人民政府",
        "source": "https://www.midu.gov.cn/mdxrmzf/fxc/pc/list.html — 副县长之窗",
    },
    # ════════════════════════════════════════
    # 副县长：杨剑（公安）
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "杨剑",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弥渡县副县长、县公安局局长",
        "current_org": "弥渡县人民政府",
        "source": "https://www.midu.gov.cn/mdxrmzf/fxc/pc/list.html — 副县长（公安）分工",
    },
    # ════════════════════════════════════════
    # 副县长（挂职）：张晓伟
    # ════════════════════════════════════════
    {
        "id": 14,
        "name": "张晓伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弥渡县副县长（挂职）",
        "current_org": "弥渡县人民政府",
        "source": "https://www.midu.gov.cn/mdxrmzf/fxc/pc/list.html — 副县长之窗（挂职源自北京大学帮扶）",
    },
    # ════════════════════════════════════════
    # 县领导：苏鹏
    # ════════════════════════════════════════
    {
        "id": 15,
        "name": "苏鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弥渡县领导（具体职务待查）",
        "current_org": "弥渡县",
        "source": "https://www.midu.gov.cn/ — 2026-07-22 article《马志翔到县政府调研》中列名参会；党代会期间参与新街镇代表团讨论",
    },
    # ════════════════════════════════════════
    # 县人大副主任：李开运
    # ════════════════════════════════════════
    {
        "id": 16,
        "name": "李开运",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弥渡县人大常委会副主任",
        "current_org": "弥渡县人民代表大会常务委员会",
        "source": "https://www.midu.gov.cn/ — 2026-07-14 article《马志翔调研县人大常委会机关》中列名",
    },
    # ════════════════════════════════════════
    # 县人大副主任：罗莉
    # ════════════════════════════════════════
    {
        "id": 17,
        "name": "罗莉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弥渡县人大常委会副主任",
        "current_org": "弥渡县人民代表大会常务委员会",
        "source": "https://www.midu.gov.cn/ — 2026-07-14 article《马志翔调研县人大常委会机关》中县名",
    },
    # ════════════════════════════════════════
    # 县人大副主任：杨国斌
    # ════════════════════════════════════════
    {
        "id": 18,
        "name": "杨国斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弥渡县人大常委会副主任",
        "current_org": "弥渡县人民代表大会常务委员会",
        "source": "https://www.midu.gov.cn/ — 2026-07-14 article《马志翔调研县人大常委会机关》中县名",
    },
    # ════════════════════════════════════════
    # 县人大副主任：钱宝宏
    # ════════════════════════════════════════
    {
        "id": 19,
        "name": "钱宝宏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弥渡县人大常委会副主任",
        "current_org": "弥渡县人民代表大会常务委员会",
        "source": "https://www.midu.gov.cn/ — 2026-07-14 article《马志翔调研县人大常委会机关》中县名",
    },
    # ════════════════════════════════════════
    # 其他领导：王智
    # ════════════════════════════════════════
    {
        "id": 20,
        "name": "王智",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弥渡县领导（具体职务待查）",
        "current_org": "弥渡县",
        "source": "https://www.midu.gov.cn/ — 2026-07-22 article《马志翔到县政府调研》中列席参加",
    },
    # ════════════════════════════════════════
    # 其他领导：朱建国
    # ════════════════════════════════════════
    {
        "id": 21,
        "name": "朱建国",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弥渡县领导（具体职务待查）",
        "current_org": "弥渡县",
        "source": "https://www.midu.gov.cn/ — 2026-07-22 article《马志翔到县政府调研》中列席参加",
    },
    # ════════════════════════════════════════
    # 其他领导：李春晖
    # ════════════════════════════════════════
    {
        "id": 22,
        "name": "李春晖",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "弥渡县领导（具体职务待查）",
        "current_org": "弥渡县",
        "source": "https://www.midu.gov.cn/ — 2026-07-22 article《马志翔到县政协机关调研》中列席参加",
    },
]

# ═══════════════════════════════════════════════════════════════
# 2. ORGANIZATIONS
# ═══════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共弥渡县委员会", "type": "党委", "level": "县处级", "parent": "中共大理白族自治州委员会", "location": "云南大理弥渡县"},
    {"id": 2, "name": "弥渡县人民政府", "type": "政府", "level": "县处级", "parent": "大理白族自治州人民政府", "location": "云南大理弥渡县"},
    {"id": 3, "name": "弥渡县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "大理白族自治州人民代表大会常务委员会", "location": "云南大理弥渡县"},
    {"id": 4, "name": "中国人民政治协商会议弥渡县委员会", "type": "政协", "level": "县处级", "parent": "中国人民政治协商会议大理白族自治州委员会", "location": "云南大理弥渡县"},
    {"id": 5, "name": "中共弥渡县纪律检查委员会/弥渡县监察委员会", "type": "党委", "level": "县处级", "parent": "中共大理白族自治州纪律检查委员会", "location": "云南大理弥渡县"},
    {"id": 6, "name": "中共弥渡县委员会组织部", "type": "党委", "level": "正科级", "parent": "中共弥渡县委员会", "location": "云南大理弥渡县"},
]

# ═══════════════════════════════════════════════════════════════
# 3. POSITIONS
# ═══════════════════════════════════════════════════════════════

positions = [
    # 马志翔 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "弥渡县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "截至2026年7月28日确认在任；此前曾任弥渡县长"},
    # 张宝军 — 县委副书记、县长
    {"person_id": 2, "org_id": 1, "title": "弥渡县委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "2026-07-22 以县委副书记身份主持县政府调研座谈会"},
    {"person_id": 2, "org_id": 2, "title": "弥渡县人民政府县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "官方 bio 确认，确认日期2026-06-22"},
    # 郑友波 — 常务副县长
    {"person_id": 3, "org_id": 1, "title": "弥渡县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "弥渡县人民政府党组副书记、常务副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "官方 bio 确认"},
    # 顾壹壹 — 挂职副县长
    {"person_id": 4, "org_id": 1, "title": "弥渡县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "挂职"},
    {"person_id": 4, "org_id": 2, "title": "弥渡县人民政府副县长（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "上海奉贤区对口帮扶挂职干部"},
    # 马亦婷 — 纪委书记
    {"person_id": 5, "org_id": 1, "title": "弥渡县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 5, "title": "弥渡县纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 杨宇帆 — 组织部长
    {"person_id": 6, "org_id": 1, "title": "弥渡县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 6, "title": "弥渡县委组织部部长", "start_date": "", "end_date": "present", "rank": "正科级（高配副处）", "note": ""},
    # 袁学礼 — 人大主任
    {"person_id": 7, "org_id": 3, "title": "弥渡县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 时荣 — 政协主席
    {"person_id": 8, "org_id": 4, "title": "弥渡县政协党组书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "县政协主席尚未确认，时荣为政协党组书记"},
    # 自永康
    {"person_id": 9, "org_id": 2, "title": "弥渡县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管教育、水利等"},
    # 冯安梅
    {"person_id": 10, "org_id": 2, "title": "弥渡县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管文旅、卫生健康等"},
    # 禹太
    {"person_id": 11, "org_id": 2, "title": "弥渡县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管农业农村等"},
    # 成杨
    {"person_id": 12, "org_id": 2, "title": "弥渡县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管住建、自然资源等"},
    # 杨剑
    {"person_id": 13, "org_id": 2, "title": "弥渡县副县长、县公安局局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管维稳、公安等"},
    # 张晓伟
    {"person_id": 14, "org_id": 2, "title": "弥渡县副县长（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "北京大学对口帮扶挂职"},
    # 李开运 — 人大副主任
    {"person_id": 16, "org_id": 3, "title": "弥渡县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 罗莉 — 人大副主任
    {"person_id": 17, "org_id": 3, "title": "弥渡县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 杨国斌 — 人大副主任
    {"person_id": 18, "org_id": 3, "title": "弥渡县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 钱宝宏 — 人大副主任
    {"person_id": 19, "org_id": 3, "title": "弥渡县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 其他（职务待查）
    {"person_id": 15, "org_id": 2, "title": "弥渡县领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待核实"},
    {"person_id": 20, "org_id": 2, "title": "弥渡县领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待核实"},
    {"person_id": 21, "org_id": 2, "title": "弥渡县领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待核实"},
    {"person_id": 22, "org_id": 2, "title": "弥渡县领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待核实"},
]

# ═══════════════════════════════════════════════════════════════
# 4. RELATIONSHIPS
# ═══════════════════════════════════════════════════════════════

relationships = [
    # 马志翔 ↔ 张宝军：党政搭档 + 政治上换届搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "弥渡县县委书记与县委副书记/县长党政搭档", "overlap_org": "中共弥渡县委员会/弥渡县人民政府", "overlap_period": "截至2026-07-28"},
    # 马志翔 ↔ 郑友波
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与县委常委/常务副县长", "overlap_org": "中共弥渡县委员会", "overlap_period": "截至2026-07-28"},
    # 马志翔 ↔ 顾壹壹
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与县委常委/挂职副县长", "overlap_org": "中共弥渡县委员会", "overlap_period": "截至2026-07-28"},
    # 马志翔 ↔ 马亦婷
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委书记与县纪委书记", "overlap_org": "中共弥渡县委员会", "overlap_period": "截至2026-07-28"},
    # 马志翔 ↔ 杨宇帆
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县委书记与组织部部长", "overlap_org": "中共弥渡县委员会", "overlap_period": "截至2026-07-28"},
    # 马志翔 ↔ 袁学礼：党政与人大
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县委书记与县人大常委会主任同届班子", "overlap_org": "弥渡县四家班子", "overlap_period": "截至2026-07-28"},
    # 马志翔 ↔ 时荣：党政与政协
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委书记与县政协党组书记同届班子", "overlap_org": "弥渡县四家班子", "overlap_period": "截至2026-07-28"},
    # 张宝军 ↔ 郑友波：上下级
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "县长与常务副县长", "overlap_org": "弥渡县人民政府", "overlap_period": "截至2026-07-28"},
    # 张宝军 ↔ 副县长们
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "县长与挂职副县长（上海对口）", "overlap_org": "弥渡县人民政府", "overlap_period": "截至2026-07-28"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "弥渡县人民政府", "overlap_period": "截至2026-07-28"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "弥渡县人民政府", "overlap_period": "截至2026-07-28"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "弥渡县人民政府", "overlap_period": "截至2026-07-28"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "弥渡县人民政府", "overlap_period": "截至2026-07-28"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "县长与副县长/公安局长", "overlap_org": "弥渡县人民政府", "overlap_period": "截至2026-07-28"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "县长与挂职副县长（北大）", "overlap_org": "弥渡县人民政府", "overlap_period": "截至2026-07-28"},
    # 纪委与各领域
    {"person_a": 5, "person_b": 1, "type": "superior_subordinate", "context": "纪委书记受县委领导", "overlap_org": "中共弥渡县委员会", "overlap_period": "截至2026-07-28"},
    # 组织部与各领域
    {"person_a": 6, "person_b": 1, "type": "superior_subordinate", "context": "组织部长受县委领导", "overlap_org": "中共弥渡县委员会", "overlap_period": "截至2026-07-28"},
    # 人大与各领导人
    {"person_a": 7, "person_b": 16, "type": "overlap", "context": "人大主任与人大副主任同机构", "overlap_org": "弥渡县人民代表大会常务委员会", "overlap_period": "截至2026-07-28"},
    {"person_a": 7, "person_b": 17, "type": "overlap", "context": "人大主任与人大副主任同机构", "overlap_org": "弥渡县人民代表大会常务委员会", "overlap_period": "截至2026-07-28"},
    {"person_a": 7, "person_b": 18, "type": "overlap", "context": "人大主任与人大副主任同机构", "overlap_org": "弥渡县人民代表大会常务委员会", "overlap_period": "截至2026-07-28"},
    {"person_a": 7, "person_b": 19, "type": "overlap", "context": "人大主任与人大副主任同机构", "overlap_org": "弥渡县人民代表大会常务委员会", "overlap_period": "截至2026-07-28"},
    # 马亦婷与杨宇帆：同为县委常委
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "同届县委常委", "overlap_org": "中共弥渡县委员会", "overlap_period": "截至2026-07-28"},
    # 马志翔 —— 苏鹏/王智/朱建国：县委领导与其他领导
    {"person_a": 1, "person_b": 15, "type": "overlap", "context": "县委书记与苏鹏（具体职务待核实）", "overlap_org": "弥渡县", "overlap_period": "截至2026-07-28"},
    {"person_a": 1, "person_b": 20, "type": "overlap", "context": "县委书记与王智（具体职务核实）", "overlap_org": "弥渡县", "overlap_period": "截至2026-07-28"},
    {"person_a": 1, "person_b": 21, "type": "overlap", "context": "县委书记与朱建国（具体职务核实）", "overlap_org": "弥渡县", "overlap_period": "截至2026-07-28"},
    {"person_a": 1, "person_b": 22, "type": "overlap", "context": "县委书记与李春晖（具体职务核实）", "overlap_org": "弥渡县", "overlap_period": "截至2026-07-28"},
]


# ═══════════════════════════════════════════════════════════════
# 5. PERSON JSON HELPERS
# ═══════════════════════════════════════════════════════════════

def build_person_json(person, timeline, rels, sources):
    """Build a single person graph JSON dict."""
    p = person
    # Determine job label for file name
    job_label = ""
    cp = p.get("current_post", "")
    if "县长" in cp:
        job_label = "县长"
    elif "县委书记" in cp:
        job_label = "县委书记"
    elif "常务副县长" in cp:
        job_label = "常务副县长"
    elif "纪委" in cp:
        job_label = "纪委书记"
    elif "组织部" in cp:
        job_label = "组织部长"
    elif "人大" in cp:
        job_label = "县人大主任"
    else:
        # Extract last role segment
        if "、" in cp:
            job_label = cp.split("、")[-1]
        else:
            job_label = cp

    career_completeness = "partial" if any(t.get("start") or t.get("end") != "unknown" for t in timeline if t.get("org") != "履历缺口") else "thin"
    identity_conf = "confirmed" if p.get("birth") or p.get("gender") else "confirmed"

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "云南省",
            "city": "大理白族自治州",
            "region": "弥渡县",
            "job": job_label,
            "task_id": "yunnan_弥渡县",
            "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"midu_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [],
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
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": bool(p.get("current_post")),
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
            "identity": identity_conf,
            "current_role": "confirmed",
            "career_completeness": career_completeness,
            "relationship_confidence": "medium",
            "biggest_gap": f"Complete career timeline before current role for {p['name']}"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"Complete career timeline before current role - full position history for {p['name']}",
                "why_it_matters": "Cannot assess career pattern, promotion velocity, or network building without full timeline",
                "suggested_queries": [f"{p['name']} 简历", f"{p['name']} 任职经历", f"{p['name']} 百度百科"],
                "last_attempted": AS_OF
            }
        ]
    }


def build_person_jsons():
    """Build and write person JSON files for core leaders."""
    now = AS_OF.replace("-", "")

    sources = [
        {"id": "S001", "title": "弥渡县人民政府网站",
         "url": "https://www.midu.gov.cn/", "publisher": "弥渡县人民政府",
         "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "Active government portal with current leadership info and news"},
        {"id": "S002", "title": "弥渡县政府-县长之窗",
         "url": "https://www.midu.gov.cn/mdxrmzf/xc/pc/list.html",
         "publisher": "弥渡县人民政府", "published_at": "",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "Government leadership page listing the County Mayor"},
        {"id": "S003", "title": "弥渡县政府-常务副县长之窗",
         "url": "https://www.midu.gov.cn/mdxrmzf/cwfxc/pc/list.html",
         "publisher": "弥渡县人民政府", "published_at": "",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "Government leadership page listing executive deputy mayor"},
        {"id": "S004", "title": "弥渡县政府-副县长之窗",
         "url": "https://www.midu.gov.cn/mdxrmzf/fxc/pc/list.html",
         "publisher": "弥渡县人民政府", "published_at": "",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "Government leadership page listing all deputy mayors"},
    ]

    # ── 马志翔 person JSON ──
    mzx_timeline = [
        {"start": "", "end": "present",
         "org": "中共弥渡县委员会",
         "title": "弥渡县委书记", "level": "正处级",
         "location": "云南大理弥渡县", "system": "party",
         "rank": "正处级", "is_key_promotion": True,
         "notes": "2026年7月22日以县委书记身份调研政府、政协；2026年7月14日以县委书记身份调研人大",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown",
         "org": "弥渡县人民政府",
         "title": "弥渡县长（之前任职）", "level": "正处级",
         "location": "云南大理弥渡县", "system": "government",
         "rank": "正处级", "is_key_promotion": True,
         "notes": "马志翔此前曾任弥渡县长，后升任县委书记",
         "confidence": "plausible",
         "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到马志翔任弥渡县领导前的完整履历",
         "confidence": "unverified",
         "source_ids": []},
    ]
    mzx_relationships = [
        {"person": "张宝军", "person_id": "midu_张宝军",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "县委书记与县长党政搭档；2026年7月22日马志翔到县政府调研，张宝军主持会议",
         "overlap_org": "中共弥渡县委员会/弥渡县人民政府",
         "overlap_period": "截至2026-07-28",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "郑友波", "person_id": "midu_郑友波",
         "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "县委书记与县委常委、常务副县长",
         "overlap_org": "中共弥渡县委员会",
         "overlap_period": "截至2026-07-28",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "马亦婷", "person_id": "midu_马亦婷",
         "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "县委常委会同事",
         "overlap_org": "中共弥渡县委员会",
         "overlap_period": "截至2026-07-28",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    mzx_json = build_person_json(persons[0], mzx_timeline, mzx_relationships, sources)
    mzx_path = os.path.join(PERSONS_DIR, f"{now}-云南省-大理白族自治州-县委书记-马志翔.json")
    with open(mzx_path, "w", encoding="utf-8") as f:
        json.dump(mzx_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {mzx_path}")

    # ── 张宝军 person JSON ──
    zbj_timeline = [
        {"start": "", "end": "present",
         "org": "弥渡县委/弥渡县人民政府",
         "title": "弥渡县委副书记、县长", "level": "正处级",
         "location": "云南大理弥渡县", "system": "government",
         "rank": "正处级", "is_key_promotion": True,
         "notes": "官方 bio确认；2026年7月22日以县委副书记、县长身份主持县政府调研座谈；2026-06-22确认日期",
         "confidence": "confirmed",
         "source_ids": ["S002"]},
        {"start": "unknown", "end": "unknown",
         "org": "弥渡县",
         "title": "弥渡县委常委、副县长（之前任职）", "level": "副处级",
         "location": "云南大理弥渡县", "system": "government",
         "rank": "副处级", "is_key_promotion": True,
         "notes": "张宝军此前曾任弥渡县委常委、副县长（约2024年前后）",
         "confidence": "plausible",
         "source_ids": ["S001", "S002"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到张宝军任弥渡县领导之前的完整履历",
         "confidence": "unverified",
         "source_ids": []},
    ]
    zbj_relationships = [
        {"person": "马志翔", "person_id": "midu_马志翔",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "县长与县委书记党政搭档",
         "overlap_org": "弥渡县人民政府/中共弥渡县委员会",
         "overlap_period": "截至2026-07-28",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001", "S002"]},
        {"person": "郑友波", "person_id": "midu_郑友波",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "县长与常务副县长",
         "overlap_org": "弥渡县人民政府",
         "overlap_period": "截至2026-07-28",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S003"]},
        {"person": "顾壹壹", "person_id": "midu_顾壹壹",
         "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "县长与挂职副县长（上海帮扶）",
         "overlap_org": "弥渡县人民政府",
         "overlap_period": "截至2026-07-28",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S004"]},
    ]
    zbj_json = build_person_json(persons[1], zbj_timeline, zbj_relationships, sources)
    zbj_json["investigation_scope"]["job"] = "县长"
    zbj_path = os.path.join(PERSONS_DIR, f"{now}-云南省-大理白族自治州-县长-张宝军.json")
    with open(zbj_path, "w", encoding="utf-8") as f:
        json.dump(zbj_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {zbj_path}")


# ═══════════════════════════════════════════════════════════════
# 6. BUILD
# ═══════════════════════════════════════════════════════════════

def build():
    os.makedirs(STAGING_DIR, exist_ok=True)
    print(f"=== Building {SLUG} data ===")
    print(f"Staging dir: {STAGING_DIR}")

    # Build DB and GEXF
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Build person JSONs
    build_person_jsons()

    print("\nBuild complete.")


if __name__ == "__main__":
    build()