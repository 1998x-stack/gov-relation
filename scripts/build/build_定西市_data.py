#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定西市领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Dingxi City leadership network.

Level: 地级市
Province: 甘肃省
Region: 定西市
Targets: 市委书记 & 市长

Research Sources:
- 定西市人民政府官方网站 (dingxi.gov.cn) 领导之窗, 2026年7月确认
- Wikipedia (zh.wikipedia.org) — 定西市
- 维基百科历任领导列表
- 新闻报道 (中国经济网, 中国甘肃网, 澎湃新闻 etc.)
- 百度百科

Research Date: 2026-07-22
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "定西市_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "定西市_network.gexf")

# ── DATA ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": "p01",
        "name": "汪尚学",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年3月",
        "birthplace": "甘肃天水",
        "native_place": "甘肃天水",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "定西市委书记",
        "current_org": "中共定西市委员会",
        "source": "Wikipedia: 定西市; 定西市人民政府官网(dingxi.gov.cn) 领导之窗 2026-07",
        "person_id": "dingxi_wang_shangxue"
    },
    {
        "id": "p02",
        "name": "武和谦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年1月",
        "birthplace": "甘肃白银",
        "native_place": "甘肃白银",
        "education": "甘肃省交通学校中专/长安大学工学硕士",
        "party_join": "1995年6月",
        "work_start": "1990年7月",
        "current_post": "武威市委书记（原定西市长）",
        "current_org": "中共武威市委员会",
        "source": "data/persons/20260717-甘肃省-武威市-市委书记-武和谦.json; 百度百科",
        "person_id": "dingxi_wu_heqian"
    },
    # ════════════════════════════════════════
    # 市委领导
    # ════════════════════════════════════════
    {
        "id": "p03",
        "name": "黄欣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "定西市委副书记",
        "current_org": "中共定西市委员会",
        "source": "定西市人民政府官网(dingxi.gov.cn) 领导之窗 2026-07",
        "person_id": "dingxi_huang_xin"
    },
    {
        "id": "p04",
        "name": "何英禅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "定西市委常委、副市长",
        "current_org": "中共定西市委员会/定西市人民政府",
        "source": "定西市人民政府官网(dingxi.gov.cn) 领导之窗 2026-07",
        "person_id": "dingxi_he_yingchan"
    },
    {
        "id": "p05",
        "name": "寇继军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "定西市委常委",
        "current_org": "中共定西市委员会",
        "source": "定西市人民政府官网(dingxi.gov.cn) 领导之窗 2026-07",
        "person_id": "dingxi_kou_jijun"
    },
    {
        "id": "p06",
        "name": "包世权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "定西市委常委",
        "current_org": "中共定西市委员会",
        "source": "定西市人民政府官网(dingxi.gov.cn) 领导之窗 2026-07",
        "person_id": "dingxi_bao_shiquan"
    },
    {
        "id": "p07",
        "name": "温选荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "定西市委常委",
        "current_org": "中共定西市委员会",
        "source": "定西市人民政府官网(dingxi.gov.cn) 领导之窗 2026-07",
        "person_id": "dingxi_wen_xuanrong"
    },
    {
        "id": "p08",
        "name": "陈景春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "定西市委常委",
        "current_org": "中共定西市委员会",
        "source": "定西市人民政府官网(dingxi.gov.cn) 领导之窗 2026-07",
        "person_id": "dingxi_chen_jingchun"
    },
    # ════════════════════════════════════════
    # 市人大领导
    # ════════════════════════════════════════
    {
        "id": "p09",
        "name": "温卫东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年7月",
        "birthplace": "甘肃靖远",
        "native_place": "甘肃靖远",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "定西市人大常委会主任",
        "current_org": "定西市人民代表大会常务委员会",
        "source": "Wikipedia: 定西市; 定西市人民政府官网(dingxi.gov.cn) 领导之窗 2026-07",
        "person_id": "dingxi_wen_weidong"
    },
    {
        "id": "p10",
        "name": "刘静",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "定西市人大常委会副主任",
        "current_org": "定西市人民代表大会常务委员会",
        "source": "定西市人民政府官网(dingxi.gov.cn) 领导之窗 2026-07",
        "person_id": "dingxi_liu_jing"
    },
    {
        "id": "p11",
        "name": "陈彦吉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "定西市人大常委会副主任",
        "current_org": "定西市人民代表大会常务委员会",
        "source": "定西市人民政府官网(dingxi.gov.cn) 领导之窗 2026-07",
        "person_id": "dingxi_chen_yanji"
    },
    {
        "id": "p12",
        "name": "马荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "定西市人大常委会副主任",
        "current_org": "定西市人民代表大会常务委员会",
        "source": "定西市人民政府官网(dingxi.gov.cn) 领导之窗 2026-07",
        "person_id": "dingxi_ma_rong"
    },
    {
        "id": "p13",
        "name": "党伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "定西市人大常委会副主任",
        "current_org": "定西市人民代表大会常务委员会",
        "source": "定西市人民政府官网(dingxi.gov.cn) 领导之窗 2026-07",
        "person_id": "dingxi_dang_wei"
    },
    {
        "id": "p14",
        "name": "祁义江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "定西市人大常委会秘书长",
        "current_org": "定西市人民代表大会常务委员会",
        "source": "定西市人民政府官网(dingxi.gov.cn) 领导之窗 2026-07",
        "person_id": "dingxi_qi_yijiang"
    },
    # ════════════════════════════════════════
    # 市政府领导（市长空缺中）
    # ════════════════════════════════════════
    {
        "id": "p15",
        "name": "王社宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "定西市副市长",
        "current_org": "定西市人民政府",
        "source": "定西市人民政府官网(dingxi.gov.cn) 领导之窗 2026-07",
        "person_id": "dingxi_wang_shering"
    },
    {
        "id": "p16",
        "name": "张岸林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "定西市副市长",
        "current_org": "定西市人民政府",
        "source": "定西市人民政府官网(dingxi.gov.cn) 领导之窗 2026-07",
        "person_id": "dingxi_zhang_anlin"
    },
    {
        "id": "p17",
        "name": "贾文举",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "定西市副市长",
        "current_org": "定西市人民政府",
        "source": "定西市人民政府官网(dingxi.gov.cn) 领导之窗 2026-07",
        "person_id": "dingxi_jia_wenju"
    },
    {
        "id": "p18",
        "name": "汤晓春",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "定西市副市长",
        "current_org": "定西市人民政府",
        "source": "定西市人民政府官网(dingxi.gov.cn) 领导之窗 2026-07",
        "person_id": "dingxi_tang_xiaochun"
    },
    {
        "id": "p19",
        "name": "王建平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "定西市副市长",
        "current_org": "定西市人民政府",
        "source": "定西市人民政府官网(dingxi.gov.cn) 领导之窗 2026-07",
        "person_id": "dingxi_wang_jianping"
    },
    {
        "id": "p20",
        "name": "宋军兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "定西市政府秘书长",
        "current_org": "定西市人民政府",
        "source": "定西市人民政府官网(dingxi.gov.cn) 领导之窗 2026-07",
        "person_id": "dingxi_song_junbing"
    },
    # ════════════════════════════════════════
    # 市政协领导
    # ════════════════════════════════════════
    {
        "id": "p21",
        "name": "高永平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "定西市政协主席",
        "current_org": "中国人民政治协商会议定西市委员会",
        "source": "定西市人民政府官网(dingxi.gov.cn) 领导之窗 2026-07",
        "person_id": "dingxi_gao_yongping"
    },
    {
        "id": "p22",
        "name": "马小兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "定西市政协副主席",
        "current_org": "中国人民政治协商会议定西市委员会",
        "source": "定西市人民政府官网(dingxi.gov.cn) 领导之窗 2026-07",
        "person_id": "dingxi_ma_xiaobing"
    },
    {
        "id": "p23",
        "name": "盛淑兰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "定西市政协副主席",
        "current_org": "中国人民政治协商会议定西市委员会",
        "source": "定西市人民政府官网(dingxi.gov.cn) 领导之窗 2026-07",
        "person_id": "dingxi_sheng_shulan"
    },
    {
        "id": "p24",
        "name": "刘永维",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "定西市政协副主席",
        "current_org": "中国人民政治协商会议定西市委员会",
        "source": "定西市人民政府官网(dingxi.gov.cn) 领导之窗 2026-07",
        "person_id": "dingxi_liu_yongwei"
    },
    {
        "id": "p25",
        "name": "徐景义",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "定西市政协副主席",
        "current_org": "中国人民政治协商会议定西市委员会",
        "source": "定西市人民政府官网(dingxi.gov.cn) 领导之窗 2026-07",
        "person_id": "dingxi_xu_jingyi"
    },
    {
        "id": "p26",
        "name": "张子恒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "定西市政协副主席",
        "current_org": "中国人民政治协商会议定西市委员会",
        "source": "定西市人民政府官网(dingxi.gov.cn) 领导之窗 2026-07",
        "person_id": "dingxi_zhang_ziheng"
    },
    {
        "id": "p27",
        "name": "谢占武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "定西市政协副主席",
        "current_org": "中国人民政治协商会议定西市委员会",
        "source": "定西市人民政府官网(dingxi.gov.cn) 领导之窗 2026-07",
        "person_id": "dingxi_xie_zhanwu"
    },
    {
        "id": "p28",
        "name": "刘荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "定西市政协副主席",
        "current_org": "中国人民政治协商会议定西市委员会",
        "source": "定西市人民政府官网(dingxi.gov.cn) 领导之窗 2026-07",
        "person_id": "dingxi_liu_rong"
    },
    # ════════════════════════════════════════
    # Predecessors — 市委书记
    # ════════════════════════════════════════
    {
        "id": "p29",
        "name": "戴超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1964年",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（曾任定西市委书记、甘肃省人大常委等）",
        "current_org": "待查",
        "source": "Wikipedia: 定西市; 中国经济网",
        "person_id": "dingxi_dai_chao"
    },
    {
        "id": "p30",
        "name": "唐晓明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（曾任定西市委书记）",
        "current_org": "待查",
        "source": "Wikipedia: 定西市",
        "person_id": "dingxi_tang_xiaoming"
    },
    {
        "id": "p31",
        "name": "张令平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（曾任定西市委书记，2019年接受调查）",
        "current_org": "待查",
        "source": "Wikipedia: 定西市",
        "person_id": "dingxi_zhang_lingping"
    },
    {
        "id": "p32",
        "name": "杨子兴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1959年",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（曾任定西市委书记、甘肃省副省长）",
        "current_org": "待查",
        "source": "Wikipedia: 定西市",
        "person_id": "dingxi_yang_zixing"
    },
    {
        "id": "p33",
        "name": "石晶",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（首任定西市委书记2003-2008）",
        "current_org": "待查",
        "source": "Wikipedia: 定西市",
        "person_id": "dingxi_shi_jing"
    },
    # ════════════════════════════════════════
    # Predecessors — 市长
    # ════════════════════════════════════════
    {
        "id": "p34",
        "name": "许尔锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（曾任定西市长、宁夏自治区公安厅长、应急管理部等）",
        "current_org": "待查",
        "source": "Wikipedia: 定西市",
        "person_id": "dingxi_xu_erfeng"
    },
    {
        "id": "p35",
        "name": "常正国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（曾任定西市长、退役军人事务部副部长等）",
        "current_org": "待查",
        "source": "Wikipedia: 定西市",
        "person_id": "dingxi_chang_zhengguo"
    },
    {
        "id": "p36",
        "name": "武文斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（首任定西市长2003-2005）",
        "current_org": "待查",
        "source": "Wikipedia: 定西市",
        "person_id": "dingxi_wu_wenbin"
    },
]

# 2. Organizations
organizations = [
    {"id": "o01", "name": "中共定西市委员会", "type": "党委", "level": "地厅级", "parent": "中共甘肃省委员会", "location": "甘肃省定西市安定区"},
    {"id": "o02", "name": "定西市人民政府", "type": "政府", "level": "地厅级", "parent": "甘肃省人民政府", "location": "甘肃省定西市安定区"},
    {"id": "o03", "name": "定西市人民代表大会常务委员会", "type": "人大", "level": "地厅级", "parent": "定西市", "location": "甘肃省定西市安定区"},
    {"id": "o04", "name": "中国人民政治协商会议定西市委员会", "type": "政协", "level": "地厅级", "parent": "定西市", "location": "甘肃省定西市安定区"},
    {"id": "o05", "name": "中共武威市委员会", "type": "党委", "level": "地厅级", "parent": "中共甘肃省委员会", "location": "甘肃省武威市"},
]

# 3. Positions
positions = [
    # 汪尚学 (p01) — 市委书记
    {"person_id": "p01", "org_id": "o01", "title": "定西市委书记", "start": "2023-03", "end": "至今", "rank": "正厅级", "note": "2023年3月任定西市委书记"},
    {"person_id": "p01", "org_id": "o02", "title": "定西市人民政府市长（前任）", "start": "2021-07", "end": "2023-04", "rank": "正厅级", "note": "接替戴超任市长，后升任书记"},
    {"person_id": "p01", "org_id": "o01", "title": "定西市委副书记", "start": "2021-07", "end": "2023-03", "rank": "副厅级", "note": "兼任市长"},
    # 武和谦 (p02) — 原市长
    {"person_id": "p02", "org_id": "o02", "title": "定西市人民政府市长", "start": "2023-04", "end": "2026-06", "rank": "正厅级", "note": "2023年4月15日当选定西市长；2026年6月调任武威市委书记"},
    {"person_id": "p02", "org_id": "o01", "title": "定西市委副书记", "start": "2023-04", "end": "2026-06", "rank": "副厅级", "note": "兼任市长"},
    {"person_id": "p02", "org_id": "o05", "title": "武威市委书记（现任）", "start": "2026-06", "end": "至今", "rank": "正厅级", "note": "2026年6月24日省委任命"},
    # 黄欣 (p03) — 市委副书记
    {"person_id": "p03", "org_id": "o01", "title": "定西市委副书记", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
    # 何英禅 (p04) — 市委常委、副市长
    {"person_id": "p04", "org_id": "o01", "title": "定西市委常委", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
    {"person_id": "p04", "org_id": "o02", "title": "定西市副市长", "start": "待查", "end": "至今", "rank": "副厅级", "note": "常务副市长？"},
    # 寇继军 (p05)
    {"person_id": "p05", "org_id": "o01", "title": "定西市委常委", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
    # 包世权 (p06)
    {"person_id": "p06", "org_id": "o01", "title": "定西市委常委", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
    # 温选荣 (p07)
    {"person_id": "p07", "org_id": "o01", "title": "定西市委常委", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
    # 陈景春 (p08)
    {"person_id": "p08", "org_id": "o01", "title": "定西市委常委", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
    # 温卫东 (p09) — 人大主任
    {"person_id": "p09", "org_id": "o03", "title": "定西市人大常委会主任", "start": "2024-01", "end": "至今", "rank": "正厅级", "note": "2024年1月当选"},
    # 人大副主任
    {"person_id": "p10", "org_id": "o03", "title": "定西市人大常委会副主任", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
    {"person_id": "p11", "org_id": "o03", "title": "定西市人大常委会副主任", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
    {"person_id": "p12", "org_id": "o03", "title": "定西市人大常委会副主任", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
    {"person_id": "p13", "org_id": "o03", "title": "定西市人大常委会副主任", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
    {"person_id": "p14", "org_id": "o03", "title": "定西市人大常委会秘书长", "start": "待查", "end": "至今", "rank": "正处级", "note": ""},
    # 副市长
    {"person_id": "p15", "org_id": "o02", "title": "定西市副市长", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
    {"person_id": "p16", "org_id": "o02", "title": "定西市副市长", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
    {"person_id": "p17", "org_id": "o02", "title": "定西市副市长", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
    {"person_id": "p18", "org_id": "o02", "title": "定西市副市长", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
    {"person_id": "p19", "org_id": "o02", "title": "定西市副市长", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
    {"person_id": "p20", "org_id": "o02", "title": "定西市政府秘书长", "start": "待查", "end": "至今", "rank": "正处级", "note": ""},
    # 政协
    {"person_id": "p21", "org_id": "o04", "title": "定西市政协主席", "start": "2021-08", "end": "至今", "rank": "正厅级", "note": "2021年8月当选"},
    {"person_id": "p22", "org_id": "o04", "title": "定西市政协副主席", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
    {"person_id": "p23", "org_id": "o04", "title": "定西市政协副主席", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
    {"person_id": "p24", "org_id": "o04", "title": "定西市政协副主席", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
    {"person_id": "p25", "org_id": "o04", "title": "定西市政协副主席", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
    {"person_id": "p26", "org_id": "o04", "title": "定西市政协副主席", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
    {"person_id": "p27", "org_id": "o04", "title": "定西市政协副主席", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
    {"person_id": "p28", "org_id": "o04", "title": "定西市政协副主席", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
    # Predecessors — 市委书记历任
    {"person_id": "p29", "org_id": "o01", "title": "定西市委书记", "start": "2021-07", "end": "2023-03", "rank": "正厅级", "note": "汪尚学前任"},
    {"person_id": "p30", "org_id": "o01", "title": "定西市委书记", "start": "2017-05", "end": "2021-07", "rank": "正厅级", "note": "戴超前任"},
    {"person_id": "p31", "org_id": "o01", "title": "定西市委书记", "start": "2013-12", "end": "2017-04", "rank": "正厅级", "note": "2019年接受调查"},
    {"person_id": "p32", "org_id": "o01", "title": "定西市委书记", "start": "2008-02", "end": "2013-11", "rank": "正厅级", "note": "后任甘肃省副省长"},
    {"person_id": "p33", "org_id": "o01", "title": "定西市委书记", "start": "2003-07", "end": "2008-01", "rank": "正厅级", "note": "首任市委书记"},
    # Predecessors — 市长历任
    {"person_id": "p34", "org_id": "o02", "title": "定西市人民政府市长", "start": "2008-03", "end": "2010-12", "rank": "正厅级", "note": "杨子兴后任"},
    {"person_id": "p35", "org_id": "o02", "title": "定西市人民政府市长", "start": "2011-02", "end": "2013-04", "rank": "正厅级", "note": "许尔锋后任"},
    {"person_id": "p36", "org_id": "o02", "title": "定西市人民政府市长", "start": "2003-12", "end": "2005-03", "rank": "正厅级", "note": "首任市长"},
]

# 4. Relationships
relationships = [
    # 现任班子核心关系
    {"person_a": "p01", "person_b": "p02", "type": "overlap", "context": "汪尚学(书记)与武和谦(市长): 党政一把手配合", "overlap_org": "中共定西市委员会/定西市人民政府", "overlap_period": "2023-04至2026-06", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p03", "type": "overlap", "context": "汪尚学(书记)与黄欣(副书记): 书记-副书记班子配合", "overlap_org": "中共定西市委员会", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p09", "type": "overlap", "context": "汪尚学(书记)与温卫东(人大主任): 市领导班子配合", "overlap_org": "定西市", "overlap_period": "2024-01至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p21", "type": "overlap", "context": "汪尚学(书记)与高永平(政协主席): 党委-政协配合", "overlap_org": "定西市", "overlap_period": "2023-03至今", "strength": "strong", "confidence": "confirmed"},

    # 市委常委之间
    {"person_a": "p04", "person_b": "p05", "type": "overlap", "context": "何英禅与寇继军: 同届市委常委", "overlap_org": "中共定西市委员会", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p06", "person_b": "p07", "type": "overlap", "context": "包世权与温选荣: 同届市委常委", "overlap_org": "中共定西市委员会", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},

    # 前后任书记关系
    {"person_a": "p01", "person_b": "p29", "type": "predecessor_successor", "context": "汪尚学接替戴超任定西市委书记", "overlap_org": "中共定西市委员会", "overlap_period": "2023-03", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p29", "person_b": "p30", "type": "predecessor_successor", "context": "戴超接替唐晓明任定西市委书记", "overlap_org": "中共定西市委员会", "overlap_period": "2021-07", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p30", "person_b": "p31", "type": "predecessor_successor", "context": "唐晓明接替张令平任定西市委书记", "overlap_org": "中共定西市委员会", "overlap_period": "2017-05", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p31", "person_b": "p32", "type": "predecessor_successor", "context": "张令平接替杨子兴任定西市委书记", "overlap_org": "中共定西市委员会", "overlap_period": "2013-12", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p32", "person_b": "p33", "type": "predecessor_successor", "context": "杨子兴接替石晶任定西市委书记", "overlap_org": "中共定西市委员会", "overlap_period": "2008-02", "strength": "strong", "confidence": "confirmed"},

    # 前后任市长关系
    {"person_a": "p02", "person_b": "p01", "type": "predecessor_successor", "context": "武和谦接替汪尚学任定西市长", "overlap_org": "定西市人民政府", "overlap_period": "2023-04", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p29", "type": "predecessor_successor", "context": "汪尚学接替戴超任定西市长（2021年）", "overlap_org": "定西市人民政府", "overlap_period": "2021-07", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p29", "person_b": "p30", "type": "predecessor_successor", "context": "戴超接替唐晓明任定西市长", "overlap_org": "定西市人民政府", "overlap_period": "2017-05", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p30", "person_b": "p35", "type": "predecessor_successor", "context": "唐晓明接替常正国任定西市长", "overlap_org": "定西市人民政府", "overlap_period": "2013-04", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p35", "person_b": "p34", "type": "predecessor_successor", "context": "常正国接替许尔锋任定西市长", "overlap_org": "定西市人民政府", "overlap_period": "2011-02", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p34", "person_b": "p32", "type": "predecessor_successor", "context": "许尔锋接替杨子兴任定西市长", "overlap_org": "定西市人民政府", "overlap_period": "2008-03", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p32", "person_b": "p36", "type": "predecessor_successor", "context": "杨子兴接替武文斌任定西市长", "overlap_org": "定西市人民政府", "overlap_period": "2005-04", "strength": "strong", "confidence": "confirmed"},

    # 由市长升书记的关系
    {"person_a": "p01", "person_b": "p29", "type": "promotion_chain", "context": "汪尚学（市长→书记）与戴超（市长→书记）: 相同升迁路径", "overlap_org": "中共定西市委员会/定西市人民政府", "overlap_period": "2017-2023", "strength": "medium", "confidence": "confirmed"},
    {"person_a": "p29", "person_b": "p30", "type": "promotion_chain", "context": "戴超（市长→书记）与唐晓明（市长→书记）: 相同升迁路径", "overlap_org": "中共定西市委员会/定西市人民政府", "overlap_period": "2013-2021", "strength": "medium", "confidence": "confirmed"},

    # 武和谦升迁链
    {"person_a": "p02", "person_b": "p01", "type": "promotion_chain", "context": "武和谦（定西市长→武威书记）: 异地升迁至同级正厅", "overlap_org": "甘肃省干部交流体系", "overlap_period": "2026-06", "strength": "medium", "confidence": "confirmed"},
]


# ── Helper Functions ──

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return RGB color string based on role."""
    title = p["current_post"]
    if "书记" in title and "纪委" not in title and "统战" not in title and "人大" not in title and "政协" not in title:
        return "255,50,50"    # Red — Party Secretary
    if "市长" in title and ("副书记" in title or "党组书记" in title or "原定西市长" in title):
        return "50,100,255"   # Blue — Mayor
    if "市长" in title or ("副市长" in title and "常委" not in title):
        return "50,100,255"   # Blue — Government head
    if "纪委" in title or "监委" in title or "监察" in title or "纪委书记" in title:
        return "255,165,0"    # Orange — Discipline
    if "副书记" in title:
        return "200,50,50"    # Dark red — Deputy Secretary
    if "常委" in title:
        return "200,100,100"  # Pink — Other Standing Committee
    if "副市长" in title:
        return "100,100,200"  # Light blue — Deputy Mayor
    if "人大" in title:
        return "200,255,255"  # Cyan — People's Congress
    if "政协" in title:
        return "255,240,200"  # Cream — CPPCC
    return "100,100,100"      # Grey — Other

def person_size(p):
    """Return node size based on role."""
    title = p["current_post"]
    if "市委书记" in title or "人大主任" in title or "政协主席" in title:
        return "20.0"
    if "市长" in title and ("副书记" in title or "党组书记" in title):
        return "20.0"
    if "原定西市长" in title or "原定西书记" in title:
        return "14.0"
    if "副书记" in title or "常委" in title:
        return "14.0"
    if "副市长" in title:
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
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>定西市领导班子工作关系网络 - 数据来源: 定西市人民政府官网, Wikipedia及公开报道</description>')
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
    print(f"=== 定西市网络数据构建 ===")
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
