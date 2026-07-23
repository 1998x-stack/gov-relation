#!/usr/bin/env python3
"""
满城区领导班子工作关系网络 — Build script
河北省保定市满城区

Confirmed sources:
- 保定市满城区人民政府门户网站 (http://www.mancheng.gov.cn/): confirms 刘玉辉 as 区委书记, 田松 as 区长
- 满城区第四次党代会 (2026-07-19~21): elected new区委领导班子
- 满城区四届人大一次会议 (2026-07-22): 田松作政府工作报告
- News: "区委书记刘玉辉主持区委常委会（扩大）会议" (2026-07-17)
- News: "政协保定市满城区第四届委员会第一次会议开幕" 刘玉辉讲话, 田松出席

Research date: 2026-07-23
"""

import json
import os
import sys
from datetime import date

# Add repo root to path
_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

import sqlite3  # noqa: used by gov_relation.runner

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

AS_OF = "2026-07-23"
DB_PATH = None  # Will be set in main()
GEXF_PATH = None  # Will be set in main()

# ── PERSONS ──
persons = [
    # ── 区委书记 (Party Secretary) ──
    {
        "id": 1,
        "name": "刘玉辉",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保定市满城区委书记",
        "current_org": "中共保定市满城区委员会",
        "source": "http://www.mancheng.gov.cn/",
    },
    # ── 区长 (District Mayor) ──
    {
        "id": 2,
        "name": "田松",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保定市满城区委副书记、区长",
        "current_org": "保定市满城区人民政府/中共保定市满城区委员会",
        "source": "http://www.mancheng.gov.cn/",
    },
    # ── 区委副书记 (Deputy Party Secretary) ──
    {
        "id": 3,
        "name": "屈会东",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保定市满城区委副书记",
        "current_org": "中共保定市满城区委员会",
        "source": "http://www.mancheng.gov.cn/",
    },
    # ── 区人大常委会主任 (人大) ──
    {
        "id": 4,
        "name": "史宏昌",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保定市满城区人大常委会主任",
        "current_org": "保定市满城区人民代表大会常务委员会",
        "source": "http://www.mancheng.gov.cn/",
    },
    # ── 区委常委、纪委书记 (Discipline) ──
    {
        "id": 5,
        "name": "徐润雨",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保定市满城区委常委、纪委书记",
        "current_org": "中共保定市满城区纪律检查委员会",
        "source": "http://www.mancheng.gov.cn/",
    },
    # ── 区委常委、组织部长 (Organization) ──
    {
        "id": 6,
        "name": "牛海利",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保定市满城区委常委、组织部部长",
        "current_org": "中共保定市满城区委员会组织部",
        "source": "http://www.mancheng.gov.cn/",
    },
    # ── 区委常委、常务副区长 (Deputy Mayor) ──
    {
        "id": 7,
        "name": "吕振",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保定市满城区委常委、区政府副区长（常务）",
        "current_org": "保定市满城区人民政府",
        "source": "http://www.mancheng.gov.cn/",
    },
    # ── 区委常委、宣传部长 (Propaganda) ──
    {
        "id": 8,
        "name": "赵英晓",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保定市满城区委常委、宣传部部长",
        "current_org": "中共保定市满城区委员会宣传部",
        "source": "http://www.mancheng.gov.cn/",
    },
    # ── 区委常委、政法委书记 (政法) ──
    {
        "id": 9,
        "name": "甄泳亮",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保定市满城区委常委、政法委书记",
        "current_org": "中共保定市满城区委员会政法委员会",
        "source": "http://www.mancheng.gov.cn/",
    },
    # ── 区委常委、统战部长 (United Front) ──
    {
        "id": 10,
        "name": "赵丽娜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保定市满城区委常委、统战部部长",
        "current_org": "中共保定市满城区委员会统战部",
        "source": "http://www.mancheng.gov.cn/",
    },
    # ── 区委常委、区委办主任 (Office Director) ──
    {
        "id": 11,
        "name": "任沛显",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保定市满城区委常委、区委办公室主任",
        "current_org": "中共保定市满城区委员会办公室",
        "source": "http://www.mancheng.gov.cn/",
    },
    # ── 区委常委、人武部 (Military) ──
    {
        "id": 12,
        "name": "马榕徽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保定市满城区委常委、人武部",
        "current_org": "保定市满城区人民武装部",
        "source": "http://www.mancheng.gov.cn/",
    },
    # ── 副区长 (Deputy Mayor) ──
    {
        "id": 13,
        "name": "刘建凯",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保定市满城区人民政府副区长",
        "current_org": "保定市满城区人民政府",
        "source": "http://www.mancheng.gov.cn/",
    },
    # ── 副区长 ──
    {
        "id": 14,
        "name": "刘严冰",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保定市满城区人民政府副区长",
        "current_org": "保定市满城区人民政府",
        "source": "http://www.mancheng.gov.cn/",
    },
    # ── 副区长 ──
    {
        "id": 15,
        "name": "郝硕",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保定市满城区人民政府副区长",
        "current_org": "保定市满城区人民政府",
        "source": "http://www.mancheng.gov.cn/",
    },
    # ── 副区长 ──
    {
        "id": 16,
        "name": "梁民",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保定市满城区人民政府副区长",
        "current_org": "保定市满城区人民政府",
        "source": "http://www.mancheng.gov.cn/",
    },
    # ── 副区长 ──
    {
        "id": 17,
        "name": "冉永占",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保定市满城区人民政府副区长",
        "current_org": "保定市满城区人民政府",
        "source": "http://www.mancheng.gov.cn/",
    },
    # ── 区政协党组书记 (政协) ──
    {
        "id": 18,
        "name": "钱国伟",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保定市满城区政协党组书记",
        "current_org": "中国人民政治协商会议保定市满城区委员会",
        "source": "http://www.mancheng.gov.cn/",
    },
    # ── 人大常委会副主任(女) ──
    {
        "id": 19,
        "name": "连冬红",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保定市满城区人大常委会副主任",
        "current_org": "保定市满城区人民代表大会常务委员会",
        "source": "http://www.mancheng.gov.cn/",
    },
    # ── 法检两院 ──
    {
        "id": 20,
        "name": "张桂霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保定市满城区人民法院院长",
        "current_org": "保定市满城区人民法院",
        "source": "http://www.mancheng.gov.cn/",
    },
    {
        "id": 21,
        "name": "李迎初",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保定市满城区人民检察院检察长",
        "current_org": "保定市满城区人民检察院",
        "source": "http://www.mancheng.gov.cn/",
    },
    # ── 前任区委书记 (Predecessor) ──
    {
        "id": 22,
        "name": "刘永胜",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "离任（上一任满城区委书记）",
        "current_org": "未知",
        "source": "https://zh.wikipedia.org/wiki/满城区",
    },
]

# ── ORGANIZATIONS ──
organizations = [
    {
        "id": 1,
        "name": "中共保定市满城区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共保定市委员会",
        "location": "保定市满城区",
    },
    {
        "id": 2,
        "name": "保定市满城区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "保定市人民政府",
        "location": "保定市满城区",
    },
    {
        "id": 3,
        "name": "保定市满城区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "保定市人民代表大会常务委员会",
        "location": "保定市满城区",
    },
    {
        "id": 4,
        "name": "中共保定市满城区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共保定市纪律检查委员会",
        "location": "保定市满城区",
    },
    {
        "id": 5,
        "name": "中共保定市满城区委员会组织部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共保定市满城区委员会",
        "location": "保定市满城区",
    },
    {
        "id": 6,
        "name": "中共保定市满城区委员会宣传部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共保定市满城区委员会",
        "location": "保定市满城区",
    },
    {
        "id": 7,
        "name": "中共保定市满城区委员会政法委员会",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共保定市满城区委员会",
        "location": "保定市满城区",
    },
    {
        "id": 8,
        "name": "中共保定市满城区委员会统战部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共保定市满城区委员会",
        "location": "保定市满城区",
    },
    {
        "id": 9,
        "name": "中共保定市满城区委员会办公室",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共保定市满城区委员会",
        "location": "保定市满城区",
    },
    {
        "id": 10,
        "name": "保定市满城区人民武装部",
        "type": "政府",
        "level": "县处级",
        "parent": "保定军分区",
        "location": "保定市满城区",
    },
    {
        "id": 11,
        "name": "中国人民政治协商会议保定市满城区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "中国人民政治协商会议保定市委员会",
        "location": "保定市满城区",
    },
    {
        "id": 12,
        "name": "保定市满城区人民法院",
        "type": "事业单位",
        "level": "县处级",
        "parent": "保定市中级人民法院",
        "location": "保定市满城区",
    },
    {
        "id": 13,
        "name": "保定市满城区人民检察院",
        "type": "事业单位",
        "level": "县处级",
        "parent": "保定市人民检察院",
        "location": "保定市满城区",
    },
]

# ── POSITIONS (current roles) ──
positions = [
    # 刘玉辉
    {"person_id": 1, "org_id": 1, "title": "保定市满城区委书记", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "当前区委书记，来源：满城区政府官网新闻确认"},
    # 田松
    {"person_id": 2, "org_id": 1, "title": "保定市满城区委副书记", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "区委副书记"},
    {"person_id": 2, "org_id": 2, "title": "保定市满城区人民政府区长", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "区政府主要负责人"},
    # 屈会东
    {"person_id": 3, "org_id": 1, "title": "保定市满城区委副书记", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "区委副书记"},
    # 史宏昌
    {"person_id": 4, "org_id": 3, "title": "保定市满城区人大常委会主任", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "区人大常委会主任"},
    # 徐润雨
    {"person_id": 5, "org_id": 4, "title": "保定市满城区委常委、纪委书记", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "区纪委书记"},
    {"person_id": 5, "org_id": 1, "title": "保定市满城区委常委", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "区委常委"},
    # 牛海利
    {"person_id": 6, "org_id": 5, "title": "保定市满城区委常委、组织部部长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "组织部长"},
    {"person_id": 6, "org_id": 1, "title": "保定市满城区委常委", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "区委常委"},
    # 吕振
    {"person_id": 7, "org_id": 2, "title": "保定市满城区人民政府副区长（常务）", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "常务副区长"},
    {"person_id": 7, "org_id": 1, "title": "保定市满城区委常委", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "区委常委"},
    # 赵英晓
    {"person_id": 8, "org_id": 6, "title": "保定市满城区委常委、宣传部部长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "宣传部长"},
    {"person_id": 8, "org_id": 1, "title": "保定市满城区委常委", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "区委常委"},
    # 甄泳亮
    {"person_id": 9, "org_id": 7, "title": "保定市满城区委常委、政法委书记", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "政法委书记"},
    {"person_id": 9, "org_id": 1, "title": "保定市满城区委常委", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "区委常委"},
    # 赵丽娜
    {"person_id": 10, "org_id": 8, "title": "保定市满城区委常委、统战部部长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "统战部长"},
    {"person_id": 10, "org_id": 1, "title": "保定市满城区委常委", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "区委常委"},
    # 任沛显
    {"person_id": 11, "org_id": 9, "title": "保定市满城区委常委、区委办公室主任", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "区委办主任"},
    {"person_id": 11, "org_id": 1, "title": "保定市满城区委常委", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "区委常委"},
    # 马榕徽
    {"person_id": 12, "org_id": 10, "title": "保定市满城区人武部（区委常委）", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "人武部"},
    {"person_id": 12, "org_id": 1, "title": "保定市满城区委常委", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "区委常委"},
    # 刘建凯
    {"person_id": 13, "org_id": 2, "title": "保定市满城区人民政府副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "副区长"},
    # 刘严冰
    {"person_id": 14, "org_id": 2, "title": "保定市满城区人民政府副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "副区长"},
    # 郝硕
    {"person_id": 15, "org_id": 2, "title": "保定市满城区人民政府副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "副区长"},
    # 梁民
    {"person_id": 16, "org_id": 2, "title": "保定市满城区人民政府副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "副区长"},
    # 冉永占
    {"person_id": 17, "org_id": 2, "title": "保定市满城区人民政府副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "副区长"},
    # 钱国伟
    {"person_id": 18, "org_id": 11, "title": "保定市满城区政协党组书记", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "区政协党组书记"},
    # 连冬红
    {"person_id": 19, "org_id": 3, "title": "保定市满城区人大常委会副主任", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "区人大副主任"},
    # 张桂霞
    {"person_id": 20, "org_id": 12, "title": "保定市满城区人民法院院长", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "法院院长"},
    # 李迎初
    {"person_id": 21, "org_id": 13, "title": "保定市满城区人民检察院检察长", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "检察院检察长"},
    # 刘永胜（前任）
    {"person_id": 22, "org_id": 1, "title": "保定市满城区委书记（前任）", "start_date": "待查", "end_date": "待查", "rank": "正处级", "note": "前任区委书记，任期不详；来源：维基百科满城区词条"},
]

# ── RELATIONSHIPS ──
relationships = [
    # 书记-区长（党委和政府主要领导）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区委书记与区长：党委和政府主要领导工作关系", "overlap_org": "中共保定市满城区委员会", "overlap_period": "共同任职期间"},
    # 书记-副书记（党委内部）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区委书记与区委副书记：党委核心班子成员", "overlap_org": "中共保定市满城区委员会", "overlap_period": "共同任职期间"},
    # 区长-常务副区长
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "区长与常务副区长：政府班子正副职关系", "overlap_org": "保定市满城区人民政府", "overlap_period": "共同任职期间"},
    # 书记-纪委书记（监督关系）
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "区委书记与纪委书记：党委领导下的监督关系", "overlap_org": "中共保定市满城区委员会", "overlap_period": "共同任职期间"},
    # 书记-组织部长
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "区委书记与组织部部长：党委组织人事工作关系", "overlap_org": "中共保定市满城区委员会", "overlap_period": "共同任职期间"},
    # 前任-现任区委书记
    {"person_a": 22, "person_b": 1, "type": "predecessor_successor", "context": "前任区委书记与现任区委书记：职务交接关系", "overlap_org": "中共保定市满城区委员会", "overlap_period": "交接过渡期"},
]

# ── BUILD ──
def main():
    # When run from staging, derive paths relative to script location
    staging_dir = os.path.dirname(os.path.abspath(__file__))

    global DB_PATH, GEXF_PATH
    DB_PATH = os.path.join(staging_dir, "满城区_network.db")
    GEXF_PATH = os.path.join(staging_dir, "满城区_network.gexf")

    run_build(
        slug="满城区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Also write person JSON files
    write_person_json(staging_dir)

    print(f"Build complete. DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"Person JSONs in: {staging_dir}")


def write_person_json(staging_dir: str):
    """Write person graph JSON files into staging dir."""
    for person in persons:
        pid = person["id"]
        name = person["name"]

        # Only write JSON for core figures (区委书记 and 区长)
        if pid not in (1, 2):
            continue

        job_slug = "区委书记" if pid == 1 else "区长"

        filename = f"{AS_OF}-河北省-保定市-{job_slug}-{name}.json"

        person_json = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河北省",
                "city": "保定市",
                "region": "满城区",
                "job": job_slug,
                "task_id": "hebei_满城区",
                "time_focus": "当前任职",
            },
            "identity": {
                "person_id": f"hebei_baoding_mancheng_{name}_{pid}",
                "name": name,
                "aliases": [],
                "gender": person.get("gender", ""),
                "ethnicity": person.get("ethnicity", ""),
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "",
                    "name_birthplace": "",
                    "official_profile_url": "http://www.mancheng.gov.cn/",
                },
            },
            "current_status": {
                "current_post": person.get("current_post", ""),
                "current_org": person.get("current_org", ""),
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"],
            },
            "career_timeline": [
                {
                    "start": "待查",
                    "end": "present",
                    "org": "中共保定市满城区委员会" if pid == 1 else "保定市满城区人民政府",
                    "title": person.get("current_post", ""),
                    "level": "县处级",
                    "location": "保定市满城区",
                    "system": "party" if pid == 1 else "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "当前任职（满城区第四次党代会后），确认来源：满城区政府官网新闻",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S002"],
                }
            ],
            "organizations": [
                {"org_id": 1, "name": "中共保定市满城区委员会", "type": "党委", "level": "县处级"},
                {"org_id": 2, "name": "保定市满城区人民政府", "type": "政府", "level": "县处级"},
            ],
            "relationships": [
                {
                    "person": "田松" if pid == 1 else "刘玉辉",
                    "person_id": f"hebei_baoding_mancheng_{'田松' if pid == 1 else '刘玉辉'}_{2 if pid == 1 else 1}",
                    "relationship_type": "superior_subordinate",
                    "strength": "strong",
                    "evidence": "区委书记与区长，党委和政府主要领导工作关系",
                    "overlap_org": "中共保定市满城区委员会",
                    "overlap_period": "共同任职期间",
                    "direction": "person_to_other" if pid == 1 else "other_to_person",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                }
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "公开资料不足，无法判断", "notable_fast_promotions": []},
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "当前公开资料不足，无法推断工作风格和个性特征。",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "目前未发现公开的纪律处分、审计问题或负面媒体报道",
                    "date": "",
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "source_register": [
                {
                    "id": "S001",
                    "title": "保定市满城区人民政府门户网站-领导之窗",
                    "url": "http://www.mancheng.gov.cn/list-ldzc.html",
                    "publisher": "保定市满城区人民政府",
                    "published_at": "",
                    "accessed_at": AS_OF,
                    "source_type": "official",
                    "reliability": "high",
                    "notes": "政府官网新闻和大会报道确认区委书记和区长姓名",
                },
                {
                    "id": "S002",
                    "title": "中国共产党保定市满城区第四次代表大会闭幕",
                    "url": "http://www.mancheng.gov.cn/show-13860.html",
                    "publisher": "满城区融媒体中心",
                    "published_at": "2026-07-21",
                    "accessed_at": AS_OF,
                    "source_type": "official",
                    "reliability": "high",
                    "notes": "区第四次党代会选举产生新一届区委领导班子",
                },
            ],
            "confidence_summary": {
                "identity": "plausible",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": f"缺乏详细履历：{name}的出生年月、籍贯、教育背景、工作经历、任现职时间均不详",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": f"{name}的完整履历（出生年月、籍贯、教育背景、工作经历）",
                    "why_it_matters": "关系网络分析的核心信息",
                    "suggested_queries": [
                        f"{name} 简历 保定 满城区",
                        f"{name} 任前公示 保定",
                        f"{name} 百度百科",
                    ],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": f"{name}的任现职时间",
                    "why_it_matters": "确定领导班子的共同工作时间起点",
                    "suggested_queries": [
                        f"满城区 人大 任命 {name} 区长" if pid == 2 else f"保定市委 任命 {name} 区委书记",
                        f"{name} 任职 满城区",
                    ],
                    "last_attempted": AS_OF,
                },
            ],
        }

        filepath = os.path.join(staging_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(person_json, f, ensure_ascii=False, indent=2)
        print(f"Person JSON written: {filepath}")


if __name__ == "__main__":
    main()
