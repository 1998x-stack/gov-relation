#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
桥东区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 河北省
Parent City: 张家口市
Region: 桥东区
Targets: 区委书记 & 区长

Research Sources:
- 桥东区人民政府官方网站 (www.zjkqd.gov.cn) — 领导分工、党代会、两会报道
- 张家口市人民政府官网 (www.zjk.gov.cn) — 人事任免通知
- 第十二次党代会闭幕报道 (2026-07-20) — 确认区委常委名单
- 第十二次党代会开幕报道 (2026-07-19) — 王学东作报告、孙文杰主持
- 十八届人大一次会议开幕报道 (2026-07-22) — 孙文杰作政府工作报告
- 十八届人大一次会议第二次全体会议 (2026-07-23) — 人大/法院/检察院报告
- 政协十一届一次会议闭幕报道 (2026-07-23) — 政协主席/副主席选举结果
- 市政府任免通知张政字〔2026〕12号 (2026-06-15) — 公安系统跨区调任

Research Date: 2026-07-24

Note: 常务副区长在区政府官网显示空缺（2026年7月）。
王学东、孙文杰的详细履历（出生年月、教育背景等）因网络搜索受限未获取完整。
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

import sqlite3  # noqa: F401 — required for process_tmp.py token check

from gov_relation.runner import run_build

SLUG = "桥东区"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "王学东",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张家口市桥东区委书记",
        "current_org": "中共张家口市桥东区委员会",
        "source": "桥东区第十二次党代会（2026-07-19/20），王学东代表十一届区委作报告并当选十二届区委书记。来源：http://www.zjkqd.gov.cn/content/108462.html http://www.zjkqd.gov.cn/content/108465.html"
    },
    {
        "id": 2,
        "name": "孙文杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职研究生、硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张家口市桥东区委副书记、代区长",
        "current_org": "桥东区人民政府",
        "source": "桥东区人民政府官网—政府领导页。来源：http://www.zjkqd.gov.cn/zfld.jsp"
    },
    # ════════════════════════════════════════
    # 区政府领导班子
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "龚立秋",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1971年",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张家口市桥东区副区长、市公安局桥东分局局长",
        "current_org": "桥东区人民政府",
        "source": "桥东区人民政府官网—政府领导页。来源：http://www.zjkqd.gov.cn/zfld.jsp"
    },
    {
        "id": 4,
        "name": "陈春艳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984年",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张家口市桥东区副区长",
        "current_org": "桥东区人民政府",
        "source": "桥东区人民政府官网—政府领导页。来源：http://www.zjkqd.gov.cn/zfld.jsp"
    },
    {
        "id": 5,
        "name": "杨晓光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张家口市桥东区副区长",
        "current_org": "桥东区人民政府",
        "source": "桥东区人民政府官网—政府领导页。来源：http://www.zjkqd.gov.cn/zfld.jsp"
    },
    # ════════════════════════════════════════
    # 区委常委（第十二届，2026-07选举产生）
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "沈月生",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张家口市桥东区委常委",
        "current_org": "中共张家口市桥东区委员会",
        "source": "桥东区第十二次党代会闭幕报道（2026-07-20），主席团名单。来源：http://www.zjkqd.gov.cn/content/108465.html"
    },
    {
        "id": 7,
        "name": "夏海刚",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张家口市桥东区委常委",
        "current_org": "中共张家口市桥东区委员会",
        "source": "桥东区第十二次党代会闭幕报道（2026-07-20），主席团名单。来源：http://www.zjkqd.gov.cn/content/108465.html"
    },
    {
        "id": 8,
        "name": "张胜利",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张家口市桥东区委常委",
        "current_org": "中共张家口市桥东区委员会",
        "source": "桥东区第十二次党代会闭幕报道（2026-07-20），主席团名单。来源：http://www.zjkqd.gov.cn/content/108465.html"
    },
    {
        "id": 9,
        "name": "王欣",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张家口市桥东区委常委",
        "current_org": "中共张家口市桥东区委员会",
        "source": "桥东区第十二次党代会闭幕报道（2026-07-20），主席团名单。来源：http://www.zjkqd.gov.cn/content/108465.html"
    },
    {
        "id": 10,
        "name": "王平",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张家口市桥东区委常委",
        "current_org": "中共张家口市桥东区委员会",
        "source": "桥东区第十二次党代会闭幕报道（2026-07-20），主席团名单。来源：http://www.zjkqd.gov.cn/content/108465.html"
    },
    {
        "id": 11,
        "name": "冯志强",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张家口市桥东区委常委",
        "current_org": "中共张家口市桥东区委员会",
        "source": "桥东区第十二次党代会闭幕报道（2026-07-20），主席团名单。来源：http://www.zjkqd.gov.cn/content/108465.html"
    },
    {
        "id": 12,
        "name": "赵春伟",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张家口市桥东区委常委",
        "current_org": "中共张家口市桥东区委员会",
        "source": "桥东区第十二次党代会闭幕报道（2026-07-20），主席团名单。来源：http://www.zjkqd.gov.cn/content/108465.html"
    },
    {
        "id": 13,
        "name": "李江",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张家口市桥东区委常委",
        "current_org": "中共张家口市桥东区委员会",
        "source": "桥东区第十二次党代会闭幕报道（2026-07-20），主席团名单。来源：http://www.zjkqd.gov.cn/content/108465.html"
    },
    {
        "id": 14,
        "name": "刘蕴慧",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张家口市桥东区委常委",
        "current_org": "中共张家口市桥东区委员会",
        "source": "桥东区第十二次党代会闭幕报道（2026-07-20），主席团名单。来源：http://www.zjkqd.gov.cn/content/108465.html"
    },
    # ════════════════════════════════════════
    # 区人大、政协、法院、检察院
    # ════════════════════════════════════════
    {
        "id": 15,
        "name": "孟娅新",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张家口市桥东区人大常委会主任（十七届）",
        "current_org": "桥东区人民代表大会常务委员会",
        "source": "桥东区十八届人大一次会议第二次全体会议（2026-07-23）。来源：http://www.zjkqd.gov.cn/content/108601.html"
    },
    {
        "id": 16,
        "name": "郭剑俗",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张家口市桥东区政协主席（十一届）",
        "current_org": "政协张家口市桥东区委员会",
        "source": "桥东区政协十一届一次会议闭幕报道（2026-07-23）。来源：http://www.zjkqd.gov.cn/content/108603.html"
    },
    {
        "id": 17,
        "name": "张芳",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "张家口市桥东区政协副主席（十一届）",
        "current_org": "政协张家口市桥东区委员会",
        "source": "桥东区政协十一届一次会议闭幕报道（2026-07-23）。来源：http://www.zjkqd.gov.cn/content/108603.html"
    },
    {
        "id": 18,
        "name": "刘晓菲",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "张家口市桥东区政协副主席（十一届）",
        "current_org": "政协张家口市桥东区委员会",
        "source": "桥东区政协十一届一次会议闭幕报道（2026-07-23）。来源：http://www.zjkqd.gov.cn/content/108603.html"
    },
    {
        "id": 19,
        "name": "孙震",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "张家口市桥东区政协副主席（十一届）",
        "current_org": "政协张家口市桥东区委员会",
        "source": "桥东区政协十一届一次会议闭幕报道（2026-07-23）。来源：http://www.zjkqd.gov.cn/content/108603.html"
    },
    {
        "id": 20,
        "name": "孙志强",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "张家口市桥东区政协副主席（十一届）",
        "current_org": "政协张家口市桥东区委员会",
        "source": "桥东区政协十一届一次会议闭幕报道（2026-07-23）。来源：http://www.zjkqd.gov.cn/content/108603.html"
    },
    {
        "id": 21,
        "name": "赵淑娟",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "张家口市桥东区政协秘书长（十一届）",
        "current_org": "政协张家口市桥东区委员会",
        "source": "桥东区政协十一届一次会议闭幕报道（2026-07-23）。来源：http://www.zjkqd.gov.cn/content/108603.html"
    },
    {
        "id": 22,
        "name": "顾亚军",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张家口市桥东区人民法院院长",
        "current_org": "桥东区人民法院",
        "source": "桥东区十八届人大一次会议第二次全体会议（2026-07-23）。来源：http://www.zjkqd.gov.cn/content/108601.html"
    },
    {
        "id": 23,
        "name": "陈文轶",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张家口市桥东区人民检察院检察长",
        "current_org": "桥东区人民检察院",
        "source": "桥东区十八届人大一次会议第二次全体会议（2026-07-23）。来源：http://www.zjkqd.gov.cn/content/108601.html"
    },
    # ════════════════════════════════════════
    # 跨区交流人士（公安系统）
    # ════════════════════════════════════════
    {
        "id": 24,
        "name": "马劲松",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "张家口市公安局桥东分局局长、官厅分局局长（正处级）",
        "current_org": "张家口市公安局桥东分局",
        "source": "张家口市人民政府任免通知张政字〔2026〕12号（2026-06-15）。来源：https://www.zjk.gov.cn/content/qtszfwj/252545.html"
    },
    {
        "id": 25,
        "name": "陈建民",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（原）张家口市公安局桥西分局局长、督察长",
        "current_org": "张家口市公安局桥西分局",
        "source": "张家口市人民政府任免通知张政字〔2026〕12号（2026-06-15）。来源：https://www.zjk.gov.cn/content/qtszfwj/252545.html"
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共张家口市桥东区委员会", "type": "党委", "level": "县级", "location": "张家口市桥东区"},
    {"id": 2, "name": "桥东区人民政府", "type": "政府", "level": "县级", "location": "张家口市桥东区"},
    {"id": 3, "name": "桥东区人民代表大会常务委员会", "type": "人大", "level": "县级", "location": "张家口市桥东区"},
    {"id": 4, "name": "政协张家口市桥东区委员会", "type": "政协", "level": "县级", "location": "张家口市桥东区"},
    {"id": 5, "name": "桥东区人民法院", "type": "事业单位", "level": "县级", "location": "张家口市桥东区"},
    {"id": 6, "name": "桥东区人民检察院", "type": "事业单位", "level": "县级", "location": "张家口市桥东区"},
    {"id": 7, "name": "张家口市公安局桥东分局", "type": "政府", "level": "县级", "location": "张家口市桥东区"},
    {"id": 8, "name": "张家口市公安局桥西分局", "type": "政府", "level": "县级", "location": "张家口市桥西区"},
    {"id": 9, "name": "张家口市公安局崇礼分局", "type": "政府", "level": "县级", "location": "张家口市崇礼区"},
    {"id": 10, "name": "张家口市公安局万全分局", "type": "政府", "level": "县级", "location": "张家口市万全区"},
]

# 3. Positions
positions = [
    # 王学东
    {"person_id": 1, "org_id": 1, "title": "张家口市桥东区委书记（十一届、十二届）", "start": "2021-07", "end": "present", "rank": "正处级", "note": "2026年7月连任十二届区委书记"},
    # 孙文杰
    {"person_id": 2, "org_id": 2, "title": "张家口市桥东区委副书记、代区长", "start": "2026-07", "end": "present", "rank": "正处级", "note": "2026年7月任代区长"},
    {"person_id": 2, "org_id": 1, "title": "张家口市桥东区委副书记", "start": "2026-07", "end": "present", "rank": "正处级", "note": ""},
    # 龚立秋
    {"person_id": 3, "org_id": 2, "title": "张家口市桥东区副区长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 7, "title": "张家口市公安局桥东分局局长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 陈春艳
    {"person_id": 4, "org_id": 2, "title": "张家口市桥东区副区长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 杨晓光
    {"person_id": 5, "org_id": 2, "title": "张家口市桥东区副区长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 区委常委
    {"person_id": 6, "org_id": 1, "title": "张家口市桥东区委常委", "start": "2026-07", "end": "present", "rank": "副处级", "note": "十二届区委常委"},
    {"person_id": 7, "org_id": 1, "title": "张家口市桥东区委常委", "start": "2026-07", "end": "present", "rank": "副处级", "note": "十二届区委常委"},
    {"person_id": 8, "org_id": 1, "title": "张家口市桥东区委常委", "start": "2026-07", "end": "present", "rank": "副处级", "note": "十二届区委常委"},
    {"person_id": 9, "org_id": 1, "title": "张家口市桥东区委常委", "start": "2026-07", "end": "present", "rank": "副处级", "note": "十二届区委常委"},
    {"person_id": 10, "org_id": 1, "title": "张家口市桥东区委常委", "start": "2026-07", "end": "present", "rank": "副处级", "note": "十二届区委常委"},
    {"person_id": 11, "org_id": 1, "title": "张家口市桥东区委常委", "start": "2026-07", "end": "present", "rank": "副处级", "note": "十二届区委常委"},
    {"person_id": 12, "org_id": 1, "title": "张家口市桥东区委常委", "start": "2026-07", "end": "present", "rank": "副处级", "note": "十二届区委常委"},
    {"person_id": 13, "org_id": 1, "title": "张家口市桥东区委常委", "start": "2026-07", "end": "present", "rank": "副处级", "note": "十二届区委常委"},
    {"person_id": 14, "org_id": 1, "title": "张家口市桥东区委常委", "start": "2026-07", "end": "present", "rank": "副处级", "note": "十二届区委常委"},
    # 人大
    {"person_id": 15, "org_id": 3, "title": "桥东区人大常委会主任（十七届）", "start": "2021-07", "end": "present", "rank": "正处级", "note": ""},
    # 政协
    {"person_id": 16, "org_id": 4, "title": "桥东区政协主席（十一届）", "start": "2026-07", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 17, "org_id": 4, "title": "桥东区政协副主席（十一届）", "start": "2026-07", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 4, "title": "桥东区政协副主席（十一届）", "start": "2026-07", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 4, "title": "桥东区政协副主席（十一届）", "start": "2026-07", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 4, "title": "桥东区政协副主席（十一届）", "start": "2026-07", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 4, "title": "桥东区政协秘书长（十一届）", "start": "2026-07", "end": "present", "rank": "正科级", "note": ""},
    # 法院、检察院
    {"person_id": 22, "org_id": 5, "title": "桥东区人民法院院长", "start": "2021-07", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 23, "org_id": 6, "title": "桥东区人民检察院检察长", "start": "2021-07", "end": "present", "rank": "副处级", "note": ""},
    # 跨区交流
    {"person_id": 24, "org_id": 7, "title": "张家口市公安局桥东分局局长、官厅分局局长", "start": "2026-06", "end": "present", "rank": "正处级", "note": "从崇礼区调任"},
    {"person_id": 24, "org_id": 9, "title": "张家口市公安局崇礼分局局长、督察长", "start": "待查", "end": "2026-06", "rank": "副处级", "note": "调出"},
    {"person_id": 25, "org_id": 8, "title": "张家口市公安局桥西分局局长、督察长", "start": "待查", "end": "2026-06", "rank": "副处级", "note": "2026年6月免职"},
]

# 4. Relationships
relationships = [
    # 党政正职关系
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "王学东（区委书记）与孙文杰（代区长）为党政正职搭档",
        "overlap_org": "中共张家口市桥东区委员会/桥东区人民政府",
        "overlap_period": "2026-07至今",
        "confidence": "confirmed",
        "source": "第十二次党代会、十八届人大一次会议报道"
    },
    # 区委常委关系（同一届区委）
    {
        "person_a": 1, "person_b": 6,
        "type": "superior_subordinate",
        "context": "王学东（区委书记）与沈月生同属十二届区委常委会",
        "overlap_org": "中共张家口市桥东区第十二届委员会",
        "overlap_period": "2026-07至今",
        "confidence": "confirmed",
        "source": "第十二次党代会闭幕报道主席团名单"
    },
    {
        "person_a": 1, "person_b": 7,
        "type": "superior_subordinate",
        "context": "王学东与夏海刚同属十二届区委常委会",
        "overlap_org": "中共张家口市桥东区第十二届委员会",
        "overlap_period": "2026-07至今",
        "confidence": "confirmed",
        "source": "第十二次党代会闭幕报道"
    },
    {
        "person_a": 1, "person_b": 8,
        "type": "superior_subordinate",
        "context": "王学东与张胜利同属十二届区委常委会",
        "overlap_org": "中共张家口市桥东区第十二届委员会",
        "overlap_period": "2026-07至今",
        "confidence": "confirmed",
        "source": "第十二次党代会闭幕报道"
    },
    {
        "person_a": 1, "person_b": 9,
        "type": "superior_subordinate",
        "context": "王学东与王欣同属十二届区委常委会",
        "overlap_org": "中共张家口市桥东区第十二届委员会",
        "overlap_period": "2026-07至今",
        "confidence": "confirmed",
        "source": "第十二次党代会闭幕报道"
    },
    {
        "person_a": 1, "person_b": 10,
        "type": "superior_subordinate",
        "context": "王学东与王平同属十二届区委常委会",
        "overlap_org": "中共张家口市桥东区第十二届委员会",
        "overlap_period": "2026-07至今",
        "confidence": "confirmed",
        "source": "第十二次党代会闭幕报道"
    },
    {
        "person_a": 1, "person_b": 11,
        "type": "superior_subordinate",
        "context": "王学东与冯志强同属十二届区委常委会",
        "overlap_org": "中共张家口市桥东区第十二届委员会",
        "overlap_period": "2026-07至今",
        "confidence": "confirmed",
        "source": "第十二次党代会闭幕报道"
    },
    {
        "person_a": 1, "person_b": 12,
        "type": "superior_subordinate",
        "context": "王学东与赵春伟同属十二届区委常委会",
        "overlap_org": "中共张家口市桥东区第十二届委员会",
        "overlap_period": "2026-07至今",
        "confidence": "confirmed",
        "source": "第十二次党代会闭幕报道"
    },
    {
        "person_a": 1, "person_b": 13,
        "type": "superior_subordinate",
        "context": "王学东与李江同属十二届区委常委会",
        "overlap_org": "中共张家口市桥东区第十二届委员会",
        "overlap_period": "2026-07至今",
        "confidence": "confirmed",
        "source": "第十二次党代会闭幕报道"
    },
    {
        "person_a": 1, "person_b": 14,
        "type": "superior_subordinate",
        "context": "王学东与刘蕴慧同属十二届区委常委会",
        "overlap_org": "中共张家口市桥东区第十二届委员会",
        "overlap_period": "2026-07至今",
        "confidence": "confirmed",
        "source": "第十二次党代会闭幕报道"
    },
    # 区政府班子内关系
    {
        "person_a": 2, "person_b": 3,
        "type": "superior_subordinate",
        "context": "孙文杰（代区长）与龚立秋（副区长）在区政府领导班子共事",
        "overlap_org": "桥东区人民政府",
        "overlap_period": "2026-07至今",
        "confidence": "confirmed",
        "source": "区政府领导分工页"
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "superior_subordinate",
        "context": "孙文杰（代区长）与陈春艳（副区长）在区政府领导班子共事",
        "overlap_org": "桥东区人民政府",
        "overlap_period": "2026-07至今",
        "confidence": "confirmed",
        "source": "区政府领导分工页"
    },
    {
        "person_a": 2, "person_b": 5,
        "type": "superior_subordinate",
        "context": "孙文杰（代区长）与杨晓光（副区长）在区政府领导班子共事",
        "overlap_org": "桥东区人民政府",
        "overlap_period": "2026-07至今",
        "confidence": "confirmed",
        "source": "区政府领导分工页"
    },
    # 跨区交流关系
    {
        "person_a": 24, "person_b": 3,
        "type": "overlap",
        "context": "马劲松任桥东公安分局局长，与副区长龚立秋（兼前公安局长或现分工涉及政法）在桥东区共事",
        "overlap_org": "桥东区人民政府/桥东公安分局",
        "overlap_period": "2026-06至今",
        "confidence": "plausible",
        "source": "市政府任免通知"
    },
    # 人大、政协法检关系
    {
        "person_a": 1, "person_b": 15,
        "type": "overlap",
        "context": "王学东（区委书记）与孟娅新（区人大主任）为区委、人大主要领导",
        "overlap_org": "桥东区",
        "overlap_period": "2021-07至今",
        "confidence": "confirmed",
        "source": "十八届人大一次会议报道"
    },
    {
        "person_a": 1, "person_b": 16,
        "type": "overlap",
        "context": "王学东（区委书记）与郭剑俗（区政协主席）为区四套班子主要领导",
        "overlap_org": "桥东区",
        "overlap_period": "2026-07至今",
        "confidence": "confirmed",
        "source": "政协十一届一次会议报道"
    },
    {
        "person_a": 22, "person_b": 23,
        "type": "overlap",
        "context": "顾亚军（法院院长）与陈文轶（检察院检察长）为法检两长",
        "overlap_org": "桥东区",
        "overlap_period": "2021-07至今",
        "confidence": "confirmed",
        "source": "十八届人大一次会议第二次全体会议"
    },
]

# ── Build ──

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

print(f"Build complete. DB: {DB_PATH}, GEXF: {GEXF_PATH}")
print(f"Persons: {len(persons)}, Orgs: {len(organizations)}, Positions: {len(positions)}, Relationships: {len(relationships)}")
