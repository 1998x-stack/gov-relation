#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
北海市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 地级市
Province: 广西壮族自治区
Parent City:
Region: 北海市
Targets: 市委书记 & 市长

当前在任 (as of 2026-07-23):
- 市委书记: 李楚 (北海市委书记、北海军分区党委第一书记)
- 市长: 李刚 (北海市委副书记、市政府市长、党组书记)
"""

import json
import os
import sys
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "北海市"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-23"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：市委书记 (2026.05-)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "李楚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年1月",
        "birthplace": "广西桂平",
        "education": "在职研究生学历，法学学士",
        "party_join": "1993年12月",
        "work_start": "1995年7月",
        "current_post": "北海市委书记、北海军分区党委第一书记",
        "current_org": "中共北海市委员会",
        "source": "https://baike.baidu.com/item/%E6%9D%8E%E6%A5%9A/13681350"
    },
    # ════════════════════════════════════════
    # 核心领导：市长 (2025.10-)
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "李刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年7月",
        "birthplace": "待查",
        "education": "研究生学历，经济学博士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "北海市委副书记、市政府市长、党组书记",
        "current_org": "北海市人民政府",
        "source": "https://baike.baidu.com/item/%E6%9D%8E%E5%88%9A/22884963"
    },
    # ════════════════════════════════════════
    # 前任市委书记 (2021.01-2026.05)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "蔡锦军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年11月",
        "birthplace": "江西九江",
        "education": "研究生学历，文学硕士，高级管理人员工商管理硕士",
        "party_join": "1996年12月",
        "work_start": "1986年8月",
        "current_post": "自治区园区办主任（党组书记）",
        "current_org": "广西壮族自治区产业园区改革发展办公室",
        "source": "https://baike.baidu.com/item/%E8%94%A1%E9%94%A6%E5%86%9B/3878047"
    },
    # ════════════════════════════════════════
    # 市人大常委会主任
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "陆海生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年9月",
        "birthplace": "广西灌阳",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "北海市人大常委会主任",
        "current_org": "北海市人民代表大会常务委员会",
        "source": "https://zh.wikipedia.org/zh-hans/%E5%8C%97%E6%B5%B7%E5%B8%82"
    },
    # ════════════════════════════════════════
    # 市政协主席
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "蔡可辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年9月",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "北海市政协主席",
        "current_org": "中国人民政治协商会议北海市委员会",
        "source": "https://zh.wikipedia.org/zh-hans/%E5%8C%97%E6%B5%B7%E5%B8%82"
    },
    # ════════════════════════════════════════
    # 市委副书记、组织部部长
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "吕勇江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年9月",
        "birthplace": "待查",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "北海市委副书记、组织部部长，市委党校校长",
        "current_org": "中共北海市委员会",
        "source": "http://m.ce.cn/bwzg/202109/01/t20210901_36869833.shtml"
    },
    # ════════════════════════════════════════
    # 市纪委书记、市监委主任
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "黄毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "北海市委常委、市纪委书记、市监委主任",
        "current_org": "中共北海市纪律检查委员会/北海市监察委员会",
        "source": "https://baike.baidu.com/item/%E4%B8%AD%E5%9B%BD%E5%85%B1%E4%BA%A7%E5%85%9A%E5%8C%97%E6%B5%B7%E5%B8%82%E5%A7%94%E5%91%98%E4%BC%9A/60050924"
    },
    # ════════════════════════════════════════
    # 常务副市长
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "黄宏瞻",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "北海市委常委、常务副市长",
        "current_org": "北海市人民政府",
        "source": "https://baike.baidu.com/item/%E4%B8%AD%E5%9B%BD%E5%85%B1%E4%BA%A7%E5%85%9A%E5%8C%97%E6%B5%B7%E5%B8%82%E5%A7%94%E5%91%98%E4%BC%9A/60050924"
    },
    # ════════════════════════════════════════
    # 市委宣传部部长
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "郑定雄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年9月",
        "birthplace": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "北海市委常委、宣传部部长",
        "current_org": "中共北海市委员会宣传部",
        "source": "http://m.ce.cn/bwzg/202109/01/t20210901_36869833.shtml"
    },
    # ════════════════════════════════════════
    # 市委统战部部长、副市长
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "龙起云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年10月",
        "birthplace": "广西北海",
        "education": "大学学历",
        "party_join": "1999年5月",
        "work_start": "1995年7月",
        "current_post": "北海市委常委、统战部部长，市政府副市长、党组成员",
        "current_org": "中共北海市委员会统战部/北海市人民政府",
        "source": "https://www.163.com/dy/article/J395PE2M05563WHO.html"
    },
    # ════════════════════════════════════════
    # 市委秘书长
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "麦成柱",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1974年2月",
        "birthplace": "广西横县",
        "education": "在职研究生学历",
        "party_join": "1995年11月",
        "work_start": "1998年4月",
        "current_post": "北海市委常委、秘书长",
        "current_org": "中共北海市委员会",
        "source": "https://www.163.com/dy/article/J395PE2M05563WHO.html"
    },
    # ════════════════════════════════════════
    # 市委政法委书记
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "杨斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年10月",
        "birthplace": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "北海市委常委、政法委书记",
        "current_org": "中共北海市委员会政法委员会",
        "source": "http://m.ce.cn/bwzg/202109/01/t20210901_36869833.shtml"
    },
    # ════════════════════════════════════════
    # 北海军分区司令员
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "沙卫良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "北海市委常委、北海军分区司令员",
        "current_org": "北海军分区",
        "source": "https://baike.baidu.com/item/%E4%B8%AD%E5%9B%BD%E5%85%B1%E4%BA%A7%E5%85%9A%E5%8C%97%E6%B5%B7%E5%B8%82%E5%A7%94%E5%91%98%E4%BC%9A/60050924"
    },
    # ════════════════════════════════════════
    # 前任市长 (2022.01-2025.10)
    # ════════════════════════════════════════
    {
        "id": 14,
        "name": "李莉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1973年7月",
        "birthplace": "待查",
        "education": "在职研究生学历，经济学博士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "自治区党委组织部分管日常工作的副部长",
        "current_org": "广西壮族自治区党委组织部",
        "source": "https://www.jfdaily.com/news/detail?id=1014303"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {
        "id": 1,
        "name": "中共北海市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广西壮族自治区委员会",
        "location": "北海市海城区"
    },
    {
        "id": 2,
        "name": "北海市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广西壮族自治区人民政府",
        "location": "北海市海城区"
    },
    {
        "id": 3,
        "name": "北海市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级市",
        "parent": "广西壮族自治区人民代表大会常务委员会",
        "location": "北海市海城区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议北海市委员会",
        "type": "政协",
        "level": "地级市",
        "parent": "中国人民政治协商会议广西壮族自治区委员会",
        "location": "北海市海城区"
    },
    {
        "id": 5,
        "name": "中共北海市纪律检查委员会/北海市监察委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共北海市委员会",
        "location": "北海市海城区"
    },
    {
        "id": 6,
        "name": "中共北海市委员会组织部",
        "type": "党委",
        "level": "地级市",
        "parent": "中共北海市委员会",
        "location": "北海市海城区"
    },
    {
        "id": 7,
        "name": "中共北海市委员会宣传部",
        "type": "党委",
        "level": "地级市",
        "parent": "中共北海市委员会",
        "location": "北海市海城区"
    },
    {
        "id": 8,
        "name": "中共北海市委员会统战部",
        "type": "党委",
        "level": "地级市",
        "parent": "中共北海市委员会",
        "location": "北海市海城区"
    },
    {
        "id": 9,
        "name": "中共北海市委员会政法委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共北海市委员会",
        "location": "北海市海城区"
    },
    {
        "id": 10,
        "name": "北海军分区",
        "type": "党委",
        "level": "地级市",
        "parent": "广西军区",
        "location": "北海市"
    },
    {
        "id": 11,
        "name": "广西壮族自治区产业园区改革发展办公室",
        "type": "政府",
        "level": "省级",
        "parent": "广西壮族自治区人民政府",
        "location": "南宁市"
    },
    {
        "id": 12,
        "name": "广西壮族自治区党委组织部",
        "type": "党委",
        "level": "省级",
        "parent": "中共广西壮族自治区委员会",
        "location": "南宁市"
    },
    {
        "id": 13,
        "name": "共青团广西壮族自治区委员会",
        "type": "群团",
        "level": "省级",
        "parent": "共青团中央",
        "location": "南宁市"
    },
    {
        "id": 14,
        "name": "中华人民共和国商务部",
        "type": "政府",
        "level": "中央",
        "parent": "中华人民共和国国务院",
        "location": "北京市"
    },
    {
        "id": 15,
        "name": "中共桂林市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广西壮族自治区委员会",
        "location": "桂林市"
    },
    {
        "id": 16,
        "name": "桂林市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广西壮族自治区人民政府",
        "location": "桂林市"
    },
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 李楚 — 北海市委书记 (2026.05-)
    {"person_id": 1, "org_id": 1, "title": "北海市委书记、北海军分区党委第一书记", "start_date": "2026-05", "end_date": "present", "rank": "正厅级", "note": "2026年5月由桂林市委书记转任"},
    # 李楚 — 桂林市委书记 (2024.12-2026.05)
    {"person_id": 1, "org_id": 15, "title": "桂林市委书记", "start_date": "2024-12", "end_date": "2026-05", "rank": "正厅级", "note": ""},
    # 李楚 — 桂林市市长 (2021.06-2025.04)
    {"person_id": 1, "org_id": 16, "title": "桂林市委副书记、市政府市长", "start_date": "2021-06", "end_date": "2025-04", "rank": "正厅级", "note": ""},
    # 李楚 — 共青团广西区委书记 (2017.05-2021.06)
    {"person_id": 1, "org_id": 13, "title": "共青团广西区委书记", "start_date": "2017-05", "end_date": "2021-06", "rank": "正厅级", "note": ""},
    # 李楚 — 河池市委常委、副市长 (2016.02-2017.05)
    {"person_id": 1, "org_id": 2, "title": "河池市委常委、市政府党组副书记、副市长", "start_date": "2016-02", "end_date": "2017-05", "rank": "副厅级", "note": "跨市调动至河池市"},
    # 李楚 — 河池市委常委、组织部部长 (2013.09-2016.02)
    {"person_id": 1, "org_id": 2, "title": "河池市委常委、组织部部长", "start_date": "2013-09", "end_date": "2016-02", "rank": "副厅级", "note": ""},
    # 李楚 — 柳州市委常委、三江县委书记 (2009.11-2013.08)
    {"person_id": 1, "org_id": 2, "title": "柳州市委常委、三江侗族自治县委书记", "start_date": "2009-11", "end_date": "2013-08", "rank": "副厅级", "note": ""},
    # 李楚 — 北流市委副书记、市长 (2009.01-2009.11)
    {"person_id": 1, "org_id": 2, "title": "北流市委副书记、市政府党组书记、市长", "start_date": "2009-01", "end_date": "2009-11", "rank": "正处级", "note": ""},
    # 李楚 — 玉林市委副秘书长 (2008.09-2009.01)
    {"person_id": 1, "org_id": 1, "title": "玉林市委副秘书长、办公室副主任（正处级）", "start_date": "2008-09", "end_date": "2009-01", "rank": "正处级", "note": ""},
    # 李楚 — 共青团玉林市委书记 (2004.07-2008.09)
    {"person_id": 1, "org_id": 13, "title": "共青团玉林市委书记", "start_date": "2004-07", "end_date": "2008-09", "rank": "正处级", "note": ""},
    # 李楚 — 北流市委常委、组织部部长 (2002.09-2004.07)
    {"person_id": 1, "org_id": 1, "title": "北流市委常委、组织部部长", "start_date": "2002-09", "end_date": "2004-07", "rank": "副处级", "note": ""},
    # 李楚 — 玉林市委组织部党政干部科科长 (2000.05-2002.09)
    {"person_id": 1, "org_id": 1, "title": "玉林市委组织部党政干部科科长", "start_date": "2000-05", "end_date": "2002-09", "rank": "正科级", "note": ""},
    # 李楚 — 玉林市委组织部干部一科副科长 (1998.03-2000.05)
    {"person_id": 1, "org_id": 1, "title": "玉林市委组织部干部一科副科长", "start_date": "1998-03", "end_date": "2000-05", "rank": "副科级", "note": ""},
    # 李楚 — 玉林地区外事办干部 (1995.07-1998.03)
    {"person_id": 1, "org_id": 2, "title": "玉林地区外事办（行署旅游局）干部", "start_date": "1995-07", "end_date": "1998-03", "rank": "科员", "note": "1996.09-1996.12 玉林地委组织部跟班学习"},
    
    # 李刚 — 北海市长 (2025.10-)
    {"person_id": 2, "org_id": 2, "title": "北海市委副书记、市政府市长、党组书记", "start_date": "2025-10", "end_date": "present", "rank": "正厅级", "note": "2025年10月17日当选"},
    # 李刚 — 北海代市长 (2025.10)
    {"person_id": 2, "org_id": 2, "title": "北海市委副书记、代市长", "start_date": "2025-10", "end_date": "2025-10", "rank": "正厅级", "note": "2025年10月11日任命"},
    # 李刚 — 北海市委副书记 (2025.09-2025.10)
    {"person_id": 2, "org_id": 1, "title": "北海市委副书记", "start_date": "2025-09", "end_date": "2025-10", "rank": "正厅级", "note": ""},
    # 李刚 — 商务部市场运行和消费促进司司长 (2024-2025)
    {"person_id": 2, "org_id": 14, "title": "商务部市场运行和消费促进司司长", "start_date": "2024", "end_date": "2025-09", "rank": "正司级", "note": ""},
    # 李刚 — 商务部流通业发展司司长 (2023-2024)
    {"person_id": 2, "org_id": 14, "title": "商务部流通业发展司司长", "start_date": "2023", "end_date": "2024", "rank": "正司级", "note": ""},
    # 李刚 — 商务部流通业发展司副司长
    {"person_id": 2, "org_id": 14, "title": "商务部流通业发展司副司长", "start_date": "待查", "end_date": "2023", "rank": "副司级", "note": ""},
    # 李刚 — 商务部市场体系建设司副巡视员/二级巡视员
    {"person_id": 2, "org_id": 14, "title": "商务部市场体系建设司副巡视员/二级巡视员", "start_date": "待查", "end_date": "待查", "rank": "司级", "note": ""},
    
    # 蔡锦军 — 自治区园区办主任 (2026.05-)
    {"person_id": 3, "org_id": 11, "title": "自治区园区办党组书记、主任", "start_date": "2026-05", "end_date": "present", "rank": "正厅级", "note": "另有任用"},
    # 蔡锦军 — 北海市委书记 (2021.01-2026.05)
    {"person_id": 3, "org_id": 1, "title": "北海市委书记", "start_date": "2021-01", "end_date": "2026-05", "rank": "正厅级", "note": "2021年1月接任"},
    # 蔡锦军 — 北海市长 (2018.02-2021.01)
    {"person_id": 3, "org_id": 2, "title": "北海市委副书记、市政府市长、党组书记", "start_date": "2018-02", "end_date": "2021-01", "rank": "正厅级", "note": ""},
    # 蔡锦军 — 自治区党委副秘书长 (2013.10-2018.01)
    {"person_id": 3, "org_id": 1, "title": "广西自治区党委副秘书长、办公厅副主任", "start_date": "2013-10", "end_date": "2018-01", "rank": "副厅级", "note": ""},
    # 蔡锦军 — 贵港市委常委、副市长 (2011.08-2013.10)
    {"person_id": 3, "org_id": 2, "title": "贵港市委常委、副市长、党组副书记", "start_date": "2011-08", "end_date": "2013-10", "rank": "副厅级", "note": ""},
    # 蔡锦军 — 贵港市委常委、政法委书记 (2008.11-2011.08)
    {"person_id": 3, "org_id": 9, "title": "贵港市委常委、政法委书记", "start_date": "2008-11", "end_date": "2011-08", "rank": "副厅级", "note": ""},
    # 蔡锦军 — 贵港市委常委、统战部部长 (2006.08-2008.11)
    {"person_id": 3, "org_id": 8, "title": "贵港市委常委、统战部部长", "start_date": "2006-08", "end_date": "2008-11", "rank": "副厅级", "note": ""},
    # 蔡锦军 — 北海市科技局局长 (2003.02-2006.08)
    {"person_id": 3, "org_id": 2, "title": "北海市科学技术局局长、党组书记", "start_date": "2003-02", "end_date": "2006-08", "rank": "正处级", "note": "兼工业园区管委会主任等"},
    # 蔡锦军 — 合浦县副县长 (2001.12-2003.02)
    {"person_id": 3, "org_id": 2, "title": "合浦县人民政府副县长", "start_date": "2001-12", "end_date": "2003-02", "rank": "副处级", "note": ""},
    # 蔡锦军 — 北海市委办公室副主任 (1998.11-2001.12)
    {"person_id": 3, "org_id": 1, "title": "北海市委办公室副主任", "start_date": "1998-11", "end_date": "2001-12", "rank": "副处级", "note": ""},
    # 蔡锦军 — 北海市委办综合科科长 (1996.04-1998.11)
    {"person_id": 3, "org_id": 1, "title": "北海市委办公室综合科科长", "start_date": "1996-04", "end_date": "1998-11", "rank": "正科级", "note": ""},
    # 蔡锦军 — 北海日报记者 (1993.07-1996.01)
    {"person_id": 3, "org_id": 2, "title": "《北海日报》社记者、新闻部副主任", "start_date": "1993-07", "end_date": "1996-01", "rank": "", "note": "1995.04-1996.01借调北海市委办公室"},
    
    # 陆海生 — 市人大常委会主任 (2024.02-)
    {"person_id": 4, "org_id": 3, "title": "北海市人大常委会主任", "start_date": "2024-02", "end_date": "present", "rank": "正厅级", "note": ""},
    # 陆海生 — 北海市委常委、统战部部长
    {"person_id": 4, "org_id": 8, "title": "北海市委常委、统战部部长，市政协党组副书记（兼）", "start_date": "2021", "end_date": "2024-02", "rank": "副厅级", "note": ""},
    
    # 蔡可辉 — 市政协主席 (2026.02-)
    {"person_id": 5, "org_id": 4, "title": "北海市政协主席", "start_date": "2026-02", "end_date": "present", "rank": "正厅级", "note": ""},
    # 蔡可辉 — 北海市委常委、政法委书记
    {"person_id": 5, "org_id": 9, "title": "北海市委常委、政法委书记", "start_date": "待查", "end_date": "2026-02", "rank": "副厅级", "note": ""},
    
    # 吕勇江 — 市委副书记、组织部部长
    {"person_id": 6, "org_id": 1, "title": "北海市委副书记、组织部部长，市委党校校长", "start_date": "2021-09", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 6, "title": "北海市委组织部部长", "start_date": "2021-09", "end_date": "present", "rank": "副厅级", "note": ""},
    
    # 黄毅 — 市纪委书记
    {"person_id": 7, "org_id": 5, "title": "北海市委常委、市纪委书记、市监委主任", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    
    # 黄宏瞻 — 常务副市长
    {"person_id": 8, "org_id": 2, "title": "北海市委常委、常务副市长", "start_date": "2025-03", "end_date": "present", "rank": "副厅级", "note": "2025年3月任副市长"},
    
    # 郑定雄 — 宣传部部长
    {"person_id": 9, "org_id": 7, "title": "北海市委常委、宣传部部长", "start_date": "2021-09", "end_date": "present", "rank": "副厅级", "note": "曾任市委秘书长"},
    
    # 龙起云 — 统战部部长、副市长
    {"person_id": 10, "org_id": 8, "title": "北海市委常委、统战部部长，市政府副市长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    
    # 麦成柱 — 市委秘书长
    {"person_id": 11, "org_id": 1, "title": "北海市委常委、秘书长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": "曾任北海市副市长"},
    
    # 杨斌 — 政法委书记
    {"person_id": 12, "org_id": 9, "title": "北海市委常委、政法委书记", "start_date": "2021-09", "end_date": "present", "rank": "副厅级", "note": "曾任北海银滩国家旅游度假区党工委书记（兼）"},
    
    # 沙卫良 — 军分区司令员
    {"person_id": 13, "org_id": 10, "title": "北海市委常委、北海军分区司令员", "start_date": "2021-09", "end_date": "present", "rank": "副厅级", "note": ""},
    
    # 李莉 — 前市长
    {"person_id": 14, "org_id": 2, "title": "北海市委副书记、市政府市长、党组书记", "start_date": "2022-01", "end_date": "2025-10", "rank": "正厅级", "note": "因工作变动辞去北海市长职务"},
    {"person_id": 14, "org_id": 12, "title": "自治区党委组织部分管日常工作的副部长", "start_date": "2025-10", "end_date": "present", "rank": "正厅级", "note": ""},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 李楚 ↔ 李刚 (书记—市长搭档)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "现任市委书记与市长搭档关系", "overlap_org": "中共北海市委员会/北海市人民政府", "overlap_period": "2026.05-"},
    # 李楚 ↔ 蔡锦军 (前任—继任)
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "李楚接替蔡锦军任北海市委书记", "overlap_org": "中共北海市委员会", "overlap_period": "2026.05"},
    # 李刚 ↔ 李莉 (前任—继任)
    {"person_a": 2, "person_b": 14, "type": "predecessor_successor", "context": "李刚接替李莉任北海市长", "overlap_org": "北海市人民政府", "overlap_period": "2025.10"},
    # 蔡锦军 ↔ 李莉 (前书记—前市长搭档)
    {"person_a": 3, "person_b": 14, "type": "overlap", "context": "蔡锦军任市委书记期间，李莉任市长", "overlap_org": "中共北海市委员会/北海市人民政府", "overlap_period": "2022.01-2025.10"},
    # 蔡锦军 ↔ 李刚 (书记—市长交班)
    {"person_a": 3, "person_b": 2, "type": "predecessor_successor", "context": "蔡锦军卸任书记与李刚接任市长有短暂工作交集", "overlap_org": "北海市人民政府/中共北海市委员会", "overlap_period": "2025.09-2025.10"},
    # 蔡锦军 → 陆海生 (前书记—人大主任)
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "蔡锦军任市委书记期间陆海生任市委常委", "overlap_org": "中共北海市委员会", "overlap_period": "2021-2024"},
    # 蔡锦军 ↔ 吕勇江 (书记—组织部长)
    {"person_a": 3, "person_b": 6, "type": "superior_subordinate", "context": "蔡锦军任书记期间吕勇江任组织部部长", "overlap_org": "中共北海市委员会", "overlap_period": "2021-2026"},
    # 蔡锦军 ↔ 黄宏瞻 (书记—常委副市长)
    {"person_a": 3, "person_b": 8, "type": "superior_subordinate", "context": "蔡锦军任书记期间黄宏瞻任副市长", "overlap_org": "中共北海市委员会", "overlap_period": "2025.03-2026.05"},
    # 蔡锦军 ↔ 郑定雄 (书记—宣传部长/秘书长)
    {"person_a": 3, "person_b": 9, "type": "superior_subordinate", "context": "蔡锦军任书记期间郑定雄先后任秘书长、宣传部部长", "overlap_org": "中共北海市委员会", "overlap_period": "2021-2026"},
    # 蔡锦军 ↔ 龙起云 (书记—副市长)
    {"person_a": 3, "person_b": 10, "type": "superior_subordinate", "context": "蔡锦军任书记期间龙起云任市委常委、副市长", "overlap_org": "中共北海市委员会", "overlap_period": "2021-2026"},
    # 蔡锦军 ↔ 杨斌 (书记—政法委书记)
    {"person_a": 3, "person_b": 12, "type": "superior_subordinate", "context": "蔡锦军任书记期间杨斌任政法委书记", "overlap_org": "中共北海市委员会", "overlap_period": "2021-2026"},
    # 蔡锦军 ↔ 麦成柱 (书记—副市长/秘书长)
    {"person_a": 3, "person_b": 11, "type": "superior_subordinate", "context": "蔡锦军任书记期间麦成柱先后任副市长、秘书长", "overlap_org": "中共北海市委员会/北海市人民政府", "overlap_period": "2021-2026"},
    # 李楚 ↔ 龙起云 (书记—副市长)
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "李楚任书记后龙起云继续任市委常委、副市长", "overlap_org": "中共北海市委员会/北海市人民政府", "overlap_period": "2026.05-"},
    # 李楚 ↔ 麦成柱 (书记—秘书长)
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "李楚任书记后麦成柱继续任市委常委、秘书长", "overlap_org": "中共北海市委员会", "overlap_period": "2026.05-"},
    # 李刚 ↔ 黄宏瞻 (市长—常务副市长)
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "李刚任市长后黄宏瞻任常务副市长", "overlap_org": "北海市人民政府", "overlap_period": "2025.10-"},
    # 黄毅 ↔ 蔡锦军 (纪委书记—书记)
    {"person_a": 7, "person_b": 3, "type": "superior_subordinate", "context": "纪委监督工作关系", "overlap_org": "中共北海市委员会", "overlap_period": "2021-2026"},
    # 吕勇江 ↔ 黄宏瞻 (组织—常务)
    {"person_a": 6, "person_b": 8, "type": "overlap", "context": "同为市委常委班子成员", "overlap_org": "中共北海市委员会", "overlap_period": "2025.03-"},
]

# =========================================================================
# 5. DATABASE
# =========================================================================
def create_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Persons
    cur.execute("""
        CREATE TABLE IF NOT EXISTS persons (
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
    
    # Organizations
    cur.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        )
    """)
    
    # Positions
    cur.execute("""
        CREATE TABLE IF NOT EXISTS positions (
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
    
    # Relationships
    cur.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
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
    
    # Insert data
    for p in persons:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"])
        )
    
    for o in organizations:
        cur.execute(
            "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
        )
    
    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"])
        )
    
    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
        )
    
    conn.commit()
    conn.close()
    
    print(f"✓ Database created: {DB_PATH}")
    print(f"  {len(persons)} persons")
    print(f"  {len(organizations)} organizations")
    print(f"  {len(positions)} positions")
    print(f"  {len(relationships)} relationships")


# =========================================================================
# 6. GEXF
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def create_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append(f'    <description>北海市领导班子工作关系网络 (as of {AS_OF})</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    
    # Node attributes
    lines.append('    <attributes class="node">')
    for attr_id, title, atype in [
        ("0", "type", "string"),
        ("1", "current_post", "string"),
        ("2", "current_org", "string"),
        ("3", "gender", "string"),
        ("4", "ethnicity", "string"),
        ("5", "birth", "string"),
        ("6", "birthplace", "string"),
        ("7", "source", "string"),
        ("8", "org_type", "string"),
        ("9", "level", "string"),
        ("10", "location", "string"),
    ]:
        lines.append(f'      <attribute id="{attr_id}" title="{title}" type="{atype}"/>')
    lines.append('    </attributes>')
    
    # Edge attributes
    lines.append('    <attributes class="edge">')
    for eid, title, etype in [
        ("0", "type", "string"),
        ("1", "context", "string"),
        ("2", "overlap_org", "string"),
        ("3", "overlap_period", "string"),
    ]:
        lines.append(f'      <attribute id="{eid}" title="{title}" type="{etype}"/>')
    lines.append('    </attributes>')
    
    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        post = p["current_post"]
        if "市委书记" in post:
            color = "255,50,50"
            size = "20.0"
        elif "市长" in post or "副市长" in post:
            color = "50,100,255"
            size = "20.0"
        elif "纪委书记" in post:
            color = "255,165,0"
            size = "12.0"
        else:
            color = "100,100,100"
            size = "12.0"
        
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["gender"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["ethnicity"])}"/>')
        lines.append(f'          <attvalue for="5" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="6" value="{esc(p["birthplace"])}"/>')
        lines.append(f'          <attvalue for="7" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append('      </node>')
    
    for o in organizations:
        org_type = o["type"]
        if org_type == "党委":
            ocolor = "255,200,200"
        elif org_type == "政府":
            ocolor = "200,200,255"
        elif org_type == "人大":
            ocolor = "200,255,255"
        elif org_type == "政协":
            ocolor = "255,240,200"
        elif org_type == "群团":
            ocolor = "255,220,255"
        else:
            ocolor = "220,220,220"
        
        oid = o["id"] + 100000
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="8" value="{esc(org_type)}"/>')
        lines.append(f'          <attvalue for="9" value="{esc(o["level"])}"/>')
        lines.append(f'          <attvalue for="10" value="{esc(o["location"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    
    # Edges
    lines.append('    <edges>')
    eid = 0
    
    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        pid = pos["person_id"]
        oid = pos["org_id"] + 100000
        lines.append(f'      <edge id="{eid}" source="p{pid}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start_date"])}~{esc(pos["end_date"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    
    # Person ↔ Person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    print(f"✓ GEXF created: {GEXF_PATH}")
    print(f"  {len(persons)} person nodes")
    print(f"  {len(organizations)} org nodes")
    print(f"  {eid} edges")


# =========================================================================
# 7. PERSON JSON
# =========================================================================
def write_person_json(person, filename_suffix, extra_entries=None):
    """Write a person graph JSON file."""
    fname = f"{AS_OF}-广西壮族自治区-北海市-{filename_suffix}-{person['name']}.json"
    fpath = os.path.join(PERSONS_DIR, fname)
    
    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "",
            "region": "北海市",
            "job": filename_suffix,
            "task_id": "guangxi_北海市",
            "time_focus": "2025-2026"
        },
        "identity": {
            "person_id": f"beihai_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": person["birthplace"],
            "education": [
                {
                    "summary": person["education"]
                }
            ],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "name_birthplace": f"{person['name']}_{person['birthplace']}"
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "No public risk signals found in available sources", "date": AS_OF, "confidence": "unverified", "source_ids": ["S001"]}
        ],
        "source_register": [
            {
                "id": "S001",
                "url": person["source"],
                "source_type": "encyclopedia",
                "reliability": "medium",
                "notes": "Primary source for identity"
            }
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "biggest_gap": ""
        },
        "open_questions": []
    }
    
    if extra_entries:
        if "career_timeline" in extra_entries:
            data["career_timeline"] = extra_entries["career_timeline"]
        if "relationships" in extra_entries:
            data["relationships"] = extra_entries["relationships"]
        if "governance_record" in extra_entries:
            data["governance_record"] = extra_entries["governance_record"]
        if "professional_profile" in extra_entries:
            data["professional_profile"].update(extra_entries["professional_profile"])
        if "open_questions" in extra_entries:
            data["open_questions"] = extra_entries["open_questions"]
        if "work_style_and_personality" in extra_entries:
            data["work_style_and_personality"]["public_style_indicators"] = extra_entries["work_style_and_personality"]
        if "source_register" in extra_entries:
            reg = data["source_register"]
            existing_ids = {s["id"] for s in reg}
            for s in extra_entries["source_register"]:
                if s["id"] not in existing_ids:
                    reg.append(s)
                    existing_ids.add(s["id"])
    
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Person JSON created: {fpath}")


# =========================================================================
# 8. MAIN
# =========================================================================
def main():
    print("=" * 60)
    print(f"  北海市领导班子工作关系网络 — 数据构建")
    print(f"  Date: {AS_OF}")
    print("=" * 60)
    
    create_db()
    print()
    create_gexf()
    print()
    
    # Person JSON: 李楚 (市委书记)
    li_chu_timeline = [
        {"start": "2026-05", "end": "present", "org": "中共北海市委员会", "title": "北海市委书记、北海军分区党委第一书记", "rank": "正厅级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2024-12", "end": "2026-05", "org": "中共桂林市委员会", "title": "桂林市委书记", "rank": "正厅级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2021-06", "end": "2025-04", "org": "桂林市人民政府", "title": "桂林市委副书记、市长、市政府党组书记", "rank": "正厅级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2017-05", "end": "2021-06", "org": "共青团广西壮族自治区委员会", "title": "共青团广西区委书记", "rank": "正厅级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2016-02", "end": "2017-05", "org": "河池市人民政府", "title": "河池市委常委、副市长、党组副书记", "rank": "副厅级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2013-09", "end": "2016-02", "org": "中共河池市委员会", "title": "河池市委常委、组织部部长", "rank": "副厅级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2009-11", "end": "2013-08", "org": "中共柳州市委员会", "title": "柳州市委常委、三江侗族自治县委书记", "rank": "副厅级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2009-01", "end": "2009-11", "org": "北流市人民政府", "title": "北流市委副书记、市长", "rank": "正处级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2008-09", "end": "2009-01", "org": "中共玉林市委员会", "title": "玉林市委副秘书长、办公室副主任（正处级）", "rank": "正处级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2004-07", "end": "2008-09", "org": "共青团玉林市委员会", "title": "共青团玉林市委书记", "rank": "正处级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2002-09", "end": "2004-07", "org": "中共北流市委员会", "title": "北流市委常委、组织部部长", "rank": "副处级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2000-05", "end": "2002-09", "org": "中共玉林市委组织部", "title": "党政干部科科长", "rank": "正科级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "1998-03", "end": "2000-05", "org": "中共玉林市委组织部", "title": "干部一科副科长", "rank": "副科级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "1995-07", "end": "1998-03", "org": "玉林地区外事办", "title": "干部", "rank": "科员", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    
    write_person_json(
        {"id": 1, "name": "李楚", "gender": "男", "ethnicity": "汉族", "birth": "1974年1月", "birthplace": "广西桂平", "education": "在职研究生学历，法学学士", "party_join": "1993年12月", "work_start": "1995年7月", "current_post": "北海市委书记、北海军分区党委第一书记", "current_org": "中共北海市委员会", "source": "https://baike.baidu.com/item/%E6%9D%8E%E6%A5%9A/13681350"},
        "市委书记",
        extra_entries={
            "career_timeline": li_chu_timeline,
            "professional_profile": {
                "primary_specializations": ["组织人事", "共青团", "地方治理"],
                "career_pattern": "cross_county_rotation",
                "systems_experience": ["party", "government", "youth_league"],
                "geographic_pattern": ["桂平", "玉林", "北流", "柳州", "河池", "桂林", "北海"]
            },
            "open_questions": [
                {"priority": "low", "question": "李楚的家庭背景和教育经历细节", "why_it_matters": "了解早期成长路径", "suggested_queries": ["李楚 家庭 背景"], "last_attempted": "2026-07-23"}
            ]
        }
    )
    
    # Person JSON: 李刚 (市长)
    li_gang_timeline = [
        {"start": "2025-10", "end": "present", "org": "北海市人民政府", "title": "北海市委副书记、市政府市长、党组书记", "rank": "正厅级", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"start": "2025-09", "end": "2025-10", "org": "中共北海市委员会", "title": "北海市委副书记", "rank": "正厅级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2024", "end": "2025-09", "org": "中华人民共和国商务部", "title": "商务部市场运行和消费促进司司长", "rank": "正司级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2023", "end": "2024", "org": "中华人民共和国商务部", "title": "商务部流通业发展司司长", "rank": "正司级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "2023", "org": "中华人民共和国商务部", "title": "商务部流通业发展司副司长", "rank": "副司级", "confidence": "plausible", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "中华人民共和国商务部", "title": "商务部市场体系建设司副巡视员/二级巡视员", "rank": "司级", "confidence": "plausible", "source_ids": ["S001"]},
    ]
    
    write_person_json(
        {"id": 2, "name": "李刚", "gender": "男", "ethnicity": "汉族", "birth": "1975年7月", "birthplace": "待查", "education": "研究生学历，经济学博士", "party_join": "中共党员", "work_start": "待查", "current_post": "北海市委副书记、市政府市长、党组书记", "current_org": "北海市人民政府", "source": "https://baike.baidu.com/item/%E6%9D%8E%E5%88%9A/22884963"},
        "市长",
        extra_entries={
            "career_timeline": li_gang_timeline,
            "professional_profile": {
                "primary_specializations": ["商贸流通", "市场运行", "经济管理"],
                "career_pattern": "provincial_department",
                "systems_experience": ["government", "commerce"],
                "geographic_pattern": ["北京", "北海"]
            },
            "open_questions": [
                {"priority": "high", "question": "李刚的早期教育背景和20年商务部内部详细职务履历", "why_it_matters": "全面了解其职业生涯轨迹", "suggested_queries": ["李刚 商务部 流通 历任 职务", "李刚 1975 北海 市长 早年 经历"], "last_attempted": "2026-07-23"},
                {"priority": "medium", "question": "李刚的籍贯和出生地", "why_it_matters": "身份基本信息", "suggested_queries": ["李刚 北海 市长 籍贯"], "last_attempted": "2026-07-23"}
            ]
        }
    )
    
    # Person JSON: 蔡锦军 (前书记)
    caijinjun_timeline = [
        {"start": "2026-05", "end": "present", "org": "广西壮族自治区产业园区改革发展办公室", "title": "党组书记、主任", "rank": "正厅级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2021-01", "end": "2026-05", "org": "中共北海市委员会", "title": "北海市委书记、北海军分区党委第一书记", "rank": "正厅级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2018-02", "end": "2021-01", "org": "北海市人民政府", "title": "北海市委副书记、市政府市长、党组书记", "rank": "正厅级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2013-10", "end": "2018-01", "org": "中共广西壮族自治区委员会", "title": "自治区党委副秘书长、办公厅副主任", "rank": "副厅级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2011-08", "end": "2013-10", "org": "贵港市人民政府", "title": "贵港市委常委、副市长、党组副书记", "rank": "副厅级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2008-11", "end": "2011-08", "org": "中共贵港市委员会", "title": "贵港市委常委、政法委书记", "rank": "副厅级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2006-08", "end": "2008-11", "org": "中共贵港市委员会", "title": "贵港市委常委、统战部部长", "rank": "副厅级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2004-05", "end": "2006-08", "org": "北海市科学技术局", "title": "北海市科技局局长、党组书记（兼工业园区管委会主任）", "rank": "正处级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2003-02", "end": "2004-05", "org": "北海市科学技术局", "title": "北海市科技局局长、党组书记", "rank": "正处级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2001-12", "end": "2003-02", "org": "合浦县人民政府", "title": "合浦县副县长", "rank": "副处级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "1998-11", "end": "2001-12", "org": "中共北海市委员会办公室", "title": "北海市委办公室副主任", "rank": "副处级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "1996-04", "end": "1998-11", "org": "中共北海市委员会办公室", "title": "综合科科长", "rank": "正科级", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "1993-07", "end": "1996-01", "org": "北海日报社", "title": "记者、新闻部副主任", "rank": "", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    
    write_person_json(
        {"id": 3, "name": "蔡锦军", "gender": "男", "ethnicity": "汉族", "birth": "1968年11月", "birthplace": "江西九江", "education": "研究生学历，文学硕士，高级管理人员工商管理硕士", "party_join": "1996年12月", "work_start": "1986年8月", "current_post": "自治区园区办党组书记、主任", "current_org": "广西壮族自治区产业园区改革发展办公室", "source": "https://baike.baidu.com/item/%E8%94%A1%E9%94%A6%E5%86%9B/3878047"},
        "前市委书记",
        extra_entries={
            "career_timeline": caijinjun_timeline,
            "professional_profile": {
                "primary_specializations": ["新闻传媒", "党委办公", "地方治理", "园区经济"],
                "career_pattern": "local_ladder",
                "systems_experience": ["party", "government", "media"],
                "geographic_pattern": ["九江", "北海", "贵港", "南宁"]
            },
            "open_questions": [
                {"priority": "low", "question": "蔡锦军1986-1993年（九江师范到广西师大研究生）期间的详细经历", "why_it_matters": "早期教育和工作经历", "suggested_queries": ["蔡锦军 九江师范 教师"], "last_attempted": "2026-07-23"}
            ]
        }
    )
    
    print()
    print("=" * 60)
    print("  Build complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
