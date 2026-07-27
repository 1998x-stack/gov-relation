#!/usr/bin/env python3
"""
康县领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Kang County leadership network.

Level: 县
Province: 甘肃省
Parent city: 陇南市
Region: 康县
Targets: 县委书记 & 县长

Research Sources:
- www.gskx.gov.cn (康县人民政府官网 - 领导之窗, 政务要闻)
- 康县人民政府官网确认的完整班子名单

Confirmed officeholders (as of 2026-07-22, from official website):
- 县委书记: 黄顺（男，汉族，1971年11月生，大学学历，中共党员）
- 县委副书记、县政府党组书记、县长: 杨满红（女，藏族，1978年10月生，研究生学历，中共党员）

Full 13-member Standing Committee roster confirmed from official source.

Research Date: 2026-07-22

NOTE: During the research session, Baidu Baike and web search tools (Exa)
were rate-limited or unavailable. Detailed biographies for core leaders
require follow-up investigation. Leadership names and roster are confirmed
from gskx.gov.cn official leadership page.
"""

import os
import sys
import sqlite3
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "康县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "康县_network.gexf")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── DATA ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": "p01",
        "name": "黄顺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年11月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共康县委书记",
        "current_org": "中共康县委员会",
        "source": "https://www.gskx.gov.cn/ldzc/index.html — 康县人民政府官网领导之窗",
        "person_id": "kangxian_huang_shun"
    },
    {
        "id": "p02",
        "name": "杨满红",
        "gender": "女",
        "ethnicity": "藏族",
        "birth": "1978年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "康县委副书记、县政府党组书记、县长",
        "current_org": "康县人民政府",
        "source": "https://www.gskx.gov.cn/ldzc/index.html — 康县人民政府官网领导之窗",
        "person_id": "kangxian_yang_manhong"
    },
    # ════════════════════════════════════════
    # Standing Committee Members (县委常委会)
    # ════════════════════════════════════════
    {
        "id": "p03",
        "name": "王斌",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "康县委副书记",
        "current_org": "中共康县委员会",
        "source": "https://www.gskx.gov.cn/ldzc/index.html",
        "person_id": "kangxian_wang_bin"
    },
    {
        "id": "p04",
        "name": "罗达",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "康县委常委、组织部部长",
        "current_org": "中共康县委员会组织部",
        "source": "https://www.gskx.gov.cn/ldzc/index.html",
        "person_id": "kangxian_luo_da"
    },
    {
        "id": "p05",
        "name": "赵海斌",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "康县委常委、常务副县长",
        "current_org": "康县人民政府",
        "source": "https://www.gskx.gov.cn/ldzc/index.html",
        "person_id": "kangxian_zhao_haibin"
    },
    {
        "id": "p06",
        "name": "秦明辉",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "康县委常委、统战部部长",
        "current_org": "中共康县委员会统战部",
        "source": "https://www.gskx.gov.cn/ldzc/index.html",
        "person_id": "kangxian_qin_minghui"
    },
    {
        "id": "p07",
        "name": "文博",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "康县委常委、政法委书记",
        "current_org": "中共康县委员会政法委员会",
        "source": "https://www.gskx.gov.cn/ldzc/index.html",
        "person_id": "kangxian_wen_bo"
    },
    {
        "id": "p08",
        "name": "李凯",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "康县委常委、宣传部部长",
        "current_org": "中共康县委员会宣传部",
        "source": "https://www.gskx.gov.cn/ldzc/index.html",
        "person_id": "kangxian_li_kai"
    },
    {
        "id": "p09",
        "name": "王源德",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "康县委常委、副县长",
        "current_org": "康县人民政府",
        "source": "https://www.gskx.gov.cn/ldzc/index.html",
        "person_id": "kangxian_wang_yuande"
    },
    {
        "id": "p10",
        "name": "杨彬",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "康县委常委、县纪委书记、县监委主任",
        "current_org": "中共康县纪律检查委员会",
        "source": "https://www.gskx.gov.cn/ldzc/index.html",
        "person_id": "kangxian_yang_bin"
    },
    {
        "id": "p11",
        "name": "连小平",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "康县委常委、人武部部长",
        "current_org": "康县人民武装部",
        "source": "https://www.gskx.gov.cn/ldzc/index.html",
        "person_id": "kangxian_lian_xiaoping"
    },
    {
        "id": "p12",
        "name": "李正军",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "康县委常委、副县长（挂职）",
        "current_org": "康县人民政府",
        "source": "https://www.gskx.gov.cn/ldzc/index.html",
        "person_id": "kangxian_li_zhengjun"
    },
    {
        "id": "p13",
        "name": "李海涛",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "康县委常委、副县长（挂职）",
        "current_org": "康县人民政府",
        "source": "https://www.gskx.gov.cn/ldzc/index.html",
        "person_id": "kangxian_li_haitao"
    },
    # ════════════════════════════════════════
    # Other Government Leaders
    # ════════════════════════════════════════
    {
        "id": "p14",
        "name": "李勇",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "康县副县长",
        "current_org": "康县人民政府",
        "source": "https://www.gskx.gov.cn/ldzc/index.html",
        "person_id": "kangxian_li_yong"
    },
    {
        "id": "p15",
        "name": "杜剑",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "康县副县长",
        "current_org": "康县人民政府",
        "source": "https://www.gskx.gov.cn/ldzc/index.html",
        "person_id": "kangxian_du_jian"
    },
    {
        "id": "p16",
        "name": "左武顺",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "康县副县长、公安局党委书记、局长",
        "current_org": "康县公安局",
        "source": "https://www.gskx.gov.cn/ldzc/index.html",
        "person_id": "kangxian_zuo_wushun"
    },
    {
        "id": "p17",
        "name": "陈录元",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "康县副县长（挂职）",
        "current_org": "康县人民政府",
        "source": "https://www.gskx.gov.cn/ldzc/index.html",
        "person_id": "kangxian_chen_luyuan"
    },
]

# 2. Organizations
organizations = [
    {"id": "o01", "name": "中共康县委员会", "type": "党委", "level": "县处级", "parent": "中共陇南市委员会", "location": "甘肃省陇南市康县"},
    {"id": "o02", "name": "康县人民政府", "type": "政府", "level": "县处级", "parent": "陇南市人民政府", "location": "甘肃省陇南市康县"},
    {"id": "o03", "name": "康县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "康县", "location": "甘肃省陇南市康县"},
    {"id": "o04", "name": "中国人民政治协商会议康县委员会", "type": "政协", "level": "县处级", "parent": "康县", "location": "甘肃省陇南市康县"},
    {"id": "o05", "name": "中共康县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共康县委员会", "location": "甘肃省陇南市康县"},
    {"id": "o06", "name": "中共康县委员会组织部", "type": "党委", "level": "县处级", "parent": "中共康县委员会", "location": "甘肃省陇南市康县"},
    {"id": "o07", "name": "中共康县委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共康县委员会", "location": "甘肃省陇南市康县"},
    {"id": "o08", "name": "中共康县委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共康县委员会", "location": "甘肃省陇南市康县"},
    {"id": "o09", "name": "中共康县委员会统战部", "type": "党委", "level": "县处级", "parent": "中共康县委员会", "location": "甘肃省陇南市康县"},
    {"id": "o10", "name": "康县人民武装部", "type": "事业单位", "level": "县处级", "parent": "陇南军分区", "location": "甘肃省陇南市康县"},
    {"id": "o11", "name": "康县公安局", "type": "政府", "level": "乡科级", "parent": "康县人民政府", "location": "甘肃省陇南市康县"},
    {"id": "o12", "name": "中共陇南市委员会", "type": "党委", "level": "地厅级", "parent": "中共甘肃省委员会", "location": "甘肃省陇南市武都区"},
    {"id": "o13", "name": "陇南市人民政府", "type": "政府", "level": "地厅级", "parent": "甘肃省人民政府", "location": "甘肃省陇南市武都区"},
]

# 3. Positions
positions = [
    # 黄顺 (p01)
    {"person_id": "p01", "org_id": "o01", "title": "康县委书记", "start": "待查", "end": "至今", "rank": "正处级", "note": "主持县委全面工作。官方确认截至2026年7月任职。具体到任时间待查。"},
    # 杨满红 (p02)
    {"person_id": "p02", "org_id": "o02", "title": "康县人民政府县长", "start": "待查", "end": "至今", "rank": "正处级", "note": "主持县政府全面工作。兼任县委副书记、县政府党组书记。"},
    {"person_id": "p02", "org_id": "o01", "title": "康县委副书记", "start": "待查", "end": "至今", "rank": "副处级", "note": "兼任县政府党组书记"},
    # 王斌 (p03)
    {"person_id": "p03", "org_id": "o01", "title": "康县委副书记", "start": "待查", "end": "至今", "rank": "副处级", "note": "专职副书记，协助书记处理县委日常工作"},
    # 罗达 (p04)
    {"person_id": "p04", "org_id": "o06", "title": "康县委组织部部长", "start": "待查", "end": "至今", "rank": "副处级", "note": "县委常委，负责组织人事工作"},
    {"person_id": "p04", "org_id": "o01", "title": "康县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 赵海斌 (p05)
    {"person_id": "p05", "org_id": "o02", "title": "康县常务副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "县委常委、县政府党组副书记、常务副县长。协助县长处理县政府日常工作。"},
    {"person_id": "p05", "org_id": "o01", "title": "康县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 秦明辉 (p06)
    {"person_id": "p06", "org_id": "o09", "title": "康县委统战部部长", "start": "待查", "end": "至今", "rank": "副处级", "note": "县委常委，负责统战工作"},
    {"person_id": "p06", "org_id": "o01", "title": "康县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 文博 (p07)
    {"person_id": "p07", "org_id": "o08", "title": "康县委政法委书记", "start": "待查", "end": "至今", "rank": "副处级", "note": "县委常委，负责政法工作"},
    {"person_id": "p07", "org_id": "o01", "title": "康县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 李凯 (p08)
    {"person_id": "p08", "org_id": "o07", "title": "康县委宣传部部长", "start": "待查", "end": "至今", "rank": "副处级", "note": "县委常委，负责宣传思想文化工作"},
    {"person_id": "p08", "org_id": "o01", "title": "康县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 王源德 (p09)
    {"person_id": "p09", "org_id": "o02", "title": "康县副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "县委常委，分管领域待查"},
    {"person_id": "p09", "org_id": "o01", "title": "康县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 杨彬 (p10)
    {"person_id": "p10", "org_id": "o05", "title": "康县纪委书记、监委主任", "start": "待查", "end": "至今", "rank": "副处级", "note": "县委常委，负责纪检监察工作"},
    {"person_id": "p10", "org_id": "o01", "title": "康县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 连小平 (p11)
    {"person_id": "p11", "org_id": "o10", "title": "康县人武部部长", "start": "待查", "end": "至今", "rank": "副处级", "note": "县委常委，负责武装工作"},
    {"person_id": "p11", "org_id": "o01", "title": "康县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 李正军 (p12) — 挂职
    {"person_id": "p12", "org_id": "o02", "title": "康县副县长（挂职）", "start": "待查", "end": "至今", "rank": "副处级", "note": "县委常委、挂职副县长"},
    {"person_id": "p12", "org_id": "o01", "title": "康县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 李海涛 (p13) — 挂职
    {"person_id": "p13", "org_id": "o02", "title": "康县副县长（挂职）", "start": "待查", "end": "至今", "rank": "副处级", "note": "县委常委、挂职副县长"},
    {"person_id": "p13", "org_id": "o01", "title": "康县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 李勇 (p14)
    {"person_id": "p14", "org_id": "o02", "title": "康县副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "副县长，分管领域待查"},
    # 杜剑 (p15)
    {"person_id": "p15", "org_id": "o02", "title": "康县副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "副县长，分管领域待查"},
    # 左武顺 (p16)
    {"person_id": "p16", "org_id": "o11", "title": "康县公安局局长", "start": "待查", "end": "至今", "rank": "乡科级", "note": "副县长兼任公安局党委书记、局长"},
    {"person_id": "p16", "org_id": "o02", "title": "康县副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 陈录元 (p17) — 挂职
    {"person_id": "p17", "org_id": "o02", "title": "康县副县长（挂职）", "start": "待查", "end": "至今", "rank": "副处级", "note": "挂职副县长"},
]

# 4. Relationships
relationships = [
    # 核心党政关系
    {"person_a": "p01", "person_b": "p02", "type": "overlap", "context": "黄顺(书记)与杨满红(县长): 康县党政一把手搭班配合", "overlap_org": "中共康县委员会/康县人民政府", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 书记与常务副县长
    {"person_a": "p01", "person_b": "p05", "type": "overlap", "context": "黄顺(书记)与赵海斌(常务副县长): 县委常委班子日常工作配合", "overlap_org": "中共康县委员会", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 书记与县纪委书记
    {"person_a": "p01", "person_b": "p10", "type": "overlap", "context": "黄顺(书记)与杨彬(纪委书记): 党风廉政建设工作配合", "overlap_org": "中共康县委员会", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    # 书记与组织部长
    {"person_a": "p01", "person_b": "p04", "type": "overlap", "context": "黄顺(书记)与罗达(组织部长): 干部任用工作配合", "overlap_org": "中共康县委员会", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    # 书记与副书记
    {"person_a": "p01", "person_b": "p03", "type": "overlap", "context": "黄顺(书记)与王斌(副书记): 县委日常工作配合", "overlap_org": "中共康县委员会", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    # 书记与政法委书记
    {"person_a": "p01", "person_b": "p07", "type": "overlap", "context": "黄顺(书记)与文博(政法委书记): 维稳工作配合", "overlap_org": "中共康县委员会", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    # 县长与常务副县长
    {"person_a": "p02", "person_b": "p05", "type": "overlap", "context": "杨满红(县长)与赵海斌(常务副县长): 县政府日常事务配合", "overlap_org": "康县人民政府", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 县长与副书记
    {"person_a": "p02", "person_b": "p03", "type": "overlap", "context": "杨满红(副书记)与王斌(副书记): 县委班子副职配合", "overlap_org": "中共康县委员会", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    # 全县常委班子内部关系（核心治理圈）
    {"person_a": "p01", "person_b": "p06", "type": "overlap", "context": "黄顺(书记)与秦明辉(统战部长): 县委班子日常工作配合", "overlap_org": "中共康县委员会", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p08", "type": "overlap", "context": "黄顺(书记)与李凯(宣传部长): 思想宣传文化工作配合", "overlap_org": "中共康县委员会", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p09", "type": "overlap", "context": "黄顺(书记)与王源德(副县长): 县委常委班子工作配合", "overlap_org": "中共康县委员会", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    # 政府内部关系
    {"person_a": "p02", "person_b": "p09", "type": "overlap", "context": "杨满红(县长)与王源德(副县长): 县政府班子配合", "overlap_org": "康县人民政府", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    {"person_a": "p02", "person_b": "p14", "type": "overlap", "context": "杨满红(县长)与李勇(副县长): 县政府班子配合", "overlap_org": "康县人民政府", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    {"person_a": "p02", "person_b": "p15", "type": "overlap", "context": "杨满红(县长)与杜剑(副县长): 县政府班子配合", "overlap_org": "康县人民政府", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    {"person_a": "p02", "person_b": "p16", "type": "overlap", "context": "杨满红(县长)与左武顺(副县长/公安局长): 政府与公安工作配合", "overlap_org": "康县人民政府", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    # 监督-组织协作关系
    {"person_a": "p10", "person_b": "p04", "type": "overlap", "context": "杨彬(纪委书记)与罗达(组织部长): 干部选拔与监督工作衔接", "overlap_org": "中共康县委员会", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
]

# ── Helper Functions ──

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return RGB color string based on current_post."""
    title = p["current_post"]
    if "县委书记" in title or ("书记" in title and "纪委" not in title and "人大" not in title and "政协" not in title and "组织" not in title and "宣传" not in title and "政法" not in title and "统战" not in title):
        return "255,50,50"    # Red — Party Secretary
    if "县长" in title and ("副书记" in title or "党组书记" in title):
        return "50,100,255"   # Blue — County Mayor
    if "县长" in title:
        return "50,100,255"   # Blue — Government head
    if "纪委" in title or "监委" in title:
        return "255,165,0"    # Orange — Discipline
    if "副书记" in title:
        return "200,50,50"    # Dark red — Deputy Secretary
    if "常委" in title:
        return "200,100,100"  # Pink — Other Standing Committee
    if "常务副县长" in title:
        return "100,100,200"  # Light blue — Executive Deputy Mayor
    if "副县长" in title:
        return "100,100,200"  # Light blue — Deputy Mayor
    if "人大" in title:
        return "200,255,255"  # Cyan — People's Congress
    if "政协" in title:
        return "255,240,200"  # Cream — CPPCC
    if "组织" in title:
        return "200,150,100"  # Brown — Organization
    if "宣传" in title:
        return "200,200,100"  # Yellow-green — Propaganda
    if "政法" in title:
        return "150,150,200"  # Purple-blue — Judiciary
    if "统战" in title:
        return "180,180,100"  # Olive — United Front
    return "100,100,100"      # Grey — Other

def person_size(p):
    """Return node size based on role."""
    title = p["current_post"]
    if "县委书记" in title or ("书记" in title and "纪委" not in title and "统战" not in title and "人大" not in title and "政协" not in title and "组织" not in title and "宣传" not in title and "政法" not in title):
        return "20.0"
    if "县长" in title and ("副书记" in title or "党组书记" in title):
        return "20.0"
    if "副书记" in title or "常委" in title:
        return "14.0"
    if "副县长" in title or "常务副县长" in title:
        return "12.0"
    if "人大" in title or "政协" in title:
        return "12.0"
    return "10.0"

def org_color(o):
    """Return RGB color string based on org type."""
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "事业单位": "220,220,220",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")

# ── Build Database ──

def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS persons (
        id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, native_place TEXT, education TEXT,
        party_join TEXT, work_start TEXT, current_post TEXT,
        current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT, org_id TEXT, title TEXT,
        start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT, person_b TEXT, type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    c.execute("DELETE FROM persons")
    c.execute("DELETE FROM organizations")
    c.execute("DELETE FROM positions")
    c.execute("DELETE FROM relationships")

    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            p["id"], p["name"], p["gender"], p["ethnicity"],
            p["birth"], p["birthplace"], p["native_place"], p["education"],
            p["party_join"], p["work_start"], p["current_post"],
            p["current_org"], p["source"]
        ))

    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""", (
            o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]
        ))

    for pos in positions:
        c.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
                     VALUES (?,?,?,?,?,?,?)""", (
            pos["person_id"], pos["org_id"], pos["title"],
            pos["start"], pos["end"], pos["rank"], pos["note"]
        ))

    for r in relationships:
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                     VALUES (?,?,?,?,?,?)""", (
            r["person_a"], r["person_b"], r["type"], r["context"],
            r["overlap_org"], r["overlap_period"]
        ))

    conn.commit()
    conn.close()

# ── Build GEXF ──

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>康县领导班子工作关系网络 - 数据来源: 康县人民政府官网(gskx.gov.cn)公开信息</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="province" type="string"/>')
    lines.append('      <attribute id="3" title="city" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('          <attvalue for="2" value="甘肃省"/>')
        lines.append('          <attvalue for="3" value="康县"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('          <attvalue for="2" value="甘肃省"/>')
        lines.append('          <attvalue for="3" value="康县"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person→Organization (worked_at)
    for pos in positions:
        eid += 1
        weight = "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person↔Person (relationship)
    for r in relationships:
        eid += 1
        weight = "2.0"
        conf = r.get("confidence", "plausible")
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{conf}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# ── Main ──

def main():
    print(f"=== 康县网络数据构建 ===")
    print(f"人员: {len(persons)} 人")
    print(f"组织机构: {len(organizations)} 个")
    print(f"任职记录: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")

    print(f"\n构建数据库...")
    build_db()
    db_size = os.path.getsize(DB_PATH)
    print(f"  ✓ {DB_PATH} ({db_size} bytes)")

    print(f"构建GEXF图文件...")
    build_gexf()
    gexf_size = os.path.getsize(GEXF_PATH)
    print(f"  ✓ {GEXF_PATH} ({gexf_size} bytes)")

    print(f"\n=== 完成 ===")

if __name__ == "__main__":
    main()
