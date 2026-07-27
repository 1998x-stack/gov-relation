#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
陇南市 (甘肃省) 领导班子工作关系网络数据构建脚本
Generate SQLite database + GEXF graph for Longnan City leadership network.

Level: 地级市
Province: 甘肃省
Region: 陇南市
Targets: 市委书记 & 市长

Research Sources:
- 陇南市人民政府官方网站 (longnan.gov.cn) 领导之窗, 2026年7月确认

Research Date: 2026-07-22
"""

import os
import sqlite3
from datetime import datetime

STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "陇南市_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "陇南市_network.gexf")

# ═══════════════════════════════════════════════
# 人员数据
# ═══════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 市委主要领导
    # ════════════════════════════════════════
    {
        "id": "longnan_liu_yongge",
        "name": "刘永革",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年12月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇南市委书记",
        "current_org": "中共陇南市委员会",
        "source": "https://www.longnan.gov.cn/ldzc/",
    },
    {
        "id": "longnan_zhang_qiang",
        "name": "张强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇南市委副书记、市长",
        "current_org": "中共陇南市委员会/陇南市人民政府",
        "source": "https://www.longnan.gov.cn/ldzc/",
    },
    {
        "id": "longnan_zhu_fengtao",
        "name": "朱锋涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇南市委副书记",
        "current_org": "中共陇南市委员会",
        "source": "https://www.longnan.gov.cn/ldzc/",
    },
    {
        "id": "longnan_wang_lijun",
        "name": "王立军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇南市委常委、市纪委书记、市监委主任",
        "current_org": "中共陇南市纪律检查委员会/陇南市监察委员会",
        "source": "https://www.longnan.gov.cn/ldzc/",
    },
    {
        "id": "longnan_tang_jinjun",
        "name": "唐进军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇南市委常委、秘书长",
        "current_org": "中共陇南市委员会",
        "source": "https://www.longnan.gov.cn/ldzc/",
    },
    {
        "id": "longnan_li_hui",
        "name": "李辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇南市委常委、武都区委书记",
        "current_org": "中共陇南市武都区委员会",
        "source": "https://www.longnan.gov.cn/ldzc/",
    },
    {
        "id": "longnan_ma_guokai",
        "name": "马国开",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇南市委常委、常务副市长",
        "current_org": "中共陇南市委员会/陇南市人民政府",
        "source": "https://www.longnan.gov.cn/ldzc/",
    },
    {
        "id": "longnan_wang_fan",
        "name": "王凡",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇南市委常委、宣传部部长",
        "current_org": "中共陇南市委员会宣传部",
        "source": "https://www.longnan.gov.cn/ldzc/",
    },
    {
        "id": "longnan_wei_shidong",
        "name": "魏世东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇南市委常委、组织部部长、统战部部长",
        "current_org": "中共陇南市委员会组织部/统战部",
        "source": "https://www.longnan.gov.cn/ldzc/",
    },
    {
        "id": "longnan_chen_jun",
        "name": "陈军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇南市委常委、市委政法委书记",
        "current_org": "中共陇南市委员会政法委员会",
        "source": "https://www.longnan.gov.cn/ldzc/",
    },
    {
        "id": "longnan_xu_guangyao",
        "name": "徐光耀",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇南市委常委、陇南军分区党委书记、政治委员",
        "current_org": "陇南军分区",
        "source": "https://www.longnan.gov.cn/ldzc/",
    },
    {
        "id": "longnan_yan_hehao",
        "name": "闫和浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇南市委常委、副市长",
        "current_org": "中共陇南市委员会/陇南市人民政府",
        "source": "https://www.longnan.gov.cn/ldzc/",
    },
    # ════════════════════════════════════════
    # 市政府副市长（非市委常委）
    # ════════════════════════════════════════
    {
        "id": "longnan_wang_jinghai",
        "name": "汪精海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇南市副市长",
        "current_org": "陇南市人民政府",
        "source": "https://www.longnan.gov.cn/ldzc/",
    },
    {
        "id": "longnan_zhang_bo",
        "name": "张波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇南市副市长",
        "current_org": "陇南市人民政府",
        "source": "https://www.longnan.gov.cn/ldzc/",
    },
    {
        "id": "longnan_zhou_ji",
        "name": "周济",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇南市副市长",
        "current_org": "陇南市人民政府",
        "source": "https://www.longnan.gov.cn/ldzc/",
    },
    {
        "id": "longnan_wang_yingju",
        "name": "王英菊",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇南市副市长",
        "current_org": "陇南市人民政府",
        "source": "https://www.longnan.gov.cn/ldzc/",
    },
    {
        "id": "longnan_liu_dongxiao",
        "name": "刘东晓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇南市副市长",
        "current_org": "陇南市人民政府",
        "source": "https://www.longnan.gov.cn/ldzc/",
    },
    # ════════════════════════════════════════
    # 市政府秘书长
    # ════════════════════════════════════════
    {
        "id": "longnan_zhou_dingtang",
        "name": "周定堂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "陇南市政府秘书长",
        "current_org": "陇南市人民政府",
        "source": "https://www.longnan.gov.cn/ldzc/",
    },
]

# ═══════════════════════════════════════════════
# 组织机构数据
# ═══════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共陇南市委员会",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共甘肃省委员会",
        "location": "甘肃省陇南市",
    },
    {
        "id": 2,
        "name": "陇南市人民政府",
        "type": "政府",
        "level": "地厅级",
        "parent": "甘肃省人民政府",
        "location": "甘肃省陇南市",
    },
    {
        "id": 3,
        "name": "中共陇南市纪律检查委员会/陇南市监察委员会",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共甘肃省纪律检查委员会",
        "location": "甘肃省陇南市",
    },
    {
        "id": 4,
        "name": "中共陇南市委员会宣传部",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共陇南市委员会",
        "location": "甘肃省陇南市",
    },
    {
        "id": 5,
        "name": "中共陇南市委员会组织部/统战部",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共陇南市委员会",
        "location": "甘肃省陇南市",
    },
    {
        "id": 6,
        "name": "中共陇南市委员会政法委员会",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共陇南市委员会",
        "location": "甘肃省陇南市",
    },
    {
        "id": 7,
        "name": "陇南军分区",
        "type": "事业单位",
        "level": "地厅级",
        "parent": "甘肃省军区",
        "location": "甘肃省陇南市",
    },
    {
        "id": 8,
        "name": "中共陇南市武都区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共陇南市委员会",
        "location": "甘肃省陇南市武都区",
    },
]

# ═══════════════════════════════════════════════
# 任职数据
# ═══════════════════════════════════════════════

positions = [
    # 刘永革 — 市委书记
    {"person_id": "longnan_liu_yongge", "org_id": 1, "title": "陇南市委书记", "start": "", "end": "present", "rank": "正厅级", "note": "主持市委全面工作"},
    # 张强 — 市长/副书记
    {"person_id": "longnan_zhang_qiang", "org_id": 1, "title": "陇南市委副书记", "start": "", "end": "present", "rank": "正厅级", "note": "兼任市长"},
    {"person_id": "longnan_zhang_qiang", "org_id": 2, "title": "陇南市市长", "start": "", "end": "present", "rank": "正厅级", "note": "主持市政府全面工作"},
    # 朱锋涛 — 副书记
    {"person_id": "longnan_zhu_fengtao", "org_id": 1, "title": "陇南市委副书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 王立军 — 纪委书记
    {"person_id": "longnan_wang_lijun", "org_id": 1, "title": "陇南市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "longnan_wang_lijun", "org_id": 3, "title": "陇南市纪委书记、市监委主任", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 唐进军 — 秘书长
    {"person_id": "longnan_tang_jinjun", "org_id": 1, "title": "陇南市委常委、秘书长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 李辉 — 武都区委书记
    {"person_id": "longnan_li_hui", "org_id": 1, "title": "陇南市委常委", "start": "", "end": "present", "rank": "副厅级", "note": "兼任武都区委书记"},
    {"person_id": "longnan_li_hui", "org_id": 8, "title": "武都区委书记", "start": "", "end": "present", "rank": "县处级", "note": "市委常委兼任"},
    # 马国开 — 常务副市长
    {"person_id": "longnan_ma_guokai", "org_id": 1, "title": "陇南市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "longnan_ma_guokai", "org_id": 2, "title": "陇南市常务副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 王凡 — 宣传部部长
    {"person_id": "longnan_wang_fan", "org_id": 1, "title": "陇南市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "longnan_wang_fan", "org_id": 4, "title": "陇南市宣传部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 魏世东 — 组织部、统战部
    {"person_id": "longnan_wei_shidong", "org_id": 1, "title": "陇南市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "longnan_wei_shidong", "org_id": 5, "title": "陇南市组织部部长、统战部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 陈军 — 政法委书记
    {"person_id": "longnan_chen_jun", "org_id": 1, "title": "陇南市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "longnan_chen_jun", "org_id": 6, "title": "陇南市政法委书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 徐光耀 — 军分区
    {"person_id": "longnan_xu_guangyao", "org_id": 1, "title": "陇南市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "longnan_xu_guangyao", "org_id": 7, "title": "陇南军分区党委书记、政治委员", "start": "", "end": "present", "rank": "正师级", "note": ""},
    # 闫和浩 — 副市长（常委）
    {"person_id": "longnan_yan_hehao", "org_id": 1, "title": "陇南市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "longnan_yan_hehao", "org_id": 2, "title": "陇南市副市长", "start": "", "end": "present", "rank": "副厅级", "note": "市委常委兼任"},
    # 汪精海 — 副市长
    {"person_id": "longnan_wang_jinghai", "org_id": 2, "title": "陇南市副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 张波 — 副市长
    {"person_id": "longnan_zhang_bo", "org_id": 2, "title": "陇南市副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 周济 — 副市长
    {"person_id": "longnan_zhou_ji", "org_id": 2, "title": "陇南市副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 王英菊 — 副市长
    {"person_id": "longnan_wang_yingju", "org_id": 2, "title": "陇南市副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 刘东晓 — 副市长
    {"person_id": "longnan_liu_dongxiao", "org_id": 2, "title": "陇南市副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 周定堂 — 秘书长
    {"person_id": "longnan_zhou_dingtang", "org_id": 2, "title": "陇南市政府秘书长", "start": "", "end": "present", "rank": "正处级", "note": ""},
]

# ═══════════════════════════════════════════════
# 关系数据
# ═══════════════════════════════════════════════

relationships = [
    # 党政一把手关系
    {
        "person_a": "longnan_liu_yongge",
        "person_b": "longnan_zhang_qiang",
        "type": "superior_subordinate",
        "context": "刘永革(市委书记)与张强(市长): 党政一把手搭班工作关系",
        "overlap_org": "中共陇南市委员会/陇南市人民政府",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 书记-副书记关系
    {
        "person_a": "longnan_liu_yongge",
        "person_b": "longnan_zhu_fengtao",
        "type": "overlap",
        "context": "刘永革(书记)与朱锋涛(副书记): 书记-副书记班子配合",
        "overlap_org": "中共陇南市委员会",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 市长-副市长关系（常务）
    {
        "person_a": "longnan_zhang_qiang",
        "person_b": "longnan_ma_guokai",
        "type": "overlap",
        "context": "张强(市长)与马国开(常务副市长): 政府正副手配合",
        "overlap_org": "陇南市人民政府",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 市长-副市长（常委）
    {
        "person_a": "longnan_zhang_qiang",
        "person_b": "longnan_yan_hehao",
        "type": "overlap",
        "context": "张强(市长)与闫和浩(常委副市长): 政府班子配合",
        "overlap_org": "陇南市人民政府",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 市长-其他副市长
    {
        "person_a": "longnan_zhang_qiang",
        "person_b": "longnan_wang_jinghai",
        "type": "overlap",
        "context": "张强(市长)与汪精海(副市长): 政府班子配合",
        "overlap_org": "陇南市人民政府",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": "longnan_zhang_qiang",
        "person_b": "longnan_zhang_bo",
        "type": "overlap",
        "context": "张强(市长)与张波(副市长): 政府班子配合",
        "overlap_org": "陇南市人民政府",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": "longnan_zhang_qiang",
        "person_b": "longnan_zhou_ji",
        "type": "overlap",
        "context": "张强(市长)与周济(副市长): 政府班子配合",
        "overlap_org": "陇南市人民政府",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": "longnan_zhang_qiang",
        "person_b": "longnan_wang_yingju",
        "type": "overlap",
        "context": "张强(市长)与王英菊(副市长): 政府班子配合",
        "overlap_org": "陇南市人民政府",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": "longnan_zhang_qiang",
        "person_b": "longnan_liu_dongxiao",
        "type": "overlap",
        "context": "张强(市长)与刘东晓(副市长): 政府班子配合",
        "overlap_org": "陇南市人民政府",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 书记-各常委
    {
        "person_a": "longnan_liu_yongge",
        "person_b": "longnan_wang_lijun",
        "type": "overlap",
        "context": "刘永革(书记)与王立军(纪委书记): 党委-纪委班子配合",
        "overlap_org": "中共陇南市委员会",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": "longnan_liu_yongge",
        "person_b": "longnan_tang_jinjun",
        "type": "overlap",
        "context": "刘永革(书记)与唐进军(秘书长): 书记-秘书长工作配合",
        "overlap_org": "中共陇南市委员会",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": "longnan_liu_yongge",
        "person_b": "longnan_li_hui",
        "type": "overlap",
        "context": "刘永革(书记)与李辉(武都区委书记): 市委-区委领导配合",
        "overlap_org": "中共陇南市委员会",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": "longnan_liu_yongge",
        "person_b": "longnan_ma_guokai",
        "type": "overlap",
        "context": "刘永革(书记)与马国开(常务副市长): 党委-政府领导配合",
        "overlap_org": "中共陇南市委员会",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": "longnan_liu_yongge",
        "person_b": "longnan_wang_fan",
        "type": "overlap",
        "context": "刘永革(书记)与王凡(宣传部部长): 党委-宣传领导配合",
        "overlap_org": "中共陇南市委员会",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": "longnan_liu_yongge",
        "person_b": "longnan_wei_shidong",
        "type": "overlap",
        "context": "刘永革(书记)与魏世东(组织部、统战部部长): 党委-组织统战领导配合",
        "overlap_org": "中共陇南市委员会",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": "longnan_liu_yongge",
        "person_b": "longnan_chen_jun",
        "type": "overlap",
        "context": "刘永革(书记)与陈军(政法委书记): 党委-政法领导配合",
        "overlap_org": "中共陇南市委员会",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": "longnan_liu_yongge",
        "person_b": "longnan_yan_hehao",
        "type": "overlap",
        "context": "刘永革(书记)与闫和浩(常委副市长): 党委-政府领导配合",
        "overlap_org": "中共陇南市委员会",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 副书记与常委
    {
        "person_a": "longnan_zhu_fengtao",
        "person_b": "longnan_wang_lijun",
        "type": "overlap",
        "context": "朱锋涛(副书记)与王立军(纪委书记): 副书记-纪委书记班子配合",
        "overlap_org": "中共陇南市委员会",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": "longnan_zhu_fengtao",
        "person_b": "longnan_ma_guokai",
        "type": "overlap",
        "context": "朱锋涛(副书记)与马国开(常务副市长): 副书记-常务副市长班子配合",
        "overlap_org": "中共陇南市委员会",
        "overlap_period": "至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 纪委书记-组织部部长
    {
        "person_a": "longnan_wang_lijun",
        "person_b": "longnan_wei_shidong",
        "type": "overlap",
        "context": "王立军(纪委书记)与魏世东(组织部部长): 纪委-组织部工作衔接",
        "overlap_org": "中共陇南市委员会",
        "overlap_period": "至今",
        "strength": "medium",
        "confidence": "confirmed",
    },
    # 常委之间
    {
        "person_a": "longnan_tang_jinjun",
        "person_b": "longnan_wang_fan",
        "type": "overlap",
        "context": "唐进军(秘书长)与王凡(宣传部部长): 市委办公厅-宣传部配合",
        "overlap_org": "中共陇南市委员会",
        "overlap_period": "至今",
        "strength": "medium",
        "confidence": "confirmed",
    },
    {
        "person_a": "longnan_chen_jun",
        "person_b": "longnan_wei_shidong",
        "type": "overlap",
        "context": "陈军(政法委书记)与魏世东(组织部部长): 政法-组织工作衔接",
        "overlap_org": "中共陇南市委员会",
        "overlap_period": "至今",
        "strength": "medium",
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
    if "书记" in title and "纪委" not in title and "统战" not in title and "宣传" not in title and "政法委" not in title and "组织" not in title:
        if "副书记" in title:
            return "200,50,50"    # Dark red — Deputy Secretary
        return "255,50,50"    # Red — Party Secretary
    if "市长" in title and "副" not in title:
        return "50,100,255"   # Blue — Government head
    if "纪委" in title or "监委" in title or "监察" in title or "纪委书记" in title:
        return "255,165,0"    # Orange — Discipline
    if "副书记" in title:
        return "200,50,50"    # Dark red — Deputy Secretary
    if "常委" in title:
        return "200,100,100"  # Pink — Other Standing Committee
    if "副市长" in title or "副" in title:
        return "100,100,200"  # Light blue — Deputy
    if "秘书长" in title:
        return "100,100,100"  # Grey — Secretary-General
    return "100,100,100"      # Grey — Other


def person_size(p):
    """Return node size based on role."""
    title = p["current_post"]
    if "市委书记" in title:
        return "20.0"
    if "市长" in title and "副" not in title:
        return "20.0"
    if "副书记" in title:
        return "16.0"
    if "常委" in title:
        return "14.0"
    if "副市长" in title or "秘书长" in title:
        return "12.0"
    return "10.0"


def org_color(o):
    """Return RGB color string based on org type."""
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "事业单位": "220,220,220",
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
    lines.append('    <description>陇南市领导班子工作关系网络 - 数据来源: 陇南市人民政府官网(longnan.gov.cn)领导之窗</description>')
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
        lines.append('          <attvalue for="3" value="陇南市"/>')
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
        lines.append('          <attvalue for="3" value="陇南市"/>')
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
    print(f"=== 陇南市网络数据构建 ===")
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
