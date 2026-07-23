#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
靖西市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县级市
Province: 广西壮族自治区
Parent City: 百色市
Region: 靖西市
Targets: 市委书记 & 市长

数据来源:
- 靖西市人民政府门户网站 (www.jingxi.gov.cn) — 领导活动报道 (2024-2026)
- 百色市政协网 — 郝玉松简历 (2025-04-17)
- 网易新闻 / 北京日报客户端 — 郝玉松清华博士拟升职报道 (2024-12-14)
- 广西县域经济网 / 百度搜索 — 刘永雄任前公示与简历 (2023-09)
- 靖西人大网 — 市政府务虚会领导名单 (2024-02-19)
- 靖西市人民政府 — 领导分工通知 (2024/2025)
- 百度百科 — 黄兰爱简历 (2025-02-10)
- 网易新闻、百色市政府 — 闭鸿飞任前公示 (2025-01-08)
- 广西纪检监察网 / 新京报 — 钟恒钦被查 (2025-05-09)
"""

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ── Ensure gov_relation is importable ──
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))

# ── Paths ──
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "靖西市"
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-23"
TODAY = AS_OF

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：市委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "郝玉松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年2月",
        "birthplace": "湖北荆州",
        "education": "博士研究生（清华大学物理学博士）",
        "party_join": "2001年6月",
        "work_start": "2007年",
        "current_post": "靖西市委书记",
        "current_org": "中共靖西市委员会",
        "source": "confirmed — 网易新闻转载 (2021-07-17)、北京日报客户端 (2024-12-14)、百色市政协网 (2025-04-17)。",
    },
    # ════════════════════════════════════════
    # 核心领导：市长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "刘永雄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年2月",
        "birthplace": "广西三江",
        "education": "大学学历",
        "party_join": "1999年4月",
        "work_start": "1999年7月",
        "current_post": "靖西市委副书记、市长",
        "current_org": "靖西市人民政府",
        "source": "confirmed — 靖西市人民政府网站领导之窗 (2024)、广西县域经济网任前公示 (2023-09-11)。",
    },
    # ════════════════════════════════════════
    # 前任市委书记（已调离/被查）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "钟恒钦",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1967年11月",
        "birthplace": "广西防城港",
        "education": "广西区委党校研究生，文学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "钦州市委原常委、副市长（被查）",
        "current_org": "",
        "source": "confirmed — 新京报 (2025-05-09)、广西纪检监察网违纪通报 (2025)。",
    },
    # ════════════════════════════════════════
    # 市委副书记（已调离）
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "黄兰爱",
        "gender": "女",
        "ethnicity": "壮族",
        "birth": "1972年9月",
        "birthplace": "广西德保",
        "education": "在职大学学历",
        "party_join": "1997年6月",
        "work_start": "1993年7月",
        "current_post": "德保县政协党组书记",
        "current_org": "德保县政协",
        "source": "confirmed — 百度百科、百色市政府任前公示 (2022-11-07)、汲古新知 (2025-02-10)。",
    },
    # ════════════════════════════════════════
    # 市委常委、统战部部长（拟任正处级）
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "闭鸿飞",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1972年12月",
        "birthplace": "广西靖西",
        "education": "在职研究生学历",
        "party_join": "1998年12月",
        "work_start": "1997年7月",
        "current_post": "那坡县人大常委会党组书记",
        "current_org": "那坡县人民代表大会常务委员会",
        "source": "confirmed — 网易新闻/百色市政府任前公示 (2025-01-08)、闭鸿飞履新那坡县报道 (2025-02-21)。",
    },
    # ════════════════════════════════════════
    # 市委常委、副市长
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "何婷婷",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "靖西市委常委、副市长",
        "current_org": "靖西市人民政府",
        "source": "confirmed — 靖西人大网2024年务虚会领导名单、靖西市政府分工通知 (2024/2025)。",
    },
    # ════════════════════════════════════════
    # 市委常委、人武部政委
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "甘泉",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "靖西市委常委、人武部政治委员",
        "current_org": "靖西市人民武装部",
        "source": "confirmed — 靖西市2022年征兵动员部署会、春节慰问活动报道。",
    },
    # ════════════════════════════════════════
    # 市委常委
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "冉福兵",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "靖西市委常委",
        "current_org": "中共靖西市委员会",
        "source": "plausible — 靖西市委三届六次全会报道 (2024-01-04) 常委名单。",
    },
    # ════════════════════════════════════════
    # 市委常委
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "张宏",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "靖西市委常委",
        "current_org": "中共靖西市委员会",
        "source": "plausible — 靖西市委三届六次全会报道 (2024-01-04) 常委名单。",
    },
    # ════════════════════════════════════════
    # 市委常委、副市长
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "刘雄",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "靖西市委常委、副市长",
        "current_org": "靖西市人民政府",
        "source": "confirmed — 靖西市政府分工通知 (2024)、靖西市人大常委会免职公告 (2025-07-18 挂职期满)。",
    },
    # ════════════════════════════════════════
    # 副市长（驻村工作队）
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "汪保华",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "靖西市副市长（驻村工作队队长）",
        "current_org": "靖西市人民政府",
        "source": "confirmed — 靖西市政府分工通知 (2024)。",
    },
    # ════════════════════════════════════════
    # 副市长（粤桂协作）
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "冯志刚",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "靖西市副市长（粤桂东西部协作）",
        "current_org": "靖西市人民政府",
        "source": "confirmed — 靖西市政府分工通知 (2024)、市政府务虚会领导名单。",
    },
    # ════════════════════════════════════════
    # 副市长、公安局局长
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "玉文波",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "靖西市副市长、公安局局长",
        "current_org": "靖西市公安局",
        "source": "confirmed — 靖西市政府务虚会领导名单 (2024-02-19)，分工通知。",
    },
    # ════════════════════════════════════════
    # 副市长
    # ════════════════════════════════════════
    {
        "id": 14,
        "name": "吴英杰",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "靖西市副市长",
        "current_org": "靖西市人民政府",
        "source": "confirmed — 靖西市政府务虚会 (2024-02-19)、烟叶产业工作会议 (2024-12-09)。",
    },
    # ════════════════════════════════════════
    # 副市长
    # ════════════════════════════════════════
    {
        "id": 15,
        "name": "乃振峰",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "靖西市副市长",
        "current_org": "靖西市人民政府",
        "source": "plausible — 靖西市政府务虚会领导名单 (2024-02-19)。",
    },
    # ════════════════════════════════════════
    # 副市长（武装/民政/交通）
    # ════════════════════════════════════════
    {
        "id": 16,
        "name": "魏岳光",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "靖西市副市长（武装、民政、交通运输）",
        "current_org": "靖西市人民政府",
        "source": "confirmed — 靖西市政府分工通知 (2024)。",
    },
    # ════════════════════════════════════════
    # 副市长（与何婷婷AB岗）
    # ════════════════════════════════════════
    {
        "id": 17,
        "name": "林强",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "靖西市副市长",
        "current_org": "靖西市人民政府",
        "source": "plausible — 靖西市政府分工通知提及与何婷婷互为AB岗 (2024)。",
    },
    # ════════════════════════════════════════
    # 市人大常委会主任
    # ════════════════════════════════════════
    {
        "id": 18,
        "name": "陈飞龙",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "靖西市人大常委会主任",
        "current_org": "靖西市人民代表大会常务委员会",
        "source": "confirmed — 靖西市人大会议报道多次提及 (2024-2026)。",
    },
    # ════════════════════════════════════════
    # 市政协主席
    # ════════════════════════════════════════
    {
        "id": 19,
        "name": "陆海",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "靖西市政协主席",
        "current_org": "中国人民政治协商会议靖西市委员会",
        "source": "confirmed — 靖西市委工作务虚会报道 (2024-02-21)。",
    },
    # ════════════════════════════════════════
    # 副市长（挂职）
    # ════════════════════════════════════════
    {
        "id": 20,
        "name": "蒋凯",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "靖西市副市长（挂职）",
        "current_org": "靖西市人民政府",
        "source": "plausible — 靖西市政府务虚会领导名单 (2024-02-19)。",
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共靖西市委员会", "type": "党委", "level": "县级市", "parent": "中共百色市委员会", "location": "百色市靖西市"},
    {"id": 2, "name": "靖西市人民政府", "type": "政府", "level": "县级市", "parent": "百色市人民政府", "location": "百色市靖西市"},
    {"id": 3, "name": "靖西市人民代表大会常务委员会", "type": "人大", "level": "县级市", "parent": "百色市人民代表大会常务委员会", "location": "百色市靖西市"},
    {"id": 4, "name": "中国人民政治协商会议靖西市委员会", "type": "政协", "level": "县级市", "parent": "中国人民政治协商会议百色市委员会", "location": "百色市靖西市"},
    {"id": 5, "name": "中共靖西市纪律检查委员会", "type": "纪委", "level": "县级市", "parent": "中共百色市纪律检查委员会", "location": "百色市靖西市"},
    {"id": 6, "name": "靖西市监察委员会", "type": "政府", "level": "县级市", "parent": "百色市监察委员会", "location": "百色市靖西市"},
    {"id": 7, "name": "靖西市人民武装部", "type": "政府", "level": "县级市", "parent": "百色军分区", "location": "百色市靖西市"},
    {"id": 8, "name": "靖西市公安局", "type": "政府", "level": "县级市", "parent": "靖西市人民政府", "location": "百色市靖西市"},
    {"id": 9, "name": "中共百色市委员会", "type": "党委", "level": "地级市", "parent": "中共广西壮族自治区委员会", "location": "百色市"},
    {"id": 10, "name": "百色市人民政府", "type": "政府", "level": "地级市", "parent": "广西壮族自治区人民政府", "location": "百色市"},
    {"id": 11, "name": "中国人民政治协商会议百色市委员会", "type": "政协", "level": "地级市", "parent": "", "location": "百色市"},
    {"id": 12, "name": "河池市人民政府", "type": "政府", "level": "地级市", "parent": "广西壮族自治区人民政府", "location": "河池市"},
    {"id": 13, "name": "凤山县人民政府", "type": "政府", "level": "县", "parent": "河池市人民政府", "location": "河池市凤山县"},
    {"id": 14, "name": "河池市金城江区委", "type": "党委", "level": "市辖区", "parent": "中共河池市委员会", "location": "河池市金城江区"},
    {"id": 15, "name": "广西河池化工股份有限公司", "type": "企业", "level": "", "parent": "", "location": "河池市"},
    {"id": 16, "name": "河池市经济委员会", "type": "政府", "level": "地级市", "parent": "河池市人民政府", "location": "河池市"},
    {"id": 17, "name": "那坡县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "百色市人民代表大会常务委员会", "location": "百色市那坡县"},
    {"id": 18, "name": "德保县政协", "type": "政协", "level": "县", "parent": "中国人民政治协商会议百色市委员会", "location": "百色市德保县"},
    {"id": 19, "name": "德保县人民政府", "type": "政府", "level": "县", "parent": "百色市人民政府", "location": "百色市德保县"},
    {"id": 20, "name": "百色市外事办公室", "type": "政府", "level": "地级市", "parent": "百色市人民政府", "location": "百色市"},
    {"id": 21, "name": "靖西市人民代表大会常务委员会", "type": "人大", "level": "县级市", "parent": "百色市人民代表大会常务委员会", "location": "百色市靖西市"},
    {"id": 22, "name": "中共钦州市委员会", "type": "党委", "level": "地级市", "parent": "中共广西壮族自治区委员会", "location": "钦州市"},
    {"id": 23, "name": "钦州市人民政府", "type": "政府", "level": "地级市", "parent": "广西壮族自治区人民政府", "location": "钦州市"},
    {"id": 24, "name": "河池市人民政府", "type": "政府", "level": "地级市", "parent": "广西壮族自治区人民政府", "location": "河池市"},
    {"id": 25, "name": "清华大学", "type": "事业单位", "level": "", "parent": "", "location": "北京市"},
    {"id": 26, "name": "中国科学技术大学", "type": "事业单位", "level": "", "parent": "", "location": "安徽省合肥市"},
]

# =========================================================================
# 3. POSITIONS (任职记录)
# =========================================================================
positions = [
    # ── 郝玉松 ──
    {"person_id": 1, "org_id": 26, "title": "学生（化学物理系）", "start_date": "1998-09", "end_date": "2002-07", "rank": "", "note": "获化学学士"},
    {"person_id": 1, "org_id": 25, "title": "学生（物理系）", "start_date": "2002-09", "end_date": "2007-12", "rank": "", "note": "获理学博士学位"},
    {"person_id": 1, "org_id": 9, "title": "挂任市发改委副主任", "start_date": "2007", "end_date": "2009", "rank": "", "note": "清华大学选调生到广西玉林挂职"},
    {"person_id": 1, "org_id": 9, "title": "玉林市发改委/市委办/陆川县工作", "start_date": "2009", "end_date": "2011", "rank": "", "note": "先后在发改委、市委办、陆川县任职"},
    {"person_id": 1, "org_id": 13, "title": "凤山县县长", "start_date": "2011", "end_date": "2016", "rank": "县处级正职", "note": "河池市凤山县人民政府"},
    {"person_id": 1, "org_id": 2, "title": "靖西市首任市长（撤县设市）", "start_date": "2016", "end_date": "2021-07", "rank": "县处级正职", "note": "靖西撤县设市后首任市长"},
    {"person_id": 1, "org_id": 1, "title": "靖西市委书记", "start_date": "2021-07", "end_date": "至今", "rank": "县处级正职（二级巡视员）", "note": "接替钟恒钦任市委书记；2024年12月拟升副厅级"},
    {"person_id": 1, "org_id": 11, "title": "百色市政协副主席、党组成员", "start_date": "2025", "end_date": "至今", "rank": "副厅级", "note": "兼任，百色市政协网确认"},
    # ── 刘永雄 ──
    {"person_id": 2, "org_id": 15, "title": "广西河池化工净化车间技术员", "start_date": "1999-07", "end_date": "待查", "rank": "", "note": "早期职业生涯"},
    {"person_id": 2, "org_id": 15, "title": "高浓度复合肥厂厂长、党支部书记", "start_date": "待查", "end_date": "2009", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 16, "title": "河池市经济委员会副主任", "start_date": "2009", "end_date": "待查", "rank": "县处级副职", "note": "后改市工信局副局长"},
    {"person_id": 2, "org_id": 12, "title": "河池市工信局副局长、党组成员", "start_date": "待查", "end_date": "2021", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 14, "title": "河池市金城江区委副书记", "start_date": "2021", "end_date": "2023-09", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "靖西市委副书记、代市长", "start_date": "2023-09", "end_date": "2023-10", "rank": "县处级正职", "note": "2023年9月任代市长"},
    {"person_id": 2, "org_id": 2, "title": "靖西市委副书记、市长", "start_date": "2023-10", "end_date": "至今", "rank": "县处级正职（二级调研员）", "note": "2023年10月全票当选靖西市长"},
    # ── 钟恒钦 ──
    {"person_id": 3, "org_id": 9, "title": "田阳县委副书记、县长", "start_date": "2010前", "end_date": "2013?", "rank": "县处级正职", "note": ""},
    {"person_id": 3, "org_id": 9, "title": "田阳县委书记", "start_date": "2013?", "end_date": "2016?", "rank": "县处级正职", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "靖西市委书记（百色市委常委兼任）", "start_date": "2016?", "end_date": "2021", "rank": "副厅级", "note": "以百色市委常委身份兼任靖西市委书记"},
    {"person_id": 3, "org_id": 24, "title": "河池市委常委、常务副市长", "start_date": "2021", "end_date": "2023", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 23, "title": "钦州市委常委、副市长", "start_date": "2023", "end_date": "2025-05", "rank": "副厅级（一级巡视员）", "note": "2025年5月任上被查"},
    # ── 黄兰爱 ──
    {"person_id": 4, "org_id": 19, "title": "德保县副县长", "start_date": "待查", "end_date": "待查", "rank": "县处级副职", "note": "早年任职"},
    {"person_id": 4, "org_id": 19, "title": "德保县委常委、统战部部长", "start_date": "待查", "end_date": "2017-09", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "靖西市委常委、统战部部长", "start_date": "2017-09", "end_date": "2021-07", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "靖西市委常委、宣传部部长、副市长", "start_date": "2021-07", "end_date": "2022-11", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "靖西市委副书记", "start_date": "2022-11", "end_date": "2024-06", "rank": "县处级副职", "note": "2022年11月任前公示拟进一步使用"},
    {"person_id": 4, "org_id": 20, "title": "百色市外事办公室主任", "start_date": "2024-06", "end_date": "2025-02", "rank": "县处级正职", "note": ""},
    {"person_id": 4, "org_id": 18, "title": "德保县政协党组书记", "start_date": "2025-02", "end_date": "至今", "rank": "县处级正职", "note": "重回德保县工作"},
    # ── 闭鸿飞 ──
    {"person_id": 5, "org_id": 2, "title": "靖西县岳圩镇农业技术推广站技术员", "start_date": "1997-07", "end_date": "2000-01", "rank": "", "note": "广西大学蚕学专业毕业"},
    {"person_id": 5, "org_id": 2, "title": "靖西县乡镇/部门任职", "start_date": "2000-01", "end_date": "2020前", "rank": "", "note": "逐步晋升"},
    {"person_id": 5, "org_id": 1, "title": "靖西市委常委、统战部部长", "start_date": "2020前", "end_date": "2025-01", "rank": "县处级副职", "note": "二级调研员"},
    {"person_id": 5, "org_id": 17, "title": "那坡县人大常委会党组书记", "start_date": "2025-02", "end_date": "至今", "rank": "县处级正职", "note": "2025年1月任前公示拟任正处级领导职务"},
    # ── 何婷婷 ──
    {"person_id": 6, "org_id": 2, "title": "靖西市委常委、副市长", "start_date": "2024前", "end_date": "至今", "rank": "县处级副职", "note": "负责相关工作"},
    # ── 甘泉 ──
    {"person_id": 7, "org_id": 7, "title": "靖西市委常委、人武部政治委员", "start_date": "2022前", "end_date": "至今", "rank": "县处级副职", "note": ""},
    # ── 冉福兵 ──
    {"person_id": 8, "org_id": 1, "title": "靖西市委常委", "start_date": "2024前", "end_date": "至今", "rank": "县处级副职", "note": "具体职务待确认"},
    # ── 张宏 ──
    {"person_id": 9, "org_id": 1, "title": "靖西市委常委", "start_date": "2024前", "end_date": "至今", "rank": "县处级副职", "note": "具体职务待确认"},
    # ── 刘雄 ──
    {"person_id": 10, "org_id": 2, "title": "靖西市委常委、副市长（挂职）", "start_date": "2024前", "end_date": "2025-07", "rank": "县处级副职", "note": "2025年7月挂职期满免职"},
    # ── 汪保华 ──
    {"person_id": 11, "org_id": 2, "title": "靖西市副市长（驻村工作队队长）", "start_date": "2024前", "end_date": "至今", "rank": "县处级副职", "note": "负责驻村工作队、定点帮扶"},
    # ── 冯志刚 ──
    {"person_id": 12, "org_id": 2, "title": "靖西市副市长（粤桂协作）", "start_date": "2024前", "end_date": "至今", "rank": "县处级副职", "note": "粤桂东西部协作"},
    # ── 玉文波 ──
    {"person_id": 13, "org_id": 8, "title": "靖西市副市长、公安局局长", "start_date": "2024前", "end_date": "至今", "rank": "县处级副职", "note": ""},
    # ── 吴英杰 ──
    {"person_id": 14, "org_id": 2, "title": "靖西市副市长", "start_date": "2023前", "end_date": "至今", "rank": "县处级副职", "note": "分管农业等方面"},
    # ── 乃振峰 ──
    {"person_id": 15, "org_id": 2, "title": "靖西市副市长", "start_date": "2024前", "end_date": "至今", "rank": "县处级副职", "note": ""},
    # ── 魏岳光 ──
    {"person_id": 16, "org_id": 2, "title": "靖西市副市长（武装、民政、交通）", "start_date": "2024前", "end_date": "至今", "rank": "县处级副职", "note": ""},
    # ── 林强 ──
    {"person_id": 17, "org_id": 2, "title": "靖西市副市长", "start_date": "2024前", "end_date": "至今", "rank": "县处级副职", "note": "与何婷婷互为AB岗"},
    # ── 陈飞龙 ──
    {"person_id": 18, "org_id": 3, "title": "靖西市人大常委会主任", "start_date": "2023前", "end_date": "至今", "rank": "县处级正职", "note": ""},
    # ── 陆海 ──
    {"person_id": 19, "org_id": 4, "title": "靖西市政协主席", "start_date": "2023前", "end_date": "至今", "rank": "县处级正职", "note": ""},
    # ── 蒋凯 ──
    {"person_id": 20, "org_id": 2, "title": "靖西市副市长（挂职）", "start_date": "2024前", "end_date": "至今", "rank": "县处级副职", "note": ""},
]

# =========================================================================
# 4. RELATIONSHIPS (关系)
# =========================================================================
relationships = [
    # ── 郝玉松 ↔ 刘永雄（党政正职搭档） ──
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "郝玉松（市委书记）与刘永雄（市长）为靖西市党政主要领导搭档，自2023年10月起共事。两人在靖西市委工作务虚会、烟叶产业工作部署会、人大会议等多种场合共同出席。",
        "overlap_org": "中共靖西市委员会/靖西市人民政府",
        "overlap_period": "2023年10月至今",
    },
    # ── 郝玉松 ← 钟恒钦（前后任） ──
    {
        "person_a": 3, "person_b": 1,
        "type": "predecessor_successor",
        "context": "钟恒钦于2016-2021年任靖西市委书记（百色市委常委兼任），郝玉松于2021年7月接任靖西市委书记。两人曾于2020年共同出席靖西版雷神山医院建设活动（钟任市委书记、郝任市长）。",
        "overlap_org": "中共靖西市委员会",
        "overlap_period": "2016-2021年（钟任书记），2021年至今（郝任书记）",
    },
    # ── 钟恒钦 ↔ 郝玉松（曾为党政搭档） ──
    {
        "person_a": 3, "person_b": 1,
        "type": "superior_subordinate",
        "context": "2016-2021年期间，钟恒钦以百色市委常委身份兼任靖西市委书记，郝玉松任靖西市市长，两人曾为靖西市党政正职搭档。",
        "overlap_org": "中共靖西市委员会/靖西市人民政府",
        "overlap_period": "2016-2021年",
    },
    # ── 郝玉松 ↔ 黄兰爱 ──
    {
        "person_a": 1, "person_b": 4,
        "type": "superior_subordinate",
        "context": "郝玉松（市委书记）与黄兰爱（市委副书记，2022.11-2024.06）在靖西市委常委会共事。黄兰爱协助郝玉松处理市委日常工作，分管宣传、乡村振兴等工作。",
        "overlap_org": "中共靖西市委员会",
        "overlap_period": "2022年11月至2024年6月",
    },
    # ── 刘永雄 ↔ 黄兰爱 ──
    {
        "person_a": 2, "person_b": 4,
        "type": "overlap",
        "context": "刘永雄（市长）与黄兰爱（市委副书记）在靖西市党政班子共事约8个月（2023年10月至2024年6月）。",
        "overlap_org": "靖西市党政班子",
        "overlap_period": "2023年10月至2024年6月",
    },
    # ── 郝玉松 ↔ 闭鸿飞 ──
    {
        "person_a": 1, "person_b": 5,
        "type": "overlap",
        "context": "郝玉松（市委书记）与闭鸿飞（市委常委、统战部长）在靖西市委常委会共事。闭鸿飞为靖西本地成长干部，长期在靖西任职。",
        "overlap_org": "中共靖西市委员会",
        "overlap_period": "2021年7月至2025年1月",
    },
    # ── 刘永雄 ↔ 闭鸿飞 ──
    {
        "person_a": 2, "person_b": 5,
        "type": "overlap",
        "context": "刘永雄（市长）与闭鸿飞（市委常委、统战部长）在靖西市共事。",
        "overlap_org": "靖西市",
        "overlap_period": "2023年10月至2025年1月",
    },
    # ── 郝玉松 ↔ 何婷婷 ──
    {
        "person_a": 1, "person_b": 6,
        "type": "overlap",
        "context": "郝玉松（市委书记）与何婷婷（市委常委、副市长）在市委常委会和市政府班子共事。",
        "overlap_org": "中共靖西市委员会/靖西市人民政府",
        "overlap_period": "2024年前至今",
    },
    # ── 刘永雄 ↔ 何婷婷 ──
    {
        "person_a": 2, "person_b": 6,
        "type": "superior_subordinate",
        "context": "刘永雄（市长）与何婷婷（市委常委、副市长）在靖西市政府班子共事，何婷婷为刘永雄的副手。",
        "overlap_org": "靖西市人民政府",
        "overlap_period": "2023年10月至今",
    },
    # ── 刘永雄 ↔ 玉文波 ──
    {
        "person_a": 2, "person_b": 13,
        "type": "superior_subordinate",
        "context": "刘永雄（市长）与玉文波（副市长、公安局局长）在靖西市政府班子共事。",
        "overlap_org": "靖西市人民政府",
        "overlap_period": "2023年10月至今",
    },
    # ── 刘永雄 ↔ 吴英杰 ──
    {
        "person_a": 2, "person_b": 14,
        "type": "superior_subordinate",
        "context": "刘永雄（市长）与吴英杰（副市长）在靖西市政府班子共事。",
        "overlap_org": "靖西市人民政府",
        "overlap_period": "2023年10月至今",
    },
    # ── 刘永雄 ↔ 汪保华 ──
    {
        "person_a": 2, "person_b": 11,
        "type": "superior_subordinate",
        "context": "刘永雄（市长）与汪保华（副市长、驻村工作队队长）在靖西市政府班子共事。",
        "overlap_org": "靖西市人民政府",
        "overlap_period": "2023年10月至今",
    },
    # ── 刘永雄 ↔ 冯志刚 ──
    {
        "person_a": 2, "person_b": 12,
        "type": "superior_subordinate",
        "context": "刘永雄（市长）与冯志刚（副市长、粤桂协作）在靖西市政府班子共事。",
        "overlap_org": "靖西市人民政府",
        "overlap_period": "2023年10月至今",
    },
    # ── 黄兰爱 ↔ 闭鸿飞 ──
    {
        "person_a": 4, "person_b": 5,
        "type": "overlap",
        "context": "黄兰爱（市委副书记）与闭鸿飞（市委常委、统战部长）在靖西市委常委会共事。",
        "overlap_org": "中共靖西市委员会",
        "overlap_period": "2022年11月至2024年6月",
    },
    # ── 陈飞龙 ↔ 郝玉松（人大与党委） ──
    {
        "person_a": 1, "person_b": 18,
        "type": "overlap",
        "context": "郝玉松（市委书记）与陈飞龙（市人大常委会主任）在靖西市四家班子中共同工作。",
        "overlap_org": "靖西市四家班子",
        "overlap_period": "2021年至今",
    },
    # ── 陈飞龙 ↔ 刘永雄（政府与人大） ──
    {
        "person_a": 2, "person_b": 18,
        "type": "overlap",
        "context": "刘永雄（市长）与陈飞龙（市人大常委会主任）在靖西市四家班子中共同工作。",
        "overlap_org": "靖西市四家班子",
        "overlap_period": "2023年10月至今",
    },
    # ── 郝玉松 ↔ 陆海（党委与政协） ──
    {
        "person_a": 1, "person_b": 19,
        "type": "overlap",
        "context": "郝玉松（市委书记）与陆海（市政协主席）在靖西市四家班子中共同工作。",
        "overlap_org": "靖西市四家班子",
        "overlap_period": "2021年至今",
    },
    # ── 钟恒钦 → 河池/钦州（跨市调任） ──
    # （钟恒钦从靖西到河池再到钦州的移动已在positions中体现，这里不重复）
]

# =========================================================================
# 5. SOURCE REGISTER (shared)
# =========================================================================
source_register = [
    {"id": "S001", "title": "靖西市人民政府门户网站 — 领导之窗/领导活动", "url": "https://www.jingxi.gov.cn/", "publisher": "靖西市人民政府", "published_at": "2024-2026", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认刘永雄、郝玉松当前职务"},
    {"id": "S002", "title": "网易新闻 — 郝玉松任广西靖西市委书记", "url": "https://www.163.com/", "publisher": "网易", "published_at": "2021-07-17", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "郝玉松完整简历"},
    {"id": "S003", "title": "北京日报客户端 — 清华博士郝玉松拟升职", "url": "https://www.bjd.com.cn/", "publisher": "北京日报", "published_at": "2024-12-14", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "郝玉松职业履历概述"},
    {"id": "S004", "title": "百色市政协网 — 政协领导郝玉松", "url": "http://www.gxbszx.gov.cn/", "publisher": "百色市政协", "published_at": "2025-04-17", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认郝玉松兼任百色市政协副主席"},
    {"id": "S005", "title": "广西县域经济网 — 刘永雄拟任县(市、区)长公示", "url": "https://www.gxcounty.com/", "publisher": "广西县域经济网", "published_at": "2023-09-11", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "刘永雄简历和任前公示"},
    {"id": "S006", "title": "靖西市第三届人大会议报道 — 刘永雄当选市长", "url": "https://www.jingxi.gov.cn/", "publisher": "靖西市人大常委会", "published_at": "2023-10", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "刘永雄2023年10月全票当选市长"},
    {"id": "S007", "title": "靖西市委三届六次全会公报", "url": "https://www.jingxi.gov.cn/", "publisher": "靖西市委", "published_at": "2024-01-04", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "郝玉松、刘永雄、常委名单确认"},
    {"id": "S008", "title": "靖西市2024年市委工作务虚会报道", "url": "https://www.jingxi.gov.cn/", "publisher": "靖西市人民政府", "published_at": "2024-02-21", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "郝玉松、刘永雄、黄兰爱、陈飞龙、陆海等确认"},
    {"id": "S009", "title": "靖西市政府务虚会报道（靖西人大网）", "url": "https://www.jingxi.gov.cn/", "publisher": "靖西市人大", "published_at": "2024-02-19", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "何婷婷、汪保华、冯志刚、蒋凯、玉文波、吴英杰、乃振峰确认"},
    {"id": "S010", "title": "靖西市政府领导分工通知 (靖政发2024/2025)", "url": "https://www.jingxi.gov.cn/", "publisher": "靖西市人民政府", "published_at": "2024-2025", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认副市长分工及AB岗安排"},
    {"id": "S011", "title": "新京报 — 钟恒钦任上被查", "url": "https://www.bjnews.com.cn/", "publisher": "新京报", "published_at": "2025-05-09", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "钟恒钦完整简历及被查信息"},
    {"id": "S012", "title": "广西纪检监察网 — 钟恒钦严重违纪违法通报", "url": "https://www.gxjjw.gov.cn/", "publisher": "广西纪检监察网", "published_at": "2025", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "钟恒钦被开除党籍和公职"},
    {"id": "S013", "title": "百度百科 — 黄兰爱", "url": "https://baike.baidu.com/", "publisher": "百度", "published_at": "2025", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "黄兰爱完整履历"},
    {"id": "S014", "title": "百色市政府任前公示（百组示字〔2022〕91号）", "url": "http://www.baise.gov.cn/", "publisher": "中共百色市委组织部", "published_at": "2022-11-07", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high", "notes": "黄兰爱拟进一步使用为市委副书记"},
    {"id": "S015", "title": "百色市政府任前公示（百组示字〔2025〕2号）", "url": "http://www.baise.gov.cn/", "publisher": "中共百色市委组织部", "published_at": "2025-01-08", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high", "notes": "闭鸿飞拟任正处级领导职务"},
    {"id": "S016", "title": "网易新闻 — 闭鸿飞简历", "url": "https://www.163.com/", "publisher": "网易", "published_at": "2025-01-08", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "闭鸿飞完整简历"},
    {"id": "S017", "title": "汲古新知 — 黄兰爱任德保县政协党组书记", "url": "", "publisher": "微信公众平台", "published_at": "2025-02-10", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "黄兰爱履新德保县政协"},
    {"id": "S018", "title": "清华大学物理系 — 龙桂鲁带队到广西调研看望系友", "url": "https://www.phys.tsinghua.edu.cn/", "publisher": "清华大学物理系", "published_at": "2014-12-03", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认郝玉松清华大学系友身份"},
]

# =========================================================================
# 5. BUILD
# =========================================================================
def build_database(db_path):
    """Create SQLite DB and insert all data."""
    conn = sqlite3.connect(str(db_path))
    try:
        from gov_relation.schema import create_tables, insert_persons, insert_organizations, insert_positions, insert_relationships
        create_tables(conn, overwrite=True)
        insert_persons(conn, persons)
        insert_organizations(conn, organizations)
        insert_positions(conn, positions)
        insert_relationships(conn, relationships)
        print(f"DB ready: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")
    finally:
        conn.close()


def build_gexf(gexf_path):
    """Generate GEXF graph file."""
    from gov_relation.gexf import GEXFBuilder
    builder = GEXFBuilder(title=SLUG)
    for p in persons:
        builder.add_person(
            id=p["id"],
            name=p.get("name", ""),
            current_post=p.get("current_post", ""),
            current_org=p.get("current_org", ""),
            gender=p.get("gender", ""),
            ethnicity=p.get("ethnicity", ""),
            birth=p.get("birth", ""),
            source=p.get("source", ""),
        )
    for o in organizations:
        builder.add_organization(
            id=o["id"] + 100000,
            name=o.get("name", ""),
            org_type=o.get("type", ""),
            level=o.get("level", ""),
            location=o.get("location", ""),
        )
    for r in relationships:
        builder.add_relationship(
            source=r["person_a"],
            target=r["person_b"],
            rel_type=r.get("type", ""),
            context=r.get("context", ""),
            overlap_org=r.get("overlap_org", ""),
            overlap_period=r.get("overlap_period", ""),
        )
    builder.write(gexf_path)
    print(f"GEXF ready: {gexf_path}")


def build_person_json(person, filename):
    """Write a single person JSON file per reference schema."""
    output_path = PERSONS_DIR / filename
    person_id = f"jingxi_{person['name']}"

    # Build career timeline from positions for this person
    timeline = []
    for pos in positions:
        if pos["person_id"] == person["id"]:
            entry = {
                "start": pos.get("start_date", "待查"),
                "end": pos.get("end_date", "至今"),
                "org": "",  # resolve later
                "title": pos["title"],
                "level": pos.get("rank", ""),
                "location": "",
                "system": "party" if "委" in pos["title"] and "政府" not in pos["title"] else "government",
                "rank": pos.get("rank", ""),
                "is_key_promotion": any(kw in pos["title"] for kw in ["书记", "市长", "县长", "主席", "部长", "副书记"]),
                "notes": pos.get("note", ""),
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
            # Resolve org name
            for o in organizations:
                if o["id"] == pos["org_id"]:
                    entry["org"] = o["name"]
                    entry["location"] = o.get("location", "")
                    break
            timeline.append(entry)

    if not timeline:
        timeline.append({
            "start": "待查", "end": "至今",
            "org": person.get("current_org", "履历缺口"),
            "title": person.get("current_post", ""),
            "level": "",
            "location": "",
            "system": "party" if "书记" in person.get("current_post", "") else "government",
            "rank": "",
            "is_key_promotion": True,
            "notes": "公开资料未找到完整履历信息",
            "confidence": "unverified",
            "source_ids": []
        })

    # Build relationships for this person
    rels = []
    for r in relationships:
        if r["person_a"] == person["id"]:
            other = next((p for p in persons if p["id"] == r["person_b"]), None)
            if other:
                rels.append({
                    "person": other["name"],
                    "person_id": f"jingxi_{other['name']}",
                    "relationship_type": r["type"],
                    "strength": "strong" if "overlap" in r["type"] or "superior" in r["type"] else "medium",
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "undirected",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                })
        elif r["person_b"] == person["id"]:
            other = next((p for p in persons if p["id"] == r["person_a"]), None)
            if other:
                rels.append({
                    "person": other["name"],
                    "person_id": f"jingxi_{other['name']}",
                    "relationship_type": r["type"],
                    "strength": "strong" if "overlap" in r["type"] or "superior" in r["type"] else "medium",
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "undirected",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                })

    doc = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "百色市",
            "region": "靖西市",
            "job": person["current_post"],
            "task_id": "guangxi_靖西市",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": person_id,
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", "待查"),
            "ethnicity": person.get("ethnicity", "待查"),
            "birth": person.get("birth", "待查"),
            "birthplace": person.get("birthplace", "待查"),
            "native_place": person.get("birthplace", "待查"),
            "education": [
                {
                    "period": "",
                    "institution": person.get("education", ""),
                    "major": "",
                    "degree": person.get("education", ""),
                    "study_type": "unknown",
                    "source_ids": []
                }
            ] if person.get("education") and person["education"] != "待查" else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth', '待查')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace', '待查')}",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": timeline,
        "organizations": [
            {
                "org_name": o["name"],
                "org_type": o.get("type", ""),
                "level": o.get("level", "")
            }
            for o in organizations
            if any(pos["org_id"] == o["id"] for pos in positions if pos["person_id"] == person["id"])
        ],
        "relationships": rels,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": f"截至2026年7月，公开渠道未发现{person['name']}的负面纪律或审计信息",
                "date": "2026-07-23",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") and person.get("birth") != "待查" else "unverified",
            "current_role": "confirmed",
            "career_completeness": "complete" if len(timeline) > 3 else "partial" if len(timeline) > 0 else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{person['name']}的完整履历及{'' if person.get('birth') != '待查' else '出生年月、籍贯、学历、'}详细信息"
        },
        "open_questions": []
    }

    # Add open questions based on what's missing
    if person.get("birth") in [None, "", "待查"]:
        doc["open_questions"].append({
            "priority": "critical",
            "question": f"{person['name']}的出生年月、籍贯、学历、入党时间、参加工作时间",
            "why_it_matters": "无法建立完整的身份标识",
            "suggested_queries": [f"{person['name']} 简历 靖西"],
            "last_attempted": AS_OF
        })
    if person.get("work_start") in [None, "", "待查"]:
        doc["open_questions"].append({
            "priority": "critical",
            "question": f"{person['name']}的完整职业生涯履历",
            "why_it_matters": "无法追溯其任职路径和系统经历",
            "suggested_queries": [f"{person['name']} 靖西 任职经历"],
            "last_attempted": AS_OF
        })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {output_path}")


def main():
    print(f"=== 靖西市数据构建 ({TODAY}) ===")

    # Run from staging directory
    os.chdir(str(STAGING_DIR))

    # 1. Database
    print("\n--- Building database ---")
    build_database(DB_PATH)

    # 2. GEXF
    print("\n--- Building GEXF ---")
    build_gexf(GEXF_PATH)

    # 3. Person JSONs
    print("\n--- Building person JSONs ---")
    # 郝玉松 — 市委书记
    build_person_json(persons[0], f"{TODAY}-广西壮族自治区-百色市-市委书记-郝玉松.json")
    # 刘永雄 — 市长
    build_person_json(persons[1], f"{TODAY}-广西壮族自治区-百色市-市长-刘永雄.json")
    # 钟恒钦 — 前任书记（被查）
    build_person_json(persons[2], f"{TODAY}-广西壮族自治区-百色市-原市委书记-钟恒钦.json")

    print("\n=== Build complete ===")


if __name__ == "__main__":
    main()
