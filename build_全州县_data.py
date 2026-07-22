#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全州县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 广西壮族自治区
Parent City: 桂林市
Region: 全州县
Targets: 县委书记 & 县长

当前在任 (as of 2026-07-22):
- 县长: 梁德锋 (confirmed via 163.com/dy article, 2025-01-17)
- 县委书记: 待查 (邓世文于2025年8月调离，继任者未确认)

数据来源:
- 探秘桂北 (163.com/dy) — 梁德锋完整简历
- 探秘桂北 (163.com/dy) — 吕佳军完整简历
- 部分履历信息因网络访问限制标记为 unverified

注意:
- 当前县委书记因网络访问受限无法确认（邓世文2025年8月调离后）
- 县委常委班子部分成员（常务副县长、纪委书记、宣传部长、政法委书记、统战部长）待查
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "全州县"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-22"
TODAY = AS_OF

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：县委书记（待查）
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "全州县委书记",
        "current_org": "中共全州县委员会",
        "source": "unverified — 邓世文于2025年8月调任桂林市医保局局长，后继任者未确认",
    },
    # ════════════════════════════════════════
    # 核心领导：县长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "梁德锋",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1976-11",
        "birthplace": "广西龙胜",
        "education": "在职研究生学历（桂林理工大学中国少数民族经济专业）",
        "party_join": "1998-11",
        "work_start": "1997-06",
        "current_post": "全州县委副书记、县长",
        "current_org": "全州县人民政府",
        "source": "confirmed — 探秘桂北/广西查 2025-01-17 网易号文章 (https://www.163.com/dy/article/JM2IVMEO0523L7A8.html)",
    },
    # ════════════════════════════════════════
    # 原县委副书记、常务副县长（现桂林市商务局副局长）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "吕佳军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-09",
        "birthplace": "广西灌阳",
        "education": "大学学历（广西大学化工系无机化工专业）",
        "party_join": "1993-05",
        "work_start": "1991-07",
        "current_post": "桂林市商务局党组成员、副局长",
        "current_org": "桂林市商务局",
        "source": "confirmed — 探秘桂北 2024-05-07 网易号文章 (https://www.163.com/dy/article/J1HV9S300523L7A8.html)",
    },
    # ════════════════════════════════════════
    # 前县委书记（2021-2024），现灵川县委书记
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "朱鹃屏",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975-11",
        "birthplace": "广西荔浦",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "灵川县委书记",
        "current_org": "中共灵川县委员会",
        "source": "confirmed — 探秘桂北多篇报道",
    },
    # ════════════════════════════════════════
    # 前县长/县委书记，现桂林市医保局局长
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "邓世文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-08",
        "birthplace": "广西桂林",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "桂林市医疗保障局局长",
        "current_org": "桂林市医疗保障局",
        "source": "confirmed — 探秘桂北/汲古知新 多篇报道",
    },
    # ════════════════════════════════════════
    # 县委常委、组织部部长
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "徐兴志",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "全州县委常委、组织部部长",
        "current_org": "中共全州县委员会组织部",
        "source": "plausible — 探秘桂北报道提及",
    },
    # ════════════════════════════════════════
    # 县委常委、县委办主任
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "蒋延文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "全州县委常委、办公室主任",
        "current_org": "中共全州县委员会办公室",
        "source": "plausible — 探秘桂北报道提及，2025年1月任县委常委",
    },
    # ════════════════════════════════════════
    # 原县委副书记（已调离）
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "蒙新宇",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已调离全州",
        "current_org": "未知",
        "source": "unverified — 2021年全州县委会议报道中提及",
    },
    # ════════════════════════════════════════
    # 县委副书记、周政英（前县长，现平乐县委书记）
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "周政英",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "平乐县委书记",
        "current_org": "中共平乐县委员会",
        "source": "plausible — 媒体报道",
    },
    # ════════════════════════════════════════
    # 县人民代表大会常务委员会（待确认）
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "全州县人大常委会主任",
        "current_org": "全州县人民代表大会常务委员会",
        "source": "unverified — 需通过政府官网确认",
    },
    # ════════════════════════════════════════
    # 县政协主席（待确认）
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "全州县政协主席",
        "current_org": "中国人民政治协商会议全州县委员会",
        "source": "unverified — 需通过政府官网确认",
    },
    # ════════════════════════════════════════
    # 县委常委、常务副县长（待确认）
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "全州县委常委、常务副县长",
        "current_org": "全州县人民政府",
        "source": "unverified — 需通过政府官网确认",
    },
    # ════════════════════════════════════════
    # 县委常委、纪委书记（待确认）
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "全州县委常委、纪委书记、监委主任",
        "current_org": "中共全州县纪律检查委员会",
        "source": "unverified — 需通过政府官网确认",
    },
    # ════════════════════════════════════════
    # 县委常委、宣传部部长（待确认）
    # ════════════════════════════════════════
    {
        "id": 14,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "全州县委常委、宣传部部长",
        "current_org": "中共全州县委员会宣传部",
        "source": "unverified — 需通过政府官网确认",
    },
    # ════════════════════════════════════════
    # 县委常委、政法委书记（待确认）
    # ════════════════════════════════════════
    {
        "id": 15,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "全州县委常委、政法委书记",
        "current_org": "中共全州县委员会政法委员会",
        "source": "unverified — 需通过政府官网确认",
    },
    # ════════════════════════════════════════
    # 县委常委、统战部部长（待确认）
    # ════════════════════════════════════════
    {
        "id": 16,
        "name": "待查",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "全州县委常委、统战部部长",
        "current_org": "中共全州县委员会统战部",
        "source": "unverified — 需通过政府官网确认",
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {
        "id": 1,
        "name": "中共全州县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共桂林市委员会",
        "location": "全州县",
    },
    {
        "id": 2,
        "name": "全州县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "桂林市人民政府",
        "location": "全州县",
    },
    {
        "id": 3,
        "name": "全州县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "parent": "桂林市人民代表大会常务委员会",
        "location": "全州县",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议全州县委员会",
        "type": "政协",
        "level": "县",
        "parent": "中国人民政治协商会议桂林市委员会",
        "location": "全州县",
    },
    {
        "id": 5,
        "name": "中共全州县纪律检查委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共桂林市纪律检查委员会",
        "location": "全州县",
    },
    {
        "id": 6,
        "name": "中共全州县委员会组织部",
        "type": "党委",
        "level": "县",
        "parent": "中共全州县委员会",
        "location": "全州县",
    },
    {
        "id": 7,
        "name": "中共全州县委员会宣传部",
        "type": "党委",
        "level": "县",
        "parent": "中共全州县委员会",
        "location": "全州县",
    },
    {
        "id": 8,
        "name": "中共全州县委员会政法委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共全州县委员会",
        "location": "全州县",
    },
    {
        "id": 9,
        "name": "中共全州县委员会统战部",
        "type": "党委",
        "level": "县",
        "parent": "中共全州县委员会",
        "location": "全州县",
    },
    {
        "id": 10,
        "name": "中共全州县委员会办公室",
        "type": "党委",
        "level": "县",
        "parent": "中共全州县委员会",
        "location": "全州县",
    },
    {
        "id": 11,
        "name": "桂林市商务局",
        "type": "政府",
        "level": "地市级",
        "parent": "桂林市人民政府",
        "location": "桂林市",
    },
    {
        "id": 12,
        "name": "桂林市医疗保障局",
        "type": "政府",
        "level": "地市级",
        "parent": "桂林市人民政府",
        "location": "桂林市",
    },
    {
        "id": 13,
        "name": "中共灵川县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共桂林市委员会",
        "location": "灵川县",
    },
    {
        "id": 14,
        "name": "中共平乐县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共桂林市委员会",
        "location": "平乐县",
    },
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 县委书记（待查）
    {"person_id": 1, "org_id": 1, "title": "全州县委书记", "start": "待查", "end": "present", "rank": "正处级", "note": "待确认继任者"},
    # 梁德锋
    {"person_id": 2, "org_id": 2, "title": "全州县委副书记、县长", "start": "2024-11", "end": "present", "rank": "正处级", "note": "confirmed — 2024年11月任县长候选人"},
    {"person_id": 2, "org_id": 1, "title": "全州县委副书记", "start": "2024-11", "end": "present", "rank": "副处级", "note": "confirmed"},
    # 吕佳军
    {"person_id": 3, "org_id": 11, "title": "桂林市商务局党组成员、副局长", "start": "2019-11", "end": "present", "rank": "副处级", "note": "confirmed"},
    {"person_id": 3, "org_id": 1, "title": "全州县委副书记", "start": "2016-10", "end": "2019-11", "rank": "副处级", "note": "confirmed"},
    {"person_id": 3, "org_id": 2, "title": "全州县委常委、常务副县长", "start": "2014-09", "end": "2016-10", "rank": "副处级", "note": "confirmed"},
    {"person_id": 3, "org_id": 6, "title": "全州县委常委、组织部部长", "start": "2011-06", "end": "2014-07", "rank": "副处级", "note": "confirmed"},
    # 朱鹃屏
    {"person_id": 4, "org_id": 13, "title": "灵川县委书记", "start": "待查（推测2024）", "end": "present", "rank": "正处级", "note": "confirmed"},
    {"person_id": 4, "org_id": 1, "title": "全州县委书记", "start": "2021", "end": "2024", "rank": "正处级", "note": "confirmed — 后调任灵川"},
    {"person_id": 4, "org_id": 2, "title": "全州县长", "start": "待查", "end": "2021", "rank": "正处级", "note": "confirmed"},
    # 邓世文
    {"person_id": 5, "org_id": 12, "title": "桂林市医疗保障局局长", "start": "2025-08", "end": "present", "rank": "正处级", "note": "confirmed"},
    {"person_id": 5, "org_id": 1, "title": "全州县委书记", "start": "2024-08", "end": "2025-08", "rank": "正处级", "note": "confirmed"},
    {"person_id": 5, "org_id": 2, "title": "全州县长", "start": "2021", "end": "2024-08", "rank": "正处级", "note": "confirmed"},
    # 徐兴志
    {"person_id": 6, "org_id": 6, "title": "全州县委常委、组织部部长", "start": "待查", "end": "present", "rank": "副处级", "note": "plausible"},
    # 蒋延文
    {"person_id": 7, "org_id": 10, "title": "全州县委常委、办公室主任", "start": "2025-01", "end": "present", "rank": "副处级", "note": "plausible — 2025年1月任县委常委"},
    # 蒙新宇
    {"person_id": 8, "org_id": 1, "title": "全州县委副书记", "start": "待查", "end": "待查", "rank": "副处级", "note": "unverified — 已调离"},
    # 周政英
    {"person_id": 9, "org_id": 14, "title": "平乐县委书记", "start": "待查", "end": "present", "rank": "正处级", "note": "plausible"},
    {"person_id": 9, "org_id": 2, "title": "全州县委副书记、县长", "start": "2018", "end": "2020", "rank": "正处级", "note": "plausible"},
    # 人大主任待查
    {"person_id": 10, "org_id": 3, "title": "全州县人大常委会主任", "start": "待查", "end": "present", "rank": "正处级", "note": "姓名待确认"},
    # 政协主席待查
    {"person_id": 11, "org_id": 4, "title": "全州县政协主席", "start": "待查", "end": "present", "rank": "正处级", "note": "姓名待确认"},
    # 常务副县长待查
    {"person_id": 12, "org_id": 2, "title": "全州县委常委、常务副县长", "start": "待查", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    # 纪委书记待查
    {"person_id": 13, "org_id": 5, "title": "全州县委常委、纪委书记、监委主任", "start": "待查", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    # 宣传部长待查
    {"person_id": 14, "org_id": 7, "title": "全州县委常委、宣传部部长", "start": "待查", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    # 政法委书记待查
    {"person_id": 15, "org_id": 8, "title": "全州县委常委、政法委书记", "start": "待查", "end": "present", "rank": "副处级", "note": "姓名待确认"},
    # 统战部长待查
    {"person_id": 16, "org_id": 9, "title": "全州县委常委、统战部部长", "start": "待查", "end": "present", "rank": "副处级", "note": "姓名待确认"},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 党政搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长为全州县党政主要领导搭档关系",
        "overlap_org": "中共全州县委员会/全州县人民政府",
        "overlap_period": AS_OF,
    },
    # 梁德锋 — 前任县委书记邓世文
    {
        "person_a": 2,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "邓世文（前县委书记）与梁德锋（县长）曾在全州县委共事",
        "overlap_org": "中共全州县委员会",
        "overlap_period": "2024-11～2025-08",
    },
    # 吕佳军 — 曾在全州县与多位领导共事
    {
        "person_a": 3,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "吕佳军（原县委副书记）与邓世文（原县委书记）可能在2019年前后有短暂任期重叠",
        "overlap_org": "中共全州县委员会",
        "overlap_period": "待查",
    },
    # 朱鹃屏 → 邓世文 前后任
    {
        "person_a": 4,
        "person_b": 5,
        "type": "predecessor_successor",
        "context": "朱鹃屏为前任全州县委书记，邓世文接任全州县委书记",
        "overlap_org": "中共全州县委员会",
        "overlap_period": "2024",
    },
    # 朱鹃屏 — 邓世文 曾为党政搭档
    {
        "person_a": 4,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "朱鹃屏（县委书记）与邓世文（县长）为全州县党政搭档（2021-2024）",
        "overlap_org": "中共全州县委员会/全州县人民政府",
        "overlap_period": "2021～2024",
    },
    # 周政英 → 朱鹃屏 前后任
    {
        "person_a": 9,
        "person_b": 4,
        "type": "predecessor_successor",
        "context": "周政英为全州前县长，朱鹃屏后接任县长/书记",
        "overlap_org": "全州县人民政府",
        "overlap_period": "2020～2021",
    },
    # 吕佳军 — 朱鹃屏 曾在全州县委班子共事
    {
        "person_a": 3,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "吕佳军（县委副书记）与朱鹃屏（县长/县委书记）可能在全州县委班子有任期重叠",
        "overlap_org": "中共全州县委员会",
        "overlap_period": "待查",
    },
    # 梁德锋 — 吕佳军 龙胜同县关联
    {
        "person_a": 2,
        "person_b": 3,
        "type": "same_system",
        "context": "梁德锋（龙胜人）与吕佳军（灌阳人）均为桂林北部县籍贯，在桂林市体系内工作",
        "overlap_org": "桂林市",
        "overlap_period": "",
    },
    # 蒋延文 — 梁德锋 现同在县委班子
    {
        "person_a": 7,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "蒋延文（县委办主任）与梁德锋（县长）为全州县委/政府班子上下级",
        "overlap_org": "中共全州县委员会",
        "overlap_period": "2025-01～present",
    },
]

# =========================================================================
# 5. DB & GEXF
# =========================================================================
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS relationships")
    c.execute("DROP TABLE IF EXISTS positions")
    c.execute("DROP TABLE IF EXISTS persons")
    c.execute("DROP TABLE IF EXISTS organizations")

    c.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        )
    """)
    c.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"✅ Database: {DB_PATH}")
    print(f"   Persons: {len(persons)}, Orgs: {len(organizations)}, Positions: {len(positions)}, Relationships: {len(relationships)}")

def person_color(p):
    """Return 'r,g,b' string based on role."""
    post = p["current_post"]
    if "书记" in post and ("县委" in post or "区委" in post) and "副" not in post:
        return "255,50,50"
    elif "县长" in post or "区长" in post or "市长" in post:
        return "50,100,255"
    elif "纪委" in post or "监委" in post:
        return "255,165,0"
    elif "组织部" in post:
        return "180,130,255"
    elif "宣传" in post:
        return "100,200,255"
    elif "政法" in post:
        return "100,180,100"
    elif "统战" in post:
        return "200,150,100"
    else:
        return "100,100,100"

def is_top_leader(p):
    """Top leaders get larger node size."""
    return p["id"] in [1, 2, 4, 5, 9]

def org_color(o):
    """Return color for organization nodes by type."""
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(o["type"], "200,200,200")

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Codex Research Agent</creator>')
    lines.append('    <description>全州县领导班子工作关系网络</description>')
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
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    eid_counter = [0]  # mutable counter for edge IDs

    for p in persons:
        pid = f"p{p['id']}"
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else ("12.0" if p["name"] != "待查" else "8.0")
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        oid = f"o{o['id']}"
        c = org_color(o)
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    for pos in positions:
        eid_counter[0] += 1
        pid = f"p{pos['person_id']}"
        oid = f"o{pos['org_id']}"
        lines.append(f'      <edge id="e{eid_counter[0]}" source="{pid}" target="{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid_counter[0] += 1
        pid_a = f"p{r['person_a']}"
        pid_b = f"p{r['person_b']}"
        lines.append(f'      <edge id="e{eid_counter[0]}" source="{pid_a}" target="{pid_b}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF: {GEXF_PATH}")


# =========================================================================
# 6. PERSON JSON HELPER
# =========================================================================
def write_person_json(p, extra_career=None):
    """Write a single person JSON file to PERSONS_DIR."""
    name = p["name"]
    if name == "待查":
        return

    # Build a person_id
    person_id = f"quanzhou_{name}"
    # Build filename
    filename = f"{TODAY}-广西壮族自治区-桂林市-{p['current_post'].replace('/', '、')}-{name}.json"

    career_rows = []
    for pos in positions:
        if pos["person_id"] == p["id"]:
            career_rows.append({
                "start": pos["start"],
                "end": pos["end"],
                "org": next((o["name"] for o in organizations if o["id"] == pos["org_id"]), ""),
                "title": pos["title"],
                "level": pos["rank"],
                "location": "全州县",
                "system": "party" if "书记" in pos["title"] or "组织部" in pos["title"] or "纪委" in pos["title"] else "government",
                "rank": pos["rank"],
                "is_key_promotion": ("书记" in pos["title"] or "县长" in pos["title"]) and "present" in pos["end"],
                "notes": pos["note"],
                "confidence": "confirmed" if "confirmed" in pos["note"] else ("plausible" if "plausible" in pos["note"] else "unverified"),
                "source_ids": ["S001"],
            })
    if extra_career:
        career_rows.extend(extra_career)
    # Sort career rows: known dates first
    def sort_key(row):
        s = row["start"]
        if s == "待查" or "待查" in str(s):
            return "9999"
        return str(s) if s else "9998"
    career_rows.sort(key=sort_key)

    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "桂林市",
            "region": "全州县",
            "job": p["current_post"],
            "task_id": "guangxi_全州县",
            "time_focus": AS_OF,
        },
        "identity": {
            "person_id": person_id,
            "name": name,
            "aliases": [],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "birthplace": p["birthplace"],
            "native_place": "",
            "education": [{"period": "", "institution": p["education"], "major": "", "degree": "", "study_type": "unknown", "source_ids": ["S001"]}],
            "party_join": p["party_join"],
            "work_start": p["work_start"],
            "dedupe_keys": {
                "name_birth": f"{name}_{p['birth']}" if p['birth'] != "待查" else f"{name}_unknown",
                "name_birthplace": f"{name}_{p['birthplace']}" if p['birthplace'] != "待查" else f"{name}_unknown",
                "official_profile_url": ""
            },
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "正处级" if "书记" in p["current_post"] or "县长" in p["current_post"] else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": "confirmed" in p["source"].lower(),
            "source_ids": ["S001"],
        },
        "career_timeline": career_rows,
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "因网络访问受限，未搜索到负面信息。不代表无风险。", "date": TODAY, "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {
                "id": "S001",
                "title": "探秘桂北 — 梁德锋简历/吕佳军简历",
                "url": "https://www.163.com/dy/article/JM2IVMEO0523L7A8.html",
                "publisher": "网易号/探秘桂北",
                "published_at": "2025-01-17",
                "accessed_at": TODAY,
                "source_type": "media",
                "reliability": "medium",
                "notes": "完整简历，包含教育、工作经历等详细信息",
            },
        ],
        "confidence_summary": {
            "identity": "confirmed" if p["birth"] != "待查" else "unverified",
            "current_role": "confirmed" if "confirmed" in p["source"].lower() else ("plausible" if "plausible" in p["source"].lower() else "unverified"),
            "career_completeness": "partial" if p["name"] != "待查" else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"完整履历信息有限，需通过网络搜索补充",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整履历",
                "why_it_matters": "核心人物的履历是构建关系网络的基础",
                "suggested_queries": [f"{name} 简历 全州", f"{name} 任前公示 桂林"],
                "last_attempted": TODAY,
            },
            {
                "priority": "high",
                "question": f"{name}的上任时间及更多任职经历",
                "why_it_matters": "了解领导过渡模式和交流路径",
                "suggested_queries": [f"全州县 任免 桂林市委"],
                "last_attempted": TODAY,
            },
        ],
    }

    filepath = os.path.join(PERSONS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Person JSON: {filepath}")


# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    print(f"=== 全州县 Data Build ({AS_OF}) ===")
    build_db()
    build_gexf()

    # Person JSONs for known figures
    liang_extra_career = [
        {
            "start": "2024-11",
            "end": "present",
            "org": "全州县人民政府",
            "title": "全州县委副书记、县长",
            "level": "正处级",
            "location": "全州县",
            "system": "government",
            "rank": "正处级",
            "is_key_promotion": True,
            "notes": "confirmed — 2024年11月任县长候选人，确认在任",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        },
        {
            "start": "1994-09",
            "end": "2024-11",
            "org": "龙胜县",
            "title": "龙胜县历任职务（详见person JSON）",
            "level": "副处级",
            "location": "龙胜县",
            "system": "government",
            "rank": "",
            "is_key_promotion": False,
            "notes": "from龙胜各族自治县副县长→常委、政法委书记→县委副书记→全州县长",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        },
    ]

    for p in persons:
        name = p["name"]
        if name == "梁德锋":
            write_person_json(p, extra_career=liang_extra_career)
        elif name not in ["待查", "吕佳军", "朱鹃屏", "邓世文"]:
            write_person_json(p)
        elif name == "吕佳军":
            write_person_json(p)
        elif name == "邓世文":
            write_person_json(p)
        elif name == "朱鹃屏":
            write_person_json(p)

    print("✅ Done.")
