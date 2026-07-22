#!/usr/bin/env python3
"""
Build 青原区 (Qingyuan District, 吉安市, Jiangxi) government personnel
relationship network — SQLite database + GEXF graph.

青原区是江西省吉安市的一个市辖区，成立于2000年，位于赣江东岸。
调查日期: 2026-07-15

Targets: 区委书记 & 区长候选人

Sources:
- Baidu Baike: 青原区, 罗青球, 梁景晗, 郭远忠, 曾昭君, 王猛, 郑德亮
- 青原区人民政府官网 qyq.gov.cn
- 吉安市政府官网 jian.gov.cn
- 吉安市委组织部任前公示

Confidence: 核心领导人 (区委书记、政协主席、纪委书记) 经百度百科词条确认，置信度高。
          区长候选人黄海生刚于2026年7月15日任命，简历尚未公开。
          部分常委成员信息来自百度百科AI聚合，需进一步验证。
"""
import sqlite3
import os
import sys
from datetime import datetime

# ── Paths ────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "青原区_network.db")
GEXF_PATH = os.path.join(BASE, "青原区_network.gexf")

today = datetime.now().strftime("%Y-%m-%d")

# ── DATA ─────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════
    #  青原区 Core Leadership (as of 2026-07-15)
    # ══════════════════════════════════════════════════════════════════════

    # ── 区委书记 ────────────────────────────────────────────────────────
    {
        "id": 1,
        "name": "罗青球",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-10",
        "birthplace": "江西吉水",
        "education": "吉安师专中文系毕业，大学学历，硕士学位",
        "party_join": "1993-01",
        "work_start": "1993-07",
        "current_post": "青原区委书记",
        "current_org": "中共青原区委员会",
        "source": "baike.baidu.com/item/罗青球; qyq.gov.cn",
    },
    # ── 区长候选人 ──────────────────────────────────────────────────
    {
        "id": 2,
        "name": "黄海生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青原区委副书记、区长候选人",
        "current_org": "青原区人民政府",
        "source": "qyq.gov.cn 政务动态; 2026年7月15日任职通知",
    },
    # ── 区委副书记 ─────────────────────────────────────────────────
    {
        "id": 3,
        "name": "李艳辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-08",
        "birthplace": "",
        "education": "在职大专",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青原区委副书记",
        "current_org": "中共青原区委员会",
        "source": "百度百科-中共青原区委; qyq.gov.cn",
    },
    # ── 区纪委书记 ────────────────────────────────────────────────
    {
        "id": 4,
        "name": "郭远忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-06",
        "birthplace": "江西永丰",
        "education": "江西公安专科学校法律专业毕业",
        "party_join": "2007-06",
        "work_start": "2005-07",
        "current_post": "青原区委常委、区纪委书记、区监委主任",
        "current_org": "中共青原区纪委/监委",
        "source": "baike.baidu.com/item/郭远忠",
    },
    # ── 常务副区长 ────────────────────────────────────────────────
    {
        "id": 5,
        "name": "王琳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青原区委常委、常务副区长",
        "current_org": "青原区人民政府",
        "source": "qyq.gov.cn; 百度AI搜索",
    },
    # ── 组织部长 ────────────────────────────────────────────────
    {
        "id": 6,
        "name": "郭敏娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青原区委常委、组织部部长",
        "current_org": "中共青原区委组织部",
        "source": "qyq.gov.cn; 百度AI搜索",
    },
    # ── 统战部长 ────────────────────────────────────────────────
    {
        "id": 7,
        "name": "段晓新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青原区委常委、统战部部长",
        "current_org": "中共青原区委统战部",
        "source": "qyq.gov.cn; 百度AI搜索",
    },
    # ── 政法委书记 ──────────────────────────────────────────────
    {
        "id": 8,
        "name": "罗序章",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青原区委常委、政法委书记",
        "current_org": "中共青原区委政法委",
        "source": "qyq.gov.cn; 百度AI搜索",
    },
    # ── 区委常委、副区长 ─────────────────────────────────────────
    {
        "id": 9,
        "name": "郑德亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-09",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青原区委常委、副区长",
        "current_org": "青原区人民政府",
        "source": "baike.baidu.com/item/郑德亮",
    },
    # ── 挂职副区长 ──────────────────────────────────────────────
    {
        "id": 10,
        "name": "王猛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-10",
        "birthplace": "辽宁凌源",
        "education": "研究生学历",
        "party_join": "2006-06",
        "work_start": "2002-08",
        "current_post": "青原区委常委、副区长（挂职）",
        "current_org": "青原区人民政府",
        "source": "baike.baidu.com/item/王猛",
    },
    # ── 区人大常委会主任 ─────────────────────────────────────
    {
        "id": 11,
        "name": "李建春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-05",
        "birthplace": "江西吉安市青原区",
        "education": "大专学历",
        "party_join": "1999-03",
        "work_start": "1992-10",
        "current_post": "青原区人大常委会主任",
        "current_org": "青原区人大常委会",
        "source": "qyq.gov.cn; 2025年10月30日补选",
    },
    # ── 区政协主席 ────────────────────────────────────────────
    {
        "id": 12,
        "name": "梁景晗",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-07",
        "birthplace": "江西泰和",
        "education": "中央党校大学",
        "party_join": "1990-12",
        "work_start": "1984-12",
        "current_post": "青原区政协主席",
        "current_org": "青原区政协",
        "source": "baike.baidu.com/item/梁景晗",
    },
    # ── 副区长（公安） ──────────────────────────────────────────
    {
        "id": 13,
        "name": "龙森容",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青原区副区长、区公安分局局长",
        "current_org": "青原区公安分局",
        "source": "qyq.gov.cn; 百度AI搜索",
    },
    # ── 副区长 ─────────────────────────────────────────────────
    {
        "id": 14,
        "name": "周忠瑜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青原区副区长",
        "current_org": "青原区人民政府",
        "source": "qyq.gov.cn; 百度AI搜索",
    },
    # ── 副区长 ─────────────────────────────────────────────────
    {
        "id": 15,
        "name": "彭聪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青原区副区长",
        "current_org": "青原区人民政府",
        "source": "qyq.gov.cn; 百度AI搜索",
    },
    # ── 前任区长（调离） ──────────────────────────────────────
    {
        "id": 16,
        "name": "曾昭君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-12",
        "birthplace": "江西井冈山",
        "education": "南昌大学工商管理专业，在职研究生",
        "party_join": "2008-01",
        "work_start": "2009-06",
        "current_post": "（原青原区区长，已调任遂川县委副书记、县长候选人）",
        "current_org": "",
        "source": "baike.baidu.com/item/曾昭君; 遂川县人大任命公告",
    },
]

organizations = [
    {"id": 1, "name": "中共青原区委员会", "type": "党委", "level": "县处级",
     "parent": "中共吉安市委员会", "location": "江西吉安青原"},
    {"id": 2, "name": "青原区人民政府", "type": "政府", "level": "县处级",
     "parent": "吉安市人民政府", "location": "江西吉安青原"},
    {"id": 3, "name": "中共青原区纪律检查委员会/监委", "type": "党委", "level": "县处级",
     "parent": "中共吉安市纪委", "location": "江西吉安青原"},
    {"id": 4, "name": "青原区人大常委会", "type": "人大", "level": "县处级",
     "parent": "吉安市人大常委会", "location": "江西吉安青原"},
    {"id": 5, "name": "青原区政协", "type": "政协", "level": "县处级",
     "parent": "吉安市政协", "location": "江西吉安青原"},
    {"id": 6, "name": "中共青原区委组织部", "type": "党委", "level": "副处级",
     "parent": "中共青原区委", "location": "江西吉安青原"},
    {"id": 7, "name": "中共青原区委政法委员会", "type": "党委", "level": "副处级",
     "parent": "中共青原区委", "location": "江西吉安青原"},
    {"id": 8, "name": "中共青原区委统战部", "type": "党委", "level": "副处级",
     "parent": "中共青原区委", "location": "江西吉安青原"},
    {"id": 9, "name": "青原区公安分局", "type": "政府", "level": "乡科级",
     "parent": "青原区人民政府", "location": "江西吉安青原"},
    # 外部组织 - 罗青球的履历相关
    {"id": 10, "name": "吉安师范学校", "type": "事业单位", "level": "县处级",
     "parent": "吉安市", "location": "江西吉安"},
    {"id": 11, "name": "井冈山经贸学校", "type": "事业单位", "level": "县处级",
     "parent": "吉安市", "location": "江西吉安"},
    {"id": 12, "name": "吉安市医疗保险处", "type": "事业单位", "level": "乡科级",
     "parent": "吉安市人民政府", "location": "江西吉安"},
    {"id": 13, "name": "吉安市人民政府办公室", "type": "政府", "level": "县处级",
     "parent": "吉安市人民政府", "location": "江西吉安"},
    {"id": 14, "name": "中共吉安市委党校", "type": "事业单位", "level": "县处级",
     "parent": "中共吉安市委", "location": "江西吉安"},
    {"id": 15, "name": "中共吉州区委", "type": "党委", "level": "县处级",
     "parent": "中共吉安市委", "location": "江西吉安吉州"},
    {"id": 16, "name": "吉州区人民政府", "type": "政府", "level": "县处级",
     "parent": "吉安市人民政府", "location": "江西吉安吉州"},
    {"id": 17, "name": "中共安福县委", "type": "党委", "level": "县处级",
     "parent": "中共吉安市委", "location": "江西安福"},
    {"id": 18, "name": "安福县人民政府", "type": "政府", "level": "县处级",
     "parent": "吉安市人民政府", "location": "江西安福"},
    {"id": 19, "name": "中共万安县委", "type": "党委", "level": "县处级",
     "parent": "中共吉安市委", "location": "江西万安"},
    # 梁景晗履历相关
    {"id": 20, "name": "泰和县工商局", "type": "政府", "level": "乡科级",
     "parent": "泰和县人民政府", "location": "江西泰和"},
    {"id": 21, "name": "中共泰和县委办公室", "type": "党委", "level": "乡科级",
     "parent": "中共泰和县委", "location": "江西泰和"},
    {"id": 22, "name": "中共泰和县委", "type": "党委", "level": "县处级",
     "parent": "中共吉安市委", "location": "江西泰和"},
    {"id": 23, "name": "泰和县人民政府", "type": "政府", "level": "县处级",
     "parent": "吉安市人民政府", "location": "江西泰和"},
    {"id": 24, "name": "中共吉安县委", "type": "党委", "level": "县处级",
     "parent": "中共吉安市委", "location": "江西吉安县"},
    {"id": 25, "name": "吉安市公路局", "type": "事业单位", "level": "县处级",
     "parent": "吉安市人民政府", "location": "江西吉安"},
    {"id": 26, "name": "吉安市公安局特警支队", "type": "政府", "level": "乡科级",
     "parent": "吉安市公安局", "location": "江西吉安"},
    # 曾昭君去向组织
    {"id": 27, "name": "中共遂川县委", "type": "党委", "level": "县处级",
     "parent": "中共吉安市委", "location": "江西遂川"},
    {"id": 28, "name": "遂川县人民政府", "type": "政府", "level": "县处级",
     "parent": "吉安市人民政府", "location": "江西遂川"},
]

positions = [
    # ── 罗青球 — 完整履历（来源：百度百科）────────────────────────────
    {"id": 1, "person_id": 1, "org_id": 10,
     "title": "吉安师范学校教师", "start": "1993-07", "end": "~1995",
     "rank": "初级", "note": "吉安师专中文系毕业，留校/分配至吉安师范"},
    {"id": 2, "person_id": 1, "org_id": 11,
     "title": "井冈山经贸学校团委书记", "start": "~1995", "end": "~2000",
     "rank": "正科级", "note": ""},
    {"id": 3, "person_id": 1, "org_id": 12,
     "title": "吉安市医疗保险处负责人", "start": "~2000", "end": "~2003",
     "rank": "", "note": ""},
    {"id": 4, "person_id": 1, "org_id": 13,
     "title": "吉安市政府办公室干部", "start": "~2003", "end": "~2008",
     "rank": "", "note": ""},
    {"id": 5, "person_id": 1, "org_id": 14,
     "title": "吉安市委党校副校长", "start": "~2008", "end": "~2011",
     "rank": "副处级", "note": ""},
    {"id": 6, "person_id": 1, "org_id": 15,
     "title": "吉州区委常委", "start": "~2011", "end": "~2013",
     "rank": "副处级", "note": ""},
    {"id": 7, "person_id": 1, "org_id": 16,
     "title": "吉州区委常委、副区长", "start": "~2011", "end": "~2013",
     "rank": "副处级", "note": ""},
    {"id": 8, "person_id": 1, "org_id": 17,
     "title": "安福县委常委", "start": "~2013", "end": "~2016",
     "rank": "副处级", "note": ""},
    {"id": 9, "person_id": 1, "org_id": 18,
     "title": "安福县委常委、常务副县长", "start": "~2013", "end": "~2016",
     "rank": "副处级", "note": ""},
    {"id": 10, "person_id": 1, "org_id": 19,
     "title": "万安县委副书记", "start": "~2016", "end": "~2019",
     "rank": "副处级", "note": ""},
    {"id": 11, "person_id": 1, "org_id": 15,
     "title": "吉州区委副书记", "start": "~2019", "end": "2020-05",
     "rank": "副处级", "note": ""},
    {"id": 12, "person_id": 1, "org_id": 16,
     "title": "吉州区委副书记、区长", "start": "2020-05", "end": "2025-05",
     "rank": "正处级", "note": "2020年5月-2025年5月任吉州区区长"},
    {"id": 13, "person_id": 1, "org_id": 1,
     "title": "青原区委书记", "start": "2025-05", "end": "",
     "rank": "正处级", "note": "2025年5月任青原区委书记，现任"},

    # ── 黄海生 — 区长候选人（履历不完整）───────────────────────────
    {"id": 14, "person_id": 2, "org_id": 1,
     "title": "青原区委副书记", "start": "~2026-07", "end": "",
     "rank": "副处级", "note": "2026年7月15日任"},
    {"id": 15, "person_id": 2, "org_id": 2,
     "title": "青原区区长候选人", "start": "2026-07-15", "end": "",
     "rank": "正处级", "note": "区长候选人，等待人大补选"},

    # ── 李艳辉 ─────────────────────────────────────────────────────
    {"id": 16, "person_id": 3, "org_id": 2,
     "title": "青原区委常委、常务副区长",
     "start": "~2023", "end": "2025-03",
     "rank": "副处级", "note": "2025年3月21日辞去副区长职务"},
    {"id": 17, "person_id": 3, "org_id": 1,
     "title": "青原区委副书记",
     "start": "~2025-03", "end": "",
     "rank": "副处级", "note": "现任"},

    # ── 郭远忠 — 完整履历（来源：百度百科）─────────────────────────
    {"id": 18, "person_id": 4, "org_id": 25,
     "title": "吉安市公路局干部", "start": "2005-07", "end": "~2006",
     "rank": "", "note": "江西公安专科学校毕业"},
    {"id": 19, "person_id": 4, "org_id": 26,
     "title": "吉安市公安局特警支队干部", "start": "~2006", "end": "~2010",
     "rank": "", "note": ""},
    {"id": 20, "person_id": 4, "org_id": 15,
     "title": "吉州区委办公室干部", "start": "~2010", "end": "~2015",
     "rank": "", "note": ""},
    {"id": 21, "person_id": 4, "org_id": 15,
     "title": "吉州区兴桥镇/古南镇街道领导",
     "start": "~2015", "end": "~2018",
     "rank": "乡科级", "note": ""},
    {"id": 22, "person_id": 4, "org_id": 3,
     "title": "吉安市纪委干部",
     "start": "~2018", "end": "~2020",
     "rank": "副处级", "note": ""},
    {"id": 23, "person_id": 4, "org_id": 3,
     "title": "吉安市纪委第六审查调查室主任",
     "start": "~2020", "end": "2021-08",
     "rank": "副处级", "note": ""},
    {"id": 24, "person_id": 4, "org_id": 1,
     "title": "青原区委常委、区纪委书记",
     "start": "2021-08", "end": "",
     "rank": "副处级", "note": "2021年8月到任；2025年9月拟任县（市、区）委副书记"},

    # ── 王琳 ──────────────────────────────────────────────────────
    {"id": 25, "person_id": 5, "org_id": 1,
     "title": "青原区委常委", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    {"id": 26, "person_id": 5, "org_id": 2,
     "title": "青原区委常委、常务副区长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},

    # ── 郭敏娟 ──────────────────────────────────────────────────
    {"id": 27, "person_id": 6, "org_id": 1,
     "title": "青原区委常委", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    {"id": 28, "person_id": 6, "org_id": 6,
     "title": "青原区委常委、组织部部长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},

    # ── 段晓新 ──────────────────────────────────────────────────
    {"id": 29, "person_id": 7, "org_id": 1,
     "title": "青原区委常委", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    {"id": 30, "person_id": 7, "org_id": 8,
     "title": "青原区委常委、统战部部长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},

    # ── 罗序章 ──────────────────────────────────────────────────
    {"id": 31, "person_id": 8, "org_id": 1,
     "title": "青原区委常委", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    {"id": 32, "person_id": 8, "org_id": 7,
     "title": "青原区委常委、政法委书记", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},

    # ── 郑德亮 ──────────────────────────────────────────────────
    {"id": 33, "person_id": 9, "org_id": 1,
     "title": "青原区委常委", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    {"id": 34, "person_id": 9, "org_id": 2,
     "title": "青原区委常委、副区长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},

    # ── 王猛（挂职） ────────────────────────────────────────────
    {"id": 35, "person_id": 10, "org_id": 1,
     "title": "青原区委常委", "start": "", "end": "",
     "rank": "副处级", "note": "挂职"},
    {"id": 36, "person_id": 10, "org_id": 2,
     "title": "青原区委常委、副区长（挂职）", "start": "", "end": "",
     "rank": "副处级", "note": "现任，挂职"},

    # ── 李建春 ──────────────────────────────────────────────────
    {"id": 37, "person_id": 11, "org_id": 4,
     "title": "青原区人大常委会主任",
     "start": "2025-10-30", "end": "",
     "rank": "正处级", "note": "2025年10月30日补选，现任"},

    # ── 梁景晗 — 完整履历（来源：百度百科）─────────────────────────
    {"id": 38, "person_id": 12, "org_id": 20,
     "title": "泰和县工商局干部", "start": "1984-12", "end": "~1992",
     "rank": "", "note": "1984年12月参加工作"},
    {"id": 39, "person_id": 12, "org_id": 21,
     "title": "泰和县委办副科级干部", "start": "~1992", "end": "~1998",
     "rank": "副科级", "note": ""},
    {"id": 40, "person_id": 12, "org_id": 22,
     "title": "泰和县中龙乡党委书记", "start": "~1998", "end": "~2001",
     "rank": "正科级", "note": ""},
    {"id": 41, "person_id": 12, "org_id": 22,
     "title": "泰和县碧溪镇党委书记", "start": "~2001", "end": "~2006",
     "rank": "正科级", "note": ""},
    {"id": 42, "person_id": 12, "org_id": 22,
     "title": "泰和县委办公室主任", "start": "~2006", "end": "~2010",
     "rank": "正科级", "note": ""},
    {"id": 43, "person_id": 12, "org_id": 22,
     "title": "泰和县政协副主席、县委统战部部长",
     "start": "~2010", "end": "~2013",
     "rank": "副处级", "note": ""},
    {"id": 44, "person_id": 12, "org_id": 23,
     "title": "泰和县副县长", "start": "~2013", "end": "~2016",
     "rank": "副处级", "note": ""},
    {"id": 45, "person_id": 12, "org_id": 22,
     "title": "泰和县委常委、统战部部长",
     "start": "~2016", "end": "~2020",
     "rank": "副处级", "note": ""},
    {"id": 46, "person_id": 12, "org_id": 22,
     "title": "泰和县委常委、政法委书记",
     "start": "~2020", "end": "~2022",
     "rank": "副处级", "note": ""},
    {"id": 47, "person_id": 12, "org_id": 24,
     "title": "吉安县委副书记", "start": "~2022", "end": "2024-02",
     "rank": "副处级", "note": ""},
    {"id": 48, "person_id": 12, "org_id": 5,
     "title": "青原区政协主席", "start": "2024-02", "end": "",
     "rank": "正处级", "note": "现任"},

    # ── 龙森容 ──────────────────────────────────────────────────
    {"id": 49, "person_id": 13, "org_id": 2,
     "title": "青原区副区长", "start": "", "end": "",
     "rank": "副处级", "note": "现任；分管公安、司法、信访"},
    {"id": 50, "person_id": 13, "org_id": 9,
     "title": "青原区公安分局局长", "start": "", "end": "",
     "rank": "正科级", "note": "现任"},

    # ── 周忠瑜 ──────────────────────────────────────────────────
    {"id": 51, "person_id": 14, "org_id": 2,
     "title": "青原区副区长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},

    # ── 彭聪 ──────────────────────────────────────────────────
    {"id": 52, "person_id": 15, "org_id": 2,
     "title": "青原区副区长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},

    # ── 曾昭君（前任区长） ──────────────────────────────────────
    {"id": 53, "person_id": 16, "org_id": 2,
     "title": "青原区区长", "start": "~2021", "end": "~2026-07",
     "rank": "正处级", "note": "前任区长，任期约2021-2026年7月"},
    {"id": 54, "person_id": 16, "org_id": 27,
     "title": "遂川县委副书记、县长候选人",
     "start": "~2026-07", "end": "",
     "rank": "正处级", "note": "已调任"},
]

relationships = [
    # 党政搭档：区委书记 × 区长候选人
    {"id": 1, "person_a_id": 1, "person_b_id": 2,
     "type": "党政搭档",
     "context": "罗青球任区委书记，黄海生任区长候选人，为党政正职搭档",
     "overlap_org": "青原区", "overlap_period": "2026-07-至今"},

    # 前任区长 → 区长候选人
    {"id": 2, "person_a_id": 16, "person_b_id": 2,
     "type": "职位接替",
     "context": "曾昭君调任遂川后，黄海生接任区长候选人",
     "overlap_org": "青原区人民政府", "overlap_period": "2026-07"},

    # 区委书记与各常委的上下级关系
    {"id": 3, "person_a_id": 1, "person_b_id": 3,
     "type": "上下级",
     "context": "区委书记与区委副书记",
     "overlap_org": "中共青原区委员会", "overlap_period": "至今"},
    {"id": 4, "person_a_id": 1, "person_b_id": 4,
     "type": "上下级",
     "context": "区委书记与纪委书记",
     "overlap_org": "中共青原区委员会", "overlap_period": "2025-至今"},
    {"id": 5, "person_a_id": 1, "person_b_id": 5,
     "type": "上下级",
     "context": "区委书记与常务副区长",
     "overlap_org": "中共青原区委员会", "overlap_period": "至今"},
    {"id": 6, "person_a_id": 1, "person_b_id": 6,
     "type": "上下级",
     "context": "区委书记与组织部长",
     "overlap_org": "中共青原区委员会", "overlap_period": "至今"},
    {"id": 7, "person_a_id": 1, "person_b_id": 7,
     "type": "上下级",
     "context": "区委书记与统战部长",
     "overlap_org": "中共青原区委员会", "overlap_period": "至今"},
    {"id": 8, "person_a_id": 1, "person_b_id": 8,
     "type": "上下级",
     "context": "区委书记与政法委书记",
     "overlap_org": "中共青原区委员会", "overlap_period": "至今"},
    {"id": 9, "person_a_id": 1, "person_b_id": 9,
     "type": "上下级",
     "context": "区委书记与常委副区长",
     "overlap_org": "中共青原区委员会", "overlap_period": "至今"},

    # 四套班子关系
    {"id": 10, "person_a_id": 1, "person_b_id": 11,
     "type": "工作关系",
     "context": "区委书记与区人大主任",
     "overlap_org": "青原区", "overlap_period": "2025-至今"},
    {"id": 11, "person_a_id": 1, "person_b_id": 12,
     "type": "工作关系",
     "context": "区委书记与区政协主席",
     "overlap_org": "青原区", "overlap_period": "2025-至今"},

    # 区长与副职
    {"id": 12, "person_a_id": 2, "person_b_id": 5,
     "type": "上下级",
     "context": "区长候选人与常务副区长",
     "overlap_org": "青原区人民政府", "overlap_period": "至今"},
    {"id": 13, "person_a_id": 2, "person_b_id": 13,
     "type": "上下级",
     "context": "区长候选人与公安分局局长",
     "overlap_org": "青原区人民政府", "overlap_period": "至今"},
    {"id": 14, "person_a_id": 2, "person_b_id": 14,
     "type": "上下级",
     "context": "区长候选人与副区长",
     "overlap_org": "青原区人民政府", "overlap_period": "至今"},
    {"id": 15, "person_a_id": 2, "person_b_id": 15,
     "type": "上下级",
     "context": "区长候选人与副区长",
     "overlap_org": "青原区人民政府", "overlap_period": "至今"},

    # 罗青球与梁景晗：曾在吉安县搭班
    {"id": 16, "person_a_id": 1, "person_b_id": 12,
     "type": "工作关系",
     "context": "罗青球任吉州区区长期间，梁景晗任吉安县委副书记（两区相邻）",
     "overlap_org": "吉安市", "overlap_period": "2022-2024"},
]


# ── BUILD SQLite ─────────────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
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
        c.execute("INSERT INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"], p["work_start"],
                   p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("INSERT INTO organizations VALUES(?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT INTO positions VALUES(?,?,?,?,?,?,?,?)",
                  (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                   pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("INSERT INTO relationships VALUES(?,?,?,?,?,?,?)",
                  (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
                   r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()

    counts = {}
    for t in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {t}")
        counts[t] = c.fetchone()[0]
    conn.close()

    print(f"✓ SQLite DB created: {DB_PATH}")
    for t, n in counts.items():
        print(f"    {t}: {n}")
    return counts


# ── BUILD GEXF ───────────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    role = p.get("current_post", "")
    if "区委书记" in role and "副" not in role:
        return "255,50,50"  # Red for party secretary
    if "区长" in role and ("副" not in role or "常务" in role):
        return "50,100,255"  # Blue for government head
    if "纪委书记" in role or "纪检" in role:
        return "255,165,0"  # Orange for discipline
    if "人大" in role:
        return "60,180,75"  # Green
    if "政协" in role:
        return "60,180,75"  # Green
    return "100,100,100"  # Grey


def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    if "事业单位" in t:
        return "220,220,220"
    return "200,200,200"


def is_top_leader(p):
    return p["id"] in (1, 2, 11, 12)


def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append('    <description>青原区领导班子工作关系网络 - 区委书记罗青球 &amp; 区长候选人黄海生</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    for aid, atitle in [("0", "type"), ("1", "role"), ("2", "birth"), ("3", "birthplace"), ("4", "education")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    for aid, atitle in [("0", "type"), ("1", "context"), ("2", "start"), ("3", "end")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("birth", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birthplace", ""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("education", ""))}"/>')
        lines.append('        </attvalues>')
        rgb = c.split(",")
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('          <attvalue for="4" value=""/>')
        lines.append('        </attvalues>')
        rgb = c.split(",")
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')

    # Worked-at edges (person -> organization)
    for pos in positions:
        eid += 1
        weight = "1.0"
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("start", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos.get("end", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Relationship edges (person <-> person)
    for r in relationships:
        eid += 1
        weight = "2.0"
        lines.append(f'      <edge id="{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✓ GEXF graph created: {GEXF_PATH}")
    print(f"    Nodes: {len(persons) + len(organizations)}")
    print(f"    Edges: {len(positions) + len(relationships)}")


# ── MAIN ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"青原区 (Qingyuan District, 吉安市) 领导班子工作关系网络")
    print(f"Date: {today}")
    print(f"{'─' * 50}")
    print(f"调查说明：")
    print(f"- 核心领导数据来源：百度百科+青原区政府官网")
    print(f"- 区委书记罗青球、政协主席梁景晗、纪委书记郭远忠履历完整（百度百科）")
    print(f"- 区长候选人黄海生刚于2026年7月15日任命，简历尚未公开")
    print(f"- 部分常委/副区长姓名来自百度AI搜索聚合，需进一步核实")
    print(f"{'─' * 50}")
    build_db()
    build_gexf()
    print(f"{'─' * 50}")
    print(f"Done. Artifacts:")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
