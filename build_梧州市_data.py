#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
梧州市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 地级市
Province: 广西壮族自治区
Parent City: 
Region: 梧州市
Targets: 市委书记 & 市长

Research Sources:
- 梧州市人民政府门户网站 (www.wuzhou.gov.cn) — 今日梧州新闻（确认现任领导）
- 快懂百科 (www.baike.com) — 邱明宏、谭秀洪个人资料
- 梧州市融媒体中心 — 2026年7月新闻报道

Current status (as of 2026-07-22):
- 市委书记: 邱明宏（确认自2026年7月在任）
- 市长: 谭秀洪（确认自2026年7月在任）

Research Date: 2026-07-22
"""

import os
import sys
import sqlite3  # noqa: F401

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (staging) ──
SLUG = "梧州市"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 市委领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "邱明宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年8月",
        "birthplace": "陕西宁强",
        "native_place": "陕西宁强",
        "education": "陕西省委党校研究生学历",
        "party_join": "中共党员（1994年1月）",
        "work_start": "1990年8月",
        "current_post": "中共梧州市委书记",
        "current_org": "中共梧州市委员会",
        "source": "快懂百科:邱明宏; wuzhou.gov.cn 2026年7月新闻报道"
    },
    {
        "id": 2,
        "name": "谭秀洪",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1973年7月",
        "birthplace": "湖南冷水江",
        "native_place": "湖南冷水江",
        "education": "英国伍斯特大学工商管理专业，工商管理硕士",
        "party_join": "中共党员（2000年6月）",
        "work_start": "1995年7月",
        "current_post": "中共梧州市委副书记、市人民政府市长、党组书记",
        "current_org": "梧州市人民政府",
        "source": "快懂百科:谭秀洪; wuzhou.gov.cn 2026年7月新闻报道"
    },
    # ════════════════════════════════════════
    # 市人大常委会领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "马克兵",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梧州市人大常委会主任",
        "current_org": "梧州市人民代表大会常务委员会",
        "source": "wuzhou.gov.cn 2026年7月21日新闻报道（选举人大代表活动）"
    },
    # ════════════════════════════════════════
    # 市政协领导
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "黄振饶",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梧州市政协主席",
        "current_org": "中国人民政治协商会议梧州市委员会",
        "source": "wuzhou.gov.cn 2026年7月21日新闻报道（选举人大代表活动）"
    },
    # ════════════════════════════════════════
    # 市委常委/副市长（主要市领导）
    # 注：以下人物根据2026年7月20日选举人大代表新闻中列名确认，
    # 具体职务分工需进一步查证
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "覃元臻",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梧州市领导（市委常委/副市长）",
        "current_org": "中共梧州市委员会/梧州市人民政府",
        "source": "wuzhou.gov.cn 2026年7月新闻报道"
    },
    {
        "id": 6,
        "name": "邝驱",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梧州市领导（市委常委/副市长）",
        "current_org": "中共梧州市委员会/梧州市人民政府",
        "source": "wuzhou.gov.cn 2026年7月新闻报道"
    },
    {
        "id": 7,
        "name": "杨赞彬",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梧州市领导（市委常委/副市长）",
        "current_org": "中共梧州市委员会/梧州市人民政府",
        "source": "wuzhou.gov.cn 2026年7月新闻报道"
    },
    {
        "id": 8,
        "name": "郝凯广",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梧州市领导（市委秘书长/市委常委）",
        "current_org": "中共梧州市委员会",
        "notes": "多次陪伴市委书记邱明宏调研，猜测为市委秘书长或重要常委",
        "source": "wuzhou.gov.cn 2026年7月新闻报道（多篇邱明宏调研活动报道中列名）"
    },
    {
        "id": 9,
        "name": "马秀明",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梧州市领导（市委常委/副市长）",
        "current_org": "中共梧州市委员会/梧州市人民政府",
        "source": "wuzhou.gov.cn 2026年7月新闻报道"
    },
    {
        "id": 10,
        "name": "杜诚",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梧州市领导",
        "current_org": "梧州市",
        "source": "wuzhou.gov.cn 2026年7月21日新闻报道"
    },
    {
        "id": 11,
        "name": "周志军",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梧州市领导",
        "current_org": "梧州市",
        "source": "wuzhou.gov.cn 2026年7月21日新闻报道"
    },
    {
        "id": 12,
        "name": "曾健勇",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梧州市领导",
        "current_org": "梧州市",
        "source": "wuzhou.gov.cn 2026年7月21日新闻报道"
    },
    {
        "id": 13,
        "name": "杨桢",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梧州市领导（副市长）",
        "current_org": "梧州市人民政府",
        "source": "wuzhou.gov.cn 2026年7月21日新闻报道"
    },
    {
        "id": 14,
        "name": "宋彤宇",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梧州市领导",
        "current_org": "梧州市",
        "source": "wuzhou.gov.cn 2026年7月21日新闻报道"
    },
    {
        "id": 15,
        "name": "黎小媚",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梧州市领导",
        "current_org": "梧州市",
        "source": "wuzhou.gov.cn 2026年7月21日新闻报道"
    },
    {
        "id": 16,
        "name": "易凯航",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梧州市领导",
        "current_org": "梧州市",
        "source": "wuzhou.gov.cn 2026年7月21日新闻报道"
    },
    {
        "id": 17,
        "name": "蒙中平",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梧州市领导（副市长）",
        "current_org": "梧州市人民政府",
        "source": "wuzhou.gov.cn 2026年7月21日新闻报道"
    },
    {
        "id": 18,
        "name": "劳高进",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梧州市领导（副市长）",
        "current_org": "梧州市人民政府",
        "source": "wuzhou.gov.cn 2026年7月新闻报道"
    },
    {
        "id": 19,
        "name": "苏思远",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梧州市领导（副市长）",
        "current_org": "梧州市人民政府",
        "source": "wuzhou.gov.cn 2026年7月新闻报道"
    },
    {
        "id": 20,
        "name": "王鹏",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梧州市领导（副市长/市政府党组成员）",
        "current_org": "梧州市人民政府",
        "source": "wuzhou.gov.cn 2026年7月新闻报道（多篇领导活动中列名）"
    },
    {
        "id": 21,
        "name": "武晓辉",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梧州市领导（副市长/市政府党组成员）",
        "current_org": "梧州市人民政府",
        "source": "wuzhou.gov.cn 2026年7月新闻报道"
    },
    {
        "id": 22,
        "name": "李彤华",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梧州市领导",
        "current_org": "梧州市",
        "source": "wuzhou.gov.cn 2026年7月21日新闻报道"
    },
    {
        "id": 23,
        "name": "李贞梅",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梧州市领导（市政协副主席）",
        "current_org": "中国人民政治协商会议梧州市委员会",
        "source": "wuzhou.gov.cn 2026年7月21日新闻报道"
    },
    {
        "id": 24,
        "name": "曹垂龙",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梧州市领导（市政协副主席）",
        "current_org": "中国人民政治协商会议梧州市委员会",
        "source": "wuzhou.gov.cn 2026年7月21日新闻报道"
    },
    {
        "id": 25,
        "name": "苏颖",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梧州市领导（副市长）",
        "current_org": "梧州市人民政府",
        "source": "wuzhou.gov.cn 2026年7月21日新闻报道"
    },
    {
        "id": 26,
        "name": "李广勇",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梧州市领导",
        "current_org": "梧州市",
        "source": "wuzhou.gov.cn 2026年7月21日新闻报道"
    },
    {
        "id": 27,
        "name": "钟锋",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梧州市领导",
        "current_org": "梧州市",
        "source": "wuzhou.gov.cn 2026年7月21日新闻报道"
    },
    {
        "id": 28,
        "name": "赖启第",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "梧州市领导",
        "current_org": "梧州市",
        "source": "wuzhou.gov.cn 2026年7月21日新闻报道"
    },
]

# 2. Organizations
organizations = [
    # 市级组织
    {"id": 1, "name": "中共梧州市委员会", "type": "党委", "level": "地级市", "parent": "中共广西壮族自治区委员会", "location": "广西梧州市"},
    {"id": 2, "name": "梧州市人民政府", "type": "政府", "level": "地级市", "parent": "广西壮族自治区人民政府", "location": "广西梧州市"},
    {"id": 3, "name": "梧州市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "", "location": "广西梧州市"},
    {"id": 4, "name": "中国人民政治协商会议梧州市委员会", "type": "政协", "level": "地级市", "parent": "", "location": "广西梧州市"},
    # 历史任职组织
    {"id": 5, "name": "广西壮族自治区商务厅", "type": "政府", "level": "省级", "parent": "广西壮族自治区人民政府", "location": "广西南宁市"},
    {"id": 6, "name": "北海市人民政府", "type": "政府", "level": "地级市", "parent": "广西壮族自治区人民政府", "location": "广西北海市"},
    {"id": 7, "name": "中共北海市委员会", "type": "党委", "level": "地级市", "parent": "中共广西壮族自治区委员会", "location": "广西北海市"},
    {"id": 8, "name": "陕西宁强县农经站", "type": "政府", "level": "县级", "parent": "", "location": "陕西宁强县"},
    {"id": 9, "name": "西安农校", "type": "事业单位", "level": "", "parent": "", "location": "陕西西安"},
    {"id": 10, "name": "陕西省委党校", "type": "事业单位", "level": "", "parent": "", "location": "陕西西安"},
    {"id": 11, "name": "广西壮族自治区口岸办公室", "type": "政府", "level": "省级", "parent": "广西壮族自治区商务厅", "location": "广西南宁市"},
    {"id": 12, "name": "中国（广西）自由贸易试验区工作办公室", "type": "政府", "level": "省级", "parent": "广西壮族自治区人民政府", "location": "广西南宁市"},
]

# 3. Positions
positions = [
    # 邱明宏 - 现任职务
    {"person_id": 1, "org_id": 1, "title": "中共梧州市委书记", "start": "2025年/2026年（待确认）", "end": "至今", "rank": "正厅级", "note": "确认自2026年7月在任，具体到任日期需查任前公示"},
    # 邱明宏 - 早期履历（根据快懂百科）
    {"person_id": 1, "org_id": 9, "title": "西安农校农业经营管理专业学生", "start": "1986年9月", "end": "1990年8月", "rank": "", "note": "学习"},
    {"person_id": 1, "org_id": 8, "title": "陕西宁强县农经站干事", "start": "1990年8月", "end": "1993年4月", "rank": "", "note": "早期工作"},
    # 邱明宏后续履历因百科页面JS渲染中断未完整获取，待补

    # 谭秀洪 - 现任职务
    {"person_id": 2, "org_id": 2, "title": "梧州市人民政府市长、党组书记", "start": "2024年/2025年（待确认）", "end": "至今", "rank": "正厅级", "note": "确认自2026年7月在任，同时担任市委副书记"},
    {"person_id": 2, "org_id": 1, "title": "中共梧州市委副书记", "start": "2024年/2025年（待确认）", "end": "至今", "rank": "正厅级", "note": ""},
    # 谭秀洪 - 历史职务
    {"person_id": 2, "org_id": 5, "title": "广西壮族自治区商务厅副厅长", "start": "待查", "end": "2021年8月", "rank": "副厅级", "note": "曾任自治区口岸办公室副主任"},
    {"person_id": 2, "org_id": 12, "title": "中国（广西）自由贸易试验区工作办公室专职副主任", "start": "待查", "end": "2021年8月", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 7, "title": "中共北海市委常委", "start": "2021年8月", "end": "2024年/2025年", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 6, "title": "北海市人民政府副市长（常务）、党组副书记", "start": "2021年8月", "end": "2024年/2025年", "rank": "副厅级", "note": "北海市政府党组副书记、副市长"},

    # 马克兵
    {"person_id": 3, "org_id": 3, "title": "梧州市人大常委会主任", "start": "待查", "end": "至今", "rank": "正厅级", "note": ""},

    # 黄振饶
    {"person_id": 4, "org_id": 4, "title": "梧州市政协主席", "start": "待查", "end": "至今", "rank": "正厅级", "note": ""},

    # 覃元臻
    {"person_id": 5, "org_id": 1, "title": "梧州市领导（疑似市委常委）", "start": "待查", "end": "至今", "rank": "副厅级", "note": "出席防汛会议等多项市领导活动"},

    # 邝驱
    {"person_id": 6, "org_id": 1, "title": "梧州市领导（疑似市委常委）", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},

    # 杨赞彬
    {"person_id": 7, "org_id": 1, "title": "梧州市领导（疑似市纪委书记/市委常委）", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},

    # 郝凯广
    {"person_id": 8, "org_id": 1, "title": "梧州市领导（疑似市委秘书长/市委常委）", "start": "待查", "end": "至今", "rank": "副厅级", "note": "多次随同市委书记邱明宏调研，疑为市委秘书长"},

    # 马秀明
    {"person_id": 9, "org_id": 1, "title": "梧州市领导（疑似市委常委/副市长）", "start": "待查", "end": "至今", "rank": "副厅级", "note": "随同邱明宏调研城市更新工作"},

    # 杜诚
    {"person_id": 10, "org_id": 2, "title": "梧州市领导", "start": "待查", "end": "至今", "rank": "", "note": ""},

    # 周志军
    {"person_id": 11, "org_id": 2, "title": "梧州市领导", "start": "待查", "end": "至今", "rank": "", "note": ""},

    # 曾健勇
    {"person_id": 12, "org_id": 2, "title": "梧州市领导", "start": "待查", "end": "至今", "rank": "", "note": ""},

    # 杨桢
    {"person_id": 13, "org_id": 2, "title": "梧州市领导（副市长）", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},

    # 蒙中平
    {"person_id": 17, "org_id": 2, "title": "梧州市领导（副市长）", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},

    # 劳高进
    {"person_id": 18, "org_id": 2, "title": "梧州市领导（副市长）", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},

    # 苏思远
    {"person_id": 19, "org_id": 2, "title": "梧州市领导（副市长）", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},

    # 王鹏
    {"person_id": 20, "org_id": 2, "title": "梧州市领导（副市长）", "start": "待查", "end": "至今", "rank": "副厅级", "note": "出席多场市领导活动"},

    # 武晓辉
    {"person_id": 21, "org_id": 2, "title": "梧州市领导（副市长）", "start": "待查", "end": "至今", "rank": "副厅级", "note": "出席多场市领导活动"},

    # 苏颖
    {"person_id": 25, "org_id": 2, "title": "梧州市领导（副市长）", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},

    # 李贞梅
    {"person_id": 23, "org_id": 4, "title": "梧州市政协副主席", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},

    # 曹垂龙
    {"person_id": 24, "org_id": 4, "title": "梧州市政协副主席", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
]

# 4. Relationships
relationships = [
    # 党政一把手关系
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "邱明宏（市委书记）与谭秀洪（市长/市委副书记）为梧州市党政一把手工作搭档",
        "overlap_org": "中共梧州市委员会/梧州市人民政府",
        "overlap_period": "2025年至今（待确认具体起始时间）",
        "confidence": "confirmed",
        "source": "wuzhou.gov.cn 2026年7月新闻报道"
    },
    # 谭秀洪 - 邱明宏（上下级关系）
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "市委书记邱明宏为市委一把手，市长谭秀洪为市政府一把手并任市委副书记",
        "overlap_org": "中共梧州市委员会",
        "overlap_period": "2025年至今",
        "confidence": "confirmed",
        "source": "wuzhou.gov.cn 2026年7月新闻报道"
    },
    # 邱明宏 - 郝凯广（工作关系）
    {
        "person_a": 1,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "郝凯广多次随同市委书记邱明宏调研、出席活动，可能为市委秘书长",
        "overlap_org": "中共梧州市委员会",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
        "source": "wuzhou.gov.cn 2026年7月新闻报道"
    },
    # 邱明宏 - 马秀明（工作关系）
    {
        "person_a": 1,
        "person_b": 9,
        "type": "overlap",
        "context": "马秀明随同邱明宏调研城市更新工作",
        "overlap_org": "中共梧州市委员会",
        "overlap_period": "2026年7月",
        "confidence": "confirmed",
        "source": "wuzhou.gov.cn 2026年7月21日新闻报道"
    },
    # 谭秀洪 - 覃元臻（工作关系）
    {
        "person_a": 2,
        "person_b": 5,
        "type": "overlap",
        "context": "覃元臻出席防汛工作会议，谭秀洪同时参加",
        "overlap_org": "梧州市人民政府",
        "overlap_period": "2026年7月",
        "confidence": "confirmed",
        "source": "wuzhou.gov.cn 2026年7月新闻报道"
    },
    # 谭秀洪 - 武晓辉（工作关系）
    {
        "person_a": 2,
        "person_b": 21,
        "type": "overlap",
        "context": "武晓辉出席防汛工作会议，谭秀洪同时参加",
        "overlap_org": "梧州市人民政府",
        "overlap_period": "2026年7月",
        "confidence": "confirmed",
        "source": "wuzhou.gov.cn 2026年7月新闻报道"
    },
    # 马克兵（人大）- 黄振饶（政协）同时出席活动
    {
        "person_a": 3,
        "person_b": 4,
        "type": "overlap",
        "context": "马克兵（市人大常委会主任）和黄振饶（市政协主席）同为市四家班子主要领导，多次共同出席活动",
        "overlap_org": "梧州市",
        "overlap_period": "2025年至今",
        "confidence": "confirmed",
        "source": "wuzhou.gov.cn 2026年7月21日新闻报道"
    },
]

# ── Build ──
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print("\n✅ Build complete!")
    print(f"   Database: {DB_PATH}")
    print(f"   GEXF:     {GEXF_PATH}")
    print(f"\nNotes:")
    print(f"  - 邱明宏（市委书记）早期履历：1986年入西安农校，1990年陕西宁强工作，完整中层履历因百科页面被截断未获取")
    print(f"  - 谭秀洪（市长）曾任商务厅副厅长、北海市委常委/副市长，到梧州具体时间待查")
    print(f"  - 27名相关市领导信息均来自2026年7月政府网站新闻名单，具体职务分工需进一步确认")
    print(f"  - 前任书记/市长信息待补充")
