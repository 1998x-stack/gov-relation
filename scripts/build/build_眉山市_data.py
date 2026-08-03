#!/usr/bin/env python3
"""眉山市 (prefecture-level city, Sichuan) 领导班子工作关系网络 — 数据构建脚本"""

import sqlite3
import sys
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(BASE, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gov_relation.runner import run_build

SLUG = "眉山市"
DATE_TAG = datetime.now().strftime("%Y%m%d")

# Staging paths
DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")

# ── Organizations ────────────────────────────────────────────────────────
ORGANIZATIONS = [
    {"id": 1, "name": "中共眉山市委", "type": "党委", "level": "地级市", "parent": "中共四川省委", "location": "四川省眉山市"},
    {"id": 2, "name": "眉山市人民政府", "type": "政府", "level": "地级市", "parent": "四川省人民政府", "location": "四川省眉山市"},
    {"id": 3, "name": "眉山市人大常委会", "type": "人大", "level": "地级市", "parent": "四川省人大常委会", "location": "四川省眉山市"},
    {"id": 4, "name": "政协眉山市委员会", "type": "政协", "level": "地级市", "parent": "政协四川省委员会", "location": "四川省眉山市"},
    {"id": 5, "name": "眉山市纪委监委", "type": "纪委", "level": "地级市", "parent": "中共眉山市委", "location": "四川省眉山市"},
    {"id": 6, "name": "眉山军分区", "type": "军队", "level": "地级市", "parent": "四川省军区", "location": "四川省眉山市"},
    {"id": 7, "name": "眉山市公安局", "type": "政府", "level": "地级市", "parent": "眉山市人民政府", "location": "四川省眉山市"},
    {"id": 8, "name": "天府新区眉山党工委", "type": "党委", "level": "地级市", "parent": "中共眉山市委", "location": "四川省眉山市"},
    {"id": 9, "name": "四川省委办公厅", "type": "党委", "level": "省级", "parent": "中共四川省委", "location": "四川省成都市"},
    {"id": 10, "name": "四川省委组织部", "type": "党委", "level": "省级", "parent": "中共四川省委", "location": "四川省成都市"},
    {"id": 11, "name": "四川省交通运输厅", "type": "政府", "level": "省级", "parent": "四川省人民政府", "location": "四川省成都市"},
    {"id": 12, "name": "泸州市人民政府", "type": "政府", "level": "地级市", "parent": "四川省人民政府", "location": "四川省泸州市"},
    {"id": 13, "name": "中共泸州市委", "type": "党委", "level": "地级市", "parent": "中共四川省委", "location": "四川省泸州市"},
    {"id": 14, "name": "四川省发展和改革委员会", "type": "政府", "level": "省级", "parent": "四川省人民政府", "location": "四川省成都市"},
    {"id": 15, "name": "眉山市中级人民法院", "type": "司法", "level": "地级市", "parent": "四川省高级人民法院", "location": "四川省眉山市"},
    {"id": 16, "name": "眉山市人民检察院", "type": "司法", "level": "地级市", "parent": "四川省人民检察院", "location": "四川省眉山市"},
    {"id": 17, "name": "眉山军分区", "type": "军队", "level": "地级市", "parent": "四川省军区", "location": "四川省眉山市"},
]

# ── Persons ──────────────────────────────────────────────────────────────
PERSONS = [
    # 01 — 张道平 (市委书记)
    {
        "id": 1, "name": "张道平", "gender": "男", "ethnicity": "汉族",
        "birth": "1970年1月", "birthplace": "四川宜宾",
        "education": "在职研究生学历，经济学博士", "party_join": "中共党员",
        "work_start": None,
        "current_post": "中共眉山市委书记、眉山军分区党委第一书记",
        "current_org": "中共眉山市委",
        "source": "https://www.ms.gov.cn/info/1483/1199786.htm",
    },
    # 02 — 王斌达 (市长)
    {
        "id": 2, "name": "王斌达", "gender": "男", "ethnicity": "汉族",
        "birth": "1979年11月", "birthplace": "浙江杭州",
        "education": "党校研究生学历", "party_join": "2002年12月",
        "work_start": "2003年7月",
        "current_post": "眉山市委副书记、市政府市长、党组书记",
        "current_org": "眉山市人民政府",
        "source": "https://www.ms.gov.cn/info/5627/1175807.htm",
    },
    # 03 — 刘海 (市委副书记)
    {
        "id": 3, "name": "刘海", "gender": "男", "ethnicity": "汉族",
        "birth": "1973年4月", "birthplace": None,
        "education": "大学，法律硕士", "party_join": "中共党员",
        "work_start": None,
        "current_post": "眉山市委副书记",
        "current_org": "中共眉山市委",
        "source": "https://www.ms.gov.cn/info/1483/1109250.htm",
    },
    # 04 — 邹汝林 (常务副市长)
    {
        "id": 4, "name": "邹汝林", "gender": "男", "ethnicity": "汉族",
        "birth": "1970年9月", "birthplace": None,
        "education": "省委党校大学", "party_join": "中共党员",
        "work_start": None,
        "current_post": "眉山市委常委、市政府常务副市长、党组副书记",
        "current_org": "眉山市人民政府",
        "source": "https://www.ms.gov.cn/info/1483/1160630.htm",
    },
    # 05 — 廖歆毓 (市纪委书记)
    {
        "id": 5, "name": "廖歆毓", "gender": "女", "ethnicity": "汉族",
        "birth": "1975年10月", "birthplace": None,
        "education": "大学，管理学硕士", "party_join": "中共党员",
        "work_start": None,
        "current_post": "眉山市委常委、市纪委书记、市监委主任",
        "current_org": "眉山市纪委监委",
        "source": "https://www.ms.gov.cn/info/1483/1170387.htm",
    },
    # 06 — 杨军 (政法委书记)
    {
        "id": 6, "name": "杨军", "gender": "男", "ethnicity": "汉族",
        "birth": "1970年4月", "birthplace": None,
        "education": "在职研究生", "party_join": "中共党员",
        "work_start": None,
        "current_post": "眉山市委常委、政法委书记",
        "current_org": "中共眉山市委",
        "source": "https://www.ms.gov.cn/info/1483/1119412.htm",
    },
    # 07 — 鲁力 (统战部部长)
    {
        "id": 7, "name": "鲁力", "gender": "男", "ethnicity": "汉族",
        "birth": "1970年6月", "birthplace": None,
        "education": "省委党校研究生", "party_join": "中共党员",
        "work_start": None,
        "current_post": "眉山市委常委、统战部部长、市总工会主席",
        "current_org": "中共眉山市委",
        "source": "https://www.ms.gov.cn/info/1483/1122218.htm",
    },
    # 08 — 关冀 (宣传部部长)
    {
        "id": 8, "name": "关冀", "gender": "男", "ethnicity": "汉族",
        "birth": "1978年9月", "birthplace": None,
        "education": "在职硕士", "party_join": "中共党员",
        "work_start": None,
        "current_post": "眉山市委常委、宣传部部长",
        "current_org": "中共眉山市委",
        "source": "https://www.ms.gov.cn/info/1483/1201097.htm",
    },
    # 09 — 杨东生 (组织部部长)
    {
        "id": 9, "name": "杨东生", "gender": "男", "ethnicity": "汉族",
        "birth": "1973年11月", "birthplace": None,
        "education": "大学", "party_join": "中共党员",
        "work_start": None,
        "current_post": "眉山市委常委、组织部部长、市直机关工委书记、党校校长",
        "current_org": "中共眉山市委",
        "source": "https://www.ms.gov.cn/info/1483/1192696.htm",
    },
    # 10 — 余华勇 (军分区政委)
    {
        "id": 10, "name": "余华勇", "gender": "男", "ethnicity": "汉族",
        "birth": "1971年8月", "birthplace": None,
        "education": "大学", "party_join": "中共党员",
        "work_start": None,
        "current_post": "眉山市委常委、眉山军分区政治委员",
        "current_org": "眉山军分区",
        "source": "https://www.ms.gov.cn/info/1483/1194401.htm",
    },
    # 11 — 郑斌 (挂职副市长)
    {
        "id": 11, "name": "郑斌", "gender": "男", "ethnicity": "汉族",
        "birth": "1982年9月", "birthplace": None,
        "education": "博士研究生", "party_join": "中共党员",
        "work_start": None,
        "current_post": "眉山市委常委、市政府副市长（挂职）",
        "current_org": "眉山市人民政府",
        "source": "https://www.ms.gov.cn/info/1483/1200288.htm",
    },
    # 12 — 李建兴 (副市长，九三学社)
    {
        "id": 12, "name": "李建兴", "gender": "男", "ethnicity": "汉族",
        "birth": "1972年10月", "birthplace": None,
        "education": "研究生", "party_join": "九三学社",
        "work_start": None,
        "current_post": "眉山市人民政府副市长",
        "current_org": "眉山市人民政府",
        "source": "https://www.ms.gov.cn/info/5628/1120201.htm",
    },
    # 13 — 李鹏 (副市长、公安局局长)
    {
        "id": 13, "name": "李鹏", "gender": "男", "ethnicity": "汉族",
        "birth": "1972年6月", "birthplace": None,
        "education": "大学", "party_join": "中共党员",
        "work_start": None,
        "current_post": "眉山市人民政府副市长、市公安局局长",
        "current_org": "眉山市公安局",
        "source": "https://www.ms.gov.cn/info/5628/1175106.htm",
    },
    # 14 — 戴林莉 (副市长)
    {
        "id": 14, "name": "戴林莉", "gender": "女", "ethnicity": "汉族",
        "birth": "1975年10月", "birthplace": None,
        "education": "研究生", "party_join": "中共党员",
        "work_start": None,
        "current_post": "眉山市人民政府副市长",
        "current_org": "眉山市人民政府",
        "source": "https://www.ms.gov.cn/info/5628/1120500.htm",
    },
    # 15 — 林双全 (副市长)
    {
        "id": 15, "name": "林双全", "gender": "男", "ethnicity": "汉族",
        "birth": "1973年9月", "birthplace": None,
        "education": "大学", "party_join": "中共党员",
        "work_start": None,
        "current_post": "眉山市人民政府副市长",
        "current_org": "眉山市人民政府",
        "source": "https://www.ms.gov.cn/info/5628/1168871.htm",
    },
    # 16 — 田一澍 (挂职副市长)
    {
        "id": 16, "name": "田一澍", "gender": "男", "ethnicity": "汉族",
        "birth": "1972年7月", "birthplace": None,
        "education": "大学", "party_join": "中共党员",
        "work_start": None,
        "current_post": "眉山市人民政府副市长（挂职）",
        "current_org": "眉山市人民政府",
        "source": "https://www.ms.gov.cn/info/5628/1177653.htm",
    },
    # 17 — 车智勇 (副市长)
    {
        "id": 17, "name": "车智勇", "gender": "男", "ethnicity": "汉族",
        "birth": "1975年10月", "birthplace": None,
        "education": "在职大学", "party_join": "中共党员",
        "work_start": None,
        "current_post": "眉山市人民政府副市长",
        "current_org": "眉山市人民政府",
        "source": "https://www.ms.gov.cn/info/5628/1195675.htm",
    },
    # 18 — 周代军 (副市长、洪雅县委书记)
    {
        "id": 18, "name": "周代军", "gender": "男", "ethnicity": "苗族",
        "birth": "1974年9月", "birthplace": "重庆彭水",
        "education": "大学（四川工业学院）", "party_join": "1995年12月",
        "work_start": "1998年7月",
        "current_post": "眉山市人民政府副市长、洪雅县委书记",
        "current_org": "眉山市人民政府",
        "source": "https://www.ms.gov.cn/info/5628/1200298.htm",
    },
    # 19 — 郭红 (市政府党组成员)
    {
        "id": 19, "name": "郭红", "gender": "女", "ethnicity": "汉族",
        "birth": "1970年4月", "birthplace": None,
        "education": "四川大学研究生", "party_join": "中共党员",
        "work_start": None,
        "current_post": "眉山市政府党组成员、天府新区眉山管委会主任",
        "current_org": "眉山市人民政府",
        "source": "https://www.ms.gov.cn/info/6919/1170168.htm",
    },
    # 20 — 黄河 (前任市委书记，现省交通运输厅厅长)
    {
        "id": 20, "name": "黄河", "gender": "男", "ethnicity": "土家族",
        "birth": "1967年3月", "birthplace": "重庆",
        "education": "在职研究生学历", "party_join": "1996年4月",
        "work_start": "1990年7月",
        "current_post": "四川省交通运输厅党组书记、厅长",
        "current_org": "四川省交通运输厅",
        "source": "https://baike.baidu.com/item/%E9%BB%84%E6%B2%B3/15948420",
    },
    # 21 — 胡元坤 (前任市委书记)
    {
        "id": 21, "name": "胡元坤", "gender": "男", "ethnicity": "汉族",
        "birth": None, "birthplace": None,
        "education": None, "party_join": None, "work_start": None,
        "current_post": "四川省政府秘书长（前任眉山市委书记）",
        "current_org": "四川省人民政府",
        "source": "https://baike.baidu.com/item/%E8%83%A1%E5%85%83%E5%9D%A4",
    },
]

# ── Positions ────────────────────────────────────────────────────────────
POSITIONS = [
    # 张道平
    {"person_id": 1, "org_id": 1, "title": "眉山市委书记", "start_date": "2026-05", "end_date": None, "rank": "正厅级",
     "note": "兼眉山军分区党委第一书记"},
    {"person_id": 1, "org_id": 9, "title": "四川省委副秘书长、办公厅主任", "start_date": "2017-08", "end_date": "2026-05", "rank": "正厅级",
     "note": "省委办公厅"},
    {"person_id": 1, "org_id": 9, "title": "四川省委办公厅综合调研室主任", "start_date": "2015-03", "end_date": "2017-08", "rank": "副厅级",
     "note": "2015年3月任现级"},

    # 王斌达
    {"person_id": 2, "org_id": 1, "title": "眉山市委副书记", "start_date": "2024-11", "end_date": None, "rank": "正厅级"},
    {"person_id": 2, "org_id": 2, "title": "眉山市人民政府市长、党组书记", "start_date": "2025-01", "end_date": None, "rank": "正厅级"},
    {"person_id": 2, "org_id": 2, "title": "眉山市代市长", "start_date": "2024-11", "end_date": "2025-01", "rank": "正厅级"},
    {"person_id": 2, "org_id": 13, "title": "泸州市委常委、常务副市长", "start_date": "2023-10", "end_date": "2024-11", "rank": "副厅级"},
    {"person_id": 2, "org_id": 12, "title": "泸州市人民政府副市长", "start_date": "2021-09", "end_date": "2023-10", "rank": "副厅级"},

    # 刘海
    {"person_id": 3, "org_id": 1, "title": "眉山市委副书记", "start_date": None, "end_date": None, "rank": "副厅级",
     "note": "专职副书记"},

    # 邹汝林
    {"person_id": 4, "org_id": 1, "title": "眉山市委常委", "start_date": None, "end_date": None, "rank": "副厅级"},
    {"person_id": 4, "org_id": 2, "title": "眉山市常务副市长、党组副书记", "start_date": None, "end_date": None, "rank": "副厅级"},

    # 廖歆毓
    {"person_id": 5, "org_id": 1, "title": "眉山市委常委", "start_date": None, "end_date": None, "rank": "副厅级"},
    {"person_id": 5, "org_id": 5, "title": "市纪委书记、市监委主任", "start_date": None, "end_date": None, "rank": "副厅级"},

    # 杨军
    {"person_id": 6, "org_id": 1, "title": "眉山市委常委、政法委书记", "start_date": None, "end_date": None, "rank": "副厅级"},

    # 鲁力
    {"person_id": 7, "org_id": 1, "title": "眉山市委常委、统战部部长", "start_date": None, "end_date": None, "rank": "副厅级"},

    # 关冀
    {"person_id": 8, "org_id": 1, "title": "眉山市委常委、宣传部部长", "start_date": None, "end_date": None, "rank": "副厅级"},

    # 杨东生
    {"person_id": 9, "org_id": 1, "title": "眉山市委常委、组织部部长", "start_date": None, "end_date": None, "rank": "副厅级"},

    # 余华勇
    {"person_id": 10, "org_id": 17, "title": "眉山军分区政治委员", "start_date": None, "end_date": None, "rank": "正师级"},
    {"person_id": 10, "org_id": 1, "title": "眉山市委常委", "start_date": None, "end_date": None, "rank": "副厅级"},

    # 郑斌
    {"person_id": 11, "org_id": 1, "title": "眉山市委常委（挂职）", "start_date": None, "end_date": None, "rank": "挂职"},
    {"person_id": 11, "org_id": 2, "title": "副市长（挂职）", "start_date": None, "end_date": None, "rank": "挂职"},

    # 李建兴
    {"person_id": 12, "org_id": 2, "title": "副市长", "start_date": None, "end_date": None, "rank": "副厅级"},

    # 李鹏
    {"person_id": 13, "org_id": 2, "title": "副市长、市公安局局长", "start_date": None, "end_date": None, "rank": "副厅级"},

    # 戴林莉
    {"person_id": 14, "org_id": 2, "title": "副市长", "start_date": None, "end_date": None, "rank": "副厅级"},

    # 林双全
    {"person_id": 15, "org_id": 2, "title": "副市长", "start_date": None, "end_date": None, "rank": "副厅级"},

    # 田一澍
    {"person_id": 16, "org_id": 2, "title": "副市长（挂职）", "start_date": None, "end_date": None, "rank": "挂职"},

    # 车智勇
    {"person_id": 17, "org_id": 2, "title": "副市长", "start_date": None, "end_date": None, "rank": "副厅级"},

    # 周代军
    {"person_id": 18, "org_id": 2, "title": "副市长、洪雅县委书记", "start_date": None, "end_date": None, "rank": "副厅级"},

    # 郭红
    {"person_id": 19, "org_id": 2, "title": "市政府党组成员、天府新区眉山管委会主任", "start_date": None, "end_date": None, "rank": "正县级"},

    # 黄河 (前任)
    {"person_id": 20, "org_id": 1, "title": "眉山市委书记", "start_date": "2024-09", "end_date": "2026-05", "rank": "正厅级"},
    {"person_id": 20, "org_id": 2, "title": "眉山市市长", "start_date": "2021-09", "end_date": "2024-09", "rank": "正厅级"},
    {"person_id": 20, "org_id": 11, "title": "四川省交通运输厅党组书记、厅长", "start_date": "2026-05", "end_date": None, "rank": "正厅级"},

    # 胡元坤 (前任书记)
    {"person_id": 21, "org_id": 1, "title": "眉山市委书记", "start_date": "2021-07", "end_date": "2024-09", "rank": "正厅级"},
]

# ── Relationships ────────────────────────────────────────────────────────
RELATIONSHIPS = [
    # 党政搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "张道平（书记）与王斌达（市长）搭班子",
     "overlap_org": "中共眉山市委/眉山市人民政府", "overlap_period": "2026年5月至今"},
    # 书记+副书记
    {"person_a": 1, "person_b": 3, "type": "上下级",
     "context": "书记+专职副书记", "overlap_org": "中共眉山市委", "overlap_period": "2026年5月至今"},
    # 市长+专职副书记
    {"person_a": 2, "person_b": 3, "type": "同级协作",
     "context": "市长+专职副书记", "overlap_org": "中共眉山市委", "overlap_period": "现任"},
    # 书记+常务副市长
    {"person_a": 1, "person_b": 4, "type": "上下级",
     "context": "书记+常务副市长", "overlap_org": "中共眉山市委/市政府", "overlap_period": "2026年5月至今"},
    # 市长+常务副市长
    {"person_a": 2, "person_b": 4, "type": "上下级",
     "context": "市长+常务副市长", "overlap_org": "眉山市人民政府", "overlap_period": "现任"},
    # 书记+纪委书记
    {"person_a": 1, "person_b": 5, "type": "上下级",
     "context": "书记+纪委书记", "overlap_org": "中共眉山市委", "overlap_period": "2026年5月至今"},
    # 常委同事：政法委书记+常务副市长
    {"person_a": 4, "person_b": 6, "type": "常委同事",
     "context": "同届市委常委", "overlap_org": "中共眉山市委", "overlap_period": "现任"},
    # 常委同事：统战+宣传
    {"person_a": 7, "person_b": 8, "type": "常委同事",
     "context": "同届市委常委", "overlap_org": "中共眉山市委", "overlap_period": "现任"},
    # 常务副市长+宣传部长
    {"person_a": 4, "person_b": 8, "type": "常委同事",
     "context": "同届市委常委", "overlap_org": "中共眉山市委", "overlap_period": "现任"},
    # 组织部长+其他常委
    {"person_a": 9, "person_b": 6, "type": "常委同事",
     "context": "组织部长+其他常委", "overlap_org": "中共眉山市委", "overlap_period": "现任"},
    # 党政搭档（前任）
    {"person_a": 20, "person_b": 2, "type": "党政搭档",
     "context": "黄河（前书记/市长）与王斌达（市长）先后搭档",
     "overlap_org": "眉山市人民政府", "overlap_period": "2024-2026"},
    # 前任与现任（书记交接）
    {"person_a": 20, "person_b": 1, "type": "predecessor_successor",
     "context": "黄河→张道平 眉山市委书记交接",
     "overlap_org": "中共眉山市委", "overlap_period": "2026年5月"},
    # 前任与现任（书记）
    {"person_a": 21, "person_b": 20, "type": "predecessor_successor",
     "context": "胡元坤→黄河 眉山市委书记交接",
     "overlap_org": "中共眉山市委", "overlap_period": "2024年9月"},
    # 市长与各副市长（上下级关系）
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "市长+副市长（九三学社）", "overlap_org": "眉山市人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "市长+副市长/公安局局长", "overlap_org": "眉山市人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "市长+副市长", "overlap_org": "眉山市人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 15, "type": "上下级", "context": "市长+副市长", "overlap_org": "眉山市人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 16, "type": "上下级", "context": "市长+挂职副市长", "overlap_org": "眉山市人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 17, "type": "上下级", "context": "市长+副市长", "overlap_org": "眉山市人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 18, "type": "上下级", "context": "市长+副市长/洪雅县委书记", "overlap_org": "眉山市人民政府", "overlap_period": "现任"},
    # 常务副市长与各副市长
    {"person_a": 4, "person_b": 12, "type": "同级协作", "context": "常务副市长+其他副市长", "overlap_org": "眉山市人民政府", "overlap_period": "现任"},
    {"person_a": 4, "person_b": 13, "type": "同级协作", "context": "常务副市长+公安局长", "overlap_org": "眉山市人民政府", "overlap_period": "现任"},
    {"person_a": 4, "person_b": 14, "type": "同级协作", "context": "常务副市长+副市长", "overlap_org": "眉山市人民政府", "overlap_period": "现任"},
    {"person_a": 4, "person_b": 15, "type": "同级协作", "context": "常务副市长+副市长", "overlap_org": "眉山市人民政府", "overlap_period": "现任"},
    {"person_a": 4, "person_b": 17, "type": "同级协作", "context": "常务副市长+副市长", "overlap_org": "眉山市人民政府", "overlap_period": "现任"},
]

# ── Entry Point ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"Build complete: {SLUG}")