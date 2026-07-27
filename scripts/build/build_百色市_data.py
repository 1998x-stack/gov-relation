#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百色市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 地级市
Province: 广西壮族自治区
Parent City:
Region: 百色市
Targets: 市委书记 & 市长

当前在任 (as of 2026-07-23):
- 市委书记: 黄汝生 (百色市委书记)
- 市长: 王永超 (百色市委副书记、市长、市政府党组书记)
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "百色市"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-23"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：市委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "黄汝生",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "百色市委书记",
        "current_org": "中共百色市委员会",
        "source": "https://www.gxbsrd.gov.cn/html/news-view-226131.html"
    },
    # ════════════════════════════════════════
    # 核心领导：市长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "王永超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年6月",
        "birthplace": "山东曹县",
        "education": "中央财经大学博士",
        "party_join": "1991年12月",
        "work_start": "1993年7月",
        "current_post": "百色市委副书记、市长、市政府党组书记",
        "current_org": "百色市人民政府/中共百色市委员会",
        "source": "https://baike.baidu.com/item/%E7%8E%8B%E6%B0%B8%E8%B6%85"
    },
    # ════════════════════════════════════════
    # 市人大常委会主任
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "周武红",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "百色市人大常委会主任、党组书记",
        "current_org": "百色市人民代表大会常务委员会",
        "source": "https://www.gxbsrd.gov.cn/html/news-view-78719.html"
    },
    # ════════════════════════════════════════
    # 市政协主席
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "石国怀",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "百色市政协主席",
        "current_org": "中国人民政治协商会议百色市委员会",
        "source": "https://www.gxbszx.gov.cn/cq-list.html?id=202"
    },
    # ════════════════════════════════════════
    # 市委常委/常务副市长
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "李建华",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "百色市委常委、副市长",
        "current_org": "中共百色市委员会/百色市人民政府",
        "source": "https://www.gxbsrd.gov.cn/html/news-view-227598.html"
    },
    {
        "id": 6,
        "name": "赖荣生",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "百色市委常委、宣传部部长",
        "current_org": "中共百色市委员会",
        "source": "https://www.gxbsrd.gov.cn/html/news-view-227695.html"
    },
    # ════════════════════════════════════════
    # 副市长
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "黄彩雪",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "百色市副市长",
        "current_org": "百色市人民政府",
        "source": "https://www.gxbsrd.gov.cn/html/news-view-227726.html"
    },
    {
        "id": 8,
        "name": "徐迪克",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "百色市副市长",
        "current_org": "百色市人民政府",
        "source": "https://www.gxbsrd.gov.cn/html/news-view-227598.html"
    },
    {
        "id": 9,
        "name": "陈列",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "百色市副市长、市公安局局长",
        "current_org": "百色市人民政府/百色市公安局",
        "source": "https://www.gxbsrd.gov.cn/html/news-view-227598.html"
    },
    {
        "id": 10,
        "name": "黄慧",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "百色市副市长",
        "current_org": "百色市人民政府",
        "source": "https://www.gxbsrd.gov.cn/html/news-view-227726.html"
    },
    {
        "id": 11,
        "name": "庞春潮",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "百色市副市长",
        "current_org": "百色市人民政府",
        "source": "https://www.gxbsrd.gov.cn/html/news-view-227726.html"
    },
    {
        "id": 12,
        "name": "方胜兵",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "百色市副市长",
        "current_org": "百色市人民政府",
        "source": "https://www.gxbsrd.gov.cn/html/news-view-227504.html"
    },
    # ════════════════════════════════════════
    # 市政府秘书长
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "蒋竞辉",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "百色市政府秘书长",
        "current_org": "百色市人民政府",
        "source": "https://www.gxbsrd.gov.cn/html/news-view-227598.html"
    },
    # ════════════════════════════════════════
    # 人大副主任
    # ════════════════════════════════════════
    {
        "id": 14,
        "name": "黄永才",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "百色市人大常委会副主任",
        "current_org": "百色市人民代表大会常务委员会",
        "source": "https://www.gxbsrd.gov.cn/html/news-view-78719.html"
    },
    {
        "id": 15,
        "name": "黄善平",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "百色市人大常委会副主任",
        "current_org": "百色市人民代表大会常务委员会",
        "source": "https://www.gxbsrd.gov.cn/html/news-view-78719.html"
    },
    {
        "id": 16,
        "name": "李荣能",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "百色市人大常委会副主任",
        "current_org": "百色市人民代表大会常务委员会",
        "source": "https://www.gxbsrd.gov.cn/html/news-view-78719.html"
    },
    {
        "id": 17,
        "name": "方立斯",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "百色市人大常委会副主任、秘书长",
        "current_org": "百色市人民代表大会常务委员会",
        "source": "https://www.gxbsrd.gov.cn/html/news-view-78719.html"
    },
    {
        "id": 18,
        "name": "陆兰碧",
        "gender": "女",
        "ethnicity": "壮族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "百色市人大常委会副主任（兼德保县委书记）",
        "current_org": "百色市人民代表大会常务委员会",
        "source": "https://www.gxbsrd.gov.cn/html/news-view-78719.html"
    },
    {
        "id": 19,
        "name": "农斌",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "百色市人大常委会副主任",
        "current_org": "百色市人民代表大会常务委员会",
        "source": "https://www.gxbsrd.gov.cn/html/news-view-78719.html"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共百色市委员会", "type": "党委", "level": "地级市", "parent": "", "location": "广西百色市"},
    {"id": 2, "name": "百色市人民政府", "type": "政府", "level": "地级市", "parent": "", "location": "广西百色市"},
    {"id": 3, "name": "百色市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "", "location": "广西百色市"},
    {"id": 4, "name": "中国人民政治协商会议百色市委员会", "type": "政协", "level": "地级市", "parent": "", "location": "广西百色市"},
    {"id": 5, "name": "中共百色市委宣传部", "type": "党委", "level": "地级市", "parent": "中共百色市委员会", "location": "广西百色市"},
    {"id": 6, "name": "百色市公安局", "type": "政府", "level": "地级市", "parent": "百色市人民政府", "location": "广西百色市"},
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 黄汝生 - 市委书记
    {"person_id": 1, "org_id": 1, "title": "百色市委书记", "start_date": "待查", "end_date": "present", "rank": "正厅级", "note": ""},
    # 王永超 - 市委副书记、市长
    {"person_id": 2, "org_id": 1, "title": "百色市委副书记", "start_date": "2025-04", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "百色市长、市政府党组书记", "start_date": "2025-04", "end_date": "present", "rank": "正厅级", "note": "2025年4月11日补选为市长"},
    # 周武红 - 市人大常委会主任
    {"person_id": 3, "org_id": 3, "title": "百色市人大常委会主任、党组书记", "start_date": "待查", "end_date": "present", "rank": "正厅级", "note": ""},
    # 石国怀 - 市政协主席
    {"person_id": 4, "org_id": 4, "title": "百色市政协主席", "start_date": "待查", "end_date": "present", "rank": "正厅级", "note": ""},
    # 李建华 - 市委常委、副市长
    {"person_id": 5, "org_id": 1, "title": "百色市委常委", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "百色市副市长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 赖荣生 - 市委常委、宣传部部长
    {"person_id": 6, "org_id": 1, "title": "百色市委常委", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 5, "title": "百色市委宣传部部长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": "兼任市创城指挥部常务副指挥长"},
    # 黄彩雪 - 副市长
    {"person_id": 7, "org_id": 2, "title": "百色市副市长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 徐迪克 - 副市长
    {"person_id": 8, "org_id": 2, "title": "百色市副市长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 陈列 - 副市长、市公安局局长
    {"person_id": 9, "org_id": 2, "title": "百色市副市长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 6, "title": "百色市公安局局长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 黄慧 - 副市长
    {"person_id": 10, "org_id": 2, "title": "百色市副市长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 庞春潮 - 副市长
    {"person_id": 11, "org_id": 2, "title": "百色市副市长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 方胜兵 - 副市长（新任）
    {"person_id": 12, "org_id": 2, "title": "百色市副市长", "start_date": "2026-06", "end_date": "present", "rank": "副厅级", "note": "2026年6月25日市五届人大常委会第三十八次会议决定任命"},
    # 蒋竞辉 - 市政府秘书长
    {"person_id": 13, "org_id": 2, "title": "百色市政府秘书长", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
    # 黄永才 - 市人大常委会副主任
    {"person_id": 14, "org_id": 3, "title": "百色市人大常委会副主任", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 黄善平 - 市人大常委会副主任
    {"person_id": 15, "org_id": 3, "title": "百色市人大常委会副主任", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 李荣能 - 市人大常委会副主任
    {"person_id": 16, "org_id": 3, "title": "百色市人大常委会副主任", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 方立斯 - 市人大常委会副主任、秘书长
    {"person_id": 17, "org_id": 3, "title": "百色市人大常委会副主任、秘书长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 陆兰碧 - 市人大常委会副主任（兼德保县委书记）
    {"person_id": 18, "org_id": 3, "title": "百色市人大常委会副主任", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": "兼德保县委书记"},
    # 农斌 - 市人大常委会副主任
    {"person_id": 19, "org_id": 3, "title": "百色市人大常委会副主任", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 党政主要领导
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "黄汝生（市委书记）与王永超（市长）为百色市党政主要搭档", "overlap_org": "百色市党政班子", "overlap_period": "2025-"},
    # 市委书记与市长
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "黄汝生（市委书记）与李建华（市委常委、副市长）为市委班子领导关系", "overlap_org": "中共百色市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "黄汝生（市委书记）与赖荣生（市委常委、宣传部部长）为市委班子领导关系", "overlap_org": "中共百色市委员会", "overlap_period": ""},
    # 市长与副市长
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "王永超（市长）与李建华（副市长）为市政府班子领导关系", "overlap_org": "百色市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "王永超（市长）与黄彩雪（副市长）为市政府班子领导关系", "overlap_org": "百色市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "王永超（市长）与徐迪克（副市长）为市政府班子领导关系", "overlap_org": "百色市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "王永超（市长）与陈列（副市长、市公安局局长）为市政府班子领导关系", "overlap_org": "百色市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "王永超（市长）与黄慧（副市长）为市政府班子领导关系", "overlap_org": "百色市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "王永超（市长）与庞春潮（副市长）为市政府班子领导关系", "overlap_org": "百色市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "王永超（市长）与方胜兵（副市长）为市政府班子领导关系", "overlap_org": "百色市人民政府", "overlap_period": "2026-06-"},
    # 市长与政府秘书长
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "王永超（市长）与蒋竞辉（市政府秘书长）为市政府班子工作关系", "overlap_org": "百色市人民政府", "overlap_period": ""},
    # 人大主任与副主任
    {"person_a": 3, "person_b": 14, "type": "上下级", "context": "周武红（市人大常委会主任）与黄永才（副主任）为市人大常委会班子成员", "overlap_org": "百色市人民代表大会常务委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 15, "type": "上下级", "context": "周武红（市人大常委会主任）与黄善平（副主任）为市人大常委会班子成员", "overlap_org": "百色市人民代表大会常务委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 16, "type": "上下级", "context": "周武红（市人大常委会主任）与李荣能（副主任）为市人大常委会班子成员", "overlap_org": "百色市人民代表大会常务委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 17, "type": "上下级", "context": "周武红（市人大常委会主任）与方立斯（副主任、秘书长）为市人大常委会班子成员", "overlap_org": "百色市人民代表大会常务委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 18, "type": "上下级", "context": "周武红（市人大常委会主任）与陆兰碧（副主任）为市人大常委会班子成员", "overlap_org": "百色市人民代表大会常务委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 19, "type": "上下级", "context": "周武红（市人大常委会主任）与农斌（副主任）为市人大常委会班子成员", "overlap_org": "百色市人民代表大会常务委员会", "overlap_period": ""},
]


# =========================================================================
# 5. HELPERS
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(current_post):
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp and "纪委书记" not in cp:
        return "200,30,30"
    if "市长" in cp and "副" not in cp:
        return "30,100,200"
    if "副书记" in cp:
        return "220,80,80"
    if "纪委" in cp:
        return "255,165,0"
    if "副" in cp:
        return "100,150,220"
    if "常委" in cp:
        return "180,100,180"
    if "主任" in cp or "人大" in cp:
        return "60,180,60"
    if "主席" in cp or "政协" in cp:
        return "60,180,60"
    return "100,100,100"


def person_size(current_post):
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp and "纪委书记" not in cp:
        return "20.0"
    if "市长" in cp and "副" not in cp:
        return "18.0"
    if "副书记" in cp:
        return "15.0"
    if "副" in cp:
        return "12.0"
    if "常委" in cp:
        return "12.0"
    if "主任" in cp or "主席" in cp:
        return "12.0"
    return "10.0"


def person_shape(current_post):
    cp = current_post or ""
    if "书记" in cp and "纪委书记" not in cp:
        return "square"
    if "人大" in cp or "政协" in cp:
        return "diamond"
    if "副" in cp:
        return "triangle"
    return "circle"


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "开发区": "200,255,200",
        "纪委": "255,200,150",
    }
    return colors.get(org_type, "200,200,200")


def _infer_rank(post):
    if not post:
        return ""
    if "书记" in post and "副书记" not in post and "副" not in post.replace("副书记", ""):
        return "正厅级"
    if "市长" in post and "副" not in post:
        return "正厅级"
    if "主任" in post and "副" not in post:
        return "正厅级"
    if "主席" in post and "副" not in post:
        return "正厅级"
    if "副" in post:
        return "副厅级"
    if "秘书长" in post:
        return "正处级"
    return ""


# =========================================================================
# 6. BUILD FUNCTIONS
# =========================================================================

def build_db():
    """Build SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

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
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

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
        );
    """)

    for p in persons:
        cur.execute("""INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) 
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"], pos.get("start_date", ""), pos.get("end_date", ""),
                     pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"], r["context"], r.get("overlap_org", ""),
                     r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


def build_gexf():
    """Build GEXF graph file."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>百色市领导班子关系网络</description>')
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
        pid = p["id"]
        post = p.get("current_post", "")
        c = person_color(post)
        sz = person_size(post)
        sh = person_shape(post)

        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'        <viz:shape value="{sh}"/>')
        lines.append('      </node>')

    # Nodes — organizations
    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o.get("type", ""))
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

    # Person → organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(
            f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"] + 100000}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ person (relationships)
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


def build_person_json(person, timeline, rels, sources):
    """Build a person graph JSON following the person_graph_json schema."""
    now = AS_OF.replace("-", "")
    slug = f"baise_{person['name']}"

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "百色市",
            "region": "百色市",
            "job": person.get("current_post", ""),
            "task_id": "guangxi_百色市",
            "time_focus": "2026-07"
        },
        "identity": {
            "person_id": slug,
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth','')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace','')}",
                "official_profile_url": person.get("source", "")
            }
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": _infer_rank(person.get("current_post", "")),
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"]
        },
        "career_timeline": timeline,
        "organizations": [],
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
                "description": "No integrity risk signals found in initial search",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": sources,
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"个人基本信息（出生年月、籍贯、教育背景）不完整。{person['name']}的完整履历需进一步调查。"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的出生年月和籍贯是什么？",
                "why_it_matters": "个人基本信息是身份识别的核心字段",
                "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 百度百科"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"{person['name']}的教育背景是什么？",
                "why_it_matters": "学缘关系是构建关系网络的重要维度",
                "suggested_queries": [f"{person['name']} 学历"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"{person['name']}的完整任职履历是怎样的？此前任何职？",
                "why_it_matters": "前序任职是构建继任关系和跨地区调任证据的关键",
                "suggested_queries": [f"{person['name']} 曾任", f"{person['name']} 调任"],
                "last_attempted": AS_OF
            }
        ]
    }


def build_all_person_jsons():
    """Build and write individual person JSON files for the two core leaders."""

    # ── 王永超 career timeline (confirmed from Baidu Baike) ──
    timeline_wang = [
        {"period": "1989.09-1993.07", "org": "西南交通大学", "title": "机械工程二系内燃机专业学习", "confirmed": True, "source_ids": ["S001"]},
        {"period": "1993.07-1993.12", "org": "首钢总公司铸造中心", "title": "技术处干部", "confirmed": True, "source_ids": ["S001"]},
        {"period": "1993.12-1997.04", "org": "广西玉柴机器股份有限公司", "title": "干部", "confirmed": True, "source_ids": ["S001"]},
        {"period": "1997.04-2001.10", "org": "广西壮族自治区机械工业厅", "title": "汽车工业处干部、副主任科员", "confirmed": True, "source_ids": ["S001"]},
        {"period": "2001.10-2002.10", "org": "广西壮族自治区政府办公厅", "title": "第二秘书处副主任科员、主任科员", "confirmed": True, "source_ids": ["S001"]},
        {"period": "2002.10-2004.07", "org": "南宁市科学技术局", "title": "副局长、党组成员", "confirmed": True, "source_ids": ["S001"]},
        {"period": "2004.07-2006.07", "org": "南宁市上林县人民政府", "title": "副县长", "confirmed": True, "source_ids": ["S001"]},
        {"period": "2006.07-2007.07", "org": "中共上林县委", "title": "县委常委、副县长", "confirmed": True, "source_ids": ["S001"]},
        {"period": "2007.07-2009.11", "org": "南宁市人民政府", "title": "副秘书长(正处级)、金融办主任", "confirmed": True, "source_ids": ["S001"]},
        {"period": "2009.11-2011.05", "org": "南宁市青秀区人民政府", "title": "青秀区委副书记、区长", "confirmed": True, "source_ids": ["S001"]},
        {"period": "2011.05-2013.07", "org": "中共南宁市邕宁区委", "title": "邕宁区委书记", "confirmed": True, "source_ids": ["S001"]},
        {"period": "2013.07-2013.09", "org": "中共南宁市邕宁区委", "title": "邕宁区委书记，兼邕宁新兴产业园区党工委书记", "confirmed": True, "source_ids": ["S001"]},
        {"period": "2013.09-2016.04", "org": "南宁市交通运输局", "title": "局长、党组书记", "confirmed": True, "source_ids": ["S001"]},
        {"period": "2016.04-2016.05", "org": "中共南宁市青秀区委", "title": "青秀区委书记（兼市交通运输局局长）", "confirmed": True, "source_ids": ["S001"]},
        {"period": "2016.05-2017.12", "org": "中共南宁市青秀区委", "title": "青秀区委书记", "confirmed": True, "source_ids": ["S001"]},
        {"period": "2017.12-2018.01", "org": "中共崇左市委", "title": "崇左市委常委（兼青秀区委书记）", "confirmed": True, "source_ids": ["S001"]},
        {"period": "2018.01-2018.02", "org": "中共崇左市委", "title": "崇左市委常委、宣传部部长", "confirmed": True, "source_ids": ["S001"]},
        {"period": "2018.02-2020.03", "org": "中共崇左市委/崇左市人民政府", "title": "崇左市委常委、宣传部部长、副市长", "confirmed": True, "source_ids": ["S001"]},
        {"period": "2020.03-2021.03", "org": "中共柳州市委/柳州市纪委监委", "title": "柳州市委常委、纪委书记，监委代主任", "confirmed": True, "source_ids": ["S001"]},
        {"period": "2021.03-2023.01", "org": "梧州市人民政府", "title": "梧州市委常委、副市长（常务），市苍海新区党工委书记（兼）", "confirmed": True, "source_ids": ["S001"]},
        {"period": "2023.01-2025.03", "org": "广西壮族自治区工业和信息化厅", "title": "党组书记、厅长", "confirmed": True, "source_ids": ["S001"]},
        {"period": "2025.04-至今", "org": "百色市人民政府/中共百色市委", "title": "百色市委副书记、市长、市政府党组书记", "confirmed": True, "source_ids": ["S001", "S002"]},
    ]

    rels_wang = [
        {"type": "党政搭档", "person": "黄汝生", "context": "与市委书记黄汝生为百色市党政主要搭档", "overlap_org": "百色市党政班子", "overlap_period": "2025-", "confidence": "confirmed", "source_ids": ["S002"]},
    ]

    sources_wang = [
        {"id": "S001", "type": "baike", "url": "https://baike.baidu.com/item/%E7%8E%8B%E6%B0%B8%E8%B6%85", "access_date": AS_OF, "notes": "王永超百度百科完整履历"},
        {"id": "S002", "type": "government_news", "url": "https://www.gxbsrd.gov.cn/", "access_date": AS_OF, "notes": "百色人大网新闻报道证实2025年4月补选为市长"},
    ]

    person_wang = build_person_json(
        [p for p in persons if p["name"] == "王永超"][0],
        timeline_wang,
        rels_wang,
        sources_wang
    )

    # ── 黄汝生 (limited data) ──
    timeline_huang = []
    rels_huang = [
        {"type": "党政搭档", "person": "王永超", "context": "与市长王永超为百色市党政主要搭档", "overlap_org": "百色市党政班子", "overlap_period": "2025-", "confidence": "confirmed", "source_ids": ["S003"]},
    ]
    sources_huang = [
        {"id": "S003", "type": "government_news", "url": "https://www.gxbsrd.gov.cn/html/news-view-226131.html", "access_date": AS_OF, "notes": "黄汝生在百色市人大会议闭幕式上的讲话，确认其市委书记身份"},
    ]

    person_huang = build_person_json(
        [p for p in persons if p["name"] == "黄汝生"][0],
        timeline_huang,
        rels_huang,
        sources_huang
    )
    person_huang["confidence_summary"]["biggest_gap"] = "黄汝生的出生年月、籍贯、教育背景、完整履历全部缺失。这是当前调查的最大缺口。"

    # Write JSON files
    now_str = AS_OF.replace("-", "")
    for person_data, name, job_title in [
        (person_huang, "黄汝生", "百色市委书记"),
        (person_wang, "王永超", "百色市长"),
    ]:
        filename = f"{now_str}-广西壮族自治区-百色市-{job_title}-{name}.json"
        filepath = os.path.join(PERSONS_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(person_data, f, ensure_ascii=False, indent=2)
        print(f"Person JSON written: {filepath}")


# =========================================================================
# 7. MAIN
# =========================================================================
def main():
    print("=" * 60)
    print(f"构建百色市领导班子关系网络")
    print(f"数据截止日期: {AS_OF}")
    print(f"暂存目录: {STAGING_DIR}")
    print("=" * 60)

    build_db()
    build_gexf()
    build_all_person_jsons()

    print()
    print("=== 构建完成 ===")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Person JSONs: {PERSONS_DIR}")


if __name__ == "__main__":
    main()
