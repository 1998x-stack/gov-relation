#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
陇西县 (定西市, 甘肃省) 领导班子工作关系网络数据构建脚本
Generate SQLite database + GEXF graph for Longxi County leadership network.

Level: 县
Province: 甘肃省
City: 定西市
Region: 陇西县
Targets: 县委书记 & 县长

Research Sources:
- 陇西县人民政府官方网站 (cnlongxi.gov.cn) 领导之窗, 2026年7月确认
- 陇西县人大常委会官方网站

Research Date: 2026-07-22
"""

import os
import sqlite3
from datetime import datetime

STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "陇西县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "陇西县_network.gexf")

# ═══════════════════════════════════════════════
# 人员数据
# ═══════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 县委领导
    # ════════════════════════════════════════
    {
        "id": "lxi_tian_xuerong",
        "name": "田学荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年11月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇西县委书记",
        "current_org": "中共陇西县委员会",
        "source": "http://www.cnlongxi.gov.cn/art/2025/11/24/art_9580_1875811.html",
    },
    {
        "id": "lxi_chen_wenguang",
        "name": "陈文广",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年1月",
        "birthplace": "",
        "native_place": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇西县委副书记、县长",
        "current_org": "中共陇西县委员会/陇西县人民政府",
        "source": "http://www.cnlongxi.gov.cn/art/2026/2/6/art_9585_1879290.html",
    },
    {
        "id": "lxi_zhang_xingcun",
        "name": "张杏村",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇西县委常委",
        "current_org": "中共陇西县委员会",
        "source": "http://www.cnlongxi.gov.cn/col/col9576/index.html?number=LX0101",
    },
    {
        "id": "lxi_zhang_rui",
        "name": "张瑞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇西县委常委",
        "current_org": "中共陇西县委员会",
        "source": "http://www.cnlongxi.gov.cn/col/col9576/index.html?number=LX0101",
    },
    {
        "id": "lxi_zeng_dairong",
        "name": "曾代荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇西县委常委、副县长",
        "current_org": "中共陇西县委员会/陇西县人民政府",
        "source": "http://www.cnlongxi.gov.cn/col/col9576/index.html?number=LX0101",
    },
    {
        "id": "lxi_han_xiqian",
        "name": "韩喜乾",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇西县委常委、副县长",
        "current_org": "中共陇西县委员会/陇西县人民政府",
        "source": "http://www.cnlongxi.gov.cn/col/col9576/index.html?number=LX0101",
    },
    {
        "id": "lxi_hao_jingke",
        "name": "郝静科",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇西县委常委",
        "current_org": "中共陇西县委员会",
        "source": "http://www.cnlongxi.gov.cn/col/col9576/index.html?number=LX0101",
    },
    {
        "id": "lxi_du_xuejun",
        "name": "杜学军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇西县委常委",
        "current_org": "中共陇西县委员会",
        "source": "http://www.cnlongxi.gov.cn/col/col9576/index.html?number=LX0101",
    },
    {
        "id": "lxi_yang_yemei",
        "name": "杨叶梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇西县委常委",
        "current_org": "中共陇西县委员会",
        "source": "http://www.cnlongxi.gov.cn/col/col9576/index.html?number=LX0101",
    },
    {
        "id": "lxi_xiao_zhenhua",
        "name": "肖振华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇西县委常委、副县长",
        "current_org": "中共陇西县委员会/陇西县人民政府",
        "source": "http://www.cnlongxi.gov.cn/col/col9576/index.html?number=LX0101",
    },
    {
        "id": "lxi_ma_liming",
        "name": "马黎明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇西县委常委、副县长",
        "current_org": "中共陇西县委员会/陇西县人民政府",
        "source": "http://www.cnlongxi.gov.cn/col/col9576/index.html?number=LX0101",
    },
    {
        "id": "lxi_guo_zhuang",
        "name": "郭壮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇西县委常委",
        "current_org": "中共陇西县委员会",
        "source": "http://www.cnlongxi.gov.cn/col/col9576/index.html?number=LX0101",
    },
    # ════════════════════════════════════════
    # 县政府副县长（非县委常委）
    # ════════════════════════════════════════
    {
        "id": "lxi_li_xiaodong",
        "name": "李晓东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇西县副县长",
        "current_org": "陇西县人民政府",
        "source": "http://www.cnlongxi.gov.cn/col/col9578/index.html?number=LX0103",
    },
    {
        "id": "lxi_zhu_yaowu",
        "name": "朱耀武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇西县副县长",
        "current_org": "陇西县人民政府",
        "source": "http://www.cnlongxi.gov.cn/col/col9578/index.html?number=LX0103",
    },
    {
        "id": "lxi_zhang_jianxiao",
        "name": "张剑啸",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "陇西县副县长",
        "current_org": "陇西县人民政府",
        "source": "http://www.cnlongxi.gov.cn/col/col9578/index.html?number=LX0103",
    },
    # ════════════════════════════════════════
    # 县人大领导
    # ════════════════════════════════════════
    {
        "id": "lxi_wang_jinyu",
        "name": "汪进玉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇西县人大常委会主任",
        "current_org": "陇西县人民代表大会常务委员会",
        "source": "http://www.cnlongxi.gov.cn/col/col9577/index.html",
    },
    {
        "id": "lxi_wang_xingji",
        "name": "王兴继",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇西县人大常委会副主任",
        "current_org": "陇西县人民代表大会常务委员会",
        "source": "http://www.cnlongxi.gov.cn/col/col9577/index.html",
    },
    {
        "id": "lxi_wang_yongde",
        "name": "王永德",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇西县人大常委会副主任",
        "current_org": "陇西县人民代表大会常务委员会",
        "source": "http://www.cnlongxi.gov.cn/col/col9577/index.html",
    },
    {
        "id": "lxi_wang_enmao",
        "name": "王恩茂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇西县人大常委会副主任",
        "current_org": "陇西县人民代表大会常务委员会",
        "source": "http://www.cnlongxi.gov.cn/col/col9577/index.html",
    },
    {
        "id": "lxi_meng_qingfang",
        "name": "孟庆芳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇西县人大常委会副主任",
        "current_org": "陇西县人民代表大会常务委员会",
        "source": "http://www.cnlongxi.gov.cn/col/col9577/index.html",
    },
    {
        "id": "lxi_wang_guodong",
        "name": "王国栋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇西县人大常委会副主任",
        "current_org": "陇西县人民代表大会常务委员会",
        "source": "http://www.cnlongxi.gov.cn/col/col9577/index.html",
    },
    {
        "id": "lxi_hu_zhaoming",
        "name": "胡照明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇西县人大常委会副主任",
        "current_org": "陇西县人民代表大会常务委员会",
        "source": "http://www.cnlongxi.gov.cn/col/col9577/index.html",
    },
    # ════════════════════════════════════════
    # 县政协领导
    # ════════════════════════════════════════
    {
        "id": "lxi_ma_jiancheng",
        "name": "马建成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇西县政协主席",
        "current_org": "中国人民政治协商会议陇西县委员会",
        "source": "http://www.cnlongxi.gov.cn/col/col9579/index.html?number=LX0104",
    },
    {
        "id": "lxi_liu_mingxia",
        "name": "刘明霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "陇西县政协副主席",
        "current_org": "中国人民政治协商会议陇西县委员会",
        "source": "http://www.cnlongxi.gov.cn/col/col9579/index.html?number=LX0104",
    },
    {
        "id": "lxi_dong_wenjun",
        "name": "董文君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "陇西县政协副主席",
        "current_org": "中国人民政治协商会议陇西县委员会",
        "source": "http://www.cnlongxi.gov.cn/col/col9579/index.html?number=LX0104",
    },
    {
        "id": "lxi_wang_jintao",
        "name": "王锦涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "陇西县政协副主席",
        "current_org": "中国人民政治协商会议陇西县委员会",
        "source": "http://www.cnlongxi.gov.cn/col/col9579/index.html?number=LX0104",
    },
    {
        "id": "lxi_yang_shulin",
        "name": "杨树林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "陇西县政协副主席",
        "current_org": "中国人民政治协商会议陇西县委员会",
        "source": "http://www.cnlongxi.gov.cn/col/col9579/index.html?number=LX0104",
    },
    {
        "id": "lxi_zhang_zhanjun",
        "name": "张占军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "陇西县政协副主席",
        "current_org": "中国人民政治协商会议陇西县委员会",
        "source": "http://www.cnlongxi.gov.cn/col/col9579/index.html?number=LX0104",
    },
    {
        "id": "lxi_xu_guixiang",
        "name": "许贵祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "陇西县政协副主席",
        "current_org": "中国人民政治协商会议陇西县委员会",
        "source": "http://www.cnlongxi.gov.cn/col/col9579/index.html?number=LX0104",
    },
]

# ═══════════════════════════════════════════════
# 组织机构数据
# ═══════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共陇西县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共定西市委员会",
        "location": "甘肃省定西市陇西县",
    },
    {
        "id": 2,
        "name": "陇西县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "定西市人民政府",
        "location": "甘肃省定西市陇西县",
    },
    {
        "id": 3,
        "name": "陇西县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "定西市人民代表大会常务委员会",
        "location": "甘肃省定西市陇西县",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议陇西县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "中国人民政治协商会议定西市委员会",
        "location": "甘肃省定西市陇西县",
    },
]

# ═══════════════════════════════════════════════
# 任职数据
# ═══════════════════════════════════════════════

positions = [
    # 田学荣 — 县委书记
    {"person_id": "lxi_tian_xuerong", "org_id": 1, "title": "陇西县委书记", "start": "", "end": "present", "rank": "正处级", "note": "主持县委全面工作"},
    # 陈文广 — 县长/副书记
    {"person_id": "lxi_chen_wenguang", "org_id": 1, "title": "陇西县委副书记", "start": "", "end": "present", "rank": "正处级", "note": "兼任县长"},
    {"person_id": "lxi_chen_wenguang", "org_id": 2, "title": "陇西县县长", "start": "", "end": "present", "rank": "正处级", "note": "主持县政府全面工作"},
    # 县委常委
    {"person_id": "lxi_zhang_xingcun", "org_id": 1, "title": "陇西县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "lxi_zhang_rui", "org_id": 1, "title": "陇西县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "lxi_zeng_dairong", "org_id": 1, "title": "陇西县委常委", "start": "", "end": "present", "rank": "副处级", "note": "兼任副县长"},
    {"person_id": "lxi_zeng_dairong", "org_id": 2, "title": "陇西县副县长", "start": "", "end": "present", "rank": "副处级", "note": "县委常委兼任"},
    {"person_id": "lxi_han_xiqian", "org_id": 1, "title": "陇西县委常委", "start": "", "end": "present", "rank": "副处级", "note": "兼任副县长"},
    {"person_id": "lxi_han_xiqian", "org_id": 2, "title": "陇西县副县长", "start": "", "end": "present", "rank": "副处级", "note": "县委常委兼任"},
    {"person_id": "lxi_hao_jingke", "org_id": 1, "title": "陇西县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "lxi_du_xuejun", "org_id": 1, "title": "陇西县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "lxi_yang_yemei", "org_id": 1, "title": "陇西县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "lxi_xiao_zhenhua", "org_id": 1, "title": "陇西县委常委", "start": "", "end": "present", "rank": "副处级", "note": "兼任副县长"},
    {"person_id": "lxi_xiao_zhenhua", "org_id": 2, "title": "陇西县副县长", "start": "", "end": "present", "rank": "副处级", "note": "县委常委兼任"},
    {"person_id": "lxi_ma_liming", "org_id": 1, "title": "陇西县委常委", "start": "", "end": "present", "rank": "副处级", "note": "兼任副县长"},
    {"person_id": "lxi_ma_liming", "org_id": 2, "title": "陇西县副县长", "start": "", "end": "present", "rank": "副处级", "note": "县委常委兼任"},
    {"person_id": "lxi_guo_zhuang", "org_id": 1, "title": "陇西县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 副县长（非县委常委）
    {"person_id": "lxi_li_xiaodong", "org_id": 2, "title": "陇西县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "lxi_zhu_yaowu", "org_id": 2, "title": "陇西县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "lxi_zhang_jianxiao", "org_id": 2, "title": "陇西县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 人大
    {"person_id": "lxi_wang_jinyu", "org_id": 3, "title": "陇西县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": "lxi_wang_xingji", "org_id": 3, "title": "陇西县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "lxi_wang_yongde", "org_id": 3, "title": "陇西县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "lxi_wang_enmao", "org_id": 3, "title": "陇西县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "lxi_meng_qingfang", "org_id": 3, "title": "陇西县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "lxi_wang_guodong", "org_id": 3, "title": "陇西县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "lxi_hu_zhaoming", "org_id": 3, "title": "陇西县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 政协
    {"person_id": "lxi_ma_jiancheng", "org_id": 4, "title": "陇西县政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": "lxi_liu_mingxia", "org_id": 4, "title": "陇西县政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "lxi_dong_wenjun", "org_id": 4, "title": "陇西县政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "lxi_wang_jintao", "org_id": 4, "title": "陇西县政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "lxi_yang_shulin", "org_id": 4, "title": "陇西县政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "lxi_zhang_zhanjun", "org_id": 4, "title": "陇西县政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "lxi_xu_guixiang", "org_id": 4, "title": "陇西县政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
]

# ═══════════════════════════════════════════════
# 关系数据
# ═══════════════════════════════════════════════

relationships = [
    # 党政一把手关系
    {
        "person_a": "lxi_tian_xuerong",
        "person_b": "lxi_chen_wenguang",
        "type": "superior_subordinate",
        "context": "县委书记-县长搭班工作关系",
        "overlap_org": "中共陇西县委员会/陇西县人民政府",
        "overlap_period": "2025-2026",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 县委书记-副书记关系
    {
        "person_a": "lxi_tian_xuerong",
        "person_b": "lxi_chen_wenguang",
        "type": "overlap",
        "context": "田学荣(书记)与陈文广(副书记): 书记-副书记班子配合",
        "overlap_org": "中共陇西县委员会",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 县委常委之间（同届常委同事关系）
    {
        "person_a": "lxi_zhang_xingcun",
        "person_b": "lxi_zhang_rui",
        "type": "overlap",
        "context": "张杏村与张瑞: 同届县委常委",
        "overlap_org": "中共陇西县委员会",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": "lxi_zeng_dairong",
        "person_b": "lxi_han_xiqian",
        "type": "overlap",
        "context": "曾代荣与韩喜乾: 同届县委常委、副县长",
        "overlap_org": "中共陇西县委员会",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": "lxi_hao_jingke",
        "person_b": "lxi_du_xuejun",
        "type": "overlap",
        "context": "郝静科与杜学军: 同届县委常委",
        "overlap_org": "中共陇西县委员会",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": "lxi_xiao_zhenhua",
        "person_b": "lxi_ma_liming",
        "type": "overlap",
        "context": "肖振华与马黎明: 同届县委常委、副县长",
        "overlap_org": "中共陇西县委员会",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": "lxi_yang_yemei",
        "person_b": "lxi_guo_zhuang",
        "type": "overlap",
        "context": "杨叶梅与郭壮: 同届县委常委",
        "overlap_org": "中共陇西县委员会",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 书记-其他常委关系
    {
        "person_a": "lxi_tian_xuerong",
        "person_b": "lxi_zhang_xingcun",
        "type": "overlap",
        "context": "田学荣(书记)与张杏村(常委): 党委班子配合",
        "overlap_org": "中共陇西县委员会",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": "lxi_tian_xuerong",
        "person_b": "lxi_hao_jingke",
        "type": "overlap",
        "context": "田学荣(书记)与郝静科(常委): 党委班子配合",
        "overlap_org": "中共陇西县委员会",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 书记-人大主任关系
    {
        "person_a": "lxi_tian_xuerong",
        "person_b": "lxi_wang_jinyu",
        "type": "overlap",
        "context": "田学荣(书记)与汪进玉(人大主任): 党委-人大配合",
        "overlap_org": "陇西县",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 书记-政协主席关系
    {
        "person_a": "lxi_tian_xuerong",
        "person_b": "lxi_ma_jiancheng",
        "type": "overlap",
        "context": "田学荣(书记)与马建成(政协主席): 党委-政协配合",
        "overlap_org": "陇西县",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 县长-副县长关系
    {
        "person_a": "lxi_chen_wenguang",
        "person_b": "lxi_li_xiaodong",
        "type": "overlap",
        "context": "陈文广(县长)与李晓东(副县长): 政府班子配合",
        "overlap_org": "陇西县人民政府",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": "lxi_chen_wenguang",
        "person_b": "lxi_zhu_yaowu",
        "type": "overlap",
        "context": "陈文广(县长)与朱耀武(副县长): 政府班子配合",
        "overlap_org": "陇西县人民政府",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": "lxi_chen_wenguang",
        "person_b": "lxi_zhang_jianxiao",
        "type": "overlap",
        "context": "陈文广(县长)与张剑啸(副县长): 政府班子配合",
        "overlap_org": "陇西县人民政府",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 人大主任-副主任关系
    {
        "person_a": "lxi_wang_jinyu",
        "person_b": "lxi_wang_xingji",
        "type": "overlap",
        "context": "汪进玉(人大主任)与王兴继(副主任): 人大班子配合",
        "overlap_org": "陇西县人民代表大会常务委员会",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 政协主席-副主席关系
    {
        "person_a": "lxi_ma_jiancheng",
        "person_b": "lxi_liu_mingxia",
        "type": "overlap",
        "context": "马建成(政协主席)与刘明霞(副主席): 政协班子配合",
        "overlap_org": "中国人民政治协商会议陇西县委员会",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
]


# ── 辅助函数 ──

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return RGB color string based on role."""
    title = p["current_post"]
    if "书记" in title and "纪委" not in title and "统战" not in title and "人大" not in title and "政协" not in title:
        if "副书记" in title:
            return "200,50,50"    # Dark red — Deputy Secretary
        return "255,50,50"    # Red — Party Secretary
    if "县长" in title or ("长" in title and "副" not in title and "书记" not in title):
        return "50,100,255"   # Blue — Government head
    if "纪委" in title or "监委" in title or "监察" in title or "纪委书记" in title:
        return "255,165,0"    # Orange — Discipline
    if "副书记" in title:
        return "200,50,50"    # Dark red — Deputy Secretary
    if "常委" in title:
        return "200,100,100"  # Pink — Other Standing Committee
    if "副县长" in title or "副" in title:
        return "100,100,200"  # Light blue — Deputy
    if "人大" in title:
        return "200,255,255"  # Cyan — People's Congress
    if "政协" in title:
        return "255,240,200"  # Cream — CPPCC
    return "100,100,100"      # Grey — Other


def person_size(p):
    """Return node size based on role."""
    title = p["current_post"]
    if "县委书记" in title:
        return "20.0"
    if "县长" in title and "副" not in title:
        return "20.0"
    if "人大主任" in title or "政协主席" in title:
        return "16.0"
    if "副书记" in title or "常委" in title:
        return "14.0"
    if "副县长" in title or "副主任" in title or "副主席" in title:
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

    c.execute("DROP TABLE IF EXISTS persons")
    c.execute("DROP TABLE IF EXISTS organizations")
    c.execute("DROP TABLE IF EXISTS positions")
    c.execute("DROP TABLE IF EXISTS relationships")

    c.execute("""CREATE TABLE persons (
        id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT,
        party_join TEXT, work_start TEXT, current_post TEXT,
        current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT, org_id INTEGER, title TEXT,
        start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    c.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT, person_b TEXT, type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", (
            p["id"], p["name"], p["gender"], p["ethnicity"],
            p["birth"], p["birthplace"], p["education"],
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
            pos["start"], pos["end"], pos["rank"], pos.get("note", "")
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
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>陇西县领导班子工作关系网络 - 数据来源: 陇西县人民政府官网(cnlongxi.gov.cn)领导之窗</description>')
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
        lines.append('          <attvalue for="3" value="定西市"/>')
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
        lines.append('          <attvalue for="3" value="定西市"/>')
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
    print(f"=== 陇西县网络数据构建 ===")
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
