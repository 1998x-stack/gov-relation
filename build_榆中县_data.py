#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 榆中县 (Yuzhong County, Lanzhou, Gansu) leadership network.

榆中县 — 甘肃省兰州市下辖县.
Covers current Party Secretary (崔峰巍), County Magistrate (魏孔毅), their predecessors,
key leadership team members, and organizational hierarchy.

Data sources:
- 榆中县人民政府网站 (www.yuzhong.gov.cn) — 县委领导/政府领导 pages
- 榆中县第十九届人大会议公告 (2024-01, 2024-03, 2026-01)
- 政协榆中县第十届委员会会议报道 (2024-01, 2025-02)
- 榆中县委十七届九次/十次/十一次全会报道 (2025-01, 2025-08, 2025-12)
- 澎湃新闻/人民网/网易新闻报道
- 百度百科
"""

import sqlite3
import os
import json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/gansu_榆中县")
os.makedirs(STAGING, exist_ok=True)

DB_PATH = os.path.join(STAGING, "榆中县_network.db")
GEXF_PATH = os.path.join(STAGING, "榆中县_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── A. Current Top Leaders ──

    # 崔峰巍 — 榆中县委书记 (from 2023-10), also 兰州榆中生态创新城党工委副书记(兼)
    {"id": 1, "name": "崔峰巍", "gender": "男", "ethnicity": "土族",
     "birth": "1978-02", "birthplace": "甘肃永靖",
     "education": "甘肃农业大学农业推广硕士",
     "party_join": "2000-12", "work_start": "2002-08",
     "current_post": "榆中县委书记",
     "current_org": "中共榆中县委",
     "source": "https://www.yuzhong.gov.cn — 榆中县政府网站县委领导页; 百度百科"},

    # 魏孔毅 — 榆中县委副书记、县长 (elected 2024-01-28)
    {"id": 2, "name": "魏孔毅", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-05", "birthplace": "甘肃皋兰",
     "education": "甘肃省委党校研究生学历",
     "party_join": "1998-10", "work_start": "1995-07",
     "current_post": "榆中县县长",
     "current_org": "榆中县人民政府",
     "source": "https://www.yuzhong.gov.cn — 榆中县政府网站政府领导页; 澎湃新闻（2024-01-29）; 百度百科"},

    # ── B. Leadership Team Members: 县委常委会 ──

    # 吕江宇 — 县委副书记、政法委书记 (2024-02 起任县委常委)
    {"id": 3, "name": "吕江宇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榆中县委副书记、政法委书记",
     "current_org": "中共榆中县委",
     "source": "https://www.yuzhong.gov.cn — 榆中县政府网站县委领导页; 榆中县委十七届九次全会报道（2025-01-02）"},

    # 赛勇 — 县委常委
    {"id": 4, "name": "赛勇", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榆中县委常委",
     "current_org": "中共榆中县委",
     "source": "https://www.yuzhong.gov.cn — 榆中县政府网站县委领导页（2025-12-02更新）"},

    # 张亚军 — 县委常委、县纪委书记、监委代主任
    {"id": 5, "name": "张亚军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榆中县委常委、县纪委书记",
     "current_org": "中共榆中县纪律检查委员会",
     "source": "https://www.yuzhong.gov.cn — 榆中县政府网站县委领导页（2025-12-05更新）; 信用中国 — 榆中县政府全体会议报道（2025-09-22）"},

    # 陈力 — 县委常委
    {"id": 6, "name": "陈力", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榆中县委常委",
     "current_org": "中共榆中县委",
     "source": "https://www.yuzhong.gov.cn — 榆中县政府网站县委领导页（2025-12-05更新）"},

    # 苏鑫良 — 县委常委
    {"id": 7, "name": "苏鑫良", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榆中县委常委",
     "current_org": "中共榆中县委",
     "source": "https://www.yuzhong.gov.cn — 榆中县政府网站县委领导页（2024-02-26更新）"},

    # 陈光华 — 县委常委、常务副县长 (previously 县监察委员会主任)
    {"id": 8, "name": "陈光华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榆中县委常委、常务副县长",
     "current_org": "榆中县人民政府",
     "source": "https://www.yuzhong.gov.cn — 榆中县政府网站县委领导页（2025-12-03更新）; 榆中县第十九届人大三次会议公告（2024-01-28）"},

    # 刘文序 — 县委常委
    {"id": 9, "name": "刘文序", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榆中县委常委",
     "current_org": "中共榆中县委",
     "source": "https://www.yuzhong.gov.cn — 榆中县政府网站县委领导页（2024-01-16更新）"},

    # 李超 — 县委常委
    {"id": 10, "name": "李超", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榆中县委常委",
     "current_org": "中共榆中县委",
     "source": "https://www.yuzhong.gov.cn — 榆中县政府网站县委领导页（2024-03-12更新）"},

    # 王龙 — 县委常委
    {"id": 11, "name": "王龙", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榆中县委常委",
     "current_org": "中共榆中县委",
     "source": "https://www.yuzhong.gov.cn — 榆中县政府网站县委领导页（2024-02-26更新）"},

    # 李奉洁 — 县委常委、副县长
    {"id": 12, "name": "李奉洁", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榆中县委常委、副县长",
     "current_org": "榆中县人民政府",
     "source": "https://www.yuzhong.gov.cn — 榆中县政府网站县委领导页（2025-08-20更新）; 网易新闻 — 2026-07-09报道"},

    # ── C. Government Leadership Team ──

    # 高永红 — 副县长
    {"id": 13, "name": "高永红", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榆中县副县长",
     "current_org": "榆中县人民政府",
     "source": "https://www.yuzhong.gov.cn — 榆中县政府网站政府领导页（2025-12-02更新）"},

    # 魏职兵 — 副县长
    {"id": 14, "name": "魏职兵", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榆中县副县长",
     "current_org": "榆中县人民政府",
     "source": "https://www.yuzhong.gov.cn — 榆中县政府网站政府领导页（2025-12-03更新）"},

    # 马昊川 — 副县长
    {"id": 15, "name": "马昊川", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榆中县副县长",
     "current_org": "榆中县人民政府",
     "source": "https://www.yuzhong.gov.cn — 榆中县政府网站政府领导页（2025-12-02更新）"},

    # 张博 — 副县长 (2026-02-10 updated)
    {"id": 16, "name": "张博", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榆中县副县长",
     "current_org": "榆中县人民政府",
     "source": "https://www.yuzhong.gov.cn — 榆中县政府网站政府领导页（2026-02-10更新）"},

    # ── D. 人大 & 政协 ──

    # 张宗福 — 县人大常委会主任
    {"id": 17, "name": "张宗福", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榆中县人大常委会主任",
     "current_org": "榆中县人大常委会",
     "source": "https://www.yuzhong.gov.cn — 榆中县两会报道（2024-01, 2025-02）"},

    # 于军 — 县政协主席
    {"id": 18, "name": "于军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榆中县政协主席",
     "current_org": "榆中县政协",
     "source": "https://www.yuzhong.gov.cn — 政协榆中县第十届三次会议（2024-01-27）; 榆中县政府网站"},

    # ── E. Predecessors ──

    # 冯月旺 — 前任榆中县委书记 (2021-11 当选, 兼兰州市人大常委会副主任)
    {"id": 19, "name": "冯月旺", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "兰州市人大常委会副主任（原榆中县委书记）",
     "current_org": "兰州市人大常委会",
     "source": "人民网 — 冯月旺当选榆中县委书记报道（2021-11-25）; 汲古新知 — 崔峰巍已任榆中县委书记（2023-10-09）"},

    # 王晓宁 — 更早前任榆中县委书记 (被停职检查)
    {"id": 20, "name": "王晓宁", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-07", "birthplace": "",
     "education": "西北师范大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原榆中县委书记（已停职）",
     "current_org": "原中共榆中县委",
     "source": "https://baike.baidu.com — 王晓宁百度百科; 甘肃省委决定 — 榆中县委书记王晓宁停职检查"},

    # 刘学强 — 前任榆中县长 (resigned 2023-10)
    {"id": 21, "name": "刘学强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原榆中县长（已辞职）",
     "current_org": "原榆中县人民政府",
     "source": "甘肃政法网 — 人事任免（2023-10-08）; 网易新闻（2026-01-14）"},

    # 马张永 — 前任县委副书记 (2024-02 前)
    {"id": 22, "name": "马张永", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原榆中县委副书记",
     "current_org": "原中共榆中县委",
     "source": "中国甘肃网 — 兰州榆中2024年新春第一会报道（2024-02-20）; 网易 — 榆中县第十九届人大三次会议报道（2024-03-02）"},

    # 王廷宏 — 县政协党组副书记
    {"id": 23, "name": "王廷宏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "榆中县政协党组副书记",
     "current_org": "榆中县政协",
     "source": "https://www.yuzhong.gov.cn — 政协榆中县十届四次会议开幕报道（2025-02-17）"},

    # ── F. City-level leaders (Lanzhou) ──
    {"id": 24, "name": "张晓强", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-11", "birthplace": "浙江庆元",
     "education": "浙江林学院林学专业、美国肯恩大学公共管理硕士",
     "party_join": "1996-06", "work_start": "1996-08",
     "current_post": "甘肃省委常委、兰州市委书记",
     "current_org": "中共兰州市委员会",
     "source": "https://zh.wikipedia.org/wiki/%E5%BC%A0%E6%99%93%E5%BC%BA_(1975%E5%B9%B4)"},

    {"id": 25, "name": "刘建勋", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-03", "birthplace": "甘肃武威",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "兰州市人民政府市长",
     "current_org": "兰州市人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E5%85%B0%E5%B7%9E%E5%B8%82"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # County-level
    {"id": 1, "name": "中共榆中县委", "type": "党委", "level": "县级", "parent": "中共兰州市委员会", "location": "甘肃省兰州市榆中县"},
    {"id": 2, "name": "榆中县人民政府", "type": "政府", "level": "县级", "parent": "兰州市人民政府", "location": "甘肃省兰州市榆中县"},
    {"id": 3, "name": "中共榆中县纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共榆中县委", "location": "甘肃省兰州市榆中县"},
    {"id": 4, "name": "榆中县人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "甘肃省兰州市榆中县"},
    {"id": 5, "name": "榆中县政协", "type": "政协", "level": "县级", "parent": "", "location": "甘肃省兰州市榆中县"},
    {"id": 6, "name": "中共榆中县委政法委员会", "type": "党委", "level": "乡科级", "parent": "中共榆中县委", "location": "甘肃省兰州市榆中县"},
    {"id": 7, "name": "兰州榆中生态创新城管理委员会", "type": "政府", "level": "县级", "parent": "兰州市人民政府", "location": "甘肃省兰州市榆中县"},

    # City-level
    {"id": 8, "name": "中共兰州市委员会", "type": "党委", "level": "副省级", "parent": "中共甘肃省委员会", "location": "甘肃省兰州市"},
    {"id": 9, "name": "兰州市人民政府", "type": "政府", "level": "副省级", "parent": "甘肃省人民政府", "location": "甘肃省兰州市"},
    {"id": 10, "name": "兰州市人大常委会", "type": "人大", "level": "副省级", "parent": "", "location": "甘肃省兰州市"},

    # Provincial-level
    {"id": 11, "name": "中共甘肃省委员会", "type": "党委", "level": "省级", "parent": "", "location": "甘肃省兰州市"},
    {"id": 12, "name": "甘肃省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "甘肃省兰州市"},
]

# =========================================================================
# POSITIONS (current and historical)
# =========================================================================
positions = [
    # ── 崔峰巍 — 县委书记 career ──
    {"person_id": 1, "org_id": 1, "title": "榆中县委书记", "start": "2023-10", "end": "", "rank": "正处", "note": "2023年10月任县委书记；同时兼任兰州榆中生态创新城党工委副书记"},
    {"person_id": 1, "org_id": 7, "title": "兰州榆中生态创新城党工委副书记（兼）", "start": "2023-10", "end": "", "rank": "正处", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "兰州市农业农村局（乡村振兴局）党组书记、局长", "start": "", "end": "2023-10", "rank": "正处", "note": "接任县委书记前任职"},
    {"person_id": 1, "org_id": 8, "title": "兰州市委副秘书长", "start": "", "end": "", "rank": "副处/正处", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "兰州市文明办主任", "start": "", "end": "", "rank": "正处", "note": "曾在兰州市委督查室、文明办等单位任职"},
    {"person_id": 1, "org_id": 8, "title": "兰州市委督查室主任", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "兰州市人民政府督查室副主任", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "兰州市农业委员会副主任", "start": "2013-07", "end": "", "rank": "副处", "note": "2013年7月从永靖县跨市州上调兰州市任农业委员会副主任"},
    {"person_id": 1, "org_id": 0, "title": "永靖县太极镇党委书记", "start": "", "end": "2013-07", "rank": "正科", "note": "在永靖县先后担任副镇长、镇长、乡党委书记、镇党委书记"},

    # ── 魏孔毅 — 县长 career ──
    {"person_id": 2, "org_id": 2, "title": "榆中县县长", "start": "2024-01-28", "end": "", "rank": "正处", "note": "2024年1月28日榆中县第十九届人大三次会议正式当选；此前2023年10月任代县长"},
    {"person_id": 2, "org_id": 1, "title": "榆中县委副书记", "start": "2023-10", "end": "", "rank": "正处", "note": ""},
    {"person_id": 2, "org_id": 7, "title": "兰州榆中生态创新城党工委委员、管委会副主任（兼）", "start": "", "end": "", "rank": "正处", "note": ""},
    {"person_id": 2, "org_id": 9, "title": "兰州市交通运输委员会主任", "start": "", "end": "2023-10", "rank": "正处", "note": "调任榆中前任职"},
    {"person_id": 2, "org_id": 9, "title": "兰州市人民防空办公室主任", "start": "", "end": "", "rank": "正处", "note": ""},
    {"person_id": 2, "org_id": 9, "title": "兰州市发展和改革委员会副主任", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 2, "org_id": 9, "title": "兰州市生态建设管理局副局长", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 2, "org_id": 0, "title": "永登县委常委、副县长", "start": "2011", "end": "", "rank": "副处", "note": "2011年起任永登县副县长、县委常委"},
    {"person_id": 2, "org_id": 0, "title": "皋兰县科技局/政协办公室/林业局", "start": "1995-07", "end": "2011", "rank": "", "note": "1995年从甘肃省林业学校毕业后在皋兰县林业局、政协办公室、科技局、什川镇等单位工作"},

    # ── 吕江宇 — 县委副书记、政法委书记 ──
    {"person_id": 3, "org_id": 1, "title": "榆中县委副书记", "start": "2024-02", "end": "", "rank": "副处", "note": "2024年2月26日更新为县委常委"},
    {"person_id": 3, "org_id": 6, "title": "榆中县委政法委书记", "start": "", "end": "", "rank": "副处", "note": "兼任，报道确认于2025-02"},

    # ── 赛勇 ──
    {"person_id": 4, "org_id": 1, "title": "榆中县委常委", "start": "", "end": "", "rank": "副处", "note": "2025年12月2日更新"},

    # ── 张亚军 ──
    {"person_id": 5, "org_id": 1, "title": "榆中县委常委", "start": "", "end": "", "rank": "副处", "note": "2025年12月5日更新"},
    {"person_id": 5, "org_id": 3, "title": "榆中县纪委书记、监委代主任", "start": "", "end": "", "rank": "副处", "note": "2025年9月报道显示为县委常委、县纪委书记、监委代主任"},

    # ── 陈力 ──
    {"person_id": 6, "org_id": 1, "title": "榆中县委常委", "start": "", "end": "", "rank": "副处", "note": "2025年12月5日更新"},

    # ── 苏鑫良 ──
    {"person_id": 7, "org_id": 1, "title": "榆中县委常委", "start": "", "end": "", "rank": "副处", "note": "2024年2月26日更新"},

    # ── 陈光华 ──
    {"person_id": 8, "org_id": 1, "title": "榆中县委常委", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "榆中县常务副县长", "start": "", "end": "", "rank": "副处", "note": "2025年1月报道显示为县委常委、常务副县长；此前曾任县监察委员会主任"},
    {"person_id": 8, "org_id": 3, "title": "榆中县监察委员会主任", "start": "2024-01-28", "end": "", "rank": "副处", "note": "2024年1月28日人大会议当选"},

    # ── 刘文序 ──
    {"person_id": 9, "org_id": 1, "title": "榆中县委常委", "start": "", "end": "", "rank": "副处", "note": "2024年1月16日更新"},

    # ── 李超 ──
    {"person_id": 10, "org_id": 1, "title": "榆中县委常委", "start": "", "end": "", "rank": "副处", "note": "2024年3月12日更新"},

    # ── 王龙 ──
    {"person_id": 11, "org_id": 1, "title": "榆中县委常委", "start": "", "end": "", "rank": "副处", "note": "2024年2月26日更新"},

    # ── 李奉洁 ──
    {"person_id": 12, "org_id": 1, "title": "榆中县委常委", "start": "", "end": "", "rank": "副处", "note": "2025年8月20日更新"},
    {"person_id": 12, "org_id": 2, "title": "榆中县副县长", "start": "", "end": "", "rank": "副处", "note": ""},

    # ── 高永红 ──
    {"person_id": 13, "org_id": 2, "title": "榆中县副县长", "start": "", "end": "", "rank": "副处", "note": "2025年12月2日更新"},

    # ── 魏职兵 ──
    {"person_id": 14, "org_id": 2, "title": "榆中县副县长", "start": "", "end": "", "rank": "副处", "note": "2025年12月3日更新"},

    # ── 马昊川 ──
    {"person_id": 15, "org_id": 2, "title": "榆中县副县长", "start": "", "end": "", "rank": "副处", "note": "2025年12月2日更新"},

    # ── 张博 ──
    {"person_id": 16, "org_id": 2, "title": "榆中县副县长", "start": "", "end": "", "rank": "副处", "note": "2026年2月10日更新"},

    # ── 张宗福 ──
    {"person_id": 17, "org_id": 4, "title": "榆中县人大常委会主任", "start": "", "end": "", "rank": "正处", "note": ""},

    # ── 于军 ──
    {"person_id": 18, "org_id": 5, "title": "榆中县政协主席", "start": "2024-01-27", "end": "", "rank": "正处", "note": "2024年1月27日政协榆中县第十届三次会议当选"},

    # ── 冯月旺 — 前任县委书记 ──
    {"person_id": 19, "org_id": 1, "title": "榆中县委书记", "start": "2021-11", "end": "2023-10", "rank": "正处", "note": "2021年11月24日当选第十七届县委书记；兼兰州市人大常委会副主任"},
    {"person_id": 19, "org_id": 10, "title": "兰州市人大常委会副主任（兼）", "start": "", "end": "", "rank": "副厅", "note": "兼任榆中县委书记期间"},

    # ── 王晓宁 — 更早前任县委书记 ──
    {"person_id": 20, "org_id": 1, "title": "榆中县委书记", "start": "", "end": "", "rank": "正处", "note": "因违纪被停职检查"},

    # ── 刘学强 — 前任县长 ──
    {"person_id": 21, "org_id": 2, "title": "榆中县县长", "start": "", "end": "2023-10", "rank": "正处", "note": "2023年10月8日辞去县长职务"},
    {"person_id": 21, "org_id": 1, "title": "榆中县委副书记", "start": "", "end": "2023-10", "rank": "正处", "note": ""},

    # ── 马张永 — 前任县委副书记 ──
    {"person_id": 22, "org_id": 1, "title": "榆中县委副书记", "start": "", "end": "2024", "rank": "副处", "note": "2024年2月仍以副书记身份出现，后被吕江宇接替"},

    # ── 王廷宏 — 县政协党组副书记 ──
    {"person_id": 23, "org_id": 5, "title": "榆中县政协党组副书记", "start": "", "end": "", "rank": "副处", "note": ""},

    # ── City leaders ──
    {"person_id": 24, "org_id": 8, "title": "甘肃省委常委、兰州市委书记", "start": "2023-07", "end": "", "rank": "副部", "note": ""},
    {"person_id": 25, "org_id": 9, "title": "兰州市市长", "start": "2023-03", "end": "", "rank": "副部", "note": ""},
]

# =========================================================================
# RELATIONSHIPS (person↔person)
# =========================================================================
relationships = [
    # ── Core Leadership Pair ──
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "崔峰巍（县委书记）与魏孔毅（县长）党政搭档", "overlap_org": "榆中县", "overlap_period": "2023-10至今"},

    # ── 崔峰巍 with key deputies ──
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记与县委副书记、政法委书记", "overlap_org": "中共榆中县委", "overlap_period": "2024-02至今"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "县委书记与县纪委书记", "overlap_org": "中共榆中县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "县委书记与常务副县长", "overlap_org": "中共榆中县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "上下级", "context": "县委书记与县委常委、副县长", "overlap_org": "中共榆中县委", "overlap_period": "2025-08至今"},
    {"person_a": 1, "person_b": 17, "type": "同僚", "context": "县委书记与人大常委会主任同届共事", "overlap_org": "榆中县", "overlap_period": ""},
    {"person_a": 1, "person_b": 18, "type": "同僚", "context": "县委书记与政协主席同届共事", "overlap_org": "榆中县", "overlap_period": ""},

    # ── 魏孔毅 with deputies ──
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "县长与常务副县长", "overlap_org": "榆中县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "县长与县委常委、副县长", "overlap_org": "榆中县人民政府", "overlap_period": "2025-08至今"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "县长与副县长", "overlap_org": "榆中县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "县长与副县长", "overlap_org": "榆中县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "上下级", "context": "县长与副县长", "overlap_org": "榆中县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "上下级", "context": "县长与副县长", "overlap_org": "榆中县人民政府", "overlap_period": "2026-02至今"},

    # ── 县委常委会内部 ──
    {"person_a": 1, "person_b": 4, "type": "同僚", "context": "县委常委班子同僚", "overlap_org": "中共榆中县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "同僚", "context": "县委常委班子同僚", "overlap_org": "中共榆中县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "同僚", "context": "县委常委班子同僚", "overlap_org": "中共榆中县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "同僚", "context": "县委常委班子同僚", "overlap_org": "中共榆中县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "同僚", "context": "县委常委班子同僚", "overlap_org": "中共榆中县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "同僚", "context": "县委常委班子同僚", "overlap_org": "中共榆中县委", "overlap_period": ""},

    # ── Predecessor-Successor ──
    {"person_a": 1, "person_b": 19, "type": "前后任", "context": "崔峰巍（2023-）接替冯月旺（2021-2023）任县委书记", "overlap_org": "中共榆中县委", "overlap_period": "2023交接"},
    {"person_a": 19, "person_b": 20, "type": "前后任", "context": "冯月旺接替王晓宁任县委书记", "overlap_org": "中共榆中县委", "overlap_period": ""},
    {"person_a": 2, "person_b": 21, "type": "前后任", "context": "魏孔毅（2024-）接替刘学强（-2023）任县长", "overlap_org": "榆中县人民政府", "overlap_period": "2023交接"},

    # ── City leadership connection ──
    {"person_a": 1, "person_b": 24, "type": "上下级", "context": "县委书记接受兰州市委书记领导", "overlap_org": "中共兰州市委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 25, "type": "上下级", "context": "县长接受市长领导", "overlap_org": "兰州市人民政府", "overlap_period": ""},
]

# =========================================================================
# BUILD SQLITE DATABASE
# =========================================================================
def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    cur.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p["gender"], p["ethnicity"],
                     p["birth"], p["birthplace"], p["education"],
                     p["party_join"], p["work_start"],
                     p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"],
                     o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
                        VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"],
                     pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                        VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"],
                     r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"✅ SQLite database written: {DB_PATH}")

# =========================================================================
# BUILD GEXF GRAPH
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def color_for_role(post):
    if post is None:
        return "100,100,100"
    if "县委书记" in post and "纪委" not in post and "副" not in post:
        return "255,50,50"
    if ("县长" in post and "副" not in post):
        return "50,100,255"
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"
    if "县委常委" in post or "县委" in post:
        return "200,150,100"
    if "人大" in post:
        return "180,180,100"
    if "政协" in post:
        return "100,180,100"
    return "100,100,100"

def org_color(otype):
    cmap = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,200,100",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return cmap.get(otype, "200,200,200")

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append('    <description>榆中县领导班子工作关系网络 — 包含县委书记、县长、领导班子成员及前后任关系</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('    </attributes>')

    # ── Nodes: Persons ──
    lines.append('    <nodes>')
    for p in persons:
        pid = f"p{p['id']}"
        c = color_for_role(p["current_post"])
        is_top = "县委书记" in (p["current_post"] or "") and "纪委" not in (p["current_post"] or "") and "副" not in (p["current_post"] or "")
        is_gov = ("县长" in (p["current_post"] or "") and "副" not in (p["current_post"] or ""))
        sz = "20.0" if is_top or is_gov else "12.0"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"] or "")}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # ── Nodes: Organizations ──
    for o in organizations:
        oid = f"o{o['id']}"
        oc = org_color(o["type"])
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # ── Edges ──
    lines.append('    <edges>')
    edge_id = 1

    # Person→Organization (worked_at)
    for pos in positions:
        pid = f"p{pos['person_id']}"
        if pos['org_id'] == 0:
            continue  # skip local-only positions without a matching org node
        oid = f"o{pos['org_id']}"
        lines.append(f'      <edge id="e{edge_id}" source="{pid}" target="{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        edge_id += 1

    # Person↔Person (relationship)
    for r in relationships:
        pa = f"p{r['person_a']}"
        pb = f"p{r['person_b']}"
        weight = "2.0"
        lines.append(f'      <edge id="e{edge_id}" source="{pa}" target="{pb}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        edge_id += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF graph written: {GEXF_PATH}")

# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    build_db()
    build_gexf()
    print(f"📊 Persons: {len(persons)}")
    print(f"🏢 Organizations: {len(organizations)}")
    print(f"💼 Positions: {len(positions)}")
    print(f"🔗 Relationships: {len(relationships)}")
    print("✅ Build complete.")
