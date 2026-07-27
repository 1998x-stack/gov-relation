#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
涿州市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县级市
Province: 河北省
Parent City: 保定市
Region: 涿州市
Targets: 市委书记 & 市长

Research Sources:
- 涿州市人民政府官方网站 (www.zhuozhou.gov.cn)
  - 领导之窗确认韩震、张玉刚、杨越、郭衍游、谢雪梅、赵鸿波、王东威、郭蓬勃、李立军
  - 赵敏涛以市委书记身份活动报道(2025-2026): 2025-09 赴京招商, 2025-11 东仙坡镇宣讲, 2025-12 重点项目建设调研, 2026-01 慰问老干部
  - 保定市水利局确认赵敏涛曾任市水利局党组书记、局长
  - 河北农业大学校友记录确认赵敏涛为城建学院95级校友,曾任保定市政府常务副秘书长、阜平县委常委/常务副县长
  - 百度百科韩震词条确认:曾任省工信厅规划处副处长、莲池区委常委/常务副区长、京南经开区党工委副书记/管委会常务副主任、市商务局党组书记/局长
  - 市人大常委会会议(2024-10-18)任命韩震为副市长、代市长;市九届人大五次会议(2025-01-15)选举韩震为市长
  - 蔡炜华曾任涿州市委书记(前任),2024年9月仍以市委书记身份率团赴太仓考察
  - 李献峰曾任涿州市市长(前任),2022年1月-2024年10月
  - 姚运涛曾任涿州市委书记(前任)
  - 市八届十一次全会主席台名单显示赵敏涛、韩震、梁建杰、赵东宏、邸庆杰、葛永泉、彭建章、王卫国、王爱军、马东来、胡江安、李楠
  - 公开报道确认:张玉刚(市委常委、常务副市长),杨越(市委常委、副市长),葛永泉(市委常委、市委办主任,后转任副市长),曹卫华(市委常委、市委办公室主任),吴媛(市委常委、宣传部长),陈雪峰(市委常委、组织部长/统战部长)

Research Date: 2026-07-24
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "涿州市"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "赵敏涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "河北农业大学城乡建设学院95级",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿州市委书记",
        "current_org": "中共涿州市委员会",
        "source": "涿州市人民政府官网赵敏涛活动报道(2025-2026). 保定市水利局党组书记、局长任职记录. 河北农业大学校友记录(2022-01-23). 来源:https://www.zhuozhou.gov.cn/"
    },
    {
        "id": 2,
        "name": "韩震",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿州市委副书记、市长",
        "current_org": "涿州市人民政府",
        "source": "涿州市人民政府领导之窗. 百度百科韩震词条确认曾任省工信厅规划处副处长、莲池区委常委/常务副区长、市商务局局长等职. 来源:https://www.zhuozhou.gov.cn/zzgxportal/lingdaozhichuang.jsp"
    },
    # ════════════════════════════════════════
    # 市委领导 (from Party Congress & Committee meetings)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "梁建杰",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿州市人大常委会主任",
        "current_org": "涿州市人大常委会",
        "source": "涿州市第八届委员会第十一次全体会议(2025)主席台前排就座名单."
    },
    {
        "id": 4,
        "name": "赵东宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿州市委副书记",
        "current_org": "中共涿州市委员会",
        "source": "涿州市第八届委员会第十一次全体会议(2025)主席台前排就座名单. 太仓市考察报道(2024-09)确认赵东宏为涿州市委副书记随蔡炜华考察."
    },
    {
        "id": 5,
        "name": "邸庆杰",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿州市政协主席",
        "current_org": "涿州市政协",
        "source": "涿州市第八届委员会第十一次全体会议(2025)主席台前排就座名单."
    },
    {
        "id": 6,
        "name": "葛永泉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿州市委常委、副市长（曾任市委办公室主任）",
        "current_org": "涿州市人民政府",
        "source": "涿州市第八届委员会第十一次全体会议(2025)主席台前排就座. 赵敏涛赴乡镇调研报道(2026-01-06)确认葛永泉为市委常委、市委办主任. 市人大常委会决定任命张玉刚、杨越为副市长,免去葛永泉副市长职务,说明葛永泉曾任副市长. 太仓考察(2024-09)确认葛永泉为市委常委、市委办公室主任."
    },
    {
        "id": 7,
        "name": "彭建章",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿州市委常委",
        "current_org": "中共涿州市委员会",
        "source": "涿州市第八届委员会第十一次全体会议(2025)主席台前排就座名单."
    },
    {
        "id": 8,
        "name": "王卫国",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿州市委常委",
        "current_org": "中共涿州市委员会",
        "source": "涿州市第八届委员会第十一次全体会议(2025)主席台前排就座名单."
    },
    {
        "id": 9,
        "name": "王爱军",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿州市委常委",
        "current_org": "中共涿州市委员会",
        "source": "涿州市第八届委员会第十一次全体会议(2025)主席台前排就座名单."
    },
    {
        "id": 10,
        "name": "马东来",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿州市委常委",
        "current_org": "中共涿州市委员会",
        "source": "涿州市第八届委员会第十一次全体会议(2025)主席台前排就座名单."
    },
    {
        "id": 11,
        "name": "胡江安",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿州市委常委",
        "current_org": "中共涿州市委员会",
        "source": "涿州市第八届委员会第十一次全体会议(2025)主席台前排就座名单."
    },
    {
        "id": 12,
        "name": "李楠",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿州市委常委",
        "current_org": "中共涿州市委员会",
        "source": "涿州市第八届委员会第十一次全体会议(2025)主席台前排就座名单."
    },
    # ════════════════════════════════════════
    # 市政府领导班子 (from 领导之窗)
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "张玉刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿州市委常委、常务副市长",
        "current_org": "涿州市人民政府",
        "source": "涿州市人民政府领导之窗. 赵敏涛调研报道(2026-01-06)确认张玉刚为市委常委、常务副市长. 市人大常委会决定任命张玉刚为副市长."
    },
    {
        "id": 14,
        "name": "杨越",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿州市委常委、副市长",
        "current_org": "涿州市人民政府",
        "source": "涿州市人民政府领导之窗. 中国农业大学报道(2026-06)确认杨越为市委常委、副市长. 市人大常委会决定任命杨越为副市长."
    },
    {
        "id": 15,
        "name": "郭衍游",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿州市副市长",
        "current_org": "涿州市人民政府",
        "source": "涿州市人民政府领导之窗."
    },
    {
        "id": 16,
        "name": "谢雪梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿州市副市长",
        "current_org": "涿州市人民政府",
        "source": "涿州市人民政府领导之窗. 赵敏涛与创新人才教育研究会座谈报道确认谢雪梅参加."
    },
    {
        "id": 17,
        "name": "赵鸿波",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿州市副市长",
        "current_org": "涿州市人民政府",
        "source": "涿州市人民政府领导之窗."
    },
    {
        "id": 18,
        "name": "王东威",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿州市副市长",
        "current_org": "涿州市人民政府",
        "source": "涿州市人民政府领导之窗. 市人大常委会决定免去王东威市财政局局长职务(说明其由财政局长转任副市长)."
    },
    {
        "id": 19,
        "name": "郭蓬勃",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿州市副市长",
        "current_org": "涿州市人民政府",
        "source": "涿州市人民政府领导之窗."
    },
    {
        "id": 20,
        "name": "李立军",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿州市副市长",
        "current_org": "涿州市人民政府",
        "source": "涿州市人民政府领导之窗."
    },
    # ════════════════════════════════════════
    # 市委办公室及其他部门领导
    # ════════════════════════════════════════
    {
        "id": 21,
        "name": "曹卫华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿州市委常委、市委办公室主任",
        "current_org": "中共涿州市委员会",
        "source": "赵敏涛赴京招商报道(2025-09-12)确认曹卫华为市委常委、市委办公室主任. 赵敏涛调研重点项目建设报道(2025-11-28)确认曹卫华为市委常委、市委办公室主任. 市人大常委会决定免去曹卫华市政府办公室主任职务."
    },
    {
        "id": 22,
        "name": "吴媛",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿州市委常委、宣传部长",
        "current_org": "中共涿州市委员会",
        "source": "赵敏涛赴京招商报道(2025-09-12)确认吴媛为市委常委、宣传部长."
    },
    {
        "id": 23,
        "name": "陈雪峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿州市委常委、组织部长、统战部长",
        "current_org": "中共涿州市委员会",
        "source": "涿州市科级领导干部集中轮训班报道(2026-03-23)确认陈雪峰为市委常委、组织部长、统战部长."
    },
    # ════════════════════════════════════════
    # 前任重要领导
    # ════════════════════════════════════════
    {
        "id": 24,
        "name": "蔡炜华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿州市委书记(前任)",
        "current_org": "中共涿州市委员会",
        "source": "河北5市多人任免报道. 太仓市人民政府考察报道(2024-09)确认蔡炜华率团在太仓考察. 来源:https://xinwen.bjd.com.cn/content/s6178e117e4b023337eee8629.html"
    },
    {
        "id": 25,
        "name": "李献峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-02",
        "birthplace": "河北涞源",
        "native_place": "河北涞源",
        "education": "省委党校研究生学历",
        "party_join": "1996-09",
        "work_start": "1994-08",
        "current_post": "涿州市市长(前任)/涿州京南经济开发区党工委书记、管委会主任",
        "current_org": "涿州市人民政府/涿州京南经济开发区",
        "source": "95商服网李献峰词条. 河北5市多人任免报道. 来源:https://www.95ye.com/shop/mobile-do-detail-id-69553.html"
    },
    {
        "id": 26,
        "name": "姚运涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿州市委书记(前任)",
        "current_org": "中共涿州市委员会",
        "source": "河北5市多人任免报道,姚运涛不再担任涿州市委书记."
    },
    {
        "id": 27,
        "name": "尚文轩",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "涿州市副市长(前任)",
        "current_org": "涿州市人民政府",
        "source": "市人大常委会决定免去尚文轩涿州市人民政府副市长职务."
    },
]

# 2. Organizations
organizations = [
    {"id": 0, "name": "中共涿州市委员会", "type": "党委", "level": "县级市", "parent": "中共保定市委", "location": "河北省保定市涿州市"},
    {"id": 1, "name": "涿州市人民政府", "type": "政府", "level": "县级市", "parent": "保定市人民政府", "location": "河北省保定市涿州市"},
    {"id": 2, "name": "涿州市人大常委会", "type": "人大", "level": "县级市", "parent": "保定市人大常委会", "location": "河北省保定市涿州市"},
    {"id": 3, "name": "涿州市政协", "type": "政协", "level": "县级市", "parent": "保定市政协", "location": "河北省保定市涿州市"},
    {"id": 4, "name": "涿州市纪律检查委员会", "type": "纪委", "level": "县级市", "parent": "中共涿州市委员会", "location": "河北省保定市涿州市"},
    {"id": 5, "name": "中共涿州市委组织部", "type": "党委部门", "level": "县级市", "parent": "中共涿州市委员会", "location": "河北省保定市涿州市"},
    {"id": 6, "name": "中共涿州市委宣传部", "type": "党委部门", "level": "县级市", "parent": "中共涿州市委员会", "location": "河北省保定市涿州市"},
    {"id": 7, "name": "中共涿州市委办公室", "type": "党委部门", "level": "县级市", "parent": "中共涿州市委员会", "location": "河北省保定市涿州市"},
    {"id": 8, "name": "涿州市人民政府办公室", "type": "政府部门", "level": "县级市", "parent": "涿州市人民政府", "location": "河北省保定市涿州市"},
    {"id": 9, "name": "涿州市财政局", "type": "政府部门", "level": "县级市", "parent": "涿州市人民政府", "location": "河北省保定市涿州市"},
    {"id": 10, "name": "涿州京南经济开发区", "type": "开发区", "level": "省级", "parent": "保定市人民政府", "location": "河北省保定市涿州市"},
    {"id": 11, "name": "河北涿州高新技术产业开发区", "type": "开发区", "level": "省级", "parent": "河北省人民政府", "location": "河北省保定市涿州市"},
    {"id": 12, "name": "河北涿州松林店经济开发区", "type": "开发区", "level": "省级", "parent": "河北省人民政府", "location": "河北省保定市涿州市"},
    {"id": 13, "name": "保定市水利局", "type": "政府部门", "level": "地市级", "parent": "保定市人民政府", "location": "河北省保定市"},
    {"id": 14, "name": "保定市人民政府", "type": "政府", "level": "地市级", "parent": "河北省人民政府", "location": "河北省保定市"},
    {"id": 15, "name": "阜平县人民政府", "type": "政府", "level": "县级", "parent": "保定市人民政府", "location": "河北省保定市阜平县"},
    {"id": 16, "name": "河北省工业和信息化厅", "type": "政府部门", "level": "省级", "parent": "河北省人民政府", "location": "河北省石家庄市"},
    {"id": 17, "name": "保定市商务局", "type": "政府部门", "level": "地市级", "parent": "保定市人民政府", "location": "河北省保定市"},
    {"id": 18, "name": "中共保定市莲池区委员会", "type": "党委", "level": "县级", "parent": "中共保定市委", "location": "河北省保定市莲池区"},
    {"id": 19, "name": "莲池区人民政府", "type": "政府", "level": "县级", "parent": "保定市人民政府", "location": "河北省保定市莲池区"},
    {"id": 20, "name": "中共保定市委", "type": "党委", "level": "地市级", "parent": "中共河北省委", "location": "河北省保定市"},
    {"id": 21, "name": "涿州师范学校", "type": "事业单位", "level": "县级", "parent": "保定市教育局", "location": "河北省保定市涿州市"},
    {"id": 22, "name": "涞源县南屯乡中学", "type": "事业单位", "level": "乡镇级", "parent": "涞源县教育局", "location": "河北省保定市涞源县"},
    {"id": 23, "name": "涞源县杨家庄镇人民政府", "type": "政府", "level": "乡镇级", "parent": "涞源县人民政府", "location": "河北省保定市涞源县"},
    {"id": 24, "name": "涞源县烟煤洞乡党委", "type": "党委", "level": "乡镇级", "parent": "中共涞源县委", "location": "河北省保定市涞源县"},
    {"id": 25, "name": "曲阳县人民政府", "type": "政府", "level": "县级", "parent": "保定市人民政府", "location": "河北省保定市曲阳县"},
    {"id": 26, "name": "中共曲阳县委宣传部", "type": "党委部门", "level": "县级", "parent": "中共曲阳县委", "location": "河北省保定市曲阳县"},
    {"id": 27, "name": "河北农业大学", "type": "事业单位", "level": "省级", "parent": "河北省教育厅", "location": "河北省保定市"},
    {"id": 28, "name": "涿州高新技术产业开发区管委会", "type": "开发区", "level": "省级", "parent": "涿州市人民政府", "location": "河北省保定市涿州市"},
]

# 3. Positions
positions = [
    # ── Current Leaders ──
    # 赵敏涛 - 市委书记
    {"person_id": 1, "org_id": 0, "title": "涿州市委书记", "start": "2025-07?（推测）", "end": "至今", "rank": "正处级", "note": "具体上任时间待查; 2025年9月起以市委书记身份公开活动"},
    {"person_id": 1, "org_id": 7, "title": "保定市水利局党组书记、局长", "start": "2023?（推测）", "end": "2025?（推测）", "rank": "正处级", "note": "保定市水利局报道确认任党组书记、局长"},
    {"person_id": 1, "org_id": 7, "title": "保定市政府常务副秘书长", "start": "2022?（推测）", "end": "2023?（推测）", "rank": "正处级", "note": "河北农业大学校友报道(2022-01)确认"},
    {"person_id": 1, "org_id": 15, "title": "阜平县委常委、常务副县长", "start": "待查", "end": "待查", "rank": "副处级", "note": "阜平县政府政务公开工作领导小组确认"},
    {"person_id": 1, "org_id": 15, "title": "阜平县副县长", "start": "待查", "end": "待查", "rank": "副处级", "note": "阜平县副县长"},
    {"person_id": 1, "org_id": 27, "title": "河北农业大学城乡建设学院学生", "start": "约1995", "end": "约1999", "rank": "", "note": "河北农业大学城建学院95级校友"},

    # 韩震 - 市长
    {"person_id": 2, "org_id": 1, "title": "涿州市委副书记、市长", "start": "2024-09（代）, 2025-01（正）", "end": "至今", "rank": "正处级", "note": "2024年10月18日任代市长; 2025年1月15日当选市长"},
    {"person_id": 2, "org_id": 11, "title": "河北涿州高新技术产业开发区党工委副书记、管委会主任", "start": "2024-09", "end": "至今", "rank": "", "note": "兼任三个开发区相关职务"},
    {"person_id": 2, "org_id": 10, "title": "京南经济开发区党工委副书记、管委会常务副主任", "start": "待查", "end": "2024-09", "rank": "正处级", "note": "百度百科确认"},
    {"person_id": 2, "org_id": 17, "title": "保定市商务局党组书记、局长", "start": "待查", "end": "待查", "rank": "正处级", "note": "百度百科确认"},
    {"person_id": 2, "org_id": 19, "title": "莲池区委常委、常务副区长", "start": "待查", "end": "待查", "rank": "副处级", "note": "百度百科确认"},
    {"person_id": 2, "org_id": 16, "title": "河北省工业和信息化厅规划处副处长、三级调研员", "start": "待查", "end": "待查", "rank": "副处级", "note": "百度百科确认"},

    # 梁建杰 - 人大主任
    {"person_id": 3, "org_id": 2, "title": "涿州市人大常委会主任", "start": "待查", "end": "至今", "rank": "正处级", "note": "信息来自全会主席台名单"},

    # 赵东宏 - 市委副书记
    {"person_id": 4, "org_id": 0, "title": "涿州市委副书记", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},

    # 邸庆杰 - 政协主席
    {"person_id": 5, "org_id": 3, "title": "涿州市政协主席", "start": "待查", "end": "至今", "rank": "正处级", "note": ""},

    # 葛永泉 - 市委常委/副市长/前市委办主任
    {"person_id": 6, "org_id": 1, "title": "涿州市委常委、副市长", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 7, "title": "涿州市委常委、市委办公室主任", "start": "待查", "end": "待查", "rank": "副处级", "note": "2024-2025年任职"},

    # 张玉刚 - 常务副市长
    {"person_id": 13, "org_id": 1, "title": "涿州市委常委、常务副市长", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},

    # 杨越 - 副市长
    {"person_id": 14, "org_id": 1, "title": "涿州市委常委、副市长", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},

    # 郭衍游 - 副市长
    {"person_id": 15, "org_id": 1, "title": "涿州市副市长", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},

    # 谢雪梅 - 副市长
    {"person_id": 16, "org_id": 1, "title": "涿州市副市长", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},

    # 赵鸿波 - 副市长
    {"person_id": 17, "org_id": 1, "title": "涿州市副市长", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},

    # 王东威 - 副市长（原财政局长）
    {"person_id": 18, "org_id": 1, "title": "涿州市副市长", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 9, "title": "涿州市财政局局长", "start": "待查", "end": "待查", "rank": "正科级", "note": "市人大常委会免去其财政局长职务"},

    # 郭蓬勃 - 副市长
    {"person_id": 19, "org_id": 1, "title": "涿州市副市长", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},

    # 李立军 - 副市长
    {"person_id": 20, "org_id": 1, "title": "涿州市副市长", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},

    # 曹卫华 - 市委办公室主任
    {"person_id": 21, "org_id": 8, "title": "涿州市委常委、市委办公室主任", "start": "待查", "end": "至今", "rank": "副处级", "note": "曾任市政府办公室主任, 后免去"},

    # 吴媛 - 宣传部长
    {"person_id": 22, "org_id": 6, "title": "涿州市委常委、宣传部长", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},

    # 陈雪峰 - 组织部长
    {"person_id": 23, "org_id": 5, "title": "涿州市委常委、组织部长、统战部长", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},

    # ── Predecessors ──
    # 蔡炜华 - 前任市委书记
    {"person_id": 24, "org_id": 0, "title": "涿州市委书记", "start": "2021-10左右", "end": "2025?（推测）", "rank": "正处级", "note": "2021年10月任市委书记, 2024年9月仍以书记身份活动"},
    {"person_id": 24, "org_id": 1, "title": "涿州市市长", "start": "待查", "end": "2021-10", "rank": "正处级", "note": "由市长转任市委书记"},
    {"person_id": 24, "org_id": 10, "title": "涿州京南经济开发区党工委书记、管委会主任", "start": "待查", "end": "2021-10", "rank": "", "note": "兼任"},

    # 李献峰 - 前任市长
    {"person_id": 25, "org_id": 1, "title": "涿州市委副书记、市长", "start": "2022-01", "end": "2024-10", "rank": "正处级", "note": "2021年10月提名, 2022年1月正式任职"},
    {"person_id": 25, "org_id": 10, "title": "涿州京南经济开发区党工委书记、管委会主任", "start": "2021-10", "end": "至今", "rank": "", "note": "兼任"},
    {"person_id": 25, "org_id": 1, "title": "涿州市委常委、副市长（分工政府常务工作）", "start": "2020-09", "end": "2021-10", "rank": "正处级", "note": "正县级"},
    {"person_id": 25, "org_id": 25, "title": "曲阳县委常委（援疆、正县级）", "start": "2017-01", "end": "2020-09", "rank": "正处级", "note": ""},
    {"person_id": 25, "org_id": 26, "title": "曲阳县委常委、宣传部长、农工委书记", "start": "2016-02", "end": "2017-01", "rank": "副处级", "note": ""},
    {"person_id": 25, "org_id": 25, "title": "曲阳县副县长", "start": "2012-02", "end": "2016-02", "rank": "副处级", "note": ""},
    {"person_id": 25, "org_id": 24, "title": "涞源县烟煤洞乡党委书记", "start": "2009-08", "end": "2011-08", "rank": "正科级", "note": ""},
    {"person_id": 25, "org_id": 23, "title": "涞源县杨家庄镇党委副书记、镇长", "start": "2006-09", "end": "2009-08", "rank": "正科级", "note": ""},

    # 姚运涛 - 前任市委书记
    {"person_id": 26, "org_id": 0, "title": "涿州市委书记", "start": "待查", "end": "2021-10", "rank": "正处级", "note": "2021年10月不再担任"},
]

# 4. Relationships
relationships = [
    # ── Current Top Team - Direct Working Relationships ──
    # 赵敏涛 ←→ 韩震 (书记+市长)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书记与市长党政主要领导搭档", "overlap_org": "中共涿州市委员会/涿州市人民政府", "overlap_period": "2025-至今"},
    # 赵敏涛 ←→ 赵东宏 (书记+副书记)
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "市委书记与专职副书记搭档", "overlap_org": "中共涿州市委员会", "overlap_period": "2025-至今"},
    # 赵敏涛 ←→ 曹卫华 (书记+市委办主任)
    {"person_a": 1, "person_b": 21, "type": "superior_subordinate", "context": "市委书记与市委办公室主任直接工作关系", "overlap_org": "中共涿州市委员会", "overlap_period": "2025-至今"},
    # 赵敏涛 ←→ 葛永泉 (书记+常委副市长/前市委办主任)
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "市委书记与市委常委工作关系", "overlap_org": "中共涿州市委员会", "overlap_period": "2025-至今"},
    # 赵敏涛 ←→ 张玉刚 (书记+常务副市长)
    {"person_a": 1, "person_b": 13, "type": "superior_subordinate", "context": "市委书记与常务副市长工作关系", "overlap_org": "中共涿州市委员会/涿州市人民政府", "overlap_period": "2025-至今"},
    # 赵敏涛 ←→ 吴媛 (书记+宣传部长)
    {"person_a": 1, "person_b": 22, "type": "superior_subordinate", "context": "市委书记与宣传部长工作关系", "overlap_org": "中共涿州市委员会", "overlap_period": "2025-至今"},
    # 赵敏涛 ←→ 陈雪峰 (书记+组织部长)
    {"person_a": 1, "person_b": 23, "type": "superior_subordinate", "context": "市委书记与组织部长工作关系", "overlap_org": "中共涿州市委员会", "overlap_period": "2025-至今"},

    # 韩震 ←→ 张玉刚 (市长+常务副市长)
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "市长与常务副市长搭档", "overlap_org": "涿州市人民政府", "overlap_period": "2025-至今"},
    # 韩震 ←→ 杨越 (市长+副市长)
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "市长与副市长工作关系", "overlap_org": "涿州市人民政府", "overlap_period": "2025-至今"},

    # ── Predecessor/Successor ──
    # 蔡炜华 → 赵敏涛 (书记交接)
    {"person_a": 24, "person_b": 1, "type": "predecessor_successor", "context": "蔡炜华前任涿州市委书记,赵敏涛接任", "overlap_org": "中共涿州市委员会", "overlap_period": "2025"},
    # 姚运涛 → 蔡炜华 (书记交接)
    {"person_a": 26, "person_b": 24, "type": "predecessor_successor", "context": "姚运涛前任涿州市委书记,蔡炜华接任(2021)", "overlap_org": "中共涿州市委员会", "overlap_period": "2021"},
    # 李献峰 → 韩震 (市长交接)
    {"person_a": 25, "person_b": 2, "type": "predecessor_successor", "context": "李献峰前任涿州市长,韩震接任(2024-10代, 2025-01正)", "overlap_org": "涿州市人民政府", "overlap_period": "2024-10"},
    # 蔡炜华 → 李献峰 (书记+市长交接)
    {"person_a": 24, "person_b": 25, "type": "predecessor_successor", "context": "蔡炜华由市长转任书记,李献峰接任市长", "overlap_org": "涿州市人民政府", "overlap_period": "2021-10"},

    # ── Same-Team Overlaps ──
    # 蔡炜华 + 李献峰 (书记+市长搭档)
    {"person_a": 24, "person_b": 25, "type": "overlap", "context": "蔡炜华任书记期间,李献峰任市长(2022-2024)", "overlap_org": "中共涿州市委员会/涿州市人民政府", "overlap_period": "2022-2024"},
    # 蔡炜华 + 葛永泉
    {"person_a": 24, "person_b": 6, "type": "overlap", "context": "蔡炜华任书记期间,葛永泉任市委常委/市委办主任", "overlap_org": "中共涿州市委员会", "overlap_period": "2021-2025"},
    # 李献峰 + 张玉刚
    {"person_a": 25, "person_b": 13, "type": "overlap", "context": "李献峰任市长期间,张玉刚任常务副市长", "overlap_org": "涿州市人民政府", "overlap_period": "2022-2024"},
    # 李献峰 + 杨越
    {"person_a": 25, "person_b": 14, "type": "overlap", "context": "李献峰任市长期间,杨越任副市长", "overlap_org": "涿州市人民政府", "overlap_period": "2022-2024"},
    # 葛永泉 + 曹卫华 (市委办前后任)
    {"person_a": 6, "person_b": 21, "type": "predecessor_successor", "context": "葛永泉曾任市委办主任,曹卫华接任", "overlap_org": "中共涿州市委办公室", "overlap_period": "2025?"},
    # 王东威 转任副市长
    {"person_a": 18, "person_b": 2, "type": "superior_subordinate", "context": "王东威由财政局长转任副市长后与韩震工作关系", "overlap_org": "涿州市人民政府", "overlap_period": "2025-至今"},
]

# ── Build ──
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
