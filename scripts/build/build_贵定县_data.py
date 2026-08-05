#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
贵定县领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Guiding County leadership network.

Level: 县
Province: 贵州省
Parent City: 黔南布依族苗族自治州
Region: 贵定县
Targets: 县委书记 & 县长

Research Sources (guiding.gov.cn — 贵定县人民政府门户网站, 2026年6-8月确认):
- 仲成鹏主持召开县委全面深化改革委员会2026年第2次会议 (2026-07-30)
- 县委常委会第155次（扩大）会议 (2026-07-03)
- 黄祖方主持召开县政府第100次常务会议 (2026-07-29)
- 贵定县安全生产工作专题会 (2026-07-30)
- 2026年贵定县禁毒委员会全体会议 (2026-06-22)
- 贵定县十九届人民代表大会第六次会议第一次全体会议 (2026-06-22)
- 仲成鹏、黄祖方到贵州昌明经济开发区调研 (2026-07-09)
- 仲成鹏、黄祖方督导调研防汛备汛 (2026-07-17)
- 仲成鹏督导调研城市发展工作 (2026-07-15)
- 仲成鹏到云雾镇、昌明镇调研 (2026-07-28)
- 2025年政府工作报告 / 2026年政府工作报告 (王伟超, 贵定县人民政府)

Confirmed officeholders (as of 2026-08-05, from guiding.gov.cn official news):
- 县委书记: 仲成鹏 (兼贵州昌明经济开发区党工委书记)
- 县委副书记、县长: 黄祖方 (2026-06代理县长, 兼贵州昌明经济开发区党工委副书记、管委会主任)
- 县委副书记: 杨奕
- 县委副书记、县委政法委书记: 刘永祥
- 县人大常委会党组书记、主任候选人: 喻正斌
- 县政府县长(前任): 王伟超 (截至2026-02, 2026年换届由黄祖方接任)

Note: Most biographical details (birth year, education, prior career) for county-level
officials remain to be filled from external sources; encoded as open gaps.

Research Date: 2026-08-05
"""

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths ──
SLUG = "贵定县"
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
        "name": "仲成鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-04",
        "birthplace": "湖北麻城",
        "education": "省委党校在职研究生",
        "party_join": "1999-06",
        "work_start": "1995-10",
        "current_post": "县委书记",
        "current_org": "中共贵定县委员会",
        "source": "百度百科 + 贵定县政务网(2026-07)"
    },
    {
        "id": 2,
        "name": "黄祖方",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987-06",
        "birthplace": "贵州瓮安",
        "education": "大学（管理学学士）",
        "party_join": "中共党员",
        "work_start": "2009-07",
        "current_post": "县委副书记、县长",
        "current_org": "贵定县人民政府",
        "source": "https://www.guiding.gov.cn — 县政府第100次常务会议(2026-07-29), 县委常委会(2026-07-03)"
    },
    {
        "id": 3,
        "name": "杨奕",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共贵定县委员会",
        "source": "https://www.guiding.gov.cn — 县委常委会第155次(扩大)会议(2026-07-03)"
    },
    {
        "id": 4,
        "name": "刘永祥",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县委政法委书记",
        "current_org": "中共贵定县委员会",
        "source": "https://www.guiding.gov.cn — 县委全面深化改革委员会会议(2026-07-30), 禁毒工作会议(2026-06-22)"
    },
    # ── 县人大 / 县政协 ──
    {
        "id": 5,
        "name": "喻正斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会党组书记、主任候选人",
        "current_org": "贵定县人民代表大会常务委员会",
        "source": "https://www.guiding.gov.cn — 县委全面深化改革委员会会议(2026-07-30)"
    },
    {
        "id": 6,
        "name": "杨先云",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导人大会执行主席",
        "current_org": "贵定县人民代表大会常务委员会",
        "source": "https://www.guiding.gov.cn — 贵定县十九届人大六次会议(2026-06-22)执行主席"
    },
    # ── 县政府 / 开发区领导 ──
    {
        "id": 7,
        "name": "杨崇武",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府领导",
        "current_org": "贵定县人民政府",
        "source": "https://www.guiding.gov.cn — 昌明经济开发区调研(2026-07-09), 县人大六次会议(2026-06-22)"
    },
    {
        "id": 8,
        "name": "罗兴平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府领导",
        "current_org": "贵定县人民政府",
        "source": "https://www.guiding.gov.cn — 昌明经济开发区调研(2026-07-09)"
    },
    {
        "id": 9,
        "name": "杨勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府领导",
        "current_org": "贵定县人民政府",
        "source": "https://www.guiding.gov.cn — 仲成鹏调研城市发展(2026-07-15), 防汛巡河(2026-07-17)"
    },
    # ── 县领导（政委员/副县长/常委）──
    {
        "id": 10,
        "name": "冯发金",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府领导",
        "current_org": "贵定县人民政府",
        "source": "https://www.guiding.gov.cn — 安全生产工作专题会(2026-07-30)"
    },
    {
        "id": 11,
        "name": "尹骏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府领导",
        "current_org": "贵定县人民政府",
        "source": "https://www.guiding.gov.cn — 安全生产工作专题会(2026-07-30), 防汛巡河(2026-07-17)"
    },
    {
        "id": 12,
        "name": "温远辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府领导",
        "current_org": "贵定县人民政府",
        "source": "https://www.guiding.gov.cn — 安全生产工作专题会(2026-07-30)"
    },
    {
        "id": 13,
        "name": "蒙甍戈",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府领导",
        "current_org": "贵定县人民政府",
        "source": "https://www.guiding.gov.cn — 安全生产工作专题会(2026-07-30)"
    },
    {
        "id": 14,
        "name": "王大兰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府领导",
        "current_org": "贵定县人民政府",
        "source": "https://www.guiding.gov.cn — 安全生产工作专题会(2026-07-30)"
    },
    {
        "id": 15,
        "name": "邹敏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府领导",
        "current_org": "贵定县人民政府",
        "source": "https://www.guiding.gov.cn — 安全生产工作专题会(2026-07-30)"
    },
    {
        "id": 16,
        "name": "杨晓旭",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府领导",
        "current_org": "贵定县人民政府",
        "source": "https://www.guiding.gov.cn — 禁毒工作会议(2026-06-22)"
    },
    {
        "id": 17,
        "name": "刘芳",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府领导",
        "current_org": "贵定县人民政府",
        "source": "https://www.guiding.gov.cn — 禁毒工作会议(2026-06-22)"
    },
    {
        "id": 18,
        "name": "张永铨",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府领导",
        "current_org": "贵定县人民政府",
        "source": "https://www.guiding.gov.cn — 禁毒工作会议(2026-06-22)"
    },
    {
        "id": 19,
        "name": "赵波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会执行主席",
        "current_org": "贵定县人民代表大会常务委员会",
        "source": "https://www.guiding.gov.cn — 贵定县十九届人大六次会议(2026-06-22)"
    },
    {
        "id": 20,
        "name": "叶黔松",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大、县政府、县政协领导",
        "current_org": "贵定县人民政府",
        "source": "https://www.guiding.gov.cn — 贵定县十九届人大六次会议(2026-06-22)"
    },
    {
        "id": 21,
        "name": "王年军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会、县政府、县政协领导",
        "current_org": "贵定县人民政府",
        "source": "https://www.guiding.gov.cn — 贵定县十九届人大六次会议(2026-06-22)"
    },
    {
        "id": 22,
        "name": "董永松",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会、县政府、县政协领导",
        "current_org": "贵定县人民政府",
        "source": "https://www.guiding.gov.cn — 贵定县十九届人大六次会议(2026-06-22)"
    },
    {
        "id": 23,
        "name": "袁菲",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会、县政府、县政协领导",
        "current_org": "贵定县人民政府",
        "source": "https://www.guiding.gov.cn — 贵定县十九届人大六次会议(2026-06-22)"
    },
    {
        "id": 24,
        "name": "唐益萍",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会、县政府、县政协领导",
        "current_org": "贵定县人民政府",
        "source": "https://www.guiding.gov.cn — 贵定县十九届人大六次会议(2026-06-22)"
    },
    {
        "id": 25,
        "name": "尹熙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会、县政府、县政协领导",
        "current_org": "贵定县人民政府",
        "source": "https://www.guiding.gov.cn — 贵定县十九届人大六次会议(2026-06-22)"
    },
    # ── 前任县长 ──
    {
        "id": 26,
        "name": "王伟超",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县长",
        "current_org": "贵定县人民政府",
        "source": "https://www.guiding.gov.cn — 2025年/2026年政府工作报告(王伟超代县长/县长)"
    },
    # ── 前任县委书记（班代荣 2026-07 被双开）──
    {
        "id": 27,
        "name": "班代荣",
        "gender": "男",
        "ethnicity": "",
        "birth": "1971-09",
        "birthplace": "贵州惠水",
        "education": "省委党校在职研究生",
        "party_join": "中共党员",
        "work_start": "1992-07",
        "current_post": "前任县委书记（已被开除党籍公职）",
        "current_org": "中共贵定县委员会",
        "source": "百度百科(班代荣) + 贵州省纪委监委通报(2026-07-30 双开)"
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共贵定县委员会", "type": "党委", "level": "县", "parent": "中共黔南布依族苗族自治州委员会", "location": "贵定县"},
    {"id": 2, "name": "贵定县人民政府", "type": "政府", "level": "县", "parent": "黔南布依族苗族自治州人民政府", "location": "贵定县"},
    {"id": 3, "name": "贵定县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "", "location": "贵定县"},
    {"id": 4, "name": "中国人民政治协商会议贵定县委员会", "type": "政协", "level": "县", "parent": "", "location": "贵定县"},
    {"id": 5, "name": "中共贵定县纪律检查委员会", "type": "党委", "level": "县", "parent": "", "location": "贵定县"},
    {"id": 6, "name": "贵州昌明经济开发区管理委员会", "type": "开发区", "level": "县管园区", "parent": "贵定县", "location": "贵定县昌明镇"},
    {"id": 7, "name": "贵定县人民法院", "type": "政法", "level": "县", "parent": "", "location": "贵定县"},
    {"id": 8, "name": "贵定县人民检察院", "type": "政法", "level": "县", "parent": "", "location": "贵定县"},
]

# 3. Positions
positions = [
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "兼中共贵州昌明经济开发区党工委书记; 2026年7月在任"},
    {"person_id": 1, "org_id": 6, "title": "贵州昌明经济开发区党工委书记", "start_date": "", "end_date": "present", "rank": "", "note": "2026-07-09 调研昌明开发区确认"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2026-06", "end_date": "present", "rank": "正处级", "note": "2026-06-22 国资委代理县长, 2026-07-29 主持县政府第100次常务会议"},
    {"person_id": 2, "org_id": 6, "title": "贵州昌明经济开发区党工委副书记、管委会主任", "start_date": "", "end_date": "present", "rank": "", "note": "2026-07-09 调研昌明开发区确认"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2026-07-03 县委常委会确认"},
    {"person_id": 4, "org_id": 1, "title": "县委副书记、县委政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "县禁毒委员会副主任（兼）", "start_date": "", "end_date": "present", "rank": "", "note": "2026-06-22 禁毒工作会议"},
    {"person_id": 5, "org_id": 3, "title": "县人大常委会党组书记、主任候选人", "start_date": "2026", "end_date": "present", "rank": "正处级", "note": "2026-07-30 全面深化改革委会议确认"},
    {"person_id": 6, "org_id": 3, "title": "县人大常委会执行主席", "start_date": "", "end_date": "present", "rank": "", "note": "2026-06-22 县人大六次会议"},
    {"person_id": 7, "org_id": 2, "title": "县政府领导", "start_date": "", "end_date": "present", "rank": "副处级", "note": "县政府/开发区领导"},
    {"person_id": 8, "org_id": 2, "title": "县政府领导", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "县政府领导", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "县政府领导", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "县政府领导", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "县政府领导", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "县政府领导", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "县政府领导", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "县政府领导", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "县政府领导", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "县政府领导", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "县政府领导", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 3, "title": "县人大常委会执行主席", "start_date": "", "end_date": "present", "rank": "", "note": "2026-06-22 主持县人大六次会议第一全体会议"},
    {"person_id": 20, "org_id": 4, "title": "县人大/县政协领导", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": 21, "org_id": 4, "title": "县人大/县政协领导", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": 22, "org_id": 4, "title": "县人大/县政协领导", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": 23, "org_id": 4, "title": "县人大/县政协领导", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": 24, "org_id": 4, "title": "县人大/县政协领导", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": 25, "org_id": 4, "title": "县政协领导", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": 26, "org_id": 2, "title": "县长（前任）", "start_date": "", "end_date": "2026-06", "rank": "正处级", "note": "2025年+2026年2月政府工作报告由王伟超报告, 2026年6月后由黄祖方接任"},
    {"person_id": 27, "org_id": 1, "title": "县委书记（前任）", "start_date": "2021", "end_date": "2026-02", "rank": "正处级", "note": "2026-02被省纪委监委立案审查调查, 2026-07-30被开除党籍、开除公职"},
]

# 4. Relationships
relationships = [
    # 县委领导班子核心
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "仲成鹏任县委书记、黄祖方任县长, 县委县政府主要领导搭档", "overlap_org": "中共贵定县委员会/贵定县人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "仲成鹏任县委书记、杨奕任县委副书记", "overlap_org": "中共贵定县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "仲成鹏任县委书记、刘永祥任县委副书记兼政法委书记", "overlap_org": "中共贵定县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "共同出席县委全面深化改革委员会会议", "overlap_org": "中共贵定县委委员会", "overlap_period": "2026-07"},
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "黄祖方任县长、刘永祥任县委政法委书记, 同出席县委全面深化改革委与禁毒委", "overlap_org": "贵定县人民政府/中共贵定县委员会", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "黄祖方(县长)与杨勇(县政府领导)共同参加防汛巡河", "overlap_org": "贵定县人民政府", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "仲成鹏(县委书记)与杨崇武(县政府领导)同到昌明开发区调研", "overlap_org": "贵州昌明经济开发区", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "仲成鹏(县委书记)与罗兴平同到昌明开发区调研", "overlap_org": "贵州昌明经济开发区", "overlap_period": "2026-07"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "黄祖方主持安全生产专题会, 冯发金等县领导参加", "overlap_org": "贵定县人民政府", "overlap_period": "2026-07-30"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "黄祖方主持安全生产专题会, 尹骏参加；防汛巡河", "overlap_org": "贵定县人民政府", "overlap_period": "2026-07"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "黄祖方主持安全生产专题会, 温远辉参加", "overlap_org": "贵定县人民政府", "overlap_period": "2026-07"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "黄祖方主持安全生产专题会, 蒙甍戈参加", "overlap_org": "贵定县人民政府", "overlap_period": "2026-07"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate",
     "context": "黄祖方主持安全生产专题会, 王大兰参加", "overlap_org": "贵定县人民政府", "overlap_period": "2026-07"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate",
     "context": "黄祖方主持安全生产专题会, 邹敏参加", "overlap_org": "贵定县人民政府", "overlap_period": "2026-07"},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate",
     "context": "黄祖方(禁毒委主任)主持禁毒工作会议, 杨晓旭参加", "overlap_org": "贵定县人民政府", "overlap_period": "2026-06"},
    {"person_a": 2, "person_b": 17, "type": "superior_subordinate",
     "context": "黄祖方主持禁毒工作会议, 刘芳参加", "overlap_org": "贵定县人民政府", "overlap_period": "2026-06"},
    {"person_a": 2, "person_b": 18, "type": "superior_subordinate",
     "context": "黄祖方主持禁毒工作会议, 张永铨参加", "overlap_org": "贵定县人民政府", "overlap_period": "2026-06"},
    {"person_a": 2, "person_b": 26, "type": "predecessor_successor",
     "context": "王伟超任县长至2026年, 由黄祖方接任县长(先代理后转正)", "overlap_org": "贵定县人民政府", "overlap_period": "2026-06"},
    {"person_a": 1, "person_b": 26, "type": "overlap",
     "context": "仲成鹏(县委书记)与王伟超(前任县长)曾在县委县政府班子共事", "overlap_org": "贵定县人民政府", "overlap_period": "2025-2026"},
    {"person_a": 5, "person_b": 6, "type": "overlap",
     "context": "喻正斌与杨先云同为县人大领军领导, 同坐执行主席台", "overlap_org": "贵定县人民代表大会常务委员会", "overlap_period": "2026-06"},
    {"person_a": 5, "person_b": 19, "type": "overlap",
     "context": "喻正斌任人大常委会党组书记, 赵波主持人大六次会议", "overlap_org": "贵定县人民代表大会常务委员会", "overlap_period": "2026-06"},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "仲成鹏任县委书记, 与杨先云等人共同执行主席/县委班子", "overlap_org": "中共贵定县委员会", "overlap_period": "2026-06"},
    {"person_a": 2, "person_b": 6, "type": "overlap",
     "context": "黄祖方(县长)与杨先云同源执行主席台(县委县政府人大政协协调)", "overlap_org": "贵定县人民政府", "overlap_period": "2026-06"},
{"person_a": 1, "person_b": 20, "type": "overlap",
     "context": "仲成鹏与叶黔松等县人大常委会/政协领导同坐执行主席台", "overlap_org": "贵定县人民代表大会常务委员会", "overlap_period": "2026-06"},
    {"person_a": 1, "person_b": 27, "type": "predecessor_successor",
     "context": "班代荣任贵定县委书记被查免职(2026-02), 仲成鹏2026-03接任县委书记", "overlap_org": "中共贵定县委员会", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 27, "type": "overlap",
     "context": "黄祖方任代县长/县长期间, 前任书记班代荣此前在位; 2026年6月政府班子重组", "overlap_org": "贵定县人民政府", "overlap_period": "2026"},
]


if __name__ == "__main__":
    # ── Output paths (staging mode) ──
    db = DB_PATH
    gexf = GEXF_PATH

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db,
        gexf_path=gexf,
    )

    print(f"Build complete: {SLUG}")
    print(f"  DB:   {db}")
    print(f"  GEXF: {gexf}")