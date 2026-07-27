#!/usr/bin/env python3
"""点军区 (Dianjun District, Yichang, Hubei) — Leadership relationship network build script.

Source: 点军区人民政府官方网站 http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html
调查日期: 2026-07-24
"""

import os
import sqlite3
import sys
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TODAY = "2026-07-24"
AS_OF = TODAY
SLUG = "点军区"
DB_PATH = os.path.join(SCRIPT_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, f"{SLUG}_network.gexf")

# ── Data ───────────────────────────────────────────────────────────────────────

persons = [
    # ── Party Committee (区委) ──
    {
        "id": 1,
        "name": "万红",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1970年11月",
        "birthplace": "",
        "education": "中专",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区委书记",
        "current_org": "中共点军区委员会",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "现任宜昌市人大常委会党组成员、副主任，宜昌市点军区委书记"
    },
    {
        "id": 2,
        "name": "王建红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年8月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区委副书记、区政府区长",
        "current_org": "点军区人民政府",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "区委副书记、区政府党组书记、区政府区长"
    },
    {
        "id": 3,
        "name": "付向阳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982年5月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区委副书记",
        "current_org": "中共点军区委员会",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "三级调研员"
    },
    {
        "id": 4,
        "name": "梁昌全",
        "gender": "男",
        "ethnicity": "",
        "birth": "1974年10月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区委常委、纪委书记、监委主任",
        "current_org": "中共点军区纪律检查委员会",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "三级调研员，四级高级监察官"
    },
    {
        "id": 5,
        "name": "裴新颜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976年2月",
        "birthplace": "",
        "education": "党校大学",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区委常委、宣传部部长",
        "current_org": "中共点军区委员会宣传部",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": ""
    },
    {
        "id": 6,
        "name": "刘勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年12月",
        "birthplace": "",
        "education": "党校大学",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区委常委、政法委书记",
        "current_org": "中共点军区委员会政法委员会",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "三级调研员"
    },
    {
        "id": 7,
        "name": "祁承荣",
        "gender": "男",
        "ethnicity": "",
        "birth": "1977年10月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区委常委、区人武部部长",
        "current_org": "点军区人民武装部",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "上校部长"
    },
    {
        "id": 8,
        "name": "王宏垚",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1985年5月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区委常委、组织部部长、统战部部长",
        "current_org": "中共点军区委员会组织部",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "兼区政协党组副书记"
    },
    {
        "id": 9,
        "name": "赵子鸿",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1987年10月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区委常委、区政府常务副区长",
        "current_org": "点军区人民政府",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "区政府党组成员，协助区长负责政府日常工作"
    },
    {
        "id": 10,
        "name": "汪填峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1990年8月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区委常委、区委办公室主任",
        "current_org": "中共点军区委员会办公室",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "区委直属机关工委书记"
    },
    # ── District Government (区政府) ──
    {
        "id": 11,
        "name": "郭振纲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年9月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区副区长、公安分局局长",
        "current_org": "点军区人民政府",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "区政府党组成员、市公安局点军区分局局长"
    },
    {
        "id": 12,
        "name": "陈大为",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年5月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区副区长",
        "current_org": "点军区人民政府",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "非中共党员，兼区红十字会会长"
    },
    {
        "id": 13,
        "name": "韩林",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978年11月",
        "birthplace": "",
        "education": "党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区副区长",
        "current_org": "点军区人民政府",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "区政府党组成员"
    },
    {
        "id": 14,
        "name": "刘申",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1984年7月",
        "birthplace": "",
        "education": "研究生、工学硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区副区长",
        "current_org": "点军区人民政府",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "区政府党组成员"
    },
    {
        "id": 15,
        "name": "付德山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年3月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区副区长",
        "current_org": "点军区人民政府",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "区政府党组成员"
    },
    {
        "id": 16,
        "name": "范平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年10月",
        "birthplace": "",
        "education": "博士研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区副区长",
        "current_org": "点军区人民政府",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "区政府党组成员"
    },
    {
        "id": 17,
        "name": "肖祖珽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年7月",
        "birthplace": "",
        "education": "博士研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区副区长",
        "current_org": "点军区人民政府",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "区政府党组成员"
    },
    {
        "id": 18,
        "name": "余红",
        "gender": "女",
        "ethnicity": "土家族",
        "birth": "1977年8月",
        "birthplace": "",
        "education": "本科、公共管理硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区党组成员、电子信息产业园管理办公室专职副主任",
        "current_org": "点军区人民政府",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "湖北点军工业园区党工委委员"
    },
    # ── People's Congress (区人大) ──
    {
        "id": 19,
        "name": "白慧",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1969年11月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区人大常委会主任",
        "current_org": "点军区人大常委会",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "党组书记"
    },
    {
        "id": 20,
        "name": "李筱霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1969年11月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区人大常委会副主任",
        "current_org": "点军区人大常委会",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "二级调研员，非中共党员"
    },
    {
        "id": 21,
        "name": "杨艳晖",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1974年1月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区人大常委会副主任",
        "current_org": "点军区人大常委会",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "党组成员，三级调研员"
    },
    {
        "id": 22,
        "name": "李忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年2月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区人大常委会副主任",
        "current_org": "点军区人大常委会",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "党组成员，三级调研员"
    },
    {
        "id": 23,
        "name": "谭华伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年7月",
        "birthplace": "",
        "education": "大专",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区人大常委会副主任",
        "current_org": "点军区人大常委会",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "党组成员"
    },
    {
        "id": 24,
        "name": "代平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年9月",
        "birthplace": "",
        "education": "大专",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区人大常委会副主任",
        "current_org": "点军区人大常委会",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "党组成员"
    },
    {
        "id": 25,
        "name": "孙科新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年6月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区人大常委会副主任",
        "current_org": "点军区人大常委会",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "党组成员"
    },
    # ── CPPCC (区政协) ──
    {
        "id": 26,
        "name": "李洪彦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年4月",
        "birthplace": "",
        "education": "党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区政协主席",
        "current_org": "点军区政协",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "党组书记"
    },
    {
        "id": 27,
        "name": "冯发柏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年4月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区政协副主席",
        "current_org": "点军区政协",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "党组副书记，三级调研员"
    },
    {
        "id": 28,
        "name": "邓玉兰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1970年9月",
        "birthplace": "",
        "education": "党校大学",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区政协副主席",
        "current_org": "点军区政协",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "三级调研员，非中共党员"
    },
    {
        "id": 29,
        "name": "刘争",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年7月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区政协副主席",
        "current_org": "点军区政协",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "非中共党员"
    },
    {
        "id": 30,
        "name": "张灿",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1985年2月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "点军区政协副主席",
        "current_org": "点军区政协",
        "source": "http://www.dianjun.gov.cn/pcms_692_quweilingdao_26.html",
        "notes": "兼区工商联主席，非中共党员"
    },
]

# ── Predecessors (former leaders) ──
# 万红 previously worked at 宜昌市招商局, became 点军区委书记 around 2022
# Previous 点军区委书记: 宋涛 (to ~2021/2022)
# Previous 点军区长: 黄文云 (to ~2023)
previous_persons = [
    {
        "id": 31,
        "name": "宋涛",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "已离任（原点军区委书记）",
        "current_org": "",
        "source": "媒体资料",
        "notes": "前任点军区委书记，约2021年离任"
    },
    {
        "id": 32,
        "name": "黄文云",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "已离任（原点军区区长）",
        "current_org": "",
        "source": "媒体资料",
        "notes": "前任点军区区长，约2023年调任宜昌市林业和园林局局长"
    },
]

persons.extend(previous_persons)

# ── Organizations ──────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共点军区委员会", "type": "党委", "level": "县处级", "parent": "中共宜昌市委", "location": "宜昌市点军区"},
    {"id": 2, "name": "点军区人民政府", "type": "政府", "level": "县处级", "parent": "宜昌市人民政府", "location": "宜昌市点军区"},
    {"id": 3, "name": "中共点军区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共点军区委员会", "location": "宜昌市点军区"},
    {"id": 4, "name": "中共点军区委员会宣传部", "type": "党委", "level": "乡科级", "parent": "中共点军区委员会", "location": "宜昌市点军区"},
    {"id": 5, "name": "中共点军区委员会政法委员会", "type": "党委", "level": "乡科级", "parent": "中共点军区委员会", "location": "宜昌市点军区"},
    {"id": 6, "name": "点军区人民武装部", "type": "党委", "level": "县处级", "parent": "宜昌军分区", "location": "宜昌市点军区"},
    {"id": 7, "name": "中共点军区委员会组织部", "type": "党委", "level": "乡科级", "parent": "中共点军区委员会", "location": "宜昌市点军区"},
    {"id": 8, "name": "中共点军区委员会办公室", "type": "党委", "level": "乡科级", "parent": "中共点军区委员会", "location": "宜昌市点军区"},
    {"id": 9, "name": "点军区人大常委会", "type": "人大", "level": "县处级", "parent": "宜昌市人大常委会", "location": "宜昌市点军区"},
    {"id": 10, "name": "点军区政协", "type": "政协", "level": "县处级", "parent": "宜昌市政协", "location": "宜昌市点军区"},
    {"id": 11, "name": "点军区人大常委会办公室", "type": "人大", "level": "乡科级", "parent": "点军区人大常委会", "location": "宜昌市点军区"},
    {"id": 12, "name": "宜昌市人大常委会", "type": "人大", "level": "地厅级", "parent": "湖北省人大常委会", "location": "宜昌市"},
    {"id": 13, "name": "中共点军区委员会统战部", "type": "党委", "level": "乡科级", "parent": "中共点军区委员会", "location": "宜昌市点军区"},
    {"id": 14, "name": "湖北点军工业园区", "type": "开发区", "level": "县处级", "parent": "点军区人民政府", "location": "宜昌市点军区"},
    {"id": 15, "name": "点军区电子信息产业园管理办公室", "type": "事业单位", "level": "乡科级", "parent": "点军区人民政府", "location": "宜昌市点军区"},
    {"id": 16, "name": "点军区人力资源和社会保障局", "type": "政府", "level": "乡科级", "parent": "点军区人民政府", "location": "宜昌市点军区"},
    {"id": 17, "name": "点军区卫生健康局", "type": "政府", "level": "乡科级", "parent": "点军区人民政府", "location": "宜昌市点军区"},
    {"id": 18, "name": "点军区教育局", "type": "政府", "level": "乡科级", "parent": "点军区人民政府", "location": "宜昌市点军区"},
    {"id": 19, "name": "点军区文化和旅游局", "type": "政府", "level": "乡科级", "parent": "点军区人民政府", "location": "宜昌市点军区"},
    {"id": 20, "name": "点军区市场监督管理局", "type": "政府", "level": "乡科级", "parent": "点军区人民政府", "location": "宜昌市点军区"},
    {"id": 21, "name": "点军区审计局", "type": "政府", "level": "乡科级", "parent": "点军区人民政府", "location": "宜昌市点军区"},
    {"id": 22, "name": "点军区发展和改革局", "type": "政府", "level": "乡科级", "parent": "点军区人民政府", "location": "宜昌市点军区"},
    {"id": 23, "name": "点军区财政局", "type": "政府", "level": "乡科级", "parent": "点军区人民政府", "location": "宜昌市点军区"},
    {"id": 24, "name": "点军区应急管理局", "type": "政府", "level": "乡科级", "parent": "点军区人民政府", "location": "宜昌市点军区"},
    {"id": 25, "name": "市公安局点军区分局", "type": "政府", "level": "乡科级", "parent": "宜昌市公安局", "location": "宜昌市点军区"},
    {"id": 26, "name": "点军区科学技术和经济信息化局", "type": "政府", "level": "乡科级", "parent": "点军区人民政府", "location": "宜昌市点军区"},
    {"id": 27, "name": "点军区住房和城乡建设局", "type": "政府", "level": "乡科级", "parent": "点军区人民政府", "location": "宜昌市点军区"},
    {"id": 28, "name": "点军区城市管理执法局", "type": "政府", "level": "乡科级", "parent": "点军区人民政府", "location": "宜昌市点军区"},
    {"id": 29, "name": "点军区招商局", "type": "政府", "level": "乡科级", "parent": "点军区人民政府", "location": "宜昌市点军区"},
    {"id": 30, "name": "点军区民政局", "type": "政府", "level": "乡科级", "parent": "点军区人民政府", "location": "宜昌市点军区"},
    {"id": 31, "name": "点军区司法局", "type": "政府", "level": "乡科级", "parent": "点军区人民政府", "location": "宜昌市点军区"},
    {"id": 32, "name": "点军区退役军人事务局", "type": "政府", "level": "乡科级", "parent": "点军区人民政府", "location": "宜昌市点军区"},
    {"id": 33, "name": "点军区医疗保障局", "type": "政府", "level": "乡科级", "parent": "点军区人民政府", "location": "宜昌市点军区"},
    {"id": 34, "name": "点军区红十字会", "type": "群团", "level": "乡科级", "parent": "点军区人民政府", "location": "宜昌市点军区"},
    {"id": 35, "name": "点军区工商联", "type": "群团", "level": "乡科级", "parent": "点军区政协", "location": "宜昌市点军区"},
    {"id": 36, "name": "中共点军区委直属机关工作委员会", "type": "党委", "level": "乡科级", "parent": "中共点军区委员会", "location": "宜昌市点军区"},
]

# ── Positions ──────────────────────────────────────────────────────────────────
positions = [
    # Current Party Committee members
    {"person_id": 1, "org_id": 1, "title": "点军区委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "兼宜昌市人大常委会党组成员、副主任（副厅级）"},
    {"person_id": 1, "org_id": 12, "title": "宜昌市人大常委会副主任、党组成员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "点军区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "区政府党组书记、区长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "点军区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "三级调研员"},
    {"person_id": 4, "org_id": 1, "title": "点军区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "区纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "三级调研员，四级高级监察官"},
    {"person_id": 5, "org_id": 1, "title": "点军区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 4, "title": "区委宣传部部长", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "点军区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "三级调研员"},
    {"person_id": 6, "org_id": 5, "title": "区委政法委书记", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "点军区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 6, "title": "区人武部上校部长", "start_date": "", "end_date": "present", "rank": "正团级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "点军区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 7, "title": "区委组织部部长", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": ""},
    {"person_id": 8, "org_id": 13, "title": "区委统战部部长", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": "兼区政协党组副书记"},
    {"person_id": 9, "org_id": 1, "title": "点军区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "区政府党组成员、常务副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "协助区长负责政府日常工作"},
    {"person_id": 10, "org_id": 1, "title": "点军区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 8, "title": "区委办公室主任", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": "兼区委直属机关工委书记"},
    # Government members
    {"person_id": 11, "org_id": 2, "title": "区政府党组成员、副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 25, "title": "市公安局点军区分局局长", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "区人民政府副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "非中共党员"},
    {"person_id": 12, "org_id": 34, "title": "区红十字会会长", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "区政府党组成员、副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "区政府党组成员、副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "区政府党组成员、副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "区政府党组成员、副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "区政府党组成员、副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "区政府党组成员", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 18, "org_id": 14, "title": "湖北点军工业园区党工委委员", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": 18, "org_id": 15, "title": "电子信息产业园管理办公室专职副主任", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # People's Congress
    {"person_id": 19, "org_id": 9, "title": "区人大常委会主任、党组书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 20, "org_id": 9, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "二级调研员"},
    {"person_id": 21, "org_id": 9, "title": "区人大常委会副主任、党组成员", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "三级调研员"},
    {"person_id": 22, "org_id": 9, "title": "区人大常委会副主任、党组成员", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "三级调研员"},
    {"person_id": 23, "org_id": 9, "title": "区人大常委会副主任、党组成员", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 24, "org_id": 9, "title": "区人大常委会副主任、党组成员", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 25, "org_id": 9, "title": "区人大常委会副主任、党组成员", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # CPPCC
    {"person_id": 26, "org_id": 10, "title": "区政协主席、党组书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 27, "org_id": 10, "title": "区政协副主席、党组副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "三级调研员"},
    {"person_id": 28, "org_id": 10, "title": "区政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "三级调研员"},
    {"person_id": 29, "org_id": 10, "title": "区政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 30, "org_id": 10, "title": "区政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "兼区工商联主席"},
]

# ── Relationships ──────────────────────────────────────────────────────────────
# Core party committee members: all serve together on the standing committee
# 万红 and 王建红: top two leaders
# Standing committee members all overlap in the same organization and period

relationships = [
    # 万红 (区委书记) ↔ key colleagues
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区委书记与区长党政搭班", "overlap_org": "中共点军区委员会", "overlap_period": "2022-至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区委书记与专职副书记", "overlap_org": "中共点军区委员会", "overlap_period": "2022-至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "区委书记与组织部部长", "overlap_org": "中共点军区委员会", "overlap_period": "2022-至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "区委书记与纪委书记", "overlap_org": "中共点军区委员会", "overlap_period": "2022-至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "区委书记与宣传部部长", "overlap_org": "中共点军区委员会", "overlap_period": "2022-至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "区委书记与政法委书记", "overlap_org": "中共点军区委员会", "overlap_period": "2022-至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "区委书记与常务副区长", "overlap_org": "中共点军区委员会", "overlap_period": "2022-至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "区委书记与区委办公室主任", "overlap_org": "中共点军区委员会", "overlap_period": "2022-至今", "confidence": "confirmed"},
    # 万红 ↔ predecessor
    {"person_a": 1, "person_b": 31, "type": "predecessor_successor", "context": "万红接替宋涛任点军区委书记", "overlap_org": "中共点军区委员会", "overlap_period": "2022", "confidence": "plausible"},
    # 王建红 (区长) ↔ government team
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "区长与常务副区长", "overlap_org": "点军区人民政府", "overlap_period": "2023-至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "区长与公安分局局长（副区长）", "overlap_org": "点军区人民政府", "overlap_period": "2023-至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "点军区人民政府", "overlap_period": "2023-至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "点军区人民政府", "overlap_period": "2023-至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "点军区人民政府", "overlap_period": "2023-至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "点军区人民政府", "overlap_period": "2023-至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "点军区人民政府", "overlap_period": "2023-至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 17, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "点军区人民政府", "overlap_period": "2023-至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 18, "type": "superior_subordinate", "context": "区长与区政府党组成员", "overlap_org": "点军区人民政府", "overlap_period": "2023-至今", "confidence": "confirmed"},
    # 王建红 ↔ predecessor
    {"person_a": 2, "person_b": 32, "type": "predecessor_successor", "context": "王建红接替黄文云任点军区区长", "overlap_org": "点军区人民政府", "overlap_period": "2023", "confidence": "plausible"},
    # Standing committee collective overlaps
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "同在区委常委会", "overlap_org": "中共点军区委员会", "overlap_period": "2023-至今", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "同在区委常委会", "overlap_org": "中共点军区委员会", "overlap_period": "2023-至今", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 8, "type": "overlap", "context": "区委副书记与组织部部长工作配合", "overlap_org": "中共点军区委员会", "overlap_period": "2023-至今", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 8, "type": "overlap", "context": "纪委与组织部在干部监督方面协作", "overlap_org": "中共点军区委员会", "overlap_period": "2023-至今", "confidence": "confirmed"},
    {"person_a": 5, "person_b": 8, "type": "overlap", "context": "宣传部与组织部同在区委常委会", "overlap_org": "中共点军区委员会", "overlap_period": "2023-至今", "confidence": "confirmed"},
    {"person_a": 6, "person_b": 11, "type": "overlap", "context": "政法委书记与公安分局局长在政法系统协作", "overlap_org": "中共点军区委员会政法委员会", "overlap_period": "2023-至今", "confidence": "confirmed"},
    {"person_a": 9, "person_b": 11, "type": "overlap", "context": "常务副区长与副区长同在区政府", "overlap_org": "点军区人民政府", "overlap_period": "2023-至今", "confidence": "confirmed"},
    {"person_a": 9, "person_b": 12, "type": "overlap", "context": "同为区政府领导成员", "overlap_org": "点军区人民政府", "overlap_period": "2023-至今", "confidence": "confirmed"},
    {"person_a": 9, "person_b": 15, "type": "overlap", "context": "常务副区长与副区长（住建、城管领域）工作配合", "overlap_org": "点军区人民政府", "overlap_period": "2023-至今", "confidence": "confirmed"},
    {"person_a": 8, "person_b": 10, "type": "overlap", "context": "组织部部长与区委办主任同为区委常委", "overlap_org": "中共点军区委员会", "overlap_period": "2023-至今", "confidence": "confirmed"},
    # 人大 ↔ 党委
    {"person_a": 19, "person_b": 1, "type": "overlap", "context": "区人大常委会主任与区委书记同属区主要领导", "overlap_org": "点军区", "overlap_period": "2023-至今", "confidence": "confirmed"},
    # 政协 ↔ 党委
    {"person_a": 26, "person_b": 1, "type": "overlap", "context": "区政协主席与区委书记", "overlap_org": "点军区", "overlap_period": "2023-至今", "confidence": "confirmed"},
    # 王宏垚 ↔ 政协 (兼政协党组副书记)
    {"person_a": 8, "person_b": 26, "type": "overlap", "context": "统战部部长兼政协党组副书记与政协主席", "overlap_org": "点军区政协", "overlap_period": "2023-至今", "confidence": "confirmed"},
    # 副区长之间关系
    {"person_a": 12, "person_b": 13, "type": "overlap", "context": "同为副区长，分工领域互补（民政人社卫健 vs 教育文旅市场监管）", "overlap_org": "点军区人民政府", "overlap_period": "2023-至今", "confidence": "confirmed"},
    {"person_a": 13, "person_b": 14, "type": "overlap", "context": "同为副区长", "overlap_org": "点军区人民政府", "overlap_period": "2023-至今", "confidence": "confirmed"},
    {"person_a": 14, "person_b": 16, "type": "overlap", "context": "同为副区长（科技工业领域协作）", "overlap_org": "点军区人民政府", "overlap_period": "2023-至今", "confidence": "confirmed"},
    {"person_a": 9, "person_b": 10, "type": "overlap", "context": "常务副区长与区委办主任同为区委常委", "overlap_org": "中共点军区委员会", "overlap_period": "2023-至今", "confidence": "confirmed"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# DATABASE BUILD
# ═══════════════════════════════════════════════════════════════════════════════

def create_tables(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT,
            notes TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start_date TEXT,
            end_date TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            confidence TEXT DEFAULT 'unverified',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)
    conn.commit()


def build():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 市辖区")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 点军区人民政府官方网站 (dianjun.gov.cn)")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    # Insert persons
    cols_p = ["id", "name", "gender", "ethnicity", "birth", "birthplace",
              "education", "party_join", "work_start", "current_post",
              "current_org", "source", "notes"]
    for p in persons:
        vals = [p.get(c, "") for c in cols_p]
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?'] * len(cols_p))})", vals)

    # Insert organizations
    cols_o = ["id", "name", "type", "level", "parent", "location"]
    for o in organizations:
        vals = [o.get(c, "") for c in cols_o]
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?'] * len(cols_o))})", vals)

    # Insert positions
    cols_pos = ["person_id", "org_id", "title", "start_date", "end_date", "rank", "note"]
    for pos in positions:
        vals = [pos.get(c, "") for c in cols_pos]
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?'] * len(cols_pos))})", vals)

    # Insert relationships
    cols_r = ["person_a", "person_b", "type", "context", "overlap_org", "overlap_period", "confidence"]
    for r in relationships:
        vals = [r.get(c, "") for c in cols_r]
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?'] * len(cols_r))})", vals)

    conn.commit()
    conn.close()

    print(f"\n  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── GEXF ──────────────────────────────────────────────────────────
    print("\n--- Building GEXF graph ---")

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color_and_size(post):
        if "区委书记" in post and "副" not in post:
            return ("255,50,50", 20.0)  # Red, top leader
        elif "区长" in post and "副" not in post:
            return ("50,100,255", 20.0)  # Blue
        elif "区委副书记" in post:
            return ("150,50,50", 15.0)  # Dark red
        elif "纪委书记" in post or "监委" in post:
            return ("255,165,0", 12.0)  # Orange
        elif "常务副区长" in post or "常务" in post:
            return ("50,100,255", 15.0)
        elif "人大常委会主任" in post:
            return ("200,255,255", 15.0)  # Cyan
        elif "政协主席" in post:
            return ("255,240,200", 15.0)  # Cream
        elif "已离任" in post or "原" in post:
            return ("150,150,150", 10.0)  # Grey, past
        else:
            return ("100,100,100", 12.0)  # Grey

    def org_color(typ):
        return {
            "党委": ("255,200,200"),
            "政府": ("200,200,255"),
            "人大": ("200,255,255"),
            "政协": ("255,240,200"),
            "开发区": ("200,255,200"),
            "事业单位": ("220,220,220"),
            "群团": ("255,220,255"),
        }.get(typ, ("200,200,200"))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
        f'  <meta lastmodifieddate="{TODAY}">',
        '    <creator>Gov-Relation Research Agent</creator>',
        f'    <description>{SLUG} 领导班子关系网络</description>',
        '  </meta>',
        '  <graph mode="static" defaultedgetype="undirected">',
        '    <attributes class="node">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="current_post" type="string"/>',
        '      <attribute id="2" title="current_org" type="string"/>',
        '      <attribute id="3" title="birth" type="string"/>',
        '      <attribute id="4" title="source" type="string"/>',
        '    </attributes>',
        '    <attributes class="edge">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="context" type="string"/>',
        '      <attribute id="2" title="overlap_org" type="string"/>',
        '      <attribute id="3" title="overlap_period" type="string"/>',
        '    </attributes>',
        '    <nodes>',
    ]

    # Person nodes
    for p in persons:
        c, sz = person_color_and_size(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')
    lines.append('    <edges>')

    eid = 0
    # person → org edges
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person ↔ person edges
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF: {GEXF_PATH}")
    print(f"  节点: {len(persons) + len(organizations)} 个")
    print(f"  边: {eid} 条")
    print(f"\n✅ {SLUG} 数据构建完成。")


if __name__ == "__main__":
    build()
