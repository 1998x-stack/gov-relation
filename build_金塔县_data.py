#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
金塔县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

数据来源:
- 金塔县人民政府网站 (jinta.gov.cn) 领导之窗, 2026年7月确认
- 金塔组工网 (jintadj.gov.cn)
- 百度百科 (杜新红、金塔县)
- 甘肃省委组织部干部任前公示公告 (2024年11月25日)
- 甘肃政务服务网、每日甘肃网、澎湃新闻等公开新闻报道
- 腾讯新闻、搜狐新闻等媒体报道

信息截至: 2026年7月22日
"""

import json
import os
import sqlite3
from datetime import datetime

# ── 路径 ──────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "金塔县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "金塔县_network.gexf")

# ── 数据 ──────────────────────────────────────────────

# 1. 人员
persons = [
    # ── 当前主要领导人 ──
    {
        "id": "p01",
        "name": "杜新红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年11月",
        "birthplace": "甘肃",
        "native_place": "甘肃",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "1990年代?",
        "current_post": "金塔县委书记",
        "current_org": "中共金塔县委员会",
        "source": "金塔县人民政府网站, 甘肃省委组织部任前公示(2024-11-25), 百度百科",
        "person_id": "jinta_du_xinhong"
    },
    {
        "id": "p02",
        "name": "黄小春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年10月",
        "birthplace": "甘肃",
        "native_place": "甘肃",
        "education": "大学/理学学士/工程硕士",
        "party_join": "中共党员",
        "work_start": "约2005年?",
        "current_post": "金塔县委副书记、县长",
        "current_org": "金塔县人民政府",
        "source": "金塔县人民政府网站, 甘肃省委组织部任前公示(2024-11-25)",
        "person_id": "jinta_huang_xiaochun"
    },
    # ── 人大、政协 ──
    {
        "id": "p03",
        "name": "曹彦军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金塔县人大常委会主任",
        "current_org": "金塔县人大常委会",
        "source": "百度百科(金塔县), 金塔县政府网站",
        "person_id": "jinta_cao_yanjun"
    },
    {
        "id": "p04",
        "name": "王军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金塔县政协主席",
        "current_org": "政协金塔县委员会",
        "source": "百度百科(金塔县), 金塔县政府网站",
        "person_id": "jinta_wang_jun"
    },
    # ── 县委常委/副县长 ──
    {
        "id": "p05",
        "name": "潘扬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金塔县委常委、副县长",
        "current_org": "金塔县人民政府",
        "source": "金塔县政府网站领导之窗, 县政府党组会议报道(2026-01)",
        "person_id": "jinta_pan_yang"
    },
    {
        "id": "p06",
        "name": "聂东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金塔县委常委、副县长",
        "current_org": "金塔县人民政府",
        "source": "金塔县政府网站领导之窗, 县政府分工通知(2025-02)",
        "person_id": "jinta_nie_dong"
    },
    {
        "id": "p07",
        "name": "张维华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金塔县副县长、县公安局局长",
        "current_org": "金塔县人民政府/金塔县公安局",
        "source": "金塔县政府网站领导之窗, 县政府党组会议报道(2026-01)",
        "person_id": "jinta_zhang_weihua"
    },
    {
        "id": "p08",
        "name": "李岩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金塔县委常委?/副县长",
        "current_org": "金塔县人民政府",
        "source": "金塔县政府网站领导之窗, 县政府党组会议报道(2026-01)",
        "person_id": "jinta_li_yan"
    },
    {
        "id": "p09",
        "name": "王世良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金塔县副县长",
        "current_org": "金塔县人民政府",
        "source": "金塔县政府网站领导之窗, 县委理论学习中心组报道(2026-01)",
        "person_id": "jinta_wang_shiliang"
    },
    {
        "id": "p10",
        "name": "刘琨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金塔县副县长",
        "current_org": "金塔县人民政府",
        "source": "金塔县政府网站领导之窗, 县政府党组会议报道(2026-01)",
        "person_id": "jinta_liu_kun"
    },
    # ── 县委常委（其他） ──
    {
        "id": "p11",
        "name": "刘志亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金塔县委常委、组织部部长",
        "current_org": "中共金塔县委员会组织部",
        "source": "金塔组工网, 金塔县政府网站",
        "person_id": "jinta_liu_zhiliang"
    },
    {
        "id": "p12",
        "name": "刘建勋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金塔县委常委、政法委书记、金塔工业集中区党工委书记",
        "current_org": "中共金塔县委员会政法委员会",
        "source": "金塔县政府网站, 酒泉政法网, 金塔法院考核报道(2025-01)",
        "person_id": "jinta_liu_jianxun"
    },
    # ── 其他县领导（经常出席活动） ──
    {
        "id": "p13",
        "name": "龚晴",
        "gender": "女?",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金塔县委常委?",
        "current_org": "中共金塔县委员会",
        "source": "腾讯新闻(金塔县委全会报道2026-03), 县委理论学习中心组报道(2026-01)",
        "person_id": "jinta_gong_qing"
    },
    {
        "id": "p14",
        "name": "张建强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金塔县领导",
        "current_org": "中共金塔县委员会",
        "source": "县委理论学习中心组报道(2026-01)",
        "person_id": "jinta_zhang_jianqiang"
    },
    {
        "id": "p15",
        "name": "张延民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金塔县领导",
        "current_org": "中共金塔县委员会",
        "source": "县委理论学习中心组报道(2026-01)",
        "person_id": "jinta_zhang_yanmin"
    },
    {
        "id": "p16",
        "name": "李娜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金塔县领导",
        "current_org": "中共金塔县委员会",
        "source": "县委理论学习中心组报道(2026-01)",
        "person_id": "jinta_li_na"
    },
    # ── 其他县政府党组成员 ──
    {
        "id": "p17",
        "name": "祁正中",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金塔县政府党组成员",
        "current_org": "金塔县人民政府",
        "source": "金塔县政府网站领导之窗, 县政府党组会议报道(2026-01)",
        "person_id": "jinta_qi_zhengzhong"
    },
    {
        "id": "p18",
        "name": "贺晓婧",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金塔县政府党组成员",
        "current_org": "金塔县人民政府",
        "source": "金塔县政府网站领导之窗, 县政府党组会议报道(2026-01)",
        "person_id": "jinta_he_xiaojing"
    },
    # ── 酒泉市领导（上级） ──
    {
        "id": "p19",
        "name": "王立奇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年12月",
        "birthplace": "辽宁北票",
        "native_place": "辽宁北票",
        "education": "研究生/工学硕士(清华大学管理科学与工程)",
        "party_join": "中共党员",
        "work_start": "2003年9月",
        "current_post": "酒泉市委书记",
        "current_org": "中共酒泉市委员会",
        "source": "百度百科, 酒泉市数据脚本",
        "person_id": "jiuquan_wang_liqi"
    },
    {
        "id": "p20",
        "name": "贾志升",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年7月",
        "birthplace": "甘肃镇原",
        "native_place": "甘肃镇原",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "1996年11月",
        "current_post": "酒泉市委副书记、市长",
        "current_org": "酒泉市人民政府",
        "source": "百度百科, 酒泉市数据脚本",
        "person_id": "jiuquan_jia_zhisheng"
    },
    # ── 前任领导 ──
    {
        "id": "p21",
        "name": "李炯芳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查(原金塔县委书记)",
        "current_org": "待查",
        "source": "腾讯新闻(金塔县人大会议2024-01), 当时县委书记为李炯芳",
        "person_id": "jinta_li_jiongfang"
    },
]

# 2. 组织机构
organizations = [
    {"id": "o01", "name": "中共金塔县委员会", "type": "党委", "level": "县处级", "parent": "中共酒泉市委员会", "location": "甘肃省酒泉市金塔县"},
    {"id": "o02", "name": "金塔县人民政府", "type": "政府", "level": "县处级", "parent": "酒泉市人民政府", "location": "甘肃省酒泉市金塔县"},
    {"id": "o03", "name": "金塔县人大常委会", "type": "人大", "level": "县处级", "parent": "金塔县", "location": "甘肃省酒泉市金塔县"},
    {"id": "o04", "name": "政协金塔县委员会", "type": "政协", "level": "县处级", "parent": "金塔县", "location": "甘肃省酒泉市金塔县"},
    {"id": "o05", "name": "中共金塔县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共金塔县委员会", "location": "甘肃省酒泉市金塔县"},
    {"id": "o06", "name": "中共金塔县委员会组织部", "type": "党委", "level": "县处级", "parent": "中共金塔县委员会", "location": "甘肃省酒泉市金塔县"},
    {"id": "o07", "name": "中共金塔县委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共金塔县委员会", "location": "甘肃省酒泉市金塔县"},
    {"id": "o08", "name": "金塔县公安局", "type": "政府", "level": "正科级", "parent": "金塔县人民政府", "location": "甘肃省酒泉市金塔县"},
    {"id": "o09", "name": "金塔工业集中区管委会", "type": "开发区", "level": "副县级", "parent": "金塔县人民政府", "location": "甘肃省酒泉市金塔县"},
    {"id": "o10", "name": "中共酒泉市委员会", "type": "党委", "level": "地厅级", "parent": "中共甘肃省委员会", "location": "甘肃省酒泉市"},
    {"id": "o11", "name": "酒泉市人民政府", "type": "政府", "level": "地厅级", "parent": "甘肃省人民政府", "location": "甘肃省酒泉市"},
    {"id": "o12", "name": "酒泉市水务局", "type": "政府", "level": "县处级", "parent": "酒泉市人民政府", "location": "甘肃省酒泉市"},
    {"id": "o13", "name": "金昌经济技术开发区管委会", "type": "开发区", "level": "县处级", "parent": "金昌市人民政府", "location": "甘肃省金昌市"},
]

# 3. 任职
positions = [
    # 杜新红
    {"person_id": "p01", "org_id": "o12", "title": "酒泉市水务局局长", "start": "2020年5月", "end": "2021年9月", "rank": "正县级", "note": ""},
    {"person_id": "p01", "org_id": "o02", "title": "金塔县委副书记、县长候选人", "start": "2021年8月", "end": "2021年11月", "rank": "正县级", "note": ""},
    {"person_id": "p01", "org_id": "o02", "title": "金塔县委副书记、县长", "start": "2021年11月", "end": "2024年11月", "rank": "正县级", "note": ""},
    {"person_id": "p01", "org_id": "o01", "title": "金塔县委书记", "start": "2024年11月", "end": "至今", "rank": "正县级", "note": "主持县委全面工作; 2024年11月任前公示, 此前为金塔县长"},
    # 黄小春
    {"person_id": "p02", "org_id": "o13", "title": "金昌经济技术开发区党工委书记、管委会主任、高新区管委会主任(兼)", "start": "?", "end": "2024年12月", "rank": "正县级", "note": "2024年11月任前公示拟提名为县长候选人"},
    {"person_id": "p02", "org_id": "o02", "title": "金塔县委副书记、代县长", "start": "2024年12月", "end": "2025年1月", "rank": "副县级", "note": "2024年12月以县长候选人身份调研核产业园"},
    {"person_id": "p02", "org_id": "o01", "title": "金塔县委副书记", "start": "2024年12月", "end": "至今", "rank": "副县级", "note": "兼任县长"},
    {"person_id": "p02", "org_id": "o02", "title": "金塔县县长", "start": "2025年1月", "end": "至今", "rank": "正县级", "note": "2025年1月在县人大会议上正式当选"},
    # 曹彦军 - 人大主任
    {"person_id": "p03", "org_id": "o03", "title": "金塔县人大常委会主任", "start": "?", "end": "至今", "rank": "正县级", "note": ""},
    # 王军 - 政协主席
    {"person_id": "p04", "org_id": "o04", "title": "金塔县政协主席", "start": "?", "end": "至今", "rank": "正县级", "note": ""},
    # 潘扬 - 县委常委、副县长
    {"person_id": "p05", "org_id": "o01", "title": "金塔县委常委", "start": "?", "end": "至今", "rank": "副县级", "note": ""},
    {"person_id": "p05", "org_id": "o02", "title": "金塔县副县长", "start": "?", "end": "至今", "rank": "副县级", "note": "县政府党组成员"},
    # 聂东 - 县委常委、副县长
    {"person_id": "p06", "org_id": "o01", "title": "金塔县委常委", "start": "?", "end": "至今", "rank": "副县级", "note": ""},
    {"person_id": "p06", "org_id": "o02", "title": "金塔县副县长", "start": "?", "end": "至今", "rank": "副县级", "note": "负责科技、工业、生态环境、交通等工作"},
    # 张维华 - 副县长、公安局长
    {"person_id": "p07", "org_id": "o02", "title": "金塔县副县长、县公安局局长", "start": "?", "end": "至今", "rank": "副县级", "note": "负责公安、司法、信访等工作"},
    {"person_id": "p07", "org_id": "o08", "title": "金塔县公安局党委书记、局长、督察长", "start": "?", "end": "至今", "rank": "正科级", "note": ""},
    # 李岩 - 副县长
    {"person_id": "p08", "org_id": "o02", "title": "金塔县副县长", "start": "?", "end": "至今", "rank": "副县级", "note": "县政府党组成员"},
    # 王世良 - 副县长
    {"person_id": "p09", "org_id": "o02", "title": "金塔县副县长", "start": "?", "end": "至今", "rank": "副县级", "note": ""},
    # 刘琨 - 副县长
    {"person_id": "p10", "org_id": "o02", "title": "金塔县副县长", "start": "?", "end": "至今", "rank": "副县级", "note": ""},
    # 刘志亮 - 组织部长
    {"person_id": "p11", "org_id": "o01", "title": "金塔县委常委", "start": "?", "end": "至今", "rank": "副县级", "note": ""},
    {"person_id": "p11", "org_id": "o06", "title": "金塔县委组织部部长", "start": "?", "end": "至今", "rank": "副县级", "note": ""},
    # 刘建勋 - 政法委书记
    {"person_id": "p12", "org_id": "o01", "title": "金塔县委常委", "start": "?", "end": "至今", "rank": "副县级", "note": ""},
    {"person_id": "p12", "org_id": "o07", "title": "金塔县委政法委书记", "start": "?", "end": "至今", "rank": "副县级", "note": ""},
    {"person_id": "p12", "org_id": "o09", "title": "金塔工业集中区党工委书记", "start": "?", "end": "至今", "rank": "副县级", "note": ""},
    # 龚晴 - 县领导
    {"person_id": "p13", "org_id": "o01", "title": "金塔县委常委?", "start": "?", "end": "至今", "rank": "副县级", "note": "出席县委全会和理论学习中心组会议"},
    # 张建强 - 县领导
    {"person_id": "p14", "org_id": "o01", "title": "金塔县领导", "start": "?", "end": "至今", "rank": "副县级", "note": "出席理论学习中心组会议"},
    # 张延民 - 县领导
    {"person_id": "p15", "org_id": "o01", "title": "金塔县领导", "start": "?", "end": "至今", "rank": "副县级", "note": "出席理论学习中心组会议"},
    # 李娜 - 县领导
    {"person_id": "p16", "org_id": "o01", "title": "金塔县领导", "start": "?", "end": "至今", "rank": "副县级", "note": "出席理论学习中心组会议"},
    # 祁正中 - 县政府党组成员
    {"person_id": "p17", "org_id": "o02", "title": "金塔县政府党组成员", "start": "?", "end": "至今", "rank": "副县级", "note": ""},
    # 贺晓婧 - 县政府党组成员
    {"person_id": "p18", "org_id": "o02", "title": "金塔县政府党组成员", "start": "?", "end": "至今", "rank": "副县级", "note": ""},
    # 王立奇 - 酒泉市委书记
    {"person_id": "p19", "org_id": "o10", "title": "酒泉市委书记", "start": "?", "end": "至今", "rank": "正厅级", "note": ""},
    # 贾志升 - 酒泉市长
    {"person_id": "p20", "org_id": "o11", "title": "酒泉市市长", "start": "?", "end": "至今", "rank": "正厅级", "note": ""},
    # 李炯芳 - 前县委书记
    {"person_id": "p21", "org_id": "o01", "title": "金塔县委书记", "start": "?", "end": "约2024年初", "rank": "正县级", "note": "前任县委书记; 杜新红的前任"},
]

# 4. 关系
relationships = [
    # 党政一把手
    {"person_a": "p01", "person_b": "p02", "type": "overlap", "context": "杜新红(书记)与黄小春(县长): 金塔县党政一把手配合作", "overlap_org": "中共金塔县委员会/金塔县人民政府", "overlap_period": "2025年至今", "strength": "strong", "confidence": "confirmed"},
    # 书记-人大
    {"person_a": "p01", "person_b": "p03", "type": "overlap", "context": "杜新红(书记)与曹彦军(人大主任): 党委与人大配合作", "overlap_org": "金塔县四套班子", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 书记-政协
    {"person_a": "p01", "person_b": "p04", "type": "overlap", "context": "杜新红(书记)与王军(政协主席): 党委与政协配合作", "overlap_org": "金塔县四套班子", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 县长-副县长(潘扬)
    {"person_a": "p02", "person_b": "p05", "type": "overlap", "context": "黄小春(县长)与潘扬(副县长): 政府正副手关系", "overlap_org": "金塔县人民政府", "overlap_period": "2025年至今", "strength": "strong", "confidence": "confirmed"},
    # 县长-副县长(聂东)
    {"person_a": "p02", "person_b": "p06", "type": "overlap", "context": "黄小春(县长)与聂东(副县长): 政府正副手关系", "overlap_org": "金塔县人民政府", "overlap_period": "2025年至今", "strength": "strong", "confidence": "confirmed"},
    # 书记-组织部长
    {"person_a": "p01", "person_b": "p11", "type": "overlap", "context": "杜新红(书记)与刘志亮(组织部长): 党委班子上下级", "overlap_org": "中共金塔县委员会", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 书记-政法委书记
    {"person_a": "p01", "person_b": "p12", "type": "overlap", "context": "杜新红(书记)与刘建勋(政法委书记): 党委班子上下级", "overlap_org": "中共金塔县委员会", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 县长-公安局长
    {"person_a": "p02", "person_b": "p07", "type": "overlap", "context": "黄小春(县长)与张维华(副县长/公安局长): 政府上下级", "overlap_org": "金塔县人民政府", "overlap_period": "2025年至今", "strength": "strong", "confidence": "confirmed"},
    # 书记-李岩(副县长)
    {"person_a": "p01", "person_b": "p08", "type": "overlap", "context": "杜新红(书记)与李岩(副县长): 党政班子上下级", "overlap_org": "金塔县人民政府/县委", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 书记-王世良
    {"person_a": "p01", "person_b": "p09", "type": "overlap", "context": "杜新红(书记)与王世良(副县长): 党委政府上下级", "overlap_org": "金塔县人民政府/县委", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 书记-刘琨
    {"person_a": "p01", "person_b": "p10", "type": "overlap", "context": "杜新红(书记)与刘琨(副县长): 党委政府上下级", "overlap_org": "金塔县人民政府/县委", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 前任-现任关系(县委书记)
    {"person_a": "p21", "person_b": "p01", "type": "predecessor_successor", "context": "李炯芳(前任书记)与杜新红(现任书记): 金塔县委书记交接", "overlap_org": "中共金塔县委员会", "overlap_period": "约2024年", "strength": "strong", "confidence": "confirmed"},
    # 杜新红自己从县长升书记
    {"person_a": "p21", "person_b": "p01", "type": "predecessor_successor", "context": "李炯芳卸任后, 杜新红由县长接任县委书记", "overlap_org": "中共金塔县委员会", "overlap_period": "2024年", "strength": "strong", "confidence": "confirmed"},
    # 酒泉市-金塔县上下级
    {"person_a": "p19", "person_b": "p01", "type": "superior_subordinate", "context": "王立奇(酒泉市委书记)与杜新红(金塔县委书记): 市级对县级", "overlap_org": "酒泉市/金塔县", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p20", "person_b": "p02", "type": "superior_subordinate", "context": "贾志升(酒泉市长)与黄小春(金塔县长): 市级对县级", "overlap_org": "酒泉市/金塔县", "overlap_period": "2025年至今", "strength": "strong", "confidence": "confirmed"},
    # 杜新红之前任酒泉市水务局长时的上下级
    {"person_a": "p19", "person_b": "p01", "type": "superior_subordinate", "context": "王立奇(酒泉书记)与杜新红(曾任酒泉市水务局长): 此前在市级有过工作关系", "overlap_org": "酒泉市", "overlap_period": "2020-2021", "strength": "medium", "confidence": "plausible"},
    # 县委常委间同僚关系
    {"person_a": "p05", "person_b": "p06", "type": "overlap", "context": "潘扬与聂东: 同为县委常委/副县长", "overlap_org": "金塔县人民政府", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p11", "person_b": "p12", "type": "overlap", "context": "刘志亮(组织部长)与刘建勋(政法委书记): 县委常委同僚", "overlap_org": "中共金塔县委员会", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p05", "person_b": "p11", "type": "overlap", "context": "潘扬(常委/副县长)与刘志亮(组织部长): 县委常委同僚", "overlap_org": "中共金塔县委员会", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 杜新红任县长时的副县长们
    {"person_a": "p01", "person_b": "p05", "type": "overlap", "context": "杜新红(曾任县长)与潘扬(副县长): 此前县长与副县长配合", "overlap_org": "金塔县人民政府", "overlap_period": "2021-2024年", "strength": "strong", "confidence": "confirmed"},
    # 政府党组成员
    {"person_a": "p02", "person_b": "p17", "type": "overlap", "context": "黄小春(县长)与祁正中(政府党组成员): 政府党组上下级", "overlap_org": "金塔县人民政府", "overlap_period": "2025年至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p02", "person_b": "p18", "type": "overlap", "context": "黄小春(县长)与贺晓婧(政府党组成员): 政府党组上下级", "overlap_org": "金塔县人民政府", "overlap_period": "2025年至今", "strength": "strong", "confidence": "confirmed"},
]


# ── 辅助函数 ──────────────────────────────────────────

def esc(s):
    """XML转义"""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """按角色返回RGB颜色"""
    title = p["current_post"]
    if "书记" in title and "纪委" not in title and "统战" not in title:
        if "副书记" in title:
            return "200,50,50"   # 暗红 — 副职(如县委副书记)
        return "255,50,50"   # 红色 — 党委正职
    if "县长" in title or ("长" in title and "副县长" not in title and "部长" not in title):
        return "50,100,255"  # 蓝色 — 政府领导
    if "纪委" in title or "监委" in title:
        return "255,165,0"   # 橙色 — 纪检
    if "常委" in title:
        return "200,100,100" # 粉红 — 其他常委
    if "人大" in title:
        return "200,255,255" # 青色 — 人大
    if "政协" in title:
        return "255,240,200" # 米色 — 政协
    if "副市长" in title or "副区长" in title or "副县长" in title:
        return "100,100,200" # 浅蓝 — 副市/县/区长
    return "100,100,100"     # 灰色 — 其他

def person_size(p):
    """按角色返回节点大小"""
    title = p["current_post"]
    if "县委书记" in title or "县长" in title:
        return "20.0"
    if "副书记" in title or "常委" in title:
        return "14.0"
    if "人大" in title or "政协" in title:
        return "12.0"
    if "副县长" in title:
        return "12.0"
    return "10.0"

def org_color(o):
    """按类型返回组织颜色"""
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "开发区": "200,255,200",
    }
    return colors.get(t, "200,200,200")

# ── 构建数据库 ────────────────────────────────────────

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
        overlap_org TEXT, overlap_period TEXT, strength TEXT, confidence TEXT,
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
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence)
                     VALUES (?,?,?,?,?,?,?,?)""", (
            r["person_a"], r["person_b"], r["type"], r["context"],
            r["overlap_org"], r["overlap_period"], r.get("strength", "medium"), r.get("confidence", "plausible")
        ))

    conn.commit()
    conn.close()

# ── 构建 GEXF ─────────────────────────────────────────

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>金塔县领导班子工作关系网络 - 数据来源: 公开报道、政府网站及甘肃省委组织部公示</description>')
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
        lines.append('          <attvalue for="3" value="金塔县"/>')
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
        lines.append('          <attvalue for="3" value="金塔县"/>')
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

# ── 主函数 ──────────────────────────────────────────

def main():
    print(f"=== 金塔县网络数据构建 ===")
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
