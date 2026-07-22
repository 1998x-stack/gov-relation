#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
桂林市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 地级市
Province: 广西壮族自治区
Parent City:
Region: 桂林市
Targets: 市委书记 & 市长

当前在任 (as of 2026-07-22):
- 市委书记: 郭忠志 (桂林市委书记)
- 市长: 卢新华 (桂林市委副书记、市长、市政府党组书记)
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "桂林市"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-22"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：市委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "郭忠志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "桂林市委书记",
        "current_org": "中共桂林市委员会",
        "source": "https://www.guilin.gov.cn/"
    },
    # ════════════════════════════════════════
    # 核心领导：市长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "卢新华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "桂林市委副书记、市长、市政府党组书记",
        "current_org": "桂林市人民政府/中共桂林市委员会",
        "source": "https://www.guilin.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldzc/"
    },
    # ════════════════════════════════════════
    # 市人大常委会主任
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "赵仲华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "桂林市人大常委会主任",
        "current_org": "桂林市人民代表大会常务委员会",
        "source": "https://www.guilin.gov.cn/"
    },
    # ════════════════════════════════════════
    # 市政协主席
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "罗试坚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "桂林市政协主席",
        "current_org": "中国人民政治协商会议桂林市委员会",
        "source": "https://www.guilin.gov.cn/"
    },
    # ════════════════════════════════════════
    # 市委常委/副市长
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "谢立品",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "桂林市委常委、副市长",
        "current_org": "中共桂林市委员会/桂林市人民政府",
        "source": "https://www.guilin.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldzc/"
    },
    {
        "id": 6,
        "name": "徐干君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "桂林市委常委、副市长",
        "current_org": "中共桂林市委员会/桂林市人民政府",
        "source": "https://www.guilin.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldzc/"
    },
    {
        "id": 7,
        "name": "杨莎莎",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "桂林市副市长",
        "current_org": "桂林市人民政府",
        "source": "https://www.guilin.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldzc/"
    },
    {
        "id": 8,
        "name": "龙杏华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "桂林市副市长",
        "current_org": "桂林市人民政府",
        "source": "https://www.guilin.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldzc/"
    },
    {
        "id": 9,
        "name": "孙环志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "桂林市副市长",
        "current_org": "桂林市人民政府",
        "source": "https://www.guilin.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldzc/"
    },
    {
        "id": 10,
        "name": "周彦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "桂林市副市长",
        "current_org": "桂林市人民政府",
        "source": "https://www.guilin.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldzc/"
    },
    {
        "id": 11,
        "name": "农健",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "桂林市副市长",
        "current_org": "桂林市人民政府",
        "source": "https://www.guilin.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldzc/"
    },
    {
        "id": 12,
        "name": "王红侠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "桂林市副市长",
        "current_org": "桂林市人民政府",
        "source": "https://www.guilin.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldzc/"
    },
    # ════════════════════════════════════════
    # 市政府秘书长
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "吴晓罡",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "桂林市政府秘书长",
        "current_org": "桂林市人民政府",
        "source": "https://www.guilin.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldzc/"
    },
    # ════════════════════════════════════════
    # 其他市委常委(从新闻中确认)
    # ════════════════════════════════════════
    {
        "id": 14,
        "name": "陈丽华",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "桂林市委常委、宣传部部长",
        "current_org": "中共桂林市委员会",
        "source": "https://www.guilin.gov.cn/"
    },
    {
        "id": 15,
        "name": "王列强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "桂林市委常委、纪委书记",
        "current_org": "中共桂林市纪律检查委员会",
        "source": "https://www.guilin.gov.cn/"
    },
    {
        "id": 16,
        "name": "赵奇玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "桂林市委常委、统战部部长",
        "current_org": "中共桂林市委员会",
        "source": "https://www.guilin.gov.cn/"
    },
    {
        "id": 17,
        "name": "蒋育亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "桂林市委常委、市委秘书长",
        "current_org": "中共桂林市委员会",
        "source": "https://www.guilin.gov.cn/"
    },
    {
        "id": 18,
        "name": "李军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "桂林市委常委、政法委书记",
        "current_org": "中共桂林市委员会",
        "source": "https://www.guilin.gov.cn/"
    },
    {
        "id": 19,
        "name": "陆波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "桂林市委常委",
        "current_org": "中共桂林市委员会",
        "source": "https://www.guilin.gov.cn/"
    },
    {
        "id": 20,
        "name": "程学武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "桂林市委常委、桂林警备区司令员",
        "current_org": "桂林警备区/中共桂林市委员会",
        "source": "https://www.guilin.gov.cn/"
    },
    {
        "id": 21,
        "name": "周卉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "桂林市委常委、组织部部长",
        "current_org": "中共桂林市委员会",
        "source": "https://www.guilin.gov.cn/"
    },
    # ════════════════════════════════════════
    # 人大副主任
    # ════════════════════════════════════════
    {
        "id": 22,
        "name": "区捷",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "桂林市人大常委会副主任",
        "current_org": "桂林市人民代表大会常务委员会",
        "source": "https://www.guilin.gov.cn/"
    },
    {
        "id": 23,
        "name": "杨玉霜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "桂林市人大常委会副主任",
        "current_org": "桂林市人民代表大会常务委员会",
        "source": "https://www.guilin.gov.cn/"
    },
    {
        "id": 24,
        "name": "韦文周",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "桂林市人大常委会副主任",
        "current_org": "桂林市人民代表大会常务委员会",
        "source": "https://www.guilin.gov.cn/"
    },
    {
        "id": 25,
        "name": "石长进",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "桂林市人大常委会副主任",
        "current_org": "桂林市人民代表大会常务委员会",
        "source": "https://www.guilin.gov.cn/"
    },
    # ════════════════════════════════════════
    # 政协副主席
    # ════════════════════════════════════════
    {
        "id": 26,
        "name": "文建中",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "桂林市政协副主席",
        "current_org": "中国人民政治协商会议桂林市委员会",
        "source": "https://www.guilin.gov.cn/"
    },
    {
        "id": 27,
        "name": "谭建国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "桂林市政协副主席",
        "current_org": "中国人民政治协商会议桂林市委员会",
        "source": "https://www.guilin.gov.cn/"
    },
    {
        "id": 28,
        "name": "王昕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "桂林市政协副主席",
        "current_org": "中国人民政治协商会议桂林市委员会",
        "source": "https://www.guilin.gov.cn/"
    },
    {
        "id": 29,
        "name": "郑平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "桂林市政协副主席",
        "current_org": "中国人民政治协商会议桂林市委员会",
        "source": "https://www.guilin.gov.cn/"
    },
    {
        "id": 30,
        "name": "谢永功",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "桂林市政协副主席",
        "current_org": "中国人民政治协商会议桂林市委员会",
        "source": "https://www.guilin.gov.cn/"
    },
    {
        "id": 31,
        "name": "卢全喜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "桂林市政协副主席",
        "current_org": "中国人民政治协商会议桂林市委员会",
        "source": "https://www.guilin.gov.cn/"
    },
    {
        "id": 32,
        "name": "孙国梁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "桂林市政协副主席",
        "current_org": "中国人民政治协商会议桂林市委员会",
        "source": "https://www.guilin.gov.cn/"
    },
    {
        "id": 33,
        "name": "莫振华",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "桂林市政协副主席",
        "current_org": "中国人民政治协商会议桂林市委员会",
        "source": "https://www.guilin.gov.cn/"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共桂林市委员会", "type": "党委", "level": "地级市", "parent": "", "location": "广西桂林市"},
    {"id": 2, "name": "桂林市人民政府", "type": "政府", "level": "地级市", "parent": "", "location": "广西桂林市"},
    {"id": 3, "name": "桂林市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "", "location": "广西桂林市"},
    {"id": 4, "name": "中国人民政治协商会议桂林市委员会", "type": "政协", "level": "地级市", "parent": "", "location": "广西桂林市"},
    {"id": 5, "name": "中共桂林市纪律检查委员会", "type": "纪委", "level": "地级市", "parent": "", "location": "广西桂林市"},
    {"id": 6, "name": "桂林警备区", "type": "党委", "level": "地级市", "parent": "", "location": "广西桂林市"},
    {"id": 7, "name": "中共桂林市委宣传部", "type": "党委", "level": "地级市", "parent": "中共桂林市委员会", "location": "广西桂林市"},
    {"id": 8, "name": "中共桂林市委统战部", "type": "党委", "level": "地级市", "parent": "中共桂林市委员会", "location": "广西桂林市"},
    {"id": 9, "name": "中共桂林市委政法委员会", "type": "党委", "level": "地级市", "parent": "中共桂林市委员会", "location": "广西桂林市"},
    {"id": 10, "name": "中共桂林市委组织部", "type": "党委", "level": "地级市", "parent": "中共桂林市委员会", "location": "广西桂林市"},
    {"id": 11, "name": "中共桂林市委办公室", "type": "党委", "level": "地级市", "parent": "中共桂林市委员会", "location": "广西桂林市"},
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 郭忠志 - 市委书记
    {"person_id": 1, "org_id": 1, "title": "桂林市委书记", "start_date": "待查", "end_date": "present", "rank": "正厅级", "note": ""},
    # 卢新华 - 市委副书记、市长
    {"person_id": 2, "org_id": 1, "title": "桂林市委副书记", "start_date": "待查", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "桂林市长、市政府党组书记", "start_date": "待查", "end_date": "present", "rank": "正厅级", "note": ""},
    # 赵仲华 - 市人大常委会主任
    {"person_id": 3, "org_id": 3, "title": "桂林市人大常委会主任", "start_date": "待查", "end_date": "present", "rank": "正厅级", "note": ""},
    # 罗试坚 - 市政协主席
    {"person_id": 4, "org_id": 4, "title": "桂林市政协主席", "start_date": "待查", "end_date": "present", "rank": "正厅级", "note": ""},
    # 谢立品 - 市委常委、副市长
    {"person_id": 5, "org_id": 1, "title": "桂林市委常委", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "桂林市副市长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 徐干君 - 市委常委、副市长
    {"person_id": 6, "org_id": 1, "title": "桂林市委常委", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "桂林市副市长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 杨莎莎 - 副市长
    {"person_id": 7, "org_id": 2, "title": "桂林市副市长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 龙杏华 - 副市长
    {"person_id": 8, "org_id": 2, "title": "桂林市副市长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 孙环志 - 副市长
    {"person_id": 9, "org_id": 2, "title": "桂林市副市长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 周彦 - 副市长
    {"person_id": 10, "org_id": 2, "title": "桂林市副市长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 农健 - 副市长
    {"person_id": 11, "org_id": 2, "title": "桂林市副市长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 王红侠 - 副市长
    {"person_id": 12, "org_id": 2, "title": "桂林市副市长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 吴晓罡 - 市政府秘书长
    {"person_id": 13, "org_id": 2, "title": "桂林市政府秘书长", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
    # 陈丽华 - 市委常委、宣传部部长
    {"person_id": 14, "org_id": 1, "title": "桂林市委常委", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 14, "org_id": 7, "title": "桂林市委宣传部部长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 王列强 - 市委常委、纪委书记
    {"person_id": 15, "org_id": 1, "title": "桂林市委常委", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 15, "org_id": 5, "title": "桂林市纪委书记", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 赵奇玲 - 市委常委、统战部部长
    {"person_id": 16, "org_id": 1, "title": "桂林市委常委", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 16, "org_id": 8, "title": "桂林市委统战部部长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 蒋育亮 - 市委常委、市委秘书长
    {"person_id": 17, "org_id": 1, "title": "桂林市委常委", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 17, "org_id": 11, "title": "桂林市委秘书长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 李军 - 市委常委、政法委书记
    {"person_id": 18, "org_id": 1, "title": "桂林市委常委", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 18, "org_id": 9, "title": "桂林市委政法委书记", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 陆波 - 市委常委
    {"person_id": 19, "org_id": 1, "title": "桂林市委常委", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 程学武 - 市委常委、警备区司令员
    {"person_id": 20, "org_id": 1, "title": "桂林市委常委", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 20, "org_id": 6, "title": "桂林警备区司令员", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 周卉 - 市委常委、组织部部长
    {"person_id": 21, "org_id": 1, "title": "桂林市委常委", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 21, "org_id": 10, "title": "桂林市委组织部部长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 区捷 - 市人大常委会副主任
    {"person_id": 22, "org_id": 3, "title": "桂林市人大常委会副主任", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 杨玉霜 - 市人大常委会副主任
    {"person_id": 23, "org_id": 3, "title": "桂林市人大常委会副主任", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 韦文周 - 市人大常委会副主任
    {"person_id": 24, "org_id": 3, "title": "桂林市人大常委会副主任", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 石长进 - 市人大常委会副主任
    {"person_id": 25, "org_id": 3, "title": "桂林市人大常委会副主任", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 文建中 - 市政协副主席
    {"person_id": 26, "org_id": 4, "title": "桂林市政协副主席", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 谭建国 - 市政协副主席
    {"person_id": 27, "org_id": 4, "title": "桂林市政协副主席", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 王昕 - 市政协副主席
    {"person_id": 28, "org_id": 4, "title": "桂林市政协副主席", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 郑平 - 市政协副主席
    {"person_id": 29, "org_id": 4, "title": "桂林市政协副主席", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 谢永功 - 市政协副主席
    {"person_id": 30, "org_id": 4, "title": "桂林市政协副主席", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 卢全喜 - 市政协副主席
    {"person_id": 31, "org_id": 4, "title": "桂林市政协副主席", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 孙国梁 - 市政协副主席
    {"person_id": 32, "org_id": 4, "title": "桂林市政协副主席", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    # 莫振华 - 市政协副主席
    {"person_id": 33, "org_id": 4, "title": "桂林市政协副主席", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 党政主要领导
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "郭忠志（市委书记）与卢新华（市长）为桂林市党政主要搭档", "overlap_org": "桂林市党政班子", "overlap_period": "2025-"},
    # 市委书记与市委常委
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "郭忠志（市委书记）与谢立品（市委常委、副市长）为市委班子领导关系", "overlap_org": "中共桂林市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "郭忠志（市委书记）与徐干君（市委常委、副市长）为市委班子领导关系", "overlap_org": "中共桂林市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 14, "type": "上下级", "context": "郭忠志（市委书记）与陈丽华（市委常委、宣传部部长）为市委班子领导关系", "overlap_org": "中共桂林市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 15, "type": "上下级", "context": "郭忠志（市委书记）与王列强（市委常委、纪委书记）为市委班子领导关系", "overlap_org": "中共桂林市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 16, "type": "上下级", "context": "郭忠志（市委书记）与赵奇玲（市委常委、统战部部长）为市委班子领导关系", "overlap_org": "中共桂林市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 17, "type": "上下级", "context": "郭忠志（市委书记）与蒋育亮（市委常委、市委秘书长）为市委班子领导关系", "overlap_org": "中共桂林市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 18, "type": "上下级", "context": "郭忠志（市委书记）与李军（市委常委、政法委书记）为市委班子领导关系", "overlap_org": "中共桂林市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 21, "type": "上下级", "context": "郭忠志（市委书记）与周卉（市委常委、组织部部长）为市委班子领导关系", "overlap_org": "中共桂林市委员会", "overlap_period": ""},
    # 市长与副市长
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "卢新华（市长）与谢立品（副市长）为市政府班子领导关系", "overlap_org": "桂林市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "卢新华（市长）与徐干君（副市长）为市政府班子领导关系", "overlap_org": "桂林市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "卢新华（市长）与杨莎莎（副市长）为市政府班子领导关系", "overlap_org": "桂林市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "卢新华（市长）与龙杏华（副市长）为市政府班子领导关系", "overlap_org": "桂林市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "卢新华（市长）与孙环志（副市长）为市政府班子领导关系", "overlap_org": "桂林市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "卢新华（市长）与周彦（副市长）为市政府班子领导关系", "overlap_org": "桂林市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "卢新华（市长）与农健（副市长）为市政府班子领导关系", "overlap_org": "桂林市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "卢新华（市长）与王红侠（副市长）为市政府班子领导关系", "overlap_org": "桂林市人民政府", "overlap_period": ""},
    # 市长与政府秘书长
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "卢新华（市长）与吴晓罡（市政府秘书长）为市政府班子工作关系", "overlap_org": "桂林市人民政府", "overlap_period": ""},
    # 人大主任与副主任
    {"person_a": 3, "person_b": 22, "type": "上下级", "context": "赵仲华（市人大常委会主任）与区捷（副主任）为市人大常委会班子成员", "overlap_org": "桂林市人民代表大会常务委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 23, "type": "上下级", "context": "赵仲华（市人大常委会主任）与杨玉霜（副主任）为市人大常委会班子成员", "overlap_org": "桂林市人民代表大会常务委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 24, "type": "上下级", "context": "赵仲华（市人大常委会主任）与韦文周（副主任）为市人大常委会班子成员", "overlap_org": "桂林市人民代表大会常务委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 25, "type": "上下级", "context": "赵仲华（市人大常委会主任）与石长进（副主任）为市人大常委会班子成员", "overlap_org": "桂林市人民代表大会常务委员会", "overlap_period": ""},
    # 政协主席与副主席
    {"person_a": 4, "person_b": 26, "type": "上下级", "context": "罗试坚（市政协主席）与文建中（副主席）为市政协班子成员", "overlap_org": "中国人民政治协商会议桂林市委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 27, "type": "上下级", "context": "罗试坚（市政协主席）与谭建国（副主席）为市政协班子成员", "overlap_org": "中国人民政治协商会议桂林市委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 28, "type": "上下级", "context": "罗试坚（市政协主席）与王昕（副主席）为市政协班子成员", "overlap_org": "中国人民政治协商会议桂林市委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 29, "type": "上下级", "context": "罗试坚（市政协主席）与郑平（副主席）为市政协班子成员", "overlap_org": "中国人民政治协商会议桂林市委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 30, "type": "上下级", "context": "罗试坚（市政协主席）与谢永功（副主席）为市政协班子成员", "overlap_org": "中国人民政治协商会议桂林市委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 31, "type": "上下级", "context": "罗试坚（市政协主席）与卢全喜（副主席）为市政协班子成员", "overlap_org": "中国人民政治协商会议桂林市委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 32, "type": "上下级", "context": "罗试坚（市政协主席）与孙国梁（副主席）为市政协班子成员", "overlap_org": "中国人民政治协商会议桂林市委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 33, "type": "上下级", "context": "罗试坚（市政协主席）与莫振华（副主席）为市政协班子成员", "overlap_org": "中国人民政治协商会议桂林市委员会", "overlap_period": ""},
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
    if "主席" in cp:
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
    lines.append(f'    <description>桂林市领导班子关系网络</description>')
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


def _infer_rank(post):
    if not post:
        return ""
    post_str = str(post)
    if "书记" in post_str and "副书记" not in post_str and "副" not in post_str.replace("副书记", ""):
        return "正厅级"
    if "市长" in post_str and "副" not in post_str:
        return "正厅级"
    if "主任" in post_str and "副" not in post_str:
        return "正厅级"
    if "主席" in post_str and "副" not in post_str:
        return "正厅级"
    if "副" in post_str:
        return "副厅级"
    if "秘书长" in post_str:
        return "正处级"
    return ""


def build_person_json(person, timeline, rels, sources):
    """Build a person graph JSON following the person_graph_json schema."""
    now = AS_OF.replace("-", "")
    slug = f"guilin_{person['name']}"

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "桂林市",
            "region": "桂林市",
            "job": person.get("current_post", ""),
            "task_id": "guangxi_桂林市",
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
            "biggest_gap": f"出生年月、籍贯、教育背景、入党时间等个人基本信息缺失。{person['name']}的完整履历（前任职务）需进一步调查。"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的出生年月和籍贯是什么？",
                "why_it_matters": "个人基本信息是身份识别的核心字段，无此信息无法进行跨人物去重和关联分析",
                "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 出生", f"{person['name']} 百度百科"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"{person['name']}的教育背景（学历、毕业院校、专业）是什么？",
                "why_it_matters": "学缘关系是构建人物关系网络的重要维度",
                "suggested_queries": [f"{person['name']} 学历", f"{person['name']} 毕业"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"{person['name']}的完整任职履历是怎样的？此前任何职？",
                "why_it_matters": "前序任职是构建继任关系和跨地区调任证据的关键",
                "suggested_queries": [f"{person['name']} 任职", f"{person['name']} 履历"],
                "last_attempted": AS_OF
            }
        ]
    }


def build_person_jsons():
    """Build individual person JSON files for core leaders."""
    now = AS_OF.replace("-", "")

    # ── Source register ──
    sources = [
        {"id": "S001", "title": "桂林市人民政府 — 首页新闻确认领导活动",
         "url": "https://www.guilin.gov.cn/", "publisher": "桂林市人民政府", "published_at": "",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "从政府首页新闻报道确认郭忠志（市委书记）、卢新华（市长）、赵仲华（人大主任）、罗试坚（政协主席）等人物的现任职务"},
        {"id": "S002", "title": "桂林市人民政府 — 领导之窗（市政府领导）",
         "url": "https://www.guilin.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldzc/", "publisher": "桂林市人民政府", "published_at": "",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "确认市长（卢新华）、8位副市长、市政府秘书长名单"},
        {"id": "S003", "title": "全市重点项目落地推进会召开 — 桂林日报",
         "url": "https://www.guilin.gov.cn/ywdt/zwdt/t27932493.shtml", "publisher": "桂林日报", "published_at": "2026-07-22",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "确认郭忠志（市委书记）、卢新华（市长）及谢立品、程学武、龙杏华、孙环志、王红侠等市领导出席"},
        {"id": "S004", "title": "市四家班子领导参加投票选举人大代表 — 桂林日报",
         "url": "https://www.guilin.gov.cn/ywdt/zwdt/t27923348.shtml", "publisher": "桂林日报", "published_at": "2026-07-21",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "完整列出市四家班子领导名单：郭忠志、卢新华、赵仲华（人大主任）、罗试坚（政协主席）及所有常委、副市长、人大副主任、政协副主席"},
    ]

    # ── 郭忠志 person JSON ──
    gzz_timeline = [
        {"start": "unknown", "end": "present", "org": "中共桂林市委员会", "title": "桂林市委书记",
         "level": "正厅级", "location": "广西桂林市", "system": "party", "rank": "正厅级",
         "is_key_promotion": True, "notes": "现任桂林市委书记（as of 2026-07-22）",
         "confidence": "confirmed", "source_ids": ["S001", "S003"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "公开资料未找到郭忠志任桂林市委书记前的完整履历。需进一步搜索：郭忠志 简历、郭忠志 任职经历等。",
         "confidence": "unverified", "source_ids": []},
    ]
    gzz_relationships = [
        {"person": "卢新华", "person_id": "guilin_卢新华", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "郭忠志（市委书记）与卢新华（市长）为桂林市党政主要搭档",
         "overlap_org": "桂林市党政班子",
         "overlap_period": "2025-",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
        {"person": "赵仲华", "person_id": "guilin_赵仲华", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "郭忠志（市委书记）与赵仲华（市人大常委会主任）为市四家班子主要领导",
         "overlap_org": "桂林市四家班子",
         "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
        {"person": "罗试坚", "person_id": "guilin_罗试坚", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "郭忠志（市委书记）与罗试坚（市政协主席）为市四家班子主要领导",
         "overlap_org": "桂林市四家班子",
         "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
    ]
    gzz_json = build_person_json(persons[0], gzz_timeline, gzz_relationships, sources)
    gzz_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-桂林市-市委书记-郭忠志.json")
    with open(gzz_path, "w", encoding="utf-8") as f:
        json.dump(gzz_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {gzz_path}")

    # ── 卢新华 person JSON ──
    lxh_timeline = [
        {"start": "unknown", "end": "present", "org": "桂林市人民政府/中共桂林市委员会", "title": "桂林市委副书记、市长、市政府党组书记",
         "level": "正厅级", "location": "广西桂林市", "system": "government", "rank": "正厅级",
         "is_key_promotion": True, "notes": "现任桂林市长（as of 2026-07-22）",
         "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "公开资料未找到卢新华任桂林市长前的完整履历。需进一步搜索：卢新华 简历、卢新华 任职经历等。",
         "confidence": "unverified", "source_ids": []},
    ]
    lxh_relationships = [
        {"person": "郭忠志", "person_id": "guilin_郭忠志", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "卢新华（市长）与郭忠志（市委书记）为桂林市党政主要搭档",
         "overlap_org": "桂林市党政班子",
         "overlap_period": "2025-",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
        {"person": "赵仲华", "person_id": "guilin_赵仲华", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "卢新华（市长）与赵仲华（市人大常委会主任）为市四家班子主要领导",
         "overlap_org": "桂林市四家班子",
         "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
        {"person": "罗试坚", "person_id": "guilin_罗试坚", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "卢新华（市长）与罗试坚（市政协主席）为市四家班子主要领导",
         "overlap_org": "桂林市四家班子",
         "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
    ]
    lxh_json = build_person_json(persons[1], lxh_timeline, lxh_relationships, sources)
    lxh_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-桂林市-市长-卢新华.json")
    with open(lxh_path, "w", encoding="utf-8") as f:
        json.dump(lxh_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lxh_path}")


# =========================================================================
# 7. BUILD
# =========================================================================
def build():
    os.makedirs(STAGING_DIR, exist_ok=True)
    print(f"=== Building {SLUG} data ===")
    print(f"Staging dir: {STAGING_DIR}")
    build_db()
    build_gexf()
    build_person_jsons()
    print("\nBuild complete.")


if __name__ == "__main__":
    build()
