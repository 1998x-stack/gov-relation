#!/usr/bin/env python3
"""
Build SQLite database + GEXF graph for 资溪县, 抚州市, 江西省.

资溪县领导班子 (as of 2026-07-15):
  - 县委书记: 李建泉 (1971-10出生，江西南城人)
  - 县长候选人: 毛奇锋 (1981-11出生，大学学历)
  - 前县长: 饶源中

资溪县位于江西省东部、抚州市东部，武夷山脉西麓。
数据来源：资溪县政府官网 (www.zixi.gov.cn) 领导之窗 及新闻报道。

Research date: 2026-07-15
"""

import sqlite3
import os
import sys
from datetime import datetime

# Paths
STAGING = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(STAGING, "..", ".."))
DB_PATH = os.path.join(STAGING, "资溪县_network.db")
GEXF_PATH = os.path.join(STAGING, "资溪县_network.gexf")

today = datetime.now().strftime("%Y-%m-%d")

# =========================================================================
# Research Data — sourced from zixi.gov.cn leadership pages (2026-07-15)
# =========================================================================

persons = [
    # === 县委领导 ===
    {
        "id": 1,
        "name": "李建泉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-10",
        "birthplace": "江西南城",
        "education": "（待补充）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "资溪县委书记",
        "current_org": "中共资溪县委员会",
        "source": "https://www.zixi.gov.cn/col/col27860/index.html",
        "notes": "1971年10月出生，江西南城人。主持县委全面工作。"
    },
    {
        "id": 2,
        "name": "毛奇锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-11",
        "birthplace": "（待核实）",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "资溪县委副书记、县长候选人",
        "current_org": "资溪县人民政府",
        "source": "https://www.zixi.gov.cn/col/col23426/index.html",
        "notes": "1981年11月出生，大学学历。负责县政府全面工作。饶源中前任县长后，毛奇锋接任县长候选人。"
    },
    {
        "id": 3,
        "name": "吴雪峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-11",
        "birthplace": "（待核实）",
        "education": "江西师范大学传播系教育技术学专业 本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "资溪县委常委、宣传部部长",
        "current_org": "中共资溪县委员会",
        "source": "https://www.zixi.gov.cn/col/col10897/index.html",
        "notes": "1975年11月出生。负责宣传思想文化和意识形态工作。"
    },
    {
        "id": 4,
        "name": "陶建华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-10",
        "birthplace": "（待核实）",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "资溪县委常委、常务副县长",
        "current_org": "资溪县人民政府",
        "source": "https://www.zixi.gov.cn/col/col9747/index.html",
        "notes": "1982年10月出生。负责县政府常务工作，分管发改、财政、税务、金融等。"
    },
    {
        "id": 5,
        "name": "王建荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-08",
        "birthplace": "（待核实）",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "资溪县委常委、统战部部长",
        "current_org": "中共资溪县委员会",
        "source": "https://www.zixi.gov.cn/col/col9750/index.html",
        "notes": "1982年8月出生。负责统战和工商联工作。"
    },
    {
        "id": 6,
        "name": "龚明明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-11",
        "birthplace": "（待核实）",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "资溪县委常委、纪委书记、监委主任",
        "current_org": "中共资溪县纪律检查委员会",
        "source": "https://www.zixi.gov.cn/col/col9743/index.html",
        "notes": "1981年11月出生。负责纪律检查和监察工作。"
    },
    {
        "id": 7,
        "name": "张义",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-05",
        "birthplace": "山东莱西",
        "education": "（待补充）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "资溪县委常委、县人武部上校部长",
        "current_org": "资溪县人民武装部",
        "source": "https://www.zixi.gov.cn/col/col28152/index.html",
        "notes": "1975年5月出生，山东莱西人。负责人民武装工作。"
    },
    {
        "id": 8,
        "name": "周勇华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-03",
        "birthplace": "江西崇仁",
        "education": "（待补充）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "资溪县委常委、组织部部长",
        "current_org": "中共资溪县委员会",
        "source": "https://www.zixi.gov.cn/col/col28153/index.html",
        "notes": "1978年3月出生，江西崇仁人。负责组织工作。"
    },
    # === 县政府领导 ===
    {
        "id": 9,
        "name": "熊迎春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-11",
        "birthplace": "（待核实）",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "资溪县副县长、县公安局局长",
        "current_org": "资溪县人民政府",
        "source": "https://www.zixi.gov.cn/col/col9739/index.html",
        "notes": "1973年11月出生。负责公安、司法、信访等工作。"
    },
    {
        "id": 10,
        "name": "郑长泽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-04",
        "birthplace": "（待核实）",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "资溪县副县长",
        "current_org": "资溪县人民政府",
        "source": "https://www.zixi.gov.cn/col/col9740/index.html",
        "notes": "1983年4月出生。负责工口、开放型经济、科技、生态环境等。"
    },
    {
        "id": 11,
        "name": "李浪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988-04",
        "birthplace": "（待核实）",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "资溪县副县长",
        "current_org": "资溪县人民政府",
        "source": "https://www.zixi.gov.cn/col/col10680/index.html",
        "notes": "1988年4月出生。负责教育、卫生健康、生态康养等。"
    },
    {
        "id": 12,
        "name": "方胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-08",
        "birthplace": "浙江淳安",
        "education": "大学文化",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "资溪县副县长",
        "current_org": "资溪县人民政府",
        "source": "https://www.zixi.gov.cn/col/col9741/index.html",
        "notes": "1981年8月出生，浙江淳安人。负责住建、城管、交通、农业农村等。"
    },
    {
        "id": 13,
        "name": "张泽栋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989-06",
        "birthplace": "山东淄博",
        "education": "（待补充）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "资溪县副县长（挂职）",
        "current_org": "资溪县人民政府",
        "source": "https://www.zixi.gov.cn/col/col26985/index.html",
        "notes": "1989年6月出生，山东淄博人。挂职副县长，负责市场监管、智汇资溪等。"
    },
    {
        "id": 14,
        "name": "赵起超",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1983-10",
        "birthplace": "湖南宁乡",
        "education": "（待补充）",
        "party_join": "民盟盟员",
        "work_start": "",
        "current_post": "资溪县副县长",
        "current_org": "资溪县人民政府",
        "source": "https://www.zixi.gov.cn/col/col27861/index.html",
        "notes": "1983年10月出生，湖南宁乡人，民盟盟员。负责民政、文旅、体育等。"
    },
    # === 前县长（过渡期） ===
    {
        "id": 15,
        "name": "饶源中",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "（待核实）",
        "birthplace": "（待核实）",
        "education": "（待补充）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "资溪县委副书记、县长（过渡交接中）",
        "current_org": "资溪县人民政府",
        "source": "https://www.zixi.gov.cn/art/2026/6/22/art_1695_4456060.html",
        "notes": "2026年6月仍以县长身份主持会议；至2026年7月毛奇锋已任县长候选人。"
    },
    # === 人大领导 ===
    {
        "id": 16,
        "name": "张俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-10",
        "birthplace": "（待核实）",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "资溪县人大常委会主任",
        "current_org": "资溪县人大常委会",
        "source": "https://www.zixi.gov.cn/col/col9751/index.html",
        "notes": "1972年10月出生。主持县人大常委会全面工作。"
    },
    {
        "id": 17,
        "name": "吴小文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-08",
        "birthplace": "（待核实）",
        "education": "南昌大学土木工程 大学学历",
        "party_join": "无党派人士",
        "work_start": "",
        "current_post": "资溪县人大常委会副主任",
        "current_org": "资溪县人大常委会",
        "source": "https://www.zixi.gov.cn/col/col9753/index.html",
        "notes": "1971年8月出生，无党派人士。"
    },
    {
        "id": 18,
        "name": "李晔",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-08",
        "birthplace": "（待核实）",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "资溪县人大常委会副主任",
        "current_org": "资溪县人大常委会",
        "source": "https://www.zixi.gov.cn/col/col9756/index.html",
        "notes": "1983年8月出生。"
    },
    {
        "id": 19,
        "name": "陈国强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-11",
        "birthplace": "（待核实）",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "资溪县人大常委会副主任",
        "current_org": "资溪县人大常委会",
        "source": "https://www.zixi.gov.cn/col/col25523/index.html",
        "notes": "1973年11月出生。"
    },
    {
        "id": 20,
        "name": "朱平江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-09",
        "birthplace": "（待核实）",
        "education": "大专",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "资溪县人大常委会副主任提名人选",
        "current_org": "资溪县人大常委会",
        "source": "https://www.zixi.gov.cn/col/col28505/index.html",
        "notes": "1972年9月出生。"
    },
    # === 政协领导 ===
    {
        "id": 21,
        "name": "黄惠忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-09",
        "birthplace": "江西资溪",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "资溪县政协主席",
        "current_org": "资溪县政协",
        "source": "https://www.zixi.gov.cn/col/col9757/index.html",
        "notes": "1970年9月出生，江西资溪人，本地成长干部。"
    },
    {
        "id": 22,
        "name": "余鑫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-04",
        "birthplace": "（待核实）",
        "education": "本科学历",
        "party_join": "无党派人士",
        "work_start": "",
        "current_post": "资溪县政协副主席、县城乡建设和交通运输局局长",
        "current_org": "资溪县政协",
        "source": "https://www.zixi.gov.cn/col/col9762/index.html",
        "notes": "1982年4月出生，无党派人士。兼任县城乡建设和交通运输局局长。"
    },
    {
        "id": 23,
        "name": "叶莉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981-02",
        "birthplace": "（待核实）",
        "education": "大学本科学历",
        "party_join": "无党派人士",
        "work_start": "",
        "current_post": "资溪县政协副主席",
        "current_org": "资溪县政协",
        "source": "https://www.zixi.gov.cn/col/col9761/index.html",
        "notes": "1981年2月出生，无党派人士。"
    },
    {
        "id": 24,
        "name": "李芳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976-03",
        "birthplace": "江西进贤",
        "education": "（待补充）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "资溪县政协副主席",
        "current_org": "资溪县政协",
        "source": "https://www.zixi.gov.cn/col/col28151/index.html",
        "notes": "1976年3月出生，江西进贤人。"
    },
]

orgs = [
    {
        "id": 1,
        "name": "中共资溪县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共抚州市委员会",
        "location": "江西抚州资溪"
    },
    {
        "id": 2,
        "name": "资溪县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "抚州市人民政府",
        "location": "江西抚州资溪"
    },
    {
        "id": 3,
        "name": "中共资溪县纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共抚州市纪律检查委员会",
        "location": "江西抚州资溪"
    },
    {
        "id": 4,
        "name": "资溪县人民武装部",
        "type": "政府",
        "level": "县处级",
        "parent": "抚州军分区",
        "location": "江西抚州资溪"
    },
    {
        "id": 5,
        "name": "资溪县人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "抚州市人大常委会",
        "location": "江西抚州资溪"
    },
    {
        "id": 6,
        "name": "资溪县政协",
        "type": "政协",
        "level": "县处级",
        "parent": "抚州市政协",
        "location": "江西抚州资溪"
    },
    {
        "id": 7,
        "name": "资溪县公安局",
        "type": "政府",
        "level": "正科级",
        "parent": "资溪县人民政府",
        "location": "江西抚州资溪"
    },
]

positions = [
    # === 县委 ===
    {
        "id": 1,
        "person_id": 1,
        "org_id": 1,
        "title": "资溪县委书记",
        "start": "（待核实）",
        "end": "",
        "rank": "县处级正职",
        "note": "现任，主持县委全面工作"
    },
    {
        "id": 2,
        "person_id": 2,
        "org_id": 2,
        "title": "资溪县委副书记、县长候选人",
        "start": "2026-07",
        "end": "",
        "rank": "县处级正职",
        "note": "县长候选人，负责县政府全面工作"
    },
    {
        "id": 3,
        "person_id": 2,
        "org_id": 1,
        "title": "资溪县委副书记",
        "start": "2026-07",
        "end": "",
        "rank": "县处级副职",
        "note": "县委副书记"
    },
    {
        "id": 4,
        "person_id": 3,
        "org_id": 1,
        "title": "资溪县委常委、宣传部部长",
        "start": "（待核实）",
        "end": "",
        "rank": "县处级副职",
        "note": "负责宣传思想文化和意识形态工作"
    },
    {
        "id": 5,
        "person_id": 4,
        "org_id": 2,
        "title": "资溪县委常委、常务副县长",
        "start": "（待核实）",
        "end": "",
        "rank": "县处级副职",
        "note": "负责县政府常务工作"
    },
    {
        "id": 6,
        "person_id": 5,
        "org_id": 1,
        "title": "资溪县委常委、统战部部长",
        "start": "（待核实）",
        "end": "",
        "rank": "县处级副职",
        "note": "负责统战和工商联工作"
    },
    {
        "id": 7,
        "person_id": 6,
        "org_id": 3,
        "title": "资溪县委常委、纪委书记、监委主任",
        "start": "（待核实）",
        "end": "",
        "rank": "县处级副职",
        "note": "负责纪律检查和监察工作"
    },
    {
        "id": 8,
        "person_id": 7,
        "org_id": 4,
        "title": "资溪县委常委、县人武部上校部长",
        "start": "（待核实）",
        "end": "",
        "rank": "县处级副职",
        "note": "负责人民武装工作"
    },
    {
        "id": 9,
        "person_id": 8,
        "org_id": 1,
        "title": "资溪县委常委、组织部部长",
        "start": "（待核实）",
        "end": "",
        "rank": "县处级副职",
        "note": "负责组织工作"
    },
    # === 政府 ===
    {
        "id": 10,
        "person_id": 9,
        "org_id": 7,
        "title": "资溪县副县长、县公安局局长",
        "start": "（待核实）",
        "end": "",
        "rank": "县处级副职",
        "note": "负责公安、司法、信访等"
    },
    {
        "id": 11,
        "person_id": 10,
        "org_id": 2,
        "title": "资溪县副县长",
        "start": "（待核实）",
        "end": "",
        "rank": "县处级副职",
        "note": "负责工口、开放型经济、科技等"
    },
    {
        "id": 12,
        "person_id": 11,
        "org_id": 2,
        "title": "资溪县副县长",
        "start": "（待核实）",
        "end": "",
        "rank": "县处级副职",
        "note": "负责教育、卫生健康、生态康养等"
    },
    {
        "id": 13,
        "person_id": 12,
        "org_id": 2,
        "title": "资溪县副县长",
        "start": "（待核实）",
        "end": "",
        "rank": "县处级副职",
        "note": "负责住建、城管、交通、农业农村等"
    },
    {
        "id": 14,
        "person_id": 13,
        "org_id": 2,
        "title": "资溪县副县长（挂职）",
        "start": "（待核实）",
        "end": "",
        "rank": "县处级副职",
        "note": "挂职，负责市场监管、智汇资溪等"
    },
    {
        "id": 15,
        "person_id": 14,
        "org_id": 2,
        "title": "资溪县副县长",
        "start": "（待核实）",
        "end": "",
        "rank": "县处级副职",
        "note": "负责民政、文旅、体育等"
    },
    # === 前县长 ===
    {
        "id": 16,
        "person_id": 15,
        "org_id": 2,
        "title": "资溪县委副书记、县长",
        "start": "（待核实）",
        "end": "2026-06",
        "rank": "县处级正职",
        "note": "前任县长，2026年6月仍在位，后毛奇锋接任县长候选人"
    },
    # === 人大 ===
    {
        "id": 17,
        "person_id": 16,
        "org_id": 5,
        "title": "资溪县人大常委会主任",
        "start": "（待核实）",
        "end": "",
        "rank": "县处级正职",
        "note": "主持县人大常委会全面工作"
    },
    {
        "id": 18,
        "person_id": 17,
        "org_id": 5,
        "title": "资溪县人大常委会副主任",
        "start": "（待核实）",
        "end": "",
        "rank": "县处级副职",
        "note": ""
    },
    {
        "id": 19,
        "person_id": 18,
        "org_id": 5,
        "title": "资溪县人大常委会副主任",
        "start": "（待核实）",
        "end": "",
        "rank": "县处级副职",
        "note": ""
    },
    {
        "id": 20,
        "person_id": 19,
        "org_id": 5,
        "title": "资溪县人大常委会副主任",
        "start": "（待核实）",
        "end": "",
        "rank": "县处级副职",
        "note": ""
    },
    {
        "id": 21,
        "person_id": 20,
        "org_id": 5,
        "title": "资溪县人大常委会副主任提名人选",
        "start": "（待核实）",
        "end": "",
        "rank": "县处级副职",
        "note": ""
    },
    # === 政协 ===
    {
        "id": 22,
        "person_id": 21,
        "org_id": 6,
        "title": "资溪县政协主席",
        "start": "（待核实）",
        "end": "",
        "rank": "县处级正职",
        "note": "主持县政协全面工作"
    },
    {
        "id": 23,
        "person_id": 22,
        "org_id": 6,
        "title": "资溪县政协副主席、县城乡建设和交通运输局局长",
        "start": "（待核实）",
        "end": "",
        "rank": "县处级副职",
        "note": "无党派人士"
    },
    {
        "id": 24,
        "person_id": 23,
        "org_id": 6,
        "title": "资溪县政协副主席",
        "start": "（待核实）",
        "end": "",
        "rank": "县处级副职",
        "note": "无党派人士"
    },
    {
        "id": 25,
        "person_id": 24,
        "org_id": 6,
        "title": "资溪县政协副主席",
        "start": "（待核实）",
        "end": "",
        "rank": "县处级副职",
        "note": ""
    },
]

relationships = [
    # 党政搭档
    {
        "id": 1,
        "person_a_id": 1,
        "person_b_id": 2,
        "type": "党政搭档",
        "context": "李建泉（县委书记）与毛奇锋（县长候选人）为资溪县党政主要领导人",
        "overlap_org": "资溪县",
        "overlap_period": "2026-07至今"
    },
    {
        "id": 2,
        "person_a_id": 1,
        "person_b_id": 15,
        "type": "党政搭档",
        "context": "李建泉（县委书记）与饶源中（前县长）在资溪县党政班子搭档",
        "overlap_org": "资溪县",
        "overlap_period": "至2026-06"
    },
    # 纪委书记与县委书记
    {
        "id": 3,
        "person_a_id": 1,
        "person_b_id": 6,
        "type": "上下级关系",
        "context": "龚明明（纪委书记）在李建泉（县委书记）领导下履行监督责任",
        "overlap_org": "中共资溪县委员会",
        "overlap_period": "在任期间"
    },
    # 组织部长与县委书记
    {
        "id": 4,
        "person_a_id": 1,
        "person_b_id": 8,
        "type": "上下级关系",
        "context": "周勇华（组织部部长）在李建泉（县委书记）领导下负责组织工作",
        "overlap_org": "中共资溪县委员会",
        "overlap_period": "在任期间"
    },
    # 同乡关系（崇仁）
    {
        "id": 5,
        "person_a_id": 8,
        "person_b_id": 21,
        "type": "同籍贯（崇仁县）",
        "context": "周勇华（组织部部长）为江西崇仁人；黄惠忠（政协主席）为江西资溪本地人",
        "overlap_org": "资溪县",
        "overlap_period": "在任期间"
    },
    # 南城同乡关系
    {
        "id": 6,
        "person_a_id": 1,
        "person_b_id": 24,
        "type": "籍贯差异",
        "context": "李建泉（江西南城人）与李芳（江西进贤人）籍贯不同，但均不在资溪本地出生",
        "overlap_org": "资溪县",
        "overlap_period": "在任期间"
    },
    # 常务副县长与县长
    {
        "id": 7,
        "person_a_id": 4,
        "person_b_id": 2,
        "type": "上下级关系",
        "context": "陶建华（常务副县长）协助毛奇锋（县长候选人）处理县政府日常工作",
        "overlap_org": "资溪县人民政府",
        "overlap_period": "2026-07至今"
    },
    # 公安局与县委
    {
        "id": 8,
        "person_a_id": 9,
        "person_b_id": 1,
        "type": "上下级关系",
        "context": "熊迎春（副县长、公安局长）在县委领导下负责公安司法工作",
        "overlap_org": "资溪县",
        "overlap_period": "在任期间"
    },
    # 人大与县委
    {
        "id": 9,
        "person_a_id": 16,
        "person_b_id": 1,
        "type": "同班子",
        "context": "张俊（人大主任）与李建泉（县委书记）为资溪县四套班子正职",
        "overlap_org": "资溪县",
        "overlap_period": "在任期间"
    },
    # 政协与县委
    {
        "id": 10,
        "person_a_id": 21,
        "person_b_id": 1,
        "type": "同班子",
        "context": "黄惠忠（政协主席）与李建泉（县委书记）为资溪县四套班子正职",
        "overlap_org": "资溪县",
        "overlap_period": "在任期间"
    },
    # 前县长与前县委书记的党政搭档
    {
        "id": 11,
        "person_a_id": 15,
        "person_b_id": 4,
        "type": "上下级关系",
        "context": "陶建华（常务副县长）在饶源中（前县长）领导下负责县政府常务工作",
        "overlap_org": "资溪县人民政府",
        "overlap_period": "至2026-06"
    },
]


# =========================================================================
# Utility functions
# =========================================================================

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def pcolor_viz(post):
    """Return viz:color RGB string based on post title."""
    post = post or ""
    if "书记" in post and ("县委" in post or "区委" in post):
        return "255,50,50"  # red for party secretary
    if "县长" in post and "副" not in post and "候选" not in post and "前任" not in post:
        return "50,100,255"  # blue for government head
    if "县长" in post and ("副" in post or "候选" in post or "前" in post):
        return "80,140,230"  # lighter blue for deputies/candidates/former
    if "副县长" in post:
        return "80,140,230"
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"  # orange for discipline
    return "120,120,120"  # grey


def ocolor_viz(otype):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(otype, "200,200,200")


def is_top_leader(pid):
    return pid in [1, 2, 15, 16, 21]


# =========================================================================
# SQLite Build
# =========================================================================

def build_sqlite():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        gender TEXT,
        ethnicity TEXT,
        birth TEXT,
        birthplace TEXT,
        education TEXT,
        party_join TEXT,
        work_start TEXT,
        current_post TEXT,
        current_org TEXT,
        source TEXT
    );
    CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT,
        level TEXT,
        parent TEXT,
        location TEXT
    );
    CREATE TABLE positions (
        id INTEGER PRIMARY KEY,
        person_id INTEGER NOT NULL,
        org_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        start TEXT,
        end TEXT,
        rank TEXT,
        note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );
    CREATE TABLE relationships (
        id INTEGER PRIMARY KEY,
        person_a_id INTEGER NOT NULL,
        person_b_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        context TEXT,
        overlap_org TEXT,
        overlap_period TEXT,
        FOREIGN KEY (person_a_id) REFERENCES persons(id),
        FOREIGN KEY (person_b_id) REFERENCES persons(id)
    );
    """)

    for p in persons:
        c.execute(
            "INSERT INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"],
             p["birth"], p["birthplace"], p["education"],
             p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"])
        )

    for o in orgs:
        c.execute(
            "INSERT INTO organizations VALUES(?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
        )

    for pos in positions:
        c.execute(
            "INSERT INTO positions VALUES(?,?,?,?,?,?,?,?)",
            (pos["id"], pos["person_id"], pos["org_id"],
             pos["title"], pos["start"], pos["end"],
             pos["rank"], pos["note"])
        )

    for r in relationships:
        c.execute(
            "INSERT INTO relationships VALUES(?,?,?,?,?,?,?)",
            (r["id"], r["person_a_id"], r["person_b_id"],
             r["type"], r["context"], r["overlap_org"], r["overlap_period"])
        )

    conn.commit()

    counts = {}
    for t in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {t}")
        counts[t] = c.fetchone()[0]
    conn.close()

    return counts


# =========================================================================
# GEXF Build
# =========================================================================

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>资溪县领导班子工作关系网络 - 2026-07-15</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    for aid, atitle in [("0", "type"), ("1", "birth"), ("2", "birthplace"), ("3", "current_post")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    for aid, atitle in [("0", "type"), ("1", "start"), ("2", "end"), ("3", "context")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = pcolor_viz(p["current_post"])
        sz = "20.0" if is_top_leader(p["id"]) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        for f, v in [("0", "person"), ("1", p.get("birth", "")),
                     ("2", p.get("birthplace", "")), ("3", p.get("current_post", ""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in orgs:
        c = ocolor_viz(o.get("type", ""))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        for f, v in [("0", "organization"), ("1", ""),
                     ("2", o.get("location", "")), ("3", "")]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(
            f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" '
            f'label="{esc(pos["title"])}" weight="1.0">'
        )
        lines.append('        <attvalues>')
        for f, v in [("0", "worked_at"), ("1", pos.get("start", "")),
                     ("2", pos.get("end", "")), ("3", pos.get("note", ""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(
            f'      <edge id="{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" '
            f'label="{esc(r["type"])}" weight="2.0">'
        )
        lines.append('        <attvalues>')
        for f, v in [("0", r["type"]), ("1", ""), ("2", ""), ("3", r.get("context", ""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    tn = len(persons) + len(orgs)
    te = len(positions) + len(relationships)
    return tn, te


# =========================================================================
# Main
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print(f"  资溪县领导班子工作关系网络 — 数据构建")
    print(f"  日期: {today}")
    print(f"  数据来源: 资溪县政府官网 (zixi.gov.cn) 领导之窗")
    print("=" * 60)

    # SQLite
    counts = build_sqlite()
    print(f"\n  ✓ SQLite: {DB_PATH}")
    for t, n in counts.items():
        print(f"    {t}: {n}")

    # GEXF
    tn, te = build_gexf()
    print(f"\n  ✓ GEXF: {GEXF_PATH}")
    print(f"    Nodes: {tn}  |  Edges: {te}")

    # Verify
    errors = []
    if not os.path.exists(DB_PATH):
        errors.append(f"Database not created: {DB_PATH}")
    if not os.path.exists(GEXF_PATH):
        errors.append(f"GEXF not created: {GEXF_PATH}")

    if errors:
        print(f"\n  ✗ ERRORS:")
        for e in errors:
            print(f"    - {e}")
        sys.exit(1)
    else:
        print(f"\n  ✓ BUILD COMPLETE")
        print(f"    DB size: {os.path.getsize(DB_PATH)} bytes")
        print(f"    GEXF size: {os.path.getsize(GEXF_PATH)} bytes")
        print()
        print(f"  📋 数据概要：")
        print(f"    - 县委书记：李建泉（1971-10，江西南城）")
        print(f"    - 县长候选人：毛奇锋（1981-11，大学学历）")
        print(f"    - 前县长：饶源中（2026年6月交接中）")
        print(f"    - 县委常委：吴雪峰、陶建华、王建荣、龚明明、张义、周勇华")
        print(f"    - 副县长：熊迎春、郑长泽、李浪、方胜、张泽栋（挂职）、赵起超")
        print(f"    - 人大主任：张俊")
        print(f"    - 政协主席：黄惠忠")
