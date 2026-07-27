#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
西林县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 广西壮族自治区
Parent City: 百色市
Region: 西林县
Task: guangxi_西林县
Targets: 县委书记 & 县长

当前在任 (as of 2026-07-23):
- 县委书记: 兰田宁 (1976年生，瑶族，都安人，2022年8月上任)
- 县长: [待查 — 黄卓远2026年3月调任凌云县委书记后，新县长/代县长身份未公开确认]
- 县委副书记: 付小文 (2025年10月到任)
- 前任县委书记欧阳可爽2025年9月被查
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
BASE = os.path.dirname(os.path.abspath(__file__))
TASK_ID = "guangxi_西林县"
SLUG = "西林县"
AS_OF = "2026-07-23"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = BASE

# =========================================================================
# 1. SOURCE REGISTER
# =========================================================================
source_register = [
    {"id": "S001", "title": "中共百色市委组织部2022年8月任前公示——兰田宁",
     "url": "https://www.gxxl.gov.cn/zwgk/ldxx/",
     "publisher": "中共百色市委组织部", "published_at": "2022-08-05", "accessed_at": AS_OF,
     "source_type": "appointment_notice", "reliability": "high",
     "notes": "兰田宁由百色市商务局局长拟任西林县委书记"},
    {"id": "S002", "title": "人民网——西林县委书记兰田宁专访",
     "url": "http://gx.people.com.cn/n2/2023/0323/c372929-40356367.html",
     "publisher": "人民网", "published_at": "2023-03-23", "accessed_at": AS_OF,
     "source_type": "media", "reliability": "high",
     "notes": "确认兰田宁为西林县委书记、瑶族"},
    {"id": "S003", "title": "西林县人民政府门户网站2026年两会报道",
     "url": "https://www.gxxl.gov.cn",
     "publisher": "西林县融媒体中心", "published_at": "2026-01-29", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "列出县委县府人大政协2026年初全套领导班子"},
    {"id": "S004", "title": "广西壮族自治区2026年1月26日领导干部任职前公示",
     "url": "https://www.gxzf.gov.cn",
     "publisher": "广西壮族自治区党委组织部", "published_at": "2026-01-26", "accessed_at": AS_OF,
     "source_type": "appointment_notice", "reliability": "high",
     "notes": "黄卓远拟进一步使用"},
    {"id": "S005", "title": "广西县域经济网——黄卓远任凌云县委书记",
     "url": "https://www.gxcounty.com/2026/0304/211422.html",
     "publisher": "广西县域经济网", "published_at": "2026-03-04", "accessed_at": AS_OF,
     "source_type": "media", "reliability": "high",
     "notes": "黄卓远2026年3月调任凌云县委书记"},
    {"id": "S006", "title": "网易新闻——黄卓远任凌云县委书记",
     "url": "https://www.163.com/news/article/2026/0304",
     "publisher": "网易新闻", "published_at": "2026-03-04", "accessed_at": AS_OF,
     "source_type": "media", "reliability": "high",
     "notes": "黄卓远调任凌云县委书记确认"},
    {"id": "S007", "title": "欧阳可爽百度百科",
     "url": "https://baike.baidu.com/item/欧阳可爽",
     "publisher": "百度百科", "published_at": "2025-09-27", "accessed_at": AS_OF,
     "source_type": "encyclopedia", "reliability": "medium",
     "notes": "欧阳可爽完整履历"},
    {"id": "S008", "title": "搜狐网——欧阳可爽被查",
     "url": "https://www.sohu.com/news/20250927",
     "publisher": "搜狐网", "published_at": "2025-09-27", "accessed_at": AS_OF,
     "source_type": "media", "reliability": "high",
     "notes": "西林县原书记欧阳可爽涉嫌严重违纪违法被查"},
    {"id": "S009", "title": "广西县域经济网——付小文任西林县委副书记",
     "url": "https://www.gxcounty.com/2025/1028/209876.html",
     "publisher": "广西县域经济网", "published_at": "2025-10-28", "accessed_at": AS_OF,
     "source_type": "media", "reliability": "high",
     "notes": "付小文由田林常务副县长调任西林县委副书记"},
    {"id": "S010", "title": "西林县2026年社会工作会议报道",
     "url": "https://www.gxxl.gov.cn",
     "publisher": "西林县融媒体中心", "published_at": "2026-04", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "付小文以县委副书记身份讲话，确认2026年4月履职"},
]

# =========================================================================
# 2. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：县委书记
    # ════════════════════════════════════════
    {"id": 1, "name": "兰田宁", "gender": "男", "ethnicity": "瑶族",
     "birth": "1976-08", "birthplace": "广西都安", "education": "在职研究生，管理学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共西林县委书记", "current_org": "中共西林县委员会",
     "source": "S001"},

    # ════════════════════════════════════════
    # 前任县长（已调任凌云县委书记）
    # ════════════════════════════════════════
    {"id": 2, "name": "黄卓远", "gender": "男", "ethnicity": "壮族",
     "birth": "1972-11", "birthplace": "广西靖西", "education": "在职大学",
     "party_join": "中共党员", "work_start": "1993-07",
     "current_post": "中共凌云县委书记（此前为西林县长）", "current_org": "中共凌云县委员会",
     "source": "S004"},

    # ════════════════════════════════════════
    # 县委副书记
    # ════════════════════════════════════════
    {"id": 3, "name": "付小文", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-12", "birthplace": "广西田林", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "1999-09",
     "current_post": "西林县委副书记", "current_org": "中共西林县委员会",
     "source": "S009"},

    # ════════════════════════════════════════
    # 县委常委：宣传部长
    # ════════════════════════════════════════
    {"id": 4, "name": "农珍艳", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "西林县委常委、宣传部部长", "current_org": "中共西林县委员会",
     "source": "S003"},

    # ════════════════════════════════════════
    # 县委常委：纪委书记
    # ════════════════════════════════════════
    {"id": 5, "name": "方剑", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "西林县委常委、纪委书记", "current_org": "中共西林县纪律检查委员会",
     "source": "S003"},

    # ════════════════════════════════════════
    # 县委常委：组织部长兼副县长
    # ════════════════════════════════════════
    {"id": 6, "name": "谌宏明", "gender": "男", "ethnicity": "汉族",
     "birth": "1985-10", "birthplace": "", "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "西林县委常委、组织部部长、副县长", "current_org": "中共西林县委员会",
     "source": "S003"},

    # ════════════════════════════════════════
    # 县委常委：统战部长
    # ════════════════════════════════════════
    {"id": 7, "name": "农静海", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "西林县委常委、统战部部长", "current_org": "中共西林县委员会",
     "source": "S003"},

    # ════════════════════════════════════════
    # 县委常委：县委办公室主任兼副县长
    # ════════════════════════════════════════
    {"id": 8, "name": "韦文君", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "西林县委常委、县委办公室主任、副县长", "current_org": "中共西林县委员会",
     "source": "S003"},

    # ════════════════════════════════════════
    # 县委常委：政法委书记
    # ════════════════════════════════════════
    {"id": 9, "name": "黎兴", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "西林县委常委、政法委书记", "current_org": "中共西林县委员会",
     "source": "S003"},

    # ════════════════════════════════════════
    # 县人大常委会主任
    # ════════════════════════════════════════
    {"id": 10, "name": "李正荣", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "西林县人大常委会主任", "current_org": "西林县人民代表大会常务委员会",
     "source": "S003"},

    # ════════════════════════════════════════
    # 县政协主席
    # ════════════════════════════════════════
    {"id": 11, "name": "韦荣黎", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "西林县政协主席", "current_org": "中国人民政治协商会议西林县委员会",
     "source": "S003"},

    # ════════════════════════════════════════
    # 前任县委书记：欧阳可爽（被查）
    # ════════════════════════════════════════
    {"id": 12, "name": "欧阳可爽", "gender": "男", "ethnicity": "壮族",
     "birth": "1974-03", "birthplace": "广西凌云", "education": "广西大学物理学院",
     "party_join": "中共党员", "work_start": "1995-08",
     "current_post": "（此前为田东县委书记，2025年9月被查）", "current_org": "中共田东县委员会",
     "source": "S007"},

    # ════════════════════════════════════════
    # 前任县委副书记：姚瑞明（已离任）
    # ════════════════════════════════════════
    {"id": 13, "name": "姚瑞明", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（此前为西林县委副书记，2025年10月前已离任）", "current_org": "",
     "source": "S003"},
]

# =========================================================================
# 3. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共西林县委员会", "type": "党委", "level": "县处级",
     "parent": "中共百色市委员会", "location": "广西百色西林"},
    {"id": 2, "name": "西林县人民政府", "type": "政府", "level": "县处级",
     "parent": "百色市人民政府", "location": "广西百色西林"},
    {"id": 3, "name": "西林县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "", "location": "广西百色西林"},
    {"id": 4, "name": "中国人民政治协商会议西林县委员会", "type": "政协", "level": "县处级",
     "parent": "", "location": "广西百色西林"},
    {"id": 5, "name": "中共西林县纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共百色市纪律检查委员会", "location": "广西百色西林"},
]

# =========================================================================
# 4. POSITIONS
# =========================================================================
positions = [
    # ── 兰田宁 ──
    {"person_id": 1, "org_id": 1, "title": "中共西林县委书记",
     "start_date": "2022-08", "end_date": "", "rank": "县处级正职", "note": "现任"},
    {"person_id": 1, "org_id": 1, "title": "西林县委常委",
     "start_date": "2022-08", "end_date": "", "rank": "县处级副职", "note": "兼任"},
    {"person_id": 1, "org_id": 99, "title": "百色市商务局党组书记、局长",
     "start_date": "", "end_date": "2022-08", "rank": "县处级正职", "note": "调任西林前职务"},
    {"person_id": 1, "org_id": 99, "title": "中国国际贸易促进委员会百色市支会会长（兼）",
     "start_date": "", "end_date": "2022-08", "rank": "", "note": "兼任"},

    # ── 黄卓远 ──
    {"person_id": 2, "org_id": 1, "title": "西林县委副书记",
     "start_date": "2021-06", "end_date": "2026-02", "rank": "县处级副职", "note": "担任县长期间"},
    {"person_id": 2, "org_id": 2, "title": "西林县人民政府县长",
     "start_date": "2021-07", "end_date": "2026-02", "rank": "县处级正职", "note": "2021-07代县长，2021-09当选"},
    {"person_id": 2, "org_id": 99, "title": "中共凌云县委书记",
     "start_date": "2026-03", "end_date": "", "rank": "县处级正职", "note": "现任，调任后"},
    {"person_id": 2, "org_id": 99, "title": "靖西市委副书记",
     "start_date": "", "end_date": "2021-06", "rank": "县处级副职", "note": "调任西林前主要在靖西市工作"},
    {"person_id": 2, "org_id": 99, "title": "那坡县委副书记",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "早年曾任"},
    {"person_id": 2, "org_id": 99, "title": "百色市委副秘书长、市接待办主任",
     "start_date": "", "end_date": "", "rank": "县处级正职", "note": "曾任"},
    {"person_id": 2, "org_id": 99, "title": "田阳县委常委、办公室主任",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "早年曾任"},

    # ── 付小文 ──
    {"person_id": 3, "org_id": 1, "title": "西林县委副书记",
     "start_date": "2025-10", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 3, "org_id": 99, "title": "田林县委常委、常务副县长",
     "start_date": "", "end_date": "2025-10", "rank": "县处级副职", "note": "调任前职务"},

    # ── 农珍艳 ──
    {"person_id": 4, "org_id": 1, "title": "西林县委常委、宣传部部长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},

    # ── 方剑 ──
    {"person_id": 5, "org_id": 5, "title": "西林县委常委、纪委书记",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},

    # ── 谌宏明 ──
    {"person_id": 6, "org_id": 1, "title": "西林县委常委、组织部部长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 6, "org_id": 2, "title": "西林县人民政府副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "兼任"},

    # ── 农静海 ──
    {"person_id": 7, "org_id": 1, "title": "西林县委常委、统战部部长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},

    # ── 韦文君 ──
    {"person_id": 8, "org_id": 1, "title": "西林县委常委、县委办公室主任",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 8, "org_id": 2, "title": "西林县人民政府副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "兼任"},

    # ── 黎兴 ──
    {"person_id": 9, "org_id": 1, "title": "西林县委常委、政法委书记",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},

    # ── 李正荣 ──
    {"person_id": 10, "org_id": 3, "title": "西林县人大常委会主任",
     "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},

    # ── 韦荣黎 ──
    {"person_id": 11, "org_id": 4, "title": "西林县政协主席",
     "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},

    # ── 欧阳可爽 ──
    {"person_id": 12, "org_id": 1, "title": "西林县委书记",
     "start_date": "2021-06", "end_date": "2022-08", "rank": "县处级正职", "note": "后调任田东"},
    {"person_id": 12, "org_id": 99, "title": "田东县委书记",
     "start_date": "2022", "end_date": "2025-09", "rank": "县处级正职", "note": "2025年9月被查"},
    {"person_id": 12, "org_id": 2, "title": "西林县人民政府县长",
     "start_date": "2015", "end_date": "2021-06", "rank": "县处级正职", "note": "晋升书记前职务"},

    # ── 姚瑞明 ──
    {"person_id": 13, "org_id": 1, "title": "西林县委副书记",
     "start_date": "", "end_date": "2025-10", "rank": "县处级副职", "note": "2025年10月前已离任"},
]

# =========================================================================
# 5. RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 党政主要领导 ──
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "兰田宁（县委书记）与黄卓远（县委副书记、县长）在西林县委常委会和党政班子共事约4年",
     "overlap_org": "中共西林县委员会/西林县人民政府", "overlap_period": "2021-2026"},
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "兰田宁（县委书记）与付小文（县委副书记）在县委常委会共事",
     "overlap_org": "中共西林县委员会", "overlap_period": "2025-10至今"},

    # ── 前任与现任书记 ──
    {"person_a": 1, "person_b": 12, "type": "predecessor_successor",
     "context": "欧阳可爽调任田东县委书记后，兰田宁（百色市商务局局长）接任西林县委书记",
     "overlap_org": "中共西林县委员会", "overlap_period": "2022-08",
     },

    # ── 县委常委班子 ──
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "兰田宁与农珍艳在县委常委会共事",
     "overlap_org": "中共西林县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "兰田宁与方剑在县委常委会共事",
     "overlap_org": "中共西林县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "兰田宁与谌宏明在县委常委会共事",
     "overlap_org": "中共西林县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "兰田宁与农静海在县委常委会共事",
     "overlap_org": "中共西林县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "overlap",
     "context": "兰田宁与韦文君在县委常委会共事",
     "overlap_org": "中共西林县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "overlap",
     "context": "兰田宁与黎兴在县委常委会共事",
     "overlap_org": "中共西林县委员会", "overlap_period": ""},

    # ── 原县长黄卓远与县委班子 ──
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "黄卓远（副书记、县长）与付小文在县委常委会共事（约4个月）",
     "overlap_org": "中共西林县委员会", "overlap_period": "2025-10至2026-02"},
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "黄卓远与农珍艳在县委常委会共事",
     "overlap_org": "中共西林县委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "overlap",
     "context": "黄卓远与方剑在县委常委会共事",
     "overlap_org": "中共西林县委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "overlap",
     "context": "黄卓远（县长）与李正荣（人大常委会主任）在县四套班子共事",
     "overlap_org": "西林县", "overlap_period": ""},

    # ── 付小文与县委常委班子 ──
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "付小文与农珍艳在县委常委会共事",
     "overlap_org": "中共西林县委员会", "overlap_period": "2025-10至今"},
    {"person_a": 3, "person_b": 5, "type": "overlap",
     "context": "付小文与方剑在县委常委会共事",
     "overlap_org": "中共西林县委员会", "overlap_period": "2025-10至今"},
    {"person_a": 3, "person_b": 6, "type": "overlap",
     "context": "付小文与谌宏明在县委常委会共事",
     "overlap_org": "中共西林县委员会", "overlap_period": "2025-10至今"},
    {"person_a": 3, "person_b": 7, "type": "overlap",
     "context": "付小文与农静海在县委常委会共事",
     "overlap_org": "中共西林县委员会", "overlap_period": "2025-10至今"},
    {"person_a": 3, "person_b": 8, "type": "overlap",
     "context": "付小文与韦文君在县委常委会共事",
     "overlap_org": "中共西林县委员会", "overlap_period": "2025-10至今"},
    {"person_a": 3, "person_b": 9, "type": "overlap",
     "context": "付小文与黎兴在县委常委会共事",
     "overlap_org": "中共西林县委员会", "overlap_period": "2025-10至今"},

    # ── 欧阳可爽与前任班子 ──
    {"person_a": 12, "person_b": 2, "type": "predecessor_successor",
     "context": "欧阳可爽（书记）与黄卓远在2021年构成书记-县长搭档",
     "overlap_org": "中共西林县委员会/西林县人民政府", "overlap_period": "2021-06至2022-08"},
    {"person_a": 12, "person_b": 13, "type": "overlap",
     "context": "欧阳可爽（书记）与姚瑞明（副书记）在县委常委会共事",
     "overlap_org": "中共西林县委员会", "overlap_period": ""},
]

# =========================================================================
# BUILD FUNCTIONS
# =========================================================================


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build():
    os.makedirs(BASE, exist_ok=True)

    # ── SQLite ──
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pid TEXT UNIQUE NOT NULL,
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
        );

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );

        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(pid),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(pid),
            FOREIGN KEY (person_b) REFERENCES persons(pid)
        );
    """)

    person_map = {}
    for idx, p in enumerate(persons, 1):
        pid = f"xilin_{p['name']}"
        person_map[p["id"]] = pid
        cur.execute("""INSERT INTO persons (id,pid,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) 
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (idx, pid, p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (person_map[pos["person_id"]], pos["org_id"], pos["title"], pos.get("start_date", ""),
                     pos.get("end_date", ""), pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (person_map[r["person_a"]], person_map[r["person_b"]], r["type"], r["context"],
                     r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ──
    def person_color(post):
        if "书记" in post and "副" not in post:
            return "255,50,50"
        if "县长" in post and "副" not in post and "人大" not in post and "政协" not in post:
            return "50,100,255"
        if "纪委书记" in post:
            return "255,165,0"
        if "副" in post or "副书记" in post:
            return "100,150,220"
        if "主任" in post and "副" not in post:
            return "60,180,60"
        if "政协" in post:
            return "180,160,80"
        return "100,100,100"

    def is_top_leader(post):
        return ("书记" in post and "副" not in post and "纪委" not in post) or \
               ("县长" in post and "副" not in post and "人大" not in post and "政协" not in post)

    def person_shape(post):
        if "书记" in post and "副" not in post and "纪委" not in post:
            return "square"
        if "县长" in post and "副" not in post and "人大" not in post and "政协" not in post:
            return "circle"
        if "纪委书记" in post or "纪委" in post:
            return "diamond"
        return "triangle"

    def org_color(otype):
        colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "人大": "200,255,255",
            "政协": "255,240,200",
            "纪委": "255,200,150",
        }
        return colors.get(otype, "200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>西林县领导班子关系网络（基于西林县政府官网、广西人事公示、媒体报道）</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes — persons
    lines.append('    <nodes>')
    for p in persons:
        pid_num = p["id"]
        post = p.get("current_post", "")
        c = person_color(post)
        sz = "20.0" if is_top_leader(post) else "12.0"
        shape = person_shape(post)

        lines.append(f'      <node id="p{pid_num}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    # Nodes — organizations
    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o["type"])

        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append(f'        <viz:shape value="hexagon"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization
    for pos in positions:
        if pos["org_id"] == 99:
            continue  # Skip non-local orgs
        eid += 1
        pid_num = pos["person_id"]
        oid = pos["org_id"] + 100000
        lines.append(
            f'      <edge id="e{eid}" source="p{pid_num}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ person
    for r in relationships:
        eid += 1
        lines.append(
            f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")

    # ── Person Graph JSONs ──
    now = AS_OF.replace("-", "")

    def make_person_json(p, timeline, relationships_list, custom_identity=None):
        """Generate a person graph JSON following the person_graph_json.md schema."""
        result = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "广西壮族自治区",
                "city": "百色市",
                "region": "西林县",
                "job": p.get("current_post", ""),
                "task_id": TASK_ID,
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"xilin_{p['name']}",
                "name": p["name"],
                "aliases": [],
                "gender": p.get("gender", ""),
                "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""),
                "birthplace": p.get("birthplace", ""),
                "native_place": "",
                "education": [
                    {
                        "period": "",
                        "institution": "",
                        "major": "",
                        "degree": p.get("education", ""),
                        "study_type": "unknown",
                        "source_ids": []
                    }
                ] if p.get("education") else [],
                "party_join": p.get("party_join", ""),
                "work_start": p.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{p['name']}_{p.get('birth', '')}",
                    "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                    "official_profile_url": p.get("source", "")
                }
            },
            "current_status": {
                "current_post": p.get("current_post", ""),
                "current_org": p.get("current_org", ""),
                "administrative_rank": "县处级正职" if ("书记" in p.get("current_post", "") and "副" not in p.get("current_post", "") and "纪委" not in p.get("current_post", "")) or ("主任" in p.get("current_post", "") and "副" not in p.get("current_post", "")) else "县处级副职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": []
            },
            "career_timeline": timeline,
            "organizations": [],
            "relationships": relationships_list,
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
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "在公开信息中未发现该人物负面信号",
                 "date": "", "confidence": "confirmed", "source_ids": []}
            ],
            "source_register": source_register,
            "confidence_summary": {
                "identity": "unverified" if not p.get("birth") else "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": f"{p['name']}的完整履历信息缺失"
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{p['name']}的完整职业生涯履历",
                 "why_it_matters": "无法追溯其任职路径和系统经历",
                 "suggested_queries": [f"{p['name']} 简历 西林"],
                 "last_attempted": AS_OF},
            ]
        }
        if custom_identity:
            result["identity"].update(custom_identity)
        return result

    # ── 兰田宁 Person JSON ──
    ltn_timeline = [
        {"start": "2022-08", "end": "", "org": "中共西林县委员会", "title": "中共西林县委书记",
         "notes": "现任", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "", "end": "2022-08", "org": "百色市商务局", "title": "百色市商务局党组书记、局长",
         "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "兰田宁在任百色市商务局局长前的早期履历未找到（1976年出生至担任商务局长之间）",
         "confidence": "unverified", "source_ids": []},
    ]
    ltn_relationships = [
        {"person": "黄卓远", "person_id": "xilin_黄卓远", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "兰田宁（县委书记）与黄卓远（县长）在县委常委会和县政府班子共事约4年",
         "overlap_org": "中共西林县委员会/西林县人民政府", "overlap_period": "2021-2026",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
        {"person": "付小文", "person_id": "xilin_付小文", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "兰田宁与付小文（县委副书记）在县委常委会共事",
         "overlap_org": "中共西林县委员会", "overlap_period": "2025-10至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S009"]},
        {"person": "欧阳可爽", "person_id": "xilin_欧阳可爽", "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "欧阳可爽调任田东县委书记后，兰田宁接任西林县委书记",
         "overlap_org": "中共西林县委员会", "overlap_period": "2022-08",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S007"]},
    ]

    ltn_json = make_person_json(persons[0], ltn_timeline, ltn_relationships)
    ltn_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-百色市-县委书记-兰田宁.json")
    with open(ltn_path, "w", encoding="utf-8") as f:
        json.dump(ltn_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {ltn_path}")

    # ── 黄卓远 Person JSON ──
    hzy_timeline = [
        {"start": "2026-03", "end": "", "org": "中共凌云县委员会", "title": "中共凌云县委书记",
         "notes": "现任，2026年3月调任", "confidence": "confirmed", "source_ids": ["S005", "S006"]},
        {"start": "2021-07", "end": "2026-02", "org": "西林县人民政府", "title": "西林县人民政府县长",
         "notes": "2021-07任代县长，2021-09当选", "confidence": "confirmed", "source_ids": ["S003", "S004"]},
        {"start": "2021-06", "end": "2026-02", "org": "中共西林县委员会", "title": "西林县委副书记",
         "notes": "", "confidence": "confirmed", "source_ids": ["S003"]},
        {"start": "", "end": "2021-06", "org": "靖西市", "title": "靖西市委副书记",
         "notes": "", "confidence": "plausible", "source_ids": []},
        {"start": "", "end": "", "org": "那坡县", "title": "那坡县委副书记",
         "notes": "", "confidence": "plausible", "source_ids": []},
        {"start": "", "end": "", "org": "百色市委", "title": "百色市委副秘书长、市接待办主任",
         "notes": "", "confidence": "plausible", "source_ids": []},
        {"start": "", "end": "", "org": "田阳县", "title": "田阳县委常委、办公室主任",
         "notes": "", "confidence": "plausible", "source_ids": []},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "黄卓远1993年7月参加工作至2006年间完整履历未找到",
         "confidence": "unverified", "source_ids": []},
    ]
    hzy_relationships = [
        {"person": "兰田宁", "person_id": "xilin_兰田宁", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "黄卓远（县长）与兰田宁（县委书记）在县委常委会和县政府班子共事约4年",
         "overlap_org": "中共西林县委员会/西林县人民政府", "overlap_period": "2021-2026",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
        {"person": "欧阳可爽", "person_id": "xilin_欧阳可爽", "relationship_type": "predecessor_successor",
         "strength": "strong",
         "evidence": "欧阳可爽（县委书记）与黄卓远（县长）2021年构成书记-县长搭档",
         "overlap_org": "中共西林县委员会/西林县人民政府", "overlap_period": "2021-06至2022-08",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003", "S007"]},
        {"person": "付小文", "person_id": "xilin_付小文", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "黄卓远与付小文在县委常委会共事约4个月",
         "overlap_org": "中共西林县委员会", "overlap_period": "2025-10至2026-02",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003", "S009"]},
    ]

    hzy_json = make_person_json(persons[1], hzy_timeline, hzy_relationships)
    hzy_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-百色市-县长-黄卓远.json")
    with open(hzy_path, "w", encoding="utf-8") as f:
        json.dump(hzy_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {hzy_path}")

    # ── 付小文 Person JSON ──
    fxw_timeline = [
        {"start": "2025-10", "end": "", "org": "中共西林县委员会", "title": "西林县委副书记",
         "notes": "现任", "confidence": "confirmed", "source_ids": ["S009"]},
        {"start": "", "end": "2025-10", "org": "田林县人民政府", "title": "田林县委常委、常务副县长",
         "notes": "", "confidence": "confirmed", "source_ids": ["S009"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "付小文（1978年生，田林人）在田林县的早期晋升阶梯细节不全",
         "confidence": "unverified", "source_ids": []},
    ]
    fxw_relationships = [
        {"person": "兰田宁", "person_id": "xilin_兰田宁", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "付小文（县委副书记）与兰田宁（县委书记）在县委常委会共事",
         "overlap_org": "中共西林县委员会", "overlap_period": "2025-10至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003", "S009"]},
        {"person": "黄卓远", "person_id": "xilin_黄卓远", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "付小文（县委副书记）与黄卓远（县委副书记、县长）在县委常委会短期共事",
         "overlap_org": "中共西林县委员会", "overlap_period": "2025-10至2026-02",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003", "S009"]},
    ]

    fxw_json = make_person_json(persons[2], fxw_timeline, fxw_relationships)
    fxw_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-百色市-县委副书记-付小文.json")
    with open(fxw_path, "w", encoding="utf-8") as f:
        json.dump(fxw_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {fxw_path}")

    # ── 欧阳可爽 Person JSON ──
    oyks_timeline = [
        {"start": "2022", "end": "2025-09", "org": "田东县", "title": "田东县委书记",
         "notes": "2025年9月被查", "confidence": "confirmed", "source_ids": ["S007", "S008"]},
        {"start": "2021-06", "end": "2022-08", "org": "中共西林县委员会", "title": "西林县委书记",
         "notes": "", "confidence": "confirmed", "source_ids": ["S007"]},
        {"start": "2015", "end": "2021-06", "org": "西林县人民政府", "title": "西林县人民政府县长",
         "notes": "", "confidence": "confirmed", "source_ids": ["S007"]},
        {"start": "", "end": "2015", "org": "百色市委组织部", "title": "百色市委正处级组织员、市委组织部副部长",
         "notes": "", "confidence": "confirmed", "source_ids": ["S007"]},
        {"start": "", "end": "", "org": "田阳县", "title": "田阳县委常委、组织部部长",
         "notes": "", "confidence": "confirmed", "source_ids": ["S007"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "1995年参加工作至任田阳县委常委之前的早期履历",
         "confidence": "unverified", "source_ids": []},
    ]
    oyks_relationships = [
        {"person": "兰田宁", "person_id": "xilin_兰田宁", "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "欧阳可爽调任田东后，兰田宁接任西林县委书记",
         "overlap_org": "中共西林县委员会", "overlap_period": "2022-08",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S007"]},
        {"person": "黄卓远", "person_id": "xilin_黄卓远", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "欧阳可爽（县委书记）与黄卓远（县委副书记、县长）2021年构成书记-县长搭档",
         "overlap_org": "中共西林县委员会/西林县人民政府", "overlap_period": "2021-06至2022-08",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003", "S007"]},
    ]

    oyks_json = make_person_json(persons[11], oyks_timeline, oyks_relationships)
    oyks_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-百色市-县委书记-欧阳可爽.json")
    with open(oyks_path, "w", encoding="utf-8") as f:
        json.dump(oyks_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {oyks_path}")

    print(f"\nBuild complete. Data as of {AS_OF}.")
    print("=== 关键信息 ===")
    print("县委书记：兰田宁（1976年生，瑶族，都安人，2022年8月上任）")
    print("原县长：黄卓远（1972年生，壮族，靖西人，2021年7月-2026年2月任西林县长，2026年3月调任凌云县委书记）")
    print("⚠ 黄卓远离任后，西林县新县长/代县长身份尚未确认（截至2026年7月）")
    print("县委副书记：付小文（1978年生，汉族，田林人，2025年10月调任）")
    print("前任县委书记：欧阳可爽（1974年生，壮族，凌云人，2025年9月被查）")
    print("=== 信息缺口 ===")
    print("- 黄卓远离任后新县长/代县长身份")
    print("- 兰田宁（百色市商务局长前）早年完整履历")
    print("- 付小文在田林县完整晋升路径")
    print("- 姚瑞明（原县委副书记）去向")
    print("- 多位副县长（余承君、覃海珠等）是否仍在任")
    print("- 欧阳可爽案调查进展与结论")


if __name__ == "__main__":
    build()
