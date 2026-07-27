#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
湛江市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 地级市
Province: 广东省
Parent City:
Region: 湛江市
Targets: 市委书记 & 市长

Research Sources:
- 维基百科 (zh.wikipedia.org) — 湛江市词条
- 湛江市政府网站 (www.zhanjiang.gov.cn)

Current status (as of 2026-07-22):
- 市委书记: 余钢（2024年10月－）
- 市长: 李勇毅（2025年3月－）
- 人大常委会主任: 余钢（兼）
- 政协主席: 李多民（2022年1月－）

Research Date: 2026-07-22

Known gaps:
- 余钢详细履历（出生地、教育背景、完整工作经历）待补
- 李勇毅详细履历（出生地、教育背景、完整工作经历）待补
- 曾进泽2025年2月离任后的去向待查
- 刘红兵现任湖南省委宣传部部长（2024年起）
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "湛江市"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 市委领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "余钢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年4月",
        "birthplace": "广东丰顺",
        "native_place": "广东丰顺",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共湛江市委书记、市人大常委会主任",
        "current_org": "中共湛江市委员会",
        "source": "Wikipedia:湛江市"
    },
    {
        "id": 2,
        "name": "李勇毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年11月",
        "birthplace": "广东清远",
        "native_place": "广东清远",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共湛江市委副书记、市长",
        "current_org": "湛江市人民政府",
        "source": "Wikipedia:湛江市"
    },
    # ════════════════════════════════════════
    # 市人大常委会领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "李多民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年3月",
        "birthplace": "甘肃民勤",
        "native_place": "甘肃民勤",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "湛江市政协主席",
        "current_org": "政协湛江市委员会",
        "source": "Wikipedia:湛江市"
    },
    # ════════════════════════════════════════
    # 市委其他领导（湛江市领导分工中常见的常现任成员）
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "吴国雄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "湛江市委常委、常务副市长",
        "current_org": "湛江市人民政府",
        "source": "Wikipedia:湛江市"
    },
    {
        "id": 5,
        "name": "谢水明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "湛江市委常委、组织部部长",
        "current_org": "中共湛江市委组织部",
        "source": "Wikipedia:湛江市"
    },
    {
        "id": 6,
        "name": "宋会勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "湛江市委常委、市纪委书记、市监委主任",
        "current_org": "中共湛江市纪律检查委员会",
        "source": "Wikipedia:湛江市"
    },
    # ════════════════════════════════════════
    # 前任领导
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "刘红兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "湖南省委宣传部部长（原湛江市委书记）",
        "current_org": "中共湖南省委宣传部",
        "source": "Wikipedia:刘红兵"
    },
    {
        "id": 8,
        "name": "曾进泽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "原湛江市市长（2020年9月－2025年2月）",
        "current_org": "",
        "source": "Wikipedia:湛江市"
    },
    # ════════════════════════════════════════
    # 更早的历任主要领导
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "郑人豪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "原湛江市委书记（2017年3月－2021年5月）",
        "current_org": "",
        "source": "Wikipedia:湛江市"
    },
    {
        "id": 10,
        "name": "姜建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "原湛江市市长（2017年4月－2020年9月）",
        "current_org": "",
        "source": "Wikipedia:湛江市"
    },
    {
        "id": 11,
        "name": "王中丙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "原湛江市市长（2011年8月－2017年4月）",
        "current_org": "",
        "source": "Wikipedia:湛江市"
    },
    {
        "id": 12,
        "name": "魏宏广",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "原湛江市委书记（2016年3月－2017年3月）",
        "current_org": "",
        "source": "Wikipedia:湛江市"
    },
    {
        "id": 13,
        "name": "刘小华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "原湛江市委书记（2011年2月－2016年3月）",
        "current_org": "",
        "source": "Wikipedia:湛江市"
    },
    {
        "id": 14,
        "name": "阮日生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "原湛江市市长（2008年7月－2011年8月）",
        "current_org": "",
        "source": "Wikipedia:湛江市"
    },
    {
        "id": 15,
        "name": "陈耀光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "原湛江市委书记（2008年6月－2011年2月）/原湛江市市长（2005年8月－2008年6月）",
        "current_org": "",
        "source": "Wikipedia:湛江市"
    },
    {
        "id": 16,
        "name": "徐少华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "原湛江市委书记（2005年8月－2008年4月）/原湛江市市长（2002年4月－2005年8月）",
        "current_org": "",
        "source": "Wikipedia:湛江市"
    },
    {
        "id": 17,
        "name": "邓维龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "原湛江市委书记（2002年3月－2005年8月）",
        "current_org": "",
        "source": "Wikipedia:湛江市"
    },
]

# 2. Organizations
organizations = [
    # ── 湛江市四大班子 ──
    {"id": 1, "name": "中共湛江市委员会", "type": "党委", "level": "地级", "parent": "中共广东省委员会", "location": "湛江市赤坎区"},
    {"id": 2, "name": "湛江市人民政府", "type": "政府", "level": "地级", "parent": "广东省人民政府", "location": "湛江市赤坎区"},
    {"id": 3, "name": "湛江市人大常委会", "type": "人大", "level": "地级", "parent": "广东省人大常委会", "location": "湛江市赤坎区"},
    {"id": 4, "name": "政协湛江市委员会", "type": "政协", "level": "地级", "parent": "政协广东省委员会", "location": "湛江市赤坎区"},
    {"id": 5, "name": "中共湛江市纪律检查委员会", "type": "党委", "level": "地级", "parent": "中共湛江市委员会", "location": "湛江市赤坎区"},

    # ── 市委职能部门 ──
    {"id": 6, "name": "中共湛江市委组织部", "type": "党委", "level": "地级", "parent": "中共湛江市委员会", "location": "湛江市赤坎区"},
    {"id": 7, "name": "中共湛江市委宣传部", "type": "党委", "level": "地级", "parent": "中共湛江市委员会", "location": "湛江市赤坎区"},
    {"id": 8, "name": "中共湛江市委统战部", "type": "党委", "level": "地级", "parent": "中共湛江市委员会", "location": "湛江市赤坎区"},
    {"id": 9, "name": "中共湛江市委政法委", "type": "党委", "level": "地级", "parent": "中共湛江市委员会", "location": "湛江市赤坎区"},

    # ── 上级/相关省级组织 ──
    {"id": 10, "name": "中共广东省委员会", "type": "党委", "level": "省级", "parent": "", "location": "广东省广州市"},
    {"id": 11, "name": "广东省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "广东省广州市"},
    {"id": 12, "name": "广东省人大常委会", "type": "人大", "level": "省级", "parent": "", "location": "广东省广州市"},
    {"id": 13, "name": "政协广东省委员会", "type": "政协", "level": "省级", "parent": "", "location": "广东省广州市"},

    # ── 前任领导去向组织 ──
    {"id": 14, "name": "中共湖南省委宣传部", "type": "党委", "level": "省级", "parent": "中共湖南省委员会", "location": "湖南省长沙市"},
]

# 3. Positions (person -> organization relationships)
positions = [
    # 余钢 — 湛江市委书记
    {"person_id": 1, "org_id": 1, "title": "中共湛江市委书记", "start": "2024年10月", "end": "present", "rank": "正厅级"},
    # 余钢 — 湛江市人大常委会主任（兼）
    {"person_id": 1, "org_id": 3, "title": "湛江市人大常委会主任", "start": "2024年10月", "end": "present", "rank": "正厅级"},

    # 李勇毅 — 湛江市长
    {"person_id": 2, "org_id": 2, "title": "湛江市市长", "start": "2025年3月", "end": "present", "rank": "正厅级"},

    # 李多民 — 政协主席
    {"person_id": 3, "org_id": 4, "title": "湛江市政协主席", "start": "2022年1月", "end": "present", "rank": "正厅级"},

    # 吴国雄 — 常务副市长
    {"person_id": 4, "org_id": 2, "title": "湛江市委常委、常务副市长", "start": "待查", "end": "present", "rank": "副厅级"},

    # 谢水明 — 组织部部长
    {"person_id": 5, "org_id": 6, "title": "湛江市委常委、组织部部长", "start": "待查", "end": "present", "rank": "副厅级"},

    # 宋会勇 — 纪委书记
    {"person_id": 6, "org_id": 5, "title": "湛江市委常委、市纪委书记、市监委主任", "start": "待查", "end": "present", "rank": "副厅级"},

    # 刘红兵 — 前市委书记
    {"person_id": 7, "org_id": 1, "title": "中共湛江市委书记", "start": "2021年5月", "end": "2024年10月", "rank": "正厅级"},
    {"person_id": 7, "org_id": 14, "title": "湖南省委宣传部部长", "start": "2024年", "end": "present", "rank": "副省级"},

    # 曾进泽 — 前市长
    {"person_id": 8, "org_id": 2, "title": "湛江市市长", "start": "2020年9月", "end": "2025年2月", "rank": "正厅级"},

    # 郑人豪 — 前市委书记
    {"person_id": 9, "org_id": 1, "title": "中共湛江市委书记", "start": "2017年3月", "end": "2021年5月", "rank": "正厅级"},

    # 姜建军 — 前市长
    {"person_id": 10, "org_id": 2, "title": "湛江市市长", "start": "2017年4月", "end": "2020年9月", "rank": "正厅级"},

    # 王中丙 — 前市长
    {"person_id": 11, "org_id": 2, "title": "湛江市市长", "start": "2011年8月", "end": "2017年4月", "rank": "正厅级"},

    # 魏宏广 — 前市委书记
    {"person_id": 12, "org_id": 1, "title": "中共湛江市委书记", "start": "2016年3月", "end": "2017年3月", "rank": "正厅级"},

    # 刘小华 — 前市委书记
    {"person_id": 13, "org_id": 1, "title": "中共湛江市委书记", "start": "2011年2月", "end": "2016年3月", "rank": "正厅级"},

    # 阮日生 — 前市长
    {"person_id": 14, "org_id": 2, "title": "湛江市市长", "start": "2008年7月", "end": "2011年8月", "rank": "正厅级"},

    # 陈耀光 — 前书记兼前市长
    {"person_id": 15, "org_id": 2, "title": "湛江市市长", "start": "2005年8月", "end": "2008年6月", "rank": "正厅级"},
    {"person_id": 15, "org_id": 1, "title": "中共湛江市委书记", "start": "2008年6月", "end": "2011年2月", "rank": "正厅级"},

    # 徐少华 — 前书记兼前市长
    {"person_id": 16, "org_id": 2, "title": "湛江市市长", "start": "2002年4月", "end": "2005年8月", "rank": "正厅级"},
    {"person_id": 16, "org_id": 1, "title": "中共湛江市委书记", "start": "2005年8月", "end": "2008年4月", "rank": "正厅级"},

    # 邓维龙 — 前市委书记
    {"person_id": 17, "org_id": 1, "title": "中共湛江市委书记", "start": "2002年3月", "end": "2005年8月", "rank": "正厅级"},
]

# 4. Relationships (person <-> person)
relationships = [
    # 余钢 — 李勇毅（现任搭档）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "2024年10月起余钢任书记、李勇毅任市长搭档", "overlap_org": "中共湛江市委员会/湛江市人民政府", "overlap_period": "2024年10月至今"},

    # 余钢 — 刘红兵（前后任书记）
    {"person_a": 1, "person_b": 7, "type": "predecessor_successor", "context": "余钢接替刘红兵任湛江市委书记", "overlap_org": "中共湛江市委员会", "overlap_period": "2024年10月"},

    # 李勇毅 — 曾进泽（前后任市长）
    {"person_a": 2, "person_b": 8, "type": "predecessor_successor", "context": "李勇毅接替曾进泽任湛江市市长", "overlap_org": "湛江市人民政府", "overlap_period": "2025年3月"},

    # 刘红兵 — 郑人豪（前后任书记）
    {"person_a": 7, "person_b": 9, "type": "predecessor_successor", "context": "刘红兵接替郑人豪任湛江市委书记", "overlap_org": "中共湛江市委员会", "overlap_period": "2021年5月"},

    # 曾进泽 — 姜建军（前后任市长）
    {"person_a": 8, "person_b": 10, "type": "predecessor_successor", "context": "曾进泽接替姜建军任湛江市市长", "overlap_org": "湛江市人民政府", "overlap_period": "2020年9月"},

    # 郑人豪 — 魏宏广（前后任书记）
    {"person_a": 9, "person_b": 12, "type": "predecessor_successor", "context": "郑人豪接替魏宏广任湛江市委书记", "overlap_org": "中共湛江市委员会", "overlap_period": "2017年3月"},

    # 姜建军 — 王中丙（前后任市长）
    {"person_a": 10, "person_b": 11, "type": "predecessor_successor", "context": "姜建军接替王中丙任湛江市市长", "overlap_org": "湛江市人民政府", "overlap_period": "2017年4月"},

    # 魏宏广 — 刘小华（前后任书记）
    {"person_a": 12, "person_b": 13, "type": "predecessor_successor", "context": "魏宏广接替刘小华任湛江市委书记", "overlap_org": "中共湛江市委员会", "overlap_period": "2016年3月"},

    # 王中丙 — 阮日生（前后任市长）
    {"person_a": 11, "person_b": 14, "type": "predecessor_successor", "context": "王中丙接替阮日生任湛江市市长", "overlap_org": "湛江市人民政府", "overlap_period": "2011年8月"},

    # 刘小华 — 陈耀光（前后任书记）
    {"person_a": 13, "person_b": 15, "type": "predecessor_successor", "context": "刘小华接替陈耀光任湛江市委书记", "overlap_org": "中共湛江市委员会", "overlap_period": "2011年2月"},

    # 陈耀光 — 阮日生（曾先后任市长和书记搭档）
    {"person_a": 15, "person_b": 14, "type": "overlap", "context": "陈耀光任书记时阮日生任市长", "overlap_org": "中共湛江市委员会/湛江市人民政府", "overlap_period": "2008年7月－2011年2月"},

    # 陈耀光 — 徐少华（前后任）
    {"person_a": 15, "person_b": 16, "type": "predecessor_successor", "context": "陈耀光接替徐少华任湛江市市长，后接替书记", "overlap_org": "湛江市人民政府", "overlap_period": "2005年8月"},
    {"person_a": 15, "person_b": 16, "type": "predecessor_successor", "context": "陈耀光接替徐少华任湛江市委书记", "overlap_org": "中共湛江市委员会", "overlap_period": "2008年6月"},

    # 徐少华 — 邓维龙（前后任书记）
    {"person_a": 16, "person_b": 17, "type": "predecessor_successor", "context": "徐少华接替邓维龙任湛江市委书记", "overlap_org": "中共湛江市委员会", "overlap_period": "2005年8月"},

    # 陈耀光 — 邓维龙（书记搭档时期）
    {"person_a": 15, "person_b": 17, "type": "overlap", "context": "邓维龙任书记时陈耀光任市长（后接书记）", "overlap_org": "中共湛江市委员会/湛江市人民政府", "overlap_period": "2005年8月－2008年6月"},
]

# ── Run ──
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
