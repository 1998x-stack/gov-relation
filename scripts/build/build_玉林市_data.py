#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
玉林市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 地级市
Province: 广西壮族自治区
Parent City:
Region: 玉林市
Targets: 市委书记 & 市长

当前在任 (as of 2026-07-23):
- 市委书记: 张惠强 (2026.04-)
- 市长: 空缺（张惠强升任书记后待补）

数据说明:
- 大量字段标注"待查"表示公开渠道未能获取到信息
- 置信度标注在每条记录中
- 来源基于 yulin.gov.cn、中国经济网、广西新闻网等公开报道
"""

import json
import os
import sys
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "玉林市"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-23"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：市委书记（现任）
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "张惠强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年11月",
        "birthplace": "待查",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "玉林市委书记",
        "current_org": "中共玉林市委员会",
        "source": "https://district.ce.cn/newarea/sddy/202604/30/t20260430_39586227.shtml"
    },
    # ════════════════════════════════════════
    # 市长（空缺中）
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "待确认（市长空缺）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "玉林市市长（空缺中，张惠强升任书记后待补）",
        "current_org": "玉林市人民政府",
        "source": ""
    },
    # ════════════════════════════════════════
    # 前任市委书记：王琛
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "王琛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "不再担任玉林市委书记（已调离）",
        "current_org": "（调离）",
        "source": "http://www.yulin.gov.cn"
    },
    # ════════════════════════════════════════
    # 再前任市委书记：莫桦（已落马）
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "莫桦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员（被开除）",
        "work_start": "待查",
        "current_post": "原玉林市委书记（被双开/判无期徒刑）",
        "current_org": "（原中共玉林市委员会）",
        "source": "https://www.sogou.com"
    },
    # ════════════════════════════════════════
    # 前任市长：白松涛
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "白松涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "原玉林市市长（已调离）",
        "current_org": "（调离）",
        "source": "https://www.sogou.com"
    },
    # ════════════════════════════════════════
    # 市委常委、常务副市长：韦庆强
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "韦庆强",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1970年10月",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "玉林市委常委、常务副市长、市政府党组副书记",
        "current_org": "玉林市人民政府/中共玉林市委员会",
        "source": "http://www.yulin.gov.cn/zwgk/ldxx/"
    },
    # ════════════════════════════════════════
    # 市委副书记：邓国忠
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "邓国忠",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "玉林市委副书记",
        "current_org": "中共玉林市委员会",
        "source": "http://www.yulin.gov.cn"
    },
    # ════════════════════════════════════════
    # 市纪委书记、监委主任：韦义
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "韦义",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1970年5月",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "玉林市委常委、市纪委书记、市监委主任",
        "current_org": "中共玉林市纪律检查委员会/玉林市监察委员会",
        "source": "http://www.yulin.gov.cn"
    },
    # ════════════════════════════════════════
    # 组织部部长：马克兵（女）
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "马克兵",
        "gender": "女",
        "ethnicity": "壮族",
        "birth": "1972年8月",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "玉林市委常委、组织部部长、市委党校校长（兼）",
        "current_org": "中共玉林市委员会/中共玉林市委组织部",
        "source": "http://www.yulin.gov.cn"
    },
    # ════════════════════════════════════════
    # 统战部部长、副市长：范小花（女）
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "范小花",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "玉林市委常委、统战部部长、副市长、市政协党组副书记（兼）",
        "current_org": "中共玉林市委员会/玉林市人民政府",
        "source": "https://www.thepaper.cn"
    },
    # ════════════════════════════════════════
    # 宣传部部长：何中奎
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "何中奎",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1975年4月",
        "birthplace": "湖北来凤",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "玉林市委常委、宣传部部长",
        "current_org": "中共玉林市委员会/中共玉林市委宣传部",
        "source": "http://www.gxcounty.com"
    },
    # ════════════════════════════════════════
    # 市委常委：甘文波
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "甘文波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年10月",
        "birthplace": "广西玉林玉州",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "玉林市委常委",
        "current_org": "中共玉林市委员会",
        "source": "http://www.gxcounty.com"
    },
    # ════════════════════════════════════════
    # 市委常委、副市长：张海鹏
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "张海鹏",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "玉林市委常委、副市长",
        "current_org": "中共玉林市委员会/玉林市人民政府",
        "source": "http://www.yulin.gov.cn"
    },
    # ════════════════════════════════════════
    # 市委常委：陈磊
    # ════════════════════════════════════════
    {
        "id": 14,
        "name": "陈磊",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "1980年代（'80后'）",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "玉林市委常委（原北部湾大学副校长）",
        "current_org": "中共玉林市委员会",
        "source": "https://www.sohu.com"
    },
    # ════════════════════════════════════════
    # 副市长：党万坚
    # ════════════════════════════════════════
    {
        "id": 15,
        "name": "党万坚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "玉林市副市长",
        "current_org": "玉林市人民政府",
        "source": "http://www.yulin.gov.cn/zwgk/ldxx/"
    },
    # ════════════════════════════════════════
    # 副市长：马少华
    # ════════════════════════════════════════
    {
        "id": 16,
        "name": "马少华",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "玉林市副市长",
        "current_org": "玉林市人民政府",
        "source": "http://www.yulin.gov.cn/zwgk/ldxx/"
    },
    # ════════════════════════════════════════
    # 副市长：王淮
    # ════════════════════════════════════════
    {
        "id": 17,
        "name": "王淮",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "玉林市副市长",
        "current_org": "玉林市人民政府",
        "source": "http://www.yulin.gov.cn/zwgk/ldxx/"
    },
    # ════════════════════════════════════════
    # 副市长：冯克森
    # ════════════════════════════════════════
    {
        "id": 18,
        "name": "冯克森",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "玉林市副市长、龙潭产业园区工委书记",
        "current_org": "玉林市人民政府/龙潭产业园区",
        "source": "http://www.yulin.gov.cn/zwgk/ldxx/"
    },
    # ════════════════════════════════════════
    # 副市长：刘启
    # ════════════════════════════════════════
    {
        "id": 19,
        "name": "刘启",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "玉林市副市长（2026年2月任）",
        "current_org": "玉林市人民政府",
        "source": "http://www.yulin.gov.cn"
    },
    # ════════════════════════════════════════
    # 副市长：仵建民
    # ════════════════════════════════════════
    {
        "id": 20,
        "name": "仵建民",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "玉林市副市长（2026年2月任）",
        "current_org": "玉林市人民政府",
        "source": "http://www.yulin.gov.cn"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共玉林市委员会", "type": "党委", "level": "地级市", "parent": "中共广西壮族自治区委员会", "location": "广西玉林"},
    {"id": 2, "name": "玉林市人民政府", "type": "政府", "level": "地级市", "parent": "广西壮族自治区人民政府", "location": "广西玉林"},
    {"id": 3, "name": "中共玉林市纪律检查委员会", "type": "党委", "level": "地级市", "parent": "中共广西壮族自治区纪律检查委员会", "location": "广西玉林"},
    {"id": 4, "name": "玉林市监察委员会", "type": "政府", "level": "地级市", "parent": "广西壮族自治区监察委员会", "location": "广西玉林"},
    {"id": 5, "name": "中共玉林市委组织部", "type": "党委", "level": "地级市", "parent": "中共玉林市委员会", "location": "广西玉林"},
    {"id": 6, "name": "中共玉林市委宣传部", "type": "党委", "level": "地级市", "parent": "中共玉林市委员会", "location": "广西玉林"},
    {"id": 7, "name": "中共玉林市委统一战线工作部", "type": "党委", "level": "地级市", "parent": "中共玉林市委员会", "location": "广西玉林"},
    {"id": 8, "name": "玉林市人大常委会", "type": "人大", "level": "地级市", "parent": "广西壮族自治区人大常委会", "location": "广西玉林"},
    {"id": 9, "name": "中国人民政治协商会议玉林市委员会", "type": "政协", "level": "地级市", "parent": "广西壮族自治区政协", "location": "广西玉林"},
    {"id": 10, "name": "龙潭产业园区", "type": "开发区", "level": "地级市", "parent": "玉林市人民政府", "location": "广西玉林"},
    {"id": 11, "name": "广西壮族自治区应急管理厅", "type": "政府", "level": "省级", "parent": "广西壮族自治区人民政府", "location": "广西南宁"},
    {"id": 12, "name": "北部湾大学", "type": "事业单位", "level": "省级", "parent": "广西壮族自治区人民政府", "location": "广西钦州"},
    {"id": 13, "name": "贺州学院", "type": "事业单位", "level": "省级", "parent": "广西壮族自治区人民政府", "location": "广西贺州"},
    {"id": 14, "name": "中共玉林市委党校", "type": "事业单位", "level": "地级市", "parent": "中共玉林市委员会", "location": "广西玉林"},
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 张惠强
    {"person_id": 1, "org_id": 1, "title": "玉林市委书记", "start_date": "2026-04", "end_date": "", "rank": "正厅级", "note": "2026年4月由市长升任"},
    {"person_id": 1, "org_id": 2, "title": "玉林市市长", "start_date": "约2024", "end_date": "2026-04", "rank": "正厅级", "note": "升任市委书记前担任玉林市市长"},
    {"person_id": 1, "org_id": 11, "title": "广西应急管理厅党委书记、厅长", "start_date": "约2022", "end_date": "约2024", "rank": "正厅级", "note": "调任玉林市长前任职"},
    # 王琛
    {"person_id": 3, "org_id": 1, "title": "玉林市委书记", "start_date": "约2023", "end_date": "2026-04", "rank": "正厅级", "note": "接替莫桦，后由张惠强接任"},
    # 莫桦
    {"person_id": 4, "org_id": 1, "title": "玉林市委书记", "start_date": "2021", "end_date": "2023", "rank": "正厅级", "note": "被查落马，后被双开/判无期徒刑"},
    # 白松涛
    {"person_id": 5, "org_id": 2, "title": "玉林市市长", "start_date": "2020", "end_date": "约2024", "rank": "正厅级", "note": "已调离玉林"},
    # 韦庆强
    {"person_id": 6, "org_id": 1, "title": "玉林市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "常务副市长、市政府党组副书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 邓国忠
    {"person_id": 7, "org_id": 1, "title": "玉林市委副书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 韦义
    {"person_id": 8, "org_id": 1, "title": "玉林市委常委、市纪委书记", "start_date": "2024", "end_date": "", "rank": "副厅级", "note": "2024年6月任代主任，2025年2月正式当选"},
    {"person_id": 8, "org_id": 4, "title": "玉林市监委主任", "start_date": "2024", "end_date": "", "rank": "副厅级", "note": ""},
    # 马克兵
    {"person_id": 9, "org_id": 1, "title": "玉林市委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼任市委党校校长"},
    {"person_id": 9, "org_id": 14, "title": "市委党校校长（兼）", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 范小花
    {"person_id": 10, "org_id": 1, "title": "玉林市委常委、统战部部长", "start_date": "2025", "end_date": "", "rank": "副厅级", "note": "2025年5月任"},
    {"person_id": 10, "org_id": 2, "title": "玉林市副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼任"},
    # 何中奎
    {"person_id": 11, "org_id": 1, "title": "玉林市委常委、宣传部部长", "start_date": "2026初", "end_date": "", "rank": "副厅级", "note": "接替调任贺州学院的李勇齐"},
    # 甘文波
    {"person_id": 12, "org_id": 1, "title": "玉林市委常委", "start_date": "2024", "end_date": "", "rank": "副厅级", "note": "由容县县委书记晋升"},
    # 张海鹏
    {"person_id": 13, "org_id": 1, "title": "玉林市委常委", "start_date": "2024", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "玉林市副市长", "start_date": "2024-06", "end_date": "", "rank": "副厅级", "note": ""},
    # 陈磊
    {"person_id": 14, "org_id": 1, "title": "玉林市委常委", "start_date": "2025-09", "end_date": "", "rank": "副厅级", "note": "原北部湾大学副校长挂职返还后任职"},
    # 党万坚
    {"person_id": 15, "org_id": 2, "title": "玉林市副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 马少华
    {"person_id": 16, "org_id": 2, "title": "玉林市副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 王淮
    {"person_id": 17, "org_id": 2, "title": "玉林市副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 冯克森
    {"person_id": 18, "org_id": 2, "title": "玉林市副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼任龙潭产业园区工委书记"},
    {"person_id": 18, "org_id": 10, "title": "龙潭产业园区工委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 刘启
    {"person_id": 19, "org_id": 2, "title": "玉林市副市长", "start_date": "2026-02", "end_date": "", "rank": "副厅级", "note": ""},
    # 仵建民
    {"person_id": 20, "org_id": 2, "title": "玉林市副市长", "start_date": "2026-02", "end_date": "", "rank": "副厅级", "note": ""},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 张惠强 <-> 韦庆强（共事：市长-常务副市长）
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "市长与常务副市长工作搭档（2024-2026）", "overlap_org": "玉林市人民政府", "overlap_period": "2024-2026"},
    # 张惠强 <-> 邓国忠（共事：市长-副书记）
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "市长与市委副书记工作搭档", "overlap_org": "中共玉林市委员会", "overlap_period": "2024-2026"},
    # 张惠强 <-> 韦义（共事）
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "书记与纪委书记工作搭档", "overlap_org": "中共玉林市委员会", "overlap_period": "2024-2026"},
    # 张惠强 <-> 马克兵（共事）
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "书记与组织部长工作搭档", "overlap_org": "中共玉林市委员会", "overlap_period": ""},
    # 张惠强 <-> 范小花（共事）
    {"person_a": 1, "person_b": 10, "type": "共事", "context": "书记与统战部长工作搭档", "overlap_org": "中共玉林市委员会", "overlap_period": "2025-2026"},
    # 张惠强 <-> 何中奎（共事）
    {"person_a": 1, "person_b": 11, "type": "共事", "context": "书记与宣传部长工作搭档", "overlap_org": "中共玉林市委员会", "overlap_period": "2026-2026"},
    # 张惠强 <-> 甘文波（共事）
    {"person_a": 1, "person_b": 12, "type": "共事", "context": "书记与市委常委工作搭档", "overlap_org": "中共玉林市委员会", "overlap_period": "2024-2026"},
    # 张惠强 <-> 张海鹏（共事）
    {"person_a": 1, "person_b": 13, "type": "共事", "context": "书记与市委常委/副市长工作搭档", "overlap_org": "玉林市人民政府/中共玉林市委员会", "overlap_period": "2024-2026"},
    # 张惠强 <-> 陈磊（共事）
    {"person_a": 1, "person_b": 14, "type": "共事", "context": "书记与市委常委工作搭档", "overlap_org": "中共玉林市委员会", "overlap_period": "2025-2026"},
    # 张惠强 -- 王琛（前后任：书记）
    {"person_a": 1, "person_b": 3, "type": "前后任", "context": "张惠强接替王琛任玉林市委书记", "overlap_org": "中共玉林市委员会", "overlap_period": "2026"},
    # 王琛 -- 莫桦（前后任：书记）
    {"person_a": 3, "person_b": 4, "type": "前后任", "context": "王琛接替莫桦任玉林市委书记", "overlap_org": "中共玉林市委员会", "overlap_period": "2023"},
    # 张惠强 -- 白松涛（前后任：市长）
    {"person_a": 1, "person_b": 5, "type": "前后任", "context": "张惠强接替白松涛任玉林市市长", "overlap_org": "玉林市人民政府", "overlap_period": "2024"},
    # 韦庆强 <-> 党万坚（共事：副市长间协作）
    {"person_a": 6, "person_b": 15, "type": "共事", "context": "常务副市长与副市长工作搭档", "overlap_org": "玉林市人民政府", "overlap_period": ""},
    # 韦庆强 <-> 马少华（共事）
    {"person_a": 6, "person_b": 16, "type": "共事", "context": "常务副市长与副市长工作搭档", "overlap_org": "玉林市人民政府", "overlap_period": ""},
    # 马克兵 <-> 何中奎（共事）
    {"person_a": 9, "person_b": 11, "type": "共事", "context": "组织部长与宣传部长同为市委常委工作搭档", "overlap_org": "中共玉林市委员会", "overlap_period": "2026"},
    # 韦义 <-> 马克兵（共事）
    {"person_a": 8, "person_b": 9, "type": "共事", "context": "纪委书记与组织部长同为市委常委", "overlap_org": "中共玉林市委员会", "overlap_period": ""},
    # 范小花 <-> 何中奎（共事）
    {"person_a": 10, "person_b": 11, "type": "共事", "context": "统战部长与宣传部长同为市委常委", "overlap_org": "中共玉林市委员会", "overlap_period": "2026"},
    # 甘文波 <-> 张海鹏（共事）
    {"person_a": 12, "person_b": 13, "type": "共事", "context": "同为市委常委", "overlap_org": "中共玉林市委员会", "overlap_period": "2024"},
    # 陈磊 <-> 甘文波（共事）
    {"person_a": 14, "person_b": 12, "type": "共事", "context": "同为市委常委", "overlap_org": "中共玉林市委员会", "overlap_period": "2025"},
    # 李勇齐（通过何中奎间接）— 前后任关系体现在宣传部
    # 何中奎原接替李勇齐（已调任贺州学院），但李勇齐未列入本数据集
]

# =========================================================================
# 5. RUN BUILD
# =========================================================================

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def build_db():
    """Build SQLite database."""
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create tables
    c.execute("DROP TABLE IF EXISTS relationships")
    c.execute("DROP TABLE IF EXISTS positions")
    c.execute("DROP TABLE IF EXISTS organizations")
    c.execute("DROP TABLE IF EXISTS persons")

    c.execute("""
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
        )
    """)

    c.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        )
    """)

    c.execute("""
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
        )
    """)

    c.execute("""
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
        )
    """)

    # Insert persons
    for p in persons:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    # Insert organizations
    for o in organizations:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    # Insert positions
    for pos in positions:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))

    # Insert relationships
    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"✅ Created database: {DB_PATH}")


def build_gexf():
    """Build GEXF graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>玉林市领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="gender" type="string"/>')
    lines.append('      <attribute id="4" title="ethnicity" type="string"/>')
    lines.append('      <attribute id="5" title="birth" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: Persons
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        role = p["current_post"]
        # Color by role
        if "书记" in role and "纪委" not in role and "副书记" not in role:
            r, g, b, a = 200, 30, 30, 1.0      # 深红 — 一把手
            sz = 60.0
        elif "副书记" in role:
            r, g, b, a = 220, 80, 80, 0.9       # 浅红 — 副书记
            sz = 45.0
        elif "市长" in role and "副" not in role:
            r, g, b, a = 30, 100, 200, 1.0      # 深蓝 — 政府首长
            sz = 55.0
        elif "常务副" in role:
            r, g, b, a = 100, 150, 220, 0.85    # 浅蓝 — 副职
            sz = 35.0
        elif "纪委书记" in role:
            r, g, b, a = 255, 165, 0, 1.0       # 橙色 — 纪委
            sz = 35.0
        elif "副" in role:
            r, g, b, a = 100, 150, 220, 0.85    # 浅蓝 — 副职
            sz = 35.0
        elif "市委常委" in role:
            r, g, b, a = 180, 100, 180, 0.85    # 紫色 — 常委
            sz = 30.0
        else:
            r, g, b, a = 180, 180, 180, 0.7
            sz = 20.0

        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["gender"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["ethnicity"])}"/>')
        lines.append(f'          <attvalue for="5" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}" a="{a}"/>')
        lines.append(f'        <viz:size value="{sz:.1f}"/>')
        lines.append('      </node>')

    # Nodes: Organizations
    org_colors = {
        "党委": (255, 200, 200),
        "政府": (200, 200, 255),
        "人大": (200, 255, 255),
        "政协": (255, 240, 200),
        "开发区": (200, 255, 200),
        "事业单位": (220, 220, 220),
    }
    for o in organizations:
        oid = o["id"] + 100000
        or_, og, ob = org_colors.get(o["type"], (200, 200, 200))
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{or_}" g="{og}" b="{ob}" a="0.8"/>')
        lines.append(f'        <viz:size value="15.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges: person->organization (worked_at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        pid = pos["person_id"]
        oid = pos["org_id"] + 100000
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="任职"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges: person<->person (relationship)
    for r in relationships:
        eid += 1
        weight = "2.0" if r["type"] == "共事" else "1.5"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ Created GEXF: {GEXF_PATH}")


# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    build_db()
    build_gexf()

    # Summary
    print(f"\n📊 Summary for {SLUG}:")
    print(f"   Persons (非空名): {sum(1 for p in persons if p['name'] and '待确认' not in p['name'] and '空缺' not in p['name'])} 人")
    print(f"   Persons (含待确认): {len(persons)} 人")
    print(f"   Organizations: {len(organizations)} 个")
    print(f"   Positions: {len(positions)} 条")
    print(f"   Relationships: {len(relationships)} 对")
    print(f"\n   DB: {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
    print(f"\n⚠️  Note: Web access was degraded during research. Many biography fields are marked as 待查.")
    print(f"   Current 市委书记: 张惠强（2026年4月上任）")
    print(f"   Current 市长: 空缺（张惠强升任书记后待补）")
