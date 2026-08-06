#!/usr/bin/env python3
"""镇宁布依族苗族自治县（安顺市）领导班子关系网络数据生成脚本。

Targets: 县委书记 孙涛, 县长 欧靖
Data as of: 2026-08-05
Sources: 镇宁自治县人民政府官网 (www.gzzn.gov.cn), 安顺市人民政府官网 (www.anshun.gov.cn)
"""

import json
import os
import sqlite3
from datetime import datetime

TASK_ID = "guizhou_镇宁布依族苗族自治县"
SLUG = "镇宁布依族苗族自治县"
AS_OF = "2026-08-05"
PROVINCE = "贵州省"
PARENT_CITY = "安顺市"

BASE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else "data/tmp/guizhou_镇宁布依族苗族自治县"
_BASE_OVERRIDE = os.environ.get("ZHENNING_BASE")
if _BASE_OVERRIDE:
    BASE = _BASE_OVERRIDE

DB_PATH = os.path.join(BASE, "镇宁布依族苗族自治县_network.db")
GEXF_PATH = os.path.join(BASE, "镇宁布依族苗族自治县_network.gexf")
PERSONS_DIR = os.path.join(BASE, "persons")
os.makedirs(PERSONS_DIR, exist_ok=True)

# ── Data ──────────────────────────────────────────────────────────────────────

persons = [
    # 1 - 县委书记（一把手）
    {
        "id": 1,
        "name": "孙涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "镇宁布依族苗族自治县委书记",
        "current_org": "中共镇宁布依族苗族自治县委员会",
        "source": "https://www.gzzn.gov.cn/xw/ldhd/202607/t20260731_90681712.html",
    },
    # 2 - 县长（二把手）
    {
        "id": 2,
        "name": "欧靖",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1986年8月",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "镇宁布依族苗族自治县委副书记、县人民政府党组书记、县长",
        "current_org": "镇宁布依族苗族自治县人民政府",
        "source": "https://www.gzzn.gov.cn/gk/ldzc/202511/t20251114_88946524.html",
    },
    # 3 - 县委常委、常务副县长
    {
        "id": 3,
        "name": "徐杨",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1986年6月",
        "birthplace": "",
        "education": "大学，工程硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "镇宁布依族苗族自治县委常委、县人民政府党组副书记、常务副县长",
        "current_org": "镇宁布依族苗族自治县人民政府",
        "source": "https://www.gzzn.gov.cn/gk/ldzc/202107/t20210727_81653186.html",
    },
    # 4 - 县委常委、副县长
    {
        "id": 4,
        "name": "葛鑫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年10月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "镇宁布依族苗族自治县委常委、县人民政府副县长",
        "current_org": "镇宁布依族苗族自治县人民政府",
        "source": "https://www.gzzn.gov.cn/gk/ldzc/202309/t20230927_82519343.html",
    },
    # 5 - 县委常委、副县长（挂职）
    {
        "id": 5,
        "name": "郑冬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年12月",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "镇宁布依族苗族自治县委常委、县人民政府副县长（挂职）",
        "current_org": "镇宁布依族苗族自治县人民政府",
        "source": "https://www.gzzn.gov.cn/gk/ldzc/202406/t20240613_84865713.html",
    },
    # 6 - 县委常委、副县长（挂职）
    {
        "id": 6,
        "name": "陈晶炜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年7月",
        "birthplace": "",
        "education": "工商管理硕士，在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "镇宁布依族苗族自治县委常委、县人民政府副县长（挂职）",
        "current_org": "镇宁布依族苗族自治县人民政府",
        "source": "https://www.gzzn.gov.cn/gk/ldzc/202511/t20251105_88917589.html",
    },
    # 7 - 副县长、县公安局局长
    {
        "id": 7,
        "name": "鲍安华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年10月",
        "birthplace": "",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "镇宁布依族苗族自治县人民政府副县长、县公安局局长",
        "current_org": "镇宁布依族苗族自治县人民政府",
        "source": "https://www.gzzn.gov.cn/gk/ldzc/202201/t20220114_81653187.html",
    },
    # 8 - 副县长（女，布依族）
    {
        "id": 8,
        "name": "苏正兵",
        "gender": "男",
        "ethnicity": "布依族",
        "birth": "1974年10月",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "镇宁布依族苗族自治县人民政府副县长",
        "current_org": "镇宁布依族苗族自治县人民政府",
        "source": "https://www.gzzn.gov.cn/gk/ldzc/202201/t20220114_81653189.html",
    },
    # 9 副县长
    {
        "id": 9,
        "name": "匡永豪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年9月",
        "birthplace": "",
        "education": "理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "镇宁布依族苗族自治县人民政府副县长",
        "current_org": "镇宁布依族苗族自治县人民政府",
        "source": "https://www.gzzn.gov.cn/gk/ldzc/202511/t20251103_88899494.html",
    },
    # 10 副县长、县产业园区党工委书记
    {
        "id": 10,
        "name": "郑安",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "镇宁布依族苗族自治县人民政府副县长、县产业园区党工委书记",
        "current_org": "镇宁布依族苗族自治县人民政府",
        "source": "https://www.gzzn.gov.cn/gk/ldzc/202511/t20251103_88899844.html",
    },
    # 11 副县长
    {
        "id": 11,
        "name": "程守德",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989年8月",
        "birthplace": "",
        "education": "大学，管理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "镇宁布依族苗族自治县人民政府副县长",
        "current_org": "镇宁布依族苗族自治县人民政府",
        "source": "https://www.gzzn.gov.cn/gk/ldzc/202606/t20260603_90472287.html",
    },
    # 12 县政协主席
    {
        "id": 12,
        "name": "徐启才",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "镇宁布依族苗族自治县政协主席",
        "current_org": "中国人民政治协商会议镇宁布依族苗族自治县委员会",
        "source": "https://www.gzzn.gov.cn/xw/ldhd/202607/t20260731_90681712.html",
    },
    # 13 县人大常委会主任
    {
        "id": 13,
        "name": "罗昌华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "镇宁布依族苗族自治县人大常委会主任",
        "current_org": "镇宁布依族苗族自治县人大常委会",
        "source": "https://www.gzzn.gov.cn/xw/ldhd/",
    },
    # 14 县委常委、宣传部部长（拟任人大常委会主任）
    {
        "id": 14,
        "name": "卓颖",
        "gender": "女",
        "ethnicity": "土家族",
        "birth": "1972年3月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "镇宁布依族苗族自治县委常委、县委宣传部部长",
        "current_org": "中共镇宁布依族苗族自治县委宣传部",
        "source": "https://www.anshun.gov.cn/xwzx/gggs/202607/t20260726_90661120.html",
    },
    # 15 - 原县委组织部部长（2024年，现已调离位待核）
    {
        "id": 15,
        "name": "张海",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "镇宁布依族苗族自治县委常委、县委组织部部长（2024）",
        "current_org": "中共镇宁布依族苗族自治县委组织部",
        "source": "https://www.gzzn.gov.cn/xw/ldhd/202410/t20241023_85969872.html",
    },
    # 16 - 原县委副书记（2024-2025）
    {
        "id": 16,
        "name": "纳松",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "镇宁布依族苗族自治县委副书记（2024-2025）",
        "current_org": "中共镇宁布依族苗族自治县委员会",
        "source": "https://www.gzzn.gov.cn/xw/ldhd/202412/t20241209_86319426.html",
    },
    # 17 汛纪委副书记（2025）——纪委书记 何江鎏
    {
        "id": 17,
        "name": "何江鎏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "镇宁布依族苗族自治县纪委书记（2025）",
        "current_org": "中共镇宁布依族苗族自治县纪律检查委员会",
        "source": "https://www.gzzn.gov.cn/xw/ldhd/202501/t20250122_86668824.html",
    },
    # 18 - 前任县委书记
    {
        "id": 18,
        "name": "黄玮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "安顺市政协副主席、原镇宁县委书记",
        "current_org": "中国人民政治协商会议安顺市委员会",
        "source": "https://www.gzzn.gov.cn/xw/ldhd/202502/t20250205_86720931.html",
    },
    # 19 前任县长
    {
        "id": 19,
        "name": "刘文觉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "镇宁布依族苗族自治县原县委副书记、县长（2023-2025）",
        "current_org": "镇宁布依族苗族自治县人民政府",
        "source": "https://www.gzzn.gov.cn/xw/ldhd/202509/t20250930_88672214.html",
    },
    # 20 原常务副县长（2023）
    {
        "id": 20,
        "name": "骆桂",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "镇宁布依族苗族自治县委常委、常务副县长（2023）",
        "current_org": "镇宁布依族苗族自治县人民政府",
        "source": "https://www.gzzn.gov.cn/gk/ldzc/202107/t20210727_81653186.html",
    },
    # 21 州发展改革局局长（拟任副县长）
    {
        "id": 21,
        "name": "杨沫",
        "gender": "女",
        "ethnicity": "布依族",
        "birth": "1984年2月",
        "birthplace": "",
        "education": "大学，法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "镇宁布依族苗族自治县发展和改革局局长（拟任副县长）",
        "current_org": "镇宁布依族苗族自治县发展和改革局",
        "source": "https://www.anshun.gov.cn/xwzx/gggs/202607/t20260726_90661120.html",
    },
    # 22 原财政局长（拟任副县长）
    {
        "id": 22,
        "name": "罗栋",
        "gender": "男",
        "ethnicity": "布依族",
        "birth": "1986年6月",
        "birthplace": "",
        "education": "大学，工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "镇宁布依族苗族自治县财政局局长（拟任副县长）",
        "current_org": "镇宁布依族苗族自治县财政局",
        "source": "https://www.anshun.gov.cn/xwzx/gggs/202607/t20260719_90636374.html",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共镇宁布依族苗族自治县委员会", "type": "党委", "level": "县", "parent": "中共安顺市委员会", "location": "镇宁布依族苗族自治县"},
    {"id": 2, "name": "镇宁布依族苗族自治县人民政府", "type": "政府", "level": "县", "parent": "安顺市人民政府", "location": "镇宁布依族苗族自治县"},
    {"id": 3, "name": "镇宁布依族苗族自治县人大常委会", "type": "人大", "level": "县", "parent": "", "location": "镇宁布依族苗族自治县"},
    {"id": 4, "name": "中国人民政治协商会议镇宁布依族苗族自治县委员会", "type": "政协", "level": "县", "parent": "", "location": "镇宁布依族苗族自治县"},
    {"id": 5, "name": "镇宁布依族苗族自治县公安局", "type": "政府", "level": "县", "parent": "镇宁布依族苗族自治县人民政府", "location": "镇宁布依族苗族自治县"},
    {"id": 6, "name": "镇宁布依族苗族自治县发展和改革局", "type": "政府", "level": "县", "parent": "镇宁布依族苗族自治县人民政府", "location": "镇宁布依族苗族自治县"},
    {"id": 7, "name": "镇宁布依族苗族自治县财政局", "type": "政府", "level": "县", "parent": "镇宁布依族苗族自治县人民政府", "location": "镇宁布依族苗族自治县"},
    {"id": 8, "name": "中共镇宁布依族苗族自治县委组织部", "type": "党委", "level": "县", "parent": "中共镇宁布依族苗族自治县委员会", "location": "镇宁布依族苗族自治县"},
    {"id": 9, "name": "中国人民政治协商会议安顺市委员会", "type": "政协", "level": "市", "parent": "", "location": "安顺市"},
    {"id": 10, "name": "中共镇宁布依族苗族自治县委宣传部", "type": "党委", "level": "县", "parent": "中共镇宁布依族苗族自治县委员会", "location": "镇宁布依族苗族自治县"},
]

# ── Positions ─────────────────────────────────────────────────────────────────

positions = [
    # 孙涛（县委书记）
    {"person_id": 1, "org_id": 1, "title": "镇宁布依族苗族自治县委书记", "start_date": "2024年", "end_date": "", "rank": "县处级正职", "note": "2024年年中起任县委书记（官方新闻最早2024-07以县委书记身份出席）"},
    # 欧靖（县长）
    {"person_id": 2, "org_id": 2, "title": "镇宁布依族苗族自治县委副书记、县人民政府党组书记、县长", "start_date": "2025年", "end_date": "", "rank": "县处级正职", "note": "2025年接任县长（官方新闻2025-12以县长身份出席），2026-04兼任县经开区管委会主任"},
    {"person_id": 2, "org_id": 1, "title": "镇宁布依族苗族自治县委副书记", "start_date": "2025年", "end_date": "", "rank": "县处级副职", "note": "县委副书记"},
    # 徐杨（常务副县长）
    {"person_id": 3, "org_id": 2, "title": "镇宁布依族苗族自治县委常委、常务副县长、党组副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "2026-07任前公示拟任县委副书记"},
    # 葛鑫
    {"person_id": 4, "org_id": 2, "title": "镇宁布依族苗族自治县委常委、副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 郑冬（挂职）
    {"person_id": 5, "org_id": 2, "title": "镇宁布依族苗族自治县委常委、副县长（挂职）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "挂职干部"},
    # 陈晶炜（挂职）
    {"person_id": 6, "org_id": 2, "title": "镇宁布依族苗族自治县委常委、副县长（挂职）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "挂职干部"},
    # 鲍安华
    {"person_id": 7, "org_id": 2, "title": "镇宁布依族苗族自治县人民政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "镇宁布依族苗族自治县公安局局长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 苏正兵
    {"person_id": 8, "org_id": 2, "title": "镇宁布依族苗族自治县人民政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 匡永豪
    {"person_id": 9, "org_id": 2, "title": "镇宁布依族苗族自治县人民政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "2026-07拟任县委常委"},
    # 郑安
    {"person_id": 10, "org_id": 2, "title": "镇宁布依族苗族自治县人民政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "县产业园区党工委书记"},
    # 程守德
    {"person_id": 11, "org_id": 2, "title": "镇宁布依族苗族自治县人民政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 徐启才（政协主席）
    {"person_id": 12, "org_id": 4, "title": "镇宁布依族苗族自治县政协主席", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},
    # 罗昌华（人大主任）
    {"person_id": 13, "org_id": 3, "title": "镇宁布依族苗族自治县人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},
    # 卓颖（宣传部长）
    {"person_id": 14, "org_id": 10, "title": "镇宁布依族苗族自治县委常委、县委宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "2026-07拟任县人大常委会主任候选人"},
    # 张海（组织部长）
    {"person_id": 15, "org_id": 8, "title": "镇宁布依族苗族自治县委常委、县委组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "2024年任"},
    # 纳松（县委副书记）
    {"person_id": 16, "org_id": 1, "title": "镇宁布依族苗族自治县委副书记", "start_date": "2024年", "end_date": "2025年", "rank": "县处级副职", "note": "2024-2025年任县委副书记"},
    # 何江鎏（纪委书记）
    {"person_id": 17, "org_id": 1, "title": "镇宁布依族苗族自治县纪委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "2025年任纪委"},
    # 黄玮（前任书记）
    {"person_id": 18, "org_id": 1, "title": "镇宁布依族苗族自治县委书记", "start_date": "", "end_date": "2024年", "rank": "县处级正职", "note": "前任县委书记（兼安顺市政协副主席）"},
    {"person_id": 18, "org_id": 9, "title": "安顺市政协副主席", "start_date": "", "end_date": "", "rank": "副厅局级", "note": "兼任市政协副主席"},
    # 刘文觉（前任县长）
    {"person_id": 19, "org_id": 2, "title": "镇宁布依族苗族自治县委副书记、县长", "start_date": "2023年", "end_date": "2025年", "rank": "县处级正职", "note": "前任县长，2025年被欧靖接任"},
    # 骆桂（前常务副县长）
    {"person_id": 20, "org_id": 2, "title": "镇宁布依族苗族自治县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "2023年任，后被徐杨接任"},
    # 杨沫（发改局长）
    {"person_id": 21, "org_id": 6, "title": "镇宁布依族苗族自治县发展和改革局局长", "start_date": "", "end_date": "", "rank": "正科级", "note": "2026-07拟任副县长"},
    # 罗栋（财政局长）
    {"person_id": 22, "org_id": 7, "title": "镇宁布依族苗族自治县财政局局长", "start_date": "", "end_date": "", "rank": "正科级", "note": "2026-07拟任副县长"},
]

# ── Relationships ─────────────────────────────────────────────────────────────

relationships = [
    # 孙涛 → 欧靖（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "孙涛（书记）与欧靖（县长）为镇宁县党政正职搭档", "overlap_org": "镇宁布依族苗族自治县", "overlap_period": "2025年至今"},
    # 孙涛 → 刘文觉（前任搭档）
    {"person_a": 1, "person_b": 19, "type": "superior_subordinate", "context": "孙涛（书记）任内前期与刘文觉（县长）搭档", "overlap_org": "镇宁布依族苗族自治县", "overlap_period": "2024-2025"},
    # 孙涛 → 黄玮（前后任书记）
    {"person_a": 1, "person_b": 18, "type": "predecessor_successor", "context": "黄玮（2023-2024年任书记，兼安顺市政协副主席）→ 孙涛（2024年接任）", "overlap_org": "中共镇宁布依族苗族自治县委员会", "overlap_period": "2023-2024"},
    # 欧靖 → 刘文觉（前后任县长）
    {"person_a": 2, "person_b": 19, "type": "predecessor_successor", "context": "刘文觉（2023-2025年任县长）→ 欧靖（2025年接任）", "overlap_org": "镇宁布依族苗族自治县人民政府", "overlap_period": "2023-2025"},
    # 孙涛 → 徐杨（上下级）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "孙涛（书记）与徐杨（常务副县长）为县委常委会搭档", "overlap_org": "中共镇宁布依族苗族自治县委员会", "overlap_period": ""},
    # 欧靖 → 徐杨（正副手）
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "欧靖（县长）与徐杨（常务副县长）为县政府正副手搭档", "overlap_org": "镇宁布依族苗族自治县人民政府", "overlap_period": ""},
    # 欧靖 → 鲍安华（公安-政府副手）
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "欧靖（县长）领导鲍安华（副县长兼公安局长）", "overlap_org": "镇宁布依族苗族自治县人民政府", "overlap_period": ""},
    # 徐杨 → 匡永豪（拟任县委常委同列）
    {"person_a": 3, "person_b": 9, "type": "overlap", "context": "镇宁县政府领导班子同事", "overlap_org": "镇宁布依族苗族自治县人民政府", "overlap_period": ""},
    # 卓颖 → 罗昌华（人大主任继任关系）
    {"person_a": 14, "person_b": 13, "type": "overlap", "context": "卓颖（宣传部长）拟任县人大常委会主任候选人，与罗昌华（现主任）属人大体系交接", "overlap_org": "镇宁布依族苗族自治县人大常委会", "overlap_period": ""},
    # 纳松 → 徐杨（同任县委副书记位的前后）
    {"person_a": 16, "person_b": 3, "type": "overlap", "context": "纳松（2024-2025县委副书记），徐杨拟任县委副书记", "overlap_org": "中共镇宁布依族苗族自治县委员会", "overlap_period": ""},
    # 罗栋 / 杨沫 → 县政府（内升）
    {"person_a": 22, "person_b": 2, "type": "superior_subordinate", "context": "罗栋（财政局长）拟任副县长，县内晋升", "overlap_org": "镇宁布依族苗族自治县财政局", "overlap_period": ""},
    {"person_a": 21, "person_b": 2, "type": "superior_subordinate", "context": "杨沫（发改局长）拟任副县长，县内晋升", "overlap_org": "镇宁布依族苗族自治县发展和改革局", "overlap_period": ""},
]

# ── Person JSON 文件 ──────────────────────────────────────────────────────────

PERSON_JSONS = [
    {
        "filename": f"{AS_OF}-{PROVINCE}-{PARENT_CITY}-县委书记-孙涛.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": PROVINCE,
                "city": PARENT_CITY,
                "region": "镇宁布依族苗族自治县",
                "job": "县委书记",
                "task_id": TASK_ID,
                "time_focus": "2024-2026"
            },
            "identity": {
                "person_id": "zhenning_sun_tao",
                "name": "孙涛",
                "aliases": [],
                "gender": "",
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "孙涛_未知",
                    "name_birthplace": "",
                    "official_profile_url": "https://www.gzzn.gov.cn/xw/ldhd/202607/t20260731_90681712.html"
                }
            },
            "current_status": {
                "current_post": "镇宁布依族苗族自治县委书记",
                "current_org": "中共镇宁布依族苗族自治县委员会",
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002", "S010"]
            },
            "career_timeline": [
                {"start": "2024年", "end": "至今", "org": "中共镇宁布依族苗族自治县委员会", "title": "县委书记", "level": "县处级正职", "location": "镇宁县", "system": "party", "rank": "", "is_key_promotion": True, "notes": "2024年7月起以县委书记身份出席活动（官方新闻最早2024-07），此前职务公开资料未披露", "confidence": "confirmed", "source_ids": ["S010", "S011"]},
                {"start": "未知", "end": "2024年", "org": "履历缺口", "title": "", "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False, "notes": "公开资料未找到2024年7月前的完整履历（此前在安顺市直部门或区县的任职待查）", "confidence": "unverified", "source_ids": []}
            ],
            "organizations": [
                {"id": "org_zhenning_party", "name": "中共镇宁布依族苗族自治县委员会", "role": "现任领导", "period": "2024至今"}
            ],
            "relationships": [
                {"person": "欧靖", "person_id": "zhenning_ou_jing", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "党政正职搭档，共同出席县领导活动", "overlap_org": "镇宁布依族苗族自治县", "overlap_period": "2025年至今", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "黄玮", "person_id": "zhenning_huang_wei", "relationship_type": "predecessor_successor", "strength": "medium", "evidence": "黄玮（2023-2024任书记）→孙涛（2024接任）", "overlap_org": "中共镇宁布依族苗族自治县委员会", "overlap_period": "2023-2024", "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S006"]}
            ],
            "governance_record": [
                {"period": "2026", "domain": "other", "achievement_or_event": "多次赴乡镇（良田镇、马厂镇）调研乡村振兴、基层党建等重点工作", "role_in_event": "调研主持", "measurable_outcome": "", "location": "镇宁县", "confidence": "confirmed", "source_ids": ["S002"]}
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["party"],
                "geographic_pattern": ["镇宁县"],
                "promotion_velocity": {"summary": "2024年起任镇宁县委书记，此前履历待查", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "未发现负面立案审查或舆情信号", "date": "", "confidence": "plausible", "source_ids": []}
            ],
            "source_register": [
                {"id": "S001", "title": "孙涛欧靖徐启才等县领导开展八一走访慰问", "url": "https://www.gzzn.gov.cn/xw/ldhd/202607/t20260731_90681712.html", "publisher": "镇宁县人民政府网", "published_at": "2026-07-31", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认孙涛为县委书记、欧靖为县长"},
                {"id": "S002", "title": "孙涛到良田镇调研座谈", "url": "https://www.gzzn.gov.cn/xw/ldhd/202607/t20260716_90631032.html", "publisher": "镇宁县人民政府网", "published_at": "2026-07-16", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认孙涛为县委书记"},
                {"id": "S010", "title": "镇宁县领导活动档案（2024-2026历任书记活动）", "url": "https://www.gzzn.gov.cn/xw/ldhd/", "publisher": "镇宁县人民政府网", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "领导活动日志，用于梳理历任书记任职时段"},
                {"id": "S006", "title": "黄玮（市政协副主席、县委书记）活动报道", "url": "https://www.gzzn.gov.cn/xw/ldhd/202311/t20231108_83052872.html", "publisher": "镇宁县人民政府网", "published_at": "2023-11-08", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认黄玮曾任县委书记（兼安顺市政协副主席）"}
            ],
            "confidence_summary": {
                "identity": "partial",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "high",
                "biggest_gap": "孙涛任镇宁县委书记前的完整履历、出生年月、民族、教育背景"
            },
            "open_questions": [
                {"priority": "critical", "question": "孙涛在2024年7月任县委书记前的职业经历（此前在安顺市哪个单位或县区任职）？", "why_it_matters": "无法追踪其晋升路径和专业背景", "suggested_queries": ["孙涛 镇宁 县委书记 简历", "孙涛 安顺 任前公示"], "last_attempted": AS_OF},
                {"priority": "high", "question": "孙涛的出生年月、籍贯、民族、教育背景", "why_it_matters": "无法评估其政治资历和专业背景", "suggested_queries": ["孙涛 镇宁 出生"], "last_attempted": AS_OF}
            ]
        }
    },
    {
        "filename": "20260805-贵州省-安顺市-县长-欧靖.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": PROVINCE,
                "city": PARENT_CITY,
                "region": "镇宁布依族苗族自治县",
                "job": "县长",
                "task_id": TASK_ID,
                "time_focus": "2025-2026"
            },
            "identity": {
                "person_id": "zhenning_ou_jing",
                "name": "欧靖",
                "aliases": [],
                "gender": "男",
                "ethnicity": "苗族",
                "birth": "1986年8月",
                "birthplace": "",
                "native_place": "",
                "education": [{"period": "", "institution": "", "major": "", "degree": "本科", "study_type": "full_time", "source_ids": []}],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "欧靖_1986.08",
                    "name_birthplace": "",
                    "official_profile_url": "https://www.gzzn.gov.cn/gk/ldzc/202511/t20251114_88946524.html"
                }
            },
            "current_status": {
                "current_post": "镇宁布依族苗族自治县委副书记、县人民政府党组书记、县长",
                "current_org": "镇宁布依族苗族自治县人民政府",
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S101"]
            },
            "career_timeline": [
                {"start": "2025年", "end": "至今", "org": "镇宁布依族苗族自治县人民政府", "title": "县委副书记、县长", "level": "县处级正职", "location": "镇宁县", "system": "government", "rank": "", "is_key_promotion": True, "notes": "2025年接任县长（官方新闻2025-12首见以县长身份），2026-04兼任县经开区管委会主任", "confidence": "confirmed", "source_ids": ["S101", "S103"]},
                {"start": "未知", "end": "2025年", "org": "履历缺口", "title": "", "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False, "notes": "公开资料未找到2025年接任县长前的完整履历（可能来自安顺市内部调动或镇宁县内晋升）", "confidence": "unverified", "source_ids": []}
            ],
            "organizations": [
                {"id": "org_zhenning_gov", "name": "镇宁布依族苗族自治县人民政府", "role": "现任领导", "period": "2025至今"},
                {"id": "org_zhenning_party", "name": "中共镇宁布依族苗族自治县委员会", "role": "县委副书记", "period": "2025至今"}
            ],
            "relationships": [
                {"person": "孙涛", "person_id": "zhenning_sun_tao", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "党政正职搭档", "overlap_org": "镇宁布依族苗族自治县", "overlap_period": "2025年至今", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "刘文觉", "person_id": "zhenning_liu_wenjue", "relationship_type": "predecessor_successor", "strength": "medium", "evidence": "刘文觉（2023-2025县长）→欧靖（2025接任）", "overlap_org": "镇宁布依族苗族自治县人民政府", "overlap_period": "2023-2025", "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S104"]},
                {"person": "徐杨", "person_id": "zhenning_xu_yang", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "县长与常务副县长正副手搭档", "overlap_org": "镇宁布依族苗族自治县人民政府", "overlap_period": "", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S101"]}
            ],
            "governance_record": [
                {"period": "2026", "domain": "admin", "achievement_or_event": "主持召开县政府常务会议、到县住建局调研等项目", "role_in_event": "主持人/调研方", "measurable_outcome": "", "location": "镇宁县", "confidence": "confirmed", "source_ids": ["S102"]}
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["government"],
                "geographic_pattern": ["镇宁县"],
                "promotion_velocity": {"summary": "2025年任镇宁县长（苗族乡土年轻干部，1986年生）", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "未发现负面立案审查或舆情信号", "date": "", "confidence": "plausible", "source_ids": []}
            ],
            "source_register": [
                {"id": "S101", "title": "镇宁县领导之窗·欧靖简历", "url": "https://www.gzzn.gov.cn/gk/ldzc/202511/t20251114_88946524.html", "publisher": "镇宁县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认欧靖为县委副书记、县长"},
                {"id": "S102", "title": "欧靖主持召开县政府常务会议", "url": "https://www.gzzn.gov.cn/xw/ldhd/202605/t20260527_90219235.html", "publisher": "镇宁县人民政府", "published_at": "2026-05-27", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认欧靖主持县政府常务会议"},
                {"id": "S103", "title": "县人民政府关于欧靖等同志任职的通知（镇府任〔2026〕8号）", "url": "https://www.gzzn.gov.cn/gk/rsxx/rsrm/202604/t20260403_89965700.html", "publisher": "镇宁自治县人民政府", "published_at": "2026-04-03", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "欧靖兼任贵州镇宁经开区管委会主任"},
                {"id": "S104", "title": "镇宁县领导活动档案（历任县长时段）", "url": "https://www.gzzn.gov.cn/xw/ldhd/", "publisher": "镇宁县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "线索：刘文觉2023-2025任县长，欧靖2025接任"}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "high",
                "biggest_gap": "欧靖2025年接任县长前往的完整履历"
            },
            "open_questions": [
                {"priority": "critical", "question": "欧靖2025年任县长前的任职经历（此前在哪个县/市局任职）？", "why_it_matters": "无法判断其专业背景来源和是否跨县调动", "suggested_queries": ["欧靖 镇宁 简历", "欧靖 安顺 任职"], "last_attempted": AS_OF},
                {"priority": "high", "question": "欧靖的教育院校、专业和出生月份精确日期", "why_it_matters": "仅知本科、出生1986年8月", "suggested_queries": ["欧靖 出生", "欧靖 教育"], "last_attempted": AS_OF}
            ]
        }
    },
    {
        "filename": "20260805-贵州省-安顺市-常务副县长-徐杨.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": "2026-08-05",
            "investigation_scope": {
                "province": "贵州省",
                "city": "安顺市",
                "region": "镇宁布依族苗族自治县",
                "job": "常务副县长",
                "task_id": "guizhou_镇宁布依族苗族自治县",
                "time_focus": "2025-2026"
            },
            "identity": {
                "person_id": "zhenning_xu_yang",
                "name": "徐杨",
                "aliases": [],
                "gender": "女",
                "ethnicity": "汉族",
                "birth": "1986年6月",
                "birthplace": "",
                "native_place": "",
                "education": [{"period": "", "institution": "", "major": "", "degree": "工程硕士", "study_type": "full_time", "source_ids": ["S202"]}],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "徐杨_1986.06",
                    "name_birthplace": "",
                    "official_profile_url": "https://www.gzzn.gov.cn/gk/ldzc/202107/t20210727_81653186.html"
                }
            },
            "current_status": {
                "current_post": "镇宁自治县委常委、常务副县长（2026-07拟任县委副书记）",
                "current_org": "镇宁布依族苗族自治县人民政府",
                "administrative_rank": "县处级副职",
                "as_of": "2026-08-05",
                "is_current_confirmed": True,
                "source_ids": ["S201", "S202"]
            },
            "career_timeline": [],
            "organizations": [],
            "relationships": [
                {"person": "匡永豪", "person_id": "zhenning_kuang_yonghao", "relationship_type": "overlap", "strength": "weak", "evidence": "同为镇宁县跻身进入市党委常委名单（2026-07）", "overlap_org": "镇宁县人民政府", "overlap_period": "", "direction": "other_to_other", "confidence": "confirmed", "source_ids": ["S202"]}
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": ["财政金融"],
                "secondary_specializations": [],
                "career_pattern": "local_ladder",
                "systems_experience": ["government"],
                "geographic_pattern": ["镇宁县"],
                "promotion_velocity": {"summary": "从常务副县长拟任县委副书记（2026），属于现实提拔", "notable_fast_promotions": ["2026拟任县委副书记"]}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "未发现负面信号", "date": "", "confidence": "plausible", "source_ids": []}
            ],
            "source_register": [
                {"id": "S201", "title": "徐杨简历", "url": "https://www.gzzn.gov.cn/gk/ldzc/202107/t20210727_81653186.html", "publisher": "镇宁县人民政府", "published_at": "", "accessed_at": "2026-08-05", "source_type": "official", "reliability": "high", "notes": "常务副县长简历"},
                {"id": "S202", "title": "安顺市委组织部干部任前公示（2026-07-03）", "url": "https://www.anshun.gov.cn/xwzx/gggs/202607/t20260703_90586565.html", "publisher": "安顺市人民政府", "published_at": "2026-07-05", "accessed_at": "2026-08-05", "source_type": "official", "reliability": "high", "notes": "徐杨拟任县委副书记、匡永豪拟任县委常委"}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "徐杨任常务副县长前的完整履历"
            },
            "open_questions": [
                {"priority": "medium", "question": "徐杨任镇宁常务副县长前的任职经历", "why_it_matters": "作为拟任县委副书记的关键人物，履历不明", "suggested_queries": ["徐杨 镇宁 履历"], "last_attempted": "2026-08-05"}
            ]
        }
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
#  Build functions
# ═══════════════════════════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return GEXF color for a person based on role."""
    role = p.get("current_post", "")
    if "县委书记" in role or "书记" in role and "副书记" not in role:
        return "255,50,50"  # Red for party secretary
    if "县长" in role or "区长" in role:
        return "50,100,255"  # Blue for government head
    if "常务副" in role:
        return "50,100,255"
    if "挂职" in role:
        return "150,150,150"  # Grey for temporary
    if "人大" in role:
        return "200,255,255"  # Cyan for NPC
    if "政协" in role:
        return "255,240,200"  # Cream for CPPCC
    if "副" in role:
        return "100,150,255"  # Light blue for deputies
    if "局长" in role:
        return "150,150,150"
    return "100,100,100"


def is_top_leader(p):
    role = p.get("current_post", "")
    return "县委书记" in role or ("县长" in role and "副" not in role)


def org_color(org):
    t = org.get("type", "")
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")


def build_db():
    """创建并填充SQLite数据库。"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS relationships")
    cur.execute("DROP TABLE IF EXISTS positions")
    cur.execute("DROP TABLE IF EXISTS organizations")
    cur.execute("DROP TABLE IF EXISTS persons")

    cur.execute("""
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
        )
    """)
    cur.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        )
    """)
    cur.execute("""
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
        )
    """)
    cur.execute("""
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
        )
    """)

    for p in persons:
        cur.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education,
                                 party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
              p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
              p.get("party_join", ""), p.get("work_start", ""),
              p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
              o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos.get("title", ""),
              pos.get("start_date", ""), pos.get("end_date", ""),
              pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r.get("type", ""),
              r.get("context", ""), r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()

    print(f"DB: {DB_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")


def build_gexf():
    """生成 GEXF 1.3 图文件（含 viz namespace）。"""
    today = datetime.now().strftime("%Y-%m-%d")
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>镇宁布依族苗族自治县领导班子关系网络 (as of {AS_OF})</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="ethnicity" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else ("12.0" if p["id"] <= 3 else "10.0")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth", ""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("ethnicity", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('          <attvalue for="4" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    for r in relationships:
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r.get("type", ""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"GEXF: {GEXF_PATH}")
    print(f"  {len(persons)} person nodes")
    print(f"  {len(organizations)} org nodes")
    print(f"  {len(positions)} person-org edges")
    print(f"  {len(relationships)} person-person edges")


def write_person_jsons():
    for pj in PERSON_JSONS:
        path = os.path.join(PERSONS_DIR, pj["filename"])
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pj["data"], f, ensure_ascii=False, indent=2)
        print(f"Person JSON: {path}")


def main():
    print("=" * 60)
    print(f"  镇宁布依族苗族自治县领导班子关系网络")
    print(f"  Data as of: {AS_OF}")
    print(f"  Staging: {BASE}")
    print("=" * 60)
    print()
    build_db()
    print()
    build_gexf()
    print()
    write_person_jsons()
    print()
    print("Done.")


if __name__ == "__main__":
    main()