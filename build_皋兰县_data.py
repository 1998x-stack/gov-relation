#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 皋兰县 (Gaolan County, Lanzhou, Gansu) leadership network.

皋兰县 — 甘肃省兰州市下辖县.
Covers current Party Secretary (康石), County Magistrate (沈毅), their predecessors,
key leadership team members, and organizational hierarchy.
"""

import sqlite3
import os
import json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/gansu_皋兰县")
os.makedirs(STAGING, exist_ok=True)

DB_PATH = os.path.join(STAGING, "皋兰县_network.db")
GEXF_PATH = os.path.join(STAGING, "皋兰县_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── A. Current Top Leaders ──

    # 康石 — 皋兰县委书记, also 兰州新区党工委委员、管委会副主任 (from 2026.05)
    {"id": 1, "name": "康石", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-04", "birthplace": "湖南娄底",
     "education": "研究生学历，工学硕士",
     "party_join": "中共党员", "work_start": "2010-07",
     "current_post": "皋兰县委书记",
     "current_org": "中共皋兰县委",
     "source": "https://www.gaolan.gov.cn — 皋兰县政府网站康石个人页面; 兰州新区官方网站领导介绍页"},

    # 沈毅 — 皋兰县委副书记、县长 (since 2025.04)
    {"id": 2, "name": "沈毅", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-10-24", "birthplace": "河南尉氏",
     "education": "大学学历，军事学学士、工学学士（解放军信息工程大学指挥自动化专业）",
     "party_join": "2002-12", "work_start": "2001-09",
     "current_post": "皋兰县县长",
     "current_org": "皋兰县人民政府",
     "source": "https://www.gaolan.gov.cn — 皋兰县政府网站沈毅个人页面; 百度百科"},

    # ── B. Leadership Team Members ──

    # 刘冬青 — 县委副书记、县政府党组副书记、副县长
    {"id": 3, "name": "刘冬青", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "皋兰县委副书记、副县长",
     "current_org": "皋兰县人民政府",
     "source": "https://www.gaolan.gov.cn — 皋兰县政府网站县委/县政府领导页"},

    # 张建华 — 县委常委、副县长
    {"id": 4, "name": "张建华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "皋兰县委常委、副县长",
     "current_org": "皋兰县人民政府",
     "source": "https://www.gaolan.gov.cn — 皋兰县政府网站县政府领导页"},

    # 张建龙 — 县委常委、组织部部长
    {"id": 5, "name": "张建龙", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "皋兰县委常委、组织部部长",
     "current_org": "中共皋兰县委组织部",
     "source": "https://www.gaolan.gov.cn — 皋兰县政府网站县委领导页"},

    # 颜维祥 — 县委常委、政法委书记
    {"id": 6, "name": "颜维祥", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "皋兰县委常委、政法委书记",
     "current_org": "中共皋兰县委政法委员会",
     "source": "https://www.gaolan.gov.cn — 皋兰县公安工作会议报道（2026.02.28）"},

    # 丁晓辉 — 县委常委、副县长
    {"id": 7, "name": "丁晓辉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "皋兰县委常委、副县长",
     "current_org": "皋兰县人民政府",
     "source": "https://www.gaolan.gov.cn — 皋兰县政府网站班子成员页"},

    # 邵博 — 县委常委、副县长(挂职)
    {"id": 8, "name": "邵博", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "皋兰县委常委、副县长(挂职)",
     "current_org": "皋兰县人民政府",
     "source": "https://www.gaolan.gov.cn — 皋兰县政府网站班子成员页"},

    # 姜勇志 — 县委常委、副县长(挂职)
    {"id": 9, "name": "姜勇志", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "皋兰县委常委、副县长(挂职)",
     "current_org": "皋兰县人民政府",
     "source": "https://www.gaolan.gov.cn — 皋兰县政府网站班子成员页"},

    # 赵志军 — 副县长
    {"id": 10, "name": "赵志军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "皋兰县副县长",
     "current_org": "皋兰县人民政府",
     "source": "https://www.gaolan.gov.cn — 皋兰县政府网站班子成员页"},

    # 高丽遵 — 副县长
    {"id": 11, "name": "高丽遵", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "皋兰县副县长",
     "current_org": "皋兰县人民政府",
     "source": "https://www.gaolan.gov.cn — 皋兰县政府网站班子成员页"},

    # 何正春 — 县人大常委会主任
    {"id": 12, "name": "何正春", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "皋兰县人大常委会主任",
     "current_org": "皋兰县人大常委会",
     "source": "https://www.gaolan.gov.cn — 皋兰县两会报道（2026.01）"},

    # 彭斌嘉 — 县政协主席
    {"id": 13, "name": "彭斌嘉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "皋兰县政协主席",
     "current_org": "皋兰县政协",
     "source": "https://www.gaolan.gov.cn — 皋兰县政府网站"},

    # ── C. Predecessors ──

    # 范仲阔 — 前任皋兰县长 (2021-2025)
    {"id": 14, "name": "范仲阔", "gender": "男", "ethnicity": "土族",
     "birth": "1975-10", "birthplace": "甘肃永靖",
     "education": "省委党校研究生学历，管理学学士（西北民族学院工商行政管理专业）",
     "party_join": "中共党员", "work_start": "1999-07",
     "current_post": "原皋兰县长",
     "current_org": "原皋兰县人民政府",
     "source": "https://www.gaolan.gov.cn — 皋兰县政府网站范仲阔页面; 百度百科"},

    # 杜宁让 — 更早前任皋兰县长 (2013-2021)
    {"id": 15, "name": "杜宁让", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-08", "birthplace": "甘肃宁县",
     "education": "在职研究生学历，公共管理博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原皋兰县长（已晋升）",
     "current_org": "原皋兰县人民政府",
     "source": "https://www.lanzhou.gov.cn — 兰州市委组织部任前公示（2019.11）; 人民网（2021.07）"},

    # 宗满德 — 前任皋兰县委书记
    {"id": 16, "name": "宗满德", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原皋兰县委书记",
     "current_org": "原中共皋兰县委",
     "source": "公开报道 — 皋兰历任县委书记资料"},

    # 尤占海 — 更早皋兰县委书记
    {"id": 17, "name": "尤占海", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原皋兰县委书记",
     "current_org": "原中共皋兰县委",
     "source": "公开报道 — 兰州市委常委会决定"},

    # ── D. City-level leaders (Lanzhou) ──

    {"id": 18, "name": "张晓强", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-11", "birthplace": "浙江庆元",
     "education": "浙江林学院林学专业、美国肯恩大学公共管理硕士",
     "party_join": "1996-06", "work_start": "1996-08",
     "current_post": "甘肃省委常委、兰州市委书记",
     "current_org": "中共兰州市委员会",
     "source": "https://zh.wikipedia.org/wiki/%E5%BC%A0%E6%99%93%E5%BC%BA_(1975%E5%B9%B4)"},

    {"id": 19, "name": "刘建勋", "gender": "男", "ethnicity": "汉族",
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
    {"id": 1, "name": "中共皋兰县委", "type": "党委", "level": "县级", "parent": "中共兰州市委员会", "location": "甘肃省兰州市皋兰县"},
    {"id": 2, "name": "皋兰县人民政府", "type": "政府", "level": "县级", "parent": "兰州市人民政府", "location": "甘肃省兰州市皋兰县"},
    {"id": 3, "name": "中共皋兰县纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共皋兰县委", "location": "甘肃省兰州市皋兰县"},
    {"id": 4, "name": "中共皋兰县委组织部", "type": "党委", "level": "乡科级", "parent": "中共皋兰县委", "location": "甘肃省兰州市皋兰县"},
    {"id": 5, "name": "中共皋兰县委政法委员会", "type": "党委", "level": "乡科级", "parent": "中共皋兰县委", "location": "甘肃省兰州市皋兰县"},
    {"id": 6, "name": "皋兰县人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "甘肃省兰州市皋兰县"},
    {"id": 7, "name": "皋兰县政协", "type": "政协", "level": "县级", "parent": "", "location": "甘肃省兰州市皋兰县"},
    {"id": 8, "name": "皋兰县公安局", "type": "政府", "level": "乡科级", "parent": "皋兰县人民政府", "location": "甘肃省兰州市皋兰县"},

    # City-level
    {"id": 9, "name": "中共兰州市委员会", "type": "党委", "level": "副省级", "parent": "中共甘肃省委员会", "location": "甘肃省兰州市"},
    {"id": 10, "name": "兰州市人民政府", "type": "政府", "level": "副省级", "parent": "甘肃省人民政府", "location": "甘肃省兰州市"},
    {"id": 11, "name": "兰州新区管理委员会", "type": "政府", "level": "副省级", "parent": "甘肃省人民政府", "location": "甘肃省兰州市兰州新区"},

    # Provincial-level
    {"id": 12, "name": "中共甘肃省委员会", "type": "党委", "level": "省级", "parent": "", "location": "甘肃省兰州市"},
    {"id": 13, "name": "甘肃省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "甘肃省兰州市"},
]

# =========================================================================
# POSITIONS (current and historical)
# =========================================================================
positions = [
    # ── 康石 — 县委书记 career ──
    {"person_id": 1, "org_id": 1, "title": "皋兰县委书记", "start": "2020-05", "end": "", "rank": "正处", "note": "2021年11月连任第十五届县委书记"},
    {"person_id": 1, "org_id": 11, "title": "兰州新区党工委委员、管委会副主任", "start": "2026-05", "end": "", "rank": "副厅", "note": "兼任皋兰县委书记"},
    {"person_id": 1, "org_id": 12, "title": "甘肃省委组织部选调生", "start": "2010-07", "end": "2011", "rank": "", "note": "2010届甘肃省委组织部选调生"},

    # ── 沈毅 — 县长 career ──
    {"person_id": 2, "org_id": 2, "title": "皋兰县县长", "start": "2025-04", "end": "", "rank": "正处", "note": "2025年4月8日任代县长，4月14日当选"},
    {"person_id": 2, "org_id": 1, "title": "皋兰县委副书记", "start": "2025-03", "end": "", "rank": "正处", "note": ""},

    # 沈毅 prior career (from news reports)
    {"person_id": 2, "org_id": 9, "title": "兰州市西固区委（待确认具体职务）", "start": "2023", "end": "2025-03", "rank": "", "note": "任前公示显示来自西固区委"},
    {"person_id": 2, "org_id": 9, "title": "兰州市安宁区委（待确认具体职务）", "start": "", "end": "", "rank": "", "note": "媒体报道在安宁区任职"},
    {"person_id": 2, "org_id": 9, "title": "兰州市城关区临夏路街道党工委书记", "start": "2015", "end": "", "rank": "正科", "note": "2015年空降城关区"},
    {"person_id": 2, "org_id": 9, "title": "兰州市委常委办公室副主任", "start": "2013", "end": "2015", "rank": "", "note": "转业至兰州市委"},
    {"person_id": 2, "org_id": 9, "title": "兰州市委信息处副处长/副科级干部", "start": "2013", "end": "", "rank": "", "note": "转业后历任市委信息处多职"},

    # ── 刘冬青 ──
    {"person_id": 3, "org_id": 1, "title": "皋兰县委副书记", "start": "2021-08", "end": "", "rank": "副处", "note": "三级调研员"},
    {"person_id": 3, "org_id": 2, "title": "皋兰县副县长", "start": "2021-08", "end": "", "rank": "副处", "note": "县政府党组副书记"},

    # ── 张建华 ──
    {"person_id": 4, "org_id": 1, "title": "皋兰县委常委", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "皋兰县副县长", "start": "", "end": "", "rank": "副处", "note": "三级调研员"},

    # ── 张建龙 ──
    {"person_id": 5, "org_id": 1, "title": "皋兰县委常委", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 5, "org_id": 4, "title": "皋兰县委组织部部长", "start": "", "end": "", "rank": "副处", "note": "兼县委党校校长"},

    # ── 颜维祥 ──
    {"person_id": 6, "org_id": 1, "title": "皋兰县委常委", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 6, "org_id": 5, "title": "皋兰县委政法委书记", "start": "", "end": "", "rank": "副处", "note": ""},

    # ── 丁晓辉 ──
    {"person_id": 7, "org_id": 1, "title": "皋兰县委常委", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "皋兰县副县长", "start": "", "end": "", "rank": "副处", "note": ""},

    # ── 邵博 (挂职) ──
    {"person_id": 8, "org_id": 1, "title": "皋兰县委常委（挂职）", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "皋兰县副县长（挂职）", "start": "", "end": "", "rank": "", "note": ""},

    # ── 姜勇志 (挂职) ──
    {"person_id": 9, "org_id": 1, "title": "皋兰县委常委（挂职）", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "皋兰县副县长（挂职）", "start": "", "end": "", "rank": "", "note": ""},

    # ── 赵志军 ──
    {"person_id": 10, "org_id": 2, "title": "皋兰县副县长", "start": "", "end": "", "rank": "副处", "note": ""},

    # ── 高丽遵 ──
    {"person_id": 11, "org_id": 2, "title": "皋兰县副县长", "start": "", "end": "", "rank": "副处", "note": ""},

    # ── 何正春 ──
    {"person_id": 12, "org_id": 6, "title": "皋兰县人大常委会主任", "start": "", "end": "", "rank": "正处", "note": ""},

    # ── 彭斌嘉 ──
    {"person_id": 13, "org_id": 7, "title": "皋兰县政协主席", "start": "", "end": "", "rank": "正处", "note": ""},

    # ── 范仲阔 — 前任县长 ──
    {"person_id": 14, "org_id": 2, "title": "皋兰县县长", "start": "2021-08", "end": "2025-03", "rank": "正处", "note": "曾任代县长，后任县长"},
    {"person_id": 14, "org_id": 1, "title": "皋兰县委副书记", "start": "2021-08", "end": "2025-03", "rank": "正处", "note": ""},

    # ── 杜宁让 — 前任县长 ──
    {"person_id": 15, "org_id": 2, "title": "皋兰县县长", "start": "2013-12", "end": "2021-08", "rank": "正处", "note": "晋升副市（州）长人选"},

    # ── 宗满德 — 前任县委书记 ──
    {"person_id": 16, "org_id": 1, "title": "皋兰县委书记", "start": "2013-04", "end": "2020-05", "rank": "正处", "note": "接替徐大武"},

    # ── 尤占海 — 更早前任县委书记 ──
    {"person_id": 17, "org_id": 1, "title": "皋兰县委书记", "start": "", "end": "2013-04", "rank": "正处", "note": "由兰州市委常委会决定"},

    # ── City leaders ──
    {"person_id": 18, "org_id": 9, "title": "甘肃省委常委、兰州市委书记", "start": "2023-07", "end": "", "rank": "副部", "note": "全国最年轻省会市委书记"},
    {"person_id": 19, "org_id": 10, "title": "兰州市市长", "start": "2023-03", "end": "", "rank": "副部", "note": ""},
]

# =========================================================================
# RELATIONSHIPS (person↔person)
# =========================================================================
relationships = [
    # ── Core Leadership Pair ──
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "康石（县委书记）与沈毅（县长）党政搭档", "overlap_org": "皋兰县", "overlap_period": "2025-04至今"},

    # ── 康石 with key deputies ──
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记与县委副书记党政关系", "overlap_org": "中共皋兰县委", "overlap_period": "2021-08至今"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "县委书记与组织部部长工作关系", "overlap_org": "中共皋兰县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "县委书记与政法委书记工作关系", "overlap_org": "中共皋兰县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "同僚", "context": "县委书记与人大常委会主任同届共事", "overlap_org": "皋兰县", "overlap_period": ""},
    {"person_a": 1, "person_b": 13, "type": "同僚", "context": "县委书记与政协主席同届共事", "overlap_org": "皋兰县", "overlap_period": ""},

    # ── 沈毅 with deputies ──
    {"person_a": 2, "person_b": 3, "type": "党政搭档", "context": "县长与常务副县长（县委副书记兼）工作关系", "overlap_org": "皋兰县人民政府", "overlap_period": "2025-04至今"},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "县长与县委常委、副县长工作关系", "overlap_org": "皋兰县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "县长与县委常委、副县长工作关系", "overlap_org": "皋兰县人民政府", "overlap_period": ""},

    # ── Predecessor-Successor ──
    {"person_a": 1, "person_b": 16, "type": "前后任", "context": "康石（2020-）接替宗满德（2013-2020）任县委书记", "overlap_org": "中共皋兰县委", "overlap_period": "2020交接"},
    {"person_a": 16, "person_b": 17, "type": "前后任", "context": "宗满德接替尤占海任县委书记", "overlap_org": "中共皋兰县委", "overlap_period": "2013交接"},
    {"person_a": 2, "person_b": 14, "type": "前后任", "context": "沈毅（2025-）接替范仲阔（2021-2025）任县长", "overlap_org": "皋兰县人民政府", "overlap_period": "2025交接"},
    {"person_a": 14, "person_b": 15, "type": "前后任", "context": "范仲阔接替杜宁让（2013-2021）任县长", "overlap_org": "皋兰县人民政府", "overlap_period": "2021交接"},

    # ── 范仲阔 with 康石 (former pair) ──
    {"person_a": 1, "person_b": 14, "type": "党政搭档", "context": "康石（县委书记）与范仲阔（县长）曾党政搭档", "overlap_org": "皋兰县", "overlap_period": "2021-2025"},
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
    lines.append('    <description>皋兰县领导班子工作关系网络 — 包含县委书记、县长、领导班子成员及前后任关系</description>')
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
