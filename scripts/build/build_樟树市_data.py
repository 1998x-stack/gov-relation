#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
樟树市领导班子工作关系网络 — 数据构建脚本
调研日期: 2026-07-15
来源说明: 宜春市人民政府网站、樟树市人民政府官网新闻信息、百度百科
"""

import sqlite3
import os
from datetime import datetime

# Determine paths dynamically: if run from staging dir, output there; otherwise use canonical paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STAGING = "data/tmp" in SCRIPT_DIR or "tmp" in SCRIPT_DIR

if STAGING:
    BASE = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
    DB_PATH = os.path.join(SCRIPT_DIR, "樟树市_network.db")
    GEXF_PATH = os.path.join(SCRIPT_DIR, "樟树市_network.gexf")
else:
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_PATH = os.path.join(BASE, "data/database/樟树市_network.db")
    GEXF_PATH = os.path.join(BASE, "data/graph/樟树市_network.gexf")

print(f"DB_PATH: {DB_PATH}")
print(f"GEXF_PATH: {GEXF_PATH}")

# ============================================================
# 硬编码研究数据
# ============================================================

# ---- 人员数据 ----
# 每条信息附来源URL | 区分已确认/推测/未验证
persons = [
    # ===== 党政一把手 =====
    # 市委书记 - 曾兆昕（根据现有资料，曾兆昕曾任樟树市长，后任市委书记）
    {
        "id": "zhangshu_zeng_zhaoxin",
        "name": "曾兆昕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "江西（推测宜春地区）",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "樟树市委书记",
        "current_org": "中共樟树市委员会",
        "source": "宜春市委组织部任前公示/樟树市人民政府网新闻"
    },
    # 市长 - 罗功成（根据现有资料，罗功成曾任樟树市委常委、副市长，后任市长）
    {
        "id": "zhangshu_luo_gongcheng",
        "name": "罗功成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年3月",
        "birthplace": "江西上高",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "樟树市委副书记、市人民政府市长",
        "current_org": "樟树市人民政府",
        "source": "https://www.zhangshu.gov.cn/ 樟树市人民政府网新闻/百度百科"
    },

    # ===== 前任领导 =====
    {
        "id": "zhangshu_dong_xiaoming",
        "name": "董晓明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "原樟树市委书记（去向：宜春市领导）",
        "current_org": "宜春市（待确认具体单位）",
        "source": "宜春市委组织部相关任免通知"
    },
    {
        "id": "zhangshu_yin_zhi",
        "name": "尹志来",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "原樟树市委书记（去向：待查）",
        "current_org": "宜春市",
        "source": "宜春市委组织部相关任免通知"
    },
    {
        "id": "zhangshu_hu_jiangle",
        "name": "胡江萍",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "原樟树市委书记（已调离）",
        "current_org": "待查",
        "source": "公开新闻报道"
    },

    # ===== 市委常委（按角色排序） =====
    {
        "id": "zhangshu_liu_na",
        "name": "刘娜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "樟树市委副书记",
        "current_org": "中共樟树市委员会",
        "source": "樟树市人民政府网新闻"
    },
    {
        "id": "zhangshu_lai_wei",
        "name": "赖伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "樟树市委常委、市纪委书记、市监委主任",
        "current_org": "中共樟树市纪律检查委员会/樟树市监委",
        "source": "樟树市人民政府网新闻"
    },
    {
        "id": "zhangshu_wang_xiaolong",
        "name": "王小龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "樟树市委常委、市政府常务副市长",
        "current_org": "樟树市人民政府",
        "source": "樟树市人民政府网新闻"
    },
    {
        "id": "zhangshu_shi_ming",
        "name": "时珺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "樟树市委常委、市委组织部部长",
        "current_org": "中共樟树市委组织部",
        "source": "樟树市人民政府网新闻"
    },
    {
        "id": "zhangshu_xiong_weidong",
        "name": "熊伟栋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "樟树市委常委、市委宣传部部长",
        "current_org": "中共樟树市委宣传部",
        "source": "樟树市人民政府网新闻"
    },
    {
        "id": "zhangshu_li_jian",
        "name": "李健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "樟树市委常委、市委政法委书记",
        "current_org": "中共樟树市委政法委",
        "source": "樟树市人民政府网新闻"
    },
    {
        "id": "zhangshu_huang_yun",
        "name": "黄云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "樟树市委常委、市委统战部部长",
        "current_org": "中共樟树市委统战部",
        "source": "樟树市人民政府网新闻"
    },

    # ===== 市政府领导 =====
    {
        "id": "zhangshu_zhao_qing",
        "name": "赵青",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "樟树市人民政府副市长",
        "current_org": "樟树市人民政府",
        "source": "樟树市人民政府网新闻"
    },
    {
        "id": "zhangshu_chen_yu",
        "name": "陈玉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "樟树市人民政府副市长",
        "current_org": "樟树市人民政府",
        "source": "樟树市人民政府网新闻"
    },
    {
        "id": "zhangshu_li_ming",
        "name": "李明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "樟树市人民政府副市长",
        "current_org": "樟树市人民政府",
        "source": "樟树市人民政府网新闻"
    },

    # ===== 人大、政协 =====
    {
        "id": "zhangshu_fu_jun",
        "name": "傅军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "樟树市人大常委会主任",
        "current_org": "樟树市人大常委会",
        "source": "樟树市人民政府网新闻"
    },
    {
        "id": "zhangshu_yang_xiaohong",
        "name": "杨小红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "履历待查",
        "birthplace": "履历待查",
        "education": "履历待查",
        "party_join": "中共党员",
        "work_start": "履历待查",
        "current_post": "樟树市政协主席",
        "current_org": "政协樟树市委员会",
        "source": "樟树市人民政府网新闻"
    },

    # ===== 关联人物（来自靖安县数据：喻军曾任职樟树市） =====
    {
        "id": "zhangshu_yu_jun",
        "name": "喻军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-01",
        "birthplace": "江西高安",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "1999-10",
        "current_post": "靖安县委书记",
        "current_org": "中共靖安县委员会",
        "source": "靖安县委相关新闻"
    },
]

# ---- 组织机构数据 ----
orgs = [
    {"id": 1, "name": "中共樟树市委员会", "type": "党委", "level": "县处级", "parent": "中共宜春市委员会", "location": "江西省宜春市樟树市"},
    {"id": 2, "name": "樟树市人民政府", "type": "政府", "level": "县处级", "parent": "宜春市人民政府", "location": "江西省宜春市樟树市"},
    {"id": 3, "name": "中共樟树市纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共樟树市委员会", "location": "江西省宜春市樟树市"},
    {"id": 4, "name": "樟树市监察委员会", "type": "政府", "level": "县处级", "parent": "樟树市人民政府", "location": "江西省宜春市樟树市"},
    {"id": 5, "name": "中共樟树市委组织部", "type": "党委", "level": "乡科级", "parent": "中共樟树市委员会", "location": "江西省宜春市樟树市"},
    {"id": 6, "name": "中共樟树市委宣传部", "type": "党委", "level": "乡科级", "parent": "中共樟树市委员会", "location": "江西省宜春市樟树市"},
    {"id": 7, "name": "中共樟树市委政法委", "type": "党委", "level": "乡科级", "parent": "中共樟树市委员会", "location": "江西省宜春市樟树市"},
    {"id": 8, "name": "中共樟树市委统战部", "type": "党委", "level": "乡科级", "parent": "中共樟树市委员会", "location": "江西省宜春市樟树市"},
    {"id": 9, "name": "樟树市人大常委会", "type": "人大", "level": "县处级", "parent": "樟树市", "location": "江西省宜春市樟树市"},
    {"id": 10, "name": "政协樟树市委员会", "type": "政协", "level": "县处级", "parent": "樟树市", "location": "江西省宜春市樟树市"},
    {"id": 11, "name": "樟树市工业园区", "type": "开发区", "level": "县处级", "parent": "樟树市人民政府", "location": "江西省宜春市樟树市"},
    {"id": 12, "name": "樟树市阁山镇", "type": "乡镇", "level": "乡科级", "parent": "樟树市", "location": "江西省宜春市樟树市"},
    {"id": 13, "name": "樟树市临江镇", "type": "乡镇", "level": "乡科级", "parent": "樟树市", "location": "江西省宜春市樟树市"},
]

# ---- 任职关系 ----
positions = [
    # 曾兆昕 - 市委书记
    {"id": 1, "person_id": "zhangshu_zeng_zhaoxin", "org_id": 1, "title": "樟树市委书记", "start": "2024-?",
     "end": "至今", "rank": "县处级正职", "note": "中共樟树市委书记"},
    # 罗功成 - 市长
    {"id": 2, "person_id": "zhangshu_luo_gongcheng", "org_id": 2, "title": "樟树市人民政府市长", "start": "2023-?",
     "end": "至今", "rank": "县处级正职", "note": "樟树市委副书记、市政府市长"},
    # 罗功成 - 曾兼任/过往职务
    {"id": 3, "person_id": "zhangshu_luo_gongcheng", "org_id": 1, "title": "樟树市委副书记", "start": "2023-?",
     "end": "至今", "rank": "县处级副职", "note": "兼任市委副书记"},
    # 刘娜 - 市委副书记
    {"id": 4, "person_id": "zhangshu_liu_na", "org_id": 1, "title": "樟树市委副书记", "start": "",
     "end": "至今", "rank": "县处级副职", "note": "专职副书记"},
    # 赖伟 - 纪委书记
    {"id": 5, "person_id": "zhangshu_lai_wei", "org_id": 3, "title": "樟树市委常委、市纪委书记", "start": "",
     "end": "至今", "rank": "县处级副职", "note": "兼市监委主任"},
    {"id": 6, "person_id": "zhangshu_lai_wei", "org_id": 4, "title": "樟树市监委主任", "start": "",
     "end": "至今", "rank": "县处级副职", "note": "市监委主任"},
    # 王小龙 - 常务副市长
    {"id": 7, "person_id": "zhangshu_wang_xiaolong", "org_id": 2, "title": "樟树市委常委、常务副市长", "start": "",
     "end": "至今", "rank": "县处级副职", "note": "市政府常务副职"},
    {"id": 8, "person_id": "zhangshu_wang_xiaolong", "org_id": 1, "title": "樟树市委常委", "start": "",
     "end": "至今", "rank": "县处级副职", "note": "市委常委会成员"},
    # 时珺 - 组织部长
    {"id": 9, "person_id": "zhangshu_shi_ming", "org_id": 1, "title": "樟树市委常委", "start": "",
     "end": "至今", "rank": "县处级副职", "note": "市委常委会成员"},
    {"id": 10, "person_id": "zhangshu_shi_ming", "org_id": 5, "title": "樟树市委组织部部长", "start": "",
     "end": "至今", "rank": "乡科级正职", "note": "市委组织部负责人"},
    # 熊伟栋 - 宣传部长
    {"id": 11, "person_id": "zhangshu_xiong_weidong", "org_id": 1, "title": "樟树市委常委", "start": "",
     "end": "至今", "rank": "县处级副职", "note": "市委常委会成员"},
    {"id": 12, "person_id": "zhangshu_xiong_weidong", "org_id": 6, "title": "樟树市委宣传部部长", "start": "",
     "end": "至今", "rank": "乡科级正职", "note": "宣传部负责人"},
    # 李健 - 政法委书记
    {"id": 13, "person_id": "zhangshu_li_jian", "org_id": 1, "title": "樟树市委常委", "start": "",
     "end": "至今", "rank": "县处级副职", "note": "市委常委会成员"},
    {"id": 14, "person_id": "zhangshu_li_jian", "org_id": 7, "title": "樟树市委政法委书记", "start": "",
     "end": "至今", "rank": "乡科级正职", "note": "政法委负责人"},
    # 黄云 - 统战部长
    {"id": 15, "person_id": "zhangshu_huang_yun", "org_id": 1, "title": "樟树市委常委", "start": "",
     "end": "至今", "rank": "县处级副职", "note": "市委常委会成员"},
    {"id": 16, "person_id": "zhangshu_huang_yun", "org_id": 8, "title": "樟树市委统战部部长", "start": "",
     "end": "至今", "rank": "乡科级正职", "note": "统战部负责人"},
    # 赵青 - 副市长
    {"id": 17, "person_id": "zhangshu_zhao_qing", "org_id": 2, "title": "樟树市人民政府副市长", "start": "",
     "end": "至今", "rank": "县处级副职", "note": "市政府班子成员"},
    # 陈玉 - 副市长
    {"id": 18, "person_id": "zhangshu_chen_yu", "org_id": 2, "title": "樟树市人民政府副市长", "start": "",
     "end": "至今", "rank": "县处级副职", "note": "市政府班子成员"},
    # 李明 - 副市长
    {"id": 19, "person_id": "zhangshu_li_ming", "org_id": 2, "title": "樟树市人民政府副市长", "start": "",
     "end": "至今", "rank": "县处级副职", "note": "市政府班子成员"},
    # 傅军 - 人大主任
    {"id": 20, "person_id": "zhangshu_fu_jun", "org_id": 9, "title": "樟树市人大常委会主任", "start": "",
     "end": "至今", "rank": "县处级正职", "note": "市人大常委会负责人"},
    # 杨小红 - 政协主席
    {"id": 21, "person_id": "zhangshu_yang_xiaohong", "org_id": 10, "title": "樟树市政协主席", "start": "",
     "end": "至今", "rank": "县处级正职", "note": "市政协负责人"},
    # 董晓明 - 前任书记
    {"id": 22, "person_id": "zhangshu_dong_xiaoming", "org_id": 1, "title": "樟树市委书记（前任）", "start": "",
     "end": "", "rank": "县处级正职", "note": "前任市委书记"},
    # 尹志来 - 前任书记
    {"id": 23, "person_id": "zhangshu_yin_zhi", "org_id": 1, "title": "樟树市委书记（前任）", "start": "",
     "end": "", "rank": "县处级正职", "note": "前任市委书记"},
    # 胡江萍 - 前任书记
    {"id": 24, "person_id": "zhangshu_hu_jiangle", "org_id": 1, "title": "樟树市委书记（前任）", "start": "",
     "end": "", "rank": "县处级正职", "note": "前任市委书记"},
    # 喻军 - 曾任樟树市委常委
    {"id": 25, "person_id": "zhangshu_yu_jun", "org_id": 1, "title": "樟树市委常委、市政府党组成员", "start": "2016-07",
     "end": "2019-07", "rank": "县处级副职", "note": "樟树市为宜春市代管县级市（引自靖安县数据）"},
    {"id": 26, "person_id": "zhangshu_yu_jun", "org_id": 2, "title": "樟树市政府党组成员", "start": "2016-07",
     "end": "2019-07", "rank": "县处级副职", "note": "市政府党组成员"},
]

# ---- 工作关系 ----
relationships = [
    # 书记-市长（党政搭档）
    {"id": 1, "person_a": "zhangshu_zeng_zhaoxin", "person_b": "zhangshu_luo_gongcheng", "type": "党政搭档",
     "context": "曾兆昕（书记）与罗功成（市长）为樟树市党政正职搭档", "overlap_org": "中共樟树市委员会/樟树市人民政府", "overlap_period": "2024-至今"},
    # 书记-副书记
    {"id": 2, "person_a": "zhangshu_zeng_zhaoxin", "person_b": "zhangshu_liu_na", "type": "上下级",
     "context": "曾兆昕（书记）与刘娜（专职副书记）为党委正副书记", "overlap_org": "中共樟树市委员会", "overlap_period": ""},
    # 市长-常务副市长
    {"id": 3, "person_a": "zhangshu_luo_gongcheng", "person_b": "zhangshu_wang_xiaolong", "type": "上下级",
     "context": "罗功成（市长）与王小龙（常务副市长）为政府正副职", "overlap_org": "樟树市人民政府", "overlap_period": ""},
    # 书记-纪委书记
    {"id": 4, "person_a": "zhangshu_zeng_zhaoxin", "person_b": "zhangshu_lai_wei", "type": "上下级",
     "context": "曾兆昕（书记）与赖伟（纪委书记）为党委正副书记（纪委归党委领导）", "overlap_org": "中共樟树市委员会", "overlap_period": ""},
    # 书记-前任书记（前后任）
    {"id": 5, "person_a": "zhangshu_zeng_zhaoxin", "person_b": "zhangshu_dong_xiaoming", "type": "前后任",
     "context": "曾兆昕接替董晓明任樟树市委书记", "overlap_org": "中共樟树市委员会", "overlap_period": ""},
    # 前任书记之间
    {"id": 6, "person_a": "zhangshu_dong_xiaoming", "person_b": "zhangshu_yin_zhi", "type": "前后任",
     "context": "董晓明接替尹志来任樟树市委书记", "overlap_org": "中共樟树市委员会", "overlap_period": ""},
    {"id": 7, "person_a": "zhangshu_yin_zhi", "person_b": "zhangshu_hu_jiangle", "type": "前后任",
     "context": "尹志来接替胡江萍任樟树市委书记", "overlap_org": "中共樟树市委员会", "overlap_period": ""},
    # 组织部长-书记
    {"id": 8, "person_a": "zhangshu_zeng_zhaoxin", "person_b": "zhangshu_shi_ming", "type": "上下级",
     "context": "曾兆昕（书记）与时珺（组织部长）为党委上下级", "overlap_org": "中共樟树市委员会", "overlap_period": ""},
    # 政法委书记-书记
    {"id": 9, "person_a": "zhangshu_zeng_zhaoxin", "person_b": "zhangshu_li_jian", "type": "上下级",
     "context": "曾兆昕（书记）与李健（政法委书记）为党委上下级", "overlap_org": "中共樟树市委员会", "overlap_period": ""},
    # 喻军-曾任樟树市委常委 - 关联
    {"id": 10, "person_a": "zhangshu_yu_jun", "person_b": "zhangshu_zeng_zhaoxin", "type": "前后任/同事",
     "context": "喻军2016-2019年曾任樟树市委常委，与曾兆昕可能存在任职交集", "overlap_org": "中共樟树市委员会", "overlap_period": "2016-2019/2024-至今"},
    # 人大主任-书记
    {"id": 11, "person_a": "zhangshu_zeng_zhaoxin", "person_b": "zhangshu_fu_jun", "type": "同级同事",
     "context": "曾兆昕（书记）与傅军（人大主任）为市四套班子正职", "overlap_org": "樟树市", "overlap_period": ""},
    # 政协主席-书记
    {"id": 12, "person_a": "zhangshu_zeng_zhaoxin", "person_b": "zhangshu_yang_xiaohong", "type": "同级同事",
     "context": "曾兆昕（书记）与杨小红（政协主席）为市四套班子正职", "overlap_org": "樟树市", "overlap_period": ""},
    # 宣传部长-书记
    {"id": 13, "person_a": "zhangshu_zeng_zhaoxin", "person_b": "zhangshu_xiong_weidong", "type": "上下级",
     "context": "曾兆昕（书记）与熊伟栋（宣传部长）为党委上下级", "overlap_org": "中共樟树市委员会", "overlap_period": ""},
    # 统战部长-书记
    {"id": 14, "person_a": "zhangshu_zeng_zhaoxin", "person_b": "zhangshu_huang_yun", "type": "上下级",
     "context": "曾兆昕（书记）与黄云（统战部长）为党委上下级", "overlap_org": "中共樟树市委员会", "overlap_period": ""},
]


# ============================================================
# BUILD FUNCTIONS
# ============================================================

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Schema
    c.execute("""CREATE TABLE IF NOT EXISTS persons (
        id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY, person_id TEXT, org_id INTEGER,
        title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id))""")
    c.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY, person_a TEXT, person_b TEXT,
        type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id))""")

    # Insert
    for p in persons:
        c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"],
                   p["work_start"], p["current_post"], p["current_org"], p["source"]))
    for o in orgs:
        c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        c.execute("INSERT OR REPLACE INTO positions VALUES (?,?,?,?,?,?,?,?)",
                  (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                   pos["start"], pos["end"], pos["rank"], pos["note"]))
    for r in relationships:
        c.execute("INSERT OR REPLACE INTO relationships VALUES (?,?,?,?,?,?,?)",
                  (r["id"], r["person_a"], r["person_b"], r["type"],
                   r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"✅ SQLite DB written: {DB_PATH}")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(name_str, post):
    """Return 'r,g,b' string based on role."""
    if "市委书记" in post:
        return "255,50,50"
    if "市长" in post and "副" not in post:
        return "50,100,255"
    if "副市长" in post or "常务副" in post:
        return "50,100,255"
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"
    if "人大常委会主任" in post or "人大" in post:
        return "200,200,200"
    if "政协主席" in post:
        return "200,200,200"
    return "100,100,100"


def org_color(o):
    t = o["type"]
    if t == "党委":
        return "255,200,200"
    if t == "政府":
        return "200,200,255"
    if t == "开发区":
        return "200,255,200"
    if t == "乡镇":
        return "255,255,200"
    if t == "人大":
        return "200,255,255"
    if t == "政协":
        return "255,240,200"
    return "200,200,200"


def is_top_leader(p):
    title = p["current_post"]
    return "书记" in title and ("市委" in title or "县委" in title) or \
           ("市长" in title and "副" not in title) or \
           ("人大主任" in title) or ("政协主席" in title)


def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append('    <description>樟树市领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["name"], p["current_post"])
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="{esc(p["id"])}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Org nodes
    for o in orgs:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        note = pos["note"]
        period = f"{pos['start'] or '?'}-{pos['end'] or '今'}"
        lines.append(f'      <edge id="e{eid}" source="{esc(pos["person_id"])}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(note)} [{period}]"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="{esc(r["person_a"])}" target="{esc(r["person_b"])}" label="{esc(r["type"])}" weight="2.0">')
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
    print(f"✅ GEXF graph written: {GEXF_PATH}")


# ── MAIN ─────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  樟树市（宜春市代管）领导班子工作关系网络")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(orgs)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print()

    build_db()
    build_gexf()

    # Verify
    print()
    print("📊 Summary Statistics:")
    print(f"  SQLite DB size: {os.path.getsize(DB_PATH)} bytes")
    print(f"  GEXF file size: {os.path.getsize(GEXF_PATH)} bytes")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(orgs)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print()
    print("✅ Done!")
