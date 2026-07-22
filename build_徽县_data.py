#!/usr/bin/env python3
"""
徽县领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Huixian County leadership network.

Level: 县
Province: 甘肃省
Parent city: 陇南市
Region: 徽县
Targets: 县委书记 & 县长

Research Sources:
- www.gshxzf.gov.cn (徽县人民政府官网, 领导之窗页面)
- 徽县人民政府办公室新闻报道
- 徽县人民代表大会常务委员会任免名单

Confirmed officeholders (as of 2026-07-22, from official website):
- 县委书记: 王福全（二级巡视员）
- 县委副书记、政府县长: 刘鹏飞（一级调研员）

Research Date: 2026-07-22
"""

import os
import sys
import sqlite3
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "data/database/徽县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "data/graph/徽县_network.gexf")

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
        "name": "王福全",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年12月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "徽县委书记、二级巡视员",
        "current_org": "中共徽县委员会",
        "source": "徽县人民政府官网 - 领导之窗; 徽县人民政府新闻报道",
        "person_id": "huixian_wang_fuquan"
    },
    {
        "id": "p02",
        "name": "刘鹏飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "省委党校研究生、管理学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "徽县委副书记、政府县长、一级调研员",
        "current_org": "徽县人民政府",
        "source": "徽县人民政府官网 - 领导之窗; 徽县人民政府新闻报道",
        "person_id": "huixian_liu_pengfei"
    },
    # ════════════════════════════════════════
    # Current Standing Committee Members
    # Source: 徽县人民政府官网 领导之窗 (2026-07-22)
    # ════════════════════════════════════════
    {
        "id": "p03",
        "name": "任静",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "徽县委副书记",
        "current_org": "中共徽县委员会",
        "source": "徽县人民政府官网 - 领导之窗",
        "person_id": "huixian_ren_jing"
    },
    {
        "id": "p04",
        "name": "张军民",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "徽县委常委、政府常务副县长",
        "current_org": "徽县人民政府",
        "source": "徽县人民政府官网 - 领导之窗",
        "person_id": "huixian_zhang_junmin"
    },
    {
        "id": "p05",
        "name": "李军",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "徽县委常委、组织部部长",
        "current_org": "中共徽县委员会组织部",
        "source": "徽县人民政府官网 - 领导之窗",
        "person_id": "huixian_li_jun"
    },
    {
        "id": "p06",
        "name": "杨宇琛",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "徽县委常委、纪委书记、县监委主任",
        "current_org": "中共徽县纪律检查委员会",
        "source": "徽县人民政府官网 - 领导之窗",
        "person_id": "huixian_yang_yuchen"
    },
    {
        "id": "p07",
        "name": "董启军",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "徽县委常委、宣传部部长",
        "current_org": "中共徽县委员会宣传部",
        "source": "徽县人民政府官网 - 领导之窗",
        "person_id": "huixian_dong_qijun"
    },
    {
        "id": "p08",
        "name": "毛鲜花",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "徽县委常委、政法委书记",
        "current_org": "中共徽县委员会政法委员会",
        "source": "徽县人民政府官网 - 领导之窗",
        "person_id": "huixian_mao_xianhua"
    },
    {
        "id": "p09",
        "name": "李波",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "徽县委常委、政府副县长",
        "current_org": "徽县人民政府",
        "source": "徽县人民政府官网 - 领导之窗",
        "person_id": "huixian_li_bo"
    },
    {
        "id": "p10",
        "name": "张棚",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "徽县委常委、政府副县长",
        "current_org": "徽县人民政府",
        "source": "徽县人民政府官网 - 领导之窗",
        "person_id": "huixian_zhang_peng"
    },
    {
        "id": "p11",
        "name": "郭力源",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "徽县委常委、政府副县长",
        "current_org": "徽县人民政府",
        "source": "徽县人民政府官网 - 领导之窗",
        "person_id": "huixian_guo_liyuan"
    },
    {
        "id": "p12",
        "name": "肖辉",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "徽县委常委、统战部部长",
        "current_org": "中共徽县委员会统战部",
        "source": "徽县人民政府官网 - 领导之窗",
        "person_id": "huixian_xiao_hui"
    },
    # ════════════════════════════════════════
    # Other Government Leaders
    # Source: 徽县人民政府官网 领导之窗 (2026-07-22)
    # ════════════════════════════════════════
    {
        "id": "p13",
        "name": "杨茹",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "徽县政府副县长",
        "current_org": "徽县人民政府",
        "source": "徽县人民政府官网 - 领导之窗; 2025年1月人大常委会决定任命",
        "person_id": "huixian_yang_ru"
    },
    {
        "id": "p14",
        "name": "白东东",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "徽县政府副县长",
        "current_org": "徽县人民政府",
        "source": "徽县人民政府官网 - 领导之窗",
        "person_id": "huixian_bai_dongdong"
    },
    {
        "id": "p15",
        "name": "李云祥",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "徽县政府副县长人选",
        "current_org": "徽县人民政府",
        "source": "徽县人民政府官网 - 领导之窗",
        "person_id": "huixian_li_yunxiang"
    },
    {
        "id": "p16",
        "name": "何陶",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "徽县政府副县长人选",
        "current_org": "徽县人民政府",
        "source": "徽县人民政府官网 - 领导之窗",
        "person_id": "huixian_he_tao"
    },
]

# 2. Organizations
organizations = [
    {"id": "o01", "name": "中共徽县委员会", "type": "党委", "level": "县处级", "parent": "中共陇南市委员会", "location": "甘肃省陇南市徽县"},
    {"id": "o02", "name": "徽县人民政府", "type": "政府", "level": "县处级", "parent": "陇南市人民政府", "location": "甘肃省陇南市徽县"},
    {"id": "o03", "name": "徽县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "徽县", "location": "甘肃省陇南市徽县"},
    {"id": "o04", "name": "中国人民政治协商会议徽县委员会", "type": "政协", "level": "县处级", "parent": "徽县", "location": "甘肃省陇南市徽县"},
    {"id": "o05", "name": "中共徽县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共徽县委员会", "location": "甘肃省陇南市徽县"},
    {"id": "o06", "name": "中共徽县委员会组织部", "type": "党委", "level": "县处级", "parent": "中共徽县委员会", "location": "甘肃省陇南市徽县"},
    {"id": "o07", "name": "中共徽县委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共徽县委员会", "location": "甘肃省陇南市徽县"},
    {"id": "o08", "name": "中共徽县委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共徽县委员会", "location": "甘肃省陇南市徽县"},
    {"id": "o09", "name": "中共徽县委员会统战部", "type": "党委", "level": "县处级", "parent": "中共徽县委员会", "location": "甘肃省陇南市徽县"},
    {"id": "o10", "name": "中共陇南市委员会", "type": "党委", "level": "地厅级", "parent": "中共甘肃省委员会", "location": "甘肃省陇南市武都区"},
    {"id": "o11", "name": "陇南市人民政府", "type": "政府", "level": "地厅级", "parent": "甘肃省人民政府", "location": "甘肃省陇南市武都区"},
]

# 3. Positions
positions = [
    # 王福全 (p01) — 县委书记
    {"person_id": "p01", "org_id": "o01", "title": "徽县委书记", "start": "待查", "end": "至今", "rank": "正处级", "note": "主持县委全面工作。二级巡视员。具体任命时间待查。"},
    # 刘鹏飞 (p02) — 县长
    {"person_id": "p02", "org_id": "o02", "title": "徽县人民政府县长", "start": "待查", "end": "至今", "rank": "正处级", "note": "主持县政府全面工作，负责审计工作，主管县审计局。兼任县委副书记。一级调研员。"},
    {"person_id": "p02", "org_id": "o01", "title": "徽县委副书记", "start": "待查", "end": "至今", "rank": "副处级", "note": "兼任县政府党组书记。"},
    # 任静 (p03) — 县委副书记
    {"person_id": "p03", "org_id": "o01", "title": "徽县委副书记", "start": "待查", "end": "至今", "rank": "副处级", "note": "专职副书记。曾主持县委农村工作领导小组会议。"},
    {"person_id": "p03", "org_id": "o01", "title": "徽县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 张军民 (p04) — 常务副县长
    {"person_id": "p04", "org_id": "o02", "title": "徽县常务副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "县委常委、县政府党组副书记、常务副县长。"},
    {"person_id": "p04", "org_id": "o01", "title": "徽县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 李军 (p05) — 组织部长
    {"person_id": "p05", "org_id": "o06", "title": "徽县委组织部部长", "start": "待查", "end": "至今", "rank": "副处级", "note": "县委常委，负责组织人事工作。"},
    {"person_id": "p05", "org_id": "o01", "title": "徽县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 杨宇琛 (p06) — 纪委书记
    {"person_id": "p06", "org_id": "o05", "title": "徽县纪委书记、监委主任", "start": "待查", "end": "至今", "rank": "副处级", "note": "县委常委，负责纪检监察工作。"},
    {"person_id": "p06", "org_id": "o01", "title": "徽县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 董启军 (p07) — 宣传部长
    {"person_id": "p07", "org_id": "o07", "title": "徽县委宣传部部长", "start": "待查", "end": "至今", "rank": "副处级", "note": "县委常委，负责宣传思想文化工作。"},
    {"person_id": "p07", "org_id": "o01", "title": "徽县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 毛鲜花 (p08) — 政法委书记
    {"person_id": "p08", "org_id": "o08", "title": "徽县委政法委书记", "start": "待查", "end": "至今", "rank": "副处级", "note": "县委常委，负责政法工作。"},
    {"person_id": "p08", "org_id": "o01", "title": "徽县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 李波 (p09) — 县委常委、副县长
    {"person_id": "p09", "org_id": "o02", "title": "徽县政府副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "县委常委、政府副县长。"},
    {"person_id": "p09", "org_id": "o01", "title": "徽县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 张棚 (p10) — 县委常委、副县长
    {"person_id": "p10", "org_id": "o02", "title": "徽县政府副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "县委常委、政府副县长。"},
    {"person_id": "p10", "org_id": "o01", "title": "徽县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 郭力源 (p11) — 县委常委、副县长
    {"person_id": "p11", "org_id": "o02", "title": "徽县政府副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "县委常委、政府副县长。"},
    {"person_id": "p11", "org_id": "o01", "title": "徽县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 肖辉 (p12) — 统战部长
    {"person_id": "p12", "org_id": "o09", "title": "徽县委统战部部长", "start": "待查", "end": "至今", "rank": "副处级", "note": "县委常委，负责统战工作。"},
    {"person_id": "p12", "org_id": "o01", "title": "徽县委常委", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 杨茹 (p13) — 副县长
    {"person_id": "p13", "org_id": "o02", "title": "徽县政府副县长", "start": "2025-01", "end": "至今", "rank": "副处级", "note": "2025年1月9日徽县第十九届人大常委会第二十三次会议决定任命。"},
    # 白东东 (p14) — 副县长
    {"person_id": "p14", "org_id": "o02", "title": "徽县政府副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # 李云祥 (p15) — 副县长人选
    {"person_id": "p15", "org_id": "o02", "title": "徽县政府副县长人选", "start": "待查", "end": "至今", "rank": "副处级", "note": "副县长人选（待人大常委会任命）。"},
    # 何陶 (p16) — 副县长人选
    {"person_id": "p16", "org_id": "o02", "title": "徽县政府副县长人选", "start": "待查", "end": "至今", "rank": "副处级", "note": "副县长人选（待人大常委会任命）。"},
]

# 4. Relationships
relationships = [
    # 核心党政关系
    {"person_a": "p01", "person_b": "p02", "type": "overlap", "context": "王福全(书记)与刘鹏飞(县长): 徽县党政一把手搭班配合", "overlap_org": "中共徽县委员会/徽县人民政府", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 书记与专职副书记
    {"person_a": "p01", "person_b": "p03", "type": "overlap", "context": "王福全(书记)与任静(副书记): 县委班子日常配合", "overlap_org": "中共徽县委员会", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 县长与专职副书记
    {"person_a": "p02", "person_b": "p03", "type": "overlap", "context": "刘鹏飞(县长)与任静(副书记): 县委班子日常配合", "overlap_org": "中共徽县委员会", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    # 书记与常务副县长
    {"person_a": "p01", "person_b": "p04", "type": "overlap", "context": "王福全(书记)与张军民(常务副县长): 县委与政府日常工作配合", "overlap_org": "中共徽县委员会", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 县长与常务副县长
    {"person_a": "p02", "person_b": "p04", "type": "overlap", "context": "刘鹏飞(县长)与张军民(常务副县长): 县政府一、二把手工作关系", "overlap_org": "徽县人民政府", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 书记与纪委书记
    {"person_a": "p01", "person_b": "p06", "type": "overlap", "context": "王福全(书记)与杨宇琛(纪委书记): 县委与纪委工作关系", "overlap_org": "中共徽县委员会", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    # 书记与组织部长
    {"person_a": "p01", "person_b": "p05", "type": "overlap", "context": "王福全(书记)与李军(组织部长): 干部任用工作配合", "overlap_org": "中共徽县委员会", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    # 书记与宣传部长
    {"person_a": "p01", "person_b": "p07", "type": "overlap", "context": "王福全(书记)与董启军(宣传部长): 宣传思想工作配合", "overlap_org": "中共徽县委员会", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    # 书记与政法委书记
    {"person_a": "p01", "person_b": "p08", "type": "overlap", "context": "王福全(书记)与毛鲜花(政法委书记): 政法维稳工作配合", "overlap_org": "中共徽县委员会", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    # 书记与统战部长
    {"person_a": "p01", "person_b": "p12", "type": "overlap", "context": "王福全(书记)与肖辉(统战部长): 统战工作配合", "overlap_org": "中共徽县委员会", "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    # 县长与各副县长（县委常委班子）
    {"person_a": "p02", "person_b": "p09", "type": "overlap", "context": "刘鹏飞(县长)与李波(副县长): 县政府工作配合", "overlap_org": "徽县人民政府", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p02", "person_b": "p10", "type": "overlap", "context": "刘鹏飞(县长)与张棚(副县长): 县政府工作配合", "overlap_org": "徽县人民政府", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p02", "person_b": "p11", "type": "overlap", "context": "刘鹏飞(县长)与郭力源(副县长): 县政府工作配合", "overlap_org": "徽县人民政府", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p02", "person_b": "p13", "type": "overlap", "context": "刘鹏飞(县长)与杨茹(副县长): 县政府工作配合", "overlap_org": "徽县人民政府", "overlap_period": "2025-01至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p02", "person_b": "p14", "type": "overlap", "context": "刘鹏飞(县长)与白东东(副县长): 县政府工作配合", "overlap_org": "徽县人民政府", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
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
    if "常委" in title and "常务副县长" in title:
        return "100,100,200"  # Light blue — Deputy Mayor (standing committee)
    if "组织" in title:
        return "200,150,100"  # Brown — Organization
    if "宣传" in title:
        return "200,200,100"  # Yellow-green — Propaganda
    if "政法" in title:
        return "150,150,200"  # Purple-blue — Judiciary
    if "统战" in title:
        return "200,180,220"  # Light purple — United Front
    if "常委" in title:
        return "200,100,100"  # Pink — Other Standing Committee
    if "副县长" in title or "常务副县长" in title:
        return "100,100,200"  # Light blue — Deputy Mayor
    if "人大" in title:
        return "200,255,255"  # Cyan — People's Congress
    if "政协" in title:
        return "255,240,200"  # Cream — CPPCC
    return "100,100,100"      # Grey — Other

def person_size(p):
    """Return node size based on role."""
    title = p["current_post"]
    if "县委书记" in title or "人大主任" in title or "政协主席" in title:
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
    lines.append('    <description>徽县领导班子工作关系网络 - 数据来源: 徽县人民政府官网领导之窗及公开新闻报道</description>')
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
        lines.append('          <attvalue for="3" value="徽县"/>')
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
        lines.append('          <attvalue for="3" value="徽县"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
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
    print(f"=== 徽县网络数据构建 ===")
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
